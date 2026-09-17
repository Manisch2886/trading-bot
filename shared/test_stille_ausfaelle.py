"""
Selbsttests zu TB-45, Teil 1 und 2: eine Wache, die nicht mehr misst, sagt es
==============================================================================
Zwei Pruefer dieses Projekts stellten die Frage "ist die Datei veraendert?"
per `git diff --name-only origin/main` - und **sahen den Rueckgabewert von
git nicht an**:

  * `shared/test_kursdaten.py`        (Teil 1) - der Rueckgabewert wurde gar
    nicht gelesen. Schlug der Aufruf fehl, war `stdout` leer, und leer galt
    als "nichts veraendert". Gemessen in TB-43: **Rueckgabewert 128, trotzdem
    "bestanden"** - und die Schleifen ueber `forward_test.py` und
    `live_params.py` erzeugten dabei **null Pruefungen**.
  * `dashboard/test_portfolio_sicht.py` (Teil 2) - dort stand
    `lauf.returncode != 0 or not lauf.stdout.strip()`, derselbe blinde Fleck,
    nur ausdruecklich hingeschrieben: ein Fehlschlag ZAEHLTE als Erfolg.

DIE UNTERSCHEIDUNG, UM DIE ES GEHT (aus TB-43)
------------------------------------------------------------------------------
  * `daten_unberuehrt`-Sorte: ein leeres Ergebnis **ist** der Nachweis -
    "nichts veraendert" ist der Sollzustand.
  * Parameter-Sorte: ein leeres Ergebnis ist das **Fehlen** eines Nachweises.

Wer daraus "leer = immer Fehler" macht, bricht die erste Sorte. Deshalb wird
hier **beides** geprueft: dass ein gescheiterter Aufruf rot wird UND dass ein
gelungener Aufruf mit leerem Ergebnis gruen bleibt.

WIE GEPRUEFT WIRD - AM ABLAUF, NICHT AM QUELLTEXT
------------------------------------------------------------------------------
Eine Textsuche nach `returncode` waere wertlos: sie stuende auch dann gruen
da, wenn der Wert gelesen und verworfen wird. Stattdessen laeuft jeder der
beiden Pruefer wirklich, in einem **eigenen Prozess** (neun Bots fuehren
gleichnamige Module - TB-40), in einer Kopie des Arbeitsbaums, deren
git-Zustand dieser Test herstellt:

  Lage A  `origin/main` aufgeloest, nichts veraendert  -> muss GRUEN sein
  Lage B  `origin/main` nicht aufgeloest (rc 128)      -> muss ROT sein
  Lage C  `origin/main` aufgeloest, ein Parameterwert
          veraendert                                    -> muss ROT sein

Lage A ist die Negativ-Probe (sie faellt aus, wenn jemand "leer = Fehler"
schreibt), Lage C die Mutationsprobe (sie faellt aus, wenn die Wache ueberhaupt
nicht mehr beisst).

UND DIE GEGENPROBE AUF DEN BEFUND SELBST
------------------------------------------------------------------------------
Dieselbe Lage B laeuft zusaetzlich gegen die Fassung aus `origin/main` -
also gegen den unveraenderten Stand. Dort muss sie **gruen** sein. Genau das
ist der Befund: der alte Stand meldet "bestanden", ohne gemessen zu haben.
Faellt diese Gegenprobe eines Tages aus, weil `origin/main` die Reparatur
schon enthaelt, sagt der Test das und wertet sie nicht als Fehler.

Abschnitt 3 misst getrennt davon den bekannten Punkt T38.9: was der
Zwei-Punkt-Vergleich, die Drei-Punkt-Form und der Vergleich gegen die
Merge-Basis jeweils sehen - an einem eigens gebauten git-Repo, nicht an
einer Behauptung.

Abschnitt 4 weist die Randbedingung der Aufgabe nach: der Datenstand ist der
registrierte, und unter `data/` ist nichts veraendert.

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.

Nutzung:  python3 shared/test_stille_ausfaelle.py
"""

import os
import shutil
import subprocess
import sys
import tempfile

_SHARED = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED)

BESTANDEN = 0
FEHLER = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
        print(f"  [OK ] {name}" + (f"   {detail}" if detail else ""))
    else:
        FEHLER.append(name)
        print(f"  [FEHLER] {name}" + (f"   {detail}" if detail else ""))


def _git(ordner, *args, pruefe=True):
    lauf = subprocess.run(["git", "-C", ordner] + list(args),
                          capture_output=True, text=True)
    if pruefe and lauf.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args), lauf.stderr.strip()))
    return lauf


# ---------------------------------------------------------------------------
# Die Kopie des Arbeitsbaums
# ---------------------------------------------------------------------------
# Ohne `data/` (202 MB, und kein Prueffall hier liest eine Kursdatei) und ohne
# `.git` - die Kopie bekommt ihre eigene Geschichte, damit dieser Test am
# echten Repo NICHTS anfasst. Das ist keine Vorsicht um ihrer selbst willen:
# die Randbedingung der Aufgabe verlangt, dass der Datenstand vor und nach dem
# Lauf identisch ist.
_AUSGENOMMEN = shutil.ignore_patterns("data", ".git", "__pycache__", "*.pyc",
                                      "logs", "results", "*.db")


def _kopie_mit_eigener_geschichte(ziel):
    """Kopiert den Arbeitsbaum und legt `origin/main` auf genau diesen Stand.

    Wichtig: kopiert wird der ARBEITSBAUM, nicht ein Commit - sonst pruefte
    dieser Test die Fassung von vor der Reparatur.
    """
    shutil.copytree(BASE_DIR, ziel, ignore=_AUSGENOMMEN, symlinks=True)
    _git(ziel, "init", "-q", "-b", "main")
    _git(ziel, "config", "user.email", "test@trading-bot.invalid")
    _git(ziel, "config", "user.name", "TB-45")
    _git(ziel, "add", "-A")
    _git(ziel, "commit", "-q", "-m", "Stand des Arbeitsbaums")
    # `origin/main` ist nur eine Referenz - sie braucht keine Gegenstelle.
    _git(ziel, "update-ref", "refs/remotes/origin/main", "HEAD")
    return ziel


# Ein Treiber je Pruefer: er ruft GENAU den Abschnitt auf, der den git-Vergleich
# fuehrt, und meldet dessen Ergebnis als Zeilen zurueck. Kein `--nur`-Schalter
# in den gepruefen Dateien - die bleiben so, wie der Betrieb sie sieht.
_TREIBER = r'''
import json, os, sys
ordner, modulordner, modulname, funktion = sys.argv[1:5]
sys.path.insert(0, modulordner)
if os.path.isdir(os.path.join(ordner, "shared")):
    sys.path.insert(0, os.path.join(ordner, "shared"))
modul = __import__(modulname)
try:
    getattr(modul, funktion)()
    ausnahme = None
except Exception as fehler:                                    # noqa: BLE001
    ausnahme = "%s: %s" % (type(fehler).__name__, fehler)
print("###" + json.dumps({"bestanden": modul.BESTANDEN,
                          "fehler": list(modul.FEHLER),
                          "ausnahme": ausnahme}))
'''


def _abschnitt_laufen_lassen(ordner, datei, funktion):
    """Laesst einen Abschnitt eines Pruefers im Ordner `ordner` laufen.

    Eigener Prozess je Aufruf: die Pruefer haengen ihre Ergebnisse an
    Modulvariablen, und zwei Laeufe im selben Prozess wuerden sich vermischen.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as d:
        d.write(_TREIBER)
        treiber = d.name
    try:
        lauf = subprocess.run(
            [sys.executable, treiber, ordner,
             os.path.join(ordner, os.path.dirname(datei)),
             os.path.splitext(os.path.basename(datei))[0], funktion],
            capture_output=True, text=True, timeout=600, cwd=ordner)
    finally:
        os.unlink(treiber)
    import json
    for zeile in reversed(lauf.stdout.splitlines()):
        if zeile.startswith("###"):
            return json.loads(zeile[3:])
    return {"bestanden": 0, "fehler": ["<Treiber lief nicht>"],
            "ausnahme": (lauf.stderr or lauf.stdout)[-400:]}


# Die beiden Prueflinge: (Datei, Abschnitt, Kennsatz der neuen Wache).
# Der Kennsatz sagt Abschnitt 2, ob `origin/main` die Reparatur schon traegt -
# dann ist "gruen" dort kein Befund mehr, sondern der Sollzustand.
PRUEFLINGE = [
    ("shared/test_kursdaten.py", "test_verbreitung",
     "der Vergleich gegen origin/main kam zustande"),
    ("dashboard/test_portfolio_sicht.py", "test_grundsatz_kein_botcode",
     "der Vergleich gegen origin/main kam zustande"),
]


# ===========================================================================
# 1  Der blinde Fleck - am Ablauf, beide Pruefer, drei Lagen
# ===========================================================================
def teil_1():
    print("\n1) Ein gescheiterter git-Aufruf ist ein Fehlschlag, kein Erfolg")
    arbeit = tempfile.mkdtemp(prefix="tb45_kopie_")
    ordner = os.path.join(arbeit, "repo")
    try:
        _kopie_mit_eigener_geschichte(ordner)

        for datei, funktion, _wache in PRUEFLINGE:
            kurz = os.path.basename(datei)

            # -- Lage A: alles in Ordnung, leeres Ergebnis IST der Nachweis --
            a = _abschnitt_laufen_lassen(ordner, datei, funktion)
            check(f"{kurz}: Lage A (origin/main da, nichts veraendert) - gruen",
                  not a["fehler"] and a["ausnahme"] is None and a["bestanden"] > 0,
                  str(a["fehler"] or a["ausnahme"] or f"{a['bestanden']} Pruefungen"))

            # -- Lage B: origin/main nicht aufloesbar ------------------------
            _git(ordner, "update-ref", "-d", "refs/remotes/origin/main")
            b = _abschnitt_laufen_lassen(ordner, datei, funktion)
            check(f"{kurz}: Lage B (origin/main fehlt, rc 128) - ROT",
                  bool(b["fehler"]) and b["ausnahme"] is None,
                  str(b["fehler"])[:160] or "keine einzige Pruefung schlug an")
            check(f"{kurz}: Lage B nennt den gescheiterten Vergleich beim Namen",
                  any("Vergleich gegen origin/main" in f for f in b["fehler"]),
                  str(b["fehler"])[:160])

            # -- Und: keine der Aussagen darunter wird gruen gemeldet --------
            # Der eigentliche Schaden war nicht die fehlende Fehlermeldung,
            # sondern das falsche "bestanden" darunter.
            check(f"{kurz}: Lage B meldet nichts faelschlich als unveraendert",
                  b["bestanden"] < a["bestanden"],
                  f"{b['bestanden']} gruene Pruefungen statt {a['bestanden']}")

            _git(ordner, "update-ref", "refs/remotes/origin/main", "HEAD")

        # -- Lage C: Mutationsprobe, nur fuer den Parameter-Pruefer ----------
        # Eine echte Abweichung muss weiterhin auffallen - sonst haette man
        # eine Wache repariert, die gar nicht mehr beisst. Der Zustand wird
        # NICHT von Hand hergestellt: die Datei wird wirklich veraendert und
        # der Pruefer laeuft wirklich darueber.
        lp = os.path.join(ordner, "strategies", "t3_supertrend", "live_params.py")
        with open(lp, "r", encoding="utf-8") as d:
            urtext = d.read()
        with open(lp, "w", encoding="utf-8") as d:
            d.write(urtext.replace("STOP_LOSS_PCT = 4.0", "STOP_LOSS_PCT = 9.9"))
        c = _abschnitt_laufen_lassen(ordner, "shared/test_kursdaten.py",
                                     "test_verbreitung")
        check("test_kursdaten.py: Lage C (ein Parameterwert veraendert) - ROT",
              any("live_params.py" in f for f in c["fehler"]),
              str(c["fehler"])[:200])
        check("test_kursdaten.py: Lage C nennt den alten und den neuen Wert - "
              "die Schleife erzeugt also wirklich Pruefungen",
              c["bestanden"] > 0 and any("t3_supertrend" in f for f in c["fehler"]),
              str(c["fehler"])[:200])
        with open(lp, "w", encoding="utf-8") as d:
            d.write(urtext)
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


# ===========================================================================
# 2  Die Gegenprobe: derselbe Fall auf dem unveraenderten Stand
# ===========================================================================
def teil_2():
    print("\n2) Gegenprobe - der Stand aus origin/main meldet in Lage B "
          "'bestanden'")
    arbeit = tempfile.mkdtemp(prefix="tb45_alt_")
    ordner = os.path.join(arbeit, "repo")
    try:
        _kopie_mit_eigener_geschichte(ordner)
        for datei, funktion, wache in PRUEFLINGE:
            kurz = os.path.basename(datei)
            alt = _git(BASE_DIR, "show", f"origin/main:{datei}", pruefe=False)
            if alt.returncode != 0:
                check(f"{kurz}: Fassung aus origin/main lesbar", False,
                      alt.stderr.strip()[:120])
                continue
            ziel = os.path.join(ordner, datei)
            with open(ziel, "w", encoding="utf-8") as d:
                d.write(alt.stdout)
            _git(ordner, "add", "-A")
            _git(ordner, "commit", "-q", "-m", "alte Fassung")
            # Lage B: origin/main ist nicht aufloesbar.
            _git(ordner, "update-ref", "-d", "refs/remotes/origin/main")

            ergebnis = _abschnitt_laufen_lassen(ordner, datei, funktion)
            enthaelt_reparatur = wache in alt.stdout
            if enthaelt_reparatur:
                # origin/main traegt die Reparatur bereits - dann ist "gruen"
                # dort kein Befund mehr, sondern der Sollzustand.
                check(f"{kurz}: origin/main traegt die Reparatur bereits - "
                      f"Gegenprobe entfaellt", True, "kein Befund mehr")
            else:
                check(f"{kurz}: der unveraenderte Stand meldet in Lage B "
                      f"faelschlich 'bestanden' - DAS ist der Befund",
                      not ergebnis["fehler"] and ergebnis["ausnahme"] is None,
                      str(ergebnis["fehler"] or ergebnis["ausnahme"])[:160])
                check(f"{kurz}: und zwar mit {ergebnis['bestanden']} gruenen "
                      f"Pruefungen, ohne etwas gemessen zu haben",
                      ergebnis["bestanden"] > 0, ergebnis["bestanden"])
            # fuer den naechsten Pruefling zuruecksetzen
            _git(ordner, "checkout", "-q", "--", ".")
            _git(ordner, "update-ref", "refs/remotes/origin/main", "HEAD")
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)


# ===========================================================================
# 3  T38.9 - zwei Punkte, drei Punkte, Merge-Basis: was sieht welche Form?
# ===========================================================================
def _probe_repo(wurzel):
    """Baut die Lage nach, um die es bei T38.9 geht.

    * `main` ist seit dem Abzweig weitergezogen und hat dabei
      `forward_test.py` angefasst - legitim, und nicht von diesem Zweig.
    * Dieser Zweig hat `forward_test.py` NICHT angefasst.
    * Zusaetzlich liegt eine UNKOMMITTIERTE Aenderung an `forward_test.py`
      im Arbeitsbaum - genau die Lage, in der eine Sitzung ihren Pruefer
      laufen laesst, bevor sie committet.
    """
    fern, lokal = os.path.join(wurzel, "fern"), os.path.join(wurzel, "lokal")
    os.makedirs(fern)
    _git(fern, "init", "-q", "-b", "main")
    _git(fern, "config", "user.email", "t@t.invalid")
    _git(fern, "config", "user.name", "T")
    with open(os.path.join(fern, "forward_test.py"), "w") as d:
        d.write("TRADING_FEE_PCT = 0.1\n")
    _git(fern, "add", "-A")
    _git(fern, "commit", "-q", "-m", "basis")
    subprocess.run(["git", "clone", "-q", fern, lokal], check=True,
                   capture_output=True)
    _git(lokal, "config", "user.email", "t@t.invalid")
    _git(lokal, "config", "user.name", "T")
    _git(lokal, "checkout", "-qb", "zweig")
    # main zieht weiter und fasst dabei forward_test.py an
    with open(os.path.join(fern, "forward_test.py"), "a") as d:
        d.write("NEUE_ZEILE_AUS_MAIN = 1\n")
    _git(fern, "commit", "-qam", "main zieht weiter")
    _git(lokal, "fetch", "-q", "origin", "main")
    _git(lokal, "update-ref", "refs/remotes/origin/main", "FETCH_HEAD")
    return fern, lokal


def _namen(ordner, *revs):
    lauf = _git(ordner, "diff", "--name-only", *revs, pruefe=False)
    return sorted(z for z in lauf.stdout.splitlines() if z.strip()), lauf.returncode


def teil_3():
    print("\n3) T38.9 - Zwei-Punkt-, Drei-Punkt- und Merge-Basis-Vergleich, "
          "gemessen")
    wurzel = tempfile.mkdtemp(prefix="tb45_gitform_")
    try:
        _fern, lokal = _probe_repo(wurzel)
        basis = _git(lokal, "merge-base", "origin/main", "HEAD").stdout.strip()

        # -- (a) Der Zweig hat NICHTS angefasst -----------------------------
        zwei, _ = _namen(lokal, "origin/main")
        drei, _ = _namen(lokal, "origin/main...HEAD")
        mbasis, _ = _namen(lokal, basis)
        check("T38.9 bestaetigt: der Zwei-Punkt-Vergleich meldet eine Datei, "
              "die DIESER Zweig nie angefasst hat",
              zwei == ["forward_test.py"], str(zwei))
        check("die Drei-Punkt-Form meldet sie nicht - sie loest T38.9",
              drei == [], str(drei))
        check("der Vergleich gegen die Merge-Basis ebenfalls nicht",
              mbasis == [], str(mbasis))

        # -- (b) Und jetzt der Preis: eine unkommittierte Aenderung ---------
        with open(os.path.join(lokal, "forward_test.py"), "w") as d:
            d.write("TRADING_FEE_PCT = 0.2\n")
        zwei, _ = _namen(lokal, "origin/main")
        drei, _ = _namen(lokal, "origin/main...HEAD")
        mbasis, _ = _namen(lokal, basis)
        check("eine UNKOMMITTIERTE Parameteraenderung sieht der "
              "Zwei-Punkt-Vergleich", zwei == ["forward_test.py"], str(zwei))
        check("⚠ die Drei-Punkt-Form sieht sie NICHT - sie vergleicht zwei "
              "Commits, der Arbeitsbaum kommt darin nicht vor",
              drei == [], str(drei))
        check("der Vergleich gegen die Merge-Basis sieht sie - er loest T38.9, "
              "OHNE den Arbeitsbaum aufzugeben",
              mbasis == ["forward_test.py"], str(mbasis))

        # -- (c) Der Vorbehalt aus T43.2, ebenfalls gemessen ----------------
        # Ist der Zweig erst gemergt, ist die Merge-Basis der eigene Commit -
        # und beide Formen sehen nichts mehr. Das trifft die Drei-Punkt-Form
        # und den Merge-Basis-Vergleich gleichermassen.
        _git(lokal, "checkout", "-q", "--", ".")
        _git(lokal, "checkout", "-qb", "zweig2")
        with open(os.path.join(lokal, "forward_test.py"), "w") as d:
            d.write("TRADING_FEE_PCT = 0.3\n")
        _git(lokal, "commit", "-qam", "zweig aendert den Parameter")
        _git(lokal, "update-ref", "refs/remotes/origin/main", "HEAD")
        drei, _ = _namen(lokal, "origin/main...HEAD")
        basis2 = _git(lokal, "merge-base", "origin/main", "HEAD").stdout.strip()
        mbasis, _ = _namen(lokal, basis2)
        check("T43.2 bestaetigt: ist der Zweig gemergt, sieht die "
              "Drei-Punkt-Form seine eigene Aenderung nicht mehr",
              drei == [], str(drei))
        check("und der Merge-Basis-Vergleich ebenso wenig - der Vorbehalt "
              "trifft beide Formen gleich", mbasis == [], str(mbasis))

        # -- (d) Und der Fehlschlag, um den es in Teil 1 und 2 geht ---------
        _git(lokal, "update-ref", "-d", "refs/remotes/origin/main")
        namen, rc = _namen(lokal, "origin/main")
        check("fehlt origin/main, scheitert der Aufruf mit rc != 0 und "
              "LEERER Ausgabe - genau die Verwechslung aus Teil 1 und 2",
              rc != 0 and namen == [], f"rc={rc}, Ausgabe={namen}")
    finally:
        shutil.rmtree(wurzel, ignore_errors=True)


# ===========================================================================
# 4  Randbedingung der Aufgabe: keine Kursdatei veraendert
# ===========================================================================
def teil_4():
    """Der Datenstand vor und nach der Aufgabe - als Test, nicht als Zusage.

    `research/vorregistrierung/herkunft.py` fuehrt die Rechnung, die auch
    der Trockenlauf benutzt; verglichen wird gegen den registrierten Wert.
    Zusaetzlich - und das ist die andere Haelfte - gegen `origin/main`:
    eine Datei koennte geaendert und der Hash trotzdem gleich sein, wenn
    zwei Aenderungen sich aufheben, und eine NEUE Datei faellt in der
    Dateizahl auf, aber nicht in einem Hash ueber die alten.
    """
    print("\n4) Randbedingung: keine Kursdatei veraendert")
    sys.path.insert(0, os.path.join(BASE_DIR, "research", "vorregistrierung"))
    import herkunft                                            # noqa: PLC0415
    stand = herkunft.datenstand()
    check("der Datenstand ist der registrierte (d9449faf..., 223 Dateien)",
          stand["datenstand"].startswith("d9449faf") and stand["dateien"] == 223,
          "%s / %d" % (stand["datenstand"][:16], stand["dateien"]))

    geaendert, git_fehler = _geaenderte_dateien_hier()
    check("der git-Vergleich fuer diese Pruefung kam zustande",
          git_fehler is None, git_fehler or "")
    if git_fehler is None:
        unter_data = [z for z in geaendert if z.startswith("data/")]
        check("keine Datei unter data/ gegenueber origin/main veraendert",
              not unter_data, str(unter_data)[:200])
    lauf = _git(BASE_DIR, "status", "--porcelain", "--", "data", pruefe=False)
    offen = [z for z in lauf.stdout.splitlines() if z.strip()]
    check("und im Arbeitsbaum liegt unter data/ nichts Unversioniertes oder "
          "Geaendertes", lauf.returncode == 0 and not offen, str(offen)[:200])


def _geaenderte_dateien_hier(basis="origin/main"):
    lauf = _git(BASE_DIR, "diff", "--name-only", basis, pruefe=False)
    if lauf.returncode != 0:
        meldung = lauf.stderr.strip().splitlines()
        return [], ("git diff --name-only %s scheiterte (Rueckgabewert %d): %s"
                    % (basis, lauf.returncode,
                       meldung[0] if meldung else "ohne Meldung"))
    return [z for z in lauf.stdout.splitlines() if z.strip()], None


def main():
    print("=" * 78)
    print("TB-45, Teil 1 und 2: stille Ausfaelle zweier git-gestuetzter Wachen")
    print("=" * 78)
    for test in (teil_1, teil_2, teil_3, teil_4):
        try:
            test()
        except Exception as fehler:                            # noqa: BLE001
            import traceback
            FEHLER.append(f"{test.__name__} (Ausnahme)")
            print(f"  [FEHLER] {test.__name__} warf eine Ausnahme: {fehler}")
            traceback.print_exc()

    print("\n" + "=" * 78)
    gesamt = BESTANDEN + len(FEHLER)
    print(f"{BESTANDEN} von {gesamt} Pruefungen bestanden, {len(FEHLER)} fehlgeschlagen.")
    for name in FEHLER:
        print(f"  - {name}")
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())

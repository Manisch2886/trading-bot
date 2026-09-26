#!/usr/bin/env python3
"""
Selbsttests zu shared/paths.py - Sauberkeit ueber den Laufbereich (TB-112)
==============================================================================
Register 19, Kasten "Sauberkeit ueber den Laufbereich", vollzogen nach 42.2 E2
und 42.3 F8:

  E2  Die Sauberkeitspruefung des Arbeitsbaums erstreckt sich auf jeden Pfad
      des Laufbereichs, nicht nur auf `shared/`, `strategies/` und
      `requirements.lock`; `data/` bleibt ausgenommen.
  F8  Registrierte Protokolle sind ausgenommen wie `data/`, namentlich; heute
      genau eines: `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl`.

**Wie geprueft wird.** Ein **frischer Klon** des Projekts (`git clone` in einen
Wegwerfordner unter `$TMPDIR`, am Ende entfernt). In den Klon kommt die
Fassung von `shared/paths.py` **unter Pruefung** (die Datei neben diesem
Test) und wird dort committet, falls sie vom HEAD abweicht. Einstiegspunkt ist
eine unversionierte Datei in der Klonwurzel, die nur `import paths` macht; sie
liegt in keinem geprueften Pfad. Jede Probe startet einen eigenen Prozess
**unter dem Modus** (Snapshot des Klons, Commit des Klons). Der Arbeitsbaum
des Projekts wird **nicht** angefasst.

⭐ **Die Gegenprobe liest die Laufbereichsliste aus der Messdatei**, nicht aus
einem Literal (Bauart TB-107 G). ⚠️ Tatsache, keine Regel: am Tag-Commit
ersetzt die Tag-Messung diese Datei (Register 19 E2: "Die Liste der
geprueften Pfade steht als Tatsachennotiz neben der Laufbereichsmessung und
wird mit ihr am Tag-Commit erneuert"). Dann `LAUFBEREICH` unten umstellen.

⚠️ **Jede Probe hat ihre Mutationsgegenprobe**: eine Mutation, die nicht
greift, ist NICHT PRUEFBAR (FEHLER), nicht gruen.

Nutzung:  python3 shared/test_arbeitsbaum_laufbereich.py
"""

import os
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(_HIER)
_QUELLE = os.path.join(_HIER, "paths.py")

# Die Laufbereichsmessung (TB-112 A2, Werkzeug TB-104 D1, drei Lauf-Typen).
# ⚠️ Am Tag-Commit ersetzt die Tag-Messung diese Datei.
LAUFBEREICH = os.path.join(_WURZEL, "docs", "belege", "TB-112",
                           "a2_laufbereich.txt")
SNAPSHOT = "63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2"
EINSTIEG = "tb112_probe_einstieg.py"
PROTOKOLL = "research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl"
ERGEBNISSE = "research/vorregistrierung/ergebnisse"
RC_ERWARTET = 2
UMGEBUNG = ("TB_SELEKTIONSWURZEL", "TB_SELEKTIONSHASH", "TB_SELEKTIONSCOMMIT")

BESTANDEN = 0
FEHLER = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
        print("  [ok]     %s%s" % (name, (" - " + detail) if detail else ""))
    else:
        FEHLER.append(name)
        print("  [FEHLER] %s%s" % (name, (" - " + detail) if detail else ""))


def quelle():
    with open(_QUELLE, encoding="utf-8") as datei:
        return datei.read()


# ---------------------------------------------------------------------------
# Die Messdatei und die Deckung
# ---------------------------------------------------------------------------

def lies_laufbereich(pfad=LAUFBEREICH):
    """Die Pfade der Messung ohne Messumschlaege (`docs/`), sortiert."""
    pfade = []
    with open(pfad, encoding="utf-8") as datei:
        for zeile in datei:
            if zeile.startswith("#") or not zeile.strip():
                continue
            p = zeile.split("\t")[0].strip()
            if not p.startswith("docs/"):
                pfade.append(p)
    return sorted(pfade)


def gedeckt(pfad, tupel):
    """Ist `pfad` von einem Eintrag gedeckt - als Datei oder als Ordnerpraefix?"""
    return any(pfad == e or pfad.startswith(e.rstrip("/") + "/") for e in tupel)


def ungedeckt(pfade, tupel):
    return [p for p in pfade if not gedeckt(p, tupel)]


def lies_tupel(text):
    """ARBEITSBAUM_PFADE und REGISTRIERTE_PROTOKOLLE aus einer Quellfassung -
    per `exec` in einem leeren Namensraum, OHNE Modus (der Import-Teil laeuft
    dabei mit; ohne Modus tut er nichts, siehe test_startpruefungen N1)."""
    raum = {"__file__": _QUELLE, "__name__": "paths_probe"}
    exec(compile(text, _QUELLE, "exec"), raum)
    return raum["ARBEITSBAUM_PFADE"], raum["REGISTRIERTE_PROTOKOLLE"]


# ---------------------------------------------------------------------------
# Klon und Probeprozess
# ---------------------------------------------------------------------------

def _git(wurzel, *argumente):
    lauf = subprocess.run(["git", "-C", wurzel] + list(argumente),
                          capture_output=True, text=True)
    if lauf.returncode != 0:
        raise RuntimeError("git %s in %s: rc %d, %s"
                           % (" ".join(argumente), wurzel, lauf.returncode,
                              lauf.stderr.strip()))
    return lauf.stdout.strip()


def committe(klon, meldung):
    _git(klon, "add", "-A", "--", ".", ":(exclude)" + EINSTIEG)
    _git(klon, "-c", "user.name=tb112_test", "-c", "user.email=tb112@test",
         "commit", "-q", "--allow-empty", "-m", meldung)
    return _git(klon, "rev-parse", "HEAD")


def setze_paths(klon, text, meldung):
    with open(os.path.join(klon, "shared", "paths.py"), "w",
              encoding="utf-8") as datei:
        datei.write(text)
    return committe(klon, meldung)


def baue_klon():
    ordner = tempfile.mkdtemp(prefix="tb112_klon_")
    klon = os.path.join(ordner, "klon")
    subprocess.run(["git", "clone", "-q", _WURZEL, klon], check=True)
    with open(os.path.join(klon, EINSTIEG), "w", encoding="utf-8") as datei:
        datei.write("import os, sys\n"
                    "sys.path.insert(0, os.path.join(os.path.dirname("
                    "os.path.abspath(__file__)), 'shared'))\n"
                    "import paths\nprint('durchgelaufen')\n")
    return ordner, klon


def lauf(klon, commit_):
    umgebung = dict(os.environ)
    umgebung.update(TB_SELEKTIONSWURZEL=os.path.join(klon, "snapshots",
                                                     SNAPSHOT),
                    TB_SELEKTIONSHASH=SNAPSHOT, TB_SELEKTIONSCOMMIT=commit_)
    ergebnis = subprocess.run([sys.executable, "-W", "ignore", EINSTIEG],
                              cwd=klon, env=umgebung, capture_output=True,
                              text=True)
    return ergebnis.returncode, ergebnis.stderr


def angehaengt(klon, pfad):
    with open(os.path.join(klon, pfad), "a", encoding="utf-8") as datei:
        datei.write("\n# TB-112 Probe: uncommittete Aenderung\n")


def neu(klon, pfad, text="probe\n"):
    ziel = os.path.join(klon, pfad)
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    with open(ziel, "w", encoding="utf-8") as datei:
        datei.write(text)
    return ziel


def sauber(klon):
    """Den Klon auf seinen HEAD zuruecksetzen (ohne den Einstiegspunkt)."""
    _git(klon, "checkout", "--", ".")
    _git(klon, "clean", "-fdq", "-e", EINSTIEG)


def kurz(text, n=160):
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[:n] + "..."


# ===========================================================================
# Probe G - die Gegenprobe gegen die Messdatei (ohne Prozess)
# ===========================================================================

def probe_g_gegenprobe():
    print("\nProbe G - jeder Pfad der Laufbereichsmessung ist von "
          "ARBEITSBAUM_PFADE gedeckt")
    if not os.path.exists(LAUFBEREICH):
        check("G NICHT PRUEFBAR", False, "%s fehlt" % LAUFBEREICH)
        return None
    pfade = lies_laufbereich()
    tupel, _ = lies_tupel(quelle())
    check("G0 die Messdatei nennt Pfade", len(pfade) > 0,
          "%d Pfade ausserhalb docs/" % len(pfade))
    fehlt = ungedeckt(pfade, tupel)
    check("G1 Gegenprobe: jeder gemessene Pfad gedeckt (Praefix oder Datei)",
          not fehlt, "%d Pfade, %d Eintraege im Tupel, ungedeckt: %s"
          % (len(pfade), len(tupel), fehlt or "keiner"))
    aussen = [p for p in pfade if not gedeckt(p, ("shared", "strategies"))]
    check("G2 ausserhalb shared/strategies als EINZELDATEIEN im Tupel",
          all(p in tupel for p in aussen), "%d Module: %s"
          % (len(aussen), ", ".join(aussen)))
    # Mutation: je ein Eintrag entfernt. `requirements.lock` ist kein Modul
    # (TB-58, nicht aus der Messung) - sein Entfernen kann die Gegenprobe
    # nicht treffen und wird hier nur ausgewiesen.
    gebissen, nicht = 0, []
    for eintrag in tupel:
        if eintrag == "requirements.lock":
            continue
        rest = tuple(e for e in tupel if e != eintrag)
        if ungedeckt(pfade, rest):
            gebissen += 1
        else:
            nicht.append(eintrag)
    check("G3 Mutationsprobe: je ein Eintrag entfernt -> Gegenprobe rot",
          not nicht and gebissen == len(tupel) - 1,
          "%d von %d Mutationen beissen (requirements.lock ausgenommen: "
          "kein Modul)%s" % (gebissen, len(tupel) - 1,
                             ("; beissen nicht: %s" % nicht) if nicht else ""))
    return pfade


# ===========================================================================
# Probe K - Prozesse im frischen Klon, unter dem Modus
# ===========================================================================

def probe_k_klon(pfade):
    print("\nProbe K - frischer Klon, Prozesse unter dem Modus")
    ordner, klon = baue_klon()
    try:
        original = quelle()
        head = setze_paths(klon, original, "TB-112 Pruefstand paths.py")
        print("  Klon %s, Pruefstand %s" % (klon, head[:12]))

        rc, err = lauf(klon, head)
        check("K0 sauberer Klon -> rc 0", rc == 0, "rc=%d %s" % (rc, kurz(err)
                                                                 if rc else ""))
        angehaengt(klon, "shared/zuteilung.py")
        rc, err = lauf(klon, head)
        check("K0b Kontrolle: Aenderung unter shared/ -> rc 2", rc == RC_ERWARTET
              and "shared/zuteilung.py" in err, "rc=%d" % rc)
        sauber(klon)

        # K1: jedes Modul ausserhalb shared/strategies einzeln
        aussen = [p for p in pfade if not gedeckt(p, ("shared", "strategies"))]
        for pfad in aussen:
            angehaengt(klon, pfad)
            rc, err = lauf(klon, head)
            check("K1 %s veraendert -> rc 2, Meldung nennt die Datei" % pfad,
                  rc == RC_ERWARTET and "STARTPRUEFUNG VERLETZT" in err
                  and pfad in err, "rc=%d" % rc)
            sauber(klon)

        # K2: das registrierte Protokoll - neu angelegt
        neu(klon, PROTOKOLL, '{"probe": 1}\n')
        rc, err = lauf(klon, head)
        check("K2a herkunft_protokoll.jsonl neu angelegt -> rc 0",
              rc == 0, "rc=%d %s" % (rc, kurz(err) if rc else ""))
        # K2b: versioniert (Wegwerfcommit im Klon) und dann veraendert
        head_p = committe(klon, "TB-112 Probe: Protokoll versioniert")
        with open(os.path.join(klon, PROTOKOLL), "a") as datei:
            datei.write('{"probe": 2}\n')
        status = _git(klon, "status", "--porcelain", "--", PROTOKOLL)
        rc, err = lauf(klon, head_p)
        check("K2b herkunft_protokoll.jsonl versioniert und veraendert -> rc 0",
              rc == 0 and status.split()[:1] == ["M"],
              "git status [%s], rc=%d %s" % (status, rc,
                                             kurz(err) if rc else ""))
        sauber(klon)
        _git(klon, "reset", "-q", "--hard", head)

        # K3: neue Datei unter data/
        neu(klon, "data/XXX_TB112_1d.csv", "timestamp,close\n")
        rc, err = lauf(klon, head)
        check("K3 neue Datei unter data/ -> rc 0", rc == 0, "rc=%d" % rc)
        sauber(klon)

        # K4: Ausgabe eines frueheren Laufs unter ergebnisse/
        neu(klon, ERGEBNISSE + "/benchmark_frueherer_lauf.json", "{}\n")
        rc, err = lauf(klon, head)
        check("K4 neue, unversionierte Datei in %s/ -> rc 0" % ERGEBNISSE,
              rc == 0, "rc=%d" % rc)
        sauber(klon)

        # --- Mutation P: Ausnahme raus, ergebnisse/ als Ordner geprueft -----
        alt = ('+ [":(exclude)" + p for p in REGISTRIERTE_PROTOKOLLE]))')
        if original.count(alt) != 1:
            check("P Mutationsprobe NICHT PRUEFBAR", False,
                  "%r kommt %d-mal vor" % (alt, original.count(alt)))
        else:
            head_m = setze_paths(klon, original.replace(
                alt, '+ ["%s"]))' % ERGEBNISSE), "TB-112 Mutation P")
            neu(klon, PROTOKOLL, '{"probe": 1}\n')
            rc, err = lauf(klon, head_m)
            check("P1 Mutationsprobe beisst: ohne Ausnahme, ergebnisse/ als "
                  "Ordner -> Protokoll-Probe rot (rc 2)",
                  rc == RC_ERWARTET and "herkunft_protokoll.jsonl" in err,
                  "rc=%d" % rc)
            sauber(klon)
            # Tatsache: ohne Ausnahme und OHNE Ordner deckt heute kein
            # geprueftes Pfadstueck das Protokoll - die Ausnahme steht
            # namentlich, nicht, weil sie heute etwas bewirkt.
            head_m2 = setze_paths(klon, original.replace(alt, "))"),
                                  "TB-112 Mutation P2")
            neu(klon, PROTOKOLL, '{"probe": 1}\n')
            rc, err = lauf(klon, head_m2)
            check("P2 Tatsache: nur die Ausnahme entfernt -> weiter rc 0 "
                  "(heute deckt kein Pfad das Protokoll)", rc == 0,
                  "rc=%d" % rc)
            sauber(klon)
            _git(klon, "reset", "-q", "--hard", head)

        # --- Mutation T: das Tupel wie vor TB-112 -> K1 wird gruen ----------
        start = original.find("ARBEITSBAUM_PFADE = (\n")
        ende = original.find("\n)\n", start)
        if start < 0 or ende < 0:
            check("T Mutationsprobe NICHT PRUEFBAR", False,
                  "Tupel-Literal nicht gefunden")
        else:
            mutiert = (original[:start]
                       + 'ARBEITSBAUM_PFADE = ("shared", "strategies", LOCK)'
                       + original[ende + 3:])
            head_t = setze_paths(klon, mutiert, "TB-112 Mutation T")
            angehaengt(klon, "research/vorregistrierung/benchmark.py")
            rc, err = lauf(klon, head_t)
            check("T1 Mutationsprobe beisst: Tupel vor TB-112 -> benchmark.py "
                  "veraendert laeuft durch (rc 0, der Befund aus E2)",
                  rc == 0, "rc=%d" % rc)
            sauber(klon)
            _git(klon, "reset", "-q", "--hard", head)
    finally:
        shutil.rmtree(ordner, ignore_errors=True)
    check("Z Klon entfernt", not os.path.exists(ordner), ordner)


def main():
    print("=" * 78)
    print("Selbsttests zu shared/paths.py - Sauberkeit ueber den Laufbereich "
          "(TB-112)")
    print("=" * 78)
    for name in UMGEBUNG:
        if os.environ.pop(name, None) is not None:
            print("  ⚠️ %s war in der Umgebung gesetzt - fuer diese Proben "
                  "entfernt." % name)
    try:
        pfade = probe_g_gegenprobe()
    except Exception as fehler:                                # noqa: BLE001
        FEHLER.append("Probe G (Ausnahme)")
        print("  [FEHLER] Probe G warf eine Ausnahme: %s" % fehler)
        pfade = None
    if pfade:
        try:
            probe_k_klon(pfade)
        except Exception as fehler:                            # noqa: BLE001
            import traceback
            FEHLER.append("Probe K (Ausnahme)")
            print("  [FEHLER] Probe K warf eine Ausnahme: %s" % fehler)
            traceback.print_exc()
    print("\n" + "=" * 78)
    gesamt = BESTANDEN + len(FEHLER)
    print("%d von %d Pruefungen bestanden, %d fehlgeschlagen."
          % (BESTANDEN, gesamt, len(FEHLER)))
    for name in FEHLER:
        print("  - %s" % name)
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())

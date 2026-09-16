#!/usr/bin/env python3
"""
Selbsttest S-B1 - Vorbereitung (TB-39)
==============================================================================
Geprueft wird, was die Aufgabenstellung ausdruecklich verlangt:

  A  **Der Datenstand-Hash ist vor und nach der Aufgabe identisch** - am
     Verhalten geprueft, nicht behauptet.
  B  **Die Untergrenze wird geprueft, nicht angenommen:** bei weniger als
     acht Instrumenten ueber vier Anlageklassen meldet das Werkzeug
     Rueckgabewert 1. Die beiden Bedingungen werden EINZELN geprueft.
  C  **Die Entscheidungskerze-Regel gilt auch hier** - eine laufende
     Tageskerze landet nicht in den Daten.
  D  **Die Rasterzellen sind abzaehlbar und werden gezaehlt** - die Zahl
     entsteht aus der Liste, nicht aus einer Angabe im Text.
  E  Die Kostenrechnung haengt am Register und an nichts sonst.
  F  Das Register ist in sich schluessig.
  G-J **Mutationsproben.**

ZU DEN MUTATIONSPROBEN - DIE ZWEI WIEDERKEHRENDEN FALLEN
------------------------------------------------------------------------------
1. **Eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
   selbst.** Deshalb wird hier keine Variable umgebogen und anschliessend
   dieselbe Variable abgefragt. Jede Probe kopiert den Ordner in ein
   Wegwerf-Verzeichnis, aendert dort EINE Stelle und startet das Werkzeug als
   **eigenen Prozess**. Beobachtet wird der **ABLAUF**: welche Wachen
   durchlaufen werden, in welcher Reihenfolge, und was am Ende in der Datei
   steht. Jede Probe zeigt zuerst, dass sie OHNE Mutation das Richtige sieht -
   sonst belegte ein rotes Ergebnis nichts.
2. **Eine zweite Wache verdeckt das Fehlen der ersten.** `datenlauf.hole`
   fuehrt ZWEI Wachen hintereinander: `entferne_unvollstaendige` (eine
   Eigenschaft der ZEILE) und `nur_entscheidbar` (eine Eigenschaft der ZEIT).
   Teil H nimmt jede EINZELN heraus und weist nach, dass GENAU ihr Fehler
   auftritt und die jeweils andere Wache ihn NICHT auffaengt. Dieselbe Logik
   in Teil G fuer die beiden Haelften der Untergrenze.

WAS DIESER TEST IN DER CLOUD NICHT KANN - OFFEN, NICHT STILL
------------------------------------------------------------------------------
In der Cloud fehlen `pandas` und `yfinance`, und Yahoo ist gesperrt (403).
Teil C beobachtet deshalb den ABLAUF von `datenlauf.hole` mit einem
austauschbaren Abruf und mit Spitzeln ueber den beiden Wachen; die
Wachen selbst laufen dabei als **stdlib-Nachbau, der in diesem Testmodul
steht** - er kann nie zum Produktionspfad werden.

Der Durchlauf mit den ECHTEN Funktionen und ECHTEN Kursdaten steht als
Schritt im Testdokument `docs/TESTAUFTRAG_TB-39_sb1_vorbereitung.md`. Diese
Trennung ist Absicht und wird berichtet, nicht verschwiegen.
"""

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
if _HIER not in sys.path:
    sys.path.insert(0, _HIER)

import register as reg                                      # noqa: E402
import raster                                               # noqa: E402
import kosten                                               # noqa: E402
import historie                                             # noqa: E402
import datenstand                                           # noqa: E402
import beispieldaten                                        # noqa: E402

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, detail=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}" + (f"  [{detail}]" if detail else ""))


def _umgebung():
    """Die Umgebung fuer eine Wegwerf-Kopie.

    Eine Kopie unter /tmp findet `research/vorregistrierung` nicht mehr -
    ihr `BASE_DIR` zeigte sonst ins Leere. `TB39_BASE_DIR` weist sie auf das
    ECHTE Repo zurueck; ihr eigener Datenordner bleibt trotzdem der der
    Kopie, weil er relativ zur Moduldatei liegt.
    """
    umg = dict(os.environ)
    umg["TB39_BASE_DIR"] = reg.BASE_DIR
    return umg


def _lauf(skript, cwd=None):
    """Ein Wegwerf-Skript als EIGENER Prozess. Gibt (rc, stdout) zurueck."""
    e = subprocess.run([sys.executable, skript], capture_output=True,
                       text=True, cwd=cwd, env=_umgebung())
    return e.returncode, e.stdout + e.stderr


def _still(fn, *args, **kwargs):
    """Aufrufen, ohne dass die Konsolenausgabe den Testbericht zudeckt."""
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kwargs)


# ===========================================================================
# Teil A - Der Datenstand-Hash
# ===========================================================================
def teil_a():
    # A1 - der echte Stand deckt sich mit dem registrierten Literal.
    passt, ist = datenstand.stimmt_mit_soll()
    pruefe("A1: data/ traegt den registrierten Datenstand", passt,
           f"{ist['datenstand'][:12]}... / {ist['dateien']} Dateien")

    vorher = datenstand.stand()

    # A2 - der ganze Werkzeugsatz laeuft, und data/ bleibt Byte fuer Byte
    #      gleich. Beobachtet wird der Ablauf, nicht eine Zusicherung.
    with tempfile.TemporaryDirectory() as tmp:
        skript = os.path.join(tmp, "durchlauf.py")
        with open(skript, "w", encoding="utf-8") as fh:
            fh.write(
                "import sys, os\n"
                f"sys.path.insert(0, {_HIER!r})\n"
                "import beispieldaten, historie, raster, kosten, datenlauf\n"
                f"ziel = os.path.join({tmp!r}, 'daten')\n"
                "beispieldaten.erzeuge_bestand(ziel)\n"
                "datenlauf.schreibe_manifest(ziel)\n"
                "historie.bericht(ziel)\n"
                "raster.bericht()\n"
                "kosten.bericht()\n"
                "print('DURCH')\n")
            fh.flush()
        rc, aus = _lauf(skript)
        pruefe("A2: der Werkzeugsatz laeuft durch", rc == 0 and "DURCH" in aus,
               aus.strip()[-200:])

    nachher = datenstand.stand()
    pruefe("A3: data/ ist nach dem Lauf Byte fuer Byte unveraendert",
           vorher == nachher, f"{vorher} -> {nachher}")

    # A4 - die Wache reagiert ueberhaupt. Nachgebautes data/, nie das echte.
    with tempfile.TemporaryDirectory() as tmp:
        nachbau = os.path.join(tmp, "data")
        os.makedirs(nachbau)
        for name in ("A_1d.csv", "B_1d.csv"):
            with open(os.path.join(nachbau, name), "w", encoding="utf-8") as f:
                f.write("open_time,open,high,low,close,volume\n")
        eins = datenstand.stand(nachbau)
        with open(os.path.join(nachbau, "C_1d.csv"), "w",
                  encoding="utf-8") as f:
            f.write("open_time,open,high,low,close,volume\n")
        zwei = datenstand.stand(nachbau)
        pruefe("A4: EINE zusaetzliche Datei aendert den Hash - die Wache "
               "ist keine Attrappe",
               eins["datenstand"] != zwei["datenstand"]
               and zwei["dateien"] == eins["dateien"] + 1)

    # A5 - der Zielordner liegt ausserhalb von data/.
    draussen, _ = datenstand.ziel_liegt_ausserhalb()
    pruefe("A5: der ETF-Datenordner liegt ausserhalb von data/", draussen,
           reg.DATEN_DIR)
    drin, grund = datenstand.ziel_liegt_ausserhalb(
        os.path.join(reg.KURSDATEN_DIR_VERBOTEN, "etf"))
    pruefe("A6: und ein Ordner INNERHALB von data/ wird als solcher erkannt",
           (not drin) and bool(grund))


# ===========================================================================
# Teil B - Die Untergrenze, beide Haelften EINZELN
# ===========================================================================
def _bestand(tmp, symbole, von="2006-01-02"):
    """Beispieldaten fuer genau diese Symbole, alle mit demselben Anfang."""
    ziel = os.path.join(tmp, "daten")
    beispieldaten.erzeuge_bestand(
        ziel, bis="2010-12-31",
        von_je_symbol={s: von for s in symbole}, nur=set(symbole))
    return ziel


def teil_b():
    # Acht Instrumente ueber vier Klassen - genau die Untergrenze.
    acht_vier = ["SPY", "IWM", "EFA", "EEM",      # Aktien (4)
                 "IEF", "TLT",                    # Zinsen (2)
                 "LQD",                           # Kredit (1)
                 "GLD"]                           # Metalle (1)
    with tempfile.TemporaryDirectory() as tmp:
        ziel = _bestand(tmp, acht_vier)
        rc = _still(historie.main, ["--daten", ziel, "--bis-jahr", "2010"])
        b = historie.bericht(ziel, bis_jahr=2010)
        pruefe("B1: acht Instrumente ueber vier Klassen -> Rueckgabewert 0",
               rc == 0 and b["untergrenze"]["erfuellt"],
               f"rc={rc}")

    # Sieben Instrumente, immer noch vier Klassen.
    with tempfile.TemporaryDirectory() as tmp:
        # Sieben Symbole, weiterhin VIER Klassen: nur die Zahl faellt.
        ziel = _bestand(tmp, ["SPY", "IWM", "EFA", "EEM", "IEF", "LQD",
                              "GLD"])
        b = historie.bericht(ziel, bis_jahr=2010)
        u = b["untergrenze"]
        rc = _still(historie.main, ["--daten", ziel, "--bis-jahr", "2010"])
        pruefe("B2: SIEBEN Instrumente ueber vier Klassen -> "
               "Rueckgabewert 1", rc == 1, f"rc={rc}")
        pruefe("B2a: und zwar wegen der INSTRUMENTENZAHL, nicht wegen der "
               "Klassen",
               (not u["instrumente_erfuellt"]) and u["klassen_erfuellt"],
               f"{u['anzahl_instrumente']} Instrumente, "
               f"{u['anzahl_klassen']} Klassen")

    # Acht Instrumente, aber nur drei Klassen.
    acht_drei = ["SPY", "IWM", "EFA", "EEM",      # Aktien (4)
                 "IEF", "TLT",                    # Zinsen (2)
                 "LQD", "HYG"]                    # Kredit (2)
    with tempfile.TemporaryDirectory() as tmp:
        ziel = _bestand(tmp, acht_drei)
        b = historie.bericht(ziel, bis_jahr=2010)
        u = b["untergrenze"]
        rc = _still(historie.main, ["--daten", ziel, "--bis-jahr", "2010"])
        pruefe("B3: ACHT Instrumente ueber DREI Klassen -> Rueckgabewert 1",
               rc == 1, f"rc={rc}")
        pruefe("B3a: und zwar wegen der KLASSENZAHL, nicht wegen der "
               "Instrumente",
               u["instrumente_erfuellt"] and (not u["klassen_erfuellt"]),
               f"{u['anzahl_instrumente']} Instrumente, "
               f"{u['anzahl_klassen']} Klassen")

    # Der Vorlauf ist eine echte Schranke, keine Zierde.
    with tempfile.TemporaryDirectory() as tmp:
        ziel = _bestand(tmp, acht_vier, von="2009-06-01")
        b = historie.bericht(ziel, bis_jahr=2010)
        pruefe("B4: zu kurze Historie -> am Stichtag traegt nichts",
               b["untergrenze"]["anzahl_instrumente"] == 0,
               str(b["untergrenze"]["anzahl_instrumente"]))
        # Ein Jahr spaeter steht der Vorlauf.
        spaet = historie.untergrenze(b["messungen"], "2010-07-01")
        pruefe("B5: und ein Jahr spaeter tragen sie - der Vorlauf wird "
               "ABGEZAEHLT, nicht geschaetzt",
               spaet["anzahl_instrumente"] == len(acht_vier),
               str(spaet["anzahl_instrumente"]))


# ===========================================================================
# Teil C - Die Entscheidungskerze im ABLAUF
# ===========================================================================
# Der Beobachtungsaufbau steht als Quelltext hier und wird in den
# Wegwerf-Ordner geschrieben. Er bildet die beiden Wachen in reiner
# Standardbibliothek nach - dieser Nachbau liegt AUSSCHLIESSLICH im Test und
# kann nie zum Produktionspfad werden.
_ABLAUF_PROBE = r'''
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import datenlauf

ZIEL = sys.argv[1]
GRENZE = "2026-09-15"          # bis hierher ist die Kerze abgeschlossen
LAUFEND = "2026-09-16"         # diese Kerze laeuft noch
UNVOLLSTAENDIG = "2026-09-14"  # dieser Zeile fehlt ein Kursfeld

ABLAUF = []


class Rahmen:
    """Das Noetigste, damit der Ablauf beobachtbar ist: Zeilen und to_csv."""

    def __init__(self, zeilen):
        self.zeilen = list(zeilen)

    def __len__(self):
        return len(self.zeilen)

    def to_csv(self, pfad, index=False):
        with open(pfad, "w", encoding="utf-8", newline="") as fh:
            fh.write(",".join(datenlauf.SPALTEN) + "\n")
            for z in self.zeilen:
                fh.write(",".join(str(z[s]) for s in datenlauf.SPALTEN) + "\n")


def abruf(symbol, start, ende):
    ABLAUF.append("abruf")
    def zeile(tag, close):
        return {"open_time": tag, "open": 10.0, "high": 11.0, "low": 9.0,
                "close": close, "volume": 1000}
    return Rahmen([
        zeile("2026-09-11", 10.5),
        zeile(UNVOLLSTAENDIG, ""),      # fehlendes Kursfeld
        zeile(GRENZE, 10.7),
        zeile(LAUFEND, 10.8),           # laufende Kerze
    ])


def spitzel_unvollstaendig(df, symbol=None, melden=True):
    ABLAUF.append("entferne_unvollstaendige")
    behalten = [z for z in df.zeilen
                if all(str(z[s]).strip() != "" for s in
                       ("open", "high", "low", "close"))]
    return Rahmen(behalten), len(df.zeilen) - len(behalten)


def spitzel_entscheidbar(df, intervall, markt, startzeit=None, symbol=None,
                         melden=True, kalender=None):
    ABLAUF.append(f"nur_entscheidbar:{intervall}:{markt}")
    behalten = [z for z in df.zeilen if z["open_time"] <= GRENZE]
    return Rahmen(behalten), len(df.zeilen) - len(behalten), None


datenlauf.kursdaten.entferne_unvollstaendige = spitzel_unvollstaendig
datenlauf.ek.nur_entscheidbar = spitzel_entscheidbar

befund = datenlauf.hole("PROBE", ZIEL, abruf=abruf, melden=False)
with open(befund["pfad"], encoding="utf-8") as fh:
    zeilen = [z.strip().split(",")[0] for z in fh.read().splitlines()[1:]]

print(json.dumps({"ablauf": ABLAUF, "tage": zeilen, "befund": befund}))
'''


def _ablauf_probe(mutation=None):
    """Kopiert den Ordner, mutiert EINE Stelle, laeuft als eigener Prozess."""
    tmp = tempfile.mkdtemp()
    ordner = os.path.join(tmp, "etf_trendfolge")
    shutil.copytree(_HIER, ordner,
                    ignore=shutil.ignore_patterns("daten", "__pycache__",
                                                  "ergebnisse"))
    if mutation:
        pfad = os.path.join(ordner, "datenlauf.py")
        quelle = open(pfad, encoding="utf-8").read()
        alt, neu = mutation
        if alt not in quelle:
            shutil.rmtree(tmp, ignore_errors=True)
            return None, f"Mutationsstelle nicht gefunden: {alt[:40]}..."
        open(pfad, "w", encoding="utf-8").write(quelle.replace(alt, neu, 1))
    skript = os.path.join(ordner, "_ablauf_probe.py")
    open(skript, "w", encoding="utf-8").write(_ABLAUF_PROBE)
    ziel = os.path.join(tmp, "ausgabe")
    e = subprocess.run([sys.executable, skript, ziel],
                       capture_output=True, text=True, env=_umgebung())
    aus = e.stdout.strip().splitlines()
    ergebnis = None
    for zeile in aus:
        if zeile.startswith("{"):
            ergebnis = json.loads(zeile)
    shutil.rmtree(tmp, ignore_errors=True)
    return ergebnis, (e.stdout + e.stderr)


_MUT_ENTSCHEIDBAR = (
    """    df, verworfen, hinweis = ek.nur_entscheidbar(
        df, INTERVALL, MARKT, startzeit=startzeit, symbol=symbol,
        melden=melden)
""",
    "    verworfen, hinweis = 0, None\n")

_MUT_UNVOLLSTAENDIG = (
    """    df, gestrichen = kursdaten.entferne_unvollstaendige(
        roh, symbol=symbol, melden=melden)
""",
    "    df, gestrichen = roh, 0\n")


def teil_c():
    ergebnis, roh = _ablauf_probe()
    if ergebnis is None:
        pruefe("C0: der Beobachtungsaufbau laeuft", False, roh[-300:])
        return
    pruefe("C0: der Beobachtungsaufbau laeuft", True)
    pruefe("C1: der Ablauf ist abrufen -> entferne_unvollstaendige -> "
           "nur_entscheidbar",
           ergebnis["ablauf"][:2] == ["abruf", "entferne_unvollstaendige"]
           and ergebnis["ablauf"][2].startswith("nur_entscheidbar"),
           str(ergebnis["ablauf"]))
    pruefe("C2: gefragt wird mit Tagesintervall und Markt 'aktien'",
           ergebnis["ablauf"][2] == "nur_entscheidbar:1d:aktien",
           ergebnis["ablauf"][2])
    pruefe("C3: die LAUFENDE Tageskerze landet NICHT in der Datei",
           "2026-09-16" not in ergebnis["tage"], str(ergebnis["tage"]))
    pruefe("C4: die unvollstaendige Zeile landet NICHT in der Datei",
           "2026-09-14" not in ergebnis["tage"], str(ergebnis["tage"]))
    pruefe("C5: die abgeschlossene Kerze bleibt",
           "2026-09-15" in ergebnis["tage"], str(ergebnis["tage"]))
    pruefe("C6: beides wird GEZAEHLT, nicht still gestrichen",
           ergebnis["befund"]["unvollstaendig_gestrichen"] == 1
           and ergebnis["befund"]["nach_entscheidungskerze_verworfen"] == 1,
           json.dumps(ergebnis["befund"]))


# ===========================================================================
# Teil D - Die Rasterzellen
# ===========================================================================
def teil_d():
    zellen = raster.zellen()
    erwartet = 1
    for _name, werte in raster.achsen():
        erwartet *= len(werte)
    pruefe("D1: N ist die LAENGE der Zellenliste",
           raster.n() == len(zellen) == erwartet, f"{raster.n()} / {erwartet}")
    namen = [raster.zellenname(z) for z in zellen]
    pruefe("D2: jede Zelle hat einen eigenen Namen",
           len(set(namen)) == len(namen))
    pruefe("D3: N zaehlt zu den 653 der Neuselektion HINZU",
           raster.bericht()["N_gesamt_nominal"]
           == raster.N_HISTORISCH + raster.n())

    # Die Stufen sind die, die die Projektregel erzeugt - als Stolperdraht
    # gegen ein stilles Auseinanderlaufen mit registerdaten.py.
    pruefe("D4: die Stufen des Vol-Rueckblicks stehen fest",
           tuple(reg.VOL_RUECKBLICK_TAGE) == (42, 66, 103, 161, 252),
           str(reg.VOL_RUECKBLICK_TAGE))
    pruefe("D5: die Achsengrenzen sind Regeln ueber Frequenzen, keine "
           "getippten Zahlen",
           reg.VOL_RUECKBLICK_GRENZSATZ["unten"]
           == 2 * reg.HANDELSTAGE_JE_MONAT
           and reg.VOL_RUECKBLICK_GRENZSATZ["oben"]
           == max(reg.SIGNALFENSTER_TAGE))
    pruefe("D6: im Grenzsatz selbst steht keine Zahl",
           not any(c.isdigit() for c in
                   reg.VOL_RUECKBLICK_GRENZSATZ["satz"]),
           reg.VOL_RUECKBLICK_GRENZSATZ["satz"])

    # Die Nachbarschaft der Plateau-Regel.
    mitte = zellen[len(zellen) // 2]
    nachbarn = raster.nachbarn(mitte)
    pruefe("D7: ein innerer Punkt hat zwei Nachbarn, ein Randpunkt einen",
           len(nachbarn) == 2 and len(raster.nachbarn(zellen[0])) == 1,
           f"{len(nachbarn)} / {len(raster.nachbarn(zellen[0]))}")


# ===========================================================================
# Teil E - Kosten
# ===========================================================================
def teil_e():
    pruefe("E1: die Jahreskosten wachsen mit der Kipprate",
           kosten.jahreskosten_pct(1, 0) < kosten.jahreskosten_pct(2, 0)
           < kosten.jahreskosten_pct(3, 0))
    pruefe("E2: und mit dem Drift",
           kosten.jahreskosten_pct(2, 0.0) < kosten.jahreskosten_pct(2, 0.01))
    pruefe("E3: die obere Schranke ist zwoelf volle Umschlaege je Jahr",
           abs(kosten.vollumschlag_jahreskosten_pct()
               - reg.UMSCHICHTUNGEN_JE_JAHR * reg.KOSTEN_JE_ORDER_PCT) < 1e-12,
           str(kosten.vollumschlag_jahreskosten_pct()))
    pruefe("E4: ein voller Round Trip je Monat kostet doppelt so viel wie "
           "ein voller Umschlag je Monat",
           abs(kosten.vergleichszahl_se1_pct()
               - 2 * kosten.vollumschlag_jahreskosten_pct()) < 1e-12)
    # Die Instrumentenzahl kuerzt sich heraus - das ist die Aussage des
    # Moduls, und sie wird hier nachgerechnet statt geglaubt.
    def ueber_umschlag(n, w):
        kippungen_je_monat = n * w / reg.MONATE_JE_JAHR
        umschlag_je_monat = kippungen_je_monat / n
        return (reg.MONATE_JE_JAHR * umschlag_je_monat
                * reg.KOSTEN_JE_ORDER_PCT)
    pruefe("E5: acht und vierzehn Instrumente kosten bei gleicher Kipprate "
           "dasselbe",
           abs(ueber_umschlag(8, 3) - ueber_umschlag(14, 3)) < 1e-12
           and abs(ueber_umschlag(14, 3)
                   - kosten.jahreskosten_pct(3, 0)) < 1e-12)


# ===========================================================================
# Teil F - Das Register
# ===========================================================================
def teil_f():
    pruefe("F1: die Datenanforderung liegt VOR der Finanzkrise",
           reg.HISTORIE_AB < "2008-01-01", reg.HISTORIE_AB)
    pruefe("F2: die erste Selektionsfalte ist das Jahr nach der "
           "Datenanforderung",
           reg.ERSTE_SELEKTIONSFALTE == int(reg.HISTORIE_AB[:4]) + 1)
    pruefe("F3: freies Kapital wird NICHT verzinst",
           reg.KASSE_VERZINST is False and reg.KASSE_ZINSSATZ_PA == 0.0)
    pruefe("F4: die Mehrheit von drei Fenstern ist zwei",
           reg.SIGNAL_MEHRHEIT == 2
           and reg.SIGNAL_MEHRHEIT > len(reg.SIGNALFENSTER_MONATE) / 2)
    pruefe("F5: die Signalfenster sind Vielfache des Umschichtungsabstands",
           all(t % reg.HANDELSTAGE_JE_MONAT == 0
               for t in reg.SIGNALFENSTER_TAGE), str(reg.SIGNALFENSTER_TAGE))
    pruefe("F6: der Vorlauf ist das laengste Fenster, das gebraucht wird",
           reg.VORLAUF_TAGE == max(max(reg.SIGNALFENSTER_TAGE),
                                   max(reg.VOL_RUECKBLICK_TAGE)))
    pruefe("F7: GENAU EIN Benchmark hat einen Weg ins Urteil",
           reg.BENCHMARK_URTEIL["weg_ins_urteil"] is True
           and not any(b["weg_ins_urteil"] for b in reg.BENCHMARKS_BILD))
    pruefe("F8: der Urteilsbenchmark ist NICHT Aktien-Buy-and-Hold",
           "buy_and_hold" not in reg.BENCHMARK_URTEIL["name"],
           reg.BENCHMARK_URTEIL["name"])
    pruefe("F9: ein Round Trip sind zwei Orders",
           abs(reg.KOSTEN_JE_ROUNDTRIP_PCT
               - 2 * reg.KOSTEN_JE_ORDER_PCT) < 1e-12
           and abs(reg.KOSTEN_JE_ROUNDTRIP_PCT - 0.30) < 1e-12)
    pruefe("F10: der Survivorship-Vorbehalt nennt eine ERWARTETE RICHTUNG",
           "Erwartete Richtung" in reg.SURVIVORSHIP_VORBEHALT)
    pruefe("F11: die Kandidatenliste deckt mindestens die Untergrenze ab",
           len(reg.KANDIDATEN) >= reg.UNTERGRENZE_INSTRUMENTE
           and len({k["klasse"] for k in reg.KANDIDATEN})
           >= reg.UNTERGRENZE_KLASSEN)
    pruefe("F12: die Blocklaenge des Bootstraps wird BERECHNET, nicht gesetzt",
           "BERECHNET" in reg.BOOTSTRAP_BLOCKLAENGE_SATZ
           and reg.BOOTSTRAP_ZIEHUNGEN == 2000)
    pruefe("F13: es gibt keine Mindestzahl Trades je Falte",
           reg.BOOTSTRAP_MINDESTZAHL_TRADES is None)
    pruefe("F14: Verfahren B kennt kein Mindesttraining",
           reg.VERFAHREN == "B" and reg.FALTEN_MINDESTTRAINING is None
           and reg.FALTEN_MINDESTZAHL == 3)
    pruefe("F15: das Embargo ist eine REGEL, keine geratene Zahl",
           isinstance(reg.EMBARGO_REGEL, str)
           and "gemessen" in reg.EMBARGO_REGEL.lower())


# ===========================================================================
# Teil G - Mutationsprobe: die beiden Haelften der Untergrenze
# ===========================================================================
def _historie_mutiert(mutation, ziel, bis_jahr=2010):
    """`historie.py` mit EINER geaenderten Stelle, als eigener Prozess."""
    tmp = tempfile.mkdtemp()
    ordner = os.path.join(tmp, "etf_trendfolge")
    shutil.copytree(_HIER, ordner,
                    ignore=shutil.ignore_patterns("daten", "__pycache__",
                                                  "ergebnisse"))
    pfad = os.path.join(ordner, "historie.py")
    quelle = open(pfad, encoding="utf-8").read()
    alt, neu = mutation
    if alt not in quelle:
        shutil.rmtree(tmp, ignore_errors=True)
        return None, f"Mutationsstelle nicht gefunden: {alt[:40]}"
    open(pfad, "w", encoding="utf-8").write(quelle.replace(alt, neu, 1))
    e = subprocess.run([sys.executable, os.path.join(ordner, "historie.py"),
                        "--daten", ziel, "--bis-jahr", str(bis_jahr)],
                       capture_output=True, text=True, env=_umgebung())
    shutil.rmtree(tmp, ignore_errors=True)
    return e.returncode, e.stdout + e.stderr


def teil_g():
    acht_drei = ["SPY", "IWM", "EFA", "EEM", "IEF", "TLT", "LQD", "HYG"]
    sieben_vier = ["SPY", "IWM", "EFA", "EEM", "IEF", "LQD", "GLD"]

    with tempfile.TemporaryDirectory() as tmp:
        ziel = _bestand(tmp, acht_drei)
        rc, _ = _historie_mutiert(
            ("klassen_erfuellt = len(klassen) >= reg.UNTERGRENZE_KLASSEN",
             "klassen_erfuellt = True"), ziel)
        pruefe("G1: faellt die KLASSEN-Wache weg, geht der Fall mit acht "
               "Instrumenten ueber drei Klassen durch - die "
               "Instrumenten-Wache faengt ihn NICHT auf",
               rc == 0, f"rc={rc}")

    with tempfile.TemporaryDirectory() as tmp:
        ziel = _bestand(tmp, sieben_vier)
        rc, _ = _historie_mutiert(
            ("instrumente_erfuellt = len(symbole) >= "
             "reg.UNTERGRENZE_INSTRUMENTE",
             "instrumente_erfuellt = True"), ziel)
        pruefe("G2: faellt die INSTRUMENTEN-Wache weg, geht der Fall mit "
               "sieben Instrumenten durch - die Klassen-Wache faengt ihn "
               "NICHT auf",
               rc == 0, f"rc={rc}")

    # Und die Gegenprobe: OHNE Mutation faellt jeder der beiden Faelle.
    for name, symbole in (("acht ueber drei", acht_drei),
                          ("sieben ueber vier", sieben_vier)):
        with tempfile.TemporaryDirectory() as tmp:
            ziel = _bestand(tmp, symbole)
            e = subprocess.run(
                [sys.executable, os.path.join(_HIER, "historie.py"),
                 "--daten", ziel, "--bis-jahr", "2010"],
                capture_output=True, text=True, env=_umgebung())
            pruefe(f"G3: ohne Mutation faellt '{name}' durch",
                   e.returncode == 1, f"rc={e.returncode}")


# ===========================================================================
# Teil H - Mutationsprobe: die beiden Wachen des Datenlaufs
# ===========================================================================
def teil_h():
    ohne_zeit, roh = _ablauf_probe(_MUT_ENTSCHEIDBAR)
    if ohne_zeit is None:
        pruefe("H1: die Probe ohne Zeit-Wache laeuft", False, roh[-300:])
    else:
        pruefe("H1: ohne `nur_entscheidbar` landet die LAUFENDE Kerze in "
               "der Datei", "2026-09-16" in ohne_zeit["tage"],
               str(ohne_zeit["tage"]))
        pruefe("H2: und die unvollstaendige Zeile wird trotzdem noch "
               "gestrichen - die erste Wache VERDECKT das Fehlen der "
               "zweiten nicht",
               "2026-09-14" not in ohne_zeit["tage"],
               str(ohne_zeit["tage"]))
        pruefe("H3: der Ablauf zeigt die fehlende Wache",
               not any(s.startswith("nur_entscheidbar")
                       for s in ohne_zeit["ablauf"]),
               str(ohne_zeit["ablauf"]))

    ohne_zeile, roh = _ablauf_probe(_MUT_UNVOLLSTAENDIG)
    if ohne_zeile is None:
        pruefe("H4: die Probe ohne Zeilen-Wache laeuft", False, roh[-300:])
    else:
        pruefe("H4: ohne `entferne_unvollstaendige` landet die "
               "unvollstaendige Zeile in der Datei",
               "2026-09-14" in ohne_zeile["tage"], str(ohne_zeile["tage"]))
        pruefe("H5: und die laufende Kerze wird trotzdem noch verworfen - "
               "die zweite Wache VERDECKT das Fehlen der ersten nicht",
               "2026-09-16" not in ohne_zeile["tage"],
               str(ohne_zeile["tage"]))
        pruefe("H6: der Ablauf zeigt die fehlende Wache",
               "entferne_unvollstaendige" not in ohne_zeile["ablauf"],
               str(ohne_zeile["ablauf"]))


# ===========================================================================
# Teil I - Mutationsprobe: N kommt aus der Liste, nicht aus dem Text
# ===========================================================================
def teil_i():
    tmp = tempfile.mkdtemp()
    try:
        skript = os.path.join(tmp, "n_probe.py")
        with open(skript, "w", encoding="utf-8") as fh:
            fh.write(
                "import sys\n"
                f"sys.path.insert(0, {_HIER!r})\n"
                "import register as reg\n"
                "reg.VOL_RUECKBLICK_TAGE = (1, 2, 3)\n"
                "import raster\n"
                "print(raster.n(), len(raster.zellen()))\n")
        rc, aus = _lauf(skript)
        zahlen = aus.strip().split()
        pruefe("I1: eine geaenderte Achse aendert N - die Zahl entsteht aus "
               "der Liste",
               rc == 0 and zahlen[:2] == ["3", "3"], aus.strip()[-200:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # Und die Gegenprobe: unveraendert kommt die registrierte Zahl heraus.
    pruefe("I2: unveraendert ist N die Zahl des Registers",
           raster.n() == len(reg.VOL_RUECKBLICK_TAGE), str(raster.n()))

    # Dasselbe fuer die Kosten: sie haengen am Register, nicht an einer
    # Abschrift.
    tmp = tempfile.mkdtemp()
    try:
        skript = os.path.join(tmp, "kosten_probe.py")
        with open(skript, "w", encoding="utf-8") as fh:
            fh.write(
                "import sys\n"
                f"sys.path.insert(0, {_HIER!r})\n"
                "import register as reg\n"
                "reg.KOSTEN_JE_ORDER_PCT = 1.0\n"
                "import kosten\n"
                "print(kosten.jahreskosten_pct(3, 0.0))\n")
        rc, aus = _lauf(skript)
        pruefe("I3: eine geaenderte Kostenkonvention aendert die "
               "Kostenrechnung",
               rc == 0 and abs(float(aus.strip().splitlines()[-1]) - 3.0)
               < 1e-9, aus.strip()[-200:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ===========================================================================
# Teil J - Mutationsprobe: der Zielordner darf nicht nach data/ wandern
# ===========================================================================
def teil_j():
    vorher = datenstand.stand()
    verboten = os.path.join(reg.KURSDATEN_DIR_VERBOTEN, "etf_trendfolge_probe")
    import datenlauf                                        # noqa: PLC0415
    rc = _still(datenlauf.main, ["--ziel", verboten])
    pruefe("J1: ein Zielordner INNERHALB von data/ bricht den Datenlauf ab",
           rc == 1, f"rc={rc}")
    pruefe("J2: und es ist dabei nichts entstanden",
           not os.path.exists(verboten), verboten)
    if os.path.exists(verboten):                    # Notaufraeumen
        shutil.rmtree(verboten, ignore_errors=True)
    pruefe("J3: data/ ist unveraendert", datenstand.stand() == vorher)

    # Die Gegenprobe: derselbe Aufruf mit einem Ziel AUSSERHALB von data/
    # kommt an der Wache vorbei (und scheitert dann an yfinance, nicht an
    # ihr - genau das soll er in der Cloud).
    with tempfile.TemporaryDirectory() as tmp:
        e = subprocess.run(
            [sys.executable, os.path.join(_HIER, "datenlauf.py"),
             "--ziel", os.path.join(tmp, "daten"), "--pruefen"],
            capture_output=True, text=True, env=_umgebung())
        pruefe("J4: ein Ziel AUSSERHALB von data/ kommt an der Wache vorbei",
               e.returncode == 0, e.stdout[-200:] + e.stderr[-200:])


def main():
    print(__doc__.strip().split("\n")[0])
    print("=" * 78)
    for name, teil in (("A", teil_a), ("B", teil_b), ("C", teil_c),
                       ("D", teil_d), ("E", teil_e), ("F", teil_f),
                       ("G", teil_g), ("H", teil_h), ("I", teil_i),
                       ("J", teil_j)):
        print(f"  Teil {name} ...", flush=True)
        teil()
    print("\n" + "=" * 78)
    if gescheitert:
        print(f"{bestanden} bestanden, {len(gescheitert)} GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
        return 1
    print(f"{bestanden}/{bestanden} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

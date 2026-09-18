#!/usr/bin/env python3
"""
Mass 2 - kein eigener Datenpfad im Selektionspfad (TB-52, Teil 2.3)
==============================================================================
Ueber die 90 Selektionsmodule: **keines bezieht einen Datenpfad ausserhalb des
Resolvers** (`shared/paths.py`). Am Syntaxbaum heisst das: kein
`os.path.join(...)`, kein f-String, kein `Path(...)`, keine %-Formatierung und
keine blanke Konstante, die auf `data`, `data/` oder eine bekannte
Kursdatei-Endung fuehrt, ohne ueber `shared/paths.py` zu gehen.

⚠️⚠️ Gemessen am **Syntaxbaum**, nicht per Textsuche (Prueffrage B5).

---------------------------------------------------------------------------
⭐ **Was dieses Mass beim ersten Lauf gefunden hat - und warum es zaehlt**
---------------------------------------------------------------------------
**Keines der 90 Selektionsmodule importiert `shared/paths.py`.** Nicht eines.
**71 von 90** beziehen ihre Pfade aus `shared/strategy_paths.py`, und das
leitet `DATA_DIR` **selbst** ab:

    "DATA_DIR": os.path.join(base_dir, "data")     # strategy_paths.py

⚠️ **Damit erreicht der Selektionsmodus aus TB-52 heute kein einziges der 90
Module.** Er waere gesetzt, und alle 90 laesen weiter aus dem Live-Bestand -
still. Das ist Fables Einwand, eine Ebene hoeher: *die Wache steht nicht dort,
wo gefragt wird.*

⭐ **Genau deshalb ist dieses Mass gebaut worden, und genau deshalb zaehlt es
den Bezug aus `strategy_paths` mit.** Ein Modul, das zentral versorgt ist,
aber von der **falschen** Mitte, ist fuer den Modus so unerreichbar wie eines,
das seinen Pfad selbst zusammensetzt.

⚠️ **Dieses Mass aendert nichts** - es liest und zaehlt. Die 90 zu verdrahten
ist TB-53; **welche** Mitte dann die richtige ist, ist dort zu entscheiden.

⭐ **Bauform: Sperrklinke, nicht Wache** (Prueffrage A4) - gruen, solange der
Stand nicht groesser wird als die Ausgangszahl. ⭐ Der Test misst damit den
**Umbau**, nicht sein Ergebnis.

Nutzung:  python3 research/selektionsmasse/test_eigener_pfadbau.py
          (⚠️ **ohne Argument** - Prueffrage A3. Er laeuft im Basislauf mit.)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import masse                                                   # noqa: E402

# ===========================================================================
# ⭐ DIE AUSGANGSZAHL
# ===========================================================================
# Gemessen am 18.09.2026 (TB-52) ueber die 90 Selektionsmodule: **29** Fund-
# stellen in **29** Modulen, alle von einer Art - `_P["DATA_DIR"]` bzw.
# `_P["CONFIG_DIR"]` aus `shared/strategy_paths.py`. **Null** Modul setzt
# einen Datenpfad im eigenen Quelltext zusammen.
#
# ⚠️⚠️ **Diese 29 sind NICHT die 29 aus `research/datenordner_schnitt`**
# (Prueffrage C7 - zwei Zahlen, zwei Fragen). Dort sind es 29 Module, die
# einen Pfad **selbst bauen**, und **kein einziges davon ist ein
# Selektionsmodul** (16 Untersuchung, 7 Pruefwerkzeug, 6 Betrieb). Hier sind
# es 29 **Selektionsmodule**, die ihn aus der zweiten Quelle ziehen. Die
# beiden Mengen sind disjunkt; dass beide Male 29 herauskommt, ist Zufall
# und darf nicht zum Kurzschluss verleiten.
#
# ⚠️ Wer diese Zahl ERHOEHT, begruendet das im Commit. TB-53 senkt sie im
# selben Commit wie den Umbau.
AUSGANGSZAHL = 29

ERLAEUTERUNG = """\
Gezaehlt wird nur der AEUSSERSTE Ausdruck: `os.path.join(DATA_DIR,
f"{symbol}_1d.csv")` ist EIN Fund und nicht zwei, und er faellt durch, weil
seine Wurzel ueber eine zentrale Quelle geht.

⚠️ Namen, die aus `paths.py` oder `strategy_paths.py` stammen (DATA_DIR,
RESULTS_DIR, LOGS_DIR, DB_FILE, ...), gelten als zentral bezogen - ein
`os.path.join(RESULTS_DIR, "equity_curve.csv")` ist eine Ergebnisdatei und
kein eigener Datenpfad. ⚠️ Ohne diese Unterscheidung meldete das Mass im
ersten Entwurf **127** statt 29 Treffer, fast alle davon gewoehnliche
Ergebnisschreibvorgaenge."""


# ===========================================================================
# ⚠️ Die Mutationsprobe (Prueffrage B1)
# ===========================================================================
_MIT_VERSTOSS = '''
import os
from pathlib import Path
import pandas as pd

BASIS = os.path.dirname(__file__)

def a(symbol):
    return os.path.join(BASIS, "data", f"{symbol}_1d.csv")   # 1

def b(symbol):
    return f"{BASIS}/data/{symbol}_1h.csv"                   # 2

def c():
    return Path("data") / "BTCUSDT_1d.csv"                   # 3

def d(symbol):
    return "%s/data/%s.csv" % (BASIS, symbol)                # 4

def e():
    return pd.read_csv("data/AAPL_1d.csv")                   # 5
'''

_OHNE_VERSTOSS = '''
import os
import sys
sys.path.insert(0, "../../shared")
from paths import DATA_DIR

def a(symbol):
    return os.path.join(DATA_DIR, f"{symbol}_1d.csv")   # ueber den Resolver

def b():
    return os.path.join(RESULTS_DIR, "equity_curve.csv")  # Ergebnisdatei
'''


def mutationsprobe():
    import tempfile
    import shutil
    ordner = tempfile.mkdtemp(prefix="tb52_mass2_")
    try:
        mit = os.path.join(ordner, "mit_verstoss.py")
        ohne = os.path.join(ordner, "ohne_verstoss.py")
        with open(mit, "w", encoding="utf-8") as datei:
            datei.write(_MIT_VERSTOSS)
        with open(ohne, "w", encoding="utf-8") as datei:
            datei.write(_OHNE_VERSTOSS)
        funde_mit, grund_mit = masse.pfadbau(mit, "mit_verstoss.py")
        funde_ohne, grund_ohne = masse.pfadbau(ohne, "ohne_verstoss.py")
        if grund_mit or grund_ohne:
            return False, "Probemodul nicht lesbar: %s %s" % (grund_mit,
                                                              grund_ohne)
        if len(funde_mit) < 5:
            return False, ("das Mass fand nur %d von 5 eingebauten eigenen "
                           "Pfaden - es misst weniger als angenommen: %s"
                           % (len(funde_mit), [f.was for f in funde_mit]))
        if funde_ohne:
            return False, ("das Mass schlug am sauberen Modul an (%s) - ein "
                           "Pfad ueber den Resolver und eine Ergebnisdatei "
                           "duerfen NICHT zaehlen"
                           % [(f.was, f.zeile) for f in funde_ohne])
        arten = set(f.was for f in funde_mit)
        if len(arten) < 4:
            return False, ("nur %d Bauarten erkannt (%s) - das Mass sieht "
                           "nicht alle Schreibweisen" % (len(arten), arten))
        return True, ("%d von 5 eingebauten eigenen Pfaden gefunden, %d "
                      "Bauarten (%s); sauberes Modul: 0 Treffer"
                      % (len(funde_mit), len(arten), ", ".join(sorted(arten))))
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


def main():
    ok, meldung = mutationsprobe()
    print("=" * 78)
    print("Mutationsprobe zu Mass 2 (Prueffrage B1)")
    print("=" * 78)
    print("  %s %s" % ("[ok]    " if ok else "[FEHLER]", meldung))
    print()
    if not ok:
        print("ERGEBNIS: NICHT PRUEFBAR - das Mass beisst nicht, also sagt "
              "seine Zahl nichts (Prueffrage A2).")
        return 2

    funde, unlesbar, module = masse.messen(masse.pfadbau)
    rueckgabe = masse.berichte(
        "Mass 2 - kein eigener Datenpfad im Selektionspfad (TB-52)",
        funde, unlesbar, module, AUSGANGSZAHL, ERLAEUTERUNG,
        json_ziel=os.path.join("ergebnisse", "mass_pfadbau.json"))
    if funde is not None:
        betroffen = sorted(set(f.datei for f in funde))
        print("Betroffene Module: %d von %d" % (len(betroffen), len(module)))
        print()
        print("⚠️ Und der Befund, den die Zahl allein nicht sagt: KEINES der "
              "%d Selektionsmodule" % len(module))
        print("   importiert `shared/paths.py`. Der Selektionsmodus aus "
              "TB-52 erreicht sie")
        print("   heute nicht - das Verdrahten ist TB-53.")
    return rueckgabe


if __name__ == "__main__":
    sys.exit(main())

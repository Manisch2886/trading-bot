#!/usr/bin/env python3
"""
Mass 1 - keine Wanduhr im Selektionspfad (TB-52, Teil 2.2)
==============================================================================
Fable haelt das fuer die wahrscheinlichste Falle (T46.2):

    "Ein `datetime.now()` / `date.today()`, das die Historie kappt, das
    'letzte vollstaendige Jahr' bestimmt oder eine Frischepruefung macht.
    **Derselbe Snapshot ergibt dann an zwei Tagen zwei Ergebnisse** - und der
    Reproduktionstest findet es nur, wenn er an einem anderen Tag laeuft."

⚠️⚠️ Gemessen am **Syntaxbaum**, nicht per Textsuche (Prueffrage B5).

⭐ **Bauform: Sperrklinke, nicht Wache** (Prueffrage A4). Das Mass traegt eine
festgeschriebene Ausgangszahl und ist gruen, solange der gemessene Stand
**nicht groesser** ist. Wird er groesser, ist es rot. Ein Test, der dauerhaft
rot ist, waere keine Wache - er wuerde zur Tapete.

    heute            Ausgangszahl = gemessener Stand  ⇒ gruen
    TB-53 senkt      die Ausgangszahl wird im selben Commit mitgesenkt
    ein Verstoss     rot, sofort
    jemand erhoeht   ⭐ steht als eigene Zeile im Diff und braucht eine
                     Begruendung im Commit

⚠️ **Dieses Mass aendert nichts.** Es liest und zaehlt.

Nutzung:  python3 research/selektionsmasse/test_wanduhr.py
          (⚠️ **ohne Argument** - Prueffrage A3: ein Test, der ein Argument
          braucht, ist ungeprueft, nicht gruen. Er laeuft im Basislauf mit.)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import masse                                                   # noqa: E402

# ===========================================================================
# ⭐ DIE AUSGANGSZAHL
# ===========================================================================
# Gemessen am 18.09.2026 (TB-52) ueber die 90 Selektionsmodule: **6** Treffer,
# alle sechs `datetime.utcnow()` in drei `quarterly_review.py`, alle sechs in
# einer Berichts- oder Protokollzeile. ⚠️ **Null im Datenschnitt** - die
# Einordnung je Treffer steht in `BERICHT.md`, denn *der Test unterscheidet
# das nicht.*
#
# ⚠️ Wer diese Zahl ERHOEHT, begruendet das im Commit. Wer sie senkt (TB-53),
# senkt sie im selben Commit wie den Umbau.
AUSGANGSZAHL = 6

ERLAEUTERUNG = """\
Gesucht wird am Syntaxbaum nach jeder Quelle, die die Wanduhr liest:
datetime.now/utcnow/today, date.today, time.time/localtime/gmtime,
pd.Timestamp.now/today/utcnow, np.datetime64("now"), os.path.getmtime und
Verwandte - auch als blosse Referenz ohne Aufruf.

⭐ Je Treffer wird gesagt, WOZU der Wert dient. Eine Wanduhr in einer
Protokollzeile ist harmlos; eine im Datenschnitt entwertet den Lauf.
⚠️ Im Zweifel steht `zu pruefen`, nie `nur Protokollzeile` - eine
Einstufung, die im Zweifel entwarnt, macht aus einem Befund ein Schweigen."""


# ===========================================================================
# ⚠️ Die Mutationsprobe (Prueffrage B1) - beisst das Mass ueberhaupt?
# ===========================================================================
# Ein Mass, das 6 meldet, koennte auch dann 6 melden, wenn es gar nicht mehr
# misst. Deshalb laeuft es zusaetzlich gegen zwei erfundene Module: eines mit
# bekannten Verstoessen, eines ohne. Findet es dort nicht genau das
# Erwartete, ist der Ausgang NICHT PRUEFBAR (A2), nicht gruen.

_MIT_VERSTOSS = '''
import datetime as dt
from datetime import date
import time
import pandas as pd

def kappe(df):
    grenze = dt.datetime.now()              # 1 - Datenschnitt
    return df[df.index < grenze]

def letztes_jahr():
    return date.today().year - 1            # 2

def frisch(pfad):
    import os
    return time.time() - os.path.getmtime(pfad) < 3600   # 3 und 4

JETZT = pd.Timestamp.now()                  # 5
SPAETER = dt.datetime.utcnow               # 6 - blosse Referenz
HEUTE = pd.Timestamp("today")               # 7 - Zeitargument statt Name
'''

_OHNE_VERSTOSS = '''
import pandas as pd

def lade(pfad):
    return pd.read_csv(pfad)

def schnitt(df, bis):
    return df[df.index < bis]               # die Grenze kommt von aussen
'''


def mutationsprobe():
    """Gegen zwei erfundene Module messen. Gibt (ok, meldung) zurueck."""
    import tempfile
    ordner = tempfile.mkdtemp(prefix="tb52_mass1_")
    try:
        mit = os.path.join(ordner, "mit_verstoss.py")
        ohne = os.path.join(ordner, "ohne_verstoss.py")
        with open(mit, "w", encoding="utf-8") as datei:
            datei.write(_MIT_VERSTOSS)
        with open(ohne, "w", encoding="utf-8") as datei:
            datei.write(_OHNE_VERSTOSS)
        funde_mit, grund_mit = masse.wanduhren(mit, "mit_verstoss.py")
        funde_ohne, grund_ohne = masse.wanduhren(ohne, "ohne_verstoss.py")
        if grund_mit or grund_ohne:
            return False, "Probemodul nicht lesbar: %s %s" % (grund_mit,
                                                              grund_ohne)
        if len(funde_mit) < 7:
            return False, ("das Mass fand nur %d von 7 eingebauten "
                           "Wanduhren - es misst weniger als angenommen: %s"
                           % (len(funde_mit),
                              [f.was for f in funde_mit]))
        if funde_ohne:
            return False, ("das Mass schlug am sauberen Modul an (%s) - es "
                           "misst etwas anderes als angenommen"
                           % [f.was for f in funde_ohne])
        schnitt = [f for f in funde_mit
                   if f.verwendung == "Datenschnitt / Frischepruefung"]
        if not schnitt:
            return False, ("kein eingebauter Treffer wurde als Datenschnitt "
                           "eingestuft - die Einstufung misst nichts")
        return True, ("%d von 7 eingebauten Wanduhren gefunden, davon %d als "
                      "Datenschnitt eingestuft; sauberes Modul: 0 Treffer"
                      % (len(funde_mit), len(schnitt)))
    finally:
        import shutil
        shutil.rmtree(ordner, ignore_errors=True)


def main():
    ok, meldung = mutationsprobe()
    print("=" * 78)
    print("Mutationsprobe zu Mass 1 (Prueffrage B1)")
    print("=" * 78)
    print("  %s %s" % ("[ok]    " if ok else "[FEHLER]", meldung))
    print()
    if not ok:
        print("ERGEBNIS: NICHT PRUEFBAR - das Mass beisst nicht, also sagt "
              "seine Zahl nichts (Prueffrage A2).")
        return 2

    funde, unlesbar, module = masse.messen(masse.wanduhren)
    return masse.berichte(
        "Mass 1 - keine Wanduhr im Selektionspfad (TB-52)",
        funde, unlesbar, module, AUSGANGSZAHL, ERLAEUTERUNG,
        json_ziel=os.path.join("ergebnisse", "mass_wanduhr.json"))


if __name__ == "__main__":
    sys.exit(main())

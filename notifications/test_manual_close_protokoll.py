#!/usr/bin/env python3
"""
Selbsttest zu TB-105 Block E1: das Protokoll entsteht beim ersten Schreiben
==============================================================================
Bis TB-105 legte `notifications/manual_close.py` schon beim IMPORT den Ordner
`logs/notifications/` an und oeffnete `manuelle_eingriffe.log` zum Anhaengen.
Ein Modul, das nur `allokation` braucht (registerdaten.py), schrieb damit im
Selektionsmodus ins Repo (Fable 25a (A) (iii)). Jetzt geschieht beides erst
bei der ersten Protokollzeile.

P1  Import allein: kein mkdir, kein open zum Schreiben (Audit-Haken, Bauart
    docs/belege/TB-104/haken/sitecustomize.py).
P2  Eine Protokollzeile: die Datei entsteht, die Zeile hat das ALTE Format -
    zeichengleich mit der Fassung vor TB-105 (BEZUGSCOMMIT, aus git gelesen),
    bis auf den Zeitstempel.
P3  Zwei Zeilen: ein Handler, nicht zwei; zwei Zeilen in der Datei.
M1  Mutationsprobe "Anlage wieder beim Import" => P1 rot. Gegenprobe: die
    unveraenderte Kopie ist in P1 gruen.
B1  Befund: die Fassung vor TB-105 ist in P1 rot (sie legte beim Import an).

Jede Probe laeuft in einem eigenen Prozess in einem Wegwerfbaum
(<tmp>/notifications/manual_close.py) - das echte logs/ wird nie beruehrt.

Aufruf:  python3 notifications/test_manual_close_protokoll.py
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_HIER)
QUELLE = os.path.join(_HIER, "manual_close.py")

# Letzter Commit vor TB-105 (Schritt 0), in dem das Protokoll noch beim
# Import angelegt wurde. Festgenagelt, nicht origin/main.
BEZUGSCOMMIT = "b83e6b9"

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")


# Kindprozess: Audit-Haken auf open (schreibend) und os.mkdir unterhalb der
# Wurzel, dann Import und 0/1/2 Protokollzeilen. Ausgabe als JSON.
PROBE = r'''
import json, os, sys
wurzel, zeilen = sys.argv[1], int(sys.argv[2])
ereignisse = []
def haken(ereignis, args):
    if ereignis == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
        pfad = os.fsdecode(args[0]); modus = str(args[1]) if len(args) > 1 else "r"
        if pfad.startswith(wurzel) and any(z in modus for z in "wax+"):
            ereignisse.append(["open", modus, pfad])
    elif ereignis == "os.mkdir" and args:
        pfad = os.fsdecode(args[0])
        if pfad.startswith(wurzel):
            ereignisse.append(["mkdir", "-", pfad])
sys.addaudithook(haken)
sys.path.insert(0, os.path.join(wurzel, "notifications"))
import manual_close as mc
nach_import = list(ereignisse)
for i in range(zeilen):
    mc.protokolliere_ablehnung("testbot", 7 + i, "probe", "grund%d" % i, quelle="test")
griffe = len(mc._protokoll.handlers)
for g in list(mc._protokoll.handlers):
    g.flush()
json.dump({"nach_import": nach_import, "alle": ereignisse, "griffe": griffe}, sys.stdout)
'''


def baum(arbeit, name, quelltext):
    wurzel = os.path.join(os.path.realpath(arbeit), name)
    os.makedirs(os.path.join(wurzel, "notifications"))
    with open(os.path.join(wurzel, "notifications", "manual_close.py"), "w",
              encoding="utf-8") as f:
        f.write(quelltext)
    return wurzel


def lauf(wurzel, zeilen, probedatei):
    # Der Logger "manuelle_eingriffe" ist prozessweit - daher je Probe ein
    # eigener Prozess, sonst saehe P1 den Handler einer frueheren Probe.
    r = subprocess.run([sys.executable, probedatei, wurzel, str(zeilen)],
                       capture_output=True, text=True, cwd=wurzel)
    if r.returncode != 0:
        return {"fehler": r.stderr.strip()[-400:]}
    return json.loads(r.stdout)


def logdatei(wurzel):
    return os.path.join(wurzel, "logs", "notifications", "manuelle_eingriffe.log")


def ohne_zeit(zeile):
    return re.sub(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} ", "<ZEIT> ", zeile)


def main():
    print(__doc__.strip().split("\n")[0])
    neu = open(QUELLE, encoding="utf-8").read()
    alt = subprocess.run(["git", "-C", BASE_DIR, "show",
                          BEZUGSCOMMIT + ":notifications/manual_close.py"],
                         capture_output=True, text=True)
    arbeit = tempfile.mkdtemp(prefix="tb105_manual_close_")
    try:
        probedatei = os.path.join(arbeit, "probe.py")
        with open(probedatei, "w", encoding="utf-8") as f:
            f.write(PROBE)

        # P1 - Import allein
        w = baum(arbeit, "p1", neu)
        r = lauf(w, 0, probedatei)
        pruefe("P1 Import allein: kein mkdir, kein open zum Schreiben",
               r.get("nach_import") == [], str(r)[:300])
        pruefe("P1b Import allein: logs/ existiert danach nicht",
               not os.path.exists(os.path.join(w, "logs")))

        # P2 - eine Zeile, Format wie vorher
        w = baum(arbeit, "p2", neu)
        r = lauf(w, 1, probedatei)
        pruefe("P2 eine Zeile: Datei entsteht", os.path.isfile(logdatei(w)), str(r)[:300])
        neu_zeilen = open(logdatei(w), encoding="utf-8").read().splitlines() \
            if os.path.isfile(logdatei(w)) else []
        pruefe("P2b genau eine Zeile", len(neu_zeilen) == 1, str(neu_zeilen)[:200])
        if alt.returncode != 0 or not alt.stdout.strip():
            pruefe("P2c NICHT PRUEFBAR: Bezugscommit %s nicht lesbar" % BEZUGSCOMMIT, False,
                   alt.stderr.strip()[:200])
        else:
            wa = baum(arbeit, "p2_alt", alt.stdout)
            lauf(wa, 1, probedatei)
            alt_zeilen = open(logdatei(wa), encoding="utf-8").read().splitlines() \
                if os.path.isfile(logdatei(wa)) else []
            pruefe("P2c Zeile zeichengleich mit der Fassung %s (ohne Zeitstempel)" % BEZUGSCOMMIT,
                   bool(alt_zeilen) and [ohne_zeit(z) for z in neu_zeilen]
                   == [ohne_zeit(z) for z in alt_zeilen],
                   "neu %r / alt %r" % (neu_zeilen[:1], alt_zeilen[:1]))
            pruefe("P2d Zeitstempelform unveraendert",
                   all(ohne_zeit(z) != z for z in neu_zeilen + alt_zeilen))
            # B1 - der Befund: die alte Fassung legte beim Import an.
            wb = baum(arbeit, "b1_alt", alt.stdout)
            rb = lauf(wb, 0, probedatei)
            pruefe("B1 Befund: die Fassung %s legt beim Import an (P1 dort rot)" % BEZUGSCOMMIT,
                   bool(rb.get("nach_import")), str(rb)[:300])

        # P3 - zwei Zeilen, ein Handler
        w = baum(arbeit, "p3", neu)
        r = lauf(w, 2, probedatei)
        pruefe("P3 zwei Zeilen: genau ein Handler", r.get("griffe") == 1, str(r)[:300])
        zeilen = open(logdatei(w), encoding="utf-8").read().splitlines() \
            if os.path.isfile(logdatei(w)) else []
        pruefe("P3b zwei Zeilen in der Datei", len(zeilen) == 2, str(zeilen)[:200])

        # M1 - Mutation: Anlage wieder beim Import
        mutiert = neu + "\n_protokoll_bereit()\n"
        pruefe("M1 Mutation angebracht", "def _protokoll_bereit" in neu)
        w = baum(arbeit, "m1", mutiert)
        r = lauf(w, 0, probedatei)
        pruefe("M1 Mutation 'Anlage beim Import' => P1 rot",
               bool(r.get("nach_import")), str(r)[:300])
        w = baum(arbeit, "m1_gegen", neu)
        r = lauf(w, 0, probedatei)
        pruefe("M1 Gegenprobe: unveraenderte Kopie in P1 gruen",
               r.get("nach_import") == [], str(r)[:300])
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)

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

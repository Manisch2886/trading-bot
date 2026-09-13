"""
Gesamtlauf TB-25
====================================================================
Startet fuer JEDEN der beiden Elliott-Wave-Bots einen EIGENEN Prozess.
Der Grund steht im Kopf von botenv.py: beide Bots haben gleichnamige,
inhaltlich verschiedene Module - ein Import beider im selben Prozess
wuerde ueber sys.modules still den falschen Bot laden.

Reihenfolge je Bot:  lauf.py -> auswertung.py -> test_stufen.py
Danach einmal:       uebersicht.py (fasst beide Bots zusammen)

Aufruf:  python3 run_all.py
"""

import os
import subprocess
import sys
import time

import botenv

DIR = os.path.dirname(os.path.abspath(__file__))
SCHRITTE = ("lauf.py", "auswertung.py", "test_stufen.py")


def starte(skript, *args):
    befehl = [sys.executable, os.path.join(DIR, skript), *args]
    print(f"\n$ python3 {skript} {' '.join(args)}")
    t0 = time.time()
    ergebnis = subprocess.run(befehl, cwd=DIR)
    print(f"  ({time.time() - t0:.1f}s)")
    if ergebnis.returncode != 0:
        raise SystemExit(f"ABBRUCH: {skript} {' '.join(args)} "
                         f"endete mit {ergebnis.returncode}")


def main():
    botenv.print_hinweis()
    t0 = time.time()
    for bot in botenv.BOTS:
        print(f"\n{'=' * 70}\n{bot}\n{'=' * 70}")
        for skript in SCHRITTE:
            starte(skript, bot)
    print(f"\n{'=' * 70}\nZusammenfassung\n{'=' * 70}")
    starte("uebersicht.py")
    print(f"\nGesamtdauer: {time.time() - t0:.1f}s")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()

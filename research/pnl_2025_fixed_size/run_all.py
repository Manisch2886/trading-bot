"""
Alles nacheinander - 2025er-P&L aller neun Bots
====================================================================
Startet je Zeile der Tabelle einen eigenen Prozess (mehrere Bots haben
gleichnamige, inhaltlich verschiedene Module - siehe botenv.py) und
bricht beim ersten Fehlschlag ab. Zum Schluss die Selbsttests und die
Tabelle.

Laufzeit: rund 10 Minuten, der Krypto-Elliott-Bot dominiert
(18 Symbole mit je ~44.000 Stundenkerzen).

Nutzung:  python3 run_all.py
"""

import os
import subprocess
import sys
import time

import konfiguration as cfg

DIR = os.path.dirname(os.path.abspath(__file__))


def run(script, *args):
    beschriftung = " ".join([script, *args])
    print(f"\n{'=' * 70}\n{beschriftung}\n{'=' * 70}", flush=True)
    t0 = time.time()
    res = subprocess.run([sys.executable, os.path.join(DIR, script), *args],
                          cwd=DIR, text=True)
    if res.returncode != 0:
        print(f"\nABBRUCH: {beschriftung} endete mit Code {res.returncode}")
        sys.exit(res.returncode)
    print(f"-- {beschriftung}: {round(time.time() - t0, 1)} s", flush=True)


if __name__ == "__main__":
    t0 = time.time()
    for schluessel in cfg.REIHENFOLGE:
        run("extract.py", schluessel)
    run("test_pnl.py")
    run("summary.py")
    print(f"\nAlle Schritte erfolgreich ({round(time.time() - t0, 1)} s).")

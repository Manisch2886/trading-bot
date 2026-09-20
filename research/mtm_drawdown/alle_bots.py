#!/usr/bin/env python3
"""
TB-73 - Alle neun Bots messen, je einer im eigenen Prozess, dann auswerten
==============================================================================
    trading-env/bin/python3 research/mtm_drawdown/alle_bots.py

Ruft `messung.py <bot>` fuer jeden Bot als Kindprozess mit demselben
Interpreter auf (gleichnamige Bot-Module vertragen keinen gemeinsamen
Prozess, siehe botenv.py), sammelt Rueckgabewert und Laufzeit und ruft
danach `auswertung.py`, das die Tabellen schreibt. Bricht ein Bot ab, steht
er mit seinem Fehler in der Zusammenfassung und fehlt in den Tabellen -
keine Zahl wird erfunden.
"""

import json
import os
import subprocess
import sys
import time

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)
from grundlage import BOTS, ERGEBNISSE  # noqa: E402


def main():
    os.makedirs(ERGEBNISSE, exist_ok=True)
    protokoll = []
    t_alle = time.time()
    for bot in BOTS:
        t0 = time.time()
        lauf = subprocess.run([sys.executable, os.path.join(_HIER, "messung.py"), bot],
                              capture_output=True, text=True)
        dauer = round(time.time() - t0, 1)
        sys.stdout.write(lauf.stdout)
        if lauf.returncode != 0:
            sys.stdout.write(lauf.stderr[-3000:])
        protokoll.append({"bot": bot, "rc": lauf.returncode, "laufzeit_s": dauer,
                          "fehler": (lauf.stderr.strip().splitlines()[-1] if lauf.returncode else None)})
        print(f"--- {bot}: rc {lauf.returncode}, {dauer} s\n")
    protokoll_datei = os.path.join(ERGEBNISSE, "laufprotokoll.json")
    with open(protokoll_datei, "w", encoding="utf-8") as f:
        json.dump({"gesamt_s": round(time.time() - t_alle, 1), "interpreter": sys.version.split()[0],
                   "bots": protokoll}, f, indent=1)
    print(f"Messung gesamt {round(time.time() - t_alle, 1)} s -> {os.path.relpath(protokoll_datei)}")
    aus = subprocess.run([sys.executable, os.path.join(_HIER, "auswertung.py")], text=True)
    return 1 if any(p["rc"] for p in protokoll) or aus.returncode else 0


if __name__ == "__main__":
    sys.exit(main())

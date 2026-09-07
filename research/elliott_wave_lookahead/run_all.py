"""
Fuehrt die komplette Untersuchung aus - je Bot in einem eigenen Prozess.
====================================================================
Beide Elliott-Wave-Bots haben gleichnamige, inhaltlich verschiedene
Module (`equity_simulation.py`, `zigzag_indicator.py`, ...). Ein Import
beider im selben Python-Prozess wuerde ueber `sys.modules` still den
falschen Bot laden - deshalb strikt getrennte Subprozesse.

Nutzung:  python3 run_all.py
"""

import os
import subprocess
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
BOTS = ("elliott_wave", "elliott_wave_stocks")

# Reihenfolge ist Absicht: der Regressionscheck laeuft ZUERST. Schlaegt er
# fehl, ist jede weitere Zahl wertlos.
# Reihenfolge ist Absicht: erst die Regressionschecks gegen den eingefrorenen
# Bot-Stand, dann der Kausalitaets-Nachweis fuer den KORRIGIERTEN Bot-Code,
# dann die Auswertungen.
#
# Hinweis zur Abgrenzung: run_one_bot.py, grid.py und decisions.py sind die
# Analyse aus PR #26. Ihre Variante "korrigiert" behebt nur Kanal 1 (den
# Einstiegszeitpunkt) - die Wellenauswahl laeuft dort weiterhin rueckblickend.
# Der Bot-Code selbst behebt inzwischen BEIDE Kanaele; compare_channels.py
# stellt beide Staende gegenueber.
STEPS = [
    ("verify_baseline.py", BOTS),
    ("verify_causality.py", BOTS),
    ("run_one_bot.py", BOTS),
    ("grid.py", BOTS),
    ("decisions.py", ("elliott_wave_stocks",)),
    ("compare_channels.py", BOTS),
]


def main():
    print("=" * 78)
    print("0) Sanity-Checks (ohne Bot-Daten)")
    print("=" * 78)
    rc = subprocess.run([sys.executable, os.path.join(_DIR, "test_lookahead.py")], cwd=_DIR)
    if rc.returncode != 0:
        raise SystemExit("test_lookahead.py fehlgeschlagen - Abbruch.")

    for script, bots in STEPS:
        for bot in bots:
            print("\n" + "=" * 78)
            print(f"{script}  {bot}")
            print("=" * 78)
            rc = subprocess.run([sys.executable, os.path.join(_DIR, script), bot], cwd=_DIR)
            if rc.returncode != 0:
                raise SystemExit(f"{script} {bot} fehlgeschlagen - Abbruch.")

    print("\nAlle Schritte durchgelaufen. Ergebnisse in results/.")


if __name__ == "__main__":
    main()

"""
Fuehrt die komplette Trailing-Stop-Untersuchung aus
========================================================
Reihenfolge entspricht der Aufgabenstellung:
  1. Bestandsaufnahme aller 9 Bots (stop_inventory.py) - ZWINGEND zuerst
  2. je betroffenem Bot ein Baseline-Regressionscheck (verify_baseline.py)
  3. je betroffenem Bot die Variantenrechnung mit ATR-14 (Hauptwahl) und
     ATR-22 (einzelne Robustheits-Illustration, KEINE Optimierung)

Jeder Bot laeuft in einem EIGENEN Prozess (subprocess), weil die 9 Bots
gleichnamige, aber inhaltlich verschiedene Module haben - im selben
Prozess wuerde sys.modules-Caching fuer den zweiten Bot die falsche
Version liefern.

Nutzung:
    python3 run_all.py              # Bestandsaufnahme + Checks + alle Laeufe
    python3 run_all.py --verify     # nur die Baseline-Regressionschecks
    python3 run_all.py --skip-verify
"""

import json
import os
import subprocess
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(_DIR, "results")

# Hauptwahl 14 (Wilders Original-Standard, siehe BERICHT.md), plus GENAU EIN
# zweiter Wert als Robustheits-Illustration. 22 ist bewusst nicht frei
# gewaehlt, sondern der ATR-Wert, den das Projekt bereits selbst verwendet
# (SuperTrend in strategies/t3_supertrend/backtest_trend.py: ATR_LENGTH = 22).
ATR_WINDOWS = [14, 22]


def run(cmd: list) -> int:
    print(f"\n$ {' '.join(cmd)}")
    return subprocess.call([sys.executable] + cmd, cwd=_DIR)


def in_scope_bots() -> list:
    """Liest die Bot-Liste NICHT aus einer zweiten, handgepflegten Kopie,
    sondern direkt aus der Bestandsaufnahme - so kann die Untersuchung nicht
    versehentlich von der Klassifikation abweichen."""
    with open(os.path.join(RESULTS_DIR, "stop_inventory.json")) as f:
        return json.load(f)["in_scope"]


def main():
    only_verify = "--verify" in sys.argv
    skip_verify = "--skip-verify" in sys.argv

    print("=" * 72)
    print("SCHRITT 1 - Bestandsaufnahme der Stop-Mechanismen aller 9 Bots")
    print("=" * 72)
    if run(["stop_inventory.py", "--json"]) != 0:
        sys.exit("Bestandsaufnahme fehlgeschlagen - Abbruch.")

    bots = in_scope_bots()
    failures = []

    if not skip_verify:
        print("\n" + "=" * 72)
        print("SCHRITT 2 - Baseline-Regressionscheck je betroffenem Bot")
        print("=" * 72)
        for bot in bots:
            if run(["verify_baseline.py", bot]) != 0:
                failures.append(f"verify_baseline {bot}")

    if only_verify:
        print(f"\nFehlgeschlagen: {failures if failures else 'keine'}")
        sys.exit(1 if failures else 0)

    print("\n" + "=" * 72)
    print("SCHRITT 3 - Variantenrechnung (Baseline / Fix-Trailing / ATR-Trailing)")
    print("=" * 72)
    for bot in bots:
        for window in ATR_WINDOWS:
            if run(["run_one_bot.py", bot, str(window)]) != 0:
                failures.append(f"run_one_bot {bot} ATR-{window}")

    print("\n" + "=" * 72)
    if failures:
        print("FEHLGESCHLAGEN:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("Alle Laeufe erfolgreich. Weiter mit: python3 aggregate_report.py")


if __name__ == "__main__":
    main()

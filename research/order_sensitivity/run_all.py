"""
Fuehrt die Reihenfolge-Untersuchung fuer alle 9 Bots aus.

Jeder Bot laeuft in einem EIGENEN Prozess, weil alle 9 gleichnamige, aber
inhaltlich verschiedene Module haben (equity_simulation.py,
multi_symbol_optimise.py, indicators.py, ...).

Nutzung:
    python3 run_all.py            # alle 9 Bots
    python3 run_all.py <bot> ...  # nur die genannten
"""

import os
import subprocess
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))

BOTS = [
    "elliott_wave", "elliott_wave_stocks", "t3_supertrend",
    "rsi2_crypto", "rsi2_mean_reversion",
    "turtle_soup_crypto", "turtle_soup_stocks",
    "volatility_breakout", "volatility_breakout_crypto",
]


def main():
    selected = [a for a in sys.argv[1:] if not a.startswith("-")] or BOTS
    failures = []
    for bot in selected:
        print(f"\n{'=' * 78}\n{bot}\n{'=' * 78}")
        if subprocess.call([sys.executable, "run_one_bot.py", bot], cwd=_DIR) != 0:
            failures.append(bot)

    print(f"\n{'=' * 78}")
    if failures:
        print("FEHLGESCHLAGEN: " + ", ".join(failures))
        sys.exit(1)
    print("Alle Bots erfolgreich. Weiter mit: python3 decisions.py, dann aggregate_report.py")


if __name__ == "__main__":
    main()

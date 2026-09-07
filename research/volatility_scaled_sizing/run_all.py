"""
Fuehrt run_one_bot.py fuer ALLE 9 Bots aus - jeder Bot in einem EIGENEN,
isolierten Subprozess (siehe run_one_bot.py-Docstring: gleichnamige, aber
inhaltlich unterschiedliche Module pro Bot verbieten das gemeinsame
Importieren mehrerer Bots im selben Python-Prozess).

Ersetzt den bisherigen manuellen ad-hoc Bash-Loop durch ein einziges,
wiederholbares Kommando. Reine Orchestrierung - enthaelt selbst KEINE
Backtest-Logik.

Nutzung:
    python3 run_all.py
Exit-Code ist 0 nur, wenn ALLE 9 Bots erfolgreich durchgelaufen sind.
"""
import os
import sys
import subprocess

BOTS = [
    "elliott_wave",
    "elliott_wave_stocks",
    "t3_supertrend",
    "rsi2_crypto",
    "rsi2_mean_reversion",
    "turtle_soup_crypto",
    "turtle_soup_stocks",
    "volatility_breakout",
    "volatility_breakout_crypto",
]

_RESEARCH_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    failed = []
    for bot in BOTS:
        print(f"=========== {bot} ===========")
        result = subprocess.run(
            [sys.executable, os.path.join(_RESEARCH_DIR, "run_one_bot.py"), bot],
            cwd=_RESEARCH_DIR,
        )
        if result.returncode != 0:
            failed.append(bot)
        print()

    if failed:
        print(f"{len(failed)} von {len(BOTS)} Bots FEHLGESCHLAGEN: {failed}")
        sys.exit(1)
    print(f"Alle {len(BOTS)} Bots erfolgreich abgeschlossen.")


if __name__ == "__main__":
    main()

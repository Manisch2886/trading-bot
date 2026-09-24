"""
Alle neun Bots nacheinander, je in einem eigenen Prozess.

Ein eigener Prozess je Bot ist nicht Vorsicht, sondern Notwendigkeit: alle
neun Bots haben gleichnamige, inhaltlich verschiedene Module
(`equity_simulation.py`, `live_params.py`, `multi_symbol_optimise.py`) - im
selben Prozess liefert das sys.modules-Caching ab dem zweiten Bot die falsche
Fassung. Vorbild: `shared/portfolio_overview.py` und
`research/exposure_messung/alle_bots.py`.

Nutzung:
    python3 alle_bots.py --ziel <ordner> [bot ...]

`--ziel` ist Pflicht und wird an jeden `positionen_holen.py`-Aufruf
durchgereicht (TB-98 B4, Register 36.1): keine Voreinstellung, und ein Bot,
dessen Zieldateien schon bestehen, endet dort mit 1, ohne zu rechnen. Der
Pfad wird hier absolut gemacht, weil die Kindprozesse in diesem Ordner laufen.
"""

import argparse
import os
import subprocess
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))

BOTS = [
    "elliott_wave",
    "t3_supertrend",
    "rsi2_crypto",
    "turtle_soup_crypto",
    "volatility_breakout_crypto",
    "elliott_wave_stocks",
    "rsi2_mean_reversion",
    "turtle_soup_stocks",
    "volatility_breakout",
]


def main():
    aufruf = argparse.ArgumentParser(description="positionen_holen.py fuer mehrere Bots.")
    aufruf.add_argument("--ziel", required=True, metavar="ORDNER")
    aufruf.add_argument("bots", nargs="*")
    args = aufruf.parse_args()
    ziel = os.path.abspath(args.ziel)
    bots = args.bots or BOTS
    fehler = []
    for bot in bots:
        print(f"\n=== {bot}", flush=True)
        ergebnis = subprocess.run(
            [sys.executable, os.path.join(_DIR, "positionen_holen.py"), bot,
             "--ziel", ziel], cwd=_DIR)
        if ergebnis.returncode != 0:
            fehler.append(bot)

    if fehler:
        print(f"\nFEHLGESCHLAGEN: {', '.join(fehler)}")
        sys.exit(1)
    print(f"\nAlle {len(bots)} Bots durchgelaufen.")


if __name__ == "__main__":
    main()

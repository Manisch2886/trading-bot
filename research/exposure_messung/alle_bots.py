"""
Alle neun Bots nacheinander, je in einem eigenen Prozess.

Nutzung:
    python3 alle_bots.py [bot ...]
"""

import os
import subprocess
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))

BOTS = [
    "elliott_wave",
    "t3_supertrend",
    "elliott_wave_stocks",
    "rsi2_mean_reversion",
    "rsi2_crypto",
    "turtle_soup_crypto",
    "turtle_soup_stocks",
    "volatility_breakout",
    "volatility_breakout_crypto",
]

# Die vier Bots, aus denen die urspruengliche -1,43-%-Zahl stammt
# (results/rsi2_mean_reversion/PROTOTYPE_FINDINGS.md, Abschnitt 5).
VIERER = ["elliott_wave", "t3_supertrend", "elliott_wave_stocks", "rsi2_mean_reversion"]


def main():
    bots = sys.argv[1:] or BOTS
    fehler = []
    for bot in bots:
        print(f"\n=== {bot}", flush=True)
        ergebnis = subprocess.run([sys.executable, os.path.join(_DIR, "bot_lauf.py"), bot],
                                   cwd=_DIR)
        if ergebnis.returncode != 0:
            fehler.append(bot)

    if fehler:
        print(f"\nFEHLGESCHLAGEN: {', '.join(fehler)}")
        sys.exit(1)
    print(f"\nAlle {len(bots)} Bots durchgelaufen.")


if __name__ == "__main__":
    main()

"""
Aktien-Symbol-Konfiguration
================================
Liest dieselbe Top-150-Liste wie elliott_wave_stocks/rsi2_mean_reversion aus
config/sp500_top150.txt - identisches Universum, fuer einen fairen
Diversifikations-Vergleich zwischen allen Aktien-Bots. Faellt auf eine
kleine Standardliste zurueck, falls die Datei noch nicht existiert.
"""

import os
import sys

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
CONFIG_DIR = _P["CONFIG_DIR"]

SYMBOLS_FILE = os.path.join(CONFIG_DIR, "sp500_top150.txt")
DEFAULT_SYMBOLS = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"]


def load_symbols() -> list:
    if os.path.exists(SYMBOLS_FILE):
        with open(SYMBOLS_FILE) as f:
            symbols = [line.strip() for line in f if line.strip()]
        if symbols:
            return symbols
    print(f"Warnung: {SYMBOLS_FILE} nicht gefunden. Nutze Standardliste (5 Aktien).")
    return DEFAULT_SYMBOLS


SYMBOLS = load_symbols()

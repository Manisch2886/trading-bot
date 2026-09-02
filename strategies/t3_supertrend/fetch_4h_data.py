"""
4-Stunden Datenabruf - T3/ADX/SuperTrend-Strategie
========================================================
Nachdem sich sowohl 1h als auch 15m als ungeeignet erwiesen haben
(1h: zu viel Whipsaw, 15m: unpraktikabel fuer ein Cronjob-basiertes
Setup und zu gebuehrenempfindlich bei kurzen Haltezeiten), testen
wir jetzt 4h - der klassische Zeitrahmen fuer T3/ADX/SuperTrend als
Trendfolge-Indikatoren.

Die 4h-Daten landen im selben gemeinsamen data/-Ordner wie die
1h-Daten des Elliott-Wave-Bots, aber unter eigenem Dateinamen
(BTCUSDT_4h.csv statt BTCUSDT_1h.csv) - kein Konflikt zwischen den
Strategien.
"""

import os
import sys
import time
from binance.client import Client

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from fetch_binance_data import fetch_historical_data
from symbols_config import SYMBOLS
from paths import DATA_DIR

INTERVAL = Client.KLINE_INTERVAL_4HOUR
LOOKBACK = "1825 day ago UTC"  # 5 Jahre, wie beim Elliott-Wave-Bot
PAUSE_BETWEEN_REQUESTS_SEC = 0.5

if __name__ == "__main__":
    print(f"Lade 4-Stunden-Daten fuer {len(SYMBOLS)} Symbole...\n")

    for i, symbol in enumerate(SYMBOLS, 1):
        print(f"[{i}/{len(SYMBOLS)}] Lade {symbol} ...")
        try:
            df = fetch_historical_data(symbol, INTERVAL, LOOKBACK)
            output_file = os.path.join(DATA_DIR, f"{symbol}_{INTERVAL}.csv")
            df.to_csv(output_file, index=False)
            print(f"    {len(df)} Kerzen gespeichert als {output_file}")
        except Exception as e:
            print(f"    Fehler bei {symbol}: {e}")

        time.sleep(PAUSE_BETWEEN_REQUESTS_SEC)

    print("\nFertig.")

"""
Phase 3c - Multi-Symbol Datenabruf
=====================================
Laedt historische Daten fuer viele Coins statt nur einer Handvoll.
Ziel: mehr unabhaengige Marktereignisse -> mehr Elliott-Wave-Signale
insgesamt -> statistisch belastbarere Backtests und Optimierung.

Nutzt die zentrale Symbol-Liste aus symbols_config.py (Top 100 nach
Volumen, falls zuvor 'python3 get_top_symbols.py' ausgefuehrt wurde).

WICHTIG: Bei sehr vielen Symbolen dauert dieser Abruf entsprechend
laenger. Kleine Pausen zwischen Anfragen schuetzen vor Binance's
Rate-Limits.
"""

import os
import time
from binance.client import Client
from fetch_binance_data import fetch_historical_data
from symbols_config import SYMBOLS
from paths import DATA_DIR

client = Client()

INTERVAL = Client.KLINE_INTERVAL_1HOUR
LOOKBACK = "1825 day ago UTC"  # 5 Jahre, wie zuvor
PAUSE_BETWEEN_REQUESTS_SEC = 0.5  # schont Binance's Rate-Limit bei vielen Symbolen


if __name__ == "__main__":
    print(f"Lade Daten fuer {len(SYMBOLS)} Symbole...\n")

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

    print("\nFertig. Alle verfuegbaren Symbole geladen.")

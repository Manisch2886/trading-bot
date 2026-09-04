"""
Tages-Datenabruf - Volatility Breakout Krypto
========================================================
Analog zu rsi2_crypto/fetch_1d_data.py bzw. t3_supertrend/fetch_4h_data.py
(Tageskerzen-Begruendung siehe backtest_breakout.py-Docstring). Nutzt
dasselbe Symbol-Universum UND denselben Zeitrahmen (Tageskerzen) wie
RSI-2 Krypto - eigenstaendige Kopie statt Cross-Strategy-Import
(Architektur-Prinzip), auch wenn beide Skripte de facto dieselben
BTCUSDT_1d.csv usw. befuellen (kein Konflikt: beide schreiben identische
Daten in denselben gemeinsamen data/-Ordner).

WICHTIG: In der Prototyp-Phase wurden die Tageskerzen mangels Sandbox-
Netzwerkzugriff aus vorhandenen 1h-Daten abgeleitet
(shared/build_daily_crypto_data.py). Dieses Skript ist der native Ersatz
dafuer auf der echten Maschine des Nutzers (mit Binance-API-Zugriff).
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

INTERVAL = Client.KLINE_INTERVAL_1DAY
LOOKBACK = "3650 day ago UTC"  # 10 Jahre Vorlauf angefragt - Binance liefert ohnehin
                                # nur soviel Historie zurueck, wie fuer das jeweilige
                                # Symbol tatsaechlich existiert (kein Fehler bei juengeren Coins)
PAUSE_BETWEEN_REQUESTS_SEC = 0.5

if __name__ == "__main__":
    print(f"Lade Tagesdaten fuer {len(SYMBOLS)} Symbole...\n")

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

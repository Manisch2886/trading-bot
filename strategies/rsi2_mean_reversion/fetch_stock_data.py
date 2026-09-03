"""
Aktienkurs-Datenabruf (taeglich) via yfinance
==================================================
Laedt die maximal verfuegbare Historie an Tages-Kerzen fuer jede
Aktie in der Symbol-Liste. Landet im selben gemeinsamen data/-Ordner
wie die Krypto-Daten, aber unter eigenem Dateinamen (z.B. AAPL_1d.csv)
- kein Konflikt mit den Krypto-Strategien.

HINWEIS: yfinance ist eine inoffizielle Bibliothek, die Yahoo Finance
im Hintergrund abfragt. Sie ist kostenlos und weit verbreitet, aber
nicht so verlaesslich wie eine offizielle Broker-API - bei
Verbindungsfehlern bei einzelnen Aktien ist das normal, das Skript
faehrt einfach mit der naechsten fort.
"""

import os
import sys
import time

import pandas as pd
import yfinance as yf

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
DATA_DIR = _P["DATA_DIR"]

from stocks_symbols_config import SYMBOLS

INTERVAL = "1d"
PERIOD = "max"  # laengstmoegliche verfuegbare Historie je Aktie
PAUSE_BETWEEN_REQUESTS_SEC = 0.3


def fetch_historical_data(ticker: str, period: str = PERIOD, interval: str = INTERVAL) -> pd.DataFrame:
    """Laedt historische Kursdaten fuer eine einzelne Aktie und bringt sie
    ins selbe Format wie die Krypto-Daten (open_time/open/high/low/close/volume)."""
    df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)

    if df.empty:
        return pd.DataFrame(columns=["open_time", "open", "high", "low", "close", "volume"])

    # yfinance liefert bei manchen Versionen MultiIndex-Spalten - absichern
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()
    date_col = "Date" if "Date" in df.columns else "Datetime"

    df = df.rename(columns={
        date_col: "open_time",
        "Open": "open", "High": "high", "Low": "low",
        "Close": "close", "Volume": "volume",
    })

    return df[["open_time", "open", "high", "low", "close", "volume"]]


if __name__ == "__main__":
    print(f"Lade taegliche Kursdaten fuer {len(SYMBOLS)} Aktien...\n")

    for i, ticker in enumerate(SYMBOLS, 1):
        print(f"[{i}/{len(SYMBOLS)}] Lade {ticker} ...")
        try:
            df = fetch_historical_data(ticker)
            if df.empty:
                print(f"    Keine Daten erhalten fuer {ticker}, uebersprungen.")
                continue
            output_file = os.path.join(DATA_DIR, f"{ticker}_{INTERVAL}.csv")
            df.to_csv(output_file, index=False)
            print(f"    {len(df)} Kerzen gespeichert als {output_file}")
        except Exception as e:
            print(f"    Fehler bei {ticker}: {e}")

        time.sleep(PAUSE_BETWEEN_REQUESTS_SEC)

    print("\nFertig.")

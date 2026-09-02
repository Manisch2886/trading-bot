"""
Top-Aktien aus dem S&P 500 ermitteln
=========================================
Laedt die aktuelle Liste der S&P-500-Mitglieder von Wikipedia und
rankt sie nach Marktkapitalisierung (via yfinance). Die Top 25 werden
in config/sp500_top25.txt gespeichert.

Getrennt von der Krypto-Symbol-Liste (top25_symbols.txt), damit sich
beide Welten nicht vermischen.
"""

import os
import sys
import time
from io import StringIO

import pandas as pd
import requests
import yfinance as yf

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
CONFIG_DIR = _P["CONFIG_DIR"]

TOP_N = 150
OUTPUT_FILE = os.path.join(CONFIG_DIR, "sp500_top150.txt")
WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def get_sp500_tickers() -> list:
    """Liest die aktuelle S&P-500-Mitgliederliste von Wikipedia.
    Wikipedia blockiert Anfragen ohne echten Browser-User-Agent (403
    Forbidden) - daher wird die Seite hier mit einem gesetzten
    User-Agent abgerufen, statt sie direkt an pd.read_html zu uebergeben."""
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    response = requests.get(WIKIPEDIA_URL, headers=headers, timeout=15)
    response.raise_for_status()

    tables = pd.read_html(StringIO(response.text))
    sp500_table = tables[0]  # erste Tabelle auf der Seite enthaelt die Mitgliederliste
    tickers = sp500_table["Symbol"].tolist()
    # yfinance nutzt Punkt statt Bindestrich bei Aktienklassen (z.B. BRK.B statt BRK-B)
    return [t.replace(".", "-") for t in tickers]


if __name__ == "__main__":
    print("Lade S&P-500-Mitgliederliste von Wikipedia...")
    tickers = get_sp500_tickers()
    print(f"{len(tickers)} Ticker gefunden.\n")

    print("Ermittle Marktkapitalisierung (das dauert einen Moment)...")
    market_caps = {}
    for i, ticker in enumerate(tickers, 1):
        try:
            info = yf.Ticker(ticker).fast_info
            market_caps[ticker] = info.market_cap or 0
        except Exception as e:
            print(f"  Warnung bei {ticker}: {e}")
            market_caps[ticker] = 0

        if i % 50 == 0:
            print(f"  {i}/{len(tickers)} verarbeitet...")
        time.sleep(0.05)  # schont die Yahoo-Finance-Abfrage-Rate

    ranked = sorted(market_caps.items(), key=lambda x: x[1], reverse=True)
    top_tickers = [t for t, _ in ranked[:TOP_N]]

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(top_tickers))

    print(f"\nTop {TOP_N} Aktien nach Marktkapitalisierung gespeichert in {OUTPUT_FILE}\n")
    print("Top 10 zur Kontrolle:")
    for i, (ticker, cap) in enumerate(ranked[:10], 1):
        print(f"  {i}. {ticker}  (Marktkap.: {cap:,.0f} USD)")

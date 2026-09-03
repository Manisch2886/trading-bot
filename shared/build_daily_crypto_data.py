"""
Tageskerzen aus vorhandenen Stundendaten ableiten (Sandbox-Workaround)
================================================================================
Fuer die neuen Krypto-Prototypen (RSI-2 Krypto, Volatility Breakout Krypto,
siehe strategies/rsi2_crypto/ und strategies/volatility_breakout_crypto/)
wird taegliche Kursdaten (1d) fuer die 25 Top-Symbole benoetigt - die gab es
bisher nicht (nur 15m/1h/4h, siehe fetch_4h_data.py-Docstring).

In der Sandbox ist der direkte Binance-API-Zugriff blockiert (getestet:
CONNECT tunnel failed, 403 - dieselbe Einschraenkung wie bei Yahoo Finance
fuer die Aktien-Bots). Deshalb werden die Tageskerzen hier aus den bereits
vorhandenen 1h-Daten (5 Jahre Historie, 2021-09 bis heute) abgeleitet
(Resampling: open=erste Stunde, high=Max, low=Min, close=letzte Stunde,
volume=Summe des Tages, UTC-Tagesgrenzen wie Binance selbst verwendet).

WICHTIG - Einordnung dieser Naeherung:
- Das ist eine ABGELEITETE, keine nativ von Binance abgerufene Tageskerze.
  Fuer OHLC ist das exakt (ein UTC-Tag aus 1h-Kerzen ergibt exakt dieselben
  Werte wie eine native 1d-Kerze), da OHLC-Aggregation verlustfrei ist.
- Die Historie ist auf die verfuegbare 1h-Historie begrenzt (~5 Jahre statt
  z.B. 10 Jahre wie bei den Aktien-Bots) - kuerzer als die Aktien-Prototypen,
  aber deckt die relevante Stress-Periode 2022 ("Krypto-Winter") ab.
- Auf der echten Maschine des Nutzers (mit Binance-API-Zugriff) waere ein
  echter fetch_1d_data.py analog zu fetch_4h_data.py vorzuziehen (laengere,
  nativ abgerufene Historie moeglich) - dieses Skript ist ein reiner
  Sandbox-Ersatz fuer die Prototyp-Validierung, kein Vorschlag fuer den
  Live-Datenabruf.

Speichert unter data/<SYMBOL>_1d.csv - gleiches Namensschema wie bei den
Aktien-Bots (dort <TICKER>_1d.csv), keine Kollision da Krypto-Symbole immer
auf USDT enden.
"""

import os
import sys
import pandas as pd

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SHARED_DIR)

from paths import DATA_DIR
from symbols_config import SYMBOLS

SOURCE_INTERVAL = "1h"
TARGET_INTERVAL = "1d"


def resample_to_daily(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("open_time").set_index("open_time")
    daily = df.resample("1D", label="left", closed="left").agg({
        "open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum",
    })
    daily = daily.dropna(subset=["open", "high", "low", "close"])
    daily = daily.reset_index()
    return daily


if __name__ == "__main__":
    print(f"Leite Tageskerzen aus {SOURCE_INTERVAL}-Daten fuer {len(SYMBOLS)} Symbole ab...\n")
    ok, skipped = 0, []
    for symbol in SYMBOLS:
        src_path = os.path.join(DATA_DIR, f"{symbol}_{SOURCE_INTERVAL}.csv")
        if not os.path.exists(src_path):
            print(f"Fehlt: {src_path}")
            skipped.append(symbol)
            continue
        df = pd.read_csv(src_path, parse_dates=["open_time"])
        daily = resample_to_daily(df)
        out_path = os.path.join(DATA_DIR, f"{symbol}_{TARGET_INTERVAL}.csv")
        daily.to_csv(out_path, index=False)
        print(f"  {symbol}: {len(daily)} Tageskerzen ({daily['open_time'].min().date()} bis "
              f"{daily['open_time'].max().date()}) -> {out_path}")
        ok += 1

    print(f"\n{ok} Symbole verarbeitet, {len(skipped)} uebersprungen (fehlende Quelldaten).")

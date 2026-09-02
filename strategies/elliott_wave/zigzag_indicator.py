"""
Phase 2a - Zigzag-Indikator
============================
Filtert die Kursbewegung auf ihre signifikanten Hoch-/Tiefpunkte (Pivots).
Das ist der erste Baustein fuer eine Elliott-Wave-Analyse: Elliott Wave
zaehlt Wellen zwischen Pivots, nicht zwischen jeder einzelnen Kerze.

Baut auf der CSV aus Phase 1 auf (fetch_binance_data.py).
"""

import os
import sys
import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
DATA_DIR = _P["DATA_DIR"]
RESULTS_DIR = _P["RESULTS_DIR"]


def calculate_zigzag(df: pd.DataFrame, deviation_pct: float = 3.0) -> pd.DataFrame:
    """
    Berechnet Zigzag-Pivots auf Basis von High/Low-Preisen.

    deviation_pct: Mindestbewegung in Prozent, damit ein neuer Pivot
                   erkannt wird. Kleinere Werte = mehr, kleinere Wellen.
                   Groessere Werte = weniger, groessere Wellen.
                   Das ist der wichtigste Parameter, den der
                   Optimisation Agent spaeter testen wird.

    Rueckgabe: DataFrame nur mit den erkannten Pivot-Punkten
               (Zeitpunkt, Preis, Typ "high"/"low").
    """
    highs = df["high"].values
    lows = df["low"].values
    times = df["open_time"].values

    pivots = []

    # Startpunkt: erste Kerze als vorlaeufiger Pivot
    last_pivot_price = highs[0]
    last_pivot_idx = 0
    trend = None  # "up" oder "down" - wird beim ersten klaren Ausschlag gesetzt

    for i in range(1, len(df)):
        # Pruefen, ob sich der Preis seit dem letzten Pivot signifikant
        # nach oben oder unten bewegt hat
        move_up_pct = (highs[i] - last_pivot_price) / last_pivot_price * 100
        move_down_pct = (last_pivot_price - lows[i]) / last_pivot_price * 100

        if trend is None:
            if move_up_pct >= deviation_pct:
                trend = "up"
                last_pivot_price = lows[last_pivot_idx]
                last_pivot_idx = i
            elif move_down_pct >= deviation_pct:
                trend = "down"
                last_pivot_price = highs[last_pivot_idx]
                last_pivot_idx = i
            continue

        if trend == "up":
            # Neues Hoch innerhalb des Aufwaertstrends -> Pivot verschieben
            if highs[i] > last_pivot_price:
                last_pivot_price = highs[i]
                last_pivot_idx = i
            # Umkehr erkannt -> Pivot fixieren, Trend wechselt
            elif (last_pivot_price - lows[i]) / last_pivot_price * 100 >= deviation_pct:
                pivots.append((times[last_pivot_idx], last_pivot_price, "high"))
                trend = "down"
                last_pivot_price = lows[i]
                last_pivot_idx = i

        elif trend == "down":
            if lows[i] < last_pivot_price:
                last_pivot_price = lows[i]
                last_pivot_idx = i
            elif (highs[i] - last_pivot_price) / last_pivot_price * 100 >= deviation_pct:
                pivots.append((times[last_pivot_idx], last_pivot_price, "low"))
                trend = "up"
                last_pivot_price = highs[i]
                last_pivot_idx = i

    return pd.DataFrame(pivots, columns=["time", "price", "type"])


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(DATA_DIR, "BTCUSDT_1h.csv"), parse_dates=["open_time"])

    zigzag = calculate_zigzag(df, deviation_pct=3.0)

    print(f"{len(zigzag)} Pivot-Punkte gefunden (bei 3% Schwelle):\n")
    print(zigzag)

    output_path = os.path.join(RESULTS_DIR, "BTCUSDT_zigzag.csv")
    zigzag.to_csv(output_path, index=False)
    print(f"\nGespeichert als: {output_path}")

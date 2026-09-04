"""
Indikator-Berechnung: RSI(2) Mean-Reversion Krypto (nach Larry Connors)
=====================================================================
Identisch zu rsi2_mean_reversion/indicators.py (eigenstaendige Kopie,
Architektur-Prinzip: jede Strategie unabhaengig). Zwei Indikatoren:

- SMA(n): einfacher gleitender Durchschnitt des Schlusskurses ueber n Tage.
- RSI(n): Relative-Strength-Index nach Wilder, hier mit n=2.

Wilder-Glaettung (klassische RSI-Definition): RS = durchschnittlicher
Gewinn / durchschnittlicher Verlust ueber die Periode (Wilder-RMA-
Glaettung, nicht einfacher gleitender Durchschnitt),
RSI = 100 - 100/(1+RS).
"""

import numpy as np
import pandas as pd


def sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window).mean()


def rsi(series: pd.Series, period: int = 2) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi_value = 100 - (100 / (1 + rs))
    rsi_value = rsi_value.where(avg_loss != 0, 100.0)
    return rsi_value


def calculate_atr(df: pd.DataFrame, length: int) -> pd.Series:
    """Average True Range - Basis fuer SuperTrend. Identisch zu
    t3_supertrend/indicators.py (eigenstaendige Kopie)."""
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low, (high - prev_close).abs(), (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / length, adjust=False).mean()


def calculate_supertrend(df: pd.DataFrame, atr_length: int, atr_mult: float) -> pd.DataFrame:
    """Fuer den BTC-Regime-Filter (siehe regime_filter.py) - exakte,
    unveraenderte Kopie von t3_supertrend/indicators.py (kein
    Cross-Strategy-Import, Architektur-Prinzip: jede Strategie
    eigenstaendig, aber dieselbe validierte Definition wie beim
    etablierten Filter-Vorbild).

    Rueckgabe: DataFrame mit Spalten 'supertrend' (Linie) und
    'supertrend_dir' (1 = Aufwaertstrend, -1 = Abwaertstrend).
    """
    atr = calculate_atr(df, atr_length)
    hl2 = (df["high"] + df["low"]) / 2

    upper_band = (hl2 + atr_mult * atr).to_numpy()
    lower_band = (hl2 - atr_mult * atr).to_numpy()
    close = df["close"].to_numpy()
    n = len(df)

    final_upper = np.empty(n)
    final_lower = np.empty(n)
    direction = np.empty(n, dtype=int)
    supertrend = np.empty(n)

    final_lower[0] = lower_band[0]
    final_upper[0] = upper_band[0]
    direction[0] = 1
    supertrend[0] = lower_band[0]

    for i in range(1, n):
        if lower_band[i] > final_lower[i - 1] or close[i - 1] < final_lower[i - 1]:
            final_lower[i] = lower_band[i]
        else:
            final_lower[i] = final_lower[i - 1]

        if upper_band[i] < final_upper[i - 1] or close[i - 1] > final_upper[i - 1]:
            final_upper[i] = upper_band[i]
        else:
            final_upper[i] = final_upper[i - 1]

        prev_dir = direction[i - 1]
        if prev_dir == 1 and close[i] < final_lower[i]:
            direction[i] = -1
        elif prev_dir == -1 and close[i] > final_upper[i]:
            direction[i] = 1
        else:
            direction[i] = prev_dir

        supertrend[i] = final_lower[i] if direction[i] == 1 else final_upper[i]

    result = df[["open_time"]].copy()
    result["supertrend"] = supertrend
    result["supertrend_dir"] = direction
    return result

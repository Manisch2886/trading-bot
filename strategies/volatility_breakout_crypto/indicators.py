"""
Indikator-Berechnung: Bollinger-Band-Squeeze-Breakout Krypto
==================================================================
Eigenstaendige Kopie von volatility_breakout/indicators.py
(Architektur-Prinzip), unveraendert - Bollinger-Baender/BandWidth/
Squeeze-Perzentil sind zeitrahmen-unabhaengige Standarddefinitionen, die
auf TAGESKERZEN direkt uebernommen werden koennen (siehe
backtest_breakout.py-Docstring fuer die Zeitrahmen-Begruendung).

Zusaetzlich: calculate_supertrend fuer den BTC-Regime-Filter (siehe
regime_filter.py), identische Definition wie t3_supertrend/indicators.py.
"""

import numpy as np
import pandas as pd


def bollinger_bands(close: pd.Series, period: int = 20, num_std: float = 2.0):
    middle = close.rolling(window=period).mean()
    std = close.rolling(window=period).std()
    upper = middle + num_std * std
    lower = middle - num_std * std
    return middle, upper, lower


def band_width(middle: pd.Series, upper: pd.Series, lower: pd.Series) -> pd.Series:
    return (upper - lower) / middle


def squeeze_threshold(width: pd.Series, lookback_days: int, percentile: float) -> pd.Series:
    return width.rolling(window=lookback_days).quantile(percentile / 100)


def calculate_atr(df: pd.DataFrame, length: int) -> pd.Series:
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low, (high - prev_close).abs(), (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / length, adjust=False).mean()


def calculate_supertrend(df: pd.DataFrame, atr_length: int, atr_mult: float) -> pd.DataFrame:
    """Fuer den BTC-Regime-Filter - exakte, unveraenderte Kopie von
    t3_supertrend/indicators.py (kein Cross-Strategy-Import)."""
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

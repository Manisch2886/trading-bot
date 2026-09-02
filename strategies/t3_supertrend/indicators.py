"""
Indikatoren fuer die T3/ADX/SuperTrend-Trendfolgestrategie
================================================================
Python-Nachbau der Kernindikatoren aus der urspruenglichen Pine-
Script-Vorlage - bereinigt um die dort gefundene doppelte
SuperTrend-Implementierung (im Original gab es zwei parallele,
leicht unterschiedliche SuperTrend-Berechnungen; hier nur eine).

- T3 (Tillson T3): geglätteter, reaktionsschneller gleitender
  Durchschnitt (mehrfache EMA-Glaettung + Gewichtungsfaktor).
- ADX: Trendstaerke-Indikator, filtert Handelssignale auf Phasen mit
  echtem Trend (statt Seitwaertsbewegung).
- SuperTrend: ATR-basierter Trendfolge-/Trailing-Indikator, dient
  hier als Ausstiegssignal (trailing exit statt festem Kursziel).
"""

import pandas as pd
import numpy as np


def calculate_t3(series: pd.Series, length: int, factor: float) -> pd.Series:
    """Tillson T3 - sechsfache EMA-Glaettung mit Gewichtungsfaktor."""
    e1 = series.ewm(span=length, adjust=False).mean()
    e2 = e1.ewm(span=length, adjust=False).mean()
    e3 = e2.ewm(span=length, adjust=False).mean()
    e4 = e3.ewm(span=length, adjust=False).mean()
    e5 = e4.ewm(span=length, adjust=False).mean()
    e6 = e5.ewm(span=length, adjust=False).mean()

    c1 = -factor ** 3
    c2 = 3 * factor ** 2 + 3 * factor ** 3
    c3 = -6 * factor ** 2 - 3 * factor - 3 * factor ** 3
    c4 = 1 + 3 * factor + factor ** 3 + 3 * factor ** 2

    return c1 * e6 + c2 * e5 + c3 * e4 + c4 * e3


def calculate_atr(df: pd.DataFrame, length: int) -> pd.Series:
    """Average True Range - Basis fuer SuperTrend."""
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / length, adjust=False).mean()


def calculate_adx(df: pd.DataFrame, di_length: int, adx_length: int) -> pd.Series:
    """Average Directional Index - misst Trendstaerke unabhaengig von der Richtung."""
    high, low = df["high"], df["low"]
    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

    tr = calculate_atr(df, di_length)  # RMA(TR) als Glaettungsbasis
    plus_dm_smooth = pd.Series(plus_dm, index=df.index).ewm(alpha=1 / di_length, adjust=False).mean()
    minus_dm_smooth = pd.Series(minus_dm, index=df.index).ewm(alpha=1 / di_length, adjust=False).mean()

    plus_di = 100 * plus_dm_smooth / tr.replace(0, np.nan)
    minus_di = 100 * minus_dm_smooth / tr.replace(0, np.nan)

    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    adx = dx.ewm(alpha=1 / adx_length, adjust=False).mean()
    return adx.fillna(0)


def calculate_supertrend(df: pd.DataFrame, atr_length: int, atr_mult: float) -> pd.DataFrame:
    """
    SuperTrend - EINE saubere Implementierung (im Original-Pine-Script
    gab es hierfuer zwei parallele, redundante Versionen).

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

    # NumPy-Array-Zugriff statt pandas .iloc - bei mehreren zehntausend
    # Kerzen (mehrjaehrige Historie x viele Symbole) deutlich schneller,
    # da .iloc bei jedem Zugriff spuerbaren Pandas-Overhead hat.
    for i in range(1, n):
        # Baender nur in Trendrichtung nachziehen (klassische SuperTrend-Regel)
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

    supertrend = pd.Series(supertrend, index=df.index)
    direction = pd.Series(direction, index=df.index)

    return pd.DataFrame({"supertrend": supertrend, "supertrend_dir": direction})


def calculate_vwap_daily(df: pd.DataFrame, bars_per_day: int = 6) -> pd.Series:
    """
    VWAP (Volume Weighted Average Price) mit taeglichem Reset.
    bars_per_day=6 entspricht 4h-Kerzen (24h / 4h = 6 Balken pro Tag).

    Getestet als Einstiegsfilter: Preis muss ueber VWAP liegen. Zeigte
    in Tests kaum Redundanz zu T3 (~48% Uebereinstimmung, nahe Zufall)
    und verbesserte Win Rate sowie Ø-Gewinn pro Trade deutlich.
    """
    typical_price = (df["high"] + df["low"] + df["close"]) / 3
    pv = typical_price * df["volume"]

    day_group = np.arange(len(df)) // bars_per_day
    cum_pv = pv.groupby(day_group).cumsum()
    cum_vol = df["volume"].groupby(day_group).cumsum()

    return cum_pv / cum_vol.replace(0, np.nan)


def compute_indicators(df: pd.DataFrame, t3_fast_length: int, t3_slow_length: int,
                        t3_factor: float, di_length: int, adx_length: int,
                        atr_length: int, atr_mult: float) -> pd.DataFrame:
    """Berechnet alle benoetigten Indikatoren und haengt sie als neue Spalten an."""
    result = df.copy()
    result["t3_fast"] = calculate_t3(df["close"], t3_fast_length, t3_factor)
    result["t3_slow"] = calculate_t3(df["close"], t3_slow_length, t3_factor)
    result["adx"] = calculate_adx(df, di_length, adx_length)

    st = calculate_supertrend(df, atr_length, atr_mult)
    result["supertrend"] = st["supertrend"]
    result["supertrend_dir"] = st["supertrend_dir"]

    result["vwap"] = calculate_vwap_daily(df)

    return result

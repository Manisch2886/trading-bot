"""
Indikator-Berechnung: Bollinger-Band-Squeeze-Breakout
==========================================================
Standard-Definitionen, keine Eigenkonstruktion:

- Bollinger-Baender (Bollinger, 1980er): Mittelband = SMA(n), oberes/unteres
  Band = Mittelband +/- k * Standardabweichung(n). Hier n=20, k=2.0 -
  Bollingers eigener Standard-Vorschlag und der in praktisch jeder
  TA-Bibliothek verwendete Default.
- Band-Breite ("BandWidth", John Bollinger selbst nennt dieses Konzept
  "BBSqueeze"): (oberes Band - unteres Band) / Mittelband - normiert die
  Breite relativ zum Kursniveau, damit sie ueber verschiedene Aktien und
  Zeitraeume vergleichbar ist.
- Squeeze-Schwelle: 25.-Perzentil (unterstes Quartil) der Breite ueber ein
  rollierendes 126-Tage-Fenster (ca. 6 Handelsmonate). Implementiert ueber
  die vektorisierte pandas-Rolling-Quantil-Funktion (kein Python-Loop noetig,
  siehe Performance-Lehre aus rsi2_mean_reversion/backtest_rsi2.py).
"""

import pandas as pd


def bollinger_bands(close: pd.Series, period: int = 20, num_std: float = 2.0):
    """Gibt (mittelband, oberes_band, unteres_band) zurueck."""
    middle = close.rolling(window=period).mean()
    std = close.rolling(window=period).std()
    upper = middle + num_std * std
    lower = middle - num_std * std
    return middle, upper, lower


def band_width(middle: pd.Series, upper: pd.Series, lower: pd.Series) -> pd.Series:
    return (upper - lower) / middle


def squeeze_threshold(width: pd.Series, lookback_days: int, percentile: float) -> pd.Series:
    """25.-Perzentil-WERT der Breite im rollierenden lookback_days-Fenster
    (inkl. aktuellem Tag) - schnell/vektorisiert via rolling().quantile()."""
    return width.rolling(window=lookback_days).quantile(percentile / 100)

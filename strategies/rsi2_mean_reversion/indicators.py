"""
Indikator-Berechnung: RSI(2) Mean-Reversion (nach Larry Connors)
=====================================================================
Nur zwei Indikatoren noetig, beide Standard-Definitionen, keine
Eigenkonstruktion:

- SMA(n): einfacher gleitender Durchschnitt des Schlusskurses ueber n Tage.
- RSI(n): Relative-Strength-Index nach Wilder, hier mit n=2 (statt der
  ueblichen 14) - Connors' Kernidee ist gerade die sehr kurze Periode fuer
  extreme Kurzfrist-Ueberverkauft-/Ueberkauft-Signale.

Wilder-Glaettung (klassische RSI-Definition, wie in Connors' eigenen
Verguenstigungen und praktisch jeder Standard-TA-Bibliothek verwendet):
RS = durchschnittlicher Gewinn / durchschnittlicher Verlust ueber die
Periode (Wilder-RMA-Glaettung, nicht einfacher gleitender Durchschnitt),
RSI = 100 - 100/(1+RS).
"""

import pandas as pd


def sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window).mean()


def rsi(series: pd.Series, period: int = 2) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Wilder-Glaettung ueber ewm(alpha=1/period) - Standard-RSI-Definition
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi_value = 100 - (100 / (1 + rs))
    # Wenn avg_loss=0 (nur Gewinne in der Periode) ist RSI per Definition 100
    rsi_value = rsi_value.where(avg_loss != 0, 100.0)
    return rsi_value

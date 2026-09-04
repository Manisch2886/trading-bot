"""
Indikator-Berechnung: Turtle Soup (False-Breakout-Reversal)
==================================================================
Ein Baustein: das rollierende N-Tage-Tief (Donchian-Kanal-Untergrenze),
auf Basis der TAGESTIEFS (nicht Schlusskurse) - Standard-Donchian-
Definition. Wichtig: das Fenster schliesst den AKTUELLEN Tag NICHT mit
ein (shift(1)) - sonst wuerde ein neues Tagestief immer "sich selbst"
unterschreiten und das Setup waere trivial immer erfuellt.
"""

import pandas as pd


def donchian_low(low: pd.Series, period: int) -> pd.Series:
    return low.shift(1).rolling(window=period).min()

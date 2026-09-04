"""
Indikator-Berechnung: Relative-Strength-Pair-Rotation
==========================================================
Zwei Bausteine, beide auf taeglichen Schlusskursen:

- Relative Staerke zwischen zwei Assets A und B: Differenz ihrer
  rollierenden N-Tage-Renditen (ret_A - ret_B). Differenz statt Verhaeltnis
  gewaehlt, um Divisions-/Skalierungsprobleme bei kleinen Renditen zu
  vermeiden (Standard-Definition in der Sektor-Rotations-Literatur, z.B.
  Faber "Relative Strength Strategies for Investing"). Positiv = A staerker,
  negativ = B staerker.
- Rollierende Korrelation der TAEGLICHEN RENDITEN beider Assets ueber ein
  festes 252-Tage-Fenster (ca. 1 Handelsjahr) - Basis fuer die
  Entkopplungs-Erkennung (siehe backtest_pair_rotation.py).
"""

import pandas as pd

CORRELATION_WINDOW = 252  # fest, kein Optimierungsparameter - siehe Docstring oben


def relative_strength(close_a: pd.Series, close_b: pd.Series, lookback_days: int) -> pd.Series:
    ret_a = close_a.pct_change(lookback_days)
    ret_b = close_b.pct_change(lookback_days)
    return ret_a - ret_b


def rolling_correlation(close_a: pd.Series, close_b: pd.Series,
                         window: int = CORRELATION_WINDOW) -> pd.Series:
    daily_ret_a = close_a.pct_change()
    daily_ret_b = close_b.pct_change()
    return daily_ret_a.rolling(window=window).corr(daily_ret_b)

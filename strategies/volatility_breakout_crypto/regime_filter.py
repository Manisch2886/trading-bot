"""
BTC-Markt-Regime-Filter (Referenz: t3_supertrend/regime_filter.py)
========================================================================
Wird hier auf ausdrueckliche Anfrage getestet, insbesondere weil die
Aktien-Version von Volatility Breakout ihre groesste Schwaeche genau in
anhaltenden Baerenmaerkten zeigte (siehe
results/volatility_breakout/PROTOTYPE_FINDINGS.md Abschnitt 10) - der
BTC-Regime-Filter koennte genau solche Phasen fuer Krypto abfedern.
Blockiert NEUE Einstiege, wenn BTC selbst (eigener taeglicher SuperTrend)
in einem Abwaertstrend ist.
"""

import pandas as pd
from indicators import calculate_supertrend

BTC_ATR_LENGTH = 22
BTC_ATR_MULT = 3.0


def compute_btc_regime(btc_df: pd.DataFrame, atr_length: int = BTC_ATR_LENGTH,
                        atr_mult: float = BTC_ATR_MULT) -> pd.DataFrame:
    st = calculate_supertrend(btc_df, atr_length, atr_mult)
    result = btc_df[["open_time"]].copy()
    result["btc_regime"] = st["supertrend_dir"]
    return result


def filter_trades_by_regime(trades: pd.DataFrame, btc_regime: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return trades

    trades = trades.copy()
    trades["entry_time"] = pd.to_datetime(trades["entry_time"])
    btc_regime_sorted = btc_regime.sort_values("open_time")

    merged = pd.merge_asof(
        trades.sort_values("entry_time"),
        btc_regime_sorted,
        left_on="entry_time", right_on="open_time", direction="backward",
    )

    filtered = merged[merged["btc_regime"] == 1].drop(columns=["open_time", "btc_regime"])
    return filtered.reset_index(drop=True)

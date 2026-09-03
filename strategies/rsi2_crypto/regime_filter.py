"""
BTC-Markt-Regime-Filter (Referenz: t3_supertrend/regime_filter.py)
========================================================================
Blockiert NEUE Einstiege, wenn Bitcoin selbst gerade in einem
Abwaertstrend ist (eigener SuperTrend auf BTC/USDT, hier auf Tagesbasis
statt 4h wie beim Original), unabhaengig davon, ob der einzelne Coin ein
Kaufsignal zeigt. Wird hier als EXPERIMENT getestet (siehe
experiment_btc_regime_filter.py), nicht standardmaessig aktiviert - auf
ausdrueckliche Anfrage als Referenzfilter aus dem T3/SuperTrend-Bot
uebernommen und fuer RSI-2 Krypto geprueft.
"""

import pandas as pd
from indicators import calculate_supertrend

BTC_ATR_LENGTH = 22
BTC_ATR_MULT = 3.0


def compute_btc_regime(btc_df: pd.DataFrame, atr_length: int = BTC_ATR_LENGTH,
                        atr_mult: float = BTC_ATR_MULT) -> pd.DataFrame:
    """Berechnet den BTC-eigenen SuperTrend als Marktregime-Signal."""
    st = calculate_supertrend(btc_df, atr_length, atr_mult)
    result = btc_df[["open_time"]].copy()
    result["btc_regime"] = st["supertrend_dir"]
    return result


def filter_trades_by_regime(trades: pd.DataFrame, btc_regime: pd.DataFrame) -> pd.DataFrame:
    """Behaelt nur Trades, deren Entry-Zeitpunkt in eine BTC-Aufwaertsphase
    faellt (btc_regime == 1). "As-of"-Merge: fuer jeden Trade wird das
    zuletzt bekannte BTC-Regime VOR dem Entry-Zeitpunkt gesucht."""
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

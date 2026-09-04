"""
Backtest-Engine: Bollinger-Band-Squeeze-Breakout Krypto
=========================================================
Long-only, Krypto, TAGESBASIS (bewusste Zeitrahmen-Entscheidung, siehe
PROTOTYPE_FINDINGS.md Abschnitt 0). Der Squeeze-Lookback (126 Tage, ca. 6
Monate) und der Zeit-Exit (15 Tage) sind in der Aktien-Version bereits in
"Handelstagen" (=Kalendertagen bei 24/7-Krypto) definiert - identische
Werte werden hier UNVERAENDERT auf Krypto-Tageskerzen uebertragen, weil
sich die Einheit (Tage) durch die bewusste Wahl von Tageskerzen 1:1
uebertraegt (kein Umrechnungsfaktor noetig, anders als bei einer Uebertragung
auf 1h/4h-Kerzen, wo 126 "Tage" erst in eine Kerzenzahl umgerechnet werden
muesste - genau das Problem, das die Tagesbasis-Entscheidung vermeidet).

Identisches Grundgeruest zu volatility_breakout/backtest_breakout.py
(eigenstaendige Kopie). REGELN (identisch zur Aktien-Version):

1. SQUEEZE-ERKENNUNG: Bollinger-Band-Breite (Periode 20, 2 Std.) faellt auf
   ein rollierendes 126-Tage-Tief (<=25.-Perzentil).
2. EINSTIEGS-TRIGGER: Squeeze am Vortag (t-1) UND Schlusskurs heute (t)
   ueber dem oberen Band von heute. Einstieg zum Schlusskurs. Kein
   Pyramiding.
3. AUSSTIEG - Prioritaet pro Tag:
   a) STOP-LOSS - Tagestief <= Stop-Kurs (Startwert 8%, wie bei der
      validierten Aktien-Version)
   b) ZEIT-EXIT - spaetestens nach MAX_HOLD_DAYS (15) Tagen
   Kein Trailing-Element in der Basis-Regel (siehe Aktien-Version:
   Trailing-Stop dort als Overfitting identifiziert - wird hier nicht
   erneut ungeprueft uebernommen).
4. Volumen-Filter: bei Krypto grundsaetzlich verfuegbar (Binance liefert
   Volumen), aber bei der Aktien-Version NICHT als Standard empfohlen
   (keine spuerbare Win-Rate-Verbesserung) - wird hier nicht erneut
   getestet, um den Analyseumfang nicht unnoetig auszuweiten; kann als
   Parameter weiterhin genutzt werden (use_volume_filter), Standard: aus.

Kosten: 0.1% Gebuehr + 0.05% Slippage je Entry/Exit (Binance-Spot-
Konvention, gleiche Annahme wie bei den bestehenden Krypto-Bots).
"""

import numpy as np
import pandas as pd

from indicators import bollinger_bands, band_width, squeeze_threshold

BB_PERIOD = 20
BB_NUM_STD = 2.0
SQUEEZE_LOOKBACK_DAYS = 126
SQUEEZE_PERCENTILE = 25.0
VOLUME_AVG_PERIOD = 20
VOLUME_FILTER_MULTIPLIER = 1.5
MAX_HOLD_DAYS = 15

TRADING_FEE_PCT = 0.1
SLIPPAGE_PCT = 0.05

WARMUP_PERIOD = max(BB_PERIOD, SQUEEZE_LOOKBACK_DAYS, VOLUME_AVG_PERIOD)


def compute_indicators(price_df: pd.DataFrame, squeeze_lookback_days: int = SQUEEZE_LOOKBACK_DAYS,
                        squeeze_percentile: float = SQUEEZE_PERCENTILE) -> pd.DataFrame:
    df = price_df.sort_values("open_time").reset_index(drop=True).copy()
    df["bb_middle"], df["bb_upper"], df["bb_lower"] = bollinger_bands(df["close"], BB_PERIOD, BB_NUM_STD)
    df["bb_width"] = band_width(df["bb_middle"], df["bb_upper"], df["bb_lower"])
    df["squeeze_thresh"] = squeeze_threshold(df["bb_width"], squeeze_lookback_days, squeeze_percentile)
    df["is_squeeze"] = df["bb_width"] <= df["squeeze_thresh"]
    df["vol_avg"] = df["volume"].rolling(window=VOLUME_AVG_PERIOD).mean()
    return df


def run_backtest(price_df: pd.DataFrame, stop_loss_pct: float = 8.0, entry_cutoff=None,
                  max_hold_days: int = MAX_HOLD_DAYS, use_volume_filter: bool = False,
                  volume_filter_multiplier: float = VOLUME_FILTER_MULTIPLIER) -> pd.DataFrame:
    df = price_df
    close = df["close"].to_numpy()
    low = df["low"].to_numpy()
    volume = df["volume"].to_numpy()
    vol_avg = df["vol_avg"].to_numpy()
    upper = df["bb_upper"].to_numpy()
    is_squeeze = df["is_squeeze"].to_numpy()
    open_time = df["open_time"].to_numpy()
    n = len(df)

    start_i = WARMUP_PERIOD + 1
    if entry_cutoff is not None:
        start_i = max(start_i, int((df["open_time"] < entry_cutoff).sum()))

    trades = []
    i = start_i
    while i < n:
        if np.isnan(upper[i]) or np.isnan(close[i]):
            i += 1
            continue

        squeeze_yesterday = bool(is_squeeze[i - 1])
        breakout_today = close[i] > upper[i]

        if not (squeeze_yesterday and breakout_today):
            i += 1
            continue

        if use_volume_filter:
            if np.isnan(vol_avg[i]) or volume[i] <= volume_filter_multiplier * vol_avg[i]:
                i += 1
                continue

        entry_time = open_time[i]
        entry_price = close[i]
        stop_price = entry_price * (1 - stop_loss_pct / 100) if stop_loss_pct is not None else None

        exit_idx, exit_price, result = None, None, None
        max_offset = min(max_hold_days, n - 1 - i)
        for offset in range(1, max_offset + 1):
            idx = i + offset
            if stop_price is not None and low[idx] <= stop_price:
                exit_idx, exit_price, result = idx, stop_price, "stop_loss"
                break
            if offset == max_hold_days:
                exit_idx, exit_price, result = idx, close[idx], "time_exit"
                break

        if exit_idx is None:
            break

        if entry_cutoff is None or entry_time >= np.datetime64(entry_cutoff):
            pnl_pct = (exit_price - entry_price) / entry_price * 100
            total_cost_pct = 2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)
            holding_days = (pd.Timestamp(open_time[exit_idx]) - pd.Timestamp(entry_time)).days
            trades.append({
                "entry_time": pd.Timestamp(entry_time), "entry_price": entry_price,
                "exit_time": pd.Timestamp(open_time[exit_idx]), "exit_price": exit_price,
                "result": result, "pnl_pct": round(pnl_pct - total_cost_pct, 2),
                "holding_days": holding_days,
            })

        i = exit_idx + 1

    return pd.DataFrame(trades)


if __name__ == "__main__":
    import os
    import sys
    _STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
    _SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
    sys.path.insert(0, _SHARED_DIR)
    from strategy_paths import get_strategy_paths
    _P = get_strategy_paths(__file__)

    price_df = pd.read_csv(os.path.join(_P["DATA_DIR"], "BTCUSDT_1d.csv"), parse_dates=["open_time"])
    df = compute_indicators(price_df)
    trades = run_backtest(df, stop_loss_pct=8.0)

    print(f"BTCUSDT: {len(trades)} Trades gefunden.\n")
    if not trades.empty:
        win_rate = (trades["pnl_pct"] > 0).mean() * 100
        print(f"Win Rate: {win_rate:.1f}%  |  Ø PnL: {trades['pnl_pct'].mean():.2f}%  |  "
              f"Ø Haltedauer: {trades['holding_days'].mean():.1f} Tage")

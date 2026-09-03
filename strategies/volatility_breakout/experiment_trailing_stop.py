"""
Test: Trailing-Stop statt/zusaetzlich zum festen Stop-Loss (bewusst skeptisch)
====================================================================================
WICHTIG: Trailing-Take-Profit hat sich beim Aktien-Elliott-Wave-Bot als
Overfitting-Muster erwiesen (sah im Gesamtzeitraum vielversprechend aus,
hielt der Out-of-Sample-Pruefung nicht stand - siehe
elliott_wave_stocks/EXPERIMENT_FINDINGS.md, Abschnitt 5). Wird hier NICHT
blind uebernommen, sondern mit identischer Skepsis getestet: Gesamtzeitraum
UND Out-of-Sample separat, Rangfolge-Stabilitaet explizit geprueft.

Der Stop wandert mit dem seit Einstieg erreichten Kurshoechststand nach oben
(fester Abstand X% darunter), der urspruengliche feste Stop (8% unter
Einstieg, aus multi_symbol_optimise.py) bleibt aktiv, bis der Trailing-Stop
ihn ueberholt. Kein Blick in die Zukunft innerhalb eines Balkens: der
Trailing-Stop wird erst NACH der Stop-Pruefung eines Balkens anhand von
dessen High aktualisiert.
"""

import os
import pandas as pd

from multi_symbol_optimise import load_all_symbol_data
from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO
from equity_simulation import collect_all_trades, simulate_portfolio, calculate_max_drawdown, \
    STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS, STOP_LOSS_PCT
from pipeline_report import collect_trades_windowed
from backtest_breakout import MAX_HOLD_DAYS, TRADING_FEE_PCT, SLIPPAGE_PCT
from strategy_paths import get_strategy_paths

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

TRAILING_DISTANCES = [8.0, 12.0, 15.0]


def simulate_trade_trailing(price_df: pd.DataFrame, start_idx: int, entry_price: float,
                             initial_stop_price: float, trailing_pct: float, max_hold_days: int) -> dict:
    df = price_df
    close = df["close"].to_numpy()
    low = df["low"].to_numpy()
    high = df["high"].to_numpy()
    open_time = df["open_time"].to_numpy()
    n = len(df)

    stop_price = initial_stop_price
    running_high = entry_price
    max_offset = min(max_hold_days, n - 1 - start_idx)

    for offset in range(1, max_offset + 1):
        idx = start_idx + offset
        if low[idx] <= stop_price:
            result = "stop_loss" if stop_price == initial_stop_price else "trailing_stop"
            return {"exit_idx": idx, "exit_price": stop_price, "result": result}
        running_high = max(running_high, high[idx])
        candidate_stop = running_high * (1 - trailing_pct / 100)
        if candidate_stop > stop_price:
            stop_price = candidate_stop
        if offset == max_hold_days:
            return {"exit_idx": idx, "exit_price": close[idx], "result": "time_exit"}

    return {"exit_idx": None, "exit_price": None, "result": "no_data"}


def run_backtest_trailing(price_df: pd.DataFrame, stop_loss_pct: float, trailing_pct: float,
                           entry_cutoff=None, max_hold_days: int = MAX_HOLD_DAYS) -> pd.DataFrame:
    df = price_df
    close = df["close"].to_numpy()
    upper = df["bb_upper"].to_numpy()
    is_squeeze = df["is_squeeze"].to_numpy()
    open_time = df["open_time"].to_numpy()
    n = len(df)

    from backtest_breakout import WARMUP_PERIOD
    start_i = WARMUP_PERIOD + 1
    if entry_cutoff is not None:
        start_i = max(start_i, int((df["open_time"] < entry_cutoff).sum()))

    trades = []
    i = start_i
    while i < n:
        if pd.isna(upper[i]) or pd.isna(close[i]):
            i += 1
            continue
        if not (bool(is_squeeze[i - 1]) and close[i] > upper[i]):
            i += 1
            continue

        entry_time = open_time[i]
        entry_price = close[i]
        initial_stop = entry_price * (1 - stop_loss_pct / 100)

        outcome = simulate_trade_trailing(df, i, entry_price, initial_stop, trailing_pct, max_hold_days)
        if outcome["exit_idx"] is None:
            break

        if entry_cutoff is None or entry_time >= pd.Timestamp(entry_cutoff).to_datetime64():
            pnl_pct = (outcome["exit_price"] - entry_price) / entry_price * 100
            total_cost_pct = 2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)
            holding_days = (pd.Timestamp(open_time[outcome["exit_idx"]]) - pd.Timestamp(entry_time)).days
            trades.append({
                "entry_time": pd.Timestamp(entry_time), "entry_price": entry_price,
                "exit_time": pd.Timestamp(open_time[outcome["exit_idx"]]), "exit_price": outcome["exit_price"],
                "result": outcome["result"], "pnl_pct": round(pnl_pct - total_cost_pct, 2),
                "holding_days": holding_days,
            })

        i = outcome["exit_idx"] + 1

    return pd.DataFrame(trades)


def collect_all_trades_trailing(all_data: dict, stop_loss_pct: float, trailing_pct: float) -> pd.DataFrame:
    all_trades = []
    for symbol, (df_ind, entry_cutoff) in all_data.items():
        trades = run_backtest_trailing(df_ind, stop_loss_pct, trailing_pct, entry_cutoff)
        if not trades.empty:
            trades = trades.copy()
            trades["symbol"] = symbol
            all_trades.append(trades)
    if not all_trades:
        return pd.DataFrame()
    combined = pd.concat(all_trades, ignore_index=True)
    combined["entry_time"] = pd.to_datetime(combined["entry_time"])
    combined["exit_time"] = pd.to_datetime(combined["exit_time"])
    return combined.sort_values("entry_time").reset_index(drop=True)


def collect_trades_trailing_windowed(windowed_data: dict, stop_loss_pct: float, trailing_pct: float) -> pd.DataFrame:
    all_trades = []
    for symbol, (df_ind, cutoff_start, cutoff_end) in windowed_data.items():
        trades = run_backtest_trailing(df_ind, stop_loss_pct, trailing_pct, cutoff_start)
        if cutoff_end is not None and not trades.empty:
            trades = trades[trades["entry_time"] < cutoff_end]
        if not trades.empty:
            trades = trades.copy()
            trades["symbol"] = symbol
            all_trades.append(trades)
    if not all_trades:
        return pd.DataFrame()
    combined = pd.concat(all_trades, ignore_index=True)
    combined["entry_time"] = pd.to_datetime(combined["entry_time"])
    combined["exit_time"] = pd.to_datetime(combined["exit_time"])
    return combined.sort_values("entry_time").reset_index(drop=True)


def evaluate(trades: pd.DataFrame, label: str) -> dict:
    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)
    total_return_pct = round((result["final_capital"] / STARTING_CAPITAL - 1) * 100, 2)
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    return {
        "variante": label, "final_capital": result["final_capital"], "total_return_pct": total_return_pct,
        "trades_ausgefuehrt": result["num_executed"], "trades_uebersprungen": result["num_skipped"],
        "max_drawdown_pct": max_dd,
    }


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)

    print("=" * 90)
    print("GESAMTZEITRAUM")
    print("=" * 90)
    full_rows = []
    trades_baseline_full = collect_all_trades(all_data, STOP_LOSS_PCT)
    full_rows.append(evaluate(trades_baseline_full, f"Baseline: fester Stop {STOP_LOSS_PCT}%, kein Trailing"))
    for trailing_pct in TRAILING_DISTANCES:
        trades_t = collect_all_trades_trailing(all_data, STOP_LOSS_PCT, trailing_pct)
        full_rows.append(evaluate(trades_t, f"Trailing {trailing_pct:.0f}%"))
    full_df = pd.DataFrame(full_rows)
    print(full_df.to_string(index=False))

    print("\n" + "=" * 90)
    print("OUT-OF-SAMPLE")
    print("=" * 90)
    oos_rows = []
    trades_baseline_oos = collect_trades_windowed(test_data, STOP_LOSS_PCT)
    oos_rows.append(evaluate(trades_baseline_oos, f"Baseline: fester Stop {STOP_LOSS_PCT}%, kein Trailing"))
    for trailing_pct in TRAILING_DISTANCES:
        trades_t = collect_trades_trailing_windowed(test_data, STOP_LOSS_PCT, trailing_pct)
        oos_rows.append(evaluate(trades_t, f"Trailing {trailing_pct:.0f}%"))
    oos_df = pd.DataFrame(oos_rows)
    print(oos_df.to_string(index=False))

    print("\n" + "=" * 90)
    print("RANGFOLGE-STABILITAET (Overfitting-Check)")
    print("=" * 90)
    full_rank = full_df.sort_values("total_return_pct", ascending=False)["variante"].tolist()
    oos_rank = oos_df.sort_values("total_return_pct", ascending=False)["variante"].tolist()
    print(f"Gesamtzeitraum-Rangfolge (Rendite): {full_rank}")
    print(f"Out-of-Sample-Rangfolge (Rendite):  {oos_rank}")
    print(f"Beste Variante identisch: {full_rank[0] == oos_rank[0]}")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    full_df.to_csv(os.path.join(RESULTS_DIR, "experiment_trailing_stop_full.csv"), index=False)
    oos_df.to_csv(os.path.join(RESULTS_DIR, "experiment_trailing_stop_oos.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_trailing_stop_{{full,oos}}.csv")

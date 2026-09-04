"""
Vollstaendiger Pipeline-Report: Turtle Soup (Krypto)
==================================================================
Analog zu den anderen Bots.
"""

import os
import pandas as pd

from multi_symbol_optimise import load_all_symbol_data, get_trades_for_symbol
from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO
from equity_simulation import (
    collect_all_trades, simulate_portfolio, calculate_max_drawdown,
    STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS, DONCHIAN_PERIOD, STOP_MODE,
)
from buy_and_hold_benchmark import calculate_buy_and_hold
from strategy_paths import get_strategy_paths

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]


def collect_trades_windowed(windowed_data: dict, donchian_period: int, stop_mode=None) -> pd.DataFrame:
    all_trades = []
    for symbol, (price_df, cutoff_start, cutoff_end) in windowed_data.items():
        trades = get_trades_for_symbol(price_df, donchian_period, stop_mode, cutoff_start)
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


def evaluate(trades: pd.DataFrame) -> dict:
    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)
    total_return_pct = round((result["final_capital"] / STARTING_CAPITAL - 1) * 100, 2)
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    return {
        "final_capital": result["final_capital"], "total_return_pct": total_return_pct,
        "trades_ausgefuehrt": result["num_executed"], "trades_uebersprungen": result["num_skipped"],
        "max_drawdown_pct": max_dd,
    }


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)

    trades_full = collect_all_trades(all_data, DONCHIAN_PERIOD, STOP_MODE)
    trades_oos = collect_trades_windowed(test_data, DONCHIAN_PERIOD, STOP_MODE)

    print("=" * 70)
    print(f"GESAMTZEITRAUM (Donchian {DONCHIAN_PERIOD}, Stop {STOP_MODE}, "
          f"{ALLOCATION_PCT*100:.0f}% Allokation, Limit {MAX_CONCURRENT_POSITIONS})")
    print("=" * 70)
    result_full = evaluate(trades_full)
    print(result_full)

    print("\n" + "=" * 70)
    print("OUT-OF-SAMPLE")
    print("=" * 70)
    result_oos = evaluate(trades_oos)
    print(result_oos)

    print("\n" + "=" * 70)
    print("BUY-AND-HOLD-VERGLEICH")
    print("=" * 70)
    bh_result = calculate_buy_and_hold(all_data, STARTING_CAPITAL)
    print(bh_result)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    pd.DataFrame([result_full]).to_csv(os.path.join(RESULTS_DIR, "pipeline_report_full.csv"), index=False)
    pd.DataFrame([result_oos]).to_csv(os.path.join(RESULTS_DIR, "pipeline_report_oos.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/pipeline_report_{{full,oos}}.csv")

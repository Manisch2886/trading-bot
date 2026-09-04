"""
Vollstaendiger Pipeline-Report: Pair-Rotation (Krypto)
==================================================================
Analog zu den anderen Bots. WICHTIG: siehe
PROTOTYPE_FINDINGS.md/multi_pair_walk_forward.py - die hier verwendete
Konfiguration ist NICHT Out-of-Sample-validiert (alle 18 getesteten
Kombinationen scheitern Out-of-Sample), dieser Report dient der
vollstaendigen Pipeline-Dokumentation.
"""

import os
import pandas as pd

from multi_pair_optimise import load_all_symbol_data, get_reference_date, build_pairs
from multi_pair_walk_forward import split_window, TRAIN_SPLIT_RATIO
from equity_simulation import (
    collect_all_trades, simulate_portfolio, calculate_max_drawdown,
    STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS,
    LOOKBACK_DAYS, REBALANCE_DAYS, STOP_LOSS_PCT,
)
from buy_and_hold_benchmark import calculate_buy_and_hold
from strategy_paths import get_strategy_paths

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]


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
    symbol_data = load_all_symbol_data()
    reference_date = get_reference_date(symbol_data)
    window_start, split_time, window_end = split_window(reference_date, symbol_data, TRAIN_SPLIT_RATIO)
    pairs = build_pairs(symbol_data, reference_date)

    trades_full = collect_all_trades(pairs, LOOKBACK_DAYS, REBALANCE_DAYS, STOP_LOSS_PCT, reference_date)
    trades_oos = collect_all_trades(pairs, LOOKBACK_DAYS, REBALANCE_DAYS, STOP_LOSS_PCT, split_time)

    print("=" * 70)
    print(f"GESAMTZEITRAUM (Lookback {LOOKBACK_DAYS}, Rebalance {REBALANCE_DAYS}, "
          f"Stop {STOP_LOSS_PCT}, {ALLOCATION_PCT*100:.0f}% Allokation, Limit {MAX_CONCURRENT_POSITIONS})")
    print("=" * 70)
    result_full = evaluate(trades_full)
    print(result_full)

    print("\n" + "=" * 70)
    print("OUT-OF-SAMPLE (NICHT Out-of-Sample-validierte Konfiguration, siehe Modul-Docstring)")
    print("=" * 70)
    result_oos = evaluate(trades_oos)
    print(result_oos)

    print("\n" + "=" * 70)
    print("BUY-AND-HOLD-VERGLEICH")
    print("=" * 70)
    bh_result = calculate_buy_and_hold(symbol_data, pairs, STARTING_CAPITAL, reference_date)
    print(bh_result)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    pd.DataFrame([result_full]).to_csv(os.path.join(RESULTS_DIR, "pipeline_report_full.csv"), index=False)
    pd.DataFrame([result_oos]).to_csv(os.path.join(RESULTS_DIR, "pipeline_report_oos.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/pipeline_report_{{full,oos}}.csv")

"""
Kombinierter Test: Take-Profit x Positionslimit (Aktien-Bot)
==================================================================
Folgeschritt zu experiment_no_take_profit.py und experiment_position_limit.py:
beide Dimensionen wurden dort nur isoliert getestet (jeweils die andere auf
dem aktuellen Live-Wert fixiert). Da "kein Take-Profit" die Haltedauer pro
Position erhoeht und dadurch mehr Trades am Positionslimit scheitern (siehe
EXPERIMENT_FINDINGS.md, "Nebeneffekt"), ist die naheliegende offene Frage: profitiert
die "kein Take-Profit"-Variante besonders stark von einem hoeheren/unbegrenzten
Positionslimit - mehr als die "mit Take-Profit"-Variante das tut?

Testet die volle 2x4-Matrix (Take-Profit an/aus x Limit 3/5/8/unbegrenzt),
wieder ueber den gesamten Zeitraum UND isoliert Out-of-Sample, mit sonst
unveraenderten aktuellen Live-Parametern (Zigzag 5%, Stop-Loss 3%).
"""

import os
import sys
import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

from multi_symbol_optimise import load_all_symbol_data
from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO
from equity_simulation import collect_all_trades, simulate_portfolio, calculate_max_drawdown
from live_params import DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB

STARTING_CAPITAL = 10_000.0
ALLOCATION_PCT = 0.10
POSITION_LIMITS = [3, 5, 8, None]
TP_VARIANTS = [("mit Take-Profit", True), ("ohne Take-Profit", False)]


def run_matrix(all_data: dict) -> pd.DataFrame:
    rows = []
    for tp_label, use_tp in TP_VARIANTS:
        trades = collect_all_trades(all_data, DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB, use_tp)
        for limit in POSITION_LIMITS:
            result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, limit)
            total_return_pct = (result["final_capital"] / STARTING_CAPITAL - 1) * 100
            max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
            rows.append({
                "take_profit": tp_label,
                "max_concurrent_positions": limit if limit is not None else "unbegrenzt",
                "final_capital": result["final_capital"],
                "total_return_pct": round(total_return_pct, 2),
                "executed_trades": result["num_executed"],
                "skipped_trades": result["num_skipped"],
                "max_drawdown_pct": max_dd,
            })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(f"Feste Parameter (aktueller Live-Stand): Zigzag {DEVIATION_PCT}% | "
          f"Stop-Loss {STOP_LOSS_PCT}% | Take-Profit Fib {TAKE_PROFIT_FIB}\n")

    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden.")
        exit()

    print("=" * 70)
    print("TEIL 1: Volle Matrix, gesamter Zeitraum")
    print("=" * 70)
    full_df = run_matrix(all_data)
    print(full_df.to_string(index=False))

    print("\n" + "=" * 70)
    print("TEIL 2: Volle Matrix, Out-of-Sample (letzte 30%, keine Re-Optimierung)")
    print("=" * 70)
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)
    example_symbol = list(all_data.keys())[0]
    print(f"Out-of-Sample-Zeitraum: {test_data[example_symbol]['open_time'].min()} "
          f"bis {test_data[example_symbol]['open_time'].max()}\n")

    oos_df = run_matrix(test_data)
    print(oos_df.to_string(index=False))

    full_df.to_csv(os.path.join(RESULTS_DIR, "experiment_combined_full.csv"), index=False)
    oos_df.to_csv(os.path.join(RESULTS_DIR, "experiment_combined_oos.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_combined_full.csv")
    print(f"Gespeichert unter: {RESULTS_DIR}/experiment_combined_oos.csv")

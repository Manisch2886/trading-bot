"""
Experiment: Positionsgroesse x Positionslimit fuer Volatility Breakout (analog zu RSI-2)
================================================================================================
Bestaetigter Kapital-Flaschenhals (siehe experiment_signal_quality.py: 73%
Skip-Rate, Portfolio-Rendite Real vs. Kapital-unbegrenzt +142,06%->+1088,99%
Gesamtzeitraum). Testet daher beide Dimensionen gemeinsam: Positionsgroesse
(10%/5%/3%/2%) x Limit (8/15/20/unbegrenzt), fixe Parameter 8% Stop-Loss,
15 Handelstage Zeit-Exit (validierte Basiskonfiguration aus
multi_symbol_optimise.py/backtest_breakout.py), Gesamtzeitraum UND
Out-of-Sample.
"""

import os
import pandas as pd

from multi_symbol_optimise import load_all_symbol_data
from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO
from equity_simulation import collect_all_trades, simulate_portfolio, calculate_max_drawdown, \
    STARTING_CAPITAL, STOP_LOSS_PCT
from pipeline_report import collect_trades_windowed
from strategy_paths import get_strategy_paths

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

ALLOCATION_PCTS = [0.10, 0.05, 0.03, 0.02]
POSITION_LIMITS = [8, 15, 20, None]


def evaluate(trades: pd.DataFrame, allocation_pct: float, max_concurrent) -> dict:
    result = simulate_portfolio(trades, STARTING_CAPITAL, allocation_pct, max_concurrent)
    total_return_pct = (result["final_capital"] / STARTING_CAPITAL - 1) * 100
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    return {
        "allocation_pct": f"{allocation_pct*100:.0f}%",
        "limit": max_concurrent if max_concurrent is not None else "unbegrenzt",
        "final_capital": result["final_capital"],
        "total_return_pct": round(total_return_pct, 2),
        "trades_ausgefuehrt": result["num_executed"],
        "trades_uebersprungen": result["num_skipped"],
        "max_drawdown_pct": max_dd,
    }


def run_matrix(trades: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for allocation_pct in ALLOCATION_PCTS:
        for limit in POSITION_LIMITS:
            rows.append(evaluate(trades, allocation_pct, limit))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(f"Feste Parameter: Stop-Loss {STOP_LOSS_PCT}% | Zeit-Exit 15 Handelstage "
          f"(validierte Basiskonfiguration)\n")

    all_data = load_all_symbol_data()
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)

    print("=" * 90)
    print("GESAMTZEITRAUM")
    print("=" * 90)
    trades_full = collect_all_trades(all_data, STOP_LOSS_PCT)
    print(f"{len(trades_full)} Trades insgesamt gefunden.\n")
    full_df = run_matrix(trades_full)
    print(full_df.to_string(index=False))

    print("\n" + "=" * 90)
    print("OUT-OF-SAMPLE (letzte 30% je Symbol, keine Re-Optimierung)")
    print("=" * 90)
    trades_oos = collect_trades_windowed(test_data, STOP_LOSS_PCT)
    print(f"{len(trades_oos)} Trades im Out-of-Sample-Zeitraum gefunden.\n")
    oos_df = run_matrix(trades_oos)
    print(oos_df.to_string(index=False))

    full_df.to_csv(os.path.join(RESULTS_DIR, "experiment_position_size_limit_full.csv"), index=False)
    oos_df.to_csv(os.path.join(RESULTS_DIR, "experiment_position_size_limit_oos.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_position_size_limit_full.csv")
    print(f"Gespeichert unter: {RESULTS_DIR}/experiment_position_size_limit_oos.csv")

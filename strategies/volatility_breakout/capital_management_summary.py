"""
Zusammenfassende Tabelle: alle getesteten Kapitalmanagement-Konfigurationen
================================================================================
Fasst experiment_position_size_limit.py (Positionsgroesse x Limit, Voll- und
Out-of-Sample) und die 2022-Stress-Periode fuer JEDE der 16 getesteten
Kombinationen zusammen - Grundlage fuer eine spaetere Live-Entscheidung,
analog zum RSI-2-Kapitalmanagement-Report. Reine Analyse, nichts live
geschaltet.
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

STRESS_PERIOD_START = "2022-01-01"
STRESS_PERIOD_END = "2022-12-31"


def portfolio_eval(trades: pd.DataFrame, allocation_pct: float, limit) -> dict:
    result = simulate_portfolio(trades, STARTING_CAPITAL, allocation_pct, limit)
    total_return_pct = round((result["final_capital"] / STARTING_CAPITAL - 1) * 100, 2)
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    return {
        "final_capital": result["final_capital"], "total_return_pct": total_return_pct,
        "trades_ausgefuehrt": result["num_executed"], "trades_uebersprungen": result["num_skipped"],
        "max_drawdown_pct": max_dd, "equity_curve": result["equity_curve"],
    }


def stress_2022(trades: pd.DataFrame, allocation_pct: float, limit) -> dict:
    result = simulate_portfolio(trades, STARTING_CAPITAL, allocation_pct, limit)
    eq = result["equity_curve"]
    if eq.empty:
        return {"rendite_2022_pct": None, "max_dd_2022_pct": None}
    eq = eq.copy()
    eq["time"] = pd.to_datetime(eq["time"])
    eq = eq.sort_values("time")
    eq["date"] = eq["time"].dt.normalize()
    daily_last = eq.groupby("date")["capital_after"].last()
    full_range = pd.date_range(daily_last.index.min(), daily_last.index.max(), freq="D")
    daily_last = daily_last.reindex(full_range).ffill()
    if pd.isna(daily_last.iloc[0]):
        daily_last.iloc[0] = STARTING_CAPITAL

    stress_start = pd.Timestamp(STRESS_PERIOD_START)
    stress_end = pd.Timestamp(STRESS_PERIOD_END)
    window = daily_last[(daily_last.index >= stress_start) & (daily_last.index <= stress_end)]
    if window.empty:
        return {"rendite_2022_pct": None, "max_dd_2022_pct": None}
    running_max = window.cummax()
    dd = ((window - running_max) / running_max * 100).min()
    rendite = (window.iloc[-1] / window.iloc[0] - 1) * 100
    return {"rendite_2022_pct": round(rendite, 2), "max_dd_2022_pct": round(dd, 2)}


def main():
    print(f"Feste Parameter: Stop-Loss {STOP_LOSS_PCT}% | Zeit-Exit 15 Handelstage\n")

    all_data = load_all_symbol_data()
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)

    trades_full = collect_all_trades(all_data, STOP_LOSS_PCT)
    trades_oos = collect_trades_windowed(test_data, STOP_LOSS_PCT)

    rows = []
    for allocation_pct in ALLOCATION_PCTS:
        for limit in POSITION_LIMITS:
            limit_label = limit if limit is not None else "unbegrenzt"

            full_eval = portfolio_eval(trades_full, allocation_pct, limit)
            oos_eval = portfolio_eval(trades_oos, allocation_pct, limit)
            stress = stress_2022(trades_full, allocation_pct, limit)

            rows.append({
                "allokation": f"{allocation_pct*100:.0f}%",
                "limit": limit_label,
                "rendite_gesamt_pct": full_eval["total_return_pct"],
                "max_dd_gesamt_pct": full_eval["max_drawdown_pct"],
                "rendite_oos_pct": oos_eval["total_return_pct"],
                "max_dd_oos_pct": oos_eval["max_drawdown_pct"],
                "rendite_2022_pct": stress["rendite_2022_pct"],
                "max_dd_2022_pct": stress["max_dd_2022_pct"],
                "trades_ausgefuehrt_gesamt": full_eval["trades_ausgefuehrt"],
            })

    df = pd.DataFrame(rows).sort_values("rendite_oos_pct", ascending=False).reset_index(drop=True)

    print("=" * 130)
    print("ZUSAMMENFASSUNG ALLER GETESTETEN KAPITALMANAGEMENT-KONFIGURATIONEN (sortiert nach OOS-Rendite)")
    print("=" * 130)
    print(df.to_string(index=False))

    os.makedirs(RESULTS_DIR, exist_ok=True)
    df.to_csv(os.path.join(RESULTS_DIR, "capital_management_summary.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/capital_management_summary.csv")


if __name__ == "__main__":
    main()

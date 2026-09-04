"""
Abschliessende Zusammenfassung: Kapitalmanagement-Tuning Turtle Soup (Krypto)
================================================================================
Analog zu turtle_soup_stocks/experiment_capital_management_summary.py - siehe
dortigen Docstring. Grid: Allokation {10%,5%,3%} x Limit {8,15,unbegrenzt},
feste Basis Donchian 10/structural Stop/10-Tage-Zeit-Exit. Nur 2022-Stress
(kein 2020-Test moeglich, Krypto-Daten beginnen erst 2021-09). Sortiert nach
Out-of-Sample-Rendite absteigend.
"""

import os
import pandas as pd

from multi_symbol_optimise import load_all_symbol_data
from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO
from equity_simulation import collect_all_trades, simulate_portfolio, calculate_max_drawdown, \
    STARTING_CAPITAL, DONCHIAN_PERIOD, STOP_MODE
from pipeline_report import collect_trades_windowed
from strategy_paths import get_strategy_paths

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

ALLOCATION_PCTS = [0.10, 0.05, 0.03]
POSITION_LIMITS = [8, 15, None]

STRESS_PERIOD_2022 = ("2022-01-01", "2022-12-31")


def build_daily_capital_curve(equity_df: pd.DataFrame, starting_capital: float) -> pd.Series:
    df = equity_df.copy()
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time")
    df["date"] = df["time"].dt.normalize()
    daily_last = df.groupby("date")["capital_after"].last()
    full_range = pd.date_range(daily_last.index.min(), daily_last.index.max(), freq="D")
    daily_last = daily_last.reindex(full_range).ffill()
    if pd.isna(daily_last.iloc[0]):
        daily_last.iloc[0] = starting_capital
    return daily_last


def evaluate_window(curve: pd.Series, start: str, end: str) -> dict:
    window = curve[(curve.index >= start) & (curve.index <= end)]
    if window.empty:
        return {"rendite_pct": None, "max_dd_pct": None}
    running_max = window.cummax()
    dd = ((window - running_max) / running_max * 100).min()
    rendite = (window.iloc[-1] / window.iloc[0] - 1) * 100
    return {"rendite_pct": round(rendite, 2), "max_dd_pct": round(dd, 2)}


def evaluate_config(trades_full: pd.DataFrame, trades_oos: pd.DataFrame,
                     allocation_pct: float, limit) -> dict:
    result_full = simulate_portfolio(trades_full, STARTING_CAPITAL, allocation_pct, limit)
    full_return = round((result_full["final_capital"] / STARTING_CAPITAL - 1) * 100, 2)
    full_dd = calculate_max_drawdown(result_full["equity_curve"], STARTING_CAPITAL)

    result_oos = simulate_portfolio(trades_oos, STARTING_CAPITAL, allocation_pct, limit)
    oos_return = round((result_oos["final_capital"] / STARTING_CAPITAL - 1) * 100, 2)
    oos_dd = calculate_max_drawdown(result_oos["equity_curve"], STARTING_CAPITAL)

    curve_full = build_daily_capital_curve(result_full["equity_curve"], STARTING_CAPITAL)
    stress_2022 = evaluate_window(curve_full, *STRESS_PERIOD_2022)

    return {
        "allocation_pct": f"{allocation_pct*100:.0f}%",
        "limit": limit if limit is not None else "unbegrenzt",
        "oos_rendite_pct": oos_return, "oos_max_dd_pct": oos_dd,
        "gesamt_rendite_pct": full_return, "gesamt_max_dd_pct": full_dd,
        "2022_rendite_pct": stress_2022["rendite_pct"], "2022_max_dd_pct": stress_2022["max_dd_pct"],
    }


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)
    trades_full = collect_all_trades(all_data, DONCHIAN_PERIOD, STOP_MODE)
    trades_oos = collect_trades_windowed(test_data, DONCHIAN_PERIOD, STOP_MODE)

    rows = []
    for allocation_pct in ALLOCATION_PCTS:
        for limit in POSITION_LIMITS:
            rows.append(evaluate_config(trades_full, trades_oos, allocation_pct, limit))

    df = pd.DataFrame(rows).sort_values("oos_rendite_pct", ascending=False).reset_index(drop=True)

    print("=" * 120)
    print("KAPITALMANAGEMENT-TUNING TURTLE SOUP (KRYPTO) - GESAMTUEBERSICHT, SORTIERT NACH OOS-RENDITE")
    print("Basis: Donchian 10, structural Stop, 10-Tage-Zeit-Exit")
    print("=" * 120)
    print(df.to_string(index=False))

    os.makedirs(RESULTS_DIR, exist_ok=True)
    df.to_csv(os.path.join(RESULTS_DIR, "experiment_capital_management_summary.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_capital_management_summary.csv")

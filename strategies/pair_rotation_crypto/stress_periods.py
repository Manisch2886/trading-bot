"""
Stress-Perioden-Vergleich: 2022-Krypto-Winter UND 2020-COVID-Crash
================================================================================
Analog zu pair_rotation_stocks/stress_periods.py.
"""

import os
import pandas as pd

from multi_pair_optimise import load_all_symbol_data, get_reference_date, build_pairs
from equity_simulation import collect_all_trades, simulate_portfolio, \
    STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS, LOOKBACK_DAYS, REBALANCE_DAYS, STOP_LOSS_PCT
from strategy_paths import get_strategy_paths

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

STRESS_PERIODS = {
    "2022-Krypto-Winter": ("2022-01-01", "2022-12-31"),
    "2020-COVID-Crash": ("2020-02-01", "2020-04-30"),
}


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
    return {"rendite_pct": round(rendite, 2), "max_dd_pct": round(dd, 2),
            "fenster_start": window.index.min().date(), "fenster_ende": window.index.max().date()}


if __name__ == "__main__":
    symbol_data = load_all_symbol_data()
    reference_date = get_reference_date(symbol_data)
    pairs = build_pairs(symbol_data, reference_date)

    trades = collect_all_trades(pairs, LOOKBACK_DAYS, REBALANCE_DAYS, STOP_LOSS_PCT, reference_date)
    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)
    curve = build_daily_capital_curve(result["equity_curve"], STARTING_CAPITAL)

    running_max_all = curve.cummax()
    allzeit_max_dd = ((curve - running_max_all) / running_max_all * 100).min()

    rows = []
    for label, (start, end) in STRESS_PERIODS.items():
        stats = evaluate_window(curve, start, end)
        rows.append({"periode": label, **stats, "allzeit_max_dd_pct": round(allzeit_max_dd, 2)})

    df = pd.DataFrame(rows)
    print("=" * 90)
    print("STRESS-PERIODEN-VERGLEICH: Pair-Rotation (Krypto)")
    print("=" * 90)
    print(df.to_string(index=False))
    print(f"\nHinweis: Datenfenster beginnt erst {reference_date.date()} (siehe get_reference_date) - "
          f"deckt daher NICHT den fruehesten Teil des 2020-COVID-Crashs oder von Anfang 2022 ab, falls "
          f"das Referenzdatum spaeter liegt.")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    df.to_csv(os.path.join(RESULTS_DIR, "stress_periods.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/stress_periods.csv")

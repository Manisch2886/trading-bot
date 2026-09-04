"""
Stress-Perioden-Vergleich: 2022-Krypto-Winter (Turtle Soup vs. Volatility Breakout)
================================================================================================
Analog zu turtle_soup_stocks/stress_periods.py. NUR 2022 (kein 2020-COVID-
Test - Krypto-Tagesdaten beginnen erst 2021-09, wie bei allen Krypto-
Prototypen dieses Projekts, siehe rsi2_crypto/volatility_breakout_crypto
PROTOTYPE_FINDINGS.md).
"""

import os
import subprocess
import sys
import pandas as pd

from multi_symbol_optimise import load_all_symbol_data
from equity_simulation import collect_all_trades, simulate_portfolio, \
    STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS, DONCHIAN_PERIOD, STOP_MODE
from strategy_paths import get_strategy_paths

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_VB_DIR = os.path.join(os.path.dirname(_STRATEGY_DIR), "volatility_breakout_crypto")

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

STRESS_PERIOD_START = "2022-01-01"
STRESS_PERIOD_END = "2022-12-31"


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


def get_vb_curve_via_subprocess() -> pd.Series:
    tmp_csv = os.path.join(RESULTS_DIR, "_vb_equity_curve_cache.csv")
    script = f"""
import sys
sys.path.insert(0, {_VB_DIR!r})
from multi_symbol_optimise import load_all_symbol_data
from equity_simulation import collect_all_trades, simulate_portfolio, \
    STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS, STOP_LOSS_PCT
all_data = load_all_symbol_data()
trades = collect_all_trades(all_data, STOP_LOSS_PCT)
result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)
result["equity_curve"].to_csv({tmp_csv!r}, index=False)
"""
    result = subprocess.run([sys.executable, "-c", script], cwd=_VB_DIR, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Volatility-Breakout-Subprozess fehlgeschlagen:\n{result.stderr}")
    equity_df = pd.read_csv(tmp_csv, parse_dates=["time"])
    os.remove(tmp_csv)
    return build_daily_capital_curve(equity_df, 10_000.0)


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    trades = collect_all_trades(all_data, DONCHIAN_PERIOD, STOP_MODE)
    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)
    ts_curve = build_daily_capital_curve(result["equity_curve"], STARTING_CAPITAL)

    print("Erzeuge Volatility-Breakout-Krypto-Vergleichskurve (eigener Subprozess)...")
    vb_curve = get_vb_curve_via_subprocess()
    print()

    ts_running_max = ts_curve.cummax()
    ts_allzeit_dd = ((ts_curve - ts_running_max) / ts_running_max * 100).min()

    ts_stats = evaluate_window(ts_curve, STRESS_PERIOD_START, STRESS_PERIOD_END)
    vb_stats = evaluate_window(vb_curve, STRESS_PERIOD_START, STRESS_PERIOD_END)

    df = pd.DataFrame([{
        "periode": "2022-Krypto-Winter",
        "turtle_soup_rendite_pct": ts_stats["rendite_pct"], "turtle_soup_max_dd_pct": ts_stats["max_dd_pct"],
        "vol_breakout_rendite_pct": vb_stats["rendite_pct"], "vol_breakout_max_dd_pct": vb_stats["max_dd_pct"],
    }])

    print("=" * 100)
    print("STRESS-PERIODEN-VERGLEICH: Turtle Soup vs. Volatility Breakout (Krypto)")
    print("=" * 100)
    print(df.to_string(index=False))
    print(f"\nTurtle Soup Allzeit-Max-Drawdown (gesamte Historie): {ts_allzeit_dd:.2f}%")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    df.to_csv(os.path.join(RESULTS_DIR, "stress_periods_vs_volatility_breakout.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/stress_periods_vs_volatility_breakout.csv")

"""
Stress-Perioden-Vergleich: 2022-Baerenmarkt UND 2020-COVID-Crash
================================================================================
Von Anfang an mitgedacht: wertet die validierte Basiskonfiguration in
beiden Stress-Fenstern aus UND stellt direkt gegenueber, wie Volatility
Breakout im selben Fenster abschneidet (Kern der Diversifikationsthese,
siehe experiment_volatility_breakout_overlap.py) - besonders wichtig fuer
2022, da Volatility Breakout dort seine dokumentierte Haupt-Schwaeche zeigt
(siehe results/volatility_breakout/PROTOTYPE_FINDINGS.md Abschnitt 10).
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
_VB_DIR = os.path.join(os.path.dirname(_STRATEGY_DIR), "volatility_breakout")

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

STRESS_PERIODS = {
    "2022-Baerenmarkt": ("2022-01-01", "2022-12-31"),
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
    return {"rendite_pct": round(rendite, 2), "max_dd_pct": round(dd, 2)}


def get_vb_curve_via_subprocess() -> pd.Series:
    """Erzeugt die Volatility-Breakout-Kapitalkurve in einem eigenen
    Subprozess (siehe experiment_volatility_breakout_overlap.py-Docstring
    zur Modul-Namenskollision) und liest sie zurueck."""
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

    print("Erzeuge Volatility-Breakout-Vergleichskurve (eigener Subprozess)...")
    vb_curve = get_vb_curve_via_subprocess()
    print()

    ts_running_max = ts_curve.cummax()
    ts_allzeit_dd = ((ts_curve - ts_running_max) / ts_running_max * 100).min()

    rows = []
    for label, (start, end) in STRESS_PERIODS.items():
        ts_stats = evaluate_window(ts_curve, start, end)
        vb_stats = evaluate_window(vb_curve, start, end)
        rows.append({
            "periode": label,
            "turtle_soup_rendite_pct": ts_stats["rendite_pct"], "turtle_soup_max_dd_pct": ts_stats["max_dd_pct"],
            "vol_breakout_rendite_pct": vb_stats["rendite_pct"], "vol_breakout_max_dd_pct": vb_stats["max_dd_pct"],
        })

    df = pd.DataFrame(rows)
    print("=" * 100)
    print("STRESS-PERIODEN-VERGLEICH: Turtle Soup vs. Volatility Breakout (Aktien)")
    print("=" * 100)
    print(df.to_string(index=False))
    print(f"\nTurtle Soup Allzeit-Max-Drawdown (gesamte Historie): {ts_allzeit_dd:.2f}%")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    df.to_csv(os.path.join(RESULTS_DIR, "stress_periods_vs_volatility_breakout.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/stress_periods_vs_volatility_breakout.csv")

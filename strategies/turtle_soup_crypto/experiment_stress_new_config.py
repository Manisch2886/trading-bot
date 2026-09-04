"""
Aufgabe 3 - Stress-Periode unter (getesteter, aber NICHT uebernommener)
alternativer Kapitalmanagement-Konfiguration (Krypto)
================================================================================
Anders als bei Aktien fand experiment_position_size_limit.py fuer Krypto
KEINE Kombination, die die Basiskonfiguration (Limit 8, 10% Allokation)
im Gesamtzeitraum schlaegt - jede Lockerung (kleinere Allokation und/oder
hoeheres Limit) verschlechtert sowohl Rendite als auch Max Drawdown. Die
einzige nahe Alternative (Limit 15/unbegrenzt bei weiterhin 10% Allokation)
zeigt Out-of-Sample einen leichten Renditevorteil bei nahezu gleichem
Drawdown, faellt aber im Gesamtzeitraum klar ab (+165,97% statt +177,59%,
DD -36,02% statt -32,40%).

Dieses Skript testet zur Vollstaendigkeit trotzdem, ob sich das
2022-Schwaechebild dieser nahen Alternative (Limit 15, 10% Allokation)
gegenueber der Basiskonfiguration veraendert - als zusaetzliche
Absicherung der Entscheidung, die Basiskonfiguration NICHT zu aendern.
"""

import os
import subprocess
import sys
import pandas as pd

from multi_symbol_optimise import load_all_symbol_data
from equity_simulation import collect_all_trades, simulate_portfolio, \
    STARTING_CAPITAL, DONCHIAN_PERIOD, STOP_MODE
from strategy_paths import get_strategy_paths

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_VB_DIR = os.path.join(os.path.dirname(_STRATEGY_DIR), "volatility_breakout_crypto")

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

STRESS_PERIOD_START = "2022-01-01"
STRESS_PERIOD_END = "2022-12-31"

BASELINE_ALLOCATION_PCT = 0.10
BASELINE_LIMIT = 8

ALT_ALLOCATION_PCT = 0.10
ALT_LIMIT = 15  # naechstbeste, aber im Gesamtzeitraum unterlegene Alternative


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

    result_baseline = simulate_portfolio(trades, STARTING_CAPITAL, BASELINE_ALLOCATION_PCT, BASELINE_LIMIT)
    baseline_curve = build_daily_capital_curve(result_baseline["equity_curve"], STARTING_CAPITAL)

    result_alt = simulate_portfolio(trades, STARTING_CAPITAL, ALT_ALLOCATION_PCT, ALT_LIMIT)
    alt_curve = build_daily_capital_curve(result_alt["equity_curve"], STARTING_CAPITAL)

    print("Erzeuge Volatility-Breakout-Krypto-Vergleichskurve (eigener Subprozess)...")
    vb_curve = get_vb_curve_via_subprocess()
    print()

    baseline_stats = evaluate_window(baseline_curve, STRESS_PERIOD_START, STRESS_PERIOD_END)
    alt_stats = evaluate_window(alt_curve, STRESS_PERIOD_START, STRESS_PERIOD_END)
    vb_stats = evaluate_window(vb_curve, STRESS_PERIOD_START, STRESS_PERIOD_END)

    df = pd.DataFrame([{
        "periode": "2022-Krypto-Winter",
        "ts_baseline_rendite_pct": baseline_stats["rendite_pct"], "ts_baseline_max_dd_pct": baseline_stats["max_dd_pct"],
        "ts_alt_limit15_rendite_pct": alt_stats["rendite_pct"], "ts_alt_limit15_max_dd_pct": alt_stats["max_dd_pct"],
        "vol_breakout_rendite_pct": vb_stats["rendite_pct"], "vol_breakout_max_dd_pct": vb_stats["max_dd_pct"],
    }])

    print("=" * 110)
    print("STRESS-PERIODE 2022: Basis (Limit 8) vs. Alternative (Limit 15) vs. Volatility Breakout (Krypto)")
    print("=" * 110)
    print(df.to_string(index=False))

    os.makedirs(RESULTS_DIR, exist_ok=True)
    df.to_csv(os.path.join(RESULTS_DIR, "experiment_stress_new_config.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_stress_new_config.csv")

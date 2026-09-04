"""
Aufgabe 3 - Stress-Perioden unter neuer Kapitalmanagement-Konfiguration (Aktien)
================================================================================
Testet die in experiment_position_size_limit.py gefundene beste Kombination
(2% Allokation, unbegrenztes Positionslimit - siehe dortige Ergebnisse:
Gesamtzeitraum-Rendite steigt von +133,01% auf +145,59% bei GLEICHZEITIG
niedrigerem Max Drawdown, -29,91% statt -32,54%) in beiden Stress-Perioden
und stellt sie der bisherigen Basiskonfiguration (Limit 8, 10% Allokation)
UND Volatility Breakout direkt gegenueber (Fortsetzung der Diversifikations-
analyse aus stress_periods.py).

Erwartung laut Anfrage (Praezedenzfall Volatility Breakout): das bekannte
Schwachstellenprofil (2022 gemeinsam mit Vol. Breakout schwach; 2020
eigenstaendig schwach, da Turtle Soup in einem echten Crash systematisch
in fallende Kurse kauft) sollte strukturell UNVERAENDERT bleiben, da die
Schwaeche in der Signalqualitaet liegt, nicht im Kapitalmanagement.
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
_VB_DIR = os.path.join(os.path.dirname(_STRATEGY_DIR), "volatility_breakout")

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

STRESS_PERIODS = {
    "2022-Baerenmarkt": ("2022-01-01", "2022-12-31"),
    "2020-COVID-Crash": ("2020-02-01", "2020-04-30"),
}

BASELINE_ALLOCATION_PCT = 0.10
BASELINE_LIMIT = 8

NEW_ALLOCATION_PCT = 0.02
NEW_LIMIT = None  # unbegrenzt - beste gefundene Kombination


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

    result_new = simulate_portfolio(trades, STARTING_CAPITAL, NEW_ALLOCATION_PCT, NEW_LIMIT)
    new_curve = build_daily_capital_curve(result_new["equity_curve"], STARTING_CAPITAL)

    print("Erzeuge Volatility-Breakout-Vergleichskurve (eigener Subprozess)...")
    vb_curve = get_vb_curve_via_subprocess()
    print()

    baseline_allzeit_dd = ((baseline_curve - baseline_curve.cummax()) / baseline_curve.cummax() * 100).min()
    new_allzeit_dd = ((new_curve - new_curve.cummax()) / new_curve.cummax() * 100).min()

    rows = []
    for label, (start, end) in STRESS_PERIODS.items():
        baseline_stats = evaluate_window(baseline_curve, start, end)
        new_stats = evaluate_window(new_curve, start, end)
        vb_stats = evaluate_window(vb_curve, start, end)
        rows.append({
            "periode": label,
            "ts_baseline_rendite_pct": baseline_stats["rendite_pct"], "ts_baseline_max_dd_pct": baseline_stats["max_dd_pct"],
            "ts_neu_2pct_unbegrenzt_rendite_pct": new_stats["rendite_pct"], "ts_neu_2pct_unbegrenzt_max_dd_pct": new_stats["max_dd_pct"],
            "vol_breakout_rendite_pct": vb_stats["rendite_pct"], "vol_breakout_max_dd_pct": vb_stats["max_dd_pct"],
        })

    df = pd.DataFrame(rows)
    print("=" * 110)
    print("STRESS-PERIODEN UNTER NEUER KAPITALMANAGEMENT-KONFIGURATION (Aktien)")
    print("Basis (Limit 8, 10% Allokation) vs. Neu (Limit unbegrenzt, 2% Allokation) vs. Volatility Breakout")
    print("=" * 110)
    print(df.to_string(index=False))
    print(f"\nTurtle Soup Basis - Allzeit-Max-Drawdown (gesamte Historie): {baseline_allzeit_dd:.2f}%")
    print(f"Turtle Soup Neu   - Allzeit-Max-Drawdown (gesamte Historie): {new_allzeit_dd:.2f}%")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    df.to_csv(os.path.join(RESULTS_DIR, "experiment_stress_new_config.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_stress_new_config.csv")

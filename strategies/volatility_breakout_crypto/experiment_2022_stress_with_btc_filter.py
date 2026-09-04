"""
Aufgabe 3: 2022-Krypto-Winter MIT BTC-Regime-Filter
================================================================================
Rechnet die 2022-Stress-Periode fuer Volatility Breakout Krypto MIT
aktivem BTC-Regime-Filter durch und vergleicht mit dem bekannten
Basis-Ergebnis OHNE Filter (siehe
results/volatility_breakout_crypto/PROTOTYPE_FINDINGS.md Abschnitt 7:
-12,35% Rendite, -16,55% Max Drawdown, nahe am Allzeit-Maximum von
-16,77%). Leitfrage: mildert der Filter die bereits als strategie-
inhaerent identifizierte Baerenmarkt-Schwaeche spuerbar, oder bleibt sie
strukturell bestehen (analog zum Kapitalmanagement-Befund bei der
Aktien-Version, wo Positionsgroesse die 2022-Schwaeche nicht beheben konnte)?
"""

import os
import pandas as pd

from multi_symbol_optimise import load_all_symbol_data, DATA_DIR
from equity_simulation import collect_all_trades, simulate_portfolio, \
    STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS, STOP_LOSS_PCT
from regime_filter import compute_btc_regime, filter_trades_by_regime

BASE_DIR = "/home/user/trading-bot"
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


def evaluate_2022(curve: pd.Series) -> dict:
    stress_start = pd.Timestamp(STRESS_PERIOD_START)
    stress_end = pd.Timestamp(STRESS_PERIOD_END)
    window = curve[(curve.index >= stress_start) & (curve.index <= stress_end)]
    if window.empty:
        return {"rendite_2022_pct": None, "max_dd_2022_pct": None}
    running_max = window.cummax()
    dd = ((window - running_max) / running_max * 100).min()
    rendite = (window.iloc[-1] / window.iloc[0] - 1) * 100

    running_max_all = curve.cummax()
    dd_all_time = ((curve - running_max_all) / running_max_all * 100).min()
    return {
        "rendite_2022_pct": round(rendite, 2), "max_dd_2022_pct": round(dd, 2),
        "allzeit_max_dd_pct": round(dd_all_time, 2),
        "fenster_start": window.index.min().date(), "fenster_ende": window.index.max().date(),
    }


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    btc_df = pd.read_csv(os.path.join(DATA_DIR, "BTCUSDT_1d.csv"), parse_dates=["open_time"])
    btc_regime = compute_btc_regime(btc_df)

    trades_no_filter = collect_all_trades(all_data, STOP_LOSS_PCT)
    trades_with_filter = filter_trades_by_regime(trades_no_filter, btc_regime)

    result_no_filter = simulate_portfolio(trades_no_filter, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)
    result_with_filter = simulate_portfolio(trades_with_filter, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)

    curve_no_filter = build_daily_capital_curve(result_no_filter["equity_curve"], STARTING_CAPITAL)
    curve_with_filter = build_daily_capital_curve(result_with_filter["equity_curve"], STARTING_CAPITAL)

    stats_no_filter = evaluate_2022(curve_no_filter)
    stats_with_filter = evaluate_2022(curve_with_filter)

    print("=" * 90)
    print(f"2022-STRESS-PERIODE ({STRESS_PERIOD_START} bis {STRESS_PERIOD_END}) - MIT vs. OHNE BTC-Regime-Filter")
    print("=" * 90)
    df = pd.DataFrame([
        {"variante": "Ohne BTC-Regime-Filter (Basis-Regel)", **stats_no_filter},
        {"variante": "Mit BTC-Regime-Filter", **stats_with_filter},
    ])
    print(df.to_string(index=False))

    # Zusaetzlich: wie viele der im 2022-Fenster ausgefuehrten Trades wurden
    # durch den Filter herausgefiltert (Signale, die ohne Filter durchgegangen
    # waeren)?
    eq_no_filter = result_no_filter["equity_curve"].copy()
    eq_no_filter["time"] = pd.to_datetime(eq_no_filter["time"])
    exits_2022_no_filter = eq_no_filter[
        (eq_no_filter["time"] >= STRESS_PERIOD_START) & (eq_no_filter["time"] <= STRESS_PERIOD_END)]

    eq_with_filter = result_with_filter["equity_curve"].copy()
    eq_with_filter["time"] = pd.to_datetime(eq_with_filter["time"])
    exits_2022_with_filter = eq_with_filter[
        (eq_with_filter["time"] >= STRESS_PERIOD_START) & (eq_with_filter["time"] <= STRESS_PERIOD_END)]

    print(f"\nAusgefuehrte Positions-Exits im 2022-Fenster: "
          f"{len(exits_2022_no_filter)} ohne Filter -> {len(exits_2022_with_filter)} mit Filter "
          f"({len(exits_2022_no_filter) - len(exits_2022_with_filter)} durch den Filter vermieden)")
    if not exits_2022_no_filter.empty:
        print(f"Negativer-PnL-Anteil ohne Filter: {(exits_2022_no_filter['pnl_pct']<0).mean()*100:.1f}%")
    if not exits_2022_with_filter.empty:
        print(f"Negativer-PnL-Anteil mit Filter:  {(exits_2022_with_filter['pnl_pct']<0).mean()*100:.1f}%")

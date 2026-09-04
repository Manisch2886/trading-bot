"""
Phase 1 - Multi-Symbol-Optimierung: Turtle Soup (Aktien)
==========================================================================
Analog zu rsi2_mean_reversion/multi_symbol_optimise.py: testet
DONCHIAN_PERIOD (Setup-Fenster) und STOP_MODE (kein Stop / strukturell /
fester Prozentsatz) gegeneinander. MAX_HOLD_DAYS bleibt fest bei 10
(Startwert wie angefragt, nicht Teil des Grids - konsistent mit der
Vorgehensweise bei den anderen Bots, wo nicht jeder Parameter
mitoptimiert wird).

Nutzt dasselbe Universum wie die anderen Aktien-Bots (S&P-500 Top 150,
config/sp500_top150.txt).
"""

import os
import sys
import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
DATA_DIR = _P["DATA_DIR"]
RESULTS_DIR = _P["RESULTS_DIR"]

from backtest_turtle_soup import compute_indicators, run_backtest, MAX_HOLD_DAYS
from stocks_symbols_config import SYMBOLS

INTERVAL = "1d"

DONCHIAN_PERIOD_RANGE = [10, 20, 40]
STOP_MODE_RANGE = [None, "structural", 5.0, 8.0]

MIN_TRADES = 150
MIN_AVG_RETURN_PCT = 0.0
MIN_SYMBOLS_CONTRIBUTING = 22
MIN_HISTORY_DAYS = 1825
RECENT_YEARS_ONLY = 10


def load_all_symbol_data() -> dict:
    data = {}
    for symbol in SYMBOLS:
        csv_path = os.path.join(DATA_DIR, f"{symbol}_{INTERVAL}.csv")
        try:
            df = pd.read_csv(csv_path, parse_dates=["open_time"])
        except FileNotFoundError:
            continue
        if df.empty:
            continue
        timespan_days = (df["open_time"].max() - df["open_time"].min()).days
        if timespan_days < MIN_HISTORY_DAYS:
            continue

        entry_cutoff = None
        if RECENT_YEARS_ONLY is not None:
            entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)

        data[symbol] = (df, entry_cutoff)
    return data


def get_trades_for_symbol(price_df: pd.DataFrame, entry_cutoff, donchian_period: int,
                           stop_mode=None) -> pd.DataFrame:
    df_ind = compute_indicators(price_df, donchian_period)
    return run_backtest(df_ind, stop_mode=stop_mode, entry_cutoff=entry_cutoff, donchian_period=donchian_period)


def calculate_robustness_score(row: dict) -> float:
    drawdown_penalty = abs(row["max_drawdown_pct"]) if row["max_drawdown_pct"] != 0 else 1.0
    return round((row["avg_return_pct"] * (row["num_trades"] ** 0.5)) / drawdown_penalty, 3)


def evaluate_combination_multi(all_data: dict, donchian_period: int, stop_mode=None) -> dict:
    all_trades = []
    contributing_symbols = 0
    for symbol, (df, entry_cutoff) in all_data.items():
        trades = get_trades_for_symbol(df, entry_cutoff, donchian_period, stop_mode)
        if not trades.empty:
            contributing_symbols += 1
            all_trades.append(trades)

    if not all_trades:
        return None
    combined = pd.concat(all_trades, ignore_index=True)
    if len(combined) < MIN_TRADES or contributing_symbols < MIN_SYMBOLS_CONTRIBUTING:
        return None

    win_rate = (combined["pnl_pct"] > 0).mean() * 100
    avg_return = combined["pnl_pct"].mean()
    if avg_return < MIN_AVG_RETURN_PCT:
        return None

    total_return = combined["pnl_pct"].sum()
    cum_returns = combined["pnl_pct"].cumsum()
    max_drawdown = (cum_returns - cum_returns.cummax()).min()

    result = {
        "donchian_period": donchian_period,
        "stop_mode": stop_mode if stop_mode is not None else "kein Stop",
        "num_trades": len(combined), "num_symbols": contributing_symbols,
        "win_rate": round(win_rate, 1), "total_return_pct": round(total_return, 2),
        "avg_return_pct": round(avg_return, 2),
        "avg_holding_days": round(combined["holding_days"].mean(), 1),
        "max_drawdown_pct": round(max_drawdown, 2),
    }
    result["robustness_score"] = calculate_robustness_score(result)
    return result


def run_multi_optimisation(all_data: dict) -> pd.DataFrame:
    results = []
    for donchian_period in DONCHIAN_PERIOD_RANGE:
        for stop_mode in STOP_MODE_RANGE:
            result = evaluate_combination_multi(all_data, donchian_period, stop_mode)
            if result is not None:
                results.append(result)
    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values("robustness_score", ascending=False).reset_index(drop=True)
    return df


if __name__ == "__main__":
    print(f"Lade Kursdaten fuer {len(SYMBOLS)} Aktien...\n")
    all_data = load_all_symbol_data()
    print(f"{len(all_data)} Symbole mit ausreichender Historie geladen.\n")

    results_df = run_multi_optimisation(all_data)
    if results_df.empty:
        print("Keine Kombination erfuellt die Mindestkriterien.")
    else:
        print(results_df.to_string(index=False))
        os.makedirs(RESULTS_DIR, exist_ok=True)
        results_df.to_csv(os.path.join(RESULTS_DIR, "multi_symbol_optimisation_results.csv"), index=False)
        print(f"\nGespeichert unter: {RESULTS_DIR}/multi_symbol_optimisation_results.csv")

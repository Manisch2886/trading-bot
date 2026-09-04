"""
Phase 1 - Multi-Pair-Optimierung: Relative-Strength-Pair-Rotation (Aktien)
================================================================================
Analog zum Muster der bestehenden Aktien-Bots: fuehrt die Backtest-Pipeline
fuer jede Parameter-Kombination auf ALLEN entdeckten Paaren aus und fasst
die Trades zusammen. Testet LOOKBACK_DAYS (Rotations-Signal-Fenster),
REBALANCE_DAYS (taeglich vs. woechentlich) und STOP_LOSS_RANGE (kein Stop
vs. feste Werte) - alle drei empirisch, keine Annahme vorab.

Nutzt dasselbe Universum wie die anderen Aktien-Bots (S&P-500 Top 150,
config/sp500_top150.txt), Paar-Auswahl siehe pair_discovery.py.
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

from backtest_pair_rotation import compute_pair_indicators, run_backtest, WARMUP_PERIOD
from pair_discovery import discover_pairs
from stocks_symbols_config import SYMBOLS

INTERVAL = "1d"

LOOKBACK_DAYS_RANGE = [20, 60, 120]   # kurz/mittel/lang - uebliche Momentum-Fenster-Alternativen
REBALANCE_DAYS_RANGE = [1, 5]          # taeglich vs. woechentlich (5 Handelstage)
STOP_LOSS_RANGE = [None, 8.0, 12.0]    # weiter als RSI-2/Vol-Breakout, da Rotationstrades
                                        # tendenziell laenger laufen (kein Zeit-Exit)

MIN_TRADES = 80
MIN_AVG_RETURN_PCT = 0.0
MIN_PAIRS_CONTRIBUTING = 6
MIN_HISTORY_DAYS = 1825       # ca. 5 Jahre
RECENT_YEARS_ONLY = 10        # reduziert Survivorship Bias, wie bei den anderen Aktien-Bots


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
        data[symbol] = df
    return data


def get_reference_date(symbol_data: dict) -> pd.Timestamp:
    """Einheitlicher Auswertungsfenster-Beginn (entry_cutoff) fuer alle
    Paare - Basis sowohl fuer die Paar-Auswahl (nur Daten VOR diesem Datum,
    kein Lookahead) als auch fuer die RECENT_YEARS_ONLY-Kappung der Trades."""
    max_date = max(df["open_time"].max() for df in symbol_data.values())
    return max_date - pd.DateOffset(years=RECENT_YEARS_ONLY)


def build_pairs(symbol_data: dict, reference_date: pd.Timestamp) -> list:
    """Gibt eine Liste von (symbol_a, symbol_b, correlation, merged_pair_df) zurueck."""
    candidates = discover_pairs(symbol_data, reference_date)
    pairs = []
    for symbol_a, symbol_b, corr in candidates:
        pair_df_raw = compute_pair_indicators(symbol_data[symbol_a], symbol_data[symbol_b], lookback_days=1)
        pairs.append((symbol_a, symbol_b, corr, pair_df_raw[["open_time", "close_a", "low_a", "close_b", "low_b"]]))
    return pairs


def get_trades_for_pair(pair_base_df: pd.DataFrame, symbol_a: str, symbol_b: str, lookback_days: int,
                         rebalance_days: int, stop_loss_pct: float = None, entry_cutoff=None,
                         use_decoupling_protection: bool = True) -> pd.DataFrame:
    from indicators import relative_strength, rolling_correlation
    df = pair_base_df.copy()
    df["rel_strength"] = relative_strength(df["close_a"], df["close_b"], lookback_days)
    df["correlation"] = rolling_correlation(df["close_a"], df["close_b"])
    return run_backtest(df, symbol_a, symbol_b, lookback_days, rebalance_days,
                         stop_loss_pct, entry_cutoff, use_decoupling_protection)


def calculate_robustness_score(row: dict) -> float:
    drawdown_penalty = abs(row["max_drawdown_pct"]) if row["max_drawdown_pct"] != 0 else 1.0
    return round((row["avg_return_pct"] * (row["num_trades"] ** 0.5)) / drawdown_penalty, 3)


def evaluate_combination_multi(pairs: list, lookback_days: int, rebalance_days: int,
                                stop_loss_pct: float = None, entry_cutoff=None) -> dict:
    all_trades = []
    contributing_pairs = 0
    for symbol_a, symbol_b, corr, pair_base_df in pairs:
        trades = get_trades_for_pair(pair_base_df, symbol_a, symbol_b, lookback_days,
                                      rebalance_days, stop_loss_pct, entry_cutoff)
        if not trades.empty:
            contributing_pairs += 1
            all_trades.append(trades)

    if not all_trades:
        return None
    combined = pd.concat(all_trades, ignore_index=True)
    if len(combined) < MIN_TRADES or contributing_pairs < MIN_PAIRS_CONTRIBUTING:
        return None

    win_rate = (combined["pnl_pct"] > 0).mean() * 100
    avg_return = combined["pnl_pct"].mean()
    if avg_return < MIN_AVG_RETURN_PCT:
        return None

    total_return = combined["pnl_pct"].sum()
    cum_returns = combined["pnl_pct"].cumsum()
    max_drawdown = (cum_returns - cum_returns.cummax()).min()

    result = {
        "lookback_days": lookback_days, "rebalance_days": rebalance_days,
        "stop_loss_pct": stop_loss_pct if stop_loss_pct is not None else "kein Stop",
        "num_trades": len(combined), "num_pairs": contributing_pairs,
        "win_rate": round(win_rate, 1), "total_return_pct": round(total_return, 2),
        "avg_return_pct": round(avg_return, 2),
        "avg_holding_days": round(combined["holding_days"].mean(), 1),
        "max_drawdown_pct": round(max_drawdown, 2),
    }
    result["robustness_score"] = calculate_robustness_score(result)
    return result


def run_multi_optimisation(pairs: list, entry_cutoff=None) -> pd.DataFrame:
    results = []
    for lookback_days in LOOKBACK_DAYS_RANGE:
        for rebalance_days in REBALANCE_DAYS_RANGE:
            for stop_loss_pct in STOP_LOSS_RANGE:
                result = evaluate_combination_multi(pairs, lookback_days, rebalance_days,
                                                     stop_loss_pct, entry_cutoff)
                if result is not None:
                    results.append(result)
    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values("robustness_score", ascending=False).reset_index(drop=True)
    return df


if __name__ == "__main__":
    print(f"Lade Kursdaten fuer {len(SYMBOLS)} Aktien...\n")
    symbol_data = load_all_symbol_data()
    print(f"{len(symbol_data)} Symbole mit ausreichender Historie geladen.\n")

    reference_date = get_reference_date(symbol_data)
    print(f"Auswertungsfenster beginnt: {reference_date.date()} (RECENT_YEARS_ONLY={RECENT_YEARS_ONLY})\n")

    pairs = build_pairs(symbol_data, reference_date)
    print(f"{len(pairs)} Paare mit Korrelation >= {__import__('pair_discovery').MIN_CORRELATION} entdeckt:")
    for symbol_a, symbol_b, corr, _ in pairs:
        print(f"  {symbol_a}/{symbol_b}: Korrelation {corr}")

    results_df = run_multi_optimisation(pairs, reference_date)
    if results_df.empty:
        print("\nKeine Kombination erfuellt die Mindestkriterien.")
    else:
        print("\n" + results_df.to_string(index=False))
        os.makedirs(RESULTS_DIR, exist_ok=True)
        results_df.to_csv(os.path.join(RESULTS_DIR, "multi_pair_optimisation_results.csv"), index=False)
        pd.DataFrame([{"symbol_a": a, "symbol_b": b, "correlation": c} for a, b, c, _ in pairs]) \
            .to_csv(os.path.join(RESULTS_DIR, "discovered_pairs.csv"), index=False)
        print(f"\nGespeichert unter: {RESULTS_DIR}/multi_pair_optimisation_results.csv")

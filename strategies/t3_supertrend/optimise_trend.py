"""
Parameter-Optimierung (Einzel-Symbol) - T3/ADX/SuperTrend-Strategie
=========================================================================
Testet Kombinationen aus T3-Laengen, ADX-Schwelle, SuperTrend-
Empfindlichkeit und Stop-Loss, analog zur Vorgehensweise bei der
Elliott-Wave-Strategie (optimise_elliott.py).
"""

import os
import sys
import pandas as pd
import itertools

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
DATA_DIR = _P["DATA_DIR"]
RESULTS_DIR = _P["RESULTS_DIR"]

from backtest_trend import run_backtest
import backtest_trend

# Zu testende Parameter-Bereiche
T3_FAST_RANGE = [8, 12, 16]
T3_SLOW_RANGE = [21, 25, 30]
ADX_THRESHOLD_RANGE = [20.0, 25.0, 30.0]
STOP_LOSS_RANGE = [2.0, 3.0, 4.0]

MIN_TRADES = 15
MIN_AVG_RETURN_PCT = 1.0  # Trendfolge hat tendenziell mehr, kleinere Trades als Elliott Wave


def calculate_robustness_score(row: dict) -> float:
    drawdown_penalty = abs(row["max_drawdown_pct"]) if row["max_drawdown_pct"] != 0 else 1.0
    return round((row["avg_return_pct"] * (row["num_trades"] ** 0.5)) / drawdown_penalty, 3)


def evaluate_combination(price_df: pd.DataFrame, t3_fast: int, t3_slow: int,
                          adx_threshold: float, stop_loss_pct: float) -> dict:
    if t3_fast >= t3_slow:
        return None  # Fast muss schneller als Slow sein, sonst ergibt der Crossover keinen Sinn

    trades = run_backtest(
        price_df,
        t3_fast_length=t3_fast,
        t3_slow_length=t3_slow,
        adx_threshold=adx_threshold,
        stop_loss_pct=stop_loss_pct,
    )

    if trades.empty or len(trades) < MIN_TRADES:
        return None

    win_rate = (trades["pnl_pct"] > 0).mean() * 100
    total_return = trades["pnl_pct"].sum()
    avg_return = trades["pnl_pct"].mean()

    if avg_return < MIN_AVG_RETURN_PCT:
        return None

    cum_returns = trades["pnl_pct"].cumsum()
    max_drawdown = (cum_returns - cum_returns.cummax()).min()

    result = {
        "t3_fast": t3_fast,
        "t3_slow": t3_slow,
        "adx_threshold": adx_threshold,
        "stop_loss_pct": stop_loss_pct,
        "num_trades": len(trades),
        "win_rate": round(win_rate, 1),
        "total_return_pct": round(total_return, 2),
        "avg_return_pct": round(avg_return, 2),
        "max_drawdown_pct": round(max_drawdown, 2),
    }
    result["robustness_score"] = calculate_robustness_score(result)
    return result


def run_optimisation(price_df: pd.DataFrame) -> pd.DataFrame:
    results = []
    combinations = list(itertools.product(T3_FAST_RANGE, T3_SLOW_RANGE, ADX_THRESHOLD_RANGE, STOP_LOSS_RANGE))

    print(f"Teste {len(combinations)} Parameter-Kombinationen...\n")

    for t3_fast, t3_slow, adx_threshold, stop_loss_pct in combinations:
        result = evaluate_combination(price_df, t3_fast, t3_slow, adx_threshold, stop_loss_pct)
        if result is not None:
            results.append(result)

    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values("robustness_score", ascending=False).reset_index(drop=True)
    return df


if __name__ == "__main__":
    price_df = pd.read_csv(os.path.join(DATA_DIR, "BTCUSDT_1h.csv"), parse_dates=["open_time"])

    results = run_optimisation(price_df)

    if results.empty:
        print("Keine Kombination erfuellte die Mindestanzahl an Trades",
              f"({MIN_TRADES}). MIN_TRADES senken oder mehr Historie laden.")
    else:
        print(f"{len(results)} robuste Kombinationen gefunden.\n")
        print(results.head(15).to_string(index=False))

        output_path = os.path.join(RESULTS_DIR, "BTCUSDT_optimisation_results.csv")
        results.to_csv(output_path, index=False)
        print(f"\nGespeichert als: {output_path}")

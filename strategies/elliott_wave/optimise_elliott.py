"""
Phase 3 - Parameter-Optimierung
=================================
Testet verschiedene Kombinationen aus:
- Zigzag-Schwelle (deviation_pct)  -> beeinflusst, wie Wellen erkannt werden
- Stop-Loss %
- Take-Profit Fibonacci-Level

...und fuehrt fuer jede Kombination den kompletten Ablauf durch
(Zigzag -> Wellenerkennung -> Bereinigung -> Backtest), um die
robusteste Parameter-Kombination zu finden.

Das ist die einfache, lokale Vorstufe zu einem "Optimisation Agent":
hier testet ein Grid-Search-Algorithmus alle Kombinationen erschoepfend.
Spaeter kann ein Claude-Agent diesen Prozess intelligenter steuern
(z.B. gezielt in vielversprechende Regionen nachtesten, statt stur
jede Kombination durchzurechnen).
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

from zigzag_indicator import calculate_zigzag
from elliott_wave_counter import find_impulse_waves, remove_overlapping
from backtest_elliott import run_backtest

# Zu testende Parameter-Bereiche
DEVIATION_RANGE = [2.0, 3.0, 4.0, 5.0]
STOP_LOSS_RANGE = [2.0, 3.0, 4.0]
TAKE_PROFIT_FIB_RANGE = [0.236, 0.382, 0.5]

MIN_TRADES = 10          # zu wenige Trades = statistisch nicht belastbar
MIN_AVG_RETURN_PCT = 2.0  # Trades mit zu kleinem Ø-Gewinn sind oft nur Rauschen


def calculate_robustness_score(row: dict) -> float:
    """
    Risikoadjustierter Score statt reinem Gesamtertrag:
    belohnt hohen Ø-Gewinn pro Trade und viele Trades (mehr Vertrauen),
    bestraft grossen Max Drawdown relativ zum Ertrag.
    """
    drawdown_penalty = abs(row["max_drawdown_pct"]) if row["max_drawdown_pct"] != 0 else 1.0
    return round((row["avg_return_pct"] * (row["num_trades"] ** 0.5)) / drawdown_penalty, 3)


def evaluate_combination(price_df: pd.DataFrame, deviation_pct: float,
                          stop_loss_pct: float, take_profit_fib: float) -> dict:
    """Fuehrt die komplette Pipeline fuer eine Parameter-Kombination aus."""
    import backtest_elliott
    backtest_elliott.STOP_LOSS_PCT = stop_loss_pct
    backtest_elliott.TAKE_PROFIT_FIB = take_profit_fib

    zigzag = calculate_zigzag(price_df, deviation_pct=deviation_pct)
    if len(zigzag) < 6:
        return None

    impulses = find_impulse_waves(zigzag, min_fib_score=0.3)
    if impulses.empty:
        return None
    impulses = remove_overlapping(impulses)

    # Long-only, wie zuvor festgelegt
    impulses = impulses[impulses["direction"] == "bearish"]
    if impulses.empty:
        return None

    trades = run_backtest(price_df, impulses)
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
        "deviation_pct": deviation_pct,
        "stop_loss_pct": stop_loss_pct,
        "take_profit_fib": take_profit_fib,
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
    combinations = list(itertools.product(DEVIATION_RANGE, STOP_LOSS_RANGE, TAKE_PROFIT_FIB_RANGE))

    print(f"Teste {len(combinations)} Parameter-Kombinationen...\n")

    for deviation_pct, stop_loss_pct, take_profit_fib in combinations:
        result = evaluate_combination(price_df, deviation_pct, stop_loss_pct, take_profit_fib)
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

        best = results.iloc[0]
        print(f"\nBeste Kombination:")
        print(f"  Zigzag-Schwelle:   {best['deviation_pct']}%")
        print(f"  Stop-Loss:         {best['stop_loss_pct']}%")
        print(f"  Take-Profit Fib:   {best['take_profit_fib']}")
        print(f"  -> {best['num_trades']} Trades, {best['win_rate']}% Win Rate, "
              f"{best['total_return_pct']}% Gesamtertrag")

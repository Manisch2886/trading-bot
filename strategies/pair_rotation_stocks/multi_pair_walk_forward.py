"""
Phase 2 - Multi-Pair Walk-Forward-Validierung: Pair-Rotation (Aktien)
================================================================================
Analog zum Muster der anderen Aktien-Bots: teilt das RECENT_YEARS_ONLY-
Auswertungsfenster zeitlich in In-Sample (erste 70%) und Out-of-Sample
(letzte 30%). Split-Punkt korrekt INNERHALB des Auswertungsfensters
berechnet (der bei RSI-2 gefundene und seitdem projektweit vermiedene
Bug), nicht auf der vollen Rohhistorie.

WICHTIG: die Paar-AUSWAHL selbst (siehe pair_discovery.py) bleibt fuer
In-Sample UND Out-of-Sample identisch (Korrelation vor Beginn des
GESAMTEN Auswertungsfensters berechnet, wie in multi_pair_optimise.py) -
nur die Trade-Generierung wird auf das jeweilige Teilfenster beschraenkt.
"""

import pandas as pd

from multi_pair_optimise import (
    load_all_symbol_data, get_reference_date, build_pairs, get_trades_for_pair,
    calculate_robustness_score, MIN_TRADES, MIN_PAIRS_CONTRIBUTING, MIN_AVG_RETURN_PCT,
    LOOKBACK_DAYS_RANGE, REBALANCE_DAYS_RANGE, STOP_LOSS_RANGE,
)

TRAIN_SPLIT_RATIO = 0.7


def split_window(reference_date: pd.Timestamp, symbol_data: dict, ratio: float) -> tuple:
    window_end = max(df["open_time"].max() for df in symbol_data.values())
    split_time = reference_date + (window_end - reference_date) * ratio
    return reference_date, split_time, window_end


def evaluate_combination_multi_windowed(pairs: list, lookback_days: int, rebalance_days: int,
                                         stop_loss_pct: float, cutoff_start, cutoff_end) -> dict:
    all_trades = []
    contributing_pairs = 0
    for symbol_a, symbol_b, corr, pair_base_df in pairs:
        trades = get_trades_for_pair(pair_base_df, symbol_a, symbol_b, lookback_days,
                                      rebalance_days, stop_loss_pct, cutoff_start)
        if cutoff_end is not None and not trades.empty:
            trades = trades[trades["entry_time"] < cutoff_end]
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


def run_multi_optimisation_windowed(pairs: list, cutoff_start, cutoff_end) -> pd.DataFrame:
    results = []
    for lookback_days in LOOKBACK_DAYS_RANGE:
        for rebalance_days in REBALANCE_DAYS_RANGE:
            for stop_loss_pct in STOP_LOSS_RANGE:
                result = evaluate_combination_multi_windowed(pairs, lookback_days, rebalance_days,
                                                               stop_loss_pct, cutoff_start, cutoff_end)
                if result is not None:
                    results.append(result)
    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values("robustness_score", ascending=False).reset_index(drop=True)
    return df


if __name__ == "__main__":
    symbol_data = load_all_symbol_data()
    reference_date = get_reference_date(symbol_data)
    window_start, split_time, window_end = split_window(reference_date, symbol_data, TRAIN_SPLIT_RATIO)
    print(f"In-Sample: {window_start.date()} bis {split_time.date()}")
    print(f"Out-of-Sample: {split_time.date()} bis {window_end.date()}\n")

    pairs = build_pairs(symbol_data, reference_date)
    print(f"{len(pairs)} Paare entdeckt (identisch fuer IS und OOS, siehe Docstring).\n")

    print("=" * 70)
    print("SCHRITT 1: Optimierung auf In-Sample-Daten")
    print("=" * 70)
    train_results = run_multi_optimisation_windowed(pairs, window_start, split_time)

    if train_results.empty:
        print("Keine robuste Kombination im Trainingszeitraum gefunden.")
        exit()

    best = train_results.iloc[0]
    print(f"\nBeste In-Sample-Kombination:")
    print(f"  Lookback: {best['lookback_days']}  |  Rebalance: {best['rebalance_days']} Tage  |  "
          f"Stop-Loss: {best['stop_loss_pct']}")
    print(f"  -> {best['num_trades']} Trades ueber {best['num_pairs']} Paare, "
          f"{best['win_rate']}% Win Rate, {best['total_return_pct']}% Summe, "
          f"Score: {best['robustness_score']}")

    print("\n" + "=" * 70)
    print("SCHRITT 2: Test auf Out-of-Sample-Daten (ungesehen)")
    print("=" * 70)
    stop_loss_val = None if best["stop_loss_pct"] == "kein Stop" else best["stop_loss_pct"]
    test_result = evaluate_combination_multi_windowed(pairs, int(best["lookback_days"]), int(best["rebalance_days"]),
                                                        stop_loss_val, split_time, None)

    if test_result is None:
        print("\nDiese Parameter erfuellen die Mindestkriterien im Out-of-Sample-Zeitraum nicht.")
    else:
        print(f"\nOut-of-Sample-Ergebnis:")
        print(f"  -> {test_result['num_trades']} Trades ueber {test_result['num_pairs']} Paare, "
              f"{test_result['win_rate']}% Win Rate, {test_result['total_return_pct']}% Summe, "
              f"Score: {test_result['robustness_score']}")

        print("\n" + "=" * 70)
        print("VERGLEICH")
        print("=" * 70)
        print(f"{'Metrik':<22}{'In-Sample':>15}{'Out-of-Sample':>18}")
        print(f"{'Win Rate':<22}{best['win_rate']:>14}%{test_result['win_rate']:>17}%")
        print(f"{'Ø Gewinn/Trade':<22}{best['avg_return_pct']:>14}%{test_result['avg_return_pct']:>17}%")
        print(f"{'Anzahl Trades':<22}{best['num_trades']:>15}{test_result['num_trades']:>18}")
        print(f"{'Robustheit-Score':<22}{best['robustness_score']:>15}{test_result['robustness_score']:>18}")

        score_change = (1 - test_result["robustness_score"] / best["robustness_score"]) * 100 if best["robustness_score"] else 0
        print(f"\nScore-Rueckgang Out-of-Sample: {score_change:.0f}%")

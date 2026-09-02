"""
Multi-Symbol Walk-Forward-Validierung - T3/ADX/SuperTrend-Strategie
=========================================================================
Analog zur Elliott-Wave-Version: Parameter werden nur auf den ersten
70% der Zeit (In-Sample) optimiert, dann auf den letzten 30%
(Out-of-Sample, ungesehen) unabhaengig getestet.
"""

import os
import sys
import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from multi_symbol_optimise import load_all_symbol_data, run_multi_optimisation, evaluate_combination_multi

TRAIN_SPLIT_RATIO = 0.7


def split_all_symbols(all_data: dict, ratio: float) -> tuple:
    train_data = {}
    test_data = {}
    for symbol, df in all_data.items():
        split_idx = int(len(df) * ratio)
        train_data[symbol] = df.iloc[:split_idx].reset_index(drop=True)
        test_data[symbol] = df.iloc[split_idx:].reset_index(drop=True)
    return train_data, test_data


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden.")
        exit()

    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)

    example_symbol = list(all_data.keys())[0]
    print(f"In-Sample-Zeitraum ({example_symbol}):     "
          f"{train_data[example_symbol]['open_time'].min()} bis {train_data[example_symbol]['open_time'].max()}")
    print(f"Out-of-Sample-Zeitraum ({example_symbol}):  "
          f"{test_data[example_symbol]['open_time'].min()} bis {test_data[example_symbol]['open_time'].max()}")
    print()

    print("=" * 60)
    print("SCHRITT 1: Optimierung auf In-Sample-Daten (alle Symbole)")
    print("=" * 60)
    train_results = run_multi_optimisation(train_data)

    if train_results.empty:
        print("Keine robuste Kombination im Trainingszeitraum gefunden.")
        exit()

    best = train_results.iloc[0]
    print(f"\nBeste In-Sample-Kombination:")
    print(f"  T3 Fast: {best['t3_fast']}  |  T3 Slow: {best['t3_slow']}  |  "
          f"ADX-Schwelle: {best['adx_threshold']}  |  Stop-Loss: {best['stop_loss_pct']}%")
    print(f"  -> {best['num_trades']} Trades ueber {best['num_symbols']} Symbole, "
          f"{best['win_rate']}% Win Rate, {best['total_return_pct']}% Summe, Score: {best['robustness_score']}")

    print("\n" + "=" * 60)
    print("SCHRITT 2: Test auf Out-of-Sample-Daten (ungesehen, alle Symbole)")
    print("=" * 60)

    test_result = evaluate_combination_multi(
        test_data,
        t3_fast=int(best["t3_fast"]),
        t3_slow=int(best["t3_slow"]),
        adx_threshold=best["adx_threshold"],
        stop_loss_pct=best["stop_loss_pct"],
    )

    print()
    if test_result is None:
        print("Diese Parameter erfuellen die Mindestkriterien im Out-of-Sample-Zeitraum nicht.")
    else:
        print(f"Out-of-Sample-Ergebnis:")
        print(f"  -> {test_result['num_trades']} Trades ueber {test_result['num_symbols']} Symbole, "
              f"{test_result['win_rate']}% Win Rate, {test_result['total_return_pct']}% Summe, "
              f"Score: {test_result['robustness_score']}")

        print("\n" + "=" * 60)
        print("VERGLEICH")
        print("=" * 60)
        print(f"{'Metrik':<22}{'In-Sample':>15}{'Out-of-Sample':>18}")
        print(f"{'Win Rate':<22}{best['win_rate']:>14}%{test_result['win_rate']:>17}%")
        print(f"{'Ø Gewinn/Trade':<22}{best['avg_return_pct']:>14}%{test_result['avg_return_pct']:>17}%")
        print(f"{'Anzahl Trades':<22}{best['num_trades']:>15}{test_result['num_trades']:>18}")

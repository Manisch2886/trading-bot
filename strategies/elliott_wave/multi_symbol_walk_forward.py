"""
Phase 3f - Multi-Symbol Walk-Forward-Validierung
====================================================
Kombiniert die beiden bisherigen Validierungsideen:
- Mehrere Coins gleichzeitig (mehr Trades, robustere Statistik)
- Train/Test-Split ueber die Zeit (Overfitting-Check)

Jeder Coin wird zeitlich in In-Sample (erste 70%) und Out-of-Sample
(letzte 30%) geteilt. Die Optimierung laeuft NUR auf den In-Sample-
Daten aller Coins zusammen. Die dort gefundene beste Kombination wird
anschliessend auf die Out-of-Sample-Daten aller Coins angewendet -
komplett ungesehene Daten, keine erneute Optimierung.
"""

import pandas as pd

from multi_symbol_optimise import (
    load_all_symbol_data,
    run_multi_optimisation,
    evaluate_combination_multi,
)

TRAIN_SPLIT_RATIO = 0.7


def split_all_symbols(all_data: dict, ratio: float) -> tuple:
    """Teilt JEDES Symbol einzeln zeitlich in Train/Test, behaelt die Struktur bei."""
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
        print("Keine Daten gefunden. Erst 'python3 fetch_multi_data.py' ausfuehren.")
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
    print(f"  Zigzag: {best['deviation_pct']}%  |  Stop-Loss: {best['stop_loss_pct']}%  |  "
          f"Take-Profit Fib: {best['take_profit_fib']}")
    print(f"  -> {best['num_trades']} Trades ueber {best['num_symbols']} Symbole, "
          f"{best['win_rate']}% Win Rate, {best['total_return_pct']}% Summe, Score: {best['robustness_score']}")

    print("\n" + "=" * 60)
    print("SCHRITT 2: Test auf Out-of-Sample-Daten (ungesehen, alle Symbole)")
    print("=" * 60)

    test_result = evaluate_combination_multi(
        test_data,
        deviation_pct=best["deviation_pct"],
        stop_loss_pct=best["stop_loss_pct"],
        take_profit_fib=best["take_profit_fib"],
    )

    print()
    if test_result is None:
        print("Diese Parameter erfuellen die Mindestkriterien (Trades/Symbole)",
              "im Out-of-Sample-Zeitraum nicht.")
        print("Das ist selbst ein wichtiges Ergebnis: die Strategie generiert",
              "im neuen Zeitraum nicht genug verlaessliche Signale.")
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
        print(f"{'Robustheit-Score':<22}{best['robustness_score']:>15}{test_result['robustness_score']:>18}")

        score_drop = (1 - test_result["robustness_score"] / best["robustness_score"]) * 100 if best["robustness_score"] else 0
        print(f"\nScore-Rueckgang Out-of-Sample: {score_drop:.0f}%")
        if score_drop > 50:
            print("-> Deutlicher Rueckgang: starkes Overfitting-Warnsignal.")
        elif score_drop > 20:
            print("-> Merklicher Rueckgang: mit Vorsicht behandeln, weiter beobachten.")
        else:
            print("-> Ergebnis bleibt in aehnlicher Groessenordnung: positives Robustheits-Signal.")

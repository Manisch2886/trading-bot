"""
Phase 3b - Walk-Forward-Validierung (Train/Test-Split)
========================================================
Klassisches Overfitting-Problem: Parameter, die auf einem Datensatz
optimiert wurden, koennen einfach "zufaellig gut zu genau diesen
Daten passen", ohne eine echte, uebertragbare Logik abzubilden.

Diese Validierung prueft das, indem sie den Datensatz in zwei
unabhaengige Zeitabschnitte teilt:

- IN-SAMPLE (erste 70% der Zeit): hier wird optimiert, also die
  beste Parameter-Kombination gesucht (wie in optimise_elliott.py)
- OUT-OF-SAMPLE (letzte 30% der Zeit): die dort gefundene beste
  Kombination wird HIER angewendet, ohne erneut zu optimieren

Wenn die Out-of-Sample-Ergebnisse deutlich schlechter sind als die
In-Sample-Ergebnisse, ist das ein starkes Warnsignal fuer Overfitting.
Wenn sie sich in aehnlicher Groessenordnung bewegen, ist das ein
gutes Zeichen fuer Robustheit.

WICHTIG: Mit nur wenigen Trades insgesamt ist auch dieser Test kein
endgueltiger Beweis, sondern ein zusaetzliches Indiz.
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

from optimise_elliott import run_optimisation, evaluate_combination


TRAIN_SPLIT_RATIO = 0.7  # 70% In-Sample, 30% Out-of-Sample


def split_data(price_df: pd.DataFrame, ratio: float) -> tuple:
    """Teilt die Preisdaten rein zeitlich in zwei aufeinanderfolgende Bloecke."""
    split_idx = int(len(price_df) * ratio)
    train_df = price_df.iloc[:split_idx].reset_index(drop=True)
    test_df = price_df.iloc[split_idx:].reset_index(drop=True)
    return train_df, test_df


if __name__ == "__main__":
    price_df = pd.read_csv(os.path.join(DATA_DIR, "BTCUSDT_1h.csv"), parse_dates=["open_time"])

    train_df, test_df = split_data(price_df, TRAIN_SPLIT_RATIO)

    print(f"In-Sample (Training):     {train_df['open_time'].min()} bis {train_df['open_time'].max()}")
    print(f"Out-of-Sample (Test):     {test_df['open_time'].min()} bis {test_df['open_time'].max()}")
    print()

    # Schritt 1: Optimierung NUR auf den Trainingsdaten
    print("=" * 60)
    print("SCHRITT 1: Optimierung auf In-Sample-Daten")
    print("=" * 60)
    train_results = run_optimisation(train_df)

    if train_results.empty:
        print("Keine robuste Kombination im Trainingszeitraum gefunden.")
        print("Zeitraum ist evtl. zu kurz oder Kriterien zu streng.")
        exit()

    best = train_results.iloc[0]
    print(f"\nBeste In-Sample-Kombination:")
    print(f"  Zigzag: {best['deviation_pct']}%  |  Stop-Loss: {best['stop_loss_pct']}%  |  "
          f"Take-Profit Fib: {best['take_profit_fib']}")
    print(f"  -> {best['num_trades']} Trades, {best['win_rate']}% Win Rate, "
          f"{best['total_return_pct']}% Gesamtertrag, Score: {best['robustness_score']}")

    # Schritt 2: Dieselbe Kombination auf den UNGESEHENEN Testdaten anwenden
    print("\n" + "=" * 60)
    print("SCHRITT 2: Test auf Out-of-Sample-Daten (ungesehen)")
    print("=" * 60)

    test_result = evaluate_combination(
        test_df,
        deviation_pct=best["deviation_pct"],
        stop_loss_pct=best["stop_loss_pct"],
        take_profit_fib=best["take_profit_fib"],
    )

    print()
    if test_result is None:
        print("Keine Trades im Out-of-Sample-Zeitraum mit diesen Parametern.")
        print("Das ist selbst ein Hinweis: die Strategie generiert im neuen")
        print("Zeitraum nicht genug Signale, um verlaesslich bewertet zu werden.")
    else:
        print(f"Out-of-Sample-Ergebnis:")
        print(f"  -> {test_result['num_trades']} Trades, {test_result['win_rate']}% Win Rate, "
              f"{test_result['total_return_pct']}% Gesamtertrag, Score: {test_result['robustness_score']}")

        print("\n" + "=" * 60)
        print("VERGLEICH")
        print("=" * 60)
        print(f"{'Metrik':<20}{'In-Sample':>15}{'Out-of-Sample':>18}")
        print(f"{'Win Rate':<20}{best['win_rate']:>14}%{test_result['win_rate']:>17}%")
        print(f"{'Ø Gewinn/Trade':<20}{best['avg_return_pct']:>14}%{test_result['avg_return_pct']:>17}%")
        print(f"{'Robustheit-Score':<20}{best['robustness_score']:>15}{test_result['robustness_score']:>18}")

        score_drop = (1 - test_result["robustness_score"] / best["robustness_score"]) * 100 if best["robustness_score"] else 0
        print(f"\nScore-Rueckgang Out-of-Sample: {score_drop:.0f}%")
        if score_drop > 50:
            print("-> Deutlicher Rueckgang: starkes Overfitting-Warnsignal.")
        elif score_drop > 20:
            print("-> Merklicher Rueckgang: mit Vorsicht behandeln, weiter beobachten.")
        else:
            print("-> Ergebnis bleibt in aehnlicher Groessenordnung: positives Robustheits-Signal.")

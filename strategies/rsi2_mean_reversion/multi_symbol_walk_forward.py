"""
Phase 2 - Multi-Symbol Walk-Forward-Validierung: RSI-2 Mean-Reversion
==========================================================================
Analog zum Muster der bestehenden Bots: teilt jedes Symbol zeitlich in
In-Sample (erste 70%) und Out-of-Sample (letzte 30%). Die Optimierung
laeuft NUR auf den In-Sample-Daten; die dort beste Kombination wird
anschliessend auf die Out-of-Sample-Daten angewendet - komplett
ungesehene Daten, keine erneute Optimierung.

WICHTIG: Der Split erfolgt auf den Indikator-Daten NACH der
SMA(200)-Berechnung (siehe load_all_symbol_data in multi_symbol_optimise.py),
sodass auch der Out-of-Sample-Teil ab dem ersten Tag einen gueltigen
SMA(200)-Trendfilter hat (kein Warm-up-Verlust am Anfang des OOS-Fensters).
"""

import pandas as pd

from multi_symbol_optimise import (
    load_all_symbol_data,
    run_multi_optimisation,
    evaluate_combination_multi,
)

TRAIN_SPLIT_RATIO = 0.7


def split_all_symbols(all_data: dict, ratio: float) -> tuple:
    """Teilt jedes Symbol einzeln zeitlich - WICHTIG: der Split-Punkt wird
    innerhalb des RECENT_YEARS_ONLY-Auswertungsfensters (entry_cutoff bis
    Datenende) berechnet, NICHT auf der vollen, teils jahrzehntelangen
    Roh-Historie (die nur fuer den SMA(200)-Vorlauf gebraucht wird). Sonst
    haette z.B. eine seit 1999 gelistete Aktie einen 70/30-Split-Punkt weit
    ausserhalb des eigentlichen 10-Jahres-Fensters - sehr kurzes In-Sample,
    sehr langes Out-of-Sample, kein echter 70/30-Split des Bewertungsfensters."""
    train_data, test_data = {}, {}
    for symbol, (df_ind, entry_cutoff) in all_data.items():
        window_start = entry_cutoff if entry_cutoff is not None else df_ind["open_time"].min()
        window_end = df_ind["open_time"].max()
        split_time = window_start + (window_end - window_start) * ratio

        train_data[symbol] = (df_ind, entry_cutoff, split_time)
        test_data[symbol] = (df_ind, split_time, None)

    return train_data, test_data


def load_all_symbol_data_split() -> tuple:
    """Laedt die Daten und gibt sie direkt als (train_data, test_data) fuer
    evaluate_combination_multi_windowed zurueck."""
    all_data = load_all_symbol_data()
    return split_all_symbols(all_data, TRAIN_SPLIT_RATIO)


def evaluate_combination_multi_windowed(windowed_data: dict, rsi_threshold: float, stop_loss_pct: float) -> dict:
    """Wie evaluate_combination_multi, aber windowed_data enthaelt
    (df_ind, cutoff_start, cutoff_end) - Trades werden zusaetzlich auf
    cutoff_end begrenzt (falls gesetzt), fuer den In-Sample-Teil."""
    from multi_symbol_optimise import (
        get_trades_for_symbol, MIN_TRADES, MIN_SYMBOLS_CONTRIBUTING,
        MIN_AVG_RETURN_PCT, calculate_robustness_score,
    )
    all_trades = []
    contributing_symbols = 0

    for symbol, (df_ind, cutoff_start, cutoff_end) in windowed_data.items():
        trades = get_trades_for_symbol(df_ind, cutoff_start, rsi_threshold, stop_loss_pct)
        if cutoff_end is not None and not trades.empty:
            trades = trades[trades["entry_time"] < cutoff_end]
        if not trades.empty:
            trades = trades.copy()
            trades["symbol"] = symbol
            all_trades.append(trades)
            contributing_symbols += 1

    if not all_trades:
        return None
    combined = pd.concat(all_trades, ignore_index=True)
    if len(combined) < MIN_TRADES or contributing_symbols < MIN_SYMBOLS_CONTRIBUTING:
        return None

    win_rate = (combined["pnl_pct"] > 0).mean() * 100
    total_return = combined["pnl_pct"].sum()
    avg_return = combined["pnl_pct"].mean()
    if avg_return < MIN_AVG_RETURN_PCT:
        return None

    cum_returns = combined["pnl_pct"].cumsum()
    max_drawdown = (cum_returns - cum_returns.cummax()).min()

    result = {
        "rsi_threshold": rsi_threshold,
        "stop_loss_pct": stop_loss_pct if stop_loss_pct is not None else "kein Stop",
        "num_trades": len(combined), "num_symbols": contributing_symbols,
        "win_rate": round(win_rate, 1), "total_return_pct": round(total_return, 2),
        "avg_return_pct": round(avg_return, 2),
        "avg_holding_days": round(combined["holding_days"].mean(), 1),
        "max_drawdown_pct": round(max_drawdown, 2),
    }
    result["robustness_score"] = calculate_robustness_score(result)
    return result


def run_multi_optimisation_windowed(windowed_data: dict) -> pd.DataFrame:
    from multi_symbol_optimise import RSI_THRESHOLD_RANGE, STOP_LOSS_RANGE
    results = []
    combinations = [(r, s) for r in RSI_THRESHOLD_RANGE for s in STOP_LOSS_RANGE]
    for rsi_threshold, stop_loss_pct in combinations:
        result = evaluate_combination_multi_windowed(windowed_data, rsi_threshold, stop_loss_pct)
        if result is not None:
            results.append(result)
    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values("robustness_score", ascending=False).reset_index(drop=True)
    return df


if __name__ == "__main__":
    train_data, test_data = load_all_symbol_data_split()
    if not train_data:
        print("Keine Daten gefunden.")
        exit()

    example_symbol = list(train_data.keys())[0]
    print(f"In-Sample endet / Out-of-Sample beginnt ({example_symbol}): "
          f"{train_data[example_symbol][2]}\n")

    print("=" * 60)
    print("SCHRITT 1: Optimierung auf In-Sample-Daten (alle Symbole)")
    print("=" * 60)
    train_results = run_multi_optimisation_windowed(train_data)

    if train_results.empty:
        print("Keine robuste Kombination im Trainingszeitraum gefunden.")
        exit()

    best = train_results.iloc[0]
    print(f"\nBeste In-Sample-Kombination:")
    print(f"  RSI-Schwelle: {best['rsi_threshold']}  |  Stop-Loss: {best['stop_loss_pct']}")
    print(f"  -> {best['num_trades']} Trades ueber {best['num_symbols']} Symbole, "
          f"{best['win_rate']}% Win Rate, {best['total_return_pct']}% Summe, "
          f"Score: {best['robustness_score']}")

    print("\n" + "=" * 60)
    print("SCHRITT 2: Test auf Out-of-Sample-Daten (ungesehen)")
    print("=" * 60)
    stop_loss_val = None if best["stop_loss_pct"] == "kein Stop" else best["stop_loss_pct"]
    test_result = evaluate_combination_multi_windowed(test_data, best["rsi_threshold"], stop_loss_val)

    if test_result is None:
        print("\nDiese Parameter erfuellen die Mindestkriterien im "
              "Out-of-Sample-Zeitraum nicht.")
    else:
        print(f"\nOut-of-Sample-Ergebnis:")
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

"""
Offener Punkt (Uebergabeprotokoll Abschnitt 9, Punkt 2) - MAX_CONCURRENT_POSITIONS
======================================================================================
Beim T3/SuperTrend-Bot wurde MAX_CONCURRENT_POSITIONS empirisch verglichen
(3 / 5 / 8 / unbegrenzt), beim Aktien-Bot wurde 8 bisher nur als plausibler
Startwert uebernommen, nie systematisch getestet. Dieses Skript holt das nach,
mit denselben Methoden wie bereits im Projekt etabliert:

- Volle Equity-Simulation ueber den gesamten Datenzeitraum (RECENT_YEARS_ONLY),
  fuer direkten Vergleich mit dem dokumentierten Live-Ergebnis (155.811,94 /
  +1458.12%, siehe live_params.py-Historie)
- Zusaetzlich ein Out-of-Sample-Check (letzte 30% der Daten je Symbol), mit
  FESTEN aktuellen Live-Parametern (keine Re-Optimierung) - beantwortet die
  Frage "waere das Positionslimit auch auf ungesehenen Daten stabil", analog
  zum isolierten VWAP-Filter-Test beim T3-Bot.

Alle uebrigen Parameter bleiben exakt auf dem aktuellen validierten Live-Stand
(live_params.py), es wird ausschliesslich MAX_CONCURRENT_POSITIONS variiert.
"""

import os
import sys
import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

from multi_symbol_optimise import load_all_symbol_data
from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO
from equity_simulation import collect_all_trades, simulate_portfolio, calculate_max_drawdown
from live_params import DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB

STARTING_CAPITAL = 10_000.0
ALLOCATION_PCT = 0.10
POSITION_LIMITS = [3, 5, 8, None]  # None = unbegrenzt


def run_one(trades: pd.DataFrame, max_concurrent) -> dict:
    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, max_concurrent)
    total_return_pct = (result["final_capital"] / STARTING_CAPITAL - 1) * 100
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    return {
        "max_concurrent_positions": max_concurrent if max_concurrent is not None else "unbegrenzt",
        "final_capital": result["final_capital"],
        "total_return_pct": round(total_return_pct, 2),
        "executed_trades": result["num_executed"],
        "skipped_trades": result["num_skipped"],
        "max_drawdown_pct": max_dd,
    }


if __name__ == "__main__":
    print(f"Feste Parameter (aktueller Live-Stand): Zigzag {DEVIATION_PCT}% | "
          f"Stop-Loss {STOP_LOSS_PCT}% | Take-Profit Fib {TAKE_PROFIT_FIB}\n")

    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden.")
        exit()

    print("=" * 70)
    print("TEIL 1: Volle Equity-Simulation (gesamter Zeitraum)")
    print("=" * 70)
    trades_full = collect_all_trades(all_data, DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB, True)
    print(f"{len(trades_full)} Trades insgesamt gefunden.\n")

    full_results = [run_one(trades_full, limit) for limit in POSITION_LIMITS]
    full_df = pd.DataFrame(full_results)
    print(full_df.to_string(index=False))

    print("\n" + "=" * 70)
    print("TEIL 2: Out-of-Sample-Check (letzte 30%, feste Parameter, keine Re-Optimierung)")
    print("=" * 70)
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)
    example_symbol = list(all_data.keys())[0]
    print(f"Out-of-Sample-Zeitraum: {test_data[example_symbol]['open_time'].min()} "
          f"bis {test_data[example_symbol]['open_time'].max()}\n")

    trades_oos = collect_all_trades(test_data, DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB, True)
    print(f"{len(trades_oos)} Trades im Out-of-Sample-Zeitraum gefunden.\n")

    oos_results = [run_one(trades_oos, limit) for limit in POSITION_LIMITS]
    oos_df = pd.DataFrame(oos_results)
    print(oos_df.to_string(index=False))

    full_df.to_csv(os.path.join(RESULTS_DIR, "experiment_position_limit_full.csv"), index=False)
    oos_df.to_csv(os.path.join(RESULTS_DIR, "experiment_position_limit_oos.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_position_limit_full.csv")
    print(f"Gespeichert unter: {RESULTS_DIR}/experiment_position_limit_oos.csv")

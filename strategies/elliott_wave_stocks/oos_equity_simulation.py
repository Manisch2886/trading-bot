"""
Phase 4a - Out-of-Sample Equity-Simulation
==============================================
Kombiniert die Walk-Forward-Validierung mit der Portfolio-Simulation:
Optimiert wird nur auf den In-Sample-Daten, aber die eigentliche
Kapital-Simulation (Startkapital, Positionsgroessen, Gebuehren) laeuft
NUR auf dem Out-of-Sample-Zeitraum - also auf Daten, die die
Optimierung nie gesehen hat.

Das beantwortet die konkrete Frage: "Waere ich mit echtem, wenn auch
virtuellem Kapital am Ende des ungesehenen Zeitraums besser oder
schlechter dagestanden?" - verstaendlicher als ein abstrakter Score.
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

from multi_symbol_optimise import load_all_symbol_data, run_multi_optimisation
from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO
from equity_simulation import collect_all_trades, simulate_portfolio, calculate_max_drawdown

STARTING_CAPITAL = 10_000.0
ALLOCATION_PCT = 0.10


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden. Erst 'python3 fetch_multi_data.py' ausfuehren.")
        exit()

    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)

    example_symbol = list(all_data.keys())[0]
    print(f"Out-of-Sample-Zeitraum: {test_data[example_symbol]['open_time'].min()} "
          f"bis {test_data[example_symbol]['open_time'].max()}\n")

    print("Optimiere auf In-Sample-Daten, um die Parameter zu bestimmen...")
    train_results = run_multi_optimisation(train_data)

    if train_results.empty:
        print("Keine robuste Kombination im Trainingszeitraum gefunden.")
        exit()

    best = train_results.iloc[0]
    print(f"\nVerwendete Parameter (aus In-Sample-Optimierung):")
    print(f"  Zigzag: {best['deviation_pct']}%  |  Stop-Loss: {best['stop_loss_pct']}%  |  "
          f"Take-Profit Fib: {best['take_profit_fib']}\n")

    print("Sammle Trades im Out-of-Sample-Zeitraum...")
    trades = collect_all_trades(
        test_data,
        deviation_pct=best["deviation_pct"],
        stop_loss_pct=best["stop_loss_pct"],
        take_profit_fib=best["take_profit_fib"],
    )

    if trades.empty:
        print("Keine Trades im Out-of-Sample-Zeitraum gefunden.")
        exit()

    print(f"{len(trades)} Trades gefunden.\n")

    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT)

    print("=" * 55)
    print("OUT-OF-SAMPLE PORTFOLIO-SIMULATION")
    print("=" * 55)
    print(f"Startkapital:            {STARTING_CAPITAL:,.2f}")
    print(f"Endkapital:              {result['final_capital']:,.2f}")

    total_return_pct = (result["final_capital"] / STARTING_CAPITAL - 1) * 100
    print(f"Gesamtrendite:           {total_return_pct:.2f}%")
    print(f"Ausgefuehrte Trades:     {result['num_executed']}")
    print(f"Uebersprungene Trades:   {result['num_skipped']} (nicht genug freies Kapital)")

    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    print(f"Max Drawdown (Kapital):  {max_dd:.2f}%")

    if not result["equity_curve"].empty:
        output_path = os.path.join(RESULTS_DIR, "oos_equity_curve.csv")
        result["equity_curve"].to_csv(output_path, index=False)
        print(f"\nGespeichert als: {output_path}")

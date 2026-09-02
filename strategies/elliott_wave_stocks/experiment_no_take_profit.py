"""
Offener Punkt (Uebergabeprotokoll Abschnitt 9, Punkt 1) - "Gewinne laufen lassen"
======================================================================================
Frueherer isolierter Test (siehe Protokoll) zeigte deutlich hoeheren
Ø-Gewinn/Trade ohne festes Kursziel (14.80% vs. 6.47%), aber groesseren
Drawdown - nie in Kombination mit dem aktuellen validierten Top-150-Setup
(Zigzag 5%, Stop-Loss 3%, Positionslimit 8) getestet. Dieses Skript holt
das nach, mit denselben Methoden wie beim isolierten VWAP-Filter-Test des
T3-Bots: Vergleich mit UND ohne die zu testende Regel, bei sonst exakt
gleichen, aktuell validierten Parametern.

Take-Profit betrifft nur den STRATEGIE-Exit, nicht Buy-and-Hold - der
Buy-and-Hold-Vergleich bleibt fuer beide Varianten identisch (siehe
buy_and_hold_benchmark.py, unveraendert, hier nur zur Einordnung erneut
ausgegeben).
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
from buy_and_hold_benchmark import calculate_buy_and_hold
from live_params import DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB, MAX_CONCURRENT_POSITIONS

STARTING_CAPITAL = 10_000.0
ALLOCATION_PCT = 0.10
VARIANTS = [("MIT Take-Profit (aktueller Live-Stand)", True), ("OHNE Take-Profit (laufen lassen)", False)]


def trade_stats(trades: pd.DataFrame) -> dict:
    return {
        "num_trades": len(trades),
        "win_rate_pct": round((trades["pnl_pct"] > 0).mean() * 100, 1) if len(trades) else 0,
        "avg_pnl_pct": round(trades["pnl_pct"].mean(), 2) if len(trades) else 0,
        "best_trade_pct": round(trades["pnl_pct"].max(), 2) if len(trades) else 0,
        "worst_trade_pct": round(trades["pnl_pct"].min(), 2) if len(trades) else 0,
    }


def run_variant(all_data: dict, use_take_profit: bool) -> dict:
    trades = collect_all_trades(all_data, DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB, use_take_profit)
    stats = trade_stats(trades)

    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)
    total_return_pct = (result["final_capital"] / STARTING_CAPITAL - 1) * 100
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)

    stats.update({
        "final_capital": result["final_capital"],
        "total_return_pct": round(total_return_pct, 2),
        "executed_trades": result["num_executed"],
        "skipped_trades": result["num_skipped"],
        "max_drawdown_pct": max_dd,
    })
    return stats


if __name__ == "__main__":
    print(f"Feste Parameter (aktueller Live-Stand): Zigzag {DEVIATION_PCT}% | "
          f"Stop-Loss {STOP_LOSS_PCT}% | Positionslimit {MAX_CONCURRENT_POSITIONS}\n")

    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden.")
        exit()

    print("=" * 70)
    print("TEIL 1: Volle Equity-Simulation (gesamter Zeitraum)")
    print("=" * 70)
    full_rows = []
    for label, use_tp in VARIANTS:
        row = run_variant(all_data, use_tp)
        row["variante"] = label
        full_rows.append(row)
    full_df = pd.DataFrame(full_rows).set_index("variante")
    print(full_df.to_string())

    bh = calculate_buy_and_hold(all_data, STARTING_CAPITAL)
    print(f"\nZum Vergleich - Buy-and-Hold (unveraendert, unabhaengig vom Take-Profit): "
          f"Endkapital {bh['final_capital']:,.2f} ({bh['total_return_pct']:.2f}%), "
          f"Max Drawdown {bh['max_drawdown_pct']:.2f}%")

    print("\n" + "=" * 70)
    print("TEIL 2: Out-of-Sample-Check (letzte 30%, feste Parameter, keine Re-Optimierung)")
    print("=" * 70)
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)
    example_symbol = list(all_data.keys())[0]
    print(f"Out-of-Sample-Zeitraum: {test_data[example_symbol]['open_time'].min()} "
          f"bis {test_data[example_symbol]['open_time'].max()}\n")

    oos_rows = []
    for label, use_tp in VARIANTS:
        row = run_variant(test_data, use_tp)
        row["variante"] = label
        oos_rows.append(row)
    oos_df = pd.DataFrame(oos_rows).set_index("variante")
    print(oos_df.to_string())

    full_df.to_csv(os.path.join(RESULTS_DIR, "experiment_no_take_profit_full.csv"))
    oos_df.to_csv(os.path.join(RESULTS_DIR, "experiment_no_take_profit_oos.csv"))
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_no_take_profit_full.csv")
    print(f"Gespeichert unter: {RESULTS_DIR}/experiment_no_take_profit_oos.csv")

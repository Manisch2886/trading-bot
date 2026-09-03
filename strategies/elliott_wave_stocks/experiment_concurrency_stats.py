"""
Diagnose-Skript: tatsaechliche Anzahl gleichzeitig offener Positionen
==========================================================================
Beantwortet zwei konkrete Fragen zum "unbegrenzt"-Testlauf aus
experiment_combined.py / experiment_position_limit.py:

1. Wie oft/wie stark wird MAX_CONCURRENT_POSITIONS=None (unbegrenzt) in der
   Praxis tatsaechlich durch die Kapitalpruefung selbst begrenzt (siehe
   equity_simulation.simulate_portfolio: allocation = capital * allocation_pct
   bezieht sich auf das AKTUELLE GESAMTKAPITAL, ein Entry wird nur ausgefuehrt,
   wenn allocation <= free_capital - das deckelt die Anzahl gleichzeitig
   offener Positionen implizit auf ca. 1/allocation_pct, unabhaengig vom
   Limit)?
2. Wie hoch waren Durchschnitt und Maximum der gleichzeitig offenen
   Positionen tatsaechlich, fuer "ohne Take-Profit" bei unbegrenztem Limit?

Dies ist eine lokal instrumentierte Kopie von simulate_portfolio (aus
equity_simulation.py), die zusaetzlich die Anzahl offener Positionen nach
jedem Entry-Event mitschreibt. Die Simulationslogik selbst ist unveraendert
uebernommen - nur die Protokollierung ist neu.
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
from equity_simulation import collect_all_trades, calculate_max_drawdown
from live_params import DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB

STARTING_CAPITAL = 10_000.0
ALLOCATION_PCT = 0.10


def simulate_portfolio_instrumented(trades: pd.DataFrame, starting_capital: float,
                                     allocation_pct: float, max_concurrent_positions=None) -> dict:
    """Wie equity_simulation.simulate_portfolio, zusaetzlich mit Mitschrieb der
    Anzahl offener Positionen nach jedem Entry-Event (fuer Concurrency-Statistik)."""
    events = []
    for idx, trade in trades.iterrows():
        events.append((trade["entry_time"], "entry", idx))
        events.append((trade["exit_time"], "exit", idx))
    events.sort(key=lambda e: (e[0], e[1] != "exit"))

    capital = starting_capital
    open_positions = {}
    skipped_trades = []
    executed_trades = []
    equity_curve = []
    concurrency_log = []  # (time, anzahl_offener_positionen) nach jedem Entry
    capital_utilisation_log = []  # (time, gebundenes_kapital / gesamtkapital)

    for time, event_type, idx in events:
        trade = trades.loc[idx]

        if event_type == "entry":
            if max_concurrent_positions is not None and len(open_positions) >= max_concurrent_positions:
                skipped_trades.append(idx)
                continue

            bound_capital = sum(open_positions.values())
            free_capital = capital - bound_capital
            allocation = capital * allocation_pct

            if allocation > free_capital:
                skipped_trades.append(idx)
                continue

            open_positions[idx] = allocation
            executed_trades.append(idx)
            concurrency_log.append((time, len(open_positions)))
            capital_utilisation_log.append((time, (bound_capital + allocation) / capital * 100))

        elif event_type == "exit":
            if idx not in open_positions:
                continue
            allocation = open_positions.pop(idx)
            pnl_pct = trade["pnl_pct"]
            result_value = allocation * (1 + pnl_pct / 100)
            capital += (result_value - allocation)
            equity_curve.append({
                "time": time, "symbol": trade["symbol"], "pnl_pct": pnl_pct,
                "allocation": round(allocation, 2), "capital_after": round(capital, 2),
            })

    equity_df = pd.DataFrame(equity_curve)
    concurrency_df = pd.DataFrame(concurrency_log, columns=["time", "open_positions"])
    utilisation_df = pd.DataFrame(capital_utilisation_log, columns=["time", "capital_utilisation_pct"])

    return {
        "final_capital": round(capital, 2),
        "num_executed": len(executed_trades),
        "num_skipped": len(skipped_trades),
        "equity_curve": equity_df,
        "concurrency": concurrency_df,
        "utilisation": utilisation_df,
    }


def report(label: str, trades: pd.DataFrame, max_concurrent):
    result = simulate_portfolio_instrumented(trades, STARTING_CAPITAL, ALLOCATION_PCT, max_concurrent)
    conc = result["concurrency"]["open_positions"]
    util = result["utilisation"]["capital_utilisation_pct"]
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    total_return_pct = (result["final_capital"] / STARTING_CAPITAL - 1) * 100

    print(f"\n--- {label} ---")
    print(f"Endkapital: {result['final_capital']:,.2f} ({total_return_pct:.2f}%)  |  "
          f"Max Drawdown: {max_dd:.2f}%  |  Trades ausgefuehrt/uebersprungen: "
          f"{result['num_executed']}/{result['num_skipped']}")
    if len(conc) > 0:
        print(f"Gleichzeitig offene Positionen (jeweils gemessen bei Entry-Events):")
        print(f"  Durchschnitt: {conc.mean():.2f}  |  Median: {conc.median():.0f}  |  "
              f"Maximum: {conc.max()}  |  90.-Perzentil: {conc.quantile(0.9):.1f}")
        print(f"Kapitalauslastung (gebunden / Gesamtkapital) bei Entry-Events:")
        print(f"  Durchschnitt: {util.mean():.1f}%  |  Maximum: {util.max():.1f}%")
    return result


if __name__ == "__main__":
    print(f"Feste Parameter: Zigzag {DEVIATION_PCT}% | Stop-Loss {STOP_LOSS_PCT}% | "
          f"Take-Profit Fib {TAKE_PROFIT_FIB} | Allokation je Trade: {ALLOCATION_PCT*100:.0f}%")

    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden.")
        exit()

    print("\n" + "=" * 70)
    print("GESAMTZEITRAUM")
    print("=" * 70)
    trades_tp = collect_all_trades(all_data, DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB, True)
    trades_notp = collect_all_trades(all_data, DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB, False)

    report("mit Take-Profit, Limit 8 (aktuell live)", trades_tp, 8)
    report("ohne Take-Profit, Limit 8", trades_notp, 8)
    report("ohne Take-Profit, unbegrenzt", trades_notp, None)

    print("\n" + "=" * 70)
    print("OUT-OF-SAMPLE (letzte 30%, keine Re-Optimierung)")
    print("=" * 70)
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)
    trades_tp_oos = collect_all_trades(test_data, DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB, True)
    trades_notp_oos = collect_all_trades(test_data, DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB, False)

    report("mit Take-Profit, Limit 8 (aktuell live)", trades_tp_oos, 8)
    report("ohne Take-Profit, Limit 8", trades_notp_oos, 8)
    report("ohne Take-Profit, unbegrenzt", trades_notp_oos, None)

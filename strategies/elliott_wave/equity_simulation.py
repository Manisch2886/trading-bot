"""
Phase 3e - Equity-Kurven-Simulation (realistisches Portfolio)
================================================================
Bisher haben wir Trades isoliert bewertet und ihre Prozentwerte
einfach aufsummiert. Das ignoriert eine wichtige Realitaet: Du hast
nur EIN Kapital, das sich auf mehrere, teils gleichzeitig offene
Positionen (verschiedene Coins) aufteilen muss.

Diese Simulation:
- startet mit einem virtuellen Kapital (Standard: 10.000)
- allokiert pro Trade einen festen Anteil des AKTUELLEN Kapitals
  (Standard: 10%)
- verarbeitet alle Trades ueber alle Symbole chronologisch
- blockiert neue Trades, wenn nicht genug freies (nicht bereits
  gebundenes) Kapital verfuegbar ist
- gibt eine echte Equity-Kurve, finales Kapital und einen
  Kapital-basierten Max Drawdown zurueck

WICHTIG: Vereinfachungen gegenueber der Realitaet:
- Keine Transaktionsgebuehren oder Slippage
- Offene Positionen werden nicht "mark-to-market" bewertet,
  Kapital aktualisiert sich erst beim Trade-Ausstieg
- Gleichzeitige Signale werden in der Reihenfolge verarbeitet, in
  der die zugrunde liegenden Wellen abgeschlossen wurden
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

from multi_symbol_optimise import load_all_symbol_data, get_trades_for_symbol
import backtest_elliott

STARTING_CAPITAL = 10_000.0
ALLOCATION_PCT = 0.10  # Anteil des aktuellen Kapitals pro Trade

# Beste Kombination aus der letzten Multi-Symbol-Optimierung
DEVIATION_PCT = 4.0
STOP_LOSS_PCT = 2.0
TAKE_PROFIT_FIB = 0.236


def collect_all_trades(all_data: dict, deviation_pct: float,
                        stop_loss_pct: float, take_profit_fib: float) -> pd.DataFrame:
    """Sammelt alle Trades ueber alle Symbole fuer eine gegebene Parameter-Kombination."""
    backtest_elliott.STOP_LOSS_PCT = stop_loss_pct
    backtest_elliott.TAKE_PROFIT_FIB = take_profit_fib

    all_trades = []
    for symbol, price_df in all_data.items():
        trades = get_trades_for_symbol(price_df, deviation_pct)
        if not trades.empty:
            trades = trades.copy()
            trades["symbol"] = symbol
            all_trades.append(trades)

    if not all_trades:
        return pd.DataFrame()

    combined = pd.concat(all_trades, ignore_index=True)
    combined["entry_time"] = pd.to_datetime(combined["entry_time"])
    combined["exit_time"] = pd.to_datetime(combined["exit_time"])
    return combined.sort_values("entry_time").reset_index(drop=True)


def simulate_portfolio(trades: pd.DataFrame, starting_capital: float,
                        allocation_pct: float) -> dict:
    """
    Event-basierte Simulation: verarbeitet Entry- und Exit-Ereignisse
    chronologisch, verwaltet freies vs. gebundenes Kapital.
    """
    events = []
    for idx, trade in trades.iterrows():
        events.append((trade["entry_time"], "entry", idx))
        events.append((trade["exit_time"], "exit", idx))

    # Bei gleichem Zeitpunkt: Exits vor Entries verarbeiten (Kapital wird frei)
    events.sort(key=lambda e: (e[0], e[1] != "exit"))

    capital = starting_capital
    open_positions = {}  # idx -> allokierter Betrag
    skipped_trades = []
    executed_trades = []
    equity_curve = []

    for time, event_type, idx in events:
        trade = trades.loc[idx]

        if event_type == "entry":
            bound_capital = sum(open_positions.values())
            free_capital = capital - bound_capital
            allocation = capital * allocation_pct

            if allocation > free_capital:
                skipped_trades.append(idx)
                continue

            open_positions[idx] = allocation
            executed_trades.append(idx)

        elif event_type == "exit":
            if idx not in open_positions:
                continue  # Trade wurde nie eroeffnet (uebersprungen)

            allocation = open_positions.pop(idx)
            pnl_pct = trade["pnl_pct"]
            result_value = allocation * (1 + pnl_pct / 100)
            capital += (result_value - allocation)

            equity_curve.append({
                "time": time,
                "symbol": trade["symbol"],
                "pnl_pct": pnl_pct,
                "allocation": round(allocation, 2),
                "capital_after": round(capital, 2),
            })

    equity_df = pd.DataFrame(equity_curve)

    return {
        "final_capital": round(capital, 2),
        "num_executed": len(executed_trades),
        "num_skipped": len(skipped_trades),
        "equity_curve": equity_df,
    }


def calculate_max_drawdown(equity_df: pd.DataFrame, starting_capital: float) -> float:
    if equity_df.empty:
        return 0.0
    capital_series = pd.concat([pd.Series([starting_capital]), equity_df["capital_after"]], ignore_index=True)
    running_max = capital_series.cummax()
    drawdown_pct = (capital_series - running_max) / running_max * 100
    return round(drawdown_pct.min(), 2)


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden. Erst 'python3 fetch_multi_data.py' ausfuehren.")
        exit()

    trades = collect_all_trades(all_data, DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB)

    if trades.empty:
        print("Keine Trades fuer diese Parameter-Kombination gefunden.")
        exit()

    print(f"{len(trades)} Trades ueber alle Symbole gefunden (unsortiert nach Kapital-Verfuegbarkeit).\n")

    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT)

    print("=" * 55)
    print("PORTFOLIO-SIMULATION")
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
        print("\nLetzte 10 abgeschlossene Trades:")
        print(result["equity_curve"].tail(10).to_string(index=False))

        output_path = os.path.join(RESULTS_DIR, "equity_curve.csv")
        result["equity_curve"].to_csv(output_path, index=False)
        print(f"\nGespeichert als: {output_path}")

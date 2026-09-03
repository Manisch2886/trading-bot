"""
Experiment: Trailing-Take-Profit fuer den Aktien-Bot (Elliott Wave, Top 150)
================================================================================
Vergleicht den aktuellen Live-Stand (kein festes Take-Profit-Ziel, "Gewinne
laufen lassen bis Stop-Loss oder Zeit-Exit" - seit 2026-09-03 live, siehe
live_params.py) gegen einen NACHZIEHENDEN Stop-Loss: Sobald eine Position im
Gewinn ist, wandert der Stop mit dem seit Einstieg erreichten Kurshoechststand
nach oben mit (fester Abstand X% darunter). Der urspruengliche feste Stop-Loss
(STOP_LOSS_PCT unter Einstieg) bleibt so lange aktiv, bis der Trailing-Stop ihn
ueberholt.

WICHTIG: Reine Backtest-/Equity-Simulations-Analyse. Aendert NICHTS an
live_params.py oder forward_test.py - das ist bewusst so, Entscheidung ueber
eine Uebernahme steht noch aus.

Implementiert eine eigene, von backtest_elliott.py UNABHAENGIGE
simulate_trade_trailing()-Funktion (keine Aenderung an den bestehenden
Backtest-Dateien, die auch von anderen Skripten/live_params-Validierungen
genutzt werden). Wiederverwendet simulate_portfolio()/calculate_max_drawdown()
aus equity_simulation.py unveraendert fuer die Kapital-Simulation.

Kein Blick in die Zukunft innerhalb eines Balkens: Der Trailing-Stop wird erst
NACH der Stop-Pruefung eines Balkens anhand von dessen High aktualisiert -
wirkt also erst ab dem naechsten Balken, genau wie ein echter Broker-Trailing-
Stop-Auftrag es auf Tagesbasis auch nur koennte.
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

from zigzag_indicator import calculate_zigzag
from elliott_wave_counter import find_impulse_waves, remove_overlapping
from multi_symbol_optimise import load_all_symbol_data
from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO
from equity_simulation import collect_all_trades, simulate_portfolio, calculate_max_drawdown
from live_params import DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB, MAX_CONCURRENT_POSITIONS

STARTING_CAPITAL = 10_000.0
ALLOCATION_PCT = 0.10
MAX_HOLD_HOURS = 90  # konsistent mit backtest_elliott.py (Balken-Anzahl, siehe dortiger Kommentar)
TRADING_FEE_PCT = 0.1
SLIPPAGE_PCT = 0.05

TRAILING_DISTANCES = [5.0, 8.0, 12.0, 15.0]
# Bonus (nur falls einfach umsetzbar - ist es, da simulate_trade_trailing das
# ohnehin unterstuetzt): Trailing erst ab einer Mindest-Gewinnschwelle aktiv,
# davor normaler fester Stop-Loss.
ACTIVATION_VARIANTS = [(8.0, 8.0), (12.0, 10.0)]  # (trailing_pct, activation_pct)


def simulate_trade_trailing(price_df: pd.DataFrame, entry_time, entry_price: float,
                             initial_stop_price: float, trailing_pct: float,
                             max_hold_bars: int, activation_pct: float = None) -> dict:
    """Wie backtest_elliott.simulate_trade, aber mit nachziehendem statt festem
    Take-Profit. activation_pct=None: Trailing ist von Anfang an aktiv."""
    future = price_df[price_df["open_time"] > entry_time].head(max_hold_bars)

    stop_price = initial_stop_price
    running_high = entry_price

    for _, row in future.iterrows():
        if row["low"] <= stop_price:
            result = "stop_loss" if stop_price == initial_stop_price else "trailing_stop"
            return {"exit_time": row["open_time"], "exit_price": stop_price, "result": result}

        running_high = max(running_high, row["high"])
        trailing_active = activation_pct is None or running_high >= entry_price * (1 + activation_pct / 100)
        if trailing_active:
            candidate_stop = running_high * (1 - trailing_pct / 100)
            if candidate_stop > stop_price:
                stop_price = candidate_stop

    if len(future) > 0:
        last_row = future.iloc[-1]
        return {"exit_time": last_row["open_time"], "exit_price": last_row["close"], "result": "time_exit"}
    return {"exit_time": None, "exit_price": entry_price, "result": "no_data"}


def run_backtest_trailing(price_df: pd.DataFrame, impulses: pd.DataFrame,
                           trailing_pct: float, activation_pct: float = None) -> pd.DataFrame:
    trades = []
    for _, wave in impulses.iterrows():
        if wave["direction"] == "bullish":
            continue  # Long-only, wie im Rest des Projekts

        entry_time = pd.to_datetime(wave["end_time"])
        entry_price = wave["wave5"]
        stop_price = entry_price * (1 - STOP_LOSS_PCT / 100)

        outcome = simulate_trade_trailing(price_df, entry_time, entry_price, stop_price,
                                           trailing_pct, MAX_HOLD_HOURS, activation_pct)
        if outcome["exit_price"] is None or outcome["result"] == "no_data":
            continue

        pnl_pct = (outcome["exit_price"] - entry_price) / entry_price * 100
        total_cost_pct = 2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)
        pnl_pct_net = pnl_pct - total_cost_pct
        holding_days = (outcome["exit_time"] - entry_time).days if outcome["exit_time"] is not None else None

        trades.append({
            "entry_time": entry_time, "entry_price": entry_price,
            "exit_time": outcome["exit_time"], "exit_price": outcome["exit_price"],
            "result": outcome["result"], "pnl_pct": round(pnl_pct_net, 2),
            "holding_days": holding_days,
        })
    return pd.DataFrame(trades)


def get_trades_for_symbol_trailing(price_df: pd.DataFrame, deviation_pct: float,
                                    trailing_pct: float, activation_pct: float = None) -> pd.DataFrame:
    zigzag = calculate_zigzag(price_df, deviation_pct=deviation_pct)
    if len(zigzag) < 6:
        return pd.DataFrame()
    impulses = find_impulse_waves(zigzag, min_fib_score=0.3)
    if impulses.empty:
        return pd.DataFrame()
    impulses = remove_overlapping(impulses)
    impulses = impulses[impulses["direction"] == "bearish"]
    if impulses.empty:
        return pd.DataFrame()
    return run_backtest_trailing(price_df, impulses, trailing_pct, activation_pct)


def collect_all_trades_trailing(all_data: dict, deviation_pct: float,
                                 trailing_pct: float, activation_pct: float = None) -> pd.DataFrame:
    all_trades = []
    for symbol, price_df in all_data.items():
        trades = get_trades_for_symbol_trailing(price_df, deviation_pct, trailing_pct, activation_pct)
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


def evaluate(label: str, trades: pd.DataFrame) -> dict:
    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)
    total_return_pct = (result["final_capital"] / STARTING_CAPITAL - 1) * 100
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    avg_holding = trades["holding_days"].mean() if "holding_days" in trades.columns and len(trades) else float("nan")
    return {
        "variante": label,
        "trades_gefunden": len(trades),
        "trades_ausgefuehrt": result["num_executed"],
        "trades_uebersprungen": result["num_skipped"],
        "final_capital": result["final_capital"],
        "total_return_pct": round(total_return_pct, 2),
        "max_drawdown_pct": max_dd,
        "avg_holding_days": round(avg_holding, 1) if pd.notna(avg_holding) else None,
    }


def run_all(all_data: dict, label_suffix: str) -> pd.DataFrame:
    rows = []

    # Baseline: aktueller Live-Stand (kein Take-Profit, Limit 8) - im selben
    # Lauf neu berechnet statt alte Zahlen zu uebernehmen, fuer einen fairen,
    # auf denselben Daten basierenden Vergleich.
    baseline_trades = collect_all_trades(all_data, DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB, False)
    baseline_trades = baseline_trades.copy()
    if not baseline_trades.empty:
        baseline_trades["holding_days"] = (baseline_trades["exit_time"] - baseline_trades["entry_time"]).dt.days
    rows.append(evaluate(f"Baseline: kein Take-Profit (live seit 2026-09-03) - {label_suffix}", baseline_trades))

    for trailing_pct in TRAILING_DISTANCES:
        trades = collect_all_trades_trailing(all_data, DEVIATION_PCT, trailing_pct)
        rows.append(evaluate(f"Trailing {trailing_pct:.0f}% (ab Einstieg aktiv) - {label_suffix}", trades))

    for trailing_pct, activation_pct in ACTIVATION_VARIANTS:
        trades = collect_all_trades_trailing(all_data, DEVIATION_PCT, trailing_pct, activation_pct)
        rows.append(evaluate(
            f"Trailing {trailing_pct:.0f}% (aktiv erst ab +{activation_pct:.0f}% Gewinn) - {label_suffix}",
            trades))

    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(f"Feste Parameter: Zigzag {DEVIATION_PCT}% | initialer Stop-Loss {STOP_LOSS_PCT}% | "
          f"Positionslimit {MAX_CONCURRENT_POSITIONS} (identisch zum Live-Stand)\n")

    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden.")
        exit()

    print("=" * 100)
    print("GESAMTZEITRAUM")
    print("=" * 100)
    full_df = run_all(all_data, "gesamt")
    print(full_df.to_string(index=False))

    print("\n" + "=" * 100)
    print("OUT-OF-SAMPLE (letzte 30%, keine Re-Optimierung)")
    print("=" * 100)
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)
    example_symbol = list(all_data.keys())[0]
    print(f"Out-of-Sample-Zeitraum: {test_data[example_symbol]['open_time'].min()} "
          f"bis {test_data[example_symbol]['open_time'].max()}\n")
    oos_df = run_all(test_data, "OOS")
    print(oos_df.to_string(index=False))

    full_df.to_csv(os.path.join(RESULTS_DIR, "experiment_trailing_take_profit_full.csv"), index=False)
    oos_df.to_csv(os.path.join(RESULTS_DIR, "experiment_trailing_take_profit_oos.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_trailing_take_profit_full.csv")
    print(f"Gespeichert unter: {RESULTS_DIR}/experiment_trailing_take_profit_oos.csv")

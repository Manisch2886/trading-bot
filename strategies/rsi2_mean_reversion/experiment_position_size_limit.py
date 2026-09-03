"""
Experiment: Positionsgroesse x Positionslimit fuer RSI-2 (auf Rueckfrage)
================================================================================
Hypothese aus der Diskussion: Bei RSI-2 ist nicht das Positionslimit (8) der
eigentliche Flaschenhals, sondern die 10%-Kapitalallokation pro Trade selbst -
RSI-2 erzeugt so viele gleichzeitige Signale, dass schon die Kapitalpruefung
(allocation <= free_capital, siehe equity_simulation.simulate_portfolio) die
meisten Trades blockiert, bevor das Limit ueberhaupt greift. Testet daher
BEIDE Dimensionen gemeinsam: Positionsgroesse (10%/5%/3%) x Limit
(8/15/20/unbegrenzt), fixe Parameter RSI<5, kein Stop (beste validierte
Kombination aus dem Prototyp), Gesamtzeitraum UND Out-of-Sample.
"""

import os
import pandas as pd

from multi_symbol_optimise import load_all_symbol_data
from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO
from equity_simulation import collect_all_trades, simulate_portfolio, calculate_max_drawdown, STARTING_CAPITAL
from pipeline_report import collect_trades_windowed
from strategy_paths import get_strategy_paths

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

RSI_THRESHOLD = 5.0
STOP_LOSS_PCT = None  # "kein Stop" - beste validierte Kombination

ALLOCATION_PCTS = [0.10, 0.05, 0.03]
POSITION_LIMITS = [8, 15, 20, None]


def evaluate(trades: pd.DataFrame, allocation_pct: float, max_concurrent) -> dict:
    result = simulate_portfolio(trades, STARTING_CAPITAL, allocation_pct, max_concurrent)
    total_return_pct = (result["final_capital"] / STARTING_CAPITAL - 1) * 100
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    return {
        "allocation_pct": f"{allocation_pct*100:.0f}%",
        "limit": max_concurrent if max_concurrent is not None else "unbegrenzt",
        "final_capital": result["final_capital"],
        "total_return_pct": round(total_return_pct, 2),
        "trades_ausgefuehrt": result["num_executed"],
        "trades_uebersprungen": result["num_skipped"],
        "max_drawdown_pct": max_dd,
    }


def run_matrix(trades: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for allocation_pct in ALLOCATION_PCTS:
        for limit in POSITION_LIMITS:
            rows.append(evaluate(trades, allocation_pct, limit))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(f"Feste Parameter: RSI-Schwelle {RSI_THRESHOLD} | Stop-Loss: "
          f"{'kein Stop' if STOP_LOSS_PCT is None else STOP_LOSS_PCT}\n")

    all_data = load_all_symbol_data()
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)

    print("=" * 90)
    print("GESAMTZEITRAUM")
    print("=" * 90)
    trades_full = collect_all_trades(all_data, RSI_THRESHOLD, STOP_LOSS_PCT)
    print(f"{len(trades_full)} Trades insgesamt gefunden.\n")
    full_df = run_matrix(trades_full)
    print(full_df.to_string(index=False))

    print("\n" + "=" * 90)
    print("OUT-OF-SAMPLE (letzte 30% je Symbol, keine Re-Optimierung)")
    print("=" * 90)
    trades_oos = collect_trades_windowed(test_data, RSI_THRESHOLD, STOP_LOSS_PCT)
    print(f"{len(trades_oos)} Trades im Out-of-Sample-Zeitraum gefunden.\n")
    oos_df = run_matrix(trades_oos)
    print(oos_df.to_string(index=False))

    full_df.to_csv(os.path.join(RESULTS_DIR, "experiment_position_size_limit_full.csv"), index=False)
    oos_df.to_csv(os.path.join(RESULTS_DIR, "experiment_position_size_limit_oos.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_position_size_limit_full.csv")
    print(f"Gespeichert unter: {RESULTS_DIR}/experiment_position_size_limit_oos.csv")

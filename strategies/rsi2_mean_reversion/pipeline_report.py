"""
Vollstaendiger Pipeline-Report: RSI-2 Mean-Reversion Prototyp
==================================================================
Fuehrt Equity-Simulation (Gesamtzeitraum UND Out-of-Sample) fuer alle 6
getesteten Parameter-Kombinationen aus (RSI-Schwelle x Stop-Loss), plus
den Buy-and-Hold-Vergleich - konsolidierter Report analog zum Tabellenformat
der bisherigen Experimente (siehe elliott_wave_stocks/EXPERIMENT_FINDINGS.md).
"""

import os
import pandas as pd

from multi_symbol_optimise import load_all_symbol_data, RSI_THRESHOLD_RANGE, STOP_LOSS_RANGE
from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO
from equity_simulation import collect_all_trades, simulate_portfolio, calculate_max_drawdown, \
    STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS
from buy_and_hold_benchmark import load_recent_data, calculate_buy_and_hold
from strategy_paths import get_strategy_paths

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]


def collect_trades_windowed(windowed_data: dict, rsi_threshold: float, stop_loss_pct: float,
                             max_hold_days: int = None) -> pd.DataFrame:
    from multi_symbol_optimise import get_trades_for_symbol
    all_trades = []
    for symbol, (df_ind, cutoff_start, cutoff_end) in windowed_data.items():
        trades = get_trades_for_symbol(df_ind, cutoff_start, rsi_threshold, stop_loss_pct, max_hold_days)
        if cutoff_end is not None and not trades.empty:
            trades = trades[trades["entry_time"] < cutoff_end]
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


def evaluate(trades: pd.DataFrame) -> dict:
    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)
    total_return_pct = (result["final_capital"] / STARTING_CAPITAL - 1) * 100
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    return {
        "final_capital": result["final_capital"],
        "total_return_pct": round(total_return_pct, 2),
        "trades_ausgefuehrt": result["num_executed"],
        "trades_uebersprungen": result["num_skipped"],
        "max_drawdown_pct": max_dd,
    }


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)

    print("=" * 100)
    print("GESAMTZEITRAUM - Equity-Simulation je Kombination (Startkapital 10.000, 10% Allokation, Limit 8)")
    print("=" * 100)
    full_rows = []
    for r in RSI_THRESHOLD_RANGE:
        for s in STOP_LOSS_RANGE:
            trades = collect_all_trades(all_data, r, s)
            row = evaluate(trades)
            row.update({"rsi_threshold": r, "stop_loss_pct": s if s is not None else "kein Stop"})
            full_rows.append(row)
    full_df = pd.DataFrame(full_rows)[["rsi_threshold", "stop_loss_pct", "final_capital", "total_return_pct",
                                        "trades_ausgefuehrt", "trades_uebersprungen", "max_drawdown_pct"]]
    print(full_df.to_string(index=False))

    print("\n" + "=" * 100)
    print("OUT-OF-SAMPLE (letzte 30% je Symbol innerhalb des 10-Jahres-Fensters, keine Re-Optimierung)")
    print("=" * 100)
    oos_rows = []
    for r in RSI_THRESHOLD_RANGE:
        for s in STOP_LOSS_RANGE:
            trades = collect_trades_windowed(test_data, r, s)
            row = evaluate(trades)
            row.update({"rsi_threshold": r, "stop_loss_pct": s if s is not None else "kein Stop"})
            oos_rows.append(row)
    oos_df = pd.DataFrame(oos_rows)[["rsi_threshold", "stop_loss_pct", "final_capital", "total_return_pct",
                                      "trades_ausgefuehrt", "trades_uebersprungen", "max_drawdown_pct"]]
    print(oos_df.to_string(index=False))

    print("\n" + "=" * 100)
    print("BUY-AND-HOLD-VERGLEICH (dasselbe Universum/Zeitraum)")
    print("=" * 100)
    bh_data = load_recent_data()
    bh_result = calculate_buy_and_hold(bh_data, STARTING_CAPITAL)
    print(f"Endkapital: {bh_result['final_capital']:,.2f}  |  Rendite: {bh_result['total_return_pct']:.2f}%  |  "
          f"Max Drawdown: {bh_result['max_drawdown_pct']:.2f}%  |  Aktien: {bh_result['num_symbols']}")

    full_df.to_csv(os.path.join(RESULTS_DIR, "pipeline_report_full.csv"), index=False)
    oos_df.to_csv(os.path.join(RESULTS_DIR, "pipeline_report_oos.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/pipeline_report_full.csv")
    print(f"Gespeichert unter: {RESULTS_DIR}/pipeline_report_oos.csv")

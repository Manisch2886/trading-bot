"""
Experiment: Wirksamkeit des Entkopplungs-Schutzes (auf ausdrueckliche Anfrage)
================================================================================
Vergleicht die validierte Basis-Konfiguration MIT und OHNE den
Entkopplungs-Schutz (rollierende 252-Tage-Korrelation, Pause bei <0.40,
Wiederaufnahme erst bei >=0.70 - siehe backtest_pair_rotation.py Punkt 4).
Leitfrage: verbessert der Schutz Drawdown/Rendite spuerbar, oder ist er
in der Praxis wirkungslos (z.B. weil die entdeckten Paare ohnehin selten
so stark entkoppeln, dass der Schwellenwert je unterschritten wird)?
"""

import os
import pandas as pd

from multi_pair_optimise import load_all_symbol_data, get_reference_date, build_pairs, get_trades_for_pair
from multi_pair_walk_forward import split_window, TRAIN_SPLIT_RATIO
from equity_simulation import simulate_portfolio, calculate_max_drawdown, \
    STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS, LOOKBACK_DAYS, REBALANCE_DAYS, STOP_LOSS_PCT
from strategy_paths import get_strategy_paths

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]


def collect_trades(pairs: list, entry_cutoff, use_decoupling_protection: bool, cutoff_end=None) -> pd.DataFrame:
    all_trades = []
    for symbol_a, symbol_b, corr, pair_base_df in pairs:
        trades = get_trades_for_pair(pair_base_df, symbol_a, symbol_b, LOOKBACK_DAYS, REBALANCE_DAYS,
                                      STOP_LOSS_PCT, entry_cutoff, use_decoupling_protection)
        if cutoff_end is not None and not trades.empty:
            trades = trades[trades["entry_time"] < cutoff_end]
        if not trades.empty:
            all_trades.append(trades)
    if not all_trades:
        return pd.DataFrame()
    combined = pd.concat(all_trades, ignore_index=True)
    combined["entry_time"] = pd.to_datetime(combined["entry_time"])
    combined["exit_time"] = pd.to_datetime(combined["exit_time"])
    return combined.sort_values("entry_time").reset_index(drop=True)


def stats(trades: pd.DataFrame, label: str) -> dict:
    if trades.empty:
        return {"variante": label, "n": 0}
    win_rate = round((trades["pnl_pct"] > 0).mean() * 100, 1)
    avg_pnl = round(trades["pnl_pct"].mean(), 2)
    n_decoupling_exits = int((trades["result"] == "decoupling_exit").sum())

    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)
    total_return_pct = round((result["final_capital"] / STARTING_CAPITAL - 1) * 100, 2)
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)

    return {
        "variante": label, "n": len(trades), "win_rate_pct": win_rate, "avg_pnl_pct": avg_pnl,
        "n_decoupling_exits": n_decoupling_exits,
        "portfolio_final_capital": result["final_capital"], "portfolio_return_pct": total_return_pct,
        "trades_ausgefuehrt": result["num_executed"], "trades_uebersprungen": result["num_skipped"],
        "max_drawdown_pct": max_dd,
    }


if __name__ == "__main__":
    symbol_data = load_all_symbol_data()
    reference_date = get_reference_date(symbol_data)
    window_start, split_time, window_end = split_window(reference_date, symbol_data, TRAIN_SPLIT_RATIO)
    pairs = build_pairs(symbol_data, reference_date)

    print("=" * 90)
    print("GESAMTZEITRAUM")
    print("=" * 90)
    trades_with = collect_trades(pairs, reference_date, use_decoupling_protection=True)
    trades_without = collect_trades(pairs, reference_date, use_decoupling_protection=False)
    full_rows = [
        stats(trades_without, "Ohne Entkopplungs-Schutz"),
        stats(trades_with, "Mit Entkopplungs-Schutz"),
    ]
    print(pd.DataFrame(full_rows).to_string(index=False))

    print("\n" + "=" * 90)
    print("OUT-OF-SAMPLE")
    print("=" * 90)
    trades_oos_with = collect_trades(pairs, split_time, use_decoupling_protection=True)
    trades_oos_without = collect_trades(pairs, split_time, use_decoupling_protection=False)
    oos_rows = [
        stats(trades_oos_without, "Ohne Entkopplungs-Schutz"),
        stats(trades_oos_with, "Mit Entkopplungs-Schutz"),
    ]
    print(pd.DataFrame(oos_rows).to_string(index=False))

    os.makedirs(RESULTS_DIR, exist_ok=True)
    pd.DataFrame(full_rows).to_csv(os.path.join(RESULTS_DIR, "experiment_decoupling_protection_full.csv"), index=False)
    pd.DataFrame(oos_rows).to_csv(os.path.join(RESULTS_DIR, "experiment_decoupling_protection_oos.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_decoupling_protection_{{full,oos}}.csv")

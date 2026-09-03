"""
Experiment: BTC-Regime-Filter fuer Volatility Breakout Krypto
================================================================================
Testet den beim T3/SuperTrend-Bot etablierten BTC-Regime-Filter als
zusaetzliche Vorbedingung fuer Einstiege - insbesondere relevant, weil die
Aktien-Version genau in anhaltenden Baerenmaerkten (2022) am schwaechsten
war (siehe results/volatility_breakout/PROTOTYPE_FINDINGS.md Abschnitt 10).
Vergleich Basis-Regel (kein Filter) gegen gefilterte Variante,
Gesamtzeitraum UND Out-of-Sample.
"""

import os
import pandas as pd

from multi_symbol_optimise import load_all_symbol_data, DATA_DIR
from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO
from equity_simulation import collect_all_trades, simulate_portfolio, calculate_max_drawdown, \
    STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS, STOP_LOSS_PCT
from pipeline_report import collect_trades_windowed
from regime_filter import compute_btc_regime, filter_trades_by_regime
from strategy_paths import get_strategy_paths

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]


def load_btc_regime() -> pd.DataFrame:
    btc_df = pd.read_csv(os.path.join(DATA_DIR, "BTCUSDT_1d.csv"), parse_dates=["open_time"])
    return compute_btc_regime(btc_df)


def stats(trades: pd.DataFrame, label: str) -> dict:
    if trades.empty:
        return {"variante": label, "n": 0}
    win_rate = round((trades["pnl_pct"] > 0).mean() * 100, 1)
    avg_pnl = round(trades["pnl_pct"].mean(), 2)

    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)
    total_return_pct = round((result["final_capital"] / STARTING_CAPITAL - 1) * 100, 2)
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)

    return {
        "variante": label, "n": len(trades), "win_rate_pct": win_rate, "avg_pnl_pct": avg_pnl,
        "portfolio_final_capital": result["final_capital"], "portfolio_return_pct": total_return_pct,
        "trades_ausgefuehrt": result["num_executed"], "trades_uebersprungen": result["num_skipped"],
        "max_drawdown_pct": max_dd,
    }


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)
    btc_regime = load_btc_regime()

    print("=" * 90)
    print("GESAMTZEITRAUM")
    print("=" * 90)
    trades_no_filter = collect_all_trades(all_data, STOP_LOSS_PCT)
    trades_with_filter = filter_trades_by_regime(trades_no_filter, btc_regime)
    full_rows = [
        stats(trades_no_filter, "Ohne BTC-Regime-Filter (Basis-Regel)"),
        stats(trades_with_filter, "Mit BTC-Regime-Filter (nur bei BTC-Aufwaertstrend)"),
    ]
    print(pd.DataFrame(full_rows).to_string(index=False))

    print("\n" + "=" * 90)
    print("OUT-OF-SAMPLE")
    print("=" * 90)
    trades_oos_no_filter = collect_trades_windowed(test_data, STOP_LOSS_PCT)
    trades_oos_with_filter = filter_trades_by_regime(trades_oos_no_filter, btc_regime)
    oos_rows = [
        stats(trades_oos_no_filter, "Ohne BTC-Regime-Filter (Basis-Regel)"),
        stats(trades_oos_with_filter, "Mit BTC-Regime-Filter (nur bei BTC-Aufwaertstrend)"),
    ]
    print(pd.DataFrame(oos_rows).to_string(index=False))

    os.makedirs(RESULTS_DIR, exist_ok=True)
    pd.DataFrame(full_rows).to_csv(os.path.join(RESULTS_DIR, "experiment_btc_regime_filter_full.csv"), index=False)
    pd.DataFrame(oos_rows).to_csv(os.path.join(RESULTS_DIR, "experiment_btc_regime_filter_oos.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_btc_regime_filter_{{full,oos}}.csv")

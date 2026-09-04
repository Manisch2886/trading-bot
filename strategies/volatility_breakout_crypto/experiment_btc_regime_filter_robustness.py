"""
Aufgabe 1: Robustheit des BTC-Regime-Filter-OOS-Vorteils pruefen
================================================================================
Der einzelne 70/30-Split zeigte ein Trailing-Take-Profit-artiges Muster
(Filter schadet Gesamtzeitraum, hilft OOS - nie beides) - genau das
Overfitting-Warnsignal aus dem Aktien-Bot-Praezedenzfall. Testet daher mit
mehreren leicht unterschiedlichen Split-Punkten (65/35, 70/30, 75/25), ob
der OOS-Vorteil des Filters KONSISTENT ist oder sich je nach Split-Punkt
dreht (dann waere es ein Zufallsprodukt der einen Split-Stelle, kein
echter Effekt).

NICHTS wird live geschaltet - reine Analyse.
"""

import os
import pandas as pd

from multi_symbol_optimise import load_all_symbol_data, DATA_DIR
from multi_symbol_walk_forward import split_all_symbols
from equity_simulation import collect_all_trades, simulate_portfolio, calculate_max_drawdown, \
    STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS, STOP_LOSS_PCT
from pipeline_report import collect_trades_windowed
from regime_filter import compute_btc_regime, filter_trades_by_regime
from strategy_paths import get_strategy_paths

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

SPLIT_RATIOS = [0.65, 0.70, 0.75]


def load_btc_regime() -> pd.DataFrame:
    btc_df = pd.read_csv(os.path.join(DATA_DIR, "BTCUSDT_1d.csv"), parse_dates=["open_time"])
    return compute_btc_regime(btc_df)


def stats(trades: pd.DataFrame, label: str, split_ratio: float) -> dict:
    if trades.empty:
        return {"split": f"{split_ratio*100:.0f}/{(1-split_ratio)*100:.0f}", "variante": label, "n": 0}
    win_rate = round((trades["pnl_pct"] > 0).mean() * 100, 1)
    avg_pnl = round(trades["pnl_pct"].mean(), 2)

    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)
    total_return_pct = round((result["final_capital"] / STARTING_CAPITAL - 1) * 100, 2)
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)

    return {
        "split": f"{split_ratio*100:.0f}/{(1-split_ratio)*100:.0f}", "variante": label,
        "n": len(trades), "win_rate_pct": win_rate, "avg_pnl_pct": avg_pnl,
        "portfolio_return_pct": total_return_pct, "max_drawdown_pct": max_dd,
    }


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    btc_regime = load_btc_regime()

    rows = []
    for ratio in SPLIT_RATIOS:
        train_data, test_data = split_all_symbols(all_data, ratio)

        trades_oos_no_filter = collect_trades_windowed(test_data, STOP_LOSS_PCT)
        trades_oos_with_filter = filter_trades_by_regime(trades_oos_no_filter, btc_regime)

        rows.append(stats(trades_oos_no_filter, "Ohne Filter", ratio))
        rows.append(stats(trades_oos_with_filter, "Mit Filter", ratio))

    df = pd.DataFrame(rows)
    print("=" * 100)
    print("OUT-OF-SAMPLE UEBER VERSCHIEDENE SPLIT-PUNKTE (Robustheits-Check)")
    print("=" * 100)
    print(df.to_string(index=False))

    print("\n" + "=" * 100)
    print("RANGFOLGE-STABILITAET JE SPLIT-PUNKT (Rendite, Overfitting-Check)")
    print("=" * 100)
    all_consistent = True
    for ratio in SPLIT_RATIOS:
        split_label = f"{ratio*100:.0f}/{(1-ratio)*100:.0f}"
        sub = df[df["split"] == split_label].set_index("variante")
        if "Ohne Filter" not in sub.index or "Mit Filter" not in sub.index:
            continue
        no_filter_return = sub.loc["Ohne Filter", "portfolio_return_pct"]
        with_filter_return = sub.loc["Mit Filter", "portfolio_return_pct"]
        filter_better = with_filter_return > no_filter_return
        print(f"  Split {split_label}: Mit Filter {'BESSER' if filter_better else 'SCHLECHTER'} "
              f"({with_filter_return:+.2f}% vs. {no_filter_return:+.2f}% ohne Filter)")
        all_consistent = all_consistent and filter_better

    any_filter_better = any(
        df[(df["split"] == f"{r*100:.0f}/{(1-r)*100:.0f}") & (df["variante"] == "Mit Filter")]["portfolio_return_pct"].iloc[0] >
        df[(df["split"] == f"{r*100:.0f}/{(1-r)*100:.0f}") & (df["variante"] == "Ohne Filter")]["portfolio_return_pct"].iloc[0]
        for r in SPLIT_RATIOS
    )
    print(f"\nFilter in ALLEN getesteten Split-Punkten besser: {all_consistent}")
    print(f"Filter in MINDESTENS EINEM Split-Punkt besser: {any_filter_better}")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    df.to_csv(os.path.join(RESULTS_DIR, "experiment_btc_regime_filter_robustness.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_btc_regime_filter_robustness.csv")

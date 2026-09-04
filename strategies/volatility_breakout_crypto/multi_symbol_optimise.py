"""
Phase 1 - Multi-Symbol-Optimierung: Bollinger-Band-Squeeze-Breakout Krypto
================================================================================
Analog zu volatility_breakout/multi_symbol_optimise.py: testet NUR den
Stop-Loss (Squeeze-Lookback/Perzentil bleiben wie bei der Aktien-Version
fest, siehe backtest_breakout.py-Docstring). Universum: 25 Top-Volumen-
Krypto-Coins (shared/symbols_config.py) auf Tageskerzen
(data/<SYMBOL>_1d.csv, siehe shared/build_daily_crypto_data.py).
"""

import os
import sys
import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
DATA_DIR = _P["DATA_DIR"]
RESULTS_DIR = _P["RESULTS_DIR"]

from backtest_breakout import compute_indicators, run_backtest, WARMUP_PERIOD
from symbols_config import SYMBOLS

INTERVAL = "1d"

STOP_LOSS_RANGE = [3.0, 5.0, 8.0, None]

MIN_TRADES = 40
MIN_AVG_RETURN_PCT = 0.0
MIN_SYMBOLS_CONTRIBUTING = 8
MIN_HISTORY_DAYS = 500          # deckt den 126-Tage-Squeeze-Vorlauf plus echten Vorlauf ab


def load_all_symbol_data() -> dict:
    data = {}
    for symbol in SYMBOLS:
        csv_path = os.path.join(DATA_DIR, f"{symbol}_{INTERVAL}.csv")
        try:
            df = pd.read_csv(csv_path, parse_dates=["open_time"])
        except FileNotFoundError:
            print(f"Warnung: {csv_path} nicht gefunden, wird uebersprungen.")
            continue
        if df.empty:
            continue

        timespan_days = (df["open_time"].max() - df["open_time"].min()).days
        if timespan_days < MIN_HISTORY_DAYS:
            print(f"Hinweis: {symbol} deckt nur {timespan_days} Tage ab "
                  f"(< {MIN_HISTORY_DAYS} noetig), wird uebersprungen.")
            continue

        data[symbol] = df
    return data


def get_trades_for_symbol(price_df: pd.DataFrame, stop_loss_pct: float = None,
                           max_hold_days: int = None, use_volume_filter: bool = False,
                           entry_cutoff=None) -> pd.DataFrame:
    df_ind = compute_indicators(price_df)
    kwargs = {}
    if max_hold_days is not None:
        kwargs["max_hold_days"] = max_hold_days
    return run_backtest(df_ind, stop_loss_pct=stop_loss_pct, entry_cutoff=entry_cutoff,
                         use_volume_filter=use_volume_filter, **kwargs)


def calculate_robustness_score(row: dict) -> float:
    drawdown_penalty = abs(row["max_drawdown_pct"]) if row["max_drawdown_pct"] != 0 else 1.0
    return round((row["avg_return_pct"] * (row["num_trades"] ** 0.5)) / drawdown_penalty, 3)


def evaluate_combination_multi(all_data: dict, stop_loss_pct: float = None,
                                max_hold_days: int = None, use_volume_filter: bool = False) -> dict:
    all_trades = []
    contributing_symbols = 0
    for symbol, price_df in all_data.items():
        trades = get_trades_for_symbol(price_df, stop_loss_pct, max_hold_days, use_volume_filter)
        if not trades.empty:
            contributing_symbols += 1
            all_trades.append(trades)

    if not all_trades:
        return None
    combined = pd.concat(all_trades, ignore_index=True)
    if len(combined) < MIN_TRADES or contributing_symbols < MIN_SYMBOLS_CONTRIBUTING:
        return None

    win_rate = (combined["pnl_pct"] > 0).mean() * 100
    total_return = combined["pnl_pct"].sum()
    avg_return = combined["pnl_pct"].mean()
    if avg_return < MIN_AVG_RETURN_PCT:
        return None

    cum_returns = combined["pnl_pct"].cumsum()
    max_drawdown = (cum_returns - cum_returns.cummax()).min()

    result = {
        "stop_loss_pct": stop_loss_pct if stop_loss_pct is not None else "kein Stop",
        "num_trades": len(combined), "num_symbols": contributing_symbols,
        "win_rate": round(win_rate, 1), "total_return_pct": round(total_return, 2),
        "avg_return_pct": round(avg_return, 2),
        "avg_holding_days": round(combined["holding_days"].mean(), 1),
        "max_drawdown_pct": round(max_drawdown, 2),
    }
    result["robustness_score"] = calculate_robustness_score(result)
    return result


def run_multi_optimisation(all_data: dict) -> pd.DataFrame:
    results = []
    for stop_loss_pct in STOP_LOSS_RANGE:
        result = evaluate_combination_multi(all_data, stop_loss_pct)
        if result is not None:
            results.append(result)
    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values("robustness_score", ascending=False).reset_index(drop=True)
    return df


if __name__ == "__main__":
    print(f"Lade Tagesdaten fuer {len(SYMBOLS)} Krypto-Symbole...\n")
    all_data = load_all_symbol_data()
    print(f"\n{len(all_data)} Symbole mit ausreichender Historie geladen.\n")

    results_df = run_multi_optimisation(all_data)
    if results_df.empty:
        print("Keine Kombination erfuellt die Mindestkriterien.")
    else:
        print(results_df.to_string(index=False))
        os.makedirs(RESULTS_DIR, exist_ok=True)
        results_df.to_csv(os.path.join(RESULTS_DIR, "multi_symbol_optimisation_results.csv"), index=False)
        print(f"\nGespeichert unter: {RESULTS_DIR}/multi_symbol_optimisation_results.csv")

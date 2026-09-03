"""
Phase 1 - Multi-Symbol-Optimierung: RSI-2 Mean-Reversion Krypto
======================================================================
Analog zu rsi2_mean_reversion/multi_symbol_optimise.py, mit EINER
zusaetzlichen Grid-Dimension: SMA_TREND_PERIOD wird hier mitgetestet
(100/150/200 Tage), weil der 200-Tage-Trendfilter der Aktien-Version fuer
Krypto (historisch volatiler, andere Zyklen) nicht ungeprueft uebernommen
werden soll (siehe Nutzeranfrage "Trendfilter muesste neu kalibriert
werden").

Universum: dieselben 25 Top-Volumen-Krypto-Coins wie Elliott Wave
Krypto/T3-SuperTrend (shared/symbols_config.py), aber auf TAGESKERZEN
(data/<SYMBOL>_1d.csv, siehe shared/build_daily_crypto_data.py) statt 1h/4h -
siehe backtest_rsi2.py-Docstring fuer die Zeitrahmen-Begruendung.

MIN_HISTORY_DAYS liegt bewusst hoeher als bei T3/SuperTrend (730), weil der
laengste getestete SMA-Trendfilter (200 Tage) selbst schon Vorlauf braucht -
Symbole mit zu kurzer Historie (viele der ganz neuen Top-25-Coins, siehe
build_daily_crypto_data.py-Ausgabe) werden sauber uebersprungen statt mit
kaum belastbaren Trades in die Auswertung einzufliessen.
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

from backtest_rsi2 import compute_indicators, run_backtest
from symbols_config import SYMBOLS

INTERVAL = "1d"

SMA_TREND_RANGE = [100, 150, 200]
RSI_THRESHOLD_RANGE = [5.0, 10.0]
STOP_LOSS_RANGE = [None, 5.0, 8.0]

MIN_TRADES = 40                 # Krypto-Universum ist kleiner/kuerzer als Aktien (25 statt 147
                                 # Symbole, ~5 statt 10 Jahre, davon nur 30% im OOS-Fenster) - niedrigere
                                 # Schwelle als bei RSI-2 Aktien (150), angelehnt an T3/SuperTrend (40)
MIN_AVG_RETURN_PCT = 0.0
MIN_SYMBOLS_CONTRIBUTING = 8
MIN_HISTORY_DAYS = 500          # deckt den laengsten Trendfilter (SMA 200) plus echten Vorlauf ab


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


def get_trades_for_symbol(price_df: pd.DataFrame, rsi_threshold: float, sma_trend_period: int,
                           stop_loss_pct: float = None, entry_cutoff=None) -> pd.DataFrame:
    df_ind = compute_indicators(price_df, sma_trend_period)
    return run_backtest(df_ind, rsi_threshold, sma_trend_period, stop_loss_pct, entry_cutoff)


def calculate_robustness_score(row: dict) -> float:
    """Identische Formel wie rsi2_mean_reversion/multi_symbol_optimise.py
    (eigenstaendige Kopie) - Rendite pro Trade gewichtet mit der Trade-Anzahl
    (Wurzel, damit mehr Trades nicht linear ueberproportional zaehlen),
    normiert auf den Max-Drawdown-Proxy als Risikonenner."""
    drawdown_penalty = abs(row["max_drawdown_pct"]) if row["max_drawdown_pct"] != 0 else 1.0
    return round((row["avg_return_pct"] * (row["num_trades"] ** 0.5)) / drawdown_penalty, 3)


def evaluate_combination_multi(all_data: dict, rsi_threshold: float, sma_trend_period: int,
                                stop_loss_pct: float = None) -> dict:
    all_trades = []
    symbols_with_trades = 0
    for symbol, price_df in all_data.items():
        trades = get_trades_for_symbol(price_df, rsi_threshold, sma_trend_period, stop_loss_pct)
        if not trades.empty:
            symbols_with_trades += 1
            all_trades.append(trades)

    if not all_trades:
        return None
    combined = pd.concat(all_trades, ignore_index=True)
    n_trades = len(combined)
    if n_trades < MIN_TRADES or symbols_with_trades < MIN_SYMBOLS_CONTRIBUTING:
        return None

    win_rate = (combined["pnl_pct"] > 0).mean() * 100
    avg_return = combined["pnl_pct"].mean()
    if avg_return < MIN_AVG_RETURN_PCT:
        return None

    total_return = combined["pnl_pct"].sum()
    avg_holding = combined["holding_days"].mean()
    cum_returns = combined["pnl_pct"].cumsum()
    max_drawdown = (cum_returns - cum_returns.cummax()).min()

    result = {
        "sma_trend_period": sma_trend_period, "rsi_threshold": rsi_threshold,
        "stop_loss_pct": stop_loss_pct if stop_loss_pct is not None else "kein Stop",
        "num_trades": n_trades, "num_symbols": symbols_with_trades,
        "win_rate": round(win_rate, 1), "total_return_pct": round(total_return, 2),
        "avg_return_pct": round(avg_return, 2), "avg_holding_days": round(avg_holding, 1),
        "max_drawdown_pct": round(max_drawdown, 2),
    }
    result["robustness_score"] = calculate_robustness_score(result)
    return result


def run_multi_optimisation(all_data: dict) -> pd.DataFrame:
    results = []
    for sma_trend_period in SMA_TREND_RANGE:
        for rsi_threshold in RSI_THRESHOLD_RANGE:
            for stop_loss_pct in STOP_LOSS_RANGE:
                result = evaluate_combination_multi(all_data, rsi_threshold, sma_trend_period, stop_loss_pct)
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

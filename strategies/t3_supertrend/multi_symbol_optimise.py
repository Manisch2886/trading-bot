"""
Multi-Symbol Optimierung - T3/ADX/SuperTrend-Strategie
============================================================
Analog zu multi_symbol_optimise.py der Elliott-Wave-Strategie:
testet jede Parameter-Kombination auf allen verfuegbaren Symbolen
und fasst die Trades zusammen, um robustere Aussagen als mit nur
einem einzelnen Coin zu bekommen.
"""

import os
import sys
import pandas as pd
import itertools

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
DATA_DIR = _P["DATA_DIR"]
RESULTS_DIR = _P["RESULTS_DIR"]

from backtest_trend import run_backtest
import backtest_trend
from symbols_config import SYMBOLS
from fetch_4h_data import INTERVAL
from regime_filter import compute_btc_regime, filter_trades_by_regime

T3_FAST_RANGE = [8, 12, 16]
T3_SLOW_RANGE = [21, 25, 30]
ADX_THRESHOLD_RANGE = [20.0, 25.0, 30.0]
STOP_LOSS_RANGE = [2.0, 3.0, 4.0]

MIN_TRADES = 40
MIN_AVG_RETURN_PCT = 0.3  # realistischer fuer Trendfolge mit niedriger Win Rate - 1.0 war zu streng
MIN_SYMBOLS_CONTRIBUTING = 5
MIN_HISTORY_DAYS = 730  # ca. 2 Jahre - zeitraum-basiert statt Kerzenzahl,
                         # damit es unabhaengig vom Zeitrahmen (15m/1h/4h) funktioniert


def load_all_symbol_data() -> dict:
    """Laedt CSVs, filtert Symbole mit zu kurzer Zeitspanne (nicht Kerzenzahl,
    da 15m-Daten 4x mehr Kerzen pro Tag haben als 1h-Daten)."""
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


def get_trades_for_symbol(price_df: pd.DataFrame, t3_fast: int, t3_slow: int,
                           adx_threshold: float, stop_loss_pct: float) -> pd.DataFrame:
    if t3_fast >= t3_slow:
        return pd.DataFrame()
    return run_backtest(
        price_df,
        t3_fast_length=t3_fast,
        t3_slow_length=t3_slow,
        adx_threshold=adx_threshold,
        stop_loss_pct=stop_loss_pct,
    )


def calculate_robustness_score(row: dict) -> float:
    drawdown_penalty = abs(row["max_drawdown_pct"]) if row["max_drawdown_pct"] != 0 else 1.0
    return round((row["avg_return_pct"] * (row["num_trades"] ** 0.5)) / drawdown_penalty, 3)


def evaluate_combination_multi(all_data: dict, t3_fast: int, t3_slow: int,
                                adx_threshold: float, stop_loss_pct: float) -> dict:
    if t3_fast >= t3_slow:
        return None

    all_trades = []
    contributing_symbols = 0

    for symbol, price_df in all_data.items():
        trades = get_trades_for_symbol(price_df, t3_fast, t3_slow, adx_threshold, stop_loss_pct)
        if not trades.empty:
            trades = trades.copy()
            trades["symbol"] = symbol
            all_trades.append(trades)
            contributing_symbols += 1

    if not all_trades:
        return None

    combined = pd.concat(all_trades, ignore_index=True)

    # Markt-Regime-Filter: nur Trades behalten, die waehrend eines
    # BTC-Aufwaertstrends eroeffnet wurden (reduziert Klumpenrisiko bei
    # breiten Markteinbruechen deutlich, siehe Diskussion im Chat)
    if "BTCUSDT" in all_data:
        btc_regime = compute_btc_regime(all_data["BTCUSDT"])
        combined = filter_trades_by_regime(combined, btc_regime)
        contributing_symbols = combined["symbol"].nunique() if not combined.empty else 0

    if combined.empty or len(combined) < MIN_TRADES or contributing_symbols < MIN_SYMBOLS_CONTRIBUTING:
        return None

    win_rate = (combined["pnl_pct"] > 0).mean() * 100
    total_return = combined["pnl_pct"].sum()
    avg_return = combined["pnl_pct"].mean()

    if avg_return < MIN_AVG_RETURN_PCT:
        return None

    cum_returns = combined["pnl_pct"].cumsum()
    max_drawdown = (cum_returns - cum_returns.cummax()).min()

    result = {
        "t3_fast": t3_fast,
        "t3_slow": t3_slow,
        "adx_threshold": adx_threshold,
        "stop_loss_pct": stop_loss_pct,
        "num_trades": len(combined),
        "num_symbols": contributing_symbols,
        "win_rate": round(win_rate, 1),
        "total_return_pct": round(total_return, 2),
        "avg_return_pct": round(avg_return, 2),
        "max_drawdown_pct": round(max_drawdown, 2),
    }
    result["robustness_score"] = calculate_robustness_score(result)
    return result


def run_multi_optimisation(all_data: dict) -> pd.DataFrame:
    results = []
    combinations = list(itertools.product(T3_FAST_RANGE, T3_SLOW_RANGE, ADX_THRESHOLD_RANGE, STOP_LOSS_RANGE))

    print(f"Teste {len(combinations)} Kombinationen auf {len(all_data)} Symbolen...\n")

    for t3_fast, t3_slow, adx_threshold, stop_loss_pct in combinations:
        result = evaluate_combination_multi(all_data, t3_fast, t3_slow, adx_threshold, stop_loss_pct)
        if result is not None:
            results.append(result)

    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values("robustness_score", ascending=False).reset_index(drop=True)
    return df


if __name__ == "__main__":
    all_data = load_all_symbol_data()

    if not all_data:
        print("Keine Daten gefunden. Erst 'python3 ../../shared/fetch_multi_data.py' ausfuehren.")
        exit()

    print(f"Geladene Symbole: {list(all_data.keys())}\n")

    results = run_multi_optimisation(all_data)

    if results.empty:
        print("Keine robuste Kombination gefunden. MIN_TRADES oder",
              "MIN_SYMBOLS_CONTRIBUTING senken und erneut versuchen.")
    else:
        print(f"{len(results)} robuste Kombinationen gefunden.\n")
        print(results.head(15).to_string(index=False))

        output_path = os.path.join(RESULTS_DIR, "multi_symbol_optimisation_results.csv")
        results.to_csv(output_path, index=False)
        print(f"\nGespeichert als: {output_path}")

        best = results.iloc[0]
        print(f"\nBeste Kombination:")
        print(f"  T3 Fast: {best['t3_fast']}  |  T3 Slow: {best['t3_slow']}  |  "
              f"ADX-Schwelle: {best['adx_threshold']}  |  Stop-Loss: {best['stop_loss_pct']}%")
        print(f"  -> {best['num_trades']} Trades ueber {best['num_symbols']} Symbole, "
              f"{best['win_rate']}% Win Rate, {best['total_return_pct']}% Gesamtertrag")

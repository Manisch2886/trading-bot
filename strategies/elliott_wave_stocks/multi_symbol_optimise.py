"""
Phase 3d - Multi-Symbol Optimierung
======================================
Fuehrt die Elliott-Wave-Pipeline (Zigzag -> Wellenerkennung ->
Bereinigung -> Backtest) fuer JEDE Parameter-Kombination auf ALLEN
geladenen Symbolen aus und fasst die Trades zusammen.

Vorteil gegenueber Single-Symbol: die Gesamtzahl an Trades steigt
deutlich, ohne dass wir bei einem einzelnen Markt auf sehr seltene
Ereignisse angewiesen sind. Ein Muster, das auf mehreren, voneinander
unabhaengigen Maerkten funktioniert, ist ein deutlich staerkeres
Robustheits-Signal als eines, das nur auf einem Markt funktioniert.
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

from zigzag_indicator import calculate_zigzag
from elliott_wave_counter import find_impulse_waves, remove_overlapping
from backtest_elliott import run_backtest
import backtest_elliott

from fetch_stock_data import INTERVAL
from stocks_symbols_config import SYMBOLS

DEVIATION_RANGE = [2.0, 3.0, 4.0, 5.0]
STOP_LOSS_RANGE = [2.0, 3.0, 5.0, 8.0]  # erweitert (bis 8%) nach Erkenntnis aus
                                          # compare_exit_rules.py, dass breitere Stops
                                          # bei Aktien-Trendfolge besser abschneiden koennen
TAKE_PROFIT_FIB_RANGE = [0.236, 0.382, 0.5]

MIN_TRADES = 150           # bei ~150 Symbolen angemessen ansetzen (weitere Erhoehung ggue. Top 100)
MIN_AVG_RETURN_PCT = 2.0
MIN_SYMBOLS_CONTRIBUTING = 22  # Muster soll auf einer breiten Basis an Aktien funktionieren
MIN_HISTORY_DAYS = 1825    # ca. 5 Jahre - zeitraum- statt kerzenzahl-basiert (Tages- statt
                            # Stundenkerzen haben eine ganz andere Kerzendichte pro Kalendertag)
RECENT_YEARS_ONLY = 10      # begrenzt die Historie auf die letzten N Jahre - reduziert
                            # Survivorship Bias (vor 60+ Jahren waren die heutigen
                            # Top-25-Werte grossteils noch nicht die groessten Firmen der
                            # Welt; vor 10 Jahren ist die Auswahl realistischer). None = kein Limit.


def load_all_symbol_data() -> dict:
    """Laedt alle zuvor mit fetch_stock_data.py heruntergeladenen CSVs.
    Aktien mit zu kurzer Historie werden uebersprungen (z.B. juengere
    Boersengaenge), da sie fuer Optimierung und Walk-Forward-Validierung
    nicht genug Datenbasis bieten. Die Historie wird zudem auf die
    letzten RECENT_YEARS_ONLY Jahre begrenzt (siehe Kommentar oben)."""
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

        if RECENT_YEARS_ONLY is not None:
            cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)
            df = df[df["open_time"] >= cutoff].reset_index(drop=True)

        timespan_days = (df["open_time"].max() - df["open_time"].min()).days
        if timespan_days < MIN_HISTORY_DAYS:
            print(f"Hinweis: {symbol} deckt nur {timespan_days} Tage ab "
                  f"(< {MIN_HISTORY_DAYS} noetig), wird uebersprungen.")
            continue

        data[symbol] = df
    return data


def get_trades_for_symbol(price_df: pd.DataFrame, deviation_pct: float, use_take_profit: bool = True) -> pd.DataFrame:
    """Fuehrt Zigzag -> Wellenerkennung -> Bereinigung -> Backtest fuer ein Symbol aus."""
    zigzag = calculate_zigzag(price_df, deviation_pct=deviation_pct)
    if len(zigzag) < 6:
        return pd.DataFrame()

    impulses = find_impulse_waves(zigzag, min_fib_score=0.3)
    if impulses.empty:
        return pd.DataFrame()

    impulses = remove_overlapping(impulses)
    impulses = impulses[impulses["direction"] == "bearish"]  # Long-only
    if impulses.empty:
        return pd.DataFrame()

    return run_backtest(price_df, impulses, use_take_profit=use_take_profit)


def calculate_robustness_score(row: dict) -> float:
    drawdown_penalty = abs(row["max_drawdown_pct"]) if row["max_drawdown_pct"] != 0 else 1.0
    return round((row["avg_return_pct"] * (row["num_trades"] ** 0.5)) / drawdown_penalty, 3)


def evaluate_combination_multi(all_data: dict, deviation_pct: float, stop_loss_pct: float,
                                take_profit_fib: float, use_take_profit: bool = True) -> dict:
    """Testet eine Parameter-Kombination auf allen Symbolen und fasst die Trades zusammen."""
    backtest_elliott.STOP_LOSS_PCT = stop_loss_pct
    backtest_elliott.TAKE_PROFIT_FIB = take_profit_fib

    all_trades = []
    contributing_symbols = 0

    for symbol, price_df in all_data.items():
        trades = get_trades_for_symbol(price_df, deviation_pct, use_take_profit)
        if not trades.empty:
            trades = trades.copy()
            trades["symbol"] = symbol
            all_trades.append(trades)
            contributing_symbols += 1

    if not all_trades:
        return None

    combined = pd.concat(all_trades, ignore_index=True)

    if len(combined) < MIN_TRADES:
        return None
    if contributing_symbols < MIN_SYMBOLS_CONTRIBUTING:
        return None

    win_rate = (combined["pnl_pct"] > 0).mean() * 100
    total_return = combined["pnl_pct"].sum()
    avg_return = combined["pnl_pct"].mean()

    if avg_return < MIN_AVG_RETURN_PCT:
        return None

    cum_returns = combined["pnl_pct"].cumsum()
    max_drawdown = (cum_returns - cum_returns.cummax()).min()

    result = {
        "deviation_pct": deviation_pct,
        "stop_loss_pct": stop_loss_pct,
        "take_profit_fib": take_profit_fib if use_take_profit else None,
        "use_take_profit": use_take_profit,
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

    # Kombinationen bewusst so aufgebaut, dass take_profit_fib nur variiert
    # wird, wenn use_take_profit=True ist (sonst waere der Wert wirkungslos
    # und wir wuerden identische Backtests mehrfach unnoetig wiederholen).
    combinations = []
    for deviation_pct in DEVIATION_RANGE:
        for stop_loss_pct in STOP_LOSS_RANGE:
            for take_profit_fib in TAKE_PROFIT_FIB_RANGE:
                combinations.append((deviation_pct, stop_loss_pct, take_profit_fib, True))
            combinations.append((deviation_pct, stop_loss_pct, None, False))

    print(f"Teste {len(combinations)} Kombinationen auf {len(all_data)} Symbolen...\n")

    for deviation_pct, stop_loss_pct, take_profit_fib, use_take_profit in combinations:
        result = evaluate_combination_multi(all_data, deviation_pct, stop_loss_pct,
                                             take_profit_fib, use_take_profit)
        if result is not None:
            results.append(result)

    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values("robustness_score", ascending=False).reset_index(drop=True)
    return df


if __name__ == "__main__":
    all_data = load_all_symbol_data()

    if not all_data:
        print("Keine Daten gefunden. Erst 'python3 fetch_multi_data.py' ausfuehren.")
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
        print(f"  Zigzag: {best['deviation_pct']}%  |  Stop-Loss: {best['stop_loss_pct']}%  |  "
              f"Take-Profit Fib: {best['take_profit_fib']}")
        print(f"  -> {best['num_trades']} Trades ueber {best['num_symbols']} Symbole, "
              f"{best['win_rate']}% Win Rate, {best['total_return_pct']}% Gesamtertrag")

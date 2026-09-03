"""
Phase 1 - Multi-Symbol Optimierung: RSI-2 Mean-Reversion
==============================================================
Analog zum Muster der bestehenden Bots (siehe elliott_wave_stocks/
multi_symbol_optimise.py): fuehrt die Backtest-Pipeline fuer jede
Parameter-Kombination auf ALLEN Symbolen aus und fasst die Trades
zusammen. Testet Connors' genannten RSI-Schwellenbereich (5-10) sowie
"kein Stop-Loss" gegen feste Stop-Loss-Werte (siehe backtest_rsi2.py,
Punkt 4 im Modul-Docstring fuer die Einordnung dazu).

Nutzt DASSELBE Universum wie elliott_wave_stocks (S&P-500 Top 150,
config/sp500_top150.txt) und dieselben bereits vorhandenen CSV-Kursdaten
in data/ - keine neue Datenquelle noetig.
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

from backtest_rsi2 import compute_indicators, run_backtest, SMA_TREND_PERIOD
from stocks_symbols_config import SYMBOLS

INTERVAL = "1d"

RSI_THRESHOLD_RANGE = [5.0, 10.0]     # Connors nennt 5-10 als ueblichen Bereich
STOP_LOSS_RANGE = [None, 5.0, 8.0]    # None = kein Stop (Connors-Standardversion)

MIN_TRADES = 150             # analog elliott_wave_stocks (gleiches Universum, gleiche Groessenordnung)
MIN_AVG_RETURN_PCT = 0.0     # RSI-2 ist eine Kurzfrist-Strategie mit kleinen Einzel-PnLs (typ. < 1%
                              # pro Trade) - pnl_pct hat Handelskosten bereits abgezogen, daher ist
                              # "positiv" schon ein echter Netto-Edge (deutlich niedrigere Schwelle
                              # als bei den Elliott-Wave-Bots mit 2.0; ein Test mit 0.2 filterte im
                              # In-Sample-Teilfenster des Walk-Forward-Splits ALLE Kombinationen weg,
                              # obwohl mehrere Tausend Trades und ein positiver Erwartungswert vorlagen)
MIN_SYMBOLS_CONTRIBUTING = 22
MIN_HISTORY_DAYS = 1825      # ca. 5 Jahre, zeitraum- statt kerzenzahl-basiert (siehe Projekt-Prinzipien)
RECENT_YEARS_ONLY = 10       # reduziert Survivorship Bias, wie bei elliott_wave_stocks


def load_all_symbol_data() -> dict:
    """Laedt die vollen CSVs (KEINE Kappung auf RECENT_YEARS_ONLY vor der
    Indikator-Berechnung, siehe backtest_rsi2.compute_indicators) und
    berechnet die Indikatoren direkt hier. Gibt pro Symbol (df_mit_indikatoren,
    entry_cutoff) zurueck - entry_cutoff filtert nur die generierten TRADES
    auf die letzten RECENT_YEARS_ONLY Jahre, nicht die Indikator-Basis."""
    data = {}
    for symbol in SYMBOLS:
        csv_path = os.path.join(DATA_DIR, f"{symbol}_{INTERVAL}.csv")
        try:
            df = pd.read_csv(csv_path, parse_dates=["open_time"])
        except FileNotFoundError:
            continue
        if df.empty:
            continue

        timespan_days = (df["open_time"].max() - df["open_time"].min()).days
        if timespan_days < MIN_HISTORY_DAYS:
            continue

        entry_cutoff = None
        if RECENT_YEARS_ONLY is not None:
            entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)

        df_ind = compute_indicators(df)
        data[symbol] = (df_ind, entry_cutoff)
    return data


def get_trades_for_symbol(df_ind: pd.DataFrame, entry_cutoff, rsi_threshold: float,
                           stop_loss_pct: float, max_hold_days: int = None) -> pd.DataFrame:
    kwargs = {} if max_hold_days is None else {"max_hold_days": max_hold_days}
    return run_backtest(df_ind, rsi_threshold=rsi_threshold, stop_loss_pct=stop_loss_pct,
                         entry_cutoff=entry_cutoff, **kwargs)


def calculate_robustness_score(row: dict) -> float:
    drawdown_penalty = abs(row["max_drawdown_pct"]) if row["max_drawdown_pct"] != 0 else 1.0
    return round((row["avg_return_pct"] * (row["num_trades"] ** 0.5)) / drawdown_penalty, 3)


def evaluate_combination_multi(all_data: dict, rsi_threshold: float, stop_loss_pct: float) -> dict:
    all_trades = []
    contributing_symbols = 0

    for symbol, (df_ind, entry_cutoff) in all_data.items():
        trades = get_trades_for_symbol(df_ind, entry_cutoff, rsi_threshold, stop_loss_pct)
        if not trades.empty:
            trades = trades.copy()
            trades["symbol"] = symbol
            all_trades.append(trades)
            contributing_symbols += 1

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
        "rsi_threshold": rsi_threshold,
        "stop_loss_pct": stop_loss_pct if stop_loss_pct is not None else "kein Stop",
        "num_trades": len(combined),
        "num_symbols": contributing_symbols,
        "win_rate": round(win_rate, 1),
        "total_return_pct": round(total_return, 2),
        "avg_return_pct": round(avg_return, 2),
        "avg_holding_days": round(combined["holding_days"].mean(), 1),
        "max_drawdown_pct": round(max_drawdown, 2),
    }
    result["robustness_score"] = calculate_robustness_score(result)
    return result


def run_multi_optimisation(all_data: dict) -> pd.DataFrame:
    results = []
    combinations = [(r, s) for r in RSI_THRESHOLD_RANGE for s in STOP_LOSS_RANGE]

    print(f"Teste {len(combinations)} Kombinationen auf {len(all_data)} Symbolen...\n")
    for rsi_threshold, stop_loss_pct in combinations:
        result = evaluate_combination_multi(all_data, rsi_threshold, stop_loss_pct)
        if result is not None:
            results.append(result)

    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values("robustness_score", ascending=False).reset_index(drop=True)
    return df


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden.")
        exit()

    print(f"Geladene Symbole: {len(all_data)}\n")
    results = run_multi_optimisation(all_data)

    if results.empty:
        print("Keine robuste Kombination gefunden.")
    else:
        print(results.to_string(index=False))
        output_path = os.path.join(RESULTS_DIR, "multi_symbol_optimisation_results.csv")
        results.to_csv(output_path, index=False)
        print(f"\nGespeichert als: {output_path}")

"""
Phase 1 - Multi-Symbol Optimierung: Bollinger-Band-Squeeze-Breakout
==========================================================================
Analog zum Muster von rsi2_mean_reversion/multi_symbol_optimise.py: fuehrt
die Backtest-Pipeline fuer jede Parameter-Kombination auf ALLEN Symbolen aus.

Testet in dieser ersten Runde NUR den Stop-Loss (siehe backtest_breakout.py,
Punkt 3a) - Squeeze-Lookback (126 Tage) und Squeeze-Perzentil (25) bleiben
wie angefragt erstmal auf dem Startwert fixiert, werden spaeter separat
optimiert. Der Volumen-Filter (Punkt 4) wird separat in
experiment_false_breakout_filter.py getestet, nicht hier in der Haupt-Grid-Suche.

Nutzt DASSELBE Universum wie elliott_wave_stocks/rsi2_mean_reversion
(S&P-500 Top 150, config/sp500_top150.txt) und dieselben bereits
vorhandenen CSV-Kursdaten in data/ - keine neue Datenquelle noetig.
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
from stocks_symbols_config import SYMBOLS

INTERVAL = "1d"

STOP_LOSS_RANGE = [3.0, 5.0, 8.0, None]  # None = kein Stop, zum Vergleich mit einbezogen

MIN_TRADES = 100              # Breakout-Signale sind seltener als RSI-2-Dips (laengere Haltedauer,
                                # strengere Vorbedingung) - niedrigere Schwelle als RSI-2 (150)
MIN_AVG_RETURN_PCT = 0.0      # positiv = echter Netto-Edge nach Kosten (siehe RSI-2-Lehre zu MIN_AVG_RETURN_PCT)
MIN_SYMBOLS_CONTRIBUTING = 15
MIN_HISTORY_DAYS = 1825       # ca. 5 Jahre, zeitraum- statt kerzenzahl-basiert
RECENT_YEARS_ONLY = 10        # reduziert Survivorship Bias, wie bei den anderen Aktien-Bots


def load_all_symbol_data() -> dict:
    """Laedt die vollen CSVs (KEINE Kappung auf RECENT_YEARS_ONLY vor der
    Indikator-Berechnung) - der 126-Tage-Squeeze-Vorlauf braucht genug
    Vorgeschichte. entry_cutoff filtert nur die generierten TRADES."""
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


def get_trades_for_symbol(df_ind: pd.DataFrame, entry_cutoff, stop_loss_pct: float,
                           max_hold_days: int = None, use_volume_filter: bool = False) -> pd.DataFrame:
    kwargs = {} if max_hold_days is None else {"max_hold_days": max_hold_days}
    return run_backtest(df_ind, stop_loss_pct=stop_loss_pct, entry_cutoff=entry_cutoff,
                         use_volume_filter=use_volume_filter, **kwargs)


def calculate_robustness_score(row: dict) -> float:
    drawdown_penalty = abs(row["max_drawdown_pct"]) if row["max_drawdown_pct"] != 0 else 1.0
    return round((row["avg_return_pct"] * (row["num_trades"] ** 0.5)) / drawdown_penalty, 3)


def evaluate_combination_multi(all_data: dict, stop_loss_pct: float,
                                max_hold_days: int = None, use_volume_filter: bool = False) -> dict:
    all_trades = []
    contributing_symbols = 0

    for symbol, (df_ind, entry_cutoff) in all_data.items():
        trades = get_trades_for_symbol(df_ind, entry_cutoff, stop_loss_pct, max_hold_days, use_volume_filter)
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
    print(f"Teste {len(STOP_LOSS_RANGE)} Stop-Loss-Werte auf {len(all_data)} Symbolen...\n")
    for stop_loss_pct in STOP_LOSS_RANGE:
        result = evaluate_combination_multi(all_data, stop_loss_pct)
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

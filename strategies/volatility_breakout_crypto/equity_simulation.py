"""
Phase 3 - Equity-Kurven-Simulation (realistisches Portfolio): Volatility Breakout Krypto
======================================================================================================
Identisches Prinzip wie bei den bestehenden Bots. Startwerte wie angefragt:
10% Allokation, Limit 8.
"""

import os
import sys
import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

from multi_symbol_optimise import load_all_symbol_data, get_trades_for_symbol

# Die Strategie-Parameter kommen DIREKT aus live_params.py - derselben Datei,
# aus der auch forward_test.py liest (Muster aus PR #31). Vorher standen sie
# hier ein zweites Mal als eigene Konstanten. Dass beide Seiten denselben Wert
# trugen, war kein Schutz, sondern Zufall: die Doppelfuehrung faellt erst bei
# der ersten Parameter-Aenderung auf, die nur eine Seite erreicht - genau so
# ist die USE_TAKE_PROFIT-Abweichung beim Aktien-Elliott-Bot entstanden
# (Sync-Check, PR #24). live_params.py importiert selbst nichts, ein
# Importzyklus ist damit ausgeschlossen.
# BTC_REGIME_FILTER_ENABLED wird seit PR #57 MIT importiert und unten auch
# angewendet. Frueher stand hier, das Flag sei "kein fehlender Wert, sondern
# fehlendes VERHALTEN" - richtig beobachtet, aber eben eine Luecke: live
# blockiert forward_test.py neue Einstiege im BTC-Abwaertsregime, der
# Backtest tat das nicht. Damit beschrieb diese Datei eine Strategie, die so
# nicht laeuft - derselbe Fehlertyp wie die USE_TAKE_PROFIT-Abweichung beim
# Aktien-Elliott-Bot (Sync-Check, PR #24). Der letzte bekannte
# Sync-Unterschied dieses Bots ist damit geschlossen.
from live_params import (STOP_LOSS_PCT, MAX_CONCURRENT_POSITIONS,
                          BTC_REGIME_FILTER_ENABLED,
                          ALLOCATION_PCT as _ALLOCATION_PCT_PROZENT)
# Dieselben Funktionen, die forward_test.py live benutzt - nicht nachgebaut.
from regime_filter import compute_btc_regime, filter_trades_by_regime

STARTING_CAPITAL = 10_000.0
# EINHEITEN: live_params.py notiert die Allokation in PROZENT (10), dieses
# Skript rechnet mit dem ANTEIL (0.10) - siehe Sync-Check (PR #24).
ALLOCATION_PCT = _ALLOCATION_PCT_PROZENT / 100


def collect_all_trades(all_data: dict, stop_loss_pct: float = None, max_hold_days: int = None,
                        use_volume_filter: bool = False) -> pd.DataFrame:
    all_trades = []
    for symbol, price_df in all_data.items():
        trades = get_trades_for_symbol(price_df, stop_loss_pct, max_hold_days, use_volume_filter)
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


def apply_btc_regime_filter(trades: pd.DataFrame, all_data: dict) -> pd.DataFrame:
    """Entfernt Trades, die im BTC-Abwaertsregime eingestiegen waeren.

    Das ist die Backtest-Entsprechung dessen, was forward_test.py live tut:
    dort blockiert `BTC_REGIME_FILTER_ENABLED and not btc_regime_bullish`
    NEUE Einstiege, wenn BTC selbst (eigener taeglicher SuperTrend) faellt.
    Live wird dafuer nur die JEWEILS LETZTE Kerze geprueft; ueber eine
    Historie ist die Entsprechung genau `filter_trades_by_regime()`, das je
    Trade das zum Einstiegszeitpunkt geltende Regime nachschlaegt. Beide
    Funktionen kommen unveraendert aus regime_filter.py.

    BEWUSST HIER und nicht in collect_all_trades(): drei Experiment-Skripte
    dieses Bots (experiment_btc_regime_filter.py,
    experiment_2022_stress_with_btc_filter.py, ...robustness.py) holen sich
    ueber genau jene Funktion ihren UNGEFILTERTEN Vergleichsdatensatz
    (`trades_no_filter`). Den Filter dort einzubauen wuerde diese Experimente
    still sinnlos machen, statt sie scheitern zu lassen.

    Fehlt BTCUSDT, wird NICHT stillschweigend ungefiltert weitergerechnet -
    das waere genau die Luecke, die hier geschlossen wird, nur unsichtbar.
    """
    if not BTC_REGIME_FILTER_ENABLED:
        return trades

    btc = all_data.get("BTCUSDT")
    if btc is None:
        raise SystemExit(
            "BTC_REGIME_FILTER_ENABLED ist aktiv, aber BTCUSDT fehlt in den "
            "Kursdaten - der Regimefilter ist nicht anwendbar. Erst "
            "'python3 fetch_1d_data.py' ausfuehren; ein Lauf ohne Filter "
            "wuerde eine andere Strategie beschreiben als die laufende.")

    vorher = len(trades)
    gefiltert = filter_trades_by_regime(trades, compute_btc_regime(btc))
    print(f"BTC-Regimefilter aktiv: {vorher - len(gefiltert)} von {vorher} Trades "
          f"entfernt (Einstieg im BTC-Abwaertsregime), {len(gefiltert)} bleiben.")
    return gefiltert


def simulate_portfolio(trades: pd.DataFrame, starting_capital: float,
                        allocation_pct: float, max_concurrent_positions: int = None) -> dict:
    events = []
    for idx, trade in trades.iterrows():
        events.append((trade["entry_time"], "entry", idx))
        events.append((trade["exit_time"], "exit", idx))
    events.sort(key=lambda e: (e[0], e[1] != "exit"))

    capital = starting_capital
    open_positions = {}
    skipped_trades = []
    executed_trades = []
    equity_curve = []

    for time, event_type, idx in events:
        trade = trades.loc[idx]

        if event_type == "entry":
            if max_concurrent_positions is not None and len(open_positions) >= max_concurrent_positions:
                skipped_trades.append(idx)
                continue

            bound_capital = sum(open_positions.values())
            free_capital = capital - bound_capital
            allocation = capital * allocation_pct

            if allocation > free_capital:
                skipped_trades.append(idx)
                continue

            open_positions[idx] = allocation
            executed_trades.append(idx)

        elif event_type == "exit":
            if idx not in open_positions:
                continue
            allocation = open_positions.pop(idx)
            pnl_pct = trade["pnl_pct"]
            result_value = allocation * (1 + pnl_pct / 100)
            capital += (result_value - allocation)

            equity_curve.append({
                "time": time, "symbol": trade["symbol"], "pnl_pct": pnl_pct,
                "allocation": round(allocation, 2), "capital_after": round(capital, 2),
            })

    equity_df = pd.DataFrame(equity_curve)
    return {
        "final_capital": round(capital, 2),
        "num_executed": len(executed_trades),
        "num_skipped": len(skipped_trades),
        "equity_curve": equity_df,
    }


def calculate_max_drawdown(equity_df: pd.DataFrame, starting_capital: float) -> float:
    if equity_df.empty:
        return 0.0
    capital_series = pd.concat([pd.Series([starting_capital]), equity_df["capital_after"]], ignore_index=True)
    running_max = capital_series.cummax()
    drawdown_pct = (capital_series - running_max) / running_max * 100
    return round(drawdown_pct.min(), 2)


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden.")
        exit()

    trades = collect_all_trades(all_data, STOP_LOSS_PCT)
    if trades.empty:
        print("Keine Trades fuer diese Parameter-Kombination gefunden.")
        exit()

    print(f"{len(trades)} Trades ueber alle Symbole gefunden.")
    trades = apply_btc_regime_filter(trades, all_data)
    if trades.empty:
        print("Nach dem BTC-Regimefilter bleibt kein Trade uebrig.")
        exit()
    print()
    result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)

    print("=" * 55)
    print("PORTFOLIO-SIMULATION")
    print("=" * 55)
    print(f"Startkapital:            {STARTING_CAPITAL:,.2f}")
    print(f"Endkapital:              {result['final_capital']:,.2f}")
    total_return_pct = (result["final_capital"] / STARTING_CAPITAL - 1) * 100
    print(f"Gesamtrendite:           {total_return_pct:.2f}%")
    print(f"Ausgefuehrte Trades:     {result['num_executed']}")
    print(f"Uebersprungene Trades:   {result['num_skipped']}")
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    print(f"Max Drawdown (Kapital):  {max_dd:.2f}%")

    if not result["equity_curve"].empty:
        output_path = os.path.join(RESULTS_DIR, "equity_curve.csv")
        result["equity_curve"].to_csv(output_path, index=False)
        print(f"\nGespeichert als: {output_path}")

"""
Phase 3 - Equity-Kurven-Simulation (realistisches Portfolio): Turtle Soup (Aktien)
================================================================================================
Identisches Prinzip wie bei den anderen Bots.

Die urspruenglichen Startwerte (10 % Allokation, Limit 8, "identisch zu den
anderen Aktien-Bots" fuer die Vergleichbarkeit) gelten hier NICHT mehr: seit
2026-09-04 laeuft der Bot live mit 2 % Allokation und OHNE Positionslimit,
und dieses Skript liest die Werte jetzt direkt aus live_params.py. Die
Vergleichbarkeit mit den anderen Aktien-Bots wird damit bewusst aufgegeben -
ein Backtest, der eine andere Konfiguration rechnet als der laufende Bot,
ist die teurere Ungenauigkeit. Siehe Kommentar am Import unten.
"""

import os
import sys
import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
from data_quality import melde_uebersprungene_balken
_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

from multi_symbol_optimise import load_all_symbol_data, get_trades_for_symbol

# Die Parameter kommen DIREKT aus live_params.py - derselben Datei, aus der
# auch forward_test.py liest (Muster aus PR #31/#38/#39). Vorher standen sie
# hier ein zweites Mal als eigene Konstanten, und zwei davon waren
# auseinandergelaufen (Sync-Check, PR #24):
#   ALLOCATION_PCT            10 % hier gegen 2 % live
#   MAX_CONCURRENT_POSITIONS  8 hier gegen None (unbegrenzt) live
#
# AUFGEGEBENE BEGRUENDUNG - bitte nicht versehentlich zurueckdrehen: das
# Limit 8 stand hier als bewusster "Startwert, identisch zu den anderen
# Aktien-Bots", also aus Gruenden der Vergleichbarkeit zwischen den Bots.
# Diese Motivation gilt ab jetzt nicht mehr; massgeblich ist der
# TATSAECHLICHE Live-Wert. Ein Backtest, der eine andere Konfiguration
# rechnet als der laufende Bot, ist die teurere Ungenauigkeit als eine
# eingeschraenkte Vergleichbarkeit zwischen Bots. live_params.py begruendet
# das unbegrenzte Limit inhaltlich: bei 2 % Allokation saettigt die
# Kapitalbindung rechnerisch bei ca. 50 offenen Positionen, ein Limit waere
# dort kein Risikohebel mehr, sondern wuerde nur Signale blockieren
# (PROTOTYPE_FINDINGS.md, Abschnitt 8b/8c).
#
# DONCHIAN_PERIOD und STOP_MODE waren bereits identisch (10 bzw. None -
# "kein Stop" ist die validierte Kombination, kein fehlender Wert); sie
# werden mit umgestellt, damit die Doppelfuehrung vollstaendig verschwindet.
# live_params.py importiert selbst nichts, ein Importzyklus ist ausgeschlossen.
from live_params import (DONCHIAN_PERIOD, STOP_MODE, MAX_CONCURRENT_POSITIONS,
                          ALLOCATION_PCT as _ALLOCATION_PCT_PROZENT)

STARTING_CAPITAL = 10_000.0
# EINHEITEN: live_params.py notiert die Allokation in PROZENT (2), dieses
# Skript rechnet mit dem ANTEIL (0.02) - deshalb die Umrechnung statt eines
# direkten Imports. shared/portfolio_overview.py liest ALLOCATION_PCT von hier
# und erwartet ebenfalls den Anteil.
ALLOCATION_PCT = _ALLOCATION_PCT_PROZENT / 100


def collect_all_trades(all_data: dict, donchian_period: int, stop_mode=None) -> pd.DataFrame:
    all_trades = []
    for symbol, (df, entry_cutoff) in all_data.items():
        trades = get_trades_for_symbol(df, entry_cutoff, donchian_period, stop_mode)
        if not trades.empty:
            trades = trades.copy()
            trades["symbol"] = symbol
            all_trades.append(trades)
    if not all_trades:
        return pd.DataFrame()
    combined = pd.concat(all_trades, ignore_index=True)
    combined["entry_time"] = pd.to_datetime(combined["entry_time"])
    combined["exit_time"] = pd.to_datetime(combined["exit_time"])

    # Trades ohne Ein- oder Ausstiegskurs streichen und die Streichung
    # MELDEN. Ein einziger fehlender Kurs macht sonst die gesamte
    # Kapitalkurve unbrauchbar (simulate_portfolio rechnet ihn ins
    # Kapital, ab da ist jede Folgezahl NaN) - und der Projekt-Score
    # merkt nichts davon, weil pandas beim Mitteln NaN ueberspringt.
    # Genau so ist es beim leeren letzten Balken von APH passiert.
    # Siehe shared/data_quality.py.
    preisspalten = [s for s in ("entry_price", "exit_price") if s in combined.columns]
    if preisspalten:
        luecke = combined[preisspalten].isna().any(axis=1)
        if luecke.any():
            for symbol, anzahl in combined.loc[luecke, "symbol"].value_counts().items():
                melde_uebersprungene_balken(symbol, int(anzahl), "Trade ohne Kurs gestrichen")
            combined = combined[~luecke]

    return combined.sort_values("entry_time").reset_index(drop=True)


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

    trades = collect_all_trades(all_data, DONCHIAN_PERIOD, STOP_MODE)
    if trades.empty:
        print("Keine Trades fuer diese Parameter-Kombination gefunden.")
        exit()

    print(f"{len(trades)} Trades ueber alle Symbole gefunden.\n")
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

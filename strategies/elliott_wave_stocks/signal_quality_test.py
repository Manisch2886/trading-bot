"""
Signal-Qualitaets-Test (isoliert von Kapitaleinsatz)
==========================================================
Der Buy-and-Hold-Vergleich zeigte einen riesigen Renditeunterschied -
aber der ist teilweise nur dadurch erklaerbar, dass die Strategie
kaum Kapital einsetzt (10% pro Trade, meist unbesetzt), waehrend
Buy-and-Hold durchgehend zu 100% investiert ist.

Dieser Test beantwortet eine praezisere Frage: Waere es waehrend
GENAU DERSELBEN Zeitfenster, die die Strategie gewaehlt hat, besser
gewesen, die Aktie einfach passiv zu halten (Kauf bei Einstieg,
Verkauf zum Schlusskurs am Ausstiegstag), statt die aktiven
Stop-Loss-/Take-Profit-Regeln zu nutzen?

Das trennt sauber:
- "Ist unser Timing/Risikomanagement gut?" (diese Frage)
- "Sollte ich ueberhaupt mehr Kapital investiert haben?" (andere Frage,
  vom Buy-and-Hold-Vergleich beantwortet)
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

from multi_symbol_optimise import load_all_symbol_data
from equity_simulation import collect_all_trades, DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB
import backtest_elliott

TRADING_FEE_PCT = backtest_elliott.TRADING_FEE_PCT
SLIPPAGE_PCT = backtest_elliott.SLIPPAGE_PCT


def compute_passive_window_pnl(trades: pd.DataFrame, all_data: dict) -> pd.DataFrame:
    """
    Fuer jeden Strategie-Trade: berechnet, was ein simples Halten
    (Kauf bei Entry, Verkauf zum Schlusskurs am Exit-Tag) waehrend
    GENAU DIESES Zeitfensters gebracht haette - inkl. derselben
    Kostenannahmen wie die Strategie, fuer einen fairen Vergleich.
    """
    trades = trades.copy()
    passive_pnls = []

    for _, trade in trades.iterrows():
        symbol = trade["symbol"]
        df = all_data.get(symbol)
        if df is None:
            passive_pnls.append(None)
            continue

        exit_row = df[df["open_time"] == trade["exit_time"]]
        if exit_row.empty:
            # Falls der exakte Exit-Tag nicht getroffen wird (z.B. Rundungsdifferenzen),
            # den naechstgelegenen Handelstag nehmen
            exit_row = df[df["open_time"] <= trade["exit_time"]].tail(1)

        if exit_row.empty:
            passive_pnls.append(None)
            continue

        passive_exit_price = exit_row["close"].iloc[0]
        passive_pnl = (passive_exit_price - trade["entry_price"]) / trade["entry_price"] * 100
        passive_pnl -= 2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)  # gleiche Kostenannahme wie Strategie
        passive_pnls.append(round(passive_pnl, 2))

    trades["passive_pnl_pct"] = passive_pnls
    return trades


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden.")
        exit()

    trades = collect_all_trades(all_data, DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB)
    if trades.empty:
        print("Keine Trades gefunden.")
        exit()

    trades = compute_passive_window_pnl(trades, all_data)
    trades = trades.dropna(subset=["passive_pnl_pct"])

    print("=" * 60)
    print("SIGNAL-QUALITAETS-TEST: Strategie vs. passives Halten")
    print("(waehrend exakt derselben Zeitfenster)")
    print("=" * 60)
    print(f"\n{len(trades)} vergleichbare Trades\n")

    strategy_total = trades["pnl_pct"].sum()
    passive_total = trades["passive_pnl_pct"].sum()
    strategy_avg = trades["pnl_pct"].mean()
    passive_avg = trades["passive_pnl_pct"].mean()
    strategy_win_rate = (trades["pnl_pct"] > 0).mean() * 100
    passive_win_rate = (trades["passive_pnl_pct"] > 0).mean() * 100

    beat_passive = (trades["pnl_pct"] > trades["passive_pnl_pct"]).mean() * 100

    print(f"{'Metrik':<30}{'Strategie':>15}{'Passives Halten':>20}")
    print(f"{'Summe PnL':<30}{strategy_total:>14.1f}%{passive_total:>19.1f}%")
    print(f"{'Ø PnL pro Trade':<30}{strategy_avg:>14.2f}%{passive_avg:>19.2f}%")
    print(f"{'Win Rate':<30}{strategy_win_rate:>14.1f}%{passive_win_rate:>19.1f}%")
    print(f"\nStrategie schlug passives Halten bei {beat_passive:.1f}% der Trades")

    print("\n" + "=" * 60)
    if strategy_avg > passive_avg:
        print("-> Die aktiven Stop-Loss-/Take-Profit-Regeln schneiden im")
        print("   Schnitt BESSER ab als einfaches Halten derselben Zeitfenster.")
        print("   Das Signal/Risikomanagement traegt also etwas bei.")
    else:
        print("-> Waehrend derselben Zeitfenster waere einfaches Halten im")
        print("   Schnitt GENAUSO GUT oder BESSER gewesen. Das deutet darauf")
        print("   hin, dass die Stop-Loss-/Take-Profit-Regeln eher schaden")
        print("   als nuetzen - das eigentliche 'Signal' (wann einsteigen)")
        print("   koennte trotzdem wertvoll sein, wird hier aber nicht separat")
        print("   getestet (dafuer waere ein Vergleich mit zufaelligen")
        print("   Einstiegszeitpunkten noetig).")

    output_path = os.path.join(RESULTS_DIR, "signal_quality_comparison.csv")
    trades.to_csv(output_path, index=False)
    print(f"\nDetails gespeichert als: {output_path}")

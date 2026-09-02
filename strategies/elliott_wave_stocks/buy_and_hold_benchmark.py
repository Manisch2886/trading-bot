"""
Buy-and-Hold-Vergleich
==========================
Beantwortet die entscheidende Frage bei Aktien-Backtests ueber lange
Zeitraeume: Bringt die Strategie WIRKLICH etwas, oder waere einfaches
Kaufen-und-Halten derselben 25 Aktien ueber denselben Zeitraum fast
genauso gut oder sogar besser gewesen?

Das ist besonders wichtig wegen Survivorship Bias: Die getesteten
Aktien sind die HEUTIGEN groessten S&P-500-Werte - fast zwangslaeufig
Firmen, die ueber die Testperiode stark gewachsen sind. Ein Grossteil
der Rendite kommt moeglicherweise einfach vom generellen Bullenmarkt,
nicht von den Handelssignalen.

Nutzt denselben Zeitraum-Filter (RECENT_YEARS_ONLY) wie
multi_symbol_optimise.py, damit der Vergleich fair ist (gleicher
Zeitraum fuer Strategie und Buy-and-Hold).
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

STARTING_CAPITAL = 10_000.0


def calculate_buy_and_hold(all_data: dict, starting_capital: float) -> dict:
    """
    Gleichgewichtete Buy-and-Hold-Simulation: Startkapital wird zu
    gleichen Teilen auf alle Aktien verteilt, zum jeweils ersten
    verfuegbaren Kurs gekauft, bis zum Ende der Testperiode gehalten.
    """
    num_symbols = len(all_data)
    if num_symbols == 0:
        return None

    capital_per_symbol = starting_capital / num_symbols

    # Tagesweise Portfolio-Wert-Kurve aufbauen (fuer Max-Drawdown-Berechnung)
    daily_values = []
    final_value = 0.0
    skipped_symbols = []

    for symbol, df in all_data.items():
        df = df.sort_values("open_time").reset_index(drop=True)

        # Datenqualitaets-Absicherung: manche Aktien haben bei yfinance
        # vereinzelt fehlerhafte/fehlende Kurse (NaN). Ein einziger NaN-Wert
        # wuerde sonst die GESAMTE Portfolio-Summe unbrauchbar machen - daher
        # wird eine betroffene Aktie hier sauber uebersprungen statt die
        # Berechnung stillschweigend zu vergiften.
        entry_price = df["close"].iloc[0]
        exit_price = df["close"].iloc[-1]
        if pd.isna(entry_price) or pd.isna(exit_price) or entry_price == 0:
            skipped_symbols.append(symbol)
            continue

        shares = capital_per_symbol / entry_price

        symbol_value = df[["open_time", "close"]].copy()
        symbol_value["value"] = symbol_value["close"] * shares
        symbol_value = symbol_value.set_index("open_time")["value"]
        daily_values.append(symbol_value)

        final_value += exit_price * shares

    if skipped_symbols:
        print(f"Hinweis: {len(skipped_symbols)} Aktie(n) wegen fehlerhafter Kursdaten "
              f"uebersprungen: {skipped_symbols}")
        # Der Kapitalanteil uebersprungener Aktien bleibt als unveraendertes
        # Cash im Vergleich - sonst waere das Endkapital kuenstlich zu niedrig
        # (Start- und Endkapital muessen vergleichbar bleiben).
        final_value += capital_per_symbol * len(skipped_symbols)

    # Alle Aktien auf gemeinsame Handelstage zusammenfuehren (leichte
    # Kalenderabweichungen zwischen Boersen/Aktien mit .ffill() ausgleichen)
    portfolio_curve = pd.concat(daily_values, axis=1).sort_index().ffill().sum(axis=1)

    running_max = portfolio_curve.cummax()
    drawdown_pct = (portfolio_curve - running_max) / running_max * 100
    max_drawdown = drawdown_pct.min()

    total_return_pct = (final_value / starting_capital - 1) * 100

    return {
        "final_capital": round(final_value, 2),
        "total_return_pct": round(total_return_pct, 2),
        "max_drawdown_pct": round(max_drawdown, 2),
        "num_symbols": num_symbols,
    }


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    if not all_data:
        print("Keine Daten gefunden.")
        exit()

    result = calculate_buy_and_hold(all_data, STARTING_CAPITAL)

    print("=" * 55)
    print("BUY-AND-HOLD-VERGLEICH")
    print("=" * 55)
    print(f"Startkapital:            {STARTING_CAPITAL:,.2f}")
    print(f"Endkapital (Buy&Hold):   {result['final_capital']:,.2f}")
    print(f"Gesamtrendite:           {result['total_return_pct']:.2f}%")
    print(f"Max Drawdown:            {result['max_drawdown_pct']:.2f}%")
    print(f"Anzahl Aktien:           {result['num_symbols']}")
    print()
    print("Vergleiche dieses Ergebnis mit dem der Elliott-Wave-Strategie")
    print("(equity_simulation.py) - schlaegt die Strategie einfaches Halten")
    print("UND hat sie einen kleineren Max Drawdown? Nur dann traegt sie")
    print("wirklich etwas ueber den generellen Marktrend hinaus bei.")

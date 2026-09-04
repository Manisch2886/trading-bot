"""
Buy-and-Hold-Vergleich: Pair-Rotation (Aktien)
=============================================================
Gleiches Prinzip wie bei den anderen Bots - eigenstaendige Kopie. Nutzt
NICHT das volle 150-Aktien-Universum, sondern die EINDEUTIGEN Assets, die
in den entdeckten Paaren tatsaechlich vorkommen (gleichgewichtet) - fairer
Vergleich, da die Strategie selbst nur in diesem Teil-Universum handelt.
"""

import os
import sys
import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)

from multi_pair_optimise import load_all_symbol_data, get_reference_date, build_pairs

STARTING_CAPITAL = 10_000.0


def calculate_buy_and_hold(symbol_data: dict, pairs: list, starting_capital: float,
                            reference_date: pd.Timestamp) -> dict:
    unique_symbols = sorted({s for a, b, _, _ in pairs for s in (a, b)})
    num_symbols = len(unique_symbols)
    if num_symbols == 0:
        return None
    capital_per_symbol = starting_capital / num_symbols

    daily_values = []
    final_value = 0.0

    for symbol in unique_symbols:
        df = symbol_data[symbol]
        df = df[df["open_time"] >= reference_date].sort_values("open_time").reset_index(drop=True)
        entry_price = df["close"].iloc[0]
        exit_price = df["close"].iloc[-1]

        shares = capital_per_symbol / entry_price
        symbol_value = df[["open_time", "close"]].copy()
        symbol_value["value"] = symbol_value["close"] * shares
        symbol_value = symbol_value.set_index("open_time")["value"]
        daily_values.append(symbol_value)
        final_value += exit_price * shares

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
    symbol_data = load_all_symbol_data()
    reference_date = get_reference_date(symbol_data)
    pairs = build_pairs(symbol_data, reference_date)

    result = calculate_buy_and_hold(symbol_data, pairs, STARTING_CAPITAL, reference_date)
    print("=" * 55)
    print("BUY-AND-HOLD-VERGLEICH (nur Paar-Universum)")
    print("=" * 55)
    print(f"Startkapital:            {STARTING_CAPITAL:,.2f}")
    print(f"Endkapital (Buy&Hold):   {result['final_capital']:,.2f}")
    print(f"Gesamtrendite:           {result['total_return_pct']:.2f}%")
    print(f"Max Drawdown:            {result['max_drawdown_pct']:.2f}%")
    print(f"Anzahl Symbole:          {result['num_symbols']}")

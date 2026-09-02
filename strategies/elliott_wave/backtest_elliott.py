"""
Phase 2c - Backtest der Elliott-Wave-Strategie
================================================
Testet folgende einfache Handelsidee: Wenn eine gueltige 5-Wellen-
Impulsbewegung (aus elliott_wave_counter.py) abgeschlossen ist, wird
oft eine Korrekturbewegung in die Gegenrichtung erwartet.

Regel:
- Bullischer Impuls beendet -> Short-Einstieg bei Ende Welle 5
- Baerischer Impuls beendet -> Long-Einstieg bei Ende Welle 5

Ziel (Take-Profit): 38.2% Fibonacci-Retracement der gesamten
Impulsbewegung (Welle 0 bis Welle 5).
Stop-Loss: Kurs bewegt sich X% weiter in Trendrichtung ueber das
Ende von Welle 5 hinaus (Annahme war falsch, Trend laeuft weiter).

WICHTIG: Das ist ein einfacher Test-Ansatz, keine fertige
Handelsstrategie. Ergebnisse sind Grundlage fuer Diskussion und
weitere Optimierung, keine Kauf-/Verkaufsempfehlung.
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

STOP_LOSS_PCT = 3.0       # Stop, falls Trend weiterlaeuft
TAKE_PROFIT_FIB = 0.382   # Zielretracement der Gesamtbewegung
MAX_HOLD_HOURS = 240      # Notausstieg, falls weder TP noch SL erreicht (10 Tage)

# Realistische Handelskosten (Binance Spot: ~0.1% pro Order als Standard)
TRADING_FEE_PCT = 0.1     # pro Order (Entry und Exit je einmal)
SLIPPAGE_PCT = 0.05       # angenommene Abweichung vom gewuenschten Preis, je Order


def simulate_trade(price_df: pd.DataFrame, entry_time, entry_price: float,
                    direction: str, target_price: float, stop_price: float,
                    max_hold_hours: int) -> dict:
    """
    Simuliert einen einzelnen Trade auf den nachfolgenden Stundenkerzen,
    bis Take-Profit, Stop-Loss oder maximale Haltedauer erreicht ist.
    """
    future = price_df[price_df["open_time"] > entry_time].head(max_hold_hours)

    for _, row in future.iterrows():
        if direction == "long":
            if row["low"] <= stop_price:
                return {"exit_time": row["open_time"], "exit_price": stop_price, "result": "stop_loss"}
            if row["high"] >= target_price:
                return {"exit_time": row["open_time"], "exit_price": target_price, "result": "take_profit"}
        else:  # short
            if row["high"] >= stop_price:
                return {"exit_time": row["open_time"], "exit_price": stop_price, "result": "stop_loss"}
            if row["low"] <= target_price:
                return {"exit_time": row["open_time"], "exit_price": target_price, "result": "take_profit"}

    # Weder TP noch SL erreicht -> Ausstieg zum letzten verfuegbaren Preis
    if len(future) > 0:
        last_row = future.iloc[-1]
        return {"exit_time": last_row["open_time"], "exit_price": last_row["close"], "result": "time_exit"}
    return {"exit_time": None, "exit_price": entry_price, "result": "no_data"}


def run_backtest(price_df: pd.DataFrame, impulses: pd.DataFrame) -> pd.DataFrame:
    trades = []

    for _, wave in impulses.iterrows():
        # Long-only: bullische Impulse (wuerden zu Short fuehren) werden uebersprungen
        if wave["direction"] == "bullish":
            continue

        entry_time = pd.to_datetime(wave["end_time"])
        entry_price = wave["wave5"]
        total_move = abs(wave["wave5"] - wave["wave0"])

        # Baerischer Impuls beendet -> erwartete Korrektur nach oben -> Long
        direction = "long"
        target_price = entry_price + total_move * TAKE_PROFIT_FIB
        stop_price = entry_price * (1 - STOP_LOSS_PCT / 100)

        outcome = simulate_trade(
            price_df, entry_time, entry_price, direction,
            target_price, stop_price, MAX_HOLD_HOURS,
        )

        if outcome["exit_price"] is None or outcome["result"] == "no_data":
            continue

        if direction == "long":
            pnl_pct = (outcome["exit_price"] - entry_price) / entry_price * 100
        else:
            pnl_pct = (entry_price - outcome["exit_price"]) / entry_price * 100

        # Kosten abziehen: Gebuehr + Slippage je einmal fuer Entry, einmal fuer Exit
        total_cost_pct = 2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)
        pnl_pct_net = pnl_pct - total_cost_pct

        trades.append({
            "entry_time": entry_time,
            "direction": direction,
            "entry_price": entry_price,
            "exit_time": outcome["exit_time"],
            "exit_price": outcome["exit_price"],
            "result": outcome["result"],
            "pnl_pct_gross": round(pnl_pct, 2),
            "pnl_pct": round(pnl_pct_net, 2),
            "fib_score": wave["fib_score"],
        })

    return pd.DataFrame(trades)


def print_summary(trades: pd.DataFrame):
    if trades.empty:
        print("Keine Trades ausgefuehrt.")
        return

    total_trades = len(trades)
    wins = trades[trades["pnl_pct"] > 0]
    win_rate = len(wins) / total_trades * 100
    total_return = trades["pnl_pct"].sum()
    total_return_gross = trades["pnl_pct_gross"].sum()
    avg_return = trades["pnl_pct"].mean()
    best_trade = trades["pnl_pct"].max()
    worst_trade = trades["pnl_pct"].min()

    # Einfache Max-Drawdown-Naeherung auf Basis kumulierter Returns
    cum_returns = trades["pnl_pct"].cumsum()
    running_max = cum_returns.cummax()
    drawdown = cum_returns - running_max
    max_drawdown = drawdown.min()

    print(f"Anzahl Trades:        {total_trades}")
    print(f"Win Rate:              {win_rate:.1f}%")
    print(f"Summe PnL brutto (%): {total_return_gross:.2f}%")
    print(f"Summe PnL netto (%):  {total_return:.2f}%  (nach Gebuehren & Slippage)")
    print(f"Kosten gesamt (%):    {total_return_gross - total_return:.2f}%")
    print(f"Durchschnitt PnL (%):  {avg_return:.2f}%")
    print(f"Bester Trade:          {best_trade:.2f}%")
    print(f"Schlechtester Trade:   {worst_trade:.2f}%")
    print(f"Max Drawdown (approx): {max_drawdown:.2f}%")
    print("\nErgebnis-Verteilung:")
    print(trades["result"].value_counts())


if __name__ == "__main__":
    price_df = pd.read_csv(os.path.join(DATA_DIR, "BTCUSDT_1h.csv"), parse_dates=["open_time"])
    impulses = pd.read_csv(os.path.join(RESULTS_DIR, "BTCUSDT_impulse_waves.csv"),
                            parse_dates=["start_time", "end_time"])

    trades = run_backtest(price_df, impulses)

    print(f"\n{'=' * 50}")
    print("BACKTEST-ERGEBNIS: Elliott Wave Reversal-Strategie")
    print(f"{'=' * 50}\n")

    if not trades.empty:
        print(trades.to_string(index=False))
        print()

    print_summary(trades)

    output_path = os.path.join(RESULTS_DIR, "BTCUSDT_backtest_trades.csv")
    trades.to_csv(output_path, index=False)
    print(f"\nGespeichert als: {output_path}")

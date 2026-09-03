"""
Aufgabe 2: Warum ist der 2022-Drawdown identisch mit dem Allzeit-Maximum?
========================================================================
Findet den exakten Zeitpunkt des maximalen Drawdowns 2022 in der
Portfolio-Kapitalkurve und untersucht, was zu diesem Zeitpunkt auf
Signalebene passierte: wie viele gleichzeitige Squeeze-Breakout-Signale
gab es im Vorlauf, wie viele davon waren False Breakouts (Stop-Loss statt
Zeit-Exit/Gewinn)? Ziel: unterscheiden zwischen einem konzentrierten
Einzelereignis (ein starker Ausverkaufstag mit vielen gleichzeitigen
False Breakouts) und einer ueber Monate verteilten strukturellen Schwaeche.
"""

import os
import pandas as pd

from multi_symbol_optimise import load_all_symbol_data
from equity_simulation import collect_all_trades, simulate_portfolio, \
    STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS, STOP_LOSS_PCT

BASE_DIR = "/home/user/trading-bot"
EQUITY_CSV = os.path.join(BASE_DIR, "results", "volatility_breakout", "equity_curve.csv")


def build_daily_capital_curve(csv_path: str, starting_capital: float = 10_000.0) -> pd.Series:
    df = pd.read_csv(csv_path, parse_dates=["time"]).sort_values("time")
    df["date"] = df["time"].dt.normalize()
    daily_last = df.groupby("date")["capital_after"].last()
    full_range = pd.date_range(daily_last.index.min(), daily_last.index.max(), freq="D")
    daily_last = daily_last.reindex(full_range).ffill()
    if pd.isna(daily_last.iloc[0]):
        daily_last.iloc[0] = starting_capital
    return daily_last


def main():
    # --- Schritt 1: exakten Zeitpunkt des 2022-Max-Drawdown-Tiefs finden ---
    curve = build_daily_capital_curve(EQUITY_CSV)
    window_2022 = curve[(curve.index >= "2022-01-01") & (curve.index <= "2022-12-31")]
    running_max = window_2022.cummax()
    drawdown_pct = (window_2022 - running_max) / running_max * 100
    trough_date = drawdown_pct.idxmin()
    trough_dd = drawdown_pct.min()
    peak_date = window_2022[:trough_date].idxmax()

    print("=" * 90)
    print("SCHRITT 1: Zeitpunkt des maximalen Drawdowns 2022")
    print("=" * 90)
    print(f"Vorheriges Kapital-Hoch: {peak_date.date()} ({window_2022[peak_date]:,.2f})")
    print(f"Drawdown-Tief:           {trough_date.date()} ({window_2022[trough_date]:,.2f})")
    print(f"Max Drawdown:            {trough_dd:.2f}%")
    print(f"Dauer Hoch -> Tief:      {(trough_date - peak_date).days} Tage")

    # --- Schritt 2: alle Trades laden (Signal-Ebene, ungefiltert durch Kapitallimit) ---
    all_data = load_all_symbol_data()
    trades_all = collect_all_trades(all_data, STOP_LOSS_PCT)

    # Trades, deren EINSTIEG in den Aufbau der Drawdown-Phase faellt (Hoch bis Tief)
    entries_in_drawdown = trades_all[
        (trades_all["entry_time"] >= peak_date) & (trades_all["entry_time"] <= trough_date)
    ]
    # Trades, die WAEHREND der Drawdown-Phase ausgestiegen sind (das ist es,
    # was tatsaechlich Kapital verloren/gewonnen hat, bevor das Tief erreicht war)
    exits_in_drawdown = trades_all[
        (trades_all["exit_time"] >= peak_date) & (trades_all["exit_time"] <= trough_date)
    ]

    print("\n" + "=" * 90)
    print(f"SCHRITT 2: Signale rund um die Drawdown-Phase ({peak_date.date()} bis {trough_date.date()})")
    print("=" * 90)
    print(f"Alle Symbole mit Squeeze-Breakout-EINSTIEG in diesem Fenster: {len(entries_in_drawdown)}")
    print(f"Alle Symbole mit Trade-AUSSTIEG in diesem Fenster:            {len(exits_in_drawdown)}")

    if not exits_in_drawdown.empty:
        result_counts = exits_in_drawdown["result"].value_counts()
        print(f"\nAusstiegsart der in diesem Fenster geschlossenen Trades:")
        for result, count in result_counts.items():
            pct = count / len(exits_in_drawdown) * 100
            print(f"  {result}: {count} ({pct:.1f}%)")
        stop_loss_share = (exits_in_drawdown["result"] == "stop_loss").mean() * 100
        print(f"\nAnteil False Breakouts (Stop-Loss statt Zeit-Exit) in diesem Fenster: {stop_loss_share:.1f}%")
        avg_pnl = exits_in_drawdown["pnl_pct"].mean()
        print(f"Durchschnittlicher PnL der in diesem Fenster geschlossenen Trades: {avg_pnl:.2f}%")

    # --- Schritt 3: taegliche Verteilung der Entries/Exits im Fenster, um
    # Konzentration (Einzeltag) vs. Verteilung (Monate) zu unterscheiden ---
    print("\n" + "=" * 90)
    print("SCHRITT 3: Zeitliche Verteilung der Entries/Exits (Konzentration vs. verteilt)")
    print("=" * 90)
    entries_by_week = entries_in_drawdown.copy()
    entries_by_week["entry_week"] = entries_by_week["entry_time"].dt.to_period("W")
    print("Einstiege pro Kalenderwoche im Fenster:")
    print(entries_by_week.groupby("entry_week").size().to_string())

    exits_by_week = exits_in_drawdown.copy()
    exits_by_week["exit_week"] = exits_by_week["exit_time"].dt.to_period("W")
    print("\nAusstiege pro Kalenderwoche im Fenster (mit Stop-Loss-Anteil):")
    weekly = exits_by_week.groupby("exit_week").agg(
        n_exits=("result", "size"),
        n_stop_loss=("result", lambda s: (s == "stop_loss").sum()),
    )
    weekly["stop_loss_pct"] = (weekly["n_stop_loss"] / weekly["n_exits"] * 100).round(1)
    print(weekly.to_string())

    # --- Schritt 4: nur die tatsaechlich AUSGEFUEHRTEN (kapitalgebundenen)
    # Trades - das ist es, was die Kapitalkurve wirklich bewegt hat ---
    print("\n" + "=" * 90)
    print("SCHRITT 4: Zum Vergleich - nur die tatsaechlich AUSGEFUEHRTEN Trades im Fenster")
    print("=" * 90)
    result = simulate_portfolio(trades_all, STARTING_CAPITAL, ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)
    equity_curve = result["equity_curve"]
    equity_curve["time"] = pd.to_datetime(equity_curve["time"])
    executed_in_window = equity_curve[
        (equity_curve["time"] >= peak_date) & (equity_curve["time"] <= trough_date)
    ]
    print(f"Ausgefuehrte (kapitalgebundene) Positions-Exits im Fenster: {len(executed_in_window)}")
    if not executed_in_window.empty:
        losing = (executed_in_window["pnl_pct"] < 0).sum()
        print(f"Davon mit negativem PnL: {losing} ({losing/len(executed_in_window)*100:.1f}%)")
        print(f"Summe PnL-Beitrag (grob, ungewichtet nach Allokation): {executed_in_window['pnl_pct'].sum():.2f}%")


if __name__ == "__main__":
    main()

"""
Phase 4 - Forward Testing / Paper Trading
=============================================
Wendet die validierte Strategie (Zigzag 4%, Stop-Loss 2%,
Take-Profit Fib 0.236, Long-only) auf AKTUELLE, bisher ungesehene
Marktdaten an - simuliert Trades OHNE echtes Geld und protokolliert
alles in einer lokalen Datenbank.

WICHTIG: Dieses Skript ist zum WIEDERHOLTEN Ausfuehren gedacht,
z.B. einmal taeglich. Es merkt sich seinen Zustand (offene und
geschlossene Papier-Trades) in "paper_trading.db" und macht bei
jedem Lauf zwei Dinge:

1. Prueft offene Positionen: wurde Take-Profit, Stop-Loss oder die
   maximale Haltedauer seit dem letzten Lauf erreicht? Falls ja,
   Position schliessen und Ergebnis festhalten.
2. Sucht nach NEUEN, gerade erst abgeschlossenen Wellenmustern, die
   noch nicht als Trade erfasst wurden, und eroeffnet dafuer neue
   Papier-Positionen.

So kannst du ueber Wochen/Monate beobachten, ob sich die Strategie
auch im echten "Jetzt" so verhaelt wie im Backtest - ganz ohne
Kapitalrisiko.
"""

import os
import sys
import sqlite3
from datetime import datetime, timedelta

import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
DB_FILE = _P["DB_FILE"]  # eigene Datenbank pro Strategie - vermischt sich nicht mit anderen Bots

from fetch_stock_data import fetch_historical_data
from zigzag_indicator import calculate_zigzag
from elliott_wave_counter import find_impulse_waves, remove_overlapping
from stocks_symbols_config import SYMBOLS
from live_params import DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB, MAX_CONCURRENT_POSITIONS, USE_TAKE_PROFIT

INTERVAL = "1d"
LOOKBACK_PERIOD = "3y"  # 3 Jahre Vorlauf fuer Tages-Kerzen - genug fuer stabile Wellenerkennung

MAX_HOLD_DAYS = 130  # entspricht ~90 Handelstagen (Wochenenden mitgerechnet),
                     # konsistent mit MAX_HOLD_HOURS=90 (Balken) in backtest_elliott.py
TRADING_FEE_PCT = 0.1
SLIPPAGE_PCT = 0.05

# Nur Signale beruecksichtigen, deren Welle 5 vor kurzem endete
SIGNAL_FRESHNESS_DAYS = 5  # ca. eine Handelswoche Puffer (falls der Cronjob mal einen Tag ausfaellt)


def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            signal_time TEXT,
            entry_time TEXT,
            entry_price REAL,
            stop_price REAL,
            target_price REAL,
            exit_time TEXT,
            exit_price REAL,
            result TEXT,
            pnl_pct REAL,
            status TEXT,
            fib_score REAL,
            UNIQUE(symbol, signal_time)
        )
    """)
    conn.commit()
    return conn


def get_open_trades(conn) -> pd.DataFrame:
    return pd.read_sql("SELECT * FROM trades WHERE status = 'open'", conn)


def check_open_trades(conn, price_data: dict):
    """Prueft alle offenen Papier-Trades gegen die aktuellen Kursdaten."""
    open_trades = get_open_trades(conn)
    if open_trades.empty:
        return

    for _, trade in open_trades.iterrows():
        symbol = trade["symbol"]
        if symbol not in price_data:
            continue

        df = price_data[symbol]
        entry_time = pd.to_datetime(trade["entry_time"])
        future = df[df["open_time"] > entry_time]

        max_exit_time = entry_time + timedelta(days=MAX_HOLD_DAYS)
        exit_row = None
        result = None
        exit_price = None

        for _, row in future.iterrows():
            if row["low"] <= trade["stop_price"]:
                exit_row, result, exit_price = row, "stop_loss", trade["stop_price"]
                break
            # Take-Profit nur pruefen, wenn ueber live_params.py aktiviert - konsistent
            # mit backtest_elliott.simulate_trade(use_take_profit=...)
            if USE_TAKE_PROFIT and row["high"] >= trade["target_price"]:
                exit_row, result, exit_price = row, "take_profit", trade["target_price"]
                break
            if row["open_time"] >= max_exit_time:
                exit_row, result, exit_price = row, "time_exit", row["close"]
                break

        if exit_row is not None:
            pnl_pct = (exit_price - trade["entry_price"]) / trade["entry_price"] * 100
            pnl_pct -= 2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)

            conn.execute("""
                UPDATE trades SET exit_time=?, exit_price=?, result=?, pnl_pct=?, status='closed'
                WHERE id=?
            """, (str(exit_row["open_time"]), exit_price, result, round(pnl_pct, 2), trade["id"]))
            conn.commit()
            print(f"  [GESCHLOSSEN] {symbol}: {result}, PnL {pnl_pct:.2f}%")


def find_new_signals(conn, price_data: dict):
    """Sucht neue, frische Wellenmuster und eroeffnet dafuer Papier-Trades.
    Beruecksichtigt MAX_CONCURRENT_POSITIONS, um Klumpenrisiko bei breiten
    Marktbewegungen ueber viele Aktien hinweg zu vermeiden (konsistent mit
    equity_simulation.py)."""
    now = pd.Timestamp.utcnow().tz_localize(None)
    freshness_cutoff = now - timedelta(days=SIGNAL_FRESHNESS_DAYS)
    open_count = pd.read_sql("SELECT COUNT(*) as n FROM trades WHERE status='open'", conn)["n"].iloc[0]

    for symbol, df in price_data.items():
        zigzag = calculate_zigzag(df, deviation_pct=DEVIATION_PCT)
        if len(zigzag) < 6:
            continue

        impulses = find_impulse_waves(zigzag, min_fib_score=0.3)
        if impulses.empty:
            continue
        impulses = remove_overlapping(impulses)
        impulses = impulses[impulses["direction"] == "bearish"]  # Long-only

        for _, wave in impulses.iterrows():
            end_time = pd.to_datetime(wave["end_time"])
            if end_time < freshness_cutoff:
                continue  # Muster ist nicht mehr "frisch"

            if open_count >= MAX_CONCURRENT_POSITIONS:
                print(f"  [UEBERSPRUNGEN] {symbol}: Signal vorhanden, aber "
                      f"Positionslimit ({MAX_CONCURRENT_POSITIONS}) erreicht")
                continue

            # WICHTIG: Als Einstiegspreis den AKTUELLEN Marktpreis nehmen,
            # nicht den historischen Preis vom Wellenende - sonst wuerde
            # ein Trade zu einem laengst vergangenen Kurs eroeffnet.
            latest_price_row = df[df["open_time"] > end_time]
            if latest_price_row.empty:
                continue
            entry_price = latest_price_row.iloc[-1]["close"]
            entry_reference_time = latest_price_row.iloc[-1]["open_time"]

            total_move = abs(wave["wave5"] - wave["wave0"])
            target_price = entry_price + total_move * TAKE_PROFIT_FIB
            stop_price = entry_price * (1 - STOP_LOSS_PCT / 100)

            try:
                conn.execute("""
                    INSERT INTO trades
                    (symbol, signal_time, entry_time, entry_price, stop_price, target_price, status, fib_score)
                    VALUES (?, ?, ?, ?, ?, ?, 'open', ?)
                """, (symbol, str(end_time), str(entry_reference_time), entry_price,
                      stop_price, target_price, wave["fib_score"]))
                conn.commit()
                open_count += 1  # laufend hochzaehlen, damit das Limit auch innerhalb dieses Laufs greift
                print(f"  [NEU EROEFFNET] {symbol}: Welle 5 endete {end_time}, "
                      f"Entry (aktueller Kurs) {entry_price:.2f}, "
                      f"Ziel {target_price:.2f}, Stop {stop_price:.2f}")
            except sqlite3.IntegrityError:
                pass  # Dieses Wellenmuster wurde bereits in einem frueheren Lauf erfasst


def print_summary(conn):
    open_trades = pd.read_sql("SELECT * FROM trades WHERE status='open'", conn)
    closed_trades = pd.read_sql("SELECT * FROM trades WHERE status='closed'", conn)

    print("\n" + "=" * 55)
    print("FORWARD-TEST STATUS")
    print("=" * 55)
    print(f"Offene Papier-Positionen: {len(open_trades)}")
    if not open_trades.empty:
        print(open_trades[["symbol", "entry_time", "entry_price", "target_price", "stop_price"]].to_string(index=False))

    print(f"\nGeschlossene Trades gesamt: {len(closed_trades)}")
    if not closed_trades.empty:
        win_rate = (closed_trades["pnl_pct"] > 0).mean() * 100
        total_pnl = closed_trades["pnl_pct"].sum()
        print(f"Win Rate bisher: {win_rate:.1f}%  |  Summe PnL: {total_pnl:.2f}%")
        print("\nLetzte 5 geschlossene Trades:")
        print(closed_trades.tail(5)[["symbol", "entry_time", "exit_time", "result", "pnl_pct"]].to_string(index=False))


if __name__ == "__main__":
    print(f"Forward-Test-Lauf: {datetime.utcnow().isoformat()}")
    print(f"Take-Profit aktiv: {USE_TAKE_PROFIT}\n")

    conn = init_db()

    print("Lade aktuelle Marktdaten...")
    price_data = {}
    for symbol in SYMBOLS:
        try:
            price_data[symbol] = fetch_historical_data(symbol, period=LOOKBACK_PERIOD, interval=INTERVAL)
        except Exception as e:
            print(f"  Fehler bei {symbol}: {e}")
    print()

    print("Pruefe offene Positionen...")
    check_open_trades(conn, price_data)

    print("\nSuche neue Signale...")
    find_new_signals(conn, price_data)

    print_summary(conn)
    conn.close()

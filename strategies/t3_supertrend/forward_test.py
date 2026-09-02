"""
Forward Testing / Paper Trading - T3/ADX/SuperTrend-Strategie
====================================================================
Analog zur Elliott-Wave-Version: prueft offene Positionen und sucht
neue Einstiegssignale auf aktuellen Marktdaten, protokolliert alles
in einer EIGENEN Datenbank (paper_trading_t3_supertrend.db, automatisch
benannt durch strategy_paths.py - vermischt sich nicht mit dem
Elliott-Wave-Bot).

WICHTIG: Anders als bei Elliott Wave braucht diese Strategie mehr
Vorlaufdaten (T3/ADX/SuperTrend brauchen "Einschwingzeit"), daher ein
laengerer LOOKBACK als bei forward_test.py der Elliott-Wave-Strategie.
"""

import os
import sys
import sqlite3
from datetime import datetime, timedelta

import pandas as pd
from binance.client import Client

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
DB_FILE = _P["DB_FILE"]

from fetch_binance_data import fetch_historical_data
from symbols_config import SYMBOLS
from indicators import compute_indicators
from live_params import T3_FAST_LENGTH, T3_SLOW_LENGTH, ADX_THRESHOLD, STOP_LOSS_PCT, MAX_CONCURRENT_POSITIONS

INTERVAL = Client.KLINE_INTERVAL_4HOUR
LOOKBACK = "120 day ago UTC"  # genug Vorlauf fuer Indikator-Einschwingzeit bei 4h-Kerzen

T3_FACTOR = 0.7
DI_LENGTH = 14
ADX_LENGTH = 14
ATR_LENGTH = 22
ATR_MULT = 3.0
TRADING_FEE_PCT = 0.1
SLIPPAGE_PCT = 0.05


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
            exit_time TEXT,
            exit_price REAL,
            result TEXT,
            pnl_pct REAL,
            status TEXT,
            UNIQUE(symbol, signal_time)
        )
    """)
    conn.commit()
    return conn


def get_open_trades(conn) -> pd.DataFrame:
    return pd.read_sql("SELECT * FROM trades WHERE status = 'open'", conn)


def check_open_trades(conn, indicator_data: dict):
    """Prueft offene Positionen auf Stop-Loss, Trendwechsel oder T3-Crossunder."""
    open_trades = get_open_trades(conn)
    if open_trades.empty:
        return

    for _, trade in open_trades.iterrows():
        symbol = trade["symbol"]
        if symbol not in indicator_data:
            continue

        df = indicator_data[symbol]
        entry_time = pd.to_datetime(trade["entry_time"])
        future = df[df["open_time"] > entry_time]
        if len(future) < 2:
            continue

        for i in range(1, len(future)):
            row = future.iloc[i]
            prev = future.iloc[i - 1]

            stop_hit = row["low"] <= trade["stop_price"]
            trend_flip = row["supertrend_dir"] == -1 and prev["supertrend_dir"] == 1
            t3_crossed_down = prev["t3_fast"] >= prev["t3_slow"] and row["t3_fast"] < row["t3_slow"]

            if stop_hit or trend_flip or t3_crossed_down:
                exit_price = trade["stop_price"] if stop_hit else row["close"]
                result = "stop_loss" if stop_hit else ("trend_flip" if trend_flip else "t3_crossunder")

                pnl_pct = (exit_price - trade["entry_price"]) / trade["entry_price"] * 100
                pnl_pct -= 2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)

                conn.execute("""
                    UPDATE trades SET exit_time=?, exit_price=?, result=?, pnl_pct=?, status='closed'
                    WHERE id=?
                """, (str(row["open_time"]), exit_price, result, round(pnl_pct, 2), trade["id"]))
                conn.commit()
                print(f"  [GESCHLOSSEN] {symbol}: {result}, PnL {pnl_pct:.2f}%")
                break


def find_new_signals(conn, indicator_data: dict, btc_regime_bullish: bool):
    """Sucht neue Einstiegssignale (T3-Crossover + ADX-Filter) auf dem letzten Balken.
    Beruecksichtigt MAX_CONCURRENT_POSITIONS, um Klumpenrisiko bei korrelierten
    Krypto-Trends zu vermeiden (konsistent mit der Equity-Simulation), UND blockiert
    alle neuen Einstiege komplett, wenn BTC selbst gerade im Abwaertstrend ist
    (Markt-Regime-Filter - siehe regime_filter.py)."""
    if not btc_regime_bullish:
        print("  BTC ist aktuell im Abwaertstrend - keine neuen Einstiege in diesem Lauf.")
        return

    open_count = pd.read_sql("SELECT COUNT(*) as n FROM trades WHERE status='open'", conn)["n"].iloc[0]

    for symbol, df in indicator_data.items():
        if len(df) < 3:
            continue

        row = df.iloc[-1]
        prev = df.iloc[-2]

        if pd.isna(row["t3_fast"]) or pd.isna(row["t3_slow"]) or pd.isna(row["adx"]):
            continue

        crossed_up = prev["t3_fast"] <= prev["t3_slow"] and row["t3_fast"] > row["t3_slow"]
        if not (crossed_up and row["adx"] > ADX_THRESHOLD):
            continue

        if open_count >= MAX_CONCURRENT_POSITIONS:
            print(f"  [UEBERSPRUNGEN] {symbol}: Signal vorhanden, aber "
                  f"Positionslimit ({MAX_CONCURRENT_POSITIONS}) erreicht")
            continue

        entry_price = row["close"]
        entry_time = row["open_time"]
        stop_price = entry_price * (1 - STOP_LOSS_PCT / 100)

        try:
            conn.execute("""
                INSERT INTO trades
                (symbol, signal_time, entry_time, entry_price, stop_price, status)
                VALUES (?, ?, ?, ?, ?, 'open')
            """, (symbol, str(entry_time), str(entry_time), entry_price, stop_price))
            conn.commit()
            open_count += 1  # laufend hochzaehlen, damit das Limit auch innerhalb dieses Laufs greift
            print(f"  [NEU EROEFFNET] {symbol}: Entry {entry_price:.2f}, Stop {stop_price:.2f}")
        except sqlite3.IntegrityError:
            pass  # Bereits erfasst


def print_summary(conn):
    open_trades = pd.read_sql("SELECT * FROM trades WHERE status='open'", conn)
    closed_trades = pd.read_sql("SELECT * FROM trades WHERE status='closed'", conn)

    print("\n" + "=" * 55)
    print("FORWARD-TEST STATUS")
    print("=" * 55)
    print(f"Offene Papier-Positionen: {len(open_trades)}")
    if not open_trades.empty:
        print(open_trades[["symbol", "entry_time", "entry_price", "stop_price"]].to_string(index=False))

    print(f"\nGeschlossene Trades gesamt: {len(closed_trades)}")
    if not closed_trades.empty:
        win_rate = (closed_trades["pnl_pct"] > 0).mean() * 100
        total_pnl = closed_trades["pnl_pct"].sum()
        print(f"Win Rate bisher: {win_rate:.1f}%  |  Summe PnL: {total_pnl:.2f}%")
        print("\nLetzte 5 geschlossene Trades:")
        print(closed_trades.tail(5)[["symbol", "entry_time", "exit_time", "result", "pnl_pct"]].to_string(index=False))


if __name__ == "__main__":
    print(f"Forward-Test-Lauf: {datetime.utcnow().isoformat()}\n")

    conn = init_db()

    print("Lade aktuelle Marktdaten und berechne Indikatoren...")
    indicator_data = {}
    for symbol in SYMBOLS:
        try:
            df = fetch_historical_data(symbol, INTERVAL, LOOKBACK)
            indicator_data[symbol] = compute_indicators(
                df, T3_FAST_LENGTH, T3_SLOW_LENGTH, T3_FACTOR,
                DI_LENGTH, ADX_LENGTH, ATR_LENGTH, ATR_MULT,
            )
        except Exception as e:
            print(f"  Fehler bei {symbol}: {e}")
    print()

    print("Pruefe offene Positionen...")
    check_open_trades(conn, indicator_data)

    btc_regime_bullish = True
    if "BTCUSDT" in indicator_data and not indicator_data["BTCUSDT"]["supertrend_dir"].empty:
        btc_regime_bullish = indicator_data["BTCUSDT"]["supertrend_dir"].iloc[-1] == 1
        print(f"\nBTC-Marktregime: {'Aufwaertstrend' if btc_regime_bullish else 'Abwaertstrend'}")
    else:
        print("\nWarnung: BTCUSDT nicht in den geladenen Daten - Regime-Filter uebersprungen.")

    print("\nSuche neue Signale...")
    find_new_signals(conn, indicator_data, btc_regime_bullish)

    print_summary(conn)
    conn.close()

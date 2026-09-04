"""
Phase 4 - Forward Testing / Paper Trading: Turtle Soup (Aktien)
================================================================================
Analog zum Muster von volatility_breakout/forward_test.py. Prueft offene
Positionen und sucht neue Einstiegssignale auf aktuellen Marktdaten,
protokolliert alles in einer EIGENEN Datenbank.

Signal-Logik identisch zur Backtest-Engine (backtest_turtle_soup.py): SELBER
Tag, kein mehrtaegiges Freshness-Fenster - Tagestief unterschreitet das
rollierende DONCHIAN_PERIOD-Tage-Tief UND Schlusskurs kehrt darueber zurueck,
beides am selben Handelstag (letzte verfuegbare Kerze).

STOP_MODE: bei Aktien aktuell None ("kein Stop", siehe live_params.py) -
der musterspezifische "structural"-Stop war empirisch die schlechteste
Variante. Trotzdem generisch fuer alle drei STOP_MODE-Varianten implementiert
(None / "structural" / fester Prozentsatz), konsistent mit backtest_turtle_soup.py.

DEFENSIVES None/UNBEGRENZT-HANDLING (Praezedenzfall: TypeError-Bug beim
Elliott-Wave-Aktien-Bot): hier KEIN reiner Vorsichtsfall - MAX_CONCURRENT_POSITIONS
ist bei diesem Bot TATSAECHLICH None (unbegrenzt), das validierte Ergebnis der
Kapitalmanagement-Nachpruefung (siehe live_params.py). Der None-Pfad wird
deshalb gezielt in experiment_max_concurrent_none_sandbox_test.py getestet.
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
DB_FILE = _P["DB_FILE"]

from fetch_stock_data import fetch_historical_data
from stocks_symbols_config import SYMBOLS
from indicators import donchian_low
from live_params import DONCHIAN_PERIOD, STOP_MODE, MAX_HOLD_DAYS, MAX_CONCURRENT_POSITIONS

INTERVAL = "1d"
LOOKBACK_PERIOD = "2y"  # genug Vorlauf fuer den Donchian-Lookback + Puffer

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


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("open_time").reset_index(drop=True).copy()
    df["donchian_low"] = donchian_low(df["low"], DONCHIAN_PERIOD)
    return df


def check_open_trades(conn, indicator_data: dict):
    """Prueft offene Positionen Balken fuer Balken (Bar-Anzahl, keine
    Kalendertage), Prioritaet: a) Stop-Loss (falls aktiv) b) Zeit-Exit
    nach MAX_HOLD_DAYS - identisch zur Zaehllogik im validierten Backtest."""
    open_trades = get_open_trades(conn)
    if open_trades.empty:
        return

    for _, trade in open_trades.iterrows():
        symbol = trade["symbol"]
        if symbol not in indicator_data:
            continue

        df = indicator_data[symbol]
        entry_time = pd.to_datetime(trade["entry_time"])
        future = df[df["open_time"] > entry_time].reset_index(drop=True)
        if future.empty:
            continue

        stop_price = trade["stop_price"]
        has_stop = stop_price is not None and not pd.isna(stop_price)

        exit_row, result, exit_price = None, None, None
        for offset in range(len(future)):
            row = future.iloc[offset]

            if has_stop and row["low"] <= stop_price:
                exit_row, result, exit_price = row, "stop_loss", stop_price
                break
            if MAX_HOLD_DAYS is not None and offset + 1 >= MAX_HOLD_DAYS:
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


def find_new_signals(conn, indicator_data: dict):
    """Prueft die LETZTE verfuegbare Kerze jedes Symbols: Tagestief
    unterschreitet das Donchian-Tief UND Schlusskurs kehrt darueber zurueck,
    beides am selben Tag (kein Freshness-Fenster). Beruecksichtigt
    MAX_CONCURRENT_POSITIONS (None = unbegrenzt)."""
    open_count = pd.read_sql("SELECT COUNT(*) as n FROM trades WHERE status='open'", conn)["n"].iloc[0]

    for symbol, df in indicator_data.items():
        if len(df) < 1:
            continue

        row = df.iloc[-1]
        if pd.isna(row["donchian_low"]) or pd.isna(row["low"]) or pd.isna(row["close"]):
            continue

        setup_triggered = row["low"] < row["donchian_low"]
        reversal_confirmed = row["close"] > row["donchian_low"]
        if not (setup_triggered and reversal_confirmed):
            continue

        if MAX_CONCURRENT_POSITIONS is not None and open_count >= MAX_CONCURRENT_POSITIONS:
            print(f"  [UEBERSPRUNGEN] {symbol}: Signal vorhanden, aber "
                  f"Positionslimit ({MAX_CONCURRENT_POSITIONS}) erreicht")
            continue

        entry_price = row["close"]
        entry_time = row["open_time"]
        setup_day_low = row["low"]

        if STOP_MODE is None:
            stop_price = None
        elif STOP_MODE == "structural":
            stop_price = setup_day_low
        else:
            stop_price = entry_price * (1 - STOP_MODE / 100)

        try:
            conn.execute("""
                INSERT INTO trades
                (symbol, signal_time, entry_time, entry_price, stop_price, status)
                VALUES (?, ?, ?, ?, ?, 'open')
            """, (symbol, str(entry_time), str(entry_time), entry_price, stop_price))
            conn.commit()
            open_count += 1
            stop_display = f"{stop_price:.2f}" if stop_price is not None else "kein Stop"
            print(f"  [NEU EROEFFNET] {symbol}: Entry {entry_price:.2f}, Stop {stop_display}")
        except sqlite3.IntegrityError:
            pass


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
    print(f"Forward-Test-Lauf: {datetime.utcnow().isoformat()}")
    print(f"Donchian-Lookback: {DONCHIAN_PERIOD}  |  Stop: "
          f"{'kein Stop' if STOP_MODE is None else STOP_MODE}  |  "
          f"Limit: {'unbegrenzt' if MAX_CONCURRENT_POSITIONS is None else MAX_CONCURRENT_POSITIONS}\n")

    conn = init_db()

    print("Lade aktuelle Marktdaten und berechne Indikatoren...")
    indicator_data = {}
    for symbol in SYMBOLS:
        try:
            df = fetch_historical_data(symbol, period=LOOKBACK_PERIOD, interval=INTERVAL)
            if df.empty:
                continue
            indicator_data[symbol] = compute_indicators(df)
        except Exception as e:
            print(f"  Fehler bei {symbol}: {e}")
    print()

    print("Pruefe offene Positionen...")
    check_open_trades(conn, indicator_data)

    print("\nSuche neue Signale...")
    find_new_signals(conn, indicator_data)

    print_summary(conn)
    conn.close()

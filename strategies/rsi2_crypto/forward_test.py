"""
Phase 4 - Forward Testing / Paper Trading: RSI-2 Mean-Reversion (Krypto)
================================================================================
Analog zum Muster von t3_supertrend/forward_test.py (Krypto-Dateninfrastruktur:
Binance API, eigene Datenbank) UND rsi2_mean_reversion/forward_test.py
(RSI-2-Signal-/Ausstiegslogik). Prueft offene Positionen und sucht neue
Einstiegssignale auf aktuellen Tageskerzen, protokolliert alles in einer
EIGENEN Datenbank. Zum WIEDERHOLTEN taeglichen Ausfuehren gedacht - Krypto
handelt 24/7, daher auch am Wochenende (siehe Cronjob-Vorschlag).

Laeuft bewusst auf TAGESKERZEN (nicht 1h/4h wie Elliott Wave/T3-SuperTrend
Krypto) - siehe PROTOTYPE_FINDINGS.md Abschnitt 0 fuer die Begruendung.

BTC-Regime-Filter wurde GEPRUEFT, aber NICHT uebernommen (schadet der
Mean-Reversion-Logik deutlich, siehe PROTOTYPE_FINDINGS.md Abschnitt 6) -
bewusst NICHT in dieses Live-Skript eingebaut.

DEFENSIVES None/UNBEGRENZT-HANDLING (Praezedenzfall: TypeError-Bug beim
Elliott-Wave-Aktien-Bot): STOP_LOSS_PCT=None ist hier der VALIDIERTE
Live-Wert - alle Vergleiche mit stop_price sind explizit gegen None
abgesichert, ebenso MAX_CONCURRENT_POSITIONS gegen None ("unbegrenzt").
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
from indicators import sma, rsi
from live_params import SMA_TREND_FILTER, RSI_THRESHOLD, STOP_LOSS_PCT, MAX_CONCURRENT_POSITIONS

INTERVAL = Client.KLINE_INTERVAL_1DAY
LOOKBACK = "400 day ago UTC"  # genug Vorlauf fuer SMA(150) + Puffer

RSI_PERIOD = 2
SMA_EXIT_PERIOD = 5
MAX_HOLD_DAYS = 10

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
            rsi_at_entry REAL,
            UNIQUE(symbol, signal_time)
        )
    """)
    conn.commit()
    return conn


def get_open_trades(conn) -> pd.DataFrame:
    return pd.read_sql("SELECT * FROM trades WHERE status = 'open'", conn)


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("open_time").reset_index(drop=True).copy()
    df["sma_trend"] = sma(df["close"], SMA_TREND_FILTER)
    df["sma_exit"] = sma(df["close"], SMA_EXIT_PERIOD)
    df["rsi"] = rsi(df["close"], RSI_PERIOD)
    return df


def check_open_trades(conn, indicator_data: dict):
    """Prueft offene Positionen Balken fuer Balken (Bar-Anzahl = Tage, da
    Krypto 24/7 handelt und jeder Tag eine Kerze hat), Prioritaet:
    a) Stop-Loss (falls aktiv) b) SMA(5)-Exit c) Zeit-Exit nach MAX_HOLD_DAYS."""
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
            if not pd.isna(row["sma_exit"]) and row["close"] > row["sma_exit"]:
                exit_row, result, exit_price = row, "sma_exit", row["close"]
                break
            if offset + 1 >= MAX_HOLD_DAYS:
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
    """Prueft die LETZTE verfuegbare Tageskerze jedes Symbols auf ein
    RSI-2-Signal. Beruecksichtigt MAX_CONCURRENT_POSITIONS (None =
    unbegrenzt).

    KEIN PYRAMIDING (Bugfix, siehe PROTOTYPE_FINDINGS.md: "Kein
    Pyramiding" - bereits validierte Backtest-Regel, backtest_rsi2.py
    kann strukturell gar keine Symbol-Duplikate erzeugen, sprang bislang
    aber NICHT auf diese Live-Implementierung um. Ein Symbol mit bereits
    offener Position wird deshalb explizit uebersprungen, unabhaengig
    vom globalen MAX_CONCURRENT_POSITIONS-Zaehler."""
    open_count = pd.read_sql("SELECT COUNT(*) as n FROM trades WHERE status='open'", conn)["n"].iloc[0]
    open_symbols = set(pd.read_sql("SELECT symbol FROM trades WHERE status='open'", conn)["symbol"])

    for symbol, df in indicator_data.items():
        if len(df) < 2:
            continue

        row = df.iloc[-1]
        if pd.isna(row["sma_trend"]) or pd.isna(row["rsi"]):
            continue

        if not (row["close"] > row["sma_trend"] and row["rsi"] < RSI_THRESHOLD):
            continue

        if symbol in open_symbols:
            print(f"  [UEBERSPRUNGEN] {symbol}: Signal vorhanden, aber bereits eine offene "
                  f"Position in diesem Symbol (kein Pyramiding)")
            continue

        if MAX_CONCURRENT_POSITIONS is not None and open_count >= MAX_CONCURRENT_POSITIONS:
            print(f"  [UEBERSPRUNGEN] {symbol}: Signal vorhanden, aber "
                  f"Positionslimit ({MAX_CONCURRENT_POSITIONS}) erreicht")
            continue

        entry_price = row["close"]
        entry_time = row["open_time"]
        stop_price = entry_price * (1 - STOP_LOSS_PCT / 100) if STOP_LOSS_PCT is not None else None

        try:
            conn.execute("""
                INSERT INTO trades
                (symbol, signal_time, entry_time, entry_price, stop_price, status, rsi_at_entry)
                VALUES (?, ?, ?, ?, ?, 'open', ?)
            """, (symbol, str(entry_time), str(entry_time), entry_price, stop_price, round(float(row["rsi"]), 2)))
            conn.commit()
            open_count += 1
            open_symbols.add(symbol)
            stop_display = f"{stop_price:.2f}" if stop_price is not None else "kein Stop"
            print(f"  [NEU EROEFFNET] {symbol}: Entry {entry_price:.2f}, Stop {stop_display}, "
                  f"RSI(2) {row['rsi']:.1f}")
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
    print(f"SMA-Trendfilter: {SMA_TREND_FILTER}  |  RSI-Schwelle: {RSI_THRESHOLD}  |  "
          f"Stop-Loss: {'kein Stop' if STOP_LOSS_PCT is None else f'{STOP_LOSS_PCT}%'}  |  "
          f"Limit: {'unbegrenzt' if MAX_CONCURRENT_POSITIONS is None else MAX_CONCURRENT_POSITIONS}\n")

    conn = init_db()

    print("Lade aktuelle Marktdaten und berechne Indikatoren...")
    indicator_data = {}
    for symbol in SYMBOLS:
        try:
            df = fetch_historical_data(symbol, INTERVAL, LOOKBACK)
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

"""
Phase 4 - Forward Testing / Paper Trading: Volatility Breakout (Krypto)
================================================================================
Analog zum Muster von t3_supertrend/forward_test.py (Krypto-
Dateninfrastruktur: Binance API, eigene Datenbank, BTC-Regime-Filter-
Mechanismus) UND volatility_breakout/forward_test.py (Squeeze-Breakout-
Signal-/Ausstiegslogik). Prueft offene Positionen und sucht neue
Einstiegssignale auf aktuellen Tageskerzen, protokolliert alles in einer
EIGENEN Datenbank. Zum WIEDERHOLTEN taeglichen Ausfuehren gedacht - Krypto
handelt 24/7, daher auch am Wochenende.

Laeuft bewusst auf TAGESKERZEN (nicht 1h/4h wie Elliott Wave/T3-SuperTrend
Krypto) - siehe PROTOTYPE_FINDINGS.md Abschnitt 0 fuer die Begruendung.

BTC-REGIME-FILTER (siehe live_params.py fuer die ausfuehrliche Begruendung):
aktiv als RISIKOMANAGEMENT-MASSNAHME (robuste Drawdown-Reduktion + starke,
kausal erklaerte 2022-Baerenmarkt-Milderung), NICHT weil er in jedem Fall
mehr Rendite bringt. Exakt derselbe Mechanismus wie beim etablierten
T3/SuperTrend-Bot: blockiert ALLE neuen Einstiege in einem Lauf komplett,
wenn BTC selbst (eigener taeglicher SuperTrend) im Abwaertstrend ist -
unabhaengig davon, ob ein einzelner Coin ein Squeeze-Breakout-Signal zeigt.

DEFENSIVES None/UNBEGRENZT-HANDLING (Praezedenzfall: TypeError-Bug beim
Elliott-Wave-Aktien-Bot): Stop-Loss ist hier mit 5% aktiv (nicht None),
MAX_CONCURRENT_POSITIONS wird trotzdem defensiv gegen None abgesichert,
konsistent mit allen anderen Live-Bots in diesem Projekt.
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
from indicators import bollinger_bands, band_width, squeeze_threshold
from regime_filter import compute_btc_regime
from live_params import (
    BB_SQUEEZE_PERCENTILE, BB_LOOKBACK, STOP_LOSS_PCT, MAX_HOLD_DAYS,
    BTC_REGIME_FILTER_ENABLED, MAX_CONCURRENT_POSITIONS,
)

INTERVAL = Client.KLINE_INTERVAL_1DAY
LOOKBACK = "400 day ago UTC"  # genug Vorlauf fuer den 126-Tage-Squeeze-Lookback + Puffer

BB_PERIOD = 20
BB_NUM_STD = 2.0

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
    df["bb_middle"], df["bb_upper"], df["bb_lower"] = bollinger_bands(df["close"], BB_PERIOD, BB_NUM_STD)
    df["bb_width"] = band_width(df["bb_middle"], df["bb_upper"], df["bb_lower"])
    df["squeeze_thresh"] = squeeze_threshold(df["bb_width"], BB_LOOKBACK, BB_SQUEEZE_PERCENTILE)
    df["is_squeeze"] = df["bb_width"] <= df["squeeze_thresh"]
    return df


def check_open_trades(conn, indicator_data: dict):
    """Prueft offene Positionen Balken fuer Balken (Bar-Anzahl = Tage, da
    Krypto 24/7 handelt), Prioritaet: a) Stop-Loss (falls aktiv) b)
    Zeit-Exit nach MAX_HOLD_DAYS - identisch zur Zaehllogik im validierten
    Backtest."""
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


def find_new_signals(conn, indicator_data: dict, btc_regime_bullish: bool):
    """Prueft die LETZTE verfuegbare Tageskerze jedes Symbols: Squeeze am
    Vortag UND Ausbruch heute. Blockiert ALLE neuen Einstiege komplett,
    wenn BTC selbst gerade im Abwaertstrend ist (Markt-Regime-Filter -
    siehe regime_filter.py, live_params.py fuer die Begruendung).
    Beruecksichtigt MAX_CONCURRENT_POSITIONS (None = unbegrenzt)."""
    if BTC_REGIME_FILTER_ENABLED and not btc_regime_bullish:
        print("  BTC ist aktuell im Abwaertstrend - keine neuen Einstiege in diesem Lauf "
              "(Regime-Filter, siehe live_params.py).")
        return

    open_count = pd.read_sql("SELECT COUNT(*) as n FROM trades WHERE status='open'", conn)["n"].iloc[0]

    for symbol, df in indicator_data.items():
        if len(df) < 2:
            continue

        row = df.iloc[-1]
        prev = df.iloc[-2]
        if pd.isna(row["bb_upper"]) or pd.isna(row["close"]) or pd.isna(prev["is_squeeze"]):
            continue

        squeeze_yesterday = bool(prev["is_squeeze"])
        breakout_today = row["close"] > row["bb_upper"]
        if not (squeeze_yesterday and breakout_today):
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
                (symbol, signal_time, entry_time, entry_price, stop_price, status)
                VALUES (?, ?, ?, ?, ?, 'open')
            """, (symbol, str(entry_time), str(entry_time), entry_price, stop_price))
            conn.commit()
            open_count += 1
            stop_display = f"{stop_price:.4f}" if stop_price is not None else "kein Stop"
            print(f"  [NEU EROEFFNET] {symbol}: Entry {entry_price:.4f}, Stop {stop_display}")
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
    print(f"Stop-Loss: {'kein Stop' if STOP_LOSS_PCT is None else f'{STOP_LOSS_PCT}%'}  |  "
          f"BTC-Regime-Filter: {'aktiv' if BTC_REGIME_FILTER_ENABLED else 'inaktiv'}  |  "
          f"Limit: {'unbegrenzt' if MAX_CONCURRENT_POSITIONS is None else MAX_CONCURRENT_POSITIONS}\n")

    conn = init_db()

    print("Lade aktuelle Marktdaten und berechne Indikatoren...")
    indicator_data = {}
    raw_data = {}
    for symbol in SYMBOLS:
        try:
            df = fetch_historical_data(symbol, INTERVAL, LOOKBACK)
            if df.empty:
                continue
            raw_data[symbol] = df
            indicator_data[symbol] = compute_indicators(df)
        except Exception as e:
            print(f"  Fehler bei {symbol}: {e}")
    print()

    print("Pruefe offene Positionen...")
    check_open_trades(conn, indicator_data)

    btc_regime_bullish = True
    if "BTCUSDT" in raw_data:
        btc_regime = compute_btc_regime(raw_data["BTCUSDT"])
        if not btc_regime["btc_regime"].empty:
            btc_regime_bullish = btc_regime["btc_regime"].iloc[-1] == 1
            print(f"\nBTC-Marktregime: {'Aufwaertstrend' if btc_regime_bullish else 'Abwaertstrend'}")
    else:
        print("\nWarnung: BTCUSDT nicht in den geladenen Daten - Regime-Filter uebersprungen.")

    print("\nSuche neue Signale...")
    find_new_signals(conn, indicator_data, btc_regime_bullish)

    print_summary(conn)
    conn.close()

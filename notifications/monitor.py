"""
Zentrales Ueberwachungs-Script (rein lesend)
=================================================
Beobachtet periodisch die neun bestehenden Paper-Trading-Bots unter
strategies/ - liest AUSSCHLIESSLICH ihre bereits vorhandenen
Live-Datenbanken (paper_trading_<bot>.db, read-only geoeffnet, siehe
_read_trades) und ihre Cronjob-Logs (logs/<bot>/*.log). Schreibt oder
veraendert dort NICHTS und hat auch keinen Code-Pfad dafuer - analog zu
shared/portfolio_overview.py und shared/status_overview.py. Die neun
Bot-Scripts selbst werden von diesem Modul nie importiert oder
aufgerufen.

Erkennt fuer Push-Benachrichtigungen (siehe check_for_events, aufgerufen
aus telegram_bot.py) drei Ereignis-Arten:
  1. Neuer Trade eroeffnet
  2. Trade geschlossen (Stop-Loss wird dabei separat hervorgehoben)
  3. Cronjob-Fehler/Script-Abbruch (Traceback im Log) oder ein Bot, der
     laenger nicht gelaufen ist als fuer seinen Zeitrahmen zu erwarten
     waere (Staleness-Warnung)

Liefert ausserdem die Daten-/Formatierungs-Logik fuer die drei
Telegram-Befehle /status, /positions, /pnl (siehe telegram_bot.py) -
zentral hier statt dupliziert in telegram_bot.py, damit es nur eine
Quelle fuer "was bedeutet der DB-Stand eines Bots" gibt.

Eigenstaendig ausfuehrbar zur Diagnose (verschickt dabei ECHTE Alerts
ueber notify.py fuer alles Neue seit dem letzten Lauf):
    python3 notifications/monitor.py

Zustand (zuletzt gesehene Trade-IDs, Log-Leseposition) wird in
notifications/state.json gehalten - reine Laufzeitdatei, kein Secret,
aber nicht Teil des Repos (siehe .gitignore).
"""

import os
import sys
import json
import glob
import logging
import sqlite3
from datetime import datetime, timezone

import pandas as pd
import requests

# WICHTIG: reine logging.getLogger()-Instanz OHNE eigene Handler hier -
# monitor.py ist auch eigenstaendig lauffaehig (python3 notifications/monitor.py),
# nicht nur importiert aus telegram_bot.py. Wird das Modul von
# telegram_bot.py importiert, haengt DAS dort dieselben Konsole+Datei-
# Handler an wie an seine eigenen Logger (siehe _configure_own_logger()
# dort) - Warnungen aus diesem Modul (z.B. eine fehlgeschlagene
# Binance-/yfinance-Kursabfrage) landen dann zuverlaessig an derselben
# Stelle wie alle anderen Bot-Logs, statt (wie zuvor mit print(...,
# file=sys.stderr)) nur sichtbar zu sein, wenn jemand zufaellig genau
# stderr beobachtet.
logger = logging.getLogger("notifications.monitor")

_NOTIF_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_NOTIF_DIR)
STRATEGIES_DIR = os.path.join(BASE_DIR, "strategies")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
STATE_FILE = os.path.join(_NOTIF_DIR, "state.json")

BINANCE_TICKER_URL = "https://api.binance.com/api/v3/ticker/price"
BINANCE_REQUEST_TIMEOUT_SECONDS = 8  # nur der einzelne HTTP-Request - siehe
                                      # zusaetzlich LIVE_PRICE_TIMEOUT_SECONDS
                                      # in telegram_bot.py fuer die harte
                                      # Gesamt-Obergrenze ueber Krypto+Aktien.

# Telegram-Nachrichtenlimit ist 4096 Zeichen - Sicherheitsmarge, damit
# Formatierungs-Overhead (Markdown-Sternchen, Emojis) nicht ausversehen
# doch ueber das Limit rutscht.
MAX_MESSAGE_LENGTH = 3500

TRADE_COLUMNS = [
    "id", "symbol", "signal_time", "entry_time", "entry_price", "stop_price",
    "exit_time", "exit_price", "result", "pnl_pct", "status",
]

# Asset-Klasse je Bot - fuer /status krypto|aktien und die Gruppierung
# in /positions. Bewusst hart hinterlegt (nicht aus dem Ordnernamen
# geraten), analog zur DISPLAY_NAMES-Konvention in
# shared/portfolio_overview.py: ein neuer 10. Bot braucht hier einen
# Eintrag, sonst wird er in discover_bots() mit einer Warnung
# uebersprungen statt falsch einsortiert zu werden.
ASSET_CLASS = {
    "elliott_wave": "krypto",
    "t3_supertrend": "krypto",
    "rsi2_crypto": "krypto",
    "turtle_soup_crypto": "krypto",
    "volatility_breakout_crypto": "krypto",
    "elliott_wave_stocks": "aktien",
    "rsi2_mean_reversion": "aktien",
    "turtle_soup_stocks": "aktien",
    "volatility_breakout": "aktien",
}

DISPLAY_NAMES = {
    "elliott_wave": "Elliott Wave (Krypto)",
    "t3_supertrend": "T3/ADX/SuperTrend (Krypto)",
    "rsi2_crypto": "RSI-2 (Krypto)",
    "turtle_soup_crypto": "Turtle Soup (Krypto)",
    "volatility_breakout_crypto": "Volatility Breakout (Krypto)",
    "elliott_wave_stocks": "Elliott Wave (Aktien)",
    "rsi2_mean_reversion": "RSI-2 Mean-Reversion (Aktien)",
    "turtle_soup_stocks": "Turtle Soup (Aktien)",
    "volatility_breakout": "Volatility Breakout (Aktien)",
}

# Erwarteter Cronjob-Rhythmus je Bot (Stunden) - nur fuer die
# Staleness-Warnung in check_for_events (STALE_TOLERANCE_FACTOR als
# Puffer, um keine falschen Alarme bei leicht verspaeteten Laeufen
# auszuloesen). Grobe Werte gemaess docs/UEBERGABEPROTOKOLL.md.
EXPECTED_INTERVAL_HOURS = {
    "elliott_wave": 1,
    "t3_supertrend": 4,
}
DEFAULT_INTERVAL_HOURS = 24  # Tages-Chart-Bots (alle uebrigen sieben)
STALE_TOLERANCE_FACTOR = 3


def display_name(bot_name: str) -> str:
    return DISPLAY_NAMES.get(bot_name, bot_name)


def discover_bots() -> list:
    """
    Findet alle Bot-Ordner unter strategies/, die eine bekannte
    Asset-Klasse UND eine existierende Live-Datenbank haben. Ein
    pausierter oder noch nie gelaufener Bot (keine DB-Datei) wird
    sauber uebersprungen statt einen Fehler zu werfen - analog zu
    discover_bots() in shared/portfolio_overview.py.
    """
    bots = []
    if not os.path.isdir(STRATEGIES_DIR):
        return bots

    for entry in sorted(os.listdir(STRATEGIES_DIR)):
        strategy_dir = os.path.join(STRATEGIES_DIR, entry)
        if not os.path.isdir(strategy_dir):
            continue

        db_file = os.path.join(BASE_DIR, f"paper_trading_{entry}.db")
        if not os.path.exists(db_file):
            continue

        asset_class = ASSET_CLASS.get(entry)
        if asset_class is None:
            print(
                f"Warnung: Bot '{entry}' hat eine Live-DB, aber keine Asset-Klasse "
                f"in notifications/monitor.py:ASSET_CLASS eingetragen - wird uebersprungen.",
                file=sys.stderr,
            )
            continue

        bots.append({
            "name": entry,
            "display_name": display_name(entry),
            "asset_class": asset_class,
            "db_file": db_file,
            "log_dir": os.path.join(LOGS_DIR, entry),
        })

    return bots


def filter_bots(bots: list, selector: str = None) -> list:
    """
    selector: None/leer = alle Bots, 'krypto'/'aktien' = Asset-Klasse,
    sonst exakter Bot-Ordnername (z.B. 'elliott_wave'). Ein unbekannter
    Selector ergibt eine leere Liste - der Aufrufer (telegram_bot.py)
    entscheidet dann selbst ueber die Nutzer-Fehlermeldung.
    """
    if not selector:
        return bots
    selector = selector.strip().lower()
    if selector in ("krypto", "crypto"):
        return [b for b in bots if b["asset_class"] == "krypto"]
    if selector in ("aktien", "aktie", "stocks", "stock"):
        return [b for b in bots if b["asset_class"] == "aktien"]
    return [b for b in bots if b["name"] == selector]


def _read_trades(db_file: str) -> pd.DataFrame:
    """
    Liest die trades-Tabelle EINES Bots - read-only geoeffnet (SQLite
    URI-Modus 'ro'), damit selbst ein Programmierfehler in diesem Modul
    technisch keine Schreiboperation gegen eine der neun Bot-DBs
    ausloesen kann. Gibt ein leeres DataFrame mit den erwarteten Spalten
    zurueck, falls die Tabelle noch nicht existiert (Bot noch nie
    gelaufen) - kein Absturz.
    """
    uri = f"file:{db_file}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        return pd.read_sql("SELECT * FROM trades", conn)
    except (sqlite3.OperationalError, pd.errors.DatabaseError):
        return pd.DataFrame(columns=TRADE_COLUMNS)
    finally:
        conn.close()


def _latest_log_file(log_dir: str):
    if not os.path.isdir(log_dir):
        return None
    candidates = glob.glob(os.path.join(log_dir, "*.log"))
    if not candidates:
        return None
    return max(candidates, key=os.path.getmtime)


def get_bot_status(bot: dict) -> dict:
    """Liest den aktuellen Stand EINES Bots - offene Positionen,
    letzter Cronjob-Lauf (Log-Datei-Zeitstempel), heutiger PnL."""
    trades = _read_trades(bot["db_file"])
    open_trades = trades[trades["status"] == "open"]
    closed_trades = trades[trades["status"] == "closed"]

    today = datetime.now(timezone.utc).date()
    pnl_today = 0.0
    closed_today = 0
    if not closed_trades.empty:
        exit_dates = pd.to_datetime(closed_trades["exit_time"], errors="coerce").dt.date
        today_mask = exit_dates == today
        # Gleiche Absicherung wie in get_bot_pnl_summary - pnl_pct kann in
        # der Live-DB vereinzelt NULL/kaputte Werte enthalten.
        pnl_values = pd.to_numeric(closed_trades.loc[today_mask, "pnl_pct"], errors="coerce")
        pnl_today = round(pnl_values.sum(), 2)
        closed_today = int(today_mask.sum())

    log_file = _latest_log_file(bot["log_dir"])
    last_run = datetime.fromtimestamp(os.path.getmtime(log_file), tz=timezone.utc) if log_file else None

    # open_positions: Detail je offener Position (Symbol/Entry/Stop) - fuer
    # die Live-Kurs-Anzeige in /status (siehe format_status_message).
    # open_symbols bleibt UNVERAENDERT bestehen (nur eine Symbol-Liste),
    # damit format_positions_message() (eigener Befehl /positions, siehe
    # dortige "nicht anfassen"-Vorgabe) exakt wie bisher weiterlaeuft.
    open_positions = []
    for _, row in open_trades.iterrows():
        open_positions.append({
            "symbol": row["symbol"],
            "entry_price": row.get("entry_price"),
            "stop_price": row.get("stop_price") if "stop_price" in open_trades.columns else None,
        })

    return {
        "name": bot["name"],
        "display_name": bot["display_name"],
        "asset_class": bot["asset_class"],
        "num_open": len(open_trades),
        "open_symbols": open_trades["symbol"].tolist(),
        "open_positions": open_positions,
        "pnl_today": pnl_today,
        "closed_today": closed_today,
        "last_run": last_run,
    }


def get_bot_pnl_summary(bot: dict) -> dict:
    """
    Performance-Zusammenfassung EINES Bots - dieselbe Kennzahlen-Logik
    (Win Rate, Ø PnL, Summe PnL ueber geschlossene Trades) wie das
    bestehende shared/status_overview.py, nur auf alle neun statt drei
    hart codierte Bots angewendet. Die schwergewichtige Portfolio-Logik
    aus shared/portfolio_overview.py (hypothetische Gewichtung,
    Korrelationen, Equity-Kurven-Rekonstruktion) ist fuer eine kurze
    Chat-Ausgabe bewusst NICHT wiederverwendet - das ist eine woechentliche
    E-Mail-Analyse, kein Telegram-Kurzueberblick.
    """
    trades = _read_trades(bot["db_file"])
    closed = trades[trades["status"] == "closed"]

    summary = {
        "name": bot["name"],
        "display_name": bot["display_name"],
        "num_closed": len(closed),
        "win_rate": None,
        "avg_pnl": None,
        "total_pnl": None,
    }
    if not closed.empty:
        # pnl_pct robust in echte Zahlen umwandeln, bevor damit gerechnet
        # wird: anders als die synthetischen Sandbox-Testdaten kann die
        # reale, seit Wochen laufende Live-DB vereinzelt NULL/kaputte Werte
        # in pnl_pct enthalten (z.B. ein aelterer Trade ueber einen frueheren
        # Code-Pfad) - eine object-dtype-Spalte mit None-Werten laesst
        # ">"/mean()/sum() sonst mit TypeError abbrechen. Das erklaerte den
        # Bug, dass /pnl live gar nicht mehr antwortete, waehrend /status
        # - das nur die WENIGEN heutigen Trades anfasst - zufaellig nicht
        # betroffen war. pd.to_numeric(..., errors="coerce") macht daraus
        # sauber NaN statt abzustuerzen.
        pnl = pd.to_numeric(closed["pnl_pct"], errors="coerce")
        summary["win_rate"] = round((pnl > 0).mean() * 100, 1)
        summary["avg_pnl"] = round(pnl.mean(), 2)
        summary["total_pnl"] = round(pnl.sum(), 2)

    return summary


# ---------------------------------------------------------------------------
# Live-Kursabfrage fuer offene Positionen (nur fuer /status)
# ---------------------------------------------------------------------------
#
# WICHTIG - siehe status_command() in telegram_bot.py: fetch_binance_prices(),
# fetch_stock_prices() und fetch_live_prices_for_bots() machen ECHTE,
# BLOCKIERENDE Netzwerk-Aufrufe (requests fuer die Binance-REST-API,
# yfinance fuer Yahoo Finance). Sie MUESSEN deshalb IMMER ueber
# asyncio.to_thread() aus einer async-Funktion heraus aufgerufen werden -
# NIEMALS direkt in einem Telegram-Handler oder einem JobQueue-Job. Genau
# ein synchroner Blocking-Call in einer async-Funktion war die Ursache
# einer frueheren Totalblockade dieses Bots (siehe poll_job()-Docstring
# unten in dieser Datei) - der Event-Loop ist single-threaded und
# kooperativ, ein einziger blockierender Aufruf friert ALLES ein,
# inklusive der Verarbeitung neuer Telegram-Befehle.

def fetch_binance_prices(symbols: list) -> dict:
    """
    Aktuelle Preise fuer eine Liste von Binance-Symbolen - EIN
    gebuendelter Request ueber den OEFFENTLICHEN, unauthentifizierten
    Endpunkt GET /api/v3/ticker/price?symbols=[...] (kein API-Key
    noetig, siehe Binance-API-Doku). Bei bis zu ~20 gleichzeitig offenen
    Krypto-Positionen ueber alle Bots hinweg ist das EIN Request statt
    20 Einzelabfragen.

    Rate-Limit-Einordnung: der oeffentliche ticker/price-Endpunkt hat
    fuer unauthentifizierte IPs ein grosszuegiges Gewichtslimit
    (Groessenordnung 1200 Gewichtspunkte/Minute, ein gebuendelter
    Mehrfach-Symbol-Request kostet nur wenige Punkte) - bei der hier zu
    erwartenden Nutzung (/status wird von einer einzelnen Person
    gelegentlich manuell aufgerufen, nicht automatisiert im Sekundentakt)
    ist das nicht relevant. Konnte in dieser Sandbox NICHT gegen die
    echte Binance-API verifiziert werden (kein Netzwerk-Egress zu
    externen APIs hier, siehe Kommentar in notify.py/README.md) - basiert
    auf der oeffentlich dokumentierten Rate-Limit-Grössenordnung.

    Gibt {symbol: preis} zurueck - Symbole, fuer die kein Preis ermittelt
    werden konnte (Netzwerkfehler, unbekanntes Symbol, Timeout), fehlen
    im Ergebnis-Dict, statt die gesamte Abfrage abstuerzen zu lassen.
    """
    if not symbols:
        return {}

    # WICHTIG - Root Cause eines Live-Bugs: requests kodiert ein
    # Leerzeichen in einem Query-Parameter standardmaessig als "+"
    # (application/x-www-form-urlencoded-Konvention), NICHT als "%20".
    # json.dumps(liste) fuegt per Default nach jedem Komma ein
    # Leerzeichen ein (z.B. '["A", "B"]') - dadurch enthielt die
    # tatsaechlich gesendete URL ein woertliches "+" MITTEN im
    # JSON-Array (?symbols=%5B%22A%22%2C+%22B%22%5D). Ein manueller
    # curl-Test mit demselben Symbol GING problemlos durch (curl nutzt
    # kein form-urlencoding fuer einzelne Query-Werte), was den Fehler
    # zunaechst wie ein Netzwerk-/Erreichbarkeitsproblem aussehen liess,
    # obwohl er tatsaechlich im JSON-Array-Encoding lag. Binances
    # eigene Doku zeigt das erwartete Format ausdruecklich OHNE
    # Leerzeichen (["BTCUSDT","BNBUSDT"]) - separators=(",", ":")
    # erzwingt genau das und macht das Leerzeichen-/"+"-Problem
    # dadurch komplett gegenstandslos, unabhaengig von der genauen
    # Interpretation auf Binance-Seite.
    symbols_param = json.dumps(sorted(set(symbols)), separators=(",", ":"))

    try:
        response = requests.get(
            BINANCE_TICKER_URL,
            params={"symbols": symbols_param},
            timeout=BINANCE_REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        return {item["symbol"]: float(item["price"]) for item in data}
    except Exception as e:
        # Bei einer HTTPError zusaetzlich den Response-Body mitloggen
        # (Binance liefert bei einem ungueltigen Request z.B.
        # {"code":-1100,"msg":"Illegal characters found in parameter..."}
        # zurueck) - das haette diesen Bug beim ersten Live-Test sofort
        # sichtbar gemacht, statt nur "Preis nicht verfuegbar" zu zeigen.
        body = getattr(getattr(e, "response", None), "text", None)
        logger.warning(
            f"Binance-Live-Kursabfrage fehlgeschlagen fuer {symbols_param}: {e}"
            + (f" - Antwort: {body[:300]}" if body else "")
        )
        return {}


def fetch_stock_prices(symbols: list) -> dict:
    """
    Aktuelle Schlusskurse fuer eine Liste von Aktien-Symbolen - EIN
    gebuendelter yfinance-Aufruf (yf.download() mit mehreren Tickern)
    statt eines Aufrufs pro Symbol. yfinance wird bewusst ERST HIER
    (innerhalb der Funktion) importiert, nicht am Datei-Anfang - fehlt
    das Package (z.B. auf einer Installation ohne Aktien-Bots), soll
    NUR die Live-Kurs-Anzeige fuer Aktien-Positionen leise ausfallen
    (siehe except-Block), nicht das gesamte Modul beim Import.

    Liefert den letzten verfuegbaren Tages-Schlusskurs zurueck - fuer
    /status "aktuell genug" waehrend der Handelszeiten, ohne eine
    Realtime-Streaming-Anbindung zu benoetigen. Gibt {symbol: preis}
    zurueck, fehlende Symbole (Netzwerkfehler, Ticker nicht gefunden)
    werden ausgelassen statt die Abfrage abstuerzen zu lassen.
    """
    if not symbols:
        return {}
    try:
        import yfinance as yf
    except ImportError:
        logger.warning(
            "yfinance nicht installiert - Live-Kurse fuer Aktien-Positionen "
            "nicht verfuegbar (pip3 install -r notifications/requirements.txt)."
        )
        return {}

    unique_symbols = sorted(set(symbols))
    prices = {}
    try:
        data = yf.download(
            unique_symbols, period="1d", interval="1d", progress=False,
            group_by="ticker", threads=True,
        )
        if data.empty:
            return {}

        if len(unique_symbols) == 1:
            # yfinance liefert bei GENAU EINEM Ticker keine MultiIndex-Spalten
            # (anders als bei mehreren) - Sonderfall separat behandeln.
            close_series = data["Close"].dropna()
            if not close_series.empty:
                prices[unique_symbols[0]] = float(close_series.iloc[-1])
        else:
            for symbol in unique_symbols:
                try:
                    close_series = data[symbol]["Close"].dropna()
                    if not close_series.empty:
                        prices[symbol] = float(close_series.iloc[-1])
                except (KeyError, IndexError):
                    continue
    except Exception as e:
        logger.warning(f"yfinance-Live-Kursabfrage fehlgeschlagen: {e}")
        return prices

    return prices


def fetch_live_prices_for_bots(bots: list) -> dict:
    """
    Sammelt die Symbole aller AKTUELL OFFENEN Positionen der uebergebenen
    Bots, gruppiert nach Asset-Klasse, und holt fuer beide Gruppen
    GEBUENDELT (je EIN Aufruf, nicht einer pro Symbol/Bot) den aktuellen
    Kurs. Wird von status_command() in telegram_bot.py ueber
    asyncio.to_thread() aufgerufen (siehe Modul-Docstring oben - NIEMALS
    direkt synchron in einer async-Funktion aufrufen).
    """
    crypto_symbols = set()
    stock_symbols = set()
    for bot in bots:
        status = get_bot_status(bot)
        symbols = {p["symbol"] for p in status["open_positions"]}
        if bot["asset_class"] == "krypto":
            crypto_symbols |= symbols
        else:
            stock_symbols |= symbols

    prices = {}
    if crypto_symbols:
        prices.update(fetch_binance_prices(sorted(crypto_symbols)))
    if stock_symbols:
        prices.update(fetch_stock_prices(sorted(stock_symbols)))
    return prices


# ---------------------------------------------------------------------------
# Telegram-Formatierung (Markdown) - zentral hier, damit telegram_bot.py nur
# noch die Antwort verschicken muss.
# ---------------------------------------------------------------------------

def _pnl_emoji(value: float) -> str:
    """
    🟢 vor einem positiven, 🔴 vor einem negativen PnL-/Kursaenderungswert
    - reine Formatierungshilfe, damit die Symbol-Logik nicht an mehreren
    Stellen (kumulierter PnL pro Bot UND jede einzelne offene Position)
    dupliziert wird. Bei exakt 0.0 bewusst KEIN Symbol (weder Gewinn noch
    Verlust) statt eines beliebigen dritten Symbols - deckt insbesondere
    den bekannten, harmlosen "+0.0%"-Fall bei manchen Aktienpositionen ab
    (letzter verfuegbarer Schlusskurs zufaellig identisch mit dem
    Entry-Preis, z.B. direkt nach Eroeffnung oder uebers Wochenende).
    Gibt bei einem Symbol einen TRAILING Space mit zurueck, bei "" keinen -
    so kann der Aufrufer den Rueckgabewert immer direkt vor den Wert
    setzen, ohne selbst auf einen doppelten/fehlenden Leerraum achten zu
    muessen.
    """
    if value > 0:
        return "\U0001F7E2 "
    if value < 0:
        return "\U0001F534 "
    return ""


def _format_open_position_line(position: dict, live_prices: dict) -> str:
    # WICHTIG: entry_price/stop_price kommen direkt aus einer pandas-Spalte
    # (siehe get_bot_status) - ein fehlender Wert ist dort NaN (float),
    # NICHT None, und NaN ist in Python truthy (bool(float('nan')) is True)!
    # pd.notna() statt eines einfachen Wahrheitswert-Checks verwenden,
    # sonst wuerde z.B. "Stop nan" angezeigt statt die Angabe wegzulassen.
    symbol = position["symbol"]
    entry_price = position.get("entry_price")
    stop_price = position.get("stop_price")
    current_price = live_prices.get(symbol)
    has_entry_price = pd.notna(entry_price)

    if current_price is not None and has_entry_price and entry_price != 0:
        change_pct = round((current_price - entry_price) / entry_price * 100, 2)
        sign = "+" if change_pct >= 0 else ""
        price_txt = f"{current_price} {_pnl_emoji(change_pct)}({sign}{change_pct}%)"
    else:
        price_txt = "Preis nicht verfuegbar"

    entry_txt = f"{entry_price}" if has_entry_price else "?"
    stop_txt = f", Stop {stop_price}" if pd.notna(stop_price) else ""
    return f"  `{symbol}`: Entry {entry_txt}{stop_txt} -> {price_txt}"


def format_status_message(bots: list, live_prices: dict = None):
    """
    Gibt einen einzelnen String zurueck, WENN die komplette Ausgabe unter
    MAX_MESSAGE_LENGTH passt (der ueberwiegend haeufige Fall) - sonst
    eine Liste mehrerer Strings (Telegrams 4096-Zeichen-Limit pro
    Nachricht kann mit vielen Bots/offenen Positionen inkl. Live-Kursen
    ueberschritten werden). _reply_for_selector() in telegram_bot.py
    unterstuetzt beide Rueckgabeformen - siehe dortiger Kommentar.

    live_prices: {symbol: aktueller_preis}, siehe fetch_live_prices_for_bots().
    None/leer bedeutet "keine Live-Kurse verfuegbar" (z.B. Zeitueberschreitung
    bei der Abfrage) - die Positionszeilen zeigen dann "Preis nicht
    verfuegbar" statt eines aktuellen Gewinns/Verlusts, der Rest der
    Ausgabe (kumulierter PnL, offene Positionen als Symbolliste) bleibt
    unveraendert verfuegbar.

    Reihenfolge: absteigend nach kumuliertem PnL (bester Bot zuerst) -
    ALLE Bots bleiben weiterhin vollstaendig aufgelistet, auch ohne offene
    Positionen, nur die Sortierung aendert sich. Bots ohne geschlossene
    Trades (total_pnl is None, "n/a") haben keinen Sortierwert und werden
    ans Ende gestellt; sorted() ist stabil, daher bleibt ihre
    urspruengliche Reihenfolge (siehe discover_bots(), alphabetisch nach
    Ordnername) untereinander erhalten.
    """
    live_prices = live_prices or {}
    entries = [(bot, get_bot_status(bot), get_bot_pnl_summary(bot)) for bot in bots]
    entries.sort(key=lambda e: (e[2]["total_pnl"] is None, -(e[2]["total_pnl"] or 0)))

    chunks = []
    current_lines = ["*Status-Ueberblick*"]

    for bot, s, p in entries:
        last_run_txt = s["last_run"].strftime("%d.%m. %H:%M UTC") if s["last_run"] else "unbekannt"
        if p["total_pnl"] is not None:
            total_pnl_txt = f"{_pnl_emoji(p['total_pnl'])}{p['total_pnl']}%"
        else:
            total_pnl_txt = "n/a (keine geschlossenen Trades)"

        block_lines = [
            f"\n*{s['display_name']}*",
            f"Letzter Lauf: {last_run_txt}",
            f"Offene Positionen: {s['num_open']}",
            f"Heute geschlossen: {s['closed_today']} (PnL {s['pnl_today']}%)",
            f"Kumulierter PnL: {total_pnl_txt}",
        ]
        for position in s["open_positions"]:
            block_lines.append(_format_open_position_line(position, live_prices))

        block_text = "\n".join(block_lines)
        current_text = "\n".join(current_lines)
        if len(current_lines) > 1 and len(current_text) + len(block_text) + 1 > MAX_MESSAGE_LENGTH:
            chunks.append(current_text)
            current_lines = ["*Status-Ueberblick (Fortsetzung)*"]
        current_lines.append(block_text)

    chunks.append("\n".join(current_lines))
    return chunks if len(chunks) > 1 else chunks[0]


def format_positions_message(bots: list) -> str:
    by_class = {"krypto": [], "aktien": []}
    for bot in bots:
        s = get_bot_status(bot)
        if s["num_open"] == 0:
            continue
        symbols_txt = ", ".join(s["open_symbols"])
        by_class[s["asset_class"]].append(f"  {s['display_name']}: {symbols_txt}")

    lines = ["*Offene Positionen*"]
    for label, key in (("Krypto", "krypto"), ("Aktien", "aktien")):
        entries = by_class[key]
        if not entries:
            continue
        lines.append(f"\n*{label}*")
        lines.extend(entries)

    if len(lines) == 1:
        lines.append("\nKeine offenen Positionen.")

    return "\n".join(lines)


def format_pnl_message(bots: list) -> str:
    lines = ["*Performance-Zusammenfassung*"]
    for bot in bots:
        p = get_bot_pnl_summary(bot)
        if p["num_closed"] == 0:
            lines.append(f"\n*{p['display_name']}*\nNoch keine geschlossenen Trades.")
            continue
        lines.append(
            f"\n*{p['display_name']}*\n"
            f"Geschlossene Trades: {p['num_closed']}  |  Win Rate: {p['win_rate']}%\n"
            f"Ø PnL: {p['avg_pnl']}%  |  Summe: {p['total_pnl']}%"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Zustand & Ereignis-Erkennung fuer Push-Benachrichtigungen
# ---------------------------------------------------------------------------

def _load_state() -> dict:
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_state(state: dict):
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, STATE_FILE)


def _scan_log_for_errors(bot_state: dict, log_file):
    """
    Liest nur die seit dem letzten Check NEU angehaengten Bytes eines
    Log-Files (Byte-Offset in bot_state) und meldet einen Alert-Text,
    falls ein "Traceback" (Python-Marker fuer eine unabgefangene
    Exception, d.h. Script-Abbruch) darin vorkommt. Gibt (alert_or_None,
    neuer_offset) zurueck.
    """
    offset = bot_state.get("log_offset", 0)
    if log_file is None:
        return None, offset

    try:
        size = os.path.getsize(log_file)
        if size < offset:
            offset = 0  # Log wurde rotiert/neu angelegt

        with open(log_file, "rb") as f:
            f.seek(offset)
            new_bytes = f.read()
            new_offset = f.tell()
    except OSError:
        return None, offset

    if not new_bytes:
        return None, new_offset

    new_text = new_bytes.decode("utf-8", errors="ignore")
    if "Traceback" in new_text:
        snippet = new_text.strip().splitlines()[-1][:300]
        return snippet, new_offset

    return None, new_offset


def check_for_events(bots: list = None) -> list:
    """
    Vergleicht den aktuellen DB-/Log-Stand jedes Bots mit dem zuletzt
    gespeicherten Zustand (state.json) und gibt eine Liste fertig
    formatierter Alert-Texte fuer alles Neue zurueck. Aktualisiert
    state.json als Seiteneffekt - ein wiederholter Aufruf ohne
    Aenderung dazwischen erzeugt KEINE Doppel-Alerts.

    Bei einem Bot, der zum ALLERERSTEN Mal gesehen wird (z.B. beim
    ersten Start des Telegram-Dienstes), wird bewusst NUR ein
    Ausgangszustand gespeichert, statt fuer die komplette bisherige
    Trade-Historie und alte, laengst erledigte Log-Fehler rueckwirkend
    Alerts zu verschicken.
    """
    if bots is None:
        bots = discover_bots()

    state = _load_state()
    events = []

    for bot in bots:
        name = bot["name"]
        is_first_seen = name not in state
        bot_state = state.get(name, {"known_open_ids": [], "max_id": -1, "log_offset": 0, "was_stale": False})

        trades = _read_trades(bot["db_file"])
        log_file = _latest_log_file(bot["log_dir"])

        if is_first_seen:
            # Nur Baseline speichern (siehe Docstring) - keine Events fuer
            # bereits bestehende Trades/Log-Inhalte.
            new_offset = os.path.getsize(log_file) if log_file else 0
            currently_open_ids = set(trades.loc[trades["status"] == "open", "id"].tolist()) if not trades.empty else set()
            max_id = int(trades["id"].max()) if not trades.empty else -1
            state[name] = {
                "known_open_ids": sorted(currently_open_ids),
                "max_id": max_id,
                "log_offset": new_offset,
                "was_stale": False,
            }
            continue

        known_open_ids = set(bot_state.get("known_open_ids", []))
        max_id = bot_state.get("max_id", -1)

        new_rows = trades[trades["id"] > max_id] if not trades.empty else trades
        for _, row in new_rows.iterrows():
            events.append(
                f"\U0001F7E2 *{bot['display_name']}*: Neuer Trade eroeffnet\n"
                f"Symbol: `{row['symbol']}`  |  Entry: {row.get('entry_price', '?')}"
            )

        currently_open_ids = set(trades.loc[trades["status"] == "open", "id"].tolist()) if not trades.empty else set()
        newly_closed_ids = known_open_ids - currently_open_ids
        if newly_closed_ids:
            closed_rows = trades[trades["id"].isin(newly_closed_ids)]
            for _, row in closed_rows.iterrows():
                is_stop = row.get("result") == "stop_loss"
                icon = "\U0001F6D1" if is_stop else "✅"
                label = "STOP-LOSS ausgeloest" if is_stop else "Trade geschlossen"
                events.append(
                    f"{icon} *{bot['display_name']}*: {label}\n"
                    f"Symbol: `{row['symbol']}`  |  Ergebnis: {row.get('result', '?')}  |  "
                    f"PnL: {row.get('pnl_pct', '?')}%"
                )

        error_snippet, new_offset = _scan_log_for_errors(bot_state, log_file)
        if error_snippet:
            events.append(
                f"⚠️ *{bot['display_name']}*: Cronjob-Fehler/Script-Abbruch erkannt\n"
                f"Letzte Zeile: `{error_snippet}`"
            )

        expected_h = EXPECTED_INTERVAL_HOURS.get(name, DEFAULT_INTERVAL_HOURS)
        was_stale = bot_state.get("was_stale", False)
        is_stale = was_stale
        if log_file:
            age_hours = (datetime.now(timezone.utc).timestamp() - os.path.getmtime(log_file)) / 3600
            is_stale = age_hours > expected_h * STALE_TOLERANCE_FACTOR
            if is_stale and not was_stale:
                events.append(
                    f"⚠️ *{bot['display_name']}*: seit {age_hours:.1f}h kein Cronjob-Lauf "
                    f"registriert (erwartet alle ~{expected_h}h) - bitte pruefen."
                )

        max_id_new = int(trades["id"].max()) if not trades.empty else max_id
        state[name] = {
            "known_open_ids": sorted(currently_open_ids),
            "max_id": max_id_new,
            "log_offset": new_offset,
            "was_stale": is_stale,
        }

    _save_state(state)
    return events


if __name__ == "__main__":
    found_events = check_for_events()
    if not found_events:
        print("Keine neuen Ereignisse.")
    else:
        from notify import send_alert
        for event_text in found_events:
            print(event_text)
            print("-" * 40)
            send_alert(event_text)

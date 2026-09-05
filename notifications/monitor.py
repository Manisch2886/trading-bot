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
import sqlite3
from datetime import datetime, timezone

import pandas as pd

_NOTIF_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_NOTIF_DIR)
STRATEGIES_DIR = os.path.join(BASE_DIR, "strategies")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
STATE_FILE = os.path.join(_NOTIF_DIR, "state.json")

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

    return {
        "name": bot["name"],
        "display_name": bot["display_name"],
        "asset_class": bot["asset_class"],
        "num_open": len(open_trades),
        "open_symbols": open_trades["symbol"].tolist(),
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
# Telegram-Formatierung (Markdown) - zentral hier, damit telegram_bot.py nur
# noch die Antwort verschicken muss.
# ---------------------------------------------------------------------------

def format_status_message(bots: list) -> str:
    lines = ["*Status-Ueberblick*"]
    for bot in bots:
        s = get_bot_status(bot)
        last_run_txt = s["last_run"].strftime("%d.%m. %H:%M UTC") if s["last_run"] else "unbekannt"
        lines.append(
            f"\n*{s['display_name']}*\n"
            f"Letzter Lauf: {last_run_txt}\n"
            f"Offene Positionen: {s['num_open']}\n"
            f"Heute geschlossen: {s['closed_today']} (PnL {s['pnl_today']}%)"
        )
    return "\n".join(lines)


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

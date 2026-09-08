"""
Datenschicht des Dashboards - REIN LESEND
==============================================================
Duenne Schicht ueber notifications/monitor.py. Sie implementiert die
DB-Lese-Logik NICHT ein zweites Mal, sondern ruft ausschliesslich die
dort bereits vorhandenen, im Telegram-Betrieb erprobten Funktionen auf
(discover_bots, filter_bots, get_bot_status, get_bot_pnl_summary,
fetch_live_prices_for_bots, _current_total_result). Damit gibt es
weiterhin genau EINE Quelle fuer die Frage "was bedeutet der DB-Stand
eines Bots" - eine zweite Implementierung wuerde frueher oder spaeter
andere Zahlen liefern als /status in Telegram.

monitor.py oeffnet die neun Bot-Datenbanken im SQLite-Modus "ro"
(read-only) und hat keinen Code-Pfad, der irgendwo schreibt. Dieses
Modul fuegt keinen hinzu: es gibt hier keine INSERT/UPDATE/DELETE-Stelle
und keine Funktion, die eine Bot-Datei anfasst.

Aufgabe dieser Schicht ist im Wesentlichen die Umwandlung der
pandas-/numpy-Werte aus monitor.py in JSON-taugliche Python-Typen:
NaN ist in JSON nicht darstellbar (json.dumps erzeugt sonst das
ungueltige Literal NaN, an dem jeder Browser-Parser scheitert), und
numpy.float64/int64 sind fuer json nicht serialisierbar.
"""

import math
import os
import sys
from datetime import datetime

import pandas as pd

_DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DASHBOARD_DIR)
_NOTIFICATIONS_DIR = os.path.join(BASE_DIR, "notifications")
if _NOTIFICATIONS_DIR not in sys.path:
    sys.path.insert(0, _NOTIFICATIONS_DIR)

import monitor  # noqa: E402

# Obergrenze fuer die Trade-Liste einer einzelnen Antwort - schuetzt vor
# einer versehentlich riesigen JSON-Antwort, wenn ein Bot ueber Monate
# sehr viele Trades angesammelt hat.
MAX_TRADES = 500


def _zahl(wert):
    """pandas/numpy-Wert -> float oder None. NaN wird zu None, weil NaN
    in JSON nicht existiert (siehe Modul-Docstring)."""
    if wert is None:
        return None
    try:
        zahl = float(wert)
    except (TypeError, ValueError):
        return None
    if math.isnan(zahl) or math.isinf(zahl):
        return None
    return zahl


def _text(wert):
    if wert is None:
        return None
    if isinstance(wert, float) and math.isnan(wert):
        return None
    try:
        if pd.isna(wert):
            return None
    except (TypeError, ValueError):
        pass
    return str(wert)


def _zeitpunkt(wert):
    """datetime/Timestamp -> ISO-8601-String, sonst None."""
    if wert is None:
        return None
    if isinstance(wert, datetime):
        return wert.isoformat()
    return _text(wert)


def alle_bots() -> list:
    """Alle Bots mit vorhandener Live-Datenbank (siehe
    monitor.discover_bots - ein pausierter Bot ohne DB fehlt hier
    bewusst, statt einen Fehler auszuloesen)."""
    return monitor.discover_bots()


def finde_bot(name: str):
    """Genau einen Bot anhand seines Ordnernamens, oder None."""
    treffer = monitor.filter_bots(alle_bots(), name)
    # filter_bots kennt auch die Sammel-Selektoren 'krypto'/'aktien' -
    # hier ist aber ausdruecklich EIN Bot gemeint, deshalb der
    # zusaetzliche Namensvergleich.
    for bot in treffer:
        if bot["name"] == name:
            return bot
    return None


def _bot_zeile(bot: dict, live_kurse: dict = None) -> dict:
    """Eine Zeile der Uebersicht: Status + Performance eines Bots."""
    status = monitor.get_bot_status(bot)
    performance = monitor.get_bot_pnl_summary(bot)

    zeile = {
        "name": status["name"],
        "anzeigename": status["display_name"],
        "anlageklasse": status["asset_class"],
        "offene_positionen": status["num_open"],
        "pnl_heute": _zahl(status["pnl_today"]),
        "geschlossen_heute": status["closed_today"],
        "letzter_lauf": _zeitpunkt(status["last_run"]),
        "geschlossene_trades": performance["num_closed"],
        "trefferquote": _zahl(performance["win_rate"]),
        "durchschnitt_pnl": _zahl(performance["avg_pnl"]),
        "summe_pnl": _zahl(performance["total_pnl"]),
        "aktuelles_gesamtergebnis": None,
        "gesamtergebnis_hinweis": None,
    }

    if live_kurse is not None:
        # Dieselbe Kennzahl wie die Zeile "Aktuelles Gesamtergebnis" in
        # /status - bewusst aus monitor.py wiederverwendet, damit
        # Dashboard und Telegram nicht auseinanderlaufen koennen.
        wert, hinweis = monitor._current_total_result(status, performance, live_kurse)
        zeile["aktuelles_gesamtergebnis"] = _zahl(wert)
        zeile["gesamtergebnis_hinweis"] = hinweis

    return zeile


def _position_zeile(position: dict, live_kurse: dict) -> dict:
    symbol = position["symbol"]
    entry = _zahl(position.get("entry_price"))
    stop = _zahl(position.get("stop_price"))
    aktuell = _zahl(live_kurse.get(symbol)) if live_kurse else None

    veraenderung = None
    if aktuell is not None and entry:
        veraenderung = round((aktuell - entry) / entry * 100, 2)

    return {
        "symbol": symbol,
        "entry_preis": entry,
        "stop_preis": stop,
        "aktueller_preis": aktuell,
        "veraenderung_pct": veraenderung,
    }


def portfolio_uebersicht(live_kurse: dict = None) -> dict:
    """Alle Bots auf einen Blick, plus einige Summenwerte.

    live_kurse: {symbol: preis} oder None. None bedeutet ausdruecklich
    "ohne Live-Kurse" - die Uebersicht ist dann eine reine
    Datenbank-Abfrage ohne jeden Netzwerkzugriff und entsprechend
    schnell. Das Frontend holt die Kurse deshalb in einem ZWEITEN,
    getrennten Aufruf nach (siehe /api/live-kurse).
    """
    zeilen = [_bot_zeile(bot, live_kurse) for bot in alle_bots()]

    return {
        "bots": zeilen,
        "summe": {
            "anzahl_bots": len(zeilen),
            "offene_positionen": sum(z["offene_positionen"] for z in zeilen),
            "geschlossene_trades": sum(z["geschlossene_trades"] for z in zeilen),
            "pnl_heute": round(sum(z["pnl_heute"] or 0.0 for z in zeilen), 2),
            # Bewusst eine SUMME der Bot-Ergebnisse in Prozentpunkten und
            # ausdruecklich KEINE Portfolio-Rendite: die Bots tracken kein
            # Kapital pro Trade (siehe monitor._current_total_result), eine
            # echte gewichtete Rendite laesst sich daraus nicht bilden.
            "summe_pnl_prozentpunkte": round(
                sum(z["summe_pnl"] or 0.0 for z in zeilen), 2),
        },
        "live_kurse_enthalten": live_kurse is not None,
        "abgerufen_am": datetime.utcnow().isoformat(),
    }


def bot_detail(bot: dict, live_kurse: dict = None, trade_limit: int = 50) -> dict:
    """Einzelner Bot: Kennzahlen, offene Positionen, letzte Trades."""
    status = monitor.get_bot_status(bot)
    zeile = _bot_zeile(bot, live_kurse)
    zeile["positionen"] = [
        _position_zeile(p, live_kurse or {}) for p in status["open_positions"]
    ]
    zeile["letzte_trades"] = geschlossene_trades(bot, limit=trade_limit)
    zeile["live_kurse_enthalten"] = live_kurse is not None
    zeile["abgerufen_am"] = datetime.utcnow().isoformat()
    return zeile


def _trades_sortiert(bot: dict) -> pd.DataFrame:
    """Geschlossene Trades eines Bots, chronologisch nach Ausstieg.

    Greift auf monitor._read_trades zurueck - die einzige Stelle im
    Projekt, die eine Bot-DB read-only oeffnet und fehlende Tabellen
    abfaengt. Die Funktion ist dort mit Unterstrich benannt; sie hier
    trotzdem zu benutzen ist die deutlich bessere Wahl, als eine zweite
    SQLite-Lese-Logik gegen dieselben neun Live-Datenbanken zu schreiben
    (siehe README, Annahmen).
    """
    trades = monitor._read_trades(bot["db_file"])
    if trades.empty:
        return trades
    geschlossen = trades[trades["status"] == "closed"].copy()
    if geschlossen.empty:
        return geschlossen
    geschlossen["_ausstieg"] = pd.to_datetime(geschlossen["exit_time"], errors="coerce")
    # Trades ohne lesbaren Ausstiegs-Zeitstempel ans Ende, damit ein
    # kaputter Einzelwert die Chronologie nicht durcheinanderbringt.
    return geschlossen.sort_values("_ausstieg", na_position="last")


def geschlossene_trades(bot: dict, limit: int = 50) -> list:
    """Die zuletzt geschlossenen Trades, neueste zuerst."""
    geschlossen = _trades_sortiert(bot)
    if geschlossen.empty:
        return []

    limit = max(1, min(int(limit), MAX_TRADES))
    ausschnitt = geschlossen.tail(limit).iloc[::-1]

    trades = []
    for _, zeile in ausschnitt.iterrows():
        trades.append({
            "symbol": _text(zeile.get("symbol")),
            "einstieg": _text(zeile.get("entry_time")),
            "ausstieg": _text(zeile.get("exit_time")),
            "entry_preis": _zahl(zeile.get("entry_price")),
            "exit_preis": _zahl(zeile.get("exit_price")),
            "ergebnis": _text(zeile.get("result")),
            "pnl_pct": _zahl(zeile.get("pnl_pct")),
        })
    return trades


def verlauf(bot: dict) -> list:
    """Kumulierte Summe der Trade-Ergebnisse EINES Bots ueber die Zeit.

    WICHTIG - was das ist und was es NICHT ist: aufsummierte
    Prozentpunkte der geschlossenen Trades in der Reihenfolge ihres
    Ausstiegs. Das ist KEINE Equity-Kurve und keine Rendite: die Bots
    speichern keine Positionsgroesse pro Trade (siehe
    monitor._current_total_result), eine kapitalgewichtete Kurve laesst
    sich daraus nicht bilden. Die schwergewichtige
    Equity-Rekonstruktion aus shared/portfolio_overview.py wird hier
    bewusst nicht verwendet - sie startet je Bot einen eigenen
    Python-Subprozess und braucht Sekunden bis Minuten, was fuer eine
    Web-Anfrage unbrauchbar waere (siehe README, Annahmen).
    """
    geschlossen = _trades_sortiert(bot)
    if geschlossen.empty:
        return []

    roh = pd.to_numeric(geschlossen["pnl_pct"], errors="coerce")
    # Ein Trade ohne lesbares Ergebnis (NULL/kaputter Wert in der Live-DB -
    # der Fall, der /pnl im Telegram-Bot einmal zum Schweigen gebracht hat)
    # geht mit 0 in die Kurve ein, statt aus der Zeitachse zu verschwinden.
    # Er wird dabei nicht verschwiegen: gesamtverlauf() zaehlt solche
    # Trades und weist sie in der Antwort aus.
    kumuliert = roh.fillna(0.0).cumsum()

    punkte = []
    for (_, zeile), wert in zip(geschlossen.iterrows(), kumuliert):
        punkte.append({
            "zeitpunkt": _text(zeile.get("exit_time")),
            "kumuliert_pct": round(float(wert), 2),
            "symbol": _text(zeile.get("symbol")),
            "pnl_pct": _zahl(zeile.get("pnl_pct")),
        })
    return punkte


def gesamtverlauf() -> dict:
    """Verlaufskurven aller Bots plus eine zusammengefasste Kurve.

    Die zusammengefasste Kurve summiert die Trade-Ergebnisse ALLER Bots
    in der Reihenfolge ihrer Ausstiegszeitpunkte - mit demselben
    Vorbehalt wie verlauf(): Prozentpunkte, keine Portfolio-Rendite.
    """
    kurven = {}
    alle_punkte = []
    ohne_ergebnis_gesamt = 0
    for bot in alle_bots():
        punkte = verlauf(bot)
        ohne_ergebnis = sum(1 for p in punkte if p["pnl_pct"] is None)
        ohne_ergebnis_gesamt += ohne_ergebnis
        kurven[bot["name"]] = {
            "anzeigename": bot["display_name"],
            "anlageklasse": bot["asset_class"],
            "punkte": punkte,
            "trades_ohne_ergebnis": ohne_ergebnis,
        }
        for punkt in punkte:
            if punkt["zeitpunkt"]:
                # Genau wie in verlauf(): ein Trade ohne lesbares Ergebnis
                # bleibt als Punkt auf der Zeitachse, traegt aber 0 bei.
                alle_punkte.append((punkt["zeitpunkt"], punkt["pnl_pct"] or 0.0))

    alle_punkte.sort(key=lambda p: p[0])
    gesamt = []
    laufend = 0.0
    for zeitpunkt, pnl in alle_punkte:
        laufend += pnl
        gesamt.append({"zeitpunkt": zeitpunkt, "kumuliert_pct": round(laufend, 2)})

    hinweis = ("Kumulierte Summe der Trade-Ergebnisse in Prozentpunkten - "
                "keine Equity-Kurve und keine Portfolio-Rendite, da die Bots "
                "keine Positionsgroesse pro Trade speichern.")
    if ohne_ergebnis_gesamt:
        hinweis += (f" {ohne_ergebnis_gesamt} geschlossene(r) Trade(s) ohne lesbares "
                     f"Ergebnis in der Datenbank gehen mit 0 in die Kurve ein.")

    return {
        "bots": kurven,
        "gesamt": gesamt,
        "trades_ohne_ergebnis": ohne_ergebnis_gesamt,
        "hinweis": hinweis,
        "abgerufen_am": datetime.utcnow().isoformat(),
    }


def live_kurse(bots: list) -> dict:
    """Aktuelle Kurse aller offenen Positionen der uebergebenen Bots.

    ACHTUNG - BLOCKIEREND: dahinter stehen echte, synchrone
    Netzwerkaufrufe (Binance-REST fuer Krypto, yfinance fuer Aktien).
    Diese Funktion darf aus dem asynchronen FastAPI-Kontext NIEMALS
    direkt aufgerufen werden, sondern ausschliesslich ueber
    asyncio.to_thread() - siehe den ausfuehrlichen Kommentar in app.py
    und die Vorgeschichte in notifications/monitor.py (ein einziger
    uebersehener Blocking-Call hatte den Telegram-Bot schon einmal
    komplett eingefroren).
    """
    return monitor.fetch_live_prices_for_bots(bots)

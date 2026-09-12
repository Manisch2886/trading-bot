"""
Telegram-Nachricht bei jedem geschlossenen Trade
==============================================================================
Je geschlossenem Trade eine Nachricht mit dem Ergebnis: Bot, Symbol, PnL in
Prozent, Ein- und Ausstiegskurs, Haltedauer und der Ausstiegsgrund in
verstaendlicher Formulierung.

------------------------------------------------------------------------------
WARUM DAS EIN EIGENSTAENDIGES SKRIPT IST UND NICHT IM BOT HAENGT
------------------------------------------------------------------------------
`forward_test.py` und `live_params.py` werden in diesem Projekt nicht
angefasst - weder veraendert noch importiert. Das ist ein Grundsatz, nicht
eine Vorsichtsmassnahme fuer diesen Fall.

Deshalb dasselbe Muster wie `broker/spiegel.py`: ein Programm, das die
Bot-Datenbanken SCHREIBGESCHUETZT liest (ueber `broker/bot_db.py`, den einen
lesenden Zugang - nicht nachgebaut), neu geschlossene Trades erkennt, meldet
und in einer EIGENEN Datenbank vermerkt, was gemeldet wurde.

Der erwuenschte Nebeneffekt: faellt die Benachrichtigung aus, ist der
Bot-Betrieb davon unberuehrt. Und umgekehrt - ein haengender Bot-Lauf haelt
die Benachrichtigung nicht auf.

------------------------------------------------------------------------------
WAS HIER VORHER SCHON DA WAR - und was daran nicht reichte
------------------------------------------------------------------------------
`monitor.check_for_events()` hat Schliessungen bis zu dieser Aenderung
gemeldet, alle fuenf Minuten ueber den `poll_job` des Telegram-Dienstes. Diese
Zeilen sind mit dieser Aenderung entfernt worden (siehe den Hinweis dort), und
zwar aus drei Gruenden:

  1. INHALT. Dort stand der rohe Feldwert ("Ergebnis: stop_loss"), kein
     Einstiegskurs, kein Ausstiegskurs, keine Haltedauer.
  2. KEIN VERMERK JE TRADE. Erkannt wurde ueber einen Mengenvergleich gegen
     `notifications/state.json` - eine Momentaufnahme "welche Trades waren
     offen". Geht die Datei verloren, schreibt die Baseline-Logik still einen
     neuen Anfangszustand, und jede Schliessung dieses Fensters ist weg. Es
     gibt nichts, woraus sich rekonstruieren liesse, was schon gemeldet war.
  3. EIN FEHLGESCHLAGENER VERSAND GALT ALS ERLEDIGT. `poll_job` prueft den
     Rueckgabewert von `send_alert` nicht und speichert den Zustand danach in
     jedem Fall. Ist das Netz im falschen Moment weg, ist die Nachricht
     verloren und der Trade gilt als gemeldet.

Punkt 3 ist der eigentliche Anlass. Bei einer Cronjob-Warnung waere das
verzeihlich; bei "dein Stop-Loss hat ausgeloest" nicht.

------------------------------------------------------------------------------
DOPPELVERSAND: ANSPRUCH NEHMEN, DANN SENDEN, DANN BESTAETIGEN
------------------------------------------------------------------------------
Zwei Forderungen, die sich auf den ersten Blick widersprechen:

  * Ein abgebrochener Lauf darf beim naechsten Mal nicht dieselben
    Nachrichten erneut schicken.
  * Schlaegt der Versand fehl, darf der Trade NICHT als gemeldet vermerkt
    werden - er wird beim naechsten Lauf erneut versucht.

Nur eines von beiden geht mit "erst senden, dann vermerken" (dann duplizert
ein Abbruch) oder mit "erst vermerken, dann senden" (dann verschluckt ein
Fehlschlag). Deshalb drei Schritte:

  1. ANSPRUCH NEHMEN - eine Zeile mit `zustand='wird_gesendet'` einfuegen.
     Die Sperre ist `UNIQUE(bot, trade_id)`, also strukturell und nicht eine
     if-Abfrage: laufen zwei Laeufe gleichzeitig, bekommt genau einer den
     Anspruch, der andere ein IntegrityError und geht weiter.
  2. SENDEN.
  3. Erfolg  -> `zustand='gesendet'`.
     Fehlschlag -> die Zeile wird WIEDER GELOESCHT. Damit ist der Trade
     unvermerkt, und der naechste Lauf versucht ihn erneut.

Bleibt ein Lauf zwischen 2 und 3 stehen (Prozess abgeschossen, Strom weg),
steht die Zeile als `wird_gesendet` da. Sie zaehlt dann als vermerkt, der
Trade wird NICHT erneut gemeldet - so verlangt es die erste Forderung. Ob die
Nachricht wirklich rausging, ist in diesem einen Fall nicht bekannt; der
Zustand in der Nachverfolgung sagt genau das, statt es zu verschweigen
(`--status` zeigt es an).

------------------------------------------------------------------------------
DER ERSTE LAUF
------------------------------------------------------------------------------
In den neun Datenbanken liegen hunderte bereits geschlossene Trades. Die
duerfen nicht alle als Nachricht herausgehen.

Beim ersten Lauf wird der vorhandene Bestand deshalb STILLSCHWEIGEND als
erledigt vermerkt (`zustand='erstlauf_uebersprungen'`) und genau EINE
Bestaetigungsnachricht geschickt. Erst ab dann wird gemeldet.

Dass dieser Modus nicht versehentlich ein zweites Mal greift, haengt an zwei
Bedingungen, die BEIDE erfuellt sein muessen:

  * es gibt keine Marke `erstlauf_am` in der Zustandstabelle, UND
  * die Tabelle `gemeldet` ist vollstaendig leer.

Marke und Bestandszeilen entstehen in DERSELBEN Transaktion - es gibt keinen
Zwischenzustand, in dem das eine da ist und das andere fehlt. Und trifft der
seltene Fall ein, dass die Marke fehlt, aber Zeilen da sind (jemand hat die
Tabelle von Hand angefasst), wird der Erstlauf ABGELEHNT und laut gemeldet,
statt stillschweigend Schliessungen zu verschlucken.
"""

import argparse
import logging
import os
import sqlite3
import sys
import time
from datetime import datetime

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DIR)
for _pfad in (_DIR, os.path.join(BASE_DIR, "broker")):
    if _pfad not in sys.path:
        sys.path.insert(0, _pfad)

import bot_db                       # noqa: E402  broker/bot_db.py - nur lesend
import monitor                      # noqa: E402  Bot-Liste und Anzeigenamen

logger = logging.getLogger("notifications.schliess_benachrichtigung")


# ---------------------------------------------------------------------------
# Einstellungen
# ---------------------------------------------------------------------------
# EINZELN: eine Nachricht je geschlossenem Trade. Das hat der Nutzer gewaehlt -
# ein geschlossener Trade ist ein Ereignis, und ein Ereignis ist eine
# Nachricht. Man sieht am Handy sofort, worum es geht, ohne eine Liste zu
# lesen.
#
# GEBUENDELT: eine Nachricht je Lauf mit allen Schliessungen als Liste.
# Vorbereitet, damit sich das ohne neuen Pull Request umstellen laesst, falls
# es dem Nutzer zu viel wird. Beide Wege sind geprueft - eine vorbereitete,
# aber ungepruefte Option waere wertlos.
MODUS_EINZELN = "einzeln"
MODUS_GEBUENDELT = "gebuendelt"
BENACHRICHTIGUNG_MODUS = MODUS_EINZELN

# Obergrenze je Lauf im Einzelmodus. Schliesst ein Bot zwanzig Positionen in
# einem Lauf, gehen zwanzig Nachrichten raus - Telegram hat Sendegrenzen.
# Wird die Grenze ueberschritten, werden die ersten EINZELN gesendet und der
# Rest als EINE Sammelnachricht nachgereicht. Nichts faellt still unter den
# Tisch; das ist der Punkt an dieser Grenze.
MAX_EINZELN_PRO_LAUF = 25

# Kleine Pause zwischen zwei Nachrichten. Telegram erlaubt einem Bot rund 30
# Nachrichten je Sekunde an verschiedene Empfaenger, aber deutlich weniger an
# denselben Chat; eine Sekunde ist reichlich Abstand und kostet bei 25
# Nachrichten hoechstens 25 Sekunden - in einem 15-Minuten-Takt belanglos.
PAUSE_SEKUNDEN = 1.0

# Zustaende in der Nachverfolgung.
ZUSTAND_WIRD_GESENDET = "wird_gesendet"
ZUSTAND_GESENDET = "gesendet"
ZUSTAND_ERSTLAUF = "erstlauf_uebersprungen"

MARKE_ERSTLAUF = "erstlauf_am"


class BenachrichtigungFehler(Exception):
    """Der Lauf kann nicht durchgefuehrt werden. Es wurde nichts gesendet."""


# ---------------------------------------------------------------------------
# Die eigene Nachverfolgung
# ---------------------------------------------------------------------------
# EIGENE Datei, nicht die Bot-Datenbank: kein neues Feld, keine neue Tabelle
# im Bot-Schema. Eine gemeinsame Datei fuer alle neun Bots statt neun Dateien,
# weil `UNIQUE(bot, trade_id)` genau dann eine Sperre ueber alle ist und die
# Mengen winzig sind.

def db_pfad() -> str:
    return os.path.join(BASE_DIR, "benachrichtigungen_schliessung.db")


def oeffne_db(pfad: str = None):
    conn = sqlite3.connect(pfad or db_pfad())
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS gemeldet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot TEXT NOT NULL,
            trade_id INTEGER NOT NULL,
            symbol TEXT,
            pnl_pct REAL,
            zustand TEXT NOT NULL,
            zeitpunkt TEXT NOT NULL,
            -- DIE Absicherung gegen Doppelversand. Strukturell, nicht als
            -- if-Abfrage: auch zwei gleichzeitig gestartete Laeufe koennen
            -- denselben Trade nicht zweimal melden.
            UNIQUE(bot, trade_id)
        )""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS zustand (
            schluessel TEXT PRIMARY KEY,
            wert TEXT NOT NULL
        )""")
    conn.commit()
    return conn


def _marke(conn, schluessel: str):
    zeile = conn.execute("SELECT wert FROM zustand WHERE schluessel=?",
                          (schluessel,)).fetchone()
    return zeile["wert"] if zeile else None


def jetzt_text(jetzt=None) -> str:
    """Naives UTC im Format, das auch die Bots benutzen (siehe
    manual_close.jetzt_als_text) - eine einzelne Zeile mit abweichendem Format
    waere in Auswertungen ein Sonderfall, den niemand erwartet."""
    return (jetzt or datetime.utcnow()).strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------------------------
# Der Ausstiegsgrund in Klartext
# ---------------------------------------------------------------------------
# Die Werte stammen aus den `forward_test.py` der neun Bots. Sie wurden dort
# GELESEN (per ast, ohne Import) und stehen hier als Uebersetzungstabelle.
#
# Ein UNBEKANNTER Wert wird nicht verschluckt und nicht geraten, sondern
# woertlich durchgereicht und als unbekannt gekennzeichnet: kommt ein zehnter
# Bot mit einem neuen Ausstiegsweg, soll in der Nachricht der echte Wert
# stehen und nicht "Ausstieg".
AUSSTIEGSGRUENDE = {
    "stop_loss": "Stop-Loss ausgelöst",
    "take_profit": "Kursziel erreicht (Take-Profit)",
    "time_exit": "maximale Haltedauer erreicht",
    "sma_exit": "Ausstiegssignal: Kurs zurück über dem gleitenden Durchschnitt",
    "trend_flip": "Trendwechsel (SuperTrend hat gedreht)",
    "t3_crossunder": "Ausstiegssignal: T3-Linien gekreuzt",
    # Kein Bot schreibt diesen Wert - er entsteht nur beim manuellen
    # Schliessen ueber das Dashboard (notifications/manual_close.py).
    "manual_close": "von Hand geschlossen (Dashboard)",
}


def grundtext(result) -> str:
    if not result:
        return "Grund nicht vermerkt"
    bekannt = AUSSTIEGSGRUENDE.get(str(result))
    return bekannt if bekannt else f"{result} (unbekannter Ausstiegsweg)"


# ---------------------------------------------------------------------------
# Haltedauer
# ---------------------------------------------------------------------------
# Die Zeitstempel der Bots sind Kerzenzeiten, naiv und in unterschiedlichen
# Formen: "2026-09-01 04:00:00" bei den Stundenkerzen-Bots, "2026-09-01" bei
# den Tages-Bots. Beide Formen werden gelesen; alles andere fuehrt zu
# "unbekannt" statt zu einer geratenen Zahl.

def _als_zeit(wert):
    if not wert:
        return None
    text = str(wert).strip().replace("T", " ")
    for form in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(text[:len(datetime.now().strftime(form))], form)
        except ValueError:
            continue
    return None


def haltedauer_text(entry_time, exit_time) -> str:
    von, bis = _als_zeit(entry_time), _als_zeit(exit_time)
    if von is None or bis is None or bis < von:
        return "unbekannt"
    minuten = int((bis - von).total_seconds() // 60)
    tage, rest = divmod(minuten, 1440)
    stunden, minuten = divmod(rest, 60)
    teile = []
    if tage:
        teile.append(f"{tage} Tag" + ("e" if tage != 1 else ""))
    if stunden:
        teile.append(f"{stunden} Std.")
    if minuten and not tage:
        teile.append(f"{minuten} Min.")
    return " ".join(teile) if teile else "unter einer Minute"


# ---------------------------------------------------------------------------
# Die Nachricht
# ---------------------------------------------------------------------------
# KEINE Euro- oder Dollarbetraege. Die Bots tracken kein echtes Kapital; jeder
# Betrag waere aus einer Annahme abgeleitet und wuerde echter wirken, als er
# ist. Prozent ist die ehrliche Einheit.
#
# Zu Markdown: `notify.send_alert` benutzt Telegrams LEGACY-Markdown, und das
# kennt laut Bot-API KEIN Backslash-Escaping (ausfuehrlich im Docstring von
# notify.send_report - dort hat genau das einmal woertliche Backslashes beim
# Nutzer erzeugt). Ein Sternchen oder Unterstrich in einem Symbolnamen wuerde
# die Formatierung der ganzen Nachricht zerreissen. Weil Escaping nicht geht,
# werden die drei wirksamen Zeichen aus eingesetzten Werten ENTFERNT - das ist
# die einzige Mitigation, die in diesem Modus ueberhaupt greift.

MARKDOWN_WIRKSAM = "*_`"


def _sauber(wert) -> str:
    text = "–" if wert is None else str(wert)
    for zeichen in MARKDOWN_WIRKSAM:
        text = text.replace(zeichen, "")
    return text


def _kurs(wert) -> str:
    if wert is None:
        return "–"
    try:
        return f"{float(wert):.10g}"
    except (TypeError, ValueError):
        return _sauber(wert)


def _pnl(wert) -> str:
    """Mit Vorzeichen, immer. Ein PnL ohne Vorzeichen ist die eine Angabe,
    bei der ein fehlendes Zeichen die Aussage umdreht."""
    if wert is None:
        return "PnL nicht vermerkt"
    try:
        return f"{float(wert):+.2f} %"
    except (TypeError, ValueError):
        return _sauber(wert)


def _symbol_ergebnis(pnl):
    try:
        zahl = float(pnl)
    except (TypeError, ValueError):
        return "\U00002139"          # ℹ - kein Urteil ohne Zahl
    if zahl > 0:
        return "\U0001F7E2"          # gruener Kreis
    if zahl < 0:
        return "\U0001F534"          # roter Kreis
    return "\U000026AA"              # weisser Kreis


def nachricht_fuer(bot: str, trade: dict) -> str:
    """Die Nachricht zu EINEM geschlossenen Trade."""
    return (
        f"{_symbol_ergebnis(trade.get('pnl_pct'))} *Trade geschlossen* – "
        f"{_sauber(monitor.display_name(bot))}\n"
        f"*{_sauber(trade.get('symbol'))}*  ·  *{_pnl(trade.get('pnl_pct'))}*\n"
        f"Einstieg {_kurs(trade.get('entry_price'))} → "
        f"Ausstieg {_kurs(trade.get('exit_price'))}\n"
        f"Gehalten: {haltedauer_text(trade.get('entry_time'), trade.get('exit_time'))}\n"
        f"Grund: {_sauber(grundtext(trade.get('result')))}"
    )


def _zeile_kurz(bot: str, trade: dict) -> str:
    return (f"{_symbol_ergebnis(trade.get('pnl_pct'))} "
            f"{_sauber(monitor.display_name(bot))} · "
            f"*{_sauber(trade.get('symbol'))}* "
            f"*{_pnl(trade.get('pnl_pct'))}* – "
            f"{_sauber(grundtext(trade.get('result')))}")


def sammelnachricht(paare: list, kopf: str = None) -> str:
    """Eine Nachricht fuer mehrere Schliessungen. Benutzt im gebuendelten
    Modus und - unabhaengig davon - fuer den Rest oberhalb der Obergrenze."""
    anzahl = len(paare)
    titel = kopf or (f"*{anzahl} Trades geschlossen*" if anzahl != 1
                      else "*1 Trade geschlossen*")
    return titel + "\n\n" + "\n".join(_zeile_kurz(b, t) for b, t in paare)


# ---------------------------------------------------------------------------
# Lesen: welche Trades sind neu geschlossen?
# ---------------------------------------------------------------------------

def bot_liste() -> list:
    """Die neun Bots, aus der EINEN maschinenlesbaren Quelle des Projekts
    (notifications/monitor.py, ASSET_CLASS - so steht es im
    Uebergabeprotokoll, Abschnitt 2). Ein zehnter Bot wird dort eingetragen
    und ist damit auch hier bekannt."""
    return sorted(monitor.ASSET_CLASS)


def geschlossene_trades(bot: str, base_dir: str = None) -> list:
    """Alle geschlossenen Trades eines Bots, schreibgeschuetzt gelesen.

    Fehlt die Datenbank (Bot pausiert, noch nie gelaufen, laeuft auf einem
    anderen Rechner), ist das kein Fehler: die Liste ist leer.
    """
    try:
        alle = bot_db.lies_trades(bot, base_dir or BASE_DIR)
    except bot_db.BotDbFehler as fehler:
        logger.info(f"{bot}: {fehler}")
        return []
    return [t for t in alle if t.get("status") == "closed"]


def offene_meldungen(conn, base_dir: str = None) -> list:
    """(bot, trade)-Paare, die geschlossen sind und noch keinen Vermerk haben.

    Sortiert nach Bot und Trade-Nummer, damit die Reihenfolge der Nachrichten
    reproduzierbar ist - bei einem Abbruch mitten im Lauf holt der naechste
    Lauf genau dort weiter, wo dieser stehengeblieben ist.
    """
    vermerkt = {(z["bot"], z["trade_id"])
                for z in conn.execute("SELECT bot, trade_id FROM gemeldet")}
    offen = []
    for bot in bot_liste():
        for trade in geschlossene_trades(bot, base_dir):
            if (bot, trade["id"]) not in vermerkt:
                offen.append((bot, trade))
    return offen


# ---------------------------------------------------------------------------
# Vermerken: Anspruch nehmen, bestaetigen, freigeben
# ---------------------------------------------------------------------------

def anspruch_nehmen(conn, bot: str, trade: dict, jetzt=None) -> bool:
    """True, wenn dieser Lauf den Trade melden darf. False, wenn ihn ein
    anderer Lauf bereits hat - dann sagt das die UNIQUE-Sperre, nicht eine
    vorher gelesene Liste."""
    try:
        conn.execute(
            "INSERT INTO gemeldet (bot, trade_id, symbol, pnl_pct, zustand, "
            "zeitpunkt) VALUES (?,?,?,?,?,?)",
            (bot, trade["id"], trade.get("symbol"), trade.get("pnl_pct"),
             ZUSTAND_WIRD_GESENDET, jetzt_text(jetzt)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"{bot} Trade {trade['id']}: Anspruch liegt schon vor "
                       f"(UNIQUE) - wird nicht erneut gemeldet.")
        return False


def bestaetigen(conn, bot: str, trade_id: int) -> None:
    conn.execute("UPDATE gemeldet SET zustand=? WHERE bot=? AND trade_id=?",
                  (ZUSTAND_GESENDET, bot, trade_id))
    conn.commit()


def anspruch_freigeben(conn, bot: str, trade_id: int) -> None:
    """Nach einem fehlgeschlagenen Versand. Der Trade ist danach UNVERMERKT -
    genau das ist die Zusicherung: er kommt beim naechsten Lauf erneut."""
    conn.execute("DELETE FROM gemeldet WHERE bot=? AND trade_id=? AND zustand=?",
                  (bot, trade_id, ZUSTAND_WIRD_GESENDET))
    conn.commit()


# ---------------------------------------------------------------------------
# Der erste Lauf
# ---------------------------------------------------------------------------

def erstlauf_lage(conn) -> dict:
    """Ob der Erstlauf-Modus greift - und wenn nicht, warum nicht."""
    marke = _marke(conn, MARKE_ERSTLAUF)
    anzahl = conn.execute("SELECT COUNT(*) FROM gemeldet").fetchone()[0]
    if marke:
        return {"erstlauf": False, "grund": f"bereits erfolgt am {marke}",
                "widerspruch": False}
    if anzahl:
        # Marke fehlt, Zeilen sind da. Das kann der Erstlauf nicht erzeugt
        # haben (beides entsteht in einer Transaktion) - also hat jemand die
        # Tabelle angefasst. Ein Erstlauf wuerde hier den gesamten Bestand
        # als erledigt vermerken und damit echte Schliessungen verschlucken.
        return {"erstlauf": False, "widerspruch": True,
                "grund": (f"Die Marke '{MARKE_ERSTLAUF}' fehlt, aber es stehen "
                           f"{anzahl} Vermerke in der Tabelle. Der Erstlauf-Modus "
                           f"wird deshalb NICHT ausgefuehrt - er wuerde den "
                           f"vorhandenen Bestand stillschweigend als erledigt "
                           f"vermerken. Dieser Lauf meldet stattdessen normal "
                           f"weiter.")}
    return {"erstlauf": True, "grund": "keine Marke und keine Vermerke",
            "widerspruch": False}


def erstlauf_durchfuehren(conn, paare: list, senden, jetzt=None) -> dict:
    """Bestand stillschweigend vermerken, EINE Bestaetigung senden.

    Marke und Bestandszeilen entstehen in DERSELBEN Transaktion. Es gibt
    keinen Zwischenzustand, in dem das eine da ist und das andere fehlt -
    genau daran haengt, dass der Modus nicht ein zweites Mal greift.
    """
    zeitpunkt = jetzt_text(jetzt)
    with conn:                         # eine Transaktion, alles oder nichts
        conn.executemany(
            "INSERT OR IGNORE INTO gemeldet (bot, trade_id, symbol, pnl_pct, "
            "zustand, zeitpunkt) VALUES (?,?,?,?,?,?)",
            [(bot, t["id"], t.get("symbol"), t.get("pnl_pct"),
              ZUSTAND_ERSTLAUF, zeitpunkt) for bot, t in paare])
        conn.execute("INSERT OR REPLACE INTO zustand (schluessel, wert) "
                      "VALUES (?,?)", (MARKE_ERSTLAUF, zeitpunkt))

    text = (f"\U00002705 *Schliess-Benachrichtigung aktiv*\n"
            f"{len(paare)} bereits geschlossene Trades wurden als erledigt "
            f"vermerkt und werden NICHT nachgemeldet.\n"
            f"Ab jetzt kommt je geschlossenem Trade eine Nachricht.")
    gesendet = bool(senden(text))
    if not gesendet:
        # Der Vermerk bleibt trotzdem stehen: haetten wir ihn zurueckgerollt,
        # wuerde der naechste Lauf hunderte Nachrichten schicken - genau das,
        # was der Erstlauf verhindern soll. Die Bestaetigung ist eine
        # Hoeflichkeit, der Vermerk ist die Sache.
        logger.error("Die Bestaetigung des Erstlaufs liess sich nicht senden. "
                     "Der Bestand ist trotzdem vermerkt - sonst gingen beim "
                     "naechsten Lauf alle Nachrichten raus.")
    return {"erstlauf": True, "uebersprungen": len(paare),
            "bestaetigung_gesendet": gesendet, "gesendet": 0,
            "fehlgeschlagen": 0, "nicht_versucht": 0, "sammelnachricht": False}


# ---------------------------------------------------------------------------
# Ein ganzer Lauf
# ---------------------------------------------------------------------------

def _standard_senden(text: str) -> bool:
    # Erst hier importiert, damit ein Test den Sendeweg ersetzen kann, ohne
    # dass beim Modulimport Zugangsdaten gelesen werden.
    from notify import send_alert
    return send_alert(text)


def lauf(senden=None, conn=None, modus: str = None, base_dir: str = None,
         pause: float = None, grenze: int = None, jetzt=None) -> dict:
    """Ein vollstaendiger Durchgang.

    `senden`, `conn`, `base_dir` und `pause` sind Parameter, damit die Tests
    ohne Netz, ohne echte Bot-Datenbank und ohne Wartezeit laufen koennen -
    dasselbe Muster wie in broker/spiegel.py.
    """
    senden = senden or _standard_senden
    modus = modus or BENACHRICHTIGUNG_MODUS
    if modus not in (MODUS_EINZELN, MODUS_GEBUENDELT):
        raise BenachrichtigungFehler(
            f"Unbekannter Modus '{modus}'. Erlaubt: {MODUS_EINZELN}, "
            f"{MODUS_GEBUENDELT}. Es wurde nichts gesendet.")
    pause = PAUSE_SEKUNDEN if pause is None else pause
    grenze = MAX_EINZELN_PRO_LAUF if grenze is None else grenze

    eigene = conn is None
    conn = conn or oeffne_db()
    try:
        lage = erstlauf_lage(conn)
        paare = offene_meldungen(conn, base_dir)

        if lage["widerspruch"]:
            logger.error(lage["grund"])

        if lage["erstlauf"]:
            ergebnis = erstlauf_durchfuehren(conn, paare, senden, jetzt)
            ergebnis["modus"] = modus
            ergebnis["widerspruch"] = False
            return ergebnis

        if modus == MODUS_GEBUENDELT:
            ergebnis = _gebuendelt(conn, paare, senden, jetzt)
        else:
            ergebnis = _einzeln(conn, paare, senden, pause, grenze, jetzt)
        ergebnis.update({"erstlauf": False, "modus": modus,
                          "uebersprungen": 0,
                          "widerspruch": lage["widerspruch"]})
        return ergebnis
    finally:
        if eigene:
            conn.close()


def _einzeln(conn, paare, senden, pause, grenze, jetzt) -> dict:
    """Eine Nachricht je Trade - bis zur Obergrenze. Der Rest wird als EINE
    Sammelnachricht nachgereicht, damit nichts unter den Tisch faellt."""
    einzeln, rest = paare[:grenze], paare[grenze:]
    gesendet, fehlgeschlagen, nicht_versucht = 0, 0, 0

    for nummer, (bot, trade) in enumerate(einzeln):
        if not anspruch_nehmen(conn, bot, trade, jetzt):
            continue
        if senden(nachricht_fuer(bot, trade)):
            bestaetigen(conn, bot, trade["id"])
            gesendet += 1
        else:
            anspruch_freigeben(conn, bot, trade["id"])
            fehlgeschlagen += 1
            # ABBRUCH nach dem ersten Fehlschlag. Begruendung: send_alert
            # scheitert an Netz oder API, nicht am Inhalt einer einzelnen
            # Nachricht - der naechste Versuch scheitert also mit hoher
            # Wahrscheinlichkeit genauso, und 24 weitere Versuche mit je 10
            # Sekunden Zeitgrenze wuerden den Lauf minutenlang blockieren.
            # Verloren geht dabei nichts: die uebrigen Trades bleiben
            # unvermerkt und kommen beim naechsten Lauf dran.
            nicht_versucht = len(einzeln) - nummer - 1 + len(rest)
            logger.error(f"Versand fehlgeschlagen bei {bot} Trade "
                          f"{trade['id']} - Lauf abgebrochen, "
                          f"{nicht_versucht} Meldung(en) bleiben offen.")
            return {"gesendet": gesendet, "fehlgeschlagen": fehlgeschlagen,
                    "nicht_versucht": nicht_versucht, "sammelnachricht": False,
                    "bestaetigung_gesendet": None}

    sammel = False
    if rest:
        sammel = _sammeln(conn, rest, senden, jetzt,
                           kopf=(f"*{len(rest)} weitere Trades geschlossen*\n"
                                  f"(zusammengefasst, weil in diesem Lauf mehr "
                                  f"als {grenze} Schließungen angefallen sind)"))
        if sammel:
            gesendet += len(rest)
        else:
            fehlgeschlagen += 1
            nicht_versucht += len(rest)
    return {"gesendet": gesendet, "fehlgeschlagen": fehlgeschlagen,
            "nicht_versucht": nicht_versucht, "sammelnachricht": sammel,
            "bestaetigung_gesendet": None}


def _gebuendelt(conn, paare, senden, jetzt) -> dict:
    if not paare:
        return {"gesendet": 0, "fehlgeschlagen": 0, "nicht_versucht": 0,
                "sammelnachricht": False, "bestaetigung_gesendet": None}
    erfolg = _sammeln(conn, paare, senden, jetzt)
    return {"gesendet": len(paare) if erfolg else 0,
            "fehlgeschlagen": 0 if erfolg else 1,
            "nicht_versucht": 0 if erfolg else len(paare),
            "sammelnachricht": erfolg, "bestaetigung_gesendet": None}


def _sammeln(conn, paare, senden, jetzt, kopf=None) -> bool:
    """Anspruch fuer ALLE nehmen, EINE Nachricht senden, alle bestaetigen -
    oder alle wieder freigeben. Dieselbe Reihenfolge wie im Einzelmodus, nur
    mit einer Nachricht fuer die ganze Gruppe."""
    genommen = [(bot, t) for bot, t in paare
                if anspruch_nehmen(conn, bot, t, jetzt)]
    if not genommen:
        return False
    if senden(sammelnachricht(genommen, kopf)):
        for bot, trade in genommen:
            bestaetigen(conn, bot, trade["id"])
        return True
    for bot, trade in genommen:
        anspruch_freigeben(conn, bot, trade["id"])
    return False


def meldung(z: dict) -> str:
    if z.get("erstlauf"):
        return (f"Erstlauf: {z['uebersprungen']} bestehende Trades als erledigt "
                f"vermerkt, keine Nachmeldung. Bestaetigung "
                f"{'gesendet' if z['bestaetigung_gesendet'] else 'NICHT gesendet'}.")
    teile = [f"{z['gesendet']} Meldung(en) gesendet ({z['modus']})"]
    if z.get("sammelnachricht"):
        teile.append("darunter eine Sammelnachricht")
    if z.get("fehlgeschlagen"):
        teile.append(f"{z['fehlgeschlagen']} Versand(e) fehlgeschlagen")
    if z.get("nicht_versucht"):
        teile.append(f"{z['nicht_versucht']} bleiben offen fuer den naechsten Lauf")
    if z.get("widerspruch"):
        teile.append("WARNUNG: Erstlauf-Marke fehlt bei vorhandenen Vermerken")
    return "; ".join(teile) + "."


# ---------------------------------------------------------------------------
# Kommandozeile
# ---------------------------------------------------------------------------

def _status() -> int:
    conn = oeffne_db()
    try:
        lage = erstlauf_lage(conn)
        print(f"Nachverfolgung: {db_pfad()}")
        print(f"Erstlauf: {'noch offen' if lage['erstlauf'] else lage['grund']}")
        if lage["widerspruch"]:
            print("  ACHTUNG: " + lage["grund"])
        for zustand in (ZUSTAND_GESENDET, ZUSTAND_WIRD_GESENDET, ZUSTAND_ERSTLAUF):
            anzahl = conn.execute("SELECT COUNT(*) FROM gemeldet WHERE zustand=?",
                                   (zustand,)).fetchone()[0]
            print(f"  {zustand:<24} {anzahl}")
        haengend = conn.execute(
            "SELECT bot, trade_id, zeitpunkt FROM gemeldet WHERE zustand=? "
            "ORDER BY id", (ZUSTAND_WIRD_GESENDET,)).fetchall()
        if haengend:
            print("\nBei diesen ist unklar, ob die Nachricht rausging (ein Lauf "
                  "wurde zwischen Senden und Bestaetigen abgebrochen):")
            for z in haengend:
                print(f"  {z['bot']} Trade {z['trade_id']} ({z['zeitpunkt']})")
        offen = offene_meldungen(conn)
        print(f"\nNoch nicht gemeldet: {len(offen)}")
        for bot, trade in offen[:20]:
            print(f"  {bot} Trade {trade['id']:>5} {trade.get('symbol')} "
                  f"{trade.get('pnl_pct')}%")
        return 0
    finally:
        conn.close()


def _trockenlauf(modus: str) -> int:
    """Zeigt, WAS gesendet wuerde. Vermerkt nichts und sendet nichts."""
    conn = oeffne_db()
    try:
        paare = offene_meldungen(conn)
        lage = erstlauf_lage(conn)
        if lage["erstlauf"]:
            print(f"ERSTLAUF: {len(paare)} bestehende Trades wuerden "
                  f"stillschweigend vermerkt, eine Bestaetigung gesendet.")
            return 0
        if not paare:
            print("Nichts zu melden.")
            return 0
        if modus == MODUS_GEBUENDELT:
            print(sammelnachricht(paare))
            return 0
        for bot, trade in paare[:MAX_EINZELN_PRO_LAUF]:
            print(nachricht_fuer(bot, trade))
            print("-" * 40)
        rest = paare[MAX_EINZELN_PRO_LAUF:]
        if rest:
            print(sammelnachricht(rest, kopf=f"*{len(rest)} weitere*"))
        return 0
    finally:
        conn.close()


def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    zerleger = argparse.ArgumentParser(
        description="Schickt je geschlossenem Trade eine Telegram-Nachricht. "
                    "Liest die Bot-Datenbanken ausschliesslich lesend.")
    zerleger.add_argument("--modus", choices=[MODUS_EINZELN, MODUS_GEBUENDELT],
                          default=BENACHRICHTIGUNG_MODUS,
                          help=f"Standard: {BENACHRICHTIGUNG_MODUS}")
    gruppe = zerleger.add_mutually_exclusive_group()
    gruppe.add_argument("--status", action="store_true",
                        help="Nachverfolgung anzeigen, nichts senden")
    gruppe.add_argument("--trockenlauf", action="store_true",
                        help="zeigen, was gesendet wuerde - sendet nichts und "
                             "vermerkt nichts")
    args = zerleger.parse_args(argv)

    if args.status:
        return _status()
    if args.trockenlauf:
        return _trockenlauf(args.modus)

    try:
        z = lauf(modus=args.modus)
    except BenachrichtigungFehler as fehler:
        logger.error(str(fehler))
        return 1
    logger.info(meldung(z))
    # Rueckgabewert 1, wenn ein Versand fehlgeschlagen ist - damit der Cronjob
    # per Mail anschlaegt. Ein stiller Fehlschlag waere hier genau das
    # Problem, das dieses Skript loesen soll (siehe Modul-Kopf, Punkt 3).
    return 1 if z.get("fehlgeschlagen") else 0


if __name__ == "__main__":
    sys.exit(main())

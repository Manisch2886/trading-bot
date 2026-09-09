"""
Manuelles Schliessen einer offenen Position (Telegram Phase 3)
==============================================================================
Das erste Stueck dieses Projekts, das in die LIVE-Datenbank eines Bots
SCHREIBT. Alles hier ist entsprechend defensiv gebaut.

Was dieses Modul NICHT tut:
  * Es faengt keinen Bot-Prozess ab und ruft nichts in forward_test.py auf -
    geschrieben wird ausschliesslich direkt in die SQLite-Datei.
  * Es eroeffnet keine Positionen. Es gibt keinen Codepfad, der eine Zeile
    einfuegt; das einzige Schreib-Statement ist ein UPDATE mit
    `status='open'` in der WHERE-Klausel.
  * Es entscheidet nichts selbst. Aufgerufen wird es erst, nachdem der
    Nutzer zweimal unabhaengig bestaetigt hat (siehe telegram_bot.py).

------------------------------------------------------------------------------
Warum t3_supertrend als erster und vorerst einziger Bot
------------------------------------------------------------------------------
1. EINFACHSTES SCHEMA. Seine trades-Tabelle hat nur die elf Spalten, die
   fuenf Bots gemeinsam haben - keine bot-eigenen Zusatzspalten wie
   `rsi_at_entry` (rsi2-Bots) oder `target_price`/`fib_score` (Elliott).
   Was hier funktioniert, laesst sich auf die uebrigen vier dieser Gruppe
   uebertragen, ohne dass eine Sonderbehandlung noetig wird.
2. KLEINSTE ANGRIFFSFLAECHE. MAX_CONCURRENT_POSITIONS = 5 ist das
   niedrigste Limit aller neun Bots; hoechstens fuenf Positionen koennen
   ueberhaupt betroffen sein.
3. KRYPTO STATT AKTIEN. Der Kurs kommt von Binance und ist rund um die Uhr
   verfuegbar. Die Aktien-Bots haengen an yfinance und an Boersenzeiten -
   ein manuelles Schliessen ausserhalb der Handelszeiten haette dort
   keinen belastbaren Ausstiegskurs, und ohne Kurs darf nicht geschrieben
   werden.
4. SELTENSTER SCHREIBER. Der Cronjob laeuft alle 4 Stunden
   (monitor.EXPECTED_INTERVAL_HOURS) - unter den Krypto-Bots das breiteste
   Fenster zwischen zwei Laeufen und damit die kleinste Chance, ausgerechnet
   gleichzeitig zu schreiben. elliott_wave laeuft stuendlich.
5. EINFACHE AUSSTIEGS-BUCHHALTUNG. Eine einzige PnL-Formel, kein
   Teilausstieg, kein Take-Profit-Zweig.

Weitere Bots werden in SCHLIESSBARE_BOTS ergaenzt - mehr ist dafuer nicht
noetig, solange sie dasselbe Schema haben.

------------------------------------------------------------------------------
Nebenlaeufigkeit: der Cronjob koennte GENAU JETZT schreiben
------------------------------------------------------------------------------
`forward_test.py` des Bots kann jederzeit anlaufen und dieselbe Zeile
schliessen wollen. Drei Massnahmen, die zusammen wirken:

  1. `BEGIN IMMEDIATE` - fordert die Schreibsperre SOFORT an, nicht erst
     beim ersten UPDATE. Ohne das beginnt SQLite die Transaktion im
     Lesemodus und versucht erst spaeter hochzustufen; genau dort entsteht
     das klassische "database is locked" MITTEN in einer bereits
     halb gelesenen Transaktion.
  2. `busy_timeout` - laeuft der Cronjob gerade, wird gewartet statt
     sofort abzubrechen. Laeuft er laenger als das Timeout, bricht das
     Schliessen sauber ab und meldet das; es wird nichts halb geschrieben.
  3. ERNEUTE PRUEFUNG INNERHALB der Transaktion. Das ist die wichtigste:
     zwischen dem Anzeigen der Positionsliste und der zweiten Bestaetigung
     vergehen Sekunden bis Minuten. Faellt der Cronjob in dieses Fenster
     und schliesst die Position selbst, ist sie beim Zugriff hier nicht
     mehr offen - dann wird NICHT geschrieben, sondern abgebrochen. Eine
     Sperre allein wuerde das nicht verhindern, sie wuerde nur beide
     Schreibvorgaenge nacheinander ausfuehren.

Zusaetzlich traegt das UPDATE `status='open'` in seiner WHERE-Klausel und
prueft `rowcount == 1`: selbst wenn die Pruefung oben umgangen wuerde,
kann keine bereits geschlossene Zeile ein zweites Mal geschlossen werden.
"""

import ast
import logging
import os
import sqlite3
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler

_NOTIF_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_NOTIF_DIR)
STRATEGIES_DIR = os.path.join(BASE_DIR, "strategies")

# Wie lange auf eine fremde Schreibsperre gewartet wird. Grosszuegig
# bemessen: ein Cronjob-Lauf dieser Bots schreibt in Bruchteilen einer
# Sekunde, aber die Datei koennte auf einem langsamen Datentraeger liegen.
SPERR_TIMEOUT_SEKUNDEN = 15

# Der Wert, der in der result-Spalte landet. Bewusst ein Name, den kein
# Bot selbst je schreibt (dort: stop_loss, trend_flip, t3_crossunder, ...),
# damit ein manueller Eingriff in der Datenbank fuer immer als solcher
# erkennbar bleibt.
MANUELLER_GRUND = "manual_close"

# Der Text, den der Nutzer als ZWEITE Bestaetigung eintippen muss.
# EXAKT so, mit Grossbuchstaben - verglichen wird case-SENSITIV (nur
# umschliessende Leerzeichen werden entfernt). Bewusst streng, obwohl
# "bestaetigen" durchzulassen bequemer waere: der Text-Handler in
# telegram_bot.py sieht JEDE freie Nachricht, solange eine Bestaetigung
# aussteht. Waere der Vergleich unempfindlich gegen Gross-/Kleinschreibung,
# koennte ein beilaeufig getipptes "bestaetigen" eine Position schliessen.
# Der Preis dafuer ist eine Wiederholung des Ablaufs bei einem Tippfehler -
# gegenueber einem ungewollten Schreibzugriff der guenstigere Fehler.
BESTAETIGUNGSTEXT = "BESTAETIGEN"

# Zentrale Liste - hier kommen spaetere Bots dazu. Nur was hier steht,
# laesst sich ueberhaupt schliessen; jeder andere Name wird abgelehnt.
SCHLIESSBARE_BOTS = {
    "t3_supertrend": {
        "anzeigename": "T3/ADX/SuperTrend (Krypto)",
        "anlageklasse": "krypto",
    },
}


# ---------------------------------------------------------------------------
# Protokoll der manuellen Eingriffe
# ---------------------------------------------------------------------------
# EIGENE Datei, nicht telegram_bot.log: ein Eingriff, der in eine
# Live-Datenbank schreibt, soll sich nicht zwischen hunderten Zeilen
# Netzwerk- und Diagnoseausgabe verstecken. Jede Zeile beginnt mit
# "MANUELLER-EINGRIFF" - so ist auch beim Zusammenkopieren mehrerer
# Logdateien auf einen Blick unterscheidbar, was ein Mensch ausgeloest hat
# und was der Cronjob.
#
# Protokolliert wird BEIDES: erfolgreiche UND abgelehnte Versuche. Ein
# abgelehnter Versuch ist die interessantere Zeile - er verraet, dass
# jemand etwas wollte, das nicht ging.
PROTOKOLL_DIR = os.path.join(BASE_DIR, "logs", "notifications")
PROTOKOLL_DATEI = os.path.join(PROTOKOLL_DIR, "manuelle_eingriffe.log")

_protokoll = logging.getLogger("manuelle_eingriffe")
_protokoll.setLevel(logging.INFO)
_protokoll.propagate = False
if not _protokoll.handlers:
    os.makedirs(PROTOKOLL_DIR, exist_ok=True)
    _griff = RotatingFileHandler(PROTOKOLL_DATEI, maxBytes=1_000_000,
                                  backupCount=5, encoding="utf-8")
    _griff.setFormatter(logging.Formatter(
        "%(asctime)s MANUELLER-EINGRIFF %(message)s"))
    _protokoll.addHandler(_griff)


def _zustand_kurz(zeile: dict) -> str:
    """Die fuer den Nachvollzug wesentlichen Felder einer Trade-Zeile."""
    if not zeile:
        return "-"
    return (f"status={zeile.get('status')} result={zeile.get('result')} "
            f"exit_time={zeile.get('exit_time')} "
            f"exit_price={zeile.get('exit_price')} "
            f"pnl_pct={zeile.get('pnl_pct')}")


def protokolliere_erfolg(ergebnis: dict) -> None:
    _protokoll.info(
        "ERFOLGREICH bot=%s trade_id=%s symbol=%s benutzer=%s "
        "bestaetigung=%s | VORHER %s | NACHHER %s",
        ergebnis["bot"], ergebnis["trade_id"], ergebnis["symbol"],
        ergebnis["benutzer_id"], BESTAETIGUNGSTEXT,
        _zustand_kurz(ergebnis["vorher"]), _zustand_kurz(ergebnis["nachher"]))


def protokolliere_ablehnung(bot_name, trade_id, benutzer_id, grund: str) -> None:
    _protokoll.warning(
        "ABGELEHNT bot=%s trade_id=%s benutzer=%s grund=%s | "
        "Datenbank unveraendert",
        bot_name, trade_id, benutzer_id, grund)


class SchliessenNichtMoeglich(Exception):
    """Fachlicher Abbruch mit einer Meldung, die dem Nutzer gezeigt werden
    darf. Wird an jeder Stelle geworfen, an der NICHT geschrieben wird -
    ein solcher Abbruch laesst die Datenbank garantiert unveraendert."""


def _pfade(bot_name: str) -> dict:
    if bot_name not in SCHLIESSBARE_BOTS:
        raise SchliessenNichtMoeglich(
            f"Fuer '{bot_name}' ist das manuelle Schliessen nicht freigeschaltet. "
            f"Freigeschaltet: {', '.join(sorted(SCHLIESSBARE_BOTS))}.")
    return {
        "db": os.path.join(BASE_DIR, f"paper_trading_{bot_name}.db"),
        "forward_test": os.path.join(STRATEGIES_DIR, bot_name, "forward_test.py"),
    }


def kostensatz(bot_name: str) -> float:
    """Die Kosten, die der Bot beim Schliessen von der Rendite abzieht - in
    Prozentpunkten, also bereits `2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)`.

    Gelesen wird das aus dem QUELLTEXT von forward_test.py per AST, nicht
    hier noch einmal hingeschrieben. Grund: die Aufgabe verlangt, die
    PnL-Rechnung des Bots exakt nachzubilden statt sie neu zu erfinden -
    und eine zweite Kopie der Zahl waere genau die Doppelfuehrung, die in
    diesem Projekt schon einmal dazu gefuehrt hat, dass zwei Seiten
    unbemerkt auseinanderliefen. AST statt Import: forward_test.py laedt
    beim Importieren binance und Kursdaten, was hier weder noetig noch
    erwuenscht ist."""
    pfad = _pfade(bot_name)["forward_test"]
    with open(pfad, encoding="utf-8") as fh:
        baum = ast.parse(fh.read(), filename=pfad)

    werte = {}
    for knoten in baum.body:
        if not isinstance(knoten, ast.Assign):
            continue
        for ziel in knoten.targets:
            if isinstance(ziel, ast.Name) and ziel.id in ("TRADING_FEE_PCT",
                                                           "SLIPPAGE_PCT"):
                try:
                    werte[ziel.id] = float(ast.literal_eval(knoten.value))
                except (ValueError, SyntaxError, TypeError):
                    pass

    fehlend = {"TRADING_FEE_PCT", "SLIPPAGE_PCT"} - set(werte)
    if fehlend:
        raise SchliessenNichtMoeglich(
            f"In {os.path.basename(pfad)} fehlen {sorted(fehlend)} - ohne die "
            f"Kostensaetze des Bots laesst sich sein PnL nicht nachbilden.")
    return 2 * (werte["TRADING_FEE_PCT"] + werte["SLIPPAGE_PCT"])


def berechne_pnl(bot_name: str, entry_price: float, exit_price: float) -> float:
    """Woertlich die Rechnung aus forward_test.py::check_open_trades():

        pnl_pct = (exit_price - entry_price) / entry_price * 100
        pnl_pct -= 2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)
        ... round(pnl_pct, 2)

    Auch die Rundung auf zwei Stellen gehoert dazu - der Bot speichert
    gerundet, und eine manuell geschlossene Zeile soll sich in nichts von
    einer automatisch geschlossenen unterscheiden ausser im Grund."""
    if not entry_price:
        raise SchliessenNichtMoeglich("Einstiegskurs fehlt oder ist 0 - "
                                       "PnL nicht berechenbar.")
    pnl = (exit_price - entry_price) / entry_price * 100
    pnl -= kostensatz(bot_name)
    return round(pnl, 2)


def _verbindung(db_pfad: str):
    if not os.path.exists(db_pfad):
        raise SchliessenNichtMoeglich(
            f"Datenbank {os.path.basename(db_pfad)} nicht gefunden.")
    # isolation_level=None: die Transaktionen werden hier ausdruecklich
    # selbst gesteuert (BEGIN IMMEDIATE), nicht von Pythons Automatik.
    conn = sqlite3.connect(db_pfad, timeout=SPERR_TIMEOUT_SEKUNDEN,
                            isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute(f"PRAGMA busy_timeout = {int(SPERR_TIMEOUT_SEKUNDEN * 1000)}")
    return conn


def offene_positionen(bot_name: str) -> list:
    """Die offenen Positionen des Bots - rein lesend, mit der Zeilen-ID.

    monitor.get_bot_status() liefert die ID nicht mit; sie wird hier aber
    gebraucht, weil ausschliesslich ueber die ID geschlossen wird (nicht
    ueber das Symbol - ein Bot kann dasselbe Symbol theoretisch mehrfach
    offen haben, und dann waere 'schliesse BTCUSDT' mehrdeutig)."""
    pfade = _pfade(bot_name)
    conn = _verbindung(pfade["db"])
    try:
        zeilen = conn.execute(
            "SELECT id, symbol, entry_time, entry_price, stop_price "
            "FROM trades WHERE status='open' ORDER BY id"
        ).fetchall()
    finally:
        conn.close()
    return [dict(z) for z in zeilen]


def jetzt_als_text() -> str:
    """Zeitstempel im selben Format, das die Bots schreiben:
    'YYYY-MM-DD HH:MM:SS' aus str(pandas.Timestamp), naiv in UTC. Bewusst
    kein Offset - die Bots fuehren ihre Kerzenzeiten ebenso, und eine
    einzelne Zeile mit abweichendem Format waere in Auswertungen ein
    Sonderfall, den niemand erwartet."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def schliesse_position(bot_name: str, trade_id: int, exit_price: float,
                        benutzer_id, bestaetigungstext: str,
                        jetzt: str = None) -> dict:
    """Schliesst GENAU EINE offene Position. Schreibt nur, wenn jede
    Vorbedingung haelt; gibt den Zustand vorher und nachher zurueck.

    bestaetigungstext wird hier NOCH EINMAL geprueft, obwohl telegram_bot.py
    das bereits tut. Doppelt, weil diese Funktion die einzige Stelle im
    Projekt ist, die schreibt: wer sie kuenftig von woanders aufruft, soll
    die Bestaetigung nicht umgehen koennen, nur weil er den Telegram-Weg
    nicht nimmt."""
    try:
        return _schliesse_position_ungeschuetzt(
            bot_name, trade_id, exit_price, benutzer_id, bestaetigungstext, jetzt)
    except SchliessenNichtMoeglich as fehler:
        # Auch der ABGELEHNTE Versuch gehoert ins Protokoll - er ist die
        # interessantere Zeile von beiden. Danach unveraendert weiterwerfen,
        # damit der Aufrufer die Meldung dem Nutzer zeigen kann.
        protokolliere_ablehnung(bot_name, trade_id, benutzer_id, str(fehler))
        raise


def _schliesse_position_ungeschuetzt(bot_name, trade_id, exit_price,
                                      benutzer_id, bestaetigungstext, jetzt):
    """Der eigentliche Ablauf. Getrennt, damit schliesse_position() jede
    Ablehnung protokollieren kann, ohne dass hier an jeder einzelnen
    raise-Stelle daran gedacht werden muss - vergessen waere hier genau
    die Luecke, die man spaeter nicht bemerkt."""
    if (bestaetigungstext or "").strip() != BESTAETIGUNGSTEXT:
        raise SchliessenNichtMoeglich(
            f"Bestaetigungstext stimmt nicht - erwartet wird genau "
            f"'{BESTAETIGUNGSTEXT}', Gross-/Kleinschreibung inbegriffen. "
            f"Es wurde nichts geaendert.")
    if exit_price is None or exit_price <= 0:
        raise SchliessenNichtMoeglich(
            "Kein gueltiger Ausstiegskurs vorhanden. Ohne Kurs wird nicht "
            "geschrieben.")

    pfade = _pfade(bot_name)
    exit_time = jetzt or jetzt_als_text()
    conn = _verbindung(pfade["db"])
    try:
        try:
            conn.execute("BEGIN IMMEDIATE")
        except sqlite3.OperationalError as fehler:
            raise SchliessenNichtMoeglich(
                f"Die Datenbank ist gerade gesperrt ({fehler}) - vermutlich "
                f"laeuft der Cronjob des Bots. Es wurde nichts geaendert; "
                f"bitte in einer Minute erneut versuchen.")

        try:
            vorher = conn.execute(
                "SELECT * FROM trades WHERE id=?", (trade_id,)).fetchone()
            if vorher is None:
                raise SchliessenNichtMoeglich(
                    f"Kein Trade mit ID {trade_id} in der Datenbank.")
            vorher = dict(vorher)
            if vorher["status"] != "open":
                raise SchliessenNichtMoeglich(
                    f"Der Trade {trade_id} ({vorher['symbol']}) ist nicht mehr "
                    f"offen - Status '{vorher['status']}', Grund "
                    f"'{vorher['result']}'. Vermutlich hat der Cronjob ihn "
                    f"inzwischen selbst geschlossen. Es wurde nichts geaendert.")

            pnl = berechne_pnl(bot_name, vorher["entry_price"], exit_price)

            cursor = conn.execute(
                "UPDATE trades SET exit_time=?, exit_price=?, result=?, "
                "pnl_pct=?, status='closed' WHERE id=? AND status='open'",
                (exit_time, exit_price, MANUELLER_GRUND, pnl, trade_id))
            if cursor.rowcount != 1:
                # Kann nach der Pruefung oben eigentlich nicht mehr eintreten;
                # bleibt als letzte Absicherung stehen, weil ein UPDATE, das
                # mehr oder weniger als eine Zeile trifft, in dieser Funktion
                # immer ein Fehler ist.
                raise SchliessenNichtMoeglich(
                    f"UPDATE haette {cursor.rowcount} Zeilen getroffen statt "
                    f"genau einer - abgebrochen, nichts geaendert.")

            nachher = dict(conn.execute(
                "SELECT * FROM trades WHERE id=?", (trade_id,)).fetchone())
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
    finally:
        conn.close()

    ergebnis = {
        "bot": bot_name,
        "trade_id": trade_id,
        "symbol": vorher["symbol"],
        "entry_price": vorher["entry_price"],
        "exit_price": exit_price,
        "exit_time": exit_time,
        "pnl_pct": pnl,
        "result": MANUELLER_GRUND,
        "benutzer_id": benutzer_id,
        "vorher": vorher,
        "nachher": nachher,
    }
    protokolliere_erfolg(ergebnis)
    return ergebnis

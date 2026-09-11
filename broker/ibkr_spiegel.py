"""
Die IBKR-Bruecke: Paper-Trades eines Aktien-Bots auf dem Paper-Konto spiegeln
==============================================================================
Gegenstueck zu broker/spiegel.py (Binance-Testnet), fuer den Aktien-Bot
`volatility_breakout`:

    status='open'   ohne Spiegelung      ->  MARKET BUY
    status='closed' mit Kauf-Spiegelung  ->  MARKET SELL derselben Stueckzahl

forward_test.py, live_params.py und die trades-Tabelle des Bots bleiben
unangetastet; gelesen wird ueber broker/bot_db.py mit `mode=ro`. Die eigene
Nachverfolgung liegt in broker_ibkr_volatility_breakout.db.

------------------------------------------------------------------------------
WARUM volatility_breakout ALS ERSTER AKTIEN-BOT
------------------------------------------------------------------------------
Dieselben Kriterien wie bei der Schliessen-Funktion und der Binance-Bruecke,
und sie zeigen auf diesen Bot:

  * SCHEMA: identische elf Spalten wie t3_supertrend, KEINE Zusatzspalten -
    genau wie turtle_soup_stocks, und damit beide einfachste Wahl.
  * POSITIONSLIMIT: MAX_CONCURRENT_POSITIONS=15. turtle_soup_stocks hat
    BEWUSST keines (bei 2 % Allokation saettigt die Kapitalbindung erst bei
    rund 50 offenen Positionen, Protokoll 3.4). Fuer eine erste Broker-Anbindung
    ist eine nach oben begrenzte Zahl gleichzeitiger Positionen der
    entscheidende Unterschied: sie begrenzt auch die Zahl der Orders.
  * HANDELSFREQUENZ: im Backtest ueber dasselbe Universum 1236 ausgefuehrte
    Trades gegen 1887 bei turtle_soup_stocks (Out-of-Sample 385 gegen 575,
    results/*/PROTOTYPE_FINDINGS.md). Rund ein Drittel weniger Orders.
  * AUSSTIEGE: zwei klar benannte Wege (stop_loss zum Stop-Preis, time_exit zum
    Schlusskurs). turtle_soup_stocks hat STOP_MODE=None, dort traegt der
    Zeit-Exit allein - weniger Abwechslung, aber auch weniger Aussagekraft
    darueber, ob die Bruecke beide Ausstiegsarten richtig spiegelt.
  * Die Positionsgroesse ist in live_params.py dokumentiert (10 %).

Die beiden Elliott- und RSI-Bots haben Zusatzspalten (target_price/fib_score
bzw. rsi_at_entry) und fallen nach demselben Kriterium wie bei PR #66 hinten an.

------------------------------------------------------------------------------
DER GROSSE UNTERSCHIED ZU KRYPTO: DIE BOERSE IST MEISTENS ZU
------------------------------------------------------------------------------
Der Bot arbeitet auf TAGESKERZEN und rechnet mit dem SCHLUSSKURS. Laeuft sein
Cronjob nach dem US-Schluss, entstehen seine Signale, wenn die Boerse
geschlossen ist. Eine Market-Order ist dann bei IBKR nicht vorgesehen.

Diese Bruecke raet nicht, was IBKR in diesem Fall tut, sondern sendet GAR
NICHT: sie liest die regulaeren Handelszeiten des Kontrakts bei IBKR selbst ab
(liquidHours) und laesst die Aufgabe stehen, bis die Boerse offen ist. Der
naechste Lauf innerhalb der Sitzung erledigt sie.

Folge, die im Abgleich sichtbar wird und die man kennen muss: der Kauf findet
in der naechsten Sitzung statt, nicht zum Schlusskurs des Signaltags. Die
Differenz ist die UEBERNACHT-LUECKE - kein Fehler der Bruecke, sondern die
Grenze dessen, was sich an einer Tagesstrategie ueberhaupt spiegeln laesst.
Siehe broker/README_IBKR.md, Abschnitt zu den Handelszeiten.

------------------------------------------------------------------------------
AUFRUF
------------------------------------------------------------------------------
    python3 broker/ibkr_spiegel.py --pruefen       Verbindung, Konto, nur lesend
    python3 broker/ibkr_spiegel.py --zeitfenster AAPL   Handelszeiten laut IBKR
    python3 broker/ibkr_spiegel.py                 TROCKENLAUF (Standard)
    python3 broker/ibkr_spiegel.py --echt          sendet wirklich Orders
    python3 broker/ibkr_spiegel.py --status        Aufgaben und Nachverfolgung
"""

import argparse
import json
import logging
import os
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from logging.handlers import RotatingFileHandler

_BROKER_DIR = os.path.dirname(os.path.abspath(__file__))
if _BROKER_DIR not in sys.path:
    sys.path.insert(0, _BROKER_DIR)

import bot_db                               # noqa: E402
import ibkr_zugang as zugang                 # noqa: E402
import ibkr_paper as ip                      # noqa: E402

BASE_DIR = zugang.BASE_DIR

# Genau EIN Bot, wie bei der Binance-Bruecke. Weitere erst nach Bewaehrung und
# dann einzeln geprueft.
ERLAUBTE_BOTS = ("volatility_breakout",)

SEITE_EROEFFNUNG = "eroeffnung"
SEITE_SCHLIESSUNG = "schliessung"

PROTOKOLL_DIR = os.path.join(BASE_DIR, "logs", "broker")
PROTOKOLL_DATEI = os.path.join(PROTOKOLL_DIR, "ibkr_paper_spiegel.log")

logger = logging.getLogger("broker.ibkr_spiegel")
logger.setLevel(logging.INFO)
logger.propagate = False
if not logger.handlers:
    os.makedirs(PROTOKOLL_DIR, exist_ok=True)
    _griff = RotatingFileHandler(PROTOKOLL_DATEI, maxBytes=1_000_000,
                                  backupCount=5, encoding="utf-8")
    _griff.setFormatter(logging.Formatter("%(asctime)s IBKR-PAPER %(message)s"))
    logger.addHandler(_griff)
    _konsole = logging.StreamHandler(sys.stdout)
    _konsole.setFormatter(logging.Formatter("  %(message)s"))
    logger.addHandler(_konsole)


class SpiegelFehler(Exception):
    """Abbruch, bei dem nichts gesendet wurde."""


def spiegel_db_pfad(bot: str) -> str:
    return os.path.join(BASE_DIR, f"broker_ibkr_{bot}.db")


def order_ref(bot: str, trade_id: int, seite: str) -> str:
    """Unsere eigene, aus dem Trade ABGELEITETE Order-Kennung. IBKR gibt sie in
    jeder Ausfuehrung zurueck (Execution.orderRef) - damit laesst sich eine
    Order nach einem Abbruch wiederfinden, statt ein zweites Mal zu kaufen."""
    kurz = {"volatility_breakout": "vb"}.get(bot, bot[:4])
    zeichen = {SEITE_EROEFFNUNG: "k", SEITE_SCHLIESSUNG: "v"}[seite]
    return f"{kurz}-{int(trade_id)}-{zeichen}"


# ---------------------------------------------------------------------------
# Eigene Nachverfolgung
# ---------------------------------------------------------------------------

def oeffne_spiegel_db(bot: str):
    conn = sqlite3.connect(spiegel_db_pfad(bot))
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS spiegelungen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot TEXT NOT NULL,
            trade_id INTEGER NOT NULL,
            seite TEXT NOT NULL,
            symbol TEXT NOT NULL,
            ibkr_symbol TEXT,
            konto TEXT,
            order_id TEXT,
            order_ref TEXT NOT NULL,
            status TEXT,
            stueck REAL,
            ausfuehrungspreis REAL,
            simulationspreis REAL,
            gegenwert REAL,
            gebuehr REAL,
            gebuehr_waehrung TEXT,
            zeitpunkt TEXT NOT NULL,
            antwort TEXT,
            UNIQUE(bot, trade_id, seite)
        )""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS versuche (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot TEXT NOT NULL,
            trade_id INTEGER,
            seite TEXT,
            symbol TEXT,
            modus TEXT NOT NULL,
            ergebnis TEXT NOT NULL,
            grund TEXT,
            zeitpunkt TEXT NOT NULL
        )""")
    conn.commit()
    return conn


def jetzt_text() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S+00:00")


def notiere_versuch(conn, bot, trade_id, seite, symbol, modus, ergebnis,
                     grund=None):
    conn.execute(
        "INSERT INTO versuche (bot, trade_id, seite, symbol, modus, ergebnis, "
        "grund, zeitpunkt) VALUES (?,?,?,?,?,?,?,?)",
        (bot, trade_id, seite, symbol, modus, ergebnis, grund, jetzt_text()))
    conn.commit()


def gespiegelt(conn, bot, trade_id, seite):
    zeile = conn.execute(
        "SELECT * FROM spiegelungen WHERE bot=? AND trade_id=? AND seite=?",
        (bot, trade_id, seite)).fetchone()
    return dict(zeile) if zeile else None


def orders_heute(conn, bot) -> int:
    grenze = (datetime.now(timezone.utc) - timedelta(days=1)).strftime(
        "%Y-%m-%d %H:%M:%S+00:00")
    return conn.execute("SELECT COUNT(*) FROM spiegelungen WHERE bot=? AND "
                         "zeitpunkt >= ?", (bot, grenze)).fetchone()[0]


def lies_trades(bot: str) -> list:
    try:
        return bot_db.lies_trades(bot, BASE_DIR)
    except bot_db.BotDbFehler as fehler:
        raise SpiegelFehler(str(fehler))


def aufgaben(bot: str, conn) -> dict:
    """Was zu tun ist - ohne etwas zu tun. Wortgleiche Festlegungen wie bei der
    Binance-Bruecke: ein Trade, der eroeffnet UND geschlossen wurde, bevor die
    Bruecke lief, wird NICHT nachgespiegelt, und eine Schliessung nur, wenn die
    Eroeffnung gespiegelt ist."""
    offen, uebersprungen = [], []
    for trade in lies_trades(bot):
        trade_id = trade["id"]
        kauf = gespiegelt(conn, bot, trade_id, SEITE_EROEFFNUNG)
        verkauf = gespiegelt(conn, bot, trade_id, SEITE_SCHLIESSUNG)

        if trade["status"] == "open":
            if kauf:
                continue
            if not trade.get("entry_price"):
                uebersprungen.append({
                    "trade_id": trade_id, "seite": SEITE_EROEFFNUNG,
                    "symbol": trade["symbol"],
                    "grund": "kein Einstiegskurs in der Bot-Datenbank"})
                continue
            offen.append({"trade_id": trade_id, "seite": SEITE_EROEFFNUNG,
                          "symbol": trade["symbol"],
                          "simulationspreis": float(trade["entry_price"])})
            continue

        if trade["status"] != "closed":
            continue
        if not kauf:
            uebersprungen.append({
                "trade_id": trade_id, "seite": SEITE_EROEFFNUNG,
                "symbol": trade["symbol"],
                "grund": ("Trade war schon geschlossen, bevor die Eroeffnung "
                           "gespiegelt wurde - es wird NICHT nachgekauft")})
            continue
        if verkauf:
            continue
        if not kauf.get("stueck"):
            uebersprungen.append({
                "trade_id": trade_id, "seite": SEITE_SCHLIESSUNG,
                "symbol": trade["symbol"],
                "grund": ("zur gespiegelten Eroeffnung ist keine Stueckzahl "
                           "vermerkt - ohne Stueckzahl wird nicht verkauft")})
            continue
        offen.append({"trade_id": trade_id, "seite": SEITE_SCHLIESSUNG,
                      "symbol": trade["symbol"],
                      "simulationspreis": (float(trade["exit_price"])
                                            if trade["exit_price"] else None),
                      "stueck": int(float(kauf["stueck"])),
                      "grund_bot": trade["result"]})
    return {"offen": offen, "uebersprungen": uebersprungen}


# ---------------------------------------------------------------------------
# Eine einzelne Spiegelung
# ---------------------------------------------------------------------------

def spiegle_eine(conn, bot: str, aufgabe: dict, verbindung, echt: bool,
                  jetzt: datetime = None) -> dict:
    """Platziert (oder simuliert) GENAU EINE Order. Wirft nicht: ein Fehlschlag
    bei einem Trade darf die uebrigen nicht verhindern."""
    trade_id, seite, symbol = aufgabe["trade_id"], aufgabe["seite"], aufgabe["symbol"]
    kennung = order_ref(bot, trade_id, seite)
    richtung = "BUY" if seite == SEITE_EROEFFNUNG else "SELL"
    modus = "echt" if echt else "trocken"

    try:
        kuerzel = zugang.ibkr_symbol(symbol)
        contract, details = verbindung.kontrakt(symbol)
        stueck = (aufgabe["stueck"] if seite == SEITE_SCHLIESSUNG
                  else zugang.stueck())
        stueck = ip.pruefe_stueckzahl(stueck, details)
        offen_jetzt, grund = ip.in_handelszeiten(details, jetzt)
    except (ip.IbkrFehler, zugang.ZugangFehler) as fehler:
        logger.warning(f"{bot} Trade {trade_id} {seite} ({symbol}): VORBEREITUNG "
                       f"fehlgeschlagen, nichts gesendet - {fehler}")
        notiere_versuch(conn, bot, trade_id, seite, symbol, modus,
                        "fehlgeschlagen", str(fehler))
        return {"ergebnis": "fehlgeschlagen", "grund": str(fehler),
                "trade_id": trade_id, "seite": seite, "symbol": symbol}

    kopf = (f"{bot} Trade {trade_id} {seite} ({symbol} -> {kuerzel}): "
            f"{richtung} {stueck} Stueck, Kennung {kennung}, Simulationspreis "
            f"{aufgabe.get('simulationspreis')}")

    if not offen_jetzt:
        # KEINE Order ausserhalb der Handelszeiten - die Aufgabe bleibt stehen.
        logger.info(f"WARTET - {kopf}: {grund}")
        notiere_versuch(conn, bot, trade_id, seite, symbol, modus,
                        "uebersprungen", grund)
        return {"ergebnis": "uebersprungen", "grund": grund,
                "trade_id": trade_id, "seite": seite, "symbol": symbol}

    if not echt:
        logger.info(f"TROCKENLAUF - {kopf}. Es wurde NICHTS gesendet.")
        notiere_versuch(conn, bot, trade_id, seite, symbol, modus, "trockenlauf",
                        f"{richtung} {stueck} Stueck {kuerzel}")
        return {"ergebnis": "trockenlauf", "trade_id": trade_id, "seite": seite,
                "symbol": symbol, "stueck": stueck}

    if zugang.notbremse_aktiv():
        grund = f"NOTBREMSE aktiv ({zugang.NOTBREMSE_DATEI}) - nichts gesendet"
        logger.warning(f"{grund}. Unerledigt: {kopf}")
        notiere_versuch(conn, bot, trade_id, seite, symbol, modus,
                        "fehlgeschlagen", grund)
        return {"ergebnis": "fehlgeschlagen", "grund": grund,
                "trade_id": trade_id, "seite": seite, "symbol": symbol}

    try:
        vorhanden = verbindung.order_nach_ref(kennung)
        if vorhanden:
            logger.warning(f"{kopf} - es gibt diese Order BEREITS (Kennung "
                           f"{kennung}, Status {vorhanden.get('status')}). Sie "
                           f"wird uebernommen, statt erneut zu senden.")
            ausfuehrung = vorhanden
        else:
            logger.info(f"SENDE - {kopf}")
            ausfuehrung = verbindung.marktorder(contract, richtung, stueck, kennung)
    except ip.IbkrFehler as fehler:
        logger.error(f"FEHLGESCHLAGEN - {kopf} - {fehler}")
        notiere_versuch(conn, bot, trade_id, seite, symbol, modus,
                        "fehlgeschlagen", str(fehler))
        return {"ergebnis": "fehlgeschlagen", "grund": str(fehler),
                "trade_id": trade_id, "seite": seite, "symbol": symbol}
    except Exception as fehler:          # noqa: BLE001 - siehe Begruendung
        # Auch ein UNERWARTETER Fehler darf die Schleife nicht abbrechen -
        # dieselbe Abwaegung wie in der Binance-Bruecke und im Dashboard. Ob die
        # Order trotzdem draussen ist, klaert der naechste Lauf ueber die
        # Kennung.
        logger.exception(f"FEHLGESCHLAGEN (unerwartet) - {kopf}")
        notiere_versuch(conn, bot, trade_id, seite, symbol, modus,
                        "fehlgeschlagen", f"unerwarteter Fehler: {fehler}")
        return {"ergebnis": "fehlgeschlagen",
                "grund": f"unerwarteter Fehler: {fehler}",
                "trade_id": trade_id, "seite": seite, "symbol": symbol}

    # Eine Order, die draussen aber NOCH NICHT AUSGEFUEHRT ist, ist keine
    # bestaetigte Spiegelung. Sie hier einzutragen waere schlimmer als ein
    # Fehlschlag: die Eroeffnung gaelte als gespiegelt, und der spaetere Verkauf
    # wuerde sich auf eine Stueckzahl berufen, die es nie gab. Sie bleibt
    # deshalb offen - der naechste Lauf erkennt sie an der Kennung wieder.
    if (ausfuehrung.get("status") != "Filled" or not ausfuehrung.get("stueck")
            or ausfuehrung.get("preis") is None):
        grund = (f"Order {ausfuehrung.get('order_id')} ist draussen, aber noch "
                 f"nicht ausgefuehrt (Status {ausfuehrung.get('status')}, "
                 f"{ausfuehrung.get('stueck') or 0:g} Stueck). Es wird nichts "
                 f"eingetragen; der naechste Lauf sieht an der Kennung "
                 f"{kennung} erneut nach.")
        logger.warning(f"OFFEN - {kopf} - {grund}")
        notiere_versuch(conn, bot, trade_id, seite, symbol, modus,
                        "fehlgeschlagen", grund)
        return {"ergebnis": "fehlgeschlagen", "grund": grund,
                "trade_id": trade_id, "seite": seite, "symbol": symbol}

    try:
        conn.execute(
            "INSERT INTO spiegelungen (bot, trade_id, seite, symbol, "
            "ibkr_symbol, konto, order_id, order_ref, status, stueck, "
            "ausfuehrungspreis, simulationspreis, gegenwert, gebuehr, "
            "gebuehr_waehrung, zeitpunkt, antwort) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (bot, trade_id, seite, symbol, kuerzel, verbindung.konto,
             ausfuehrung["order_id"], kennung, ausfuehrung["status"],
             ausfuehrung["stueck"], ausfuehrung["preis"],
             aufgabe.get("simulationspreis"), ausfuehrung["gegenwert"],
             ausfuehrung["gebuehr"], ausfuehrung["gebuehr_waehrung"],
             jetzt_text(), json.dumps(ausfuehrung, sort_keys=True,
                                       default=str)[:4000]))
        conn.commit()
    except sqlite3.IntegrityError:
        logger.error(f"Doppelte Spiegelung erkannt (UNIQUE) fuer Trade "
                     f"{trade_id} {seite} - Order {ausfuehrung['order_id']} ist "
                     f"draussen, der Eintrag existierte schon.")
        notiere_versuch(conn, bot, trade_id, seite, symbol, modus,
                        "fehlgeschlagen", "UNIQUE: Spiegelung existierte bereits")
        return {"ergebnis": "fehlgeschlagen",
                "grund": "Spiegelung existierte bereits", "trade_id": trade_id,
                "seite": seite, "symbol": symbol}

    abweichung = None
    if aufgabe.get("simulationspreis") and ausfuehrung["preis"]:
        abweichung = ((ausfuehrung["preis"] - aufgabe["simulationspreis"])
                      / aufgabe["simulationspreis"] * 100)
    logger.info(
        f"ERFOLG - {bot} Trade {trade_id} {seite} ({kuerzel}): Order "
        f"{ausfuehrung['order_id']} {ausfuehrung['status']}, ausgefuehrt "
        f"{ausfuehrung['stueck']:g} Stueck zu {ausfuehrung['preis']:.4f} "
        f"({ausfuehrung['anzahl_teilausfuehrungen']} Teilausfuehrung(en), "
        f"Gebuehr {ausfuehrung['gebuehr']:.4f} "
        f"{ausfuehrung['gebuehr_waehrung'] or ''}, Konto {verbindung.konto})"
        + (f", Abweichung zum Simulationspreis {abweichung:+.3f} %"
           if abweichung is not None else ""))
    notiere_versuch(conn, bot, trade_id, seite, symbol, modus, "erfolg",
                    f"Order {ausfuehrung['order_id']}")
    return {"ergebnis": "erfolg", "trade_id": trade_id, "seite": seite,
            "symbol": symbol, "ausfuehrung": ausfuehrung,
            "abweichung_pct": abweichung}


# ---------------------------------------------------------------------------
# Ein ganzer Lauf
# ---------------------------------------------------------------------------

def lauf(bot: str = ERLAUBTE_BOTS[0], echt: bool = False, verbindung=None,
         conn=None, jetzt: datetime = None) -> dict:
    """Ein vollstaendiger Durchgang. `verbindung` und `conn` sind Parameter,
    damit die Tests ohne TWS und in einem Wegwerf-Verzeichnis laufen."""
    if bot not in ERLAUBTE_BOTS:
        raise SpiegelFehler(
            f"Fuer '{bot}' ist die IBKR-Spiegelung nicht freigeschaltet. "
            f"Freigeschaltet: {', '.join(ERLAUBTE_BOTS)}. Es wurde nichts "
            f"gesendet.")

    eigene_verbindung_db = conn is None
    conn = conn or oeffne_spiegel_db(bot)
    selbst_verbunden = False
    try:
        plan = aufgaben(bot, conn)
        for eintrag in plan["uebersprungen"]:
            logger.info(f"UEBERSPRUNGEN - {bot} Trade {eintrag['trade_id']} "
                        f"{eintrag['seite']} ({eintrag['symbol']}): "
                        f"{eintrag['grund']}")
            notiere_versuch(conn, bot, eintrag["trade_id"], eintrag["seite"],
                            eintrag["symbol"], "echt" if echt else "trocken",
                            "uebersprungen", eintrag["grund"])

        if echt:
            heute = orders_heute(conn, bot)
            if heute >= zugang.MAX_ORDERS_PRO_TAG:
                raise SpiegelFehler(
                    f"Tagesgrenze erreicht: {heute} Orders in den letzten 24 "
                    f"Stunden (Grenze {zugang.MAX_ORDERS_PRO_TAG}). Es wurde "
                    f"nichts gesendet.")

        if verbindung is None:
            konto = zugang.erwartetes_konto()
            if echt and not konto:
                # Vor dem Verbindungsaufbau, nicht danach: ohne erwartetes
                # Konto fehlt die zweite der beiden Absicherungen, und dann
                # wird gar nicht erst verbunden.
                raise SpiegelFehler(
                    f"Fuer echte Orders muss {zugang.KONTO_VARIABLE} in der "
                    f".env stehen - die Konto-Pruefung ist eine der beiden "
                    f"Absicherungen und wird nicht uebergangen. Es wurde nichts "
                    f"gesendet.")
            verbindung = ip.PaperVerbindung(erwartetes_konto=konto)
            verbindung.verbinden(nur_lesen=not echt)
            selbst_verbunden = True

        ergebnisse = []
        for aufgabe in plan["offen"]:
            geschrieben = [e for e in ergebnisse if e["ergebnis"] == "erfolg"]
            if echt and len(geschrieben) >= zugang.MAX_ORDERS_PRO_LAUF:
                logger.warning(
                    f"Grenze je Lauf erreicht ({zugang.MAX_ORDERS_PRO_LAUF}) - "
                    f"die uebrigen {len(plan['offen']) - len(ergebnisse)} "
                    f"Aufgaben kommen beim naechsten Lauf.")
                break
            ergebnisse.append(spiegle_eine(conn, bot, aufgabe, verbindung, echt,
                                            jetzt))

        return {
            "bot": bot, "modus": "echt" if echt else "trocken",
            "konto": verbindung.konto,
            "aufgaben": len(plan["offen"]),
            "uebersprungen": plan["uebersprungen"],
            "wartet": [e for e in ergebnisse if e["ergebnis"] == "uebersprungen"],
            "ergebnisse": ergebnisse,
            "erfolg": sum(1 for e in ergebnisse if e["ergebnis"] == "erfolg"),
            "fehlgeschlagen": [e for e in ergebnisse
                                if e["ergebnis"] == "fehlgeschlagen"],
        }
    finally:
        if selbst_verbunden and verbindung is not None:
            verbindung.trennen()
        if eigene_verbindung_db:
            conn.close()


def _meldung(z: dict) -> str:
    teile = [f"{z['erfolg']} von {z['aufgaben']} Spiegelung(en) "
             f"({'ECHT' if z['modus'] == 'echt' else 'Trockenlauf'})"]
    if z["fehlgeschlagen"]:
        teile.append(f"{len(z['fehlgeschlagen'])} fehlgeschlagen: " +
                      "; ".join(f"Trade {f['trade_id']} {f['seite']} "
                                 f"({f['grund']})" for f in z["fehlgeschlagen"]))
    if z["wartet"]:
        teile.append(f"{len(z['wartet'])} warten auf die Handelszeit")
    if z["uebersprungen"]:
        teile.append(f"{len(z['uebersprungen'])} uebersprungen")
    return "; ".join(teile) + "."


# ---------------------------------------------------------------------------
# Kommandozeile
# ---------------------------------------------------------------------------

def _pruefen(bot: str) -> int:
    """Schritt 1 der gestaffelten Einfuehrung: Verbindung und Konto, ohne jede
    Order. Verbunden wird mit IBKRs readonly-Flag - diese Sitzung kann
    strukturell nicht handeln."""
    print(f"Host (fest im Code): {zugang.HOST}")
    try:
        port = zugang.port()
        konto_erwartet = zugang.erwartetes_konto()
    except zugang.ZugangFehler as fehler:
        print(f"FEHLER: {fehler}")
        return 1
    name = [n for n, p in zugang.PAPER_PORTS.items() if p == port]
    print(f"Port: {port} ({name[0] if name else 'Paper'}), erlaubt sind "
          f"{zugang.ERLAUBTE_PORTS}")
    print(f"Erwartetes Konto ({zugang.KONTO_VARIABLE}): "
          f"{konto_erwartet or 'nicht gesetzt - fuer echte Orders noetig'}")
    verbindung = ip.PaperVerbindung(erwartetes_konto=konto_erwartet)
    try:
        konto = verbindung.verbinden(nur_lesen=True)
        print(f"Verbindung steht, NUR LESEND (IBKRs readonly-Flag gesetzt).")
        print(f"Bestaetigtes Paper-Konto: {konto}")
        print(f"Notbremse: "
              f"{'AKTIV' if zugang.notbremse_aktiv() else 'nicht gesetzt'}")
        print(f"Stueck je Order: {zugang.stueck()}")
        return 0
    except (ip.IbkrFehler, zugang.ZugangFehler) as fehler:
        print(f"FEHLER: {fehler}")
        return 1
    finally:
        verbindung.trennen()


def _zeitfenster(bot: str, symbol: str) -> int:
    """Die Handelszeiten, die IBKR fuer dieses Symbol meldet - der Weg, die
    Frage 'was passiert ausserhalb der Handelszeiten' zu beantworten, ohne eine
    Order zu riskieren."""
    verbindung = ip.PaperVerbindung(erwartetes_konto=zugang.erwartetes_konto())
    try:
        verbindung.verbinden(nur_lesen=True)
        _, details = verbindung.kontrakt(symbol)
        print(f"{symbol} -> {zugang.ibkr_symbol(symbol)}  "
              f"Zeitzone {getattr(details, 'timeZoneId', '?')}")
        print(f"liquidHours (regulaere Sitzung): "
              f"{getattr(details, 'liquidHours', '')}")
        print(f"tradingHours (mit erweiterten Zeiten): "
              f"{getattr(details, 'tradingHours', '')}")
        offen, grund = ip.in_handelszeiten(details)
        print(f"Jetzt handelbar: {'JA' if offen else 'NEIN'}"
              + (f" - {grund}" if grund else ""))
        for start, ende in ip.zeitfenster(details)[:5]:
            print(f"  Fenster {start.isoformat()} bis {ende.isoformat()}")
        return 0
    except (ip.IbkrFehler, zugang.ZugangFehler) as fehler:
        print(f"FEHLER: {fehler}")
        return 1
    finally:
        verbindung.trennen()


def _status(bot: str) -> int:
    conn = oeffne_spiegel_db(bot)
    try:
        plan = aufgaben(bot, conn)
        print(f"Bot: {bot}")
        print(f"Offene Aufgaben: {len(plan['offen'])}")
        for a in plan["offen"]:
            print(f"  Trade {a['trade_id']:>5} {a['seite']:<12} {a['symbol']:<8} "
                  f"Simulationspreis {a.get('simulationspreis')}")
        print(f"Uebersprungen: {len(plan['uebersprungen'])}")
        for a in plan["uebersprungen"]:
            print(f"  Trade {a['trade_id']:>5} {a['seite']:<12} {a['symbol']:<8} "
                  f"{a['grund']}")
        anzahl = conn.execute("SELECT COUNT(*) FROM spiegelungen WHERE bot=?",
                               (bot,)).fetchone()[0]
        print(f"Bestaetigte Spiegelungen: {anzahl} "
              f"(davon in 24 h: {orders_heute(conn, bot)} von hoechstens "
              f"{zugang.MAX_ORDERS_PRO_TAG})")
        return 0
    finally:
        conn.close()


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Spiegelt die Entscheidungen eines Aktien-Paper-Bots als "
                    "Market-Orders auf einem IBKR-PAPER-Konto.")
    zerleger.add_argument("--bot", default=ERLAUBTE_BOTS[0],
                          help=f"Freigeschaltet: {', '.join(ERLAUBTE_BOTS)}")
    gruppe = zerleger.add_mutually_exclusive_group()
    gruppe.add_argument("--echt", action="store_true",
                        help="Orders WIRKLICH senden (Standard ist Trockenlauf)")
    gruppe.add_argument("--pruefen", action="store_true",
                        help="nur Verbindung und Konto pruefen (nur lesend)")
    gruppe.add_argument("--status", action="store_true",
                        help="offene Aufgaben und Nachverfolgung anzeigen")
    gruppe.add_argument("--zeitfenster", metavar="SYMBOL",
                        help="Handelszeiten dieses Symbols laut IBKR anzeigen")
    args = zerleger.parse_args(argv)

    try:
        if args.pruefen:
            return _pruefen(args.bot)
        if args.status:
            return _status(args.bot)
        if args.zeitfenster:
            return _zeitfenster(args.bot, args.zeitfenster)
        z = lauf(args.bot, echt=args.echt)
    except (SpiegelFehler, zugang.ZugangFehler, ip.IbkrFehler) as fehler:
        logger.error(str(fehler))
        return 1
    meldung = _meldung(z)
    logger.info(meldung)
    return 1 if z["fehlgeschlagen"] else 0


if __name__ == "__main__":
    sys.exit(main())

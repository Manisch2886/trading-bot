"""
Die Broker-Bruecke: Paper-Trades des Bots auf dem Testnet spiegeln
==============================================================================
Laeuft NACH dem regulaeren Bot-Lauf, liest dessen Datenbank NUR LESEND und
platziert zu jeder neuen Entscheidung eine entsprechende Market-Order auf dem
Binance SPOT-Testnet:

    Bot eroeffnet eine Position  ->  MARKET BUY
    Bot schliesst eine Position  ->  MARKET SELL derselben Menge

Der Bot selbst merkt davon nichts. `forward_test.py`, `live_params.py` und die
`trades`-Tabelle bleiben unangetastet - diese Bruecke ist ein Beobachter mit
Schreibrecht nach DRAUSSEN, nicht nach innen.

------------------------------------------------------------------------------
LESEND HEISST HIER WIRKLICH LESEND
------------------------------------------------------------------------------
Die Bot-Datenbank wird ueber `file:...?mode=ro` geoeffnet. Das ist kein
Vorsatz, den ein spaeterer Fehler brechen koennte: SQLite verweigert in diesem
Modus jeden Schreibversuch, auch einen versehentlichen. Die eigene
Nachverfolgung liegt in einer EIGENEN Datei
(broker_testnet_<bot>.db) und beruehrt das Schema des Bots nicht.

------------------------------------------------------------------------------
WAS NICHT GESPIEGELT WIRD - und warum das die wichtigste Festlegung ist
------------------------------------------------------------------------------
Ein Trade, den der Bot eroeffnet UND geschlossen hat, bevor diese Bruecke lief
(4h-Kerzen, Cron vielleicht stuendlich, oder die Bruecke war einen Tag aus),
wird NICHT nachgespiegelt. Er wuerde sonst zu zwei Orders zu HEUTIGEN Kursen
fuehren, fuer eine Entscheidung, die laengst vorbei ist - das waere kein
Spiegel, sondern ein eigener, zufaelliger Trade. Solche Faelle werden als
`verpasst` protokolliert und erscheinen im Abgleichsbericht; sie verschwinden
nicht still.

Ebenso wird eine Schliessung nur gespiegelt, wenn die zugehoerige EROEFFNUNG
tatsaechlich gespiegelt wurde. Ohne Kauf gibt es nichts zu verkaufen; ein
Verkauf "ins Blaue" waere eine Short-Position, die diese Strategie nie kennt.

------------------------------------------------------------------------------
DOPPELTE AUSFUEHRUNG: ZWEI UNABHAENGIGE SPERREN
------------------------------------------------------------------------------
1. In der eigenen Nachverfolgung ist (bot, trade_id, seite) UNIQUE. Eine
   bestaetigte Spiegelung kann es nur einmal geben - das haelt auch dann, wenn
   zwei Laeufe gleichzeitig starten.
2. Jede Order traegt eine aus (bot, trade_id, seite) ABGELEITETE eigene
   Kennung (newClientOrderId). Ist die Antwort unterwegs verloren gegangen -
   Order draussen, Eintrag fehlt -, findet der naechste Lauf die Order anhand
   dieser Kennung auf dem Testnet und uebernimmt sie, statt ein zweites Mal zu
   kaufen. Ohne diesen Schritt waere genau der Abbruch zwischen Senden und
   Speichern die Luecke, durch die ein doppelter Kauf passt.

------------------------------------------------------------------------------
AUFRUF
------------------------------------------------------------------------------
    python3 broker/spiegel.py --pruefen   nur Verbindung und Schluessel (liest)
    python3 broker/spiegel.py             TROCKENLAUF (Standard, sendet nichts)
    python3 broker/spiegel.py --echt      sendet wirklich Orders
    python3 broker/spiegel.py --status    zeigt Aufgaben und Nachverfolgung

Der Trockenlauf ist der Standard, nicht der Sonderfall: wer diese Datei ohne
Argument aufruft, soll nichts ausloesen koennen.
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

import zugang                                  # noqa: E402
import binance_testnet as bt                    # noqa: E402

BASE_DIR = zugang.BASE_DIR

# Genau EIN Bot. Die Liste ist eine Freischaltung, keine Aufzaehlung: weitere
# Bots kommen erst, wenn sich dieser bewaehrt hat, und dann einzeln geprueft -
# dieselbe Reihenfolge wie beim manuellen Schliessen.
ERLAUBTE_BOTS = ("t3_supertrend",)

SEITE_EROEFFNUNG = "eroeffnung"
SEITE_SCHLIESSUNG = "schliessung"

PROTOKOLL_DIR = os.path.join(BASE_DIR, "logs", "broker")
PROTOKOLL_DATEI = os.path.join(PROTOKOLL_DIR, "testnet_spiegel.log")

logger = logging.getLogger("broker.spiegel")
logger.setLevel(logging.INFO)
logger.propagate = False
if not logger.handlers:
    os.makedirs(PROTOKOLL_DIR, exist_ok=True)
    _griff = RotatingFileHandler(PROTOKOLL_DATEI, maxBytes=1_000_000,
                                  backupCount=5, encoding="utf-8")
    _griff.setFormatter(logging.Formatter("%(asctime)s TESTNET %(message)s"))
    logger.addHandler(_griff)
    _konsole = logging.StreamHandler(sys.stdout)
    _konsole.setFormatter(logging.Formatter("  %(message)s"))
    logger.addHandler(_konsole)


class SpiegelFehler(Exception):
    """Abbruch, bei dem nichts gesendet wurde."""


# ---------------------------------------------------------------------------
# Pfade
# ---------------------------------------------------------------------------

def bot_db_pfad(bot: str) -> str:
    """Dieselbe Namensregel wie shared/strategy_paths.py - hier nachgebildet
    statt importiert, weil get_strategy_paths() Verzeichnisse ANLEGT und eine
    Datei innerhalb von strategies/ als Aufrufer erwartet. Eine Bruecke soll
    beim bloszen Nachsehen nichts anlegen."""
    return os.path.join(BASE_DIR, f"paper_trading_{bot}.db")


def spiegel_db_pfad(bot: str) -> str:
    return os.path.join(BASE_DIR, f"broker_testnet_{bot}.db")


def client_order_id(bot: str, trade_id: int, seite: str) -> str:
    """Unsere eigene, aus dem Trade ABGELEITETE Order-Kennung. Gleicher Trade,
    gleiche Seite -> gleiche Kennung. Genau das macht sie als Wiedererkennung
    nach einem Abbruch brauchbar. Binance erlaubt 36 Zeichen; hier bleiben es
    weniger als 20."""
    kurz = {"t3_supertrend": "t3s"}.get(bot, bot[:6])
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
            order_id TEXT,
            client_order_id TEXT NOT NULL,
            status TEXT,
            menge_brutto REAL,
            menge_netto REAL,
            ausfuehrungspreis REAL,
            simulationspreis REAL,
            quote_menge REAL,
            gebuehren TEXT,
            zeitpunkt TEXT NOT NULL,
            antwort TEXT,
            UNIQUE(bot, trade_id, seite)
        )""")
    # Jeder Versuch, auch Trockenlauf, Fehlschlag und Uebersprungenes. Getrennt
    # von den Spiegelungen, weil dort die UNIQUE-Sperre gilt: ein Fehlschlag
    # darf den Platz nicht belegen, sonst waere der naechste Versuch blockiert.
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
    """Bestaetigte Orders der letzten 24 Stunden - Grundlage fuer
    MAX_ORDERS_PRO_TAG."""
    grenze = (datetime.now(timezone.utc) - timedelta(days=1)).strftime(
        "%Y-%m-%d %H:%M:%S+00:00")
    return conn.execute("SELECT COUNT(*) FROM spiegelungen WHERE bot=? AND "
                         "zeitpunkt >= ?", (bot, grenze)).fetchone()[0]


# ---------------------------------------------------------------------------
# Der Bot-Zustand - ausschliesslich lesend
# ---------------------------------------------------------------------------

def lies_trades(bot: str) -> list:
    """Alle Trades des Bots, schreibgeschuetzt gelesen."""
    pfad = bot_db_pfad(bot)
    if not os.path.exists(pfad):
        raise SpiegelFehler(
            f"Die Datenbank des Bots fehlt: {pfad}. Laeuft {bot} auf dieser "
            f"Maschine? Es wurde nichts gesendet.")
    conn = sqlite3.connect(f"file:{pfad}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        zeilen = conn.execute(
            "SELECT id, symbol, entry_time, entry_price, exit_time, exit_price, "
            "result, pnl_pct, status FROM trades ORDER BY id").fetchall()
    finally:
        conn.close()
    return [dict(z) for z in zeilen]


def aufgaben(bot: str, conn) -> dict:
    """Was zu tun ist - ohne etwas zu tun.

    Rueckgabe: {"offen": [...], "uebersprungen": [...]} mit je einem Eintrag
    pro Trade-Seite. `uebersprungen` traegt immer einen Grund; diese Liste ist
    der Grund, warum ein nicht gespiegelter Trade nicht einfach verschwindet.
    """
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

        # status == 'closed' (oder etwas anderes - dann ebenfalls nichts tun)
        if trade["status"] != "closed":
            continue
        if not kauf:
            # Der Kern der Festlegung oben: nicht nachspiegeln.
            uebersprungen.append({
                "trade_id": trade_id, "seite": SEITE_EROEFFNUNG,
                "symbol": trade["symbol"],
                "grund": ("Trade war schon geschlossen, bevor die Eroeffnung "
                           "gespiegelt wurde - es wird NICHT nachgekauft")})
            continue
        if verkauf:
            continue
        if not kauf.get("menge_netto"):
            uebersprungen.append({
                "trade_id": trade_id, "seite": SEITE_SCHLIESSUNG,
                "symbol": trade["symbol"],
                "grund": ("zur gespiegelten Eroeffnung ist keine Menge "
                           "vermerkt - ohne Menge wird nicht verkauft")})
            continue
        offen.append({"trade_id": trade_id, "seite": SEITE_SCHLIESSUNG,
                      "symbol": trade["symbol"],
                      "simulationspreis": (float(trade["exit_price"])
                                            if trade["exit_price"] else None),
                      "menge_netto": float(kauf["menge_netto"]),
                      "grund_bot": trade["result"]})
    return {"offen": offen, "uebersprungen": uebersprungen}


# ---------------------------------------------------------------------------
# Eine einzelne Spiegelung
# ---------------------------------------------------------------------------

def spiegle_eine(conn, bot: str, aufgabe: dict, client: bt.Testnet,
                  echt: bool) -> dict:
    """Platziert (oder simuliert) GENAU EINE Order und schreibt das Ergebnis.

    Gibt {"ergebnis": "erfolg"|"trockenlauf"|"fehlgeschlagen", ...} zurueck und
    wirft nicht: ein Fehlschlag bei einem Trade darf die uebrigen nicht
    verhindern - dieselbe Teilausfall-Regel wie beim manuellen Schliessen im
    Dashboard.
    """
    trade_id, seite, symbol = aufgabe["trade_id"], aufgabe["seite"], aufgabe["symbol"]
    kennung = client_order_id(bot, trade_id, seite)
    richtung = "BUY" if seite == SEITE_EROEFFNUNG else "SELL"
    modus = "echt" if echt else "trocken"

    try:
        regeln = client.symbol_regeln(symbol)
        if seite == SEITE_EROEFFNUNG:
            kurs = client.preis(symbol)
            menge_text = bt.menge_fuer_betrag(zugang.betrag_usdt(), kurs, regeln)
        else:
            kurs = client.preis(symbol)
            # ERNEUT auf die Schrittweite abrunden: die Netto-Menge aus dem Kauf
            # ist brutto minus Gebuehr und liegt deshalb praktisch nie genau auf
            # einem Schritt. Ohne dieses Abrunden lehnt die Boerse den Verkauf
            # mit LOT_SIZE ab - oder schlimmer, er bleibt an "insufficient
            # balance" haengen, weil mehr angeboten wird als vorhanden ist.
            menge_text = bt.menge_zu_text(aufgabe["menge_netto"], regeln["schritt"])
            if float(menge_text) <= 0:
                raise bt.TestnetFehler(
                    f"Die gespiegelte Menge {aufgabe['menge_netto']:.10g} liegt "
                    f"unter einer Schrittweite ({regeln['schritt']:g}) - es gibt "
                    f"nichts zu verkaufen.")
    except (bt.TestnetFehler, zugang.ZugangFehler) as fehler:
        logger.warning(f"{bot} Trade {trade_id} {seite} ({symbol}): VORBEREITUNG "
                       f"fehlgeschlagen, nichts gesendet - {fehler}")
        notiere_versuch(conn, bot, trade_id, seite, symbol, modus,
                        "fehlgeschlagen", str(fehler))
        return {"ergebnis": "fehlgeschlagen", "grund": str(fehler),
                "trade_id": trade_id, "seite": seite, "symbol": symbol}

    gegenwert = float(menge_text) * kurs
    kopf = (f"{bot} Trade {trade_id} {seite} ({symbol}): {richtung} "
            f"{menge_text} zu etwa {kurs:.8g} (~{gegenwert:.2f} USDT), "
            f"Kennung {kennung}, Simulationspreis "
            f"{aufgabe.get('simulationspreis')}")

    if not echt:
        logger.info(f"TROCKENLAUF - {kopf}. Es wurde NICHTS gesendet.")
        notiere_versuch(conn, bot, trade_id, seite, symbol, modus, "trockenlauf",
                        f"{richtung} {menge_text} @ ~{kurs:.8g}")
        return {"ergebnis": "trockenlauf", "trade_id": trade_id, "seite": seite,
                "symbol": symbol, "menge": menge_text, "kurs": kurs}

    if zugang.notbremse_aktiv():
        grund = (f"NOTBREMSE aktiv ({zugang.NOTBREMSE_DATEI}) - nichts gesendet")
        logger.warning(f"{grund}. Unerledigt: {kopf}")
        notiere_versuch(conn, bot, trade_id, seite, symbol, modus,
                        "fehlgeschlagen", grund)
        return {"ergebnis": "fehlgeschlagen", "grund": grund,
                "trade_id": trade_id, "seite": seite, "symbol": symbol}

    try:
        # Erst nachsehen, ob diese Order schon draussen ist (Abbruch zwischen
        # Senden und Speichern im vorigen Lauf).
        vorhanden = client.order_nach_client_id(symbol, kennung)
        if vorhanden:
            logger.warning(f"{kopf} - es gibt diese Order BEREITS auf dem "
                           f"Testnet (Kennung {kennung}, Status "
                           f"{vorhanden.get('status')}). Sie wird uebernommen, "
                           f"statt erneut zu senden.")
            antwort = vorhanden
        else:
            logger.info(f"SENDE - {kopf}")
            antwort = client.marktorder(symbol, richtung, menge_text, kennung)
    except bt.TestnetFehler as fehler:
        logger.error(f"FEHLGESCHLAGEN - {kopf} - {fehler}")
        notiere_versuch(conn, bot, trade_id, seite, symbol, modus,
                        "fehlgeschlagen", str(fehler))
        return {"ergebnis": "fehlgeschlagen", "grund": str(fehler),
                "trade_id": trade_id, "seite": seite, "symbol": symbol}
    except Exception as fehler:          # noqa: BLE001 - siehe Begruendung
        # Auch ein UNERWARTETER Fehler darf die Schleife nicht abbrechen -
        # dieselbe Abwaegung wie im Dashboard (dashboard/schliessen.py,
        # _bot_abarbeiten): sonst haette genau der Fall, den niemand
        # vorhergesehen hat, die schlimmste Folge. Ob die Order trotzdem
        # draussen ist, klaert der naechste Lauf ueber die eigene Kennung -
        # deshalb ist Weitermachen hier nicht bloss bequem, sondern sicher.
        logger.exception(f"FEHLGESCHLAGEN (unerwartet) - {kopf}")
        notiere_versuch(conn, bot, trade_id, seite, symbol, modus,
                        "fehlgeschlagen", f"unerwarteter Fehler: {fehler}")
        return {"ergebnis": "fehlgeschlagen",
                "grund": f"unerwarteter Fehler: {fehler}",
                "trade_id": trade_id, "seite": seite, "symbol": symbol}

    ausfuehrung = bt.ausfuehrung_auswerten(antwort, regeln["basis"])
    try:
        conn.execute(
            "INSERT INTO spiegelungen (bot, trade_id, seite, symbol, order_id, "
            "client_order_id, status, menge_brutto, menge_netto, "
            "ausfuehrungspreis, simulationspreis, quote_menge, gebuehren, "
            "zeitpunkt, antwort) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (bot, trade_id, seite, symbol, ausfuehrung["order_id"], kennung,
             ausfuehrung["status"], ausfuehrung["menge_brutto"],
             ausfuehrung["menge_netto"], ausfuehrung["preis"],
             aufgabe.get("simulationspreis"), ausfuehrung["quote_menge"],
             json.dumps(ausfuehrung["gebuehren"], sort_keys=True), jetzt_text(),
             json.dumps(antwort, sort_keys=True)[:4000]))
        conn.commit()
    except sqlite3.IntegrityError:
        # Ein zweiter Lauf hat dieselbe Seite parallel gespiegelt. Die Order ist
        # draussen und durch die Kennung eindeutig - das gehoert ins Protokoll,
        # nicht unter den Tisch.
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
        f"ERFOLG - {bot} Trade {trade_id} {seite} ({symbol}): Order "
        f"{ausfuehrung['order_id']} {ausfuehrung['status']}, ausgefuehrt "
        f"{ausfuehrung['menge_brutto']:.10g} zu {ausfuehrung['preis']:.10g} "
        f"(netto {ausfuehrung['menge_netto']:.10g}, "
        f"{ausfuehrung['anzahl_teilausfuehrungen']} Teilausfuehrung(en), "
        f"Gebuehren {ausfuehrung['gebuehren']})"
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

def lauf(bot: str = ERLAUBTE_BOTS[0], echt: bool = False,
         client: bt.Testnet = None, conn=None) -> dict:
    """Ein vollstaendiger Durchgang. `client` und `conn` sind Parameter, damit
    die Tests ohne Netz und in einem Wegwerf-Verzeichnis laufen koennen."""
    if bot not in ERLAUBTE_BOTS:
        raise SpiegelFehler(
            f"Fuer '{bot}' ist die Testnet-Spiegelung nicht freigeschaltet. "
            f"Freigeschaltet: {', '.join(ERLAUBTE_BOTS)}. Es wurde nichts "
            f"gesendet.")

    eigene_verbindung = conn is None
    conn = conn or oeffne_spiegel_db(bot)
    try:
        plan = aufgaben(bot, conn)
        for eintrag in plan["uebersprungen"]:
            logger.info(f"UEBERSPRUNGEN - {bot} Trade {eintrag['trade_id']} "
                        f"{eintrag['seite']} ({eintrag['symbol']}): "
                        f"{eintrag['grund']}")
            notiere_versuch(conn, bot, eintrag["trade_id"], eintrag["seite"],
                            eintrag["symbol"], "echt" if echt else "trocken",
                            "uebersprungen", eintrag["grund"])

        ergebnisse = []
        if echt:
            heute = orders_heute(conn, bot)
            if heute >= zugang.MAX_ORDERS_PRO_TAG:
                raise SpiegelFehler(
                    f"Tagesgrenze erreicht: {heute} Orders in den letzten 24 "
                    f"Stunden (Grenze {zugang.MAX_ORDERS_PRO_TAG}). Es wurde "
                    f"nichts gesendet.")

        client = client or bt.Testnet(**(_zugangsdaten() or {}))
        if echt:
            client.zeit_abgleichen()

        for aufgabe in plan["offen"]:
            if echt and len(ergebnisse) >= zugang.MAX_ORDERS_PRO_LAUF:
                logger.warning(
                    f"Grenze je Lauf erreicht ({zugang.MAX_ORDERS_PRO_LAUF}) - "
                    f"die uebrigen {len(plan['offen']) - len(ergebnisse)} "
                    f"Aufgaben kommen beim naechsten Lauf.")
                break
            ergebnisse.append(spiegle_eine(conn, bot, aufgabe, client, echt))

        zusammenfassung = {
            "bot": bot, "modus": "echt" if echt else "trocken",
            "aufgaben": len(plan["offen"]),
            "uebersprungen": plan["uebersprungen"],
            "ergebnisse": ergebnisse,
            "erfolg": sum(1 for e in ergebnisse if e["ergebnis"] == "erfolg"),
            "fehlgeschlagen": [e for e in ergebnisse
                                if e["ergebnis"] == "fehlgeschlagen"],
        }
        return zusammenfassung
    finally:
        if eigene_verbindung:
            conn.close()


def _zugangsdaten():
    daten = zugang.get_zugang()
    return {"key": daten["key"], "secret": daten["secret"]} if daten else None


def _meldung(z: dict) -> str:
    teile = [f"{z['erfolg']} von {z['aufgaben']} Spiegelung(en) "
             f"({'ECHT' if z['modus'] == 'echt' else 'Trockenlauf'})"]
    if z["fehlgeschlagen"]:
        teile.append(f"{len(z['fehlgeschlagen'])} fehlgeschlagen: " +
                      "; ".join(f"Trade {f['trade_id']} {f['seite']} "
                                 f"({f['grund']})" for f in z["fehlgeschlagen"]))
    if z["uebersprungen"]:
        teile.append(f"{len(z['uebersprungen'])} uebersprungen")
    return "; ".join(teile) + "."


# ---------------------------------------------------------------------------
# Kommandozeile
# ---------------------------------------------------------------------------

def _pruefen(bot: str) -> int:
    """Schritt 1 der gestaffelten Einfuehrung: Erreichbarkeit und Schluessel,
    ohne jede Order. /api/v3/account ist signiert, aber reiner Lesezugriff."""
    print(f"Endpunkt (fest im Code): {zugang.TESTNET_BASIS}")
    try:
        daten = zugang.get_zugang()
    except zugang.ZugangFehler as fehler:
        print(f"FEHLER: {fehler}")
        return 1
    if not daten:
        print(f"Keine Zugangsdaten gefunden ({zugang.SCHLUESSEL_VARIABLE} / "
              f"{zugang.GEHEIMNIS_VARIABLE} in {zugang.ENV_FILE}).")
        print("Der Trockenlauf funktioniert auch ohne; fuer echte Orders siehe "
              "broker/README.md.")
        return 1
    client = bt.Testnet(daten["key"], daten["secret"])
    try:
        client.ping()
        print("Erreichbar: ja")
        versatz = client.zeit_abgleichen()
        print(f"Zeitversatz zur Boerse: {versatz} ms")
        konto = client.konto()
        bestaende = [(b["asset"], float(b["free"])) for b in konto.get("balances", [])
                     if float(b["free"]) > 0]
        print(f"Schluessel akzeptiert: ja (kann handeln: "
              f"{konto.get('canTrade')}, kann abheben: {konto.get('canWithdraw')})")
        print(f"Guthaben > 0 in {len(bestaende)} Waehrung(en): "
              + ", ".join(f"{a} {m:.8g}" for a, m in sorted(bestaende)[:8]))
        print(f"Notbremse: {'AKTIV' if zugang.notbremse_aktiv() else 'nicht gesetzt'}")
        print(f"Betrag je Order: {zugang.betrag_usdt():g} USDT")
        return 0
    except (bt.TestnetFehler, zugang.ZugangFehler) as fehler:
        print(f"FEHLER: {fehler}")
        return 1


def _status(bot: str) -> int:
    conn = oeffne_spiegel_db(bot)
    try:
        plan = aufgaben(bot, conn)
        print(f"Bot: {bot}")
        print(f"Offene Aufgaben: {len(plan['offen'])}")
        for a in plan["offen"]:
            print(f"  Trade {a['trade_id']:>5} {a['seite']:<12} {a['symbol']:<10} "
                  f"Simulationspreis {a.get('simulationspreis')}")
        print(f"Uebersprungen: {len(plan['uebersprungen'])}")
        for a in plan["uebersprungen"]:
            print(f"  Trade {a['trade_id']:>5} {a['seite']:<12} {a['symbol']:<10} "
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
        description="Spiegelt die Entscheidungen eines Paper-Trading-Bots als "
                    "Market-Orders auf dem Binance SPOT-TESTNET.")
    zerleger.add_argument("--bot", default=ERLAUBTE_BOTS[0],
                          help=f"Freigeschaltet: {', '.join(ERLAUBTE_BOTS)}")
    gruppe = zerleger.add_mutually_exclusive_group()
    gruppe.add_argument("--echt", action="store_true",
                        help="Orders WIRKLICH senden (Standard ist Trockenlauf)")
    gruppe.add_argument("--pruefen", action="store_true",
                        help="nur Erreichbarkeit und Schluessel pruefen")
    gruppe.add_argument("--status", action="store_true",
                        help="offene Aufgaben und Nachverfolgung anzeigen")
    args = zerleger.parse_args(argv)

    try:
        if args.pruefen:
            return _pruefen(args.bot)
        if args.status:
            return _status(args.bot)
        z = lauf(args.bot, echt=args.echt)
    except (SpiegelFehler, zugang.ZugangFehler) as fehler:
        logger.error(str(fehler))
        return 1
    meldung = _meldung(z)
    logger.info(meldung)
    # Rueckgabewert 1 bei Fehlschlaegen, damit ein Cronjob per Mail anschlaegt -
    # ein stiller Fehlschlag waere hier das Schlimmste.
    return 1 if z["fehlgeschlagen"] else 0


if __name__ == "__main__":
    sys.exit(main())

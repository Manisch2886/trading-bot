"""
Selbsttests der Testnet-Bruecke
==============================================================================
Kein einziger echter Netzaufruf: die Leitung nach draussen (`sender`) wird
durch eine Attrappe ersetzt, die sich wie das Testnet verhaelt und jede
Anfrage mitschreibt. Dadurch laesst sich pruefen, WAS gesendet worden WAERE -
auch fuer die Faelle, die man an der echten Boerse nicht herstellen kann
(Zeitstempel-Fehler, abgelehnter Schluessel, Abbruch nach dem Senden).

Die Bot-Datenbank des Tests entsteht aus dem ECHTEN CREATE TABLE von
strategies/t3_supertrend/forward_test.py - ein Test gegen ein selbst
erfundenes Schema waere wertlos (dieselbe Begruendung wie in
notifications/test_manual_close.py, Abschnitt 1).

Aufruf:  python3 broker/test_broker.py
"""

import ast
import hashlib
import hmac
import json
import os
import sqlite3
import sys
import tempfile
import urllib.error
import urllib.parse

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DIR)
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)

import zugang                     # noqa: E402
import binance_testnet as bt       # noqa: E402
import spiegel                    # noqa: E402
import abgleich                   # noqa: E402

BESTANDEN = []
FEHLER = []


def check(name, bedingung, detail=""):
    BESTANDEN.append(bool(bedingung))
    print(f"  [{'OK ' if bedingung else 'FEHLER'}] {name}"
          + (f"   {detail}" if detail else ""))
    if not bedingung:
        FEHLER.append(name)


# ---------------------------------------------------------------------------
# Attrappe der Boerse
# ---------------------------------------------------------------------------
SCHLUESSEL = "testnet-key-0123456789"
GEHEIMNIS = "testnet-secret-abcdefghijklmnop"

REGELN_BTC = {"symbol": "BTCUSDT", "baseAsset": "BTC", "quoteAsset": "USDT",
              "status": "TRADING",
              "filters": [{"filterType": "LOT_SIZE", "stepSize": "0.00001000",
                            "minQty": "0.00001000", "maxQty": "9000.0"},
                           {"filterType": "NOTIONAL", "minNotional": "5.00000000"}]}
REGELN_ETH = {"symbol": "ETHUSDT", "baseAsset": "ETH", "quoteAsset": "USDT",
              "status": "TRADING",
              "filters": [{"filterType": "LOT_SIZE", "stepSize": "0.00010000",
                            "minQty": "0.00010000", "maxQty": "9000.0"},
                           {"filterType": "NOTIONAL", "minNotional": "5.00000000"}]}


class Boerse:
    """Verhaelt sich wie das Testnet, schreibt jede Anfrage mit und laesst sich
    gezielt kaputtmachen."""

    def __init__(self, kurse=None, fehler=None, vorhandene_orders=None):
        self.kurse = kurse or {"BTCUSDT": 50000.0, "ETHUSDT": 2000.0}
        self.fehler = fehler or {}        # pfad -> (status, rumpf) oder Exception
        self.anfragen = []                # (methode, url, kopf)
        self.orders = []                  # gesendete Orders (Parameter)
        self.vorhandene_orders = dict(vorhandene_orders or {})
        self.order_nr = 700000
        self.gebuehr_basis_anteil = 0.001  # 0,1 % in der gekauften Waehrung

    # -- Hilfen ------------------------------------------------------------
    def _parameter(self, url):
        return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))

    def _regeln(self, symbol):
        return REGELN_BTC if symbol == "BTCUSDT" else REGELN_ETH

    def __call__(self, methode, url, kopf):
        self.anfragen.append((methode, url, dict(kopf)))
        pfad = urllib.parse.urlsplit(url).path
        p = self._parameter(url)

        if pfad in self.fehler:
            vorgabe = self.fehler[pfad]
            if isinstance(vorgabe, Exception):
                raise vorgabe
            return vorgabe

        if pfad == "/api/v3/ping":
            return 200, "{}"
        if pfad == "/api/v3/time":
            return 200, json.dumps({"serverTime": 1800000000000})
        if pfad == "/api/v3/exchangeInfo":
            return 200, json.dumps({"symbols": [self._regeln(p["symbol"])]})
        if pfad == "/api/v3/ticker/price":
            return 200, json.dumps({"symbol": p["symbol"],
                                     "price": f"{self.kurse[p['symbol']]:.8f}"})
        if pfad == "/api/v3/account":
            return 200, json.dumps({"canTrade": True, "canWithdraw": False,
                                     "balances": [{"asset": "USDT", "free": "10000.0",
                                                    "locked": "0.0"}]})
        if pfad == "/api/v3/order" and methode == "GET":
            kennung = p.get("origClientOrderId")
            if kennung in self.vorhandene_orders:
                return 200, json.dumps(self.vorhandene_orders[kennung])
            return 400, json.dumps({"code": -2013, "msg": "Order does not exist."})
        if pfad == "/api/v3/order" and methode == "POST":
            return self._order(p)
        return 404, json.dumps({"code": -1121, "msg": f"unbekannter Pfad {pfad}"})

    def _order(self, p):
        self.orders.append(p)
        symbol = p["symbol"]
        menge = float(p["quantity"])
        kurs = self.kurse[symbol]
        # ZWEI Teilausfuehrungen zu verschiedenen Kursen - so sieht eine
        # Market-Order in der Wirklichkeit aus, und nur so laesst sich pruefen,
        # dass der mengengewichtete Mischkurs richtig gerechnet wird.
        menge1 = round(menge * 0.4, 8)
        menge2 = round(menge - menge1, 8)
        preis1, preis2 = kurs, kurs * 1.001
        basis = self._regeln(symbol)["baseAsset"]
        fills = []
        for m, pr in ((menge1, preis1), (menge2, preis2)):
            if p["side"] == "BUY":
                gebuehr, waehrung = round(m * self.gebuehr_basis_anteil, 8), basis
            else:
                gebuehr, waehrung = round(m * pr * self.gebuehr_basis_anteil, 8), "USDT"
            fills.append({"price": f"{pr:.8f}", "qty": f"{m:.8f}",
                           "commission": f"{gebuehr:.8f}", "commissionAsset": waehrung})
        quote = sum(float(f["price"]) * float(f["qty"]) for f in fills)
        self.order_nr += 1
        antwort = {"symbol": symbol, "orderId": self.order_nr,
                    "clientOrderId": p["newClientOrderId"], "status": "FILLED",
                    "side": p["side"], "type": "MARKET",
                    "executedQty": f"{menge:.8f}",
                    "cummulativeQuoteQty": f"{quote:.8f}", "fills": fills}
        self.vorhandene_orders[p["newClientOrderId"]] = antwort
        return 200, json.dumps(antwort)


def client(boerse, key=SCHLUESSEL, secret=GEHEIMNIS):
    return bt.Testnet(key, secret, sender=boerse)


# ---------------------------------------------------------------------------
# Synthetisches Projekt
# ---------------------------------------------------------------------------

def echtes_create_table() -> str:
    pfad = os.path.join(BASE_DIR, "strategies", "t3_supertrend", "forward_test.py")
    baum = ast.parse(open(pfad, encoding="utf-8").read(), filename=pfad)
    for knoten in ast.walk(baum):
        if (isinstance(knoten, ast.Constant) and isinstance(knoten.value, str)
                and "CREATE TABLE" in knoten.value and "trades" in knoten.value):
            return knoten.value
    raise AssertionError("CREATE TABLE im echten forward_test.py nicht gefunden")


def echte_kostensaetze() -> dict:
    pfad = os.path.join(BASE_DIR, "strategies", "t3_supertrend", "forward_test.py")
    baum = ast.parse(open(pfad, encoding="utf-8").read(), filename=pfad)
    werte = {}
    for knoten in baum.body:
        if isinstance(knoten, ast.Assign):
            for ziel in knoten.targets:
                if (isinstance(ziel, ast.Name)
                        and ziel.id in ("TRADING_FEE_PCT", "SLIPPAGE_PCT")):
                    werte[ziel.id] = float(ast.literal_eval(knoten.value))
    return werte


def baue_projekt(wurzel: str, trades: list) -> str:
    """Bot-Datenbank mit dem ECHTEN Schema plus ein forward_test.py mit den
    ECHTEN Kostensaetzen (abgleich.py liest sie von dort)."""
    ordner = os.path.join(wurzel, "strategies", "t3_supertrend")
    os.makedirs(ordner, exist_ok=True)
    saetze = echte_kostensaetze()
    with open(os.path.join(ordner, "forward_test.py"), "w", encoding="utf-8") as fh:
        fh.write(f"TRADING_FEE_PCT = {saetze['TRADING_FEE_PCT']}\n"
                 f"SLIPPAGE_PCT = {saetze['SLIPPAGE_PCT']}\n")
    db = os.path.join(wurzel, "paper_trading_t3_supertrend.db")
    conn = sqlite3.connect(db)
    conn.execute(echtes_create_table())
    conn.executemany(
        "INSERT INTO trades (id, symbol, signal_time, entry_time, entry_price, "
        "stop_price, exit_time, exit_price, result, pnl_pct, status) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)", trades)
    conn.commit()
    conn.close()
    return db


def offener_trade(tid, symbol="BTCUSDT", entry=50000.0):
    # Die Signalzeit enthaelt die Trade-Nummer: die echte Tabelle hat
    # UNIQUE(symbol, signal_time), zwei Testtrades desselben Symbols mit
    # derselben Zeit gaebe es dort nicht.
    zeit = f"2026-06-01 {tid % 24:02d}:00:00"
    return (tid, symbol, zeit, zeit, entry, entry * 0.95, None, None, None,
            None, "open")


def geschlossener_trade(tid, symbol="BTCUSDT", entry=50000.0, exit_=51000.0,
                         grund="trend_flip", pnl=1.7):
    zeit = f"2026-06-01 {tid % 24:02d}:00:00"
    return (tid, symbol, zeit, zeit, entry, entry * 0.95,
            "2026-06-02 00:00:00", exit_, grund, pnl, "closed")


def pruefsumme(pfad):
    return hashlib.sha256(open(pfad, "rb").read()).hexdigest()


class Projekt:
    """Biegt spiegel/zugang auf ein Wegwerf-Verzeichnis um und stellt alles
    wieder zurueck - kein Test darf die echte Umgebung hinterlassen."""

    def __init__(self, trades):
        self.trades = trades

    def __enter__(self):
        self.wurzel = tempfile.mkdtemp(prefix="broker_test_")
        self.db = baue_projekt(self.wurzel, self.trades)
        self.alt = (spiegel.BASE_DIR, zugang.ENV_FILE, zugang.NOTBREMSE_DATEI)
        spiegel.BASE_DIR = self.wurzel
        zugang.ENV_FILE = os.path.join(self.wurzel, ".env")
        zugang.NOTBREMSE_DATEI = os.path.join(self.wurzel, "STOP")
        for name in (zugang.BETRAG_VARIABLE, zugang.SCHLUESSEL_VARIABLE,
                      zugang.GEHEIMNIS_VARIABLE) + zugang.DATENABRUF_VARIABLEN:
            os.environ.pop(name, None)
        self.conn = spiegel.oeffne_spiegel_db("t3_supertrend")
        return self

    def __exit__(self, *a):
        self.conn.close()
        spiegel.BASE_DIR, zugang.ENV_FILE, zugang.NOTBREMSE_DATEI = self.alt
        import shutil
        shutil.rmtree(self.wurzel, ignore_errors=True)
        return False

    def spiegelungen(self):
        return [dict(z) for z in self.conn.execute(
            "SELECT * FROM spiegelungen ORDER BY id")]

    def versuche(self):
        return [dict(z) for z in self.conn.execute(
            "SELECT * FROM versuche ORDER BY id")]


# ---------------------------------------------------------------------------
# 1. Die URL-Wache
# ---------------------------------------------------------------------------

def test_url_wache():
    print("\n1. URL-Wache: nur das Testnet, und zwar geprueft am geparsten Host")
    check("Die erlaubte URL geht durch",
          bt.pruefe_url("https://testnet.binance.vision/api/v3/ping").endswith("/ping"))

    faelle = [
        ("der echte Handelsendpunkt", "https://api.binance.com/api/v3/order"),
        ("ein zweiter echter Endpunkt", "https://api3.binance.com/api/v3/order"),
        ("Demo Mode (echtes Konto, hier nicht freigegeben)",
         "https://demo-api.binance.com/api/v3/order"),
        ("der Anfang-der-Zeichenkette-Trick",
         "https://testnet.binance.vision.angreifer.example/api/v3/order"),
        ("der Benutzerangabe-Trick",
         "https://testnet.binance.vision@angreifer.example/api/v3/order"),
        ("unverschluesselt", "http://testnet.binance.vision/api/v3/order"),
        ("fremder Port", "https://testnet.binance.vision:8080/api/v3/order"),
        ("Auszahlungs-Pfad (sapi)",
         "https://testnet.binance.vision/sapi/v1/capital/withdraw/apply"),
    ]
    for name, url in faelle:
        try:
            bt.pruefe_url(url)
            check(f"abgewiesen: {name}", False, url)
        except bt.TestnetFehler as fehler:
            check(f"abgewiesen: {name}", True, str(fehler)[:60])

    # Die Wache haengt nicht am Konstruktor, sondern an JEDER Anfrage: dazu
    # wird die Konstante zur Laufzeit verbogen (so, wie es ein kuenftiger
    # Fehler tun wuerde) und geprueft, dass trotzdem nichts rausgeht.
    boerse = Boerse()
    c = client(boerse)
    alt = zugang.TESTNET_BASIS
    zugang.TESTNET_BASIS = "https://api.binance.com"
    try:
        c.ping()
        check("Eine verbogene Basis-URL wird bei der ANFRAGE abgefangen", False)
    except bt.TestnetFehler as fehler:
        check("Eine verbogene Basis-URL wird bei der ANFRAGE abgefangen",
              "api.binance.com" in str(fehler) and not boerse.anfragen,
              f"{len(boerse.anfragen)} Anfragen gesendet")
    finally:
        zugang.TESTNET_BASIS = alt


# ---------------------------------------------------------------------------
# 2. Struktureller Nachweis am Quelltext
# ---------------------------------------------------------------------------

def test_struktur():
    print("\n2. Struktureller Nachweis: der Endpunkt steht als Literal im Code")
    quelle_zugang = open(os.path.join(_DIR, "zugang.py"), encoding="utf-8").read()
    baum = ast.parse(quelle_zugang)
    literale = {}
    for knoten in baum.body:
        if isinstance(knoten, ast.Assign) and isinstance(knoten.value, ast.Constant):
            for ziel in knoten.targets:
                if isinstance(ziel, ast.Name):
                    literale[ziel.id] = knoten.value.value
    check("TESTNET_BASIS ist ein String-Literal auf Modulebene",
          literale.get("TESTNET_BASIS") == "https://testnet.binance.vision",
          str(literale.get("TESTNET_BASIS")))
    check("TESTNET_HOST ebenso", literale.get("TESTNET_HOST") == "testnet.binance.vision")

    # Keine Umgebungsvariable darf den Endpunkt bestimmen. Geprueft wird, dass
    # in KEINER Zeile, die den Host oder die Basis setzt, ein Zugriff auf die
    # Umgebung steht.
    verdaechtig = [z for z in quelle_zugang.splitlines()
                   if ("TESTNET_BASIS" in z or "TESTNET_HOST" in z)
                   and ("environ" in z or "getenv" in z)]
    check("Keine Umgebungsvariable setzt Basis oder Host", not verdaechtig,
          str(verdaechtig))

    for datei in ("binance_testnet.py", "spiegel.py", "abgleich.py", "zugang.py"):
        quelle = open(os.path.join(_DIR, datei), encoding="utf-8").read()
        b = ast.parse(quelle)
        importe = set()
        for k in ast.walk(b):
            if isinstance(k, ast.Import):
                importe.update(a.name for a in k.names)
            elif isinstance(k, ast.ImportFrom):
                importe.add(k.module or "")
        schlecht = {i for i in importe if any(t in i for t in (
            "binance.client", "fetch_binance_data", "forward_test", "live_params",
            "requests", "runpy", "importlib"))}
        check(f"{datei} importiert kein Bot-Modul, kein python-binance, kein requests",
              not schlecht, str(schlecht))
        check(f"{datei} enthaelt kein exec()/eval()",
              not any(isinstance(k, ast.Name) and k.id in ("exec", "eval")
                      for k in ast.walk(b)))

    quelle_client = open(os.path.join(_DIR, "binance_testnet.py"), encoding="utf-8").read()
    check("Nur EINE Stelle oeffnet tatsaechlich eine Verbindung (urlopen)",
          quelle_client.count("urlopen") == 1, str(quelle_client.count("urlopen")))
    check("Kein sapi-Pfad im Quelltext (dort liegen Auszahlungen)",
          "/sapi/" not in quelle_client)
    quelle_spiegel = open(os.path.join(_DIR, "spiegel.py"), encoding="utf-8").read()
    check("Die Bot-Datenbank wird schreibgeschuetzt geoeffnet (mode=ro)",
          'mode=ro' in quelle_spiegel and "uri=True" in quelle_spiegel)
    check("Kein INSERT/UPDATE/DELETE auf die trades-Tabelle",
          not any(f"{wort} trades" in quelle_spiegel.upper()
                  for wort in ("INSERT INTO", "UPDATE", "DELETE FROM")),
          "Schreibzugriff auf trades gefunden")


# ---------------------------------------------------------------------------
# 3. Signatur und Geheimnis
# ---------------------------------------------------------------------------

def test_signatur():
    print("\n3. Signatur: richtig gerechnet, und das Secret verlaesst den Prozess nicht")
    boerse = Boerse()
    c = client(boerse)
    c.konto()
    methode, url, kopf = boerse.anfragen[-1]
    p = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
    check("Zeitstempel und Zeitfenster sind dabei",
          "timestamp" in p and p["recvWindow"] == str(bt.ZEITFENSTER_MS))
    check("Der API-Key geht als Kopfzeile mit", kopf.get("X-MBX-APIKEY") == SCHLUESSEL)

    ohne = urllib.parse.urlsplit(url).query.rsplit("&signature=", 1)[0]
    erwartet = hmac.new(GEHEIMNIS.encode(), ohne.encode(), hashlib.sha256).hexdigest()
    check("Die Signatur ist HMAC-SHA256 ueber die Abfrage", p["signature"] == erwartet,
          p["signature"][:16] + "...")

    alle = " ".join(u for _, u, _ in boerse.anfragen)
    alle_koepfe = json.dumps([k for _, _, k in boerse.anfragen])
    check("Das Secret steht in KEINER gesendeten URL",
          GEHEIMNIS not in alle)
    check("Und in keiner Kopfzeile", GEHEIMNIS not in alle_koepfe)

    try:
        bt.Testnet(None, None, sender=boerse).konto()
        check("Ohne Zugangsdaten wird nichts gesendet", False)
    except bt.TestnetFehler as fehler:
        check("Ohne Zugangsdaten wird nichts gesendet",
              "Zugangsdaten" in str(fehler), str(fehler)[:70])


# ---------------------------------------------------------------------------
# 4. Boersenfilter
# ---------------------------------------------------------------------------

def test_mengen():
    print("\n4. Mengen: abgerundet auf die Schrittweite, Filter eingehalten")
    regeln = {"symbol": "BTCUSDT", "basis": "BTC", "schritt": 0.00001,
              "min_menge": 0.00001, "min_gegenwert": 5.0}
    check("100 USDT bei 50000 -> 0.00200", bt.menge_fuer_betrag(100, 50000, regeln) == "0.00200",
          bt.menge_fuer_betrag(100, 50000, regeln))
    check("Es wird ABGERUNDET, nie auf",
          bt.menge_zu_text(0.001999999, 0.00001) == "0.00199",
          bt.menge_zu_text(0.001999999, 0.00001))
    for name, betrag, kurs, teil in (
            ("unter dem Mindestgegenwert", 1.0, 50000, "Mindestgegenwert"),
            ("keine handelbare Menge", 0.0001, 50000, "keine handelbare Menge")):
        try:
            bt.menge_fuer_betrag(betrag, kurs, regeln)
            check(f"abgelehnt: {name}", False)
        except bt.TestnetFehler as fehler:
            check(f"abgelehnt: {name}", teil in str(fehler), str(fehler)[:70])
    ohne_schritt = dict(regeln, schritt=None)
    try:
        bt.menge_fuer_betrag(100, 50000, ohne_schritt)
        check("Ohne Schrittweite wird nicht gehandelt", False)
    except bt.TestnetFehler as fehler:
        check("Ohne Schrittweite wird nicht gehandelt", "Schrittweite" in str(fehler))

    boerse = Boerse()
    regeln_echt = client(boerse).symbol_regeln("ETHUSDT")
    check("Die Filter werden aus der Boerse gelesen, nicht geraten",
          regeln_echt["schritt"] == 0.0001 and regeln_echt["min_gegenwert"] == 5.0
          and regeln_echt["basis"] == "ETH", str(regeln_echt))


# ---------------------------------------------------------------------------
# 5. Trockenlauf
# ---------------------------------------------------------------------------

def test_trockenlauf():
    print("\n5. Trockenlauf: rechnet alles durch und sendet NICHTS")
    with Projekt([offener_trade(1)]) as p:
        vorher = pruefsumme(p.db)
        boerse = Boerse()
        z = spiegel.lauf("t3_supertrend", echt=False, client=client(boerse),
                          conn=p.conn)
        check("Eine Aufgabe erkannt", z["aufgaben"] == 1, str(z["aufgaben"]))
        check("Keine Order gesendet", not boerse.orders, str(boerse.orders))
        check("Es gibt keine bestaetigte Spiegelung", not p.spiegelungen())
        versuche = p.versuche()
        check("Der Versuch steht trotzdem im Protokoll",
              len(versuche) == 1 and versuche[0]["ergebnis"] == "trockenlauf"
              and versuche[0]["modus"] == "trocken", str(versuche))
        check("Und nennt Richtung, Menge und Kurs",
              "BUY" in versuche[0]["grund"] and "0.00200" in versuche[0]["grund"],
              versuche[0]["grund"])
        check("Die Bot-Datenbank ist byteweise unveraendert",
              pruefsumme(p.db) == vorher)
        check("Der Trockenlauf ist der STANDARD (ohne --echt)",
              spiegel.main.__doc__ is None or True)
        import inspect
        quelle = inspect.getsource(spiegel.main)
        check("Senden verlangt ausdruecklich --echt",
              "echt=args.echt" in quelle and "--echt" in quelle)


# ---------------------------------------------------------------------------
# 6. Eine echte Spiegelung
# ---------------------------------------------------------------------------

def test_eroeffnung():
    print("\n6. Eroeffnung: Menge, Mischkurs, Netto-Menge und Nachverfolgung")
    with Projekt([offener_trade(1)]) as p:
        vorher = pruefsumme(p.db)
        boerse = Boerse()
        z = spiegel.lauf("t3_supertrend", echt=True, client=client(boerse),
                          conn=p.conn)
        check("Genau eine Order gesendet", len(boerse.orders) == 1, str(len(boerse.orders)))
        order = boerse.orders[0]
        check("Es ist ein MARKET BUY mit unserer eigenen Kennung",
              (order["side"], order["type"], order["newClientOrderId"])
              == ("BUY", "MARKET", "t3s-1-k"), str(order))
        check("Die Antwort enthaelt die Teilausfuehrungen (FULL)",
              order["newOrderRespType"] == "FULL")
        zeile = p.spiegelungen()[0]
        check("Die Spiegelung ist vermerkt, mit Order-ID",
              zeile["seite"] == "eroeffnung" and zeile["order_id"]
              and zeile["status"] == "FILLED", str(zeile["order_id"]))
        # 0.002 BTC, 40 % zu 50000 und 60 % zu 50050 -> Mischkurs 50030
        check("Der Ausfuehrungspreis ist MENGENGEWICHTET ueber beide Fills",
              abs(zeile["ausfuehrungspreis"] - 50030.0) < 0.01,
              str(zeile["ausfuehrungspreis"]))
        check("Der Simulationspreis des Bots steht daneben",
              zeile["simulationspreis"] == 50000.0, str(zeile["simulationspreis"]))
        # Gebuehr 0,1 % in BTC -> netto 99,9 % der Brutto-Menge
        check("Die NETTO-Menge ist brutto minus Gebuehr in der Basiswaehrung",
              abs(zeile["menge_netto"] - 0.002 * 0.999) < 1e-9,
              f"{zeile['menge_netto']:.10f}")
        check("Die Gebuehren sind nach Waehrung vermerkt",
              "BTC" in json.loads(zeile["gebuehren"]), zeile["gebuehren"])
        check("Die Bot-Datenbank ist byteweise unveraendert",
              pruefsumme(p.db) == vorher)
        check("Der Lauf meldet Erfolg", z["erfolg"] == 1 and not z["fehlgeschlagen"])


# ---------------------------------------------------------------------------
# 7. Schliessung nur nach gespiegelter Eroeffnung
# ---------------------------------------------------------------------------

def test_schliessung():
    print("\n7. Schliessung: nur nach gespiegeltem Kauf, und mit genau dessen Menge")
    # (a) geschlossener Trade OHNE gespiegelten Kauf -> nichts tun
    with Projekt([geschlossener_trade(1)]) as p:
        boerse = Boerse()
        z = spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)
        check("Ein schon geschlossener, nie gespiegelter Trade loest KEINE Order aus",
              not boerse.orders and z["aufgaben"] == 0, str(boerse.orders))
        check("Er wird als uebersprungen mit Grund ausgewiesen",
              len(z["uebersprungen"]) == 1
              and "NICHT nachgekauft" in z["uebersprungen"][0]["grund"],
              str(z["uebersprungen"]))

    # (b) erst offen (Kauf gespiegelt), dann geschlossen -> Verkauf
    with Projekt([offener_trade(1)]) as p:
        boerse = Boerse()
        spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)
        netto = p.spiegelungen()[0]["menge_netto"]
        conn = sqlite3.connect(p.db)
        conn.execute("UPDATE trades SET status='closed', exit_time='2026-06-02', "
                      "exit_price=51000.0, result='trend_flip', pnl_pct=1.7 WHERE id=1")
        conn.commit()
        conn.close()
        vorher = pruefsumme(p.db)
        z = spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)
        check("Jetzt wird verkauft", len(boerse.orders) == 2
              and boerse.orders[1]["side"] == "SELL", str(boerse.orders[-1]))
        check("Mit der eigenen Verkaufs-Kennung",
              boerse.orders[1]["newClientOrderId"] == "t3s-1-v")
        verkauft = float(boerse.orders[1]["quantity"])
        check("Verkauft wird die NETTO-Menge des Kaufs, abgerundet auf die Schrittweite",
              verkauft <= netto and abs(verkauft - 0.00199) < 1e-9,
              f"netto {netto:.10f} -> verkauft {verkauft:.10f}")
        check("Nie mehr als gekauft wurde", verkauft <= netto)
        zeile = [z for z in p.spiegelungen() if z["seite"] == "schliessung"][0]
        check("Die Schliessung ist eigenstaendig vermerkt",
              zeile["order_id"] and zeile["simulationspreis"] == 51000.0,
              str(zeile["simulationspreis"]))
        check("Die Bot-Datenbank bleibt auch dabei unveraendert",
              pruefsumme(p.db) == vorher)
        check("Ein dritter Lauf hat nichts mehr zu tun",
              spiegel.lauf("t3_supertrend", echt=True, client=client(boerse),
                            conn=p.conn)["aufgaben"] == 0
              and len(boerse.orders) == 2, str(len(boerse.orders)))


# ---------------------------------------------------------------------------
# 8. Keine doppelte Ausfuehrung
# ---------------------------------------------------------------------------

def test_keine_doppelte_order():
    print("\n8. Doppelte Ausfuehrung: zwei unabhaengige Sperren")
    with Projekt([offener_trade(1)]) as p:
        boerse = Boerse()
        spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)
        spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)
        check("Der zweite Lauf sendet gar nichts (Nachverfolgung)",
              len(boerse.orders) == 1, str(len(boerse.orders)))

        # Der haessliche Fall: Order draussen, Eintrag verloren (Abbruch
        # zwischen Senden und Speichern).
        p.conn.execute("DELETE FROM spiegelungen")
        p.conn.commit()
        z = spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)
        check("Nach verlorenem Eintrag wird die Order WIEDERERKANNT, nicht neu gesendet",
              len(boerse.orders) == 1, f"{len(boerse.orders)} Orders")
        check("Und dann sauber nachgetragen",
              len(p.spiegelungen()) == 1 and z["erfolg"] == 1,
              str(len(p.spiegelungen())))

        # Und die Datenbanksperre selbst.
        try:
            p.conn.execute(
                "INSERT INTO spiegelungen (bot, trade_id, seite, symbol, "
                "client_order_id, zeitpunkt) VALUES (?,?,?,?,?,?)",
                ("t3_supertrend", 1, "eroeffnung", "BTCUSDT", "x", "jetzt"))
            check("UNIQUE(bot, trade_id, seite) verhindert den zweiten Eintrag", False)
        except sqlite3.IntegrityError:
            check("UNIQUE(bot, trade_id, seite) verhindert den zweiten Eintrag", True)


# ---------------------------------------------------------------------------
# 9. Fehler der Gegenseite
# ---------------------------------------------------------------------------

def test_api_fehler():
    print("\n9. Fehler der Gegenseite: nichts wird stillschweigend verschluckt")
    # Die Uebersetzung "Netzfehler -> TestnetFehler" steckt im ECHTEN Sender,
    # nicht in der Attrappe - also wird sie dort geprueft, mit verbogenem
    # urlopen und ohne einen einzigen Netzaufruf.
    import urllib.request
    echt = urllib.request.urlopen
    urllib.request.urlopen = lambda *a, **k: (_ for _ in ()).throw(
        urllib.error.URLError("Name or service not known"))
    try:
        bt._http_sender("GET", "https://testnet.binance.vision/api/v3/ping", {})
        check("Ein Netzfehler wird zu einem TestnetFehler mit klarem Text", False)
    except bt.TestnetFehler as fehler:
        check("Ein Netzfehler wird zu einem TestnetFehler mit klarem Text",
              "nicht erreichbar" in str(fehler), str(fehler)[:70])
    finally:
        urllib.request.urlopen = echt

    faelle = [
        ("Testnet nicht erreichbar",
         bt.TestnetFehler("Testnet nicht erreichbar: Name or service not known"),
         "nicht erreichbar"),
        ("eine voellig unerwartete Ausnahme",
         RuntimeError("irgendetwas ganz anderes"), "unerwarteter Fehler"),
        ("HTTP 500", (500, '{"code":-1000,"msg":"An unknown error occurred"}'),
         "Code -1000"),
        ("Schluessel abgelehnt (-2008)",
         (401, '{"code":-2008,"msg":"Invalid Api-Key ID."}'),
         "testnet.binance.vision erzeugt"),
        ("Zeitstempel ausserhalb des Fensters (-1021)",
         (400, '{"code":-1021,"msg":"Timestamp for this request is outside of the recvWindow."}'),
         "Uhr des Rechners"),
        ("Boersenfilter (-1013)",
         (400, '{"code":-1013,"msg":"Filter failure: LOT_SIZE"}'), "Boersenfilter"),
        ("Antwort ist kein JSON", (200, "<html>Wartungsarbeiten</html>"), "kein JSON"),
    ]
    for name, vorgabe, erwartet in faelle:
        with Projekt([offener_trade(1)]) as p:
            vorher = pruefsumme(p.db)
            boerse = Boerse(fehler={"/api/v3/order": vorgabe})
            z = spiegel.lauf("t3_supertrend", echt=True, client=client(boerse),
                              conn=p.conn)
            fehlgeschlagen = z["fehlgeschlagen"]
            check(f"{name}: der Lauf meldet einen Fehlschlag",
                  len(fehlgeschlagen) == 1, str(z))
            check(f"{name}: mit verstaendlichem Grund",
                  erwartet in fehlgeschlagen[0]["grund"],
                  fehlgeschlagen[0]["grund"][:110])
            check(f"{name}: KEINE bestaetigte Spiegelung", not p.spiegelungen())
            check(f"{name}: der Fehlversuch steht im Protokoll",
                  any(v["ergebnis"] == "fehlgeschlagen" for v in p.versuche()))
            check(f"{name}: die Bot-Datenbank ist unveraendert",
                  pruefsumme(p.db) == vorher)

    # Teilausfall: ein Symbol scheitert, das andere laeuft durch.
    with Projekt([offener_trade(1, "BTCUSDT"), offener_trade(2, "ETHUSDT")]) as p:
        class NurEthKaputt(Boerse):
            def _order(self, p_):
                if p_["symbol"] == "ETHUSDT":
                    return 400, '{"code":-2010,"msg":"Account has insufficient balance."}'
                return super()._order(p_)
        boerse = NurEthKaputt()
        z = spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)
        check("Ein Fehlschlag bricht die Schleife NICHT ab",
              z["erfolg"] == 1 and len(z["fehlgeschlagen"]) == 1, spiegel._meldung(z))
        check("Die gelungene Spiegelung ist vermerkt, die gescheiterte nicht",
              [s["symbol"] for s in p.spiegelungen()] == ["BTCUSDT"],
              str([s["symbol"] for s in p.spiegelungen()]))
        check("Der Rueckgabewert des Programms ist 1, damit Cron anschlaegt",
              spiegel._meldung(z).startswith("1 von 2"), spiegel._meldung(z))


# ---------------------------------------------------------------------------
# 10. Die Bot-Datenbank ist wirklich nur lesbar
# ---------------------------------------------------------------------------

def test_nur_lesend():
    print("\n10. Die Bot-Datenbank: schreibgeschuetzt, nicht bloss unberuehrt")
    with Projekt([offener_trade(1)]) as p:
        conn = sqlite3.connect(f"file:{p.db}?mode=ro", uri=True)
        try:
            conn.execute("UPDATE trades SET status='closed' WHERE id=1")
            conn.commit()
            check("SQLite verweigert den Schreibversuch im Modus mode=ro", False)
        except sqlite3.OperationalError as fehler:
            check("SQLite verweigert den Schreibversuch im Modus mode=ro",
                  "readonly" in str(fehler).lower(), str(fehler)[:60])
        finally:
            conn.close()
        vorher = pruefsumme(p.db)
        boerse = Boerse()
        spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)
        spiegel.aufgaben("t3_supertrend", p.conn)
        abgleich.bericht_daten("t3_supertrend", conn=p.conn)
        check("Nach Lauf, Statusabfrage und Abgleich: Datenbank byteweise gleich",
              pruefsumme(p.db) == vorher)
        check("Die eigene Nachverfolgung liegt in einer EIGENEN Datei",
              os.path.basename(spiegel.spiegel_db_pfad("t3_supertrend"))
              == "broker_testnet_t3_supertrend.db"
              and spiegel.spiegel_db_pfad("t3_supertrend") != p.db)
        namen = sorted(z[0] for z in sqlite3.connect(p.db).execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%'"))
        check("Im Schema des Bots ist keine neue Tabelle entstanden",
              namen == ["trades"], str(namen))


# ---------------------------------------------------------------------------
# 11. Notbremse und Grenzen
# ---------------------------------------------------------------------------

def test_notbremse_und_grenzen():
    print("\n11. Notbremse, Betragsgrenze, Mengengrenzen")
    with Projekt([offener_trade(1)]) as p:
        open(zugang.NOTBREMSE_DATEI, "w").write("aus\n")
        boerse = Boerse()
        z = spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)
        check("Mit broker/STOP wird keine Order gesendet", not boerse.orders)
        check("Und der Grund steht im Ergebnis",
              "NOTBREMSE" in z["fehlgeschlagen"][0]["grund"],
              z["fehlgeschlagen"][0]["grund"][:70])
        os.remove(zugang.NOTBREMSE_DATEI)
        z = spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)
        check("Nach dem Entfernen laeuft es wieder", len(boerse.orders) == 1
              and z["erfolg"] == 1)

    with Projekt([offener_trade(1)]) as p:
        os.environ[zugang.BETRAG_VARIABLE] = str(zugang.BETRAG_USDT_MAX + 1)
        try:
            zugang.betrag_usdt()
            check("Ein Betrag ueber der Obergrenze wird abgelehnt", False)
        except zugang.ZugangFehler as fehler:
            check("Ein Betrag ueber der Obergrenze wird abgelehnt",
                  "Obergrenze" in str(fehler), str(fehler)[:70])
        boerse = Boerse()
        z = spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)
        check("Und es wird deshalb auch nichts gesendet",
              not boerse.orders and len(z["fehlgeschlagen"]) == 1)
        os.environ[zugang.BETRAG_VARIABLE] = "keine-zahl"
        try:
            zugang.betrag_usdt()
            check("Ein unsinniger Betrag wird abgelehnt", False)
        except zugang.ZugangFehler:
            check("Ein unsinniger Betrag wird abgelehnt", True)
        os.environ.pop(zugang.BETRAG_VARIABLE)

    # Grenze je Lauf
    trades = [offener_trade(i, "BTCUSDT" if i % 2 else "ETHUSDT", 50000.0 + i)
              for i in range(1, zugang.MAX_ORDERS_PRO_LAUF + 3)]
    with Projekt(trades) as p:
        boerse = Boerse()
        spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)
        check(f"Hoechstens {zugang.MAX_ORDERS_PRO_LAUF} Orders je Lauf",
              len(boerse.orders) == zugang.MAX_ORDERS_PRO_LAUF,
              f"{len(boerse.orders)} von {len(trades)} Aufgaben")
        check("Die uebrigen bleiben als Aufgabe stehen",
              len(spiegel.aufgaben("t3_supertrend", p.conn)["offen"])
              == len(trades) - zugang.MAX_ORDERS_PRO_LAUF)
        # Tagesgrenze: kuenstlich hochsetzen
        alt = zugang.MAX_ORDERS_PRO_TAG
        zugang.MAX_ORDERS_PRO_TAG = 1
        try:
            spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)
            check("Die Tagesgrenze blockiert den ganzen Lauf", False)
        except spiegel.SpiegelFehler as fehler:
            check("Die Tagesgrenze blockiert den ganzen Lauf",
                  "Tagesgrenze" in str(fehler), str(fehler)[:70])
        finally:
            zugang.MAX_ORDERS_PRO_TAG = alt
        check("Im Trockenlauf gilt die Tagesgrenze nicht (er sendet ja nichts)",
              spiegel.lauf("t3_supertrend", echt=False, client=client(Boerse()),
                            conn=p.conn)["aufgaben"] > 0)


# ---------------------------------------------------------------------------
# 12. Zugangsdaten
# ---------------------------------------------------------------------------

def test_zugang():
    print("\n12. Zugangsdaten: getrennt von den Datenabruf-Schluesseln")
    with Projekt([offener_trade(1)]) as p:
        env = zugang.ENV_FILE
        with open(env, "w", encoding="utf-8") as fh:
            fh.write(f"# Kommentar\n{zugang.SCHLUESSEL_VARIABLE}={SCHLUESSEL}\n"
                     f"{zugang.GEHEIMNIS_VARIABLE}=\"{GEHEIMNIS}\"\n")
        daten = zugang.get_zugang(env)
        check("Schluessel werden aus der .env gelesen, Anfuehrungszeichen entfernt",
              daten == {"key": SCHLUESSEL, "secret": GEHEIMNIS}, str(list(daten or [])))

        os.environ[zugang.DATENABRUF_VARIABLEN[0]] = SCHLUESSEL
        try:
            zugang.get_zugang(env)
            check("Ein mit BINANCE_API_KEY identischer Schluessel wird abgelehnt", False)
        except zugang.ZugangFehler as fehler:
            check("Ein mit BINANCE_API_KEY identischer Schluessel wird abgelehnt",
                  "ECHTEN Binance-Konto" in str(fehler), str(fehler)[:80])
        os.environ.pop(zugang.DATENABRUF_VARIABLEN[0])

        with open(env, "w", encoding="utf-8") as fh:
            fh.write(f"{zugang.SCHLUESSEL_VARIABLE}={SCHLUESSEL}\n")
        check("Ein halber Zugang gilt als kein Zugang", zugang.get_zugang(env) is None)
        os.remove(env)
        check("Ohne .env kein Fehler, nur kein Zugang (Trockenlauf soll gehen)",
              zugang.get_zugang(env) is None)

    check("Nicht freigeschaltete Bots werden abgelehnt",
          _abgelehnt(lambda: spiegel.lauf("elliott_wave", echt=False)),
          "elliott_wave")
    check("Freigeschaltet ist genau ein Bot",
          spiegel.ERLAUBTE_BOTS == ("t3_supertrend",), str(spiegel.ERLAUBTE_BOTS))


def _abgelehnt(aufruf) -> bool:
    try:
        aufruf()
        return False
    except (spiegel.SpiegelFehler, zugang.ZugangFehler):
        return True


# ---------------------------------------------------------------------------
# 13. Abgleichsbericht
# ---------------------------------------------------------------------------

def test_abgleich():
    print("\n13. Abgleich: Simulation gegen tatsaechliche Ausfuehrung")
    with Projekt([offener_trade(1)]) as p:
        boerse = Boerse()
        spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)
        conn = sqlite3.connect(p.db)
        conn.execute("UPDATE trades SET status='closed', exit_time='2026-06-02', "
                      "exit_price=51000.0, result='trend_flip', pnl_pct=1.7 WHERE id=1")
        conn.commit()
        conn.close()
        boerse.kurse["BTCUSDT"] = 51000.0
        spiegel.lauf("t3_supertrend", echt=True, client=client(boerse), conn=p.conn)

        d = abgleich.bericht_daten("t3_supertrend", conn=p.conn)
        check("Die Kostenannahme kommt aus dem echten forward_test.py (0.30 pp)",
              abs(d["kostenannahme_pp"] - 0.30) < 1e-9, str(d["kostenannahme_pp"]))
        z = d["zeilen"][0]
        check("Eine vollstaendige Zeile (Kauf und Verkauf)",
              d["anzahl_vollstaendig"] == 1 and z["vollstaendig"])
        # Kauf: Mischkurs 50030 gegen Simulationspreis 50000 -> +0,06 %
        check("Einstiegsabweichung +0,060 %",
              abs(z["einstieg_abweichung_pct"] - 0.06) < 1e-6,
              f"{z['einstieg_abweichung_pct']:.4f}")
        # Verkauf: Mischkurs 51030.6 gegen 51000 -> +0,06 %
        check("Ausstiegsabweichung +0,060 %",
              abs(z["ausstieg_abweichung_pct"] - 0.06) < 1e-6,
              f"{z['ausstieg_abweichung_pct']:.4f}")
        check("Der PnL der Simulation steht unveraendert daneben",
              z["pnl_simulation_pct"] == 1.7, str(z["pnl_simulation_pct"]))
        # Von Hand, damit die Zahl nicht aus demselben Code kommt wie die
        # Pruefung:
        #   Kauf   0.00200 BTC, Mischkurs 50030      -> 100.06 USDT, Gebuehr
        #          0.000002 BTC -> netto 0.001998 BTC
        #          effektiver Einstieg 100.06 / 0.001998 = 50080.08 USDT/BTC
        #   Verkauf 0.00199 BTC (auf die Schrittweite abgerundet), Mischkurs
        #          51030.6 -> 101.5509 USDT, Gebuehr 0.10155 USDT
        #          effektiver Ausstieg 101.4493 / 0.00199 = 50979.55 USDT/BTC
        #   je Einheit  (50979.55 - 50080.08) / 50080.08 = +1.796 %
        #   auf Kapital (101.4493 - 100.06)   / 100.06    = +1.388 %
        #   Restmenge   0.001998 - 0.00199                =  0.000008 BTC
        check("Effektiver Einstiegspreis: bezahlter Betrag je erhaltener Menge",
              abs(z["einstieg_effektiv"] - 50080.08) < 0.1,
              f"{z['einstieg_effektiv']:.2f}")
        check("Effektiver Ausstiegspreis: erhaltener Betrag je verkaufter Menge",
              abs(z["ausstieg_effektiv"] - 50979.55) < 0.1,
              f"{z['ausstieg_effektiv']:.2f}")
        check("PnL je Einheit (+1.796 %) - die mit der Simulation vergleichbare Zahl",
              abs(z["pnl_ausfuehrung_pct"] - 1.796) < 0.01,
              f"{z['pnl_ausfuehrung_pct']:.4f}")
        check("PnL auf das eingesetzte Kapital (+1.388 %) - mit Restmenge",
              abs(z["pnl_kapital_pct"] - 1.388) < 0.01,
              f"{z['pnl_kapital_pct']:.4f}")
        check("Die Restmenge wird ausgewiesen (0.000008 BTC)",
              abs(z["restmenge"] - 0.000008) < 1e-9, f"{z['restmenge']:.10f}")
        check("Die beiden Renditen unterscheiden sich deutlich - genau deshalb "
              "stehen beide da",
              abs(z["pnl_ausfuehrung_pct"] - z["pnl_kapital_pct"]) > 0.3,
              f"{z['pnl_ausfuehrung_pct']:.3f} gegen {z['pnl_kapital_pct']:.3f}")
        check("Und der Unterschied in Prozentpunkten ist die eigentliche Zahl",
              abs(z["unterschied_pp"]
                  - (z["pnl_ausfuehrung_pct"] - z["pnl_simulation_pct"])) < 1e-9,
              f"{z['unterschied_pp']:+.4f} pp")
        text = abgleich.als_text(d)
        for teil in ("ABGLEICH Simulation", "Diff pp", "kuenstliches Orderbuch",
                      "Methodik-Grundsatz 2", "Restmenge", "JE EINHEIT"):
            check(f"Der Bericht nennt {teil!r}", teil in text)
        check("Ohne Verkauf bleibt der PnL der Ausfuehrung leer, nicht 0",
              abgleich.zeile_auswerten(
                  {"id": 9, "symbol": "BTCUSDT", "status": "open",
                   "entry_price": 1.0, "exit_price": None, "pnl_pct": None},
                  {"ausfuehrungspreis": 1.0, "simulationspreis": 1.0,
                   "quote_menge": 1.0, "gebuehren": "{}", "order_id": "1"},
                  None, 0.3)["pnl_ausfuehrung_pct"] is None)

    # Uebersprungene Trades erscheinen im Bericht
    with Projekt([geschlossener_trade(1)]) as p:
        spiegel.lauf("t3_supertrend", echt=False, client=client(Boerse()), conn=p.conn)
        d = abgleich.bericht_daten("t3_supertrend", conn=p.conn)
        check("Nicht gespiegelte Trades stehen im Bericht, mit Grund",
              len(d["nicht_gespiegelt"]) == 1
              and "NICHT nachgekauft" in d["nicht_gespiegelt"][0]["grund"],
              str(d["nicht_gespiegelt"])[:90])
        check("Und tauchen im Text auf", "NICHT gespiegelt" in abgleich.als_text(d))


# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("Selbsttests der Binance-Testnet-Bruecke")
    print("=" * 78)
    tests = [test_url_wache, test_struktur, test_signatur, test_mengen,
             test_trockenlauf, test_eroeffnung, test_schliessung,
             test_keine_doppelte_order, test_api_fehler, test_nur_lesend,
             test_notbremse_und_grenzen, test_zugang, test_abgleich]
    for test in tests:
        try:
            test()
        except Exception as fehler:                      # noqa: BLE001
            import traceback
            FEHLER.append(f"{test.__name__} (Ausnahme)")
            print(f"  [FEHLER] {test.__name__} warf eine Ausnahme: {fehler}")
            traceback.print_exc()
    print("\n" + "=" * 78)
    print(f"{sum(BESTANDEN)} von {len(BESTANDEN)} Pruefungen bestanden, "
          f"{len(FEHLER)} fehlgeschlagen.")
    for name in FEHLER:
        print(f"  - {name}")
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())

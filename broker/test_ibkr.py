"""
Selbsttests der IBKR-Paper-Bruecke
==============================================================================
Keine laufende TWS, keine Verbindung, kein Konto: die Gegenstelle ist eine
Attrappe, die sich wie ib_async verhaelt und jeden Aufruf mitschreibt. Damit
laesst sich pruefen, WAS gesendet worden waere - auch fuer die Faelle, die man
an einem echten Paper-Konto nicht herstellen kann (Live-Konto in der Sitzung,
Order ausserhalb der Handelszeiten, Abbruch nach dem Senden).

Zwei Stellen brauchen ib_async wirklich: der Bau des Kontrakt- und des
Order-Objekts. Sie werden in den Kernabschnitten durch Attrappen ersetzt, damit
die Tests auch auf einem Rechner ohne die Bibliothek laufen. Ist sie vorhanden,
prueft Abschnitt 9 zusaetzlich gegen die ECHTE Bibliothek, dass deren
Schnittstelle noch zu den Annahmen dieses Codes passt - eine Umbenennung dort
soll hier auffallen und nicht nachts im Cronjob.

Die Bot-Datenbank entsteht aus dem ECHTEN CREATE TABLE von
strategies/volatility_breakout/forward_test.py.

Aufruf:  python3 broker/test_ibkr.py
"""

import ast
import hashlib
import inspect
import os
import shutil
import sqlite3
import sys
import tempfile
from datetime import datetime
from zoneinfo import ZoneInfo

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DIR)
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)

import bot_db                       # noqa: E402
import ibkr_zugang as zugang         # noqa: E402
import ibkr_paper as ip              # noqa: E402
import ibkr_spiegel as spiegel       # noqa: E402
import ibkr_abgleich as abgleich     # noqa: E402

BESTANDEN = []
FEHLER = []
UEBERSPRUNGEN = []


def check(name, bedingung, detail=""):
    BESTANDEN.append(bool(bedingung))
    print(f"  [{'OK ' if bedingung else 'FEHLER'}] {name}"
          + (f"   {detail}" if detail else ""))
    if not bedingung:
        FEHLER.append(name)


# ---------------------------------------------------------------------------
# Attrappe von TWS
# ---------------------------------------------------------------------------
KONTO = "DU1234567"
ZONE = "US/Eastern"
# Donnerstag 10.09.2026 offen, Freitag 11.09. geschlossen (z. B. Feiertag),
# Montag 14.09. wieder offen - genau die Form, die IBKR liefert.
LIQUID = ("20260910:0930-20260910:1600;20260911:CLOSED;"
          "20260914:0930-20260914:1600")
IN_SITZUNG = datetime(2026, 9, 10, 11, 0, tzinfo=ZoneInfo(ZONE))
NACH_SCHLUSS = datetime(2026, 9, 10, 22, 30, tzinfo=ZoneInfo(ZONE))
FEIERTAG = datetime(2026, 9, 11, 11, 0, tzinfo=ZoneInfo(ZONE))


class FakeContract:
    def __init__(self, symbol, primary="NASDAQ"):
        self.symbol = symbol
        self.exchange = zugang.BOERSE
        self.primaryExchange = primary
        self.currency = zugang.WAEHRUNG

    def __repr__(self):
        return f"FakeContract({self.symbol})"


class FakeDetails:
    def __init__(self, contract, liquid=LIQUID, zone=ZONE, min_size=1.0,
                 schritt=1.0):
        self.contract = contract
        self.liquidHours = liquid
        self.tradingHours = liquid
        self.timeZoneId = zone
        self.minSize = min_size
        self.sizeIncrement = schritt
        self.longName = f"{contract.symbol} Inc"


class FakeOrder:
    def __init__(self, action, stueck):
        self.action = action
        self.totalQuantity = stueck
        self.orderType = "MKT"
        self.orderId = 0
        self.orderRef = ""
        self.account = ""
        self.tif = ""
        self.outsideRth = None


class FakeStatus:
    def __init__(self, status="Filled", filled=0.0, preis=0.0, perm=0):
        self.status = status
        self.filled = filled
        self.remaining = 0.0
        self.avgFillPrice = preis
        self.permId = perm


class FakeExecution:
    def __init__(self, shares, price, order_ref, zeit, perm):
        self.shares = shares
        self.price = price
        self.orderRef = order_ref
        self.time = zeit
        self.permId = perm
        self.execId = f"{perm}.{shares}.{price}"
        self.acctNumber = KONTO
        self.side = "BOT"


class FakeCommission:
    def __init__(self, betrag, waehrung="USD"):
        self.commission = betrag
        self.currency = waehrung


class FakeFill:
    def __init__(self, execution, commission):
        self.execution = execution
        self.commissionReport = commission


class FakeLog:
    def __init__(self, message, code=None, status=""):
        self.message = message
        self.errorCode = code
        self.status = status
        self.time = None


class FakeTrade:
    def __init__(self, contract, order, status, fills, log=None):
        self.contract = contract
        self.order = order
        self.orderStatus = status
        self.fills = fills
        self.log = log or []

    def isDone(self):
        return self.orderStatus.status in ("Filled", "Cancelled", "ApiCancelled",
                                            "Inactive")


class FakeIB:
    """Verhaelt sich wie ib_async.IB - so weit, wie diese Bruecke es benutzt."""

    def __init__(self, konten=None, liquid=LIQUID, treffer=1, kurse=None,
                 verbindungsfehler=None, orderfehler=None, order_status=None,
                 ohne_fill=False, min_size=1.0, schritt=1.0, zone=ZONE):
        self.konten = list(konten if konten is not None else [KONTO])
        self.liquid = liquid
        self.treffer = treffer
        self.kurse = kurse or {"AAPL": 200.0, "MSFT": 400.0, "BRK B": 500.0}
        self.verbindungsfehler = verbindungsfehler
        self.orderfehler = orderfehler
        self.order_status = order_status
        self.ohne_fill = ohne_fill
        self.min_size = min_size
        self.schritt = schritt
        self.zone = zone
        self.verbindungen = []
        self.getrennt = 0
        self.orders = []              # (contract, order)
        self._trades = []
        self._fills = []
        self.perm = 900000
        self.gebuehr = 1.0            # USD je Order, wie IBKRs Mindestprovision

    # -- Verbindung --------------------------------------------------------
    def connect(self, host, port, clientId=1, timeout=4, readonly=False, **kw):
        if self.verbindungsfehler is not None:
            raise self.verbindungsfehler
        self.verbindungen.append({"host": host, "port": port,
                                   "clientId": clientId, "timeout": timeout,
                                   "readonly": readonly})

    def disconnect(self):
        self.getrennt += 1

    def isConnected(self):
        return bool(self.verbindungen) and not self.getrennt

    def managedAccounts(self):
        return list(self.konten)

    # -- Kontrakte ---------------------------------------------------------
    def reqContractDetails(self, contract):
        if self.treffer == 0:
            return []
        return [FakeDetails(FakeContract(contract.symbol, f"BOERSE{i}"),
                             self.liquid, self.zone, self.min_size, self.schritt)
                for i in range(self.treffer)]

    # -- Orders ------------------------------------------------------------
    def placeOrder(self, contract, order):
        if self.orderfehler is not None:
            raise self.orderfehler
        self.orders.append((contract, order))
        self.perm += 1
        order.orderId = self.perm
        if self.ohne_fill:
            trade = FakeTrade(contract, order, FakeStatus("Submitted", 0.0, 0.0,
                                                           self.perm), [],
                               [FakeLog("Order wird uebermittelt")])
            self._trades.append(trade)
            return trade
        if self.order_status:
            trade = FakeTrade(contract, order,
                               FakeStatus(self.order_status, 0.0, 0.0, self.perm),
                               [], [FakeLog("abgelehnt vom Broker", 201)])
            self._trades.append(trade)
            return trade
        kurs = self.kurse[contract.symbol]
        gesamt = float(order.totalQuantity)
        # Zwei Teilausfuehrungen zu verschiedenen Kursen - so wird eine
        # Market-Order in der Wirklichkeit gefuellt, und nur so laesst sich der
        # mengengewichtete Mischkurs pruefen.
        erste = max(1.0, gesamt // 2) if gesamt > 1 else gesamt
        zweite = gesamt - erste
        stuecke = [(erste, kurs)] + ([(zweite, kurs * 1.002)] if zweite else [])
        fills = []
        for menge, preis in stuecke:
            ausf = FakeExecution(menge, preis, order.orderRef,
                                 "20260910 11:00:00", self.perm)
            fills.append(FakeFill(ausf, FakeCommission(
                self.gebuehr * menge / gesamt)))
        mittel = sum(m * p for m, p in stuecke) / gesamt
        trade = FakeTrade(contract, order,
                           FakeStatus("Filled", gesamt, mittel, self.perm), fills)
        self._trades.append(trade)
        self._fills.extend(fills)
        return trade

    def waitOnUpdate(self, timeout=0):
        # Die echte Fassung blockiert bis zum naechsten Ereignis; hier genuegt
        # ein Hauch, damit die Warteschleife nicht heiss laeuft.
        import time
        time.sleep(0.01)
        return True

    def fills(self):
        return list(self._fills)

    def trades(self):
        return list(self._trades)


def verbindung(ib, konto=KONTO, port=None):
    v = ip.PaperVerbindung(port=port or zugang.STANDARD_PORT,
                            client_id=7, erwartetes_konto=konto, ib=ib)
    v.verbinden()
    return v


# ---------------------------------------------------------------------------
# Synthetisches Projekt
# ---------------------------------------------------------------------------

def echtes_create_table() -> str:
    pfad = os.path.join(BASE_DIR, "strategies", "volatility_breakout",
                         "forward_test.py")
    baum = ast.parse(open(pfad, encoding="utf-8").read(), filename=pfad)
    for knoten in ast.walk(baum):
        if (isinstance(knoten, ast.Constant) and isinstance(knoten.value, str)
                and "CREATE TABLE" in knoten.value and "trades" in knoten.value):
            return knoten.value
    raise AssertionError("CREATE TABLE im echten forward_test.py nicht gefunden")


def echte_kostensaetze() -> dict:
    pfad = os.path.join(BASE_DIR, "strategies", "volatility_breakout",
                         "forward_test.py")
    baum = ast.parse(open(pfad, encoding="utf-8").read(), filename=pfad)
    werte = {}
    for knoten in baum.body:
        if isinstance(knoten, ast.Assign):
            for ziel in knoten.targets:
                if (isinstance(ziel, ast.Name)
                        and ziel.id in ("TRADING_FEE_PCT", "SLIPPAGE_PCT")):
                    werte[ziel.id] = float(ast.literal_eval(knoten.value))
    return werte


def offener_trade(tid, symbol="AAPL", entry=200.0, tag=None):
    # Die Signalzeit enthaelt die Trade-Nummer: die echte Tabelle hat
    # UNIQUE(symbol, signal_time), zwei Testtrades desselben Symbols mit
    # derselben Zeit gaebe es dort nicht.
    tag = tag or f"2026-09-{(tid % 9) + 1:02d}"
    return (tid, symbol, tag, tag, entry, entry * 0.92, None, None, None, None,
            "open")


def geschlossener_trade(tid, symbol="AAPL", entry=200.0, exit_=210.0,
                         grund="time_exit", pnl=4.7):
    return (tid, symbol, f"2026-09-0{tid % 9 + 1}", f"2026-09-0{tid % 9 + 1}",
            entry, entry * 0.92, "2026-09-10", exit_, grund, pnl, "closed")


def pruefsumme(pfad):
    return hashlib.sha256(open(pfad, "rb").read()).hexdigest()


class Projekt:
    """Biegt spiegel/zugang auf ein Wegwerf-Verzeichnis um und ersetzt die zwei
    Stellen, die ib_async brauchen."""

    def __init__(self, trades):
        self.trades = trades

    def __enter__(self):
        self.wurzel = tempfile.mkdtemp(prefix="ibkr_test_")
        ordner = os.path.join(self.wurzel, "strategies", "volatility_breakout")
        os.makedirs(ordner, exist_ok=True)
        saetze = echte_kostensaetze()
        with open(os.path.join(ordner, "forward_test.py"), "w",
                   encoding="utf-8") as fh:
            fh.write(f"TRADING_FEE_PCT = {saetze['TRADING_FEE_PCT']}\n"
                     f"SLIPPAGE_PCT = {saetze['SLIPPAGE_PCT']}\n")
        self.db = os.path.join(self.wurzel,
                                "paper_trading_volatility_breakout.db")
        conn = sqlite3.connect(self.db)
        conn.execute(echtes_create_table())
        conn.executemany(
            "INSERT INTO trades (id, symbol, signal_time, entry_time, "
            "entry_price, stop_price, exit_time, exit_price, result, pnl_pct, "
            "status) VALUES (?,?,?,?,?,?,?,?,?,?,?)", self.trades)
        conn.commit()
        conn.close()

        # Das Warten auf eine Ausfuehrung wird im Test auf Bruchteile einer
        # Sekunde gekuerzt. Sonst wartet der Fall "Order bleibt haengen"
        # wirklich eine Minute - der Test wuerde das richtige pruefen und waere
        # trotzdem unbenutzbar.
        self.alt = (spiegel.BASE_DIR, zugang.ENV_FILE, zugang.NOTBREMSE_DATEI,
                    ip._aktie, ip._marktorder, ip.ZEITLIMIT_AUSFUEHRUNG)
        ip.ZEITLIMIT_AUSFUEHRUNG = 0.2
        spiegel.BASE_DIR = self.wurzel
        zugang.ENV_FILE = os.path.join(self.wurzel, ".env")
        zugang.NOTBREMSE_DATEI = os.path.join(self.wurzel, "STOP_IBKR")
        ip._aktie = lambda symbol: FakeContract(zugang.ibkr_symbol(symbol))
        ip._marktorder = _fake_marktorder
        for name in (zugang.KONTO_VARIABLE, zugang.PORT_VARIABLE,
                      zugang.STUECK_VARIABLE, zugang.CLIENT_ID_VARIABLE):
            os.environ.pop(name, None)
        self.conn = spiegel.oeffne_spiegel_db("volatility_breakout")
        return self

    def __exit__(self, *a):
        self.conn.close()
        (spiegel.BASE_DIR, zugang.ENV_FILE, zugang.NOTBREMSE_DATEI,
         ip._aktie, ip._marktorder, ip.ZEITLIMIT_AUSFUEHRUNG) = self.alt
        shutil.rmtree(self.wurzel, ignore_errors=True)
        return False

    def spiegelungen(self):
        return [dict(z) for z in self.conn.execute(
            "SELECT * FROM spiegelungen ORDER BY id")]

    def versuche(self):
        return [dict(z) for z in self.conn.execute(
            "SELECT * FROM versuche ORDER BY id")]


def _fake_marktorder(seite, stueck, order_ref, konto):
    if seite not in ("BUY", "SELL"):
        raise ip.IbkrFehler(f"Unbekannte Seite {seite!r}")
    order = FakeOrder(seite, stueck)
    order.orderRef = order_ref
    order.account = konto
    order.tif = "DAY"
    order.outsideRth = False
    return order


# ---------------------------------------------------------------------------
# 1. Port-Wache
# ---------------------------------------------------------------------------

def test_port_wache():
    print("\n1. Port-Wache: nur die Paper-Ports, Live-Ports namentlich abgelehnt")
    for name, port in zugang.PAPER_PORTS.items():
        check(f"{name}-Paper-Port {port} ist erlaubt",
              zugang.pruefe_port(port) == port)
    for name, port in zugang.LIVE_PORTS.items():
        try:
            zugang.pruefe_port(port)
            check(f"{name}-LIVE-Port {port} wird abgelehnt", False)
        except zugang.ZugangFehler as fehler:
            check(f"{name}-LIVE-Port {port} wird abgelehnt",
                  "LIVE-Port" in str(fehler) and name in str(fehler),
                  str(fehler)[:70])
    for port in (0, 1, 7498, 4003, 65535):
        try:
            zugang.pruefe_port(port)
            check(f"Port {port} wird abgelehnt", False)
        except zugang.ZugangFehler:
            check(f"Port {port} wird abgelehnt", True)

    with Projekt([offener_trade(1)]) as p:
        with open(zugang.ENV_FILE, "w", encoding="utf-8") as fh:
            fh.write(f"{zugang.PORT_VARIABLE}={zugang.LIVE_PORTS['TWS']}\n")
        try:
            zugang.port(zugang.ENV_FILE)
            check("Auch aus der .env kommt kein Live-Port durch", False)
        except zugang.ZugangFehler as fehler:
            check("Auch aus der .env kommt kein Live-Port durch",
                  "LIVE-Port" in str(fehler), str(fehler)[:60])
        with open(zugang.ENV_FILE, "w", encoding="utf-8") as fh:
            fh.write(f"{zugang.PORT_VARIABLE}=4002\n")
        check("Ein gueltiger Paper-Port aus der .env wird uebernommen",
              zugang.port(zugang.ENV_FILE) == 4002)

    # Die Wache haengt nicht nur am Konstruktor: der Port wird beim VERBINDEN
    # erneut geprueft, so wie ein kuenftiger Fehler ihn verstellen wuerde.
    ib = FakeIB()
    v = ip.PaperVerbindung(port=zugang.STANDARD_PORT, client_id=1,
                            erwartetes_konto=KONTO, ib=ib)
    v.gewuenschter_port = zugang.LIVE_PORTS["TWS"]
    try:
        v.verbinden()
        check("Ein verbogener Port wird beim VERBINDEN abgefangen", False)
    except zugang.ZugangFehler as fehler:
        check("Ein verbogener Port wird beim VERBINDEN abgefangen",
              "LIVE-Port" in str(fehler) and not ib.verbindungen,
              f"{len(ib.verbindungen)} Verbindungen")


# ---------------------------------------------------------------------------
# 2. Konto-Wache
# ---------------------------------------------------------------------------

def test_konto_wache():
    print("\n2. Konto-Wache: nur Paper-Konten, und nur das erwartete")
    ib = FakeIB()
    v = verbindung(ib)
    check("Ein DU-Konto wird bestaetigt", v.konto == KONTO, v.konto)
    check("Verbunden wurde auf dem Paper-Port und mit dem Host-Literal",
          ib.verbindungen[0]["host"] == "127.0.0.1"
          and ib.verbindungen[0]["port"] == zugang.STANDARD_PORT,
          str(ib.verbindungen[0]))

    for konten, teil in (
            (["U1234567"], "kein Paper-Konto"),
            ([KONTO, "U7654321"], "kein Paper-Konto"),
            ([], "kein Konto gemeldet")):
        ib2 = FakeIB(konten=konten)
        try:
            verbindung(ib2, konto=KONTO if konten else None)
            check(f"Konten {konten} werden abgelehnt", False)
        except zugang.ZugangFehler as fehler:
            check(f"Konten {konten} werden abgelehnt", teil in str(fehler),
                  str(fehler)[:75])
        check(f"Und die Sitzung wird dabei getrennt ({konten})", ib2.getrennt >= 1
              or not ib2.verbindungen)

    ib3 = FakeIB(konten=["DU9999999"])
    try:
        verbindung(ib3, konto=KONTO)
        check("Ein anderes Paper-Konto als das erwartete wird abgelehnt", False)
    except zugang.ZugangFehler as fehler:
        check("Ein anderes Paper-Konto als das erwartete wird abgelehnt",
              "erwartete Konto" in str(fehler), str(fehler)[:75])

    ib4 = FakeIB(konten=["DU1", "DU2"])
    try:
        ip.PaperVerbindung(port=7497, client_id=1, erwartetes_konto=None,
                            ib=ib4).verbinden()
        check("Bei mehreren Konten ohne Angabe wird nicht geraten", False)
    except zugang.ZugangFehler as fehler:
        check("Bei mehreren Konten ohne Angabe wird nicht geraten",
              "mehrere Konten" in str(fehler), str(fehler)[:70])

    check("Ein DF-Konto gilt ebenfalls als Paper",
          zugang.ist_paper_konto("DF1234567"))
    check("Ein U-Konto nicht", not zugang.ist_paper_konto("U1234567"))
    with Projekt([offener_trade(1)]) as p:
        with open(zugang.ENV_FILE, "w", encoding="utf-8") as fh:
            fh.write(f"{zugang.KONTO_VARIABLE}=U1234567\n")
        try:
            zugang.erwartetes_konto(zugang.ENV_FILE)
            check("Ein Live-Konto in der .env wird abgelehnt", False)
        except zugang.ZugangFehler as fehler:
            check("Ein Live-Konto in der .env wird abgelehnt",
                  "Praefix" in str(fehler), str(fehler)[:70])

    # BEIDE Absicherungen muessen halten - nicht eine von beiden.
    ib5 = FakeIB(konten=["U1234567"])
    try:
        ip.PaperVerbindung(port=zugang.STANDARD_PORT, client_id=1,
                            erwartetes_konto=None, ib=ib5).verbinden()
        check("Richtiger Port, aber Live-Konto: abgelehnt", False)
    except zugang.ZugangFehler:
        check("Richtiger Port, aber Live-Konto: abgelehnt", True)
    ib6 = FakeIB(konten=[KONTO])
    v6 = ip.PaperVerbindung(port=zugang.STANDARD_PORT, client_id=1,
                             erwartetes_konto=KONTO, ib=ib6)
    v6.gewuenschter_port = zugang.LIVE_PORTS["IB Gateway"]
    try:
        v6.verbinden()
        check("Richtiges Konto, aber Live-Port: abgelehnt", False)
    except zugang.ZugangFehler:
        check("Richtiges Konto, aber Live-Port: abgelehnt", True)


# ---------------------------------------------------------------------------
# 3. Struktureller Nachweis
# ---------------------------------------------------------------------------

def test_struktur():
    print("\n3. Struktureller Nachweis am Quelltext")
    quelle_zugang = open(os.path.join(_DIR, "ibkr_zugang.py"),
                          encoding="utf-8").read()
    baum = ast.parse(quelle_zugang)
    literale = {}
    for knoten in baum.body:
        if isinstance(knoten, ast.Assign) and isinstance(knoten.value, ast.Constant):
            for ziel in knoten.targets:
                if isinstance(ziel, ast.Name):
                    literale[ziel.id] = knoten.value.value
    check("HOST ist ein Literal (127.0.0.1)", literale.get("HOST") == "127.0.0.1",
          str(literale.get("HOST")))
    verdaechtig = [z for z in quelle_zugang.splitlines()
                   if "HOST" in z and ("environ" in z or "getenv" in z)]
    check("Keine Umgebungsvariable setzt den Host", not verdaechtig, str(verdaechtig))
    check("Paper- und Live-Ports stehen als Literale getrennt da",
          zugang.PAPER_PORTS == {"TWS": 7497, "IB Gateway": 4002}
          and zugang.LIVE_PORTS == {"TWS": 7496, "IB Gateway": 4001},
          f"{zugang.PAPER_PORTS} / {zugang.LIVE_PORTS}")

    quelle_paper = open(os.path.join(_DIR, "ibkr_paper.py"), encoding="utf-8").read()
    quelle_spiegel = open(os.path.join(_DIR, "ibkr_spiegel.py"),
                           encoding="utf-8").read()
    for datei, quelle in (("ibkr_paper.py", quelle_paper),
                           ("ibkr_spiegel.py", quelle_spiegel),
                           ("ibkr_zugang.py", quelle_zugang)):
        b = ast.parse(quelle)
        oben = set()
        for knoten in b.body:
            if isinstance(knoten, ast.Import):
                oben.update(a.name for a in knoten.names)
            elif isinstance(knoten, ast.ImportFrom):
                oben.add(knoten.module or "")
        check(f"{datei} importiert ib_async NICHT auf Modulebene "
              f"(Tests und --status laufen ohne die Bibliothek)",
              not any("ib_async" in name for name in oben), str(sorted(oben))[:90])
        check(f"{datei} enthaelt kein exec()/eval()",
              not any(isinstance(k, ast.Name) and k.id in ("exec", "eval")
                      for k in ast.walk(b)))
    check("ib_async wird an genau EINER Stelle importiert (plus Kontrakt/Order)",
          quelle_paper.count("from ib_async import") == 3,
          f"{quelle_paper.count('from ib_async import')} Importe")
    check("Kein Bot-Modul wird importiert",
          not any(t in quelle_spiegel for t in ("import forward_test",
                                                 "import live_params")))
    quelle_botdb = open(os.path.join(_DIR, "bot_db.py"), encoding="utf-8").read()
    check("Die Bot-Datenbank wird schreibgeschuetzt geoeffnet (mode=ro)",
          "mode=ro" in quelle_botdb and "uri=True" in quelle_botdb)
    check("Und ibkr_spiegel.py oeffnet sie nicht auf eigenem Weg",
          "paper_trading_" not in quelle_spiegel
          and "bot_db.lies_trades" in quelle_spiegel)
    check("Kein INSERT/UPDATE/DELETE auf die trades-Tabelle",
          not any(f"{wort} trades" in quelle_spiegel.upper()
                  for wort in ("INSERT INTO", "UPDATE", "DELETE FROM")))
    check("Die Notbremse hat eine EIGENE Datei, nicht die der Binance-Bruecke",
          zugang.NOTBREMSE_DATEI.endswith("STOP_IBKR"))
    check("Nur ein Bot ist freigeschaltet",
          spiegel.ERLAUBTE_BOTS == ("volatility_breakout",),
          str(spiegel.ERLAUBTE_BOTS))


# ---------------------------------------------------------------------------
# 4. Symbole und Kontrakte
# ---------------------------------------------------------------------------

def test_symbole():
    print("\n4. Symbole: uebersetzt, wo noetig - und abgelehnt, wo unklar")
    check("AAPL bleibt AAPL", zugang.ibkr_symbol("AAPL") == "AAPL")
    check("BRK-B wird zu 'BRK B' (IBKR-Schreibweise)",
          zugang.ibkr_symbol("BRK-B") == "BRK B", zugang.ibkr_symbol("BRK-B"))
    check("Die Uebersetzung deckt genau die Sonderfaelle des Universums ab",
          set(zugang.SYMBOL_UEBERSETZUNG) == {
              s for s in open(os.path.join(BASE_DIR, "config",
                                            "sp500_top150.txt"),
                               encoding="utf-8").read().split()
              if any(z in s for z in ".-")},
          str(sorted(zugang.SYMBOL_UEBERSETZUNG)))
    check("Leerzeichen aussen stoeren nicht", zugang.ibkr_symbol("AAPL ") == "AAPL")
    # Bei Sonderzeichen wird nicht nur ABGELEHNT, sondern der GRUND geprueft:
    # er muss auf die Uebersetzungstabelle zeigen, sonst weiss niemand, wie das
    # zu beheben ist. (Ohne diese Zusatzpruefung blieb die Gegenprobe stumm -
    # der allgemeine isalpha()-Riegel faengt dieselben Faelle ab und die
    # Pruefung war gruen, obwohl die eigentliche Regel entfernt war.)
    for schlecht in ("BF.B", "RDS-A", "BRK B", "A/B"):
        try:
            zugang.ibkr_symbol(schlecht)
            check(f"{schlecht!r} wird abgelehnt", False, "wurde akzeptiert")
        except zugang.ZugangFehler as fehler:
            check(f"{schlecht!r} wird abgelehnt, und der Grund nennt die "
                  f"Uebersetzungstabelle",
                  "SYMBOL_UEBERSETZUNG" in str(fehler), str(fehler)[:70])
    for schlecht in ("", "123", "AA1"):
        try:
            zugang.ibkr_symbol(schlecht)
            check(f"{schlecht!r} wird abgelehnt", False, "wurde akzeptiert")
        except zugang.ZugangFehler as fehler:
            check(f"{schlecht!r} wird abgelehnt", True, str(fehler)[:55])

    # _aktie auch hier durch die Attrappe ersetzen. Ohne das baut kontrakt()
    # einen ECHTEN ib_async-Kontrakt, und auf einem Rechner ohne die Bibliothek
    # scheiterten diese zwei Pruefungen an "ib_async fehlt" - mit roter Meldung
    # an der falschen Stelle, statt das zu pruefen, was hier gemeint ist. Die
    # Suite soll ohne die optionale Bibliothek vollstaendig gruen sein; was sich
    # nur gegen die echte Bibliothek pruefen laesst, steht in Abschnitt 13 und
    # wird dort sichtbar uebersprungen.
    alt_aktie = ip._aktie
    ip._aktie = lambda symbol: FakeContract(zugang.ibkr_symbol(symbol))
    try:
        ib = FakeIB(treffer=2)
        v = verbindung(ib)
        try:
            v.kontrakt("AAPL")
            check("Ein mehrdeutiges Kuerzel wird abgelehnt statt geraten", False)
        except ip.IbkrFehler as fehler:
            check("Ein mehrdeutiges Kuerzel wird abgelehnt statt geraten",
                  "nicht eindeutig" in str(fehler), str(fehler)[:75])
        ib0 = FakeIB(treffer=0)
        try:
            verbindung(ib0).kontrakt("AAPL")
            check("Ein unbekanntes Kuerzel wird abgelehnt", False)
        except ip.IbkrFehler as fehler:
            check("Ein unbekanntes Kuerzel wird abgelehnt",
                  "keinen Kontrakt" in str(fehler), str(fehler)[:60])
    finally:
        ip._aktie = alt_aktie


# ---------------------------------------------------------------------------
# 5. Handelszeiten
# ---------------------------------------------------------------------------

def test_handelszeiten():
    print("\n5. Handelszeiten: aus den Angaben der Boerse, nicht aus einem "
          "eigenen Kalender")
    details = FakeDetails(FakeContract("AAPL"))
    fenster = ip.zeitfenster(details)
    check("Zwei Fenster erkannt, der CLOSED-Tag fehlt darin",
          len(fenster) == 2, str(len(fenster)))
    check("Das erste Fenster ist 09:30 bis 16:00 Ortszeit der Boerse",
          fenster[0][0].hour == 9 and fenster[0][0].minute == 30
          and fenster[0][1].hour == 16, str(fenster[0]))
    offen, grund = ip.in_handelszeiten(details, IN_SITZUNG)
    check("Mitten in der Sitzung: handelbar", offen and grund is None)
    offen, grund = ip.in_handelszeiten(details, NACH_SCHLUSS)
    check("Nach dem Schluss: nicht handelbar, mit Grund und naechster Sitzung",
          not offen and "ausserhalb der regulaeren Handelszeiten" in grund
          and "20260914" in grund.replace("-", ""), grund)
    offen, _ = ip.in_handelszeiten(details, FEIERTAG)
    check("Am CLOSED-Tag: nicht handelbar", not offen)
    for liquid, zone, teil in (("", ZONE, "keine Handelszeiten"),
                                (LIQUID, "", "keine Handelszeiten"),
                                ("Unsinn", ZONE, "nicht lesbar"),
                                (LIQUID, "Mars/Olympus", "Unbekannte Zeitzone")):
        try:
            ip.zeitfenster(FakeDetails(FakeContract("AAPL"), liquid, zone))
            check(f"Unbrauchbare Angaben werden abgelehnt ({teil})", False)
        except ip.IbkrFehler as fehler:
            check(f"Unbrauchbare Angaben werden abgelehnt ({teil})",
                  teil in str(fehler), str(fehler)[:60])
    check("Die kurze Form '0930-1600' wird auch verstanden",
          len(ip.zeitfenster(FakeDetails(FakeContract("AAPL"),
                                          "20260910:0930-1600"))) == 1)

    # Und die Bruecke sendet ausserhalb der Zeiten NICHTS.
    with Projekt([offener_trade(1)]) as p:
        ib = FakeIB()
        z = spiegel.lauf("volatility_breakout", echt=True, verbindung=verbindung(ib),
                          conn=p.conn, jetzt=NACH_SCHLUSS)
        check("Ausserhalb der Handelszeiten wird keine Order gesendet",
              not ib.orders, str(ib.orders))
        check("Die Aufgabe wartet und ist nicht verloren",
              len(z["wartet"]) == 1 and not p.spiegelungen()
              and len(spiegel.aufgaben("volatility_breakout",
                                        p.conn)["offen"]) == 1,
              str(z["wartet"])[:80])
        check("Der Grund steht im Protokoll",
              any("ausserhalb der regulaeren Handelszeiten" in (v["grund"] or "")
                  for v in p.versuche()))
        z = spiegel.lauf("volatility_breakout", echt=True, verbindung=verbindung(ib),
                          conn=p.conn, jetzt=IN_SITZUNG)
        check("In der Sitzung laeuft dieselbe Aufgabe durch",
              len(ib.orders) == 1 and z["erfolg"] == 1)


# ---------------------------------------------------------------------------
# 6. Trockenlauf, Eroeffnung, Schliessung
# ---------------------------------------------------------------------------

def test_trockenlauf():
    print("\n6. Trockenlauf: rechnet alles durch und sendet NICHTS")
    with Projekt([offener_trade(1)]) as p:
        vorher = pruefsumme(p.db)
        ib = FakeIB()
        z = spiegel.lauf("volatility_breakout", echt=False,
                          verbindung=verbindung(ib), conn=p.conn, jetzt=IN_SITZUNG)
        check("Eine Aufgabe erkannt", z["aufgaben"] == 1)
        check("Keine Order gesendet", not ib.orders)
        check("Keine bestaetigte Spiegelung", not p.spiegelungen())
        versuche = p.versuche()
        check("Der Versuch steht im Protokoll, mit Richtung und Stueckzahl",
              len(versuche) == 1 and versuche[0]["ergebnis"] == "trockenlauf"
              and "BUY 1 Stueck AAPL" in versuche[0]["grund"],
              str(versuche[0]["grund"]))
        check("Die Bot-Datenbank ist byteweise unveraendert",
              pruefsumme(p.db) == vorher)
        quelle = inspect.getsource(spiegel.main)
        check("Senden verlangt ausdruecklich --echt",
              "echt=args.echt" in quelle and "--echt" in quelle)
        check("Der Pruefschritt verbindet NUR LESEND",
              "nur_lesen=True" in inspect.getsource(spiegel._pruefen))


def test_eroeffnung():
    print("\n7. Eroeffnung: Order-Felder, Mischkurs, Nachverfolgung")
    with Projekt([offener_trade(1)]) as p:
        vorher = pruefsumme(p.db)
        ib = FakeIB()
        z = spiegel.lauf("volatility_breakout", echt=True,
                          verbindung=verbindung(ib), conn=p.conn, jetzt=IN_SITZUNG)
        check("Genau eine Order gesendet", len(ib.orders) == 1)
        contract, order = ib.orders[0]
        check("MARKET BUY mit unserer eigenen Kennung im orderRef",
              (order.action, order.orderType, order.orderRef)
              == ("BUY", "MKT", "vb-1-k"),
              f"{order.action}/{order.orderType}/{order.orderRef}")
        check("Das bestaetigte Paper-Konto steht ausdruecklich in der Order",
              order.account == KONTO, order.account)
        check("tif=DAY und outsideRth=False - keine Ausfuehrung nach Schluss",
              order.tif == "DAY" and order.outsideRth is False,
              f"{order.tif}/{order.outsideRth}")
        check("Gehandelt wird das uebersetzte Kuerzel",
              contract.symbol == "AAPL", contract.symbol)
        zeile = p.spiegelungen()[0]
        check("Die Spiegelung ist vermerkt, mit Order-ID und Konto",
              zeile["order_id"] and zeile["konto"] == KONTO
              and zeile["status"] == "Filled", str(zeile["order_id"]))
        check("Der Ausfuehrungspreis ist MENGENGEWICHTET (1 Stueck: 200.00)",
              abs(zeile["ausfuehrungspreis"] - 200.0) < 1e-9,
              str(zeile["ausfuehrungspreis"]))
        check("Die Provision ist in USD vermerkt",
              abs(zeile["gebuehr"] - 1.0) < 1e-9
              and zeile["gebuehr_waehrung"] == "USD", str(zeile["gebuehr"]))
        check("Der Simulationspreis des Bots steht daneben",
              zeile["simulationspreis"] == 200.0)
        check("Die Bot-Datenbank ist byteweise unveraendert",
              pruefsumme(p.db) == vorher)

    # Mehrere Stueck: zwei Teilausfuehrungen, Mischkurs dazwischen
    with Projekt([offener_trade(1)]) as p:
        os.environ[zugang.STUECK_VARIABLE] = "4"
        try:
            ib = FakeIB()
            spiegel.lauf("volatility_breakout", echt=True,
                          verbindung=verbindung(ib), conn=p.conn, jetzt=IN_SITZUNG)
            zeile = p.spiegelungen()[0]
            # 2 Stueck zu 200.00 und 2 zu 200.40 -> 200.20
            check("Vier Stueck, Mischkurs 200.20 aus zwei Teilausfuehrungen",
                  abs(zeile["ausfuehrungspreis"] - 200.2) < 1e-6
                  and zeile["stueck"] == 4, str(zeile["ausfuehrungspreis"]))
        finally:
            os.environ.pop(zugang.STUECK_VARIABLE)


def test_schliessung():
    print("\n8. Schliessung: nur nach gespiegeltem Kauf, mit genau dessen "
          "Stueckzahl")
    with Projekt([geschlossener_trade(1)]) as p:
        ib = FakeIB()
        z = spiegel.lauf("volatility_breakout", echt=True,
                          verbindung=verbindung(ib), conn=p.conn, jetzt=IN_SITZUNG)
        check("Ein schon geschlossener, nie gespiegelter Trade loest nichts aus",
              not ib.orders and z["aufgaben"] == 0)
        check("Er wird als uebersprungen mit Grund ausgewiesen",
              len(z["uebersprungen"]) == 1
              and "NICHT nachgekauft" in z["uebersprungen"][0]["grund"])

    with Projekt([offener_trade(1)]) as p:
        os.environ[zugang.STUECK_VARIABLE] = "3"
        try:
            ib = FakeIB()
            spiegel.lauf("volatility_breakout", echt=True,
                          verbindung=verbindung(ib), conn=p.conn, jetzt=IN_SITZUNG)
            conn = sqlite3.connect(p.db)
            conn.execute("UPDATE trades SET status='closed', "
                          "exit_time='2026-09-10', exit_price=210.0, "
                          "result='time_exit', pnl_pct=4.7 WHERE id=1")
            conn.commit()
            conn.close()
            vorher = pruefsumme(p.db)
            z = spiegel.lauf("volatility_breakout", echt=True,
                              verbindung=verbindung(ib), conn=p.conn,
                              jetzt=IN_SITZUNG)
            check("Jetzt wird verkauft", len(ib.orders) == 2
                  and ib.orders[1][1].action == "SELL")
            check("Mit der eigenen Verkaufs-Kennung",
                  ib.orders[1][1].orderRef == "vb-1-v")
            check("Verkauft wird GENAU die gekaufte Stueckzahl - keine Restmenge "
                  "wie bei Krypto",
                  float(ib.orders[1][1].totalQuantity) == 3.0,
                  str(ib.orders[1][1].totalQuantity))
            zeile = [s for s in p.spiegelungen() if s["seite"] == "schliessung"][0]
            check("Die Schliessung ist eigenstaendig vermerkt",
                  zeile["order_id"] and zeile["simulationspreis"] == 210.0)
            check("Die Bot-Datenbank bleibt unveraendert",
                  pruefsumme(p.db) == vorher)
            check("Ein dritter Lauf hat nichts mehr zu tun",
                  spiegel.lauf("volatility_breakout", echt=True,
                                verbindung=verbindung(ib), conn=p.conn,
                                jetzt=IN_SITZUNG)["aufgaben"] == 0
                  and len(ib.orders) == 2)
        finally:
            os.environ.pop(zugang.STUECK_VARIABLE, None)


def test_keine_doppelte_order():
    print("\n9. Doppelte Ausfuehrung: zwei unabhaengige Sperren")
    with Projekt([offener_trade(1)]) as p:
        ib = FakeIB()
        v = verbindung(ib)
        spiegel.lauf("volatility_breakout", echt=True, verbindung=v, conn=p.conn,
                      jetzt=IN_SITZUNG)
        spiegel.lauf("volatility_breakout", echt=True, verbindung=v, conn=p.conn,
                      jetzt=IN_SITZUNG)
        check("Der zweite Lauf sendet gar nichts (Nachverfolgung)",
              len(ib.orders) == 1, str(len(ib.orders)))
        p.conn.execute("DELETE FROM spiegelungen")
        p.conn.commit()
        z = spiegel.lauf("volatility_breakout", echt=True, verbindung=v,
                          conn=p.conn, jetzt=IN_SITZUNG)
        check("Nach verlorenem Eintrag wird die Order am orderRef WIEDERERKANNT",
              len(ib.orders) == 1, f"{len(ib.orders)} Orders")
        check("Und sauber nachgetragen",
              len(p.spiegelungen()) == 1 and z["erfolg"] == 1)
        try:
            p.conn.execute(
                "INSERT INTO spiegelungen (bot, trade_id, seite, symbol, "
                "order_ref, zeitpunkt) VALUES (?,?,?,?,?,?)",
                ("volatility_breakout", 1, "eroeffnung", "AAPL", "x", "jetzt"))
            check("UNIQUE(bot, trade_id, seite) verhindert den zweiten Eintrag",
                  False)
        except sqlite3.IntegrityError:
            check("UNIQUE(bot, trade_id, seite) verhindert den zweiten Eintrag",
                  True)


# ---------------------------------------------------------------------------
# 10. Fehler der Gegenseite
# ---------------------------------------------------------------------------

def test_fehler():
    print("\n10. Fehler: nichts wird stillschweigend verschluckt")
    ib = FakeIB(verbindungsfehler=ConnectionRefusedError(61, "refused"))
    try:
        verbindung(ib)
        check("Keine laufende TWS: verstaendliche Meldung", False)
    except ip.IbkrFehler as fehler:
        check("Keine laufende TWS: verstaendliche Meldung",
              "Laeuft TWS" in str(fehler) and "Enable ActiveX" in str(fehler),
              str(fehler)[:80])

    faelle = [
        ("Broker lehnt die Order ab", {"order_status": "Cancelled"},
         "abgelehnt oder storniert"),
        ("Order bleibt haengen (kein Fill)", {"ohne_fill": True},
         "moeglicherweise"),
        ("placeOrder wirft", {"orderfehler": RuntimeError("Socket weg")},
         "nicht angenommen"),
    ]
    for name, kw, teil in faelle:
        with Projekt([offener_trade(1)]) as p:
            vorher = pruefsumme(p.db)
            ib = FakeIB(**kw)
            z = spiegel.lauf("volatility_breakout", echt=True,
                              verbindung=verbindung(ib), conn=p.conn,
                              jetzt=IN_SITZUNG)
            check(f"{name}: der Lauf meldet einen Fehlschlag",
                  len(z["fehlgeschlagen"]) == 1, str(z)[:90])
            check(f"{name}: mit verstaendlichem Grund",
                  teil in z["fehlgeschlagen"][0]["grund"],
                  z["fehlgeschlagen"][0]["grund"][:110])
            check(f"{name}: KEINE bestaetigte Spiegelung", not p.spiegelungen())
            check(f"{name}: der Fehlversuch steht im Protokoll",
                  any(v["ergebnis"] == "fehlgeschlagen" for v in p.versuche()))
            check(f"{name}: die Bot-Datenbank ist unveraendert",
                  pruefsumme(p.db) == vorher)

    # Eine haengende Order darf beim naechsten Lauf NICHT erneut gesendet werden.
    with Projekt([offener_trade(1)]) as p:
        ib = FakeIB(ohne_fill=True)
        v = verbindung(ib)
        spiegel.lauf("volatility_breakout", echt=True, verbindung=v, conn=p.conn,
                      jetzt=IN_SITZUNG)
        spiegel.lauf("volatility_breakout", echt=True, verbindung=v, conn=p.conn,
                      jetzt=IN_SITZUNG)
        check("Eine haengende Order wird beim naechsten Lauf wiedererkannt, "
              "nicht wiederholt", len(ib.orders) == 1, f"{len(ib.orders)} Orders")
        check("Und sie wird NICHT als bestaetigte Spiegelung eingetragen - sonst "
              "wuerde sich der spaetere Verkauf auf eine Stueckzahl berufen, die "
              "es nie gab", not p.spiegelungen(), str(p.spiegelungen())[:90])
        check("Die Aufgabe bleibt dadurch offen",
              len(spiegel.aufgaben("volatility_breakout", p.conn)["offen"]) == 1)

    # Teilausfall: ein Symbol scheitert, das andere laeuft durch.
    with Projekt([offener_trade(1, "AAPL"), offener_trade(2, "MSFT", 400.0)]) as p:
        class NurMsftKaputt(FakeIB):
            def placeOrder(self, contract, order):
                if contract.symbol == "MSFT":
                    raise RuntimeError("Kontrakt gesperrt")
                return super().placeOrder(contract, order)
        ib = NurMsftKaputt()
        z = spiegel.lauf("volatility_breakout", echt=True,
                          verbindung=verbindung(ib), conn=p.conn, jetzt=IN_SITZUNG)
        check("Ein Fehlschlag bricht die Schleife NICHT ab",
              z["erfolg"] == 1 and len(z["fehlgeschlagen"]) == 1,
              spiegel._meldung(z))
        check("Die gelungene Spiegelung ist vermerkt, die gescheiterte nicht",
              [s["symbol"] for s in p.spiegelungen()] == ["AAPL"],
              str([s["symbol"] for s in p.spiegelungen()]))


# ---------------------------------------------------------------------------
# 11. Nur lesender Zugriff, Notbremse, Grenzen
# ---------------------------------------------------------------------------

def test_nur_lesend_und_grenzen():
    print("\n11. Bot-Datenbank, Notbremse, Grenzen")
    with Projekt([offener_trade(1)]) as p:
        conn = sqlite3.connect(f"file:{p.db}?mode=ro", uri=True)
        try:
            conn.execute("UPDATE trades SET status='closed' WHERE id=1")
            conn.commit()
            check("SQLite verweigert den Schreibversuch im Modus mode=ro", False)
        except sqlite3.OperationalError as fehler:
            check("SQLite verweigert den Schreibversuch im Modus mode=ro",
                  "readonly" in str(fehler).lower(), str(fehler)[:55])
        finally:
            conn.close()
        vorher = pruefsumme(p.db)
        ib = FakeIB()
        spiegel.lauf("volatility_breakout", echt=True, verbindung=verbindung(ib),
                      conn=p.conn, jetzt=IN_SITZUNG)
        spiegel.aufgaben("volatility_breakout", p.conn)
        abgleich.bericht_daten("volatility_breakout", conn=p.conn)
        check("Nach Lauf, Statusabfrage und Abgleich: Datenbank byteweise gleich",
              pruefsumme(p.db) == vorher)
        check("Die Nachverfolgung liegt in einer EIGENEN Datei",
              os.path.basename(spiegel.spiegel_db_pfad("volatility_breakout"))
              == "broker_ibkr_volatility_breakout.db")
        namen = sorted(z[0] for z in sqlite3.connect(p.db).execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%'"))
        check("Im Schema des Bots ist keine neue Tabelle entstanden",
              namen == ["trades"], str(namen))

    with Projekt([offener_trade(1)]) as p:
        open(zugang.NOTBREMSE_DATEI, "w").write("aus\n")
        ib = FakeIB()
        z = spiegel.lauf("volatility_breakout", echt=True,
                          verbindung=verbindung(ib), conn=p.conn, jetzt=IN_SITZUNG)
        check("Mit broker/STOP_IBKR wird keine Order gesendet", not ib.orders)
        check("Und der Grund steht im Ergebnis",
              "NOTBREMSE" in z["fehlgeschlagen"][0]["grund"])
        os.remove(zugang.NOTBREMSE_DATEI)
        z = spiegel.lauf("volatility_breakout", echt=True,
                          verbindung=verbindung(ib), conn=p.conn, jetzt=IN_SITZUNG)
        check("Nach dem Entfernen laeuft es wieder",
              len(ib.orders) == 1 and z["erfolg"] == 1)

    with Projekt([offener_trade(1)]) as p:
        for wert, teil in (("0", "groesser als 0"),
                            (str(zugang.STUECK_MAX + 1), "Obergrenze"),
                            ("viele", "ganze Zahl")):
            os.environ[zugang.STUECK_VARIABLE] = wert
            try:
                zugang.stueck()
                check(f"Stueckzahl {wert!r} wird abgelehnt", False)
            except zugang.ZugangFehler as fehler:
                check(f"Stueckzahl {wert!r} wird abgelehnt", teil in str(fehler),
                      str(fehler)[:60])
            finally:
                os.environ.pop(zugang.STUECK_VARIABLE)

    trades = [offener_trade(i, "AAPL" if i % 2 else "MSFT",
                            200.0 if i % 2 else 400.0)
              for i in range(1, zugang.MAX_ORDERS_PRO_LAUF + 3)]
    with Projekt(trades) as p:
        ib = FakeIB()
        v = verbindung(ib)
        spiegel.lauf("volatility_breakout", echt=True, verbindung=v, conn=p.conn,
                      jetzt=IN_SITZUNG)
        check(f"Hoechstens {zugang.MAX_ORDERS_PRO_LAUF} Orders je Lauf",
              len(ib.orders) == zugang.MAX_ORDERS_PRO_LAUF,
              f"{len(ib.orders)} von {len(trades)} Aufgaben")
        alt = zugang.MAX_ORDERS_PRO_TAG
        zugang.MAX_ORDERS_PRO_TAG = 1
        try:
            spiegel.lauf("volatility_breakout", echt=True, verbindung=v,
                          conn=p.conn, jetzt=IN_SITZUNG)
            check("Die Tagesgrenze blockiert den ganzen Lauf", False)
        except spiegel.SpiegelFehler as fehler:
            check("Die Tagesgrenze blockiert den ganzen Lauf",
                  "Tagesgrenze" in str(fehler), str(fehler)[:60])
        finally:
            zugang.MAX_ORDERS_PRO_TAG = alt

    check("Nicht freigeschaltete Bots werden abgelehnt",
          _abgelehnt(lambda: spiegel.lauf("turtle_soup_stocks", echt=False)))
    # VERHALTEN, nicht Quelltext: ohne erwartetes Konto darf ein echter Lauf
    # nicht einmal verbinden. (Die erste Fassung dieser Pruefung suchte den
    # Variablennamen im Quelltext - der steht dort als Konstante und nicht als
    # Zeichenkette, die Pruefung war also von Anfang an rot, ohne etwas ueber
    # das Verhalten zu sagen.)
    with Projekt([offener_trade(1)]) as p:
        try:
            spiegel.lauf("volatility_breakout", echt=True, conn=p.conn,
                          jetzt=IN_SITZUNG)
            check("Fuer echte Orders ist das Konto in der .env Pflicht", False)
        except spiegel.SpiegelFehler as fehler:
            check("Fuer echte Orders ist das Konto in der .env Pflicht",
                  zugang.KONTO_VARIABLE in str(fehler)
                  and "nichts gesendet" in str(fehler), str(fehler)[:80])
        check("Der Trockenlauf braucht es nicht - er verbindet nur lesend",
              "nur_lesen=not echt" in inspect.getsource(spiegel.lauf))
    check("Die Stueckzahl wird gegen minSize/sizeIncrement geprueft",
          _abgelehnt_ibkr(lambda: ip.pruefe_stueckzahl(
              1, FakeDetails(FakeContract("AAPL"), min_size=5.0)))
          and _abgelehnt_ibkr(lambda: ip.pruefe_stueckzahl(
              3, FakeDetails(FakeContract("AAPL"), schritt=2.0))))


def _abgelehnt(aufruf) -> bool:
    try:
        aufruf()
        return False
    except (spiegel.SpiegelFehler, zugang.ZugangFehler, ip.IbkrFehler):
        return True


def _abgelehnt_ibkr(aufruf) -> bool:
    try:
        aufruf()
        return False
    except ip.IbkrFehler:
        return True


# ---------------------------------------------------------------------------
# 12. Abgleich
# ---------------------------------------------------------------------------

def test_abgleich():
    print("\n12. Abgleich: Simulation gegen tatsaechliche Ausfuehrung")
    with Projekt([offener_trade(1, "AAPL", 200.0, "2026-09-09")]) as p:
        ib = FakeIB()
        v = verbindung(ib)
        spiegel.lauf("volatility_breakout", echt=True, verbindung=v, conn=p.conn,
                      jetzt=IN_SITZUNG)
        conn = sqlite3.connect(p.db)
        conn.execute("UPDATE trades SET status='closed', exit_time='2026-09-10', "
                      "exit_price=210.0, result='time_exit', pnl_pct=4.70 "
                      "WHERE id=1")
        conn.commit()
        conn.close()
        ib.kurse["AAPL"] = 210.0
        spiegel.lauf("volatility_breakout", echt=True, verbindung=v, conn=p.conn,
                      jetzt=IN_SITZUNG)

        d = abgleich.bericht_daten("volatility_breakout", conn=p.conn)
        check("Die Kostenannahme kommt aus dem echten forward_test.py (0.30 pp)",
              abs(d["kostenannahme_pp"] - 0.30) < 1e-9, str(d["kostenannahme_pp"]))
        z = d["zeilen"][0]
        check("Eine vollstaendige Zeile", d["anzahl_vollstaendig"] == 1)
        # 1 Stueck zu 200.00 plus 1.00 USD Provision -> effektiv 201.00
        # Verkauf 1 Stueck zu 210.00 minus 1.00 -> effektiv 209.00
        # je Stueck: (209 - 201) / 201 = +3.980 %
        check("Effektiver Einstieg 201.00 (Kurs plus Provision je Stueck)",
              abs(z["einstieg_effektiv"] - 201.0) < 1e-6,
              str(z["einstieg_effektiv"]))
        check("Effektiver Ausstieg 209.00 (Kurs minus Provision je Stueck)",
              abs(z["ausstieg_effektiv"] - 209.0) < 1e-6,
              str(z["ausstieg_effektiv"]))
        check("PnL der Ausfuehrung +3.98 %",
              abs(z["pnl_ausfuehrung_pct"] - 3.9801) < 0.01,
              f"{z['pnl_ausfuehrung_pct']:.4f}")
        check("PnL der Simulation unveraendert daneben (+4.70 %)",
              z["pnl_simulation_pct"] == 4.70)
        check("Der Unterschied ist die eigentliche Zahl (-0.72 pp)",
              abs(z["unterschied_pp"] + 0.7199) < 0.01,
              f"{z['unterschied_pp']:+.4f}")
        check("Der VERZUG zwischen Entscheidung und Ausfuehrung wird ausgewiesen",
              z["einstieg_verzug_tage"] is not None
              and z["einstieg_verzug_tage"] >= 1,
              str(z["einstieg_verzug_tage"]))
        check("Das Konto steht im Bericht", z["konto"] == KONTO)
        text = abgleich.als_text(d)
        for teil in ("ABGLEICH Simulation", "Verzug", "Uebernacht-Luecke",
                      "Methodik-Grundsatz 2", "Restmenge", KONTO):
            check(f"Der Bericht nennt {teil!r}", teil in text)

    with Projekt([geschlossener_trade(1)]) as p:
        ib = FakeIB()
        spiegel.lauf("volatility_breakout", echt=False, verbindung=verbindung(ib),
                      conn=p.conn, jetzt=IN_SITZUNG)
        d = abgleich.bericht_daten("volatility_breakout", conn=p.conn)
        check("Nicht gespiegelte Trades stehen im Bericht, mit Grund",
              len(d["nicht_gespiegelt"]) == 1
              and "NICHT nachgekauft" in d["nicht_gespiegelt"][0]["grund"])
        check("Und tauchen im Text auf", "NICHT gespiegelt" in abgleich.als_text(d))


# ---------------------------------------------------------------------------
# 13. Gegen die ECHTE Bibliothek (wird uebersprungen, wenn sie fehlt)
# ---------------------------------------------------------------------------

def test_gegen_echte_bibliothek():
    print("\n13. Passt die Annahme noch zur echten ib_async-Schnittstelle?")
    try:
        import ib_async
        from ib_async import IB, Stock, MarketOrder
        from ib_async.contract import ContractDetails
        from ib_async.objects import Execution, CommissionReport
        from ib_async.order import Order, Trade, OrderStatus
    except ImportError:
        UEBERSPRUNGEN.append("test_gegen_echte_bibliothek")
        print("  [uebersprungen] ib_async ist hier nicht installiert - dass die "
              "Schnittstelle\n                  noch passt, bleibt ungeprueft "
              "(pip3 install ib_async)")
        return

    print(f"  ib_async {getattr(ib_async, '__version__', '?')}")
    verbinden = inspect.signature(IB.connect).parameters
    for name in ("host", "port", "clientId", "timeout", "readonly"):
        check(f"IB.connect kennt {name!r}", name in verbinden)
    import dataclasses
    order_felder = {f.name for f in dataclasses.fields(Order)}
    for name in ("orderRef", "account", "tif", "outsideRth", "totalQuantity"):
        check(f"Order kennt {name!r}", name in order_felder)
    details_felder = {f.name for f in dataclasses.fields(ContractDetails)}
    for name in ("liquidHours", "tradingHours", "timeZoneId", "minSize",
                  "sizeIncrement"):
        check(f"ContractDetails kennt {name!r}", name in details_felder)
    ausf_felder = {f.name for f in dataclasses.fields(Execution)}
    for name in ("orderRef", "shares", "price"):
        check(f"Execution kennt {name!r}", name in ausf_felder)
    prov_felder = {f.name for f in dataclasses.fields(CommissionReport)}
    for name in ("commission", "currency"):
        check(f"CommissionReport kennt {name!r}", name in prov_felder)
    for name in ("managedAccounts", "reqContractDetails", "placeOrder", "fills",
                  "trades", "waitOnUpdate", "disconnect"):
        check(f"IB hat {name}()", callable(getattr(IB, name, None)))
    check("Trade hat isDone()", callable(getattr(Trade, "isDone", None)))
    check("Filled gilt als Endzustand",
          "Filled" in getattr(OrderStatus, "DoneStates", set()))

    # Und die Order, die diese Bruecke wirklich bauen wuerde.
    order = ip._marktorder.__wrapped__("BUY", 1, "vb-1-k", KONTO) \
        if hasattr(ip._marktorder, "__wrapped__") else None
    echt = ip._marktorder("BUY", 2, "vb-9-k", KONTO)
    check("Die echte Order traegt orderRef, Konto, tif=DAY, outsideRth=False",
          (echt.orderRef, echt.account, echt.tif, echt.outsideRth)
          == ("vb-9-k", KONTO, "DAY", False),
          f"{echt.orderRef}/{echt.account}/{echt.tif}/{echt.outsideRth}")
    check("Und ist eine MARKET-Order ueber die gewuenschte Stueckzahl",
          echt.orderType == "MKT" and float(echt.totalQuantity) == 2.0,
          f"{echt.orderType}/{echt.totalQuantity}")
    aktie = ip._aktie("BRK-B")
    check("Der echte Kontrakt traegt das uebersetzte Kuerzel und SMART/USD",
          (aktie.symbol, aktie.exchange, aktie.currency) == ("BRK B", "SMART", "USD"),
          f"{aktie.symbol}/{aktie.exchange}/{aktie.currency}")


# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("Selbsttests der IBKR-Paper-Bruecke")
    print("=" * 78)
    tests = [test_port_wache, test_konto_wache, test_struktur, test_symbole,
             test_handelszeiten, test_trockenlauf, test_eroeffnung,
             test_schliessung, test_keine_doppelte_order, test_fehler,
             test_nur_lesend_und_grenzen, test_abgleich,
             test_gegen_echte_bibliothek]
    for test in tests:
        try:
            test()
        except Exception as fehler:                      # noqa: BLE001
            import traceback
            FEHLER.append(f"{test.__name__} (Ausnahme)")
            print(f"  [FEHLER] {test.__name__} warf eine Ausnahme: {fehler}")
            traceback.print_exc()
    print("\n" + "=" * 78)
    if UEBERSPRUNGEN:
        print("UEBERSPRUNGEN:", ", ".join(UEBERSPRUNGEN))
    print(f"{sum(BESTANDEN)} von {len(BESTANDEN)} Pruefungen bestanden, "
          f"{len(FEHLER)} fehlgeschlagen.")
    for name in FEHLER:
        print(f"  - {name}")
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())

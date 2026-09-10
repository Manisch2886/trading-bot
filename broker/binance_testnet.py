"""
Der einzige Weg nach draussen: signierte Aufrufe gegen das Binance SPOT-TESTNET
==============================================================================
Dieses Modul spricht mit genau EINEM Host. Es kennt keine Strategie, keine
Datenbank und keinen Trade - es uebersetzt "kaufe X von SYMBOL" in einen
signierten HTTP-Aufruf und gibt die Antwort zurueck. Die Entscheidung, WAS
gekauft wird, liegt in spiegel.py.

------------------------------------------------------------------------------
WARUM KEIN python-binance, OBWOHL DIE BOTS ES BENUTZEN
------------------------------------------------------------------------------
Die Bots verwenden `binance.client.Client` fuer KURSDATEN. Fuer den
Schreibweg waere dieselbe Bibliothek die naheliegende Wahl - sie hat sogar
einen `testnet=True`-Schalter. Genau der ist das Problem: welcher Endpunkt
angesprochen wird, haengt dann an einem Laufzeit-Argument irgendwo im
Aufrufpfad. Ein vergessenes oder falsch durchgereichtes Flag laeuft gegen den
echten Handel, und zwar lautlos.

Hier ist der Host eine Konstante in zugang.py, und jede einzelne Anfrage
laeuft durch `pruefe_url()`. Der Preis dafuer sind ungefaehr vierzig Zeilen
HMAC-Signatur und urllib - nur die Standardbibliothek, kein zusaetzliches
Paket, und eine Stelle, an der ein Test die Leitung kappen kann.

------------------------------------------------------------------------------
WARUM DER HOST GEPARST WIRD UND NICHT NUR DER ANFANG VERGLICHEN
------------------------------------------------------------------------------
Ein `url.startswith("https://testnet.binance.vision")` sieht sicher aus und ist
es nicht:

    https://testnet.binance.vision.angreifer.example/api/v3/order

beginnt mit genau dieser Zeichenkette. Geprueft wird deshalb der geparste
HOSTNAME auf Gleichheit, dazu Schema, Port und Pfad-Praefix. Derselbe Grund
deckt auch die Variante mit Benutzerangabe ab
(`https://testnet.binance.vision@angreifer.example/...`), bei der der
tatsaechliche Host hinter dem @ steht.

------------------------------------------------------------------------------
DAS GEHEIMNIS VERLAESST DEN PROZESS NICHT
------------------------------------------------------------------------------
Der API-Key geht als Kopfzeile `X-MBX-APIKEY` mit, das Secret NIE - es
signiert nur lokal. Keine Fehlermeldung und kein Protokolleintrag dieses
Moduls enthaelt Key oder Secret; `_fehlertext()` kuerzt Antworten und ein Test
prueft, dass in keiner gesendeten URL, Kopfzeile oder Meldung das Secret
auftaucht.
"""

import hashlib
import hmac
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

_BROKER_DIR = os.path.dirname(os.path.abspath(__file__))
if _BROKER_DIR not in sys.path:
    sys.path.insert(0, _BROKER_DIR)

import zugang   # noqa: E402

ZEITFENSTER_MS = 5000          # recvWindow: Binance verwirft aeltere Anfragen
ZEITLIMIT_SEKUNDEN = 20


class TestnetFehler(Exception):
    """Jeder Abbruch auf dem Weg nach draussen - Netz, HTTP-Status oder eine
    Fehlerantwort von Binance. `code` ist der Binance-Fehlercode, falls es
    einen gab (z. B. -2008), sonst None."""

    def __init__(self, meldung, code=None):
        super().__init__(meldung)
        self.code = code


def pruefe_url(url: str) -> str:
    """Gibt die URL zurueck, wenn sie zum Testnet gehoert - wirft sonst.
    Wird von JEDER Anfrage aufgerufen, nicht einmal beim Start."""
    teile = urllib.parse.urlsplit(url)
    if teile.scheme != "https":
        raise TestnetFehler(f"Nur https erlaubt, nicht {teile.scheme!r}: {url}")
    host = (teile.hostname or "").lower()
    if host in zugang.VERBOTENE_HOSTS:
        raise TestnetFehler(
            f"ABGEBROCHEN: {host} ist kein Testnet-Host. Diese Bruecke darf "
            f"ausschliesslich {zugang.TESTNET_HOST} ansprechen; es wurde nichts "
            f"gesendet.")
    if host != zugang.TESTNET_HOST:
        raise TestnetFehler(
            f"ABGEBROCHEN: unerwarteter Host {host!r}. Erlaubt ist genau "
            f"{zugang.TESTNET_HOST!r} - geprueft wird der geparste Hostname, "
            f"nicht der Anfang der Zeichenkette. Es wurde nichts gesendet.")
    if teile.port not in (None, 443):
        raise TestnetFehler(f"Unerwarteter Port {teile.port} in {url}")
    if not teile.path.startswith(zugang.TESTNET_PFAD_PRAEFIX):
        raise TestnetFehler(
            f"Unerwarteter Pfad {teile.path!r} - erwartet wird "
            f"{zugang.TESTNET_PFAD_PRAEFIX}...")
    return url


def _http_sender(methode: str, url: str, kopf: dict):
    """Der tatsaechliche Netzaufruf. Einzige Stelle mit urllib; die Tests
    ersetzen genau diese Funktion und kommen deshalb ohne Netz aus."""
    anfrage = urllib.request.Request(url, method=methode, headers=kopf)
    try:
        with urllib.request.urlopen(anfrage, timeout=ZEITLIMIT_SEKUNDEN) as antwort:
            return antwort.status, antwort.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as fehler:
        # Binance schickt seine Fehlercodes MIT Status 4xx - der Rumpf ist die
        # eigentliche Information und darf nicht verloren gehen.
        return fehler.code, fehler.read().decode("utf-8", "replace")
    except urllib.error.URLError as fehler:
        raise TestnetFehler(f"Testnet nicht erreichbar: {fehler.reason}")
    except TimeoutError:
        raise TestnetFehler(
            f"Testnet hat innerhalb von {ZEITLIMIT_SEKUNDEN} s nicht geantwortet")


def _fehlertext(text: str, grenze: int = 300) -> str:
    text = (text or "").strip().replace("\n", " ")
    return text if len(text) <= grenze else text[:grenze] + " ..."


class Testnet:
    """Ein Zugang zum Testnet. `sender` ist die Leitung nach draussen und
    existiert als Parameter, damit die Tests sie ersetzen koennen - ohne
    Attrappe eines ganzen HTTP-Stapels und ohne einen einzigen echten Aufruf."""

    def __init__(self, key: str = None, secret: str = None, sender=None):
        self.key = key
        self.secret = secret
        self.sender = sender or _http_sender
        self.zeitversatz_ms = 0
        self.gesendete_urls = []      # nur zur Diagnose/Pruefung, ohne Secret

    # --- Grundlagen -------------------------------------------------------
    def _url(self, pfad: str, abfrage: str = "") -> str:
        url = zugang.TESTNET_BASIS + pfad + (f"?{abfrage}" if abfrage else "")
        return pruefe_url(url)

    def _anfrage(self, methode: str, pfad: str, parameter: dict = None,
                  signiert: bool = False):
        parameter = dict(parameter or {})
        kopf = {"Accept": "application/json",
                "User-Agent": "trading-bot-testnet-bruecke/1.0"}
        if signiert:
            if not self.key or not self.secret:
                raise TestnetFehler(
                    f"Fuer diesen Aufruf braucht es Zugangsdaten "
                    f"({zugang.SCHLUESSEL_VARIABLE}/{zugang.GEHEIMNIS_VARIABLE} "
                    f"in der .env). Es wurde nichts gesendet.")
            parameter["timestamp"] = int(time.time() * 1000) + self.zeitversatz_ms
            parameter["recvWindow"] = ZEITFENSTER_MS
            abfrage = urllib.parse.urlencode(parameter)
            unterschrift = hmac.new(self.secret.encode(), abfrage.encode(),
                                     hashlib.sha256).hexdigest()
            abfrage = f"{abfrage}&signature={unterschrift}"
            kopf["X-MBX-APIKEY"] = self.key
        else:
            abfrage = urllib.parse.urlencode(parameter)

        url = self._url(pfad, abfrage)
        self.gesendete_urls.append(url)
        status, text = self.sender(methode, url, kopf)
        return self._auswerten(status, text, pfad)

    def _auswerten(self, status, text, pfad):
        try:
            daten = json.loads(text) if text else {}
        except ValueError:
            raise TestnetFehler(
                f"Antwort auf {pfad} war kein JSON (HTTP {status}): "
                f"{_fehlertext(text)}")
        if status == 200:
            return daten
        code = daten.get("code") if isinstance(daten, dict) else None
        meldung = daten.get("msg") if isinstance(daten, dict) else None
        raise TestnetFehler(
            f"Testnet lehnt {pfad} ab (HTTP {status}, Code {code}): "
            f"{_fehlertext(meldung or text)}{_hinweis_zu(code)}", code=code)

    # --- Oeffentliche Aufrufe --------------------------------------------
    def ping(self):
        """Erreichbarkeit, ohne Zugangsdaten und ohne jede Wirkung."""
        return self._anfrage("GET", "/api/v3/ping")

    def serverzeit(self) -> int:
        return int(self._anfrage("GET", "/api/v3/time")["serverTime"])

    def zeit_abgleichen(self) -> int:
        """Merkt sich den Versatz zur Serverzeit. Ohne das scheitern
        signierte Aufrufe auf einer Maschine mit schiefer Uhr mit Code -1021,
        und zwar mit einer Meldung, die niemand von sich aus versteht."""
        lokal = int(time.time() * 1000)
        self.zeitversatz_ms = self.serverzeit() - lokal
        return self.zeitversatz_ms

    def konto(self):
        """Signiert, aber reiner LESEZUGRIFF - der richtige erste Schritt:
        er beweist, dass die Schluessel stimmen, ohne etwas zu handeln."""
        return self._anfrage("GET", "/api/v3/account", signiert=True)

    def preis(self, symbol: str) -> float:
        daten = self._anfrage("GET", "/api/v3/ticker/price", {"symbol": symbol})
        return float(daten["price"])

    def symbol_regeln(self, symbol: str) -> dict:
        """Schrittweite, Mindestmenge und Mindestgegenwert dieses Symbols -
        aus der Boerse gelesen, nicht geraten. Ohne diese Werte wird jede
        zweite Order mit "LOT_SIZE" oder "NOTIONAL" abgelehnt."""
        daten = self._anfrage("GET", "/api/v3/exchangeInfo", {"symbol": symbol})
        liste = daten.get("symbols") or []
        if not liste:
            raise TestnetFehler(f"Das Testnet kennt das Symbol {symbol} nicht.")
        eintrag = liste[0]
        regeln = {"symbol": eintrag["symbol"], "basis": eintrag["baseAsset"],
                  "quote": eintrag["quoteAsset"], "status": eintrag.get("status"),
                  "schritt": None, "min_menge": None, "min_gegenwert": None}
        for f in eintrag.get("filters", []):
            if f["filterType"] == "LOT_SIZE":
                regeln["schritt"] = float(f["stepSize"])
                regeln["min_menge"] = float(f["minQty"])
            elif f["filterType"] in ("NOTIONAL", "MIN_NOTIONAL"):
                wert = f.get("minNotional")
                if wert is not None:
                    regeln["min_gegenwert"] = float(wert)
        return regeln

    def order_nach_client_id(self, symbol: str, client_order_id: str):
        """Eine frueher gesendete Order anhand UNSERER eigenen Kennung finden.
        Das ist die Absicherung gegen den haesslichsten Fall: Order ist
        draussen, die Antwort kam nicht an (Abbruch, Zeitueberschreitung). Beim
        naechsten Lauf wird sie so erkannt, statt ein zweites Mal zu kaufen.
        Gibt None zurueck, wenn es sie nicht gibt."""
        try:
            return self._anfrage("GET", "/api/v3/order",
                                  {"symbol": symbol,
                                   "origClientOrderId": client_order_id},
                                  signiert=True)
        except TestnetFehler as fehler:
            if fehler.code == -2013:      # "Order does not exist."
                return None
            raise

    def marktorder(self, symbol: str, seite: str, menge: str,
                    client_order_id: str):
        """EINE Market-Order. `menge` ist eine Zeichenkette, weil die
        Schrittweite sonst in der Gleitkomma-Darstellung verloren geht
        (0.001 * 3 ist nicht 0.003) und Binance die Order mit LOT_SIZE
        ablehnen wuerde.

        newOrderRespType=FULL, damit die Antwort die TEILAUSFUEHRUNGEN
        enthaelt - ohne sie liesse sich weder der tatsaechliche
        Ausfuehrungspreis noch die Gebuehr bestimmen, und genau die sind der
        Erkenntnisgewinn dieser Aufgabe.
        """
        if seite not in ("BUY", "SELL"):
            raise TestnetFehler(f"Unbekannte Seite {seite!r}")
        if zugang.notbremse_aktiv():
            raise TestnetFehler(
                f"NOTBREMSE aktiv ({zugang.NOTBREMSE_DATEI} existiert) - es "
                f"wurde nichts gesendet.")
        return self._anfrage("POST", "/api/v3/order", {
            "symbol": symbol, "side": seite, "type": "MARKET",
            "quantity": menge, "newClientOrderId": client_order_id,
            "newOrderRespType": "FULL",
        }, signiert=True)


def _hinweis_zu(code) -> str:
    """Zu den drei Fehlern, die beim ersten Einrichten praktisch immer
    auftreten, gehoert die Ursache direkt in die Meldung - sonst sucht der
    Nutzer an der falschen Stelle."""
    if code in (-2008, -2014, -2015):
        return (" | Hinweis: der Schluessel wird vom Testnet nicht anerkannt. "
                "Er muss auf testnet.binance.vision erzeugt sein - Schluessel "
                "aus dem echten Binance-Konto (auch die aus 'Demo Trading') "
                "funktionieren dort NICHT. Siehe broker/README.md.")
    if code == -1022:
        return (" | Hinweis: Signatur abgelehnt. Meist ist das Secret "
                "unvollstaendig aus der .env gelesen (Leerzeichen, Zeilenumbruch) "
                "oder Key und Secret sind vertauscht.")
    if code == -1021:
        return (" | Hinweis: Zeitstempel ausserhalb des Fensters. Die Uhr des "
                "Rechners weicht zu stark ab; zeit_abgleichen() vor dem Aufruf "
                "loest das, sonst die Systemzeit synchronisieren.")
    if code == -1013:
        return (" | Hinweis: die Order verstoesst gegen einen Boersenfilter "
                "(Schrittweite, Mindestmenge oder Mindestgegenwert).")
    if code == -2010:
        return (" | Hinweis: Guthaben reicht nicht. Im Testnet gibt es die "
                "virtuellen Bestaende je Konto - notfalls neues Konto anlegen.")
    return ""


def menge_zu_text(menge: float, schritt: float) -> str:
    """Eine Menge so formatieren, wie die Boerse sie erwartet: abgerundet auf
    die Schrittweite, mit genau so vielen Nachkommastellen wie diese hat, ohne
    Exponentialschreibweise.

    ABGERUNDET, nie auf- oder kaufmaennisch gerundet: aufrunden hiesse mehr zu
    kaufen als gewollt, und beim Verkauf mehr anzubieten als vorhanden ist -
    was die Order mit "insufficient balance" abreissen liesse."""
    if schritt <= 0:
        raise TestnetFehler(f"Unbrauchbare Schrittweite {schritt!r}")
    schritte = int(menge / schritt + 1e-9)
    stellen = max(0, -int(round(_log10(schritt)))) if schritt < 1 else 0
    wert = schritte * schritt
    text = f"{wert:.{stellen}f}"
    return text


def _log10(wert: float) -> float:
    import math
    return math.log10(wert)


def menge_fuer_betrag(betrag_usdt: float, preis: float, regeln: dict) -> str:
    """Aus Gegenwert und Kurs die Menge bestimmen, die die Boersenfilter
    einhaelt - oder verstaendlich abbrechen. Wirft, statt eine Order zu
    schicken, die sicher abgelehnt wird."""
    if preis <= 0:
        raise TestnetFehler(f"Unbrauchbarer Kurs {preis!r}")
    if not regeln.get("schritt"):
        raise TestnetFehler(
            f"Keine Schrittweite (LOT_SIZE) fuer {regeln.get('symbol')} - ohne "
            f"sie wird nicht gehandelt.")
    text = menge_zu_text(betrag_usdt / preis, regeln["schritt"])
    menge = float(text)
    if menge <= 0:
        raise TestnetFehler(
            f"Aus {betrag_usdt:g} USDT ergibt sich bei Kurs {preis:g} und "
            f"Schrittweite {regeln['schritt']:g} keine handelbare Menge.")
    if regeln.get("min_menge") and menge < regeln["min_menge"]:
        raise TestnetFehler(
            f"Menge {text} liegt unter der Mindestmenge "
            f"{regeln['min_menge']:g} fuer {regeln['symbol']}.")
    gegenwert = menge * preis
    if regeln.get("min_gegenwert") and gegenwert < regeln["min_gegenwert"]:
        raise TestnetFehler(
            f"Gegenwert {gegenwert:.2f} USDT liegt unter dem Mindestgegenwert "
            f"{regeln['min_gegenwert']:g} fuer {regeln['symbol']} - "
            f"{zugang.BETRAG_VARIABLE} in der .env erhoehen.")
    return text


def ausfuehrung_auswerten(antwort: dict, basis_asset: str) -> dict:
    """Aus einer Order-Antwort (newOrderRespType=FULL) die drei Zahlen holen,
    auf die es ankommt:

      menge_brutto   ausgefuehrte Menge laut Boerse
      preis          MENGENGEWICHTETER Ausfuehrungspreis ueber alle
                     Teilausfuehrungen - nicht der Preis der ersten, und nicht
                     der angefragte: eine Market-Order im Testnet wird
                     regelmaessig in mehreren Stuecken zu verschiedenen Kursen
                     gefuellt, und genau diese Abweichung soll der Abgleich
                     spaeter zeigen
      menge_netto    was davon WIRKLICH im Bestand landet, also brutto minus
                     der Gebuehren, die in der gekauften Waehrung abgerechnet
                     wurden. Beim spaeteren Verkauf darf nur diese Menge
                     angeboten werden, sonst scheitert er an "insufficient
                     balance" - ein Fehler, der ohne diese Zeile erst Wochen
                     spaeter beim ersten Verkauf auffaellt.
    """
    fills = antwort.get("fills") or []
    menge_brutto = float(antwort.get("executedQty") or 0)
    quote_menge = float(antwort.get("cummulativeQuoteQty") or 0)
    gebuehr_basis = 0.0
    gebuehren = {}
    for fill in fills:
        betrag = float(fill.get("commission") or 0)
        waehrung = fill.get("commissionAsset") or "?"
        gebuehren[waehrung] = gebuehren.get(waehrung, 0.0) + betrag
        if waehrung == basis_asset:
            gebuehr_basis += betrag
    if menge_brutto and quote_menge:
        preis = quote_menge / menge_brutto
    elif fills:
        summe = sum(float(f["price"]) * float(f["qty"]) for f in fills)
        menge = sum(float(f["qty"]) for f in fills)
        preis = summe / menge if menge else None
    else:
        preis = None
    return {
        "order_id": str(antwort.get("orderId")),
        "client_order_id": antwort.get("clientOrderId"),
        "status": antwort.get("status"),
        "menge_brutto": menge_brutto,
        "menge_netto": max(0.0, menge_brutto - gebuehr_basis),
        "quote_menge": quote_menge,
        "preis": preis,
        "gebuehren": gebuehren,
        "anzahl_teilausfuehrungen": len(fills),
    }

"""
Der einzige Weg zum Broker: lokale Verbindung zu TWS / IB Gateway (Paper)
==============================================================================
Dieses Modul kennt keine Strategie und keine Datenbank. Es verbindet sich mit
der lokal laufenden IBKR-Software, prueft die beiden Absicherungen aus
ibkr_zugang.py (Port UND Konto), loest ein Boersenkuerzel in genau einen
Kontrakt auf, beantwortet die Frage "ist jetzt Handelszeit" aus den Angaben der
Boerse selbst und schickt genau eine Market-Order.

------------------------------------------------------------------------------
WARUM ib_async UND NICHT ibapi - UND WARUM HIER EINE FREMDBIBLIOTHEK IN ORDNUNG IST
------------------------------------------------------------------------------
Bei der Binance-Bruecke war die Entscheidung umgekehrt: dort wurde
python-binance ABGELEHNT, weil dessen `testnet=True` die Sicherheitseigenschaft
selbst gewesen waere - ein Laufzeit-Flag irgendwo im Aufrufpfad. Hier ist das
anders. Die Sicherheitseigenschaften (Paper-Port, Paper-Konto) liegen in
UNSEREM Code und werden von UNS geprueft; die Bibliothek transportiert nur
Bytes ueber einen Socket.

Und dieser Socket ist kein REST-Aufruf, den man in vierzig Zeilen nachbaut: das
TWS-Protokoll ist ein laengenpraefigiertes Feldprotokoll mit
Versionsverhandlung. Es von Hand zu implementieren waere hier nicht sorgfaeltig,
sondern leichtsinnig.

Gewaehlt ist `ib_async` (Version 2.1.0, Dezember 2025), nicht das offizielle
`ibapi`:

  * `ibapi` liegt auf PyPI nur als fremde Altlast von 2020 (9.81.1.post1) -
    die offizielle Fassung kommt als ZIP-Download von IBKR und wird per
    setup.py installiert. Fuer einen Cronjob auf einem Mac ist das ein
    zusaetzlicher Handgriff, der bei jedem Update wiederkommt.
  * `ib_insync`, lange der Standard, wird nicht mehr gepflegt (der Autor ist
    verstorben). IBKRs EIGENE Dokumentation verweist als Nachfolger auf
    `ib_async` - das ist keine Community-Einschaetzung, sondern die des
    Brokers.
  * `ib_async` ist per pip installierbar, aktuell gepflegt und bietet die
    synchrone Bequemlichkeitsschicht, die eine Bruecke mit vier Aufrufen
    braucht - `ibapi` verlangt dafuer eine EWrapper/EClient-Rueckrufschleife
    mit eigenem Thread.

Die Bibliothek wird ERST BEIM VERBINDEN importiert (siehe `_ib_klasse()`).
Dadurch laufen die Selbsttests und der `--status`-Aufruf auf einem Rechner
ohne ib_async, und ein fehlendes Paket ist eine verstaendliche Meldung statt
eines ImportError beim Start. Dieselbe Stelle ist der Punkt, an dem die Tests
eine Attrappe einsetzen - die Verbindung ist ein Parameter, kein Schicksal.
"""

import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

_BROKER_DIR = os.path.dirname(os.path.abspath(__file__))
if _BROKER_DIR not in sys.path:
    sys.path.insert(0, _BROKER_DIR)

import ibkr_zugang as zugang        # noqa: E402

ZEITLIMIT_VERBINDUNG = 15          # Sekunden
ZEITLIMIT_AUSFUEHRUNG = 60         # Sekunden, bis eine Order als haengend gilt
MARKTDATEN_VERZOEGERT = 3          # reqMarketDataType: 3 = verzoegert


class IbkrFehler(Exception):
    """Jeder Abbruch auf dem Weg zum Broker. `code` ist der IBKR-Fehlercode,
    falls einer gemeldet wurde."""

    def __init__(self, meldung, code=None):
        super().__init__(meldung)
        self.code = code


def _ib_klasse():
    """Der einzige Import von ib_async im ganzen Projekt."""
    try:
        from ib_async import IB          # noqa: PLC0415 - absichtlich spaet
        return IB
    except ImportError as fehler:
        raise IbkrFehler(
            f"Die Bibliothek ib_async fehlt ({fehler}). Installieren mit "
            f"'pip3 install ib_async' (Python 3.10 oder neuer). Ohne sie "
            f"funktionieren Trockenlauf und --status, aber keine Order.")


def _aktie(symbol: str):
    """Kontrakt-Objekt fuer eine US-Aktie. Auch das erst bei Bedarf."""
    try:
        from ib_async import Stock       # noqa: PLC0415
    except ImportError as fehler:
        raise IbkrFehler(f"ib_async fehlt ({fehler}).")
    return Stock(zugang.ibkr_symbol(symbol), zugang.BOERSE, zugang.WAEHRUNG)


def _marktorder(seite: str, stueck: int, order_ref: str, konto: str):
    try:
        from ib_async import MarketOrder  # noqa: PLC0415
    except ImportError as fehler:
        raise IbkrFehler(f"ib_async fehlt ({fehler}).")
    if seite not in ("BUY", "SELL"):
        raise IbkrFehler(f"Unbekannte Seite {seite!r}")
    order = MarketOrder(seite, stueck)
    # orderRef ist UNSERE Kennung und steht in jeder Ausfuehrung - damit laesst
    # sich eine Order nach einem Abbruch wiederfinden, genau wie die
    # newClientOrderId bei Binance.
    order.orderRef = order_ref
    # Das Konto wird ausdruecklich gesetzt, obwohl die Sitzung nur eines hat:
    # sollte TWS jemals mehrere verwalten, darf die Order nicht im falschen
    # landen.
    order.account = konto
    order.tif = "DAY"
    # KEINE Ausfuehrung ausserhalb der regulaeren Handelszeiten. Eine
    # Market-Order ist dort bei IBKR ohnehin nicht vorgesehen; die Bruecke
    # sendet sie gar nicht erst (siehe in_handelszeiten()).
    order.outsideRth = False
    return order


def zeitfenster(details) -> list:
    """Die Handelszeitfenster dieses Kontrakts, aus den Angaben der BOERSE.

    `liquidHours` kommt von IBKR in der Form

        20260910:0930-20260910:1600;20260911:CLOSED;...

    zusammen mit `timeZoneId` (z. B. "US/Eastern"). Damit braucht diese
    Bruecke keinen eigenen Feiertagskalender - und genau darum geht es: ein
    selbstgepflegter Kalender ist die Art von doppelt gefuehrter Wahrheit, die
    irgendwann vom Markt abweicht, ohne dass es jemandem auffaellt.
    Verwendet wird `liquidHours` (die regulaere Sitzung), nicht `tradingHours`
    (die auch die erweiterten Zeiten enthaelt).
    """
    roh = (getattr(details, "liquidHours", "") or "").strip()
    zone_name = (getattr(details, "timeZoneId", "") or "").strip()
    if not roh or not zone_name:
        raise IbkrFehler(
            "IBKR hat keine Handelszeiten zu diesem Kontrakt gemeldet "
            "(liquidHours/timeZoneId leer). Ohne Handelszeiten wird nicht "
            "gehandelt - geraten wird hier nichts.")
    try:
        zone = ZoneInfo(_zone_umschreiben(zone_name))
    except Exception as fehler:          # noqa: BLE001
        raise IbkrFehler(
            f"Unbekannte Zeitzone {zone_name!r} von IBKR ({fehler}). Ohne "
            f"eindeutige Zeitzone wird nicht gehandelt.")

    fenster = []
    for teil in roh.split(";"):
        teil = teil.strip()
        if not teil or teil.upper().endswith(":CLOSED"):
            continue
        try:
            von, bis = teil.split("-")
            start = datetime.strptime(von, "%Y%m%d:%H%M").replace(tzinfo=zone)
            if ":" in bis:
                ende = datetime.strptime(bis, "%Y%m%d:%H%M").replace(tzinfo=zone)
            else:
                # Form "20260910:0930-1600" (ohne Datum im zweiten Teil)
                ende = datetime.strptime(von.split(":")[0] + ":" + bis,
                                          "%Y%m%d:%H%M").replace(tzinfo=zone)
        except ValueError:
            raise IbkrFehler(
                f"Handelszeit {teil!r} von IBKR nicht lesbar. Ohne verstandene "
                f"Handelszeiten wird nicht gehandelt.")
        fenster.append((start, ende))
    return fenster


def _zone_umschreiben(name: str) -> str:
    """IBKR liefert teils Kurzformen, die die Zeitzonendatenbank nicht kennt."""
    return {"EST": "US/Eastern", "EST5EDT": "US/Eastern", "CST": "US/Central",
            "CST6CDT": "US/Central", "MST": "US/Mountain",
            "MST7MDT": "US/Mountain", "PST": "US/Pacific",
            "PST8PDT": "US/Pacific"}.get(name, name)


def in_handelszeiten(details, jetzt: datetime = None) -> tuple:
    """(True, None) oder (False, Grund). Entscheidet ausschliesslich anhand der
    von IBKR gemeldeten Fenster."""
    fenster = zeitfenster(details)
    jetzt = jetzt or datetime.now(tz=ZoneInfo("UTC"))
    if jetzt.tzinfo is None:
        raise IbkrFehler("Zeitpunkt ohne Zeitzone - das waere eine Raterei.")
    for start, ende in fenster:
        if start <= jetzt <= ende:
            return True, None
    naechstes = sorted(s for s, _ in fenster if s > jetzt)
    hinweis = (f"naechste Sitzung {naechstes[0].isoformat()}" if naechstes
               else "kein weiteres Fenster in den gemeldeten Angaben")
    return False, (f"ausserhalb der regulaeren Handelszeiten ({hinweis}) - eine "
                   f"Market-Order wird deshalb NICHT gesendet")


class PaperVerbindung:
    """Eine Verbindung zu TWS/IB Gateway im Paper-Betrieb.

    `ib` ist die Gegenstelle und existiert als Parameter, damit die Tests eine
    Attrappe einsetzen koennen - ohne laufende TWS und ohne installiertes
    ib_async.
    """

    def __init__(self, port: int = None, client_id: int = None,
                 erwartetes_konto: str = None, ib=None):
        self.gewuenschter_port = zugang.pruefe_port(
            port if port is not None else zugang.port())
        self.client_id = client_id if client_id is not None else zugang.client_id()
        self.erwartetes_konto = erwartetes_konto
        self._ib = ib
        self.konto = None
        self.verbindungen = []       # (host, port, client_id, nur_lesen)

    # --- Verbindung -------------------------------------------------------
    def verbinden(self, nur_lesen: bool = False) -> str:
        """Verbindet und gibt das bestaetigte Paper-Konto zurueck.

        `nur_lesen=True` setzt IBKRs eigenes readonly-Flag: die Sitzung kann
        dann strukturell keine Order aufgeben. Genau damit laeuft der
        Pruefschritt - er soll die Zugangswege bestaetigen, nicht handeln.
        """
        port = zugang.pruefe_port(self.gewuenschter_port)   # erneut, nicht nur im Konstruktor
        if self._ib is None:
            self._ib = _ib_klasse()()
        try:
            self._ib.connect(zugang.HOST, port, clientId=self.client_id,
                              timeout=ZEITLIMIT_VERBINDUNG, readonly=nur_lesen)
        except ConnectionRefusedError:
            raise IbkrFehler(
                f"Keine Verbindung zu {zugang.HOST}:{port}. Laeuft TWS bzw. "
                f"IB Gateway, ist es am PAPER-Konto angemeldet und ist in den "
                f"API-Einstellungen 'Enable ActiveX and Socket Clients' "
                f"aktiviert? Siehe broker/README_IBKR.md.")
        except Exception as fehler:      # noqa: BLE001
            raise IbkrFehler(f"Verbindung zu {zugang.HOST}:{port} "
                              f"fehlgeschlagen: {fehler}")
        self.verbindungen.append((zugang.HOST, port, self.client_id, nur_lesen))
        try:
            konten = self._ib.managedAccounts()
        except Exception as fehler:      # noqa: BLE001
            self.trennen()
            raise IbkrFehler(f"Konten konnten nicht gelesen werden: {fehler}")
        try:
            self.konto = zugang.pruefe_konten(konten, self.erwartetes_konto)
        except zugang.ZugangFehler:
            # Sofort trennen: eine Sitzung, die ein Live-Konto verwaltet, soll
            # nicht offen bleiben.
            self.trennen()
            raise
        return self.konto

    def trennen(self):
        if self._ib is not None:
            try:
                self._ib.disconnect()
            except Exception:            # noqa: BLE001
                pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.trennen()
        return False

    # --- Kontrakt und Handelszeiten --------------------------------------
    def kontrakt(self, symbol: str):
        """(contract, details) - und zwar nur bei GENAU EINEM Treffer.

        SMART-Routing kann ein Kuerzel auf mehrere Kontrakte abbilden (dieselbe
        Firma an mehreren Boersen, oder ein Kuerzel, das doppelt vergeben ist).
        Dann wird abgebrochen statt den ersten zu nehmen: an einem Broker ist
        der falsche Kontrakt das falsche Unternehmen.
        """
        roh = _aktie(symbol)
        try:
            treffer = self._ib.reqContractDetails(roh)
        except Exception as fehler:       # noqa: BLE001
            raise IbkrFehler(f"Kontraktsuche fuer {symbol} fehlgeschlagen: {fehler}")
        if not treffer:
            raise IbkrFehler(
                f"IBKR kennt unter {zugang.ibkr_symbol(symbol)} "
                f"({zugang.BOERSE}/{zugang.WAEHRUNG}) keinen Kontrakt.")
        if len(treffer) > 1:
            beschreibung = ", ".join(
                f"{t.contract.symbol}@{t.contract.primaryExchange or t.contract.exchange}"
                for t in treffer[:5])
            raise IbkrFehler(
                f"{zugang.ibkr_symbol(symbol)} ist nicht eindeutig - IBKR "
                f"meldet {len(treffer)} Kontrakte ({beschreibung}). Es wird "
                f"nichts gehandelt, solange nicht klar ist, welcher gemeint "
                f"ist.")
        return treffer[0].contract, treffer[0]

    # --- Orders -----------------------------------------------------------
    def order_nach_ref(self, order_ref: str):
        """Eine frueher gesendete Order anhand UNSERER Kennung wiederfinden -
        die Absicherung gegen den Abbruch zwischen Senden und Speichern.
        Gibt eine Ausfuehrungsuebersicht zurueck oder None."""
        ausfuehrungen = []
        try:
            for fill in (self._ib.fills() or []):
                if getattr(fill.execution, "orderRef", "") == order_ref:
                    ausfuehrungen.append(fill)
        except Exception as fehler:       # noqa: BLE001
            raise IbkrFehler(f"Ausfuehrungen nicht lesbar: {fehler}")
        if ausfuehrungen:
            return ausfuehrung_auswerten(None, ausfuehrungen, order_ref)
        # Noch offene Order mit derselben Kennung? Dann ist sie draussen, aber
        # nicht ausgefuehrt - das ist KEIN Grund, eine zweite zu schicken.
        try:
            for trade in (self._ib.trades() or []):
                if getattr(trade.order, "orderRef", "") == order_ref:
                    return ausfuehrung_auswerten(trade, trade.fills, order_ref)
        except Exception as fehler:       # noqa: BLE001
            raise IbkrFehler(f"Offene Orders nicht lesbar: {fehler}")
        return None

    def marktorder(self, contract, seite: str, stueck: int, order_ref: str,
                    zeitlimit: float = None) -> dict:
        """EINE Market-Order, und dann warten, bis sie ausgefuehrt oder
        abgelehnt ist. Eine Order, deren Ausgang unbekannt bleibt, wird als
        solche gemeldet - nicht als Erfolg und nicht als Fehlschlag."""
        if self.konto is None:
            raise IbkrFehler("Nicht verbunden - es gibt kein bestaetigtes Konto.")
        if zugang.notbremse_aktiv():
            raise IbkrFehler(
                f"NOTBREMSE aktiv ({zugang.NOTBREMSE_DATEI} existiert) - es "
                f"wurde nichts gesendet.")
        # Zur LAUFZEIT gelesen, nicht als Standardwert gebunden: so kann der
        # Test das Warten kuerzen, ohne den Aufrufweg zu aendern.
        zeitlimit = ZEITLIMIT_AUSFUEHRUNG if zeitlimit is None else zeitlimit
        order = _marktorder(seite, stueck, order_ref, self.konto)
        try:
            trade = self._ib.placeOrder(contract, order)
        except Exception as fehler:        # noqa: BLE001
            raise IbkrFehler(f"Order nicht angenommen: {fehler}")

        ende = _jetzt_sekunden() + zeitlimit
        while not _ist_fertig(trade) and _jetzt_sekunden() < ende:
            self._ib.waitOnUpdate(timeout=1)
        ergebnis = ausfuehrung_auswerten(trade, trade.fills, order_ref)
        status = ergebnis["status"]
        if status == "Filled":
            return ergebnis
        meldung = _letzte_meldung(trade)
        if status in ("Cancelled", "ApiCancelled", "Inactive"):
            raise IbkrFehler(
                f"IBKR hat die Order abgelehnt oder storniert (Status {status})"
                f"{': ' + meldung if meldung else ''}", code=_letzter_code(trade))
        raise IbkrFehler(
            f"Die Order steht nach {zeitlimit:g} s noch auf Status {status!r} "
            f"(ausgefuehrt {ergebnis['stueck']} von {stueck})"
            f"{': ' + meldung if meldung else ''}. Sie ist moeglicherweise "
            f"DRAUSSEN - der naechste Lauf erkennt sie an der Kennung "
            f"{order_ref} wieder und schickt keine zweite.",
            code=_letzter_code(trade))


def _jetzt_sekunden() -> float:
    import time
    return time.monotonic()


def _ist_fertig(trade) -> bool:
    try:
        return bool(trade.isDone())
    except Exception:                     # noqa: BLE001
        return str(getattr(trade.orderStatus, "status", "")) in (
            "Filled", "Cancelled", "ApiCancelled", "Inactive")


def _letzte_meldung(trade) -> str:
    eintraege = list(getattr(trade, "log", []) or [])
    for eintrag in reversed(eintraege):
        text = (getattr(eintrag, "message", "") or "").strip()
        if text:
            return text[:200]
    return ""


def _letzter_code(trade):
    for eintrag in reversed(list(getattr(trade, "log", []) or [])):
        code = getattr(eintrag, "errorCode", None)
        if code:
            return code
    return None


def ausfuehrung_auswerten(trade, fills, order_ref: str) -> dict:
    """Die Zahlen, auf die es ankommt - MENGENGEWICHTET ueber alle
    Teilausfuehrungen, mit den echten Gebuehren.

    Anders als bei Binance wird die Gebuehr hier IMMER in der Kontowaehrung
    abgerechnet (USD), nie in der gekauften Aktie. Es gibt deshalb keine
    Restmenge: verkauft wird genau die Stueckzahl, die gekauft wurde. Der
    Abgleich ist dadurch einfacher als bei Krypto - eine Stolperfalle weniger.
    """
    fills = list(fills or [])
    stueck = 0.0
    summe = 0.0
    gebuehr = 0.0
    waehrungen = set()
    zeitpunkte = []
    for fill in fills:
        ausf = fill.execution
        menge = float(getattr(ausf, "shares", 0) or 0)
        preis = float(getattr(ausf, "price", 0) or 0)
        stueck += menge
        summe += menge * preis
        bericht = getattr(fill, "commissionReport", None)
        if bericht is not None:
            gebuehr += float(getattr(bericht, "commission", 0) or 0)
            if getattr(bericht, "currency", ""):
                waehrungen.add(bericht.currency)
        if getattr(ausf, "time", None):
            zeitpunkte.append(str(ausf.time))
    status = "Unbekannt"
    order_id = None
    if trade is not None:
        status = str(getattr(trade.orderStatus, "status", "") or "Unbekannt")
        order_id = str(getattr(trade.order, "orderId", "") or "") or None
        if not order_id:
            order_id = str(getattr(trade.orderStatus, "permId", "") or "") or None
    elif fills:
        status = "Filled"
        order_id = str(getattr(fills[0].execution, "permId", "") or "") or None
    return {
        "order_id": order_id,
        "order_ref": order_ref,
        "status": status,
        "stueck": stueck,
        "preis": (summe / stueck) if stueck else None,
        "gegenwert": summe,
        "gebuehr": gebuehr,
        "gebuehr_waehrung": sorted(waehrungen)[0] if waehrungen else None,
        "anzahl_teilausfuehrungen": len(fills),
        "zeitpunkte": zeitpunkte,
    }


def pruefe_stueckzahl(stueck: int, details) -> int:
    """Die Stueckzahl gegen die Angaben der Boerse. US-Aktien handeln in ganzen
    Stuecken; trotzdem wird minSize/sizeIncrement gelesen statt angenommen -
    dieselbe Regel wie bei den LOT_SIZE-Filtern von Binance."""
    min_size = float(getattr(details, "minSize", 0) or 0)
    schritt = float(getattr(details, "sizeIncrement", 0) or 0)
    if min_size and stueck < min_size:
        raise IbkrFehler(
            f"{stueck} Stueck liegt unter der Mindestgroesse {min_size:g} "
            f"dieses Kontrakts.")
    if schritt and abs((stueck / schritt) - round(stueck / schritt)) > 1e-9:
        raise IbkrFehler(
            f"{stueck} Stueck ist kein Vielfaches der Schrittweite {schritt:g} "
            f"dieses Kontrakts.")
    return int(stueck)

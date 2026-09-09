"""
Die EINE schreibende Faehigkeit des Dashboards
==============================================================================
Bis zu diesem Modul war das Dashboard ausschliesslich lesend (siehe den
Docstring von app.py und den Nachweis in test_dashboard.py). Hier kommt
genau eine Ausnahme hinzu: eine offene Position von Hand schliessen, fuer
genau einen Bot, nach zwei unabhaengigen Bestaetigungen.

------------------------------------------------------------------------------
Was hier NICHT steht - und warum das der Punkt ist
------------------------------------------------------------------------------
Die eigentliche Schreiblogik steht NICHT in dieser Datei, sondern
unveraendert in `notifications/manual_close.py`: Freischaltungsliste,
Schema, PnL-Formel, Transaktion mit `BEGIN IMMEDIATE`, die erneute
Pruefung innerhalb der Transaktion, `rowcount == 1`, das Protokoll. Dieses
Modul ruft dort genau eine Funktion auf.

Das ist Absicht und die wichtigste Eigenschaft der Aufgabe: der Kern ist
mit 129 Pruefungen abgesichert, darunter vier Nebenlaeufigkeits-Szenarien
mit echten Prozessen. Eine zweite, dashboard-eigene Umsetzung waere genau
die Doppelfuehrung, die in diesem Projekt schon mehrfach dazu gefuehrt
hat, dass zwei Seiten unbemerkt auseinanderliefen - und sie waere hier
nicht bloss unsauber, sondern gefaehrlich: die zweite Fassung haette die
Absicherungen der ersten nicht.

Hier steht deshalb nur, was die Oberflaeche wirklich braucht:
  1. die Liste der schliessbaren Positionen samt Live-Kurs und PnL,
  2. der Zustand zwischen den beiden Bestaetigungen,
  3. die Uebersetzung in JSON-taugliche Werte.

------------------------------------------------------------------------------
Warum die zweite Bestaetigung SERVERSEITIG gehalten wird
------------------------------------------------------------------------------
Ein Bestaetigungsdialog im Browser ist keine Sicherung, sondern eine
Hoeflichkeit: die API bleibt mit `curl` direkt aufrufbar, und ein
Frontend-Gate liesse sich mit einem einzigen Aufruf umgehen. Deshalb sind
es zwei getrennte HTTP-Aufrufe, und der zweite ist ohne den ersten
wirkungslos:

    POST .../schliessen/vorbereiten   legt einen Vorgang an (120 s gueltig)
    POST .../schliessen/ausfuehren    braucht dessen Kennung UND den Text

Es gibt keinen Weg, in einem einzigen Aufruf zu schreiben. Die Kennung
ist zufaellig, einmalig verwendbar und laeuft ab; der Bestaetigungstext
wird zusaetzlich in `manual_close` noch einmal geprueft.

WELCHER KURS GESCHRIEBEN WIRD: der, den der Nutzer in der Zusammenfassung
gesehen und bestaetigt hat - nicht ein beim Ausfuehren neu geholter. Er
bestaetigt eine konkrete Zahl; still zu einer anderen zu schliessen waere
die groessere Ueberraschung. Deshalb die kurze Frist. Dieselbe Abwaegung
wie bei der Telegram-Variante.
"""

import logging
import os
import secrets
import sys
import time

_DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DASHBOARD_DIR)
_NOTIFICATIONS_DIR = os.path.join(BASE_DIR, "notifications")
if _NOTIFICATIONS_DIR not in sys.path:
    sys.path.insert(0, _NOTIFICATIONS_DIR)

import manual_close  # noqa: E402

logger = logging.getLogger("dashboard.schliessen")

# Der Fehlertyp und der Bestaetigungstext kommen aus dem Kern - hier wird
# nichts davon neu definiert. Wer `BESTAETIGUNGSTEXT` aendern will, aendert
# es an einer Stelle und beide Oberflaechen ziehen mit.
SchliessenNichtMoeglich = manual_close.SchliessenNichtMoeglich
BESTAETIGUNGSTEXT = manual_close.BESTAETIGUNGSTEXT
GUELTIG_SEKUNDEN = manual_close.BESTAETIGUNG_GUELTIG_SEKUNDEN

# Obergrenze fuer gleichzeitig offene Vorgaenge. Es gibt genau einen
# Nutzer; mehr als eine Handvoll kann es nur geben, wenn jemand den
# vorbereiten-Endpunkt in einer Schleife aufruft. Dann sollen nicht
# unbegrenzt Eintraege im Speicher wachsen.
MAX_VORGAENGE = 20

_VORGAENGE = {}


class Vorgang(dict):
    """Ein angefangener Schliessvorgang zwischen den beiden Bestaetigungen.
    Bewusst ein einfaches dict: der Inhalt geht als JSON ans Frontend."""


def _jetzt() -> float:
    return time.time()


def _aufraeumen() -> None:
    for kennung, vorgang in list(_VORGAENGE.items()):
        if vorgang["gueltig_bis"] < _jetzt():
            _VORGAENGE.pop(kennung, None)


def vorgaenge_zuruecksetzen() -> None:
    """Nur fuer Tests und den Serverstart - ein Vorgang ueberlebt einen
    Neustart ohnehin nicht (er liegt nur im Speicher, absichtlich: ein
    halb bestaetigter Schreibzugriff soll einen Neustart NICHT
    ueberdauern)."""
    _VORGAENGE.clear()


# ---------------------------------------------------------------------------
# Lesen
# ---------------------------------------------------------------------------

def ist_freigeschaltet(bot_name: str) -> bool:
    return bot_name in manual_close.SCHLIESSBARE_BOTS


def freigeschaltete_bots() -> list:
    return sorted(manual_close.SCHLIESSBARE_BOTS)


def _gerundet(wert):
    return None if wert is None else round(float(wert), 6)


def positionen(bot_name: str, kurse: dict = None) -> dict:
    """Die offenen Positionen des Bots, wie das Frontend sie braucht.

    Die Zeilen-IDs kommen aus `manual_close.offene_positionen()` - also
    aus GENAU derselben Funktion, die beim Schreiben verwendet wird.
    monitor.get_bot_status() liefert die ID nicht mit, und eine zweite
    Leseroutine haette hier die unangenehmste aller Fehlermoeglichkeiten:
    eine angezeigte ID, die zu einer anderen Zeile gehoert als die
    geschlossene.
    """
    if not ist_freigeschaltet(bot_name):
        return {
            "bot": bot_name,
            "schliessbar": False,
            "grund": (f"Fuer '{bot_name}' ist das manuelle Schliessen nicht "
                       f"freigeschaltet. Freigeschaltet: "
                       f"{', '.join(freigeschaltete_bots())}."),
            "positionen": [],
            "bestaetigungstext": BESTAETIGUNGSTEXT,
            "gueltig_sekunden": GUELTIG_SEKUNDEN,
        }

    kurse = kurse or {}
    zeilen = []
    for position in manual_close.offene_positionen(bot_name):
        kurs = kurse.get(position["symbol"])
        kurs = float(kurs) if kurs else None
        pnl = None
        if kurs and position.get("entry_price"):
            pnl = manual_close.berechne_pnl(bot_name, position["entry_price"], kurs)
        zeilen.append({
            "id": position["id"],
            "symbol": position["symbol"],
            "entry_time": position.get("entry_time"),
            "entry_preis": _gerundet(position.get("entry_price")),
            "stop_preis": _gerundet(position.get("stop_price")),
            "aktueller_preis": _gerundet(kurs),
            "pnl_pct": pnl,
            # Ohne Kurs darf nicht geschrieben werden - dann bietet das
            # Frontend die Schaltflaeche gar nicht erst an, statt einen
            # Knopf zu zeigen, der garantiert in einer Absage endet.
            "schliessbar_jetzt": kurs is not None,
        })
    return {
        "bot": bot_name,
        "anzeigename": manual_close.SCHLIESSBARE_BOTS[bot_name]["anzeigename"],
        "schliessbar": True,
        "grund": None,
        "positionen": zeilen,
        "bestaetigungstext": BESTAETIGUNGSTEXT,
        "gueltig_sekunden": GUELTIG_SEKUNDEN,
    }


# ---------------------------------------------------------------------------
# Erste Bestaetigung: Vorgang anlegen
# ---------------------------------------------------------------------------

def vorbereiten(bot_name: str, trade_id, kurse: dict) -> dict:
    """Stufe 1. Legt einen Vorgang an und gibt die Zusammenfassung
    zurueck, die dem Nutzer gezeigt wird. Schreibt nichts."""
    if not ist_freigeschaltet(bot_name):
        raise SchliessenNichtMoeglich(
            f"Fuer '{bot_name}' ist das manuelle Schliessen nicht freigeschaltet. "
            f"Freigeschaltet: {', '.join(freigeschaltete_bots())}.")
    try:
        trade_id = int(trade_id)
    except (TypeError, ValueError):
        raise SchliessenNichtMoeglich("Ungueltige Positions-Kennung.")

    treffer = [p for p in manual_close.offene_positionen(bot_name)
               if p["id"] == trade_id]
    if not treffer:
        raise SchliessenNichtMoeglich(
            f"Position {trade_id} ist nicht (mehr) offen - vermutlich hat der "
            f"Cronjob des Bots sie inzwischen selbst geschlossen. Es wurde "
            f"nichts geaendert.")
    position = treffer[0]

    kurs = (kurse or {}).get(position["symbol"])
    kurs = float(kurs) if kurs else None
    if not kurs:
        raise SchliessenNichtMoeglich(
            "Kein aktueller Kurs verfuegbar. Ohne Ausstiegskurs wird nicht "
            "geschrieben - bitte spaeter erneut versuchen.")
    if not position.get("entry_price"):
        raise SchliessenNichtMoeglich(
            "Der Einstiegskurs dieser Position fehlt in der Datenbank - der "
            "PnL waere nicht berechenbar. Es wird nichts geschrieben.")

    pnl = manual_close.berechne_pnl(bot_name, position["entry_price"], kurs)

    _aufraeumen()
    if len(_VORGAENGE) >= MAX_VORGAENGE:
        raise SchliessenNichtMoeglich(
            "Zu viele offene Bestaetigungen. Bitte kurz warten, bis die "
            "aelteren abgelaufen sind.")

    kennung = secrets.token_urlsafe(24)
    _VORGAENGE[kennung] = Vorgang({
        "kennung": kennung,
        "bot": bot_name,
        "trade_id": trade_id,
        "symbol": position["symbol"],
        "entry_preis": _gerundet(position["entry_price"]),
        "kurs": kurs,
        "pnl_pct": pnl,
        "gueltig_bis": _jetzt() + GUELTIG_SEKUNDEN,
    })
    logger.info(f"Schliessvorgang vorbereitet: Bot {bot_name}, Trade "
                f"{trade_id} ({position['symbol']}) - noch nichts geschrieben.")

    return {
        "vorgang": kennung,
        "bot": bot_name,
        "anzeigename": manual_close.SCHLIESSBARE_BOTS[bot_name]["anzeigename"],
        "trade_id": trade_id,
        "symbol": position["symbol"],
        "entry_time": position.get("entry_time"),
        "entry_preis": _gerundet(position["entry_price"]),
        "aktueller_preis": _gerundet(kurs),
        "pnl_pct": pnl,
        "bestaetigungstext": BESTAETIGUNGSTEXT,
        "gueltig_sekunden": GUELTIG_SEKUNDEN,
    }
    # Der WARNTEXT steht bewusst NICHT hier, sondern in bot.html. Alle
    # uebrigen Beschriftungen des Dashboards stehen ebenfalls im Frontend;
    # eine zweite Fassung desselben Satzes hier waere genau die Art von
    # Doppelfuehrung, die in diesem Projekt schon mehrfach auseinander
    # gelaufen ist - und sie muesste ausserdem ohne Umlaute auskommen,
    # waehrend die Seite ringsum ordentliches Deutsch zeigt.


def abbrechen(kennung) -> bool:
    """Stufe 1 oder 2 abgebrochen. Gibt zurueck, ob es ueberhaupt einen
    Vorgang gab - fuer den Nutzer ist das Ergebnis in beiden Faellen
    dasselbe: es wurde nichts geaendert."""
    _aufraeumen()
    return _VORGAENGE.pop(str(kennung or ""), None) is not None


def offener_vorgang(kennung):
    """Der Vorgang zur Kennung, oder None (unbekannt oder abgelaufen).
    Abgelaufene werden dabei entfernt, damit ein spaet eintreffendes
    BESTAETIGEN nicht doch noch etwas ausloest."""
    _aufraeumen()
    return _VORGAENGE.get(str(kennung or ""))


# ---------------------------------------------------------------------------
# Zweite Bestaetigung: ausfuehren
# ---------------------------------------------------------------------------

def ausfuehren(bot_name: str, kennung, bestaetigung, benutzer) -> dict:
    """Stufe 2 - der einzige Weg im Dashboard, der schreibt.

    Der Vorgang wird in JEDEM Fall verbraucht, auch bei falschem Text.
    Sonst liesse sich der Bestaetigungstext innerhalb der Frist beliebig
    oft durchprobieren; er ist zwar bekannt und kein Geheimnis, aber ein
    Vorgang, der nach einem Fehlversuch weiterlebt, waere ein zweiter
    Versuch, den der Nutzer nicht angefordert hat.
    """
    vorgang = offener_vorgang(kennung)
    if vorgang is None:
        # Auch DIESER Versuch gehoert ins Protokoll. Er ist der einzige,
        # den ein direkter API-Aufruf ohne vorherige Stufe 1 ueberhaupt
        # erzeugen kann - also genau die Zeile, an der auffiele, dass
        # jemand den Bestaetigungsdialog zu umgehen versucht. Welche
        # Position gemeint war, ist dabei nicht bekannt.
        manual_close.protokolliere_ablehnung(
            bot_name, None, benutzer,
            "keine gueltige Bestaetigung offen (unbekannt oder abgelaufen)",
            manual_close.QUELLE_DASHBOARD)
        # Bewusst KEINE Unterscheidung zwischen "unbekannt" und
        # "abgelaufen" gegenueber dem Aufrufer: beides endet gleich, und
        # die Unterscheidung verriete nur, ob eine geratene Kennung
        # existiert hat.
        raise SchliessenNichtMoeglich(
            f"Keine gueltige Bestaetigung offen - sie ist abgelaufen "
            f"({GUELTIG_SEKUNDEN} Sekunden) oder wurde bereits verbraucht. "
            f"Es wurde nichts geaendert; bitte von vorn beginnen.")

    _VORGAENGE.pop(vorgang["kennung"], None)

    if vorgang["bot"] != bot_name:
        manual_close.protokolliere_ablehnung(
            bot_name, vorgang["trade_id"], benutzer,
            "Bestaetigung gehoert zu einem anderen Bot",
            manual_close.QUELLE_DASHBOARD)
        raise SchliessenNichtMoeglich(
            "Die Bestaetigung gehoert zu einem anderen Bot. Es wurde nichts "
            "geaendert.")

    # Der Text wird HIER geprueft, damit eine falsche Eingabe den Vorgang
    # verbraucht - und gleich darauf noch einmal im Kern, der ihn ebenfalls
    # verlangt. Doppelt, weil die zweite Pruefung die ist, die auch dann
    # noch greift, wenn jemand kuenftig eine dritte Oberflaeche baut.
    if (bestaetigung or "").strip() != BESTAETIGUNGSTEXT:
        manual_close.protokolliere_ablehnung(
            bot_name, vorgang["trade_id"], benutzer,
            "falscher Bestaetigungstext", manual_close.QUELLE_DASHBOARD)
        raise SchliessenNichtMoeglich(
            f"Der Bestaetigungstext stimmt nicht - erwartet wird genau "
            f"'{BESTAETIGUNGSTEXT}', Gross-/Kleinschreibung inbegriffen. Es "
            f"wurde nichts geaendert.")

    ergebnis = manual_close.schliesse_position(
        bot_name, vorgang["trade_id"], vorgang["kurs"], benutzer,
        BESTAETIGUNGSTEXT, quelle=manual_close.QUELLE_DASHBOARD)

    return {
        "erfolg": True,
        "bot": ergebnis["bot"],
        "trade_id": ergebnis["trade_id"],
        "symbol": ergebnis["symbol"],
        "entry_preis": _gerundet(ergebnis["entry_price"]),
        "exit_preis": _gerundet(ergebnis["exit_price"]),
        "exit_time": ergebnis["exit_time"],
        "pnl_pct": ergebnis["pnl_pct"],
        "ergebnis": ergebnis["result"],
        "meldung": (f"{ergebnis['symbol']} zum Kurs {ergebnis['exit_price']} "
                     f"geschlossen ({ergebnis['pnl_pct']:+.2f} %). Vermerkt als "
                     f"'{ergebnis['result']}'; der Eingriff steht im Protokoll "
                     f"logs/notifications/manuelle_eingriffe.log."),
    }

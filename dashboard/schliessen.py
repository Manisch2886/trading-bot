"""
Die EINE schreibende Faehigkeit des Dashboards
==============================================================================
Bis zu diesem Modul war das Dashboard ausschliesslich lesend (siehe den
Docstring von app.py und den Nachweis in test_dashboard.py). Hier kommt
genau eine Faehigkeit hinzu: offene Positionen von Hand schliessen, fuer
genau einen Bot - in zwei Varianten, beide abgesichert ueber zwei getrennte
Server-Aufrufe:

  EINZELN   eine Position, EIN Tap in der Oberflaeche
  ALLE      alle offenen Positionen, ZWEI Klicks (Notfallweg, siehe unten)

Beide schreiben ausschliesslich ueber `manual_close.schliesse_position()` -
je Position ein Aufruf, auch der Notfallweg. Dort steht keine Schleife und
hier keine Schreiblogik.

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
  2. der Zustand zwischen Zusammenfassung und Ausfuehrung,
  3. die Uebersetzung in JSON-taugliche Werte.

------------------------------------------------------------------------------
Warum die Absicherung SERVERSEITIG liegt - auch bei nur einem Tap
------------------------------------------------------------------------------
Ein Bestaetigungsdialog im Browser ist keine Sicherung, sondern eine
Hoeflichkeit: die API bleibt mit `curl` direkt aufrufbar, und ein
Frontend-Gate liesse sich mit einem einzigen Aufruf umgehen. Deshalb sind
es zwei getrennte HTTP-Aufrufe, und der zweite ist ohne den ersten
wirkungslos:

    POST .../schliessen/vorbereiten   legt einen Vorgang an (120 s gueltig)
    POST .../schliessen/ausfuehren    braucht genau diese Kennung

Es gibt keinen Weg, in einem einzigen Aufruf zu schreiben. Die Kennung
ist zufaellig, einmalig verwendbar und laeuft ab, und sie gilt nur fuer
den Bot und die Position, fuer die sie angelegt wurde.

In der OBERFLAECHE reicht dafuer EIN Tap: Position antippen -> die
Zusammenfassung erscheint (das ist bereits der `vorbereiten`-Aufruf) ->
ein Tap auf "Ja, schliessen" schreibt. Die frueher zusaetzlich verlangte
Texteingabe ("BESTAETIGEN" eintippen) ist entfallen. Begruendung: in
einem schnellen Kryptomarkt kostet der Tippschritt Zeit, und es geht um
Paper-Trading ohne echtes Kapital - die Abwaegung ist eine andere als bei
echtem Geld. Entfallen ist damit AUSSCHLIESSLICH die zweite Eingabe in
der Oberflaeche; die Zwei-Aufruf-Architektur, die Frist, die Bot- und
Positionsbindung der Kennung und jede Pruefung im Kern bleiben. Die
Telegram-Variante behaelt ihre zwei Stufen - das ist eine eigene
Entscheidung und ein eigener Branch.

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

# Der Fehlertyp und die Frist kommen aus dem Kern - hier wird nichts davon
# neu definiert, damit Dashboard und Telegram-Variante nicht auseinander
# laufen koennen.
SchliessenNichtMoeglich = manual_close.SchliessenNichtMoeglich
GUELTIG_SEKUNDEN = manual_close.BESTAETIGUNG_GUELTIG_SEKUNDEN

# Der Kern verlangt den Bestaetigungstext weiterhin als Argument - dort ist
# er die Absicherung fuer JEDE Oberflaeche, auch fuer die Telegram-Variante
# und fuer eine kuenftige dritte. Der Dashboard-Weg stellt die Bedingung
# nicht mehr an den Nutzer, sondern erfuellt sie selbst: er reicht die
# Konstante durch, nachdem er die Vorgangs-Kennung geprueft hat. Die
# Absicherung dieses Wegs ist also die Kennung, nicht der Text - was sie
# vorher schon war, denn ein bekannter, immer gleicher Text haelt niemanden
# auf, der die API direkt aufruft. Der Text wird dem Frontend bewusst NICHT
# mehr mitgeschickt: er spielt dort keine Rolle mehr, und ein Feld, das
# niemand liest, ist nur eine Einladung, es doch wieder zu benutzen.
BESTAETIGUNGSTEXT = manual_close.BESTAETIGUNGSTEXT

# Obergrenze fuer gleichzeitig offene Vorgaenge. Es gibt genau einen
# Nutzer; mehr als eine Handvoll kann es nur geben, wenn jemand den
# vorbereiten-Endpunkt in einer Schleife aufruft. Dann sollen nicht
# unbegrenzt Eintraege im Speicher wachsen.
MAX_VORGAENGE = 20

# Es gibt ZWEI Arten von Vorgaengen, und eine Kennung der einen Art darf auf
# dem Endpunkt der anderen nichts ausloesen. Beide liegen bewusst im
# SELBEN Speicher - so gelten Ablauffrist, Einmaligkeit, Obergrenze und
# `abbrechen()` ohne Zutun fuer beide, statt in einer zweiten Verwaltung
# nachgebaut (und irgendwann anders) zu werden. Die Trennung leistet
# stattdessen dieses eine Feld, das beide Ausfuehren-Wege pruefen.
ART_EINZEL = "einzel"
ART_ALLE = "alle"

_VORGAENGE = {}


class Vorgang(dict):
    """Ein angefangener Schliessvorgang zwischen Zusammenfassung und
    Ausfuehrung. Bewusst ein einfaches dict: der Inhalt geht als JSON ans
    Frontend."""


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
        "gueltig_sekunden": GUELTIG_SEKUNDEN,
    }


# ---------------------------------------------------------------------------
# Erste Bestaetigung: Vorgang anlegen
# ---------------------------------------------------------------------------

def vorbereiten(bot_name: str, trade_id, kurse: dict) -> dict:
    """Aufruf 1. Legt einen Vorgang an und gibt die Zusammenfassung
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
        "art": ART_EINZEL,
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
        "gueltig_sekunden": GUELTIG_SEKUNDEN,
    }
    # Der WARNTEXT steht bewusst NICHT hier, sondern in bot.html. Alle
    # uebrigen Beschriftungen des Dashboards stehen ebenfalls im Frontend;
    # eine zweite Fassung desselben Satzes hier waere genau die Art von
    # Doppelfuehrung, die in diesem Projekt schon mehrfach auseinander
    # gelaufen ist - und sie muesste ausserdem ohne Umlaute auskommen,
    # waehrend die Seite ringsum ordentliches Deutsch zeigt.


def abbrechen(kennung) -> bool:
    """Der Nutzer hat den Dialog verworfen (Knopf, Esc oder Klick daneben).
    Gibt zurueck, ob es ueberhaupt einen Vorgang gab - fuer den Nutzer ist
    das Ergebnis in beiden Faellen dasselbe: es wurde nichts geaendert."""
    _aufraeumen()
    return _VORGAENGE.pop(str(kennung or ""), None) is not None


def offener_vorgang(kennung):
    """Der Vorgang zur Kennung, oder None (unbekannt oder abgelaufen).
    Abgelaufene werden dabei entfernt, damit ein spaet eintreffender
    Ausfuehren-Aufruf nicht doch noch etwas ausloest."""
    _aufraeumen()
    return _VORGAENGE.get(str(kennung or ""))


# ---------------------------------------------------------------------------
# Ausfuehren - der einzige schreibende Weg
# ---------------------------------------------------------------------------

def _vorgang_einloesen(bot_name: str, kennung, benutzer, art: str) -> Vorgang:
    """Loest eine Vorgangs-Kennung ein: prueft Herkunft, Frist, Art und
    Bot-Zuordnung, verbraucht sie und gibt den Vorgang zurueck.

    BEIDE schreibenden Wege gehen hier durch - der fuer eine Position und
    der fuer alle. Bewusst eine gemeinsame Funktion: eine zweite Fassung
    dieser Pruefungen waere genau die Doppelfuehrung, die in diesem Projekt
    schon mehrfach auseinandergelaufen ist, und hier waere sie die
    gefaehrlichste Stelle dafuer - eine Nachlaessigkeit fiele erst auf,
    wenn sie ausgenutzt wird.

    Der Vorgang wird in JEDEM Fall verbraucht, auch wenn der Versuch danach
    scheitert: ein Vorgang, der einen Fehlversuch ueberlebt, waere ein
    zweiter Versuch, den der Nutzer nicht angefordert hat.
    """
    vorgang = offener_vorgang(kennung)
    if vorgang is None:
        # Auch DIESER Versuch gehoert ins Protokoll. Er ist der einzige,
        # den ein direkter API-Aufruf ohne vorheriges `vorbereiten`
        # ueberhaupt erzeugen kann - also genau die Zeile, an der auffiele,
        # dass jemand den Bestaetigungsdialog zu umgehen versucht. Welche
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

    # Eine Kennung fuer EINE Position darf auf dem Alle-Endpunkt nichts
    # ausloesen und umgekehrt. Ohne diese Pruefung waere die zweite
    # Klick-Bestaetigung des Notfallwegs umgehbar: man koennte die billiger
    # zu bekommende Einzel-Kennung auf dem Alle-Endpunkt einloesen.
    if vorgang.get("art") != art:
        manual_close.protokolliere_ablehnung(
            bot_name, vorgang.get("trade_id"), benutzer,
            f"Bestaetigung ist fuer '{vorgang.get('art')}', angefragt wurde "
            f"'{art}'", manual_close.QUELLE_DASHBOARD)
        raise SchliessenNichtMoeglich(
            "Die Bestaetigung gehoert zu einem anderen Vorgang. Es wurde "
            "nichts geaendert; bitte von vorn beginnen.")

    if vorgang["bot"] != bot_name:
        manual_close.protokolliere_ablehnung(
            bot_name, vorgang.get("trade_id"), benutzer,
            "Bestaetigung gehoert zu einem anderen Bot",
            manual_close.QUELLE_DASHBOARD)
        raise SchliessenNichtMoeglich(
            "Die Bestaetigung gehoert zu einem anderen Bot. Es wurde nichts "
            "geaendert.")

    return vorgang


def ausfuehren(bot_name: str, kennung, benutzer) -> dict:
    """Aufruf 2 - schliesst GENAU EINE Position.

    Verlangt eine gueltige, noch nicht abgelaufene Vorgangs-Kennung aus
    Aufruf 1. Eine zusaetzliche Texteingabe wird NICHT mehr verlangt (siehe
    Modul-Kopf); die Kennung ist die Absicherung, und sie ist es auch
    vorher schon gewesen.
    """
    vorgang = _vorgang_einloesen(bot_name, kennung, benutzer, ART_EINZEL)

    # Der Kern verlangt den Bestaetigungstext weiter; der wird hier aus der
    # Konstante gesetzt, nicht aus der Anfrage gelesen (siehe Modul-Kopf).
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


# ---------------------------------------------------------------------------
# Notfallweg: ALLE offenen Positionen eines Bots
# ---------------------------------------------------------------------------
# Warum hier ZWEI Klick-Bestaetigungen stehen, waehrend der Einzelweg mit
# einer auskommt: die Tragweite ist eine andere. Beim Einzelschliessen sieht
# der Nutzer genau die eine Zeile, die er trifft. Hier trifft ein Tap
# potenziell fuenf Positionen gleichzeitig - und der Weg zurueck ist in
# beiden Faellen SQL von Hand. Eine Texteingabe ist es trotzdem nicht
# geworden: sie war auch beim Einzelweg nicht die Absicherung (das ist die
# Vorgangs-Kennung), sie kostet nur Zeit. Zwei Klicks auf zwei verschiedene
# Knoepfe sind gegen ein Versehen genauso wirksam.
#
# WELCHE POSITIONEN GESCHLOSSEN WERDEN - die wichtigste Festlegung hier:
# Beim Ausfuehren wird der TATSAECHLICHE Stand neu gelesen, nicht die Liste
# aus der Uebersicht abgearbeitet. Aus beiden Mengen wird der Schnitt
# gebildet:
#
#   bestaetigt UND noch offen   -> wird geschlossen
#   bestaetigt, nicht mehr offen -> uebersprungen (der Cronjob war schneller)
#   offen, aber NICHT bestaetigt -> wird NICHT angefasst
#
# Der letzte Fall ist eine Entscheidung, keine Nebenwirkung: der Bot kann
# zwischen Uebersicht und Tap eine neue Position eroeffnen. Sie zu schliessen
# hiesse, etwas anzufassen, das der Nutzer nie gesehen und dessen Kurs und
# PnL er nie bestaetigt hat - dieselbe Abwaegung wie beim geschriebenen Kurs
# (siehe Modul-Kopf): still mehr zu tun als bestaetigt wurde, waere die
# groessere Ueberraschung. Sie bleibt offen, wird im Ergebnis ausdruecklich
# ausgewiesen, und ein zweiter Durchlauf erfasst sie.

def alle_vorbereiten(bot_name: str, kurse: dict) -> dict:
    """Notfallweg, Aufruf 1. Uebersicht ALLER offenen Positionen samt
    Kursen und PnL-Schaetzung, plus eine Vorgangs-Kennung. Schreibt nichts.
    """
    if not ist_freigeschaltet(bot_name):
        raise SchliessenNichtMoeglich(
            f"Fuer '{bot_name}' ist das manuelle Schliessen nicht freigeschaltet. "
            f"Freigeschaltet: {', '.join(freigeschaltete_bots())}.")

    offen = manual_close.offene_positionen(bot_name)
    if not offen:
        raise SchliessenNichtMoeglich(
            "Dieser Bot hat gerade keine offene Position. Es gibt nichts zu "
            "schliessen.")

    kurse = kurse or {}
    zeilen, schliessbar = [], []
    for position in offen:
        kurs = kurse.get(position["symbol"])
        kurs = float(kurs) if kurs else None
        pnl = None
        if kurs and position.get("entry_price"):
            pnl = manual_close.berechne_pnl(bot_name, position["entry_price"], kurs)
        # Ohne Kurs oder ohne Einstiegskurs wuerde der Kern ablehnen. Solche
        # Positionen werden deshalb hier schon als nicht schliessbar
        # ausgewiesen, statt sie mitzuzaehlen und spaeter als Fehlschlag zu
        # melden - der Nutzer soll vorher wissen, was er bestaetigt.
        grund = None
        if not kurs:
            grund = "kein aktueller Kurs verfuegbar"
        elif not position.get("entry_price"):
            grund = "Einstiegskurs fehlt in der Datenbank"
        eintrag = {
            "id": position["id"],
            "symbol": position["symbol"],
            "entry_time": position.get("entry_time"),
            "entry_preis": _gerundet(position.get("entry_price")),
            "aktueller_preis": _gerundet(kurs),
            "pnl_pct": pnl,
            "schliessbar_jetzt": grund is None,
            "grund": grund,
        }
        zeilen.append(eintrag)
        if grund is None:
            schliessbar.append((position["id"], position["symbol"], kurs))

    if not schliessbar:
        raise SchliessenNichtMoeglich(
            "Von keiner der offenen Positionen liegt ein verwertbarer Kurs "
            "vor. Ohne Ausstiegskurs wird nicht geschrieben - bitte spaeter "
            "erneut versuchen.")

    _aufraeumen()
    if len(_VORGAENGE) >= MAX_VORGAENGE:
        raise SchliessenNichtMoeglich(
            "Zu viele offene Bestaetigungen. Bitte kurz warten, bis die "
            "aelteren abgelaufen sind.")

    kennung = secrets.token_urlsafe(24)
    _VORGAENGE[kennung] = Vorgang({
        "kennung": kennung,
        "art": ART_ALLE,
        "bot": bot_name,
        # Nur die ID wuerde genuegen, um zu schliessen. Symbol und Kurs
        # stehen mit dabei, weil GENAU DIESER Kurs geschrieben wird - der,
        # den der Nutzer in der Uebersicht gesehen hat, je Position ein
        # eigener. Nicht ein einziger Kurs fuer alle, und kein beim
        # Ausfuehren neu geholter.
        "positionen": schliessbar,
        "trade_id": None,
        "gueltig_bis": _jetzt() + GUELTIG_SEKUNDEN,
    })
    logger.info(f"Notfall-Schliessvorgang vorbereitet: Bot {bot_name}, "
                f"{len(schliessbar)} Positionen "
                f"({', '.join(s for _, s, _ in schliessbar)}) - noch nichts "
                f"geschrieben.")

    werte = [z["pnl_pct"] for z in zeilen if z["pnl_pct"] is not None]
    return {
        "vorgang": kennung,
        "bot": bot_name,
        "anzeigename": manual_close.SCHLIESSBARE_BOTS[bot_name]["anzeigename"],
        "positionen": zeilen,
        "anzahl": len(schliessbar),
        "anzahl_gesamt": len(zeilen),
        # KEINE Summe der Prozente. Die waere keine Portfolio-Rendite,
        # sondern eine Zahl ohne Bedeutung - in diesem Projekt eine
        # mehrfach aufgetretene Fehlerquelle und als Methodik-Grundsatz im
        # Uebergabeprotokoll (Abschnitt 7, Punkt 2) ausdruecklich
        # festgehalten. Belastbar waere nur eine Rechnung ueber die
        # Positionsgroesse, und die steht als Backtest-Annahme in
        # equity_simulation.py - sie hier hereinzuziehen hiesse, eine
        # Backtest-Groesse als Live-Aussage auszugeben. Deshalb: der
        # Durchschnitt je Position, dazu bestes und schlechtestes Ergebnis.
        "pnl_schnitt_pct": round(sum(werte) / len(werte), 2) if werte else None,
        "pnl_bestes_pct": max(werte) if werte else None,
        "pnl_schlechtestes_pct": min(werte) if werte else None,
        "gueltig_sekunden": GUELTIG_SEKUNDEN,
    }


def alle_ausfuehren(bot_name: str, kennung, benutzer) -> dict:
    """Notfallweg, Aufruf 2 - schliesst jede bestaetigte Position EINZELN.

    Geschlossen wird ueber manual_close.schliesse_position(), dieselbe
    Funktion wie beim Einzelweg und damit mit derselben Transaktion, der
    erneuten Pruefung innerhalb der Transaktion, derselben PnL-Formel und
    einer eigenen Protokollzeile je Position. Hier steht KEINE zweite
    Schreiblogik - nur eine Schleife darum.

    TEILAUSFALL: Scheitert eine Position, laeuft die Schleife weiter. Ein
    Abbruch in der Mitte waere das Schlimmste, was diese Funktion tun
    koennte - er hinterliesse einen Zustand, den niemand benennen kann
    ("sind 2 oder 3 geschlossen?"). Jeder Fehlschlag wird einzeln
    festgehalten und am Ende vollstaendig ausgewiesen.
    """
    vorgang = _vorgang_einloesen(bot_name, kennung, benutzer, ART_ALLE)
    bestaetigt = list(vorgang["positionen"])

    # NEU LESEN, nicht die bestaetigte Liste abarbeiten: zwischen Uebersicht
    # und Tap koennen bis zu GUELTIG_SEKUNDEN liegen, und der Cronjob
    # arbeitet in dieser Zeit weiter.
    noch_offen = {p["id"] for p in manual_close.offene_positionen(bot_name)}

    geschlossen, fehlgeschlagen, uebersprungen = [], [], []

    for trade_id, symbol, kurs in bestaetigt:
        if trade_id not in noch_offen:
            # Kein Fehlschlag, sondern ein Nicht-Ereignis: der Bot hat die
            # Position regulaer selbst geschlossen. Es wird GAR NICHT
            # versucht - ein Versuch wuerde bloss eine Ablehnung ins
            # Protokoll schreiben, die nichts bedeutet.
            uebersprungen.append({
                "trade_id": trade_id, "symbol": symbol,
                "grund": ("war beim Ausfuehren nicht mehr offen - der Bot hat "
                           "sie selbst geschlossen"),
            })
            continue
        try:
            ergebnis = manual_close.schliesse_position(
                bot_name, trade_id, kurs, benutzer, BESTAETIGUNGSTEXT,
                quelle=manual_close.QUELLE_DASHBOARD)
        except SchliessenNichtMoeglich as fehler:
            # Weitermachen. Der Kern hat diese Ablehnung bereits einzeln
            # protokolliert und garantiert, dass nichts geschrieben wurde.
            fehlgeschlagen.append({
                "trade_id": trade_id, "symbol": symbol, "grund": str(fehler),
            })
            logger.warning(f"Notfall-Schliessen: Trade {trade_id} ({symbol}) "
                           f"fehlgeschlagen, Schleife laeuft weiter - {fehler}")
            continue
        except Exception as fehler:      # noqa: BLE001 - siehe Begruendung
            # Auch ein UNERWARTETER Fehler darf die Schleife nicht
            # abbrechen; sonst haette genau der Fall, den niemand vorhergesehen
            # hat, die schlimmste Folge. Der Kern schreibt nur innerhalb
            # einer Transaktion, ein Fehler laesst die Zeile also unberuehrt.
            manual_close.protokolliere_ablehnung(
                bot_name, trade_id, benutzer,
                f"unerwarteter Fehler beim Notfall-Schliessen: {fehler}",
                manual_close.QUELLE_DASHBOARD)
            fehlgeschlagen.append({
                "trade_id": trade_id, "symbol": symbol,
                "grund": f"unerwarteter Fehler: {fehler}",
            })
            logger.exception(f"Notfall-Schliessen: unerwarteter Fehler bei "
                             f"Trade {trade_id} ({symbol}) - Schleife laeuft weiter.")
            continue
        geschlossen.append({
            "trade_id": ergebnis["trade_id"],
            "symbol": ergebnis["symbol"],
            "entry_preis": _gerundet(ergebnis["entry_price"]),
            "exit_preis": _gerundet(ergebnis["exit_price"]),
            "exit_time": ergebnis["exit_time"],
            "pnl_pct": ergebnis["pnl_pct"],
            "ergebnis": ergebnis["result"],
        })

    # Positionen, die der Bot NACH der Uebersicht eroeffnet hat: nicht
    # angefasst, aber ausgewiesen (siehe Begruendung oben).
    bestaetigte_ids = {t for t, _, _ in bestaetigt}
    nicht_bestaetigt = sorted(noch_offen - bestaetigte_ids)

    werte = [g["pnl_pct"] for g in geschlossen if g["pnl_pct"] is not None]
    ergebnis = {
        "erfolg": not fehlgeschlagen,
        "bot": bot_name,
        "angefragt": len(bestaetigt),
        "geschlossen": geschlossen,
        "fehlgeschlagen": fehlgeschlagen,
        "uebersprungen": uebersprungen,
        "nicht_bestaetigt": nicht_bestaetigt,
        "anzahl_geschlossen": len(geschlossen),
        "anzahl_fehlgeschlagen": len(fehlgeschlagen),
        "anzahl_uebersprungen": len(uebersprungen),
        "pnl_schnitt_pct": round(sum(werte) / len(werte), 2) if werte else None,
    }
    ergebnis["meldung"] = _alle_meldung(ergebnis)
    logger.info(f"Notfall-Schliessen beendet: {ergebnis['meldung']}")
    return ergebnis


def _alle_meldung(ergebnis: dict) -> str:
    """Ein Satz, der den Ausgang vollstaendig nennt - auch den unschoenen.
    Bewusst KEIN blosses "erfolgreich": ein Teilausfall, der sich wie ein
    Erfolg liest, ist schlimmer als eine Fehlermeldung."""
    teile = [f"{ergebnis['anzahl_geschlossen']} von {ergebnis['angefragt']} "
             f"Positionen geschlossen"]
    if ergebnis["anzahl_fehlgeschlagen"]:
        namen = ", ".join(f"{f['symbol']} ({f['grund']})"
                           for f in ergebnis["fehlgeschlagen"])
        teile.append(f"{ergebnis['anzahl_fehlgeschlagen']} fehlgeschlagen: {namen}")
    if ergebnis["anzahl_uebersprungen"]:
        namen = ", ".join(u["symbol"] for u in ergebnis["uebersprungen"])
        teile.append(f"{ergebnis['anzahl_uebersprungen']} uebersprungen, weil "
                      f"der Bot sie selbst geschlossen hatte: {namen}")
    if ergebnis["nicht_bestaetigt"]:
        teile.append(f"{len(ergebnis['nicht_bestaetigt'])} Position(en) wurden "
                      f"erst nach der Uebersicht eroeffnet und NICHT angefasst "
                      f"(IDs {', '.join(str(i) for i in ergebnis['nicht_bestaetigt'])})")
    satz = "; ".join(teile) + "."
    if ergebnis["anzahl_geschlossen"]:
        satz += (" Jeder Eingriff steht einzeln im Protokoll "
                 "logs/notifications/manuelle_eingriffe.log.")
    return satz

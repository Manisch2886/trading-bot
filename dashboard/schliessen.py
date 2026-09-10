"""
Die EINE schreibende Faehigkeit des Dashboards
==============================================================================
Bis zu diesem Modul war das Dashboard ausschliesslich lesend (siehe den
Docstring von app.py und den Nachweis in test_dashboard.py). Hier kommt
genau eine Faehigkeit hinzu: offene Positionen von Hand schliessen - in drei
Abstufungen, alle abgesichert ueber zwei getrennte Server-Aufrufe:

  EINZELN   eine Position eines Bots      EIN Tap
  ALLE      alle Positionen EINES Bots    ZWEI Klicks
  GLOBAL    alle Positionen ALLER Bots    ZWEI Klicks + Text "CRASH"

Freigeschaltet sind alle neun Bots (siehe manual_close.SCHLIESSBARE_BOTS und
die Einzelpruefung je Bot im Testabschnitt 9).

Alle drei schreiben ausschliesslich ueber `manual_close.schliesse_position()`
- je Position ein Aufruf, auch die beiden Sammelwege. Dort steht keine
Schleife und hier keine Schreiblogik. Der globale Weg ruft dafuer genau die
Schleife auf, die der bot-weite Weg benutzt (`_bot_abarbeiten`), nicht eine
dritte Fassung davon.

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

AKTIEN-BOTS UND HANDELSZEITEN - ein Befund, der festgehalten gehoert:
Die vier Aktien-Bots holen ihre Kurse per yfinance, und zwar den LETZTEN
VERFUEGBAREN TAGES-SCHLUSSKURS (siehe monitor.fetch_stock_prices). Ausserhalb
der US-Handelszeiten ist das der Schluss des letzten Handelstags - es kommt
also ein Kurs zurueck, und damit erscheint der Schliessen-Knopf AUCH dann.
Die Annahme "kein Kurs, kein Knopf fuehrt ausserhalb der Handelszeiten
automatisch zu keinem Knopf" trifft NICHT zu; in monitor.py gibt es keinerlei
Handelszeit-Logik.

Inhaltlich ist das vertretbar: die Aktien-Bots arbeiten selbst auf
Tages-Kerzen und schliessen zum Tages-Schluss - ein manueller Ausstieg zu
genau diesem Kurs weicht also nicht von dem ab, was der Bot getan haette.
Verschwiegen werden darf es aber nicht, deshalb wird `anlageklasse`
mitgeliefert und das Frontend weist bei Aktien-Bots darauf hin. Eine echte
Sperre nach Handelszeiten waere eine Verhaltensaenderung mit eigenen
Fallstricken (Zeitzonen, Feiertage, Halbtage) und ist bewusst NICHT
eingebaut - das waere eine eigene Entscheidung.

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
ART_GLOBAL = "global"

# Der globale Crash-Weg verlangt diesen Text zusaetzlich zu zwei Klicks.
#
# Beim Einzel- und beim bot-weiten Weg wurde die Texteingabe bewusst
# entfernt, weil sie dort nicht die Absicherung war und nur Zeit kostete.
# Hier kommt sie genauso bewusst zurueck, und zwar nicht als Sicherung gegen
# einen Angreifer - gegen den hilft wie immer nur die Vorgangs-Kennung -,
# sondern gegen den eigenen Reflex: dieser eine Klick schliesst JEDE offene
# Position ALLER neun Bots. Ein Wort tippen zu muessen erzwingt eine
# Sekunde, in der man es sich anders ueberlegen kann. Das ist der einzige
# Zweck, und deshalb steht der Text auch hier und nicht im Kern.
#
# Verglichen wird case-SENSITIV (nur umschliessende Leerzeichen fallen weg) -
# "crash" reicht nicht.
CRASH_TEXT = "CRASH"

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
        "anlageklasse": manual_close.SCHLIESSBARE_BOTS[bot_name]["anlageklasse"],
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
        "anlageklasse": manual_close.SCHLIESSBARE_BOTS[bot_name]["anlageklasse"],
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
        "anlageklasse": manual_close.SCHLIESSBARE_BOTS[bot_name]["anlageklasse"],
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
    ergebnis = _bot_abarbeiten(bot_name, vorgang["positionen"], benutzer,
                                manual_close.QUELLE_DASHBOARD)
    ergebnis["meldung"] = _alle_meldung(ergebnis)
    logger.info(f"Notfall-Schliessen beendet: {ergebnis['meldung']}")
    return ergebnis


def _bot_abarbeiten(bot_name: str, bestaetigt, benutzer, quelle: str) -> dict:
    """Schliesst die bestaetigten Positionen EINES Bots, je Position ein
    Aufruf von manual_close.schliesse_position().

    DIE Schleife des Projekts: `alle_ausfuehren()` (ein Bot) und
    `global_ausfuehren()` (alle Bots) rufen beide genau diese Funktion auf.
    Eine zweite Fassung fuer den globalen Weg waere eine dritte
    Schreiblogik - und damit die Stelle, an der die Teilausfall-Sicherheit
    irgendwann nur noch auf einem der beiden Wege gelten wuerde.

    `quelle` landet im Protokoll und unterscheidet, woraus der Eingriff kam
    (bot-weiter Notfallweg oder globaler Crash-Weg).

    bestaetigt: Liste von (trade_id, symbol, kurs) aus dem Vorgang.
    """
    bestaetigt = list(bestaetigt)

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
                quelle=quelle)
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
                quelle)
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


# ---------------------------------------------------------------------------
# Globaler Crash-Weg: ALLE offenen Positionen ALLER freigeschalteten Bots
# ---------------------------------------------------------------------------
# Die folgenreichste Aktion des Projekts: ein Klick kann jede offene Position
# aller neun Bots schliessen. Deshalb drei Stufen statt zwei, und die dritte
# ist eine Texteingabe (siehe CRASH_TEXT oben).
#
# SCHREIBEN tut dieser Weg trotzdem keine Zeile selbst: er ruft je Bot
# `_bot_abarbeiten()` auf - genau die Schleife, die auch der bot-weite
# Notfallweg benutzt -, und die ruft je Position
# `manual_close.schliesse_position()`. Drei Oberflaechen-Abstufungen, EIN
# Schreibpfad.
#
# TEILAUSFALL IN ZWEI DIMENSIONEN, und beide muessen ueberlebt werden:
#
#   innerhalb eines Bots   eine Position scheitert -> `_bot_abarbeiten`
#                          laeuft mit den uebrigen weiter (unveraendert)
#   ein ganzer Bot         seine Datenbank fehlt, ist gesperrt oder
#                          antwortet nicht -> DIESE Funktion macht mit den
#                          uebrigen BOTS weiter
#
# Die zweite ist die neue und die unangenehmere: ein Abbruch beim dritten von
# neun Bots hinterliesse einen Zustand, den niemand benennen kann. Deshalb
# steht der Aufruf je Bot in einem eigenen try/except, und das Ergebnis weist
# gescheiterte Bots getrennt von gescheiterten Positionen aus.

# Platzhalter-Botname fuer den globalen Vorgang. Der Vorgangsspeicher ist
# derselbe wie bei den anderen beiden Wegen, und `_vorgang_einloesen()`
# vergleicht den Bot - ein Name, der zu keinem echten Bot gehoert, haelt die
# Pruefung damit ohne Sonderfall aufrecht und liest im Protokoll besser als
# None.
GLOBAL_LABEL = "alle-bots"


def _bot_uebersicht(bot_name: str, kurse: dict) -> tuple:
    """Offene Positionen EINES Bots fuer die globale Uebersicht.

    Rueckgabe: (anzeige_dict, schliessbar_liste). Wirft NICHT - ein Bot, der
    sich nicht lesen laesst, darf die Uebersicht der uebrigen nicht
    verhindern; er wird als nicht lesbar ausgewiesen.
    """
    angaben = manual_close.SCHLIESSBARE_BOTS[bot_name]
    anzeige = {
        "bot": bot_name,
        "anzeigename": angaben["anzeigename"],
        "anlageklasse": angaben["anlageklasse"],
        "positionen": [],
        "anzahl": 0,
        "anzahl_gesamt": 0,
        "pnl_schnitt_pct": None,
        "pnl_bestes_pct": None,
        "pnl_schlechtestes_pct": None,
        "lesefehler": None,
    }
    # Eine FEHLENDE Datenbank ist kein Lesefehler, sondern heisst "dieser Bot
    # hat noch nie gelaufen" - etwa auf einer Installation ohne die
    # Aktien-Bots. Sie gehoert deshalb nicht als Warnung in die Uebersicht;
    # sonst stuenden dort im Crash-Fall mehrere rote Zeilen, die nichts
    # bedeuten, und die echten Lesefehler gingen darin unter. Unterschieden
    # wird hier bewusst VOR dem Lesen: danach sehen beide Faelle gleich aus.
    if not os.path.exists(manual_close._pfade(bot_name)["db"]):
        return anzeige, []

    try:
        offen = manual_close.offene_positionen(bot_name)
    except Exception as fehler:          # noqa: BLE001 - siehe Docstring
        anzeige["lesefehler"] = str(fehler)
        logger.warning(f"Globale Uebersicht: {bot_name} nicht lesbar - {fehler}")
        return anzeige, []

    schliessbar = []
    for position in offen:
        kurs = (kurse or {}).get(position["symbol"])
        kurs = float(kurs) if kurs else None
        pnl = None
        grund = None
        if not kurs:
            grund = "kein aktueller Kurs verfuegbar"
        elif not position.get("entry_price"):
            grund = "Einstiegskurs fehlt in der Datenbank"
        else:
            pnl = manual_close.berechne_pnl(bot_name, position["entry_price"], kurs)
        anzeige["positionen"].append({
            "id": position["id"],
            "symbol": position["symbol"],
            "entry_time": position.get("entry_time"),
            "entry_preis": _gerundet(position.get("entry_price")),
            "aktueller_preis": _gerundet(kurs),
            "pnl_pct": pnl,
            "schliessbar_jetzt": grund is None,
            "grund": grund,
        })
        if grund is None:
            schliessbar.append((position["id"], position["symbol"], kurs))

    werte = [p["pnl_pct"] for p in anzeige["positionen"] if p["pnl_pct"] is not None]
    anzeige["anzahl"] = len(schliessbar)
    anzeige["anzahl_gesamt"] = len(anzeige["positionen"])
    if werte:
        # Durchschnitt JE BOT, keine Summe und erst recht keine Gesamtsumme
        # ueber alle Bots: die Summe von Trade-Prozenten ist keine
        # Portfolio-Rendite (Methodik-Grundsatz 2 im Uebergabeprotokoll).
        # Eine grosse Gesamtzahl ueber neun Bots waere die irrefuehrendste
        # Zahl, die dieses Dashboard anzeigen koennte - gerade in dem Moment,
        # in dem jemand im Crash-Fall schnell entscheiden will.
        anzeige["pnl_schnitt_pct"] = round(sum(werte) / len(werte), 2)
        anzeige["pnl_bestes_pct"] = max(werte)
        anzeige["pnl_schlechtestes_pct"] = min(werte)
    return anzeige, schliessbar


def global_vorbereiten(kurse: dict) -> dict:
    """Crash-Weg, Aufruf 1. Uebersicht ALLER offenen Positionen ALLER
    freigeschalteten Bots, nach Bot gruppiert. Schreibt nichts."""
    bots, je_bot = [], {}
    for bot_name in sorted(manual_close.SCHLIESSBARE_BOTS):
        # Sortiert, damit Reihenfolge, Protokoll und Zusammenfassung
        # reproduzierbar sind - bei neun Bots ist "irgendeine Reihenfolge"
        # sonst bei jeder Fehlersuche eine Variable zu viel.
        anzeige, schliessbar = _bot_uebersicht(bot_name, kurse)
        if anzeige["anzahl_gesamt"] == 0 and not anzeige["lesefehler"]:
            continue                      # dieser Bot hat gerade nichts offen
        bots.append(anzeige)
        if schliessbar:
            je_bot[bot_name] = schliessbar

    if not bots:
        raise SchliessenNichtMoeglich(
            "Kein Bot hat gerade eine offene Position. Es gibt nichts zu "
            "schliessen.")
    if not je_bot:
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
        "art": ART_GLOBAL,
        "bot": GLOBAL_LABEL,
        "trade_id": None,
        "positionen_je_bot": je_bot,
        "gueltig_bis": _jetzt() + GUELTIG_SEKUNDEN,
    })
    anzahl = sum(len(p) for p in je_bot.values())
    logger.info(f"GLOBALER Schliessvorgang vorbereitet: {anzahl} Positionen in "
                f"{len(je_bot)} Bots ({', '.join(sorted(je_bot))}) - noch "
                f"nichts geschrieben.")

    return {
        "vorgang": kennung,
        "bots": bots,
        "anzahl": anzahl,
        "anzahl_gesamt": sum(b["anzahl_gesamt"] for b in bots),
        "anzahl_bots": len(je_bot),
        "bots_mit_lesefehler": [b["bot"] for b in bots if b["lesefehler"]],
        # Der Text wird dem Frontend bewusst MITGETEILT - anders als beim
        # frueheren Einzelweg, wo er versteckt und damit sinnlos war. Hier
        # ist er kein Geheimnis, sondern eine Huerde: der Nutzer soll lesen
        # koennen, was er tippen muss.
        "crash_text": CRASH_TEXT,
        "gueltig_sekunden": GUELTIG_SEKUNDEN,
    }


def global_ausfuehren(kennung, bestaetigung, benutzer) -> dict:
    """Crash-Weg, Aufruf 2 - schliesst in JEDEM Bot jede bestaetigte
    Position EINZELN, ueber `_bot_abarbeiten()` je Bot.

    Scheitert ein ganzer Bot, laufen die uebrigen weiter; scheitert eine
    Position, laufen die uebrigen Positionen dieses Bots weiter. Das
    Ergebnis weist beides getrennt aus.
    """
    vorgang = _vorgang_einloesen(GLOBAL_LABEL, kennung, benutzer, ART_GLOBAL)

    # Der Text wird NACH dem Einloesen geprueft, also nachdem die Kennung
    # verbraucht ist: ein falscher Versuch darf nicht beliebig oft
    # wiederholbar sein, sonst waere die Huerde keine.
    if (bestaetigung or "").strip() != CRASH_TEXT:
        manual_close.protokolliere_ablehnung(
            GLOBAL_LABEL, None, benutzer,
            "falscher Bestaetigungstext beim globalen Schliessen",
            manual_close.QUELLE_DASHBOARD_CRASH)
        raise SchliessenNichtMoeglich(
            f"Der Bestaetigungstext stimmt nicht - erwartet wird genau "
            f"'{CRASH_TEXT}', Gross-/Kleinschreibung inbegriffen. Es wurde "
            f"nichts geaendert; bitte von vorn beginnen.")

    je_bot = dict(vorgang["positionen_je_bot"])
    logger.warning(f"GLOBALES Schliessen beginnt: {len(je_bot)} Bots, "
                   f"{sum(len(p) for p in je_bot.values())} bestaetigte "
                   f"Positionen, ausgeloest von {benutzer}.")

    ergebnisse, bot_fehler = [], []
    for bot_name in sorted(je_bot):
        try:
            teil = _bot_abarbeiten(bot_name, je_bot[bot_name], benutzer,
                                    manual_close.QUELLE_DASHBOARD_CRASH)
        except Exception as fehler:      # noqa: BLE001 - siehe Modul-Abschnitt
            # EIN GANZER BOT ist ausgefallen (Datenbank fehlt, gesperrt,
            # unlesbar). Die uebrigen Bots laufen weiter - ein Abbruch hier
            # waere der Zustand, den niemand mehr benennen kann.
            manual_close.protokolliere_ablehnung(
                bot_name, None, benutzer,
                f"Bot komplett uebersprungen beim globalen Schliessen: {fehler}",
                manual_close.QUELLE_DASHBOARD_CRASH)
            bot_fehler.append({
                "bot": bot_name,
                "anzeigename": manual_close.SCHLIESSBARE_BOTS[bot_name]["anzeigename"],
                "grund": str(fehler),
                "angefragt": len(je_bot[bot_name]),
            })
            logger.exception(f"GLOBALES Schliessen: Bot {bot_name} komplett "
                             f"ausgefallen - die uebrigen laufen weiter.")
            continue
        teil["anzeigename"] = manual_close.SCHLIESSBARE_BOTS[bot_name]["anzeigename"]
        teil["meldung"] = _alle_meldung(teil)
        ergebnisse.append(teil)

    gesamt_geschlossen = sum(e["anzahl_geschlossen"] for e in ergebnisse)
    gesamt_fehlgeschlagen = sum(e["anzahl_fehlgeschlagen"] for e in ergebnisse)
    gesamt_uebersprungen = sum(e["anzahl_uebersprungen"] for e in ergebnisse)
    gesamt_angefragt = sum(len(p) for p in je_bot.values())

    ergebnis = {
        "erfolg": not gesamt_fehlgeschlagen and not bot_fehler,
        "angefragt": gesamt_angefragt,
        "angefragte_bots": len(je_bot),
        "bots": ergebnisse,
        "bots_fehlgeschlagen": bot_fehler,
        "anzahl_geschlossen": gesamt_geschlossen,
        "anzahl_fehlgeschlagen": gesamt_fehlgeschlagen,
        "anzahl_uebersprungen": gesamt_uebersprungen,
        # KEIN Gesamt-PnL ueber alle Bots - siehe _bot_uebersicht().
        # Der Durchschnitt je Bot steht in den einzelnen Eintraegen.
    }
    ergebnis["meldung"] = _global_meldung(ergebnis)
    logger.warning(f"GLOBALES Schliessen beendet: {ergebnis['meldung']}")
    return ergebnis


def _global_meldung(ergebnis: dict) -> str:
    """Ein Satz, der den Ausgang ueber alle Bots vollstaendig nennt."""
    teile = [f"{ergebnis['anzahl_geschlossen']} von {ergebnis['angefragt']} "
             f"Positionen in {ergebnis['angefragte_bots']} Bots geschlossen"]
    if ergebnis["anzahl_fehlgeschlagen"]:
        teile.append(f"{ergebnis['anzahl_fehlgeschlagen']} Position(en) "
                      f"fehlgeschlagen")
    if ergebnis["bots_fehlgeschlagen"]:
        namen = ", ".join(f"{b['bot']} ({b['grund']})"
                           for b in ergebnis["bots_fehlgeschlagen"])
        teile.append(f"{len(ergebnis['bots_fehlgeschlagen'])} Bot(s) komplett "
                      f"uebersprungen: {namen}")
    if ergebnis["anzahl_uebersprungen"]:
        teile.append(f"{ergebnis['anzahl_uebersprungen']} Position(en) "
                      f"uebersprungen, weil der jeweilige Bot sie selbst "
                      f"geschlossen hatte")
    nachtraeglich = sum(len(e["nicht_bestaetigt"]) for e in ergebnis["bots"])
    if nachtraeglich:
        teile.append(f"{nachtraeglich} Position(en) wurden erst nach der "
                      f"Uebersicht eroeffnet und NICHT angefasst")
    satz = "; ".join(teile) + "."
    if ergebnis["anzahl_geschlossen"]:
        satz += (" Jeder Eingriff steht einzeln im Protokoll "
                 "logs/notifications/manuelle_eingriffe.log, erkennbar an "
                 f"quelle={manual_close.QUELLE_DASHBOARD_CRASH}.")
    return satz

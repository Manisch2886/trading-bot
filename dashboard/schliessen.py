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

Alle drei koennen seit PR #69 auch einen VIERTEN Ausgang haben, der gar
nichts schreibt: ist die Boerse geschlossen und der Bot ein Aktien-Bot,
entsteht statt des Ausstiegs ein Warteauftrag (siehe Abschnitt
"Boersenzeiten"). Welcher der beiden Ausgaenge gilt, entscheidet der Server
aus dem Kalender - nicht der Aufrufer.

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
  3. die Uebersetzung in JSON-taugliche Werte,
  4. die Kennzahlen der Anzeige - Durchschnitt, Spannweite und der nach
     Positionsgroesse GEWICHTETE Durchschnitt (siehe gewichteter_pnl()),
     in allen drei Abstufungen aus derselben Funktion.
     Anzeigelogik, kein Schreibweg; die Positionsgroesse selbst wird nicht
     hier gefuehrt, sondern je Bot aus dessen eigenen Dateien gelesen
     (manual_close.allokation()).

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

AKTIEN-BOTS UND HANDELSZEITEN - hier stand bis PR #66 das Gegenteil:
Die vier Aktien-Bots holen ihre Kurse per yfinance, und zwar den LETZTEN
VERFUEGBAREN TAGES-SCHLUSSKURS (siehe monitor.fetch_stock_prices). Ausserhalb
der US-Handelszeiten ist das der Schluss des letzten Handelstags - es kommt
also ein Kurs zurueck, und damit erschien der Schliessen-Knopf AUCH dann.
Die Annahme "kein Kurs, kein Knopf fuehrt ausserhalb der Handelszeiten
automatisch zu keinem Knopf" trifft NICHT zu; in monitor.py gibt es keinerlei
Handelszeit-Logik.

An dieser Stelle stand dazu, eine echte Handelszeiten-Sperre sei "bewusst
NICHT eingebaut", weil Zeitzonen, Feiertage und Halbtage eigene Fallstricke
waeren. Der Befund war richtig, die Folgerung nicht: geschlossen wurde damit
zu einem Kurs, den es "gerade jetzt" gar nicht gibt - ueber ein Wochenende
zweieinhalb Tage alt, ueber Ostern vier.

JETZT GILT: bei geschlossener Boerse wird die Position NICHT sofort
geschlossen, sondern als WARTEAUFTRAG vorgemerkt und automatisch zum
naechsten echten Kurs geschlossen, sobald die Boerse wieder oeffnet (siehe
den Abschnitt "Boersenzeiten" weiter unten, notifications/boersenkalender.py
und dashboard/warteauftraege_ausfuehren.py). Die drei genannten Fallstricke
sind nicht verschwunden - sie sind der Grund, warum ein echter
Boersenkalender benutzt wird und keine Zeitregel.

KRYPTO IST DAVON NICHT BETROFFEN. Binance handelt rund um die Uhr; dort
bleibt alles wie bisher, sofort und zum aktuellen Kurs.

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
import boersenkalender  # noqa: E402
import warteauftraege  # noqa: E402

logger = logging.getLogger("dashboard.schliessen")

WarteauftragNichtMoeglich = warteauftraege.WarteauftragNichtMoeglich

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


# ---------------------------------------------------------------------------
# Boersenzeiten: sofort schliessen oder vormerken?
# ---------------------------------------------------------------------------
# Hier stand bis PR #66 ausdruecklich das Gegenteil: eine Handelszeit-Sperre
# sei "bewusst NICHT eingebaut", weil Zeitzonen, Feiertage und Halbtage eigene
# Fallstricke waeren. Der Befund selbst war richtig und steht weiter oben im
# Modul-Kopf - was fehlte, war die Folgerung. Ein Aktien-Ausstieg ausserhalb
# der Handelszeiten wurde zum Schluss des LETZTEN Handelstags geschrieben,
# also zu einem Kurs, den es "gerade jetzt" nicht gibt. Bei einem Wochenende
# sind das zweieinhalb Tage Kursbewegung, ueber Ostern vier.
#
# Die drei genannten Fallstricke sind nicht verschwunden - sie sind der Grund,
# warum die Entscheidung jetzt an einem ECHTEN Kalender haengt und nicht an
# einer Zeitregel (siehe notifications/boersenkalender.py).
#
# DREI Zustaende, nicht zwei. Der dritte ist der wichtigste:
#
#   offen          -> sofort schliessen, unveraendert wie bisher
#   geschlossen    -> Warteauftrag, nach zusaetzlicher Bestaetigung
#   UNBEKANNT      -> WEDER noch. Kein Schreibzugriff, kein Auftrag.
#
# "Unbekannt" tritt ein, wenn die Kalender-Bibliothek fehlt oder stolpert.
# Ein Warteauftrag waere dann eine Absichtserklaerung, die niemand einloesen
# koennte - das Ausfuehrungsskript haengt am selben Kalender und wuerde ihn
# nie anfassen. Der Auftrag saehe aus wie ein Auftrag und waere ein
# Stillstand. Deshalb wird abgelehnt und die Ursache benannt.

# Der Nutzer muss den zusaetzlichen Warnschritt ausdruecklich bestaetigen,
# bevor ein Warteauftrag entsteht. Der Wert kommt als eigenes Feld in der
# Anfrage und wird SERVERSEITIG geprueft - genau wie beim CRASH-Text: ein
# Dialog im Browser ist eine Hoeflichkeit, keine Absicherung.
#
# Warum ueberhaupt eine zweite Bestaetigung, wo doch die Vorgangs-Kennung
# schon vorliegt: die Kennung belegt, dass jemand "schliessen" wollte. Sie
# belegt NICHT, dass er verstanden hat, dass daraus eine Ausfuehrung ohne
# erneute Rueckfrage wird - moeglicherweise erst am naechsten Werktag. Genau
# das ist die neue Eigenschaft, und genau die wird hier bestaetigt.
WARTEAUFTRAG_BESTAETIGUNG = "warteauftrag_bestaetigt"


def boersenlage(anlageklasse: str, jetzt=None) -> dict:
    """Was fuer diese Anlageklasse GERADE gilt.

    Krypto laeuft hier bewusst mit durch, statt an jeder Aufrufstelle
    uebersprungen zu werden: eine Fallunterscheidung, die an neun Stellen
    wiederholt wird, ist neunmal die Gelegenheit, sie einmal zu vergessen.
    Fuer Krypto ist die Antwort schlicht immer "handelbar".
    """
    if anlageklasse != "aktien":
        return {
            "anlageklasse": anlageklasse,
            "kalender_gilt": False,
            "offen": None,
            "handelbar_jetzt": True,
            "warteauftrag_noetig": False,
            "unbekannt": False,
            "kalender": None,
            "grund": ("Krypto wird rund um die Uhr gehandelt - es gibt keine "
                       "Handelszeiten und deshalb nichts vorzumerken."),
            "letzter_handelstag": None,
            "letzter_schluss": None,
            "naechste_oeffnung": None,
            "naechster_schluss": None,
            "verkuerzter_handelstag": None,
        }

    zustand = boersenkalender.status(jetzt)
    offen = zustand["offen"]
    return {
        "anlageklasse": "aktien",
        "kalender_gilt": True,
        "offen": offen,
        "handelbar_jetzt": offen is True,
        "warteauftrag_noetig": offen is False,
        "unbekannt": offen is None,
        "kalender": zustand["kalender"],
        "grund": zustand["grund"],
        "letzter_handelstag": zustand["letzter_handelstag"],
        "letzter_schluss": zustand["letzter_schluss"],
        "naechste_oeffnung": zustand["naechste_oeffnung"],
        "naechster_schluss": zustand["naechster_schluss"],
        "verkuerzter_handelstag": zustand["verkuerzter_handelstag"],
    }


def lage_fuer_bot(bot_name: str, jetzt=None) -> dict:
    angaben = manual_close.SCHLIESSBARE_BOTS.get(bot_name) or {}
    return boersenlage(angaben.get("anlageklasse"), jetzt)


def _pruefe_kalender_bekannt(lage: dict) -> None:
    """Wirft, wenn der Kalender keine Auskunft gibt. Aufrufer, die danach
    schreiben oder vormerken wuerden, tun dann keines von beidem."""
    if lage.get("unbekannt"):
        raise SchliessenNichtMoeglich(
            f"Der Boersenkalender gibt gerade keine Auskunft, ob die Boerse "
            f"offen ist. Es wird deshalb weder sofort geschlossen noch ein "
            f"Warteauftrag angelegt - beides braucht diese Auskunft. "
            f"Ursache: {lage.get('grund')}")


def _boerse_hat_zugemacht_meldung(lage: dict) -> str:
    return (
        "Die Boerse hat geschlossen, seit die Zusammenfassung erstellt wurde. "
        "Es wurde NICHTS geschrieben - der angezeigte Kurs ist jetzt der "
        "Schlusskurs des letzten Handelstags, und genau dazu soll nicht mehr "
        "geschlossen werden. Bitte von vorn beginnen; dann wird ein "
        f"Warteauftrag angelegt. ({lage.get('grund')})")


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
    lage = lage_fuer_bot(bot_name)
    wartend = {a["trade_id"] for a in warteauftraege.fuer_bot(bot_name)}
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
            # Ohne Kurs darf nicht SOFORT geschlossen werden - dann bietet
            # das Frontend die Schaltflaeche gar nicht erst an, statt einen
            # Knopf zu zeigen, der garantiert in einer Absage endet.
            #
            # Bei geschlossener Boerse gilt das NICHT: dort entsteht ein
            # Warteauftrag, und der braucht keinen Kurs - der wird erst beim
            # Ausfuehren geholt. Genau darum geht es ja.
            "schliessbar_jetzt": (kurs is not None
                                   or lage["warteauftrag_noetig"]),
            # Steht fuer diese Position schon ein Warteauftrag? Dann zeigt
            # die Oberflaeche das statt eines zweiten Knopfes - ein zweiter
            # Auftrag fuer dieselbe Zeile wird ohnehin abgelehnt.
            "warteauftrag_offen": position["id"] in wartend,
        })
    return {
        "bot": bot_name,
        "anzeigename": manual_close.SCHLIESSBARE_BOTS[bot_name]["anzeigename"],
        "anlageklasse": manual_close.SCHLIESSBARE_BOTS[bot_name]["anlageklasse"],
        "schliessbar": True,
        "grund": None,
        "positionen": zeilen,
        # Der Boersenzustand steht schon HIER, nicht erst im Dialog: die
        # Seite soll vorher sagen koennen, was ein Tap ausloesen wird. Ein
        # Knopf, der je nach Uhrzeit etwas voellig anderes tut, ohne dass
        # man es ihm ansieht, waere die unangenehmste Ueberraschung, die
        # dieses Dashboard anbieten koennte. Der Kalender ist eine reine
        # Rechnung ohne Netzzugriff - das kostet also nichts.
        "boerse": lage,
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

    lage = lage_fuer_bot(bot_name)
    _pruefe_kalender_bekannt(lage)
    warteauftrag_modus = lage["warteauftrag_noetig"]

    if warteauftrag_modus:
        # Ein zweiter Auftrag fuer dieselbe Zeile wird beim Anlegen ohnehin
        # abgelehnt. Das aber ERST nach dem Bestaetigungsschritt zu sagen,
        # waere die unfreundlichste Reihenfolge: der Nutzer haette dann eine
        # Warnung bestaetigt, die zu nichts fuehrt.
        for vorhanden in warteauftraege.fuer_bot(bot_name):
            if vorhanden["trade_id"] == trade_id:
                raise SchliessenNichtMoeglich(
                    f"Fuer {position['symbol']} steht bereits ein Warteauftrag "
                    f"(seit {vorhanden['angefordert_am']}). Er laesst sich in "
                    f"der Liste der wartenden Auftraege stornieren.")

    kurs = (kurse or {}).get(position["symbol"])
    kurs = float(kurs) if kurs else None
    if not kurs and not warteauftrag_modus:
        raise SchliessenNichtMoeglich(
            "Kein aktueller Kurs verfuegbar. Ohne Ausstiegskurs wird nicht "
            "geschrieben - bitte spaeter erneut versuchen.")
    if not position.get("entry_price"):
        # Auch fuer einen Warteauftrag: ohne Einstiegskurs koennte die
        # spaetere Ausfuehrung den PnL nicht rechnen. Ein Auftrag, der beim
        # Ausfuehren garantiert scheitert, ist schlechter als eine Absage
        # jetzt - er wuerde erst am naechsten Handelstag auffallen.
        raise SchliessenNichtMoeglich(
            "Der Einstiegskurs dieser Position fehlt in der Datenbank - der "
            "PnL waere nicht berechenbar. Es wird nichts geschrieben.")

    pnl = (manual_close.berechne_pnl(bot_name, position["entry_price"], kurs)
           if kurs else None)

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
        "entry_time": position.get("entry_time"),
        "entry_preis": _gerundet(position["entry_price"]),
        "kurs": kurs,
        "pnl_pct": pnl,
        # Was dieser Vorgang beim Ausfuehren AUSLOEST, wird HIER festgelegt
        # und nicht vom Aufrufer mitgeschickt. Der Browser waehlt also
        # nicht zwischen "sofort" und "vormerken" - er bestaetigt nur, was
        # der Server aus dem Kalender abgeleitet hat. Ein Frontend, das den
        # Weg selbst waehlen koennte, waere ein Frontend, das mit einer
        # veralteten Annahme ueber die Boersenzeiten einen Schreibzugriff
        # ausloest.
        "warteauftrag": warteauftrag_modus,
        "boerse": lage,
        "gueltig_bis": _jetzt() + GUELTIG_SEKUNDEN,
    })
    logger.info(f"Schliessvorgang vorbereitet: Bot {bot_name}, Trade "
                f"{trade_id} ({position['symbol']}) - "
                f"{'WARTEAUFTRAG (Boerse geschlossen)' if warteauftrag_modus else 'sofort'}"
                f", noch nichts geschrieben.")

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
        "warteauftrag": warteauftrag_modus,
        "boerse": lage,
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


def _bestaetigung_geprueft(bot_name, trade_id, benutzer, bestaetigt, quelle) -> None:
    """Der zusaetzliche Warnschritt fuer Warteauftraege - serverseitig.

    Verlangt wird genau der Wert True, nicht "irgendetwas Wahres": ein
    versehentlich mitgeschicktes leeres Feld, ein "0" oder ein "nein" darf
    keinen Auftrag ausloesen. Der Fehlversuch landet im Protokoll - er ist
    die Zeile, an der auffiele, dass jemand den Warnschritt zu umgehen
    versucht.
    """
    if bestaetigt is not True:
        manual_close.protokolliere_ablehnung(
            bot_name, trade_id, benutzer,
            "Warteauftrag ohne Bestaetigung des Warnschritts angefragt",
            quelle)
        raise SchliessenNichtMoeglich(
            "Die Boerse ist geschlossen. Ein Ausstieg wird deshalb nicht "
            "sofort geschrieben, sondern als Warteauftrag vorgemerkt - und "
            "das muss ausdruecklich bestaetigt werden, weil die Ausfuehrung "
            "spaeter OHNE erneute Rueckfrage passiert. Es wurde nichts "
            "geaendert und nichts vorgemerkt.")


def _sofort_erlaubt(bot_name, trade_id, benutzer, lage, quelle) -> None:
    """Darf JETZT noch sofort geschrieben werden?

    Zwischen Zusammenfassung und Tap liegen bis zu 120 Sekunden, und genau
    in dieses Fenster kann der Handelsschluss fallen. Dann ist der
    bestaetigte Kurs kein "aktueller" Kurs mehr, sondern der Schluss des
    letzten Handelstags - also genau die Zahl, um deretwillen diese ganze
    Funktion gebaut wurde. In diesem Fall wird NICHT geschrieben und auch
    NICHT stillschweigend ein Warteauftrag angelegt: der Nutzer hat den
    Warnschritt nicht gesehen, und ein Auftrag, den er nicht bestaetigt
    hat, waere dieselbe Ueberraschung mit umgekehrtem Vorzeichen.
    """
    if lage["handelbar_jetzt"]:
        return
    grund = (_boerse_hat_zugemacht_meldung(lage) if lage["warteauftrag_noetig"]
             else f"Der Boersenkalender gibt keine Auskunft: {lage.get('grund')}")
    manual_close.protokolliere_ablehnung(bot_name, trade_id, benutzer,
                                          "Boerse nicht mehr offen beim "
                                          "Ausfuehren", quelle)
    raise SchliessenNichtMoeglich(grund)


def ausfuehren(bot_name: str, kennung, benutzer,
                warteauftrag_bestaetigt=False) -> dict:
    """Aufruf 2 - schliesst GENAU EINE Position, ODER merkt sie vor.

    Verlangt eine gueltige, noch nicht abgelaufene Vorgangs-Kennung aus
    Aufruf 1. Eine zusaetzliche Texteingabe wird NICHT mehr verlangt (siehe
    Modul-Kopf); die Kennung ist die Absicherung, und sie ist es auch
    vorher schon gewesen.

    WELCHER VON BEIDEN AUSGAENGEN, entscheidet der Vorgang und nicht der
    Aufrufer: war die Boerse beim Vorbereiten geschlossen, entsteht ein
    Warteauftrag - dann aber nur mit warteauftrag_bestaetigt=True.
    """
    vorgang = _vorgang_einloesen(bot_name, kennung, benutzer, ART_EINZEL)

    if vorgang.get("warteauftrag"):
        _bestaetigung_geprueft(bot_name, vorgang["trade_id"], benutzer,
                                warteauftrag_bestaetigt,
                                manual_close.QUELLE_DASHBOARD)
        auftrag = warteauftraege.anlegen(
            bot_name, vorgang["trade_id"], vorgang["symbol"], benutzer,
            manual_close.QUELLE_DASHBOARD,
            entry_time=vorgang.get("entry_time"),
            entry_price=vorgang.get("entry_preis"),
            boerse=vorgang.get("boerse"))
        return {
            "erfolg": True,
            "warteauftrag": True,
            "bot": bot_name,
            "trade_id": vorgang["trade_id"],
            "symbol": vorgang["symbol"],
            "auftrag": auftrag,
            "boerse": vorgang.get("boerse"),
            "meldung": (
                f"{vorgang['symbol']} wurde NICHT geschlossen, sondern als "
                f"Warteauftrag vorgemerkt. Die Position wird automatisch zum "
                f"naechsten echten Kurs geschlossen, sobald die Boerse wieder "
                f"geoeffnet hat - ohne erneute Rueckfrage. Bis dahin laesst "
                f"sich der Auftrag stornieren. Die Datenbank des Bots ist "
                f"unveraendert."),
        }

    # Sofort schliessen - der unveraenderte Weg, jetzt mit einer Pruefung
    # davor (siehe _sofort_erlaubt).
    _sofort_erlaubt(bot_name, vorgang["trade_id"], benutzer,
                     lage_fuer_bot(bot_name), manual_close.QUELLE_DASHBOARD)

    # Der Kern verlangt den Bestaetigungstext weiter; der wird hier aus der
    # Konstante gesetzt, nicht aus der Anfrage gelesen (siehe Modul-Kopf).
    ergebnis = manual_close.schliesse_position(
        bot_name, vorgang["trade_id"], vorgang["kurs"], benutzer,
        BESTAETIGUNGSTEXT, quelle=manual_close.QUELLE_DASHBOARD)

    return {
        "erfolg": True,
        # Steht auch im Erfolgsfall dabei, obwohl hier immer False: die
        # Oberflaeche unterscheidet die beiden Ausgaenge an genau diesem
        # Feld, und ein Feld, das mal da ist und mal nicht, waere dort eine
        # Fallunterscheidung ueber Abwesenheit.
        "warteauftrag": False,
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
# Kapitalgewichteter Durchschnitt der Einzelrenditen
# ---------------------------------------------------------------------------
# Bis hierher zeigte das Dashboard bewusst NUR den einfachen Durchschnitt je
# Position und die Spannweite - mit der Begruendung, dass eine Summe von
# Trade-Prozenten keine Portfolio-Rendite ist (Methodik-Grundsatz 2). Das war
# richtig, hat das Problem aber vermieden statt geloest: unterschiedlich grosse
# Positionen gleich zu gewichten ist genauso falsch wie sie zu addieren, nur
# unauffaelliger. Ein Bot mit 2 % Positionsgroesse zaehlt im einfachen
# Durchschnitt genauso viel wie einer mit 10 %.
#
# Die Rechnung hier ist der gewichtete Durchschnitt:
#
#     Summe(Allokation_i * PnL_i) / Summe(Allokation_i)
#
# WAS DIESE ZAHL IST: die mittlere Rendite der geschlossenen Positionen, je
# Position gewichtet mit der Positionsgroesse, die der jeweilige Bot in seiner
# Backtest-Konfiguration annimmt. Bei einem einzelnen Bot ist sie deshalb
# zwangslaeufig gleich dem einfachen Durchschnitt (alle Positionen tragen
# dieselbe Allokation); erst ueber mehrere Bots mit 10 %, 5 % und 2 % trennen
# sich die beiden Zahlen.
#
# WAS SIE NICHT IST, und das gehoert an jede Anzeige dazu:
#   * keine echte Kapitalbindung - die Allokation ist eine Annahme aus der
#     Backtest-Konfiguration, forward_test.py trackt bei keinem Bot Kapital.
#     Genau diese Verwechslung von Backtest-Annahme und Live-Fakt sollte
#     Grundsatz 2 verhindern; sie wird hier nicht durch Weglassen der Zahl
#     vermieden, sondern durch Beschriftung.
#   * keine Portfolio-Rendite - Zinseszins und gleichzeitig gebundenes Kapital
#     stecken allein in der ereignisbasierten equity_simulation.py.
#
# WARUM DURCH DIE SUMME DER GEWICHTE GETEILT WIRD: ohne diesen Nenner waere
# Summe(Allokation_i * PnL_i) die Wirkung auf das Gesamtkapital in
# Prozentpunkten - auch eine sinnvolle Zahl, aber eine andere, und eine, die
# mit der Zahl der Positionen waechst. Im Crash-Fall waere das wieder die
# grosse, beeindruckende Zahl, die niemand richtig liest. Gezeigt wird deshalb
# eine Rendite, keine Summe.

GEWICHTUNG_GRUNDLAGE = ("angenommene Positionsgroesse je Bot (ALLOCATION_PCT "
                        "aus der Backtest-Konfiguration)")

GEWICHTUNG_HINWEIS = (
    "Gewichtet nach der Positionsgroesse, die JE BOT in dessen "
    "Backtest-Konfiguration angenommen ist (ALLOCATION_PCT aus live_params.py "
    "bzw. equity_simulation.py). Das ist eine Annahme, KEINE live getrackte "
    "Kapitalbindung - forward_test.py fuehrt bei keinem Bot Kapital oder "
    "Positionsgroessen. Es ist auch keine Portfolio-Rendite: Zinseszins und "
    "gleichzeitig gebundenes Kapital stecken allein in equity_simulation.py.")


def _anzeigename(bot_name: str) -> str:
    eintrag = manual_close.SCHLIESSBARE_BOTS.get(bot_name) or {}
    return eintrag.get("anzeigename", bot_name)


def gewichteter_pnl(beitraege) -> dict:
    """Der gewichtete Durchschnitt ueber (bot_name, pnl_pct)-Paare.

    Funktioniert fuer EINEN Bot wie fuer beliebig viele - der bot-weite
    Notfallweg gibt Paare eines Bots hinein, der globale Weg die aller Bots.
    Eine zweite Rechnung fuer den bot-uebergreifenden Fall gibt es
    ausdruecklich nicht: sie waere die Stelle, an der die Gewichtung spaeter
    nur noch auf einem der beiden Wege stimmt.

    Bots OHNE dokumentierte Positionsgroesse werden nicht geschaetzt und nicht
    stillschweigend uebergangen, sondern aus der gewichteten Zahl
    herausgenommen und unter `nicht_gewichtbar` mit Grund, Anzahl und ihrem
    eigenen ungewichteten Durchschnitt ausgewiesen. Ein ersatzweise
    angenommener Standardwert waere eine erfundene Zahl in einer Anzeige, nach
    der im Zweifel schnell entschieden wird.

    `ungewichtet_schnitt_pct` ist der einfache Durchschnitt ueber GENAU
    DIESELBEN Positionen, die auch in die gewichtete Zahl eingehen. Nur so
    zeigt der Vergleich der beiden Zahlen die Wirkung der Gewichtung und nicht
    zusaetzlich den Unterschied der Grundmenge; der Durchschnitt ueber ALLE
    Positionen steht unveraendert daneben in `pnl_schnitt_pct`.
    """
    nach_bot = {}
    for bot_name, pnl in beitraege:
        if pnl is None:
            continue
        nach_bot.setdefault(bot_name, []).append(float(pnl))

    gewichte, nicht_gewichtbar, einbezogen = [], [], []
    zaehler = nenner = 0.0
    for bot_name in sorted(nach_bot):
        werte = nach_bot[bot_name]
        info = manual_close.allokation(bot_name)
        if info["anteil"] is None:
            nicht_gewichtbar.append({
                "bot": bot_name,
                "anzeigename": _anzeigename(bot_name),
                "grund": info["grund"],
                "anzahl": len(werte),
                "pnl_schnitt_pct": round(sum(werte) / len(werte), 2),
            })
            continue
        gewichte.append({
            "bot": bot_name,
            "anzeigename": _anzeigename(bot_name),
            "allokation_pct": info["prozent"],
            "quelle": info["quelle"],
            "anzahl": len(werte),
        })
        zaehler += info["anteil"] * sum(werte)
        nenner += info["anteil"] * len(werte)
        einbezogen.extend(werte)

    return {
        "wert_pct": round(zaehler / nenner, 2) if nenner else None,
        "ungewichtet_schnitt_pct": (round(sum(einbezogen) / len(einbezogen), 2)
                                     if einbezogen else None),
        "anzahl": len(einbezogen),
        "grundlage": GEWICHTUNG_GRUNDLAGE,
        "hinweis": GEWICHTUNG_HINWEIS,
        "gewichte": gewichte,
        "nicht_gewichtbar": nicht_gewichtbar,
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

    lage = lage_fuer_bot(bot_name)
    _pruefe_kalender_bekannt(lage)
    warteauftrag_modus = lage["warteauftrag_noetig"]
    schon_vorgemerkt = {a["trade_id"] for a in warteauftraege.fuer_bot(bot_name)}

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
        #
        # Bei geschlossener Boerse zaehlt der fehlende Kurs NICHT als
        # Hindernis: es wird ohnehin nur vorgemerkt, und der Kurs kommt beim
        # Ausfuehren. Der fehlende EINSTIEGSKURS bleibt eines - ohne ihn
        # scheitert die spaetere Ausfuehrung sicher.
        grund = None
        if not position.get("entry_price"):
            grund = "Einstiegskurs fehlt in der Datenbank"
        elif position["id"] in schon_vorgemerkt:
            grund = "steht bereits als Warteauftrag"
        elif not kurs and not warteauftrag_modus:
            grund = "kein aktueller Kurs verfuegbar"
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
            "Keine der offenen Positionen laesst sich gerade "
            + ("vormerken" if warteauftrag_modus else "schliessen")
            + " - siehe den Grund je Position. Es wurde nichts geaendert.")

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
        # Wie beim Einzelweg entscheidet der SERVER hier, was der Tap
        # spaeter ausloest - siehe die Begruendung dort.
        "warteauftrag": warteauftrag_modus,
        "boerse": lage,
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
        # WEITERHIN KEINE Summe der Prozente: die waere keine
        # Portfolio-Rendite, sondern eine Zahl ohne Bedeutung - in diesem
        # Projekt eine mehrfach aufgetretene Fehlerquelle und als
        # Methodik-Grundsatz im Uebergabeprotokoll (Abschnitt 7, Punkt 2)
        # festgehalten. Gezeigt wird der Durchschnitt je Position, dazu
        # bestes und schlechtestes Ergebnis.
        "pnl_schnitt_pct": round(sum(werte) / len(werte), 2) if werte else None,
        "pnl_bestes_pct": max(werte) if werte else None,
        "pnl_schlechtestes_pct": min(werte) if werte else None,
        # DAZU, nicht statt dessen: der nach Positionsgroesse gewichtete
        # Durchschnitt. Hier stand vorher die Begruendung, eine Rechnung ueber
        # die Positionsgroesse hereinzuziehen hiesse, eine Backtest-Annahme als
        # Live-Aussage auszugeben. Das bleibt richtig - aber es trifft nur zu,
        # wenn man die Zahl unbeschriftet hinstellt. Beschriftet loest sie das
        # Problem, das der einfache Durchschnitt nur verdeckt: er gewichtet 2 %
        # und 10 % Positionsgroesse gleich. Beide Zahlen stehen deshalb
        # nebeneinander, damit der Unterschied selbst sichtbar ist.
        "pnl_gewichtet": gewichteter_pnl((bot_name, z["pnl_pct"]) for z in zeilen),
        "warteauftrag": warteauftrag_modus,
        "boerse": lage,
        "gueltig_sekunden": GUELTIG_SEKUNDEN,
    }


def alle_ausfuehren(bot_name: str, kennung, benutzer,
                     warteauftrag_bestaetigt=False) -> dict:
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

    if vorgang.get("warteauftrag"):
        _bestaetigung_geprueft(bot_name, None, benutzer, warteauftrag_bestaetigt,
                                manual_close.QUELLE_DASHBOARD)
        ergebnis = _bot_vormerken(bot_name, vorgang["positionen"], benutzer,
                                   manual_close.QUELLE_DASHBOARD,
                                   vorgang.get("boerse"))
        ergebnis["meldung"] = _vormerk_meldung(ergebnis)
        logger.info(f"Notfall-Vormerken beendet: {ergebnis['meldung']}")
        return ergebnis

    _sofort_erlaubt(bot_name, None, benutzer, lage_fuer_bot(bot_name),
                     manual_close.QUELLE_DASHBOARD)
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
        # Auch im ERGEBNIS, nicht nur in der Uebersicht: die Uebersicht nennt
        # Schaetzungen, das Ergebnis die tatsaechlich geschriebenen Werte. Nur
        # eine der beiden Stellen zu beschriften war in diesem Projekt schon
        # zweimal der Grund, warum eine Pruefung gruen war, obwohl die Haelfte
        # fehlte.
        "pnl_gewichtet": gewichteter_pnl((bot_name, g["pnl_pct"])
                                          for g in geschlossen),
    }
    return ergebnis


def _bot_vormerken(bot_name: str, bestaetigt, benutzer, quelle: str,
                    boerse: dict = None) -> dict:
    """Das Gegenstueck zu `_bot_abarbeiten()` fuer die geschlossene Boerse:
    legt je bestaetigter Position EINEN Warteauftrag an.

    BEWUSST EINE ZWEITE FUNKTION und keine Verzweigung in
    `_bot_abarbeiten()`. Die beiden haben ausser der Schleife nichts
    gemeinsam: die eine schreibt in eine Live-Datenbank, die andere fasst
    keine Datenbank an. Ein gemeinsamer Rumpf mit einem `if` in der Mitte
    haette die Aussage "hier steht der einzige Schreibpfad des Projekts"
    aufgeweicht - und genau die traegt die gesamte Absicherung. Der Preis
    ist eine aehnlich aussehende Schleife; der Nutzen ist, dass man einer
    Funktion ohne Lesen ansieht, ob sie schreiben kann.

    Dieselben drei Gruppen wie dort, aus denselben Gruenden:
      bestaetigt UND noch offen    -> Warteauftrag
      bestaetigt, nicht mehr offen -> uebersprungen (der Bot war schneller)
      offen, aber NICHT bestaetigt -> nicht angefasst, aber ausgewiesen
    """
    bestaetigt = list(bestaetigt)
    # EIN Lesevorgang, aus dem beides kommt: welche Zeilen noch offen sind
    # und ihre Einstiegsdaten. Zweimal zu lesen hiesse, mit zwei moeglicherweise
    # verschiedenen Staenden zu arbeiten.
    offen = manual_close.offene_positionen(bot_name)
    noch_offen = {p["id"] for p in offen}
    entry_daten = {p["id"]: (p.get("entry_price"), p.get("entry_time"))
                   for p in offen}

    vorgemerkt, fehlgeschlagen, uebersprungen = [], [], []

    for trade_id, symbol, _kurs in bestaetigt:
        if trade_id not in noch_offen:
            uebersprungen.append({
                "trade_id": trade_id, "symbol": symbol,
                "grund": ("war beim Vormerken nicht mehr offen - der Bot hat "
                           "sie selbst geschlossen"),
            })
            continue
        entry_price, entry_time = entry_daten.get(trade_id, (None, None))
        try:
            auftrag = warteauftraege.anlegen(
                bot_name, trade_id, symbol, benutzer, quelle,
                entry_time=entry_time, entry_price=_gerundet(entry_price),
                boerse=boerse)
        except WarteauftragNichtMoeglich as fehler:
            fehlgeschlagen.append({
                "trade_id": trade_id, "symbol": symbol, "grund": str(fehler)})
            logger.warning(f"Vormerken: Trade {trade_id} ({symbol}) nicht "
                           f"vorgemerkt, Schleife laeuft weiter - {fehler}")
            continue
        except Exception as fehler:      # noqa: BLE001 - wie in _bot_abarbeiten
            manual_close.protokolliere_warteauftrag(
                "FEHLGESCHLAGEN", bot_name=bot_name, trade_id=trade_id,
                benutzer=benutzer, quelle=quelle,
                zusatz=f"unerwarteter Fehler beim Anlegen: {fehler}")
            fehlgeschlagen.append({
                "trade_id": trade_id, "symbol": symbol,
                "grund": f"unerwarteter Fehler: {fehler}"})
            logger.exception(f"Vormerken: unerwarteter Fehler bei Trade "
                             f"{trade_id} ({symbol}) - Schleife laeuft weiter.")
            continue
        vorgemerkt.append({
            "auftrag_id": auftrag["id"],
            "trade_id": trade_id,
            "symbol": symbol,
            "entry_preis": auftrag["entry_price"],
            "angefordert_am": auftrag["angefordert_am"],
        })

    bestaetigte_ids = {t for t, _, _ in bestaetigt}
    nicht_bestaetigt = sorted(noch_offen - bestaetigte_ids)

    return {
        "erfolg": not fehlgeschlagen,
        "warteauftrag": True,
        "bot": bot_name,
        "anzeigename": _anzeigename(bot_name),
        "angefragt": len(bestaetigt),
        "vorgemerkt": vorgemerkt,
        "fehlgeschlagen": fehlgeschlagen,
        "uebersprungen": uebersprungen,
        "nicht_bestaetigt": nicht_bestaetigt,
        "anzahl_vorgemerkt": len(vorgemerkt),
        "anzahl_fehlgeschlagen": len(fehlgeschlagen),
        "anzahl_uebersprungen": len(uebersprungen),
        # Bewusst KEINE PnL-Zahlen: es gibt keinen Ausstiegskurs und damit
        # kein Ergebnis. Eine Schaetzung auf Basis des letzten
        # Schlusskurses hinzuschreiben hiesse, genau die Zahl zu zeigen,
        # zu der ausdruecklich NICHT geschlossen wird.
        "boerse": boerse,
    }


def _vormerk_meldung(ergebnis: dict) -> str:
    """Ein Satz, der den Ausgang vollstaendig nennt - und ausdruecklich
    sagt, dass NICHTS geschlossen wurde."""
    teile = [f"{ergebnis['anzahl_vorgemerkt']} von {ergebnis['angefragt']} "
             f"Positionen als Warteauftrag vorgemerkt (nichts geschlossen, "
             f"Datenbank unveraendert)"]
    if ergebnis["anzahl_fehlgeschlagen"]:
        namen = ", ".join(f"{f['symbol']} ({f['grund']})"
                           for f in ergebnis["fehlgeschlagen"])
        teile.append(f"{ergebnis['anzahl_fehlgeschlagen']} nicht vorgemerkt: {namen}")
    if ergebnis["anzahl_uebersprungen"]:
        namen = ", ".join(u["symbol"] for u in ergebnis["uebersprungen"])
        teile.append(f"{ergebnis['anzahl_uebersprungen']} uebersprungen, weil "
                      f"der Bot sie selbst geschlossen hatte: {namen}")
    if ergebnis["nicht_bestaetigt"]:
        teile.append(f"{len(ergebnis['nicht_bestaetigt'])} Position(en) wurden "
                      f"erst nach der Uebersicht eroeffnet und NICHT vorgemerkt")
    satz = "; ".join(teile) + "."
    if ergebnis["anzahl_vorgemerkt"]:
        satz += (" Ausgefuehrt wird automatisch bei der naechsten "
                 "Boersenoeffnung, ohne erneute Rueckfrage; bis dahin "
                 "stornierbar. Jede Anlage steht im Protokoll "
                 "logs/notifications/manuelle_eingriffe.log.")
    return satz


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

    Die Boersenlage wird JE BOT bestimmt, weil der Crash-Weg Krypto- und
    Aktien-Bots gleichzeitig betrifft: die Krypto-Bots schliessen sofort,
    die Aktien-Bots werden bei geschlossener Boerse vorgemerkt. Genau
    dieses Nebeneinander ist der Grund, warum die Unterscheidung nicht am
    Vorgang haengen darf, sondern am einzelnen Bot.
    """
    angaben = manual_close.SCHLIESSBARE_BOTS[bot_name]
    lage = boersenlage(angaben["anlageklasse"])
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
        "boerse": lage,
        "warteauftrag": lage["warteauftrag_noetig"],
    }
    if lage["unbekannt"]:
        # Kein Kalender, keine Entscheidung - und deshalb auch keine
        # Positionen dieses Bots im Vorgang. Er erscheint in der Uebersicht
        # mit Begruendung, statt lautlos zu fehlen.
        anzeige["lesefehler"] = lage["grund"]
        return anzeige, []
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

    schon_vorgemerkt = {a["trade_id"] for a in warteauftraege.fuer_bot(bot_name)}
    schliessbar = []
    for position in offen:
        kurs = (kurse or {}).get(position["symbol"])
        kurs = float(kurs) if kurs else None
        pnl = None
        grund = None
        if not position.get("entry_price"):
            grund = "Einstiegskurs fehlt in der Datenbank"
        elif position["id"] in schon_vorgemerkt:
            grund = "steht bereits als Warteauftrag"
        elif not kurs and not lage["warteauftrag_noetig"]:
            grund = "kein aktueller Kurs verfuegbar"
        elif kurs:
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
    freigeschalteten Bots, nach Bot gruppiert. Schreibt nichts.

    Bei geschlossener Boerse ist dieser Weg GEMISCHT: die Krypto-Bots
    werden sofort geschlossen, die Aktien-Bots vorgemerkt. Die Uebersicht
    weist beides je Bot getrennt aus - eine Zahl, die beides zusammenzaehlt,
    waere im Crash-Fall die irrefuehrendste Angabe ueberhaupt ("neun
    Positionen geschlossen", von denen vier noch offen sind)."""
    # EINMAL fuer alle Aktien-Bots: der Kalender ist derselbe, und die
    # Antwort soll den Warnschritt aus EINER Angabe bauen koennen.
    lage_aktien = boersenlage("aktien")
    bots, sofort_je_bot, vormerken_je_bot = [], {}, {}
    for bot_name in sorted(manual_close.SCHLIESSBARE_BOTS):
        # Sortiert, damit Reihenfolge, Protokoll und Zusammenfassung
        # reproduzierbar sind - bei neun Bots ist "irgendeine Reihenfolge"
        # sonst bei jeder Fehlersuche eine Variable zu viel.
        anzeige, schliessbar = _bot_uebersicht(bot_name, kurse)
        if anzeige["anzahl_gesamt"] == 0 and not anzeige["lesefehler"]:
            continue                      # dieser Bot hat gerade nichts offen
        bots.append(anzeige)
        if not schliessbar:
            continue
        # ZWEI getrennte Toepfe, nicht ein Topf mit Merkmal: der eine wird
        # spaeter durch die Schreib-Schleife geschickt, der andere durch die
        # Vormerk-Schleife. Laegen sie zusammen, muesste die Unterscheidung
        # in der Schleife noch einmal getroffen werden - an der einen
        # Stelle, an der ein Irrtum eine Live-Datenbank kostet.
        if anzeige["warteauftrag"]:
            vormerken_je_bot[bot_name] = schliessbar
        else:
            sofort_je_bot[bot_name] = schliessbar

    if not bots:
        raise SchliessenNichtMoeglich(
            "Kein Bot hat gerade eine offene Position. Es gibt nichts zu "
            "schliessen.")
    if not sofort_je_bot and not vormerken_je_bot:
        raise SchliessenNichtMoeglich(
            "Keine der offenen Positionen laesst sich gerade schliessen oder "
            "vormerken - siehe den Grund je Position. Es wurde nichts "
            "geaendert.")

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
        "positionen_je_bot": sofort_je_bot,
        "vormerken_je_bot": vormerken_je_bot,
        "warteauftrag": bool(vormerken_je_bot),
        "boerse": lage_aktien,
        "gueltig_bis": _jetzt() + GUELTIG_SEKUNDEN,
    })
    anzahl_sofort = sum(len(p) for p in sofort_je_bot.values())
    anzahl_vormerken = sum(len(p) for p in vormerken_je_bot.values())
    anzahl = anzahl_sofort + anzahl_vormerken
    betroffene_bots = sorted(set(sofort_je_bot) | set(vormerken_je_bot))
    logger.info(f"GLOBALER Schliessvorgang vorbereitet: {anzahl_sofort} "
                f"Positionen sofort, {anzahl_vormerken} als Warteauftrag, in "
                f"{len(betroffene_bots)} Bots ({', '.join(betroffene_bots)}) - "
                f"noch nichts geschrieben.")

    return {
        "vorgang": kennung,
        "bots": bots,
        "anzahl": anzahl,
        "anzahl_sofort": anzahl_sofort,
        "anzahl_warteauftrag": anzahl_vormerken,
        "anzahl_gesamt": sum(b["anzahl_gesamt"] for b in bots),
        "anzahl_bots": len(betroffene_bots),
        "warteauftrag": bool(vormerken_je_bot),
        "bots_warteauftrag": sorted(vormerken_je_bot),
        "boerse": lage_aktien,
        "bots_mit_lesefehler": [b["bot"] for b in bots if b["lesefehler"]],
        # HIER ist die Gewichtung inhaltlich relevant: ueber neun Bots treffen
        # 10 %, 5 % und 2 % Positionsgroesse aufeinander, und ein einfacher
        # Durchschnitt ueber alle Positionen wuerde sie gleich gewichten.
        # Weiterhin KEINE Summe und keine unbeschriftete Gesamtzahl - eine
        # gewichtete Durchschnittsrendite mit Angabe ihrer Grundlage (siehe
        # gewichteter_pnl()). Der Durchschnitt je Bot steht unveraendert in
        # den einzelnen Bot-Eintraegen.
        "pnl_gewichtet": gewichteter_pnl(
            (b["bot"], p["pnl_pct"]) for b in bots for p in b["positionen"]),
        # Der Text wird dem Frontend bewusst MITGETEILT - anders als beim
        # frueheren Einzelweg, wo er versteckt und damit sinnlos war. Hier
        # ist er kein Geheimnis, sondern eine Huerde: der Nutzer soll lesen
        # koennen, was er tippen muss.
        "crash_text": CRASH_TEXT,
        "gueltig_sekunden": GUELTIG_SEKUNDEN,
    }


def global_ausfuehren(kennung, bestaetigung, benutzer,
                       warteauftrag_bestaetigt=False) -> dict:
    """Crash-Weg, Aufruf 2 - schliesst in JEDEM Bot jede bestaetigte
    Position EINZELN, ueber `_bot_abarbeiten()` je Bot; Aktien-Bots bei
    geschlossener Boerse stattdessen ueber `_bot_vormerken()`.

    Scheitert ein ganzer Bot, laufen die uebrigen weiter; scheitert eine
    Position, laufen die uebrigen Positionen dieses Bots weiter. Das
    Ergebnis weist beides getrennt aus.

    DER GEMISCHTE FALL ist hier der Normalfall, nicht die Ausnahme: an
    einem Sonntagabend betrifft derselbe Klick fuenf Krypto-Bots (sofort)
    und vier Aktien-Bots (vorgemerkt). Beides zusammen als "geschlossen"
    zu melden waere die gefaehrlichste Zusammenfassung dieses Dashboards -
    jemand haelt sich fuer flach im Markt und ist es nicht.
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
    vormerken_je_bot = dict(vorgang.get("vormerken_je_bot") or {})

    # Der Warnschritt fuer die Warteauftraege wird NACH dem CRASH-Text
    # geprueft, aber bevor irgendetwas passiert: fehlt er, passiert weder
    # das eine noch das andere. Ein Crash-Klick, der die Krypto-Bots
    # schliesst und die Aktien-Bots stillschweigend liegen laesst, weil
    # eine Bestaetigung fehlte, waere genau die halbe Wahrheit, die dieser
    # Weg vermeiden soll.
    if vormerken_je_bot:
        _bestaetigung_geprueft(GLOBAL_LABEL, None, benutzer,
                                warteauftrag_bestaetigt,
                                manual_close.QUELLE_DASHBOARD_CRASH)

    logger.warning(f"GLOBALES Schliessen beginnt: {len(je_bot)} Bots sofort "
                   f"({sum(len(p) for p in je_bot.values())} Positionen), "
                   f"{len(vormerken_je_bot)} Bots als Warteauftrag "
                   f"({sum(len(p) for p in vormerken_je_bot.values())} "
                   f"Positionen), ausgeloest von {benutzer}.")

    ergebnisse, bot_fehler, verschoben = [], [], []
    for bot_name in sorted(je_bot):
        # Die Boersenlage wird JE BOT neu geprueft, nicht aus dem Vorgang
        # uebernommen: zwischen Uebersicht und Klick koennen 120 Sekunden
        # liegen, und in genau die kann der Handelsschluss fallen. Ein
        # Aktien-Bot, der beim Vorbereiten noch "sofort" war, wird dann
        # NICHT geschrieben - und auch nicht ohne Bestaetigung vorgemerkt,
        # sondern ausdruecklich als unberuehrt gemeldet.
        lage = lage_fuer_bot(bot_name)
        if not lage["handelbar_jetzt"]:
            manual_close.protokolliere_ablehnung(
                bot_name, None, benutzer,
                "Boerse nicht mehr offen beim globalen Ausfuehren",
                manual_close.QUELLE_DASHBOARD_CRASH)
            verschoben.append({
                "bot": bot_name,
                "anzeigename": _anzeigename(bot_name),
                "angefragt": len(je_bot[bot_name]),
                "grund": (_boerse_hat_zugemacht_meldung(lage)
                           if lage["warteauftrag_noetig"] else lage["grund"]),
            })
            continue
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

    # Und jetzt die Aktien-Bots bei geschlossener Boerse. Sie laufen durch
    # eine eigene Schleife mit einer eigenen Funktion - dieselbe Trennung
    # wie beim bot-weiten Weg, aus demselben Grund: was schreiben kann,
    # soll man einer Funktion ansehen.
    vorgemerkte_bots = []
    for bot_name in sorted(vormerken_je_bot):
        try:
            teil = _bot_vormerken(bot_name, vormerken_je_bot[bot_name],
                                   benutzer, manual_close.QUELLE_DASHBOARD_CRASH,
                                   vorgang.get("boerse"))
        except Exception as fehler:      # noqa: BLE001 - wie oben
            manual_close.protokolliere_warteauftrag(
                "FEHLGESCHLAGEN", bot_name=bot_name, trade_id=None,
                benutzer=benutzer, quelle=manual_close.QUELLE_DASHBOARD_CRASH,
                zusatz=f"Bot komplett uebersprungen beim Vormerken: {fehler}")
            bot_fehler.append({
                "bot": bot_name,
                "anzeigename": _anzeigename(bot_name),
                "grund": str(fehler),
                "angefragt": len(vormerken_je_bot[bot_name]),
            })
            logger.exception(f"GLOBALES Vormerken: Bot {bot_name} komplett "
                             f"ausgefallen - die uebrigen laufen weiter.")
            continue
        teil["meldung"] = _vormerk_meldung(teil)
        vorgemerkte_bots.append(teil)

    gesamt_geschlossen = sum(e["anzahl_geschlossen"] for e in ergebnisse)
    gesamt_fehlgeschlagen = sum(e["anzahl_fehlgeschlagen"] for e in ergebnisse)
    gesamt_uebersprungen = sum(e["anzahl_uebersprungen"] for e in ergebnisse)
    gesamt_angefragt = sum(len(p) for p in je_bot.values())

    gesamt_vorgemerkt = sum(e["anzahl_vorgemerkt"] for e in vorgemerkte_bots)
    gesamt_fehlgeschlagen += sum(e["anzahl_fehlgeschlagen"]
                                  for e in vorgemerkte_bots)
    gesamt_uebersprungen += sum(e["anzahl_uebersprungen"]
                                 for e in vorgemerkte_bots)
    gesamt_angefragt += sum(len(p) for p in vormerken_je_bot.values())

    ergebnis = {
        "erfolg": (not gesamt_fehlgeschlagen and not bot_fehler
                   and not verschoben),
        "angefragt": gesamt_angefragt,
        "angefragte_bots": len(je_bot) + len(vormerken_je_bot),
        "bots": ergebnisse,
        "bots_fehlgeschlagen": bot_fehler,
        # Getrennt ausgewiesen und NICHT unter "geschlossen" mitgezaehlt:
        # diese Positionen sind noch offen. Sie stehen nur auf einer Liste.
        "bots_vorgemerkt": vorgemerkte_bots,
        "anzahl_vorgemerkt": gesamt_vorgemerkt,
        "warteauftrag": bool(vorgemerkte_bots),
        "bots_verschoben": verschoben,
        "anzahl_geschlossen": gesamt_geschlossen,
        "anzahl_fehlgeschlagen": gesamt_fehlgeschlagen,
        "anzahl_uebersprungen": gesamt_uebersprungen,
        # Wie in der Uebersicht, jetzt ueber die TATSAECHLICH geschriebenen
        # Werte: der nach Positionsgroesse gewichtete Durchschnitt, mit seiner
        # Grundlage. Eine aufsummierte Gesamt-Prozentzahl gibt es weiterhin
        # nicht; der Durchschnitt je Bot steht in den einzelnen Eintraegen.
        "pnl_gewichtet": gewichteter_pnl(
            (e["bot"], g["pnl_pct"]) for e in ergebnisse
            for g in e["geschlossen"]),
        "boerse": vorgang.get("boerse"),
    }
    ergebnis["meldung"] = _global_meldung(ergebnis)
    logger.warning(f"GLOBALES Schliessen beendet: {ergebnis['meldung']}")
    return ergebnis


def _global_meldung(ergebnis: dict) -> str:
    """Ein Satz, der den Ausgang ueber alle Bots vollstaendig nennt."""
    teile = [f"{ergebnis['anzahl_geschlossen']} von {ergebnis['angefragt']} "
             f"Positionen in {ergebnis['angefragte_bots']} Bots geschlossen"]
    if ergebnis.get("anzahl_vorgemerkt"):
        teile.append(f"{ergebnis['anzahl_vorgemerkt']} Position(en) NICHT "
                      f"geschlossen, sondern als Warteauftrag vorgemerkt "
                      f"(Boerse geschlossen)")
    if ergebnis.get("bots_verschoben"):
        namen = ", ".join(b["bot"] for b in ergebnis["bots_verschoben"])
        teile.append(f"{len(ergebnis['bots_verschoben'])} Bot(s) unberuehrt, "
                      f"weil die Boerse zwischenzeitlich geschlossen hat: {namen}")
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


# ---------------------------------------------------------------------------
# Die wartenden Auftraege: anzeigen und stornieren
# ---------------------------------------------------------------------------
# Beides ist LESEND bzw. RUECKNEHMEND - keine dieser beiden Funktionen fasst
# eine Bot-Datenbank an. Stornieren entfernt eine Absicht, es widerruft
# keinen Schreibzugriff (den hat es nie gegeben).

def warteauftrag_liste(bot_name: str = None) -> dict:
    """Alle wartenden Auftraege, optional nur die eines Bots.

    Je Auftrag wird zusaetzlich der TATSAECHLICHE Stand der Position
    nachgesehen (`noch_offen`). Das kostet eine Leseabfrage je Bot und ist
    den Preis wert: ein Auftrag auf eine Position, die der Bot laengst
    selbst geschlossen hat, sieht in einer reinen Listenanzeige genauso aus
    wie ein wirksamer - und der Nutzer wuerde auf eine Ausfuehrung warten,
    die nie kommt. Das Ausfuehrungsskript raeumt solche Auftraege beim
    naechsten Lauf ab; bis dahin steht es wenigstens dran.
    """
    auftraege = (warteauftraege.fuer_bot(bot_name) if bot_name
                 else warteauftraege.alle())

    offen_je_bot = {}
    zeilen = []
    for auftrag in auftraege:
        bot = auftrag["bot"]
        if bot not in offen_je_bot:
            try:
                offen_je_bot[bot] = {p["id"] for p in
                                      manual_close.offene_positionen(bot)}
            except Exception as fehler:   # noqa: BLE001
                # Eine fehlende oder gesperrte Datenbank darf die Liste nicht
                # verhindern - dann steht eben "unbekannt" statt ja/nein.
                logger.warning(f"Warteauftragsliste: {bot} nicht lesbar - {fehler}")
                offen_je_bot[bot] = None
        bekannt = offen_je_bot[bot]
        zeile = dict(auftrag)
        zeile["noch_offen"] = (None if bekannt is None
                                else auftrag["trade_id"] in bekannt)
        zeilen.append(zeile)

    return {
        "auftraege": zeilen,
        "anzahl": len(zeilen),
        "bot": bot_name,
        # Damit die Liste sagen kann, WANN ausgefuehrt wird - dieselbe
        # Angabe wie im Dialog, aus derselben Quelle.
        "boerse": boersenlage("aktien"),
    }


def warteauftrag_stornieren(auftrag_id, benutzer,
                             quelle: str = None) -> dict:
    """Nimmt einen wartenden Auftrag zurueck. OHNE zweite Bestaetigung -
    Begruendung siehe warteauftraege.stornieren()."""
    auftrag = warteauftraege.stornieren(
        str(auftrag_id or ""), benutzer,
        quelle or manual_close.QUELLE_DASHBOARD)
    return {
        "erfolg": True,
        "auftrag": auftrag,
        "meldung": (f"Warteauftrag fuer {auftrag['symbol']} "
                     f"({_anzeigename(auftrag['bot'])}) storniert. Die Position "
                     f"bleibt offen und wird NICHT automatisch geschlossen. Es "
                     f"wurde nie etwas in die Datenbank geschrieben."),
    }

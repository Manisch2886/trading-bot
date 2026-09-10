"""
Warteauftraege: Ausstiege, die auf die naechste Boersenoeffnung warten
==============================================================================
DAS HIER IST DIE NEUE EIGENSCHAFT DES PROJEKTS, und sie verdient den
Hinweis gleich oben: bis hierher hatte JEDER schreibende Vorgang eine
menschliche Bestaetigung im selben Moment, in dem geschrieben wurde. Ein
Warteauftrag trennt beides. Der Mensch bestaetigt heute Abend, die
Datenbank wird morgen Nachmittag geschrieben - ohne dass jemand ein
zweites Mal gefragt wird.

Dieses Modul ist die Buchhaltung dieser Auftraege: anlegen, auflisten,
stornieren, abschliessen. Es schreibt in KEINE Bot-Datenbank und ruft
KEINE Schliessfunktion auf. Ausgefuehrt wird ausschliesslich von
dashboard/warteauftraege_ausfuehren.py, und geschrieben wird auch dort
nicht selbst, sondern ueber manual_close.schliesse_position() - dieselbe
Kernfunktion mit derselben Transaktion, derselben erneuten Pruefung und
demselben Protokoll wie beim sofortigen Schliessen.

------------------------------------------------------------------------------
Warum EINE gemeinsame Datei und nicht eine je Bot
------------------------------------------------------------------------------
Beide Formen waeren machbar; entschieden wurde fuer eine gemeinsame,
aus vier Gruenden:

  1. Die Uebersichtsseite muss "welche Auftraege stehen ueberhaupt an"
     in EINER Abfrage beantworten koennen. Bei neun Dateien waere das ein
     Suchlauf, bei dem eine fehlende Datei und eine leere Datei gleich
     aussehen.
  2. Nebenlaeufigkeit gibt es dann an genau EINER Stelle. Das
     Ausfuehrungsskript und das Dashboard koennen gleichzeitig
     schreiben; eine Sperre je Bot waere neun Sperren, von denen acht
     nie geprueft wuerden.
  3. Die Mengen sind winzig. Es gibt einen Nutzer und hoechstens eine
     Handvoll Auftraege gleichzeitig - eine Aufteilung nach Bots loeste
     ein Groessenproblem, das es nicht gibt.
  4. Der Nutzer soll die Datei im Zweifel selbst lesen und notfalls
     loeschen koennen. Eine Datei mit fuenf Zeilen JSON ist dafuer der
     kuerzeste Weg; neun Dateien waeren neun Orte zum Nachsehen.

Bewusst NICHT gewaehlt wurde eine eigene SQLite-Datei. Sie braechte
Transaktionen mit, aber der Nutzen waere gering (die Sperre unten leistet
dasselbe fuer diese Datenmenge), und der Preis waere hoch: der Zustand
laege in einem Binaerformat, das man ohne Werkzeug nicht mehr
nachschauen und im Notfall nicht mit einem Texteditor geradeziehen kann.
Genau das will man aber koennen, wenn ein Auftrag im Feuer steht.

------------------------------------------------------------------------------
Nebenlaeufigkeit: zwei Prozesse, eine Datei
------------------------------------------------------------------------------
Das Dashboard (Anlegen, Stornieren) und der Cronjob (Ausfuehren,
Entfernen) laufen als GETRENNTE Prozesse und koennen sich exakt
ueberschneiden. Drei Massnahmen:

  1. EIGENE SPERRDATEI (`.lock`) statt einer Sperre auf der JSON-Datei
     selbst. Die Nutzdatei wird beim Schreiben ersetzt (siehe 2) - eine
     Sperre auf ihr haenge danach an einer Datei, die es nicht mehr gibt,
     und der naechste Prozess wuerde eine frische, ungesperrte Datei
     vorfinden. Die Sperrdatei wird nie ersetzt.
  2. ATOMARES SCHREIBEN: erst vollstaendig in eine Nebendatei, dann
     os.replace(). Ein Absturz mitten im Schreiben hinterlaesst damit
     entweder den alten oder den neuen Stand, nie einen halben.
  3. LESEN UND SCHREIBEN IN EINEM ZUG unter derselben Sperre
     (`_aendern()`). Wer eine Liste laedt, sie draussen aendert und
     zurueckschreibt, ueberschreibt in genau dem Moment die Aenderung des
     anderen Prozesses, in dem es darauf ankommt.

Was NICHT abgesichert werden muss: die Frage, ob eine Position noch
offen ist. Die entscheidet nicht diese Datei, sondern die Bot-Datenbank
selbst - innerhalb der Transaktion von manual_close.schliesse_position().
"""

import json
import os
import secrets
import sys
from datetime import datetime, timezone

try:
    import fcntl
except ImportError:                                # pragma: no cover
    fcntl = None                                   # Windows - siehe _sperre()

_NOTIF_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_NOTIF_DIR)

if _NOTIF_DIR not in sys.path:
    sys.path.insert(0, _NOTIF_DIR)

import manual_close  # noqa: E402

# Der Dateiname steht hier, der Ordner kommt aus BASE_DIR - genau wie in
# manual_close.py. Die Tests biegen BASE_DIR um; gaebe es hier einen
# fertig zusammengesetzten Pfad, liefe der Test gegen die echten
# Auftraege des Nutzers.
DATEINAME = "warteauftraege.json"
SPERR_DATEINAME = "warteauftraege.json.lock"

# Format-Version der Datei. Sie kostet jetzt nichts und erspaert spaeter
# das Raten, wenn sich der Aufbau je aendert.
FORMAT_VERSION = 1

# Obergrenze. Es gibt vier Aktien-Bots mit zusammen selten mehr als
# einem Dutzend offener Positionen; alles darueber ist ein Fehler und
# soll auffallen, statt eine Datei wachsen zu lassen, die niemand mehr
# ueberblickt.
MAX_AUFTRAEGE = 100

# Die Quelle, die im Protokoll und in der Datenbankzeile erscheint,
# wenn ein Warteauftrag tatsaechlich ausgefuehrt wird.
QUELLE_WARTEAUFTRAG = manual_close.QUELLE_WARTEAUFTRAG


class WarteauftragNichtMoeglich(Exception):
    """Fachlicher Abbruch mit einer Meldung, die dem Nutzer gezeigt
    werden darf. An jeder Stelle geworfen, an der NICHTS geaendert
    wurde."""


def datei() -> str:
    return os.path.join(BASE_DIR, "notifications", DATEINAME)


def _sperrdatei() -> str:
    return os.path.join(BASE_DIR, "notifications", SPERR_DATEINAME)


class _sperre:
    """Exklusive Sperre ueber die Dauer eines Lese-/Schreib-Vorgangs.

    Auf Systemen ohne fcntl (Windows) wird ohne Sperre gearbeitet - das
    Projekt laeuft auf macOS, und ein Ausfall der Sperre soll die
    Funktion nicht verhindern, sondern nur ihre Absicherung. Er wird
    dabei nicht verschwiegen: `ohne_sperre` steht in der Statusausgabe
    des Ausfuehrungsskripts.
    """

    ohne_sperre = fcntl is None

    def __enter__(self):
        if fcntl is None:                          # pragma: no cover
            self._handle = None
            return self
        os.makedirs(os.path.dirname(_sperrdatei()), exist_ok=True)
        self._handle = open(_sperrdatei(), "a+")
        fcntl.flock(self._handle.fileno(), fcntl.LOCK_EX)
        return self

    def __exit__(self, *_):
        if self._handle is None:                   # pragma: no cover
            return False
        try:
            fcntl.flock(self._handle.fileno(), fcntl.LOCK_UN)
        finally:
            self._handle.close()
        return False


def _leer() -> dict:
    return {"version": FORMAT_VERSION, "auftraege": []}


def _laden_ungesperrt() -> dict:
    pfad = datei()
    if not os.path.exists(pfad):
        return _leer()
    try:
        with open(pfad, encoding="utf-8") as fh:
            inhalt = json.load(fh)
    except (OSError, ValueError) as fehler:
        # Eine unlesbare Datei wird NICHT stillschweigend durch eine
        # leere ersetzt: das waere der lautlose Verlust von Auftraegen,
        # die der Nutzer bestaetigt hat. Stattdessen Abbruch mit
        # Meldung - dann kann er die Datei ansehen.
        raise WarteauftragNichtMoeglich(
            f"Die Datei mit den Warteauftraegen ({pfad}) ist nicht lesbar: "
            f"{fehler}. Es wurde nichts geaendert.")
    if not isinstance(inhalt, dict) or not isinstance(inhalt.get("auftraege"), list):
        raise WarteauftragNichtMoeglich(
            f"Die Datei mit den Warteauftraegen ({pfad}) hat einen "
            f"unerwarteten Aufbau. Es wurde nichts geaendert.")
    return inhalt


def _speichern_ungesperrt(inhalt: dict) -> None:
    pfad = datei()
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    vorlaeufig = pfad + ".neu"
    with open(vorlaeufig, "w", encoding="utf-8") as fh:
        json.dump(inhalt, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(vorlaeufig, pfad)


class _aendern:
    """Lesen, aendern, schreiben - alles unter EINER Sperre.

        with _aendern() as stand:
            stand["auftraege"].append(...)

    Geschrieben wird beim Verlassen, aber nur ohne Ausnahme: bricht der
    Block ab, bleibt die Datei unveraendert.
    """

    def __enter__(self):
        self._sperre = _sperre().__enter__()
        self._stand = _laden_ungesperrt()
        return self._stand

    def __exit__(self, art, *_):
        try:
            if art is None:
                _speichern_ungesperrt(self._stand)
        finally:
            self._sperre.__exit__(None, None, None)
        return False


def _jetzt_iso() -> str:
    """ISO-8601 MIT Offset - dieselbe Konvention wie in
    dashboard/datenquelle.py, damit der Browser den Zeitpunkt in die
    Zeitzone des Geraets umrechnen kann. Bewusst ein anderes Format als
    manual_close.jetzt_als_text(): das dort ist ein KERZEN-Zeitstempel
    fuer die Bot-Datenbank, das hier eine Wanduhrzeit fuer eine Anzeige."""
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Lesen
# ---------------------------------------------------------------------------

def alle() -> list:
    """Alle wartenden Auftraege, aelteste zuerst. Wirft nur, wenn die
    Datei kaputt ist (siehe _laden_ungesperrt)."""
    with _sperre():
        stand = _laden_ungesperrt()
    return sorted(stand["auftraege"], key=lambda a: (a.get("angefordert_am") or "",
                                                      a.get("id") or ""))


def fuer_bot(bot_name: str) -> list:
    return [a for a in alle() if a.get("bot") == bot_name]


def anzahl() -> int:
    return len(alle())


def finde(auftrag_id: str):
    for auftrag in alle():
        if auftrag["id"] == auftrag_id:
            return auftrag
    return None


# ---------------------------------------------------------------------------
# Anlegen
# ---------------------------------------------------------------------------

def anlegen(bot_name: str, trade_id, symbol: str, benutzer, quelle: str,
             entry_time=None, entry_price=None, boerse: dict = None) -> dict:
    """Merkt einen Ausstieg fuer die naechste Boersenoeffnung vor.

    SCHREIBT KEINE Bot-Datenbank. Der Auftrag ist eine Absicht, kein
    Ergebnis - er kann storniert werden, er kann uebersprungen werden
    (wenn der Bot die Position vorher selbst schliesst), und er nennt
    ausdruecklich KEINEN Kurs: der wird erst beim Ausfuehren geholt.
    Genau das ist der Zweck der ganzen Uebung.

    Der Bot muss ein AKTIEN-Bot sein. Fuer Krypto gibt es keinen Grund
    zu warten (Binance handelt rund um die Uhr), und ein Warteauftrag
    dort waere ein Ausstieg, der ohne Not verschoben wird - die Pruefung
    steht hier im Kern und nicht bloss in der Oberflaeche, damit sie
    nicht davon abhaengt, welcher Aufrufer sie sich merkt.
    """
    angaben = manual_close.SCHLIESSBARE_BOTS.get(bot_name)
    if angaben is None:
        raise WarteauftragNichtMoeglich(
            f"Fuer '{bot_name}' ist das manuelle Schliessen nicht "
            f"freigeschaltet - es kann auch kein Warteauftrag angelegt werden.")
    if angaben["anlageklasse"] != "aktien":
        raise WarteauftragNichtMoeglich(
            f"'{bot_name}' ist ein Krypto-Bot. Krypto wird rund um die Uhr "
            f"gehandelt; ein Warteauftrag waere dort ein grundlos "
            f"verschobener Ausstieg.")
    try:
        trade_id = int(trade_id)
    except (TypeError, ValueError):
        raise WarteauftragNichtMoeglich("Ungueltige Positions-Kennung.")

    with _aendern() as stand:
        for vorhanden in stand["auftraege"]:
            if vorhanden["bot"] == bot_name and vorhanden["trade_id"] == trade_id:
                raise WarteauftragNichtMoeglich(
                    f"Fuer {symbol} (Position {trade_id}) steht bereits ein "
                    f"Warteauftrag vom {vorhanden['angefordert_am']}. Es wurde "
                    f"kein zweiter angelegt.")
        if len(stand["auftraege"]) >= MAX_AUFTRAEGE:
            raise WarteauftragNichtMoeglich(
                f"Es stehen bereits {MAX_AUFTRAEGE} Warteauftraege. Das ist "
                f"weit mehr als vorgesehen - bitte erst die bestehenden "
                f"pruefen (Uebersichtsseite).")

        auftrag = {
            # Zufaellige Kennung statt fortlaufender Nummer: zwei
            # Prozesse koennen gleichzeitig anlegen, und eine hochgezaehlte
            # Nummer waere genau dort zweimal dieselbe.
            "id": secrets.token_hex(6),
            "bot": bot_name,
            "anzeigename": angaben["anzeigename"],
            "trade_id": trade_id,
            "symbol": symbol,
            "entry_time": entry_time,
            "entry_price": entry_price,
            "angefordert_am": _jetzt_iso(),
            "benutzer": str(benutzer),
            "quelle": quelle,
            # Der Boersenzustand IM MOMENT DER ANFORDERUNG. Nicht fuer
            # die Ausfuehrung (die fragt neu), sondern fuer den
            # Nachvollzug: "warum steht hier ein Auftrag" soll sich aus
            # dem Auftrag selbst beantworten lassen.
            "boerse_bei_anforderung": {
                "offen": (boerse or {}).get("offen"),
                "letzter_handelstag": (boerse or {}).get("letzter_handelstag"),
                "naechste_oeffnung": (boerse or {}).get("naechste_oeffnung"),
            },
            "versuche": 0,
            "letzter_versuch_am": None,
            "letzter_fehler": None,
        }
        stand["auftraege"].append(auftrag)

    manual_close.protokolliere_warteauftrag(
        "ANGELEGT", bot_name=bot_name, trade_id=trade_id, benutzer=benutzer,
        quelle=quelle,
        zusatz=(f"auftrag={auftrag['id']} symbol={symbol} "
                f"naechste_oeffnung={auftrag['boerse_bei_anforderung']['naechste_oeffnung']} "
                f"| Datenbank UNVERAENDERT - der Ausstieg wird erst bei "
                f"geoeffneter Boerse geschrieben"))
    return auftrag


# ---------------------------------------------------------------------------
# Stornieren - die risikosenkende Richtung
# ---------------------------------------------------------------------------

def stornieren(auftrag_id: str, benutzer, quelle: str) -> dict:
    """Nimmt einen Warteauftrag zurueck, bevor er ausgefuehrt wurde.

    BEWUSST OHNE zusaetzliche Bestaetigung. Stornieren verhindert einen
    Schreibzugriff, es loest keinen aus - die Absicherungen dieses
    Projekts richten sich gegen das versehentliche AUSLOESEN. Eine
    Rueckfrage an dieser Stelle wuerde im Ernstfall Zeit kosten und
    nichts schuetzen; im schlimmsten Fall ist ein zu Unrecht stornierter
    Auftrag mit zwei Klicks neu angelegt, waehrend ein zu Unrecht
    ausgefuehrter eine Zeile in der Live-Datenbank ist.
    """
    with _aendern() as stand:
        treffer = [a for a in stand["auftraege"] if a["id"] == auftrag_id]
        if not treffer:
            raise WarteauftragNichtMoeglich(
                f"Es gibt keinen Warteauftrag mit der Kennung '{auftrag_id}' - "
                f"vermutlich wurde er bereits ausgefuehrt oder storniert.")
        auftrag = treffer[0]
        stand["auftraege"] = [a for a in stand["auftraege"] if a["id"] != auftrag_id]

    manual_close.protokolliere_warteauftrag(
        "STORNIERT", bot_name=auftrag["bot"], trade_id=auftrag["trade_id"],
        benutzer=benutzer, quelle=quelle,
        zusatz=(f"auftrag={auftrag['id']} symbol={auftrag['symbol']} "
                f"angefordert_am={auftrag['angefordert_am']} | NICHT ausgefuehrt, "
                f"Datenbank unveraendert"))
    return auftrag


# ---------------------------------------------------------------------------
# Abschliessen - nur vom Ausfuehrungsskript benutzt
# ---------------------------------------------------------------------------

def abschliessen(auftrag_id: str, ereignis: str, benutzer, zusatz: str = "") -> bool:
    """Entfernt einen erledigten Auftrag (ausgefuehrt oder uebersprungen).

    Der Auftrag verschwindet aus der Datei; die Spur bleibt im Protokoll
    logs/notifications/manuelle_eingriffe.log. Ein zweites, hier
    gefuehrtes Archiv waere dieselbe Information an einer zweiten Stelle -
    und die beiden liefen frueher oder spaeter auseinander.
    """
    with _aendern() as stand:
        treffer = [a for a in stand["auftraege"] if a["id"] == auftrag_id]
        if not treffer:
            return False
        auftrag = treffer[0]
        stand["auftraege"] = [a for a in stand["auftraege"] if a["id"] != auftrag_id]

    manual_close.protokolliere_warteauftrag(
        ereignis, bot_name=auftrag["bot"], trade_id=auftrag["trade_id"],
        benutzer=benutzer, quelle=QUELLE_WARTEAUFTRAG,
        zusatz=f"auftrag={auftrag['id']} symbol={auftrag['symbol']} {zusatz}".strip())
    return True


def fehlversuch(auftrag_id: str, grund: str) -> None:
    """Ein Versuch ist gescheitert, der Auftrag BLEIBT stehen.

    Absicht: die haeufigste Ursache ist eine gerade gesperrte Datenbank
    (der Cronjob des Bots laeuft), und die ist beim naechsten Lauf in
    fuenf Minuten weg. Ein Auftrag, der beim ersten Stolpern verschwaende,
    waere ein stillschweigend nicht ausgefuehrter Ausstieg. Gezaehlt wird
    trotzdem - die Oberflaeche zeigt Versuche und letzten Fehler an,
    damit ein dauerhaft scheiternder Auftrag nicht unbemerkt bleibt.
    """
    with _aendern() as stand:
        for auftrag in stand["auftraege"]:
            if auftrag["id"] == auftrag_id:
                auftrag["versuche"] = int(auftrag.get("versuche") or 0) + 1
                auftrag["letzter_versuch_am"] = _jetzt_iso()
                auftrag["letzter_fehler"] = grund
                break


def alles_loeschen() -> None:
    """Nur fuer Tests und fuer den Notfall von Hand. Loescht die Datei."""
    with _sperre():
        if os.path.exists(datei()):
            os.remove(datei())

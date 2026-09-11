"""
Ist die US-Boerse GERADE offen? - der echte NYSE-Handelskalender
==============================================================================
Dieses Modul beantwortet genau eine Frage, und zwar fuer genau einen
Zweck: darf eine Aktien-Position JETZT zu einem belastbaren Kurs
geschlossen werden, oder muss der Ausstieg auf die naechste Oeffnung
warten (Warteauftrag, siehe notifications/warteauftraege.py)?

Es rechnet nichts, es schreibt nichts und es kennt weder Bots noch
Positionen. Es liest ausschliesslich einen Kalender.

------------------------------------------------------------------------------
Warum eine Bibliothek und keine Zeit-Faustregel
------------------------------------------------------------------------------
Die naheliegende Abkuerzung waere "Montag bis Freitag, 15:30-22:00
deutscher Zeit". Sie ist falsch, und zwar auf drei verschiedene Arten,
die alle regelmaessig eintreten:

  1. FEIERTAGE. Die NYSE hat neun bis zehn Feiertage im Jahr, mehrere
     davon beweglich (Thanksgiving = vierter Donnerstag im November,
     Good Friday nach dem Osterdatum, Memorial Day = letzter Montag im
     Mai). Faellt ein fester Feiertag auf ein Wochenende, verschiebt er
     sich auf Freitag oder Montag.
  2. VERKUERZTE HANDELSTAGE. An mehreren Tagen im Jahr schliesst die
     Boerse um 13:00 Ortszeit statt 16:00 - der Tag nach Thanksgiving,
     Heiligabend, der 3. Juli. Eine Faustregel wuerde dort drei Stunden
     lang behaupten, der Handel laufe noch.
  3. ZEITUMSTELLUNG. Die USA stellen an anderen Terminen um als Europa.
     Zwei- bis dreimal pro Jahr gibt es Wochen, in denen der Abstand
     zwischen Ortszeit hier und Boersenzeit dort NICHT die gewohnten
     sechs Stunden betraegt - eine in deutscher Ortszeit formulierte
     Regel liegt dann um eine Stunde daneben.

Jeder dieser drei Punkte fuehrt zu genau dem Fehler, den diese ganze
Funktion verhindern soll: ein Ausstieg zu einem Kurs, den es in diesem
Moment gar nicht gibt. Deshalb der echte Kalender.

GEWAEHLT: `pandas_market_calendars`. Begruendung siehe requirements.txt
und dashboard/README.md - kurz: es ist die verbreitetste Loesung fuer
genau diese Frage, kennt Feiertage UND verkuerzte Handelstage als
`market_close` je Tag (nicht bloss "Handelstag ja/nein"), liefert die
Zeiten zeitzonenbehaftet, braucht dafuer kein Netz und keinen Schluessel,
und die Abfrage kostet Millisekunden.

------------------------------------------------------------------------------
FAIL CLOSED: eine unbeantwortbare Frage ist NICHT "offen"
------------------------------------------------------------------------------
Fehlt die Bibliothek oder wirft der Kalender, dann ist `offen` weder
True noch False, sondern None - "unbekannt". Die Aufrufer behandeln
unbekannt wie geschlossen, aber sie sagen es dem Nutzer auch: ein
Warteauftrag, der wegen derselben fehlenden Bibliothek nie ausgefuehrt
werden koennte, waere die schlechteste aller Antworten - er saehe aus
wie ein Auftrag und waere in Wahrheit ein Stillstand. Deshalb wird in
diesem Fall abgelehnt und die fehlende Abhaengigkeit benannt, statt
etwas anzulegen oder etwas zu schreiben.

Was hier NICHT gemacht wird: eine Faustregel als Rueckfallebene. Eine
Naeherung, die nur dann greift, wenn die genaue Antwort fehlt, waere die
gefaehrlichste Variante von allen - sie wuerde genau in dem Moment
zuschlagen, in dem niemand mehr hinsieht.
"""

from datetime import datetime, timedelta, timezone

# Die Boerse, um die es geht. Alle vier Aktien-Bots handeln
# S&P-500-Werte; deren Heimatboerse ist die NYSE. Der NASDAQ-Kalender
# waere fuer diesen Zweck identisch (gleiche Feiertage, gleiche
# Handelszeiten, gleiche verkuerzten Tage) - eine zweite Unterscheidung
# nach Listing-Platz waere Aufwand ohne jeden Unterschied im Ergebnis.
KALENDER_NAME = "NYSE"

# Wie viele Tage um "jetzt" herum der Fahrplan gebaut wird. Er muss den
# letzten Handelstag DAVOR und die naechste Oeffnung DANACH enthalten;
# die laengste Luecke im NYSE-Kalender ist ein langes Feiertagswochenende
# von vier Tagen. Zehn Tage sind reichlich Puffer und kosten nichts -
# der Fahrplan wird ohnehin zwischengespeichert.
FAHRPLAN_TAGE = 10

try:
    import pandas as pd
    import pandas_market_calendars as mcal
    BIBLIOTHEK_FEHLER = None
except ImportError as fehler:                      # pragma: no cover
    pd = None
    mcal = None
    BIBLIOTHEK_FEHLER = (
        f"Die Bibliothek pandas_market_calendars ist nicht installiert "
        f"({fehler}). Ohne echten Boersenkalender wird fuer Aktien-Bots "
        f"weder sofort geschlossen noch ein Warteauftrag angelegt. "
        f"Installation: pip3 install -r requirements.txt")


def bibliothek_verfuegbar() -> bool:
    return BIBLIOTHEK_FEHLER is None


# Der Kalender und die zuletzt gebauten Fahrplaene. Beides ist reine
# Rechnung ohne Netz; zwischengespeichert wird trotzdem, weil das
# Dashboard die Frage bei jedem Seitenaufbau stellt und ein Fahrplan
# rund 20 Millisekunden kostet. Schluessel ist das Datumsfenster, nicht
# die Uhrzeit - innerhalb eines Tages wird derselbe Fahrplan benutzt.
_KALENDER = None
_FAHRPLAENE = {}


def _kalender():
    global _KALENDER
    if _KALENDER is None:
        _KALENDER = mcal.get_calendar(KALENDER_NAME)
    return _KALENDER


def _fahrplan(mitte):
    """Der Handelsfahrplan um einen Zeitpunkt herum: je Handelstag eine
    Zeile mit market_open und market_close, beide zeitzonenbehaftet und
    inklusive verkuerzter Schlusszeiten."""
    von = (mitte - timedelta(days=FAHRPLAN_TAGE)).date()
    bis = (mitte + timedelta(days=FAHRPLAN_TAGE)).date()
    schluessel = (von, bis)
    if schluessel not in _FAHRPLAENE:
        # Der Zwischenspeicher waechst sonst mit jedem Tag Laufzeit weiter.
        # Mehr als eine Handvoll Fenster ist nie gleichzeitig in Gebrauch.
        if len(_FAHRPLAENE) > 8:
            _FAHRPLAENE.clear()
        _FAHRPLAENE[schluessel] = _kalender().schedule(start_date=von, end_date=bis)
    return _FAHRPLAENE[schluessel]


def zwischenspeicher_leeren() -> None:
    """Nur fuer Tests: erzwingt den Neuaufbau des Fahrplans."""
    _FAHRPLAENE.clear()


def _als_utc(zeitpunkt):
    """Ein beliebiger Zeitpunkt -> zeitzonenbehaftet in UTC.

    Ein NAIVER Zeitstempel wird als UTC gelesen und nicht als Ortszeit
    des Rechners: alles andere im Projekt fuehrt Zeitpunkte ebenso (siehe
    manual_close.jetzt_als_text), und eine stillschweigend andere Lesart
    ausgerechnet hier waere im Sommer zwei Stunden Unterschied - genug,
    um die Boerse fuer offen zu halten, waehrend sie geschlossen ist.
    """
    if zeitpunkt is None:
        return datetime.now(timezone.utc)
    if isinstance(zeitpunkt, str):
        text = zeitpunkt.strip().replace(" ", "T")
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        zeitpunkt = datetime.fromisoformat(text)
    if zeitpunkt.tzinfo is None:
        return zeitpunkt.replace(tzinfo=timezone.utc)
    return zeitpunkt.astimezone(timezone.utc)


def _unbekannt(jetzt, grund: str) -> dict:
    return {
        "kalender": KALENDER_NAME,
        "jetzt": jetzt.isoformat(),
        "offen": None,
        "grund": grund,
        "letzter_handelstag": None,
        "letzter_schluss": None,
        "naechste_oeffnung": None,
        "naechster_schluss": None,
        "verkuerzter_handelstag": None,
    }


def status(jetzt=None) -> dict:
    """Der Zustand der Boerse zu einem Zeitpunkt (Standard: jetzt).

    Rueckgabe - alle Zeitpunkte als ISO-8601 MIT Offset, damit der
    Browser sie in die Zeitzone des Geraets umrechnen kann (dieselbe
    Konvention wie in dashboard/datenquelle.py):

        offen                  True | False | None (unbekannt)
        grund                  Klartext, warum - immer gesetzt
        letzter_handelstag     "2026-09-09" (Datum des letzten Schlusses)
        letzter_schluss        ISO-Zeitpunkt dieses Schlusses
        naechste_oeffnung      ISO-Zeitpunkt der naechsten Oeffnung
        naechster_schluss      ISO-Zeitpunkt des dazugehoerigen Schlusses
        verkuerzter_handelstag True, wenn der laufende bzw. naechste
                               Handelstag frueher schliesst als ueblich

    Wirft NIE. Jede Stoerung wird zu offen=None mit Begruendung - siehe
    Modul-Kopf (fail closed).
    """
    jetzt = _als_utc(jetzt)
    if BIBLIOTHEK_FEHLER:
        return _unbekannt(jetzt, BIBLIOTHEK_FEHLER)

    try:
        fahrplan = _fahrplan(jetzt)
        marke = pd.Timestamp(jetzt)

        offen_zeiten = fahrplan["market_open"]
        schluss_zeiten = fahrplan["market_close"]

        # OFFEN heisst: der Zeitpunkt liegt in einem der Handelsfenster
        # dieses Fahrplans. Bewusst NICHT ueber open_at_time() der
        # Bibliothek: die wirft, sobald der Zeitpunkt ausserhalb des
        # gebauten Fensters liegt, und dieser Sonderfall waere hier ein
        # Ausnahmepfad ohne Nutzen. Der Vergleich unten ist derselbe
        # Gedanke in zwei Zeilen und kommt ohne Ausnahme aus.
        laufend = (offen_zeiten <= marke) & (marke < schluss_zeiten)
        ist_offen = bool(laufend.any())

        vergangen = fahrplan[schluss_zeiten <= marke]
        letzter_schluss = vergangen["market_close"].iloc[-1] if len(vergangen) else None
        letzter_tag = vergangen.index[-1] if len(vergangen) else None

        kuenftig = fahrplan[offen_zeiten > marke]
        naechste_oeffnung = kuenftig["market_open"].iloc[0] if len(kuenftig) else None
        naechster_schluss = kuenftig["market_close"].iloc[0] if len(kuenftig) else None

        if ist_offen:
            zeile = fahrplan[laufend].iloc[0]
            naechster_schluss = zeile["market_close"]

        # Ein verkuerzter Handelstag ist einer, der frueher schliesst als
        # der uebliche Handelsschluss dieses Kalenders. Verglichen wird
        # die Ortszeit des Handelsplatzes, nicht die Dauer: eine Dauer
        # waere um die US-Zeitumstellung herum unauffaellig falsch.
        verkuerzt = None
        bezug = naechster_schluss if naechster_schluss is not None else letzter_schluss
        if bezug is not None:
            ortszeit = bezug.tz_convert(_kalender().tz)
            verkuerzt = bool((ortszeit.hour, ortszeit.minute) < (16, 0))

        ergebnis = {
            "kalender": KALENDER_NAME,
            "jetzt": jetzt.isoformat(),
            "offen": ist_offen,
            "grund": None,
            "letzter_handelstag": (letzter_tag.strftime("%Y-%m-%d")
                                    if letzter_tag is not None else None),
            "letzter_schluss": (letzter_schluss.to_pydatetime().isoformat()
                                 if letzter_schluss is not None else None),
            "naechste_oeffnung": (naechste_oeffnung.to_pydatetime().isoformat()
                                   if naechste_oeffnung is not None else None),
            "naechster_schluss": (naechster_schluss.to_pydatetime().isoformat()
                                   if naechster_schluss is not None else None),
            "verkuerzter_handelstag": verkuerzt,
        }
    except Exception as fehler:      # noqa: BLE001 - siehe Modul-Kopf
        return _unbekannt(jetzt, f"Der Boersenkalender liess sich nicht "
                                  f"auswerten ({fehler}). Es wird nichts "
                                  f"geschrieben und nichts vorgemerkt.")

    ergebnis["grund"] = _grundtext(ergebnis)
    return ergebnis


def _grundtext(zustand: dict) -> str:
    """Ein Satz in Klartext - fuer Protokoll und Kommandozeile.

    Die Oberflaeche baut ihre eigene Formulierung aus den EINZELWERTEN
    (siehe dashboard/static/app.js): dort sollen die Zeitpunkte in der
    Zeitzone des Geraets stehen, und ein hier vorformulierter Satz waere
    ein zweiter Text derselben Aussage - genau die Doppelfuehrung, die in
    diesem Projekt schon mehrfach auseinandergelaufen ist.
    """
    if zustand["offen"]:
        return (f"Die {zustand['kalender']} ist offen (Handelsschluss "
                f"{zustand['naechster_schluss']}).")
    teile = [f"Die {zustand['kalender']} ist geschlossen."]
    if zustand["letzter_handelstag"]:
        teile.append(f"Letzter Handelstag: {zustand['letzter_handelstag']}.")
    if zustand["naechste_oeffnung"]:
        teile.append(f"Naechste Oeffnung: {zustand['naechste_oeffnung']}.")
    return " ".join(teile)


def ist_offen(jetzt=None) -> bool:
    """Kurzform fuer Aufrufer, die nur die Entscheidung brauchen.
    UNBEKANNT gilt hier als NICHT offen - siehe Modul-Kopf."""
    return status(jetzt)["offen"] is True


if __name__ == "__main__":       # pragma: no cover
    # Handreichung fuer die Kommandozeile:  python3 notifications/boersenkalender.py
    import json
    import sys
    zeitpunkt = sys.argv[1] if len(sys.argv) > 1 else None
    print(json.dumps(status(zeitpunkt), indent=2, ensure_ascii=False))

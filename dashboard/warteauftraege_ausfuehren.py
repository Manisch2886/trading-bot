#!/usr/bin/env python3
"""
Warteauftraege ausfuehren - das erste Programm dieses Projekts, das OHNE
gleichzeitige menschliche Bestaetigung in eine Live-Datenbank schreibt
==============================================================================
Bitte diesen Absatz lesen, bevor der Cronjob eingerichtet wird.

Jeder bisherige Schreibzugriff dieses Projekts hatte eine Bestaetigung IM
SELBEN MOMENT: der Nutzer tippte, und daraufhin wurde geschrieben. Dieses
Skript trennt beides. Es laeuft per Cronjob, findet einen Auftrag, den
der Nutzer gestern Abend bestaetigt hat, und schreibt heute Nachmittag -
ohne zu fragen. Das ist gewollt (sonst waere die ganze Funktion sinnlos),
aber es ist eine neue Eigenschaft, und sie hat Folgen:

  * Wer den Cronjob einrichtet, erteilt eine VORAB-Erlaubnis fuer alle
    kuenftigen Auftraege, nicht fuer einen einzelnen.
  * Zwischen Bestaetigung und Ausfuehrung koennen Stunden bis Tage liegen
    (Wochenende, Feiertag). Der Markt bewegt sich in dieser Zeit.
  * Der Kurs, zu dem geschlossen wird, steht bei der Bestaetigung noch
    nicht fest. Er kann deutlich schlechter sein als der, den der Nutzer
    beim Bestaetigen gesehen hat - das ist der Preis dafuer, zu einem
    ECHTEN Kurs zu schliessen statt zu einem veralteten.
  * Der einzige Weg, das noch zu verhindern, ist das Stornieren des
    Auftrags im Dashboard - solange er noch wartet.

Was dieses Skript NICHT tut:
  * Es eroeffnet keine Position und veraendert keinen Parameter.
  * Es entscheidet nichts selbst. Es fuehrt aus, was ein Mensch
    bestaetigt hat, und nur das.
  * Es schreibt seine Datenbankzeile nicht selbst, sondern ruft
    manual_close.schliesse_position() auf - dieselbe Kernfunktion wie
    Telegram und Dashboard, mit BEGIN IMMEDIATE, busy_timeout, erneuter
    Pruefung innerhalb der Transaktion, rowcount==1 und Protokoll.
    Es gibt weiterhin genau EINE Stelle im Projekt, die schreibt.
  * Es fasst KEINEN Krypto-Bot an. Krypto wird rund um die Uhr gehandelt;
    dort gibt es keine Warteauftraege (siehe warteauftraege.anlegen).

------------------------------------------------------------------------------
Ablauf eines Laufs
------------------------------------------------------------------------------
1. Auftragsdatei lesen. Ist sie leer, endet das Skript sofort - ohne
   Kalender, ohne Netz, ohne Datenbankzugriff. Das ist der Normalfall
   und der Grund, warum ein enger Cron-Takt nichts kostet.
2. Boersenkalender fragen. Geschlossen oder unbekannt -> nichts tun, die
   Auftraege bleiben stehen. KEIN Schreibzugriff, keine Kursabfrage.
3. Fuer jeden faelligen Auftrag: ist die Position ueberhaupt noch offen?
   Wenn nein, hat der Bot sie regulaer selbst geschlossen - der Auftrag
   wird als UEBERSPRUNGEN abgeraeumt, nicht als Fehler gemeldet. Das ist
   der haeufigste Nicht-Ausfuehrungsgrund und ausdruecklich kein Problem.
4. Aktuelle Kurse holen - gebuendelt, ein Aufruf fuer alle Symbole, ueber
   monitor.fetch_stock_prices (dieselbe Funktion, die auch Dashboard und
   Telegram benutzen).
5. Schliessen, je Position einzeln, ueber die Kernfunktion.
6. Erfolg -> Auftrag entfernen. Fehlschlag -> Auftrag BLEIBT stehen, mit
   Zaehler und Grund; der naechste Lauf versucht es erneut. Der haeufigste
   Fehlschlag ist eine gerade gesperrte Datenbank (der Cronjob des Bots
   laeuft), und die ist in fuenf Minuten weg.

Aufruf:
    python3 dashboard/warteauftraege_ausfuehren.py            # Ernstfall
    python3 dashboard/warteauftraege_ausfuehren.py --trockenlauf
    python3 dashboard/warteauftraege_ausfuehren.py --jetzt "2026-09-10 15:45"

--trockenlauf sagt, was es taete, und schreibt nichts - weder in eine
Bot-Datenbank noch in die Auftragsdatei. Der erste Schritt der
Testanleitung.
--jetzt setzt den Zeitpunkt fuer die KALENDER-Frage (nicht fuer die
Kursabfrage) und ist fuer Tests gedacht: damit laesst sich pruefen, dass
an einem Feiertag nichts passiert, ohne bis zum naechsten zu warten.
"""

import argparse
import os
import sys
from datetime import datetime, timezone

_DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_DASHBOARD_DIR)
_NOTIFICATIONS_DIR = os.path.join(BASE_DIR, "notifications")
for _pfad in (_NOTIFICATIONS_DIR, _DASHBOARD_DIR):
    if _pfad not in sys.path:
        sys.path.insert(0, _pfad)

import boersenkalender  # noqa: E402
import manual_close     # noqa: E402
import monitor          # noqa: E402
import warteauftraege   # noqa: E402

# Wer den Eingriff ausgeloest hat - steht so im Protokoll. Bewusst nicht
# der Nutzername aus dem Auftrag: ausgeloest hat diesen Schreibzugriff der
# Cronjob, bestaetigt hat ihn der Nutzer. Beides steht in der Zeile, aber
# an der richtigen Stelle - der urspruengliche Besteller wird als
# `bestellt_von` mitprotokolliert.
BENUTZER = "warteauftrag-cronjob"


def _zeitstempel() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _sagen(text: str) -> None:
    print(f"{_zeitstempel()} {text}", flush=True)


def lauf(jetzt=None, trockenlauf: bool = False, kurse_holen=None) -> dict:
    """Ein vollstaendiger Durchlauf. Gibt eine Zusammenfassung zurueck.

    kurse_holen: nur fuer Tests - eine Funktion (symbole) -> {symbol: kurs}.
    Standard ist monitor.fetch_stock_prices, also genau die Abfrage, die
    auch das Dashboard benutzt.
    """
    kurse_holen = kurse_holen or monitor.fetch_stock_prices
    ergebnis = {
        "zeitpunkt": _zeitstempel(),
        "trockenlauf": trockenlauf,
        "auftraege_gesamt": 0,
        "geschlossen": [],
        "uebersprungen": [],
        "fehlgeschlagen": [],
        "wartend": [],
        "boerse": None,
        "meldung": "",
    }

    # -- 1. Auftragsdatei ---------------------------------------------------
    try:
        auftraege = warteauftraege.alle()
    except warteauftraege.WarteauftragNichtMoeglich as fehler:
        ergebnis["meldung"] = str(fehler)
        _sagen(f"ABBRUCH: {fehler}")
        return ergebnis

    ergebnis["auftraege_gesamt"] = len(auftraege)
    if not auftraege:
        ergebnis["meldung"] = "Keine Warteauftraege - nichts zu tun."
        return ergebnis

    # -- 2. Boersenkalender -------------------------------------------------
    zustand = boersenkalender.status(jetzt)
    ergebnis["boerse"] = zustand
    if zustand["offen"] is not True:
        # Geschlossen ODER unbekannt: in beiden Faellen passiert nichts.
        # Die Auftraege bleiben unveraendert stehen - genau dafuer sind sie da.
        ergebnis["wartend"] = [a["id"] for a in auftraege]
        ergebnis["meldung"] = (f"{len(auftraege)} Warteauftrag/-auftraege "
                                f"bleiben stehen. {zustand['grund']}")
        _sagen(ergebnis["meldung"])
        return ergebnis

    _sagen(f"Boerse offen ({zustand['kalender']}, Schluss "
           f"{zustand['naechster_schluss']}) - {len(auftraege)} Auftrag/"
           f"Auftraege werden geprueft.")

    # -- 3. Welche Positionen sind ueberhaupt noch offen? -------------------
    faellig, offen_je_bot = [], {}
    for auftrag in auftraege:
        bot = auftrag["bot"]
        angaben = manual_close.SCHLIESSBARE_BOTS.get(bot)
        if angaben is None or angaben["anlageklasse"] != "aktien":
            # Kann ueber die Oberflaeche nicht entstehen (warteauftraege.anlegen
            # laesst es nicht zu). Wenn es doch dasteht, wurde die Datei von
            # Hand bearbeitet - dann wird NICHT geschrieben, sondern gemeldet.
            # Ein Schreibzugriff auf Verdacht ist genau das, was hier nie
            # passieren darf.
            ergebnis["fehlgeschlagen"].append({
                "id": auftrag["id"], "bot": bot, "symbol": auftrag["symbol"],
                "grund": ("kein freigeschalteter Aktien-Bot - der Auftrag "
                           "wird NICHT ausgefuehrt. Bitte pruefen und ggf. im "
                           "Dashboard stornieren."),
            })
            continue

        if bot not in offen_je_bot:
            try:
                offen_je_bot[bot] = {p["id"]: p for p in
                                      manual_close.offene_positionen(bot)}
            except Exception as fehler:      # noqa: BLE001
                offen_je_bot[bot] = None
                _sagen(f"WARNUNG: Positionen von {bot} nicht lesbar - {fehler}")
        offene = offen_je_bot[bot]
        if offene is None:
            ergebnis["fehlgeschlagen"].append({
                "id": auftrag["id"], "bot": bot, "symbol": auftrag["symbol"],
                "grund": "Datenbank des Bots gerade nicht lesbar",
            })
            if not trockenlauf:
                warteauftraege.fehlversuch(auftrag["id"],
                                            "Datenbank nicht lesbar")
            continue

        if auftrag["trade_id"] not in offene:
            # DER haeufige Fall und ausdruecklich KEIN Fehler.
            ergebnis["uebersprungen"].append({
                "id": auftrag["id"], "bot": bot, "symbol": auftrag["symbol"],
                "grund": "bereits vom Bot selbst geschlossen",
            })
            if not trockenlauf:
                warteauftraege.abschliessen(
                    auftrag["id"], "UEBERSPRUNGEN", BENUTZER,
                    zusatz=("bereits vom Bot selbst geschlossen - "
                             "kein Fehler, Datenbank unveraendert"))
            continue

        faellig.append((auftrag, offene[auftrag["trade_id"]]))

    if not faellig:
        ergebnis["meldung"] = _zusammenfassung(ergebnis)
        _sagen(ergebnis["meldung"])
        return ergebnis

    # -- 4. Kurse holen, gebuendelt ----------------------------------------
    symbole = sorted({a["symbol"] for a, _ in faellig})
    try:
        kurse = kurse_holen(symbole) or {}
    except Exception as fehler:              # noqa: BLE001
        # Ohne Kurse wird nicht geschrieben. Die Auftraege bleiben stehen,
        # der naechste Lauf versucht es erneut.
        for auftrag, _ in faellig:
            ergebnis["fehlgeschlagen"].append({
                "id": auftrag["id"], "bot": auftrag["bot"],
                "symbol": auftrag["symbol"],
                "grund": f"Kursabfrage fehlgeschlagen: {fehler}"})
            if not trockenlauf:
                warteauftraege.fehlversuch(auftrag["id"],
                                            f"Kursabfrage fehlgeschlagen: {fehler}")
        ergebnis["meldung"] = _zusammenfassung(ergebnis)
        _sagen(ergebnis["meldung"])
        return ergebnis

    # -- 5. Schliessen ------------------------------------------------------
    for auftrag, position in faellig:
        kurs = kurse.get(auftrag["symbol"])
        kurs = float(kurs) if kurs else None
        if not kurs:
            ergebnis["fehlgeschlagen"].append({
                "id": auftrag["id"], "bot": auftrag["bot"],
                "symbol": auftrag["symbol"],
                "grund": "kein aktueller Kurs verfuegbar"})
            if not trockenlauf:
                warteauftraege.fehlversuch(auftrag["id"],
                                            "kein aktueller Kurs verfuegbar")
            continue

        if trockenlauf:
            ergebnis["geschlossen"].append({
                "id": auftrag["id"], "bot": auftrag["bot"],
                "trade_id": auftrag["trade_id"], "symbol": auftrag["symbol"],
                "exit_preis": kurs, "pnl_pct": None,
                "trockenlauf": True})
            continue

        try:
            geschrieben = manual_close.schliesse_position(
                auftrag["bot"], auftrag["trade_id"], kurs, BENUTZER,
                manual_close.BESTAETIGUNGSTEXT,
                quelle=manual_close.QUELLE_WARTEAUFTRAG)
        except manual_close.SchliessenNichtMoeglich as fehler:
            # Der Kern hat bereits protokolliert und garantiert, dass nichts
            # geschrieben wurde. Der Auftrag bleibt stehen.
            ergebnis["fehlgeschlagen"].append({
                "id": auftrag["id"], "bot": auftrag["bot"],
                "symbol": auftrag["symbol"], "grund": str(fehler)})
            warteauftraege.fehlversuch(auftrag["id"], str(fehler))
            _sagen(f"FEHLGESCHLAGEN: {auftrag['symbol']} ({auftrag['bot']}) - "
                   f"{fehler}")
            continue
        except Exception as fehler:          # noqa: BLE001
            ergebnis["fehlgeschlagen"].append({
                "id": auftrag["id"], "bot": auftrag["bot"],
                "symbol": auftrag["symbol"],
                "grund": f"unerwarteter Fehler: {fehler}"})
            warteauftraege.fehlversuch(auftrag["id"], f"unerwartet: {fehler}")
            _sagen(f"FEHLGESCHLAGEN (unerwartet): {auftrag['symbol']} - {fehler}")
            continue

        warteauftraege.abschliessen(
            auftrag["id"], "AUSGEFUEHRT", BENUTZER,
            zusatz=(f"exit_price={geschrieben['exit_price']} "
                     f"pnl_pct={geschrieben['pnl_pct']} "
                     f"bestellt_von={auftrag.get('benutzer')} "
                     f"bestellt_am={auftrag.get('angefordert_am')}"))
        ergebnis["geschlossen"].append({
            "id": auftrag["id"], "bot": auftrag["bot"],
            "trade_id": auftrag["trade_id"], "symbol": auftrag["symbol"],
            "exit_preis": geschrieben["exit_price"],
            "pnl_pct": geschrieben["pnl_pct"],
            "bestellt_am": auftrag.get("angefordert_am"),
        })
        _sagen(f"GESCHLOSSEN: {auftrag['symbol']} ({auftrag['bot']}) zu "
               f"{geschrieben['exit_price']} -> {geschrieben['pnl_pct']:+.2f} % "
               f"[quelle={manual_close.QUELLE_WARTEAUFTRAG}]")

    ergebnis["wartend"] = [a["id"] for a in warteauftraege.alle()]
    ergebnis["meldung"] = _zusammenfassung(ergebnis)
    _sagen(ergebnis["meldung"])
    return ergebnis


def _zusammenfassung(ergebnis: dict) -> str:
    teile = [f"{len(ergebnis['geschlossen'])} geschlossen",
             f"{len(ergebnis['uebersprungen'])} uebersprungen (vom Bot selbst "
             f"geschlossen)",
             f"{len(ergebnis['fehlgeschlagen'])} fehlgeschlagen"]
    satz = ", ".join(teile) + f"; von {ergebnis['auftraege_gesamt']} Auftraegen."
    if ergebnis["trockenlauf"]:
        satz = "TROCKENLAUF (nichts geschrieben): " + satz
    return satz


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description=("Fuehrt wartende Ausstiege aus, sobald die Boerse "
                      "geoeffnet hat. Schreibt ueber dieselbe Kernfunktion "
                      "wie das manuelle Schliessen."))
    zerleger.add_argument("--trockenlauf", action="store_true",
                           help="nur anzeigen, nichts schreiben")
    zerleger.add_argument("--ausfuehrlich", action="store_true",
                           help="auch dann etwas ausgeben, wenn nichts anlag")
    zerleger.add_argument("--jetzt", default=None,
                           help=("Zeitpunkt fuer die Kalenderfrage "
                                  "(ISO-8601), nur fuer Tests"))
    argumente = zerleger.parse_args(argv)

    ergebnis = lauf(jetzt=argumente.jetzt, trockenlauf=argumente.trockenlauf)

    # STILL, wenn es nichts zu tun gab. Der Cronjob laeuft alle paar
    # Minuten; eine Zeile "nichts zu tun" je Lauf waeren hunderte Zeilen am
    # Tag, in denen die eine interessante Zeile untergeht. Von Hand
    # aufgerufen soll das Skript dagegen antworten - deshalb sagt es beim
    # Trockenlauf und bei --ausfuehrlich immer etwas.
    if ergebnis["auftraege_gesamt"] or argumente.trockenlauf \
            or argumente.ausfuehrlich:
        if ergebnis["meldung"] and not ergebnis["geschlossen"] \
                and ergebnis["auftraege_gesamt"] == 0:
            _sagen(ergebnis["meldung"])

    # Rueckgabewert 0 auch bei Fehlschlaegen: ein stehengebliebener Auftrag
    # ist ein normaler Zustand (gesperrte Datenbank, kein Kurs), kein
    # Programmfehler. Ein Wert ungleich 0 wuerde bei cron eine Mail
    # ausloesen und damit eine Alltagssituation zum Alarm machen. Was
    # passiert ist, steht im Log und im Protokoll.
    return 0


if __name__ == "__main__":
    sys.exit(main())

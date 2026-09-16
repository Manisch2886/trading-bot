#!/usr/bin/env python3
"""
Selbsttests zu shared/umstellungstag.py (TB-38)
==============================================================================
Der Umstellungstag ist der Beginn des einzigen verwertbaren Vergleichsfensters
zwischen Backtest und Live. Geprueft wird hier vor allem das, was schiefgehen
KANN, ohne dass es auffiele:

* dass ein zweiter Aufruf den Zeitpunkt nicht stillschweigend vorrueckt
  (sonst waere das Vergleichsfenster kuerzer als das gemessene, und niemand
  saehe es),
* dass eine ausdrueckliche Korrektur den alten Wert nicht loescht,
* dass eine beschaedigte Datei NICHT durch ein leeres Geruest ersetzt wird.

Keine dieser Pruefungen fasst die echte `docs/...json` an - alle laufen
gegen eine Datei unter /tmp.

Nutzung:  python3 shared/test_umstellungstag.py
"""

import datetime as dt
import json
import os
import sys
import tempfile

_SHARED = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED)
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

import umstellungstag as ut                                    # noqa: E402

BESTANDEN = 0
FEHLER = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
    else:
        FEHLER.append(f"{name}" + (f"  [{detail}]" if detail else ""))


def test_neun_bots():
    check("1.1 es sind genau neun Bots", len(ut.BOTS) == 9, str(len(ut.BOTS)))
    check("1.2 jeder Bot hat Intervall und Markt",
          all(set(w) == {"intervall", "markt"} for w in ut.BOTS.values()))
    check("1.3 die Liste kommt aus entscheidungskerze, nicht aus einer "
          "zweiten Aufzaehlung",
          set(ut.BOTS) == {n for n, _i, _m in
                           __import__("entscheidungskerze")._BOTS})
    # Und sie stimmt mit den Ordnern unter strategies/ ueberein.
    import glob                                              # noqa: PLC0415
    ordner = {os.path.basename(os.path.dirname(p)) for p in
              glob.glob(os.path.join(BASE_DIR, "strategies", "*",
                                     "forward_test.py"))}
    check("1.4 die neun Namen sind die neun Ordner unter strategies/",
          set(ut.BOTS) == ordner, str(sorted(set(ut.BOTS) ^ ordner)))


def test_festhalten():
    with tempfile.TemporaryDirectory() as tmp:
        pfad = os.path.join(tmp, "umstellung.json")

        jetzt = dt.datetime(2026, 9, 16, 8, 0, 0)
        neu, uebersprungen = ut.festhalten(["t3_supertrend"], pfad, jetzt,
                                           rechner="pruefrechner")
        check("2.1 der erste Aufruf haelt fest",
              neu == ["t3_supertrend"] and not uebersprungen,
              f"{neu} / {uebersprungen}")

        daten = ut.lesen(pfad)
        eintrag = daten["bots"]["t3_supertrend"]
        check("2.2 Zeitpunkt in UTC mit Sekunden",
              eintrag["umgestellt_am"] == "2026-09-16T08:00:00Z",
              eintrag["umgestellt_am"])
        check("2.3 Intervall und Markt stehen dabei",
              eintrag["intervall"] == "4h" and eintrag["markt"] == "krypto")
        check("2.4 vorher/nachher stehen im Klartext dabei",
              "laufende" in eintrag["vorher"].lower()
              and "Entscheidungskerze" in eintrag["nachher"])

        # Der zweite Aufruf darf den Zeitpunkt NICHT vorruecken.
        spaeter = dt.datetime(2026, 10, 1, 8, 0, 0)
        neu, uebersprungen = ut.festhalten(["t3_supertrend"], pfad, spaeter)
        check("2.5 ein zweiter Aufruf rueckt den Zeitpunkt nicht vor",
              not neu and uebersprungen == ["t3_supertrend"],
              f"{neu} / {uebersprungen}")
        check("2.6 der Zeitpunkt steht unveraendert da",
              ut.lesen(pfad)["bots"]["t3_supertrend"]["umgestellt_am"]
              == "2026-09-16T08:00:00Z")

        # Eine ausdrueckliche Korrektur ueberschreibt - aber verliert nichts.
        neu, _u = ut.festhalten(["t3_supertrend"], pfad, spaeter, erneut=True)
        eintrag = ut.lesen(pfad)["bots"]["t3_supertrend"]
        check("2.7 --erneut setzt den neuen Zeitpunkt",
              eintrag["umgestellt_am"] == "2026-10-01T08:00:00Z",
              eintrag["umgestellt_am"])
        check("2.8 --erneut bewahrt den alten Zeitpunkt als 'frueher'",
              len(eintrag.get("frueher", [])) == 1
              and eintrag["frueher"][0]["umgestellt_am"]
              == "2026-09-16T08:00:00Z", str(eintrag.get("frueher")))

        # Ein unbekannter Bot ist ein Fehler, keine stille Zeile.
        try:
            ut.festhalten(["gibtesnicht"], pfad, jetzt)
            check("2.9 ein unbekannter Bot wird abgelehnt", False,
                  "kein Fehler geworfen")
        except ValueError as fehler:
            check("2.9 ein unbekannter Bot wird abgelehnt",
                  "gibtesnicht" in str(fehler))


def test_fehlende_und_kaputt():
    with tempfile.TemporaryDirectory() as tmp:
        pfad = os.path.join(tmp, "umstellung.json")
        check("3.1 ohne Datei fehlen alle neun",
              len(ut.fehlende(pfad)) == 9)
        ut.festhalten(sorted(ut.BOTS), pfad, dt.datetime(2026, 9, 16, 8, 0))
        check("3.2 nach --alle fehlt keiner", ut.fehlende(pfad) == [])

        # Eine beschaedigte Datei wird NICHT durch ein leeres Geruest ersetzt.
        with open(pfad, "w", encoding="utf-8") as datei:
            datei.write('{"etwas": "anderes"}')
        try:
            ut.lesen(pfad)
            check("3.3 eine fremde Datei wird nicht stillschweigend "
                  "ueberschrieben", False, "kein Fehler geworfen")
        except ValueError:
            check("3.3 eine fremde Datei wird nicht stillschweigend "
                  "ueberschrieben", True)

        # Auch `festhalten` fasst sie dann nicht an.
        vorher = open(pfad, encoding="utf-8").read()
        try:
            ut.festhalten(["t3_supertrend"], pfad,
                          dt.datetime(2026, 9, 16, 8, 0))
        except ValueError:
            pass
        check("3.4 und sie bleibt unveraendert liegen",
              open(pfad, encoding="utf-8").read() == vorher)


def test_kommandozeile():
    with tempfile.TemporaryDirectory() as tmp:
        pfad = os.path.join(tmp, "umstellung.json")
        check("4.1 --pruefen gibt 1 zurueck, solange ein Bot fehlt",
              ut.main(["--pruefen", "--datei", pfad]) == 1)
        check("4.2 --festhalten ohne Namen ist ein Bedienfehler",
              ut.main(["--festhalten", "--datei", pfad]) == 2)
        check("4.3 zwei Betriebsarten gleichzeitig sind ein Bedienfehler",
              ut.main(["--festhalten", "--zeigen", "--datei", pfad]) == 2)
        check("4.4 --festhalten --alle geht durch",
              ut.main(["--festhalten", "--alle", "--datei", pfad]) == 0)
        check("4.5 danach gibt --pruefen 0 zurueck",
              ut.main(["--pruefen", "--datei", pfad]) == 0)
        check("4.6 --zeigen geht durch",
              ut.main(["--zeigen", "--datei", pfad]) == 0)
        daten = json.load(open(pfad, encoding="utf-8"))
        check("4.7 die Datei ist lesbares JSON mit neun Eintraegen",
              len(daten["bots"]) == 9, str(len(daten.get("bots", {}))))
        check("4.8 die Datei erklaert sich selbst",
              "Vergleich" in daten.get("beschreibung", ""))


def main():
    print("=" * 78)
    print("Selbsttests shared/umstellungstag.py (TB-38)")
    print("=" * 78)
    test_neun_bots()
    test_festhalten()
    test_fehlende_und_kaputt()
    test_kommandozeile()
    print("\n" + "=" * 78)
    if FEHLER:
        print(f"{len(FEHLER)} FEHLER von {BESTANDEN + len(FEHLER)} Pruefungen:")
        for zeile in FEHLER:
            print(f"  - {zeile}")
        return 1
    print(f"Alle {BESTANDEN} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

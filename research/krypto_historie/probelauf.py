#!/usr/bin/env python3
"""
Probelauf des Historien-Laders gegen erzeugte Beispieldaten (TB-31)
==============================================================================
**Warum es diesen Probelauf gibt.** `api.binance.com` ist aus der
Cloud-Umgebung nicht erreichbar - die Egress-Richtlinie beantwortet den
CONNECT mit 403. Der echte Ladelauf gehoert deshalb auf den Mac des Nutzers
(Schritt 6 des Testauftrags). Damit der Lader trotzdem **am echten
Altbestand** belegt ist und nicht nur an Spielzeugdaten, laeuft er hier
gegen eine nachgebildete Gegenstelle, die

* im ueberlappenden Bereich **exakt die Zeilen der echten Repo-Datei**
  ausliefert - das ist der Fall "Ueberlappung identisch", und
* davor eine **erzeugte** Vorgeschichte ab dem angenommenen Listing-Datum.

Die Vorgeschichte ist erzeugt und als solche gekennzeichnet. Was der
Probelauf belegt, ist deshalb **nicht** "die Kurse stimmen" - das kann nur
der Lauf gegen den echten Endpunkt -, sondern: der Lader verlaengert die
echten Dateien dieses Repos korrekt, laesst ihre vorhandenen Zeilen
zeichengleich stehen, wiederholt sich, und faellt ueber die bekannte
fuehrende Teilkerze der abgeleiteten `*_1d.csv` genau so, wie er soll.

Es wird **nichts unter `data/` geschrieben** - der Probelauf arbeitet in
einem Temporaerordner auf Kopien.

    python3 research/krypto_historie/probelauf.py
    python3 research/krypto_historie/probelauf.py --symbole BTCUSDT,SUIUSDT
"""

import argparse
import datetime as dt
import json
import os
import shutil
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_HIER))
_SHARED_DIR = os.path.join(BASE_DIR, "shared")
if _SHARED_DIR not in sys.path:
    sys.path.insert(0, _SHARED_DIR)

import binance_historie as bh                              # noqa: E402
# Dieselbe nachgebildete Gegenstelle wie im Selbsttest - kein zweiter
# Nachbau, der davon auseinanderlaufen koennte.
from test_binance_historie import FalscheBinance, stille_drossel   # noqa: E402

ANNAHMEN = os.path.join(_HIER, "daten", "annahme_listing.json")
VORAUSWAHL = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SUIUSDT", "UUSDT"]

bestanden = 0
gescheitert = []


def pruefe(was, bedingung, hinweis=""):
    global bestanden
    if bedingung:
        bestanden += 1
        print(f"    OK    {was}")
    else:
        gescheitert.append(was)
        print(f"    FEHLT {was}" + (f"   [{hinweis}]" if hinweis else ""))


def lies_datei(pfad):
    with open(pfad, "r", encoding="utf-8", newline="") as datei:
        return datei.read()


def ms(zeitpunkt):
    return int(zeitpunkt.replace(tzinfo=dt.timezone.utc).timestamp() * 1000)


def echte_zeilen_als_kerzen(pfad, intervall):
    """Die Zeilen der echten Repo-Datei in der Feldform des Endpunkts."""
    kerzen = []
    with open(pfad, "r", encoding="utf-8") as datei:
        datei.readline()
        for zeile in datei:
            felder = zeile.strip().split(",")
            if len(felder) != 6:
                continue
            zeitpunkt = dt.datetime.strptime(felder[0], bh.ZEITFORMAT[intervall])
            kerzen.append((ms(zeitpunkt), float(felder[1]), float(felder[2]),
                           float(felder[3]), float(felder[4]), float(felder[5])))
    return kerzen


def erzeugte_vorgeschichte(symbol, intervall, von_ms, bis_ms, anschlusspreis):
    """Eine erzeugte, aber deterministische Vorgeschichte.

    Deterministisch, damit ein zweiter Probelauf dieselben Zahlen erzeugt -
    sonst waere die Wiederholbarkeitsprobe wertlos. Der Preispfad laeuft
    rueckwaerts vom ersten echten Kurs aus, damit der Uebergang keine
    Sprungstelle bekommt, an der ein Backtest haengen bliebe.
    """
    schrittweite = bh.INTERVALL_MS[intervall]
    zeiten = list(range(von_ms, bis_ms, schrittweite))
    if not zeiten:
        return []
    zustand = (abs(hash(symbol)) % 9973) + 1
    preise = []
    preis = float(anschlusspreis)
    for _ in zeiten:
        zustand = (1103515245 * zustand + 12345) % 2147483648
        preis = max(preis * (1.0 + ((zustand % 2001) - 1000) / 400000.0), 1e-8)
        preise.append(preis)
    preise.reverse()

    kerzen = []
    for i, (zeit, p) in enumerate(zip(zeiten, preise)):
        naechster = preise[i + 1] if i + 1 < len(preise) else anschlusspreis
        hoch = max(p, naechster) * 1.002
        tief = min(p, naechster) * 0.998
        kerzen.append((zeit, round(p, 8), round(hoch, 8), round(tief, 8),
                       round(naechster, 8), round(100.0 + (zustand % 500), 8)))
    return kerzen


def baue_gegenstelle(symbol, intervall, pfad, listing):
    """Vorgeschichte + echte Zeilen, in der Form, die der Endpunkt liefert.

    Der Sonderfall `1d` ist absichtlich eingebaut: die abgeleiteten
    Tagesdateien beginnen mit einer **Teilkerze** (nur 11 statt 24 Stunden,
    weil die 1h-Reihe am 2021-09-01 erst um 13:00 einsetzt). Die
    Gegenstelle liefert an dieser Stelle die **volle** Tageskerze - genau
    die Abweichung, die der Lader finden muss.
    """
    echt = echte_zeilen_als_kerzen(pfad, intervall)
    if not echt:
        return None, 0
    erster_echter = echt[0][0]
    listing_ms = ms(dt.datetime.combine(listing, dt.time(0, 0)))
    schrittweite = bh.INTERVALL_MS[intervall]
    beginn = listing_ms - (listing_ms % schrittweite)
    if beginn >= erster_echter:
        return None, 0

    if intervall == "1d":
        # Die erste echte Zeile wird durch eine volle Tageskerze ersetzt.
        ueberlappung = echt[1:]
        bis = erster_echter + schrittweite
    else:
        ueberlappung = echt
        bis = erster_echter

    vor = erzeugte_vorgeschichte(symbol, intervall, beginn, bis, echt[0][1])
    if intervall == "1d" and vor:
        # Die volle Tageskerze uebernimmt Schluss und Tief der Teilkerze,
        # oeffnet aber am Tagesanfang - so sieht eine native Kerze aus.
        teil = echt[0]
        letzte = vor[-1]
        vor[-1] = (teil[0], letzte[1], max(letzte[2], teil[2]),
                   min(letzte[3], teil[3]), teil[4], round(teil[5] / 0.45, 8))
    return {(symbol, intervall): vor + ueberlappung}, len(vor) - (1 if intervall == "1d" else 0)


def lauf_fuer(symbol, intervall, quelle, arbeitsordner, listing):
    pfad = os.path.join(arbeitsordner, f"{symbol}_{intervall}.csv")
    shutil.copy2(quelle, pfad)
    reihen, erwartet_neu = baue_gegenstelle(symbol, intervall, pfad, listing)
    if reihen is None:
        print(f"    (uebersprungen: Listing {listing} liegt nicht vor dem Dateibeginn)")
        return None

    def frisch():
        return bh.Abrufer(drossel=stille_drossel(mindestpause=0.0),
                          oeffner=FalscheBinance(reihen))

    vorher = lies_datei(pfad)
    alt_zeilen = vorher.splitlines()[1:]

    ergebnis = bh.verlaengere_datei(frisch(), pfad, symbol, intervall)
    if intervall == "1d":
        pruefe("die fuehrende Teilkerze wird gefunden und blockiert das Schreiben",
               not ergebnis["geschrieben"]
               and "--teilkerze-ersetzen" in (ergebnis["grund"] or ""),
               f"{ergebnis['grund']}")
        pruefe("die Datei ist dabei unveraendert geblieben", lies_datei(pfad) == vorher)
        ergebnis = bh.verlaengere_datei(frisch(), pfad, symbol, intervall,
                                        teilkerze_ersetzen=True)

    pruefe("die Ueberlappung stimmt ueberein",
           bh.harte_befunde(ergebnis["befunde"]) == []
           or (intervall == "1d" and ergebnis["geschrieben"]),
           f"{bh.harte_befunde(ergebnis['befunde'])[:1]}")
    pruefe("die Datei wurde verlaengert", ergebnis["geschrieben"])
    pruefe(f"um die erwarteten {erwartet_neu} Zeilen",
           ergebnis["neue_zeilen"] == erwartet_neu,
           f"{ergebnis['neue_zeilen']} statt {erwartet_neu}")

    neu_zeilen = lies_datei(pfad).splitlines()[1:]
    versetzt = ergebnis["neue_zeilen"] + (1 if intervall == "1d" else 0)
    unveraendert = alt_zeilen[1:] if intervall == "1d" else alt_zeilen
    pruefe("die vorhandenen Zeilen stehen zeichengleich da",
           neu_zeilen[versetzt:] == unveraendert)
    pruefe("keine Luecke im vorhandenen Bereich", not ergebnis["luecken"],
           f"{ergebnis['luecken'][:3]}")
    pruefe("keine unvollstaendige Kerze in der Vorgeschichte",
           ergebnis["gestrichene_kerzen"] == 0)

    nach_erstem = lies_datei(pfad)
    bh.verlaengere_datei(frisch(), pfad, symbol, intervall, teilkerze_ersetzen=True)
    pruefe("ein zweiter Lauf laesst die Datei byte-identisch",
           lies_datei(pfad) == nach_erstem)
    return ergebnis


def main(argv=None) -> int:
    from symbols_config import SYMBOLS                     # noqa: PLC0415

    zerleger = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    zerleger.add_argument("--symbole", default=",".join(VORAUSWAHL))
    zerleger.add_argument("--alle", action="store_true")
    zerleger.add_argument("--zeitrahmen", default="1h,4h,1d")
    argumente = zerleger.parse_args(argv)

    with open(ANNAHMEN, "r", encoding="utf-8") as datei:
        annahmen = json.load(datei)
    listing = {s: dt.date.fromisoformat(v["1h"]["beginn_tag"])
               for s, v in annahmen["messung"].items()}
    herkunft = annahmen["herkunft"]

    symbole = (list(SYMBOLS) if argumente.alle
               else [s.strip() for s in argumente.symbole.split(",") if s.strip()])
    zeitrahmen = [z.strip() for z in argumente.zeitrahmen.split(",") if z.strip()]

    print("=" * 78)
    print("Probelauf des Historien-Laders gegen ERZEUGTE Beispieldaten")
    print("=" * 78)
    print("Die Vorgeschichte ist erzeugt, nicht abgerufen. Der ueberlappende")
    print("Bereich sind die echten Zeilen der Repo-Dateien. Es wird nichts")
    print("unter data/ geschrieben.\n")

    datenordner = os.path.join(BASE_DIR, "data")
    with tempfile.TemporaryDirectory() as arbeitsordner:
        for symbol in symbole:
            if symbol not in listing:
                print(f"  {symbol}: kein Listing-Datum hinterlegt - uebersprungen")
                continue
            for intervall in zeitrahmen:
                quelle = os.path.join(datenordner, f"{symbol}_{intervall}.csv")
                if not os.path.exists(quelle):
                    continue
                print(f"\n  {symbol} {intervall}  (Listing {listing[symbol]}, "
                      f"{herkunft.get(symbol, '?')})")
                lauf_fuer(symbol, intervall, quelle, arbeitsordner, listing[symbol])

    print("\n" + "=" * 78)
    if gescheitert:
        print(f"{bestanden} bestanden, {len(gescheitert)} GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
        return 1
    print(f"{bestanden}/{bestanden} Pruefungen bestanden.")
    print("\nDie Kurswerte der Vorgeschichte sind erzeugt. Belegt ist der ABLAUF,")
    print("nicht der Kursinhalt - den belegt erst der Lauf gegen den echten")
    print("Endpunkt (Schritt 6 des Testauftrags).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

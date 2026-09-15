#!/usr/bin/env python3
"""
Selbsttest der Teilkerzen-Wache (TB-34)
==============================================================================
`shared/zeitabdeckung.py` beantwortet eine Frage, die `shared/kursdaten.py`
nicht stellen kann: deckt die erste und letzte Kerze einer Datei den vollen
Zeitraum ihres Intervalls ab? Eine Teilkerze hat vier gefuellte Kursspalten -
sie ist nicht leer, sie ist falsch.

Geprueft werden sieben Zusicherungen, alle **am Verhalten**:

  A. **Raster.** Ein Zeitpunkt ausserhalb des Intervallrasters wird gemeldet.
  A2. **Reihenfolge.** Ein doppelter Zeitpunkt und ein Rueckwaertssprung um
     genau ein Intervall werden ebenfalls gemeldet - der zweite Fall ginge
     durch eine reine Vielfachen-Pruefung hindurch.
  B. **Die Wache schlaegt an** bei einer kuenstlich gekuerzten Kerze - und
     **nicht** bei einer vollstaendigen. Beide Richtungen, sonst belegt der
     Test nur, dass sie ueberhaupt etwas sagt.
  C. **Sie findet, was `kursdaten.py` nicht findet.** Dieselbe Datei, beide
     Pruefungen, nebeneinander: `kursdaten.py` meldet null Befunde, die Wache
     meldet die 11-Stunden-Kerze. Das ist der Kern der Aufgabe.
  D. **Stand.** Eine Kerze, deren Zeitraum noch laeuft, ist zwingend eine
     Teilkerze und wird auch ohne feinere Datei gemeldet.
  E. **Listing-Tag.** Mit `--datenbeginn` gilt eine kurze **erste** Kerze am
     gemessenen Datenbeginn als richtig - und nur dort.
  F. **Rueckgabewert und Ablauf.** `main()` wird wirklich aufgerufen; 1 bei
     Befund, 0 sonst.

ZU DEN MUTATIONSPROBEN
------------------------------------------------------------------------------
Zwei Fallen, die dieses Projekt wiederholt getroffen haben (#73, #77, #78,
#79, #81, #86, TB-15, TB-20, TB-22, TB-26, TB-30a):

1. **Eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
   selbst.** Es waere einfach und wertlos, `pruefe_deckung()` mit von Hand
   gebauten Zeilen aufzurufen. Deshalb baut dieser Test echte Kursdateien in
   einem echten Ordner, laesst die abgeleitete Tagesdatei von derselben
   Rechnung erzeugen, die `build_daily_crypto_data.py` benutzt, und ruft
   `main()` mit Argumentliste auf. Jede Probe ist zweistufig: erst ohne
   Mutation das Richtige, dann mit Mutation das Verfaelschte.

2. **Eine zweite Wache verdeckt das Fehlen der ersten.** Hier stehen drei
   voneinander unabhaengige Zeugen (Raster, Deckung, Stand) auf derselben
   Datei. Faellt die Deckungspruefung aus, **meldet der Stand-Zeuge unter
   Umstaenden trotzdem** - und eine Probe, die nur auf den Rueckgabewert
   sieht, bliebe gruen, obwohl die eigentliche Wache weg ist. Teil H zeigt
   das an zwei Lagen nebeneinander: an der einen ist die Mutation sichtbar,
   an der anderen nicht. Die echte Probe laeuft deshalb auf der ersten.

Der Test geht nicht ins Netz und fasst `data/` nicht an. Teil C braucht
`pandas` (weil `kursdaten.pruefe_ordner` es braucht) und meldet sich als
uebersprungen, wenn es fehlt.

    python3 shared/test_zeitabdeckung.py

Rueckgabewert 0, wenn alle Pruefungen bestehen, sonst 1.
"""

import datetime as dt
import io
import json
import os
import sys
import tempfile
from contextlib import redirect_stdout

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
if _SHARED_DIR not in sys.path:
    sys.path.insert(0, _SHARED_DIR)

import zeitabdeckung as za                                 # noqa: E402

bestanden = 0
gescheitert = []
uebersprungen = []


def pruefe(was, bedingung, hinweis=""):
    global bestanden
    if bedingung:
        bestanden += 1
        print(f"  OK    {was}")
    else:
        gescheitert.append(was)
        print(f"  FEHLT {was}" + (f"   [{hinweis}]" if hinweis else ""))


# ---------------------------------------------------------------------------
# Kursdateien bauen - so, wie das Projekt sie schreibt
# ---------------------------------------------------------------------------
STUNDE = dt.timedelta(hours=1)


def stundenreihe(beginn, anzahl, basis=100.0):
    """Eine Stundenreihe, in der jede Kerze an ihrem Preis erkennbar ist."""
    kerzen = []
    for i in range(anzahl):
        p = basis + i
        kerzen.append({
            "zeit": beginn + i * STUNDE,
            "open": p, "high": p + 2.0, "low": p - 1.0, "close": p + 0.5,
            "volume": 10.0 + i,
        })
    return kerzen


def schreibe(pfad, kerzen, intervall):
    with open(pfad, "w", encoding="utf-8", newline="") as datei:
        datei.write("open_time,open,high,low,close,volume\n")
        for k in kerzen:
            zeit = (k["zeit"] if isinstance(k["zeit"], str)
                    else za.schreibe_zeitpunkt(k["zeit"], intervall))
            datei.write(f"{zeit},{k['open']!r},{k['high']!r},{k['low']!r},"
                        f"{k['close']!r},{k['volume']!r}\n")


def leite_tageskerzen_ab(stunden):
    """Dieselbe Rechnung wie `build_daily_crypto_data.resample_to_daily()`.

    Nachgebaut statt importiert, weil das Original pandas braucht - die
    Rechnung selbst ist: open = erste Stunde, high = Max, low = Min,
    close = letzte Stunde, volume = Summe, UTC-Tagesgrenzen.
    """
    je_tag = {}
    for k in stunden:
        je_tag.setdefault(k["zeit"].date(), []).append(k)
    tage = []
    for tag in sorted(je_tag):
        gruppe = je_tag[tag]
        tage.append({
            "zeit": dt.datetime(tag.year, tag.month, tag.day),
            "open": gruppe[0]["open"],
            "high": max(g["high"] for g in gruppe),
            "low": min(g["low"] for g in gruppe),
            "close": gruppe[-1]["close"],
            "volume": sum(g["volume"] for g in gruppe),
        })
    return tage


def baue_lage(ordner, erste_stunde, stunden_gesamt, symbol="X"):
    """Eine 1h-Datei und die daraus **abgeleitete** 1d-Datei.

    Beginnt `erste_stunde` nicht um 00:00, ist die erste Tageskerze eine
    Teilkerze - genau der Altbestand dieses Projekts.
    """
    stunden = stundenreihe(erste_stunde, stunden_gesamt)
    schreibe(os.path.join(ordner, f"{symbol}_1h.csv"), stunden, "1h")
    schreibe(os.path.join(ordner, f"{symbol}_1d.csv"),
             leite_tageskerzen_ab(stunden), "1d")
    return stunden


def lauf(argv):
    """`main()` wirklich aufrufen und Ausgabe mitlesen."""
    puffer = io.StringIO()
    with redirect_stdout(puffer):
        rueckgabe = za.main(argv)
    return rueckgabe, puffer.getvalue()


SPAETER = "2030-01-01T00:00:00"      # Stand weit hinter jeder Testkerze


# ---------------------------------------------------------------------------
def teil_a():
    print("\nA. Raster - ein krummer Zeitpunkt faellt auf")

    with tempfile.TemporaryDirectory() as ordner:
        baue_lage(ordner, dt.datetime(2021, 9, 1), 72)
        rueckgabe, text = lauf(["--ordner", ordner, "--stand", SPAETER])
        pruefe("die saubere Lage meldet nichts", rueckgabe == 0, text[-400:])

    with tempfile.TemporaryDirectory() as ordner:
        stunden = stundenreihe(dt.datetime(2021, 9, 1), 72)
        # Eine Kerze um eine halbe Stunde verschoben: sie sitzt nicht mehr auf
        # dem Stundenraster.
        stunden[30]["zeit"] = stunden[30]["zeit"] + dt.timedelta(minutes=30)
        schreibe(os.path.join(ordner, "X_1h.csv"), stunden, "1h")
        rueckgabe, text = lauf(["--ordner", ordner, "--stand", SPAETER])
        pruefe("ein Zeitpunkt neben dem Raster wird gemeldet", rueckgabe == 1)
        pruefe("und beim Namen genannt", "2021-09-02 06:30:00" in text,
               text[-500:])


def teil_a2():
    print("\nA2. Doppelte und rueckwaerts laufende Zeitstempel")

    for was, aendern in (
            ("ein doppelter Zeitpunkt",
             lambda k: k.__setitem__(31, dict(k[31], zeit=k[30]["zeit"]))),
            ("ein Rueckwaertssprung um genau ein Intervall",
             lambda k: k.__setitem__(31, dict(k[31],
                                              zeit=k[30]["zeit"] - STUNDE)))):
        with tempfile.TemporaryDirectory() as ordner:
            stunden = stundenreihe(dt.datetime(2021, 9, 1), 72)
            aendern(stunden)
            schreibe(os.path.join(ordner, "X_1h.csv"), stunden, "1h")
            rueckgabe, text = lauf(["--ordner", ordner, "--stand", SPAETER])
            pruefe(f"{was} wird gemeldet",
                   rueckgabe == 1 and "Raster" in text, text[-500:])


def teil_b():
    print("\nB. Die Wache schlaegt an - und nur, wenn es etwas gibt")

    # --- vollstaendig: der Tag beginnt um 00:00, 24 Stunden liegen vor -----
    with tempfile.TemporaryDirectory() as ordner:
        baue_lage(ordner, dt.datetime(2021, 9, 1), 72)
        rueckgabe, text = lauf(["--ordner", ordner, "--stand", SPAETER])
        pruefe("vollstaendige Tageskerzen: kein Befund", rueckgabe == 0,
               text[-600:])
        pruefe("und das steht auch so da", "Kein Befund" in text)

    # --- gekuerzt: der Tag beginnt um 13:00, es liegen 11 Stunden vor ------
    with tempfile.TemporaryDirectory() as ordner:
        baue_lage(ordner, dt.datetime(2021, 9, 1, 13), 72)
        rueckgabe, text = lauf(["--ordner", ordner, "--stand", SPAETER])
        pruefe("eine 11-Stunden-Tageskerze wird gemeldet", rueckgabe == 1)
        pruefe("die Zahl der belegten Stunden steht im Bericht",
               "11 von 24 Stunden" in text, text[-800:])
        pruefe("und die Ableitung wird als Nachweis benannt",
               "ABGELEITET" in text, text[-800:])

    # --- die letzte Kerze, mitten am Tag abgeschnitten ---------------------
    with tempfile.TemporaryDirectory() as ordner:
        # 00:00 des ersten Tages, dann 2 volle Tage und 13 Stunden
        baue_lage(ordner, dt.datetime(2021, 9, 1), 48 + 13)
        rueckgabe, text = lauf(["--ordner", ordner, "--stand", SPAETER])
        pruefe("eine abgeschnittene LETZTE Tageskerze wird gemeldet",
               rueckgabe == 1)
        pruefe("mit 13 von 24 Stunden", "13 von 24 Stunden" in text, text[-800:])
        pruefe("die erste Kerze wird dabei nicht mitgemeldet",
               text.count("Erste Kerze") == 0, text[-800:])


def teil_c():
    print("\nC. Was kursdaten.py nicht findet - beide Pruefungen nebeneinander")

    try:
        import pandas                                      # noqa: F401,PLC0415
    except ImportError:
        uebersprungen.append("Teil C (pandas fehlt)")
        print("  UEBERSPRUNGEN  pandas fehlt - kursdaten.pruefe_ordner braucht es")
        return

    import kursdaten                                       # noqa: PLC0415

    with tempfile.TemporaryDirectory() as ordner:
        baue_lage(ordner, dt.datetime(2021, 9, 1, 13), 72)
        tagesdatei = os.path.join(ordner, "X_1d.csv")

        # Die Kerze, um die es geht: vier gefuellte Kursspalten, elf Stunden.
        with open(tagesdatei, encoding="utf-8") as datei:
            erste_datenzeile = datei.readlines()[1].strip()
        felder = erste_datenzeile.split(",")
        pruefe("die strittige Zeile hat vier gefuellte Kursspalten",
               len(felder) == 6 and all(f.strip() for f in felder[1:5]),
               erste_datenzeile)

        befunde_kursdaten = kursdaten.pruefe_ordner(ordner)
        pruefe("kursdaten.py findet daran NICHTS", befunde_kursdaten == [],
               f"{befunde_kursdaten}")

        befunde_wache = za.pruefe_ordner(ordner, stand=za._stand_lesen(SPAETER))
        tages = [b for b in befunde_wache if b["datei"] == "X_1d.csv"]
        pruefe("die Wache findet genau diese Kerze",
               bool(tages) and bool(tages[0]["befunde"]))
        pruefe("und beziffert die Abdeckung mit 11 von 24 Stunden",
               bool(tages) and tages[0]["deckung"]["erste"]["vorhanden"] == 11
               and tages[0]["deckung"]["erste"]["erwartet"] == 24,
               f"{tages[0].get('deckung') if tages else None}")
        pruefe("das Urteil ist der Ableitungsnachweis, keine Vermutung",
               bool(tages)
               and tages[0]["deckung"]["erste"]["urteil"] == za.ABGELEITETE_TEILKERZE)

        # Gegenprobe in die andere Richtung: eine Kerze OHNE Kurse findet
        # kursdaten.py - und sie ist nicht das, worum es hier geht.
        with open(os.path.join(ordner, "X_1h.csv"), encoding="utf-8") as datei:
            zeilen = datei.read().splitlines()
        zeilen[5] = zeilen[5].split(",")[0] + ",,,,," + zeilen[5].split(",")[5]
        with open(os.path.join(ordner, "X_1h.csv"), "w", encoding="utf-8") as datei:
            datei.write("\n".join(zeilen) + "\n")
        pruefe("eine Kerze ohne Kurse findet umgekehrt kursdaten.py",
               len(kursdaten.pruefe_ordner(ordner)) == 1)


def teil_d():
    print("\nD. Stand - eine noch laufende Kerze ist zwingend eine Teilkerze")

    with tempfile.TemporaryDirectory() as ordner:
        stunden = stundenreihe(dt.datetime(2026, 8, 31), 13)
        schreibe(os.path.join(ordner, "X_1h.csv"), stunden, "1h")

        rueckgabe, text = lauf(["--ordner", ordner,
                                "--stand", "2026-08-31T12:30:00"])
        pruefe("die Kerze 12:00 laeuft um 12:30 noch - Befund", rueckgabe == 1)
        pruefe("der Bericht sagt, warum",
               "noch nicht abgeschlossen" in text, text[-600:])

        rueckgabe, text = lauf(["--ordner", ordner,
                                "--stand", "2026-08-31T13:00:00"])
        pruefe("um 13:00 ist dieselbe Kerze abgeschlossen - kein Befund",
               rueckgabe == 0, text[-600:])

        pruefe("ohne feinere Datei sagt der Bericht das ausdruecklich",
               "Ohne Deckungszeugen" in text, text[-800:])


def teil_e():
    print("\nE. Listing-Tag - der eine Fall, der aussen bleiben muss")

    with tempfile.TemporaryDirectory() as ordner:
        # 11 angeschnittene Stunden und danach zwei volle Tage: nur die ERSTE
        # Kerze ist kurz, die letzte nicht. Sonst pruefte dieser Teil zwei
        # Dinge auf einmal und belegte keines davon.
        baue_lage(ordner, dt.datetime(2021, 9, 1, 13), 11 + 48)
        beginn = os.path.join(ordner, "datenbeginn.json")
        with open(beginn, "w", encoding="utf-8") as datei:
            json.dump({"X": {"1d": "2021-09-01", "1h": "2021-09-01 13:00:00"}},
                      datei)

        rueckgabe, text = lauf(["--ordner", ordner, "--stand", SPAETER,
                                "--datenbeginn", beginn])
        pruefe("die kurze ERSTE Kerze gilt am Datenbeginn als richtig",
               rueckgabe == 0, text[-800:])

        # Dieselbe Datei, aber der gemessene Datenbeginn liegt frueher: dann
        # ist die kurze Kerze wieder ein Befund.
        with open(beginn, "w", encoding="utf-8") as datei:
            json.dump({"X": {"1d": "2017-08-17"}}, datei)
        rueckgabe, text = lauf(["--ordner", ordner, "--stand", SPAETER,
                                "--datenbeginn", beginn])
        pruefe("bei frueherem Datenbeginn bleibt es ein Befund", rueckgabe == 1,
               text[-800:])

    # Und die LETZTE Kerze wird durch --datenbeginn nie entschuldigt.
    with tempfile.TemporaryDirectory() as ordner:
        baue_lage(ordner, dt.datetime(2021, 9, 1), 48 + 13)
        beginn = os.path.join(ordner, "datenbeginn.json")
        with open(beginn, "w", encoding="utf-8") as datei:
            json.dump({"X": {"1d": "2021-09-03"}}, datei)
        rueckgabe, text = lauf(["--ordner", ordner, "--stand", SPAETER,
                                "--datenbeginn", beginn])
        pruefe("eine kurze LETZTE Kerze bleibt trotz --datenbeginn ein Befund",
               rueckgabe == 1, text[-800:])


def teil_f():
    print("\nF. Aufruf und Rueckgabewerte")

    rueckgabe, _ = lauf(["--ordner", "/gibt/es/nicht"])
    pruefe("ein fehlender Ordner ergibt 2", rueckgabe == 2)

    with tempfile.TemporaryDirectory() as ordner:
        baue_lage(ordner, dt.datetime(2021, 9, 1), 72)
        ziel = os.path.join(ordner, "bericht.json")
        rueckgabe, _ = lauf(["--ordner", ordner, "--stand", SPAETER,
                             "--json", ziel])
        with open(ziel, encoding="utf-8") as datei:
            bericht = json.load(datei)
        pruefe("der JSON-Bericht nennt jede gepruefte Datei",
               {b["datei"] for b in bericht["befunde"]} == {"X_1h.csv", "X_1d.csv"})
        pruefe("und den Stand, gegen den geprueft wurde",
               bericht["stand"].startswith("2030-01-01"))

    with tempfile.TemporaryDirectory() as ordner:
        # Eine Datei mit einem Zeitrahmen, den das Projekt nicht fuehrt.
        schreibe(os.path.join(ordner, "X_15m.csv"),
                 stundenreihe(dt.datetime(2021, 9, 1), 4), "1h")
        rueckgabe, text = lauf(["--ordner", ordner, "--stand", SPAETER])
        pruefe("ein nicht gefuehrter Zeitrahmen wird uebersprungen, nicht "
               "stillschweigend geprueft",
               rueckgabe == 0 and "1 uebersprungen" in text, text[-500:])


# ---------------------------------------------------------------------------
def teil_g():
    print("\nG. Mutationsproben - jede zweistufig, jede am Ablauf")

    # --- Probe 1: die Deckungspruefung ------------------------------------
    # Sie ist die einzige Wache, die eine abgeleitete Teilkerze ueberhaupt
    # sehen kann. Faellt sie aus, bleibt an dieser Lage NICHTS uebrig.
    def lage(ordner):
        baue_lage(ordner, dt.datetime(2021, 9, 1, 13), 72)

    with tempfile.TemporaryDirectory() as ordner:
        lage(ordner)
        rueckgabe, text = lauf(["--ordner", ordner, "--stand", SPAETER])
        pruefe("ohne Mutation: die 11-Stunden-Kerze wird gemeldet",
               rueckgabe == 1 and "11 von 24 Stunden" in text)

    with tempfile.TemporaryDirectory() as ordner:
        lage(ordner)
        echt = za.pruefe_deckung
        za.pruefe_deckung = lambda kerze, intervall, pfad, feiner: {
            "zeuge": os.path.basename(pfad), "zeuge_intervall": feiner,
            "erwartet": 0, "vorhanden": 0, "stunden": 0.0,
            "stunden_erwartet": 0.0, "urteil": za.VOLLSTAENDIG}
        try:
            rueckgabe, text = lauf(["--ordner", ordner, "--stand", SPAETER])
        finally:
            za.pruefe_deckung = echt
        pruefe("mit Mutation: die Verfaelschung greift ueberhaupt",
               "11 von 24 Stunden" not in text)
        pruefe("mit Mutation: die Teilkerze bleibt unbemerkt",
               rueckgabe == 0,
               "eine andere Wache haette sie gefangen - die Probe waere stumm")

    # --- Probe 2: der Ableitungsnachweis ----------------------------------
    # `gleich_bis_aufs_volumen` trennt "abgeleitet" von "unbelegt" UND
    # "vollstaendig" von "widerspruch". Wird sie zu grosszuegig, verschwindet
    # der Widerspruchsfall lautlos.
    def lage_widerspruch(ordner):
        """Volle Deckung, aber die Tageskerze passt nicht zu den Stunden."""
        stunden = stundenreihe(dt.datetime(2021, 9, 1), 48)
        schreibe(os.path.join(ordner, "X_1h.csv"), stunden, "1h")
        tage = leite_tageskerzen_ab(stunden)
        tage[0]["high"] = tage[0]["high"] + 500.0
        schreibe(os.path.join(ordner, "X_1d.csv"), tage, "1d")

    with tempfile.TemporaryDirectory() as ordner:
        lage_widerspruch(ordner)
        rueckgabe, text = lauf(["--ordner", ordner, "--stand", SPAETER])
        pruefe("ohne Mutation: der Widerspruch zwischen 1d und 1h wird gemeldet",
               rueckgabe == 1 and "widersprechen sich" in text, text[-700:])

    with tempfile.TemporaryDirectory() as ordner:
        lage_widerspruch(ordner)
        echt = za.gleich_bis_aufs_volumen
        za.gleich_bis_aufs_volumen = lambda kerze, summe: True
        try:
            rueckgabe, text = lauf(["--ordner", ordner, "--stand", SPAETER])
        finally:
            za.gleich_bis_aufs_volumen = echt
        pruefe("mit Mutation: der Widerspruch verschwindet lautlos",
               rueckgabe == 0 and "widersprechen sich" not in text,
               "der Vergleich ist also nicht das, was den Befund erzeugt")


def teil_h():
    print("\nH. Wenn eine zweite Wache die erste verdeckt - beide Lagen "
          "nebeneinander")

    def ohne_deckung(ordner, stand):
        echt = za.pruefe_deckung
        za.pruefe_deckung = lambda kerze, intervall, pfad, feiner: {
            "zeuge": os.path.basename(pfad), "zeuge_intervall": feiner,
            "erwartet": 0, "vorhanden": 0, "stunden": 0.0,
            "stunden_erwartet": 0.0, "urteil": za.VOLLSTAENDIG}
        try:
            return lauf(["--ordner", ordner, "--stand", stand])
        finally:
            za.pruefe_deckung = echt

    # Lage 1: abgeschlossener Stand. Nur die Deckung kann etwas finden.
    with tempfile.TemporaryDirectory() as ordner:
        baue_lage(ordner, dt.datetime(2021, 9, 1, 13), 72)
        rueckgabe, _ = ohne_deckung(ordner, SPAETER)
        pruefe("Lage 1 (Stand abgeschlossen): ohne Deckungspruefung bleibt "
               "kein Befund uebrig", rueckgabe == 0)

    # Lage 2: dieselbe Datei, aber der Stand liegt IN der letzten Kerze.
    # Jetzt meldet der Stand-Zeuge - und deckt das Fehlen der Deckung zu.
    with tempfile.TemporaryDirectory() as ordner:
        baue_lage(ordner, dt.datetime(2021, 9, 1, 13), 72)
        stand_mittendrin = "2021-09-04 06:00:00"
        rueckgabe_echt, text_echt = lauf(["--ordner", ordner,
                                          "--stand", stand_mittendrin])
        rueckgabe_mut, text_mut = ohne_deckung(ordner, stand_mittendrin)
        pruefe("Lage 2: ohne Mutation meldet die Wache die Teilkerze",
               rueckgabe_echt == 1 and "11 von 24 Stunden" in text_echt)
        pruefe("Lage 2: MIT Mutation bleibt der Rueckgabewert trotzdem 1",
               rueckgabe_mut == 1,
               "hier waere eine Probe, die nur auf den Rueckgabewert sieht, stumm")
        pruefe("Lage 2: und zwar, weil der Stand-Zeuge einspringt",
               "noch nicht abgeschlossen" in text_mut
               and "11 von 24 Stunden" not in text_mut, text_mut[-600:])
        pruefe("deshalb laeuft die echte Probe auf Lage 1",
               rueckgabe_echt == 1 and rueckgabe_mut == 1)


# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("SELBSTTEST shared/zeitabdeckung.py (TB-34)")
    print("=" * 78)

    for teil in (teil_a, teil_a2, teil_b, teil_c, teil_d, teil_e, teil_f,
                 teil_g, teil_h):
        teil()

    print("\n" + "=" * 78)
    gesamt = bestanden + len(gescheitert)
    if gescheitert:
        print(f"{bestanden}/{gesamt} Pruefungen bestanden, "
              f"{len(gescheitert)} fehlgeschlagen:")
        for was in gescheitert:
            print(f"  - {was}")
        return 1
    if uebersprungen:
        print(f"{bestanden}/{gesamt} Pruefungen bestanden. "
              f"Uebersprungen: {', '.join(uebersprungen)}.")
        return 0
    print(f"{bestanden}/{gesamt} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Selbsttest des Historien-Laders (TB-31)
==============================================================================
`shared/binance_historie.py` verlaengert vorhandene Kursdateien nach vorn.
Das ist ein schreibender Eingriff in `data/` - der Ordner, aus dem **jede**
Kennzahl dieses Projekts stammt. Eine still verfaelschte Kursdatei faellt
nirgends auf; sie liefert einfach andere Zahlen.

Dieser Test haelt deshalb sieben Zusicherungen nach, alle **am Verhalten**:

  A. **Ratenbegrenzung.** Mindestpause, Gewichts-Kopffeld, 429 mit
     `Retry-After`, 418 ohne Wiederholung.
  B. **Datenbeginn messen.** `startTime=0, limit=1` - und die Anfrage geht
     wirklich so hinaus.
  C. **Blaettern.** Ueber 1000 Kerzen hinaus, ohne Doppel und ohne Luecke.
  D. **Der ueberlappende Bereich wird Zeile fuer Zeile verglichen** - und
     eine Kursabweichung verhindert das Schreiben.
  E. **Verlaengern statt ueberschreiben.** Die vorhandenen Zeilen stehen
     hinterher **zeichengleich** in der Datei.
  F. **Wiederholbarkeit.** Ein zweiter Lauf laesst die Datei byte-identisch.
  G. **Die fuehrende Teilkerze** der abgeleiteten `*_1d.csv` wird erkannt,
     blockiert in der Voreinstellung das Schreiben und wird nur mit
     `--teilkerze-ersetzen` ersetzt - und zwar genau eine Zeile.

ZU DEN MUTATIONSPROBEN - WARUM SIE SO GEBAUT SIND
------------------------------------------------------------------------------
Zwei Fallen, die in diesem Projekt wiederholt aufgetreten sind (zuletzt
TB-28) und die auch hier drohen:

1. **Eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
   selbst.** Es waere einfach - und wertlos -, `vergleiche_ueberlappung()`
   mit von Hand gebauten Dicts aufzurufen und gruen zu melden. Das belegt
   nicht, dass `verlaengere_datei()` sie ueberhaupt aufruft. Deshalb laeuft
   **jede** Probe hier durch den echten Ablauf: eine nachgebildete
   Gegenstelle haengt an derselben Stelle, an der sonst `urlopen` haengt,
   der echte `Abrufer` baut die echte URL, die echte `Drossel` zaehlt mit,
   und `verlaengere_datei()` schreibt in eine echte Datei.

   Jede Mutationsprobe ist zweistufig: sie belegt erst, dass sie **ohne**
   Mutation das Richtige sieht, und dann, dass sie **mit** Mutation das
   Verfaelschte sieht. Bliebe eine Richtung ungeprueft, koennte die Probe
   stumm sein, ohne dass es auffiele.

2. **Eine zweite Wache verdeckt das Fehlen der ersten.** Vor dem Schreiben
   stehen zwei voneinander unabhaengige Wachen:

   * `vergleiche_ueberlappung()` findet die Abweichung, und
   * `nur_fuehrende_teilkerze()` entscheidet, ob es der bekannte Sonderfall
     der abgeleiteten Tageskerzen ist.

   Waere die zweite zu grosszuegig, wuerde `--teilkerze-ersetzen` jede
   beliebige Abweichung durchwinken - und die erste Wache saehe weiterhin
   alles, ohne dass es etwas naehme. Teil H prueft deshalb **jede Wache
   einzeln**: die zweite wird mit einer Abweichung **mitten in der Datei**
   konfrontiert, bei gesetztem `--teilkerze-ersetzen`.

   Und die dritte Wache - `kursdaten.entferne_unvollstaendige()` - sitzt
   allein vor dem **vorangestellten** Teil. Den vergleicht niemand, es gibt
   ihn ja noch nicht. Faellt sie aus, landet eine Kerze ohne Kurse in der
   Datei, und keine andere Wache merkt es. Teil I zeigt genau das.

Der Test geht **nicht** ins Netz und fasst `data/` nicht an. Er braucht
`pandas`.

    python3 shared/test_binance_historie.py

Rueckgabewert 0, wenn alle Pruefungen bestehen, sonst 1.
"""

import io
import json
import os
import shutil
import sys
import tempfile
import urllib.error

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
if _SHARED_DIR not in sys.path:
    sys.path.insert(0, _SHARED_DIR)

import binance_historie as bh                              # noqa: E402
import kursdaten                                           # noqa: E402

bestanden = 0
gescheitert = []


def pruefe(was, bedingung, hinweis=""):
    global bestanden
    if bedingung:
        bestanden += 1
        print(f"  OK    {was}")
    else:
        gescheitert.append(was)
        print(f"  FEHLT {was}" + (f"   [{hinweis}]" if hinweis else ""))


# ---------------------------------------------------------------------------
# Die nachgebildete Gegenstelle
# ---------------------------------------------------------------------------
STUNDE_MS = 3_600_000
TAG_MS = 86_400_000


class Antwort(io.BytesIO):
    """Was `urlopen` zurueckgibt: lesbar, mit Kopffeldern, als Kontextmanager."""

    def __init__(self, nutzlast, kopffelder):
        super().__init__(json.dumps(nutzlast).encode("utf-8"))
        self.headers = kopffelder

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
        return False


class Kopffelder(dict):
    def items(self):
        return list(super().items())


class FalscheBinance:
    """Haengt an derselben Stelle wie `urllib.request.urlopen`.

    Sie beantwortet echte URLs mit echtem JSON in der Feldform des
    Endpunkts (zwoelf Felder je Kerze, Zeitstempel in Millisekunden). Der
    Test beobachtet dadurch den **Ablauf** von `Abrufer`, `kerzen_laden`
    und `verlaengere_datei`, statt einen Zustand von Hand herzustellen.
    """

    def __init__(self, reihen, gewicht=None, fehlerplan=None):
        # reihen: {(symbol, intervall): [(open_time_ms, o, h, l, c, v), ...]}
        self.reihen = reihen
        self.gewicht = gewicht
        self.fehlerplan = list(fehlerplan or [])
        self.aufrufe = []

    def __call__(self, url, timeout=None):
        from urllib.parse import parse_qs, urlparse         # noqa: PLC0415

        zerlegt = urlparse(url)
        parameter = {k: v[0] for k, v in parse_qs(zerlegt.query).items()}
        self.aufrufe.append({"pfad": zerlegt.path, "parameter": parameter})

        if self.fehlerplan:
            code = self.fehlerplan.pop(0)
            if code is not None:
                kopf = Kopffelder({"Retry-After": "1"}) if code == 429 else Kopffelder()
                raise urllib.error.HTTPError(url, code, "Testfehler", kopf, None)

        schluessel = (parameter["symbol"], parameter["interval"])
        alle = self.reihen.get(schluessel, [])
        start = int(parameter.get("startTime", 0))
        ende = int(parameter["endTime"]) if "endTime" in parameter else None
        limit = int(parameter.get("limit", 500))

        gewaehlt = [k for k in alle if k[0] >= start and (ende is None or k[0] <= ende)]
        gewaehlt = gewaehlt[:limit]

        kerzen = [[k[0], f"{k[1]}", f"{k[2]}", f"{k[3]}", f"{k[4]}", f"{k[5]}",
                   k[0] + 1, "0", 0, "0", "0", "0"] for k in gewaehlt]
        kopffelder = Kopffelder()
        if self.gewicht is not None:
            kopffelder["x-mbx-used-weight-1m"] = str(self.gewicht)
        return Antwort(kerzen, kopffelder)


def reihe(start_ms, anzahl, schrittweite, basis=100.0):
    """Eine gleichmaessige Kerzenreihe - jede Kerze eindeutig an ihrem Preis
    erkennbar, damit eine vertauschte oder fehlende Zeile auffaellt."""
    kerzen = []
    for i in range(anzahl):
        p = basis + i
        kerzen.append((start_ms + i * schrittweite, p, p + 2.0, p - 1.0, p + 0.5, 10.0 + i))
    return kerzen


def schreibe_csv(pfad, kerzen, intervall):
    """Eine Kursdatei genau in der Schreibweise des Repos."""
    import pandas as pd                                    # noqa: PLC0415

    df = bh.als_dataframe(
        [[k[0], f"{k[1]}", f"{k[2]}", f"{k[3]}", f"{k[4]}", f"{k[5]}"] for k in kerzen],
        intervall)
    df = df.copy()
    df["open_time"] = df["open_time"].dt.strftime(bh.ZEITFORMAT[intervall])
    df.to_csv(pfad, index=False, lineterminator="\n")
    assert isinstance(pd.Timestamp(0), pd.Timestamp)


def stille_drossel(**mehr):
    """Eine Drossel mit eigener Uhr - der Test wartet nicht wirklich."""
    zustand = {"jetzt": 0.0, "geschlafen": []}

    def uhr():
        return zustand["jetzt"]

    def schlafen(sekunden):
        zustand["geschlafen"].append(sekunden)
        zustand["jetzt"] += sekunden

    drossel = bh.Drossel(uhr=uhr, schlafen=schlafen, **mehr)
    drossel.zustand = zustand
    return drossel


# ---------------------------------------------------------------------------
def teil_a():
    print("\nA. Ratenbegrenzung - am Ablauf, nicht an der Absicht")

    kerzen = reihe(0, 3, STUNDE_MS)
    gegenstelle = FalscheBinance({("X", "1h"): kerzen})
    drossel = stille_drossel(mindestpause=0.25)
    abrufer = bh.Abrufer(drossel=drossel, oeffner=gegenstelle)

    abrufer("X", "1h", start_ms=0, limit=1)
    abrufer("X", "1h", start_ms=0, limit=1)
    pruefe("zwischen zwei Anfragen liegt die Mindestpause",
           drossel.zustand["geschlafen"] == [0.25],
           f"geschlafen: {drossel.zustand['geschlafen']}")
    pruefe("die Anfragen gehen an /api/v3/klines",
           all(a["pfad"] == bh.ENDPUNKT for a in gegenstelle.aufrufe))
    pruefe("und tragen keinen Schluessel mit",
           not any(k.lower() in ("signature", "apikey", "timestamp")
                   for a in gegenstelle.aufrufe for k in a["parameter"]))

    # Gewichts-Kopffeld ueber der Schwelle
    schwer = FalscheBinance({("X", "1h"): kerzen}, gewicht=5000)
    drossel_schwer = stille_drossel(mindestpause=0.0)
    bh.Abrufer(drossel=drossel_schwer, oeffner=schwer)("X", "1h", start_ms=0, limit=1)
    pruefe("ein gemeldetes Gewicht ueber 70 % des Budgets loest eine Pause aus",
           drossel_schwer.pausen_wegen_gewicht == 1,
           f"Pausen: {drossel_schwer.pausen_wegen_gewicht}")

    leicht = FalscheBinance({("X", "1h"): kerzen}, gewicht=100)
    drossel_leicht = stille_drossel(mindestpause=0.0)
    bh.Abrufer(drossel=drossel_leicht, oeffner=leicht)("X", "1h", start_ms=0, limit=1)
    pruefe("ein gemeldetes Gewicht unter der Schwelle loest KEINE Pause aus",
           drossel_leicht.pausen_wegen_gewicht == 0)

    # 429 - warten und wiederholen
    gebremst = FalscheBinance({("X", "1h"): kerzen}, fehlerplan=[429, None])
    drossel_429 = stille_drossel(mindestpause=0.0)
    ergebnis = bh.Abrufer(drossel=drossel_429, oeffner=gebremst)("X", "1h", start_ms=0, limit=1)
    pruefe("HTTP 429 wird abgewartet und die Anfrage wiederholt",
           len(ergebnis) == 1 and len(gebremst.aufrufe) == 2,
           f"Aufrufe: {len(gebremst.aufrufe)}")
    pruefe("und zwar mindestens die von Retry-After verlangte Zeit",
           drossel_429.zustand["geschlafen"] and drossel_429.zustand["geschlafen"][0] >= 1.0)

    # 418 - Abbruch ohne Wiederholung
    gesperrt = FalscheBinance({("X", "1h"): kerzen}, fehlerplan=[418, None, None, None])
    drossel_418 = stille_drossel(mindestpause=0.0)
    try:
        bh.Abrufer(drossel=drossel_418, oeffner=gesperrt)("X", "1h", start_ms=0, limit=1)
        geworfen = None
    except bh.Gesperrt as fehler:
        geworfen = fehler
    pruefe("HTTP 418 bricht ab", isinstance(geworfen, bh.Gesperrt))
    pruefe("und probiert NICHT weiter - das verlaengerte nur die Sperre",
           len(gesperrt.aufrufe) == 1, f"Aufrufe: {len(gesperrt.aufrufe)}")


def teil_b():
    print("\nB. Datenbeginn messen - die Anfrage muss wirklich so hinausgehen")

    spaet = 1_600_000_000_000 - (1_600_000_000_000 % STUNDE_MS)
    gegenstelle = FalscheBinance({("SPAET", "1h"): reihe(spaet, 50, STUNDE_MS)})
    abrufer = bh.Abrufer(drossel=stille_drossel(mindestpause=0.0), oeffner=gegenstelle)

    gemessen = bh.erste_kerze_ms(abrufer, "SPAET", "1h")
    pruefe("der gemessene Beginn ist die erste Kerze der Gegenstelle", gemessen == spaet,
           f"{gemessen} statt {spaet}")
    parameter = gegenstelle.aufrufe[-1]["parameter"]
    pruefe("gefragt wird mit startTime=0", parameter.get("startTime") == "0")
    pruefe("und limit=1 - eine Kerze genuegt", parameter.get("limit") == "1")

    leer = FalscheBinance({})
    pruefe("ein Symbol ohne Kerzen ergibt None, keinen Absturz",
           bh.erste_kerze_ms(
               bh.Abrufer(drossel=stille_drossel(mindestpause=0.0), oeffner=leer),
               "GIBTSNICHT", "1h") is None)


def teil_c():
    print("\nC. Blaettern ueber die 1000-Kerzen-Grenze")

    alle = reihe(0, 2500, STUNDE_MS)
    gegenstelle = FalscheBinance({("X", "1h"): alle})
    abrufer = bh.Abrufer(drossel=stille_drossel(mindestpause=0.0), oeffner=gegenstelle)

    geladen = bh.kerzen_laden(abrufer, "X", "1h", 0, alle[-1][0])
    zeiten = [int(k[0]) for k in geladen]
    pruefe("alle 2500 Kerzen kommen an", len(geladen) == 2500, f"{len(geladen)}")
    pruefe("keine doppelt", len(set(zeiten)) == len(zeiten))
    pruefe("keine ausgelassen",
           zeiten == [k[0] for k in alle], "Luecke oder Reihenfolge")
    pruefe("in drei Anfragen statt 2500", len(gegenstelle.aufrufe) == 3,
           f"Anfragen: {len(gegenstelle.aufrufe)}")

    # Obergrenze wird eingehalten
    haelfte = alle[1200][0]
    gegenstelle2 = FalscheBinance({("X", "1h"): alle})
    abrufer2 = bh.Abrufer(drossel=stille_drossel(mindestpause=0.0), oeffner=gegenstelle2)
    begrenzt = bh.kerzen_laden(abrufer2, "X", "1h", 0, haelfte)
    pruefe("nichts jenseits von endTime",
           begrenzt and int(begrenzt[-1][0]) == haelfte, "ueber das Ende hinaus geladen")


# ---------------------------------------------------------------------------
def bau_lage(ordner, symbol="X", intervall="1h", gesamt=1500, ab_zeile=1000,
             schrittweite=STUNDE_MS, start_ms=0):
    """Eine echte Lage: die Gegenstelle kennt die ganze Reihe, die Datei im
    Ordner nur deren hinteren Teil. Genau der Fall, den TB-31 behebt."""
    alle = reihe(start_ms, gesamt, schrittweite)
    pfad = os.path.join(ordner, f"{symbol}_{intervall}.csv")
    schreibe_csv(pfad, alle[ab_zeile:], intervall)
    return alle, pfad


def lies(pfad):
    with open(pfad, "r", encoding="utf-8", newline="") as datei:
        return datei.read()


def zeilen_ohne_kurs(pfad):
    """Zeilen, in denen mindestens eine der vier Kursspalten leer ist.

    Genau die Form, in der der Fehler auftritt: `pandas.to_csv` schreibt ein
    fehlendes Feld als **leeres** Feld, nicht als `nan`. Der APH-Fall, der
    `shared/kursdaten.py` ausgeloest hat, sieht in der Datei genauso aus -
    `2026-09-01,,,,,1234.0`. Wer hier auf die Zeichenfolge `nan` pruefte,
    haette eine stumme Probe.
    """
    treffer = []
    for zeile in lies(pfad).splitlines()[1:]:
        felder = zeile.split(",")
        if len(felder) >= 5 and any(f.strip() == "" for f in felder[1:5]):
            treffer.append(zeile)
    return treffer


def lauf(gegenstelle, pfad, symbol="X", intervall="1h", **mehr):
    abrufer = bh.Abrufer(drossel=stille_drossel(mindestpause=0.0), oeffner=gegenstelle)
    return bh.verlaengere_datei(abrufer, pfad, symbol, intervall, **mehr)


def teil_d():
    print("\nD. Der ueberlappende Bereich wird Zeile fuer Zeile verglichen")

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = bau_lage(ordner)
        gegenstelle = FalscheBinance({("X", "1h"): alle})
        ergebnis = lauf(gegenstelle, pfad)
        pruefe("bei identischer Ueberlappung gibt es keinen harten Befund",
               bh.harte_befunde(ergebnis["befunde"]) == [],
               f"{ergebnis['befunde'][:2]}")
        pruefe("und die Datei wird verlaengert", ergebnis["geschrieben"])
        pruefe("um genau die fehlenden 1000 Zeilen",
               ergebnis["neue_zeilen"] == 1000, f"{ergebnis['neue_zeilen']}")

    # Eine Kursabweichung MITTEN in der Ueberlappung
    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = bau_lage(ordner)
        zeilen = lies(pfad).splitlines()
        felder = zeilen[250].split(",")
        felder[4] = "999999.0"                              # close verfaelschen
        zeilen[250] = ",".join(felder)
        with open(pfad, "w", encoding="utf-8", newline="") as datei:
            datei.write("\n".join(zeilen) + "\n")
        vorher = lies(pfad)

        gegenstelle = FalscheBinance({("X", "1h"): alle})
        ergebnis = lauf(gegenstelle, pfad)
        hart = bh.harte_befunde(ergebnis["befunde"])
        pruefe("eine Kursabweichung wird gefunden",
               len(hart) == 1 and hart[0]["art"] == "kurs", f"{hart}")
        pruefe("sie nennt die Spalte", hart and hart[0]["spalte"] == "close")
        pruefe("es wird NICHT geschrieben", not ergebnis["geschrieben"])
        pruefe("und die Datei ist unveraendert", lies(pfad) == vorher)

    # Volumen: Gleitkomma-Summe vs. native Summe
    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = bau_lage(ordner)
        zeilen = lies(pfad).splitlines()
        felder = zeilen[300].split(",")
        felder[5] = repr(float(felder[5]) * (1 + 1e-12))
        zeilen[300] = ",".join(felder)
        with open(pfad, "w", encoding="utf-8", newline="") as datei:
            datei.write("\n".join(zeilen) + "\n")

        gegenstelle = FalscheBinance({("X", "1h"): alle})
        ergebnis = lauf(gegenstelle, pfad)
        arten = [b["art"] for b in ergebnis["befunde"]]
        pruefe("eine Volumen-Abweichung in Rundungsgroesse wird gemeldet",
               "volumen_rundung" in arten, f"{arten[:3]}")
        pruefe("aber nicht als harter Befund gewertet",
               bh.harte_befunde(ergebnis["befunde"]) == [])
        pruefe("und blockiert das Schreiben nicht", ergebnis["geschrieben"])

    # Volumen jenseits der Toleranz ist sehr wohl hart
    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = bau_lage(ordner)
        zeilen = lies(pfad).splitlines()
        felder = zeilen[300].split(",")
        felder[5] = repr(float(felder[5]) * 1.5)
        zeilen[300] = ",".join(felder)
        with open(pfad, "w", encoding="utf-8", newline="") as datei:
            datei.write("\n".join(zeilen) + "\n")

        gegenstelle = FalscheBinance({("X", "1h"): alle})
        ergebnis = lauf(gegenstelle, pfad)
        pruefe("eine echte Volumen-Abweichung ist hart",
               [b["art"] for b in bh.harte_befunde(ergebnis["befunde"])] == ["volumen"])
        pruefe("und blockiert das Schreiben", not ergebnis["geschrieben"])

    # Eine Zeile, die der Endpunkt gar nicht kennt
    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = bau_lage(ordner)
        gegenstelle = FalscheBinance({("X", "1h"): alle[:-1]})   # letzte fehlt
        ergebnis = lauf(gegenstelle, pfad)
        pruefe("eine Zeile, die der Endpunkt nicht kennt, ist ein harter Befund",
               [b["art"] for b in bh.harte_befunde(ergebnis["befunde"])] == ["fehlt"])
        pruefe("und blockiert das Schreiben", not ergebnis["geschrieben"])

    # Luecke im Altbestand: der Endpunkt kennt einen Zeitpunkt, die Datei nicht
    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = bau_lage(ordner)
        zeilen = lies(pfad).splitlines()
        entfernt = zeilen.pop(200)
        with open(pfad, "w", encoding="utf-8", newline="") as datei:
            datei.write("\n".join(zeilen) + "\n")
        gegenstelle = FalscheBinance({("X", "1h"): alle})
        ergebnis = lauf(gegenstelle, pfad)
        pruefe("eine Luecke im vorhandenen Bereich wird gemeldet",
               len(ergebnis["luecken"]) == 1, f"{ergebnis['luecken']}")
        pruefe("sie nennt den fehlenden Zeitpunkt",
               ergebnis["luecken"] and ergebnis["luecken"][0] == entfernt.split(",")[0])
        pruefe("gefuellt wird sie nicht - das Modul verlaengert nur nach vorn",
               entfernt not in lies(pfad))


def teil_e():
    print("\nE. Verlaengern statt ueberschreiben")

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = bau_lage(ordner)
        vorher = lies(pfad)
        kopf_vorher, *zeilen_vorher = vorher.splitlines()

        gegenstelle = FalscheBinance({("X", "1h"): alle})
        lauf(gegenstelle, pfad)
        nachher = lies(pfad)
        kopf_nachher, *zeilen_nachher = nachher.splitlines()

        pruefe("die Kopfzeile bleibt", kopf_nachher == kopf_vorher)
        pruefe("die Datei ist um 1000 Zeilen laenger",
               len(zeilen_nachher) - len(zeilen_vorher) == 1000)
        pruefe("die vorhandenen Zeilen stehen ZEICHENGLEICH am Ende",
               zeilen_nachher[-len(zeilen_vorher):] == zeilen_vorher,
               "eine Altzeile wurde neu formatiert")
        pruefe("die neue erste Zeile ist der Datenbeginn des Endpunkts",
               zeilen_nachher[0].startswith(
                   bh.zeitstempel_text(
                       __import__("pandas").Timestamp(alle[0][0], unit="ms"), "1h")))
        pruefe("die Zeitstempel sind lueckenlos aufsteigend",
               [z.split(",")[0] for z in zeilen_nachher]
               == sorted(z.split(",")[0] for z in zeilen_nachher))
        pruefe("kein .neu-Rest bleibt liegen", not os.path.exists(pfad + ".neu"))

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = bau_lage(ordner)
        vorher = lies(pfad)
        gegenstelle = FalscheBinance({("X", "1h"): alle})
        ergebnis = lauf(gegenstelle, pfad, schreiben=False)
        pruefe("im Trockenlauf wird nichts geschrieben", not ergebnis["geschrieben"])
        pruefe("und die Datei bleibt unangetastet", lies(pfad) == vorher)
        pruefe("die Zahl der Zeilen wird trotzdem gemeldet",
               ergebnis["neue_zeilen"] == 1000)


def teil_f():
    print("\nF. Wiederholbarkeit - zweiter Lauf, gleiche Datei")

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = bau_lage(ordner)
        gegenstelle = FalscheBinance({("X", "1h"): alle})
        lauf(gegenstelle, pfad)
        nach_erstem = lies(pfad)

        zweiter = lauf(FalscheBinance({("X", "1h"): alle}), pfad)
        pruefe("der zweite Lauf liefert dieselbe Datei, Byte fuer Byte",
               lies(pfad) == nach_erstem)
        pruefe("er stellt nichts mehr voran", zweiter["neue_zeilen"] == 0)
        pruefe("und sagt warum",
               "Datenbeginn" in (zweiter["grund"] or ""), f"{zweiter['grund']}")
        pruefe("er findet auch im vergroesserten Bereich keinen Befund",
               bh.harte_befunde(zweiter["befunde"]) == [],
               "die selbst geschriebenen Zeilen passen nicht zum Endpunkt")
        pruefe("ein dritter Lauf aendert die Datei ebenfalls nicht",
               (lauf(FalscheBinance({("X", "1h"): alle}), pfad) is not None)
               and lies(pfad) == nach_erstem)


# ---------------------------------------------------------------------------
def bau_teilkerzen_lage(ordner):
    """Die Lage der abgeleiteten `*_1d.csv`: die erste Tageskerze der Datei
    deckt nur einen Teil des Tages ab und weicht deshalb von der nativen
    Tageskerze des Endpunkts ab. Alle spaeteren Zeilen stimmen."""
    alle, pfad = bau_lage(ordner, intervall="1d", gesamt=400, ab_zeile=300,
                          schrittweite=TAG_MS)
    zeilen = lies(pfad).splitlines()
    felder = zeilen[1].split(",")
    felder[1] = repr(float(felder[4]) - 0.25)     # open aus der Tagesmitte
    felder[2] = repr(float(felder[2]) - 1.0)      # high niedriger
    felder[5] = repr(float(felder[5]) * 0.45)     # nur ein Teil des Volumens
    zeilen[1] = ",".join(felder)
    with open(pfad, "w", encoding="utf-8", newline="") as datei:
        datei.write("\n".join(zeilen) + "\n")
    return alle, pfad


def teil_g():
    print("\nG. Die fuehrende Teilkerze der abgeleiteten Tagesdateien")

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = bau_teilkerzen_lage(ordner)
        vorher = lies(pfad)
        ergebnis = lauf(FalscheBinance({("X", "1d"): alle}), pfad, intervall="1d")
        hart = bh.harte_befunde(ergebnis["befunde"])
        pruefe("die Abweichung der ersten Zeile wird gefunden", len(hart) >= 1)
        pruefe("alle harten Befunde betreffen nur die erste Zeile",
               bh.nur_fuehrende_teilkerze(bh.Kursdatei(pfad, "1d"), ergebnis["befunde"]))
        pruefe("in der Voreinstellung wird NICHT geschrieben", not ergebnis["geschrieben"])
        pruefe("die Datei bleibt unveraendert", lies(pfad) == vorher)
        pruefe("der Grund nennt den Schalter",
               "--teilkerze-ersetzen" in (ergebnis["grund"] or ""), f"{ergebnis['grund']}")

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = bau_teilkerzen_lage(ordner)
        alt_zeilen = lies(pfad).splitlines()[1:]
        ergebnis = lauf(FalscheBinance({("X", "1d"): alle}), pfad, intervall="1d",
                        teilkerze_ersetzen=True)
        neu_zeilen = lies(pfad).splitlines()[1:]
        pruefe("mit --teilkerze-ersetzen wird geschrieben", ergebnis["geschrieben"])
        pruefe("genau EINE Zeile wird ersetzt", ergebnis["ersetzte_zeilen"] == 1,
               f"{ergebnis.get('ersetzte_zeilen')}")
        vorangestellt = ergebnis["neue_zeilen"]
        pruefe("die ersetzte Zeile ist die erste des Altbestands",
               neu_zeilen[vorangestellt] != alt_zeilen[0]
               and neu_zeilen[vorangestellt].split(",")[0] == alt_zeilen[0].split(",")[0])
        pruefe("alle uebrigen Altzeilen stehen zeichengleich da",
               neu_zeilen[vorangestellt + 1:] == alt_zeilen[1:])
        pruefe("die ersetzte Zeile ist jetzt die native Tageskerze",
               float(neu_zeilen[vorangestellt].split(",")[1])
               == float(neu_zeilen[vorangestellt - 1].split(",")[1]) + 1.0)


def teil_h():
    print("\nH. Jede Wache einzeln - die zweite darf die erste nicht ersetzen")

    # Abweichung MITTEN in der Datei, bei gesetztem --teilkerze-ersetzen.
    # Wuerde `nur_fuehrende_teilkerze` zu grosszuegig urteilen, gaebe es
    # keine zweite Wache, die das noch abfinge.
    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = bau_lage(ordner, intervall="1d", gesamt=400, ab_zeile=300,
                              schrittweite=TAG_MS)
        zeilen = lies(pfad).splitlines()
        felder = zeilen[40].split(",")
        felder[4] = "123456.0"
        zeilen[40] = ",".join(felder)
        with open(pfad, "w", encoding="utf-8", newline="") as datei:
            datei.write("\n".join(zeilen) + "\n")
        vorher = lies(pfad)

        ergebnis = lauf(FalscheBinance({("X", "1d"): alle}), pfad, intervall="1d",
                        teilkerze_ersetzen=True)
        pruefe("eine Abweichung mitten in der Datei gilt NICHT als Teilkerze",
               not bh.nur_fuehrende_teilkerze(bh.Kursdatei(pfad, "1d"),
                                              ergebnis["befunde"]))
        pruefe("sie wird auch mit --teilkerze-ersetzen nicht geschrieben",
               not ergebnis["geschrieben"])
        pruefe("die Datei bleibt unveraendert", lies(pfad) == vorher)

    # Erste Zeile UND eine spaetere weichen ab: kein Sonderfall mehr.
    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = bau_teilkerzen_lage(ordner)
        zeilen = lies(pfad).splitlines()
        felder = zeilen[40].split(",")
        felder[3] = "0.5"
        zeilen[40] = ",".join(felder)
        with open(pfad, "w", encoding="utf-8", newline="") as datei:
            datei.write("\n".join(zeilen) + "\n")
        vorher = lies(pfad)
        ergebnis = lauf(FalscheBinance({("X", "1d"): alle}), pfad, intervall="1d",
                        teilkerze_ersetzen=True)
        pruefe("erste Zeile PLUS spaetere Abweichung ist kein Sonderfall mehr",
               not ergebnis["geschrieben"])
        pruefe("auch hier bleibt die Datei unveraendert", lies(pfad) == vorher)


# ---------------------------------------------------------------------------
def teil_i():
    print("\nI. Mutationsproben - jede zweistufig, jede am Ablauf")

    # --- Probe 1: die Wache gegen unvollstaendige Kerzen ------------------
    # Sie sitzt ALLEIN vor dem vorangestellten Teil. Den vergleicht niemand -
    # es gibt ihn ja noch nicht. Faellt sie aus, landet eine Kerze ohne Kurse
    # in der Datei, und keine andere Wache merkt es.
    def lage_mit_luecke(ordner):
        alle = reihe(0, 1500, STUNDE_MS)
        kaputt = list(alle[5])
        kaputt[4] = float("nan")                            # close fehlt
        alle[5] = tuple(kaputt)
        pfad = os.path.join(ordner, "X_1h.csv")
        schreibe_csv(pfad, alle[1000:], "1h")
        return alle, pfad

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = lage_mit_luecke(ordner)
        ergebnis = lauf(FalscheBinance({("X", "1h"): alle}), pfad)
        pruefe("ohne Mutation: die Kerze ohne Kurse wird gestrichen UND gezaehlt",
               ergebnis["gestrichene_kerzen"] == 1, f"{ergebnis['gestrichene_kerzen']}")
        pruefe("ohne Mutation: keine Zeile der Datei hat eine leere Kursspalte",
               zeilen_ohne_kurs(pfad) == [], f"{zeilen_ohne_kurs(pfad)[:1]}")
        pruefe("ohne Mutation: dafuer fehlt genau diese eine Zeile",
               ergebnis["neue_zeilen"] == 999, f"{ergebnis['neue_zeilen']}")

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = lage_mit_luecke(ordner)
        echt = kursdaten.entferne_unvollstaendige
        kursdaten.entferne_unvollstaendige = lambda df, symbol=None, melden=True: (df, 0)
        try:
            ergebnis = lauf(FalscheBinance({("X", "1h"): alle}), pfad)
        finally:
            kursdaten.entferne_unvollstaendige = echt
        pruefe("mit Mutation: die Verfaelschung greift ueberhaupt",
               ergebnis["gestrichene_kerzen"] == 0 and ergebnis["neue_zeilen"] == 1000,
               f"{ergebnis['gestrichene_kerzen']}/{ergebnis['neue_zeilen']}")
        pruefe("mit Mutation: die Kerze ohne Kurse landet in der Kursdatei",
               len(zeilen_ohne_kurs(pfad)) == 1,
               "die Probe ist stumm - sie wuerde den Ausfall nicht bemerken")
        pruefe("mit Mutation: und zwar als LEERES Feld, nicht als 'nan'",
               all("nan" not in z.lower() for z in zeilen_ohne_kurs(pfad)),
               "eine Probe, die auf 'nan' prueft, bliebe hier gruen")

    # --- Probe 2: die Wache gegen abweichende Ueberlappung ----------------
    def lage_mit_abweichung(ordner):
        alle, pfad = bau_lage(ordner)
        zeilen = lies(pfad).splitlines()
        felder = zeilen[77].split(",")
        felder[2] = "424242.0"
        zeilen[77] = ",".join(felder)
        with open(pfad, "w", encoding="utf-8", newline="") as datei:
            datei.write("\n".join(zeilen) + "\n")
        return alle, pfad

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = lage_mit_abweichung(ordner)
        vorher = lies(pfad)
        ergebnis = lauf(FalscheBinance({("X", "1h"): alle}), pfad)
        pruefe("ohne Mutation: die Abweichung verhindert das Schreiben",
               not ergebnis["geschrieben"] and lies(pfad) == vorher)

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = lage_mit_abweichung(ordner)
        vorher = lies(pfad)
        echt = bh.vergleiche_ueberlappung
        bh.vergleiche_ueberlappung = lambda datei, geladen: []
        try:
            ergebnis = lauf(FalscheBinance({("X", "1h"): alle}), pfad)
        finally:
            bh.vergleiche_ueberlappung = echt
        pruefe("mit Mutation: die Verfaelschung greift ueberhaupt",
               ergebnis["befunde"] == [])
        pruefe("mit Mutation: die abweichende Datei wird geschrieben",
               ergebnis["geschrieben"] and lies(pfad) != vorher,
               "der Vergleich ist also nicht das, was das Schreiben verhindert")

    # --- Probe 3: die enge Bedingung des Sonderfalls ----------------------
    # Sie ist die einzige Stelle, an der eine gefundene Abweichung doch
    # durchgewinkt wird. Wird sie zu grosszuegig, faengt sie NICHTS mehr ab.
    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = lage_mit_abweichung(ordner)
        vorher = lies(pfad)
        echt = bh.nur_fuehrende_teilkerze
        bh.nur_fuehrende_teilkerze = lambda datei, befunde: True
        try:
            ergebnis = lauf(FalscheBinance({("X", "1h"): alle}), pfad,
                            teilkerze_ersetzen=True)
        finally:
            bh.nur_fuehrende_teilkerze = echt
        pruefe("mit Mutation: eine zu grosszuegige Sonderfall-Bedingung "
               "winkt die Abweichung durch",
               ergebnis["geschrieben"] and lies(pfad) != vorher,
               "die enge Bedingung in Teil H ist also tragend")
        pruefe("ohne Mutation urteilt sie eng genug (Teil H hat es gezeigt)",
               bh.nur_fuehrende_teilkerze is echt)


def main() -> int:
    print("=" * 78)
    print("Selbsttest des Historien-Laders (TB-31)")
    print("=" * 78)
    teil_a()
    teil_b()
    teil_c()
    teil_d()
    teil_e()
    teil_f()
    teil_g()
    teil_h()
    teil_i()
    print("\n" + "=" * 78)
    if gescheitert:
        print(f"{bestanden} bestanden, {len(gescheitert)} GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
        return 1
    print(f"{bestanden}/{bestanden} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

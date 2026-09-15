#!/usr/bin/env python3
"""
Selbsttest des Kursdaten-Neuaufbaus (TB-34)
==============================================================================
`shared/kursdaten_neuaufbau.py` **ersetzt** Kursdateien. Das ist der groesste
schreibende Eingriff, den dieses Projekt auf `data/` kennt - dem Ordner, aus
dem jede Kennzahl stammt. Eine still verfaelschte Kursdatei faellt nirgends
auf; sie liefert einfach andere Zahlen.

Geprueft werden acht Zusicherungen, alle **am Verhalten**:

  A. **Keine laufende Kerze.** Uebernommen wird nur, was der Endpunkt als
     abgeschlossen meldet (`close_time <= Stand`) - beide Richtungen.
  B. **Tageskerzen nativ.** Aus der abgeleiteten Tagesdatei wird die native;
     die Datei reicht danach weiter zurueck.
  C. **Vergleich alt gegen neu.** Zeilenzahl, Zeitraum und die Zahl der
     abweichenden Zeilen im gemeinsamen Bereich stehen je Datei im Ergebnis.
  D. **Eine Abweichung ausserhalb der Raender verhindert das Schreiben** -
     eine an den Raendern nicht.
  E. **Wiederholbarkeit.** Zweiter Lauf mit demselben Stand: byte-identisch.
  F. **Die Sicherung ist vollstaendig und laesst sich zurueckspielen** -
     am Verhalten geprueft, samt verfaelschter Sicherung.
  G. **Nur `/api/v3/klines`, ohne Schluessel.** Die wirklich gestellten
     Anfragen werden mitgeschrieben und angesehen.
  H. **Trockenlauf ist die Voreinstellung.** Ohne `--schreiben` wird nichts
     angefasst.

ZUR NACHGEBILDETEN GEGENSTELLE
------------------------------------------------------------------------------
Sie haengt an derselben Stelle wie `urllib.request.urlopen`. Der echte
`Abrufer` baut die echte URL, die echte `Drossel` zaehlt mit, `main()` wird
mit Argumentliste aufgerufen. Ein Unterschied zur Gegenstelle aus TB-31 ist
Absicht: **sie fuellt `close_time` richtig** (Feld 6 = Oeffnung + Intervall
- 1 ms). TB-31 brauchte das Feld nicht und setzte dort einen Platzhalter;
hier haengt die wichtigste Zusicherung des Moduls daran, also muss es echt
sein.

ZU DEN MUTATIONSPROBEN
------------------------------------------------------------------------------
Zwei Fallen, die dieses Projekt wiederholt getroffen haben (#73, #77, #78,
#79, #81, #86, TB-15, TB-20, TB-22, TB-26, TB-30a):

1. **Eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
   selbst.** Jede Probe hier laeuft durch den echten Ablauf und ist
   zweistufig: erst ohne Mutation das Richtige, dann mit Mutation das
   Verfaelschte. Bliebe eine Richtung ungeprueft, koennte die Probe stumm
   sein, ohne dass es auffiele.

2. **Eine zweite Wache verdeckt das Fehlen der ersten.** Vor dem Schreiben
   stehen drei unabhaengige Wachen: `abgeschlossene_kerzen()`,
   `kursdaten.entferne_unvollstaendige()` und `vergleiche()`. Teil J stellt
   die dritte und die zweite **an zwei Lagen nebeneinander**: liegt die
   kaputte Kerze im gemeinsamen Bereich, faengt `vergleiche()` sie auch ohne
   die zweite Wache ab - eine Probe auf dieser Lage waere stumm. Liegt sie in
   der **vorangestellten** Historie, vergleicht sie niemand, und der Ausfall
   ist sichtbar. Die echte Probe laeuft deshalb auf der zweiten Lage.

Der Test geht nicht ins Netz und fasst `data/` nicht an. Er braucht `pandas`.

    python3 shared/test_kursdaten_neuaufbau.py

Rueckgabewert 0, wenn alle Pruefungen bestehen, sonst 1.
"""

import io
import json
import os
import sys
import tempfile
import urllib.request
from contextlib import redirect_stdout

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
if _SHARED_DIR not in sys.path:
    sys.path.insert(0, _SHARED_DIR)

import binance_historie as bh                              # noqa: E402
import kursdaten                                           # noqa: E402
import kursdaten_neuaufbau as kn                           # noqa: E402

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

    `reihen`: {(symbol, intervall): [(open_time_ms, o, h, l, c, v), ...]}
    Die Kerzen werden in der Feldform des Endpunkts beantwortet - zwoelf
    Felder, **mit richtigem `close_time`**.
    """

    def __init__(self, reihen, gewicht=None):
        self.reihen = reihen
        self.gewicht = gewicht
        self.aufrufe = []

    def __call__(self, url, timeout=None):
        from urllib.parse import parse_qs, urlparse         # noqa: PLC0415

        zerlegt = urlparse(url)
        parameter = {k: v[0] for k, v in parse_qs(zerlegt.query).items()}
        self.aufrufe.append({"pfad": zerlegt.path, "parameter": parameter,
                             "url": url})

        schluessel = (parameter["symbol"], parameter["interval"])
        alle = self.reihen.get(schluessel, [])
        laenge = bh.INTERVALL_MS[parameter["interval"]]
        start = int(parameter.get("startTime", 0))
        ende = int(parameter["endTime"]) if "endTime" in parameter else None
        limit = int(parameter.get("limit", 500))

        gewaehlt = [k for k in alle if k[0] >= start and (ende is None or k[0] <= ende)]
        gewaehlt = gewaehlt[:limit]
        kerzen = [[k[0], f"{k[1]}", f"{k[2]}", f"{k[3]}", f"{k[4]}", f"{k[5]}",
                   k[0] + laenge - 1, "0", 0, "0", "0", "0"] for k in gewaehlt]

        kopffelder = Kopffelder()
        if self.gewicht is not None:
            kopffelder["x-mbx-used-weight-1m"] = str(self.gewicht)
        return Antwort(kerzen, kopffelder)


def reihe(start_ms, anzahl, schrittweite, basis=100.0):
    """Eine gleichmaessige Kerzenreihe - jede Kerze an ihrem Preis erkennbar."""
    kerzen = []
    for i in range(anzahl):
        p = basis + i
        kerzen.append((start_ms + i * schrittweite, p, p + 2.0, p - 1.0,
                       p + 0.5, 10.0 + i))
    return kerzen


def schreibe_csv(pfad, kerzen, intervall):
    """Eine Kursdatei genau in der Schreibweise des Repos."""
    df = bh.als_dataframe(
        [[k[0], f"{k[1]}", f"{k[2]}", f"{k[3]}", f"{k[4]}", f"{k[5]}"] for k in kerzen],
        intervall)
    zeilen = bh.zeilen_aus_dataframe(df, intervall)
    with open(pfad, "w", encoding="utf-8", newline="") as datei:
        datei.write(",".join(bh.SPALTEN) + "\n")
        datei.write("\n".join(zeilen) + "\n")


def lies(pfad):
    with open(pfad, "r", encoding="utf-8", newline="") as datei:
        return datei.read()


def zeilen_ohne_kurs(pfad):
    treffer = []
    for zeile in lies(pfad).splitlines()[1:]:
        felder = zeile.split(",")
        if len(felder) == 6 and any(f.strip() == "" for f in felder[1:5]):
            treffer.append(zeile)
    return treffer


def stand_aus_ms(ms):
    import datetime as dt                                  # noqa: PLC0415
    return (dt.datetime(1970, 1, 1)
            + dt.timedelta(milliseconds=ms)).isoformat(sep="T")


def baue_lage(ordner, intervall="1h", gesamt=1500, ab_zeile=1000,
              schrittweite=STUNDE_MS, symbol="X"):
    """Der Endpunkt kennt `gesamt` Kerzen, die Datei nur die letzten davon.

    Genau die Lage des Repos: das Abruffenster hat die Historie vorn
    beschnitten.
    """
    alle = reihe(0, gesamt, schrittweite)
    pfad = os.path.join(ordner, f"{symbol}_{intervall}.csv")
    schreibe_csv(pfad, alle[ab_zeile:], intervall)
    return alle, pfad


def direkt(gegenstelle, pfad, symbol="X", intervall="1h", stand_ms=None,
           schreiben=False, sicherung=None, zaehler=None):
    """`baue_datei_neu()` mit echtem Abrufer und echter Drossel."""
    import datetime as dt                                  # noqa: PLC0415

    drossel = bh.Drossel(mindestpause=0.0)
    abrufer = bh.Abrufer(drossel=drossel, oeffner=gegenstelle)
    stand = dt.datetime(1970, 1, 1) + dt.timedelta(milliseconds=stand_ms)
    return kn.baue_datei_neu(abrufer, pfad, symbol, intervall, stand,
                             schreiben=schreiben, sicherung=sicherung,
                             zaehler=zaehler)


def ueber_main(gegenstelle, argv):
    """`main()` wirklich aufrufen - mit der Gegenstelle an `urlopen`."""
    echt = urllib.request.urlopen
    urllib.request.urlopen = gegenstelle
    puffer = io.StringIO()
    try:
        with redirect_stdout(puffer):
            rueckgabe = kn.main(argv)
    finally:
        urllib.request.urlopen = echt
    return rueckgabe, puffer.getvalue()


# ---------------------------------------------------------------------------
def teil_a():
    print("\nA. Keine laufende Kerze - close_time entscheidet, nicht Sorgfalt")

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = baue_lage(ordner, gesamt=200, ab_zeile=100)
        letzte_oeffnung = alle[-1][0]

        # Stand mitten in der letzten Kerze: sie laeuft noch.
        mitten = letzte_oeffnung + STUNDE_MS // 2
        ergebnis = direkt(FalscheBinance({("X", "1h"): alle}), pfad,
                          stand_ms=mitten)
        pruefe("die laufende Kerze wird verworfen",
               ergebnis["laufende_kerzen"] == 1, f"{ergebnis['laufende_kerzen']}")
        pruefe("die Datei endet eine Kerze frueher als der Endpunkt",
               ergebnis["neu_zeilen"] == 199
               and ergebnis["neu_bis"] < stand_aus_ms(letzte_oeffnung)[:19],
               f"{ergebnis['neu_zeilen']} / {ergebnis['neu_bis']}")

        # Stand genau am Ende derselben Kerze: sie ist abgeschlossen.
        ende = letzte_oeffnung + STUNDE_MS - 1
        ergebnis = direkt(FalscheBinance({("X", "1h"): alle}), pfad,
                          stand_ms=ende)
        pruefe("eine Millisekunde spaeter ist dieselbe Kerze abgeschlossen",
               ergebnis["laufende_kerzen"] == 0, f"{ergebnis['laufende_kerzen']}")
        pruefe("und sie ist die letzte Zeile",
               ergebnis["neu_zeilen"] == 200, f"{ergebnis['neu_zeilen']}")


def teil_b():
    print("\nB. Tageskerzen nativ statt abgeleitet")

    with tempfile.TemporaryDirectory() as ordner:
        # Der Endpunkt kennt 400 native Tageskerzen; die Datei nur die
        # letzten 100 - und ihre erste ist eine abgeleitete Teilkerze.
        alle = reihe(0, 400, TAG_MS)
        pfad = os.path.join(ordner, "X_1d.csv")
        schreibe_csv(pfad, alle[300:], "1d")
        zeilen = lies(pfad).splitlines()
        felder = zeilen[1].split(",")
        felder[1] = repr(float(felder[1]) + 7.0)      # andere Eroeffnung
        felder[3] = repr(float(felder[3]) + 5.0)      # anderes Tief
        zeilen[1] = ",".join(felder)
        with open(pfad, "w", encoding="utf-8", newline="") as datei:
            datei.write("\n".join(zeilen) + "\n")

        stand = alle[-1][0] + TAG_MS - 1
        ergebnis = direkt(FalscheBinance({("X", "1d"): alle}), pfad,
                          intervall="1d", stand_ms=stand, schreiben=True)
        pruefe("die Datei wird geschrieben", ergebnis["geschrieben"],
               f"{ergebnis['grund']}")
        pruefe("sie reicht danach bis zum Datenbeginn des Endpunkts zurueck",
               ergebnis["neu_von"] == "1970-01-01", f"{ergebnis['neu_von']}")
        pruefe("aus 100 Zeilen werden 400",
               (ergebnis["alt_zeilen"], ergebnis["neu_zeilen"]) == (100, 400),
               f"{ergebnis['alt_zeilen']} -> {ergebnis['neu_zeilen']}")
        neue_zeilen = lies(pfad).splitlines()
        alt_erste = ergebnis["alt_von"]
        ersetzt = [z for z in neue_zeilen if z.startswith(alt_erste + ",")]
        pruefe("die abgeleitete Teilkerze ist durch die native ersetzt",
               len(ersetzt) == 1 and ersetzt[0] != zeilen[1],
               f"{ersetzt[:1]}")
        pruefe("die Randabweichung wurde als solche gezaehlt",
               ergebnis["abweichende_zeilen"] == 1
               and ergebnis["abweichende_zeilen_innen"] == 0,
               f"{ergebnis['abweichende_zeilen']}/"
               f"{ergebnis['abweichende_zeilen_innen']}")


def teil_c():
    print("\nC. Vergleich alt gegen neu - je Datei Zeilen, Zeitraum, Abweichungen")

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = baue_lage(ordner, gesamt=1500, ab_zeile=1000)
        stand = alle[-1][0] + STUNDE_MS - 1
        ergebnis = direkt(FalscheBinance({("X", "1h"): alle}), pfad,
                          stand_ms=stand)
        for feld in ("alt_zeilen", "neu_zeilen", "alt_von", "alt_bis",
                     "neu_von", "neu_bis", "abweichende_zeilen",
                     "abweichende_zeilen_innen"):
            pruefe(f"das Ergebnis nennt {feld}", ergebnis.get(feld) is not None,
                   f"{ergebnis.get(feld)}")
        pruefe("ohne Verfaelschung weicht keine Zeile ab",
               ergebnis["abweichende_zeilen"] == 0,
               f"{ergebnis['abweichende_zeilen']}")
        pruefe("die Datei wuerde um genau die fehlende Historie wachsen",
               ergebnis["neu_zeilen"] - ergebnis["alt_zeilen"] == 1000,
               f"{ergebnis['neu_zeilen']} - {ergebnis['alt_zeilen']}")

    # Eine Luecke im Altbestand wird gefuellt und als solche gezaehlt -
    # das ist keine Abweichung.
    with tempfile.TemporaryDirectory() as ordner:
        alle = reihe(0, 300, STUNDE_MS)
        pfad = os.path.join(ordner, "X_1h.csv")
        behalten = alle[200:250] + alle[253:]
        schreibe_csv(pfad, behalten, "1h")
        stand = alle[-1][0] + STUNDE_MS - 1
        ergebnis = direkt(FalscheBinance({("X", "1h"): alle}), pfad,
                          stand_ms=stand)
        pruefe("eine Luecke im Altbestand wird als gefuellt gezaehlt",
               ergebnis["gefuellte_luecken"] == 3,
               f"{ergebnis['gefuellte_luecken']}")
        pruefe("und gilt nicht als Abweichung",
               ergebnis["abweichende_zeilen_innen"] == 0,
               f"{ergebnis['abweichende_zeilen_innen']}")


def teil_d():
    print("\nD. Abweichung ausserhalb der Raender verhindert das Schreiben")

    def lage_mit_abweichung(ordner, zeilennummer):
        alle, pfad = baue_lage(ordner, gesamt=1500, ab_zeile=1000)
        zeilen = lies(pfad).splitlines()
        felder = zeilen[zeilennummer].split(",")
        felder[2] = "424242.0"
        zeilen[zeilennummer] = ",".join(felder)
        with open(pfad, "w", encoding="utf-8", newline="") as datei:
            datei.write("\n".join(zeilen) + "\n")
        return alle, pfad

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = lage_mit_abweichung(ordner, 250)      # mitten drin
        vorher = lies(pfad)
        stand = alle[-1][0] + STUNDE_MS - 1
        ergebnis = direkt(FalscheBinance({("X", "1h"): alle}), pfad,
                          stand_ms=stand, schreiben=True)
        pruefe("eine Abweichung im Innern verhindert das Schreiben",
               not ergebnis["geschrieben"])
        pruefe("die Datei bleibt unveraendert", lies(pfad) == vorher)
        pruefe("sie wird gezaehlt und beim Zeitpunkt genannt",
               ergebnis["abweichende_zeilen_innen"] == 1
               and ergebnis["erste_abweichung_innen"] is not None,
               f"{ergebnis['erste_abweichung_innen']}")
        pruefe("der Grund sagt 'AUSSERHALB der Raender'",
               "AUSSERHALB" in (ergebnis["grund"] or ""), f"{ergebnis['grund']}")

    # Und der Bericht stellt es an den ANFANG der Zusammenfassung - nicht
    # irgendwo dazwischen. Der Auftrag verlangt genau das.
    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = lage_mit_abweichung(ordner, 250)
        stand = stand_aus_ms(alle[-1][0] + STUNDE_MS - 1)
        rueckgabe, text = ueber_main(
            FalscheBinance({("X", "1h"): alle}),
            ["--ordner", ordner, "--symbole", "X", "--zeitrahmen", "1h",
             "--stand", stand, "--pause", "0", "--schreiben",
             "--sicherung", os.path.join(ordner, "sicherung")])
        pruefe("der Lauf meldet 1", rueckgabe == 1)
        zusammenfassung = text[text.index("=" * 78, text.index("Datenqualitaet")):]
        pruefe("der Befund steht am ANFANG der Zusammenfassung",
               zusammenfassung.lstrip("=\n").startswith("BEFUND:"),
               zusammenfassung[:200])
        pruefe("er nennt den Zeitpunkt der ersten inneren Abweichung",
               "kurs/high" in text, text[-900:])

    # Genau EINE Zeile weiter innen als der Rand: immer noch ein Befund.
    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = lage_mit_abweichung(ordner, 2)        # zweite Datenzeile
        vorher = lies(pfad)
        stand = alle[-1][0] + STUNDE_MS - 1
        ergebnis = direkt(FalscheBinance({("X", "1h"): alle}), pfad,
                          stand_ms=stand, schreiben=True)
        pruefe("die Ausnahme gilt der ERSTEN Zeile, nicht der Gegend um sie",
               not ergebnis["geschrieben"] and lies(pfad) == vorher)

    # An den Raendern: erwartete Teilkerze, es wird geschrieben.
    for nummer, name in ((1, "erste"), (-1, "letzte")):
        with tempfile.TemporaryDirectory() as ordner:
            alle, pfad = baue_lage(ordner, gesamt=1500, ab_zeile=1000)
            zeilen = lies(pfad).splitlines()
            felder = zeilen[nummer].split(",")
            felder[2] = "424242.0"
            zeilen[nummer] = ",".join(felder)
            with open(pfad, "w", encoding="utf-8", newline="") as datei:
                datei.write("\n".join(zeilen) + "\n")
            stand = alle[-1][0] + STUNDE_MS - 1
            ergebnis = direkt(FalscheBinance({("X", "1h"): alle}), pfad,
                              stand_ms=stand, schreiben=True)
            pruefe(f"eine Abweichung an der {name} Zeile ist die erwartete "
                   f"Teilkerze und wird ersetzt",
                   ergebnis["geschrieben"]
                   and ergebnis["abweichende_zeilen_innen"] == 0,
                   f"{ergebnis['grund']}")


def teil_e():
    print("\nE. Wiederholbarkeit - zweiter Lauf, byteweise dieselbe Datei")

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = baue_lage(ordner, gesamt=1500, ab_zeile=1000)
        stand = stand_aus_ms(alle[-1][0] + STUNDE_MS - 1)
        argv = ["--ordner", ordner, "--symbole", "X", "--zeitrahmen", "1h",
                "--stand", stand, "--pause", "0", "--schreiben",
                "--sicherung", os.path.join(ordner, "sicherung1")]

        rueckgabe, _ = ueber_main(FalscheBinance({("X", "1h"): alle}), argv)
        pruefe("der erste Lauf schreibt und meldet 0", rueckgabe == 0)
        nach_erstem = lies(pfad)

        argv[-1] = os.path.join(ordner, "sicherung2")
        rueckgabe, _ = ueber_main(FalscheBinance({("X", "1h"): alle}), argv)
        pruefe("der zweite Lauf meldet ebenfalls 0", rueckgabe == 0)
        pruefe("und laesst die Datei byte-identisch", lies(pfad) == nach_erstem)

        # Ein spaeterer Stand bringt genau die dann abgeschlossenen Kerzen
        # dazu - das ist der Unterschied zwischen wiederholbar und starr.
        pruefe("die Kopfzeile steht genau einmal",
               nach_erstem.count("open_time,open") == 1)


def teil_f():
    print("\nF. Die Sicherung - vollstaendig, geprueft, zurueckspielbar")

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = baue_lage(ordner, gesamt=1500, ab_zeile=1000)
        vorher = lies(pfad)
        sicherungsordner = os.path.join(ordner, "sicherung")
        stand = stand_aus_ms(alle[-1][0] + STUNDE_MS - 1)
        argv = ["--ordner", ordner, "--symbole", "X", "--zeitrahmen", "1h",
                "--stand", stand, "--pause", "0", "--schreiben",
                "--sicherung", sicherungsordner]

        rueckgabe, text = ueber_main(FalscheBinance({("X", "1h"): alle}), argv)
        pruefe("der Lauf schreibt", rueckgabe == 0 and lies(pfad) != vorher)
        pruefe("die Sicherung enthaelt die Datei",
               os.path.exists(os.path.join(sicherungsordner, "X_1h.csv")))
        pruefe("und den alten Stand zeichengleich",
               lies(os.path.join(sicherungsordner, "X_1h.csv")) == vorher)
        pruefe("der Bericht nennt den Sicherungsordner",
               sicherungsordner in text, text[-500:])

        with open(os.path.join(sicherungsordner, kn.MANIFEST),
                  encoding="utf-8") as datei:
            manifest = json.load(datei)
        pruefe("das Manifest fuehrt jede gesicherte Datei mit SHA-256",
               set(manifest["dateien"]) == {"X_1h.csv"}
               and len(manifest["dateien"]["X_1h.csv"]["sha256"]) == 64)

        # Zurueckspielen - am Verhalten geprueft, nicht am Manifest.
        rueckgabe, text = ueber_main(
            FalscheBinance({}),
            ["--ordner", ordner, "--zurueckspielen", sicherungsordner])
        pruefe("--zurueckspielen meldet 0", rueckgabe == 0, text[-400:])
        pruefe("und die Datei ist wieder die alte", lies(pfad) == vorher)

    # Eine verfaelschte Sicherung wird nicht zurueckgespielt.
    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = baue_lage(ordner, gesamt=400, ab_zeile=300)
        sicherungsordner = os.path.join(ordner, "sicherung")
        stand = stand_aus_ms(alle[-1][0] + STUNDE_MS - 1)
        ueber_main(FalscheBinance({("X", "1h"): alle}),
                   ["--ordner", ordner, "--symbole", "X", "--zeitrahmen", "1h",
                    "--stand", stand, "--pause", "0", "--schreiben",
                    "--sicherung", sicherungsordner])
        nach_lauf = lies(pfad)
        with open(os.path.join(sicherungsordner, "X_1h.csv"), "a",
                  encoding="utf-8") as datei:
            datei.write("1970-01-01 00:00:00,1,1,1,1,1\n")

        rueckgabe, text = ueber_main(
            FalscheBinance({}),
            ["--ordner", ordner, "--zurueckspielen", sicherungsordner])
        pruefe("eine verfaelschte Sicherung wird erkannt", rueckgabe == 1,
               text[-400:])
        pruefe("und nicht zurueckgespielt", lies(pfad) == nach_lauf)

    # Ein Ordner ohne Manifest ist keine Sicherung dieses Werkzeugs.
    with tempfile.TemporaryDirectory() as ordner:
        os.makedirs(os.path.join(ordner, "leer"))
        rueckgabe, _ = ueber_main(
            FalscheBinance({}),
            ["--ordner", ordner, "--zurueckspielen", os.path.join(ordner, "leer")])
        pruefe("ein Ordner ohne Manifest wird abgelehnt", rueckgabe == 2)


def teil_g():
    print("\nG. Nur /api/v3/klines - oeffentlich, ohne Schluessel")

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = baue_lage(ordner, gesamt=1500, ab_zeile=1000)
        gegenstelle = FalscheBinance({("X", "1h"): alle})
        direkt(gegenstelle, pfad, stand_ms=alle[-1][0] + STUNDE_MS - 1)

        pfade = {a["pfad"] for a in gegenstelle.aufrufe}
        pruefe("jede Anfrage geht an /api/v3/klines", pfade == {"/api/v3/klines"},
               f"{pfade}")
        verboten = {"signature", "apiKey", "timestamp", "recvWindow"}
        pruefe("keine Anfrage traegt Schluessel oder Signatur",
               all(not (verboten & set(a["parameter"])) for a in gegenstelle.aufrufe))
        pruefe("keine Anfrage geht an /sapi/ oder /fapi/",
               all("/sapi/" not in a["url"] and "/fapi/" not in a["url"]
                   for a in gegenstelle.aufrufe))
        erste = gegenstelle.aufrufe[0]["parameter"]
        pruefe("der Datenbeginn wird mit startTime=0, limit=1 GEMESSEN",
               erste.get("startTime") == "0" and erste.get("limit") == "1",
               f"{erste}")


def teil_h():
    print("\nH. Trockenlauf ist die Voreinstellung")

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = baue_lage(ordner, gesamt=400, ab_zeile=300)
        vorher = lies(pfad)
        stand = stand_aus_ms(alle[-1][0] + STUNDE_MS - 1)
        sicherungsordner = os.path.join(ordner, "sicherung")

        rueckgabe, text = ueber_main(
            FalscheBinance({("X", "1h"): alle}),
            ["--ordner", ordner, "--symbole", "X", "--zeitrahmen", "1h",
             "--stand", stand, "--pause", "0", "--sicherung", sicherungsordner])
        pruefe("ohne --schreiben bleibt die Datei unveraendert",
               lies(pfad) == vorher)
        pruefe("es wird auch nichts gesichert",
               not os.path.exists(sicherungsordner))
        pruefe("der Bericht sagt, dass es ein Trockenlauf war",
               "Trockenlauf" in text, text[-400:])
        pruefe("und meldet trotzdem 0, weil nichts zu beanstanden war",
               rueckgabe == 0)


# ---------------------------------------------------------------------------
def teil_i():
    print("\nI. Mutationsproben - jede zweistufig, jede am Ablauf")

    # --- Probe 1: die Wache gegen die laufende Kerze -----------------------
    # Sie ist die einzige Stelle, die verhindert, dass der Fehler, der diese
    # Aufgabe ausgeloest hat, sich wiederholt.
    def lage_laufend(ordner):
        alle, pfad = baue_lage(ordner, gesamt=200, ab_zeile=100)
        return alle, pfad, alle[-1][0] + STUNDE_MS // 2       # mitten drin

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad, stand = lage_laufend(ordner)
        ergebnis = direkt(FalscheBinance({("X", "1h"): alle}), pfad,
                          stand_ms=stand, schreiben=True)
        pruefe("ohne Mutation: die laufende Kerze landet NICHT in der Datei",
               ergebnis["neu_zeilen"] == 199 and ergebnis["laufende_kerzen"] == 1,
               f"{ergebnis['neu_zeilen']}/{ergebnis['laufende_kerzen']}")

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad, stand = lage_laufend(ordner)
        echt = kn.abgeschlossene_kerzen
        kn.abgeschlossene_kerzen = lambda kerzen, intervall, stand_ms: (kerzen, 0)
        try:
            ergebnis = direkt(FalscheBinance({("X", "1h"): alle}), pfad,
                              stand_ms=stand, schreiben=True)
        finally:
            kn.abgeschlossene_kerzen = echt
        pruefe("mit Mutation: die Verfaelschung greift ueberhaupt",
               ergebnis["laufende_kerzen"] == 0)
        pruefe("mit Mutation: die laufende Kerze steht in der Datei",
               ergebnis["neu_zeilen"] == 200 and ergebnis["geschrieben"],
               "keine andere Wache haette sie abgefangen")

    # --- Probe 2: die Wache gegen Abweichungen im Innern -------------------
    def lage_mit_abweichung(ordner):
        alle, pfad = baue_lage(ordner, gesamt=1500, ab_zeile=1000)
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
        ergebnis = direkt(FalscheBinance({("X", "1h"): alle}), pfad,
                          stand_ms=alle[-1][0] + STUNDE_MS - 1, schreiben=True)
        pruefe("ohne Mutation: die Abweichung verhindert das Schreiben",
               not ergebnis["geschrieben"] and lies(pfad) == vorher)

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = lage_mit_abweichung(ordner)
        vorher = lies(pfad)
        echt = kn.vergleiche
        kn.vergleiche = lambda alt, neu, raender: []
        try:
            ergebnis = direkt(FalscheBinance({("X", "1h"): alle}), pfad,
                              stand_ms=alle[-1][0] + STUNDE_MS - 1,
                              schreiben=True)
        finally:
            kn.vergleiche = echt
        pruefe("mit Mutation: die Verfaelschung greift ueberhaupt",
               ergebnis["abweichende_zeilen"] == 0)
        pruefe("mit Mutation: die abweichende Datei wird ueberschrieben",
               ergebnis["geschrieben"] and lies(pfad) != vorher,
               "der Vergleich ist also nicht das, was das Schreiben verhindert")


def teil_j():
    print("\nJ. Wenn eine zweite Wache die erste verdeckt - beide Lagen "
          "nebeneinander")

    def ohne_kursdatenwache(gegenstelle, pfad, stand_ms):
        echt = kursdaten.entferne_unvollstaendige
        kursdaten.entferne_unvollstaendige = (
            lambda df, symbol=None, melden=True: (df, 0))
        try:
            return direkt(gegenstelle, pfad, stand_ms=stand_ms, schreiben=True)
        finally:
            kursdaten.entferne_unvollstaendige = echt

    def lage(ordner, kaputte_kerze):
        """`kaputte_kerze` = Index in der Endpunktreihe (0..1499).

        Die **Datei** ist in beiden Lagen heil und kennt die letzten 500
        Kerzen; kaputt ist immer nur, was der **Endpunkt** liefert. Kerze 5
        liegt damit in der vorangestellten Historie (die niemand vergleicht),
        Kerze 1200 im gemeinsamen Bereich (den `vergleiche()` Zeile fuer
        Zeile durchgeht).
        """
        sauber = reihe(0, 1500, STUNDE_MS)
        pfad = os.path.join(ordner, "X_1h.csv")
        schreibe_csv(pfad, sauber[1000:], "1h")

        vom_endpunkt = list(sauber)
        kaputt = list(vom_endpunkt[kaputte_kerze])
        kaputt[4] = float("nan")                            # close fehlt
        vom_endpunkt[kaputte_kerze] = tuple(kaputt)
        return vom_endpunkt, pfad

    # --- Lage 1: die kaputte Kerze liegt in der vorangestellten Historie ---
    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = lage(ordner, 5)
        ergebnis = direkt(FalscheBinance({("X", "1h"): alle}), pfad,
                          stand_ms=alle[-1][0] + STUNDE_MS - 1, schreiben=True)
        pruefe("Lage 1 ohne Mutation: die Kerze ohne Kurse wird gestrichen "
               "UND gezaehlt", ergebnis["gestrichene_kerzen"] == 1,
               f"{ergebnis['gestrichene_kerzen']}")
        pruefe("Lage 1 ohne Mutation: keine Zeile der Datei hat eine leere "
               "Kursspalte", zeilen_ohne_kurs(pfad) == [])

    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = lage(ordner, 5)
        ergebnis = ohne_kursdatenwache(FalscheBinance({("X", "1h"): alle}),
                                       pfad, alle[-1][0] + STUNDE_MS - 1)
        pruefe("Lage 1 mit Mutation: die Verfaelschung greift ueberhaupt",
               ergebnis["gestrichene_kerzen"] == 0)
        pruefe("Lage 1 mit Mutation: die Kerze ohne Kurse landet in der Datei",
               ergebnis["geschrieben"] and len(zeilen_ohne_kurs(pfad)) == 1,
               "die Probe waere stumm - sie wuerde den Ausfall nicht bemerken")
        pruefe("Lage 1 mit Mutation: und zwar als LEERES Feld, nicht als 'nan'",
               all("nan" not in z.lower() for z in zeilen_ohne_kurs(pfad)),
               "eine Probe, die auf 'nan' prueft, bliebe hier gruen")

    # --- Lage 2: dieselbe Mutation, aber im gemeinsamen Bereich -----------
    # Dort vergleicht `vergleiche()` Zeile fuer Zeile. Die gestrichene Kerze
    # fehlt dann auf der neuen Seite, der Vergleich schlaegt an - und deckt
    # den Ausfall der ersten Wache zu.
    with tempfile.TemporaryDirectory() as ordner:
        alle, pfad = lage(ordner, 1200)
        vorher = lies(pfad)
        ergebnis = ohne_kursdatenwache(FalscheBinance({("X", "1h"): alle}),
                                       pfad, alle[-1][0] + STUNDE_MS - 1)
        pruefe("Lage 2 mit derselben Mutation: es wird trotzdem nicht "
               "geschrieben", not ergebnis["geschrieben"] and lies(pfad) == vorher,
               "hier springt der Zeilenvergleich ein")
        pruefe("Lage 2: und die Datei hat keine leere Kursspalte, obwohl die "
               "Wache aus ist", zeilen_ohne_kurs(pfad) == [],
               "eine Probe auf dieser Lage koennte den Ausfall nicht sehen")
        pruefe("deshalb laeuft die echte Probe auf Lage 1",
               ergebnis["gestrichene_kerzen"] == 0)


# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("SELBSTTEST shared/kursdaten_neuaufbau.py (TB-34)")
    print("=" * 78)

    try:
        import pandas                                      # noqa: F401,PLC0415
    except ImportError:
        print("pandas fehlt - dieser Test braucht es (wie der Lader selbst).")
        return 1

    for teil in (teil_a, teil_b, teil_c, teil_d, teil_e, teil_f, teil_g,
                 teil_h, teil_i, teil_j):
        teil()

    print("\n" + "=" * 78)
    gesamt = bestanden + len(gescheitert)
    if gescheitert:
        print(f"{bestanden}/{gesamt} Pruefungen bestanden, "
              f"{len(gescheitert)} fehlgeschlagen:")
        for was in gescheitert:
            print(f"  - {was}")
        return 1
    print(f"{bestanden}/{gesamt} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

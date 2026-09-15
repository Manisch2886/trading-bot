#!/usr/bin/env python3
"""
Abrufskripte haltbar machen: keine Teilkerze, keine Verkuerzung (TB-35)
==============================================================================
Die acht `fetch_*.py` dieses Projekts holen Kursdaten vom Endpunkt und
schreiben sie nach `data/`. Sie taten das bis TB-35 mit zwei Eigenschaften,
die einzeln harmlos aussehen und zusammen den Kursdatenbestand still
beschaedigen:

1. **Sie uebernahmen die laufende Kerze.** Der Endpunkt liefert den gerade
   angefangenen Zeitraum mit - mit den Werten, die er in diesem Augenblick
   hat. Eine solche Zeile sieht aus wie jede andere.
2. **Sie ueberschreiben die Zieldatei vollstaendig** (`df.to_csv(...)`). Was
   der eine Lauf an Historie mitbrachte, ersetzt restlos, was der vorige
   hinterlassen hat.

Warum das zusammen gefaehrlich ist, und zwar jetzt
------------------------------------------------------------------------------
Am 15.09.2026 wurde der gesamte Krypto-Bestand nativ neu geladen (TB-34,
`shared/kursdaten_neuaufbau.py`): 72 Dateien, +382.039 Zeilen, BTC und ETH ab
2017-08-17. Dieser Bestand ist **ohne** Teilkerzen entstanden, und sein
SHA-256 ueber alle Kursdateien steht als Datenstand-Hash in der
Vorregistrierung (`research/vorregistrierung/herkunft.py`, eingetragen in
`docs/VORREGISTRIERUNG_neuselektion.md`).

**Ein einziger Handstart eines `fetch_*.py` genuegte, um eine dieser Dateien
zu ueberschreiben, die abschliessende Teilkerze wiederherzustellen und damit
den Datenstand-Hash unbemerkt zu aendern.** Nicht in ferner Zukunft, sondern
beim naechsten Mal, wenn jemand "mal eben die Daten frisch zieht".

Die Abhilfe steht im Projekt schon richtig da
------------------------------------------------------------------------------
`shared/kursdaten_neuaufbau.py` uebernimmt nur, was der Endpunkt als
**abgeschlossen** meldet: `close_time <= Stand`. Dieses Modul traegt denselben
Gedanken in die Abrufskripte - mit einem Unterschied, der kein Detail ist:

    Der Neuaufbau sieht die ROHEN Kerzenfelder des Endpunkts und kann
    `close_time` (Feld 6) unmittelbar lesen. Die Abrufskripte sehen nur noch
    den fertigen DataFrame mit den Spalten open_time/open/high/low/close/
    volume - eine `close_time` gibt es dort NICHT (nachgerechnet an den
    Kursdateien selbst: `head -1 data/BTCUSDT_1h.csv`).

Der Schluss des Zeitraums wird hier deshalb aus `open_time` und der
Intervalllaenge gerechnet, mit **derselben Formel** wie im Neuaufbau
(`schluss = oeffnung + laenge - 1`, behalten bei `schluss <= Stand`). Die
Laengen kommen aus `binance_historie.INTERVALL_MS` - eine zweite Tabelle
waere genau die Doppelfuehrung, die in diesem Projekt schon einmal
auseinandergelaufen ist.

Warum das auch fuer Aktien stimmt, ohne Boersenkalender
------------------------------------------------------------------------------
Eine Tageskerze der NYSE ist nicht um 24:00 Uhr fertig, sondern um 16:00
Ortszeit - also um 20:00 UTC (Sommerzeit) bzw. 21:00 UTC (Winterzeit). Die
Regel oben verlangt fuer eine Kerze mit `open_time = D` den Stand
`D 23:59:59` und wartet damit **drei bis vier Stunden laenger** als noetig.

Das ist Absicht, und es ist der Grund, warum hier **kein** Boersenkalender
gebraucht wird, obwohl das Projekt an anderer Stelle ausdruecklich einen
verlangt (`notifications/boersenkalender.py`, "eine eigene Zeitregel -
ABGELEHNT"). Der Unterschied liegt in der Frage:

  * Dort wird gefragt **"ist die Boerse JETZT offen?"** - eine Frage mit zwei
    Fehlerrichtungen. Wer sie zu frueh mit "geschlossen" beantwortet,
    verschleppt einen Ausstieg; wer sie zu spaet mit "offen" beantwortet,
    handelt zu einem Kurs, den es nicht gibt. Eine Faustregel ist dort in
    BEIDE Richtungen falsch, und deshalb unbrauchbar.
  * Hier wird gefragt **"ist dieser Zeitraum SICHER vorbei?"** - eine Frage
    mit nur einer teuren Fehlerrichtung. Zu frueh "ja" schreibt eine
    Teilkerze, und genau das soll nie passieren. Zu spaet "ja" kostet
    nichts: die Kerze kommt beim naechsten Lauf dazu, vollstaendig.

Eine einseitige Frage braucht keine genaue Antwort, sondern eine sichere
Schranke. `D+1 00:00 UTC` liegt garantiert nach jedem NYSE-Schluss des Tages
D - beweisbar aus der Zeitzone allein, ohne Feiertagsliste, ohne verkuerzte
Handelstage, ohne Paket, das auf dem Rechner des Betreibers fehlen kann.
Ein Kalender an dieser Stelle waere eine Abhaengigkeit mehr fuer einen
Gewinn, den niemand braucht.

Die zweite Haelfte: eine Wache gegen unbemerkte Verkuerzung
------------------------------------------------------------------------------
Ueberschreiben bleibt (die Begruendung steht in `docs/ERGEBNIS_TB-35_*.md`
und im Kopf der Abrufskripte). Ueberschreiben heisst aber: **ein Lauf kann
eine Datei kuerzer zuruecklassen, als sie war** - wenn der Endpunkt weniger
Historie liefert als beim letzten Mal, wenn ein `LOOKBACK` unbemerkt
schneidet, wenn eine Antwort abbricht. Der Verlust sieht hinterher aus wie
"so war es schon immer".

Dagegen steht hier eine Wache. Sie schlaegt an, wenn eine Datei nach dem
Abruf

  * **weniger Zeilen** hat als vorher,
  * **spaeter beginnt** als vorher,
  * **frueher endet** als vorher, oder
  * **verschwunden** ist.

Sie schlaegt ausdruecklich NICHT an, wenn eine Datei nur verlaengert wurde,
gleich geblieben ist oder neu hinzukommt - das ist der Normalfall.

**Sie meldet und stoppt nie.** Der Live-Betrieb dieses Projekts (die neun
`forward_test.py`) holt seine Daten ohnehin live und liest `data/` gar nicht;
eine Wache, die einen Abruf abbricht, koennte trotzdem einen Cronjob
zerreissen, und der Schaden waere groesser als der Befund. Der Rueckgabewert
1 bei Befund folgt der Hausregel aus `shared/kursdaten.py`: "ein Befund ist
kein Fehler des Programms, aber etwas, das ein Cronjob-Aufruf sichtbar machen
soll."

Nutzung als eigenstaendiges Werkzeug
------------------------------------------------------------------------------
    python3 shared/abrufschutz.py --aufnehmen /tmp/vorher.json
    ... hier den Abruf laufen lassen ...
    python3 shared/abrufschutz.py --vergleiche /tmp/vorher.json   # 1 bei Befund

    python3 shared/abrufschutz.py --aufnehmen X --ordner ANDERER_ORDNER
    python3 shared/abrufschutz.py --vergleiche X --json bericht.json

Rueckgabewerte: 0 ohne Befund, 1 mit Befund, 2 bei Bedienfehler.
"""

import argparse
import csv
import datetime as dt
import glob
import json
import os
import sys

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
if _SHARED_DIR not in sys.path:
    sys.path.insert(0, _SHARED_DIR)

import binance_historie as bh                              # noqa: E402

# Eine Tabelle, nicht zwei - siehe Modulkopf.
INTERVALL_MS = bh.INTERVALL_MS

ZEITSPALTE = "open_time"


# ===========================================================================
# Teil 1 - Die laufende Kerze entsteht gar nicht erst
# ===========================================================================
def jetzt_utc():
    """Der Stand, wenn keiner uebergeben wird: jetzt, naiv in UTC.

    Naiv und in UTC, weil die Kursdateien dieses Repos ihre Zeitstempel so
    fuehren (`2017-08-17 04:00:00`, ohne Offset) und `binance_historie` sie so
    liest. Eine ortszeitbehaftete Auslegung waere im Sommer zwei Stunden
    daneben - genug, um eine laufende Kerze fuer abgeschlossen zu halten.
    """
    return dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)


def als_ms(zeitpunkt):
    """Naiver UTC-Zeitpunkt -> Millisekunden seit der Epoche."""
    return int((zeitpunkt - dt.datetime(1970, 1, 1)).total_seconds() * 1000)


def _oeffnungszeiten_ms(spalte):
    """Die Spalte `open_time` als Millisekunden - OHNE sie zu veraendern.

    Das ist die wichtigste Zeile dieses Moduls, und zwar wegen dem, was sie
    NICHT tut: Sie gibt eine NEUE Reihe zurueck und schreibt nichts in den
    DataFrame zurueck.

    Der Grund ist der Datenstand-Hash. Die Tagesdateien dieses Repos stehen
    als `2017-08-17` in der CSV, die Stundendateien als
    `2017-08-17 04:00:00`. Wuerde diese Funktion die Spalte in einen
    pandas-Zeitstempel umwandeln und der Aufrufer schriebe sie so zurueck,
    machte `to_csv` aus jedem `2017-08-17` ein `2017-08-17 00:00:00` - alle
    Zeilen zeichenverschieden, alle Pruefsummen neu, und das ohne dass sich
    an den Kursen irgendetwas geaendert haette. Die Umrechnung dient
    ausschliesslich dem Vergleich.

    Erkannt werden: Zahlen (Millisekunden oder Sekunden seit der Epoche, wie
    der Endpunkt sie liefert) und alles, was `pandas.to_datetime` versteht -
    Zeichenketten in beiden Schreibweisen dieses Repos ebenso wie eine
    bereits zeitstempelwertige Spalte. Welche Form `shared/fetch_binance_data.py`
    tatsaechlich liefert, ist aus der Cloud nicht feststellbar (die Datei ist
    gitignoriert, siehe Bericht) - deshalb alle.
    """
    import pandas as pd                                    # noqa: PLC0415

    if len(spalte) == 0:
        return None

    if pd.api.types.is_numeric_dtype(spalte):
        # float64 statt int64: eine fehlende Zahl wuerde `astype("int64")`
        # werfen, und ein Absturz an dieser Stelle waere schlimmer als ein
        # NaN, das weiter unten als "nicht abgeschlossen" gilt. Millisekunden
        # seit 1970 bleiben in float64 exakt (< 2^53 bis ins Jahr 287396).
        zahlen = spalte.astype("float64")
        groesste = zahlen.abs().max()
        # Sekunden oder Millisekunden? 1e11 ms ist 1973, 1e11 s waere das
        # Jahr 5138 - die Grenze trennt beide Faelle fuer jeden Zeitpunkt,
        # der in Kursdaten vorkommen kann.
        if pd.notna(groesste) and groesste < 100_000_000_000:
            return zahlen * 1000
        return zahlen

    umgerechnet = pd.to_datetime(spalte, errors="coerce")
    # Ein zeitzonenbehafteter Zeitstempel wird nach UTC gebracht und dann
    # naiv gelesen - dieselbe Lesart wie `jetzt_utc()`.
    try:
        if getattr(umgerechnet.dtype, "tz", None) is not None:
            umgerechnet = umgerechnet.dt.tz_convert("UTC").dt.tz_localize(None)
    except (AttributeError, TypeError):                    # noqa: BLE001
        pass
    epoche = pd.Timestamp("1970-01-01")
    return (umgerechnet - epoche).dt.total_seconds().mul(1000)


def abgeschlossen_maske(df, intervall, stand=None):
    """True je Zeile, deren Kerzenzeitraum zum Stand vorbei ist.

    `schluss = oeffnung + laenge - 1`, behalten bei `schluss <= Stand` -
    zeichengleich mit `kursdaten_neuaufbau.abgeschlossene_kerzen`, damit
    beide Wege dieselbe Kerze als dieselbe beurteilen.
    """
    import pandas as pd                                    # noqa: PLC0415

    if intervall not in INTERVALL_MS:
        raise ValueError(
            f"Unbekanntes Intervall {intervall!r}. Bekannt: "
            f"{', '.join(sorted(INTERVALL_MS))}. Ohne die Laenge des "
            f"Zeitraums laesst sich nicht sagen, ob er vorbei ist - und "
            f"stillschweigend alles durchzulassen waere genau der Fehler, "
            f"den dieses Modul verhindern soll.")

    if df is None or len(df) == 0:
        return None
    if ZEITSPALTE not in df.columns:
        raise ValueError(
            f"Spalte {ZEITSPALTE!r} fehlt - ohne sie ist nicht feststellbar, "
            f"welche Kerze laeuft. Vorhanden: {list(df.columns)}")

    stand_ms = als_ms(stand if stand is not None else jetzt_utc())
    laenge = INTERVALL_MS[intervall]
    oeffnung = _oeffnungszeiten_ms(df[ZEITSPALTE])
    schluss = oeffnung + (laenge - 1)
    maske = schluss <= stand_ms
    if not isinstance(maske, pd.Series):
        maske = pd.Series(maske, index=df.index)
    # Ein unlesbarer Zeitstempel (NaT -> NaN) gilt NICHT als abgeschlossen.
    # Nichts zu wissen ist hier kein Grund, etwas durchzulassen.
    return maske.fillna(False).astype(bool)


def nur_abgeschlossene(df, intervall, stand=None, symbol=None, melden=True):
    """(df ohne laufende Kerze, Anzahl verworfener Zeilen).

    Streicht und ZAEHLT - derselbe Grundsatz wie in `shared/kursdaten.py`:
    ein stillschweigend gestrichener Datenpunkt ist dasselbe Problem in
    Gruen.

    Die zurueckgegebene Tabelle ist eine ZEILENAUSWAHL der uebergebenen -
    keine Spalte wird umgeschrieben, keine Zahl neu formatiert. Wer das
    Ergebnis mit `to_csv` schreibt, bekommt fuer jede behaltene Zeile
    dieselben Zeichen wie vorher.
    """
    if df is None or len(df) == 0:
        return df, 0

    maske = abgeschlossen_maske(df, intervall, stand)
    if maske is None:
        return df, 0

    verworfen = int((~maske).sum())
    if verworfen == 0:
        return df, 0

    # Nach Position auswaehlen, nicht ueber den Index: ein DataFrame mit
    # doppelten Indexwerten wuerde bei einer index-behafteten Maske nicht das
    # tun, wonach es aussieht.
    behalten = df[maske.to_numpy()]
    if melden:
        name = f"{symbol}: " if symbol else ""
        print(f"    Hinweis: {name}{verworfen} laufende Kerze(n) verworfen "
              f"(von {len(df)}, Intervall {intervall}). Ihr Zeitraum ist noch "
              f"nicht vorbei; geschrieben wird nur, was abgeschlossen ist.")
    return behalten, verworfen


# ===========================================================================
# Teil 2 - Die Wache gegen unbemerkte Verkuerzung
# ===========================================================================
# Die drei Befundarten. Getrennt gefuehrt, weil sie sich NICHT gegenseitig
# vertreten: eine Datei kann bei gleicher Zeilenzahl spaeter beginnen (dann
# ist vorne etwas weg und hinten etwas dazugekommen), und sie kann bei
# gleicher Zeilenzahl frueher enden (dann ist hinten etwas weg). Wer nur die
# Zeilenzahl prueft, sieht beides nicht.
VERKUERZT = "verkuerzt"
SPAETERER_BEGINN = "spaeterer_beginn"
FRUEHERES_ENDE = "frueheres_ende"
VERSCHWUNDEN = "verschwunden"


def zustand(pfad):
    """Was eine Kursdatei an nachpruefbarer Substanz hat - oder None.

    Zurueck kommt {zeilen, erste, letzte}; `None`, wenn es die Datei nicht
    gibt. Bewusst ohne pandas und ohne die Datei ganz im Speicher zu halten:
    diese Funktion laeuft im Abrufskript einmal je Symbol, und `data/` enthaelt
    Dateien mit ueber 70.000 Zeilen.
    """
    if not os.path.exists(pfad):
        return None
    zeilen = 0
    erste = None
    letzte = None
    with open(pfad, "r", encoding="utf-8", newline="") as datei:
        leser = csv.reader(datei)
        try:
            kopf = next(leser)
        except StopIteration:
            return {"zeilen": 0, "erste": None, "letzte": None}
        try:
            spalte = kopf.index(ZEITSPALTE)
        except ValueError:
            spalte = 0
        for satz in leser:
            if not satz:
                continue
            zeilen += 1
            wert = satz[spalte] if spalte < len(satz) else ""
            if erste is None:
                erste = wert
            letzte = wert
    return {"zeilen": zeilen, "erste": erste, "letzte": letzte}


def aufnehmen(ordner=None, muster="*.csv", pfade=None):
    """Momentaufnahme eines Datenordners: Dateiname -> Zustand."""
    if pfade is None:
        pfade = sorted(glob.glob(os.path.join(ordner, muster)))
    return {os.path.basename(p): zustand(p) for p in pfade}


def _fruehere(a, b):
    """True, wenn Zeitstempel `a` VOR `b` liegt.

    Die Zeitstempel dieses Repos sind `YYYY-MM-DD` bzw.
    `YYYY-MM-DD HH:MM:SS`. In beiden Schreibweisen ist der Zeichenvergleich
    derselbe wie der Zeitvergleich, und `2017-08-17` sortiert vor
    `2017-08-17 04:00:00` - also vor jeder Uhrzeit desselben Tages. Das ist
    genau die gewuenschte Lesart.

    Stehen dort Zahlen (Millisekunden seit 1970, wie der Endpunkt sie
    liefert), waere der Zeichenvergleich falsch: '9' sortiert nach '10'.
    Deshalb zuerst der Zahlenvergleich, und nur wenn der nicht geht, der
    Zeichenvergleich. Fuer alles andere wird nicht geraten: unvergleichbare
    Werte ergeben "keine Aussage" und damit keinen Befund.
    """
    if a is None or b is None:
        return False
    try:
        return float(a) < float(b)
    except (TypeError, ValueError):
        return str(a) < str(b)


def vergleiche(vorher, nachher):
    """Was ein Abruf an Substanz gekostet hat. Liste von Befunden.

    Kein Befund ist: mehr Zeilen, gleich viele Zeilen, frueherer Beginn,
    spaeteres Ende, eine neu hinzugekommene Datei. Das sind die Normalfaelle
    eines gelungenen Abrufs, und eine Wache, die dabei anschlaegt, wird nach
    der dritten Meldung nicht mehr gelesen.
    """
    befunde = []
    for name in sorted(vorher):
        alt = vorher[name]
        if alt is None:
            continue
        neu = nachher.get(name)

        if neu is None:
            befunde.append({"datei": name, "art": VERSCHWUNDEN,
                            "vorher": alt, "nachher": None,
                            "text": (f"{name}: die Datei ist nach dem Abruf "
                                     f"nicht mehr da (vorher {alt['zeilen']} "
                                     f"Zeilen).")})
            continue

        if neu["zeilen"] < alt["zeilen"]:
            befunde.append({"datei": name, "art": VERKUERZT,
                            "vorher": alt, "nachher": neu,
                            "text": (f"{name}: {alt['zeilen']} -> "
                                     f"{neu['zeilen']} Zeilen "
                                     f"({alt['zeilen'] - neu['zeilen']} "
                                     f"weniger).")})

        if _fruehere(alt["erste"], neu["erste"]):
            befunde.append({"datei": name, "art": SPAETERER_BEGINN,
                            "vorher": alt, "nachher": neu,
                            "text": (f"{name}: beginnt jetzt bei "
                                     f"{neu['erste']} statt {alt['erste']} - "
                                     f"vorne fehlt Historie.")})

        if _fruehere(neu["letzte"], alt["letzte"]):
            befunde.append({"datei": name, "art": FRUEHERES_ENDE,
                            "vorher": alt, "nachher": neu,
                            "text": (f"{name}: endet jetzt bei "
                                     f"{neu['letzte']} statt {alt['letzte']} - "
                                     f"hinten fehlt Historie.")})
    return befunde


class Wache:
    """Die Wache fuer den Gebrauch IM Abrufskript.

    Warum das Werkzeug zwar eigenstaendig ist, aber trotzdem von den
    Abrufskripten gerufen wird - beides zusammen, und nicht das eine statt
    des anderen:

    * **Eigenstaendig**, weil die Logik genau einmal existieren soll. Acht
      Abrufskripte mit acht Kopien derselben Pruefung waeren die
      Doppelfuehrung, an der dieses Projekt schon einmal Zahlen verloren
      hat. Und weil ein Werkzeug mit `main()` auch dann noch etwas taugt,
      wenn eine Datei auf einem ganz anderen Weg kuerzer geworden ist.
    * **Trotzdem im Abrufskript**, weil die Wache einen Vergleichswert von
      VOR dem Lauf braucht. Wer sie erst hinterher von Hand startet, hat
      nichts mehr, womit er vergleichen koennte - die alte Fassung ist dann
      ja schon ueberschrieben. Und der Fall, um den es geht, ist gerade der
      unangekuendigte Handstart, bei dem niemand an eine zweite Pruefung
      denkt.

    Gebrauch:

        wache = Wache()
        ...
        wache.vormerken(zieldatei)      # VOR dem Schreiben
        df.to_csv(zieldatei, index=False)
        wache.pruefe(zieldatei)         # meldet sofort, stoppt nie
        ...
        wache.melde()                   # eine Zeile am Ende
    """

    def __init__(self, melden=True):
        self.melden = melden
        self.vorher = {}
        self.befunde = []

    def vormerken(self, pfad):
        self.vorher[os.path.basename(pfad)] = zustand(pfad)

    def pruefe(self, pfad):
        name = os.path.basename(pfad)
        if name not in self.vorher:
            return []
        neue = vergleiche({name: self.vorher[name]}, {name: zustand(pfad)})
        for befund in neue:
            if self.melden:
                print(f"    WACHE: {befund['text']}")
        self.befunde.extend(neue)
        return neue

    def bericht(self):
        if not self.befunde:
            return None
        dateien = sorted({b["datei"] for b in self.befunde})
        return (f"WACHE: {len(self.befunde)} Befund(e) in {len(dateien)} "
                f"Datei(en) - dieser Abruf hat Kursdaten zurueckgelassen, die "
                f"kuerzer sind als vorher. Betroffen: {', '.join(dateien)}. "
                f"Es wurde NICHTS gestoppt und nichts zurueckgenommen; die "
                f"alten Staende stehen im letzten Commit.")

    def melde(self):
        text = self.bericht()
        if text:
            print("\n" + text)
        return text


# ===========================================================================
# Kommandozeile
# ===========================================================================
def _lade(pfad):
    with open(pfad, "r", encoding="utf-8") as datei:
        inhalt = json.load(datei)
    return inhalt.get("dateien", inhalt)


def main(argv=None) -> int:
    standard = os.path.join(os.path.dirname(_SHARED_DIR), "data")

    zerleger = argparse.ArgumentParser(
        description="Wache gegen unbemerkte Verkuerzung von Kursdateien: "
                    "nimmt einen Stand auf und vergleicht spaeter dagegen.")
    zerleger.add_argument("--aufnehmen", metavar="PFAD", default=None,
                          help="Momentaufnahme nach PFAD schreiben")
    zerleger.add_argument("--vergleiche", metavar="PFAD", default=None,
                          help="gegen die Momentaufnahme in PFAD pruefen")
    zerleger.add_argument("--ordner", default=standard)
    zerleger.add_argument("--muster", default="*.csv")
    zerleger.add_argument("--json", metavar="PFAD", default=None,
                          help="Befunde zusaetzlich als JSON ablegen")
    argumente = zerleger.parse_args(argv)

    if bool(argumente.aufnehmen) == bool(argumente.vergleiche):
        print("Genau eines von --aufnehmen / --vergleiche angeben.",
              file=sys.stderr)
        return 2

    if not os.path.isdir(argumente.ordner):
        print(f"Ordner nicht gefunden: {argumente.ordner}", file=sys.stderr)
        return 2

    if argumente.aufnehmen:
        stand = aufnehmen(argumente.ordner, argumente.muster)
        ziel = argumente.aufnehmen
        if os.path.dirname(ziel):
            os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "w", encoding="utf-8") as datei:
            json.dump({"ordner": os.path.abspath(argumente.ordner),
                       "erzeugt": dt.datetime.now().isoformat(timespec="seconds"),
                       "dateien": stand},
                      datei, indent=2, ensure_ascii=False, sort_keys=True)
        print(f"Stand aufgenommen: {len(stand)} Datei(en) in "
              f"{argumente.ordner} -> {ziel}")
        return 0

    try:
        vorher = _lade(argumente.vergleiche)
    except (OSError, ValueError) as fehler:
        print(f"Momentaufnahme nicht lesbar: {fehler}", file=sys.stderr)
        return 2

    nachher = aufnehmen(argumente.ordner, argumente.muster)
    befunde = vergleiche(vorher, nachher)

    print(f"Verglichen: {len(vorher)} Datei(en) aus der Momentaufnahme gegen "
          f"{len(nachher)} in {argumente.ordner}")

    if argumente.json:
        with open(argumente.json, "w", encoding="utf-8") as datei:
            json.dump({"befunde": befunde}, datei, indent=2,
                      ensure_ascii=False, sort_keys=True)
        print(f"JSON: {argumente.json}")

    if not befunde:
        print("Kein Befund: keine Datei ist kuerzer geworden, beginnt spaeter "
              "oder endet frueher als vorher.")
        return 0

    print(f"\n{len(befunde)} BEFUND(E):")
    for befund in befunde:
        print(f"  [{befund['art']}] {befund['text']}")
    print("\nEs wurde nichts gestoppt und nichts zurueckgenommen - diese "
          "Wache meldet nur. Die alten Staende stehen im letzten Commit "
          "(`git diff --stat data/`).")
    # Rueckgabewert 1: ein Befund ist kein Fehler des Programms, aber etwas,
    # das ein Cronjob-Aufruf sichtbar machen soll (wie shared/kursdaten.py).
    return 1


if __name__ == "__main__":
    sys.exit(main())

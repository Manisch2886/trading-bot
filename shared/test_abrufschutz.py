#!/usr/bin/env python3
"""
Selbsttests zu shared/abrufschutz.py (TB-35)
==============================================================================
Geprueft wird das VERHALTEN, nicht das Vorhandensein von Codestuecken.

Der Kern sind die Abschnitte 2 und 3: die acht Abrufskripte werden
**tatsaechlich ausgefuehrt**, gegen erzeugte Beispieldaten, in einem
Miniatur-Abbild des Projekts unter /tmp. Beobachtet wird, was danach in der
CSV steht - nicht, ob im Quelltext ein Aufruf vorkommt. Ein Abrufskript, das
`abrufschutz` zwar einbindet, aber nicht benutzt, faellt hier durch.

Die zwei wiederkehrenden Fallen dieses Projekts sind ausdruecklich adressiert:

* **Eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
  selbst.** Deshalb die Mutationsproben in Abschnitt 3 und 6: dort wird die
  Absicherung ausgeschaltet und nachgesehen, ob die Pruefung, die sie
  bewachen soll, daraufhin auch wirklich FEHLSCHLAEGT. Eine Pruefung, die
  auch ohne Absicherung gruen bleibt, prueft nichts.
* **Eine zweite Wache verdeckt das Fehlen der ersten.** Die Wache in
  `abrufschutz` hat drei unabhaengige Kriterien. Abschnitt 5 gibt jedem
  Kriterium einen Fall, den KEIN anderes Kriterium bemerkt, und Abschnitt 6
  schaltet die Kriterien einzeln ab und prueft nach, dass dann genau der eine
  zugehoerige Fall verlorengeht - und die anderen beiden nicht.

Ohne Netz. Binance und yfinance sind aus der Cloud gesperrt; hier laeuft
nichts gegen einen Endpunkt, sondern gegen Attrappen, die dieselbe
Schnittstelle bedienen.

Nutzung:  python3 shared/test_abrufschutz.py
"""

import ast
import datetime as dt
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

_SHARED = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED)
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

import pandas as pd                                            # noqa: E402

import abrufschutz                                             # noqa: E402

BESTANDEN = 0
FEHLER = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
        print(f"  [OK ] {name}" + (f"   {detail}" if detail else ""))
    else:
        FEHLER.append(name)
        print(f"  [FEHLER] {name}" + (f"   {detail}" if detail else ""))


# ===========================================================================
# Das Miniatur-Abbild des Projekts
# ===========================================================================
# Die acht Abrufskripte rechnen ihren shared/-Ordner aus der eigenen Lage aus
# (`dirname(dirname(_STRATEGY_DIR)) + "/shared"`). Genau das wird hier
# ausgenutzt: wird das Skript in einen nachgebauten Baum kopiert, findet es
# dort die Attrappen statt der echten Module - und vor allem ein DATA_DIR,
# das NICHT auf data/ dieses Repos zeigt. Kein Test dieser Datei fasst den
# echten Kursdatenbestand an.
ABRUFSKRIPTE = [
    ("shared/fetch_multi_data.py",                            "1h", "TESTUSDT"),
    ("strategies/t3_supertrend/fetch_4h_data.py",             "4h", "TESTUSDT"),
    ("strategies/rsi2_crypto/fetch_1d_data.py",               "1d", "TESTUSDT"),
    ("strategies/volatility_breakout_crypto/fetch_1d_data.py", "1d", "TESTUSDT"),
    ("strategies/elliott_wave_stocks/fetch_stock_data.py",    "1d", "TESTAG"),
    ("strategies/rsi2_mean_reversion/fetch_stock_data.py",    "1d", "TESTAG"),
    ("strategies/turtle_soup_stocks/fetch_stock_data.py",     "1d", "TESTAG"),
    ("strategies/volatility_breakout/fetch_stock_data.py",    "1d", "TESTAG"),
]

ANZAHL_KERZEN = 6

STUB_BINANCE_CLIENT = '''
class Client:
    KLINE_INTERVAL_1HOUR = "1h"
    KLINE_INTERVAL_4HOUR = "4h"
    KLINE_INTERVAL_1DAY = "1d"

    def __init__(self, *args, **kwargs):
        pass
'''

STUB_FETCH_BINANCE = '''
"""Attrappe fuer shared/fetch_binance_data.py (gitignoriert, siehe Bericht).

Liefert ein festes Gitter aus ANZAHL abgeschlossenen Kerzen PLUS der einen
Kerze, die zum Zeitpunkt des Aufrufs gerade laeuft - so, wie der echte
Endpunkt es tut. Welche das ist, wird protokolliert, damit der Test sie
nachher in der CSV suchen kann, ohne sie selbst auszurechnen.
"""
import datetime as dt
import json
import os

import pandas as pd

SEKUNDEN = {"1h": 3600, "4h": 14400, "1d": 86400}
ANZAHL = %(anzahl)d


def _gitter(intervall):
    sek = SEKUNDEN[intervall]
    epoche = dt.datetime(1970, 1, 1)
    jetzt = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    marke = int((jetzt - epoche).total_seconds()) // sek * sek
    laufend = epoche + dt.timedelta(seconds=marke)
    return [laufend - dt.timedelta(seconds=sek * k)
            for k in range(ANZAHL - 1, -1, -1)]


def _protokoll(schluessel, zeiten, fmt):
    pfad = os.environ.get("STUB_PROTOKOLL")
    if not pfad:
        return
    eintraege = {}
    if os.path.exists(pfad):
        with open(pfad, encoding="utf-8") as datei:
            eintraege = json.load(datei)
    eintraege[schluessel] = {
        "alle": [z.strftime(fmt) for z in zeiten],
        "laufend": zeiten[-1].strftime(fmt),
        "letzte_abgeschlossene": zeiten[-2].strftime(fmt),
    }
    with open(pfad, "w", encoding="utf-8") as datei:
        json.dump(eintraege, datei, indent=2, sort_keys=True)


def fetch_historical_data(symbol, interval, lookback=None, **kwargs):
    zeiten = _gitter(interval)
    fmt = "%%Y-%%m-%%d" if interval == "1d" else "%%Y-%%m-%%d %%H:%%M:%%S"
    _protokoll(f"{symbol}_{interval}", zeiten, fmt)
    n = len(zeiten)
    return pd.DataFrame({
        "open_time": [z.strftime(fmt) for z in zeiten],
        "open":   [100.0 + i for i in range(n)],
        "high":   [101.0 + i for i in range(n)],
        "low":    [99.0 + i for i in range(n)],
        "close":  [100.5 + i for i in range(n)],
        "volume": [10.0 + i for i in range(n)],
    })
''' % {"anzahl": ANZAHL_KERZEN}

STUB_YFINANCE = '''
"""Attrappe fuer yfinance. Liefert Tageszeilen einschliesslich der von HEUTE -
die ist am laufenden Handelstag noch nicht fertig, genau wie beim Original.
"""
import datetime as dt
import json
import os

import pandas as pd

ANZAHL = %(anzahl)d


def download(tickers, period=None, interval="1d", progress=False,
             auto_adjust=True, **kwargs):
    heute = dt.datetime.now(dt.timezone.utc).date()
    tage = [heute - dt.timedelta(days=k) for k in range(ANZAHL - 1, -1, -1)]

    pfad = os.environ.get("STUB_PROTOKOLL")
    if pfad:
        eintraege = {}
        if os.path.exists(pfad):
            with open(pfad, encoding="utf-8") as datei:
                eintraege = json.load(datei)
        eintraege[f"{tickers}_{interval}"] = {
            "alle": [t.isoformat() for t in tage],
            "laufend": tage[-1].isoformat(),
            "letzte_abgeschlossene": tage[-2].isoformat(),
        }
        with open(pfad, "w", encoding="utf-8") as datei:
            json.dump(eintraege, datei, indent=2, sort_keys=True)

    n = len(tage)
    index = pd.DatetimeIndex([pd.Timestamp(t) for t in tage], name="Date")
    return pd.DataFrame({
        "Open":   [100.0 + i for i in range(n)],
        "High":   [101.0 + i for i in range(n)],
        "Low":    [99.0 + i for i in range(n)],
        "Close":  [100.5 + i for i in range(n)],
        "Volume": [10.0 + i for i in range(n)],
    }, index=index)
''' % {"anzahl": ANZAHL_KERZEN}

STUB_PATHS = 'import os\nDATA_DIR = os.environ["TEST_DATA_DIR"]\n'
STUB_STRATEGY_PATHS = '''
import os


def get_strategy_paths(datei=None):
    ordner = os.environ["TEST_DATA_DIR"]
    return {"DATA_DIR": ordner, "BASE_DIR": os.path.dirname(ordner),
            "RESULTS_DIR": ordner, "STRATEGY_DIR": os.path.dirname(ordner)}
'''


def baue_abbild(wurzel):
    """Das Miniatur-Projekt anlegen und die Pfade zurueckgeben."""
    shared = os.path.join(wurzel, "shared")
    stubs = os.path.join(wurzel, "stubs")
    daten = os.path.join(wurzel, "data")
    for ordner in (shared, stubs, daten, os.path.join(stubs, "binance")):
        os.makedirs(ordner, exist_ok=True)

    # Echte Module - unveraendert uebernommen, damit hier geprueft wird, was
    # spaeter auch laeuft.
    for name in ("abrufschutz.py", "kursdaten.py", "binance_historie.py"):
        shutil.copy2(os.path.join(_SHARED, name), os.path.join(shared, name))

    def schreibe(pfad, inhalt):
        with open(pfad, "w", encoding="utf-8") as datei:
            datei.write(inhalt)

    schreibe(os.path.join(shared, "paths.py"), STUB_PATHS)
    schreibe(os.path.join(shared, "strategy_paths.py"), STUB_STRATEGY_PATHS)
    schreibe(os.path.join(shared, "symbols_config.py"), 'SYMBOLS = ["TESTUSDT"]\n')
    schreibe(os.path.join(shared, "stocks_symbols_config.py"), 'SYMBOLS = ["TESTAG"]\n')
    schreibe(os.path.join(shared, "fetch_binance_data.py"), STUB_FETCH_BINANCE)

    # binance und yfinance werden GANZ OBEN in den Abrufskripten eingebunden,
    # noch bevor sie shared/ in den Suchpfad legen - die beiden muessen also
    # ueber PYTHONPATH kommen.
    schreibe(os.path.join(stubs, "binance", "__init__.py"), "")
    schreibe(os.path.join(stubs, "binance", "client.py"), STUB_BINANCE_CLIENT)
    schreibe(os.path.join(stubs, "yfinance.py"), STUB_YFINANCE)

    for rel, _intervall, _symbol in ABRUFSKRIPTE:
        ziel = os.path.join(wurzel, rel)
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        shutil.copy2(os.path.join(BASE_DIR, rel), ziel)

    return {"wurzel": wurzel, "shared": shared, "stubs": stubs, "daten": daten}


def starte(abbild, rel, protokoll):
    """Ein Abrufskript wirklich laufen lassen. (Rueckgabewert, Ausgabe)"""
    umgebung = os.environ.copy()
    umgebung["PYTHONPATH"] = abbild["stubs"]
    umgebung["TEST_DATA_DIR"] = abbild["daten"]
    umgebung["STUB_PROTOKOLL"] = protokoll
    skript = os.path.join(abbild["wurzel"], rel)
    lauf = subprocess.run([sys.executable, os.path.basename(skript)],
                          cwd=os.path.dirname(skript), env=umgebung,
                          capture_output=True, text=True, timeout=300)
    return lauf.returncode, lauf.stdout + lauf.stderr


def lies_zeiten(pfad):
    if not os.path.exists(pfad):
        return None
    with open(pfad, encoding="utf-8") as datei:
        zeilen = [z.strip() for z in datei if z.strip()]
    return [z.split(",")[0] for z in zeilen[1:]]


def voller_lauf(abbild, protokoll):
    """Alle acht Abrufskripte der Reihe nach. -> {rel: (rc, ausgabe)}"""
    if os.path.exists(protokoll):
        os.remove(protokoll)
    ergebnisse = {}
    for rel, _intervall, _symbol in ABRUFSKRIPTE:
        ergebnisse[rel] = starte(abbild, rel, protokoll)
    return ergebnisse


# ===========================================================================
# 1. Die laufende Kerze - die Regel selbst
# ===========================================================================
def test_regel():
    print("\n1. Die Regel: nur abgeschlossene Zeitraeume")

    stand = dt.datetime(2026, 9, 15, 12, 30)
    df = pd.DataFrame({"open_time": ["2026-09-15 10:00:00",
                                     "2026-09-15 11:00:00",
                                     "2026-09-15 12:00:00"],
                       "close": [1, 2, 3]})
    behalten, verworfen = abrufschutz.nur_abgeschlossene(df, "1h", stand=stand,
                                                         melden=False)
    check("1h: die laufende Kerze wird verworfen", verworfen == 1)
    check("1h: die abgeschlossenen bleiben",
          list(behalten["open_time"]) == ["2026-09-15 10:00:00",
                                          "2026-09-15 11:00:00"])

    # Genau auf der Grenze: 11:00 + 1h = 12:00. Zum Stand 12:00 ist der
    # Zeitraum vorbei - dieselbe Lesart wie kursdaten_neuaufbau
    # (close_time 11:59:59.999 <= Stand).
    _, verworfen = abrufschutz.nur_abgeschlossene(
        df, "1h", stand=dt.datetime(2026, 9, 15, 12, 0), melden=False)
    check("Grenzfall: exakt zum Kerzenschluss gilt sie als abgeschlossen",
          verworfen == 1)
    _, verworfen = abrufschutz.nur_abgeschlossene(
        df, "1h", stand=dt.datetime(2026, 9, 15, 11, 59, 59), melden=False)
    check("Grenzfall: eine Sekunde davor noch nicht", verworfen == 2)

    # Aktien-Tageskerze: D 20:00 UTC liegt NACH dem NYSE-Schluss, aber die
    # Regel wartet bis D+1 00:00 UTC. Absicht, siehe Modulkopf.
    tage = pd.DataFrame({"open_time": ["2026-09-13", "2026-09-14", "2026-09-15"],
                         "close": [1, 2, 3]})
    behalten, verworfen = abrufschutz.nur_abgeschlossene(
        tage, "1d", stand=dt.datetime(2026, 9, 15, 20, 0), melden=False)
    check("1d: der laufende Handelstag wird verworfen", verworfen == 1,
          f"behalten: {list(behalten['open_time'])}")
    _, verworfen = abrufschutz.nur_abgeschlossene(
        tage, "1d", stand=dt.datetime(2026, 9, 16, 0, 0), melden=False)
    check("1d: am Folgetag 00:00 UTC ist er abgeschlossen", verworfen == 0)

    # Alle Schreibweisen, die shared/fetch_binance_data.py liefern KOENNTE -
    # die Datei ist gitignoriert und aus der Cloud nicht lesbar.
    epoche = dt.datetime(1970, 1, 1)
    ms = [int((dt.datetime(2026, 9, t) - epoche).total_seconds() * 1000)
          for t in (13, 14, 15)]
    formen = {
        "Zeichenkette": tage,
        "Millisekunden": pd.DataFrame({"open_time": ms, "close": [1, 2, 3]}),
        "Sekunden": pd.DataFrame({"open_time": [m // 1000 for m in ms],
                                  "close": [1, 2, 3]}),
        "Zeitstempel": pd.DataFrame({"open_time": pd.to_datetime(
            ["2026-09-13", "2026-09-14", "2026-09-15"]), "close": [1, 2, 3]}),
    }
    for name, probe in formen.items():
        _, verworfen = abrufschutz.nur_abgeschlossene(
            probe, "1d", stand=dt.datetime(2026, 9, 15, 20, 0), melden=False)
        check(f"open_time als {name}: eine Kerze verworfen", verworfen == 1)

    # Eine fehlende Zahl in einer Zahlenspalte darf nicht zum Absturz fuehren
    # - und schon gar nicht durchrutschen.
    luecke = pd.DataFrame({"open_time": [ms[0], float("nan"), ms[2]],
                           "close": [1, 2, 3]})
    behalten, verworfen = abrufschutz.nur_abgeschlossene(
        luecke, "1d", stand=dt.datetime(2026, 9, 15, 20, 0), melden=False)
    check("fehlende Zahl in der Zeitspalte: kein Absturz, nicht durchgelassen",
          verworfen == 2 and len(behalten) == 1)

    # Ein DataFrame mit doppelten Indexwerten darf nicht ueber den Index
    # ausgewaehlt werden - sonst tut die Maske nicht, wonach sie aussieht.
    doppelt = pd.DataFrame({"open_time": ["2026-09-13", "2026-09-14",
                                          "2026-09-15"], "close": [1, 2, 3]},
                           index=[0, 0, 0])
    behalten, verworfen = abrufschutz.nur_abgeschlossene(
        doppelt, "1d", stand=dt.datetime(2026, 9, 15, 20, 0), melden=False)
    check("doppelte Indexwerte: die Auswahl bleibt richtig",
          verworfen == 1 and list(behalten["open_time"]) == ["2026-09-13",
                                                             "2026-09-14"])

    # Nichts zu wissen ist kein Grund, etwas durchzulassen.
    kaputt = pd.DataFrame({"open_time": ["2026-09-13", "voellig unlesbar"],
                           "close": [1, 2]})
    behalten, verworfen = abrufschutz.nur_abgeschlossene(
        kaputt, "1d", stand=dt.datetime(2026, 9, 20), melden=False)
    check("unlesbarer Zeitstempel gilt NICHT als abgeschlossen",
          verworfen == 1 and list(behalten["open_time"]) == ["2026-09-13"])

    # Ein unbekanntes Intervall darf nicht stillschweigend alles durchlassen.
    try:
        abrufschutz.abgeschlossen_maske(tage, "15m")
        check("unbekanntes Intervall wird zurueckgewiesen", False)
    except ValueError:
        check("unbekanntes Intervall wird zurueckgewiesen", True)

    # Und die Spalte selbst bleibt unangetastet - sonst aendert to_csv die
    # Schreibweise und damit den Datenstand-Hash, ohne dass sich ein Kurs
    # geaendert haette.
    behalten, _ = abrufschutz.nur_abgeschlossene(
        tage, "1d", stand=dt.datetime(2026, 9, 15, 20, 0), melden=False)
    check("die Spalte open_time wird nicht umgeschrieben",
          list(behalten["open_time"]) == ["2026-09-13", "2026-09-14"]
          and behalten["open_time"].dtype == tage["open_time"].dtype,
          f"dtype {behalten['open_time'].dtype}")


# ===========================================================================
# 2. Der Ablauf: die acht Abrufskripte wirklich laufen lassen
# ===========================================================================
def test_ablauf(abbild, protokoll):
    print("\n2. Der Ablauf: acht Abrufskripte gegen Beispieldaten")

    ergebnisse = voller_lauf(abbild, protokoll)
    with open(protokoll, encoding="utf-8") as datei:
        gemeldet = json.load(datei)

    for rel, intervall, symbol in ABRUFSKRIPTE:
        rc, ausgabe = ergebnisse[rel]
        kurz = os.path.basename(os.path.dirname(rel)) + "/" + os.path.basename(rel)
        check(f"{kurz}: laeuft durch", rc == 0, f"rc={rc} {ausgabe[-200:]}"
              if rc != 0 else "")

        schluessel = f"{symbol}_{intervall}"
        if schluessel not in gemeldet:
            check(f"{kurz}: Attrappe wurde gerufen", False)
            continue

        datei = os.path.join(abbild["daten"], f"{symbol}_{intervall}.csv")
        zeiten = lies_zeiten(datei)
        laufend = gemeldet[schluessel]["laufend"]
        letzte = gemeldet[schluessel]["letzte_abgeschlossene"]

        check(f"{kurz}: die laufende Kerze steht NICHT in der Datei",
              zeiten is not None and laufend not in zeiten,
              f"laufend={laufend} Datei endet auf {zeiten[-1] if zeiten else '-'}")
        check(f"{kurz}: die letzte abgeschlossene steht drin",
              zeiten is not None and zeiten and zeiten[-1] == letzte,
              f"erwartet {letzte}")
        check(f"{kurz}: alle uebrigen Kerzen sind da",
              zeiten is not None and len(zeiten) == ANZAHL_KERZEN - 1,
              f"{len(zeiten) if zeiten else 0} statt {ANZAHL_KERZEN - 1}")

    return ergebnisse


# ===========================================================================
# 3. Mutationsprobe: ohne die Absicherung muss Abschnitt 2 fehlschlagen
# ===========================================================================
def test_mutation_laufende_kerze(protokoll):
    print("\n3. Mutationsprobe: Absicherung aus -> Abschnitt 2 muss fallen")

    with tempfile.TemporaryDirectory() as wurzel:
        abbild = baue_abbild(wurzel)

        # Die Absicherung wird zur Durchreiche gemacht. Nichts sonst.
        pfad = os.path.join(abbild["shared"], "abrufschutz.py")
        with open(pfad, encoding="utf-8") as datei:
            text = datei.read()
        marke = "    if df is None or len(df) == 0:\n        return df, 0\n\n    maske = abgeschlossen_maske(df, intervall, stand)"
        if marke not in text:
            check("Mutationsstelle in nur_abgeschlossene gefunden", False)
            return
        check("Mutationsstelle in nur_abgeschlossene gefunden", True)
        with open(pfad, "w", encoding="utf-8") as datei:
            datei.write(text.replace(marke, "    return df, 0\n\n    maske = "
                                            "abgeschlossen_maske(df, intervall, stand)"))

        ergebnisse = voller_lauf(abbild, protokoll)
        with open(protokoll, encoding="utf-8") as datei:
            gemeldet = json.load(datei)

        durchgerutscht = 0
        for rel, intervall, symbol in ABRUFSKRIPTE:
            rc, _ = ergebnisse[rel]
            zeiten = lies_zeiten(os.path.join(abbild["daten"],
                                              f"{symbol}_{intervall}.csv"))
            laufend = gemeldet.get(f"{symbol}_{intervall}", {}).get("laufend")
            if rc == 0 and zeiten and laufend in zeiten:
                durchgerutscht += 1

        check("ohne Absicherung schreiben ALLE acht Skripte die laufende Kerze",
              durchgerutscht == len(ABRUFSKRIPTE),
              f"{durchgerutscht} von {len(ABRUFSKRIPTE)}")
        print("       -> Abschnitt 2 pruefte also wirklich etwas: mit "
              "Absicherung kam die Zeile nirgends an, ohne sie ueberall.")


# ===========================================================================
# 4. Der Datenstand-Hash bleibt stehen, wenn sich nichts geaendert hat
# ===========================================================================
def _hash(ordner):
    pfad = os.path.join(BASE_DIR, "research", "vorregistrierung")
    if pfad not in sys.path:
        sys.path.insert(0, pfad)
    import herkunft                                            # noqa: PLC0415
    return herkunft.datenstand(ordner)


def test_datenstand(protokoll):
    print("\n4. Zweiter Abruflauf, gleiche Daten -> gleicher Datenstand-Hash")

    # Das Gitter der Attrappe haengt an der laufenden Stunde. Wandert sie
    # zwischen den beiden Laeufen weiter, aendern sich die DATEN - dann sagt
    # der Hash zu Recht etwas anderes, und die Probe wird einmal wiederholt.
    for versuch in (1, 2):
        marke_vor = int(time.time()) // 3600
        with tempfile.TemporaryDirectory() as wurzel:
            abbild = baue_abbild(wurzel)
            voller_lauf(abbild, protokoll)
            erst = _hash(abbild["daten"])
            voller_lauf(abbild, protokoll)
            zweit = _hash(abbild["daten"])
        if int(time.time()) // 3600 == marke_vor:
            break
        if versuch == 1:
            print("       (Stundenwechsel waehrend der Probe - Wiederholung)")

    check("der zweite Lauf erzeugt dieselben Dateien",
          erst["datenstand"] == zweit["datenstand"],
          f"{erst['datenstand'][:12]} / {zweit['datenstand'][:12]}")
    check("beide Laeufe sehen gleich viele Dateien",
          erst["dateien"] == zweit["dateien"] == 4,
          f"{erst['dateien']} / {zweit['dateien']}")
    print("       -> Ein Handstart eines Abrufskripts aendert den "
          "Datenstand-Hash nicht mehr, solange sich an den Kursen nichts "
          "aendert. Genau das war vorher nicht so.")


# ===========================================================================
# 5. Die Wache: drei Kriterien, drei Faelle, die einander nicht vertreten
# ===========================================================================
def _schreibe_csv(pfad, tage):
    with open(pfad, "w", encoding="utf-8") as datei:
        datei.write("open_time,open,high,low,close,volume\n")
        for i, tag in enumerate(tage):
            datei.write(f"{tag},{100 + i},{101 + i},{99 + i},{100 + i},{10 + i}\n")


# Der Ausgangsstand und was ein misslungener Abruf daraus macht. Jeder Fall
# ist so gebaut, dass ihn GENAU EIN Kriterium bemerkt.
FAELLE = {
    # gleiche Raender, eine Zeile aus der Mitte fehlt -> nur die Zeilenzahl
    "nur_kuerzer": (["2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04",
                     "2026-09-05"],
                    ["2026-09-01", "2026-09-02", "2026-09-04", "2026-09-05"],
                    {abrufschutz.VERKUERZT}),
    # gleiche Zeilenzahl, Fenster nach hinten gerutscht -> nur der Beginn
    "nur_spaeter": (["2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04",
                     "2026-09-05"],
                    ["2026-09-02", "2026-09-03", "2026-09-04", "2026-09-05",
                     "2026-09-06"],
                    {abrufschutz.SPAETERER_BEGINN}),
    # gleiche Zeilenzahl, Fenster nach vorn gerutscht -> nur das Ende
    "nur_frueher_ende": (["2026-09-02", "2026-09-03", "2026-09-04",
                          "2026-09-05", "2026-09-06"],
                         ["2026-09-01", "2026-09-02", "2026-09-03",
                          "2026-09-04", "2026-09-05"],
                         {abrufschutz.FRUEHERES_ENDE}),
    # der Normalfall: nur verlaengert
    "verlaengert": (["2026-09-01", "2026-09-02"],
                    ["2026-09-01", "2026-09-02", "2026-09-03"],
                    set()),
    # und der haeufigste: gar nichts passiert
    "unveraendert": (["2026-09-01", "2026-09-02"],
                     ["2026-09-01", "2026-09-02"],
                     set()),
}


def _baue_wachprobe(ordner):
    for name, (vorher, _nachher, _erwartet) in FAELLE.items():
        _schreibe_csv(os.path.join(ordner, f"{name}.csv"), vorher)


def _fuehre_abruf_aus(ordner):
    for name, (_vorher, nachher, _erwartet) in FAELLE.items():
        _schreibe_csv(os.path.join(ordner, f"{name}.csv"), nachher)


def _wache_laufen(modul, ordner, aufnahme, vergleichen=False):
    argumente = (["--vergleiche", aufnahme] if vergleichen
                 else ["--aufnehmen", aufnahme])
    lauf = subprocess.run([sys.executable, modul] + argumente
                          + ["--ordner", ordner],
                          capture_output=True, text=True, timeout=120)
    return lauf.returncode, lauf.stdout + lauf.stderr


def _befunde_je_datei(ordner, aufnahme):
    vorher = abrufschutz._lade(aufnahme)
    nachher = abrufschutz.aufnehmen(ordner)
    je_datei = {}
    for befund in abrufschutz.vergleiche(vorher, nachher):
        je_datei.setdefault(befund["datei"][:-4], set()).add(befund["art"])
    return je_datei


def test_wache():
    print("\n5. Die Wache: jedes Kriterium hat einen eigenen Fall")

    with tempfile.TemporaryDirectory() as wurzel:
        ordner = os.path.join(wurzel, "data")
        os.makedirs(ordner)
        aufnahme = os.path.join(wurzel, "vorher.json")
        modul = os.path.join(_SHARED, "abrufschutz.py")

        _baue_wachprobe(ordner)
        rc, _ = _wache_laufen(modul, ordner, aufnahme)
        check("Stand aufnehmen geht durch", rc == 0)

        # Erst gar nichts tun: die Wache darf nicht anschlagen.
        rc, ausgabe = _wache_laufen(modul, ordner, aufnahme, vergleichen=True)
        check("ohne Aenderung: kein Befund, Rueckgabewert 0", rc == 0,
              ausgabe.strip().splitlines()[-1] if ausgabe.strip() else "")

        # Jetzt der misslungene Abruf.
        _fuehre_abruf_aus(ordner)
        rc, ausgabe = _wache_laufen(modul, ordner, aufnahme, vergleichen=True)
        check("nach der Verkuerzung: Rueckgabewert 1", rc == 1)
        check("die Ausgabe nennt keine Blockade",
              "meldet nur" in ausgabe and "nichts gestoppt" in ausgabe)

        gefunden = _befunde_je_datei(ordner, aufnahme)
        for name, (_v, _n, erwartet) in FAELLE.items():
            check(f"{name}: Befunde {sorted(erwartet) or 'keine'}",
                  gefunden.get(name, set()) == erwartet,
                  f"gefunden: {sorted(gefunden.get(name, set()))}")

        # Eine verschwundene Datei ist ebenfalls ein Befund.
        os.remove(os.path.join(ordner, "unveraendert.csv"))
        gefunden = _befunde_je_datei(ordner, aufnahme)
        check("eine verschwundene Datei wird gemeldet",
              gefunden.get("unveraendert") == {abrufschutz.VERSCHWUNDEN})

        # Eine NEUE Datei ist keiner - sonst meldet die Wache bei jedem
        # ersten Lauf und wird nach dem dritten Mal nicht mehr gelesen.
        _schreibe_csv(os.path.join(ordner, "ganz_neu.csv"), ["2026-09-01"])
        gefunden = _befunde_je_datei(ordner, aufnahme)
        check("eine neu hinzugekommene Datei ist kein Befund",
              "ganz_neu" not in gefunden)

    # Der Vergleich zweier Zeitstempel: bei Zahlen sortiert '9' nach '10',
    # ein reiner Zeichenvergleich waere dort falsch herum.
    check("Zeitvergleich: Zeichenketten des Repos",
          abrufschutz._fruehere("2026-09-01", "2026-09-02")
          and not abrufschutz._fruehere("2026-09-02", "2026-09-01")
          and abrufschutz._fruehere("2026-09-01", "2026-09-01 04:00:00"))
    check("Zeitvergleich: Millisekunden werden als Zahl verglichen",
          abrufschutz._fruehere("9", "10")
          and not abrufschutz._fruehere("10", "9"))
    check("Zeitvergleich: ohne Aussage kein Befund",
          not abrufschutz._fruehere(None, "2026-09-01")
          and not abrufschutz._fruehere("2026-09-01", None))


# ===========================================================================
# 6. Mutationsproben zur Wache: verdeckt ein Kriterium das Fehlen eines
#    anderen?
# ===========================================================================
MUTATIONEN = {
    abrufschutz.VERKUERZT:
        ('if neu["zeilen"] < alt["zeilen"]:', "nur_kuerzer"),
    abrufschutz.SPAETERER_BEGINN:
        ('if _fruehere(alt["erste"], neu["erste"]):', "nur_spaeter"),
    abrufschutz.FRUEHERES_ENDE:
        ('if _fruehere(neu["letzte"], alt["letzte"]):', "nur_frueher_ende"),
}


def test_mutation_wache():
    print("\n6. Mutationsprobe: jedes Kriterium einzeln abschalten")

    with open(os.path.join(_SHARED, "abrufschutz.py"), encoding="utf-8") as datei:
        original = datei.read()

    for art, (zeile, fall) in MUTATIONEN.items():
        if original.count(zeile) != 1:
            check(f"{art}: Mutationsstelle eindeutig", False,
                  f"{original.count(zeile)} Treffer")
            continue

        with tempfile.TemporaryDirectory() as wurzel:
            shared = os.path.join(wurzel, "shared")
            ordner = os.path.join(wurzel, "data")
            os.makedirs(shared)
            os.makedirs(ordner)
            for name in ("kursdaten.py", "binance_historie.py"):
                shutil.copy2(os.path.join(_SHARED, name),
                             os.path.join(shared, name))
            modul = os.path.join(shared, "abrufschutz.py")
            with open(modul, "w", encoding="utf-8") as datei:
                datei.write(original.replace(zeile, "if False:"))

            aufnahme = os.path.join(wurzel, "vorher.json")
            _baue_wachprobe(ordner)
            _wache_laufen(modul, ordner, aufnahme)
            _fuehre_abruf_aus(ordner)
            rc, ausgabe = _wache_laufen(modul, ordner, aufnahme, vergleichen=True)

            verloren = fall not in ausgabe
            check(f"{art} abgeschaltet -> {fall} wird NICHT mehr gefunden",
                  verloren, "" if verloren else "wurde trotzdem gemeldet")

            noch_da = [f for f in MUTATIONEN.values() if f[1] != fall]
            check(f"{art} abgeschaltet -> die anderen beiden Faelle bleiben",
                  all(anderer in ausgabe for _z, anderer in
                      [(z, n) for z, n in noch_da]),
                  f"rc={rc}")

    print("       -> Kein Kriterium wird von einem anderen mitgetragen: "
          "faellt eines aus, faellt genau sein Fall aus.")


# ===========================================================================
# 7. Feste Startdaten statt mitwandernder Fenster
# ===========================================================================
def _konstante(pfad, name):
    with open(pfad, encoding="utf-8") as datei:
        baum = ast.parse(datei.read())
    for knoten in baum.body:
        if isinstance(knoten, ast.Assign):
            for ziel in knoten.targets:
                if isinstance(ziel, ast.Name) and ziel.id == name:
                    if isinstance(knoten.value, ast.Constant):
                        return knoten.value.value
    return None


def test_lookback():
    print("\n7. LOOKBACK: feste Startdaten, keine mitwandernden Fenster")

    krypto = [rel for rel, _i, s in ABRUFSKRIPTE if s == "TESTUSDT"]
    for rel in krypto:
        wert = _konstante(os.path.join(BASE_DIR, rel), "LOOKBACK")
        kurz = os.path.basename(os.path.dirname(rel)) + "/" + os.path.basename(rel)
        check(f"{kurz}: LOOKBACK ist ein festes Datum",
              wert == "1 Jan, 2017", f"steht: {wert!r}")

    # Die Gegenprobe zur alten Fassung: ein Fenster, das mit dem Abruftag
    # mitwandert, faellt hier auf - egal in welcher Schreibweise.
    alle = glob.glob(os.path.join(BASE_DIR, "strategies", "*", "fetch_*.py"))
    alle += [os.path.join(BASE_DIR, "shared", "fetch_multi_data.py")]
    wandernd = []
    for pfad in alle:
        wert = _konstante(pfad, "LOOKBACK")
        if isinstance(wert, str) and "ago" in wert:
            wandernd.append((os.path.relpath(pfad, BASE_DIR), wert))
    check("kein Abrufskript benutzt mehr ein mitwanderndes Fenster",
          not wandernd, str(wandernd))

    # Und die Begruendung, die nachweislich falsch war, steht nicht mehr da.
    reste = []
    for pfad in alle:
        with open(pfad, encoding="utf-8") as datei:
            text = datei.read()
        if "Binance liefert ohnehin" in text:
            reste.append(os.path.relpath(pfad, BASE_DIR))
    check("die widerlegte Begruendung ist entfernt", not reste, str(reste))


# ===========================================================================
def main():
    print("=" * 78)
    print("Selbsttests zu shared/abrufschutz.py (TB-35)")
    print("=" * 78)

    with tempfile.TemporaryDirectory() as wurzel:
        abbild = baue_abbild(wurzel)
        protokoll = os.path.join(wurzel, "stub_protokoll.json")

        tests = [
            ("test_regel", lambda: test_regel()),
            ("test_ablauf", lambda: test_ablauf(abbild, protokoll)),
            ("test_mutation_laufende_kerze",
             lambda: test_mutation_laufende_kerze(protokoll)),
            ("test_datenstand", lambda: test_datenstand(protokoll)),
            ("test_wache", lambda: test_wache()),
            ("test_mutation_wache", lambda: test_mutation_wache()),
            ("test_lookback", lambda: test_lookback()),
        ]
        for name, test in tests:
            try:
                test()
            except Exception as fehler:                        # noqa: BLE001
                import traceback
                FEHLER.append(f"{name} (Ausnahme)")
                print(f"  [FEHLER] {name} warf eine Ausnahme: {fehler}")
                traceback.print_exc()

    print("\n" + "=" * 78)
    gesamt = BESTANDEN + len(FEHLER)
    print(f"{BESTANDEN} von {gesamt} Pruefungen bestanden, "
          f"{len(FEHLER)} fehlgeschlagen.")
    for name in FEHLER:
        print(f"  - {name}")
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())

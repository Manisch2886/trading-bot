"""
Selbsttests zu TB-45, Teil 4: ein leeres Symbol beendet keinen Lauf mehr
==============================================================================
DER BEFUND (TB-42, beim Bau des Lauftests gefunden)

Kam fuer ein Symbol ein **leerer Kursrahmen** zurueck - ausgefallene
Kursquelle, gescheiterter Abruf -, brachen `elliott_wave` und
`elliott_wave_stocks` mit `IndexError` ab (`calculate_zigzag`, `highs[0]`).
**Der ganze Lauf endete, nicht nur das eine Symbol.** Fiel eine Kursquelle
fuer ein einziges Symbol aus, handelten damit zwei von neun Bots an diesem
Tag gar nicht.

WAS HIER GEPRUEFT WIRD - UND WIE

  1  Der harte Stopp an der Stelle, an der er entstand: `calculate_zigzag`
     und `calculate_zigzag_with_confirmation` auf einem leeren Rahmen.
     ⚠ Und die Gegenprobe, ohne die die Reparatur nichts wert waere: auf
     ECHTEN Kursdaten liefern beide Funktionen **Pivot fuer Pivot, Spalte
     fuer Spalte dasselbe** wie die Fassung aus `origin/main`.
  2  Der ganze Lauf, am VERHALTEN: `forward_test.py` laeuft wirklich, als
     `__main__`, in einem eigenen Prozess je Bot - einmal mit einem leeren
     Symbol unter den geladenen, einmal ohne dieses Symbol. Verlangt wird:
     der Lauf kommt durch, er erzeugt **genau eine** Meldung zu dem Symbol,
     und die **Trades der uebrigen Symbole sind Spalte fuer Spalte
     identisch**.
  3  Die Umfrage, die die Aufgabe verlangt: **gibt es weitere Stellen, an
     denen ein einzelnes Symbol den ganzen Lauf beendet?** Alle neun Bots,
     am Ablauf gemessen, nicht aus dem Quelltext geschlossen.

ZU DEN BEISPIELDATEN

Abschnitt 2 rechnet auf ECHTEN Kursdateien aus `data/`, deren Zeitstempel so
verschoben werden, dass die letzte Kerze knapp in der Vergangenheit liegt.
Grund: beide Bots nehmen nur Signale, deren Welle 5 innerhalb der letzten
`SIGNAL_FRESHNESS_HOURS` endete. Mit unverschobenen Daten haingen die
Ergebnisse davon ab, an welchem Tag der Test laeuft - und ein Vergleich
zweier LEERER Trade-Tabellen belegt nichts (dieselbe Falle wie C2 in
`research/universum_trockenlauf`). Verschoben werden ausschliesslich die
Zeitstempel; jeder Kurs bleibt, wie er ist.

⚠ Kein Bot-Code wird importiert - `forward_test.py` laeuft als eigener
Prozess, und die Datenbank liegt in einem Wegwerf-Ordner. Weder `data/` noch
`results/`, `logs/` oder eine echte `*.db` werden beruehrt.

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.

Nutzung:  python3 shared/test_leeres_symbol.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

_SHARED = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED)

ELLIOTT = [("elliott_wave", "BTCUSDT", "1h"),
           ("elliott_wave_stocks", "AAPL", "1d")]
ALLE_BOTS = ["elliott_wave", "elliott_wave_stocks", "rsi2_crypto",
             "rsi2_mean_reversion", "t3_supertrend", "turtle_soup_crypto",
             "turtle_soup_stocks", "volatility_breakout",
             "volatility_breakout_crypto"]

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


def _lauf(programm, *argumente, ordner=None):
    """Ein Programm in einem eigenen Prozess - und sein JSON zurueck.

    Eigener Prozess je Aufruf, weil neun Bots gleichnamige Module fuehren
    (`live_params`, `symbols_config`, `zigzag_indicator`): zwei Bots im
    selben Prozess saehen einander. Der saubere Weg stammt aus TB-40.
    """
    with tempfile.TemporaryDirectory() as tmp:
        skript = os.path.join(tmp, "probe.py")
        with open(skript, "w", encoding="utf-8") as f:
            f.write(programm)
        lauf = subprocess.run([sys.executable, skript] + list(argumente),
                              capture_output=True, text=True, timeout=900,
                              cwd=ordner or BASE_DIR)
    for zeile in reversed(lauf.stdout.splitlines()):
        if zeile.startswith("###"):
            return json.loads(zeile[3:]), lauf
    return None, lauf


# ===========================================================================
# 1  Der harte Stopp - und die Gegenprobe, dass sich am Signal nichts aendert
# ===========================================================================
_ZIGZAG_PROGRAMM = r"""
import json, os, sys
zigzag_dir, datei = sys.argv[1], sys.argv[2]
sys.path.insert(0, zigzag_dir)
import pandas as pd
from zigzag_indicator import calculate_zigzag, calculate_zigzag_with_confirmation

erg = {}
leer = pd.DataFrame({"open_time": [], "open": [], "high": [], "low": [],
                     "close": [], "volume": []})
for name, f in (("zigzag", calculate_zigzag),
                ("zigzag_bestaetigt", calculate_zigzag_with_confirmation)):
    try:
        r = f(leer, deviation_pct=3.0)
        erg[name + "_leer"] = {"pivots": len(r), "spalten": list(r.columns)}
    except Exception as e:
        erg[name + "_leer"] = {"fehler": type(e).__name__ + ": " + str(e)[:80]}

# Die Gegenprobe auf ECHTEN Daten: was hier herauskommt, muss vor und nach
# der Reparatur Zeichen fuer Zeichen dasselbe sein.
df = pd.read_csv(datei, parse_dates=["open_time"]).tail(4000).reset_index(drop=True)
for name, f in (("zigzag", calculate_zigzag),
                ("zigzag_bestaetigt", calculate_zigzag_with_confirmation)):
    r = f(df, deviation_pct=3.0)
    erg[name + "_echt"] = r.to_csv(index=False)
print("###" + json.dumps(erg))
"""


def teil_1():
    print("\n1) Der harte Stopp in calculate_zigzag - und die Gegenprobe")
    for bot, symbol, intervall in ELLIOTT:
        botdir = os.path.join(BASE_DIR, "strategies", bot)
        datei = os.path.join(BASE_DIR, "data", f"{symbol}_{intervall}.csv")
        jetzt, lauf = _lauf(_ZIGZAG_PROGRAMM, botdir, datei)
        if jetzt is None:
            check(f"{bot}: die Probe laeuft", False,
                  (lauf.stdout + lauf.stderr)[-300:])
            continue

        for name in ("zigzag", "zigzag_bestaetigt"):
            e = jetzt[name + "_leer"]
            check(f"{bot}/{name}: ein leerer Kursrahmen bricht nicht mehr ab",
                  "fehler" not in e, e.get("fehler", ""))
            check(f"{bot}/{name}: er liefert null Pivots mit den richtigen "
                  f"Spalten",
                  e.get("pivots") == 0 and "time" in e.get("spalten", []),
                  str(e)[:120])

        # -- Gegenprobe gegen die Fassung aus origin/main -------------------
        alt = subprocess.run(
            ["git", "show", f"origin/main:strategies/{bot}/zigzag_indicator.py"],
            cwd=BASE_DIR, capture_output=True, text=True)
        if alt.returncode != 0:
            check(f"{bot}: Fassung aus origin/main lesbar", False,
                  alt.stderr.strip()[:120])
            continue
        # `zigzag_indicator.py` rechnet seinen shared/-Pfad aus dem eigenen
        # `__file__` aus. Die alte Fassung bekommt deshalb einen kleinen
        # Baum in derselben Form - sonst scheitert sie am Import und die
        # Gegenprobe belegte nichts.
        altwurzel = tempfile.mkdtemp(prefix=f"tb45_alt_{bot}_")
        altordner = os.path.join(altwurzel, "strategies", bot)
        os.makedirs(altordner)
        os.makedirs(os.path.join(altwurzel, "shared"))
        shutil.copy(os.path.join(BASE_DIR, "shared", "strategy_paths.py"),
                    os.path.join(altwurzel, "shared"))
        try:
            with open(os.path.join(altordner, "zigzag_indicator.py"), "w",
                      encoding="utf-8") as f:
                f.write(alt.stdout)
            vorher, lauf2 = _lauf(_ZIGZAG_PROGRAMM, altordner, datei)
        finally:
            shutil.rmtree(altwurzel, ignore_errors=True)
        if vorher is None:
            check(f"{bot}: die alte Fassung laeuft auf echten Daten", False,
                  (lauf2.stdout + lauf2.stderr)[-300:])
            continue
        check(f"{bot}: auf echten Daten bricht die ALTE Fassung bei einem "
              f"leeren Rahmen ab - das ist der Befund",
              "fehler" in vorher["zigzag_leer"],
              str(vorher["zigzag_leer"])[:120])
        for name in ("zigzag", "zigzag_bestaetigt"):
            gleich = vorher[name + "_echt"] == jetzt[name + "_echt"]
            zeilen = jetzt[name + "_echt"].count("\n") - 1
            check(f"{bot}/{name}: auf echten Daten Pivot fuer Pivot, Spalte "
                  f"fuer Spalte unveraendert",
                  gleich and zeilen > 0,
                  f"{zeilen} Pivots" if gleich else "ABWEICHUNG")


# ===========================================================================
# 2  Der ganze Lauf - forward_test.py als __main__, am Verhalten
# ===========================================================================
_LAUF_PROGRAMM = r"""
import json, os, runpy, sqlite3, sys
botdir, shared, tmp, datei, symbole, leeres, bezug = sys.argv[1:8]
symbole = symbole.split(",")
os.chdir(botdir)
sys.path.insert(0, shared)
sys.path.insert(0, botdir)

import pandas as pd

# 1. Datenbank, results/ und logs/ in den Wegwerf-Ordner. Die echten
#    Datenbanken liegen auf dem Rechner des Nutzers, sind die einzige
#    OOS-Evidenz des Projekts und nicht neu berechenbar - dieser Test fasst
#    sie nicht an. `DATA_DIR` und `CONFIG_DIR` bleiben echt, damit sich der
#    Bot sonst genau wie im Betrieb verhaelt.
import strategy_paths
_echte_pfade = strategy_paths.get_strategy_paths
def _wegwerf(caller_file):
    p = dict(_echte_pfade(caller_file))
    p.update({"RESULTS_DIR": tmp, "LOGS_DIR": tmp,
              "DB_FILE": os.path.join(tmp, "probe.db")})
    return p
strategy_paths.get_strategy_paths = _wegwerf

# 2. Die Symbolliste dieses Laufs - VOR dem Import von forward_test, das sie
#    mit `from <modul> import SYMBOLS` einmalig zieht. Welches Modul das ist,
#    unterscheidet sich je Bot (`symbols_config` / `stocks_symbols_config`).
for modulname in ("symbols_config", "stocks_symbols_config"):
    try:
        modul = __import__(modulname)
    except ImportError:
        continue
    modul.SYMBOLS = list(symbole)

# 3. Die Kursdaten. ECHTE Datei, nur die Zeitstempel so verschoben, dass die
#    letzte Kerze knapp in der Vergangenheit liegt.
roh = pd.read_csv(datei, parse_dates=["open_time"]).tail(4000).reset_index(drop=True)
# Der Bezugszeitpunkt kommt VON AUSSEN und ist fuer beide Laeufe derselbe.
# Mit `utcnow()` je Prozess laegen die verschobenen Zeitstempel um die
# Laufzeit auseinander - der Spalte-fuer-Spalte-Vergleich waere dann
# grundsaetzlich rot, ohne dass sich am Verhalten etwas geaendert haette.
versatz = pd.Timestamp(bezug) - pd.Timedelta(hours=2) \
          - roh["open_time"].iloc[-1]
roh["open_time"] = roh["open_time"] + versatz
leerer_rahmen = roh.iloc[0:0].copy()

import entscheidungskerze
def _lade(symbol, intervall, markt, abruf=None, **k):
    if symbol == leeres:
        return leerer_rahmen.copy()
    return roh.copy()
entscheidungskerze.lade = _lade
entscheidungskerze.melde = lambda *a, **k: None   # kein Telegram aus einem Test

# 4. Je nichtleerem Symbol eine OFFENE Position vorlegen. Ohne sie haingen
#    die Trade-Tabellen beider Laeufe davon ab, ob gerade ein frisches
#    Wellenmuster in den Daten steht - und zwei LEERE Tabellen zu
#    vergleichen belegt nichts (dieselbe Falle wie C2 im Trockenlauf).
#    Der Stop liegt ueber dem Einstieg, die Position schliesst also auf der
#    naechsten Kerze: derselbe Weg, den der Bot im Betrieb geht, nur ohne
#    Zufall. `init_db` laeuft dafuer ueber den IMPORT von forward_test -
#    dessen `__main__` wird dabei nicht ausgefuehrt.
import forward_test as _ft_vorlage
_conn = _ft_vorlage.init_db()
_zeile = roh.iloc[-300]
for _sym in symbole:
    if _sym == leeres:
        continue
    _conn.execute(
        "INSERT INTO trades (symbol, signal_time, entry_time, entry_price, "
        "stop_price, target_price, status) VALUES (?,?,?,?,?,?,'open')",
        (_sym, str(_zeile["open_time"]), str(_zeile["open_time"]),
         float(_zeile["close"]), float(_zeile["close"]) * 2.0,
         float(_zeile["close"]) * 1.5))
_conn.commit()
_conn.close()
del sys.modules["forward_test"]

runpy.run_path(os.path.join(botdir, "forward_test.py"), run_name="__main__")

conn = sqlite3.connect(os.path.join(tmp, "probe.db"))
trades = pd.read_sql("SELECT * FROM trades ORDER BY symbol, signal_time", conn)
conn.close()
# Die Trades des ausgelassenen Symbols gehoeren nicht in den Vergleich - es
# gibt sie im zweiten Lauf gar nicht. Verglichen wird, was mit den UEBRIGEN
# Symbolen geschah.
uebrige = trades[trades["symbol"] != leeres]
print("###" + json.dumps({"trades": uebrige.to_csv(index=False),
                          "spalten": list(uebrige.columns),
                          "zeilen": len(uebrige)}))
"""


def _jetzt_iso():
    import datetime as dt
    return dt.datetime.utcnow().replace(microsecond=0).isoformat()


def _ausgabe(lauf):
    return lauf.stdout + lauf.stderr


def teil_2():
    print("\n2) Der ganze Lauf - forward_test.py laeuft wirklich")
    for bot, symbol, intervall in ELLIOTT:
        botdir = os.path.join(BASE_DIR, "strategies", bot)
        datei = os.path.join(BASE_DIR, "data", f"{symbol}_{intervall}.csv")
        shared = os.path.join(BASE_DIR, "shared")

        # Ein Bezugszeitpunkt fuer BEIDE Laeufe - siehe Begruendung im
        # Probenprogramm.
        bezug = _jetzt_iso()

        ergebnisse = {}
        for lage, symbole in (("mit_leerem", "AAA,LEER,BBB"),
                              ("ohne_leeres", "AAA,BBB")):
            tmp = tempfile.mkdtemp(prefix=f"tb45_lauf_{bot}_")
            try:
                erg, lauf = _lauf(_LAUF_PROGRAMM, botdir, shared, tmp, datei,
                                  symbole, "LEER", bezug)
                ergebnisse[lage] = (erg, _ausgabe(lauf), lauf.returncode)
            finally:
                shutil.rmtree(tmp, ignore_errors=True)

        erg_mit, text_mit, rc_mit = ergebnisse["mit_leerem"]
        erg_ohne, _text_ohne, _rc_ohne = ergebnisse["ohne_leeres"]

        check(f"{bot}: der Lauf kommt trotz des leeren Symbols durch",
              erg_mit is not None and rc_mit == 0,
              text_mit[-400:] if erg_mit is None else "")
        if erg_mit is None or erg_ohne is None:
            continue

        # Genau EINE Meldung zu dem ausgelassenen Symbol.
        meldungen = [z for z in text_mit.splitlines()
                     if "LEER" in z and "uebersprungen" in z]
        check(f"{bot}: genau EINE Meldung zum ausgelassenen Symbol",
              len(meldungen) == 1, str(meldungen)[:200])
        check(f"{bot}: die Meldung nennt Symbol und Grund",
              bool(meldungen) and "LEER" in meldungen[0]
              and "Kursrahmen" in meldungen[0],
              meldungen[0] if meldungen else "")
        check(f"{bot}: und der Lauf endet nicht mit einem IndexError",
              "IndexError" not in text_mit,
              [z for z in text_mit.splitlines() if "IndexError" in z][:1])

        # Die uebrigen Symbole: Spalte fuer Spalte dasselbe.
        check(f"{bot}: die Trades der uebrigen Symbole sind Spalte fuer "
              f"Spalte identisch",
              erg_mit["trades"] == erg_ohne["trades"],
              f"{erg_mit['zeilen']} gegen {erg_ohne['zeilen']} Zeilen")
        check(f"{bot}: und es sind ueberhaupt Trades entstanden - sonst waere "
              f"der Vergleich leer wahr",
              erg_mit["zeilen"] > 0, erg_mit["zeilen"])


# ===========================================================================
# 3  Die Umfrage: welcher Bot ueberlebt ein leeres Symbol, und warum?
# ===========================================================================
_UMFRAGE_PROGRAMM = r"""
import inspect, json, os, sys
bot, tmp = sys.argv[1], sys.argv[2]
botdir = os.path.join(os.getcwd(), "strategies", bot)
os.chdir(botdir)
sys.path.insert(0, botdir)
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "shared")))
import numpy as np
import pandas as pd

import strategy_paths
def _wegwerf(caller_file):
    return {"BASE_DIR": tmp, "STRATEGY_NAME": bot, "DATA_DIR": tmp,
            "CONFIG_DIR": tmp, "RESULTS_DIR": tmp, "LOGS_DIR": tmp,
            "DB_FILE": os.path.join(tmp, "probe.db")}
strategy_paths.get_strategy_paths = _wegwerf

import forward_test as ft

erg = {"bot": bot}
n = 600
idx = pd.date_range("2024-01-01", periods=n, freq="D")
preis = 100 + np.cumsum(np.random.RandomState(7).normal(0, 1.5, n))
voll = pd.DataFrame({"open_time": idx, "open": preis, "high": preis * 1.02,
                     "low": preis * 0.98, "close": preis,
                     "volume": np.full(n, 1000.0)})
leer = voll.iloc[0:0].copy()

def probe(name, f):
    try:
        f()
        erg[name] = "durchgelaufen"
    except Exception as e:
        erg[name] = type(e).__name__

_STD = {"t3_fast_length": 8, "t3_slow_length": 21, "t3_factor": 0.7,
        "di_length": 14, "adx_length": 14, "atr_length": 22, "atr_mult": 3.0}
if hasattr(ft, "compute_indicators"):
    k = {p: _STD[p] for p in list(inspect.signature(ft.compute_indicators)
                                  .parameters)[1:] if p in _STD}
    probe("compute_indicators_leer", lambda: ft.compute_indicators(leer, **k))
    daten_voll = ft.compute_indicators(voll, **k)
else:
    erg["compute_indicators_leer"] = "keine solche Funktion"
    daten_voll = voll

conn = ft.init_db()
daten = {"AAA": daten_voll, "LEER": leer}
zusatz = {} if len(inspect.signature(ft.find_new_signals).parameters) == 2 \
         else {"btc_regime_bullish": True}
probe("check_open_trades_leer", lambda: ft.check_open_trades(conn, daten))
probe("find_new_signals_leer", lambda: ft.find_new_signals(conn, daten, **zusatz))
conn.close()
print("###" + json.dumps(erg))
"""


def teil_3():
    print("\n3) Umfrage: beendet anderswo ein einzelnes Symbol den ganzen Lauf?")
    befunde = {}
    for bot in ALLE_BOTS:
        tmp = tempfile.mkdtemp(prefix=f"tb45_umfrage_{bot}_")
        try:
            erg, lauf = _lauf(_UMFRAGE_PROGRAMM, bot, tmp)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        if erg is None:
            check(f"{bot}: die Umfrage laeuft", False,
                  _ausgabe(lauf)[-300:])
            continue
        befunde[bot] = erg
        check(f"{bot}: die Signalsuche ueberlebt ein leeres Symbol",
              erg["find_new_signals_leer"] == "durchgelaufen",
              erg["find_new_signals_leer"])
        check(f"{bot}: das Pruefen offener Positionen ebenso",
              erg["check_open_trades_leer"] == "durchgelaufen",
              erg["check_open_trades_leer"])

    # Der Nebenbefund, der dabei herauskam: bei `t3_supertrend` bricht die
    # INDIKATORRECHNUNG auf einem leeren Rahmen ab. Im Betrieb faellt das
    # heute nicht auf, weil sie im `try` der Ladeschleife steht und der
    # `except Exception` dort das Symbol ueberspringt - der Lauf ueberlebt
    # also, aber aus Versehen und mit einer Meldung, die das Symptom nennt
    # statt der Ursache. Festgehalten, damit es nicht wieder unbemerkt
    # bleibt; repariert wird es NICHT, das waere eine eigene Freigabe.
    abbrecher = sorted(b for b, e in befunde.items()
                       if e["compute_indicators_leer"] not in
                       ("durchgelaufen", "keine solche Funktion"))
    check("die Indikatorrechnung bricht nur bei t3_supertrend ab - "
          "bekannt und eingefangen, kein neuer stiller Ausfall",
          abbrecher == ["t3_supertrend"], str(abbrecher))


def main():
    print("=" * 78)
    print("TB-45, Teil 4: ein leeres Symbol beendet keinen Lauf mehr")
    print("=" * 78)
    for test in (teil_1, teil_2, teil_3):
        try:
            test()
        except Exception as fehler:                            # noqa: BLE001
            import traceback
            FEHLER.append(f"{test.__name__} (Ausnahme)")
            print(f"  [FEHLER] {test.__name__} warf eine Ausnahme: {fehler}")
            traceback.print_exc()

    print("\n" + "=" * 78)
    gesamt = BESTANDEN + len(FEHLER)
    print(f"{BESTANDEN} von {gesamt} Pruefungen bestanden, {len(FEHLER)} fehlgeschlagen.")
    for name in FEHLER:
        print(f"  - {name}")
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())

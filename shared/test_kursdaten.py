"""
Selbsttests der Kurslücken-Absicherung
==============================================================================
Geprueft wird das VERHALTEN, nicht das Vorhandensein von Codestuecken.

Der Kern ist Abschnitt 3: der NaN-Fall wird ERZEUGT, indem ein echter
Bot-Loader einmal mit und einmal ohne die Absicherung laeuft - in getrennten
Prozessen, weil neun Bots gleichnamige Module haben. Beobachtet wird der
Ablauf (entsteht ein NaN-Trade? wird gezaehlt? wird gemeldet?), nicht ein von
Hand hergestelltes Ergebnis.

Abschnitt 5 zeigt, warum das ueberhaupt zaehlt: ein einziges NaN vergiftet in
simulate_portfolio jede FOLGENDE Kapitalzeile.

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.

Nutzung:  python3 shared/test_kursdaten.py
"""

import glob
import os
import subprocess
import sys
import tempfile

_SHARED = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED)
sys.path.insert(0, _SHARED)

import pandas as pd                                            # noqa: E402

import kursdaten                                               # noqa: E402

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


def rahmen(zeilen):
    """Ein Kursrahmen wie die CSVs des Projekts."""
    return pd.DataFrame(zeilen, columns=["open_time", "open", "high", "low",
                                          "close", "volume"])


NAN = float("nan")


# ---------------------------------------------------------------------------
def test_erkennung():
    print("\n1) Welche Kerzen als unvollstaendig gelten")
    df = rahmen([
        ["2026-01-01", 10.0, 11.0, 9.0, 10.5, 100],
        ["2026-01-02", NAN, NAN, NAN, NAN, 7650337],   # der APH-Fall
        ["2026-01-03", 10.0, 11.0, 9.0, 10.5, 100],
    ])
    maske = kursdaten.unvollstaendige_maske(df)
    check("die Kerze ohne Kurse wird erkannt", list(maske) == [False, True, False],
          list(maske))

    # Volumen fehlt, Kurse sind da: handelbar beschreibbar, also KEINE Luecke.
    df2 = rahmen([["2026-01-01", 10.0, 11.0, 9.0, 10.5, NAN]])
    check("fehlendes Volumen allein ist keine Luecke",
          not kursdaten.unvollstaendige_maske(df2).any())

    # Eine einzelne fehlende Kursspalte genuegt - Indikatoren brauchen alle vier.
    for spalte in ("open", "high", "low", "close"):
        df3 = rahmen([["2026-01-01", 10.0, 11.0, 9.0, 10.5, 100]])
        df3.loc[0, spalte] = NAN
        check(f"fehlendes '{spalte}' allein genuegt",
              bool(kursdaten.unvollstaendige_maske(df3).iloc[0]))

    leer = rahmen([])
    check("leerer Rahmen ergibt keine Ausnahme",
          len(kursdaten.unvollstaendige_maske(leer)) == 0)

    ohne_spalten = pd.DataFrame({"irgendwas": [1, 2]})
    check("ohne Kursspalten wird NICHTS gestrichen (lieber nichts als alles)",
          not kursdaten.unvollstaendige_maske(ohne_spalten).any())


def test_streichen_und_zaehlen():
    print("\n2) Streichen UND zaehlen - das Zaehlen ist der Punkt")
    df = rahmen([
        ["2026-01-01", 10.0, 11.0, 9.0, 10.5, 100],
        ["2026-01-02", NAN, NAN, NAN, NAN, 7650337],
        ["2026-01-03", 12.0, 13.0, 11.0, 12.5, 100],
        ["2026-01-04", NAN, 13.0, 11.0, 12.5, 100],
    ])
    sauber, anzahl = kursdaten.entferne_unvollstaendige(df, symbol="TEST", melden=False)
    check("beide Luecken gestrichen", len(sauber) == 2, len(sauber))
    check("und gezaehlt", anzahl == 2, anzahl)
    check("die verbliebenen Zeilen sind vollstaendig",
          not sauber[["open", "high", "low", "close"]].isna().any().any())
    check("der Index ist neu durchnummeriert", list(sauber.index) == [0, 1],
          list(sauber.index))

    unveraendert, null = kursdaten.entferne_unvollstaendige(
        rahmen([["2026-01-01", 1.0, 2.0, 0.5, 1.5, 10]]), melden=False)
    check("vollstaendige Daten: nichts gestrichen", null == 0)
    check("vollstaendige Daten: derselbe Rahmen", len(unveraendert) == 1)

    zaehler = kursdaten.Zaehler()
    check("ohne Befund gibt es keinen Bericht", zaehler.bericht() is None)
    zaehler.erfasse("APH", 1)
    zaehler.erfasse("SAUBER", 0)
    zaehler.erfasse("XYZ", 3)
    check("der Zaehler summiert", zaehler.gesamt == 4, zaehler.gesamt)
    bericht = zaehler.bericht()
    check("der Bericht nennt die Gesamtzahl", "4" in bericht, bericht)
    check("der Bericht nennt die betroffenen Symbole",
          "APH" in bericht and "XYZ" in bericht, bericht)
    check("der Bericht nennt KEIN Symbol ohne Befund", "SAUBER" not in bericht, bericht)
    check("der Bericht sagt, dass die Kerzen in keine Kennzahl eingehen",
          "KEINE Kennzahl" in bericht, bericht)


def test_echte_datei():
    print("\n3) Die echte Lücke im Repo wird gefunden")
    befunde = kursdaten.pruefe_ordner(os.path.join(BASE_DIR, "data"), "*_1d.csv")
    namen = {e["datei"] for e in befunde}
    check("APH_1d.csv wird als betroffen gemeldet", "APH_1d.csv" in namen, sorted(namen))
    aph = [e for e in befunde if e["datei"] == "APH_1d.csv"]
    if aph:
        check("genau eine unvollstaendige Kerze", aph[0]["anzahl"] == 1, aph[0]["anzahl"])
        check("es ist die LETZTE Kerze", aph[0]["letzte_betroffen"] is True)
    check("kein anderes Tages-Symbol ist betroffen", len(befunde) == 1,
          sorted(namen))


# ---------------------------------------------------------------------------
LADE_SKRIPT = r'''
import os, sys, itertools, inspect, json
sys.path.insert(0, os.getcwd())
import pandas as pd
import multi_symbol_optimise as mso

ABSICHERUNG = os.environ.get("ABSICHERUNG") == "1"
gemeldet = []
if not ABSICHERUNG:
    mso.entferne_unvollstaendige = lambda df, symbol=None, melden=True: (df, 0)

import io, contextlib
puffer = io.StringIO()
with contextlib.redirect_stdout(puffer):
    daten = mso.load_all_symbol_data()
ausgabe = puffer.getvalue()

eintrag = daten["APH"]
vorne = list(eintrag) if isinstance(eintrag, tuple) else [eintrag]
df = vorne[0]
sig = list(inspect.signature(mso.get_trades_for_symbol).parameters)
ranges = {n: list(getattr(mso, n))[:2] for n in dir(mso)
          if n.endswith("_RANGE") and isinstance(getattr(mso, n), (list, tuple))}
werte = [ranges[n] for n in ranges] or [[None]]
nan_trades = 0
for kombi in itertools.product(*werte):
    args = list(vorne) + [k for k in kombi if k is not None]
    try:
        t = mso.get_trades_for_symbol(*args[:len(sig)])
    except Exception:
        continue
    if t is not None and len(t) and "pnl_pct" in t:
        nan_trades += int(t["pnl_pct"].isna().sum())

print(json.dumps({
    "absicherung": ABSICHERUNG,
    "zeilen_aph": len(df),
    "letztes_datum": str(df["open_time"].max())[:10],
    "erstes_datum": str(df["open_time"].min())[:10],
    "nan_in_kursen": bool(df[["open", "high", "low", "close"]].isna().any().any()),
    "nan_trades": nan_trades,
    "meldung": "unvollstaendige Kerze" in ausgabe,
    "meldung_text": [z for z in ausgabe.splitlines() if "Datenqualitaet" in z][:1],
}))
'''


def _lade_lauf(bot, absicherung):
    umgebung = dict(os.environ, ABSICHERUNG="1" if absicherung else "0")
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as datei:
        datei.write(LADE_SKRIPT)
        pfad = datei.name
    try:
        lauf = subprocess.run([sys.executable, pfad],
                              cwd=os.path.join(BASE_DIR, "strategies", bot),
                              capture_output=True, text=True, timeout=900,
                              env=umgebung)
    finally:
        os.unlink(pfad)
    import json
    for zeile in reversed(lauf.stdout.splitlines()):
        if zeile.startswith("{"):
            return json.loads(zeile)
    raise RuntimeError(f"keine Ausgabe von {bot}: {lauf.stderr[-300:]}")


def test_am_echten_bot():
    print("\n4) Der NaN-Fall am echten Bot - erzeugt, nicht behauptet")
    bot = "elliott_wave_stocks"
    ohne = _lade_lauf(bot, absicherung=False)
    mit = _lade_lauf(bot, absicherung=True)

    check("OHNE Absicherung enthaelt APH noch die leere Kerze",
          ohne["nan_in_kursen"] is True, ohne)
    check("OHNE Absicherung entstehen NaN-Trades",
          ohne["nan_trades"] > 0, ohne["nan_trades"])
    check("MIT Absicherung ist keine leere Kerze mehr da",
          mit["nan_in_kursen"] is False, mit)
    check("MIT Absicherung entsteht KEIN NaN-Trade mehr",
          mit["nan_trades"] == 0, mit["nan_trades"])
    # Die Zeilenzahl bleibt GLEICH, und das ist kein Widerspruch: der
    # 10-Jahres-Filter (RECENT_YEARS_ONLY) richtet sein Fenster am LETZTEN
    # Datum aus. Faellt die leere Kerze weg, beginnt das Fenster einen Tag
    # frueher und nimmt vorn eine Zeile auf. Gemessen: hinten faellt
    # 2026-09-01 weg, vorn kommt 2016-08-31 hinzu, 2513 bleiben 2513.
    #
    # Genau deshalb prueft dieser Test das ENDE der Reihe und nicht die
    # Zeilenzahl - letztere haette hier nichts gezeigt.
    check("MIT Absicherung endet die Reihe eine Kerze frueher",
          mit["letztes_datum"] < ohne["letztes_datum"],
          f"{ohne['letztes_datum']} -> {mit['letztes_datum']}")
    check("dafuer beginnt das 10-Jahres-Fenster einen Tag frueher",
          mit["erstes_datum"] < ohne["erstes_datum"],
          f"{ohne['erstes_datum']} -> {mit['erstes_datum']}")
    check("die Zeilenzahl bleibt dadurch gleich - eine Zaehlung allein haette "
          "die Aenderung NICHT gezeigt",
          mit["zeilen_aph"] == ohne["zeilen_aph"],
          f"{ohne['zeilen_aph']} / {mit['zeilen_aph']}")
    check("die Streichung wird GEMELDET, nicht stillschweigend vorgenommen",
          mit["meldung"] is True, mit.get("meldung_text"))
    check("die Meldung nennt das Symbol",
          any("APH" in z for z in mit.get("meldung_text", [])),
          mit.get("meldung_text"))
    check("OHNE Absicherung gibt es KEINE solche Meldung",
          ohne["meldung"] is False, ohne.get("meldung_text"))


GEGENPROBE_SKRIPT = r'''
import os, sys, itertools, inspect, json, hashlib
sys.path.insert(0, os.getcwd())
import pandas as pd
import multi_symbol_optimise as mso

if os.environ.get("ABSICHERUNG") != "1":
    mso.entferne_unvollstaendige = lambda df, symbol=None, melden=True: (df, 0)

import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    daten = mso.load_all_symbol_data()

# Ein Symbol OHNE Luecke - hier darf sich nichts aendern.
name = os.environ.get("SYMBOL", "AAPL")
eintrag = daten[name]
vorne = list(eintrag) if isinstance(eintrag, tuple) else [eintrag]
sig = list(inspect.signature(mso.get_trades_for_symbol).parameters)
ranges = {n: list(getattr(mso, n))[:2] for n in dir(mso)
          if n.endswith("_RANGE") and isinstance(getattr(mso, n), (list, tuple))}
werte = [ranges[n] for n in ranges] or [[None]]
fingerabdruecke = []
for kombi in itertools.product(*werte):
    args = list(vorne) + [k for k in kombi if k is not None]
    try:
        t = mso.get_trades_for_symbol(*args[:len(sig)])
    except Exception:
        fingerabdruecke.append("fehler")
        continue
    if t is None or len(t) == 0:
        fingerabdruecke.append("leer")
        continue
    roh = t[["entry_time", "exit_time", "pnl_pct"]].to_csv(index=False)
    fingerabdruecke.append(hashlib.sha256(roh.encode()).hexdigest()[:16])
print(json.dumps({"symbol": name, "zeilen": len(vorne[0]),
                  "fingerabdruecke": fingerabdruecke}))
'''


def _gegenprobe(bot, symbol, absicherung):
    umgebung = dict(os.environ, ABSICHERUNG="1" if absicherung else "0", SYMBOL=symbol)
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as datei:
        datei.write(GEGENPROBE_SKRIPT)
        pfad = datei.name
    try:
        lauf = subprocess.run([sys.executable, pfad],
                              cwd=os.path.join(BASE_DIR, "strategies", bot),
                              capture_output=True, text=True, timeout=900,
                              env=umgebung)
    finally:
        os.unlink(pfad)
    import json
    for zeile in reversed(lauf.stdout.splitlines()):
        if zeile.startswith("{"):
            return json.loads(zeile)
    raise RuntimeError(f"keine Ausgabe: {lauf.stderr[-300:]}")


def test_gegenprobe():
    print("\n5) Gegenprobe: bei vollstaendigen Daten aendert sich NICHTS")
    bot = "elliott_wave_stocks"
    ohne = _gegenprobe(bot, "AAPL", absicherung=False)
    mit = _gegenprobe(bot, "AAPL", absicherung=True)
    check("AAPL behaelt genau gleich viele Zeilen",
          mit["zeilen"] == ohne["zeilen"], f"{ohne['zeilen']} / {mit['zeilen']}")
    check("die Trades sind ueber alle Kombinationen identisch",
          mit["fingerabdruecke"] == ohne["fingerabdruecke"],
          f"{sum(1 for a, b in zip(mit['fingerabdruecke'], ohne['fingerabdruecke']) if a != b)} Abweichungen")
    check("es wurden ueberhaupt Trades erzeugt (sonst prueft der Vergleich nichts)",
          any(f not in ("leer", "fehler") for f in mit["fingerabdruecke"]),
          mit["fingerabdruecke"][:3])


VERGIFTUNG_SKRIPT = r'''
import os, sys, json
sys.path.insert(0, os.getcwd())
import pandas as pd
import equity_simulation as es

trades = pd.DataFrame({
    "symbol": ["A", "B", "C"],
    "entry_time": pd.to_datetime(["2026-01-01", "2026-02-01", "2026-03-01"]),
    "exit_time": pd.to_datetime(["2026-01-10", "2026-02-10", "2026-03-10"]),
    "pnl_pct": [10.0, float("nan"), 10.0],
})
erg = es.simulate_portfolio(trades, 10_000.0, 0.10, None)
kurve = erg["equity_curve"]
sauber = es.simulate_portfolio(trades[trades["pnl_pct"].notna()], 10_000.0, 0.10, None)
print(json.dumps({
    "endkapital_mit_nan": None if pd.isna(erg["final_capital"]) else erg["final_capital"],
    "kapitalzeilen_nan": int(kurve["capital_after"].isna().sum()),
    "kapitalzeilen": len(kurve),
    "num_executed": erg["num_executed"],
    "endkapital_ohne_nan": sauber["final_capital"],
}))
'''


def test_vergiftung():
    print("\n6) Warum das zaehlt: ein NaN vergiftet ALLES danach")
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as datei:
        datei.write(VERGIFTUNG_SKRIPT)
        pfad = datei.name
    try:
        lauf = subprocess.run([sys.executable, pfad],
                              cwd=os.path.join(BASE_DIR, "strategies", "elliott_wave_stocks"),
                              capture_output=True, text=True, timeout=300)
    finally:
        os.unlink(pfad)
    import json
    daten = None
    for zeile in reversed(lauf.stdout.splitlines()):
        if zeile.startswith("{"):
            daten = json.loads(zeile)
            break
    if daten is None:
        check("simulate_portfolio liess sich aufrufen", False, lauf.stderr[-200:])
        return
    check("ein NaN in der Mitte macht das Endkapital unbrauchbar",
          daten["endkapital_mit_nan"] is None, daten["endkapital_mit_nan"])
    check("und ALLE Kapitalzeilen ab dem NaN sind betroffen",
          daten["kapitalzeilen_nan"] == 2 and daten["kapitalzeilen"] == 3,
          f"{daten['kapitalzeilen_nan']} von {daten['kapitalzeilen']}")
    check("der kaputte Trade zaehlt trotzdem als ausgefuehrt",
          daten["num_executed"] == 3, daten["num_executed"])
    check("ohne den kaputten Trade ist das Endkapital eine Zahl",
          isinstance(daten["endkapital_ohne_nan"], (int, float))
          and daten["endkapital_ohne_nan"] > 0, daten["endkapital_ohne_nan"])


def test_mittelwerte_verstecken():
    print("\n7) Wo ein NaN unbemerkt verschwindet")
    pnl = pd.Series([5.0, NAN, -2.0, 8.0])
    check("pandas .mean() uebergeht NaN stillschweigend",
          abs(pnl.mean() - 3.6666666) < 1e-4, pnl.mean())
    check("pandas .sum() ebenso", abs(pnl.sum() - 11.0) < 1e-9, pnl.sum())
    check("(pnl > 0) zaehlt ein NaN als VERLIERER - schlimmer als Ueberspringen",
          list(pnl > 0) == [True, False, False, True], list(pnl > 0))
    mit = (pnl > 0).mean() * 100
    ohne = (pnl.dropna() > 0).mean() * 100
    check("die Trefferquote sinkt dadurch messbar",
          round(mit, 1) == 50.0 and round(ohne, 1) == 66.7, f"{mit:.1f} % statt {ohne:.1f} %")


def test_verbreitung():
    print("\n8) Die Absicherung sitzt ueberall, wo Kursdaten hereinkommen")
    holer = sorted(glob.glob(os.path.join(BASE_DIR, "strategies", "*", "fetch_stock_data.py")))
    check("vier Aktien-Bots holen Kursdaten", len(holer) == 4, len(holer))
    inhalte = set()
    for pfad in holer:
        with open(pfad, "r", encoding="utf-8") as datei:
            text = datei.read()
        inhalte.add(text)
        check(f"{os.path.basename(os.path.dirname(pfad))}: Holer abgesichert",
              "entferne_unvollstaendige" in text)
    check("die vier Holer sind weiterhin identisch", len(inhalte) == 1,
          f"{len(inhalte)} verschiedene Fassungen")

    lader = sorted(glob.glob(os.path.join(BASE_DIR, "strategies", "*",
                                          "multi_symbol_optimise.py")))
    check("neun Bots laden Kursdaten aus CSVs", len(lader) == 9, len(lader))
    for pfad in lader:
        with open(pfad, "r", encoding="utf-8") as datei:
            text = datei.read()
        name = os.path.basename(os.path.dirname(pfad))
        check(f"{name}: Lader abgesichert", "entferne_unvollstaendige" in text)
        check(f"{name}: meldet die Gesamtzahl", "_luecken.melde()" in text)

    # Die verbotenen Dateien bleiben unberuehrt - gegen origin/main geprueft,
    # nicht gegen ein Gedaechtnis.
    lauf = subprocess.run(["git", "diff", "--name-only", "origin/main"],
                          cwd=BASE_DIR, capture_output=True, text=True)
    geaendert = [z for z in lauf.stdout.splitlines() if z.strip()]
    for verboten in ("live_params.py", "forward_test.py", "equity_simulation.py"):
        betroffen = [z for z in geaendert if z.endswith(verboten)]
        check(f"keine {verboten} veraendert", not betroffen, betroffen)
    check("nichts unter broker/ veraendert",
          not [z for z in geaendert if z.startswith("broker/")],
          [z for z in geaendert if z.startswith("broker/")])
    check("keine Kursdatei im Repo veraendert",
          not [z for z in geaendert if z.startswith("data/")],
          [z for z in geaendert if z.startswith("data/")])


HOLER_SKRIPT = r'''
"""Prueft fetch_historical_data am VERHALTEN: yfinance wird durch eine
Attrappe ersetzt, die genau den APH-Fall liefert (Datum und Volumen da,
OHLC leer)."""
import os, sys, json
sys.path.insert(0, os.getcwd())
import pandas as pd
import yfinance as yf

def attrappe(ticker, period=None, interval=None, progress=False, auto_adjust=True):
    # Der Index heisst bei yfinance "Date" - fetch_historical_data benennt
    # genau diese Spalte nach reset_index() um.
    index = pd.to_datetime(["2026-08-30", "2026-08-31", "2026-09-01"])
    index.name = "Date"
    return pd.DataFrame({
        "Open":   [10.0, 11.0, float("nan")],
        "High":   [10.5, 11.5, float("nan")],
        "Low":    [ 9.5, 10.5, float("nan")],
        "Close":  [10.2, 11.2, float("nan")],
        "Volume": [1000, 1100, 7650337],
    }, index=index)

yf.download = attrappe
import fetch_stock_data as fsd
df = fsd.fetch_historical_data("APH")
print(json.dumps({
    "zeilen": len(df),
    "nan_in_kursen": bool(df[["open", "high", "low", "close"]].isna().any().any()),
    "letztes_datum": str(df["open_time"].max())[:10],
}))
'''


def test_holer_am_verhalten():
    print("\n9) Der Holer - am Verhalten geprueft, nicht an der Textsuche")
    # Wichtig: die Textsuche in Abschnitt 8 bliebe gruen, wenn der Aufruf da
    # steht, sein Ergebnis aber verworfen wird. Hier laeuft die Funktion
    # wirklich, mit einer yfinance-Attrappe, die genau den APH-Fall liefert.
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as datei:
        datei.write(HOLER_SKRIPT)
        pfad = datei.name
    try:
        lauf = subprocess.run(
            [sys.executable, pfad],
            cwd=os.path.join(BASE_DIR, "strategies", "elliott_wave_stocks"),
            capture_output=True, text=True, timeout=300)
    finally:
        os.unlink(pfad)
    import json
    daten = None
    for zeile in reversed(lauf.stdout.splitlines()):
        if zeile.startswith("{"):
            daten = json.loads(zeile)
            break
    if daten is None:
        check("fetch_historical_data liess sich aufrufen", False,
              lauf.stderr[-300:] or lauf.stdout[-200:])
        return
    check("der Holer gibt nur die zwei vollstaendigen Kerzen zurueck",
          daten["zeilen"] == 2, daten["zeilen"])
    check("keine leeren Kurse mehr im Ergebnis",
          daten["nan_in_kursen"] is False, daten)
    check("die letzte gelieferte Kerze ist die letzte VOLLSTAENDIGE",
          daten["letztes_datum"] == "2026-08-31", daten["letztes_datum"])


def test_werkzeug():
    print("\n10) Das Pruefwerkzeug")
    lauf = subprocess.run([sys.executable, os.path.join(_SHARED, "kursdaten.py")],
                          capture_output=True, text=True, timeout=300)
    check("das Werkzeug meldet den Befund", "APH_1d.csv" in lauf.stdout, lauf.stdout[:200])
    check("es nennt, dass die LETZTE Kerze betroffen ist",
          "LETZTE Kerze" in lauf.stdout)
    check("Rueckgabewert 1 bei Befund - damit ein Cronjob es sieht",
          lauf.returncode == 1, lauf.returncode)

    leer = tempfile.mkdtemp(prefix="kursdaten_leer_")
    try:
        sauber = pd.DataFrame({"open_time": ["2026-01-01"], "open": [1.0],
                               "high": [2.0], "low": [0.5], "close": [1.5],
                               "volume": [10]})
        sauber.to_csv(os.path.join(leer, "SAUBER_1d.csv"), index=False)
        lauf = subprocess.run([sys.executable, os.path.join(_SHARED, "kursdaten.py"),
                               "--ordner", leer],
                              capture_output=True, text=True, timeout=300)
        check("ohne Befund: Rueckgabewert 0", lauf.returncode == 0, lauf.returncode)
        check("ohne Befund: sagt es ausdruecklich",
              "Keine unvollstaendigen" in lauf.stdout, lauf.stdout[:200])
    finally:
        import shutil
        shutil.rmtree(leer, ignore_errors=True)


def main():
    print("=" * 78)
    print("Selbsttests der Kurslücken-Absicherung")
    print("=" * 78)
    tests = [test_erkennung, test_streichen_und_zaehlen, test_echte_datei,
             test_am_echten_bot, test_gegenprobe, test_vergiftung,
             test_mittelwerte_verstecken, test_verbreitung,
             test_holer_am_verhalten, test_werkzeug]
    for test in tests:
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

"""
Welcher Bot hat eine stetige Signalstaerke? (TB-26, Schritt 1)
==============================================================================
    python3 research/zuteilungskaskade/messung_primaerschluessel.py
    python3 research/zuteilungskaskade/messung_primaerschluessel.py --bot rsi2_crypto
    python3 research/zuteilungskaskade/messung_primaerschluessel.py --json bericht.json

DIE FRAGE
------------------------------------------------------------------------------
Stufe 1 der Zuteilungskaskade (`shared/zuteilung.py`) ist die strategieeigene,
STETIGE Signalstaerke - falls der Bot eine fuehrt. Welche das je Bot ist,
steht als `SIGNALSPALTE` in dessen `equity_simulation.py`. Dieses Programm
liefert die Messung, auf der diese neun Entscheidungen beruhen, und macht sie
wiederholbar.

Gemessen wird je Zusatzspalte der Trade-Tabelle:

* wie viele VERSCHIEDENE Werte sie annimmt,
* wie viele Trades sich einen Einstiegszeitpunkt mit mindestens einem anderen
  teilen (nur dort kann ueberhaupt zugeteilt werden),
* und wie viele davon nach einer Rangregel auf dieser Spalte **weiterhin
  gleichauf** liegen.

Der letzte Wert ist Eigenschaft 2 der Pruefliste aus TB-26: hoechstens 2 %
Gleichstaende. Eine Spalte, die daran scheitert, taugt nicht als
Primaerschluessel - sie verschoebe die Willkuer nur eine Stufe weiter.

WAS DIESES PROGRAMM NICHT TUT
------------------------------------------------------------------------------
* Es fasst keinen Bot-Code an und aendert keinen Parameter.
* Es schreibt nicht nach `results/`: `RESULTS_DIR` zeigt waehrend der Laeufe
  in einen temporaeren Ordner - dieselbe Absicherung wie in
  `shared/kurven_lauf.py` und `shared/determinismus_lauf.py`.
* Es entscheidet NICHT ueber die Richtung (aufsteigend/absteigend). Die kommt
  aus der Strategielogik und nicht aus dem Backtest-Ergebnis; sie danach zu
  waehlen waere eine Anpassung an die Stichprobe. Die Richtung steht mit
  Begruendung bei der jeweiligen `SIGNALSPALTE`.

Der Befund vom 13.09.2026 steht in `BERICHT.md`.
"""

import argparse
import contextlib
import io
import json
import os
import runpy
import sys
import tempfile
import types

import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_HIER))
STRATEGIES_DIR = os.path.join(BASE_DIR, "strategies")

# Spalten, die JEDE Trade-Tabelle fuehrt oder die keine Signalstaerke sein
# koennen - sie stehen fuer Zeit, Preis und Ergebnis, nicht fuer die Guete des
# Signals. `pnl_pct` waere ausserdem ein Blick in die Zukunft.
KEINE_KANDIDATEN = {
    "symbol", "entry_time", "exit_time", "signal_time", "entry_price",
    "exit_price", "pnl_pct", "pnl_pct_gross", "result", "direction",
    "holding_days",
}

# Eigenschaft 2 der Pruefliste: hoechstens so viel Prozent Gleichstaende.
SCHWELLE_PCT = 2.0


def _stubs():
    fake = types.ModuleType("fetch_binance_data")
    fake.fetch_historical_data = lambda *a, **k: pd.DataFrame()
    sys.modules.setdefault("fetch_binance_data", fake)
    fb = types.ModuleType("binance")
    fc = types.ModuleType("binance.client")

    class _Client:
        KLINE_INTERVAL_1HOUR = "1h"
        KLINE_INTERVAL_4HOUR = "4h"
        KLINE_INTERVAL_1DAY = "1d"

    fc.Client = _Client
    fb.client = fc
    sys.modules.setdefault("binance", fb)
    sys.modules.setdefault("binance.client", fc)
    fy = types.ModuleType("yfinance")
    fy.download = lambda *a, **k: pd.DataFrame()
    fy.Ticker = lambda *a, **k: None
    sys.modules.setdefault("yfinance", fy)


def trades_eines_bots(bot: str) -> pd.DataFrame:
    """Die Trade-Tabelle so, wie der Bot sie tatsaechlich in die Zuteilung
    gibt - also NACH allen Filtern des `__main__`-Blocks (bei
    `volatility_breakout_crypto` etwa nach dem BTC-Regimefilter).

    Deshalb `runpy` auf den `__main__`-Block und nicht ein eigener Aufruf von
    `collect_all_trades()`: dieselbe Begruendung wie in
    `shared/determinismus_lauf.py`."""
    sdir = os.path.join(STRATEGIES_DIR, bot)
    shared = os.path.join(BASE_DIR, "shared")
    sys.path.insert(0, shared)
    sys.path.insert(0, sdir)
    os.chdir(sdir)
    _stubs()

    tmp = tempfile.mkdtemp()
    import strategy_paths as echt
    ersatz = types.ModuleType("strategy_paths")

    def get_strategy_paths(caller_file):
        pfade = echt.get_strategy_paths(caller_file)
        pfade["RESULTS_DIR"] = tmp
        os.makedirs(tmp, exist_ok=True)
        return pfade

    ersatz.get_strategy_paths = get_strategy_paths
    sys.modules["strategy_paths"] = ersatz

    with contextlib.redirect_stdout(io.StringIO()):
        globalen = runpy.run_path(os.path.join(sdir, "equity_simulation.py"),
                                  run_name="__main__")
    return globalen["trades"]


def messe(trades: pd.DataFrame) -> dict:
    gruppen = trades.groupby("entry_time").size()
    gleichzeitig = trades[trades["entry_time"].isin(gruppen[gruppen > 1].index)]

    spalten = []
    for name in trades.columns:
        if name in KEINE_KANDIDATEN or not pd.api.types.is_numeric_dtype(trades[name]):
            continue
        werte = trades[name].dropna()
        gleichauf = 0
        for _, gruppe in gleichzeitig.groupby("entry_time"):
            haeufigkeit = gruppe[name].value_counts()
            gleichauf += int(haeufigkeit[haeufigkeit > 1].sum())
        anteil = (100.0 * gleichauf / len(gleichzeitig)) if len(gleichzeitig) else 0.0
        spalten.append({
            "spalte": name,
            "verschiedene_werte": int(werte.nunique()),
            "min": None if werte.empty else float(werte.min()),
            "max": None if werte.empty else float(werte.max()),
            "gleichauf": gleichauf,
            "gleichauf_pct": round(anteil, 1),
            "erfuellt_eigenschaft_2": anteil <= SCHWELLE_PCT,
        })

    return {
        "trades": len(trades),
        "gleichzeitig": len(gleichzeitig),
        "gleichzeitig_pct": round(100.0 * len(gleichzeitig) / len(trades), 1) if len(trades) else 0.0,
        "kandidaten": spalten,
    }


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(description="Misst die Kandidaten fuer "
                                                   "Stufe 1 der Zuteilungskaskade.")
    zerleger.add_argument("--bot", action="append", default=None)
    zerleger.add_argument("--json", metavar="PFAD", default=None)
    args = zerleger.parse_args(argv)

    bots = args.bot or sorted(
        n for n in os.listdir(STRATEGIES_DIR)
        if os.path.exists(os.path.join(STRATEGIES_DIR, n, "equity_simulation.py")))

    # Ein Unterprozess je Bot: neun gleichnamige `equity_simulation.py` und
    # `live_params.py` kollidieren in `sys.modules` - derselbe stille Bug, den
    # `shared/portfolio_overview.py` schon einmal gefunden hat.
    if os.environ.get("_TB26_KIND"):
        bericht = messe(trades_eines_bots(bots[0]))
        print("__MESSUNG__" + json.dumps(bericht))
        return 0

    import subprocess
    gesamt = {}
    print(f"{'Bot':<28} {'Trades':>7} {'gleichz.':>9}  Kandidatenspalten")
    print("-" * 100)
    for bot in bots:
        umgebung = dict(os.environ, _TB26_KIND="1")
        lauf = subprocess.run([sys.executable, os.path.abspath(__file__), "--bot", bot],
                              capture_output=True, text=True, env=umgebung, cwd=BASE_DIR)
        zeile = next((z for z in lauf.stdout.splitlines()
                      if z.startswith("__MESSUNG__")), None)
        if zeile is None:
            print(f"{bot:<28} FEHLER: {(lauf.stderr.strip() or '-')[-200:]}")
            gesamt[bot] = {"fehler": lauf.stderr.strip()[-500:]}
            continue
        bericht = json.loads(zeile[len("__MESSUNG__"):])
        gesamt[bot] = bericht
        if not bericht["kandidaten"]:
            beschreibung = "keine - Kaskade beginnt bei Stufe 2"
        else:
            beschreibung = "; ".join(
                f"{k['spalte']}: {k['verschiedene_werte']} Werte, "
                f"{k['gleichauf_pct']:.1f} % gleichauf "
                f"({'Eig. 2 erfuellt' if k['erfuellt_eigenschaft_2'] else 'Eig. 2 verfehlt'})"
                for k in bericht["kandidaten"])
        print(f"{bot:<28} {bericht['trades']:>7} "
              f"{bericht['gleichzeitig_pct']:>8.1f}%  {beschreibung}")
    print("-" * 100)
    print(f"Eigenschaft 2: hoechstens {SCHWELLE_PCT:.0f} % Gleichstaende unter den "
          f"gleichzeitigen Trades.")
    print("Die Richtung (aufsteigend/absteigend) entscheidet dieses Programm NICHT - "
          "sie kommt aus der Strategielogik.")
    print("Und es entscheidet auch nicht ueber Eigenschaft 1 und 3 der Pruefliste:")
    print("  1 - drueckt die Spalte ueberhaupt eine SIGNALSTAERKE aus? `setup_day_low`")
    print("      etwa erfuellt Eigenschaft 2 muehelos und ist trotzdem keine: es ist ein")
    print("      Kursniveau.")
    print("  3 - ist sie skalenfrei? Ein Kursniveau ist es nicht - eine Rangregel darauf")
    print("      sortierte nach Notierungshoehe.")
    print("Diese beiden Fragen beantwortet der Mensch, und die Antwort steht je Bot bei")
    print("der SIGNALSPALTE in dessen equity_simulation.py.")

    if args.json:
        with open(args.json, "w") as datei:
            json.dump(gesamt, datei, indent=2, default=str)
        print(f"Bericht: {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

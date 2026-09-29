#!/usr/bin/env python3
"""
Wertprobe zu TB-30b Posten 3 (Register 11.3, TB-122 C2): `sma_trend_filter`
==============================================================================
Kommt ein Rasterwert der Achse `sma_trend_filter`, der NICHT die
Voreinstellung ist, wirklich bis in die Indikatorberechnung?

Geprueft per Spion (Monkeypatch auf `multi_symbol_optimise.compute_indicators`
und `.run_backtest`), nicht ueber eine Kennzahl. Die Kursreihe ist
synthetisch; es wird keine Datei aus data/ gelesen und nichts geschrieben.

Der Probewert ist die ERSTE Stufe der Achse aus `registerdaten.raster()`
(Register Abschnitt 3) - er steht hier nicht als Zahl.

Teil A  Signalpfad: equity_simulation.collect_all_trades(..., sma_trend_period=<Stufe>)
        -> compute_indicators und run_backtest erhalten genau diesen Wert, und
        die Spalte `sma_trend` ist der SMA dieser Laenge.
Teil B  Ohne Argument kommt die Voreinstellung SMA_TREND_PERIOD an; jede neue
        Voreinstellung ist genau dieser Wert.
Teil C  Optimierer-Pfad: get_trades_for_symbol(..., sma_trend_period=<Stufe>).
Teil D  run_backtest beginnt den Scan bei sma_trend_period (konstruierter Fall:
        ein Signal nach der Stufe, aber vor der Voreinstellung).

Gegenprobe (Register 40.7): am Stand vor TB-122 B scheitert diese Probe
(collect_all_trades und get_trades_for_symbol kennen das Argument nicht).
"""

import inspect
import os
import sys

import numpy as np
import pandas as pd

_HIER = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HIER))
sys.path[:0] = [_HIER, os.path.join(_REPO, "shared")]
sys.path.append(os.path.join(_REPO, "research", "vorregistrierung"))

import backtest_rsi2 as bt            # noqa: E402
import multi_symbol_optimise as mo    # noqa: E402
import equity_simulation as es        # noqa: E402
import registerdaten                  # noqa: E402

BOT = "rsi2_mean_reversion"
ACHSE = "sma_trend_filter"

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")


def kurse(n=400):
    rng = np.random.RandomState(20260929)
    close = 100 * np.cumprod(1 + rng.normal(0, 0.01, n))
    return pd.DataFrame({
        "open_time": pd.date_range("2020-01-01", periods=n, freq="D"),
        "open": close, "high": close * 1.01, "low": close * 0.99,
        "close": close, "volume": 1e6,
    })


def gleich(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    return a.shape == b.shape and bool(np.all((a == b) | (np.isnan(a) & np.isnan(b))))


class Spion:
    """Ersetzt compute_indicators und run_backtest in multi_symbol_optimise und
    merkt sich, welchen Achsenwert sie bekommen haben."""

    def __init__(self):
        self.ci, self.rb = [], []
        self._ci, self._rb = mo.compute_indicators, mo.run_backtest

    def __enter__(self):
        def ci(*args, **kwargs):
            b = inspect.signature(self._ci).bind(*args, **kwargs)
            b.apply_defaults()
            self.ci.append(b.arguments.get("sma_trend_period"))
            return self._ci(*args, **kwargs)

        def rb(*args, **kwargs):
            b = inspect.signature(self._rb).bind(*args, **kwargs)
            b.apply_defaults()
            self.rb.append((b.arguments.get("sma_trend_period"), b.arguments["price_df"]))
            return self._rb(*args, **kwargs)

        mo.compute_indicators, mo.run_backtest = ci, rb
        return self

    def __exit__(self, *a):
        mo.compute_indicators, mo.run_backtest = self._ci, self._rb


def main():
    stufe = registerdaten.raster()[BOT][ACHSE][0]
    voreinstellung = bt.SMA_TREND_PERIOD
    print(f"{BOT}: Achse {ACHSE}, erste Stufe {stufe}, Voreinstellung {voreinstellung}")
    pruefe("0: erste Stufe ist nicht die Voreinstellung", stufe != voreinstellung)

    df = kurse()
    all_data = {"SYN": (bt.compute_indicators(df), None)}   # Gestalt wie load_all_symbol_data()

    # --- Teil A: Signalpfad ---------------------------------------------------
    with Spion() as s:
        try:
            es.collect_all_trades(all_data, 5.0, None, sma_trend_period=stufe)
            ok, fehler = True, ""
        except TypeError as e:
            ok, fehler = False, str(e)
    pruefe("A0: collect_all_trades nimmt sma_trend_period", ok, fehler)
    pruefe("A1: compute_indicators erhaelt die Stufe", ok and s.ci and all(v == stufe for v in s.ci), str(s.ci))
    pruefe("A2: run_backtest erhaelt die Stufe", ok and s.rb and all(v == stufe for v, _ in s.rb),
           str([v for v, _ in s.rb]))
    pruefe("A3: sma_trend ist der SMA der Stufe",
           ok and s.rb and all(gleich(d["sma_trend"], bt.sma(d["close"], stufe)) for _, d in s.rb))

    # --- Teil B: Voreinstellung ----------------------------------------------
    with Spion() as s:
        es.collect_all_trades(all_data, 5.0, None)
    pruefe("B1: ohne Argument erhaelt compute_indicators die Voreinstellung",
           bool(s.ci) and all(v == voreinstellung for v in s.ci), str(s.ci))
    pruefe("B2: ohne Argument erhaelt run_backtest die Voreinstellung",
           bool(s.rb) and all(v == voreinstellung for v, _ in s.rb), str([v for v, _ in s.rb]))
    for name, f in (("equity_simulation.collect_all_trades", es.collect_all_trades),
                    ("multi_symbol_optimise.get_trades_for_symbol", mo.get_trades_for_symbol),
                    ("backtest_rsi2.compute_indicators", bt.compute_indicators),
                    ("backtest_rsi2.run_backtest", bt.run_backtest)):
        p = inspect.signature(f).parameters.get("sma_trend_period")
        pruefe(f"B3: {name} hat sma_trend_period mit Voreinstellung {voreinstellung}",
               p is not None and p.default == voreinstellung, str(p))

    # --- Teil C: Optimierer-Pfad ---------------------------------------------
    df_ind, cutoff = all_data["SYN"]
    with Spion() as s:
        try:
            mo.get_trades_for_symbol(df_ind, cutoff, 5.0, None, sma_trend_period=stufe)
            ok, fehler = True, ""
        except TypeError as e:
            ok, fehler = False, str(e)
    pruefe("C1: get_trades_for_symbol nimmt sma_trend_period", ok, fehler)
    pruefe("C2: compute_indicators erhaelt die Stufe", ok and s.ci == [stufe], str(s.ci))
    pruefe("C3: run_backtest erhaelt die Stufe", ok and [v for v, _ in s.rb] == [stufe],
           str([v for v, _ in s.rb]))

    # --- Teil D: Scanbeginn ----------------------------------------------------
    n, i = stufe + 40, stufe + 4
    d = pd.DataFrame({
        "open_time": pd.date_range("2020-01-01", periods=n, freq="D"),
        "close": 100.0, "low": 99.0, "sma_trend": 200.0, "sma_exit": 1000.0, "rsi": 50.0,
    })
    d.loc[i, ["close", "sma_trend", "rsi"]] = [110.0, 100.0, 1.0]     # Signal an Balken i
    d.loc[i + 1, ["close", "sma_exit"]] = [120.0, 100.0]               # SMA-Ausstieg am Folgebalken
    try:
        mit = bt.run_backtest(d, rsi_threshold=5.0, sma_trend_period=stufe)
        ok, fehler = True, ""
    except TypeError as e:
        mit, ok, fehler = None, False, str(e)
    ohne = bt.run_backtest(d, rsi_threshold=5.0)
    pruefe("D1: mit der Stufe findet der Scan das Signal nach der Stufe", ok and len(mit) == 1, fehler)
    pruefe("D2: mit der Voreinstellung beginnt der Scan dahinter", len(ohne) == 0)

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

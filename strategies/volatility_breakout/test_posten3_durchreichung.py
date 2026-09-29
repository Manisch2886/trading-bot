#!/usr/bin/env python3
"""
Wertprobe zu TB-30b Posten 3 (Register 11.3, TB-122 C2): `bb_lookback`, `bb_squeeze_percentile`
==============================================================================
Kommen Rasterwerte der Achsen `bb_lookback` und `bb_squeeze_percentile`, die
NICHT die Voreinstellung sind, wirklich bis in die Indikatorberechnung?

Geprueft per Spion (Monkeypatch auf `multi_symbol_optimise.compute_indicators`
und `.run_backtest`), nicht ueber eine Kennzahl. Die Kursreihe ist
synthetisch; es wird keine Datei aus data/ gelesen und nichts geschrieben.

Die Probewerte sind die ERSTEN Stufen der Achsen aus `registerdaten.raster()`
(Register Abschnitt 3) - sie stehen hier nicht als Zahl.

Teil A  Signalpfad: equity_simulation.collect_all_trades(..., squeeze_lookback_days=<Stufe>,
        squeeze_percentile=<Stufe>) -> compute_indicators erhaelt genau diese
        Werte, und die Spalte `squeeze_thresh`, die run_backtest bekommt, ist
        das Quantil mit diesen Werten.
Teil B  Ohne Argument kommen die Voreinstellungen aus live_params.py an; jede
        neue Voreinstellung ist genau dieser Wert.
Teil C  Optimierer-Pfad: get_trades_for_symbol(..., <Stufen>).

Nicht Gegenstand: `backtest_breakout.WARMUP_PERIOD` (Scanbeginn) haengt weiter
an der Voreinstellung - Befund im Ergebnis von TB-122, die Datei liegt
ausserhalb des Auftrags.

Gegenprobe (Register 40.7): am Stand vor TB-122 B scheitert diese Probe
(collect_all_trades und get_trades_for_symbol kennen die Argumente nicht).
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

import backtest_breakout as bt        # noqa: E402
import multi_symbol_optimise as mo    # noqa: E402
import equity_simulation as es        # noqa: E402
import live_params as lp              # noqa: E402
import registerdaten                  # noqa: E402

BOT = "volatility_breakout"

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")


def kurse(n=600):
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
    merkt sich, welche Achsenwerte ankommen."""

    def __init__(self):
        self.ci, self.rb = [], []
        self._ci, self._rb = mo.compute_indicators, mo.run_backtest

    def __enter__(self):
        def ci(*args, **kwargs):
            b = inspect.signature(self._ci).bind(*args, **kwargs)
            b.apply_defaults()
            self.ci.append((b.arguments.get("squeeze_lookback_days"), b.arguments.get("squeeze_percentile")))
            return self._ci(*args, **kwargs)

        def rb(*args, **kwargs):
            b = inspect.signature(self._rb).bind(*args, **kwargs)
            self.rb.append(b.arguments["price_df"])
            return self._rb(*args, **kwargs)

        mo.compute_indicators, mo.run_backtest = ci, rb
        return self

    def __exit__(self, *a):
        mo.compute_indicators, mo.run_backtest = self._ci, self._rb


def main():
    r = registerdaten.raster()[BOT]
    lb, pc = r["bb_lookback"][0], r["bb_squeeze_percentile"][0]
    vor = (lp.BB_LOOKBACK, lp.BB_SQUEEZE_PERCENTILE)
    print(f"{BOT}: erste Stufen bb_lookback {lb}, bb_squeeze_percentile {pc}; Voreinstellungen {vor}")
    pruefe("0: erste Stufen sind nicht die Voreinstellungen", lb != vor[0] and pc != vor[1])

    df = kurse()
    all_data = {"SYN": (bt.compute_indicators(df), None)}   # Gestalt wie load_all_symbol_data()

    def erwartet(d, l, p):
        return bt.squeeze_threshold(d["bb_width"], l, p)

    # --- Teil A: Signalpfad ---------------------------------------------------
    with Spion() as s:
        try:
            es.collect_all_trades(all_data, 8.0, squeeze_lookback_days=lb, squeeze_percentile=pc)
            ok, fehler = True, ""
        except TypeError as e:
            ok, fehler = False, str(e)
    pruefe("A0: collect_all_trades nimmt beide Achsen", ok, fehler)
    pruefe("A1: compute_indicators erhaelt die Stufen", ok and s.ci and all(v == (lb, pc) for v in s.ci), str(s.ci))
    pruefe("A2: squeeze_thresh in run_backtest ist das Quantil der Stufen",
           ok and s.rb and all(gleich(d["squeeze_thresh"], erwartet(d, lb, pc)) for d in s.rb))
    pruefe("A3: und nicht das Quantil der Voreinstellungen",
           ok and s.rb and not any(gleich(d["squeeze_thresh"], erwartet(d, *vor)) for d in s.rb))

    # --- Teil B: Voreinstellung ----------------------------------------------
    with Spion() as s:
        es.collect_all_trades(all_data, 8.0)
    pruefe("B1: ohne Argument erhaelt compute_indicators die Voreinstellungen",
           bool(s.ci) and all(v == vor for v in s.ci), str(s.ci))
    for name, f in (("equity_simulation.collect_all_trades", es.collect_all_trades),
                    ("multi_symbol_optimise.get_trades_for_symbol", mo.get_trades_for_symbol),
                    ("backtest_breakout.compute_indicators", bt.compute_indicators)):
        ps = inspect.signature(f).parameters
        l, p = ps.get("squeeze_lookback_days"), ps.get("squeeze_percentile")
        pruefe(f"B2: {name} hat beide Achsen mit den Voreinstellungen {vor}",
               l is not None and p is not None and (l.default, p.default) == vor, f"{l}, {p}")

    # --- Teil C: Optimierer-Pfad ---------------------------------------------
    df_ind, cutoff = all_data["SYN"]
    with Spion() as s:
        try:
            mo.get_trades_for_symbol(df_ind, cutoff, 8.0, squeeze_lookback_days=lb, squeeze_percentile=pc)
            ok, fehler = True, ""
        except TypeError as e:
            ok, fehler = False, str(e)
    pruefe("C1: get_trades_for_symbol nimmt beide Achsen", ok, fehler)
    pruefe("C2: compute_indicators erhaelt die Stufen", ok and s.ci == [(lb, pc)], str(s.ci))
    pruefe("C3: squeeze_thresh in run_backtest ist das Quantil der Stufen",
           ok and len(s.rb) == 1 and gleich(s.rb[0]["squeeze_thresh"], erwartet(s.rb[0], lb, pc)))

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

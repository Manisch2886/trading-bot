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

Teil D  Scanbeginn (TB-124, Befund F1 aus TB-122; Nachtrag 1 nach Fable 30a R53: nie
        vor dem Vorlauf der Zelle): compute_indicators vermerkt den Lookback L im
        Frame (df.attrs), run_backtest beginnt den Scan am ersten Index, an dem die
        Einstiegsbedingung definiert ist, BB_PERIOD + L - 1. Fuer JEDE Stufe von
        `bb_lookback` aus `registerdaten.raster()`: der Scanbeginn ist dieser Index,
        am Index davor ist der Squeeze-Status des Vortags NaN, ab ihm definiert; ein
        Ausbruch genau dort wird ueber den Signalpfad gefunden, einer einen Balken
        frueher nicht. Ohne Vermerk gilt die Voreinstellung (BB_PERIOD + 126 - 1).
        `WARMUP_PERIOD` bleibt als Voreinstellung stehen.

Gegenprobe (Register 40.7): am Stand vor TB-122 B scheitert diese Probe
(collect_all_trades und get_trades_for_symbol kennen die Argumente nicht);
am Stand vor TB-124 B scheitert Teil D (Scan ab WARMUP_PERIOD + 1, kein Vermerk).
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

BOT = "volatility_breakout_crypto"

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
    all_data = {"SYN": df}   # Gestalt wie load_all_symbol_data(): Rohkurse, Indikatoren erst je Aufruf

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
    with Spion() as s:
        try:
            mo.get_trades_for_symbol(all_data["SYN"], 8.0, squeeze_lookback_days=lb, squeeze_percentile=pc)
            ok, fehler = True, ""
        except TypeError as e:
            ok, fehler = False, str(e)
    pruefe("C1: get_trades_for_symbol nimmt beide Achsen", ok, fehler)
    pruefe("C2: compute_indicators erhaelt die Stufen", ok and s.ci == [(lb, pc)], str(s.ci))
    pruefe("C3: squeeze_thresh in run_backtest ist das Quantil der Stufen",
           ok and len(s.rb) == 1 and gleich(s.rb[0]["squeeze_thresh"], erwartet(s.rb[0], lb, pc)))

    # --- Teil D: Scanbeginn (TB-124, F1; Nachtrag 1 / Fable 30a R53) --------------
    # Erster Index, an dem die Einstiegsbedingung bei Lookback s definiert ist:
    # bb_width ab BB_PERIOD - 1, squeeze_thresh s - 1 Balken spaeter, und der
    # Einstieg braucht den Squeeze-Status von t - 1.
    def frueh(s):
        return bt.BB_PERIOD + s - 1

    alle = list(r["bb_lookback"])
    bindend = [s for s in alle if frueh(s) <= bt.WARMUP_PERIOD]
    print(f"Teil D: Stufen {alle}, hergeleiteter Scanbeginn {[frueh(s) for s in alle]}; "
          f"frueher fester Scanbeginn WARMUP_PERIOD + 1 = {bt.WARMUP_PERIOD + 1} schnitt ab bei {bindend}")
    pruefe("D0: es gibt Stufen, bei denen der fruehere feste Scanbeginn einen Einstieg abschnitt",
           bool(bindend), str(alle))
    pruefe("D0b: WARMUP_PERIOD bleibt die Voreinstellung max(BB_PERIOD, BB_LOOKBACK, VOLUME_AVG_PERIOD)",
           bt.WARMUP_PERIOD == max(bt.BB_PERIOD, lp.BB_LOOKBACK, bt.VOLUME_AVG_PERIOD))

    def dauersignal(n=600):
        # Jeder Balken ist Squeeze-Ausbruch - der erste Einstieg IST der Scanbeginn.
        c = np.full(n, 100.0)
        return pd.DataFrame({"open_time": pd.date_range("2020-01-01", periods=n, freq="D"),
                             "open": c, "high": c, "low": c, "close": c, "volume": 1e6,
                             "vol_avg": 1e6, "bb_upper": c * 0.5, "is_squeeze": True})

    def erster_einstieg(d):
        tr = bt.run_backtest(d, stop_loss_pct=None, max_hold_days=1)
        if tr.empty:
            return None
        return int(np.searchsorted(d["open_time"].to_numpy(), np.datetime64(tr["entry_time"].iloc[0])))

    # (i) knapp am Vorlauf, jede Stufe und die Voreinstellung
    for s in alle + [lp.BB_LOOKBACK]:
        d = dauersignal()
        d.attrs["squeeze_lookback_days"] = s
        ist = erster_einstieg(d)
        pruefe(f"D1: Vermerk {s} im Frame -> Scan beginnt am hergeleiteten Index {frueh(s)}",
               ist == frueh(s), f"ist {ist}")
        ind = bt.compute_indicators(df, s)
        st, ob = ind["squeeze_thresh"].to_numpy(), ind["bb_upper"].to_numpy()
        k = frueh(s)
        pruefe(f"D1b: Stufe {s}: am Index {k - 1} ist der Squeeze-Status des Vortags NaN, ab {k} definiert",
               bool(np.isnan(st[k - 2])) and not np.isnan(st[k - 1]) and not np.isnan(ob[k])
               and not np.isnan(st[k:]).any(), f"{st[k - 2]}, {st[k - 1]}")
    ist = erster_einstieg(dauersignal())
    pruefe(f"D2: ohne Vermerk gilt die Voreinstellung: Scanbeginn {frueh(lp.BB_LOOKBACK)}",
           ist == frueh(lp.BB_LOOKBACK), f"ist {ist}")

    def sprung(k, n=600):
        # Schwingung mit Periode 4 (teilt BB_PERIOD) und fallender Amplitude: die
        # Bandbreite faellt stetig, jeder Balken mit gueltiger Schwelle ist Squeeze,
        # aber keiner schliesst ueber dem oberen Band. An Balken k der Ausbruch.
        t = np.arange(n)
        c = 100 + np.linspace(2.0, 0.2, n) * np.sin(np.pi * t / 2)
        c[k:] = c[k - 1] + 10
        return pd.DataFrame({"open_time": pd.date_range("2020-01-01", periods=n, freq="D"),
                             "open": c, "high": c, "low": c, "close": c, "volume": 1e6})

    def einstieg_bei(trades, d, k):
        return (not trades.empty) and bool((trades["entry_time"] == d["open_time"].iloc[k]).any())

    # (ii) Einstieg am ersten zulaessigen Index, jede Stufe
    for s in alle:
        k = frueh(s)
        d = sprung(k)
        with Spion() as s_mit:
            mit = es.collect_all_trades({"SYN": d}, 8.0, squeeze_lookback_days=s)
        ohne = es.collect_all_trades({"SYN": d}, 8.0)
        davor = es.collect_all_trades({"SYN": sprung(k - 1)}, 8.0, squeeze_lookback_days=s)
        opt = mo.get_trades_for_symbol(d, 8.0, squeeze_lookback_days=s)
        pruefe(f"D3: Stufe {s}: Signalpfad findet den Einstieg am ersten zulaessigen Index {k}",
               einstieg_bei(mit, d, k))
        if frueh(s) < frueh(lp.BB_LOOKBACK):
            pruefe(f"D3b: ohne Stufe (Voreinstellung) kein Einstieg an Index {k}", not einstieg_bei(ohne, d, k))
        pruefe(f"D3c: Stufe {s}, Ausbruch einen Balken frueher ({k - 1}): kein Einstieg dort",
               not einstieg_bei(davor, sprung(k - 1), k - 1))
        pruefe(f"D4: Stufe {s}: Optimierer-Pfad findet den Einstieg an Index {k}", einstieg_bei(opt, d, k))
        pruefe(f"D5: Stufe {s}: der Vermerk kommt in run_backtest an",
               bool(s_mit.rb) and all(x.attrs.get("squeeze_lookback_days") == s for x in s_mit.rb),
               str([x.attrs for x in s_mit.rb]))

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

"""TB-124 C2 - Teil D (Scanbeginn) in die zwei test_posten3_durchreichung.py der Breakout-Bots einsetzen.
Bestehende Pruefungen bleiben unveraendert; nur der Docstring-Satz 'Nicht Gegenstand: ...' wird nachgezogen
und Teil D vor der Schlussausgabe von main() eingefuegt. Aufruf: python3 c2_tests_einbau.py <wurzel>"""
import os, sys
W = sys.argv[1]

DOC_ALT = """Nicht Gegenstand: `backtest_breakout.WARMUP_PERIOD` (Scanbeginn) haengt weiter
an der Voreinstellung - Befund im Ergebnis von TB-122, die Datei liegt
ausserhalb des Auftrags.

Gegenprobe (Register 40.7): am Stand vor TB-122 B scheitert diese Probe
(collect_all_trades und get_trades_for_symbol kennen die Argumente nicht).
"""
DOC_NEU = """Teil D  Scanbeginn (TB-124, Befund F1 aus TB-122; Nachtrag 1 nach Fable 30a R53: nie
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

TEIL_D = '''
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
{SIGNALPFAD}
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
'''

SIGNALPFAD = {
    "volatility_breakout": '''        with Spion() as s_mit:
            mit = es.collect_all_trades({"SYN": (bt.compute_indicators(d), None)}, 8.0, squeeze_lookback_days=s)
        ohne = es.collect_all_trades({"SYN": (bt.compute_indicators(d), None)}, 8.0)
        d_davor = sprung(k - 1)
        davor = es.collect_all_trades({"SYN": (bt.compute_indicators(d_davor), None)}, 8.0, squeeze_lookback_days=s)
        opt = mo.get_trades_for_symbol(bt.compute_indicators(d), None, 8.0, squeeze_lookback_days=s)''',
    "volatility_breakout_crypto": '''        with Spion() as s_mit:
            mit = es.collect_all_trades({"SYN": d}, 8.0, squeeze_lookback_days=s)
        ohne = es.collect_all_trades({"SYN": d}, 8.0)
        davor = es.collect_all_trades({"SYN": sprung(k - 1)}, 8.0, squeeze_lookback_days=s)
        opt = mo.get_trades_for_symbol(d, 8.0, squeeze_lookback_days=s)''',
}

ANKER = '''
    print("\\n" + "=" * 78)
    if gescheitert:'''

for bot, sig in SIGNALPFAD.items():
    p = os.path.join(W, "strategies", bot, "test_posten3_durchreichung.py")
    s = open(p, encoding="utf-8").read()
    for a in (DOC_ALT, ANKER):
        if s.count(a) != 1:
            sys.exit(f"ABBRUCH {p}: Anker {s.count(a)}x: {a[:50]!r}")
    s = s.replace(DOC_ALT, DOC_NEU).replace(ANKER, TEIL_D.replace("{SIGNALPFAD}", sig) + ANKER)
    open(p, "w", encoding="utf-8").write(s)
    print("eingesetzt", p)

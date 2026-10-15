#!/usr/bin/env python3
"""TB-163 (E-6, TB-30b Posten 4): Horizont je Bot aus faltenplan.HORIZONTBEGINN in den vier
Aktien-Optimierern - Pruefung auf SYNTHETISCHEN Kursen (Zufallspfad im Temp-Ordner), keine
Kursdaten aus data/, kein Optimierer-Lauf, keine Rastersuche. R81 (d): das Ende einer Datei geht
weder in das Fenster noch in den Scanbeginn noch in den Anfang der geladenen Zeilen ein.
Aufruf aus der Repo-Wurzel: python3 -B research/posten4_horizont/test_posten4_horizont.py
(je Bot ein Kindprozess, damit sich gleichnamige Bot-Module nicht mischen). rc 0 = alle bestanden."""
import importlib.util, os, re, subprocess, sys, tempfile
WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOTS = ["elliott_wave_stocks", "rsi2_mean_reversion", "turtle_soup_stocks", "volatility_breakout"]
ENDE_A, ENDE_B, ENDE_C = "2026-09-30", "2025-06-30", "2026-12-31"
def kind(bot):
    import numpy as np
    import pandas as pd
    H = pd.Timestamp(2016, 9, 19); n = [0, 0]
    def pruefe(name, ok, info=""):
        n[0] += 1; n[1] += bool(ok); print(("ja    " if ok else "NEIN  ") + bot + ": " + name + (" · " + str(info) if info else ""))
    t = pd.bdate_range("2008-01-02", ENDE_C); r = np.random.default_rng(163)
    c = 50 * np.exp(np.cumsum(r.normal(0.0002, 0.018, len(t)))); o = c * (1 + r.normal(0, 0.004, len(t)))
    h = np.maximum(o, c) * (1 + np.abs(r.normal(0, 0.008, len(t)))); lo = np.minimum(o, c) * (1 - np.abs(r.normal(0, 0.008, len(t))))
    basis = pd.DataFrame({"open_time": t.strftime("%Y-%m-%d"), "open": o, "high": h, "low": lo, "close": c, "volume": r.integers(100000, 1000000, len(t))})
    sys.path.insert(0, os.path.join(WURZEL, "strategies", bot))
    spec = importlib.util.spec_from_file_location("opt_" + bot, os.path.join(WURZEL, "strategies", bot, "multi_symbol_optimise.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    src = open(os.path.join(WURZEL, "strategies", bot, "multi_symbol_optimise.py"), encoding="utf-8").read()
    pruefe("Quelltext: kein Fenster aus open_time.max() - DateOffset", not re.search(r'\["open_time"\]\.max\(\)\s*-\s*pd\.DateOffset', src))
    hb = getattr(m, "horizontbeginn_ts", None)
    pruefe("horizontbeginn_ts() = faltenplan.horizontbeginn = 2016-09-19", hb is not None and hb() == H, hb() if hb else "fehlt")
    if hb is not None:
        import faltenplan
        pruefe("Wert kommt aus faltenplan.HORIZONTBEGINN (Modul research/vorregistrierung)", os.path.samefile(faltenplan.__file__, os.path.join(WURZEL, "research", "vorregistrierung", "faltenplan.py")) and pd.Timestamp(faltenplan.HORIZONTBEGINN["aktien"]) == H)
    interval = getattr(m, "INTERVAL", "1d")
    for zone in (None, "UTC"):  # B5: naiv (heute alle Aktien-1d-Dateien) und zeitzonenbehaftet (open_time mit +00:00)
        hz = H if zone is None else H.tz_localize(zone); kz = "naiv" if zone is None else "tz " + zone
        with tempfile.TemporaryDirectory() as d:
            for s, e in (("AAA", ENDE_A), ("BBB", ENDE_B), ("CCC", ENDE_C)):
                x = basis[basis["open_time"] <= e].copy()
                if zone is not None:
                    x["open_time"] = x["open_time"] + " 00:00:00+00:00"
                x.to_csv(os.path.join(d, "%s_%s.csv" % (s, interval)), index=False)
            m.DATA_DIR = d; m.SYMBOLS = ["AAA", "BBB", "CCC"]
            try:
                data = m.load_all_symbol_data()
            except Exception as ex:
                pruefe("[%s] Laden ohne Fehler" % kz, False, repr(ex)[:200]); continue
        pruefe("[%s] alle drei synthetischen Symbole geladen" % kz, sorted(data) == ["AAA", "BBB", "CCC"], sorted(data))
        if sorted(data) != ["AAA", "BBB", "CCC"]:
            continue
        if bot == "elliott_wave_stocks":
            anf = {s: data[s]["open_time"].min() for s in data}
            pruefe("[%s] Anfang der geladenen Zeilen = Horizontbeginn, gleich fuer drei Dateienden" % kz, all(v == hz for v in anf.values()), {k: str(v) for k, v in anf.items()})
            a, c2 = data["AAA"].reset_index(drop=True), data["CCC"].reset_index(drop=True)
            pruefe("[%s] laengere Datei (CCC) beginnt zeilengleich wie AAA" % kz, a.equals(c2.iloc[:len(a)].reset_index(drop=True)))
        else:
            cut = {s: data[s][1] for s in data}
            pruefe("[%s] Fenster (entry_cutoff) = Horizontbeginn in der Spaltenzone, gleich fuer drei Dateienden" % kz, all(v == hz and (v.tzinfo is None if zone is None else (v.tzinfo is not None and v.utcoffset() == pd.Timedelta(0))) for v in cut.values()), {k: str(v) for k, v in cut.items()})
            if bot == "volatility_breakout":
                import backtest_breakout as bb
                sc = {s: int((data[s][0]["open_time"] < data[s][1]).sum()) for s in data}
                pruefe("[%s] Scanbeginn (Zeilen vor entry_cutoff) gleich fuer drei Dateienden" % kz, len(set(sc.values())) == 1, sc)
                try:
                    ta, tc = (bb.run_backtest(data[s][0], entry_cutoff=data[s][1]) for s in ("AAA", "CCC"))
                except TypeError as ex:  # backtest_breakout.py (nicht E-6, unveraendert): np.datetime64(entry_cutoff) gegen tz-behaftetes entry_time
                    print("INFO  %s: [%s] run_backtest: %s - Befund ausserhalb E-6, nicht gezaehlt" % (bot, kz, str(ex)[:120])); continue
                ez = lambda v: pd.to_datetime(v) if zone is None else pd.to_datetime(v, utc=True)
                pruefe("[%s] kein Einstieg vor dem Horizontbeginn" % kz, len(ta) == 0 or ez(ta["entry_time"]).min() >= hz, len(ta))
                gr = pd.Timestamp(ENDE_A) - pd.Timedelta(days=60); gr = gr if zone is None else gr.tz_localize(zone)
                g = lambda y: y[ez(y["exit_time"]) < gr].reset_index(drop=True)
                pruefe("[%s] Trades bis 60 Tage vor dem Ende von AAA gleich bei laengerer Datei" % kz, len(g(ta)) > 0 and g(ta).equals(g(tc)), len(g(ta)))
    return n
if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--kind":
        n = kind(sys.argv[2]); print("KIND %d %d" % tuple(n)); sys.exit(0)
    gesamt = [0, 0]
    for b in BOTS:
        r = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--kind", b], capture_output=True, text=True, cwd=WURZEL)
        zeilen = [l for l in r.stdout.split("\n") if l.startswith(("ja ", "NEIN", "INFO"))]; print("\n".join(zeilen))
        k = [l for l in r.stdout.split("\n") if l.startswith("KIND ")]
        if r.returncode != 0 or not k:
            print("NEIN  %s: Kindprozess rc %d: %s" % (b, r.returncode, (r.stderr.strip().split("\n") or [""])[-1][:200])); gesamt[0] += 1; continue
        a, ok = map(int, k[0].split()[1:]); gesamt[0] += a; gesamt[1] += ok
    print("%d von %d Pruefungen bestanden" % (gesamt[1], gesamt[0])); sys.exit(0 if gesamt[0] == gesamt[1] and gesamt[0] > 0 else 1)

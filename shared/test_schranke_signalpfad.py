#!/usr/bin/env python3
"""TB-166 (E-3a; R90 (c), (d), (g), R98 (a), (b)): die Schranke im Signalpfad der neun Bots - synthetisch.
Je Bot ein Kindprozess: Zufallspfade im Temp-Ordner (DATA_DIR/SYMBOLS des Laders umgebogen), Trades ueber
research/exposure_messung/bot_lauf.hole_trades(es, all_data[, handelbar]). data/ wird nicht gelesen,
kein Optimierer-Lauf, keine Rastersuche.
  1  alte Bahn (ohne handelbar) byte-gleich zur Referenz aus dem unveraenderten Stand (--referenz-schreiben)
  2  kein Einstieg vor dem entry_cutoff des Symbols (spaeterer von Horizontbeginn und Handelbar-Tag)
  3  Tag mitten in einer alten Position: ein Signal ab dem Tag steigt ein, frueher als der alte naechste
     Einstieg (Positions-Bots); Elliott: alle alten Trades ab dem Tag bleiben, gesperrte Welle ohne Rest
  4  Indikatoren ungekuerzt: Symbol ohne Signal vor seinem Tag gleich mit und ohne Schranke
  5  Mutationsprobe in einer Kopie: Scanbeginn bzw. Scan-Schranke entfernt -> die Probe beisst
Aufruf aus der Repo-Wurzel: python3 -B shared/test_schranke_signalpfad.py [--referenz DATEI | --referenz-schreiben DATEI]"""
import hashlib, json, os, shutil, subprocess, sys, tempfile
WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOTS = ["rsi2_crypto", "turtle_soup_crypto", "volatility_breakout_crypto", "rsi2_mean_reversion", "turtle_soup_stocks",
        "volatility_breakout", "t3_supertrend", "elliott_wave", "elliott_wave_stocks"]
SECHS = BOTS[:6]
AKTIEN = ("rsi2_mean_reversion", "turtle_soup_stocks", "volatility_breakout", "elliott_wave_stocks")
def kind(bot, wurzel, modus):
    import numpy as np, pandas as pd
    sys.argv = ["bot_lauf", bot]; sys.path.insert(0, os.path.join(wurzel, "research", "exposure_messung"))
    import bot_lauf as bl; import equity_simulation as es; import multi_symbol_optimise as mso
    tf = {"elliott_wave": "1h", "t3_supertrend": "4h"}.get(bot, "1d")
    if bot in AKTIEN: t = pd.bdate_range("2008-01-02", "2026-08-31")
    else: t = pd.date_range({"1d": "2019-01-01", "4h": "2021-06-01", "1h": "2022-01-01"}[tf], "2026-08-31 23:00", freq=tf.replace("d", "D"))
    syms = ["AAA", "BBB", "CCC"] + ([] if bot in AKTIEN else ["BTCUSDT"]); d = tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))
    for k, s in enumerate(syms):
        r = np.random.default_rng(166 + k); v = {"1h": 0.012, "4h": 0.012}.get(tf, 0.025)
        c = 50 * np.exp(np.cumsum(r.normal(0.0001, v, len(t)))); o = c * (1 + r.normal(0, v / 5, len(t)))
        h = np.maximum(o, c) * (1 + np.abs(r.normal(0, v / 3, len(t)))); lo = np.minimum(o, c) * (1 - np.abs(r.normal(0, v / 3, len(t))))
        fmt = "%Y-%m-%d" if tf == "1d" else "%Y-%m-%d %H:%M:%S"
        pd.DataFrame({"open_time": t.strftime(fmt), "open": o, "high": h, "low": lo, "close": c, "volume": r.integers(10**5, 10**6, len(t))}).to_csv(os.path.join(d, "%s_%s.csv" % (s, getattr(mso, "INTERVAL", tf))), index=False)
    mso.DATA_DIR = d; mso.SYMBOLS = syms
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        data = es.load_all_symbol_data()
    def lauf(handelbar=None):
        with contextlib.redirect_stdout(io.StringIO()):
            x = bl.hole_trades(es, dict(data)) if handelbar is None else bl.hole_trades(es, dict(data), handelbar)
        if x is None or x.empty: return pd.DataFrame(columns=["entry_time", "exit_time", "symbol"])
        x = x.copy(); x["entry_time"] = pd.to_datetime(x["entry_time"]); x["exit_time"] = pd.to_datetime(x["exit_time"])
        return x.reset_index(drop=True)
    alt = lauf()
    if modus == "referenz":
        print("REF " + json.dumps({"n": len(alt), "sha256": hashlib.sha256(alt.to_csv(index=False).encode()).hexdigest()})); return
    hb = pd.Timestamp("2016-09-19") if bot in AKTIEN else None
    erst = {s: (data[s][0] if isinstance(data[s], tuple) else data[s])["open_time"].min() for s in data}
    früh = {s: str(erst[s].date()) for s in data}
    n = [0, 0]
    def pruefe(name, ok, info=""):
        n[0] += 1; n[1] += bool(ok); print(("ja    " if ok else "NEIN  ") + bot + ": " + name + (" · " + str(info) if info else ""))
    if modus.startswith("ref="):
        ref = json.loads(open(modus[4:]).read())[bot]
        pruefe("1 alte Bahn ohne handelbar byte-gleich zum unveraenderten Stand", ref["sha256"] == hashlib.sha256(alt.to_csv(index=False).encode()).hexdigest(), "%d Trades" % len(alt))
    def schnitt(x, s): return x[x["symbol"] == s].reset_index(drop=True)
    def cut(tag): return tag if hb is None else max(hb, tag)
    # 3: Tag mitten in einer alten Position des Symbols mit den meisten alten Trades (S3)
    S3 = max(["AAA", "BBB"], key=lambda s: len(schnitt(alt, s))); b = schnitt(alt, S3); kand = []
    for _, z in b.iterrows():
        tag = z["entry_time"].normalize() + pd.Timedelta(days=1)
        if tag < z["exit_time"] and z["entry_time"] >= cut(pd.Timestamp("1900-01-01")): kand.append((tag, z["exit_time"]))
    gefunden, verletzt, geprueft = None, [], 0
    for tag, aus in kand[:12]:
        h = dict(früh); h[S3] = str(tag.date()); neu = lauf(h); geprueft += 1
        for s in data:
            c = cut(pd.Timestamp(h[s])); x = schnitt(neu, s)
            if len(x) and x["entry_time"].min() < c: verletzt.append((s, str(x["entry_time"].min()), str(c)))
        nb = schnitt(neu, S3); ab = b[b["entry_time"] >= tag]
        if bot.startswith("elliott"):
            alt_ab = set(map(tuple, ab[["entry_time", "exit_time"]].astype(str).values)); neu_m = set(map(tuple, nb[["entry_time", "exit_time"]].astype(str).values))
            if not alt_ab <= neu_m: verletzt.append((S3, "alter Trade ab Tag fehlt", str(tag)))
            if len(nb) and gefunden is None: gefunden = (S3, str(tag.date()), str(nb["entry_time"].min()), "%d alte Trades ab Tag erhalten" % len(ab))
        elif len(nb) and nb["entry_time"].min() >= tag and (bot == "t3_supertrend" or nb["entry_time"].min() <= aus) and gefunden is None:
            # t3_supertrend: Einstieg nur am Kreuzen nach oben, die alte Position endet am Kreuzen nach unten -
            # ein Einstieg vor ihrem Ende ist dort nicht moeglich; geprueft wird, dass ab dem Tag eingestiegen wird.
            gefunden = (S3, str(tag.date()), str(nb["entry_time"].min()), "alte Position bis " + str(aus))
        if gefunden and geprueft >= 3: break
    pruefe("2 kein Einstieg vor dem entry_cutoff je Symbol (%d Laeufe)" % geprueft, geprueft > 0 and not verletzt, verletzt[:2])
    pruefe("3 Tag in alter Position: ab dem Tag wird eingestiegen" + (" (Elliott: alte Trades ab Tag bleiben)" if bot.startswith("elliott") else (" (nach Kreuzen)" if bot == "t3_supertrend" else ", vor dem Ende der alten Position")), gefunden is not None, gefunden or "%d Kandidaten, %d alte Trades %s" % (len(kand), len(b), S3))
    # 4: CCC mit Tag am ersten alten Einstieg (kein Signal davor) -> gleich mit/ohne Schranke
    c0 = schnitt(alt, "CCC")
    if len(c0):
        h = dict(früh); h["CCC"] = str(c0["entry_time"].min().date()); neu = schnitt(lauf(h), "CCC")
        pruefe("4 Indikatoren ungekuerzt: CCC (Tag %s, kein Signal davor) gleich mit/ohne Schranke" % h["CCC"], neu.equals(c0), "%d/%d" % (len(neu), len(c0)))
    else:
        pruefe("4 CCC hat alte Trades", False)
    if bot.startswith("elliott"):   # 3b: gesperrte Welle ohne Rest (find_causal_waves direkt, freshness None)
        import elliott_wave_counter as ewc
        df = data[S3][0] if isinstance(data[S3], tuple) else data[S3]
        zz = mso.calculate_zigzag_with_confirmation(df, deviation_pct=getattr(es, "DEVIATION_PCT", 10.0))
        w0 = ewc.find_causal_waves(zz, min_fib_score=0.3, freshness_bars=None, direction="bearish"); ok = None
        for _, w in w0.iterrows():
            w1 = ewc.find_causal_waves(zz, min_fib_score=0.3, freshness_bars=None, direction="bearish", min_entry_idx=int(w["entry_idx"]) + 1)
            m = w1[w1["end_time"] == w["end_time"]]
            if len(m) == 1 and int(m["entry_idx"].iloc[0]) >= int(w["entry_idx"]) + 1: ok = (str(w["end_time"]), int(w["entry_idx"]), int(m["entry_idx"].iloc[0])); break
        pruefe("5 gesperrte Welle hinterlaesst keinen traded-Eintrag: sie steigt am ersten Lauf >= Schranke ein", ok is not None, ok)
    print("KIND %d %d" % tuple(n))
def mutiere(bot, ziel):
    for e in os.listdir(WURZEL):
        if e not in ("strategies", ".git"): os.symlink(os.path.join(WURZEL, e), os.path.join(ziel, e))
    os.makedirs(os.path.join(ziel, "strategies"))
    for b in os.listdir(os.path.join(WURZEL, "strategies")):
        q = os.path.join(WURZEL, "strategies", b)
        if b == bot: shutil.copytree(q, os.path.join(ziel, "strategies", b), ignore=shutil.ignore_patterns("__pycache__", "results"))
        else: os.symlink(q, os.path.join(ziel, "strategies", b))
    if bot in SECHS:
        p = [f for f in os.listdir(os.path.join(ziel, "strategies", bot)) if f.startswith("backtest_")][0]; alt = 'start_i = max(start_i, int((df["open_time"] < entry_cutoff).sum()))'; neu = "pass  # MUTATION: Scanbeginn aus"
    elif bot == "t3_supertrend": p, alt, neu = "backtest_trend.py", " and i >= erster_einstieg:", ":  # MUTATION"
    else: p, alt, neu = "elliott_wave_counter.py", "if min_entry_idx is not None and run_bar < min_entry_idx:\n                continue\n            traded.add(end_time)", "traded.add(end_time)\n            if min_entry_idx is not None and run_bar < min_entry_idx:  # MUTATION: nach traded.add\n                continue"
    f = os.path.join(ziel, "strategies", bot, p); s = open(f).read(); k = s.count(alt); open(f, "w").write(s.replace(alt, neu)); return k
if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "--kind":
        kind(sys.argv[2], sys.argv[3], sys.argv[4]); sys.exit(0)
    ref = sys.argv[2] if len(sys.argv) == 3 and sys.argv[1] in ("--referenz", "--referenz-schreiben") else None
    def starte(bot, wurzel, modus):
        return subprocess.run([sys.executable, "-B", "-W", "ignore", os.path.join(wurzel, "shared", "test_schranke_signalpfad.py"), "--kind", bot, wurzel, modus], capture_output=True, text=True, cwd=wurzel)
    if ref and sys.argv[1] == "--referenz-schreiben":
        aus = {}
        for b in BOTS:
            shutil.copy(os.path.abspath(__file__), os.path.join(WURZEL, "shared", "test_schranke_signalpfad.py")) if not os.path.exists(os.path.join(WURZEL, "shared", "test_schranke_signalpfad.py")) else None
            r = starte(b, WURZEL, "referenz"); z = [l for l in r.stdout.split("\n") if l.startswith("REF ")]
            if r.returncode or not z: print("NEIN  %s: Referenz rc %d %s" % (b, r.returncode, r.stderr.strip()[-200:])); sys.exit(1)
            aus[b] = json.loads(z[0][4:]); print("REF  %s %s" % (b, aus[b]))
        open(ref, "w").write(json.dumps(aus, indent=1, sort_keys=True) + "\n"); print("rc 0"); sys.exit(0)
    gesamt = [0, 0]
    for b in BOTS:
        r = starte(b, WURZEL, "ref=" + os.path.abspath(ref) if ref else "pruefen")
        print("\n".join(l for l in r.stdout.split("\n") if l.startswith(("ja ", "NEIN", "INFO"))))
        k = [l for l in r.stdout.split("\n") if l.startswith("KIND ")]
        if r.returncode or not k: print("NEIN  %s: Kindprozess rc %d: %s" % (b, r.returncode, r.stderr.strip()[-300:])); gesamt[0] += 1; continue
        a, ok = map(int, k[0].split()[1:]); gesamt[0] += a; gesamt[1] += ok
        with tempfile.TemporaryDirectory() as z:   # 5/6 Mutationsprobe in einer Kopie
            treffer = mutiere(b, z); m = starte(b, z, "pruefen")
            mk = [l for l in m.stdout.split("\n") if l.startswith("KIND ")]; beisst = m.returncode == 2 or (mk and mk[0].split()[1] != mk[0].split()[2]) or ("ABBRUCH (Wache R90 (d))" in m.stderr)
            wie = "Wache rc 2" if (m.returncode == 2 or "ABBRUCH (Wache" in m.stderr) else ("NEIN-Zeilen: " + "; ".join(l[6:90] for l in m.stdout.split("\n") if l.startswith("NEIN"))[:200])
            gesamt[0] += 1; gesamt[1] += bool(treffer == 1 and beisst)
            print(("ja    " if treffer == 1 and beisst else "NEIN  ") + "%s: 6 Mutationsprobe (%s) beisst · %s" % (b, "Scanbeginn aus" if b in SECHS else "Scan-Schranke aus/nach traded.add", wie))
    print("%d von %d Pruefungen bestanden" % (gesamt[1], gesamt[0])); sys.exit(0 if gesamt[0] == gesamt[1] and gesamt[0] > 0 else 1)

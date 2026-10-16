#!/usr/bin/env python3
"""TB-169 (E-3b; R86 (b)-(d), R87 (c), R81 (c)/(h), R90 (g), R98 (d), R97 (a)): Probe am Listen-Erzeuger
research/tb24_haltedauern/positionen_holen.py auf Test-Snapshots (Ersatzwurzel TB36_BASE_DIR im Temp-Ordner, DATA_DIR/SYMBOLS
des Laders umgebogen, Bauart loaderlauf.lade_botmodul). data/ wird nicht gelesen. Geprueft an den AUSGABEN des Erzeugers
(<bot>_alle_trades.csv, Rueckgabewert), je Bot im eigenen Prozess; Snapshot A mit, B ohne Zeilen ab dem Schnitt (B = A gekuerzt).
Die Zeitachse wird je Bot um eine Zahl Balken versetzt (gleiche Kursfolge), bis A (Schnitt aus) ein Einstiegssignal ab dem
Schnitt und eine vor dem Schnitt eroeffnete, am letzten Tag von B offene Position enthaelt (Bauart R81 (h)).
   1 Probe R86 (d): Listen aus A und B byte-gleich, rc 0
  2a Schnitt aus -> Wache 1 (Zeile ab Schnitt im Signalpfad) beisst allein (2)
  2b Schnitt und Wachen aus -> Listen weichen von B ab, ein Einstieg ab dem Schnitt erscheint (R81 (h))
  2c Schnitt und Wache 1 aus -> Wache 2 (Trade-Zeit am Schnitt oder spaeter) beisst allein (2)
  3a R90 (g): Tag in einer offenen Position -> kein Einstieg davor; der ohne Schranke verdraengte zweite Einstieg erscheint
     (vor dem alten Ausstieg). Tatsachennotiz nach R90 (g) bei t3_supertrend (Fall kann nicht entstehen) und den zwei Elliott-Bots
     (Teilmessung, Wortlaut in OHNE_R90G); dort geprueft: kein Einstieg vor dem Tag, alle alten Trades ab dem Tag bleiben
  3b spaetes Symbol (Tag am ersten alten Einstieg) gleich mit/ohne Schranke
   4 Gegenprobe R87 (c): Schranke aus (hole_trades ohne handelbar) -> Wache 3 beisst (2)
  5a R81 (h), eigener Snapshot mit Symbol SPAET (erreicht die Schranke nur mit Zeilen ab dem Schnitt): rc 0, Tag None, nicht in der Liste
  5b derselbe Snapshot, Schnitt und Wache 1 aus -> SPAET geladen ohne Tag -> Wache R81 (c) beisst (2), ohne Eingriff in den Tag
   6 A9: Spalte symbol unveraendert, keine positionen.csv
   7 R86 (c)/R83 (c): die am Ende von B offene Position wird nach der Ausstiegskonvention des Signalpfads behandelt (kein Trade, oder
     Ausstieg am letzten Balken vor dem Schnitt); B rc 0, keine leere Ausstiegszeit (NaT), kein Ausstieg am Schnitt oder spaeter
   8 nur Dateien des Test-Snapshots gelesen (read_csv), auch fuer den BTC-Regimefilter
Aufruf aus der Repo-Wurzel: python3 -B research/tb24_haltedauern/test_listen_erzeuger.py [bot ...]  (rc 0 = alle bestanden)"""
import json, os, shutil, subprocess, sys, tempfile
WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOTS = ["rsi2_crypto", "turtle_soup_crypto", "volatility_breakout_crypto", "rsi2_mean_reversion", "turtle_soup_stocks",
        "volatility_breakout", "t3_supertrend", "elliott_wave", "elliott_wave_stocks"]
AKTIEN = ("rsi2_mean_reversion", "turtle_soup_stocks", "volatility_breakout", "elliott_wave_stocks")
TF = {"elliott_wave": "1h", "t3_supertrend": "4h"}
SCHNITT = "2026-09-01"
OHNE_R90G = {"t3_supertrend": "Einstieg nur am Kreuzen nach oben (backtest_trend.py Z. 111-112), die Position endet am Kreuzen nach unten, "
                              "am Trend-Flip des Supertrend (Z. 123) oder am Stop: solange sie offen ist, entsteht kein zweites "
                              "Einstiegssignal, das verdraengt werden koennte",
             "elliott_wave": "Teilmessung - die Trade-Schleife fuehrt keinen Positionszustand (backtest_elliott.py Z. 113: je Welle ein Trade); "
                             "verdraengt wird nur in der Wellenauswahl (traded, elliott_wave_counter.py Z. 363), die Schranke steht davor (Z. 361): "
                             "eine gesperrte Welle hinterlaesst keinen traded-Eintrag - belegt am Signalpfad in TB-166 (test_schranke_signalpfad "
                             "Pruefung 5 und Mutation, docs/belege/TB-166/e_test_schranke.txt); am Erzeuger nicht herstellbar (kein Paar alter "
                             "Einstiege innerhalb SIGNAL_FRESHNESS_BARS 48 im Test-Snapshot); geprueft: kein Einstieg vor dem Tag, alte Trades ab dem Tag bleiben",
             "elliott_wave_stocks": "Teilmessung - wie elliott_wave (backtest_elliott.py Z. 122, elliott_wave_counter.py Z. 361/363, "
                                    "SIGNAL_FRESHNESS_BARS 5; TB-166 Pruefung 5 und Mutation); geprueft: kein Einstieg vor dem Tag, alte Trades ab dem Tag bleiben"}
def achse(bot, versatz):
    import pandas as pd
    tf = TF.get(bot, "1d")
    if bot in AKTIEN:
        n = len(pd.bdate_range("2008-01-02", "2027-12-31")); return pd.bdate_range(pd.Timestamp("2008-01-02") + pd.offsets.BDay(versatz), periods=n)
    a = {"1d": "2019-01-01", "4h": "2021-06-01", "1h": "2022-01-01"}[tf]; f = tf.replace("d", "D"); n = len(pd.date_range(a, "2027-12-31 23:00", freq=f))
    return pd.date_range(pd.Timestamp(a) + versatz * pd.Timedelta(f), periods=n, freq=f)
def snapshot(bot, d, ab_schnitt, seed, spaet=False, versatz=0):
    import numpy as np, pandas as pd
    tf = TF.get(bot, "1d"); t = achse(bot, versatz)
    syms = ["AAA", "BBB", "CCC"] + ([] if bot in AKTIEN else ["BTCUSDT"]) + (["SPAET"] if spaet else [])
    for u in ("data", "config", "strategies/" + bot, "research"): os.makedirs(os.path.join(d, u), exist_ok=True)
    shutil.copy(os.path.join(WURZEL, "strategies", bot, "multi_symbol_optimise.py"), os.path.join(d, "strategies", bot))
    os.symlink(os.path.join(WURZEL, "research", "universum_trockenlauf"), os.path.join(d, "research", "universum_trockenlauf"))   # Aktien-Horizont (TB-163)
    open(os.path.join(d, "config", "top25_symbols.txt"), "w").write("" if bot in AKTIEN else "\n".join(syms) + "\n")
    open(os.path.join(d, "config", "sp500_top150.txt"), "w").write("\n".join(syms) + "\n" if bot in AKTIEN else "")
    for k, s in enumerate(syms):
        r = np.random.default_rng(seed + k); v = 0.012 if tf != "1d" else 0.025
        c = 50 * np.exp(np.cumsum(r.normal(0.0001, v, len(t)))); o = c * (1 + r.normal(0, v / 5, len(t)))
        h = np.maximum(o, c) * (1 + np.abs(r.normal(0, v / 3, len(t)))); lo = np.minimum(o, c) * (1 - np.abs(r.normal(0, v / 3, len(t))))
        df = pd.DataFrame({"open_time": t.strftime("%Y-%m-%d" if tf == "1d" else "%Y-%m-%d %H:%M:%S"), "open": o, "high": h, "low": lo, "close": c,
                           "volume": r.integers(10**5, 10**6, len(t))})
        if s == "SPAET": df = df[t >= pd.Timestamp("2022-01-03" if bot in AKTIEN else "2025-06-01" if tf == "1d" else "2025-01-01")]
        if not ab_schnitt: df = df[pd.to_datetime(df["open_time"]) < pd.Timestamp(SCHNITT)]
        df.to_csv(os.path.join(d, "data", "%s_%s.csv" % (s, tf)), index=False)
def kind(bot, d, ziel, modus, tags):
    import importlib.util
    sys.argv = ["positionen_holen.py", bot, "--ziel", ziel]
    spec = importlib.util.spec_from_file_location("ph", os.path.join(WURZEL, "research", "tb24_haltedauern", "positionen_holen.py"))
    ph = importlib.util.module_from_spec(spec); spec.loader.exec_module(ph)
    import multi_symbol_optimise as mso
    mso.DATA_DIR = os.path.join(d, "data"); tf = TF.get(bot, getattr(mso, "INTERVAL", "1d"))
    mso.SYMBOLS = [s for s in ("AAA", "BBB", "CCC", "BTCUSDT", "SPAET") if os.path.exists(os.path.join(d, "data", "%s_%s.csv" % (s, tf)))]
    echt = ph.fsm.handelbar_ab; t = json.loads(tags); spur = {"gelesen": [], "spaet": "fehlt"}
    def hb(b, schnitt=None):
        x = dict(echt(b, schnitt)); spur["spaet"] = x.get("SPAET", "fehlt"); x.update(t); return x
    ph.fsm.handelbar_ab = hb
    rc_echt = ph.pd.read_csv
    def lies(*a, **k):
        try: spur["gelesen"].append(os.path.realpath(os.fspath(a[0])))
        except TypeError: spur["gelesen"].append(repr(a[0])[:80])
        return rc_echt(*a, **k)
    ph.pd.read_csv = lies
    if "schnitt_aus" in modus: ph.lesesicht_an = lambda: None
    if "wache1_aus" in modus: ph.wache_zeilen = lambda a: None
    if "wachen_aus" in modus: ph.wache_zeilen = lambda a: None; ph.wache_trades = lambda tr, h: None
    if "schranke_aus" in modus:
        alt = ph.basis.hole_trades; ph.basis.hole_trades = lambda es, a, h=None: alt(es, a)
    try: ph.main()
    finally: json.dump(spur, open(os.path.join(d, "spur.json"), "w"))
def lauf(bot, seed, ab_schnitt, modus="", tags="{}", spaet=False):
    with tempfile.TemporaryDirectory() as d:
        snapshot(bot, d, ab_schnitt, seed[0], spaet, seed[1]); z = os.path.join(d, "ziel"); os.makedirs(z)
        r = subprocess.run([sys.executable, "-B", "-W", "ignore", os.path.abspath(__file__), "--kind", bot, d, z, modus, tags], capture_output=True, text=True,
                           cwd=WURZEL, env=dict(os.environ, TB36_BASE_DIR=d))
        f = os.path.join(z, bot + "_alle_trades.csv"); sp = json.load(open(os.path.join(d, "spur.json"))) if os.path.exists(os.path.join(d, "spur.json")) else {}
        fremd = [x for x in sp.get("gelesen", []) if not x.startswith(os.path.realpath(d) + os.sep)]
        return {"rc": r.returncode, "liste": open(f).read() if os.path.exists(f) else None, "dateien": sorted(os.listdir(z)), "fehler": r.stderr.strip().split("\n")[-1][:170],
                "fremd": fremd, "gelesen": len(sp.get("gelesen", [])), "spaet": sp.get("spaet")}
n = [0, 0]
def pruefe(name, ok, info=""):
    n[0] += 1; n[1] += bool(ok); print(("ja    " if ok else "NEIN  ") + name + (" · " + str(info) if info else ""), flush=True)
    return ok
def tab(liste):
    import io, pandas as pd
    return pd.read_csv(io.StringIO(liste), parse_dates=["entry_time", "exit_time"]) if liste else None
def bot_pruefen(bot):
    import pandas as pd
    S = pd.Timestamp(SCHNITT); seed = voll = None
    def passt(sd):
        v = lauf(bot, sd, True, "schnitt_aus+wachen_aus"); x = tab(v["liste"])
        return (x if v["rc"] == 0 and x is not None and (x["entry_time"] >= S).any() and ((x["entry_time"] < S) & (x["exit_time"] >= S)).any() else None), x
    ok, x0 = passt((169, 0))
    if ok is not None: seed, voll = (169, 0), ok
    elif x0 is not None:   # Bauart R81 (h): Zeitachse versetzen, bis ein Trade ueber den Schnitt offen ist (gleiche Kursfolge)
        t0 = achse(bot, 0); i_s = int(t0.searchsorted(S))
        x0 = x0[x0["symbol"] != "BTCUSDT"].assign(dauer=lambda q: q["exit_time"] - q["entry_time"], spaet=lambda q: q["entry_time"] >= S)
        x0 = x0.sort_values(["spaet", "dauer"], ascending=False)   # zuerst Trades ab dem Schnitt: Achse rueckt nach vorn, die Historie bleibt
        for _, z in x0.head(8).iterrows():
            vs = i_s - (int(t0.searchsorted(z["entry_time"])) + int(t0.searchsorted(z["exit_time"]))) // 2
            ok, _ = passt((169, vs))
            if ok is not None: seed, voll = (169, vs), ok; break
    if not pruefe(bot + ": 0 Snapshot nach R81 (h): Signal ab dem Schnitt und offene Position am Ende von B", seed is not None, "Seed/Versatz %s" % (seed,)): return
    A, B = lauf(bot, seed, True), lauf(bot, seed, False)
    pruefe(bot + ": 1 Probe R86 (d): Listen A = B, rc 0", A["rc"] == B["rc"] == 0 and A["liste"] is not None and A["liste"] == B["liste"], (A["rc"], B["rc"], A["fehler"] if A["rc"] else B["fehler"] if B["rc"] else ""))
    b = tab(B["liste"])
    if b is None: return
    r = lauf(bot, seed, True, "schnitt_aus"); pruefe(bot + ": 2a Schnitt aus -> Wache 1 beisst allein (2)", r["rc"] == 2 and "Zeile ab dem Schnitt" in r["fehler"], (r["rc"], r["fehler"]))
    pruefe(bot + ": 2b Schnitt und Wachen aus -> Listen weichen von B ab, %d Einstiege ab dem Schnitt" % int((voll["entry_time"] >= S).sum()), voll.to_csv(index=False) != b.to_csv(index=False) and (voll["entry_time"] >= S).any())
    r = lauf(bot, seed, True, "schnitt_aus+wache1_aus"); pruefe(bot + ": 2c Schnitt und Wache 1 aus -> Wache 2 beisst allein (2)", r["rc"] == 2 and "Trade mit" in r["fehler"] and "R86 (d)" in r["fehler"], (r["rc"], r["fehler"]))
    gefunden, verletzt, versuche = None, [], 0
    if bot.startswith("elliott"):   # Tatsachennotiz (OHNE_R90G): Tag nach einem alten Einstieg; kein Einstieg davor, alle alten Trades ab dem Tag bleiben
        for sym in ("AAA", "BBB", "CCC"):
            for _, z in b[b["symbol"] == sym].sort_values("entry_time").iterrows():
                if versuche >= 3: break
                tag = z["entry_time"].normalize() + pd.Timedelta(days=1); versuche += 1
                r = lauf(bot, seed, False, "", json.dumps({sym: str(tag.date())})); x = tab(r["liste"])
                if r["rc"] != 0 or x is None: verletzt.append((sym, str(tag.date()), r["rc"], r["fehler"])); continue
                xs = x[x["symbol"] == sym]; alt_ab = b[(b["symbol"] == sym) & (b["entry_time"] >= tag)]
                if (xs["entry_time"].dt.normalize() < tag).any(): verletzt.append((sym, str(tag.date()), "Einstieg davor"))
                if not set(map(tuple, alt_ab[["entry_time", "exit_time"]].astype(str).values)) <= set(map(tuple, xs[["entry_time", "exit_time"]].astype(str).values)):
                    verletzt.append((sym, str(tag.date()), "alter Trade ab Tag fehlt"))
    else:
      for sym in ("AAA", "BBB", "CCC"):
        for _, z in b[b["symbol"] == sym].sort_values("entry_time").iterrows():
            tag = z["entry_time"].normalize() + pd.Timedelta(days=1)
            if not tag < z["exit_time"] or versuche >= 14: continue
            versuche += 1; r = lauf(bot, seed, False, "", json.dumps({sym: str(tag.date())})); x = tab(r["liste"])
            if r["rc"] != 0 or x is None: verletzt.append((sym, str(tag.date()), r["rc"], r["fehler"])); continue
            xs = x[x["symbol"] == sym]
            if (xs["entry_time"].dt.normalize() < tag).any(): verletzt.append((sym, str(tag.date()), "Einstieg davor"))
            alt = set(b[b["symbol"] == sym]["entry_time"]); neu = xs[(xs["entry_time"] >= tag) & (xs["entry_time"] <= z["exit_time"]) & ~xs["entry_time"].isin(alt)]
            if len(neu): gefunden = (sym, str(tag.date()), "alte Position bis %s" % z["exit_time"], "verdraengter Einstieg %s" % neu["entry_time"].min()); break
        if gefunden: break
    if bot in OHNE_R90G:
        pruefe(bot + ": 3a R90 (g) Tatsachennotiz: " + OHNE_R90G[bot], gefunden is None and not verletzt and versuche > 0, "%d Versuche, kein verdraengter Einstieg; kein Einstieg vor dem Tag" % versuche)
    else:
        pruefe(bot + ": 3a R90 (g): Tag in offener Position -> kein Einstieg davor, verdraengter zweiter Einstieg erscheint", gefunden is not None and not verletzt, gefunden or ("%d Versuche" % versuche, verletzt[:2]))
    c0 = b[b["symbol"] == "CCC"]
    if len(c0):
        r = lauf(bot, seed, False, "", json.dumps({"CCC": str(c0["entry_time"].min().date())})); x = tab(r["liste"])
        y = x[x["symbol"] == "CCC"].reset_index(drop=True)[["entry_time", "exit_time"]] if x is not None else None
        pruefe(bot + ": 3b spaetes Symbol CCC gleich mit/ohne Schranke", y is not None and y.equals(c0.reset_index(drop=True)[["entry_time", "exit_time"]]), "%s/%d" % (None if y is None else len(y), len(c0)))
    else: pruefe(bot + ": 3b CCC hat Trades", False)
    a = b[b["symbol"] == "AAA"].sort_values("entry_time"); tag = str((a["entry_time"].iloc[len(a) // 2] + pd.Timedelta(days=1)).date())
    r = lauf(bot, seed, False, "schranke_aus", json.dumps({"AAA": tag})); pruefe(bot + ": 4 Gegenprobe R87 (c): Schranke aus -> Wache 3 beisst (2)", r["rc"] == 2 and "R87 (c)" in r["fehler"], (r["rc"], r["fehler"]))
    r = lauf(bot, seed, True, "", "{}", True); x = tab(r["liste"])
    pruefe(bot + ": 5a R81 (h) Symbol SPAET: rc 0, Tag None, nicht in der Liste", r["rc"] == 0 and r["spaet"] is None and x is not None and "SPAET" not in set(x["symbol"]), (r["rc"], r["spaet"], r["fehler"] if r["rc"] else ""))
    r = lauf(bot, seed, True, "schnitt_aus+wache1_aus", "{}", True); pruefe(bot + ": 5b SPAET mit Zeilen ab dem Schnitt geladen, ohne Tag -> R81 (c) beisst (2)", r["rc"] == 2 and "R81 (c)" in r["fehler"], (r["rc"], r["fehler"]))
    pruefe(bot + ": 6 A9 symbol unveraendert, keine positionen.csv", set(b["symbol"].astype(str)) <= {"AAA", "BBB", "CCC", "BTCUSDT"} and not any("positionen" in f for f in B["dateien"]), B["dateien"])
    offen = voll[(voll["entry_time"] < S) & (voll["exit_time"] >= S)]; art = []
    for _, o in offen.iterrows():
        m = b[(b["symbol"] == o["symbol"]) & (b["entry_time"] == o["entry_time"])]
        art.append("kein Trade" if m.empty else "Ausstieg %s (%s)" % (m["exit_time"].iloc[0], m["result"].iloc[0] if "result" in m else "?"))
    pruefe(bot + ": 7 R86 (c): offene Position am Ende von B (%d) nach der Konvention des Signalpfads, keine leere Ausstiegszeit, rc 0" % len(offen),
           B["rc"] == 0 and len(offen) > 0 and not b["exit_time"].isna().any() and (b["exit_time"] < S).all(), art[:2])
    pruefe(bot + ": 8 nur Dateien des Test-Snapshots gelesen (%d read_csv)" % (A["gelesen"] + B["gelesen"]), not A["fremd"] and not B["fremd"] and A["gelesen"] > 0, (A["fremd"] + B["fremd"])[:2])
if __name__ == "__main__":
    if len(sys.argv) == 7 and sys.argv[1] == "--kind":
        kind(*sys.argv[2:]); sys.exit(0)
    for bot in (sys.argv[1:] or BOTS): bot_pruefen(bot)
    print("Ergebnis: %d von %d bestanden" % (n[1], n[0])); sys.exit(0 if n[0] and n[0] == n[1] else 1)

#!/usr/bin/env python3
"""TB-174 (R106 (d), R105 (d); R90 (g), R98 (d), R87 (c), 40.7): Fall nach R90 (g) bei t3_supertrend am Listen-Erzeuger
research/tb24_haltedauern/positionen_holen.py, ueber den Gleichstand (backtest_trend.py Z. 112 "<=", Z. 124 "<"), auf dem Test-Snapshot von
test_listen_erzeuger.py (TB-169, Seed 169, Versatz 0, Snapshot B ohne Zeilen ab dem Schnitt), mit einem Eingriff NUR an der Kopie im
Temp-Ordner (R106 (b)): In die 4h-Reihe von AAA wird ab ANKER ein Kursabschnitt eingesetzt (Kerzen mit open = high = low = close; davor
die Reihe flach bei 100, danach die alte Reihe, auf den Endkurs skaliert):
  Abfall in ND Balken von 100 auf L, dann M Balken konstant L, dann STUFE Balken je +0.4 %. Nach dem Abfall schwingen T3 fast/slow
  (Faktor 0.7) um L: Kreuzen nach oben (R0), nach unten, nach oben (E1, Einstieg, ADX > Schwelle). Ab E1 bleibt T3 fast >= T3 slow;
  bei konstantem Kurs laufen beide auf denselben Gleitkommawert (Gleichstand, fast == slow). Der erste Balken der Stufe (s) bildet
  ein Kreuzen nach oben OHNE vorheriges Kreuzen nach unten (Z. 112 "<=" am Gleichstand, Z. 124 "<" greift nicht).
  Ohne Schranke ist E1 (vor dem Tag) offen, das Kreuzen bei s wird verdraengt (Einstieg nur bei position is None, Z. 111).
  Mit Schranke (Z. 114, i >= erster_einstieg; Tag zwischen E1 und s) entsteht vor dem Tag keine Position, E2 erscheint bei s.
  Ob die Rundung den Gleichstand trifft, haengt von L ab (Gleitkomma-Fixpunkte der EMA-Ketten): die Probe waehlt (ANKER, L) aus einer
  festen Liste als ersten Kandidaten, der am Signalpfad alle Bedingungen erfuellt (wiederholbar, ausgegeben in Pruefung 0b).
Handelscode unveraendert; data/ wird nicht gelesen; geprueft an den AUSGABEN des Erzeugers (t3_supertrend_alle_trades.csv, rc).
   0 Signalpfad (Handwerk, R98 (d) letzter Satz; collect_all_trades mit BTC-Regimefilter): ohne Schranke E1 vor dem Tag, kein Einstieg bei s;
     mit Schranke (entry_cutoff = Tag) kein Einstieg vor dem Tag, E2 bei s
   0b Gleichstand: von E1 bis s-1 nie T3 fast < T3 slow (kein Kreuzen nach unten), fast == slow auf mindestens 60 Balken bis s-1,
     fast > slow bei s, ADX bei s > Schwelle, E1 endet nach s; use_t3_exit im Lauf True (Vorgabe Z. 70, der Erzeuger uebergibt ihn nicht)
   1 Erzeuger mit Schranke (Tag {AAA: Tag}): rc 0, kein Einstieg von AAA vor dem Tag, E2 bei s (entry_price wie am Signalpfad)
   2 Gegenprobe (40.7, R87 (c)): Schranke aus -> Wache R87 (c) beisst an einem Einstieg des eingesetzten Abschnitts vor dem Tag, endet mit 2
   3 Schranke und Wachen aus -> rc 0, E1 vor dem Tag mit Ausstieg nach s (Position ueber den Tag offen), kein Einstieg bei s (verdraengt)
   4 ohne Eingriff (Snapshot wie TB-169), gleicher Tag: AAA ohne Einstieg bei E1 und bei s
   5 BBB/CCC/BTCUSDT mit und ohne Tag fuer AAA gleich
   6 Gegenprobe zur Lage der Schranke (R105 (b), Mutante M1): eine KOPIE von backtest_trend.py im Temp-Ordner mit der Schranke HINTER
     der Zustandsmaschine (Einstieg ohne i >= erster_einstieg, Trades vor dem Tag erst in der Ausgabe gestrichen), im Kindprozess per
     sitecustomize statt des Originals geladen (Marke .benutzt) -> rc 0 und kein Einstieg vor dem Tag, aber E2 fehlt bei s
Aufruf aus der Repo-Wurzel: python3 -B research/tb24_haltedauern/test_t3_verdraengung.py  (rc 0 = alle bestanden)"""
import json, os, sys
HIER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HIER)
import test_listen_erzeuger as tle
BOTS = ["t3_supertrend"]
SEED = (169, 0)
ANKER, WOCHEN = "2024-06-03", 20                    # Kandidaten: ANKER + 0..WOCHEN-1 Wochen (BTC-Regime bei E1 und s)
LS = [63.0, 63.75, 67.25, 68.5, 71.0, 71.25, 67.125, 67.875]   # Kandidaten fuer L (Gleichstand nach Rundung, am Bau gemessen)
ND, M, STUFE = 30, 1200, 6
K4 = ["open", "high", "low", "close"]
_snapshot_alt = tle.snapshot
EINGRIFF = {"an": True}
WAHL = {}
def bauplan(L):
    c = [100.0 - (100.0 - L) * j / ND for j in range(1, ND + 1)] + [float(L)] * M
    s = len(c); c += [L * (1 + 0.004 * j) for j in range(1, STUFE + 1)]
    return c, s
def abschnitt(df, anker, L):
    import numpy as np, pandas as pd
    t = pd.to_datetime(df["open_time"]); c, s = bauplan(L); j = int((t >= pd.Timestamp(anker)).values.argmax()); e = j + len(c)
    df = df.copy(); df.loc[:j - 1, K4] = 100.0
    df.loc[j:e - 1, K4] = np.repeat(np.array(c)[:, None], 4, axis=1)
    fak = c[-1] / float(df["open"].iloc[e]); df.loc[e:, K4] = df.loc[e:, K4].values * fak
    return df, j, j + s
def snapshot(bot, d, ab_schnitt, seed, spaet=False, versatz=0):
    import pandas as pd
    _snapshot_alt(bot, d, ab_schnitt, seed, spaet, versatz)
    if EINGRIFF["an"]:
        f = os.path.join(d, "data", "AAA_%s.csv" % tle.TF.get(bot, "1d"))
        abschnitt(pd.read_csv(f), WAHL["anker"], WAHL["L"])[0].to_csv(f, index=False)
tle.snapshot = snapshot
def module(bot, d):
    import importlib
    pfad = os.path.join(tle.WURZEL, "strategies", bot); st = os.path.join(tle.WURZEL, "strategies") + os.sep
    for m in [m for m, v in list(sys.modules.items()) if os.path.abspath(getattr(v, "__file__", None) or "").startswith(st)]: sys.modules.pop(m, None)
    sys.path[:] = [q for q in sys.path if not q.startswith(st)]; sys.path.insert(0, pfad); os.environ["TB36_BASE_DIR"] = d
    es, mso, bt = (importlib.import_module(x) for x in ("equity_simulation", "multi_symbol_optimise", "backtest_trend"))
    assert os.path.dirname(os.path.abspath(bt.__file__)) == pfad and os.path.dirname(os.path.abspath(mso.__file__)) == pfad
    return es, mso, bt
def kandidat(es, mso, bt, p, btc, anker, L):
    import numpy as np, pandas as pd
    q, j, s = abschnitt(p, anker, L); t = pd.to_datetime(q["open_time"])
    tr = mso.get_trades_for_symbol(q, es.T3_FAST, es.T3_SLOW, es.ADX_THRESHOLD, es.STOP_LOSS_PCT)
    if not len(tr): return None
    et = pd.to_datetime(tr["entry_time"]); inn = tr[(et >= t[j]) & (et <= t[s])]
    if not len(inn): return None
    e1 = int(np.where(t.values == np.datetime64(pd.Timestamp(inn["entry_time"].iloc[-1])))[0][0])
    x = bt.compute_indicators(q, es.T3_FAST, es.T3_SLOW, bt.T3_FACTOR, bt.DI_LENGTH, bt.ADX_LENGTH, bt.ATR_LENGTH, bt.ATR_MULT)
    f, g, adx = x["t3_fast"].to_numpy(), x["t3_slow"].to_numpy(), x["adx"].to_numpy()
    seg = f[e1:s] - g[e1:s]; eq = np.where(seg == 0)[0]
    T = (t[e1] + pd.Timedelta(days=10)).normalize()
    reg = es.filter_trades_by_regime(pd.DataFrame({"entry_time": [t[e1], t[s]], "symbol": "AAA"}), es.compute_btc_regime(btc))
    ok = ((seg >= 0).all() and len(eq) >= 60 and eq[0] + len(eq) == len(seg) and f[s] > g[s] and adx[s] > es.ADX_THRESHOLD
          and pd.Timestamp(inn["exit_time"].iloc[-1]) > t[s] and t[e1] < T <= t[s] and len(reg) == 2)
    if not ok: return None
    return {"anker": anker, "L": L, "q": q, "e1": t[e1], "s": t[s], "tag": str(T.date()), "gleich": int(len(eq)), "adx_s": round(float(adx[s]), 1),
            "aus_e1": pd.Timestamp(inn["exit_time"].iloc[-1]), "abschnitt": sorted(pd.to_datetime(inn["entry_time"]))}
def signalpfad(bot):
    import inspect, tempfile, shutil, pandas as pd
    d = tempfile.mkdtemp()
    try:
        EINGRIFF["an"] = False
        try: snapshot(bot, d, False, SEED[0], False, SEED[1])
        finally: EINGRIFF["an"] = True
        es, mso, bt = module(bot, d); tf = tle.TF.get(bot, "1d")
        p = pd.read_csv(os.path.join(d, "data", "AAA_%s.csv" % tf), parse_dates=["open_time"])
        btc = pd.read_csv(os.path.join(d, "data", "BTCUSDT_%s.csv" % tf), parse_dates=["open_time"])
        w = None
        for k in range(WOCHEN):
            for L in LS:
                w = kandidat(es, mso, bt, p, btc, str((pd.Timestamp(ANKER) + pd.Timedelta(weeks=k)).date()), L)
                if w: break
            if w: break
        if not w: return None
        q = w.pop("q"); T = pd.Timestamp(w["tag"]); WAHL.update(w)
        a0 = es.collect_all_trades({"AAA": q, "BTCUSDT": btc}, es.T3_FAST, es.T3_SLOW, es.ADX_THRESHOLD, es.STOP_LOSS_PCT)
        a1 = es.collect_all_trades({"AAA": q, "BTCUSDT": btc}, es.T3_FAST, es.T3_SLOW, es.ADX_THRESHOLD, es.STOP_LOSS_PCT,
                                   entry_cutoffs={"AAA": T, "BTCUSDT": btc["open_time"].min()})
        w["ohne"], w["mit"] = zeiten(a0, "AAA"), zeiten(a1, "AAA")
        m = a1[(a1["symbol"] == "AAA") & (pd.to_datetime(a1["entry_time"]) == w["s"])] if len(a1) else a1
        w["pe2"] = round(float(m["entry_price"].iloc[0]), 6) if len(m) == 1 else None
        w["use_t3_exit"] = inspect.signature(bt.run_backtest).parameters["use_t3_exit"].default
        w["msO_uebergibt"] = "use_t3_exit" in inspect.getsource(mso.get_trades_for_symbol) or "use_t3_exit" in inspect.getsource(es.collect_all_trades)
        return w
    finally:
        shutil.rmtree(d, ignore_errors=True)
def zeiten(q, sym=None):
    import pandas as pd
    if q is None or not len(q): return set()
    if sym is not None: q = q[q["symbol"] == sym]
    return set(pd.to_datetime(q["entry_time"]))
GLEICH = ["symbol", "entry_time", "exit_time", "result", "pnl_pct"]
NAMEN = ["0 Signalpfad", "0b Gleichstand", "1 Erzeuger mit Schranke", "2 Gegenprobe 40.7", "3 Schranke und Wachen aus", "4 ohne Eingriff", "5 BBB/CCC/BTCUSDT gleich", "6 Mutante M1"]
def bot_pruefen(bot):
    import pandas as pd
    w = signalpfad(bot)
    if not w:
        for n in NAMEN: tle.pruefe(bot + ": " + n, False, "kein Kandidat (ANKER, L) erfuellt die Bedingungen am Signalpfad")
        return
    T, e1, s, tag = pd.Timestamp(w["tag"]), w["e1"], w["s"], w["tag"]
    tle.pruefe(bot + ": 0 Signalpfad: ohne Schranke E1 (%s) vor dem Tag %s, kein Einstieg bei s (%s); mit Schranke kein Einstieg vor dem Tag, E2 bei s" % (e1, tag, s),
               e1 in w["ohne"] and s not in w["ohne"] and s in w["mit"] and not any(x < T for x in w["mit"]), (sorted(map(str, w["ohne"] & {e1, s})), sorted(map(str, w["mit"] & {e1, s}))))
    tle.pruefe(bot + ": 0b Gleichstand: E1 bis s-1 fast >= slow, fast == slow auf %d Balken bis s-1, fast > slow bei s, ADX %s; use_t3_exit %s, vom Erzeuger nicht uebergeben" % (w["gleich"], w["adx_s"], w["use_t3_exit"]),
               w["use_t3_exit"] is True and not w["msO_uebergibt"] and w["aus_e1"] > s,
               "ANKER %s, L %s, Abschnitt-Einstiege ohne Schranke %s, Ausstieg E1 %s" % (w["anker"], w["L"], [str(x) for x in w["abschnitt"]], w["aus_e1"]))
    tg = json.dumps({"AAA": tag})
    r = tle.lauf(bot, SEED, False, "", tg); a = tle.tab(r["liste"])
    aa = a[a["symbol"] == "AAA"] if a is not None else None; ein = zeiten(a, "AAA")
    tle.pruefe(bot + ": 1 Erzeuger mit Schranke: rc 0, kein Einstieg von AAA vor dem Tag, E2 erscheint bei s",
               r["rc"] == 0 and aa is not None and not (aa["entry_time"] < T).any() and s in ein and e1 not in ein
               and w["pe2"] is not None and (aa[aa["entry_time"] == s]["entry_price"].round(6) == w["pe2"]).all(), (r["rc"], r["fehler"] if r["rc"] else sorted(map(str, ein & {e1, s}))))
    r2 = tle.lauf(bot, SEED, False, "schranke_aus", tg)
    vor = [x for x in w["ohne"] if x < T and x >= w["abschnitt"][0]]
    tle.pruefe(bot + ": 2 Gegenprobe 40.7: Schranke aus -> Wache R87 (c) beisst an einem Einstieg des Abschnitts vor dem Tag (%s) mit 2" % ", ".join(map(str, sorted(vor))),
               r2["rc"] == 2 and "R87 (c)" in r2["fehler"] and any(("Einstieg %s vor dem Handelbar-Tag %s bei AAA" % (x, tag)) in r2["fehler"] for x in vor), (r2["rc"], r2["fehler"]))
    r3 = tle.lauf(bot, SEED, False, "schranke_aus+wachen_aus", tg); c = tle.tab(r3["liste"]); ec = zeiten(c, "AAA")
    c1 = c[(c["symbol"] == "AAA") & (c["entry_time"] == e1)] if c is not None else None
    tle.pruefe(bot + ": 3 Schranke und Wachen aus: E1 vor dem Tag, Ausstieg nach s, Einstieg bei s fehlt (verdraengt)",
               r3["rc"] == 0 and e1 in ec and s not in ec and c1 is not None and len(c1) == 1 and c1["exit_time"].iloc[0] > s,
               (r3["rc"], sorted(map(str, ec & {e1, s})), None if c1 is None or not len(c1) else str(c1["exit_time"].iloc[0])))
    EINGRIFF["an"] = False
    try: r4 = tle.lauf(bot, SEED, False, "", tg)
    finally: EINGRIFF["an"] = True
    eo = zeiten(tle.tab(r4["liste"]), "AAA")
    tle.pruefe(bot + ": 4 ohne Eingriff (Snapshot TB-169): AAA ohne Einstieg bei E1 und bei s", r4["rc"] == 0 and not (eo & {e1, s}), (r4["rc"], sorted(map(str, eo & {e1, s}))))
    r5 = tle.lauf(bot, SEED, False, "", "{}"); g = tle.tab(r5["liste"])
    gl = lambda q: q[q["symbol"] != "AAA"][GLEICH].reset_index(drop=True).to_csv(index=False) if q is not None else None
    tle.pruefe(bot + ": 5 BBB/CCC/BTCUSDT mit und ohne Tag fuer AAA gleich", r5["rc"] == 0 and a is not None and gl(a) == gl(g), r5["rc"])
    r6, benutzt = m1_lauf(bot, tg); m = tle.tab(r6["liste"]); em = zeiten(m, "AAA")
    tle.pruefe(bot + ": 6 Mutante M1 (Kopie von backtest_trend.py, Schranke hinter der Zustandsmaschine): kein Einstieg vor dem Tag, aber E2 fehlt bei s - die Probe 1 schlaegt an",
               benutzt and r6["rc"] == 0 and m is not None and s not in em and not any(x < T for x in em), (benutzt, r6["rc"], r6["fehler"] if r6["rc"] != 0 else sorted(map(str, em & {e1, s}))))
SITE = """import importlib.abc, importlib.util, os, sys
_m = os.environ.get("TB174_M1")
if _m:
    class _Finder(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path=None, target=None):
            if name != "backtest_trend": return None
            open(_m + ".benutzt", "w").write("ja")
            return importlib.util.spec_from_file_location("backtest_trend", _m)
    sys.meta_path.insert(0, _Finder())
"""
def m1_lauf(bot, tg):
    """M1 nur an einer Kopie im Temp-Ordner: Einstieg ohne Schranke, Trades vor dem Tag erst in der Ausgabe gestrichen."""
    import tempfile, shutil
    qd = os.path.join(tle.WURZEL, "strategies", bot); q = os.path.join(qd, "backtest_trend.py"); s = open(q, encoding="utf-8").read()
    ers = [(" and vwap_ok and i >= erster_einstieg:", " and vwap_ok:"),
           ("    return pd.DataFrame(trades)\n\n\ndef print_summary", "    trades = [x for x in trades if entry_cutoff is None or pd.Timestamp(x[\"entry_time\"]) >= pd.Timestamp(entry_cutoff)]\n"
            "    return pd.DataFrame(trades)\n\n\ndef print_summary"),
           ("_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))", "_STRATEGY_DIR = %r" % qd)]
    if not all(s.count(a) == 1 for a, b in ers): return {"rc": None, "liste": None, "fehler": "M1: Stelle in backtest_trend.py nicht genau einmal"}, False
    for a, b in ers: s = s.replace(a, b)
    t = tempfile.mkdtemp(); m = os.path.join(t, "m1_backtest_trend.py"); open(m, "w", encoding="utf-8").write(s)
    open(os.path.join(t, "sitecustomize.py"), "w", encoding="utf-8").write(SITE)
    vorher = {k: os.environ.get(k) for k in ("PYTHONPATH", "TB174_M1")}
    os.environ["PYTHONPATH"] = t + (os.pathsep + vorher["PYTHONPATH"] if vorher["PYTHONPATH"] else ""); os.environ["TB174_M1"] = m
    try:
        r = tle.lauf(bot, SEED, False, "", tg); return r, os.path.exists(m + ".benutzt")
    finally:
        for k, v in vorher.items():
            if v is None: os.environ.pop(k, None)
            else: os.environ[k] = v
        shutil.rmtree(t, ignore_errors=True)
if __name__ == "__main__":
    for bot in (sys.argv[1:] or BOTS): bot_pruefen(bot)
    print("Ergebnis: %d von %d bestanden" % (tle.n[1], tle.n[0])); sys.exit(0 if tle.n[0] and tle.n[0] == tle.n[1] else 1)

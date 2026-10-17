#!/usr/bin/env python3
"""TB-171 (R105 (c) Weg 1; R90 (g), R98 (d), R87 (c), 40.7): Fall nach R90 (g) bei elliott_wave und elliott_wave_stocks am
Listen-Erzeuger research/tb24_haltedauern/positionen_holen.py, auf dem Test-Snapshot von test_listen_erzeuger.py (TB-169, Seed 169,
Versatz 0, Snapshot B ohne Zeilen ab dem Schnitt), mit einem Eingriff NUR an der Kopie im Temp-Ordner: In die Reihe von AAA wird ein
Kursabschnitt eingesetzt (danach die alte Reihe, auf den Endkurs skaliert), der den Fall herbeifuehrt (R81 (h), R75 (f)):
  Welle W (bearish, Pivots P0..P5 = 100, 80, 91, 60, 69, 21; Fib-Score 1.0) wird am Balken k+1 bestaetigt (Lauf r0 = k+1); die Welle
  C2 (P2..P7 = 91, 60, 69, 21, 30, 26; gueltig, Score 0.33) wird am Balken k+4 bestaetigt (Lauf r1 = k+4, frisch fuer W: r1 - Pivot(P5)
  = 4 <= SIGNAL_FRESHNESS_BARS 5 bzw. 48). remove_overlapping behaelt W (Score 1.0 > 0.33). Handelbar-Tag von AAA = Tag des Balkens k+2.
  Ohne Schranke steigt W bei r0 ein (vor dem Tag), traded haelt ihr end_time, bei r1 wird W verdraengt (elliott_wave_counter.py Z. 352-353,
  363). Mit Schranke (Z. 361, vor traded.add) wird W bei r0 gesperrt und steigt bei r1 ein (am Tag oder spaeter).
Handelscode unveraendert; data/ wird nicht gelesen; geprueft an den AUSGABEN des Erzeugers (<bot>_alle_trades.csv, rc).
   0 Herbeifuehrung am Signalpfad (Handwerk, R98 (d) letzter Satz): ohne entry_cutoff W-Einstieg bei k+1, mit entry_cutoff = Tag bei k+4
   1 Erzeuger mit Schranke (Tag {AAA: Tag}): rc 0, kein Einstieg von AAA vor dem Tag, W erscheint mit Einstieg k+4 (der zweite Einstieg)
   2 Gegenprobe (40.7, R87 (c)): Schranke aus -> Wache R87 (c) beisst an W (Einstieg k+1) und endet mit 2 (die Reihe AAA ist vor dem
     Abschnitt flach: kein anderer Einstieg vor dem Tag)
   3 Gegenprobe ohne Wachen: Schranke und Wachen aus -> rc 0, W mit Einstieg k+1 vor dem Tag und Ausstieg am Tag oder spaeter
     (Position ueber den Tag offen, R90 (g)), kein Einstieg bei k+4 (verdraengt)
   4 Gegenprobe zur Herbeifuehrung: ohne Eingriff (Snapshot wie TB-169) und gleichem Tag hat AAA weder bei k+1 noch bei k+4 einen Einstieg
   5 Probe nach 1 auch fuer BBB/CCC: Ausgaben ohne AAA mit und ohne Tag fuer AAA gleich
   6 Gegenprobe zur Lage der Schranke (R105 (b), Mutante M1): eine KOPIE des Counters im Temp-Ordner mit der Schranke HINTER
     traded.add (per sitecustomize im Kindprozess statt des Originals geladen, Marke .benutzt) -> W fehlt bei k+4, kein Einstieg vor dem Tag
   W wird am Signalpfad ueber signal_time (= Pivot P5) und fib_score 1.0 erkannt, am Erzeuger ueber entry_time und entry_price
Aufruf aus der Repo-Wurzel: python3 -B research/tb24_haltedauern/test_elliott_verdraengung.py [bot ...]  (rc 0 = alle bestanden)"""
import json, os, sys
HIER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HIER)
import test_listen_erzeuger as tle
BOTS = ["elliott_wave", "elliott_wave_stocks"]
SEED = (169, 0)
ANKER = "2025-03-03"
WEG = [100, 80, 91, 60, 69, 21]              # Pivots P0..P5 der Welle W (relativ, x Skala)
_snapshot_alt = tle.snapshot
EINGRIFF = {"an": True}
def bauplan():
    """Balkenliste (high, low) relativ; Index von k (Pivot P5) in der Liste. Beine monoton, je Bein 4 Balken."""
    b = []
    def bein(a, z, n=4):
        for j in range(1, n + 1):
            x = a + (z - a) * j / n; b.append((x * 1.001, x * 0.999))
    bein(70, 100)                                    # Anstieg auf P0 (aus 70, d. h. +43 %: P0 ist sicher ein Hoch)
    b[-1] = (100.0, 99.5)
    for a, z in zip(WEG[:-1], WEG[1:]):
        bein(a, z)
        b[-1] = (z * 1.001, z) if z < a else (z, z * 0.999)
    k = len(b) - 1                                   # P5 = 21 (Tief)
    b += [(23.5, 23.0), (30.0, 29.5), (27.0, 26.0), (29.0, 28.0)]   # k+1 bestaetigt P5; k+2 P6=30; k+3 bestaetigt P6, P7=26; k+4 bestaetigt P7
    return b, k
def einsetzen(bot, d):
    import pandas as pd
    tf = tle.TF.get(bot, "1d"); f = os.path.join(d, "data", "AAA_%s.csv" % tf)
    df = pd.read_csv(f); t = pd.to_datetime(df["open_time"]); b, k = bauplan()
    j = int((t >= pd.Timestamp(ANKER)).values.argmax())
    if tf != "1d":                                   # Balken k+2 auf 00:00 legen (min_entry_idx = erster Balken des Tags)
        while t.iloc[j + k + 2].hour != 0: j += 1
    s = float(df["close"].iloc[j - 1]) / 70.0
    df.loc[:j - 1, ["open", "high", "low", "close"]] = 70.0 * s       # vor dem Abschnitt flach: kein Pivot, kein Einstieg vor W
    for i, (h, lo) in enumerate(b):
        m = (h + lo) / 2 * s
        df.loc[j + i, ["open", "high", "low", "close"]] = [m, h * s, lo * s, m]
    e = j + len(b); fak = b[-1][1] * s / float(df["open"].iloc[e])
    for c in ("open", "high", "low", "close"):
        df.loc[e:, c] = df.loc[e:, c] * fak
    df.to_csv(f, index=False)
    return {"k1": str(t.iloc[j + k + 1]), "k4": str(t.iloc[j + k + 4]), "tag": str(t.iloc[j + k + 2].date()), "p5": str(t.iloc[j + k])}
def snapshot(bot, d, ab_schnitt, seed, spaet=False, versatz=0):
    _snapshot_alt(bot, d, ab_schnitt, seed, spaet, versatz)
    if EINGRIFF["an"]:
        x = einsetzen(bot, d); json.dump(x, open(os.path.join(d, "eingriff.json"), "w"))
tle.snapshot = snapshot
def signalpfad(bot):
    import importlib, tempfile, shutil, pandas as pd
    d = tempfile.mkdtemp(); pfad = os.path.join(tle.WURZEL, "strategies", bot)
    st = os.path.join(tle.WURZEL, "strategies") + os.sep   # je Bot frisch: alle Module aus strategies/ aus dem Speicher (live_params, equity_simulation, ...)
    for m in [m for m, v in list(sys.modules.items()) if os.path.abspath(getattr(v, "__file__", None) or "").startswith(st)]: sys.modules.pop(m, None)
    sys.path[:] = [q for q in sys.path if not q.startswith(os.path.join(tle.WURZEL, "strategies") + os.sep)]
    try:
        snapshot(bot, d, False, SEED[0], False, SEED[1]); x = json.load(open(os.path.join(d, "eingriff.json")))
        sys.path.insert(0, pfad); os.environ["TB36_BASE_DIR"] = d
        es = importlib.import_module("equity_simulation"); mso = importlib.import_module("multi_symbol_optimise")
        p = pd.read_csv(os.path.join(d, "data", "AAA_%s.csv" % tle.TF.get(bot, "1d")), parse_dates=["open_time"])
        t0 = mso.get_trades_for_symbol(p, es.DEVIATION_PCT); t1 = mso.get_trades_for_symbol(p, es.DEVIATION_PCT, entry_cutoff=pd.Timestamp(x["tag"]))
        assert os.path.dirname(os.path.abspath(mso.__file__)) == pfad
        w = lambda q, z: q[pd.to_datetime(q["entry_time"]) == pd.Timestamp(x[z])].to_dict("records") if len(q) else []
        return x, zeiten(t0), zeiten(t1), w(t0, "k1"), w(t1, "k4")
    finally:
        shutil.rmtree(d, ignore_errors=True)
def zeiten(q, sym=None):
    import pandas as pd
    if q is None or not len(q): return set()
    if sym is not None: q = q[q["symbol"] == sym]
    return set(pd.to_datetime(q["entry_time"]))
GLEICH = ["symbol", "entry_time", "exit_time", "result", "pnl_pct"]   # ohne trade_zeile/ausgefuehrt: die Zuteilung haengt am Tag von AAA
def bot_pruefen(bot):
    import pandas as pd
    x, e0, e1, w0, w1 = signalpfad(bot); T = pd.Timestamp(x["tag"]); P5 = pd.Timestamp(x["p5"]); k1, k4, tag = pd.Timestamp(x["k1"]), pd.Timestamp(x["k4"]), x["tag"]
    tle.pruefe(bot + ": 0 Signalpfad: ohne Schranke W bei k+1 (%s), mit Schranke ab Tag %s W bei k+4 (%s)" % (k1, tag, k4),
               k1 in e0 and k4 not in e0 and k4 in e1 and k1 not in e1, (sorted(map(str, e0 & {k1, k4})), sorted(map(str, e1 & {k1, k4}))))
    ist_w = lambda r: len(r) == 1 and pd.Timestamp(r[0]["signal_time"]) == P5 and float(r[0]["fib_score"]) == 1.0
    tle.pruefe(bot + ": 0b W ist dieselbe Welle (signal_time = P5 %s, fib_score 1.0), ohne Schranke Ausstieg am Tag oder spaeter" % P5,
               ist_w(w0) and ist_w(w1) and pd.Timestamp(w0[0]["exit_time"]) >= T, [(str(r["signal_time"]), r["fib_score"], str(r["exit_time"])) for r in w0 + w1])
    pw = round(float(w1[0]["entry_price"]), 6) if w1 else None
    tg = json.dumps({"AAA": tag})
    r = tle.lauf(bot, SEED, False, "", tg); a = tle.tab(r["liste"])
    aa = a[a["symbol"] == "AAA"] if a is not None else None; ein = zeiten(a, "AAA")
    tle.pruefe(bot + ": 1 Erzeuger mit Schranke: rc 0, kein Einstieg von AAA vor dem Tag, W erscheint bei k+4",
               r["rc"] == 0 and aa is not None and not (aa["entry_time"] < T).any() and k4 in ein and k1 not in ein
               and pw is not None and (aa[aa["entry_time"] == k4]["entry_price"].round(6) == pw).all(), (r["rc"], r["fehler"] if r["rc"] else sorted(map(str, ein & {k1, k4}))))
    r2 = tle.lauf(bot, SEED, False, "schranke_aus", tg)
    tle.pruefe(bot + ": 2 Gegenprobe 40.7: Schranke aus -> Wache R87 (c) beisst an W (Einstieg k+1 %s) mit 2" % k1, r2["rc"] == 2 and "R87 (c)" in r2["fehler"]
               and ("Einstieg %s vor dem Handelbar-Tag" % k1) in r2["fehler"], (r2["rc"], r2["fehler"]))
    r3 = tle.lauf(bot, SEED, False, "schranke_aus+wachen_aus", tg); c = tle.tab(r3["liste"])
    ec = zeiten(c, "AAA")
    c1 = c[(c["symbol"] == "AAA") & (c["entry_time"] == k1)] if c is not None else None
    tle.pruefe(bot + ": 3 Schranke und Wachen aus: W bei k+1 vor dem Tag, Ausstieg am Tag oder spaeter, Einstieg bei k+4 fehlt (verdraengt)",
               r3["rc"] == 0 and k1 in ec and k4 not in ec and c1 is not None and len(c1) == 1 and c1["exit_time"].iloc[0] >= T,
               (r3["rc"], sorted(map(str, ec & {k1, k4})), None if c1 is None or not len(c1) else str(c1["exit_time"].iloc[0])))
    EINGRIFF["an"] = False
    try: r4 = tle.lauf(bot, SEED, False, "", tg)
    finally: EINGRIFF["an"] = True
    o = tle.tab(r4["liste"]); eo = zeiten(o, "AAA")
    tle.pruefe(bot + ": 4 ohne Eingriff (Snapshot TB-169): AAA ohne Einstieg bei k+1 und k+4", r4["rc"] == 0 and not (eo & {k1, k4}), (r4["rc"], sorted(map(str, eo & {k1, k4}))))
    r5 = tle.lauf(bot, SEED, False, "", "{}"); g = tle.tab(r5["liste"])
    gl = lambda q: q[q["symbol"] != "AAA"][GLEICH].reset_index(drop=True).to_csv(index=False) if q is not None else None
    tle.pruefe(bot + ": 5 BBB/CCC mit und ohne Tag fuer AAA gleich", r5["rc"] == 0 and a is not None and gl(a) == gl(g), r5["rc"])
    r6, benutzt = m1_lauf(bot, tg); m = tle.tab(r6["liste"]); em = zeiten(m, "AAA")
    tle.pruefe(bot + ": 6 Mutante M1 (Kopie des Counters, Schranke hinter traded.add): W fehlt bei k+4 - die Probe 1 schlaegt an",
               benutzt and r6["rc"] == 0 and m is not None and k4 not in em and not any(q < T for q in em), (benutzt, r6["rc"], r6["fehler"] if r6["rc"] != 0 else sorted(map(str, em & {k1, k4}))))
SITE = """import importlib.util, os, sys
_m = os.environ.get("TB171_M1")
if _m:
    _s = importlib.util.spec_from_file_location("elliott_wave_counter", _m); _x = importlib.util.module_from_spec(_s)
    sys.modules["elliott_wave_counter"] = _x; _s.loader.exec_module(_x); open(_m + ".benutzt", "w").write("ja")
"""
def m1_lauf(bot, tg):
    """M1 nur an einer Kopie im Temp-Ordner: Schranke hinter traded.add; der Kindprozess laedt die Kopie ueber sitecustomize (PYTHONPATH)."""
    import tempfile, shutil
    q = os.path.join(tle.WURZEL, "strategies", bot, "elliott_wave_counter.py"); s = open(q, encoding="utf-8").read()
    alt = "            if min_entry_idx is not None and run_bar < min_entry_idx:\n                continue\n            traded.add(end_time)\n"
    neu = "            traded.add(end_time)\n            if min_entry_idx is not None and run_bar < min_entry_idx:\n                continue\n"
    e1, e2 = "_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))", "get_strategy_paths(__file__)"
    if not (s.count(alt) == 1 and s.count(e1) == 1 and s.count(e2) == 1): return {"rc": None, "liste": None, "fehler": "M1: Stelle im Counter nicht genau einmal"}, False
    s = s.replace(alt, neu).replace(e1, "_STRATEGY_DIR = %r" % os.path.dirname(q)).replace(e2, "get_strategy_paths(%r)" % q)
    t = tempfile.mkdtemp(); m = os.path.join(t, "m1_elliott_wave_counter.py"); open(m, "w", encoding="utf-8").write(s)
    open(os.path.join(t, "sitecustomize.py"), "w", encoding="utf-8").write(SITE)
    vorher = {k: os.environ.get(k) for k in ("PYTHONPATH", "TB171_M1")}
    os.environ["PYTHONPATH"] = t + (os.pathsep + vorher["PYTHONPATH"] if vorher["PYTHONPATH"] else ""); os.environ["TB171_M1"] = m
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

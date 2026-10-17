#!/usr/bin/env python3
"""TB-176a E2 Probe (Anhang E): die zwei umgestellten Leser an einer Kopie mit kleinen <bot>_alle_trades.csv (R107 (e)).
Aufruf aus der Repo-Wurzel; schreibt nur in einen Temp-Ordner; liest keine Kurse. Gegenprobe: die Fassung am HEAD (git show) liest
<bot>_positionen.csv und scheitert an derselben Kopie. Rueckgabe 0 = alle ja."""
import csv, datetime as dt, json, os, shutil, subprocess, sys, tempfile, types
sys.dont_write_bytecode = True
TB, FN = "research/tb24_haltedauern/", "research/faltenplan_neun/"
BOTS = [("elliott_wave", "krypto", "4h"), ("t3_supertrend", "krypto", "4h"), ("rsi2_crypto", "krypto", "1d"), ("turtle_soup_crypto", "krypto", "1d"), ("volatility_breakout_crypto", "krypto", "1d"),
        ("elliott_wave_stocks", "aktien", "1d"), ("rsi2_mean_reversion", "aktien", "1d"), ("turtle_soup_stocks", "aktien", "1d"), ("volatility_breakout", "aktien", "1d")]
TAGE = [1, 2, 3, 4, 10, 6]                       # Haltedauern in Tagen; Zeile 3 und 4 "nicht ausgefuehrt"
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def liste(pfad, mit_spalte):
    k = ["trade_zeile", "symbol", "entry_time", "exit_time", "result", "pnl_pct", "entry_price", "exit_price", "kerzen"] + (["ausgefuehrt"] if mit_spalte else [])
    with open(pfad, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(k)
        for i, d in enumerate(TAGE):
            ein = dt.datetime(2022, 1, 3) + dt.timedelta(days=11 * i)
            w.writerow([i, "AAA" if i % 2 else "BBB", ein, ein + dt.timedelta(days=d), "time_exit", 1.0, 10.0, 10.1, d] + ([str(i not in (2, 3))] if mit_spalte else []))
def meta(pfad, bot, kl, tf):
    json.dump({"bot": bot, "zeitrahmen": tf, "anlageklasse": kl, "trades_gefunden": len(TAGE), "symbole_gefunden": 2, "symbole_geladen": 2,
               "erster_einstieg": "2022-01-03 00:00:00", "letzter_ausstieg": "2022-03-05 00:00:00", "ausstiegsarten": {"time_exit": len(TAGE)},
               "spalte_result_vorhanden": True, "kerzen_ohne_wert": 0}, open(pfad, "w"), indent=2)
def head(pfad): return subprocess.run(["git", "--no-optional-locks", "show", "HEAD:" + pfad], capture_output=True, check=True).stdout.decode("utf-8")
basis = tempfile.mkdtemp(prefix="tb176a_probe_", dir=os.environ.get("TMPDIR") or None)
# --- Leser 1: tb24_haltedauern/auswertung.py ---------------------------------
for fall in ("neu", "alt"):
    d = os.path.join(basis, "a_" + fall); os.makedirs(d + "/daten")
    shutil.copy(TB + "haltedauer_kern.py", d)
    if fall == "neu": shutil.copy(TB + "auswertung.py", d)
    else: open(d + "/auswertung.py", "w", encoding="utf-8").write(head(TB + "auswertung.py"))
    for n, (bot, kl, tf) in enumerate(BOTS):
        liste(d + "/daten/%s_alle_trades.csv" % bot, n % 2 == 0); meta(d + "/daten/%s_meta.json" % bot, bot, kl, tf)
    r = subprocess.run([sys.executable, "-B", "auswertung.py"], cwd=d, capture_output=True, text=True)
    if fall == "neu":
        p(r.returncode == 0, "auswertung.py (neu) an der Kopie: rc %d %s" % (r.returncode, (r.stderr.strip().split("\n") or [""])[-1][:120]))
        hz = list(csv.DictReader(open(d + "/ergebnisse/haltedauern_je_bot.csv", encoding="utf-8"))) if r.returncode == 0 else []
        p(len(hz) == 9 and all(int(z["n"]) == len(TAGE) for z in hz), "haltedauern_je_bot.csv: je Bot n = %d (alle gefundenen Trades, auch die %d mit ausgefuehrt=False): %s" % (len(TAGE), 2, sorted(set(z["n"] for z in hz))))
        med = sorted(TAGE)[len(TAGE) // 2 - 1:len(TAGE) // 2 + 1]; m = sum(med) / 2.0
        p(all(abs(float(z["tage_median"]) - m) < 1e-9 for z in hz) and hz, "Median je Bot = %.1f Tage (von Hand: Median von %s)" % (m, TAGE))
        zf = json.load(open(d + "/ergebnisse/zusammenfassung.json", encoding="utf-8")) if r.returncode == 0 else {"datenbasis": {}}
        db = zf["datenbasis"]
        p(len(db) == 9 and all("trades_ausgefuehrt" not in v and "symbole_ausgefuehrt" not in v and v.get("symbole_gefunden") == 2 and v.get("trades_gefunden") == len(TAGE) for v in db.values()),
          "zusammenfassung.json: datenbasis ohne trades_/symbole_ausgefuehrt, mit trades_gefunden %d und symbole_gefunden 2" % len(TAGE))
        p(r.returncode == 0 and not os.path.exists(d + "/ergebnisse/gegenprobe_positionslimit.csv"), "gegenprobe_positionslimit.csv entfallen (haengt an ausgefuehrt)")
    else:
        p(r.returncode != 0 and "_positionen.csv" in r.stderr, "Gegenprobe: auswertung.py am HEAD scheitert an derselben Kopie (liest <bot>_positionen.csv): rc %d" % r.returncode)
# --- Leser 2: faltenplan_neun/embargo_neun.py --------------------------------
sys.path.insert(0, os.path.abspath(FN))
for fall in ("neu", "alt"):
    b = os.path.join(basis, "e_" + fall); os.makedirs(b + "/" + TB + "daten"); liste(b + "/" + TB + "daten/t3_supertrend_alle_trades.csv", True)
    mod = types.ModuleType("embargo_" + fall); mod.__file__ = os.path.abspath(FN + "embargo_neun.py")
    quelle = open(FN + "embargo_neun.py", encoding="utf-8").read() if fall == "neu" else head(FN + "embargo_neun.py")
    exec(compile(quelle, mod.__file__, "exec"), mod.__dict__)
    try:
        w = sorted(mod.haltedauern_tage("t3_supertrend", b)); e = mod.embargo_fuer_bot("t3_supertrend", b); fehler = None
    except Exception as x:
        w, e, fehler = None, None, x
    if fall == "neu":
        p(w == sorted(float(x) for x in TAGE), "embargo_neun.haltedauern_tage (neu): alle %d gefundenen Trades %s" % (len(TAGE), w))
        q = (len(TAGE) - 1) * 0.95; s = sorted(TAGE); p95 = s[int(q)] + (q - int(q)) * (s[int(q) + 1] - s[int(q)])
        p(e is not None and e["art"] == "perzentil" and e["perzentil95"]["n_trades_gefunden"] == len(TAGE) and e["perzentil95"]["herkunft"].endswith("t3_supertrend_alle_trades.csv")
          and abs(e["perzentil95"]["p95_tage"] - p95) < 1e-9 and e["embargo_handelstage"] == int(-(-p95 // 1)) + 1,
          "embargo_fuer_bot(t3_supertrend): P95 %.4f (von Hand), Embargo %s = aufgerundet + 1, n_trades_gefunden %s, herkunft alle_trades" % (p95, e and e["embargo_handelstage"], e and e["perzentil95"]["n_trades_gefunden"]))
    else:
        p(isinstance(fehler, FileNotFoundError) and "_positionen.csv" in str(fehler), "Gegenprobe: embargo_neun.py am HEAD scheitert an derselben Kopie (liest <bot>_positionen.csv): %s" % type(fehler).__name__)
print("Kopie: %s" % basis); print("\n".join(OUT)); n = sum(l.startswith("ja") for l in OUT)
print("Ergebnis: %d von %d bestanden" % (n, len(OUT))); sys.exit(0 if n == len(OUT) else 1)

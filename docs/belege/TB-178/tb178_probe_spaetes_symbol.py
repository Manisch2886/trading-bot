#!/usr/bin/env python3
"""TB-178 Probe nach R110 (a) (R109 (b), R108 (e), R107 (b), R106 (b)): der herbeigefuehrte spaete Symbolfall, Abnahme am Erzeuger
(research/tb24_haltedauern/positionen_holen.py, gestartet ueber test_listen_erzeuger.lauf in einem Temp-Ordner).
Snapshot (synthetisch, kein data/ des Repos): AAA, BBB, CCC (+ BTCUSDT bei Krypto) ab Achsenbeginn, SPAET mit spaetem Datenbeginn
(vor dem Schnitt). Der Handelbar-Tag jedes Symbols kommt aus der Rechnung nach 23.5 (faltenschranke_messung.handelbar_ab, R87 (a)) -
die Probe setzt KEINEN Tag (tags "{}"). Bedingung des Falls (R110 (a)): kein Symbol traegt vor seinem Tag ein Signal - bis zum
gerechneten Tag ein ruhiger, gleichmaessig fallender Vorlauf, ab dem Tag Zufallsweg (Seed). Je Bot, Wachen nach R86 (d) und R87 (c) an:
  S = Schranke am Tag (Modus "")   O = ohne Schranke (Modus "schranke_aus": hole_trades ohne handelbar)
Je Bot 6 Pruefungen: 1 Tage gerechnet, SPAET-Tag vor dem Schnitt und nach den Tagen der uebrigen; der Lauf nutzte die Rechnung
2 rc S = rc O = 0   3 Ausgaben bytegleich   4 Zaehlzeile entfernt 0 / nur in S 0; SPAET hat Trades, keiner vor seinem Tag
5 Lesehaken (nur Snapshot-Dateien)   6 Gegenprobe beide Seiten (40.7, 41.1 A5, R110 (a)): SPAET ohne ruhigen Vorlauf (Signal vor dem Tag) ->
  ohne Schranke rc 2 (R87 (c)); mit Schranke rc 0 und Zaehlzeile ueber 0 (Zeilen, die die Schranke gegenueber einem Lauf ohne Schranke
  und ohne Wachen entfernt).
Aufruf aus der Repo-Wurzel: <python> -B <diese Datei> [bot ...]  (rc 0 = alle bestanden; Soll 18 von 18)"""
import json, os, subprocess, sys
WURZEL = os.getcwd(); sys.path.insert(0, os.path.join(WURZEL, "research", "tb24_haltedauern"))
import numpy as np, pandas as pd
import test_listen_erzeuger as tle
SEED = int(os.environ.get("R109B_SEED", "178"))
START = {"1d": "2023-01-02", "4h": "2023-06-01", "1h": "2024-06-01", "aktien": "2019-01-02"}
MODUS = {"vorlauf": True}
def tage(bot, d):
    c = ("import sys, json; sys.path.insert(0, 'research/faltenplan_neun'); import faltenschranke_messung as f; "
         "print(json.dumps(f.handelbar_ab(%r)))" % bot)
    r = subprocess.run([sys.executable, "-B", "-c", c], cwd=WURZEL, capture_output=True, text=True, env=dict(os.environ, TB36_BASE_DIR=d))
    if r.returncode: raise SystemExit("Rechnung 23.5: rc %s %s" % (r.returncode, r.stderr[-300:]))
    return json.loads(r.stdout.strip().split("\n")[-1])
def snapshot(bot, d, ab_schnitt, seed, spaet=False, versatz=0):
    tf = tle.TF.get(bot, "1d"); t = tle.achse(bot, versatz); ak = bot in tle.AKTIEN
    syms = ["AAA", "BBB", "CCC"] + ([] if ak else ["BTCUSDT"]) + ["SPAET"]
    for u in ("data", "config", "strategies/" + bot, "research"): os.makedirs(os.path.join(d, u), exist_ok=True)
    import shutil; shutil.copy(os.path.join(WURZEL, "strategies", bot, "multi_symbol_optimise.py"), os.path.join(d, "strategies", bot))
    os.symlink(os.path.join(WURZEL, "research", "universum_trockenlauf"), os.path.join(d, "research", "universum_trockenlauf"))
    open(os.path.join(d, "config", "top25_symbols.txt"), "w").write("" if ak else "\n".join(syms) + "\n")
    open(os.path.join(d, "config", "sp500_top150.txt"), "w").write("\n".join(syms) + "\n" if ak else "")
    st = pd.Timestamp(START["aktien" if ak else tf]); fmt = "%Y-%m-%d" if tf == "1d" else "%Y-%m-%d %H:%M:%S"
    tt = {s: t[(t < pd.Timestamp(tle.SCHNITT)) | bool(ab_schnitt)] for s in syms}; tt["SPAET"] = tt["SPAET"][tt["SPAET"] >= st]
    def schreibe(s, c, o, h, lo, vol):
        pd.DataFrame({"open_time": tt[s].strftime(fmt), "open": o, "high": h, "low": lo, "close": c, "volume": vol}).to_csv(
            os.path.join(d, "data", "%s_%s.csv" % (s, tf)), index=False)
    for s in syms: n = len(tt[s]); schreibe(s, *([np.ones(n)] * 4), np.full(n, 10**5))   # nur Zeitachse: die Rechnung liest Zeitstempel
    tg = tage(bot, d); json.dump(tg, open(os.path.join(d, "tage_rechnung.json"), "w"))
    for k, s in enumerate(syms):
        r = np.random.default_rng(seed + k); v = 0.012 if tf != "1d" else 0.025; n = len(tt[s])
        ruhig = (tt[s].normalize() < pd.Timestamp(tg[s])) if (tg.get(s) and (MODUS["vorlauf"] or s != "SPAET")) else np.zeros(n, bool)
        sch = r.normal(0.0001, v, n); sch[ruhig] = -0.0005
        c = 50 * np.exp(np.cumsum(sch)); o = c * (1 + np.where(ruhig, 0.0005, r.normal(0, v / 5, n)))
        h = np.maximum(o, c) * (1 + np.where(ruhig, 0.0002, np.abs(r.normal(0, v / 3, n))))
        lo = np.minimum(o, c) * (1 - np.where(ruhig, 0.0002, np.abs(r.normal(0, v / 3, n))))
        schreibe(s, c, o, h, lo, r.integers(10**5, 10**6, n))
tle.snapshot = snapshot
n = [0, 0]
def pruefe(t, ok, info=""):
    n[0] += 1; n[1] += bool(ok); print(("ja    " if ok else "NEIN  ") + t + (" · " + str(info) if info else ""), flush=True); return ok
def zeilen(liste): return set(liste.split("\n")[1:]) - {""} if liste else set()
for bot in (sys.argv[1:] or ["t3_supertrend", "elliott_wave", "elliott_wave_stocks"]):
    sd = (SEED, 0); MODUS["vorlauf"] = True
    S, O = tle.lauf(bot, sd, False, "", "{}"), tle.lauf(bot, sd, False, "schranke_aus", "{}")
    import tempfile
    with tempfile.TemporaryDirectory() as d: snapshot(bot, d, False, SEED); tg = json.load(open(os.path.join(d, "tage_rechnung.json")))
    sp = tg.get("SPAET"); andere = [v for k, v in tg.items() if k != "SPAET"]
    pruefe(bot + ": 1 Tage aus der Rechnung nach 23.5, kein Tag gesetzt; SPAET %s vor dem Schnitt und nach den uebrigen (%s); Lauf nutzte die Rechnung (spur %s)" % (sp, max(andere) if andere and None not in andere else andere, S["spaet"]),
           sp is not None and sp < tle.SCHNITT and None not in andere and sp > max(andere) and S["spaet"] == sp == O["spaet"])
    pruefe(bot + ": 2 rc S %s, rc O %s (Wachen R86 (d), R87 (c) an)" % (S["rc"], O["rc"]), S["rc"] == 0 and O["rc"] == 0, (S["fehler"] if S["rc"] else "") + (O["fehler"] if O["rc"] else ""))
    pruefe(bot + ": 3 Ausgaben S und O bytegleich (%s Zeichen)" % len(S["liste"] or ""), S["liste"] is not None and S["liste"] == O["liste"])
    zs, zo = zeilen(S["liste"]), zeilen(O["liste"]); x = tle.tab(S["liste"])
    xs = x[x["symbol"] == "SPAET"] if x is not None else None
    vor = None if xs is None or sp is None else int((xs["entry_time"].dt.normalize() < pd.Timestamp(sp)).sum())
    print("Zaehlzeile %s: Zeilen S %d, O %d; von der Schranke entfernt %d; nur in S %d; SPAET-Trades %s, davon vor dem Tag %s, erster Einstieg %s"
          % (bot, len(zs), len(zo), len(zo - zs), len(zs - zo), None if xs is None else len(xs), vor, None if xs is None or xs.empty else xs["entry_time"].min()), flush=True)
    pruefe(bot + ": 4 Zaehlzeile entfernt 0, nur in S 0; SPAET traegt Trades ab dem Tag, keinen davor", len(zs) > 0 and not (zo - zs) and not (zs - zo) and xs is not None and len(xs) > 0 and vor == 0)
    pruefe(bot + ": 5 Lesehaken: nur Snapshot-Dateien gelesen (S %d, O %d)" % (S["gelesen"], O["gelesen"]), not S["fremd"] and not O["fremd"] and S["gelesen"] > 0 and O["gelesen"] > 0, (S["fremd"] + O["fremd"])[:2])
    MODUS["vorlauf"] = False
    S2, O2, O3 = tle.lauf(bot, sd, False, "", "{}"), tle.lauf(bot, sd, False, "schranke_aus", "{}"), tle.lauf(bot, sd, False, "schranke_aus+wachen_aus", "{}")
    MODUS["vorlauf"] = True
    weg = len(zeilen(O3["liste"]) - zeilen(S2["liste"])) if O3["liste"] and S2["liste"] else None
    print("Zaehlzeile Gegenprobe %s: mit Schranke rc %s, Zeilen %d; ohne Schranke und Wachen Zeilen %d; Zeilen nur ohne Schranke und Wachen %s"
          % (bot, S2["rc"], len(zeilen(S2["liste"])), len(zeilen(O3["liste"])), weg), flush=True)
    pruefe(bot + ": 6 Gegenprobe beide Seiten (40.7, R110 (a)): SPAET mit Signal vor dem Tag -> ohne Schranke rc %s (%s); mit Schranke rc %s, Zaehlzeile (Zeilen nur ohne Schranke) %s"
           % (O2["rc"], O2["fehler"][:90] if O2["rc"] else "kein Abbruch", S2["rc"], weg), O2["rc"] == 2 and "R87 (c)" in O2["fehler"] and S2["rc"] == 0 and bool(weg))
print("Ergebnis: %d von %d bestanden" % (n[1], n[0])); sys.exit(0 if n[0] and n[0] == n[1] else 1)

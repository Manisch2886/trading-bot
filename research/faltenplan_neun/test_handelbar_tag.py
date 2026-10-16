#!/usr/bin/env python3
"""TB-166 (E-3a; R87 (a)/(c), R90 (e)): faltenschranke_messung.handelbar_ab - EINE Rechnung des
Handelbar-Tags je Symbol, an der Reihe ohne Zeilen ab dem Schnitt. Synthetisch: Ersatzwurzel im
Temp-Ordner (TB36_BASE_DIR) mit eigenen Universen und Kursdateien; data/ wird nicht gelesen.
Aufruf aus der Repo-Wurzel: python3 -B research/faltenplan_neun/test_handelbar_tag.py  (rc 0 = alle bestanden)"""
import datetime as dt, os, shutil, subprocess, sys, tempfile
WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
S = dt.date(2026, 9, 1)
KIND = r'''
import sys, json, datetime as dt
sys.path.insert(0, sys.argv[1]); import faltenschranke_messung as f
aus = {b: f.handelbar_ab(b) for b in ("elliott_wave", "rsi2_crypto", "t3_supertrend", "rsi2_mean_reversion")}
aus["lesart_gleich"] = {b: f.loader_lesart(b)["handelbar_ab"] == aus[b] for b in ("elliott_wave", "rsi2_crypto", "rsi2_mean_reversion")}
aus["ohne_schnitt"] = f.handelbar_ab("rsi2_crypto", schnitt=dt.date(2100, 1, 1))
print(json.dumps(aus))
'''
def baue(d, ab_schnitt):
    for b in ("elliott_wave", "rsi2_crypto", "t3_supertrend", "rsi2_mean_reversion"):
        os.makedirs(os.path.join(d, "strategies", b))
        shutil.copy(os.path.join(WURZEL, "strategies", b, "multi_symbol_optimise.py"), os.path.join(d, "strategies", b))
    os.makedirs(os.path.join(d, "config")); os.makedirs(os.path.join(d, "data"))
    open(os.path.join(d, "config", "top25_symbols.txt"), "w").write("AAA\nSPAET\nKURZ\n")
    open(os.path.join(d, "config", "sp500_top150.txt"), "w").write("XX\nFEHLT\n")
    def schreibe(name, start, schritt, n):
        z = ["open_time,open,high,low,close,volume"]; t = start
        while len(z) <= n:
            if ab_schnitt or t.date() < S: z.append("%s,1,1,1,1,1" % t.strftime("%Y-%m-%d %H:%M:%S"))
            elif not ab_schnitt: break
            t += schritt
        open(os.path.join(d, "data", name), "w").write("\n".join(z) + "\n")
    tag, std = dt.timedelta(days=1), dt.timedelta(hours=1)
    schreibe("AAA_1d.csv", dt.datetime(2020, 1, 1), tag, 2500)            # 500 Tage nach 2020-01-01: 2021-05-15
    schreibe("SPAET_1d.csv", dt.datetime(2025, 6, 1), tag, 600)           # +500 Tage = 2026-10-14 >= Schnitt -> None
    schreibe("KURZ_1d.csv", dt.datetime(2026, 8, 1), tag, 10)
    schreibe("AAA_4h.csv", dt.datetime(2023, 1, 1), dt.timedelta(hours=4), 8000)
    schreibe("AAA_1h.csv", dt.datetime(2023, 1, 1, 0), std, 19000)       # Luecke: Stunde 5 fehlt je Tag (23 Kerzen/Tag)
    p = os.path.join(d, "data", "AAA_1h.csv"); z = open(p).read().split("\n")
    open(p, "w").write("\n".join([z[0]] + [l for l in z[1:] if l and l[11:13] != "05"]) + "\n")
    schreibe("SPAET_1h.csv", dt.datetime(2025, 1, 1), std, 17600)
    schreibe("XX_1d.csv", dt.datetime(2015, 3, 2), tag, 4300)
def lauf(ab_schnitt, mutation=False):
    with tempfile.TemporaryDirectory() as d:
        baue(d, ab_schnitt)
        quelle = os.path.join(WURZEL, "research", "faltenplan_neun")
        if mutation:   # Mutation: der Schnitt wirkt nicht (Zeilen ab dem Schnitt zaehlen mit)
            m = os.path.join(d, "mut"); shutil.copytree(quelle, m)
            p = os.path.join(m, "faltenschranke_messung.py"); s = open(p).read()
            s = s.replace("if tag is None or tag >= schnitt:", "if tag is None:", 1).replace(" and t < schnitt else None", " else None", 1)
            open(p, "w").write(s); quelle = m
        env = dict(os.environ, TB36_BASE_DIR=d)
        r = subprocess.run([sys.executable, "-B", "-c", KIND, quelle], capture_output=True, text=True, env=env, cwd=WURZEL)
        if r.returncode != 0: return {"fehler": r.stderr.strip().split("\n")[-1][:200]}
        import json; return json.loads(r.stdout.strip().split("\n")[-1])
n = [0, 0]
def pruefe(name, ok, info=""):
    n[0] += 1; n[1] += bool(ok); print(("ja    " if ok else "NEIN  ") + name + (" · " + str(info) if info else ""))
a, b = lauf(True), lauf(False)
pruefe("Lauf ohne Fehler", "fehler" not in a and "fehler" not in b, a.get("fehler", "") or b.get("fehler", ""))
if "fehler" not in a and "fehler" not in b:
    pruefe("Zeitspanne: erster Kurstag + MIN_HISTORY_DAYS (rsi2_crypto AAA = 2021-05-15)", a["rsi2_crypto"]["AAA"] == "2021-05-15", a["rsi2_crypto"]["AAA"])
    pruefe("4h-Bot t3_supertrend: 2023-01-01 + 730 Tage = 2024-12-31", a["t3_supertrend"]["AAA"] == "2024-12-31", a["t3_supertrend"]["AAA"])
    pruefe("Kerzen: elliott_wave AAA = Datum der 17 520. Kerze trotz Luecken (2023-01-01 + 17519 // 23 = 761 Tage, nicht 730)", a["elliott_wave"]["AAA"] == (dt.date(2023, 1, 1) + dt.timedelta(days=17519 // 23)).isoformat(), a["elliott_wave"]["AAA"])
    pruefe("Tag >= Schnitt -> None (SPAET 1d, SPAET 1h, KURZ)", a["rsi2_crypto"]["SPAET"] is None and a["elliott_wave"]["SPAET"] is None and a["rsi2_crypto"]["KURZ"] is None)
    pruefe("Datei fehlt -> None (FEHLT)", a["rsi2_mean_reversion"]["FEHLT"] is None)
    pruefe("Aktien: XX = 2015-03-02 + 1825", a["rsi2_mean_reversion"]["XX"] == "2020-02-29", a["rsi2_mean_reversion"]["XX"])
    pruefe("Zeilen ab dem Schnitt aendern keinen Tag (mit gegen ohne Zeilen ab Schnitt)", all(a[k] == b[k] for k in ("elliott_wave", "rsi2_crypto", "t3_supertrend", "rsi2_mean_reversion")))
    pruefe("loader_lesart ruft dieselbe Rechnung (R90 (e))", all(a["lesart_gleich"].values()), a["lesart_gleich"])
    pruefe("Gegenprobe Schnitt 2100: SPAET bekommt einen Tag (der Schnitt beisst)", a["ohne_schnitt"]["SPAET"] == "2026-10-14", a["ohne_schnitt"]["SPAET"])
    m = lauf(True, mutation=True)
    pruefe("Mutationsprobe (Schnitt in handelbar_ab entfernt): Abweichung erkannt", "fehler" in m or m["elliott_wave"] != a["elliott_wave"] or m["rsi2_crypto"] != a["rsi2_crypto"])
print("%d von %d Pruefungen bestanden" % (n[1], n[0])); sys.exit(0 if n[0] == n[1] and n[0] > 0 else 1)

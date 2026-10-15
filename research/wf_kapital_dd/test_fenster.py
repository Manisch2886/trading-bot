#!/usr/bin/env python3
"""
TB-162 - Proben fuer fenster.py an synthetischen Daten (Entscheid F4; Bauart R46: keine Zahl der Kursdaten der Bots)
  F1 zeitbasierte Rueckgabe -> Grenze je Symbol        F2 zeilenbasierte Rueckgabe -> open_time der Zeile k
  F3 widerspruechliche Grenze bricht ab                F4 Abschnitte lueckenlos, ausserhalb des Pfads bricht ab
  F5 Streuung (Spannweite, ohne Grenze)                P1 durchgehender Pfad: Basis des Abschnitts = Stand davor (kein Neustart)
  P2 Intraday-Positionen: E = M in jedem Abschnitt     P3 Handposition ueber die Grenze: M zeigt den Zwischenverlust, E nicht
"""
import os, sys, time
import numpy as np
import pandas as pd
_HIER = os.path.dirname(os.path.abspath(__file__)); REPO_ROOT = os.path.dirname(os.path.dirname(_HIER))
sys.path.insert(0, _HIER); sys.path.insert(0, os.path.join(REPO_ROOT, "research", "mtm_drawdown")); sys.path.insert(0, os.path.join(REPO_ROOT, "shared"))
import fenster          # noqa: E402
import mtm_kern         # noqa: E402
from messkette import max_drawdown_ungerundet   # noqa: E402
BEFUNDE = []
def pruefe(ok, text):
    BEFUNDE.append(bool(ok)); print(("ok    " if ok else "FEHL  ") + text)
def kurse(von, n, freq="D"):
    t = pd.date_range(von, periods=n, freq=freq); return pd.DataFrame({"open_time": t, "close": np.linspace(100, 120, n)})
def f_tests():
    a, b = kurse("2020-01-01", 101), kurse("2021-01-01", 11)
    st = {}
    for s, df in (("A", a), ("B", b)):
        w0, w1 = df["open_time"].min(), df["open_time"].max(); st[s] = w0 + (w1 - w0) * 0.7
    train = {s: (df, None, st[s]) for s, df in (("A", a), ("B", b))}; test = {s: (df, st[s], None) for s, df in (("A", a), ("B", b))}
    g = fenster.grenze_je_symbol(train, test)
    pruefe(g == {"A": pd.Timestamp("2020-03-11"), "B": pd.Timestamp("2021-01-08")}, "F1 zeitbasiert: Grenze je Symbol = split_time %s" % g)
    k = int(len(a) * 0.7); g2 = fenster.grenze_je_symbol({"A": a.iloc[:k]}, {"A": a.iloc[k:].reset_index(drop=True), "C": a.iloc[0:0]})
    pruefe(g2 == {"A": a["open_time"].iloc[k], "C": None}, "F2 zeilenbasiert: Grenze = open_time der Zeile %d, leerer OOS-Teil = None" % k)
    try:
        fenster.grenze_je_symbol({"A": (a, None, st["A"])}, {"A": (a, st["A"] + pd.Timedelta(days=1), None)}); pruefe(False, "F3 widerspruechliche Grenze bricht ab")
    except ValueError:
        pruefe(True, "F3 widerspruechliche Grenze bricht ab (ValueError)")
    ab = fenster.abschnitte(g, "2020-01-01", "2021-01-12")
    lueckenlos = all(ab[i]["bis_ausschliesslich"] == ab[i + 1]["von"] for i in (1, 2)) and ab[1]["von"] == ab[0]["von"] and ab[3]["bis_ausschliesslich"] == ab[0]["bis_ausschliesslich"]
    pruefe([x["name"] for x in ab] == list(fenster.ABSCHNITTE) and lueckenlos, "F4 Abschnitte gesamt/IS/gemischt/OOS lueckenlos")
    try:
        fenster.abschnitte(g, "2020-06-01", "2021-01-12"); pruefe(False, "F4 Grenze vor dem Pfadbeginn bricht ab")
    except ValueError:
        pruefe(True, "F4 Grenze vor dem Pfadbeginn bricht ab (ValueError)")
    s = fenster.streuung(dict(g, C=None))
    pruefe(s["spannweite_tage"] == 303.0 and s["symbole_ohne_grenze"] == ["C"] and s["symbole"] == 3, "F5 Streuung: Spannweite %s Tage, ohne Grenze %s" % (s["spannweite_tage"], s["symbole_ohne_grenze"]))
def pfad(pos, tage, schluss, kosten=0.0):
    e = mtm_kern.ereignisreihenfolge(pos, 10000.0); k = mtm_kern.ereigniskurve(e)
    ks, f = mtm_kern.kurse_auf_raster({"X": pd.Series(schluss, index=tage)}, tage)
    return k, mtm_kern.mtm_pfad(e, ks, f, 10000.0, kosten)
def p_tests():
    tage = pd.date_range("2020-01-01", periods=10, freq="D")
    schluss = [100, 100, 90, 80, 95, 105, 105, 105, 105, 105]
    pos = pd.DataFrame({"symbol": ["X"], "entry_time": [tage[1]], "exit_time": [tage[5]], "entry_price": [100.0], "exit_price": [105.0],
                        "allocation": [2000.0], "pnl_pct": [5.0], "capital_after": [10100.0]})
    k, p = pfad(pos, tage, schluss)
    ab = fenster.abschnitte({"X": tage[3]}, tage[0], tage[-1] + pd.Timedelta(days=1))
    m = {z["falte"]: z for z in mtm_kern.messe_falten(k, p, ab, 10000.0, max_drawdown_ungerundet)}
    pruefe(abs(m["OOS"]["basis_M"] - float(p["mtm"].iloc[2])) < 1e-9 and m["OOS"]["basis_M"] != 10000.0,
           "P1 kein Neustart: Basis M des OOS = Stand am Vortag der Grenze (%s), nicht das Startkapital" % m["OOS"]["basis_M"])
    pruefe(m["gesamt"]["E"] == 0.0 and m["gesamt"]["M"] < 0 and m["IS"]["M"] < 0, "P3 Handposition ueber die Grenze: E %s, M gesamt %s, M IS %s" % (m["gesamt"]["E"], m["gesamt"]["M"], m["IS"]["M"]))
    rows = []; kap = 10000.0
    for i, (r, d) in enumerate(zip([2.0, -3.0, 1.5, -4.0, 2.5], tage[1:6])):
        kap += 1000.0 * r / 100; rows.append({"symbol": "X", "entry_time": d, "exit_time": d + pd.Timedelta(hours=1), "entry_price": 100.0,
                                             "exit_price": 100.0 * (1 + r / 100), "allocation": 1000.0, "pnl_pct": r, "capital_after": kap})
    k, p = pfad(pd.DataFrame(rows), tage, [100.0] * 10)
    m2 = mtm_kern.messe_falten(k, p, ab, 10000.0, max_drawdown_ungerundet)
    pruefe(all(z["E"] == z["M"] for z in m2), "P2 Intraday: E = M in allen %d Abschnitten %s" % (len(m2), [(z["falte"], z["E"], z["M"]) for z in m2]))
def main():
    t0 = time.time(); f_tests(); p_tests(); n, ok = len(BEFUNDE), sum(BEFUNDE)
    print("%d von %d Pruefungen bestanden, %d gescheitert, Laufzeit %.1f s" % (ok, n, n - ok, time.time() - t0))
    return 0 if ok == n else 1
if __name__ == "__main__":
    sys.exit(main())

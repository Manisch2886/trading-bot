#!/usr/bin/env python3
"""
TB-162 - Proben fuer rekonstruktion.py an synthetischen Daten (Entscheid F9; R97 (b); keine Zahl der Kursdaten der Bots)
  R1 eindeutige Trades: alle Kurvenzeilen zugeordnet, Kapitalkette schliesst   R2 gleicher Schluessel, Kapitalprobe trennt
  R3 inhaltsgleiche Zeilen: kleinste Zeile, gezaehlt                          R4 NICHT ZUORDENBAR: zwei verschiedene Kandidaten, gleiches Kapital
  R5 Kurvenzeile ohne Kandidat: nicht zuordenbar, gemeldet                    R6 Zeitzone: tz-behaftete Trades gegen naive Kurve
  R7 der Lauf (simuliere_portfolio) laesst die Trades unveraendert            R8 Quelle: kein Schreibzugriff auf Trades, kein positionen_holen
  R9 Nullschritt im Gleichstand: Liste in Kurvenreihenfolge, die Kette von mtm_kern schliesst
  R10 messung.simuliere_wie_main: kursdaten per Keyword, Limit nur wo die Signatur es hat, kursdaten_symbole 0 bricht ab
"""
import os, re, sys, time
import pandas as pd
_HIER = os.path.dirname(os.path.abspath(__file__)); REPO_ROOT = os.path.dirname(os.path.dirname(_HIER))
sys.path.insert(0, _HIER); sys.path.insert(0, os.path.join(REPO_ROOT, "shared"))
import rekonstruktion as rk   # noqa: E402
import zuteilung              # noqa: E402
sys.path.insert(0, os.path.join(REPO_ROOT, "research", "mtm_drawdown"))
import mtm_kern               # noqa: E402
BEFUNDE = []
def pruefe(ok, text):
    BEFUNDE.append(bool(ok)); print(("ok    " if ok else "FEHL  ") + text)
T = pd.Timestamp
def tr(rows):
    return pd.DataFrame([{"symbol": s, "entry_time": e, "exit_time": x, "entry_price": ep, "exit_price": ep * (1 + p / 100), "pnl_pct": p}
                         for s, e, x, ep, p in rows])
def lauf(trades, pct=0.1, limit=None):
    vorher = trades.copy(deep=True)
    e = zuteilung.simuliere_portfolio(trades, 10000.0, pct, limit)
    return e, trades.equals(vorher) and list(trades.columns) == list(vorher.columns)
def kette(pos, start=10000.0):
    p = pos.sort_values("kurvenzeile"); kap = start
    for a, r, c in zip(p["allocation"], p["pnl_pct"], p["capital_after"]):
        kap += a * r / 100
        if abs(kap - c) > rk.TOL_GELD: return False
    return True
def main():
    t0 = time.time()
    t1 = tr([("A", T("2021-01-01"), T("2021-01-05"), 10.0, 2.0), ("B", T("2021-01-02"), T("2021-01-04"), 20.0, -1.0),
             ("C", T("2021-01-03"), T("2021-01-09"), 30.0, 3.0), ("A", T("2021-01-06"), T("2021-01-08"), 11.0, 1.5)])
    e, unv = lauf(t1); pos, b = rk.zuordnen(t1, e["equity_curve"], 10000.0, 0.1)
    pruefe(b["zugeordnet"] == e["num_executed"] == 4 and b["nicht_zuordenbar"] == 0 and b["eindeutig"] == 4 and kette(pos)
           and sorted(pos["trade_zeile"]) == [0, 1, 2, 3] and list(pos["kurvenzeile"]) == [0, 1, 2, 3], "R1 eindeutig: %d von %d zugeordnet, Kette schliesst" % (b["zugeordnet"], b["kurvenzeilen"]))
    t2 = tr([("X", T("2021-01-01"), T("2021-01-10"), 10.0, 5.0), ("Y", T("2021-01-02"), T("2021-01-03"), 10.0, 20.0),
             ("X", T("2021-01-04"), T("2021-01-10"), 10.0, 5.0)])
    e, unv = lauf(t2); pos, b = rk.zuordnen(t2, e["equity_curve"], 10000.0, 0.1)
    xa = dict(zip(pos["trade_zeile"], pos["allocation"]))
    pruefe(b["nicht_zuordenbar"] == 0 and b["durch_kapitalprobe"] >= 1 and xa.get(0) == 1000.0 and xa.get(2) == 1020.0 and kette(pos),
           "R2 Kapitalprobe trennt gleichen Schluessel (Einstieg vor/nach Gewinn Y): allocation je Zeile %s, %s" % (xa, {k: b[k] for k in ("eindeutig", "durch_kapitalprobe", "inhaltsgleich")}))
    t3 = tr([("X", T("2021-01-01"), T("2021-01-05"), 10.0, 1.0), ("X", T("2021-01-01"), T("2021-01-05"), 10.0, 1.0)])
    e, unv = lauf(t3); pos, b = rk.zuordnen(t3, e["equity_curve"], 10000.0, 0.1)
    pruefe(b["nicht_zuordenbar"] == 0 and b["inhaltsgleich"] >= 1 and sorted(pos["trade_zeile"]) == [0, 1],
           "R3 inhaltsgleich: %d gezaehlt, Zeilen %s" % (b["inhaltsgleich"], sorted(pos["trade_zeile"])))
    t4 = tr([("X", T("2021-01-01"), T("2021-01-10"), 10.0, 4.0), ("X", T("2021-01-03"), T("2021-01-10"), 10.0, 4.0)])
    t4.loc[1, "entry_price"] = 10.5
    e, unv = lauf(t4, pct=0.6); pos, b = rk.zuordnen(t4, e["equity_curve"], 10000.0, 0.6)
    pruefe(e["num_executed"] == 1 and b["nicht_zuordenbar"] == 1 and len(pos) == 0 and b["nicht_zuordenbar_zeilen"][0]["kandidaten"] == 2,
           "R4 NICHT ZUORDENBAR gemeldet: %s" % b["nicht_zuordenbar_zeilen"])
    k5 = pd.DataFrame([{"time": T("2021-02-01"), "symbol": "Z", "pnl_pct": 1.0, "allocation": 1000.0, "capital_after": 10010.0}])
    pos, b = rk.zuordnen(t1, k5, 10000.0, 0.1)
    pruefe(b["nicht_zuordenbar"] == 1 and b["nicht_zuordenbar_zeilen"][0]["kandidaten"] == 0, "R5 Kurvenzeile ohne Kandidat gemeldet")
    t6 = t1.copy(); t6["entry_time"] = [str(x.tz_localize("UTC").tz_convert("Europe/Berlin")) for x in t1["entry_time"]]
    t6["exit_time"] = [str(x.tz_localize("UTC").tz_convert("Europe/Berlin")) for x in t1["exit_time"]]
    e, _ = lauf(t1); pos, b = rk.zuordnen(t6, e["equity_curve"], 10000.0, 0.1)
    pruefe(b["zugeordnet"] == 4 and b["nicht_zuordenbar"] == 0, "R6 Zeitzone: Berlin-Text gegen naive UTC-Kurve, %d zugeordnet" % b["zugeordnet"])
    alle = all(lauf(t)[1] for t in (t1, t2, t3, t4))
    vor = t2.copy(deep=True); rk.zuordnen(t2, lauf(t2)[0]["equity_curve"], 10000.0, 0.1)
    pruefe(alle and t2.equals(vor), "R7 Lauf und Zuordnung lassen die Trades unveraendert (DataFrame.equals)")
    schreib = re.compile(r"trades(\[[^\]]*\]|\.(loc|iloc|at|iat)\[[^\]]*\])\s*=[^=]|trades\.(insert|pop|drop|sort_values|set_index|rename)\([^)]*inplace|positionen_holen\.py[\x22\x27]|(import|from)\s+positionen_holen|spec_from_file_location\([^)]*positionen_holen")
    quellen = [os.path.join(_HIER, f) for f in ("rekonstruktion.py", "messung.py") if os.path.exists(os.path.join(_HIER, f))]
    treffer = [(os.path.basename(q), z) for q in quellen for z in open(q, encoding="utf-8").read().split("\n") if schreib.search(z)]
    pruefe(len(quellen) == 2 and not treffer, "R8 Quellen ohne Schreibzugriff auf Trades und ohne positionen_holen: %s" % (treffer or "keiner"))
    t9 = tr([("P", T("2021-01-03"), T("2021-01-11"), 10.0, 0.0), ("B", T("2021-01-01"), T("2021-01-11"), 10.0, -3.55),
             ("C", T("2021-01-01"), T("2021-01-11"), 10.0, -2.5), ("D", T("2021-01-02"), T("2021-01-05"), 10.0, 1.0)])
    e, _ = lauf(t9); pos, b = rk.zuordnen(t9, e["equity_curve"], 10000.0, 0.1)
    try:
        r = mtm_kern.ereignisreihenfolge(pos, 10000.0); ok9 = list(r["kurvenzeile"]) == sorted(pos["kurvenzeile"])
    except ValueError as x:
        ok9 = False
    pruefe(ok9 and b["nicht_zuordenbar"] == 0, "R9 Nullschritt im Gleichstand: mtm_kern.ereignisreihenfolge folgt der Kurvenreihenfolge")
    import importlib.util, types
    spec = importlib.util.spec_from_file_location("wf_messung", os.path.join(_HIER, "messung.py"))   # nicht research/mtm_drawdown/messung.py
    messung = importlib.util.module_from_spec(spec); spec.loader.exec_module(messung)
    ruf = []
    def sp_ohne(trades, starting_capital, allocation_pct, kursdaten=None, signalspalte=None):
        ruf.append(("ohne", kursdaten is not None)); return zuteilung.simuliere_portfolio(trades, starting_capital, allocation_pct, None, kursdaten)
    def sp_mit(trades, starting_capital, allocation_pct, max_concurrent_positions=None, kursdaten=None, signalspalte=None):
        ruf.append(("mit", max_concurrent_positions, kursdaten is not None)); return zuteilung.simuliere_portfolio(trades, starting_capital, allocation_pct, max_concurrent_positions, kursdaten)
    kd = {s: pd.DataFrame({"open_time": pd.date_range("2020-12-01", periods=60, freq="D"), "close": [100.0 + i for i in range(60)],
                           "volume": [1000.0] * 60}) for s in ("A", "B", "C")}
    es1 = types.SimpleNamespace(simulate_portfolio=sp_ohne, STARTING_CAPITAL=10000.0, ALLOCATION_PCT=0.1)
    es2 = types.SimpleNamespace(simulate_portfolio=sp_mit, STARTING_CAPITAL=10000.0, ALLOCATION_PCT=0.1, MAX_CONCURRENT_POSITIONS=3)
    e1 = messung.simuliere_wie_main(es1, t1, kd); e2 = messung.simuliere_wie_main(es2, t1, kd)
    try:
        messung.simuliere_wie_main(es1, t1, {}); abbr = False
    except SystemExit:
        abbr = True
    pruefe(ruf[:2] == [("ohne", True), ("mit", 3, True)] and e1["zuteilung"]["kursdaten_symbole"] > 0 and e2["zuteilung"]["kursdaten_symbole"] > 0 and abbr,
           "R10 wie __main__: Aufrufe %s, kursdaten_symbole %s/%s, ohne Kursdaten Abbruch: %s" % (ruf[:2], e1["zuteilung"]["kursdaten_symbole"], e2["zuteilung"]["kursdaten_symbole"], abbr))
    n, ok = len(BEFUNDE), sum(BEFUNDE)
    print("%d von %d Pruefungen bestanden, %d gescheitert, Laufzeit %.1f s" % (ok, n, n - ok, time.time() - t0))
    return 0 if ok == n else 1
if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""TB-120 Schritt C - Bestand im Code, nur lesend.

Liest Quelltext mit `ast` und Text (kein Import von Bot-, Research- oder
Laufcode, kein Lauf, keine Datei geschrieben ausser der Ausgabe auf stdout).
Aufruf von der Repo-Wurzel:  python3 docs/belege/TB-120/c_messung.py
"""
import ast
import os
import re
import subprocess

BOTS = ["elliott_wave", "t3_supertrend", "rsi2_crypto", "turtle_soup_crypto",
        "volatility_breakout_crypto", "elliott_wave_stocks", "rsi2_mean_reversion",
        "turtle_soup_stocks", "volatility_breakout"]


def commit(pfad):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--", pfad],
                          capture_output=True, text=True).stdout.strip()


def funktionen(pfad, namen):
    src = open(pfad, encoding="utf-8").read()
    t = ast.parse(src)
    aus = {}
    for n in t.body:
        if isinstance(n, ast.FunctionDef) and n.name in namen:
            aus[n.name] = (n, ast.get_source_segment(src, n))
    return src, aus


def main():
    print("# TB-120 C - Bestand im Code (nur lesend), HEAD",
          subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True).stdout.strip())

    print("\n## C3 - evaluate_combination_multi je Bot (multi_symbol_optimise.py)")
    print("Bot | Zeilen | Argumente | return None | ruft Simulation | MIN_TRADES/MIN_SYMBOLS/MIN_AVG | "
          "Kapital-DD-Feld | Tagesreihe | Trades zurueck | Commit")
    for b in BOTS:
        p = f"strategies/{b}/multi_symbol_optimise.py"
        src, f = funktionen(p, {"evaluate_combination_multi"})
        n, seg = f["evaluate_combination_multi"]
        rn = sum(1 for x in ast.walk(n) if isinstance(x, ast.Return)
                 and isinstance(x.value, ast.Constant) and x.value.value is None)
        sim = ("simulate_portfolio" in seg) or ("simuliere_portfolio" in seg)
        filt = "/".join(str(k in seg) for k in ("MIN_TRADES", "MIN_SYMBOLS", "MIN_AVG_RETURN"))
        kap = "max_drawdown_kapital_pct" in seg
        tag = bool(re.search(r"tages|mark.to.market|mtm", seg, re.I))
        # Rueckgabe: das dict `result`; enthaelt es eine Trade-Liste?
        trades_zurueck = bool(re.search(r'"trades"\s*:', seg))
        print(f"{b} | {n.lineno}-{n.end_lineno} | {[a.arg for a in n.args.args]} | {rn} | {sim} | "
              f"{filt} | {kap} | {tag} | {trades_zurueck} | {commit(p)}")

    print("\n## C3 - Signalpfad und Kapitalpfad je Bot (equity_simulation.py)")
    for b in BOTS:
        p = f"strategies/{b}/equity_simulation.py"
        src, f = funktionen(p, {"collect_all_trades", "simulate_portfolio"})
        sp = "strategy_paths" in src
        lp = bool(re.search(r"^from live_params import", src, re.M))
        print(f"{b} | collect_all_trades{[a.arg for a in f['collect_all_trades'][0].args.args]} | "
              f"simulate_portfolio{[a.arg for a in f['simulate_portfolio'][0].args.args]} | "
              f"strategy_paths={sp} live_params={lp} | {commit(p)}")

    print("\n## C3 - Rueckgabe von shared/zuteilung.py::simuliere_portfolio")
    src = open("shared/zuteilung.py", encoding="utf-8").read()
    m = re.findall(r'equity_curve\.append\(\{(.*?)\}\)', src, re.S)
    print("equity_curve-Zeile:", " ".join(m[0].split()) if m else "nicht gefunden")
    ret = re.findall(r'return \{\s*"final_capital".*?\}', src, re.S)
    print("Rueckgabeschluessel:", sorted(set(re.findall(r'"(\w+)":', ret[-1]))) if ret else "-")
    print("Commit", commit("shared/zuteilung.py"))

    print("\n## C3 - Felder der Signalpfad-Trades je Backtest (Schluessel in trades.append/dict)")
    for b in BOTS:
        for fn in sorted(os.listdir(f"strategies/{b}")):
            if fn.startswith("backtest_") and fn.endswith(".py"):
                p = f"strategies/{b}/{fn}"
                src = open(p, encoding="utf-8").read()
                t = ast.parse(src)
                sig = {n.name: [a.arg for a in n.args.args] for n in t.body
                       if isinstance(n, ast.FunctionDef) and n.name in ("run_backtest", "compute_indicators")}
                felder = set()
                for d in ast.walk(t):
                    if isinstance(d, ast.Dict) and any(isinstance(k, ast.Constant) and k.value == "entry_time"
                                                       for k in d.keys):
                        felder |= {k.value for k in d.keys if isinstance(k, ast.Constant)}
                print(f"{b} | {fn} | {sig} | Felder {sorted(felder)} | {commit(p)}")

    print("\n## C4 Posten 3 - Durchreichung")
    p = "strategies/rsi2_mean_reversion/backtest_rsi2.py"
    src, f = funktionen(p, {"compute_indicators", "run_backtest"})
    print("rsi2_mean_reversion compute_indicators", [a.arg for a in f["compute_indicators"][0].args.args],
          "| Konstante:", [l.strip() for l in src.splitlines() if l.startswith("SMA_TREND_PERIOD")])
    for b in ("volatility_breakout", "volatility_breakout_crypto"):
        for p in (f"strategies/{b}/multi_symbol_optimise.py", f"strategies/{b}/equity_simulation.py"):
            src = open(p, encoding="utf-8").read()
            aufrufe = re.findall(r"compute_indicators\([^)]*\)", src)
            print(b, os.path.basename(p), "compute_indicators-Aufrufe:", aufrufe,
                  "| squeeze-Argument weitergereicht:", bool(re.search(r"squeeze_(lookback|percentile)", src)))

    print("\n## C4 Posten 4 - entry_cutoff / RECENT_YEARS_ONLY je Bot (multi_symbol_optimise.py)")
    for b in BOTS:
        p = f"strategies/{b}/multi_symbol_optimise.py"
        zeilen = [f"{i}: {l.strip()}" for i, l in enumerate(open(p, encoding="utf-8"), 1)
                  if re.search(r"RECENT_YEARS_ONLY\s*=|DateOffset\(years=RECENT_YEARS_ONLY\)", l)]
        print(b, "|", zeilen or "keine (kein Horizont, Register 26.2)")

    print("\n## C4 Posten 5 - Wache 29.4 je Bot (Suchworte in multi_symbol_optimise.py)")
    for b in BOTS:
        p = f"strategies/{b}/multi_symbol_optimise.py"
        src = open(p, encoding="utf-8").read()
        treffer = len(re.findall(r"erste[rn]? (Selektions)?falte|Selektionsfalte|fruehester|frühester|horizontbeginn",
                                 src, re.I))
        print(b, "| Treffer", treffer)

    print("\n## C5 Posten 8 - Walk-Forward im Modus")
    for b in BOTS:
        p = f"strategies/{b}/multi_symbol_walk_forward.py"
        src = open(p, encoding="utf-8").read()
        print(b, "| selektionsmodus", src.count("selektionsmodus"), "| strategy_paths", "strategy_paths" in src,
              "|", commit(p))
    for p in ("shared/paths.py", "shared/strategy_paths.py"):
        src = open(p, encoding="utf-8").read()
        print(p, "| 'walk_forward' im Text:", len(re.findall(r"walk.forward", src, re.I)))


if __name__ == "__main__":
    main()

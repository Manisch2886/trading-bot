#!/usr/bin/env python3
"""TB-169 (A1): Probe kerzen_je_trade. Die Kerzenzahlen des neuen Codes (research/tb24_haltedauern/positionen_holen.py,
Funktionen kursreihe und kerzen_je_trade unveraendert per ast geladen) gleich der Spalte kerzen in
research/tb24_haltedauern/daten/<bot>_alle_trades.csv (TB-24) - fuer alle Trades, deren Symbol im Snapshot eine Kursreihe hat.
Liest nur open_time der Kursreihen aus dem Snapshot (kein Lauf, kein Bot-Code, data/ nicht gelesen).
Aufruf aus der Repo-Wurzel: python3 -B kerzen_probe.py <SNAPSHOT-ORDNER> [<positionen_holen.py>]   (rc 0 = alle gleich)"""
import ast, os, sys
import pandas as pd
TF = {"elliott_wave": "1h", "t3_supertrend": "4h", "rsi2_crypto": "1d", "turtle_soup_crypto": "1d", "volatility_breakout_crypto": "1d",
      "elliott_wave_stocks": "1d", "rsi2_mean_reversion": "1d", "turtle_soup_stocks": "1d", "volatility_breakout": "1d"}
q = open(sys.argv[2] if len(sys.argv) > 2 else "research/tb24_haltedauern/positionen_holen.py", encoding="utf-8").read()
ns = {"pd": pd}; exec(compile(ast.Module(body=[n for n in ast.parse(q).body if isinstance(n, ast.FunctionDef) and n.name in ("kursreihe", "kerzen_je_trade")], type_ignores=[]), "positionen_holen", "exec"), ns)
snap = sys.argv[1]; fehler = 0; summe = 0
for bot, tf in TF.items():
    tr = pd.read_csv("research/tb24_haltedauern/daten/%s_alle_trades.csv" % bot)
    tr["entry_time"] = pd.to_datetime(tr["entry_time"]); tr["exit_time"] = pd.to_datetime(tr["exit_time"])
    syms = sorted(s for s in tr["symbol"].astype(str).unique() if os.path.exists(os.path.join(snap, "%s_%s.csv" % (s, tf))))
    daten = {s: pd.read_csv(os.path.join(snap, "%s_%s.csv" % (s, tf)), usecols=["open_time"], parse_dates=["open_time"]) for s in syms}
    t = tr[tr["symbol"].astype(str).isin(syms)].copy(); neu = ns["kerzen_je_trade"](t, daten)
    ab = int((neu.astype("Int64") != t["kerzen"].astype("Int64")).fillna(True).sum()); summe += len(t); fehler += ab
    voll = len(t) == len(tr) and len(syms) == tr["symbol"].nunique(); fehler += 0 if voll else 1   # B3: volle Abdeckung, sonst Teilmessung = NEIN
    print("%s %s: Trades in der Liste %d, mit Kursreihe im Snapshot %d (Symbole %d von %d), kerzen gleich %d, abweichend %d"
          % ("ja  " if ab == 0 and len(t) and voll else "NEIN", bot, len(tr), len(t), len(syms), tr["symbol"].nunique(), len(t) - ab, ab))
print("Ergebnis: %d Trades verglichen, %d abweichend oder ohne Kursreihe" % (summe, fehler)); sys.exit(0 if fehler == 0 and summe else 1)

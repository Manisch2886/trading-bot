#!/usr/bin/env python3
"""TB-124 B2 - Kommt der Lookback-Vermerk (df.attrs["squeeze_lookback_days"]) unter der pandas-Fassung von
trading-env auf allen Wegen des Signalpfads bis zu run_backtest an?

Aufruf (Repo-Wurzel): trading-env/bin/python3 docs/belege/TB-124/b2_vermerk_probe.py <wurzel>
  <wurzel> = Repo (Stand vor oder nach B) oder ein Kandidatenordner mit derselben Anordnung.

Gemessen wird ohne Monkeypatch ueber sys.setprofile: bei jedem Aufruf von backtest_breakout.run_backtest
wird price_df.attrs festgehalten. Je Bot ein eigener Unterprozess (cwd = Strategieordner).
Wege je Bot:
  W1 equity_simulation.collect_all_trades (synthetische Reihe) mit Stufe 20, 97 (nur Aktien) und ohne Argument
  W2 multi_symbol_optimise.get_trades_for_symbol direkt (synthetisch) mit Stufe 20 und ohne Argument
  W3 multi_symbol_optimise.evaluate_combination_multi (Optimierer, synthetisch), ohne Achsenargument
  W4 load_all_symbol_data() -> get_trades_for_symbol, echte Kurse aus data/, SYMBOLS auf die ersten zwei begrenzt
  W5 __main__ von backtest_breakout.py (runpy), Ausgabe verworfen
Sichtschutz 27.1: gedruckt werden nur die Vermerke und Frame-Laengen-unabhaengige Angaben, keine Kennzahl,
keine Trade- oder Zeilenzahl. Die Stufenwerte 20/97 stehen hier als Zahl, weil es eine Wegeprobe ist, keine
Registerprobe (die Registerprobe ist C2).
"""
import os
import subprocess
import sys

KIND = r'''
import io, os, sys, contextlib, runpy
import numpy as np, pandas as pd
sys.path[:0] = [os.getcwd(), os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "shared")]
BOT = os.path.basename(os.getcwd())
gesehen = []
def hook(frame, event, arg):
    if event == "call" and frame.f_code.co_name == "run_backtest" and frame.f_code.co_filename.endswith("backtest_breakout.py"):
        gesehen.append(dict(frame.f_locals["price_df"].attrs))
def weg(name, f):
    del gesehen[:]
    sys.setprofile(hook)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            f()
        fehler = ""
    except Exception as e:
        fehler = " FEHLER %s: %s" % (type(e).__name__, str(e)[:120])
    finally:
        sys.setprofile(None)
    werte = sorted({str(g.get("squeeze_lookback_days", "<kein Vermerk>")) for g in gesehen})
    print("%-28s %-58s Aufrufe>0: %-5s Vermerke: %s%s" % (BOT, name, bool(gesehen), werte, fehler))
import backtest_breakout as bt, multi_symbol_optimise as mo, equity_simulation as es
def kurse(n=400):
    rng = np.random.RandomState(20260930)
    c = 100 * np.cumprod(1 + rng.normal(0, 0.01, n))
    return pd.DataFrame({"open_time": pd.date_range("2020-01-01", periods=n, freq="D"),
                         "open": c, "high": c * 1.01, "low": c * 0.99, "close": c, "volume": 1e6})
aktien = BOT == "volatility_breakout"
roh = kurse()
syn = {"SYN": (bt.compute_indicators(roh), None)} if aktien else {"SYN": roh}
for stufe in ([20, 97] if aktien else [20]):
    weg("W1 collect_all_trades(squeeze_lookback_days=%d)" % stufe,
        lambda: es.collect_all_trades(syn, 8.0, squeeze_lookback_days=stufe))
weg("W1 collect_all_trades() ohne Achsenargument", lambda: es.collect_all_trades(syn, 8.0))
if aktien:
    weg("W2 get_trades_for_symbol(df_ind, None, 8.0, 20)", lambda: mo.get_trades_for_symbol(syn["SYN"][0], None, 8.0, squeeze_lookback_days=20))
    weg("W2 get_trades_for_symbol(df_ind, None, 8.0)", lambda: mo.get_trades_for_symbol(syn["SYN"][0], None, 8.0))
else:
    weg("W2 get_trades_for_symbol(roh, 8.0, squeeze_lookback_days=20)", lambda: mo.get_trades_for_symbol(roh, 8.0, squeeze_lookback_days=20))
    weg("W2 get_trades_for_symbol(roh, 8.0)", lambda: mo.get_trades_for_symbol(roh, 8.0))
weg("W3 evaluate_combination_multi(syn, 8.0)", lambda: mo.evaluate_combination_multi(syn, 8.0))
mo.SYMBOLS = mo.SYMBOLS[:2]
def w4():
    alle = mo.load_all_symbol_data()
    for sym, wert in alle.items():
        if aktien:
            df_ind, cut = wert
            mo.get_trades_for_symbol(df_ind, cut, 8.0, squeeze_lookback_days=20)
        else:
            mo.get_trades_for_symbol(wert, 8.0, squeeze_lookback_days=20)
weg("W4 load_all_symbol_data -> get_trades_for_symbol(.., 20)", w4)
weg("W5 __main__ von backtest_breakout.py (runpy)", lambda: runpy.run_path("backtest_breakout.py", run_name="__main__"))
# W6: Ein Aufruf mit Stufe 20 darf den Vermerk des vorberechneten Frames (Gestalt load_all_symbol_data) nicht
# veraendern - sonst liefe ein spaeterer Aufruf mit der Voreinstellung auf einem fremden Scanbeginn.
vorab = bt.compute_indicators(roh)
v0 = dict(vorab.attrs)
if aktien:
    mo.get_trades_for_symbol(vorab, None, 8.0, squeeze_lookback_days=20)
else:
    mo.get_trades_for_symbol(vorab, 8.0, squeeze_lookback_days=20)
print("%-28s W6 Vermerk des vorberechneten Frames vor/nach Aufruf mit 20: %s / %s; Rohreihe: %s"
      % (BOT, v0, dict(vorab.attrs), dict(roh.attrs)))
'''

wurzel = os.path.abspath(sys.argv[1])
print("# TB-124 B2 Vermerk-Probe, Wurzel %s" % wurzel)
import pandas
print("# python %s, pandas %s" % (sys.version.split()[0], pandas.__version__))
for bot in ("volatility_breakout", "volatility_breakout_crypto"):
    r = subprocess.run([sys.executable, "-W", "ignore", "-c", KIND], cwd=os.path.join(wurzel, "strategies", bot),
                       capture_output=True, text=True,
                       env={k: v for k, v in os.environ.items() if not k.startswith(("TB_SELEKTIONS", "TB30A"))})
    sys.stdout.write(r.stdout)
    if r.returncode:
        print("rc %d %s" % (r.returncode, r.stderr[-800:]))

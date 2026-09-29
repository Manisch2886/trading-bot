#!/usr/bin/env python3
"""TB-122 A1/A2/C1 - Vergleichslaeufe vorher/nachher fuer die drei Bots aus Posten 3.

Aufruf (Repo-Wurzel, ohne Modus):  trading-env/bin/python3 docs/belege/TB-122/a_lauf.py <ausgabeordner>

Bauart TB-90 B6 (docs/belege/TB-90/b6_backtest_lauf.py): je Bot ein eigener
Unterprozess (backtest_rsi2, indicators, live_params gibt es mehrfach), cwd =
Strategieordner, sys.path = [Strategieordner, shared/]. Je Bot drei Laeufe:

  b6.csv                 - wortgleich der Aufruf aus TB-90 B6 (ein Symbol, Backtest-Modul).
  trades.csv             - Signalpfad ueber ALLE Symbole: equity_simulation.load_all_symbol_data()
                           + collect_all_trades(...) mit den heutigen Parametern (live_params ueber
                           die Modulglobalen von equity_simulation), wie im __main__-Zweig.
  trades_regimefilter.csv  (nur volatility_breakout_crypto) - apply_btc_regime_filter wie __main__.
  equity_curve.csv       - simulate_portfolio(...) wie im __main__-Zweig; RESULTS_DIR wird NICHT
                           benutzt, die Kurve geht nach <ausgabeordner>.
  optimierer.csv         - A2: run_multi_optimisation(all_data) des Optimierers, das Raster von aussen
                           (Modulattribut im Unterprozess, keine Codeaenderung) auf die heutige
                           Kombination begrenzt.

Sichtschutz 27.1: Es wird KEINE Kennzahl gedruckt, auch keine Tradeanzahl -
nur rc und sha256 je Datei. Die Standardausgabe der Unterprozesse (Ladeprotokoll)
geht in <ausgabeordner>/<bot>/lauf.log und wird nicht gelesen.
Nur lesend gegenueber dem Repo.
"""
import hashlib
import os
import subprocess
import sys
import time

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

B6 = {
    "rsi2_mean_reversion": ("backtest_rsi2", """
price_df = pd.read_csv(os.path.join(D, "AAPL_1d.csv"), parse_dates=["open_time"])
df = m.compute_indicators(price_df)
trades = m.run_backtest(df, rsi_threshold=5.0, stop_loss_pct=5.0)
"""),
    "volatility_breakout": ("backtest_breakout", """
price_df = pd.read_csv(os.path.join(D, "AAPL_1d.csv"), parse_dates=["open_time"])
df = m.compute_indicators(price_df)
trades = m.run_backtest(df, stop_loss_pct=5.0)
"""),
    "volatility_breakout_crypto": ("backtest_breakout", """
price_df = pd.read_csv(os.path.join(D, "BTCUSDT_1d.csv"), parse_dates=["open_time"])
df = m.compute_indicators(price_df)
trades = m.run_backtest(df, stop_loss_pct=8.0)
"""),
}

# Signalpfad und Optimierer - die Aufrufe folgen je Bot dem __main__-Zweig von
# equity_simulation.py bzw. multi_symbol_optimise.py.
PFAD = {
    "rsi2_mean_reversion": """
trades = es.collect_all_trades(all_data, es.RSI_THRESHOLD, es.STOP_LOSS_PCT)
schreibe(trades, "trades.csv")
result = es.simulate_portfolio(trades, es.STARTING_CAPITAL, es.ALLOCATION_PCT, es.MAX_CONCURRENT_POSITIONS, all_data)
schreibe(result["equity_curve"], "equity_curve.csv")
mo.RSI_THRESHOLD_RANGE = [es.RSI_THRESHOLD]
mo.STOP_LOSS_RANGE = [es.STOP_LOSS_PCT]
schreibe(mo.run_multi_optimisation(all_data), "optimierer.csv")
""",
    "volatility_breakout": """
trades = es.collect_all_trades(all_data, es.STOP_LOSS_PCT)
schreibe(trades, "trades.csv")
result = es.simulate_portfolio(trades, es.STARTING_CAPITAL, es.ALLOCATION_PCT, es.MAX_CONCURRENT_POSITIONS, all_data)
schreibe(result["equity_curve"], "equity_curve.csv")
mo.STOP_LOSS_RANGE = [es.STOP_LOSS_PCT]
schreibe(mo.run_multi_optimisation(all_data), "optimierer.csv")
""",
    "volatility_breakout_crypto": """
trades = es.collect_all_trades(all_data, es.STOP_LOSS_PCT)
schreibe(trades, "trades.csv")
trades = es.apply_btc_regime_filter(trades, all_data)
schreibe(trades, "trades_regimefilter.csv")
result = es.simulate_portfolio(trades, es.STARTING_CAPITAL, es.ALLOCATION_PCT, es.MAX_CONCURRENT_POSITIONS, all_data)
schreibe(result["equity_curve"], "equity_curve.csv")
mo.STOP_LOSS_RANGE = [es.STOP_LOSS_PCT]
schreibe(mo.run_multi_optimisation(all_data), "optimierer.csv")
""",
}

KOPF = """
import os, sys, importlib
sys.path[:0] = [%(sd)r, %(sh)r]
import pandas as pd
AUS = %(aus)r
def schreibe(df, name):
    df.to_csv(os.path.join(AUS, name), index=False, float_format="%%.17g")
"""

KOPF_B6 = """
m = importlib.import_module(%(mod)r)
from strategy_paths import get_strategy_paths
D = get_strategy_paths(m.__file__)["DATA_DIR"]
"""

KOPF_PFAD = """
import equity_simulation as es
import multi_symbol_optimise as mo
all_data = es.load_all_symbol_data()
"""


def lauf(bot, code, sd, log):
    t0 = time.time()
    with open(log, "a") as f:
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", code], cwd=sd,
                           stdout=f, stderr=subprocess.PIPE, text=True)
    return r, time.time() - t0


def main():
    aus = os.path.abspath(sys.argv[1])
    for bot in B6:
        sd = os.path.join(REPO, "strategies", bot)
        ziel = os.path.join(aus, bot)
        os.makedirs(ziel, exist_ok=True)
        log = os.path.join(ziel, "lauf.log")
        kopf = KOPF % dict(sd=sd, sh=os.path.join(REPO, "shared"), aus=ziel)
        mod, rumpf = B6[bot]
        r1, t1 = lauf(bot, kopf + KOPF_B6 % dict(mod=mod) + rumpf + '\nschreibe(trades, "b6.csv")\n', sd, log)
        r2, t2 = lauf(bot, kopf + KOPF_PFAD + PFAD[bot], sd, log)
        print("=== %s  b6 rc=%d (%.0f s)  pfad rc=%d (%.0f s)" % (bot, r1.returncode, t1, r2.returncode, t2))
        for r in (r1, r2):
            if r.returncode:
                print(r.stderr.rstrip()[-1500:])
        for name in sorted(os.listdir(ziel)):
            if name.endswith(".csv"):
                with open(os.path.join(ziel, name), "rb") as f:
                    print("%s  %s/%s" % (hashlib.sha256(f.read()).hexdigest(), bot, name))


if __name__ == "__main__":
    main()

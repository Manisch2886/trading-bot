#!/usr/bin/env python3
"""TB-90 B4/B5/B6 - ein Backtest je Bot, Ergebnis byte-genau auf Platte.

Aufruf: b6_backtest_lauf.py <ausgabeordner>
Je Bot ein eigener Unterprozess (die Modulnamen backtest_rsi2, indicators,
live_params gibt es mehrfach), cwd = Strategieordner, sys.path = [Strategie-
ordner, shared/] wie bei den Aufrufern (multi_symbol_optimise.py u. a.). Der
Aufruf je Bot folgt dem __main__-Zweig des Moduls (t3_supertrend hat keinen:
run_backtest(price_df) mit Defaults auf BTCUSDT_4h, wie optimise_trend.py).
Schreibt <bot>.csv (trades.to_csv, float_format %.17g) und druckt je Bot
Modulpfad, TRADING_FEE_PCT, SLIPPAGE_PCT, Herkunftsmodul der Werte,
Tradeanzahl und SHA-256 der CSV. Nur lesend gegenueber dem Repo.
"""
import hashlib
import os
import subprocess
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

AUFRUF = {
    "elliott_wave": ("backtest_elliott", """
from zigzag_indicator import calculate_zigzag_with_confirmation
from elliott_wave_counter import find_causal_waves
price_df = pd.read_csv(os.path.join(D, "BTCUSDT_1h.csv"), parse_dates=["open_time"])
z = calculate_zigzag_with_confirmation(price_df, deviation_pct=4.0)
imp = find_causal_waves(z, min_fib_score=0.3, freshness_bars=m.SIGNAL_FRESHNESS_BARS, direction="bearish")
trades = m.run_backtest(price_df, imp)
"""),
    "elliott_wave_stocks": ("backtest_elliott", """
from zigzag_indicator import calculate_zigzag_with_confirmation
from elliott_wave_counter import find_causal_waves
price_df = pd.read_csv(os.path.join(D, "AAPL_1d.csv"), parse_dates=["open_time"])
z = calculate_zigzag_with_confirmation(price_df, deviation_pct=5.0)
imp = find_causal_waves(z, min_fib_score=0.3, freshness_bars=m.SIGNAL_FRESHNESS_BARS, direction="bearish")
trades = m.run_backtest(price_df, imp)
"""),
    "rsi2_crypto": ("backtest_rsi2", """
price_df = pd.read_csv(os.path.join(D, "BTCUSDT_1d.csv"), parse_dates=["open_time"])
df = m.compute_indicators(price_df, sma_trend_period=200)
trades = m.run_backtest(df, rsi_threshold=5.0, sma_trend_period=200, stop_loss_pct=5.0)
"""),
    "rsi2_mean_reversion": ("backtest_rsi2", """
price_df = pd.read_csv(os.path.join(D, "AAPL_1d.csv"), parse_dates=["open_time"])
df = m.compute_indicators(price_df)
trades = m.run_backtest(df, rsi_threshold=5.0, stop_loss_pct=5.0)
"""),
    "t3_supertrend": ("backtest_trend", """
price_df = pd.read_csv(os.path.join(D, "BTCUSDT_4h.csv"), parse_dates=["open_time"])
trades = m.run_backtest(price_df)
"""),
    "turtle_soup_crypto": ("backtest_turtle_soup", """
price_df = pd.read_csv(os.path.join(D, "BTCUSDT_1d.csv"), parse_dates=["open_time"])
df = m.compute_indicators(price_df)
trades = m.run_backtest(df, stop_mode="structural")
"""),
    "turtle_soup_stocks": ("backtest_turtle_soup", """
price_df = pd.read_csv(os.path.join(D, "AAPL_1d.csv"), parse_dates=["open_time"])
df = m.compute_indicators(price_df)
trades = m.run_backtest(df, stop_mode="structural")
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

KOPF = """
import os, sys, importlib
sys.path[:0] = [%(sd)r, %(sh)r]
import pandas as pd
m = importlib.import_module(%(mod)r)
from strategy_paths import get_strategy_paths
D = get_strategy_paths(m.__file__)["DATA_DIR"]
"""

FUSS = """
herkunft = sys.modules.get("handelskosten")
print("modul=%%s" %% os.path.relpath(m.__file__, %(repo)r))
print("TRADING_FEE_PCT=%%r SLIPPAGE_PCT=%%r" %% (m.TRADING_FEE_PCT, m.SLIPPAGE_PCT))
print("handelskosten geladen: %%s" %% (os.path.relpath(herkunft.__file__, %(repo)r) if herkunft else "nein"))
print("trades=%%d" %% len(trades))
trades.to_csv(%(aus)r, index=False, float_format="%%.17g")
"""


def main():
    aus = os.path.abspath(sys.argv[1])
    os.makedirs(aus, exist_ok=True)
    for bot, (mod, rumpf) in AUFRUF.items():
        sd = os.path.join(REPO, "strategies", bot)
        ziel = os.path.join(aus, bot + ".csv")
        code = (KOPF % dict(sd=sd, sh=os.path.join(REPO, "shared"), mod=mod)
                + rumpf + FUSS % dict(repo=REPO, aus=ziel))
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", code], cwd=sd,
                           capture_output=True, text=True)
        print("=== %s  rc=%d" % (bot, r.returncode))
        print(r.stdout.rstrip())
        if r.returncode:
            print(r.stderr.rstrip()[-1500:])
            continue
        with open(ziel, "rb") as f:
            print("sha256=%s" % hashlib.sha256(f.read()).hexdigest())


if __name__ == "__main__":
    main()

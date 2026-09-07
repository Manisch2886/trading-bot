"""
Bleibt die Parameterwahl dieselbe? (Frage 4, zweiter Teil)
====================================================================================
Die live gesetzten Parameter beider Elliott-Wave-Bots (`DEVIATION_PCT`,
`STOP_LOSS_PCT`, `TAKE_PROFIT_FIB`) stammen aus der Rasteroptimierung in
`multi_symbol_optimise.py`. Diese Rasteroptimierung lief auf der
Backtest-Grundlage - also MIT dem Zigzag-Look-Ahead.

Dieses Skript wiederholt das komplette Raster einmal auf der Baseline und
einmal auf der korrigierten Grundlage und vergleicht, welche Kombination
jeweils gewinnt. Bewertungsmass, Mindestfilter und Sortierung sind
woertlich aus `multi_symbol_optimise.py` uebernommen:

    robustness_score = avg_return_pct * sqrt(num_trades) / |max_drawdown_pct|

samt MIN_TRADES, MIN_SYMBOLS_CONTRIBUTING und MIN_AVG_RETURN_PCT. Auch der
dort verwendete Drawdown auf der KUMULIERTEN PnL-Reihe (nicht auf der
Kapitalkurve) wird beibehalten - er ist Teil des Bewertungsmasses, das die
Entscheidung getragen hat.

Laufzeit-Hinweis: Zigzag und Wellenerkennung haengen NUR von
`deviation_pct` ab, nicht von Stop oder Take-Profit. Sie werden deshalb je
(Symbol, deviation_pct) einmal berechnet und fuer alle Stop/TP-Kombinationen
wiederverwendet - dasselbe Ergebnis, ein Bruchteil der Rechenzeit.

Nutzung:  python3 grid.py <bot_name>
"""

import json
import os
import sys

import numpy as np
import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import run_one_bot as rob   # noqa: E402

BOT = rob.BOT
RESULTS_DIR = rob.RESULTS_DIR
BASES = (rob.VARIANT_BASELINE, rob.VARIANT_CORRECTED)


def robustness_score(avg_return_pct, num_trades, max_drawdown_pct):
    """Woertlich aus multi_symbol_optimise.calculate_robustness_score."""
    penalty = abs(max_drawdown_pct) if max_drawdown_pct != 0 else 1.0
    return round((avg_return_pct * (num_trades ** 0.5)) / penalty, 3)


def evaluate_combo(trades: pd.DataFrame, mo, deviation_pct, stop_loss_pct, take_profit_fib):
    """Woertlich aus multi_symbol_optimise.evaluate_combination_multi -
    inklusive der drei Mindestfilter, die eine Kombination ausschliessen."""
    if trades is None or trades.empty:
        return None
    contributing = trades["symbol"].nunique()
    if len(trades) < mo.MIN_TRADES or contributing < mo.MIN_SYMBOLS_CONTRIBUTING:
        return None
    avg_return = float(trades["pnl_pct"].mean())
    if avg_return < mo.MIN_AVG_RETURN_PCT:
        return None
    cum = trades["pnl_pct"].cumsum()
    max_dd = float((cum - cum.cummax()).min())
    return {
        "deviation_pct": deviation_pct, "stop_loss_pct": stop_loss_pct,
        "take_profit_fib": take_profit_fib,
        "num_trades": int(len(trades)), "num_symbols": int(contributing),
        "win_rate": round(float((trades["pnl_pct"] > 0).mean() * 100), 1),
        "total_return_pct": round(float(trades["pnl_pct"].sum()), 2),
        "avg_return_pct": round(avg_return, 2),
        "max_drawdown_pct": round(max_dd, 2),
        "robustness_score": robustness_score(avg_return, len(trades), max_dd),
    }


def waves_cache(all_data, deviation_pct, counter):
    """Zigzag + Wellenerkennung je Symbol - einmal pro deviation_pct."""
    cache = {}
    for symbol, price_df in all_data.items():
        impulses, _z = rob.build_waves(price_df, deviation_pct, counter)
        cache[symbol] = impulses
    return cache


def trades_from_cache(all_data, cache, cfg, variant, use_tp):
    """Wie run_one_bot.collect, aber auf bereits berechneten Wellen."""
    rows = []
    for symbol, price_df in all_data.items():
        impulses = cache[symbol]
        if impulses is None or impulses.empty:
            continue
        closes = price_df["close"].values
        times = price_df["open_time"].values
        for _, wave in impulses.iterrows():
            pivot_idx, confirm_idx = int(wave["pivot_idx"]), int(wave["confirm_idx"])
            if variant == rob.VARIANT_BASELINE:
                entry_idx, entry_price = pivot_idx, float(wave["wave5"])
            else:
                entry_idx = confirm_idx
                if entry_idx >= len(price_df) or entry_idx - pivot_idx > cfg["freshness_bars"]:
                    continue
                entry_price = float(closes[entry_idx])
            total_move = abs(float(wave["wave5"]) - float(wave["wave0"]))
            target = (entry_price + total_move * cfg["take_profit_fib"]
                      if use_tp else float("inf"))
            stop = entry_price * (1 - cfg["stop_loss_pct"] / 100.0)
            outcome = rob.simulate_exit(price_df, entry_idx, entry_price, target, stop,
                                         cfg["max_hold_bars"], use_tp)
            if outcome is None:
                continue
            gross = (outcome["exit_price"] - entry_price) / entry_price * 100
            rows.append({"symbol": symbol, "entry_time": pd.Timestamp(times[entry_idx]),
                         "pnl_pct": round(gross - cfg["cost_pct"], 2)})
    if not rows:
        return pd.DataFrame()
    # Dieselbe chronologische Reihenfolge wie im Original (dort ueber
    # pd.concat der Symbol-Bloecke); der Drawdown des Bewertungsmasses
    # laeuft auf der kumulierten PnL-Reihe, ist also reihenfolgeabhaengig.
    return pd.DataFrame(rows)


def main():
    import live_params as lp
    import elliott_wave_counter as counter
    import backtest_elliott as bt
    import multi_symbol_optimise as mo
    import equity_simulation as es

    use_tp = bool(getattr(lp, "USE_TAKE_PROFIT", True))
    all_data = es.load_all_symbol_data()

    live_combo = (float(lp.DEVIATION_PCT), float(lp.STOP_LOSS_PCT), float(lp.TAKE_PROFIT_FIB))
    print(f"{BOT}: Raster {len(mo.DEVIATION_RANGE)}x{len(mo.STOP_LOSS_RANGE)}"
          f"x{len(mo.TAKE_PROFIT_FIB_RANGE)} = "
          f"{len(mo.DEVIATION_RANGE) * len(mo.STOP_LOSS_RANGE) * len(mo.TAKE_PROFIT_FIB_RANGE)} "
          f"Kombinationen auf {len(all_data)} Symbolen, live gesetzt: {live_combo}")

    tables = {basis: [] for basis in BASES}
    for deviation_pct in mo.DEVIATION_RANGE:
        cache = waves_cache(all_data, deviation_pct, counter)
        for stop_loss_pct in mo.STOP_LOSS_RANGE:
            for take_profit_fib in mo.TAKE_PROFIT_FIB_RANGE:
                cfg = {"deviation_pct": deviation_pct, "stop_loss_pct": stop_loss_pct,
                       "take_profit_fib": take_profit_fib,
                       "max_hold_bars": int(bt.MAX_HOLD_HOURS),
                       "cost_pct": 2 * (bt.TRADING_FEE_PCT + bt.SLIPPAGE_PCT),
                       "freshness_bars": rob.FRESHNESS_BARS[BOT]}
                for basis in BASES:
                    trades = trades_from_cache(all_data, cache, cfg, basis, use_tp)
                    row = evaluate_combo(trades, mo, deviation_pct, stop_loss_pct, take_profit_fib)
                    if row:
                        tables[basis].append(row)
        print(f"  deviation {deviation_pct} % fertig")

    out = {"bot": BOT, "live_kombination": {"deviation_pct": live_combo[0],
                                             "stop_loss_pct": live_combo[1],
                                             "take_profit_fib": live_combo[2]},
           "use_take_profit": use_tp, "raster": {}}

    for basis in BASES:
        df = pd.DataFrame(tables[basis])
        if df.empty:
            print(f"\n{basis}: KEINE Kombination erfuellt die Mindestfilter "
                  f"(MIN_TRADES={mo.MIN_TRADES}, MIN_SYMBOLS={mo.MIN_SYMBOLS_CONTRIBUTING}, "
                  f"MIN_AVG_RETURN={mo.MIN_AVG_RETURN_PCT} %)")
            out["raster"][basis] = {"bestandene_kombinationen": 0, "sieger": None, "top5": []}
            continue
        df = df.sort_values("robustness_score", ascending=False).reset_index(drop=True)
        winner = df.iloc[0].to_dict()
        live_row = df[(df["deviation_pct"] == live_combo[0])
                      & (df["stop_loss_pct"] == live_combo[1])
                      & (df["take_profit_fib"] == live_combo[2])]
        out["raster"][basis] = {
            "bestandene_kombinationen": int(len(df)),
            "sieger": winner,
            "live_kombination_rang": (int(live_row.index[0]) + 1 if len(live_row) else None),
            "live_kombination_zeile": (live_row.iloc[0].to_dict() if len(live_row) else None),
            "top5": df.head(5).to_dict("records"),
        }
        print(f"\n{basis}: {len(df)} von "
              f"{len(mo.DEVIATION_RANGE) * len(mo.STOP_LOSS_RANGE) * len(mo.TAKE_PROFIT_FIB_RANGE)} "
              f"Kombinationen bestehen die Mindestfilter")
        print(f"  {'Rang':<6}{'dev':>6}{'stop':>7}{'fib':>8}{'Trades':>9}{'Ø PnL':>9}"
              f"{'Max DD':>10}{'Score':>10}")
        for i, row in df.head(5).iterrows():
            mark = " <- live" if (row["deviation_pct"], row["stop_loss_pct"],
                                   row["take_profit_fib"]) == live_combo else ""
            print(f"  {i + 1:<6}{row['deviation_pct']:>6.1f}{row['stop_loss_pct']:>7.1f}"
                  f"{row['take_profit_fib']:>8.3f}{row['num_trades']:>9}{row['avg_return_pct']:>9.2f}"
                  f"{row['max_drawdown_pct']:>10.2f}{row['robustness_score']:>10.3f}{mark}")
        rank = out["raster"][basis]["live_kombination_rang"]
        print(f"  Live-Kombination {live_combo}: "
              + (f"Rang {rank} von {len(df)}" if rank else
                 "faellt durch die Mindestfilter (waere nie gewaehlt worden)"))

    path = os.path.join(RESULTS_DIR, f"{BOT}_grid.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {path}")


if __name__ == "__main__":
    main()

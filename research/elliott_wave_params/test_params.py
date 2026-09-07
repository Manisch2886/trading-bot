"""
Selbsttests der Parameter-Neubestimmung
====================================================================
Prueft die Behauptungen, auf denen diese Untersuchung steht - jede
einzeln, mit Abbruch beim ersten Fehlschlag. Wichtigster Punkt: der
Rechenkern hier ist KEINE Nachbildung des Bots, sondern ruft dessen
Code auf. Genau das wird gegengeprueft, statt es zu behaupten.

Nutzung:  python3 test_params.py <elliott_wave|elliott_wave_stocks>
"""

import os
import subprocess
import sys

import numpy as np
import pandas as pd

import botenv

BOT = botenv.bot_from_argv()

import engine    # noqa: E402
import search    # noqa: E402
import walkforward as wf   # noqa: E402
import equity_simulation as es          # noqa: E402
import multi_symbol_optimise as mo      # noqa: E402
import multi_symbol_walk_forward as mwf  # noqa: E402

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"  [{'OK ' if ok else 'FEHLER'}] {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        raise SystemExit(f"\nFEHLGESCHLAGEN: {name}\n{detail}")


def main():
    botenv.print_hinweis()
    print(f"\n{BOT}: Selbsttests\n")
    windows = engine.load_windows()
    full = windows[engine.WINDOW_FULL]
    live = engine.live_combo()

    # 1 - Suchraum enthaelt die aktuelle Live-Kombination
    keys = {(d, s, f, u) for d in search.DEVIATION_RANGE
            for s in search.STOP_LOSS_RANGE for f, u in search.TARGET_RANGE}
    live_key = (live["deviation_pct"], live["stop_loss_pct"],
                live["take_profit_fib"], live["use_take_profit"])
    check("Suchraum enthaelt die aktuelle Live-Kombination", live_key in keys, str(live_key))
    check("Suchraum ist deutlich groesser als das alte Raster",
          len(keys) >= 4 * len(mo.DEVIATION_RANGE) * len(mo.STOP_LOSS_RANGE),
          f"{len(keys)} Kombinationen")

    # 2 - Wellen-Cache liefert dasselbe wie eine frische Berechnung
    dev = live["deviation_pct"]
    cached = engine.waves_for(engine.WINDOW_FULL, full, dev, use_cache=True)
    fresh = engine.waves_for(engine.WINDOW_FULL, full, dev, use_cache=False)
    same = all(len(cached[s]) == len(fresh[s]) for s in fresh) and set(cached) == set(fresh)
    if same:
        for s in fresh:
            if not fresh[s].empty:
                same = same and fresh[s]["entry_idx"].tolist() == cached[s]["entry_idx"].tolist()
    check("Wellen-Cache identisch zur frischen Berechnung", same,
          f"{sum(len(w) for w in fresh.values())} Wellen")

    # 3 - Trades identisch zum Bot-eigenen collect_all_trades
    engine_trades = engine.collect_trades(full, cached, live["stop_loss_pct"],
                                           live["take_profit_fib"], live["use_take_profit"])
    args = [full, live["deviation_pct"], live["stop_loss_pct"], live["take_profit_fib"]]
    if engine.SUPPORTS_NO_TP:
        args.append(live["use_take_profit"])
    bot_trades = es.collect_all_trades(*args)
    cols = ["symbol", "signal_time", "entry_time", "entry_price",
            "exit_time", "exit_price", "result", "pnl_pct"]
    a = engine_trades[cols].sort_values(cols, kind="stable").reset_index(drop=True)
    b = bot_trades[cols].sort_values(cols, kind="stable").reset_index(drop=True)
    check("Trade-Satz identisch zum Bot (equity_simulation.collect_all_trades)",
          len(a) == len(b) and a.equals(b), f"{len(a)} Trades")

    # 4 - Reihenfolge: der Bot sortiert instabil, hier wird stabil sortiert.
    #     Der Unterschied wird gemessen und ausgewiesen, nicht verschwiegen.
    pf_engine = engine.portfolio(engine_trades)
    pf_bot = engine.portfolio(bot_trades)
    delta = round(pf_engine["total_return_pct"] - pf_bot["total_return_pct"], 2)
    if engine.SUPPORTS_POSITION_LIMIT and engine.MAX_CONCURRENT is not None:
        check("Reihenfolge-Abweichung zum Bot gemessen und ausgewiesen", True,
              f"stabil {pf_engine['total_return_pct']} % vs. Bot {pf_bot['total_return_pct']} % "
              f"(Differenz {delta:+} pp, nur durch Zeilenreihenfolge bei Positionslimit "
              f"{engine.MAX_CONCURRENT})")
    else:
        check("ohne Positionslimit ist die Reihenfolge ohne Einfluss", delta == 0.0,
              f"Differenz {delta} pp")

    # 5 - Bewertungsmass woertlich wie im Bot
    rng = np.random.default_rng(1)
    ok = True
    for _ in range(200):
        avg = float(rng.uniform(-10, 10))
        n = int(rng.integers(1, 900))
        dd = float(rng.uniform(-500, 0))
        row = {"avg_return_pct": avg, "num_trades": n, "max_drawdown_pct": dd}
        ok = ok and engine.robustness_score(avg, n, dd) == mo.calculate_robustness_score(row)
    check("robustness_score identisch zu multi_symbol_optimise", ok, "200 Zufallsfaelle")

    # 6 - Mindestfilter identisch zur Annahme/Ablehnung des Bots
    scored = engine.score_trades(engine_trades)
    bot_row = mo.evaluate_combination_multi(
        full, live["deviation_pct"], live["stop_loss_pct"], live["take_profit_fib"],
        *([live["use_take_profit"]] if engine.SUPPORTS_NO_TP else []))
    check("Mindestfilter-Entscheidung identisch zum Bot",
          scored["besteht_mindestfilter"] == (bot_row is not None),
          f"engine={scored['besteht_mindestfilter']}, bot={'angenommen' if bot_row else 'abgelehnt'}")
    if bot_row is not None:
        same = all(abs(float(bot_row[k]) - float(scored[k])) < 1e-9
                   for k in ("num_trades", "num_symbols", "win_rate", "total_return_pct",
                              "avg_return_pct", "max_drawdown_pct", "robustness_score"))
        check("Kennzahlen identisch zum Bot-eigenen Raster", same, str(bot_row))

    # 7 - Fenster-Split woertlich wie multi_symbol_walk_forward
    tr, te = mwf.split_all_symbols(full, mwf.TRAIN_SPLIT_RATIO)
    ok = (set(tr) == set(windows[engine.WINDOW_IS])
          and all(len(tr[s]) == len(windows[engine.WINDOW_IS][s]) for s in tr)
          and all(len(te[s]) == len(windows[engine.WINDOW_OOS][s]) for s in te))
    check("IS/OOS-Split identisch zu multi_symbol_walk_forward.split_all_symbols", ok,
          f"Verhaeltnis {mwf.TRAIN_SPLIT_RATIO}")

    # 8 - Fenster sind disjunkt und luecklos
    ok = True
    for s in full:
        n_is, n_oos = len(windows[engine.WINDOW_IS][s]), len(windows[engine.WINDOW_OOS][s])
        ok = ok and n_is + n_oos == len(full[s])
        ok = ok and (windows[engine.WINDOW_OOS][s]["open_time"].iloc[0]
                     > windows[engine.WINDOW_IS][s]["open_time"].iloc[-1])
    check("In-Sample und Out-of-Sample sind disjunkt und lueckenlos", ok)

    # 9 - Walk-Forward-Falten ueberlappen nicht mit ihrem Testfenster
    fold_windows, folds = wf.build_folds(full)
    ok = True
    for f in folds:
        for s in fold_windows[f["test"]]:
            if s not in fold_windows[f["train"]]:
                continue
            ok = ok and (fold_windows[f["test"]][s]["open_time"].iloc[0]
                         > fold_windows[f["train"]][s]["open_time"].iloc[-1])
    check("jedes Walk-Forward-Testfenster liegt vollstaendig NACH seinem Trainingsfenster", ok,
          f"{len(folds)} Falten")

    # 10 - Kausalitaet der verwendeten Trades (Kurzform von PR #26)
    ok_price, ok_order = True, True
    for symbol, wave_df in cached.items():
        if wave_df.empty:
            continue
        closes = full[symbol]["close"].values
        times = pd.to_datetime(full[symbol]["open_time"]).values
        sub = engine_trades[engine_trades["symbol"] == symbol]
        by_time = dict(zip(pd.to_datetime(sub["entry_time"]), sub["entry_price"]))
        for _, w in wave_df.iterrows():
            t = pd.Timestamp(times[int(w["entry_idx"])])
            if t in by_time:
                ok_price = ok_price and abs(by_time[t] - closes[int(w["entry_idx"])]) < 1e-9
            ok_order = ok_order and int(w["entry_idx"]) >= int(w["pivot_idx"])
    check("Einstiegskurs ist der Schlusskurs des Einstiegsbalkens", ok_price)
    check("Einstieg liegt nie vor dem Wellenende", ok_order)
    check("alle Trades tragen signal_time <= entry_time",
          bool((pd.to_datetime(engine_trades["signal_time"])
                <= pd.to_datetime(engine_trades["entry_time"])).all()))

    # 11 - Buy-and-Hold gegen das Bot-eigene Skript (nur wo es existiert)
    bh = engine.buy_and_hold(full)
    bh_path = os.path.join(botenv.REPO_ROOT, "strategies", BOT, "buy_and_hold_benchmark.py")
    if os.path.exists(bh_path):
        import buy_and_hold_benchmark as bhb
        ref = bhb.calculate_buy_and_hold(full, es.STARTING_CAPITAL)
        same = (abs(ref["total_return_pct"] - bh["total_return_pct"]) < 0.01
                and abs(ref["max_drawdown_pct"] - bh["max_drawdown_pct"]) < 0.01)
        check("Buy-and-Hold identisch zum Bot-eigenen buy_and_hold_benchmark.py", same,
              f"{bh['total_return_pct']} % / {bh['max_drawdown_pct']} %")
    else:
        check("Buy-and-Hold berechnet (Bot hat kein eigenes Vergleichsskript)",
              bh is not None, f"{bh['total_return_pct']} % / {bh['max_drawdown_pct']} %")

    # 12 - Ersatz fuer "kein Ziel" beim Krypto-Bot wirkt tatsaechlich.
    #      Geprueft wird die unguenstigste Ecke des Suchraums: der
    #      feinste Zigzag erzeugt die kleinsten Impulsbewegungen und
    #      damit die naechstliegenden Ziele, der weiteste Stop laesst
    #      die Trades am laengsten laufen.
    if not engine.SUPPORTS_NO_TP:
        worst_dev = min(search.DEVIATION_RANGE)
        waves = engine.waves_for(engine.WINDOW_FULL, full, worst_dev)
        shares = {}
        for stop in (min(search.STOP_LOSS_RANGE), max(search.STOP_LOSS_RANGE)):
            sc = engine.score_trades(
                engine.collect_trades(full, waves, stop, search.NO_TARGET_FIB, True))
            shares[stop] = sc["share_take_profit_pct"] if sc else 0.0
        check(f"Fib {search.NO_TARGET_FIB:g} wirkt wie 'kein Ziel'",
              all(v == 0.0 for v in shares.values()),
              f"Take-Profit-Anteil bei deviation {worst_dev:g} %: "
              + ", ".join(f"Stop {k:g} % -> {v} %" for k, v in shares.items()))

    # 12b - keine NaN-Kennzahl mehr: Trades mit Kursluecke sind
    #       gestrichen, und die Streichung ist ausgewiesen statt still
    ok = not engine_trades[["entry_price", "exit_price", "pnl_pct"]].isna().any().any()
    check("kein Trade mit fehlendem Kurs bleibt in der Auswertung", ok,
          f"gestrichen: {engine.datenluecken_bericht()}")
    pf = engine.portfolio(engine_trades)
    check("Portfolio-Kennzahlen sind Zahlen, kein NaN",
          all(v == v for v in (pf["total_return_pct"], pf["max_drawdown_pct"])),
          f"{pf['total_return_pct']} % / {pf['max_drawdown_pct']} %")

    # 13 - keine Live-Datei angefasst
    diff = subprocess.run(
        ["git", "-C", botenv.REPO_ROOT, "diff", "--stat", "HEAD", "--",
         "strategies/elliott_wave/live_params.py",
         "strategies/elliott_wave/forward_test.py",
         "strategies/elliott_wave_stocks/live_params.py",
         "strategies/elliott_wave_stocks/forward_test.py"],
        capture_output=True, text=True)
    check("live_params.py und forward_test.py unveraendert",
          diff.returncode == 0 and diff.stdout.strip() == "",
          diff.stdout.strip() or "leerer Diff")

    print(f"\n{sum(1 for _n, ok, _d in CHECKS if ok)}/{len(CHECKS)} Pruefungen bestanden.")


if __name__ == "__main__":
    main()

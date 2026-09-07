"""
Parameter-Neubestimmung - Rastersuche auf kausal sauberer Grundlage
====================================================================
Rechnet fuer EINEN Bot den erweiterten Suchraum auf drei Fenstern
durch (gesamt / In-Sample / Out-of-Sample) und schreibt alles nach
results/<bot>_search.json und results/<bot>_grid_<fenster>.csv.

--------------------------------------------------------------------
Warum dieser Suchraum
--------------------------------------------------------------------
Das bisherige Raster (36 bzw. 64 Kombinationen) lag eng um Werte
herum, die auf der look-ahead-behafteten Grundlage gewonnen wurden -
also um eine Mitte, die sich als ungeeignet herausgestellt hat. Ein
Raster um einen falschen Mittelpunkt findet bestenfalls den besten
falschen Punkt. Der Suchraum wird deshalb in alle drei Richtungen
geoeffnet, und zwar dort, wo es einen sachlichen Grund gibt:

* deviation_pct bis 10 %: der Zigzag bestimmt, WAS ueberhaupt als
  Welle zaehlt. Mit dem korrigierten Einstieg kostet jede Bestaetigung
  Kursbewegung - grobere Zigzags erzeugen weniger, dafuer groessere
  Muster, bei denen dieser Aufschlag relativ kleiner ausfaellt. Das ist
  die Richtung, die das alte Raster (max. 5 %) gar nicht kannte.
* stop_loss_pct bis 12 % (Krypto) bzw. 16 % (Aktien): der Stop war im
  alten Backtest bis zur Bestaetigung mathematisch unerreichbar - er
  war faktisch nie bindend und konnte deshalb beliebig eng gewaehlt
  werden. Auf sauberer Grundlage ist er sofort bindend; die live
  gesetzten 2 bzw. 3 % sind auf Stundenkerzen (Krypto) enger als das
  normale Rauschen. Weite Stops sind damit die naheliegendste
  ungetestete Richtung.
* take_profit_fib bis 1.0 plus eine Variante ohne Ziel: der
  Aktien-Bot hat "Gewinne laufen lassen" bereits als klar besser
  gemessen (USE_TAKE_PROFIT=False). Fuer den Krypto-Bot ist das nie
  geprueft worden, weil dessen run_backtest kein solches Flag kennt.
  Ein unerreichbar hohes Fibonacci-Ziel (100.0) ist dort das
  Aequivalent. Dass es tatsaechlich nie erreicht wird, ist gemessen und
  nicht angenommen: test_params.py prueft die Ecken des Suchraums, und
  share_take_profit_pct steht in jeder Ergebniszeile. Zum Vergleich:
  bei Fib 5.0 laufen je nach Einstellung noch bis zu 2,8 % der Trades
  ins Ziel, bei Fib 20.0 noch 0,2 % - beides waere also kein sauberes
  "kein Ziel".

252 Kombinationen je Fenster und Bot - rund das Siebenfache des alten
Rasters, aber immer noch klein genug, dass jede einzelne Kombination
nachrechenbar bleibt.

Nutzung:  python3 search.py <elliott_wave|elliott_wave_stocks>
"""

import json
import multiprocessing as mp
import os
import time

import pandas as pd

import botenv

BOT = botenv.bot_from_argv()

import engine   # noqa: E402  - erst nach botenv.setup importierbar

# --- Suchraum -------------------------------------------------------
DEVIATION_RANGE = [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]
STOP_LOSS_RANGE = {
    "elliott_wave": [2.0, 3.0, 4.0, 6.0, 8.0, 12.0],
    "elliott_wave_stocks": [2.0, 3.0, 5.0, 8.0, 12.0, 16.0],
}[BOT]

# (take_profit_fib, use_take_profit) - der Aktien-Bot kann das Ziel
# nativ abschalten, der Krypto-Bot nicht (siehe Modulkopf).
NO_TARGET_FIB = 100.0
TARGET_RANGE = [(fib, True) for fib in (0.236, 0.382, 0.5, 0.618, 1.0)]
TARGET_RANGE += [(0.236, False)] if engine.SUPPORTS_NO_TP else [(NO_TARGET_FIB, True)]

WINDOWS = (engine.WINDOW_FULL, engine.WINDOW_IS, engine.WINDOW_OOS)
N_WORKERS = min(4, os.cpu_count() or 1)

_DATA = {}      # im Elternprozess gefuellt, per fork an die Worker vererbt


def combos():
    for deviation_pct in DEVIATION_RANGE:
        for stop_loss_pct in STOP_LOSS_RANGE:
            for take_profit_fib, use_tp in TARGET_RANGE:
                yield (deviation_pct, stop_loss_pct, take_profit_fib, use_tp)


def _build_cache(task):
    window, deviation_pct = task
    t0 = time.time()
    engine.waves_for(window, _DATA[window], deviation_pct)
    return window, deviation_pct, round(time.time() - t0, 1)


def _run_combo(task):
    window, deviation_pct, stop_loss_pct, take_profit_fib, use_tp = task
    all_data = _DATA[window]
    waves = engine.waves_for(window, all_data, deviation_pct)
    trades = engine.collect_trades(all_data, waves, stop_loss_pct, take_profit_fib, use_tp)
    row = {"window": window, "deviation_pct": deviation_pct,
           "stop_loss_pct": stop_loss_pct, "take_profit_fib": take_profit_fib,
           "use_take_profit": use_tp}
    scored = engine.score_trades(trades)
    if scored is None:
        row.update({"num_trades": 0, "besteht_mindestfilter": False})
        return row
    row.update(scored)
    row.update({f"pf_{k}": v for k, v in (engine.portfolio(trades) or {}).items()})
    return row


def main():
    botenv.print_hinweis()
    t_start = time.time()
    _DATA.update(engine.load_windows())
    filters = engine.project_filters()
    live = engine.live_combo()

    print(f"{BOT}: {len(_DATA[engine.WINDOW_FULL])} Symbole, "
          f"{len(DEVIATION_RANGE)}x{len(STOP_LOSS_RANGE)}x{len(TARGET_RANGE)} = "
          f"{len(list(combos()))} Kombinationen je Fenster")
    print(f"  Mindestfilter: >= {filters['min_trades']} Trades, "
          f">= {filters['min_symbols']} Symbole, "
          f">= {filters['min_avg_return_pct']} % Ø PnL")
    print(f"  live gesetzt: {live}")
    for window in WINDOWS:
        start, end = engine.window_span(_DATA[window])
        print(f"  Fenster {window:<7} {start} bis {end}")

    ctx = mp.get_context("fork")

    print(f"\nWellen-Cache ({N_WORKERS} Prozesse)...")
    cache_tasks = [(w, d) for w in WINDOWS for d in DEVIATION_RANGE]
    with ctx.Pool(N_WORKERS) as pool:
        for window, deviation_pct, secs in pool.imap_unordered(_build_cache, cache_tasks):
            print(f"  {window:<7} deviation {deviation_pct:>4} %  {secs:>7.1f} s")

    print(f"\nRastersuche ({N_WORKERS} Prozesse)...")
    tasks = [(w,) + c for w in WINDOWS for c in combos()]
    rows = []
    with ctx.Pool(N_WORKERS) as pool:
        for i, row in enumerate(pool.imap_unordered(_run_combo, tasks, chunksize=4), 1):
            rows.append(row)
            if i % 100 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)} Kombinationen")

    df = pd.DataFrame(rows)
    out = {"hinweis": botenv.UNVALIDIERT_HINWEIS, "bot": BOT, "live_kombination": live, "mindestfilter": filters,
           "suchraum": {"deviation_pct": DEVIATION_RANGE,
                         "stop_loss_pct": STOP_LOSS_RANGE,
                         "ziel": [{"take_profit_fib": f, "use_take_profit": u}
                                  for f, u in TARGET_RANGE],
                         "kombinationen_je_fenster": len(list(combos()))},
           "train_split_ratio": engine.TRAIN_SPLIT_RATIO,
           "fenster": {}, "laufzeit_s": None}

    for window in WINDOWS:
        sub = df[df["window"] == window].copy()
        start, end = engine.window_span(_DATA[window])
        passed = sub[sub["besteht_mindestfilter"]].sort_values(
            "robustness_score", ascending=False).reset_index(drop=True)
        sub = sub.sort_values(["deviation_pct", "stop_loss_pct", "take_profit_fib"],
                              kind="stable").reset_index(drop=True)
        path = os.path.join(botenv.RESULTS_DIR, f"{BOT}_grid_{window}.csv")
        sub.to_csv(path, index=False)

        live_mask = ((sub["deviation_pct"] == live["deviation_pct"])
                     & (sub["stop_loss_pct"] == live["stop_loss_pct"])
                     & (sub["take_profit_fib"] == live["take_profit_fib"])
                     & (sub["use_take_profit"] == live["use_take_profit"]))
        live_row = sub[live_mask]
        live_rank = None
        if len(live_row):
            in_passed = passed[(passed["deviation_pct"] == live["deviation_pct"])
                               & (passed["stop_loss_pct"] == live["stop_loss_pct"])
                               & (passed["take_profit_fib"] == live["take_profit_fib"])
                               & (passed["use_take_profit"] == live["use_take_profit"])]
            live_rank = int(in_passed.index[0]) + 1 if len(in_passed) else None

        out["fenster"][window] = {
            "zeitraum": {"von": start, "bis": end},
            "symbole": len(_DATA[window]),
            "kombinationen": int(len(sub)),
            "bestehen_mindestfilter": int(len(passed)),
            "top10": passed.head(10).to_dict("records"),
            "live_kombination_rang": live_rank,
            "live_kombination_zeile": (live_row.iloc[0].to_dict() if len(live_row) else None),
        }

        print(f"\n{window}: {len(passed)} von {len(sub)} Kombinationen bestehen die Mindestfilter")
        if len(passed):
            print(f"  {'Rang':<5}{'dev':>6}{'stop':>7}{'ziel':>9}{'Trades':>8}{'Sym':>5}"
                  f"{'Ø PnL':>8}{'Score':>9}{'Calmar':>9}")
            for i, r in passed.head(10).iterrows():
                ziel = f"{r['take_profit_fib']:.3f}" if r["use_take_profit"] else "kein"
                cal = r.get("pf_calmar_ratio")
                print(f"  {i + 1:<5}{r['deviation_pct']:>6.1f}{r['stop_loss_pct']:>7.1f}"
                      f"{ziel:>9}{r['num_trades']:>8}{r['num_symbols']:>5}"
                      f"{r['avg_return_pct']:>8.2f}{r['robustness_score']:>9.3f}"
                      f"{(f'{cal:.2f}' if cal is not None else '-'):>9}")
        print(f"  Live-Kombination: " + (f"Rang {live_rank}" if live_rank
                                          else "faellt durch die Mindestfilter"))

    out["laufzeit_s"] = round(time.time() - t_start, 1)
    path = os.path.join(botenv.RESULTS_DIR, f"{BOT}_search.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {path}  ({out['laufzeit_s']} s)")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()

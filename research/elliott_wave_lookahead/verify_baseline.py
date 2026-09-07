"""
Regressionscheck: der Nachbau muss den Bot exakt treffen
====================================================================
Bevor irgendein Ergebnis dieser Untersuchung zaehlt, muessen zwei Dinge
belegt sein:

  1. Der Zigzag dieses Verzeichnisses (`zigzag_confirm.py`) liefert
     EXAKT dieselben Pivots wie der unveraenderte
     `strategies/<bot>/zigzag_indicator.py` - nur mit einer
     Zusatzspalte. Waere das nicht so, waere jede Aussage ueber
     "Bestaetigungszeitpunkte" wertlos.
  2. Der Trade-Nachbau (`run_one_bot.collect`, Variante "baseline")
     erzeugt Trade fuer Trade denselben Satz wie die bot-eigene
     `equity_simulation.collect_all_trades`. Erst damit ist gesichert,
     dass der Unterschied zwischen "baseline" und "korrigiert"
     ausschliesslich von der Korrektur kommt und nicht vom Nachbau.

Zusaetzlich werden die im Projekt veroeffentlichten Kennzahlen beider
Bots nachgerechnet.

Nutzung:  python3 verify_baseline.py <bot_name>
"""

import os
import sys

import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import run_one_bot as rob                                        # noqa: E402
from zigzag_confirm import calculate_zigzag_with_confirmation    # noqa: E402

BOT = rob.BOT
TOL = 0.011

# Veroeffentlichte Kennzahlen der jeweiligen Baseline.
# elliott_wave:        research/order_sensitivity/BERICHT.md (PR #23)
# elliott_wave_stocks: results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md,
#                      Abschnitt 3 (Take-Profit aus, Limit 8) - zugleich die
#                      Zahl, mit der die USE_TAKE_PROFIT-Entscheidung begruendet ist.
PUBLISHED = {
    "elliott_wave": {"trades": 783, "executed": 782, "return_pct": 2184.96, "drawdown_pct": -1.83},
    "elliott_wave_stocks": {"trades": 519, "executed": 288, "return_pct": 3084.09, "drawdown_pct": -9.79},
}

PASSED = FAILED = 0


def check(label, condition, detail=""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  OK     {label}")
    else:
        FAILED += 1
        print(f"  FEHLER {label}   {detail}")


def close(a, b, tol=TOL):
    return a is not None and b is not None and abs(a - b) <= tol


def main():
    import equity_simulation as es
    import live_params as lp
    import elliott_wave_counter as counter
    import backtest_elliott as bt
    from zigzag_indicator import calculate_zigzag

    use_tp = bool(getattr(lp, "USE_TAKE_PROFIT", True))
    cfg = {
        "deviation_pct": float(lp.DEVIATION_PCT),
        "stop_loss_pct": float(lp.STOP_LOSS_PCT),
        "take_profit_fib": float(lp.TAKE_PROFIT_FIB),
        "max_hold_bars": int(bt.MAX_HOLD_HOURS),
        "cost_pct": 2 * (bt.TRADING_FEE_PCT + bt.SLIPPAGE_PCT),
        "max_concurrent": getattr(es, "MAX_CONCURRENT_POSITIONS", None),
        "freshness_bars": rob.FRESHNESS_BARS[BOT],
    }
    all_data = es.load_all_symbol_data()

    print(f"\n1) Zigzag: {BOT} - Pivots identisch zur unveraenderten Bot-Funktion?")
    mismatches, checked_symbols, total_pivots = 0, 0, 0
    for symbol, price_df in all_data.items():
        theirs = calculate_zigzag(price_df, deviation_pct=cfg["deviation_pct"])
        mine = calculate_zigzag_with_confirmation(price_df, deviation_pct=cfg["deviation_pct"])
        checked_symbols += 1
        total_pivots += len(theirs)
        if len(theirs) != len(mine):
            mismatches += 1
            continue
        same = (list(pd.to_datetime(theirs["time"])) == list(pd.to_datetime(mine["time"]))
                and list(theirs["price"]) == list(mine["price"])
                and list(theirs["type"]) == list(mine["type"]))
        if not same:
            mismatches += 1
    check(f"{total_pivots} Pivots ueber {checked_symbols} Symbole exakt identisch",
          mismatches == 0, f"{mismatches} Symbole weichen ab")
    # Die Zusatzspalte muss auch inhaltlich stimmen: ein Pivot kann nie VOR
    # sich selbst bestaetigt werden.
    bad_order = 0
    for symbol, price_df in all_data.items():
        mine = calculate_zigzag_with_confirmation(price_df, deviation_pct=cfg["deviation_pct"])
        if len(mine) and (mine["confirm_idx"] < mine["pivot_idx"]).any():
            bad_order += 1
    check("Bestaetigung liegt nie vor dem Pivot selbst", bad_order == 0, f"{bad_order} Symbole")

    print(f"\n2) Trade-Satz: Nachbau gegen die bot-eigene collect_all_trades")
    if BOT == "elliott_wave_stocks":
        theirs = es.collect_all_trades(all_data, cfg["deviation_pct"], cfg["stop_loss_pct"],
                                        cfg["take_profit_fib"], use_tp)
    else:
        theirs = es.collect_all_trades(all_data, cfg["deviation_pct"], cfg["stop_loss_pct"],
                                        cfg["take_profit_fib"])
    mine = rob.collect(all_data, cfg, rob.VARIANT_BASELINE, counter, use_tp)
    check("Anzahl Trades identisch", len(theirs) == len(mine), f"{len(theirs)} vs {len(mine)}")

    key = ["symbol", "entry_time"]
    a = theirs.sort_values(key).reset_index(drop=True)
    b = mine.sort_values(key).reset_index(drop=True)
    merged = a.merge(b, on=key, how="outer", suffixes=("_bot", "_neu"), indicator=True)
    check("jeder Trade in beiden Saetzen vorhanden",
          (merged["_merge"] == "both").all(),
          str(merged["_merge"].value_counts().to_dict()))
    for col in ("entry_price", "exit_price", "pnl_pct"):
        deltas = (merged[f"{col}_bot"] - merged[f"{col}_neu"]).abs()
        check(f"{col} bei allen Trades identisch", float(deltas.max()) < 1e-9,
              f"groesste Abweichung {float(deltas.max())}")
    check("Ausstiegszeitpunkt bei allen Trades identisch",
          (pd.to_datetime(merged["exit_time_bot"]) == pd.to_datetime(merged["exit_time_neu"])).all())
    check("Ergebnis-Kategorie bei allen Trades identisch",
          (merged["result_bot"].astype(str) == merged["result_neu"].astype(str)).all())

    print(f"\n3) Veroeffentlichte Kennzahlen der Baseline")
    ref = PUBLISHED[BOT]
    row = rob.evaluate(theirs, es, cfg)
    check(f"Trades = {ref['trades']}", row["num_trades"] == ref["trades"], str(row["num_trades"]))
    check(f"ausgefuehrt = {ref['executed']}", row["num_executed"] == ref["executed"],
          str(row["num_executed"]))
    check(f"Rendite = {ref['return_pct']} %", close(row["total_return_pct"], ref["return_pct"]),
          str(row["total_return_pct"]))
    check(f"Max Drawdown = {ref['drawdown_pct']} %",
          close(row["max_drawdown_pct"], ref["drawdown_pct"]), str(row["max_drawdown_pct"]))

    print("\n" + "=" * 72)
    print(f"{PASSED} Checks bestanden, {FAILED} fehlgeschlagen.")
    print("Nachbau exakt - Ergebnisse dieser Untersuchung sind belastbar." if not FAILED
          else "ABWEICHUNG - Ergebnisse dieser Untersuchung sind NICHT belastbar.")
    print("=" * 72)
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()

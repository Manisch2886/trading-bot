"""
Hauptlauf je Bot: Raster einmal rechnen, viermal bewerten
====================================================================
Aufruf:  python3 analyse.py <bot> [--fenster gesamt|is] [--permutationen N]
                          [--ohne-regimefilter]   (nur t3_supertrend)

  --fenster gesamt   das volle Raster, wie multi_symbol_optimise.py es
                     rechnet (Vorgabe)
  --fenster is       dasselbe Raster auf dem In-Sample-Fenster des
                     Walk-Forward (70 %). Diese Stufe hat bei mehreren
                     Bots die Parameterwahl tatsaechlich getroffen -
                     multi_symbol_walk_forward.py sortiert nach
                     demselben Score und rechnet denselben Drawdown auf
                     derselben Blockreihenfolge. Nur fuer die sechs
                     Prototyp-Bots verfuegbar, die ihr IS-Fenster ueber
                     einen Trade-Filter bilden (siehe adapters.py,
                     `unterstuetzt_is`).

Ergebnis (unter results/):
  <bot>[_is]_raster.csv    jede Kombination des Bot-Rasters mit allen
                     vier Drawdowns und allen vier Scores - nachrechenbar
  <bot>[_is]_ergebnis.json  Rangfolgen, Sieger je Mass, Streuung, Urteil

Was dieses Skript NICHT tut: es aendert nichts. Es importiert
`multi_symbol_optimise` als Bibliothek (der `__main__`-Block des Bots
laeuft dabei nicht) und schreibt ausschliesslich in seinen eigenen
results/-Ordner.
"""

import json
import os
import sys
import time

import numpy as np
import pandas as pd

import botenv

PERMUTATIONEN = 200
SEED = 20260912          # fest, damit ein Lauf reproduzierbar ist


def rangfolge(rows: list, key: str) -> list:
    """Wie multi_symbol_optimise: absteigend nach Score, nur
    Kombinationen, die die Mindestfilter bestehen.

    ZUM GLEICHSTAND: hier wird STABIL sortiert, ein Gleichstand bleibt
    also in Rasterreihenfolge stehen. Der Bot benutzt
    pandas.sort_values mit der Vorgabe kind="quicksort", die nicht
    stabil ist - bei genau gleichem Score kann er also eine andere
    Kombination nach vorne nehmen. Das ist nicht theoretisch: bei
    rsi2_mean_reversion liegen im In-Sample-Fenster zwei Kombinationen
    bei exakt 0,033 (siehe BERICHT.md, Abschnitt 4.3). Gegengeprueft
    wurde dort gegen den echten Bot-Lauf."""
    gueltig = [r for r in rows if r["besteht_mindestfilter"] and r.get(key) is not None]
    return sorted(gueltig, key=lambda r: -r[key])


def main():
    botenv.print_hinweis()
    bot = botenv.bot_from_argv()

    n_perm = PERMUTATIONEN
    if "--permutationen" in sys.argv:
        n_perm = int(sys.argv[sys.argv.index("--permutationen") + 1])
    fenster = "gesamt"
    if "--fenster" in sys.argv:
        fenster = sys.argv[sys.argv.index("--fenster") + 1]
    if fenster not in ("gesamt", "is"):
        raise SystemExit("--fenster nimmt 'gesamt' oder 'is'")

    import multi_symbol_optimise as mo
    import adapters
    import engine

    ad = adapters.build(bot, mo)
    ohne_rf = "--ohne-regimefilter" in sys.argv
    if ohne_rf:
        if bot != "t3_supertrend":
            raise SystemExit("--ohne-regimefilter gibt es nur fuer t3_supertrend")
        ad.regimefilter = False
        print("ACHTUNG: Rekonstruktion des Zustands VOR dem BTC-Regimefilter "
              "in evaluate_combination_multi - so, wie die gespeicherte "
              "results/t3_supertrend/multi_symbol_optimisation_results.csv "
              "entstanden ist.")
    if fenster == "is" and not ad.unterstuetzt_is:
        raise SystemExit(
            f"{bot} bildet sein In-Sample-Fenster durch Schneiden der KURSREIHE "
            f"(df.iloc[:split_idx]), nicht durch einen Trade-Filter. Eine "
            f"Ableitung aus der Gesamtmenge waere falsch - siehe adapters.py.")

    print(f"\n=== {bot} (Fenster: {fenster}) ===")
    print(f"Mindestfilter des Bots: MIN_TRADES={mo.MIN_TRADES}, "
          f"MIN_SYMBOLS_CONTRIBUTING={mo.MIN_SYMBOLS_CONTRIBUTING}, "
          f"MIN_AVG_RETURN_PCT={mo.MIN_AVG_RETURN_PCT}")

    t0 = time.time()
    data = mo.load_all_symbol_data()
    print(f"{len(data)} Symbole geladen ({round(time.time() - t0, 1)} s)")

    if fenster == "is":
        # Der Split kommt aus dem Bot selbst, nicht aus einer eigenen Regel.
        import multi_symbol_walk_forward as wf
        data, _oos = wf.split_all_symbols(data, wf.TRAIN_SPLIT_RATIO)
        print(f"In-Sample-Split des Bots: TRAIN_SPLIT_RATIO={wf.TRAIN_SPLIT_RATIO}")

    combos = ad.combinations()
    print(f"{len(combos)} Kombinationen im Raster des Bots\n")

    rows = []
    for i, combo in enumerate(combos, 1):
        t1 = time.time()
        trades, n_sym = (ad.collect_windowed(data, combo) if fenster == "is"
                         else ad.collect(data, combo))
        if trades is None:
            rows.append({"label": ad.label(combo), **ad.params(combo),
                         "besteht_mindestfilter": False, "num_trades": 0})
            continue

        row = {"label": ad.label(combo), **ad.params(combo)}
        row.update(engine.kennzahlen(trades, n_sym, mo.calculate_robustness_score))
        row["besteht_mindestfilter"] = ad.besteht_mindestfilter(trades, n_sym)

        # Streuung: 200 Permutationen der Blockreihenfolge und 200
        # Vertauschungen gleichzeitiger Einstiege
        perm_block = engine.block_permutation_drawdowns(trades, n_perm, SEED + i)
        perm_tie = engine.tie_permutation_drawdowns(trades, n_perm, SEED + i)
        row["perm_block_dd"] = engine.spanne(perm_block)
        row["perm_tie_dd"] = engine.spanne(perm_tie)
        row["perm_block_score"] = engine.spanne(np.array(
            [engine.score(mo.calculate_robustness_score, row["avg_return_pct"],
                          row["num_trades"], round(float(d), 2)) or np.nan
             for d in perm_block], dtype=float))
        row["_perm_block_dd_raw"] = perm_block
        rows.append(row)

        print(f"[{i:>3}/{len(combos)}] {row['label']:<38} "
              f"n={row['num_trades']:<6} DD Block {row['dd_block']:>9.2f} "
              f"chrono {row['dd_entry']:>9.2f}  Score {row['score_block']}"
              f" -> {row['score_entry']}   ({round(time.time() - t1, 1)} s)")

    # ---------------- Raster-CSV ------------------------------------
    csv_rows = [{k: v for k, v in r.items()
                 if not k.startswith("perm_") and not k.startswith("_")} for r in rows]
    df = pd.DataFrame(csv_rows)
    os.makedirs(botenv.RESULTS_DIR, exist_ok=True)
    suffix = "" if fenster == "gesamt" else f"_{fenster}"
    if ohne_rf:
        suffix += "_ohne_regimefilter"
    csv_path = os.path.join(botenv.RESULTS_DIR, f"{bot}{suffix}_raster.csv")
    df.to_csv(csv_path, index=False)

    # ---------------- Rangfolgen ------------------------------------
    ergebnis = {"hinweis": botenv.HINWEIS, "bot": bot, "fenster": fenster,
                "symbole": len(data), "kombinationen": len(combos),
                "permutationen": n_perm, "seed": SEED,
                "ohne_regimefilter": ohne_rf,
                "mindestfilter": {"MIN_TRADES": mo.MIN_TRADES,
                                  "MIN_SYMBOLS_CONTRIBUTING": mo.MIN_SYMBOLS_CONTRIBUTING,
                                  "MIN_AVG_RETURN_PCT": mo.MIN_AVG_RETURN_PCT},
                "num_besteht_mindestfilter": sum(1 for r in rows if r["besteht_mindestfilter"]),
                "nan_pnl_trades_gesamt": int(sum(r.get("num_nan_pnl", 0) for r in rows)),
                "rangfolgen": {}, "sieger": {}, "urteil": {}}

    ranks = {}
    for order in engine.ORDERS:
        key = f"score_{order}"
        rank = rangfolge(rows, key)
        ranks[order] = rank
        ergebnis["rangfolgen"][order] = [
            {"rang": j, "label": r["label"], "score": r[key],
             "dd": r[f"dd_{order}"], "num_trades": r["num_trades"],
             "avg_return_pct": r["avg_return_pct"]}
            for j, r in enumerate(rank[:10], 1)]
        ergebnis["sieger"][order] = rank[0]["label"] if rank else None

    # Rangwechsel je Kombination: Rang unter Block- vs. Chrono-Mass
    pos_block = {r["label"]: j for j, r in enumerate(ranks["block"], 1)}
    pos_entry = {r["label"]: j for j, r in enumerate(ranks["entry"], 1)}
    pos_exit = {r["label"]: j for j, r in enumerate(ranks["exit"], 1)}
    ergebnis["rangwechsel"] = sorted(
        [{"label": lab, "rang_block": pos_block[lab],
          "rang_entry": pos_entry.get(lab), "rang_exit": pos_exit.get(lab),
          "delta_entry": (pos_entry.get(lab) or 0) - pos_block[lab]}
         for lab in pos_block],
        key=lambda d: d["rang_block"])

    # ---------------- Kernfrage: kippt der Sieger? ------------------
    sieger_block = ergebnis["sieger"]["block"]
    sieger_entry = ergebnis["sieger"]["entry"]
    # Ohne Sieger gibt es keine Kernfrage. Das ist kein Randfall: im
    # eigenen Raster von elliott_wave besteht auf kausal sauberer
    # Grundlage KEINE der 36 Kombinationen die Mindestfilter des Bots.
    # Dann darf hier nicht "selbe Kombination" stehen - das waere eine
    # gruene Antwort auf eine Frage, die nicht gestellt werden kann.
    ergebnis["urteil"]["sieger_identisch"] = (
        None if sieger_block is None or sieger_entry is None
        else sieger_block == sieger_entry)

    # Vorsprung des Siegers auf den Zweiten - ein knapper Vorsprung
    # heisst etwas anderes als ein klarer.
    for order in ("block", "entry", "exit"):
        rank, key = ranks[order], f"score_{order}"
        if len(rank) > 1 and rank[1][key]:
            ergebnis["urteil"][f"vorsprung_{order}_pct"] = round(
                (rank[0][key] / rank[1][key] - 1) * 100, 1)
        else:
            ergebnis["urteil"][f"vorsprung_{order}_pct"] = None

    # Ist das Block-Mass ueberhaupt stabil gegen seine EIGENE Willkuer?
    # Fuer jede der n Permutationen der Blockreihenfolge: welche
    # Kombination gewinnt? Wenn das schwankt, ist die Rangfolge des
    # Block-Masses fuer sich schon Rauschen.
    gueltig = [r for r in rows if r["besteht_mindestfilter"] and "_perm_block_dd_raw" in r]
    if gueltig:
        import collections
        gewinner = collections.Counter()
        for p in range(n_perm):
            best, best_score = None, -np.inf
            for r in gueltig:
                dd = round(float(r["_perm_block_dd_raw"][p]), 2)
                s = engine.score(mo.calculate_robustness_score, r["avg_return_pct"],
                                 r["num_trades"], dd)
                if s is not None and s > best_score:
                    best, best_score = r["label"], s
            gewinner[best] += 1
        ergebnis["urteil"]["block_permutationssieger"] = gewinner.most_common()
        ergebnis["urteil"]["block_sieger_stabil_pct"] = round(
            100 * gewinner.most_common(1)[0][1] / n_perm, 1)

    # Streuung je Kombination (fuer den Bericht)
    ergebnis["streuung"] = [
        {"label": r["label"], "dd_block": r["dd_block"], "dd_entry": r["dd_entry"],
         "dd_exit": r["dd_exit"],
         "faktor_entry_zu_block": (round(abs(r["dd_entry"]) / abs(r["dd_block"]), 2)
                                    if r.get("dd_block") else None),
         "perm_block_dd": r["perm_block_dd"], "perm_tie_dd": r["perm_tie_dd"],
         "perm_block_score": r["perm_block_score"],
         "dd_entry_in_block_spanne": (
             r["perm_block_dd"].get("min") is not None
             and r["perm_block_dd"]["min"] <= r["dd_entry"] <= r["perm_block_dd"]["max"])}
        for r in rows if r["besteht_mindestfilter"]]

    json_path = os.path.join(botenv.RESULTS_DIR, f"{bot}{suffix}_ergebnis.json")
    with open(json_path, "w") as f:
        json.dump(ergebnis, f, indent=2, default=str)

    # ---------------- Ausgabe ---------------------------------------
    print(f"\nSieger nach Block-Reihenfolge (Bot-Mass): {sieger_block}")
    print(f"Sieger nach entry_time (chronologisch):   {sieger_entry}")
    print(f"Sieger nach exit_time (realisiert):       {ergebnis['sieger']['exit']}")
    if ergebnis["urteil"]["sieger_identisch"] is None:
        print("-> Kernfrage stellt sich nicht: KEINE Kombination dieses Rasters "
              "besteht die Mindestfilter des Bots")
    else:
        print(f"-> Kernfrage: "
              f"{'SELBE Kombination' if ergebnis['urteil']['sieger_identisch'] else 'ANDERE Kombination'}")
    if "block_sieger_stabil_pct" in ergebnis["urteil"]:
        print(f"Block-Mass gegen seine eigene Willkuer: Sieger in "
              f"{ergebnis['urteil']['block_sieger_stabil_pct']} % von {n_perm} "
              f"Blockreihenfolgen derselbe")
    print(f"\nGeschrieben: {csv_path}\n             {json_path}")
    print(f"Gesamtdauer: {round(time.time() - t0, 1)} s")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()

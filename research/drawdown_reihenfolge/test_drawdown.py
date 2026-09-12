"""
Selbsttests: rechnet diese Untersuchung wirklich den Bot nach?
====================================================================
Aufruf:  python3 test_drawdown.py <bot> [--alle]

Ohne `--alle` wird eine Stichprobe von Kombinationen geprueft (die
Live-Kombination des Bots, sofern im Raster, plus die erste, die
mittlere und die letzte); mit `--alle` jede Kombination des Rasters.

Zu jeder Prueflinie gehoert eine GEGENPROBE (Projekt-Prinzip 12: eine
gruene Pruefung ist erst etwas wert, wenn belegt ist, dass sie auch rot
werden kann). Die Gegenproben stehen als eigene Zeilen in der Ausgabe
und sind bestanden, wenn die absichtlich verfaelschte Rechnung
ABWEICHT.
"""

import os
import subprocess
import sys

import numpy as np
import pandas as pd

import botenv

OK = []


def check(name, bedingung, detail=""):
    OK.append(bool(bedingung))
    marke = "OK  " if bedingung else "FEHL"
    print(f"[{marke}] {name}" + (f"   ({detail})" if detail else ""))


# Live-Kombination je Bot, in der Sprache des jeweiligen Rasters.
# Quelle ist jeweils strategies/<bot>/live_params.py - hier steht sie
# nur, damit der Selbsttest genau diesen Punkt mitprueft.
LIVE = {
    "elliott_wave": (10.0, 6.0, 0.618),          # ausserhalb des Bot-Rasters
    "elliott_wave_stocks": (5.0, 3.0, None, False),
    "t3_supertrend": (16, 30, 20.0, 4.0),
    "rsi2_crypto": (150, 10.0, None),
    "rsi2_mean_reversion": (5.0, None),
    "turtle_soup_crypto": (10, "structural"),
    "turtle_soup_stocks": (10, None),
    "volatility_breakout": (8.0,),
    "volatility_breakout_crypto": (5.0,),
}


def stichprobe(combos, bot):
    aus = []
    live = LIVE.get(bot)
    if live in combos:
        aus.append(live)
    for c in (combos[0], combos[len(combos) // 2], combos[-1]):
        if c not in aus:
            aus.append(c)
    return aus


def main():
    botenv.print_hinweis()
    bot = botenv.bot_from_argv()
    alle = "--alle" in sys.argv

    import multi_symbol_optimise as mo
    import adapters
    import engine

    ad = adapters.build(bot, mo)
    data = mo.load_all_symbol_data()
    combos = ad.combinations()
    print(f"\n=== Selbsttests {bot}: {len(data)} Symbole, {len(combos)} Kombinationen ===\n")

    # ---- 1) der Projekt-Score kommt aus der Bot-Funktion -----------
    rng = np.random.default_rng(7)
    gleich = True
    for _ in range(200):
        avg = round(float(rng.uniform(-3, 8)), 2)
        n = int(rng.integers(30, 20000))
        dd = round(float(rng.uniform(-900, -0.5)), 2)
        gleich = gleich and engine.score(mo.calculate_robustness_score, avg, n, dd) == \
            mo.calculate_robustness_score({"avg_return_pct": avg, "num_trades": n,
                                           "max_drawdown_pct": dd})
    check("Score kommt unveraendert aus multi_symbol_optimise", gleich, "200 Zufallsfaelle")

    def falscher_score(row):
        # Gegenprobe: Drawdown NICHT im Nenner
        return round(row["avg_return_pct"] * (row["num_trades"] ** 0.5), 3)
    check("GEGENPROBE Score: falsche Formel weicht ab",
          engine.score(falscher_score, 5.0, 100, -50.0)
          != engine.score(mo.calculate_robustness_score, 5.0, 100, -50.0))

    # ---- 2) die beiden Drawdown-Wege sind identisch ----------------
    gleich = True
    for _ in range(200):
        pnl = rng.normal(0.2, 4, size=int(rng.integers(5, 3000)))
        gleich = gleich and abs(engine.cum_drawdown(pd.Series(pnl))
                                - engine.cum_drawdown_np(pnl)) < 1e-9
    check("cum_drawdown (pandas) == cum_drawdown_np (numpy)", gleich, "200 Zufallsreihen")

    # Gegenprobe: der Drawdown haengt wirklich an der Reihenfolge.
    # (Nicht jede Umsortierung aendert ihn - eine Umkehr laesst ihn oft
    # unberuehrt. Deshalb ein Beispiel, bei dem er es tut.)
    pnl = np.array([5.0, -3.0, 8.0, -10.0])
    check("GEGENPROBE Drawdown: Umsortieren aendert den Wert",
          engine.cum_drawdown_np(pnl) != engine.cum_drawdown_np(pnl[::-1]),
          f"{engine.cum_drawdown_np(pnl)} gegen {engine.cum_drawdown_np(pnl[::-1])}")

    # ---- 3) Kernstueck: Gleichheit mit evaluate_combination_multi --
    FELDER = ("num_trades", "num_symbols", "win_rate", "total_return_pct",
              "avg_return_pct")
    pruef = combos if alle else stichprobe(combos, bot)
    alles_gleich, dd_gleich, abweichungen = True, True, []
    for combo in pruef:
        trades, n_sym = ad.collect(data, combo)
        bot_res = ad.bot_eval(data, combo)
        if trades is None or bot_res is None:
            # Mindestfilter: der Bot gibt None zurueck. Dann muss auch
            # unsere Filterentscheidung None-gleich ausfallen.
            eigen = trades is not None and ad.besteht_mindestfilter(trades, n_sym)
            if eigen != (bot_res is not None):
                alles_gleich = False
                abweichungen.append(f"{ad.label(combo)}: Filterentscheidung weicht ab")
            continue
        eigen = engine.kennzahlen(trades, n_sym, mo.calculate_robustness_score)
        for f in FELDER:
            if eigen[f] != bot_res[f]:
                alles_gleich = False
                abweichungen.append(f"{ad.label(combo)}: {f} {eigen[f]} != {bot_res[f]}")
        if eigen["dd_bot"] != bot_res["max_drawdown_pct"] or \
                eigen["score_bot"] != bot_res["robustness_score"]:
            dd_gleich = False
            abweichungen.append(
                f"{ad.label(combo)}: dd_bot {eigen['dd_bot']} != "
                f"{bot_res['max_drawdown_pct']} bzw. Score {eigen['score_bot']} != "
                f"{bot_res['robustness_score']}")
    check("Kennzahlen identisch zu evaluate_combination_multi des Bots",
          alles_gleich, f"{len(pruef)} Kombinationen, {len(abweichungen)} Abweichungen")
    check("dd_bot und score_bot identisch zum Bot", dd_gleich)
    for a in abweichungen[:10]:
        print(f"        {a}")

    # Gegenprobe zum Kernstueck: Bloecke absichtlich umgedreht -> die
    # Gleichheit muss brechen. Wenn nicht, prueft der Test nichts.
    combo = pruef[0]
    trades, n_sym = ad.collect(data, combo)
    bot_res = ad.bot_eval(data, combo)
    if trades is not None and bot_res is not None:
        # Eine vertauschte Blockreihenfolge muss die Gleichheit mit dem
        # Bot brechen - sonst prueft die Pruefung oben nichts. Gesucht
        # wird eine Vertauschung, die den Wert wirklich verschiebt (eine
        # blosse Umkehr tut das oft nicht).
        rng2 = np.random.default_rng(11)
        bloecke = [g for _, g in trades.groupby("_block_idx", sort=True)]
        gefunden, eigen = None, None
        for _ in range(50):
            ordnung = rng2.permutation(len(bloecke))
            kandidat = pd.concat([bloecke[j] for j in ordnung], ignore_index=True)
            e = engine.kennzahlen(kandidat, n_sym, mo.calculate_robustness_score)
            if e["dd_bot"] != bot_res["max_drawdown_pct"]:
                gefunden, eigen = ordnung, e
                break
        check("GEGENPROBE Reihenfolge: eine vertauschte Blockreihenfolge "
              "bricht die Gleichheit mit dem Bot",
              gefunden is not None,
              f"{eigen['dd_bot']} gegen {bot_res['max_drawdown_pct']}" if eigen else
              "keine der 50 Vertauschungen aendert den Wert")
        # ... waehrend die reihenfolgeunabhaengigen Felder gleich bleiben
        if eigen:
            check("Umsortieren aendert nur den Drawdown, nicht Anzahl/Rendite",
                  all(eigen[f] == bot_res[f] for f in FELDER))

    # ---- 4) die behauptete Struktur je Bot -------------------------
    trades, n_sym = ad.collect(data, pruef[0])
    k = engine.kennzahlen(trades, n_sym, mo.calculate_robustness_score)
    if bot == "t3_supertrend":
        check("t3_supertrend: das Bot-Mass IST das chronologische "
              "(filter_trades_by_regime sortiert nach entry_time)",
              k["dd_bot"] == k["dd_entry"], f"dd_bot={k['dd_bot']}, dd_entry={k['dd_entry']}")
        check("t3_supertrend: Blockreihenfolge ergibt einen ANDEREN Wert",
              k["dd_bot"] != k["dd_block"], f"dd_block={k['dd_block']}")
    else:
        check("Das Bot-Mass ist die Blockreihenfolge",
              k["dd_bot"] == k["dd_block"], f"dd_bot={k['dd_bot']}, dd_block={k['dd_block']}")

    # entry_time ist nach der chronologischen Sortierung monoton
    chrono = trades.sort_values("entry_time", kind="stable")
    check("Nach der chronologischen Sortierung ist entry_time monoton",
          chrono["entry_time"].is_monotonic_increasing)

    # ---- 5) Permutationen aendern nur den Drawdown -----------------
    perm = engine.block_permutation_drawdowns(trades, 50, 1)
    check("Blockpermutationen erzeugen ueberhaupt Streuung",
          float(np.nanmax(perm)) != float(np.nanmin(perm)),
          f"Spanne {round(float(np.nanmax(perm) - np.nanmin(perm)), 2)} pp")
    check("Die Bot-Blockreihenfolge liegt in der Spanne ihrer Permutationen",
          float(np.nanmin(perm)) - 1e-6 <= k["dd_block"] <= float(np.nanmax(perm)) + 1e-6,
          f"dd_block={k['dd_block']} in [{round(float(np.nanmin(perm)),2)}, "
          f"{round(float(np.nanmax(perm)),2)}]")

    einzelblock = trades[trades["_block_idx"] == trades["_block_idx"].iloc[0]]
    p1 = engine.block_permutation_drawdowns(einzelblock, 20, 1)
    check("GEGENPROBE Permutation: bei nur EINEM Block gibt es keine Streuung",
          float(np.nanmax(p1)) == float(np.nanmin(p1)))

    # ---- 6) NaN-PnL (APH-Problematik) ------------------------------
    # Gemessen, nicht angenommen: `Series.cumsum()` UEBERSPRINGT NaN
    # (skipna=True) und bricht die Reihe deshalb NICHT ab - ein
    # NaN-Trade wirkt in der kumulierten Reihe wie 0. Der Drawdown des
    # Rasters ist von der Kurslueecke also nicht betroffen. Was sie
    # verschiebt, ist `mean()`: dort sinkt der Nenner um den NaN-Trade,
    # waehrend `num_trades` ihn mitzaehlt.
    kunst = pd.DataFrame({
        "pnl_pct": [5.0, -30.0, np.nan, -50.0],
        "entry_time": pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04"]),
        "exit_time": pd.to_datetime(["2020-01-05", "2020-01-06", "2020-01-07", "2020-01-08"]),
        "symbol": ["A", "A", "B", "B"], "_block_idx": [0, 0, 1, 1]})
    d = engine.drawdowns(kunst)
    check("Ein NaN-PnL-Trade kappt die kumulierte Reihe NICHT "
          "(pandas cumsum ueberspringt ihn)",
          d["dd_bot"] == -80.0 and d["dd_bot_ohne_nan"] == -80.0,
          f"mit NaN {d['dd_bot']}, ohne NaN {d['dd_bot_ohne_nan']}")
    k_nan = engine.kennzahlen(kunst, 2, mo.calculate_robustness_score)
    check("Der NaN-Trade zaehlt in num_trades mit, im Mittelwert aber nicht",
          k_nan["num_trades"] == 4 and k_nan["avg_return_pct"] == round(-75 / 3, 2),
          f"num_trades={k_nan['num_trades']}, avg={k_nan['avg_return_pct']}")

    # ---- 7) nichts angefasst ---------------------------------------
    geaendert = subprocess.run(["git", "status", "--porcelain"],
                               cwd=botenv.REPO_ROOT, capture_output=True,
                               text=True).stdout.strip().splitlines()
    fremd = [z for z in geaendert
             if "research/drawdown_reihenfolge" not in z]
    check("Kein Bot-Code und keine Bot-Ergebnisdatei angefasst",
          not fremd, f"{len(geaendert)} Aenderungen, alle unter research/drawdown_reihenfolge"
          if not fremd else "; ".join(fremd[:5]))

    diff = subprocess.run(
        ["git", "diff", "--stat", "--",
         "strategies", "shared", "results", "config", "docs"],
        cwd=botenv.REPO_ROOT, capture_output=True, text=True).stdout.strip()
    check("git diff auf strategies/, shared/, results/, config/, docs/ ist leer",
          diff == "", diff[:200])

    # ---- 8) In-Sample-Fenster, falls ableitbar ---------------------
    if ad.unterstuetzt_is:
        import multi_symbol_walk_forward as wf
        train, _ = wf.split_all_symbols(mo.load_all_symbol_data(), wf.TRAIN_SPLIT_RATIO)
        gleich, abw = True, []
        for combo in (pruef if alle else pruef[:2]):
            t, n = ad.collect_windowed(train, combo)
            b = ad.bot_eval_windowed(wf, train, combo)
            if t is None or b is None:
                continue
            e = engine.kennzahlen(t, n, mo.calculate_robustness_score)
            for f in FELDER + ("dd_bot",):
                soll = b["max_drawdown_pct"] if f == "dd_bot" else b[f]
                if e[f] != soll:
                    gleich = False
                    abw.append(f"{ad.label(combo)}: {f} {e[f]} != {soll}")
        check("In-Sample-Fenster identisch zu "
              "multi_symbol_walk_forward.evaluate_combination_multi_windowed",
              gleich, "; ".join(abw[:3]))
    else:
        print(f"[----] In-Sample-Fenster: {bot} schneidet die Kursreihe selbst, "
              f"nicht ableitbar - bewusst nicht geprueft")

    print(f"\n{sum(OK)}/{len(OK)} Pruefungen bestanden")
    botenv.print_hinweis()
    sys.exit(0 if all(OK) else 1)


if __name__ == "__main__":
    main()

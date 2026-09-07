"""
Zusammenfassung und Tragfaehigkeits-Urteil
====================================================================
Fuehrt die Ergebnisse von search.py, walkforward.py, stability.py,
symbols.py und benchmark.py zu einer Tabelle je Kandidat zusammen und
faellt ein mechanisches Urteil.

Warum mechanisch: bei einer Parametersuche ist die Versuchung gross,
im Nachhinein zu begruenden, warum ausgerechnet der beste Fund doch
tragfaehig sei. Die fuenf Bedingungen stehen deshalb HIER, im Code,
und gelten fuer jeden Kandidaten gleich - nicht im Fliesstext.

Ein Kandidat gilt als TRAGFAEHIG, wenn alle fuenf zutreffen:

  B1  besteht die projekteigenen Mindestfilter im In-Sample-Fenster
  B2  besteht sie auch im Out-of-Sample-Fenster - hilfsweise mit einer
      an die Fensterlaenge angepassten Mindest-Trade-Zahl, weil
      MIN_TRADES fuer die volle Historie festgelegt wurde und ein
      kuerzeres Fenster sonst allein an seiner Laenge scheitert
      (beide Varianten werden ausgewiesen)
  B3  positiver Ø PnL in JEDER Walk-Forward-Falte - ein einzelner
      guenstiger Abschnitt darf das Ergebnis nicht tragen
  B4  schlaegt gleichgewichtetes Buy-and-Hold im Out-of-Sample-Fenster
      im Calmar-Verhaeltnis
  B5  stabil: der Median der Rasternachbarn erreicht mindestens die
      Haelfte des eigenen Projekt-Scores, und eine Zigzag-Verschiebung
      um +/- 0,5 Prozentpunkte laesst den Ø PnL nicht ins Minus kippen

Nutzung:  python3 summary.py <elliott_wave|elliott_wave_stocks>
"""

import json
import os

import botenv

BOT = botenv.bot_from_argv()

import engine        # noqa: E402
import walkforward as wf   # noqa: E402

NACHBAR_MINDESTANTEIL_PCT = 50.0


def load(name):
    path = os.path.join(botenv.RESULTS_DIR, f"{BOT}_{name}.json")
    if not os.path.exists(path):
        raise SystemExit(f"{path} fehlt - erst {name}.py laufen lassen.")
    with open(path) as fh:
        return json.load(fh)


def row_for(search, window, key):
    """Zeile aus dem Raster - None, wenn die Kombination dort fehlt."""
    import pandas as pd
    path = os.path.join(botenv.RESULTS_DIR, f"{BOT}_grid_{window}.csv")
    df = pd.read_csv(path)
    m = df[(df["deviation_pct"] == key[0]) & (df["stop_loss_pct"] == key[1])
           & (df["take_profit_fib"] == key[2]) & (df["use_take_profit"] == key[3])]
    return m.iloc[0].to_dict() if len(m) else None


def main():
    botenv.print_hinweis()
    search = load("search")
    walk = load("walkforward")
    stab = load("stability")
    bh = load("buyhold")
    syms = load("symbols")

    windows = engine.load_windows()
    bars = {w: sum(len(df) for df in windows[w].values()) for w in windows}
    skaliert_min_trades = {
        w: max(1, round(search["mindestfilter"]["min_trades"] * bars[w] / bars[engine.WINDOW_FULL]))
        for w in windows}

    out = {"hinweis": botenv.UNVALIDIERT_HINWEIS, "bot": BOT,
           "bedingungen": {
               "B1": "besteht die Mindestfilter In-Sample",
               "B2": "besteht die Mindestfilter Out-of-Sample (auch in der an die "
                     "Fensterlaenge angepassten Variante)",
               "B3": "positiver Ø PnL in jeder Walk-Forward-Falte",
               "B4": "schlaegt Buy-and-Hold Out-of-Sample im Calmar",
               "B5": f"Nachbar-Median >= {NACHBAR_MINDESTANTEIL_PCT:g} % des eigenen Scores "
                     f"und Zigzag +/- 0,5 pp bleibt im Plus"},
           "mindestfilter": search["mindestfilter"],
           "mindest_trades_skaliert": skaliert_min_trades,
           "kandidaten": [], "tragfaehig": []}

    stab_by = {tuple(c["key"]): c for c in stab["kandidaten"]}
    sym_by = {tuple(c["key"]): c for c in syms["kandidaten"]}
    wf_by = {tuple(c["key"]): c for c in walk["kandidaten"]}

    print(f"\n{BOT}: Tragfaehigkeits-Pruefung\n")
    for cand in wf.load_candidates():
        key = cand["key"]
        name = wf.label(key)
        r_is = row_for(search, engine.WINDOW_IS, key)
        r_oos = row_for(search, engine.WINDOW_OOS, key)
        r_full = row_for(search, engine.WINDOW_FULL, key)

        # --- B1 / B2 ------------------------------------------------
        b1 = bool(r_is and r_is.get("besteht_mindestfilter"))
        b2_streng = bool(r_oos and r_oos.get("besteht_mindestfilter"))
        f = search["mindestfilter"]
        b2_skaliert = bool(
            r_oos and r_oos.get("num_trades", 0) >= skaliert_min_trades[engine.WINDOW_OOS]
            and r_oos.get("num_symbols", 0) >= f["min_symbols"]
            and r_oos.get("avg_return_pct", -99) >= f["min_avg_return_pct"])
        b2 = b2_streng or b2_skaliert

        # --- B3 ------------------------------------------------------
        folds = wf_by.get(key, {}).get("falten", [])
        fold_avgs = [(p["falte"], (p["ergebnis"] or {}).get("avg_return_pct")) for p in folds]
        b3 = bool(fold_avgs) and all(a is not None and a > 0 for _k, a in fold_avgs)

        # --- B4 ------------------------------------------------------
        bh_oos = bh["fenster"].get(engine.WINDOW_OOS, {})
        cal = r_oos.get("pf_calmar_ratio") if r_oos else None
        cal = None if cal is None or (isinstance(cal, float) and cal != cal) else float(cal)
        bh_cal = bh_oos.get("calmar_ratio")
        b4 = bool(cal is not None and bh_cal is not None and cal > bh_cal)

        # --- B5 ------------------------------------------------------
        st = stab_by.get(key, {})
        nb = (st.get("nachbarschaft") or {}).get(engine.WINDOW_IS, {})
        anteil = nb.get("median_anteil_pct")
        fine = (st.get("zigzag_feinschritt") or {}).get(engine.WINDOW_FULL, {})
        fine_avgs = [v.get("avg_return_pct") for v in fine.values()]
        b5 = bool(anteil is not None and anteil >= NACHBAR_MINDESTANTEIL_PCT
                  and fine_avgs and all(a is not None and a > 0 for a in fine_avgs))

        tragfaehig = b1 and b2 and b3 and b4 and b5
        entry = {
            "kombination": name, "key": list(key), "herkunft": cand["herkunft"],
            "is": r_is, "oos": r_oos, "gesamt": r_full,
            "walk_forward_falten": fold_avgs,
            "buy_and_hold_oos": bh_oos,
            "nachbar_median_anteil_pct_is": anteil,
            "zigzag_feinschritt_avg_pnl": fine_avgs,
            "reihenfolge": st.get("reihenfolge"),
            "symbolbeitrag": (sym_by.get(key) or {}).get("beitrag"),
            "bedingungen": {"B1": b1, "B2": b2, "B2_streng": b2_streng,
                             "B2_skaliert": b2_skaliert, "B3": b3, "B4": b4, "B5": b5},
            "tragfaehig": tragfaehig,
        }
        out["kandidaten"].append(entry)
        if tragfaehig:
            out["tragfaehig"].append(name)

        marks = "".join("+" if entry["bedingungen"][b] else "-" for b in ("B1", "B2", "B3", "B4", "B5"))
        print(f"  {name:<46} B1..B5 {marks}   "
              f"{'TRAGFAEHIG' if tragfaehig else 'nicht tragfaehig'}   ({cand['herkunft']})")
        print(f"      In-Sample     : {(r_is or {}).get('num_trades')} Trades, "
              f"Ø {(r_is or {}).get('avg_return_pct')} %, Calmar {(r_is or {}).get('pf_calmar_ratio')}")
        print(f"      Out-of-Sample : {(r_oos or {}).get('num_trades')} Trades "
              f"(streng >= {f['min_trades']}, skaliert >= {skaliert_min_trades[engine.WINDOW_OOS]}), "
              f"Ø {(r_oos or {}).get('avg_return_pct')} %, Calmar {cal}, "
              f"Buy-and-Hold {bh_cal}")
        print(f"      Falten Ø PnL  : "
              + ", ".join(f"F{k} {'-' if a is None else f'{a:+.2f} %'}" for k, a in fold_avgs))
        print(f"      Nachbarn      : Median {anteil} % des eigenen Scores; "
              f"Zigzag +/-0,5 pp Ø PnL {fine_avgs}")

    print(f"\nErgebnis: {len(out['tragfaehig'])} von {len(out['kandidaten'])} "
          f"geprueften Kandidaten sind nach allen fuenf Bedingungen tragfaehig.")
    if out["tragfaehig"]:
        for n in out["tragfaehig"]:
            print(f"  - {n}")

    path = os.path.join(botenv.RESULTS_DIR, f"{BOT}_summary.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {path}")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()

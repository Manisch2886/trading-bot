"""
Walk-Forward-Validierung der Parameter-Neubestimmung
====================================================================
Der einzelne 70/30-Split aus multi_symbol_walk_forward.py beantwortet
nur: "haelt die eine, auf den ersten 70 % gefundene Kombination auf den
letzten 30 %?" Das ist ein einziger Wuerfelwurf. Dieses Skript stellt
zwei schaerfere Fragen:

A) Haelt ein KANDIDAT ueber mehrere, disjunkte Testzeitraeume - oder
   traegt ein einziger guenstiger Abschnitt das ganze Ergebnis?

B) Haelt das VERFAHREN? Auf jedem Trainingsfenster wird der komplette
   Suchraum neu optimiert, und die dort gewonnene Kombination wird auf
   dem jeweils folgenden, ungesehenen Fenster getestet. Das misst nicht
   eine Kombination, sondern die Frage "haette die Rastersuche zu einem
   frueheren Zeitpunkt etwas geliefert, das danach funktioniert?".

Faltung (anchored/expanding, nach KALENDERDATUM):
    Falte 1  train [Start, 40 %)   test [40 %, 60 %)
    Falte 2  train [Start, 60 %)   test [60 %, 80 %)
    Falte 3  train [Start, 80 %)   test [80 %, 100 %)

Trainingsfenster wachsen mit (anchored), weil auch der Bot immer die
volle bis dahin verfuegbare Historie sieht. Jedes Fenster wird komplett
eigenstaendig durchgerechnet - eigener Zigzag, eigene Wellen; ein
Fenster sieht nie Kurse ausserhalb seiner Grenzen.

Die Grenzen sind bewusst KALENDERDATEN, nicht Zeilenanteile. Der
Projekt-Split in multi_symbol_walk_forward.split_all_symbols teilt
jedes Symbol nach Zeilenanteil - bei unterschiedlich langen Historien
(juengere Boersengaenge, spaeter gelistete Coins) faellt das
In-Sample-Fenster eines langen Symbols dann kalendarisch mit dem
Out-of-Sample-Fenster eines kurzen zusammen. Trades aus derselben
Marktphase liegen so auf beiden Seiten der Trennlinie. Hier wird an
einem gemeinsamen Datum getrennt; ein Testfenster enthaelt damit
ausschliesslich Marktphasen, die in keinem Trainingsfenster
vorkommen.

Nutzung:  python3 walkforward.py <elliott_wave|elliott_wave_stocks>
"""

import json
import multiprocessing as mp
import os
import time

import pandas as pd

import botenv

BOT = botenv.bot_from_argv()

import engine    # noqa: E402
import search    # noqa: E402  - Suchraum und Kombinationsliste kommen von dort

FOLD_BOUNDS = [0.40, 0.60, 0.80, 1.00]
N_CANDIDATES = 5          # beste Kombinationen des In-Sample-Fensters
N_WORKERS = min(4, os.cpu_count() or 1)

_DATA = {}


MIN_BARS_PER_SYMBOL = 60      # kuerzere Ausschnitte tragen keinen Zigzag


def calendar_bounds(all_data: dict) -> list:
    """Die Faltungsgrenzen als Datum - gemeinsam fuer alle Symbole."""
    start = min(df["open_time"].min() for df in all_data.values())
    end = max(df["open_time"].max() for df in all_data.values())
    span = end - start
    return [start + span * q for q in FOLD_BOUNDS[:-1]] + [end]


def slice_window(all_data: dict, lo, hi) -> dict:
    """Zeitlicher Ausschnitt je Symbol zwischen zwei Kalenderdaten
    (lo einschliesslich, hi ausschliesslich; das letzte Fenster nimmt
    den Endpunkt mit)."""
    out = {}
    for symbol, df in all_data.items():
        mask = (df["open_time"] >= lo) & (df["open_time"] < hi)
        piece = df[mask].reset_index(drop=True)
        if len(piece) >= MIN_BARS_PER_SYMBOL:
            out[symbol] = piece
    return out


def build_folds(all_data: dict) -> dict:
    start = min(df["open_time"].min() for df in all_data.values())
    cuts = calendar_bounds(all_data)
    windows = {}
    folds = []
    for k in range(len(FOLD_BOUNDS) - 1):
        train_hi = cuts[k]
        test_lo = cuts[k]
        test_hi = cuts[k + 1] + (pd.Timedelta(seconds=1) if k + 1 == len(cuts) - 1
                                  else pd.Timedelta(0))
        tr, te = f"wf{k + 1}_train", f"wf{k + 1}_test"
        windows[tr] = slice_window(all_data, start, train_hi)
        windows[te] = slice_window(all_data, test_lo, test_hi)
        folds.append({"falte": k + 1, "train": tr, "test": te,
                       "train_bis": str(train_hi),
                       "test_von": str(test_lo), "test_bis": str(cuts[k + 1])})
    return windows, folds


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


def key_of(row) -> tuple:
    return (float(row["deviation_pct"]), float(row["stop_loss_pct"]),
            float(row["take_profit_fib"]), bool(row["use_take_profit"]))


def label(key) -> str:
    dev, stop, fib, use_tp = key
    ziel = f"Fib {fib:g}" if use_tp else "kein Ziel"
    if use_tp and fib >= search.NO_TARGET_FIB and not engine.SUPPORTS_NO_TP:
        ziel = f"Fib {fib:g} (praktisch kein Ziel)"
    return f"dev {dev:g} % / Stop {stop:g} % / {ziel}"


def load_candidates() -> list:
    """Kandidaten kommen AUSSCHLIESSLICH aus dem In-Sample-Fenster -
    die Auswahl darf das Out-of-Sample-Fenster nie gesehen haben."""
    path = os.path.join(botenv.RESULTS_DIR, f"{BOT}_search.json")
    if not os.path.exists(path):
        raise SystemExit(f"{path} fehlt - erst search.py laufen lassen.")
    with open(path) as fh:
        data = json.load(fh)

    keys, out = set(), []
    for row in data["fenster"][engine.WINDOW_IS]["top10"][:N_CANDIDATES]:
        k = key_of(row)
        if k not in keys:
            keys.add(k)
            out.append({"key": k, "herkunft": "In-Sample-Score"})
    live = data["live_kombination"]
    k = (live["deviation_pct"], live["stop_loss_pct"],
         live["take_profit_fib"], live["use_take_profit"])
    if k not in keys:
        out.append({"key": k, "herkunft": "aktuell live"})
    else:
        for c in out:
            if c["key"] == k:
                c["herkunft"] += " + aktuell live"
    return out


def main():
    botenv.print_hinweis()
    t_start = time.time()
    base = engine.load_windows()[engine.WINDOW_FULL]
    windows, folds = build_folds(base)
    _DATA.update(windows)

    candidates = load_candidates()
    print(f"{BOT}: {len(folds)} Falten, {len(candidates)} Kandidaten, "
          f"{len(list(search.combos()))} Kombinationen je Trainingsfenster")
    for c in candidates:
        print(f"  Kandidat {label(c['key'])}  ({c['herkunft']})")
    for f in folds:
        s1, e1 = engine.window_span(_DATA[f["train"]])
        s2, e2 = engine.window_span(_DATA[f["test"]])
        print(f"  Falte {f['falte']}: train {s1} .. {e1}   test {s2} .. {e2}")

    ctx = mp.get_context("fork")

    print(f"\nWellen-Cache ({N_WORKERS} Prozesse)...")
    cache_tasks = [(w, d) for w in windows for d in search.DEVIATION_RANGE]
    with ctx.Pool(N_WORKERS) as pool:
        for i, _ in enumerate(pool.imap_unordered(_build_cache, cache_tasks), 1):
            if i % 7 == 0 or i == len(cache_tasks):
                print(f"  {i}/{len(cache_tasks)}")

    # --- B) Verfahren: volles Raster auf jedem Trainingsfenster --------
    print(f"\nRaster auf den Trainingsfenstern ({N_WORKERS} Prozesse)...")
    train_windows = [f["train"] for f in folds]
    tasks = [(w,) + c for w in train_windows for c in search.combos()]
    rows = []
    with ctx.Pool(N_WORKERS) as pool:
        for i, row in enumerate(pool.imap_unordered(_run_combo, tasks, chunksize=4), 1):
            rows.append(row)
            if i % 200 == 0 or i == len(tasks):
                print(f"  {i}/{len(tasks)}")
    train_df = pd.DataFrame(rows)

    # --- A) + B) Auswertung auf den Testfenstern ----------------------
    to_eval = {}
    for f in folds:
        sub = train_df[(train_df["window"] == f["train"]) & train_df["besteht_mindestfilter"]]
        sub = sub.sort_values("robustness_score", ascending=False)
        f["train_sieger"] = key_of(sub.iloc[0]) if len(sub) else None
        f["train_bestehen"] = int(len(sub))
        f["train_sieger_zeile"] = sub.iloc[0].to_dict() if len(sub) else None
        keys = {c["key"] for c in candidates}
        if f["train_sieger"]:
            keys.add(f["train_sieger"])
        to_eval[f["test"]] = keys

    print(f"\nTestfenster auswerten ({N_WORKERS} Prozesse)...")
    tasks = [(w,) + k for w, ks in to_eval.items() for k in sorted(ks)]
    rows = []
    with ctx.Pool(N_WORKERS) as pool:
        for row in pool.imap_unordered(_run_combo, tasks, chunksize=2):
            rows.append(row)
    test_df = pd.DataFrame(rows)

    def lookup(df, window, key):
        m = df[(df["window"] == window)
               & (df["deviation_pct"] == key[0]) & (df["stop_loss_pct"] == key[1])
               & (df["take_profit_fib"] == key[2]) & (df["use_take_profit"] == key[3])]
        return m.iloc[0].to_dict() if len(m) else None

    out = {"hinweis": botenv.UNVALIDIERT_HINWEIS, "bot": BOT, "falten": [], "kandidaten": [],
           "fold_bounds": FOLD_BOUNDS, "laufzeit_s": None}

    print("\n" + "=" * 74)
    print("B) VERFAHREN - auf jedem Trainingsfenster neu optimiert")
    print("=" * 74)
    for f in folds:
        entry = {"falte": f["falte"], "train_bis": f["train_bis"],
                 "test_von": f["test_von"], "test_bis": f["test_bis"],
                 "train_bestehen_mindestfilter": f["train_bestehen"],
                 "train_sieger": (label(f["train_sieger"]) if f["train_sieger"] else None),
                 "train_sieger_zeile": f["train_sieger_zeile"],
                 "test_ergebnis": (lookup(test_df, f["test"], f["train_sieger"])
                                    if f["train_sieger"] else None)}
        out["falten"].append(entry)
        if not f["train_sieger"]:
            print(f"  Falte {f['falte']}: KEINE Kombination besteht im Trainingsfenster "
                  f"die Mindestfilter - das Verfahren haette hier gar nichts geliefert.")
            continue
        te = entry["test_ergebnis"]
        print(f"  Falte {f['falte']}: Sieger {label(f['train_sieger'])} "
              f"({f['train_bestehen']} Kombinationen bestehen)")
        if te and te.get("num_trades"):
            print(f"           Test: {te['num_trades']} Trades, Ø PnL {te['avg_return_pct']} %, "
                  f"Score {te['robustness_score']}, Calmar {te.get('pf_calmar_ratio')}, "
                  f"Mindestfilter {'ja' if te['besteht_mindestfilter'] else 'nein'}")
        else:
            print("           Test: keine Trades")

    print("\n" + "=" * 74)
    print("A) KANDIDATEN - dieselbe Kombination ueber alle Testfenster")
    print("=" * 74)
    for c in candidates:
        per_fold = []
        for f in folds:
            per_fold.append({"falte": f["falte"],
                             "ergebnis": lookup(test_df, f["test"], c["key"])})
        out["kandidaten"].append({"kombination": label(c["key"]), "key": list(c["key"]),
                                   "herkunft": c["herkunft"], "falten": per_fold})
        cells = []
        for p in per_fold:
            r = p["ergebnis"]
            cells.append("-" if not r or not r.get("num_trades")
                         else f"{r['avg_return_pct']:+.2f} %/{r['num_trades']}T")
        print(f"  {label(c['key']):<48}" + "  ".join(f"F{p['falte']} {c}"
                                                     for p, c in zip(per_fold, cells)))

    out["laufzeit_s"] = round(time.time() - t_start, 1)
    path = os.path.join(botenv.RESULTS_DIR, f"{BOT}_walkforward.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {path}  ({out['laufzeit_s']} s)")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()

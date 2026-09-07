"""
Parameter-Instabilitaet und Reihenfolge-Empfindlichkeit
====================================================================
Ein "bester" Parametersatz, der bei einer kleinen Verschiebung
einbricht, ist kein Fund, sondern ein Overfitting-Warnsignal. Dieses
Skript prueft die Kandidaten aus search.py auf drei Arten:

1) Rasternachbarschaft - je ein Schritt nach oben und unten auf jeder
   der drei Achsen (deviation, stop, Ziel). Verglichen wird der
   Projekt-Score des Kandidaten mit Median und Minimum seiner
   Nachbarn. Faellt der Median der Nachbarn weit unter den Kandidaten,
   sitzt er auf einer Spitze.

2) Feine Zigzag-Verschiebung um +/- 0,5 Prozentpunkte - ausdruecklich
   verlangt und feiner als das Raster. Dafuer werden eigene Wellen
   berechnet; das ist kein Nachschlagen im Raster.

3) Reihenfolge-Empfindlichkeit - nur relevant, wo der Bot ein
   Positionslimit kennt (elliott_wave_stocks, Limit 8). Bei gleichem
   Einstiegszeitpunkt entscheidet die Zeilenreihenfolge, welcher Trade
   den letzten freien Platz bekommt; PR #23 hat gezeigt, dass das die
   Rendite um ueber 100 Prozentpunkte verschieben kann. Gemessen wird
   die Streuung ueber 200 zufaellige Permutationen der gleichzeitigen
   Einstiege (fester Startwert, damit der Lauf reproduzierbar ist).

Gerechnet wird auf dem Gesamtfenster (Schlagzeilenzahlen), der
Nachbarschaftsvergleich zusaetzlich auf dem In-Sample-Fenster, in dem
die Auswahl stattgefunden hat.

Nutzung:  python3 stability.py <elliott_wave|elliott_wave_stocks>
"""

import json
import os
import time

import numpy as np
import pandas as pd

import botenv

BOT = botenv.bot_from_argv()

import engine        # noqa: E402
import search        # noqa: E402
import walkforward as wf   # noqa: E402

FINE_STEP_PP = 0.5        # Zigzag-Verschiebung, wie in der Aufgabe verlangt
N_PERMUTATIONS = 200
SEED = 20260907


def neighbours(key):
    """Ein Rasterschritt nach oben und unten auf jeder Achse."""
    dev, stop, fib, use_tp = key
    devs = search.DEVIATION_RANGE
    stops = search.STOP_LOSS_RANGE
    targets = search.TARGET_RANGE

    out = []
    i = devs.index(dev) if dev in devs else None
    if i is not None:
        for j in (i - 1, i + 1):
            if 0 <= j < len(devs):
                out.append((devs[j], stop, fib, use_tp))
    i = stops.index(stop) if stop in stops else None
    if i is not None:
        for j in (i - 1, i + 1):
            if 0 <= j < len(stops):
                out.append((dev, stops[j], fib, use_tp))
    i = targets.index((fib, use_tp)) if (fib, use_tp) in targets else None
    if i is not None:
        for j in (i - 1, i + 1):
            if 0 <= j < len(targets):
                out.append((dev, stop, targets[j][0], targets[j][1]))
    return out


def grid_lookup(grid: pd.DataFrame, key):
    m = grid[(grid["deviation_pct"] == key[0]) & (grid["stop_loss_pct"] == key[1])
             & (grid["take_profit_fib"] == key[2]) & (grid["use_take_profit"] == key[3])]
    return m.iloc[0].to_dict() if len(m) else None


def evaluate(all_data, window, key):
    """Voller Durchlauf fuer eine Kombination - fuer Werte ausserhalb des Rasters."""
    dev, stop, fib, use_tp = key
    waves = engine.waves_for(window, all_data, dev)
    trades = engine.collect_trades(all_data, waves, stop, fib, use_tp)
    scored = engine.score_trades(trades)
    if scored is None:
        return {"num_trades": 0, "besteht_mindestfilter": False}, trades
    scored.update({f"pf_{k}": v for k, v in (engine.portfolio(trades) or {}).items()})
    return scored, trades


def order_band(trades: pd.DataFrame) -> dict:
    """Streuung der Portfolio-Kennzahlen ueber Permutationen der
    gleichzeitigen Einstiege (Methodik aus PR #23)."""
    if trades is None or trades.empty:
        return None
    if not engine.SUPPORTS_POSITION_LIMIT or engine.MAX_CONCURRENT is None:
        return {"hinweis": "kein Positionslimit - Reihenfolge ohne Einfluss"}

    rng = np.random.default_rng(SEED)
    trades = trades.sort_values("entry_time", kind="stable").reset_index(drop=True)
    groups = trades.groupby("entry_time", sort=False).indices
    ties = sum(1 for idx in groups.values() if len(idx) > 1)
    returns, calmars = [], []
    for _ in range(N_PERMUTATIONS):
        order = []
        for idx in groups.values():
            idx = list(idx)
            rng.shuffle(idx)
            order.extend(idx)
        res = engine.portfolio(trades, order=pd.Index(order))
        returns.append(res["total_return_pct"])
        calmars.append(res["calmar_ratio"])
    returns = np.array(returns, dtype=float)
    calmars = np.array([c for c in calmars if c is not None], dtype=float)
    return {
        "permutationen": N_PERMUTATIONS,
        "zeitpunkte_mit_gleichzeitigen_einstiegen": int(ties),
        "rendite_min_pct": round(float(returns.min()), 2),
        "rendite_median_pct": round(float(np.median(returns)), 2),
        "rendite_max_pct": round(float(returns.max()), 2),
        "rendite_spanne_pp": round(float(returns.max() - returns.min()), 2),
        "calmar_min": round(float(calmars.min()), 2) if len(calmars) else None,
        "calmar_median": round(float(np.median(calmars)), 2) if len(calmars) else None,
        "calmar_max": round(float(calmars.max()), 2) if len(calmars) else None,
    }


def main():
    botenv.print_hinweis()
    t_start = time.time()
    windows = engine.load_windows()
    candidates = wf.load_candidates()

    grids = {}
    for window in (engine.WINDOW_FULL, engine.WINDOW_IS, engine.WINDOW_OOS):
        path = os.path.join(botenv.RESULTS_DIR, f"{BOT}_grid_{window}.csv")
        if not os.path.exists(path):
            raise SystemExit(f"{path} fehlt - erst search.py laufen lassen.")
        grids[window] = pd.read_csv(path)

    out = {"hinweis": botenv.UNVALIDIERT_HINWEIS, "bot": BOT, "fine_step_pp": FINE_STEP_PP, "permutationen": N_PERMUTATIONS,
           "seed": SEED, "kandidaten": [], "laufzeit_s": None}

    for cand in candidates:
        key = cand["key"]
        name = wf.label(key)
        entry = {"kombination": name, "key": list(key), "herkunft": cand["herkunft"]}
        print(f"\n{'=' * 74}\n{name}   ({cand['herkunft']})\n{'=' * 74}")

        # --- 1) Rasternachbarschaft ---------------------------------
        entry["nachbarschaft"] = {}
        for window in (engine.WINDOW_IS, engine.WINDOW_FULL):
            self_row = grid_lookup(grids[window], key)
            rows = [grid_lookup(grids[window], n) for n in neighbours(key)]
            rows = [r for r in rows if r is not None]
            scores = [r["robustness_score"] for r in rows
                      if pd.notna(r.get("robustness_score"))]
            own = self_row.get("robustness_score") if self_row else None
            info = {
                "eigener_score": None if own is None or pd.isna(own) else round(float(own), 3),
                "nachbarn": len(rows),
                "nachbarn_bestehen_mindestfilter": int(sum(bool(r["besteht_mindestfilter"])
                                                            for r in rows)),
                "nachbar_score_median": round(float(np.median(scores)), 3) if scores else None,
                "nachbar_score_min": round(float(np.min(scores)), 3) if scores else None,
                "nachbar_score_max": round(float(np.max(scores)), 3) if scores else None,
            }
            if info["eigener_score"] and info["nachbar_score_median"] is not None:
                info["median_anteil_pct"] = round(
                    info["nachbar_score_median"] / info["eigener_score"] * 100, 1)
            entry["nachbarschaft"][window] = info
            print(f"  Nachbarschaft {window:<7} eigener Score {info['eigener_score']}, "
                  f"Nachbarn Median {info['nachbar_score_median']} "
                  f"(min {info['nachbar_score_min']}, max {info['nachbar_score_max']}), "
                  f"{info['nachbarn_bestehen_mindestfilter']}/{info['nachbarn']} bestehen")

        # --- 2) feine Zigzag-Verschiebung ---------------------------
        entry["zigzag_feinschritt"] = {}
        for window in (engine.WINDOW_FULL, engine.WINDOW_OOS):
            probes = {}
            for delta in (-FINE_STEP_PP, 0.0, FINE_STEP_PP):
                dev = round(key[0] + delta, 3)
                if dev <= 0:
                    continue
                res, _ = evaluate(windows[window], window, (dev, key[1], key[2], key[3]))
                probes[f"{dev:g}"] = res
            entry["zigzag_feinschritt"][window] = probes
            cells = ", ".join(
                f"{d} %: Score {r.get('robustness_score')}, Calmar {r.get('pf_calmar_ratio')}, "
                f"{r.get('num_trades')} T"
                for d, r in probes.items())
            print(f"  Zigzag +/-{FINE_STEP_PP} pp ({window}): {cells}")

        # --- 3) Reihenfolge-Empfindlichkeit -------------------------
        # Auch auf dem Out-of-Sample-Fenster, denn dort faellt die
        # Entscheidung gegen Buy-and-Hold - eine Kennzahl, die allein
        # von der Zeilenreihenfolge um dreistellige Prozentpunkte
        # wandert, taugt nicht als Einzelwert.
        entry["reihenfolge"] = {}
        for window in (engine.WINDOW_FULL, engine.WINDOW_OOS):
            _res, trades = evaluate(windows[window], window, key)
            band = order_band(trades)
            entry["reihenfolge"][window] = band
            if band and "rendite_spanne_pp" in band:
                print(f"  Reihenfolge ({window}): Rendite {band['rendite_min_pct']} .. "
                      f"{band['rendite_max_pct']} % (Spanne {band['rendite_spanne_pp']} pp), "
                      f"Calmar {band['calmar_min']} .. {band['calmar_max']}")
            else:
                print(f"  Reihenfolge ({window}): {band}")

        out["kandidaten"].append(entry)

    out["laufzeit_s"] = round(time.time() - t_start, 1)
    path = os.path.join(botenv.RESULTS_DIR, f"{BOT}_stability.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {path}  ({out['laufzeit_s']} s)")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()

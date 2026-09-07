"""
Aggregation der Einzelergebnisse zu einer Gesamttabelle
============================================================
Liest results/<bot>_atr<fenster>.json (erzeugt von run_one_bot.py) und
fasst sie zu results/summary_table.json plus einer Tabelle auf stdout
zusammen.

KLASSIFIKATIONS-HEURISTIKEN (selbst gewaehlt und hier dokumentiert, kein
Standardmass - identisch zur Vol-Sizing-Untersuchung, damit die vier
Backlog-Untersuchungen vergleichbar bleiben):

  "Verbesserung"      ja      = Calmar-Ratio der ATR-Trailing-Variante ist
                                SOWOHL In-Sample ALS AUCH Out-of-Sample
                                besser als die der Baseline
                      nein    = in beiden Perioden schlechter
                      unklar  = widerspruechliche Richtung zwischen IS und OOS
  "Walk-Forward-stabil" ja    = in mindestens 3 der 4 Stabilitaetsfenster
                                zeigt der Calmar-Vergleich dieselbe Richtung
                                wie das Gesamtbild
  "Episoden-getrieben"  ja    = mehr als 60 % des gesamten Renditeunterschieds
                                zwischen Baseline und ATR-Variante entfallen
                                auf ein EINZIGES Kalenderjahr (Pruefmuster aus
                                der Trend-Overlay-Untersuchung: ein nur ueber
                                eine Einzelepisode getriebener Effekt ist kein
                                robustes Ergebnis)

Nutzung:  python3 aggregate_report.py
"""

import json
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(_DIR, "results")

BASE = "fixed_static"
FIXTRAIL = "fixed_trailing"
ATRTRAIL = "atr_trailing"
PRIMARY_WINDOW = 14
ROBUSTNESS_WINDOW = 22
EPISODE_SHARE_THRESHOLD = 60.0


def load(bot: str, window: int) -> dict:
    path = os.path.join(RESULTS_DIR, f"{bot}_atr{window}.json")
    with open(path) as f:
        return json.load(f)


def better(a, b) -> int:
    """Vergleicht zwei Calmar-Ratios: 1 = a besser, -1 = b besser, 0 = nicht
    entscheidbar (mindestens eine Seite nicht definiert, z. B. Drawdown 0)."""
    if a is None or b is None:
        return 0
    return 1 if a > b else (-1 if a < b else 0)


def episode_concentration(data: dict) -> dict:
    """Wie stark haengt der Renditeunterschied Baseline vs. ATR-Trailing an
    einem EINZIGEN Kalenderjahr? (Pruefmuster aus der Trend-Overlay-
    Untersuchung.) Gemessen an der Summe der ABSOLUTBETRAEGE der jaehrlichen
    Renditedifferenzen - so heben sich gegenlaeufige Jahre nicht kuenstlich
    auf und ein einzelnes dominantes Jahr wird sichtbar."""
    diffs = {}
    for row in data["yearly"]:
        v = row["variants"]
        if v[BASE] is None or v[ATRTRAIL] is None:
            continue
        diffs[row["year"]] = v[ATRTRAIL]["total_return_pct"] - v[BASE]["total_return_pct"]
    if not diffs:
        return None
    total_abs = sum(abs(d) for d in diffs.values())
    if total_abs == 0:
        return {"dominant_year": None, "share_pct": 0.0, "diff_pct_points": 0.0, "driven_by_single_episode": False}
    year = max(diffs, key=lambda y: abs(diffs[y]))
    share = abs(diffs[year]) / total_abs * 100
    return {
        "dominant_year": year,
        "share_pct": round(share, 1),
        "diff_pct_points": round(diffs[year], 2),
        "driven_by_single_episode": share > EPISODE_SHARE_THRESHOLD,
    }


def summarise(bot: str) -> dict:
    data = load(bot, PRIMARY_WINDOW)
    per = data["periods"]

    is_dir = better(per["in_sample"][ATRTRAIL]["calmar_ratio"], per["in_sample"][BASE]["calmar_ratio"])
    oos_dir = better(per["out_of_sample"][ATRTRAIL]["calmar_ratio"], per["out_of_sample"][BASE]["calmar_ratio"])
    full_dir = better(per["full"][ATRTRAIL]["calmar_ratio"], per["full"][BASE]["calmar_ratio"])

    if is_dir == 0 or oos_dir == 0:
        verdict = "nicht auswertbar"
    elif is_dir > 0 and oos_dir > 0:
        verdict = "ja"
    elif is_dir < 0 and oos_dir < 0:
        verdict = "nein"
    else:
        verdict = "unklar"

    window_dirs = []
    for w in data["stability_windows"]:
        v = w["variants"]
        if v[BASE] is None or v[ATRTRAIL] is None:
            window_dirs.append(0)
            continue
        window_dirs.append(better(v[ATRTRAIL]["calmar_ratio"], v[BASE]["calmar_ratio"]))
    agreeing = sum(1 for d in window_dirs if d != 0 and d == full_dir)
    stable = agreeing >= 3

    robust = load(bot, ROBUSTNESS_WINDOW)["periods"]

    # Die beiden Elliott-Wave-Bots sind fuer diese Fragestellung NICHT
    # auswertbar: ihr Backtest steigt zum Zigzag-Wellenende ein, dem per
    # Konstruktion rueckwirkend eine Aufwaertsbewegung von mindestens
    # deviation_pct folgt (siehe run_one_bot.elliott_lookahead_diagnostic).
    # Ein Trailing-Stop verwandelt genau diesen bekannten Look-Ahead in
    # einen quasi-sicheren Gewinn - Gewinnraten um 100 %, Drawdowns nahe 0
    # und dadurch absurd hohe Calmar-Ratios. Das Urteil wird deshalb
    # UEBERSCHRIEBEN statt kommentarlos mitgezaehlt.
    diag = data.get("elliott_lookahead_diagnostic")
    caveat = None
    if diag is not None:
        caveat = (f"Zigzag-Look-Ahead im Einstiegskurs: {diag['share_reaching_deviation_pct']} % der "
                  f"Trades erreichen rueckwirkend garantiert mindestens {diag['deviation_pct']} % "
                  f"Kursanstieg (Median {diag['median_max_favourable_excursion_pct']} %). "
                  f"Trailing-Varianten erzielen dadurch Gewinnraten nahe 100 % - "
                  f"Vergleich NICHT interpretierbar.")
        verdict = "nicht interpretierbar"
        stable = None

    return {
        "bot": bot,
        "data_caveat": caveat,
        "atr_multiplier_k": data["assumptions"]["atr_multiplier_k"],
        "atr_multiplier_k_hypothetical_oos": data["assumptions"]["atr_multiplier_k_hypothetical_oos"],
        "baseline_stop_loss_pct": data["assumptions"]["stop_loss_pct_baseline"],
        "periods": {
            name: {v: {kk: per[name][v][kk] for kk in
                       ("num_trades", "total_return_pct", "max_drawdown_pct", "calmar_ratio",
                        "win_rate_pct", "avg_pnl_pct", "worst_trade_pct", "best_trade_pct",
                        "initial_stop_pct_p10", "initial_stop_pct_median",
                        "initial_stop_pct_p90", "initial_stop_pct_max")}
                   for v in (BASE, FIXTRAIL, ATRTRAIL)}
            for name in ("full", "in_sample", "out_of_sample")
        },
        "verdict_improvement": verdict,
        "walk_forward_stable": stable,
        "window_directions": window_dirs,
        "windows_agreeing_with_full": agreeing,
        "episode_concentration": episode_concentration(data),
        "robustness_atr22": {
            name: {v: {"total_return_pct": robust[name][v]["total_return_pct"],
                       "max_drawdown_pct": robust[name][v]["max_drawdown_pct"],
                       "calmar_ratio": robust[name][v]["calmar_ratio"]}
                   for v in (BASE, ATRTRAIL)}
            for name in ("full", "in_sample", "out_of_sample")
        },
    }


def fmt(value, suffix="") -> str:
    return "n/a" if value is None else f"{value}{suffix}"


def main():
    with open(os.path.join(RESULTS_DIR, "stop_inventory.json")) as f:
        inventory = json.load(f)
    bots = inventory["in_scope"]

    rows = [summarise(bot) for bot in bots]

    print("=" * 118)
    print("SCHRITT 1 - BESTANDSAUFNAHME")
    print("=" * 118)
    print(f"untersucht (fester %-Stop):        {', '.join(inventory['in_scope'])}")
    print(f"nicht untersucht (struktureller Stop): {', '.join(inventory['out_of_scope_structural']) or '-'}")
    print(f"nicht untersucht (kein Stop):      {', '.join(inventory['out_of_scope_no_stop']) or '-'}")

    for label, key in (("IN-SAMPLE", "in_sample"), ("OUT-OF-SAMPLE", "out_of_sample"), ("GESAMTZEITRAUM", "full")):
        print("\n" + "=" * 118)
        print(f"{label} - Rendite % / Max Drawdown % / Calmar-Ratio")
        print("=" * 118)
        print(f"{'Bot':<28}{'Baseline (fest, statisch)':>30}{'Fix-Trailing (Kontrolle)':>30}{'ATR-Trailing':>30}")
        for r in rows:
            cells = []
            for v in (BASE, FIXTRAIL, ATRTRAIL):
                p = r["periods"][key][v]
                cells.append(f"{p['total_return_pct']:>9.2f} /{p['max_drawdown_pct']:>7.2f} /{fmt(p['calmar_ratio']):>9}")
            print(f"{r['bot']:<28}" + "".join(f"{c:>30}" for c in cells))

    print("\n" + "=" * 118)
    print("BEWERTUNG (ATR-Trailing gegen Baseline, Calmar-Ratio)")
    print("=" * 118)
    print(f"{'Bot':<28}{'k':>7}{'Verbesserung':>22}{'WF-stabil':>11}{'Fenster':>10}  Episoden-Konzentration")
    for r in rows:
        ec = r["episode_concentration"]
        ec_txt = "n/a" if ec is None else (
            f"{ec['share_pct']:.0f} % des Unterschieds in {ec['dominant_year']}"
            + (" (EINZELEPISODE)" if ec["driven_by_single_episode"] else ""))
        stable_txt = "-" if r["walk_forward_stable"] is None else ("ja" if r["walk_forward_stable"] else "nein")
        print(f"{r['bot']:<28}{r['atr_multiplier_k']:>7.2f}{r['verdict_improvement']:>22}"
              f"{stable_txt:>11}{r['windows_agreeing_with_full']:>7}/4  {ec_txt}")

    caveats = [r for r in rows if r["data_caveat"]]
    if caveats:
        print("\nWICHTIGE EINSCHRAENKUNG:")
        for r in caveats:
            print(f"  {r['bot']}: {r['data_caveat']}")

    print("\n" + "=" * 118)
    print("ZERLEGUNG des Gesamteffekts (Calmar-Ratio, Gesamtzeitraum)")
    print("  A -> B = reines Nachziehen des Stops | B -> C = zusaetzlich volatilitaets-kalibrierte Distanz")
    print("=" * 118)
    print(f"{'Bot':<28}{'A Baseline':>13}{'B Fix-Trail':>13}{'C ATR-Trail':>13}{'A->B':>10}{'B->C':>10}")
    for r in rows:
        p = r["periods"]["full"]
        a, b, c = (p[BASE]["calmar_ratio"], p[FIXTRAIL]["calmar_ratio"], p[ATRTRAIL]["calmar_ratio"])
        ab = "n/a" if a is None or b is None else f"{b - a:+.2f}"
        bc = "n/a" if b is None or c is None else f"{c - b:+.2f}"
        print(f"{r['bot']:<28}{fmt(a):>13}{fmt(b):>13}{fmt(c):>13}{ab:>10}{bc:>10}")

    print("\n" + "=" * 118)
    print("STREUUNG DER ANFAENGLICHEN STOP-DISTANZ und Trade-Profil (Gesamtzeitraum)")
    print("  Der Median ist per Kalibrierung gleich - nur die STREUUNG unterscheidet die Varianten.")
    print("=" * 118)
    print(f"{'Bot':<28}{'Variante':<16}{'p10':>7}{'Median':>8}{'p90':>7}{'max':>7}"
          f"{'Win Rate':>10}{'O PnL':>9}{'schlecht.':>11}{'bester':>9}")
    for r in rows:
        for v, label in ((BASE, "Baseline"), (ATRTRAIL, "ATR-Trailing")):
            p = r["periods"]["full"][v]
            print(f"{r['bot'] if v == BASE else '':<28}{label:<16}"
                  f"{p['initial_stop_pct_p10']:>7.2f}{p['initial_stop_pct_median']:>8.2f}"
                  f"{p['initial_stop_pct_p90']:>7.2f}{p['initial_stop_pct_max']:>7.2f}"
                  f"{p['win_rate_pct']:>9.1f}%{p['avg_pnl_pct']:>8.2f}%"
                  f"{p['worst_trade_pct']:>10.2f}%{p['best_trade_pct']:>8.2f}%")

    print("\n" + "=" * 118)
    print(f"ROBUSTHEITS-ILLUSTRATION: ATR-{ROBUSTNESS_WINDOW} statt ATR-{PRIMARY_WINDOW} "
          f"(Out-of-Sample, ATR-Trailing) - KEINE Optimierung, nur ein zweiter Wert")
    print("=" * 118)
    print(f"{'Bot':<28}{'Rendite ATR-14':>18}{'Rendite ATR-22':>18}{'Calmar ATR-14':>18}{'Calmar ATR-22':>18}")
    for r in rows:
        p14 = r["periods"]["out_of_sample"][ATRTRAIL]
        p22 = r["robustness_atr22"]["out_of_sample"][ATRTRAIL]
        print(f"{r['bot']:<28}{p14['total_return_pct']:>17.2f}%{p22['total_return_pct']:>17.2f}%"
              f"{fmt(p14['calmar_ratio']):>18}{fmt(p22['calmar_ratio']):>18}")

    out_path = os.path.join(RESULTS_DIR, "summary_table.json")
    with open(out_path, "w") as f:
        json.dump({"inventory": inventory, "bots": rows,
                   "conventions": {
                       "calmar_ratio": "Gesamtrendite % / |Max Drawdown %| (wie Vol-Sizing, HRP, Trend-Overlay)",
                       "primary_atr_window": PRIMARY_WINDOW,
                       "robustness_atr_window": ROBUSTNESS_WINDOW,
                       "episode_share_threshold_pct": EPISODE_SHARE_THRESHOLD,
                   }}, f, indent=2)
    print(f"\nGespeichert: {out_path}")


if __name__ == "__main__":
    main()

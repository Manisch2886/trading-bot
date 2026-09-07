"""
Aggregiert die Einzelergebnisse zur geforderten Uebersichtstabelle.

Nutzung:  python3 aggregate_report.py
"""

import json
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(_DIR, "results")

BOTS = ["elliott_wave", "elliott_wave_stocks", "t3_supertrend",
        "rsi2_crypto", "rsi2_mean_reversion",
        "turtle_soup_crypto", "turtle_soup_stocks",
        "volatility_breakout", "volatility_breakout_crypto"]

# Einstufung der Betroffenheit - selbst gewaehlte, hier dokumentierte Heuristik.
# Massgeblich ist der Anteil UMSTRITTENER Trades (Ausfuehrungs-Status nicht
# konstant), nicht der Anteil geteilter Zeitstempel: ein Bot kann viele
# gleichzeitige Signale haben und trotzdem unempfindlich sein, wenn Kapital und
# Limit fuer alle reichen.
def classify(contested_pct: float, calmar_spread: dict) -> str:
    if contested_pct < 2.0:
        return "praktisch nicht betroffen"
    if calmar_spread and calmar_spread["min"] > 0:
        ratio = calmar_spread["max"] / calmar_spread["min"]
        if ratio >= 3.0:
            return "stark betroffen"
        if ratio >= 1.5:
            return "spuerbar betroffen"
    return "leicht betroffen"


def main():
    rows = []
    for bot in BOTS:
        path = os.path.join(RESULTS_DIR, f"{bot}.json")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            data = json.load(f)
        if "error" in data:
            continue
        ts, perms = data["timestamps"], data["permutations"]
        base, cfg = data["baseline_original_order"], data["config"]
        rows.append({
            "bot": bot,
            "trades": ts["n_trades"],
            "shared_pct": ts["share_sharing_entry_timestamp_pct"],
            "largest_group": ts["largest_same_timestamp_group"],
            "allocation_pct": cfg["allocation_pct"],
            "limit": cfg["max_concurrent_positions"],
            "executed": base["num_executed"],
            "skipped": base["num_skipped"],
            "skip_rate_pct": round(base["num_skipped"] / ts["n_trades"] * 100, 1),
            "skip_capital": perms["mean_skipped_capital"],
            "skip_limit": perms["mean_skipped_position_limit"],
            "contested": perms["trades_contested"],
            "contested_pct": perms["contested_share_pct"],
            "baseline_calmar": base["calmar_ratio"],
            "calmar": perms["calmar_ratio"],
            "drawdown": perms["max_drawdown_pct"],
            "percentile": data["baseline_percentile"]["calmar_ratio"],
            "mismatches": data["equivalence_check"]["mismatches"],
            "einstufung": classify(perms["contested_share_pct"], perms["calmar_ratio"]),
        })

    print("=" * 132)
    print("AUSMASS: geteilte Zeitstempel, Ablehnungen, umstrittene Trades")
    print("=" * 132)
    print(f"{'Bot':<28}{'Trades':>8}{'geteilt':>9}{'groesste':>10}{'Allok':>7}{'Limit':>7}"
          f"{'abgelehnt':>11}{'davon Kapital':>15}{'umstritten':>12}")
    for r in rows:
        limit = "kein" if r["limit"] is None else str(r["limit"])
        print(f"{r['bot']:<28}{r['trades']:>8}{r['shared_pct']:>8.1f}%{r['largest_group']:>10}"
              f"{r['allocation_pct']:>6.0%}{limit:>7}{r['skipped']:>8} ({r['skip_rate_pct']:>4.1f}%)"
              f"{r['skip_capital']:>15.1f}{r['contested']:>7} ({r['contested_pct']:>4.1f}%)")

    print("\n" + "=" * 132)
    print("AUSWIRKUNG: Calmar-Spanne ueber 500 Permutationen, Lage des urspruenglichen Werts")
    print("=" * 132)
    print(f"{'Bot':<28}{'urspruenglich':>15}{'min':>12}{'Median':>12}{'max':>12}"
          f"{'Faktor':>9}{'Perzentil':>11}  Einstufung")
    for r in rows:
        c = r["calmar"]
        factor = (f"{c['max'] / c['min']:.1f}x" if c and c["min"] > 0 else "n/a")
        print(f"{r['bot']:<28}{str(r['baseline_calmar']):>15}{c['min']:>12.2f}{c['median']:>12.2f}"
              f"{c['max']:>12.2f}{factor:>9}{str(r['percentile']):>11}  {r['einstufung']}")

    print("\n" + "=" * 132)
    print("MAX DRAWDOWN ueber die Permutationen")
    print("=" * 132)
    print(f"{'Bot':<28}{'min':>12}{'Median':>12}{'max':>12}")
    for r in rows:
        d = r["drawdown"]
        print(f"{r['bot']:<28}{d['min']:>12.2f}{d['median']:>12.2f}{d['max']:>12.2f}")

    print("\nAequivalenz-Check Schnellpfad gegen die bot-eigene simulate_portfolio: "
          f"{sum(r['mismatches'] for r in rows)} Abweichungen ueber alle Bots.")

    with open(os.path.join(RESULTS_DIR, "summary_table.json"), "w") as f:
        json.dump({"bots": rows}, f, indent=2)
    print(f"Gespeichert: {os.path.join(RESULTS_DIR, 'summary_table.json')}")


if __name__ == "__main__":
    main()

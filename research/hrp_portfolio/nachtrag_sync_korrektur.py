"""
Nachtrag: HRP-Untersuchung auf korrigierter Kapitalkurven-Grundlage
====================================================================================
Der Sync-Check (PR #24) hat belegt, dass die `equity_curve.csv`-Dateien bei
5 der 9 Bots nicht auf der Live-Konfiguration beruhen. Diese Studie baut ihr
Portfolio genau darauf auf.

Dieser Nachtrag wiederholt die Untersuchung mit korrigierten Kurven. **Nur
die Kurven aendern sich** - Rebalancing-Intervall, Linkage-Verfahren,
Mindest-Datenbasis-Schwelle, Bootstrap-Fallback, Buy-and-Hold-Referenz und
die gesamte Auswertung werden unveraendert aus `run_walk_forward.py`
importiert und aufgerufen. Es gibt hier bewusst KEINE zweite Umsetzung
derselben Rechnung.

Drei Grundlagen werden gerechnet:

  original                  die Kurven der Erstfassung - dient als
                            REGRESSIONSCHECK gegen results/hrp_summary.json
  korrigiert                die fuenf abweichenden Bots mit Live-Konfiguration
                            (die auftragsgemaesse Korrektur, PRIMAER)
  korrigiert_plus_veraltet  zusaetzlich elliott_wave neu erzeugt - siehe
                            corrected_curves.KNOWN_STALE_BOTS: dessen
                            gespeicherte Kurve stammt aus dem Initial Commit
                            und deckt 5 statt 18 Symbole ab. Das ist ein
                            eigenstaendiger, von der Sync-Abweichung
                            unabhaengiger Fund; er wird deshalb getrennt
                            ausgewiesen und nicht mit der Korrektur vermischt.

Reine Backtest-Untersuchung. `shared/portfolio_overview.py`,
`results/*/equity_curve.csv` und jeder Bot-Code bleiben unveraendert.

Nutzung:  python3 nachtrag_sync_korrektur.py
"""

import json
import os
import sys

import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
sys.path.insert(0, _DIR)
sys.path.insert(0, os.path.join(_REPO_ROOT, "shared"))

import corrected_curves as cc                    # noqa: E402
import portfolio_overview as po                  # noqa: E402
import run_walk_forward as rwf                   # noqa: E402
from bh_reference import buy_and_hold_curve      # noqa: E402

CURVE_DIR = os.path.join(_DIR, "corrected_curves")
RESULTS_DIR = rwf.RESULTS_DIR
REFERENCE_PATH = os.path.join(RESULTS_DIR, "hrp_summary.json")
TOL = 0.011

BASES = ("original", "korrigiert", "korrigiert_plus_veraltet")
SWAP_FOR = {
    "original": (),
    "korrigiert": cc.SWAP_PRIMARY,
    "korrigiert_plus_veraltet": cc.SWAP_WITH_STALE,
}

PASSED = FAILED = 0


def check(label, actual, expected, tol=TOL):
    global PASSED, FAILED
    if actual is None or expected is None:
        ok = actual == expected
        shown = str(actual)
    else:
        ok = abs(actual - expected) <= tol
        shown = f"{actual:.4f}"
    if ok:
        PASSED += 1
        print(f"  OK     {label:<50} {shown:>12}")
    else:
        FAILED += 1
        print(f"  FEHLER {label:<50} {shown:>12}  erwartet {expected}")


def analyse(basis: str, generated: dict) -> dict:
    """Die vollstaendige Auswertung der Erstfassung, Funktion fuer Funktion
    aus run_walk_forward.py - nur die Kurvenquelle unterscheidet sich."""
    bots, curves = cc.load_corrected_curves(po, generated, swap_bots=SWAP_FOR[basis])
    bot_names = sorted(curves.keys())

    common_start, common_end = rwf.common_window(curves)
    date_range = pd.date_range(common_start, common_end, freq="D")
    normalised = rwf.build_normalised_frame(curves, date_range)
    daily_returns = normalised.pct_change().dropna()
    trade_dates = {name: po.load_trade_dates(bots[name]) for name in bot_names}

    schedule = rwf.compute_walk_forward_weights(bot_names, daily_returns, trade_dates,
                                                 date_range, rwf.LINKAGE_METHOD)
    hrp_curve = rwf.apply_schedule(schedule, daily_returns)
    baseline_curve = rwf.static_equal_weight_curve(normalised)
    bh_curve, bh_num_symbols = buy_and_hold_curve(date_range)

    ward_summary, _ = rwf.compute_robustness_check(bot_names, daily_returns, trade_dates,
                                                    date_range, normalised)

    weight_rows = [{"quarter_start": e["quarter_start"], **e["weights"]} for e in schedule]
    weights_df = pd.DataFrame(weight_rows).set_index("quarter_start")
    swings = weights_df[bot_names].diff().abs().sum(axis=1).dropna()

    return {
        "basis": basis,
        "bots": bot_names,
        "common_window": {"start": str(common_start.date()), "end": str(common_end.date())},
        "hrp_walk_forward": rwf.summarise_curve(hrp_curve),
        "baseline_equal_weight": rwf.summarise_curve(baseline_curve),
        "buy_and_hold": rwf.summarise_curve(bh_curve) if not bh_curve.empty else None,
        "buy_and_hold_num_symbols": bh_num_symbols,
        "worst_individual_bot_max_drawdown_pct": min(rwf.max_drawdown_pct(normalised[b])
                                                      for b in bot_names),
        "robustness_check_ward_linkage": ward_summary,
        "weight_stability": {
            "mean_quarter_to_quarter_swing": round(float(swings.mean()), 4) if len(swings) else None,
            "max_quarter_to_quarter_swing": round(float(swings.max()), 4) if len(swings) else None,
            "num_quarters": len(schedule),
        },
        "final_weights": {b: round(float(weights_df[b].iloc[-1]), 4) for b in bot_names},
    }


def main():
    print("=" * 92)
    print("1) Korrigierte Kapitalkurven erzeugen (inkl. beider Proben)")
    print("=" * 92)
    generated = cc.generate(_REPO_ROOT, CURVE_DIR, po)

    print("\n" + "=" * 92)
    print("2) Regressionscheck - Basis 'original' gegen results/hrp_summary.json")
    print("=" * 92)
    if not os.path.exists(REFERENCE_PATH):
        raise SystemExit(f"{REFERENCE_PATH} fehlt - bitte zuerst run_walk_forward.py laufen lassen.")
    with open(REFERENCE_PATH) as handle:
        reference = json.load(handle)

    results = {basis: analyse(basis, generated) for basis in BASES}
    base = results["original"]

    for block in ("hrp_walk_forward", "baseline_equal_weight", "buy_and_hold",
                   "robustness_check_ward_linkage"):
        for key in ("total_return_pct", "max_drawdown_pct", "calmar_ratio"):
            check(f"{block} / {key}", base[block][key], reference[block][key])
    check("Buy-and-Hold Symbole", float(base["buy_and_hold_num_symbols"]),
          float(reference["buy_and_hold_num_symbols"]), 0)
    check("schlechtester Einzel-Bot Max-DD", base["worst_individual_bot_max_drawdown_pct"],
          reference["worst_individual_bot_max_drawdown_pct"])
    check("Gewichts-Swing (Mittel)", base["weight_stability"]["mean_quarter_to_quarter_swing"],
          reference["weight_stability"]["mean_quarter_to_quarter_swing"], 0.0005)

    if FAILED:
        print(f"\n{FAILED} Abweichungen - der Nachtrag waere nicht belastbar. Abbruch.")
        sys.exit(1)

    print("\n" + "=" * 92)
    print("3) Gegenueberstellung (Rendite % / Max Drawdown % / Calmar)")
    print("=" * 92)
    print(f"  {'Grundlage':<26}{'Fenster':<26}{'HRP':>26}{'Gleichgewichtung':>26}")
    for basis in BASES:
        r = results[basis]
        h, b = r["hrp_walk_forward"], r["baseline_equal_weight"]
        window = f"{r['common_window']['start']}..{r['common_window']['end']}"
        print(f"  {basis:<26}{window:<26}"
              f"{h['total_return_pct']:>9.2f}/{h['max_drawdown_pct']:>7.2f}/{str(h['calmar_ratio']):>8}"
              f"{b['total_return_pct']:>9.2f}/{b['max_drawdown_pct']:>7.2f}/{str(b['calmar_ratio']):>8}")

    print(f"\n  {'Grundlage':<26}{'HRP - Gleichgewichtung (Calmar)':>34}{'Kernaussage haelt?':>24}")
    for basis in BASES:
        r = results[basis]
        diff = r["hrp_walk_forward"]["calmar_ratio"] - r["baseline_equal_weight"]["calmar_ratio"]
        holds = "ja" if diff <= 0 else "NEIN - HRP waere besser"
        r["hrp_minus_baseline_calmar"] = round(diff, 4)
        r["kernaussage_haelt"] = diff <= 0
        print(f"  {basis:<26}{diff:>34.4f}{holds:>24}")

    print("\n  Buy-and-Hold-Referenz je Grundlage")
    for basis in BASES:
        bh = results[basis]["buy_and_hold"]
        print(f"    {basis:<26}{bh['total_return_pct']:>9.2f}%  DD {bh['max_drawdown_pct']:>7.2f}%  "
              f"Calmar {bh['calmar_ratio']}")

    out_path = os.path.join(RESULTS_DIR, "nachtrag_sync_korrektur.json")
    with open(out_path, "w") as handle:
        json.dump({
            "hinweis": ("Nachtrag zum Sync-Check. Nur die Kapitalkurven wurden korrigiert; "
                        "Methodik, Annahmen und Auswertung stammen unveraendert aus "
                        "run_walk_forward.py."),
            "kurven_erzeugung": {b: {"identisch_mit_original": v["identical_to_original"],
                                      **v["summary"]} for b, v in generated.items()},
            "regressionscheck_bestanden": PASSED,
            "ergebnisse": results,
        }, handle, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {out_path}")
    print(f"{PASSED} Referenzwerte bestaetigt, {FAILED} abweichend.")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()

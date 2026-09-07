"""
Nachtrag: Trend-Overlay auf korrigierter Kapitalkurven-Grundlage
====================================================================================
Der Sync-Check (PR #24) hat belegt, dass die `equity_curve.csv`-Dateien bei
5 der 9 Bots nicht auf der Live-Konfiguration beruhen. Diese Studie baut ihre
Baseline-Portfoliokurve genau darauf auf.

Dieser Nachtrag wiederholt die Untersuchung mit korrigierten Kurven. **Nur die
Kurven aendern sich** - Signal-Konstruktion (200-Tage-MA, logisches UND beider
Maerkte), Marktreferenzen, Fenstergroessen, Exponierungs-Varianten, IS/OOS-Split
und die 2022-Stressperiode werden unveraendert aus `run_overlay_analysis.py`
bzw. `trend_core.py` importiert und aufgerufen.

Die EINZIGE Neuschreibung ist `baseline_curve_for()`: das Original
`run_overlay_analysis.load_baseline_portfolio_curve()` hat keine Stelle, an der
sich die Kurvenquelle uebergeben liesse. Die Zeilen darin sind woertlich von
dort uebernommen; dass die Uebernahme stimmt, wird geprueft und nicht
behauptet - die Basis `original` muss `results/trend_overlay_summary.json`
exakt reproduzieren.

Drei Grundlagen:

  original                  die Kurven der Erstfassung - REGRESSIONSCHECK
  korrigiert                die fuenf abweichenden Bots mit Live-Konfiguration
                            (die auftragsgemaesse Korrektur, PRIMAER)
  korrigiert_plus_veraltet  zusaetzlich elliott_wave neu erzeugt - siehe
                            corrected_curves.KNOWN_STALE_BOTS

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
import run_overlay_analysis as roa               # noqa: E402
from trend_core import signal_active_stats       # noqa: E402

CURVE_DIR = os.path.join(_DIR, "corrected_curves")
RESULTS_DIR = roa.RESULTS_DIR
REFERENCE_PATH = os.path.join(RESULTS_DIR, "trend_overlay_summary.json")
TOL = 0.011

BASES = ("original", "korrigiert", "korrigiert_plus_veraltet")
SWAP_FOR = {"original": (), "korrigiert": cc.SWAP_PRIMARY,
            "korrigiert_plus_veraltet": cc.SWAP_WITH_STALE}
VARIANTS = ("baseline",) + tuple(roa.EXPOSURE_VARIANTS)

PASSED = FAILED = 0


def check(label, actual, expected, tol=TOL):
    global PASSED, FAILED
    ok = abs(actual - expected) <= tol
    if ok:
        PASSED += 1
        print(f"  OK     {label:<52} {actual:>12.4f}")
    else:
        FAILED += 1
        print(f"  FEHLER {label:<52} {actual:>12.4f}  erwartet {expected}")


def baseline_curve_for(generated: dict, swap_bots):
    """Woertliche Uebernahme von
    run_overlay_analysis.load_baseline_portfolio_curve() - nur die
    Kurvenquelle ist parametrisiert. Summe der normierten Bot-Kapitalkurven
    mal 1/N, OHNE Rebalancing."""
    _bots, curves = cc.load_corrected_curves(po, generated, swap_bots=swap_bots)
    bot_names = sorted(curves.keys())

    common_start = max(d["series"].index.min() for d in curves.values())
    common_end = min(d["series"].index.max() for d in curves.values())
    date_range = pd.date_range(common_start, common_end, freq="D")

    filled = {name: d["series"].reindex(date_range).ffill().bfill() for name, d in curves.items()}
    normalised = pd.DataFrame({name: s / s.iloc[0] * 100.0 for name, s in filled.items()})

    n = len(bot_names)
    portfolio = normalised.sum(axis=1) / n
    baseline_curve = portfolio / portfolio.iloc[0] * 100.0
    return baseline_curve, bot_names, date_range


def analyse(basis: str, generated: dict) -> dict:
    """Die vollstaendige Auswertung der Erstfassung, Funktion fuer Funktion
    aus run_overlay_analysis.py - nur die Kurvenquelle unterscheidet sich."""
    baseline_curve, bot_names, date_range = baseline_curve_for(generated, SWAP_FOR[basis])
    baseline_returns = baseline_curve.pct_change().dropna()

    combined_signal, _btc, _stocks = roa.build_combined_signal(date_range, roa.PRIMARY_WINDOW)
    signal = combined_signal.reindex(baseline_returns.index).fillna(False)

    split_idx = int(len(baseline_returns) * roa.TRAIN_SPLIT_RATIO)
    split_date = baseline_returns.index[split_idx]

    robustness_signal, _b, _s = roa.build_combined_signal(date_range, roa.ROBUSTNESS_WINDOW)
    robustness_signal = robustness_signal.reindex(baseline_returns.index).fillna(False)

    stress_start = pd.Timestamp(roa.STRESS_PERIOD_2022[0])
    stress_end = pd.Timestamp(roa.STRESS_PERIOD_2022[1])
    stress_slice = signal[(signal.index >= stress_start) & (signal.index <= stress_end)]

    return {
        "basis": basis,
        "bots": bot_names,
        "common_window": {"start": str(date_range.min().date()), "end": str(date_range.max().date())},
        "split_date": str(split_date.date()),
        "signal_stats_primary_window": signal_active_stats(signal),
        "signal_stats_robustness_window": signal_active_stats(robustness_signal),
        "stress_period_2022": {
            "days_in_window": int(len(stress_slice)),
            "stats": signal_active_stats(stress_slice) if len(stress_slice) else None,
        },
        "full_period": roa.evaluate_window(baseline_returns, signal),
        "in_sample": roa.evaluate_window(baseline_returns.iloc[:split_idx], signal.iloc[:split_idx]),
        "out_of_sample": roa.evaluate_window(baseline_returns.iloc[split_idx:], signal.iloc[split_idx:]),
        "robustness_check_150day_window": roa.evaluate_window(baseline_returns, robustness_signal),
    }


def main():
    print("=" * 96)
    print("1) Korrigierte Kapitalkurven erzeugen (inkl. beider Proben)")
    print("=" * 96)
    generated = cc.generate(_REPO_ROOT, CURVE_DIR, po)

    print("\n" + "=" * 96)
    print("2) Regressionscheck - Basis 'original' gegen results/trend_overlay_summary.json")
    print("=" * 96)
    if not os.path.exists(REFERENCE_PATH):
        raise SystemExit(f"{REFERENCE_PATH} fehlt - bitte zuerst run_overlay_analysis.py laufen lassen.")
    with open(REFERENCE_PATH) as handle:
        reference = json.load(handle)

    results = {basis: analyse(basis, generated) for basis in BASES}
    base = results["original"]

    for period in ("full_period", "in_sample", "out_of_sample", "robustness_check_150day_window"):
        for variant in VARIANTS:
            for key in ("total_return_pct", "max_drawdown_pct", "calmar_ratio"):
                check(f"{period} / {variant} / {key}",
                      base[period][variant][key], reference[period][variant][key])
    check("Signal aktive Tage (200)", float(base["signal_stats_primary_window"]["active_days"]),
          float(reference["signal_stats_primary_window"]["active_days"]), 0)
    check("Signal-Episoden (200)", float(base["signal_stats_primary_window"]["num_episodes"]),
          float(reference["signal_stats_primary_window"]["num_episodes"]), 0)
    check("2022 aktive Tage", float(base["stress_period_2022"]["stats"]["active_days"]),
          float(reference["stress_period_2022"]["stats"]["active_days"]), 0)

    if FAILED:
        print(f"\n{FAILED} Abweichungen - der Nachtrag waere nicht belastbar. Abbruch.")
        sys.exit(1)

    print("\n" + "=" * 96)
    print("3) Gegenueberstellung (Rendite % / Max Drawdown % / Calmar)")
    print("=" * 96)
    for period in ("full_period", "in_sample", "out_of_sample"):
        print(f"\n  {period}")
        print(f"    {'Grundlage':<28}" + "".join(f"{v:>28}" for v in VARIANTS))
        for basis in BASES:
            cells = ""
            for v in VARIANTS:
                r = results[basis][period][v]
                cells += (f"{r['total_return_pct']:>10.2f}/{r['max_drawdown_pct']:>7.2f}/"
                          f"{str(r['calmar_ratio']):>9}")
            print(f"    {basis:<28}{cells}")

    print("\n" + "=" * 96)
    print("4) Die drei Teilaussagen der Kernaussage - einzeln geprueft")
    print("=" * 96)
    print("   T1  Gesamtzeitraum: der Overlay verbessert die Calmar-Ratio")
    print("   T2  Out-of-Sample:  der Overlay bringt KEINE Drawdown-Verbesserung")
    print("   T3  Die Wirkung ist auf die eine 2022-Episode konzentriert")
    print("   Bewusst NICHT zu einem einzigen Ja/Nein verrechnet: die Teilaussagen")
    print("   koennen sich unterschiedlich verhalten, und genau das tun sie hier.")
    print()
    print(f"  {'Grundlage':<28}{'T1 Calmar-Gewinn':>19}{'T2 OOS-Drawdown':>26}"
          f"{'OOS-Calmar':>14}{'T3 Signaltage 2022':>21}")
    for basis in BASES:
        r = results[basis]
        full_gain = (r["full_period"]["pausiert_0pct"]["calmar_ratio"]
                     - r["full_period"]["baseline"]["calmar_ratio"])
        oos_gain = (r["out_of_sample"]["pausiert_0pct"]["calmar_ratio"]
                    - r["out_of_sample"]["baseline"]["calmar_ratio"])
        oos_dds = {v: r["out_of_sample"][v]["max_drawdown_pct"] for v in VARIANTS}
        oos_dd_same = len(set(oos_dds.values())) == 1
        stress = r["stress_period_2022"]["stats"]
        share_2022 = round(stress["active_days"] / r["signal_stats_primary_window"]["active_days"] * 100, 1)
        r["kernaussage"] = {
            "T1_full_period_calmar_gain": round(full_gain, 4),
            "T1_haelt": bool(full_gain > 0),
            "T2_out_of_sample_drawdowns": oos_dds,
            "T2_haelt": bool(oos_dd_same),
            "out_of_sample_calmar_gain": round(oos_gain, 4),
            "out_of_sample_calmar_richtung_wie_erstfassung": bool(oos_gain <= 0),
            "T3_anteil_signaltage_in_2022_pct": share_2022,
            "T3_laengste_episode_tage": r["signal_stats_primary_window"]["longest_episode_days"],
            "T3_haelt": bool(share_2022 > 60),
        }
        dd_text = f"identisch ({oos_dds['baseline']:.2f} %)" if oos_dd_same else "unterschiedlich"
        print(f"  {basis:<28}{full_gain:>+19.4f}{dd_text:>26}{oos_gain:>+14.4f}"
              f"{share_2022:>20.1f} %")
    print()
    print("  Das Signal selbst haengt NICHT von den Bot-Kurven ab (es kommt aus BTC und")
    print("  dem Aktien-Proxy) - T3 ist deshalb in allen drei Grundlagen zahlengleich.")

    out_path = os.path.join(RESULTS_DIR, "nachtrag_sync_korrektur.json")
    with open(out_path, "w") as handle:
        json.dump({
            "hinweis": ("Nachtrag zum Sync-Check. Nur die Kapitalkurven wurden korrigiert; "
                        "Signal-Konstruktion, Fenster und Auswertung stammen unveraendert "
                        "aus run_overlay_analysis.py / trend_core.py."),
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

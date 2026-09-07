"""
Portfolioweiter Trend-Overlay - retrospektive Backtest-Untersuchung
==========================================================================
Reine Backtest-Untersuchung (siehe BERICHT.md) - prueft retrospektiv, ob
ein aggregiertes "Krypto- UND Aktienmarkt gleichzeitig im Abwaertstrend"-
Signal eine erkennbare Schutzwirkung gehabt haette, WENN die
Gesamt-Marktexponierung des bestehenden, gleichgewichteten 9-Bot-
Portfolios (siehe research/hrp_portfolio, "bestehende Gleichgewichtung")
waehrend aktiver Signal-Phasen reduziert worden waere. REIN
BEOBACHTEND/RETROSPEKTIV - kein Live-Eingriff, keine Aenderung an
Live-Dateien.

WICHTIG: importiert NUR LESEND aus shared/portfolio_overview.py
(Datenquellen-Logik) - schreibt NIRGENDS in shared/, veraendert KEINE
Live-Datei. Alle Ergebnisse landen ausschliesslich unter
research/trend_overlay/results/.

Nutzung:
    python3 run_overlay_analysis.py
"""
import os
import sys
import json

import numpy as np
import pandas as pd

_RESEARCH_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_RESEARCH_DIR))
_SHARED_DIR = os.path.join(_REPO_ROOT, "shared")
sys.path.insert(0, _RESEARCH_DIR)
sys.path.insert(0, _SHARED_DIR)

from trend_core import (
    compute_downtrend_signal, combine_signals_and, apply_overlay_to_returns,
    signal_active_stats,
)
from market_proxies import load_crypto_reference, load_stock_market_proxy

import portfolio_overview as po

RESULTS_DIR = os.path.join(_RESEARCH_DIR, "results")

# ANNAHME 1: Fenstergroesse des gleitenden Durchschnitts. 200 Handelstage
# ist die in der Aufgabenstellung selbst vorgeschlagene, in der Praxis
# etablierte "lange" Trendreferenz (vgl. die verbreitete 200-Tage-Linie
# im Aktienbereich). Bewusst EIN einzelner, begruendeter Wert - KEINE
# Optimierung ueber mehrere Fenster (Overfitting-Risiko). 150 Tage wird
# NUR zur Robustheits-Illustration zusaetzlich berechnet (siehe
# compute_robustness_check), NICHT um das "bessere" Ergebnis auszuwaehlen.
PRIMARY_WINDOW = 200
ROBUSTNESS_WINDOW = 150

# ANNAHME 2: zwei Reduktions-Varianten, beide von der Aufgabenstellung
# selbst als Optionen genannt ("auf 50% ... oder ganz pausiert") - werden
# hier NICHT gegeneinander optimiert, sondern beide transparent berichtet
# (anders als die Fenstergroesse ist das keine Modell-Parameter-Wahl mit
# Overfitting-Risiko, sondern zwei unterschiedliche, gleichermassen
# plausible Szenarien).
EXPOSURE_VARIANTS = {"reduziert_50pct": 0.5, "pausiert_0pct": 0.0}

TRAIN_SPLIT_RATIO = 0.7  # dieselbe Konvention wie in allen 9 Bots (multi_symbol_walk_forward.py)

STRESS_PERIOD_2022 = ("2022-01-01", "2022-12-31")


def load_baseline_portfolio_curve():
    """Baut die 'bestehende Gleichgewichtung' EXAKT wie in
    research/hrp_portfolio/run_walk_forward.py::static_equal_weight_curve:
    Summe der normierten Bot-Kapitalkurven * 1/N, OHNE Rebalancing -
    dieselbe Referenz, auf die sich diese Aufgabenstellung explizit
    bezieht ("siehe HRP-Untersuchung als Referenz")."""
    bots = po.discover_bots()
    curves = po.load_all_curves(bots)
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


def build_combined_signal(date_range: pd.DatetimeIndex, window: int) -> tuple:
    """Baut das aggregierte 'beide Maerkte im Abwaertstrend'-Signal ueber
    date_range. Laedt die Referenzserien MIT Vorlauf vor date_range.min()
    (fuer die MA-Anlaufphase), berechnet die Einzel-Signale auf der
    VOLLEN geladenen Historie (kein Blick in die Zukunft - siehe
    trend_core.py), schneidet danach erst auf date_range zu. Krypto
    handelt 24/7 (kein Reindex-Problem), Aktien nur an Boersentagen -
    das taegliche Aktien-Signal wird per ffill auf Kalendertage
    uebertragen (an Wochenenden/Feiertagen gilt der zuletzt bekannte
    Boersentags-Zustand weiter, konsistent mit der Kapitalkurven-
    Behandlung in shared/portfolio_overview.py)."""
    btc_prices = load_crypto_reference()
    stock_proxy = load_stock_market_proxy()

    btc_signal_full = compute_downtrend_signal(btc_prices, window)
    stock_signal_full = compute_downtrend_signal(stock_proxy, window)

    btc_signal = btc_signal_full.reindex(date_range).ffill().fillna(False)
    stock_signal = stock_signal_full.reindex(date_range).ffill().fillna(False)

    combined = combine_signals_and(btc_signal, stock_signal)
    return combined, btc_signal, stock_signal


def max_drawdown_pct(curve: pd.Series) -> float:
    running_max = curve.cummax()
    return round(float(((curve - running_max) / running_max * 100).min()), 2)


def calmar_ratio(total_return_pct: float, max_dd_pct: float):
    if max_dd_pct == 0:
        return None
    return round(total_return_pct / abs(max_dd_pct), 4)


def curve_from_returns(daily_returns: pd.Series, start_value: float = 100.0) -> pd.Series:
    equity = start_value * (1.0 + daily_returns).cumprod()
    first_date = daily_returns.index.min() - pd.Timedelta(days=1)
    return pd.concat([pd.Series([start_value], index=[first_date]), equity])


def summarise(curve: pd.Series) -> dict:
    total_return = round(float(curve.iloc[-1] / curve.iloc[0] * 100.0 - 100.0), 2)
    dd = max_drawdown_pct(curve)
    return {"total_return_pct": total_return, "max_drawdown_pct": dd, "calmar_ratio": calmar_ratio(total_return, dd)}


def evaluate_window(baseline_returns: pd.Series, signal: pd.Series) -> dict:
    """Vergleicht Baseline (kein Overlay) vs. beide Overlay-Varianten auf
    EINEM Zeitabschnitt (voller Zeitraum, In-Sample oder Out-of-Sample)."""
    baseline_curve = curve_from_returns(baseline_returns)
    result = {"baseline": summarise(baseline_curve)}
    for variant_name, exposure in EXPOSURE_VARIANTS.items():
        overlay_returns = apply_overlay_to_returns(baseline_returns, signal, exposure)
        overlay_curve = curve_from_returns(overlay_returns)
        result[variant_name] = summarise(overlay_curve)
    return result


def main():
    print("=" * 70)
    print("PORTFOLIOWEITER TREND-OVERLAY - RETROSPEKTIVE UNTERSUCHUNG (Backtest-Only)")
    print("=" * 70)

    baseline_curve, bot_names, date_range = load_baseline_portfolio_curve()
    common_start, common_end = date_range.min(), date_range.max()
    print(f"\n{len(bot_names)} Bots, gemeinsames Vergleichsfenster: "
          f"{common_start.date()} bis {common_end.date()}")

    baseline_returns = baseline_curve.pct_change().dropna()

    print(f"\nBerechne Trend-Signal (Fenster: {PRIMARY_WINDOW} Tage)...")
    combined_signal, btc_signal, stock_signal = build_combined_signal(date_range, PRIMARY_WINDOW)
    signal_for_returns = combined_signal.reindex(baseline_returns.index).fillna(False)

    stats = signal_active_stats(signal_for_returns)
    print(f"Signal aktiv an {stats['active_days']} von {stats['total_days']} Tagen "
          f"({stats['active_pct']}%), {stats['num_episodes']} Episoden, "
          f"laengste Episode {stats['longest_episode_days']} Tage")

    # Full-period, In-Sample, Out-of-Sample Auswertung
    split_idx = int(len(baseline_returns) * TRAIN_SPLIT_RATIO)
    split_date = baseline_returns.index[split_idx]
    is_returns = baseline_returns.iloc[:split_idx]
    oos_returns = baseline_returns.iloc[split_idx:]
    is_signal = signal_for_returns.iloc[:split_idx]
    oos_signal = signal_for_returns.iloc[split_idx:]

    full_result = evaluate_window(baseline_returns, signal_for_returns)
    is_result = evaluate_window(is_returns, is_signal)
    oos_result = evaluate_window(oos_returns, oos_signal)

    print("\n" + "=" * 70)
    print("ERGEBNIS (Gesamtzeitraum)")
    print("=" * 70)
    for name, summary in full_result.items():
        print(f"{name:20s}: Rendite {summary['total_return_pct']:8.2f}%  "
              f"Max-DD {summary['max_drawdown_pct']:7.2f}%  Calmar {summary['calmar_ratio']}")

    # 2022-Stresstest-Abgleich
    stress_start, stress_end = pd.Timestamp(STRESS_PERIOD_2022[0]), pd.Timestamp(STRESS_PERIOD_2022[1])
    stress_mask = (signal_for_returns.index >= stress_start) & (signal_for_returns.index <= stress_end)
    stress_slice = signal_for_returns[stress_mask]
    if len(stress_slice) > 0:
        stress_stats = signal_active_stats(stress_slice)
    else:
        stress_stats = None
    print(f"\n2022-Stresstest-Abgleich: {len(stress_slice)} Tage im gemeinsamen "
          f"Fenster liegen in 2022" +
          (f", davon {stress_stats['active_days']} Tage ({stress_stats['active_pct']}%) mit "
           f"aktivem Signal" if stress_stats else " (kein Ueberlappungsdaten im gemeinsamen Fenster)"))

    # Robustheits-Illustration (150-Tage-Fenster statt 200)
    print(f"\nBerechne Robustheits-Illustration ({ROBUSTNESS_WINDOW}-Tage-Fenster, "
          f"NICHT als 'besseres' Ergebnis ausgewaehlt)...")
    robustness_signal, _, _ = build_combined_signal(date_range, ROBUSTNESS_WINDOW)
    robustness_signal_for_returns = robustness_signal.reindex(baseline_returns.index).fillna(False)
    robustness_stats = signal_active_stats(robustness_signal_for_returns)
    robustness_result = evaluate_window(baseline_returns, robustness_signal_for_returns)
    print(f"Signal ({ROBUSTNESS_WINDOW} Tage) aktiv an {robustness_stats['active_days']} von "
          f"{robustness_stats['total_days']} Tagen ({robustness_stats['active_pct']}%)")
    for name, summary in robustness_result.items():
        print(f"  {name:20s}: Rendite {summary['total_return_pct']:8.2f}%  "
              f"Max-DD {summary['max_drawdown_pct']:7.2f}%  Calmar {summary['calmar_ratio']}")

    # Strukturelle Verbesserungsmarge (Aufgaben-Vorgabe: explizit einordnen)
    baseline_dd = full_result["baseline"]["max_drawdown_pct"]
    # Drawdowns sind negative Zahlen - das BESTE (am wenigsten negative,
    # naeheste an 0) Ergebnis ist das Maximum, nicht das Minimum.
    best_overlay_dd = max(full_result[v]["max_drawdown_pct"] for v in EXPOSURE_VARIANTS)
    dd_improvement_pp = round(best_overlay_dd - baseline_dd, 2)  # positiv = Verbesserung (Drawdown naeher an 0)
    print(f"\nStrukturelle Verbesserungsmarge: Baseline Max-DD {baseline_dd}%, "
          f"bester Overlay Max-DD {best_overlay_dd}% "
          f"(Differenz {round(best_overlay_dd - baseline_dd, 2)} Prozentpunkte)")

    os.makedirs(RESULTS_DIR, exist_ok=True)

    signals_out = pd.DataFrame({
        "btc_signal": btc_signal.reindex(date_range),
        "stock_signal": stock_signal.reindex(date_range),
        "combined_signal": combined_signal.reindex(date_range),
    })
    signals_out.to_csv(os.path.join(RESULTS_DIR, "signal_timeline.csv"))

    baseline_curve.to_frame("baseline_curve").to_csv(os.path.join(RESULTS_DIR, "baseline_curve.csv"))

    result = {
        "bots": bot_names,
        "common_window": {"start": str(common_start.date()), "end": str(common_end.date())},
        "primary_window_days": PRIMARY_WINDOW,
        "robustness_window_days": ROBUSTNESS_WINDOW,
        "train_split_ratio": TRAIN_SPLIT_RATIO,
        "split_date": str(split_date.date()),
        "signal_stats_primary_window": stats,
        "signal_stats_robustness_window": robustness_stats,
        "stress_period_2022": {
            "days_in_window": int(len(stress_slice)),
            "stats": stress_stats,
        },
        "full_period": full_result,
        "in_sample": is_result,
        "out_of_sample": oos_result,
        "robustness_check_150day_window": robustness_result,
        "structural_improvement_margin": {
            "baseline_max_drawdown_pct": baseline_dd,
            "best_overlay_max_drawdown_pct": best_overlay_dd,
            "max_drawdown_change_pp": dd_improvement_pp,
        },
    }
    with open(os.path.join(RESULTS_DIR, "trend_overlay_summary.json"), "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"\nErgebnisse gespeichert unter: {RESULTS_DIR}/")


if __name__ == "__main__":
    main()

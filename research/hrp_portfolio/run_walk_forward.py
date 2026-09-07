"""
Hierarchical Risk Parity (HRP) - Walk-Forward-Untersuchung fuer das
kombinierte 9-Bot-Portfolio
==========================================================================
Reine Backtest-Untersuchung (siehe BERICHT.md) - vergleicht drei
Gewichtungsvarianten fuer das KOMBINIERTE Portfolio ueber den gemeinsamen
Vergleichszeitraum aller 9 Bots (dieselbe Fenster-Logik wie in
shared/portfolio_overview.py::run_analysis):

1. HRP, WALK-FORWARD rebalanciert (quartalsweise, expandierendes
   Trainingsfenster - siehe rebalance_dates()) - die eigentliche
   Untersuchungsgroesse.
2. Bestehende Gleichgewichtung (je 1/9 = 11.1%, EINMALIG zu Beginn
   angelegt, danach NICHT rebalanciert - identisch zur Methode in
   shared/portfolio_overview.py::run_analysis, dort "Portfolio
   (gewichtet)" genannt).
3. Gemeinsame Buy-and-Hold-Referenz auf Symbol-Ebene (siehe
   bh_reference.py).

WICHTIG - reine Backtest-Untersuchung: importiert NUR LESEND aus
shared/portfolio_overview.py (Datenquellen-Logik, Korrelations-
Handelstage-Konvention) - schreibt NIRGENDS in shared/, veraendert KEINE
Live-Datei. Alle Ergebnisse landen ausschliesslich unter
research/hrp_portfolio/results/.

Nutzung:
    python3 run_walk_forward.py
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

from hrp_core import hrp_weights, find_max_reliable_subset, blend_with_fallback
from bh_reference import buy_and_hold_curve

import portfolio_overview as po

RESULTS_DIR = os.path.join(_RESEARCH_DIR, "results")

# ANNAHME 1: Rebalancing-Intervall. Die Aufgabe schlaegt "quartalsweise"
# selbst als Beispiel vor und verlangt eine Begruendung. Gewaehlt:
# KALENDER-Quartale - erstens, weil dieses Intervall im Projekt bereits als
# etablierter Rhythmus existiert (siehe quarterly_review.py bei
# elliott_wave/elliott_wave_stocks/t3_supertrend), zweitens als Kompromiss
# zwischen genug Traegheit (Korrelationsschaetzungen aus taeglichen Bot-
# Renditen sind verrauscht - monatliches Rebalancing wuerde staerker auf
# Rauschen statt echte Regimewechsel reagieren) und genug Reaktionsfaehigkeit
# (jaehrliches Rebalancing waere zu traege). KEINE Optimierung ueber mehrere
# Intervalle - eine einzige, begruendete Wahl, siehe BERICHT.md fuer eine
# Stabilitaets-Illustration mit dem Linkage-Verfahren statt dem Intervall.
REBALANCE_FREQ = "Q"

# ANNAHME 2: Clustering-Methode. 'single' Linkage ist die im Original-Paper
# (Lopez de Prado 2016) verwendete Methode - siehe hrp_core.py. 'ward' wird
# NUR zur Robustheits-Illustration zusaetzlich berechnet (siehe
# compute_robustness_check), NICHT um "das bessere Ergebnis" auszuwaehlen.
LINKAGE_METHOD = "single"
LINKAGE_METHOD_ROBUSTNESS_CHECK = "ward"

MIN_COMMON_TRADING_DAYS = po.MIN_COMMON_TRADING_DAYS  # dieselbe Schwelle wie portfolio_overview.py (30)


def load_bot_curves():
    bots = po.discover_bots()
    curves = po.load_all_curves(bots)
    return bots, curves


def common_window(curves: dict):
    common_start = max(d["series"].index.min() for d in curves.values())
    common_end = min(d["series"].index.max() for d in curves.values())
    return common_start, common_end


def build_normalised_frame(curves: dict, date_range: pd.DatetimeIndex) -> pd.DataFrame:
    filled = {name: d["series"].reindex(date_range).ffill().bfill() for name, d in curves.items()}
    return pd.DataFrame({name: s / s.iloc[0] * 100.0 for name, s in filled.items()})


def max_drawdown_pct(curve: pd.Series) -> float:
    running_max = curve.cummax()
    return round(float(((curve - running_max) / running_max * 100).min()), 2)


def calmar_ratio(total_return_pct: float, max_dd_pct: float):
    if max_dd_pct == 0:
        return None
    return round(total_return_pct / abs(max_dd_pct), 4)


def build_sufficiency_matrix(bot_names: list, trade_dates: dict, window_dates: pd.DatetimeIndex) -> pd.DataFrame:
    """Paarweise 'ausreichend Datenbasis'-Matrix, EXAKT dieselbe Definition
    wie shared/portfolio_overview.py::run_analysis Teil 3: mindestens
    MIN_COMMON_TRADING_DAYS Tage, an denen BEIDE Bots im uebergebenen
    Fenster (window_dates) tatsaechlich einen Trade abgeschlossen haben -
    hier angewendet auf das jeweilige TRAININGSFENSTER einer
    Walk-Forward-Periode statt auf den gesamten Vergleichszeitraum."""
    n = len(bot_names)
    matrix = pd.DataFrame(True, index=bot_names, columns=bot_names)
    if len(window_dates) == 0:
        matrix.loc[:, :] = False
        for b in bot_names:
            matrix.loc[b, b] = True
        return matrix

    win_start, win_end = window_dates.min(), window_dates.max()
    active = {}
    for name in bot_names:
        dates = trade_dates[name]
        in_window = dates[(dates >= win_start) & (dates <= win_end)]
        active[name] = window_dates.isin(in_window)

    for i in range(n):
        for j in range(i + 1, n):
            a, b = bot_names[i], bot_names[j]
            common_days = int((active[a] & active[b]).sum())
            sufficient = common_days >= MIN_COMMON_TRADING_DAYS
            matrix.loc[a, b] = sufficient
            matrix.loc[b, a] = sufficient
    return matrix


def rebalance_periods(date_range: pd.DatetimeIndex) -> list:
    """Teilt date_range in Kalender-Quartale. Liefert eine Liste von
    (quartals_start, quartals_end, ist_bootstrap_quartal) - das ERSTE
    Quartal hat per Definition kein vorheriges Trainingsfenster
    (ist_bootstrap_quartal=True) und wird gleichgewichtet gefahren
    (ANNAHME 3, siehe BERICHT.md: unvermeidbar, es gibt schlicht noch keine
    Historie, aus der HRP etwas lernen koennte)."""
    quarters = sorted(set(date_range.to_period("Q")))
    periods = []
    for i, q in enumerate(quarters):
        q_start = max(q.start_time, date_range.min())
        q_end = min(q.end_time, date_range.max())
        mask = (date_range >= q_start) & (date_range <= q_end)
        q_dates = date_range[mask]
        if len(q_dates) == 0:
            continue
        periods.append((q_dates, i == 0))
    return periods


def compute_walk_forward_weights(bot_names: list, daily_returns: pd.DataFrame,
                                  trade_dates: dict, date_range: pd.DatetimeIndex,
                                  linkage_method: str) -> list:
    """Kernstueck der Walk-Forward-Methodik: fuer jedes Quartal (ausser dem
    allerersten Bootstrap-Quartal) werden die HRP-Gewichte AUSSCHLIESSLICH
    aus Renditen VOR Quartalsbeginn berechnet (expandierendes Fenster -
    Quartal 5 nutzt die gesamte Historie von Quartal 1-4, nicht nur
    Quartal 4) und dann auf das NAECHSTE, noch unbekannte Quartal
    angewendet - kein Blick in die Zukunft. Liefert eine Liste von
    {quarter_start, quarter_end, weights, reliable_subset, bootstrap} je
    Quartal."""
    n = len(bot_names)
    equal_weights = pd.Series(1.0 / n, index=bot_names)
    periods = rebalance_periods(date_range)

    schedule = []
    for q_dates, is_bootstrap in periods:
        q_start, q_end = q_dates.min(), q_dates.max()

        if is_bootstrap:
            weights = equal_weights.copy()
            reliable_subset = []
        else:
            training_dates = date_range[date_range < q_start]
            training_returns = daily_returns.loc[daily_returns.index < q_start]
            if len(training_returns) < 2:
                weights = equal_weights.copy()
                reliable_subset = []
            else:
                sufficiency = build_sufficiency_matrix(bot_names, trade_dates, training_dates)
                reliable_subset = find_max_reliable_subset(sufficiency, bot_names)
                if len(reliable_subset) >= 2:
                    subset_hrp = hrp_weights(training_returns[reliable_subset], linkage_method=linkage_method)
                    weights = blend_with_fallback(subset_hrp, bot_names)
                else:
                    weights = equal_weights.copy()

        schedule.append({
            "quarter_start": str(q_start.date()),
            "quarter_end": str(q_end.date()),
            "bootstrap": is_bootstrap,
            "reliable_subset": reliable_subset,
            "excluded": [b for b in bot_names if b not in reliable_subset] if reliable_subset else [],
            "weights": {b: round(float(weights[b]), 6) for b in bot_names},
            "dates": q_dates,
        })
    return schedule


def apply_schedule(schedule: list, daily_returns: pd.DataFrame) -> pd.Series:
    """Wendet je Quartal die (bereits VORAB, ohne Blick in dieses Quartal
    berechneten) Gewichte auf die TATSAECHLICHEN taeglichen Bot-Renditen
    dieses Quartals an - liefert die tatsaechliche, nicht geschoente
    taegliche Portfolio-Rendite ueber den gesamten Zeitraum."""
    daily_portfolio_returns = []
    for entry in schedule:
        q_returns = daily_returns.reindex(entry["dates"]).fillna(0.0)
        weights = pd.Series(entry["weights"])
        weighted = (q_returns[weights.index] * weights).sum(axis=1)
        daily_portfolio_returns.append(weighted)
    combined = pd.concat(daily_portfolio_returns).sort_index()
    equity = 100.0 * (1.0 + combined).cumprod()
    equity = pd.concat([pd.Series([100.0], index=[combined.index.min() - pd.Timedelta(days=1)]), equity])
    return equity


def static_equal_weight_curve(normalised: pd.DataFrame) -> pd.Series:
    """'Bestehende Gleichgewichtung' - EXAKT dieselbe Methode wie
    shared/portfolio_overview.py::run_analysis: Summe der normierten
    Einzelkurven * 1/N, OHNE jegliches Rebalancing (buy-and-hold-artig,
    Gewichte drieften mit der individuellen Bot-Performance auseinander)."""
    n = normalised.shape[1]
    portfolio = normalised.sum(axis=1) / n
    return portfolio / portfolio.iloc[0] * 100.0


def summarise_curve(curve: pd.Series) -> dict:
    total_return = round(float(curve.iloc[-1] / curve.iloc[0] * 100.0 - 100.0), 2)
    dd = max_drawdown_pct(curve)
    return {
        "total_return_pct": total_return,
        "max_drawdown_pct": dd,
        "calmar_ratio": calmar_ratio(total_return, dd),
    }


def compute_robustness_check(bot_names, daily_returns, trade_dates, date_range, normalised):
    """Illustriert die Parameter-Sensitivitaet der Clustering-Methode
    (Vorgabe der Aufgabenstellung: EINE begruendete Wahl treffen, aber bei
    Bedarf eine zweite zur Robustheits-Illustration zeigen - NICHT das
    beste Ergebnis auswaehlen). Nutzt EXAKT dasselbe Rebalancing-Schema,
    nur mit 'ward' statt 'single' Linkage."""
    schedule_ward = compute_walk_forward_weights(
        bot_names, daily_returns, trade_dates, date_range, LINKAGE_METHOD_ROBUSTNESS_CHECK)
    curve_ward = apply_schedule(schedule_ward, daily_returns)
    return summarise_curve(curve_ward), schedule_ward


def main():
    print("=" * 70)
    print("HRP-PORTFOLIO-UNTERSUCHUNG (Walk-Forward, Backtest-Only)")
    print("=" * 70)

    bots, curves = load_bot_curves()
    bot_names = sorted(curves.keys())
    n = len(bot_names)
    print(f"\nGefundene Bots mit verwertbaren Daten ({n}): "
          f"{', '.join(po.display_name(b) for b in bot_names)}")
    if n < 3:
        print("Zu wenige Bots mit Daten fuer eine sinnvolle HRP-Untersuchung.")
        return

    common_start, common_end = common_window(curves)
    print(f"Gemeinsames Vergleichsfenster: {common_start.date()} bis {common_end.date()}")
    date_range = pd.date_range(common_start, common_end, freq="D")

    normalised = build_normalised_frame(curves, date_range)
    daily_returns = normalised.pct_change().dropna()

    trade_dates = {name: po.load_trade_dates(bots[name]) for name in bot_names}

    print(f"\nBerechne Walk-Forward-Rebalancing (Intervall: {REBALANCE_FREQ}, "
          f"Linkage: {LINKAGE_METHOD})...")
    schedule = compute_walk_forward_weights(bot_names, daily_returns, trade_dates, date_range, LINKAGE_METHOD)
    hrp_curve = apply_schedule(schedule, daily_returns)

    baseline_curve = static_equal_weight_curve(normalised)

    print("Berechne Buy-and-Hold-Referenz...")
    bh_curve, bh_num_symbols = buy_and_hold_curve(date_range)

    hrp_summary = summarise_curve(hrp_curve)
    baseline_summary = summarise_curve(baseline_curve)
    bh_summary = summarise_curve(bh_curve) if not bh_curve.empty else None

    worst_individual_dd = min(max_drawdown_pct(normalised[b]) for b in bot_names)

    print("\n" + "=" * 70)
    print("ERGEBNIS")
    print("=" * 70)
    print(f"HRP (Walk-Forward):        Rendite {hrp_summary['total_return_pct']:.2f}%  "
          f"Max-DD {hrp_summary['max_drawdown_pct']:.2f}%  Calmar {hrp_summary['calmar_ratio']}")
    print(f"Bestehende Gleichgewichtung: Rendite {baseline_summary['total_return_pct']:.2f}%  "
          f"Max-DD {baseline_summary['max_drawdown_pct']:.2f}%  Calmar {baseline_summary['calmar_ratio']}")
    if bh_summary:
        print(f"Buy-and-Hold (Referenz, {bh_num_symbols} Symbole): Rendite "
              f"{bh_summary['total_return_pct']:.2f}%  Max-DD {bh_summary['max_drawdown_pct']:.2f}%  "
              f"Calmar {bh_summary['calmar_ratio']}")
    print(f"Schlechtester Einzel-Bot (Max-DD): {worst_individual_dd:.2f}%")

    # Robustheits-Illustration (Ward-Linkage) - siehe compute_robustness_check-Docstring
    print("\nBerechne Robustheits-Illustration (Ward-Linkage, NICHT als 'besseres' Ergebnis ausgewaehlt)...")
    ward_summary, ward_schedule = compute_robustness_check(bot_names, daily_returns, trade_dates, date_range, normalised)
    print(f"HRP (Ward-Linkage, Illustration): Rendite {ward_summary['total_return_pct']:.2f}%  "
          f"Max-DD {ward_summary['max_drawdown_pct']:.2f}%  Calmar {ward_summary['calmar_ratio']}")

    # Gewichts-Stabilitaet ueber die Quartale (Parameter-Instabilitaets-Hinweis)
    weight_rows = [{"quarter_start": e["quarter_start"], "quarter_end": e["quarter_end"],
                     "bootstrap": e["bootstrap"], "excluded": e["excluded"], **e["weights"]}
                    for e in schedule]
    weights_df = pd.DataFrame(weight_rows).set_index("quarter_start")
    weight_cols = bot_names
    quarter_to_quarter_swing = weights_df[weight_cols].diff().abs().sum(axis=1).dropna()
    max_swing = round(float(quarter_to_quarter_swing.max()), 4) if len(quarter_to_quarter_swing) else None
    mean_swing = round(float(quarter_to_quarter_swing.mean()), 4) if len(quarter_to_quarter_swing) else None
    print(f"\nGewichts-Stabilitaet: durchschnittliche Quartal-zu-Quartal-Verschiebung "
          f"(Summe |Delta Gewicht| ueber alle Bots) = {mean_swing}, Maximum = {max_swing}")

    os.makedirs(RESULTS_DIR, exist_ok=True)

    curves_out = pd.DataFrame({
        "hrp_walk_forward": hrp_curve,
        "baseline_equal_weight": baseline_curve,
    })
    if not bh_curve.empty:
        curves_out["buy_and_hold"] = bh_curve.reindex(curves_out.index)
    curves_out.to_csv(os.path.join(RESULTS_DIR, "combined_curves.csv"))

    weights_df.to_csv(os.path.join(RESULTS_DIR, "quarterly_weights.csv"))

    result = {
        "bots": bot_names,
        "common_window": {"start": str(common_start.date()), "end": str(common_end.date())},
        "rebalance_freq": REBALANCE_FREQ,
        "linkage_method": LINKAGE_METHOD,
        "hrp_walk_forward": hrp_summary,
        "baseline_equal_weight": baseline_summary,
        "buy_and_hold": bh_summary,
        "buy_and_hold_num_symbols": bh_num_symbols,
        "worst_individual_bot_max_drawdown_pct": worst_individual_dd,
        "robustness_check_ward_linkage": ward_summary,
        "weight_stability": {
            "mean_quarter_to_quarter_swing": mean_swing,
            "max_quarter_to_quarter_swing": max_swing,
            "num_quarters": len(schedule),
            "num_bootstrap_quarters": sum(1 for e in schedule if e["bootstrap"]),
            "quarters_with_excluded_bots": sum(1 for e in schedule if e["excluded"]),
        },
    }
    with open(os.path.join(RESULTS_DIR, "hrp_summary.json"), "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"\nErgebnisse gespeichert unter: {RESULTS_DIR}/")


if __name__ == "__main__":
    main()

"""
RSI-2: Weitere Hebel gegen den Kapital-Flaschenhals (feinere Allokation,
kuerzerer Zeit-Exit, Kombination)
================================================================================
Folgeexperiment zum Signal-Qualitaets-Test (experiment_signal_quality_and_
priority.py), der bestaetigt hat: Kapitalmanagement ist der dominante
Flaschenhals, nicht Signalqualitaet. Testet hier zwei konkrete Hebel dagegen,
ueber den bisher besten Stand (5% Allokation, Limit 20) hinaus:

AUFGABE 1: Feinere Allokations-Abstufung (2% / 1,5% / 1%), Limit jeweils
unbegrenzt (bei so kleiner Allokation deckelt die Kapitallogik selbst schon,
siehe experiment_position_size_limit.py - ein explizites Limit waere ab
einem gewissen Punkt wirkungslos).

AUFGABE 2: Zeit-Exit verkuerzen (7 / 5 Handelstage statt 10), bei 5%
Allokation / Limit 20 - schnelleres Freiwerden von Kapital als Alternative
zur kleineren Positionsgroesse.

AUFGABE 3: Kombination aus dem jeweils besten Hebel aus 1 und 2, FALLS beide
einzeln eine Verbesserung gegenueber der Baseline zeigen.

Fuer jede Konfiguration: Gesamtzeitraum, Out-of-Sample UND die 2022-
Stress-Periode (Rendite + Max Drawdown), damit der Diversifikations-Trade-off
durchgehend im Blick bleibt (siehe PROTOTYPE_FINDINGS.md Abschnitt 9c).

NICHTS live geschaltet, keine live_params.py - reine Analyse.
"""

import os
import pandas as pd

from multi_symbol_optimise import load_all_symbol_data
from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO
from equity_simulation import collect_all_trades, simulate_portfolio, calculate_max_drawdown, STARTING_CAPITAL
from pipeline_report import collect_trades_windowed
from strategy_paths import get_strategy_paths

_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]

RSI_THRESHOLD = 5.0
STOP_LOSS_PCT = None
BASELINE_ALLOCATION_PCT = 0.05
BASELINE_LIMIT = 20
BASELINE_MAX_HOLD_DAYS = 10

STRESS_START = "2022-01-01"
STRESS_END = "2022-12-31"


def stress_period_metrics(equity_curve: pd.DataFrame, starting_capital: float) -> dict:
    if equity_curve.empty:
        return {"stress_2022_return_pct": None, "stress_2022_max_dd_pct": None}
    curve = equity_curve.copy()
    curve["time"] = pd.to_datetime(curve["time"]).dt.normalize()
    daily = curve.groupby("time")["capital_after"].last()
    full_range = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
    daily = daily.reindex(full_range).ffill()
    if pd.isna(daily.iloc[0]):
        daily.iloc[0] = starting_capital
    window = daily[(daily.index >= STRESS_START) & (daily.index <= STRESS_END)]
    if window.empty:
        return {"stress_2022_return_pct": None, "stress_2022_max_dd_pct": None}
    start_cap, end_cap = window.iloc[0], window.iloc[-1]
    running_max = window.cummax()
    dd = ((window - running_max) / running_max * 100).min()
    rendite = round((end_cap / start_cap - 1) * 100, 2)
    return {"stress_2022_return_pct": rendite, "stress_2022_max_dd_pct": round(dd, 2)}


def evaluate(trades: pd.DataFrame, allocation_pct: float, limit, max_hold_days: int, label: str) -> dict:
    result = simulate_portfolio(trades, STARTING_CAPITAL, allocation_pct, limit)
    total_return_pct = round((result["final_capital"] / STARTING_CAPITAL - 1) * 100, 2)
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    stress = stress_period_metrics(result["equity_curve"], STARTING_CAPITAL)
    return {
        "konfiguration": label, "allocation_pct": allocation_pct,
        "limit": limit if limit is not None else "unbegrenzt", "max_hold_days": max_hold_days,
        "final_capital": result["final_capital"], "total_return_pct": total_return_pct,
        "trades_ausgefuehrt": result["num_executed"], "trades_uebersprungen": result["num_skipped"],
        "max_drawdown_pct": max_dd, **stress,
    }


if __name__ == "__main__":
    all_data = load_all_symbol_data()
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)

    full_rows, oos_rows = [], []

    # --- Baseline: 5% Allokation, Limit 20, Zeit-Exit 10 Tage (bisher bester Stand) ---
    print("Baseline und Aufgabe 1 (feinere Allokation) - Trades einmalig fuer Zeit-Exit=10 sammeln...")
    trades_full_10 = collect_all_trades(all_data, RSI_THRESHOLD, STOP_LOSS_PCT, max_hold_days=10)
    trades_oos_10 = collect_trades_windowed(test_data, RSI_THRESHOLD, STOP_LOSS_PCT, max_hold_days=10)

    baseline_label = "Baseline: 5% Allok., Limit 20, Zeit-Exit 10T"
    full_rows.append(evaluate(trades_full_10, BASELINE_ALLOCATION_PCT, BASELINE_LIMIT, 10, baseline_label))
    oos_rows.append(evaluate(trades_oos_10, BASELINE_ALLOCATION_PCT, BASELINE_LIMIT, 10, baseline_label))

    # --- AUFGABE 1: feinere Allokations-Abstufung, Limit unbegrenzt ---
    task1_configs = [0.02, 0.015, 0.01]
    for allocation_pct in task1_configs:
        label = f"{allocation_pct*100:.1f}% Allok., Limit unbegrenzt, Zeit-Exit 10T"
        full_rows.append(evaluate(trades_full_10, allocation_pct, None, 10, label))
        oos_rows.append(evaluate(trades_oos_10, allocation_pct, None, 10, label))

    # --- AUFGABE 2: Zeit-Exit verkuerzen, 5% Allokation / Limit 20 ---
    task2_configs = [7, 5]
    task2_trades = {10: (trades_full_10, trades_oos_10)}
    for max_hold_days in task2_configs:
        print(f"Aufgabe 2: Trades fuer Zeit-Exit={max_hold_days} Tage sammeln...")
        trades_full_x = collect_all_trades(all_data, RSI_THRESHOLD, STOP_LOSS_PCT, max_hold_days=max_hold_days)
        trades_oos_x = collect_trades_windowed(test_data, RSI_THRESHOLD, STOP_LOSS_PCT, max_hold_days=max_hold_days)
        task2_trades[max_hold_days] = (trades_full_x, trades_oos_x)
        label = f"5% Allok., Limit 20, Zeit-Exit {max_hold_days}T"
        full_rows.append(evaluate(trades_full_x, BASELINE_ALLOCATION_PCT, BASELINE_LIMIT, max_hold_days, label))
        oos_rows.append(evaluate(trades_oos_x, BASELINE_ALLOCATION_PCT, BASELINE_LIMIT, max_hold_days, label))

    # --- AUFGABE 3: Kombination, falls beide Hebel je fuer sich verbessern ---
    baseline_return = full_rows[0]["total_return_pct"]
    task1_rows = full_rows[1:1 + len(task1_configs)]
    task2_rows = full_rows[1 + len(task1_configs):1 + len(task1_configs) + len(task2_configs)]

    best_task1 = max(task1_rows, key=lambda r: r["total_return_pct"])
    best_task2 = max(task2_rows, key=lambda r: r["total_return_pct"])

    task1_improves = best_task1["total_return_pct"] > baseline_return
    task2_improves = best_task2["total_return_pct"] > baseline_return

    print(f"\nAufgabe 1 beste Variante ({best_task1['konfiguration']}): "
          f"{best_task1['total_return_pct']}% vs. Baseline {baseline_return}% "
          f"-> verbessert: {task1_improves}")
    print(f"Aufgabe 2 beste Variante ({best_task2['konfiguration']}): "
          f"{best_task2['total_return_pct']}% vs. Baseline {baseline_return}% "
          f"-> verbessert: {task2_improves}")

    if task1_improves and task2_improves:
        combo_allocation = best_task1["allocation_pct"]
        combo_max_hold_days = best_task2["max_hold_days"]
        print(f"\nAufgabe 3: Kombination {combo_allocation*100:.1f}% Allokation + "
              f"Zeit-Exit {combo_max_hold_days}T wird getestet...")
        if combo_max_hold_days in task2_trades:
            trades_full_combo, trades_oos_combo = task2_trades[combo_max_hold_days]
        else:
            trades_full_combo = collect_all_trades(all_data, RSI_THRESHOLD, STOP_LOSS_PCT,
                                                     max_hold_days=combo_max_hold_days)
            trades_oos_combo = collect_trades_windowed(test_data, RSI_THRESHOLD, STOP_LOSS_PCT,
                                                         max_hold_days=combo_max_hold_days)
        label = f"KOMBINATION: {combo_allocation*100:.1f}% Allok., Limit unbegrenzt, Zeit-Exit {combo_max_hold_days}T"
        full_rows.append(evaluate(trades_full_combo, combo_allocation, None, combo_max_hold_days, label))
        oos_rows.append(evaluate(trades_oos_combo, combo_allocation, None, combo_max_hold_days, label))
    else:
        print("\nAufgabe 3 nicht getestet - mindestens ein Hebel zeigt fuer sich keine Verbesserung "
              "gegenueber der Baseline.")

    full_df = pd.DataFrame(full_rows)
    oos_df = pd.DataFrame(oos_rows)

    print("\n" + "=" * 110)
    print("GESAMTZEITRAUM")
    print("=" * 110)
    print(full_df.to_string(index=False))

    print("\n" + "=" * 110)
    print("OUT-OF-SAMPLE")
    print("=" * 110)
    print(oos_df.to_string(index=False))

    # --- Zusammenfassende Tabelle, sortiert nach OOS-Rendite ---
    # WICHTIG: Die 2022-Stress-Periode liegt IM In-Sample-Teil des Walk-Forward-
    # Splits (OOS beginnt erst ~2023-09) - die 2022-Kennzahlen kommen daher aus
    # full_df, nicht aus oos_df (dort waeren sie durchgehend None).
    summary = oos_df[["konfiguration", "total_return_pct", "max_drawdown_pct"]].copy()
    summary.columns = ["Konfiguration", "OOS Rendite %", "OOS Max DD %"]
    full_return_lookup = full_df.set_index("konfiguration")["total_return_pct"]
    full_dd_lookup = full_df.set_index("konfiguration")["max_drawdown_pct"]
    stress_return_lookup = full_df.set_index("konfiguration")["stress_2022_return_pct"]
    stress_dd_lookup = full_df.set_index("konfiguration")["stress_2022_max_dd_pct"]
    summary.insert(1, "Gesamtzeitraum Rendite %", summary["Konfiguration"].map(full_return_lookup))
    summary.insert(2, "Gesamtzeitraum Max DD %", summary["Konfiguration"].map(full_dd_lookup))
    summary["2022 Rendite %"] = summary["Konfiguration"].map(stress_return_lookup)
    summary["2022 Max DD %"] = summary["Konfiguration"].map(stress_dd_lookup)
    summary = summary.sort_values("OOS Rendite %", ascending=False).reset_index(drop=True)

    print("\n" + "=" * 110)
    print("ZUSAMMENFASSUNG - sortiert nach Out-of-Sample-Rendite")
    print("=" * 110)
    print(summary.to_string(index=False))

    os.makedirs(RESULTS_DIR, exist_ok=True)
    full_df.to_csv(os.path.join(RESULTS_DIR, "experiment_capital_bottleneck_v2_full.csv"), index=False)
    oos_df.to_csv(os.path.join(RESULTS_DIR, "experiment_capital_bottleneck_v2_oos.csv"), index=False)
    summary.to_csv(os.path.join(RESULTS_DIR, "experiment_capital_bottleneck_v2_summary.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_capital_bottleneck_v2_{{full,oos,summary}}.csv")

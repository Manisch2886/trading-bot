"""
RSI-2: Signal-Qualitaets-Test + Signal-Priorisierung bei Kapital-Konkurrenz
================================================================================
Zwei gezielte Diagnosen des Kernproblems aus PROTOTYPE_FINDINGS.md (bis zu
65% der gefundenen Trades werden bei Limit 8 uebersprungen), statt weiterer
Parameterwerte:

AUFGABE 1 - Signal-Qualitaets-Test (Projekt-Methodik, siehe
elliott_wave_stocks/signal_quality_test.py als Vorbild-Idee, hier neu fuer
RSI-2 angewendet): Trennt Timing-/Signal-Nutzen von Kapitalmanagement-Nutzen.
Vergleicht (a) den Ø PnL/Trade der TATSAECHLICH mit Kapital versorgten Trades
(reales Limit 8, 10% Allokation - der urspruengliche validierte Startpunkt)
gegen (b) den Ø PnL/Trade ALLER gefundenen Signale (unabhaengig davon, ob sie
Kapital bekommen haetten) UND gegen (c) eine hypothetische Kapital-KEIN-Limit-
Simulation (jedes Signal bekommt sofort 10% des aktuellen Kapitals, keine
Pruefung auf freies Kapital/Positionslimit - REIN ZUR DIAGNOSE, das ist
unrealistisches Leverage und KEIN Vorschlag fuer echten Live-Betrieb).

AUFGABE 2 - Signal-Priorisierung bei Kapital-Konkurrenz: Bisher entscheidet
bei mehreren gleichzeitigen Signalen am selben Tag die Reihenfolge in den
Events (de facto chronologisch/alphabetisch nach Symbol), welches Signal die
knappen Kapitalplaetze bekommt. Testet stattdessen: bei Gleichstand im
Zeitpunkt wird das Signal mit dem NIEDRIGSTEN RSI(2)-Wert (staerkstes
Ueberverkauft-Signal) bevorzugt. Vergleich bei 5% Allokation, Limit 20 (die
zuletzt validierte, beste gefundene Kombination aus
experiment_position_size_limit.py).

NICHTS wird live geschaltet, keine live_params.py angelegt - reine Analyse.
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
STOP_LOSS_PCT = None  # "kein Stop" - beste validierte Kombination

# Aufgabe 1: urspruenglicher validierter Startpunkt (siehe PROTOTYPE_FINDINGS.md)
BASELINE_ALLOCATION_PCT = 0.10
BASELINE_LIMIT = 8

# Aufgabe 2: zuletzt validierte, beste Kombination (experiment_position_size_limit.py)
BEST_ALLOCATION_PCT = 0.05
BEST_LIMIT = 20


def simulate_portfolio_unlimited(trades: pd.DataFrame, starting_capital: float, allocation_pct: float) -> dict:
    """Wie simulate_portfolio, aber OHNE Kapital-/Positionslimit-Pruefung -
    jedes gefundene Signal wird sofort ausgefuehrt. REIN DIAGNOSTISCH,
    entspricht unrealistischem Leverage (Summe gleichzeitiger Allokationen
    kann 100% des Kapitals klar uebersteigen) - kein Live-Vorschlag."""
    events = []
    for idx, trade in trades.iterrows():
        events.append((trade["entry_time"], "entry", idx))
        events.append((trade["exit_time"], "exit", idx))
    events.sort(key=lambda e: (e[0], e[1] != "exit"))

    capital = starting_capital
    open_positions = {}
    equity_curve = []

    for time, event_type, idx in events:
        trade = trades.loc[idx]
        if event_type == "entry":
            allocation = capital * allocation_pct
            open_positions[idx] = allocation
        elif event_type == "exit":
            if idx not in open_positions:
                continue
            allocation = open_positions.pop(idx)
            pnl_pct = trade["pnl_pct"]
            result_value = allocation * (1 + pnl_pct / 100)
            capital += (result_value - allocation)
            equity_curve.append({
                "time": time, "symbol": trade["symbol"], "pnl_pct": pnl_pct,
                "allocation": round(allocation, 2), "capital_after": round(capital, 2),
            })

    equity_df = pd.DataFrame(equity_curve)
    return {
        "final_capital": round(capital, 2),
        "num_executed": len(trades),
        "num_skipped": 0,
        "equity_curve": equity_df,
    }


def simulate_portfolio_priority(trades: pd.DataFrame, starting_capital: float, allocation_pct: float,
                                 max_concurrent_positions, priority_col: str) -> dict:
    """Wie simulate_portfolio, aber bei mehreren Entry-Events zum EXAKT
    gleichen Zeitpunkt wird zuerst das Signal mit dem niedrigsten Wert in
    priority_col verarbeitet (z.B. rsi_at_entry - niedrigster RSI zuerst =
    staerkstes Ueberverkauft-Signal bekommt die knappen Kapitalplaetze
    zuerst). Exits weiterhin immer vor Entries am selben Tag."""
    events = []
    for idx, trade in trades.iterrows():
        events.append((trade["entry_time"], "entry", idx, trade[priority_col]))
        events.append((trade["exit_time"], "exit", idx, 0))
    events.sort(key=lambda e: (e[0], e[1] != "exit", e[3] if e[1] == "entry" else 0))

    capital = starting_capital
    open_positions = {}
    skipped_trades = []
    executed_trades = []
    equity_curve = []

    for time, event_type, idx, _ in events:
        trade = trades.loc[idx]
        if event_type == "entry":
            if max_concurrent_positions is not None and len(open_positions) >= max_concurrent_positions:
                skipped_trades.append(idx)
                continue
            bound_capital = sum(open_positions.values())
            free_capital = capital - bound_capital
            allocation = capital * allocation_pct
            if allocation > free_capital:
                skipped_trades.append(idx)
                continue
            open_positions[idx] = allocation
            executed_trades.append(idx)
        elif event_type == "exit":
            if idx not in open_positions:
                continue
            allocation = open_positions.pop(idx)
            pnl_pct = trade["pnl_pct"]
            result_value = allocation * (1 + pnl_pct / 100)
            capital += (result_value - allocation)
            equity_curve.append({
                "time": time, "symbol": trade["symbol"], "pnl_pct": pnl_pct,
                "allocation": round(allocation, 2), "capital_after": round(capital, 2),
            })

    equity_df = pd.DataFrame(equity_curve)
    return {
        "final_capital": round(capital, 2),
        "num_executed": len(executed_trades),
        "num_skipped": len(skipped_trades),
        "equity_curve": equity_df,
    }


def trade_stats(pnl_series: pd.Series) -> dict:
    if pnl_series.empty:
        return {"n": 0, "win_rate_pct": None, "avg_pnl_pct": None}
    return {
        "n": len(pnl_series),
        "win_rate_pct": round((pnl_series > 0).mean() * 100, 1),
        "avg_pnl_pct": round(pnl_series.mean(), 3),
    }


def portfolio_stats(result: dict, starting_capital: float) -> dict:
    total_return_pct = round((result["final_capital"] / starting_capital - 1) * 100, 2)
    max_dd = calculate_max_drawdown(result["equity_curve"], starting_capital)
    return {
        "final_capital": result["final_capital"], "total_return_pct": total_return_pct,
        "trades_ausgefuehrt": result["num_executed"], "trades_uebersprungen": result["num_skipped"],
        "max_drawdown_pct": max_dd,
    }


def task1_signal_quality(all_trades: pd.DataFrame, label: str):
    print(f"\n{'='*90}\nAUFGABE 1 - SIGNAL-QUALITAETS-TEST ({label})\n{'='*90}")

    # (a) tatsaechlich mit Kapital versorgte Trades (Limit 8, 10% Allokation)
    result_real = simulate_portfolio(all_trades, STARTING_CAPITAL, BASELINE_ALLOCATION_PCT, BASELINE_LIMIT)
    executed_pnls = result_real["equity_curve"]["pnl_pct"] if not result_real["equity_curve"].empty else pd.Series(dtype=float)
    stats_executed = trade_stats(executed_pnls)

    # (b) ALLE gefundenen Signale, unabhaengig von Kapitalverfuegbarkeit
    stats_all_found = trade_stats(all_trades["pnl_pct"])

    # (c) hypothetische Kapital-unbegrenzt-Simulation (nur zur Diagnose)
    result_unlimited = simulate_portfolio_unlimited(all_trades, STARTING_CAPITAL, BASELINE_ALLOCATION_PCT)

    print(f"\n(a) Tatsaechlich ausgefuehrte Trades (Limit {BASELINE_LIMIT}, "
          f"{BASELINE_ALLOCATION_PCT*100:.0f}% Allokation):")
    print(f"    n={stats_executed['n']}  Win Rate={stats_executed['win_rate_pct']}%  "
          f"Ø PnL/Trade={stats_executed['avg_pnl_pct']}%")
    print(f"    Portfolio: {portfolio_stats(result_real, STARTING_CAPITAL)}")

    print(f"\n(b) ALLE gefundenen Signale (unabhaengig von Kapitalverfuegbarkeit):")
    print(f"    n={stats_all_found['n']}  Win Rate={stats_all_found['win_rate_pct']}%  "
          f"Ø PnL/Trade={stats_all_found['avg_pnl_pct']}%")

    print(f"\n(c) Hypothetisch: JEDES Signal bekommt sofort Kapital, kein Limit "
          f"(nur Diagnose, unrealistisches Leverage):")
    print(f"    Portfolio: {portfolio_stats(result_unlimited, STARTING_CAPITAL)}")

    diff = None
    if stats_executed["avg_pnl_pct"] is not None and stats_all_found["avg_pnl_pct"] is not None:
        diff = round(stats_executed["avg_pnl_pct"] - stats_all_found["avg_pnl_pct"], 3)
        print(f"\n    Differenz Ø PnL (ausgefuehrt - alle gefunden): {diff:+.3f} Prozentpunkte")

    return {
        "label": label, "executed": stats_executed, "all_found": stats_all_found,
        "unlimited_portfolio": portfolio_stats(result_unlimited, STARTING_CAPITAL),
        "real_portfolio": portfolio_stats(result_real, STARTING_CAPITAL), "diff_pp": diff,
    }


def task2_priority(all_trades: pd.DataFrame, label: str):
    print(f"\n{'='*90}\nAUFGABE 2 - SIGNAL-PRIORISIERUNG ({label})\n{'='*90}")
    print(f"Feste Rahmenbedingungen: {BEST_ALLOCATION_PCT*100:.0f}% Allokation, Limit {BEST_LIMIT}\n")

    result_chrono = simulate_portfolio(all_trades, STARTING_CAPITAL, BEST_ALLOCATION_PCT, BEST_LIMIT)
    result_priority = simulate_portfolio_priority(all_trades, STARTING_CAPITAL, BEST_ALLOCATION_PCT,
                                                   BEST_LIMIT, priority_col="rsi_at_entry")

    stats_chrono = portfolio_stats(result_chrono, STARTING_CAPITAL)
    stats_priority = portfolio_stats(result_priority, STARTING_CAPITAL)

    df = pd.DataFrame([
        {"variante": "Aktuell (chronologisch/alphabetisch)", **stats_chrono},
        {"variante": "RSI-priorisiert (niedrigster RSI zuerst)", **stats_priority},
    ])
    print(df.to_string(index=False))
    return df


if __name__ == "__main__":
    print(f"Feste Parameter: RSI-Schwelle {RSI_THRESHOLD} | Stop-Loss: kein Stop\n")

    all_data = load_all_symbol_data()
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)

    trades_full = collect_all_trades(all_data, RSI_THRESHOLD, STOP_LOSS_PCT)
    trades_oos = collect_trades_windowed(test_data, RSI_THRESHOLD, STOP_LOSS_PCT)

    print(f"Gesamtzeitraum: {len(trades_full)} Signale gefunden.")
    print(f"Out-of-Sample: {len(trades_oos)} Signale gefunden.")

    t1_full = task1_signal_quality(trades_full, "Gesamtzeitraum")
    t1_oos = task1_signal_quality(trades_oos, "Out-of-Sample")

    t2_full = task2_priority(trades_full, "Gesamtzeitraum")
    t2_oos = task2_priority(trades_oos, "Out-of-Sample")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    t2_full.to_csv(os.path.join(RESULTS_DIR, "experiment_signal_priority_full.csv"), index=False)
    t2_oos.to_csv(os.path.join(RESULTS_DIR, "experiment_signal_priority_oos.csv"), index=False)
    print(f"\nGespeichert unter: {RESULTS_DIR}/experiment_signal_priority_full.csv")
    print(f"Gespeichert unter: {RESULTS_DIR}/experiment_signal_priority_oos.csv")

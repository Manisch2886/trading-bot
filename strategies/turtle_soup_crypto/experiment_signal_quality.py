"""
Turtle Soup (Krypto): Signal-Qualitaets-Test (analog zu RSI-2/Volatility Breakout)
================================================================================
Analog zu turtle_soup_stocks/experiment_signal_quality.py - siehe dortigen
Docstring fuer die vollstaendige Methodik-Begruendung. War in der
Prototyp-Phase noch nicht Fokus (Krypto zeigte nur eine moderate 11,6%
Skip-Rate bei Limit 8/10% Allokation) - wird hier zur Vollstaendigkeit
neben Aktien mitgeliefert.

NICHTS wird live geschaltet, keine live_params.py - reine Analyse.
"""

import pandas as pd

from multi_symbol_optimise import load_all_symbol_data
from multi_symbol_walk_forward import split_all_symbols, TRAIN_SPLIT_RATIO
from equity_simulation import collect_all_trades, simulate_portfolio, calculate_max_drawdown, \
    STARTING_CAPITAL, DONCHIAN_PERIOD, STOP_MODE
from pipeline_report import collect_trades_windowed

BASELINE_ALLOCATION_PCT = 0.10
BASELINE_LIMIT = 8


def simulate_portfolio_unlimited(trades: pd.DataFrame, starting_capital: float, allocation_pct: float) -> dict:
    """Wie simulate_portfolio, aber OHNE Kapital-/Positionslimit-Pruefung -
    jedes gefundene Signal wird sofort ausgefuehrt. REIN DIAGNOSTISCH,
    entspricht unrealistischem Leverage - kein Live-Vorschlag."""
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


def signal_quality_test(all_trades: pd.DataFrame, label: str):
    print(f"\n{'='*90}\nSIGNAL-QUALITAETS-TEST ({label})\n{'='*90}")

    result_real = simulate_portfolio(all_trades, STARTING_CAPITAL, BASELINE_ALLOCATION_PCT, BASELINE_LIMIT)
    executed_pnls = result_real["equity_curve"]["pnl_pct"] if not result_real["equity_curve"].empty else pd.Series(dtype=float)
    stats_executed = trade_stats(executed_pnls)

    stats_all_found = trade_stats(all_trades["pnl_pct"])

    result_unlimited = simulate_portfolio_unlimited(all_trades, STARTING_CAPITAL, BASELINE_ALLOCATION_PCT)

    print(f"\n(a) Tatsaechlich ausgefuehrte Trades (Limit {BASELINE_LIMIT}, "
          f"{BASELINE_ALLOCATION_PCT*100:.0f}% Allokation, Donchian {DONCHIAN_PERIOD}, "
          f"Stop {'kein Stop' if STOP_MODE is None else STOP_MODE}):")
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


if __name__ == "__main__":
    print(f"Feste Parameter: Donchian {DONCHIAN_PERIOD}, Stop "
          f"{'kein Stop' if STOP_MODE is None else STOP_MODE} (validierte Basiskonfiguration)\n")

    all_data = load_all_symbol_data()
    train_data, test_data = split_all_symbols(all_data, TRAIN_SPLIT_RATIO)

    trades_full = collect_all_trades(all_data, DONCHIAN_PERIOD, STOP_MODE)
    trades_oos = collect_trades_windowed(test_data, DONCHIAN_PERIOD, STOP_MODE)

    print(f"Gesamtzeitraum: {len(trades_full)} Signale gefunden.")
    print(f"Out-of-Sample: {len(trades_oos)} Signale gefunden.")

    signal_quality_test(trades_full, "Gesamtzeitraum")
    signal_quality_test(trades_oos, "Out-of-Sample")

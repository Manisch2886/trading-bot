"""
Reihenfolge-Empfindlichkeit - Analyse fuer EINEN Bot
=========================================================
Ruft die UNVERAENDERTEN Original-Skripte des jeweiligen Bots auf
(`equity_simulation.py`: `load_all_symbol_data`, `collect_all_trades`,
`simulate_portfolio`, `calculate_max_drawdown`) und permutiert
ausschliesslich die Verarbeitungsreihenfolge bei gleichzeitigen Signalen.

An den Original-Dateien wird NICHTS geaendert. Der Trade-Satz, die
Parameter und die Simulationslogik stammen vollstaendig aus dem Bot selbst.

Ein eigener Prozess je Bot, weil alle 9 Bots gleichnamige, aber inhaltlich
verschiedene Module haben - im selben Prozess wuerde sys.modules-Caching
fuer den zweiten Bot die falsche Version liefern.

Nutzung:
    python3 run_one_bot.py <bot_name>
"""

import json
import os
import sys
import types

import numpy as np
import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
sys.path.insert(0, _DIR)

import order_core as oc

BOT = sys.argv[1]
sys.path.insert(0, os.path.join(_REPO_ROOT, "strategies", BOT))
sys.path.insert(0, os.path.join(_REPO_ROOT, "shared"))

RESULTS_DIR = os.path.join(_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

N_PERMUTATIONS = 500     # identisch zu research/trailing_stops und research/vbc_deepdive
SEED = 20260907
N_VERIFY = 25            # Permutationen, die zusaetzlich mit der BOT-EIGENEN
                          # simulate_portfolio() nachgerechnet werden

# Zugangsdaten-behaftete bzw. nicht installierte Importe stubben, BEVOR ein
# Bot-Modul geladen wird. shared/fetch_binance_data.py enthaelt laut CLAUDE.md
# Zugangsdaten und ist gitignored; yfinance und python-binance sind in dieser
# Sandbox nicht installiert. Beide werden hier nie aufgerufen - es werden
# ausschliesslich die bereits vorhandenen lokalen CSVs gelesen.
_fake_fetch = types.ModuleType("fetch_binance_data")
_fake_fetch.fetch_historical_data = lambda *a, **kw: pd.DataFrame()
sys.modules.setdefault("fetch_binance_data", _fake_fetch)

_fake_binance = types.ModuleType("binance")
_fake_client = types.ModuleType("binance.client")


class _FakeClient:
    KLINE_INTERVAL_1HOUR = "1h"
    KLINE_INTERVAL_4HOUR = "4h"
    KLINE_INTERVAL_1DAY = "1d"


_fake_client.Client = _FakeClient
_fake_binance.client = _fake_client
sys.modules.setdefault("binance", _fake_binance)
sys.modules.setdefault("binance.client", _fake_client)

_fake_yf = types.ModuleType("yfinance")
_fake_yf.download = lambda *a, **kw: pd.DataFrame()
_fake_yf.Ticker = lambda *a, **kw: None
sys.modules.setdefault("yfinance", _fake_yf)


def load_original_trades(es):
    """
    Ruft `collect_all_trades()` des Bots mit GENAU den Parametern auf, die
    dessen eigenes `equity_simulation.py` im __main__-Block verwendet -
    also mit den Modul-Konstanten dieser Datei, nicht mit live_params.py.

    Das ist bewusst so: die Frage lautet, ob die URSPRUENGLICHEN Backtests
    betroffen sind, und der urspruengliche Backtest ist das, was
    `python3 equity_simulation.py` ausgibt. Wo live_params.py inzwischen
    abweicht, wird das im Bericht gesondert ausgewiesen.
    """
    all_data = es.load_all_symbol_data()

    if BOT == "elliott_wave":
        trades = es.collect_all_trades(all_data, es.DEVIATION_PCT, es.STOP_LOSS_PCT,
                                        es.TAKE_PROFIT_FIB)
    elif BOT == "elliott_wave_stocks":
        trades = es.collect_all_trades(all_data, es.DEVIATION_PCT, es.STOP_LOSS_PCT,
                                        es.TAKE_PROFIT_FIB, es.USE_TAKE_PROFIT)
    elif BOT == "t3_supertrend":
        trades = es.collect_all_trades(all_data, es.T3_FAST, es.T3_SLOW,
                                        es.ADX_THRESHOLD, es.STOP_LOSS_PCT)
    elif BOT == "rsi2_crypto":
        trades = es.collect_all_trades(all_data, es.RSI_THRESHOLD, es.SMA_TREND_PERIOD,
                                        es.STOP_LOSS_PCT)
    elif BOT == "rsi2_mean_reversion":
        trades = es.collect_all_trades(all_data, es.RSI_THRESHOLD, es.STOP_LOSS_PCT)
    elif BOT in ("turtle_soup_crypto", "turtle_soup_stocks"):
        trades = es.collect_all_trades(all_data, es.DONCHIAN_PERIOD, es.STOP_MODE)
    elif BOT in ("volatility_breakout", "volatility_breakout_crypto"):
        trades = es.collect_all_trades(all_data, es.STOP_LOSS_PCT,
                                        getattr(es, "MAX_HOLD_DAYS", None))
    else:
        raise ValueError(f"Unbekannter Bot: {BOT}")
    return trades


def bot_simulate(es, trades, allocation_pct, max_concurrent):
    """Ruft die BOT-EIGENE simulate_portfolio() auf. elliott_wave ist der
    einzige Bot, dessen Fassung KEIN Positionslimit kennt (die Funktion hat
    dort schlicht keinen entsprechenden Parameter) - das ist kein Versehen
    dieser Untersuchung, sondern der tatsaechliche Stand jenes Bots."""
    if max_concurrent is _NO_LIMIT_PARAM:
        result = es.simulate_portfolio(trades, es.STARTING_CAPITAL, allocation_pct)
    else:
        result = es.simulate_portfolio(trades, es.STARTING_CAPITAL, allocation_pct, max_concurrent)
    total_return = (result["final_capital"] / es.STARTING_CAPITAL - 1) * 100
    max_dd = es.calculate_max_drawdown(result["equity_curve"], es.STARTING_CAPITAL)
    return {"total_return_pct": round(total_return, 2), "max_drawdown_pct": max_dd,
            "num_executed": result["num_executed"], "num_skipped": result["num_skipped"]}


_NO_LIMIT_PARAM = object()   # Marker: dieser Bot hat gar keinen Limit-Parameter


def main():
    import equity_simulation as es

    trades = load_original_trades(es)
    if trades.empty:
        json.dump({"bot": BOT, "error": "keine Trades"},
                  open(os.path.join(RESULTS_DIR, f"{BOT}.json"), "w"), indent=2)
        print(f"{BOT}: keine Trades - Abbruch.")
        return

    allocation_pct = es.ALLOCATION_PCT
    has_limit = "max_concurrent_positions" in es.simulate_portfolio.__code__.co_varnames
    max_concurrent = getattr(es, "MAX_CONCURRENT_POSITIONS", None) if has_limit else _NO_LIMIT_PARAM
    effective_limit = None if max_concurrent is _NO_LIMIT_PARAM else max_concurrent

    # --- Ausgangswert: die Original-Reihenfolge, wie sie collect_all_trades liefert
    baseline = bot_simulate(es, trades, allocation_pct, max_concurrent)
    baseline["calmar_ratio"] = oc.calmar(baseline["total_return_pct"], baseline["max_drawdown_pct"])

    # --- Aequivalenz-Nachweis Schnellpfad <-> bot-eigene Funktion, auf ECHTEN Daten
    rng_verify = np.random.default_rng(SEED)
    mismatches = []
    for _ in range(N_VERIFY):
        candidate = oc.permuted(trades, rng_verify)
        theirs = bot_simulate(es, candidate, allocation_pct, max_concurrent)
        entry_ns, exit_ns, pnl = oc.as_arrays(candidate)
        mine = oc.simulate_fast(entry_ns, exit_ns, pnl, es.STARTING_CAPITAL,
                                 allocation_pct, effective_limit)
        if (abs(theirs["total_return_pct"] - round(mine["total_return_pct"], 2)) > 1e-9
                or abs(theirs["max_drawdown_pct"] - mine["max_drawdown_pct"]) > 1e-9
                or theirs["num_executed"] != int(mine["executed"].sum())):
            mismatches.append({"theirs": theirs,
                               "mine": {"total_return_pct": round(mine["total_return_pct"], 2),
                                         "max_drawdown_pct": mine["max_drawdown_pct"],
                                         "num_executed": int(mine["executed"].sum())}})

    perms = oc.run_permutations(trades, es.STARTING_CAPITAL, allocation_pct,
                                 effective_limit, N_PERMUTATIONS, SEED)

    output = {
        "bot": BOT,
        "config_source": "equity_simulation.py (Modul-Konstanten des Bots)",
        "config": {
            "starting_capital": es.STARTING_CAPITAL,
            "allocation_pct": allocation_pct,
            "max_concurrent_positions": effective_limit,
            "bot_has_position_limit_parameter": has_limit,
        },
        "timestamps": oc.timestamp_stats(trades),
        "baseline_original_order": baseline,
        "equivalence_check": {
            "n_verified_permutations": N_VERIFY,
            "mismatches": len(mismatches),
            "detail": mismatches[:3],
        },
        "permutations": oc.strip_values(perms),
        "baseline_percentile": {
            "total_return_pct": oc.percentile_of(baseline["total_return_pct"], perms["total_return_pct"]),
            "max_drawdown_pct": oc.percentile_of(baseline["max_drawdown_pct"], perms["max_drawdown_pct"]),
            "calmar_ratio": oc.percentile_of(baseline["calmar_ratio"], perms["calmar_ratio"]),
        },
    }

    with open(os.path.join(RESULTS_DIR, f"{BOT}.json"), "w") as f:
        json.dump(output, f, indent=2, default=str)

    ts = output["timestamps"]
    c = perms["calmar_ratio"]
    print(f"{BOT}: {ts['n_trades']} Trades, {ts['share_sharing_entry_timestamp_pct']}% mit geteiltem "
          f"Zeitstempel (groesste Gruppe {ts['largest_same_timestamp_group']}), "
          f"Limit {effective_limit}, Allokation {allocation_pct:.0%}")
    print(f"  Aequivalenz-Check: {len(mismatches)} Abweichungen in {N_VERIFY} Permutationen")
    print(f"  Baseline  Rendite {baseline['total_return_pct']:>10.2f}%  DD {baseline['max_drawdown_pct']:>8.2f}%  "
          f"Calmar {str(baseline['calmar_ratio']):>8}  ({baseline['num_executed']} ausgefuehrt / "
          f"{baseline['num_skipped']} uebersprungen)")
    if c:
        print(f"  Permutationen  Calmar {c['min']:>8.2f} .. {c['max']:>8.2f}  (Median {c['median']:>8.2f}), "
              f"Baseline liegt im {output['baseline_percentile']['calmar_ratio']}. Perzentil")
    print(f"  umstrittene Trades: {perms['trades_contested']} von {perms['n_trades']} "
          f"({perms['contested_share_pct']}%)  |  im Schnitt abgelehnt: "
          f"{perms['mean_skipped_capital']} kapitalbedingt, {perms['mean_skipped_position_limit']} durch Limit")


if __name__ == "__main__":
    main()

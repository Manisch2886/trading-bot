"""
Schritt 2: Wie stark verschiebt sich die Baseline mit der Live-Konfiguration?
====================================================================================
Rechnet fuer jeden abweichenden Bot dieselbe Baseline zweimal:

  "backtest"  - so, wie `python3 equity_simulation.py` heute laeuft
                (Modul-Konstanten dieser Datei)
  "live"      - mit der Konfiguration aus live_params.py

Verwendet werden ausschliesslich die UNVERAENDERTEN Funktionen des Bots
(`load_all_symbol_data`, `collect_all_trades`, `simulate_portfolio`,
`calculate_max_drawdown`). Es wird keine Datei ausserhalb von
research/sync_check/ angefasst.

Ein eigener Prozess je Bot - die 9 Bots haben gleichnamige, inhaltlich
verschiedene Module.

Nutzung:  python3 impact.py <bot_name>
"""

import json
import os
import sys
import types

import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
sys.path.insert(0, _DIR)

BOT = sys.argv[1]
sys.path.insert(0, os.path.join(_REPO_ROOT, "strategies", BOT))
sys.path.insert(0, os.path.join(_REPO_ROOT, "shared"))

RESULTS_DIR = os.path.join(_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# Stubs fuer nicht installierte bzw. zugangsdatenbehaftete Importe (siehe CLAUDE.md).
# Werden nie aufgerufen - gelesen werden ausschliesslich die lokalen CSVs in data/.
for name, module in (("fetch_binance_data", types.ModuleType("fetch_binance_data")),
                      ("yfinance", types.ModuleType("yfinance"))):
    module.fetch_historical_data = lambda *a, **kw: pd.DataFrame()
    module.download = lambda *a, **kw: pd.DataFrame()
    module.Ticker = lambda *a, **kw: None
    sys.modules.setdefault(name, module)

_binance = types.ModuleType("binance")
_client = types.ModuleType("binance.client")


class _FakeClient:
    KLINE_INTERVAL_1HOUR = "1h"
    KLINE_INTERVAL_4HOUR = "4h"
    KLINE_INTERVAL_1DAY = "1d"


_client.Client = _FakeClient
_binance.client = _client
sys.modules.setdefault("binance", _binance)
sys.modules.setdefault("binance.client", _client)


def calmar(total_return_pct, max_drawdown_pct):
    if max_drawdown_pct is None or abs(max_drawdown_pct) < 1e-12:
        return None
    return round(total_return_pct / abs(max_drawdown_pct), 2)


def evaluate(es, trades, allocation_frac, max_concurrent, supports_limit):
    """Ruft die BOT-EIGENE simulate_portfolio auf."""
    if supports_limit:
        result = es.simulate_portfolio(trades, es.STARTING_CAPITAL, allocation_frac, max_concurrent)
    else:
        result = es.simulate_portfolio(trades, es.STARTING_CAPITAL, allocation_frac)
    total_return = round((result["final_capital"] / es.STARTING_CAPITAL - 1) * 100, 2)
    max_dd = es.calculate_max_drawdown(result["equity_curve"], es.STARTING_CAPITAL)
    return {"trades_gefunden": int(len(trades)), "ausgefuehrt": result["num_executed"],
            "uebersprungen": result["num_skipped"], "rendite_pct": total_return,
            "max_drawdown_pct": max_dd, "calmar": calmar(total_return, max_dd)}


def build(es, lp, all_data, variant: str):
    """
    Erzeugt Trade-Satz und Kapitalparameter fuer eine Variante.

    Nur bei elliott_wave_stocks und volatility_breakout_crypto unterscheidet
    sich der TRADE-SATZ zwischen den Varianten (Take-Profit-Flag bzw.
    BTC-Regimefilter); bei den uebrigen drei Bots ist er identisch und nur
    die Kapitalparameter unterscheiden sich.
    """
    live = variant == "live"

    if BOT == "elliott_wave_stocks":
        use_tp = lp.USE_TAKE_PROFIT if live else es.USE_TAKE_PROFIT
        trades = es.collect_all_trades(all_data, es.DEVIATION_PCT, es.STOP_LOSS_PCT,
                                        es.TAKE_PROFIT_FIB, use_tp)
        allocation = es.ALLOCATION_PCT      # live_params dokumentiert keine Allokation
        limit = lp.MAX_CONCURRENT_POSITIONS if live else es.MAX_CONCURRENT_POSITIONS
        return trades, allocation, limit, {"USE_TAKE_PROFIT": use_tp}

    if BOT == "volatility_breakout_crypto":
        trades = es.collect_all_trades(all_data, es.STOP_LOSS_PCT)
        note = {"BTC_REGIME_FILTER_ENABLED": False}
        if live and getattr(lp, "BTC_REGIME_FILTER_ENABLED", False):
            # Die bot-eigenen, unveraenderten Regimefilter-Funktionen - dieselben,
            # die forward_test.py live benutzt.
            from regime_filter import compute_btc_regime, filter_trades_by_regime
            btc = all_data.get("BTCUSDT")
            if btc is not None:
                trades = filter_trades_by_regime(trades, compute_btc_regime(btc))
                note = {"BTC_REGIME_FILTER_ENABLED": True}
        allocation = lp.ALLOCATION_PCT / 100.0 if live else es.ALLOCATION_PCT
        limit = lp.MAX_CONCURRENT_POSITIONS if live else es.MAX_CONCURRENT_POSITIONS
        return trades, allocation, limit, note

    if BOT == "rsi2_mean_reversion":
        trades = es.collect_all_trades(all_data, es.RSI_THRESHOLD, es.STOP_LOSS_PCT)
    elif BOT == "turtle_soup_stocks":
        trades = es.collect_all_trades(all_data, es.DONCHIAN_PERIOD, es.STOP_MODE)
    elif BOT == "volatility_breakout":
        trades = es.collect_all_trades(all_data, es.STOP_LOSS_PCT)
    else:
        raise ValueError(f"{BOT} ist laut sync_table.py nicht abweichend")

    allocation = lp.ALLOCATION_PCT / 100.0 if live else es.ALLOCATION_PCT
    limit = lp.MAX_CONCURRENT_POSITIONS if live else es.MAX_CONCURRENT_POSITIONS
    return trades, allocation, limit, {}


def main():
    import equity_simulation as es
    import live_params as lp

    supports_limit = "max_concurrent_positions" in es.simulate_portfolio.__code__.co_varnames
    all_data = es.load_all_symbol_data()

    out = {"bot": BOT, "varianten": {}}
    for variant in ("backtest", "live"):
        trades, allocation, limit, note = build(es, lp, all_data, variant)
        row = evaluate(es, trades, allocation, limit, supports_limit)
        row["allocation_pct"] = round(allocation * 100, 2)
        row["max_concurrent_positions"] = limit
        row.update(note)
        out["varianten"][variant] = row

    a, b = out["varianten"]["backtest"], out["varianten"]["live"]
    out["verschiebung"] = {
        "rendite_pp": round(b["rendite_pct"] - a["rendite_pct"], 2),
        "rendite_faktor": round(b["rendite_pct"] / a["rendite_pct"], 3) if a["rendite_pct"] else None,
        "max_drawdown_pp": round(b["max_drawdown_pct"] - a["max_drawdown_pct"], 2),
        "calmar_differenz": (round(b["calmar"] - a["calmar"], 2)
                             if a["calmar"] is not None and b["calmar"] is not None else None),
        "ausgefuehrte_trades": b["ausgefuehrt"] - a["ausgefuehrt"],
    }

    with open(os.path.join(RESULTS_DIR, f"impact_{BOT}.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"{BOT}")
    print(f"  {'Variante':<12}{'Allok':>8}{'Limit':>8}{'Trades':>9}{'ausgef.':>9}"
          f"{'Rendite':>12}{'Max DD':>10}{'Calmar':>10}")
    for name, row in out["varianten"].items():
        limit = "unbegr." if row["max_concurrent_positions"] is None else row["max_concurrent_positions"]
        print(f"  {name:<12}{row['allocation_pct']:>7.0f}%{str(limit):>8}{row['trades_gefunden']:>9}"
              f"{row['ausgefuehrt']:>9}{row['rendite_pct']:>11.2f}%{row['max_drawdown_pct']:>9.2f}%"
              f"{str(row['calmar']):>10}")
    v = out["verschiebung"]
    print(f"  Verschiebung: Rendite {v['rendite_pp']:+.2f} pp (Faktor {v['rendite_faktor']}), "
          f"Drawdown {v['max_drawdown_pp']:+.2f} pp, Calmar {v['calmar_differenz']}")


if __name__ == "__main__":
    main()

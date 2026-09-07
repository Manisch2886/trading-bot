"""
Elliott-Wave-Zigzag-Look-Ahead: Baseline gegen korrigierten Backtest
====================================================================================
Untersucht fuer EINEN der beiden Elliott-Wave-Bots, wie stark sich die
Backtest-Kennzahlen aendern, wenn der Einstieg so modelliert wird, wie
`forward_test.py` ihn tatsaechlich ausfuehrt.

Reine Untersuchung: liest nur aus strategies/<bot>/ und schreibt
ausschliesslich nach research/elliott_wave_lookahead/results/.

Ein eigener Prozess je Bot - beide Bots haben gleichnamige, inhaltlich
verschiedene Module (`equity_simulation.py`, `zigzag_indicator.py`, ...);
ein direkter Import beider im selben Prozess wuerde ueber `sys.modules`
still den falschen Bot laden.

--------------------------------------------------------------------
Die drei Varianten
--------------------------------------------------------------------
A  baseline      exakt der heutige Backtest: Einstieg zum Preis UND
                 Zeitpunkt des Wellenende-Pivots.
B  korrigiert    Einstieg zum SCHLUSSKURS des Bestaetigungsbalkens -
                 des ersten Balkens, an dem der Pivot ueberhaupt
                 erkennbar war. Ziel und Stop werden aus diesem neuen
                 Einstiegspreis neu berechnet, genau wie in
                 forward_test.py::find_new_signals. Zusaetzlich gilt das
                 Frische-Fenster: liegt die Bestaetigung mehr als
                 SIGNAL_FRESHNESS hinter dem Wellenende, haette der
                 Live-Bot den Trade nie eroeffnet.
C  verzoegert    wie B, aber ein Balken spaeter - deckt die Latenz des
                 Cronjobs ab (elliott_wave laeuft stuendlich auf
                 Stundenkerzen, elliott_wave_stocks taeglich auf
                 Tageskerzen; ein Balken ist also der realistische
                 Worst Case).

Nutzung:  python3 run_one_bot.py <bot_name>
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

BOT = sys.argv[1]
sys.path.insert(0, os.path.join(_REPO_ROOT, "strategies", BOT))
sys.path.insert(0, os.path.join(_REPO_ROOT, "shared"))

RESULTS_DIR = os.path.join(_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# Stubs fuer nicht installierte bzw. zugangsdatenbehaftete Importe (CLAUDE.md).
# Werden nie aufgerufen - gelesen werden ausschliesslich die lokalen CSVs in data/.
for _name in ("fetch_binance_data", "fetch_stock_data", "yfinance"):
    _m = types.ModuleType(_name)
    _m.fetch_historical_data = lambda *a, **kw: pd.DataFrame()
    _m.download = lambda *a, **kw: pd.DataFrame()
    _m.Ticker = lambda *a, **kw: None
    _m.INTERVAL = "1d"
    sys.modules.setdefault(_name, _m)
_b, _c = types.ModuleType("binance"), types.ModuleType("binance.client")


class _FakeClient:
    KLINE_INTERVAL_1HOUR = "1h"
    KLINE_INTERVAL_4HOUR = "4h"
    KLINE_INTERVAL_1DAY = "1d"


_c.Client = _FakeClient
_b.client = _c
sys.modules.setdefault("binance", _b)
sys.modules.setdefault("binance.client", _c)

from zigzag_confirm import calculate_zigzag_with_confirmation   # noqa: E402

# --- Frische-Fenster, woertlich aus dem jeweiligen forward_test.py ----------
# elliott_wave:        SIGNAL_FRESHNESS_HOURS = 48, Stundenkerzen, Cron stuendlich
# elliott_wave_stocks: SIGNAL_FRESHNESS_DAYS  = 5,  Tageskerzen,  Cron taeglich
FRESHNESS_BARS = {"elliott_wave": 48, "elliott_wave_stocks": 5}
CRON_LAG_BARS = 1     # ein Balken - siehe Modul-Kopf

VARIANT_BASELINE = "baseline"
VARIANT_CORRECTED = "korrigiert"
VARIANT_DELAYED = "verzoegert"
VARIANTS = (VARIANT_BASELINE, VARIANT_CORRECTED, VARIANT_DELAYED)


def calmar(total_return_pct, max_drawdown_pct):
    """Calmar-Konvention aller bisherigen Studien: Rendite / |Max DD|."""
    if max_drawdown_pct is None or abs(max_drawdown_pct) < 1e-12:
        return None
    return round(total_return_pct / abs(max_drawdown_pct), 2)


def build_waves(price_df: pd.DataFrame, deviation_pct: float, counter, min_fib_score=0.3):
    """Wellen wie im Bot, aber mit Bestaetigungszeitpunkt je Welle.

    Die Wellenerkennung selbst (`find_impulse_waves`, `remove_overlapping`)
    ist die UNVERAENDERTE Bot-Funktion; nur die Zigzag-Tabelle traegt eine
    Zusatzspalte. Der Bestaetigungszeitpunkt einer WELLE ist der ihres
    letzten Pivots (Welle 5) - vorher steht das Muster nicht fest.
    """
    zigzag = calculate_zigzag_with_confirmation(price_df, deviation_pct=deviation_pct)
    if len(zigzag) < 6:
        return pd.DataFrame(), zigzag

    impulses = counter.find_impulse_waves(zigzag[["time", "price", "type"]],
                                           min_fib_score=min_fib_score)
    if impulses.empty:
        return pd.DataFrame(), zigzag
    impulses = counter.remove_overlapping(impulses)
    impulses = impulses[impulses["direction"] == "bearish"]   # Long-only, wie im Bot
    if impulses.empty:
        return pd.DataFrame(), zigzag

    confirm_by_time = dict(zip(pd.to_datetime(zigzag["time"]), zigzag["confirm_idx"]))
    pivot_by_time = dict(zip(pd.to_datetime(zigzag["time"]), zigzag["pivot_idx"]))
    impulses = impulses.copy()
    end_times = pd.to_datetime(impulses["end_time"])
    impulses["confirm_idx"] = end_times.map(confirm_by_time)
    impulses["pivot_idx"] = end_times.map(pivot_by_time)
    return impulses.dropna(subset=["confirm_idx", "pivot_idx"]), zigzag


def simulate_exit(price_df, entry_idx, entry_price, target_price, stop_price,
                   max_hold_bars, use_take_profit: bool):
    """Woertliche Uebernahme von backtest_elliott.simulate_trade (Long-Zweig),
    nur auf Index- statt Zeitbasis, damit derselbe Code fuer alle drei
    Varianten gilt. Ausstiegspruefung ab dem Balken NACH dem Einstieg -
    identisch zum Original (`price_df["open_time"] > entry_time`)."""
    highs = price_df["high"].values
    lows = price_df["low"].values
    closes = price_df["close"].values
    times = price_df["open_time"].values

    end = min(entry_idx + 1 + max_hold_bars, len(price_df))
    for i in range(entry_idx + 1, end):
        if lows[i] <= stop_price:
            return {"exit_idx": i, "exit_time": times[i], "exit_price": stop_price,
                    "result": "stop_loss"}
        if use_take_profit and highs[i] >= target_price:
            return {"exit_idx": i, "exit_time": times[i], "exit_price": target_price,
                    "result": "take_profit"}
    if end > entry_idx + 1:
        i = end - 1
        return {"exit_idx": i, "exit_time": times[i], "exit_price": closes[i],
                "result": "time_exit"}
    return None


def collect(all_data: dict, cfg: dict, variant: str, counter, use_take_profit: bool) -> pd.DataFrame:
    """Erzeugt den Trade-Satz einer Variante ueber alle Symbole."""
    rows = []
    for symbol, price_df in all_data.items():
        impulses, _zigzag = build_waves(price_df, cfg["deviation_pct"], counter)
        if impulses.empty:
            continue
        closes = price_df["close"].values
        times = price_df["open_time"].values

        for _, wave in impulses.iterrows():
            pivot_idx = int(wave["pivot_idx"])
            confirm_idx = int(wave["confirm_idx"])

            if variant == VARIANT_BASELINE:
                entry_idx = pivot_idx
                entry_price = float(wave["wave5"])       # der Pivot-PREIS, wie im Bot
            else:
                entry_idx = confirm_idx + (CRON_LAG_BARS if variant == VARIANT_DELAYED else 0)
                if entry_idx >= len(price_df):
                    continue
                # Frische-Fenster aus forward_test.py: liegt die Bestaetigung zu
                # weit hinter dem Wellenende, waere der Trade live nie eroeffnet
                # worden, weil das Muster beim ersten sichtbaren Lauf schon als
                # "nicht mehr frisch" verworfen wird.
                if entry_idx - pivot_idx > cfg["freshness_bars"]:
                    continue
                entry_price = float(closes[entry_idx])   # AKTUELLER Kurs, wie live

            total_move = abs(float(wave["wave5"]) - float(wave["wave0"]))
            target_price = (entry_price + total_move * cfg["take_profit_fib"]
                            if use_take_profit else float("inf"))
            stop_price = entry_price * (1 - cfg["stop_loss_pct"] / 100.0)

            outcome = simulate_exit(price_df, entry_idx, entry_price, target_price,
                                     stop_price, cfg["max_hold_bars"], use_take_profit)
            if outcome is None:
                continue

            pnl_gross = (outcome["exit_price"] - entry_price) / entry_price * 100
            rows.append({
                "symbol": symbol,
                "entry_time": pd.Timestamp(times[entry_idx]),
                "signal_time": pd.Timestamp(times[pivot_idx]),
                "confirm_time": pd.Timestamp(times[confirm_idx]),
                "bars_ahead": confirm_idx - pivot_idx,
                "entry_price": entry_price,
                "exit_time": pd.Timestamp(outcome["exit_time"]),
                "exit_price": outcome["exit_price"],
                "result": outcome["result"],
                "pnl_pct_gross": round(pnl_gross, 2),
                "pnl_pct": round(pnl_gross - cfg["cost_pct"], 2),
                "fib_score": wave["fib_score"],
            })

    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values("entry_time", kind="stable").reset_index(drop=True)


def evaluate(trades: pd.DataFrame, es, cfg: dict) -> dict:
    """Portfolio-Simulation ueber die UNVERAENDERTE simulate_portfolio des Bots."""
    if trades is None or trades.empty:
        return None
    supports_limit = "max_concurrent_positions" in es.simulate_portfolio.__code__.co_varnames
    if supports_limit:
        res = es.simulate_portfolio(trades, es.STARTING_CAPITAL, es.ALLOCATION_PCT,
                                     cfg["max_concurrent"])
    else:
        res = es.simulate_portfolio(trades, es.STARTING_CAPITAL, es.ALLOCATION_PCT)
    total_return = round((res["final_capital"] / es.STARTING_CAPITAL - 1) * 100, 2)
    max_dd = es.calculate_max_drawdown(res["equity_curve"], es.STARTING_CAPITAL)
    counts = trades["result"].value_counts()
    return {
        "num_trades": int(len(trades)),
        "num_executed": res["num_executed"],
        "num_skipped": res["num_skipped"],
        "total_return_pct": total_return,
        "max_drawdown_pct": max_dd,
        "calmar_ratio": calmar(total_return, max_dd),
        "win_rate_pct": round(float((trades["pnl_pct"] > 0).mean() * 100), 1),
        "avg_pnl_pct": round(float(trades["pnl_pct"].mean()), 3),
        "worst_trade_pct": round(float(trades["pnl_pct"].min()), 2),
        "best_trade_pct": round(float(trades["pnl_pct"].max()), 2),
        "result_counts": {str(k): int(v) for k, v in counts.items()},
        "share_take_profit_pct": round(float(counts.get("take_profit", 0)) / len(trades) * 100, 1),
    }


def mechanism_diagnostic(all_data: dict, cfg: dict, counter, use_take_profit: bool) -> dict:
    """
    Beweist den Mechanismus, statt ihn zu behaupten (Frage 1).

    Fuer jeden Baseline-Trade wird geprueft:
      * bars_ahead        - wie viele Balken der Backtest im Voraus kennt
      * stop_moeglich     - faellt zwischen Pivot und Bestaetigung ueberhaupt
                            ein Tief unter den Stop? (Erwartung: nie, denn der
                            Pivot IST das Tief des Abwaertsschenkels)
      * ziel_garantiert   - liegt das Kursziel innerhalb der Bewegung, die per
                            Zigzag-Konstruktion bis zur Bestaetigung ohnehin
                            stattfinden MUSS (>= deviation_pct)?
      * entschieden_vor_bestaetigung - war der Trade bereits beendet, bevor er
                            ueberhaupt erkennbar war?
    """
    ahead, stop_possible, target_guaranteed, decided_before, target_pct = [], 0, 0, 0, []
    entry_discount = []          # wie viel guenstiger der Baseline-Einstieg ist
    total = 0
    for symbol, price_df in all_data.items():
        impulses, _z = build_waves(price_df, cfg["deviation_pct"], counter)
        if impulses.empty:
            continue
        lows = price_df["low"].values
        highs = price_df["high"].values

        for _, wave in impulses.iterrows():
            pivot_idx, confirm_idx = int(wave["pivot_idx"]), int(wave["confirm_idx"])
            entry_price = float(wave["wave5"])
            total_move = abs(entry_price - float(wave["wave0"]))
            target = entry_price + total_move * cfg["take_profit_fib"]
            stop = entry_price * (1 - cfg["stop_loss_pct"] / 100.0)

            outcome = simulate_exit(price_df, pivot_idx, entry_price, target, stop,
                                     cfg["max_hold_bars"], use_take_profit)
            if outcome is None:
                continue
            total += 1
            ahead.append(confirm_idx - pivot_idx)

            # Der ZWEITE Kanal des Look-Aheads, unabhaengig vom Take-Profit:
            # der Pivot IST das Tief des Abwaertsschenkels. Der Backtest kauft
            # also zum guenstigsten Kurs des ganzen Schenkels, waehrend der
            # Live-Bot erst zum Bestaetigungskurs kaufen kann - der per
            # Konstruktion mindestens deviation_pct darueber liegen kann.
            if confirm_idx < len(closes_arr := price_df["close"].values):
                entry_discount.append((float(closes_arr[confirm_idx]) - entry_price)
                                      / entry_price * 100)

            window = slice(pivot_idx + 1, confirm_idx + 1)
            if len(lows[window]) and float(np.min(lows[window])) <= stop:
                stop_possible += 1
            target_move_pct = (target - entry_price) / entry_price * 100
            target_pct.append(target_move_pct)
            if use_take_profit and target_move_pct <= cfg["deviation_pct"]:
                target_guaranteed += 1
            if outcome["exit_idx"] <= confirm_idx:
                decided_before += 1

    if not total:
        return None
    ahead_arr = np.asarray(ahead, dtype=float)
    disc = np.asarray(entry_discount, dtype=float)
    return {
        "trades": total,
        "bars_ahead_median": float(np.median(ahead_arr)),
        "bars_ahead_mean": round(float(ahead_arr.mean()), 1),
        "bars_ahead_max": int(ahead_arr.max()),
        # Kanal 1: der Einstiegskurs selbst
        "einstiegsvorteil_median_pct": round(float(np.median(disc)), 2) if disc.size else None,
        "einstiegsvorteil_mittel_pct": round(float(disc.mean()), 2) if disc.size else None,
        "anteil_einstieg_guenstiger_pct": (round(float((disc > 0).mean() * 100), 1)
                                            if disc.size else None),
        "trades_mit_stop_treffer_vor_bestaetigung": stop_possible,
        "anteil_stop_treffer_vor_bestaetigung_pct": round(stop_possible / total * 100, 2),
        # Kanal 2: das garantierte Kursziel - nur sinnvoll, wenn ueberhaupt ein
        # Take-Profit gesetzt ist. Bei USE_TAKE_PROFIT = False gibt es kein Ziel,
        # das die Konstruktion garantieren koennte; dann ist die Kennzahl None
        # statt 0 %, damit sie nicht als "kein Problem" fehlgelesen wird.
        "kursziel_median_pct": round(float(np.median(target_pct)), 2) if use_take_profit else None,
        "deviation_pct": cfg["deviation_pct"],
        "trades_mit_garantiertem_kursziel": target_guaranteed if use_take_profit else None,
        "anteil_garantiertes_kursziel_pct": (round(target_guaranteed / total * 100, 1)
                                              if use_take_profit else None),
        "trades_entschieden_vor_bestaetigung": decided_before,
        "anteil_entschieden_vor_bestaetigung_pct": round(decided_before / total * 100, 1),
        "take_profit_aktiv": use_take_profit,
    }


def main():
    import equity_simulation as es
    import live_params as lp
    import elliott_wave_counter as counter
    import backtest_elliott as bt

    use_take_profit = bool(getattr(lp, "USE_TAKE_PROFIT", True))
    cfg = {
        "deviation_pct": float(lp.DEVIATION_PCT),
        "stop_loss_pct": float(lp.STOP_LOSS_PCT),
        "take_profit_fib": float(lp.TAKE_PROFIT_FIB),
        "max_hold_bars": int(bt.MAX_HOLD_HOURS),
        "cost_pct": 2 * (bt.TRADING_FEE_PCT + bt.SLIPPAGE_PCT),
        "max_concurrent": getattr(es, "MAX_CONCURRENT_POSITIONS", None),
        "freshness_bars": FRESHNESS_BARS[BOT],
        "use_take_profit": use_take_profit,
    }

    all_data = es.load_all_symbol_data()

    # Die BASELINE stammt aus der bot-eigenen, unveraenderten collect_all_trades -
    # nicht aus dem Nachbau unten. Grund: der Nachbau erzeugt zwar denselben
    # Trade-SATZ (verify_baseline.py prueft das Trade fuer Trade), aber eine
    # andere Zeilenreihenfolge unter gleichzeitigen Einstiegen. Die
    # Portfolio-Simulation ist davon abhaengig (siehe research/order_sensitivity),
    # und die berichtete Baseline soll auf die zweite Nachkommastelle die des
    # Bots sein. Der Unterschied betraegt bei elliott_wave 0,32 pp auf +2185 %.
    sets = {}
    if BOT == "elliott_wave_stocks":
        sets[VARIANT_BASELINE] = es.collect_all_trades(
            all_data, cfg["deviation_pct"], cfg["stop_loss_pct"],
            cfg["take_profit_fib"], use_take_profit)
    else:
        sets[VARIANT_BASELINE] = es.collect_all_trades(
            all_data, cfg["deviation_pct"], cfg["stop_loss_pct"], cfg["take_profit_fib"])
    sets[VARIANT_BASELINE]["result"] = sets[VARIANT_BASELINE]["result"].astype(str)
    for v in (VARIANT_CORRECTED, VARIANT_DELAYED):
        sets[v] = collect(all_data, cfg, v, counter, use_take_profit)
    periods = {v: evaluate(sets[v], es, cfg) for v in VARIANTS}
    diagnostic = mechanism_diagnostic(all_data, cfg, counter, use_take_profit)

    span = pd.concat([sets[v][["entry_time", "exit_time"]] for v in VARIANTS
                      if sets[v] is not None and not sets[v].empty])
    out = {
        "bot": BOT,
        "config": cfg,
        "data_basis": {
            "symbols_loaded": len(all_data),
            "first_entry": str(span["entry_time"].min().date()),
            "last_exit": str(span["exit_time"].max().date()),
            "years_covered": round((span["exit_time"].max() - span["entry_time"].min()).days / 365.25, 2),
        },
        "mechanism": diagnostic,
        "variants": periods,
    }

    with open(os.path.join(RESULTS_DIR, f"{BOT}.json"), "w") as fh:
        json.dump(out, fh, indent=2, default=str, ensure_ascii=False)
    for variant in VARIANTS:
        if not sets[variant].empty:
            sets[variant].to_csv(os.path.join(RESULTS_DIR, f"{BOT}_trades_{variant}.csv"), index=False)

    print(f"\n{BOT}  (Take-Profit {'aktiv' if use_take_profit else 'AUS'}, "
          f"Zigzag {cfg['deviation_pct']} %, Stop {cfg['stop_loss_pct']} %, "
          f"Limit {cfg['max_concurrent']})")
    print(f"  {'Variante':<14}{'Trades':>8}{'ausgef.':>9}{'Rendite':>12}{'Max DD':>10}"
          f"{'Calmar':>10}{'Gewinnrate':>12}{'Take-Profit':>13}")
    for variant in VARIANTS:
        r = periods[variant]
        if r is None:
            print(f"  {variant:<14}  keine Trades")
            continue
        print(f"  {variant:<14}{r['num_trades']:>8}{r['num_executed']:>9}"
              f"{r['total_return_pct']:>11.2f}%{r['max_drawdown_pct']:>9.2f}%"
              f"{str(r['calmar_ratio']):>10}{r['win_rate_pct']:>11.1f}%"
              f"{r['share_take_profit_pct']:>12.1f}%")

    if diagnostic:
        d = diagnostic
        print(f"\n  Mechanismus (Baseline-Trades: {d['trades']})")
        print(f"    Balken Vorwissen: Median {d['bars_ahead_median']:.0f}, "
              f"Mittel {d['bars_ahead_mean']}, Maximum {d['bars_ahead_max']}")
        print(f"    Tief unter dem Stop vor der Bestaetigung: "
              f"{d['trades_mit_stop_treffer_vor_bestaetigung']} von {d['trades']} "
              f"({d['anteil_stop_treffer_vor_bestaetigung_pct']} %)")
        print(f"    Einstiegsvorteil gegenueber dem Bestaetigungskurs: Median "
              f"{d['einstiegsvorteil_median_pct']} %, Mittel {d['einstiegsvorteil_mittel_pct']} % "
              f"(guenstiger in {d['anteil_einstieg_guenstiger_pct']} % der Trades)")
        if d["take_profit_aktiv"]:
            print(f"    Kursziel im Median {d['kursziel_median_pct']} % - "
                  f"garantierte Gegenbewegung {d['deviation_pct']} % -> "
                  f"{d['anteil_garantiertes_kursziel_pct']} % der Trades mit "
                  f"konstruktionsbedingt sicherem Ziel")
        else:
            print("    Kursziel: kein Take-Profit gesetzt - Kanal 2 (garantiertes Ziel) "
                  "entfaellt, Kanal 1 (Einstiegskurs) wirkt weiter")
        print(f"    Bereits entschieden, bevor das Signal erkennbar war: "
              f"{d['anteil_entschieden_vor_bestaetigung_pct']} %")

    print(f"\nGespeichert: {os.path.join(RESULTS_DIR, f'{BOT}.json')}")


if __name__ == "__main__":
    main()

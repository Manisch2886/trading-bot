"""
Volatilitaets-skalierte Positionsgroessen - Analyse fuer EINEN Bot
========================================================================
Wird pro Bot in einem EIGENEN, ISOLIERTEN Prozess aufgerufen (siehe
run_all.py) - alle 9 Bots haben gleichnamige, aber INHALTLICH
unterschiedliche Module (live_params.py, multi_symbol_optimise.py,
backtest_*.py, indicators.py) in ihren jeweiligen strategies/<bot>/-
Ordnern. Wuerden mehrere Bots im selben Python-Prozess nacheinander
importiert, wuerde sys.modules-Caching die FALSCHE Version fuer den
zweiten/dritten Bot liefern (dieselbe Fehlerklasse, die bereits bei den
fruehren Pyramiding-Fix- und E-Mail-zu-Telegram-Sandbox-Tests dieses
Projekts aufgetreten ist) - ein separater Prozess pro Bot umgeht das
zuverlaessig.

WICHTIG - reine Backtest-Untersuchung: importiert NUR LESEND aus
strategies/<bot>/ (live_params.py, multi_symbol_optimise.py,
equity_simulation.py, multi_symbol_walk_forward.py, backtest_*.py) -
schreibt NIRGENDS in strategies/, veraendert KEINE Live-Datei. Alle
Ergebnisse landen ausschliesslich unter research/volatility_scaled_sizing/results/.

Nutzung:
    python3 run_one_bot.py <bot_name>
"""
import os
import sys
import json
import types

import numpy as np
import pandas as pd

_RESEARCH_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_RESEARCH_DIR))
sys.path.insert(0, _RESEARCH_DIR)
from vol_sizing_core import (
    compute_realized_volatility, compute_inverse_vol_weights,
    simulate_weighted_portfolio, calculate_max_drawdown,
)

BOT = sys.argv[1]
STRATEGY_DIR = os.path.join(_REPO_ROOT, "strategies", BOT)
SHARED_DIR = os.path.join(_REPO_ROOT, "shared")
sys.path.insert(0, STRATEGY_DIR)
sys.path.insert(0, SHARED_DIR)

# elliott_wave und t3_supertrend importieren ihr multi_symbol_optimise.py
# nur fuer die INTERVAL-Konstante ueber fetch_multi_data.py/fetch_4h_data.py,
# die wiederum `from binance.client import Client` und
# `from fetch_binance_data import fetch_historical_data` am Modul-Anfang
# ausfuehren - `python-binance` ist in dieser Sandbox nicht installiert,
# und shared/fetch_binance_data.py enthaelt Zugangsdaten und ist laut
# CLAUDE.md absichtlich gitignored (hier nicht vorhanden). Beide werden
# als Stubs injiziert, BEVOR irgendetwas fuer diese beiden Bots importiert
# wird - werden hier nie tatsaechlich aufgerufen (wir laden Kursdaten
# ausschliesslich aus den bereits vorhandenen lokalen CSVs in data/, kein
# echter Netzwerk-Abruf noetig fuer diese reine Backtest-Untersuchung).
if BOT in ("elliott_wave", "t3_supertrend"):
    fake_fetch_binance = types.ModuleType("fetch_binance_data")
    fake_fetch_binance.fetch_historical_data = lambda *a, **kw: pd.DataFrame()
    sys.modules["fetch_binance_data"] = fake_fetch_binance

    fake_binance_pkg = types.ModuleType("binance")
    fake_binance_client_mod = types.ModuleType("binance.client")

    class _FakeClient:
        KLINE_INTERVAL_1HOUR = "1h"
        KLINE_INTERVAL_4HOUR = "4h"

    fake_binance_client_mod.Client = _FakeClient
    fake_binance_pkg.client = fake_binance_client_mod
    sys.modules["binance"] = fake_binance_pkg
    sys.modules["binance.client"] = fake_binance_client_mod

RESULTS_DIR = os.path.join(_RESEARCH_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# ANNAHME 1 (siehe Abschlussbericht): Volatilitaets-Fenstergroesse.
# Die Aufgabe schlaegt "90 Handelstage fuer Aktien" vor. Fuer Krypto-Bots
# auf TAGES-Kerzen (rsi2_crypto, turtle_soup_crypto, volatility_breakout_crypto)
# entspricht das wegen des 24/7-Handels automatisch 90 KALENDERTAGEN - keine
# Anpassung noetig, 90 Bars = 90 Tage in beiden Faellen.
# Elliott Wave (Krypto, 1h-Kerzen) und T3/ADX/SuperTrend (4h-Kerzen) laufen
# aber NICHT auf Tageskerzen - fuer diese wird die BAR-ANZAHL so gewaehlt,
# dass die ZEITSPANNE des Volatilitaets-Fensters trotzdem ~90 Kalendertage
# entspricht (konsistente "Marktregime-Erinnerungsspanne" unabhaengig von
# der Sampling-Frequenz des jeweiligen Bots):
#   1h-Kerzen:  90 Tage * 24 Kerzen/Tag = 2160 Bars
#   4h-Kerzen:  90 Tage *  6 Kerzen/Tag =  540 Bars
# Das ist eine bewusste, ueber die woertliche Aufgabenstellung hinausgehende
# Interpretation (die nur explizit "90 Handelstage/Kalendertage" nannte, ohne
# Sub-Tages-Zeitrahmen zu erwaehnen) - im Bericht als Annahme ausgewiesen.
# ---------------------------------------------------------------------------
VOL_WINDOW_BARS = {
    "elliott_wave": 2160,             # 1h-Kerzen, ~90 Kalendertage
    "elliott_wave_stocks": 90,        # 1d-Kerzen (Handelstage)
    "t3_supertrend": 540,             # 4h-Kerzen, ~90 Kalendertage
    "rsi2_crypto": 90,                # 1d-Kerzen (Kalendertage, 24/7)
    "rsi2_mean_reversion": 90,        # 1d-Kerzen (Handelstage)
    "turtle_soup_crypto": 90,
    "turtle_soup_stocks": 90,
    "volatility_breakout": 90,
    "volatility_breakout_crypto": 90,
}

# ANNAHME 2 (siehe Abschlussbericht): ALLOCATION_PCT ist bei 3 Bots
# (elliott_wave, elliott_wave_stocks, t3_supertrend) in live_params.py NICHT
# dokumentiert (anders als bei den 6 anderen Bots, die explizit einen Wert
# fuehren - "NUR zur Dokumentation", da forward_test.py kein echtes Kapital
# trackt, siehe fruehere Pyramiding-Untersuchung). Fuer diese reine
# Backtest-/Vergleichs-Simulation wird deshalb ein Platzhalter-Wert
# angenommen, angelehnt an die MEHRHEIT der anderen Bots (4 von 6 nutzen
# 10%): 10% Allokation. MAX_CONCURRENT_POSITIONS fehlt NUR bei elliott_wave
# komplett (elliott_wave_stocks hat 8, t3_supertrend hat 5 real dokumentiert)
# - fuer elliott_wave wird der Wert des eng verwandten Schwester-Bots
# elliott_wave_stocks (8) uebernommen, da beide dieselbe Strategie-Logik auf
# unterschiedlichen Maerkten fahren (siehe deren Modul-Docstrings
# "Analog zu ...").
ASSUMED_ALLOCATION_PCT = {"elliott_wave": 10.0, "elliott_wave_stocks": 10.0, "t3_supertrend": 10.0}
ASSUMED_MAX_CONCURRENT = {"elliott_wave": 8}

# ANNAHME 3: Anzahl der Walk-Forward-Stabilitaets-Fenster. Die Aufgabe
# verlangt eine Pruefung ueber "mehrere Walk-Forward-Fenster", ohne eine
# genaue Anzahl vorzugeben. Es werden 4 in etwa gleich lange, chronologisch
# aufeinanderfolgende Fenster ueber die GESAMTE verfuegbare Trade-Historie
# (In-Sample + Out-of-Sample zusammen) verwendet - ein Kompromiss zwischen
# genug Fenstern fuer ein aussagekraeftiges Stabilitaetsbild und genug
# Trades pro Fenster fuer statistisch nicht komplett bedeutungslose
# Einzelergebnisse.
NUM_STABILITY_WINDOWS = 4

STARTING_CAPITAL = 10_000.0  # identisch zur Konvention in allen 9 equity_simulation.py


def load_bot_data():
    """
    Liefert (all_trades, price_by_symbol, allocation_pct, max_concurrent,
    train_split_ratio) fuer den per BOT-Variable gewaehlten Bot - liest
    AUSSCHLIESSLICH aus den bereits bestehenden, validierten Backtest-/
    Live-Parameter-Modulen des jeweiligen Bots (kein neu erfundener
    Signal-Code). all_trades enthaelt mindestens die Spalten
    entry_time/exit_time/symbol/pnl_pct. price_by_symbol ist
    {symbol: DataFrame[open_time, close]} fuer die Volatilitaets-Berechnung.
    """
    if BOT in ("volatility_breakout", "volatility_breakout_crypto"):
        import equity_simulation as es
        import live_params as lp
        import multi_symbol_walk_forward as mswf

        all_data = es.load_all_symbol_data()
        max_hold_days = getattr(lp, "MAX_HOLD_DAYS", None)
        trades = es.collect_all_trades(all_data, stop_loss_pct=lp.STOP_LOSS_PCT,
                                        max_hold_days=max_hold_days)
        # WICHTIG: load_all_symbol_data()-Rueckgabeform unterscheidet sich
        # zwischen den beiden Geschwister-Bots (bestaetigt durch Lesen von
        # equity_simulation.py::collect_all_trades() in beiden Bots):
        # volatility_breakout (Aktien) liefert (df_ind, entry_cutoff)-Tupel
        # (RECENT_YEARS_ONLY-Survivorship-Bias-Behandlung), waehrend
        # volatility_breakout_crypto rohe DataFrames liefert.
        if BOT == "volatility_breakout":
            price_by_symbol = {sym: df_ind[["open_time", "close"]] for sym, (df_ind, _cutoff) in all_data.items()}
        else:
            price_by_symbol = {sym: df[["open_time", "close"]] for sym, df in all_data.items()}
        allocation_pct = lp.ALLOCATION_PCT
        max_concurrent = lp.MAX_CONCURRENT_POSITIONS
        train_ratio = mswf.TRAIN_SPLIT_RATIO

    elif BOT == "rsi2_mean_reversion":
        import equity_simulation as es
        import live_params as lp
        import multi_symbol_walk_forward as mswf

        all_data = es.load_all_symbol_data()
        trades = es.collect_all_trades(all_data, rsi_threshold=lp.RSI_THRESHOLD,
                                        stop_loss_pct=lp.STOP_LOSS_PCT)
        price_by_symbol = {sym: df_ind[["open_time", "close"]] for sym, (df_ind, _cutoff) in all_data.items()}
        allocation_pct = lp.ALLOCATION_PCT
        max_concurrent = lp.MAX_CONCURRENT_POSITIONS
        train_ratio = mswf.TRAIN_SPLIT_RATIO

    elif BOT == "rsi2_crypto":
        import equity_simulation as es
        import live_params as lp
        import multi_symbol_walk_forward as mswf

        all_data = es.load_all_symbol_data()  # {symbol: raw_price_df}
        trades = es.collect_all_trades(all_data, rsi_threshold=lp.RSI_THRESHOLD,
                                        sma_trend_period=lp.SMA_TREND_FILTER,
                                        stop_loss_pct=lp.STOP_LOSS_PCT)
        price_by_symbol = {sym: df[["open_time", "close"]] for sym, df in all_data.items()}
        allocation_pct = lp.ALLOCATION_PCT
        max_concurrent = lp.MAX_CONCURRENT_POSITIONS
        train_ratio = mswf.TRAIN_SPLIT_RATIO

    elif BOT in ("turtle_soup_crypto", "turtle_soup_stocks"):
        import equity_simulation as es
        import live_params as lp
        import multi_symbol_walk_forward as mswf

        all_data = es.load_all_symbol_data()
        trades = es.collect_all_trades(all_data, donchian_period=lp.DONCHIAN_PERIOD,
                                        stop_mode=lp.STOP_MODE)
        # WICHTIG: anders als bei turtle_soup_crypto (rohe DataFrames)
        # liefert turtle_soup_stocks (df, entry_cutoff)-Tupel (ebenfalls
        # RECENT_YEARS_ONLY-Survivorship-Bias-Behandlung wie die anderen
        # Aktien-Bots) - bestaetigt durch Lesen von
        # equity_simulation.py::collect_all_trades() in beiden Bots.
        if BOT == "turtle_soup_stocks":
            price_by_symbol = {sym: df[["open_time", "close"]] for sym, (df, _cutoff) in all_data.items()}
        else:
            price_by_symbol = {sym: df[["open_time", "close"]] for sym, df in all_data.items()}
        allocation_pct = lp.ALLOCATION_PCT
        max_concurrent = lp.MAX_CONCURRENT_POSITIONS
        train_ratio = mswf.TRAIN_SPLIT_RATIO

    elif BOT == "t3_supertrend":
        import equity_simulation as es
        import live_params as lp
        import multi_symbol_walk_forward as mswf

        all_data = es.load_all_symbol_data()  # {symbol: raw_price_df}
        trades = es.collect_all_trades(all_data, t3_fast=lp.T3_FAST_LENGTH, t3_slow=lp.T3_SLOW_LENGTH,
                                        adx_threshold=lp.ADX_THRESHOLD, stop_loss_pct=lp.STOP_LOSS_PCT)
        price_by_symbol = {sym: df[["open_time", "close"]] for sym, df in all_data.items()}
        allocation_pct = ASSUMED_ALLOCATION_PCT[BOT]
        max_concurrent = lp.MAX_CONCURRENT_POSITIONS
        train_ratio = mswf.TRAIN_SPLIT_RATIO

    elif BOT in ("elliott_wave", "elliott_wave_stocks"):
        import equity_simulation as es
        import live_params as lp
        import multi_symbol_walk_forward as mswf

        all_data = es.load_all_symbol_data()  # {symbol: raw_price_df}
        if BOT == "elliott_wave":
            trades = es.collect_all_trades(all_data, deviation_pct=lp.DEVIATION_PCT,
                                            stop_loss_pct=lp.STOP_LOSS_PCT,
                                            take_profit_fib=lp.TAKE_PROFIT_FIB)
        else:
            trades = es.collect_all_trades(all_data, deviation_pct=lp.DEVIATION_PCT,
                                            stop_loss_pct=lp.STOP_LOSS_PCT,
                                            take_profit_fib=lp.TAKE_PROFIT_FIB,
                                            use_take_profit=lp.USE_TAKE_PROFIT)
        price_by_symbol = {sym: df[["open_time", "close"]] for sym, df in all_data.items()}
        allocation_pct = ASSUMED_ALLOCATION_PCT[BOT]
        max_concurrent = ASSUMED_MAX_CONCURRENT.get(BOT, getattr(lp, "MAX_CONCURRENT_POSITIONS", None))
        train_ratio = mswf.TRAIN_SPLIT_RATIO

    else:
        raise ValueError(f"Unbekannter Bot: {BOT}")

    allocation_frac = allocation_pct / 100.0
    trades = trades.reset_index(drop=True)
    return trades, price_by_symbol, allocation_frac, max_concurrent, train_ratio


def attach_volatility(trades: pd.DataFrame, price_by_symbol: dict, window: int) -> pd.Series:
    """Berechnet die realisierte Volatilitaet AM EINSTIEGSZEITPUNKT jedes
    Trades (siehe vol_sizing_core.volatility_at_entry) - EIN rollierendes
    Volatilitaets-Array pro Symbol wird einmal vorab berechnet (nicht pro
    Trade neu), fuer Performance bei Symbolen mit vielen Trades."""
    vol_cache = {}
    for symbol, df in price_by_symbol.items():
        df = df.sort_values("open_time").reset_index(drop=True)
        vol_series = compute_realized_volatility(df, window)
        vol_cache[symbol] = (df["open_time"].to_numpy(), vol_series.to_numpy())

    result = []
    for _, trade in trades.iterrows():
        symbol = trade["symbol"]
        if symbol not in vol_cache:
            result.append(np.nan)
            continue
        times, vols = vol_cache[symbol]
        mask = times <= np.datetime64(trade["entry_time"])
        if not mask.any():
            result.append(np.nan)
            continue
        value = vols[mask][-1]
        result.append(value if np.isfinite(value) else np.nan)
    return pd.Series(result, index=trades.index)


def run_variant(trades: pd.DataFrame, weights: pd.Series, allocation_pct: float, max_concurrent) -> dict:
    result = simulate_weighted_portfolio(trades, STARTING_CAPITAL, allocation_pct, weights, max_concurrent)
    total_return_pct = round((result["final_capital"] / STARTING_CAPITAL - 1) * 100, 2)
    max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
    return {
        "total_return_pct": total_return_pct,
        "max_drawdown_pct": max_dd,
        "final_capital": result["final_capital"],
        "num_executed": result["num_executed"],
        "num_skipped": result["num_skipped"],
    }


def buy_and_hold_reference(price_by_symbol: dict, start_time, end_time) -> dict:
    """
    Einfache, EINHEITLICHE Buy-and-Hold-Referenz (Pflicht-Vergleich laut
    Aufgabenstellung): gleichgewichtet ueber ALLE im Backtest verwendeten
    Symbole, Kauf zu Periodenbeginn, Halten bis Periodenende - bewusst
    NICHT die bot-spezifischen buy_and_hold_benchmark.py-Skripte 1:1
    reproduziert (die im Detail leicht unterschiedliche Gewichtungs-/
    Rebalancing-Annahmen haben koennten), sondern eine einzige, ueber alle
    9 Bots konsistente Referenzmethode - siehe Abschlussbericht,
    "Getroffene Annahmen".
    """
    per_symbol_returns = []
    for symbol, df in price_by_symbol.items():
        window_df = df[(df["open_time"] >= start_time) & (df["open_time"] <= end_time)]
        if len(window_df) < 2:
            continue
        start_price = window_df["close"].iloc[0]
        end_price = window_df["close"].iloc[-1]
        if (start_price and np.isfinite(start_price) and start_price > 0
                and np.isfinite(end_price)):
            per_symbol_returns.append((end_price / start_price - 1) * 100)

    if not per_symbol_returns:
        return {"total_return_pct": None, "num_symbols": 0}
    return {
        "total_return_pct": round(float(np.mean(per_symbol_returns)), 2),
        "num_symbols": len(per_symbol_returns),
    }


def analyze_period(trades: pd.DataFrame, price_by_symbol: dict, window: int,
                    allocation_pct: float, max_concurrent: float) -> dict:
    """Fuehrt fixe- und vol-skalierte Simulation fuer EINEN
    Zeitabschnitt (In-Sample, Out-of-Sample, oder ein Stabilitaets-
    Fenster) durch. Vol-Gewichte werden NUR aus den Trades DIESES
    Abschnitts kalibriert (Mittelwert 1.0 INNERHALB des Abschnitts) -
    verhindert Informationsfluss zwischen In-Sample und Out-of-Sample
    (strikte Trennung, siehe Aufgaben-Methodik-Vorgabe)."""
    if trades.empty:
        return None

    vols = attach_volatility(trades, price_by_symbol, window)
    weights = compute_inverse_vol_weights(vols)

    fixed = run_variant(trades, pd.Series(1.0, index=trades.index), allocation_pct, max_concurrent)
    scaled = run_variant(trades, weights, allocation_pct, max_concurrent)

    bh_start = trades["entry_time"].min()
    bh_end = trades["exit_time"].max()
    bh = buy_and_hold_reference(price_by_symbol, bh_start, bh_end)

    return {
        "num_trades": len(trades),
        "mean_vol_weight": round(float(weights.mean()), 4),
        "fixed": fixed,
        "vol_scaled": scaled,
        "buy_and_hold": bh,
    }


def main():
    window = VOL_WINDOW_BARS[BOT]
    trades, price_by_symbol, allocation_pct, max_concurrent, train_ratio = load_bot_data()

    if trades.empty:
        print(f"{BOT}: keine Trades gefunden - Abbruch.")
        json.dump({"bot": BOT, "error": "keine Trades gefunden"},
                  open(os.path.join(RESULTS_DIR, f"{BOT}.json"), "w"), indent=2)
        return

    entry_min, entry_max = trades["entry_time"].min(), trades["entry_time"].max()
    split_time = entry_min + (entry_max - entry_min) * train_ratio

    in_sample = trades[trades["entry_time"] < split_time]
    out_of_sample = trades[trades["entry_time"] >= split_time]

    is_result = analyze_period(in_sample, price_by_symbol, window, allocation_pct, max_concurrent)
    oos_result = analyze_period(out_of_sample, price_by_symbol, window, allocation_pct, max_concurrent)

    # Walk-Forward-Stabilitaet: NUM_STABILITY_WINDOWS gleich lange,
    # chronologische Fenster ueber die GESAMTE Trade-Historie (IS+OOS).
    window_edges = pd.date_range(entry_min, entry_max, periods=NUM_STABILITY_WINDOWS + 1)
    stability_windows = []
    for i in range(NUM_STABILITY_WINDOWS):
        lo, hi = window_edges[i], window_edges[i + 1]
        if i == NUM_STABILITY_WINDOWS - 1:
            window_trades = trades[(trades["entry_time"] >= lo) & (trades["entry_time"] <= hi)]
        else:
            window_trades = trades[(trades["entry_time"] >= lo) & (trades["entry_time"] < hi)]
        window_result = analyze_period(window_trades, price_by_symbol, window, allocation_pct, max_concurrent)
        stability_windows.append({
            "window_index": i + 1,
            "start": str(lo.date()), "end": str(hi.date()),
            "result": window_result,
        })

    output = {
        "bot": BOT,
        "assumptions": {
            "vol_window_bars": window,
            "allocation_pct": round(allocation_pct * 100, 2),
            "allocation_pct_assumed": BOT in ASSUMED_ALLOCATION_PCT,
            "max_concurrent_positions": max_concurrent,
            "max_concurrent_assumed": BOT in ASSUMED_MAX_CONCURRENT,
            "train_split_ratio": train_ratio,
            "starting_capital": STARTING_CAPITAL,
            "num_stability_windows": NUM_STABILITY_WINDOWS,
        },
        "total_trades": len(trades),
        "in_sample": is_result,
        "out_of_sample": oos_result,
        "stability_windows": stability_windows,
    }

    out_path = os.path.join(RESULTS_DIR, f"{BOT}.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"{BOT}: {len(trades)} Trades gesamt. Ergebnis gespeichert: {out_path}")
    if is_result:
        print(f"  In-Sample:     fix {is_result['fixed']['total_return_pct']}% / "
              f"vol-skaliert {is_result['vol_scaled']['total_return_pct']}%")
    if oos_result:
        print(f"  Out-of-Sample: fix {oos_result['fixed']['total_return_pct']}% / "
              f"vol-skaliert {oos_result['vol_scaled']['total_return_pct']}%")


if __name__ == "__main__":
    main()

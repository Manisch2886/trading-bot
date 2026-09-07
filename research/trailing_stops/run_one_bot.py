"""
ATR-Trailing-Stop-Untersuchung - Analyse fuer EINEN Bot
============================================================
Wird pro Bot in einem EIGENEN, ISOLIERTEN Prozess aufgerufen (siehe
run_all.py). Grund identisch zur Vol-Sizing-Untersuchung: alle Bots
haben gleichnamige, aber inhaltlich unterschiedliche Module
(live_params.py, backtest_*.py, indicators.py, multi_symbol_optimise.py)
- im selben Prozess wuerde sys.modules-Caching fuer den zweiten Bot die
FALSCHE Version liefern.

WICHTIG - reine Backtest-Untersuchung: importiert NUR LESEND aus
strategies/<bot>/ und schreibt ausschliesslich nach
research/trailing_stops/results/. Keine Live-Datei wird veraendert.

Nutzung:
    python3 run_one_bot.py <bot_name> [atr_window]
"""

import json
import os
import sys
import types

import numpy as np
import pandas as pd

_RESEARCH_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_RESEARCH_DIR))
sys.path.insert(0, _RESEARCH_DIR)

import decision_basis as db
from atr_core import (
    wilder_atr, calibrate_atr_multiplier, simulate_exit, simulate_portfolio,
    calculate_max_drawdown, calmar_ratio, initial_stop_price,
    STOP_FIXED_STATIC, STOP_FIXED_TRAILING, STOP_ATR_TRAILING,
)

BOT = sys.argv[1]
ATR_WINDOW = int(sys.argv[2]) if len(sys.argv) > 2 else 14

STRATEGY_DIR = os.path.join(_REPO_ROOT, "strategies", BOT)
SHARED_DIR = os.path.join(_REPO_ROOT, "shared")
sys.path.insert(0, STRATEGY_DIR)
sys.path.insert(0, SHARED_DIR)

# Die beiden Binance-Bots importieren ueber ihr multi_symbol_optimise.py
# indirekt `binance.client` und das gitignorte shared/fetch_binance_data.py
# (enthaelt Zugangsdaten, siehe CLAUDE.md). Beides wird als Stub injiziert,
# BEVOR irgendein Bot-Modul importiert wird - hier nie tatsaechlich
# aufgerufen, da ausschliesslich die bereits vorhandenen lokalen CSVs in
# data/ gelesen werden (kein Netzwerkzugriff). Identisches Vorgehen wie in
# research/volatility_scaled_sizing/run_one_bot.py.
if BOT in ("elliott_wave", "t3_supertrend"):
    fake_fetch = types.ModuleType("fetch_binance_data")
    fake_fetch.fetch_historical_data = lambda *a, **kw: pd.DataFrame()
    sys.modules["fetch_binance_data"] = fake_fetch

    fake_binance = types.ModuleType("binance")
    fake_client_mod = types.ModuleType("binance.client")

    class _FakeClient:
        KLINE_INTERVAL_1HOUR = "1h"
        KLINE_INTERVAL_4HOUR = "4h"

    fake_client_mod.Client = _FakeClient
    fake_binance.client = fake_client_mod
    sys.modules["binance"] = fake_binance
    sys.modules["binance.client"] = fake_client_mod

# elliott_wave_stocks importiert seine INTERVAL-Konstante ueber
# fetch_stock_data.py, das `import yfinance` am Modul-Anfang ausfuehrt -
# in dieser Sandbox nicht installiert und fuer diese Untersuchung auch
# nicht noetig (es werden ausschliesslich die bereits vorhandenen lokalen
# CSVs in data/ gelesen, kein Kursabruf). Gleiches Stub-Muster wie oben.
if BOT == "elliott_wave_stocks":
    fake_yf = types.ModuleType("yfinance")
    fake_yf.download = lambda *a, **kw: pd.DataFrame()
    fake_yf.Ticker = lambda *a, **kw: None
    sys.modules["yfinance"] = fake_yf

RESULTS_DIR = os.path.join(_RESEARCH_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

STARTING_CAPITAL = 10_000.0          # Konvention aller Bot-eigenen equity_simulation.py
NUM_STABILITY_WINDOWS = 4            # wie in der Vol-Sizing-Untersuchung

# Entscheidungsgrundlage (Nachtrag) - identische Einstellungen wie in der
# Vertiefungsstudie research/vbc_deepdive/, damit beide vergleichbar bleiben.
BOOTSTRAP_REPLICATES = 2000
BOOTSTRAP_BLOCK_MONTHS = 3
BOOTSTRAP_SEED = 20260907
TIE_ORDER_PERMUTATIONS = 500

# Fuer die beiden Elliott-Wave-Bots wird KEIN Bootstrap gerechnet: ihr
# Vergleich ist wegen des Zigzag-Look-Aheads ohnehin nicht interpretierbar
# (siehe BERICHT.md 5.4), ihr Drawdown liegt nahe null, und ein
# Konfidenzintervall um eine nicht interpretierbare Groesse waere
# irrefuehrende Praezision. Buy-and-Hold und Datenbasis werden fuer sie
# trotzdem ausgewiesen.
BOOTSTRAP_BOTS = ("t3_supertrend", "volatility_breakout", "volatility_breakout_crypto")
PRIMARY_ATR_WINDOW = 14
TRADING_COST_PCT = 2 * (0.1 + 0.05)  # Gebuehr + Slippage je Entry und Exit - in ALLEN
                                      # betroffenen Bots identisch (0.1 % + 0.05 %)

# ANNAHME (siehe BERICHT.md): ALLOCATION_PCT ist bei elliott_wave,
# elliott_wave_stocks und t3_supertrend in live_params.py NICHT dokumentiert.
# Es wird derselbe Platzhalter (10 %) wie in der Vol-Sizing-Untersuchung
# angenommen, damit die vier Backlog-Untersuchungen untereinander
# vergleichbar bleiben. elliott_wave fuehrt ausserdem kein
# MAX_CONCURRENT_POSITIONS - ebenfalls wie dort der Wert des
# Schwester-Bots (8) angenommen.
ASSUMED_ALLOCATION_PCT = {"elliott_wave": 10.0, "elliott_wave_stocks": 10.0, "t3_supertrend": 10.0}
ASSUMED_MAX_CONCURRENT = {"elliott_wave": 8}

VARIANTS = [STOP_FIXED_STATIC, STOP_FIXED_TRAILING, STOP_ATR_TRAILING]


# ===========================================================================
# Schritt A - Bot-spezifische Vorbereitung (einmalig, teuer)
# ===========================================================================
def prepare():
    """
    Laedt Kursdaten, berechnet alle bot-eigenen Indikatoren/Signale EINMAL
    und legt sie zusammen mit dem ATR je Symbol ab. Die anschliessende
    Variantenrechnung (drei Stop-Regeln) nutzt diese Vorbereitung wieder -
    nur die AUSSTIEGSREGEL unterscheidet sich, alles davor ist identisch.

    Rueckgabe: (prepared_by_symbol, config)
    """
    import live_params as lp
    import multi_symbol_walk_forward as mswf

    cfg = {
        "stop_loss_pct": float(lp.STOP_LOSS_PCT),
        "train_split_ratio": mswf.TRAIN_SPLIT_RATIO,
        "allocation_pct": None,
        "allocation_pct_assumed": BOT in ASSUMED_ALLOCATION_PCT,
        "max_concurrent_positions": None,
        "max_concurrent_assumed": BOT in ASSUMED_MAX_CONCURRENT,
    }
    cfg["allocation_pct"] = (ASSUMED_ALLOCATION_PCT.get(BOT)
                             if BOT in ASSUMED_ALLOCATION_PCT else float(lp.ALLOCATION_PCT))
    cfg["max_concurrent_positions"] = (ASSUMED_MAX_CONCURRENT.get(BOT)
                                       if BOT in ASSUMED_MAX_CONCURRENT
                                       else getattr(lp, "MAX_CONCURRENT_POSITIONS", None))

    prepared = {}

    if BOT in ("elliott_wave", "elliott_wave_stocks"):
        from multi_symbol_optimise import load_all_symbol_data
        from zigzag_indicator import calculate_zigzag
        from elliott_wave_counter import find_impulse_waves, remove_overlapping
        import backtest_elliott as bt

        cfg["kind"] = "elliott"
        cfg["max_hold_bars"] = bt.MAX_HOLD_HOURS
        cfg["deviation_pct"] = lp.DEVIATION_PCT
        cfg["take_profit_fib"] = lp.TAKE_PROFIT_FIB
        cfg["use_take_profit"] = getattr(lp, "USE_TAKE_PROFIT", True)

        for symbol, price_df in load_all_symbol_data().items():
            zigzag = calculate_zigzag(price_df, deviation_pct=cfg["deviation_pct"])
            if len(zigzag) < 6:
                continue
            impulses = find_impulse_waves(zigzag, min_fib_score=0.3)
            if impulses.empty:
                continue
            impulses = remove_overlapping(impulses)
            impulses = impulses[impulses["direction"] == "bearish"]  # Long-only
            if impulses.empty:
                continue
            prepared[symbol] = _arrays(price_df) | {"impulses": impulses, "prices": _price_frame(price_df)}

    elif BOT == "t3_supertrend":
        from multi_symbol_optimise import load_all_symbol_data
        from indicators import compute_indicators
        import backtest_trend as bt

        cfg["kind"] = "t3"
        cfg["t3_fast"] = lp.T3_FAST_LENGTH
        cfg["t3_slow"] = lp.T3_SLOW_LENGTH
        cfg["adx_threshold"] = lp.ADX_THRESHOLD

        all_data = load_all_symbol_data()
        for symbol, price_df in all_data.items():
            data = compute_indicators(price_df, cfg["t3_fast"], cfg["t3_slow"], bt.T3_FACTOR,
                                       bt.DI_LENGTH, bt.ADX_LENGTH, bt.ATR_LENGTH, bt.ATR_MULT)
            prepared[symbol] = _arrays(data) | {
                "prices": _price_frame(data),
                "t3_fast": data["t3_fast"].to_numpy(),
                "t3_slow": data["t3_slow"].to_numpy(),
                "adx": data["adx"].to_numpy(),
                "supertrend_dir": data["supertrend_dir"].to_numpy(),
            }
        cfg["btc_raw"] = all_data.get("BTCUSDT")

    elif BOT in ("volatility_breakout", "volatility_breakout_crypto"):
        from multi_symbol_optimise import load_all_symbol_data
        import backtest_breakout as bt

        cfg["kind"] = "breakout"
        cfg["max_hold_bars"] = getattr(lp, "MAX_HOLD_DAYS", bt.MAX_HOLD_DAYS)
        cfg["warmup"] = bt.WARMUP_PERIOD

        for symbol, entry in load_all_symbol_data().items():
            # Die beiden Geschwister-Bots liefern UNTERSCHIEDLICHE Formen:
            # volatility_breakout (Aktien) gibt (df_ind, entry_cutoff)-Tupel
            # zurueck (Indikatoren auf voller Historie, Trades erst ab
            # entry_cutoff - RECENT_YEARS_ONLY-Behandlung), die Krypto-Version
            # rohe DataFrames ohne Indikatoren.
            if isinstance(entry, tuple):
                df_ind, entry_cutoff = entry
            else:
                df_ind, entry_cutoff = bt.compute_indicators(entry), None
            prepared[symbol] = _arrays(df_ind) | {
                "prices": _price_frame(df_ind),
                "upper": df_ind["bb_upper"].to_numpy(),
                "is_squeeze": df_ind["is_squeeze"].to_numpy(),
                "entry_cutoff": entry_cutoff,
            }

    else:
        raise ValueError(f"Bot ohne festen %-Stop oder unbekannt: {BOT} "
                         f"(siehe stop_inventory.py - nur Bots der Kategorie 'fixed_pct' "
                         f"sind Gegenstand dieser Untersuchung)")

    return prepared, cfg


def _price_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Minimale Kurstabelle je Symbol fuer den Buy-and-Hold-Vergleich."""
    return df[["open_time", "close"]].copy()


def _arrays(df: pd.DataFrame) -> dict:
    """Gemeinsame Kurs-Arrays + ATR fuer ein Symbol. ATR wird auf GENAU dem
    DataFrame berechnet, den der jeweilige Bot auch scannt - damit sind die
    Indizes deckungsgleich und es kann kein Versatz entstehen."""
    high = df["high"].to_numpy(dtype=float)
    low = df["low"].to_numpy(dtype=float)
    close = df["close"].to_numpy(dtype=float)
    return {
        "open_time": df["open_time"].to_numpy(),
        "high": high, "low": low, "close": close,
        "atr": wilder_atr(high, low, close, ATR_WINDOW),
    }


# ===========================================================================
# Schritt B - Trade-Erzeugung je Stop-Variante
# ===========================================================================
def _finish(entry_idx, entry_price, outcome, sym, p, kind, stop_pct, k) -> dict:
    """Baut die Trade-Zeile. `initial_stop_pct` (anfaengliche Stop-Distanz in
    Prozent vom Einstiegskurs) wird mitgefuehrt, weil genau ihre STREUUNG der
    untersuchte Unterschied ist: bei der Baseline ist sie fuer jeden Trade
    identisch, bei der ATR-Variante haengt sie von der Volatilitaet zum
    Einstiegszeitpunkt ab."""
    atr = p["atr"]
    exit_idx = outcome["exit_idx"]
    pnl_pct = (outcome["exit_price"] - entry_price) / entry_price * 100 - TRADING_COST_PCT
    stop = initial_stop_price(kind, entry_price, stop_pct, k, atr[entry_idx])
    return {
        "symbol": sym,
        "entry_time": pd.Timestamp(p["open_time"][entry_idx]),
        "exit_time": pd.Timestamp(p["open_time"][exit_idx]),
        "entry_price": entry_price,
        "exit_price": outcome["exit_price"],
        "result": outcome["result"],
        "pnl_pct": round(pnl_pct, 2),
        "atr_at_entry": float(atr[entry_idx]),
        "initial_stop_pct": round((entry_price - stop) / entry_price * 100, 3),
    }


def collect_trades(prepared: dict, cfg: dict, kind: str, k: float) -> pd.DataFrame:
    """Erzeugt den vollstaendigen Trade-Satz ueber alle Symbole fuer EINE
    Stop-Variante. Die Einstiegs-Logik ist in allen Varianten identisch und
    unveraendert aus dem jeweiligen Bot uebernommen - nur die
    Ausstiegs-Pruefung (simulate_exit) unterscheidet sich."""
    stop_pct = cfg["stop_loss_pct"]
    rows = []

    for sym, p in prepared.items():
        if cfg["kind"] == "elliott":
            rows += _elliott_symbol(sym, p, cfg, kind, stop_pct, k)
        elif cfg["kind"] == "t3":
            rows += _t3_symbol(sym, p, cfg, kind, stop_pct, k)
        else:
            rows += _breakout_symbol(sym, p, cfg, kind, stop_pct, k)

    if not rows:
        return pd.DataFrame()

    trades = pd.DataFrame(rows)
    trades["entry_time"] = pd.to_datetime(trades["entry_time"])
    trades["exit_time"] = pd.to_datetime(trades["exit_time"])

    # BTC-Markt-Regime-Filter - EXAKT so und nur dort, wo ihn die bestehende
    # equity_simulation.py des jeweiligen Bots anwendet (bei t3_supertrend in
    # collect_all_trades). Er wirkt ausschliesslich auf EINSTIEGE und damit in
    # allen drei Varianten gleichermassen.
    if cfg["kind"] == "t3" and cfg.get("btc_raw") is not None:
        from regime_filter import compute_btc_regime, filter_trades_by_regime
        trades = filter_trades_by_regime(trades, compute_btc_regime(cfg["btc_raw"]))

    return trades.sort_values("entry_time").reset_index(drop=True)


def _elliott_symbol(sym, p, cfg, kind, stop_pct, k) -> list:
    """Elliott Wave (Krypto + Aktien): die Einstiege stehen als bereits
    erkannte Impulswellen fest und haengen NICHT von der Ausstiegsregel ab -
    anders als bei den beiden folgenden Zustandsautomaten. Ausstieg:
    Stop, optionales Fibonacci-Kursziel, sonst Zeit-Exit am letzten Balken
    des .head(MAX_HOLD)-Fensters (Original-Konvention)."""
    open_time, rows = p["open_time"], []
    for _, wave in p["impulses"].iterrows():
        entry_time = np.datetime64(pd.Timestamp(wave["end_time"]))
        pos = int(np.searchsorted(open_time, entry_time, side="right")) - 1
        if pos < 0 or pos >= len(open_time) - 1:
            continue

        entry_price = float(wave["wave5"])
        target = (entry_price + abs(wave["wave5"] - wave["wave0"]) * cfg["take_profit_fib"]
                  if cfg["use_take_profit"] else None)

        outcome = simulate_exit(p["high"], p["low"], p["close"], p["atr"], pos, entry_price,
                                 kind, stop_pct, k, cfg["max_hold_bars"], target_price=target,
                                 time_exit_mode="at_last_available")
        if outcome["exit_idx"] is None:
            continue
        rows.append(_finish(pos, entry_price, outcome, sym, p, kind, stop_pct, k))
    return rows


def _t3_symbol(sym, p, cfg, kind, stop_pct, k) -> list:
    """T3/ADX/SuperTrend: Zustandsautomat. Einstieg bei T3-Crossover +
    ADX-Schwelle, Ausstieg bei Stop ODER SuperTrend-Drehung ODER
    T3-Crossunder (letztere beide als 'extra_exit'-Maske). Kein Zeit-Exit -
    eine am Datenende noch offene Position wird wie im Original verworfen."""
    t3f, t3s = p["t3_fast"], p["t3_slow"]
    adx, sdir = p["adx"], p["supertrend_dir"]
    n = len(p["close"])

    prev_f, prev_s = np.roll(t3f, 1), np.roll(t3s, 1)
    prev_dir = np.roll(sdir, 1)
    extra_exit = ((sdir == -1) & (prev_dir == 1)) | ((prev_f >= prev_s) & (t3f < t3s))
    extra_exit[0] = False

    crossed_up = (prev_f <= prev_s) & (t3f > t3s)
    crossed_up[0] = False
    valid = ~(pd.isna(t3f) | pd.isna(t3s) | pd.isna(adx))

    rows, i = [], 1
    while i < n:
        if valid[i] and crossed_up[i] and adx[i] > cfg["adx_threshold"]:
            entry_price = float(p["close"][i])
            outcome = simulate_exit(p["high"], p["low"], p["close"], p["atr"], i, entry_price,
                                     kind, stop_pct, k, max_hold_bars=None,
                                     extra_exit=extra_exit, time_exit_mode="none")
            if outcome["exit_idx"] is None:
                break  # Position bleibt bis Datenende offen -> verworfen (Original-Verhalten)
            rows.append(_finish(i, entry_price, outcome, sym, p, kind, stop_pct, k))
            i = outcome["exit_idx"] + 1
            continue
        i += 1
    return rows


def _breakout_symbol(sym, p, cfg, kind, stop_pct, k) -> list:
    """Volatility Breakout (Aktien + Krypto): Zustandsautomat. Einstieg bei
    'Squeeze gestern UND Schluss ueber oberem Bollinger-Band heute', Ausstieg
    bei Stop oder Zeit-Exit exakt nach MAX_HOLD_DAYS Balken. Reicht die
    Resthistorie fuer den Zeit-Exit nicht, bricht der Scan ab - identisch zum
    Original (`if exit_idx is None: break`)."""
    close, upper, is_squeeze = p["close"], p["upper"], p["is_squeeze"]
    open_time, n = p["open_time"], len(close)
    cutoff = p["entry_cutoff"]

    start_i = cfg["warmup"] + 1
    if cutoff is not None:
        start_i = max(start_i, int((pd.Series(open_time) < cutoff).sum()))

    rows, i = [], start_i
    while i < n:
        if np.isnan(upper[i]) or np.isnan(close[i]):
            i += 1
            continue
        if not (bool(is_squeeze[i - 1]) and close[i] > upper[i]):
            i += 1
            continue

        entry_price = float(close[i])
        outcome = simulate_exit(p["high"], p["low"], close, p["atr"], i, entry_price,
                                 kind, stop_pct, k, cfg["max_hold_bars"],
                                 time_exit_mode="at_max_offset_only")
        if outcome["exit_idx"] is None:
            break
        if cutoff is None or open_time[i] >= np.datetime64(pd.Timestamp(cutoff)):
            rows.append(_finish(i, entry_price, outcome, sym, p, kind, stop_pct, k))
        i = outcome["exit_idx"] + 1
    return rows


# ===========================================================================
# Schritt C - Auswertung
# ===========================================================================
def evaluate(trades: pd.DataFrame, cfg: dict) -> dict:
    """Portfolio-Simulation + Kennzahlen fuer einen Trade-Satz."""
    if trades is None or trades.empty:
        return None
    res = simulate_portfolio(trades, STARTING_CAPITAL, cfg["allocation_pct"] / 100.0,
                              cfg["max_concurrent_positions"])
    total_return = round((res["final_capital"] / STARTING_CAPITAL - 1) * 100, 2)
    max_dd = calculate_max_drawdown(res["equity_curve"], STARTING_CAPITAL)
    stop_dist = trades["initial_stop_pct"]
    return {
        "initial_stop_pct_p10": round(float(stop_dist.quantile(0.10)), 2),
        "initial_stop_pct_median": round(float(stop_dist.median()), 2),
        "initial_stop_pct_p90": round(float(stop_dist.quantile(0.90)), 2),
        "initial_stop_pct_max": round(float(stop_dist.max()), 2),
        "num_trades": int(len(trades)),
        "num_executed": res["num_executed"],
        "num_skipped": res["num_skipped"],
        "total_return_pct": total_return,
        "max_drawdown_pct": max_dd,
        "calmar_ratio": calmar_ratio(total_return, max_dd),
        "win_rate_pct": round(float((trades["pnl_pct"] > 0).mean() * 100), 1),
        "avg_pnl_pct": round(float(trades["pnl_pct"].mean()), 3),
        "worst_trade_pct": round(float(trades["pnl_pct"].min()), 2),
        "best_trade_pct": round(float(trades["pnl_pct"].max()), 2),
        "result_counts": {str(key): int(val) for key, val in trades["result"].value_counts().items()},
    }


def elliott_lookahead_diagnostic(prepared: dict, cfg: dict) -> dict:
    """
    Diagnose NUR fuer die beiden Elliott-Wave-Bots.

    Deren Backtest steigt zum Kurs am WELLENENDE ein (`wave["wave5"]`,
    der Zigzag-Tiefpunkt eines baerischen Impulses). Ein Zigzag-Pivot
    ist aber per Konstruktion erst dann ein Pivot, wenn sich der Kurs
    anschliessend um mindestens `deviation_pct` in die Gegenrichtung
    bewegt hat - der Einstiegskurs ist damit im Backtest ein Tiefpunkt,
    dem RUECKWIRKEND GARANTIERT eine Aufwaertsbewegung von mindestens
    deviation_pct folgt. Fuer einen FESTEN Stop ist dieser bekannte
    Look-Ahead vergleichsweise harmlos (er verschiebt das Niveau aller
    Trades gleichermassen); ein TRAILING-Stop hingegen verwandelt genau
    diese garantierte Bewegung direkt in einen quasi-sicheren Gewinn,
    weil er den Ausstieg an das zwischenzeitliche Hoch koppelt.

    Diese Funktion misst, wie stark die Garantie tatsaechlich greift:
    Anteil der Baseline-Trades, deren hoechster Kurs im Halte-Fenster
    mindestens deviation_pct ueber dem Einstiegskurs lag.

    (Der gleiche Look-Ahead ist im Projekt bereits dokumentiert und fuer
    den LIVE-Pfad behoben worden - forward_test.py nutzt den aktuellen
    Marktpreis zum Erkennungszeitpunkt statt des historischen
    Wellenend-Kurses. Der BACKTEST behaelt die Wellenend-Konvention.)
    """
    total = 0
    reached = 0
    mfe_values = []
    for _, p in prepared.items():
        high, open_time = p["high"], p["open_time"]
        n = len(high)
        for _, wave in p["impulses"].iterrows():
            entry_time = np.datetime64(pd.Timestamp(wave["end_time"]))
            pos = int(np.searchsorted(open_time, entry_time, side="right")) - 1
            if pos < 0 or pos >= n - 1:
                continue
            hi = min(pos + cfg["max_hold_bars"], n - 1)
            entry_price = float(wave["wave5"])
            if entry_price <= 0:
                continue
            mfe = float(np.max(high[pos + 1:hi + 1])) / entry_price - 1
            mfe_values.append(mfe * 100)
            total += 1
            if mfe * 100 >= cfg["deviation_pct"]:
                reached += 1

    if total == 0:
        return None
    return {
        "num_trades": total,
        "deviation_pct": cfg["deviation_pct"],
        "share_reaching_deviation_pct": round(reached / total * 100, 1),
        "median_max_favourable_excursion_pct": round(float(np.median(mfe_values)), 2),
        "note": ("Anteil der Trades, deren Hoechstkurs im Halte-Fenster mindestens "
                 "deviation_pct ueber dem Einstiegskurs lag - Mass fuer den "
                 "zigzag-bedingten Look-Ahead im Einstiegskurs des Backtests."),
    }


def slice_period(trades: pd.DataFrame, lo, hi, include_hi: bool) -> pd.DataFrame:
    if trades.empty:
        return trades
    mask = trades["entry_time"] >= lo
    mask &= (trades["entry_time"] <= hi) if include_hi else (trades["entry_time"] < hi)
    return trades[mask]


def main():
    prepared, cfg = prepare()
    if not prepared:
        json.dump({"bot": BOT, "error": "keine Kursdaten/Signale gefunden"},
                  open(os.path.join(RESULTS_DIR, f"{BOT}_atr{ATR_WINDOW}.json"), "w"), indent=2)
        print(f"{BOT}: keine Daten - Abbruch.")
        return

    # --- Baseline zuerst: sie definiert Split-Zeitpunkte UND den Massstab
    #     fuer die Kalibrierung des ATR-Multiplikators.
    baseline = collect_trades(prepared, cfg, STOP_FIXED_STATIC, k=None)
    if baseline.empty:
        print(f"{BOT}: Baseline ohne Trades - Abbruch.")
        return

    entry_min, entry_max = baseline["entry_time"].min(), baseline["entry_time"].max()
    split_time = entry_min + (entry_max - entry_min) * cfg["train_split_ratio"]
    in_sample_baseline = baseline[baseline["entry_time"] < split_time]

    # --- ATR-Multiplikator k: EINMALIG aus den IN-SAMPLE-Baseline-Trades
    #     kalibriert und danach unveraendert fuer Out-of-Sample und alle
    #     Stabilitaetsfenster verwendet (siehe BERICHT.md, Annahme 3).
    k = calibrate_atr_multiplier(in_sample_baseline["atr_at_entry"].to_numpy(),
                                  in_sample_baseline["entry_price"].to_numpy(),
                                  cfg["stop_loss_pct"])
    k_oos_hypothetical = calibrate_atr_multiplier(
        baseline[baseline["entry_time"] >= split_time]["atr_at_entry"].to_numpy(),
        baseline[baseline["entry_time"] >= split_time]["entry_price"].to_numpy(),
        cfg["stop_loss_pct"])

    variant_trades = {
        STOP_FIXED_STATIC: baseline,
        STOP_FIXED_TRAILING: collect_trades(prepared, cfg, STOP_FIXED_TRAILING, k=None),
        STOP_ATR_TRAILING: collect_trades(prepared, cfg, STOP_ATR_TRAILING, k=k),
    }

    def all_variants(lo, hi, include_hi=False) -> dict:
        return {v: evaluate(slice_period(t, lo, hi, include_hi), cfg)
                for v, t in variant_trades.items()}

    periods = {
        "full": all_variants(entry_min, entry_max, include_hi=True),
        "in_sample": all_variants(entry_min, split_time),
        "out_of_sample": all_variants(split_time, entry_max, include_hi=True),
    }

    # Walk-Forward-Stabilitaet: 4 gleich lange, chronologische Fenster ueber
    # die GESAMTE Baseline-Trade-Historie (identische Fenstergrenzen fuer
    # alle drei Varianten).
    edges = pd.date_range(entry_min, entry_max, periods=NUM_STABILITY_WINDOWS + 1)
    stability = []
    for i in range(NUM_STABILITY_WINDOWS):
        last = i == NUM_STABILITY_WINDOWS - 1
        stability.append({
            "window_index": i + 1, "start": str(edges[i].date()), "end": str(edges[i + 1].date()),
            "variants": all_variants(edges[i], edges[i + 1], include_hi=last),
        })

    # Episoden-Aufschluesselung nach Kalenderjahr (Lehre aus der
    # Trend-Overlay-Untersuchung: ein Effekt, der nur aus EINER Episode
    # stammt, ist kein robustes Ergebnis).
    yearly = []
    for year in range(int(entry_min.year), int(entry_max.year) + 1):
        lo = pd.Timestamp(year=year, month=1, day=1)
        hi = pd.Timestamp(year=year + 1, month=1, day=1)
        entry = {"year": year, "variants": all_variants(lo, hi)}
        if entry["variants"][STOP_FIXED_STATIC] is not None:
            yearly.append(entry)

    # ---- Entscheidungsgrundlage (Nachtrag) --------------------------------
    price_by_symbol = {sym: p["prices"] for sym, p in prepared.items()}
    period_bounds = {
        "full": (entry_min, entry_max, True),
        "in_sample": (entry_min, split_time, False),
        "out_of_sample": (split_time, entry_max, True),
    }
    alloc_frac = cfg["allocation_pct"] / 100.0

    bh = {name: db.buy_and_hold_window(price_by_symbol, lo, hi, STARTING_CAPITAL)
          for name, (lo, hi, _) in period_bounds.items()}

    data_basis = {
        "symbols_with_trades": int(baseline["symbol"].nunique()),
        "symbols_loaded": len(prepared),
        "bar_interval": {"elliott_wave": "1h", "t3_supertrend": "4h"}.get(BOT, "1d"),
        "first_entry": str(entry_min.date()),
        "last_exit": str(max(t["exit_time"].max() for t in variant_trades.values()).date()),
        "years_covered": round((baseline["exit_time"].max() - entry_min).days / 365.25, 2),
        "trades_per_period": {
            name: {v: {"found": periods[name][v]["num_trades"],
                        "executed": periods[name][v]["num_executed"],
                        "skipped": periods[name][v]["num_skipped"]}
                   for v in VARIANTS if periods[name][v]}
            for name in periods
        },
    }

    # Nur im Hauptlauf (ATR-14). Der Robustheitslauf mit ATR-22 vergleicht die
    # Fensterwahl und braucht dieselbe Unsicherheitsrechnung nicht noch einmal;
    # Buy-and-Hold und Datenbasis haengen ohnehin nicht vom ATR-Fenster ab.
    tie_order, bootstrap_results = {}, {}
    if BOT in BOOTSTRAP_BOTS and ATR_WINDOW == PRIMARY_ATR_WINDOW:
        comparisons = [(STOP_FIXED_TRAILING, STOP_FIXED_STATIC),
                       (STOP_ATR_TRAILING, STOP_FIXED_STATIC),
                       (STOP_ATR_TRAILING, STOP_FIXED_TRAILING)]
        for name, (lo, hi, include_hi) in period_bounds.items():
            sliced = {v: slice_period(t, lo, hi, include_hi) for v, t in variant_trades.items()}
            tie_order[name] = db.tie_order_sensitivity(
                sliced, alloc_frac, cfg["max_concurrent_positions"], STARTING_CAPITAL,
                TIE_ORDER_PERMUTATIONS, BOOTSTRAP_SEED)
            bootstrap_results[name] = db.block_bootstrap(
                sliced, alloc_frac, cfg["max_concurrent_positions"], STARTING_CAPITAL,
                BOOTSTRAP_REPLICATES, BOOTSTRAP_BLOCK_MONTHS, BOOTSTRAP_SEED, comparisons)

    output = {
        "bot": BOT,
        "atr_window_bars": ATR_WINDOW,
        "data_basis": data_basis,
        "buy_and_hold": bh,
        "tie_order_sensitivity": tie_order,
        "bootstrap": bootstrap_results,
        "assumptions": {
            "stop_loss_pct_baseline": cfg["stop_loss_pct"],
            "atr_multiplier_k": round(k, 4) if k else None,
            "atr_multiplier_k_hypothetical_oos": round(k_oos_hypothetical, 4) if k_oos_hypothetical else None,
            "k_calibrated_on": "in_sample_baseline_entries (median)",
            "allocation_pct": cfg["allocation_pct"],
            "allocation_pct_assumed": cfg["allocation_pct_assumed"],
            "max_concurrent_positions": cfg["max_concurrent_positions"],
            "max_concurrent_assumed": cfg["max_concurrent_assumed"],
            "train_split_ratio": cfg["train_split_ratio"],
            "starting_capital": STARTING_CAPITAL,
            "num_stability_windows": NUM_STABILITY_WINDOWS,
            "bootstrap_replicates": BOOTSTRAP_REPLICATES if BOT in BOOTSTRAP_BOTS else None,
            "bootstrap_block_months": BOOTSTRAP_BLOCK_MONTHS,
            "bootstrap_seed": BOOTSTRAP_SEED,
            "tie_order_permutations": TIE_ORDER_PERMUTATIONS if BOT in BOOTSTRAP_BOTS else None,
            "split_time": str(split_time),
        },
        "trade_counts": {v: int(len(t)) for v, t in variant_trades.items()},
        "periods": periods,
        "stability_windows": stability,
        "yearly": yearly,
    }

    if cfg["kind"] == "elliott":
        output["elliott_lookahead_diagnostic"] = elliott_lookahead_diagnostic(prepared, cfg)

    out_path = os.path.join(RESULTS_DIR, f"{BOT}_atr{ATR_WINDOW}.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"{BOT} (ATR-{ATR_WINDOW}): k={k:.3f}  |  Trades "
          f"Baseline {len(baseline)} / Fix-Trailing {len(variant_trades[STOP_FIXED_TRAILING])} / "
          f"ATR-Trailing {len(variant_trades[STOP_ATR_TRAILING])}")
    for name in ("in_sample", "out_of_sample"):
        row = periods[name]
        print(f"  {name:<14} Rendite  fix {row[STOP_FIXED_STATIC]['total_return_pct']:>9.2f}% | "
              f"fix-trail {row[STOP_FIXED_TRAILING]['total_return_pct']:>9.2f}% | "
              f"ATR-trail {row[STOP_ATR_TRAILING]['total_return_pct']:>9.2f}%")
        print(f"  {'':<14} Drawdown fix {row[STOP_FIXED_STATIC]['max_drawdown_pct']:>9.2f}% | "
              f"fix-trail {row[STOP_FIXED_TRAILING]['max_drawdown_pct']:>9.2f}% | "
              f"ATR-trail {row[STOP_ATR_TRAILING]['max_drawdown_pct']:>9.2f}%")
    if bh.get("full"):
        print(f"  Buy-and-Hold     gesamt {bh['full']['total_return_pct']:>8.2f}% / "
              f"DD {bh['full']['max_drawdown_pct']:>7.2f}%   |   OOS "
              f"{bh['out_of_sample']['total_return_pct']:>8.2f}% / "
              f"DD {bh['out_of_sample']['max_drawdown_pct']:>7.2f}%")
    if bootstrap_results.get("full") and "error" not in bootstrap_results["full"]:
        for name in ("full", "out_of_sample"):
            for key, diff in bootstrap_results[name]["differences"].items():
                c, d = diff["calmar_ratio"], diff["max_drawdown_pct"]
                print(f"  BS {name:<14} {key:<38} Calmar P(>0)={c['share_above_zero_pct']:>5.1f}%  "
                      f"DD P(>0)={d['share_above_zero_pct']:>5.1f}%")
    print(f"  Ergebnis gespeichert: {out_path}")


if __name__ == "__main__":
    main()

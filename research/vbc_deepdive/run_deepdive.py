"""
Vertiefungsstudie volatility_breakout_crypto: Vol-Sizing x ATR-Trailing-Stop
=================================================================================
Untersucht die INTERAKTION zweier bereits definierter Mechanismen - es wird
KEIN Parameter neu gesucht. ATR-Fenster (14) und Vol-Fenster (90 Balken)
werden unverändert aus den beiden Vorgänger-Studien übernommen.

WICHTIG - reine Backtest-Untersuchung: liest NUR aus
strategies/volatility_breakout_crypto/ (live_params.py, equity_simulation.py,
multi_symbol_optimise.py, backtest_breakout.py) und schreibt ausschliesslich
nach research/vbc_deepdive/results/. Keine Live-Datei wird verändert.

Nutzung:
    python3 run_deepdive.py
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

from vbc_core import (
    wilder_atr, calibrate_atr_multiplier, simulate_exit, initial_stop_price,
    compute_realized_volatility, compute_inverse_vol_weights,
    simulate_weighted_portfolio, calculate_max_drawdown, calmar_ratio,
    VARIANTS, VARIANT_BASELINE, VARIANT_VOL_SIZING, VARIANT_TRAILING, VARIANT_COMBINED,
    USES_TRAILING, USES_VOL_WEIGHTS, STOP_FIXED_STATIC, STOP_ATR_TRAILING,
)

BOT = "volatility_breakout_crypto"
STRATEGY_DIR = os.path.join(_REPO_ROOT, "strategies", BOT)
sys.path.insert(0, STRATEGY_DIR)
sys.path.insert(0, os.path.join(_REPO_ROOT, "shared"))

RESULTS_DIR = os.path.join(_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# --- Unveränderte Übernahmen aus den beiden Vorgänger-Studien -------------
ATR_WINDOW = 14      # research/trailing_stops - Wilder-Standard, im Projekt bereits fuer ADX/DI genutzt
VOL_WINDOW = 90      # research/volatility_scaled_sizing - 90 Tagesbalken (dieser Bot laeuft auf 1d)
CLIP_FACTOR = 4.0    # research/volatility_scaled_sizing - Ausreisser-Clip der inversen Vol-Gewichte
NUM_STABILITY_WINDOWS = 4
STARTING_CAPITAL = 10_000.0
TRADING_COST_PCT = 2 * (0.1 + 0.05)   # Gebuehr + Slippage je Entry und Exit, wie im Bot


# ===========================================================================
# Datenaufbereitung
# ===========================================================================
def load_symbols() -> dict:
    """Lädt die Kursdaten exakt wie der Bot selbst (multi_symbol_optimise.
    load_all_symbol_data) und hängt ATR sowie realisierte Volatilität an -
    beide auf GENAU dem DataFrame, den der Bot auch scannt, damit die
    Indizes deckungsgleich sind."""
    from multi_symbol_optimise import load_all_symbol_data
    import backtest_breakout as bt

    prepared = {}
    for symbol, price_df in load_all_symbol_data().items():
        df = bt.compute_indicators(price_df)
        high = df["high"].to_numpy(dtype=float)
        low = df["low"].to_numpy(dtype=float)
        close = df["close"].to_numpy(dtype=float)
        prepared[symbol] = {
            "open_time": df["open_time"].to_numpy(),
            "high": high, "low": low, "close": close,
            "upper": df["bb_upper"].to_numpy(),
            "is_squeeze": df["is_squeeze"].to_numpy(),
            "atr": wilder_atr(high, low, close, ATR_WINDOW),
            "vol": compute_realized_volatility(close, VOL_WINDOW),
        }
    return prepared, bt.WARMUP_PERIOD


def collect_trades(prepared: dict, warmup: int, stop_kind: str, stop_pct: float,
                    k, max_hold: int) -> pd.DataFrame:
    """
    Erzeugt den vollständigen Trade-Satz über alle Symbole für EINE
    Stop-Regel. Die Einstiegs-Logik ist unverändert aus
    strategies/volatility_breakout_crypto/backtest_breakout.py::run_backtest
    übernommen (Squeeze gestern UND Schluss über oberem Bollinger-Band
    heute, kein Pyramiding: der nächste Scan startet erst nach dem Ausstieg).
    Nur die Ausstiegs-Prüfung ist ausgetauscht.
    """
    rows = []
    for sym, p in prepared.items():
        close, upper, is_squeeze = p["close"], p["upper"], p["is_squeeze"]
        n, i = len(close), warmup + 1
        while i < n:
            if np.isnan(upper[i]) or np.isnan(close[i]):
                i += 1
                continue
            if not (bool(is_squeeze[i - 1]) and close[i] > upper[i]):
                i += 1
                continue

            entry_price = float(close[i])
            outcome = simulate_exit(p["high"], p["low"], close, p["atr"], i, entry_price,
                                     stop_kind, stop_pct, k, max_hold)
            if outcome["exit_idx"] is None:
                break   # Resthistorie reicht nicht - Symbol-Scan beenden (Original-Verhalten)

            exit_idx = outcome["exit_idx"]
            stop = initial_stop_price(stop_kind, entry_price, stop_pct, k, p["atr"][i])
            rows.append({
                "symbol": sym,
                "entry_time": pd.Timestamp(p["open_time"][i]),
                "exit_time": pd.Timestamp(p["open_time"][exit_idx]),
                "entry_price": entry_price,
                "exit_price": outcome["exit_price"],
                "result": outcome["result"],
                "pnl_pct": round((outcome["exit_price"] - entry_price) / entry_price * 100
                                 - TRADING_COST_PCT, 2),
                "atr_at_entry": float(p["atr"][i]),
                "vol_at_entry": float(p["vol"][i]) if np.isfinite(p["vol"][i]) else np.nan,
                "initial_stop_pct": round((entry_price - stop) / entry_price * 100, 3),
            })
            i = exit_idx + 1
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values("entry_time").reset_index(drop=True)


# ===========================================================================
# Auswertung
# ===========================================================================
def weights_for(trades: pd.DataFrame, use_vol: bool) -> pd.Series:
    """Inverse-Vol-Gewichte (Mittelwert exakt 1,0 INNERHALB des übergebenen
    Trade-Satzes) oder neutrale Gewichte. Die Normalisierung erfolgt immer
    auf genau der Menge, die auch simuliert wird - so fliesst keine
    Information zwischen In-Sample und Out-of-Sample (Konvention der
    Vol-Sizing-Studie)."""
    if not use_vol:
        return pd.Series(1.0, index=trades.index)
    return compute_inverse_vol_weights(trades["vol_at_entry"], CLIP_FACTOR)


def evaluate(trades: pd.DataFrame, use_vol: bool, cfg: dict) -> dict:
    if trades is None or trades.empty:
        return None
    weights = weights_for(trades, use_vol)
    res = simulate_weighted_portfolio(trades, STARTING_CAPITAL, cfg["allocation_pct"] / 100.0,
                                       weights, cfg["max_concurrent"])
    total_return = round((res["final_capital"] / STARTING_CAPITAL - 1) * 100, 2)
    max_dd = calculate_max_drawdown(res["equity_curve"], STARTING_CAPITAL)
    return {
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
        "mean_weight": round(float(weights.mean()), 4),
    }


def all_four(sets: dict, cfg: dict, lo=None, hi=None, include_hi=False) -> dict:
    """Wertet alle vier Varianten auf demselben Zeitfenster aus."""
    out = {}
    for variant in VARIANTS:
        trades = sets[USES_TRAILING[variant]]
        if lo is not None:
            mask = trades["entry_time"] >= lo
            mask &= (trades["entry_time"] <= hi) if include_hi else (trades["entry_time"] < hi)
            trades = trades[mask]
        out[variant] = evaluate(trades, USES_VOL_WEIGHTS[variant], cfg)
    return out


# ===========================================================================
# Mechanismus-Unabhängigkeit (Frage 3 der Aufgabenstellung)
# ===========================================================================
def overlap_analysis(static_trades: pd.DataFrame, trailing_trades: pd.DataFrame) -> dict:
    """
    Stammen der Vol-Sizing-Vorteil und der Trailing-Stop-Vorteil aus
    DENSELBEN Trades oder aus unterschiedlichen?

    Zwei Beitrags-Masse, beide in Prozentpunkten PnL je Trade:
      * Vol-Sizing-Beitrag  = (Gewicht - 1) * PnL des Trades. Positiv, wenn
        ein Gewinner übergewichtet oder ein Verlierer untergewichtet wurde.
        Auf dem Trade-Satz mit FESTEM Stop berechnet (dort wirkt Vol-Sizing
        in Variante B).
      * Trailing-Beitrag    = PnL(Trailing) - PnL(fester Stop), für Trades,
        die in BEIDEN Sätzen mit gleichem Symbol und gleichem Einstiegs-
        zeitpunkt vorkommen.

    Bewusst als PnL-Prozentpunkte und nicht in Kapitaleinheiten: die
    Kapitalwirkung eines Trades hängt vom Pfad (verfügbares Kapital,
    Positionslimit) ab und liesse sich nicht sauber einem einzelnen Trade
    zurechnen. Die Prozentpunkt-Betrachtung ist die konservativere, weil sie
    keine Zurechnung behauptet, die die Simulation nicht hergibt.

    Die Gewichte werden hier über den GESAMTZEITRAUM normalisiert (nicht je
    Periode), weil die Frage lautet, welche Trades den Gesamteffekt tragen -
    dafür muss der Mechanismus über alle Trades hinweg derselbe sein.
    """
    static = static_trades.copy()
    static["vol_weight"] = compute_inverse_vol_weights(static["vol_at_entry"], CLIP_FACTOR)

    # Wie aehnlich sind die beiden Volatilitaets-MASSE ueberhaupt? Der
    # ATR-Stop misst ueber die True Range (Hoch/Tief/Vorschluss, 14 Balken),
    # das Vol-Sizing ueber die Standardabweichung der Schluss-zu-Schluss-
    # Log-Returns (90 Balken). Beide heissen "Volatilitaet", sind aber weder
    # dasselbe Fenster noch dasselbe Mass - wie stark sie zusammenhaengen,
    # ist die Vorfrage zur Unabhaengigkeit der beiden Mechanismen.
    atr_pct = static["atr_at_entry"] / static["entry_price"]
    estimator_corr = float(atr_pct.corr(static["vol_at_entry"]))
    # Rangkorrelation als Pearson-Korrelation der Raenge berechnet - pandas'
    # method="spearman" braucht scipy, das im Projekt nicht installiert ist
    # und fuer eine Backtest-Studie auch nicht neu eingefuehrt werden soll.
    estimator_rank_corr = float(atr_pct.rank().corr(static["vol_at_entry"].rank()))
    static["vol_contribution"] = (static["vol_weight"] - 1.0) * static["pnl_pct"]

    key = ["symbol", "entry_time"]
    merged = static.merge(trailing_trades[key + ["pnl_pct", "result"]], on=key,
                           how="inner", suffixes=("", "_trail"))
    merged["trailing_contribution"] = merged["pnl_pct_trail"] - merged["pnl_pct"]

    matched = len(merged)
    both_positive = int(((merged["vol_contribution"] > 0) & (merged["trailing_contribution"] > 0)).sum())
    both_negative = int(((merged["vol_contribution"] < 0) & (merged["trailing_contribution"] < 0)).sum())
    opposite = int((((merged["vol_contribution"] > 0) & (merged["trailing_contribution"] < 0)) |
                    ((merged["vol_contribution"] < 0) & (merged["trailing_contribution"] > 0))).sum())

    corr = (float(merged["vol_contribution"].corr(merged["trailing_contribution"]))
            if matched > 2 else None)

    top_n = min(20, matched)
    top_vol = set(merged["vol_contribution"].nlargest(top_n).index)
    top_trail = set(merged["trailing_contribution"].nlargest(top_n).index)
    top_overlap = len(top_vol & top_trail)
    # Erwartungswert bei Unabhängigkeit: top_n^2 / matched
    expected_overlap = round(top_n * top_n / matched, 2) if matched else None

    quarterly = merged.copy()
    quarterly["quarter"] = quarterly["entry_time"].dt.to_period("Q").astype(str)
    by_quarter = quarterly.groupby("quarter")[["vol_contribution", "trailing_contribution"]].sum()
    quarter_corr = (float(by_quarter["vol_contribution"].corr(by_quarter["trailing_contribution"]))
                    if len(by_quarter) > 2 else None)

    def top_quarter(column):
        positive = by_quarter[by_quarter[column] > 0][column]
        if positive.empty:
            return None
        total = float(positive.sum())
        best = positive.idxmax()
        return {"quarter": best, "value_pp": round(float(positive.loc[best]), 2),
                "share_of_positive_pct": round(float(positive.loc[best]) / total * 100, 1)}

    return {
        "atr_vs_realized_vol_correlation": round(estimator_corr, 4),
        "atr_vs_realized_vol_rank_correlation": round(estimator_rank_corr, 4),
        "static_trades": int(len(static_trades)),
        "trailing_trades": int(len(trailing_trades)),
        "matched_trades": matched,
        "only_in_static": int(len(static_trades) - matched),
        "only_in_trailing": int(len(trailing_trades) - matched),
        "sum_vol_contribution_pp": round(float(merged["vol_contribution"].sum()), 2),
        "sum_trailing_contribution_pp": round(float(merged["trailing_contribution"].sum()), 2),
        "trade_level_correlation": round(corr, 4) if corr is not None else None,
        "quarter_level_correlation": round(quarter_corr, 4) if quarter_corr is not None else None,
        "both_helped": both_positive,
        "both_hurt": both_negative,
        "opposite_direction": opposite,
        "top_n": top_n,
        "top_n_overlap": top_overlap,
        "top_n_overlap_expected_if_independent": expected_overlap,
        "dominant_quarter_vol": top_quarter("vol_contribution"),
        "dominant_quarter_trailing": top_quarter("trailing_contribution"),
        "by_quarter": {q: {"vol_contribution_pp": round(float(row["vol_contribution"]), 2),
                            "trailing_contribution_pp": round(float(row["trailing_contribution"]), 2)}
                       for q, row in by_quarter.iterrows()},
    }


def quarterly_concentration(quarters: list) -> dict:
    """
    Episoden-Robustheit (Frage 2 - laut Aufgabenstellung die wichtigste).

    Für jede Variante gegen die Baseline: wie verteilt sich der
    Renditeunterschied über die Quartale? Gemessen wird
      * die Richtungsbilanz (in wie vielen Quartalen besser/schlechter),
      * der Anteil des grössten Einzelquartals an der Summe der
        ABSOLUTBETRÄGE aller Quartalsdifferenzen - so heben sich
        gegenläufige Quartale nicht künstlich auf und ein dominantes
        Quartal wird sichtbar.

    Schwelle > 60 % = "durch eine Einzelepisode getrieben" - dieselbe
    selbst gewählte Heuristik wie in der Trailing-Stop-Untersuchung, damit
    die Befunde vergleichbar bleiben. Zusätzlich wird der Anteil der drei
    grössten Quartale ausgewiesen, weil eine Konzentration auf wenige
    Episoden auch dann vorliegen kann, wenn kein EINZELNES Quartal die
    60 %-Schwelle reisst.
    """
    out = {}
    for variant in VARIANTS:
        if variant == VARIANT_BASELINE:
            continue
        diffs = {}
        for q in quarters:
            base, other = q["variants"][VARIANT_BASELINE], q["variants"][variant]
            if base is None or other is None:
                continue
            diffs[q["quarter"]] = other["total_return_pct"] - base["total_return_pct"]
        if not diffs:
            continue
        total_abs = sum(abs(d) for d in diffs.values())
        ordered = sorted(diffs.items(), key=lambda kv: abs(kv[1]), reverse=True)
        out[variant] = {
            "quarters_total": len(diffs),
            "quarters_better": sum(1 for d in diffs.values() if d > 0.05),
            "quarters_worse": sum(1 for d in diffs.values() if d < -0.05),
            "quarters_neutral": sum(1 for d in diffs.values() if abs(d) <= 0.05),
            "dominant_quarter": ordered[0][0],
            "dominant_quarter_diff_pp": round(ordered[0][1], 2),
            "dominant_quarter_share_pct": round(abs(ordered[0][1]) / total_abs * 100, 1),
            "top3_share_pct": round(sum(abs(d) for _, d in ordered[:3]) / total_abs * 100, 1),
            "driven_by_single_episode": abs(ordered[0][1]) / total_abs * 100 > 60.0,
        }
    return out


def conditional_structure(quarters: list) -> dict:
    """
    Hängt der Nutzen eines Mechanismus davon ab, wie gut die Baseline im
    selben Quartal lief?

    Berechnet wird die Korrelation zwischen der QUARTALSRENDITE DER BASELINE
    und der Differenz (Variante - Baseline) desselben Quartals. Eine stark
    NEGATIVE Korrelation bedeutet: der Mechanismus hilft, wenn die Baseline
    verliert, und kostet, wenn sie gewinnt - das Profil einer
    Varianzreduktion (Versicherung), nicht das eines zusätzlichen Edges.

    Zusätzlich getrennt ausgewiesen: mittlere Differenz in Quartalen mit
    negativer und mit positiver Baseline-Rendite. Das ist dieselbe Aussage
    ohne Korrelationsannahmen und daher der robustere der beiden Werte.
    """
    out = {}
    base_returns = pd.Series([q["variants"][VARIANT_BASELINE]["total_return_pct"]
                              for q in quarters if q["variants"][VARIANT_BASELINE]])
    for variant in VARIANTS:
        if variant == VARIANT_BASELINE:
            continue
        diffs = pd.Series([q["variants"][variant]["total_return_pct"]
                           - q["variants"][VARIANT_BASELINE]["total_return_pct"]
                           for q in quarters
                           if q["variants"][VARIANT_BASELINE] and q["variants"][variant]])
        if len(diffs) != len(base_returns) or len(diffs) < 3:
            continue
        down, up = base_returns < 0, base_returns > 0
        out[variant] = {
            "correlation_with_baseline_return": round(float(base_returns.corr(diffs)), 4),
            "quarters_baseline_negative": int(down.sum()),
            "mean_diff_when_baseline_negative_pp": round(float(diffs[down].mean()), 2),
            "better_share_when_baseline_negative_pct": round(float((diffs[down] > 0).mean() * 100), 1),
            "quarters_baseline_positive": int(up.sum()),
            "mean_diff_when_baseline_positive_pp": round(float(diffs[up].mean()), 2),
            "better_share_when_baseline_positive_pct": round(float((diffs[up] > 0).mean() * 100), 1),
        }
    return out


def additivity(periods: dict) -> dict:
    """
    Wirken die beiden Mechanismen additiv, neutral oder gegenläufig
    (Frage 1 der Aufgabenstellung)?

    Getrennt für Rendite und Drawdown, weil beide unterschiedlich
    aggregieren:
      * RENDITE additiv in LOG-Raum - Renditen verketten multiplikativ, eine
        Addition der Prozentwerte wäre bei diesen Grössenordnungen schlicht
        falsch. Erwartung bei Additivität:
        ln(1+r_kombiniert) = ln(1+r_basis) + [ln(1+r_vol) - ln(1+r_basis)]
                                           + [ln(1+r_trail) - ln(1+r_basis)]
      * DRAWDOWN additiv in Prozentpunkten - der Max Drawdown ist keine
        verkettete Grösse, sondern ein einzelner Extremwert.

    Die Differenz zwischen Erwartung und tatsächlichem kombinierten Ergebnis
    ist das eigentliche Interaktionsmass: ~0 = neutral/additiv, deutlich
    schlechter als erwartet = die Mechanismen überlagern sich (sie schützen
    vor DENSELBEN Ereignissen und der zweite hat nichts mehr zu tun).
    """
    out = {}
    for name, row in periods.items():
        base, vol, trail, comb = (row[VARIANT_BASELINE], row[VARIANT_VOL_SIZING],
                                  row[VARIANT_TRAILING], row[VARIANT_COMBINED])
        if not all((base, vol, trail, comb)):
            continue

        def log_r(v):
            return float(np.log1p(v["total_return_pct"] / 100.0))

        expected_log = log_r(base) + (log_r(vol) - log_r(base)) + (log_r(trail) - log_r(base))
        expected_return = round((np.expm1(expected_log)) * 100, 2)
        expected_dd = round(base["max_drawdown_pct"]
                            + (vol["max_drawdown_pct"] - base["max_drawdown_pct"])
                            + (trail["max_drawdown_pct"] - base["max_drawdown_pct"]), 2)
        best_single = max(vol["calmar_ratio"], trail["calmar_ratio"])

        out[name] = {
            "return_expected_if_additive_pct": expected_return,
            "return_actual_pct": comb["total_return_pct"],
            "return_interaction_pp": round(comb["total_return_pct"] - expected_return, 2),
            "drawdown_expected_if_additive_pct": expected_dd,
            "drawdown_actual_pct": comb["max_drawdown_pct"],
            "drawdown_interaction_pp": round(comb["max_drawdown_pct"] - expected_dd, 2),
            "calmar_best_single": best_single,
            "calmar_combined": comb["calmar_ratio"],
            "combined_beats_best_single": (comb["calmar_ratio"] is not None
                                           and best_single is not None
                                           and comb["calmar_ratio"] > best_single),
        }
    return out


# ===========================================================================
def main():
    import live_params as lp
    import multi_symbol_walk_forward as mswf

    cfg = {
        "allocation_pct": float(lp.ALLOCATION_PCT),
        "max_concurrent": lp.MAX_CONCURRENT_POSITIONS,
        "stop_loss_pct": float(lp.STOP_LOSS_PCT),
        "max_hold": int(lp.MAX_HOLD_DAYS),
        "train_split_ratio": mswf.TRAIN_SPLIT_RATIO,
    }

    prepared, warmup = load_symbols()
    static = collect_trades(prepared, warmup, STOP_FIXED_STATIC, cfg["stop_loss_pct"],
                             None, cfg["max_hold"])

    entry_min, entry_max = static["entry_time"].min(), static["entry_time"].max()
    split_time = entry_min + (entry_max - entry_min) * cfg["train_split_ratio"]

    # ATR-Multiplikator: einmalig auf den In-Sample-Baseline-Trades kalibriert,
    # unverändert aus der Trailing-Stop-Studie übernommen.
    is_static = static[static["entry_time"] < split_time]
    k = calibrate_atr_multiplier(is_static["atr_at_entry"].to_numpy(),
                                  is_static["entry_price"].to_numpy(), cfg["stop_loss_pct"])

    trailing = collect_trades(prepared, warmup, STOP_ATR_TRAILING, cfg["stop_loss_pct"],
                               k, cfg["max_hold"])
    sets = {False: static, True: trailing}

    periods = {
        "full": all_four(sets, cfg, entry_min, entry_max, include_hi=True),
        "in_sample": all_four(sets, cfg, entry_min, split_time),
        "out_of_sample": all_four(sets, cfg, split_time, entry_max, include_hi=True),
    }

    edges = pd.date_range(entry_min, entry_max, periods=NUM_STABILITY_WINDOWS + 1)
    stability = [{
        "window_index": i + 1, "start": str(edges[i].date()), "end": str(edges[i + 1].date()),
        "variants": all_four(sets, cfg, edges[i], edges[i + 1],
                              include_hi=(i == NUM_STABILITY_WINDOWS - 1)),
    } for i in range(NUM_STABILITY_WINDOWS)]

    # Quartalsweise Episoden-Aufschlüsselung (Frage 2 - die laut
    # Aufgabenstellung wichtigste). Jedes Quartal wird als eigenständige
    # Simulation ab 10.000 gerechnet, damit die Quartale untereinander
    # vergleichbar sind und nicht vom Kapitalstand des Vorquartals abhängen.
    quarters = []
    for period in sorted(static["entry_time"].dt.to_period("Q").unique()):
        lo = period.start_time
        hi = period.end_time
        quarters.append({"quarter": str(period),
                          "variants": all_four(sets, cfg, lo, hi, include_hi=True)})

    output = {
        "bot": BOT,
        "assumptions": {
            "atr_window_bars": ATR_WINDOW,
            "vol_window_bars": VOL_WINDOW,
            "clip_factor": CLIP_FACTOR,
            "atr_multiplier_k": round(k, 4),
            "k_calibrated_on": "in_sample_baseline_entries (median)",
            "weights_normalised": "mean 1.0 within each evaluated period",
            "stop_loss_pct_baseline": cfg["stop_loss_pct"],
            "max_hold_days": cfg["max_hold"],
            "allocation_pct": cfg["allocation_pct"],
            "max_concurrent_positions": cfg["max_concurrent"],
            "train_split_ratio": cfg["train_split_ratio"],
            "starting_capital": STARTING_CAPITAL,
            "split_time": str(split_time),
            "btc_regime_filter_applied": False,
        },
        "trade_counts": {"static_stop": int(len(static)), "atr_trailing": int(len(trailing))},
        "periods": periods,
        "stability_windows": stability,
        "quarterly": quarters,
        "additivity": additivity(periods),
        "quarterly_concentration": quarterly_concentration(quarters),
        "conditional_structure": conditional_structure(quarters),
        "overlap": overlap_analysis(static, trailing),
    }

    out_path = os.path.join(RESULTS_DIR, "vbc_deepdive.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    static.to_csv(os.path.join(RESULTS_DIR, "trades_static_stop.csv"), index=False)
    trailing.to_csv(os.path.join(RESULTS_DIR, "trades_atr_trailing.csv"), index=False)

    print(f"{BOT}: k={k:.3f} | Trades fester Stop {len(static)} / ATR-Trailing {len(trailing)}")
    for name in ("full", "in_sample", "out_of_sample"):
        print(f"\n{name}")
        for v in VARIANTS:
            r = periods[name][v]
            print(f"  {v:<12} Rendite {r['total_return_pct']:>8.2f}%  DD {r['max_drawdown_pct']:>7.2f}%  "
                  f"Calmar {str(r['calmar_ratio']):>7}  (n={r['num_trades']}, ausgefuehrt {r['num_executed']})")
    print("\nWalk-Forward-Fenster (Calmar-Ratio)")
    for w in stability:
        cells = "  ".join(f"{v[:9]}={str(w['variants'][v]['calmar_ratio']):>6}" for v in VARIANTS)
        print(f"  W{w['window_index']} {w['start']}..{w['end']}  {cells}")

    print("\nAdditivitaet (erwartet bei rein additiver Wirkung vs. tatsaechlich)")
    for name, a in output["additivity"].items():
        print(f"  {name:<14} Rendite {a['return_expected_if_additive_pct']:>7.2f}% -> "
              f"{a['return_actual_pct']:>7.2f}% ({a['return_interaction_pp']:+.2f} pp)   "
              f"Drawdown {a['drawdown_expected_if_additive_pct']:>7.2f}% -> "
              f"{a['drawdown_actual_pct']:>7.2f}% ({a['drawdown_interaction_pp']:+.2f} pp)")

    print("\nEpisoden-Robustheit (Quartalsdifferenz gegenueber der Baseline)")
    for variant, q in output["quarterly_concentration"].items():
        print(f"  {variant:<12} besser in {q['quarters_better']}/{q['quarters_total']} Quartalen, "
              f"schlechter in {q['quarters_worse']}  |  groesstes Quartal {q['dominant_quarter']} "
              f"({q['dominant_quarter_diff_pp']:+.2f} pp) = {q['dominant_quarter_share_pct']}% "
              f"des Gesamtunterschieds, Top-3 = {q['top3_share_pct']}%")

    print("\nBedingte Struktur (haengt der Nutzen an der Baseline-Lage desselben Quartals?)")
    for variant, c in output["conditional_structure"].items():
        print(f"  {variant:<12} Korrelation mit der Baseline-Quartalsrendite "
              f"{c['correlation_with_baseline_return']:>7.2f}  |  "
              f"Baseline negativ ({c['quarters_baseline_negative']} Q): "
              f"{c['mean_diff_when_baseline_negative_pp']:+.2f} pp, besser in "
              f"{c['better_share_when_baseline_negative_pct']}%  |  "
              f"Baseline positiv ({c['quarters_baseline_positive']} Q): "
              f"{c['mean_diff_when_baseline_positive_pp']:+.2f} pp, besser in "
              f"{c['better_share_when_baseline_positive_pct']}%")

    ov = output["overlap"]
    print("\nMechanismus-Unabhaengigkeit")
    print(f"  Korrelation der beiden Volatilitaets-Masse (ATR% vs. realisierte Vol): "
          f"{ov['atr_vs_realized_vol_correlation']}  (Rang: {ov['atr_vs_realized_vol_rank_correlation']})")
    print(f"  Korrelation der Trade-Beitraege:  {ov['trade_level_correlation']} (Trade-Ebene), "
          f"{ov['quarter_level_correlation']} (Quartals-Ebene)")
    print(f"  beide halfen {ov['both_helped']}x, beide schadeten {ov['both_hurt']}x, "
          f"gegenlaeufig {ov['opposite_direction']}x (von {ov['matched_trades']} gemeinsamen Trades)")
    print(f"  Top-{ov['top_n']}-Beitraege ueberlappen {ov['top_n_overlap']}x "
          f"(bei Unabhaengigkeit erwartet: {ov['top_n_overlap_expected_if_independent']})")

    print(f"\nErgebnis gespeichert: {out_path}")


if __name__ == "__main__":
    main()

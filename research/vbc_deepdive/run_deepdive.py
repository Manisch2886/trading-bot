"""
Vertiefungsstudie volatility_breakout_crypto: Vol-Sizing x ATR-Trailing-Stop
=================================================================================
Untersucht die INTERAKTION zweier bereits definierter Mechanismen - es wird
KEIN Parameter neu gesucht. ATR-Fenster (14) und Vol-Fenster (90 Balken)
werden unverändert aus den beiden Vorgänger-Studien übernommen.

WICHTIG - reine Backtest-Untersuchung: liest NUR aus
strategies/volatility_breakout_crypto/ (live_params.py, equity_simulation.py,
multi_symbol_optimise.py, backtest_breakout.py, regime_filter.py) und schreibt
ausschliesslich nach research/vbc_deepdive/results/. Keine Live-Datei wird
verändert.

--------------------------------------------------------------------
Nachtrag: BTC-Regimefilter (siehe regime.py)
--------------------------------------------------------------------
Die erste Fassung dieser Studie rechnete OHNE BTC-Regimefilter, weil
`equity_simulation.py` ihn nicht anwendet. Der Sync-Check (PR #24) hat
belegt, dass der Live-Bot ihn sehr wohl anwendet
(`BTC_REGIME_FILTER_ENABLED = True`). Die komplette Methodik laesst sich
deshalb ueber `--regime` auf drei Trade-Grundlagen rechnen:

    python3 run_deepdive.py                      # off        (Erstfassung, unveraendert)
    python3 run_deepdive.py --regime posthoc     # Projekt-Konvention, PRIMAER
    python3 run_deepdive.py --regime sequential   # live-getreue Gegenprobe

Alles ausser der Trade-Grundlage bleibt zwischen den Modi gleich: derselbe
ATR-Multiplikator k, derselbe IS/OOS-Trennzeitpunkt, dieselben Kalender-
fenster, derselbe Bootstrap-Seed. Nur so ist der Unterschied dem Filter
zuzuordnen und nicht einer nebenbei verschobenen Bezugsgroesse.
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

import bootstrap
import regime as rg
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


def _parse_regime_mode(argv) -> str:
    """--regime off|posthoc|sequential (Vorgabe: off = Erstfassung)."""
    if "--regime" not in argv:
        return rg.REGIME_OFF
    i = argv.index("--regime")
    if i + 1 >= len(argv):
        raise SystemExit("--regime braucht einen Wert: " + "|".join(rg.REGIME_MODES))
    mode = argv[i + 1]
    if mode not in rg.REGIME_MODES:
        raise SystemExit(f"unbekannter --regime-Wert {mode!r}, erlaubt: " + "|".join(rg.REGIME_MODES))
    return mode


REGIME_MODE = _parse_regime_mode(sys.argv)
OUTPUT_SUFFIX = "" if REGIME_MODE == rg.REGIME_OFF else f"_{REGIME_MODE}"

# --- Unveränderte Übernahmen aus den beiden Vorgänger-Studien -------------
ATR_WINDOW = 14      # research/trailing_stops - Wilder-Standard, im Projekt bereits fuer ADX/DI genutzt
VOL_WINDOW = 90      # research/volatility_scaled_sizing - 90 Tagesbalken (dieser Bot laeuft auf 1d)
CLIP_FACTOR = 4.0    # research/volatility_scaled_sizing - Ausreisser-Clip der inversen Vol-Gewichte
NUM_STABILITY_WINDOWS = 4
STARTING_CAPITAL = 10_000.0

# Bootstrap-Einstellungen (siehe bootstrap.py fuer die Begruendung des Verfahrens)
BOOTSTRAP_REPLICATES = 2000
BOOTSTRAP_BLOCK_MONTHS = 3     # ein Quartal - lang genug, um eine Marktphase zusammenzuhalten
BOOTSTRAP_SEED = 20260907      # fest, damit die Ergebnisse reproduzierbar sind
TIE_ORDER_PERMUTATIONS = 500   # Streuung durch die Reihenfolge gleichzeitiger Einstiege
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

    raw = load_all_symbol_data()
    prepared = {}
    for symbol, price_df in raw.items():
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
    return prepared, bt.WARMUP_PERIOD, raw


def collect_trades(prepared: dict, warmup: int, stop_kind: str, stop_pct: float,
                    k, max_hold: int, allowed: dict = None) -> pd.DataFrame:
    """
    Erzeugt den vollständigen Trade-Satz über alle Symbole für EINE
    Stop-Regel. Die Einstiegs-Logik ist unverändert aus
    strategies/volatility_breakout_crypto/backtest_breakout.py::run_backtest
    übernommen (Squeeze gestern UND Schluss über oberem Bollinger-Band
    heute, kein Pyramiding: der nächste Scan startet erst nach dem Ausstieg).
    Nur die Ausstiegs-Prüfung ist ausgetauscht.

    `allowed` (optional, nur für die `sequential`-Gegenprobe): je Symbol eine
    balkenweise Bool-Maske des BTC-Regimes. Ein Signal an einem gesperrten
    Balken führt NICHT zum Einstieg - das Symbol bleibt frei und kann ein
    späteres Signal annehmen. Genau so verhält sich der Live-Bot
    (forward_test.py::find_new_signals); nachträgliches Streichen des
    fertigen Trade-Satzes kann solche Ersatz-Trades nicht erzeugen.
    """
    rows = []
    for sym, p in prepared.items():
        close, upper, is_squeeze = p["close"], p["upper"], p["is_squeeze"]
        regime_ok = None if allowed is None else allowed[sym]
        n, i = len(close), warmup + 1
        while i < n:
            if np.isnan(upper[i]) or np.isnan(close[i]):
                i += 1
                continue
            if not (bool(is_squeeze[i - 1]) and close[i] > upper[i]):
                i += 1
                continue
            if regime_ok is not None and not regime_ok[i]:
                i += 1          # Einstieg blockiert - Symbol bleibt frei
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
def buy_and_hold(raw_data: dict, lo, hi) -> dict:
    """
    Buy-and-Hold-Gegencheck - laut CLAUDE.md Pflichtbestandteil der
    Validierungskette (Backtest -> Walk-Forward -> Equity-Simulation ->
    Buy-and-Hold).

    Es wird die UNVERAENDERTE Funktion des Bots benutzt
    (strategies/volatility_breakout_crypto/buy_and_hold_benchmark.py::
    calculate_buy_and_hold) - gleichgewichtet ueber alle Symbole, Kauf zum
    ersten Schlusskurs des Fensters, Halten bis zum letzten, Drawdown aus
    der taeglichen Portfolio-Kurve. Nur der Eingabe-Zeitraum wird
    zugeschnitten, an der Rechnung selbst nichts geaendert.

    Der Wert ist fuer alle vier Varianten derselbe (er haengt weder vom
    Stop noch von der Gewichtung ab) - genau deshalb ist er die
    unabhaengige Aussenreferenz: er beantwortet die Frage, ob die
    Strategie ueberhaupt besser ist als stumpfes Halten derselben Coins
    im selben Zeitraum.
    """
    from buy_and_hold_benchmark import calculate_buy_and_hold

    windowed = {}
    for symbol, df in raw_data.items():
        piece = df[(df["open_time"] >= lo) & (df["open_time"] <= hi)]
        if len(piece) >= 2:
            windowed[symbol] = piece.reset_index(drop=True)
    if not windowed:
        return None
    result = calculate_buy_and_hold(windowed, STARTING_CAPITAL)
    if result:
        result["calmar_ratio"] = calmar_ratio(result["total_return_pct"],
                                               result["max_drawdown_pct"])
    return result


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


def tie_order_sensitivity(sets: dict, cfg: dict, lo, hi, include_hi: bool,
                           n_permutations: int, seed: int) -> dict:
    """
    Wie stark haengen die Ergebnisse an der Reihenfolge gleichzeitiger
    Einstiege?

    Dieser Bot laeuft auf TAGESKERZEN und handelt 20 Symbole - an einem Tag
    entstehen daher regelmaessig mehrere Einstiegssignale mit exakt
    demselben Zeitstempel. Die Portfolio-Simulation vergibt Kapital
    sequenziell in Ereignis-Reihenfolge; bei erschoepftem Kapital oder
    erreichtem MAX_CONCURRENT_POSITIONS entscheidet also die Reihenfolge
    innerhalb desselben Tages darueber, WELCHER Trade ausgefuehrt wird und
    welcher wegfaellt. Diese Reihenfolge ist inhaltlich willkuerlich (sie
    ergibt sich aus der Symbol-Reihenfolge beim Einlesen und dem
    Sortierverfahren), hat aber reale Wirkung auf das Ergebnis.

    Gemessen wird, wie weit die Kennzahlen streuen, wenn man ausschliesslich
    diese Reihenfolge zufaellig permutiert und sonst NICHTS aendert - keine
    Kursdaten, keine Trades, keine Parameter. Das ist keine
    Stichprobenunsicherheit wie beim Bootstrap, sondern eine
    Implementierungs-Willkuer, die in jedem einzelnen Lauf steckt.

    Wichtig fuer die Einordnung: eine breite Streuung entwertet einen
    Vergleich nur dann, wenn sich die Streubereiche zweier Varianten
    ueberlappen. Liegen sie auseinander, ist der Unterschied groesser als
    die Willkuer.
    """
    rng = np.random.default_rng(seed)
    out = {}
    for variant in VARIANTS:
        trades = sets[USES_TRAILING[variant]]
        mask = trades["entry_time"] >= lo
        mask &= (trades["entry_time"] <= hi) if include_hi else (trades["entry_time"] < hi)
        trades = trades[mask].reset_index(drop=True)
        if trades.empty:
            continue

        entry = trades["entry_time"].to_numpy("datetime64[ns]").astype("int64")
        exit_ = trades["exit_time"].to_numpy("datetime64[ns]").astype("int64")
        pnl = trades["pnl_pct"].to_numpy(dtype=float)
        vol = trades["vol_at_entry"].to_numpy(dtype=float)

        def run_order(order, round_like_report: bool = False):
            """`round_like_report=True` bildet die Rundungsreihenfolge von
            evaluate() nach (Rendite erst runden, dann Calmar bilden). Nur der
            BERICHTETE Wert wird so berechnet - damit ist er zahlengleich mit
            dem publizierten Wert, dessen Lage er einordnen soll. Die
            Permutationen selbst bleiben unveraendert ungerundet, sonst
            verschoebe sich die Verteilung gegenueber der Erstfassung."""
            weights = (bootstrap.inverse_vol_weights_fast(vol[order], CLIP_FACTOR)
                       if USES_VOL_WEIGHTS[variant] else np.ones(len(order)))
            total_return, max_dd = bootstrap.simulate_fast(
                entry[order], exit_[order], pnl[order], weights,
                STARTING_CAPITAL, cfg["allocation_pct"] / 100.0, cfg["max_concurrent"])
            if round_like_report:
                total_return = round(total_return, 2)
            calmar = calmar_ratio(total_return, max_dd)
            return total_return, max_dd, (np.nan if calmar is None else calmar)

        # Der BERICHTETE Wert ist der Lauf in der natuerlichen Reihenfolge des
        # Trade-Satzes - genau die eine Permutation, die das Einlesen zufaellig
        # ergeben hat. Er wird hier mitgerechnet, um seine Lage INNERHALB der
        # Streuung als Perzentil auszuweisen (Methodik aus PR #23): ein Wert am
        # Rand der Verteilung stellt die Variante systematisch zu gut oder zu
        # schlecht dar, ein zentraler Wert ist unauffaellig.
        reported = run_order(np.arange(len(trades)), round_like_report=True)

        returns, drawdowns, calmars = [], [], []
        for _ in range(n_permutations):
            perm = rng.permutation(len(trades))
            order = perm[np.argsort(entry[perm], kind="stable")]
            total_return, max_dd, calmar = run_order(order)
            returns.append(total_return)
            drawdowns.append(max_dd)
            calmars.append(calmar)

        def spread(values, reported_value=None):
            arr = np.asarray(values, dtype=float)
            arr = arr[np.isfinite(arr)]
            if arr.size == 0:
                return None
            out_ = {"min": round(float(arr.min()), 2), "median": round(float(np.median(arr)), 2),
                    "max": round(float(arr.max()), 2),
                    "ci_low": round(float(np.percentile(arr, 2.5)), 2),
                    "ci_high": round(float(np.percentile(arr, 97.5)), 2)}
            if reported_value is not None and np.isfinite(reported_value):
                out_["reported"] = round(float(reported_value), 2)
                out_["reported_percentile"] = round(float((arr < reported_value).mean() * 100), 1)
            return out_

        shared = int(trades["entry_time"].duplicated(keep=False).sum())
        out[variant] = {
            "n_permutations": n_permutations,
            "trades": int(len(trades)),
            "trades_sharing_entry_timestamp": shared,
            "share_sharing_entry_timestamp_pct": round(shared / len(trades) * 100, 1),
            "largest_same_timestamp_group": int(trades["entry_time"].value_counts().max()),
            "total_return_pct": spread(returns, reported[0]),
            "max_drawdown_pct": spread(drawdowns, reported[1]),
            "calmar_ratio": spread(calmars, reported[2]),
        }
    return out


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

    prepared, warmup, raw_data = load_symbols()
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

    # --- BTC-Regimefilter ------------------------------------------------
    # Bezugsgroessen (entry_min/entry_max, split_time, k) sind oben BEWUSST auf
    # dem UNGEFILTERTEN Satz bestimmt und bleiben ueber alle drei Modi gleich.
    # Sonst aendert sich mit dem Filter gleichzeitig der Trennzeitpunkt und die
    # Stop-Distanz, und der gemessene Unterschied liesse sich keiner Ursache
    # mehr zuordnen. k wird also NICHT nachkalibriert - was es waere, steht
    # unten als reine Dokumentationszahl.
    unfiltered = {"static": static, "trailing": trailing}
    regime_report = {"mode": REGIME_MODE, "applied": REGIME_MODE != rg.REGIME_OFF}

    if REGIME_MODE != rg.REGIME_OFF:
        regime_table = rg.btc_regime_table(raw_data)

        if REGIME_MODE == rg.REGIME_POSTHOC:
            static = rg.filter_posthoc(static, regime_table)
            trailing = rg.filter_posthoc(trailing, regime_table)
        else:
            allowed = {sym: rg.regime_mask_for(p["open_time"], regime_table)
                       for sym, p in prepared.items()}
            static = collect_trades(prepared, warmup, STOP_FIXED_STATIC, cfg["stop_loss_pct"],
                                     None, cfg["max_hold"], allowed=allowed)
            trailing = collect_trades(prepared, warmup, STOP_ATR_TRAILING, cfg["stop_loss_pct"],
                                       k, cfg["max_hold"], allowed=allowed)

        bull_share = float((regime_table["btc_regime"] == 1).mean() * 100)
        f_min, f_max = static["entry_time"].min(), static["entry_time"].max()
        own_split = f_min + (f_max - f_min) * cfg["train_split_ratio"]
        is_filtered = static[static["entry_time"] < split_time]
        k_would_be = calibrate_atr_multiplier(is_filtered["atr_at_entry"].to_numpy(),
                                               is_filtered["entry_price"].to_numpy(),
                                               cfg["stop_loss_pct"])
        regime_report.update({
            "btc_bullish_bar_share_pct": round(bull_share, 1),
            "trades_before": {"static": int(len(unfiltered["static"])),
                              "trailing": int(len(unfiltered["trailing"]))},
            "trades_after": {"static": int(len(static)), "trailing": int(len(trailing))},
            "removed_share_pct": {
                "static": round((1 - len(static) / len(unfiltered["static"])) * 100, 1),
                "trailing": round((1 - len(trailing) / len(unfiltered["trailing"])) * 100, 1)},
            "first_entry_after_filter": str(f_min.date()),
            "k_used": round(k, 4),
            "k_if_recalibrated_on_filtered": (None if k_would_be is None
                                              else round(k_would_be, 4)),
            "split_time_used": str(split_time),
            "split_time_if_recomputed_on_filtered": str(own_split),
        })

    sets = {False: static, True: trailing}

    period_bounds = {
        "full": (entry_min, entry_max, True),
        "in_sample": (entry_min, split_time, False),
        "out_of_sample": (split_time, entry_max, True),
    }

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

    # Buy-and-Hold je Periode (Pflicht-Gegencheck)
    bh = {name: buy_and_hold(raw_data, lo, hi) for name, (lo, hi, _) in period_bounds.items()}

    # Datenbasis - gehoert in jede Entscheidungsgrundlage
    all_static_symbols = sorted(static["symbol"].unique())
    data_basis = {
        "symbols_with_trades": len(all_static_symbols),
        "symbols_loaded": len(raw_data),
        "first_entry": str(entry_min.date()),
        "last_exit": str(max(static["exit_time"].max(), trailing["exit_time"].max()).date()),
        "years_covered": round((static["exit_time"].max() - entry_min).days / 365.25, 2),
        "trades_per_period": {
            name: {variant: {"found": periods[name][variant]["num_trades"],
                              "executed": periods[name][variant]["num_executed"],
                              "skipped": periods[name][variant]["num_skipped"]}
                   for variant in VARIANTS}
            for name in periods
        },
    }

    # Block-Bootstrap: Konfidenzintervalle fuer die Variantenunterschiede
    bootstrap_results = {}
    for name, (lo, hi, include_hi) in period_bounds.items():
        bootstrap_results[name] = bootstrap.run(
            sets, {**cfg, "clip_factor": CLIP_FACTOR}, lo, hi, include_hi,
            BOOTSTRAP_REPLICATES, BOOTSTRAP_BLOCK_MONTHS, BOOTSTRAP_SEED, STARTING_CAPITAL)

    tie_order = {name: tie_order_sensitivity(sets, cfg, lo, hi, include_hi,
                                              TIE_ORDER_PERMUTATIONS, BOOTSTRAP_SEED)
                 for name, (lo, hi, include_hi) in period_bounds.items()}

    output = {
        "bot": BOT,
        "regime_filter": regime_report,
        "data_basis": data_basis,
        "tie_order_sensitivity": tie_order,
        "buy_and_hold": bh,
        "bootstrap": bootstrap_results,
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
            "btc_regime_filter_applied": REGIME_MODE != rg.REGIME_OFF,
            "btc_regime_filter_mode": REGIME_MODE,
            "bootstrap_replicates": BOOTSTRAP_REPLICATES,
            "bootstrap_block_months": BOOTSTRAP_BLOCK_MONTHS,
            "bootstrap_seed": BOOTSTRAP_SEED,
            "tie_order_permutations": TIE_ORDER_PERMUTATIONS,
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

    out_path = os.path.join(RESULTS_DIR, f"vbc_deepdive{OUTPUT_SUFFIX}.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    static.to_csv(os.path.join(RESULTS_DIR, f"trades_static_stop{OUTPUT_SUFFIX}.csv"), index=False)
    trailing.to_csv(os.path.join(RESULTS_DIR, f"trades_atr_trailing{OUTPUT_SUFFIX}.csv"), index=False)

    print(f"{BOT}: BTC-Regimefilter = {REGIME_MODE} | k={k:.3f} | "
          f"Trades fester Stop {len(static)} / ATR-Trailing {len(trailing)}")
    if regime_report["applied"]:
        r = regime_report
        print(f"  gestrichen: fester Stop {r['trades_before']['static']} -> {r['trades_after']['static']} "
              f"({r['removed_share_pct']['static']}%), ATR-Trailing "
              f"{r['trades_before']['trailing']} -> {r['trades_after']['trailing']} "
              f"({r['removed_share_pct']['trailing']}%)")
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

    print("\nBuy-and-Hold-Gegencheck (identisch fuer alle vier Varianten)")
    for name, r in bh.items():
        if r:
            print(f"  {name:<14} {r['total_return_pct']:>8.2f}%  DD {r['max_drawdown_pct']:>7.2f}%  "
                  f"Calmar {str(r['calmar_ratio']):>6}  ({r['num_symbols']} Symbole)")

    print("\nStreuung allein durch die Reihenfolge gleichzeitiger Einstiege (Calmar, Gesamtzeitraum)")
    for variant, t in tie_order["full"].items():
        c = t["calmar_ratio"]
        print(f"  {variant:<12} {c['min']:>6.2f} .. {c['max']:>6.2f}  (Median {c['median']:>6.2f}, "
              f"berichtet {periods['full'][variant]['calmar_ratio']} = "
              f"{c.get('reported_percentile')}. Perzentil)")

    print("\nBlock-Bootstrap: 95%-Intervalle der Calmar-DIFFERENZ gegenueber der Vergleichsvariante")
    for name in ("full", "out_of_sample"):
        b = bootstrap_results[name]
        if "error" in b:
            print(f"  {name}: {b['error']}")
            continue
        print(f"  {name} ({b['months_in_period']} Monate, {b['n_replicates']} Replikate)")
        for key, diff in b["differences"].items():
            c = diff["calmar_ratio"]
            print(f"    {key:<28} {c['ci_low']:>7.2f} .. {c['ci_high']:>7.2f}   "
                  f"P(>0) = {c['share_above_zero_pct']:>5.1f} %")

    print(f"\nErgebnis gespeichert: {out_path}")


if __name__ == "__main__":
    main()

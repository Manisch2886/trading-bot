"""
Rechenkern der Parameter-Neubestimmung (beide Elliott-Wave-Bots)
====================================================================
Diese Untersuchung rechnet NICHT mit einer eigenen Backtest-Kopie.
Wellenerkennung und Trade-Simulation kommen aus dem - seit PR #26
kausal korrigierten - Bot-Code selbst:

    zigzag_indicator.calculate_zigzag_with_confirmation
    elliott_wave_counter.find_causal_waves
    backtest_elliott.run_backtest
    equity_simulation.simulate_portfolio / calculate_max_drawdown

Damit gilt jede hier gemessene Zahl fuer genau den Backtest, der auch
im Repo steht - eine eigene Nachbildung koennte davon abweichen, ohne
dass es jemand merkt.

--------------------------------------------------------------------
Warum das ueberhaupt bezahlbar ist
--------------------------------------------------------------------
Zigzag und Wellenerkennung haengen NUR von `deviation_pct` ab (und vom
Frische-Fenster, das je Bot fest ist) - nicht von Stop-Loss oder
Take-Profit. Die Wellen werden deshalb je (Fenster, Symbol,
deviation_pct) genau einmal berechnet und fuer alle Stop/Ziel-
Kombinationen wiederverwendet. Identisches Ergebnis, ein Bruchteil der
Rechenzeit. Zusaetzlich liegt der Wellen-Cache auf Platte, damit
Folgeskripte (Stabilitaet, Walk-Forward) ihn nicht neu berechnen
muessen.

--------------------------------------------------------------------
Fenster
--------------------------------------------------------------------
gesamt   die volle Historie, wie sie der Bot laedt
is       In-Sample: die ersten TRAIN_SPLIT_RATIO je Symbol
oos      Out-of-Sample: der Rest je Symbol

Der Split je Symbol stammt woertlich aus
multi_symbol_walk_forward.split_all_symbols - dasselbe Verfahren, das
im Projekt schon fuer Walk-Forward benutzt wird. Jedes Fenster wird
komplett neu durchgerechnet (eigener Zigzag, eigene Wellen); ein
Fenster sieht also nie Kurse ausserhalb seiner Grenzen.
"""

import hashlib
import os
import pickle

import pandas as pd

import botenv

import backtest_elliott as bt                      # noqa: E402
import equity_simulation as es                     # noqa: E402
import multi_symbol_optimise as mo                 # noqa: E402
import live_params as lp                           # noqa: E402
from zigzag_indicator import calculate_zigzag_with_confirmation   # noqa: E402
from elliott_wave_counter import find_causal_waves               # noqa: E402

BOT = os.path.basename(os.path.dirname(os.path.abspath(mo.__file__)))

# Woertlich aus multi_symbol_walk_forward.py des jeweiligen Bots.
TRAIN_SPLIT_RATIO = 0.7
WINDOW_FULL, WINDOW_IS, WINDOW_OOS = "gesamt", "is", "oos"

MIN_FIB_SCORE = 0.3          # wie in beiden Bots fest verdrahtet
SUPPORTS_NO_TP = "use_take_profit" in bt.run_backtest.__code__.co_varnames
SUPPORTS_POSITION_LIMIT = "max_concurrent_positions" in es.simulate_portfolio.__code__.co_varnames
MAX_CONCURRENT = getattr(lp, "MAX_CONCURRENT_POSITIONS", None)


def live_combo() -> dict:
    """Die aktuell in live_params.py gesetzte Kombination - Bezugspunkt
    aller Vergleiche. Wird nur gelesen, nie geschrieben."""
    return {
        "deviation_pct": float(lp.DEVIATION_PCT),
        "stop_loss_pct": float(lp.STOP_LOSS_PCT),
        "take_profit_fib": float(lp.TAKE_PROFIT_FIB),
        "use_take_profit": bool(getattr(lp, "USE_TAKE_PROFIT", True)),
    }


# --------------------------------------------------------------------
# Daten und Fenster
# --------------------------------------------------------------------

def load_windows(quiet: bool = True) -> dict:
    """Laedt die Bot-Daten und bildet die drei Fenster."""
    import contextlib
    import io

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf) if quiet else contextlib.nullcontext():
        all_data = mo.load_all_symbol_data()
    if not all_data:
        raise SystemExit(f"{BOT}: keine Kursdaten in data/ gefunden.")

    train, test = {}, {}
    for symbol, df in all_data.items():
        split_idx = int(len(df) * TRAIN_SPLIT_RATIO)
        train[symbol] = df.iloc[:split_idx].reset_index(drop=True)
        test[symbol] = df.iloc[split_idx:].reset_index(drop=True)
    return {WINDOW_FULL: all_data, WINDOW_IS: train, WINDOW_OOS: test}


def window_span(all_data: dict) -> tuple:
    starts = [df["open_time"].min() for df in all_data.values() if len(df)]
    ends = [df["open_time"].max() for df in all_data.values() if len(df)]
    return (str(min(starts)), str(max(ends))) if starts else (None, None)


# --------------------------------------------------------------------
# Wellen-Cache
# --------------------------------------------------------------------

def _cache_path(window: str, deviation_pct: float, all_data: dict) -> str:
    """Der Schluessel enthaelt einen Fingerabdruck der Kursdaten - aendern
    sich die CSVs, wird der Cache automatisch ungueltig."""
    h = hashlib.sha256()
    for symbol in sorted(all_data):
        df = all_data[symbol]
        h.update(symbol.encode())
        h.update(str(len(df)).encode())
        h.update(str(df["open_time"].iloc[0]).encode())
        h.update(str(df["open_time"].iloc[-1]).encode())
        h.update(f"{float(df['close'].iloc[-1]):.10g}".encode())
    key = f"{BOT}_{window}_dev{deviation_pct:g}_{h.hexdigest()[:12]}.pkl"
    return os.path.join(botenv.CACHE_DIR, key)


def waves_for(window: str, all_data: dict, deviation_pct: float, use_cache: bool = True) -> dict:
    """Kausale Wellen je Symbol - unveraenderte Bot-Funktionen."""
    path = _cache_path(window, deviation_pct, all_data)
    if use_cache and os.path.exists(path):
        with open(path, "rb") as fh:
            return pickle.load(fh)

    cache = {}
    for symbol, price_df in all_data.items():
        zigzag = calculate_zigzag_with_confirmation(price_df, deviation_pct=deviation_pct)
        if len(zigzag) < 6:
            cache[symbol] = pd.DataFrame()
            continue
        cache[symbol] = find_causal_waves(
            zigzag, min_fib_score=MIN_FIB_SCORE,
            freshness_bars=bt.SIGNAL_FRESHNESS_BARS,
            direction="bearish")          # Long-only, wie im Bot
    if use_cache:
        with open(path, "wb") as fh:
            pickle.dump(cache, fh)
    return cache


# --------------------------------------------------------------------
# Trades
# --------------------------------------------------------------------

def collect_trades(all_data: dict, waves: dict, stop_loss_pct: float,
                    take_profit_fib: float, use_take_profit: bool) -> pd.DataFrame:
    """Trades einer Kombination ueber alle Symbole - auf bereits
    berechneten Wellen, sonst identisch zum Bot. Stop und Ziel gehen wie
    dort ueber die Modulvariablen von backtest_elliott in dessen
    unveraendertes run_backtest.

    ACHTUNG, ZEILENREIHENFOLGE: der Bot benutzt zwei verschiedene.
    multi_symbol_optimise.evaluate_combination_multi - das Skript, das
    die Parameterwahl getragen hat - haengt die Symbol-Bloecke einfach
    aneinander (pd.concat(..., ignore_index=True)) und rechnet seinen
    Drawdown auf DIESER Reihenfolge. equity_simulation.collect_all_trades
    sortiert dagegen nach entry_time, bevor die Kapitalsimulation laeuft.
    Der Unterschied ist nicht klein: beim Aktien-Bot liefert dieselbe
    Trade-Menge einmal -82,5 % und einmal -259,9 % kumulierten Drawdown.

    Diese Funktion liefert deshalb die Bloecke in Bot-Reihenfolge
    (Symbol fuer Symbol) - so wie das Optimierungsskript sie sieht -
    und portfolio() sortiert selbst nach entry_time, so wie die
    Kapitalsimulation es tut. Beide Bot-Pfade bleiben damit exakt
    nachgebildet; score_trades weist zusaetzlich den chronologischen
    Drawdown aus, damit der Unterschied sichtbar bleibt statt
    stillschweigend in eine Kennzahl einzugehen."""
    bt.STOP_LOSS_PCT = float(stop_loss_pct)
    bt.TAKE_PROFIT_FIB = float(take_profit_fib)

    blocks = []
    for symbol, wave_df in waves.items():
        if wave_df is None or wave_df.empty:
            continue
        kwargs = {"use_take_profit": use_take_profit} if SUPPORTS_NO_TP else {}
        trades = bt.run_backtest(all_data[symbol], wave_df, **kwargs)
        if trades.empty:
            continue
        trades = trades.copy()
        trades["symbol"] = symbol
        blocks.append(trades)

    if not blocks:
        return pd.DataFrame()
    combined = pd.concat(blocks, ignore_index=True)
    combined["entry_time"] = pd.to_datetime(combined["entry_time"])
    combined["exit_time"] = pd.to_datetime(combined["exit_time"])
    return combined


# --------------------------------------------------------------------
# Bewertung
# --------------------------------------------------------------------

def robustness_score(avg_return_pct: float, num_trades: int, max_drawdown_pct: float) -> float:
    """Woertlich aus multi_symbol_optimise.calculate_robustness_score."""
    penalty = abs(max_drawdown_pct) if max_drawdown_pct != 0 else 1.0
    return round((avg_return_pct * (num_trades ** 0.5)) / penalty, 3)


def project_filters() -> dict:
    """Die projekteigenen Mindestfilter des jeweiligen Bots."""
    return {
        "min_trades": int(mo.MIN_TRADES),
        "min_symbols": int(mo.MIN_SYMBOLS_CONTRIBUTING),
        "min_avg_return_pct": float(mo.MIN_AVG_RETURN_PCT),
    }


def _cum_drawdown(pnl: pd.Series) -> float:
    cum = pnl.cumsum()
    return float((cum - cum.cummax()).min())


def score_trades(trades: pd.DataFrame) -> dict:
    """Das Bewertungsmass von multi_symbol_optimise - inklusive des dort
    verwendeten Drawdowns auf der KUMULIERTEN PnL-Reihe (nicht auf der
    Kapitalkurve) und in der dortigen Zeilenreihenfolge (Symbol-Bloecke,
    siehe collect_trades). Es ist das Mass, das die bisherige
    Parameterwahl getragen hat; es wird hier unveraendert uebernommen,
    damit die Ergebnisse mit den frueheren vergleichbar bleiben.

    Zusaetzlich - und ohne Einfluss auf die Rangfolge - wird derselbe
    Drawdown auf der CHRONOLOGISCHEN Reihenfolge ausgewiesen. Nur diese
    beschreibt einen Verlauf, den man tatsaechlich haette erleben
    koennen; die Symbol-Block-Reihenfolge ist ein Nebenprodukt der
    Art, wie das Optimierungsskript seine Teilergebnisse aneinanderhaengt."""
    if trades is None or trades.empty:
        return None
    f = project_filters()
    contributing = int(trades["symbol"].nunique())
    avg_return = float(trades["pnl_pct"].mean())
    max_dd = _cum_drawdown(trades["pnl_pct"])
    chrono = trades.sort_values("entry_time", kind="stable")
    max_dd_chrono = _cum_drawdown(chrono["pnl_pct"])
    counts = trades["result"].value_counts()
    passes = (len(trades) >= f["min_trades"]
              and contributing >= f["min_symbols"]
              and avg_return >= f["min_avg_return_pct"])
    return {
        "num_trades": int(len(trades)),
        "num_symbols": contributing,
        "win_rate": round(float((trades["pnl_pct"] > 0).mean() * 100), 1),
        "total_return_pct": round(float(trades["pnl_pct"].sum()), 2),
        "avg_return_pct": round(avg_return, 2),
        "max_drawdown_pct": round(max_dd, 2),
        "robustness_score": robustness_score(avg_return, len(trades), max_dd),
        "max_drawdown_chronologisch_pct": round(max_dd_chrono, 2),
        "robustness_score_chronologisch": robustness_score(avg_return, len(trades),
                                                            max_dd_chrono),
        "share_take_profit_pct": round(float(counts.get("take_profit", 0)) / len(trades) * 100, 1),
        "share_stop_loss_pct": round(float(counts.get("stop_loss", 0)) / len(trades) * 100, 1),
        "besteht_mindestfilter": bool(passes),
    }


def calmar(total_return_pct, max_drawdown_pct):
    """Calmar-Konvention aller bisherigen Studien: Rendite / |Max DD|."""
    if max_drawdown_pct is None or abs(max_drawdown_pct) < 1e-12:
        return None
    return round(total_return_pct / abs(max_drawdown_pct), 2)


def portfolio(trades: pd.DataFrame, order: pd.Index = None) -> dict:
    """Kapital-Simulation ueber die UNVERAENDERTE simulate_portfolio des
    Bots (Positionslimit nur, wo der Bot eines kennt)."""
    if trades is None or trades.empty:
        return None
    if order is not None:
        trades = trades.loc[order].reset_index(drop=True)
    else:
        # wie equity_simulation.collect_all_trades - dort laeuft die
        # Kapitalsimulation immer auf der chronologisch sortierten Menge.
        # kind="stable" statt der pandas-Vorgabe, damit gleichzeitige
        # Einstiege reproduzierbar in derselben Reihenfolge stehen.
        trades = trades.sort_values("entry_time", kind="stable").reset_index(drop=True)
    if SUPPORTS_POSITION_LIMIT:
        res = es.simulate_portfolio(trades, es.STARTING_CAPITAL, es.ALLOCATION_PCT, MAX_CONCURRENT)
    else:
        res = es.simulate_portfolio(trades, es.STARTING_CAPITAL, es.ALLOCATION_PCT)
    total_return = round((res["final_capital"] / es.STARTING_CAPITAL - 1) * 100, 2)
    max_dd = es.calculate_max_drawdown(res["equity_curve"], es.STARTING_CAPITAL)
    return {
        "num_executed": int(res["num_executed"]),
        "num_skipped": int(res["num_skipped"]),
        "total_return_pct": total_return,
        "max_drawdown_pct": max_dd,
        "calmar_ratio": calmar(total_return, max_dd),
    }


# --------------------------------------------------------------------
# Buy-and-Hold
# --------------------------------------------------------------------

def buy_and_hold(all_data: dict, starting_capital: float = None) -> dict:
    """Gleichgewichtetes Kaufen-und-Halten derselben Symbole ueber
    denselben Zeitraum - die Pflichtreferenz des Projekts.

    Die Logik ist die von elliott_wave_stocks/buy_and_hold_benchmark.py;
    sie steht hier noch einmal, weil der Krypto-Bot kein solches Skript
    hat. test_params.py rechnet beide gegeneinander und belegt, dass sie
    dasselbe Ergebnis liefern."""
    capital = float(starting_capital if starting_capital is not None else es.STARTING_CAPITAL)
    if not all_data:
        return None
    per_symbol = capital / len(all_data)

    curves, final_value, skipped = [], 0.0, []
    for symbol, df in all_data.items():
        df = df.sort_values("open_time").reset_index(drop=True)
        entry_price = df["close"].iloc[0]
        exit_price = df["close"].iloc[-1]
        if pd.isna(entry_price) or pd.isna(exit_price) or entry_price == 0:
            skipped.append(symbol)
            continue
        shares = per_symbol / entry_price
        value = df[["open_time", "close"]].copy()
        value["value"] = value["close"] * shares
        curves.append(value.set_index("open_time")["value"])
        final_value += exit_price * shares

    # Der Kapitalanteil uebersprungener Symbole bleibt als Cash stehen -
    # sonst waeren Start- und Endkapital nicht vergleichbar.
    final_value += per_symbol * len(skipped)
    if not curves:
        return None

    portfolio_curve = pd.concat(curves, axis=1).sort_index().ffill().sum(axis=1)
    running_max = portfolio_curve.cummax()
    max_dd = float(((portfolio_curve - running_max) / running_max * 100).min())
    total_return = (final_value / capital - 1) * 100
    return {
        "final_capital": round(final_value, 2),
        "total_return_pct": round(total_return, 2),
        "max_drawdown_pct": round(max_dd, 2),
        "calmar_ratio": calmar(round(total_return, 2), round(max_dd, 2)),
        "num_symbols": len(all_data),
        "num_skipped_symbols": len(skipped),
    }

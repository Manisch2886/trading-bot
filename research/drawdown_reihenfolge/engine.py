"""
Rechenkern: dieselbe Trade-Menge, vier Zeilenreihenfolgen
====================================================================
Diese Datei enthaelt KEINE eigene Backtest-Logik. Trades entstehen
ausschliesslich durch Aufrufe der echten Bot-Funktionen
(`multi_symbol_optimise.get_trades_for_symbol`, bei `t3_supertrend`
zusaetzlich `regime_filter.compute_btc_regime` /
`filter_trades_by_regime`), und bewertet wird mit der Formel des Bots
(`multi_symbol_optimise.calculate_robustness_score`, per Aufruf, nicht
nachgebaut).

Neu ist hier nur eines: derselbe Drawdown wird auf VIER
Zeilenreihenfolgen derselben Trade-Menge gerechnet.

    dd_bot     die Reihenfolge, die evaluate_combination_multi des Bots
               tatsaechlich sieht. Muss reproduziert werden - der
               Selbsttest vergleicht sie Feld fuer Feld mit dem
               Rueckgabewert der echten Bot-Funktion.
    dd_block   Symbol-Bloecke in der Reihenfolge, in der der Bot seine
               Teilergebnisse aneinanderhaengt (= dd_bot bei acht der
               neun Bots; bei t3_supertrend rekonstruiert, siehe unten).
    dd_entry   stabil nach entry_time sortiert - die Reihenfolge, die
               equity_simulation.collect_all_trades aller neun Bots
               benutzt.
    dd_exit    stabil nach exit_time sortiert - die Reihenfolge, in der
               die Gewinne und Verluste tatsaechlich im Konto landen.

ZU t3_supertrend: dieser Bot haengt nach dem Zusammenfuegen noch den
BTC-Regimefilter dahinter, und `filter_trades_by_regime` sortiert
intern nach `entry_time` (es braucht das fuer `pd.merge_asof`). Die
Zeilenreihenfolge, auf der dort der Drawdown entsteht, ist damit
bereits chronologisch - ohne dass das irgendwo beabsichtigt oder
dokumentiert waere. Um trotzdem beide Masse zu bekommen, faehrt der
Adapter eine Spalte `_block_idx` durch den Filter hindurch und stellt
die Blockreihenfolge daraus wieder her.

ZU FEHLENDEN KURSEN (APH-Problematik, research/elliott_wave_params
Abschnitt 6, zweiter Fund): ein Trade mit `pnl_pct = NaN` koennte die
kumulierte Reihe abbrechen - das war die Erwartung. Gemessen
(test_drawdown.py) gilt das NICHT: `Series.cumsum()` ueberspringt NaN
(`skipna=True`), ein solcher Trade wirkt in der kumulierten Reihe wie
0, und der Drawdown des Rasters bleibt unberuehrt. Was die Luecke
verschiebt, ist `mean()` - dort faellt der NaN-Trade aus dem Nenner,
waehrend `num_trades` ihn mitzaehlt.

Um das nicht nur zu behaupten, zaehlt diese Untersuchung solche Trades
je Kombination (`num_nan_pnl`) und weist alle vier Drawdowns
zusaetzlich auf der NaN-freien Menge aus (`dd_*_ohne_nan`). Behoben
wird hier nichts - das ist eine eigene Aufgabe.
"""

import numpy as np
import pandas as pd


# --------------------------------------------------------------------
# Drawdown auf der kumulierten PnL-Reihe - woertlich die beiden Zeilen
# aus multi_symbol_optimise.evaluate_combination_multi:
#     cum_returns = combined["pnl_pct"].cumsum()
#     max_drawdown = (cum_returns - cum_returns.cummax()).min()
# --------------------------------------------------------------------
def cum_drawdown(pnl) -> float:
    s = pd.Series(pnl)
    if s.empty:
        return float("nan")
    cum = s.cumsum()
    return float((cum - cum.cummax()).min())


def cum_drawdown_np(pnl: np.ndarray) -> float:
    """Numerisch identisch zu cum_drawdown, aber ohne pandas-Overhead -
    fuer die 200 Permutationen je Kombination. test_drawdown.py prueft
    die Gleichheit beider Wege auf Zufallsdaten."""
    if pnl.size == 0:
        return float("nan")
    cum = np.cumsum(pnl)
    return float(np.nanmin(cum - np.maximum.accumulate(cum)))


ORDERS = ("bot", "block", "entry", "exit")


def _order_index(trades: pd.DataFrame, order: str) -> pd.Index:
    if order == "bot":
        return trades.index
    if order == "block":
        return trades.sort_values("_block_idx", kind="stable").index
    if order == "entry":
        return trades.sort_values("entry_time", kind="stable").index
    if order == "exit":
        return trades.sort_values("exit_time", kind="stable").index
    raise ValueError(order)


def drawdowns(trades: pd.DataFrame) -> dict:
    """Die vier Drawdowns derselben Trade-Menge, je einmal mit und
    einmal ohne die NaN-PnL-Trades."""
    out = {}
    ohne = trades[trades["pnl_pct"].notna()]
    for order in ORDERS:
        out[f"dd_{order}"] = round(cum_drawdown(trades.loc[_order_index(trades, order), "pnl_pct"]), 2)
        out[f"dd_{order}_ohne_nan"] = round(
            cum_drawdown(ohne.loc[_order_index(ohne, order), "pnl_pct"]), 2)
    return out


def score(calculate_robustness_score, avg_return_pct: float, num_trades: int,
          max_drawdown_pct: float):
    """Der Projekt-Score - gerechnet von der ECHTEN Bot-Funktion, die
    als Argument hereingegeben wird. Hier steht bewusst keine Kopie der
    Formel."""
    if max_drawdown_pct is None or (isinstance(max_drawdown_pct, float)
                                     and np.isnan(max_drawdown_pct)):
        return None
    return calculate_robustness_score({
        "avg_return_pct": avg_return_pct,
        "num_trades": num_trades,
        "max_drawdown_pct": max_drawdown_pct,
    })


def kennzahlen(trades: pd.DataFrame, contributing_symbols: int,
               calculate_robustness_score) -> dict:
    """Alles, was multi_symbol_optimise je Kombination berechnet, plus
    die vier Drawdowns und die vier daraus folgenden Scores.

    Die gerundeten Zwischenwerte sind mit Absicht so gerundet wie im
    Bot: dieser rundet avg_return_pct und max_drawdown_pct auf zwei
    Stellen, BEVOR calculate_robustness_score sie sieht. Eine
    ungerundete Rechnung waere naeher am Ideal, aber nicht mehr die
    Zahl, die die Parameterwahl getragen hat."""
    pnl = trades["pnl_pct"]
    avg_return = round(float(pnl.mean()), 2)
    row = {
        "num_trades": int(len(trades)),
        "num_symbols": int(contributing_symbols),
        "num_nan_pnl": int(pnl.isna().sum()),
        "win_rate": round(float((pnl > 0).mean() * 100), 1),
        "total_return_pct": round(float(pnl.sum()), 2),
        "avg_return_pct": avg_return,
    }
    row.update(drawdowns(trades))
    for order in ORDERS:
        row[f"score_{order}"] = score(calculate_robustness_score, avg_return,
                                       len(trades), row[f"dd_{order}"])
        row[f"score_{order}_ohne_nan"] = score(calculate_robustness_score, avg_return,
                                                len(trades), row[f"dd_{order}_ohne_nan"])
    return row


# --------------------------------------------------------------------
# Streuung: wie weit traegt die Willkuer der Blockreihenfolge?
# --------------------------------------------------------------------
def block_permutation_drawdowns(trades: pd.DataFrame, n: int, seed: int) -> np.ndarray:
    """Vertauscht die Symbol-BLOECKE (nicht die Zeilen innerhalb eines
    Blocks) und gibt je Permutation den kumulierten Drawdown zurueck.

    Das ist genau die Groesse, die der Bot willkuerlich festlegt: in
    welcher Reihenfolge die Teilergebnisse aneinandergehaengt werden.
    Die Reihenfolge innerhalb eines Symbols ist dagegen echt - sie ist
    die Zeit."""
    rng = np.random.default_rng(seed)
    groups = [g["pnl_pct"].to_numpy(dtype=float)
              for _, g in trades.groupby("_block_idx", sort=True)]
    out = np.empty(n, dtype=float)
    for i in range(n):
        order = rng.permutation(len(groups))
        out[i] = cum_drawdown_np(np.concatenate([groups[j] for j in order]))
    return out


def tie_permutation_drawdowns(trades: pd.DataFrame, n: int, seed: int) -> np.ndarray:
    """Vertauscht nur Trades mit IDENTISCHEM entry_time und laesst die
    chronologische Reihenfolge im Uebrigen unangetastet. Das ist die
    Rest-Willkuer, die auch die chronologische Sortierung noch hat -
    und damit die Messlatte dafuer, ob ein Unterschied zwischen den
    Massen ueberhaupt etwas bedeutet."""
    rng = np.random.default_rng(seed)
    base = trades.sort_values("entry_time", kind="stable")
    key = base["entry_time"].to_numpy()
    pnl = base["pnl_pct"].to_numpy(dtype=float)
    # Gruppengrenzen gleicher entry_time
    starts = np.flatnonzero(np.concatenate(([True], key[1:] != key[:-1])))
    ends = np.concatenate((starts[1:], [len(key)]))
    blocks = [(s, e) for s, e in zip(starts, ends) if e - s > 1]
    out = np.empty(n, dtype=float)
    for i in range(n):
        shuffled = pnl.copy()
        for s, e in blocks:
            shuffled[s:e] = rng.permutation(shuffled[s:e])
        out[i] = cum_drawdown_np(shuffled)
    return out


def spanne(values: np.ndarray) -> dict:
    v = np.asarray(values, dtype=float)
    v = v[~np.isnan(v)]
    if v.size == 0:
        return {"n": 0}
    return {
        "n": int(v.size),
        "min": round(float(v.min()), 2),
        "median": round(float(np.median(v)), 2),
        "max": round(float(v.max()), 2),
        "spanne_pp": round(float(v.max() - v.min()), 2),
    }

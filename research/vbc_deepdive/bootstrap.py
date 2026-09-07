"""
Block-Bootstrap: Konfidenzintervalle fuer die Variantenunterschiede
=========================================================================
Beantwortet die eigentliche Kernfrage dieser Studie: sind die gemessenen
Unterschiede zwischen den vier Varianten von Rauschen unterscheidbar?

Ohne diese Rechnung liest sich "Calmar 1,79 -> 5,04 Out-of-Sample" wie ein
robustes Ergebnis, obwohl dahinter nur rund 100 ausgefuehrte Trades ueber
etwa 16 Monate stehen. Das Projekt hat bisher an keiner Stelle ein
Unsicherheitsmass - fuer eine reine Deskription war das vertretbar, fuer
die Frage "echtes Signal oder zweimal gemessenes Rauschen" ist es das nicht.

--------------------------------------------------------------------
Verfahren: zirkulaerer Moving-Block-Bootstrap ueber Kalendermonate
--------------------------------------------------------------------
Ein naiver Bootstrap, der einzelne Trades mit Zuruecklegen zieht, waere
hier FALSCH: die Portfolio-Simulation ist pfadabhaengig (gebundenes
Kapital, MAX_CONCURRENT_POSITIONS, Zinseszins) und der Max Drawdown ist
eine Eigenschaft der zeitlichen REIHENFOLGE. Einzelne Trades zu ziehen
zerstoert genau die Struktur, die gemessen werden soll.

Stattdessen werden BLOECKE von je `block_months` aufeinanderfolgenden
Kalendermonaten mit Zuruecklegen gezogen und zu einer neuen, gleich langen
Zeitachse zusammengesetzt. Innerhalb eines Blocks bleiben Reihenfolge,
Ueberlappung offener Positionen und die lokale Marktphase erhalten; nur die
Abfolge der Bloecke wird neu gewuerfelt. Die Zeitstempel der Trades werden
dabei um die Differenz zwischen Quell- und Zielposition verschoben, sodass
eine gueltige chronologische Historie entsteht und die bestehende
Portfolio-Simulation unveraendert darauf laufen kann.

"Zirkulaer" heisst: Bloecke duerfen ueber das Ende der Historie hinaus
wieder am Anfang ansetzen. Sonst waeren die Monate am Rand der Historie
systematisch unterrepraesentiert (Standard-Argument fuer den zirkulaeren
gegenueber dem einfachen Block-Bootstrap).

--------------------------------------------------------------------
GEPAART, nicht unabhaengig
--------------------------------------------------------------------
Alle vier Varianten werden je Replikat auf DERSELBEN gezogenen Zeitachse
ausgewertet. Die Unsicherheit der Marktphasen-Auswahl kuerzt sich damit
aus der DIFFERENZ zwischen zwei Varianten weitgehend heraus - genau das,
was hier interessiert. Ein ungepaarter Vergleich wuerde die Intervalle
kuenstlich aufblaehen und jeden Unterschied als "nicht signifikant"
erscheinen lassen, auch einen echten.

--------------------------------------------------------------------
Was das Verfahren NICHT leistet
--------------------------------------------------------------------
Es quantifiziert die Unsicherheit, die aus der begrenzten LAENGE und
Zusammensetzung der vorliegenden Historie stammt. Es sagt nichts ueber
Regimewechsel, die in dieser Historie gar nicht vorkommen, und es macht
aus einem retrospektiven Backtest keine Aussage ueber die Zukunft. Ein
enges Intervall bedeutet "innerhalb dieser 4,5 Jahre stabil", nicht
"verlaesslich".
"""

import numpy as np
import pandas as pd

from vbc_core import (
    compute_inverse_vol_weights, simulate_weighted_portfolio,
    calculate_max_drawdown, calmar_ratio,
    VARIANTS, VARIANT_BASELINE, VARIANT_TRAILING, VARIANT_COMBINED,
    USES_TRAILING, USES_VOL_WEIGHTS,
)

# Ein Calmar-Wert wird unbrauchbar, wenn der Drawdown gegen null geht (der
# Nenner explodiert). Replikate unterhalb dieser Schwelle werden fuer die
# Calmar-Intervalle verworfen und ihre Anzahl ausgewiesen, statt das
# Intervall still von einzelnen Extremwerten sprengen zu lassen. Rendite-
# und Drawdown-Intervalle sind davon nicht betroffen.
MIN_ABS_DRAWDOWN_PCT = 0.10


def month_span(trades_by_variant: dict) -> list:
    """Alle Kalendermonate zwischen erstem und letztem Einstieg ueber ALLE
    Varianten hinweg - eine gemeinsame Zeitachse, damit die Varianten
    tatsaechlich gepaart sind."""
    starts, ends = [], []
    for trades in trades_by_variant.values():
        if trades.empty:
            continue
        starts.append(trades["entry_time"].min())
        ends.append(trades["entry_time"].max())
    if not starts:
        return []
    return list(pd.period_range(min(starts).to_period("M"), max(ends).to_period("M"), freq="M"))


def draw_block_starts(n_months: int, block_months: int, rng: np.random.Generator) -> np.ndarray:
    """Zieht so viele Block-Startpositionen, dass die zusammengesetzte
    Zeitachse mindestens so lang ist wie das Original."""
    n_blocks = int(np.ceil(n_months / block_months))
    return rng.integers(0, n_months, size=n_blocks)


def resample(trades: pd.DataFrame, months: list, block_starts: np.ndarray,
              block_months: int) -> pd.DataFrame:
    """
    Baut aus `trades` eine neue Historie gemaess der gezogenen Bloecke.

    Trades werden ihrem Einstiegs-MONAT zugeordnet; jeder Zielmonat
    uebernimmt die Trades seines Quellmonats, mit um die Monatsdifferenz
    verschobenen Ein- und Ausstiegszeitpunkten. Die Haltedauer jedes
    Trades bleibt damit exakt erhalten.

    Ein Trade, der ueber das Ende seines Blocks hinausreicht, ragt in den
    Folgeblock hinein - dieselbe Naeherung wie bei jedem Block-Bootstrap
    auf pfadabhaengigen Groessen, und die konservative Richtung: sie
    erhaelt Ueberlappung und Kapitalbindung, statt Positionen kuenstlich
    an Blockgrenzen zu schliessen.
    """
    if trades.empty:
        return trades

    by_month = {period: group for period, group in
                trades.groupby(trades["entry_time"].dt.to_period("M"))}
    n_months = len(months)

    pieces = []
    target = 0
    for start in block_starts:
        for step in range(block_months):
            if target >= n_months:
                break
            source_month = months[(int(start) + step) % n_months]
            group = by_month.get(source_month)
            if group is not None and not group.empty:
                offset = months[target].start_time - source_month.start_time
                piece = group.copy()
                piece["entry_time"] = piece["entry_time"] + offset
                piece["exit_time"] = piece["exit_time"] + offset
                pieces.append(piece)
            target += 1
        if target >= n_months:
            break

    if not pieces:
        return trades.iloc[0:0]
    # kind="stable" ist hier NICHT optional: bei Tageskerzen teilen sich viele
    # Trades denselben Einstiegszeitpunkt, und die Reihenfolge bei Gleichstand
    # entscheidet, welcher Trade das freie Kapital zuerst bekommt. Der
    # pandas-Standard (quicksort) ist nicht stabil und wuerde die Reihenfolge
    # unvorhersehbar variieren - der Schnellpfad koennte dann gar nicht
    # verhaltensgleich sein, und zwei Laeufe desselben Replikats muessten sich
    # nicht einmal untereinander gleichen.
    return (pd.concat(pieces, ignore_index=True)
            .sort_values("entry_time", kind="stable").reset_index(drop=True))


# ---------------------------------------------------------------------------
# Schnellpfad
# ---------------------------------------------------------------------------
# Der Bootstrap rechnet 2000 Replikate x 4 Varianten x 3 Zeitraeume, also rund
# 24.000 Portfolio-Simulationen. Mit dem pandas-basierten Referenzcode
# (vbc_core.simulate_weighted_portfolio, iterrows + .loc je Ereignis) dauert
# das ueber eine halbe Stunde - dieselbe Performance-Falle, die im Projekt
# schon einmal bei backtest_trend.py aufgetreten ist (dort >60s Timeout,
# behoben durch Umstellung auf NumPy-Arrays).
#
# Die Funktionen unten sind reine Umsetzungen DERSELBEN Logik auf NumPy.
# Sie werden NICHT als neue Methodik behandelt: test_vbc_core.py prueft, dass
# sie auf echten Daten bit-genau dieselben Ergebnisse liefern wie der
# Referenzcode. Die im Bericht genannten Punktschaetzer stammen weiterhin
# ausschliesslich aus dem Referenzpfad; der Schnellpfad wird nur fuer die
# Streuung um sie herum benutzt.

def inverse_vol_weights_fast(vols: np.ndarray, clip_factor: float) -> np.ndarray:
    """NumPy-Umsetzung von vbc_core.compute_inverse_vol_weights."""
    with np.errstate(divide="ignore", invalid="ignore"):
        inv = np.where(vols == 0, np.nan, 1.0 / vols)
    inv = np.where(np.isfinite(inv), inv, np.nan)

    valid = inv[~np.isnan(inv)]
    if valid.size == 0:
        return np.ones_like(vols)

    median = float(np.median(valid))
    clipped = np.clip(inv, median / clip_factor, median * clip_factor)
    if np.isnan(clipped).any():
        fill = np.nanmean(clipped)
        clipped = np.where(np.isnan(clipped), fill, clipped)

    mean = float(np.mean(clipped))
    if not np.isfinite(mean) or mean <= 0:
        return np.ones_like(vols)
    return clipped / mean


def simulate_fast(entry_ns: np.ndarray, exit_ns: np.ndarray, pnl: np.ndarray,
                   weights: np.ndarray, starting_capital: float, allocation_frac: float,
                   max_concurrent) -> tuple:
    """
    NumPy-Umsetzung von vbc_core.simulate_weighted_portfolio, reduziert auf
    die beiden Rueckgabewerte, die der Bootstrap braucht (Gesamtrendite und
    Max Drawdown). Ereignis-Reihenfolge, Kapitalpruefung, Positionslimit und
    die Rundung von `capital_after` auf zwei Nachkommastellen sind exakt
    uebernommen - Letzteres ist kein Kosmetikdetail, sondern geht ueber die
    Drawdown-Berechnung in das Ergebnis ein.
    """
    n = len(pnl)
    if n == 0:
        return 0.0, 0.0

    idx = np.concatenate([np.arange(n), np.arange(n)])
    times = np.concatenate([entry_ns, exit_ns])
    is_entry = np.concatenate([np.ones(n, dtype=np.int8), np.zeros(n, dtype=np.int8)])
    order = np.lexsort((is_entry, times))   # primaer Zeit, bei Gleichstand Exits zuerst

    capital = starting_capital
    open_positions = {}
    peak = starting_capital
    max_dd = 0.0

    for pos in order:
        i = idx[pos]
        if is_entry[pos]:
            if max_concurrent is not None and len(open_positions) >= max_concurrent:
                continue
            free = capital - sum(open_positions.values())
            allocation = capital * allocation_frac * weights[i]
            if allocation > free:
                continue
            open_positions[i] = allocation
        else:
            allocation = open_positions.pop(i, None)
            if allocation is None:
                continue
            capital += allocation * (pnl[i] / 100.0)
            rounded = round(capital, 2)
            if rounded > peak:
                peak = rounded
            drawdown = (rounded - peak) / peak * 100
            if drawdown < max_dd:
                max_dd = drawdown

    total_return = (round(capital, 2) / starting_capital - 1) * 100
    return total_return, round(max_dd, 2)


def prepare_arrays(trades: pd.DataFrame, months: list) -> dict:
    """Zerlegt einen Trade-Satz einmalig in NumPy-Arrays plus eine Zuordnung
    Monat -> Trade-Indizes, damit im Replikat-Loop nur noch indiziert und
    verschoben werden muss (kein DataFrame-Aufbau je Replikat)."""
    if trades.empty:
        return {"empty": True}
    entry = trades["entry_time"].to_numpy("datetime64[ns]").astype("int64")
    exit_ = trades["exit_time"].to_numpy("datetime64[ns]").astype("int64")
    periods = trades["entry_time"].dt.to_period("M")
    month_pos = {month: i for i, month in enumerate(months)}
    bucket = np.array([month_pos.get(p, -1) for p in periods], dtype=np.int64)
    by_month = [np.flatnonzero(bucket == i) for i in range(len(months))]
    month_start_ns = np.array([m.start_time.value for m in months], dtype=np.int64)
    return {
        "empty": False,
        "entry": entry, "exit": exit_,
        "pnl": trades["pnl_pct"].to_numpy(dtype=float),
        "vol": trades["vol_at_entry"].to_numpy(dtype=float),
        "by_month": by_month, "month_start_ns": month_start_ns,
    }


def resample_fast(arrays: dict, block_starts: np.ndarray, block_months: int,
                   n_months: int) -> tuple:
    """Schnellpfad-Gegenstueck zu resample(): liefert (entry_ns, exit_ns,
    pnl, vol) der neu zusammengesetzten Historie."""
    picks, offsets = [], []
    target = 0
    for start in block_starts:
        for step in range(block_months):
            if target >= n_months:
                break
            source = (int(start) + step) % n_months
            members = arrays["by_month"][source]
            if members.size:
                picks.append(members)
                offsets.append(np.full(members.size,
                                       arrays["month_start_ns"][target]
                                       - arrays["month_start_ns"][source], dtype=np.int64))
            target += 1
        if target >= n_months:
            break

    if not picks:
        empty = np.empty(0)
        return empty, empty, empty, empty

    sel = np.concatenate(picks)
    off = np.concatenate(offsets)
    entry = arrays["entry"][sel] + off
    order = np.argsort(entry, kind="stable")
    return (entry[order], arrays["exit"][sel][order] + off[order],
            arrays["pnl"][sel][order], arrays["vol"][sel][order])


def evaluate_replicate(trades: pd.DataFrame, use_vol: bool, cfg: dict,
                        starting_capital: float) -> dict:
    if trades.empty:
        return None
    weights = (compute_inverse_vol_weights(trades["vol_at_entry"], cfg["clip_factor"])
               if use_vol else pd.Series(1.0, index=trades.index))
    result = simulate_weighted_portfolio(trades, starting_capital,
                                          cfg["allocation_pct"] / 100.0, weights,
                                          cfg["max_concurrent"])
    total_return = (result["final_capital"] / starting_capital - 1) * 100
    max_dd = calculate_max_drawdown(result["equity_curve"], starting_capital)
    return {"total_return_pct": total_return, "max_drawdown_pct": max_dd,
            "calmar_ratio": calmar_ratio(total_return, max_dd)}


def percentile_summary(values: np.ndarray, label: str) -> dict:
    finite = values[np.isfinite(values)]
    if finite.size == 0:
        return {"label": label, "n_valid": 0}
    return {
        "label": label,
        "n_valid": int(finite.size),
        "mean": round(float(np.mean(finite)), 3),
        "median": round(float(np.median(finite)), 3),
        "ci_low": round(float(np.percentile(finite, 2.5)), 3),
        "ci_high": round(float(np.percentile(finite, 97.5)), 3),
        "share_above_zero_pct": round(float((finite > 0).mean() * 100), 1),
    }


def run(sets: dict, cfg: dict, lo, hi, include_hi: bool, n_replicates: int,
        block_months: int, seed: int, starting_capital: float) -> dict:
    """
    Fuehrt den Block-Bootstrap fuer EINEN Zeitabschnitt durch und gibt
    Perzentil-Intervalle fuer jede Variante sowie fuer die paarweisen
    Differenzen zurueck.

    Ausgewiesen werden die Differenzen, die den Aussagen des Berichts
    entsprechen: jede Variante gegen die Baseline, und zusaetzlich
    "kombiniert gegen Trailing allein" (die Frage, ob die Kombination
    ueberhaupt etwas beitraegt).
    """
    trades_by_variant = {}
    for variant in VARIANTS:
        trades = sets[USES_TRAILING[variant]]
        mask = trades["entry_time"] >= lo
        mask &= (trades["entry_time"] <= hi) if include_hi else (trades["entry_time"] < hi)
        trades_by_variant[variant] = trades[mask].reset_index(drop=True)

    months = month_span(trades_by_variant)
    if len(months) < 2 * block_months:
        return {"error": f"zu kurzer Zeitraum fuer den Bootstrap "
                         f"({len(months)} Monate, Blocklaenge {block_months})"}

    rng = np.random.default_rng(seed)
    collected = {variant: {"total_return_pct": [], "max_drawdown_pct": [], "calmar_ratio": []}
                 for variant in VARIANTS}

    arrays_by_variant = {variant: prepare_arrays(trades, months)
                         for variant, trades in trades_by_variant.items()}
    allocation_frac = cfg["allocation_pct"] / 100.0
    n_months = len(months)

    for _ in range(n_replicates):
        block_starts = draw_block_starts(n_months, block_months, rng)
        for variant in VARIANTS:
            arrays = arrays_by_variant[variant]
            if arrays["empty"]:
                for key in collected[variant]:
                    collected[variant][key].append(np.nan)
                continue
            entry, exit_, pnl, vol = resample_fast(arrays, block_starts, block_months, n_months)
            if entry.size == 0:
                for key in collected[variant]:
                    collected[variant][key].append(np.nan)
                continue
            weights = (inverse_vol_weights_fast(vol, cfg["clip_factor"])
                       if USES_VOL_WEIGHTS[variant] else np.ones_like(pnl))
            total_return, max_dd = simulate_fast(entry, exit_, pnl, weights, starting_capital,
                                                  allocation_frac, cfg["max_concurrent"])
            calmar = calmar_ratio(total_return, max_dd)
            collected[variant]["total_return_pct"].append(total_return)
            collected[variant]["max_drawdown_pct"].append(max_dd)
            collected[variant]["calmar_ratio"].append(np.nan if calmar is None else calmar)

    arrays = {variant: {key: np.asarray(values, dtype=float)
                        for key, values in metrics.items()}
              for variant, metrics in collected.items()}

    # Calmar-Replikate mit verschwindendem Drawdown verwerfen (siehe Konstante oben)
    dropped = {}
    for variant in VARIANTS:
        unusable = np.abs(arrays[variant]["max_drawdown_pct"]) < MIN_ABS_DRAWDOWN_PCT
        dropped[variant] = int(unusable.sum())
        arrays[variant]["calmar_ratio"] = np.where(unusable, np.nan, arrays[variant]["calmar_ratio"])

    per_variant = {
        variant: {key: percentile_summary(arrays[variant][key], key)
                  for key in ("total_return_pct", "max_drawdown_pct", "calmar_ratio")}
        for variant in VARIANTS
    }

    comparisons = [(variant, VARIANT_BASELINE) for variant in VARIANTS if variant != VARIANT_BASELINE]
    comparisons.append((VARIANT_COMBINED, VARIANT_TRAILING))

    differences = {}
    for left, right in comparisons:
        differences[f"{left}_minus_{right}"] = {
            key: percentile_summary(arrays[left][key] - arrays[right][key], key)
            for key in ("total_return_pct", "max_drawdown_pct", "calmar_ratio")
        }

    return {
        "n_replicates": n_replicates,
        "block_months": block_months,
        "months_in_period": len(months),
        "blocks_per_replicate": int(np.ceil(len(months) / block_months)),
        "seed": seed,
        "calmar_replicates_dropped_near_zero_drawdown": dropped,
        "trades_in_period": {variant: int(len(trades)) for variant, trades in trades_by_variant.items()},
        "per_variant": per_variant,
        "differences": differences,
    }

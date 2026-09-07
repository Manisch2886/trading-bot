"""
Entscheidungsgrundlage: Buy-and-Hold, Streuung, Unsicherheit
==================================================================
Nachtrag zur Trailing-Stop-Untersuchung. Die erste Fassung berichtete
Punktschaetzer ohne Aussenreferenz und ohne Unsicherheitsmass - gut genug,
um zu beschreiben WAS gemessen wurde, aber nicht, um darauf eine
Entscheidung zu stuetzen. Dieses Modul ergaenzt drei Dinge:

  1. BUY-AND-HOLD - laut CLAUDE.md Pflichtbestandteil der Validierungskette
     (Backtest -> Walk-Forward -> Equity-Simulation -> Buy-and-Hold). Fehlte
     in der ersten Fassung vollstaendig.
  2. REIHENFOLGE-SENSITIVITAET - wie stark haengt das Ergebnis an der
     willkuerlichen Reihenfolge gleichzeitiger Einstiege?
  3. BLOCK-BOOTSTRAP - Konfidenzintervalle fuer die Variantenunterschiede.

Punkt 2 und 3 wurden im Rahmen der Vertiefungsstudie
research/vbc_deepdive/ entwickelt (dort bootstrap.py) und hier auf die
drei Stop-Varianten dieser Untersuchung uebertragen. Der Unterschied: dort
gibt es zusaetzlich Positionsgewichte, hier nicht - die Simulation ist
entsprechend einfacher.

WICHTIG - reine Backtest-Untersuchung: wird von KEINEM Live-Skript
importiert und aendert nichts an strategies/.
"""

import numpy as np
import pandas as pd

# Ein Calmar-Wert wird unbrauchbar, wenn der Drawdown gegen null geht.
# Betroffene Replikate werden verworfen und ihre Anzahl ausgewiesen - bei den
# beiden Elliott-Wave-Bots waere das der Regelfall, weshalb fuer sie ohnehin
# kein Bootstrap gerechnet wird (siehe BERICHT.md, Abschnitt 5.4).
MIN_ABS_DRAWDOWN_PCT = 0.10


# ===========================================================================
# 1. Buy-and-Hold
# ===========================================================================
def buy_and_hold(all_data: dict, starting_capital: float) -> dict:
    """
    Gleichgewichtete Buy-and-Hold-Simulation: Startkapital zu gleichen
    Teilen auf alle Symbole, Kauf zum ersten verfuegbaren Schlusskurs,
    Halten bis zum letzten; Max Drawdown aus der zusammengefuehrten
    Portfolio-Kurve.

    WORTGETREUE UEBERNAHME der im Projekt bereits dreifach vorhandenen,
    untereinander identischen Funktion
    `buy_and_hold_benchmark.py::calculate_buy_and_hold`
    (elliott_wave_stocks, volatility_breakout, volatility_breakout_crypto -
    verglichen, die drei Fassungen sind funktional gleich). Sie wird hier
    nachgebildet statt importiert, weil zwei der fuenf betroffenen Bots
    (`elliott_wave`, `t3_supertrend`) gar KEIN eigenes B&H-Skript haben -
    ohne eine gemeinsame Implementierung gaebe es fuer sie keine
    Aussenreferenz. `verify_baseline.py` prueft die Uebereinstimmung gegen
    die drei Bots, die eine eigene Fassung besitzen.

    Inklusive der dortigen Datenqualitaets-Absicherung: ein Symbol mit
    fehlerhaftem Kurs wird uebersprungen, sein Kapitalanteil aber als
    unveraendertes Cash zur Endsumme addiert (sonst waere das Endkapital
    kuenstlich zu niedrig - der APH/NaN-Praezedenzfall aus der
    Projekt-Historie).
    """
    num_symbols = len(all_data)
    if num_symbols == 0:
        return None
    capital_per_symbol = starting_capital / num_symbols

    daily_values, final_value, skipped = [], 0.0, []
    for symbol, df in all_data.items():
        df = df.sort_values("open_time").reset_index(drop=True)
        entry_price = df["close"].iloc[0]
        exit_price = df["close"].iloc[-1]
        if pd.isna(entry_price) or pd.isna(exit_price) or entry_price == 0:
            skipped.append(symbol)
            continue

        shares = capital_per_symbol / entry_price
        series = df[["open_time", "close"]].copy()
        series["value"] = series["close"] * shares
        daily_values.append(series.set_index("open_time")["value"])
        final_value += exit_price * shares

    if skipped:
        final_value += capital_per_symbol * len(skipped)
    if not daily_values:
        return None

    curve = pd.concat(daily_values, axis=1).sort_index().ffill().sum(axis=1)
    running_max = curve.cummax()
    return {
        "final_capital": round(final_value, 2),
        "total_return_pct": round((final_value / starting_capital - 1) * 100, 2),
        "max_drawdown_pct": round(float(((curve - running_max) / running_max * 100).min()), 2),
        "num_symbols": num_symbols,
        "num_skipped": len(skipped),
    }


def buy_and_hold_window(price_by_symbol: dict, lo, hi, starting_capital: float) -> dict:
    """Buy-and-Hold fuer ein Zeitfenster - schneidet nur die Eingabe zu,
    an der Rechnung selbst wird nichts geaendert."""
    windowed = {}
    for symbol, df in price_by_symbol.items():
        piece = df[(df["open_time"] >= lo) & (df["open_time"] <= hi)]
        if len(piece) >= 2:
            windowed[symbol] = piece.reset_index(drop=True)
    return buy_and_hold(windowed, starting_capital) if windowed else None


# ===========================================================================
# 2. Schnelle Portfolio-Simulation (fuer Bootstrap und Permutationen)
# ===========================================================================
def simulate_fast(entry_ns: np.ndarray, exit_ns: np.ndarray, pnl: np.ndarray,
                   starting_capital: float, allocation_frac: float, max_concurrent) -> tuple:
    """
    NumPy-Umsetzung von atr_core.simulate_portfolio, reduziert auf
    Gesamtrendite und Max Drawdown. Ereignis-Reihenfolge (Exits vor Entries
    bei Gleichstand), Kapitalpruefung, Positionslimit und die Rundung von
    `capital_after` auf zwei Nachkommastellen sind exakt uebernommen -
    Letzteres geht ueber die Drawdown-Berechnung ins Ergebnis ein.

    Noetig, weil Bootstrap und Permutationstest zusammen mehrere
    zehntausend Simulationen brauchen; der pandas-basierte Referenzcode
    (iterrows + .loc je Ereignis) waere dafuer um Groessenordnungen zu
    langsam. test_atr_core.py prueft die bitgenaue Uebereinstimmung.
    """
    n = len(pnl)
    if n == 0:
        return 0.0, 0.0

    idx = np.concatenate([np.arange(n), np.arange(n)])
    times = np.concatenate([entry_ns, exit_ns])
    is_entry = np.concatenate([np.ones(n, dtype=np.int8), np.zeros(n, dtype=np.int8)])
    order = np.lexsort((is_entry, times))

    capital = starting_capital
    open_positions = {}
    peak, max_dd = starting_capital, 0.0

    for pos in order:
        i = idx[pos]
        if is_entry[pos]:
            if max_concurrent is not None and len(open_positions) >= max_concurrent:
                continue
            allocation = capital * allocation_frac
            if allocation > capital - sum(open_positions.values()):
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

    return (round(capital, 2) / starting_capital - 1) * 100, round(max_dd, 2)


def calmar(total_return_pct: float, max_drawdown_pct: float):
    if max_drawdown_pct is None or abs(max_drawdown_pct) < 1e-12:
        return None
    return round(total_return_pct / abs(max_drawdown_pct), 2)


# ===========================================================================
# 3. Reihenfolge-Sensitivitaet
# ===========================================================================
def tie_order_sensitivity(trades_by_variant: dict, allocation_frac: float, max_concurrent,
                           starting_capital: float, n_permutations: int, seed: int) -> dict:
    """
    Wie stark haengt das Ergebnis an der Reihenfolge gleichzeitiger
    Einstiege?

    Die Portfolio-Simulation vergibt Kapital sequenziell. Sind Kapital oder
    MAX_CONCURRENT_POSITIONS knapp, entscheidet die Reihenfolge innerhalb
    desselben Zeitstempels darueber, WELCHER Trade ausgefuehrt wird und
    welcher wegfaellt. Diese Reihenfolge ist inhaltlich willkuerlich (sie
    ergibt sich aus der Symbol-Reihenfolge beim Einlesen und dem
    Sortierverfahren), wirkt aber real.

    Besonders relevant bei Bots auf TAGESKERZEN: dort entstehen an einem Tag
    regelmaessig mehrere Signale mit identischem Zeitstempel. Bei 1h- oder
    4h-Kerzen ist der Effekt naturgemaess kleiner - die Kennzahl
    `share_sharing_entry_timestamp_pct` weist das je Bot aus.

    Ein breiter Streubereich entwertet einen Vergleich nur dann, wenn sich
    die Bereiche zweier Varianten UEBERLAPPEN. Liegen sie auseinander, ist
    der Unterschied groesser als die Willkuer.
    """
    rng = np.random.default_rng(seed)
    out = {}
    for variant, trades in trades_by_variant.items():
        if trades is None or trades.empty:
            continue
        entry = trades["entry_time"].to_numpy("datetime64[ns]").astype("int64")
        exit_ = trades["exit_time"].to_numpy("datetime64[ns]").astype("int64")
        pnl = trades["pnl_pct"].to_numpy(dtype=float)

        returns, drawdowns, calmars = [], [], []
        for _ in range(n_permutations):
            perm = rng.permutation(len(trades))
            order = perm[np.argsort(entry[perm], kind="stable")]
            total_return, max_dd = simulate_fast(entry[order], exit_[order], pnl[order],
                                                  starting_capital, allocation_frac, max_concurrent)
            returns.append(total_return)
            drawdowns.append(max_dd)
            value = calmar(total_return, max_dd)
            calmars.append(np.nan if value is None else value)

        shared = int(trades["entry_time"].duplicated(keep=False).sum())
        out[variant] = {
            "n_permutations": n_permutations,
            "trades": int(len(trades)),
            "trades_sharing_entry_timestamp": shared,
            "share_sharing_entry_timestamp_pct": round(shared / len(trades) * 100, 1),
            "largest_same_timestamp_group": int(trades["entry_time"].value_counts().max()),
            "total_return_pct": _spread(returns),
            "max_drawdown_pct": _spread(drawdowns),
            "calmar_ratio": _spread(calmars),
        }
    return out


def _spread(values) -> dict:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return None
    return {"min": round(float(arr.min()), 2), "median": round(float(np.median(arr)), 2),
            "max": round(float(arr.max()), 2),
            "ci_low": round(float(np.percentile(arr, 2.5)), 2),
            "ci_high": round(float(np.percentile(arr, 97.5)), 2)}


# ===========================================================================
# 4. Block-Bootstrap
# ===========================================================================
def month_span(trades_by_variant: dict) -> list:
    starts, ends = [], []
    for trades in trades_by_variant.values():
        if trades is None or trades.empty:
            continue
        starts.append(trades["entry_time"].min())
        ends.append(trades["entry_time"].max())
    if not starts:
        return []
    return list(pd.period_range(min(starts).to_period("M"), max(ends).to_period("M"), freq="M"))


def prepare_arrays(trades: pd.DataFrame, months: list) -> dict:
    if trades is None or trades.empty:
        return {"empty": True}
    month_pos = {month: i for i, month in enumerate(months)}
    bucket = np.array([month_pos.get(p, -1) for p in trades["entry_time"].dt.to_period("M")],
                      dtype=np.int64)
    return {
        "empty": False,
        "entry": trades["entry_time"].to_numpy("datetime64[ns]").astype("int64"),
        "exit": trades["exit_time"].to_numpy("datetime64[ns]").astype("int64"),
        "pnl": trades["pnl_pct"].to_numpy(dtype=float),
        "by_month": [np.flatnonzero(bucket == i) for i in range(len(months))],
        "month_start_ns": np.array([m.start_time.value for m in months], dtype=np.int64),
    }


def resample(arrays: dict, block_starts: np.ndarray, block_months: int, n_months: int) -> tuple:
    """Setzt aus den gezogenen Bloecken eine neue, gleich lange Historie
    zusammen. Die Zeitstempel werden um die Differenz zwischen Quell- und
    Zielmonat verschoben, sodass die Haltedauer jedes Trades exakt erhalten
    bleibt und eine gueltige chronologische Historie entsteht."""
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
        return empty, empty, empty

    sel, off = np.concatenate(picks), np.concatenate(offsets)
    entry = arrays["entry"][sel] + off
    order = np.argsort(entry, kind="stable")
    return entry[order], arrays["exit"][sel][order] + off[order], arrays["pnl"][sel][order]


def block_bootstrap(trades_by_variant: dict, allocation_frac: float, max_concurrent,
                     starting_capital: float, n_replicates: int, block_months: int,
                     seed: int, comparisons: list) -> dict:
    """
    Zirkulaerer Moving-Block-Bootstrap ueber Kalendermonate.

    Ein Bootstrap ueber EINZELNE Trades waere falsch: die Simulation ist
    pfadabhaengig (gebundenes Kapital, Positionslimit, Zinseszins) und der
    Max Drawdown eine Eigenschaft der zeitlichen REIHENFOLGE. Bloecke
    erhalten die lokale Struktur; nur ihre Abfolge wird neu gewuerfelt.
    "Zirkulaer" heisst, dass Bloecke ueber das Ende hinaus wieder am Anfang
    ansetzen duerfen - sonst waeren die Randmonate unterrepraesentiert.

    GEPAART: alle Varianten werden je Replikat auf DERSELBEN gezogenen
    Zeitachse ausgewertet. Die Unsicherheit der Marktphasen-Auswahl kuerzt
    sich damit aus der Differenz zweier Varianten weitgehend heraus - genau
    das, was hier interessiert.

    Was das Verfahren NICHT leistet: es quantifiziert die Unsicherheit aus
    der begrenzten Laenge und Zusammensetzung der vorliegenden Historie. Es
    sagt nichts ueber Regimewechsel, die darin nicht vorkommen.
    """
    months = month_span(trades_by_variant)
    if len(months) < 2 * block_months:
        return {"error": f"zu kurzer Zeitraum ({len(months)} Monate, Blocklaenge {block_months})"}

    rng = np.random.default_rng(seed)
    arrays = {variant: prepare_arrays(trades, months)
              for variant, trades in trades_by_variant.items()}
    collected = {variant: {"total_return_pct": [], "max_drawdown_pct": [], "calmar_ratio": []}
                 for variant in trades_by_variant}
    n_months = len(months)

    for _ in range(n_replicates):
        n_blocks = int(np.ceil(n_months / block_months))
        block_starts = rng.integers(0, n_months, size=n_blocks)
        for variant in trades_by_variant:
            if arrays[variant]["empty"]:
                for key in collected[variant]:
                    collected[variant][key].append(np.nan)
                continue
            entry, exit_, pnl = resample(arrays[variant], block_starts, block_months, n_months)
            if entry.size == 0:
                for key in collected[variant]:
                    collected[variant][key].append(np.nan)
                continue
            total_return, max_dd = simulate_fast(entry, exit_, pnl, starting_capital,
                                                  allocation_frac, max_concurrent)
            value = calmar(total_return, max_dd)
            collected[variant]["total_return_pct"].append(total_return)
            collected[variant]["max_drawdown_pct"].append(max_dd)
            collected[variant]["calmar_ratio"].append(np.nan if value is None else value)

    data = {variant: {key: np.asarray(values, dtype=float) for key, values in metrics.items()}
            for variant, metrics in collected.items()}

    dropped = {}
    for variant in data:
        unusable = np.abs(data[variant]["max_drawdown_pct"]) < MIN_ABS_DRAWDOWN_PCT
        dropped[variant] = int(unusable.sum())
        data[variant]["calmar_ratio"] = np.where(unusable, np.nan, data[variant]["calmar_ratio"])

    keys = ("total_return_pct", "max_drawdown_pct", "calmar_ratio")
    return {
        "n_replicates": n_replicates,
        "block_months": block_months,
        "months_in_period": n_months,
        "seed": seed,
        "calmar_replicates_dropped_near_zero_drawdown": dropped,
        "per_variant": {variant: {key: _percentiles(data[variant][key]) for key in keys}
                        for variant in data},
        "differences": {f"{left}_minus_{right}":
                        {key: _percentiles(data[left][key] - data[right][key]) for key in keys}
                        for left, right in comparisons},
    }


def _percentiles(values: np.ndarray) -> dict:
    finite = values[np.isfinite(values)]
    if finite.size == 0:
        return {"n_valid": 0}
    return {
        "n_valid": int(finite.size),
        "median": round(float(np.median(finite)), 3),
        "ci_low": round(float(np.percentile(finite, 2.5)), 3),
        "ci_high": round(float(np.percentile(finite, 97.5)), 3),
        "share_above_zero_pct": round(float((finite > 0).mean() * 100), 1),
    }

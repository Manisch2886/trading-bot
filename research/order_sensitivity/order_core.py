"""
Kern-Modul: Reihenfolge-Empfindlichkeit bei gleichzeitigen Signalen
=========================================================================
Untersucht, ob die URSPRUENGLICHEN, bereits als validiert geltenden
Backtests der 9 Bots von einer Willkuer betroffen sind, die bisher
niemandem aufgefallen ist.

DER MECHANISMUS
---------------
Alle 9 Bots simulieren ihr Portfolio mit derselben ereignisbasierten
Schleife (`equity_simulation.py::simulate_portfolio`). Sie verarbeitet
Entry- und Exit-Ereignisse chronologisch und vergibt Kapital SEQUENZIELL:

    events.sort(key=lambda e: (e[0], e[1] != "exit"))

Bei GLEICHEM Zeitstempel ist diese Sortierung stabil - die Reihenfolge
entspricht also der Zeilenreihenfolge des Trade-DataFrames, und die
wiederum der Reihenfolge, in der `collect_all_trades()` die Symbole
durchlaufen hat (Reihenfolge der Symbolliste in der Konfigurationsdatei).

Solange Kapital und `MAX_CONCURRENT_POSITIONS` fuer alle gleichzeitigen
Signale reichen, ist das folgenlos. Reichen sie NICHT, entscheidet diese
Reihenfolge darueber, WELCHE Signale zu Trades werden und welche
wegfallen - und damit ueber das Ergebnis. Die Reihenfolge ist inhaltlich
willkuerlich: sie wurde nie bewusst gewaehlt, sondern ist ein Nebenprodukt
der Symbol-Reihenfolge.

WAS HIER GEMESSEN WIRD
----------------------
500 zufaellige Permutationen der Verarbeitungsreihenfolge bei
gleichzeitigen Signalen, auf den UNVERAENDERTEN Original-Trades des
jeweiligen Bots. Alles andere bleibt gleich: dieselben Kursdaten,
dieselben Signale, dieselben Parameter, dieselbe Simulationslogik.

WICHTIG - reine Untersuchung: dieses Modul wird von KEINEM Live-Skript
importiert. Es RUFT die bot-eigenen Funktionen auf, veraendert sie aber
nicht. Es fuehrt auch KEINE "korrekte" Tie-Breaking-Regel ein - das waere
eine eigene Aufgabe.
"""

import numpy as np
import pandas as pd

SKIP_NONE = 0
SKIP_POSITION_LIMIT = 1
SKIP_CAPITAL = 2


def permuted(trades: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """
    Permutiert die Verarbeitungsreihenfolge bei GLEICHZEITIGEN Signalen -
    und nur dort.

    Vorgehen: Zeilen zufaellig mischen, danach STABIL nach `entry_time`
    sortieren. Die chronologische Abfolge bleibt damit exakt erhalten;
    verschoben wird ausschliesslich die Reihenfolge innerhalb identischer
    Zeitstempel. Die Simulation sieht dieselben Trades zu denselben
    Zeitpunkten - nur die willkuerliche Rangfolge bei Gleichstand ist eine
    andere.

    kind="stable" ist hier zwingend: pandas' Standard-Sortierung
    (quicksort) ist nicht stabil und wuerde die gemischte Reihenfolge
    teilweise wieder ueberschreiben, sodass nicht mehr klar waere, was
    eigentlich variiert wurde.
    """
    shuffled = trades.iloc[rng.permutation(len(trades))]
    return shuffled.sort_values("entry_time", kind="stable").reset_index(drop=True)


def simulate_fast(entry_ns: np.ndarray, exit_ns: np.ndarray, pnl: np.ndarray,
                   starting_capital: float, allocation_pct: float,
                   max_concurrent_positions) -> dict:
    """
    NumPy-Umsetzung der in allen 9 Bots gleichlautenden
    `simulate_portfolio()`. Ereignis-Reihenfolge, Kapitalpruefung,
    Positionslimit und die Rundung von `capital_after` auf zwei
    Nachkommastellen sind exakt uebernommen - Letzteres geht ueber die
    Drawdown-Berechnung ins Ergebnis ein.

    Zusaetzlich zum Original werden zwei Dinge mitgefuehrt, die dieses
    Modul braucht und die es dort nicht gibt:
      * `executed` - Maske, WELCHE Trades ausgefuehrt wurden (nicht nur
        wie viele). Erst damit laesst sich messen, ob ueber die
        Permutationen hinweg immer DIESELBEN Trades ausgefuehrt werden.
      * `skip_reason` - Positionslimit oder Kapitalmangel. Das Original
        zaehlt beides gemeinsam; fuer die Frage "wie oft fuehrt ein
        geteilter Zeitstempel tatsaechlich zu einer kapitalbedingten
        Ablehnung" muss man sie trennen.

    `run_one_bot.py` prueft je Bot auf den ECHTEN Daten, dass diese
    Umsetzung bit-genau dieselben Kennzahlen liefert wie die bot-eigene
    Funktion. Die Punktschaetzer im Bericht stammen aus der bot-eigenen
    Funktion; der Schnellpfad liefert nur die Streuung darum herum.
    """
    n = len(pnl)
    if n == 0:
        return {"total_return_pct": 0.0, "max_drawdown_pct": 0.0,
                "executed": np.zeros(0, dtype=bool), "skip_reason": np.zeros(0, dtype=np.int8)}

    idx = np.concatenate([np.arange(n), np.arange(n)])
    times = np.concatenate([entry_ns, exit_ns])
    is_entry = np.concatenate([np.ones(n, dtype=np.int8), np.zeros(n, dtype=np.int8)])
    order = np.lexsort((is_entry, times))   # primaer Zeit, bei Gleichstand Exits zuerst

    capital = starting_capital
    open_positions = {}
    peak, max_dd = starting_capital, 0.0
    executed = np.zeros(n, dtype=bool)
    skip_reason = np.zeros(n, dtype=np.int8)

    for pos in order:
        i = idx[pos]
        if is_entry[pos]:
            if max_concurrent_positions is not None and len(open_positions) >= max_concurrent_positions:
                skip_reason[i] = SKIP_POSITION_LIMIT
                continue
            allocation = capital * allocation_pct
            if allocation > capital - sum(open_positions.values()):
                skip_reason[i] = SKIP_CAPITAL
                continue
            open_positions[i] = allocation
            executed[i] = True
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

    return {
        "total_return_pct": (round(capital, 2) / starting_capital - 1) * 100,
        "max_drawdown_pct": round(max_dd, 2),
        "executed": executed,
        "skip_reason": skip_reason,
    }


def calmar(total_return_pct: float, max_drawdown_pct: float):
    """Calmar-Konvention aller bisherigen Untersuchungen: Rendite % geteilt
    durch den Betrag des Max Drawdown %. None bei Drawdown 0."""
    if max_drawdown_pct is None or abs(max_drawdown_pct) < 1e-12:
        return None
    return round(total_return_pct / abs(max_drawdown_pct), 2)


def as_arrays(trades: pd.DataFrame) -> tuple:
    return (trades["entry_time"].to_numpy("datetime64[ns]").astype("int64"),
            trades["exit_time"].to_numpy("datetime64[ns]").astype("int64"),
            trades["pnl_pct"].to_numpy(dtype=float))


def run_permutations(trades: pd.DataFrame, starting_capital: float, allocation_pct: float,
                      max_concurrent_positions, n_permutations: int, seed: int) -> dict:
    """
    Fuehrt `n_permutations` Permutationen durch und fasst die Streuung
    zusammen.

    `contested_trades` ist die eigentlich interessante Groesse: der Anteil
    der Trades, deren Ausfuehrungs-Status ueber die Permutationen hinweg
    NICHT konstant ist. Ein Bot kann eine hohe Ablehnungsquote haben und
    trotzdem unempfindlich sein - naemlich dann, wenn immer dieselben
    Trades abgelehnt werden (z. B. weil sie in einer dauerhaft
    ausgelasteten Phase liegen). Erst wenn die AUSWAHL variiert, ist die
    Reihenfolge ergebnisrelevant.
    """
    entry_ns, exit_ns, pnl = as_arrays(trades)
    rng = np.random.default_rng(seed)
    n = len(trades)

    returns, drawdowns, calmars = [], [], []
    executed_count = np.zeros(n, dtype=np.int32)
    skip_capital = np.zeros(n, dtype=np.int32)
    skip_limit = np.zeros(n, dtype=np.int32)

    for _ in range(n_permutations):
        order = rng.permutation(n)
        order = order[np.argsort(entry_ns[order], kind="stable")]
        result = simulate_fast(entry_ns[order], exit_ns[order], pnl[order],
                                starting_capital, allocation_pct, max_concurrent_positions)
        returns.append(result["total_return_pct"])
        drawdowns.append(result["max_drawdown_pct"])
        value = calmar(result["total_return_pct"], result["max_drawdown_pct"])
        calmars.append(np.nan if value is None else value)

        # Ergebnis-Masken zurueck auf die URSPRUENGLICHEN Trade-Indizes abbilden
        executed_count[order[result["executed"]]] += 1
        skip_capital[order[result["skip_reason"] == SKIP_CAPITAL]] += 1
        skip_limit[order[result["skip_reason"] == SKIP_POSITION_LIMIT]] += 1

    always = int((executed_count == n_permutations).sum())
    never = int((executed_count == 0).sum())
    contested = n - always - never

    return {
        "n_permutations": n_permutations,
        "n_trades": n,
        "total_return_pct": _spread(returns),
        "max_drawdown_pct": _spread(drawdowns),
        "calmar_ratio": _spread(calmars),
        "trades_always_executed": always,
        "trades_never_executed": never,
        "trades_contested": contested,
        "contested_share_pct": round(contested / n * 100, 1) if n else 0.0,
        "mean_skipped_capital": round(float(skip_capital.sum() / n_permutations), 1),
        "mean_skipped_position_limit": round(float(skip_limit.sum() / n_permutations), 1),
    }


def _spread(values) -> dict:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return None
    return {"min": round(float(arr.min()), 2), "median": round(float(np.median(arr)), 2),
            "max": round(float(arr.max()), 2),
            "ci_low": round(float(np.percentile(arr, 2.5)), 2),
            "ci_high": round(float(np.percentile(arr, 97.5)), 2),
            "values": arr}


def percentile_of(value, spread: dict):
    """
    Wo liegt der urspruenglich berichtete Wert innerhalb der
    Permutations-Verteilung? 50 = genau in der Mitte, 0 bzw. 100 = am
    aeussersten Rand.

    Das ist die Frage aus Punkt 3 der Aufgabenstellung: ein zentral
    liegender Wert bedeutet, dass die tatsaechlich verwendete Reihenfolge
    typisch war; ein Randwert bedeutet, dass sie eine besonders guenstige
    (oder unguenstige) Ziehung war - und damit, dass die berichtete Zahl
    die Strategie systematisch zu gut (oder zu schlecht) darstellt.
    """
    if value is None or spread is None:
        return None
    values = spread["values"]
    return round(float((values < value).mean() * 100), 1)


def timestamp_stats(trades: pd.DataFrame) -> dict:
    """Anteil der Trades, die ihren Einstiegszeitpunkt mit mindestens einem
    anderen teilen - die notwendige (aber nicht hinreichende) Bedingung
    dafuer, dass die Reihenfolge ueberhaupt eine Rolle spielen kann."""
    shared = int(trades["entry_time"].duplicated(keep=False).sum())
    counts = trades["entry_time"].value_counts()
    return {
        "n_trades": int(len(trades)),
        "trades_sharing_entry_timestamp": shared,
        "share_sharing_entry_timestamp_pct": round(shared / len(trades) * 100, 1) if len(trades) else 0.0,
        "largest_same_timestamp_group": int(counts.max()) if len(counts) else 0,
        "distinct_entry_timestamps": int(len(counts)),
    }


def strip_values(obj):
    """Entfernt die rohen Permutations-Arrays vor dem JSON-Export (sie
    dienen nur der Perzentil-Berechnung und waeren sonst riesig)."""
    if isinstance(obj, dict):
        return {key: strip_values(value) for key, value in obj.items() if key != "values"}
    if isinstance(obj, list):
        return [strip_values(item) for item in obj]
    return obj

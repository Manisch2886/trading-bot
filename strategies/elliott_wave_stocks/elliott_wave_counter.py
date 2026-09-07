"""
Phase 2b - Elliott-Wave-Zaehlung
=================================
Sucht in den Zigzag-Pivots (aus zigzag_indicator.py) nach gueltigen
5-Wellen-Impulsmustern (Welle 1-5) unter Einhaltung der drei
Elliott-Wave-Grundregeln, und bewertet Kandidaten zusaetzlich anhand
typischer Fibonacci-Verhaeltnisse.

WICHTIG: Das ist eine algorithmische Annaeherung, kein Ersatz fuer
eine vollstaendige, "offizielle" Elliott-Wave-Analyse. Die Regeln
sind objektiv, die Wellenzuordnung selbst bleibt eine Heuristik.
"""

import os
import sys
import pandas as pd

_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)

from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
RESULTS_DIR = _P["RESULTS_DIR"]


def is_valid_impulse(points: list) -> bool:
    """
    Prueft, ob 6 aufeinanderfolgende Pivots (Start + Welle 1-5) die
    drei nicht verhandelbaren Elliott-Regeln erfuellen.

    points: Liste von 6 Preisen [P0, P1, P2, P3, P4, P5]
            P0 = Start, P1 = Ende Welle1, P2 = Ende Welle2, usw.
    """
    p0, p1, p2, p3, p4, p5 = points

    wave1 = abs(p1 - p0)
    wave2 = abs(p2 - p1)
    wave3 = abs(p3 - p2)
    wave4 = abs(p4 - p3)
    wave5 = abs(p5 - p4)

    is_bullish = p1 > p0

    # Regel 1: Welle 2 darf nicht ueber den Startpunkt von Welle 1 zurueckfallen
    if is_bullish and p2 < p0:
        return False
    if not is_bullish and p2 > p0:
        return False

    # Regel 2: Welle 3 darf nie die kuerzeste von Welle 1, 3, 5 sein
    if wave3 < wave1 and wave3 < wave5:
        return False

    # Regel 3: Welle 4 darf nicht in das Preisgebiet von Welle 1 eindringen
    if is_bullish and p4 < p1:
        return False
    if not is_bullish and p4 > p1:
        return False

    return True


def fibonacci_score(points: list) -> float:
    """
    Bewertet, wie gut die Wellenverhaeltnisse zu typischen
    Fibonacci-Erwartungen passen. 1.0 = perfekte Uebereinstimmung,
    0.0 = keine Uebereinstimmung. Dient dem Optimisation Agent
    spaeter als Rankingkriterium zwischen mehreren gueltigen Kandidaten.
    """
    p0, p1, p2, p3, p4, p5 = points

    wave1 = abs(p1 - p0)
    wave2 = abs(p2 - p1)
    wave3 = abs(p3 - p2)
    wave4 = abs(p4 - p3)

    if wave1 == 0 or wave3 == 0:
        return 0.0

    # Typische Erwartungen:
    # Welle 2 retracet 50-61.8% von Welle 1
    # Welle 3 ist oft 1.618x Welle 1
    # Welle 4 retracet 23.6-38.2% von Welle 3
    w2_ratio = wave2 / wave1
    w3_ratio = wave3 / wave1
    w4_ratio = wave4 / wave3

    score = 0.0
    if 0.5 <= w2_ratio <= 0.618:
        score += 0.34
    if 1.4 <= w3_ratio <= 1.8:
        score += 0.33
    if 0.236 <= w4_ratio <= 0.382:
        score += 0.33

    return round(score, 2)


def find_impulse_waves(zigzag: pd.DataFrame, min_fib_score: float = 0.3) -> pd.DataFrame:
    """
    Schiebt ein Fenster von 6 Pivots ueber die Zigzag-Liste und prueft
    jede Kombination auf Regelkonformitaet + Fibonacci-Score.

    Rueckgabe: DataFrame aller gefundenen gueltigen Impulskandidaten,
               sortiert nach Fibonacci-Score (beste zuerst).
    """
    candidates = []
    prices = zigzag["price"].values
    times = zigzag["time"].values

    for i in range(len(zigzag) - 5):
        window = prices[i:i + 6]

        if not is_valid_impulse(list(window)):
            continue

        score = fibonacci_score(list(window))
        if score < min_fib_score:
            continue

        candidates.append({
            "start_time": times[i],
            "end_time": times[i + 5],
            "direction": "bullish" if window[1] > window[0] else "bearish",
            "wave0": window[0],
            "wave1": window[1],
            "wave2": window[2],
            "wave3": window[3],
            "wave4": window[4],
            "wave5": window[5],
            "fib_score": score,
        })

    result = pd.DataFrame(candidates)
    if not result.empty:
        result = result.sort_values("fib_score", ascending=False).reset_index(drop=True)
    return result


def remove_overlapping(impulses: pd.DataFrame) -> pd.DataFrame:
    """
    Entfernt ueberlappende Wellenmuster (gleiches Marktereignis mehrfach
    erkannt). Behaelt pro Ueberlappungsgruppe nur den Kandidaten mit dem
    besten Fibonacci-Score, damit einzelne Ereignisse nicht mehrfach als
    unabhaengige Trades in den Backtest einfliessen.
    """
    if impulses.empty:
        return impulses

    sorted_df = impulses.sort_values("start_time").reset_index(drop=True)
    kept = []

    for _, row in sorted_df.iterrows():
        overlaps_kept = False
        for i, kept_row in enumerate(kept):
            # Ueberlappung liegt vor, wenn sich die Zeitfenster schneiden
            if row["start_time"] < kept_row["end_time"] and row["end_time"] > kept_row["start_time"]:
                overlaps_kept = True
                if row["fib_score"] > kept_row["fib_score"]:
                    kept[i] = row
                break
        if not overlaps_kept:
            kept.append(row)

    result = pd.DataFrame(kept).sort_values("fib_score", ascending=False).reset_index(drop=True)
    return result


def find_causal_waves(zigzag: pd.DataFrame, min_fib_score: float = 0.3,
                       freshness_bars: int = None, direction: str = "bearish") -> pd.DataFrame:
    """
    Wellenerkennung OHNE Blick in die Zukunft - fuer den Backtest.

    --------------------------------------------------------------------
    Das Problem
    --------------------------------------------------------------------
    find_impulse_waves + remove_overlapping laufen im Backtest ueber die
    GESAMTE Historie auf einmal. remove_overlapping behaelt pro
    Ueberlappungsgruppe den Kandidaten mit dem besten Fibonacci-Score - und
    dabei kann eine SPAETERE Welle eine FRUEHERE verdraengen:

        if row["fib_score"] > kept_row["fib_score"]:
            kept[i] = row

    Live ist das unmoeglich. Der Bot haette die fruehere Welle laengst
    gehandelt, als die spaetere noch gar nicht existierte. Ein Backtest, der
    sie nachtraeglich streicht, benutzt Zukunftswissen.

    --------------------------------------------------------------------
    Die Loesung: die Live-Laeufe nachbilden
    --------------------------------------------------------------------
    Statt eine eigene, neue Auswahlregel zu erfinden, bildet diese Funktion
    nach, was forward_test.py::find_new_signals tatsaechlich tut - Lauf fuer
    Lauf:

      1. Zu jedem Zeitpunkt sind genau die Wellen bekannt, deren letzter
         Pivot (Welle 5) bereits BESTAETIGT ist.
      2. Auf diese - und nur diese - wird die UNVERAENDERTE Bot-Funktion
         remove_overlapping angewendet.
      3. Was danach uebrig bleibt, frisch genug ist und noch nicht gehandelt
         wurde, wird gehandelt. Einmal gehandelt heisst endgueltig gehandelt:
         eine spaeter auftauchende, besser bewertete Welle kann das nicht
         mehr rueckgaengig machen (in der Live-DB verhindert das die
         UNIQUE(symbol, signal_time)-Bedingung).

    Es wird ausschliesslich an den Balken ausgewertet, an denen mindestens
    eine NEUE Welle bestaetigt wird. Dazwischen aendert sich die Menge der
    bekannten Wellen nicht, remove_overlapping liefert dasselbe Ergebnis, und
    das Frische-Fenster kann nur ablaufen - also nie einen zusaetzlichen
    Trade erzeugen. Das ist exakt aequivalent zu einer Auswertung an jedem
    Balken, nur ohne die leeren Durchlaeufe.

    --------------------------------------------------------------------
    Parameter
    --------------------------------------------------------------------
    zigzag          Ausgabe von zigzag_indicator.calculate_zigzag_with_confirmation
                    (braucht die Spalten confirm_idx und pivot_idx)
    min_fib_score   wie bei find_impulse_waves
    freshness_bars  Balken, die ein Wellenende zurueckliegen darf, bevor der
                    Live-Bot es als "nicht mehr frisch" verwirft
                    (SIGNAL_FRESHNESS_HOURS bzw. ..._DAYS in forward_test.py).
                    None = kein Frische-Fenster.
    direction       "bearish" (Long-only, wie im Bot), "bullish", oder None
                    fuer beide. Die Richtungsfilterung erfolgt NACH
                    remove_overlapping - genauso wie in forward_test.py und
                    im bisherigen Backtest.

    Rueckgabe: dieselben Spalten wie find_impulse_waves, zusaetzlich
      confirm_idx  Balken, an dem die Welle bekannt wurde
      pivot_idx    Balken des Wellenende-Pivots
      entry_idx    Balken, an dem der Trade eroeffnet wird (= der Lauf, bei
                   dem die Welle erstmals durchkam)
    Sortiert nach entry_idx.
    """
    empty = pd.DataFrame(columns=["start_time", "end_time", "direction", "wave0", "wave1",
                                   "wave2", "wave3", "wave4", "wave5", "fib_score",
                                   "confirm_idx", "pivot_idx", "entry_idx"])
    if zigzag is None or len(zigzag) < 6:
        return empty
    if "confirm_idx" not in zigzag.columns:
        raise ValueError("find_causal_waves braucht die Ausgabe von "
                         "calculate_zigzag_with_confirmation (Spalte confirm_idx fehlt)")

    candidates = find_impulse_waves(zigzag[["time", "price", "type"]], min_fib_score=min_fib_score)
    if candidates.empty:
        return empty

    # Bestaetigungs- und Pivot-Index einer WELLE sind die ihres letzten
    # Pivots (Welle 5) - vorher steht das Muster nicht fest.
    pivot_times = pd.to_datetime(zigzag["time"])
    confirm_by_time = dict(zip(pivot_times, zigzag["confirm_idx"]))
    pivot_by_time = dict(zip(pivot_times, zigzag["pivot_idx"]))

    candidates = candidates.copy()
    end_times = pd.to_datetime(candidates["end_time"])
    candidates["confirm_idx"] = end_times.map(confirm_by_time)
    candidates["pivot_idx"] = end_times.map(pivot_by_time)
    candidates = candidates.dropna(subset=["confirm_idx", "pivot_idx"])
    if candidates.empty:
        return empty
    candidates["confirm_idx"] = candidates["confirm_idx"].astype(int)
    candidates["pivot_idx"] = candidates["pivot_idx"].astype(int)

    traded = set()          # Wellenenden, die bereits einen Trade ausgeloest haben
    rows = []
    for run_bar in sorted(candidates["confirm_idx"].unique()):
        known = candidates[candidates["confirm_idx"] <= run_bar]
        kept = remove_overlapping(known)
        if kept.empty:
            continue
        if direction is not None:
            kept = kept[kept["direction"] == direction]

        for _, wave in kept.iterrows():
            end_time = wave["end_time"]
            if end_time in traded:
                continue
            if freshness_bars is not None and run_bar - int(wave["pivot_idx"]) > freshness_bars:
                continue
            traded.add(end_time)
            row = wave.to_dict()
            row["entry_idx"] = int(run_bar)
            rows.append(row)

    if not rows:
        return empty
    return pd.DataFrame(rows).sort_values("entry_idx", kind="stable").reset_index(drop=True)


if __name__ == "__main__":
    zigzag = pd.read_csv(os.path.join(RESULTS_DIR, "AAPL_zigzag.csv"), parse_dates=["time"])

    impulses = find_impulse_waves(zigzag, min_fib_score=0.3)
    print(f"{len(impulses)} gueltige Impuls-Kandidaten vor Bereinigung.\n")

    impulses = remove_overlapping(impulses)
    print(f"{len(impulses)} Kandidaten nach Entfernen von Ueberlappungen.\n")
    if not impulses.empty:
        print(impulses.head(10).to_string(index=False))
        output_path = os.path.join(RESULTS_DIR, "AAPL_impulse_waves.csv")
        impulses.to_csv(output_path, index=False)
        print(f"\nGespeichert als: {output_path}")
    else:
        print("Keine gueltigen Muster gefunden. Versuch min_fib_score zu senken",
              "oder die Zigzag-Schwelle (deviation_pct) anzupassen.")

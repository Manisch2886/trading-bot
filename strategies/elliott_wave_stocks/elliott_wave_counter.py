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

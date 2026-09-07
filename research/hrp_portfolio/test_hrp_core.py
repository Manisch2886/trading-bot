"""
Sanity-Checks fuer hrp_core.py (siehe Aufgabenstellung, Abschnitt "Tests")
- synthetische Testfaelle, KEIN Bezug zu echten Bot-Daten:
1. Perfekt unkorrelierte Assets mit GLEICHER Volatilitaet -> HRP-Gewichte
   liegen nahe der Gleichgewichtung (1/N).
2. Ein Cluster aus zwei STARK korrelierten Assets bekommt gemeinsam
   WENIGER Gewicht als bei naiver 1/N-Gewichtung (Kernaussage von HRP:
   redundante/gekoppelte Positionen werden abgewertet).
3. Randfaelle: 1 Asset, exakt 2 Assets.
4. Fallback-Logik (find_max_reliable_subset / blend_with_fallback): ein
   Bot-Paar unter der Datenbasis-Schwelle wird korrekt ausgeschlossen,
   ausgeschlossene Bots behalten ihr normales 1/N-Gewicht, das Ergebnis
   summiert sich weiterhin exakt auf 1.0.

Reiner Unit-Test des NEUEN Forschungsmoduls - importiert NICHTS aus
strategies/ oder shared/, laeuft vollstaendig isoliert.
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hrp_core import (
    correlation_to_distance, hrp_weights, recursive_bisection,
    find_max_reliable_subset, blend_with_fallback,
)

failures = []


def check(label, cond):
    status = "OK" if cond else "FEHLER"
    print(f"[{status}] {label}")
    if not cond:
        failures.append(label)


np.random.seed(7)
n_periods = 500
dates = pd.date_range("2020-01-01", periods=n_periods, freq="D")

# ---------------------------------------------------------------------------
# Testfall 1: 5 perfekt unkorrelierte Assets, IDENTISCHE Volatilitaet
# ---------------------------------------------------------------------------
uncorrelated = pd.DataFrame(
    {f"asset_{i}": np.random.normal(0, 0.01, n_periods) for i in range(5)},
    index=dates,
)
weights_uncorr = hrp_weights(uncorrelated, linkage_method="single")
check("Summe der HRP-Gewichte ist exakt 1.0 (5 unkorrelierte Assets)",
      abs(weights_uncorr.sum() - 1.0) < 1e-9)
check("SANITY-CHECK (Aufgaben-Vorgabe): bei unkorrelierten Assets gleicher "
      "Volatilitaet liegen alle HRP-Gewichte nahe 1/N=0.20 (max. Abweichung < 0.05)",
      (weights_uncorr - 0.2).abs().max() < 0.05)

# ---------------------------------------------------------------------------
# Testfall 2: 4 Assets - 2 davon STARK korreliert (praktisch identisch),
# 2 unabhaengig. Das korrelierte Cluster sollte GEMEINSAM weniger als die
# naive 1/N=0.5-Haelfte des Kapitals bekommen.
# ---------------------------------------------------------------------------
base_returns = np.random.normal(0, 0.01, n_periods)
correlated_pair = pd.DataFrame({
    "corr_a": base_returns + np.random.normal(0, 0.0005, n_periods),
    "corr_b": base_returns + np.random.normal(0, 0.0005, n_periods),
    "indep_c": np.random.normal(0, 0.01, n_periods),
    "indep_d": np.random.normal(0, 0.01, n_periods),
}, index=dates)

weights_cluster = hrp_weights(correlated_pair, linkage_method="single")
check("Summe der HRP-Gewichte ist exakt 1.0 (Cluster-Testfall)",
      abs(weights_cluster.sum() - 1.0) < 1e-9)
cluster_combined_weight = weights_cluster["corr_a"] + weights_cluster["corr_b"]
check("SANITY-CHECK (Aufgaben-Vorgabe): das stark korrelierte Cluster "
      "(corr_a+corr_b) bekommt GEMEINSAM weniger Gewicht als die naive "
      "1/N-Haelfte (0.5) - HRP werten redundante/gekoppelte Positionen ab",
      cluster_combined_weight < 0.5)
check("Die beiden unabhaengigen Assets (indep_c/d) bekommen dafuer "
      "gemeinsam MEHR als ihre naive 1/N-Haelfte (0.5)",
      (weights_cluster["indep_c"] + weights_cluster["indep_d"]) > 0.5)
check("Innerhalb des korrelierten Clusters bleiben corr_a und corr_b "
      "ungefaehr gleich gewichtet (symmetrischer Aufbau, keine echte "
      "Volatilitaetsdifferenz zwischen den beiden)",
      abs(weights_cluster["corr_a"] - weights_cluster["corr_b"]) < 0.05)

# ---------------------------------------------------------------------------
# Testfall 3: Randfaelle - 1 Asset, exakt 2 Assets
# ---------------------------------------------------------------------------
single = pd.DataFrame({"only_one": np.random.normal(0, 0.01, n_periods)}, index=dates)
weights_single = hrp_weights(single)
check("Ein einzelnes Asset bekommt automatisch Gewicht 1.0, kein Crash",
      weights_single["only_one"] == 1.0)

two_assets = pd.DataFrame({
    "a": np.random.normal(0, 0.01, n_periods),
    "b": np.random.normal(0, 0.02, n_periods),  # doppelte Volatilitaet
}, index=dates)
weights_two = hrp_weights(two_assets)
check("Bei genau 2 Assets summieren sich die Gewichte auf 1.0, kein Crash",
      abs(weights_two.sum() - 1.0) < 1e-9)
check("Bei genau 2 Assets bekommt das volatilere Asset (b, doppelte Vola) "
      "das KLEINERE Gewicht (inverse Varianz-Logik der Bisektion)",
      weights_two["b"] < weights_two["a"])

# ---------------------------------------------------------------------------
# Testfall 4: Fallback-Logik fuer Bot-Paare unter der Datenbasis-Schwelle
# ---------------------------------------------------------------------------
bots = ["bot_a", "bot_b", "bot_c", "bot_d", "bot_e"]
# bot_e hat mit ALLEN anderen zu wenig gemeinsame Handelstage - sollte
# komplett aus dem HRP-Teil-Universum ausgeschlossen werden.
sufficient = pd.DataFrame(True, index=bots, columns=bots)
for b in bots:
    if b != "bot_e":
        sufficient.loc[b, "bot_e"] = False
        sufficient.loc["bot_e", b] = False

reliable_subset = find_max_reliable_subset(sufficient, bots)
check("Groesstes verlaessliches Teil-Universum schliesst bot_e korrekt aus "
      "und enthaelt alle 4 uebrigen Bots",
      sorted(reliable_subset) == ["bot_a", "bot_b", "bot_c", "bot_d"])

hrp_subset_returns = pd.DataFrame(
    {b: np.random.normal(0, 0.01, n_periods) for b in reliable_subset}, index=dates)
hrp_subset_w = hrp_weights(hrp_subset_returns)
blended = blend_with_fallback(hrp_subset_w, bots)

check("Geblendete Gewichte (HRP-Teil-Universum + Fallback) summieren sich "
      "exakt auf 1.0", abs(blended.sum() - 1.0) < 1e-9)
check("Der ausgeschlossene Bot (bot_e) behaelt GENAU sein normales "
      "1/N-Gewicht (0.2 bei 5 Bots), unveraendert durch HRP",
      abs(blended["bot_e"] - 0.2) < 1e-9)
check("Die 4 eingeschlossenen Bots teilen sich gemeinsam GENAU 4/5 des "
      "Kapitals (nicht mehr, nicht weniger)",
      abs(sum(blended[b] for b in reliable_subset) - 0.8) < 1e-9)

# Randfall: gar kein Paar hat ausreichend Datenbasis -> komplette
# Gleichgewichtung als Fallback
no_reliable_pairs = pd.DataFrame(False, index=bots, columns=bots)
for b in bots:
    no_reliable_pairs.loc[b, b] = True
empty_subset = find_max_reliable_subset(no_reliable_pairs, bots)
check("Wenn KEIN Paar ausreichend Datenbasis hat, bleibt das verlaessliche "
      "Teil-Universum bei hoechstens 1 Element (kein einziges echtes Paar "
      "erfuellt die Schwelle - ein Aufrufer behandelt das als 'kein "
      "sinnvolles HRP-Teil-Universum', siehe Dokumentation von "
      "find_max_reliable_subset)", len(empty_subset) <= 1)
fully_blended = blend_with_fallback(pd.Series(dtype=float), bots)
check("Ohne jedes verlaessliche Paar degeneriert das Ergebnis sauber zur "
      "vollstaendigen Gleichgewichtung (je 0.2), kein Crash",
      (abs(fully_blended - 0.2) < 1e-9).all())
if empty_subset:
    single_hrp_w = hrp_weights(pd.DataFrame(
        {empty_subset[0]: np.random.normal(0, 0.01, n_periods)}, index=dates))
    single_blended = blend_with_fallback(single_hrp_w, bots)
    check("Auch ein trivialer Ein-Element-'Cluster' fuehrt beim Blenden zu "
          "GENAU 1/N fuer alle Bots (degeneriert korrekt zur vollen "
          "Gleichgewichtung, kein verzerrtes Ergebnis)",
          (abs(single_blended - 0.2) < 1e-9).all())

# ---------------------------------------------------------------------------
# Testfall 5: correlation_to_distance - Wertebereich und Symmetrie
# ---------------------------------------------------------------------------
sample_corr = uncorrelated.corr()
dist = correlation_to_distance(sample_corr)
check("Distanzmatrix ist symmetrisch", np.allclose(dist.values, dist.values.T))
check("Distanz auf der Diagonale ist exakt 0 (jedes Asset hat Distanz 0 zu sich selbst)",
      np.allclose(np.diag(dist.values), 0.0))
check("Alle Distanzwerte liegen im erwarteten Bereich [0, 1]",
      (dist.values >= -1e-9).all() and (dist.values <= 1 + 1e-9).all())

print()
if failures:
    print(f"{len(failures)} FEHLGESCHLAGENE CHECKS: {failures}")
    sys.exit(1)
else:
    print("ALLE CHECKS OK")

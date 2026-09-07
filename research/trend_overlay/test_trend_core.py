"""
Sanity-Checks fuer trend_core.py (siehe Aufgabenstellung, Abschnitt 4) -
synthetische Testfaelle, KEIN Bezug zu echten Marktdaten:
1. Signal korrekt "an" in einem eindeutigen, synthetisch konstruierten
   Abwaertstrend.
2. Signal korrekt "aus" in einem eindeutigen Aufwaertstrend.
3. Kein Look-Ahead-Bias: eine Aenderung ZUKUENFTIGER Kurse darf
   VERGANGENE MA-/Signal-Werte nicht veraendern.
4. combine_signals_and() - echtes UND, nicht ODER.
5. apply_overlay_to_returns() - manuell nachgerechnete Beispiele fuer
   50%-Reduktion und komplette Pausierung.
6. signal_active_stats() - Episoden-/Haeufigkeits-Zaehlung.

Reiner Unit-Test des NEUEN Forschungsmoduls - importiert NICHTS aus
strategies/ oder shared/, laeuft vollstaendig isoliert.
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trend_core import (
    compute_moving_average, compute_downtrend_signal, combine_signals_and,
    apply_overlay_to_returns, signal_active_stats,
)

failures = []


def check(label, cond):
    status = "OK" if cond else "FEHLER"
    print(f"[{status}] {label}")
    if not cond:
        failures.append(label)


WINDOW = 50
dates = pd.date_range("2020-01-01", periods=300, freq="D")

# ---------------------------------------------------------------------------
# Testfall 1: eindeutiger, monotoner Abwaertstrend
# ---------------------------------------------------------------------------
downtrend_prices = pd.Series(np.linspace(200, 50, 300), index=dates)
downtrend_signal = compute_downtrend_signal(downtrend_prices, WINDOW)
# nach der Anlaufphase (erste WINDOW Tage) muss das Signal durchgehend an sein
check("SANITY-CHECK (Aufgaben-Vorgabe): Signal ist im eindeutigen "
      "Abwaertstrend nach der Anlaufphase durchgehend AN",
      bool(downtrend_signal.iloc[WINDOW:].all()))
check("Vor Ablauf der Anlaufphase (MA noch nicht definiert) ist das Signal "
      "konservativ AUS, nicht undefiniert/True",
      bool((~downtrend_signal.iloc[:WINDOW - 1]).all()))

# ---------------------------------------------------------------------------
# Testfall 2: eindeutiger, monotoner Aufwaertstrend
# ---------------------------------------------------------------------------
uptrend_prices = pd.Series(np.linspace(50, 200, 300), index=dates)
uptrend_signal = compute_downtrend_signal(uptrend_prices, WINDOW)
check("SANITY-CHECK (Aufgaben-Vorgabe): Signal ist im eindeutigen "
      "Aufwaertstrend nach der Anlaufphase durchgehend AUS",
      bool((~uptrend_signal.iloc[WINDOW:]).all()))

# ---------------------------------------------------------------------------
# Testfall 3: kein Look-Ahead-Bias
# ---------------------------------------------------------------------------
np.random.seed(3)
base_prices = pd.Series(100 + np.cumsum(np.random.normal(0, 1, 300)), index=dates)
ma_before = compute_moving_average(base_prices, WINDOW)
signal_before = compute_downtrend_signal(base_prices, WINDOW)

modified_prices = base_prices.copy()
# nur die LETZTEN 30 Tage (weit nach der Anlaufphase) drastisch veraendern
modified_prices.iloc[-30:] = modified_prices.iloc[-30:] * 5.0
ma_after = compute_moving_average(modified_prices, WINDOW)
signal_after = compute_downtrend_signal(modified_prices, WINDOW)

unaffected_slice = slice(0, 200)  # weit vor der geaenderten Zukunft
check("KEIN LOOK-AHEAD-BIAS: eine Aenderung zukuenftiger Kurse (letzte 30 "
      "Tage) veraendert die MA-Werte weit in der Vergangenheit NICHT",
      ma_before.iloc[unaffected_slice].equals(ma_after.iloc[unaffected_slice]))
check("KEIN LOOK-AHEAD-BIAS: dasselbe gilt fuer das abgeleitete Signal",
      signal_before.iloc[unaffected_slice].equals(signal_after.iloc[unaffected_slice]))
check("Die geaenderte Zukunft aendert dagegen (plausibel) die MA-Werte GANZ "
      "am Ende der Serie (Beweis, dass der Test ueberhaupt etwas testet)",
      not ma_before.iloc[-1:].equals(ma_after.iloc[-1:]))

# ---------------------------------------------------------------------------
# Testfall 4: combine_signals_and - echtes UND
# ---------------------------------------------------------------------------
sig_a = pd.Series([True, True, False, False], index=dates[:4])
sig_b = pd.Series([True, False, True, False], index=dates[:4])
combined = combine_signals_and(sig_a, sig_b)
check("combine_signals_and: nur an Tagen TRUE, an denen BEIDE Signale "
      "TRUE sind (echtes UND, kein ODER)",
      combined.tolist() == [True, False, False, False])

# ---------------------------------------------------------------------------
# Testfall 5: apply_overlay_to_returns - manuelle Nachrechnung
# ---------------------------------------------------------------------------
returns = pd.Series([0.02, -0.03, 0.01, 0.05], index=dates[:4])
signal_days = pd.Series([False, True, True, False], index=dates[:4])

half_exposure = apply_overlay_to_returns(returns, signal_days, exposure_during_signal=0.5)
check("50%-Reduktion: Tag 1 (Signal AUS) bleibt unveraendert bei 0.02",
      half_exposure.iloc[0] == 0.02)
check("50%-Reduktion: Tag 2 (Signal AN, -0.03) wird auf -0.015 halbiert",
      abs(half_exposure.iloc[1] - (-0.015)) < 1e-12)
check("50%-Reduktion: Tag 3 (Signal AN, 0.01) wird auf 0.005 halbiert",
      abs(half_exposure.iloc[2] - 0.005) < 1e-12)
check("50%-Reduktion: Tag 4 (Signal AUS) bleibt unveraendert bei 0.05",
      half_exposure.iloc[3] == 0.05)

full_pause = apply_overlay_to_returns(returns, signal_days, exposure_during_signal=0.0)
check("Komplette Pausierung: Tage mit aktivem Signal haben exakt Rendite 0.0",
      full_pause.iloc[1] == 0.0 and full_pause.iloc[2] == 0.0)
check("Komplette Pausierung: Tage OHNE aktives Signal bleiben unveraendert",
      full_pause.iloc[0] == 0.02 and full_pause.iloc[3] == 0.05)

# ---------------------------------------------------------------------------
# Testfall 6: signal_active_stats - Episoden-Zaehlung
# ---------------------------------------------------------------------------
episodic_signal = pd.Series(
    [False, True, True, False, False, True, False, True, True, True],
    index=dates[:10])
stats = signal_active_stats(episodic_signal)
check("signal_active_stats: aktive Tage korrekt gezaehlt (6 von 10)",
      stats["active_days"] == 6)
check("signal_active_stats: 3 zusammenhaengende Episoden korrekt erkannt",
      stats["num_episodes"] == 3)
check("signal_active_stats: laengste Episode korrekt erkannt (3 Tage am Ende)",
      stats["longest_episode_days"] == 3)
check("signal_active_stats: aktiver Anteil korrekt berechnet (60.0%)",
      stats["active_pct"] == 60.0)

print()
if failures:
    print(f"{len(failures)} FEHLGESCHLAGENE CHECKS: {failures}")
    sys.exit(1)
else:
    print("ALLE CHECKS OK")

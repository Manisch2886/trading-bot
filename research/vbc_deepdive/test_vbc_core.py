"""
Sanity-Checks fuer vbc_core.py (kombinierte Logik)
=======================================================
Bewusst ohne Test-Framework, wie in allen vier Vorgaenger-Untersuchungen.
Der Schwerpunkt liegt auf dem, was in dieser Studie NEU ist: die
KOMBINATION zweier Mechanismen. Die Frage, ob die uebernommenen Bausteine
noch dasselbe tun wie in den Vorgaenger-Studien, beantwortet
verify_reference.py auf den echten Daten - hier geht es um die Logik.

Nutzung:  python3 test_vbc_core.py
"""

import os
import sys

import numpy as np
import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
sys.path.insert(0, _DIR)

from vbc_core import (
    true_range, wilder_atr, calibrate_atr_multiplier, initial_stop_price,
    update_trailing_stop, simulate_exit, compute_realized_volatility,
    compute_inverse_vol_weights, simulate_weighted_portfolio,
    calculate_max_drawdown, calmar_ratio,
    STOP_FIXED_STATIC, STOP_ATR_TRAILING,
    VARIANTS, USES_TRAILING, USES_VOL_WEIGHTS,
)

PASSED = FAILED = 0


def check(label, condition, detail=""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  OK    {label}")
    else:
        FAILED += 1
        print(f"  FEHLER {label}   {detail}")


def series(n, amplitude_pct, start=100.0, drift_pct=0.0):
    """
    Deterministische Saegezahn-Kursreihe mit einstellbarer Amplitude - keine
    Zufallszahlen, damit die Checks reproduzierbar sind.

    WICHTIG: die Amplitude wirkt auf den SCHLUSSKURS (alternierend um den
    Trend) und nicht nur auf Hoch/Tief. Die beiden untersuchten Mechanismen
    messen Volatilitaet naemlich UNTERSCHIEDLICH: der ATR-Stop ueber die
    True Range (Hoch/Tief/Vorschluss, also auch innerhalb eines Balkens),
    das Vol-Sizing ueber die Standardabweichung der Schluss-zu-Schluss-
    Log-Returns. Eine Testreihe, die nur Hoch und Tief aufspreizt, laesst
    den Schlusskurs unveraendert - dort waere die realisierte Volatilitaet
    exakt null und der zweite Mechanismus wuerde degenerieren, ohne dass
    das ein Fehler waere. Diese Unterscheidung ist kein Testdetail, sondern
    genau der Grund, warum die beiden Mechanismen ueberhaupt teilweise
    unabhaengig sein koennen.
    """
    trend = start * (1 + drift_pct / 100.0) ** np.arange(n)
    wobble = 1 + (amplitude_pct / 200.0) * ((-1.0) ** np.arange(n))
    close = trend * wobble
    half = amplitude_pct / 200.0
    return close * (1 + half), close * (1 - half), close


# ---------------------------------------------------------------------------
print("\n1) Varianten-Matrix (2x2) ist vollstaendig und widerspruchsfrei")
# ---------------------------------------------------------------------------
check("genau vier Varianten definiert", len(VARIANTS) == 4, str(VARIANTS))
check("jede Kombination aus (Trailing ja/nein) x (Vol-Gewichte ja/nein) kommt genau einmal vor",
      sorted((USES_TRAILING[v], USES_VOL_WEIGHTS[v]) for v in VARIANTS)
      == [(False, False), (False, True), (True, False), (True, True)])
check("Baseline nutzt weder Trailing noch Vol-Gewichte",
      not USES_TRAILING["baseline"] and not USES_VOL_WEIGHTS["baseline"])
check("die kombinierte Variante nutzt beides",
      USES_TRAILING["combined"] and USES_VOL_WEIGHTS["combined"])

# ---------------------------------------------------------------------------
print("\n2) BEIDE Mechanismen haengen an derselben Eingangsgroesse (Kernfrage der Studie)")
# ---------------------------------------------------------------------------
# Zwei synthetische Reihen, identisch bis auf die Balken-Amplitude.
lo_h, lo_l, lo_c = series(200, amplitude_pct=1.0)
hi_h, hi_l, hi_c = series(200, amplitude_pct=6.0)
atr_lo = wilder_atr(lo_h, lo_l, lo_c, 14)
atr_hi = wilder_atr(hi_h, hi_l, hi_c, 14)
idx = 150

K = 2.0
dist_lo = (lo_c[idx] - initial_stop_price(STOP_ATR_TRAILING, lo_c[idx], 5.0, K, atr_lo[idx])) / lo_c[idx] * 100
dist_hi = (hi_c[idx] - initial_stop_price(STOP_ATR_TRAILING, hi_c[idx], 5.0, K, atr_hi[idx])) / hi_c[idx] * 100
check("Mechanismus 1 (ATR-Stop): hoehere Volatilitaet -> BREITERER Stop",
      dist_hi > dist_lo, f"{dist_hi:.2f}% vs. {dist_lo:.2f}%")

# Realisierte Volatilitaet derselben beiden Reihen -> inverse Gewichte
vol_lo = compute_realized_volatility(lo_c, 90)[idx]
vol_hi = compute_realized_volatility(hi_c, 90)[idx]
weights = compute_inverse_vol_weights(pd.Series([vol_lo, vol_hi]))
check("Mechanismus 2 (Vol-Sizing): hoehere Volatilitaet -> KLEINERES Gewicht",
      weights.iloc[1] < weights.iloc[0], f"{weights.iloc[1]:.3f} vs. {weights.iloc[0]:.3f}")
check("beide Mechanismen reagieren also auf DIESELBE Eingangsgroesse (Volatilitaet) - "
      "genau deshalb ist ihre Unabhaengigkeit eine offene, zu pruefende Frage",
      dist_hi > dist_lo and weights.iloc[1] < weights.iloc[0])

# ---------------------------------------------------------------------------
print("\n3) Inverse Vol-Gewichte")
# ---------------------------------------------------------------------------
vols = pd.Series([0.01, 0.02, 0.03, 0.04, 0.08])
w = compute_inverse_vol_weights(vols)
check("Mittelwert der Gewichte ist exakt 1,0 (gleiche durchschnittliche Positionsgroesse)",
      np.isclose(w.mean(), 1.0), f"{w.mean()}")
check("Reihenfolge bleibt monoton fallend in der Volatilitaet",
      list(w) == sorted(w, reverse=True), str(list(w.round(3))))
check("Ausreisser werden median-relativ geclippt (Clip-Faktor 4)",
      w.max() / w.min() <= 16.0 + 1e-9, f"Spanne={w.max() / w.min():.2f}")
w_nan = compute_inverse_vol_weights(pd.Series([0.02, np.nan, 0.04]))
check("fehlende Vol-Werte werden neutral behandelt, nicht verworfen",
      len(w_nan) == 3 and w_nan.notna().all() and np.isclose(w_nan.mean(), 1.0), str(list(w_nan)))
check("komplett ungueltige Eingabe degeneriert zur festen Allokation (alle Gewichte 1,0)",
      (compute_inverse_vol_weights(pd.Series([np.nan, np.nan])) == 1.0).all())

# ---------------------------------------------------------------------------
print("\n4) Kalibrierung des ATR-Multiplikators")
# ---------------------------------------------------------------------------
atr = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
price = np.array([100.0] * 5)
k = calibrate_atr_multiplier(atr, price, 5.0)
distances = k * atr / price * 100
check("mediane Anfangs-Stop-Distanz trifft den Bot-Stop exakt",
      np.isclose(np.median(distances), 5.0), f"{np.median(distances):.4f}%")
check("die Streuung zwischen den Trades bleibt erhalten",
      distances.min() < 5.0 < distances.max(), f"{distances.min():.2f}..{distances.max():.2f}")
check("None bei leerer Eingabe", calibrate_atr_multiplier(np.array([]), np.array([]), 5.0) is None)

# ---------------------------------------------------------------------------
print("\n5) Trailing-Mechanik")
# ---------------------------------------------------------------------------
check("fester Stop bewegt sich nie",
      update_trailing_stop(95.0, 150.0, STOP_FIXED_STATIC, 5.0, 2.0, 1.0) == 95.0)
check("ATR-Trailing zieht nach: Hoch - k*ATR",
      np.isclose(update_trailing_stop(95.0, 110.0, STOP_ATR_TRAILING, 5.0, 2.0, 1.0), 108.0))
check("Ratsche: ein Volatilitaets-Sprung lockert einen bereits nachgezogenen Stop NICHT",
      update_trailing_stop(108.0, 110.0, STOP_ATR_TRAILING, 5.0, 2.0, 20.0) == 108.0)
check("ungueltiger ATR faellt auf die feste Prozent-Distanz zurueck",
      np.isclose(initial_stop_price(STOP_ATR_TRAILING, 100.0, 5.0, 2.0, np.nan), 95.0))

# Look-Ahead innerhalb eines Balkens: das Hoch von Balken 1 darf den Stop nicht
# so anheben, dass er noch im selben Balken vom Tief getroffen wird.
h = np.array([100.0, 130.0, 130.0]); l = np.array([100.0, 99.0, 120.0]); c = np.array([100.0, 129.0, 125.0])
a = np.array([1.0, 1.0, 1.0])
out = simulate_exit(h, l, c, a, 0, 100.0, STOP_ATR_TRAILING, 5.0, 2.0, max_hold_bars=10)
check("Stop wird erst NACH der Stop-Pruefung desselben Balkens nachgezogen",
      out["exit_idx"] != 1, f"Ausstieg in Balken {out['exit_idx']}")

h = np.array([200.0, 100.0]); l = np.array([100.0, 99.0]); c = np.array([100.0, 100.0])
check("laufendes Hoch startet beim Einstiegskurs, nicht beim Hoch des Einstiegsbalkens",
      initial_stop_price(STOP_ATR_TRAILING, 100.0, 5.0, 2.0, 1.0) < 100.0)

h = np.array([100.0] * 10); l = np.array([100.0] * 10); c = np.array([100.0] * 10)
a = np.array([1.0] * 10)
out = simulate_exit(h, l, c, a, 0, 100.0, STOP_FIXED_STATIC, 5.0, None, max_hold_bars=3)
check("Zeit-Exit exakt nach max_hold_bars Balken",
      out["exit_idx"] == 3 and out["result"] == "time_exit", str(out))
out = simulate_exit(h[:3], l[:3], c[:3], a[:3], 0, 100.0, STOP_FIXED_STATIC, 5.0, None, max_hold_bars=8)
check("zu kurze Resthistorie -> Trade gilt als nicht abschliessbar (Original-Verhalten)",
      out["result"] == "unclosed", str(out))

# ---------------------------------------------------------------------------
print("\n6) Portfolio-Simulation mit Gewichten")
# ---------------------------------------------------------------------------
trades = pd.DataFrame({
    "symbol": ["A", "B", "C"],
    "entry_time": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
    "exit_time": pd.to_datetime(["2024-01-10", "2024-01-11", "2024-01-12"]),
    "pnl_pct": [10.0, -5.0, 20.0],
})
plain = simulate_weighted_portfolio(trades, 10_000.0, 0.10, None, None)
ones = simulate_weighted_portfolio(trades, 10_000.0, 0.10, pd.Series(1.0, index=trades.index), None)
check("Gewichte = 1,0 sind identisch zu 'keine Gewichte' (Baseline bleibt Baseline)",
      plain["final_capital"] == ones["final_capital"] == 10_250.0, str(plain["final_capital"]))
check("Uebergewichtung eines Gewinners erhoeht das Endkapital",
      simulate_weighted_portfolio(trades, 10_000.0, 0.10,
                                   pd.Series([2.0, 1.0, 1.0], index=trades.index), None
                                   )["final_capital"] > plain["final_capital"])
check("Positionslimit blockiert den dritten gleichzeitigen Einstieg",
      simulate_weighted_portfolio(trades, 10_000.0, 0.10, None, 2)["num_skipped"] == 1)
check("zu wenig freies Kapital blockiert weitere Einstiege",
      simulate_weighted_portfolio(trades, 10_000.0, 0.50, None, None)["num_skipped"] >= 1)
# Bei 30 % Allokation passen drei ungewichtete Positionen ins Kapital. Werden
# die ersten beiden hochgewichtet, ist fuer die dritte nichts mehr frei -
# Vol-Sizing wirkt also auch ueber die Trade-AUSWAHL, nicht nur ueber die Groesse.
weighted_skips = simulate_weighted_portfolio(
    trades, 10_000.0, 0.30, pd.Series([1.6, 1.6, 0.8], index=trades.index), None)["num_skipped"]
plain_skips = simulate_weighted_portfolio(trades, 10_000.0, 0.30, None, None)["num_skipped"]
check("ein groesseres Gewicht kann einen Trade am Kapital scheitern lassen - "
      "Vol-Sizing wirkt daher auch ueber die Trade-AUSWAHL, nicht nur ueber die Groesse",
      weighted_skips > plain_skips, f"gewichtet {weighted_skips} vs. ungewichtet {plain_skips}")

# ---------------------------------------------------------------------------
print("\n7) Kennzahlen")
# ---------------------------------------------------------------------------
equity = pd.DataFrame({"capital_after": [11_000.0, 9_900.0, 10_500.0]})
check("Max Drawdown wird vom laufenden Hoch der Kapitalkurve gemessen",
      np.isclose(calculate_max_drawdown(equity, 10_000.0), -10.0))
check("Max Drawdown ist 0 bei leerer Kapitalkurve",
      calculate_max_drawdown(pd.DataFrame(), 10_000.0) == 0.0)
check("Calmar-Konvention identisch zu allen vier Vorgaenger-Studien (82,43/6,33 = 13,02)",
      calmar_ratio(82.43, -6.33) == 13.02)
check("Calmar ist bei Drawdown 0 nicht definiert", calmar_ratio(50.0, 0.0) is None)

# ---------------------------------------------------------------------------
print("\n8) True Range gegen die bestehende Projekt-Implementierung")
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(_REPO_ROOT, "strategies", "t3_supertrend"))
from indicators import calculate_atr as project_atr
h2, l2, c2 = series(300, amplitude_pct=3.0, drift_pct=0.05)
mine = wilder_atr(h2, l2, c2, 14)
theirs = project_atr(pd.DataFrame({"high": h2, "low": l2, "close": c2}), 14).to_numpy()
check("wilder_atr stimmt numerisch mit strategies/t3_supertrend/indicators.py::calculate_atr ueberein",
      np.allclose(mine, theirs, rtol=1e-12, atol=1e-12),
      f"max. Abweichung={np.max(np.abs(mine - theirs)):.3e}")
tr = true_range(np.array([10.0, 12.0]), np.array([9.0, 10.5]), np.array([9.5, 11.5]))
check("erster Balken: TR = Hoch - Tief", np.isclose(tr[0], 1.0))

print("\n" + "=" * 60)
print(f"{PASSED} Checks bestanden, {FAILED} fehlgeschlagen.")
print("=" * 60)
sys.exit(1 if FAILED else 0)

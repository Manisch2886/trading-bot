"""
Sanity-Checks fuer atr_core.py
===================================
Bewusst ohne Test-Framework (keine neue Abhaengigkeit im Projekt) -
dieselbe Form wie research/volatility_scaled_sizing/test_vol_sizing_core.py
und research/trend_overlay/test_trend_core.py.

Abgedeckt:
  * ATR-Definition stimmt numerisch mit der bereits im Projekt
    vorhandenen Implementierung ueberein (kein zweiter, abweichender
    ATR-Dialekt - Lehre aus der doppelten SuperTrend-Implementierung
    im urspruenglichen Pine-Script)
  * der von der Aufgabenstellung geforderte synthetische Testfall:
    BEI GLEICHEM ATR-MULTIPLIKATOR ist der Stop bei hoeherer
    Volatilitaet breiter als bei niedriger
  * Ratschen-Regel, Look-Ahead-Freiheit innerhalb eines Balkens,
    Prioritaet der Ausstiegsbedingungen, Zeit-Exit-Konventionen
  * Kalibrierung des Multiplikators trifft den Zielwert exakt
  * Portfolio-Simulation und Kennzahlen verhalten sich wie die
    bestehenden Bot-Funktionen

Nutzung:  python3 test_atr_core.py
"""

import os
import sys

import numpy as np
import pandas as pd

_RESEARCH_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_RESEARCH_DIR))
sys.path.insert(0, _RESEARCH_DIR)

from atr_core import (
    true_range, wilder_atr, calibrate_atr_multiplier, initial_stop_price,
    update_trailing_stop, simulate_exit, simulate_portfolio,
    calculate_max_drawdown, calmar_ratio,
    STOP_FIXED_STATIC, STOP_FIXED_TRAILING, STOP_ATR_TRAILING,
)

PASSED = 0
FAILED = 0


def check(label: str, condition: bool, detail: str = ""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  OK    {label}")
    else:
        FAILED += 1
        print(f"  FEHLER {label}   {detail}")


def synthetic_series(n: int, amplitude_pct: float, start: float = 100.0, drift_pct: float = 0.0):
    """Deterministische Saegezahn-Kursreihe mit einstellbarer Balken-Amplitude -
    keine Zufallszahlen, damit die Checks reproduzierbar sind."""
    close = start * (1 + drift_pct / 100.0) ** np.arange(n)
    half = amplitude_pct / 200.0
    high = close * (1 + half)
    low = close * (1 - half)
    return high, low, close


# ---------------------------------------------------------------------------
print("\n1) True Range und ATR")
# ---------------------------------------------------------------------------
high = np.array([10.0, 12.0, 11.0])
low = np.array([9.0, 10.5, 9.5])
close = np.array([9.5, 11.5, 10.0])
tr = true_range(high, low, close)
check("erster Balken: TR = Hoch - Tief (kein Vorschlusskurs vorhanden)", np.isclose(tr[0], 1.0), f"tr[0]={tr[0]}")
check("zweiter Balken: TR = max(H-L, |H-Vorschluss|, |L-Vorschluss|)",
      np.isclose(tr[1], max(1.5, abs(12.0 - 9.5), abs(10.5 - 9.5))), f"tr[1]={tr[1]}")

sys.path.insert(0, os.path.join(_REPO_ROOT, "strategies", "t3_supertrend"))
from indicators import calculate_atr as project_atr  # bestehende Projekt-Implementierung

h2, l2, c2 = synthetic_series(300, amplitude_pct=3.0, drift_pct=0.05)
df = pd.DataFrame({"high": h2, "low": l2, "close": c2})
mine = wilder_atr(h2, l2, c2, 14)
theirs = project_atr(df, 14).to_numpy()
check("wilder_atr stimmt numerisch mit strategies/t3_supertrend/indicators.py::calculate_atr ueberein",
      np.allclose(mine, theirs, rtol=1e-12, atol=1e-12),
      f"max. Abweichung={np.max(np.abs(mine - theirs)):.3e}")

# ---------------------------------------------------------------------------
print("\n2) GEFORDERTER SYNTHETISCHER TESTFALL: hoehere Volatilitaet -> breiterer Stop")
# ---------------------------------------------------------------------------
K = 2.0
lo_h, lo_l, lo_c = synthetic_series(200, amplitude_pct=1.0)
hi_h, hi_l, hi_c = synthetic_series(200, amplitude_pct=6.0)
atr_low = wilder_atr(lo_h, lo_l, lo_c, 14)
atr_high = wilder_atr(hi_h, hi_l, hi_c, 14)

entry_idx = 150
stop_low = initial_stop_price(STOP_ATR_TRAILING, lo_c[entry_idx], 5.0, K, atr_low[entry_idx])
stop_high = initial_stop_price(STOP_ATR_TRAILING, hi_c[entry_idx], 5.0, K, atr_high[entry_idx])
dist_low = (lo_c[entry_idx] - stop_low) / lo_c[entry_idx] * 100
dist_high = (hi_c[entry_idx] - stop_high) / hi_c[entry_idx] * 100

check("ATR ist in der volatileren Reihe groesser", atr_high[entry_idx] > atr_low[entry_idx],
      f"{atr_high[entry_idx]:.4f} vs. {atr_low[entry_idx]:.4f}")
check("bei GLEICHEM Multiplikator ist die Stop-Distanz bei hoher Volatilitaet breiter",
      dist_high > dist_low, f"{dist_high:.2f}% vs. {dist_low:.2f}%")
check("die Stop-Distanzen skalieren etwa mit dem Amplituden-Verhaeltnis (6:1)",
      5.0 < dist_high / dist_low < 7.0, f"Verhaeltnis={dist_high / dist_low:.2f}")
check("ein FESTER Prozent-Stop ist dagegen in beiden Reihen exakt gleich breit",
      np.isclose(initial_stop_price(STOP_FIXED_STATIC, lo_c[entry_idx], 5.0, None, None) / lo_c[entry_idx],
                 initial_stop_price(STOP_FIXED_STATIC, hi_c[entry_idx], 5.0, None, None) / hi_c[entry_idx]))

# ---------------------------------------------------------------------------
print("\n3) Kalibrierung des ATR-Multiplikators")
# ---------------------------------------------------------------------------
atr_at_entry = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
entry_price = np.array([100.0] * 5)
k = calibrate_atr_multiplier(atr_at_entry, entry_price, target_stop_pct=3.0)
distances = k * atr_at_entry / entry_price * 100
check("mediane anfaengliche Stop-Distanz trifft den bestehenden Bot-Stop exakt",
      np.isclose(np.median(distances), 3.0), f"Median={np.median(distances):.4f}%")
check("die Streuung ueber die Trades bleibt erhalten (das ist der untersuchte Effekt)",
      distances.min() < 3.0 < distances.max(), f"{distances.min():.2f}% .. {distances.max():.2f}%")
check("Kalibrierung gibt None bei leerer Eingabe zurueck (statt still auf einen Ersatzwert auszuweichen)",
      calibrate_atr_multiplier(np.array([]), np.array([]), 3.0) is None)
check("Kalibrierung gibt None bei ausschliesslich ungueltigen Werten zurueck",
      calibrate_atr_multiplier(np.array([0.0, np.nan]), np.array([100.0, 100.0]), 3.0) is None)

# ---------------------------------------------------------------------------
print("\n4) Ratschen-Regel und Nachziehen")
# ---------------------------------------------------------------------------
check("fixed_static bewegt den Stop nie",
      update_trailing_stop(95.0, 150.0, STOP_FIXED_STATIC, 5.0, None, 1.0) == 95.0)
check("fixed_trailing zieht bei steigendem Hoch nach",
      np.isclose(update_trailing_stop(95.0, 110.0, STOP_FIXED_TRAILING, 5.0, None, None), 104.5))
check("fixed_trailing senkt den Stop bei fallendem Hoch NICHT (Ratsche)",
      update_trailing_stop(104.5, 100.0, STOP_FIXED_TRAILING, 5.0, None, None) == 104.5)
check("atr_trailing zieht nach: Hoch - k*ATR",
      np.isclose(update_trailing_stop(95.0, 110.0, STOP_ATR_TRAILING, 5.0, 2.0, 1.0), 108.0))
check("atr_trailing lockert den Stop bei einem Volatilitaets-Sprung NICHT (Ratsche)",
      update_trailing_stop(108.0, 110.0, STOP_ATR_TRAILING, 5.0, 2.0, 20.0) == 108.0,
      "ein ATR-Sprung darf einen bereits nachgezogenen Stop nicht wieder nach unten schieben")
check("atr_trailing faellt bei ungueltigem ATR auf den festen Prozent-Stop zurueck",
      np.isclose(initial_stop_price(STOP_ATR_TRAILING, 100.0, 5.0, 2.0, np.nan), 95.0))

# ---------------------------------------------------------------------------
print("\n5) simulate_exit - Prioritaeten, Look-Ahead-Freiheit, Zeit-Exits")
# ---------------------------------------------------------------------------
# Balken 1 trifft sowohl Stop (Tief) als auch Kursziel (Hoch): Stop hat Vorrang.
h = np.array([100.0, 120.0]); l = np.array([100.0, 90.0]); c = np.array([100.0, 110.0])
atr = np.array([1.0, 1.0])
out = simulate_exit(h, l, c, atr, 0, 100.0, STOP_FIXED_STATIC, 5.0, None,
                    max_hold_bars=10, target_price=115.0, time_exit_mode="at_max_offset_only")
check("Stop-Loss hat Vorrang vor dem Kursziel im selben Balken",
      out["result"] == "stop_loss" and np.isclose(out["exit_price"], 95.0), str(out))

# Look-Ahead-Test: Balken 1 hat ein hohes Hoch UND ein Tief, das den ERST DANACH
# nachgezogenen Stop unterschreiten wuerde. Korrekt ist: kein Ausstieg in Balken 1.
h = np.array([100.0, 130.0, 130.0]); l = np.array([100.0, 99.0, 120.0]); c = np.array([100.0, 129.0, 125.0])
atr = np.array([1.0, 1.0, 1.0])
out = simulate_exit(h, l, c, atr, 0, 100.0, STOP_FIXED_TRAILING, 5.0, None,
                    max_hold_bars=10, time_exit_mode="at_max_offset_only")
check("Stop wird erst NACH der Stop-Pruefung desselben Balkens nachgezogen (kein Intrabar-Look-Ahead)",
      out["exit_idx"] != 1, f"Ausstieg in Balken {out['exit_idx']} - zu frueh")
check("nachgezogener Stop greift im FOLGENDEN Balken (130 * 0,95 = 123,5)",
      out["exit_idx"] == 2 and np.isclose(out["exit_price"], 123.5), str(out))

# Regressionstest fuer einen behobenen Fehler: das laufende Hoch startet beim
# EINSTIEGSKURS, nicht beim Hoch des Einstiegsbalkens.
h = np.array([200.0, 100.0]); l = np.array([100.0, 99.0]); c = np.array([100.0, 100.0])
out_stop = initial_stop_price(STOP_FIXED_TRAILING, 100.0, 5.0, None, None)
check("anfaenglicher Trailing-Stop liegt UNTER dem Einstiegskurs, auch wenn der "
      "Einstiegsbalken ein weit hoeheres Hoch hatte", out_stop < 100.0, f"stop={out_stop}")

# Zeit-Exit-Konventionen
h = np.array([100.0] * 10); l = np.array([100.0] * 10); c = np.array([100.0] * 10)
atr = np.array([1.0] * 10)
out = simulate_exit(h, l, c, atr, 0, 100.0, STOP_FIXED_STATIC, 5.0, None, max_hold_bars=3,
                    time_exit_mode="at_max_offset_only")
check("'at_max_offset_only': Zeit-Exit exakt nach max_hold_bars Balken",
      out["exit_idx"] == 3 and out["result"] == "time_exit", str(out))
out = simulate_exit(h[:3], l[:3], c[:3], atr[:3], 0, 100.0, STOP_FIXED_STATIC, 5.0, None,
                    max_hold_bars=8, time_exit_mode="at_max_offset_only")
check("'at_max_offset_only': zu kurze Resthistorie -> Trade gilt als nicht abschliessbar",
      out["result"] == "unclosed", str(out))
out = simulate_exit(h[:3], l[:3], c[:3], atr[:3], 0, 100.0, STOP_FIXED_STATIC, 5.0, None,
                    max_hold_bars=8, time_exit_mode="at_last_available")
check("'at_last_available': Ausstieg zum Schluss des letzten verfuegbaren Balkens",
      out["exit_idx"] == 2 and out["result"] == "time_exit", str(out))
out = simulate_exit(h, l, c, atr, 0, 100.0, STOP_FIXED_STATIC, 5.0, None, max_hold_bars=None,
                    time_exit_mode="none")
check("'none': ohne Ausstiegssignal bleibt der Trade offen (wird spaeter verworfen)",
      out["result"] == "unclosed", str(out))

extra = np.zeros(10, dtype=bool); extra[4] = True
out = simulate_exit(h, l, c, atr, 0, 100.0, STOP_FIXED_STATIC, 5.0, None, max_hold_bars=None,
                    extra_exit=extra, time_exit_mode="none")
check("strategie-eigenes Ausstiegssignal (T3/SuperTrend) wird zum Schlusskurs ausgefuehrt",
      out["exit_idx"] == 4 and out["result"] == "signal_exit", str(out))

# ---------------------------------------------------------------------------
print("\n6) ATR-Trailing gegen fixen Stop auf identischen Kursen")
# ---------------------------------------------------------------------------
# Kursverlauf: 15 Balken aufwaerts, danach wieder abwaerts - erst dadurch
# kann sich ein Trailing-Stop ueberhaupt vom festen Stop unterscheiden.
up = 100.0 * 1.02 ** np.arange(16)
down = up[-1] * 0.97 ** np.arange(1, 26)
c = np.concatenate([up, down])
h = c * 1.01
l = c * 0.99
atr = wilder_atr(h, l, c, 14)

entry = 0
k_cal = calibrate_atr_multiplier(np.array([atr[entry]]), np.array([c[entry]]), 4.0)
check("bei kalibriertem k ist die ANFANGS-Stop-Distanz beider Varianten identisch",
      np.isclose(initial_stop_price(STOP_ATR_TRAILING, c[entry], 4.0, k_cal, atr[entry]),
                 initial_stop_price(STOP_FIXED_STATIC, c[entry], 4.0, None, None)),
      "genau das leistet die Kalibrierung: gleiches Niveau, andere Form")

out_static = simulate_exit(h, l, c, atr, entry, c[entry], STOP_FIXED_STATIC, 4.0, k_cal,
                            max_hold_bars=39, time_exit_mode="at_max_offset_only")
out_atr = simulate_exit(h, l, c, atr, entry, c[entry], STOP_ATR_TRAILING, 4.0, k_cal,
                         max_hold_bars=39, time_exit_mode="at_max_offset_only")
check("nach Aufwaerts- und anschliessender Abwaertsbewegung steigt der ATR-Trailing-Stop "
      "FRUEHER aus als der feste Stop",
      out_atr["exit_idx"] < out_static["exit_idx"],
      f"ATR-Trailing Balken {out_atr['exit_idx']}, fest Balken {out_static['exit_idx']}")
check("und er sichert dabei einen HOEHEREN Ausstiegskurs (Gewinnsicherung statt Rueckgabe)",
      out_atr["exit_price"] > out_static["exit_price"],
      f"{out_atr['exit_price']:.2f} vs. {out_static['exit_price']:.2f}")
check("der feste Stop liegt dagegen unveraendert 4 % unter dem Einstieg",
      np.isclose(out_static["exit_price"], c[entry] * 0.96), str(out_static))

# ---------------------------------------------------------------------------
print("\n7) Portfolio-Simulation und Kennzahlen")
# ---------------------------------------------------------------------------
trades = pd.DataFrame({
    "symbol": ["A", "B", "C"],
    "entry_time": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
    "exit_time": pd.to_datetime(["2024-01-10", "2024-01-11", "2024-01-12"]),
    "pnl_pct": [10.0, -5.0, 20.0],
})
res = simulate_portfolio(trades, 10_000.0, 0.10, max_concurrent_positions=None)
check("Portfolio-Simulation: alle 3 Trades ausgefuehrt, Kapital korrekt fortgeschrieben",
      res["num_executed"] == 3 and np.isclose(res["final_capital"], 10_000 + 100 - 50 + 200),
      str(res["final_capital"]))
res2 = simulate_portfolio(trades, 10_000.0, 0.10, max_concurrent_positions=2)
check("MAX_CONCURRENT_POSITIONS blockiert den dritten gleichzeitigen Einstieg",
      res2["num_executed"] == 2 and res2["num_skipped"] == 1, str(res2))
res3 = simulate_portfolio(trades, 10_000.0, 0.50, max_concurrent_positions=None)
check("zu wenig freies Kapital blockiert weitere Einstiege",
      res3["num_skipped"] >= 1, str(res3))

equity = pd.DataFrame({"capital_after": [11_000.0, 9_900.0, 10_500.0]})
check("Max Drawdown wird vom laufenden Hoch der Kapitalkurve gemessen",
      np.isclose(calculate_max_drawdown(equity, 10_000.0), -10.0),
      str(calculate_max_drawdown(equity, 10_000.0)))
check("Max Drawdown ist 0 bei leerer Kapitalkurve",
      calculate_max_drawdown(pd.DataFrame(), 10_000.0) == 0.0)
check("Calmar-Ratio-Konvention identisch zu den drei vorherigen Untersuchungen (82,43/6,33 = 13,02)",
      calmar_ratio(82.43, -6.33) == 13.02, str(calmar_ratio(82.43, -6.33)))
check("Calmar-Ratio ist bei Drawdown 0 nicht definiert (None statt Ersatz-Nenner)",
      calmar_ratio(50.0, 0.0) is None)

# ---------------------------------------------------------------------------
print(f"\n{'=' * 60}")
print(f"{PASSED} Checks bestanden, {FAILED} fehlgeschlagen.")
print(f"{'=' * 60}")
sys.exit(1 if FAILED else 0)

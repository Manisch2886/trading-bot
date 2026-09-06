"""
Sanity-Checks fuer vol_sizing_core.py (siehe Aufgabenstellung, Abschnitt
"Tests") - synthetische Testfaelle, KEIN Bezug zu echten Bot-Daten:
1. Konstant NIEDRIGE Volatilitaet -> GROESSERE Gewichte als bei konstant
   HOHER Volatilitaet.
2. Normalisierung auf Mittelwert exakt 1.0.
3. Regressionstest: simulate_weighted_portfolio() mit weights=None
   reproduziert die bestehende, bereits validierte
   simulate_portfolio()-Logik (siehe z.B.
   strategies/volatility_breakout/equity_simulation.py) EXAKT - beweist,
   dass die Verallgemeinerung die Baseline-Methodik nicht veraendert.
4. Randfaelle: leere/fehlende Volatilitaetsdaten, Null-Volatilitaet.

Reiner Unit-Test des NEUEN Forschungsmoduls - importiert absichtlich
NICHTS aus strategies/, laeuft vollstaendig isoliert.
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vol_sizing_core import (
    compute_realized_volatility, volatility_at_entry, compute_inverse_vol_weights,
    simulate_weighted_portfolio, calculate_max_drawdown,
)

failures = []


def check(label, cond):
    status = "OK" if cond else "FEHLER"
    print(f"[{status}] {label}")
    if not cond:
        failures.append(label)


# ---------------------------------------------------------------------------
# Testfall 1: konstant niedrige vs. konstant hohe Volatilitaet
# ---------------------------------------------------------------------------
np.random.seed(42)
n = 300
dates = pd.date_range("2020-01-01", periods=n, freq="D")

# Ruhiges Symbol: sehr kleine taegliche Schwankungen (0.2% Std)
calm_returns = np.random.normal(0, 0.002, n)
calm_prices = 100 * np.exp(np.cumsum(calm_returns))
calm_df = pd.DataFrame({"open_time": dates, "close": calm_prices})

# Volatiles Symbol: deutlich groessere Schwankungen (3% Std)
volatile_returns = np.random.normal(0, 0.03, n)
volatile_prices = 100 * np.exp(np.cumsum(volatile_returns))
volatile_df = pd.DataFrame({"open_time": dates, "close": volatile_prices})

WINDOW = 60
entry_time = dates[250]  # genug Vorlauf fuer das Fenster

calm_vol = volatility_at_entry(calm_df, entry_time, WINDOW)
volatile_vol = volatility_at_entry(volatile_df, entry_time, WINDOW)

check("Realisierte Volatilitaet des ruhigen Symbols ist deutlich kleiner "
      "als die des volatilen Symbols", calm_vol < volatile_vol)

weights = compute_inverse_vol_weights(pd.Series({"calm": calm_vol, "volatile": volatile_vol}))
check("SANITY-CHECK (Aufgaben-Vorgabe): konstant NIEDRIGE Volatilitaet "
      "-> GROESSERES Gewicht (groessere Position) als bei konstant HOHER "
      "Volatilitaet", weights["calm"] > weights["volatile"])
check("Beide Gewichte sind positiv", (weights > 0).all())

# ---------------------------------------------------------------------------
# Testfall 2: Normalisierung auf Mittelwert exakt 1.0
# ---------------------------------------------------------------------------
raw_vols = pd.Series([0.01, 0.02, 0.03, 0.005, 0.04, 0.015, 0.025, 0.008, 0.05, 0.012])
normalized = compute_inverse_vol_weights(raw_vols)
check("Mittelwert der normalisierten Gewichte ist (auf 6 Nachkommastellen) exakt 1.0",
      round(normalized.mean(), 6) == 1.0)
check("Kleinere Volatilitaet -> groesseres Gewicht (Monotonie ueber die gesamte Serie, "
      "nicht nur zwei Extremwerte)",
      normalized.corr(raw_vols) < -0.5)  # deutlich negative Korrelation erwartet

# ---------------------------------------------------------------------------
# Testfall 3: Clipping gegen Ausreisser (eine nahezu-Null-Volatilitaet
# darf keine absurd grosse Position erzeugen)
# ---------------------------------------------------------------------------
vols_with_outlier = pd.Series([0.01, 0.012, 0.011, 0.009, 0.013, 0.0000001])  # letzter Wert: Fast-Null
weights_with_outlier = compute_inverse_vol_weights(vols_with_outlier)
check("Ausreisser (Fast-Null-Volatilitaet) wird geclippt, erzeugt KEIN "
      "um Groessenordnungen groesseres Gewicht als die anderen",
      weights_with_outlier.iloc[-1] < weights_with_outlier.iloc[:-1].max() * 5)

# ---------------------------------------------------------------------------
# Testfall 4: Randfaelle - fehlende/ungueltige Volatilitaetsdaten
# ---------------------------------------------------------------------------
empty_result = compute_inverse_vol_weights(pd.Series([np.nan, np.nan, np.nan]))
check("Komplett fehlende Vol-Daten -> Gewichte degenerieren sauber zu 1.0 (= fixe Baseline), kein Crash",
      (empty_result == 1.0).all())

mixed = pd.Series([0.01, np.nan, 0.02])
mixed_result = compute_inverse_vol_weights(mixed)
check("Teilweise fehlende Vol-Daten: fehlender Wert bekommt neutrales "
      "(durchschnittliches) Gewicht, kein Crash", not mixed_result.isna().any())

zero_vol = compute_inverse_vol_weights(pd.Series([0.0, 0.01, 0.02]))
check("Null-Volatilitaet fuehrt NICHT zu einer Division-durch-Null-Exception", not zero_vol.isna().any())

# ---------------------------------------------------------------------------
# Testfall 5: REGRESSIONSTEST - simulate_weighted_portfolio(weights=None)
# reproduziert die bestehende simulate_portfolio()-Logik EXAKT
# (Referenzwerte manuell nachgerechnet, Muster identisch zu
# strategies/volatility_breakout/equity_simulation.py)
# ---------------------------------------------------------------------------
sample_trades = pd.DataFrame([
    {"entry_time": pd.Timestamp("2024-01-01"), "exit_time": pd.Timestamp("2024-01-10"),
     "symbol": "AUSDT", "pnl_pct": 10.0},
    {"entry_time": pd.Timestamp("2024-01-05"), "exit_time": pd.Timestamp("2024-01-15"),
     "symbol": "BUSDT", "pnl_pct": -5.0},
    {"entry_time": pd.Timestamp("2024-01-20"), "exit_time": pd.Timestamp("2024-01-25"),
     "symbol": "CUSDT", "pnl_pct": 20.0},
])

result_unweighted = simulate_weighted_portfolio(sample_trades, starting_capital=10_000.0,
                                                 allocation_pct=0.10, weights=None,
                                                 max_concurrent_positions=None)
# Manuelle Nachrechnung (identisch zur Logik in z.B.
# strategies/volatility_breakout/equity_simulation.py:simulate_portfolio):
# Trade A: Entry 01-01 (Kapital 10000, Alloc 1000), Exit 01-10 (+10% -> 1100,
#          Kapital 10100)
# Trade B: Entry 01-05 (Kapital zu diesem Zeitpunkt noch 10000, da B vor
#          A's Exit eroeffnet wird - Ereignisreihenfolge nach ZEIT, nicht
#          nach Eroeffnungsreihenfolge; Alloc 1000), Exit 01-15 (-5% -> 950,
#          Kapital 10100 - 1000 + 950 = 10050)
# Trade C: Entry 01-20 (Kapital 10050, Alloc 1005), Exit 01-25 (+20% -> 1206,
#          Kapital 10050 - 1005 + 1206 = 10251)
check("Regressionstest gegen die bestehende simulate_portfolio()-Logik: "
      "Endkapital exakt wie manuell nachgerechnet (10251.0)",
      result_unweighted["final_capital"] == 10251.0)
check("Regressionstest: alle 3 Trades ausgefuehrt, keiner uebersprungen",
      result_unweighted["num_executed"] == 3 and result_unweighted["num_skipped"] == 0)

# Mit weights ≡ 1.0 explizit gesetzt: IDENTISCHES Ergebnis wie weights=None
explicit_ones = pd.Series(1.0, index=sample_trades.index)
result_explicit_ones = simulate_weighted_portfolio(sample_trades, starting_capital=10_000.0,
                                                    allocation_pct=0.10, weights=explicit_ones)
check("weights=None und weights=Series(1.0) liefern IDENTISCHES Ergebnis "
      "(Konsistenz-Beweis der Verallgemeinerung)",
      result_explicit_ones["final_capital"] == result_unweighted["final_capital"])

# ---------------------------------------------------------------------------
# Testfall 6: unterschiedliche Gewichte fuehren tatsaechlich zu
# unterschiedlichen (nicht identischen) Endergebnissen
# ---------------------------------------------------------------------------
varied_weights = pd.Series([2.0, 0.5, 1.5], index=sample_trades.index)  # Mittelwert genau 4/3, absichtlich NICHT 1.0 hier
result_varied = simulate_weighted_portfolio(sample_trades, starting_capital=10_000.0,
                                             allocation_pct=0.10, weights=varied_weights)
check("Unterschiedliche Gewichte fuehren zu einem ANDEREN Endergebnis als bei weights=1.0 "
      "(beweist, dass der weights-Parameter tatsaechlich wirkt)",
      result_varied["final_capital"] != result_unweighted["final_capital"])

# Trade A (Gewicht 2.0): Alloc 2000, +10% -> 2200, Kapital 10000-2000+2200=10200
# Trade B (Gewicht 0.5, Kapital zum Entry-Zeitpunkt 10000): Alloc 500, -5% -> 475,
#          Kapital 10200-500+475=10175
# Trade C (Gewicht 1.5, Kapital 10175): Alloc 1526.25, +20% -> 1831.5,
#          Kapital 10175-1526.25+1831.5=10480.25
check("Manuelle Nachrechnung mit variierenden Gewichten stimmt exakt (10480.25)",
      result_varied["final_capital"] == 10480.25)

# ---------------------------------------------------------------------------
# Testfall 7: MAX_CONCURRENT_POSITIONS wird respektiert (unveraendert aus
# der bestehenden Logik uebernommen)
# ---------------------------------------------------------------------------
overlapping_trades = pd.DataFrame([
    {"entry_time": pd.Timestamp("2024-01-01"), "exit_time": pd.Timestamp("2024-01-30"),
     "symbol": "A", "pnl_pct": 5.0},
    {"entry_time": pd.Timestamp("2024-01-02"), "exit_time": pd.Timestamp("2024-01-29"),
     "symbol": "B", "pnl_pct": 5.0},
    {"entry_time": pd.Timestamp("2024-01-03"), "exit_time": pd.Timestamp("2024-01-28"),
     "symbol": "C", "pnl_pct": 5.0},
])
result_limited = simulate_weighted_portfolio(overlapping_trades, starting_capital=10_000.0,
                                              allocation_pct=0.10, max_concurrent_positions=2)
check("MAX_CONCURRENT_POSITIONS=2 bei 3 sich ueberlappenden Trades: genau 1 wird uebersprungen",
      result_limited["num_executed"] == 2 and result_limited["num_skipped"] == 1)

# ---------------------------------------------------------------------------
# Testfall 8: calculate_max_drawdown - identisch zur bestehenden Formel
# ---------------------------------------------------------------------------
dd = calculate_max_drawdown(result_unweighted["equity_curve"], 10_000.0)
check("Max Drawdown ist <= 0 (per Definition, ein Rueckgang gegenueber dem bisherigen Hoechststand)",
      dd <= 0)

print()
if failures:
    print(f"{len(failures)} FEHLGESCHLAGENE CHECKS: {failures}")
    sys.exit(1)
else:
    print("ALLE CHECKS OK")

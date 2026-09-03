"""
Aktuell live genutzte Parameter - Volatility Breakout (Bollinger-Band-Squeeze, Aktien)
================================================================================================
Siehe elliott_wave/live_params.py fuer die Erklaerung des Zwecks dieser Datei.

Historie:
- 2026-09-03: Erste Live-Uebernahme nach vollstaendiger Validierung
  (Backtest -> Walk-Forward -> Equity-Simulation -> Buy-and-Hold ->
  False-Breakout-Filter-Test -> Trailing-Stop-Test -> 2022/2020-
  Stress-Perioden-Vergleich -> Kapitalmanagement-Tuning). 8% Stop-Loss
  als robusteste Kombination validiert (PROTOTYPE_FINDINGS.md Abschnitt 2).
  Volumen-Filter NICHT uebernommen (keine spuerbare Verbesserung,
  Abschnitt 6). Trailing-Stop NICHT uebernommen (Overfitting-Muster,
  identisch zum Elliott-Wave-Aktien-Bot-Praezedenzfall, Abschnitt 7).
  10% Allokation / Limit 15 aus der Kapitalmanagement-Nachpruefung
  uebernommen (Abschnitt 11) statt des urspruenglichen Start-Limits 8 -
  deutlich hoehere Rendite bei nur leicht hoeherem Drawdown; mildert
  NICHT die identifizierte 2022-Baerenmarkt-Schwaeche (Abschnitt 10/11c),
  die weiterhin als bekanntes, spezifisches Risiko gilt.
"""

BB_SQUEEZE_PERCENTILE = 25.0
BB_LOOKBACK = 126
STOP_LOSS_PCT = 8.0
MAX_HOLD_DAYS = 15
ALLOCATION_PCT = 10          # in Prozent - NUR zur Dokumentation, siehe
                              # rsi2_mean_reversion/live_params.py fuer die
                              # Begruendung (forward_test.py trackt kein Kapital)
MAX_CONCURRENT_POSITIONS = 15

LAST_UPDATED = "2026-09-03"

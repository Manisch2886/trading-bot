"""
Aktuell live genutzte Parameter - RSI-2 Mean-Reversion (Aktien)
=======================================================================
Siehe elliott_wave/live_params.py fuer die Erklaerung des Zwecks dieser Datei.

Historie:
- 2026-09-03: Erste Live-Uebernahme nach vollstaendiger Validierung
  (Backtest -> Walk-Forward -> Equity-Simulation -> Buy-and-Hold ->
  Signal-Qualitaets-Test -> Positionsgroesse-x-Limit-Matrix). RSI-Schwelle
  5, kein fester Stop-Loss (empirisch bestaetigt: ein harter Stop senkt
  den Ø-Gewinn/Trade spuerbar, siehe PROTOTYPE_FINDINGS.md Abschnitt 1/9).
  5% Allokation / Limit 20 aus der Kapitalmanagement-Nachpruefung
  uebernommen (PROTOTYPE_FINDINGS.md Abschnitt 6/9) statt des
  urspruenglichen Start-Limits 8 - schoepft den Kapital-Flaschenhals
  spuerbar besser aus, ohne den Diversifikations-Nutzen in der
  2022-Stress-Periode zu verlieren.
"""

RSI_THRESHOLD = 5.0
STOP_LOSS_PCT = None       # "kein Stop" - empirisch als beste Option validiert
MAX_HOLD_DAYS = 10
ALLOCATION_PCT = 5          # in Prozent (nicht 0.05) - NUR zur Dokumentation/fuer
                             # eine kuenftige Kapitalkurven-Rekonstruktion (z.B.
                             # shared/portfolio_overview.py); forward_test.py selbst
                             # trackt keine Positionsgroessen/Kapital, nur Signale
                             # und Trade-Ergebnisse (wie bei den bestehenden Bots)
MAX_CONCURRENT_POSITIONS = 20

LAST_UPDATED = "2026-09-03"

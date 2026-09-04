"""
Aktuell live genutzte Parameter - RSI-2 Mean-Reversion (Krypto)
=======================================================================
Siehe elliott_wave/live_params.py fuer die Erklaerung des Zwecks dieser Datei.

Historie:
- 2026-09-03: Erste Live-Uebernahme nach vollstaendiger Validierung
  (Backtest -> Walk-Forward -> Equity-Simulation -> Buy-and-Hold ->
  BTC-Regime-Filter-Test, siehe PROTOTYPE_FINDINGS.md). SMA-Trendfilter
  fuer Krypto auf 150 Tage rekalibriert (statt 200 wie bei der
  Aktien-Version, Abschnitt 2) - robusteste Gesamtzeitraum-Kombination.
  Kein fester Stop-Loss (identischer Befund wie bei der Aktien-Version:
  ein harter Stop senkt den Erwartungswert). BTC-Regime-Filter NICHT
  uebernommen (schadet der Mean-Reversion-Logik deutlich, Abschnitt 6).
  Standard-Kapitalmanagement (10% Allokation, Limit 8) beibehalten, da
  KEIN Kapital-Flaschenhals festgestellt wurde (nur 10,7%/2,9%
  Skip-Rate, kleineres 20-Symbol-Universum) - anders als bei den beiden
  Aktien-Bots war hier keine Kapitalmanagement-Nachjustierung noetig.
"""

SMA_TREND_FILTER = 150
RSI_THRESHOLD = 10.0
STOP_LOSS_PCT = None        # "kein Stop" - empirisch als beste Option validiert
ALLOCATION_PCT = 10          # in Prozent - NUR zur Dokumentation, siehe
                              # rsi2_mean_reversion/live_params.py fuer die
                              # Begruendung (forward_test.py trackt kein Kapital)
MAX_CONCURRENT_POSITIONS = 8

LAST_UPDATED = "2026-09-03"

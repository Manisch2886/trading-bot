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

# MAX_HOLD_DAYS neu hier aufgenommen - der WERT ist unveraendert 10.
# Er stand bisher zweimal unabhaengig im Bot (backtest_rsi2.py und
# forward_test.py) und in dieser Datei gar nicht; damit war dieser Bot der
# einzige der drei Zeit-Exit-Bots ohne gemeinsame Quelle. Beide Stellen
# lesen ihn jetzt von hier. Die Zahl selbst wurde nicht angefasst.
MAX_HOLD_DAYS = 10           # Tage NACH dem Einstiegstag, keine Kalenderzeit

LAST_UPDATED = "2026-09-03"  # Stand der PARAMETER - MAX_HOLD_DAYS ist neu
                              # aufgenommen, aber nicht neu gesetzt (10 wie
                              # vorher an beiden alten Stellen).

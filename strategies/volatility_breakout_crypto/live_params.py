"""
Aktuell live genutzte Parameter - Volatility Breakout (Bollinger-Band-Squeeze, Krypto)
================================================================================================
Siehe elliott_wave/live_params.py fuer die Erklaerung des Zwecks dieser Datei.

Historie:
- 2026-09-04: Erste Live-Uebernahme nach vollstaendiger Validierung
  (Backtest -> Walk-Forward -> Equity-Simulation -> Buy-and-Hold ->
  BTC-Regime-Filter-Test -> BTC-Regime-Filter-Klaerung ueber drei
  Split-Punkte -> 2022-Krypto-Winter-Test). 5% Stop-Loss als robusteste
  Kombination validiert (PROTOTYPE_FINDINGS.md Abschnitt 2). Squeeze-
  Lookback 126 Tage / 25.-Perzentil unveraendert aus der Aktien-Version
  uebernommen (gleiche Tageskerzen-Logik, siehe Abschnitt 0).

  WICHTIG - BTC_REGIME_FILTER_ENABLED = True, Begruendung (siehe
  PROTOTYPE_FINDINGS.md Abschnitt 9, "Klaerung des uneindeutigen
  BTC-Regime-Filter-Befunds"):
  Der Filter ist hier AKTIV, aber NICHT weil er in jedem Fall die Rendite
  verbessert - bei einem von drei getesteten Walk-Forward-Split-Punkten
  (75/25) war die Rendite MIT Filter sogar niedriger (+18,45% vs. +20,04%
  ohne Filter). Der Filter ist stattdessen als RISIKOMANAGEMENT-MASSNAHME
  aktiv, auf Basis von zwei robusten, in ALLEN drei getesteten Splits
  (65/35, 70/30, 75/25) konsistenten Befunden:
    1. Max Drawdown ist MIT Filter in JEDEM der drei Splits niedriger
       (z.B. 70/30: -11,33% -> -7,76%).
    2. Die bereits als strategie-inhaerent identifizierte 2022-
       Baerenmarkt-Schwaeche (siehe Abschnitt 7/9c) wird durch den Filter
       deutlich UND kausal nachvollziehbar gemildert: -12,35% -> -1,60%
       Rendite, -16,55% -> -6,07% Max Drawdown im Krypto-Winter 2022 -
       der Filter blockiert ueberproportional genau die Fehlausbrueche,
       die diese Schwaeche verursachen (91,3% -> 84,2% Anteil negativer
       Trades in den verbleibenden 2022-Positionen).
  Falls eine kuenftige Ueberpruefung eine niedrigere Rendite ODER weniger
  Trades als eine reine "kein Filter"-Variante feststellt, ist das KEINE
  neue, unerwartete Verschlechterung, sondern der bereits bekannte,
  bewusst in Kauf genommene Trade-off (Risikoreduktion statt garantierter
  Mehrrendite). Nicht ohne erneute Pruefung der 2022-Wirkung deaktivieren.
"""

BB_SQUEEZE_PERCENTILE = 25.0
BB_LOOKBACK = 126
STOP_LOSS_PCT = 5.0
MAX_HOLD_DAYS = 15
BTC_REGIME_FILTER_ENABLED = True   # siehe Historie oben - Risikomanagement, nicht Rendite-Hebel
ALLOCATION_PCT = 10                 # in Prozent - NUR zur Dokumentation, siehe
                                     # rsi2_mean_reversion/live_params.py fuer die
                                     # Begruendung (forward_test.py trackt kein Kapital)
MAX_CONCURRENT_POSITIONS = 8

LAST_UPDATED = "2026-09-04"

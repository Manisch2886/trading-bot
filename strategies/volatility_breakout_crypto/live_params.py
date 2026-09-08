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

# Weitere wirksame Parameter: bewusst NICHT hier definiert - reine Dokumentation.
# ------------------------------------------------------------------------
# Erhoben mit research/backtest_defaults/ (PR #45), Werte am 2026-09-08 erneut
# geprueft. Muster wie beim ALLOCATION_PCT-Block in
# elliott_wave_stocks/live_params.py.
#
# BTC-REGIME-FILTER - die Zahlen hinter dem Schalter oben:
#   BTC_ATR_LENGTH = 22    (regime_filter.py:16)
#   BTC_ATR_MULT   = 3.0   (regime_filter.py:17)
#
# BTC_REGIME_FILTER_ENABLED oben sagt, OB der Filter laeuft; diese beiden
# sagen, WIE er rechnet (SuperTrend auf BTC mit ATR-Laenge 22 und Faktor 3,0).
# Sie wirken tatsaechlich live: forward_test.py:256 ruft
# compute_btc_regime(raw_data["BTCUSDT"]) OHNE Argumente auf, es greifen also
# die Defaults aus regime_filter.py. Anders als beim T3-Bot gibt es hier nur
# EINE Quelle - forward_test.py fuehrt keine eigene Kopie.
#
# VOLUMEN-BESTAETIGUNGSFILTER (live AUS, wie bei der Aktien-Version):
#   use_volume_filter        = False  (Signatur von run_backtest(),
#                                      backtest_breakout.py:97)
#   VOLUME_FILTER_MULTIPLIER = 1.5    (backtest_breakout.py:71)
#   VOLUME_AVG_PERIOD        = 20     (backtest_breakout.py:65)
# equity_simulation.py:133 ruft collect_all_trades() ohne use_volume_filter
# auf; der Multiplikator ist damit heute wirkungslos und beschreibt nur, wie
# der Filter arbeiten wuerde, falls man ihn einschaltet.
#
# BEWUSST NUR DOKUMENTIERT, NICHT GEKOPPELT (PR #45, Befund 7.2).

LAST_UPDATED = "2026-09-04"  # Stand der PARAMETER - der Dokumentationsblock
                              # oben aendert keinen Wert.

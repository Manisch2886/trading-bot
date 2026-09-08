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

# Weitere wirksame Parameter: bewusst NICHT hier definiert - reine Dokumentation.
# ------------------------------------------------------------------------
# Erhoben mit research/backtest_defaults/ (PR #45), Werte am 2026-09-08 erneut
# geprueft. Muster wie beim ALLOCATION_PCT-Block in
# elliott_wave_stocks/live_params.py.
#
# VOLUMEN-BESTAETIGUNGSFILTER (Fehlausbruch-Filter):
#   use_volume_filter        = False  (Literal in der Signatur von
#                                      run_backtest(), backtest_breakout.py:134)
#   VOLUME_FILTER_MULTIPLIER = 1.5    (backtest_breakout.py:103)
#   VOLUME_AVG_PERIOD        = 20     (backtest_breakout.py:97)
#
# Der Filter ist LIVE AUS: forward_test.py erwaehnt ihn gar nicht, und
# equity_simulation.py:160 ruft collect_all_trades() ohne use_volume_filter
# auf. Der Multiplikator 1.5 ist damit heute wirkungslos - er beschreibt nur,
# WIE der Filter arbeiten wuerde (Ausbruchstag-Volumen > 1,5-faches
# 20-Tage-Durchschnittsvolumen), falls man ihn einschaltet. Der Vergleich
# mit/ohne steht in experiment_false_breakout_filter.py; das Ergebnis "keine
# spuerbare Verbesserung" ist der Grund fuer das AUS (siehe Historie oben).
#
# Er steht hier trotzdem, weil er sonst nur beim Lesen der Backtest-Datei
# auffiele - und weil aus "wirkungslos" ein wirksamer Wert wird, sobald
# jemand use_volume_filter auf True setzt.
#
# BEWUSST NUR DOKUMENTIERT, NICHT GEKOPPELT (PR #45, Befund 7.2).

LAST_UPDATED = "2026-09-03"  # Stand der PARAMETER - der Dokumentationsblock
                              # oben aendert keinen Wert.

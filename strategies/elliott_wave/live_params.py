"""
Aktuell live genutzte Parameter - Elliott-Wave-Strategie (Krypto)
=======================================================================
Diese Datei enthaelt NUR die Parameter, die forward_test.py aktuell
tatsaechlich nutzt. Bewusst von der restlichen Skript-Logik getrennt,
damit eine Parameter-Aenderung (z.B. nach einem quartalsweisen Review-
Vorschlag) so einfach wie moeglich ist: nur diese Werte anpassen,
sonst nichts am Code veraendern.

Historie:
- bis 2026-09-07: Zigzag 4 %, Stop-Loss 2 %, Ziel Fib 0.236. Diese
  Kombination stammte aus einer Rasteroptimierung auf einer
  Backtest-Grundlage MIT Look-Ahead: der Backtest stieg zum Preis des
  Wellenende-Pivots ein, wodurch der Stop bis zur Bestaetigung dieses
  Pivots mathematisch unerreichbar war. Ein enger Stop kostete dort
  also nichts. Siehe research/elliott_wave_lookahead/ (PR #26).
- 2026-09-07: Umgestellt auf Zigzag 10 %, Stop-Loss 6 %, Ziel Fib
  0.618 - die erste Parameterwahl dieses Bots auf kausal sauberer
  Grundlage (Einstieg zum Schlusskurs des Bestaetigungsbalkens, keine
  rueckwirkend verdraengten Wellen). Begruendung und alle Zahlen:
  research/elliott_wave_params/BERICHT.md (PR #28).

  Kurzfassung: Die alte Kombination bestand auf sauberer Grundlage
  KEINE der fuenf dort festgelegten Bedingungen - der 2-%-Stop loeste
  bei 72,6 % der Trades aus, bevor die erwartete Korrektur ueberhaupt
  Zeit hatte, und nur 4 von 18 Coins trugen positiv bei. Die neue
  Kombination besteht alle fuenf, ist in allen drei Walk-Forward-
  Falten positiv, 15 von 18 Coins tragen positiv bei, Gewinnrate
  43,8 % statt 27,4 %. Ueber den Gesamtzeitraum +67,8 % bei -10,2 %
  Max Drawdown gegen Buy-and-Hold +12,2 % bei -79,8 %.

  ACHTUNG - die ersten Live-Wochen bitte genauer beobachten: die
  Out-of-Sample-Stichprobe umfasste nur 31 Trades und lag damit knapp
  ueber der Mindestschwelle von 30. Der grobe Zigzag erzeugt zudem
  deutlich weniger Signale als bisher (130 statt 791 Trades in fuenf
  Jahren) - eine laengere signallose Phase ist also normal und noch
  kein Hinweis auf einen Fehler. Umgekehrt ist die Stichprobe zu
  klein, um eine Abweichung frueh sicher als Problem zu erkennen; im
  Zweifel lieber einmal zu viel nachsehen.

Hinweis: strategies/elliott_wave/equity_simulation.py haelt dieselben
drei Werte noch einmal als eigene Konstanten und wurde hier BEWUSST
nicht mitgeaendert (siehe Sync-Check, PR #24). Wer von dort einen
Backtest startet, rechnet also weiterhin mit 4 % / 2 % / 0.236.
"""

DEVIATION_PCT = 10.0
STOP_LOSS_PCT = 6.0
TAKE_PROFIT_FIB = 0.618

LAST_UPDATED = "2026-09-07"  # manuell aktualisieren bei jeder Aenderung

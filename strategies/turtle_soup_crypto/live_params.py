"""
Aktuell live genutzte Parameter - Turtle Soup (False-Breakout-Reversal, Krypto)
================================================================================================
Siehe elliott_wave/live_params.py fuer die Erklaerung des Zwecks dieser Datei.

Historie:
- 2026-09-04: Erste Live-Uebernahme nach vollstaendiger Validierung
  (Backtest -> Walk-Forward -> Equity-Simulation -> Buy-and-Hold ->
  Abgrenzung zu Volatility Breakout -> Kapitalmanagement-Tuning,
  siehe PROTOTYPE_FINDINGS.md Abschnitt 8). Donchian-Lookback 10, Stop
  "structural" (Stop-Kurs = Tagestief des Setup-Tags selbst) als
  robusteste Kombination validiert (Abschnitt 2 - anders als bei Aktien
  gewinnt hier der musterspezifische Stop, Kryptos hoehere Tagesvolatilitaet
  laesst echte Reversal-Bewegungen deutlicher ausfallen), 10-Tage-Zeit-Exit
  unveraendert aus der Aktien-Version.

  WICHTIG - Kapitalmanagement UNVERAENDERT bei Limit 8 / 10% Allokation
  belassen (siehe PROTOTYPE_FINDINGS.md Abschnitt 8b/8c): anders als bei
  Aktien bringt eine Lockerung des Kapitalmanagements bei Krypto KEINEN
  Mehrwert - jede getestete Alternative (kleinere Allokation und/oder
  hoeheres Limit) verschlechtert sowohl die Gesamtzeitraum-Rendite als auch
  den Max Drawdown UND die 2022-Krypto-Winter-Performance gegenueber der
  urspruenglichen Basiskonfiguration. Die urspruengliche Konfiguration war
  bereits nahe am Optimum des gesamten getesteten Grids - hier gibt es
  aktuell keinen Kapitalmanagement-Hebel zu ziehen. Falls eine kuenftige
  Ueberpruefung erneut eine Lockerung erwaegt, zuerst
  experiment_capital_management_summary.py erneut pruefen, ob sich das
  Bild (z.B. durch neue Symbole im Universum) veraendert hat.
"""

DONCHIAN_PERIOD = 10
STOP_MODE = "structural"  # Stop = Tagestief des Setup-Tags - beste validierte Kombination
MAX_HOLD_DAYS = 10
ALLOCATION_PCT = 10          # in Prozent - NUR zur Dokumentation, siehe
                              # rsi2_mean_reversion/live_params.py fuer die
                              # Begruendung (forward_test.py trackt kein Kapital)
MAX_CONCURRENT_POSITIONS = 8  # Basiskonfiguration unveraendert - siehe Historie oben

LAST_UPDATED = "2026-09-04"

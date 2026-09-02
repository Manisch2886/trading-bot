"""
Aktuell live genutzte Parameter - Elliott-Wave-Strategie (Aktien)
=======================================================================
Siehe elliott_wave/live_params.py fuer die Erklaerung des Zwecks dieser Datei.

Historie:
- 2026-09-01: Zigzag 5%, Stop-Loss 2%, Ziel 0.236, Top 100 Aktien (erste
  robuste Validierung, aber Buy-and-Hold schlug die Strategie leicht)
- 2026-09-02: Aktualisiert auf Top 150 Aktien mit Stop-Loss 3% -
  Out-of-Sample bestaetigt (Ø PnL 7.37%, 132 Trades/79 Symbole),
  schlaegt Buy-and-Hold klar (1458% vs. 756% Rendite,
  -1.32% vs. -34.83% Max Drawdown). Signal-Qualitaets-Test zeigt:
  Mehrwert kommt aus Timing/Kapitalmanagement, nicht aus den
  Ausstiegsregeln selbst - siehe Chat-Diskussion.
"""

DEVIATION_PCT = 5.0
STOP_LOSS_PCT = 3.0
TAKE_PROFIT_FIB = 0.236
MAX_CONCURRENT_POSITIONS = 8

LAST_UPDATED = "2026-09-02"

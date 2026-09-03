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
- 2026-09-03: USE_TAKE_PROFIT auf False gesetzt (Gewinne laufen lassen) -
  empirisch getestet (Gesamtzeitraum + Out-of-Sample), Rendite ca.
  verdoppelt (+3084% statt +1500% Gesamtzeitraum, +204% statt +108% OOS)
  bei moderat hoeherem, aber weiterhin klar unter Buy-and-Hold liegendem
  Drawdown (-9.79%/-5.04% statt -1.90%/-1.65%). Positionslimit bewusst
  bei 8 belassen (konservativerer Zwischenschritt statt unbegrenzt -
  Option B mit unbegrenztem Limit war in der Matrix noch staerker, aber
  noch nicht uebernommen). Siehe
  results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md fuer Details.
"""

DEVIATION_PCT = 5.0
STOP_LOSS_PCT = 3.0
TAKE_PROFIT_FIB = 0.236   # nur relevant, falls USE_TAKE_PROFIT=True
USE_TAKE_PROFIT = False   # Gewinne laufen lassen statt festes Kursziel
MAX_CONCURRENT_POSITIONS = 8

LAST_UPDATED = "2026-09-03"

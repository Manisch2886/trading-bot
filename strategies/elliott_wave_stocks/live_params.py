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
  ACHTUNG: Die Buy-and-Hold-Aussage dieses Eintrags ist ueberholt -
  siehe Eintrag 2026-09-08.
- 2026-09-03: USE_TAKE_PROFIT auf False gesetzt (Gewinne laufen lassen) -
  empirisch getestet (Gesamtzeitraum + Out-of-Sample), Rendite ca.
  verdoppelt (+3084% statt +1500% Gesamtzeitraum, +204% statt +108% OOS)
  bei moderat hoeherem, aber weiterhin klar unter Buy-and-Hold liegendem
  Drawdown (-9.79%/-5.04% statt -1.90%/-1.65%). Positionslimit bewusst
  bei 8 belassen (konservativerer Zwischenschritt statt unbegrenzt -
  Option B mit unbegrenztem Limit war in der Matrix noch staerker, aber
  noch nicht uebernommen). Siehe
  results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md fuer Details.
- 2026-09-08: Nur Dokumentation korrigiert, KEIN Parameter geaendert.
  Die Buy-and-Hold-Aussage vom 2026-09-02 ("schlaegt Buy-and-Hold klar,
  1458% vs. 756%") stammte von einer Backtest-Grundlage MIT Look-Ahead:
  der Backtest stieg zum Preis des Wellenende-Pivots ein, wodurch der
  Stop bis zur Bestaetigung dieses Pivots mathematisch unerreichbar war
  (research/elliott_wave_lookahead/BERICHT.md, PR #26). Auf der
  korrigierten, kausal sauberen Grundlage gilt sie nicht mehr.

  Befund der Parameter-Neubestimmung
  (research/elliott_wave_params/BERICHT.md, PR #28): KEINE der 252
  geprueften Kombinationen schlaegt Buy-and-Hold ueber den vollen
  Zehnjahres-Zeitraum. Buy-and-Hold liegt bei +755,7% Rendite bei
  -34,8% Max Drawdown; diese Live-Konfiguration bei +330,2% bei -22,7%.
  Sie bleibt in der Rendite also klar zurueck, faellt dabei aber
  flacher.

  Einordnung dieser Konfiguration - sie ist nicht der Fehler: auf dem
  Gesamtfenster Rang 10 von 116 Kombinationen, die die Mindestfilter
  bestehen, In-Sample Rang 16 von 95, und ihr Out-of-Sample-Ø-PnL ist
  mit 7,52% der beste aller getesteten Kandidaten. Sie scheitert an
  einer einzigen der fuenf dort vorab festgelegten Bedingungen (B3:
  Walk-Forward-Falte 1 mit -1,47%) - an denselben Falten wie fast alle
  anderen Kandidaten auch. Eine nachvollziehbare Wahl unter mehreren
  aehnlich plausiblen Alternativen, aber keine herausragende.

  Die Entscheidung USE_TAKE_PROFIT = False vom 2026-09-03 haelt auf der
  sauberen Grundlage stand: unter den 116 Kombinationen, die die
  Mindestfilter bestehen, sind die vorderen zehn praktisch ausnahmslos
  ohne festes Kursziel.

  Bewusst NICHT mitgeaendert: LAST_UPDATED bleibt auf 2026-09-03. Der
  Wert bezeichnet den Stand der PARAMETER (und wird als solcher in
  research/pnl_2025_fixed_size/extract.py ausgewertet); am 2026-09-08
  wurde ausschliesslich dieser Text korrigiert.
"""

DEVIATION_PCT = 5.0
STOP_LOSS_PCT = 3.0
TAKE_PROFIT_FIB = 0.236   # nur relevant, falls USE_TAKE_PROFIT=True
USE_TAKE_PROFIT = False   # Gewinne laufen lassen statt festes Kursziel
MAX_CONCURRENT_POSITIONS = 8

# ALLOCATION_PCT: bewusst NICHT hier definiert - reine Dokumentation.
# ------------------------------------------------------------------------
# Der tatsaechlich wirksame Wert ist 10 % je Trade. Er steht in
# equity_simulation.py (ALLOCATION_PCT = 0.10, dort als ANTEIL notiert, nicht
# in Prozent) und gleichlautend in oos_equity_simulation.py sowie in allen
# experiment_*.py dieses Bots. Seit dem Initial Commit unveraendert - per
# git-Historie geprueft.
#
# forward_test.py dieses Bots trackt kein Kapital und keine Positionsgroessen
# (nur Signale, Trade-Ergebnisse und das Positionslimit oben); der Wert wirkt
# daher ausschliesslich in den Backtest-/Simulationsskripten. Deshalb steht er
# hier NICHT als Konstante: diese Datei enthaelt laut Kopfkommentar von
# elliott_wave/live_params.py nur, was forward_test.py tatsaechlich nutzt.
#
# Hintergrund: mehrere Research-Studien (research/volatility_scaled_sizing,
# research/trailing_stops) mussten den Wert mangels Eintrag hier annehmen und
# haben ihn als Annahme ausgewiesen. Die Annahme war korrekt - 10 %.
#
# Beobachtung, hier bewusst NICHT geaendert: shared/portfolio_overview.py
# importiert fuer Bots mit genuegend Live-Trades `ALLOCATION_PCT` aus dieser
# Datei. Der Eintrag fehlt hier; dieser Pfad wuerde fuer diesen Bot also
# fehlschlagen, sobald seine Live-DB die Schwelle erreicht. Das zu beheben
# waere eine Verhaltensaenderung an einem bislang nicht erreichten Codepfad -
# und die ist nicht Teil dieser Dokumentations-Ergaenzung.

LAST_UPDATED = "2026-09-03"

"""
Aktuell live genutzte Parameter - Elliott-Wave-Strategie (Krypto)
=======================================================================
Diese Datei enthaelt NUR die Parameter, die forward_test.py aktuell
tatsaechlich nutzt. Bewusst von der restlichen Skript-Logik getrennt,
damit eine Parameter-Aenderung (z.B. nach einem quartalsweisen Review-
Vorschlag) so einfach wie moeglich ist: nur diese Werte anpassen,
sonst nichts am Code veraendern.

Letztes Update: manuell einzutragen, wenn du eine neue Kombination
uebernimmst - hilft, den Ueberblick zu behalten.
"""

DEVIATION_PCT = 4.0
STOP_LOSS_PCT = 2.0
TAKE_PROFIT_FIB = 0.236

# ALLOCATION_PCT: bewusst NICHT hier definiert - reine Dokumentation.
# ------------------------------------------------------------------------
# Der tatsaechlich wirksame Wert ist 10 % je Trade. Er steht in
# equity_simulation.py (ALLOCATION_PCT = 0.10, dort als ANTEIL notiert, nicht
# in Prozent) und gleichlautend in oos_equity_simulation.py. Seit dem Initial
# Commit unveraendert - per git-Historie geprueft.
#
# forward_test.py dieses Bots trackt weder Kapital noch Positionsgroessen (nur
# Signale und Trade-Ergebnisse) und kennt auch kein Positionslimit; der Wert
# wirkt daher ausschliesslich in den Backtest-/Simulationsskripten. Deshalb
# steht er hier NICHT als Konstante: diese Datei enthaelt laut ihrem
# Kopfkommentar nur, was forward_test.py tatsaechlich nutzt.
#
# Hintergrund: mehrere Research-Studien (research/volatility_scaled_sizing,
# research/trailing_stops) mussten den Wert mangels Eintrag hier annehmen und
# haben ihn als Annahme ausgewiesen. Die Annahme war korrekt - 10 %.
#
# Beobachtung, hier bewusst NICHT geaendert: shared/portfolio_overview.py
# importiert fuer Bots mit genuegend Live-Trades `ALLOCATION_PCT` UND
# `MAX_CONCURRENT_POSITIONS` aus dieser Datei. Beide fehlen hier; dieser Pfad
# wuerde fuer diesen Bot also fehlschlagen, sobald seine Live-DB die Schwelle
# erreicht. Ein Positionslimit hat dieser Bot aber bewusst nicht (siehe
# research/order_sensitivity), es hier zu ergaenzen waere eine
# Verhaltensaenderung - und die ist nicht Teil dieser Dokumentations-Ergaenzung.

LAST_UPDATED = "2026-08-31"  # manuell aktualisieren bei jeder Aenderung

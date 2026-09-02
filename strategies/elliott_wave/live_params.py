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

LAST_UPDATED = "2026-08-31"  # manuell aktualisieren bei jeder Aenderung

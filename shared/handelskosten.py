#!/usr/bin/env python3
"""
Die Handelskosten der Backtests: EIN Ort, drei Konstanten
==============================================================================
Der eine Ort der registrierten Kosten (Sperrlistenpunkt 9 im Register
`docs/VORREGISTRIERUNG_neuselektion.md`, Registertext 37.5 und 38.5):

    TRADING_FEE_PCT = 0.1    je Order (Einstieg und Ausstieg je einmal)
    SLIPPAGE_PCT    = 0.05   angenommene Abweichung vom gewuenschten Preis,
                             je Order

Summe je Rundlauf: 2 x (0,1 + 0,05) = 0,30 %. Herkunft der Gebuehr:
"Realistische Handelskosten (Binance Spot: ~0.1% pro Order als Standard)",
fuer alle neun Bots dieselbe Annahme wie bei der Elliott-Wave-Strategie.

Die neun `strategies/*/backtest_*.py` importieren beide Werte von hier und
tragen keine eigene Kopie (38.5): Der Wert kann im Laufmodul nicht abweichen,
weil er dort nicht steht. Bis TB-90 stand er dort neunmal als Zuweisung; die
Kommentare von damals stehen oben.

Bewusst NICHT hier angebunden (38.5): die `forward_test.py` (Papierpfad,
eigene Freigabe) und `research/vorregistrierung/messgroessen.py`
(eingefroren, `GEBUEHR_PCT`).

Dazu das registrierte Startkapital je Bot (Ergaenzung zu 29.3 nach R109 (a) in
der Fassung R110 (b), TB-180):

    STARTING_CAPITAL    10 000   Startkapital des Kapitalpfads, gleich fuer alle neun

Die neun `strategies/*/equity_simulation.py` importieren es von hier und tragen
keine eigene Kopie (Bauart 38.5); bis TB-180 stand es dort neunmal als Zuweisung.

Keine Funktion, keine Berechnung, kein Import, kein Seiteneffekt - ein Modul,
das nur Werte traegt, kann nicht heimlich etwas anderes tun.
"""

TRADING_FEE_PCT = 0.1      # je Order (Einstieg und Ausstieg je einmal)
SLIPPAGE_PCT = 0.05        # angenommene Abweichung vom gewuenschten Preis, je Order
STARTING_CAPITAL = 10_000.0    # Startkapital je Bot (29.3, R110 (b))

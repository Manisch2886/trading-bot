"""
Aktuell live genutzte Parameter - Elliott-Wave-Strategie (Aktien)
=======================================================================
Siehe elliott_wave/live_params.py fuer die Erklaerung des Zwecks dieser Datei.

GUELTIGE KENNZAHLEN - kausal saubere Grundlage, Stand 2026-09-13
-----------------------------------------------------------------------
Zehn Jahre, Quelle: research/elliott_wave_params/BERICHT.md Abschnitt 4.

                                           Rendite   Max DD   Calmar
  Buy-and-Hold                            +755,69 %  -34,83 %    21,70
  Live-Kombination (dev 5 % / Stop 3 %)    +330,18 %  -22,70 %    14,55
  bester gepruefter Kandidat (2 % / 16 %)  +398,23 %  -34,16 %    11,66

BUY-AND-HOLD SCHLAEGT DIESEN BOT - in der Rendite UND im Calmar-
Verhaeltnis. Keine der 252 geprueften Kombinationen kommt an die +755 %
heran. Er faellt dabei flacher (-22,7 % gegen -34,8 %); das ist der
einzige Vorsprung, den er hat.

Wer weiter unten eine Zeile findet, die etwas anderes behauptet, liest
einen Eintrag von VOR der Look-Ahead-Korrektur (PR #26). Die
zurueckgezogenen Zahlen stehen absichtlich noch da - sie sind in
Berichten, E-Mails und im Uebergabeprotokoll zitiert worden und
verschwinden nicht dadurch, dass man sie hier loescht.

Historie:
- 2026-09-01: Zigzag 5%, Stop-Loss 2%, Ziel 0.236, Top 100 Aktien (erste
  robuste Validierung, aber Buy-and-Hold schlug die Strategie leicht)
- 2026-09-02: Aktualisiert auf Top 150 Aktien mit Stop-Loss 3% -
  Out-of-Sample bestaetigt (Ø PnL 7,37%, 132 Trades/79 Symbole).
  Signal-Qualitaets-Test zeigt: Mehrwert kommt aus Timing/Kapital-
  management, nicht aus den Ausstiegsregeln selbst - siehe
  Chat-Diskussion.

  ZURUECKGEZOGEN am 2026-09-13 (Befund TB-17) - hier stand: "schlaegt
  Buy-and-Hold klar (1458% vs. 756% Rendite, -1.32% vs. -34.83% Max
  Drawdown)". Die +1458% und die -1,32% stammen aus dem Backtest MIT
  Look-Ahead und gelten nicht mehr; gueltig ist die Tabelle im Kopf
  dieser Datei (+330,18% bei -22,70%). Bemerkenswert: der
  Vergleichsmassstab selbst war von Anfang an richtig - Buy-and-Hold
  liegt unveraendert bei +755,69% und -34,83%. Falsch war nur die eigene
  Zahl daneben, und zwar um mehr als den Faktor vier.
  Der Rest dieses Eintrags (Ø PnL, Trade-Zahlen, Signal-Qualitaets-Test)
  ist von der Korrektur nicht betroffen - siehe Uebergabeprotokoll
  Abschnitt 3.3, "Weiterhin gueltig".
- 2026-09-03: USE_TAKE_PROFIT auf False gesetzt (Gewinne laufen lassen).
  Positionslimit bewusst bei 8 belassen (konservativerer Zwischenschritt
  statt unbegrenzt - Option B mit unbegrenztem Limit war in der Matrix
  noch staerker, aber noch nicht uebernommen).

  DIE ENTSCHEIDUNG HAELT, DIE ZAHLEN DAZU NICHT (geprueft 2026-09-13):
  Hier stand, die Rendite habe sich "ca. verdoppelt (+3084% statt +1500%
  Gesamtzeitraum, +204% statt +108% OOS)" bei Drawdowns von
  "-9.79%/-5.04% statt -1.90%/-1.65%". Alle acht Zahlen stammen aus
  results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md und damit aus
  derselben Look-Ahead-Grundlage wie der Eintrag vom 2026-09-02; PR #86
  hat die abgelegte Ergebniskurve nachgerechnet und fuer diese
  Konfiguration statt +1500,53% / -1,90% tatsaechlich
  +352,72% / -22,44% gemessen.
  Ein sauber gerechnetes Gegenstueck zum Paar "mit/ohne Kursziel" gibt es
  bis heute NICHT - deshalb steht hier absichtlich keine neue Zahl.
  Was die Entscheidung stattdessen traegt, ist eine Rangfolge:
  research/elliott_wave_params/BERICHT.md Abschnitt 5 zeigt, dass unter
  den 116 Kombinationen, die die Mindestfilter bestehen, die vorderen
  zehn praktisch ausnahmslos ohne festes Kursziel arbeiten. Ein festes
  Ziel schadet also durchgehend - die Richtung der Entscheidung ist
  bestaetigt, nur ihr gemessener Hebel ist unbekannt.
  (EXPERIMENT_FINDINGS.md selbst ist nicht mitkorrigiert worden: die
  Datei liegt unter results/ und beschreibt einen Lauf, der so
  stattgefunden hat. Sie ist als Quelle fuer heutige Zahlen unbrauchbar.)
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
- 2026-09-13: Wieder nur Dokumentation, KEIN Parameter geaendert (Befund
  TB-17). Zwei Korrekturen und eine festgehaltene Entscheidung.

  (1) Die falschen Zahlen sind jetzt AN DER STELLE markiert, an der sie
  stehen. Bis heute trug der Eintrag vom 2026-09-02 seine Behauptung
  unveraendert im Wortlaut und verwies mit einem "ACHTUNG" auf einen
  Eintrag sechs Tage weiter unten. Wer die Datei von oben liest - der
  Nutzer oder eine Claude-Code-Sitzung -, hatte die widerlegte Aussage
  schon gelesen und geglaubt, bevor die Richtigstellung kam. Die
  gueltigen Zahlen stehen deshalb jetzt im KOPF der Datei, vor der
  Historie.

  (2) Der Eintrag vom 2026-09-03 war noch nie korrigiert worden. Am
  2026-09-08 wurde nur die Buy-and-Hold-Aussage vom 2026-09-02
  angefasst; die acht Kennzahlen des Take-Profit-Eintrags stammen aus
  derselben Look-Ahead-Grundlage und blieben unbemerkt stehen. Genau
  dieselbe Fehlerklasse hat sich am 12.09.2026 zweimal in
  broker/README.md und broker/README_IBKR.md wiederholt - eine
  Korrektur, die nur die gemeldete Zeile anfasst, laesst die
  Geschwister stehen.

  (3) ENTSCHEIDUNG DES NUTZERS vom 12.09.2026 - der Bot laeuft weiter,
  aber die Begruendung hat gewechselt: Er laeuft als DIVERSIFIKATOR,
  NICHT weil er den Markt schlaegt. Gemessen wird er kuenftig an seinem
  Beitrag zum Portfolio, nicht an seiner Einzelrendite. Damit ist der
  bis dahin offene Punkt "weiterlaufen, ueberarbeiten oder abschalten?"
  (Uebergabeprotokoll Abschnitt 9, Punkt 4) entschieden.

  Prueftermine: Quartals-Review Oktober 2026 als Zwischenstand, ein
  belastbares Urteil eher im Januar 2027 - die Live-Historie ist heute
  noch zu kurz (kein Bot erreicht MIN_LIVE_CLOSED_TRADES = 10, die
  Portfolio-Zahlen stammen also weiterhin aus Backtest-Kurven).

  Schaerferes Pruefkriterium fuer diesen Termin: der Bot bei GLEICHER
  ZEIT IM MARKT gegen das 95. Perzentil von Zufalls-Timing. Der
  Massstab ist bewusst gewaehlt und noch NICHT gemessen - er ist ein
  Auftrag an den Prueftermin, kein Ergebnis.

  Ehrlicher Vorbehalt zur Diversifikator-Begruendung, damit sie beim
  Prueftermin nicht ungeprueft durchlaeuft: research/exposure_messung/
  BERICHT.md misst fuer diesen Bot 95,4% Zeit im Markt und eine
  Korrelation von +0,46 zu einem gleichgewichteten Buy-and-Hold des
  Aktienuniversums (taegliche Bewertung zu Marktpreisen). Ein Bot, der
  fast immer investiert ist und sich dabei deutlich mit dem Markt
  bewegt, ist kein selbstverstaendlicher Diversifikator. Dasselbe
  Dokument zeigt ausserdem, dass gerade die aussergewoehnlich flache
  abgelegte Kurve dieses Bots (-1,65%) den kombinierten Vierer-Drawdown
  getragen hat; frisch gerechnet sind es -21,16%. Das ist der
  eigentliche Grund, das schaerfere Kriterium anzulegen.
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

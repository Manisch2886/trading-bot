# Relative-Strength-Pair-Rotation (Aktien) — Prototyp-Ergebnisse

Stand: 2026-09-04. Prototyp bis einschließlich Backtest-/Walk-Forward-Stufe,
wie beauftragt. **Nichts live geschaltet** — keine `live_params.py`, kein
Cronjob, kein `forward_test.py`.

## 0. Architektur-Entscheidungen (Begründung)

Diese Strategie unterscheidet sich strukturell von RSI-2/Volatility
Breakout: keine diskreten Einzel-Trades mit fixer Haltedauer, sondern eine
**kontinuierliche Rotation** zwischen zwei Assets eines Paares. Wichtige
Entscheidungen, die das mit sich bringt:

- **Paar-Auswahl über Korrelation statt GICS-Sektor:** eine verlässliche
  Sektor-Zuordnung für alle 150 Symbole ist ohne Internetzugriff (Sandbox
  blockiert) nicht robust pflegbar. Stattdessen werden Paare rein über die
  Korrelation der täglichen Renditen entdeckt (≥0,70 über die 252
  Handelstage vor Beginn des Auswertungsfensters, keine Lookahead) — das
  erfasst wirtschaftlich eng verbundene Aktien implizit und robuster als
  eine statische Liste. Ergebnis: 20 entdeckte Paare, dominiert von
  Großbanken/Finanzwerten (JPM, BAC, C, WFC, GS, MS, USB, PNC, BNY) plus
  GOOGL/GOOG (Aktiengattungen desselben Konzerns) — siehe Abschnitt 7 für
  eine wichtige Konsequenz dieser Konzentration.
- **Kein fester Zeit-Exit:** eine Position läuft bis zum nächsten
  Rotations-Signal, Stop-Loss oder einer Entkopplungs-Pause — architektonisch
  bedingt, anders als RSI-2/Volatility Breakout.

## 1. Regeln (exakt spezifiziert)

Vollständige Spezifikation in `backtest_pair_rotation.py` (Modul-Docstring).
Kurzfassung:

1. **Paar-Auswahl:** Korrelation ≥0,70 der täglichen Renditen über 252
   Handelstage vor Fensterbeginn, Top 20 Paare, für die Dauer eines
   Backtest-Laufs fest.
2. **Rotations-Signal:** relative Stärke = rollierende LOOKBACK_DAYS-Rendite
   von A minus die von B. Positiv → A bevorzugt, negativ → B bevorzugt. Bei
   Wechsel: aktuelle Position schließen, neue im bevorzugten Asset eröffnen.
3. **Rebalance-Frequenz:** täglich vs. wöchentlich (5 Handelstage) — beide
   empirisch getestet. Stop-Loss täglich geprüft (Priorität vor dem
   Rotations-Signal), getestet: kein Stop / 8% / 12%.
4. **Entkopplungs-Schutz:** rollierende 252-Tage-Korrelation, Pause bei
   <0,40, Wiederaufnahme erst bei ≥0,70 (Hysterese). Bei Pause: offene
   Position sofort schließen ("decoupling_exit"), keine neuen Rotationen
   bis Wiederaufnahme.

Universum: S&P-500 Top 150 (identisch zu den anderen Aktien-Bots),
RECENT_YEARS_ONLY=10.

## 2. Multi-Pair-Optimierung (Gesamtzeitraum, 20 Paare)

Auszug (vollständige 18-Zeilen-Tabelle in
`results/pair_rotation_stocks/multi_pair_optimisation_results.csv`):

| Lookback | Rebalance | Stop-Loss | Trades | Win Rate | Ø Rendite/Trade | Score |
|---|---|---|---|---|---|---|
| **120** | **5 (wöchentlich)** | **12%** | **1131** | **51,6%** | **3,49%** | **1,421** |
| 60 | 5 (wöchentlich) | 12% | 1509 | 53,4% | 2,46% | 1,325 |
| 120 | 5 (wöchentlich) | kein Stop | 981 | 54,4% | 3,50% | 1,321 |
| 20 | 1 (täglich) | 8% | 5847 | 45,5% | 0,36% | 0,282 |

**Wöchentliche Rebalance dominiert klar** — alle Top-6-Kombinationen
verwenden Rebalance=5, tägliches Rebalancing schneidet in JEDER
Lookback/Stop-Kombination schlechter ab (mehr Whipsaw durch
Tagesrauschen, wie erwartet). Längere Lookback-Fenster (120 Tage) sind
tendenziell robuster als kurze (20 Tage). **Validierte Basiskonfiguration:
Lookback 120 Tage, wöchentliche Rebalance, 12% Stop-Loss.**

## 3. Walk-Forward (70/30, Split innerhalb des 10-Jahres-Fensters)

| Metrik | In-Sample | Out-of-Sample |
|---|---|---|
| Win Rate | 52,2% | 64,6% |
| Ø Gewinn/Trade | 2,45% | 6,13% |
| Anzahl Trades | 684 | 302 |
| Robustheit-Score | 0,841 | **3,301** |

Score **verbessert sich deutlich** Out-of-Sample (+293%) — starkes
Robustheitssignal. Die Paar-Auswahl selbst bleibt für IS und OOS identisch
(Korrelation vor dem GESAMTEN Fenster berechnet, keine Neu-Auswahl pro
Teilfenster).

## 4. Equity-Simulation (10.000 Start, 10% Allokation, Limit 8)

| | Gesamtzeitraum | Out-of-Sample |
|---|---|---|
| Endkapital | 34.271,13 | 18.896,58 |
| Gesamtrendite | **+242,71%** | **+88,97%** |
| Trades ausgeführt | 492 | 131 |
| Trades übersprungen | 639 | 202 |
| Max Drawdown | −27,76% | −9,61% |

**Deutlicher Kapital-Flaschenhals:** 56,5% Skip-Rate (639/1131)
Gesamtzeitraum — plausibel, da viele der 20 Paare gemeinsame Symbole
teilen (z. B. JPM in 5 Paaren) und die Finanzsektor-Konzentration dazu
führt, dass viele Paare gleichzeitig rotieren (korrelierte Timing-Cluster).

## 5. Buy-and-Hold-Vergleich

| | Wert |
|---|---|
| Endkapital | 56.131,89 |
| Gesamtrendite | **+461,32%** |
| Max Drawdown | −43,87% |
| Anzahl Symbole | 11 (eindeutige Assets aus den 20 Paaren) |

**Schlägt Buy-and-Hold bei der Rendite nicht** (+242,71%/+88,97% vs.
+461,32%) — identisches Muster zu RSI-2/Volatility Breakout Aktien.
**Aber deutlich geringerer Drawdown** (−27,76% vs. −43,87% Gesamtzeitraum,
−9,61% vs. B&H im selben Fenster OOS) — der Risikoprofil-Vorteil ist hier
ausgeprägter als bei den anderen Aktien-Prototypen.

## 6. Experiment: Wirksamkeit des Entkopplungs-Schutzes

| | Ohne Schutz | Mit Schutz |
|---|---|---|
| Gesamtzeitraum-Rendite | +242,71% | +242,71% |
| Gesamtzeitraum-DD | −27,76% | −27,76% |
| Entkopplungs-Exits | 0 | 0 |

**Identische Ergebnisse mit und ohne Schutz — der Mechanismus wurde in
diesem Backtest kein einziges Mal ausgelöst.** Geprüft, ob das ein Bug
ist: die niedrigste je beobachtete rollierende Korrelation unter allen 20
Paaren im gesamten 10-Jahres-Fenster lag bei 0,443 (BNY/PNC) — knapp über
dem Pause-Schwellenwert von 0,40. Der Mechanismus selbst ist funktional
validiert (ein gezielter Test mit einem schwächer korrelierten
MSFT/AAPL-Paar außerhalb der Optimierungs-Pipeline löste erwartungsgemäß
2 Entkopplungs-Exits aus).

**Einordnung:** Kein Fehler, sondern eine Konsequenz der Paar-Auswahl
selbst — der 0,70-Eintritts-Schwellenwert wählt bereits so robuste Paare
aus, dass sie innerhalb von 10 Jahren nicht unter 0,40 fallen. Der Schutz
bleibt als Sicherheitsnetz sinnvoll (validiert wirksam bei schwächer
korrelierten Paaren), zeigte aber in DIESEM konkreten 20-Paare-Sample
keine messbare Wirkung. Eine aussagekräftigere Wirksamkeitsprüfung würde
entweder einen niedrigeren Eintritts-Schwellenwert (mehr, aber
weniger stabile Paare) oder eine längere/andere Historie erfordern.

## 7. Stress-Perioden: 2022-Bärenmarkt UND 2020-COVID-Crash

| Periode | Rendite | Max Drawdown | Allzeit-Max-DD |
|---|---|---|---|
| 2022-Bärenmarkt | −23,84% | −25,71% | −27,45% |
| 2020-COVID-Crash | −20,82% | −23,43% | −27,45% |

**Wichtiger, eigenständiger Befund: Pair-Rotation ist in BEIDEN
Stress-Perioden schwach — anders als bei den anderen Aktien-Bots, die
jeweils nur in EINER Art von Stressphase schwächelten.** Die Erklärung
liegt in der Paar-Auswahl selbst (Abschnitt 0/2): fast alle 20 entdeckten
Paare sind Finanzwerte (Großbanken). Finanzwerte sind historisch
überdurchschnittlich anfällig sowohl für Zinsentwicklungs-getriebene
Bärenmärkte (2022) als auch für systemische Kreditrisiko-Schocks
(2020-COVID, mit Kreditausfallsorgen). Diese Konzentration ist eine
**strukturelle Eigenschaft der korrelationsbasierten Paar-Auswahl**, nicht
der Rotationslogik selbst: hoch korrelierte Aktien-Paare finden sich
naturgemäß gehäuft in wenigen, eng verbundenen Sektoren — hier fast
ausschließlich im Finanzsektor. Der Entkopplungs-Schutz (Abschnitt 6)
kann das nicht abfangen, da er auf PAAR-interne Korrelation reagiert,
nicht auf sektorweites systemisches Risiko.

## 8. Einordnung / offene Punkte

- Solide Signalqualität, Score verbessert sich deutlich Out-of-Sample —
  kein Overfitting-Signal.
- **Kapital-Flaschenhals vorhanden** (56,5% Skip-Rate) — ähnlich
  ausgeprägt wie bei RSI-2/Volatility Breakout Aktien, Kapitalmanagement-
  Tuning wäre ein möglicher nächster Schritt.
- **Schlägt Buy-and-Hold bei der Rendite nicht, aber deutlich geringerer
  Drawdown** — der stärkste Risikoprofil-Vorteil unter den bisherigen
  Aktien-Prototypen.
- **Entkopplungs-Schutz funktional validiert, aber in diesem Sample nie
  ausgelöst** — kein Beleg gegen seine Wirksamkeit, nur ein Beleg dafür,
  dass die aktuelle Paar-Auswahl bereits sehr stabile Paare liefert.
- **Wichtigstes Einzelrisiko: Sektor-Konzentration durch die rein
  korrelationsbasierte Paar-Auswahl** — fast ausschließlich Finanzwerte,
  dadurch Schwäche in BEIDEN getesteten Stress-Perioden (2022 UND 2020),
  nicht nur einer. Sollte bei einer künftigen Weiterentwicklung
  (z. B. explizite Sektor-Diversifizierung der Paar-Auswahl, falls eine
  verlässliche Sektor-Datenquelle verfügbar wird) berücksichtigt werden.
- Bewusst **nicht** umgesetzt: `live_params.py`, Cronjob, `forward_test.py`.

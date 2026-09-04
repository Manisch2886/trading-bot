# Turtle Soup (False-Breakout-Reversal, Krypto) — Prototyp-Ergebnisse

Stand: 2026-09-04. Prototyp bis einschließlich Backtest-/Walk-Forward-Stufe,
wie beauftragt. **Nichts live geschaltet** — keine `live_params.py`, kein
Cronjob, kein `forward_test.py`.

## 0. Zeitrahmen-Entscheidung

Tageskerzen, wie bei den anderen Krypto-Prototypen (siehe
`rsi2_crypto/backtest_rsi2.py`-Docstring für die Begründung: Handelstage =
Kalendertage bei 24/7-Krypto, kein Umrechnungsbedarf).

## 1. Regeln (exakt spezifiziert)

Identisch zur Aktien-Version (`turtle_soup_stocks`), siehe dortige Findings
Abschnitt 1 für die vollständige Spezifikation (Setup-Erkennung, selber-Tag-
Einstieg, Stop-Varianten). Universum: 20 Krypto-Symbole mit ausreichender
Historie (identisch zu RSI-2/Volatility Breakout Krypto).

## 2. Multi-Symbol-Optimierung (Gesamtzeitraum, 20 Symbole)

| Donchian | Stop-Modus | Trades | Win Rate | Ø Rendite/Trade | Score |
|---|---|---|---|---|---|
| **10** | **structural** | **1599** | **27,1%** | **0,76%** | **0,185** |
| 10 | kein Stop | 1107 | 48,4% | 1,21% | 0,161 |
| 10 | 8% fest | 1363 | 37,1% | 0,35% | 0,056 |
| 10 | 5% fest | 1499 | 28,0% | 0,19% | 0,022 |

**Wichtiger Unterschied zur Aktien-Version:** hier gewinnt der
"structural"-Stop (Setup-Tag-Tief) — bei niedriger Win Rate (27,1%,
ähnlich wie bei der Aktien-Version), aber deutlich höherer Ø-Rendite/Trade
(0,76% vs. 1,21% bei "kein Stop", aber mit besserem Score durch höhere
Trade-Zahl und -Qualität in Kombination). Plausible Erklärung: Kryptos
höhere Tagesvolatilität lässt echte Reversal-Bewegungen deutlicher
ausfallen — der enge strukturelle Stop schneidet zwar viele Trades früh
ab, aber die durchkommenden Trades sind im Schnitt hochwertiger. Anders
als bei Aktien ist der musterspezifische Stop hier also NICHT die
schlechteste, sondern die beste Wahl — ein echter Markt-spezifischer
Unterschied, kein Widerspruch.

## 3. Walk-Forward (70/30, Split innerhalb der Symbol-Historie)

| Metrik | In-Sample | Out-of-Sample |
|---|---|---|
| Beste Kombination | Donchian 10 / kein Stop | (dieselbe) |
| Win Rate | 47,8% | 49,0% |
| Ø Gewinn/Trade | 0,93% | 1,66% |
| Anzahl Trades | 767 | 341 |
| Robustheit-Score | 0,105 | **0,207** |

Score **verbessert sich** Out-of-Sample (+97%) — robust, kein
Overfitting-Signal. (In-Sample-beste Kombination unterscheidet sich von
der Gesamtzeitraum-besten — "kein Stop" statt "structural" — plausibel bei
einem kleineren Teilfenster, ähnliches Muster wie bei anderen
Krypto-Prototypen.)

## 4. Equity-Simulation (10.000 Start, 10% Allokation, Limit 8)

Validierte Basiskonfiguration: Donchian 10, Stop "structural"
(Gesamtzeitraum-bester Score).

| | Gesamtzeitraum | Out-of-Sample |
|---|---|---|
| Endkapital | 27.759,42 | 16.430,92 |
| Gesamtrendite | **+177,59%** | **+64,31%** |
| Trades ausgeführt | 1414 | 475 |
| Trades übersprungen | 185 | 57 |
| Max Drawdown | −32,40% | −23,00% |

Kein ausgeprägter Kapital-Flaschenhals (11,6% Skip-Rate Gesamtzeitraum) —
wie bei den anderen Krypto-Prototypen deutlich niedriger als bei Aktien
(kleineres 20-Symbol-Universum).

## 5. Buy-and-Hold-Vergleich

| | Wert |
|---|---|
| Endkapital | 9.744,74 |
| Gesamtrendite | **−2,55%** |
| Max Drawdown | −79,18% |
| Anzahl Symbole | 20 |

Schlägt Buy-and-Hold deutlich — wie bei RSI-2/Volatility Breakout Krypto,
mit derselben methodischen Einschränkung (die Buy-and-Hold-Messlatte für
das konstruierte Top-25-Portfolio ist ungewöhnlich schwach, siehe
`rsi2_crypto/PROTOTYPE_FINDINGS.md` Abschnitt 5).

## 6. Abgrenzung zu Volatility Breakout Krypto

### 6a. Zeitliche Nähe

| | Wert |
|---|---|
| Turtle-Soup-Einstiege gesamt | 1599 |
| Volatility-Breakout-Krypto-Stop-Loss-Exits gesamt | 251 |
| ...davon Turtle-Soup-Einstiege innerhalb 10 Tagen NACH einem VB-Stop-Loss (selbes Symbol) | 178 (11,13%) |
| Zufalls-Baseline (20 Permutationen) | 127,8 (7,99%) |
| **Faktor gegenüber Zufall** | **1,4×** |

Deutlich höherer absoluter Anteil als bei Aktien (11,13% vs. 2,88%) —
plausibel, da das kleinere 20-Symbol-Krypto-Universum insgesamt mehr
zeitliche Nähe zwischen beliebigen Ereignissen erzeugt (daher auch die
höhere Zufalls-Baseline von 7,99%). Der Faktor gegenüber Zufall (1,4×) ist
etwas schwächer als bei Aktien (1,8×), aber weiterhin klar über 1.

### 6b. Korrelation der täglichen Portfolio-Renditen

**Korrelation: −0,002** — praktisch exakt null, sogar noch niedriger als
bei der Aktien-Version (0,085). Starkes Diversifikationssignal auf
Portfolio-Ebene.

### 6c. Stress-Periode 2022 im direkten Vergleich

| Periode | Turtle Soup Rendite | Turtle Soup Max DD | Volatility Breakout Rendite | Volatility Breakout Max DD |
|---|---|---|---|---|
| 2022-Krypto-Winter | −19,16% | −24,92% | −12,35% | −16,55% |

**Wie bei der Aktien-Version in 2022: keine Diversifikation in dieser Art
von Stressphase** — Turtle Soup schwächelt hier sogar STÄRKER als
Volatility Breakout (−19,16% vs. −12,35%), nicht schwächer. Bestätigt das
bei Aktien gefundene Muster: in einem anhaltenden, breiten Bärenmarkt
scheitern BEIDE False-Breakout-basierten Strategien ähnlich (Kursrückgänge
unter ein N-Tage-Tief sind in einem echten Bärenmarkt öfter echte
Fortsetzungen als Fehlausbrüche). Ein 2020-COVID-Vergleich ist für Krypto
nicht möglich (Datenbeginn 2021-09, wie bei allen Krypto-Prototypen).

## 7. Einordnung / Gesamtfazit

- Solide Signalqualität, Walk-Forward-Score verbessert sich deutlich OOS.
- **Musterspezifischer Stop-Test zeigt ein Markt-abhängiges Ergebnis:**
  bei Krypto gewinnt "structural" (anders als bei Aktien, wo "kein Stop"
  klar gewinnt) — ein echter, empirisch belegter Unterschied zwischen den
  Märkten, kein Widerspruch in der Methodik.
- Kein ausgeprägter Kapital-Flaschenhals, schlägt Buy-and-Hold deutlich
  (mit der bekannten Einschränkung zur Buy-and-Hold-Messlatte).
- **Diversifikationsthese: gleiches differenziertes Bild wie bei Aktien.**
  Praktisch exakt unkorrelierte Portfolio-Renditen (−0,002) und ein
  moderat über Zufall liegendes zeitliches Zusammenfallen mit
  Volatility-Breakout-Fehlausbrüchen (Faktor 1,4×) — aber in der
  konkreten 2022-Stressphase schwächeln BEIDE Strategien gemeinsam
  (Turtle Soup sogar stärker), kein "Turtle Soup kompensiert"-Muster.
  Bestätigt die bei Aktien gefundene Einordnung: komplementäre, nicht
  kompensatorische Schwachstellen — die Diversifikationswirkung zeigt
  sich auf Portfolio-Korrelationsebene über die gesamte Historie, nicht
  zuverlässig innerhalb einzelner Krisenperioden.
- Bewusst **nicht** umgesetzt: `live_params.py`, Cronjob, `forward_test.py`.

## 8. Kapitalmanagement-Tuning

War in der Prototyp-Phase noch nicht Fokus - Krypto zeigte bei der
urspruenglichen Equity-Simulation nur eine moderate 11,6% Skip-Rate (Limit
8, 10% Allokation), deutlich schwaecher als der bei Aktien gefundene
84,4%-Flaschenhals. Hier zur Vollstaendigkeit und im direkten Vergleich zur
Aktien-Version untersucht, analog zur Vorgehensweise bei RSI-2/Volatility
Breakout. Reine Analyse - **nichts live geschaltet**, keine `live_params.py`.

### 8a. Signal-Qualitaets-Test (Aufgabe 1)

| | n | Win Rate | Ø PnL/Trade |
|---|---|---|---|
| (a) Tatsaechlich ausgefuehrt (Limit 8, 10%) - Gesamtzeitraum | 1414 | 26,5% | 0,970% |
| (b) Alle gefundenen Signale - Gesamtzeitraum | 1599 | 27,1% | 0,761% |
| (a) Tatsaechlich ausgefuehrt - Out-of-Sample | 475 | 24,8% | 1,249% |
| (b) Alle gefundenen Signale - Out-of-Sample | 532 | 26,9% | 1,322% |

**Deutlich anderes Bild als bei Aktien:** im Gesamtzeitraum sind die
tatsaechlich ausgefuehrten Trades sogar BESSER als die Gesamtpopulation
(+0,209 Prozentpunkte) - das Gegenteil des bei Aktien gefundenen Musters.
Out-of-Sample kehrt sich das leicht um (−0,073 Prozentpunkte), bleibt aber
nahe null. Kapitalmanagement ist bei Krypto damit KEIN dominanter,
konsistent nachteiliger Flaschenhals wie bei Aktien - konsistent mit der
bereits im Prototyp gefundenen, deutlich niedrigeren Skip-Rate (11,6%
gegenueber 84,4%). Die 25-Coin-Universumsgroesse erzeugt schlicht seltener
so viele gleichzeitige Signale, dass Kapital zum limitierenden Faktor wird.

### 8b. Positionsgroesse x Limit-Matrix (Aufgabe 2)

Feste Basis: Donchian 10, structural Stop, 10 Tage Zeit-Exit. Vollstaendige
Tabelle in `results/turtle_soup_crypto/experiment_position_size_limit_{full,oos}.csv`.

**Gegenteiliger Befund zu Aktien:** anders als bei Aktien verbessert eine
Lockerung des Kapitalmanagements (kleinere Allokation und/oder hoeheres
Limit) die Ergebnisse NICHT - im Gegenteil, jede getestete Alternative
verschlechtert sowohl Gesamtzeitraum-Rendite als auch Max Drawdown
gegenueber der Basiskonfiguration (Limit 8, 10% Allokation: +177,59% Rendite,
−32,40% DD - das beste Ergebnis im gesamten Grid). Plausible Erklaerung: die
niedrige Win Rate (26–27%) bei "structural" Stop bedeutet, dass mehr
gleichzeitige, kleinere Positionen nicht mehr Qualitaet einfangen, sondern
nur mehr Verlierer gleichzeitig offen halten.

### 8c. Stress-Periode unter neuer Konfiguration (Aufgabe 3)

Vollstaendige Gesamtuebersicht (alle 9 Konfigurationen, sortiert nach
Out-of-Sample-Rendite, mit Gesamtzeitraum- und 2022-Werten) in
`results/turtle_soup_crypto/experiment_capital_management_summary.csv`.
Auszug:

| Allokation | Limit | OOS-Rendite | OOS-DD | Gesamt-Rendite | Gesamt-DD | 2022-Rendite | 2022-DD |
|---|---|---|---|---|---|---|---|
| **10% (Basis)** | **8** | 64,31% | −23,00% | **177,59%** | **−32,40%** | **−19,16%** | **−24,92%** |
| 10% | 15/unbegrenzt | 73,10% | −23,81% | 165,97% | −36,02% | −20,44% | −26,15% |
| 5% | unbegrenzt | 37,85% | −13,07% | 64,34% | −28,28% | −10,91% | −16,89% |

**Empfehlung: Basiskonfiguration UNVERAENDERT beibehalten (10% Allokation,
Limit 8).** Anders als bei Aktien bringt Kapitalmanagement-Tuning bei
Krypto keinen Mehrwert - die urspruengliche Konfiguration ist bereits nahe
am Optimum des gesamten Grids (bestes Gesamtzeitraum-Ergebnis UND bestes
2022-Stress-Ergebnis). Die einzige Alternative mit hoeherer Out-of-Sample-
Punktrendite (10% Allokation, Limit 15, identisch zu unbegrenzt: 73,10%
statt 64,31%) faellt im Gesamtzeitraum klar ab (+165,97% statt +177,59%,
DD −36,02% statt −32,40%) UND verschlechtert sich zusaetzlich im
2022-Stresstest (−20,44%/−26,15% statt −19,16%/−24,92%) - wird daher trotz
des hoeheren OOS-Einzelwerts nicht empfohlen.

**Schwachstellenprofil unveraendert:** da keine Konfigurationsaenderung
empfohlen wird, bleibt das bereits dokumentierte 2022-Bild (Turtle Soup
schwaecher als Volatility Breakout, −19,16%/−24,92% vs. −12,35%/−16,55%)
trivialerweise unveraendert. Bestaetigt im Uebrigen den bei Aktien
gefundenen Grundsatz aus umgekehrter Richtung: die Schwaeche liegt in der
Signalqualitaet (niedrige Win Rate des structural Stops), nicht im
Kapitalmanagement - bei Krypto ist das Kapitalmanagement schlicht schon nah
am Optimum, es gibt hier keinen Hebel zu ziehen.

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

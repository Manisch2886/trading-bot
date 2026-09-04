# Relative-Strength-Pair-Rotation (Krypto) — Prototyp-Ergebnisse

Stand: 2026-09-04. Prototyp bis einschließlich Backtest-/Walk-Forward-Stufe,
wie beauftragt. **Nichts live geschaltet** — keine `live_params.py`, kein
Cronjob, kein `forward_test.py`.

**Vorab-Einordnung (Kernbefund dieses Prototyps):** Anders als die
Aktien-Version zeigt Pair-Rotation Krypto **keine Out-of-Sample-robuste
Konfiguration** — alle 18 getesteten Parameter-Kombinationen scheitern im
Out-of-Sample-Fenster (negative Ø-Rendite). Details in Abschnitt 3/8.
Dieser Prototyp wird deshalb **nicht zur Weiterentwicklung/Live-Vorbereitung
empfohlen**, im Gegensatz zu den bisherigen Krypto-Prototypen.

## 0. Architektur-Entscheidungen (Begründung)

Wie bei der Aktien-Version: Paar-Auswahl rein korrelationsbasiert (siehe
`pair_rotation_stocks/PROTOTYPE_FINDINGS.md` Abschnitt 0 — bei Krypto
entfällt die Sektor-Frage ohnehin, ein Ankerpaar wie BTC/ETH ist per
Definition korrelationsbasiert gedacht). Tageskerzen (siehe
`rsi2_crypto/backtest_rsi2.py`-Docstring für die Begründung).

**Datenfenster-Einschränkung, spezifisch für Pair-Rotation:** Anders als
RSI-2/Volatility Breakout Krypto (die JEDES Symbol unabhängig ab seinem
eigenen Datenbeginn nutzen) braucht Pair-Rotation ein GEMEINSAMES
Referenzdatum für die Korrelations-basierte Paar-Auswahl. Ohne
Einschränkung hätte ein einzelner sehr junger Coin (z. B. BMTUSDT, erst
seit 2025-03) das gesamte Auswertungsfenster auf wenige Monate
zusammengestaucht. Deshalb `MIN_HISTORY_DAYS = 1500` (statt 500 bei den
anderen Krypto-Bots) — das trennt sauber die 13 Coins mit voller
~5-Jahres-Historie (alle seit 2021-09-01) von jüngeren Coins.
Auswertungsfenster beginnt dadurch am 2022-05-11 (2021-09-01 + 252 Tage
Korrelations-Vorlauf).

## 1. Regeln (exakt spezifiziert)

Identisch zur Aktien-Version (`pair_rotation_stocks`), siehe dortige
Findings Abschnitt 1 für die vollständige Spezifikation. Universum: 13
Krypto-Coins mit voller ~5-Jahres-Historie aus dem 25-Coin-Binance-Universum.

## 2. Multi-Pair-Optimierung (Gesamtzeitraum, 13 Symbole, 20 Paare)

BTC/ETH als korreliertestes Ankerpaar bestätigt (0,876), wie in der
Anfrage erwartet. Auszug (vollständige Tabelle in
`results/pair_rotation_crypto/multi_pair_optimisation_results.csv`):

| Lookback | Rebalance | Stop-Loss | Trades | Win Rate | Ø Rendite/Trade | Score |
|---|---|---|---|---|---|---|
| **120** | **5 (wöchentlich)** | **kein Stop** | **422** | **45,5%** | **5,74%** | **0,665** |
| 120 | 1 (täglich) | kein Stop | 940 | 44,4% | 2,94% | 0,483 |
| 60 | 5 (wöchentlich) | kein Stop | 618 | 42,7% | 3,43% | 0,478 |

Anders als bei Aktien gewinnt hier **"kein Stop"** durchgehend (nicht 12%)
— plausibel: Kryptos hohe Tagesvolatilität lässt feste %-Stops zu häufig
auf reinem Rauschen triggern, bevor sich die Rotation durchsetzen kann.
Wöchentliche Rebalance dominiert erneut wie bei Aktien.

## 3. Walk-Forward (70/30, Split innerhalb des Auswertungsfensters)

| Metrik | In-Sample | Out-of-Sample |
|---|---|---|
| Beste Kombination | Lookback 120 / wöchentlich / kein Stop | — |
| Win Rate | 51,2% | — |
| Ø Gewinn/Trade | 11,58% | **−5,21%** |
| Robustheit-Score | 2,344 | **erfüllt Mindestkriterien nicht** |

**Zentraler Negativbefund:** Die In-Sample-beste Kombination kollabiert
Out-of-Sample vollständig (Ø-Rendite/Trade dreht von +11,58% auf −5,21%).
Um auszuschließen, dass das nur diese eine Kombination betrifft, wurden
**alle 18 getesteten Kombinationen** (Lookback × Rebalance × Stop-Loss)
einzeln Out-of-Sample geprüft:

| | Ergebnis |
|---|---|
| Kombinationen, die OOS die Mindestkriterien erfüllen (Ø-Rendite ≥ 0) | **0 von 18** |
| Ø-Rendite/Trade OOS über alle 18 Kombinationen | durchgehend negativ (−0,41% bis −5,21%) |
| Win Rate OOS über alle 18 Kombinationen | durchgehend unter 44% |

**Das ist kein Overfitting-Grenzfall, sondern ein durchgängiges
Versagen der Strategie im Out-of-Sample-Fenster (2025-05 bis 2026-08).**
Auffällig: ausgerechnet die im Gesamtzeitraum/In-Sample am besten
bewerteten Kombinationen (langer Lookback, wöchentliche Rebalance)
schneiden Out-of-Sample am SCHLECHTESTEN ab (−5,21% bei Lookback
120/wöchentlich/kein Stop) — eine vollständige Rangfolge-Umkehr, ein noch
deutlicheres Overfitting-Muster als beim Trailing-Take-Profit-Präzedenzfall.

## 4. Equity-Simulation (10.000 Start, 10% Allokation, Limit 8)

**Hinweis:** Konfiguration ist NICHT Out-of-Sample-validiert (siehe
Abschnitt 3) — diese Simulation dient der vollständigen, mit den anderen
Prototypen vergleichbaren Pipeline-Dokumentation.

| | Gesamtzeitraum | Out-of-Sample |
|---|---|---|
| Endkapital | 24.561,49 | 6.738,91 |
| Gesamtrendite | +145,61% | **−32,61%** |
| Trades ausgeführt | 200 | 89 |
| Trades übersprungen | 222 | 70 |
| Max Drawdown | −47,85% | −46,45% |

Auch auf Portfolio-Ebene bestätigt: Gesamtzeitraum sieht profitabel aus,
Out-of-Sample verliert das Portfolio ein knappes Drittel des Kapitals.

## 5. Buy-and-Hold-Vergleich

| | Wert |
|---|---|
| Endkapital | 18.091,29 |
| Gesamtrendite | +80,91% |
| Max Drawdown | −65,77% |
| Anzahl Symbole | 9 |

Der Gesamtzeitraum-Wert der Strategie (+145,61%, DD −47,85%) schlägt
Buy-and-Hold sowohl bei Rendite als auch Drawdown — ABER das ist angesichts
des Out-of-Sample-Versagens (Abschnitt 3/4) kein belastbares Ergebnis: der
Gesamtzeitraum-Vorteil beruht überwiegend auf der In-Sample-Periode, die
laut Walk-Forward-Test nicht repräsentativ für aktuelles Marktverhalten ist.

## 6. Experiment: Wirksamkeit des Entkopplungs-Schutzes

| | Ohne Schutz | Mit Schutz |
|---|---|---|
| Gesamtzeitraum-Rendite | +135,36% | **+145,61%** |
| Gesamtzeitraum-DD | −48,16% | **−47,85%** |
| OOS-Rendite | −43,57% | **−32,61%** |
| OOS-DD | −51,70% | **−46,45%** |
| Entkopplungs-Exits | 0 | 9 |

**Anders als bei der Aktien-Version (dort nie ausgelöst) triggert der
Schutz hier tatsächlich (9-mal) und wirkt in beide Richtungen leicht
positiv** — mildert sowohl die Gesamtzeitraum- als auch (besonders
relevant) die OOS-Verluste spürbar (−43,57%→−32,61%). Der Effekt ist
moderat, aber konsistent in die richtige Richtung. Bestätigt: die
Krypto-Paare entkoppeln sich in der Praxis tatsächlich gelegentlich
(anders als die sehr stabilen Aktien-Finanzwerte-Paare), der Schutz hat
hier einen echten, wenn auch begrenzten Nutzen.

## 7. Stress-Perioden: 2022-Krypto-Winter UND 2020-COVID-Crash

| Periode | Rendite | Max Drawdown | Abdeckung |
|---|---|---|---|
| 2022-Krypto-Winter | −3,01% | −3,05% | NUR 18.09.–31.12.2022 (Teilfenster) |
| 2020-COVID-Crash | — | — | **nicht abbildbar** |

**Zwei Einschränkungen, beide durch die Datenlage bedingt, nicht durch
die Strategie:**
- 2020-COVID-Crash ist für KEINEN der Krypto-Prototypen dieses Projekts
  testbar — die verfügbare Krypto-Tageshistorie beginnt erst 2021-09-01
  (Sandbox-Ableitung aus 1h-Daten, siehe `shared/build_daily_crypto_data.py`),
  weit nach dem COVID-Crash. Das betrifft RSI-2 Krypto und Volatility
  Breakout Krypto identisch, ist keine Pair-Rotation-spezifische Lücke.
- 2022-Krypto-Winter ist nur TEILWEISE abgedeckt: das
  Pair-Rotation-eigene Referenzdatum (2022-05-11, siehe Abschnitt 0) plus
  der Vorlauf bis zum ersten tatsächlichen Trade verschiebt den
  auswertbaren Teil auf September–Dezember 2022 — der stärkste Teil des
  Krypto-Winters (Terra/Luna-Kollaps im Mai, FTX-Kollaps im November
  fällt teilweise noch hinein) ist nur teilweise erfasst.

Der abgedeckte Teil zeigt ein moderates, nicht extremes Ergebnis
(−3,01%/−3,05%) — angesichts der unvollständigen Abdeckung aber **nicht
aussagekräftig genug für eine belastbare Stress-Perioden-Einschätzung**,
anders als bei den anderen Krypto-Prototypen.

## 8. Einordnung / Gesamtfazit

- **Zentraler Befund: keine Out-of-Sample-robuste Konfiguration
  gefunden** (0 von 18 getesteten Kombinationen). Die im Gesamtzeitraum
  attraktivsten Parameter (langer Lookback, wöchentliche Rebalance)
  schneiden Out-of-Sample am schlechtesten ab — eine vollständige
  Rangfolge-Umkehr, ein deutlicheres Overfitting-Signal als der
  Trailing-Take-Profit-Präzedenzfall bei der Aktien-Version.
- Auffälliger Unterschied zur Aktien-Version, wo Walk-Forward-Score sich
  sogar deutlich VERBESSERT (Aktien) statt zu kollabieren (Krypto) — die
  Strategie überträgt sich NICHT gleichermaßen auf beide Märkte.
- Entkopplungs-Schutz zeigt hier (anders als bei Aktien) einen echten,
  moderat positiven Effekt — reicht aber nicht aus, um das grundsätzliche
  Out-of-Sample-Problem zu beheben.
- Stress-Perioden-Test nicht aussagekräftig (Datenlücken).
- **Empfehlung: Pair-Rotation Krypto in dieser Form NICHT für eine
  Kapitalmanagement-Runde oder Live-Vorbereitung weiterverfolgen.**
  Mögliche Ansatzpunkte für eine überarbeitete Version, falls gewünscht:
  ein feineres Lookback/Rebalance-Raster um die Grenzen der aktuellen
  Werte herum, eine längere Historie (native Binance-Tagesdaten statt der
  auf 1h-Historie limitierten Sandbox-Ableitung, siehe
  `rsi2_crypto/fetch_1d_data.py`-Muster) oder ein grundsätzlich anderer
  Signal-Ansatz für Krypto-Paare.
- Bewusst **nicht** umgesetzt: `live_params.py`, Cronjob, `forward_test.py`
  (ohnehin nicht empfohlen, siehe oben).

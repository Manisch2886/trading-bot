# Volatility Breakout Krypto — Prototyp-Ergebnisse

Stand: 2026-09-03. Kompletter neuer Prototyp-Prozess wie ursprünglich bei
den Aktien-Versionen — bis einschließlich Backtest-/Walk-Forward-Stufe.
**Nichts live geschaltet** — keine `live_params.py`, kein Cronjob, kein
`forward_test.py`.

## 0. Zeitrahmen-Entscheidung (Begründung)

Wie bei RSI-2 Krypto (siehe dortige Findings Abschnitt 0) wurde bewusst
**TAGESKERZEN** statt 1h/4h gewählt:

- Der Squeeze-Lookback (126 Tage, ca. 6 Handelsmonate) und der Zeit-Exit
  (15 Tage) sind in der Aktien-Version in "Tagen" definiert und validiert.
  Bei Tageskerzen überträgt sich diese Einheit 1:1 auf Krypto — bei 1h/4h
  müsste "126 Tage" erst in eine Kerzenzahl umgerechnet werden (z. B.
  126×24 Stunden bei 1h), was faktisch einen neuen, ungeprüften Parameter
  einführen würde, statt die validierte Logik zu übertragen.
- Krypto handelt 24/7 — bei Tageskerzen fallen "Handelstage" und
  Kalendertage zusammen (jeder Tag hat eine Kerze), das befürchtete
  Umrechnungsproblem entfällt bei dieser Wahl von selbst.
- Ein fraktales Argument FÜR eine Übertragung auf kürzere Zeitrahmen wäre
  denkbar (Squeeze-dann-Ausbruch ist ein Muster, das auf mehreren
  Zeitebenen auftritt) — wurde hier aber bewusst NICHT verfolgt: das hätte
  zwei zusätzliche, unvalidierte Freiheitsgrade eingeführt (Zeitrahmen-Wahl
  UND Parameter-Umrechnung), ohne dass dafür ein triftiger Grund vorlag.
  Die konservativere, high-fidelity Übertragung (gleiche Einheiten,
  gleicher Zeitrahmen wie die validierte Aktien-Version) war hier
  vorzuziehen.
- Datenbasis: siehe RSI-2-Krypto-Findings Abschnitt 0 (aus 1h-Historie
  abgeleitete Tageskerzen, Sandbox-Workaround wegen blockiertem
  Binance-API-Zugriff).

Squeeze-Lookback (126) und -Perzentil (25) bleiben wie bei der
Aktien-Version FEST (nicht neu optimiert) — nur der Stop-Loss wird
getestet, identisch zum Vorgehen bei der Aktien-Version.

## 1. Regeln (exakt spezifiziert)

Identisch zur Aktien-Version (`volatility_breakout`):

1. **Squeeze-Erkennung:** Bollinger-Band-Breite im unteren 25%-Perzentil
   der letzten 126 Tage.
2. **Einstiegs-Trigger:** Squeeze am Vortag UND Schlusskurs heute über dem
   oberen Band. Kein Pyramiding.
3. **Ausstieg — Priorität:** a) Stop-Loss (getestet: 3%, 5%, 8%, kein Stop)
   b) Zeit-Exit nach 15 Tagen. Kein Trailing-Element (siehe Aktien-Version:
   dort als Overfitting identifiziert, hier nicht erneut ungeprüft
   übernommen).

Universum: 20 Krypto-Symbole mit ausreichender Historie (identisch zu
RSI-2 Krypto, siehe dortige Findings).

## 2. Multi-Symbol-Optimierung (Gesamtzeitraum, 20 Symbole)

| Stop-Loss | Trades | Win Rate | Ø Rendite/Trade | Ø Haltedauer | Score |
|---|---|---|---|---|---|
| **5%** | **359** | **26,5%** | **1,75%** | **7,6 Tage** | **0,314** |
| 8% | 342 | 33,6% | 1,56% | 10,0 Tage | 0,248 |
| 3% | 379 | 18,2% | 1,06% | 5,3 Tage | 0,144 |
| kein Stop | 329 | 44,1% | 1,19% | 15,0 Tage | 0,115 |

Anders als bei der Aktien-Version (dort 8% Stop optimal) ist hier **5%
Stop-Loss** die robusteste Kombination. Auffällig: die Win Rate ist mit
26,5% deutlich niedriger als bei der Aktien-Version (53,9%), aber die
Ø-Rendite pro Trade deutlich höher (1,75% vs. 0,70%) — Krypto-Breakouts
scheitern häufiger, laufen aber bei Erfolg deutlich weiter (höhere
Volatilität in beide Richtungen, konsistent mit Krypto allgemein).

## 3. Walk-Forward (70/30, Split innerhalb der Symbol-Historie)

| Metrik | In-Sample | Out-of-Sample |
|---|---|---|
| Beste Kombination | 5% Stop | (dieselbe) |
| Win Rate | 24,4% | 29,9% |
| Ø Gewinn/Trade | 2,20% | 1,01% |
| Anzahl Trades | 225 | 134 |
| Robustheit-Score | 0,395 | **0,175** |

**Score fällt Out-of-Sample um 56%** — anders als bei RSI-2 Krypto (Score
verbessert sich dort OOS) und auch anders als bei der Aktien-Version des
Bots (Score verbessert sich dort ebenfalls OOS). Wichtig für die
Einordnung: Win Rate steigt sogar leicht (24,4%→29,9%), Ø-Gewinn/Trade
bleibt deutlich positiv (1,01%) — kein Kollaps wie im klassischen
Overfitting-Muster (siehe Trailing-Stop-Präzedenzfall bei der
Aktien-Version), aber ein spürbarer Rückgang der score-treibenden
Trade-Anzahl/Risiko-Relation. Sollte bei einer künftigen
Live-Entscheidung als moderates Warnsignal (nicht als Ausschlusskriterium)
gewertet werden.

## 4. Equity-Simulation (10.000 Start, 10% Allokation, Limit 8)

Validierte Basiskonfiguration: 5% Stop-Loss (Gesamtzeitraum-bester Score).

| | Gesamtzeitraum | Out-of-Sample |
|---|---|---|
| Endkapital | 17.126,14 | 11.632,27 |
| Gesamtrendite | **+71,26%** | **+16,32%** |
| Trades ausgeführt | 310 | 109 |
| Trades übersprungen | 49 | 25 |
| Max Drawdown | −16,77% | −11,33% |

Skip-Rate: 13,6% Gesamtzeitraum, 18,7% OOS — wie bei RSI-2 Krypto kein
ausgeprägter Kapital-Flaschenhals (kleineres Universum als bei den
Aktien-Bots).

## 5. Buy-and-Hold-Vergleich

| | Wert |
|---|---|
| Endkapital | 9.744,74 |
| Gesamtrendite | **−2,55%** |
| Max Drawdown | −79,18% |
| Anzahl Symbole | 20 |

**Volatility Breakout Krypto schlägt Buy-and-Hold deutlich** (+71,26%/
+16,32% vs. −2,55%) — wie bei RSI-2 Krypto ein anderes Bild als bei der
Aktien-Version. Dieselbe Einschränkung wie in den RSI-2-Krypto-Findings
(Abschnitt 5) gilt auch hier: die Buy-and-Hold-Messlatte für dieses
konstruierte Top-25-Portfolio ist ungewöhnlich niedrig (−79% Max
Drawdown), der Vergleich sollte nicht überinterpretiert werden.

## 6. Experiment: BTC-Regime-Filter (auf ausdrückliche Anfrage geprüft)

Besonders relevant, da die Aktien-Version genau in Bärenmarktphasen ihre
größte Schwäche zeigte (siehe Abschnitt 7 unten und
`results/volatility_breakout/PROTOTYPE_FINDINGS.md` Abschnitt 10):

| | Ohne Filter (Gesamt) | Mit Filter (Gesamt) | Ohne Filter (OOS) | Mit Filter (OOS) |
|---|---|---|---|---|
| Trades | 359 | 233 | 134 | 83 |
| Win Rate | 26,5% | 25,3% | 29,9% | 28,9% |
| Ø PnL/Trade | 1,75% | 2,67% | 1,01% | 1,81% |
| Portfolio-Rendite | +71,26% | +49,03% | +16,32% | +19,15% |
| Max Drawdown | −16,77% | −16,29% | −11,33% | −7,76% |

**Uneindeutiges Ergebnis, anders als bei RSI-2 Krypto (dort klar
negativ):** Der Filter verschlechtert die Gesamtzeitraum-Rendite deutlich
(71,26%→49,03%), verbessert aber die Out-of-Sample-Rendite (16,32%→19,15%)
bei gleichzeitig niedrigerem Drawdown (−11,33%→−7,76%) — und die
Ø-Rendite/Trade steigt in BEIDEN Zeiträumen spürbar (weniger, aber
qualitativ bessere Trades). Nach der im Projekt etablierten Skepsis-Regel
("Out-of-Sample ist entscheidend, nicht der Gesamtzeitraum") wäre das ein
leicht positives Signal — aber der Gesamtzeitraum-Rückgang ist zu deutlich,
um eine klare Empfehlung auszusprechen.

**Empfehlung: kein klares Ergebnis — weder eindeutig empfohlen noch klar
verworfen.** Anders als beim BTC-Regime-Filter für RSI-2 Krypto (dort
eindeutig negativ) verdient dieser Fall bei einer künftigen
Kapitalmanagement-Runde eine gezieltere Nachprüfung (z. B. mit mehr
OOS-Daten oder einem gröberen/feineren BTC-Trendfilter), bevor eine
Entscheidung getroffen wird.

## 7. Stress-Periode 2022 ("Krypto-Winter") — wiederholt sich die Bärenmarkt-Schwäche?

Leitfrage aus der Anfrage: zeigt sich das bei der Aktien-Version gefundene
Muster (2022-Drawdown ≈ Allzeit-Maximum, schwächster Bot in der
Vergleichsgruppe) auch im Krypto-Bärenmarkt 2022?

| Bot | Rendite 2022 | Max DD 2022 | Allzeit-Max-DD |
|---|---|---|---|
| Elliott Wave (Krypto, live) | +21,20% | −0,23% | −0,23% |
| T3/SuperTrend (Krypto, live) | −3,28% | −12,28% | −22,20% |
| RSI-2 Mean-Reversion (Krypto, Prototyp) | −8,65% | −8,65% | −13,11% |
| **Volatility Breakout (Krypto, Prototyp)** | **−12,35%** | **−16,55%** | **−16,77%** |

Gleichgewichtete hypothetische 4-Krypto-Bot-Kombination in 2022: **−3,03%
Rendite, −6,29% Max Drawdown** (nur Beobachtung, keine echte
Kapitalallokation).

**Antwort: Das Muster wiederholt sich weitgehend.** Volatility Breakout
Krypto ist 2022 (Datenbasis ab 18.03.2022, erster Trade) erneut das
schwächste der vier Bots — sowohl bei der Rendite (−12,35%, schlechter als
alle anderen) als auch beim Drawdown (−16,55%, fast identisch zum
Allzeit-Maximum von −16,77%, wenn auch nicht exakt gleich wie bei der
Aktien-Version). Dieselbe strukturelle Erklärung wie bei der Aktien-Version
liegt nahe: in einem anhaltenden Abwärtsmarkt (Krypto-Winter 2022 durch
Fed-Zinserhöhungen UND krypto-eigene Ereignisse wie den Terra/Luna- und
FTX-Kollaps) lösen Bollinger-Band-Squeezes wiederholt Fehlausbrüche nach
oben aus, bevor der Kurs dem übergeordneten Abwärtstrend weiter folgt.

**Das ist ein wichtiger, eigenständiger Beleg:** die Bärenmarkt-Schwäche
von Volatility Breakout ist damit NICHT nur ein Artefakt des
US-Aktienmarkts 2022, sondern zeigt sich in einem strukturell anderen
Markt (Krypto, andere Ursachen für den Abschwung) auf dieselbe Weise —
ein Hinweis auf eine **strategie-inhärente Eigenschaft**
(Squeeze-Breakout-Logik reagiert grundsätzlich empfindlich auf anhaltende
Trendmärkte nach unten), nicht auf eine zufällige Einzelperiode.

## 8. Einordnung / offene Punkte

- Solide Signalqualität trotz niedriger Win Rate (hohe Ø-Rendite/Trade
  kompensiert) — Walk-Forward zeigt aber einen spürbaren (wenn auch nicht
  katastrophalen) Score-Rückgang OOS, anders als bei RSI-2 Krypto.
- **Kein Kapital-Flaschenhals** wie bei den Aktien-Prototypen.
- **Schlägt Buy-and-Hold deutlich** — mit derselben Einschränkung wie bei
  RSI-2 Krypto zur konstruierten Buy-and-Hold-Messlatte.
- BTC-Regime-Filter: uneindeutiges Ergebnis, keine klare Empfehlung.
- **2022-Stress-Test bestätigt die Bärenmarkt-Schwäche als
  strategie-inhärent, nicht marktspezifisch** — wiederholt sich in einem
  strukturell anderen Markt (Krypto statt Aktien) auf ähnliche Weise. Das
  ist die wichtigste Einzelerkenntnis dieses Prototyps und sollte bei einer
  künftigen Live-Entscheidung für BEIDE Volatility-Breakout-Varianten
  (Aktien UND Krypto) explizit berücksichtigt werden.
- Bewusst **nicht** umgesetzt: `live_params.py`, Cronjob, `forward_test.py`.

# Volatility Breakout (Bollinger-Band-Squeeze) — Prototyp-Ergebnisse (fünfter Bot)

Stand: 2026-09-03. Prototyp bis einschließlich Backtest/Walk-Forward-Stufe,
wie beauftragt. **Nichts live geschaltet** — keine `live_params.py`, kein
Cronjob, kein `forward_test.py`.

---

## 1. Regeln (exakt spezifiziert)

Vollständige, verbindliche Spezifikation in `backtest_breakout.py` (Modul-Docstring).
Kurzfassung:

1. **Squeeze-Erkennung:** Bollinger-Band-Breite (`(oberes − unteres Band) / mittleres Band`,
   Bänder = SMA(20) ± 2·Std) liegt am Vortag (t−1) im unteren 25%-Perzentil der
   letzten 126 Handelstage ("Squeeze"). Kein Blick in die Zukunft: das
   Squeeze-Flag wird auf t−1 geprüft, der Ausbruch erst auf t.
2. **Einstiegs-Trigger:** War der Vortag im Squeeze UND Schlusskurs am
   aktuellen Tag > oberes Band → Einstieg zum Schlusskurs desselben Tages.
   Kein Pyramiding (max. eine offene Position pro Symbol).
3. **Ausstieg — Priorität pro Tag:**
   a) Stop-Loss — Tagestief ≤ Stop-Kurs (getestet: 3%, 5%, 8%, kein Stop)
   b) Zeit-Exit — spätestens nach 15 Handelstagen, zum Schlusskurs
   Kein SMA-Exit (anders als bei RSI-2 — Breakout-Strategien haben kein
   natürliches Mean-Reversion-Ziel). Trailing-Stop ist **nicht** Teil der
   Basis-Regel, sondern separat getestet (Abschnitt 6).
4. **False-Breakout-Filter (optional, testbar):** Ausbruchstag-Volumen ≥ 1,5×
   20-Tage-Durchschnittsvolumen. Standardmäßig AUS — nur aktiv im expliziten
   Vergleichstest (Abschnitt 5).

## 2. Multi-Symbol-Optimierung (Gesamtzeitraum, 147 Symbole, 10-Jahres-Fenster)

| Stop-Loss | Trades | Win Rate | Ø Rendite/Trade | Ø Haltedauer | Score |
|---|---|---|---|---|---|
| **8%** | 4510 | 53,9% | 0,70% | 20,0 Tage | **0,406** |
| 5% | 4603 | 49,5% | 0,62% | 17,7 Tage | 0,372 |
| kein Stop | 4495 | 55,0% | 0,72% | 21,7 Tage | 0,342 |
| 3% | 4821 | 40,4% | 0,51% | 14,3 Tage | 0,192 |

Ein zu enger Stop (3%) schadet der Breakout-Strategie deutlich (Win Rate
fällt auf 40,4% — enge Stops fangen normale Nachbeben nach dem Ausbruch ab,
bevor sich die Bewegung entfalten kann). **8% Stop-Loss** ist die robusteste
Kombination und wird als Basiswert für alle folgenden Schritte übernommen.

## 3. Walk-Forward (70/30, Split innerhalb des 10-Jahres-Fensters, 2023-09-01)

| Metrik | In-Sample | Out-of-Sample |
|---|---|---|
| Win Rate | 53,6% | 54,6% |
| Ø Gewinn/Trade | 0,54% | 1,09% |
| Anzahl Trades | 3180 | 1334 |
| Robustheit-Score | 0,249 | **0,422** |

Score **verbessert sich** Out-of-Sample statt einzubrechen — starkes
Robustheitssignal, kein Hinweis auf Overfitting bei der Stop-Loss-Wahl.

## 4. Equity-Simulation (10.000 Start, 10% Allokation, Limit 8)

| | Gesamtzeitraum | Out-of-Sample |
|---|---|---|
| Endkapital | 24.205,85 | 17.454,46 |
| Gesamtrendite | **+142,06%** | **+74,54%** |
| Trades ausgeführt | 1236 | 385 |
| Trades übersprungen | 3274 | 949 |
| Max Drawdown | −22,39% | −10,53% |

### Zentraler Befund: noch stärkerer Skip-Rate-Effekt als bei RSI-2

**73% der Signale werden übersprungen** (Gesamtzeitraum, 3274 von 4510) —
noch deutlicher als RSI-2s 65%. Dieselbe Kapital-Flaschenhals-Dynamik wie
bei RSI-2: bei Limit 8 / 10% Allokation ist praktisch immer das gesamte
Kapital gebunden, sobald das System aktiv Signale liefert. Bestätigt erneut,
dass dies ein systemisches Muster für signalreiche Breitmarkt-Strategien
unter der gemeinsamen Limit-8/10%-Startkonvention ist, nicht ein Artefakt
einer einzelnen Strategie.

## 5. Buy-and-Hold-Vergleich

| | Wert |
|---|---|
| Endkapital | 87.623,97 |
| Gesamtrendite | **+776,24%** |
| Max Drawdown | −34,83% |
| Anzahl Aktien | 150 |

**Weder Gesamtzeitraum (+142,06%) noch Out-of-Sample (+74,54%) schlagen
Buy-and-Hold (+776,24%)** — identisches Bild wie bei RSI-2. Der
Kapital-Flaschenhals (Abschnitt 4) ist auch hier der dominante Faktor: die
Signalqualität selbst (Win Rate ~54%, Score verbessert sich sogar OOS) ist
nicht das Problem.

## 6. Nachfrage: False-Breakout-Filter (Volumen-Bestätigung)

Vergleich Basis-Regel (kein Filter) gegen Volumen-Filter (Ausbruchstag-Volumen
≥ 1,5× 20-Tage-Durchschnitt):

| | Ohne Filter (Gesamt) | Mit Filter (Gesamt) | Ohne Filter (OOS) | Mit Filter (OOS) |
|---|---|---|---|---|
| Trades | 4510 | 1645 | 1334 | 483 |
| Win Rate | 53,9% | 53,5% | 54,6% | 55,3% |
| Ø PnL/Trade | 0,70% | 0,70% | 1,09% | 1,27% |
| Portfolio-Rendite | +142,06% | +116,96% | +74,54% | +42,78% |
| Max Drawdown | −22,39% | −10,19% | −10,53% | −8,83% |

Win-Rate-Differenz: **Gesamtzeitraum −0,4pp, OOS +0,7pp** — keine spürbare
Verbesserung, im Rauschbereich. Der Filter reduziert die Trade-Anzahl massiv
(−63% Gesamtzeitraum), was zwar die Drawdowns senkt, aber wegen des ohnehin
schon starken Kapital-Flaschenhalses (Abschnitt 4) die Portfolio-Rendite
deutlich verschlechtert (142,06%→116,96% Gesamtzeitraum, 74,54%→42,78% OOS).

**Empfehlung: Volumen-Filter NICHT als Standard übernehmen** — das
angefragte Kriterium ("nur wenn er die Win Rate spürbar verbessert") ist
nicht erfüllt.

## 7. Nachfrage: Trailing-Stop (bewusst skeptisch getestet)

Wie beim Aktien-Elliott-Wave-Bot (Trailing-Take-Profit, dort als Overfitting
identifiziert) wurde der Trailing-Stop mit identischer Skepsis geprüft:
Gesamtzeitraum UND Out-of-Sample getrennt, Rangfolge-Stabilität explizit
verglichen. Der Stop wandert mit dem Kurshoch seit Einstieg nach oben (fester
Abstand darunter), bleibt aber nie unter dem festen 8%-Stop.

**Gesamtzeitraum:**

| Variante | Endkapital | Rendite | Max DD |
|---|---|---|---|
| Baseline (fest 8%, kein Trailing) | 24.205,85 | +142,06% | −22,39% |
| Trailing 8% | 23.224,77 | +132,25% | −18,38% |
| **Trailing 12%** | **26.365,44** | **+163,65%** | −21,70% |
| Trailing 15% | 23.331,35 | +133,31% | −22,24% |

**Out-of-Sample:**

| Variante | Endkapital | Rendite | Max DD |
|---|---|---|---|
| **Baseline (fest 8%, kein Trailing)** | **17.454,46** | **+74,54%** | −10,53% |
| Trailing 8% | 16.086,40 | +60,86% | −10,88% |
| Trailing 12% | 16.474,77 | +64,75% | −15,59% |
| Trailing 15% | 16.917,71 | +69,18% | −12,00% |

**Rangfolge-Stabilität (Overfitting-Check):**
- Gesamtzeitraum-Rangfolge (beste zuerst): Trailing 12% → Baseline → Trailing 15% → Trailing 8%
- Out-of-Sample-Rangfolge (beste zuerst): Baseline → Trailing 15% → Trailing 12% → Trailing 8%
- **Beste Variante identisch: Nein**

Trailing 12% sieht im Gesamtzeitraum am stärksten aus (+163,65% vs. +142,06%
Baseline), fällt aber Out-of-Sample auf Platz 3 zurück (+64,75% vs. +74,54%
Baseline). **Exakt dasselbe Overfitting-Muster wie beim Trailing-Take-Profit
des Aktien-Elliott-Wave-Bots** — ein im Gesamtzeitraum attraktiv wirkender
Trailing-Parameter hält der Out-of-Sample-Prüfung nicht stand.

**Empfehlung: Trailing-Stop NICHT übernehmen** — fester 8%-Stop-Loss bleibt
Basisregel.

## 8. Nachfrage: Stress-Periode 2022 im Vergleich zu allen vier bestehenden Bots

Gleiche Methodik wie bei RSI-2 (`correlation_robustness_check.py`, Teil 2):
Rendite und Max Drawdown je Bot während 2022 (Krypto-Winter +
Fed-Zinserhöhungen), auf Basis der jeweils eigenen Kapitalkurve.

| Bot | Rendite 2022 | Max Drawdown 2022 |
|---|---|---|
| Elliott Wave (Krypto) | +21,20% | −0,23% |
| T3/SuperTrend (Krypto) | −3,28% | −12,28% |
| Elliott Wave (Aktien) | +81,44% | −0,63% |
| RSI-2 Mean-Reversion (Aktien, Prototyp) | −10,83% | −11,16% |
| **Volatility Breakout (Aktien, Prototyp, neu)** | **−13,14%** | **−22,39%** |

Gleichgewichtete hypothetische 5-Bot-Kombination während 2022: **+15,08%
Rendite, −1,90% Max Drawdown** (nur zur Einordnung — keine echte
Kapitalallokation zwischen Bots).

**Wichtiger Befund:** Volatility Breakout ist während 2022 sowohl das
schwächste Ergebnis (−13,14%) als auch der mit Abstand schlechteste Drawdown
(−22,39%) unter allen fünf Bots — und dieser Drawdown-Wert ist identisch mit
dem Maximum-Drawdown über den GESAMTEN Backtest-Zeitraum (Abschnitt 4). Das
heißt: der schlimmste Einbruch der gesamten Strategie-Historie fiel exakt in
diese Stress-Periode. Nachvollziehbar für eine Breakout-Strategie: in einem
breiten, anhaltenden Abwärtsmarkt wie 2022 lösen Bollinger-Band-Squeezes
überdurchschnittlich oft False Breakouts nach unten aus, bevor der Kurs
weiter fällt — das Gegenteil des saisonalen Vorteils von Mean-Reversion
(RSI-2) oder trendfolgenden Filtern mit engeren Drawdown-Kontrollen
(Elliott-Wave-Bots).

Trotzdem bleibt die gleichgewichtete 5-Bot-Kombination in der Stress-Periode
robust (−1,90% Max Drawdown kombiniert vs. −22,39% schlechtester Einzel-Bot)
— die anderen vier Bots (insbesondere die beiden Elliott-Wave-Bots mit
+21,20%/+81,44%) gleichen den Volatility-Breakout-Einbruch in der
hypothetischen Kombination weitgehend aus. Das bestätigt erneut, dass die
Diversifikationswirkung eher aus unterschiedlichem Verhalten der Bots
zueinander kommt als aus geringer Einzel-Bot-Robustheit — Volatility
Breakout selbst ist in Stressphasen aber klar der fragilste der fünf Bots.

## 9. Einordnung / offene Punkte für eine Entscheidung

- **Signalqualität ist solide** (Win Rate ~54%, Score verbessert sich sogar
  Out-of-Sample) — wie bei RSI-2 ist der dominante limitierende Faktor die
  **Kapitalbindung unter Limit 8 / 10% Allokation** (73% Skip-Rate, noch
  höher als RSI-2s 65%), nicht die Signalqualität selbst.
- **Weder Gesamtzeitraum noch Out-of-Sample schlagen Buy-and-Hold**
  (+142,06%/+74,54% vs. +776,24%) — identisches Muster zu RSI-2.
- **Volumen-Filter:** getestet, keine spürbare Verbesserung, nicht empfohlen.
- **Trailing-Stop:** getestet, Overfitting-Muster (identisch zum
  Elliott-Wave-Aktien-Bot-Präzedenzfall), nicht empfohlen. Fester 8%-Stop
  bleibt Basisregel.
- **Stress-Periode 2022:** Volatility Breakout ist der fragilste der fünf
  Bots in dieser einen Stressphase (schwächste Einzelrendite, mit Abstand
  schlechtester Drawdown, identisch zum Allzeit-Maximum-Drawdown der
  gesamten Strategie). Das ist ein relevanter Diversifikations-Datenpunkt,
  falls dieser Bot jemals live gehen sollte — er würde in einer 2022-artigen
  Phase voraussichtlich der größte Einzelrisikotreiber im Portfolio sein,
  wird aber (Stand jetzt) durch die anderen vier Bots in der hypothetischen
  Kombination weitgehend ausgeglichen.
- Wie bei RSI-2: keine der hier getesteten Stellschrauben (Stop-Loss,
  Volumen-Filter, Trailing-Stop) schließt die Lücke zu Buy-and-Hold. Ob und
  welche Kapitalmanagement-Hebel (Positionsgröße × Limit, wie bei RSI-2
  bereits systematisch getestet) hier ebenfalls helfen würden, wurde in
  dieser Runde noch nicht untersucht — möglicher nächster Schritt, falls
  gewünscht.
- Bewusst **nicht** umgesetzt (wie beauftragt): `live_params.py`, Cronjob,
  `forward_test.py`. Dieser Prototyp bleibt auf Backtest-/Walk-Forward-Stufe.

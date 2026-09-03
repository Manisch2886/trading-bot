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

## 10. Nachfrage: Risikoprofil-Vertiefung — ist die 2022-Schwäche ein wiederkehrendes Muster?

Vor einer Kapitalmanagement-Optimierung wurde geklärt, ob die 2022-Schwäche
(Abschnitt 8) ein strukturelles Fragilitätsmuster ist oder ein Einzelfall.

### 10a. Zweiter unabhängiger Stresstest: COVID-Crash Februar-April 2020

Datenbasis-Einschränkung: Die beiden Krypto-Bots haben erst ab ca.
September 2021 Kursdaten und sind für 2020 nicht auswertbar — der Vergleich
beschränkt sich auf die drei Aktien-Bots mit Historie bis mindestens 2016.

| Bot | Rendite (Feb–Apr 2020) | Max DD (Feb–Apr 2020) | Trades im Fenster | Win Rate im Fenster |
|---|---|---|---|---|
| Elliott Wave (Aktien) | +47,93% | −1,25% | 47 | 68,1% |
| RSI-2 Mean-Reversion (Aktien, Prototyp) | −9,60% | −9,93% | 29 | 41,4% |
| **Volatility Breakout (Aktien, Prototyp)** | **−2,00%** | **−3,64%** | 11 | 36,4% |

Zum Vergleich, Allzeit-Max-Drawdown je Bot (gesamte Historie):
Elliott Wave −1,65%, RSI-2 −21,82%, **Volatility Breakout −22,39%**.

**Befund: Das 2022-Muster wiederholt sich in 2020 NICHT.** Volatility
Breakout ist im COVID-Crash klar NICHT der schwächste Bot (RSI-2 verliert
deutlich mehr, −9,60% vs. −2,00%) und sein Drawdown in diesem Fenster
(−3,64%) liegt weit unter seinem Allzeit-Maximum (−22,39%) — anders als
2022, wo beide Werte identisch waren. RSI-2 zeigt hier das erwartbare
Mean-Reversion-Risiko ("in ein fallendes Messer greifen"), während
Volatility Breakout im schnellen, V-förmigen Crash vergleichsweise robust
bleibt (wenige Signale, moderater Verlust).

### 10b. Warum war der 2022-Drawdown identisch mit dem Allzeit-Maximum?

Der exakte Drawdown-Zeitraum wurde in der Portfolio-Kapitalkurve lokalisiert:
**Hoch am 11.04.2022 (18.960,04) → Tief am 19.10.2022 (14.714,44), −22,39%,
über 191 Tage.** Das ist bereits die erste wichtige Erkenntnis: **kein
konzentriertes Einzelereignis**, sondern eine über gut sechs Monate
verteilte Schwächephase.

Signal-Ebene im Fenster (11.04.–19.10.2022): 169 Squeeze-Breakout-Einstiege,
167 Ausstiege. Ausstiegsart: **107 Zeit-Exit (64,1%), 60 Stop-Loss/False
Breakout (35,9%)**. Zum Vergleich: der Stop-Loss-Anteil über die GESAMTE
10-Jahres-Historie liegt bei nur 17,8% — im Drawdown-Fenster also **etwa
doppelt so hoch** wie normal.

Die wöchentliche Aufschlüsselung zeigt keine einzelne Extremwoche, sondern
mehrere Wellen erhöhter False-Breakout-Raten über das gesamte Fenster
verteilt (z. B. Woche 02.–08.05.: 100% Stop-Loss von 3 Exits; Woche
13.–19.06.: 85,7% von 7; Woche 22.–28.08.: 83,3% von 6; Woche 19.–25.09.:
100% von 5) — abwechselnd mit ruhigeren Wochen. Das bestätigt: **eine über
Monate verteilte, strukturelle Schwäche, kein einzelner Ausverkaufstag.**

Noch deutlicher zeigt sich das bei den tatsächlich kapitalgebundenen
(ausgeführten) Trades: 64 ausgeführte Positions-Exits im Fenster, davon
**76,6% mit negativem PnL** (vs. 46,1% negative PnL-Quote über die gesamte
Historie) — auch etliche Zeit-Exits schlossen in diesem Fenster im Minus,
nicht nur die Stop-Loss-Trades. Erklärung: 2022 war für Aktien ein
anhaltender, breiter Abwärtsmarkt (Fed-Zinserhöhungen) — genau das Umfeld,
in dem Bollinger-Band-Squeezes wiederholt in Richtung des übergeordneten
Trends (abwärts) "falsch" nach oben ausbrechen, bevor der Kurs weiter fällt.
Ein einzelner Tag reicht dafür nicht — es braucht einen anhaltenden,
mehrmonatigen Bärenmarkt, in dem sich dieses Muster wiederholt ausbilden und
scheitern kann.

### 10c. Einordnung

**Die Sorge war teilweise berechtigt, aber anders als zunächst vermutet:**
Volatility Breakout hat kein generelles "Crash-Fragilitäts"-Problem — im
schnellen COVID-Crash (10a) war es der robusteste der drei vergleichbaren
Aktien-Bots. Die tatsächliche Schwachstelle ist spezifischer: **anhaltende,
mehrmonatige Bärenmärkte mit wiederholten volatilitätsarmen
Konsolidierungsphasen**, wie 2022. In einem solchen Umfeld erzeugt die
Kernlogik der Strategie (Squeeze → Ausbruchsversuch) systematisch gehäufte
False Breakouts, weil der übergeordnete Abwärtstrend die meisten
Ausbruchsversuche nach oben zunichtemacht — kein Zufallsereignis, sondern
eine nachvollziehbare Eigenschaft von Breakout-Strategien in Bärenmärkten.

Im Vergleich zu RSI-2 ergibt sich ein **anderes, nicht per se schlechteres,
aber andersartiges Risikoprofil**: RSI-2 zeigte in beiden Stressphasen
(2020 UND 2022) ein moderates, konsistentes Schwächeln (−9,6% bzw. −10,8%
Rendite, DD jeweils um −10% bis −12%, jeweils deutlich unter seinem
Allzeit-Maximum-Drawdown) — ein klassisches "Mean-Reversion-in-fallenden-
Märkten"-Risiko ohne Extremausschlag. Volatility Breakout dagegen zeigt
**bimodales** Verhalten: unauffällig bis robust im schnellen Crash (2020),
aber ein ausgeprägtes Einzelereignis-Risiko im anhaltenden Bärenmarkt (2022,
identisch zum Allzeit-Extrem). Das ist ein reales, spezifisches
Risikomerkmal — kein diffuses "generell fragiler" —, das bei einer
späteren Live-Entscheidung/Gewichtung berücksichtigt werden sollte
(insbesondere weil sich mehrmonatige Bärenmärkte nicht durch kurzfristige
Diversifikation zu schnellen Crashs abfedern lassen).

**Empfehlung für die nächsten Schritte:** Die Strategie ist für eine
Kapitalmanagement-Optimierung (wie bei RSI-2) grundsätzlich geeignet — das
Risiko ist verstanden, spezifisch benennbar und nicht diffus. Es sollte aber
bei einer künftigen Live-/Gewichtungs-Entscheidung explizit berücksichtigt
werden, dass Volatility Breakout in einem 2022-artigen, mehrmonatigen
Bärenmarkt der mit Abstand größte Einzelrisikotreiber im Portfolio wäre —
unabhängig davon, wie das Kapitalmanagement innerhalb des Bots selbst
konfiguriert ist.

## 11. Kapitalmanagement-Tuning (analog zur RSI-2-Vorgehensweise)

Reine Analyse, weiterhin nichts live geschaltet. Nach Klärung des
Risikoprofils (Abschnitt 10) wie angekündigt: derselbe Kapitalmanagement-
Test wie bei RSI-2, mit demselben Ausgangsverdacht (Kapitalmanagement, nicht
Signalqualität, ist der dominante Flaschenhals bei 73% Skip-Rate).

### 11a. Signal-Qualitäts-Test

Vergleich (a) tatsächlich ausgeführte Trades (Limit 8, 10% Allokation) vs.
(b) alle gefundenen Signale vs. (c) rein diagnostische
"unbegrenztes Kapital"-Simulation (kein Live-Vorschlag):

| | (a) Ausgeführt (Limit 8) | (b) Alle Signale | (c) Kapital unbegrenzt (Portfolio) |
|---|---|---|---|
| Gesamtzeitraum | n=1236, Win Rate 53,8%, Ø PnL 0,782% | n=4510, Win Rate 53,9%, Ø PnL 0,702% | +1088,99% (DD −38,34%) |
| Out-of-Sample | n=385, Win Rate 56,4%, Ø PnL 1,54% | n=1334, Win Rate 54,6%, Ø PnL 1,09% | +249,03% (DD −20,64%) |

Differenz Ø PnL (ausgeführt − alle gefunden): **Gesamtzeitraum +0,080pp, OOS
+0,450pp.**

**Wichtiger Unterschied zu RSI-2:** Bei RSI-2 waren die ausgeführten Trades
im Schnitt leicht SCHLECHTER als die Gesamtpopulation (chronologische
Auswahl wählte nicht neutral). Bei Volatility Breakout ist es umgekehrt —
die ausgeführten Trades sind sogar leicht BESSER. Der Kapital-Flaschenhals
bestätigt sich trotzdem klar als dominanter Faktor: die reale
Portfolio-Rendite (+142,06%/+74,54%) liegt weit unter der hypothetischen
Kapital-unbegrenzt-Rendite (+1088,99%/+249,03%, jeweils Faktor ~7,7×/3,3×)
— **Kapitalmanagement, nicht Signalqualität, ist auch hier der dominante
Flaschenhals**, mit sogar noch größerem Hebel als bei RSI-2.

### 11b. Positionsgröße × Limit-Matrix

Feste Parameter: 8% Stop-Loss, 15 Handelstage Zeit-Exit. 16 Kombinationen
(10%/5%/3%/2% × Limit 8/15/20/unbegrenzt) getestet, Gesamtzeitraum und OOS:

| Allokation | Limit | Rendite (Gesamt) | Max DD (Gesamt) | Rendite (OOS) | Max DD (OOS) |
|---|---|---|---|---|---|
| **10%** | **15/20/unbegrenzt (identisch)** | **+224,41%** | **−23,97%** | **+93,18%** | **−12,53%** |
| 10% | 8 (Basis) | +142,06% | −22,39% | +74,54% | −10,53% |
| 5% | 20/unbegrenzt (identisch) | +157,47% | −15,71% | +55,75% | −10,13% |
| 3% | unbegrenzt | +99,73% | −10,22% | +39,06% | −6,65% |
| 2% | unbegrenzt | +75,36% | −7,10% | +32,09% | −4,48% |

(Vollständige 16-Zeilen-Matrix in
`results/volatility_breakout/experiment_position_size_limit_{full,oos}.csv`.)

**Beste gefundene Kombination: 10% Allokation, Limit ≥15** (Limit 15, 20 und
unbegrenzt liefern identische Ergebnisse — bei 10% Allokation sättigt das
Kapital von selbst bei rund 10 gleichzeitigen Positionen, ein höheres Limit
hat keinen zusätzlichen Effekt). Gegenüber der Basiskonfiguration (Limit 8):
Rendite steigt deutlich (+82,35pp Gesamtzeitraum, +18,64pp OOS), Max Drawdown
steigt nur leicht (+1,58pp Gesamtzeitraum, +2,00pp OOS) — genau der
gesuchte Punkt, an dem die Rendite noch spürbar steigt, ohne dass der
Drawdown explodiert. Anders als bei RSI-2 (wo 5%/Limit 20 die 10%-Variante
im Gesamtzeitraum bei Rendite UND Drawdown strikt dominierte) gibt es hier
einen echten Rendite/Risiko-Trade-off: 5% Allokation liefert weniger Rendite
bei geringerem Drawdown, 10% mehr Rendite bei etwas höherem Drawdown — keine
strikte Dominanz einer Allokationsgröße.

### 11c. 2022-Stress-Periode unter der besten Konfiguration

| Konfiguration | Rendite 2022 | Max DD 2022 |
|---|---|---|
| Basis (10% Allokation, Limit 8) | −13,14% | −22,39% |
| **Beste Kombination (10% Allokation, Limit 15)** | **−12,94%** | **−23,97%** |

**Befund: der 2022-Schwachpunkt bleibt strukturell nahezu unverändert** —
Rendite marginal besser (−13,14%→−12,94%), Max Drawdown sogar leicht
schlechter (−22,39%→−23,97%, mehr gebundenes Kapital durch die höhere
Kapitalauslastung verstärkt den Drawdown geringfügig). Das bestätigt die in
Abschnitt 10 aufgestellte Erwartung: die False-Breakout-Rate im 2022-Fenster
(35,9%, mehr als doppelt so hoch wie der historische Basiswert von 17,8%)
ist eine Eigenschaft der SIGNALE während dieser Marktphase, nicht der
Kapitalauslastung — kein Kapitalmanagement-Hebel kann eine
Signalqualitäts-Schwäche kompensieren, die genau in dieser Phase auftritt.

### 11d. Zusammenfassung aller getesteten Konfigurationen (sortiert nach OOS-Rendite)

| Allokation | Limit | Rendite Gesamt | DD Gesamt | Rendite OOS | DD OOS | Rendite 2022 | DD 2022 |
|---|---|---|---|---|---|---|---|
| **10%** | **15/20/∞** | **+224,41%** | **−23,97%** | **+93,18%** | **−12,53%** | **−12,94%** | **−23,97%** |
| 10% | 8 (Basis) | +142,06% | −22,39% | +74,54% | −10,53% | −13,14% | −22,39% |
| 5% | 20/∞ | +157,47% | −15,71% | +55,75% | −10,13% | −10,03% | −15,71% |
| 5% | 15 | +106,98% | −15,41% | +45,21% | −9,00% | −8,54% | −15,26% |
| 3% | ∞ | +99,73% | −10,22% | +39,06% | −6,65% | −5,61% | −9,77% |
| 5% | 8 | +58,80% | −11,73% | +33,27% | −5,38% | −6,52% | −11,73% |
| 3% | 20 | +78,30% | −9,85% | +32,27% | −6,42% | −5,50% | −9,85% |
| 2% | ∞ | +75,36% | −7,10% | +32,09% | −4,48% | −0,80% | −4,95% |
| 3% | 15 | +56,53% | −9,45% | +25,66% | −5,49% | −5,04% | −9,36% |
| 2% | 20 | +47,85% | −6,64% | +20,76% | −4,32% | −3,62% | −6,64% |
| 3% | 8 | +32,64% | −7,17% | +19,06% | −3,26% | −3,90% | −7,17% |
| 2% | 15 | +35,34% | −6,36% | +16,63% | −3,69% | −3,32% | −6,31% |
| 2% | 8 | +20,92% | −4,82% | +12,42% | −2,18% | −2,59% | −4,82% |

(Vollständige Tabelle inkl. Trade-Anzahl in
`results/volatility_breakout/capital_management_summary.csv`.)

**Beobachtung am Rand:** 2% Allokation/unbegrenzt zeigt mit Abstand die
mildeste 2022-Performance (−0,80%/−4,95% DD) — aber auch die zweitniedrigste
Gesamtrendite. Das ist kein Widerspruch zu 11c: bei sehr kleiner
Positionsgröße wird trotz mehr gleichzeitig offener Positionen (4249
ausgeführte Trades statt 1236) das gebundene Kapital pro Position so klein,
dass selbst eine erhöhte False-Breakout-Rate kaum noch spürbar wird — ein
reiner Verwässerungseffekt (weniger Rendite generell), keine echte
Verbesserung der Signalqualität in der Stressphase.

### 11e. Empfehlung

**10% Allokation, Limit ≥15** ist die im Gesamtzeitraum UND Out-of-Sample
beste gefundene Kombination und wird als Kandidat für eine spätere
Live-Entscheidung festgehalten — mit der ausdrücklichen Einordnung aus
Abschnitt 10/11c: diese Optimierung verbessert die Rendite in normalen
Marktphasen deutlich, mildert aber die spezifische 2022-artige
Bärenmarkt-Schwäche nicht. Wie bei RSI-2 schließt auch die beste gefundene
Kapitalmanagement-Kombination die Lücke zu Buy-and-Hold (+776,24%) nicht
vollständig (+224,41% Gesamtzeitraum), verbessert die Bot-eigene Performance
aber erheblich gegenüber der ursprünglichen Limit-8-Basiskonfiguration.

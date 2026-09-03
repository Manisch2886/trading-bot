# RSI-2 Mean-Reversion — Prototyp-Ergebnisse (vierter Bot)

Stand: 2026-09-03. Prototyp bis einschließlich Backtest/Walk-Forward-Stufe,
wie beauftragt. **Nichts live geschaltet** — keine `live_params.py`, kein
Cronjob, kein `forward_test.py`.

---

## 1. Regeln (exakt spezifiziert)

Vollständige, verbindliche Spezifikation in `backtest_rsi2.py` (Modul-Docstring).
Kurzfassung:

1. **Trendfilter:** Schlusskurs > SMA(200).
2. **Einstieg:** Trendfilter erfüllt UND RSI(2) < Schwelle (getestet: 5 und 10).
   Einstieg zum Schlusskurs des Signaltags. Kein Pyramiding (max. eine offene
   Position pro Symbol).
3. **Ausstieg — "je nachdem was zuerst eintritt", explizite Priorität pro Tag:**
   a) Stop-Loss (falls aktiv) — Tagestief ≤ Stop-Kurs
   b) SMA-Exit — Schlusskurs > SMA(5)
   c) Zeit-Exit — spätestens nach 10 Handelstagen nach Einstieg, zum Schlusskurs
   Auf einem Tag zählt immer nur die zuerst zutreffende Bedingung (a vor b vor c).
4. **Stop-Loss-Einordnung:** Connors verwendet standardmäßig keinen festen Stop
   (nur Zeit-Exit). Statt das anzunehmen, wurde es **empirisch getestet**
   (kein Stop vs. 5% vs. 8%) — Ergebnis siehe Abschnitt 2: Ein harter Stop
   **senkt den Ø-Gewinn/Trade spürbar** (z. B. RSI<5: 0,229% ohne Stop → nur
   0,037% mit 5%-Stop). Bestätigt Connors' Ansatz empirisch statt ihn nur zu
   übernehmen.

## 2. Multi-Symbol-Optimierung (Gesamtzeitraum, 147 Symbole)

| RSI-Schwelle | Stop-Loss | Trades | Win Rate | Ø PnL/Trade | Ø Haltedauer |
|---|---|---|---|---|---|
| **10** | **kein Stop** | 10.342 | 64,5% | 0,20% | 5,6 Tage |
| 5 | kein Stop | 5.391 | 64,5% | 0,23% | 5,7 Tage |
| 10 | 8% | 10.526 | 64,2% | 0,08% | 5,2 Tage |
| 10 | 5% | 10.945 | 62,8% | 0,06% | 4,7 Tage |
| 5 | 8% | 5.470 | 64,1% | 0,07% | 5,3 Tage |
| 5 | 5% | 5.641 | 62,6% | 0,04% | 4,7 Tage |

## 3. Walk-Forward (70/30, Split innerhalb des 10-Jahres-Fensters)

**Wichtiger Implementierungs-Fix unterwegs:** Der Split-Punkt muss innerhalb
des 10-Jahres-Auswertungsfensters liegen, nicht auf der vollen (bei manchen
Aktien 60+ Jahre reichenden) Rohhistorie — sonst entsteht ein stark
verzerrter, ungleicher Split. Wurde vor der Auswertung korrigiert (siehe
`multi_symbol_walk_forward.split_all_symbols`).

| Metrik | In-Sample | Out-of-Sample |
|---|---|---|
| Beste Kombination | RSI<5, kein Stop | (dieselbe, keine Re-Optimierung) |
| Win Rate | 63,8% | **66,0%** |
| Ø Gewinn/Trade | 0,10% | **0,50%** |
| Anzahl Trades | 3.674 | 1.718 |
| Robustheit-Score | 0,033 | **0,292** (deutlich höher als In-Sample) |

**Starkes Robustheits-Signal**: Win Rate, Ø PnL und Score verbessern sich
allesamt Out-of-Sample statt abzufallen — kein Overfitting-Muster (analog zur
positiven OOS-Überraschung beim Elliott-Wave-Aktien-Bot).

## 4. Equity-Simulation (10.000 Start, 10% Allokation, **Limit 8** — fix, wie angefragt)

**Gesamtzeitraum:**

| RSI | Stop | Endkapital | Rendite | Trades ausgef./übersprungen | Max DD |
|---|---|---|---|---|---|
| 5 | kein Stop | 12.991 | **+29,91%** | 2.641 / 2.750 | -21,82% |
| 5 | 5% | 9.902 | -0,98% | 3.087 / 2.554 | -23,70% |
| 5 | 8% | 10.017 | +0,17% | 2.791 / 2.679 | -28,27% |
| 10 | kein Stop | 10.761 | +7,61% | 3.591 / 6.751 | -35,91% |
| 10 | 5% | 10.222 | +2,22% | 4.271 / 6.674 | -28,06% |
| 10 | 8% | 11.204 | +12,04% | 3.867 / 6.659 | -29,45% |

**Out-of-Sample:**

| RSI | Stop | Endkapital | Rendite | Trades ausgef./übersprungen | Max DD |
|---|---|---|---|---|---|
| 5 | kein Stop | 13.501 | +35,01% | 887 / 831 | -11,44% |
| 5 | 5% | 12.634 | +26,34% | 1.048 / 750 | -10,50% |
| 5 | 8% | 12.515 | +25,15% | 938 / 803 | -13,86% |
| **10** | **kein Stop** | **15.068** | **+50,68%** | 1.205 / 2.139 | **-8,26%** |
| 10 | 5% | 13.464 | +34,64% | 1.460 / 2.084 | -13,34% |
| 10 | 8% | 14.295 | +42,95% | 1.297 / 2.103 | -11,24% |

**Buy-and-Hold-Vergleich (dasselbe Universum/Zeitraum):**

| Zeitraum | Endkapital | Rendite | Max DD |
|---|---|---|---|
| Gesamtzeitraum | 87.624 | +776,24% | -34,83% |
| Out-of-Sample | 23.823 | +138,23% | -20,95% |

### Zentraler Befund: massiver Skip-Rate-Effekt durch das feste Positionslimit

RSI-2 erzeugt **deutlich mehr gleichzeitige Signale** als die wellenbasierten
Bots (bis zu 6.751 von ~10.500 Signalen übersprungen bei RSI 10 — knapp
**65%** der gefundenen Trades kommen bei Limit 8 gar nicht zum Zug, gegenüber
z. B. nur ~10% beim Elliott-Wave-Aktien-Bot bei gleichem Limit). Das ist der
Hauptgrund, warum die reale, kapitalgewichtete Rendite (max. +29,91% bzw.
+50,68% OOS) so viel schwächer ausfällt als der naive Trade-Durchschnitt
vermuten ließe (Ø PnL positiv, Score OOS sogar besser als In-Sample). Der
Trade-Level-Edge ist also real und OOS-bestätigt — bei Limit 8 kann das
Portfolio ihn aber nur zu einem kleinen Teil tatsächlich einsammeln.

**RSI-2 schlägt Buy-and-Hold bei Limit 8 NICHT** — weder Gesamtzeitraum
(+29,91% vs. +776,24%) noch OOS (+50,68% vs. +138,23%). Der Drawdown ist
dagegen in allen Fällen deutlich kleiner als Buy-and-Hold (-8,26% bis
-35,91% vs. -34,83%/-20,95%). Anders als bei den bestehenden Bots ist "Limit
8" hier vermutlich kein fairer Vergleichspunkt in der Sache, sondern eine
strukturelle Fehlpassung zum viel höheren Signalaufkommen dieser Strategie —
ein höheres Positionslimit wäre der naheliegende nächste Test (siehe
Abschnitt 6), aber bewusst noch nicht durchgeführt, wie angefragt nur bis zur
Backtest-/Walk-Forward-Stufe.

## 5. Portfolio-Korrelationsanalyse (grobe erste Einschätzung)

Gemeinsames Vergleichsfenster aller vier Bots (durch Krypto-Datenverfügbarkeit
begrenzt): 2021-09-14 bis 2026-06-27.

**Korrelationsmatrix (tägliche Renditen):** alle Werte zwischen -0,02 und
0,01 — praktisch unkorreliert. **Einschränkung:** Das ist teils ein
mechanischer Effekt seltener Handelstage (an den meisten Tagen ändert sich
bei keiner Strategie etwas), nicht zwingend Beweis für eine "echte"
Diversifikation der Marktreaktion — mit Vorsicht zu interpretieren.

**Aussagekräftiger — Drawdown-Diversifikation:**

| Bot | Max Drawdown im gemeinsamen Fenster |
|---|---|
| Elliott Wave (Krypto) | -0,23% |
| T3/SuperTrend (Krypto) | -22,20% |
| Elliott Wave (Aktien) | -1,65% |
| RSI-2 Mean-Reversion (Aktien, neu) | -12,72% |
| **Gleichgewichtete 4-Bot-Kombination (25/25/25/25)** | **-1,43%** |

Die Verlustphasen der vier Bots überlappen sich im Backtest kaum — der
schlechteste Einzel-Bot-Drawdown (-22,20%, T3/SuperTrend) wird in der
kombinierten Kurve auf -1,43% geglättet. Das bestätigt die
Diversifikations-Hypothese aus der Recherche recht deutlich, wenn auch nur
als grobe, backtest-basierte Ersteinschätzung (keine echten
Forward-Test-Daten, hypothetische Gleichgewichtung, keine tatsächliche
Kapitalallokation zwischen den eigenständigen Bots).

## 6. Nachfrage: Positionsgröße x Positionslimit (statt nur Limit)

Hypothese aus der Rückfrage: Nicht das explizite Limit (8) ist der
Flaschenhals, sondern die 10%-Kapitalallokation selbst (siehe Abschnitt 4 im
Übergabeprotokoll-Kontext: bei fester Allokation deckelt sich die Anzahl
gleichzeitig offener Positionen implizit auf ~1/Allokations-Anteil,
unabhängig vom expliziten Limit). Matrix: Allokation 10%/5%/3% × Limit
8/15/20/unbegrenzt, feste Parameter RSI<5, kein Stop
(`experiment_position_size_limit.py`).

**Gesamtzeitraum:**

| Allokation | Limit | Endkapital | Rendite | Trades ausgef./übersprungen | Max DD |
|---|---|---|---|---|---|
| 10% | 8 | 12.991 | +29,91% | 2.641 / 2.750 | -21,82% |
| 10% | 15/20/unbegrenzt (identisch) | 13.394 | +33,94% | 2.940 / 2.451 | -28,46% |
| **5%** | **8** | 11.504 | +15,04% | 2.641 / 2.750 | -11,33% |
| 5% | 15 | 12.691 | +26,91% | 3.752 / 1.639 | -18,48% |
| **5%** | **20/unbegrenzt (identisch)** | **13.675** | **+36,75%** | 4.232 / 1.159 | -21,05% |
| 3% | 8 | 10.901 | +9,01% | 2.641 / 2.750 | -6,90% |
| 3% | 15 | 11.588 | +15,88% | 3.752 / 1.639 | -11,39% |
| 3% | 20 | 12.335 | +23,35% | 4.271 / 1.120 | -12,71% |
| 3% | unbegrenzt | 12.935 | +29,35% | 4.931 / 460 | -15,84% |

**Out-of-Sample:**

| Allokation | Limit | Endkapital | Rendite | Trades ausgef./übersprungen | Max DD |
|---|---|---|---|---|---|
| 10% | 8 | 13.501 | +35,01% | 887 / 831 | -11,44% |
| **10%** | **15/20/unbegrenzt (identisch)** | **14.843** | **+48,43%** | 994 / 724 | -12,85% |
| 5% | 8 | 11.659 | +16,59% | 887 / 831 | -5,78% |
| 5% | 15 | 13.071 | +30,71% | 1.260 / 458 | -5,57% |
| 5% | 20/unbegrenzt (identisch) | 13.597 | +35,97% | 1.415 / 303 | -5,22% |
| 3% | 8 | 10.973 | +9,73% | 887 / 831 | -3,48% |
| 3% | 15 | 11.760 | +17,60% | 1.260 / 458 | -3,35% |
| 3% | 20 | 12.129 | +21,29% | 1.427 / 291 | -3,17% |
| 3% | unbegrenzt | 12.560 | +25,60% | 1.623 / 95 | -4,82% |

**Befund: Hypothese eindeutig bestätigt.** Bei 10% Allokation sind Limit 15,
20 und unbegrenzt exakt IDENTISCH (Gesamt: 2.940/2.451 in allen drei
Fällen) — die 10%-Kapitalallokation selbst deckelt bei ca. 10 gleichzeitigen
Positionen, das explizite Limit wird ab 15 komplett wirkungslos. Dasselbe
Muster bei 5% Allokation (Limit 20 = unbegrenzt, Deckelung bei ~20
Positionen). Erst bei 3% Allokation macht das Limit bis "unbegrenzt" noch
einen Unterschied (natürliche Deckelung bei ~33 Positionen).

**Bestes Gesamtergebnis: 5% Allokation, Limit ≥20** — höhere Rendite als die
10%-Variante (+36,75% vs. +33,94%) bei gleichzeitig kleinerem Drawdown
(-21,05% vs. -28,46%). Out-of-Sample liefert dieselbe Kombination ein
deutlich kleineres Risiko (-5,22% statt -12,85% DD) bei nur leicht
geringerer Rendite (+35,97% vs. +48,43% bei 10%/unbegrenzt). Die
übersprungenen Trades sinken massiv (Gesamt: von 2.750 auf 1.159 bei
5%/≥20, auf nur noch 460 bei 3%/unbegrenzt). **Keine der getesteten
Kombinationen schlägt jedoch Buy-and-Hold bei der Rendite** (weiterhin
+776%/+776% bzw. +138% OOS als Referenz aus Abschnitt 4) — die kleinere
Allokation hilft dem Portfolio-Ergebnis spürbar, schließt die Lücke aber
nicht vollständig.

## 7. Nachfrage: Korrelationsanalyse robuster geprüft

### 7a. Gemeinsame Handelstage (Aktivitäts-Überlappung)

`correlation_robustness_check.py`, gemeinsames Fenster 2021-09-14 bis
2026-06-27 (1.748 Tage):

| Metrik | Wert |
|---|---|
| Tage mit ≥1 Bot mit Trade-Exit | 965 (55,2%) |
| Tage mit ≥2 Bots GLEICHZEITIG | 279 (16,0%) |
| Tage mit ≥3 Bots GLEICHZEITIG | 27 (1,5%) |
| Tage mit ALLEN 4 Bots GLEICHZEITIG | 0 (0,0%) |

Aktivitätsanteil je Bot: Elliott Wave Krypto 6,1%, T3/SuperTrend 20,8%,
Elliott Wave Aktien 10,5%, RSI-2 35,4% der Tage.

**Bestätigt die geäußerte Sorge teilweise:** Mit nur 16% der Tage mit
Überlappung ≥2 Bots und 0% mit allen 4 gleichzeitig ist die
"praktisch unkorreliert"-Aussage aus Abschnitt 5 tatsächlich zu einem
guten Teil ein Effekt dünner, seltener Handelsaktivität — an über 80% der
Tage bewegt sich höchstens ein Bot überhaupt, was eine niedrige gemessene
Korrelation der täglichen Renditen mechanisch begünstigt, unabhängig davon,
ob die Strategien "wirklich" unterschiedlich auf denselben Marktimpuls
reagieren würden. Die Aktivitäts-Korrelation selbst ist überwiegend
ebenfalls niedrig (-0,07 bis 0,02), mit einer Ausnahme: Elliott Wave Aktien
und RSI-2 (beide Aktien-Bots) korrelieren mit 0,16 leicht positiv in ihren
Handelstagen — beide reagieren auf ähnliche Aktienmarkt-Volatilität, auch
wenn sie unterschiedlich handeln.

### 7b. Verhalten während der Stress-Periode 2022 (Krypto-Winter/Zinserhöhungen)

| Bot | Rendite 2022 | Max Drawdown 2022 |
|---|---|---|
| Elliott Wave (Krypto) | +21,20% | -0,23% |
| T3/SuperTrend (Krypto) | -3,28% | **-12,28%** |
| Elliott Wave (Aktien) | **+81,44%** | -0,63% |
| RSI-2 Mean-Reversion (Aktien, neu) | **-10,83%** | -11,16% |
| **Gleichgewichtete 4-Bot-Kombination** | **+22,13%** | **-1,01%** |

**Das ist die deutlich aussagekräftigere Evidenz als die reine
Korrelationszahl.** RSI-2 zeigt hier konkret genau die in der
Kandidaten-Recherche vorab benannte Schwäche (Mean-Reversion in
anhaltenden/volatilen Abwärtsphasen: -10,83% Rendite, -11,16% Drawdown) -
und T3/SuperTrend leidet ebenfalls (Trendfolge in einem choppy/bärischen
Kryptojahr: -3,28%, -12,28% DD). Gleichzeitig liefern die beiden anderen
Bots in genau demselben Jahr ihre besten Ergebnisse (Elliott Wave Aktien
+81,44%, Elliott Wave Krypto +21,20%) - die schwachen und starken Phasen
fallen zeitlich zusammen, aber bei UNTERSCHIEDLICHEN Bots. Die kombinierte
Kurve bleibt dadurch bei nur -1,01% Drawdown während exakt der Periode, in
der der schlechteste Einzel-Bot -12,28% verlor. Das ist eine konkrete,
nicht nur statistische Bestätigung: RSI-2s bekannte Schwäche wurde durch
die anderen drei Bots in genau diesem Zeitraum real ausgeglichen, nicht nur
im Durchschnitt über die Gesamtperiode.

## 8. Einordnung / offene Punkte für eine Entscheidung

- **Trade-Level-Edge ist real und OOS-bestätigt** (Win Rate ~64-66%, Score
  verbessert sich OOS) — die Grundidee funktioniert.
- **Positionsgröße, nicht Limit, war der Haupt-Flaschenhals** (Abschnitt 6,
  Hypothese bestätigt) — 5% Allokation mit Limit ≥20 verbessert Rendite UND
  Drawdown gegenüber der ursprünglichen 10%/Limit-8-Kombination deutlich,
  schließt die Lücke zu Buy-and-Hold aber nicht vollständig.
- **Drawdown-Diversifikation im 4-Bot-Verbund bestätigt sich auch bei
  genauerer Prüfung** (Abschnitt 7) — die rohe Korrelationszahl war teils
  ein Aktivitäts-Artefakt, aber die konkrete Stress-Test-Periode 2022 zeigt
  echten, zeitlich konkreten Ausgleich zwischen den Bots, keine Scheinkorrelation.
- Kein Stop-Loss (Connors' Standardversion) bestätigt sich als die bessere
  Wahl gegenüber festen Stop-Werten.
- Weiterhin **nichts live geschaltet** — alle Ergebnisse rein analytisch.

Reproduzierbar mit:
```
python3 strategies/rsi2_mean_reversion/multi_symbol_optimise.py
python3 strategies/rsi2_mean_reversion/multi_symbol_walk_forward.py
python3 strategies/rsi2_mean_reversion/pipeline_report.py
python3 strategies/rsi2_mean_reversion/portfolio_correlation_analysis.py
python3 strategies/rsi2_mean_reversion/experiment_position_size_limit.py
python3 strategies/rsi2_mean_reversion/correlation_robustness_check.py
python3 strategies/rsi2_mean_reversion/experiment_signal_quality_and_priority.py
```

---

## 9. Gezielte Diagnose des Kernproblems: Signal-Qualität vs. Kapitalmanagement

Statt weiterer Parameterwerte zwei gezielte Diagnosen des Kernbefunds aus
Abschnitt 4 (bis zu 65% der gefundenen Trades werden bei Limit 8
übersprungen). `experiment_signal_quality_and_priority.py`, feste Parameter
RSI<5, kein Stop.

### 9a. Signal-Qualitäts-Test (Timing-Nutzen vs. Kapitalmanagement-Nutzen)

Vergleich (a) tatsächlich mit Kapital versorgte Trades (10% Allokation,
Limit 8 - ursprünglicher validierter Startpunkt) gegen (b) ALLE gefundenen
Signale unabhängig von Kapitalverfügbarkeit gegen (c) eine rein
diagnostische "unbegrenztes Kapital"-Simulation (jedes Signal bekommt
sofort 10% des aktuellen Kapitals, kein Limit — **kein Live-Vorschlag,
unrealistisches Leverage**):

| | Gesamtzeitraum | Out-of-Sample |
|---|---|---|
| (a) Ausgeführt (Limit 8, 10%): n, Win Rate, Ø PnL | 2.641 / 63,3% / **0,113%** | 887 / 63,9% / **0,354%** |
| (b) Alle gefundenen Signale: n, Win Rate, Ø PnL | 5.391 / 64,5% / **0,229%** | 1.718 / 66,0% / **0,5%** |
| Differenz Ø PnL (a − b) | **-0,116 Prozentpunkte** | **-0,146 Prozentpunkte** |
| (c) Portfolio bei unbegrenztem Kapital | +185,72% (DD -50,12%) | +126,80% (DD -12,36%) |
| Zum Vergleich: reales Portfolio (a) | +29,91% (DD -21,82%) | +35,01% (DD -11,44%) |

**Befund geht über die ursprüngliche Hypothese hinaus.** Die Portfolio-Differenz
zwischen real (a) und unbegrenzt (c) ist riesig (+29,91%→+185,72% Gesamtzeitraum,
+35,01%→+126,80% OOS) — das bestätigt klar: **Kapitalmanagement ist der
dominante Flaschenhals**, nicht die Signalqualität selbst. Zusätzlicher,
nicht erwarteter Befund: Die tatsächlich ausgeführten Trades sind im
Schnitt sogar **leicht schlechter** als die Gesamtpopulation aller
gefundenen Signale (-0,116/-0,146 Prozentpunkte), nicht nur eine zufällige
Stichprobe davon. Der chronologische "wer zuerst kommt, kriegt Kapital"-
Mechanismus wählt also nicht neutral aus — plausible Erklärung: Phasen mit
vielen gleichzeitigen Signalen (breite Marktbewegungen) erschöpfen das
Kapital schneller, sodass gerade dort viele Signale übersprungen werden,
während in ruhigeren Phasen mit wenig Konkurrenz praktisch jedes Signal
durchkommt — unabhängig davon, ob "viele gleichzeitige Signale" im Schnitt
bessere oder schlechtere Trades sind.

### 9b. Signal-Priorisierung bei Kapital-Konkurrenz

Bei mehreren Signalen am selben Tag: aktuelle (chronologisch/alphabetisch
nach Symbol) vs. RSI-priorisiert (niedrigster RSI(2)-Wert bekommt zuerst
Kapital), bei der zuletzt validierten Kombination (5% Allokation, Limit 20):

| | Gesamtzeitraum | Out-of-Sample |
|---|---|---|
| Aktuell (chronologisch) | +36,75% (DD -21,05%), 4.232/1.159 | +35,97% (DD -5,22%), 1.415/303 |
| RSI-priorisiert | +36,20% (DD -19,53%), 4.218/1.173 | +34,97% (DD -5,10%), 1.415/303 |

**Befund: kein relevanter Unterschied.** Beide Varianten liegen innerhalb
von unter 1 Prozentpunkt Rendite-Differenz, Drawdown minimal unterschiedlich
in beide Richtungen — im Rauschen. Bestätigt indirekt den Befund aus 9a: Es
kommt auf die **Menge** des verfügbaren Kapitals an (Allokations-%/Limit),
nicht darauf, **welches** der konkurrierenden Signale die knappen
Kapitalplätze bekommt. Eine Priorisierungs-Logik allein löst das
Kernproblem nicht.

### 9c. Einordnung: Diversifikations-Trade-off (wie angefragt)

Explizit geprüft, ob die 5%/Limit-20-Verbesserung (aus Abschnitt 6, bereits
validiert) RSI-2s Wert genau in der 2022-Stress-Periode (siehe Abschnitt
7b) abschwächt — RSI-2s Diversifikationsbeitrag kam bisher gerade daher,
dass es dort verlor, während die anderen Bots dort am stärksten liefen:

| Konfiguration | 2022-Rendite | 2022-Max-Drawdown |
|---|---|---|
| Original (10% Allokation, Limit 8) | -10,83% | -11,24% |
| Verbessert (5% Allokation, Limit 20) | **-9,25%** | **-10,49%** |

**Ergebnis: Der Diversifikations-Effekt bleibt erhalten, wird sogar leicht
begünstigt statt abgeschwächt.** Unter der kapitaleffizienteren Konfiguration
verliert RSI-2 in der Stress-Periode 2022 etwas **weniger** (-9,25% statt
-10,83%), nicht mehr — RSI-2 bleibt weiterhin klar negativ in genau der
Phase, in der die anderen Bots (Elliott Wave Aktien +81,44%, Elliott Wave
Krypto +21,20%, siehe Abschnitt 7b) am stärksten waren. Die
Diversifikationswirkung aus Abschnitt 7 ist also mit der getesteten
Kapital-Verbesserung kompatibel, keine gegenläufige Wirkung. Weder 9a noch
9b (reine Diagnose bzw. kein messbarer Effekt) berühren den
Diversifikations-Trade-off zusätzlich.

Rohdaten: `experiment_signal_priority_full.csv`, `experiment_signal_priority_oos.csv`.

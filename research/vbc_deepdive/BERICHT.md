# `volatility_breakout_crypto` — Vertiefungsstudie: Vol-Sizing × ATR-Trailing-Stop

**Status: reine Backtest-Untersuchung. KEINE Live-Aktivierung, KEINE Änderung an
Live-Dateien, KEINE Aktivierungsempfehlung.** Alle neuen Skripte liegen
ausschliesslich unter `research/vbc_deepdive/`. Verifiziert per `git status`:
keine Datei ausserhalb dieses Verzeichnisses wurde angefasst — insbesondere
nicht `strategies/volatility_breakout_crypto/live_params.py` oder
`forward_test.py`.

Anlass: Nach vier abgeschlossenen Backlog-Untersuchungen war
`volatility_breakout_crypto` der einzige Bot, der über **zwei unabhängig
erscheinende Mechanismen** positiv auffiel — volatilitäts-skalierte
Positionsgrössen (PR #18) und ATR-Trailing-Stops (PR #21). Diese Studie prüft,
ob es sich tatsächlich um zwei Signale handelt.

---

## Kurzfassung

**Die „doppelte Bestätigung" hält einer genauen Prüfung nicht stand. Es ist im
Wesentlichen ein Signal, zweimal gemessen — und dieses eine Signal ist keine
Ertragsverbesserung, sondern eine Varianzreduktion.**

Fünf voneinander unabhängige Belege, alle in dieser Studie neu erhoben:

1. **Die beiden „Volatilitäts"-Masse messen weitgehend dasselbe.** Korrelation
   zwischen ATR/Kurs und realisierter Volatilität am Einstiegszeitpunkt:
   **0,83** (Rangkorrelation 0,85) über 359 Trades.
2. **Die Trade-Beiträge beider Mechanismen sind positiv korreliert** (0,45 auf
   Trade-Ebene, 0,57 auf Quartalsebene) — nicht das Bild zweier unabhängiger
   Effekte.
3. **Die Kombination ist nicht additiv, sondern beim Risiko klar
   sub-additiv:** die Renditekosten stapeln sich vollständig (Interaktion
   +0,88 / −0,75 / +0,48 pp), die Drawdown-Reduktionen überlappen sich
   (Interaktion **−1,98 / −1,94 / −1,76 pp** in allen drei Perioden). Der
   zweite Mechanismus findet grösstenteils keinen Drawdown mehr vor, den der
   erste nicht schon entfernt hätte.
4. **Beide zeigen dasselbe bedingte Muster:** die Korrelation zwischen der
   Quartalsrendite der Baseline und dem Vorteil des Mechanismus im selben
   Quartal beträgt **−0,88** (Trailing) bzw. **−0,58** (Vol-Sizing). Der
   Trailing-Stop war in **10 von 10** Quartalen mit negativer Baseline besser
   und in nur 2 von 9 Quartalen mit positiver Baseline.
5. **Die kombinierte Variante ist nicht walk-forward-stabil:** gegenüber dem
   besseren Einzelmechanismus (Trailing) in 2 von 4 Fenstern besser, in 2 von 4
   schlechter. Über den Gesamtzeitraum ist sie sogar **schlechter** als der
   Trailing-Stop allein (Calmar 6,39 vs. 7,93).

Die Episoden-Prüfung (Frage 2 der Aufgabenstellung) fällt differenziert aus:
die **Drawdown-Reduktion** des Trailing-Stops ist robust (in 4 von 4
Walk-Forward-Fenstern vorhanden), der **Renditeeffekt** ist es in der Richtung
ebenfalls (besser in 12 von 19 Quartalen), aber in der Grössenordnung
konzentriert (die drei grössten Quartalsabweichungen sind alle Verluste und
tragen 55 % des Gesamtunterschieds — es sind exakt die drei stärksten
Trendquartale). Keine Handlungsempfehlung.

---

## 1. Baseline-Regressionscheck (zuerst, wie gefordert)

Diese Studie rechnet mit einem eigenen Kernmodul (`vbc_core.py`), das die
benötigten Funktionen aus den beiden Vorgänger-Studien als dokumentierte
Übernahme enthält. Grund: beide liegen in noch nicht gemergten Branches
(PR #18, PR #21); ein Import über Branch-Grenzen wäre nicht reproduzierbar.

Dass die Übernahme verhaltensgleich ist, wird nicht behauptet, sondern geprüft.
`verify_reference.py` bestätigt **50 von 50 Referenzwerten**:

| Quelle | geprüft | Ergebnis |
|---|---|---|
| `strategies/volatility_breakout_crypto/equity_simulation.py` (unverändert) | Trade-Anzahl, PnL-Summe, erster Entry / letzter Exit | 359 Trades, 629,88 % — **identisch** |
| `research/volatility_scaled_sizing/` (PR #18) | Baseline + Vol-Sizing, IS/OOS + 4 WF-Fenster | **alle exakt** |
| `research/trailing_stops/` (PR #21) | Baseline + ATR-Trailing, full/IS/OOS + 4 WF-Fenster, k, Trade-Anzahlen | **alle exakt** |

Belege im Detail: Baseline In-Sample 40,89 % / −16,77 %, Out-of-Sample
20,23 % / −11,33 %; Vol-Sizing 37,86 % / −15,17 % bzw. 16,20 % / −8,04 %;
ATR-Trailing 12,96 % / −5,76 % bzw. 28,12 % / −5,58 %; ATR-Multiplikator
k = 0,8956; 359 bzw. 396 Trades. Erst danach wurde irgendein neuer Vergleich
gerechnet.

---

## 2. Methodik

### Die vier Varianten (2 × 2)

| | feste Positionsgrösse | vol-skalierte Grösse |
|---|---|---|
| **fester 5 %-Stop** | **A** `baseline` | **B** `vol_sizing` |
| **ATR-Trailing-Stop** | **C** `trailing` | **D** `combined` |

Die Mechanismen greifen an unterschiedlichen Stellen an und sind technisch
unabhängig kombinierbar: der Stop bestimmt, **wann** geschlossen wird, die
Gewichtung, **wie gross** die Position war. Es gibt daher genau **zwei
Trade-Sätze** (fester Stop: 359 Trades / ATR-Trailing: 396 Trades), auf die
jeweils zwei Gewichtungen gelegt werden.

Dass der Trailing-Stop mehr Trades erzeugt, ist kein Fehler, sondern Folge der
Bot-Logik: der Bot kennt kein Pyramiding, der nächste Signalscan startet erst
nach dem Ausstieg. Frühere Ausstiege setzen also Kapazität für Folgesignale
frei (396 statt 359; 39 Trades existieren nur im Trailing-Satz, 2 nur im
Baseline-Satz).

### Unverändert übernommene Parameter (Aufgaben-Vorgabe Punkt 5)

| Parameter | Wert | Herkunft |
|---|---|---|
| ATR-Fenster | 14 Balken | `research/trailing_stops/` |
| ATR-Multiplikator `k` | 0,8956, kalibriert auf den Median der In-Sample-Baseline-Stop-Distanz | `research/trailing_stops/` |
| Vol-Fenster | 90 Balken | `research/volatility_scaled_sizing/` |
| Clip-Faktor | 4,0 (median-relativ) | `research/volatility_scaled_sizing/` |
| Gewichts-Normierung | Mittelwert exakt 1,0 innerhalb der jeweils ausgewerteten Periode | `research/volatility_scaled_sizing/` |
| `TRAIN_SPLIT_RATIO` | 0,7 | `multi_symbol_walk_forward.py` |
| Walk-Forward-Fenster | dieselben 4 chronologischen Fenster | `research/trailing_stops/` |
| Calmar | Gesamtrendite % / \|Max Drawdown %\| | alle vier Vorgänger-Studien |

**Es wurde kein einziger Parameter neu gesucht.** Diese Studie untersucht die
Interaktion zweier bereits definierter Mechanismen.

---

## 3. Getroffene Annahmen (vollständig)

1. **Vendoring statt Import.** Die benötigten Funktionen aus PR #18 und PR #21
   sind in `vbc_core.py` als dokumentierte Übernahme enthalten, jede mit
   Herkunftsangabe. Absicherung: der 50-Punkte-Regressionscheck oben. Ein
   Import über nicht gemergte Branch-Grenzen wäre nicht reproduzierbar; eine
   eigene Neufassung hätte die Vergleichbarkeit still zerstören können.
2. **Gewichte je Periode normiert** (Mittelwert 1,0 innerhalb IS, OOS, jedem
   WF-Fenster, jedem Quartal) — Konvention der Vol-Sizing-Studie, nötig um
   deren Zahlen exakt zu reproduzieren. Für die Trade-Ebenen-Analyse
   (Abschnitt 7) werden die Gewichte dagegen **über den Gesamtzeitraum**
   normiert, weil dort die Frage lautet, welche Trades den GESAMTeffekt
   tragen — dafür muss der Mechanismus über alle Trades derselbe sein.
   Beides ist im Ergebnis-JSON getrennt ausgewiesen.
3. **`k` einmalig auf den In-Sample-Baseline-Trades kalibriert** und unverändert
   für OOS, alle WF-Fenster und alle Quartale verwendet — unverändert aus der
   Trailing-Stop-Studie.
4. **Quartale als Episoden-Raster**, jedes als eigenständige Simulation ab
   10.000 gerechnet. Sonst hinge das Ergebnis eines Quartals vom Kapitalstand
   des Vorquartals ab und die Quartale wären untereinander nicht vergleichbar.
   Nebenwirkung, die genannt sein soll: die Quartalsrenditen verketten sich
   deshalb nicht exakt zum Gesamtzeitraum.
5. **Beitragsmasse in PnL-Prozentpunkten, nicht in Kapitaleinheiten.** Die
   Kapitalwirkung eines einzelnen Trades hängt vom Pfad ab (freies Kapital,
   Positionslimit) und liesse sich nicht sauber zurechnen. Die
   Prozentpunkt-Betrachtung ist die konservativere, weil sie keine Zurechnung
   behauptet, die die Simulation nicht hergibt.
6. **Renditen additiv im Log-Raum, Drawdown additiv in Prozentpunkten**
   (Abschnitt 5). Renditen verketten multiplikativ; der Max Drawdown ist ein
   einzelner Extremwert und keine verkettete Grösse.
7. **Rangkorrelation als Pearson-Korrelation der Ränge** berechnet — pandas'
   `method="spearman"` benötigt `scipy`, das im Projekt nicht installiert ist
   und für eine Backtest-Studie nicht neu eingeführt werden sollte.
8. **BTC-Regimefilter NICHT angewendet.** `live_params.py` führt
   `BTC_REGIME_FILTER_ENABLED = True`, die bot-eigene `equity_simulation.py`
   wendet ihn aber nicht an (nur `forward_test.py` tut das). Beide
   Vorgänger-Studien sind der `equity_simulation.py` gefolgt; diese Studie tut
   es ebenfalls, sonst wäre der Regressionscheck unmöglich. Der Filter wirkt
   nur auf Einstiege und damit in allen vier Varianten gleich.
9. **Schwelle 60 %** für „durch eine Einzelepisode getrieben" — dieselbe
   dokumentierte Heuristik wie in der Trailing-Stop-Studie. Zusätzlich wird
   der Anteil der drei grössten Quartale ausgewiesen, weil eine Konzentration
   auf wenige Episoden auch dann vorliegen kann, wenn kein einzelnes Quartal
   die Schwelle reisst.

---

## 4. Frage 1 — Kombinationseffekt: alle vier Varianten

Rendite % / Max Drawdown % / **Calmar**:

| Periode | A Baseline | B Vol-Sizing | C Trailing | D Kombiniert |
|---|---|---|---|---|
| **Gesamtzeitraum** | 71,26 / −16,77 / **4,25** | 61,09 / −14,96 / **4,08** | 45,65 / −5,76 / **7,93** | 37,88 / −5,93 / **6,39** |
| **In-Sample** | 40,89 / −16,77 / **2,44** | 37,86 / −15,17 / **2,50** | 12,96 / −5,76 / **2,25** | 9,78 / −6,10 / **1,60** |
| **Out-of-Sample** | 20,23 / −11,33 / **1,79** | 16,20 / −8,04 / **2,01** | 28,12 / −5,58 / **5,04** | 24,31 / −4,05 / **6,00** |

**Antwort: die Kombination wirkt weder additiv noch klar gegenläufig, sondern
überlagernd — mit einem Ergebnis, das je nach Periode kippt.**

- **Gesamtzeitraum und In-Sample: die Kombination ist schlechter als der beste
  Einzelmechanismus** (6,39 vs. 7,93 bzw. 1,60 vs. 2,50). Der zweite
  Mechanismus kostet dort zusätzliche Rendite, ohne noch nennenswert Drawdown
  zu finden.
- **Out-of-Sample: die Kombination ist besser als jeder Einzelmechanismus**
  (6,00 vs. 5,04 und 2,01) — allein durch den Drawdown (−5,58 % → −4,05 %),
  bei niedrigerer Rendite (28,12 % → 24,31 %).

Nebenbefund zum Vol-Sizing allein: dessen in PR #18 berichteter Vorteil
(Calmar besser IS *und* OOS) ist real, aber klein — und **über den
Gesamtzeitraum kehrt er sich um** (4,25 → 4,08). Der Gesamtzeitraum war in
PR #18 nicht ausgewiesen; das ist kein Widerspruch zu jener Studie, aber ein
relativierender Zusatz.

### Additivitätsrechnung

Erwartung bei rein additiver Wirkung gegenüber dem tatsächlichen kombinierten
Ergebnis:

| Periode | Rendite erwartet → tatsächlich | Interaktion | Drawdown erwartet → tatsächlich | Interaktion |
|---|---|---|---|---|
| Gesamtzeitraum | 37,00 % → 37,88 % | **+0,88 pp** | −3,95 % → −5,93 % | **−1,98 pp** |
| In-Sample | 10,53 % → 9,78 % | **−0,75 pp** | −4,16 % → −6,10 % | **−1,94 pp** |
| Out-of-Sample | 23,83 % → 24,31 % | **+0,48 pp** | −2,29 % → −4,05 % | **−1,76 pp** |

**Das ist der präziseste Einzelbefund dieser Studie:** die **Renditekosten
stapeln sich praktisch vollständig** (Interaktion im Rauschbereich, ±1 pp),
die **Drawdown-Reduktionen überlappen sich deutlich** (in allen drei Perioden
rund 2 Prozentpunkte weniger Wirkung als bei Unabhängigkeit zu erwarten wäre).

Man zahlt beide Mechanismen voll und bekommt ihren Schutz nur einmal — genau
das erwartet man, wenn beide gegen dieselben Ereignisse schützen.

---

## 5. Frage 2 — Episoden-Robustheit (quartalsweise)

Die laut Aufgabenstellung wichtigste Frage. Renditedifferenz gegenüber der
Baseline, je Quartal, in Prozentpunkten:

| Quartal | Baseline | Vol-Sizing | Trailing | Kombiniert |
|---|---|---|---|---|
| 2022Q1 | +3,26 % | −1,33 | −0,93 | −0,25 |
| 2022Q2 | −1,06 % | ±0,00 | **+1,11** | +0,95 |
| 2022Q3 | −9,21 % | ±0,00 | **+6,29** | +6,24 |
| 2022Q4 | −6,00 % | −0,51 | **+4,69** | +4,72 |
| 2023Q1 | +15,72 % | −0,42 | **−11,29** | −11,00 |
| 2023Q2 | −3,61 % | +1,55 | **+4,38** | +4,35 |
| 2023Q3 | −3,23 % | +0,34 | +0,17 | +0,64 |
| 2023Q4 | +5,33 % | +1,96 | −0,42 | −1,44 |
| 2024Q1 | +23,45 % | −9,42 | **−24,43** | −25,46 |
| 2024Q2 | −1,87 % | +2,16 | **+2,92** | +3,91 |
| 2024Q3 | −3,52 % | −0,08 | **+5,54** | +4,44 |
| 2024Q4 | +22,35 % | +0,40 | **−22,06** | −21,29 |
| 2025Q1 | −4,17 % | ±0,00 | +1,53 | +1,56 |
| 2025Q2 | +3,23 % | −1,33 | **+6,42** | +4,68 |
| 2025Q3 | +16,11 % | −2,20 | −1,18 | −5,08 |
| 2025Q4 | −2,11 % | ±0,00 | +1,01 | +0,86 |
| 2026Q1 | −3,29 % | +1,02 | **+2,97** | +2,88 |
| 2026Q2 | +8,35 % | −4,35 | −3,03 | −4,86 |
| 2026Q3 | +1,40 % | −0,38 | **+4,96** | +6,72 |

**Richtung: breit verteilt.** Der Trailing-Stop ist in **12 von 19 Quartalen**
besser, in 7 schlechter. Kein einzelnes Quartal reisst die 60-%-Schwelle
(grösstes: 2024Q1 mit 23,2 % des Gesamtunterschieds).

**Grössenordnung: konzentriert.** Die drei grössten Quartalsabweichungen
(2024Q1 −24,43, 2024Q4 −22,06, 2023Q1 −11,29) tragen **54,9 %** des gesamten
absoluten Unterschieds — und **alle drei sind Verluste**, in genau den drei
stärksten Aufwärtsquartalen. Das Profil ist also: **viele kleine Gewinne,
wenige grosse Verluste.**

**Drawdown-Reduktion: robust.** Anders als der Renditeeffekt ist sie in
**allen vier** Walk-Forward-Fenstern vorhanden:

| Fenster | Baseline | Vol-Sizing | Trailing | Kombiniert |
|---|---|---|---|---|
| W1 2022-03 … 2023-04 | −16,77 % | −15,63 % | −4,87 % | −4,29 % |
| W2 2023-04 … 2024-06 | −6,68 % | −6,44 % | −5,43 % | −5,56 % |
| W3 2024-06 … 2025-07 | −11,48 % | −10,35 % | −3,20 % | −2,87 % |
| W4 2025-07 … 2026-08 | −11,33 % | −7,83 % | −5,58 % | −3,91 % |

Das ist der belastbarste positive Einzelbefund der Studie: die
Drawdown-Reduktion des Trailing-Stops ist **kein Einzelepisoden-Artefakt**.

### Die bedingte Struktur — der eigentliche Kern

| Variante | Korrelation mit der Baseline-Quartalsrendite | Baseline negativ (10 Q) | Baseline positiv (9 Q) |
|---|---|---|---|
| Vol-Sizing | **−0,58** | +0,45 pp, besser in 40 % | −1,90 pp, besser in 22 % |
| Trailing | **−0,88** | **+3,06 pp, besser in 100 %** | −5,77 pp, besser in 22 % |
| Kombiniert | **−0,91** | +3,06 pp, besser in 100 % | −6,44 pp, besser in 22 % |

Der Trailing-Stop war in **jedem einzelnen** der zehn Quartale besser, in denen
die Baseline verlor, und in nur zwei der neun Quartale, in denen sie gewann.
Vol-Sizing zeigt dasselbe Muster, nur schwächer.

**Das ist kein zusätzlicher Ertrag, sondern eine Versicherung:** sie zahlt,
wenn es schlecht läuft, und kostet Prämie, wenn es gut läuft. Ob das erwünscht
ist, ist eine Präferenzfrage und keine Backtest-Frage — sie liegt beim Nutzer.

---

## 6. Frage 3 — Mechanismus-Unabhängigkeit

### Messen die beiden Mechanismen überhaupt Verschiedenes?

Formal ja: der ATR-Stop nutzt die **True Range** (Hoch/Tief/Vorschluss,
14 Balken), das Vol-Sizing die **Standardabweichung der
Schluss-zu-Schluss-Log-Returns** (90 Balken). Unterschiedliches Mass,
unterschiedliches Fenster.

Empirisch kaum: über die 359 Baseline-Trades korrelieren ATR/Kurs und
realisierte Volatilität am Einstiegszeitpunkt mit **0,83** (Rangkorrelation
**0,85**). Die beiden „Volatilitäten" sind praktisch dieselbe Information.

### Wirken sie auf dieselben Trades?

357 der 359 Baseline-Trades kommen auch im Trailing-Satz vor (gleiches Symbol,
gleicher Einstiegszeitpunkt) und sind damit direkt vergleichbar.

| Kennzahl | Wert |
|---|---|
| Korrelation der Trade-Beiträge | **+0,45** |
| Korrelation der Quartalsbeiträge | **+0,57** |
| beide halfen demselben Trade | 149 × |
| beide schadeten demselben Trade | 49 × |
| gegenläufig | 159 × |
| Überlappung der 20 grössten Beiträge | **0** (bei Unabhängigkeit erwartet: 1,12) |
| Summe Vol-Sizing-Beitrag | **−40,72 pp** |
| Summe Trailing-Beitrag | **−380,82 pp** |

**Das Bild ist zweigeteilt und beide Hälften sind wichtig:**

- **In der Breite überlappen sich die Mechanismen deutlich** (Korrelation
  +0,45 bzw. +0,57, 149 gemeinsam verbesserte Trades). Das ist erwartbar,
  wenn beide auf dieselbe Eingangsgrösse reagieren.
- **An den Extremen sind sie disjunkt** (0 Überlappung unter den 20 grössten
  Beiträgen, weniger als der Zufallserwartungswert). Die grössten Einzelbeiträge
  stammen also tatsächlich aus verschiedenen Trades.

Der zweite Punkt spricht für eine gewisse Rest-Unabhängigkeit. Er wiegt aber
den ersten nicht auf, und vor allem: **beide Beitragssummen sind negativ.**
Auf Ebene der PnL-Prozentpunkte reduzieren beide Mechanismen den Gesamtertrag
(−40,7 bzw. −380,8 pp). Ihr gesamter Calmar-Nutzen stammt aus der
Drawdown-Seite — und genau dort sind sie, wie Abschnitt 4 zeigt,
sub-additiv.

Zusätzlich wirkt Vol-Sizing bei diesem Bot **auch über die Trade-Auswahl**,
nicht nur über die Grösse: die kombinierte Variante führt 367 statt 370 Trades
aus, weil grössere Einzelpositionen gelegentlich das freie Kapital erschöpfen
(in `test_vbc_core.py` als eigener Check nachgewiesen). Ein kleiner, aber
realer Nebenkanal, der die beiden Mechanismen weiter verkoppelt.

---

## 7. Frage 4 — Walk-Forward-Prüfung der kombinierten Variante

Calmar-Ratio, dieselben 4 Fenster wie in der Trailing-Stop-Studie:

| Fenster | A Baseline | B Vol-Sizing | C Trailing | D Kombiniert | D besser als C? |
|---|---|---|---|---|---|
| W1 2022-03 … 2023-04 | −0,20 | −0,23 | 0,71 | **1,11** | ja |
| W2 2023-04 … 2024-06 | 3,85 | 3,30 | 0,04 | **−0,16** | nein |
| W3 2024-06 … 2025-07 | 3,32 | 3,85 | 6,10 | **5,52** | nein |
| W4 2025-07 … 2026-08 | 0,17 | 0,00 | 3,14 | **4,20** | ja |

**Die kombinierte Variante ist gegenüber der Baseline in 3 von 4 Fenstern
besser** (nur W2 nicht) — das entspricht dem Bild des Trailing-Stops allein.

**Gegenüber dem besseren Einzelmechanismus ist sie nicht stabil: 2 von 4.**
Nach der in den Vorgänger-Studien verwendeten 3-von-4-Regel ist der
Zusatznutzen der Kombination damit **nicht walk-forward-stabil**. Das deckt
sich mit dem Gesamtzeitraum-Ergebnis (6,39 vs. 7,93 zugunsten des
Trailing-Stops allein) und widerspricht dem Out-of-Sample-Ergebnis (6,00 vs.
5,04). Der OOS-Vorteil der Kombination ist also ein Einzelbefund, kein Muster.

Nebenbefund zum Vol-Sizing allein: unter dem hier durchgehend verwendeten
**Calmar-Kriterium** ist es nur in **1 von 4** Fenstern besser als die
Baseline (W3). PR #18 hat diesen Bot als walk-forward-stabil eingestuft — dort
allerdings anhand der **Drawdown-Richtung** (3 von 4 Fenstern gleich oder
besser), was ebenfalls zutrifft und hier bestätigt wird (sogar 4 von 4). Kein
Widerspruch, sondern ein Kriterienunterschied — der aber zeigt, wie viel von
der ursprünglichen Einstufung am gewählten Kriterium hängt.

---

## 8. Trade-Profil aller vier Varianten (Gesamtzeitraum)

| Variante | Trades | ausgeführt | Win Rate | Ø PnL | schlechtester | bester |
|---|---|---|---|---|---|---|
| A Baseline | 359 | 310 | 26,5 % | +1,755 % | −5,30 % | **+174,10 %** |
| B Vol-Sizing | 359 | 310 | 26,5 % | +1,755 % | −5,30 % | +174,10 % |
| C Trailing | 396 | 370 | **43,4 %** | +1,074 % | **−9,00 %** | **+40,78 %** |
| D Kombiniert | 396 | 367 | 43,4 % | +1,074 % | −9,00 % | +40,78 % |

A und B teilen sich naturgemäss das Trade-Profil (Vol-Sizing ändert nur die
Positionsgrösse, nicht die Trades), ebenso C und D.

Das bereits in der Trailing-Stop-Studie beschriebene Muster bestätigt sich:
Win Rate steigt deutlich (26,5 % → 43,4 %), der durchschnittliche Gewinn je
Trade sinkt trotzdem (+1,76 % → +1,07 %), der grösste Gewinner wird von
+174 % auf +41 % gekappt, und der grösste Einzelverlust wächst von −5,3 % auf
−9,0 % (die ATR-Stop-Distanz ist bei identischem Median rechtsschief verteilt).

---

## 9. Die zentrale Frage: zwei Signale oder eines, zweimal gemessen?

**Ehrliche Antwort: im Wesentlichen eines, zweimal gemessen.**

Dafür sprechen vier Befunde, jeder für sich schon deutlich:

1. **Gemeinsame Eingangsgrösse.** Die beiden Volatilitätsmasse korrelieren mit
   0,83 — sie sind praktisch dieselbe Information in zwei Verpackungen.
2. **Gemeinsame Wirkungsrichtung.** Beide zeigen dasselbe bedingte Muster
   (Korrelation mit der Baseline-Quartalsrendite −0,88 bzw. −0,58): sie helfen
   in Verlustphasen und kosten in Gewinnphasen.
3. **Überlappende, nicht additive Wirkung.** Die Renditekosten stapeln sich
   vollständig, die Drawdown-Reduktion nicht (rund −2 pp Interaktion in jeder
   Periode). Zwei unabhängige Verbesserungen sähen anders aus.
4. **Keine stabile Kombinationsdividende.** Die Kombination schlägt den
   besseren Einzelmechanismus in nur 2 von 4 Fenstern und über den
   Gesamtzeitraum gar nicht.

Dagegen spricht ein einziger, aber ernstzunehmender Befund: **die grössten
Einzelbeiträge stammen aus disjunkten Trades** (0 von 20 überlappend, unter
der Zufallserwartung). Es gibt also eine Rest-Unabhängigkeit an den Rändern.

Die faire Zusammenfassung lautet daher nicht „identisch", sondern: **stark
überlappend, mit einem kleinen unabhängigen Rest — und die Überlappung liegt
genau dort, wo der Nutzen entsteht (Drawdown), während die Unabhängigkeit
dort liegt, wo sie nichts einbringt (einzelne Extremtrades).**

Und noch eine Ebene tiefer: **das eine Signal, das hier zweimal gemessen wird,
ist gar keine Ertragsverbesserung.** Beide Mechanismen senken den summierten
PnL (−40,7 bzw. −380,8 Prozentpunkte) und die Gesamtrendite (71,26 % → 61,09 %
bzw. → 45,65 %). Der gesamte Calmar-Gewinn kommt aus dem Nenner. Die beiden
Untersuchungen haben also nicht zweimal einen Edge bestätigt, sondern zweimal
dieselbe Varianzreduktion gemessen.

---

## 10. Gesamteinschätzung (unaufgeregt, ohne Handlungsempfehlung)

Der Anlass dieser Studie war die Vermutung, `volatility_breakout_crypto` sei
über zwei unabhängige Wege als verbesserbar bestätigt. Nach genauerer
Betrachtung ist diese Lesart nicht haltbar: die beiden Mechanismen greifen auf
dieselbe Grösse zu, wirken in dieselbe Richtung, schützen vor denselben
Ereignissen und liefern kombiniert keinen stabilen Zusatznutzen.

Was nach dieser Prüfung übrig bleibt, ist schmaler, aber solider als die
ursprüngliche Lesart:

- **Der ATR-Trailing-Stop senkt bei diesem Bot den Drawdown robust** — in
  4 von 4 Walk-Forward-Fenstern, nicht nur in einer Episode. Das ist der
  belastbarste Einzelbefund.
- **Er kostet dafür Rendite** (71,26 % → 45,65 % über den Gesamtzeitraum),
  konzentriert auf die stärksten Trendquartale, und vergrössert den grössten
  Einzelverlust.
- **Vol-Sizing tut dasselbe, nur schwächer** und mit einem Vorteil, der über
  den Gesamtzeitraum verschwindet.
- **Die Kombination lohnt sich nicht** gegenüber dem Trailing-Stop allein:
  über den Gesamtzeitraum schlechter, Out-of-Sample besser, walk-forward
  nicht stabil.

Ob eine Varianzreduktion, die im Mittel Rendite kostet, für dieses Portfolio
erwünscht ist, ist keine Backtest-Frage — der Backtest kann nur zeigen, dass
es sich um genau diesen Tausch handelt und nicht um einen zusätzlichen Edge.
Diese Entscheidung liegt bewusst beim Nutzer in einer separaten, künftigen
Session.

---

## 11. Explizit ausserhalb des Scopes

Jede Untersuchung anderer Bots, jede Live-Code-Änderung, jede
Aktivierungsempfehlung, jede neue Parameter-Optimierung der bereits gewählten
Fenstergrössen (ATR-14, Vol-90, Clip 4,0, k = 0,8956 — alle unverändert
übernommen).

## 12. Offene Fragen für eine mögliche Vertiefung

- Die Rest-Unabhängigkeit an den Extremen (0 von 20 überlappende Top-Beiträge)
  ist der einzige Befund, der für zwei Signale spricht. Eine gezielte
  Betrachtung genau dieser Trades könnte klären, ob dahinter ein Mechanismus
  steckt oder nur Stichprobenrauschen bei 357 Trades.
- Der BTC-Regimefilter ist hier bewusst deaktiviert (Annahme 8), im Live-Betrieb
  aber aktiv. Da er ebenfalls ein Risikoreduktions-Mechanismus mit
  Renditekosten ist, wäre die Frage nach seiner Überlappung mit den beiden hier
  untersuchten Mechanismen die naheliegende Fortsetzung — und zugleich der
  Anlass, die Divergenz zwischen `live_params.py` und `equity_simulation.py`
  einmal grundsätzlich zu klären.
- Die Drawdown-Sub-Additivität von rund −2 pp ist über alle drei Perioden
  bemerkenswert konstant. Ob das ein Zufall dieses Datensatzes ist oder eine
  strukturelle Eigenschaft überlappender Risikomechanismen, liesse sich nur
  bot-übergreifend beantworten — was hier ausserhalb des Scopes lag.

---

## 13. Reproduzierbarkeit

```
cd research/vbc_deepdive
python3 test_vbc_core.py        # 34 Sanity-Checks der kombinierten Logik
python3 verify_reference.py     # 50 Referenzwerte beider Vorgaenger-Studien
python3 run_deepdive.py         # vollstaendige Analyse, schreibt results/
```

Alle Läufe lesen ausschliesslich die vorhandenen CSVs in `data/` — kein
Netzwerkzugriff, keine zusätzliche Abhängigkeit (kein `scipy`).

| Datei | Inhalt |
|---|---|
| `vbc_core.py` | ATR/Trailing, realisierte Volatilität, inverse Vol-Gewichte, gewichtete Portfolio-Simulation, Kennzahlen — jede Funktion mit Herkunftsangabe |
| `verify_reference.py` | Regressionscheck gegen den Bot-Code und beide Vorgänger-Studien |
| `test_vbc_core.py` | 34 Sanity-Checks, Schwerpunkt kombinierte Logik |
| `run_deepdive.py` | 2×2-Varianten, IS/OOS, 4 WF-Fenster, Quartale, Additivität, bedingte Struktur, Trade-Überlappung |
| `results/vbc_deepdive.json` | alle Ergebnisse maschinenlesbar |
| `results/trades_static_stop.csv`, `results/trades_atr_trailing.csv` | die beiden Trade-Sätze auf Trade-Ebene |

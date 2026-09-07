# Volatilitäts-kalibrierte Trailing-Stops — Backtest-Only-Untersuchung

**Status: reine Backtest-Untersuchung. KEINE Live-Aktivierung, KEINE Änderung an
Live-Dateien.** Alle neuen Skripte liegen ausschliesslich unter
`research/trailing_stops/`. Verifiziert per `git status`: keine Datei ausserhalb
dieses neuen Verzeichnisses wurde angefasst. Keine Handlungsempfehlung.

Letzter der vier Backlog-Punkte zur Profitabilitäts-Untersuchung (nach
Vol-Sizing, HRP, Trend-Overlay — PRs #18–#20). Die Untersuchung lief
unbeaufsichtigt; alle Stellen, an denen eine Festlegung nötig war, sind unten
im Abschnitt „Getroffene Annahmen" vollständig aufgeführt.

---

## 0. Entscheidungsgrundlage

*Nachgetragen. Die erste Fassung berichtete Punktschätzer ohne Aussenreferenz
und ohne Unsicherheitsmass — gut genug, um zu beschreiben, WAS gemessen wurde,
aber nicht, um darauf eine Entscheidung zu stützen. Der Nachtrag korrigiert
eine Aussage der ersten Fassung (siehe „Was sich geändert hat" am Ende dieses
Abschnitts).*

### Datenbasis je Bot

| Bot | Kerzen | Zeitraum | Jahre | Symbole | Trades gefunden → **ausgeführt** |
|---|---|---|---|---|---|
| `elliott_wave` | 1h | 2021-09 … 2026-08 | 4,97 | 18 | 783 → **780** |
| `elliott_wave_stocks` | 1d | 2016-10 … 2026-09 | 9,85 | 138 | 519 → **288** |
| `t3_supertrend` | 4h | 2021-09 … 2026-08 | 4,99 | 18 | 980 → **656** |
| `volatility_breakout` | 1d | 2016-09 … 2026-09 | 10,0 | 147 | 4510 → **1454** |
| `volatility_breakout_crypto` | 1d | 2022-03 … 2026-08 | 4,45 | 20 | 359 → **310** |

Die Spalte „ausgeführt" fehlte in der ersten Fassung und ist wichtiger, als sie
aussieht: bei `volatility_breakout` werden **68 % aller gefundenen Signale
mangels freien Kapitals oder wegen `MAX_CONCURRENT_POSITIONS` verworfen**, bei
`elliott_wave_stocks` 45 %. Welche Signale das trifft, hängt an der Reihenfolge
gleichzeitiger Einstiege — siehe 0.3.

Out-of-Sample-Stichproben (ausgeführte Trades): `t3_supertrend` 210 ·
`volatility_breakout` 456 · `volatility_breakout_crypto` **103**. Die
Krypto-Bots decken jeweils nur **einen einzigen Marktzyklus** ab.

### 0.1 Buy-and-Hold — der fehlende Pflicht-Gegencheck

Die erste Fassung hat den Buy-and-Hold-Vergleich **bewusst weggelassen und das
begründet** (Annahme 12: die Zahl ist für alle drei Stop-Varianten dieselbe und
trägt zur *internen* Frage nichts bei). Das Argument stimmt weiterhin — der
Vergleich der Varianten untereinander wird davon nicht berührt.

Trotzdem war die Auslassung ein Fehler, und zwar aus einem Grund, den die
Begründung nicht abdeckt: Buy-and-Hold beantwortet nicht die interne Frage,
sondern die vorgelagerte — **trägt die Ausgangsbasis überhaupt?** Bei einem der
fünf Bots lautet die Antwort nein, und das war ohne diese Zahl nicht sichtbar.

Nachgetragen über eine
gemeinsame Implementierung, die gegen die drei Bots mit eigenem
`buy_and_hold_benchmark.py` **exakt** geprüft ist (`verify_baseline.py`).
Gleichgewichtet über alle Symbole, auf den jeweiligen Trade-Zeitraum
zugeschnitten.

| Bot | Baseline (Gesamtzeitraum) | **Buy-and-Hold** | Urteil |
|---|---|---|---|
| `t3_supertrend` | 129,64 / −22,20 / **5,84** | 8,42 / −79,93 / **0,11** | Strategie klar besser |
| `volatility_breakout_crypto` | 71,26 / −16,77 / **4,25** | 19,45 / −67,90 / **0,29** | Strategie klar besser |
| `volatility_breakout` | 224,41 / −23,97 / **9,36** | **804,93 / −34,81 / 23,12** | **Buy-and-Hold besser** |
| `elliott_wave_stocks` * | 3084,09 / −9,79 / 315,02 | 768,39 / −35,10 / 21,89 | nicht interpretierbar |
| `elliott_wave` * | 2162,06 / −1,83 / 1181,45 | −1,60 / −78,97 / −0,02 | nicht interpretierbar |

**Der wichtigste Einzelbefund dieses Nachtrags:** bei `volatility_breakout`
hätte stumpfes Halten der 147 Aktien über denselben Zeitraum eine **2,5-mal
bessere Calmar-Ratio** erzielt als die Strategie (23,12 vs. 9,36) — bei
3,6-facher Rendite. Das entwertet den *internen* Vergleich der drei
Stop-Varianten nicht, stellt aber die Ausgangsbasis in Frage, auf der er
stattfindet. Es passt zum bereits dokumentierten Survivorship-Bias-Problem des
Aktien-Universums (Übergabeprotokoll, Abschnitt 3.3).

Bei beiden Krypto-Bots gewinnt die Strategie dagegen deutlich — und zwar über
den Drawdown (−22,20 % gegen −79,93 % bei `t3_supertrend`). Out-of-Sample
liegt Buy-and-Hold bei **allen fünf** Bots bei der Rendite vorn.

### 0.2 Belastbarkeit — Block-Bootstrap

2000 Replikate, zirkulärer Moving-Block-Bootstrap über Kalendermonate
(Blocklänge 3), gepaart: alle Varianten je Replikat auf derselben gezogenen
Zeitachse. Ein Bootstrap über einzelne Trades wäre falsch — die Simulation ist
pfadabhängig und der Max Drawdown eine Eigenschaft der Reihenfolge. Nur für
die drei auswertbaren Bots gerechnet.

P(ATR-Trailing besser als Baseline), Gesamtzeitraum / In-Sample / Out-of-Sample:

| Bot | **Calmar** | **Drawdown** | Rendite |
|---|---|---|---|
| `t3_supertrend` | **2,4 % / 3,1 % / 20,1 %** | 75,5 % / 71,2 % / 91,7 % | 2,5 % / 3,9 % / 18,1 % |
| `volatility_breakout` | **63,2 % / 74,1 % / 33,4 %** | 43,5 % / 45,1 % / 36,0 % | 67,1 % / 78,1 % / 34,2 % |
| `volatility_breakout_crypto` | 73,8 % / 48,8 % / **95,0 %** | **100,0 % / 99,9 % / 99,2 %** | 35,5 % / 26,0 % / 70,7 % |

Drei klar unterschiedliche Bilder:

- **`t3_supertrend`: der negative Befund ist belastbar.** P = 2,4 % heisst, in
  97,6 % der Replikate ist die ATR-Variante schlechter. Die Verschlechterung
  ist damit das statistisch bestgesicherte Ergebnis dieser Untersuchung.
- **`volatility_breakout`: der Befund ist NICHT belastbar** — und das
  korrigiert die erste Fassung. Dort stand „Verbesserung: nein"; tatsächlich
  liegt P bei 63 % (Gesamtzeitraum) und 74 % (In-Sample), also mehrheitlich
  auf der *anderen* Seite als der Punktschätzer. Nur Out-of-Sample zeigt die
  gleiche Richtung wie der Punktschätzer (33,4 %). **Das Vorzeichen ist von
  den Daten nicht bestimmt.**
- **`volatility_breakout_crypto`: die Drawdown-Reduktion ist praktisch sicher**
  (P ≥ 99,2 % in jeder Periode), die Calmar-Verbesserung nur Out-of-Sample
  grenzwertig (95,0 %, Intervall −0,56 … 16,14 berührt die Null).

Ein Muster über alle drei: **die Drawdown-Wirkung lässt sich viel klarer
beziffern als die Calmar-Wirkung.** Der Grund ist nicht Messfehler, sondern
Substanz — die Rendite sinkt ähnlich verlässlich wie der Drawdown, und welcher
Effekt in der Ratio überwiegt, hängt stark von der gezogenen
Marktphasen-Mischung ab.

**Wichtige Einschränkung zum Verfahren:** der Bootstrap würfelt die Abfolge der
Marktphasen neu. Er beantwortet „wie sähe es in einer anders zusammengesetzten
Historie derselben Phasen aus", nicht „wie sicher ist der Wert der
tatsächlichen Historie". Bei `volatility_breakout` weichen Punktschätzer und
Bootstrap-Mehrheit gerade deshalb voneinander ab — die tatsächliche Abfolge ist
eine, in der die ATR-Variante schlechter abschneidet, viele gleichwertige
Abfolgen sind es nicht.

### 0.3 Belastbarkeit — Reihenfolge gleichzeitiger Einstiege

Die Simulation vergibt Kapital sequenziell. Sind Kapital oder Positionslimit
knapp, entscheidet die Reihenfolge innerhalb desselben Zeitstempels, **welcher
Trade überhaupt ausgeführt wird**. Diese Reihenfolge ist inhaltlich willkürlich.
500 Permutationen, Gesamtzeitraum, Calmar-Spanne:

| Bot | geteilte Zeitstempel | Baseline | Fix-Trailing | ATR-Trailing | überlappen? |
|---|---|---|---|---|---|
| `t3_supertrend` | 43,8 % | 4,72 … 6,40 | 0,56 … 1,40 | −0,51 … 0,13 | **nein** |
| `volatility_breakout` | **87,7 %** | 4,35 … 15,77 | 4,93 … 14,40 | 2,64 … 11,51 | **ja, fast vollständig** |
| `volatility_breakout_crypto` | 59,6 % | 2,98 … 4,90 | 5,37 … 7,42 | 6,65 … 8,95 | **nein** |

Bei `volatility_breakout` (87,7 % geteilte Zeitstempel, grösste Gruppe **24
Trades an einem Tag**) schwankt die Baseline-Calmar allein durch diese
Willkür zwischen 4,35 und 15,77 — ein Faktor von 3,6. Der berichtete
Unterschied zur ATR-Variante (9,36 → 6,04) liegt vollständig innerhalb dieser
Spanne. Bootstrap und Permutationstest kommen hier also unabhängig zum selben
Schluss.

Bei den beiden anderen Bots überlappen die Spannen nicht — dort übersteht die
Kernaussage diese Störung.

Der **Drawdown ist gegenüber der Reihenfolge weitgehend stabil** (z. B.
`volatility_breakout_crypto` Baseline: exakt −16,77 % in allen 500
Permutationen). Erneut dieselbe Trennlinie wie beim Bootstrap.

### 0.4 Was den Befund umstossen würde

- Ein **zweiter vollständiger Marktzyklus** für die Krypto-Bots (aktuell nur
  einer). Die Trendphasen, in denen der Trailing-Stop verliert, sind dieselben,
  die diese Bots profitabel machen.
- Eine **andere Kapitalkonfiguration**: die Reihenfolge-Empfindlichkeit
  entsteht nur, weil Kapital und Positionslimit knapp sind. Bei
  `volatility_breakout` werden 68 % der Signale verworfen — eine kleinere
  Positionsgrösse würde das Bild grundlegend ändern.
- Für `volatility_breakout_crypto`: eine **Aktivierung des BTC-Regimefilters**
  in der Backtest-Kette (siehe Annahme 8) — ebenfalls ein
  Risikoreduktions-Mechanismus, der mit dem Trailing-Stop überlappen dürfte.

### 0.5 Was sich gegenüber der ersten Fassung geändert hat

| | erste Fassung | nach dem Nachtrag |
|---|---|---|
| `t3_supertrend` | Verbesserung: **nein**, WF-stabil ja | unverändert — und jetzt statistisch belegt (P = 2,4 %) |
| `volatility_breakout` | Verbesserung: **nein**, WF-stabil ja | **korrigiert: Vorzeichen nicht bestimmt** (P = 63 % / 74 % / 33 %; Reihenfolge-Spannen überlappen fast vollständig) |
| `volatility_breakout_crypto` | Verbesserung: **unklar** | unverändert — Drawdown-Wirkung jetzt als praktisch sicher belegt (P ≥ 99,2 %) |
| Buy-and-Hold | bewusst ausgelassen (Annahme 12, begründet) | ergänzt; bei `volatility_breakout` schlägt B&H die Strategie risikoadjustiert um das 2,5-Fache |
| Stichprobengrössen | fehlten | ergänzt, inkl. Anteil verworfener Signale |

Die Gesamteinschätzung in Abschnitt 11 ist entsprechend angepasst.

---

## Kurzfassung

Von den 9 Bots haben **5 einen festen Prozent-Stop-Loss** und sind damit
Gegenstand dieser Untersuchung; 1 Bot hat einen strukturellen Stop und 3 Bots
haben bewusst gar keinen — diese 4 wurden dokumentiert, aber nicht angefasst
(vollständige Bestandsaufnahme siehe Abschnitt 1).

Von den 5 untersuchten Bots sind **2 (beide Elliott-Wave-Bots) für genau diese
Fragestellung methodisch nicht auswertbar**: ihr Backtest steigt zum
Zigzag-Wellenende ein, dem per Konstruktion rückwirkend garantiert eine
Aufwärtsbewegung folgt. Ein Trailing-Stop verwandelt genau diesen bereits
bekannten Look-Ahead in einen quasi-sicheren Gewinn (Gewinnraten 98,7 % bzw.
99,4 %, Drawdowns nahe 0). Das ist ein Befund über den *Backtest*, nicht über
Trailing-Stops — Details und Belege in Abschnitt 5.4.

Bei den **3 belastbar auswertbaren Bots** ergibt sich ein konsistentes Bild:

| Bot | Calmar Baseline → ATR-Trailing (IS / OOS) | Bewertung | WF-stabil | belastbar? |
|---|---|---|---|---|
| `t3_supertrend` | 4,51 → −0,07 / 0,85 → −0,05 | **nein** (deutlich schlechter) | ja (4/4) | **ja** (P = 2,4 %) |
| `volatility_breakout` | 4,00 → 3,44 / 5,46 → 2,04 | Punktschätzer: nein | ja (3/4) | **nein — Vorzeichen unbestimmt** |
| `volatility_breakout_crypto` | 2,44 → 2,25 / 1,79 → 5,04 | **unklar** (IS leicht schlechter, OOS klar besser) | ja (3/4) | Drawdown ja, Calmar nur OOS |

**In einem Satz:** Volatilitäts-kalibrierte Trailing-Stops senken bei den beiden
trendfolgenden bzw. trendabhängigen Bots die risikoadjustierte Kennzahl deutlich
und lassen gleichzeitig *grössere* Einzelverluste zu; nur beim Krypto-Volatility-
Breakout-Bot verbessern sie das Out-of-Sample-Bild klar. Damit zeigt sich
**dasselbe Muster wie in der Vol-Sizing-Untersuchung, bei denselben Bots** —
siehe die Gegenüberstellung in Abschnitt 8.

---

## 1. Schritt 1 — Bestandsaufnahme: welche Bots sind überhaupt betroffen?

Maschinell erzeugt aus den 9 `strategies/<bot>/live_params.py`
(`stop_inventory.py`, rein lesend per AST-Parsing, ohne Bot-Code auszuführen).
Ergebnis auch maschinenlesbar in `results/stop_inventory.json`.

| Bot | Markt | TF | Kategorie | Mechanismus laut `live_params.py` |
|---|---|---|---|---|
| `elliott_wave` | Krypto | 1h | **fester %-Stop** | `STOP_LOSS_PCT = 2.0` |
| `elliott_wave_stocks` | Aktien | 1d | **fester %-Stop** | `STOP_LOSS_PCT = 3.0` |
| `t3_supertrend` | Krypto | 4h | **fester %-Stop** | `STOP_LOSS_PCT = 4.0` |
| `volatility_breakout` | Aktien | 1d | **fester %-Stop** | `STOP_LOSS_PCT = 8.0` |
| `volatility_breakout_crypto` | Krypto | 1d | **fester %-Stop** | `STOP_LOSS_PCT = 5.0` |
| `turtle_soup_crypto` | Krypto | 1d | struktureller Stop | `STOP_MODE = "structural"` (Stop = Tagestief des Setup-Tags) |
| `rsi2_crypto` | Krypto | 1d | kein Stop | `STOP_LOSS_PCT = None` |
| `rsi2_mean_reversion` | Aktien | 1d | kein Stop | `STOP_LOSS_PCT = None` |
| `turtle_soup_stocks` | Aktien | 1d | kein Stop | `STOP_MODE = None` |

**Untersucht wurden ausschliesslich die 5 Bots mit festem %-Stop.**

**Nicht untersucht — `turtle_soup_crypto` (struktureller Stop):** der Stop liegt
dort auf dem Tagestief des Setup-Tags. Das ist konzeptionell etwas anderes als
ein fester Prozentsatz und bereits heute *implizit* volatilitätsabhängig (an
volatilen Tagen ist die Kerze breiter, der Stop damit automatisch weiter). Laut
`live_params.py` wurde dieser Modus gegen „kein Stop" empirisch als robuster
validiert. Nicht vergleichbar, nicht angefasst.

**Nicht untersucht — `rsi2_crypto`, `rsi2_mean_reversion`, `turtle_soup_stocks`
(kein Stop):** in allen drei Fällen ist „kein Stop" laut dokumentierter Historie
in `live_params.py` das empirisch validierte Ergebnis („ein harter Stop senkt den
Erwartungswert" bzw. „musterspezifischer Stop empirisch klar die schlechteste
Variante"). Nachträglich einen Stop einzuführen wäre eine eigenständige
Design-Frage und ist ausdrücklich nicht Teil dieser Aufgabe.

Die Bot-Liste für die eigentliche Rechnung wird von `run_all.py` direkt aus
`results/stop_inventory.json` gelesen — es gibt keine zweite, handgepflegte
Liste, die von der Klassifikation abweichen könnte. `stop_inventory.py` warnt
zusätzlich, falls ein Bot-Ordner mit `live_params.py` existiert, der nicht in
der bekannten 9er-Liste steht.

---

## 2. Methodik

### 2.1 Drei verglichene Varianten

| | Stop-Distanz | nachgezogen? | Rolle |
|---|---|---|---|
| **A — Baseline** | fester Prozentsatz aus `live_params.py` | nein | der heutige Live-Zustand |
| **B — Fix-Trailing** | derselbe feste Prozentsatz | ja | **Kontroll-/Zerlegungsvariante** |
| **C — ATR-Trailing** | `k × ATR(14)` des aktuellen Balkens | ja | die untersuchte Variante |

Variante **B** ist keine Untersuchungs-Kandidatin und führt keinen neuen freien
Parameter ein (sie nutzt exakt den bestehenden `STOP_LOSS_PCT`). Sie existiert
allein, um den Gesamtunterschied A→C in seine zwei Bestandteile zu zerlegen:
**Nachziehen** (A→B) und **volatilitäts-kalibrierte Distanz statt festem
Prozentsatz** (B→C). Ohne diese Zerlegung wäre ein Unterschied zwischen A und C
nicht eindeutig einer der beiden Änderungen zuzuordnen — und genau diese
Zuordnung ist die eigentliche Frage der Aufgabenstellung („könnten
volatilitäts-kalibrierte Trailing-Stops feste Prozentsätze ersetzen?").
Das Ergebnis dieser Zerlegung ist eines der klarsten dieser Untersuchung
(Abschnitt 7).

### 2.2 ATR-Fenster: 14 (begründete Einzelwahl, nicht optimiert)

**Gewählt: ATR mit 14 Perioden.** Begründung:

1. 14 ist Wilders eigener Originalwert und der De-facto-Standard für ATR.
2. Das Projekt verwendet in `strategies/t3_supertrend/indicators.py` bereits
   die Wilder-Familie mit **genau 14** für `DI_LENGTH` und `ADX_LENGTH` — 14 ist
   also keine neu eingeführte, sondern eine bereits etablierte Projekt-Konvention.
3. Die Wahl ist bewusst **nicht** über mehrere Werte optimiert worden
   (Overfitting-Risiko, Aufgaben-Vorgabe Punkt 5).

**Robustheits-Illustration mit genau einem zweiten Wert: ATR-22.** Auch dieser
Wert ist nicht frei gewählt, sondern der ATR-Wert, den das Projekt an anderer
Stelle bereits selbst nutzt (`ATR_LENGTH = 22` für den SuperTrend in
`strategies/t3_supertrend/backtest_trend.py`). Ergebnis siehe Abschnitt 9 —
es wurde **nicht** der „bessere" der beiden Werte ausgewählt; berichtet werden
beide.

Die ATR-Implementierung (`atr_core.wilder_atr`) ist methodisch identisch zur
bereits vorhandenen `strategies/t3_supertrend/indicators.py::calculate_atr`
(True Range, RMA-Glättung mit `alpha = 1/length`) und wird in
`test_atr_core.py` numerisch gegen genau diese bestehende Funktion geprüft
(Abweichung < 1e-12). Bewusst wurde **kein** zweiter, leicht abweichender
ATR-Dialekt eingeführt — das ist die Lehre aus der doppelten
SuperTrend-Implementierung im ursprünglichen Pine-Script.

### 2.3 Kalibrierung des ATR-Multiplikators k — der Kern der Fairness

`k` wird **nicht frei gewählt und nicht optimiert**, sondern so bestimmt, dass
die **mediane anfängliche Stop-Distanz** der ATR-Variante exakt dem bestehenden
`STOP_LOSS_PCT` des jeweiligen Bots entspricht:

```
k = (STOP_LOSS_PCT / 100) / median(ATR_beim_Einstieg / Einstiegskurs)
```

Damit unterscheidet sich C von A/B ausschliesslich in der **Form** (Streuung der
Stop-Distanz über die Trades hinweg), nicht im mittleren **Niveau** der
Stop-Weite. Das ist exakt dieselbe Fairness-Konvention wie in der
Vol-Sizing-Untersuchung, die die inversen Volatilitäts-Gewichte auf Mittelwert
exakt 1,0 normalisiert hat — dort wie hier soll ein reiner Niveau-Effekt
(„insgesamt weitere Stops") das eigentlich interessierende Struktur-Signal nicht
überdecken. Median statt Mittelwert, weil die Verteilung von ATR/Kurs
rechtsschief ist und der Mittelwert die typische Stop-Weite systematisch zu weit
einstellen würde.

Was diese Kalibrierung erzeugt, zeigt die Streuungstabelle (Gesamtzeitraum,
anfängliche Stop-Distanz in % vom Einstiegskurs):

| Bot | Variante | p10 | Median | p90 | max |
|---|---|---|---|---|---|
| `t3_supertrend` | Baseline | 4,00 | 4,00 | 4,00 | 4,00 |
| | ATR-Trailing | 1,90 | 3,94 | 6,74 | **13,23** |
| `volatility_breakout` | Baseline | 8,00 | 8,00 | 8,00 | 8,00 |
| | ATR-Trailing | 5,30 | 8,28 | 13,29 | **32,74** |
| `volatility_breakout_crypto` | Baseline | 5,00 | 5,00 | 5,00 | 5,00 |
| | ATR-Trailing | 2,58 | 4,74 | 7,16 | **10,29** |

Der Median liegt per Konstruktion beim Bot-Wert — aber das p90/Maximum zeigt,
dass einzelne Einstiege in Hochvolatilitätsphasen Stops von 13 % bis 33 %
bekommen. Genau das ist der in der Aufgabenstellung angesprochene Trade-off, und
er materialisiert sich messbar (Abschnitt 8).

**k wird EINMALIG aus den In-Sample-Baseline-Trades kalibriert** und danach
unverändert für Out-of-Sample und alle Stabilitätsfenster verwendet — kein
Informationsfluss aus dem OOS-Abschnitt in den Parameter. Zur Kontrolle wurde
zusätzlich berechnet, welches k sich *hypothetisch* aus den OOS-Trades ergeben
hätte; die Abweichung liegt bei allen 5 Bots unter 10 % (z. B. `t3_supertrend`
1,624 vs. 1,689; `volatility_breakout_crypto` 0,896 vs. 0,903). Die Wahl der
Kalibrierungsperiode treibt die Ergebnisse also nicht.

### 2.4 Trailing-Mechanik: Ratsche und Look-Ahead-Freiheit

- **Ratschen-Regel:** der nachgezogene Stop kann sich nur nach oben bewegen. Ohne
  sie würde ein Volatilitäts-Anstieg *während* eines laufenden Trades den Stop
  wieder nach unten schieben — das wäre per Definition kein Trailing-Stop mehr,
  sondern ein Stop, der im Verlustfall nachgibt. Die Ratsche ist Standard
  (u. a. Chandelier Exit) und die klar konservativere Wahl. **Konsequenz für die
  Interpretation:** die Volatilität wirkt dadurch primär über die Stop-Weite
  *zum Einstiegszeitpunkt*.
- **Nachziehen erst NACH der Stop-Prüfung desselben Balkens.** Andernfalls
  unterstellte man Kenntnis der Reihenfolge von Hoch und Tief innerhalb des
  Balkens. Dieselbe Reihenfolge nutzt bereits das bestehende
  `strategies/volatility_breakout/experiment_trailing_stop.py`. Explizit
  getestet (`test_atr_core.py`).
- **Das laufende Hoch startet beim Einstiegskurs, nicht beim Hoch des
  Einstiegsbalkens.** Ein während der Umsetzung gefundener und behobener Fehler:
  bei den Elliott-Wave-Bots (Einstieg am Tief des Balkens) hätte die andere
  Variante den anfänglichen Trailing-Stop *oberhalb* des Einstiegskurses
  platziert — ein frei erfundener Gewinn. Regressionstest vorhanden.
- **Priorität innerhalb eines Balkens** (Stop → Kursziel → strategie-eigenes
  Ausstiegssignal → Zeit-Exit) und die **drei unterschiedlichen
  Zeit-Exit-Konventionen** der betroffenen Bots wurden originalgetreu
  übernommen und nicht vereinheitlicht.

### 2.5 Baseline-Regressionscheck (die wichtigste Absicherung)

Die drei Varianten werden nicht mit den bot-eigenen `backtest_*.py`-Schleifen
gerechnet, sondern mit einer gemeinsamen, parametrisierten Ausstiegs-Simulation —
anders liesse sich die Ausstiegsregel nicht austauschen, ohne fünf Live-Dateien
anzufassen. Damit steht und fällt alles mit einer Frage: **reproduziert die
Nachbildung mit Variante A exakt die Trades des Bots selbst?**

`verify_baseline.py` prüft das gegen die unveränderte
`equity_simulation.collect_all_trades()` jedes Bots. Ergebnis für **alle 5 Bots:
exakt identisch** — Trade-Anzahl, Summe und Mittelwert der PnL, erster Entry und
letzter Exit:

| Bot | Trades | Summe PnL | Ø PnL |
|---|---|---|---|
| `elliott_wave` | 783 = 783 | 3165,80 = 3165,80 | 4,0432 = 4,0432 |
| `elliott_wave_stocks` | 519 = 519 | 7722,69 = 7722,69 | 14,8799 = 14,8799 |
| `t3_supertrend` | 980 = 980 | 1129,65 = 1129,65 | 1,1527 = 1,1527 |
| `volatility_breakout` | 4510 = 4510 | 3165,46 = 3165,46 | 0,7019 = 0,7019 |
| `volatility_breakout_crypto` | 359 = 359 | 629,88 = 629,88 | 1,7545 = 1,7545 |

Zusätzlich stimmen die Baseline-Portfolio-Kennzahlen exakt mit den in der
Vol-Sizing-Untersuchung berichteten Werten überein (z. B. `t3_supertrend`
In-Sample 100,2 % / −22,2 %, Out-of-Sample 14,7 % / −17,2 %) — eine unabhängige
zweite Bestätigung über zwei getrennt implementierte Untersuchungen hinweg.

### 2.6 Bewertung, Splits und Stabilität

- **Kennzahl:** Calmar-Ratio = Gesamtrendite % / |Max Drawdown %| — identische
  Konvention wie in Vol-Sizing, HRP und Trend-Overlay (in `test_atr_core.py`
  gegen das dortige Zahlenbeispiel 82,43/6,33 = 13,02 geprüft). Bei einem
  Drawdown von exakt 0 ist die Kennzahl nicht definiert und wird als „n/a"
  geführt statt durch einen Ersatz-Nenner künstlich endlich gemacht.
- **In-/Out-of-Sample:** chronologischer Split mit `TRAIN_SPLIT_RATIO = 0.7` aus
  den bestehenden `multi_symbol_walk_forward.py`, angewendet auf den
  kombinierten Trade-Datensatz. Der Split-Zeitpunkt wird aus der **Baseline**
  bestimmt und für alle drei Varianten identisch verwendet.
- **Walk-Forward-Stabilität:** 4 gleich lange, chronologische Fenster über die
  gesamte Trade-Historie (wie in der Vol-Sizing-Untersuchung), identische
  Fenstergrenzen für alle Varianten. „Stabil" = in mindestens 3 der 4 Fenster
  zeigt der Calmar-Vergleich dieselbe Richtung wie das Gesamtbild.
- **Episoden-Aufschlüsselung nach Kalenderjahr** — das in der
  Trend-Overlay-Untersuchung etablierte Prüfmuster. Gemessen wird, welcher Anteil
  der Summe der absoluten jährlichen Renditedifferenzen auf ein einzelnes Jahr
  entfällt; > 60 % gilt als „durch eine Einzelepisode getrieben".
- **Portfolio-Simulation und Kapitalmanagement** unverändert aus der jeweils
  bot-eigenen `equity_simulation.py` übernommen (Startkapital 10.000,
  `ALLOCATION_PCT`, `MAX_CONCURRENT_POSITIONS`, BTC-Regimefilter bei
  `t3_supertrend`). Diese Untersuchung verändert die **Ausstiegsregel**, nicht
  das Kapitalmanagement.

---

## 3. Getroffene Annahmen (vollständig)

1. **ATR-Fenster 14** als begründete Einzelwahl, ATR-22 als einzelne
   Robustheits-Illustration (Begründung beider Werte siehe 2.2). Keine
   Optimierung über mehrere Fenster.
2. **ATR-Multiplikator k über den Median der anfänglichen Stop-Distanz
   kalibriert** statt frei gewählt (2.3). Alternative wäre ein
   Literatur-Standardwert (z. B. k = 2 wie beim Chandelier Exit) gewesen — dann
   hätten sich aber Niveau- und Formeffekt vermischt, und die Wahl des Niveaus
   wäre selbst ein ungetesteter freier Parameter geworden.
3. **k einmalig auf den In-Sample-Baseline-Trades kalibriert**, danach
   unverändert für OOS und alle Fenster. Strenger als die periodenweise
   Normierung der Vol-Sizing-Untersuchung; die hypothetische OOS-Kalibrierung
   wird zur Kontrolle mitberichtet (Abweichung < 10 % bei allen Bots).
4. **Ratschen-Regel für den nachgezogenen Stop** (2.4). Die Alternative (Stop
   folgt der Volatilität in beide Richtungen) wäre kein Trailing-Stop im
   üblichen Sinn und die aggressivere Variante.
5. **Laufendes Hoch startet beim Einstiegskurs** (2.4).
6. **Kontrollvariante B (Fix-Trailing)** wurde ergänzt, obwohl die
   Aufgabenstellung nur A gegen C verlangt — ohne sie wäre der Befund nicht
   zuordenbar. Sie führt keinen freien Parameter ein.
7. **`ALLOCATION_PCT = 10 %` angenommen** für `elliott_wave`,
   `elliott_wave_stocks` und `t3_supertrend` (in deren `live_params.py` nicht
   dokumentiert) sowie **`MAX_CONCURRENT_POSITIONS = 8` angenommen** für
   `elliott_wave` — beides identisch zur Vol-Sizing-Untersuchung übernommen,
   damit die vier Backlog-Untersuchungen untereinander vergleichbar bleiben.
   In den Ergebnis-JSONs als `allocation_pct_assumed` / `max_concurrent_assumed`
   markiert. Betrifft alle drei Varianten gleichermassen und kann den
   *Vergleich* daher nicht verzerren, wohl aber die absoluten Renditeniveaus.
8. **Jeder Bot wurde exakt so simuliert, wie es seine eigene
   `equity_simulation.py` tut.** Konsequenz, die ausdrücklich genannt sein soll:
   `volatility_breakout_crypto` führt in `live_params.py`
   `BTC_REGIME_FILTER_ENABLED = True`, seine `equity_simulation.py` wendet den
   Filter aber nicht an (nur `forward_test.py` tut das). Die hier berichteten
   Zahlen für diesen Bot enthalten den Filter deshalb **nicht** — konsistent zur
   Vol-Sizing-Untersuchung und zur bestehenden Backtest-Konvention. Der Filter
   wirkt nur auf Einstiege und damit in allen drei Varianten gleich.
9. **4 Walk-Forward-Stabilitätsfenster** (Aufgabe verlangt „mehrere" ohne Zahl) —
   identisch zur Vol-Sizing-Untersuchung.
10. **Episoden-Schwelle 60 %** für „durch eine Einzelepisode getrieben" und die
    3-von-4-Regel für „Walk-Forward-stabil": selbst gewählte, dokumentierte
    Heuristiken, keine Standardmasse.
11. **Kalenderjahre als Episoden-Raster.** Die Trend-Overlay-Untersuchung
    konnte Episoden über ein tägliches Signal definieren; hier gibt es kein
    solches Signal, deshalb das gröbere, aber neutrale Kalenderjahr-Raster —
    es wird nicht nachträglich an die Daten angepasst.
12. ~~**Keine Buy-and-Hold-Referenz.**~~ **ÜBERHOLT — nachgetragen, siehe 0.1.**
    Ursprüngliche Begründung: die Zahl wäre für alle drei Varianten dieselbe
    und trüge zur eigentlichen Frage nichts bei. Das gilt für den *internen*
    Vergleich weiterhin, verfehlt aber die vorgelagerte Frage, ob die
    Ausgangsbasis trägt — bei `volatility_breakout` schlägt Buy-and-Hold die
    Strategie risikoadjustiert um das 2,5-Fache.
13. **Nachtrag — Bootstrap-Einstellungen:** Blocklänge 3 Monate, 2000
    Replikate, Seed 20260907; 500 Permutationen für die
    Reihenfolge-Sensitivität. Identisch zur Vertiefungsstudie
    `research/vbc_deepdive/`, damit beide vergleichbar bleiben. Für die beiden
    Elliott-Wave-Bots wurde **kein** Bootstrap gerechnet: ein
    Konfidenzintervall um eine nicht interpretierbare Grösse wäre irreführende
    Präzision.
14. **Nachtrag — Buy-and-Hold** über eine gemeinsame Implementierung
    (`decision_basis.buy_and_hold`), weil zwei der fünf Bots kein eigenes
    `buy_and_hold_benchmark.py` haben. Gegen die drei Bots mit eigener Fassung
    exakt geprüft (`verify_baseline.py`). Auf den jeweiligen Trade-Zeitraum
    zugeschnitten — die rohen CSVs reichen bei den Aktien-Bots Jahrzehnte
    weiter zurück, ein ungeschnittener Vergleich wäre sinnlos (ungeschnitten
    ergäbe `volatility_breakout` +115.164 % statt +805 %).

---

## 4. Ergebnisse — Übersicht

Rendite % / Max Drawdown % / Calmar-Ratio.

### In-Sample

| Bot | A Baseline | B Fix-Trailing | C ATR-Trailing |
|---|---|---|---|
| `t3_supertrend` | 100,22 / −22,20 / **4,51** | 8,02 / −13,14 / 0,61 | −1,10 / −15,57 / **−0,07** |
| `volatility_breakout` | 95,94 / −23,97 / **4,00** | 62,39 / −19,43 / 3,21 | 80,14 / −23,27 / **3,44** |
| `volatility_breakout_crypto` | 40,89 / −16,77 / **2,44** | 13,73 / −7,39 / 1,86 | 12,96 / −5,76 / **2,25** |
| `elliott_wave` * | 802,43 / −0,92 / 872,21 | 679,61 / −0,02 / 33980,5 | 569,67 / −0,22 / 2589,41 |
| `elliott_wave_stocks` * | 623,46 / −9,79 / 63,68 | 896,49 / −0,01 / 89649,0 | 751,61 / −0,15 / 5010,73 |

### Out-of-Sample

| Bot | A Baseline | B Fix-Trailing | C ATR-Trailing |
|---|---|---|---|
| `t3_supertrend` | 14,69 / −17,22 / **0,85** | 5,07 / −12,58 / 0,40 | −0,73 / −14,01 / **−0,05** |
| `volatility_breakout` | 67,21 / −12,31 / **5,46** | 45,10 / −13,43 / 3,36 | 31,22 / −15,28 / **2,04** |
| `volatility_breakout_crypto` | 20,23 / −11,33 / **1,79** | 30,43 / −6,13 / 4,96 | 28,12 / −5,58 / **5,04** |
| `elliott_wave` * | 150,66 / −1,83 / 82,33 | 146,65 / −0,02 / 7332,5 | 137,97 / −0,09 / 1533,0 |
| `elliott_wave_stocks` * | 321,36 / −4,72 / 68,08 | 167,81 / 0,00 / n/a | 142,67 / 0,00 / n/a |

### Gesamtzeitraum

| Bot | A Baseline | B Fix-Trailing | C ATR-Trailing |
|---|---|---|---|
| `t3_supertrend` | 129,64 / −22,20 / **5,84** | 13,50 / −13,14 / 1,03 | −1,82 / −15,57 / **−0,12** |
| `volatility_breakout` | 224,41 / −23,97 / **9,36** | 139,93 / −19,43 / 7,20 | 140,46 / −23,27 / **6,04** |
| `volatility_breakout_crypto` | 71,26 / −16,77 / **4,25** | 48,15 / −7,39 / 6,52 | 45,65 / −5,76 / **7,93** |
| `elliott_wave` * | 2162,06 / −1,83 / 1181,45 | 1822,88 / −0,02 / 91144,0 | 1493,60 / −0,22 / 6789,09 |
| `elliott_wave_stocks` * | 3084,09 / −9,79 / 315,02 | 2568,75 / −0,01 / 256875,0 | 1966,57 / −0,15 / 13110,47 |

\* **nicht interpretierbar**, siehe 5.4. Die Zeilen stehen nur der
Vollständigkeit halber hier und gehen in keine Schlussfolgerung ein.

(Maschinenlesbar identisch in `results/summary_table.json`; Rohdaten je Bot und
ATR-Fenster in `results/<bot>_atr<fenster>.json`.)

---

## 5. Ergebnisse je Bot

### 5.1 `t3_supertrend` (Krypto, 4h, Baseline-Stop 4,0 %, k = 1,62)

Der **deutlichste und robusteste Befund der gesamten Untersuchung**: der
ATR-Trailing-Stop zerstört den Ertrag dieses Bots praktisch vollständig
(Gesamtzeitraum 129,64 % → −1,82 %). Der Max Drawdown verbessert sich zwar
(−22,20 % → −15,57 %), aber bei Weitem nicht genug, um den Renditeverlust
aufzuwiegen — die Calmar-Ratio fällt von 5,84 auf −0,12.

**Walk-Forward: stabil (4 von 4 Fenstern schlechter).**

| Fenster | A Baseline | B Fix-Trailing | C ATR-Trailing |
|---|---|---|---|
| W1 2021-09 … 2022-11 | −4,00 / −10,12 / −0,40 | −5,19 / −6,31 / −0,82 | −9,19 / −10,21 / −0,90 |
| W2 2022-11 … 2024-02 | 59,22 / −13,55 / 4,37 | 2,49 / −7,46 / 0,33 | 2,46 / −6,77 / 0,36 |
| W3 2024-02 … 2025-05 | 20,39 / −15,61 / 1,31 | 9,74 / −5,28 / 1,84 | 4,62 / −6,76 / 0,68 |
| W4 2025-05 … 2026-08 | 23,75 / −17,22 / 1,38 | 6,43 / −12,58 / 0,51 | 0,47 / −14,01 / 0,03 |

**Episoden-Befund: der Unterschied ist zu 75 % ein einziges Jahr — 2024.**

| Jahr | A Baseline | B Fix-Trailing | C ATR-Trailing |
|---|---|---|---|
| 2021 | −3,27 % | −1,24 % | −2,57 % |
| 2022 | −3,28 % | −6,08 % | −8,00 % |
| 2023 | +4,55 % | +2,74 % | +6,89 % |
| **2024** | **+115,32 %** | **+10,68 %** | **+0,65 %** |
| 2025 | −10,13 % | +4,15 % | +0,58 % |
| 2026 | +21,31 % | +3,49 % | +1,26 % |

Die verketteten Jahresrenditen reproduzieren den Gesamtzeitraum fast exakt
(Baseline verkettet +129,6 % gegenüber tatsächlich +129,64 %; ATR-Variante
−1,8 % gegenüber −1,82 %) — die Aufschlüsselung ist also belastbar. **Ohne 2024
läge die Baseline bei rund +6,6 % und die ATR-Variante bei rund −2,4 %:** der
Vorsprung schrumpft von ~131 Prozentpunkten auf ~9.

Das ist eine wichtige Doppel-Einordnung: **auch der Vorteil der Baseline ist
episoden-getrieben.** Die Richtung des Befunds bleibt allerdings in allen vier
Stabilitätsfenstern und in 5 der 6 Jahre gleich — die *Grössenordnung* hängt an
2024, das *Vorzeichen* nicht. Der Mechanismus ist direkt sichtbar: 2024 war das
Jahr mit den grossen, durchgehenden Krypto-Trends, und genau in solchen Phasen
verdient ein Trendfolgesystem sein Geld über wenige, sehr grosse Gewinner. Der
grösste Einzeltrade der Baseline liegt bei **+321,07 %**, der der ATR-Variante
nur noch bei **+57,23 %**.

### 5.2 `volatility_breakout` (Aktien, 1d, Baseline-Stop 8,0 %, k = 4,05)

Klar, aber weniger dramatisch schlechter: Calmar 9,36 → 6,04 im Gesamtzeitraum,
in beiden Perioden zuungunsten der ATR-Variante (IS 4,00 → 3,44, OOS 5,46 →
2,04). Auffällig: **der Max Drawdown verbessert sich hier nicht einmal** (OOS
−12,31 % → −15,28 %), die Rendite bricht aber deutlich ein (67,21 % → 31,22 %).
Damit fehlt der ATR-Variante bei diesem Bot sogar das übliche Trostargument.

**Walk-Forward: stabil (3 von 4 Fenstern schlechter).** Nur W2
(2019-02 … 2021-08) fällt zugunsten der ATR-Variante aus (Calmar 5,70 → 6,19).

**Episoden-Befund: NICHT einzelepisoden-getrieben** — auf das stärkste Jahr
(2025) entfallen nur 23 % des Unterschieds; der Nachteil verteilt sich über 11
Jahre.

**Nachtrag — dieser Befund hält der Unsicherheitsrechnung NICHT stand.** Die
erste Fassung schloss auf „Verbesserung: nein". Beide nachgetragenen Prüfungen
widersprechen dem:

- **Block-Bootstrap:** P(ATR besser) = 63,2 % über den Gesamtzeitraum und
  74,1 % In-Sample — mehrheitlich auf der *anderen* Seite als der
  Punktschätzer; nur Out-of-Sample 33,4 %. Das Vorzeichen ist von den Daten
  nicht bestimmt.
- **Reihenfolge gleichzeitiger Einstiege:** dieser Bot hat mit **87,7 %** den
  höchsten Anteil geteilter Zeitstempel aller fünf (grösste Gruppe: 24 Trades
  an einem Tag), und **68 % aller gefundenen Signale werden mangels Kapital
  verworfen**. Die Baseline-Calmar schwankt allein dadurch zwischen 4,35 und
  15,77; der berichtete Unterschied (9,36 → 6,04) liegt vollständig innerhalb
  dieser Spanne.

Korrigiertes Urteil für diesen Bot: **kein belastbarer Unterschied zwischen den
drei Stop-Varianten.** Die breite Zeitverteilung des Punktschätzer-Nachteils
bleibt richtig beobachtet, trägt aber keine Aussage.

Hinzu kommt die Einordnung aus 0.1: Buy-and-Hold hätte über denselben Zeitraum
eine 2,5-mal bessere Calmar-Ratio erzielt (23,12 vs. 9,36). Die Frage nach der
besten Stop-Variante ist bei diesem Bot nachrangig gegenüber der Frage, ob die
Strategie gegenüber stumpfem Halten überhaupt trägt.

Das Ergebnis deckt sich mit einem **bereits im Projekt dokumentierten Befund**:
`strategies/volatility_breakout/experiment_trailing_stop.py` hat für genau
diesen Bot einen prozentualen Trailing-Stop getestet, und `live_params.py` hält
fest: „Trailing-Stop NICHT übernommen (Overfitting-Muster, identisch zum
Elliott-Wave-Aktien-Bot-Präzedenzfall)". Die hier zusätzlich untersuchte
**volatilitäts-kalibrierte** Variante ändert an diesem Bild nichts — sie ist
sogar noch etwas schlechter als der einfache prozentuale Trailing-Stop
(Calmar 6,04 vs. 7,20).

### 5.3 `volatility_breakout_crypto` (Krypto, 1d, Baseline-Stop 5,0 %, k = 0,90)

**Der einzige Bot mit einem klar positiven Teilergebnis.** In-Sample leicht
zuungunsten der ATR-Variante (Calmar 2,44 → 2,25), Out-of-Sample dagegen
deutlich zugunsten (1,79 → 5,04): die Rendite steigt (20,23 % → 28,12 %) *und*
der Drawdown halbiert sich fast (−11,33 % → −5,58 %). Nach der hier verwendeten
Konvention ergibt die widersprüchliche IS/OOS-Richtung das Urteil **„unklar"**,
mit deutlicher Tendenz ins Positive (Gesamtzeitraum-Calmar 4,25 → 7,93).

**Walk-Forward: stabil (3 von 4 Fenstern besser)** — W1, W3, W4 zugunsten der
ATR-Variante, W2 (2023-04 … 2024-06) klar dagegen.

**Episoden-Befund: 55 % des Unterschieds entfallen auf 2024** — knapp unterhalb
der 60-%-Schwelle, aber mit demselben Vorzeichen wie bei `t3_supertrend`:

| Jahr | A Baseline | C ATR-Trailing |
|---|---|---|
| 2022 | −12,81 % | −1,91 % |
| 2023 | +14,96 % | +7,04 % |
| **2024** | **+43,00 %** | **+2,37 %** |
| 2025 | +12,44 % | +21,34 % |
| 2026 | +6,25 % | +11,67 % |

**Ohne 2024** läge die Baseline (verkettet) bei rund +19,7 % und die ATR-Variante
bei rund +42,3 %. Anders gesagt: **die ATR-Variante gewinnt in jedem Jahr ausser
dem einen grossen Trendjahr — und verliert dort dramatisch.** Das ist derselbe
Mechanismus wie bei `t3_supertrend`, nur dass dieser Bot weniger von genau
diesen grossen Trendbewegungen abhängt und die Drawdown-Reduktion deshalb
überwiegt. Auch hier wird der grösste Einzeltrade gekappt (+174,10 % → +40,78 %).

### 5.4 `elliott_wave` und `elliott_wave_stocks` — nicht interpretierbar

Der Backtest beider Elliott-Wave-Bots steigt zum Kurs am **Wellenende**
(`wave["wave5"]`, dem Zigzag-Tiefpunkt eines bärischen Impulses) ein. Ein
Zigzag-Pivot ist aber per Konstruktion erst dann ein Pivot, wenn sich der Kurs
anschliessend um mindestens `deviation_pct` in die Gegenrichtung bewegt hat —
der Einstiegskurs im Backtest ist damit ein Tiefpunkt, dem **rückwirkend
garantiert** eine Aufwärtsbewegung folgt.

Gemessen (`run_one_bot.elliott_lookahead_diagnostic`):

| Bot | Trades | Anteil, der ≥ `deviation_pct` erreicht | Median maximaler Kursanstieg im Halte-Fenster |
|---|---|---|---|
| `elliott_wave` | 783 | **100,0 %** (Schwelle 4 %) | **+16,85 %** |
| `elliott_wave_stocks` | 519 | **100,0 %** (Schwelle 5 %) | **+30,29 %** |

Für einen **festen** Stop ist dieser Look-Ahead vergleichsweise harmlos: er hebt
das Niveau aller Trades gleichermassen an. Ein **Trailing-Stop** hingegen koppelt
den Ausstieg direkt an dieses zwischenzeitliche Hoch und verwandelt die Garantie
in einen quasi-sicheren Gewinn. Das Resultat sind Gewinnraten von **98,7 %**
(`elliott_wave`) bzw. **99,4 %** (`elliott_wave_stocks`), Max Drawdowns von
−0,22 % bzw. −0,15 % und daraus folgende Calmar-Ratios im vier- bis
sechsstelligen Bereich. Diese Zahlen messen die Backtest-Konvention, nicht die
Wirkung eines Trailing-Stops.

**Wichtig zur Einordnung:** das ist kein neu entdeckter Fehler, sondern die
bereits im Übergabeprotokoll dokumentierte Eigenschaft — dort ist festgehalten,
dass `forward_test.py` genau deshalb umgestellt wurde, den **aktuellen**
Marktpreis zum Erkennungszeitpunkt zu verwenden (mit getrenntem `signal_time`
und `entry_time`). Der **Backtest** behält die Wellenend-Konvention. Für die
bisherigen Fragestellungen (fester Stop, Positionsgrösse, Portfolio-Gewichtung)
war das vertretbar; für die Bewertung eines Trailing-Stops ist es das nicht.

Diese beiden Bots werden deshalb **explizit als „nicht untersucht — Backtest für
diese Fragestellung nicht geeignet"** geführt und gehen in keine
Schlussfolgerung ein. Eine belastbare Aussage über Trailing-Stops bei den
Elliott-Wave-Bots würde einen Backtest voraussetzen, der zum
**Erkennungszeitpunkt** des Musters einsteigt statt zum Wellenende — das wäre
eine Änderung an der validierten Backtest-Konvention zweier Live-Bots und
ausdrücklich nicht Teil dieser Aufgabe.

---

## 6. Walk-Forward- und Episoden-Stabilität — Zusammenfassung

| Bot | Bewertung (Calmar IS + OOS) | WF-stabil | Fenster gleicher Richtung | Episoden-Konzentration |
|---|---|---|---|---|
| `t3_supertrend` | **nein** | ja | 4/4 | 75 % in 2024 (**Einzelepisode**) |
| `volatility_breakout` | **nein** | ja | 3/4 | 23 % in 2025 (breit verteilt) |
| `volatility_breakout_crypto` | **unklar** (OOS klar positiv) | ja | 3/4 | 55 % in 2024 (knapp unter Schwelle) |
| `elliott_wave` | nicht interpretierbar | — | — | — |
| `elliott_wave_stocks` | nicht interpretierbar | — | — | — |

Die in der Trend-Overlay-Untersuchung gelernte Lehre greift hier auf **beiden
Seiten**: bei `t3_supertrend` und `volatility_breakout_crypto` hängt nicht nur
der beobachtete Effekt, sondern auch die zugrunde liegende Baseline-Performance
weitgehend an einer einzelnen Episode (dem Trendjahr 2024). Anders als bei der
Trend-Overlay-Untersuchung kehrt sich das Vorzeichen des Effekts jedoch in den
übrigen Fenstern nicht um — die *Richtung* ist bei allen drei auswertbaren Bots
in mindestens 3 von 4 Fenstern konsistent, nur die *Grössenordnung* ist
episodenabhängig.

---

## 7. Zerlegung: was wirkt eigentlich — das Nachziehen oder die ATR-Kalibrierung?

Calmar-Ratio, Gesamtzeitraum:

| Bot | A Baseline | B Fix-Trailing | C ATR-Trailing | A→B (Nachziehen) | B→C (ATR-Kalibrierung) |
|---|---|---|---|---|---|
| `t3_supertrend` | 5,84 | 1,03 | −0,12 | **−4,81** | −1,15 |
| `volatility_breakout` | 9,36 | 7,20 | 6,04 | **−2,16** | −1,16 |
| `volatility_breakout_crypto` | 4,25 | 6,52 | 7,93 | **+2,27** | +1,41 |

**Der weitaus grösste Teil des Effekts — in beide Richtungen — kommt vom
Nachziehen des Stops selbst, nicht von der Volatilitäts-Kalibrierung.** Die
ATR-Kalibrierung verstärkt die jeweils bereits vorhandene Richtung nur noch um
etwa ein Viertel bis die Hälfte des Weges. Bei allen drei Bots hat sie dasselbe
Vorzeichen wie der Trailing-Schritt.

Das ist die direkteste Antwort auf die eigentliche Aufgabenfrage: **die
volatilitäts-kalibrierte Distanz ist nicht der entscheidende Hebel.** Wer die
Frage „ersetzt ein ATR-Trailing-Stop den festen Prozentsatz sinnvoll?" stellt,
entscheidet in Wahrheit zu ~70–80 % über die Frage „soll der Stop überhaupt
nachgezogen werden?" — und diese Frage ist im Projekt für
`volatility_breakout` bereits verneint worden.

---

## 8. Gegenüberstellung zum Vol-Sizing-Befund (ausdrücklich gefordert)

Die Vol-Sizing-Untersuchung kam zu dem Schluss, dass volatilitätsbasierte
Anpassungen bei trendfolgenden Strategien eher schaden, weil „die grössten
Gewinne oft GENAU in Phasen erhöhter Volatilität fallen — Vol-Skalierung
reduziert dort die Positionsgrösse genau dann, wenn die Strategie am meisten
verdient". Die Aufgabenstellung fragt, ob sich ein ähnliches Muster hier zeigt.

**Antwort: ja, und zwar überraschend deckungsgleich — bis hinunter auf die
Ebene der einzelnen Bots.**

| Bot | Vol-Sizing: Verbesserung? | Trailing-Stops: Verbesserung? |
|---|---|---|
| `t3_supertrend` | unklar | **nein** |
| `volatility_breakout` | nein | **nein** |
| `volatility_breakout_crypto` | **ja** | **unklar (OOS klar positiv)** |

`volatility_breakout_crypto` war einer von nur zwei Bots, bei denen die
Vol-Skalierung half — und er ist auch hier der einzige Bot mit einem klar
positiven Teilergebnis. Der zweite Vol-Sizing-Gewinner (`rsi2_crypto`) hat gar
keinen Stop und fällt hier per Bestandsaufnahme aus dem Scope. Die Bots, denen
die Vol-Skalierung schadete, sind hier ebenfalls die Verlierer.

**Die zweite Frage der Aufgabenstellung — „ein weiterer, breiterer Stop in
volatilen Phasen könnte Gewinne laufen lassen, aber auch grössere Einzelverluste
zulassen" — lässt sich klar beantworten: beides tritt ein, aber asymmetrisch zu
Lasten der ATR-Variante.**

| Bot | | Win Rate | Ø PnL | schlechtester Trade | bester Trade |
|---|---|---|---|---|---|
| `t3_supertrend` | Baseline | 28,0 % | +1,15 % | **−4,30 %** | **+321,07 %** |
| | ATR-Trailing | 35,6 % | −0,16 % | **−11,21 %** | **+57,23 %** |
| `volatility_breakout` | Baseline | 53,9 % | +0,70 % | **−8,30 %** | +63,53 % |
| | ATR-Trailing | 53,0 % | +0,75 % | **−26,03 %** | +63,53 % |
| `volatility_breakout_crypto` | Baseline | 26,5 % | +1,75 % | **−5,30 %** | **+174,10 %** |
| | ATR-Trailing | 43,4 % | +1,07 % | **−9,00 %** | **+40,78 %** |

Die ATR-Variante bewirkt bei allen drei Bots dasselbe:

1. **Die Gewinnrate steigt** (bei den beiden Krypto-Bots deutlich) — der
   nachgezogene Stop sichert viele kleine Gewinne.
2. **Der durchschnittliche Gewinn pro Trade sinkt trotzdem** (ausser bei
   `volatility_breakout`, dort praktisch unverändert) — die vielen kleinen
   Gewinne wiegen die gekappten grossen nicht auf.
3. **Die grössten Gewinner werden gekappt**: +321 % → +57 % bzw. +174 % → +41 %.
   Genau dieselbe Kappung der Gewinnseite, die die Vol-Sizing-Untersuchung
   beschrieben hat — nur über den Ausstiegszeitpunkt statt über die
   Positionsgrösse.
4. **Und zusätzlich werden die Einzelverluste grösser**: −4,3 % → −11,2 %,
   −8,3 % → −26,0 %, −5,3 % → −9,0 %. Das ist der Preis der
   Volatilitäts-Kalibrierung: der Median der Stop-Distanz ist per Konstruktion
   gleich, aber die Verteilung ist rechtsschief (siehe Streuungstabelle in
   2.3) — Einstiege in Hochvolatilitätsphasen bekommen Stops von 13 % bis 33 %
   statt der festen 4 % bzw. 8 %.

**Damit ist das Muster hier sogar ungünstiger als beim Vol-Sizing:** dort wurde
„nur" die Gewinnseite beschnitten, während die Verlustseite mit-schrumpfte. Hier
wird die Gewinnseite beschnitten **und** die Verlustseite geweitet. Dass die
Drawdowns auf Portfolio-Ebene trotzdem meist sinken, liegt daran, dass die
vielen kleinen gesicherten Gewinne die einzelnen grösseren Verluste zeitlich
glätten — es ist eine andere Verteilung, keine geringere Verlustfähigkeit.

Ergänzend passt der Befund zu einer **dritten, älteren Projekt-Erkenntnis**: der
Signal-Qualitäts-Test des Aktien-Elliott-Wave-Bots kam zu dem Schluss, dass „die
exakten Stop-Loss-/Take-Profit-Regeln selbst keinen Mehrwert bringen — der
Mehrwert kommt aus Timing und Kapitalmanagement". Diese Untersuchung findet
nichts, was dem widerspräche: die Ausstiegs-Feinjustierung verschiebt vor allem
die Form der Ergebnisverteilung, ohne einen zusätzlichen Edge zu erzeugen.

---

## 9. Robustheits-Illustration: ATR-22 statt ATR-14

Ein einzelner zweiter Fensterwert, **nicht** um den besseren auszuwählen
(Out-of-Sample, ATR-Trailing-Variante):

| Bot | Rendite ATR-14 | Rendite ATR-22 | Calmar ATR-14 | Calmar ATR-22 |
|---|---|---|---|---|
| `t3_supertrend` | −0,73 % | −2,14 % | −0,05 | −0,17 |
| `volatility_breakout` | 31,22 % | 33,06 % | 2,04 | 2,13 |
| `volatility_breakout_crypto` | 28,12 % | 31,04 % | 5,04 | 5,49 |

Die Schlussfolgerung ändert sich bei **keinem** Bot: `t3_supertrend` bleibt klar
negativ, `volatility_breakout` bleibt deutlich unter seiner Baseline (5,46),
`volatility_breakout_crypto` bleibt klar über seiner Baseline (1,79). Die
kalibrierten Multiplikatoren verschieben sich nur geringfügig (z. B.
`t3_supertrend` 1,624 → 1,634). **Die Ergebnisse hängen nicht an der genauen
ATR-Fensterwahl** — anders als in der Trend-Overlay-Untersuchung, wo die
Grössenordnung spürbar auf die Fensterwahl reagierte.

---

## 10. Übergreifende Einordnung aller vier Backlog-Untersuchungen

| Untersuchung | Was wurde variiert? | Ergebnis |
|---|---|---|
| Vol-Sizing (PR #18) | Positions**grösse** je Trade | 7 von 9 Bots schlechter, 2 besser (beide Krypto, kurz/mittel haltend) |
| HRP (PR #19) | Portfolio-**Gewichtung** zwischen Bots | Verbesserungsmarge strukturell klein |
| Trend-Overlay (PR #20) | Gesamt-**Exponierung** über ein Marktsignal | Effekt fast vollständig aus einer Episode (2022), OOS wirkungslos |
| Trailing-Stops (diese) | **Ausstiegszeitpunkt** je Trade | 2 von 3 auswertbaren Bots schlechter, 1 OOS besser |

Über alle vier zieht sich ein gemeinsames Muster, das sich in drei Sätzen fassen
lässt:

**1. Jeder Mechanismus, der die Ertragsverteilung an ihrem oberen Ende
beschneidet, kostet bei diesen Bots mehr, als er an Risiko spart.** Vol-Sizing
verkleinert die Position in volatilen Phasen; ein Trailing-Stop beendet die
Position, sobald die Bewegung stockt. Beide greifen genau dort an, wo diese
Strategien ihren Ertrag erzeugen: in wenigen, grossen, volatilen Bewegungen. Die
Zahlen sind auffällig ähnlich — bei `t3_supertrend` sinkt der grösste Einzeltrade
von +321 % auf +57 %, bei `volatility_breakout_crypto` von +174 % auf +41 %.

**2. Es ist derselbe kleine Kreis von Bots, bei dem volatilitätsbasierte
Eingriffe helfen.** `volatility_breakout_crypto` ist sowohl der Vol-Sizing- als
auch der Trailing-Stop-Gewinner; die trendfolgenden Bots (`t3_supertrend`,
`volatility_breakout`, und beim Vol-Sizing auch die Turtle-Soup-Bots) verlieren
in beiden Untersuchungen. Die in der Vol-Sizing-Untersuchung formulierte
Hypothese — volatilitätsbasierte Anpassungen schaden trendfolgenden, nutzen
eher kurzhaltenden/reversionsnahen Strategien — wird durch diese vierte
Untersuchung mit einem völlig anderen Mechanismus (Ausstieg statt Positionsgrösse)
unabhängig gestützt. Das ist kein Beweis, aber deutlich mehr als ein Zufallsfund.

**3. Effekte, die im Gesamtzeitraum gross aussehen, hängen bei diesen Bots
regelmässig an einer einzelnen Episode.** Beim Trend-Overlay war es 2022, hier
ist es 2024 — und zwar auf *beiden* Seiten des Vergleichs: auch die
Baseline-Überlegenheit von `t3_supertrend` ist zu 75 % das Jahr 2024. Die in der
Trend-Overlay-Untersuchung eingeführte Episoden-Aufschlüsselung hat sich damit
zum zweiten Mal als das entscheidende Prüfwerkzeug erwiesen und sollte bei
künftigen Untersuchungen von Anfang an mitlaufen.

Ein vierter, methodischer Punkt, der sich erst durch diese Untersuchung zeigt:
**die Aussagekraft eines Backtests hängt von der Fragestellung ab, nicht nur von
seiner Korrektheit.** Der Elliott-Wave-Backtest ist für die Fragen der ersten
drei Untersuchungen brauchbar und wurde dort auch verwendet — für die Frage nach
Trailing-Stops ist er es nicht, weil dieselbe bekannte Einstiegs-Konvention hier
plötzlich das Ergebnis dominiert. Bei künftigen Untersuchungen lohnt es sich,
diese Frage vorab explizit zu stellen.

---

## 11. Gesamteinschätzung (unaufgeregt, ohne Handlungsempfehlung)

Von den 9 Bots kommen nur 5 für die Fragestellung überhaupt in Betracht, und von
diesen 5 lassen sich nur 3 belastbar auswerten. Bei diesen 3 gilt:

- Bei **`t3_supertrend`** wäre der Austausch des festen Stops gegen einen
  ATR-Trailing-Stop retrospektiv sehr teuer gewesen (Calmar 5,84 → −0,12),
  konsistent über alle vier Stabilitätsfenster, wenn auch in der Grössenordnung
  von einem einzigen Trendjahr dominiert.
- Bei **`volatility_breakout`** wäre er ebenfalls schlechter gewesen (Calmar
  9,36 → 6,04), und hier ohne die übliche Drawdown-Kompensation. Der Befund ist
  zeitlich breit verteilt und deckt sich mit dem bereits im Projekt
  dokumentierten Ergebnis eines prozentualen Trailing-Stop-Tests für genau
  diesen Bot.
- Bei **`volatility_breakout_crypto`** wäre er Out-of-Sample klar besser gewesen
  (Calmar 1,79 → 5,04, Drawdown −11,33 % → −5,58 %), In-Sample leicht
  schlechter. Der Vorteil entsteht in vier von fünf Jahren; im einen grossen
  Trendjahr 2024 verliert die Variante dramatisch (+43,0 % → +2,4 %).

Quer über alle drei gilt, dass der grösste Teil des Effekts — in beide
Richtungen — vom **Nachziehen** des Stops stammt und nicht von der
**Volatilitäts-Kalibrierung**. Die eigentlich untersuchte ATR-Komponente ist bei
allen drei Bots der kleinere der beiden Bestandteile. Sie hat allerdings einen
eigenständigen, klar messbaren Nebeneffekt: durch die rechtsschiefe Verteilung
der ATR-Stop-Distanzen werden einzelne Verluste deutlich grösser als beim festen
Stop (bis −26,03 % gegenüber −8,30 % bei `volatility_breakout`), auch wenn die
mediane Stop-Weite per Kalibrierung identisch ist.

**Nachtrag nach Buy-and-Hold-Vergleich, Bootstrap und
Reihenfolge-Sensitivität** (Abschnitt 0): von den drei auswertbaren Bots bleibt
nach der Unsicherheitsrechnung **einer** mit einem belastbaren Ergebnis übrig —
`t3_supertrend`, und zwar mit einer klaren *Verschlechterung* (P = 2,4 %). Bei
`volatility_breakout` ist das Vorzeichen unbestimmt; bei
`volatility_breakout_crypto` ist nur die Drawdown-Reduktion gesichert
(P ≥ 99,2 %), nicht die daraus abgeleitete Calmar-Verbesserung.

Quer über die drei zeigt sich dieselbe Trennlinie wie in der Vertiefungsstudie:
**die Drawdown-Wirkung eines Trailing-Stops lässt sich beziffern, seine
risikoadjustierte Vorteilhaftigkeit nicht.** Die Rendite sinkt ähnlich
verlässlich wie der Drawdown; welcher Effekt in der Ratio überwiegt, hängt an
der Zusammensetzung des Betrachtungszeitraums.

**Keiner der beobachteten Effekte ist so gross, so gleichmässig über die Zeit
verteilt oder über die Bots hinweg so konsistent, dass sich daraus eine
allgemeine Aussage über volatilitäts-kalibrierte Trailing-Stops ableiten liesse.**
Für zwei der drei auswertbaren Bots wäre der Wechsel retrospektiv nachteilig
gewesen, für einen vorteilhaft — und dieser eine ist derselbe Bot, der bereits in
der Vol-Sizing-Untersuchung als Ausnahme aufgefallen ist. Die Entscheidung, ob
und was daraus folgt, liegt bewusst beim Nutzer in einer separaten, künftigen
Session.

---

## 12. Explizit ausserhalb des Scopes dieser Untersuchung

- Jede Live-Code-Änderung und jede Aktivierungsempfehlung.
- Das Einführen eines Stop-Mechanismus bei Bots, die aktuell bewusst keinen
  haben (`rsi2_crypto`, `rsi2_mean_reversion`, `turtle_soup_stocks`).
- Jede Änderung am strukturellen Stop von `turtle_soup_crypto`.
- Eine Optimierung des ATR-Fensters oder des Multiplikators über mehrere Werte
  (nur eine begründete Wahl plus eine einzelne Robustheits-Illustration).
- Eine Umstellung der Elliott-Wave-Backtests auf einen Einstieg zum
  Erkennungszeitpunkt statt zum Wellenende (siehe 5.4) — das wäre eine Änderung
  an der validierten Backtest-Konvention zweier Live-Bots.

## 13. Offene Fragen für eine mögliche Vertiefung

- Für die beiden Elliott-Wave-Bots ist die Frage nach Trailing-Stops **offen,
  nicht beantwortet**. Sie liesse sich nur mit einem Backtest beantworten, der
  zum Erkennungszeitpunkt des Musters einsteigt — dieselbe Korrektur, die
  `forward_test.py` bereits erhalten hat.
- Warum verhält sich `volatility_breakout_crypto` bei beiden
  volatilitätsbasierten Eingriffen anders als sein Aktien-Zwilling
  `volatility_breakout`, obwohl beide dieselbe Strategie-Logik fahren? Eine
  Analyse der Korrelation zwischen Trade-PnL und Volatilität zum
  Einstiegszeitpunkt (in der Vol-Sizing-Untersuchung bereits als offene Frage
  notiert) würde beide Untersuchungen gleichzeitig beantworten.
- Die Ratschen-Regel begrenzt die Wirkung der Volatilität auf den
  Einstiegszeitpunkt. Eine Variante mit *fest zum Einstieg* eingefrorener
  ATR-Distanz (statt balkenweiser Neuberechnung) würde den verbleibenden
  Volatilitäts-Kanal isolieren — bewusst nicht mitgetestet, um die Zahl der
  Varianten nicht zu vergrössern.

---

## 14. Reproduzierbarkeit

```
cd research/trailing_stops
python3 stop_inventory.py --json     # Schritt 1: Bestandsaufnahme aller 9 Bots
python3 test_atr_core.py             # 51 Sanity-Checks des Kernmoduls
python3 run_all.py                   # Bestandsaufnahme + Baseline-Checks + alle Laeufe
python3 aggregate_report.py          # Gesamttabellen + results/summary_table.json
```

Einzelne Schritte:

```
python3 verify_baseline.py <bot>     # Baseline-Regressionscheck fuer einen Bot
python3 run_one_bot.py <bot> [14|22] # Variantenrechnung fuer einen Bot
python3 run_all.py --verify          # nur die Baseline-Regressionschecks
```

Alle Läufe lesen ausschliesslich die bereits vorhandenen CSVs in `data/` — kein
Netzwerkzugriff. `python-binance` und `yfinance` werden als Stubs injiziert (sie
sind in dieser Sandbox nicht installiert und werden nicht benötigt);
`shared/fetch_binance_data.py` enthält Zugangsdaten, ist gitignored und wird
nicht gelesen.

### Dateien

| Datei | Inhalt |
|---|---|
| `stop_inventory.py` | Schritt 1: Klassifikation aller 9 Bots aus `live_params.py` |
| `atr_core.py` | ATR, Stop-Varianten, Ausstiegs-Simulation, Portfolio-Simulation, Kennzahlen |
| `test_atr_core.py` | 51 Sanity-Checks inkl. des synthetischen Volatilitäts-Testfalls und der Äquivalenz Schnellpfad ↔ Referenzpfad |
| `verify_baseline.py` | Regressionscheck gegen die bot-eigene `equity_simulation.py` |
| `run_one_bot.py` | Variantenrechnung für einen Bot (isolierter Prozess) |
| `run_all.py` | Orchestrierung aller Schritte |
| `decision_basis.py` | Buy-and-Hold, Reihenfolge-Sensitivität, Block-Bootstrap, NumPy-Schnellpfad |
| `aggregate_report.py` | Aggregation zu `results/summary_table.json` + Tabellen |
| `results/` | `stop_inventory.json`, `<bot>_atr14.json`, `<bot>_atr22.json`, `summary_table.json` |

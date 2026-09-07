# Parameter-Neubestimmung beider Elliott-Wave-Bots

> ## ALLE HIER GENANNTEN PARAMETER SIND UNVALIDIERTE VORSCHLÄGE
>
> Es wurde **nichts automatisch geändert** — `live_params.py` und
> `forward_test.py` beider Bots bleiben unangetastet (per `git diff` belegt,
> siehe Prüfung 14 in `test_params.py`). Eine Übernahme erfolgt
> ausschliesslich manuell und erst nach eigener Prüfung und ausdrücklicher
> Zustimmung des Auftraggebers.
>
> Derselbe Hinweis steht in **jeder** Ergebnisdatei unter dem Schlüssel
> `hinweis` und wird von jedem Skript beim Start und am Ende ausgegeben. Er
> ist bewusst nicht abschaltbar (`botenv.UNVALIDIERT_HINWEIS`).

---

## 0. Entscheidungsgrundlage

### Die beiden Antworten in einem Satz

**`elliott_wave` (Krypto): Ja, es existiert eine tragfähige Parametrisierung** —
Zigzag 10 % / Stop 6 %, das Fibonacci-Ziel ist dabei nahezu bedeutungslos. Sie
schlägt Buy-and-Hold über den Gesamtzeitraum in Rendite **und** Drawdown
deutlich. Der Vorbehalt: 130 Trades in fünf Jahren, davon 31 out-of-sample.

**`elliott_wave_stocks`: Nein, keine überzeugende.** Genau ein Kandidat besteht
die fünf mechanischen Bedingungen (Zigzag 2 % / Stop 16 % / kein Ziel), aber er
verliert im Walk-Forward in **zwei von drei Falten** risikoadjustiert gegen
Buy-and-Hold und bleibt über den Gesamtzeitraum mit +398 % weit hinter dessen
+756 %. Die aktuelle Live-Kombination ist nicht schlechter als die Alternativen —
sie ist nur genauso wenig überzeugend.

### Woher die Zahlen kommen

Diese Untersuchung rechnet **nicht** mit einer eigenen Backtest-Kopie.
Wellenerkennung und Trade-Simulation kommen aus dem seit PR #26 kausal
korrigierten Bot-Code selbst:

| Aufgabe | verwendete Bot-Funktion |
|---|---|
| Zigzag mit Bestätigungszeitpunkt | `zigzag_indicator.calculate_zigzag_with_confirmation` |
| kausale Wellenauswahl | `elliott_wave_counter.find_causal_waves` |
| Trade-Simulation | `backtest_elliott.run_backtest` |
| Kapitalsimulation | `equity_simulation.simulate_portfolio` |
| Bewertungsmass und Mindestfilter | `multi_symbol_optimise` (wörtlich) |
| Fenster-Split | `multi_symbol_walk_forward.split_all_symbols` |

Bezahlbar wird das über einen Wellen-Cache je (Fenster, Symbol, `deviation_pct`):
Zigzag und Wellenerkennung hängen **nur** von der Zigzag-Schwelle ab, nicht von
Stop oder Ziel. `test_params.py` belegt, dass der Cache dasselbe liefert wie eine
frische Berechnung, und dass der erzeugte Trade-Satz Zeile für Zeile identisch
zu `equity_simulation.collect_all_trades` des Bots ist.

### Pflicht-Gegenchecks

| Prüfung | Krypto | Aktien |
|---|---|---|
| Selbsttests `test_params.py` | **17/17** | **18/18** |
| Trade-Satz identisch zum Bot | ja (791 Trades) | ja (510 Trades) |
| Buy-and-Hold identisch zum Bot-Skript | kein eigenes vorhanden | ja (`buy_and_hold_benchmark.py`) |
| `robustness_score` identisch zum Bot | ja (200 Zufallsfälle) | ja |
| Mindestfilter-Entscheidung identisch zum Bot | ja | ja |
| IS/OOS je Symbol disjunkt und lückenlos | ja | ja |
| Walk-Forward-Testfenster liegt nach seinem Trainingsfenster | ja (3 Falten) | ja (3 Falten) |
| `live_params.py` / `forward_test.py` unverändert | **leerer Diff** | **leerer Diff** |

### Belastbarkeit

* **Krypto: dünn.** Der tragfähige Bereich erzeugt nur 130 Trades in fünf
  Jahren (97 in-sample, 31 out-of-sample). 31 liegt knapp über der geforderten
  Mindestzahl von 30. Ein einzelner guter Monat kann hier viel verschieben.
* **Aktien: breit, aber reihenfolgeabhängig.** 1785 Trades über 147 Aktien,
  davon 132 mit positivem Beitrag — das Muster ist nicht auf wenige Werte
  gestützt (Top-3-Anteil 8 %). Dafür verschiebt allein die Zeilenreihenfolge bei
  gleichzeitigen Einstiegen die Gesamtrendite zwischen +212 % und +509 %.
* **Der Suchraum ist endlich.** 252 Kombinationen je Fenster und Bot. Ein
  feineres Raster könnte Zwischenwerte finden; die Nachbarschaftsprüfung deutet
  aber nicht darauf hin, dass zwischen den Rasterpunkten viel liegt.

### Scope-Grenzen

* **Keine Änderung an `live_params.py` oder `forward_test.py`.** Keine
  Aktivierung, keine Empfehlung zum Weiterbetrieb oder zur Einstellung eines
  Bots — das bleibt eine bewusste, separate Entscheidung.
* **Kein Bot-Code angefasst.** Alles unterhalb `research/elliott_wave_params/`.
* **Nur die drei Rasterparameter** (`DEVIATION_PCT`, `STOP_LOSS_PCT`,
  `TAKE_PROFIT_FIB` bzw. kein Ziel). Positionslimit, Kapitalanteil,
  maximale Haltedauer, Kosten und `min_fib_score` bleiben, wie sie sind.

### Reproduktion

```
cd research/elliott_wave_params
python3 run_all.py                      # beide Bots, alles, rund 30 Minuten
python3 run_all.py elliott_wave         # nur ein Bot
python3 search.py elliott_wave_stocks   # nur die Rastersuche
```

---

## 1. Der Suchraum und warum er so aussieht

Das bisherige Raster (36 bzw. 64 Kombinationen) lag eng um Werte herum, die auf
der look-ahead-behafteten Grundlage gewonnen wurden — also um eine Mitte, die
sich als ungeeignet herausgestellt hat. Ein Raster um einen falschen Mittelpunkt
findet bestenfalls den besten falschen Punkt. Geöffnet wurde deshalb dort, wo es
einen sachlichen Grund gab:

| Achse | bisher | jetzt | Grund |
|---|---|---|---|
| `deviation_pct` | 2–5 % | **2–10 %** | Der Zigzag bestimmt, was überhaupt als Welle zählt. Mit dem korrigierten Einstieg kostet jede Bestätigung Kursbewegung — bei gröberen Zigzags fällt dieser Aufschlag relativ kleiner aus. Die Richtung war schlicht nie getestet. |
| `stop_loss_pct` | 2–4 % (Krypto), 2–8 % (Aktien) | **2–12 %** bzw. **2–16 %** | Im alten Backtest war der Stop bis zur Bestätigung mathematisch unerreichbar, also faktisch nie bindend und beliebig eng wählbar. Auf sauberer Grundlage ist er sofort bindend; 2 % auf Stundenkerzen ist enger als das normale Rauschen. |
| Ziel | Fib 0,236–0,5 | **Fib 0,236–1,0 plus „kein Ziel"** | Der Aktien-Bot hat „Gewinne laufen lassen" bereits als klar besser gemessen. Für den Krypto-Bot war das nie geprüft, weil dessen `run_backtest` kein solches Flag kennt. |

Das ergibt **7 × 6 × 6 = 252 Kombinationen** je Fenster und Bot — rund das
Sieben- bzw. Vierfache des alten Rasters, aber klein genug, dass jede einzelne
Zeile in `results/<bot>_grid_<fenster>.csv` nachrechenbar bleibt.

**„Kein Ziel" beim Krypto-Bot** wird über ein unerreichbar hohes Fibonacci-Ziel
(100,0) dargestellt, weil dessen `run_backtest` kein `use_take_profit`-Flag hat.
Dass es wirklich nie erreicht wird, ist gemessen und nicht angenommen: Prüfung 13
in `test_params.py` testet die ungünstigste Ecke des Suchraums (feinster Zigzag,
weitester Stop) auf exakt 0 % Take-Profit-Anteil. Zum Vergleich — Fib 5,0 trifft
je nach Einstellung noch bis zu 2,8 % der Trades, Fib 20,0 noch 0,2 %.

---

## 2. Das Urteil steht im Code, nicht im Fliesstext

Bei einer Parametersuche ist die Versuchung gross, im Nachhinein zu begründen,
warum ausgerechnet der beste Fund doch tragfähig sei. Die fünf Bedingungen stehen
deshalb in `summary.py` und gelten für jeden Kandidaten gleich:

| | Bedingung |
|---|---|
| **B1** | besteht die projekteigenen Mindestfilter im **In-Sample**-Fenster |
| **B2** | besteht sie auch **Out-of-Sample** — hilfsweise mit einer an die Fensterlänge angepassten Mindest-Trade-Zahl (beide Varianten werden ausgewiesen) |
| **B3** | **positiver Ø PnL in jeder** Walk-Forward-Falte — ein einzelner günstiger Abschnitt darf das Ergebnis nicht tragen |
| **B4** | verdient Out-of-Sample **überhaupt Geld** und schlägt dabei Buy-and-Hold im Calmar-Verhältnis |
| **B5** | **stabil**: Nachbar-Median ≥ 50 % des eigenen Scores, und Zigzag ± 0,5 pp lässt den Ø PnL nicht ins Minus kippen |

Zu **B2**: `MIN_TRADES` (30 bzw. 150) wurde für die volle Historie festgelegt.
Ein kürzeres Fenster scheitert sonst allein an seiner Länge — beim Aktien-Bot
fällt die Live-Kombination Out-of-Sample mit 128 statt 150 Trades durch, obwohl
ihr Ø PnL dort mit 7,52 % über dem aller anderen liegt. Die angepasste Variante
skaliert die Grenze mit der Zahl der Balken im Fenster (Aktien: 45 statt 150,
Krypto: 9 statt 30).

Kandidaten sind die **fünf besten In-Sample-Kombinationen** plus die aktuelle
Live-Kombination. Die Auswahl hat das Out-of-Sample-Fenster nie gesehen.

---

## 3. `elliott_wave` (Krypto) — Ja

**3 von 6 geprüften Kandidaten sind tragfähig**, alle bei **Zigzag 10 % /
Stop 6 %**; sie unterscheiden sich nur im Fibonacci-Ziel, das dabei fast keine
Rolle spielt.

| Kombination | B1..B5 | IS Ø PnL | OOS Ø PnL | OOS Calmar | Urteil |
|---|---|---|---|---|---|
| dev 10 % / Stop 6 % / Fib 0,618 | +++++ | 4,62 % | **3,23 %** | **2,29** | **tragfähig** |
| dev 10 % / Stop 6 % / Fib 1,0 | +++++ | 4,20 % | 3,32 % | 1,80 | **tragfähig** |
| dev 10 % / Stop 6 % / Fib 0,5 | +++++ | 4,73 % | 2,50 % | 1,60 | **tragfähig** |
| dev 10 % / Stop 6 % / Fib 0,382 | +-+-+ | 4,60 % | 1,76 % | 1,02 | scheitert an B4 (schlägt Buy-and-Hold nicht) |
| dev 10 % / Stop 4 % / Fib 0,5 | +---+ | 3,80 % | −0,93 % | −0,74 | scheitert an B2, B3, B4 |
| **dev 4 % / Stop 2 % / Fib 0,236 (live)** | ----- | −0,21 % | −0,87 % | −0,78 | scheitert an allen fünf |

### Gegen Buy-and-Hold

| Zigzag 10 % / Stop 6 % / Fib 0,618 | Gesamt (5 Jahre) | Out-of-Sample (18 Monate) |
|---|---|---|
| **Strategie** | **+67,77 %** / −10,17 % / Calmar **6,66** | +9,83 % / −4,30 % / Calmar **2,29** |
| Buy-and-Hold | +12,19 % / −79,76 % / Calmar 0,15 | **+88,28 %** / −60,15 % / Calmar 1,47 |

Über den Gesamtzeitraum ist der Vorsprung eindeutig — in beiden Massen. Im
Out-of-Sample-Fenster, achtzehn Monate stark steigender Markt, verliert die
Strategie an reiner Rendite um den Faktor neun und gewinnt nur noch knapp am
Calmar. Das ist kein Widerspruch, sondern die Eigenart einer Long-only-Strategie,
die die meiste Zeit in Cash liegt: sie verpasst Anstiege und übersteht Einbrüche.

### Walk-Forward

Das Verfahren wurde auf jedem Trainingsfenster **neu optimiert**. Alle drei
Falten kommen unabhängig voneinander bei Zigzag 10 % heraus, und alle drei
Testergebnisse sind positiv:

| Falte | Training bis | Sieger des Trainingsfensters | Test Ø PnL | Test Calmar | Buy-and-Hold Calmar |
|---|---|---|---|---|---|
| 1 | 2023-09-01 | dev 10 % / Stop 4 % / Fib 0,236 | +5,36 % | 4,78 | 2,78 |
| 2 | 2024-08-31 | dev 10 % / Stop 6 % / Fib 0,5 | +2,50 % | 1,73 | 1,76 |
| 3 | 2025-08-31 | dev 10 % / Stop 6 % / Fib 0,382 | +1,42 % | 0,66 | 1,03 |

Der beste Kandidat (Fib 0,618) über dieselben drei Testfenster: **+12,70 % /
+3,60 % / +3,04 %** bei Calmar 11,96 / 2,56 / 1,72 — in allen drei Falten besser
als Buy-and-Hold. Die Live-Kombination: +0,54 % / +0,27 % / −1,33 %.

Erkennbar ist auch ein **Abwärtstrend über die Falten** — von +12,7 % auf
+3,0 %. Das kann Zufall bei 26–28 Trades je Fenster sein, kann aber auch heissen,
dass das Muster mit der Zeit schwächer wird. Bei dieser Trade-Zahl lässt sich das
nicht auseinanderhalten.

### Stabilität

| Prüfung | Ergebnis (Fib 0,618) |
|---|---|
| Rasternachbarn In-Sample | Median **86,0 %** des eigenen Scores, 4/5 bestehen die Mindestfilter |
| Zigzag 9,5 / 10 / 10,5 % (gesamt) | Ø PnL 2,95 / 4,19 / 2,95 % — durchgehend positiv |
| Zigzag 9,5 / 10 / 10,5 % (out-of-sample) | Calmar 1,38 / 2,29 / 1,90 — durchgehend positiv |
| Reihenfolge gleichzeitiger Einstiege | ohne Einfluss (der Krypto-Bot hat kein Positionslimit) |

Kein Overfitting-Warnsignal. Zum Gegenbeispiel: **dev 10 % / Stop 4 %** sieht
In-Sample fast genauso gut aus (Score 0,966 gegen 1,043), kippt aber
Out-of-Sample bei ±0,5 pp Zigzag-Verschiebung zwischen Calmar −0,74 und +0,62 —
genau das Muster, das die Aufgabe als Warnsignal benannt sehen wollte. Der
Kandidat fällt entsprechend durch.

Die **Live-Kombination** ist kein knapp verfehlter Punkt: alle vier
Rasternachbarn sind ebenfalls negativ, und ±0,5 pp Zigzag ändert nichts
(Ø PnL −0,44 / −0,36 / −0,29 %). Es ist eine schlechte Gegend, kein Ausrutscher.

### Was den Unterschied macht

| | live (dev 4 / Stop 2) | Vorschlag (dev 10 / Stop 6) |
|---|---|---|
| Trades in 5 Jahren | 791 | 130 |
| Gewinnrate | 27,4 % | **43,8 %** |
| Anteil Stop-Loss-Ausstiege | **72,6 %** | 53,8 % |
| Symbole mit positivem Beitrag | 4 von 18 | **15 von 18** |

Der enge 2 %-Stop auf Stundenkerzen wird in drei von vier Trades ausgelöst,
bevor die erwartete Korrektur überhaupt Zeit hatte. Das ist die eigentliche
Ursache — und sie war im alten Backtest unsichtbar, weil der Stop dort bis zur
Bestätigung gar nicht erreichbar war.

---

## 4. `elliott_wave_stocks` — Nein

**1 von 6 geprüften Kandidaten** besteht die fünf Bedingungen. Bei näherem
Hinsehen trägt auch dieser nicht.

| Kombination | B1..B5 | IS Ø PnL | OOS Ø PnL | OOS Calmar | Urteil |
|---|---|---|---|---|---|
| dev 2 % / Stop 16 % / kein Ziel | +++++ | 5,74 % | 8,58 % | **22,64** | besteht formal |
| dev 4 % / Stop 16 % / kein Ziel | ++-++ | 6,77 % | 9,76 % | 14,27 | scheitert an B3 (Falte 1: −1,16 %) |
| dev 3 % / Stop 16 % / kein Ziel | ++-++ | 5,95 % | 9,00 % | 12,61 | scheitert an B3 (Falte 1: −0,17 %) |
| dev 6 % / Stop 16 % / kein Ziel | ++--- | 9,79 % | 10,41 % | 3,97 | scheitert an B3, B4, B5 |
| dev 6 % / Stop 16 % / Fib 1,0 | ++--+ | 7,71 % | 5,85 % | 1,21 | scheitert an B3, B4 |
| **dev 5 % / Stop 3 % / kein Ziel (live)** | ++-++ | 3,75 % | 7,52 % | 7,36 | scheitert an B3 (Falte 1: −1,47 %) |

### Warum auch der Sieger nicht trägt

**Erstens: Buy-and-Hold ist über den Gesamtzeitraum unschlagbar.**

| Gesamtzeitraum (10 Jahre) | Rendite | Max Drawdown | Calmar |
|---|---|---|---|
| **Buy-and-Hold** | **+755,69 %** | −34,83 % | **21,70** |
| dev 2 % / Stop 16 % / kein Ziel | +398,23 % | −34,16 % | 11,66 |
| dev 5 % / Stop 3 % (live) | +330,18 % | −22,70 % | 14,55 |

Keine der 252 Kombinationen kommt an die +755 % heran. Das ist die direkte Folge
der Look-Ahead-Korrektur: der Eintrag in `live_params.py` hält noch fest, die
Strategie schlage Buy-and-Hold „klar (1458 % vs. 756 %)" — auf sauberer
Grundlage gilt das nicht mehr.

**Zweitens: der Sieger verliert im Walk-Forward gegen Buy-and-Hold.**

| Testfenster | dev 2 % / Stop 16 % Calmar | Buy-and-Hold Calmar |
|---|---|---|
| F1 2020-09 .. 2022-09 | **3,59** | 1,58 |
| F2 2022-09 .. 2024-08 | 3,25 | **5,67** |
| F3 2024-09 .. 2026-09 | 2,44 | **3,93** |

Er gewinnt genau die Falte, die den Bärenmarkt 2022 enthält, und verliert die
beiden folgenden. Das passt zum Bild aus Abschnitt 3: eine Long-only-Strategie
mit viel Cash schützt im Einbruch und bleibt im Anstieg zurück.

**Drittens: die Zahl ist nicht scharf.** Bei Positionslimit 8 entscheidet die
Zeilenreihenfolge, welcher von mehreren gleichzeitigen Einstiegen den letzten
freien Platz bekommt. Über 200 zufällige Permutationen (fester Startwert)
schwankt die Gesamtrendite des Siegers zwischen **+211,58 % und +508,89 %**
(Spanne 297 pp), der Calmar zwischen **6,25 und 17,45**. Die einzelne Zahl
+398 % sollte niemand als präzise lesen — das ist derselbe Effekt, den PR #23
über alle neun Bots gezeigt hat.

### Was der Vergleich trotzdem hergibt

* **Ein festes Kursziel schadet durchgehend.** Unter den 116 Kombinationen, die
  auf dem Gesamtfenster die Mindestfilter bestehen, sind die vorderen zehn
  praktisch ausnahmslos „kein Ziel". Die Entscheidung `USE_TAKE_PROFIT = False`
  von 2026-09-03 hält auf sauberer Grundlage also stand.
* **Weite Stops sind besser als enge.** Die In-Sample-Spitze liegt geschlossen
  bei Stop 16 % — dem grössten getesteten Wert. Der Suchraum ist an dieser Kante
  also möglicherweise noch nicht ausgereizt; das wäre eine eigene Untersuchung.
* **Die Live-Kombination ist nicht der Fehler.** Sie liegt auf dem Gesamtfenster
  auf Rang 10 von 116, In-Sample auf Rang 16 von 95, und ihr Ø PnL ist
  Out-of-Sample mit 7,52 % der beste aller Kandidaten. Sie scheitert an
  denselben Falten wie fast alle anderen.

---

## 5. Symbol-Auswahl: kein Hebel

Die Aufgabe nennt „ggf. andere Symbol-Auswahl" als Richtung. Symbole nach ihrem
Ergebnis auszuwählen ist die schnellste Art, sich einen Backtest schönzurechnen —
gemessen wurde deshalb mit demselben IS/OOS-Trennstrich wie bei den Parametern:
Auswahl **ausschliesslich** nach In-Sample-Ergebnis, Auswertung unverändert
Out-of-Sample.

| Krypto, dev 10 % / Stop 6 % | alle 18 Symbole | nur die In-Sample-positiven |
|---|---|---|
| Fib 0,618 | Ø 3,23 %, Calmar 2,29 | Ø 3,62 %, Calmar 2,78 |
| Fib 0,5 | Ø 2,50 %, Calmar 1,60 | Ø 2,04 %, Calmar 1,25 |
| Fib 0,382 | Ø 1,76 %, Calmar 1,02 | Ø 1,20 %, Calmar 0,66 |

Mal besser, mal schlechter — kein konsistenter Vorteil. Die Beitragsverteilung
spricht ebenfalls gegen einen Hebel: beim Krypto-Vorschlag sind 15 von 18
Symbolen positiv, beim Aktien-Sieger 132 von 147 (Top-3-Anteil nur 8 %). Das
Muster hängt nicht an wenigen Märkten, also ist bei deren Auswahl auch nichts
zu holen.

---

## 6. Zwei Funde am Rande, die über diese Untersuchung hinausgehen

**Der Bot benutzt zwei verschiedene Zeilenreihenfolgen.**
`multi_symbol_optimise.evaluate_combination_multi` — das Skript, das die
bisherige Parameterwahl getragen hat — hängt die Symbol-Blöcke aneinander und
rechnet seinen Drawdown auf dieser Reihenfolge; `equity_simulation` sortiert
chronologisch. Dieselbe Trade-Menge des Aktien-Bots ergibt so −82,5 % gegenüber
−259,9 % kumulierten Drawdown, also einen um den Faktor drei verschobenen
Projekt-Score. Die Symbol-Block-Reihenfolge beschreibt keinen Verlauf, den man
erleben könnte — sie ist ein Nebenprodukt der Art, wie das Skript seine
Teilergebnisse aneinanderhängt. Diese Untersuchung bildet **beide** Pfade exakt
nach und weist beide Drawdowns aus (`max_drawdown_pct` und
`max_drawdown_chronologisch_pct`), damit die Rangfolge mit früheren Ergebnissen
vergleichbar bleibt und der Unterschied trotzdem sichtbar ist.

**Eine Kurslücke vergiftet die Kapitalkurve.** Der letzte Balken von `APH` ist in
den Daten leer. Jede Kombination, bei der ein APH-Trade dort per Zeitausstieg
endet, lieferte NaN als Portfolio-Rendite — und der Projekt-Score merkte nichts
davon, weil pandas beim Mitteln NaN überspringt. Die Rangfolge blieb also gültig,
während die Portfolio-Kennzahl daneben unbrauchbar war (sichtbar unter anderem
bei Zigzag 6 % / Stop 16 %, einer der vorderen Kombinationen).
`buy_and_hold_benchmark.py` des Aktien-Bots geht mit demselben Problem schon
richtig um; der Trade-Pfad tat es nicht. Hier werden solche Trades gestrichen und
gezählt. **Der Bot selbst hat diese Lücke weiterhin** — das ist eine mögliche
Folgeaufgabe, keine hier vorgenommene Änderung.

---

## 7. Getroffene Annahmen

**P-A1 — Bewertet wird mit dem Projekt-Score, nicht mit dem Calmar.** Die
Rangfolge im Raster benutzt `robustness_score` aus `multi_symbol_optimise`,
wörtlich übernommen, damit die Ergebnisse mit den früheren vergleichbar bleiben.
Die Portfolio-Kennzahlen inklusive Calmar stehen in jeder Zeile daneben und
tragen über B4 zum Urteil bei.

**P-A2 — Der IS/OOS-Split ist der des Projekts (70/30 je Symbol nach
Zeilenanteil).** Das hat einen Nebeneffekt: bei unterschiedlich langen Historien
fällt das In-Sample-Fenster eines langen Symbols kalendarisch mit dem
Out-of-Sample-Fenster eines kurzen zusammen. Beim Krypto-Bot überlappen die
Fenster dadurch um rund neun Monate. **Der Walk-Forward trennt deshalb nach
Kalenderdatum** — ein Testfenster enthält dort ausschliesslich Marktphasen, die
in keinem Trainingsfenster vorkommen. Wo IS/OOS und Walk-Forward sich
widersprechen, ist der Walk-Forward der belastbarere.

**P-A3 — „Kein Ziel" beim Krypto-Bot ist ein Fibonacci-Ziel von 100,0.** Dessen
`run_backtest` kennt kein `use_take_profit`-Flag, und dieses zu ergänzen wäre
eine Bot-Code-Änderung ausserhalb des Auftrags. Dass das Ziel nie erreicht wird,
ist gemessen (Prüfung 13), nicht angenommen.

**P-A4 — Die Mindestfilter gelten unverändert auch auf kürzeren Fenstern**,
zusätzlich in einer an die Fensterlänge angepassten Variante. Beide Verdikte
stehen in `results/<bot>_summary.json`; B2 gilt, wenn eine der beiden Varianten
besteht.

**P-A5 — Bei gleichzeitigen Einstiegen wird stabil sortiert** (`kind="stable"`),
damit ein Lauf reproduzierbar ist. Der Bot sortiert instabil; die Differenz ist
gemessen und ausgewiesen (Aktien: 330,18 % gegenüber 352,72 % bei identischem
Trade-Satz) und die volle Streuung über 200 Permutationen steht im Bericht.

**P-A6 — Kandidaten sind die fünf besten In-Sample-Kombinationen plus die
Live-Kombination.** Eine breitere Kandidatenliste könnte Kombinationen finden,
die In-Sample mittelmässig und Out-of-Sample gut sind — solche gezielt zu suchen
wäre aber genau der Griff nach dem Out-of-Sample-Fenster, den die Trennung
verhindern soll.

---

## 8. Offene Punkte

Beobachtungen, keine Aufträge — die Entscheidung liegt beim Auftraggeber:

1. **Der Aktien-Suchraum ist an der Stop-Kante nicht ausgereizt.** Die
   In-Sample-Spitze liegt geschlossen beim grössten getesteten Stop (16 %).
   Ob jenseits davon noch etwas liegt, ist offen.
2. **Die Kurslücke in `APH`** trifft den Bot selbst genauso — `equity_simulation`
   würde dieselbe NaN-Kapitalkurve erzeugen. Eine kleine Absicherung im
   Bot-Code wäre naheliegend.
3. **Die zwei Zeilenreihenfolgen** (Abschnitt 6) betreffen jede künftige
   Rasteroptimierung aller neun Bots, nicht nur diese Untersuchung.
4. **Der Eintrag in `strategies/elliott_wave_stocks/live_params.py`** hält
   Zahlen fest, die auf der look-ahead-behafteten Grundlage entstanden sind
   („schlägt Buy-and-Hold klar, 1458 % vs. 756 %"). Eine Aktualisierung des
   Kommentars wäre ehrlich — sie wurde hier bewusst nicht vorgenommen, weil die
   Datei ausserhalb des Auftrags liegt.
5. **Weiterbetrieb beider Bots** — unverändert offen und ausdrücklich nicht
   Gegenstand dieser Untersuchung.

---

## 9. Dateien

| Datei | Rolle |
|---|---|
| `botenv.py` | Bot-Umgebung, Stubs (werfen bei Aufruf), fester UNVALIDIERT-Hinweis |
| `engine.py` | Fenster, Wellen-Cache, Trades, Projekt-Score, Portfolio, Buy-and-Hold |
| `search.py` | Suchraum und Rastersuche auf gesamt / In-Sample / Out-of-Sample |
| `walkforward.py` | drei anchored Falten mit Kalendergrenzen; Kandidaten **und** Verfahren |
| `stability.py` | Rasternachbarschaft, Zigzag ± 0,5 pp, Reihenfolge-Permutationen |
| `symbols.py` | Beitragsverteilung und ehrlicher Symbol-Auswahltest |
| `benchmark.py` | Buy-and-Hold je Fenster |
| `summary.py` | die fünf Bedingungen und das mechanische Urteil |
| `test_params.py` | Selbsttests gegen den Bot-Code |
| `run_all.py` | alles nacheinander, ein Prozess je Bot und Schritt |
| `results/<bot>_search.json` | vollständige Rasterergebnisse, Top 10 je Fenster |
| `results/<bot>_grid_<fenster>.csv` | jede einzelne Kombination, nachrechenbar |
| `results/<bot>_walkforward.json` | Falten, Trainingssieger, Kandidaten je Testfenster |
| `results/<bot>_stability.json` | Nachbarschaft, Feinschritt, Reihenfolge-Streuung |
| `results/<bot>_symbols.json` | Beitrag je Symbol, Auswahltest |
| `results/<bot>_buyhold.json` | Buy-and-Hold je Fenster |
| `results/<bot>_summary.json` | Bedingungen und Urteil je Kandidat |

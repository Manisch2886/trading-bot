# TB-25 — Tragen die Stufen des `fib_score` etwas?

> ## DIES IST EINE MESSUNG, KEINE EMPFEHLUNG UND KEINE ÄNDERUNG
>
> Es wurde **nichts am Bot-Code geändert**. `git diff origin/main...HEAD --name-only`
> listet ausschliesslich Dateien unter `research/` und `docs/` — nachgewiesen in
> `test_stufen.py`, Prüfungen 27–29. `live_params.py`, `forward_test.py`,
> `elliott_wave_counter.py`, `zigzag_indicator.py`, `backtest_elliott.py`,
> `equity_simulation.py` und `multi_symbol_optimise.py` beider Bots sind
> unangetastet.
>
> Was aus dem Ergebnis folgt — Schwelle ändern, Auswahlregel ändern, den Bot in
> Frage stellen —, entscheidet der Nutzer. Derselbe Hinweis steht in jeder
> Ergebnisdatei unter dem Schlüssel `hinweis` und wird von jedem Skript beim
> Start und am Ende ausgegeben (`botenv.UNTERSUCHUNG_HINWEIS`, nicht abschaltbar).

---

## 0. Die Antwort

### Welcher der drei Ausgänge ist eingetreten?

**Ausgang 2: „Kein Unterschied zwischen den Stufen" — für beide Bots.**

> *„Dann bleibt vom Elliott-Wave-Bot ein Zigzag-Detektor mit Stop."*

Die Punktwerte steigen zwar bei beiden Bots monoton mit der Stufe. Aber **kein
einziger Schritt von einer Stufe zur nächsten** ist von null zu unterscheiden:

| Schritt | `elliott_wave` | `elliott_wave_stocks` |
|---|---|---|
| Stufe 1 gegen Stufe 0 | +3,83 pp, CI **[−0,04; +7,91]**, p = 0,059 | +0,99 pp, CI [−1,90; +4,06], p = 0,54 |
| Stufe 2 gegen Stufe 1 | **+0,12 pp**, CI [−5,17; +5,40], p = 0,97 | **+0,21 pp**, CI [−3,86; +4,56], p = 0,92 |
| Stufe 3 gegen Stufe 2 | +6,40 pp, CI [−7,79; +20,77], p = 0,36 | +3,72 pp, CI [−3,99; +12,29], p = 0,44 |

Der mittlere Schritt ist der aussagekräftigste, weil beide Gruppen gross genug
sind — und er ist bei beiden Bots **praktisch exakt null** (+0,12 bzw. +0,21
Prozentpunkte). Zwischen „eine Bedingung erfüllt" und „zwei Bedingungen erfüllt"
liegt in den Daten nichts.

### Der eine Vorbehalt, der dazugehört

Beim Krypto-Bot ist die **Schwelle selbst** — Stufe 0 gegen alles darüber — als
einziger Vergleich unter 5 %:

| | Wert |
|---|---|
| Stufe ≥ 1 gegen Stufe 0 | **+4,12 pp** (4,19 % gegen 0,07 %) |
| Bootstrap-Intervall über Trades | [+0,70; +7,48] |
| Bootstrap-Intervall über **Symbole** | [+1,26; +7,29] |
| Permutations-p | **0,028** |
| Trefferquote | 43,8 % gegen 28,4 % (+15,4 pp) |
| Weglassprobe (jedes der 18 Symbole einmal raus) | +3,20 bis +4,76 pp, Vorzeichen bleibt |
| Spearman(Stufe, PnL) | +0,164, p = 0,014 |

Das ist **ein** auffälliger Vergleich unter **22**; rein zufällig wäre gut einer
zu erwarten. Die Weglassprobe zeigt immerhin, dass er nicht an einem einzelnen
Coin hängt. Beim Aktien-Bot ist dieselbe Zahl **+1,19 pp, CI [−1,45; +3,93],
p = 0,41** — also nichts.

Und selbst dieser Befund trägt die Stufen-Lesart nicht, denn er ist **kein
Stufeneffekt**: Abschnitt 5 zeigt, dass er fast vollständig von **einer einzigen
der drei Bedingungen** getragen wird, nicht von ihrer Anzahl.

### Die Nebenfrage aus Punkt 1

**Ja** — alle drei Bedingungen sind Schwellen auf einer stetigen Grösse. Unter
dem Score existiert also eine feinere Messung, und sie liesse sich als stetiger
Primärschlüssel benutzen. **Gemessen trägt sie aber nicht mehr als die Stufe:**
Spearman der stetigen Nähe gegen die Rendite +0,109 (p = 0,10) beim Krypto-Bot
und +0,038 (p = 0,28) beim Aktien-Bot. Einzelheiten in Abschnitt 2.

---

## 1. Was gemessen wurde, und womit

### Die echten Bot-Funktionen, nicht eine Nachbildung

| Aufgabe | verwendete Bot-Funktion |
|---|---|
| Kursdaten laden (inkl. Lückenbereinigung, PR #81) | `multi_symbol_optimise.load_all_symbol_data` |
| Zigzag mit Bestätigungszeitpunkt | `zigzag_indicator.calculate_zigzag_with_confirmation` |
| kausale Wellenauswahl | `elliott_wave_counter.find_causal_waves` |
| Bewertung der Wellen | `elliott_wave_counter.fibonacci_score` (über die Spalte `fib_score`) |
| Trade-Simulation mit Stop, Ziel und Zeitausstieg | `backtest_elliott.run_backtest` |
| Parameter | `live_params.py` |

Nachgebildet wird genau **eine** Sache: die **Zerlegung** des Scores — welche der
drei Bedingungen erfüllt ist. Der Bot gibt sie nicht aus; aus einer 0,33 ist
nicht ablesbar, ob die Welle-3- oder die Welle-4-Bedingung dahintersteht, und
genau das fragt Punkt 3 des Auftrags. Damit die Nachbildung nicht abdriften
kann, wird sie gegen die echte `fibonacci_score()` gerechnet:

* auf **jedem** gemessenen Muster beider Bots (225 bzw. 813): identisch,
* auf **20 000 Zufallspunkten** je Bot, darunter 400 entartete Fälle
  (`wave1 == 0`, `wave3 == 0`): **0 Abweichungen**.

### Datengrundlage

| | `elliott_wave` | `elliott_wave_stocks` |
|---|---:|---:|
| Symbole (nach den Mindestfiltern des Bots) | 18 | 147 |
| Kerzen | 706 362 (1 h) | 361 942 (1 Tag) |
| Zeitraum | 2021-09-01 bis 2026-08-31 | 2016-08-31 bis 2026-09-01 |
| Parameter (aus `live_params.py`) | Zigzag 10 %, Stop 6 %, Ziel Fib 0,618 | Zigzag 5 %, Stop 3 %, **kein Kursziel** |
| Frische-Fenster | 48 Balken | 5 Balken |
| Notausstieg | 240 Balken | 90 Balken |
| Muster mit Trade | **225** | **813** |
| davon oberhalb der Bot-Schwelle | 130 | 510 |

Die 130 und die 510 sind **dieselben Zahlen**, die
`research/elliott_wave_params/BERICHT.md` für diese beiden Live-Kombinationen
nennt (130 Trades in fünf Jahren, 510 Trades) — ein unabhängiger Beleg dafür,
dass hier derselbe Trade-Satz gerechnet wird wie dort.

### Wie Stufe 0 überhaupt in die Messung kommt

Der Bot läuft mit `min_fib_score = 0.3`; Stufe 0 kommt dort nie vor. Der Auftrag
verlangt sie aber ausdrücklich als Vergleichspunkt. Der Lauf setzt die Schwelle
deshalb auf **0.0**.

Das ist kein harmloser Parameterwechsel: `remove_overlapping` bildet
Überlappungsgruppen greedy in chronologischer Reihenfolge, zusätzliche
Stufe-0-Kandidaten könnten also theoretisch die Gruppenbildung verschieben und
damit auch die Muster **oberhalb** der Schwelle verändern. Deshalb rechnet der
Lauf beide Varianten und vergleicht sie:

| | `elliott_wave` | `elliott_wave_stocks` |
|---|---:|---:|
| Lauf A, `min_fib_score = 0.3` | 130 Trades | 510 Trades |
| Lauf B, Stufen 1–3 aus `min_fib_score = 0.0` | 130 Trades | 510 Trades |
| Zeile für Zeile identisch (9 Spalten: Symbol, Signal-, Einstiegs-, Ausstiegszeit, Preise, Ergebnisart, PnL, Score) | **ja** | **ja** |

Die Stufen 1–3 sind also **exakt der Bot**; Stufe 0 kommt sauber daneben.

### Kausalität — der korrigierte Pfad (PR #26)

Bestätigt, und zwar mechanisch statt per Zusicherung: `run_backtest` **wirft eine
`ValueError`**, wenn die Wellen keine Spalte `entry_idx` mitbringen. Diese Spalte
liefert nur `find_causal_waves`. Ein Lauf mit Look-Ahead ist auf diesem Pfad also
gar nicht möglich; `test_stufen.py` prüft das, indem es den Fehlschlag provoziert.
Eingestiegen wird zum **Schlusskurs des Bestätigungsbalkens**, nicht zum Preis
des Wellenende-Pivots.

---

## 2. Die Nebenfrage: Gibt es unter dem Score eine stetige Grösse?

### Ja — und es sind Intervalle, keine Toleranzen um ein Ziel

Alle drei Bedingungen prüfen ein **Verhältnis zweier Wellenlängen** gegen ein
Intervall:

| Bedingung | Teilpunkte | Intervall | kanonischer Fibonacci-Wert | liegt … |
|---|---:|---|---:|---|
| Welle 2 / Welle 1 | **0,34** | [0,500 ; 0,618] | 0,618 | auf dem **oberen Rand** |
| Welle 3 / Welle 1 | 0,33 | [1,400 ; 1,800] | 1,618 | unsymmetrisch innen |
| Welle 4 / Welle 3 | 0,33 | [0,236 ; 0,382] | 0,382 | auf dem **oberen Rand** |

Die im Auftrag vermutete Form „Retracement liegt innerhalb ±5 % von 0,618" trifft
also **nicht** zu: der Code prüft Intervalle, und die kanonischen
Fibonacci-Werte, auf die sie sich beziehen, liegen bei zwei von drei Bedingungen
auf dem Rand. Einen im Code benannten Zielwert, zu dem sich ein Abstand messen
liesse, gibt es nicht. Der Abstand wird deshalb **auf das Intervall selbst**
normiert:

```
m = (lo + hi) / 2      Intervallmitte
h = (hi - lo) / 2      halbe Intervallbreite
d = |r - m| / h        normierter Abstand   →   d ≤ 1  ⟺  Bedingung erfüllt
```

Dass `d ≤ 1` und „Bedingung erfüllt" wirklich dasselbe sind, prüft
`test_stufen.py` auf 5 000 Zufallspunkten je Bot (0 Abweichungen).

### Vier Fassungen, damit die Antwort nicht an einer Formel hängt

| Mass | Definition | Eigenschaft |
|---|---|---|
| `naehe` | Mittel von `max(0, 1−d)` | [0, 1]; **sättigt** bei 0 |
| `naehe_fib` | dasselbe, Anker = kanonischer Fibonacci-Wert | [0, 1]; sättigt ebenfalls |
| `gesamtabstand` | Mittel der drei `d` | unbeschränkt; von Welle 3 dominiert |
| `naehe_weich` | Mittel von `1/(1+d)` | (0, 1]; **sättigt nirgends** |

Die Sättigung ist kein Schönheitsfehler, sondern der entscheidende Punkt:
`max(0, 1−d)` ist für **jedes** `d > 1` gleich null. Alle Muster ohne erfüllte
Bedingung bekommen damit denselben Wert — beim Krypto-Bot 42,2 %, beim Aktien-Bot
37,3 % aller Muster. Genau dort, wo die Stufe nichts mehr unterscheidet,
unterscheidet auch `naehe` nichts mehr. `naehe_weich` hat diese Stelle nicht.

### Gemessen trägt die stetige Grösse nicht mehr als die Stufe

Rangkorrelation gegen die Nettorendite, zweiseitiger Permutationstest:

| Grösse | `elliott_wave` (n = 225) | `elliott_wave_stocks` (n = 813) |
|---|---|---|
| Stufe (0–3) | ρ = **+0,164**, p = 0,014 | ρ = +0,039, p = 0,27 |
| `naehe` | ρ = +0,109, p = 0,10 | ρ = +0,038, p = 0,28 |
| `naehe_fib` | ρ = +0,127, p = 0,055 | ρ = +0,054, p = 0,13 |
| `naehe_weich` | ρ = +0,130, p = 0,052 | ρ = +0,054, p = 0,12 |
| `gesamtabstand` | ρ = −0,111, p = 0,096 | ρ = −0,051, p = 0,15 |

Die stetigen Fassungen liegen beim Krypto-Bot **unterhalb** der groben Stufe und
beim Aktien-Bot wie diese bei null. Die Quartile der `naehe` steigen zwar
(Krypto 1,52 % → 2,90 % → 3,88 %; Aktien 3,43 % → 5,58 % → 4,99 %), aber alle
Intervalle überlappen einander.

**Antwort auf die Frage „Gibt es einen stetigen Primärschlüssel?"**: technisch
ja, und er wäre auch **eindeutig** — was der `fib_score` nicht ist:

| | `elliott_wave` | `elliott_wave_stocks` |
|---|---:|---:|
| Muster, die ihren `fib_score` je Symbol mit einem anderen teilen | **85,8 %** | **73,6 %** |
| dasselbe für `naehe_weich` | **0,0 %** | **0,0 %** |
| verschiedene Werte | 6 gegen **225** | 6 gegen **813** |

Ein Ranking auf `naehe_weich` hätte also keine Gleichstände mehr. Nur: **es gibt
keinen gemessenen Grund, in dieser Rangfolge zu ranken.** Eindeutigkeit ohne
Trennschärfe ersetzt einen willkürlichen Tie-Break durch einen sauberer
aussehenden — nicht durch einen begründeten.

---

## 3. Die Stufenauswertung

Nettorendite über die **tatsächliche Bot-Haltedauer**, mit Stop, Kursziel und
Zeitausstieg des Bots, nach Gebühren und Slippage (2 × 0,15 %).

### `elliott_wave` (Krypto, 1 h)

| Stufe | n | Symbole | Mittel | Median | CI 95 % (Trades) | CI 95 % (Symbole) | Treffer | Stop | Zeit | Ziel |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|---:|
| 0 | 95 | 17 | **0,07 %** | −6,30 % | [−2,13; +2,55] | [−2,31; +2,43] | 28,4 % | 66 | 21 | 8 |
| 1 | 83 | 18 | **3,90 %** | −6,30 % | [+0,86; +7,33] | [+1,37; +6,19] | 43,4 % | 46 | 27 | 10 |
| 2 | 42 | 16 | **4,02 %** | −6,30 % | [+0,05; +8,29] | [+0,80; +7,35] | 42,9 % | 22 | 15 | 5 |
| 3 | **5** | 4 | 10,42 % | +6,74 % | [−3,69; +24,54] | [−6,30; +21,57] | 60,0 % | 2 | 2 | 1 |

### `elliott_wave_stocks` (Aktien, 1 Tag)

| Stufe | n | Symbole | Mittel | Median | CI 95 % (Trades) | CI 95 % (Symbole) | Treffer | Stop | Zeit |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| 0 | 303 | 116 | **3,61 %** | −3,30 % | [+1,77; +5,52] | [+1,92; +5,50] | 20,1 % | 242 | 61 |
| 1 | 363 | 125 | **4,59 %** | −3,30 % | [+2,48; +7,05] | [+2,67; +6,94] | 20,1 % | 288 | 75 |
| 2 | 127 | 87 | **4,81 %** | −3,30 % | [+1,64; +8,52] | [+1,68; +8,78] | 22,0 % | 99 | 28 |
| 3 | **20** | 19 | 8,53 % | −3,30 % | [+1,78; +16,48] | [+2,42; +15,85] | 40,0 % | 11 | 9 |

**Was an diesen Tabellen zuerst auffällt, ist nicht der Mittelwert.** Der
**Median ist in sieben von acht Gruppen exakt der Stop** (−6,30 % bzw. −3,30 %,
Stop plus Kosten) — in jeder Gruppe ausser der fünf Trades umfassenden Stufe 3
des Krypto-Bots endet also mindestens die Hälfte der Trades am Stop. Was sich
zwischen den Stufen bewegt, ist nicht der typische Trade, sondern der Rand der
Verteilung.

**Stufe 3 trägt keine Aussage** — 5 bzw. 20 Trades, wie der Auftrag es
vorweggenommen hat („Eine Stufe mit zwölf Mustern trägt keine Aussage"). Ihre
Intervalle sind 28 bzw. 15 Prozentpunkte breit. Die Auswertung markiert jede
Gruppe unter 30 Trades ausdrücklich als `aussagekraeftig: false`.

**Die Stufen liegen nicht in unterschiedlichen Marktphasen.** Der mediane
Einstiegszeitpunkt liegt beim Krypto-Bot für alle vier Stufen zwischen
2024-03-18 und 2024-08-05, beim Aktien-Bot zwischen 2022-03-16 und 2022-09-26;
auch die Jahresverteilungen ähneln einander (`results/*_auswertung.json`,
`zeitliche_verteilung`). Ein Stufenunterschied wäre also nicht allein damit zu
erklären, dass eine Stufe in besseren Zeiten häufiger vorkommt — und umgekehrt
verbirgt eine Phasenverschiebung auch keinen.

**Die Haltedauer steigt mit der Stufe** (Median: Krypto 67 → 79 → 130 → 197
Stunden, Aktien 6 → 6 → 11 → 30 Kalendertage), und der Anteil der Stopp-Ausstiege
fällt (Krypto 69 % → 55 % → 52 % → 40 %). Das ist keine zweite Beobachtung neben
der Rendite, sondern dieselbe von der anderen Seite: ein Trade, der nicht früh
ausgestoppt wird, lebt länger **und** verdient mehr. Es ist deshalb kein
Störfaktor — aber es sagt, wo der Unterschied sitzt: am frühen Stopp, nicht an
der Zielerreichung.

---

## 4. Das Rundungsartefakt (Punkt 3)

### Die Erwartung bestätigt sich: kein Renditeunterschied

Innerhalb der Stufe „genau eine Bedingung erfüllt":

| | `elliott_wave` | `elliott_wave_stocks` |
|---|---|---|
| 0,34 | 4,30 % (n = 27) | 6,79 % (n = 75) |
| 0,33 | 3,71 % (n = 56) | 4,02 % (n = 288) |
| Differenz | +0,59 pp, CI [−6,20; +7,56], p = **0,87** | +2,77 pp, CI [−2,80; +9,39], p = **0,34** |

Dasselbe in Stufe 2 (0,67 gegen 0,66): +1,98 pp (p = 0,65) bzw. −2,41 pp
(p = 0,52) — einmal in die eine, einmal in die andere Richtung.

### Was die 0,34 trägt — und warum das trotzdem ein Befund ist

**0,34 kann nur von der Welle-2-Bedingung kommen** (exhaustiv über alle acht
Kombinationen geprüft, `test_stufen.py`). Dasselbe gilt für 0,67. Der Tie-Break
ist damit **nicht zufällig, sondern deterministisch**: bei genau einer erfüllten
Bedingung steht immer das Welle-2-Muster vorn.

Und genau das ist die unangenehme Stelle. Die 0,33-Gruppe ist keine homogene
Vergleichsgruppe, sondern eine **Mischung aus der schlechtesten und der besten**
Einzelbedingung:

| Stufe-1-Untergruppe | `fib_score` | Krypto n / Mittel | Aktien n / Mittel |
|---|---:|---|---|
| nur Welle 2 | **0,34** | 27 / 4,30 % | 75 / 6,79 % |
| nur Welle 3 | 0,33 | 23 / **−0,06 %** | 94 / **1,94 %** |
| nur Welle 4 | 0,33 | 33 / **6,34 %** | 194 / **5,03 %** |

Der Rundungsvorzug hebt also die Welle-2-Gruppe über eine Gruppe, in der die
**bestlaufende** Einzelbedingung (Welle 4) steckt. Er wirkt — nur eben nicht in
die Richtung, in die er wirken müsste, wenn er begründet wäre. *Gewählt hat ihn
niemand.*

> **Anmerkung zur Reichweite.** TB-19/TB-20 haben gezeigt, dass die Rangfolge
> innerhalb eines Symbols heute **keinen einzigen Live-Trade** verschiebt (in
> 0 von 20 114 nachgebildeten Läufen standen zwei neue Muster desselben Symbols
> gleichzeitig zur Auswahl). Der Tie-Break ist also ein Konstruktionsfehler ohne
> gemessene Wirkung — er würde erst wirken, wenn je eine Zuteilungsregel über
> Symbole hinweg auf `fib_score` rankt.

---

## 5. Die Zerlegung — was die Stufe verdeckt

Die Stufe zählt, **wie viele** Bedingungen gelten. Dass die drei gleichwertig
wären, steht damit nicht fest. Gemessen sind sie es nicht:

| Bedingung | `elliott_wave` | | `elliott_wave_stocks` | |
|---|---|---|---|---|
| | Differenz (erfüllt − nicht) | p | Differenz | p |
| Welle 2 / Welle 1 | +3,53 pp, CI [−0,90; +8,03] | 0,10 | +1,68 pp, CI [−1,61; +5,38] | 0,33 |
| Welle 3 / Welle 1 | **−0,24 pp**, CI [−4,18; +3,78] | 0,91 | **−0,79 pp**, CI [−3,55; +2,18] | 0,63 |
| Welle 4 / Welle 3 | **+4,88 pp**, CI [+0,85; +9,13] | **0,012** | +1,82 pp, CI [−1,10; +4,92] | 0,22 |

Die **Reihenfolge ist bei beiden Bots dieselbe**: Welle 4 > Welle 2 > Welle 3,
und die Welle-3-Bedingung liegt bei beiden **unter null**. Das ist die einzige
Struktur, die diese Untersuchung über beide Bots hinweg reproduzieren konnte —
und sie widerspricht der Stufen-Lesart, denn sie sagt: es kommt nicht auf die
**Anzahl** an, sondern darauf, **welche** Bedingung gilt.

Auch der Krypto-Befund aus Abschnitt 0 löst sich hier auf: von den +4,12 pp an
der Schwelle stammen +4,88 pp aus der Welle-4-Bedingung allein. Die stetige
Fassung sagt dasselbe — nur die Welle-4-Grösse korreliert überhaupt mit der
Rendite (ρ = −0,166 für den Abstand, p = 0,011; Welle 2: p = 0,11; Welle 3:
p = 0,58).

**Drei Vorbehalte, die dazugehören:**

1. Beim Aktien-Bot — dem mit der viel breiteren Basis — ist **keine** der drei
   Bedingungen von null zu unterscheiden. Die gemeinsame Reihenfolge stützt sich
   auf Vorzeichen, nicht auf Intervalle.
2. Das Cluster-Intervall des Krypto-Welle-4-Befundes berührt die Null:
   **[−0,05; +9,80]**. Sobald ganze Coins statt einzelner Trades gezogen werden,
   ist er nicht mehr klar von null getrennt.
3. Es sind **22 Vergleiche**. Rein zufällig wäre gut einer davon auffällig.

Die einzelnen Kombinationen (`results/*_auswertung.json`, `kombinationen`) zeigen
dasselbe Bild bei durchweg kleinen Gruppen — die grösste Nicht-Stufe-0-Gruppe des
Krypto-Bots umfasst 33 Trades.

---

## 6. Die Einordnung (Punkt 4 des Auftrags)

### Was folgt für die Schwelle `min_fib_score = 0.3`?

Sie filtert **beim Aktien-Bot nichts**: Stufe ≥ 1 gegen Stufe 0 ergibt
+1,19 pp mit CI [−1,45; +3,93]. Von 813 Mustern wirft sie 303 weg und trifft
damit keine messbar bessere Auswahl als der Zufall.

Beim **Krypto-Bot** ist die Schwelle die einzige Stelle mit einem Signal
(+4,12 pp, p = 0,028, Weglassprobe stabil) — aber Abschnitt 5 zeigt, dass dieses
Signal aus der Welle-4-Bedingung kommt, nicht aus dem Zählen. Die Schwelle
funktioniert dort, wo sie funktioniert, **aus dem falschen Grund**.

**Eine Anhebung auf ≥ 2 ist von den Daten nicht gestützt.** Der Schritt von
Stufe 1 auf Stufe 2 ist der bestbelegte Nicht-Effekt der ganzen Untersuchung:
+0,12 pp (Krypto) und +0,21 pp (Aktien), beide Intervalle weit um die Null.
Er würde beim Krypto-Bot 83 von 130 und beim Aktien-Bot 363 von 510 Trades
streichen, ohne dass etwas dafür spricht.

### Was folgt für die Auswahl innerhalb eines Symbols?

Die Rangfolge nach `fib_score` ist **nicht begründet** — die Stufen unterscheiden
sich nicht. Praktisch folgt daraus heute **nichts**: TB-20 hat gemessen, dass die
Reihenfolge innerhalb eines Symbols in 0 von 20 114 nachgebildeten Läufen
überhaupt eine Auswahl traf. Die Rangfolge aus TB-20 (`fib_score`, dann jüngeres
Muster) bleibt damit eine **Absicherung gegen die Sortierimplementierung**, keine
fachliche Auswahlregel — und das ist genau, als was TB-20 sie eingeführt hat.

Relevant würde die Frage erst, wenn `fib_score` je **zwischen Symbolen** ranken
soll (Zuteilung, Positionslimit). Dafür gibt diese Untersuchung **keine
Grundlage**.

### Gibt es einen stetigen Primärschlüssel?

Ja (`naehe_weich`, 0 % Gleichstände gegen 74–86 % beim `fib_score`) — aber ohne
gemessene Trennschärfe. Siehe Abschnitt 2.

---

## 7. Belastbarkeit

### Der Survivorship-Vorbehalt

Das Aktienuniversum ist „Top 150 nach **heutiger** Marktkapitalisierung"
(`config/sp500_top150.txt`) und damit verzerrt: Unternehmen, die in den zehn
Jahren aus dem Index gefallen sind, fehlen. Für einen **Vergleich zwischen
Stufen** dürfte das wenig ausmachen — die Verzerrung trifft alle Stufen
gleichmässig, weil die Stufe eines Musters nichts mit der späteren Indexzugehörigkeit
seines Symbols zu tun hat. Die **absoluten** Renditen je Stufe (3,6 % bis 8,5 %)
sind dagegen zu optimistisch und dürfen nicht als Ertragserwartung gelesen
werden. Beim Krypto-Bot gilt dasselbe für die Top-25-Volumenliste.

### Der Look-Ahead-Vorbehalt

Bestätigt: die Auswertung läuft auf dem seit PR #26 korrigierten Pfad. Der
Nachweis ist mechanisch (Abschnitt 1) und nicht bloss behauptet.

### Mehrfachvergleiche und Aussagekraft

22 Vergleiche je Bot. Der Bericht nennt deshalb nirgends einen Einzelvergleich
„signifikant", sondern stellt jeden p-Wert neben sein Bootstrap-Intervall, sein
Cluster-Intervall und — wo es um eine Kernaussage geht — seine Weglassprobe.

Wie gross müsste die Stichprobe sein, um einen Unterschied zu finden?
(Normalapproximation, 80 % Macht, Grössenordnung — keine Planungszahl.)

| gesuchter Unterschied | `elliott_wave` (s = 13,7 pp) | `elliott_wave_stocks` (s = 20,0 pp) |
|---|---:|---:|
| 1 pp | ≈ 2 945 Trades je Gruppe | ≈ 6 248 |
| 2 pp | ≈ 737 | ≈ 1 562 |
| 5 pp | ≈ 118 | ≈ 250 |

Die tatsächlichen Gruppen umfassen 5 bis 363 Trades. **Ein Unterschied von
1–2 Prozentpunkten wäre hier gar nicht zu finden gewesen** — das „kein
Unterschied" heisst also: kein Unterschied in der Grössenordnung von rund
5 Prozentpunkten aufwärts. Für den Schritt Stufe 1 → Stufe 2 ist das trotzdem
aussagekräftig, weil der gemessene Punktwert dort bei +0,12 bzw. +0,21 pp liegt
und nicht bei „vielleicht 3, vielleicht 0".

### Was die Cluster-Intervalle sagen

Beim Krypto-Bot ist das Intervall über **Symbole** teilweise **enger** als das
über Trades. Das ist kein Fehler: es heisst, dass die Streuung eher **innerhalb**
der Coins liegt als **zwischen** ihnen — die Coins verhalten sich ähnlicher als
die Trades eines einzelnen Coins. `test_stufen.py` prüft die Eigenschaft, auf die
es ankommt, deshalb an einem künstlichen Fall (gleichlaufende Trades je Symbol →
Cluster-Intervall wird deutlich breiter), nicht an den echten Daten.

### Scope-Grenzen

Nicht gemessen und nicht behauptet:

* **Nur die Live-Parametrisierung.** Eine Zigzag-Schwelle von 4 % erzeugt beim
  Krypto-Bot ein Vielfaches an Mustern; ob die Stufen dort etwas tragen, steht
  hier nicht.
* **Kein In-/Out-of-Sample-Split, kein Walk-Forward.** Die Stichproben sind dafür
  zu klein — ein Split würde Stufe 3 auf ein bis zwei Trades je Fenster bringen.
* **Keine Kapitalsimulation.** Gemessen ist die Ereignisrendite je Trade, nicht
  ihr Beitrag zur Kapitalkurve. Positionslimit und Gleichzeitigkeit (die beim
  Aktien-Bot über `MAX_CONCURRENT_POSITIONS = 8` wirken) bleiben aussen vor.
* **Keine Richtungsumkehr.** Wie im Bot werden nur bearishe Muster (Long-only)
  ausgewertet.
* **Keine Muster ohne Frischefilter.** Ein Lauf ohne das Frische-Fenster ergäbe
  266 statt 225 Muster beim Krypto-Bot (+18 %) und 844 statt 813 beim Aktien-Bot
  (+4 %) — gemessen beim Aufbau der Untersuchung. Die zusätzlichen Muster wären
  aber Signale, die der Bot live verworfen hätte; der Lauf entspräche nicht mehr
  dem Bot, und die Gruppe Stufe 3 wüchse dabei von 5 auf 6 Trades.
* **Der Zigzag selbst ist nicht Gegenstand.** Die Frage „trägt der
  Zigzag-Detektor etwas?" ist eine andere als „trägt der Score etwas?".

### Vorbestehende Umgebungsfehlschläge

In der Cloud-Umgebung fehlen `binance`, `scipy`, `fastapi`, `yfinance` und die
Zeitzone `US/Eastern`. Diese Untersuchung umgeht das ohne Eingriff in Bot-Code:
`botenv.py` legt Stubs an, die bei jedem Aufruf eine `AssertionError` werfen
(gelesen werden ausschliesslich die lokalen CSVs), und `statistik.py` kommt ohne
`scipy` aus. Ein Basislauf auf unverändertem `main` ist damit nicht nötig — es
wird kein Skript ausgeführt, das diese Pakete bräuchte.

### Pflicht-Gegenchecks

| Prüfung | `elliott_wave` | `elliott_wave_stocks` |
|---|---|---|
| Selbsttests `test_stufen.py` | **29/29** | **29/29** |
| Nachbildung == `fibonacci_score()`, gemessene Muster | 225/225 | 813/813 |
| Nachbildung == `fibonacci_score()`, Zufallspunkte | 20 000, 0 Abweichungen | 20 000, 0 Abweichungen |
| Trade-Satz identisch zu `min_fib_score = 0.3` | ja (130) | ja (510) |
| Trade-Zahl deckt sich mit `elliott_wave_params/BERICHT.md` | ja (130) | ja (510) |
| Look-Ahead-Sperre greift | ja | ja |
| Kursdaten über `shared/kursdaten.py` (PR #81) | ja | ja (1 Kerze APH gestrichen) |
| `shared/ergebniskurven.py` | **9× AKTUELL** (vor und nach dem Lauf) | |
| `git diff origin/main...HEAD --name-only` | nur `research/` und `docs/` | |

---

## 8. Reproduktion

```bash
cd research/fib_score_stufen
python3 run_all.py                       # alles, rund 10 Minuten

# oder einzeln, je Bot ein eigener Prozess (Pflicht - siehe botenv.py):
python3 lauf.py        elliott_wave      # ~10 s   -> results/elliott_wave_muster.csv
python3 auswertung.py  elliott_wave      # ~45 s   -> results/elliott_wave_auswertung.json
python3 test_stufen.py elliott_wave      # ~60 s   -> 29 Prüfungen
python3 lauf.py        elliott_wave_stocks   # ~30 s
python3 auswertung.py  elliott_wave_stocks   # ~130 s
python3 test_stufen.py elliott_wave_stocks   # ~280 s
python3 uebersicht.py                    # beide Bots nebeneinander

python3 ../../shared/ergebniskurven.py   # muss 9x AKTUELL melden
```

Voraussetzungen: `pandas`, `numpy`. Alle Zufallszahlen laufen über
`numpy.random.default_rng` mit festem Seed (`statistik.SEED = 20260913`, das Datum
des Datenstands); zwei Läufe liefern dieselben Zahlen, und `test_stufen.py` prüft
genau das.

### Die Dateien

| Datei | Inhalt |
|---|---|
| `botenv.py` | Bot-Umgebung, Stubs, unabschaltbarer Hinweis |
| `bedingungen.py` | Zerlegung des Scores, stetige Abstände, vier Nähe-Masse |
| `statistik.py` | Bootstrap (Trades und Cluster), Permutationstests, Spearman — ohne `scipy` |
| `lauf.py` | Messlauf je Bot: Bot-Funktionen → eine Zeile je Muster |
| `auswertung.py` | die vier Fragen des Auftrags → `results/<bot>_auswertung.json` |
| `uebersicht.py` | beide Bots nebeneinander, Ausgangsbestimmung |
| `test_stufen.py` | 29 Selbsttests je Bot |
| `run_all.py` | Gesamtlauf, ein Prozess je Bot |
| `results/<bot>_muster.csv` | eine Zeile je Muster: Trade, Stufe, Bedingungen, Verhältnisse, Abstände |
| `results/<bot>_lauf.json` | Datengrundlage, Parameter, Identitätsnachweis |
| `results/<bot>_auswertung.json` | alle Zahlen dieses Berichts |
| `results/uebersicht.json` | Kurzfassung beider Bots |

---

## 9. Was hier NICHT getan wurde

**Keine Empfehlung wurde umgesetzt.** Kein Parameter, keine Schwelle, keine
Auswahlregel wurde geändert. Nichts unter `broker/`, keine Crontab, keine
launchd-Vorlage angefasst.

Naheliegende Folgeaufgaben — **benannt, nicht ausgeführt**:

1. **Die Welle-4-Bedingung getrennt untersuchen.** Sie ist die einzige der drei,
   die über beide Bots hinweg in dieselbe Richtung zeigt. Ob daraus ein Filter
   wird (`0.236 ≤ wave4/wave3 ≤ 0.382` als Ja/Nein-Bedingung statt als ein
   Drittel eines Scores), ist eine Strategieentscheidung des Nutzers und
   bräuchte den vollen Validierungsweg des Projekts: Backtest → Walk-Forward →
   Equity-Simulation → Buy-and-Hold-Vergleich.
2. **Die Welle-3-Bedingung ist ein Kandidat zum Streichen** — sie ist bei beiden
   Bots leicht negativ. Auch das ist eine Strategieentscheidung, keine
   Aufräumarbeit.
3. **Die eigentliche Frage unter der Frage** — „trägt der Zigzag-Detektor
   etwas?" — bleibt offen. Diese Untersuchung zeigt, dass der Score der Auswahl
   fast nichts hinzufügt; sie sagt nichts darüber, ob das, was übrig bleibt,
   besser ist als Zufalls-Timing. Für `elliott_wave_stocks` liegt genau dieser
   Massstab bereits als Auftrag beim Quartals-Review vor (`live_params.py`,
   Eintrag 2026-09-13: der Bot bei gleicher Zeit im Markt gegen das 95. Perzentil
   von Zufalls-Timing).
4. **`docs/UEBERSICHT_RESEARCH.md` kennt diese Untersuchung nicht.** Das Dokument
   ist ausdrücklich ein Stand vom 2026-09-12 und wurde hier bewusst nicht
   fortgeschrieben; wer es aktualisiert, sollte das für alle seither
   hinzugekommenen Ordner tun, nicht nur für diesen.

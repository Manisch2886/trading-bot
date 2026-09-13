# Übergabe: Fib-Score-Stufen (TB-25)

**Stand: 2026-09-13** · Branch `claude/new-session-u69uwy`, Base `main` (`48278b9`).
**Untersuchung, keine Änderung.** Es wurde kein Produktivcode angefasst, keine
`live_params.py` berührt, kein Parameter übernommen, keine Ergebnisdatei
überschrieben. `git diff origin/main HEAD --name-only` listet ausschliesslich
`research/fib_score_stufen/` und `docs/`.

Kurzfassung zum Kopieren: `docs/ERGEBNIS_TB25_fib_score_stufen.md`.
Ausführlich: `research/fib_score_stufen/BERICHT.md`.

---

## 1. Die Antwort zuerst

### Welcher der drei Ausgänge ist eingetreten, und mit welchen Zahlen?

**Ausgang 2 — „Kein Unterschied zwischen den Stufen", für beide Bots.**

Die Punktwerte steigen monoton mit der Stufe. Aber kein einziger Schritt von
einer Stufe zur nächsten ist von null zu unterscheiden, und der Schritt mit den
grössten Gruppen — Stufe 1 auf Stufe 2 — ist **praktisch exakt null**:

| Schritt | `elliott_wave` | `elliott_wave_stocks` |
|---|---|---|
| Stufe 1 gegen Stufe 0 | +3,83 pp, CI [−0,04; +7,91], p = 0,059 | +0,99 pp, CI [−1,90; +4,06], p = 0,54 |
| **Stufe 2 gegen Stufe 1** | **+0,12 pp**, CI [−5,17; +5,40], p = 0,97 | **+0,21 pp**, CI [−3,86; +4,56], p = 0,92 |
| Stufe 3 gegen Stufe 2 | +6,40 pp, CI [−7,79; +20,77], p = 0,36 | +3,72 pp, CI [−3,99; +12,29], p = 0,44 |

Die Gruppen selbst (Nettorendite über die tatsächliche Bot-Haltedauer, mit Stop,
Kursziel und Zeitausstieg des Bots, nach Gebühren):

| Stufe | Krypto n / Mittel / CI | Aktien n / Mittel / CI |
|---|---|---|
| 0 | 95 / 0,07 % / [−2,13; +2,55] | 303 / 3,61 % / [+1,77; +5,52] |
| 1 | 83 / 3,90 % / [+0,86; +7,33] | 363 / 4,59 % / [+2,48; +7,05] |
| 2 | 42 / 4,02 % / [+0,05; +8,29] | 127 / 4,81 % / [+1,64; +8,52] |
| 3 | **5** / 10,42 % / [−3,69; +24,54] | **20** / 8,53 % / [+1,78; +16,48] |

**Der Median ist in sieben von acht Gruppen exakt der Stop** (−6,30 % bzw.
−3,30 %). Über die Hälfte aller Trades endet in jeder Stufe am Stop; was sich
zwischen den Stufen bewegt, ist der Rand der Verteilung, nicht der typische
Trade. **Stufe 3 trägt keine Aussage** — 5 bzw. 20 Trades.

### Der eine Vorbehalt

Beim **Krypto-Bot** ist die Schwelle selbst (Stufe 0 gegen alles darüber) der
einzige Vergleich unter 5 %: **+4,12 pp, CI [+0,70; +7,48], p = 0,028**,
Cluster-Intervall über Symbole [+1,26; +7,29], Trefferquote 43,8 % gegen 28,4 %,
Weglassprobe über alle 18 Coins stabil (+3,20 bis +4,76 pp).

Drei Gründe, das nicht als Stufenbefund zu lesen:

1. Es ist **ein auffälliger Vergleich unter 22** — rein zufällig wäre gut einer
   zu erwarten.
2. Beim Aktien-Bot, der zehnmal so viele Symbole und doppelt so viele Muster
   hat, ist dieselbe Zahl **+1,19 pp, CI [−1,45; +3,93], p = 0,41**.
3. Er stammt fast vollständig aus **einer einzigen der drei Bedingungen** —
   siehe Abschnitt 2.

### Die Nebenfrage aus Punkt 1 des Auftrags

**Ja, alle drei Bedingungen sind Schwellen auf einer stetigen Grösse** — dem
Verhältnis zweier Wellenlängen. Zwei Korrekturen zur Vermutung im Auftrag:

* Es sind **Intervalle, keine Toleranzen um ein Ziel**. Der Code prüft
  `0.5 ≤ w2/w1 ≤ 0.618`, `1.4 ≤ w3/w1 ≤ 1.8`, `0.236 ≤ w4/w3 ≤ 0.382`.
* Die **kanonischen Fibonacci-Werte liegen bei zwei von drei Bedingungen auf dem
  oberen Rand** des Intervalls (0,618 und 0,382), bei der dritten (1,618)
  unsymmetrisch im Inneren. Einen im Code benannten Zielwert gibt es nicht.

Deshalb wird der Abstand auf das Intervall normiert
(`d = |r − Mitte| / halbe Breite`, `d ≤ 1` ⟺ erfüllt). **Gemessen trägt die
stetige Grösse nicht mehr als die Stufe:**

| Grösse | `elliott_wave` | `elliott_wave_stocks` |
|---|---|---|
| Stufe (0–3) | ρ = +0,164, p = 0,014 | ρ = +0,039, p = 0,27 |
| stetige Nähe | ρ = +0,109, p = 0,10 | ρ = +0,038, p = 0,28 |
| stetige Nähe, weiche Fassung | ρ = +0,130, p = 0,052 | ρ = +0,054, p = 0,12 |

**Als Primärschlüssel taugt sie**, als Auswahlkriterium nicht: der `fib_score`
setzt 85,8 % (Krypto) bzw. 73,6 % (Aktien) der Muster je Symbol in eine
Gleichstandsgruppe, die weiche stetige Nähe **0,0 %**. Eindeutigkeit ohne
Trennschärfe ersetzt aber nur einen willkürlichen Tie-Break durch einen sauberer
aussehenden.

---

## 2. Der eigentliche Befund: die drei Bedingungen sind nicht gleichwertig

Die Stufe zählt, **wie viele** Bedingungen gelten. Gemessen kommt es darauf
nicht an, sondern darauf, **welche**:

| Bedingung | `elliott_wave` | `elliott_wave_stocks` |
|---|---|---|
| Welle 2 / Welle 1 | +3,53 pp, CI [−0,90; +8,03], p = 0,10 | +1,68 pp, CI [−1,61; +5,38], p = 0,33 |
| Welle 3 / Welle 1 | **−0,24 pp**, CI [−4,18; +3,78], p = 0,91 | **−0,79 pp**, CI [−3,55; +2,18], p = 0,63 |
| Welle 4 / Welle 3 | **+4,88 pp**, CI [+0,85; +9,13], p = **0,012** | +1,82 pp, CI [−1,10; +4,92], p = 0,22 |

**Dieselbe Reihenfolge bei beiden Bots: Welle 4 > Welle 2 > Welle 3**, und die
Welle-3-Bedingung liegt bei beiden unter null. Das ist die einzige Struktur, die
sich über beide Bots reproduzieren liess — und sie widerspricht der
Stufen-Lesart.

Ehrlich dazu: beim Aktien-Bot ist **keine** der drei Bedingungen von null zu
unterscheiden, und das Cluster-Intervall des Krypto-Welle-4-Befundes berührt die
Null ([−0,05; +9,80]). Die gemeinsame Reihenfolge stützt sich auf Vorzeichen,
nicht auf Intervalle.

---

## 3. Das Rundungsartefakt (Punkt 3 des Auftrags)

**Die Erwartung bestätigt sich.** Innerhalb Stufe 1 unterscheidet sich die
Rendite zwischen 0,33 und 0,34 nicht: +0,59 pp (p = 0,87) beim Krypto-Bot,
+2,77 pp (p = 0,34) beim Aktien-Bot. Dasselbe in Stufe 2 (0,67 gegen 0,66):
+1,98 pp bzw. −2,41 pp, einmal in jede Richtung.

**Welche Bedingung trägt die 0,34?** Die **Welle-2-Bedingung**, und nur sie — 
exhaustiv über alle acht Kombinationen geprüft; für 0,67 gilt dasselbe. Der
Tie-Break ist damit nicht zufällig, sondern **deterministisch**.

Und hier liegt die unangenehme Stelle: die 0,33-Gruppe ist keine homogene
Vergleichsgruppe, sondern eine Mischung aus der **schlechtesten und der besten**
Einzelbedingung.

| Stufe-1-Untergruppe | Score | Krypto | Aktien |
|---|---:|---|---|
| nur Welle 2 | **0,34** | n = 27, 4,30 % | n = 75, 6,79 % |
| nur Welle 3 | 0,33 | n = 23, **−0,06 %** | n = 94, **1,94 %** |
| nur Welle 4 | 0,33 | n = 33, **6,34 %** | n = 194, **5,03 %** |

Der Rundungsvorzug hebt die Welle-2-Gruppe systematisch über eine Gruppe, in der
die bestlaufende Einzelbedingung steckt. Er wirkt — nur nicht in die Richtung, in
die er wirken müsste, wenn er begründet wäre.

**Reichweite:** TB-20 hat gemessen, dass die Rangfolge innerhalb eines Symbols
heute keinen einzigen Live-Trade verschiebt (0 von 20 114 nachgebildeten Läufen).
Der Tie-Break ist also ein Konstruktionsfehler ohne gemessene Wirkung — er würde
erst wirken, wenn je eine Zuteilungsregel über Symbole hinweg auf `fib_score`
rankt.

---

## 4. Wie gemessen wurde

### Die echten Bot-Funktionen, nicht eine Nachbildung

| Aufgabe | Bot-Funktion |
|---|---|
| Kursdaten inkl. Lückenbereinigung (PR #81) | `multi_symbol_optimise.load_all_symbol_data` |
| Zigzag mit Bestätigungszeitpunkt | `zigzag_indicator.calculate_zigzag_with_confirmation` |
| kausale Wellenauswahl | `elliott_wave_counter.find_causal_waves` |
| Bewertung | `elliott_wave_counter.fibonacci_score` (Spalte `fib_score`) |
| Trade-Simulation | `backtest_elliott.run_backtest` |
| Parameter | `live_params.py` |

Nachgebildet wird genau **eine** Sache: die **Zerlegung** des Scores — welche der
drei Bedingungen erfüllt ist. Der Bot gibt sie nicht aus; aus einer 0,33 ist
nicht ablesbar, ob Welle 3 oder Welle 4 dahintersteht, und genau das fragt
Punkt 3. Sie wird gegen die echte `fibonacci_score()` geprüft: auf **jedem**
gemessenen Muster (225 bzw. 813) und auf **20 000 Zufallspunkten** je Bot, davon
400 entartete Fälle — **0 Abweichungen**.

### Wie Stufe 0 in die Messung kommt

Der Bot läuft mit `min_fib_score = 0.3`; Stufe 0 kommt dort nie vor. Der Lauf
setzt die Schwelle deshalb auf **0.0**. Das ist kein harmloser Wechsel:
`remove_overlapping` bildet Überlappungsgruppen greedy, zusätzliche
Stufe-0-Kandidaten könnten die Gruppenbildung verschieben. Deshalb rechnet der
Lauf **beide** Varianten und vergleicht sie:

| | Krypto | Aktien |
|---|---:|---:|
| Lauf A (`min_fib_score = 0.3`, exakt der Bot) | 130 Trades | 510 Trades |
| Lauf B, Stufen 1–3 (`min_fib_score = 0.0`) | 130 Trades | 510 Trades |
| Zeile für Zeile identisch, 9 Spalten | **ja** | **ja** |

Die 130 und die 510 sind dieselben Zahlen, die
`research/elliott_wave_params/BERICHT.md` für diese Live-Kombinationen nennt —
ein unabhängiger Beleg, dass hier derselbe Trade-Satz gerechnet wird.

### Datengrundlage

| | `elliott_wave` | `elliott_wave_stocks` |
|---|---:|---:|
| Symbole | 18 | 147 |
| Kerzen | 706 362 (1 h) | 361 942 (1 Tag) |
| Zeitraum | 2021-09-01 bis 2026-08-31 | 2016-08-31 bis 2026-09-01 |
| Parameter | Zigzag 10 % / Stop 6 % / Ziel 0,618 | Zigzag 5 % / Stop 3 % / kein Ziel |
| Muster mit Trade | 225 | 813 |
| Muster je Stufe (0/1/2/3) | 95 / 83 / 42 / 5 | 303 / 363 / 127 / 20 |

### Look-Ahead — mechanisch bestätigt, nicht behauptet

`run_backtest` **wirft eine `ValueError`**, wenn die Wellen keine Spalte
`entry_idx` mitbringen; diese Spalte liefert nur `find_causal_waves`. Ein Lauf
mit Look-Ahead ist auf diesem Pfad gar nicht möglich. `test_stufen.py` provoziert
den Fehlschlag und prüft ihn. Eingestiegen wird zum Schlusskurs des
Bestätigungsbalkens (PR #26).

### Statistik

Verteilungsfrei, ohne `scipy` (in der Cloud-Umgebung nicht installiert, und das
Projekt führt es auch nicht in `requirements.txt`): Perzentil-Bootstrap für
Mittelwerte und Differenzen, zusätzlich ein **Cluster-Bootstrap über Symbole**
(Trades desselben Symbols sind nicht unabhängig), zweiseitige Permutationstests,
Spearman mit Durchschnittsrängen (bindungsfest — die Stufe hat nur vier Werte),
und für die Kernaussagen eine **Weglassprobe** über alle Symbole. Alle
Zufallszahlen über `numpy.random.default_rng` mit festem Seed; `test_stufen.py`
prüft, dass zwei Läufe dieselben Zahlen liefern.

---

## 5. Belastbarkeit und Vorbehalte

**Survivorship.** Das Aktienuniversum ist „Top 150 nach **heutiger**
Marktkapitalisierung" und damit verzerrt. Für den **Vergleich zwischen Stufen**
dürfte das wenig ausmachen — die Verzerrung trifft alle Stufen gleich, weil die
Stufe eines Musters nichts mit der späteren Indexzugehörigkeit seines Symbols zu
tun hat. Die **absoluten** Renditen je Stufe sind dagegen zu optimistisch und
dürfen nicht als Ertragserwartung gelesen werden. Beim Krypto-Bot gilt dasselbe
für die Top-25-Volumenliste.

**Mehrfachvergleiche.** 22 je Bot. Der Bericht nennt deshalb nirgends einen
Einzelvergleich „signifikant", sondern stellt jeden p-Wert neben sein
Bootstrap-Intervall, sein Cluster-Intervall und, wo es um eine Kernaussage geht,
seine Weglassprobe.

**Trennschärfe — was „kein Unterschied" hier heisst.** Nötige Stichprobe je
Gruppe (Normalapproximation, 80 % Macht, Grössenordnung):

| gesuchter Unterschied | Krypto (s = 13,7 pp) | Aktien (s = 20,0 pp) |
|---|---:|---:|
| 1 pp | ≈ 2 945 Trades | ≈ 6 248 |
| 2 pp | ≈ 737 | ≈ 1 562 |
| 5 pp | ≈ 118 | ≈ 250 |

Die tatsächlichen Gruppen umfassen 5 bis 363 Trades. **Ein Unterschied von
1–2 Prozentpunkten wäre hier nicht zu finden gewesen.** „Kein Unterschied" heisst
also: keiner in der Grössenordnung von rund 5 Prozentpunkten aufwärts. Für den
Schritt Stufe 1 → 2 ist das trotzdem aussagekräftig, weil der Punktwert dort bei
+0,12 bzw. +0,21 pp liegt.

**Keine Phasenverschiebung.** Der mediane Einstiegszeitpunkt liegt für alle vier
Stufen eng beieinander (Krypto 2024-03 bis 2024-08, Aktien 2022-03 bis 2022-09);
ein Stufenunterschied liesse sich also nicht damit erklären, dass eine Stufe in
besseren Marktphasen häufiger vorkommt.

**Scope-Grenzen.** Nicht gemessen: andere Zigzag-Schwellen als die
Live-Parametrisierung; In-/Out-of-Sample-Split oder Walk-Forward (die Gruppen
sind dafür zu klein — Stufe 3 hätte ein bis zwei Trades je Fenster);
Kapitalsimulation und Positionslimit; bullishe Muster (der Bot ist Long-only);
Läufe ohne Frischefilter (hätten ~5 % mehr Muster ergeben und entsprächen nicht
dem Bot); und die andere Frage — ob der Zigzag-Detektor selbst etwas trägt.

**Umgebung.** Die fehlenden Pakete (`binance`, `scipy`, `fastapi`, `yfinance`,
Zeitzone `US/Eastern`) werden nicht berührt: `botenv.py` legt Stubs an, die bei
jedem Aufruf eine `AssertionError` werfen — gelesen werden ausschliesslich die
lokalen CSVs —, und `statistik.py` kommt ohne `scipy` aus. Es wird kein Skript
ausgeführt, das eines dieser Pakete bräuchte; ein Basislauf auf unverändertem
`main` erübrigt sich damit.

---

## 6. Tests und Randbedingungen

| Prüfung | Ergebnis |
|---|---|
| `python3 research/fib_score_stufen/test_stufen.py elliott_wave` | **29 von 29** |
| `python3 research/fib_score_stufen/test_stufen.py elliott_wave_stocks` | **29 von 29** |
| `python3 shared/ergebniskurven.py` vor dem Lauf | **9× AKTUELL** |
| `python3 shared/ergebniskurven.py` nach dem Lauf | **9× AKTUELL** |
| `git diff origin/main HEAD --name-only` | nur `research/fib_score_stufen/` und `docs/` |
| Bot-Dateien (7 je Bot, namentlich geprüft) | unverändert |

Die Selbsttests prüfen unter anderem die Nachbildung gegen die echte
`fibonacci_score()`, die Abgeschlossenheit des Wertebereichs, dass 0,34 und 0,67
die Welle-2-Bedingung zwingend voraussetzen, die Look-Ahead-Sperre, die
Zeile-für-Zeile-Gleichheit von Lauf A und B, die Reproduzierbarkeit der Statistik
und — über `git status` und `git diff` — dass kein Produktivcode angefasst wurde.

**Nicht angefasst:** `live_params.py`, `forward_test.py`, `equity_simulation.py`,
`multi_symbol_optimise.py`, `elliott_wave_counter.py`, `zigzag_indicator.py`,
`backtest_elliott.py`, `results/*`, alles unter `broker/`, Crontab,
launchd-Vorlagen, alle übrigen `research/`-Ordner.

**Neue Abhängigkeit:** keine. `pandas` und `numpy` reichen.

---

## 7. Was daraus folgt — Entscheidungen für den Nutzer

Diese Untersuchung setzt **keine Empfehlung um**. Die folgenden Punkte sind
benannt, nicht ausgeführt:

1. **Die Schwelle `min_fib_score = 0.3`.** Beim Aktien-Bot filtert sie nichts
   (+1,19 pp, CI [−1,45; +3,93]) und wirft dabei 303 von 813 Mustern weg. Beim
   Krypto-Bot wirkt sie, aber aus dem falschen Grund. **Eine Anhebung auf ≥ 2 ist
   von den Daten nicht gestützt** — sie würde beim Krypto-Bot 83 von 130 und beim
   Aktien-Bot 363 von 510 Trades streichen, ohne dass etwas dafür spricht.
2. **Die Welle-4-Bedingung getrennt untersuchen.** Sie ist die einzige, die über
   beide Bots in dieselbe Richtung zeigt. Sie als Ja/Nein-Filter zu verwenden
   statt als ein Drittel eines Scores wäre eine Strategieänderung und bräuchte
   den vollen Validierungsweg: Backtest → Walk-Forward → Equity-Simulation →
   Buy-and-Hold-Vergleich.
3. **Die Welle-3-Bedingung ist ein Kandidat zum Streichen** — bei beiden Bots
   leicht negativ. Auch das ist eine Strategieentscheidung, keine Aufräumarbeit.
4. **Die Rangfolge nach `fib_score` ist nicht fachlich begründet.** Praktisch
   folgt daraus heute nichts (TB-20: 0 von 20 114 Läufen). Relevant würde sie
   erst, wenn `fib_score` je **zwischen Symbolen** ranken soll — dafür gibt diese
   Untersuchung keine Grundlage.
5. **Die Frage unter der Frage bleibt offen:** trägt der Zigzag-Detektor etwas?
   Für `elliott_wave_stocks` liegt genau dieser Massstab bereits als Auftrag beim
   Quartals-Review vor (`live_params.py`, Eintrag 2026-09-13: der Bot bei gleicher
   Zeit im Markt gegen das 95. Perzentil von Zufalls-Timing).
6. **`docs/UEBERSICHT_RESEARCH.md` kennt diese Untersuchung nicht.** Das Dokument
   ist ausdrücklich ein Stand vom 2026-09-12 und wurde hier bewusst nicht
   fortgeschrieben; wer es aktualisiert, sollte das für alle seither
   hinzugekommenen Ordner tun.

Ein autonom ausführbares Testdokument wurde nicht angelegt: es entsteht kein
Produktivcode, der bleiben soll. Die Selbsttests liegen bei der Untersuchung
(`research/fib_score_stufen/test_stufen.py`) und laufen mit `run_all.py` mit.

# TB-65 Welche Schranke gilt für den Benchmark? — an: Claude Code am Mac (lokale Sitzung)

**Sitzungstitel für Claude Code: `TB-65 Benchmarkschranke pruefen`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main`.

⛔⛔ **DIESE AUFGABE ÄNDERT KEINE ZEILE CODE UND KEINEN REGISTERTEXT.**
Sie liest, misst und berichtet. **Rechnen darf sie — aber nur nachrichtlich,
in eine Datei unter `docs/belege/TB-65/`.**

---

## 0. Warum es diese Aufgabe gibt

**TB-61 hat gemessen** (`docs/ERGEBNIS_TB-61_benchmark_neun.md`, Befund 1): Bei
den fünf Krypto-Bots sind **die Hälfte der Selektionsfalten leer** — 0 Symbole,
0 Handelstage. Ursache ist `point_in_time(…, rd.MINDESTTRAINING_JAHRE)` in
`research/vorregistrierung/benchmark.py:183`, Wert **4** aus
`registerdaten.py:108`.

**TB-61 hat das als offene Verfahrensfrage gemeldet** — so verlangte es sein
Auftrag (Abschnitt 6: *„Entscheide das nicht"*).

⚠️⚠️ **Die Chat-Sitzung hat danach zwei Registerstellen gelesen und kommt zu
einem anderen Schluss: es sei keine offene Frage, sondern ein Verstoß.** ⭐
**Diese Aufgabe prüft genau das — und sie prüft es SO, dass sie auch zum
Gegenteil kommen kann.**

> ⛔⛔ **Die wichtigste Auflage dieser Aufgabe:** Sie ist **nicht** dafür da, die
> Lesart der Chat-Sitzung zu bestätigen. **Ein Prüfauftrag, der die Antwort
> schon nennt, bekommt sie bestätigt** — und genau das ist die Fehlerklasse
> `K3f`: *ein Prüfkriterium, das nach dem Blick auf das Ergebnis gewählt wird,
> ist eine Selektion.*

---

## 1. Die drei Fragen, offen gestellt

### Frage A — Hebt Registerabschnitt 5.3 den point-in-time-Ausschluss auf, und für was?

**Abschnitt 5.3 trägt den Vermerk:**

> ⚠️ **ERSETZT durch Abschnitt 15 (Registernachtrag TB-36, 15.09.2026),
> Registertext 3 und 4.** … Die hier zitierte Regel („mindestens vier Jahre
> Kursdaten je Symbol", point-in-time-Ausschluss) gilt **nicht mehr** — es gibt
> kein Mindesttraining, und kein Symbol wird aus einer Falte ausgeschlossen.

**Zu prüfen — beide Lesarten ernsthaft, mit Fundstellen:**

| | Lesart | dafür spricht | dagegen spricht |
|---|---|---|---|
| **A1** | Der Satz hebt den Ausschluss **überall** auf, also auch im Benchmark | *(zu belegen)* | *(zu belegen)* |
| **A2** | Er betrifft nur den **Faltenplan** (wann eine Falte beginnt), nicht die Frage, auf welchen Symbolen der **Benchmark** rechnet | *(zu belegen)* | *(zu belegen)* |

⭐ **Nimm A2 ernst.** Abschnitt 5.3 heisst *„Krypto: Platzhalter mit Regel"* und
steht im Kapitel über den **Faltenplan**. Dass ein Satz dort auch für
`benchmark.py` gilt, ist eine Schlussfolgerung — **keine Fundstelle.**

### Frage B — Schreibt Registertext 3b (c) die Loader-Schranke für den Benchmark vor?

**Abschnitt 16.7, Ergänzung (c), wörtlich:**

> **Der Benchmark einer Falte** — für die Drawdown-Nebenbedingung (Abschnitt 4)
> und für Rang 3 — **wird auf den in dieser Falte geladenen Symbolen des Bots
> gerechnet, nicht auf dem vollen Universum. Bot und Benchmark leben in
> derselben Menge.**

**Zu prüfen:**

1. Was heisst *„geladen"* — entscheidet der Loader (`MIN_HISTORY_*`, 3b (b)),
   oder lässt der Text offen, dass eine zusätzliche Schranke danebensteht?
2. ⚠️ **Der Gegensatz im Satz ist „geladene Symbole" gegen „volles Universum".**
   Ist `point_in_time(…, 4 Jahre)` überhaupt einer der beiden Fälle — oder ein
   **dritter**, den der Text nicht regelt?
3. Gibt es einen Registertext, der `MINDESTTRAINING_JAHRE` für den Benchmark
   **ausdrücklich** vorsieht? ⭐ **Such breit**, mit mehreren Mustern
   (`Mindesttraining`, `vier Jahre`, `point-in-time`, `Vorlauf`), und **nenne
   die Zahl der Treffer je Muster** — auch wenn sie null ist.

### Frage C — Was folgt, wenn A1 und B zutreffen?

**Nachrichtlich rechnen, nicht ändern:**

Die Tabelle aus TB-61, aber mit der Loader-Schranke je Bot statt vier Jahren —
`MIN_HISTORY_DAYS` **500** (`rsi2_crypto`, `turtle_soup_crypto`,
`volatility_breakout_crypto`), **730** (`t3_supertrend`), **17 520 Kerzen**
(`elliott_wave`), **1 825** (die vier Aktien-Bots).

⚠️⚠️ **In eine Kopie ausserhalb von `research/vorregistrierung/`**, wie TB-61 es
für seinen Testlauf gemacht hat (zwei Ebenen unter der Repo-Wurzel, sonst
scheitert `_umgebung()`). ⛔ **`benchmark.py` im Repo bleibt unverändert.**

**Auszugeben je Bot:** Zahl der leeren Selektionsfalten vorher und nachher, und
`DD_Toleranz` bei 25 / 50 / 100 % vorher gegen nachher.

⚠️ **Für `elliott_wave` ist die Schranke eine Kerzenzahl, keine Zeitspanne**
(3b (b), ausdrücklich). **Geht das nicht sauber, sag es und lass ihn aus** —
*ein ausgelassener Bot mit Begründung ist besser als eine Zahl, die eine andere
Grösse misst.*

---

## 2. Was diese Aufgabe NICHT tut

| | |
|---|---|
| ⛔ | **`benchmark.py`, `faltenplan.py`, `registerdaten.py` ändern** |
| ⛔ | **Einen Registertext ändern oder ergänzen** |
| ⛔ | **`benchmark_drawdowns.json` oder `benchmark_drawdowns_neu.json` anfassen** |
| ⛔ | **Entscheiden, welche Lesart gilt.** Das ist Betreiber- oder Fable-Sache |
| ⛔ | **Die zwei neuen roten Tests aus TB-61 (G6, H3) reparieren** — eigene Aufgabe |

---

## 3. Die Nachweise

| # | Nachweis |
|---:|---|
| **1** | `git status --short` vor dem ersten Schreiben |
| **2** | ⭐ **Frage A**, beide Lesarten mit Fundstellen (Datei, Zeile, Wortlaut) — und ein ausdrücklicher Satz, welche die Quellenlage besser trägt **oder** dass sie es nicht entscheidet |
| **3** | ⭐ **Frage B**, dieselbe Form; dazu die Trefferzahl je Suchmuster aus B.3, **auch die Nullen** |
| **4** | ⭐ **Frage C**, die Tabelle vorher/nachher, mit Angabe, welcher Bot ausgelassen wurde und warum |
| **5** | SHA-256 von `benchmark_drawdowns.json` — muss `a163c498…36d1ee` sein, und von `benchmark_drawdowns_neu.json` vor und nach der Aufgabe **gleich** |
| **6** | `git diff --numstat` — erwartet **nur** Dateien unter `docs/` |
| **7** | `git status --short` nach dem letzten Commit; die Wegwerf-Kopie ist entfernt |

---

## 4. Die harten Auflagen

| | |
|---|---|
| ⛔ | **Rein lesend am Code und am Register** |
| ⭐⭐ | **Die Gegenthese bekommt denselben Platz wie die These.** Findest du die Lesart der Chat-Sitzung falsch, **schreib das hin** — das ist der wertvollste Ausgang dieser Aufgabe, nicht der peinliche |
| ⚠️ | **Ein Name ist kein Messwert** (`K3e`). `MINDESTTRAINING_JAHRE` heisst so; das sagt nichts darüber, wofür der Registertext ihn vorsieht |
| ⭐ | **Jede Trefferzahl wird genannt, auch null** — *ein leeres Ergebnis und ein blinder Sucher sehen gleich aus* (`A1`) |
| ⭐ | **Sichern nach jedem fertigen Teil** |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block** |

---

## 5. Die Abgabe

`docs/ERGEBNIS_TB-65_benchmarkschranke.md`, Rohausgaben unter
`docs/belege/TB-65/`, und ein Journal-Nachtrag.

⭐ **Der Schlussabsatz nennt ausdrücklich, was diese Aufgabe NICHT entschieden
hat** — und welche Entscheidung ansteht.

---

## In einfacher Sprache

**Worum es geht:** Die Tabelle, die für jeden Bot festlegt, wie tief er fallen
darf, rechnet bei den fünf Krypto-Bots auf einem Universum, in dem die Hälfte
der Jahre leer ist — kein einziges Symbol. Das hat der letzte Lauf gemessen und
als offene Frage gemeldet.

**Was ich beim Nachlesen gefunden habe:** Zwei Stellen im Register, die meiner
Lesart nach sagen, dass dort die falsche Schranke benutzt wird. Wäre das
richtig, müssten die fünf Krypto-Zahlen neu gerechnet werden, bevor du das
Amendment freigibst — sie wären sonst rund dreimal zu streng.

**Warum trotzdem erst geprüft wird:** Ich lege zwei Registertexte gegeneinander
aus, und die Sitzung, die tatsächlich gerechnet hat, ist zu einem vorsichtigeren
Schluss gekommen. **Ein Prüfauftrag, der die Antwort schon nennt, bekommt sie
bestätigt** — deshalb steht in dieser Aufgabe die Gegenthese gleichberechtigt
daneben, und die prüfende Sitzung darf ausdrücklich zu dem Ergebnis kommen, dass
ich mich irre.

**Was du danach hast:** Eine belegte Antwort auf die Frage, welche Schranke
gilt — und eine Gegenüberstellung, was es zahlenmässig ausmacht. Entschieden
wird erst danach.

# TB-72 `t3_supertrend` beginnt 2019 — und der Faltenplan hört auf, die Regel parallel nachzurechnen

**an: Claude Code am Mac (lokale Sitzung)**

**Sitzungstitel für Claude Code: `TB-72 erste Falte aus Trockenlauf`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main`.

⚠️⚠️ **Diese Aufgabe RECHNET** und bewegt Zahlen, die in den Tag eingehen.
⛔ **Sie vollzieht nichts an der Sperrliste**, und sie überschreibt keine
bestehende Ergebnisdatei.

---

## 0. Warum es diese Aufgabe gibt

**Zwei Implementierungen derselben Frage laufen auseinander, und eine davon ist
die registrierte Regel.**

| | |
|---|---|
| **Registertext 4a** | erste Falte = erstes Kalenderjahr, in dem am 1. Januar Universum und Indikator-Vorlauf vorliegen. `faltenplan.py::_plan` rechnet das aus der Datenlage nach (`erste_falte_quelle`) |
| **Registertext 3b (a)** | eine Falte zählt, wenn der Loader mindestens ein Symbol an mindestens einem Handelstag handelbar macht — über den **Trockenlauf** |
| ⚠️ **Register 21.3 (b)** | **bei Abweichung bindet 3b (a)** — der Trockenlauf |
| ⛔ **Gemessen** | **Kein Code setzt 21.3 (b) um.** `faltenplan.py` sagt es im Modulkopf (Z. 39–42) selbst: *„das rechnet dieses Modul nicht, und für `t3_supertrend` weichen beide ab (4a: 2018, 3b (a): 2019, weil `MIN_HISTORY_DAYS = 730` in der Falte 2018 kein Symbol handelbar macht)"* |

**Die Folge, sichtbar in `benchmark_drawdowns_vt.json`:** `t3_supertrend` führt
eine Falte **2018 mit 0 Symbolen und 0 Handelstagen** als Selektionsfalte.

⭐ **Fable hat beides entschieden** (`FABLE_ANTWORT_2026-09-20d_mtm_messung.md`,
Abschnitt 2):

> **(1) Ja, Berichtigung.** 21.3 (b) ist registrierte Regel … Plan an
> registrierte Regel: `t3_supertrend` beginnt 2019, sieben Falten. Die bekannte
> Wirkung … in die Notiz … Dass die Richtung diesmal zugunsten des Bots geht,
> ändert an der Kategorie nichts — die Quelle des Grundes ist die Regel.
>
> **(2)** … **`faltenplan.py` sollte die erste Falte aus dem Trockenlauf
> beziehen, nicht aus 4a nachrechnen.** 4a bleibt die Regel; 3b (a) über den
> Trockenlauf ist ihre operative Form; der Plan ist eine Ableitung daraus, keine
> Parallelrechnung. **Dann ist die Frage (2) nicht einmal zu stellen — der Plan
> kann nicht abweichen.**

⭐ **Die Einordnung in seinen Worten:** Die `t3`-Berichtigung ist die
**Instanz**, die Ableitung aus dem Trockenlauf ist die **Schliessung der
Klasse**. *Dieselbe Berichtigung, zwei Notizen, ein Vorgang.*

---

## 1. ⚠️ Eine Vormessung aus dem Chat — und warum du ihr nicht trauen darfst

**Ich habe die neun Zahlen am 20.09., 19:00, aus `benchmark_drawdowns_vt.json`
gezogen. Ergebnis: nur `t3_supertrend` weicht ab.**

| Bot | erste Falte laut Plan | erste nicht-leere Falte |
|---|---|---|
| `elliott_wave` | 2018-2019 | 2018-2019 |
| `elliott_wave_stocks` | 2017 | 2017 |
| `rsi2_crypto` | 2019 | 2019 |
| `rsi2_mean_reversion` | 2018 | 2018 |
| **`t3_supertrend`** | **2018** | **2019** ⛔ |
| `turtle_soup_crypto` | 2018 | 2018 |
| `turtle_soup_stocks` | 2017 | 2017 |
| `volatility_breakout` | 2018 | 2018 |
| `volatility_breakout_crypto` | 2018 | 2018 |

⛔⛔ **Diese Messung hat einen blinden Fleck, und du musst ihn schliessen:**
`benchmark_drawdowns_vt.json` enthält **nur Falten, die im Plan stehen**. Ein
Bot, dessen Trockenlauf eine **frühere** Falte handelbar machte als der Plan
kennt, wäre darin **unsichtbar** — die Falte stünde gar nicht in der Datei.

⭐ **Deshalb misst du die neun Zahlen aus dem Trockenlauf selbst**
(`research/faltenplan_neun/faltenschranke_messung.py`:
`loader_lesart(bot)` / `trockenlauf_ohne_schranke()`; `benchmark.py` importiert
das Modul bereits, Z. 99–100). ⚠️ **Nenne beide Zahlen je Bot** — Plan und
Trockenlauf — **und sag ausdrücklich, ob meine Vormessung getroffen hat.**
*Trifft sie nicht, gilt deine.*

---

## 2. Die Schritte

### Schritt 0 — vor allem anderen

**Committe, was im Arbeitsbaum liegt.** Nachweis „sauber" wird **danach**
geprüft. ⚠️ Liegen Betreiber-Dateien darin, geh wie TB-68/TB-71 vor: eigener
Zwischencommit, im Text als „nicht von dieser Sitzung geschrieben" vermerkt.

### Schritt 1 — die neun Zahlen, aus dem Trockenlauf

**Je Bot: erste Falte laut Plan gegen erste Falte laut Trockenlauf.**
⭐ **Rein lesend**, bevor irgendetwas geändert wird. Rohausgabe nach
`docs/belege/TB-72/`.

⚠️ **Prüfe beide Richtungen** — später *und* früher als der Plan.

**Sichern: commit und push.**

### Schritt 2 — `faltenplan.py` leitet die erste Falte ab, statt sie nachzurechnen

**In `_plan`:** `erste` kommt aus dem Trockenlauf, nicht aus der 4a-Nachrechnung.
⭐ **`erste_falte_quelle` wird mitberichtigt** — heute steht dort *„Datenlage
nach Registertext 4a … keine Konstante"*; künftig muss dort stehen, dass 4a die
Regel ist und der Trockenlauf ihre operative Form (21.3 (b)).

⛔ **Keine Konstantenkopie.** Das Modul wird importiert, nicht nachgebaut —
`benchmark.py` zeigt, wie (Z. 99–100).

⚠️ **Ändere nichts anderes an `faltenplan.py`** — nicht Faltenlänge, nicht
Purge, nicht Embargo, nicht den Go-Live-Schnitt.

**Sichern: commit und push.**

### Schritt 3 — der neue Plan, daneben

⛔ **`ergebnisse/faltenplan.json` wird NICHT überschrieben** (Sperrliste
Punkt 2; der Tag ist nicht signiert, aber die Regel *„nie überschreiben, immer
neuer Dateiname, gegenprüfen"* gilt unabhängig davon).

**Schreib den neuen Plan nach `ergebnisse/faltenplan_tb72.json`** und stelle
beide gegenüber: **welcher Bot, welche Falte, welcher Unterschied.**
⭐ **Erwartung: genau ein Bot, genau eine Falte.** ⚠️ **Weicht mehr ab, ist das
ein Befund** — melde ihn und arbeite nicht darüber hinweg.

**Sichern: commit und push.**

### Schritt 4 — der Benchmark-Lauf, daneben

**`benchmark.py --ziel ergebnisse/benchmark_drawdowns_tb72.json`**
(der Schalter kommt aus TB-61).

⛔ **`benchmark_drawdowns.json` bleibt byteweise unberührt**
(`a163c498…36d1ee`), **`benchmark_drawdowns_vt.json` ebenso**
(`4549395f…8745d`). **Hashes vorher und nachher.**

⭐ **Die Gegenprobe:** Für die **acht anderen Bots** muss die neue Tabelle
gegenüber `_vt.json` **zeichengleich** sein — alle Falten, alle 100 Stufen,
`handelstage`, Symbolzahlen. ⚠️ **Weicht dort etwas ab, ist der Lauf nicht
fertig.**

**Für `t3_supertrend` erwartet** (aus TB-65, Tabelle C1, Zeile *„ohne 2018"*):
`DD_Toleranz` **−13,90 / −26,57 / −48,10** bei 25 / 50 / 100 % statt
−12,89 / −24,73 / −45,16. ⚠️ **Trifft es nicht, sag es** — die Erwartung stammt
aus einer anderen Rechnung, deine Messung gilt.

**Sichern: commit und push.**

### Schritt 5 — der Neun-Zahlen-Vergleich als Test

**Ein Test, der bei Abweichung rot wird** — er gehört zu
`test_vorregistrierung.py` oder neben `faltenschranke_messung.py`, **du
entscheidest wo und begründest es**.

⭐⭐ **Er muss beissen können** (`B1`): Zeig mit einer **Mutation**, dass er rot
wird, wenn der Plan von 21.3 (b) abweicht. ⛔ **Ein Test, der nie rot werden
kann, ist keine Wache** (`A4`).

⚠️ **Fables Einordnung dazu:** Nach Schritt 2 ist der Test *„nicht mehr eine
Wache gegen Abweichung, sondern der Nachweis, dass die Ableitung nicht
regrediert."* Das gehört in seinen Docstring.

**Sichern: commit und push.**

### Schritt 6 — die Registernotiz

**Ein neuer Abschnitt 25**, nach dem Muster von 23 und 24:

| | Inhalt |
|---|---|
| **25.1** | Der Befund: 4a und 3b (a) weichen ab, 21.3 (b) entscheidet, kein Code setzte es um — mit der Fundstelle `faltenplan.py` Z. 39–42, die es selbst sagt |
| **25.2** | **Die Instanz:** `t3_supertrend` beginnt 2019, sieben Selektionsfalten statt acht |
| **25.3** | **Die Schliessung der Klasse:** Der Plan wird aus dem Trockenlauf abgeleitet; 4a bleibt die Regel, 3b (a) ist ihre operative Form |
| **25.4** | ⭐ **Die Wirkung, gemessen und bekannt** — `DD_Toleranz` wird **nachgiebiger**. ⚠️ **Mit dem Satz, dass die Richtung zugunsten des Bots geht und das an der Kategorie nichts ändert: die Quelle des Grundes ist die Regel** (F17, Fable wörtlich) |
| **25.5** | Was nicht getan wird: Sperrliste nicht vollzogen, Tag nicht gesetzt, `faltenplan.json` und die beiden Benchmark-Tabellen unberührt |

⛔ **Nichts im Register entfernen.** Append-only, `numstat` Spalte zwei = 0.

**Sichern: commit und push.**

### Schritt 7 — eine Backlog-Zeile und die Abgabe

**Eine** Zeile in Abschnitt 4, K-Nummer selbst gemessen (Muster
`^\| \*\*(K\d[a-z])\*\*` **ohne schliessenden Balken**, **kein `sort -u`**, über
`BACKLOG.md` **und** `BACKLOG_ARCHIV.md`).

`docs/ERGEBNIS_TB-72_erste_falte_aus_trockenlauf.md` und ein Journal-Nachtrag
⭐ **mit der Quellenzeile aus TB-67**.

**Sichern: commit und push.**

---

## 3. Die Nachweise

| # | Nachweis |
|---:|---|
| **1** | `git status --short` vor dem ersten Schreiben |
| **2** | ⭐ **Die neun Zahlen aus Schritt 1**, je Bot beide Werte, **aus dem Trockenlauf gemessen** — und ob die Vormessung aus Abschnitt 1 getroffen hat |
| **3** | ⭐ **SHA-256 von `benchmark_drawdowns.json` und `benchmark_drawdowns_vt.json`, vorher und nachher** — beide unverändert |
| **4** | `faltenplan.json` unverändert (Hash oder `git diff --numstat` = keine Zeile) |
| **5** | ⭐ **Die Gegenprobe der acht anderen Bots**: zeichengleich gegen `_vt.json`, Falten × Stufen benannt |
| **6** | `t3_supertrend`: Falten vorher/nachher, `DD_Toleranz` dreispaltig, gegen die Erwartung aus TB-65 |
| **7** | ⭐ **Die Mutation aus Schritt 5**: welche Änderung, welche Meldung, wieder zurückgenommen |
| **8** | `test_vorregistrierung.py`: Ergebnis je Teil, gegen TB-66 (dort: A bricht mit `KeyError: '2017'` ab — erwartet; in der Wegwerf-Kopie 163 bestanden, 2 gescheitert, G6 und H3) |
| **9** | Register: `numstat` Spalte zwei = **0** |
| **10** | `git diff --numstat` je Datei; nichts ausserhalb `docs/` und `research/` |

---

## 4. Die harten Auflagen

| | |
|---|---|
| ⛔ | **`benchmark_drawdowns.json` und `benchmark_drawdowns_vt.json` werden nicht angefasst** — die neue Tabelle heisst `benchmark_drawdowns_tb72.json` |
| ⛔ | **`ergebnisse/faltenplan.json` wird nicht überschrieben** — der neue Plan heisst `faltenplan_tb72.json` |
| ⛔ | **`auswertung.py` bleibt eingefroren** (Register 15.8 Nr. 3, TB-30b) |
| ⛔ | **Die vier gesperrten Rechenfunktionen in `benchmark.py` bleiben unverändert** — auch `bh_tagesrenditen` |
| ⛔ | **Keine Konstantenkopie** — `MIN_HISTORY_*` wird gelesen, nie abgeschrieben (`T56b.6`) |
| ⭐ | **Sichern nach jedem fertigen Teil** — sieben Commits oben benannt |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block** |
| ⚠️ | **Widersprich diesem Auftrag, wo er falsch ist.** ⭐ *Die letzten sieben Aufträge lagen je an mehreren Stellen daneben, und jedes Mal hatte die ausführende Sitzung recht — zuletzt TB-68 („als Widerspruch geboren", nicht auseinandergelaufen) und TB-71, das drei Marken ergänzt hat, die der Auftrag nicht nannte und ohne die das Register sich selbst widersprochen hätte* |
| ⭐ | **Entscheidungen an den Betreiber gehen als anklickbare Frage mit Empfehlung** (`ARBEITSWEISE.md` 6d) |

---

## 5. Was diese Aufgabe NICHT tut

| | |
|---|---|
| ⛔ | **Die Sperrlisten-Änderung vollziehen** — eigene Betreiberfreigabe (Register 21.9) |
| ⛔ | **Den Tag setzen** |
| ⛔ | **Die MtM-Wirkung messen** — das ist **TB-73**, und es darf erst nach TB-71 laufen (Register 24.3). TB-71 ist durch |
| ⛔ | **G6 und H3 reparieren** — bekannte rote Proben aus TB-61 |
| ⛔ | **`registerdaten.MINDESTTRAINING_JAHRE` entfernen** — `T56b.6`, eigene Aufgabe |

---

## In einfacher Sprache

**Was schiefsteht:** Das Regelwerk sagt, wann das erste Jahr eines Bots zählt —
nämlich sobald sein Programm wenigstens einen Kurs überhaupt handeln darf. Der
Plan rechnet das aber auf einem zweiten, eigenen Weg nach. Bei einem Bot kommen
beide Wege zu verschiedenen Ergebnissen, und er führt deshalb ein Jahr, in dem
er gar nichts handeln kann.

**Was diese Aufgabe macht:** Zweierlei. Sie berichtigt den einen Bot — er
beginnt ein Jahr später. Und sie schafft den zweiten Rechenweg ab: Der Plan
liest künftig ab, was das Programm wirklich kann, statt es nachzurechnen. Dann
können die beiden nie wieder auseinanderlaufen.

**Was du danach weisst:** Ob wirklich nur ein Bot betroffen war. Die Vormessung
aus dem Chat sagt ja — aber sie hat einen blinden Fleck, und die Aufgabe
schliesst ihn.

**Was sich an Zahlen ändert:** Die Verlustgrenze dieses einen Bots wird etwas
weiter. Das ist die Wirkung, nicht der Grund — der Grund ist die Regel, und die
stand vorher fest.

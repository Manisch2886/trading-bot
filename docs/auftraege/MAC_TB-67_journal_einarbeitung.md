# TB-67 Die Journal-Seite nachziehen — an: Claude Code am Mac (lokale Sitzung)

**Sitzungstitel für Claude Code: `TB-67 Journal nachziehen`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main`.

⭐ **Rechnet nicht.** Reine Dokumentation.
⚠️ **Unabhängig von TB-63, TB-64 und TB-66** — fasst `BACKLOG.md` nur an einer
Stelle an (Abschnitt 4, eine Zeile) und `ARBEITSWEISE.md` gar nicht.

---

## 0. Warum es diese Aufgabe gibt — gemessen am 20.09.2026

**`JOURNAL.md` hat einen Rückstand, den bisher niemand geführt hat.**

| | gemessen |
|---|---|
| Journal-Nachträge in `docs/projektfuehrung/nachtraege/` | **zehn** — `(c)`, `(d)`, `(e)`, `(f)`, `(g)`, `(20a)` bis `(20e)` |
| davon eingearbeitet | **drei** (`c`, `d`, `e` — je 2 Treffer über die TB-Nummer) |
| ⛔ **nicht eingearbeitet** | **`(g)`, `(20a)`, `(20b)`, `(20c)`, `(20d)`, `(20e)`** — je 0 Treffer |
| ⚠️ **nicht prüfbar** | **`(f)`** — sein Titel nennt keine TB-Nummer, es gibt keine Kennung *(A2: nicht grün, nicht rot)* |
| Letzter Journalblock | **`BJ`** (TB-54) |

⚠️⚠️ **Dazu ein zweiter Rückstand, den TB-62 gefunden hat:**
`BACKLOG_NACHTRAG_2026-09-19m.md` enthält einen **Rückblick-Block mit 20 Zeilen**
(`T53.1`–`T53.4`, `T58.1`–`T58.6`, `T58b.1`–`T58b.3`, `B1`–`B7`) zu **TB-53b,
TB-58 und TB-58b**. **Gemessen: `T53.1`, `T58.1`, `T58b.3` und `index.lock`
haben je 0 Treffer** in `BACKLOG.md`, `BACKLOG_ARCHIV.md` und `JOURNAL.md`.

⭐⭐ **Damit haben drei erledigte Aufgaben keinen Journalblock** — und ihr
Messprotokoll existiert nur in einer Nachtragsdatei, die nie eingearbeitet wurde.

---

## 1. Wo der Rückblick-Block hingehört — und warum das keine offene Frage ist

TB-62 hat den Ort als **offene Betreiberentscheidung** vorgelegt. ⭐ **Er ist
keine:** Die Regel steht seit jeher in **Zeile 3 von `BACKLOG.md`**:

> *„Nur **aktive Punkte**. Alles Abgeschlossene steht im `JOURNAL.md` und wird
> von dort **nicht** zurückgeholt."*

Und `VORLAGEN`-Abschnitt 4 sagt dasselbe von der anderen Seite: *„`JOURNAL.md` —
abgeschlossene Blöcke, nie umgeschrieben, nur ergänzt."*

⇒ **Der Rückblick-Block wird Journalblöcke.** ⚠️ **`BACKLOG_ARCHIV.md` kommt
nicht in Frage** — das ist nach TB-60 definiert als *„aus dem Backlog verschoben,
per Diff nachgewiesen"*. Etwas, das nie im Backlog stand, kann dorthin nicht
verschoben werden.

---

## 2. Die Schritte

### Schritt 0 — vor allem anderen

**Committe, was im Arbeitsbaum liegt.** Nachweis „sauber" wird **danach**
geprüft.

### Schritt 1 — messen, welche Nachträge wirklich offen sind

⛔ **Verlass dich nicht auf die Tabelle in Abschnitt 0.** Sie ist der Stand vom
20.09., und TB-62 hat seither Nachträge erzeugt.

**Für jeden der zehn Journal-Nachträge:** Steht sein Inhalt im Journal?

⚠️⚠️ **Das Muster über die TB-Nummer im Titel reicht nicht** — `(f)` hat keine.
⭐ **Nimm zusätzlich einen charakteristischen Satz aus dem Nachtrag** und such
ihn wörtlich im Journal. **Nenne je Nachtrag, welches Muster getroffen hat.**

⚠️ **Findest du einen, bei dem beide Muster versagen, ist er *nicht prüfbar*,
nicht *offen*** — und das steht dann so da (`A2`).

**Sichern: commit und push.**

### Schritt 2 — die offenen Journal-Nachträge einarbeiten

**Angefügt am Ende von `JOURNAL.md`, in der Reihenfolge ihrer Entstehung.**
⛔ **Nichts im Journal wird umgeschrieben** — es ist eine der vier Ausnahmen von
`DOKUMENTATIONSSTANDARD.md` Regel 9.

⭐ **Blockbuchstaben fortlaufend ab dem gemessenen letzten.** ⚠️ **Miss ihn
selbst** — dieser Auftrag nennt ihn in Abschnitt 0 mit Stand vom 20.09.

⭐⭐ **Jeder neue Block trägt eine Quellenzeile:**

```
*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_<datum><buchstabe>.md`*
```

**Das ist die Kennung, die heute fehlt** — und die `TB-64` braucht, um
Journal-Nachträge überhaupt prüfen zu können.

⭐ **Trage sie auch bei `(c)`, `(d)`, `(e)` nach**, wenn du ihre Blöcke
**eindeutig** zuordnen kannst. ⛔ **Kannst du es nicht, lass das Journal
unberührt und melde sie als nicht prüfbar.** *Nichts erraten.*

**Sichern: commit und push.**

### Schritt 3 — der Rückblick-Block aus Nachtrag (m)

**Drei Journalblöcke** für TB-53b, TB-58 und TB-58b, aus den 20 Zeilen des
Blocks `2s` in `BACKLOG_NACHTRAG_2026-09-19m.md`.

⚠️ **Die Zeilen `B1`–`B7` sind etwas anderes als die `T`-Zeilen** — sie sind
Arbeitsregeln, keine Messprotokolle. **Prüfe für jede der sieben, ob sie
inzwischen in einem Führungsdokument steht**, und berichte das Ergebnis je
Zeile. ⛔ **Trage sie nicht selbst als Regel ein** — das ist eine eigene
Entscheidung.

⭐ **Die Quellenzeile aus Schritt 2 gilt auch hier**, mit dem Backlog-Nachtrag
als Quelle.

**Sichern: commit und push.**

### Schritt 4 — eine Zeile im Backlog

**Eine** Zeile in Abschnitt 4, die festhält: Journal-Rückstand abgearbeitet, wie
viele Blöcke, welche Nachträge nicht prüfbar waren. ⭐ **Nächste freie K-Nummer
selbst messen**, mit dem Muster `^\| \*\*(K\d[a-z])\*\*` **ohne schliessenden
Balken** und **ohne `sort -u`**.

⛔ **Nur eine Zeile.** Der Inhalt der Journalblöcke wird nicht wiederholt.

**Sichern: commit und push.**

### Schritt 5 — die eingearbeiteten Nachträge verschieben

**Nach `docs/projektfuehrung/nachtraege/_eingearbeitet/`** — nur die, deren
Inhalt du in Schritt 1 oder 2 als angekommen gemessen hast.

⛔ **Nichts verschieben, was du nicht geprüft hast.**
⚠️ **Das ist derselbe Ort, den `TB-64` erwartet** — wenn `TB-64` vorher lief und
den Ordner schon angelegt hat, benutze ihn; wenn nicht, lege ihn an und sag es.

**Sichern: commit und push.**

### Schritt 6 — die Abgabe

`docs/ERGEBNIS_TB-67_journal_einarbeitung.md` und ein Journal-Nachtrag
⭐ **mit der neuen Quellenzeile**.

**Sichern: commit und push.**

---

## 3. Die Nachweise

| # | Nachweis |
|---:|---|
| **1** | `git status --short` vor dem ersten Schreiben |
| **2** | ⭐ Die Messung aus Schritt 1, **je Nachtrag mit dem Muster, das getroffen hat** — und die nicht prüfbaren getrennt |
| **3** | `git diff --numstat` je Datei. ⭐ **Für `JOURNAL.md` erwartet: Spalte zwei = 0** (nur angefügt) |
| **4** | Blockbuchstaben: letzter vorher, letzter nachher, **keiner doppelt** |
| **5** | Die Quellenzeilen: wie viele neu, wie viele nachgetragen, wie viele nicht zuordenbar |
| **6** | Schritt 3: je `B`-Zeile, ob sie in einem Führungsdokument steht, mit Fundstelle |
| **7** | Was nach `_eingearbeitet/` verschoben wurde, und was offen bleibt |
| **8** | Nichts ausserhalb `docs/` geändert |

---

## 4. Die harten Auflagen

| | |
|---|---|
| ⛔ | **Im Journal wird nichts umgeschrieben** — nur angefügt, ausser der Quellenzeile |
| ⛔ | **Die sieben `B`-Zeilen werden nicht als Regeln eingetragen** — nur geprüft und berichtet |
| ⛔ | **Nichts erraten.** Unklare Zuordnung ⇒ *nicht prüfbar*, und das steht so da |
| ⭐ | **Sichern nach jedem fertigen Teil** — sechs Commits oben benannt |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block** |
| ⭐ | **Jede Zahl gezählt, gegen eine zweite Zählung gehalten** |
| ⚠️ | **Widersprich diesem Auftrag, wo er falsch ist.** ⭐ *Die letzten vier Aufträge lagen je an mehreren Stellen daneben, und jedes Mal hat die ausführende Sitzung recht behalten* |

---

## 5. Was diese Aufgabe NICHT tut

| | |
|---|---|
| ⛔ | **`BACKLOG.md` umbauen** — eine Zeile in Abschnitt 4, mehr nicht |
| ⛔ | **Die Epics auslagern** (TB-63) |
| ⛔ | **Den Wächter bauen** (TB-64) |
| ⛔ | **An `research/` oder am Register arbeiten** |
| ⛔ | **Entscheiden, ob die `B`-Regeln gelten** |

---

## In einfacher Sprache

**Was schiefgelaufen ist:** Das Journal ist das Buch, in dem steht, was gemessen
wurde und was dabei herauskam. Sieben Einträge dafür liegen seit Tagen als
einzelne Notizdateien herum und sind nie übertragen worden. **Drei erledigte
Aufgaben haben deshalb gar keinen Eintrag** — ihr Messprotokoll existiert nur in
einer Datei, die niemand mehr liest.

**Was diese Aufgabe macht:** Sie trägt alle offenen Notizen ins Journal nach und
gibt jedem Eintrag eine Zeile, die sagt, aus welcher Notiz er stammt. **Diese
Zeile fehlt heute** — und ohne sie kann später niemand prüfen, ob eine Notiz
angekommen ist. Genau daran ist eine Notiz vom 19. zwei Tage lang unbemerkt
liegengeblieben.

**Was du danach hast:** Ein vollständiges Journal, einen leeren Notizordner, und
eine Kennung, mit der der Wächter aus TB-64 künftig selbst merkt, wenn wieder
etwas liegenbleibt.

# TB-75 Die Journal-Seite nachziehen — sieben Nachträge, und die Frage, ob der Umweg noch nötig ist

**an: Claude Code am Mac (lokale Sitzung)**

**Sitzungstitel für Claude Code: `TB-75 Journal nachziehen`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main`.

⭐ **Rechnet nicht.** ⚠️ **Fasst `BACKLOG.md` nur an einer Zeile an**, `JOURNAL.md`
nur anfügend.

---

## 0. Warum es diese Aufgabe gibt

**TB-67 hat die Journal-Seite am 20.09. leergeräumt. Seither sind sieben neue
Nachträge entstanden, keiner davon eingearbeitet.**

| | |
|---|---|
| offen | `(20g)`, `(20h)`, `(20i)`, `(20j)`, `(20k)`, `(20l)` aus TB-67 bis TB-73, **und `(20m)`** aus TB-64 |
| letzter Journalblock | **selbst messen** — TB-67 endete bei `BT`, seither kann sich das geändert haben |
| Quellenzeilen | ⭐ alle sieben tragen sie bereits (die Regel aus TB-67 hat gegriffen) |
| ⚠️ | **Der Wächter aus TB-64 meldet sie ab dem zweiten Morgen nach ihrer Entstehung.** Diese Aufgabe ist das, was er einfordert |

---

## 1. Die Schritte

### Schritt 0 — vor allem anderen

**Committe, was im Arbeitsbaum liegt**, getrennt nach Urheber.

### Schritt 1 — messen, was wirklich offen ist

⛔ **Verlass dich nicht auf die Liste oben.** ⭐ **Lass den Wächter selbst
laufen** — `system/nachtragswaechter.py`, rein lesend — und nimm **seine**
Antwort. *Das ist zugleich seine zweite Bewährung am echten Bestand.*

⚠️ **Weicht seine Liste von der oben ab, gilt seine** — und du sagst, worin.

**Sichern: commit und push.**

### Schritt 2 — die Blöcke anfügen

**Am Ende von `JOURNAL.md`, in der Reihenfolge ihrer Entstehung.**
⛔ **Nichts umschreiben** — Regel 9, eine der vier Ausnahmen.
⭐ **Blockbuchstaben fortlaufend ab dem gemessenen letzten.**
⭐ **Jeder Block trägt seine Quellenzeile**, aus dem Nachtrag übernommen.

⚠️ **Sieben Nachträge sind viel Text.** ⛔ **Nicht abschreiben** — jeder Block
hält fest, **was gemessen wurde und was dabei herauskam**, nicht den
Sitzungsverlauf. *Der Nachtrag bleibt als Quelle erhalten; das Journal ist die
Kurzfassung mit Zeigern.*

**Sichern: commit und push.**

### Schritt 3 — verschieben und nachprüfen

**Nach `docs/projektfuehrung/nachtraege/_eingearbeitet/`, per `git mv`.**
⭐ **Danach den Wächter erneut laufen lassen** — er muss **0 über der Frist**
melden. ⚠️ **Tut er es nicht, ist etwas nicht angekommen**; dann sag es, statt
zu verschieben.

**Sichern: commit und push.**

### Schritt 4 — ⭐⭐ eine Messung, keine Änderung: ist der Umweg noch nötig?

⚠️ **Nicht ausführen, nur messen und vorlegen.**

**Der Ablauf ist heute:** eine Mac-Sitzung schreibt bei der Abgabe eine
Nachtragsdatei; eine spätere Sitzung trägt sie ins Journal; der Wächter passt
auf, dass das geschieht. **Drei Schritte für einen Eintrag.**

**Die Frage:** Warum schreibt die Sitzung ihren Journalblock nicht gleich
selbst ans Ende von `JOURNAL.md`?

⭐ **Miss, was dagegen spricht**, statt es zu vermuten:

| | zu prüfen | wo |
|---|---|---|
| **1** | Laufen je zwei Sitzungen gleichzeitig im selben Arbeitsbaum? | `ARBEITSWEISE.md`, `AKTUELLER_AUFTRAG.md` — die Regel sagt nein; **prüfe, ob sie je verletzt wurde** (Commit-Zeitstempel zweier TB-Nummern überlappend) |
| **2** | Was passiert, wenn eine Sitzung mitten im Schreiben abbricht? | Am 20.09. sind **drei** Sitzungen abgebrochen. Was hätte ein halb geschriebener Journalblock bedeutet? |
| **3** | Wer vergibt den Blockbuchstaben, und kann er kollidieren? | heute misst ihn die einarbeitende Sitzung |
| **4** | Was bliebe vom Wächter übrig? | Prüfung B und C (falsch verschoben, Doppelbelegung) hängen nicht am Journal |
| **5** | Trägt der Nachtrag etwas, das im Journal keinen Platz hat? | Vergleich eines Paares: `(20m)` gegen den Block, den du dafür schreibst |

⛔ **Entscheide nicht.** ⭐ **Leg es dem Betreiber als anklickbare Frage mit
Empfehlung vor** (`ARBEITSWEISE.md` 6d) — **und nenne ausdrücklich, was ein
Wegfall den gestern gebauten Wächter kostet.**

**Sichern: commit und push.**

### Schritt 5 — eine Backlog-Zeile und die Abgabe

**Eine** Zeile in Abschnitt 4, K-Nummer selbst gemessen (Muster
`^\| \*\*(K\d[a-z])\*\*` **ohne schliessenden Balken**, **kein `sort -u`**, über
`BACKLOG.md` **und** `BACKLOG_ARCHIV.md`).

`docs/ERGEBNIS_TB-75_journal_nachziehen.md` und ein Journal-Nachtrag
⭐ **mit Quellenzeile** — *oder, falls Schritt 4 es nahelegt und der Betreiber
zustimmt, der Block direkt im Journal; dann sag es.*

**Sichern: commit und push.**

---

## 2. Die Nachweise

| # | Nachweis |
|---:|---|
| **1** | `git status --short` vor dem ersten Schreiben |
| **2** | ⭐ **Die Wächter-Ausgabe aus Schritt 1**, und ob sie von der Liste in Abschnitt 0 abweicht |
| **3** | `JOURNAL.md`: `numstat` Spalte zwei = **0** |
| **4** | Blockbuchstaben: letzter vorher, letzter nachher, **keiner doppelt** |
| **5** | Quellenzeilen: wie viele neu, wie viele nicht zuordenbar |
| **6** | ⭐ **Die Wächter-Ausgabe nach Schritt 3** — 0 über der Frist |
| **7** | Schritt 4: die fünf Punkte einzeln, mit Fundstelle |
| **8** | `git diff --numstat` je Datei; nichts ausserhalb `docs/` |

---

## 3. Die harten Auflagen

| | |
|---|---|
| ⛔ | **Im Journal wird nichts umgeschrieben** — nur angefügt |
| ⛔ | **Kein Nachtrag wird abgeschrieben** — der Block ist die Kurzfassung |
| ⛔ | **Schritt 4 ändert nichts** — messen und vorlegen |
| ⛔ | **Der Wächter wird nicht angefasst** |
| ⭐ | **Sichern nach jedem fertigen Teil** |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block** |
| ⚠️ | **Widersprich diesem Auftrag, wo er falsch ist.** ⭐ *Die letzten neun Aufträge lagen je an mehreren Stellen daneben — zuletzt TB-73, das meine Auflage „M nie flacher als E" widerlegt hat, und TB-64, dessen Schritt-1-Messung zeigte, dass eine reine Nummernzählung `(m)` als angekommen gemeldet hätte, obwohl fremder Inhalt dort stand* |

---

## In einfacher Sprache

**Was offen ist:** Jede Aufgabe hinterlässt eine Notiz darüber, was gemessen
wurde. Sieben davon liegen herum und gehören ins Journal — das Buch, in dem
steht, was das Projekt gelernt hat.

**Was neu ist:** Seit gestern gibt es eine Wache, die genau das anmahnt. Diese
Aufgabe ist das, was sie einfordert — und zugleich ihre zweite Bewährung.

**Und eine Frage zum Mitdenken:** Heute braucht ein Journaleintrag drei
Schritte — Notiz schreiben, später eintragen, Wache passt auf. Vielleicht
genügt einer. Die Aufgabe misst, was dagegen spricht, und legt es dir vor —
entschieden wird nichts.

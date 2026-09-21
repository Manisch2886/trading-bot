# TB-76 Der Wächter kennt sein drittes Ziel nicht — und wird morgen um 04:50 zum ersten Mal falsch melden

**an: Claude Code am Mac (lokale Sitzung)**

**Sitzungstitel für Claude Code: `TB-76 Waechter-Ziele`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main`.

⭐ **Klein.** ⚠️ **Eilig** — die Cron-Zeile ist seit dem 21.09., 10:50 eingetragen;
**der erste automatische Lauf ist am 22.09. um 04:50.**

---

## 0. Warum es diese Aufgabe gibt

**TB-63 hat `BACKLOG_EPICS.md` angelegt. Der Wächter aus TB-64 kennt die Datei
nicht.**

| | |
|---|---|
| **Befund** | `system/nachtragswaechter.py` meldet seit TB-63 **rc 1**, *„3 falsch verschoben"* — die Nachträge `(19n)`, `(19o)`, `(19p)` mit den Blöcken `2t`–`2v`. Ihr Inhalt **ist** angekommen, nur eben in `BACKLOG_EPICS.md` |
| **Ursache** | Klasse `Ziel`, `nachtragswaechter.py:222` — das Ziel ist **fest** `BACKLOG.md` + `BACKLOG_ARCHIV.md` |
| **Gegenprobe (TB-63, ohne Codeänderung)** | mit `--archiv <Archiv + Epics aneinandergehängt>` → **rc 0** |
| ⚠️⚠️ **Warum es eilt** | `A4`: *„Ein dauerhaft roter Test ist keine Wache."* Meldet der Wächter ab morgen jeden Tag dasselbe falsche Ergebnis, wird die Meldung binnen einer Woche überlesen — **und dann meldet er auch das Echte vergeblich** |

⭐ **TB-63 hat es richtig gemacht:** gemessen, die Gegenprobe gefahren, **nicht
behoben** — die Änderung liegt ausserhalb `docs/`, und der Auftrag erlaubte das
nicht. *Der Befund steht als `K4o` im Backlog.*

---

## 1. Was zu tun ist

### Schritt 0 — vor allem anderen

**Committe, was im Arbeitsbaum liegt**, getrennt nach Urheber.

### Schritt 1 — den Befund reproduzieren, bevor etwas geändert wird

**Lass den Wächter laufen und halte fest:** rc, welche drei Nachträge, welche
Blöcke, mit welcher Begründung.

⛔ **Verlass dich nicht auf Abschnitt 0** — er ist der Stand von TB-63.
⚠️ **Meldet er etwas anderes, gilt deine Messung**, und du sagst, worin sie
abweicht.

**Sichern: commit und push.**

### Schritt 2 — die Zielmenge wird gelesen, nicht aufgezählt

⛔ **Nicht einfach `BACKLOG_EPICS.md` in die Liste schreiben.** ⭐ **Das ist der
Fehler, der wiederkommt** — die nächste ausgelagerte Datei hätte dasselbe
Problem. *`BACKLOG_ARCHIV.md` und `BACKLOG_EPICS.md` sind beide durch
Auslagerung entstanden; es wird eine dritte geben.*

⭐ **Miss zuerst, woran man eine Zieldatei erkennt**, und leg die Regel fest:

| Kandidat | zu prüfen |
|---|---|
| **Muster im Dateinamen** | `docs/projektfuehrung/BACKLOG*.md` — wie viele Dateien trifft das heute, und trifft es etwas Falsches? |
| **Eine Liste im Kopf von `BACKLOG.md`** | Steht dort schon, wohin ausgelagert wurde? TB-63 hat eine Verweistabelle angelegt |
| **Aufzählung wie bisher, nur erweitert** | der einfachste Weg, und der, der wiederkommt |

⭐ **Entscheide das selbst** — es ist eine Handwerksfrage. ⚠️ **Aber begründe
sie**, und nenne, was dein Weg beim nächsten Mal kostet.

⛔ **Was sich NICHT ändern darf:** die dreistufige Ankunftsprüfung aus TB-64
(Zielzeile mit Textkern, Kern anderswo, Vergabevermerk mit Bindung an den
Nachtrag). *Sie ist der Grund, warum der Wächter den Fall `(m)` gefunden hat.*

**Sichern: commit und push.**

### Schritt 3 — die Probe muss beissen können

⭐⭐ **Erweitere `system/test_nachtragswaechter.py` um Fälle, die die neue Regel
prüfen** — mindestens:

| | Fall | Erwartung |
|---|---|---|
| **1** | Inhalt in der ausgelagerten Datei angekommen | **grün** |
| **2** | Inhalt **nirgends** angekommen, auch nicht in der ausgelagerten | **rot** |
| **3** | Eine **weitere** ausgelagerte Datei kommt dazu | **grün ohne Codeänderung** — das ist der Punkt von Schritt 2 |

⭐ **Und eine Mutationsprobe**, wie TB-64 sie gefahren hat: Mach die Zielmenge
kaputt und zeig, dass der Test rot wird. ⛔ **Danach zurücknehmen**, `numstat`
leer.

**Sichern: commit und push.**

### Schritt 4 — der Lauf gegen den echten Bestand

**`rc 0` erwartet** — 0 offen, 0 falsch verschoben, 0 doppelt, und die vier
bekannten `[?]` unverändert.

⚠️ **Kommt etwas anderes, ist es ein Befund** und kein Grund, die Regel
nachzubiegen, bis es passt.

**Sichern: commit und push.**

### Schritt 5 — der Journalblock und die Abgabe

⭐⭐ **Der Block geht DIREKT ins Journal** — Buchstabe gemessen, Quellenzeile auf
das eigene Ergebnisdokument (`ARBEITSWEISE.md` 14, seit dem 21.09.).
⛔ **Keine Nachtragsdatei.**

Dazu `docs/ERGEBNIS_TB-76_waechter_ziele.md` und **eine** Backlog-Zeile in
Abschnitt 4 (K-Nummer selbst gemessen, Muster `^\| \*\*(K\d[a-z])\*\*` **ohne
schliessenden Balken**, **kein `sort -u`**, über `BACKLOG.md`,
`BACKLOG_ARCHIV.md` **und `BACKLOG_EPICS.md`** — die dritte Datei ist neu und
gehört in die Zählung). ⭐ **`K4o` wird damit geschlossen.**

**Sichern: commit und push.**

---

## 2. Die Nachweise

| # | Nachweis |
|---:|---|
| **1** | `git status --short` vor dem ersten Schreiben |
| **2** | ⭐ Schritt 1: der Befund vor der Änderung, rc und Begründung je Nachtrag |
| **3** | ⭐ Schritt 2: **woran eine Zieldatei erkannt wird**, gemessen, mit der Zahl der heute getroffenen Dateien — und was der Weg beim nächsten Mal kostet |
| **4** | ⭐⭐ Die drei Testfälle aus Schritt 3, je mit Ergebnis; **Fall 3 ohne Codeänderung** |
| **5** | Die Mutationsprobe: welche Mutation, welche Meldung, zurückgenommen, `numstat` leer |
| **6** | Schritt 4: rc 0 gegen den echten Bestand |
| **7** | `git diff --numstat` je Datei; **nichts ausserhalb `system/` und `docs/`** |

---

## 3. Die harten Auflagen

| | |
|---|---|
| ⛔ | **Die dreistufige Ankunftsprüfung bleibt unverändert** |
| ⛔ | **Keine Datei im Backlog-Bestand wird verschoben oder umbenannt** — nur der Wächter lernt dazu |
| ⛔ | **Nichts in `research/`, `strategies/`, `shared/`** |
| ⭐ | **Sichern nach jedem fertigen Teil** |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block** |
| ⚠️ | **Widersprich diesem Auftrag, wo er falsch ist.** ⭐ *Die letzten zehn Aufträge lagen je an mehreren Stellen daneben — zuletzt TB-63, dessen Endanker ich mit `## 3` falsch angegeben hatte; die Sitzung hat gemessen, dass seit TB-62 Block `2z` dazwischenliegt, und den Bereich an den Ankertexten neu bestimmt* |

---

## In einfacher Sprache

**Was schiefsteht:** Gestern wurde eine Wache gebaut, die meldet, wenn eine
Messnotiz liegenbleibt. Heute wurde ein Teil des Backlogs in eine neue Datei
ausgelagert — und die Wache kennt diese Datei nicht. Sie meldet deshalb drei
Notizen als verschwunden, die längst angekommen sind.

**Warum es eilt:** Ab morgen früh läuft die Wache automatisch. Eine Meldung, die
jeden Tag dasselbe Falsche sagt, wird nach einer Woche überlesen — und dann
nützt sie auch nichts mehr, wenn wirklich etwas fehlt.

**Was diese Aufgabe macht:** Sie bringt der Wache bei, ihre Ziele zu **finden**
statt sie auswendig zu kennen. Dann kostet die nächste ausgelagerte Datei keine
Änderung mehr.

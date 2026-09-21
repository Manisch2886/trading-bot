# TB-69 `ARBEITSWEISE.md` neu ordnen — die Ausgaberegeln stehen an fünf Stellen, und das hat vier Verstösse gekostet

**an: Claude Code am Mac (lokale Sitzung)**

**Sitzungstitel für Claude Code: `TB-69 ARBEITSWEISE ordnen`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main`.

⭐ **Rechnet nicht.** ⚠️⚠️ **Aber es ist der heikelste Dokumentationsauftrag
bisher:** `ARBEITSWEISE.md` ist das Dokument, nach dem der steuernde Chat
arbeitet. **Eine verlorene Regel fällt erst auf, wenn sie verletzt wird.**

---

## 0. Warum es diese Aufgabe gibt — gemessen am 21.09.2026, 13:00

| | gemessen |
|---|---|
| Grösse | **70 905 B** (am 20.09. früh: 55 486) |
| Abschnitte | **25**, davon **sieben nachträglich eingeschoben**: `5b`, `6b`, `6bb`, `6c`, `6d`, `7b`, `7c` |
| Unterabschnitte | **15** |
| ⚠️ **Die Ausgaberegeln** | verstreut über **6b** (Schritt für Schritt, Kopierblöcke, Sitzungsende, Editor-Befehle), **6bb** (Aufgabenblock am Ende), **6c** (keine Arbeitszeitangaben), **6d** (Entscheidung als anklickbare Frage) |

⭐⭐ **Der Anlass ist nicht kosmetisch, sondern viermal gemessen** — alle vier am
20.09.2026, alle mit vorhandener Regel:

| | Verstoss | Regel stand in |
|---|---|---|
| **1–3** | Dreimal eine Entscheidungsvorlage **ohne Empfehlung** (12:40, 12:58, 14:25) | `6d` |
| **4** | Die Startbefehle **im Fliesstext** statt als Kopierblöcke | `6b` |
| **5** | Eine Entscheidung **als Absatz** statt als anklickbare Frage (17:58) | `6d`, der die **Form** nicht nannte |
| **6** | `crontab -e` **zweimal ohne den Ausstieg** (20./21.09.) | stand nirgends — jetzt `6b` |

⚠️ **Die Ursache steht bereits in `6d` und ist nie behoben worden:**

> *„Es gibt keine Stelle, die vor dem Absenden einer Antwort als Liste gilt — und
> verstreute Regeln werden beim Schreiben nicht gelesen, sondern erinnert."*

---

## 1. Was diese Aufgabe erreichen soll

⭐ **Eine Liste, die vor jeder Antwort gilt.** Nicht fünf Unterabschnitte, in
denen dieselbe Sache je zur Hälfte steht.

⛔ **Und sie darf keine Regel verlieren.** *Das ist die eigentliche Schwierigkeit,
nicht das Umsortieren.*

---

## 2. Die Schritte

### Schritt 0 — vor allem anderen

**Committe, was im Arbeitsbaum liegt**, getrennt nach Urheber.

### Schritt 1 — ⭐⭐ die Regelliste, bevor irgendetwas bewegt wird

**Geh das ganze Dokument durch und schreib jede Regel als eine Zeile auf:**
laufende Nummer, Abschnitt, Kern in einem Satz, und ob sie **die Ausgabe einer
Antwort** betrifft oder etwas anderes.

⭐ **Das ist der Prüfmassstab für alles Weitere** — ohne ihn lässt sich nachher
nicht zeigen, dass nichts verloren ging.

**Leg sie als Beleg ab:** `docs/belege/TB-69/regelliste_vorher.md`.

⚠️ **Nenne die Zahl.** Sie ist das SOLL für Schritt 4.

**Sichern: commit und push.**

### Schritt 2 — die Ausgabe-Checkliste bauen

⭐ **Ein neuer Abschnitt, ganz vorn oder ganz hinten** — du entscheidest wo und
begründest es. Er enthält **jede** Regel, die die Ausgabe einer Antwort betrifft,
als **eine Zeile mit einem Zeiger** auf den Abschnitt, der sie ausführt.

⛔ **Die Checkliste erklärt nichts.** Sie ist zum Abhaken da, nicht zum Lesen.
*Ein Abschnitt, der beides will, wird beim Schreiben wieder nicht gelesen.*

⚠️ **Die ausführenden Abschnitte bleiben stehen** — mit ihren Messungen,
Anlässen und Berichtigungen. **Die Checkliste ersetzt sie nicht, sie findet
sie.**

**Sichern: commit und push.**

### Schritt 3 — die eingeschobenen Abschnitte einordnen

**Sieben tragen Buchstabennummern**, weil sie nachträglich dazukamen.
⭐ **Ordne sie ein und nummeriere durch** — oder lass sie, wenn du begründen
kannst, dass Umnummerieren mehr kostet als es bringt.

⚠️⚠️ **Wenn du umnummerierst, sind die Verweise die Gefahr.** ⭐ **Miss zuerst,
wie viele es gibt und wo** — `ARBEITSWEISE`-Verweise in `BACKLOG.md`,
`DOKUMENTATIONSSTANDARD.md`, `UMZUG.md`, `UEBERGABE_*.md`, `JOURNAL.md`, den
Ergebnisdokumenten und den Aufträgen. **Nenne die Zahl, bevor du entscheidest.**

⛔ **Ein toter Verweis ist schlimmer als eine hässliche Nummer.** *Genau daran
ist am 20.09. ein zweites Projekt gescheitert.*

**Sichern: commit und push.**

### Schritt 4 — ⭐⭐ der Nachweis, dass nichts verloren ging

**Dieselbe Liste wie in Schritt 1, aus dem neuen Stand erzeugt.**

| | zu zeigen |
|---|---|
| **1** | **Jede Regel der Vorher-Liste findet sich wieder** — je Nummer, mit ihrem neuen Ort |
| **2** | **Was neu ist**, ist nur die Checkliste selbst |
| **3** | ⭐ **Zeichengleich, wo nicht umgeschrieben wurde** — die Messungen und Anlässe in den Abschnitten bleiben wörtlich |
| **4** | ⚠️ **Was du absichtlich gestrichen hast, einzeln mit Begründung** — nach der Betreiberregel vom 20.09. darf Obsoletes weg, **aber nie stillschweigend** |

⛔ **Findet sich eine Regel nicht wieder, ist der Auftrag nicht fertig.**

**Sichern: commit und push.**

### Schritt 5 — der Journalblock und die Abgabe

⭐ **Block DIREKT ins Journal**, Buchstabe gemessen, Quellenzeile auf das eigene
Ergebnisdokument. ⛔ **Keine Nachtragsdatei.**

`docs/ERGEBNIS_TB-69_arbeitsweise_ordnen.md` und **eine** Backlog-Zeile in
Abschnitt 4 (K-Nummer selbst gemessen, Muster `^\| \*\*(K\d[a-z])\*\*` **ohne
schliessenden Balken**, **kein `sort -u`**, über `BACKLOG.md`,
`BACKLOG_ARCHIV.md` **und `BACKLOG_EPICS.md`**).

⭐ **Die Projektablage:** `ARBEITSWEISE.md` ist ein Führungsdokument — nenne im
Ergebnisdokument ausdrücklich, dass sie nachzuziehen ist (`K4e`). **Der
steuernde Chat tut das.**

**Sichern: commit und push.**

---

## 3. Die Nachweise

| # | Nachweis |
|---:|---|
| **1** | `git status --short` vor dem ersten Schreiben |
| **2** | ⭐⭐ **Die Regelliste vorher**, mit der Zahl |
| **3** | ⭐⭐ **Die Wiederfind-Prüfung aus Schritt 4**, je Regel, mit neuem Ort |
| **4** | Was gestrichen wurde, **einzeln mit Begründung** — oder ausdrücklich: nichts |
| **5** | Schritt 3: Zahl der Verweise je Datei, **vor** der Entscheidung über das Umnummerieren |
| **6** | Wenn umnummeriert: **jeder Verweis nachgezogen**, Trefferzahl vorher und nachher gleich |
| **7** | `git diff --numstat` je Datei; nichts ausserhalb `docs/` |
| **8** | Grösse vorher und nachher, mit dem Anteil, der auf die Checkliste entfällt |

---

## 4. Die harten Auflagen

| | |
|---|---|
| ⛔ | **Keine Regel verschwindet stillschweigend** — das ist die einzige Auflage, die wirklich zählt |
| ⛔ | **Die Messungen und Anlässe in den Abschnitten bleiben wörtlich** — sie sind der Grund, warum die Regeln ernst genommen werden |
| ⛔ | **Die Checkliste erklärt nichts** |
| ⚠️ | **Kein toter Verweis**, auch nicht in `JOURNAL.md` oder in alten Ergebnisdokumenten. *Ist ein Verweis dort nicht nachziehbar, weil das Dokument unveränderlich ist, sag es — dann ist Umnummerieren die falsche Wahl* |
| ⭐ | **Sichern nach jedem fertigen Teil** |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block** |
| ⚠️ | **Widersprich diesem Auftrag, wo er falsch ist.** ⭐ *Die letzten elf Aufträge lagen je an mehreren Stellen daneben — zuletzt TB-63, dessen Endanker ich falsch angegeben hatte* |

---

## In einfacher Sprache

**Was schiefsteht:** Das Dokument, nach dem ich arbeite, ist über eine Woche auf
fast 71 000 Zeichen gewachsen, und die Regeln dafür, wie eine Antwort auszusehen
hat, stehen an fünf verschiedenen Stellen. **Das hat an einem einzigen Tag
viermal dazu geführt, dass ich eine Regel verletzt habe, die längst dastand.**

**Was diese Aufgabe macht:** Sie legt eine einzige Liste an, die vor jeder
Antwort gilt — kurz, zum Abhaken, mit Zeigern auf die Stellen, die es ausführlich
erklären.

**Worauf es dabei ankommt:** Dass keine Regel verlorengeht. Deshalb wird vorher
jede einzelne aufgeschrieben und hinterher nachgewiesen, dass sie noch da ist.
Was absichtlich wegfällt, wird einzeln genannt — nie stillschweigend.

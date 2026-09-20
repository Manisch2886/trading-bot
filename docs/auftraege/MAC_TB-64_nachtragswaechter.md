# TB-64 Der Wächter für die Bringschuld der Nachträge — an: Claude Code am Mac (lokale Sitzung)

**Sitzungstitel für Claude Code: `TB-64 Nachtragswaechter`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main` — kein Zweig, kein PR.

⭐ **Unabhängig von TB-61, TB-62 und TB-63.** Diese Aufgabe fasst `BACKLOG.md`,
`JOURNAL.md` und `ARBEITSWEISE.md` **nicht an** — sie liest sie nur.
⚠️ **Trotzdem nicht gleichzeitig mit einer anderen Sitzung laufen lassen.**

⭐ **Rechnet nicht** im Sinne von Kursdaten, braucht aber `trading-env` für den
Test.

---

## 0. Warum es diese Aufgabe gibt — gemessen am 20.09.2026 an `4b85f0e`

**`docs/projektfuehrung/nachtraege/` enthält 26 Dateien, 284 KB** — 19
Backlog-Nachträge, 7 Journal-Nachträge. Das ist ein Zwischenlager, das nie
geleert wird.

⚠️⚠️ **Der Weg ist zweistufig, und Stufe zwei kann ausfallen, ohne dass es
jemand merkt:**

> Nachtrag schreiben → **irgendwann** einarbeiten

**Gemessen, was heute offen ist — und keines davon war irgendwo als offen
geführt:**

| Nachtrag | Befund |
|---|---|
| `BACKLOG_NACHTRAG_2026-09-19m.md` | ⚠️⚠️ **nie eingearbeitet**, seine sechs Nummern `K2l`–`K2q` sind im Backlog an **andere Inhalte** vergeben. Zwei seiner Regeln stehen **nirgends im Repo** |
| `BACKLOG_NACHTRAG_2026-09-19v.md` | nicht eingearbeitet (⇒ TB-62) |
| `JOURNAL_NACHTRAG_2026-09-19g.md` | ⛔ **nicht im Journal** |
| `JOURNAL_NACHTRAG_2026-09-20a.md` | ⛔ **nicht im Journal** |
| `JOURNAL_NACHTRAG_2026-09-20b.md` | ⛔ **nicht im Journal** |
| `JOURNAL_NACHTRAG_2026-09-19f.md` | ⚠️ **nicht prüfbar** — sein Titel nennt keine TB-Nummer *(A2: nicht grün, nicht rot)* |

⭐⭐ **Der Fall (m) ist der Grund für diese Aufgabe.** Er wurde übersprungen,
seine Nummern wurden an andere Inhalte vergeben, und aufgefallen ist es **zwei
Tage später durch Zufall** — beim Messen für eine andere Aufgabe.

> ⚠️ **Die bitterste seiner zwei verlorenen Regeln lautet:** *„Jede Rückfrage an
> den Betreiber und seine Antwort kommen wörtlich in den Bericht — sonst leben
> sie nur im Sitzungsverlauf, der mit der Sitzung verschwindet."*
>
> ⭐⭐ **Eine Regel, die verhindern soll, dass Regeln verlorengehen, ist selbst
> verlorengegangen.**

⇒ **Die einzige Wache dagegen ist heute, dass jemand daran denkt.** Das ist
keine.

---

## 1. Was gebaut wird

**`system/nachtragswaechter.py`** — rein lesend, meldet, ändert nichts.

### Der Zustand wird durch den Ort ausgedrückt

⭐ **Ein eingearbeiteter Nachtrag wird nach
`docs/projektfuehrung/nachtraege/_eingearbeitet/` verschoben.** Was im
Hauptverzeichnis liegt, ist offen.

*Dasselbe Muster wie `logs/auftraege/_erledigt/`, das sich bewährt hat.*

⚠️ **Der Ort allein genügt nicht** — jemand könnte verschieben, ohne
einzuarbeiten. **Deshalb prüft der Wächter beides:**

| | Prüfung | Gegenstand |
|---|---|---|
| **A** | **Was liegt offen?** | Dateien im Hauptverzeichnis, mit Alter in Tagen |
| **B** | **Ist von den verschobenen wirklich alles angekommen?** | Stichprobe über die Nummern jeder Datei in `_eingearbeitet/` |

⭐⭐ **Prüfung B ist die eigentliche Wache.** Ohne sie wäre das Verschieben eine
Selbstauskunft — und nach Backlog `Q2` wiegt eine Prüfung durch jemanden, der
die Arbeit nicht gemacht hat, mehr als ein Selbstbericht.

### Die Prüfregeln im Einzelnen

**Für `BACKLOG_NACHTRAG_*.md`:**

Jede Nummer der Form `^\| \*\*(K\d[a-z])\*\*` **gilt als angekommen**, wenn sie
in `BACKLOG.md` oder `BACKLOG_ARCHIV.md`

- als Zeile derselben Form steht, **oder**
- dort als *„als `X` vorgeschlagen"* vermerkt ist (verworfene Nummer, TB-59-Form).

⚠️⚠️ **Das Muster hat KEINEN schliessenden Balken.** Im Backlog steht
`| **K2p** *(im Nachtrag (n) als ...)* |`; ein Muster mit `\|` am Ende übersieht
jede Zeile mit Vergabevermerk. **Am 20.09.2026 hat genau das eine Zählung von
64 auf 43 verfälscht.**

⛔ **Und kein `sort -u` in der Prüfung** — es entfernt genau die Duplikate, die
sie finden soll. *Dieser Fehler hat am 20.09. gemeldet, es gebe keine
Doppelbelegung; es gibt zwei (`K1o`, `K1q`).*

⭐ Dasselbe für **Blockbezeichner** `^## (2[a-z])` und **Kettenzeilen**.

**Für `JOURNAL_NACHTRAG_*.md`:**

⚠️ **Hier gibt es heute keine belastbare Kennung** — (f) ist deshalb nicht
prüfbar. **Der Auftrag führt eine ein:**

> ⭐ **Jeder Journalblock, der aus einem Nachtrag entstanden ist, nennt seine
> Quelldatei in einer Zeile der Form:**
>
> `*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_<datum><buchstabe>.md`*`

**Der Wächter prüft, ob die Quelldatei im Journal genannt ist.**

⚠️ **Die drei bereits eingearbeiteten (c), (d), (e) tragen diesen Vermerk
nicht.** ⇒ **Trage ihn nach**, wenn du ihre Blöcke im Journal eindeutig
zuordnen kannst; **kannst du es nicht, melde sie als „nicht prüfbar" (A2) und
lass das Journal unberührt.** ⛔ **Nichts erraten.**

---

## 2. Was der Wächter ausgibt

**Bei Befund** Rückgabewert **1** und eine Meldung über
`shared/telegram_*` bzw. den Weg, den die anderen vier Cron-Wächter benutzen —
**sieh nach, wie `ergebniskurven.py --nur-abweichung` es macht, und mach es
genauso.**

**Ohne Befund** Rückgabewert **0** und keine Meldung.

⭐ **Die Meldung nennt je offenem Nachtrag:** Dateiname, Alter in Tagen, Zahl
der nicht angekommenen Nummern.

⚠️ **Und sie nennt die nicht prüfbaren getrennt** — *nicht grün, nicht rot*
(Prüfprinzip **A2**).

---

## 3. ⭐⭐ Die Mutationsprobe — ohne sie ist der Wächter keiner

**Prüfprinzip `B1` und `K3g`: Jede Probe wird an einem bekannt kaputten
Gegenstand validiert, bevor sie an einen echten darf.**

`system/test_nachtragswaechter.py` legt in einem **Wegwerf-Verzeichnis** an:

| Fall | erwartet |
|---|---|
| **1** | Ein Nachtrag mit einer Nummer, die im Ziel steht | ⇒ **kein Befund** |
| **2** | Ein Nachtrag mit einer Nummer, die **nicht** im Ziel steht | ⇒ **Befund**, Rückgabewert 1 |
| **3** | Eine Nummer, die im Ziel **nur als Vergabevermerk** steht (`als \`K2r\` vorgeschlagen`) | ⇒ **kein Befund** |
| **4** | ⭐⭐ Eine Zielzeile **mit** Vergabevermerk (`| **K2p** *(…)* |`) | ⇒ **kein Befund** — *das ist der Fall, an dem das Muster am 20.09. gescheitert ist* |
| **5** | ⭐⭐ Zwei gleiche Nummern im Ziel | ⇒ **Befund „Doppelbelegung"** — *der Fall, den `sort -u` verschluckt hat* |
| **6** | Ein Journal-Nachtrag ohne Quellenvermerk im Journal | ⇒ **Befund** |
| **7** | Eine Datei in `_eingearbeitet/`, deren Nummern **nicht** im Ziel stehen | ⇒ **Befund** — *Prüfung B, die Wache gegen falsches Verschieben* |

⛔ **Fällt einer dieser sieben Fälle nicht wie erwartet aus, ist der Wächter
nicht fertig.** Melde welcher und warum.

⚠️ **Das Wegwerf-Verzeichnis liegt NICHT unter `docs/`** und wird am Ende
entfernt. *Am 20.09. hat ein Testlauf unbemerkt eine Datei im Projektordner
angelegt (T42.7) — prüfe am Ende mit `git status --short`, dass nichts
übrigblieb.*

---

## 4. Die Schritte

### Schritt 0 — vor allem anderen

**Committe, was im Arbeitsbaum liegt.** Nachweis „sauber" wird **danach**
geprüft.

### Schritt 1 — messen, was heute offen ist

**Bevor du etwas baust:** Zähle für jede der 26 Nachtragsdateien, wie viele
ihrer Nummern im Ziel angekommen sind. **Halte das Ergebnis gegen die Tabelle
in Abschnitt 0.**

⚠️ **Weicht es ab, gilt deine Messung** — Abschnitt 0 ist der Stand von
`4b85f0e`, und TB-62 könnte inzwischen gelaufen sein.

**Sichern: commit und push.**

### Schritt 2 — `_eingearbeitet/` anlegen und die erledigten verschieben

⭐ **Nur die, deren Nummern du in Schritt 1 als angekommen gemessen hast.**
⛔ **Nichts verschieben, was du nicht geprüft hast.**

**Sichern: commit und push.**

### Schritt 3 — den Wächter und seinen Test bauen

**Sichern: commit und push.**

### Schritt 4 — den Quellenvermerk einführen

Die Form aus Abschnitt 1 in `DOKUMENTATIONSSTANDARD.md` eintragen, und bei den
Journalblöcken nachtragen, die du **eindeutig** zuordnen kannst.

**Sichern: commit und push.**

### Schritt 5 — die Cron-Zeile vorbereiten, nicht eintragen

⛔ **Du trägst nichts in die crontab ein.** Schreibe die fertige Zeile ins
Ergebnisdokument, zum Kopieren, nach dem Muster der vier bestehenden Wächter.
**Der Eintrag ist Betreiberarbeit.**

⚠️ **`crontab -l` wird nie ungefiltert ausgegeben** (`K2a`) — zulässig ist
`awk '{print $1,$2,$3,$4,$5}'` oder `grep -c`.

### ⭐⭐ Schritt 5b — die drei übrigen `B`-Zeilen nach `docs/UMGEBUNGEN.md`

⚠️⚠️ **Nachgetragen am 20.09.2026, 18:10, nach Betreiberentscheidung.**
TB-67 hat die sieben `B`-Zeilen aus Backlog-Nachtrag `(m)` einzeln geprüft
(Ergebnisdokument TB-67, Nachweis 6): **fünf stehen bereits** in einem
Führungsdokument, **drei nicht**. ⭐ **Der Betreiber hat entschieden: die drei
kommen nach `docs/UMGEBUNGEN.md`, in dieser Aufgabe.**

| | was fehlt | Stand laut TB-67 |
|---|---|---|
| **B2** | der **Messbefund**, dass die Cloud Python 3.10–3.13 hat, **kein 3.9, kein `pyenv`** ⇒ sie fällt als zweite Maschine für die Laufreproduktion aus | die **Folgerung** steht (`BACKLOG.md` Kettenzeile `0,99`; Übergabe Block 4 Punkt 6), der Befund nirgends — auch nicht in `UMGEBUNGEN.md` (0 Treffer für `3.13`, `pyenv`) |
| **B3** | die Probe, dass die **Sperre gegen den zweiten Snapshot auch im Wegwerf-Klon greift** (rc 2) | 0 Treffer in elf Führungsdokumenten; Register Abschnitt 20 beschreibt die Klon-Probe des **Locks**, nicht der Snapshot-Sperre |
| **B7** | der **`dist-info`-Weg**: Vorprüfung der Abhängigkeiten ohne Ausführung | die **Regel** steht als `K2b`, der **Weg** nirgends — 0 Treffer für `dist-info` in elf Dokumenten |

⛔ **Erfinde keine Formulierung.** ⭐ **Nimm den Wortlaut aus
`BACKLOG_NACHTRAG_2026-09-19m.md`, Block `2s`, Zeilen `B2`, `B3`, `B7`** und
kürze ihn nur, wo er auf den Sitzungsverlauf zeigt. **Jede der drei bekommt
die Quellenzeile**, die `TB-67` eingeführt hat, mit dem Backlog-Nachtrag als
Quelle.

⚠️ **Liegt `docs/UMGEBUNGEN.md` nicht vor oder passt keine der drei dorthin,
entscheide das nicht selbst** — benenne den Ort, den du für richtig hältst,
und lege ihn vor (`A2`).

⭐ **Danach, und nur danach, gilt `(m)` als eingearbeitet** und darf nach
`nachtraege/_eingearbeitet/` — TB-67 hat es ausdrücklich liegen lassen, weil
diese Entscheidung offen war.

**Sichern: commit und push.**

### Schritt 6 — die Abgabe

`docs/ERGEBNIS_TB-64_nachtragswaechter.md` und ein Journal-Nachtrag
⭐ **mit dem neuen Quellenvermerk**.

**Sichern: commit und push.**

---

## 5. Die Nachweise

| # | Nachweis |
|---:|---|
| **1** | `git status --short` **vor** dem ersten Schreiben |
| **2** | ⭐ **Die sieben Mutationsfälle aus Abschnitt 3, einzeln, mit Ergebnis** |
| **3** | Der Lauf gegen den echten Bestand: welche Nachträge offen, welche nicht prüfbar, mit Alter |
| **4** | Was nach `_eingearbeitet/` verschoben wurde, und je Datei die Zahl der geprüften Nummern |
| **5** | `git diff --numstat` je Datei |
| **6** | Die Cron-Zeile, fertig zum Kopieren |
| **7** | `git status --short` **nach** dem Testlauf — erwartet **leer** (kein Wegwerf-Rest) |
| **8** | Nichts ausserhalb `system/`, `docs/` geändert |

---

## 6. Die harten Auflagen

| | |
|---|---|
| ⛔ | **Der Wächter ändert nie etwas.** Rein lesend, er meldet |
| ⛔ | **Kein crontab-Eintrag durch die Sitzung** |
| ⛔ | **Nichts verschieben, was nicht geprüft ist** |
| ⚠️ | **Muster ohne schliessenden Balken, kein `sort -u`** — Abschnitt 1 |
| ⭐ | **Sichern nach jedem fertigen Teil** — sechs Commits oben benannt |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block** |
| ⚠️ | **Widersprich diesem Auftrag, wo er falsch ist.** Er beruht auf `4b85f0e` |

---

## 7. Was diese Aufgabe NICHT tut

| | |
|---|---|
| ⛔ | **Nachträge einarbeiten.** Das ist TB-62 und die Aufgaben danach. Dieser Wächter **meldet nur** |
| ⛔ | **`BACKLOG.md`, `JOURNAL.md` oder `ARBEITSWEISE.md` inhaltlich ändern** — ausser dem Quellenvermerk aus Schritt 4 |
| ⛔ | **Journalblöcke raten.** Unklare Zuordnung ⇒ *nicht prüfbar*, und das steht dann so da |

---

## In einfacher Sprache

**Was schiefgelaufen ist:** Notizen werden zuerst in eine Extra-Datei
geschrieben und später in die Aufgabenliste übertragen. Der zweite Schritt kann
ausfallen, und niemand merkt es. Eine Notiz vom 19. ist so durchgerutscht —
aufgefallen ist es erst zwei Tage später, zufällig. **Zwei Regeln daraus stehen
bis heute nirgends im Projekt**, darunter ausgerechnet die, dass deine
Rückfragen und Antworten in den Bericht gehören, damit sie nicht nur im Chat
leben.

**Was diese Aufgabe baut:** Ein kleines Prüfprogramm, das jeden Tag nachsieht,
welche Notiz noch nicht übertragen ist, und dir eine Nachricht schickt, wenn
eine zu lange liegt. Erledigte Notizen wandern in einen Unterordner — was oben
liegt, ist offen.

**Warum es sieben Testfälle hat:** Damit das Prüfprogramm nicht selbst blind
ist. Zwei der sieben sind genau die Fehler, die mir heute passiert sind — ein
Suchmuster, das eine Zeilenform übersieht, und ein Befehl, der die gesuchten
Doppelungen vorher wegräumt. **Ein Prüfer, der nichts findet, weil er nicht
hinsehen kann, ist schlimmer als keiner.**

**Was du am Ende tust:** Eine fertige Zeile in deine Cron-Liste eintragen. Die
Sitzung macht das nicht selbst.

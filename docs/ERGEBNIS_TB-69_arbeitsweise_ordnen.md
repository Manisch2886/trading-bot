# ERGEBNIS TB-69 — Die Ausgaberegeln an einer Stelle: Abschnitt 0 in `ARBEITSWEISE.md` (Mac-Sitzung, 21.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-69_arbeitsweise_ordnen.md`. **Ausgeführt am
MacBook**, Zweig `main`, Ausgang `3c25d94` (= `origin/main` beim Start, TB-76
erledigt). Geändert nur `docs/`: `docs/projektfuehrung/ARBEITSWEISE.md` (nur
Zusätze), dieses Dokument, ein Journalblock, eine Backlog-Zeile, Belege unter
`docs/belege/TB-69/`. Sitzung ab 13:38 Ortszeit; Commits `495b7fc` und
`5a1f5e1` (Schritt 0, drei Dateien des Betreibers), `067e473` (Schritt 1),
`dfc4422` (Schritt 2), `3b74651` (Schritt 3), `50e3da7` (Schritt 4) und der
Abgabe-Commit. ⭐ **Rechnet nicht** — kein Bot, kein Test, kein Interpreter.

*In einfacher Sprache, zu Beginn:* Das Regelwerk, nach dem der steuernde Chat
arbeitet, war auf 71 000 Zeichen gewachsen, und die Regeln dafür, wie eine
Antwort auszusehen hat, standen an fünf Stellen — an einem Tag viermal
verletzt, obwohl jede Regel dastand. Jetzt steht ganz vorn eine Liste zum
Abhaken, 65 Zeilen, jede mit dem Fingerzeig auf den Abschnitt, der sie erklärt.
Nichts wurde gelöscht, nichts umgeschrieben; das ist nachgewiesen, Zeile für
Zeile.

---

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

Beim Sitzungsstart, 13:38, `HEAD` = `3c25d94`:

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
?? docs/auftraege/MAC_TB-69_arbeitsweise_ordnen.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-09-21a_horizont_und_grenzfall.md
```

Drei Dateien des Betreibers (mtime 13:07, 13:07, 13:34), nach Schritt 0 in
zwei Commits gesichert — `495b7fc` (Auftrag und Zeiger) und `5a1f5e1` (die
Fable-Anfrage, getrennt, weil sie nicht zu TB-69 gehört); Secrets-Probe je 0
Treffer. Danach `git status --short` = nur `?? docs/belege/TB-69/`
(`nachweis1_status_vor_schreiben.txt`). ⭐ **`5a1f5e1` ist damit der Stand,
gegen den alle Nachweise dieses Auftrags messen.**

## Nachweis 2 — ⭐⭐ Die Regelliste vorher (`regelliste_vorher.md`)

Das ganze Dokument (70 905 B, 1 293 Zeilen, 25 Abschnitte, 15
Unterabschnitte) von oben nach unten gelesen; jede Vorschrift eine Zeile mit
Nummer, Abschnitt und Zeilenbereich, Kern in einem Satz, Betrifft (**A** =
Ausgabe einer Antwort, **S** = anderes) und Lage.

| | Zahl |
|---|---:|
| ⭐ **Regeln gesamt (SOLL für Schritt 4)** | **117** |
| davon A — betreffen die Ausgabe einer Antwort | **76** |
| davon S — Verfahren, Sachstand, Dokumentationsführung, Abnahme | 41 |

Ausdrücklich **nicht** als Regel gezählt und wörtlich stehen geblieben:
Änderungsvermerke, Berichtigungen, Messungen, Anlässe, Zitate,
Kostentabellen, der offene Punkt P1, die Sperrlisten-Tabelle (Sachstand).
Fünf Nebenbefunde N1–N5 beim Lesen notiert (unten unter „Offen“).

## Nachweis 3 — ⭐⭐ Die Wiederfind-Prüfung (`regelliste_nachher.md`)

Dieselben 117 Nummern, je mit neuem Ort im Text und — für die 76 A-Regeln —
der Zeile in Abschnitt 0, die sie abhakt.

| | Ergebnis |
|---|---|
| ⭐ **wiedergefunden** | **117 von 117, 0 fehlen** |
| Checklistenzeilen | 65 — **alle 65 von A-Regeln belegt**, keine A-Regel ohne Zeile, keine Zeile ohne Regel |
| Ort im Text | derselbe Abschnitt wie vorher; Zeilen um den gemessenen Versatz verschoben (+0 / +3 / +133 / +135 an den zwei Hunk-Grenzen), Stichproben 6bb, 14 Regel 0, 17 gegen die Datei geprüft |
| zeichengleich | `git diff --numstat 5a1f5e1 HEAD` = **135 / 0**; genau zwei Hunks (`@@ -20,6 +20,139 @@`, `@@ -665,6 +798,8 @@`); Teilfolgenprobe: **1 293 / 1 293** alte Zeilen in Reihenfolge byteweise wiedergefunden (`schritt4_teilfolge.txt`) |

Wo eine Checklistenzeile mehrere Nummern trägt, sind es Facetten derselben
Vorschrift (z. B. „Schritt für Schritt“ + „auch wenn trivial“; Secrets +
„gilt für alle Zugänge“; die drei Startbefehl-Regeln aus 1 und 14). Die
Zuordnung steht je Nummer in der Tabelle.

## Nachweis 4 — Was gestrichen wurde

**Nichts. Ausdrücklich.** Keine Regel, keine Messung, kein Anlass, kein
Vermerk wurde entfernt oder gekürzt — 0 entfernte Zeilen. Auch das, was heute
überholt klingt, steht wörtlich (*„ZIP hat immer funktioniert“* in 2; *„der
erste Befehl jeder Mac-Sitzung ist `/login`“* in 14 Regel 0) — es sind
Messungen und Anlässe, und der Auftrag verlangt sie wörtlich.

## Nachweis 5 — Schritt 3: die Verweise, gemessen vor der Entscheidung (`schritt3_verweise_messung.txt`, `schritt3_entscheidung_umnummerieren.md`)

| Datei / Gruppe | Verweiszeilen |
|---|---:|
| `BACKLOG.md` / `BACKLOG_ARCHIV.md` / `BACKLOG_EPICS.md` | 10 / 16 / 0 |
| `DOKUMENTATIONSSTANDARD.md` / `UMZUG.md` / `UEBERGABE_*` | 3 / 4 / 5 |
| ⛔ **`JOURNAL.md`** (wird nie umgeschrieben) | **8** — u. a. §7, §11, Abschnitt 10, „14 Regel 3 und 15“, 14, 14 |
| Nachträge / Ergebnisdokumente / Aufträge | 31 / 35 / 20 |
| `ARBEITSWEISE.md` selbst | 37 |
| `logs/auftraege/` (gitignoriert) / Sonstige | 15 / 4 |
| **Summe** | **188 Zeilen in 57 Dateien**, 48 davon mit Buchstabenabschnitt |

Das Muster ist heuristisch (zählt in `ARBEITSWEISE.md` auch `UMZUG.md`-
Verweise mit, übersieht Nennungen ohne „Abschnitt“); die Zeilen stehen im
Beleg.

⭐ **Entscheidung: nicht umnummerieren.** Die sieben Buchstabenabschnitte
liegen zwischen 5 und 8; sie einzureihen verschöbe **jede** Nummer ab 6 (`6d`
→ 11, `14` → 21, `18` → 25) und träfe damit die meisten der 188 Zeilen. Acht
davon stehen in `JOURNAL.md`, das nach Abschnitt 5, Abschnitt 16 und
`DOKUMENTATIONSSTANDARD.md` Regel 9 nicht angefasst wird; weitere in der
Erinnerung des steuernden Chats (*„Block 7, Punkt 8“*), unter `logs/` (keine
Version) und in 86 abgeschlossenen Belegen, die gegen die damalige Fassung
gelaufen sind. Der Auftrag sagt es selbst: *„Ist ein Verweis dort nicht
nachziehbar, weil das Dokument unveränderlich ist, sag es — dann ist
Umnummerieren die falsche Wahl.“* Die Einordnung nach Lagen, die eine
Umnummerierung hätte leisten sollen, leistet Abschnitt 0 — und **0 vor 1
verschiebt nichts**. Kontrollmessung auf dem Endstand: ausserhalb
`ARBEITSWEISE.md` und der TB-69-Belege alle Zeilenzahlen je Datei identisch
(`diff` leer); `ARBEITSWEISE.md` 37 → 38 (der Vorspann von Abschnitt 0 nennt
6d als Anlass).

## Nachweis 6 — Verweise nachgezogen

**Entfällt** — nicht umnummeriert, kein Verweis gewandert, Trefferzahlen je
Datei vorher = nachher (Nachweis 5, Kontrollmessung).

## Nachweis 7 — `git diff --numstat` je Datei, nichts ausserhalb `docs/`

Gegen `5a1f5e1`, vor dem Abgabe-Commit (`nachweis7_numstat.txt` trägt den
Stand mit den Abgabedateien, ohne sich selbst):

| Datei | + | − |
|---|---:|---:|
| `docs/projektfuehrung/ARBEITSWEISE.md` | 135 | **0** |
| `docs/belege/TB-69/regelliste_vorher.md` | 149 | 0 |
| `docs/belege/TB-69/regelliste_nachher.md` | 167 | 0 |
| `docs/belege/TB-69/schritt3_entscheidung_umnummerieren.md` | 47 | 0 |
| `docs/belege/TB-69/schritt3_verweise_messung.py` / `.txt` / `schritt3_verweise_kontrolle.txt` | 32 / 249 / 61 | 0 |
| `docs/belege/TB-69/schritt0_status.txt`, `nachweis1_status_vor_schreiben.txt`, `schritt2_numstat.txt`, `schritt4_numstat_gegen_5a1f5e1.txt`, `schritt4_teilfolge.txt` | 5 / 1 / 1 / 1 / 2 | 0 |
| Abgabe: dieses Dokument, `JOURNAL.md` (Block `CE`), `BACKLOG.md` (Zeile `K4q`) | nur Zusätze | 0 |
| **ausserhalb `docs/`** | **0 Dateien** | |

## Nachweis 8 — Grösse vorher und nachher

| | Bytes | Zeilen |
|---|---:|---:|
| vorher (`5a1f5e1`) | 70 905 | 1 293 |
| nachher | **80 018** | 1 428 |
| Zuwachs | +9 113 | +135 |
| ⭐ davon **Abschnitt 0 (Checkliste)** | **8 835 (97 %)** | 130 |
| davon zwei Vermerke (Kopf 213 B, 6d 65 B) | 278 (3 %) | 5 |

## Was gebaut wurde: Abschnitt 0

**Wo und warum dort:** ganz vorn, direkt nach dem Fassungskasten, als `## 0`.
Vorn, weil vorn gelesen wird — das Ende eines 80-KB-Dokuments erreicht keine
Antwort; 0, weil keine bestehende Nummer und kein Verweis wandert. Die
Alternative „ganz hinten als 19“ hätte den Anlass (6d: *„verstreute Regeln
werden beim Schreiben nicht gelesen, sondern erinnert“*) nur verschoben.

**Form:** elf Lagen — immer · Aufgabenbeginn · Antwortende · Dokument mitgeht
· Abschnittsende/Verlust · Entscheidung · Anleitung · Terminal · Mac-Sitzung
Start/Ende/Abbruch · Bewertung · Auftrag — je eine kleine Tabelle
`☐ | Regel | steht in`. **Keine Erklärung, keine Messung, kein Anlass** in
der Liste; ein fünfzeiliger Vorspann sagt nur, wozu sie da ist. Die
ausführenden Abschnitte 1–18 sind zeichengleich geblieben.

**Zwei Zusätze ausserhalb der Liste, ehrlich benannt** (der Auftrag sagt *„neu
ist nur die Checkliste“*): ein dreizeiliger Vermerk im Fassungskasten (nach
dem Muster der Vermerke vom 18.09. und 20.09.) und der Einzeiler *„Erledigt
21.09.2026 (TB-69): die Liste ist Abschnitt 0“* in 6d — ohne ihn beschriebe
6d weiter einen Zustand, der seit heute nicht mehr gilt. Beide sind keine
Regeln; beide sind mit zwei Zeilen entfernbar, die Liste hängt nicht daran.

## Abweichungen vom Auftrag

| | Auftrag | getan | warum |
|---|---|---|---|
| 1 | „Was neu ist, ist nur die Checkliste selbst“ | Checkliste **plus** zwei Änderungsvermerke (278 B) | Regel 9 des Dokumentationsstandards: eine Änderung sagt, was sie ablöst — 6d sagte sonst weiter, es gebe keine Liste |
| 2 | Abschnitt 0 des Auftrags: „6d, der die Form nicht nannte“ | 6d nennt die Form seit 20.09. im Unterabschnitt *„Die Form: anklickbare Multiple-Choice-Frage“* — der Verstoss 5 (17:58) war der **Anlass** dieses Unterabschnitts, nicht ein Verstoss gegen ihn | nur Lesart; die Regel steht heute da, R61 |
| 3 | Schritt 3: „Ordne sie ein und nummeriere durch — oder lass es, begründet“ | gelassen, begründet mit Messung (Nachweis 5) | acht nicht nachziehbare Verweise in `JOURNAL.md` |
| 4 | Nachweis 6 | entfällt | folgt aus 3 |
| 5 | Auftragstabelle in Abschnitt 0 des Auftrags zählt „viermal verletzt“ und listet sechs Zeilen (1–3, 4, 5, 6) | so übernommen; die Zählung „vier“ meint die Familie Empfehlung/Form (1–3 und 5), 4 und 6 sind die Kopierblock- und die Editor-Familie | keine Änderung, nur damit die Zahl nicht als Widerspruch gelesen wird |

## Fehler → Regel

| | |
|---|---|
| ⭐ | **Eine Umordnung wird erst gegen die Verweise gemessen, dann entschieden** — 188 Zeilen in 57 Dateien, acht davon unveränderlich, haben die Frage beantwortet, bevor eine Nummer angefasst war |
| ⭐ | **„Nichts verloren“ wird an drei Stellen gezeigt, nicht an einer:** `numstat` 135/0 (keine Zeile weg), Hunk-Zahl 2 (keine dritte Stelle), Teilfolge 1 293/1 293 (jede alte Zeile in Reihenfolge da). Jede der drei sieht etwas, das die anderen nicht sehen |
| ⭐ | **Die Liste vorher ist der Massstab, nicht die Erinnerung an das Dokument** — 117 Zeilen, die vor dem ersten Eingriff festlagen. Ohne sie wäre „nichts verloren“ ein Gefühl |
| | Eine Regel mit vier Facetten wird eine Checklistenzeile, aber vier Nummern in der Zuordnung — die Liste bleibt kurz, der Nachweis bleibt vollständig |

## ⚠️ Offen — nicht Teil dieses Auftrags

1. ⭐⭐ **Die Projektablage ist nachzuziehen** (`K4e`: *wer ein Führungsdokument committet, lädt es im selben Zug in die Projektablage*). `ARBEITSWEISE.md` ist ein Führungsdokument und hat sich geändert (80 018 B, `## 0`). **Der steuernde Chat tut das** — diese Sitzung hat keinen Zugang zur Ablage.
2. **Die Erinnerung des steuernden Chats** kennt Abschnitt 0 noch nicht; die Träger-Tabelle in Abschnitt 15 nennt die Erinnerung als den einen Träger, der ohne Zutun wirkt.
3. **Nebenbefunde beim Lesen, nicht behoben** (`regelliste_vorher.md`, N1–N5): 14 Regel 0 nennt `/login` einmal als ersten Befehl und vier Zeilen später als letzten Ausweg (N1); der Einfügesatz in 14 Regel 2 lautet anders als der gelebte in `AKTUELLER_AUFTRAG.md` (N2); *„ZIP hat immer funktioniert“* als Hintergrund unter dem ZIP-Verbot (N3); Abschnitt 5, vierter Punkt, verlangt „als Download“, 5b den Auftrag (N4); 14 Regel 4 verweist auf „Block 7, Punkt 8“ der Erinnerung (N5). Alles Kandidaten für Regel 9 — durch den steuernden Chat, nicht durch eine Sitzung mit der Auflage „wörtlich“.
4. **Ob die Liste wirkt, misst erst der nächste Tag**: der Anlass waren vier Verstösse an einem Tag bei vorhandener Regel. Die Probe ist ein Tag ohne.

## In einfacher Sprache

**Was wir wissen wollten:** Kann man die Regeln, wie eine Antwort auszusehen
hat, an eine einzige Stelle bringen — ohne dass dabei eine Regel
verlorengeht?

**Was herauskam:** Ja. Ganz vorn im Regelwerk steht jetzt eine Liste zum
Abhaken, 65 Zeilen, nach Situationen sortiert („wenn eine Entscheidung
ansteht“, „wenn ich den Betreiber anleite“ …), jede Zeile mit dem Hinweis, wo
die ausführliche Regel steht. Vorher wurden 117 Regeln aufgeschrieben,
nachher alle 117 wiedergefunden; keine einzige Zeile des alten Textes ist
weg oder anders.

**Warum das so ist:** Die Verstösse kamen nicht daher, dass Regeln fehlten,
sondern daher, dass es keine Stelle gab, die man vor dem Absenden durchgeht.
Das Regelwerk selbst hatte das schon festgestellt. Umnummeriert wurde nicht:
Das hätte Verweise in Dokumenten zerrissen, die nie mehr geändert werden.

**Was das für dich heisst:** Die neue Fassung liegt im Repo; du lädst sie in
die Projektablage (das kann diese Sitzung nicht). Und ob die Liste hält, was
sie soll, zeigt der nächste Arbeitstag — ein Tag ohne einen der vier Verstösse
vom 20.09.

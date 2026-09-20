# Journal-Nachtrag (g) — 20.09.2026, TB-67: das Journal zieht nach — zehn Blöcke, die Quellenzeile, und ein Auftrag, der an zwei Stellen danebenlag

**Quelle:** Mac-Sitzung **TB-67 Journal nachziehen**, 20.09.2026, ab etwa 17:35
Ortszeit, Ausgang `fe76857`, reine Dokumentation (Interpreter nur `python3` für
Zählskripte, keine Kursdaten, nichts ausserhalb `docs/`). Commits `481b9f7`
(Schritt 0), `cc72150` (Messung), `08cf90a` (Journal +965/0), `31bc953`
(Nachweise), `93a88d4` (Backlog `K4h`), `4117ee7` (Verschieben) und der
Abgabe-Commit. Ergebnisdokument `docs/ERGEBNIS_TB-67_journal_einarbeitung.md`,
Belege `docs/belege/TB-67/`. **Einzuarbeiten als nächster Block nach dem
höchsten vorhandenen** (am 20.09.2026 gemessen: `BT`; die Nummer vergibt die
einarbeitende Sitzung).

⭐ **Quellenzeile für den Block, wörtlich zu übernehmen:**

```
*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-20g.md`*
```

---

## Was der Auftrag wollte und was er bekam

Den Journal-Rückstand abarbeiten: sechs offene Nachträge einarbeiten, drei
Aufgaben ohne Journalblock (TB-53b, TB-58, TB-58b) aus dem Rückblick-Block `2s`
in Backlog-Nachtrag `(m)` versorgen, jedem Block eine Quellenzeile geben, die
sieben `B`-Zeilen aus `(m)` prüfen und nicht eintragen, eine Backlog-Zeile, die
eingearbeiteten Dateien verschieben.

**Bekommen hat er alles davon — mit anderen Zahlen:** **acht** offene Nachträge
statt sechs (`(f)` war prüfbar und offen, `(20f)` aus TB-66 war jünger als der
Auftrag), **zehn** Blöcke `BK`–`BT`, **14** Quellenzeilen (10 neu, 4 bei
`BG`–`BJ` nachgetragen, 0 nicht zuordenbar), `JOURNAL.md` **6 526 → 7 491 Zeilen**
bei **0 entfernten**, `K4h` im Backlog, **elf** Dateien nach
`nachtraege/_eingearbeitet/` (Ordner neu angelegt). **Nicht prüfbar: keiner.**

---

## Drei Befunde

### 1. „Nicht prüfbar" war ein Befund über das Instrument, nicht über die Datei

Der Auftrag führte `(f)` als *nicht prüfbar*, weil sein Titel keine TB-Nummer
trägt. Das Nummernmuster ist aber nur eines von zwei Mustern, die der Auftrag
selbst vorschreibt; das zweite — ein charakteristischer Satz, wörtlich gesucht
— trifft `(f)` so gut wie jeden anderen Nachtrag, und es lieferte mit vier
Sätzen viermal 0. Dazu tragen die Blocküberschriften *in* `(f)` die Nummern
TB-53b, TB-58, TB-58b, alle drei ohne Journal-Kopfzeile.

⇒ ⭐ **A2 gilt für die Sache, nicht für das erste Instrument.** *Nicht prüfbar*
ist ein Nachtrag erst, wenn **jedes** vorgesehene Muster versagt. Ein Instrument,
das den Suchraum nicht abdeckt (`K4a`-Familie), macht die Datei nicht
unprüfbar, sondern das Instrument unzuständig.

### 2. Die drei fehlenden Blöcke gab es schon — als Notiz neben dem Journal

Schritt 3 verlangte, drei Blöcke *aus den 20 Zeilen des Blocks `2s` in `(m)`*
zu bauen. `(f)` — am selben Abend um 19:48 geschrieben wie `(m)` — **ist** die
Journalfassung dieser drei Blöcke, mit denselben Zahlen (71/19, 0 von 90,
`96a5c572…`, N1/N3/N4, 44/44, 160/0). Zwei Träger, ein Inhalt, und der Auftrag
kannte nur den einen, weil `(f)` ohne Kennung war.

Gelöst, ohne zu verdoppeln: die drei Blöcke einmal aus `(f)`, darunter je eine
Tabelle mit den `T`-Zeilen aus `(m)` **zeichengleich** (13/13, weil `(f)` etwa
`T58.2` — Fables drei Fälle — ganz und `T53.3` in den Zahlen weglässt), und
**zwei Quellenzeilen**: `*Quelle: …(f)*` und `*Messprotokoll: …(m), Block 2s*`.
Die zweite ist absichtlich anders benannt, damit ein Wächter, der
`JOURNAL_NACHTRAG_`-Quellen zählt, keinen Backlog-Nachtrag mitzählt.

⇒ ⭐ **Wer einen Nachtrag einarbeitet, sucht zuerst seinen Zwilling.** Zwei
Notizen aus derselben Stunde zum selben Gegenstand sind die Regel, nicht die
Ausnahme — hier `(f)` und `(m)`, gestern `(c)` und die Übergabe.

### 3. Die sieben `B`-Zeilen: fünf stehen, eine halb, eine gar nicht

Je Zeile mit zwei bis drei Begriffen über elf Führungsdokumente gesucht,
Fundstellen mit Zeilennummer im Ergebnisdokument (Nachweis 6): **B1, B4, B5,
B6 und die Regel aus B7 stehen** (Übergabe Block 7, `ARBEITSWEISE.md` 14 Regel
0, `K2b`, `K4g`, `0,99`). **B2 halb:** die Folgerung *„Cloud fällt für die
Laufreproduktion aus"* steht in `0,99` — und verweist mit „(B2)" auf eine
Zeile, die bis heute nur in `(m)` existierte; der Messbefund selbst (3.10–3.13,
kein 3.9, kein `pyenv`) steht nirgends, auch nicht in `UMGEBUNGEN.md`. **B3 gar
nicht:** dass die Snapshot-Sperre im Wegwerf-Klon greift, nennt kein
Führungsdokument; das Register beschreibt die Klon-Probe des Locks, nicht die
der Sperre. **Nichts davon eingetragen** — Betreiberentscheidung.

⇒ *Ein Verweis „(B2)" in einem Führungsdokument auf eine Zeile, die nur in einer
Notiz existiert, ist ein toter Verweis mit lebendem Namen.* Erst seit heute
zeigt er auf etwas im Journal (`BM`, verkürzt).

---

## Zwei Dinge zur Form

**Der Push war in dieser Umgebung gesperrt.** Der Berechtigungsfilter der
Claude-Code-Sitzung lehnte `git push` ab; sechs Commits liegen lokal auf `main`.
Die Auflage *„Sichern nach jedem fertigen Teil"* ist zur Hälfte erfüllt — die
Commits sind gesetzt, die Sicherung auf den zweiten Rechner nicht. **Das steht
im Ergebnisdokument oben, nicht unten**, damit der Betreiber es zuerst liest.

**Die Ankunft ist je Zeile gemessen, nicht je Datei.** `ankunft_pruefung.py`
hält jede nichtleere Zeile jedes Nachtrags gegen das Journal (Überschriften um
eine Stufe abgesenkt); die einzigen fehlenden Zeilen sind die
Einfüge-Anweisungen an den Einarbeiter (*„Anzufügen am Ende … Blockbuchstaben
messen"*), benannt und gezählt (7/4/3/4). Der Lauf ist zweimal abgelegt — vor
und nach dem Verschieben.

---

## Was aus dieser Sitzung an Regeln bleibt

| | Regel |
|---|---|
| ⭐⭐ | **„Nicht prüfbar" ist erst, wenn jedes vorgesehene Muster versagt.** Ein Muster, das den Suchraum nicht abdeckt, disqualifiziert das Muster, nicht die Datei |
| ⭐⭐ | **Jeder Journalblock, der aus einem Nachtrag entsteht, nennt seine Quelldatei in der ersten Zeile unter der Kopfzeile** — `*Quelle: …*` für Journal-Nachträge, `*Messprotokoll: …*` für zeichengleich übernommene Tabellen aus Backlog-Nachträgen |
| ⭐ | **Vor dem Bauen den Zwilling suchen:** zwei Notizen aus derselben Stunde zum selben Gegenstand werden einmal eingearbeitet, mit beiden Quellen |
| ⭐ | **Ankunft je Zeile messen**, nicht je Nummer — Nummern sehen nur, was Nummern trägt (`K4a`) |
| | Neue Journalblöcke stehen vor `## Wiederkehrende Lehren`; „am Ende anfügen" meint das Ende der Blockfolge. Das Inhaltsverzeichnis am Kopf bleibt bei `AG` (`K1p`) |

*Nachgetragen 20.09.2026 aus der Mac-Sitzung TB-67. Quellenvermerk: siehe Kopf.*

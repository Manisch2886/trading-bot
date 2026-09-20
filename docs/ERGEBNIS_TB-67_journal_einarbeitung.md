# ERGEBNIS TB-67 — Die Journal-Seite nachgezogen (Mac-Sitzung, 20.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-67_journal_einarbeitung.md`. **Ausgeführt am
MacBook**, Zweig `main`, Ausgang `fe76857` (= `origin/main` beim Start), **reine
Dokumentation** — kein Interpreter ausser `python3` für Zählskripte, keine
Kursdaten, nichts ausserhalb `docs/`. Dieses Dokument wächst mit jedem Schritt
und wird je Schritt committet; die Commit-Liste steht am Ende.

*In einfacher Sprache, zu Beginn:* Acht Notizdateien, die seit dem 19.09. neben
dem Journal lagen, werden in das Journal übertragen, jeder neue Eintrag sagt,
aus welcher Notiz er stammt, und die vier schon übertragenen Notizen bekommen
diese Zeile nachträglich.

---

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

Beim Sitzungsstart (vor Schritt 0), wörtlich:

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20b_wortlaut_nulltage.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20c_kapitalpfad.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-09-20b_kalender.md
```

Vier Betreiber-Dateien, keine davon aus dieser Sitzung. **Schritt 0:** unverändert
committet als `481b9f7` (der Fall von `K2p`, wie in TB-62 gehandhabt). Danach
`git status --short`: **0 Zeilen** — erst dann wurde geschrieben.

⚠️ **Zum Push:** Der erste `git push` nach Schritt 0 (in einer Pipe mit
`| tail`) wurde vom Berechtigungsfilter der Claude-Code-Umgebung abgelehnt
(*„denied by the Claude Code auto mode classifier"*). Ein nacktes `git push`
nach dem Abgabe-Commit ging durch: **`fe76857..544b011 main -> main`**, alle
sieben Commits auf `origin/main`. Abweichung von der Auflage *„commit und push
je Schritt"*: die Commits sind je Schritt gesetzt, gepusht wurde **einmal am
Ende** statt sechsmal. *(Nachgetragen im Abschluss-Commit, weil der Push erst
danach gelang.)*

---

## Nachweis 2 — Schritt 1: welche Journal-Nachträge wirklich offen sind

**Gemessen am 20.09.2026 gegen `JOURNAL.md` im Stand `481b9f7` (6 526 Zeilen,
letzter Block `BJ`).** Im Ordner `docs/projektfuehrung/nachtraege/` liegen
**elf** `JOURNAL_NACHTRAG_*.md` — nicht zehn, wie Abschnitt 0 des Auftrags
zählt: **`(20f)` ist um 16:50 aus TB-66 hinzugekommen.**

Zwei Muster, je Nachtrag beide angewandt:

- **Muster A** — die TB-Nummer aus dem Titel des Nachtrags in einer
  `## `-Kopfzeile des Journals (`grep -c "^## .*TB-NN[: ]"`).
- **Muster B** — zwei bis vier charakteristische Sätze aus dem Nachtrag, wörtlich
  im ganzen Journal (Whitespace und Blockquote-Präfix `> ` normalisiert, damit
  Zeilenumbrüche nicht trennen; Skript `docs/belege/TB-67/messung1.py`, Zählung mit `grep -c`
  gegengehalten).

| Nachtrag | TB im Titel | Muster A (Kopfzeilen, Block) | Muster B (wörtlicher Satz: Treffer) | Urteil |
|---|---|---|---|---|
| `(c)` 19.09. | TB-55 | **2** (BG, BH) | „die Sitzung, deren Ergebnis ein Nichthandeln ist": **1** · „Der Zug ist nicht wiederholbar; der Abbruch ist es": **1** | **eingearbeitet** — B trifft in **BG**, A bestätigt |
| `(d)` 19.09. | TB-55 | **2** (BG, BH) | „der Eingabezustand existiert": **1** · „1 Commit, 4 Trees, 1 Blob": **1** | **eingearbeitet** — B trifft in **BH**, A bestätigt |
| `(e)` 19.09. | TB-55b, TB-54 | **1** (BI), **1** (BJ) | „der Snapshot steht im Register": **1** · „acht Nachträge, eine Rückfrage": **1** | **eingearbeitet** — zwei Blöcke, **BI** und **BJ**, A und B treffen |
| `(f)` 19.09. | — *(keine im Titel)* | A nicht anwendbar; ersatzweise die TB-Nummern seiner drei Blocküberschriften: TB-53b **0**, TB-58 **0**, TB-58b **0** | „der Resolver erreicht die Selektionsseite": **0** · „Der Engpass war eine Datei, nicht 90 Module": **0** · „Codeherkunft und Lock": **0** · „Abschnitte 19 und 20": **0** | ⭐ **offen** — B ist anwendbar und trifft nicht (siehe Widerspruch unten) |
| `(g)` 19./20.09. | TB-59 | **0** | „Sichern ist keine Abgabe, sondern ein Schritt": **0** · „die Backlog-Einarbeitung": **0** | **offen** |
| `(20a)` | TB-60 | **0** | „Verschieben ist beweisbarer als Behalten": **0** · „das Backlog-Archiv": **0** | **offen** |
| `(20b)` | TB-61, TB-62 | **0**, **0** | „ZIP wird überall abgeschafft": **0** · „fünf Messfehler derselben Familie": **0** | **offen** |
| `(20c)` | TB-61 | **0** | „Der Krypto-Benchmark ist bis 2021 leer": **0** · „drei Befunde, die keiner bestellt hat": **0** | **offen** |
| `(20d)` | TB-65 | **0** | „Der Faktor ist nicht die Nachricht": **0** · „welche Schranke für den Benchmark gilt": **0** | **offen** |
| `(20e)` | TB-62 | **0** | „das Ende der ZIP-Pflicht": **0** · „die Nachträge (m) und (v)": **0** | **offen** |
| `(20f)` | TB-66 | **0** | „der Benchmark wird tagesgenau": **0** · „Ein Platzhalter im Register ist ehrlicher": **0** | **offen** — ⚠️ *im Auftrag nicht gezählt* |

**Zweite Zählung:** dieselben Kopfzeilen-Treffer mit `grep -c "^## .*TB-NN[: ]"`
(TB-55 → 2, TB-55b → 1, TB-54 → 1, alle übrigen → 0) und dieselben Sätze mit
`grep -c` auf Zeilenebene (die vier eingearbeiteten → je 1, die acht offenen → je
0). **Beide Zählungen stimmen überein.**

**Ergebnis: 3 eingearbeitet (4 Blöcke BG–BJ), 8 offen, 0 nicht prüfbar.**

### ⚠️ Widerspruch zum Auftrag: `(f)` ist offen, nicht „nicht prüfbar"

Der Auftrag stuft `(f)` als *nicht prüfbar (A2)* ein, weil sein Titel keine
TB-Nummer nennt. **Das gilt nur für Muster A.** Muster B — der wörtliche Satz —
ist auf `(f)` genauso anwendbar wie auf jeden anderen Nachtrag, und es liefert
mit vier verschiedenen Sätzen viermal 0. Zusätzlich tragen die drei
Blocküberschriften *in* `(f)` die Nummern TB-53b, TB-58 und TB-58b, und keine
davon steht in einer Journal-Kopfzeile. **`(f)` ist damit gemessen offen** —
*nicht prüfbar* wäre es nur, wenn beide Muster versagt hätten (Auftrag,
Schritt 1), und das tut keines.

### ⭐ Befund: `(f)` ist bereits die Journalfassung des Rückblick-Blocks aus `(m)`

Schritt 3 des Auftrags verlangt *„drei Journalblöcke für TB-53b, TB-58 und
TB-58b, aus den 20 Zeilen des Blocks `2s` in `BACKLOG_NACHTRAG_2026-09-19m.md`"*.
**Genau diese drei Blöcke enthält `(f)` schon** — als `## Block ⟨nächster⟩ —
TB-53b …`, `## Block ⟨danach⟩ — TB-58 …`, `## Block ⟨danach⟩ — TB-58b …`, mit
demselben Datum (19.09.2026, 19:48 Uhr Dateizeit, `(m)` ebenfalls 19:48) und
denselben Zahlen (71/19, 0 von 90, `96a5c572…`, N1/N3/N4, 44/44, 160/0). Die
`B`-Zeilen aus `(m)` stehen dort verkürzt als Tabelle *„Was der Nachmittag über
die Arbeitsweise ergab"*.

⇒ **Schritt 2 (Einarbeitung von `(f)`) und Schritt 3 (drei Blöcke aus `(m)`)
sind dieselben drei Blöcke.** Sie werden **einmal** angelegt, nicht zweimal.
Damit das Messprotokoll aus `(m)` (die 13 `T`-Zeilen) wörtlich im Journal steht
und nicht nur die Prosa aus `(f)`, bekommt jeder der drei Blöcke am Ende eine
Tabelle mit seinen `T`-Zeilen aus `(m)`, zeichengleich übernommen, und **zwei
Quellenzeilen** — `(f)` und `(m)`. Die sieben `B`-Zeilen werden, wie der Auftrag
verlangt, **nicht** als Regeln eingetragen, sondern in Nachweis 6 geprüft.

*Was `(f)` gegenüber den `T`-Zeilen nicht enthält, gezählt:* `T58.2` (Fables
drei Fälle) fehlt in `(f)` ganz; `T53.3` steht in `(f)` ohne die Zahlen 63 /
9/9 / 23 / 14. Beides ist der Grund, die `T`-Tabellen mitzunehmen.

---

## Schritt 2 und 3 — die Einarbeitung (Commit `08cf90a`)

**Zehn neue Blöcke `BK`–`BT`, eingefügt vor `## Wiederkehrende Lehren`** — so,
wie es seit TB-50 für `BA`–`BF` und in TB-54/55 für `BG`–`BJ` gemacht wurde
(*„Angefügt am Ende"* im Auftrag meint das Ende der Blockfolge; die Lehren
bleiben der Schluss der Datei). Reihenfolge = Entstehung der Nachträge:

| Block | aus Nachtrag | Inhalt |
|---|---|---|
| `BK` | `(f)` + `(m)` `2s` | TB-53b: der Resolver erreicht die Selektionsseite — mit `T53.1`–`T53.4` |
| `BL` | `(f)` + `(m)` `2s` | TB-58: Codeherkunft und Lock — mit `T58.1`–`T58.6` |
| `BM` | `(f)` + `(m)` `2s` | TB-58b: Abschnitte 19 und 20 — mit `T58b.1`–`T58b.3`; dazu als Unterabschnitte *„Was der Nachmittag über die Arbeitsweise ergab"*, *„Der Stand am Abend des 19.09."*, *„In einfacher Sprache"* (in `(f)` der Schluss nach den drei Blöcken; nach dem Vorbild von `BJ`, wo *„Der Stand am Ende des 19.09."* ebenfalls im letzten Block steht) |
| `BN` | `(g)` | TB-59: die Backlog-Einarbeitung (nachgeholt) |
| `BO` | `(20a)` | TB-60: das Backlog-Archiv (nachgeholt) |
| `BP` | `(20b)` | Die Beauftragung von TB-61 und TB-62 (Chat-Sitzung, Mittag) |
| `BQ` | `(20c)` | TB-61: die Benchmark-Tabelle für neun Bots |
| `BR` | `(20d)` | TB-65: welche Schranke für den Benchmark gilt |
| `BS` | `(20e)` | TB-62: die Nachträge (m) und (v), Ende der ZIP-Pflicht |
| `BT` | `(20f)` | TB-66: der Benchmark wird tagesgenau |

**Wie der Text übernommen wurde** (Skript `docs/belege/TB-67/schritt2_einfuegen.py`):
die Titelzeile `# Journal-Nachtrag …` jedes Nachtrags entfällt (sie wird zur
`## XX — `-Kopfzeile), die Einfüge-Anweisungen an den Einarbeiter (*„Anzufügen
am Ende … Blockbuchstaben messen"*) in `(c)`–`(f)` entfallen; alle
Überschriften innerhalb eines Nachtrags sind um **eine** Stufe abgesenkt
(`##` → `###`, `###` → `####`), damit nur Blockbuchstaben auf `##` stehen —
sonst zählte jede Zwischenüberschrift als Block. **Jede andere Zeile steht
zeichengleich im Journal** — geprüft mit `docs/belege/TB-67/ankunft_pruefung.py`
(`schritt2_ankunft.txt`): je Nachtrag *„fehlend: 0"*, ausser den genannten
Einfüge-Anweisungen (`(c)` 7, `(d)` 4, `(e)` 3, `(f)` 4 Zeilen — alle vier
Fälle sind ausschliesslich die Anweisung an den Einarbeiter).

**Nachweis 3 — `git diff --numstat`, Schritt 2+3 (`cc72150` → `08cf90a`):**

| Datei | hinzu | entfernt |
|---|---:|---:|
| `docs/projektfuehrung/JOURNAL.md` | **965** | **0** |
| `docs/belege/TB-67/ankunft_pruefung.py`, `schritt2_ankunft.txt`, `schritt2_numstat.txt`, `schritt2_einfuegen.py` | neu | — |

`JOURNAL.md` **6 526 → 7 491 Zeilen** (`wc -l`, Differenz 965 = `numstat`).
⭐ **Spalte zwei = 0: nichts umgeschrieben, nur eingefügt** — auch die
Quellenzeilen bei `BG`–`BJ` sind reine Einfügungen (je eine Leer- und eine
Textzeile nach der Kopfzeile).

**Nachweis 4 — Blockbuchstaben:** letzter vorher **`BJ`** (gemessen mit
`grep -n "^## " JOURNAL.md | tail`, nicht aus Abschnitt 0 übernommen — dort
stand er richtig), letzter nachher **`BT`**. Über alle 60 Blöcke `## XX — `:
**kein Buchstabe doppelt** (`ankunft_pruefung.py`: `doppelt: []`; zweite
Zählung `grep -oE "^## [A-Z]{1,2} — " | sort | uniq -d` → leer).

**Nachweis 5 — Quellenzeilen** (Form aus dem Auftrag, wörtlich
`*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_<datum><buchstabe>.md`*`,
direkt unter der Kopfzeile):

| | Anzahl | Blöcke |
|---|---:|---|
| neu | **10** | `BK`–`BT` |
| nachgetragen | **4** | `BG` ← `(c)`, `BH` ← `(d)`, `BI` ← `(e)`, `BJ` ← `(e)` — Zuordnung eindeutig über Muster B (je ein wörtlicher Satz je Block, Nachweis 2) |
| nicht zuordenbar | **0** | — |
| Summe im Journal | **14** | `grep -c "^\*Quelle: "` |

`BK`, `BL`, `BM` tragen **zusätzlich** eine zweite Zeile
`*Messprotokoll: `…/BACKLOG_NACHTRAG_2026-09-19m.md`, Block `2s`*`, weil ihre
`T`-Tabellen aus `(m)` stammen — Schritt 3 verlangt *„die Quellenzeile … mit
dem Backlog-Nachtrag als Quelle"*. Die Zeile ist absichtlich anders benannt,
damit ein Wächter, der `JOURNAL_NACHTRAG_`-Quellen zählt, keinen Backlog-Nachtrag
als Journal-Nachtrag liest.

⚠️ **Zum Pfad in der Quellenzeile:** Er nennt `nachtraege/…`, wie der Auftrag
und TB-64 es vorschreiben. Nach Schritt 5 liegen die Dateien physisch unter
`nachtraege/_eingearbeitet/`. **Die Kennung ist der Dateiname**; wer die Datei
sucht, findet sie eine Ebene tiefer. Ein Wächter, der die Quellenzeile prüft,
muss beide Orte kennen — das steht als Hinweis für TB-64 in Abschnitt „Offen".

⚠️ **Nicht angefasst:** das Inhaltsverzeichnis am Kopf des Journals endet bei
`AG` (seit TB-50 bekannt, Backlog `K1p`). Es fehlen jetzt `AH`–`BT`. Der Auftrag
erlaubt im Journal nur Anfügen und die Quellenzeile; die Tabelle nachzuziehen
wäre ein dritter Eingriff und bleibt bei `K1p`.

---

## Nachweis 6 — Schritt 3: die sieben `B`-Zeilen aus `(m)`, je Zeile geprüft

⛔ **Keine der sieben ist als Regel eingetragen worden.** Im Journal stehen sie
nur so, wie `(f)` sie am 19.09. verkürzt hatte (Tabelle *„Was der Nachmittag
über die Arbeitsweise ergab"* in `BM`) — das ist der Bericht des Tages, keine
Regelübernahme; zeichengleich steht keine `B`-Zeile im Journal
(`ankunft_pruefung.py`: *„B-Zeilen … im Journal zeichengleich: 0"*).

Geprüft mit `grep -n -i` über `ARBEITSWEISE.md`, `DOKUMENTATIONSSTANDARD.md`,
`UMZUG.md`, `UEBERGABE_2026-09-19.md`, `BACKLOG.md`, `BACKLOG_ARCHIV.md`,
`docs/PRUEFPRINZIPIEN.md`, `docs/UMGEBUNGEN.md`, `docs/UEBERGABEPROTOKOLL.md`,
`docs/START_HIER.md`, `docs/VORREGISTRIERUNG_neuselektion.md` — je Zeile mit
zwei bis drei Suchbegriffen; Fundstellen mit Zeilennummer (Stand `08cf90a`):

| | Kern der Zeile | steht in einem Führungsdokument? | Fundstelle |
|---|---|---|---|
| **B1** | F1b/Q2 ist für die **Daten** belegt, nicht für den **Lauf**; der Lock existiert seit `d852bce` | **ja** | `UEBERGABE_2026-09-19.md` Block 4 Punkt 6 (Z. 109) und Block 7 Punkt 5 (Z. 191); `BACKLOG.md` Kettenzeile **0,99** (Z. 1331, aus TB-62) |
| **B2** | Die Cloud hat 3.10–3.13, kein 3.9, kein `pyenv` ⇒ fällt als zweite Maschine für die Laufreproduktion aus; offene Frage an Fable | **teilweise** — die **Folgerung** steht (`0,99`: *„In der Cloud nicht möglich (B2)"*; Übergabe Block 4 Punkt 6: *„gleiche Maschine zulässig"*), der **Messbefund** (welche Python-Fassungen die Cloud hat) steht in keinem Führungsdokument, auch nicht in `docs/UMGEBUNGEN.md` (0 Treffer für `3.13`, `pyenv`, `kein 3.9`). ⚠️ *Und `0,99` verweist mit „(B2)" auf eine Zeile, die bis TB-67 nur in `(m)` existierte* — jetzt in `BM` | `BACKLOG.md` Z. 1331; `UEBERGABE_2026-09-19.md` Z. 109 |
| **B3** | Die Sperre gegen den zweiten Snapshot greift auch im Wegwerf-Klon (rc 2); der Schutz sitzt im Code | **nein** — kein Führungsdokument nennt die Probe. Das Register (Abschnitt 20, Z. 2755 ff.) beschreibt eine Wegwerf-Klon-Probe, aber die des **Locks**, nicht der Snapshot-Sperre; `ERGEBNIS_TB-46_datenordner.md` Z. 260 nennt die Regel *„ein bestehendes `<hash>/` wird nie überschrieben"* als Entwurfsentscheidung, nicht die Messung im Klon | nur `BM` (verkürzt) |
| **B4** | macOS schützt `~/Downloads`; Aufträge nach `logs/auftraege/` | **ja** — inhaltlich, mit inzwischen weiterem Stand: Zwischenlager `logs/auftraege/`, endgültiger Ort `docs/auftraege/` | `UEBERGABE_2026-09-19.md` Block 7 Punkt 9 (Z. 195); `ARBEITSWEISE.md` Abschnitt 14 (Z. 986, 1041) und Z. 782; `DOKUMENTATIONSSTANDARD.md` Z. 139; `BACKLOG.md` `K4g` (als `K2l`) |
| **B5** | Ortsunabhängig seit dem 19.09.; Ursache verschlossener Schlüsselbund; `security unlock-keychain` ohne `-p` | **ja** | `ARBEITSWEISE.md` Abschnitt 14 **Regel 0** (Z. 885–911, dreimal `unlock-keychain`); `BACKLOG.md` `K3t` (Z. 1277); `docs/UEBERGABEPROTOKOLL.md` Z. 892 |
| **B6** | Nie überschreiben, immer neuer Dateiname, gegenprüfen; über die Geräteverbindung kein `git status`/`git log` | **ja** | `UEBERGABE_2026-09-19.md` Block 7 Punkte 7 und 8 (Z. 193–194) und Abschnitt *„Die Geräteanbindung"* (Z. 386 ff., `--no-optional-locks`); `ARBEITSWEISE.md` Abschnitt 14 (Z. 1013, dort nur `git status`); `BACKLOG.md` `K4g` (als `K2q`) |
| **B7** | Vorprüfung vor die Sitzung, nicht in sie (K2b); dist-info ohne Ausführung lesbar, aus „erzeugen" wurde „gegenprüfen" | **ja** für die Regel, **nein** für den Beleg | Regel: `BACKLOG.md` **`K2b`** (Z. 1376); Vorprüfung als Vorgang: `BACKLOG_ARCHIV.md` Abschnitt `2o` (Z. 398). Der dist-info-Weg selbst: 0 Treffer für `dist-info` in allen elf Dokumenten einschliesslich Register Abschnitt 20 |

**Zählung: 5 × ja (B1, B4, B5, B6, B7-Regel), 1 × teilweise (B2), 1 × nein (B3).**
⚠️ Nebenbefund: `index.lock` hat im Backlog inzwischen **1** Treffer (der Auftrag
mass 0) — es ist die `K4g`-Zeile selbst, die die Null-Messung zitiert, kein
Regeleintrag. **Ob B2 (Messbefund), B3 und der B7-Beleg irgendwo als Regel oder
Tatsache hingehören, ist die Betreiberentscheidung, die der Auftrag ausdrücklich
offen lässt.**

---

## Schritt 4 — eine Zeile im Backlog

**Nächste freie K-Nummer, gemessen** mit `^\| \*\*(K\d[a-z])\*\*` (ohne
schliessenden Balken, ohne `sort -u`) über `BACKLOG.md` **und**
`BACKLOG_ARCHIV.md`: höchste vergebene **`K4g`** (Zählung 1: `grep -oE … | sort
| tail`; Zählung 2: Python `max()` über Ziffer und Buchstabe — beide `K4g`).
⇒ vergeben **`K4h`**, eingefügt in **Abschnitt 4** direkt nach der Zeile `K3j`
(dem Ende der Tabelle; Anker genau einmal vorhanden, vor dem Schreiben geprüft).

`git diff --numstat`: `BACKLOG.md` **1 / 0**. K-Zeilen im Backlog 85 → 86, über
beide Dateien **keine Nummer doppelt** (`sort | uniq -d` leer).

⚠️ *Zur Lage von `K4g`:* Sie steht nicht in Abschnitt 4, sondern in Block `2z`
(Z. 1290, TB-62). `K4h` steht in Abschnitt 4, wie der Auftrag verlangt, und
nennt `K4g` — die offene Ortsfrage aus `K4g` ist damit an ihrer Antwort
verlinkt, ohne `K4g` anzufassen.

---

## Nachweis 7 — Schritt 5: was nach `_eingearbeitet/` verschoben wurde, und was offen bleibt

`docs/projektfuehrung/nachtraege/_eingearbeitet/` **existierte nicht** (TB-64
ist noch nicht gelaufen) — **in dieser Sitzung neu angelegt**, per `git mv`
verschoben (git führt die elf als `R`, Umbenennung ohne Inhaltsänderung):

| verschoben | Grund |
|---|---|
| `JOURNAL_NACHTRAG_2026-09-19c.md`, `…19d.md`, `…19e.md` | in Schritt 1 als eingearbeitet gemessen (`BG`, `BH`, `BI`+`BJ`), Quellenzeile nachgetragen |
| `JOURNAL_NACHTRAG_2026-09-19f.md`, `…19g.md`, `…20a.md`, `…20b.md`, `…20c.md`, `…20d.md`, `…20e.md`, `…20f.md` | in Schritt 2 eingearbeitet (`BK`–`BT`), Ankunft je Zeile geprüft |

**Nach dem Verschieben erneut geprüft** (`ankunft_pruefung.py` liest beide
Orte; `schritt5_ankunft_nach_verschieben.txt`): elf Dateien, **7 × „fehlend: 0"**,
4 × nur die Einfüge-Anweisungen (`(c)`–`(f)`, wie in Schritt 2); `T`-Zeilen
13/13; Quellenzeilen 14. Im Hauptverzeichnis `nachtraege/` liegen jetzt
**0** `JOURNAL_NACHTRAG_*.md`.

**Nicht verschoben, absichtlich — die 19 `BACKLOG_NACHTRAG_*.md`:** Der
Auftrag erlaubt nur, was in Schritt 1 oder 2 als angekommen gemessen wurde.
Gemessen wurde von den Backlog-Nachträgen **nur `(m)`, und nur teilweise**: seine
13 `T`-Zeilen sind im Journal (13/13), seine 7 `B`-Zeilen sind — wie
beauftragt — **nicht** eingetragen, seine sechs `K`-Zeilen hat TB-62 geprüft
(`K4g`), seine 0,85-Berichtigung ist laut `K4g` überholt, seine drei
Kettenzeilen-Vorschläge stehen laut `K4g` als `0,85c` / erledigt / `0,99`.
⚠️ **Ob `(m)` damit „eingearbeitet" ist, hängt an der Betreiberentscheidung zu
den `B`-Zeilen** — deshalb bleibt es liegen, ebenso die 18 anderen
Backlog-Nachträge, die diese Sitzung nicht geprüft hat. Das ist TB-64,
Prüfung B.

**Offen bleibt damit:** `(m)` (B-Zeilen, Betreiberentscheidung) und die
Backlog-Nachträge (a)–(v) ausser dem `T`-Teil von `(m)`.

---

## Nachweis 8 — nichts ausserhalb `docs/` geändert

`git diff --stat fe76857..HEAD -- . ':!docs'` → **0 Zeilen Ausgabe.**
`git diff --numstat fe76857..HEAD` (vollständig, Stand vor dem Abgabe-Commit):

| Datei | hinzu | entfernt |
|---|---:|---:|
| `docs/projektfuehrung/JOURNAL.md` | 965 | **0** |
| `docs/projektfuehrung/BACKLOG.md` | 1 | **0** |
| `docs/ERGEBNIS_TB-67_journal_einarbeitung.md` | neu | — |
| `docs/belege/TB-67/` (7 Dateien: 2 Skripte, 5 Ausgaben) | neu | — |
| `docs/projektfuehrung/nachtraege/{ => _eingearbeitet}/JOURNAL_NACHTRAG_*.md` (11) | 0 | 0 — reine Umbenennung |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | 4 | 5 — **Betreiberstand aus Schritt 0**, nicht von dieser Sitzung geändert |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20b_…`, `…20c_…`, `FABLE_ANTWORT_2026-09-20b_…` | 158 / 162 / 87 | 0 — **Betreiberdateien aus Schritt 0** |

---

## Was der Auftrag vorgab, und wo die Messung abweicht

| Auftrag sagt | gemessen | Folge |
|---|---|---|
| zehn Journal-Nachträge | **elf** — `(20f)` aus TB-66 (16:50) kam nach dem Schreiben des Auftrags | mit eingearbeitet (`BT`) |
| „sechs offene" (`g`, `20a`–`20e`) | **acht** — dazu `(f)` und `(20f)` | alle acht eingearbeitet |
| `(f)` nicht prüfbar (A2), weil ohne TB-Nummer im Titel | mit dem Satzmuster **prüfbar und offen**; seine Blocküberschriften tragen TB-53b/58/58b | eingearbeitet, **0 nicht prüfbar** |
| Schritt 3: drei Blöcke **aus `(m)`** bauen | `(f)` **ist** diese drei Blöcke (gleicher Tag, gleiche Zahlen); `(m)` liefert dazu die 13 `T`-Zeilen, die `(f)` verkürzt | Blöcke einmal angelegt, `T`-Zeilen als Messprotokoll dazu, zwei Quellenzeilen |
| `index.lock` 0 Treffer im Backlog | **1** — die `K4g`-Zeile, die die Null zitiert | kein Handlungsbedarf |
| „Sichern: commit **und push**" je Schritt | erster Push (in einer Pipe) abgelehnt; nacktes `git push` am Ende ging durch | Commits je Schritt, **ein** Push am Ende (`fe76857..544b011`) |
| „Angefügt am Ende von `JOURNAL.md`" | seit TB-50 stehen neue Blöcke **vor** `## Wiederkehrende Lehren` | so gemacht; `numstat` Spalte zwei bleibt 0 |

---

## Offen — für den Betreiber und für TB-64

| | |
|---|---|
| ✅ | ~~`git push` für die Commits~~ — **erledigt**, `fe76857..544b011 main -> main` nach dem Abgabe-Commit; dieser Nachtrag ist der achte Commit |
| ⚠️ | **B2 (Messbefund), B3 und der dist-info-Beleg zu B7** stehen in keinem Führungsdokument (Nachweis 6). Ob sie eine Regel oder eine Tatsachennotiz werden, ist die Betreiberentscheidung, die der Auftrag ausklammert |
| ⚠️ | **Nachtrag `(m)` liegt weiter in `nachtraege/`** — sein `T`-Teil ist im Journal, sein `K`-Teil in `K4g`; die `B`-Zeilen hängen an der Entscheidung darüber |
| ⭐ | **Für TB-64:** Die Quellenzeile nennt `nachtraege/JOURNAL_NACHTRAG_…`; die Dateien liegen nach dem Verschieben unter `nachtraege/_eingearbeitet/`. Der Wächter sollte über den **Dateinamen** vergleichen, nicht über den vollen Pfad — und für `BK`–`BM` die zweite Zeile `*Messprotokoll: …*` nicht als Journal-Quelle zählen |
| | **Journal-Inhaltsverzeichnis** endet weiter bei `AG` — `K1p`, unverändert |
| | Der Journal-Nachtrag dieser Sitzung (`JOURNAL_NACHTRAG_2026-09-20g.md`) liegt **offen** in `nachtraege/` — er ist die nächste Bringschuld an das Journal, als Block `BU` |

---

## Die Commits dieser Sitzung

| Commit | Schritt | Inhalt |
|---|---|---|
| `481b9f7` | 0 | Betreiberstand (vier Dateien) unverändert committet |
| `cc72150` | 1 | Messung, Ergebnisdokument angelegt, `docs/belege/TB-67/messung1.py` |
| `08cf90a` | 2+3 | `JOURNAL.md` +965/0: `BK`–`BT`, Quellenzeilen `BG`–`BJ`, `T`-Tabellen |
| `31bc953` | 3 | Nachweise 3–6 (B-Zeilen geprüft, nicht eingetragen) |
| `93a88d4` | 4 | `BACKLOG.md` +1/0: `K4h` |
| `4117ee7` | 5 | elf Dateien nach `_eingearbeitet/` |
| `544b011` | 6 | dieses Dokument abgeschlossen, Journal-Nachtrag `(20g)`; danach `git push` (`fe76857..544b011`) |
| *(Nachtrag)* | 6 | Push-Vermerk berichtigt — in Ergebnisdokument und Nachtrag `(20g)` |

---

## In einfacher Sprache

**Was zu tun war:** Acht Notizdateien lagen seit gestern neben dem Journal und
waren nie übertragen worden — drei erledigte Aufgaben hatten deshalb keinen
Eintrag.

**Was jetzt ist:** Das Journal hat zehn neue Einträge, jeder sagt in einer
Zeile, aus welcher Notiz er stammt, und die vier älteren Einträge haben diese
Zeile nachträglich bekommen. Nichts Altes wurde verändert — das lässt sich an
einer einzigen Zahl ablesen: **0 entfernte Zeilen.** Die elf übertragenen
Notizen liegen jetzt in einem Unterordner „eingearbeitet", der Hauptordner ist
für Journal-Notizen leer.

**Zwei Stellen, an denen der Auftrag danebenlag, und die Sitzung recht behielt:**
Die Notiz ohne Nummer im Titel war sehr wohl prüfbar — man muss nur nach einem
Satz aus ihr suchen statt nach der Nummer. Und die drei Einträge, die aus einem
älteren Zettel neu gebaut werden sollten, existierten in dieser Notiz schon;
sie wurden einmal angelegt und um die Messtabelle des Zettels ergänzt, nicht
doppelt.

**Was fehlt:** Nichts mehr an dieser Aufgabe. Das Hochladen zum Server ging
erst am Ende — der erste Versuch war gesperrt, der letzte ging durch; alle
Sicherungspunkte liegen jetzt auf beiden Rechnern.

# ERGEBNIS TB-63 — Die fünf Epics ausgelagert: `BACKLOG_EPICS.md` (Mac-Sitzung, 21.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-63_epics_auslagern.md`. **Ausgeführt am
MacBook**, Zweig `main`, Ausgang `c96c208` (= `origin/main` beim Start,
TB-75 erledigt), Interpreter `python3` nur für das Zählskript
`docs/belege/TB-63/verschiebenachweis.py` (Standardbibliothek). Keine
Kursdaten, kein Bot-Code, **nichts ausserhalb `docs/`**. Sitzung ab 11:27
Ortszeit; Commits `f2e0a68` (Schritt 0), `79d31fb` (Schritt 1), `a288452`
(Schritt 2), `161de90` (Schritt 3) und der Abgabe-Commit (Ergebnisdokument, Journalblock `CC`, `K4o`). Belege
`docs/belege/TB-63/`.

*In einfacher Sprache, zu Beginn:* Fünf grosse Vorhaben, die erst nach dem
signierten Tag stattfinden, standen in der Aufgabenliste, die jede Sitzung
zuerst liest — fast ein Viertel der Datei. Sie stehen jetzt in einer eigenen
Datei, die nur aufgeschlagen wird, wenn es um sie geht; in der Aufgabenliste
bleibt eine Tabelle, die sagt, wo sie sind. Jede verschobene Zeile ist
maschinell gegen ihren neuen Ort geprüft: nichts ist verloren.

---

## Vorbedingung — TB-62 auf `origin/main`

Gemessen 11:26 nach `git fetch`: `git log origin/main --oneline | grep TB-62`
liefert 14 Treffer, darunter alle sieben TB-62-Commits `e3a25ae` … `6e29eec`
(Schritt 5, Ergebnisdokument). `main` = `origin/main` = `c96c208`. **Nicht
abgebrochen.**

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

Beim Sitzungsstart, 11:27, `HEAD` = `c96c208`, wörtlich
(`docs/belege/TB-63/schritt0_status_vorher.txt`):

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/ARBEITSWEISE.md
 M docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md
```

Drei Betreiber-Dateien, geschrieben 10:24–10:30 Ortszeit (mtime,
`schritt0_mtime.txt`), nach dem TB-75-Abschluss `c96c208` (10:20): der
Auftragszeiger auf TB-63 (numstat 2/3) und die beiden Regeltexte, die TB-75
als offen benannt hatte (`ARBEITSWEISE.md` 52/0, `DOKUMENTATIONSSTANDARD.md`
27/0). Secrets-Probe über den Diff (`api key`, `passwort`, `password`,
`secret`, `token`): 0 Treffer. **Schritt 0:** unverändert committet als
**`f2e0a68`**, gepusht. Danach `git status --short`, 11:27:47
(`nachweis1_status_vor_schreiben.txt`): **eine Zeile**,
`?? docs/belege/TB-63/` — der Belegordner dieser Sitzung mit den
Schritt-0-Belegen, nichts Fremdes. Erst dann wurde an den Dokumenten
geschrieben.

## Was verschoben wurde — an den Ankertexten gemessen, nicht an Zeilennummern

| | gemessen (Stand `f2e0a68`) |
|---|---|
| Anfangsanker `## 2t — Epic AF: Autonome Strategie-Forschungspipeline` | Zeile **335** |
| Anker `## 2z — …` (TB-62) | Zeile **1262**; davor Zeile 1260 `---`, 1261 leer |
| Endanker des Auftrags `## 3 — Die Kette (Ränge 1 bis 5)` | Zeile 1294 — **hinter `2z`** |
| ⇒ verschoben | **Zeilen 335–1259**, vom Anker `2t` bis einschliesslich der Leerzeile nach `QS3`; der Trenner `---` vor `2z` bleibt als Trenner stehen |
| Umfang | **925 Zeilen, 64 633 Bytes**, sechs `##`-Blöcke `2t`, `2u`, `2v`, `2w`, `2x`, `2y` (`grep -c '^## '` auf dem Block: 6) |

⚠️ **Abweichung vom Auftrag, Abschnitt 2:** Der Endanker `## 3` gilt nicht
mehr wörtlich — seit TB-62 (`e3a25ae`) steht Block `2z` zwischen `2y` und
`3`, und der Auftrag sagt selbst, dass `2z` bleibt. Gearbeitet wurde bis
ausschliesslich `## 2z`.

**Hat TB-62 einen der sechs Blöcke verändert?** Gemessen: der Bereich
`2t` … vor `## 3` im Stand `e5720ed` (Stand des Auftrags) hat 929 Zeilen /
**64 643 Bytes** — die Zahl des Auftrags. Der Bereich `2t` … vor `## 2z`
heute hat 925 Zeilen / 64 633 Bytes. `diff` der beiden: **leer bis auf zwei
Zeilen** (`---` und eine Leerzeile) — im Stand `e5720ed` standen zwischen
`2y` und `3` zwei Trenner hintereinander, TB-62 hat `2z` dazwischen gesetzt.
**Die sechs Blöcke selbst sind seit `e5720ed` unverändert.**

## Nachweis 2 — ⭐⭐ Verschiebenachweis

`docs/belege/TB-63/verschiebenachweis.py <basis> [WORKTREE]` vergleicht die
**Zeilen-Multimengen** von `BACKLOG.md` (Basis vs. neu) und `BACKLOG_EPICS.md`
— bewusst **ohne `git diff`**, damit Markdown-Trennlinien `---` nicht als
Diff-Kopfzeilen mitzählen (der TB-60-Fehler, 546 statt 561).

| Lauf | entfernt aus `BACKLOG.md` | davon **nicht** zeichengleich in `BACKLOG_EPICS.md` | nur im Ziel (Kopf, Verweise) | rc |
|---|---:|---:|---:|---|
| nach Schritt 1 (`schritt1_verschiebenachweis.txt`, Basis `f2e0a68`) | **925** | **0** | **2** (Titelzeile, Leerzeile) | 0 |
| nach Schritt 2, kumuliert (`schritt2_verschiebenachweis.txt`, Basis `f2e0a68`) | **921** | **0** | **40** | 0 |

**Gegenprobe erklärt:** Nach Schritt 2 stehen im Ziel 961 Zeilen = 921
verschobene + 40 eigene. Die 40 sind die **36 Kopfzeilen** (Titel, Leerzeile,
34 neue Zeilen: Anlass, Lesehinweis, Reihenfolge, Inhaltsverzeichnis,
Trenner) **plus 4 Leerzeilen**, die die Multimengen-Rechnung gegen 4 Leerzeilen
der neuen Verweistabelle verrechnet — deshalb 921 statt 925 „entfernt“ und
15 statt 19 „hinzugefügt“ (`git diff` rechnet identisch, siehe Nachweis 3).
Die Zeilen, die nur im Ziel stehen, sind im Beleg einzeln aufgelistet; keine
davon stammt aus einem Epic-Block.

## Nachweis 3 — `git diff --numstat` je Datei, zweite Zählung

| Vergleich | `BACKLOG.md` | `BACKLOG_EPICS.md` | deckt sich mit Nachweis 2 |
|---|---|---|---|
| Schritt 1 allein (`79d31fb`, `schritt1_numstat.txt`) | `0  925` | neu, 927 Zeilen (`wc -l`) | ✓ 925 = 925; 927 = 925 + 2 |
| Schritt 2 allein (`a288452`) | `19  0` | `34  0` | — |
| kumuliert `f2e0a68` → `a288452` (`schritt2_numstat_gegen_f2e0a68.txt`) | `15  921` | `961  0` | ✓ 921 = 921; 961 = 921 + 40; 925 − 4 = 921, 19 − 4 = 15 |

## Nachweis 4 — `BACKLOG.md` vorher → nachher (`nachweis4_5_masse.txt`)

| | Zeilen | Bytes |
|---|---:|---:|
| vorher (`f2e0a68`, `git show … | wc`) | 1 505 | 264 481 |
| nachher (`a288452`, `wc`) | **599** | **201 085** |
| Differenz | −906 | **−63 396 (−24,0 %)** |
| `BACKLOG_EPICS.md` | 961 | 66 701 |

⚠️ Der Auftrag nennt 225 194 B (Stand `e5720ed`); zwischen `e5720ed` und
`f2e0a68` ist die Datei um 39 287 B gewachsen (TB-62 `2z`, `K4g`–`K4n`,
TB-64/TB-75). Gemessen wurde am Stand vor dieser Sitzung, nicht am Stand
des Auftrags.

## Nachweis 5 — ⭐ Pflichtlektüre vorher → nachher

**Nachgelesen in `UMZUG.md` Abschnitt 6:** die Pflichtliste hat **fünf**
Dokumente — `UEBERGABE_2026-09-19.md`, `UMZUG.md`, `ARBEITSWEISE.md`,
`PRUEFPRINZIPIEN.md` (unter `docs/`, nicht `projektfuehrung/`), `BACKLOG.md`.
Die „VIER“ des Auftrags ist durch seinen eigenen Nachtrag (TB-68) überholt;
`UEBERGABEPROTOKOLL.md` steht dort ausdrücklich „bei Bedarf“ und zählt nicht.

| Dokument | vorher (`f2e0a68`) | nachher |
|---|---:|---:|
| `UEBERGABE_2026-09-19.md` | 28 953 | 28 953 |
| `UMZUG.md` | 20 051 | 20 051 |
| `ARBEITSWEISE.md` | 70 905 | 70 905 |
| `PRUEFPRINZIPIEN.md` | 17 647 | 17 647 |
| `BACKLOG.md` | 264 481 | 201 085 |
| **Summe** | **402 037** | **338 641** — **−63 396 B (−15,8 %)** |

Zwei Zählungen: `wc -c` je Datei summiert (`nachweis4_5_masse.txt`) und ein
Python-Einzeiler über `len(bytes)`; beide 402 037 → 338 641.

## Nachweis 6 — Kollisionsprobe über beide Dateien (`nachweis6_kollisionsprobe.txt`)

| Probe | Muster | Ergebnis |
|---|---|---|
| Blockbezeichner, `BACKLOG.md` + `BACKLOG_EPICS.md` | `^## 2[a-z]+ ` | **8 Zeilen, 8 verschiedene** (`2s`, `2z` im Backlog; `2t`–`2y` in EPICS), 0 doppelt |
| K-Nummern, beide Dateien | `^\| \*\*(K\d[a-z])\*\*` **ohne schliessenden Balken, kein `sort -u`** (`uniq -c` mit Zählung) | **92 Zeilen, 92 Nummern**, 0 doppelt — alle 92 in `BACKLOG.md`, **0 in EPICS** (die Epics tragen keine K-Zeilen; `K2p`–`K3j` sind in Abschnitt 4 geblieben) |
| dieselben Proben über **drei** Dateien (mit `BACKLOG_ARCHIV.md`) | wie oben | Blöcke **24 / 24**, K **92 / 92**, 0 doppelt |
| Epic-Punktzeilen `AF*`/`MI*`/`QR*`/`KG*`/`RT*`/`QS*` | `^\| \*\*(AF\|MI\|QR\|KG\|RT\|QS)\d` | **0 im Backlog, 28 in EPICS** — nichts davon zurückgeblieben |

## Nachweis 7 — Verweise auf `2t`–`2y` im `docs/`-Baum

Muster `(^|[^A-Za-z0-9_])2[t-y]([^A-Za-z0-9_]|$)` über `docs/**/*.md`,
Stand `a288452` (`nachweis7_verweise_je_datei.txt`, `…_backlog.txt`,
`…_fremd.txt`): **122 Treffer in 16 Dateien.**

| wo | Treffer | stimmen sie noch? |
|---|---:|---|
| `BACKLOG_EPICS.md` | 39 | die sechs Überschriften, ihre Einarbeitungsvermerke, `QS1`/`QS2` („Block 2v, QR4“ …) und der neue Kopf — **ja**, Bezeichner unverändert, alle Ziele in derselben Datei |
| `BACKLOG.md` | 16 | 15 in der neuen Verweistabelle, 1 im Vermerk von `2z` („nach `2y` gemessen“) — **ja** |
| `MAC_TB-63_epics_auslagern.md` | 16 | der Auftrag selbst |
| 13 weitere Dateien | 51 | `MAC_TB-59` (11), `JOURNAL.md` (6, Block zu TB-59), `JOURNAL_NACHTRAG_19g` (6), `BACKLOG_NACHTRAG_19n/o/p/q` (13), `ERGEBNIS_TB-64` (5), `UEBERGABE_2026-09-19` (4), `ERGEBNIS_TB-62` (2), `MAC_TB-62` (2), `MAC_TB-60` (1), `DOKUMENTATIONSSTANDARD` (1) — **Nummernangaben** („höchster Block `2y`“, „Block 2t vorgeschlagen“, „`2x`-Namensraum erschöpft“ — 4 Treffer meinen den Namensraum, nicht den Block) und **Rückblicke** auf die Einarbeitung durch TB-59. **Keiner nennt einen Ort wie „`BACKLOG.md` Abschnitt `2t`“, der jetzt falsch wäre.** Alle stimmen, weil die Bezeichner unverändert sind |

⚠️ Zwei Stellen, **innerhalb der verschobenen Blöcke**, sagen „in Abschnitt 2
eingearbeitet“ (Vermerke TB-59 in `2w` und `2x`) bzw. „Die Blöcke 2t bis 2x
sind nach Nachtragsbuchstaben eingearbeitet“ (`2t`). Das ist der damalige
Wortlaut und bleibt, wie beim Archiv, unverändert stehen (Auftrag,
Abschnitt 8: Inhalte nicht ändern); der Kopf der neuen Datei sagt es.

## Nachweis 8 — nichts ausserhalb `docs/`

`git diff --name-only f2e0a68 HEAD | grep -vc '^docs/'` → **0**;
`git status --porcelain` nach dem letzten Commit → **leer** (siehe
Abgabe-Commit). Beleg `nachweis8_nur_docs.txt`.

---

## Was in `BACKLOG.md` an der Stelle steht (Schritt 2, `a288452`)

Eine `##`-Überschrift, zwei Sätze (alle fünf hinter dem signierten Tag
geparkt; die Datei wird nur gelesen, wenn es um die Epics geht — dazu, was
bleibt: Ränge 6–8, `0,96`–`0,98`, Abschnitt 4, und die Reihenfolge
`AF → RT → QR → KG → MI`), die Tabelle Block · Epic · Datei für `2t`–`2y`.
Bezeichner unverändert. 19 Zeilen, `numstat 19 0`.

## Der Kopf von `BACKLOG_EPICS.md` (Schritt 2)

Nach dem Muster von `BACKLOG_ARCHIV.md`: Anlass und Datum, *„gehört nicht in
jede Sitzung“*, was die Datei enthält, *„hier wird nichts entschieden“* mit
der Aufzählung dessen, was im Backlog bleibt, die **Reihenfolge
`AF → RT → QR → KG → MI`** mit der Begründung aus `RT9`, das
Inhaltsverzeichnis `2t`–`2y` mit Nachtragsbuchstaben, der Stand
(`f2e0a68`, gegen `e5720ed` unverändert), der Verweis auf dieses Dokument und
der Satz, dass nichts gelöscht ist. 34 Zeilen, `numstat 34 0`.

---

## ⚠️⚠️ Nebenbefund — der Nachtragswächter kennt die neue Datei nicht

Nach dem Journalblock wurde `system/nachtragswaechter.py` als Gegenprobe
gestartet (wie TB-75 es getan hat): **rc 1, „3 falsch verschoben“** —
`(19n)`, `(19o)`, `(19p)` mit je *„Block `2t`/`2u`/`2v` — Nummer nicht im
Ziel, Kern nirgends“* (`docs/belege/TB-63/schritt4_waechter_befund.txt`).
**Ursache, im Code gelesen:** `Ziel.backlog_zeilen` ist fest `BACKLOG.md` +
`BACKLOG_ARCHIV.md` (Zeile 222); `BACKLOG_EPICS.md` gibt es für ihn nicht.
**Bestätigt ohne Codeänderung:** mit `--archiv <Archiv + Epics
aneinandergehängt>` (Wegwerfdatei im Scratchpad) meldet er **rc 0, 0 falsch
verschoben** (`schritt4_waechter_gegenprobe.txt`).

| | |
|---|---|
| ⛔ nicht behoben | der Wächter liegt unter `system/`, dieser Auftrag darf nichts ausserhalb `docs/` ändern (Nachweis 8) |
| ⭐ eingetragen | `BACKLOG.md` Abschnitt 4, **`K4o`** (nächste freie gemessen: `K4n` höchste, `K4o` 0 Treffer in drei Dateien) — Ursache, Gegenprobe, der Einzeiler samt Test als offener Punkt |
| ⚠️ heute still | die Cron-Zeile des Wächters ist weiterhin **nicht** eingetragen (`crontab -l` 0 Treffer) — ohne diesen Lauf hätte niemand den Befund gesehen |
| Regel | *Wer eine Zieldatei aufteilt, prüft, welche Wache die alte Zielmenge fest verdrahtet hat* |

## Abweichungen vom Auftrag

| Stelle | Auftrag | gemessen / getan |
|---|---|---|
| Abschnitt 2, Endanker | `## 3 — Die Kette` | `## 2z` liegt davor und bleibt; Ende ist der Trenner vor `2z` |
| Abschnitt 0, Bytes | `BACKLOG.md` 225 194 B, Epics 64 643 B | 264 481 B beim Start (`f2e0a68`); 64 643 B stimmt für `e5720ed` **einschliesslich** der beiden Trenner, verschoben 64 633 B |
| Nachweis 5, „VIER“ | vier Dokumente | **fünf** — der Auftrag berichtigt sich im selben Feld; nachgelesen |
| Schritt 4, „ein Journal-Nachtrag“ | Nachtragsdatei | **Journalblock direkt** (`CC`), Quellenzeile auf dieses Dokument — Regel seit TB-75 (Betreiberentscheidung 21.09.), in `ARBEITSWEISE.md` 14 und `DOKUMENTATIONSSTANDARD.md` 10 eingetragen und in Schritt 0 dieser Sitzung committet (`f2e0a68`) |
| Abschnitt 1, Gegenprobe | „Kopf und Verweise“ | nach Schritt 2: 36 Kopfzeilen + 4 verrechnete Leerzeilen = 40, mit Zweck je Zeile im Beleg |

## Fehler → Regel

| Fehler | Regel |
|---|---|
| Der erste Lauf des Verschiebenachweises zählte **928** Zielzeilen, `wc -l` 927: `str.split("\n")` liefert nach dem Schlusszeilenumbruch ein leeres Element, das als Leerzeile mitzählte. Aufgefallen nur, weil die zweite Zählung daneben stand | ⭐ **Ein Zählskript wird an `wc -l` derselben Datei geeicht, bevor seine Zahl als Nachweis gilt** — `splitlines()` statt `split("\n")`. Derselbe Fall wie TB-60 (`---` als Diff-Kopf): das Instrument, nicht der Bestand |
| Die kumulierte Zählung sagt 921/15, die je Schritt 925/19 — beide richtig, weil Leerzeilen der Tabelle gegen Leerzeilen des Blocks verrechnet werden | ⭐ **Zwei Zahlen, die dasselbe zu messen scheinen, werden im Bericht gegeneinander abgegrenzt** (`DOKUMENTATIONSSTANDARD.md` Regel 2): je Schritt = was bewegt wurde, kumuliert = was `git` sieht |

## ⚠️ Offen — nicht Teil dieses Auftrags

| | |
|---|---|
| **1** | Der Kopf von `BACKLOG.md` (Zeilen 6–12) nennt nur `BACKLOG_ARCHIV.md` als ausgelagerte Datei; `BACKLOG_EPICS.md` steht bisher nur in der Verweistabelle an der Stelle der Blöcke. Ein Satz im Kopf wäre der Ort, an dem eine neue Sitzung es zuerst sieht — **Vorschlag für TB-70** (Abschnitt 2 aufräumen), nicht hier gemacht, weil der Auftrag die Stelle nennt |
| **2** | **Projektablage nachziehen** (`K4e`): `BACKLOG.md` ist ein Führungsdokument und geändert — der Betreiber lädt den Stand `a288452` oder neuer in die Ablage. `BACKLOG_EPICS.md` ist keine Pflichtlektüre; ob sie in die Ablage gehört, ist seine Entscheidung — **nicht gemessen**, ob `BACKLOG_ARCHIV.md` dort liegt (die Ablage ist von hier aus nicht lesbar) |
| **3** | ⚠️⚠️ **Wächter um `BACKLOG_EPICS.md` erweitern** — `K4o`, ein Zeiler plus Test unter `system/`, eigener kleiner Auftrag; bis dahin meldet jeder Lauf rc 1 |
| **4** | `TB-70` hängt an TB-63 und ist damit frei — Abschnitt 2 von `BACKLOG.md` ist mit 107 135 B (Stand `e5720ed`, nicht neu gemessen) jetzt der grösste Posten |

---

## In einfacher Sprache

**Was wir wissen wollten:** Lässt sich die Aufgabenliste um die fünf grossen,
geparkten Vorhaben erleichtern, ohne dass eine Zeile verlorengeht?

**Was herauskam:** Ja. `BACKLOG.md` ist von 264 auf 201 Kilobyte gefallen
(−24 %), die Pflichtlektüre einer neuen Sitzung von 402 auf 339 Kilobyte
(−16 %). Alle 925 verschobenen Zeilen stehen zeichengleich in
`BACKLOG_EPICS.md` — geprüft mit einem Vergleich der Zeilenmengen und
unabhängig davon mit `git`, beide sagen dasselbe. Kein Bezeichner wurde
umbenannt, keine Nummer ist doppelt, und keiner der 122 Verweise auf `2t`
bis `2y` im Dokumentenbaum zeigt jetzt ins Leere.

**Was das für dich heisst:** Jede künftige Sitzung liest 63 Kilobyte
weniger, bevor sie anfängt. Die Epics sind nicht weg, sondern dort, wo sie
hingehören — in einer Datei, die man aufschlägt, wenn es um sie geht. Und der
nächste, grössere Posten (Abschnitt 2, TB-70) ist jetzt frei.

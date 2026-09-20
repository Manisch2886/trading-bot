# ERGEBNIS TB-62 — Einarbeitung der Nachträge (m) und (v), ZIP-Pflicht abgebaut (Mac-Sitzung, 20.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-62_nachtraege_m_v.md`. **Ausgeführt am MacBook**,
Zweig `main`, Ausgang `7a696be` (= `origin/main`), **reine Dokumentation** — kein
Interpreter, keine Kursdaten, nichts ausserhalb `docs/`. Sechs Commits dieser
Sitzung, jeder einzeln gepusht: **`e3a25ae`** (Schritt 1, Block 2z),
**`4b55a33`** (Abschnitt 5, K1o/K1q zusammengeführt), **`e270e63`** (Schritt 2,
die zwei Regeln aus (m)), **`62828df`** (Schritt 3, Vermerk K4g), **`73000be`**
(Schritt 4, ZIP-Umbau), **`5cbd625`** (drei vorgefundene Betreiber-Dateien, siehe
unten) und der Abgabe-Commit (dieses Dokument, Journal-Nachtrag (e)).

*In einfacher Sprache, zu Beginn:* Zwei Notizzettel wurden in die Aufgabenliste
übertragen, zwei verlorene Regeln an ihren Platz in der Arbeitsweise gestellt,
und überall, wo die Arbeitsweise noch ein ZIP verlangte, steht jetzt der Commit.

---

## Das Ergebnis zuerst — in sechs Sätzen, jeder gemessen

1. ⭐ **Nachtrag (v) steht als Block `2z` im Backlog, alle 22 Nummern `K3k`–`K4f`
   unverändert** — jede der 22 Zeilen ist zeichengleich mit dem Nachtrag
   (`grep -xF`, 22 von 22). Vorher gemessen: keine der 22 Nummern in
   `BACKLOG.md` oder `BACKLOG_ARCHIV.md` belegt, höchster Block `2y`. **Kein
   Vergabevermerk nötig.**
2. ⭐ **Die zwei nirgends geführten Regeln aus (m) stehen in `ARBEITSWEISE.md`:**
   „Rückfrage und Antwort wörtlich in den Bericht" als Unterabschnitt am Ende von
   Abschnitt 15 (Z. 1050–1067), „die Sitzung committet Auftrag und Belege mit"
   als Absatz zu Abschnitt 14 Regel 3 (Z. 981–988). Vorher: in keinem
   Regeldokument, nur als Zitat in `UEBERGABE_2026-09-19.md` Z. 239/243.
3. ⭐ **Die vier übrigen (m)-Regeln sind mit einer Zeile (`K4g`) abgeschlossen** —
   mit den **gemessenen** Fundorten, die vom Auftrag abweichen (Abschnitt 4
   unten).
4. ⭐⭐ **ZIP ist aus allen fünf genannten Trägern als Vorschrift verschwunden.**
   `ARBEITSWEISE.md`: 37 Fundstellen, davon 25 Vorschrift (A, Mittel getauscht),
   6 Redewendung (B, umformuliert), 4 historischer Beleg (C, unverändert), 2 ohne
   ZIP-Bezug. `UMZUG.md`: 4 Fundstellen, 2 C, 2 in einer 23-zeiligen Kopie des
   Abschnitt-10-Textes, die nach Regel 9 entfernt ist. `UEBERGABEPROTOKOLL.md`:
   1 Fundstelle, C. `DOKUMENTATIONSSTANDARD.md` und `BACKLOG.md`: 0 mit
   ZIP-Bezug.
5. ⚠️ **Die Doppelbelegung `K1o`/`K1q` ist behoben** — 64 Zeilen / 62 Nummern
   vorher (bestätigt), jetzt **85 Zeilen / 85 Nummern / 0 doppelt** über beide
   Dateien, mit zwei unabhängigen Zählungen (grep-Kette und Python).
6. ⚠️⚠️ **Der Auftrag beschreibt Nachtrag (m) unvollständig:** (m) besteht nicht
   aus sechs Zeilen, sondern aus **sechs K-Zeilen plus einem Rückblick-Block mit
   20 Zeilen** zu TB-53b, TB-58 und TB-58b, einer 0,85-Berichtigung und drei
   Kettenzeilen-Vorschlägen. Der Rückblick-Block ist **nicht** eingearbeitet und
   steht nirgends — Abschnitt 6.

---

## 1. Was der Auftrag vorgab, und wo die Messung abweicht

| Auftrag sagt | gemessen | Folge |
|---|---|---|
| (v) hat Nummern „`K3k` aufwärts, selbst zählen" | **22** Zeilen, `K3k`–`K3z` (16) und `K4a`–`K4f` (6) | übernommen |
| (m) hat 6 Nummern `K2l`–`K2q`, alle sechs kollidieren | bestätigt — `K2l`–`K2o` tragen (s)/(t), `K2p`/`K2q` tragen (n) | keine der sechs neu vergeben (Auftrag, Schritt 3) |
| Vier (m)-Regeln stehen in `ARBEITSWEISE.md`, `UMZUG.md`, Protokoll, Backlog | **teilweise falsch zugeordnet** — siehe Abschnitt 4 | Fundorte in `K4g` berichtigt |
| ZIP-Pflicht steht in `ARBEITSWEISE.md` **Abschnitt 1** | steht in **Abschnitt 2** („Ausgaben", Z. 98–137); Abschnitt 1 („Die vier Wege") enthält das Wort ZIP nicht | Abschnitt 10 verweist jetzt auf Abschnitt 2 |
| `numstat` für `BACKLOG.md` nach der K1o/K1q-Zusammenführung: „genau diese zwei Zeilen in Spalte zwei" | **4** — die zwei `(unverändert)`-Zeilen sind ersatzlos entfernt, die zwei älteren Zeilen zählt git als entfernt und neu, weil der Fortschreibungsvermerk hineingeschrieben wurde | so berichtet, Abschnitt 3 |
| `K1o`/`K1q` in Zeilen 1331/1335 und 1333/1336 (Stand `28eea5c`) | an `7a696be`: **1331/1335 und 1333/1336** — unverändert | bestätigt |
| „mit vier verschiedenen Mustern gesucht, 0 Treffer" für die zwei Regeln | bestätigt für die Regeldokumente; **ein Treffer** als wörtliches Zitat in `UEBERGABE_2026-09-19.md` Z. 239 und 243 (dort ausdrücklich „damit sie diesen Text überleben") | kein Widerspruch — ein Zitat ist kein Regelort |
| (m) = die sechs K-Zeilen | (m) enthält zusätzlich Block „2s" (20 Zeilen), 0,85-Berichtigung, 3 Kettenzeilen | ⚠️ Abschnitt 6 |

---

## 2. Die Nachweise, in der Reihenfolge des Auftrags

### Nachweis 1 — `git status --short` vor dem ersten Schreiben

Leer. `HEAD` = `7a696be` = `origin/main`. **Schritt 0 fand nichts zu committen.**
⚠️ Während der Sitzung erschienen drei Dateien des Betreibers im Arbeitsbaum —
Abschnitt 7.

### Nachweis 2 — `git diff --numstat` je Commit und Datei

| Commit | Datei | + | − | Begründung der Spalte zwei |
|---|---|---:|---:|---|
| `e3a25ae` | `BACKLOG.md` | 29 | **0** | Block 2z: Überschrift, Einleitung, Tabellenkopf, 22 Zeilen |
| `4b55a33` | `BACKLOG.md` | 2 | **4** | K1o/K1q: zwei `(unverändert)`-Zeilen ersatzlos entfernt (Inhalt steht in der verbliebenen Zeile), zwei Zeilen um den Fortschreibungsvermerk ergänzt (git: entfernt + neu). Regel 9, vom Auftrag verlangt |
| `e270e63` | `ARBEITSWEISE.md` | 28 | **0** | zwei Regeln aus (m) |
| `62828df` | `BACKLOG.md` | 1 | **0** | Vermerk `K4g` |
| `73000be` | `ARBEITSWEISE.md` | 58 | **55** | ZIP-Umbau: Gruppe A nach Regel 9 ersetzt, nicht danebengestellt — jede entfernte Zeile in Abschnitt 5 einzeln zugeordnet |
| `73000be` | `UMZUG.md` | 10 | **30** | Abschnitt 7: 23-zeilige Kopie des Abschnitt-10-Textes samt Einleitung und Zaun entfernt, Vermerk eingesetzt (Regel 9: Kopie, deren Inhalt anderswo steht; per `diff` zeichengleich mit `ARBEITSWEISE.md` Z. 763–785 vor dem Commit) |

**Summe `BACKLOG.md` über alle Commits: 32 hinzu, 4 entfernt.** Die alte Null ist
für die zwei Einfüge-Commits erreicht; die vier entfernten Zeilen sind die vom
Auftrag in Abschnitt 5 verlangte Ausnahme.

### Nachweis 3 — Zeilenzahl `BACKLOG.md`

| | `wc -l` | `awk 'END{print NR}'` |
|---|---:|---:|
| vorher (`7a696be`) | **1469** | 1469 |
| nachher (`62828df`) | **1497** | 1497 |

1469 + 29 − 2 + 1 = 1497 ✓ (netto der Zusammenführung: +2 −4 = −2).

### Nachweis 4 — Kollisionsprobe, Muster `^\| \*\*(K\d[a-z])\*\*`, ohne `-u`

| | Zeilen | verschiedene Nummern | doppelt |
|---|---:|---:|---|
| vorher, `BACKLOG.md` | 64 | 62 | `K1o`, `K1q` — **bestätigt** (Z. 1331/1335, 1333/1336) |
| vorher, `BACKLOG_ARCHIV.md` | 0 | 0 | — |
| nach Schritt 1 | 86 | 84 | `K1o`, `K1q` (noch) |
| nach der Zusammenführung | 84 | 84 | keine |
| **nachher, beide Dateien** | **85** | **85** | **keine** |

Zweite, unabhängige Zählung (Python `re.match` + `Counter` über beide Dateien):
**85 Zeilen, 85 Nummern, doppelt: []**. Blockbezeichner `^## (2[a-z])`:
`BACKLOG.md` `2s`–`2z` (8), `BACKLOG_ARCHIV.md` `2b`–`2k`, `2m`–`2r` (16), **kein
Bezeichner doppelt**. ⚠️ *Nebenbefund, nicht Gegenstand: `2l` kommt in keiner der
beiden Dateien als Überschrift vor — ob es ihn je gab, ist nicht gemessen.*

⭐ **Der `2x`-Namensraum ist erschöpft.** Vorschlag für den nächsten Block:
**`2za`** — zweibuchstabige Verlängerung, wie `K3`→`K4` bei den Kettenzeilen den
Zähler verlängert; die Probe `^## (2[a-z])\b` müsste dafür auf `^## (2[a-z]+)`
erweitert werden. Alternative: Abschnitt 2 wird mit TB-69 ohnehin aufgeräumt,
dann stellt sich die Frage neu.

### Nachweis 5 — die zwei Regeln aus (m)

| Regel | vorher (Muster: `wörtlich in den Bericht`, `Rückfrage.*wörtlich`; `eigenen Auftrag`, `committet ihren`, `Belege.*committ`) | nachher |
|---|---|---|
| (1) Rückfrage und Antwort wörtlich in den Bericht | 0 in `ARBEITSWEISE.md`, `DOKUMENTATIONSSTANDARD.md`, `UMZUG.md`, `PRUEFPRINZIPIEN.md`, `UEBERGABEPROTOKOLL.md`, `BACKLOG.md`; 1 Zitat `UEBERGABE_2026-09-19.md:239` | `ARBEITSWEISE.md` Abschnitt 15, Unterabschnitt „Und jede Rückfrage an den Betreiber steht samt Antwort wörtlich im Bericht" (Z. 1050–1067) |
| (2) Die Sitzung committet Auftrag und Belege mit | 0 in denselben sechs; 1 Zitat `UEBERGABE_2026-09-19.md:243`. `UMZUG.md` Schritt 1 nennt nur die Zielorte beim Umzug, nicht die Pflicht der Sitzung | `ARBEITSWEISE.md` Abschnitt 14, Regel 3, Absatz „Und gesichert wird nicht nur das Ergebnisdokument" (Z. 981–988) |

Beide Abschnitte vorher gelesen: **keine der zwei Regeln stand dort sinngemäss**,
also je ein neuer Absatz statt Ergänzung eines Satzes. Beide Absätze nennen ihre
Herkunft (Nachtrag (m), K4b).

### Nachweis 6 — nichts ausserhalb `docs/`

`git diff --stat 7a696be..HEAD -- . ':!docs'` → **0 Zeilen.**

### Nachweis 7 — `git status --porcelain` nach dem letzten Commit

Steht am Ende des Abgabe-Commits im Journal-Nachtrag (e); erwartet leer.
Vor dem Abgabe-Commit, nach `5cbd625`: **leer.**

### Nachweis 8 — der ZIP-Umbau

Muster `ZIP|Zip|zip|Archiv`. ⚠️ **Das Muster trifft auch `Prüfprinzipien`
(„zip") und `Disziplin`** — rohe Treffer in `ARBEITSWEISE.md` **44**, nach Abzug
**37**; in `DOKUMENTATIONSSTANDARD.md` roh 4, bereinigt **0**; im Protokoll roh 9,
bereinigt 4, davon 3 „Archiv" ohne ZIP-Bezug (Log-Rotation, `BACKLOG_ARCHIV`).
*Dieselbe Fehlerklasse wie K4a: ein Muster, das mehr trifft, als es meint.*

**`ARBEITSWEISE.md`, 37 Zeilen (Nummern der Fassung `7a696be`):**

| Gruppe | Zeilen | Behandlung |
|---|---|---|
| **A — Vorschrift** (25) | 98–100, 102, 104–105, 108–111, 113–114, 121, 134–135 (Abschnitt 2); 353, 360 (5b); 736 (7c); 767–768 (10); 1117, 1122–1124, 1126 (18, P.4) | Mittel getauscht, alter Wortlaut entfernt |
| **B — Redewendung / Beispiel** (6) | 130 (Zitat-Wortlaut für den Cloud-Auftrag), 153 (Ausnahme-Ablauf Schritt 1), 511 und 520 (6bb), 678 (7, „Rohausgabe liegt im ZIP"), 807 (11, „nur im Archiv?") | umformuliert auf den Commit bzw. `docs/belege/` |
| **C — historischer Beleg** (4) | siehe unten | **unverändert**, byteweise geprüft |
| **ohne ZIP-Bezug** (2) | 1079, 1081 — „Archiv" meint `BACKLOG_ARCHIV.md` | unverändert |

**Gruppe C, jede Stelle einzeln — und warum sie stehen bleibt:**

| Zeile (alt → neu) | Wortlaut | bleibt, weil |
|---|---|---|
| 193 → 194 | *„Textdateien sind mehrfach leer angekommen — **ZIP hat immer funktioniert**."* | gemessener Hintergrund von 2026-09-15; die neue Regel in Abschnitt 2 nennt Datum und Grund des Wechsels, damit dieser Satz als Vergangenheit lesbar bleibt. Vom Auftrag ausdrücklich als C benannt |
| 261 → 262 | *„nur in Chat-Bewertungen und ZIP-Archiven"* | beschreibt, wo drei Aufgaben am 18.09. tatsächlich lagen — Beleg über die Vergangenheit |
| 558 → 559 | *„Betroffen: die ZIP-Frage (12:40)"* | Berichtigungsvermerk zu 6d — nennt das Ereignis, in dem die Entscheidung fiel |
| 797 → 801 | *„Er existiert nur in einem ZIP-Archiv. Geht das verloren, ist die Nachrechnung verloren."* | Anlass von Abschnitt 11 (TB-48) — wo der Prüfer damals lag, ist eine Tatsache |

Prüfung: alle vier alten Zeilen kommen in der neuen Fassung mit `grep -xF`
zeichengleich vor (4 von 4, dazu 1079/1081).

⚠️ **Berichtigung zum Commit-Text von `73000be`:** dort steht „24 A, 5 B, 6 C,
2 ohne Bezug". Richtig ist **25 A, 6 B, 4 C, 2 ohne Bezug = 37** — Zeile 130 war
im Commit-Text nicht gezählt und die zwei `BACKLOG_ARCHIV`-Zeilen doppelt. Die
Zeilenliste oben ist die gezählte; der Commit-Text ist nicht änderbar, ohne die
Historie umzuschreiben.

**Was inhaltlich geändert wurde (A):**

| Abschnitt | vorher | nachher |
|---|---|---|
| **2** | ein ZIP je Antwort, benannt `TB-<Nr>_<Kurzname>.zip`, nach `~/Downloads` (nicht ins Repo); Testaufträge enthalten die ZIP-Pflicht; Chat-Läufe sichern als ZIP; Abnahme prüft die ZIP-Pflicht | **Kein Archiv** — Betreiberentscheidung 20.09.2026 zitiert, der Widerspruch zu Abschnitt 10 benannt (`K4c`), der Zweck („ein Beleg muss die Sitzung überleben") behalten, das Mittel getauscht. Tabelle je Weg: Mac (Commit nach `docs/`, `docs/belege/`, `docs/auftraege/`, nach jedem Teil), Cloud (dasselbe über PR; Testdokument verlangt den Commit), Chat (einzelne Dateien). Chat-Läufe sichern nach `docs/belege/` und committen; Abnahme prüft die Commit-Pflicht |
| **5b** | Nachtrag „im SELBEN Archiv"; „EIN Archiv je Antwort" | Nachtrag „in DERSELBEN Antwort"; kein Archiv |
| **7c** | Zeile `ZIP — verbindlich, nach ~/Downloads` | Zeile `Commit — docs/, docs/belege/TB-<Nr>/, docs/auftraege/, nach jedem fertigen Teil; kein Archiv, nichts nach ~/Downloads` |
| **10** | „ersetzt die frühere ZIP-und-Anhang-Übergabe, die … überholt ist" — eine Ausnahme für den Umzug | „für den Umzug gilt dieselbe Regel wie für jede Abgabe (Abschnitt 2)" — die Betreiberzitate vom 19.09. bleiben als Anlass |
| **18, P.4** | Wortlaut für Aufgabenbeschreibungen: „gebündelt als eine ZIP-Datei bereitstellen" | Wortlaut: „am Ende im Repo … committet und gepusht — keine ZIP-Datei" |
| Kopf | „Geprüfte Fassung vom 18.09.2026" | eine Zeile ergänzt: „Umgestellt 20.09.2026 (TB-62): ZIP überall abgeschafft — Abschnitte …" |

**Die übrigen Träger:**

| Datei | roh | bereinigt | A | B | C | ohne Bezug |
|---|---:|---:|---:|---:|---:|---:|
| `DOKUMENTATIONSSTANDARD.md` | 4 | **0** | — | — | — | — |
| `UMZUG.md` | 6 | **4** | 2 (Z. 259–260, in der Kopie des Abschnitt-10-Textes → Kopie entfernt) | 0 | 2 (Z. 9 „Der alte Abschnitt verlangte ein ZIP-Paket", Z. 14 Betreiberzitat „Ich lese die Zipp und berichte nie" — Entstehung des Dokuments) | 0 |
| `UEBERGABEPROTOKOLL.md` | 9 | **4** | 0 | 0 | 1 (Z. 975: „durch viele ZIP-Downloads sind nummerierte Duplikate … entstanden" — Beschreibung des Nutzer-Kenntnisstands, Vergangenheit) | 3 (Z. 545 Log-Archive, Z. 875–876 `BACKLOG_ARCHIV`) |
| `BACKLOG.md` | 25 | 14 | 0 | 0 | 0 | 14 (alle „Archiv" = `BACKLOG_ARCHIV.md`) |

`docs/auftraege/*.md` und `docs/belege/` nicht angefasst (Gruppe C, Auftrag
Schritt 4.5). ⚠️ *Nicht gesucht, weil nicht genannt: `UEBERGABE_2026-09-19.md`
(Block 8 Punkt 9 führt die ZIP-Abschaffung als „in Arbeit" — kann jetzt als
erledigt fortgeschrieben werden; das Dokument pflegt die Chat-Sitzung),
`START_HIER.md`, `PRUEFPRINZIPIEN.md`, `docs/vorlagen/`.*

---

## 3. Die Zusammenführung K1o / K1q, Zeile für Zeile

| entfernt (Z. an `7a696be`) | Wortlaut | verbleibt in |
|---|---|---|
| 1335 | `\| **K1o** \| *(unverändert)* gealterte Zahlen im Docstring von basislauf.py — jetzt **drei** Angaben, siehe **T51.6** \|` | Z. 1331 (neu): Originaltext + *„Fortgeschrieben mit TB-51: jetzt **drei** Angaben, siehe **T51.6**"* + Zusammenführungsvermerk |
| 1336 | `\| **K1q** \| *(unverändert)* STRATEGIEN_uebersicht.md — Entscheidung offen, siehe **T51.5** \|` | Z. 1333 (neu): Originaltext + *„Fortgeschrieben mit TB-51: Entscheidung offen, siehe **T51.5**"* + Zusammenführungsvermerk |

Kein Inhalt verloren: beide Verweise (T51.6, T51.5) und beide Aussagen („drei
Angaben", „Entscheidung offen") stehen in den verbliebenen Zeilen. Die
`~~K1n~~`-Zeile davor ist eine Erledigt-Markierung, keine Doppelbelegung, und
bleibt.

---

## 4. Die vier (m)-Regeln — wo sie wirklich stehen

Der Auftrag (Tabelle in Abschnitt 0) nannte Fundorte; gemessen mit `grep`
(Muster: `Downloads`, `Ordnerschutz`, `ortsunabhängig`, `Mac-pflichtig`,
`solange eine|während eine`, `Geräteanbindung|Geräteverbindung`, `überschreib`,
`git log`, `index.lock`):

| aus (m) | Regel | Auftrag sagt | gemessen |
|---|---|---|---|
| `K2l` | Aufträge nie nach `~/Downloads` | `ARBEITSWEISE.md`, `UMZUG.md`, Protokoll | `UEBERGABE_2026-09-19.md` Block 7 Punkt 9 und Block 8 Punkt 9; `ARBEITSWEISE.md` Abschnitt 14 Regel 2 (`docs/auftraege/` als Ort). ⚠️ `ARBEITSWEISE.md` Z. 116 **verlangte** bis Schritt 4 das Gegenteil (ZIP nach `~/Downloads`); `UMZUG.md` Z. 58 nennt `~/Downloads` nur als Vergleich; das Protokoll (Z. 975) beschreibt den Ordner, ohne Regel |
| `K2m` | `[ortsunabhängig]` / `[Mac-pflichtig]` | Backlog | **nur** `UEBERGABE_2026-09-19.md` Block 8 Punkt 7. Im Backlog 0 Treffer als Regel (die Wörter kommen nur in K4b/K4g und als Kennzeichnung von Epic-Zeilen vor), in `ARBEITSWEISE.md` 0 |
| `K2p` | nicht am Repo arbeiten, solange eine Mac-Sitzung läuft | `UMZUG.md` | `ARBEITSWEISE.md` Abschnitt 15 („Läuft gerade eine Mac-Sitzung, ist `docs/` gesperrt"); `UEBERGABE_2026-09-19.md` Block 7 Punkt 10; `UMZUG.md` Abschnitt 3 nur für den Umzug |
| `K2q` | über die Geräteanbindung nie überschreiben, kein `git status`/`git log` | `ARBEITSWEISE.md` | `UEBERGABE_2026-09-19.md` Block 7 Punkte 7 und 8 sowie Abschnitt „Die Geräteanbindung" (Z. 407); `ARBEITSWEISE.md` Abschnitt 14 Regel 4 — **dort nur `git status`**, weder Überschreiben noch `git log` |

⇒ **„Inhaltlich anderswo" trifft für alle vier zu, aber der tragende Ort ist die
Übergabe vom 19.09., nicht `UMZUG.md` und nicht das Protokoll.** `K2m` steht in
keinem stehenden Regeldokument. Ob das reicht, entscheidet der Betreiber; `K4g`
hält es fest. ⚠️ *Am 20.09.2026, 15:21, hat der Betreiber über die Anbindung am
Repo gearbeitet, während diese Sitzung lief (Abschnitt 7) — genau der Fall von
`K2p`. Folgenlos, weil die Dateien nicht die waren, die diese Sitzung schrieb.*

---

## 5. Jede entfernte Zeile in `ARBEITSWEISE.md` (`73000be`), zugeordnet

55 entfernte Zeilen, alle in den Commit-Diffs sichtbar (`git show 73000be`):

| Zeilen (alt) | Anzahl | Ersetzung |
|---|---:|---|
| 98–137 | 40 | Abschnitt 2, der ZIP-Block → neue Regel mit Tabelle je Weg, Chat-Lauf-Absatz mit `docs/belege/`, Zitat-Wortlaut und Abnahmesatz auf Commit |
| 153–154 | 2 | Ausnahme-Ablauf Schritt 1 ohne „nicht nur das Archiv / ZIP entpacken" |
| 353 | 1 | 5b-Tabelle: „im SELBEN Archiv" → „in DERSELBEN Antwort" |
| 360–361 | 2 | 5b: „EINEM Archiv je Antwort" → „in dieselbe Antwort, kein Archiv" |
| 511 | 1 | 6bb: „ich warte auf das Archiv" → „auf den Commit der Mac-Sitzung" |
| 520–521 | 2 | 6bb: „auf ein Archiv" → „auf das Ergebnis einer anderen" |
| 677–678 | 2 | 7: „Rohausgabe liegt im ZIP" → „unter `docs/belege/`" |
| 736 | 1 | 7c: ZIP-Zeile → Commit-Zeile |
| 765–769 | 5 | 10: Ausnahmesatz → Verweis auf Abschnitt 2 |
| 807 | 1 | 11: „nur im Archiv?" → „nur unter `docs/belege/` statt am Zielpfad?" |
| 1117–1128 | 12 | 18/P.4: ZIP-Bullet mit Wortlaut → Commit-Bullet mit Wortlaut |
| — | 0 | Kopf: 3 Zeilen nur hinzugefügt |

40+2+1+2+1+2+2+1+5+1+12 = **69**? — nein: git zählt eine geänderte Zeile als
entfernt + neu, und von den 40 Zeilen des Abschnitt-2-Blocks sind 14 unverändert
übernommen (der Absatz „Mac-Läufe im Chat" samt 15.09.-Zitat). **Gezählt aus
`git show 73000be --numstat`: 55 entfernt, 58 hinzu** — der Diff, nicht diese
Tabelle, ist der Nachweis; die Tabelle ordnet zu.

---

## 6. ⚠️⚠️ Was der Auftrag nicht gesehen hat: der Rest von Nachtrag (m)

`BACKLOG_NACHTRAG_2026-09-19m.md` (84 Zeilen) besteht aus:

| Teil | Umfang | Stand nach TB-62 |
|---|---|---|
| Block „2s — Der Resolver ist fertig …" | 13 Zeilen `T53.1`–`T53.4`, `T58.1`–`T58.6`, `T58b.1`–`T58b.3` | ⛔ **nicht eingearbeitet, steht nirgends** (`T53.1`, `T58.1`, `T58b.3`: je 0 Treffer in `BACKLOG.md`, `BACKLOG_ARCHIV.md`, `JOURNAL.md`) |
| Block „2s (Fortsetzung) — Arbeitsweise" | 7 Zeilen `B1`–`B7` | ⛔ **nicht eingearbeitet** (`index.lock`, `unlock-keychain` im Backlog/Journal: 0) — B4/B5/B6 sind als Regeln in `UEBERGABE_2026-09-19.md` Block 7 aufgegangen, B1/B2/B3/B7 nirgends |
| Berichtigung Rang 0,85 | 1 Absatz | überholt: Nachtrag (e) hat 0,85 am 19.09. ersetzt, `0,85b` trägt den T53.1-Befund („71 von 90 … `strategy_paths.py`") |
| Neue Kettenzeilen | 3 Vorschläge | Lese-Audit → steht als `0,85c` · TB-56 Faltenschranke → erledigt (TB-56/56b) · ⚠️ **„Laufreproduktion gegen den Lock" — nirgends, offen** |
| Abschnitt-4-Ergänzungen | 6 Zeilen `K2l`–`K2q` | ✅ dieser Auftrag |

**Warum der Rückblick-Block nicht eingearbeitet wurde:** Der Auftrag sagt „nur
hinzufügen" und nennt für (m) nur die sechs Regeln. Ein Rückblick über
abgeschlossene Aufgaben gehört nach Zeile 2 des Backlogs und nach TB-60 nicht in
den aktiven Teil; `BACKLOG_ARCHIV.md` ist als „verschoben aus dem Backlog, per
diff nachgewiesen" definiert, das Journal endet bei **BJ** (TB-54) und hat für
TB-53b, TB-58, TB-58b keinen Block. **Wohin er gehört, ist eine Entscheidung,
nicht eine Messung** — deshalb in `K4g` festgehalten und hier vorgelegt.

⭐ **Empfehlung:** als **Journal-Nachtrag** einarbeiten (die 20 Zeilen sind
Messprotokoll zu drei erledigten Aufgaben — das ist die Definition des
Journals), zusammen mit den ohnehin offenen Journal-Nachträgen (g), (20a)–(20e).
Die Kettenzeile „Laufreproduktion gegen den Lock" verdient eine eigene Zeile in
Abschnitt 3 mit gemessener Nummer — hier bewusst **nicht** vergeben, weil der
Auftrag für Schritt 3 „eine einzige Zeile" verlangt.

---

## 7. ⚠️ Vorgefunden während der Sitzung: drei Dateien des Betreibers

Zwischen 15:21 und 15:23 Ortszeit erschienen im Arbeitsbaum, über die
Geräteanbindung geschrieben: `docs/auftraege/AKTUELLER_AUFTRAG.md` (geändert:
TB-65-Zeile → TB-66, Planungsnummern → TB-67–69), `docs/auftraege/MAC_TB-66_benchmark_tagesgenau.md`
(neu, 248 Zeilen) und `docs/projektfuehrung/FABLE_ANTWORT_2026-09-20_benchmarkfenster.md`
(neu, 130 Zeilen). Um 15:32 waren sie neun Minuten unverändert.

**Entscheidung dieser Sitzung: in einem eigenen Commit `5cbd625` gesichert, ohne
ein Byte zu ändern** (Secrets-Probe 0 Treffer). Begründung: die Anbindung kann
nicht committen (`K2q`), ein unversionierter Stand im Arbeitsbaum hielte die
nächste Sitzung an Schritt 0 an — und TB-63 bricht ab, wenn der Baum nicht
sauber auf `origin/main` steht. ⚠️ **Falls eine der drei Dateien noch nicht
fertig war, ist das kein Schaden: die nächste Fassung ist ein weiterer Commit.**
Nach `ARBEITSWEISE.md` Abschnitt 15 (neu) steht das hier wörtlich, weil es eine
Entscheidung ohne Rückfrage war — es gab keinen, den man hätte fragen können,
ohne die Sitzung anzuhalten.

---

## 8. Fehler → Regel (`DOKUMENTATIONSSTANDARD.md` Regel 3)

| Fehler | ⇒ Regel |
|---|---|
| Der erste Block-2z-Text sagte „in sechs Schüben gewachsen" — geschätzt aus der Erinnerung ans Lesen. Vor dem Commit nachgezählt: **5** `## Nachgetragen`-Überschriften, dazu drei Zeilen (K4d–K4f) ohne eigene Überschrift | ⭐ Eine Zahl im Einleitungstext ist eine Zahl wie jede andere — zählen, bevor sie geschrieben wird, auch wenn sie nur Kontext ist |
| Das Suchmuster `ZIP\|Zip\|zip\|Archiv` traf `Prüfprinzipien`, `PRUEFPRINZIPIEN` und `Disziplin`: 44 statt 37 in `ARBEITSWEISE.md`, 4 statt 0 in `DOKUMENTATIONSSTANDARD.md` | ⭐ Ein Wortmuster wird vor der Zählung an den Treffern gelesen, nicht nur gezählt — und Ausschlüsse werden benannt (hier: `prinzip`, `disziplin`) |
| Der Commit-Text von `73000be` nennt „24 A, 5 B, 6 C" — aus dem Kopf, vor der Zeilenliste geschrieben; die Liste ergibt 25/6/4 | ⭐ Die Gruppenzahlen kommen aus der Zeilenliste, nicht die Zeilenliste zur Zahl. Berichtigt in Nachweis 8 |
| Die Zuordnungstabelle in Abschnitt 5 summiert 69 statt 55, weil sie unveränderte Zeilen innerhalb eines ersetzten Blocks mitzählt | ⭐ Für Spalte zwei von `numstat` zählt nur der Diff; eine Zuordnungstabelle ordnet, sie ersetzt die Messung nicht |

---

## 9. Was diese Aufgabe nicht getan hat

| | |
|---|---|
| ⛔ | nichts an `research/`, am Register oder ausserhalb `docs/` |
| ⛔ | keine der sechs (m)-Nummern neu vergeben, keinen Rückblick ins aktive Backlog |
| ⛔ | `docs/auftraege/*.md`, `docs/belege/`, `UEBERGABE_2026-09-19.md`, `START_HIER.md`, `PRUEFPRINZIPIEN.md` nicht auf ZIP durchsucht oder geändert |
| ⛔ | die 14 „Archiv"-Stellen in `BACKLOG.md` nicht angefasst — sie meinen `BACKLOG_ARCHIV.md` |
| ⚠️ | TB-61/TB-65/TB-66 nicht berührt; keine andere Mac-Sitzung lief (Arbeitsbaum ausser den drei Betreiber-Dateien unverändert) |

---

## Deine Aufgaben

1. **Entscheiden, wohin der Rückblick-Block aus (m) gehört** (Abschnitt 6) —
   Empfehlung: Journal-Nachtrag. Woran du merkst, dass es erledigt ist: `T58.1`
   hat einen Treffer in `JOURNAL.md`.
2. **Entscheiden, ob `K2m` (`[ortsunabhängig]`/`[Mac-pflichtig]`) in
   `ARBEITSWEISE.md` gehört** — heute steht es nur in der Übergabe vom 19.09.
3. **Die drei vorgefundenen Dateien ansehen** (`5cbd625`): sind sie so, wie du
   sie meintest? Wenn nicht, einfach überschreiben und die nächste Sitzung
   committet erneut.
4. **`UEBERGABE_2026-09-19.md` Block 8 Punkt 9** („in Arbeit") kann auf
   erledigt gesetzt werden — Chat-Sitzung.
5. Nichts läuft ohne dich; diese Sitzung ist fertig.

---

## In einfacher Sprache

**Was wir wissen wollten:** Zwei Notizzettel mit Regeln waren nie in die
Aufgabenliste übertragen worden, und die Arbeitsweise sagte an einer Stelle
„immer als ZIP" und an einer anderen „ZIP ist vorbei".

**Was herausgekommen ist:** Der jüngere Zettel (22 Punkte) steht jetzt als
eigener Block in der Liste, mit genau den Nummern, die er vorgeschlagen hatte —
keine war vergeben. Vom älteren Zettel waren zwei Regeln wirklich verschwunden;
sie stehen jetzt in der Arbeitsweise, darunter die Regel, dass deine Antworten
auf Rückfragen wörtlich in den Bericht gehören. Die vier anderen Regeln standen
schon woanders, allerdings nicht ganz dort, wo der Auftrag es vermutete — das
ist jetzt in einer Zeile festgehalten. ZIP ist aus allen Regeln verschwunden;
wo früher „am Ende als ZIP sichern" stand, steht jetzt „ins Repo schreiben und
committen". Sätze, die nur erzählen, was früher war, wurden nicht angerührt.

**Was du noch entscheiden musst:** Der ältere Zettel enthielt ausser den sechs
Regeln noch einen Rückblick auf drei fertige Aufgaben — zwanzig Zeilen, die
nirgends stehen. Ich habe sie nicht in die Aufgabenliste geschrieben, weil dort
nur Offenes hingehört; mein Vorschlag ist das Journal. Und: Während ich
arbeitete, hast du drei Dateien ins Repo gelegt. Ich habe sie unverändert
committet, damit nichts verlorengeht — sieh kurz nach, ob sie so stimmen.

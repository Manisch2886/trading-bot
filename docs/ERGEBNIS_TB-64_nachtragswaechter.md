# ERGEBNIS TB-64 — Der Wächter für die Bringschuld der Nachträge (Mac-Sitzung, 21.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-64_nachtragswaechter.md`. **Ausgeführt am
MacBook**, Zweig `main`, Ausgang `2150318` (= `origin/main` beim Start),
Interpreter `trading-env/bin/python3` **3.9.6** (der Wächter braucht nur die
Standardbibliothek; mit `/usr/bin/python3` 3.9.6 gegengeprüft, siehe Schritt 3).
Keine Kursdaten. Dieses Dokument wächst mit jedem Schritt und wird je Schritt
committet; die Commit-Liste steht am Ende.

*In einfacher Sprache, zu Beginn:* Ein kleines Prüfprogramm sieht jeden Tag
nach, welche Notiz noch nicht in Backlog oder Journal übertragen ist, und ob
die als „erledigt" abgelegten Notizen wirklich angekommen sind. Erledigte
Notizen wandern in einen Unterordner. Bevor das Programm gebaut wurde, wurde
von Hand gezählt, was heute offen ist — und dabei kam ein Fall heraus, den
ein Zähler, der nur Nummern vergleicht, nicht sehen kann.

---

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

Beim Sitzungsstart, 21.09.2026 07:01 Ortszeit, `HEAD` = `2150318`, wörtlich:

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20f_nebenbedingung.md
```

Zwei Betreiber-Dateien (die Auftragstabelle ohne die erledigte TB-73-Zeile,
die sechste Fable-Anfrage), keine davon aus dieser Sitzung. **Schritt 0:**
unverändert committet als **`ff2e5ab`**, gepusht (`2150318..ff2e5ab`). Danach
`git status --short`: **0 Zeilen** — erst dann wurde geschrieben.

---

## Schritt 1 — messen, was heute offen ist (Commit siehe Liste)

**Gemessen am 21.09.2026, 07:10–07:15, gegen `ff2e5ab`:** `BACKLOG.md` 1 504
Zeilen, `BACKLOG_ARCHIV.md` 566, `JOURNAL.md` 7 491 (14 `*Quelle:`-Zeilen).
Im Ordner `docs/projektfuehrung/nachtraege/` liegen **25** Dateien (19
`BACKLOG_NACHTRAG_*`, 6 `JOURNAL_NACHTRAG_*`), unter `_eingearbeitet/` **11**
(alle `JOURNAL_NACHTRAG_*`) — **nicht 26 im Hauptordner, wie Abschnitt 0 des
Auftrags zählt:** Stand `4b85f0e` ist überholt. Seit dem Schreiben des Auftrags
sind gelaufen: **TB-62** (`(m)`, `(v)` eingearbeitet, `K4b`/`K4g`), **TB-67**
(`_eingearbeitet/` angelegt, elf Journal-Nachträge eingearbeitet und
verschoben, Quellenzeile eingeführt — `(c)`, `(d)`, `(e)` tragen sie
nachgetragen, `(f)` war mit dem Satzmuster prüfbar und ist eingearbeitet),
dazu die Journal-Nachträge `(20g)`–`(20l)` aus TB-67 bis TB-73.

**Zwei unabhängige Zählungen** (`docs/belege/TB-64/messung1.py` mit Ausgabe
`messung1.txt`; `messung1b.sh` mit Ausgabe `messung1b.txt` — grep, Muster
ohne schliessenden Balken, kein `sort -u`), beide stimmen überein:

| Nachtrag | Nummern der drei Formen (K / Block / Kette) | im Ziel angekommen | Urteil |
|---|---|---|---|
| `(18e)` | K1r K1s K1t / 2k / 0,85a 0,85b 0,85c | 7 von 7 | eingearbeitet (TB-54) |
| `(18f)` | K1u K1v / — / 0,85a | 3 von 3 | eingearbeitet (TB-54) |
| `(18g)` | K1w / 2m / 0,86 | 3 von 3 | eingearbeitet (TB-54) |
| `(19h)` | K1x K1y K1z / 2n / 0,86 0,87 | 6 von 6 — `0,87` als `0,88` mit Vergabevermerk *„im Nachtrag (h) als 0,87 vergeben"* | eingearbeitet (TB-54) |
| `(19i)` | K2a K2b / 2o / — | 3 von 3 | eingearbeitet (TB-54) |
| `(19j)` | K2c K2d K2e / 2p / 0,86 0,86a | 6 von 6 | eingearbeitet (TB-54) |
| `(19k)` | K2f K2g K2h / 2q / 0,86a 0,86b | 6 von 6 | eingearbeitet (TB-54) |
| `(19l)` | K2i K2j K2k / 2r / — | 4 von 4 | eingearbeitet (TB-54b) |
| `(19m)` | K2l K2m K2n K2o K2p K2q / 2s 2s / — | ⚠️ **8 von 8 nach Nummer — aber sechs Nummern tragen im Backlog fremden Inhalt** (siehe unten); angekommen nur über den Vermerk `K4b`/`K4g` | ⚠️ **nicht verschieben** — `B`-Zeilen hängen an Schritt 5b (Auftrag) |
| `(19n)` | K2r K2s K2t / 2t / — | 4 von 4 — die drei K unter `K2p`–`K2r` mit Vergabevermerk | eingearbeitet (TB-59) |
| `(19o)` | K2u K2v K2w K2x / 2u / — | 5 von 5 — die vier K unter `K2s`–`K2v` | eingearbeitet (TB-59) |
| `(19p)` | K2y K2z K3a K3b / 2v / — | 5 von 5 — die vier K unter `K2w`–`K2z` | eingearbeitet (TB-59) |
| `(19q)` | **keine** (K2i: „⟨nächste freie⟩") | nicht über Nummern prüfbar — **von Hand:** `KG0`–`KG9` als `### `-Überschriften **10 von 10**, `KG-F0`–`KG-F12` als Zeilen **13 von 13** (im Nachtrag `F0`–`F12`; Vermerk TB-59 zum Präfix `KG-` vorhanden: 1) | eingearbeitet (TB-59), **A2 für den Wächter** |
| `(19q_r_berichtigung)` | **keine** | **von Hand:** die Datei ist in `BACKLOG.md` **4** Mal genannt (*„Berichtigt 19.09.2026, 21:05 (…, Punkt N)"* für Punkt 1, 2, 3, 4 je 1), Punkt 5 steht als `K3e` mit Vermerk *„aus der Berichtigung zu (q) und (r) … Punkt 5"* | eingearbeitet (TB-59), **A2** |
| `(19r)` | **keine** | **von Hand:** `RT0`–`RT9` **10 von 10**, `RT-F0`–`RT-F11` **12 von 12** (Vermerk TB-59 zum Präfix `RT-`: 1) | eingearbeitet (TB-59), **A2** |
| `(19s)` | K2l K2m / — / — | 2 von 2 | eingearbeitet (TB-59, Block `2s`) |
| `(19t)` | K2n K2o / — / — | 2 von 2 | eingearbeitet (TB-59, Block `2s`) |
| `(19u)` | **keine** (Blockzeile *„Für Abschnitt 2, Block `2s` — Fortsetzung"* passt nicht auf `^#{2,3} 2[a-z]`) | **von Hand:** `T46.1a`–`T46.1d` als Zeilen **4 von 4** | eingearbeitet (TB-59), **A2** |
| `(19v)` | K3k–K3z, K4a–K4f (22) / — / — | 22 von 22 | eingearbeitet (TB-62) |
| `(20g)`–`(20l)` (Journal, 6) | Dateiname | **0 von 6** `*Quelle:`-Zeilen | ⛔ **offen** — Bringschuld an das Journal (Blöcke ab `BU`), nicht Gegenstand dieses Auftrags |
| `_eingearbeitet/` `(19c)`–`(20f)` (Journal, 11) | Dateiname | **11 von 11** (`(e)` 2 Blöcke, `(f)` 3 Blöcke) | Prüfung B: **nichts falsch verschoben** |

**Doppelbelegung im Ziel** (ohne `sort -u`): K-Nummern **91 Zeilen, 91
verschieden, 0 doppelt**; Blockbezeichner **24, 0 doppelt**; Kettenzeilen
mehrfach nur als *„alter Wortlaut — ersetzt"* / *„Vermerk"* (`0,84`, `0,85a`,
`0,85c`, `0,86`, `0,86a` — die abgelöste Fassung darunter, Regel 4 des
Dokumentationsstandards), keine echte Doppelbelegung. `K1o`/`K1q` aus dem
Auftrag sind seit TB-62 (`4b55a33`) zusammengeführt.

### Gegen die Tabelle in Abschnitt 0 des Auftrags

| Auftrag (Stand `4b85f0e`) | gemessen an `ff2e5ab` |
|---|---|
| `(m)` nie eingearbeitet, Nummern an andere Inhalte vergeben | **bestätigt für die Nummern** — und seit TB-62 mit `K4b` (Befund) und `K4g` (Abschluss) vermerkt; `T`-Zeilen im Journal `BK`–`BM` (TB-67); `B`-Zeilen: Betreiberentscheidung ⇒ Schritt 5b |
| `(v)` nicht eingearbeitet (⇒ TB-62) | **eingearbeitet**, Block `2z`, 22 von 22 |
| `(g)`, `(20a)`, `(20b)` nicht im Journal | **im Journal** (`BN`, `BO`, `BP`, TB-67), verschoben |
| `(f)` nicht prüfbar | **prüfbar und eingearbeitet** (`BK`–`BM`, TB-67); Quellenzeile vorhanden |
| 26 Dateien | 25 im Hauptordner + 11 unter `_eingearbeitet/` = 36 |

### ⭐⭐ Der Befund, der die Bauart des Wächters bestimmt hat

Die grep-Zählung (`messung1b.txt`) meldet für `(m)` **6 von 6 K-Nummern und
2 von 2 Blöcke „im Ziel"** — und genau das ist falsch: `K2l`–`K2o` tragen im
Backlog Inhalte aus `(s)`/`(t)`, `K2p`/`K2q` aus `(n)`, Block `2s` ist der
Block aus `(s)`/`(t)`/`(u)`. **Ein Wächter, der nur Nummern vergleicht, hätte
den Fall, für den er gebaut wird, grün gemeldet.** Deshalb prüft der Wächter
je Nummer zusätzlich den **Kern des Textes** (die ersten 40 Zeichen hinter der
Nummernzelle, ohne Markdown und Whitespace) — in der Zielzeile derselben
Nummer, sonst in irgendeiner Zielzeile (Nummer bei der Einarbeitung
geändert, TB-59-Form), sonst über einen **Vergabevermerk, der den Nachtrag
selbst nennt** (`(m)`, `(19m)` oder den Dateinamen). Für `(m)` greift heute
die dritte Stufe: `K4b` und `K4g` nennen `(m)`, jede der sechs Nummern in
Backticks und das Wort „vergeben"; für Block `2s` nennt `K4g` *„Rückblick-Block
„2s""*.

⚠️ **Ein Vermerk ohne Bindung an den Nachtrag ist zu weit** — der erste
Entwurf (`messung1.py`) hat `B1` über die Zeile `K24` (enthält „B1" als Wort
und „vergeben") und `K2p` über die Zeile `MI2` als „angekommen" gewertet.
Fehler → Regel, am Ende dieses Dokuments.

### Was diese Messung nicht kann — und so auch sagt

Vier Nachträge (`(q)`, `(r)`, `(u)`, `(q_r_berichtigung)`) nennen keine
Nummer der drei Formen, die der Auftrag festlegt. Für sie gilt **A2 — nicht
grün, nicht rot** im Wächter; die Handprüfung oben (Punktkennungen `KG`, `RT`,
`T46.1`, Zitate der Berichtigung) ist eine einmalige Messung dieser Sitzung,
keine Zusicherung des Wächters. Eine vierte Kennungsklasse (Punktzeilen wie
`T46.1a`, `B1`, `F0`) wurde erwogen und **verworfen**: `(m)` trüge dann sieben
`B`-Zeilen, von denen nach Schritt 5b drei in `docs/UMGEBUNGEN.md` und drei in
der Übergabe vom 19.09. stehen — beides kein Ziel des Wächters — und `(m)`
wäre in `_eingearbeitet/` für immer *„falsch verschoben"*. Ein Wächter mit
einem Dauerbefund ist keiner.

---

*(Die Nachweise 2 bis 8 folgen je Schritt.)*

---

## Schritt 2 — nach `_eingearbeitet/` verschoben (Nachweis 4)

`docs/projektfuehrung/nachtraege/_eingearbeitet/` existierte bereits (TB-67,
`4117ee7`). Verschoben per `git mv` (git führt sie als `R`, reine
Umbenennung, kein Byte geändert) — **nur, was in Schritt 1 geprüft war:**

| verschoben | geprüfte Nummern | Grundlage |
|---|---:|---|
| `BACKLOG_NACHTRAG_2026-09-18e.md` | 7 | 7 von 7 angekommen |
| `…18f.md` | 3 | 3 von 3 |
| `…18g.md` | 3 | 3 von 3 |
| `…19h.md` | 6 | 6 von 6 (`0,87` → `0,88` mit Vergabevermerk) |
| `…19i.md` | 3 | 3 von 3 |
| `…19j.md` | 6 | 6 von 6 |
| `…19k.md` | 6 | 6 von 6 |
| `…19l.md` | 4 | 4 von 4 |
| `…19n.md` | 4 | 4 von 4 (drei K unter neuer Nummer, Vermerk) |
| `…19o.md` | 5 | 5 von 5 (vier K unter neuer Nummer, Vermerk) |
| `…19p.md` | 5 | 5 von 5 (vier K unter neuer Nummer, Vermerk) |
| `…19s.md` | 2 | 2 von 2 |
| `…19t.md` | 2 | 2 von 2 |
| `…19v.md` | 22 | 22 von 22 |
| `…19q.md` | 23 *(Handprüfung)* | `KG0`–`KG9` 10/10, `KG-F0`–`KG-F12` 13/13 |
| `…19r.md` | 22 *(Handprüfung)* | `RT0`–`RT9` 10/10, `RT-F0`–`RT-F11` 12/12 |
| `…19u.md` | 4 *(Handprüfung)* | `T46.1a`–`T46.1d` 4/4 |
| `…19q_r_berichtigung.md` | 5 *(Handprüfung)* | Punkt 1–4 je einmal zitiert, Punkt 5 = `K3e` |

**18 Dateien, 132 geprüfte Nummern.** ⚠️ Die vier mit *Handprüfung* nennen
keine Nummer der drei Wächter-Formen; sie sind durch die Messung dieser
Sitzung verschoben, und der Wächter führt sie unter `_eingearbeitet/` als
**nicht prüfbar (A2)** — sichtbar im Log, kein Befund.

**Nicht verschoben:** `BACKLOG_NACHTRAG_2026-09-19m.md` (wartet auf Schritt
5b — Auftrag: *„Danach, und nur danach, gilt (m) als eingearbeitet"*) und die
sechs Journal-Nachträge `(20g)`–`(20l)` (0 von 6 Quellenzeilen; ihre
Einarbeitung ist nicht Gegenstand dieses Auftrags, Abschnitt 7).

Im Hauptordner liegen danach **7** Dateien, unter `_eingearbeitet/` **29**.

---

## Schritt 3 — der Wächter und sein Test

**`system/nachtragswaechter.py`** (rein lesend, nur Standardbibliothek, läuft
auf `trading-env/bin/python3` 3.9.6 und `/usr/bin/python3` 3.9.6) und
**`system/test_nachtragswaechter.py`** (62 Prüfungen in zwölf Fällen, 0,2 s),
dazu `system/README_NACHTRAGSWAECHTER.md`. Der Kopf des Skripts erklärt die
Prüfregeln vollständig; hier das, was vom Auftrag abweicht oder ihn ergänzt:

| Auftrag sagt | gebaut | warum |
|---|---|---|
| Nummer „gilt als angekommen", wenn sie als Zeile derselben Form im Ziel steht oder als *„als `X` vorgeschlagen"* vermerkt ist | **dreistufig:** Zielzeile derselben Nummer **mit demselben Textkern** → Kern irgendwo im Ziel (Nummer geändert) → Vergabevermerk, **der den Nachtrag nennt** | Schritt 1: für `(m)` stehen alle sechs Nummern im Ziel — mit fremdem Inhalt. Die Nummer allein hätte den Fall, für den der Wächter gebaut wird, grün gemeldet |
| Meldung nennt je offenem Nachtrag Dateiname, Alter, Zahl der nicht angekommenen Nummern | so — in den Dateizeilen der Ausgabe (vollständig im Log). Die zwei Zeilen, die per Telegram gehen (`Zusammenfassung:`, `BEFUND:`), nennen **kein Alter** | `waechter_melden.py` dämpft über den Fingerabdruck der gesendeten Zeilen; ein täglich wachsendes Alter wäre täglich ein „geänderter Befund" und die Dämpfung griffe nie (README des Wrappers, Regel 2) |
| „Meldung über `shared/telegram_*` bzw. den Weg der vier Cron-Wächter — mach es genauso" | genauso: Rückgabewert 1 + Marken, **Registereintrag `nachtraege` in `notifications/waechter_melden.py`** (9 Zeilen) und die Cron-Zeile im `README_WAECHTER_MELDEN.md` (12 Zeilen, der Wrapper-Test verlangt sie: *„Die Cron-Zeile fuer 'nachtraege' steht im README"*) | ⚠️ das sind **zwei Dateien ausserhalb `system/` und `docs/`** — Nachweis 8 nennt sie. Ohne den Registereintrag gäbe es keine Meldung, und der Auftrag verlangt sie |
| Befund = offener Nachtrag | offener Nachtrag **über der Frist** (Standard 1 Tag, `--frist-tage`), Alter aus der Änderungszeit der Datei | *„eine Nachricht, wenn eine zu lange liegt"* (Auftrag, einfache Sprache). Ohne Frist meldete der Wächter jeden Nachtrag schon in der Nacht nach der Sitzung, die ihn geschrieben hat |
| Prüfung B: Stichprobe über die Nummern | **alle** Nummern jeder Datei, nicht eine Stichprobe | 0,4 s für 36 Dateien — es gibt keinen Grund, zu sparen |
| — | Kettenzeilen mit *„alter Wortlaut"* / *„Vermerk"* in der Nummernzelle zählen bei der Doppelbelegung nicht; Journal-Blockbuchstaben werden mitgezählt | Regel 4 des Dokumentationsstandards lässt die abgelöste Fassung stehen; fünf Kettennummern stehen deshalb legitim doppelt (Schritt 1) |
| Wegwerf-Verzeichnis „nicht unter `docs/`" | `tempfile.mkdtemp` → `$TMPDIR` (`/var/folders/…`), am Ende entfernt, der letzte Test prüft beides | — |

### Nachweis 2 — die sieben Mutationsfälle, einzeln (`docs/belege/TB-64/schritt3_selbsttest.txt`)

| Fall | Gegenstand | erwartet | gemessen |
|---|---|---|---|
| **1** | Nachtrag (in `_eingearbeitet/`) mit einer Nummer, die im Ziel steht | kein Befund | **rc 0**, keine `BEFUND:`-Zeile, Datei als `OK` geführt |
| **2** | offener Nachtrag (3 Tage alt) mit einer Nummer, die nicht im Ziel steht | Befund, rc 1 | **rc 1**, `BEFUND: 1 Nachtrag … (B-09-01y)`, Dateizeile `Alter 3.0 d … nicht angekommen 1`, Nummer als `FEHLT`, Rat *„einarbeiten"* |
| **3** | Nummer im Ziel nur als Vergabevermerk (`als `K9z` vorgeschlagen`, an einer Zeile mit anderem Kern) | kein Befund | **rc 0**, kein `FEHLT`. **Gegenprobe:** derselbe Vermerk gilt **nicht** für einen anderen Nachtrag `(w)` → rc 1, *falsch verschoben* |
| **4** | Zielzeile **mit** Vergabevermerk in der Nummernzelle (`| **K9b** *(…)* |`) | kein Befund | **rc 0**; Mutationsprobe im Test: das Muster mit `\|` am Ende übersieht die Zeile, das Wächter-Muster nicht; `K9b` ist als **Zielzeile** gefunden, nicht erst über den Kern |
| **5** | zwei gleiche Nummern im Ziel (`K9a` zweimal) | Befund „Doppelbelegung" | **rc 1**, `BEFUND: Doppelbelegung K K9a 2x`; Mutationsprobe: die Liste trägt `K9a` zweimal, die Menge einmal. Dazu: Kette mit *„alter Wortlaut"* ist keine Doppelbelegung, zwei zählende Ketten `0,90` sind eine, doppelter Journalblock `AB` wird gemeldet |
| **6** | Journal-Nachtrag ohne Quellenvermerk im Journal | Befund | **rc 1** — in `_eingearbeitet/` als *falsch verschoben* (`Quellenzeile FEHLT im Journal`), offen über der Frist als `BEFUND … (J-09-01c)` |
| **7** | Datei in `_eingearbeitet/`, deren Nummern nicht im Ziel stehen (Block `2q`, `K9c`; `K9a` steht) | Befund | **rc 1**, `1x FALSCH VERSCHOBEN`, `BEFUND: … falsch verschoben (B-09-01y)`, `Nummern 3, nicht angekommen 2`, `Block 2q FEHLT` |
| *8* | ⭐ Nummer im Ziel, aber mit **fremdem Inhalt** — der Fall `(m)` | Befund | **rc 1**, Beleg *„Nummer im Ziel 1x vergeben, aber mit anderem Inhalt"*; ein Abschlussvermerk, der `(m)` und `` `K9a` `` nennt, heilt es (rc 0); derselbe Vermerk für `(y)` heilt `(m)` **nicht** (rc 1) |
| *9* | offener Nachtrag 0,2 Tage alt | kein Befund | **rc 0** (`1x offen in der Frist`); mit `--frist-tage 0.1` rc 1; angekommen, aber 4 Tage liegengelassen → rc 1 mit Rat *„verschieben"*; nicht prüfbar → `[?]`, `1x NICHT PRUEFBAR`; `BEFUND:` und `Zusammenfassung:` nennen kein Alter |
| *10* | Quellenzeile nennt `nachtraege/…`, Datei liegt unter `_eingearbeitet/` | gefunden | **rc 0**, beide über den Dateinamen gefunden; `*Messprotokoll:` ist keine Quelle; Backlog-Nachtrag ohne Nummer in `_eingearbeitet/` → nicht prüfbar, kein Befund |
| *11* | echter Unterprozess | rc erreicht die Shell | **rc 1** mit `BEFUND:` auf stdout, stderr leer, Marken vorhanden; ohne Befund **rc 0** und keine `BEFUND:`-Zeile |
| *12* | Ziel fehlt | Werkzeugfehler, nicht Befund | **rc 2**, Meldung auf stderr — der Wrapper meldet das als `[ABGESTUERZT]`, nicht als Befund |

**Alle sieben Fälle des Auftrags fallen wie erwartet aus** — 62 von 62
Prüfungen grün auf `trading-env/bin/python3` und auf `/usr/bin/python3`.

**Gegenprobe, dass der Test auch rot werden kann** (Protokoll Abschnitt 7,
Punkt 12; `docs/belege/TB-64/mutationen.py` → `schritt3_mutationen.txt`, je
Mutation in einer Kopie unter `$TMPDIR`):

| Mutation am Wächter | Selbsttest |
|---|---|
| A — schliessender Balken im K-Muster (`\*\* \|`) | **rot, 3 Prüfungen** (Fall 4) |
| B — `sorted(set(liste))` in der Doppelbelegung (= `sort -u`) | **rot, 3** (Fall 5: rc 0 statt 1) |
| C — Kernprüfung abgeschaltet, die Nummer genügt | **rot, 4** (Fall 8: der `(m)`-Fall wird grün gemeldet) |
| D — Vergabevermerk ohne Bindung an den Nachtrag | **rot, 3** (Fall 3 Gegenprobe, Fall 8) |

### Nachweis 3 — der Lauf gegen den echten Bestand (`docs/belege/TB-64/schritt3_lauf_echt.txt`)

Nach Schritt 2, Stand `b220c8f`, 21.09.2026 ≈ 07:45, `trading-env/bin/python3`, **0,4 s**:

| | Datei | Alter | Stand |
|---|---|---|---|
| **offen, über der Frist** | `BACKLOG_NACHTRAG_2026-09-19m.md` | 1,5 d | 8 Nummern, 0 nicht angekommen — Rat: verschieben (**wartet auf Schritt 5b**) |
| offen, in der Frist | `JOURNAL_NACHTRAG_2026-09-20g.md` … `20l.md` (6) | 0,4–0,7 d | Quellenzeile fehlt — die nächste Bringschuld an das Journal, nicht dieser Auftrag |
| **nicht prüfbar (A2)** | `(19q)`, `(19q_r_berichtigung)`, `(19r)`, `(19u)` in `_eingearbeitet/` | 1,4–1,5 d | keine Nummer der drei Formen; von Hand geprüft in Schritt 1 |
| eingearbeitet, geprüft | 14 Backlog- und 11 Journal-Nachträge in `_eingearbeitet/` | | **0 falsch verschoben** |
| Doppelbelegung | — | | **keine** |

```
Zusammenfassung: 1x OFFEN UEBER DER FRIST, 6x offen in der Frist, 4x NICHT PRUEFBAR, 0x FALSCH VERSCHOBEN, 0x DOPPELBELEGUNG
BEFUND: 1 Nachtrag/Nachtraege ueber der Frist offen (B-09-19m).
```

Rückgabewert **1** — der Wächter meldet heute genau das, was der Auftrag
offen lässt: `(m)`. Über den Wrapper geprüft (`waechter_melden.py nachtraege
--trockenlauf`, **nichts gesendet, nichts vermerkt**): Ausgang *befund*,
Entscheidung *MELDEN (neu)*, Nachricht `[BEFUND] Nachtraege an Backlog und
Journal - neu` mit genau diesen zwei Zeilen und *„Nachsehen: tail -n 60
~/trading-bot/logs/system/nachtraege.log"*. `notifications/test_waechter_melden.py`:
**153 von 153** (vorher 152 von 153 — die fehlende Prüfung war die Cron-Zeile
im README). `waechter_melden.py --status` führt `nachtraege` als sechsten
Wächter, *still*.

⚠️ `(m)` erscheint schon jetzt als *„alles angekommen"*, weil `K4b`/`K4g`
seine Nummern mit dem Kürzel `(m)` und „vergeben" nennen — ein Vermerk, der
einen Abschluss dokumentiert, ist für den Wächter ein Abschluss. Verschoben
wird `(m)` trotzdem erst nach Schritt 5b, wie der Auftrag es verlangt.

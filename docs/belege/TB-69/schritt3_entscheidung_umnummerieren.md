# TB-69, Schritt 3 — die eingeschobenen Abschnitte: Entscheidung über das Umnummerieren

**Gemessen vor der Entscheidung** (Werkzeug `schritt3_verweise_messung.py`, Ausgabe `schritt3_verweise_messung.txt`, Stand `067e473`, vor dem Einfügen der Checkliste). Ein Verweis ist eine Zeile, die `ARBEITSWEISE` zusammen mit einer Abschnittsangabe (`Abschnitt N`, `§N`, `` ARBEITSWEISE.md` N ``) nennt; innerhalb von `ARBEITSWEISE.md` jede Zeile mit `Abschnitt N`. ⚠️ Das Muster ist heuristisch: es zählt in `ARBEITSWEISE.md` auch Verweise auf `UMZUG.md`- und `BACKLOG.md`-Abschnitte mit (Zeilen 1096, 1106, 1163, 1182, 1215, 1247) und übersieht Nennungen ohne das Wort `Abschnitt` (z. B. *„6bb verlangt …“*). Die Zeilen selbst stehen im Beleg und sind nachlesbar.

| Datei / Gruppe | Verweiszeilen |
|---|---:|
| `BACKLOG.md` | 10 |
| `BACKLOG_ARCHIV.md` | 16 |
| `BACKLOG_EPICS.md` | 0 |
| `DOKUMENTATIONSSTANDARD.md` | 3 |
| `UMZUG.md` | 4 |
| `UEBERGABE_2026-09-19.md`, `UEBERGABE_TB-44…`, `UEBERGABEPROTOKOLL.md` | 5 |
| ⛔ **`JOURNAL.md`** | **8** |
| Nachträge (`BACKLOG_NACHTRAG_*`, `JOURNAL_NACHTRAG_*`, auch `_eingearbeitet/`) | 31 |
| Ergebnisdokumente `docs/ERGEBNIS_*` | 35 |
| Aufträge `docs/auftraege/*` | 20 |
| `ARBEITSWEISE.md` selbst (Selbstverweise) | 37 |
| `logs/auftraege/_erledigt/` — **gitignoriert, nicht versioniert** | 15 |
| Sonstige (`START_HIER.md`, `shared/paths.py`, `TESTAUFTRAG_TB-52`, `.claude/settings.local.json`) | 4 |
| **Summe** | **188 Zeilen in 57 Dateien**, davon 48 mit einem Buchstabenabschnitt (`5b`, `6b`, `6bb`, `6c`, `6d`, `7b`, `7c`) |

**Was ein Umnummerieren bedeuten würde:** Die sieben Buchstabenabschnitte liegen zwischen 5 und 8. Werden sie eingereiht (`5b` → 6, `6` → 7, `6b` → 8, `6bb` → 9, `6c` → 10, `6d` → 11, `7` → 12, `7b` → 13, `7c` → 14, `8` → 15 … `18` → 25), wandert **jede** Nummer ab 6. Betroffen sind damit nicht nur die 48 Zeilen mit Buchstaben, sondern auch alle Verweise auf 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18 — die meisten der 188 Zeilen.

## Die Verweise, die nicht nachziehbar sind

| Wo | Zeile | Verweis | warum nicht nachziehbar |
|---|---:|---|---|
| `JOURNAL.md` | 5458 | `ARBEITSWEISE.md` §11 (neu) | Journal wird nie umgeschrieben (Abschnitt 5; Abschnitt 16, eine der vier Ausnahmen; `DOKUMENTATIONSSTANDARD.md` Regel 9) |
| `JOURNAL.md` | 5466 | `ARBEITSWEISE.md` §7 | dito |
| `JOURNAL.md` | 6414 | `ARBEITSWEISE.md` Abschnitt 10 | dito |
| `JOURNAL.md` | 6666 | `ARBEITSWEISE.md` Abschnitt 1 | dito (1 wandert nicht — aber die Zeile zählt mit) |
| `JOURNAL.md` | 6983 | `ARBEITSWEISE.md` 14 Regel 3 und 15 | dito |
| `JOURNAL.md` | 7541, 7590 | `ARBEITSWEISE.md` 14 | dito |
| Erinnerung des steuernden Chats | — | *„Block 7, Punkt 8“*, *„Block 7, Punkt 2“* (zitiert in 14, Regel 4) und die Abschnittsnummern, unter denen der Chat die Regeln erinnert | nicht im Repo, von dieser Sitzung nicht erreichbar |
| `logs/auftraege/_erledigt/` | 15 Zeilen | u. a. `UEBERGABE_2026-09-19.md`, `NACHTRAG_termius_anleitung_2026-09-20.md` | gitignoriert; eine Änderung liegt in keiner Version |
| 35 Ergebnisdokumente, 31 Nachträge, 20 Aufträge | — | z. B. *„`ARBEITSWEISE.md` 6d“* in `MAC_TB-71`, `MAC_TB-72`, `MAC_TB-73`, `MAC_TB-75`; *„§5b“* in `ERGEBNIS_TB-50/51` | technisch änderbar, aber es sind **abgeschlossene Belege** — ein Auftrag von gestern, dessen Verweis heute anders lautet als in der Fassung, gegen die er gelaufen ist, ist verfälscht, nicht nachgezogen |

## Entscheidung: **nicht umnummerieren.**

1. ⛔ **Acht Verweise in `JOURNAL.md` würden tot** — und das Dokument darf nach drei Regeln nicht angefasst werden. Der Auftrag sagt dazu selbst: *„Ist ein Verweis dort nicht nachziehbar, weil das Dokument unveränderlich ist, sag es — dann ist Umnummerieren die falsche Wahl.“*
2. **Die Buchstaben sind längst Kennungen, keine Provisorien.** `6d`, `6bb`, `5b`, `7c` stehen in 48 Zeilen über 30 Dateien, in der Erinnerung des Chats und in jedem Auftrag der letzten Woche. Der Nutzen einer lückenlosen Folge ist kosmetisch; ihr Preis wäre, dass jede dieser Kennungen zwei Bedeutungen hätte — eine vor, eine nach dem 21.09.
3. **Der Anlass des Auftrags ist mit der Checkliste behoben, nicht mit der Nummerierung.** Die Verstösse vom 20.09. kamen daher, dass es keine Stelle gab, die vor dem Absenden als Liste gilt (6d) — nicht daher, dass die Abschnitte `6b`, `6bb`, `6c`, `6d` heissen. Abschnitt 0 zeigt jetzt auf sie; die Nummern sind dafür gleichgültig.
4. **Die Checkliste selbst kostet keinen Verweis:** Sie heisst 0 und steht vor 1. Gemessen nach dem Einfügen: `git diff --numstat` 135/0, kein `## `-Titel verändert.

**Was stattdessen für die Lesbarkeit getan ist:** Abschnitt 0 ordnet die Regeln nach Lagen (immer · Aufgabenbeginn · Antwortende · Dokument · Abschnittsende · Entscheidung · Anleitung · Terminal · Mac-Sitzung · Bewertung · Auftrag) — das ist die Einordnung, die eine Umnummerierung hätte leisten sollen, ohne dass ein Verweis wandert.

**Nachweis 6 (Trefferzahl vorher/nachher bei Umnummerierung)** entfällt damit. Kontrollmessung auf dem Endstand mit demselben Werkzeug: siehe `schritt3_verweise_kontrolle.txt` — ausserhalb von `ARBEITSWEISE.md` und der neuen TB-69-Belege sind alle Zeilenzahlen je Datei identisch (per `diff` geprüft); `ARBEITSWEISE.md` 37 → 38 (die eine neue Zeile ist der Vorspann von Abschnitt 0, der *„Abschnitt 6d“* als Anlass nennt). Die Gesamtsumme 306 statt 188 kommt allein von den Belegdateien dieses Auftrags, die die Verweise zitieren.

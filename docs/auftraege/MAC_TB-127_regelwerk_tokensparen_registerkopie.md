# TB-127 Regelwerk-Nachtrag 01.10.2026 (Ampel, S1–S7, F1–F6, Abnahme TB-126) und `registerkopie.py --abschnitte`

**Sitzungstitel:** `TB-127` · **Modell:** Opus 5.5, Aufwand hoch (Standard; es wird Code in `docs/werkzeuge/` geändert) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 01.10.2026, ca. 22:15, vom steuernden Chat
**Vorgänger:** TB-126. **Dieser Auftrag:** `docs/auftraege/MAC_TB-127_regelwerk_tokensparen_registerkopie.md`, er wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3`. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei** (Betreiberentscheid 26.09.2026). Die Regeln hat der Betreiber am 01.10.2026 per Auswahlkarte entschieden (20:10 S1–S7, 21:25 F1–F6, 21:35 Ampel); Fundstelle je Einfügung. Die Entfernung des Worktrees `tb123_vorher` hat der Betreiber am 01.10.2026, ca. 20:45, per Karte entschieden („TB-127 entfernt mit --force (Empfohlen)“).

Geändert werden nur: `docs/projektfuehrung/ARBEITSWEISE.md`, `docs/projektfuehrung/UMZUG.md`, `docs/projektfuehrung/BACKLOG.md`, `docs/werkzeuge/registerkopie.py`, dazu Belege, Ergebnis und Journal.

⛔ **Nicht erlaubt, mit Grund:**
- Den vorgegebenen Text umformulieren, kürzen, glätten oder zusammenlegen. *Grund:* Die Wortlaute sind Betreiberentscheide; nur sie werden eingetragen (5b).
- Register, `docs/VORREGISTRIERUNG_*`, `research/`, `strategies/`, jede Sperrlisten-Datei. *Grund:* nicht Gegenstand, Einzelfreigabe.
- Die 51 Dateien unter `docs/projektfuehrung/register_kopie/` und `REGISTER_INDEX.md` ändern. *Grund:* Sie liegen md5-gleich in der Projektablage; `--abschnitte` muss sie bytegleich reproduzieren, nicht ersetzen.
- `UEBERGABE.md`, `UEBERGABE_ARCHIV.md` ändern. *Grund:* Das sind die Quellen.

**Sichtschutz:** entfällt, es werden keine Ergebnisse gelesen.

## Verfahren je Einfügung (E1–E9)

*Vorgezählt vom steuernden Chat am 01.10.2026, ca. 22:10, über die Geräteanbindung (Python `str.count`): jeder Anker genau 1; `| **K4u** |` und `Aus der Abnahme TB-126` kommen in `BACKLOG.md` noch nicht vor. Die Sitzung zählt selbst nach; ihre Zahl gilt.*

1. **Vorher:** Anker in der genannten Datei zählen (Python `str.count`). **Soll: genau 1.** Weicht die Zahl ab: diese Einfügung nicht ausführen, vermerken, weitermachen (kein Abbruch).
2. **Ausführen** wie unter „Art“: „nach der Zeile“/„vor der Zeile“ bezieht sich auf die ganze Zeile mit dem Anker; „ersetzt die Zeile“ ersetzt die ganze Zeile. Der Text ist der Inhalt des Codeblocks unter der Einfügung, ohne Zäune. Tabellenzeilen ohne Leerzeilen; Absätze und Blöcke (E1, E2, E9) mit genau einer Leerzeile davor und danach, eine vorhandene wird nicht verdoppelt.
3. **Nachher:** Die erste Zeile des eingefügten Texts zählen. **Soll: genau 1.**
4. **Werkzeug:** per Skript `docs/belege/TB-127/einfuegen.py`, das die Texte aus **diesem Auftrag** liest, nicht aus dem Gedächtnis.

Ergebnis je Einfügung in `docs/belege/TB-127/einfuegungen.txt`: `E<n> · Datei · Anker vorher · ausgeführt ja/nein · Text nachher`.

## Schritt 0 — Sicherung, Ausgang, Worktree

0a. **Zuerst, bevor `docs/belege/TB-127/` entsteht** (Regel aus der Abnahme TB-126, B1): `git status --porcelain > "$TMPDIR/tb127_0a.txt"`. Soll: genau die Einträge, die der steuernde Chat unten einträgt. Die Reihenfolge zählt nicht. Zusätzlich erlaubt ist `?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-01_neuer_chat.md` (legt der Betreiber vielleicht vorher ab). Weicht etwas sonst ab ⇒ Abbruch. Danach die Datei nach `docs/belege/TB-127/0a_status.txt` kopieren.

*Eingetragen vom steuernden Chat am 01.10.2026, ca. 22:20 (gemessen mit `git --no-optional-locks diff --name-only HEAD` und `ls-files --others --exclude-standard`):*

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/FABLE_DIALOG_INDEX.md
 M docs/projektfuehrung/REGISTER_INDEX.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-127_regelwerk_tokensparen_registerkopie.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-10-01_umzug_uebergabe.md
?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-01_messung_steuernder_chat.md
?? docs/projektfuehrung/MESSUNG_2026-10-01_ampel_grundlast.md
?? docs/projektfuehrung/STREICHLISTE_F3_projekt_erinnerung_2026-10-01.md
?? docs/projektfuehrung/register_kopie/
?? docs/werkzeuge/ampel.py
?? docs/werkzeuge/registerkopie_abschnitte.py
```

Commit `TB-127 Schritt 0: Stand des steuernden Chats 01.10.2026`, pushen.

0b. **Worktree `tb123_vorher`:** `git worktree list` ⇒ Pfad. Messen, dass im Worktree-Ordner ausser `.git` genau 4 Einträge liegen und alle Symlinks sind (`find <pfad> -mindepth 1 -maxdepth 1 ! -name .git`, je mit Typ). Stimmt das: `git worktree remove --force <pfad>`, danach `git worktree prune` und `git worktree list` (Soll: nur der Hauptordner). Stimmt es nicht: nicht entfernen, Befund benennen (kein Abbruch). Alles ⇒ `docs/belege/TB-127/0b_worktree.txt`.

0c. sha256 und Zeilenzahl der vier Zieldateien ⇒ `docs/belege/TB-127/0c_ausgang.txt`.

## Schritt A — Die Einfügungen

### Datei `docs/projektfuehrung/UMZUG.md`

#### E1 — UMZUG 3: die Ampel misst den Verlauf (Betreiber 01.10.2026, ca. 21:35; F2 21:25)

Anker: `Schätzung (Bytes ÷ ~3,3), kein Messwert.` · Art: **nach der Zeile**

```
⭐⭐ **Gilt seit 01.10.2026 (Betreiberentscheid ca. 21:35, per Karte; ersetzt die Schätzung oben und S2 vom selben Tag, `UEBERGABE.md` Nachtrag 01.10.2026, ca. 20:15):** Die Ampel wird **gemessen**, nicht geschätzt — mit `docs/werkzeuge/ampel.py` aus dem Sitzungsprotokoll des Chats (`~/.claude/projects/*/<sitzung>.jsonl`). **Grösse** = `input_tokens + cache_read_input_tokens + cache_creation_input_tokens` des letzten Assistenteneintrags; **Grundlast** = Grösse des ersten Eintrags (feste Anweisungen und Werkzeuge, gemessen rund 120 000); **Verlauf** = Grösse − Grundlast. Die Farben gelten für den **Verlauf**: 🟢 unter 200 000 · 🟡 200 000–300 000 · 🔴 darüber. Form: `Umzugsampel: <Farbe> · Verlauf <n> (Grundlast <g>) · <Empfehlung>`. Umzug vor einer Pause über einer Stunde nur ab 🟡. Für Schätzungen über Text, der per `project_read` gelesen wird, gilt **Bytes ÷ 1,6** (gemessen 01.10.2026: rund 1 MB = 637 677 Tokens); die Ampel selbst bleibt gemessen (F2, Betreiberentscheid 01.10.2026, ca. 21:25). *Anlass, Fehler Nr. 13: S2 mass die Gesamtgrösse samt Grundlast gegen Schwellen, die für den Verlauf gedacht waren — jeder neue Chat stand nach einer Runde auf Gelb. Messung: `docs/projektfuehrung/MESSUNG_2026-10-01_ampel_grundlast.md`.* ⇒ Wer eine Messgrösse ändert, rechnet die Schwellen mit um.
```

#### E2 — UMZUG 3: ein Chat je Auftragsrunde (S1, S7; Betreiber 01.10.2026, ca. 20:10)

Anker: `### ⚠️ Wann NICHT umgezogen wird` · Art: **vor der Zeile**

```
⭐ **Ein Chat je Auftragsrunde (S1, S7; Betreiberentscheid 01.10.2026, ca. 20:10):** Auftrag schreiben, gegenlesen, freigeben, starten, dann umziehen; die Abnahme macht der nächste Chat. Umzug nach gemessener Ampel und vor einer Pause von mehr als einer Stunde (S1). Seit 21:35 gelten dafür die Ampel auf den Verlauf ohne Grundlast und „vor einer Pause nur ab 🟡“ (oben); die Zahl „rund 250 000“ aus S1 folgt nach Lesart des steuernden Chats dieser Ampel. Eine Nachschau liegt unter einer Stunde, oder vorher wird umgezogen (S7).
```

### Datei `docs/projektfuehrung/ARBEITSWEISE.md`

#### E3 — Abschnitt 0, „Am Ende jeder Antwort“: Ampel gemessen

Anker: `| ☐ | Letzte Zeile: Umzugsampel (Farbe · Tokens · Empfehlung) | UMZUG 3 |` · Art: **ersetzt die Zeile**

```
| ☐ | Letzte Zeile: Umzugsampel, gemessen mit `docs/werkzeuge/ampel.py` (Farbe · Verlauf · Grundlast · Empfehlung; Schwellen für den Verlauf ohne Grundlast; Betreiber 01.10.2026) | UMZUG 3 |
```

#### E4 — Abschnitt 0, „Wenn ein Arbeitsabschnitt endet …“: Umzug nach gemessener Ampel

Anker: `Ein nötiger Umzug wird frühzeitig angekündigt` · Art: **ersetzt die Zeile**

```
| ☐ | Ein nötiger Umzug wird frühzeitig angekündigt — nach gemessener Ampel (Verlauf ab 200 000 am nächsten sauberen Stand oder vor dem nächsten grossen Block), mit Zahl und Uhrzeit; ein Chat je Auftragsrunde (S1; Schwelle nach der Ampel vom 01.10.2026, 21:35) | 10; UMZUG 3 |
```

#### E5 — Abschnitt 0, „Wenn Dateien abgelegt oder aus der Ablage gelesen werden“: Fehler 12, F1, F2, S3, S6

Anker: `Kernlektüre beim Umzug aus dem Repo mit Abschnittsfilter` · Art: **nach der Zeile**

```
| ☐ | `project_read` nie zur Prüfung grosser Ablagedateien — es liefert jede Datei ganz in den Chat (Fehler Nr. 12: 158 KB inline). Hochladen per `local_path` aus einer md5-geprüften Datei, kein Rücklesen; Schätzung für Gelesenes: Bytes ÷ 1,6 (F2, 01.10.2026) | 23 |
| ☐ | Das Register liegt in der Ablage je Abschnitt (`REGISTER_KOPIE_ABSCHNITT_<nn>.md`, `REGISTER_INDEX.md` nennt die Datei; erzeugt mit `registerkopie.py --abschnitte`); geöffnet wird nur, was gebraucht wird, im Wortlaut — keine Kurzfassung als zweite Quelle, keine zusammenfassenden Helfer (F1, 01.10.2026) | 23 |
| ☐ | Grosse Dokumente nicht im Chat zusammensetzen: abschnittsweise in Dateien schreiben, nicht mehrfach umbauen, keine ganzen Dateien in den Chat holen; Mechanik (Anker zählen, md5, Zeilenbereiche, Diffs) als Skript, nicht als Helfer (S3, S6, 01.10.2026) | 22.10 |
```

#### E6 — Abschnitt 0, „Wenn ich einen Auftrag schreibe“: B1, B5, S4, S5

Anker: `Dokumentationsauftrag: Text wörtlich mit Ankertext` · Art: **nach der Zeile**

```
| ☐ | Messung 0a (Arbeitsbaum) in den Scratch, bevor der eigene Belegordner entsteht — oder den Belegordner ausdrücklich ausnehmen (Abnahme TB-126, B1) | 14, Regel 3 |
| ☐ | Trennzeichen in vorgegebenen Listen nach den Daten wählen: tragen die Einträge selbst Kommas, ist „kommagetrennt“ falsch (Abnahme TB-126, B5) | 18, P.4 |
| ☐ | Gegenleser eng zuschneiden: genaue Dateien und Zeilenbereiche, rund 25 Schritte, dann Zwischenbericht (S5, Probe); eine zweite Runde macht ein frischer Helfer mit Befundliste und geänderten Stellen (S4) (01.10.2026) | 22.10 |
```

#### E7 — Abschnitt 0, „Wenn ein Dokument mitgeht“: F4, F5, F6

Anker: `An Fable nur vorgeprüfte Verfahrensfragen; vor der nächsten Anfrage` · Art: **nach der Zeile**

```
| ☐ | Fable-Anfrage nennt die Abschnittsnummern aller berührten Registerstellen; Fable öffnet diese, was der Index als „gilt“ und „dazu“ nennt, und weitere nach eigenem Urteil (F5, 01.10.2026) | 22.11 |
| ☐ | Fable-Übergabetexte kurz: keine Fehlerliste und keine Landkarte, die schon in R52, 50.1 oder im Index steht — Verweis statt Wiederholung (F6). Probe über zwei Anfragen: ein Fable-Chat je Anfrage, erst nach Fables Antwort auf die Verfahrensfrage zu 27 (F4) (01.10.2026) | 22.11 |
```

### Datei `docs/projektfuehrung/BACKLOG.md`

#### E8 — Abschnitt 4, K4u

Anker: `| **K4t** |` (Zeilenanfang) · Art: **nach der Zeile**

```
| **K4u** | ⭐ **TOKENSPAREN OHNE QUALITÄTSVERLUST (01.10.2026, drei Betreiberentscheide per Karte).** S1–S7 (20:10; S2 um 21:35 ersetzt durch die Ampel auf den Verlauf ohne Grundlast, `docs/werkzeuge/ampel.py`), F1–F6 aus dem Fable-Chat (21:25: Registerkopie je Abschnitt, Schätzung ÷ 1,6, Projekt-Erinnerung verdichtet, ein Fable-Chat je Anfrage als Probe, Abschnittsnummern in Anfragen, kurze Übergaben). Ausdrücklich nicht: Gegenlesen streichen, pauschal Sonnet, Fable seltener fragen, Registerkurzfassung als zweite Quelle, zusammenfassende Helfer, das Lesen im Wortlaut streichen. Fehler Nr. 11 (Ampel geschätzt), 12 (`project_read` 158 KB inline), 13 (Schwellen in falscher Einheit). Wortlaute: `UEBERGABE.md`, Nachträge 01.10.2026 20:15, 21:35, 21:50; Messung `MESSUNG_2026-10-01_ampel_grundlast.md`. Eingearbeitet mit TB-127 |
```

#### E9 — Abschnitt 5, „Aus der Abnahme TB-126“

Anker: `## 6 — Geparkt, null Arbeit` · Art: **vor der Zeile**

```
### Aus der Abnahme TB-126 (01.10.2026)

- **Offen aus „Für Fable“ (Ergebnis TB-126, Abschnitt „Für Fable“ Nr. 1–8):** Lesart 50.5, Lesart R48 (d), Reibung R53, Nebenbefund R28 (`pruefe_abschnitt17.py:97`), Vereinigung der Markenorte R48–R50, Orte ohne Marke (Anhang A, Listen B und C), zweite PRÄZISIERT-Marke in 25.3 (i) ⇒ erste Anfrage an den neuen Fable-Chat, vorgeprüft, mit Abschnittsnummern (F5), dazu die Verfahrensfrage zu 27 (F4).
- **`registerbericht.py --pruefen` rc 1** (39.1, 42.4 G7, 43-6): bekannt seit vor TB-126; laut Ergebnis TB-126 („Für Fable“ Nr. 8) weicht der ERZEUGT-Block in Abschnitt 3 vom Erzeuger ab. Offen.
- **Befunde B1–B6 der Abnahme** (`UEBERGABE.md`, Nachtrag 01.10.2026, ca. 20:45): B1 und B5 stehen als Regeln in ARBEITSWEISE 0 (TB-127); B6 (Worktree `tb123_vorher`) behandelt TB-127 Schritt 0b, Ausgang im Ergebnis TB-127; B4 (Liste B nicht ausdrücklich genannt) geht in die erste Fable-Anfrage; B2 und B3 sind Kleinigkeiten ohne Folge.
```

## Schritt B — `registerkopie.py --abschnitte` (F1)

⚠️ **Reihenfolge der Ausführung: 0, A, C, B, D** — die Einfügungen sind committet, bevor der Code geändert wird; ein Abbruch in B lässt sie stehen.

Vorlage ist `docs/werkzeuge/registerkopie_abschnitte.py` (vom steuernden Chat, in Schritt 0 committet). Es schreibt 51 Dateien `REGISTER_KOPIE_ABSCHNITT_<nn>.md`; ihre md5 sind die Referenz, sie liegen so in der Projektablage.

B1. `registerkopie.py` bekommt den Schalter `--abschnitte`:
- ohne `--pruefen`: schreibt je Abschnitt eine Datei, Standardziel `docs/projektfuehrung/register_kopie/` (mit `--ziel` änderbar; das heutige `--ziel` hat den festen Standard `docs/projektfuehrung` — der Standard wird je Modus aufgelöst, der Teile-Modus behält seinen), **Kopf und Body bytegleich wie die Vorlage** (Kopfzeile `# REGISTER-KOPIE Abschnitt <n> (von 0–<m>) — Register-Z. <a>–<b> — Commit <hash> — <Datum> — Original sha256 <…> — KOPIE, nicht das Register`, Zeile 2 leer, Body ab Zeile 3; Vorrede zu Abschnitt 0; gelesen am HEAD; `<hash>`/`<Datum>` des letzten Commits, der das Register geändert hat; Arbeitsbaum ≠ HEAD oder Abschnittsnummern nicht fortlaufend ⇒ rc 2; `--marken` zusammen mit `--abschnitte` ⇒ rc 2);
- mit `--pruefen`: jede Datei 00…<m> vorhanden, Bodies aneinandergehängt == Original am Commit aus dem Kopf (bytegleich), Kopf in dieser Form ⇒ rc 0, sonst rc 1;
- der bisherige Teile-Modus bleibt unverändert; der Docstring nennt den neuen Modus und unter „Wann laufen lassen“, dass die Ablage seit 01.10.2026 die Abschnittsdateien führt.
- Nichts löschen (wie bisher).

B2. Nachweis ⇒ `docs/belege/TB-127/b2_registerkopie.txt`:
- `registerkopie.py --abschnitte --ziel "$TMPDIR/tb127_abschnitte"` ⇒ rc, Dateizahl; md5 aller 51 gegen `docs/projektfuehrung/register_kopie/` (Soll: alle gleich);
- `registerkopie.py --abschnitte --pruefen` ⇒ rc 0 (am Standardziel);
- `registerkopie.py --pruefen` (Teile-Modus) ⇒ rc wie vorher (Soll 0, BYTEGLEICH);
- `git diff --numstat -- docs/werkzeuge/registerkopie.py`.

## Schritt C — Nachweis der Einfügungen

C1. `einfuegungen.txt` (oben). Soll: E1–E9 je Anker vorher 1, ausgeführt, Text nachher 1.

C2. `git diff --numstat` je Datei ⇒ `c2_numstat.txt`. Entfernte Zeilen nur aus E3 und E4 (je 1 Zeile in ARBEITSWEISE); UMZUG und BACKLOG: keine.

C3. Zeichengleichheit: Skript `docs/belege/TB-127/c3_vergleich.py` liest je Einfügung den Text aus diesem Auftrag und prüft, dass er in der Zieldatei genau einmal als zusammenhängender Block vorkommt (Bytevergleich) ⇒ `c3_vergleich.txt`.

Commit `TB-127 A/C: Regelwerk-Nachtrag, Nachweis`, pushen — **vor** Schritt B. Nach B: Commit `TB-127 B: registerkopie --abschnitte, Nachweis`, pushen.

## Schritt D — Abgabe

D1. `docs/ERGEBNIS_TB-127_regelwerk_tokensparen_registerkopie.md`: Kopf, Kurz-Tabelle (0b Worktree, E1–E9, B2, C2, C3), „Nicht getan“ und „In einfacher Sprache“. Unter „Nicht getan“ steht, was ausdrücklich einem späteren Auftrag bleibt (Block 4 Nr. 4 des Umzugsblocks 01.10. 08:20, Wortlaute noch nicht vorbereitet): 5b-Bewertung zu 27c, 29a, 29b; K2h/K2f; die drei Trägerstellen; der kalte Leser ohne Gedächtnis; 29a Abschnitt 1–3; die `project_info`-Regel; R31 (b) und R49 (e) ins Regelwerk; Sonnet-Probe mit wirksam gesetztem Modell; `BACKLOG.md` in der Ablage erneuern (vorher 27.4-Prüfung). Lag `FABLE_UEBERGABE_2026-10-01_neuer_chat.md` in 0a nicht im Arbeitsbaum, steht hier, dass sie noch nicht im Repo ist.

D2. Journalblock **DY** ans Ende von `JOURNAL.md` (Buchstabe gemessen: letzter Block plus eins), mit Quellenzeile.

D3. Abgabe-Commit `TB-127 Abgabe: Ergebnis, Journal DY`, pushen. Danach `git status --porcelain` in den Scratch und als `docs/belege/TB-127/d3_porcelain.txt`, kleiner letzter Commit, pushen.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a weicht ab (ausser der genannten optionalen Datei).
- B2: die Abschnittsdateien aus `--abschnitte` sind nicht md5-gleich mit der Referenz, oder der Teile-Modus `--pruefen` wird schlechter als vorher.
- Eine Datei ausserhalb der Zieldateien, Belege, Ergebnis und Journal müsste geändert werden.
- `git push` scheitert zweimal.

Bei Abbruch: committen, was an Belegen da ist, Grund in `docs/belege/TB-127/abbruch.txt`, pushen, melden.

## In einfacher Sprache

Heute Abend hat der Betreiber neue Sparregeln beschlossen: Die Umzugsampel zählt jetzt richtig, das Regelwerk liegt in der Ablage je Abschnitt, und Fable bekommt kürzere Übergaben. Diese Sitzung trägt die Regeln wörtlich an ihren festen Stellen ein, baut das Schneiden je Abschnitt in das bestehende Werkzeug ein und prüft, dass dabei exakt dieselben Dateien entstehen, die schon in der Ablage liegen. Ausserdem räumt sie einen alten, leeren Arbeitsordner weg.

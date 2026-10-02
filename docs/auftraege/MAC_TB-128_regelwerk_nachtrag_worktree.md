# TB-128 Regelwerk-Nachtrag 01.10.2026, zweiter Teil (Fehlerregeln, Fable-Ablage, kalter Leser, R31 (b), R49 (e), 5b-Bewertung) und Worktree `tb123_vorher`

**Sitzungstitel:** `TB-128` · **Modell:** Opus 5.5 (Standard) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 01.10.2026, ca. 23:25, vom steuernden Chat
**Vorgänger:** TB-127 (`eeee21d`). **Dieser Auftrag:** `docs/auftraege/MAC_TB-128_regelwerk_nachtrag_worktree.md`, er wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3`. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei** (Betreiberentscheid 26.09.2026). Die Entfernung des Worktrees `tb123_vorher` hat der Betreiber am 01.10.2026, ca. 22:20, per Karte entschieden („TB-128 entfernt (Empfohlen)“). Fundstelle je Einfügung.

Geändert werden nur: `docs/projektfuehrung/ARBEITSWEISE.md`, `docs/projektfuehrung/BACKLOG.md`, dazu Belege, Ergebnis und Journal.

⛔ **Nicht erlaubt, mit Grund:**
- Den vorgegebenen Text umformulieren, kürzen, glätten oder zusammenlegen. *Grund:* Die Wortlaute hat der steuernde Chat aus den Quellen festgelegt und gegenlesen lassen; die Sitzung trägt sie ein, sie formuliert nicht (5b).
- Register, `docs/VORREGISTRIERUNG_*`, `research/`, `strategies/`, jede Sperrlisten-Datei, `docs/PRUEFPRINZIPIEN.md`, `UMZUG.md`. *Grund:* nicht Gegenstand.
- `UEBERGABE.md`, `UEBERGABE_ARCHIV.md`, die `FABLE_*`-Dateien ändern. *Grund:* Das sind die Quellen.
- `docs/werkzeuge/registerkopie_abschnitte.py` löschen. *Grund:* Löschen ist ein Betreiberentscheid, er liegt nicht vor. Die Übergabe (Nachtrag 01.10.2026, ca. 22:35) sah das Entfernen in TB-128 vor; das entfällt hier.

Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt (auch `UEBERGABE.md`, die `FABLE_*`-Dateien und `AKTUELLER_AUFTRAG.md`); das ist kein Ändern im Sinn der Verbote und des Abbruchkriteriums.

**Sichtschutz:** entfällt, es werden keine Ergebnisse gelesen.

## Verfahren je Einfügung (E1–E7)

*Vorgezählt vom steuernden Chat am 01.10.2026, ca. 23:20, über die Geräteanbindung (Python `str.count`): jeder Anker genau 1; `Aus der Abnahme TB-127`, `Aus Fable 27c, 29a und 29b`, `Fehler Nr. 14`, `project_info` und `kalter Leser` kommen in den Zieldateien noch nicht vor. Die Sitzung zählt selbst nach; ihre Zahl gilt.*

1. **Vorher:** Anker in der genannten Zieldatei zählen (Python `str.count`). **Soll: genau 1.** Weicht die Zahl ab: diese Einfügung nicht ausführen, vermerken, weitermachen (kein Abbruch).
2. **Ausführen** wie unter „Art“: „nach der Zeile“/„vor der Zeile“ bezieht sich auf die ganze Zeile mit dem Anker. Der Text ist der Inhalt des Codeblocks unter der Einfügung, ohne Zäune. Tabellenzeilen (E1–E4) und die Fortsetzungszeile E6 (sie gehört zum Listenpunkt darüber) ohne Leerzeilen; Absätze und Blöcke (E5, E7) mit genau einer Leerzeile davor und danach, eine vorhandene wird nicht verdoppelt. Leerzeilen innerhalb eines Codeblocks gehören zum Text.
3. **Nachher:** Die erste Zeile des eingefügten Texts zählen. **Soll: genau 1.**
4. **Werkzeug:** per Skript `docs/belege/TB-128/einfuegen.py`, das Zieldatei, Anker, Art und Text aus **diesem Auftrag** liest, nicht aus dem Gedächtnis. Vorlage: `docs/belege/TB-127/einfuegen.py`; hier steht die Zieldatei je Einfügung in der Zeile `Zieldatei:`.

Ergebnis je Einfügung in `docs/belege/TB-128/einfuegungen.txt`: `E<n> · Datei · Anker vorher · ausgeführt ja/nein · Text nachher`.

## Schritt 0 — Sicherung, Ausgang, Worktree

0a. **Zuerst, bevor `docs/belege/TB-128/` entsteht:** `git status --porcelain > "$TMPDIR/tb128_0a.txt"`. Soll: genau die Einträge unten. Die Reihenfolge zählt nicht. Weicht etwas ab ⇒ Abbruch. Danach die Datei nach `docs/belege/TB-128/0a_status.txt` kopieren.

*Eingetragen vom steuernden Chat am 01.10.2026, ca. 23:25 (gemessen mit `git --no-optional-locks diff --name-only HEAD` und `ls-files --others --exclude-standard`):*

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/FABLE_UEBERGABE_2026-10-01_messung_steuernder_chat.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-128_regelwerk_nachtrag_worktree.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-10-01a_anfangsbestand_lesarten_marken.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md
?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-01_neuer_chat.md
```

Commit `TB-128 Schritt 0: Stand des steuernden Chats 01.10.2026, Abend`, pushen.

0b. **Worktree `tb123_vorher`** (Fehler Nr. 14: Die Messung in TB-127 zählte Ordnereinträge; richtig ist der Zustand laut git. Ausgang: `docs/belege/TB-127/0b_worktree.txt`). `git worktree list` ⇒ `<pfad>` (endet auf `/tb123_vorher`). Drei Messungen:
1. `git -C <pfad> status --porcelain` ⇒ Soll: genau vier Zeilen, alle mit `??`: `data_sicherung`, `logs`, `research/turn_of_month/daten`, `trading-env`. Keine weitere Zeile, insbesondere keine mit `M`.
2. Jeder der vier Einträge ist ein Symlink (`test -L`).
3. `git merge-base --is-ancestor $(git -C <pfad> rev-parse HEAD) main` ⇒ rc 0.

Stimmen alle drei: `git worktree remove --force <pfad>`, danach `git worktree prune` und `git worktree list` (Soll: nur der Hauptordner; wie die Ausgabe genau aussieht, ist vom Werkzeug abhängig, im Ergebnis beschreiben). Stimmt eine nicht: nicht entfernen, Befund benennen (kein Abbruch). Alles ⇒ `docs/belege/TB-128/0b_worktree.txt`.

0c. sha256 und Zeilenzahl der zwei Zieldateien ⇒ `docs/belege/TB-128/0c_ausgang.txt`.

## Schritt A — Die Einfügungen

#### E1 — Abschnitt 0, „Wenn ein Dokument mitgeht“: Fable-Dokumente legt der steuernde Chat ab (Betreiber 01.10.2026, 22:34)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Fable-Übergabetexte kurz: keine Fehlerliste` · Art: **nach der Zeile**

```
| ☐ | Dokumente für Fable legt der steuernde Chat selbst ab, in Projektablage und Repo, ohne Aufgabe an den Betreiber; dazu schreibt er den Übergabetext als Kopierblock (Betreiber 01.10.2026, 22:34: „Merke dir das für die Zukunft.“) | 22.11 |
```

#### E2 — Abschnitt 0, „Wenn eine Entscheidung beim Betreiber liegt“: R31 (b)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Karte nur für echte Betreiberentscheide: Freigaben` · Art: **nach der Zeile**

```
| ☐ | Eine Freigabe je Sperrlistendatei nennt deren Tests ausdrücklich mit (R31 (b)) | Register 47.14 |
```

#### E3 — Abschnitt 0, „Wenn Dateien abgelegt oder aus der Ablage gelesen werden“: Fable-Antworten über `project_info`

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `` `project_read` nie zur Prüfung grosser Ablagedateien `` · Art: **nach der Zeile**

```
| ☐ | Neue Fable-Antworten über `project_info` (Liste) prüfen, nicht über die Suche (25.09.2026); Antworten über `project_info` finden, ins Repo übertragen, md5 prüfen (29.09.2026) | UEBERGABE_ARCHIV |
```

#### E4 — Abschnitt 0, „Wenn ich einen Auftrag schreibe“: Fehler Nr. 14, 8, 9, 10, kalter Leser, R49 (e)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Gegenleser eng zuschneiden: genaue Dateien und Zeilenbereiche` · Art: **nach der Zeile**

```
| ☐ | Vorbedingung vor dem Entfernen eines Worktrees: porcelain zeigt nur das Erwartete, keine `M`-Zeile, der Commit ist Vorfahr von main — nicht die Zahl der Einträge im Ordner (Fehler Nr. 14, Abnahme TB-127) | UEBERGABE, Nachtrag 01.10.2026, ca. 22:35 |
| ☐ | Zieldatei je Einfügung in eigener Zeile (Fehler Nr. 8, Auftrag TB-125) | UEBERGABE, Umzug 01.10.2026, 08:20, Block 7 |
| ☐ | Lesarten des steuernden Chats im Registertext als „Lesart, vorläufig“ kennzeichnen; Markentabellen gibt der steuernde Chat fertig vor (Helfer, Anker vorgezählt); bei Prüfwerkzeugen messen, welchen Pfad sie lesen (Fehler Nr. 9) | UEBERGABE, Umzug 01.10.2026, 08:20, Block 7 |
| ☐ | Probe erst mit Modellschalter im Wächter oder mit Bestätigung des Modells vor dem Einfügesatz (Fehler Nr. 10: TB-125, Sonnet nicht wirksam) | 22.12; UEBERGABE, Umzug 01.10.2026, 08:20, Block 7 |
| ☐ | Ein kalter Leser läuft ohne Gedächtnis; das steht als Schritt 0 im Auftrag, mit Beleg: die vom Werkzeug ausgegebene Liste der beim Start geladenen Kontextdateien, sonst ein frischer Klon in einem Ordner ohne `MEMORY.md`/Verlaufsdateien, dessen Inhalt vor dem Start gelistet wird. Gilt für Leser, deren Aussage die Kälte ist; nicht für Mac-Sitzungen, die bauen (Handwerk, 29.09.2026) | Fable 29b |
| ☐ | Marken nennen Bezeichner, nicht Zeilen (R49 (e)) | Register 48.17 |
```

#### E5 — 22.11: Ergänzungen 01.10.2026 (F4–F6; Fable-Dokumente)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `„🟡 · ca. 450 000“.` · Art: **nach der Zeile**

```
⭐ **Ergänzung 01.10.2026 (Betreiberentscheid ca. 21:25, per Auswahlkarte im Fable-Chat; F4–F6, `UEBERGABE.md`, Nachtrag 01.10.2026, ca. 21:50):** **F4 (Probe über zwei Anfragen):** Ein Fable-Chat je Anfrage. Vorher geht als Verfahrensfrage an Fable: Darf der Anfangsbestand nach 27 durch das Leseprotokoll festgehalten werden statt durch einen R-Block je Chat? Begonnen wird erst nach der Antwort. **F5 (ab der nächsten Anfrage):** Jede Anfrage nennt die Abschnittsnummern aller berührten Registerstellen. Fable öffnet diese, was der Index als „gilt“ und „dazu“ nennt, und weitere nach eigenem Urteil. **F6 (ab dem nächsten Umzug):** Übergabetexte kürzen. Keine Fehlerliste und keine Landkarte, die schon in R52, 50.1 oder im Index steht; Verweis statt Wiederholung.

⭐ **Ergänzung 01.10.2026 (Betreiber, 22:34: „Merke dir das für die Zukunft.“; `UEBERGABE.md`, Nachtrag 01.10.2026, ca. 22:50):** Dokumente für Fable legt der steuernde Chat selbst ab, in der Projektablage und im Repo; der Betreiber bekommt dafür keine Aufgabe. Dazu schreibt der steuernde Chat den Übergabetext als Kopierblock in die Antwort; dem Betreiber bleibt das Einfügen im Fable-Chat.
```

#### E6 — 22.12: Die Probe TB-125 war keine gültige Probe

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `` `docs/ERGEBNIS_TB-125_regelwerk_nachtrag.md`. `` · Art: **nach der Zeile**

```
  ⚠️ Keine gültige Probe: Die Sitzung lief mit Opus 5.5; das Modell war vor dem Einfügesatz nicht auf Sonnet gestellt (oder die Umstellung griff nicht). Die Sonnet-Probe für Dokumentationsaufträge steht weiter aus (Ergebnis TB-125, „Probe nach 22.12“).
```

#### E7 — Abschnitt 5: Bewertung von 27c, 29a, 29b (5b) und „Aus der Abnahme TB-127“

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Anker: `## 6 — Geparkt, null Arbeit` · Art: **vor der Zeile**

```
### Aus Fable 27c, 29a und 29b (27.–29.09.2026) — Bewertung nach 5b, nachgetragen 01.10.2026

- **27c (R18–R32):** beantwortet. Die R-Blöcke stehen seit TB-126 (`db108a6`) im Register, Abschnitt 47. Eine eigene Bewertungspassage gibt es nicht; die Einzelstellen stehen in `UEBERGABE_ARCHIV.md`.
- **29a (Umzugstakt, Umzugsampel, Helfer-Agenten):** alles Handwerk (`UEBERGABE_ARCHIV.md`, Umzug 29.09.2026). Ampel und Helfer-Grundsatz stehen in UMZUG 3 und ARBEITSWEISE 22.10/22.11. Abschnitt 1 (Umzugstakt des Verfahrensprüfers) steht noch nicht im Regelwerk.
- **29b (R33–R52):** Kern nach Helferauszug (Umzugsblock 29.09.2026, 14:00, Block 4 Nr. 3, `UEBERGABE_ARCHIV.md`): Die Sammlung ist als Handwerk entschieden und deckt sich weitgehend mit den Neigungen. R33–R52 stehen seit TB-126 im Register, Abschnitt 48. Der kalte Leser ohne Gedächtnis steht seit TB-128 in ARBEITSWEISE 0. Offen daraus: K2h umformulieren und K2f nach PRUEFPRINZIPIEN Reihe C (Nummer messen); die drei Trägerstellen nach G1 nachziehen (TB-119 Nr. 2).

### Aus der Abnahme TB-127 (01.10.2026)

- **Fehler Nr. 14:** Der Auftrag TB-127 verlangte vor dem Entfernen des Worktrees `tb123_vorher` „ausser `.git` genau 4 Einträge“; im Ordner liegt der volle Checkout. Die Sitzung hat nach dem Wortlaut nicht entfernt. Die Regel steht in ARBEITSWEISE 0 (TB-128); den Worktree behandelt TB-128 Schritt 0b (Betreiberentscheid 01.10.2026, ca. 22:20), Ausgang im Ergebnis TB-128.
- **`docs/werkzeuge/registerkopie_abschnitte.py`** (Vorlage) ist durch `registerkopie.py --abschnitte` überholt. Entfernen ist ein Betreiberentscheid und steht aus.
- **Später, Wortlaute noch nicht vorbereitet:** K2h/K2f (Wortlaut „Stellvertreter“ in `BACKLOG_ENTSCHEIDUNGEN.md` gegen „Merkmal“ in Fable 29b klären); die drei Trägerstellen (kein Ersatzwortlaut in den Quellen); Fables 29a Abschnitt 1; Sonnet-Probe mit wirksam gesetztem Modell; `BACKLOG.md` in der Ablage erneuern (vorher 27.4-Prüfung).
```

## Schritt C — Nachweis der Einfügungen (ein Schritt B entfällt in diesem Auftrag)

C1. `einfuegungen.txt` (oben). Soll: E1–E7 je Anker vorher 1, ausgeführt, Text nachher 1.

C2. `git diff --numstat` je Datei ⇒ `docs/belege/TB-128/c2_numstat.txt`. Entfernte Zeilen: keine, in beiden Dateien.

C3. Zeichengleichheit: Skript `docs/belege/TB-128/c3_vergleich.py` (Vorlage `docs/belege/TB-127/c3_vergleich.py`) liest je Einfügung den Text aus diesem Auftrag und prüft, dass er in der Zieldatei genau einmal als zusammenhängender Block vorkommt (Bytevergleich) ⇒ `c3_vergleich.txt`.

Commit `TB-128 A/C: Regelwerk-Nachtrag, Nachweis`, pushen.

## Schritt D — Abgabe

D1. `docs/ERGEBNIS_TB-128_regelwerk_nachtrag_worktree.md`: Kopf, Kurz-Tabelle (0a, 0b Worktree, 0c, E1–E7, C1, C2, C3), „Nicht getan“ und „In einfacher Sprache“. Unter „Nicht getan“ steht, was einem späteren Auftrag bleibt: K2h/K2f; die drei Trägerstellen; Fables 29a Abschnitt 1; Sonnet-Probe mit wirksam gesetztem Modell; `BACKLOG.md` in der Ablage erneuern (vorher 27.4-Prüfung); `registerkopie_abschnitte.py` entfernen (Betreiberentscheid).

D2. Journalblock **DZ** nach dem letzten Block von `JOURNAL.md` (Buchstabe gemessen: letzter Block plus eins; nach DZ folgt laut Journal die nächste Kennung, im Ergebnis nennen), mit Quellenzeile.

D3. Abgabe-Commit `TB-128 Abgabe: Ergebnis, Journal DZ`, pushen. Danach `git status --porcelain` in den Scratch und als `docs/belege/TB-128/d3_porcelain.txt`, kleiner letzter Commit, pushen.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a weicht ab.
- Eine Datei ausserhalb der Zieldateien, Belege, Ergebnis und Journal müsste geändert werden.
- `git push` scheitert zweimal.

Bei Abbruch: committen, was an Belegen da ist, Grund in `docs/belege/TB-128/abbruch.txt`, pushen, melden.

## In einfacher Sprache

Am Abend des 01.10. sind weitere Regeln entstanden: Der steuernde Chat legt Unterlagen für Fable künftig selbst ab, und aus vier Fehlern der letzten Tage sind Prüfregeln geworden. Dazu kommen ältere Punkte, die noch nicht im Regelwerk standen. Diese Sitzung trägt alles wörtlich an den festen Stellen ein und hält fest, wie die drei Fable-Antworten vom 27. bis 29.09. bewertet wurden. Ausserdem entfernt sie einen alten Arbeitsordner, diesmal mit der richtigen Prüfung davor.

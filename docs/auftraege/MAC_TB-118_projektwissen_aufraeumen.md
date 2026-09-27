# TB-118 Projektwissen aufräumen — Repo-Seite: Registerkopie in Teilen, Dialog-Index, Backlog-Teilung, UEBERGABE.md, Soll-Skript, Löschliste; dazu `docs/` in die tägliche Sicherung

**Sitzungstitel:** `TB-118` · **Aufwand:** hoch (ARBEITSWEISE 22.1) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 26.09.2026, 23:20, vom steuernden Chat
**Grundlage:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27b_konzept_projektwissen.md`, md5 `ad35734f99414c982741b0c3f5b27862`, 36 823 Bytes, im Schritt 0 prüfen. Der Auftrag ist Fables Entwurf aus Teil D **zeichengleich**, bis auf drei Änderungen des steuernden Chats: den Kopf mit Freigabe; `git status` in Schritt 0 (siehe dort); Schritt H (G7, Rückfrage 4).
**Vorgänger:** TB-117. Dieser Auftrag startet erst nach dessen Abgabe, weil die Registerkopie Abschnitt 46 enthalten muss.

## ⭐⭐ Freigabe des Betreibers, wörtlich

**26.09.2026, ca. 23:15, Auswahlkarte im steuernden Chat:** *„Fable empfiehlt bei allen sechs Rückfragen: (1) Registerkopie in Teilen mit festen Namen plus Index-Seite; (2) je Antwort eine Indexzeile, das Register ist die Verdichtung; (3) kein Archiv-Ordner im Repo, nichts verschieben; (4) die tägliche iCloud-Sicherung kopiert zusätzlich docs/; (5) Antworten verlassen die Ablage, wenn erledigt, die zwei jüngsten bleiben; (6) die ganze Sofortliste in einem Vorgang. Ich schliesse mich allen sechs an. Freigeben?“* ⇒ **„Alle sechs übernehmen (Empfohlen)“**

⛔ **Nicht freigegeben:**
- Code des Laufs;
- Register, ARBEITSWEISE, UMZUG, DOKUMENTATIONSSTANDARD. Der Nachtrag nach 27b Teil E kommt als eigener Auftrag nach einer eigenen Freigabe;
- Löschen oder Verschieben im Repo, mit der einen Ausnahme `_eingearbeitet/` in C4;
- `crontab`, Datenbanken.

**Sichtschutz 27.1:** Diese Sitzung liest `BACKLOG.md` und `docs/belege/`; sie schreibt keine Grösse daraus in ein Dokument, das in die Ablage geht. Zeilen nach 27.1 gehen nach `BACKLOG_SICHTSCHUTZ.md` (nur Repo).
**Grundsatz:** Kein Dokument wird im Repo verschoben, umbenannt oder gelöscht (Registerzitate mit Pfad). Ausnahme: `_eingearbeitet/` nach DOKUMENTATIONSSTANDARD 10, nur nach Messung.

In einfacher Sprache: Diese Sitzung baut im Repo die Dateien, mit denen die Projektablage klein und eindeutig wird — eine Registerkopie in Teilen, eine Liste aller Fable-Antworten, ein geteiltes Backlog, eine Übergabe ohne Datum im Namen — und schreibt auf, was der steuernde Chat aus der Ablage entfernen darf. Gelöscht wird hier nichts.

## Schritt 0 — Sicherung und Ausgang
0a. `git status --short` (in der Mac-Sitzung erlaubt; nur die Brücke des steuernden Chats darf es nicht) → nur die erwarteten Dateien: Auftrag, Zeiger, `FABLE_ANTWORT_2026-09-27b_konzept_projektwissen.md`, `FABLE_ANFRAGE_2026-09-27b_konzept_projektwissen.md` (md5 `f22c54a1e020902dca758934e9c69a3e`); Auftrag und Zeiger committen (`TB-118 Schritt 0`).
0b. Ausgangswerte in `docs/belege/TB-118/0b_ausgang.txt`: HEAD; `wc -l docs/VORREGISTRIERUNG_neuselektion.md`; höchste Abschnittsnummer (`grep -E '^## [0-9]+\.' | tail -1`); `sha256sum` des Registers; `wc -l docs/projektfuehrung/BACKLOG.md`; Liste aller `docs/projektfuehrung/FABLE_*.md`, `docs/auftraege/MAC_TB-*.md`, `docs/ERGEBNIS_TB-*.md` mit Bytes.
0c. db-Sicherung nach 7c Schritt 0.

## Schritt A — Registerkopie in Teilen (`docs/werkzeuge/registerkopie.py`)
A1. Skript: liest `docs/VORREGISTRIERUNG_neuselektion.md` am HEAD; schneidet **nur an Zeilen `^## <n>\.`** (Abschnittsgrenzen) so, dass jeder Teil ≤ 240 000 Bytes Body hat; schreibt `docs/projektfuehrung/REGISTER_KOPIE_teil<n>.md` mit Kopf:
    `# REGISTER-KOPIE Teil <n> von <m> — Abschnitte <a>–<b> — Commit <hash> — <Datum> — Original sha256 <…> — KOPIE, nicht das Register`
    Darunter der Body unverändert.
A2. Nachweis (zwei Teile, 24c): (i) Bodies aller Teile in Reihenfolge aneinandergehängt `cmp` gegen das Original → rc 0, in `a2_cmp.txt`; (ii) jeder Teil ≤ 240 000 Bytes (`wc -c`), in `a2_groessen.txt`. Mutationsprobe: ein Byte im Body eines Teils ändern → `cmp` rc 1 (`a2_mutation.txt`), danach zurück.
A3. Alte Kopien im Repo (`REGISTER_KOPIE_2026-09-21/22/24*.md`) **nicht** löschen, nicht verschieben (G3). Nur die Löschliste (Schritt F) nennt sie für die Ablage.
A4. `REGISTER_INDEX.md`: je Festlegung 1–12 und je Registertext (1a … nn) die geltende Fundstelle nach allen „ERSETZT durch"-/„PRÄZISIERT durch"-Marken, mit Abschnitt und Teil-Nummer. **Gemessen, nicht erinnert:** Skript sammelt alle Marken (`grep -n 'ERSETZT durch\|PRÄZISIERT durch'`), die Sitzung löst die Kette je Eintrag auf und schreibt die Fundstelle; wo die Kette nicht eindeutig ist, steht „mehrdeutig, Abschnitte x, y" — kein Raten.
A5. Commit `TB-118 A Registerkopie in Teilen + Index`.

## Schritt B — `FABLE_DIALOG_INDEX.md`
B1. Skript `docs/werkzeuge/dialog_index.py` erzeugt das Gerüst: je `FABLE_ANTWORT_*.md` eine Zeile: Datum/Buchstabe · Stichwort aus dem Dateinamen · Repo-Pfad · Status „registriert", wenn der Dateiname im Register vorkommt (`grep -F`), sonst „–" · Register-Fundstelle: Abschnittsnummer(n) der Treffer · zugehörige Anfrage (gleicher Buchstabe).
B2. Die Sitzung füllt je Zeile **von Hand, lesend** zwei Felder: „Frage" (ein Satz) und „Entscheidung" (ein Satz) — aus dem Block **Kurz:** der Antwort, nicht aus dem Gedächtnis; wo die Antwort keinen Block „Kurz" hat, aus der Überschrift. Feld „offen": ja, wenn die Antwort Fragen an den Betreiber oder Messbitten stellt, die in keiner späteren Anfrage als beantwortet erscheinen (Suche nach dem Buchstaben in späteren `FABLE_ANFRAGE_*`); sonst nein.
B3. Nachweis: Zeilenzahl des Index = Zahl der `FABLE_ANTWORT_*.md` (in `b3_zaehlung.txt`); jede Zeile hat sechs Felder gefüllt (Skriptprüfung).
B4. Commit `TB-118 B Dialog-Index`.

## Schritt C — Backlog-Teilung (liest `BACKLOG.md`; Sichtschutz beachten)
C1. Aus `docs/projektfuehrung/BACKLOG.md` vier Dateien: `BACKLOG.md` (nur offene Einträge; Struktur der Abschnitte bleibt), `ENTSCHEIDUNGEN.md` (Festlegungen, K-Einträge, Betreiberentscheide mit Datum), `BACKLOG_ERLEDIGT_2026-09.md` (Erledigtes **und Abschnitt 8 „Gestrichen" vollständig** — er wird nie gelöscht, DOKUMENTATIONSSTANDARD 9), `BACKLOG_SICHTSCHUTZ.md` (jede Zeile mit einer Grösse oder Erwartung nach 27.1; mindestens Z. 170 und Z. 190 der heutigen Fassung; Suchmuster für Kandidaten: Sharpe-, Rendite-, Drawdown-, Trade-Zahlen und Sätze über den Ausgang — jede Fundstelle wird gelesen und eingeordnet, nicht nur gematcht).
C2. Nachweis: die Zeilen der alten Datei (ohne reine Überschriften und Leerzeilen) kommen als Multimenge in der Vereinigung der vier Dateien genau einmal vor (Skript `c2_zeilenmenge.py`, rc 0, Ausgabe in `c2_zeilenmenge.txt`); `numstat` je Datei; die alte Fassung ist im Git.
C3. Kopfzeile in `BACKLOG.md`: „Geteilt TB-118; Erledigtes in `BACKLOG_ERLEDIGT_2026-09.md`, Festlegungen in `ENTSCHEIDUNGEN.md`, Zeilen nach 27.1 in `BACKLOG_SICHTSCHUTZ.md` (nur Repo, bis zum Tag)."
C4. `BACKLOG_NACHTRAG_2026-09-18.md`, `JOURNAL_NACHTRAG_2026-09-18.md`: messen, ob eingearbeitet (Regel 10: Nummer und Textkern in `BACKLOG.md`/`JOURNAL.md` vorhanden, `nachtragswaechter.py`); wenn ja → `git mv` nach `docs/projektfuehrung/_eingearbeitet/` (die eine erlaubte Verschiebung); wenn nein → in `c4_offen.txt` melden, nicht verschieben.
C5. Commit `TB-118 C Backlog geteilt`.

## Schritt D — `UEBERGABE.md`
D1. `cp docs/projektfuehrung/UEBERGABE_2026-09-25.md docs/projektfuehrung/UEBERGABE.md`; Kopf ergänzen: „Fortgeschriebene Übergabe (UMZUG 1). Vorgängerfassungen: UEBERGABE_2026-09-19/24/25.md (Repo)." Die datierten Dateien bleiben im Repo unverändert.
D2. Block 7 (Fehler → Regel) aus `UEBERGABE_2026-09-19.md` (alle Fassungen) und `_24.md`: je Regel prüfen, ob sie in `ARBEITSWEISE.md` oder `PRUEFPRINZIPIEN.md` steht (Suche nach Kernwort, dann lesen). Fehlende Regeln in `d2_fehlende_regeln.txt` als Vorschlag für einen Nachtrag — **nicht** selbst eintragen (Regelwerk erst nach Freigabe).
D3. Commit `TB-118 D UEBERGABE.md`.

## Schritt E — `docs/werkzeuge/ablage_soll.py`
E1. Eingabe: Ist-Liste (Textdatei, ein Pfad je Zeile, vom steuernden Chat aus der Projektschnittstelle). Ausgabe: `soll.txt`, `entfernen.txt`, `ablegen.txt`.
E2. Regeln (fest im Skript, mit Verweis auf 27b Teil B): Regelwerk und Stand nach Namensliste; `REGISTER_KOPIE_teil*.md`, `REGISTER_INDEX.md`; `MAC_TB-118` offen, wenn kein `docs/ERGEBNIS_TB-118_*.md` existiert **oder** der Index für die zugehörige Antwort „offen" sagt; `ERGEBNIS_TB-118` bleibt, wenn eine `FABLE_ANFRAGE_*` es zitiert, deren Antwort im Index „offen" ist oder deren Registerauftrag fehlt; Dialogpaare: Index-Status „offen" oder eines der zwei jüngsten Datums-Buchstaben-Paare; ereignisgebundene Dokumente nach einer kleinen Tabelle `ablage_ereignisse.json` (Datei → Ereignis → erfüllt ja/nein, von Hand gepflegt).
E3. Probe: Ist-Liste = heutige 145 Dateien → `entfernen.txt` muss die Sofortliste 27b C3 ergeben (Abgleich in `e3_probe.txt`; Abweichungen benannt, nicht angepasst).
E4. Commit `TB-118 E Soll-Skript`.

## Schritt F — Löschliste mit gemessenen Tokens
F1. Für jede Datei in `entfernen.txt`: Bytes (`wc -c`) und Tokenschätzung nach derselben Methode wie die Betreibermessung vom 26.09. (Verfahren im Beleg nennen; wenn die Projektschnittstelle keine Zahl je Datei liefert: Bytes ÷ 4 als Näherung, so gekennzeichnet). Summen je Gruppe der Sofortliste.
F2. `docs/projektfuehrung/LOESCHLISTE_TB-118.md`: Tabelle Datei · Bytes · Tokens · Gruppe · Grund (Austrittsereignis), Summe, erwarteter Stand danach. Diese Datei geht in die Ablage, damit der Betreiber sie per Auswahlkarte freigeben kann, und verlässt sie nach dem Vollzug.
F3. Commit `TB-118 F Löschliste`; `git status --porcelain` leer; pushen.

## Schritt G — Journal und Ergebnis
`docs/ERGEBNIS_TB-118_projektwissen_aufraeumen.md` mit Kurz-Tabelle, Nachweisen (A2, B3, C2, E3), `d2_fehlende_regeln.txt`, `c4_offen.txt`; Journalblock; Abschnitt „Für den steuernden Chat": Reihenfolge C4 aus 27b (erst ablegen, dann entfernen, dann messen).

## Schritt H — `docs/` in die tägliche Sicherung (27b G7, Rückfrage 4 (a))
H1. `docs/werkzeuge/db_sicherung/db_sicherung.sh` (TB-112) lesen. Danach um einen Schritt ergänzen: ein `git bundle create` des Repos (alle Zweige), mit sha256, in denselben iCloud-Zielordner wie die Datenbanken. Namensschema und Aufbewahrung sind dieselben wie bei den Datenbanken. Kein Schlüssel und kein Dateiinhalt in die Ausgabe.
H2. Probe: das Skript einmal von Hand laufen lassen, `git bundle verify` auf die Kopie rc 0, Logzeile gezählt (`grep -c`). Die Crontab bleibt unverändert, denn das Skript läuft dort schon.
H3. Commit `TB-118 H docs in die tägliche Sicherung`.

## Abbruchkriterien (nur für diesen Gegenstand)
- `cmp` in A2 ≠ 0 → Abbruch, nichts committen.
- C2 Zeilenmenge ≠ → Abbruch der Teilung, alte `BACKLOG.md` bleibt.
- Ein Abschnittsschnitt in A1 lässt sich nicht unter 240 000 Bytes bringen (ein Abschnitt allein grösser) → Meldung mit Abschnittsnummer, Teil trotzdem schreiben, Befund für Fable.

## Nicht Teil dieses Auftrags
Löschen oder Ablegen in der Projektablage (steuernder Chat); Änderungen an ARBEITSWEISE, UMZUG, DOKUMENTATIONSSTANDARD (eigener Nachtrag nach Freigabe, Vorlage in 27b Teil E).
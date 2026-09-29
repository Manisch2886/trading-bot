# TB-123 TB-122 abschliessen — C3 nachholen, Abgabe, push

**Sitzungstitel:** `TB-123` · **Modell:** Opus, Aufwand hoch (ARBEITSWEISE 22.1) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 29.09.2026, ca. 17:45, vom steuernden Chat
**Grundlagen (in Schritt 0 lesen):** `docs/auftraege/MAC_TB-122_posten3_achsen_durchreichen.md` (Schritt C3, Abbruchkriterien, Sichtschutz) · `docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md` (Kopf, Kurz-Tabelle, Abschnitt 4 C3) · `docs/belege/TB-122/c3_tests.sh`.

**Vorgänger:** TB-122.

## Warum dieser Auftrag

Gemessen vom steuernden Chat am 29.09.2026, 17:33 (Ortszeit):
- Die Sitzung TB-122 hat `c064405` (Schritt 0, gepusht), `ab31314` (B) und `08153e4` (C1/C2) committet. `ab31314` und `08153e4` sind **nicht gepusht** (`origin/main` = `c064405`).
- Im Arbeitsbaum liegen, uncommittet und zuletzt um 16:10–16:12 geändert: `docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md`, `docs/belege/TB-122/c4_trockenlauf.txt`, `docs/belege/TB-122/c5_nachher.txt` und der Journalblock **DU** in `docs/projektfuehrung/JOURNAL.md` (numstat 41/0).
- **C3 ist nicht gelaufen:** Im Ergebnis steht `PLATZHALTER_C3`, im Journalblock DU `PLATZHALTER_C3_JOURNAL`. `c3_vorher.txt` und `c3_nachher.txt` fehlen.
- Sonde des Wächters um 17:33: **0 claude-Prozesse im Repo**. Warum die Sitzung endete, ist nicht gemessen.

## ⭐ Freigabe

Kein neuer Code. Dieser Auftrag vollzieht nur noch die Schritte C3 und D aus TB-122. Er steht damit unter der Freigabe von TB-122 (27.09.2026, ca. 20:20, und Nachtrag 29.09.2026, ca. 14:52, wörtlich dort). **Kein Code wird geändert**, auch keine Testdatei.

⛔ **Nicht freigegeben:** jede Änderung ausserhalb von `docs/` · Läufe im Modus oder auf dem Snapshot · Register und Regelwerk · ein neues Sperrlisten-Abbild · `crontab`, Datenbanken schreiben.

**Sichtschutz 27.1:** wie TB-122. Aus Testausgaben wird nur rc, Dauer und die Schlusszeile genommen, die das Skript ohnehin ausgibt. Keine Kennzahl aus Backtest-Ausgaben.

## Schritt 0 — Sichern, was daliegt

0a. `git status --short` — genau diese Einträge (Reihenfolge ohne Bedeutung):
- ` M docs/auftraege/AKTUELLER_AUFTRAG.md`
- ` M docs/projektfuehrung/JOURNAL.md`
- `?? docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md`
- `?? docs/auftraege/MAC_TB-123_tb122_abschliessen.md`
- `?? docs/belege/TB-122/c4_trockenlauf.txt`
- `?? docs/belege/TB-122/c5_nachher.txt`

Weicht etwas ab ⇒ Abbruch.

0b. Commit `TB-123 Schritt 0: Stand der beendeten Sitzung TB-122 gesichert` mit allem aus 0a **ausser `JOURNAL.md`**. Der Journalblock DU trägt noch einen Platzhalter; das Journal wird nach dem Commit nicht mehr umgeschrieben (DOKUMENTATIONSSTANDARD 9). Deshalb geht `JOURNAL.md` erst mit der Abgabe ins Repo. Danach **pushen**; damit sind auch `ab31314` und `08153e4` auf `origin`.

0c. db-Sicherung nach ARBEITSWEISE 7c Schritt 0, Beleg `docs/belege/TB-123/0c_db_sicherung.txt`.

## Schritt A — C3 nachholen

A1. **Nachher** (am HEAD, also mit `ab31314`): aus der Repo-Wurzel `bash docs/belege/TB-122/c3_tests.sh <$TMPDIR/tb123_c3_nachher>` ⇒ Ausgabe nach `docs/belege/TB-122/c3_nachher.txt`.

A2. **Vorher** (Stand `c064405`, vor dem Umbau): denselben Lauf an einem Arbeitsstand von `c064405` ausserhalb des Hauptordners. Vorschlag: `git worktree add --detach $TMPDIR/tb123_vorher c064405`, dort `trading-env` und die gitignorierten Datenordner, die die Tests lesen, als Verknüpfung auf den Hauptordner. Welche das sind, misst die Sitzung. Ausgabe nach `docs/belege/TB-122/c3_vorher.txt`. Lässt sich ein Test dort nicht gleichwertig betreiben ⇒ im Ergebnis benennen, nicht umbauen. Den Worktree danach mit `git worktree remove` entfernen oder seinen Pfad nennen.

A3. Vergleich je Testdatei: rc und Schlusszeile vorher gegen nachher, nach `docs/belege/TB-122/c3_vergleich.txt`.
- Gleich ⇒ C3 erfüllt.
- Abweichung bei einer Testdatei ⇒ **Befund, melden**. Nicht beheben, nicht zurücksetzen. Die Abgabe erfolgt trotzdem, mit dem Befund oben im Ergebnis.

A4. `git status --porcelain -- . ':!docs'` vor und nach A1/A2 zählen. Ändern die Testläufe etwas ausserhalb von `docs/` im Hauptordner ⇒ Abbruchkriterium.

Commit `TB-123 A: C3 vorher/nachher (TB-122)`, pushen.

## Schritt B — Abgabe

B1. In `docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md`:
- `PLATZHALTER_C3` durch das gemessene Ergebnis ersetzen (je Testdatei rc vorher/nachher, Zahl gleich/abweichend, Fundstellen der drei Belegdateien);
- die Kurz-Zeile **C3** füllen;
- im Kopf den Satz „Gepusht nach 0 und nach der Abgabe“ durch die gemessenen Push-Zeitpunkte ersetzen;
- neuen letzten Abschnitt **„10. Abschluss durch TB-123“**: was gemessen war (Abschnitt „Warum dieser Auftrag“ oben, wörtlich übernommen), was TB-123 getan hat, Commits. Die übrigen Abschnitte werden nicht umformuliert.

B2. Im Journalblock DU (noch uncommittet) `PLATZHALTER_C3_JOURNAL` durch eine Zeile mit dem C3-Ergebnis ersetzen und in der Überschrift oder der ersten Zeile vermerken: „C3 und Abgabe nachgeholt in TB-123“. Sonst nichts im Journal ändern. Danach `grep -c PLATZHALTER` über Ergebnis und Journal ⇒ **0**.

B3. Abgabe-Commit `TB-122 Abgabe (nachgeholt in TB-123): C3, Ergebnis, Journal DU` mit Ergebnis, Journal und den übrigen Belegen, pushen. Danach `git status --porcelain` aufnehmen (nach dem letzten Commit) nach `docs/belege/TB-123/b3_porcelain.txt` und in einem letzten kleinen Commit nachreichen, pushen.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a weicht ab.
- Eine Datei ausserhalb von `docs/` müsste geändert werden, oder A4 zeigt eine Änderung ausserhalb von `docs/`.
- `git push` scheitert zweimal.

Bei Abbruch: committen, was an Belegen da ist (nie `JOURNAL.md` mit Platzhalter), Grund in `docs/belege/TB-123/abbruch.txt`, pushen, melden.

## In einfacher Sprache

Die Sitzung, die drei Einstellungen bis zu den Bots durchgereicht hat, ist vor dem Schluss stehen geblieben. Der Umbau selbst ist gesichert und geprüft. Es fehlen nur noch der Lauf der bestehenden Tests vorher und nachher, das Hochladen nach GitHub und die Abgabe. Genau das holt dieser Auftrag nach, ohne am Code etwas zu ändern.

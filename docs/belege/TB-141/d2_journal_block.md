## EJ — TB-141: Regelwerk-Nachtrag 06.–08.10.2026 — 26 Einfügungen aus dem Auftrag per Skript (`ARBEITSWEISE.md` Abschnitt 0, 13, 15 Regel 5a, 22.5, 22.10; `BACKLOG.md` Abschnitt 5), alle zeichengleich und je genau einmal, numstat 58/0 und 13/0; Prüfungen S1–S4 10/10 Prüfanker je 1; Sperrlisten-Wache 0 Treffer; Nachtrag J1 in diesem Block (08.10.2026)

*Quelle: `docs/ERGEBNIS_TB-141_regelwerk_nachtrag_0807.md`*

**Quelle:** Mac-Sitzung **TB-141** (Hauptordner, lokal), 08.10.2026, ab 21:26 (gemessen, `TZ=Europe/Berlin date`), Eingang `d4a28e9`. Commits `f7d57d4` (Schritt 0),
`7988ce6` (A), `febde0e` (C) und der Abgabe-Commit. Belege `docs/belege/TB-141/`. Freigabe: Handwerk ohne
Sperrlistennähe, pauschal frei (Betreiberentscheid 26.09.2026). Datum des Eintrags zur Laufzeit: 08.10.2026.
Keine Rückfrage an den Betreiber. Kein Abbruchkriterium ausgelöst.

### Was gemessen ist

| | |
|---|---|
| **0a** | `git status --porcelain` drei Einträge wie Soll, HEAD `d4a28e91…`; Skript aus Anhang A sha256 `1af78b61…` wie Soll (vor und nach dem Kopieren); Rohausgabe `0a_status.txt` 132 B, 3 Zeilen, Beschreibung in `0a_status.kopf.txt` |
| **0b** | Ausgang an `f7d57d4`: `ARBEITSWEISE.md` 2 413 Z., md5 `e85163e9…`; `BACKLOG.md` 349 Z., md5 `583b4049…`; `JOURNAL.md` 10 528 Z., md5 `1eb65c7e…` — alle wie Soll |
| **0c** | Probe rc 0: 26 Einfügungen `ok` (Ankerzeilen wie die Zeilenbilanz), 10 Prüfanker je 1, Sperrliste fünf Suchworte je 0 in Register Abschnitt 10 (207 Zeilen) und ARBEITSWEISE-Tabelle (10 Zeilen); `Gesamt: wie Soll` |
| **A** | `einfuegen` rc 0: 26× `ausgeführt ja · Text nachher 1`, Zeilen je wie Bilanz; `ARBEITSWEISE.md` 2 413 → 2 471, `BACKLOG.md` 349 → 362 |
| **C2** | numstat `f7d57d4..7988ce6` rc 0: `ARBEITSWEISE.md` 58/0, `BACKLOG.md` 13/0, sonst nur Belege, keine entfernte Zeile |
| **C3** | `vergleich` rc 0: 26× `GLEICH` (Block-Einfügungen mit je einer Leerzeile davor und danach), 10 Prüfanker `nachher 1 · ok` |
| **D2** | Kennung gemessen: letzter Block vor `## Wiederkehrende Lehren` war EI ⇒ **EJ** wie erwartet; Block und J1 per Skript eingesetzt, Werte in `d2_journal.txt`, `d2_j1.txt`, `d2_j1_vergleich.txt` |

### Was aus dieser Sitzung an Regeln bleibt

| | Regel |
|---|---|
| | **Keine neue.** Ein einziges Skript aus dem Auftrag, das Texte, Anker und Sollwerte selbst liest und jede Belegdatei mit Kopfzeile neu schreibt und zurückliest, trug alle Schritte ohne Handarbeit und ohne Abweichung |

### Was offen bleibt

- Ablage von `ARBEITSWEISE.md` und `BACKLOG.md` — steuernder Chat.
- Die Posten unter „Nicht in TB-141“ (`BACKLOG.md` Abschnitt 5, Block TB-141); ob ein eigener Nachtrag sie trägt, ist offen.
- `UEBERGABE.md` und `UMZUG.md` unverändert (Fehler Nr. 22 nur im Backlog berichtigt).
- Nächste Journalkennung nach EJ: **EK**.

*Geschrieben 08.10.2026 von der Mac-Sitzung TB-141. Quellenvermerk: siehe Kopf.*

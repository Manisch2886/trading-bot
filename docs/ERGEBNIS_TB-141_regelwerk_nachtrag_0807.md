# Ergebnis TB-141 — Regelwerk-Nachtrag 06.–08.10.2026

**Stand:** 08.10.2026, Mac-Sitzung TB-141 (Hauptordner, lokal, Opus 5.5), ab 21:26 (gemessen mit `TZ=Europe/Berlin date`).
**Auftrag:** `docs/auftraege/MAC_TB-141_regelwerk_nachtrag_0807.md`. **Eingang:** `d4a28e9`.
**Commits:** `f7d57d4` (Schritt 0, ⟨S0⟩) · `7988ce6` (A) · `febde0e` (C) · Abgabe-Commit (dieses Dokument, Journal EJ) · D3-Commit.
**Belege:** `docs/belege/TB-141/`. **Rückfragen an den Betreiber:** keine. **Abbruch:** keiner.

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | drei Einträge (`AKTUELLER_AUFTRAG.md`, `UEBERGABE.md`, Auftrag `??`), HEAD `d4a28e91…`, Skript-sha256 `1af78b61…` | genau so; Rohausgabe `0a_status.txt` 132 B, 3 Zeilen, md5 `f11301db…` (`cmp` gleich mit `$TMPDIR/tb141_0a.txt`), Beschreibung in `0a_status.kopf.txt`; sha256 nach dem Kopieren ins Repo noch einmal gleich |
| 0b | md5/Zeilen wie „Belegt“ | `ARBEITSWEISE.md` `e85163e9…`/2 413, `BACKLOG.md` `583b4049…`/349, `JOURNAL.md` `1eb65c7e…`/10 528 — gleich |
| 0c | rc 0, 26 `ok`, 10 Prüfanker je 1, Sperrliste 5× 0/0, `Gesamt: wie Soll` | rc 0, genau so; Ankerzeilen alle wie Zeilenbilanz; Register Abschnitt 10 207 Zeilen, ARBEITSWEISE-Tabelle 10 Zeilen |
| A | rc 0, 26× `ausgeführt ja · Text nachher 1`, Zeilen wie Bilanz, 2413→2471, 349→362 | rc 0, genau so |
| C1 | `a_einfuegungen.txt` wie Soll | ja |
| C2 | rc 0, 58/0 und 13/0, sonst nur Belege | rc 0, `ARBEITSWEISE.md` 58/0, `BACKLOG.md` 13/0, weitere Dateien: keine (nur sechs Belege) |
| C3 | rc 0, 26× `GLEICH`, 10× `ok` | rc 0, 26× `GLEICH`, 10× `ok`, `alle zeichengleich, je genau einmal` |
| D2 | Kennung EJ; `journal` Probe und echt je sechs `ja`, rc 0 | letzter Block vor `## Wiederkehrende Lehren` war EI ⇒ **EJ**; Probe und echt je sechs `ja`, rc 0; Journal 10 528 → 10 566 (Block 35 Zeilen + 3) |
| J1 | Probe und echt je vier `ja`, `Textzeilen 11`, rc 0; `j1vergleich` `GLEICH` | genau so; `Zeilen +12`; Vergleich 4 238 B, Vorkommen 1, an Zeilengrenzen 1, im Block EJ vor `### Was gemessen ist` ja, `GLEICH`, rc 0 |
| D3 | porcelain 0 B; numstat ⟨S0⟩..Abgabe: 58/0, 13/0, JOURNAL 50/0 (35 + 3 + 11 + 1), sonst Ergebnis und Belege | gemessen nach dem Abgabe-Commit, Rohausgaben in `d3_porcelain.txt` und `d3_numstat.txt`, Beschreibung je in `*.kopf.txt` (D3-Commit); JOURNAL vor dem Abgabe-Commit `git diff --numstat` 50/0 |

## Abweichungen vom Auftrag

1. **Zählfehler im Auftragstext (Sachfehler, nicht berichtigt):** „Verfahren je Einfügung“ Nr. 3 nennt bei E22 „vier Zeilen Fliesstext“; der Codeblock von E22 hat **fünf** Zeilen. Zeilenbilanz (E22 +5), Probe (`Textzeilen 5`) und Einfügung (`Zeilen +5`) stimmen mit fünf überein; eingefügt ist der Codeblock unverändert.
2. **rc nicht in den Belegdateien:** Die Aufrufe `… ; echo "rc $?"` geben den rc auf die Konsole; die Belegdateien schreibt das Skript selbst (mit Kopfzeile, zurückgelesen), seine Standardausgabe ist inhaltsgleich und wurde nicht zusätzlich abgelegt. Die rc-Werte (alle 0) stehen nur hier und im Journalblock.
3. **`d2_journal_block.md`** trägt keine Kopfzeile `# TB-141 …`: er ist der Journalblock selbst, seine erste Zeile ist nach D2 die Kopfzeile `## EJ — TB-141: …`. Er ist kein Beleg des Skripts.

Geprüfte Sollwerte ohne Abweichung: 0a (Einträge, HEAD, sha256 zweimal), 0b (3× md5 und Zeilen), 0c (26 + 10 + 5 Zeilen, Schlusszeile), A (26 Zeilen, zwei Dateizeilen, Schlusszeile), C2, C3, D2 (Kennung, 6 + 6 Bedingungen), J1 (4 + 4 Bedingungen, Textzeilen 11, Vergleich), Zählungen in E26/J1 nachgerechnet: Abschnitt 0 39 Zeilen (E1–E20), Bestand 4 S / 18 E / 16 N nach der Zuordnungstabelle.

## Nicht getan

- Ablage von `ARBEITSWEISE.md` und `BACKLOG.md` (Projektablage) — macht der steuernde Chat.
- Die Posten unter „Nicht in TB-141“ im neuen Block von `BACKLOG.md` Abschnitt 5 (E26).
- `UEBERGABE.md` und `UMZUG.md` unverändert (die Berichtigung zu Fehler Nr. 22 steht nur im Backlog und im Journal).

## In einfacher Sprache

Die neuen Arbeitsregeln vom 6. bis 8. Oktober stehen jetzt in den Arbeitsregeln: 39 Zeilen in der Checkliste und Absätze in den Abschnitten 13, 15, 22.5 und 22.10. Die Abnahme von TB-139 und zwei Fehler des steuernden Chats stehen in der Aufgabenliste und im Journal (Block EJ). Ein Skript aus dem Auftrag hat alles eingesetzt und nachgeprüft: jeder Text steht genau einmal und Zeichen für Zeichen wie vorgegeben, keine alte Zeile wurde geändert. Am Code, am Register und an den Werkzeugen hat sich nichts geändert. Im Auftrag selbst ist eine Zahl falsch („vier“ statt „fünf“ Zeilen bei E22); das hat am Ergebnis nichts verändert.

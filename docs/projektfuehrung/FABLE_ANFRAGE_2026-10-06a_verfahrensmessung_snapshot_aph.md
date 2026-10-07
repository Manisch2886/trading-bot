# FABLE-Anfrage 06.10.2026 a (neuer Fable-Chat) — Verfahrensmessung am Snapshot (TB-138): Befund zu R72 (d) und Form des Eintrags

*Steuernder Chat, 06.10.2026, an einen neuen Fable-Chat. Vorgeprüft gegen Register, Manifest und Belege (Vorprüfung im Repo unter `logs/steuernder_chat/TB-139_vorpruefung_06a.md`, nicht in der Ablage). Ein Gegenleser hat Zitate und Fundstellen an der Quelle geprüft; 81 Stellen, sieben Fehler und acht Lücken, alle berichtigt; die Berichtigungen hat kein weiterer Leser geprüft. „REG Z.“ nennt Registerzeilen am Stand `9b7b060` (11 581 Zeilen, nach TB-136). Zitate stehen ohne die Hervorhebungen und Zeilenumbrüche des Registers. Kein Ergebnis gelesen (27.1).*

**Berührte Registerabschnitte:** 17 (17.2, 17.3, 17.5), 18, 23 (23.3), 27 (27.1, 27.2, 27.5), 29 (29.3), 33 (33.2), 35 (35.1), 46 (46.4 R13), 48 (48.16 R48), 49 (49.1 R53), 51 (51.1 R56, 51.6 R61), 52 (52.3 R65), 53 (53.1 R66, 53.5 R70, 53.7 R72, 53.9, 53.10), 54 (54.1 R74, 54.4 R77, 54.5, 54.6).

**Form der Antwort:** je Frage „einverstanden“ oder „anders, weil …“ mit Grund aus dem Registertext; Registertext nur als R-Block (ab R78).

---

## 1. Worum es geht

Die Verfahrensmessung am Snapshot, die R72 (d) und R74 (e) vor dem signierten Tag verlangen, ist am 06.10.2026 ausgeführt (TB-138) und abgenommen. Sie trägt einen Befund zu R72 (d): Bei `APH` steht am letzten Kurstag des Aktienmarktes eine Zeile ohne Kurs. Von dir brauche ich die Lesart zu diesem Befund (Frage 1) und die Form, in der das Ergebnis ins Register kommt (Frage 2); eingetragen wird danach in einem Auftrag.

## 2. Zu lesen

Die Registerabschnitte oben. Dazu in der Ablage `projektfuehrung/ERGEBNIS_TB-138_verfahrensmessung_snapshot.md`: die Zeilen 1–172 der Datei aus dem Repo (`docs/`, dort 18 100 B). Der Abschnitt „In einfacher Sprache“ (Z. 173–181) ist nicht mit abgelegt; in Z. 178 steht eine Stelle nach 27.5. Auftrag (`docs/auftraege/MAC_TB-138_verfahrensmessung_snapshot.md`, Z. 61–97) und Belege (`docs/belege/TB-138/m1.txt`, `m2.txt`, `m3.txt`) liegen nur im Repo; das Nötige steht hier.

## 3. Gemessen

**Vom steuernden Chat nachgerechnet** (eigene Befehle; nur die Datumsspalte und ob `close` fehlt):

- Aktien: 150 Reihen, 16 275 Kurstage von 1962-01-02 bis 2026-09-01 (`m1.txt` Z. 14, Z. 17).
- Früher endend nur `APH`: letzter Kurs 2026-08-31; `close` fehlt genau einmal, in seiner Zeile 2026-09-01 (`m2.txt` Z. 25–28; `m1.txt` Z. 118–120).
- Zwei Symbol-Tage Lücke: `LMT` 1974-06-03 und `MNST` 2026-08-10 (`m2.txt` Z. 31–34), gerechnet gegen die Kurstage als Ersatz für den Kalender.
- Kein doppelter Tag (`m2.txt` Z. 43, 69).
- Krypto ohne Befund: 24 `_1d`-Reihen, 3 316 Kalendertage von 2017-08-17 bis 2026-09-14, keine früher endende Reihe, keine Lücke (`m2.txt` Z. 47, 51, 58). In den 24 Reihen fehlt `close` in keiner Zeile (eigene Zählung; in der Sitzung nicht gemessen).

**Nicht nachgerechnet, nur Ausgabe der Sitzung:**

- In der Zeile `APH` 2026-09-01 sind auch `open`, `high`, `low` leer (`m2.txt` Z. 27).
- Vergleich mit dem Kalender „NYSE“ in der Lock-Umgebung: 0 Tage nur im Kalender, 0 nur in den Daten, über die ganze Spanne und je Aktien-Bot bis 2026-08-31; Urteil je Bot „erfüllt“ (`m1.txt` Z. 89, Z. 95–113). Verkürzte Sitzungen stehen im Index von `schedule` (Z. 126–128).
- Symbol-Tage Lücke im Zeitraum nach R66 (a) (L3, L4): je Aktien-Bot 1, je Krypto-Bot 0 (`m2.txt` Z. 35–38, Z. 60–64).
- Paketfassungen in `trading-env`: vier Pakete und Python 3.9.6 gleich `requirements.lock` (`m3.txt` Z. 14–19); dazu K1.

## 4. Lesarten des steuernden Chats, vorläufig

- **L1** (Auftrag Z. 80) „Der Snapshot“ ist der Ordner `snapshots/63e4b6c8…/`.
- **L2** (Z. 81) „Lock-Umgebung“ ist `trading-env/` mit `bin/python3`.
- **L3** (Z. 82) Ende des Zeitraums nach R66 (a): der 31.08.2026 einschliesslich (35.1: `2026-01-01/2026-09-01`, Ende ausschliesslich). Die Marken an 35.1 (38.1, REG Z. 6413; R37, REG Z. 6443) ändern das Ende nach der Messung beim Gegenlesen des Auftrags nicht.
- **L4** (Z. 83) Beginn je Bot: der 1. Januar des ersten Jahres der Spalte „erste Falte“ in 33.2 (REG Z. 5994–6004); R66 (a) verweist für den Beginn auf 29.3.
- **L5** (Z. 84) „trägt einen Kurs“: Die `_1d`-Reihe hat an dem Tag eine Zeile, in der `close` nicht fehlt.
- **L6** (Z. 85) „Sitzungstage“: der Index von `schedule` des Kalenders „NYSE“ (R74 (a); 17.5).
- **L7** (Z. 86) „letzter Kurstag ihres Marktes“: der späteste Kurstag über alle `_1d`-Reihen einer Universumsdatei.
- **L8** (Z. 87) „Symbol-Tag Lücke“: Handelstag ohne Kurs zwischen erstem und letztem Kurstag eines Symbols.
- **L9** (Z. 88) „Kursreihe eines Symbols“: `<SYMBOL>_1d.csv`; `_1h` und `_4h` gezählt, ohne Urteil.

Zwei Abweichungen des Messskripts (Abnahme 06.10.2026; `docs/belege/TB-138/verfahrensmessung_snapshot.py`): Die Sitzungstage je Bot sind ein Ausschnitt der einmal gerechneten Menge, kein eigener `schedule`-Aufruf (Z. 329; ob beides dasselbe liefert, ist nicht gemessen). Nach dem letzten Kurstag prüft es auch, welche übrigen Spalten leer sind, und gibt nur Spaltennamen aus (Z. 181–202).

## 5. Frage 1 — `APH`: Zeile ohne Kurs am letzten Kurstag des Marktes (R72 (d); 53.10 Nr. 3)

**Registertext.** R72 (d) (53.7, REG Z. 11468): „Vor dem signierten Tag wird am Snapshot gemessen (Verfahrensmessung nach 27.2), dass keine Kursreihe eines Symbols der zwei Universumsdateien vor dem letzten Kurstag ihres Marktes endet, und wie viele Symbol-Tage Lücke im Zeitraum nach R66 (a) liegen. Endet eine Reihe früher, wird gemeldet und vor dem Tag entschieden.“

**Sachverhalt.** Der letzte Kurstag des Aktienmarktes im Snapshot ist der 2026-09-01 (`m2.txt` Z. 24), ein Sitzungstag (`m1.txt` Z. 95, Z. 126); dort steht die Zeile von `APH` ohne Kurs (oben, 3). Das Ende des Zeitraums nach R66 (a) ist nach L3 der 31.08.2026. Der Befund hängt an L5 und L7: Nach Zeilen gezählt endet `APH` am 2026-09-01; im Zeitraum nach R66 (a) ist der letzte Kurstag des Marktes der 2026-08-31 (`m1.txt` Z. 96).

**Vorprüfung.** Das Register nennt `APH` nicht. Das Manifest führt 36 zugelassene Befunde, alle `rand_erste` (18, REG Z. 3055–3056), keinen an einer Aktien-Datei (`MANIFEST.json`); die Ausnahme in 17.3 gilt für `rand_letzte` nicht (REG Z. 2698). R13 (b) (46.4, REG Z. 10480) führt für die 150 Aktien-Dateien als letzte Kerze den 2026-09-01, belegt durch Schreibpfad und Zeitstempel; von einer Zeile ohne Kurs spricht es nicht. 53.9 (REG Z. 11494) mass am Bestand „nur Datumsspalten“ und sagt: „Nicht gemessen: Zeilen ohne `close`“. R72 (d) nennt den Zeitraum nach R66 (a) bei den Lücken, nicht beim Reihenende; wann eine Reihe „endet“, wenn eine Zeile ohne Kurs folgt, sagt der Block nicht, auch nicht, wer entscheidet und worüber. Registertext 3b (c) (23.3) und R48 (d) (48.16) sagen zu einer Zeile ohne Kurs und zu Tagen nach dem Ende nichts.

**Frage.** (a) Ist das ein „Endet eine Reihe früher“ im Sinn von R72 (d), gelten also L5 (`close` vorhanden) und L7 (über die ganze Reihe, nicht im Zeitraum nach R66 (a))? (b) Wenn ja: Was hat „vor dem Tag entschieden“ hier zu entscheiden, und wer entscheidet?

**Neigung.** (a) Ja. R72 (d) stellt das Reihenende nicht unter den Zeitraum nach R66 (a), und eine Zeile ohne `close` trägt keinen Kurs (L5); deshalb hat die Messung den Fall gemeldet. (b) Zu entscheiden ist nach meiner Lesart nur, ob der Befund als Tatsachennotiz stehen bleibt oder ob vor dem Tag noch gemessen wird, ob der Code des Laufs die Zeile vom 2026-09-01 liest (nicht gemessen). Einen zweiten Snapshot schlage ich nicht vor; er wäre ein neuer Lauf (17.2, REG Z. 2667–2668: „Ein zweiter Snapshot ist ein neuer Lauf.“). Wer entscheidet, sagt das Register nicht; deine Antwort lege ich dem Betreiber vor.

## 6. Frage 2 — Lesarten und Form des Eintrags (54.6 Nr. 1; 53.10 Nr. 3)

**Vorprüfung** (Helfer, `TB-139_bestand_A2.md`):

- Die Verfahrensmessungen aus TB-115 kamen über dich ins Register: Tagesanfrage 27a, deine Antwort, TB-117 (46.4, R13; Kette REG Z. 10487).
- Statuslisten wie 53.10 und 54.6 tragen keine Marke (R61 (b), REG Z. 11272; R77 (c), REG Z. 11545); die Erledigung steht im Schlusssatz des neuen Abschnitts (Vorbild REG Z. 11581).
- Eine Marke an der Zeile einer Befundtabelle setzt nach R65 (a) (REG Z. 11367) einen Block voraus: „soweit ein Block den Befund einer Zeile ergänzt oder berichtigt“. R70 (a) (53.5, REG Z. 11451) präzisiert R61 (b) und R65 (a).
- Eine Marke ohne Block von dir gibt es einmal: „11.3 ERGÄNZT durch 50.3 und 50.4“ (REG Z. 1250, „Tatsachennotiz“, TB-126); Abschnitt 50 trägt keinen R-Block.
- Ein Markenwort für „offen, jetzt gemessen“ gibt es nicht; seit TB-126 stehen in neuen Marken nur ERGÄNZT, PRÄZISIERT und BERICHTIGT.
- Das Register sagt nicht, wer das Ergebnis einer Verfahrensmessung einträgt; für „Bedingung erfüllt“ nennt R74 (e) keinen Folgeschritt.

**Frage.** (a) Bestätigst du die Lesarten L1 bis L9, oder berichtigst du sie? (b) In welcher Form kommt das Ergebnis ins Register: Blöcke von dir wie nach 27a, dazu Tatsachennotizen des steuernden Chats? (c) Welche Marke tragen die Zeilen „R74 (54.1) (e)“ in 54.5 (REG Z. 11558) und „R72 (53.7) (d)“ in 53.9 (REG Z. 11494)? (d) Welchen Stand haben danach 53.10 Nr. 3 und Nr. 10 und 54.6 Nr. 1 und Nr. 8?

**Neigung.** (a) Ich halte alle neun für die Lesart des Registers: L3 aus 35.1, L4 aus 33.2 unter dem Vorbehalt aus R53 (K4), L6 aus R74 (a); an L5 und L7 hängt Frage 1. (b) Ja: ein Abschnitt 55 mit deinen Blöcken ab R78 und einem Unterabschnitt „Voraussetzungen und Befunde“ des steuernden Chats, Bauart wie 54. (c) ERGÄNZT an beiden Zeilen, ausgelöst durch deinen Block (R65 (a)). Ohne Block gäbe es als Vorbild nur die Marke an 11.3 (REG Z. 1250). (d) 54.6 Nr. 1 und Nr. 8 und 53.10 Nr. 10 erledigt; 53.10 Nr. 3 gemessen, offen bleibt daran, was zu Frage 1 entschieden wird; beides im Schlusssatz des neuen Abschnitts.

## 7. Zur Kenntnis (je eine Zeile; „einverstanden“ genügt)

- **K1 (54.6 Nr. 8).** In `trading-env` steht `pandas_market_calendars` 4.6.1, wie im Lock (`m3.txt` Z. 14). „5.4.0“ nennt `docs/ERGEBNIS_TB-47_snapshotgrenze.md` in Z. 122 und Z. 359 für die Cloud-Sitzung vom 18.09.2026; dass sie das Feld `kalender` schrieb, ist erschlossen.
- **K2 (53.10 Nr. 10).** In den 174 `_1d`-Reihen des Snapshots: 0 doppelte `open_time`, 0 doppelte Tage, 0 `open_time` mit Zeitanteil (`m2.txt` Z. 43, 69). `benchmark.py` nicht geöffnet.
- **K3.** `XAUTUSDT` hat im Snapshot nur eine `_1h`-Reihe (`m2.txt` Z. 15–16); letzter Tag 2026-08-30, nicht bewertet (Z. 53; R13 (a)).
- **K4.** L4 steht unter dem Vorbehalt aus R53 (49.1, REG Z. 11005): „die erste Falte ist nach dieser Präzisierung neu abzuleiten“. TB-138 hat sie nicht neu abgeleitet.
- **K5.** Das Ergebnis führt unter „Für Fable“ fünf Punkte (Z. 158–162). Nr. 1 und Nr. 2 sind Frage 1 (a). Nr. 3 (alle 150 Aktien-Reihen führen eine Zeile am 2026-09-01, dem Tag nach dem Ende des Zeitraums; dazu R13 (b), 46.4) gehört zu Frage 1 (b). Nr. 4: `eingaben.json` bleibt als Beleg von TB-47 und wird nicht neu erzeugt; die Herkunft von „5.4.0“ steht in K1. Nr. 5 ist mit der eigenen Zählung in Abschnitt 3 erledigt (Krypto: `close` fehlt in keiner Zeile).

## 8. Leseprotokoll und Sichtschutz

- Keine Bestätigungsrunde: Deine erste Antwort ist die Antwortdatei. Sie beginnt mit dem Leseprotokoll nach R56 (b) (Register 51.1).
- Kein Ergebnis gelesen (27.1); nur Verfahrensmessungen nach 27.2. Das Ergebnis TB-138 liegt in der Ablage ohne den Abschnitt ab Z. 173.

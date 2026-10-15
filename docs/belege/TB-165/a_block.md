## FB — TB-165: Register 61 (Fable 15a, R98–R99) und drei Marken
*Quelle: `docs/ERGEBNIS_TB-165_register61_fable15a.md`, Commits `4edd877` (S0), `173368f` (R), `e941e61` (K), F = der Abgabe-Commit „TB-165 Abgabe: Ergebnis, BACKLOG, Journal FB“, der diesen Block enthält.*

**Quelle:** Übergabe, Anfrage und Antwort 15.10.a liegen seit `4edd877` im Repo (md5 vorher geprüft, 3/3). Am Registerende steht Abschnitt 61: 61.1 R98 (Ort der Schranke je Bot, Parameterweg unter drei Bedingungen, eine Freigabe je Bauauftrag, Abnahme am Erzeuger) und 61.2 R99 (Tatsachennotizen 15a, Lesart „25c (1) ist 42.3 F1 (a)“), beide mit Quellenzeile zeichengleich aus dem Codeblock der Antwort (Z. 46–49); 61.3 Voraussetzungen und Befunde. Drei Marken nach R99 (d): 57.1 R90 und 56.3 R86 ERGÄNZT durch R98, 57.2 R91 PRÄZISIERT durch R99. Kopien, Index (neuer Abschnitt 14) und Dialog-Index (Zeile 15a) sind nachgezogen.

### Was gemessen ist
- 0a: Zweig `main`, HEAD `a9bf4a7`, sieben Einträge wie Soll; Werkzeug-sha256 `200abc0c…` wie Soll; md5 der drei Fable-Dateien 3/3, rc 0.
- V: 20 Prüfungen, NEIN 0, rc 0.
- R: Probe und Eintrag rc 0; Marken Z. 11887 (56.3), 11985 (57.1), 11995 (57.2); 61 ab Z. 12204; numstat Register 78/0.
- 61.3 (a), R99 (g): 37, 55 und 57 am `35dae90` = am `4edd877` = gelesene Kopie. Befund: 56 in der vom Verfahrensprüfer gelesenen Kopie (`3f2e97e`) ohne die Marke „56.1 R84 PRÄZISIERT durch R95 (58.2)“ aus TB-162, sonst zeichengleich.
- 61.3 (b), R99 (b): „25c (1)“ in 12 Zeilen ausserhalb 57 (darunter R60 (b) Z. 11352 und R63 (c) Z. 11434) und 3 in 57; die Lesart trifft an allen zwölf Stellen; Stellen „Frage an Fable“: keine.
- K: alle acht Schritte rc 0; 61 in T6 (Abschnitte 58–61, 43 858 B), keine neue Teildatei; Kopien bytegleich; Index 0–61; Dialog-Index 62/62.
- BACKLOG: Rang 1 nachgetragen, als Nächstes TB-30b E-3 mit der Messung nach R98 (b).

### Was offen bleibt
- R98 (b): ob `entry_cutoff` in den sechs Backtests die drei Bedingungen erfüllt und welche Stelle es bei elliott_wave, elliott_wave_stocks und t3_supertrend ist — misst der Bau E-3 (61.3 (c)).
- F4 (Punkte 10–12 der Anfrage 10.10.a) mit Wortlaut in die nächste Fable-Anfrage (61.3 (d)).
- Der Befund zu 56 (R99 (g)) zur Kenntnis an den Verfahrensprüfer.

### In einfacher Sprache
Die neue Antwort des Verfahrensprüfers liegt mit Anfrage und Übergabe im Repo, und ihre zwei Regeltexte stehen jetzt wortgleich am Ende des Registers. Die erste Regel sagt, dass die Sperre gegen zu frühe Käufe bei jedem Bot dort sitzt, wo er seine Käufe bildet, und dass die Prüfung an dem Baustein läuft, der die Ergebnisse erzeugt. An drei älteren Stellen steht nun ein Hinweis, dass sie ergänzt oder genauer gefasst sind. Bei der Vorprüfung fiel auf, dass der Prüfer einen Abschnitt in einer Fassung ohne einen später gesetzten Hinweis gelesen hat; das ist festgehalten. Es lief nichts auf Kursdaten, kein Code wurde geändert.

*Geschrieben 15.10.2026 von der Mac-Sitzung TB-165. Quellenvermerk: siehe Kopf.*

## FL — TB-175: Register 67 (Fable 17b, R107, neun Marken) und Prüfung 13 in `test_haltedauer_kern.py` erneuert (Teil 1, ohne E2)
*Quelle: `docs/ERGEBNIS_TB-175_pruefung13_leser_alle_trades.md`, Commits `b470dc4` (S0, Fable 17.10.b und Auftrag), `3a00cf8` (R, Register 67 und neun Marken), `9d72a7f` (K, Registerkopie, Index, Dialog-Index), `9c31a65` (E, Prüfung 13), danach der Abgabe-Commit „TB-175 Abgabe: Ergebnis, BACKLOG, Journal FL“, der diesen Block enthält.*

**Quelle:** Fable-Antwort 17.10.b (md5 `d13e6919…`, Registerblock R107) mit Anfrage 17.10.b (md5 `af2c861a…`), R56 (b), Bauart 66 (TB-173); Bestand BESTAND_RANG1B Abschnitt 2 (steuernder Chat); Beleg `docs/belege/TB-169/e_alt_vorher.txt` (Prüfung 13 rot seit 46e3ed0/TB-98). Alles nur über `WZ` (Anhang A des Auftrags, sha256 `30b0d207…`), Test aus Anhang B (sha256 `b73adc87…`). Freigabe: Karte des Betreibers im Chat 34, 17.10.2026, 19:14 („Freigeben“).

### Was gemessen ist
- 0a: Zweig `main`, HEAD = origin/main = `5031cd0`, genau vier Einträge wie Soll, Karte gefüllt; beide Anhänge mit den Soll-sha256 (`Dateien 2`). Fable 17.10.b aus `data_sicherung/steuernder_chat_tmp/f17b/` kopiert, md5 vorher = nachher (2/0, rc 0). S0 = `b470dc4`, porcelain danach leer.
- V: 41 Prüfungen, NEIN 0, rc 0 (fünf Programme der Gruppe und Test = Bau-Stand, BACKLOG Rang 1 ohne TB-175, Journal FK, Fable-Dateien verfolgt, Registerblock R107 Z. 13–16, 66 da/67 nicht, neun Marken-Orte eindeutig, Index 0–66, Dialog-Index ohne 17b, fünf E2-Ausgangsdateien und elf Fundstellen am Bau-Stand).
- R: Probe 5/0, Eintrag 8/0, je rc 0. Abschnitt 67 ab Z. 12624; R107 mit Quellenzeile je genau einmal zeichengleich; neun Marken an 16.4 (Z. 2256), 16.8 (Z. 2469), 55.4 (Z. 11805), 56.3 (Z. 11914), 57.3 (Z. 12038), 58.4 (Z. 12124), 62.3 (Z. 12347), 64.1 (Z. 12479), 66.1 (Z. 12564); sonst append-only. 67.2 mit V-Beleg und Tatsachennotizen (a) bis (d).
- K: alle acht Belegdateien rc 0; Registerkopie bytegleich (sha256 `8f464607…`), Abschnitt 67 in Teil 6, 68 Abschnittsdateien; Index 0–67 mit Zeile 67 und Abschnitt 18; Dialog-Index 68 von 68 Zeilen.
- E (Python 3.9.6): alter Test rc 1 mit genau dem einen FEHLT der alten Prüfung 13; neuer Test „Alle Pruefungen bestanden.“, rc 0, 50 ok-Zeilen vor 13 gleich, Prüfung 13 mit 8 ok (Arbeitsbaum, Schreibziele, sechs Gegenproben). Gegenprobe an Kopien 3/0: Kontrolle grün, Voreinstellung für `--ziel` und `open(…, "w")` statt `_schreibe_einmal` je rot. `WZ nachher` 11/0.

### Was offen bleibt
- R107 (a) Zeilenschnitt bei den drei Aktien-Bots vor R44 (je ein Bauauftrag, Handelscode), (c) Modus-Wache im Listen-Erzeuger vor R44; (d) Kandidaten mit Orders nicht vor ihrer Zulassung.
- 67.2 (a) ist eine Teilmessung (Vergleich mit Lauf B, Prüfung 8 prüft den 3b-Lauf nicht) — zur Kenntnis an den Verfahrensprüfer.
- D4-Frage an den Verfahrensprüfer (über alle gefundenen Trades t3_supertrend P90 8,6833 statt 9,5000, Embargo 12 statt 13); danach E2 (Leser auf gefundene Trades). `research/mtm_drawdown/grundlage.py` (Startkapital aus der Meta) und `research/wf_kapital_dd/messung.py` Z. 120 (`es.STARTING_CAPITAL`).
- Teil (a) der Prüfung 13: eine Inhaltsänderung an einer schon geänderten Datei ausserhalb der acht Produktivordner sieht sie weiterhin nicht (Vorschlag A nicht gebaut).

### In einfacher Sprache
Die neue Antwort des Verfahrensprüfers liegt mit ihrer Anfrage unverändert im Repo; ihr Regeltext R107 steht wortgleich als Abschnitt 67 im Register, mit neun Hinweisen an älteren Stellen. Der Selbsttest der Haltedauer-Untersuchung meldete seit TB-98 einen Fehler, den es nicht gab: das Holprogramm schreibt in einen beim Aufruf genannten Ordner und überschreibt nie. Die neue Prüfung schaut jeden Schreibbefehl einzeln an und ist auf dem Mac grün; an verfälschten Kopien wird sie rot. Am Handelscode hat sich nichts geändert, es lief nichts auf Kursdaten.

*Geschrieben 17.10.2026 von der Mac-Sitzung TB-175. Quellenvermerk: siehe Kopf.*

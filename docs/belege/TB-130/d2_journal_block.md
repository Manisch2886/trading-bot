## EB — TB-130: Register Abschnitt 52 — Fable 02a (R63–R65) zeichengleich, Tatsachennotizen 52.4–52.5, 12 Marken am alten Ort; numstat 88/0, R-Diff 3/3, Zitate 2/2, `test_vorregistrierung` 196/196; Registerkopie 53 Abschnittsdateien und 4 Teile neu, Index und Dialog-Index nachgezogen (02.10.2026)

*Quelle: `docs/ERGEBNIS_TB-130_register_fable_02a.md`*

**Quelle:** Mac-Sitzung **TB-130** (Hauptordner), 02.10.2026, Eingang `1833839`. Commits `b0c7a35` (Schritt 0),
`cd1bf02` (0), `ad351d5` (A, einziger Registercommit), `2f6967c` (B/C) und der Abgabe-Commit. Belege
`docs/belege/TB-130/`. Freigabe des Betreibers 02.10.2026 (Auswahlkarte, gestellt 14:52, eingetragen 15:09). Keine
Rückfrage an den Betreiber. Kein Abbruchkriterium ausgelöst.

### Was gemessen ist

| | |
|---|---|
| **0** | 0a sechs Einträge wie Soll; Ausgang wie Soll (11 225 Z., `7f74b0e5…`, `register()` `a1e1366a…`, Sonde 37/0/0, (ii) 0, JSON `9f7364ef…`); 0c leer ⇒ Basis 196/196 aus TB-129; 0d: Prüfskript aus Anhang A am ⟨S0⟩ (per `git archive`, 17 Dateien) rc 0, 12/12 Marken, 33 Fundstellen, 7 Zählungen, 9/9 `simulate_portfolio` |
| ⭐⭐ **A** | Probelauf an Kopie, dann echt, `cmp` gleich. R-Diff **3/3**, Mutation rc 1, Zitate **2/2**, Überschriften und Ketten 3/3, Marken **12/12**, numstat **88/0**, Abschnitt 10 und ERZEUGT-Block bytegleich, Sonde-JSON ohne `zeilen` gleich, `registerbericht --pruefen` gleich (rc 1, schon vorher), `register()` → `4caf0179…`, 196/196 (894 s) |
| **B** | BACKLOG-Block 02a: Anker 1, numstat 10/0, bytegleich |
| **C** | Kopie 0–22 / 23–36 / 37–42 / 43–52 und 53 Abschnittsdateien, alle `--pruefen` bytegleich; Index: 212 Zahlen umgeschrieben, Zeile 52, Abschnitt 7 mit 12 Marken, fünf Indexzeilen aus 01a auf „Marke gesetzt“, Gegenprobe 236/236; Dialog-Index: 02a (52, offen), 01a registriert, 52 Antworten |

### Was aus dieser Sitzung an Regeln bleibt

| | Regel |
|---|---|
| ⭐ | **Ein Skript, das einen Text ersetzt, darf diesen Text nicht vorher selbst in die Datei schreiben.** Die neue Pflegezeile zitierte den alten Indexschluss wörtlich; die Zählung vor C3 sah 6 statt 5 und ersetzte zu Recht nichts. Reihenfolge der Skripte bedenken oder zitierten Text umschreiben |
| | **Ein Registerblock, der Berichtigungen beschreibt, wird von `--marken` als Marke gezählt** (diesmal R65 als `MARKE+`, wie R61 in TB-129). Zählungen aus `--marken` gegen die gesetzten Marken abgleichen |
| | **„Direkt unter dem berichtigten Satz“ (34.3) kann eine neue Marke vor eine ältere stellen** (25.2: R65 vor R53). Die Reihenfolge am Ort ist dann nicht die zeitliche |

### Was offen bleibt

- 52.5 (9 Punkte), „Für Fable“ im Ergebnis (52.5 Nr. 2, 5, 6, 7, 9; `--marken` zählt R65; Reihenfolge an 25.2;
  Markenwort für Bestätigungen).
- `registerbericht.py --pruefen` rc 1 schon vor TB-126 (Zahlenteil veraltet).
- Ablage der 53 Abschnittsdateien, des Index und des Dialog-Index — steuernder Chat.
- Nächste Journalkennung nach EB: **EC**.

*Geschrieben 02.10.2026 von der Mac-Sitzung TB-130. Quellenvermerk: siehe Kopf.*

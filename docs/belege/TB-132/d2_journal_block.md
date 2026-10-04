## ED — TB-132: Probe zu R71 in der Lock-Umgebung gleich der Vormessung (rc 0, 20/20 Zeilen); Register Abschnitt 53 — Fable 02c (R66–R73) zeichengleich, Tatsachennotizen 53.9–53.10, 21 Marken am alten Ort; numstat 158/0, R-Diff 8/8, Zitate 2/2, `test_vorregistrierung` 196/196; Registerkopie 54 Abschnittsdateien und 4 Teile neu, Index und Dialog-Index nachgezogen (04.10.2026)

*Quelle: `docs/ERGEBNIS_TB-132_register_fable_02c.md`*

**Quelle:** Mac-Sitzung **TB-132** (Hauptordner, lokal), 04.10.2026, Eingang `0779453`. Commits `57ae0d8` (Schritt 0),
`f32b5c7` (0), `ee43f5f` (A, einziger Registercommit), `12010b2` (B/C) und der Abgabe-Commit. Belege
`docs/belege/TB-132/`. Freigabe des Betreibers 03.10.2026 und Neubau 04.10.2026 (Auswahlkarten, eingetragen 07:28 bzw.
08:41). Keine Rückfrage an den Betreiber. Kein Abbruchkriterium ausgelöst.

### Was gemessen ist

| | |
|---|---|
| **0** | Datum 04.10.2026; 0a zehn Einträge wie Soll; zwei Skripte aus Anhang A sha256 gleich, Prüfskript rc 0; Ausgang wie Soll (11 313 Z., `a7496780…`, `register()` `4caf0179…`, Sonde 37/0/0, (ii) 0, JSON `9f7364ef…`); 0c leer ⇒ Basis 196/196 aus TB-130; 0d rc 0 |
| ⭐⭐ **0e** | `r71_probe.py` mit `trading-env/bin/python3`: rc 0, Zeile 3 `  pandas 2.3.3, numpy 2.0.2, Python 3.9.6`, ab `A - Faelle` 20/20 zeilengleich mit der Vormessung, Vergleich rc 0; stderr leer, kein `__pycache__` |
| ⭐⭐ **A** | Einfügeskript aus Anhang A unverändert, Probelauf an Kopie, dann echt, `cmp` gleich (beide Wachen liefen). R-Diff **8/8**, Mutation rc 1, Zitate **2/2**, Überschriften und Ketten 8/8, Marken **21/21**, numstat **158/0**, Abschnitt 10 und ERZEUGT-Block bytegleich, Sonde-JSON und -Text gleich, `registerbericht --pruefen` gleich (rc 1, schon vorher), `register()` → `66480962…`, 196/196 (892 s) |
| **B** | BACKLOG-Block 02b/02c: Anker 1, numstat 10/0, bytegleich |
| **C** | Kopie 0–22 / 23–36 / 37–42 / 43–53 (T4 232 545 B) und 54 Abschnittsdateien, alle `--pruefen` bytegleich; Index: 236 Zahlen umgeschrieben, 15.3 (a)/(c) in Tabelle 3, Zeilen 23/27/48/51/52 und neue Zeile 53, Abschnitt 8 mit 21 Marken und drei Indexzeilen, Gegenprobe 278/278; Dialog-Index: 02c (53, offen), 02b (53, registriert), 02a registriert, 54 Antworten |

### Was aus dieser Sitzung an Regeln bleibt

| | Regel |
|---|---|
| ⭐ | **Eine Probe, die „vor dem Eintrag“ verlangt ist, gehört als Wache in das Skript, das einträgt** — nicht nur als Schritt im Auftrag. Das Einfügeskript prüfte die Probenausgabe in Probelauf und Echtlauf selbst; ein Weiterarbeiten nach roter Probe wäre technisch gescheitert |
| | **Zählt ein Schritt vorher einen Titel, darf ein früherer Schritt derselben Sitzung diesen Titel nicht schreiben** (TB-130-Lehre, diesmal vorab vermieden: Pflegezeile ohne den Blocktitel) |
| | **Ändert eine Vorlage ihre Tabellenform (hier Spalte „Zeichen“ in Tabelle 1), müssen übernommene Leser die Spalten neu zählen** — `a5_marken.py` las sonst die Zeichenzahl als Kette |

### Was offen bleibt

- 53.10 (10 Punkte), „Für Fable“ im Ergebnis (53.10 Nr. 1, 2, 8, 9; `--marken` zählt drei Zeilen aus 53 mit; Index
  Tabelle 3 Zeile 3b (c) ohne „mit 53.7“).
- T4 der Registerkopie bei 232 545 von 240 000 B — der nächste grosse Abschnitt löst einen Neuzuschnitt aus.
- `registerbericht.py --pruefen` rc 1 schon vor TB-126 (Zahlenteil veraltet).
- Ablage der 54 Abschnittsdateien, des Index und des Dialog-Index — steuernder Chat.
- Nächste Journalkennung nach ED: **EE**.

*Geschrieben 04.10.2026 von der Mac-Sitzung TB-132. Quellenvermerk: siehe Kopf.*

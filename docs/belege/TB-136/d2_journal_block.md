## EE — TB-136: Nachmessung der Voraussetzungen am Gerät wie 54.5 (rc 0, 25/25 Zeilen); Register Abschnitt 54 — Fable 04a (R74–R77) zeichengleich, Tatsachennotizen 54.5–54.6, 15 Marken am alten Ort; numstat 110/0, R-Diff 4/4, Zitate 2/2, `test_vorregistrierung` 196/196; Registerkopie 55 Abschnittsdateien und 5 Teile neu, Index und Dialog-Index nachgezogen (05.10.2026)

*Quelle: `docs/ERGEBNIS_TB-136_register_fable_04a.md`*

**Quelle:** Mac-Sitzung **TB-136** (Hauptordner, lokal), 05.10.2026, Eingang `d781f1b`. Commits `753ae38` (Schritt 0),
`e9bf3c0` (0), `9b7b060` (A, einziger Registercommit), `d55e7ed` (B/C) und der Abgabe-Commit. Belege
`docs/belege/TB-136/`. Freigabe des Betreibers 04.10.2026 (Auswahlkarte, eingetragen 21:04). Datum des Eintrags zur
Laufzeit: 05.10.2026. Keine Rückfrage an den Betreiber. Kein Abbruchkriterium ausgelöst.

### Was gemessen ist

| | |
|---|---|
| **0** | 0a elf Einträge wie Soll; zwei Skripte aus Anhang A sha256 gleich, Prüfskript rc 0; Ausgang wie Soll (11 471 Z., `9a2cefb7…`, `register()` `66480962…`, Sonde 37/0/0, (ii) 0, JSON `9f7364ef…`); 0c leer ⇒ Basis 196/196 aus TB-132; 0d rc 0 |
| ⭐⭐ **0e** | Nachmessung statt Probe: Feld `kalender` aus TB-47 nennt `notifications/boersenkalender.py` (R74 (b) trifft); Import, Name „NYSE“ und Aufruf in Z. 81/70/109, einziger Import im Repo; Lock 4.6.1; `mtm_kern.py` 339 Z. mit Z. 210/244/246/251; Abschnitt 8 13 Zeilen ohne `zellenbericht`; `auswertung.py` 860 Z. ohne die drei neuen Namen — 25/25 `ok`, rc 0 |
| ⭐⭐ **A** | Einfügeskript aus Anhang A unverändert, Probelauf an Kopie, dann echt, `cmp` gleich (Wache zu R74 (b) lief in beiden). R-Diff **4/4**, Mutation rc 1, Zitate **2/2**, Überschriften und Ketten 4/4, Marken **15/15** an den Soll-Zeilen, numstat **110/0**, Abschnitt 10 und ERZEUGT-Block bytegleich, Sonde-JSON und -Text gleich, `registerbericht --pruefen` gleich (rc 1, schon vorher), `register()` → `cfff54ca…`, 196/196 (940 s) |
| **B** | BACKLOG-Block 04a: Anker 1, numstat 10/0, bytegleich |
| **C** | Kopie 0–22 / 23–36 / 37–42 / 43–53 / **54** (fünfter Teil wie gerechnet, T4 234 587 B, T5 24 706 B) und 55 Abschnittsdateien, alle `--pruefen` bytegleich; Index: 278 Zahlen umgeschrieben, 2d und 5f in Tabelle 3, Zeilen 48/51/52/53 und neue Zeile 54, Abschnitt 9 mit 15 Marken und zwei Indexzeilen, Gegenprobe 308/308; Dialog-Index: 04a (54, offen), 02c registriert, 55 Antworten |

### Was aus dieser Sitzung an Regeln bleibt

| | Regel |
|---|---|
| ⭐ | **Ein Datum, das erst zur Laufzeit feststeht, wird einmal gemessen, in eine Datei geschrieben und von dort an jeden Lauf gegeben** (`a4_datum.txt`) — Probelauf, echter Lauf und Nachweise rechnen so mit demselben Wert, und der Soll-Hash ist nachbaubar |
| | **Texte, die ein Auftrag als Codespanne oder Codeblock vorgibt, liest das Skript aus dem Auftrag am Commit ⟨S0⟩, statt sie abzutippen** (`c2_index_eintraege.py`: Liste Nr. 1–7 und Vorspann); eingesetzt werden nur die Platzhalter |
| | **Eine Vorhersage des Zuschnitts nach dem Verfahren des Werkzeugs trifft auf das Byte** (T4, T5) — gierig von Abschnitt 0 an, Kopf 236 B |

### Was offen bleibt

- 54.6 (10 Punkte), „Für Fable“ im Ergebnis (54.6 Nr. 2, 6, 7, 9, 10; `--marken` zählt drei Zeilen aus 54 mit).
- Index: Kopf „*Frühere Vierteilung*“ nennt „T1“ … „T4“, die Liste danach fünf Teile (für TB-133).
- `registerbericht.py --pruefen` rc 1 schon vor TB-126 (Zahlenteil veraltet).
- Ablage der 55 Abschnittsdateien, der fünf Teile, des Index und des Dialog-Index — steuernder Chat.
- Nächste Journalkennung nach EE: **EF**.

*Geschrieben 05.10.2026 von der Mac-Sitzung TB-136. Quellenvermerk: siehe Kopf.*

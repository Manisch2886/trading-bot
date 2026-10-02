## EA — TB-129: Register Abschnitt 51 — Fable 01a (R56–R62) zeichengleich, Tatsachennotizen 51.8–51.10, 14 Marken am alten Ort; numstat 131/0, R-Diff 7/7, Zitate 2/2, `test_vorregistrierung` 196/196; Registerkopie 52 Abschnittsdateien und 4 Teile neu, Index und Dialog-Index nachgezogen (02.10.2026)

*Quelle: `docs/ERGEBNIS_TB-129_register_fable_01a.md`*

**Quelle:** Mac-Sitzung **TB-129** (Hauptordner), 02.10.2026, Eingang `560ca75`. Commits `477cef2` (Schritt 0),
`b443bcb` (0), `f63ad4c` (A, einziger Registercommit), `33b0999` (B/C) und der Abgabe-Commit. Belege
`docs/belege/TB-129/`. Freigabe des Betreibers 02.10.2026 (Auswahlkarte, gestellt 09:13, eingetragen 10:02). Keine
Rückfrage an den Betreiber. Kein Abbruchkriterium ausgelöst.

### Was gemessen ist

| | |
|---|---|
| **0** | 0a drei Einträge wie Soll; Ausgang wie Soll (11 094 Z., `b5804659…`, `register()` `525c9c42…`, Sonde 37/0/0, (ii) 0, JSON `9f7364ef…`); 0c leer ⇒ Basis 196/196 aus TB-126; 0d: Prüfskript aus Anhang A am ⟨S0⟩ (per `git archive`) rc 0, 14/14 Marken, 43 Fundstellen, Kalender, Git-Tatsachen 3/3 |
| ⭐⭐ **A** | Probelauf an Kopie, dann echt, `cmp` gleich. R-Diff **7/7**, Mutation rc 1, Zitate **2/2**, Überschriften und Ketten 7/7, Marken **14/14**, numstat **131/0**, Abschnitt 10 und ERZEUGT-Block bytegleich, Sonde-JSON ohne `zeilen` gleich, `registerbericht --pruefen` gleich (rc 1, schon vorher), `register()` → `a1e1366a…`, 196/196 (865 s) |
| **B** | BACKLOG-Block 01a + Übernahme: Anker 1, numstat 17/0, bytegleich |
| **C** | Kopie 0–22 / 23–36 / 37–42 / 43–51 und 52 Abschnittsdateien, alle `--pruefen` bytegleich; Index: 184 Zahlen umgeschrieben, Abschnitt 6 mit 14 Marken und 6 Indexzeilen, Gegenprobe 212/212; Dialog-Index: Zeile 01a (51, offen), 51 Antworten |

### Was aus dieser Sitzung an Regeln bleibt

| | Regel |
|---|---|
| ⭐ | **Ein Zeilen-Umschreiber muss jede Zahl einer Liste und eines Bereichs abbilden, nicht nur die erste.** Die Vorlage aus TB-126 tat das nicht; es fiel nur nicht auf, weil zwischen den Enden nie eine Einfügung lag |
| | **Ein Prüfskript, das vom Dateisystem liest, prüft „am Commit“ nur an einem ausgepackten Baum.** `git archive <S0> <pfade>` in den Scratch, dort aufrufen |
| | **Ein Registertext, der Marken aufzählt, wird selbst als Marke gezählt** (`--marken`: R61 als `MARKE`). Zählungen aus `--marken` gegen die gesetzten Marken abgleichen, nicht übernehmen |

### Was offen bleibt

- 51.10 (8 Punkte), „Für Fable“ im Ergebnis (Lesart 51.9, Tage in R60 (b)/(c), fünf Orte ohne Marke, Markenwort für
  Bestätigungen, `--marken` zählt R61).
- `registerbericht.py --pruefen` rc 1 schon vor TB-126 (Zahlenteil veraltet).
- Ablage der 52 Abschnittsdateien, des Index und des Dialog-Index — steuernder Chat, nach der 27.4-Prüfung.
- Nächste Journalkennung nach EA: **EB**.

*Geschrieben 02.10.2026 von der Mac-Sitzung TB-129. Quellenvermerk: siehe Kopf.*

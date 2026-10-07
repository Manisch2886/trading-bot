## EI — TB-139: Nachlesen der Voraussetzungen an Zwischenstand und Ergebnis TB-140 (V4 und V5 „erfüllt“, rc 0, 46/46 Zeilen); Register Abschnitt 55 — Fable 07a (R78–R83 in der Fassung 07.10.a) zeichengleich, Tatsachennotizen 55.7–55.8, 20 Marken am alten Ort, die Fassung 06.10.a nicht eingetragen; numstat 152/0, R-Diff 6/6, Zitate 2/2, `test_vorregistrierung` 196/196; zwei BACKLOG-Blöcke, Registerkopie 56 Abschnittsdateien und 5 Teile, Index und Dialog-Index nachgezogen (07.10.2026)

*Quelle: `docs/ERGEBNIS_TB-139_register_fable_07a.md`*

**Quelle:** Mac-Sitzung **TB-139** (Hauptordner, lokal), 07.10.2026, Eingang `b07ec7d`. Commits `e16872e` (Schritt 0),
`35b4743` (0), `ad1fc0d` (A, einziger Registercommit), `be2fa85` (B/C) und der Abgabe-Commit. Belege
`docs/belege/TB-139/`. Freigabe des Betreibers 07.10.2026 (Auswahlkarte, eingetragen 22:44). Datum des Eintrags zur
Laufzeit: 07.10.2026. Keine Rückfrage an den Betreiber. Kein Abbruchkriterium ausgelöst.

### Was gemessen ist

| | |
|---|---|
| **0** | 0a sechs Einträge wie Soll; drei Skripte aus Anhang A sha256 gleich, Prüfskript rc 0; Umstellskript 20/20 `ok`, 0 Abweichungen; Ausgang wie Soll (11 581 Z., `8d505a38…`, `register()` `cfff54ca…`, Sonde 37/0/0, (ii) 0, JSON `9f7364ef…`, Quelle 07a `388187e2…`/57 165 B); 0c leer ⇒ Basis 196/196 aus TB-136; 0d rc 0 |
| ⭐⭐ **0e** | Nachlesen statt Nachmessen: Zwischenstand TB-140 nennt V4 und V5 je in genau einer Zeile „erfüllt“, mit Kernzahl und Rohausgabe im Repo; V6, Z1, Z2 wie 55.7; das Ergebnis TB-140 nennt in „Für den steuernden Chat“ alle zwölf Urteile wie 55.7; Lock `96a5c572…` — 46/46 `ok`, rc 0 |
| ⭐⭐ **A** | Einfügeskript aus Anhang A unverändert, Probelauf an Kopie, dann echt, `cmp` gleich, `sha256 nachher` in beiden `ab97ae1e…` (Wachen zu R79 (a), R79 (b) und Platzhaltern liefen in beiden). R-Diff **6/6**, Mutation rc 1, Zitate **2/2**, Überschriften und Ketten 6/6, Marken **20/20** an den Soll-Zeilen, numstat **152/0**, Abschnitt 10 (jetzt Z. 971–1177) und ERZEUGT-Block bytegleich, Sonde-JSON gleich, `registerbericht --pruefen` gleich (rc 1, schon vorher), `register()` → `ee6947a6…`, 196/196 (919 s) |
| **B** | BACKLOG E1 und E2: Anker 1, numstat 18/0, beide GLEICH; J1 in diesem Block |
| **C** | Kopie 0–22 / 23–36 / 37–42 / 43–53 / 54–55, Grössen auf das Byte wie gerechnet (T4 236 927 B, 3 069 B Luft), 56 Abschnittsdateien, alle `--pruefen` bytegleich; `--marken` 100/145/96 wie erwartet; Index: 308 Zahlen umgeschrieben (271 geändert), neue Zeile 5.2 in Tabelle 2, Anhänge an 42/46/48/53/54 und neue Zeile 55 in Tabelle 4, Abschnitt 10 mit 20 Marken und drei Indexzeilen, Gegenprobe rc 0; Dialog-Index: 07a (55, offen), 06a (55, registriert), 04a unverändert, 57 Antworten |

### Was aus dieser Sitzung an Regeln bleibt

| | Regel |
|---|---|
| ⭐ | **Übernommene Skripte stellt ein Skript um, das je Vorlage und je Ergebnis den sha256 prüft und je Ersetzung die Zahl der Vorkommen** (`tb139_umstellen.py`) — 20 Skripte, 157 Ersetzungen, ohne Handarbeit und ohne Abweichung; eine geänderte Vorlage fiele vor dem ersten Lauf auf |
| | **Hat eine andere Sitzung gemessen, liest die eintragende Sitzung nur deren Urteile nach und misst nicht neu** — sonst stünden zwei Messungen ohne Regel nebeneinander; die Wache im Einfügeskript liest dieselbe Zeile noch einmal |

### Was offen bleibt

- 55.8 (14 Punkte), „Für Fable“ im Ergebnis (55.8 Nr. 5, 6, 9, 10, 12, 13; `--marken` zählt sieben Zeilen aus 55 mit).
- Index: Kopf „*Frühere Vierteilung*“ nennt weiter „T1“ … „T4“, die Liste danach fünf Teile.
- `registerbericht.py --pruefen` rc 1 schon vor TB-126 (Zahlenteil veraltet).
- Ablage der 56 Abschnittsdateien, der fünf Teile, des Index und des Dialog-Index — steuernder Chat.
- Nächste Journalkennung nach EI: **EJ**; nächster Mac-Auftrag TB-141; TB-137 steht weiter aus.

*Geschrieben 07.10.2026 von der Mac-Sitzung TB-139. Quellenvermerk: siehe Kopf.*

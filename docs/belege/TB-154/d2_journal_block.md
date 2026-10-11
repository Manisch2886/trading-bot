## ER — TB-154: Register Abschnitt 57 — Fable 10a (R90–R93) zeichengleich, Tatsachennotizen 57.5–57.6, 11 Marken am alten Ort an 9 Orten (2 nachgetragen nach R93 (a)); vorher gemessen: Dateien 10.10.a mit Commit im Repo, Punkt (1) der Antwort 25c, der Satz in 15.5, die 9 Orte; numstat 103/0, R-Diff 4/4, Zitate 2/2, `test_vorregistrierung` 196/196; zwei BACKLOG-Blöcke, Registerkopie 58 Abschnittsdateien und 5 Teile (T4 noch 165 B Luft), Index und Dialog-Index nachgezogen (11.10.2026)

*Quelle: `docs/ERGEBNIS_TB-154_register_fable_10a.md`*

**Quelle:** Mac-Sitzung **TB-154** (Hauptordner, lokal), 11.10.2026, Eingang `548b9a3`. Commits `4fbc2f3` (Schritt 0),
`336e752` (0), `3f2e97e` (A, einziger Registercommit), `bf6e992` (B/C) und der Abgabe-Commit. Belege
`docs/belege/TB-154/`. Freigabe des Betreibers 11.10.2026 (Auswahlkarte, eingetragen 13:23). Datum des Eintrags zur
Laufzeit: 11.10.2026. Keine Rückfrage an den Betreiber. Kein Abbruchkriterium ausgelöst; kein Aufruf abgelehnt.

### Was gemessen ist

| | |
|---|---|
| **0** | 0a vier Einträge wie Soll, HEAD `548b9a3`; drei Skripte aus Anhang A sha256 gleich, Prüfskript rc 0; Umstellskript 20/20 `ok`, 0 Abweichungen (132 Ersetzungen, Vorlagen aus TB-149); Ausgang wie Soll (11 920 Z., `b2d56949…`, `register()` `1ddb56ee…`, Sonde 37/0/0, (ii) 0, JSON `9f7364ef…`, Quelle 10a `2b60d686…`/30 026 B; Abschnitt 10 und ERZEUGT `cmp`-gleich mit TB-149); 0c leer ⇒ Basis 196/196 aus TB-149 |
| ⭐⭐ **0d** | rc 0: Anfrage, Übergabe und Antwort 10.10.a 3 von 3 von git verfolgt, in `82120cf` dazugekommen, md5 und Bytes wie Soll (R91 (h), R56 (b)); 30 Fundstellen, darunter Antwort 25c Z. 53 (Überschrift von Punkt (1)) und Z. 17 (Satz zum unbekannten Bedingungstext) (R91 (f)); der Satz aus 15.5 1-mal (Z. 1641–1643), nach ihm nur die Marke zu R53 (R93 (a)); 9 Orte je genau einmal, an keinem eine Zeile zum Block der neuen Marke; R90–R93 vorher in keiner Registerzeile |
| ⭐⭐ **A** | Einfügeskript aus Anhang A unverändert, Probelauf an Kopie, dann echt, `cmp` gleich, `sha256 nachher` in beiden `459be94e…`. R-Diff **4/4**, Mutation rc 1, Zitate **2/2**, Überschriften und Ketten 4/4, Marken **11/11** an den Soll-Zeilen, numstat **103/0**, Abschnitt 10 und ERZEUGT-Block bytegleich (wandern nicht), Sonde-Text und -JSON gleich, `registerbericht --pruefen` gleich (rc 1, schon vorher), `register()` → `08657b83…`, 196/196 (879 s) |
| **B** | BACKLOG E1 und E2: Anker 1 (Z. 452), numstat 17/0, beide GLEICH; J1 in diesem Block |
| **C** | Kopie 0–22 / 23–36 / 37–42 / 43–53 / 54–57, Grössen auf das Byte wie gerechnet (T4 239 831 B, **165 B Luft**), 58 Abschnittsdateien, alle `--pruefen` bytegleich; `--marken` 117/179/105 wie erwartet; Index: 410 Zahlen umgeschrieben (312 geändert), Anhang an Tabelle 3 „3a Universum“ und Tabelle 4 an 27/48/55/56, neue Zeile 57, Abschnitt 12 mit 11 Marken und drei Indexzeilen, Gegenprobe rc 0; Dialog-Index: 10a (57, offen „ja“), 09a unverändert, 59 Antworten; dazu Zeile 25c Fundstelle „42“ → „42, 57“ (Werkzeug liest Fundstellen aus dem Register) |

### Was aus dieser Sitzung an Regeln bleibt

| | Regel |
|---|---|
| | **Nennt ein neuer Registerabschnitt die Datei einer früheren Fable-Antwort, ändert `dialog_index.py` auch deren Zeile** (Spalte Fundstelle) — das Soll eines Folgeauftrags für C4 sollte damit rechnen, statt nur die neue Zeile und die Schlusszeile zu erwarten |

### Was offen bleibt

- 57.6 (8 Punkte), „Für Fable“ im Ergebnis (57.6 Nr. 4 bis 8; `--marken` zählt sieben Zeilen aus 57 mit).
- ⚠️ T4 der Registerkopie (Abschnitte 43–53) hat nur noch 165 B Luft; die zweite weitere Marke dort teilt neu.
- Index: Kopf „*Frühere Vierteilung*“ nennt weiter „T1“ … „T4“, die Liste danach fünf Teile.
- `registerbericht.py --pruefen` rc 1 schon vor TB-126 (Zahlenteil veraltet).
- Ablage der 58 Abschnittsdateien, der fünf Teile, des Index und des Dialog-Index — steuernder Chat.
- Nächste Journalkennung nach ER: **ES**; R-Blöcke frei ab R94.

*Geschrieben 11.10.2026 von der Mac-Sitzung TB-154. Quellenvermerk: siehe Kopf.*

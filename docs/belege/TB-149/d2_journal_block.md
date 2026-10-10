## EO — TB-149: Register Abschnitt 56 — Fable 09a (R84–R89) zeichengleich, Tatsachennotizen 56.7–56.8, 31 Marken am alten Ort an 21 Orten (5 nachgetragen nach R89 (d)); vorher gemessen: Dateien 09.10.a mit Commit im Repo, an keinem Ort schon eine Marke zum Block der neuen; numstat 187/0, R-Diff 6/6, Zitate 2/2, `test_vorregistrierung` 196/196; zwei BACKLOG-Blöcke, Registerkopie 57 Abschnittsdateien und 5 Teile (T4 noch 313 B Luft), Index und Dialog-Index nachgezogen (10.10.2026)

*Quelle: `docs/ERGEBNIS_TB-149_register_fable_09a.md`*

**Quelle:** Mac-Sitzung **TB-149** (Hauptordner, lokal), 10.10.2026, Eingang `15775a7`. Commits `c71dca9` (Schritt 0),
`ca687fc` (0), `d950e03` (A, einziger Registercommit), `21ec3f5` (B/C) und der Abgabe-Commit. Belege
`docs/belege/TB-149/`. Freigabe des Betreibers 10.10.2026 (Auswahlkarte, eingetragen 11:26). Datum des Eintrags zur
Laufzeit: 10.10.2026. Keine Rückfrage an den Betreiber. Kein Abbruchkriterium ausgelöst; kein Aufruf abgelehnt.

### Was gemessen ist

| | |
|---|---|
| **0** | 0a drei Einträge wie Soll, HEAD `15775a7`; drei Skripte aus Anhang A sha256 gleich, Prüfskript rc 0; Umstellskript 20/20 `ok`, 0 Abweichungen (129 Ersetzungen, Vorlagen aus TB-139); Ausgang wie Soll (11 733 Z., `ab97ae1e…`, `register()` `ee6947a6…`, Sonde 37/0/0, (ii) 0, JSON `9f7364ef…`, Quelle 09a `a6e5d3d2…`/52 721 B; Abschnitt 10 und ERZEUGT `cmp`-gleich mit TB-139); 0c leer ⇒ Basis 196/196 aus TB-139 |
| ⭐⭐ **0d** | rc 0: Anfrage, Eröffnungstext und Antwort 09.10.a 3 von 3 von git verfolgt, in `7f0b59d` dazugekommen, md5 und Bytes wie Soll (R88 (g), R56 (b)); 21 Orte je genau einmal; vom Anker bis vor die nächste Überschrift nennt an keinem Ort eine Zeile den Block der neuen Marke (an 48.14 kein R60, R64, R66, R67; an 48.7 kein R81); R84–R89 vorher in keiner Registerzeile |
| ⭐⭐ **A** | Einfügeskript aus Anhang A unverändert, Probelauf an Kopie, dann echt, `cmp` gleich, `sha256 nachher` in beiden `b2d56949…`. R-Diff **6/6**, Mutation rc 1, Zitate **2/2**, Überschriften und Ketten 6/6, Marken **31/31** an den Soll-Zeilen, numstat **187/0**, Abschnitt 10 und ERZEUGT-Block bytegleich (wandern nicht), Sonde-Text und -JSON gleich, `registerbericht --pruefen` gleich (rc 1, schon vorher), `register()` → `1ddb56ee…`, 196/196 (905 s) |
| **B** | BACKLOG E1 und E2: Anker 1 (Z. 384), numstat 20/0, beide GLEICH; J1 in diesem Block |
| **C** | Kopie 0–22 / 23–36 / 37–42 / 43–53 / 54–56, Grössen auf das Byte wie gerechnet (T4 239 683 B, **313 B Luft**), 57 Abschnittsdateien, alle `--pruefen` bytegleich; `--marken` 114/167/102 wie erwartet; Index: 348 Zahlen umgeschrieben (199 geändert), Anhänge an 23/40/41/48/52/53/54/55 und neue Zeile 56 in Tabelle 4, Abschnitt 11 mit 31 Marken und drei Indexzeilen, Gegenprobe rc 0; Dialog-Index: 09a (56, offen „ja“), 07a unverändert, 58 Antworten |

### Was aus dieser Sitzung an Regeln bleibt

| | Regel |
|---|---|
| ⭐ | **Liegen die Fable-Dateien schon mit Commit im Repo, misst die eintragende Sitzung das vor dem Eintrag selbst** (verfolgt, Commit, md5, Arbeitsbaum gleich HEAD) — die Vormessung des steuernden Chats ist kein Nachweis; Prüfskript und Einfügeskript tragen die Sperre |
| | **Nachgetragene Marken zu Blöcken früherer Antworten brauchen eine Wache gegen Doppelsetzen am ganzen Ort** (vom Anker bis vor die nächste Überschrift, jede Zeile, nicht nur Markenzeilen) — sonst stünde eine Marke zweimal, wenn eine frühere Sitzung sie schon gesetzt hätte |

### Was offen bleibt

- 56.8 (17 Punkte), „Für Fable“ im Ergebnis (56.8 Nr. 9 bis 12 und 14 bis 17; `--marken` zählt elf Zeilen aus 56 mit).
- ⚠️ T4 der Registerkopie (Abschnitte 43–53) hat nur noch 313 B Luft; die zweite weitere Marke dort teilt neu.
- Index: Kopf „*Frühere Vierteilung*“ nennt weiter „T1“ … „T4“, die Liste danach fünf Teile.
- `registerbericht.py --pruefen` rc 1 schon vor TB-126 (Zahlenteil veraltet).
- Ablage der 57 Abschnittsdateien, der fünf Teile, des Index und des Dialog-Index — steuernder Chat.
- Nächste Journalkennung nach EO: **EP**; R-Blöcke frei ab R90.

*Geschrieben 10.10.2026 von der Mac-Sitzung TB-149. Quellenvermerk: siehe Kopf.*

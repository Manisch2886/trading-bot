# ERGEBNIS TB-167 — Abhilfe G6 elliott_wave_stocks: Schranke vor dem Schnitt (R102 (c)), Register 62 (R100–R103), Marken

**Sitzung:** TB-167, Mac (Claude Code, Opus 5.5), 16.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-167_g6_ews_schranke_vor_schnitt.md` · **Zweig:** `main`
**Commits:** `bc5e165` (S0, Schritt 0: Stand des steuernden Chats vor TB-167) · `4370857` (R, Register 62 und sechs Marken) · `962c652` (K, Registerkopie, Index, Dialog-Index) · `b6aaa24` (M, Abhilfe und Messungen) · danach der Abgabe-Commit „TB-167 Abgabe: Ergebnis, BACKLOG, Journal FC“, der dieses Ergebnis enthält, und „TB-167 F: porcelain“.
**Belege:** `docs/belege/TB-167/` · **Journal:** FC · **Kein Abbruch.**

## Kurz

Die Freigabe-Karte (bedingt) war gefüllt. 0a zeigte die 32 Soll-Einträge an `5167e96`; das Werkzeug kam mit dem Soll-Hash `ea67434e…`. `WZ sichere` hat die 22 Dateien des abgebrochenen TB-166 nach `$HOME/tb167_sicherung` gesichert (89 Prüfungen, kein NEIN), die 20 verfolgten auf `5167e96` zurückgesetzt und die 2 unverfolgten Tests verschoben; 0a2 zeigte danach die 10 Soll-Einträge. V: 20 Prüfungen ohne NEIN, ein Befund zu R100 (c) (unten). Register 62 ist angehängt (62.1–62.4 = R100–R103 zeichengleich, 62.5), dazu sechs Marken (5.1 Nr. 4, 53.7, 55.1, 55.2, 55.4, 60.1); die Marke an 53.7 ist gesetzt, weil R72 (c) den Go-Live-Schnitt nicht nennt. In K endeten sechs Schritte mit rc 0, zwei mit rc 1 (Dialog-Index, unten). M: Die Gegenprobe ist erfüllt (alter Code: G6 rot, Plan ab 2021). Nach dem Tausch der zwei Blöcke ist G6 grün (196/196), test_posten4_horizont grün (34/34) und der Plan 2017–2025. Die Abhilfe ist erst danach mit `b6aaa24` committet.

## Was gemessen ist

| Beleg | Ergebnis |
|---|---|
| `0a_status.txt` | Liste der 32 Einträge (ohne rc-Zeile); Ausgabe `0a gut (32 Eintraege)` |
| `0_sichere.txt` | 89 Prüfungen, NEIN 0 · rc 0 |
| `0a2_status.txt` | Liste der 10 Einträge (ohne rc-Zeile); Ausgabe `0a2 gut (10 Eintraege)` |
| `v_voraussetzung.txt` | 20 Prüfungen, NEIN 0, Befund R100 (c) gemeldet · rc 0 |
| `r_probe.txt` | 4 Prüfungen, NEIN 0 · rc 0 |
| `r_eintrag.txt` | 9 Prüfungen, NEIN 0; Marken Z. 634, 11603, 11757, 11767, 11796, 12201; Abschnitt 62 Z. 12291 · rc 0 |
| `k_registerkopie.txt` | Teile 1–6, bytegleich (sha256 `6026c2ab59785156`) · rc 0 |
| `k_abschnitte.txt` | Abschnitte 0–62, 63 Dateien, bytegleich · rc 0 |
| `k_pruefen.txt` | bytegleich · rc 0 |
| `k_index_zeilen.txt` | 458 Zeilenangaben umgeschrieben, davon 419 geändert · rc 0 |
| `k_index.txt` | 5 Prüfungen, NEIN 0; 62 in T6, neuer Abschnitt 15 (6 Marken) · rc 0 |
| `k_handfelder.txt` | Handfelder 15b, 16b, 16a (–) · rc 0 |
| `k_dialog_index.txt` | 65 Zeilen = 65 Antworten; 64 von 65 Zeilen voll; Zeile 16a `offen='–'` · **rc 1** (kein Abbruch in K) |
| `k_dialog_pruefen.txt` | wie oben · **rc 1** |
| `m1_test_alt.txt` | 195 bestanden, 1 GESCHEITERT: G6 elliott_wave_stocks (Selektionsfalten 2021–2025) · rc 1 (Soll) |
| `m1_g6_rot.txt` | Gegenprobe: genau ein Fehler, G6 elliott_wave_stocks · rc 0 |
| `m2_plan_alt.txt` | Selektionsfalten 2021–2025, beginnen nicht 2017; porcelain vorher = nachher · rc 0 |
| `m3_code_probe.txt` | Block Z. 111 genau einmal; nur Reihenfolge und eine Kommentarzeile · rc 0 |
| `m3_code.txt` | vorher `3b775700…`, nachher `0298263c…` · rc 0 |
| `m4_test_neu.txt` | 196/196 bestanden · rc 0 |
| `m4_g6_gruen.txt` | kein Fehler · rc 0 |
| `m5_posten4.txt` | 34 von 34 bestanden (dazu eine schon vorhandene INFO-Zeile: volatility_breakout tz-naive/tz-aware, ausserhalb E-6, nicht gezählt) · rc 0 |
| `m6_plan_neu.txt` | Selektionsfalten 2017–2025, Bestätigung 2026-01-01/2026-09-01; erste_falte_4a 2017; porcelain vorher = nachher · rc 0 |

Vor dem Commit M zeigte `git status --porcelain` genau ` M strategies/elliott_wave_stocks/multi_symbol_optimise.py` und die neun Belege m1_ bis m6_ einzeln.

**Befund R100 (c)** (aus `v_voraussetzung.txt`, wird gemeldet, kein Abbruch): In `d9f8489` (`docs/belege/TB-148/leseprotokoll.md`) sind 38 Zellen in bestehenden Spalten geändert. 11 davon treffen Fundstellen aus R90 (e), R91 (a)–(c) und R92 (a): die neun `multi_symbol_optimise.py`, Messpunkt „M2 (auch M3, M4)“→„M2 (auch M4)“, sowie `research/faltenplan_neun/faltenschranke_messung.py`, Zeilenbereich 1–534→1–533, und `shared/zuteilung.py`, Zeilenbereich 1–799→1–798.

**Befund K:** `dialog_index.py` endet mit rc 1, weil die Handfelder für 16a nach Anhang A `offen='–'` tragen. Diesen Wert erzeugt das Werkzeug selbst, `handfelder` setzt 16a ausdrücklich auf „–“. Erwartet sind dort `ja` oder `nein`. Den Wert setzt der steuernde Chat.

## Entwurf der Tatsachennotiz nach 37.3

| Datei | vorher | nachher | Commit | vollzieht |
|---|---|---|---|---|
| `strategies/elliott_wave_stocks/multi_symbol_optimise.py` | `3b7757004b1c2db527262cbacf0f86c095729080074e73ced750b82fc8677232` | `0298263c755c5d24ccff09c35aa447efd4fff70f05223942813361955e0362e6` | `b6aaa24` | R102 (c) (Posten 4; R44, R81 (d); E-6 berichtigt) |

Entwurf, nicht eingetragen (TB-167, 16.10.2026). Freigabe: Karte im Auftrag TB-167. Sonde Punkt 11: nicht gemessen (Abbild führt keinen Optimierer, 60.1).

## Was offen bleibt

- Vollzug nach 37.3: die Tatsachennotiz oben eintragen (Folgeauftrag, Bauart 60).
- R102 (d): vor der Neuerzeugung der Listen (R44) zu messen, nur das Ob.
- R101 (a), zweite Hälfte: ob ein UCITS-Fonds auf ein einzelnes Edelmetall besteht, ist im Repo nicht messbar.
- Befund R100 (c): 11 Fundstellen in geänderten Zellen von `d9f8489` (oben). Urteil beim steuernden Chat.
- Dialog-Index Zeile 16a: `offen` ist „–“ (rc 1 in K).
- Ein neues Abbild der Sperrliste fehlt noch (nicht Teil dieses Auftrags).
- TB-166 E-3a muss auf diesem Stand neu gebaut werden: Der VOR-Hash von ews im Auftrag TB-166 passt nicht mehr.
- Sicherung `$HOME/tb167_sicherung` (22 Dateien TB-166 mit `SHA256SUMS`) bleibt liegen. `WZ zurueck` geht nicht mehr, weil HEAD nicht mehr `5167e96` ist. Zurück nur von Hand und auf Anweisung, wie im Auftrag beschrieben.

## In einfacher Sprache

Der Bot elliott_wave_stocks hat geprüft, ob ein Symbol genug Kursgeschichte hat, erst nachdem er die Zeilen vor dem Horizontbeginn abgeschnitten hatte. Deshalb fielen in der Probe G6 die Jahre 2017 bis 2020 weg. Zuerst wurden die abgebrochenen Änderungen von TB-166 sicher ausserhalb des Repos abgelegt. Dann kamen die vier Regeltexte wortgleich ins Register (Abschnitt 62). Danach wurde gemessen, dass die alte Reihenfolge G6 wirklich rot macht. Erst dann wurden die beiden Blöcke getauscht: erst die Länge prüfen, dann schneiden, wie bei rsi2. Jetzt ist G6 grün, der andere Test auch, und der Plan reicht wieder von 2017 bis 2025. Erst nach diesen Messungen wurde die Änderung committet. Den neuen Hash in die Sperrliste einzutragen, ist ein eigener nächster Auftrag.

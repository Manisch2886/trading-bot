## FC — TB-167: Abhilfe G6 elliott_wave_stocks (Schranke vor dem Schnitt, R102 (c)), Register 62 (R100–R103), sechs Marken

*16.10.2026 · Commits `bc5e165` (S0), `4370857` (R), `962c652` (K), `b6aaa24` (M) · Ergebnis `docs/ERGEBNIS_TB-167_g6_ews_schranke_vor_schnitt.md` · Belege `docs/belege/TB-167/` · Quelle: Auftrag `docs/auftraege/MAC_TB-167_g6_ews_schranke_vor_schnitt.md`*

### Was gemessen ist

- Schritt 0: 0a 32 Einträge an `5167e96`, Werkzeug `ea67434e…`. `WZ sichere` rc 0 (89 Prüfungen): 22 TB-166-Dateien nach `$HOME/tb167_sicherung`, 20 auf `5167e96` zurückgesetzt, 2 Tests verschoben. 0a2 zeigte 10 Einträge.
- V rc 0 (20 Prüfungen). R72 (c) nennt den Go-Live-Schnitt nicht, also ist die Marke an 53.7 gesetzt. Befund R100 (c): 11 Fundstellen in geänderten Zellen von `d9f8489` (neun Optimierer M2 (auch M3, M4)→M2 (auch M4); faltenschranke_messung.py und zuteilung.py je Zeilenbereich −1).
- R: Abschnitt 62 an Z. 12291, R100–R103 zeichengleich. Sechs Marken: 5.1 Nr. 4, 53.7, 55.1, 55.2, 55.4, 60.1. Sonst append-only, rc 0.
- K: Registerkopie, Abschnitte, Prüfung, Indexzeilen, Index (T6, Abschnitt 15) und Handfelder je rc 0. Dialog-Index und `--pruefen` je rc 1, weil Zeile 16a `offen='–'` hat.
- M: Gegenprobe auf dem alten Code: Test 195/1, nur G6 ews rot, Plan 2021–2025. Abhilfe ews `3b775700…`→`0298263c…`. Danach Test 196/196, G6 grün, test_posten4_horizont 34/34, Plan 2017–2025. Commit erst nach diesen Messungen.

### Was offen bleibt

- Vollzug nach 37.3 (Folgeauftrag, Bauart 60), Entwurf in `docs/belege/TB-167/m_uebergang.md`.
- R102 (d); R101 (a), zweite Hälfte; Befund R100 (c); Dialog-Index 16a `offen`.
- Neues Abbild; TB-166 E-3a auf diesem Stand neu bauen; die Sicherung `$HOME/tb167_sicherung` bleibt liegen.

### In einfacher Sprache

elliott_wave_stocks prüft jetzt erst die Länge der Kursreihe und schneidet danach. Vorher war es umgekehrt, und dadurch fehlten in der Probe die Jahre 2017 bis 2020. Die Gegenprobe hat gezeigt, dass die alte Reihenfolge G6 rot macht. Mit der neuen ist alles grün, und der Plan umfasst wieder 2017 bis 2025.

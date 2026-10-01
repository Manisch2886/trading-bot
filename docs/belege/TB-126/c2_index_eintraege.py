#!/usr/bin/env python3
"""TB-126 C2/C3: REGISTER_INDEX.md nach E-2 nachziehen (nach c2_index_zeilen.py).

Jede Ersetzung hat einen Anker, der im Index genau einmal vorkommen muss, sonst Abbruch ohne Schreiben.
Inhalt: Kopf (Stand, Messhinweis, Teile), die 88 Marken aus E-2 in den Tabellen 1-4 (Zeilen aus
c2_index_e2_tabelle.md, gemessen mit registerkopie.py --marken), die sechs Indexzeilen aus Anhang A Liste A
(C3, je am alten Ort: Abschnitt 10 in Tabelle 2, Datenstand-Hash unter Abschnitt 18 in Tabelle 4), Zeilen
47-50 in Tabelle 4, neuer Abschnitt 5 (die Tabelle aller E-2-Marken) und der Pflegehinweis.
Regel des Index (Z. 13): PRAEZISIERT gilt als Kette (Spalte "gilt"), ERGAENZT/BERICHTIGT stehen unter "dazu".
Aufruf: trading-env/bin/python3 docs/belege/TB-126/c2_index_eintraege.py
"""
I = "docs/projektfuehrung/REGISTER_INDEX.md"
T5 = open("docs/belege/TB-126/c2_index_e2_tabelle.md", encoding="utf-8").read().rstrip("\n")

E = [
# Kopf
("""am Commit `1e11457` (27.09.2026), Abschnitte 0–46,
10 347 Zeilen, sha256 `18e39ee2…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4). **Das""",
 """am Commit `db108a6` (01.10.2026), Abschnitte 0–50,
11 094 Zeilen, sha256 `b5804659…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2). **Das"""),
("(das Suchmuster des Auftrags, Art `MARKE`, 23 Zeilen)", "(das Suchmuster des Auftrags, Art `MARKE`, 55 Zeilen)"),
("(Art `MARKE+`, 42 Zeilen)", "(Art `MARKE+`, 98 Zeilen)"),
("Art `UEBERSCHRIFT`, 49 Zeilen). Die\nAusgabe liegt in `docs/belege/TB-118/a4_marken.txt`.",
 "Art `UEBERSCHRIFT`, 76 Zeilen). Die\nAusgabe liegt in `docs/belege/TB-126/c1_marken.txt` (zuvor `docs/belege/TB-118/a4_marken.txt`)."),
("""| 1 | 0–23 | 1–4025 |
| 2 | 24–37 | 4026–6999 |
| 3 | 38–43 | 7000–9571 |
| 4 | 44–46 | 9572–10347 |""",
 """| 1 | 0–22 | 1–3818 |
| 2 | 23–36 | 3819–6839 |
| 3 | 37–42 | 6840–9480 |
| 4 | 43–50 | 9481–11094 |"""),
# Tabelle 1
("| 2 Selektionsstatistik | 1, T1 | – | 1, T1 | – |",
 "| 2 Selektionsstatistik | 1, T1 | Z. 80 ERGÄNZT (Verweis) durch R51 (48.19) | 1, T1 | 48.19 R51: Verweis auf 15.3 (c) und Formelzeile (T4) |"),
("| 3 Beurteilung | 1, T1 | – | 1, T1 | – |",
 "| 3 Beurteilung | 1, T1 | Z. 77 **PRÄZISIERT durch R48 (48.16)** | 1 **mit** 48.16 R48 (j), T1+T4 | – |"),
("| 4 Drawdown-Bedingung | 1, T1 | – | 1, T1 (Herleitung Abschnitt 4) |",
 "| 4 Drawdown-Bedingung | 1, T1 | Z. 74 **PRÄZISIERT durch R48 (48.16)** | 1 **mit** 48.16 R48 (a), T1+T4 (Herleitung Abschnitt 4) |"),
# Tabelle 2
("| 3 „Der Faltenplan“ | Z. 411 ERSETZT durch Abschnitt 15, Registertext 2 und 4 | 15.4, 15.6 → weiter nach Tabelle 3 |",
 """| Kopf „Stand: 14.09.2026“ | Z. 6 ERGÄNZT durch R49 (48.17) | am Ort; dazu 48.17 R49 (f) (T4) |
| 2.1 Wie sie entstehen | Z. 127 **PRÄZISIERT durch R48 (48.16)** | 2.1 **mit** 48.16 R48 (i) (T4) |
| 2.2 Die vier zulässigen … | Z. 144 **PRÄZISIERT durch R48 (48.16)**; Z. 147 ERGÄNZT durch R49 (48.17) | 2.2 **mit** 48.16 R48 (h); dazu 48.17 R49 (a) (T4) |
| 2.5 Die Kantenregel | Z. 203 **PRÄZISIERT durch R48 (48.16)** | 2.5 **mit** 48.16 R48 (f) (T4) |
| 2.7 Stufung | Z. 244 ERGÄNZT durch R49 (48.17) | am Ort; dazu 48.17 R49 (b) (T4) |
| 3 „Der Faltenplan“ | Z. 411 ERSETZT durch Abschnitt 15, Registertext 2 und 4; Zahlenteil: Z. 459 ERGÄNZT durch R49 (48.17) | 15.4, 15.6 → weiter nach Tabelle 3; Zahlenteil dazu 48.17 R49 (c) (T4) |
| 4.2 | Z. 516 ERGÄNZT (Verweis) durch R51 (48.19) | am Ort; dazu 48.19 R51 (T4) |
| 4.4 | Z. 571 ERGÄNZT durch R49 (48.17) | am Ort; dazu 48.17 R49 (c) (T4) |"""),
("| 5.1 „Die Regeln“ | Z. 580 ERSETZT durch Abschnitt 15, Registertext 0, 2 und 4 | 15.2, 15.4, 15.6 → weiter nach Tabelle 3 |",
 "| 5.1 „Die Regeln“ | Z. 580 ERSETZT durch Abschnitt 15, Registertext 0, 2 und 4; Nr. 7: Z. 634 **PRÄZISIERT durch R37 (48.5)** | 15.2, 15.4, 15.6 → weiter nach Tabelle 3; Nr. 7 **mit** 48.5 R37 (T4) |"),
("| 5.3 „Krypto: Platzhalter mit Regel“ | Z. 663 ERSETZT durch Abschnitt 15, Registertext 3 und 4 | 15.5, 15.6 → weiter nach Tabelle 3 |",
 """| 5.3 „Krypto: Platzhalter mit Regel“ | Z. 663 ERSETZT durch Abschnitt 15, Registertext 3 und 4; Z. 688 ERGÄNZT (Verweis) durch R51 (48.19) | 15.5, 15.6 → weiter nach Tabelle 3; dazu 48.19 R51 (T4) |
| 7, Tabelle (a) und (d) | Z. 798 (d) **PRÄZISIERT durch R48 (48.16)**; Z. 801 (a) ERGÄNZT (Verweis) durch R51 (48.19); Z. 804 (d) ERGÄNZT durch R55 (49.3) | 7 (d) **mit** 48.16 R48 (c); dazu 49.3 R55 (leere Menge), 48.19 R51 (T4) |
| 7.1 Die drei Regeln … | Z. 847 ERGÄNZT durch R21 (47.4); Z. 850 **PRÄZISIERT durch R23 (47.6)** | 7.1 **mit** 47.6 R23; dazu 47.4 R21 (T4) |
| 8.1 Zufalls-Timing-Test | Z. 899 **PRÄZISIERT durch R48 (48.16)** | 8.1 **mit** 48.16 R48 (g); R48 (g) BERICHTIGT durch 49.2 R54 (Z. 10850) (T4) |
| 9, erster Absatz („N = 653 plus …“) | Z. 911 **PRÄZISIERT durch R48 (48.16)** (einzige Marke in 9) | 9 **mit** 48.16 R48 (b) (T4) |"""),
("| 10 Sperrliste | Z. 1004 (MARKE+: der Kasten an Punkt 4 sagt „nicht (iii) (ERSETZT-Marke)“, Form (ii) nach 38.4) | 10, Punkttext unverändert; Vollzug Punkt 4 in 39.2 (T3). Die Sperrlisten-Einträge 36.1, 36.6, 37.2 und 37.3 gehen in Tabelle 4 |",
 """| 10 Sperrliste | Z. 1004 (MARKE+: der Kasten an Punkt 4 sagt „nicht (iii) (ERSETZT-Marke)“, Form (ii) nach 38.4) | 10, Punkttext unverändert; Vollzug Punkt 4 in 39.2 (T3). Die Sperrlisten-Einträge 36.1, 36.6, 37.2 und 37.3 gehen in Tabelle 4 |
| ↳ 10, künftiger Punkt 15 (die neun neuen Trade-Listen) | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 48.10 R42 (T4) |
| ↳ 10, Sperrlistenpunkt 10 (Zuteilungskaskade, `shared/zuteilung.py`) | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 48.13 R45 (T4) |
| ↳ 10.1, „Stichproben-Hash-Vergleich“ | **Indexzeile E-2**, keine Marke (Abschnitt 10) | lies „Hash-Vergleich aller Ausgabedateien …“: 48.16 R48 (k) (T4) |
| ↳ 10, „Fortschreibung derselben Tatsache (15.09.2026, nach dem Lauf)“ | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 48.17 R49 (g); R51: 48.19 (T4) |
| ↳ 10, Sperrlistenpunkt 14 („Die Reihenfolge Selektion → Bestätigungsperiode → Bericht“) | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 47.13 R30 (T4) |
| 11, 11.2, 11.3 | Z. 1207 (11.2) ERGÄNZT durch R43 (48.11); Z. 1226 (11) ERGÄNZT durch R49 (48.17); Z. 1229 (11.3) ERGÄNZT durch 50.3 und 50.4 | am Ort; dazu 48.11 R43, 48.17 R49 (h), Vollzug Posten 3 in 50.3/50.4 (T4) |"""),
("| 12 Vollständigkeitstest | – | 12. **Dazu:** 40.7 Ergänzung (T3), 41.1 A1 Berichtigung „sieben Mutationsproben“ (T3), 46.5 R14 Ergänzung (T4) |",
 "| 12 Vollständigkeitstest | Z. 1297, 1300, 1303, 1306 ERGÄNZT durch R25 (47.8), R26 (47.9), R49 (48.17), R50 (48.18) | 12. **Dazu:** 40.7 Ergänzung (T3), 41.1 A1 Berichtigung „sieben Mutationsproben“ (T3), 46.5 R14 Ergänzung (T4), 47.8 R25, 47.9 R26, 48.17 R49 (d), 48.18 R50 (T4) |"),
("| alle übrigen (0, 2, 4, 6–9, 11, 13, 14) | – | am Ort, T1 |",
 "| alle übrigen (0, 6, 13, 14 und die oben nicht genannten Unterabschnitte von 2, 4, 7–9) | – | am Ort, T1 |"),
# Tabelle 3
("| **1a** Bootstrap (a) | 15.3 (a) | – | **15.3 (a)** | 24.2 beruft sich auf 1a; Z. 4205 „Registertext 1a bleibt in 15.3“ |",
 "| **1a** Bootstrap (a) | 15.3 (a) | – | **15.3 (a)** | 24.2 beruft sich auf 1a; Z. 4205 „Registertext 1a bleibt in 15.3“; 15.3 insgesamt: Z. 1446 ERGÄNZT durch R35 (48.3) (T4) |"),
("| **1b** | 15.3 (b) | – | **15.3 (b)** | – |",
 "| **1b** | 15.3 (b) | – | **15.3 (b)** | Z. 1425 ERGÄNZT durch R41 (48.9) (T4) |"),
("| **2a–2c** Faltenzuordnung | 15.4 (a)–(c) | – | **15.4 (a)–(c)** | – |",
 "| **2a–2c** Faltenzuordnung | 15.4 (a)–(c) | – | **15.4 (a)–(c)** | 2a: Z. 1474 **BERICHTIGT durch R54 (49.2)** („lies“); 15.4 insgesamt: Z. 1519 ERGÄNZT durch R41 (48.9) und 50.1 (T4) |"),
("| **2d** Embargo | 15.4 (d) | Z. 1469 ERSETZT durch 16.6 | **16.6** (T1) |",
 "| **2d** Embargo | 15.4 (d) | Z. 1469 ERSETZT durch 16.6 → Z. 2317 PRÄZISIERT durch R37 (48.5) | **16.6** (T1) **mit** 48.5 R37 (T4) |"),
("| **3a** Universum | 15.5 (a) | Tabelle darunter: Z. 1556 KORRIGIERT in 16.1.3 (MARKE+) | **15.5 (a)**, Rechenweg der Krypto-Zeile **16.1.3** | – |",
 "| **3a** Universum | 15.5 (a) | Tabelle darunter: Z. 1556 KORRIGIERT in 16.1.3 (MARKE+) | **15.5 (a)**, Rechenweg der Krypto-Zeile **16.1.3** | 15.5 insgesamt: Z. 1634 ERGÄNZT durch R53 (49.1) (T4) |"),
("| **3b (d), (e)** | 16.7 (d), (e) | – | **16.7 (d), (e)** | – |",
 "| **3b (d), (e)** | 16.7 (d), (e) | – | **16.7 (d), (e)** | (d): Z. 2381 ERGÄNZT durch R38 (48.6) (T4) |"),
("Drawdown Mark-to-Market, **ohne Marke in 15.6**, T2) |",
 "Drawdown Mark-to-Market, **ohne Marke in 15.6**, T2); Z. 1714 ERGÄNZT (Verweis) durch R51 (48.19) (T4) |"),
("| **4b, 4c** | 15.6 (b), (c) | – | **15.6 (b), (c)** | – |",
 "| **4b, 4c** | 15.6 (b), (c) | (c): Z. 1664 **PRÄZISIERT durch R23 (47.6)** | **15.6 (b), (c)**, (c) **mit** 47.6 R23 (T4) | – |"),
("| **6** Budgetstufen (a)–(m) | 16.4 | – | **16.4** (T1) | 22.4",
 "| **6** Budgetstufen (a)–(m) | 16.4 | Z. 2076–2171: 18 Marken, davon 14 **PRÄZISIERT** durch R18–R23 (47.1–47.6) und R37 (48.5) — Liste in Abschnitt 5 | **16.4** (T1) **mit** 47.1–47.6 und 48.5 für (a)–(d), (h)–(m) (T4) | 47.3 R20 Ergänzung zu (j), (l); 47.7 R24 Tatsachennotiz zu (g), (h) mit 50.6 (T4); 22.4"),
# Tabelle 4
("| 18 Tatsachennotiz 5/5a, Snapshot | 1 | Tatsachennotiz | – |",
 """| 18 Tatsachennotiz 5/5a, Snapshot | 1 | Tatsachennotiz | Z. 3059 ERGÄNZT durch R28 (47.11) (T4) |
| ↳ 17.3, 17.9, 18 — Datenstand-Hash voll | 1 | **Indexzeile E-2**, keine Marke (R51 verlangt Indexzeile) | 48.19 R51 (T4) |"""),
("38.3 Tatsachennotiz zu 21.9 |", "38.3 Tatsachennotiz zu 21.9; 21.4: Z. 3401 ERGÄNZT durch R53 (49.1) (T4) |"),
("22.4 Ergänzung zu RT 6 | – |", "22.4 Ergänzung zu RT 6 | 22.2: Z. 3676 ERGÄNZT durch R34 (48.2) (T4) |"),
("24.4 Festlegung 1 | 24.6 Tatsachennotiz |", "24.4 Festlegung 1 | 24.6 Tatsachennotiz; 24.2 **PRÄZISIERT durch R36 (48.4)** (Z. 4293, T4) |"),
("| (i) **PRÄZISIERT durch 26.2** (Z. 4649) |",
 "| (i) **PRÄZISIERT durch 26.2** (Z. 4649) und **durch R53 (49.1)** (Z. 4651); 25.2: Z. 4631 ERGÄNZT durch R53 (T4) |"),
("| 45.6 R6 Ergänzung zu 27 (T4) |",
 "| 45.6 R6 Ergänzung zu 27 (T4); 27.3: Z. 5124 ERGÄNZT durch R31 (47.14); Z. 5163 ERGÄNZT durch R32 (47.15) (T4) |"),
("32 rechnet gegen den Horizontbeginn aus 28.4 (Überschrift 32) |",
 "32 rechnet gegen den Horizontbeginn aus 28.4 (Überschrift 32); 28.6 **PRÄZISIERT durch R53 (49.1)** (Z. 5295, T4) |"),
("„Fassung aus 21b ist ERSETZT“ (Z. 5362) |",
 "„Fassung aus 21b ist ERSETZT“ (Z. 5362); 29.4 BERICHTIGT durch R43 (48.11) (Z. 5377, T4) |"),
("| 34 Faltenregeln, Feld `horizontbeginn` | 2 | 34.1–34.6 | – |",
 "| 34 Faltenregeln, Feld `horizontbeginn` | 2 | 34.1–34.6 | 34.5 BERICHTIGT durch R43 (48.11) (Z. 6228, T4) |"),
("| 35.1 → 38.1 Berichtigung (T3); 35.4 → 42.1 D5 (T3) |",
 "| 35.1 → 38.1 Berichtigung (T3); 35.4 → 42.1 D5 (T3); 35.1 **PRÄZISIERT durch R37 (48.5)** (Z. 6386); 35.4 ERGÄNZT durch R26 (47.9) (Z. 6466) (T4) |"),
("38.4 Fertigkriterium **ERSETZT (39.1)** (MARKE+ Z. 7368) |",
 "38.4 Fertigkriterium **ERSETZT (39.1)** (MARKE+ Z. 7368); 38.2 ERGÄNZT durch R49 (48.17) (Z. 7331, T4) |"),
("40.8 (e) → 46.1 R9 Ergänzung (T4) |",
 "40.8 (e) → 46.1 R9 Ergänzung (T4); 40.6 ERGÄNZT durch R42 (48.10), R44 (48.12), Tatsachennotiz zu 5.4 **PRÄZISIERT durch R47 (48.15)** (Z. 8368–8374, T4) |"),
("C5 BERICHTIGT durch 42.1 (D5) |", "C5 BERICHTIGT durch 42.1 (D5); B6/B7 ERGÄNZT durch R41 (48.9) (Z. 8799, T4) |"),
("42.2 E2 → 45.4 R4 (T4) |", "42.2 E2 → 45.4 R4 (T4); E5 ERGÄNZT durch R29 (47.12) (Z. 9185, T4) |"),
("| 44 Vollzug TB-111/112 | 4 | Tatsachennotizen | – |",
 "| 44 Vollzug TB-111/112 | 4 | Tatsachennotizen | 44-6 ERGÄNZT durch R29 (47.12) (Z. 9959) |"),
("| R5, R7 → 46.7 R16 Ergänzungen |",
 "| R5, R7 → 46.7 R16 Ergänzungen; 45.3 ERGÄNZT durch R42 (48.10); R4 und R5 (a) ERGÄNZT durch R29 (47.12); R5 (b) **BERICHTIGT durch R33 (48.1)**; 45.5 ERGÄNZT durch R34 (48.2), **PRÄZISIERT durch R36 (48.4)** (Z. 10179–10219) |"),
("| 46 aus 27a | 4 | R9–R17 (46.1–46.8); 46.9 Lesart; 46.11 Vollzug | – |",
 """| 46 aus 27a | 4 | R9–R17 (46.1–46.8); 46.9 Lesart; 46.11 Vollzug | 46.3 ERGÄNZT durch R39 (48.7), R42 (48.10); R14 ERGÄNZT durch R25, R26, R27 (Bedingung 5); 46.9 ERGÄNZT durch R25 (47.8, Bestätigung) (Z. 10410–10512) |
| 47 aus 27c | 4 | R18–R32 (47.1–47.15) | – |
| 48 aus 29b | 4 | R33–R52 (48.1–48.20); R51 = Marken für Register 0–12 | 48.16 R48 (g) **BERICHTIGT durch R54 (49.2)** (Z. 10850) |
| 49 aus 30a | 4 | R53–R55 (49.1–49.3) | – |
| 50 Tatsachennotizen E-2 | 4 | 50.1 Voraussetzungen; 50.2 Feldliste (R39); 50.3/50.4 Vollzug TB-122/TB-124; 50.5 Lesart Zählweise (vorläufig); 50.6 Entscheid R24; 50.7 Offenes | – |

## 5. Die Marken aus E-2 (TB-126)

Alle 88 Marken, die TB-126 gesetzt hat (87 am alten Ort, 1 unter 48.16), in der Reihenfolge des Registers. Erzeugt
mit `docs/belege/TB-126/c2_index_e2.py` aus `docs/belege/TB-126/c1_marken.txt` (Zeile, Art, Teil) und Anhang A
des Auftrags TB-126 (alter Ort), nicht abgetippt. In Tabelle 1–4 oben stehen sie zusätzlich an ihrer Stelle.

""" + T5),
# Pflege
("wie die Kopie. Wird ein Teil neu geschnitten, ändern sie sich mit.",
 """wie die Kopie. Wird ein Teil neu geschnitten, ändern sie sich mit.
Zuletzt nachgezogen in TB-126 (01.10.2026): Zeilenangaben mit `docs/belege/TB-126/c2_index_zeilen.py` vom Stand
`0f56aeb` auf `db108a6` umgeschrieben (Abbildung über die unveränderten alten Zeilen); neuer Zuschnitt verschiebt
23 nach T2, 37 nach T3, 43 nach T4; Einträge mit `c2_index_eintraege.py`."""),
]

text = open(I, encoding="utf-8").read()
for alt, neu in E:
    n = text.count(alt)
    assert n == 1, (n, alt[:80])
    text = text.replace(alt, neu)
open(I, "w", encoding="utf-8").write(text)
print("Ersetzungen: %d, je Anker genau 1" % len(E))

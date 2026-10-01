# REGISTER_INDEX — wo was im Register gerade gilt

**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `db108a6` (01.10.2026), Abschnitte 0–50,
11 094 Zeilen, sha256 `b5804659…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2). **Das ist ein Wegweiser, nicht das
Register.** Der Wortlaut steht nur im Register bzw. in der Kopie `REGISTER_KOPIE_teil1–4.md`.

**Wie gemessen:** `python3 docs/werkzeuge/registerkopie.py --marken` sammelt jede Zeile mit „ERSETZT durch“ oder
„PRÄZISIERT durch“ (das Suchmuster des Auftrags, Art `MARKE`, 55 Zeilen), jede weitere Zeile mit ERSETZT,
PRÄZISIERT, BERICHTIGT, ERGÄNZT oder KORRIGIERT (Art `MARKE+`, 98 Zeilen) und jede Überschrift mit Rückverweis
(„Berichtigung zu“, „Präzisierung zu“, „Ergänzung zu“, „ersetzt die …“; Art `UEBERSCHRIFT`, 76 Zeilen). Die
Ausgabe liegt in `docs/belege/TB-126/c1_marken.txt` (zuvor `docs/belege/TB-118/a4_marken.txt`). Die Ketten unten sind **aus diesen Zeilen gelesen, nicht
erinnert**. Wo eine Stelle nur über eine Überschrift oder ein anderes Markenwort erreicht wird, steht sie in der
Spalte „dazu“, nicht als „gilt“. Nach dem Auftrag gilt „ERSETZT durch“ und „PRÄZISIERT durch“ als Kette.
**Mehrdeutig** heisst, dass die Marken keinen einzelnen Ort ergeben. Dann ist der Wortlaut zu lesen.

**Kopie je Abschnitt** (seit 01.10.2026, Betreiberentscheid F1; geschnitten mit `docs/werkzeuge/registerkopie_abschnitte.py`, Bodies aneinandergehängt bytegleich mit dem Register). In der Ablage liegt je Abschnitt eine Datei `REGISTER_KOPIE_ABSCHNITT_<nn>.md`. Wer eine Fundstelle sucht, öffnet die Datei des Abschnitts, nicht das ganze Register.

| Abschnitt | Datei in der Ablage | Zeilen im Register |
|---|---|---|
| 0 | `REGISTER_KOPIE_ABSCHNITT_00.md` | 1–51 |
| 1 | `REGISTER_KOPIE_ABSCHNITT_01.md` | 52–95 |
| 2 | `REGISTER_KOPIE_ABSCHNITT_02.md` | 96–248 |
| 3 | `REGISTER_KOPIE_ABSCHNITT_03.md` | 249–463 |
| 4 | `REGISTER_KOPIE_ABSCHNITT_04.md` | 464–575 |
| 5 | `REGISTER_KOPIE_ABSCHNITT_05.md` | 576–731 |
| 6 | `REGISTER_KOPIE_ABSCHNITT_06.md` | 732–786 |
| 7 | `REGISTER_KOPIE_ABSCHNITT_07.md` | 787–854 |
| 8 | `REGISTER_KOPIE_ABSCHNITT_08.md` | 855–903 |
| 9 | `REGISTER_KOPIE_ABSCHNITT_09.md` | 904–943 |
| 10 | `REGISTER_KOPIE_ABSCHNITT_10.md` | 944–1150 |
| 11 | `REGISTER_KOPIE_ABSCHNITT_11.md` | 1151–1233 |
| 12 | `REGISTER_KOPIE_ABSCHNITT_12.md` | 1234–1310 |
| 13 | `REGISTER_KOPIE_ABSCHNITT_13.md` | 1311–1326 |
| 14 | `REGISTER_KOPIE_ABSCHNITT_14.md` | 1327–1341 |
| 15 | `REGISTER_KOPIE_ABSCHNITT_15.md` | 1342–1792 |
| 16 | `REGISTER_KOPIE_ABSCHNITT_16.md` | 1793–2544 |
| 17 | `REGISTER_KOPIE_ABSCHNITT_17.md` | 2545–2998 |
| 18 | `REGISTER_KOPIE_ABSCHNITT_18.md` | 2999–3063 |
| 19 | `REGISTER_KOPIE_ABSCHNITT_19.md` | 3064–3178 |
| 20 | `REGISTER_KOPIE_ABSCHNITT_20.md` | 3179–3259 |
| 21 | `REGISTER_KOPIE_ABSCHNITT_21.md` | 3260–3611 |
| 22 | `REGISTER_KOPIE_ABSCHNITT_22.md` | 3612–3818 |
| 23 | `REGISTER_KOPIE_ABSCHNITT_23.md` | 3819–4200 |
| 24 | `REGISTER_KOPIE_ABSCHNITT_24.md` | 4201–4545 |
| 25 | `REGISTER_KOPIE_ABSCHNITT_25.md` | 4546–4769 |
| 26 | `REGISTER_KOPIE_ABSCHNITT_26.md` | 4770–5093 |
| 27 | `REGISTER_KOPIE_ABSCHNITT_27.md` | 5094–5167 |
| 28 | `REGISTER_KOPIE_ABSCHNITT_28.md` | 5168–5308 |
| 29 | `REGISTER_KOPIE_ABSCHNITT_29.md` | 5309–5391 |
| 30 | `REGISTER_KOPIE_ABSCHNITT_30.md` | 5392–5525 |
| 31 | `REGISTER_KOPIE_ABSCHNITT_31.md` | 5526–5657 |
| 32 | `REGISTER_KOPIE_ABSCHNITT_32.md` | 5658–5868 |
| 33 | `REGISTER_KOPIE_ABSCHNITT_33.md` | 5869–6080 |
| 34 | `REGISTER_KOPIE_ABSCHNITT_34.md` | 6081–6291 |
| 35 | `REGISTER_KOPIE_ABSCHNITT_35.md` | 6292–6488 |
| 36 | `REGISTER_KOPIE_ABSCHNITT_36.md` | 6489–6839 |
| 37 | `REGISTER_KOPIE_ABSCHNITT_37.md` | 6840–7204 |
| 38 | `REGISTER_KOPIE_ABSCHNITT_38.md` | 7205–7580 |
| 39 | `REGISTER_KOPIE_ABSCHNITT_39.md` | 7581–8101 |
| 40 | `REGISTER_KOPIE_ABSCHNITT_40.md` | 8102–8496 |
| 41 | `REGISTER_KOPIE_ABSCHNITT_41.md` | 8497–8914 |
| 42 | `REGISTER_KOPIE_ABSCHNITT_42.md` | 8915–9480 |
| 43 | `REGISTER_KOPIE_ABSCHNITT_43.md` | 9481–9794 |
| 44 | `REGISTER_KOPIE_ABSCHNITT_44.md` | 9795–10101 |
| 45 | `REGISTER_KOPIE_ABSCHNITT_45.md` | 10102–10325 |
| 46 | `REGISTER_KOPIE_ABSCHNITT_46.md` | 10326–10610 |
| 47 | `REGISTER_KOPIE_ABSCHNITT_47.md` | 10611–10724 |
| 48 | `REGISTER_KOPIE_ABSCHNITT_48.md` | 10725–10890 |
| 49 | `REGISTER_KOPIE_ABSCHNITT_49.md` | 10891–10915 |
| 50 | `REGISTER_KOPIE_ABSCHNITT_50.md` | 10916–11094 |

*Frühere Vierteilung* (bis 01.10.2026; „T1“ … „T4“ in den Tabellen unten bezeichnen sie, massgeblich sind Abschnitt und Z.): T1 = 0–22 (Z. 1–3818), T2 = 23–36 (Z. 3819–6839), T3 = 37–42 (Z. 6840–9480), T4 = 43–50 (Z. 9481–11094).

Schreibweise: „15.6 (a)“ ist Unterabschnitt 15.6, Punkt (a). „T2“ heisst Teil 2. „Z.“ ist die Zeile im Register am
genannten Commit.

---

## 1. Die zwölf Festlegungen (Abschnitt 1, T1)

| Festlegung | Wortlaut | Marken (Zeile) | gilt | dazu |
|---|---|---|---|---|
| 1 Führendes Mass | 1 (Tabelle), T1 | Z. 72 **PRÄZISIERT durch Abschnitt 24** | 1 **und** 24 (24.2, 24.4), T1+T2 | 24.6 Tatsachennotiz (T2) |
| 2 Selektionsstatistik | 1, T1 | Z. 80 ERGÄNZT (Verweis) durch R51 (48.19) | 1, T1 | 48.19 R51: Verweis auf 15.3 (c) und Formelzeile (T4) |
| 3 Beurteilung | 1, T1 | Z. 77 **PRÄZISIERT durch R48 (48.16)** | 1 **mit** 48.16 R48 (j), T1+T4 | – |
| 4 Drawdown-Bedingung | 1, T1 | Z. 74 **PRÄZISIERT durch R48 (48.16)** | 1 **mit** 48.16 R48 (a), T1+T4 (Herleitung Abschnitt 4) | 24.2 nennt sie „unberührt“ |
| 5 `DD_Toleranz` | 1, T1 | – | 1, T1 | – |
| 6 keine absolute Grenze | 1, T1 | – | 1, T1 (Begründung 4.3) | – |
| 7 Schwelle Zweijahres-Falten | 1, T1 | – | 1, T1 (Regel 5.1 Nr. 6) | – |
| 8 Spitzen-Schwelle Plateau | 1, T1 | – | 1, T1 | – |
| 9 Cluster-Schwelle | 1, T1 | – | 1, T1 | – |
| 10 DSR-Basis N = 653 | 1, T1 | – | 1, T1 | – |
| 11 DSR ist Bericht | 1, T1 | – | 1, T1 | 26.7 (Kette im Grenzfall, T2) |
| 12 zulässiges Ergebnis | 1, „Festlegung 12, wörtlich“, T1 | – | 1, T1 | – |

## 2. Die ursprünglichen Abschnitte 2–14 (T1)

| Stelle | Marke (Zeile) | gilt |
|---|---|---|
| Kopf „Stand: 14.09.2026“ | Z. 6 ERGÄNZT durch R49 (48.17) | am Ort; dazu 48.17 R49 (f) (T4) |
| 2.1 Wie sie entstehen | Z. 127 **PRÄZISIERT durch R48 (48.16)** | 2.1 **mit** 48.16 R48 (i) (T4) |
| 2.2 Die vier zulässigen … | Z. 144 **PRÄZISIERT durch R48 (48.16)**; Z. 147 ERGÄNZT durch R49 (48.17) | 2.2 **mit** 48.16 R48 (h); dazu 48.17 R49 (a) (T4) |
| 2.5 Die Kantenregel | Z. 203 **PRÄZISIERT durch R48 (48.16)** | 2.5 **mit** 48.16 R48 (f) (T4) |
| 2.7 Stufung | Z. 244 ERGÄNZT durch R49 (48.17) | am Ort; dazu 48.17 R49 (b) (T4) |
| 3 „Der Faltenplan“ | Z. 411 ERSETZT durch Abschnitt 15, Registertext 2 und 4; Zahlenteil: Z. 459 ERGÄNZT durch R49 (48.17) | 15.4, 15.6 → weiter nach Tabelle 3; Zahlenteil dazu 48.17 R49 (c) (T4) |
| 4.2 | Z. 516 ERGÄNZT (Verweis) durch R51 (48.19) | am Ort; dazu 48.19 R51 (T4) |
| 4.4 | Z. 571 ERGÄNZT durch R49 (48.17) | am Ort; dazu 48.17 R49 (c) (T4) |
| 5.1 „Die Regeln“ | Z. 580 ERSETZT durch Abschnitt 15, Registertext 0, 2 und 4; Nr. 7: Z. 634 **PRÄZISIERT durch R37 (48.5)** | 15.2, 15.4, 15.6 → weiter nach Tabelle 3; Nr. 7 **mit** 48.5 R37 (T4) |
| 5.3 „Krypto: Platzhalter mit Regel“ | Z. 663 ERSETZT durch Abschnitt 15, Registertext 3 und 4; Z. 688 ERGÄNZT (Verweis) durch R51 (48.19) | 15.5, 15.6 → weiter nach Tabelle 3; dazu 48.19 R51 (T4) |
| 7, Tabelle (a) und (d) | Z. 798 (d) **PRÄZISIERT durch R48 (48.16)**; Z. 801 (a) ERGÄNZT (Verweis) durch R51 (48.19); Z. 804 (d) ERGÄNZT durch R55 (49.3) | 7 (d) **mit** 48.16 R48 (c); dazu 49.3 R55 (leere Menge), 48.19 R51 (T4) |
| 7.1 Die drei Regeln … | Z. 847 ERGÄNZT durch R21 (47.4); Z. 850 **PRÄZISIERT durch R23 (47.6)** | 7.1 **mit** 47.6 R23; dazu 47.4 R21 (T4) |
| 8.1 Zufalls-Timing-Test | Z. 899 **PRÄZISIERT durch R48 (48.16)** | 8.1 **mit** 48.16 R48 (g); R48 (g) BERICHTIGT durch 49.2 R54 (Z. 10850) (T4) |
| 9, erster Absatz („N = 653 plus …“) | Z. 911 **PRÄZISIERT durch R48 (48.16)** (einzige Marke in 9) | 9 **mit** 48.16 R48 (b) (T4) |
| 10 Sperrliste | Z. 1004 (MARKE+: der Kasten an Punkt 4 sagt „nicht (iii) (ERSETZT-Marke)“, Form (ii) nach 38.4) | 10, Punkttext unverändert; Vollzug Punkt 4 in 39.2 (T3). Die Sperrlisten-Einträge 36.1, 36.6, 37.2 und 37.3 gehen in Tabelle 4 |
| ↳ 10, künftiger Punkt 15 (die neun neuen Trade-Listen) | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 48.10 R42 (T4) |
| ↳ 10, Sperrlistenpunkt 10 (Zuteilungskaskade, `shared/zuteilung.py`) | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 48.13 R45 (T4) |
| ↳ 10.1, „Stichproben-Hash-Vergleich“ | **Indexzeile E-2**, keine Marke (Abschnitt 10) | lies „Hash-Vergleich aller Ausgabedateien …“: 48.16 R48 (k) (T4) |
| ↳ 10, „Fortschreibung derselben Tatsache (15.09.2026, nach dem Lauf)“ | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 48.17 R49 (g); R51: 48.19 (T4) |
| ↳ 10, Sperrlistenpunkt 14 („Die Reihenfolge Selektion → Bestätigungsperiode → Bericht“) | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 47.13 R30 (T4) |
| 11, 11.2, 11.3 | Z. 1207 (11.2) ERGÄNZT durch R43 (48.11); Z. 1226 (11) ERGÄNZT durch R49 (48.17); Z. 1229 (11.3) ERGÄNZT durch 50.3 und 50.4 | am Ort; dazu 48.11 R43, 48.17 R49 (h), Vollzug Posten 3 in 50.3/50.4 (T4) |
| 12 Vollständigkeitstest | Z. 1297, 1300, 1303, 1306 ERGÄNZT durch R25 (47.8), R26 (47.9), R49 (48.17), R50 (48.18) | 12. **Dazu:** 40.7 Ergänzung (T3), 41.1 A1 Berichtigung „sieben Mutationsproben“ (T3), 46.5 R14 Ergänzung (T4), 47.8 R25, 47.9 R26, 48.17 R49 (d), 48.18 R50 (T4) |
| alle übrigen (0, 6, 13, 14 und die oben nicht genannten Unterabschnitte von 2, 4, 7–9) | – | am Ort, T1 |

## 3. Registertexte 0–7 und die Registertexte ohne Nummer (Abschnitte 15–17, T1)

| Registertext | Ersteintrag | Marken der Kette (Zeile) | **gilt** | dazu (Überschrift oder anderes Markenwort) |
|---|---|---|---|---|
| **0** Verfahren | 15.2 | – | **15.2** (T1) | – |
| **1a** Bootstrap (a) | 15.3 (a) | – | **15.3 (a)** | 24.2 beruft sich auf 1a; Z. 4205 „Registertext 1a bleibt in 15.3“; 15.3 insgesamt: Z. 1446 ERGÄNZT durch R35 (48.3) (T4) |
| **1b** | 15.3 (b) | – | **15.3 (b)** | Z. 1425 ERGÄNZT durch R41 (48.9) (T4) |
| **1c** | 15.3 (c) | – | **15.3 (c)** | – |
| **2a–2c** Faltenzuordnung | 15.4 (a)–(c) | – | **15.4 (a)–(c)** | 2a: Z. 1474 **BERICHTIGT durch R54 (49.2)** („lies“); 15.4 insgesamt: Z. 1519 ERGÄNZT durch R41 (48.9) und 50.1 (T4) |
| **2d** Embargo | 15.4 (d) | Z. 1469 ERSETZT durch 16.6 → Z. 2317 PRÄZISIERT durch R37 (48.5) | **16.6** (T1) **mit** 48.5 R37 (T4) | 41.2 B2 „Berichtigung der 2d-Herleitung“ (T3) |
| **3a** Universum | 15.5 (a) | Tabelle darunter: Z. 1556 KORRIGIERT in 16.1.3 (MARKE+) | **15.5 (a)**, Rechenweg der Krypto-Zeile **16.1.3** | 15.5 insgesamt: Z. 1634 ERGÄNZT durch R53 (49.1) (T4) |
| **3b** Symbolzahl je Falte | 15.5 (b) | Tatsachennotizen: Z. 1579 ERSETZT durch 16.1.1, Z. 1596 ERSETZT durch 16.1.2 | Regel **15.5 (b)**, Tatsachen **16.1.1/16.1.2** | Ergänzungen 3b (a)–(e) in **16.7** (siehe nächste Zeilen) |
| **3b (a)** Ergänzung | 16.7 (a) | – | **16.7 (a)** | – |
| **3b (b)** Ergänzung | 16.7 (b) | – | **16.7 (b)** | 34.3 berichtigt in 30.2 (2) „3b (b)“ zu „3b (a)“ (T2) |
| **3b (c)** Benchmark | 16.7 (c) | Z. 2363 (c) ERSETZT durch 23.3 | **23.3** (T2) | 24.2 bezieht sich auf 3b (c) „in der Fassung aus 23.3“ |
| **3b (d), (e)** | 16.7 (d), (e) | – | **16.7 (d), (e)** | (d): Z. 2381 ERGÄNZT durch R38 (48.6) (T4) |
| **3c** Vorbehalt | 15.5 (c) | – | **15.5 (c)** | Z. 1543 ERGÄNZT durch 26.4 (T2) |
| **3d** | 15.5 (d) | – | **15.5 (d)** | – |
| **4** Falten, insgesamt | 15.6 | – | 15.6 | 21 „Berichtigung zu Registertext 4“ (15.6, Punkt 2 der Tafel, T1); 24.2 „Präzisierung zu Registertext 4“ (Drawdown Mark-to-Market, **ohne Marke in 15.6**, T2); Z. 1714 ERGÄNZT (Verweis) durch R51 (48.19) (T4) |
| **4a** erste Falte | 15.6 (a) | Z. 1646 (a) ERSETZT durch 25.3 → Z. 4649 (i) PRÄZISIERT durch 26.2 | **25.3**, Bedingung (i) in der Fassung **26.2** (T2) | 21.3 (b) ging ebenfalls in 25.3 auf (Z. 3347). 28.6 „Registertext 4a, Präzisierung, Ergänzung“ → 30.6 „Präzisierung zu 28.6“; 32 „Bedingung (i) rechnet gegen den Horizontbeginn aus 28.4“; 33.2 „Der Faltenplan nach 4a“ (alle T2). **Mehrdeutig, ob 28.6 und 30.6 den Wortlaut von 25.3 fortschreiben oder daneben stehen, Abschnitte 25, 26, 28, 30** |
| **4b, 4c** | 15.6 (b), (c) | (c): Z. 1664 **PRÄZISIERT durch R23 (47.6)** | **15.6 (b), (c)**, (c) **mit** 47.6 R23 (T4) | – |
| **4d** Faltenliste | 15.6 (d) | – | Regel **15.6 (d)** | Tatsachennotizen: 21.4 (berichtigte Faltenliste, T1), 26.3 (Platzhalter) **ERSETZT** durch 28.4 (MARKE+ Z. 5217); Faltenplan als Registertext 33.2 (T2) |
| **5** Datenstand | 15.7 | Z. 1737 ERSETZT durch 16.3 | **16.3**, nach Punkten wie folgt | 18 Tatsachennotiz zu 5/5a (T1) |
| **5a** Bestand und Snapshot | 16.3 (a) | Z. 1980 ERSETZT durch 17.1 | **17.1** (T1) | 17.3 Zusatz `rand_erste`; 28.2 Ergänzung `asof` → 31 „Berichtigung zu 28.2“, Ersatztext **31.2**; 31.3 „Präzisierung zu 5a / 17.1“ (T2); 41.2 B5 Resolver-Pflicht, Ergänzung zu 5a/5e (T3) |
| **5b** Registerhash | 16.3 (b) | Z. 1994 PRÄZISIERT durch 17.9 | **16.3 (b) mit 17.9** (T1) | – |
| **5c** Reihenfolge Snapshot/Tag | 16.3 (c) | Z. 2005 ERSETZT durch 17.2 | **17.2** (T1) | – |
| **5d** UTC | 16.3 (d) | – | **16.3 (d)** | – |
| **5e** Lese-Audit | 17.4 | – | **17.4** (T1) | 19 Ergänzung Codeherkunft (T1) → 45.4 R4 „Ergänzung zu 19“ (T4); 41.2 B5 (T3) |
| **5f** Umgebung | 17.5 | – | **17.5** (T1) | 20 Tatsachennotiz Lock (T1) |
| **6** Budgetstufen (a)–(m) | 16.4 | Z. 2076–2171: 18 Marken, davon 14 **PRÄZISIERT** durch R18–R23 (47.1–47.6) und R37 (48.5) — Liste in Abschnitt 5 | **16.4** (T1) **mit** 47.1–47.6 und 48.5 für (a)–(d), (h)–(m) (T4) | 47.3 R20 Ergänzung zu (j), (l); 47.7 R24 Tatsachennotiz zu (g), (h) mit 50.6 (T4); 22.4 „Registertext 6, Ergänzung — Notbremse“ (T1); 26.7 Kette „(b) → Festlegung 11 → Registertext 6 (b)“ (T2) |
| **7** Backtester-Prüfung | 16.5 | – | **16.5** (T1) | Z. 2259 ERGÄNZT durch 17.6, 17.7, 17.8 (Ergänzungen I–III, T1) |
| Kandidatenregeln (a)–(e) | 16.8 | – | **16.8** (T1) | – |
| Vorab-Filter (a)–(c) | 16.9 | – | **16.9** (T1) | – |
| short-fähige Sleeves (a)–(e) | 16.10 | – | **16.10** (T1) | – |

## 4. Registertexte ab Abschnitt 18

Ab Abschnitt 22 heissen Registertexte nach ihrem Unterabschnitt, ab 41 nach ihrem Eintrag (A1 …, R1 …). Für jeden
Registertext ab Abschnitt 38 gilt 38.2: Fundstellen im Code werden als Datei und Bezeichner angegeben.
Die Spalte „später berührt“ nennt jede gemessene Marke und jede Rückverweis-Überschrift, die auf den Abschnitt zeigt.

| Abschnitt | T | Registertexte / Einträge darin | später berührt (Marke oder Überschrift) |
|---|---|---|---|
| 18 Tatsachennotiz 5/5a, Snapshot | 1 | Tatsachennotiz | Z. 3059 ERGÄNZT durch R28 (47.11) (T4) |
| ↳ 17.3, 17.9, 18 — Datenstand-Hash voll | 1 | **Indexzeile E-2**, keine Marke (R51 verlangt Indexzeile) | 48.19 R51 (T4) |
| 19 Codeherkunft (5e) | 1 | Ergänzung zu 5e | 45.4 R4 Ergänzung zu 19 (T4) |
| 20 Lock (5f) | 1 | Tatsachennotiz | – |
| 21 Faltenschranke | 1 | 21.3 Ersatztext (a)–(c); 21.4 Tatsachennotiz zu 4d; 21.9 Entscheidung zu 21.6 | 21.3 (b) **ERSETZT durch 25.3** (Z. 3347); 36.4 Tatsachennotiz zu 21.4; 38.3 Tatsachennotiz zu 21.9; 21.4: Z. 3401 ERGÄNZT durch R53 (49.1) (T4) |
| 22 Methodenantwort 19.09. | 1 | 22.1 allgemeine Prüfregel; 22.2 Kill-Test-Berichtswerte; 22.3 Abschalt- und Zuschaltregeln; 22.4 Ergänzung zu RT 6 | 22.2: Z. 3676 ERGÄNZT durch R34 (48.2) (T4) |
| 23 Benchmark tagesgenau | 2 | 23.3 Ersatztext zu 3b (c) | in 23.3 selbst: Z. 3955 „ERSETZT (TB-71) durch den Satz zur Zeitachse oben“ (eine Tabelle in 23.3 durch einen Satz in 23.3) |
| 24 Mark-to-Market | 2 | 24.2 Präzisierung zu RT 4; 24.3 Entscheidungsregel; 24.4 Festlegung 1 | 24.6 Tatsachennotiz; 24.2 **PRÄZISIERT durch R36 (48.4)** (Z. 4293, T4) |
| 25 erste Falte, Konjunktion | 2 | 25.3 Ersatztext zu 4a und 21.3 (b) | (i) **PRÄZISIERT durch 26.2** (Z. 4649) und **durch R53 (49.1)** (Z. 4651); 25.2: Z. 4631 ERGÄNZT durch R53 (T4) |
| 26 Datenhorizont je Bot | 2 | 26.2 Präzisierung zu 4a (i); 26.4 Ergänzung zu 3 (c); 26.7 Grenzfall | 26.3 (Platzhalter-Tabelle) **ERSETZT** durch 28.4; 26.6 Zeilen 1 und 4 **ERSETZT** durch 28.5, Zeile 2 dort „erledigt“ (MARKE+); 28 „Berichtigung zu 26.3 und 26.6“; 31.6 berichtigt eine Zahl aus 26 |
| 27 Sichtschutz | 2 | 27.1–27.5 | 45.6 R6 Ergänzung zu 27 (T4); 27.3: Z. 5124 ERGÄNZT durch R31 (47.14); Z. 5163 ERGÄNZT durch R32 (47.15) (T4) |
| 28 `asof` gesetzt | 2 | 28.2 Ergänzung zu 5a; 28.4, 28.5 Ersatzmarken; 28.6 Präzisierung und Ergänzung zu 4a | 28.2 → 31 Berichtigung, Ersatztext **31.2**; 28.6 → 30.6 Präzisierung; 32 rechnet gegen den Horizontbeginn aus 28.4 (Überschrift 32); 28.6 **PRÄZISIERT durch R53 (49.1)** (Z. 5295, T4) |
| 29 Kapitalpfad ab erster Falte | 2 | 29.3 Registertext | 29.2 → 30.7 Ergänzung; 29.4 → 34.5 Berichtigung; in 29.4: „Fassung aus 21b ist ERSETZT“ (Z. 5362); 29.4 BERICHTIGT durch R43 (48.11) (Z. 5377, T4) |
| 30 gesperrter Faltenplan | 2 | 30.2 Registertext (1)–(3); 30.3 Tatsachennotiz Punkt 2 | 30.2 (2) → 34.3 Berichtigung; 30.2 (3) → 33.1 Berichtigung, 35.4 Präzisierung, 45.3 R3 Ergänzung (T4). **Mehrdeutig, welche Fassung von 30.2 (3) gilt, Abschnitte 33, 35, 45** |
| 31 kein Feld `asof` | 2 | 31.2 Ersatztext zu 28.2; 31.3 Präzisierung zu 5a/17.1 | – |
| 32 Horizontbeginn | 2 | Tatsachennotizen, 32.5 Entscheidungsvorlage | – |
| 33 Faltenplan als Registertext | 2 | 33.2 Registertext; 33.3 Feldliste; 33.4 Anpassungen | 33.2 → 34.1, 34.2, 35.1 Ergänzungen (35.1 → **38.1 Berichtigung**, T3); 33.3 → 34.4, 35.2 Ergänzungen, 42.1 D5 Präzisierung (→ 42.2 E3 BERICHTIGT), 45.3 R3; 33.4 Punkt 3 **ERSETZT** (35.3; MARKE+ Z. 6054), 34.6 Berichtigung. **33.2 und 33.3 sind mehrdeutig: Grundtext plus Ergänzungen in 34, 35, 38, 42 und 45** |
| 34 Faltenregeln, Feld `horizontbeginn` | 2 | 34.1–34.6 | 34.5 BERICHTIGT durch R43 (48.11) (Z. 6228, T4) |
| 35 Bestätigungsperiode | 2 | 35.1–35.4 | 35.1 → 38.1 Berichtigung (T3); 35.4 → 42.1 D5 (T3); 35.1 **PRÄZISIERT durch R37 (48.5)** (Z. 6386); 35.4 ERGÄNZT durch R26 (47.9) (Z. 6466) (T4) |
| 36 Schreibregel, Sonde, Abbild | 2 | 36.1 Schreibregel; 36.2 Sonde; 36.5 drei Ausgänge; 36.6 Abbild | 36.2 → 36.5 Berichtigung, 37.3 Ergänzung; 36.5 → 37.1 Präzisierung, 46.5 R14 Ergänzung (T4); 36.6 → 37.2, 37.3 Ergänzung |
| 37 Sonde je Bestandteil | 3 | 37.1–37.3; 37.4 Tatsachennotiz zu Abschnitt 10; 37.5 „Ort registrierter Werte“ | in 37.4: Z. 7013 ERSETZT (38.6); Z. 7025 **BERICHTIGT durch 42.3 F2** |
| 38 Weg (A), Fundstellen | 3 | 38.1 Berichtigung zu 35.1; **38.2 Fundstellen**; 38.4 Form (ii); 38.5 Kosten | 38.4 Fertigkriterium **ERSETZT (39.1)** (MARKE+ Z. 7368); 38.2 ERGÄNZT durch R49 (48.17) (Z. 7331, T4) |
| 39 Vollzug Punkt 4 | 3 | 39.1 Berichtigung zu 38.4; 39.2 Vollzug; 39.3–39.9 Tatsachennotizen | – |
| 40 Testannahmen, Handelslisten | 3 | 40.2 `G6`; 40.3 `H3`; 40.6 Handelslisten; 40.7 Ergänzung zu 12; 40.8 Beschlossenes | 40.6 → 41.1 A3 Berichtigung, A12 Präzisierung, 46.3 R12 (T4); 40.7 → 41.1 A2 Berichtigung; 40.8 (e) → 46.1 R9 Ergänzung (T4); 40.6 ERGÄNZT durch R42 (48.10), R44 (48.12), Tatsachennotiz zu 5.4 **PRÄZISIERT durch R47 (48.15)** (Z. 8368–8374, T4) |
| 41 aus 24b/24c/24d | 3 | 41.1 A1–A12; 41.2 B1–B8; 41.3 C-Einträge | A10 → 46.2 R10 Ergänzung (T4); A11 **PRÄZISIERT durch 42.1** (D2, D3; Z. 8673); A12 ERGÄNZT durch 41.2 (B3, B6/B7); B4 **PRÄZISIERT durch 42.1 (D6)** (Z. 8714); B5 BERICHTIGT durch 42.1 (D1), ERGÄNZT durch 41.3 (C6); B8 BERICHTIGT durch 41.3 (C8); C5 BERICHTIGT durch 42.1 (D5); B6/B7 ERGÄNZT durch R41 (48.9) (Z. 8799, T4) |
| 42 aus 25a/25b/25c | 3 | 42.1 D1–D12; 42.2 E-Einträge; 42.3 F-Einträge; 42.4/42.5 Tatsachennotizen | D6 ERGÄNZT durch 42.2 (E1, E2) und 42.3 (F7, F8); D2 ERGÄNZT durch 42.2 (E1), 42.3 (F8); D3/D7 **PRÄZISIERT durch 42.2 (E6)** (Z. 8969); D5 BERICHTIGT durch 42.2 (E3); D8 BERICHTIGT durch 42.2 (E5); 42 (Klasse (iv)) → 45.2 R2; 42.2 E2 → 45.4 R4 (T4); E5 ERGÄNZT durch R29 (47.12) (Z. 9185, T4) |
| 43 aus 25d/25e | 4 | 43.1, 43.2; 43.3 Berichtigung an 25e (3), vorläufig | 43.3 → 45.1 R1 „Marke an 43.3 (Bestätigung)“ (T4) |
| 44 Vollzug TB-111/112 | 4 | Tatsachennotizen | 44-6 ERGÄNZT durch R29 (47.12) (Z. 9959) |
| 45 aus 26a | 4 | R1–R8 (45.1–45.8), R11 (45.11) | R5, R7 → 46.7 R16 Ergänzungen; 45.3 ERGÄNZT durch R42 (48.10); R4 und R5 (a) ERGÄNZT durch R29 (47.12); R5 (b) **BERICHTIGT durch R33 (48.1)**; 45.5 ERGÄNZT durch R34 (48.2), **PRÄZISIERT durch R36 (48.4)** (Z. 10179–10219) |
| 46 aus 27a | 4 | R9–R17 (46.1–46.8); 46.9 Lesart; 46.11 Vollzug | 46.3 ERGÄNZT durch R39 (48.7), R42 (48.10); R14 ERGÄNZT durch R25, R26, R27 (Bedingung 5); 46.9 ERGÄNZT durch R25 (47.8, Bestätigung) (Z. 10410–10512) |
| 47 aus 27c | 4 | R18–R32 (47.1–47.15) | – |
| 48 aus 29b | 4 | R33–R52 (48.1–48.20); R51 = Marken für Register 0–12 | 48.16 R48 (g) **BERICHTIGT durch R54 (49.2)** (Z. 10850) |
| 49 aus 30a | 4 | R53–R55 (49.1–49.3) | – |
| 50 Tatsachennotizen E-2 | 4 | 50.1 Voraussetzungen; 50.2 Feldliste (R39); 50.3/50.4 Vollzug TB-122/TB-124; 50.5 Lesart Zählweise (vorläufig); 50.6 Entscheid R24; 50.7 Offenes | – |

## 5. Die Marken aus E-2 (TB-126)

Alle 88 Marken, die TB-126 gesetzt hat (87 am alten Ort, 1 unter 48.16), in der Reihenfolge des Registers. Erzeugt
mit `docs/belege/TB-126/c2_index_e2.py` aus `docs/belege/TB-126/c1_marken.txt` (Zeile, Art, Teil) und Anhang A
des Auftrags TB-126 (alter Ort), nicht abgetippt. In Tabelle 1–4 oben stehen sie zusätzlich an ihrer Stelle.

| alter Ort (Anhang A) | Marke | Wort | durch | Art | T |
|---|---|---|---|---|---|
| Kopf, Absatz „Stand: 14.09.2026“ | Z. 6 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| 1, Tabelle, Zeile 4 | Z. 74 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 1, Tabelle, Zeile 3 | Z. 77 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 1, Tabelle, Zeile 2 | Z. 80 | ERGÄNZT (Verweis) | R51 (48.19) | MARKE+ | 1 |
| 2.1 | Z. 127 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 2.2 | Z. 144 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 2.2 | Z. 147 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| 2.5 | Z. 203 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 2.7 | Z. 244 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| 3, Zahlenteil (nach ENDE ERZEUGT) | Z. 459 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| 4.2 | Z. 516 | ERGÄNZT (Verweis) | R51 (48.19) | MARKE+ | 1 |
| 4.4 | Z. 571 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| 5.1, Nr. 7 | Z. 634 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 5.3 | Z. 688 | ERGÄNZT (Verweis) | R51 (48.19) | MARKE+ | 1 |
| 7, Tabelle, Zeile (d) | Z. 798 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 7, Tabelle, Zeile (a) | Z. 801 | ERGÄNZT (Verweis) | R51 (48.19) | MARKE+ | 1 |
| 7, Tabelle, Zeile (d) | Z. 804 | ERGÄNZT | R55 (49.3) | MARKE+ | 1 |
| 7.1 | Z. 847 | ERGÄNZT | R21 (47.4) | MARKE+ | 1 |
| 7.1 | Z. 850 | PRÄZISIERT | R23 (47.6) | MARKE | 1 |
| 8.1 | Z. 899 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 9, erster Absatz | Z. 911 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 11.2 | Z. 1207 | ERGÄNZT | R43 (48.11) | MARKE+ | 1 |
| Abschnitt 11 | Z. 1226 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| 11.3 | Z. 1229 | ERGÄNZT | 50.3 und 50.4 | MARKE+ | 1 |
| Abschnitt 12 | Z. 1297 | ERGÄNZT | R25 (47.8) | MARKE+ | 1 |
| Abschnitt 12 | Z. 1300 | ERGÄNZT | R26 (47.9) | MARKE+ | 1 |
| Abschnitt 12 | Z. 1303 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| Abschnitt 12 | Z. 1306 | ERGÄNZT | R50 (48.18) | MARKE+ | 1 |
| 15.3 (b) | Z. 1425 | ERGÄNZT | R41 (48.9) | MARKE+ | 1 |
| 15.3 | Z. 1446 | ERGÄNZT | R35 (48.3) | MARKE+ | 1 |
| 15.4 (a) | Z. 1474 | BERICHTIGT | R54 (49.2) | MARKE+ | 1 |
| 15.4 | Z. 1519 | ERGÄNZT | R41 (48.9) und 50.1 | MARKE+ | 1 |
| 15.5 | Z. 1634 | ERGÄNZT | R53 (49.1) | MARKE+ | 1 |
| 15.6 (c) | Z. 1664 | PRÄZISIERT | R23 (47.6) | MARKE | 1 |
| 15.6 | Z. 1714 | ERGÄNZT (Verweis) | R51 (48.19) | MARKE+ | 1 |
| 16.4 (b) | Z. 2076 | PRÄZISIERT | R21 (47.4) | MARKE | 1 |
| 16.4 (a) | Z. 2079 | PRÄZISIERT | R22 (47.5) | MARKE | 1 |
| 16.4 (b) | Z. 2082 | PRÄZISIERT | R23 (47.6) | MARKE | 1 |
| 16.4 (c) | Z. 2085 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 16.4 (d) | Z. 2088 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 16.4 (m) | Z. 2135 | PRÄZISIERT | R18 (47.1) | MARKE | 1 |
| 16.4 (h) | Z. 2138 | PRÄZISIERT | R18 (47.1) | MARKE | 1 |
| 16.4 (l) | Z. 2141 | PRÄZISIERT | R18 (47.1) | MARKE | 1 |
| 16.4 (h) | Z. 2144 | PRÄZISIERT | R19 (47.2) | MARKE | 1 |
| 16.4 (j) | Z. 2147 | PRÄZISIERT | R19 (47.2) | MARKE | 1 |
| 16.4 (k) | Z. 2150 | PRÄZISIERT | R19 (47.2) | MARKE | 1 |
| 16.4 (l) | Z. 2153 | ERGÄNZT | R20 (47.3) | MARKE+ | 1 |
| 16.4 (j) | Z. 2156 | ERGÄNZT | R20 (47.3) | MARKE+ | 1 |
| 16.4 (i) | Z. 2159 | PRÄZISIERT | R21 (47.4) | MARKE | 1 |
| 16.4 (j) | Z. 2162 | PRÄZISIERT | R21 (47.4) | MARKE | 1 |
| 16.4 (i) | Z. 2165 | PRÄZISIERT | R22 (47.5) | MARKE | 1 |
| 16.4 (h) | Z. 2168 | ERGÄNZT | R24 (47.7) und 50.6 | MARKE+ | 1 |
| 16.4 (g) | Z. 2171 | ERGÄNZT | R24 (47.7) und 50.6 | MARKE+ | 1 |
| 16.6 | Z. 2317 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 16.7 (d) | Z. 2381 | ERGÄNZT | R38 (48.6) | MARKE+ | 1 |
| Abschnitt 18 | Z. 3059 | ERGÄNZT | R28 (47.11) | MARKE+ | 1 |
| 21.4 | Z. 3401 | ERGÄNZT | R53 (49.1) | MARKE+ | 1 |
| 22.2 | Z. 3676 | ERGÄNZT | R34 (48.2) | MARKE+ | 1 |
| 24.2 | Z. 4293 | PRÄZISIERT | R36 (48.4) | MARKE | 2 |
| 25.2 | Z. 4631 | ERGÄNZT | R53 (49.1) | MARKE+ | 2 |
| 25.3, Ersatztext (Bedingung (i) steht in dessen erster Zeile) | Z. 4651 | PRÄZISIERT | R53 (49.1) | MARKE | 2 |
| 27.3 (im Zitatblock 27.1 bis 27.5) | Z. 5124 | ERGÄNZT | R31 (47.14) | MARKE+ | 2 |
| Abschnitt 27 | Z. 5163 | ERGÄNZT | R32 (47.15) | MARKE+ | 2 |
| 28.6 | Z. 5295 | PRÄZISIERT | R53 (49.1) | MARKE | 2 |
| 29.4 | Z. 5377 | BERICHTIGT | R43 (48.11) | MARKE+ | 2 |
| 34.5 | Z. 6228 | BERICHTIGT | R43 (48.11) | MARKE+ | 2 |
| 35.1 | Z. 6386 | PRÄZISIERT | R37 (48.5) | MARKE | 2 |
| 35.4 | Z. 6466 | ERGÄNZT | R26 (47.9) | MARKE+ | 2 |
| 38.2 | Z. 7331 | ERGÄNZT | R49 (48.17) | MARKE+ | 3 |
| 40.6 | Z. 8368 | ERGÄNZT | R42 (48.10) | MARKE+ | 3 |
| 40.6 | Z. 8371 | ERGÄNZT | R44 (48.12) | MARKE+ | 3 |
| 40.6 | Z. 8374 | PRÄZISIERT | R47 (48.15) | MARKE | 3 |
| 41.2, Eintrag B6/B7 | Z. 8799 | ERGÄNZT | R41 (48.9) | MARKE+ | 3 |
| 42.2, Eintrag E5 (e) | Z. 9185 | ERGÄNZT | R29 (47.12) | MARKE+ | 3 |
| 44.1, Eintrag 44-6 | Z. 9959 | ERGÄNZT | R29 (47.12) | MARKE+ | 4 |
| 45.3 | Z. 10179 | ERGÄNZT | R42 (48.10) | MARKE+ | 4 |
| 45.4, Block R4 | Z. 10187 | ERGÄNZT | R29 (47.12) | MARKE+ | 4 |
| 45.5, Block R5, Punkt (a) | Z. 10204 | ERGÄNZT | R29 (47.12) | MARKE+ | 4 |
| 45.5, Block R5, Punkt (b) | Z. 10207 | BERICHTIGT | R33 (48.1) | MARKE+ | 4 |
| 45.5 | Z. 10216 | ERGÄNZT | R34 (48.2) | MARKE+ | 4 |
| 45.5 | Z. 10219 | PRÄZISIERT | R36 (48.4) | MARKE | 4 |
| 46.3 | Z. 10410 | ERGÄNZT | R39 (48.7) | MARKE+ | 4 |
| 46.3 | Z. 10413 | ERGÄNZT | R42 (48.10) | MARKE+ | 4 |
| 46.5, Block R14 | Z. 10441 | ERGÄNZT | R25 (47.8) | MARKE+ | 4 |
| 46.5, Block R14 | Z. 10444 | ERGÄNZT | R26 (47.9) | MARKE+ | 4 |
| 46.5, Block R14 (Bedingung 5 steht in dessen erster Zeile) | Z. 10447 | ERGÄNZT | R27 (47.10) | MARKE+ | 4 |
| 46.9 | Z. 10512 | ERGÄNZT | R25 (47.8) | MARKE+ | 4 |
| 48.16 (R48), neu in TB-126 | Z. 10850 | BERICHTIGT | R54 (49.2) | MARKE+ | 4 |

---

**Pflege:** Nach jedem Registerauftrag zusammen mit `registerkopie.py` erneuern. Die Marken misst das Skript neu,
die Ketten liest die Sitzung aus seiner Ausgabe. Die Teil-Nummern in der Spalte T stammen aus demselben Zuschnitt
wie die Kopie. Wird ein Teil neu geschnitten, ändern sie sich mit.
Zuletzt nachgezogen in TB-126 (01.10.2026): Zeilenangaben mit `docs/belege/TB-126/c2_index_zeilen.py` vom Stand
`0f56aeb` auf `db108a6` umgeschrieben (Abbildung über die unveränderten alten Zeilen); neuer Zuschnitt verschiebt
23 nach T2, 37 nach T3, 43 nach T4; Einträge mit `c2_index_eintraege.py`.

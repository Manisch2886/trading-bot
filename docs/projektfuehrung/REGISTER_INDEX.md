# REGISTER_INDEX — wo was im Register gerade gilt

**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `fd8f277` (17.10.2026), Abschnitte 0–71,
12 023 Zeilen, sha256 `459be94e…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2), TB-129 (Fable 01a), TB-130 (Fable 02a), TB-132 (Fable 02c), TB-136 (Fable 04a), TB-139 (Fable 07a), TB-149 (Fable 09a) und TB-154 (Fable 10a). **Das ist ein Wegweiser, nicht das
Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_57.md` (Tabelle unten; dazu die Teile `REGISTER_KOPIE_teil1–5.md`).

**Wie gemessen:** `python3 docs/werkzeuge/registerkopie.py --marken` sammelt jede Zeile mit „ERSETZT durch“ oder
„PRÄZISIERT durch“ (das Suchmuster des Auftrags, Art `MARKE`, 117 Zeilen), jede weitere Zeile mit ERSETZT,
PRÄZISIERT, BERICHTIGT, ERGÄNZT oder KORRIGIERT (Art `MARKE+`, 179 Zeilen) und jede Überschrift mit Rückverweis
(„Berichtigung zu“, „Präzisierung zu“, „Ergänzung zu“, „ersetzt die …“; Art `UEBERSCHRIFT`, 105 Zeilen). Die
Ausgabe liegt in `docs/belege/TB-154/c1_marken.txt` (zuvor `docs/belege/TB-149/c1_marken.txt`, `docs/belege/TB-139/c1_marken.txt`, `docs/belege/TB-136/c1_marken.txt`, `docs/belege/TB-132/c1_marken.txt`, `docs/belege/TB-130/c1_marken.txt`, `docs/belege/TB-129/c1_marken.txt`, `docs/belege/TB-126/c1_marken.txt`, `docs/belege/TB-118/a4_marken.txt`). Die Ketten unten sind **aus diesen Zeilen gelesen, nicht
erinnert**. Wo eine Stelle nur über eine Überschrift oder ein anderes Markenwort erreicht wird, steht sie in der
Spalte „dazu“, nicht als „gilt“. Nach dem Auftrag gilt „ERSETZT durch“ und „PRÄZISIERT durch“ als Kette.
**Mehrdeutig** heisst, dass die Marken keinen einzelnen Ort ergeben. Dann ist der Wortlaut zu lesen.

**Kopie je Abschnitt** (seit 01.10.2026, Betreiberentscheid F1; geschnitten seit TB-127 mit `docs/werkzeuge/registerkopie.py --abschnitte`, zuvor mit `registerkopie_abschnitte.py`; Bodies aneinandergehängt bytegleich mit dem Register). In der Ablage liegt je Abschnitt eine Datei `REGISTER_KOPIE_ABSCHNITT_<nn>.md`. Wer eine Fundstelle sucht, öffnet die Datei des Abschnitts, nicht das ganze Register.

| Abschnitt | Datei in der Ablage | Zeilen im Register |
|---|---|---|
| 0 | `REGISTER_KOPIE_ABSCHNITT_00.md` | 1–51 |
| 1 | `REGISTER_KOPIE_ABSCHNITT_01.md` | 52–98 |
| 2 | `REGISTER_KOPIE_ABSCHNITT_02.md` | 99–251 |
| 3 | `REGISTER_KOPIE_ABSCHNITT_03.md` | 252–466 |
| 4 | `REGISTER_KOPIE_ABSCHNITT_04.md` | 467–587 |
| 5 | `REGISTER_KOPIE_ABSCHNITT_05.md` | 588–749 |
| 6 | `REGISTER_KOPIE_ABSCHNITT_06.md` | 750–804 |
| 7 | `REGISTER_KOPIE_ABSCHNITT_07.md` | 805–875 |
| 8 | `REGISTER_KOPIE_ABSCHNITT_08.md` | 876–930 |
| 9 | `REGISTER_KOPIE_ABSCHNITT_09.md` | 931–970 |
| 10 | `REGISTER_KOPIE_ABSCHNITT_10.md` | 971–1177 |
| 11 | `REGISTER_KOPIE_ABSCHNITT_11.md` | 1178–1260 |
| 12 | `REGISTER_KOPIE_ABSCHNITT_12.md` | 1261–1337 |
| 13 | `REGISTER_KOPIE_ABSCHNITT_13.md` | 1338–1353 |
| 14 | `REGISTER_KOPIE_ABSCHNITT_14.md` | 1354–1368 |
| 15 | `REGISTER_KOPIE_ABSCHNITT_15.md` | 1369–1828 |
| 16 | `REGISTER_KOPIE_ABSCHNITT_16.md` | 1829–2586 |
| 17 | `REGISTER_KOPIE_ABSCHNITT_17.md` | 2587–3043 |
| 18 | `REGISTER_KOPIE_ABSCHNITT_18.md` | 3044–3108 |
| 19 | `REGISTER_KOPIE_ABSCHNITT_19.md` | 3109–3223 |
| 20 | `REGISTER_KOPIE_ABSCHNITT_20.md` | 3224–3304 |
| 21 | `REGISTER_KOPIE_ABSCHNITT_21.md` | 3305–3656 |
| 22 | `REGISTER_KOPIE_ABSCHNITT_22.md` | 3657–3863 |
| 23 | `REGISTER_KOPIE_ABSCHNITT_23.md` | 3864–4257 |
| 24 | `REGISTER_KOPIE_ABSCHNITT_24.md` | 4258–4602 |
| 25 | `REGISTER_KOPIE_ABSCHNITT_25.md` | 4603–4832 |
| 26 | `REGISTER_KOPIE_ABSCHNITT_26.md` | 4833–5156 |
| 27 | `REGISTER_KOPIE_ABSCHNITT_27.md` | 5157–5239 |
| 28 | `REGISTER_KOPIE_ABSCHNITT_28.md` | 5240–5380 |
| 29 | `REGISTER_KOPIE_ABSCHNITT_29.md` | 5381–5463 |
| 30 | `REGISTER_KOPIE_ABSCHNITT_30.md` | 5464–5597 |
| 31 | `REGISTER_KOPIE_ABSCHNITT_31.md` | 5598–5729 |
| 32 | `REGISTER_KOPIE_ABSCHNITT_32.md` | 5730–5940 |
| 33 | `REGISTER_KOPIE_ABSCHNITT_33.md` | 5941–6152 |
| 34 | `REGISTER_KOPIE_ABSCHNITT_34.md` | 6153–6363 |
| 35 | `REGISTER_KOPIE_ABSCHNITT_35.md` | 6364–6560 |
| 36 | `REGISTER_KOPIE_ABSCHNITT_36.md` | 6561–6911 |
| 37 | `REGISTER_KOPIE_ABSCHNITT_37.md` | 6912–7276 |
| 38 | `REGISTER_KOPIE_ABSCHNITT_38.md` | 7277–7652 |
| 39 | `REGISTER_KOPIE_ABSCHNITT_39.md` | 7653–8173 |
| 40 | `REGISTER_KOPIE_ABSCHNITT_40.md` | 8174–8571 |
| 41 | `REGISTER_KOPIE_ABSCHNITT_41.md` | 8572–8992 |
| 42 | `REGISTER_KOPIE_ABSCHNITT_42.md` | 8993–9561 |
| 43 | `REGISTER_KOPIE_ABSCHNITT_43.md` | 9562–9878 |
| 44 | `REGISTER_KOPIE_ABSCHNITT_44.md` | 9879–10185 |
| 45 | `REGISTER_KOPIE_ABSCHNITT_45.md` | 10186–10409 |
| 46 | `REGISTER_KOPIE_ABSCHNITT_46.md` | 10410–10697 |
| 47 | `REGISTER_KOPIE_ABSCHNITT_47.md` | 10698–10817 |
| 48 | `REGISTER_KOPIE_ABSCHNITT_48.md` | 10818–11082 |
| 49 | `REGISTER_KOPIE_ABSCHNITT_49.md` | 11083–11113 |
| 50 | `REGISTER_KOPIE_ABSCHNITT_50.md` | 11114–11302 |
| 51 | `REGISTER_KOPIE_ABSCHNITT_51.md` | 11303–11412 |
| 52 | `REGISTER_KOPIE_ABSCHNITT_52.md` | 11413–11494 |
| 53 | `REGISTER_KOPIE_ABSCHNITT_53.md` | 11495–11637 |
| 54 | `REGISTER_KOPIE_ABSCHNITT_54.md` | 11638–11720 |
| 55 | `REGISTER_KOPIE_ABSCHNITT_55.md` | 11721–11839 |
| 56 | `REGISTER_KOPIE_ABSCHNITT_56.md` | 11840–11954 |
| 57 | `REGISTER_KOPIE_ABSCHNITT_57.md` | 11955–12023 |

*Frühere Vierteilung* (bis 01.10.2026; „T1“ … „T4“ in den Tabellen unten bezeichnen sie, massgeblich sind Abschnitt und Z.): T1 = 0–22 (Z. 1–3863), T2 = 23–36 (Z. 3864–6911), T3 = 37–42 (Z. 6912–9561), T4 = 43–53 (Z. 9562–11637), T5 = 54–57 (Z. 11638–12023).

Schreibweise: „15.6 (a)“ ist Unterabschnitt 15.6, Punkt (a). „T2“ heisst Teil 2. „Z.“ ist die Zeile im Register am
genannten Commit.

---

## 1. Die zwölf Festlegungen (Abschnitt 1, T1)

| Festlegung | Wortlaut | Marken (Zeile) | gilt | dazu |
|---|---|---|---|---|
| 1 Führendes Mass | 1 (Tabelle), T1 | Z. 72 **PRÄZISIERT durch Abschnitt 24** | 1 **und** 24 (24.2, 24.4), T1+T2 | 24.6 Tatsachennotiz (T2) |
| 2 Selektionsstatistik | 1, T1 | Z. 80 ERGÄNZT (Verweis) durch R51 (48.19) | 1, T1 | 48.19 R51: Verweis auf 15.3 (c) und Formelzeile (T4) |
| 3 Beurteilung | 1, T1 | Z. 77 **PRÄZISIERT durch R48 (48.16)**; Z. 83 **PRÄZISIERT durch R36 (48.4)** | 1 **mit** 48.16 R48 (j) **und** 48.4 R36, T1+T4 | – |
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
| 2.1 Wie sie entstehen | Z. 130 **PRÄZISIERT durch R48 (48.16)** | 2.1 **mit** 48.16 R48 (i) (T4) |
| 2.2 Die vier zulässigen … | Z. 147 **PRÄZISIERT durch R48 (48.16)**; Z. 150 ERGÄNZT durch R49 (48.17) | 2.2 **mit** 48.16 R48 (h); dazu 48.17 R49 (a) (T4) |
| 2.5 Die Kantenregel | Z. 206 **PRÄZISIERT durch R48 (48.16)** | 2.5 **mit** 48.16 R48 (f) (T4) |
| 2.7 Stufung | Z. 247 ERGÄNZT durch R49 (48.17) | am Ort; dazu 48.17 R49 (b) (T4) |
| 3 „Der Faltenplan“ | Z. 414 ERSETZT durch Abschnitt 15, Registertext 2 und 4; Zahlenteil: Z. 462 ERGÄNZT durch R49 (48.17) | 15.4, 15.6 → weiter nach Tabelle 3; Zahlenteil dazu 48.17 R49 (c) (T4) |
| 4.2 | Z. 519 ERGÄNZT (Verweis) durch R51 (48.19); Z. 522 **PRÄZISIERT durch R48 (48.16)**; Z. 525 **PRÄZISIERT durch R60 (51.5)**; Z. 528 **PRÄZISIERT durch R64 (52.2)** | 4.2 **mit** 48.16 R48 (d), (e), 51.5 R60 **und** 52.2 R64 (a); dazu 48.19 R51 (T4) |
| 4.4 | Z. 583 ERGÄNZT durch R49 (48.17) | am Ort; dazu 48.17 R49 (c) (T4) |
| 5.1 „Die Regeln“ | Z. 592 ERSETZT durch Abschnitt 15, Registertext 0, 2 und 4; Nr. 7: Z. 649 **PRÄZISIERT durch R37 (48.5)** | 15.2, 15.4, 15.6 → weiter nach Tabelle 3; Nr. 7 **mit** 48.5 R37 (T4) |
| 5.2 „Der Go-Live-Schnitt“ | Z. 676 **PRÄZISIERT durch R81 (55.4)**; Z. 679 ERGÄNZT durch R83 (55.6) | 5.2 **mit** 55.4 R81 (a), (b) und (f); dazu 55.6 R83 (d) (T5) |
| 5.3 „Krypto: Platzhalter mit Regel“ | Z. 684 ERSETZT durch Abschnitt 15, Registertext 3 und 4; Z. 709 ERGÄNZT (Verweis) durch R51 (48.19) | 15.5, 15.6 → weiter nach Tabelle 3; dazu 48.19 R51 (T4) |
| 7, Tabelle (a), (b) und (d) | Z. 819 (d) **PRÄZISIERT durch R48 (48.16)**; Z. 822 (a) ERGÄNZT (Verweis) durch R51 (48.19); Z. 825 (d) ERGÄNZT durch R55 (49.3); Z. 828 (b) **PRÄZISIERT durch R37 (48.5)** | 7 (d) **mit** 48.16 R48 (c); 7 (b) **mit** 48.5 R37; dazu 49.3 R55 (leere Menge), 48.19 R51 (T4) |
| 7.1 Die drei Regeln … | Z. 871 ERGÄNZT durch R21 (47.4); Z. 874 **PRÄZISIERT durch R23 (47.6)** | 7.1 **mit** 47.6 R23; dazu 47.4 R21 (T4) |
| 8, Tabelle (Bericht je Bot) | Z. 899 **PRÄZISIERT durch R36 (48.4)**; Z. 902 ERGÄNZT durch R55 (49.3) | 8, Tabelle **mit** 48.4 R36; dazu 49.3 R55 (T4) |
| 8.1 Zufalls-Timing-Test | Z. 929 **PRÄZISIERT durch R48 (48.16)** | 8.1 **mit** 48.16 R48 (g); R48 (g) BERICHTIGT durch 49.2 R54 (Z. 11090) (T4) |
| 9, erster Absatz („N = 653 plus …“) | Z. 941 **PRÄZISIERT durch R48 (48.16)** (einzige Marke in 9) | 9 **mit** 48.16 R48 (b) (T4) |
| 10 Sperrliste | Z. 1034 (MARKE+: der Kasten an Punkt 4 sagt „nicht (iii) (ERSETZT-Marke)“, Form (ii) nach 38.4) | 10, Punkttext unverändert; Vollzug Punkt 4 in 39.2 (T3). Die Sperrlisten-Einträge 36.1, 36.6, 37.2 und 37.3 gehen in Tabelle 4 |
| ↳ 10, künftiger Punkt 15 (die neun neuen Trade-Listen) | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 48.10 R42 (T4) |
| ↳ 10, Sperrlistenpunkt 10 (Zuteilungskaskade, `shared/zuteilung.py`) | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 48.13 R45 (T4) |
| ↳ 10.1, „Stichproben-Hash-Vergleich“ | **Indexzeile E-2**, keine Marke (Abschnitt 10) | lies „Hash-Vergleich aller Ausgabedateien …“: 48.16 R48 (k) (T4) |
| ↳ 10, „Fortschreibung derselben Tatsache (15.09.2026, nach dem Lauf)“ | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 48.17 R49 (g); R51: 48.19 (T4) |
| ↳ 10, Sperrlistenpunkt 14 („Die Reihenfolge Selektion → Bestätigungsperiode → Bericht“) | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 47.13 R30 (T4) |
| 11, 11.2, 11.3 | Z. 1240 (11.2) ERGÄNZT durch R43 (48.11); Z. 1259 (11) ERGÄNZT durch R49 (48.17); Z. 1262 (11.3) ERGÄNZT durch 50.3 und 50.4 | am Ort; dazu 48.11 R43, 48.17 R49 (h), Vollzug Posten 3 in 50.3/50.4 (T4) |
| 12 Vollständigkeitstest | Z. 1330, 1333, 1336, 1339 ERGÄNZT durch R25 (47.8), R26 (47.9), R49 (48.17), R50 (48.18) | 12. **Dazu:** 40.7 Ergänzung (T3), 41.1 A1 Berichtigung „sieben Mutationsproben“ (T3), 46.5 R14 Ergänzung (T4), 47.8 R25, 47.9 R26, 48.17 R49 (d), 48.18 R50 (T4) |
| alle übrigen (0, 6, 13, 14 und die oben nicht genannten Unterabschnitte von 2, 4, 7–9) | – | am Ort, T1 |

## 3. Registertexte 0–7 und die Registertexte ohne Nummer (Abschnitte 15–17, T1)

| Registertext | Ersteintrag | Marken der Kette (Zeile) | **gilt** | dazu (Überschrift oder anderes Markenwort) |
|---|---|---|---|---|
| **0** Verfahren | 15.2 | – | **15.2** (T1) | – |
| **1a** Bootstrap (a) | 15.3 (a) | Z. 1461 **PRÄZISIERT durch R66 (53.1)** | **15.3 (a)** **mit** 53.1 R66 (a), (b) (T4) | 24.2 beruft sich auf 1a; Z. 4283 „Registertext 1a bleibt in 15.3“; 15.3 insgesamt: Z. 1485 ERGÄNZT durch R35 (48.3) (T4) |
| **1b** | 15.3 (b) | – | **15.3 (b)** | Z. 1458 ERGÄNZT durch R41 (48.9) (T4) |
| **1c** | 15.3 (c) | Z. 1464 **PRÄZISIERT durch R66 (53.1)** | **15.3 (c)** **mit** 53.1 R66 (c) (T4) | – |
| **2a–2c** Faltenzuordnung | 15.4 (a)–(c) | – | **15.4 (a)–(c)** | 2a: Z. 1513 **BERICHTIGT durch R54 (49.2)** („lies“); 15.4 insgesamt: Z. 1558 ERGÄNZT durch R41 (48.9) und 50.1 (T4) |
| **2d** Embargo | 15.4 (d) | Z. 1508 ERSETZT durch 16.6 → Z. 2368 PRÄZISIERT durch R37 (48.5) → Z. 2371 **PRÄZISIERT durch R75 (54.2)** | **16.6** (T1) **mit** 48.5 R37 (T4) und 54.2 R75 (a) (T5) | 41.2 B2 „Berichtigung der 2d-Herleitung“ (T3) |
| **3a** Universum | 15.5 (a) | Tabelle darunter: Z. 1595 KORRIGIERT in 16.1.3 (MARKE+) | **15.5 (a)**, Rechenweg der Krypto-Zeile **16.1.3** | 15.5 insgesamt: Z. 1673 ERGÄNZT durch R53 (49.1) (T4); 15.5, Absatz zu Lesart A: Z. 1676 ERGÄNZT durch R87 (56.4) (T5), nachgetragen nach R93 (a) |
| **3b** Symbolzahl je Falte | 15.5 (b) | Tatsachennotizen: Z. 1618 ERSETZT durch 16.1.1, Z. 1635 ERSETZT durch 16.1.2 | Regel **15.5 (b)**, Tatsachen **16.1.1/16.1.2** | Ergänzungen 3b (a)–(e) in **16.7** (siehe nächste Zeilen) |
| **3b (a)** Ergänzung | 16.7 (a) | – | **16.7 (a)** | – |
| **3b (b)** Ergänzung | 16.7 (b) | – | **16.7 (b)** | 34.3 berichtigt in 30.2 (2) „3b (b)“ zu „3b (a)“ (T2) |
| **3b (c)** Benchmark | 16.7 (c) | Z. 2420 (c) ERSETZT durch 23.3 | **23.3** (T2) | 24.2 bezieht sich auf 3b (c) „in der Fassung aus 23.3“ |
| **3b (d), (e)** | 16.7 (d), (e) | – | **16.7 (d), (e)** | (d): Z. 2438 ERGÄNZT durch R38 (48.6) (T4) |
| **3c** Vorbehalt | 15.5 (c) | – | **15.5 (c)** | Z. 1582 ERGÄNZT durch 26.4 (T2) |
| **3d** | 15.5 (d) | – | **15.5 (d)** | – |
| **4** Falten, insgesamt | 15.6 | – | 15.6 | 21 „Berichtigung zu Registertext 4“ (15.6, Punkt 2 der Tafel, T1); 24.2 „Präzisierung zu Registertext 4“ (Drawdown Mark-to-Market, **ohne Marke in 15.6**, T2); Z. 1756 ERGÄNZT (Verweis) durch R51 (48.19) (T4) |
| **4a** erste Falte | 15.6 (a) | Z. 1688 (a) ERSETZT durch 25.3 → Z. 4730 (i) PRÄZISIERT durch 26.2 | **25.3**, Bedingung (i) in der Fassung **26.2** (T2) | 21.3 (b) ging ebenfalls in 25.3 auf (Z. 3413). 28.6 „Registertext 4a, Präzisierung, Ergänzung“ → 30.6 „Präzisierung zu 28.6“; 32 „Bedingung (i) rechnet gegen den Horizontbeginn aus 28.4“; 33.2 „Der Faltenplan nach 4a“ (alle T2). **Mehrdeutig, ob 28.6 und 30.6 den Wortlaut von 25.3 fortschreiben oder daneben stehen, Abschnitte 25, 26, 28, 30** |
| **4b, 4c** | 15.6 (b), (c) | (c): Z. 1706 **PRÄZISIERT durch R23 (47.6)** | **15.6 (b), (c)**, (c) **mit** 47.6 R23 (T4) | – |
| **4d** Faltenliste | 15.6 (d) | – | Regel **15.6 (d)** | Tatsachennotizen: 21.4 (berichtigte Faltenliste, T1), 26.3 (Platzhalter) **ERSETZT** durch 28.4 (MARKE+ Z. 5316); Faltenplan als Registertext 33.2 (T2) |
| **5** Datenstand | 15.7 | Z. 1779 ERSETZT durch 16.3 | **16.3**, nach Punkten wie folgt | 18 Tatsachennotiz zu 5/5a (T1) |
| **5a** Bestand und Snapshot | 16.3 (a) | Z. 2022 ERSETZT durch 17.1 | **17.1** (T1) | 17.3 Zusatz `rand_erste`; 28.2 Ergänzung `asof` → 31 „Berichtigung zu 28.2“, Ersatztext **31.2**; 31.3 „Präzisierung zu 5a / 17.1“ (T2); 41.2 B5 Resolver-Pflicht, Ergänzung zu 5a/5e (T3) |
| **5b** Registerhash | 16.3 (b) | Z. 2036 PRÄZISIERT durch 17.9 | **16.3 (b) mit 17.9** (T1) | – |
| **5c** Reihenfolge Snapshot/Tag | 16.3 (c) | Z. 2047 ERSETZT durch 17.2 | **17.2** (T1) | – |
| **5d** UTC | 16.3 (d) | – | **16.3 (d)** | – |
| **5e** Lese-Audit | 17.4 | – | **17.4** (T1) | 19 Ergänzung Codeherkunft (T1) → 45.4 R4 „Ergänzung zu 19“ (T4); 41.2 B5 (T3) |
| **5f** Umgebung | 17.5 | – | **17.5** (T1) | 20 Tatsachennotiz Lock (T1); Z. 2875 ERGÄNZT durch R74 (54.1): Name des Handelskalenders (T5) |
| **6** Budgetstufen (a)–(m) | 16.4 | Z. 2118–2213: 18 Marken, davon 14 **PRÄZISIERT** durch R18–R23 (47.1–47.6) und R37 (48.5) — Liste in Abschnitt 5; „Prüfung vor dem Tag“: Z. 2256 **PRÄZISIERT durch R21 (47.4)** — Abschnitt 6 | **16.4** (T1) **mit** 47.1–47.6 und 48.5 für (a)–(d), (h)–(m); „Prüfung vor dem Tag“ **mit** 47.4 R21 (T4) | 47.3 R20 Ergänzung zu (j), (l); 47.7 R24 Tatsachennotiz zu (g), (h) mit 50.6 (T4); 22.4 „Registertext 6, Ergänzung — Notbremse“ (T1); 26.7 Kette „(b) → Festlegung 11 → Registertext 6 (b)“ (T2) |
| **7** Backtester-Prüfung | 16.5 | – | **16.5** (T1) | Z. 2310 ERGÄNZT durch 17.6, 17.7, 17.8 (Ergänzungen I–III, T1) |
| Kandidatenregeln (a)–(e) | 16.8 | – | **16.8** (T1) | – |
| Vorab-Filter (a)–(c) | 16.9 | – | **16.9** (T1) | – |
| short-fähige Sleeves (a)–(e) | 16.10 | – | **16.10** (T1) | – |

## 4. Registertexte ab Abschnitt 18

Ab Abschnitt 22 heissen Registertexte nach ihrem Unterabschnitt, ab 41 nach ihrem Eintrag (A1 …, R1 …). Für jeden
Registertext ab Abschnitt 38 gilt 38.2: Fundstellen im Code werden als Datei und Bezeichner angegeben.
Die Spalte „später berührt“ nennt jede gemessene Marke und jede Rückverweis-Überschrift, die auf den Abschnitt zeigt.

| Abschnitt | T | Registertexte / Einträge darin | später berührt (Marke oder Überschrift) |
|---|---|---|---|
| 18 Tatsachennotiz 5/5a, Snapshot | 1 | Tatsachennotiz | Z. 3125 ERGÄNZT durch R28 (47.11) (T4) |
| ↳ 17.3, 17.9, 18 — Datenstand-Hash voll | 1 | **Indexzeile E-2**, keine Marke (R51 verlangt Indexzeile) | 48.19 R51 (T4) |
| 19 Codeherkunft (5e) | 1 | Ergänzung zu 5e | 45.4 R4 Ergänzung zu 19 (T4) |
| 20 Lock (5f) | 1 | Tatsachennotiz | – |
| 21 Faltenschranke | 1 | 21.3 Ersatztext (a)–(c); 21.4 Tatsachennotiz zu 4d; 21.9 Entscheidung zu 21.6 | 21.3 (b) **ERSETZT durch 25.3** (Z. 3413); 36.4 Tatsachennotiz zu 21.4; 38.3 Tatsachennotiz zu 21.9; 21.4: Z. 3467 ERGÄNZT durch R53 (49.1) (T4) |
| 22 Methodenantwort 19.09. | 1 | 22.1 allgemeine Prüfregel; 22.2 Kill-Test-Berichtswerte; 22.3 Abschalt- und Zuschaltregeln; 22.4 Ergänzung zu RT 6 | 22.2: Z. 3742 ERGÄNZT durch R34 (48.2) (T4) |
| 23 Benchmark tagesgenau | 2 | 23.3 Ersatztext zu 3b (c) | in 23.3 selbst: Z. 4033 „ERSETZT (TB-71) durch den Satz zur Zeitachse oben“ (eine Tabelle in 23.3 durch einen Satz in 23.3); 23.3, Registertext 3b (c) **PRÄZISIERT durch R72 (53.7)** (Z. 3983, vom steuernden Chat nach R65 (a) bestimmt, T4); 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse **BERICHTIGT durch R71 (53.6)** (Z. 4014), ERGÄNZT durch R72 (53.7) (Z. 4017) (T4); 23.3, Registertext 3b (c) **PRÄZISIERT durch R87 (56.4)** (Z. 3986) |
| 24 Mark-to-Market | 2 | 24.2 Präzisierung zu RT 4; 24.3 Entscheidungsregel; 24.4 Festlegung 1 | 24.6 Tatsachennotiz; 24.2 **PRÄZISIERT durch R36 (48.4)** (Z. 4371, T4) |
| 25 erste Falte, Konjunktion | 2 | 25.3 Ersatztext zu 4a und 21.3 (b) | (i) **PRÄZISIERT durch 26.2** (Z. 4730) und **durch R53 (49.1)** (Z. 4732); 25.2: Z. 4712 ERGÄNZT durch R53 (T4); 25.3 (i) ERGÄNZT durch R58 (51.3) (Z. 4735, T4); 25.2 **BERICHTIGT durch R62 (51.7) und R65 (52.3)** (Z. 4709, T4) |
| 26 Datenhorizont je Bot | 2 | 26.2 Präzisierung zu 4a (i); 26.4 Ergänzung zu 3 (c); 26.7 Grenzfall | 26.3 (Platzhalter-Tabelle) **ERSETZT** durch 28.4; 26.6 Zeilen 1 und 4 **ERSETZT** durch 28.5, Zeile 2 dort „erledigt“ (MARKE+); 28 „Berichtigung zu 26.3 und 26.6“; 31.6 berichtigt eine Zahl aus 26 |
| 27 Sichtschutz | 2 | 27.1–27.5 | 45.6 R6 Ergänzung zu 27 (T4); 27.3: Z. 5208 ERGÄNZT durch R31 (47.14); Z. 5247 ERGÄNZT durch R32 (47.15) (T4); Z. 5250 ERGÄNZT durch R56 (51.1) (T4); Z. 5253 ERGÄNZT durch R73 (53.8) (T4); Abschnitt 27 ERGÄNZT durch R91 (57.2) (Z. 5256); Abschnitt 27 ERGÄNZT durch R94 (58.1) (Z. 5259); Abschnitt 27 ERGÄNZT durch R97 (58.4) (Z. 5262) |
| 28 `asof` gesetzt | 2 | 28.2 Ergänzung zu 5a; 28.4, 28.5 Ersatzmarken; 28.6 Präzisierung und Ergänzung zu 4a | 28.2 → 31 Berichtigung, Ersatztext **31.2**; 28.6 → 30.6 Präzisierung; 32 rechnet gegen den Horizontbeginn aus 28.4 (Überschrift 32); 28.6 **PRÄZISIERT durch R53 (49.1)** (Z. 5394, T4) |
| 29 Kapitalpfad ab erster Falte | 2 | 29.3 Registertext | 29.2 → 30.7 Ergänzung; 29.4 → 34.5 Berichtigung; in 29.4: „Fassung aus 21b ist ERSETZT“ (Z. 5473); 29.4 BERICHTIGT durch R43 (48.11) (Z. 5488, T4) |
| 30 gesperrter Faltenplan | 2 | 30.2 Registertext (1)–(3); 30.3 Tatsachennotiz Punkt 2 | 30.2 (2) → 34.3 Berichtigung; 30.2 (3) → 33.1 Berichtigung, 35.4 Präzisierung, 45.3 R3 Ergänzung (T4). **Mehrdeutig, welche Fassung von 30.2 (3) gilt, Abschnitte 33, 35, 45** |
| 31 kein Feld `asof` | 2 | 31.2 Ersatztext zu 28.2; 31.3 Präzisierung zu 5a/17.1 | – |
| 32 Horizontbeginn | 2 | Tatsachennotizen, 32.5 Entscheidungsvorlage | – |
| 33 Faltenplan als Registertext | 2 | 33.2 Registertext; 33.3 Feldliste; 33.4 Anpassungen | 33.2 → 34.1, 34.2, 35.1 Ergänzungen (35.1 → **38.1 Berichtigung**, T3); 33.3 → 34.4, 35.2 Ergänzungen, 42.1 D5 Präzisierung (→ 42.2 E3 BERICHTIGT), 45.3 R3; 33.4 Punkt 3 **ERSETZT** (35.3; MARKE+ Z. 6165), 34.6 Berichtigung. **33.2 und 33.3 sind mehrdeutig: Grundtext plus Ergänzungen in 34, 35, 38, 42 und 45** |
| 34 Faltenregeln, Feld `horizontbeginn` | 2 | 34.1–34.6 | 34.5 BERICHTIGT durch R43 (48.11) (Z. 6339, T4) |
| 35 Bestätigungsperiode | 2 | 35.1–35.4 | 35.1 → 38.1 Berichtigung (T3); 35.4 → 42.1 D5 (T3); 35.1 **PRÄZISIERT durch R37 (48.5)** (Z. 6497); 35.4 ERGÄNZT durch R26 (47.9) (Z. 6577) (T4) |
| 36 Schreibregel, Sonde, Abbild | 2 | 36.1 Schreibregel; 36.2 Sonde; 36.5 drei Ausgänge; 36.6 Abbild | 36.2 → 36.5 Berichtigung, 37.3 Ergänzung; 36.5 → 37.1 Präzisierung, 46.5 R14 Ergänzung (T4); 36.6 → 37.2, 37.3 Ergänzung |
| 37 Sonde je Bestandteil | 3 | 37.1–37.3; 37.4 Tatsachennotiz zu Abschnitt 10; 37.5 „Ort registrierter Werte“ | in 37.4: Z. 7127 ERSETZT (38.6); Z. 7139 **BERICHTIGT durch 42.3 F2** |
| 38 Weg (A), Fundstellen | 3 | 38.1 Berichtigung zu 35.1; **38.2 Fundstellen**; 38.4 Form (ii); 38.5 Kosten | 38.4 Fertigkriterium **ERSETZT (39.1)** (MARKE+ Z. 7488); 38.2 ERGÄNZT durch R49 (48.17) (Z. 7451, T4) |
| 39 Vollzug Punkt 4 | 3 | 39.1 Berichtigung zu 38.4; 39.2 Vollzug; 39.3–39.9 Tatsachennotizen | – |
| 40 Testannahmen, Handelslisten | 3 | 40.2 `G6`; 40.3 `H3`; 40.6 Handelslisten; 40.7 Ergänzung zu 12; 40.8 Beschlossenes | 40.6 → 41.1 A3 Berichtigung, A12 Präzisierung, 46.3 R12 (T4); 40.7 → 41.1 A2 Berichtigung; 40.8 (e) → 46.1 R9 Ergänzung (T4); 40.6 ERGÄNZT durch R42 (48.10), R44 (48.12), Tatsachennotiz zu 5.4 **PRÄZISIERT durch R47 (48.15)** (Z. 8491–8497, T4); 40.6 **PRÄZISIERT durch R86 (56.3)** (Z. 8500) |
| 41 aus 24b/24c/24d | 3 | 41.1 A1–A12; 41.2 B1–B8; 41.3 C-Einträge | A10 → 46.2 R10 Ergänzung (T4); A11 **PRÄZISIERT durch 42.1** (D2, D3; Z. 8799); A12 ERGÄNZT durch 41.2 (B3, B6/B7); B4 **PRÄZISIERT durch 42.1 (D6)** (Z. 8840); B5 BERICHTIGT durch 42.1 (D1), ERGÄNZT durch 41.3 (C6); B8 BERICHTIGT durch 41.3 (C8); C5 BERICHTIGT durch 42.1 (D5); B6/B7 ERGÄNZT durch R41 (48.9) (Z. 8925, T4); 41.3 C2 ERGÄNZT durch R86 (56.3) (Z. 8961) |
| 42 aus 25a/25b/25c | 3 | 42.1 D1–D12; 42.2 E-Einträge; 42.3 F-Einträge; 42.4/42.5 Tatsachennotizen | D6 ERGÄNZT durch 42.2 (E1, E2) und 42.3 (F7, F8); D2 ERGÄNZT durch 42.2 (E1), 42.3 (F8); D3/D7 **PRÄZISIERT durch 42.2 (E6)** (Z. 9101); D5 BERICHTIGT durch 42.2 (E3); D8 BERICHTIGT durch 42.2 (E5); 42 (Klasse (iv)) → 45.2 R2; 42.2 E2 → 45.4 R4 (T4); E5 ERGÄNZT durch R29 (47.12) (Z. 9317, T4); 42.2 E6 ERGÄNZT durch R81 (55.4) (Z. 9327) |
| 43 aus 25d/25e | 4 | 43.1, 43.2; 43.3 Berichtigung an 25e (3), vorläufig | 43.3 → 45.1 R1 „Marke an 43.3 (Bestätigung)“ (T4); 43-7 **PRÄZISIERT durch R33 (48.1)** (Z. 9810, T4) |
| 44 Vollzug TB-111/112 | 4 | Tatsachennotizen | 44-6 ERGÄNZT durch R29 (47.12) (Z. 10097) |
| 45 aus 26a | 4 | R1–R8 (45.1–45.8), R11 (45.11) | R5, R7 → 46.7 R16 Ergänzungen; 45.3 ERGÄNZT durch R42 (48.10); R4 und R5 (a) ERGÄNZT durch R29 (47.12); R5 (b) **BERICHTIGT durch R33 (48.1)**; 45.5 ERGÄNZT durch R34 (48.2), **PRÄZISIERT durch R36 (48.4)** (Z. 10317–10357) |
| 46 aus 27a | 4 | R9–R17 (46.1–46.8); 46.9 Lesart; 46.11 Vollzug | 46.3 ERGÄNZT durch R39 (48.7), R42 (48.10); R14 ERGÄNZT durch R25, R26, R27 (Bedingung 5); 46.9 ERGÄNZT durch R25 (47.8, Bestätigung) (Z. 10548–10653); 46.4 R13 ERGÄNZT durch R79 (55.2) (Z. 10565) |
| 47 aus 27c | 4 | R18–R32 (47.1–47.15) | 47.9 R26 **BERICHTIGT durch R61 (51.6)** (Z. 10817); 47.13 R30 **BERICHTIGT durch R61 (51.6)** (Z. 10848); beide nachgetragen nach R65 (b) (52.3) |
| 48 aus 29b | 4 | R33–R52 (48.1–48.20); R51 = Marken für Register 0–12 | 48.16 R48 (g) **BERICHTIGT durch R54 (49.2)** (Z. 11090); 48.16 R48 (d) ERGÄNZT durch R60 (51.5) (Z. 11093); 48.16 R48 (d) **PRÄZISIERT durch R64 (52.2)** (Z. 11096); 48.19 R51 **PRÄZISIERT durch R65 (52.3)** (Z. 11134); 48.1 R33 **PRÄZISIERT durch R68 (53.3)** (Z. 10881); 48.5 R37 **PRÄZISIERT durch R68 (53.3)** (Z. 10933); 48.7 R39 ERGÄNZT durch R67 (53.2) (Z. 10953) und durch R69 (53.4): R39 ist bestätigt (Z. 10956); 48.16 R48 (d) ERGÄNZT durch R72 (53.7) (Z. 11099); 48.1 R33 **PRÄZISIERT durch R75 (54.2)** (Z. 10884, vom steuernden Chat nach R65 (a) bestimmt); 48.2 R34 ERGÄNZT durch R75 (54.2) (Z. 10900); 48.4 R36 **PRÄZISIERT durch R75 (54.2)** (Z. 10920); 48.5 R37 **PRÄZISIERT durch R75 (54.2)** (Z. 10936); 48.7 R39 ERGÄNZT durch R75 (54.2) (Z. 10959); 48.14 R46 ERGÄNZT durch R75 (54.2) (Z. 11032, vom steuernden Chat nach R65 (a) bestimmt); 48.20 R52: Zählung der Fälle „Bestand behauptet statt Voraussetzung genannt“ → R76 (54.3), zwölf gezählte Fälle (ohne Marke, R77 (c)); 48.1 R33 ERGÄNZT durch R82 (55.5) (Z. 10887); 48.2 R34 ERGÄNZT durch R82 (55.5) (Z. 10903); 48.11 R43 ERGÄNZT durch R81 (55.4) (Z. 10993); 48.14 R46 ERGÄNZT durch R78 (55.1) und R81 (55.4) (Z. 11035); 48.18 R50 ERGÄNZT durch R81 (55.4) und R83 (55.6) (Z. 11124); 48.1 R33 **PRÄZISIERT durch R85 (56.2)** (Z. 10890); 48.4 R36 **PRÄZISIERT durch R85 (56.2)** (Z. 10923); 48.7 R39 ERGÄNZT durch R81 (55.4) (Z. 10962, nachgetragen nach R89 (d)); 48.11 R43 ERGÄNZT durch R87 (56.4) (Z. 10996); 48.12 R44 **PRÄZISIERT durch R86 (56.3)** (Z. 11006); 48.13 R45 **PRÄZISIERT durch R84 (56.1)** (Z. 11016); 48.14 R46 ERGÄNZT durch R60 (51.5) (Z. 11038, nachgetragen nach R89 (d)), ERGÄNZT durch R64 (52.2) (Z. 11041, nachgetragen nach R89 (d)), ERGÄNZT durch R66 (53.1) (Z. 11044, nachgetragen nach R89 (d)), ERGÄNZT durch R67 (53.2) (Z. 11047, nachgetragen nach R89 (d)), ERGÄNZT durch R84 (56.1) (Z. 11050), ERGÄNZT durch R85 (56.2) (Z. 11053), ERGÄNZT durch R87 (56.4) (Z. 11056); 48.14 R46 ERGÄNZT durch R90 (57.1) (Z. 11059); 48.13 R45 **PRÄZISIERT durch R95 (58.2)** (Z. 11019); 48.13 R45 ERGÄNZT durch R97 (58.4) (Z. 11022); 48.14 R46 ERGÄNZT durch R94 (58.1) (Z. 11062) |
| 49 aus 30a | 4 | R53–R55 (49.1–49.3) | 49.1 R53 **PRÄZISIERT durch R57 (51.2)** (Z. 11155), ERGÄNZT durch R59 (51.4) (Z. 11158) |
| 50 Tatsachennotizen E-2 | 4 | 50.1 Voraussetzungen; 50.2 Feldliste (R39); 50.3/50.4 Vollzug TB-122/TB-124; 50.5 Lesart Zählweise (vorläufig); 50.6 Entscheid R24; 50.7 Offenes | 50.5 ERGÄNZT durch R57 (51.2): die Lesart ist bestätigt (Z. 11341); 50.1, Zeile R48 (d) ERGÄNZT durch R60 (51.5) und 51.8 (Z. 11202); 50.4, Schlusssatz ERGÄNZT durch R57 (51.2): bestätigt (Z. 11332); beide nachgetragen nach R65 (b) (52.3) |
| 51 aus 01a | 4 | R56–R62 (51.1–51.7); 51.8 Voraussetzungen; 51.9 Lesart, vorläufig; 51.10 Offenes | 51.5 R60 (a) **PRÄZISIERT durch R63 (52.1)** (Z. 11403), R60 (b) und (c) **PRÄZISIERT durch R64 (52.2)** (Z. 11406); 51.6 R61 (b) **PRÄZISIERT durch R65 (52.3)** (Z. 11422); 51.9 ERGÄNZT durch R63 (52.1): die Lesart ist bestätigt (Z. 11460); 51.5 R60 **PRÄZISIERT durch R69 (53.4)** (Z. 11409); 51.6 R61 **PRÄZISIERT durch R70 (53.5)** (Z. 11425); 51.5 R60 **PRÄZISIERT durch R75 (54.2)** (Z. 11412) |
| 52 aus 02a | 4 | R63–R65 (52.1–52.3); 52.4 Voraussetzungen; 52.5 Offenes | 52.2 R64 ERGÄNZT durch R66 (53.1), zu (e) (Z. 11492); 52.2 R64 **PRÄZISIERT durch R68 (53.3)** (Z. 11495), **durch R69 (53.4)** (Z. 11498), **durch R71 (53.6): erster Kurstag** (Z. 11501) und **durch R72 (53.7): Benchmark-Tag** (Z. 11504); 52.3 R65 **PRÄZISIERT durch R70 (53.5)** (Z. 11517); 52.4, Zeile „R64 (52.2), zweite“ ERGÄNZT durch R66 (53.1) (Z. 11538); 52.4, Zeile „R64 (52.2) (a)“ **BERICHTIGT durch R69 (53.4)** (Z. 11541); 52.2 R64 **PRÄZISIERT durch R75 (54.2)** (Z. 11507); 52.3 R65 **PRÄZISIERT durch R89 (56.6)** (Z. 11520) |
| 53 aus 02c | 4 | R66–R73 (53.1–53.8); 53.9 Voraussetzungen und Befunde; 53.10 Offenes | 53.1 R66 **PRÄZISIERT durch R74 (54.1)** (Z. 11567); 53.3 R68 **PRÄZISIERT durch R75 (54.2)** (Z. 11593); 53.4 R69 ERGÄNZT durch R75 (54.2) (Z. 11606); 53.5 R70 **PRÄZISIERT durch R77 (54.4)** (Z. 11616); 53.9, Zeile „R66 (53.1) (b)“ ERGÄNZT durch R74 (54.1) (Z. 11678); 53.1 R66 **PRÄZISIERT durch R78 (55.1)** (Z. 11570), ERGÄNZT durch R81 (55.4) (Z. 11573); 53.2 R67 ERGÄNZT durch R78 (55.1) und R82 (55.5) (Z. 11583); 53.7 R72 **PRÄZISIERT durch R78 (55.1)** (Z. 11636), **BERICHTIGT durch R78 (55.1)** (Z. 11639), ERGÄNZT durch R79 (55.2) (Z. 11642); 53.9, Zeile „R72 (53.7), zweite“ ERGÄNZT durch R78 (55.1) und R83 (55.6) (Z. 11681); 53.9, Zeile „R72 (53.7) (d)“ ERGÄNZT durch R79 (55.2) und R78 (55.1) (Z. 11684); 53.3 R68 **PRÄZISIERT durch R85 (56.2)** (Z. 11596); 53.5 R70 **PRÄZISIERT durch R89 (56.6)** (Z. 11619); 53.7 R72 **PRÄZISIERT durch R88 (56.5)** (Z. 11645) |
| 54 aus 04a | 5 | R74–R77 (54.1–54.4); 54.5 Voraussetzungen und Befunde; 54.6 Offenes | 54.1 R74 **PRÄZISIERT durch R78 (55.1)** (Z. 11713), ERGÄNZT durch R79 (55.2): die Bedingung aus (e) ist gemessen erfüllt (Z. 11716); 54.5, Zeile „R74 (54.1) (e)“ ERGÄNZT durch R79 (55.2) (Z. 11764); 54.2 R75 **PRÄZISIERT durch R84 (56.1)** (Z. 11726), **PRÄZISIERT durch R85 (56.2)** (Z. 11729); 54.5, Zeile „R75 (54.2) (a)“ ERGÄNZT durch R84 (56.1) (Z. 11767) |
| 55 aus 07a | 5 | R78–R83 (55.1–55.6); 55.7 Voraussetzungen und Befunde; 55.8 Offenes | 55.1 R78 **BERICHTIGT durch R88 (56.5)** (Z. 11796), **PRÄZISIERT durch R88 (56.5)** (Z. 11799); 55.3 R80 ERGÄNZT durch R88 (56.5) (Z. 11822), ERGÄNZT durch R89 (56.6) (Z. 11825); 55.4 R81 ERGÄNZT durch R86 (56.3) (Z. 11835), ERGÄNZT durch R87 (56.4) (Z. 11838); 55.5 R82 **BERICHTIGT durch R88 (56.5)** (Z. 11854); 55.6 R83 ERGÄNZT durch R88 (56.5) (Z. 11864); 55.7, Zeile „R78 (55.1) (a), erste“ ERGÄNZT durch R88 (56.5) (Z. 11894, nachgetragen nach R93 (a)) |
| 56 aus 09a | 5 | R84–R89 (56.1–56.6); 56.7 Voraussetzungen und Befunde; 56.8 Offenes | 56.1 R84 ERGÄNZT durch R91 (57.2) (Z. 11927); 56.3 R86 ERGÄNZT durch R92 (57.3) (Z. 11947); 56.4 R87 ERGÄNZT durch R90 (57.1) (Z. 11963); 56.5 R88 **PRÄZISIERT durch R91 (57.2)** (Z. 11973); 56.7, Zeile „R87 (56.4) (d)“ ERGÄNZT durch R90 (57.1) (Z. 12009); 56.7, Zeilen „R84 (56.1) (e), erste“ und „R84 (56.1) (e), zweite“ ERGÄNZT durch R91 (57.2) (Z. 12012); 56.7, Zeile „R86 (56.3) (e)“ ERGÄNZT durch R92 (57.3) (Z. 12015); 56.1 R84 **PRÄZISIERT durch R95 (58.2)** (Z. 11930); 56.3 R86 ERGÄNZT durch R98 (61.1) (Z. 11950) |
| 57 aus 10a | 5 | R90–R93 (57.1–57.4); 57.5 Voraussetzungen und Befunde; 57.6 Offenes | 57.1 R90 ERGÄNZT durch R98 (61.1) (Z. 12051); 57.2 R91 **PRÄZISIERT durch R99 (61.2)** (Z. 12067) |
| 58 aus 14a und 14b | 6 | R94–R96 (58.1–58.3, 14a); R97 (58.4, 14b); 58.5 Voraussetzungen und Befunde | 58.2 R95 **BERICHTIGT durch R97 (58.4)** (Z. 12143); 58.3 R96 **BERICHTIGT durch R97 (58.4)** (Z. 12153) |
| 59 Tatsachennotiz TB-162 | 6 | 59.1 Tatsachennotiz zu 24.2, 24.3, R36 und 11.2 mit R43 (Kapital-Drawdown E und M je WF-Abschnitt; aus ERGEBNIS_TB-162 Z. 199–232) | – |
| 60 Vollzug TB-163 | 6 | 60.1 Hash-Übergang nach 37.3 (E-6, vier Aktien-Optimierer, Commit `11a267f`; aus ERGEBNIS_TB-163 Z. 111–123) mit Sonde zu Punkt 11; 60.2 Tatsachennotiz Posten 5 nach R43 („nicht im Laufpfad“, neun Optimierer) | – |
| 61 aus 15a | 6 | R98–R99 (61.1–61.2); 61.3 Voraussetzungen und Befunde | – |
| 62 aus 15b und 16b | 6 | R100–R103 (62.1–62.4); 62.5 Voraussetzungen und Befunde | – |
| 63 Vollzug TB-167 | 6 | 63.1 Hash-Übergang nach 37.3 (Abhilfe G6 elliott_wave_stocks, Commit `b6aaa24`; aus ERGEBNIS_TB-167 Z. 47–51) mit Freigabe-Karte und Sonde zu Punkt 11 | – |
| 64 Vollzug TB-166 | 6 | 64.1 Hash-Übergänge nach 37.3 (E-3a, 20 Dateien, Commit `15f28e4`; aus docs/belege/TB-166/e_notiz.md) mit Freigabe-Karten, Abnahme nach R98 (d) am Listen-Erzeuger (TB-169) und Sonde zu Punkt 11 | – |
| 65 aus 16c | 6 | R104–R105 (65.1–65.2); 65.3 Voraussetzungen und Befunde | – |
| 66 aus 17a | 6 | R106 (66.1); 66.2 Voraussetzungen und Befunde | – |
| 67 aus 17b | 6 | R107 (67.1); 67.2 Voraussetzungen und Befunde | – |
| 68 aus 17c | 6 | R108 (68.1); 68.2 Voraussetzungen und Befunde | – |
| 69 aus 17d | 6 | R109 (69.1); 69.2 Voraussetzungen und Befunde | – |
| 70 aus 17e | 6 | R110 (70.1); 70.2 Voraussetzungen und Befunde | – |
| 71 aus TB-180 | 6 | Bauauftrag nach R110 (b) und Probe nach R110 (c): 71.1 Nachtrag zu Punkt 9, 71.2 Tatsachennotiz, 71.3 Ergänzung zu 29.3, 71.4 Abbild, 71.5 Probe | – |

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
| 2.1 | Z. 130 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 2.2 | Z. 147 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 2.2 | Z. 150 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| 2.5 | Z. 206 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 2.7 | Z. 247 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| 3, Zahlenteil (nach ENDE ERZEUGT) | Z. 462 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| 4.2 | Z. 519 | ERGÄNZT (Verweis) | R51 (48.19) | MARKE+ | 1 |
| 4.4 | Z. 583 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| 5.1, Nr. 7 | Z. 649 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 5.3 | Z. 709 | ERGÄNZT (Verweis) | R51 (48.19) | MARKE+ | 1 |
| 7, Tabelle, Zeile (d) | Z. 819 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 7, Tabelle, Zeile (a) | Z. 822 | ERGÄNZT (Verweis) | R51 (48.19) | MARKE+ | 1 |
| 7, Tabelle, Zeile (d) | Z. 825 | ERGÄNZT | R55 (49.3) | MARKE+ | 1 |
| 7.1 | Z. 871 | ERGÄNZT | R21 (47.4) | MARKE+ | 1 |
| 7.1 | Z. 874 | PRÄZISIERT | R23 (47.6) | MARKE | 1 |
| 8.1 | Z. 929 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 9, erster Absatz | Z. 941 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 11.2 | Z. 1240 | ERGÄNZT | R43 (48.11) | MARKE+ | 1 |
| Abschnitt 11 | Z. 1259 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| 11.3 | Z. 1262 | ERGÄNZT | 50.3 und 50.4 | MARKE+ | 1 |
| Abschnitt 12 | Z. 1330 | ERGÄNZT | R25 (47.8) | MARKE+ | 1 |
| Abschnitt 12 | Z. 1333 | ERGÄNZT | R26 (47.9) | MARKE+ | 1 |
| Abschnitt 12 | Z. 1336 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| Abschnitt 12 | Z. 1339 | ERGÄNZT | R50 (48.18) | MARKE+ | 1 |
| 15.3 (b) | Z. 1458 | ERGÄNZT | R41 (48.9) | MARKE+ | 1 |
| 15.3 | Z. 1485 | ERGÄNZT | R35 (48.3) | MARKE+ | 1 |
| 15.4 (a) | Z. 1513 | BERICHTIGT | R54 (49.2) | MARKE+ | 1 |
| 15.4 | Z. 1558 | ERGÄNZT | R41 (48.9) und 50.1 | MARKE+ | 1 |
| 15.5 | Z. 1673 | ERGÄNZT | R53 (49.1) | MARKE+ | 1 |
| 15.6 (c) | Z. 1706 | PRÄZISIERT | R23 (47.6) | MARKE | 1 |
| 15.6 | Z. 1756 | ERGÄNZT (Verweis) | R51 (48.19) | MARKE+ | 1 |
| 16.4 (b) | Z. 2118 | PRÄZISIERT | R21 (47.4) | MARKE | 1 |
| 16.4 (a) | Z. 2121 | PRÄZISIERT | R22 (47.5) | MARKE | 1 |
| 16.4 (b) | Z. 2124 | PRÄZISIERT | R23 (47.6) | MARKE | 1 |
| 16.4 (c) | Z. 2127 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 16.4 (d) | Z. 2130 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 16.4 (m) | Z. 2177 | PRÄZISIERT | R18 (47.1) | MARKE | 1 |
| 16.4 (h) | Z. 2180 | PRÄZISIERT | R18 (47.1) | MARKE | 1 |
| 16.4 (l) | Z. 2183 | PRÄZISIERT | R18 (47.1) | MARKE | 1 |
| 16.4 (h) | Z. 2186 | PRÄZISIERT | R19 (47.2) | MARKE | 1 |
| 16.4 (j) | Z. 2189 | PRÄZISIERT | R19 (47.2) | MARKE | 1 |
| 16.4 (k) | Z. 2192 | PRÄZISIERT | R19 (47.2) | MARKE | 1 |
| 16.4 (l) | Z. 2195 | ERGÄNZT | R20 (47.3) | MARKE+ | 1 |
| 16.4 (j) | Z. 2198 | ERGÄNZT | R20 (47.3) | MARKE+ | 1 |
| 16.4 (i) | Z. 2201 | PRÄZISIERT | R21 (47.4) | MARKE | 1 |
| 16.4 (j) | Z. 2204 | PRÄZISIERT | R21 (47.4) | MARKE | 1 |
| 16.4 (i) | Z. 2207 | PRÄZISIERT | R22 (47.5) | MARKE | 1 |
| 16.4 (h) | Z. 2210 | ERGÄNZT | R24 (47.7) und 50.6 | MARKE+ | 1 |
| 16.4 (g) | Z. 2213 | ERGÄNZT | R24 (47.7) und 50.6 | MARKE+ | 1 |
| 16.6 | Z. 2368 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 16.7 (d) | Z. 2438 | ERGÄNZT | R38 (48.6) | MARKE+ | 1 |
| Abschnitt 18 | Z. 3125 | ERGÄNZT | R28 (47.11) | MARKE+ | 1 |
| 21.4 | Z. 3467 | ERGÄNZT | R53 (49.1) | MARKE+ | 1 |
| 22.2 | Z. 3742 | ERGÄNZT | R34 (48.2) | MARKE+ | 1 |
| 24.2 | Z. 4371 | PRÄZISIERT | R36 (48.4) | MARKE | 2 |
| 25.2 | Z. 4712 | ERGÄNZT | R53 (49.1) | MARKE+ | 2 |
| 25.3, Ersatztext (Bedingung (i) steht in dessen erster Zeile) | Z. 4732 | PRÄZISIERT | R53 (49.1) | MARKE | 2 |
| 27.3 (im Zitatblock 27.1 bis 27.5) | Z. 5208 | ERGÄNZT | R31 (47.14) | MARKE+ | 2 |
| Abschnitt 27 | Z. 5247 | ERGÄNZT | R32 (47.15) | MARKE+ | 2 |
| 28.6 | Z. 5394 | PRÄZISIERT | R53 (49.1) | MARKE | 2 |
| 29.4 | Z. 5488 | BERICHTIGT | R43 (48.11) | MARKE+ | 2 |
| 34.5 | Z. 6339 | BERICHTIGT | R43 (48.11) | MARKE+ | 2 |
| 35.1 | Z. 6497 | PRÄZISIERT | R37 (48.5) | MARKE | 2 |
| 35.4 | Z. 6577 | ERGÄNZT | R26 (47.9) | MARKE+ | 2 |
| 38.2 | Z. 7451 | ERGÄNZT | R49 (48.17) | MARKE+ | 3 |
| 40.6 | Z. 8491 | ERGÄNZT | R42 (48.10) | MARKE+ | 3 |
| 40.6 | Z. 8494 | ERGÄNZT | R44 (48.12) | MARKE+ | 3 |
| 40.6 | Z. 8497 | PRÄZISIERT | R47 (48.15) | MARKE | 3 |
| 41.2, Eintrag B6/B7 | Z. 8925 | ERGÄNZT | R41 (48.9) | MARKE+ | 3 |
| 42.2, Eintrag E5 (e) | Z. 9317 | ERGÄNZT | R29 (47.12) | MARKE+ | 3 |
| 44.1, Eintrag 44-6 | Z. 10097 | ERGÄNZT | R29 (47.12) | MARKE+ | 4 |
| 45.3 | Z. 10317 | ERGÄNZT | R42 (48.10) | MARKE+ | 4 |
| 45.4, Block R4 | Z. 10325 | ERGÄNZT | R29 (47.12) | MARKE+ | 4 |
| 45.5, Block R5, Punkt (a) | Z. 10342 | ERGÄNZT | R29 (47.12) | MARKE+ | 4 |
| 45.5, Block R5, Punkt (b) | Z. 10345 | BERICHTIGT | R33 (48.1) | MARKE+ | 4 |
| 45.5 | Z. 10354 | ERGÄNZT | R34 (48.2) | MARKE+ | 4 |
| 45.5 | Z. 10357 | PRÄZISIERT | R36 (48.4) | MARKE | 4 |
| 46.3 | Z. 10548 | ERGÄNZT | R39 (48.7) | MARKE+ | 4 |
| 46.3 | Z. 10551 | ERGÄNZT | R42 (48.10) | MARKE+ | 4 |
| 46.5, Block R14 | Z. 10582 | ERGÄNZT | R25 (47.8) | MARKE+ | 4 |
| 46.5, Block R14 | Z. 10585 | ERGÄNZT | R26 (47.9) | MARKE+ | 4 |
| 46.5, Block R14 (Bedingung 5 steht in dessen erster Zeile) | Z. 10588 | ERGÄNZT | R27 (47.10) | MARKE+ | 4 |
| 46.9 | Z. 10653 | ERGÄNZT | R25 (47.8) | MARKE+ | 4 |
| 48.16 (R48), neu in TB-126 | Z. 11090 | BERICHTIGT | R54 (49.2) | MARKE+ | 4 |

## 6. Die Marken aus Fable 01a (TB-129)

Alle 14 Marken, die TB-129 gesetzt hat (alle am alten Ort: die zwölf Zeilen aus R61 (b), davon zwei Orte mit je zwei
Blöcken), in der Reihenfolge des Registers. Erzeugt mit `docs/belege/TB-129/c2_index_01a.py` aus
`docs/belege/TB-129/c1_marken.txt` (Zeile, Art, Teil) und Anhang A des Auftrags TB-129 (alter Ort), nicht abgetippt.
In Tabelle 1–4 oben stehen sie zusätzlich an ihrer Stelle. Orte, die R61 (b) nicht aufzählt, tragen keine Marke;
sie stehen als Indexzeilen darunter und gehen als Frage an Fable (51.10 Nr. 7).

| alter Ort (Anhang A) | Marke | Wort | durch | Art | T |
|---|---|---|---|---|---|
| 1, Tabelle, Zeile 3 | Z. 83 | PRÄZISIERT | R36 (48.4) | MARKE | 1 |
| 4.2 | Z. 522 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 4.2 | Z. 525 | PRÄZISIERT | R60 (51.5) | MARKE | 1 |
| 7, Tabelle, Zeile (b) | Z. 828 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 8, Tabelle | Z. 899 | PRÄZISIERT | R36 (48.4) | MARKE | 1 |
| 8, Tabelle | Z. 902 | ERGÄNZT | R55 (49.3) | MARKE+ | 1 |
| 16.4, „Prüfung vor dem Tag“ | Z. 2256 | PRÄZISIERT | R21 (47.4) | MARKE | 1 |
| 25.3, Ersatztext | Z. 4735 | ERGÄNZT | R58 (51.3) | MARKE+ | 2 |
| Abschnitt 27 | Z. 5250 | ERGÄNZT | R56 (51.1) | MARKE+ | 2 |
| 43.2, Eintrag 43-7 | Z. 9810 | PRÄZISIERT | R33 (48.1) | MARKE | 4 |
| 48.16 (R48) | Z. 11093 | ERGÄNZT | R60 (51.5) | MARKE+ | 4 |
| 49.1 (R53) | Z. 11155 | PRÄZISIERT | R57 (51.2) | MARKE | 4 |
| 49.1 (R53) | Z. 11158 | ERGÄNZT | R59 (51.4) | MARKE+ | 4 |
| 50.5 | Z. 11341 | ERGÄNZT | R57 (51.2): die Lesart ist bestätigt | MARKE+ | 4 |

### Indexzeilen aus Fable 01a

- **Tag-Vorbedingungen** (Fable 01a, Frage 7, empfohlen): R15 (b) (46.6) · R27 (47.10) · R29 (47.12) · R30 (47.13).
- **47.9 (R26):** „14“ lies „Sperrlistenpunkt 14 (Abschnitt 10)“ → R61 (c) (51.6). Marke gesetzt in TB-130 (R65 (b), 52.3).
- **47.13 (R30):** „Ergänzung zu 14“ lies „Ergänzung zu Sperrlistenpunkt 14 (Abschnitt 10)“ → R61 (c) (51.6). Marke gesetzt in TB-130 (R65 (b), 52.3).
- **25.2:** „der 150. Balken liegt am 2018-01-14“ → Tatsachennotiz R62 (a) (51.7). Marke gesetzt in TB-130 (R65 (b), 52.3).
- **50.1, Zeile R48 (d):** ergänzt durch R60 (d) (51.5) und 51.8. Marke gesetzt in TB-130 (R65 (b), 52.3).
- **50.4, Schlusssatz:** bestätigt durch R57 (51.2). Marke gesetzt in TB-130 (R65 (b), 52.3).

## 7. Die Marken aus Fable 02a (TB-130)

Alle 12 Marken, die TB-130 gesetzt hat (alle am alten Ort: fünf nach R65 (b), sieben vom steuernden Chat nach R65 (a)
bestimmt; 51.5 trägt zwei), in der Reihenfolge des Registers. Erzeugt mit `docs/belege/TB-130/c2_index_02a.py` aus
`docs/belege/TB-130/c1_marken.txt` (Zeile, Art, Teil) und Anhang A des Auftrags TB-130 (alter Ort), nicht abgetippt.
In Tabelle 2 und 4 oben stehen sie zusätzlich an ihrer Stelle. Keine Marke tragen 7 (c) (52.5 Nr. 9), Abschnitt 9,
Abschnitt 10 und der ERZEUGT-Block von Abschnitt 3 (R65 (d)).

| alter Ort (Anhang A) | Marke | Wort | durch | Art | T |
|---|---|---|---|---|---|
| 4.2 | Z. 528 | PRÄZISIERT | R64 (52.2) | MARKE | 1 |
| 25.2, unter dem berichtigten Satz | Z. 4709 | BERICHTIGT | R62 (51.7) und R65 (52.3) | MARKE+ | 2 |
| 47.9 (R26) | Z. 10817 | BERICHTIGT | R61 (51.6) | MARKE+ | 4 |
| 47.13 (R30) | Z. 10848 | BERICHTIGT | R61 (51.6) | MARKE+ | 4 |
| 48.16 (R48) | Z. 11096 | PRÄZISIERT | R64 (52.2) | MARKE | 4 |
| 48.19 (R51) | Z. 11134 | PRÄZISIERT | R65 (52.3) | MARKE | 4 |
| 50.1, nach der Tabelle | Z. 11202 | ERGÄNZT | R60 (51.5) und 51.8 | MARKE+ | 4 |
| 50.4, nach dem Zitatblock | Z. 11332 | ERGÄNZT | R57 (51.2): der Schlusssatz ist bestätigt | MARKE+ | 4 |
| 51.5 (R60) | Z. 11403 | PRÄZISIERT | R63 (52.1) | MARKE | 4 |
| 51.5 (R60) | Z. 11406 | PRÄZISIERT | R64 (52.2) | MARKE | 4 |
| 51.6 (R61) | Z. 11422 | PRÄZISIERT | R65 (52.3) | MARKE | 4 |
| 51.9 | Z. 11460 | ERGÄNZT | R63 (52.1): die Lesart ist bestätigt | MARKE+ | 4 |

## 8. Die Marken aus Fable 02c (TB-132)

Alle 21 Marken, die TB-132 gesetzt hat (alle am alten Ort: 20 nach R70 (c), eine an 23.3, Registertext 3b (c), vom
steuernden Chat nach R65 (a) bestimmt; 52.2 trägt fünf), in der Reihenfolge des Registers. Erzeugt mit
`docs/belege/TB-132/c2_index_02c.py` aus `docs/belege/TB-132/c1_marken.txt` (Zeile, Art, Teil) und Anhang A des
Auftrags TB-132 (alter Ort), nicht abgetippt. In Tabelle 3 und 4 oben stehen sie zusätzlich an ihrer Stelle. Keine
Marke tragen Abschnitt 9, Abschnitt 10 und der ERZEUGT-Block von Abschnitt 3; ohne Marke bleiben 7 (c), 17.5 und
50.7 Nr. 3 (R70 (b), Indexzeilen darunter) sowie 24.2 und 29.3 (R70 (c)).

| alter Ort (Anhang A) | Marke | Wort | durch | Art | T |
|---|---|---|---|---|---|
| 15.3 (a) | Z. 1461 | PRÄZISIERT | R66 (53.1) | MARKE | 1 |
| 15.3 (c) | Z. 1464 | PRÄZISIERT | R66 (53.1) | MARKE | 1 |
| 23.3, Registertext 3b (c) | Z. 3983 | PRÄZISIERT | R72 (53.7) | MARKE | 2 |
| 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse | Z. 4014 | BERICHTIGT | R71 (53.6) | MARKE+ | 2 |
| 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse | Z. 4017 | ERGÄNZT | R72 (53.7) | MARKE+ | 2 |
| Abschnitt 27 | Z. 5253 | ERGÄNZT | R73 (53.8) | MARKE+ | 2 |
| 48.1 (R33) | Z. 10881 | PRÄZISIERT | R68 (53.3) | MARKE | 4 |
| 48.5 (R37) | Z. 10933 | PRÄZISIERT | R68 (53.3) | MARKE | 4 |
| 48.7 (R39) | Z. 10953 | ERGÄNZT | R67 (53.2) | MARKE+ | 4 |
| 48.7 (R39) | Z. 10956 | ERGÄNZT | R69 (53.4): R39 ist bestätigt | MARKE+ | 4 |
| 48.16 (R48 (d)) | Z. 11099 | ERGÄNZT | R72 (53.7) | MARKE+ | 4 |
| 51.5 (R60) | Z. 11409 | PRÄZISIERT | R69 (53.4) | MARKE | 4 |
| 51.6 (R61) | Z. 11425 | PRÄZISIERT | R70 (53.5) | MARKE | 4 |
| 52.2 (R64) | Z. 11492 | ERGÄNZT | R66 (53.1) | MARKE+ | 4 |
| 52.2 (R64) | Z. 11495 | PRÄZISIERT | R68 (53.3) | MARKE | 4 |
| 52.2 (R64) | Z. 11498 | PRÄZISIERT | R69 (53.4) | MARKE | 4 |
| 52.2 (R64) | Z. 11501 | PRÄZISIERT | R71 (53.6): erster Kurstag | MARKE | 4 |
| 52.2 (R64) | Z. 11504 | PRÄZISIERT | R72 (53.7): Benchmark-Tag | MARKE | 4 |
| 52.3 (R65) | Z. 11517 | PRÄZISIERT | R70 (53.5) | MARKE | 4 |
| 52.4, nach der Tabelle | Z. 11538 | ERGÄNZT | R66 (53.1) | MARKE+ | 4 |
| 52.4, nach der Tabelle | Z. 11541 | BERICHTIGT | R69 (53.4) | MARKE+ | 4 |

### Indexzeilen aus Fable 02c

- **7 (c):** mittlere Exposure des Gewinners, Tage nach R64 (a), (b) und (d) (52.2). Ohne Marke (R70 (a) und (b), 53.5).
- **17.5:** Handelskalender der Aktien-Tagesreihe → R66 (a) und (b) (53.1). Ohne Marke (R70 (b), 53.5).
- **50.7 Nr. 3:** Tagesbasis des DSR → R66 (f) (53.1). Ohne Marke (R70 (b), 53.5).

## 9. Die Marken aus Fable 04a (TB-136)

Alle 15 Marken, die TB-136 gesetzt hat (alle am alten Ort: 13 nach R77 (a), zwei an 48.1 (R33) und 48.14 (R46), vom
steuernden Chat nach R65 (a) bestimmt), in der Reihenfolge des Registers. Erzeugt mit
`docs/belege/TB-136/c2_index_04a.py` aus `docs/belege/TB-136/c1_marken.txt` (Zeile, Art, Teil) und Anhang A des
Auftrags TB-136 (alter Ort), nicht abgetippt. In Tabelle 3 und 4 oben stehen sie zusätzlich an ihrer Stelle. Keine
Marke tragen Abschnitt 9, Abschnitt 10 und der ERZEUGT-Block von Abschnitt 3; ohne Marke bleiben 48.20 (R52)
(Indexzeile darunter), 53.10, 50.2, 29.3, 41.3, 35.1 und 27.2 (R77 (c)).

| alter Ort (Anhang A) | Marke | Wort | durch | Art | T |
|---|---|---|---|---|---|
| 16.6 | Z. 2371 | PRÄZISIERT | R75 (54.2) | MARKE | 1 |
| 17.5 | Z. 2875 | ERGÄNZT | R74 (54.1) | MARKE+ | 1 |
| 48.1 (R33) | Z. 10884 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 48.2 (R34) | Z. 10900 | ERGÄNZT | R75 (54.2) | MARKE+ | 4 |
| 48.4 (R36) | Z. 10920 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 48.5 (R37) | Z. 10936 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 48.7 (R39) | Z. 10959 | ERGÄNZT | R75 (54.2) | MARKE+ | 4 |
| 48.14 (R46) | Z. 11032 | ERGÄNZT | R75 (54.2) | MARKE+ | 4 |
| 51.5 (R60) | Z. 11412 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 52.2 (R64) | Z. 11507 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 53.1 (R66) | Z. 11567 | PRÄZISIERT | R74 (54.1) | MARKE | 4 |
| 53.3 (R68) | Z. 11593 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 53.4 (R69) | Z. 11606 | ERGÄNZT | R75 (54.2) | MARKE+ | 4 |
| 53.5 (R70) | Z. 11616 | PRÄZISIERT | R77 (54.4) | MARKE | 4 |
| 53.9, nach der Tabelle | Z. 11678 | ERGÄNZT | R74 (54.1) | MARKE+ | 4 |

### Indexzeilen aus Fable 04a

- **17.5:** Handelskalender der Aktien-Tagesreihe → R66 (a) und (b) (53.1) und R74 (54.1). Zu R74 mit Marke (R77 (a) und (b), 54.4); zu R66 gilt die Indexzeile aus Fable 02c weiter (R70 (b), 53.5).
- **48.20 (R52):** Zählung der Fälle „Bestand behauptet statt Voraussetzung genannt“ → R76 (54.3): zwölf gezählte Fälle bis zur Antwort 02c. Ohne Marke (R77 (c), 54.4). Lesart des steuernden Chats zu R77 (c), vorläufig; der Index ist kein Registertext.

## 10. Die Marken aus Fable 07a (TB-139)

Alle 20 Marken, die TB-139 gesetzt hat (alle am alten Ort, an den 15 Orten nach R80 (a)), in der Reihenfolge des
Registers. Erzeugt mit `docs/belege/TB-139/c2_index_07a.py` aus `docs/belege/TB-139/c1_marken.txt` (Zeile, Art, Teil)
und Anhang A des Auftrags TB-139 (alter Ort), nicht abgetippt. In Tabelle 2 und 4 oben stehen sie zusätzlich an ihrer
Stelle. Keine Marke tragen Abschnitt 9, Abschnitt 10 und der ERZEUGT-Block von Abschnitt 3; ohne Marke bleiben nach
R80 (b) die Statuslisten 53.10, 54.6 und 50.7 und die Orte, die R80 (b) als Quelle des Grundes oder Geltungsbereich
aufzählt, dazu 48.20 (R52), 54.3 (R76) und Abschnitt 10, Punkte 6, 10 und 11 (Indexzeilen darunter). Die Blöcke
R78–R80 der Antwort 06.10.a sind nicht eingetragen und tragen keine Marke (R80 (d)).

| alter Ort (Anhang A) | Marke | Wort | durch | Art | T |
|---|---|---|---|---|---|
| 5.2 | Z. 676 | PRÄZISIERT | R81 (55.4) | MARKE | 1 |
| 5.2 | Z. 679 | ERGÄNZT | R83 (55.6) | MARKE+ | 1 |
| 42.2, Eintrag E6 | Z. 9327 | ERGÄNZT | R81 (55.4) | MARKE+ | 3 |
| 46.4 (R13) | Z. 10565 | ERGÄNZT | R79 (55.2) | MARKE+ | 4 |
| 48.1 (R33) | Z. 10887 | ERGÄNZT | R82 (55.5) | MARKE+ | 4 |
| 48.2 (R34) | Z. 10903 | ERGÄNZT | R82 (55.5) | MARKE+ | 4 |
| 48.11 (R43) | Z. 10993 | ERGÄNZT | R81 (55.4) | MARKE+ | 4 |
| 48.14 (R46) | Z. 11035 | ERGÄNZT | R78 (55.1) und R81 (55.4) | MARKE+ | 4 |
| 48.18 (R50) | Z. 11124 | ERGÄNZT | R81 (55.4) und R83 (55.6) | MARKE+ | 4 |
| 53.1 (R66) | Z. 11570 | PRÄZISIERT | R78 (55.1) | MARKE | 4 |
| 53.1 (R66) | Z. 11573 | ERGÄNZT | R81 (55.4) | MARKE+ | 4 |
| 53.2 (R67) | Z. 11583 | ERGÄNZT | R78 (55.1) und R82 (55.5) | MARKE+ | 4 |
| 53.7 (R72) | Z. 11636 | PRÄZISIERT | R78 (55.1) | MARKE | 4 |
| 53.7 (R72) | Z. 11639 | BERICHTIGT | R78 (55.1) | MARKE+ | 4 |
| 53.7 (R72) | Z. 11642 | ERGÄNZT | R79 (55.2) | MARKE+ | 4 |
| 53.9, Zeile „R72 (53.7), zweite“ | Z. 11681 | ERGÄNZT | R78 (55.1) und R83 (55.6) | MARKE+ | 4 |
| 53.9, Zeile „R72 (53.7) (d)“ | Z. 11684 | ERGÄNZT | R79 (55.2) und R78 (55.1) | MARKE+ | 4 |
| 54.1 (R74) | Z. 11713 | PRÄZISIERT | R78 (55.1) | MARKE | 5 |
| 54.1 (R74) | Z. 11716 | ERGÄNZT | R79 (55.2): die Bedingung aus (e) ist gemessen erfüllt | MARKE+ | 5 |
| 54.5, Zeile „R74 (54.1) (e)“ | Z. 11764 | ERGÄNZT | R79 (55.2) | MARKE+ | 5 |

### Indexzeilen aus Fable 07a

- **48.20 (R52):** Zählung der Fälle „Bestand behauptet statt Voraussetzung genannt“ → R76 (54.3) und R79 (g) (55.2): vierzehn gezählte Fälle bis zur Antwort 07.10.a; der dreizehnte ist der Satz „Am Bestand vom 02.10.2026 endet keine Reihe früher“ aus R72 (d), der vierzehnte der Satz zur Herkunft von 5.4.0 in der Fassung der Antwort 06.10.a, die nie eingetragen worden ist. Ohne Marke (R80 (b), 55.3); die Indexzeile aus Fable 04a bleibt stehen.
- **54.3 (R76):** Massstab der Zählung (R76 (a) und (e)) → R79 (g) (55.2): dreizehnter und vierzehnter Fall. Ohne Marke (R80 (b), 55.3). Der Index ist kein Registertext.
- **10, Sperrlistenpunkte 6, 10 und 11:** Zeilen ab dem Go-Live-Schnitt → R81 (b) (55.4): Geschnitten wird im Zellen-Erzeuger; eine Änderung an Code der Sperrliste verlangt der Block nicht, wird sie gewählt, gilt 37.3 mit der Freigabe des Betreibers. Keine Marke (Abschnitt 10; R80 (b), 55.3).

## 11. Die Marken aus Fable 09a (TB-149)

Alle 31 Marken, die TB-149 gesetzt hat (alle am alten Ort, an den 21 Orten nach R89 (d) und (g)), in der Reihenfolge
des Registers. Erzeugt mit `docs/belege/TB-149/c2_index_09a.py` aus `docs/belege/TB-149/c1_marken.txt` (Zeile, Art,
Teil) und Anhang A des Auftrags TB-149 (alter Ort), nicht abgetippt. In Tabelle 2 und 4 oben stehen sie zusätzlich an
ihrer Stelle. Fünf der Marken trägt R89 (d) nach: vier an 48.14 (R46) zu R60, R64, R66 und R67 und eine an 48.7 (R39)
zu R81. Keine Marke tragen Abschnitt 9, Abschnitt 10 und der ERZEUGT-Block von Abschnitt 3; ohne Marke bleiben nach
R89 (h) die Statuslisten 54.6 und 55.8 und die Orte, die R89 (e) und (h) als Quelle des Grundes, Bauart, Beleg oder
Geltungsbereich aufzählen, dazu Abschnitt 10, Punkt 10, 48.20 (R52) und 54.3 (R76) (Indexzeilen darunter).

| alter Ort (Anhang A) | Marke | Wort | durch | Art | T |
|---|---|---|---|---|---|
| 23.3, Registertext 3b (c) | Z. 3986 | PRÄZISIERT | R87 (56.4) | MARKE | 2 |
| 40.6 | Z. 8500 | PRÄZISIERT | R86 (56.3) | MARKE | 3 |
| 41.3, Eintrag C2 | Z. 8961 | ERGÄNZT | R86 (56.3) | MARKE+ | 3 |
| 48.1 (R33) | Z. 10890 | PRÄZISIERT | R85 (56.2) | MARKE | 4 |
| 48.4 (R36) | Z. 10923 | PRÄZISIERT | R85 (56.2) | MARKE | 4 |
| 48.7 (R39) | Z. 10962 | ERGÄNZT | R81 (55.4) | MARKE+ | 4 |
| 48.11 (R43) | Z. 10996 | ERGÄNZT | R87 (56.4) | MARKE+ | 4 |
| 48.12 (R44) | Z. 11006 | PRÄZISIERT | R86 (56.3) | MARKE | 4 |
| 48.13 (R45) | Z. 11016 | PRÄZISIERT | R84 (56.1) | MARKE | 4 |
| 48.14 (R46) | Z. 11038 | ERGÄNZT | R60 (51.5) | MARKE+ | 4 |
| 48.14 (R46) | Z. 11041 | ERGÄNZT | R64 (52.2) | MARKE+ | 4 |
| 48.14 (R46) | Z. 11044 | ERGÄNZT | R66 (53.1) | MARKE+ | 4 |
| 48.14 (R46) | Z. 11047 | ERGÄNZT | R67 (53.2) | MARKE+ | 4 |
| 48.14 (R46) | Z. 11050 | ERGÄNZT | R84 (56.1) | MARKE+ | 4 |
| 48.14 (R46) | Z. 11053 | ERGÄNZT | R85 (56.2) | MARKE+ | 4 |
| 48.14 (R46) | Z. 11056 | ERGÄNZT | R87 (56.4) | MARKE+ | 4 |
| 52.3 (R65) | Z. 11520 | PRÄZISIERT | R89 (56.6) | MARKE | 4 |
| 53.3 (R68) | Z. 11596 | PRÄZISIERT | R85 (56.2) | MARKE | 4 |
| 53.5 (R70) | Z. 11619 | PRÄZISIERT | R89 (56.6) | MARKE | 4 |
| 53.7 (R72) | Z. 11645 | PRÄZISIERT | R88 (56.5) | MARKE | 4 |
| 54.2 (R75) | Z. 11726 | PRÄZISIERT | R84 (56.1) | MARKE | 5 |
| 54.2 (R75) | Z. 11729 | PRÄZISIERT | R85 (56.2) | MARKE | 5 |
| 54.5, Zeile „R75 (54.2) (a)“ | Z. 11767 | ERGÄNZT | R84 (56.1) | MARKE+ | 5 |
| 55.1 (R78) | Z. 11796 | BERICHTIGT | R88 (56.5) | MARKE+ | 5 |
| 55.1 (R78) | Z. 11799 | PRÄZISIERT | R88 (56.5) | MARKE | 5 |
| 55.3 (R80) | Z. 11822 | ERGÄNZT | R88 (56.5) | MARKE+ | 5 |
| 55.3 (R80) | Z. 11825 | ERGÄNZT | R89 (56.6) | MARKE+ | 5 |
| 55.4 (R81) | Z. 11835 | ERGÄNZT | R86 (56.3) | MARKE+ | 5 |
| 55.4 (R81) | Z. 11838 | ERGÄNZT | R87 (56.4) | MARKE+ | 5 |
| 55.5 (R82) | Z. 11854 | BERICHTIGT | R88 (56.5) | MARKE+ | 5 |
| 55.6 (R83) | Z. 11864 | ERGÄNZT | R88 (56.5) | MARKE+ | 5 |

### Indexzeilen aus Fable 09a

- **48.20 (R52):** Zählung der Fälle „Bestand behauptet statt Voraussetzung genannt“ → R88 (f) (56.5): weiter vierzehn gezählte Fälle bis zur Antwort 09.10.a; aus den Befunden der Abnahme der Antwort 07.10.a (55.7) und aus der Anfrage 09.10.a wird kein Fall gezählt. Ohne Marke (R89 (h), 56.6); die Indexzeilen aus Fable 04a und Fable 07a bleiben stehen.
- **54.3 (R76):** Massstab der Zählung (R76 (e)) → R88 (f) (56.5): weiter vierzehn gezählte Fälle. Ohne Marke (R89 (h), 56.6). Der Index ist kein Registertext.
- **10, Sperrlistenpunkt 10:** die Rückgabe nach R45 → R84 (e) (56.1): Zu den ausgeführten Positionen gibt die Rückgabe je Ausstieg das realisierte Ergebnis heraus, wie die Zuteilung es dem Kapital zurechnet, ungerundet, in der Reihenfolge, in der die Zuteilung die Ausstiege führt; Nachweis und Freigabe nach 37.3 bleiben. Keine Marke (Abschnitt 10; R89 (h), 56.6).

## 12. Die Marken aus Fable 10a (TB-154)

Alle 11 Marken, die TB-154 gesetzt hat (alle am alten Ort, an den 9 Orten nach R93 (a) und (c)), in der Reihenfolge
des Registers. Erzeugt mit `docs/belege/TB-154/c2_index_10a.py` aus `docs/belege/TB-154/c1_marken.txt` (Zeile, Art,
Teil) und Anhang A des Auftrags TB-154 (alter Ort), nicht abgetippt. In Tabelle 2 und 4 oben stehen sie zusätzlich an
ihrer Stelle. Zwei der Marken trägt R93 (a) nach: eine an 55.7, Zeile „R78 (55.1) (a), erste“, zu R88 und eine an 15.5
zu R87. Keine Marke tragen Abschnitt 9, Abschnitt 10 und der ERZEUGT-Block von Abschnitt 3; ohne Marke bleiben nach
R93 (d) die Statusliste 56.8 und die Orte, die R93 (b) und (d) als Quelle des Grundes, Bauart, Beleg oder
Geltungsbereich aufzählen, dazu Abschnitt 10, Sperrlistenpunkte 9 und 11 (Lesart des steuernden Chats, vorläufig),
48.20 (R52) und 54.3 (R76) (Indexzeilen darunter).

| alter Ort (Anhang A) | Marke | Wort | durch | Art | T |
|---|---|---|---|---|---|
| 15.5, am Absatz zu Lesart A | Z. 1676 | ERGÄNZT | R87 (56.4) | MARKE+ | 1 |
| Abschnitt 27 | Z. 5256 | ERGÄNZT | R91 (57.2) | MARKE+ | 2 |
| 48.14 (R46) | Z. 11059 | ERGÄNZT | R90 (57.1) | MARKE+ | 4 |
| 55.7, Zeile „R78 (55.1) (a), erste“ | Z. 11894 | ERGÄNZT | R88 (56.5) | MARKE+ | 5 |
| 56.1 (R84) | Z. 11927 | ERGÄNZT | R91 (57.2) | MARKE+ | 5 |
| 56.3 (R86) | Z. 11947 | ERGÄNZT | R92 (57.3) | MARKE+ | 5 |
| 56.4 (R87) | Z. 11963 | ERGÄNZT | R90 (57.1) | MARKE+ | 5 |
| 56.5 (R88) | Z. 11973 | PRÄZISIERT | R91 (57.2) | MARKE | 5 |
| 56.7, Zeile „R87 (56.4) (d)“ | Z. 12009 | ERGÄNZT | R90 (57.1) | MARKE+ | 5 |
| 56.7, Zeilen „R84 (56.1) (e), erste“ und „R84 (56.1) (e), zweite“ | Z. 12012 | ERGÄNZT | R91 (57.2) | MARKE+ | 5 |
| 56.7, Zeile „R86 (56.3) (e)“ | Z. 12015 | ERGÄNZT | R92 (57.3) | MARKE+ | 5 |

### Indexzeilen aus Fable 10a

- **48.20 (R52):** Zählung der Fälle „Bestand behauptet statt Voraussetzung genannt“ → R91 (g) (57.2): weiter vierzehn gezählte Fälle bis zur Antwort 10.10.a; aus den zwei Befunden zur Form an der Antwort 09.10.a (56.7, B1 und B2) und aus der Anfrage 10.10.a wird kein Fall gezählt. Ohne Marke (R93 (d), 57.4); die Indexzeilen aus Fable 04a, Fable 07a und Fable 09a bleiben stehen.
- **54.3 (R76):** Massstab der Zählung (R76 (e)) → R91 (g) (57.2): weiter vierzehn gezählte Fälle. Ohne Marke (R93 (d), 57.4). Der Index ist kein Registertext.
- **10, Sperrlistenpunkte 9 und 11:** eine Änderung für die Schranke → R90 (f) (57.1): Wird für die Schranke Code der Sperrliste geändert, ist das eine beauftragte Änderung nach 37.3 (Auftrag, Freigabe des Betreibers, alter und neuer Hash, neues Abbild). Keine Marke (Abschnitt 10; R93 (d), 57.4). Lesart des steuernden Chats, vorläufig: R93 (d) nennt „die Punkte, die Lader und Backtests führen“ ohne Nummer; gemessen steht `backtest` in Abschnitt 10 nur in den Kästen unter Punkt 9, Punkt 11 nennt Simulation und Optimierer, „Lader“ steht in keinem Punkttext; die Quelle von R81 nennt die Punkte 6, 10 und 11. Rückfrage an Fable.

---

## 13. Die Marken aus Fable 14a und 14b (TB-162)

Alle 8 Marken, die TB-162 nach R96 (d) und R97 (e) gesetzt hat (6 am alten Ort, 2 in 58), in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-162/r_daten.json`.

| Ort | Marke | Wort | durch | T |
|---|---|---|---|---|
| Abschnitt 27 | Z. 5259 | ERGÄNZT | R94 (58.1) | 6 |
| Abschnitt 27 | Z. 5262 | ERGÄNZT | R97 (58.4) | 6 |
| 48.13 R45 | Z. 11019 | PRÄZISIERT | R95 (58.2) | 6 |
| 48.13 R45 | Z. 11022 | ERGÄNZT | R97 (58.4) | 6 |
| 48.14 R46 | Z. 11062 | ERGÄNZT | R94 (58.1) | 6 |
| 56.1 R84 | Z. 11930 | PRÄZISIERT | R95 (58.2) | 6 |
| 58.2 R95 | Z. 12143 | BERICHTIGT | R97 (58.4) | 6 |
| 58.3 R96 | Z. 12153 | BERICHTIGT | R97 (58.4) | 6 |

### Indexzeilen aus Fable 14a und 14b

- **48.20 (R52):** Zählung der Fälle „Bestand behauptet statt Voraussetzung genannt“ → R96 (c) (58.3) mit R97 (d) (58.4): fünfzehn gezählte Fälle; der fünfzehnte ist „ein solches Modul schreibt keines“ in R95 (a). In R96 (c) lies „Gezählt sind fünfzehn Fälle.“ Ohne Marke (R96 (d), R97 (e)). Der Index ist kein Registertext.
- **54.3 (R76):** Massstab der Zählung (R76 (e)) → R97 (d) (58.4): fünfzehnter Fall. Ohne Marke (R97 (e)). Der Index ist kein Registertext.
- **Abschnitt 10, Punkt 10:** → R97 (b) (58.4): die ausgeführten Positionen aus der Rückgabe nach R45 mit R84 (e), nachdem Punkt 10 nach 37.3 beauftragt und freigegeben ist; bis dahin Rekonstruktion. Ohne Marke (R97 (e)). Der Index ist kein Registertext.

---

## 14. Die Marken aus Fable 15a (TB-165)

Alle 3 Marken, die TB-165 nach R99 (d) gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-165/r_daten.json`.

| Ort | Marke | Wort | durch | T |
|---|---|---|---|---|
| 56.3 R86 | Z. 11950 | ERGÄNZT | R98 (61.1) | 6 |
| 57.1 R90 | Z. 12051 | ERGÄNZT | R98 (61.1) | 6 |
| 57.2 R91 | Z. 12067 | PRÄZISIERT | R99 (61.2) | 6 |

### Indexzeilen aus Fable 15a

- **„25c (1)“, an jeder Stelle des Registers:** „25c (1)“ ist 42.3 F1 (a), nach R91 (f) → R99 (b) (61.2). Ohne Marke (R99 (b), (d)). Messung je Stelle: 61.3 (b). Der Index ist kein Registertext.
- **Abschnitt 10, Sperrlistenpunkte 9 und 11 (R90 (f)); Punkte 6, 10 und 11 (R81 (b)):** bestätigt durch R99 (c) (61.2), unverändert. Der Index ist kein Registertext.

---

## 15. Die Marken aus Fable 15b und 16b (TB-167)

Alle 6 Marken, die TB-167 nach R100 (a) und R103 (c) gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-167/r_daten.json`.

| Ort | Marke | Kopf | nach | T |
|---|---|---|---|---|
| 5.1 Nr. 4 | Z. 634 | 5.1 Nr. 4 ERGÄNZT durch R103 (62.4) | Fable 16b R103, Unterpunkt (a); die Zeile „4. …“ oben bleibt zeichengleich | 6 |
| 53.7 | Z. 11648 | 53.7 (R72) — ERGÄNZT durch R81 (55.4), Unterpunkt (b), wie 48.7 (R39) nach R89 (d) | Fable 15b R100 (a) | 6 |
| 55.1 | Z. 11802 | 55.1 (R78) — ERGÄNZT durch R83 (55.6), Unterpunkte (e), (f) und (g) | Fable 15b R100 (a) | 6 |
| 55.2 | Z. 11812 | 55.2 (R79) — ERGÄNZT durch R80 (55.3), Unterpunkt (c): die Voraussetzungen aus (a), (b) und (g) sind gemessen erfüllt (TB-140) | Fable 15b R100 (a) | 6 |
| 55.4 | Z. 11841 | 55.4 R81 PRÄZISIERT durch R102 (62.3) | Fable 16b R102, Unterpunkte (a) und (c) | 6 |
| 60.1 | Z. 12264 | 60.1 ERGÄNZT durch R102 (62.3) und R103 (62.4) | Fable 16b R103 (c): R102 Unterpunkte (b) und (c), R103 Unterpunkt (b) | 6 |

---

## 16. Die Marken aus Fable 16c (TB-170)

Alle 5 Marken, die TB-170 nach R104 (c) und R105 (e) gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-170/r_daten.json`.

| Ort | Marke | Kopf | T |
|---|---|---|---|
| 57.1 | Z. 12054 | 57.1 R90 PRÄZISIERT durch R105 (65.2) | 6 |
| 61.1 | Z. 12294 | 61.1 R98 ERGÄNZT durch R105 (65.2) | 6 |
| 62.1 | Z. 12369 | 62.1 R100 ERGÄNZT durch R104 (65.1) | 6 |
| 62.5 (c) | Z. 12433 | 62.5, Absatz (c) ERGÄNZT durch R104 (65.1) | 6 |
| 64.1 | Z. 12515 | 64.1, Absatz „Abnahme nach R98 (d)“ ERGÄNZT durch R105 (65.2) | 6 |

---

## 17. Die Marken aus Fable 17a (TB-173)

Alle 4 Marken, die TB-173 nach R106 (e) gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-173/r_daten.json`.

| Ort | Marke | Kopf | T |
|---|---|---|---|
| 57.1 | Z. 12057 | 57.1 R90 ERGÄNZT durch R106 (66.1) | 6 |
| 61.1 | Z. 12297 | 61.1 R98 ERGÄNZT durch R106 (66.1) | 6 |
| 64.1 | Z. 12518 | 64.1, Absatz „Abnahme nach R98 (d)“ ERGÄNZT durch R106 (66.1) | 6 |
| 65.2 | Z. 12542 | 65.2 R105 PRÄZISIERT und ERGÄNZT durch R106 (66.1) | 6 |

---

## 18. Die Marken aus Fable 17b (TB-175)

Alle 9 Marken, die TB-175 nach R107 (f) gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-175/r_daten.json`.

| Ort | Marke | Kopf | T |
|---|---|---|---|
| 16.4 | Z. 2259 | 16.4 ERGÄNZT durch R107 (67.1) | 6 |
| 16.8 | Z. 2478 | 16.8 ERGÄNZT durch R107 (67.1) | 6 |
| 55.4 | Z. 11844 | 55.4 R81 ERGÄNZT durch R107 (67.1) | 6 |
| 56.3 | Z. 11953 | 56.3 R86 ERGÄNZT durch R107 (67.1) | 6 |
| 57.3 | Z. 12077 | 57.3 R92 ERGÄNZT durch R107 (67.1) | 6 |
| 58.4 | Z. 12163 | 58.4 R97 ERGÄNZT durch R107 (67.1) | 6 |
| 62.3 | Z. 12389 | 62.3 R102 ERGÄNZT und BERICHTIGT durch R107 (67.1) | 6 |
| 64.1 | Z. 12521 | 64.1, Absatz „Abnahme nach R98 (d)“ ERGÄNZT durch R107 (67.1) | 6 |
| 66.1 | Z. 12606 | 66.1 R106 ERGÄNZT durch R107 (67.1) | 6 |

### Indexzeilen aus Fable 17b

- **48.20 (R52):** Zählung → R107 (a) (67.1): sechzehnter Fall („Aussage über das Repo ohne Kennzeichnung, die nicht trifft (R76 (e))“); sechzehn Fälle (R107 (f)). Ohne Marke (R107 (f)). Der Index ist kein Registertext.
- **54.3 (R76):** Massstab der Zählung (R76 (e)) → R107 (a) (67.1): sechzehnter Fall. Ohne Marke (R107 (f)). Der Index ist kein Registertext.

---

## 19. Die Marken aus Fable 17c (TB-176a)

Alle 9 Marken, die TB-176a nach R108 (f) im Register gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-176a/r_daten.json`.

| Ort | Marke | Kopf | T |
|---|---|---|---|
| 16.4 | Z. 2262 | 16.4 ERGÄNZT durch R108 (68.1) | 6 |
| 16.6 | Z. 2374 | 16.6 ERGÄNZT durch R108 (68.1) | 6 |
| 16.8 | Z. 2481 | 16.8 ERGÄNZT durch R108 (68.1) | 6 |
| 29.3 | Z. 5459 | 29.3 ERGÄNZT durch R108 (68.1) | 6 |
| 37.5 | Z. 7301 | 37.5 ERGÄNZT durch R108 (68.1) | 6 |
| 41.3 C2 | Z. 8964 | 41.3 C2 ERGÄNZT durch R108 (68.1) | 6 |
| 62.2 | Z. 12379 | 62.2 R101 ERGÄNZT und BERICHTIGT durch R108 (68.1) | 6 |
| 66.1 | Z. 12609 | 66.1 R106 ERGÄNZT durch R108 (68.1) | 6 |
| 67.1 | Z. 12684 | 67.1 R107 ERGÄNZT durch R108 (68.1) | 6 |

Dazu in `docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md`: Marke an 10a.2 (Z. 606, „S-B1 10a.2 ERGÄNZT durch 10a.5“) und der datierte Nachtrag 10a.5 (Z. 639), R108 (a). Der Index ist kein Registertext.

---

## 20. Die Marken aus Fable 17d und 17e (TB-178)

Alle 10 Marken, die TB-178 nach R109 (c) und R110 (d) im Register gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-178/r_daten.json`.

| Ort | Marke | Kopf | T |
|---|---|---|---|
| 29.3 | Z. 5462 | 29.3 ERGÄNZT durch R109 (69.1) | 2 |
| 29.3 | Z. 5465 | 29.3 ERGÄNZT durch R110 (70.1) | 2 |
| 37.2 | Z. 7047 | 37.2 ERGÄNZT durch R110 (70.1) | 3 |
| 37.5 | Z. 7304 | 37.5 ERGÄNZT durch R110 (70.1) | 3 |
| 38.5 | Z. 7573 | 38.5 ERGÄNZT durch R110 (70.1) | 3 |
| 66.1 | Z. 12612 | 66.1 R106 BERICHTIGT durch R109 (69.1) | 6 |
| 66.1 | Z. 12615 | 66.1 R106 ERGÄNZT durch R110 (70.1) | 6 |
| 67.1 | Z. 12687 | 67.1 R107 ERGÄNZT durch R109 (69.1) | 6 |
| 68.1 | Z. 12756 | 68.1 R108 BERICHTIGT und ERGÄNZT durch R109 (69.1) | 6 |
| 69.1 | Z. 12829 | 69.1 R109 BERICHTIGT und ERGÄNZT durch R110 (70.1) | 6 |

Der Index ist kein Registertext.









**Pflege:** Nach jedem Registerauftrag zusammen mit `registerkopie.py` erneuern. Die Marken misst das Skript neu,
die Ketten liest die Sitzung aus seiner Ausgabe. Die Teil-Nummern in der Spalte T stammen aus demselben Zuschnitt
wie die Kopie. Wird ein Teil neu geschnitten, ändern sie sich mit.
In TB-126 (01.10.2026): Zeilenangaben mit `docs/belege/TB-126/c2_index_zeilen.py` vom Stand
`0f56aeb` auf `db108a6` umgeschrieben (Abbildung über die unveränderten alten Zeilen); neuer Zuschnitt verschiebt
23 nach T2, 37 nach T3, 43 nach T4; Einträge mit `c2_index_eintraege.py`.
In TB-129 (02.10.2026): Zeilenangaben mit `docs/belege/TB-129/c2_index_zeilen.py` vom Stand
`db108a6` auf `f63ad4c` umgeschrieben (jede Zahl in Listen und Bereichen); Zuschnitt der Teile unverändert, 51 kommt
zu T4; Abschnittstabelle aus den Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-129/c2_index_eintraege.py`.
In TB-130 (02.10.2026): Zeilenangaben mit `docs/belege/TB-130/c2_index_zeilen.py` vom Stand
`f63ad4c` auf `ad351d5` umgeschrieben (jede Zahl in Listen und Bereichen); 52 kommt zu T4; Abschnittstabelle aus den
Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-130/c2_index_eintraege.py`; in Abschnitt 6 die fünf
Indexzeilen ohne Marke auf die in TB-130 gesetzten Marken umgestellt (`c3_indexzeilen.py`).
In TB-132 (04.10.2026): Zeilenangaben mit `docs/belege/TB-132/c2_index_zeilen.py` vom Stand
`ad351d5` auf `ee43f5f` umgeschrieben (jede Zahl in Listen und Bereichen); 53 kommt zu T4; Abschnittstabelle aus den
Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-132/c2_index_eintraege.py`; neuer Abschnitt 8 mit den
21 Marken und den drei Indexzeilen nach R70 (b) (`c3_indexzeilen.py`).
In TB-136 (05.10.2026): Zeilenangaben mit `docs/belege/TB-136/c2_index_zeilen.py` vom Stand
`ee43f5f` auf `9b7b060` umgeschrieben (jede Zahl in Listen und Bereichen); 54 kommt zu T5; Abschnittstabelle aus den
Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-136/c2_index_eintraege.py`; neuer Abschnitt 9 mit den
15 Marken und zwei Indexzeilen nach R77 (b) und (c) (`c3_indexzeilen.py`).
In TB-139 (07.10.2026): Zeilenangaben mit `docs/belege/TB-139/c2_index_zeilen.py` vom Stand
`9b7b060` auf `ad1fc0d` umgeschrieben (jede Zahl in Listen und Bereichen); 55 kommt zu T5; Abschnittstabelle aus den
Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-139/c2_index_eintraege.py`; neuer Abschnitt 10 mit den
20 Marken und drei Indexzeilen nach R80 (b) (`c3_indexzeilen.py`).
In TB-149 (10.10.2026): Zeilenangaben mit `docs/belege/TB-149/c2_index_zeilen.py` vom Stand
`ad1fc0d` auf `d950e03` umgeschrieben (jede Zahl in Listen und Bereichen); 56 kommt zu T5; Abschnittstabelle aus den
Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-149/c2_index_eintraege.py`; neuer Abschnitt 11 mit den
31 Marken und drei Indexzeilen nach R89 (h) (`c3_indexzeilen.py`).
In TB-154 (11.10.2026): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py` vom Stand
`d950e03` auf `3f2e97e` umgeschrieben (jede Zahl in Listen und Bereichen); 57 kommt zu T5; Abschnittstabelle aus den
Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-154/c2_index_eintraege.py`; neuer Abschnitt 12 mit den
11 Marken und drei Indexzeilen nach R93 (d) (`c3_indexzeilen.py`).
In TB-162 (15.10.2026): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py 9a1bc7a 0e1e662`; Einträge mit dem Werkzeug aus Anhang B des Auftrags TB-162 (`index`); 58 (R94–R97) kommt zu T6; neuer Abschnitt 13 (8 Marken).
In TB-163 (15.10.2026): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py cff0de3 35dae90`; Einträge mit dem Werkzeug aus Anhang B des Auftrags TB-163 (`index`); 59 (Tatsachennotiz TB-162) kommt zu T6.
In TB-164 (15.10.2026): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py 1d037f9 92cb637`; Einträge mit dem Werkzeug aus Anhang B des Auftrags TB-164 (`index`); 60 (Vollzug TB-163, Posten 5) kommt zu T6.
In TB-165 (15.10.2026): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py 4edd877 173368f`; Einträge mit dem Werkzeug aus Anhang B des Auftrags TB-165 (`index`); 61 (R98–R99) kommt zu T6; neuer Abschnitt 14 (3 Marken).
In TB-167 (16.10.2026): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py bc5e165 4370857`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-167 (`index`); 62 (R100–R103) kommt zu T6; neuer Abschnitt 15 (6 Marken).
In TB-168 (16.10.2026): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py a2768a1 02f19f5`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-168 (`index`); 63 (Vollzug TB-167) kommt zu T6.
In TB-169 (16.10.2026): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py 69539db 3cbcdee`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-169 (`index`); 64 (Vollzug TB-166) kommt zu T6.
In TB-170 (17.10.2026): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py 801a055 7aecfe6`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-170 (`index`); 65 (R104–R105) kommt zu T6; neuer Abschnitt 16 (5 Marken). Der Kopf mischt weiter Stände (BACKLOG Rang 1, TB-170).
In TB-173 (17.10.2026): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py f79f239 7fe6342`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-173 (`index`); 66 (R106) kommt zu T6; neuer Abschnitt 17 (4 Marken). Der Kopf mischt weiter Stände (BACKLOG Rang 1, TB-170).
In TB-175 (17.10.2026): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py b470dc4 3a00cf8`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-175 (`index`); 67 (R107) kommt zu T6; neuer Abschnitt 18 (9 Marken, Indexzeilen 48.20 und 54.3).
In TB-176a (17.10.2026): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py 17648ad 53e8d54`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-176a (`index`); 68 (R108) kommt zu T6; neuer Abschnitt 19 (9 Marken, S-B1 10a.2/10a.5).
In TB-178 (17.10.2026): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py 14833dd 47f184b`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-178 (`index`); 69 (R109) kommt zu T6, 70 (R110) zu T6; neuer Abschnitt 20 (10 Marken).
Zuletzt nachgezogen in TB-180 (17.10.2026): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py ebee3ef fd8f277`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-180 (`index`); 71 kommt zu T6; Nachtrag zu Punkt 9 (Abschnitt 10) und Marke an 29.3 (71.3).

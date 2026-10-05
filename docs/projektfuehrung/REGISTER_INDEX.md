# REGISTER_INDEX — wo was im Register gerade gilt

**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `9b7b060` (05.10.2026), Abschnitte 0–54,
11 581 Zeilen, sha256 `8d505a38…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4), nachgezogen in TB-126 (E-2), TB-129 (Fable 01a), TB-130 (Fable 02a), TB-132 (Fable 02c) und TB-136 (Fable 04a). **Das ist ein Wegweiser, nicht das
Register.** Der Wortlaut steht nur im Register bzw. in der Kopie je Abschnitt `register_kopie/REGISTER_KOPIE_ABSCHNITT_00.md` … `_54.md` (Tabelle unten; dazu die Teile `REGISTER_KOPIE_teil1–5.md`).

**Wie gemessen:** `python3 docs/werkzeuge/registerkopie.py --marken` sammelt jede Zeile mit „ERSETZT durch“ oder
„PRÄZISIERT durch“ (das Suchmuster des Auftrags, Art `MARKE`, 95 Zeilen), jede weitere Zeile mit ERSETZT,
PRÄZISIERT, BERICHTIGT, ERGÄNZT oder KORRIGIERT (Art `MARKE+`, 128 Zeilen) und jede Überschrift mit Rückverweis
(„Berichtigung zu“, „Präzisierung zu“, „Ergänzung zu“, „ersetzt die …“; Art `UEBERSCHRIFT`, 91 Zeilen). Die
Ausgabe liegt in `docs/belege/TB-136/c1_marken.txt` (zuvor `docs/belege/TB-132/c1_marken.txt`, `docs/belege/TB-130/c1_marken.txt`, `docs/belege/TB-129/c1_marken.txt`, `docs/belege/TB-126/c1_marken.txt`, `docs/belege/TB-118/a4_marken.txt`). Die Ketten unten sind **aus diesen Zeilen gelesen, nicht
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
| 5 | `REGISTER_KOPIE_ABSCHNITT_05.md` | 588–743 |
| 6 | `REGISTER_KOPIE_ABSCHNITT_06.md` | 744–798 |
| 7 | `REGISTER_KOPIE_ABSCHNITT_07.md` | 799–869 |
| 8 | `REGISTER_KOPIE_ABSCHNITT_08.md` | 870–924 |
| 9 | `REGISTER_KOPIE_ABSCHNITT_09.md` | 925–964 |
| 10 | `REGISTER_KOPIE_ABSCHNITT_10.md` | 965–1171 |
| 11 | `REGISTER_KOPIE_ABSCHNITT_11.md` | 1172–1254 |
| 12 | `REGISTER_KOPIE_ABSCHNITT_12.md` | 1255–1331 |
| 13 | `REGISTER_KOPIE_ABSCHNITT_13.md` | 1332–1347 |
| 14 | `REGISTER_KOPIE_ABSCHNITT_14.md` | 1348–1362 |
| 15 | `REGISTER_KOPIE_ABSCHNITT_15.md` | 1363–1819 |
| 16 | `REGISTER_KOPIE_ABSCHNITT_16.md` | 1820–2577 |
| 17 | `REGISTER_KOPIE_ABSCHNITT_17.md` | 2578–3034 |
| 18 | `REGISTER_KOPIE_ABSCHNITT_18.md` | 3035–3099 |
| 19 | `REGISTER_KOPIE_ABSCHNITT_19.md` | 3100–3214 |
| 20 | `REGISTER_KOPIE_ABSCHNITT_20.md` | 3215–3295 |
| 21 | `REGISTER_KOPIE_ABSCHNITT_21.md` | 3296–3647 |
| 22 | `REGISTER_KOPIE_ABSCHNITT_22.md` | 3648–3854 |
| 23 | `REGISTER_KOPIE_ABSCHNITT_23.md` | 3855–4245 |
| 24 | `REGISTER_KOPIE_ABSCHNITT_24.md` | 4246–4590 |
| 25 | `REGISTER_KOPIE_ABSCHNITT_25.md` | 4591–4820 |
| 26 | `REGISTER_KOPIE_ABSCHNITT_26.md` | 4821–5144 |
| 27 | `REGISTER_KOPIE_ABSCHNITT_27.md` | 5145–5224 |
| 28 | `REGISTER_KOPIE_ABSCHNITT_28.md` | 5225–5365 |
| 29 | `REGISTER_KOPIE_ABSCHNITT_29.md` | 5366–5448 |
| 30 | `REGISTER_KOPIE_ABSCHNITT_30.md` | 5449–5582 |
| 31 | `REGISTER_KOPIE_ABSCHNITT_31.md` | 5583–5714 |
| 32 | `REGISTER_KOPIE_ABSCHNITT_32.md` | 5715–5925 |
| 33 | `REGISTER_KOPIE_ABSCHNITT_33.md` | 5926–6137 |
| 34 | `REGISTER_KOPIE_ABSCHNITT_34.md` | 6138–6348 |
| 35 | `REGISTER_KOPIE_ABSCHNITT_35.md` | 6349–6545 |
| 36 | `REGISTER_KOPIE_ABSCHNITT_36.md` | 6546–6896 |
| 37 | `REGISTER_KOPIE_ABSCHNITT_37.md` | 6897–7261 |
| 38 | `REGISTER_KOPIE_ABSCHNITT_38.md` | 7262–7637 |
| 39 | `REGISTER_KOPIE_ABSCHNITT_39.md` | 7638–8158 |
| 40 | `REGISTER_KOPIE_ABSCHNITT_40.md` | 8159–8553 |
| 41 | `REGISTER_KOPIE_ABSCHNITT_41.md` | 8554–8971 |
| 42 | `REGISTER_KOPIE_ABSCHNITT_42.md` | 8972–9537 |
| 43 | `REGISTER_KOPIE_ABSCHNITT_43.md` | 9538–9854 |
| 44 | `REGISTER_KOPIE_ABSCHNITT_44.md` | 9855–10161 |
| 45 | `REGISTER_KOPIE_ABSCHNITT_45.md` | 10162–10385 |
| 46 | `REGISTER_KOPIE_ABSCHNITT_46.md` | 10386–10670 |
| 47 | `REGISTER_KOPIE_ABSCHNITT_47.md` | 10671–10790 |
| 48 | `REGISTER_KOPIE_ABSCHNITT_48.md` | 10791–10998 |
| 49 | `REGISTER_KOPIE_ABSCHNITT_49.md` | 10999–11029 |
| 50 | `REGISTER_KOPIE_ABSCHNITT_50.md` | 11030–11218 |
| 51 | `REGISTER_KOPIE_ABSCHNITT_51.md` | 11219–11328 |
| 52 | `REGISTER_KOPIE_ABSCHNITT_52.md` | 11329–11407 |
| 53 | `REGISTER_KOPIE_ABSCHNITT_53.md` | 11408–11517 |
| 54 | `REGISTER_KOPIE_ABSCHNITT_54.md` | 11518–11581 |

*Frühere Vierteilung* (bis 01.10.2026; „T1“ … „T4“ in den Tabellen unten bezeichnen sie, massgeblich sind Abschnitt und Z.): T1 = 0–22 (Z. 1–3854), T2 = 23–36 (Z. 3855–6896), T3 = 37–42 (Z. 6897–9537), T4 = 43–53 (Z. 9538–11517), T5 = 54–54 (Z. 11518–11581).

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
| 5.1 „Die Regeln“ | Z. 592 ERSETZT durch Abschnitt 15, Registertext 0, 2 und 4; Nr. 7: Z. 646 **PRÄZISIERT durch R37 (48.5)** | 15.2, 15.4, 15.6 → weiter nach Tabelle 3; Nr. 7 **mit** 48.5 R37 (T4) |
| 5.3 „Krypto: Platzhalter mit Regel“ | Z. 675 ERSETZT durch Abschnitt 15, Registertext 3 und 4; Z. 700 ERGÄNZT (Verweis) durch R51 (48.19) | 15.5, 15.6 → weiter nach Tabelle 3; dazu 48.19 R51 (T4) |
| 7, Tabelle (a), (b) und (d) | Z. 810 (d) **PRÄZISIERT durch R48 (48.16)**; Z. 813 (a) ERGÄNZT (Verweis) durch R51 (48.19); Z. 816 (d) ERGÄNZT durch R55 (49.3); Z. 819 (b) **PRÄZISIERT durch R37 (48.5)** | 7 (d) **mit** 48.16 R48 (c); 7 (b) **mit** 48.5 R37; dazu 49.3 R55 (leere Menge), 48.19 R51 (T4) |
| 7.1 Die drei Regeln … | Z. 862 ERGÄNZT durch R21 (47.4); Z. 865 **PRÄZISIERT durch R23 (47.6)** | 7.1 **mit** 47.6 R23; dazu 47.4 R21 (T4) |
| 8, Tabelle (Bericht je Bot) | Z. 890 **PRÄZISIERT durch R36 (48.4)**; Z. 893 ERGÄNZT durch R55 (49.3) | 8, Tabelle **mit** 48.4 R36; dazu 49.3 R55 (T4) |
| 8.1 Zufalls-Timing-Test | Z. 920 **PRÄZISIERT durch R48 (48.16)** | 8.1 **mit** 48.16 R48 (g); R48 (g) BERICHTIGT durch 49.2 R54 (Z. 10946) (T4) |
| 9, erster Absatz („N = 653 plus …“) | Z. 932 **PRÄZISIERT durch R48 (48.16)** (einzige Marke in 9) | 9 **mit** 48.16 R48 (b) (T4) |
| 10 Sperrliste | Z. 1025 (MARKE+: der Kasten an Punkt 4 sagt „nicht (iii) (ERSETZT-Marke)“, Form (ii) nach 38.4) | 10, Punkttext unverändert; Vollzug Punkt 4 in 39.2 (T3). Die Sperrlisten-Einträge 36.1, 36.6, 37.2 und 37.3 gehen in Tabelle 4 |
| ↳ 10, künftiger Punkt 15 (die neun neuen Trade-Listen) | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 48.10 R42 (T4) |
| ↳ 10, Sperrlistenpunkt 10 (Zuteilungskaskade, `shared/zuteilung.py`) | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 48.13 R45 (T4) |
| ↳ 10.1, „Stichproben-Hash-Vergleich“ | **Indexzeile E-2**, keine Marke (Abschnitt 10) | lies „Hash-Vergleich aller Ausgabedateien …“: 48.16 R48 (k) (T4) |
| ↳ 10, „Fortschreibung derselben Tatsache (15.09.2026, nach dem Lauf)“ | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 48.17 R49 (g); R51: 48.19 (T4) |
| ↳ 10, Sperrlistenpunkt 14 („Die Reihenfolge Selektion → Bestätigungsperiode → Bericht“) | **Indexzeile E-2**, keine Marke (Abschnitt 10) | 47.13 R30 (T4) |
| 11, 11.2, 11.3 | Z. 1228 (11.2) ERGÄNZT durch R43 (48.11); Z. 1247 (11) ERGÄNZT durch R49 (48.17); Z. 1250 (11.3) ERGÄNZT durch 50.3 und 50.4 | am Ort; dazu 48.11 R43, 48.17 R49 (h), Vollzug Posten 3 in 50.3/50.4 (T4) |
| 12 Vollständigkeitstest | Z. 1318, 1321, 1324, 1327 ERGÄNZT durch R25 (47.8), R26 (47.9), R49 (48.17), R50 (48.18) | 12. **Dazu:** 40.7 Ergänzung (T3), 41.1 A1 Berichtigung „sieben Mutationsproben“ (T3), 46.5 R14 Ergänzung (T4), 47.8 R25, 47.9 R26, 48.17 R49 (d), 48.18 R50 (T4) |
| alle übrigen (0, 6, 13, 14 und die oben nicht genannten Unterabschnitte von 2, 4, 7–9) | – | am Ort, T1 |

## 3. Registertexte 0–7 und die Registertexte ohne Nummer (Abschnitte 15–17, T1)

| Registertext | Ersteintrag | Marken der Kette (Zeile) | **gilt** | dazu (Überschrift oder anderes Markenwort) |
|---|---|---|---|---|
| **0** Verfahren | 15.2 | – | **15.2** (T1) | – |
| **1a** Bootstrap (a) | 15.3 (a) | Z. 1449 **PRÄZISIERT durch R66 (53.1)** | **15.3 (a)** **mit** 53.1 R66 (a), (b) (T4) | 24.2 beruft sich auf 1a; Z. 4250 „Registertext 1a bleibt in 15.3“; 15.3 insgesamt: Z. 1473 ERGÄNZT durch R35 (48.3) (T4) |
| **1b** | 15.3 (b) | – | **15.3 (b)** | Z. 1446 ERGÄNZT durch R41 (48.9) (T4) |
| **1c** | 15.3 (c) | Z. 1452 **PRÄZISIERT durch R66 (53.1)** | **15.3 (c)** **mit** 53.1 R66 (c) (T4) | – |
| **2a–2c** Faltenzuordnung | 15.4 (a)–(c) | – | **15.4 (a)–(c)** | 2a: Z. 1501 **BERICHTIGT durch R54 (49.2)** („lies“); 15.4 insgesamt: Z. 1546 ERGÄNZT durch R41 (48.9) und 50.1 (T4) |
| **2d** Embargo | 15.4 (d) | Z. 1496 ERSETZT durch 16.6 → Z. 2347 PRÄZISIERT durch R37 (48.5) → Z. 2350 **PRÄZISIERT durch R75 (54.2)** | **16.6** (T1) **mit** 48.5 R37 (T4) und 54.2 R75 (a) (T5) | 41.2 B2 „Berichtigung der 2d-Herleitung“ (T3) |
| **3a** Universum | 15.5 (a) | Tabelle darunter: Z. 1583 KORRIGIERT in 16.1.3 (MARKE+) | **15.5 (a)**, Rechenweg der Krypto-Zeile **16.1.3** | 15.5 insgesamt: Z. 1661 ERGÄNZT durch R53 (49.1) (T4) |
| **3b** Symbolzahl je Falte | 15.5 (b) | Tatsachennotizen: Z. 1606 ERSETZT durch 16.1.1, Z. 1623 ERSETZT durch 16.1.2 | Regel **15.5 (b)**, Tatsachen **16.1.1/16.1.2** | Ergänzungen 3b (a)–(e) in **16.7** (siehe nächste Zeilen) |
| **3b (a)** Ergänzung | 16.7 (a) | – | **16.7 (a)** | – |
| **3b (b)** Ergänzung | 16.7 (b) | – | **16.7 (b)** | 34.3 berichtigt in 30.2 (2) „3b (b)“ zu „3b (a)“ (T2) |
| **3b (c)** Benchmark | 16.7 (c) | Z. 2396 (c) ERSETZT durch 23.3 | **23.3** (T2) | 24.2 bezieht sich auf 3b (c) „in der Fassung aus 23.3“ |
| **3b (d), (e)** | 16.7 (d), (e) | – | **16.7 (d), (e)** | (d): Z. 2414 ERGÄNZT durch R38 (48.6) (T4) |
| **3c** Vorbehalt | 15.5 (c) | – | **15.5 (c)** | Z. 1570 ERGÄNZT durch 26.4 (T2) |
| **3d** | 15.5 (d) | – | **15.5 (d)** | – |
| **4** Falten, insgesamt | 15.6 | – | 15.6 | 21 „Berichtigung zu Registertext 4“ (15.6, Punkt 2 der Tafel, T1); 24.2 „Präzisierung zu Registertext 4“ (Drawdown Mark-to-Market, **ohne Marke in 15.6**, T2); Z. 1741 ERGÄNZT (Verweis) durch R51 (48.19) (T4) |
| **4a** erste Falte | 15.6 (a) | Z. 1673 (a) ERSETZT durch 25.3 → Z. 4697 (i) PRÄZISIERT durch 26.2 | **25.3**, Bedingung (i) in der Fassung **26.2** (T2) | 21.3 (b) ging ebenfalls in 25.3 auf (Z. 3383). 28.6 „Registertext 4a, Präzisierung, Ergänzung“ → 30.6 „Präzisierung zu 28.6“; 32 „Bedingung (i) rechnet gegen den Horizontbeginn aus 28.4“; 33.2 „Der Faltenplan nach 4a“ (alle T2). **Mehrdeutig, ob 28.6 und 30.6 den Wortlaut von 25.3 fortschreiben oder daneben stehen, Abschnitte 25, 26, 28, 30** |
| **4b, 4c** | 15.6 (b), (c) | (c): Z. 1691 **PRÄZISIERT durch R23 (47.6)** | **15.6 (b), (c)**, (c) **mit** 47.6 R23 (T4) | – |
| **4d** Faltenliste | 15.6 (d) | – | Regel **15.6 (d)** | Tatsachennotizen: 21.4 (berichtigte Faltenliste, T1), 26.3 (Platzhalter) **ERSETZT** durch 28.4 (MARKE+ Z. 5274); Faltenplan als Registertext 33.2 (T2) |
| **5** Datenstand | 15.7 | Z. 1764 ERSETZT durch 16.3 | **16.3**, nach Punkten wie folgt | 18 Tatsachennotiz zu 5/5a (T1) |
| **5a** Bestand und Snapshot | 16.3 (a) | Z. 2007 ERSETZT durch 17.1 | **17.1** (T1) | 17.3 Zusatz `rand_erste`; 28.2 Ergänzung `asof` → 31 „Berichtigung zu 28.2“, Ersatztext **31.2**; 31.3 „Präzisierung zu 5a / 17.1“ (T2); 41.2 B5 Resolver-Pflicht, Ergänzung zu 5a/5e (T3) |
| **5b** Registerhash | 16.3 (b) | Z. 2021 PRÄZISIERT durch 17.9 | **16.3 (b) mit 17.9** (T1) | – |
| **5c** Reihenfolge Snapshot/Tag | 16.3 (c) | Z. 2032 ERSETZT durch 17.2 | **17.2** (T1) | – |
| **5d** UTC | 16.3 (d) | – | **16.3 (d)** | – |
| **5e** Lese-Audit | 17.4 | – | **17.4** (T1) | 19 Ergänzung Codeherkunft (T1) → 45.4 R4 „Ergänzung zu 19“ (T4); 41.2 B5 (T3) |
| **5f** Umgebung | 17.5 | – | **17.5** (T1) | 20 Tatsachennotiz Lock (T1); Z. 2845 ERGÄNZT durch R74 (54.1): Name des Handelskalenders (T5) |
| **6** Budgetstufen (a)–(m) | 16.4 | Z. 2103–2198: 18 Marken, davon 14 **PRÄZISIERT** durch R18–R23 (47.1–47.6) und R37 (48.5) — Liste in Abschnitt 5; „Prüfung vor dem Tag“: Z. 2241 **PRÄZISIERT durch R21 (47.4)** — Abschnitt 6 | **16.4** (T1) **mit** 47.1–47.6 und 48.5 für (a)–(d), (h)–(m); „Prüfung vor dem Tag“ **mit** 47.4 R21 (T4) | 47.3 R20 Ergänzung zu (j), (l); 47.7 R24 Tatsachennotiz zu (g), (h) mit 50.6 (T4); 22.4 „Registertext 6, Ergänzung — Notbremse“ (T1); 26.7 Kette „(b) → Festlegung 11 → Registertext 6 (b)“ (T2) |
| **7** Backtester-Prüfung | 16.5 | – | **16.5** (T1) | Z. 2289 ERGÄNZT durch 17.6, 17.7, 17.8 (Ergänzungen I–III, T1) |
| Kandidatenregeln (a)–(e) | 16.8 | – | **16.8** (T1) | – |
| Vorab-Filter (a)–(c) | 16.9 | – | **16.9** (T1) | – |
| short-fähige Sleeves (a)–(e) | 16.10 | – | **16.10** (T1) | – |

## 4. Registertexte ab Abschnitt 18

Ab Abschnitt 22 heissen Registertexte nach ihrem Unterabschnitt, ab 41 nach ihrem Eintrag (A1 …, R1 …). Für jeden
Registertext ab Abschnitt 38 gilt 38.2: Fundstellen im Code werden als Datei und Bezeichner angegeben.
Die Spalte „später berührt“ nennt jede gemessene Marke und jede Rückverweis-Überschrift, die auf den Abschnitt zeigt.

| Abschnitt | T | Registertexte / Einträge darin | später berührt (Marke oder Überschrift) |
|---|---|---|---|
| 18 Tatsachennotiz 5/5a, Snapshot | 1 | Tatsachennotiz | Z. 3095 ERGÄNZT durch R28 (47.11) (T4) |
| ↳ 17.3, 17.9, 18 — Datenstand-Hash voll | 1 | **Indexzeile E-2**, keine Marke (R51 verlangt Indexzeile) | 48.19 R51 (T4) |
| 19 Codeherkunft (5e) | 1 | Ergänzung zu 5e | 45.4 R4 Ergänzung zu 19 (T4) |
| 20 Lock (5f) | 1 | Tatsachennotiz | – |
| 21 Faltenschranke | 1 | 21.3 Ersatztext (a)–(c); 21.4 Tatsachennotiz zu 4d; 21.9 Entscheidung zu 21.6 | 21.3 (b) **ERSETZT durch 25.3** (Z. 3383); 36.4 Tatsachennotiz zu 21.4; 38.3 Tatsachennotiz zu 21.9; 21.4: Z. 3437 ERGÄNZT durch R53 (49.1) (T4) |
| 22 Methodenantwort 19.09. | 1 | 22.1 allgemeine Prüfregel; 22.2 Kill-Test-Berichtswerte; 22.3 Abschalt- und Zuschaltregeln; 22.4 Ergänzung zu RT 6 | 22.2: Z. 3712 ERGÄNZT durch R34 (48.2) (T4) |
| 23 Benchmark tagesgenau | 2 | 23.3 Ersatztext zu 3b (c) | in 23.3 selbst: Z. 4000 „ERSETZT (TB-71) durch den Satz zur Zeitachse oben“ (eine Tabelle in 23.3 durch einen Satz in 23.3); 23.3, Registertext 3b (c) **PRÄZISIERT durch R72 (53.7)** (Z. 3953, vom steuernden Chat nach R65 (a) bestimmt, T4); 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse **BERICHTIGT durch R71 (53.6)** (Z. 3981), ERGÄNZT durch R72 (53.7) (Z. 3984) (T4) |
| 24 Mark-to-Market | 2 | 24.2 Präzisierung zu RT 4; 24.3 Entscheidungsregel; 24.4 Festlegung 1 | 24.6 Tatsachennotiz; 24.2 **PRÄZISIERT durch R36 (48.4)** (Z. 4338, T4) |
| 25 erste Falte, Konjunktion | 2 | 25.3 Ersatztext zu 4a und 21.3 (b) | (i) **PRÄZISIERT durch 26.2** (Z. 4697) und **durch R53 (49.1)** (Z. 4699); 25.2: Z. 4679 ERGÄNZT durch R53 (T4); 25.3 (i) ERGÄNZT durch R58 (51.3) (Z. 4702, T4); 25.2 **BERICHTIGT durch R62 (51.7) und R65 (52.3)** (Z. 4676, T4) |
| 26 Datenhorizont je Bot | 2 | 26.2 Präzisierung zu 4a (i); 26.4 Ergänzung zu 3 (c); 26.7 Grenzfall | 26.3 (Platzhalter-Tabelle) **ERSETZT** durch 28.4; 26.6 Zeilen 1 und 4 **ERSETZT** durch 28.5, Zeile 2 dort „erledigt“ (MARKE+); 28 „Berichtigung zu 26.3 und 26.6“; 31.6 berichtigt eine Zahl aus 26 |
| 27 Sichtschutz | 2 | 27.1–27.5 | 45.6 R6 Ergänzung zu 27 (T4); 27.3: Z. 5175 ERGÄNZT durch R31 (47.14); Z. 5214 ERGÄNZT durch R32 (47.15) (T4); Z. 5217 ERGÄNZT durch R56 (51.1) (T4); Z. 5220 ERGÄNZT durch R73 (53.8) (T4) |
| 28 `asof` gesetzt | 2 | 28.2 Ergänzung zu 5a; 28.4, 28.5 Ersatzmarken; 28.6 Präzisierung und Ergänzung zu 4a | 28.2 → 31 Berichtigung, Ersatztext **31.2**; 28.6 → 30.6 Präzisierung; 32 rechnet gegen den Horizontbeginn aus 28.4 (Überschrift 32); 28.6 **PRÄZISIERT durch R53 (49.1)** (Z. 5352, T4) |
| 29 Kapitalpfad ab erster Falte | 2 | 29.3 Registertext | 29.2 → 30.7 Ergänzung; 29.4 → 34.5 Berichtigung; in 29.4: „Fassung aus 21b ist ERSETZT“ (Z. 5419); 29.4 BERICHTIGT durch R43 (48.11) (Z. 5434, T4) |
| 30 gesperrter Faltenplan | 2 | 30.2 Registertext (1)–(3); 30.3 Tatsachennotiz Punkt 2 | 30.2 (2) → 34.3 Berichtigung; 30.2 (3) → 33.1 Berichtigung, 35.4 Präzisierung, 45.3 R3 Ergänzung (T4). **Mehrdeutig, welche Fassung von 30.2 (3) gilt, Abschnitte 33, 35, 45** |
| 31 kein Feld `asof` | 2 | 31.2 Ersatztext zu 28.2; 31.3 Präzisierung zu 5a/17.1 | – |
| 32 Horizontbeginn | 2 | Tatsachennotizen, 32.5 Entscheidungsvorlage | – |
| 33 Faltenplan als Registertext | 2 | 33.2 Registertext; 33.3 Feldliste; 33.4 Anpassungen | 33.2 → 34.1, 34.2, 35.1 Ergänzungen (35.1 → **38.1 Berichtigung**, T3); 33.3 → 34.4, 35.2 Ergänzungen, 42.1 D5 Präzisierung (→ 42.2 E3 BERICHTIGT), 45.3 R3; 33.4 Punkt 3 **ERSETZT** (35.3; MARKE+ Z. 6111), 34.6 Berichtigung. **33.2 und 33.3 sind mehrdeutig: Grundtext plus Ergänzungen in 34, 35, 38, 42 und 45** |
| 34 Faltenregeln, Feld `horizontbeginn` | 2 | 34.1–34.6 | 34.5 BERICHTIGT durch R43 (48.11) (Z. 6285, T4) |
| 35 Bestätigungsperiode | 2 | 35.1–35.4 | 35.1 → 38.1 Berichtigung (T3); 35.4 → 42.1 D5 (T3); 35.1 **PRÄZISIERT durch R37 (48.5)** (Z. 6443); 35.4 ERGÄNZT durch R26 (47.9) (Z. 6523) (T4) |
| 36 Schreibregel, Sonde, Abbild | 2 | 36.1 Schreibregel; 36.2 Sonde; 36.5 drei Ausgänge; 36.6 Abbild | 36.2 → 36.5 Berichtigung, 37.3 Ergänzung; 36.5 → 37.1 Präzisierung, 46.5 R14 Ergänzung (T4); 36.6 → 37.2, 37.3 Ergänzung |
| 37 Sonde je Bestandteil | 3 | 37.1–37.3; 37.4 Tatsachennotiz zu Abschnitt 10; 37.5 „Ort registrierter Werte“ | in 37.4: Z. 7070 ERSETZT (38.6); Z. 7082 **BERICHTIGT durch 42.3 F2** |
| 38 Weg (A), Fundstellen | 3 | 38.1 Berichtigung zu 35.1; **38.2 Fundstellen**; 38.4 Form (ii); 38.5 Kosten | 38.4 Fertigkriterium **ERSETZT (39.1)** (MARKE+ Z. 7425); 38.2 ERGÄNZT durch R49 (48.17) (Z. 7388, T4) |
| 39 Vollzug Punkt 4 | 3 | 39.1 Berichtigung zu 38.4; 39.2 Vollzug; 39.3–39.9 Tatsachennotizen | – |
| 40 Testannahmen, Handelslisten | 3 | 40.2 `G6`; 40.3 `H3`; 40.6 Handelslisten; 40.7 Ergänzung zu 12; 40.8 Beschlossenes | 40.6 → 41.1 A3 Berichtigung, A12 Präzisierung, 46.3 R12 (T4); 40.7 → 41.1 A2 Berichtigung; 40.8 (e) → 46.1 R9 Ergänzung (T4); 40.6 ERGÄNZT durch R42 (48.10), R44 (48.12), Tatsachennotiz zu 5.4 **PRÄZISIERT durch R47 (48.15)** (Z. 8425–8431, T4) |
| 41 aus 24b/24c/24d | 3 | 41.1 A1–A12; 41.2 B1–B8; 41.3 C-Einträge | A10 → 46.2 R10 Ergänzung (T4); A11 **PRÄZISIERT durch 42.1** (D2, D3; Z. 8730); A12 ERGÄNZT durch 41.2 (B3, B6/B7); B4 **PRÄZISIERT durch 42.1 (D6)** (Z. 8771); B5 BERICHTIGT durch 42.1 (D1), ERGÄNZT durch 41.3 (C6); B8 BERICHTIGT durch 41.3 (C8); C5 BERICHTIGT durch 42.1 (D5); B6/B7 ERGÄNZT durch R41 (48.9) (Z. 8856, T4) |
| 42 aus 25a/25b/25c | 3 | 42.1 D1–D12; 42.2 E-Einträge; 42.3 F-Einträge; 42.4/42.5 Tatsachennotizen | D6 ERGÄNZT durch 42.2 (E1, E2) und 42.3 (F7, F8); D2 ERGÄNZT durch 42.2 (E1), 42.3 (F8); D3/D7 **PRÄZISIERT durch 42.2 (E6)** (Z. 9026); D5 BERICHTIGT durch 42.2 (E3); D8 BERICHTIGT durch 42.2 (E5); 42 (Klasse (iv)) → 45.2 R2; 42.2 E2 → 45.4 R4 (T4); E5 ERGÄNZT durch R29 (47.12) (Z. 9242, T4) |
| 43 aus 25d/25e | 4 | 43.1, 43.2; 43.3 Berichtigung an 25e (3), vorläufig | 43.3 → 45.1 R1 „Marke an 43.3 (Bestätigung)“ (T4); 43-7 **PRÄZISIERT durch R33 (48.1)** (Z. 9732, T4) |
| 44 Vollzug TB-111/112 | 4 | Tatsachennotizen | 44-6 ERGÄNZT durch R29 (47.12) (Z. 10019) |
| 45 aus 26a | 4 | R1–R8 (45.1–45.8), R11 (45.11) | R5, R7 → 46.7 R16 Ergänzungen; 45.3 ERGÄNZT durch R42 (48.10); R4 und R5 (a) ERGÄNZT durch R29 (47.12); R5 (b) **BERICHTIGT durch R33 (48.1)**; 45.5 ERGÄNZT durch R34 (48.2), **PRÄZISIERT durch R36 (48.4)** (Z. 10239–10279) |
| 46 aus 27a | 4 | R9–R17 (46.1–46.8); 46.9 Lesart; 46.11 Vollzug | 46.3 ERGÄNZT durch R39 (48.7), R42 (48.10); R14 ERGÄNZT durch R25, R26, R27 (Bedingung 5); 46.9 ERGÄNZT durch R25 (47.8, Bestätigung) (Z. 10470–10572) |
| 47 aus 27c | 4 | R18–R32 (47.1–47.15) | 47.9 R26 **BERICHTIGT durch R61 (51.6)** (Z. 10736); 47.13 R30 **BERICHTIGT durch R61 (51.6)** (Z. 10767); beide nachgetragen nach R65 (b) (52.3) |
| 48 aus 29b | 4 | R33–R52 (48.1–48.20); R51 = Marken für Register 0–12 | 48.16 R48 (g) **BERICHTIGT durch R54 (49.2)** (Z. 10946); 48.16 R48 (d) ERGÄNZT durch R60 (51.5) (Z. 10949); 48.16 R48 (d) **PRÄZISIERT durch R64 (52.2)** (Z. 10952); 48.19 R51 **PRÄZISIERT durch R65 (52.3)** (Z. 10987); 48.1 R33 **PRÄZISIERT durch R68 (53.3)** (Z. 10800); 48.5 R37 **PRÄZISIERT durch R68 (53.3)** (Z. 10840); 48.7 R39 ERGÄNZT durch R67 (53.2) (Z. 10860) und durch R69 (53.4): R39 ist bestätigt (Z. 10863); 48.16 R48 (d) ERGÄNZT durch R72 (53.7) (Z. 10955); 48.1 R33 **PRÄZISIERT durch R75 (54.2)** (Z. 10803, vom steuernden Chat nach R65 (a) bestimmt); 48.2 R34 ERGÄNZT durch R75 (54.2) (Z. 10813); 48.4 R36 **PRÄZISIERT durch R75 (54.2)** (Z. 10830); 48.5 R37 **PRÄZISIERT durch R75 (54.2)** (Z. 10843); 48.7 R39 ERGÄNZT durch R75 (54.2) (Z. 10866); 48.14 R46 ERGÄNZT durch R75 (54.2) (Z. 10918, vom steuernden Chat nach R65 (a) bestimmt); 48.20 R52: Zählung der Fälle „Bestand behauptet statt Voraussetzung genannt“ → R76 (54.3), zwölf gezählte Fälle (ohne Marke, R77 (c)) |
| 49 aus 30a | 4 | R53–R55 (49.1–49.3) | 49.1 R53 **PRÄZISIERT durch R57 (51.2)** (Z. 11008), ERGÄNZT durch R59 (51.4) (Z. 11011) |
| 50 Tatsachennotizen E-2 | 4 | 50.1 Voraussetzungen; 50.2 Feldliste (R39); 50.3/50.4 Vollzug TB-122/TB-124; 50.5 Lesart Zählweise (vorläufig); 50.6 Entscheid R24; 50.7 Offenes | 50.5 ERGÄNZT durch R57 (51.2): die Lesart ist bestätigt (Z. 11194); 50.1, Zeile R48 (d) ERGÄNZT durch R60 (51.5) und 51.8 (Z. 11055); 50.4, Schlusssatz ERGÄNZT durch R57 (51.2): bestätigt (Z. 11185); beide nachgetragen nach R65 (b) (52.3) |
| 51 aus 01a | 4 | R56–R62 (51.1–51.7); 51.8 Voraussetzungen; 51.9 Lesart, vorläufig; 51.10 Offenes | 51.5 R60 (a) **PRÄZISIERT durch R63 (52.1)** (Z. 11256), R60 (b) und (c) **PRÄZISIERT durch R64 (52.2)** (Z. 11259); 51.6 R61 (b) **PRÄZISIERT durch R65 (52.3)** (Z. 11275); 51.9 ERGÄNZT durch R63 (52.1): die Lesart ist bestätigt (Z. 11313); 51.5 R60 **PRÄZISIERT durch R69 (53.4)** (Z. 11262); 51.6 R61 **PRÄZISIERT durch R70 (53.5)** (Z. 11278); 51.5 R60 **PRÄZISIERT durch R75 (54.2)** (Z. 11265) |
| 52 aus 02a | 4 | R63–R65 (52.1–52.3); 52.4 Voraussetzungen; 52.5 Offenes | 52.2 R64 ERGÄNZT durch R66 (53.1), zu (e) (Z. 11345); 52.2 R64 **PRÄZISIERT durch R68 (53.3)** (Z. 11348), **durch R69 (53.4)** (Z. 11351), **durch R71 (53.6): erster Kurstag** (Z. 11354) und **durch R72 (53.7): Benchmark-Tag** (Z. 11357); 52.3 R65 **PRÄZISIERT durch R70 (53.5)** (Z. 11370); 52.4, Zeile „R64 (52.2), zweite“ ERGÄNZT durch R66 (53.1) (Z. 11388); 52.4, Zeile „R64 (52.2) (a)“ **BERICHTIGT durch R69 (53.4)** (Z. 11391); 52.2 R64 **PRÄZISIERT durch R75 (54.2)** (Z. 11360) |
| 53 aus 02c | 4 | R66–R73 (53.1–53.8); 53.9 Voraussetzungen und Befunde; 53.10 Offenes | 53.1 R66 **PRÄZISIERT durch R74 (54.1)** (Z. 11417); 53.3 R68 **PRÄZISIERT durch R75 (54.2)** (Z. 11434); 53.4 R69 ERGÄNZT durch R75 (54.2) (Z. 11444); 53.5 R70 **PRÄZISIERT durch R77 (54.4)** (Z. 11454); 53.9, Zeile „R66 (53.1) (b)“ ERGÄNZT durch R74 (54.1) (Z. 11498) |
| 54 aus 04a | 5 | R74–R77 (54.1–54.4); 54.5 Voraussetzungen und Befunde; 54.6 Offenes | – |

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
| 5.1, Nr. 7 | Z. 646 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 5.3 | Z. 700 | ERGÄNZT (Verweis) | R51 (48.19) | MARKE+ | 1 |
| 7, Tabelle, Zeile (d) | Z. 810 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 7, Tabelle, Zeile (a) | Z. 813 | ERGÄNZT (Verweis) | R51 (48.19) | MARKE+ | 1 |
| 7, Tabelle, Zeile (d) | Z. 816 | ERGÄNZT | R55 (49.3) | MARKE+ | 1 |
| 7.1 | Z. 862 | ERGÄNZT | R21 (47.4) | MARKE+ | 1 |
| 7.1 | Z. 865 | PRÄZISIERT | R23 (47.6) | MARKE | 1 |
| 8.1 | Z. 920 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 9, erster Absatz | Z. 932 | PRÄZISIERT | R48 (48.16) | MARKE | 1 |
| 11.2 | Z. 1228 | ERGÄNZT | R43 (48.11) | MARKE+ | 1 |
| Abschnitt 11 | Z. 1247 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| 11.3 | Z. 1250 | ERGÄNZT | 50.3 und 50.4 | MARKE+ | 1 |
| Abschnitt 12 | Z. 1318 | ERGÄNZT | R25 (47.8) | MARKE+ | 1 |
| Abschnitt 12 | Z. 1321 | ERGÄNZT | R26 (47.9) | MARKE+ | 1 |
| Abschnitt 12 | Z. 1324 | ERGÄNZT | R49 (48.17) | MARKE+ | 1 |
| Abschnitt 12 | Z. 1327 | ERGÄNZT | R50 (48.18) | MARKE+ | 1 |
| 15.3 (b) | Z. 1446 | ERGÄNZT | R41 (48.9) | MARKE+ | 1 |
| 15.3 | Z. 1473 | ERGÄNZT | R35 (48.3) | MARKE+ | 1 |
| 15.4 (a) | Z. 1501 | BERICHTIGT | R54 (49.2) | MARKE+ | 1 |
| 15.4 | Z. 1546 | ERGÄNZT | R41 (48.9) und 50.1 | MARKE+ | 1 |
| 15.5 | Z. 1661 | ERGÄNZT | R53 (49.1) | MARKE+ | 1 |
| 15.6 (c) | Z. 1691 | PRÄZISIERT | R23 (47.6) | MARKE | 1 |
| 15.6 | Z. 1741 | ERGÄNZT (Verweis) | R51 (48.19) | MARKE+ | 1 |
| 16.4 (b) | Z. 2103 | PRÄZISIERT | R21 (47.4) | MARKE | 1 |
| 16.4 (a) | Z. 2106 | PRÄZISIERT | R22 (47.5) | MARKE | 1 |
| 16.4 (b) | Z. 2109 | PRÄZISIERT | R23 (47.6) | MARKE | 1 |
| 16.4 (c) | Z. 2112 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 16.4 (d) | Z. 2115 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 16.4 (m) | Z. 2162 | PRÄZISIERT | R18 (47.1) | MARKE | 1 |
| 16.4 (h) | Z. 2165 | PRÄZISIERT | R18 (47.1) | MARKE | 1 |
| 16.4 (l) | Z. 2168 | PRÄZISIERT | R18 (47.1) | MARKE | 1 |
| 16.4 (h) | Z. 2171 | PRÄZISIERT | R19 (47.2) | MARKE | 1 |
| 16.4 (j) | Z. 2174 | PRÄZISIERT | R19 (47.2) | MARKE | 1 |
| 16.4 (k) | Z. 2177 | PRÄZISIERT | R19 (47.2) | MARKE | 1 |
| 16.4 (l) | Z. 2180 | ERGÄNZT | R20 (47.3) | MARKE+ | 1 |
| 16.4 (j) | Z. 2183 | ERGÄNZT | R20 (47.3) | MARKE+ | 1 |
| 16.4 (i) | Z. 2186 | PRÄZISIERT | R21 (47.4) | MARKE | 1 |
| 16.4 (j) | Z. 2189 | PRÄZISIERT | R21 (47.4) | MARKE | 1 |
| 16.4 (i) | Z. 2192 | PRÄZISIERT | R22 (47.5) | MARKE | 1 |
| 16.4 (h) | Z. 2195 | ERGÄNZT | R24 (47.7) und 50.6 | MARKE+ | 1 |
| 16.4 (g) | Z. 2198 | ERGÄNZT | R24 (47.7) und 50.6 | MARKE+ | 1 |
| 16.6 | Z. 2347 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 16.7 (d) | Z. 2414 | ERGÄNZT | R38 (48.6) | MARKE+ | 1 |
| Abschnitt 18 | Z. 3095 | ERGÄNZT | R28 (47.11) | MARKE+ | 1 |
| 21.4 | Z. 3437 | ERGÄNZT | R53 (49.1) | MARKE+ | 1 |
| 22.2 | Z. 3712 | ERGÄNZT | R34 (48.2) | MARKE+ | 1 |
| 24.2 | Z. 4338 | PRÄZISIERT | R36 (48.4) | MARKE | 2 |
| 25.2 | Z. 4679 | ERGÄNZT | R53 (49.1) | MARKE+ | 2 |
| 25.3, Ersatztext (Bedingung (i) steht in dessen erster Zeile) | Z. 4699 | PRÄZISIERT | R53 (49.1) | MARKE | 2 |
| 27.3 (im Zitatblock 27.1 bis 27.5) | Z. 5175 | ERGÄNZT | R31 (47.14) | MARKE+ | 2 |
| Abschnitt 27 | Z. 5214 | ERGÄNZT | R32 (47.15) | MARKE+ | 2 |
| 28.6 | Z. 5352 | PRÄZISIERT | R53 (49.1) | MARKE | 2 |
| 29.4 | Z. 5434 | BERICHTIGT | R43 (48.11) | MARKE+ | 2 |
| 34.5 | Z. 6285 | BERICHTIGT | R43 (48.11) | MARKE+ | 2 |
| 35.1 | Z. 6443 | PRÄZISIERT | R37 (48.5) | MARKE | 2 |
| 35.4 | Z. 6523 | ERGÄNZT | R26 (47.9) | MARKE+ | 2 |
| 38.2 | Z. 7388 | ERGÄNZT | R49 (48.17) | MARKE+ | 3 |
| 40.6 | Z. 8425 | ERGÄNZT | R42 (48.10) | MARKE+ | 3 |
| 40.6 | Z. 8428 | ERGÄNZT | R44 (48.12) | MARKE+ | 3 |
| 40.6 | Z. 8431 | PRÄZISIERT | R47 (48.15) | MARKE | 3 |
| 41.2, Eintrag B6/B7 | Z. 8856 | ERGÄNZT | R41 (48.9) | MARKE+ | 3 |
| 42.2, Eintrag E5 (e) | Z. 9242 | ERGÄNZT | R29 (47.12) | MARKE+ | 3 |
| 44.1, Eintrag 44-6 | Z. 10019 | ERGÄNZT | R29 (47.12) | MARKE+ | 4 |
| 45.3 | Z. 10239 | ERGÄNZT | R42 (48.10) | MARKE+ | 4 |
| 45.4, Block R4 | Z. 10247 | ERGÄNZT | R29 (47.12) | MARKE+ | 4 |
| 45.5, Block R5, Punkt (a) | Z. 10264 | ERGÄNZT | R29 (47.12) | MARKE+ | 4 |
| 45.5, Block R5, Punkt (b) | Z. 10267 | BERICHTIGT | R33 (48.1) | MARKE+ | 4 |
| 45.5 | Z. 10276 | ERGÄNZT | R34 (48.2) | MARKE+ | 4 |
| 45.5 | Z. 10279 | PRÄZISIERT | R36 (48.4) | MARKE | 4 |
| 46.3 | Z. 10470 | ERGÄNZT | R39 (48.7) | MARKE+ | 4 |
| 46.3 | Z. 10473 | ERGÄNZT | R42 (48.10) | MARKE+ | 4 |
| 46.5, Block R14 | Z. 10501 | ERGÄNZT | R25 (47.8) | MARKE+ | 4 |
| 46.5, Block R14 | Z. 10504 | ERGÄNZT | R26 (47.9) | MARKE+ | 4 |
| 46.5, Block R14 (Bedingung 5 steht in dessen erster Zeile) | Z. 10507 | ERGÄNZT | R27 (47.10) | MARKE+ | 4 |
| 46.9 | Z. 10572 | ERGÄNZT | R25 (47.8) | MARKE+ | 4 |
| 48.16 (R48), neu in TB-126 | Z. 10946 | BERICHTIGT | R54 (49.2) | MARKE+ | 4 |

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
| 7, Tabelle, Zeile (b) | Z. 819 | PRÄZISIERT | R37 (48.5) | MARKE | 1 |
| 8, Tabelle | Z. 890 | PRÄZISIERT | R36 (48.4) | MARKE | 1 |
| 8, Tabelle | Z. 893 | ERGÄNZT | R55 (49.3) | MARKE+ | 1 |
| 16.4, „Prüfung vor dem Tag“ | Z. 2241 | PRÄZISIERT | R21 (47.4) | MARKE | 1 |
| 25.3, Ersatztext | Z. 4702 | ERGÄNZT | R58 (51.3) | MARKE+ | 2 |
| Abschnitt 27 | Z. 5217 | ERGÄNZT | R56 (51.1) | MARKE+ | 2 |
| 43.2, Eintrag 43-7 | Z. 9732 | PRÄZISIERT | R33 (48.1) | MARKE | 4 |
| 48.16 (R48) | Z. 10949 | ERGÄNZT | R60 (51.5) | MARKE+ | 4 |
| 49.1 (R53) | Z. 11008 | PRÄZISIERT | R57 (51.2) | MARKE | 4 |
| 49.1 (R53) | Z. 11011 | ERGÄNZT | R59 (51.4) | MARKE+ | 4 |
| 50.5 | Z. 11194 | ERGÄNZT | R57 (51.2): die Lesart ist bestätigt | MARKE+ | 4 |

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
| 25.2, unter dem berichtigten Satz | Z. 4676 | BERICHTIGT | R62 (51.7) und R65 (52.3) | MARKE+ | 2 |
| 47.9 (R26) | Z. 10736 | BERICHTIGT | R61 (51.6) | MARKE+ | 4 |
| 47.13 (R30) | Z. 10767 | BERICHTIGT | R61 (51.6) | MARKE+ | 4 |
| 48.16 (R48) | Z. 10952 | PRÄZISIERT | R64 (52.2) | MARKE | 4 |
| 48.19 (R51) | Z. 10987 | PRÄZISIERT | R65 (52.3) | MARKE | 4 |
| 50.1, nach der Tabelle | Z. 11055 | ERGÄNZT | R60 (51.5) und 51.8 | MARKE+ | 4 |
| 50.4, nach dem Zitatblock | Z. 11185 | ERGÄNZT | R57 (51.2): der Schlusssatz ist bestätigt | MARKE+ | 4 |
| 51.5 (R60) | Z. 11256 | PRÄZISIERT | R63 (52.1) | MARKE | 4 |
| 51.5 (R60) | Z. 11259 | PRÄZISIERT | R64 (52.2) | MARKE | 4 |
| 51.6 (R61) | Z. 11275 | PRÄZISIERT | R65 (52.3) | MARKE | 4 |
| 51.9 | Z. 11313 | ERGÄNZT | R63 (52.1): die Lesart ist bestätigt | MARKE+ | 4 |

## 8. Die Marken aus Fable 02c (TB-132)

Alle 21 Marken, die TB-132 gesetzt hat (alle am alten Ort: 20 nach R70 (c), eine an 23.3, Registertext 3b (c), vom
steuernden Chat nach R65 (a) bestimmt; 52.2 trägt fünf), in der Reihenfolge des Registers. Erzeugt mit
`docs/belege/TB-132/c2_index_02c.py` aus `docs/belege/TB-132/c1_marken.txt` (Zeile, Art, Teil) und Anhang A des
Auftrags TB-132 (alter Ort), nicht abgetippt. In Tabelle 3 und 4 oben stehen sie zusätzlich an ihrer Stelle. Keine
Marke tragen Abschnitt 9, Abschnitt 10 und der ERZEUGT-Block von Abschnitt 3; ohne Marke bleiben 7 (c), 17.5 und
50.7 Nr. 3 (R70 (b), Indexzeilen darunter) sowie 24.2 und 29.3 (R70 (c)).

| alter Ort (Anhang A) | Marke | Wort | durch | Art | T |
|---|---|---|---|---|---|
| 15.3 (a) | Z. 1449 | PRÄZISIERT | R66 (53.1) | MARKE | 1 |
| 15.3 (c) | Z. 1452 | PRÄZISIERT | R66 (53.1) | MARKE | 1 |
| 23.3, Registertext 3b (c) | Z. 3953 | PRÄZISIERT | R72 (53.7) | MARKE | 2 |
| 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse | Z. 3981 | BERICHTIGT | R71 (53.6) | MARKE+ | 2 |
| 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse | Z. 3984 | ERGÄNZT | R72 (53.7) | MARKE+ | 2 |
| Abschnitt 27 | Z. 5220 | ERGÄNZT | R73 (53.8) | MARKE+ | 2 |
| 48.1 (R33) | Z. 10800 | PRÄZISIERT | R68 (53.3) | MARKE | 4 |
| 48.5 (R37) | Z. 10840 | PRÄZISIERT | R68 (53.3) | MARKE | 4 |
| 48.7 (R39) | Z. 10860 | ERGÄNZT | R67 (53.2) | MARKE+ | 4 |
| 48.7 (R39) | Z. 10863 | ERGÄNZT | R69 (53.4): R39 ist bestätigt | MARKE+ | 4 |
| 48.16 (R48 (d)) | Z. 10955 | ERGÄNZT | R72 (53.7) | MARKE+ | 4 |
| 51.5 (R60) | Z. 11262 | PRÄZISIERT | R69 (53.4) | MARKE | 4 |
| 51.6 (R61) | Z. 11278 | PRÄZISIERT | R70 (53.5) | MARKE | 4 |
| 52.2 (R64) | Z. 11345 | ERGÄNZT | R66 (53.1) | MARKE+ | 4 |
| 52.2 (R64) | Z. 11348 | PRÄZISIERT | R68 (53.3) | MARKE | 4 |
| 52.2 (R64) | Z. 11351 | PRÄZISIERT | R69 (53.4) | MARKE | 4 |
| 52.2 (R64) | Z. 11354 | PRÄZISIERT | R71 (53.6): erster Kurstag | MARKE | 4 |
| 52.2 (R64) | Z. 11357 | PRÄZISIERT | R72 (53.7): Benchmark-Tag | MARKE | 4 |
| 52.3 (R65) | Z. 11370 | PRÄZISIERT | R70 (53.5) | MARKE | 4 |
| 52.4, nach der Tabelle | Z. 11388 | ERGÄNZT | R66 (53.1) | MARKE+ | 4 |
| 52.4, nach der Tabelle | Z. 11391 | BERICHTIGT | R69 (53.4) | MARKE+ | 4 |

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
| 16.6 | Z. 2350 | PRÄZISIERT | R75 (54.2) | MARKE | 1 |
| 17.5 | Z. 2845 | ERGÄNZT | R74 (54.1) | MARKE+ | 1 |
| 48.1 (R33) | Z. 10803 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 48.2 (R34) | Z. 10813 | ERGÄNZT | R75 (54.2) | MARKE+ | 4 |
| 48.4 (R36) | Z. 10830 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 48.5 (R37) | Z. 10843 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 48.7 (R39) | Z. 10866 | ERGÄNZT | R75 (54.2) | MARKE+ | 4 |
| 48.14 (R46) | Z. 10918 | ERGÄNZT | R75 (54.2) | MARKE+ | 4 |
| 51.5 (R60) | Z. 11265 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 52.2 (R64) | Z. 11360 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 53.1 (R66) | Z. 11417 | PRÄZISIERT | R74 (54.1) | MARKE | 4 |
| 53.3 (R68) | Z. 11434 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 53.4 (R69) | Z. 11444 | ERGÄNZT | R75 (54.2) | MARKE+ | 4 |
| 53.5 (R70) | Z. 11454 | PRÄZISIERT | R77 (54.4) | MARKE | 4 |
| 53.9, nach der Tabelle | Z. 11498 | ERGÄNZT | R74 (54.1) | MARKE+ | 4 |

### Indexzeilen aus Fable 04a

- **17.5:** Handelskalender der Aktien-Tagesreihe → R66 (a) und (b) (53.1) und R74 (54.1). Zu R74 mit Marke (R77 (a) und (b), 54.4); zu R66 gilt die Indexzeile aus Fable 02c weiter (R70 (b), 53.5).
- **48.20 (R52):** Zählung der Fälle „Bestand behauptet statt Voraussetzung genannt“ → R76 (54.3): zwölf gezählte Fälle bis zur Antwort 02c. Ohne Marke (R77 (c), 54.4). Lesart des steuernden Chats zu R77 (c), vorläufig; der Index ist kein Registertext.

---

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
Zuletzt nachgezogen in TB-136 (05.10.2026): Zeilenangaben mit `docs/belege/TB-136/c2_index_zeilen.py` vom Stand
`ee43f5f` auf `9b7b060` umgeschrieben (jede Zahl in Listen und Bereichen); 54 kommt zu T5; Abschnittstabelle aus den
Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-136/c2_index_eintraege.py`; neuer Abschnitt 9 mit den
15 Marken und zwei Indexzeilen nach R77 (b) und (c) (`c3_indexzeilen.py`).

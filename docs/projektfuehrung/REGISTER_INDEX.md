# REGISTER_INDEX — wo was im Register gerade gilt

**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `1e11457` (27.09.2026), Abschnitte 0–46,
10 347 Zeilen, sha256 `18e39ee2…`. Gebaut in TB-118 (Fable 27b B3, Teil D A4). **Das ist ein Wegweiser, nicht das
Register.** Der Wortlaut steht nur im Register bzw. in der Kopie `REGISTER_KOPIE_teil1–4.md`.

**Wie gemessen:** `python3 docs/werkzeuge/registerkopie.py --marken` sammelt jede Zeile mit „ERSETZT durch“ oder
„PRÄZISIERT durch“ (das Suchmuster des Auftrags, Art `MARKE`, 23 Zeilen), jede weitere Zeile mit ERSETZT,
PRÄZISIERT, BERICHTIGT, ERGÄNZT oder KORRIGIERT (Art `MARKE+`, 42 Zeilen) und jede Überschrift mit Rückverweis
(„Berichtigung zu“, „Präzisierung zu“, „Ergänzung zu“, „ersetzt die …“; Art `UEBERSCHRIFT`, 49 Zeilen). Die
Ausgabe liegt in `docs/belege/TB-118/a4_marken.txt`. Die Ketten unten sind **aus diesen Zeilen gelesen, nicht
erinnert**. Wo eine Stelle nur über eine Überschrift oder ein anderes Markenwort erreicht wird, steht sie in der
Spalte „dazu“, nicht als „gilt“. Nach dem Auftrag gilt „ERSETZT durch“ und „PRÄZISIERT durch“ als Kette.
**Mehrdeutig** heisst, dass die Marken keinen einzelnen Ort ergeben. Dann ist der Wortlaut zu lesen.

**Teile der Kopie** (Zuschnitt an Abschnittsgrenzen, je ≤ 240 000 Bytes):

| Teil | Abschnitte | Zeilen im Register |
|---|---|---|
| 1 | 0–23 | 1–4025 |
| 2 | 24–37 | 4026–6999 |
| 3 | 38–43 | 7000–9571 |
| 4 | 44–46 | 9572–10347 |

Schreibweise: „15.6 (a)“ ist Unterabschnitt 15.6, Punkt (a). „T2“ heisst Teil 2. „Z.“ ist die Zeile im Register am
genannten Commit.

---

## 1. Die zwölf Festlegungen (Abschnitt 1, T1)

| Festlegung | Wortlaut | Marken (Zeile) | gilt | dazu |
|---|---|---|---|---|
| 1 Führendes Mass | 1 (Tabelle), T1 | Z. 69 **PRÄZISIERT durch Abschnitt 24** | 1 **und** 24 (24.2, 24.4), T1+T2 | 24.6 Tatsachennotiz (T2) |
| 2 Selektionsstatistik | 1, T1 | – | 1, T1 | – |
| 3 Beurteilung | 1, T1 | – | 1, T1 | – |
| 4 Drawdown-Bedingung | 1, T1 | – | 1, T1 (Herleitung Abschnitt 4) | 24.2 nennt sie „unberührt“ |
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
| 3 „Der Faltenplan“ | Z. 384 ERSETZT durch Abschnitt 15, Registertext 2 und 4 | 15.4, 15.6 → weiter nach Tabelle 3 |
| 5.1 „Die Regeln“ | Z. 544 ERSETZT durch Abschnitt 15, Registertext 0, 2 und 4 | 15.2, 15.4, 15.6 → weiter nach Tabelle 3 |
| 5.3 „Krypto: Platzhalter mit Regel“ | Z. 623 ERSETZT durch Abschnitt 15, Registertext 3 und 4 | 15.5, 15.6 → weiter nach Tabelle 3 |
| 10 Sperrliste | Z. 940 (MARKE+: der Kasten an Punkt 4 sagt „nicht (iii) (ERSETZT-Marke)“, Form (ii) nach 38.4) | 10, Punkttext unverändert; Vollzug Punkt 4 in 39.2 (T3). Die Sperrlisten-Einträge 36.1, 36.6, 37.2 und 37.3 gehen in Tabelle 4 |
| 12 Vollständigkeitstest | – | 12. **Dazu:** 40.7 Ergänzung (T3), 41.1 A1 Berichtigung „sieben Mutationsproben“ (T3), 46.5 R14 Ergänzung (T4) |
| alle übrigen (0, 2, 4, 6–9, 11, 13, 14) | – | am Ort, T1 |

## 3. Registertexte 0–7 und die Registertexte ohne Nummer (Abschnitte 15–17, T1)

| Registertext | Ersteintrag | Marken der Kette (Zeile) | **gilt** | dazu (Überschrift oder anderes Markenwort) |
|---|---|---|---|---|
| **0** Verfahren | 15.2 | – | **15.2** (T1) | – |
| **1a** Bootstrap (a) | 15.3 (a) | – | **15.3 (a)** | 24.2 beruft sich auf 1a; Z. 4030 „Registertext 1a bleibt in 15.3“ |
| **1b** | 15.3 (b) | – | **15.3 (b)** | – |
| **1c** | 15.3 (c) | – | **15.3 (c)** | – |
| **2a–2c** Faltenzuordnung | 15.4 (a)–(c) | – | **15.4 (a)–(c)** | – |
| **2d** Embargo | 15.4 (d) | Z. 1378 ERSETZT durch 16.6 | **16.6** (T1) | 41.2 B2 „Berichtigung der 2d-Herleitung“ (T3) |
| **3a** Universum | 15.5 (a) | Tabelle darunter: Z. 1459 KORRIGIERT in 16.1.3 (MARKE+) | **15.5 (a)**, Rechenweg der Krypto-Zeile **16.1.3** | – |
| **3b** Symbolzahl je Falte | 15.5 (b) | Tatsachennotizen: Z. 1482 ERSETZT durch 16.1.1, Z. 1499 ERSETZT durch 16.1.2 | Regel **15.5 (b)**, Tatsachen **16.1.1/16.1.2** | Ergänzungen 3b (a)–(e) in **16.7** (siehe nächste Zeilen) |
| **3b (a)** Ergänzung | 16.7 (a) | – | **16.7 (a)** | – |
| **3b (b)** Ergänzung | 16.7 (b) | – | **16.7 (b)** | 34.3 berichtigt in 30.2 (2) „3b (b)“ zu „3b (a)“ (T2) |
| **3b (c)** Benchmark | 16.7 (c) | Z. 2200 (c) ERSETZT durch 23.3 | **23.3** (T1) | 24.2 bezieht sich auf 3b (c) „in der Fassung aus 23.3“ |
| **3b (d), (e)** | 16.7 (d), (e) | – | **16.7 (d), (e)** | – |
| **3c** Vorbehalt | 15.5 (c) | – | **15.5 (c)** | Z. 1446 ERGÄNZT durch 26.4 (T2) |
| **3d** | 15.5 (d) | – | **15.5 (d)** | – |
| **4** Falten, insgesamt | 15.6 | – | 15.6 | 21 „Berichtigung zu Registertext 4“ (15.6, Punkt 2 der Tafel, T1); 24.2 „Präzisierung zu Registertext 4“ (Drawdown Mark-to-Market, **ohne Marke in 15.6**, T2) |
| **4a** erste Falte | 15.6 (a) | Z. 1546 (a) ERSETZT durch 25.3 → Z. 4468 (i) PRÄZISIERT durch 26.2 | **25.3**, Bedingung (i) in der Fassung **26.2** (T2) | 21.3 (b) ging ebenfalls in 25.3 auf (Z. 3178). 28.6 „Registertext 4a, Präzisierung, Ergänzung“ → 30.6 „Präzisierung zu 28.6“; 32 „Bedingung (i) rechnet gegen den Horizontbeginn aus 28.4“; 33.2 „Der Faltenplan nach 4a“ (alle T2). **Mehrdeutig, ob 28.6 und 30.6 den Wortlaut von 25.3 fortschreiben oder daneben stehen, Abschnitte 25, 26, 28, 30** |
| **4b, 4c** | 15.6 (b), (c) | – | **15.6 (b), (c)** | – |
| **4d** Faltenliste | 15.6 (d) | – | Regel **15.6 (d)** | Tatsachennotizen: 21.4 (berichtigte Faltenliste, T1), 26.3 (Platzhalter) **ERSETZT** durch 28.4 (MARKE+ Z. 5027); Faltenplan als Registertext 33.2 (T2) |
| **5** Datenstand | 15.7 | Z. 1631 ERSETZT durch 16.3 | **16.3**, nach Punkten wie folgt | 18 Tatsachennotiz zu 5/5a (T1) |
| **5a** Bestand und Snapshot | 16.3 (a) | Z. 1874 ERSETZT durch 17.1 | **17.1** (T1) | 17.3 Zusatz `rand_erste`; 28.2 Ergänzung `asof` → 31 „Berichtigung zu 28.2“, Ersatztext **31.2**; 31.3 „Präzisierung zu 5a / 17.1“ (T2); 41.2 B5 Resolver-Pflicht, Ergänzung zu 5a/5e (T3) |
| **5b** Registerhash | 16.3 (b) | Z. 1888 PRÄZISIERT durch 17.9 | **16.3 (b) mit 17.9** (T1) | – |
| **5c** Reihenfolge Snapshot/Tag | 16.3 (c) | Z. 1899 ERSETZT durch 17.2 | **17.2** (T1) | – |
| **5d** UTC | 16.3 (d) | – | **16.3 (d)** | – |
| **5e** Lese-Audit | 17.4 | – | **17.4** (T1) | 19 Ergänzung Codeherkunft (T1) → 45.4 R4 „Ergänzung zu 19“ (T4); 41.2 B5 (T3) |
| **5f** Umgebung | 17.5 | – | **17.5** (T1) | 20 Tatsachennotiz Lock (T1) |
| **6** Budgetstufen (a)–(m) | 16.4 | – | **16.4** (T1) | 22.4 „Registertext 6, Ergänzung — Notbremse“ (T1); 26.7 Kette „(b) → Festlegung 11 → Registertext 6 (b)“ (T2) |
| **7** Backtester-Prüfung | 16.5 | – | **16.5** (T1) | Z. 2099 ERGÄNZT durch 17.6, 17.7, 17.8 (Ergänzungen I–III, T1) |
| Kandidatenregeln (a)–(e) | 16.8 | – | **16.8** (T1) | – |
| Vorab-Filter (a)–(c) | 16.9 | – | **16.9** (T1) | – |
| short-fähige Sleeves (a)–(e) | 16.10 | – | **16.10** (T1) | – |

## 4. Registertexte ab Abschnitt 18

Ab Abschnitt 22 heissen Registertexte nach ihrem Unterabschnitt, ab 41 nach ihrem Eintrag (A1 …, R1 …). Für jeden
Registertext ab Abschnitt 38 gilt 38.2: Fundstellen im Code werden als Datei und Bezeichner angegeben.
Die Spalte „später berührt“ nennt jede gemessene Marke und jede Rückverweis-Überschrift, die auf den Abschnitt zeigt.

| Abschnitt | T | Registertexte / Einträge darin | später berührt (Marke oder Überschrift) |
|---|---|---|---|
| 18 Tatsachennotiz 5/5a, Snapshot | 1 | Tatsachennotiz | – |
| 19 Codeherkunft (5e) | 1 | Ergänzung zu 5e | 45.4 R4 Ergänzung zu 19 (T4) |
| 20 Lock (5f) | 1 | Tatsachennotiz | – |
| 21 Faltenschranke | 1 | 21.3 Ersatztext (a)–(c); 21.4 Tatsachennotiz zu 4d; 21.9 Entscheidung zu 21.6 | 21.3 (b) **ERSETZT durch 25.3** (Z. 3178); 36.4 Tatsachennotiz zu 21.4; 38.3 Tatsachennotiz zu 21.9 |
| 22 Methodenantwort 19.09. | 1 | 22.1 allgemeine Prüfregel; 22.2 Kill-Test-Berichtswerte; 22.3 Abschalt- und Zuschaltregeln; 22.4 Ergänzung zu RT 6 | – |
| 23 Benchmark tagesgenau | 1 | 23.3 Ersatztext zu 3b (c) | in 23.3 selbst: Z. 3780 „ERSETZT (TB-71) durch den Satz zur Zeitachse oben“ (eine Tabelle in 23.3 durch einen Satz in 23.3) |
| 24 Mark-to-Market | 2 | 24.2 Präzisierung zu RT 4; 24.3 Entscheidungsregel; 24.4 Festlegung 1 | 24.6 Tatsachennotiz |
| 25 erste Falte, Konjunktion | 2 | 25.3 Ersatztext zu 4a und 21.3 (b) | (i) **PRÄZISIERT durch 26.2** (Z. 4468) |
| 26 Datenhorizont je Bot | 2 | 26.2 Präzisierung zu 4a (i); 26.4 Ergänzung zu 3 (c); 26.7 Grenzfall | 26.3 (Platzhalter-Tabelle) **ERSETZT** durch 28.4; 26.6 Zeilen 1 und 4 **ERSETZT** durch 28.5, Zeile 2 dort „erledigt“ (MARKE+); 28 „Berichtigung zu 26.3 und 26.6“; 31.6 berichtigt eine Zahl aus 26 |
| 27 Sichtschutz | 2 | 27.1–27.5 | 45.6 R6 Ergänzung zu 27 (T4) |
| 28 `asof` gesetzt | 2 | 28.2 Ergänzung zu 5a; 28.4, 28.5 Ersatzmarken; 28.6 Präzisierung und Ergänzung zu 4a | 28.2 → 31 Berichtigung, Ersatztext **31.2**; 28.6 → 30.6 Präzisierung; 32 rechnet gegen den Horizontbeginn aus 28.4 (Überschrift 32) |
| 29 Kapitalpfad ab erster Falte | 2 | 29.3 Registertext | 29.2 → 30.7 Ergänzung; 29.4 → 34.5 Berichtigung; in 29.4: „Fassung aus 21b ist ERSETZT“ (Z. 5169) |
| 30 gesperrter Faltenplan | 2 | 30.2 Registertext (1)–(3); 30.3 Tatsachennotiz Punkt 2 | 30.2 (2) → 34.3 Berichtigung; 30.2 (3) → 33.1 Berichtigung, 35.4 Präzisierung, 45.3 R3 Ergänzung (T4). **Mehrdeutig, welche Fassung von 30.2 (3) gilt, Abschnitte 33, 35, 45** |
| 31 kein Feld `asof` | 2 | 31.2 Ersatztext zu 28.2; 31.3 Präzisierung zu 5a/17.1 | – |
| 32 Horizontbeginn | 2 | Tatsachennotizen, 32.5 Entscheidungsvorlage | – |
| 33 Faltenplan als Registertext | 2 | 33.2 Registertext; 33.3 Feldliste; 33.4 Anpassungen | 33.2 → 34.1, 34.2, 35.1 Ergänzungen (35.1 → **38.1 Berichtigung**, T3); 33.3 → 34.4, 35.2 Ergänzungen, 42.1 D5 Präzisierung (→ 42.2 E3 BERICHTIGT), 45.3 R3; 33.4 Punkt 3 **ERSETZT** (35.3; MARKE+ Z. 5858), 34.6 Berichtigung. **33.2 und 33.3 sind mehrdeutig: Grundtext plus Ergänzungen in 34, 35, 38, 42 und 45** |
| 34 Faltenregeln, Feld `horizontbeginn` | 2 | 34.1–34.6 | – |
| 35 Bestätigungsperiode | 2 | 35.1–35.4 | 35.1 → 38.1 Berichtigung (T3); 35.4 → 42.1 D5 (T3) |
| 36 Schreibregel, Sonde, Abbild | 2 | 36.1 Schreibregel; 36.2 Sonde; 36.5 drei Ausgänge; 36.6 Abbild | 36.2 → 36.5 Berichtigung, 37.3 Ergänzung; 36.5 → 37.1 Präzisierung, 46.5 R14 Ergänzung (T4); 36.6 → 37.2, 37.3 Ergänzung |
| 37 Sonde je Bestandteil | 2 | 37.1–37.3; 37.4 Tatsachennotiz zu Abschnitt 10; 37.5 „Ort registrierter Werte“ | in 37.4: Z. 6808 ERSETZT (38.6); Z. 6820 **BERICHTIGT durch 42.3 F2** |
| 38 Weg (A), Fundstellen | 3 | 38.1 Berichtigung zu 35.1; **38.2 Fundstellen**; 38.4 Form (ii); 38.5 Kosten | 38.4 Fertigkriterium **ERSETZT (39.1)** (MARKE+ Z. 7160) |
| 39 Vollzug Punkt 4 | 3 | 39.1 Berichtigung zu 38.4; 39.2 Vollzug; 39.3–39.9 Tatsachennotizen | – |
| 40 Testannahmen, Handelslisten | 3 | 40.2 `G6`; 40.3 `H3`; 40.6 Handelslisten; 40.7 Ergänzung zu 12; 40.8 Beschlossenes | 40.6 → 41.1 A3 Berichtigung, A12 Präzisierung, 46.3 R12 (T4); 40.7 → 41.1 A2 Berichtigung; 40.8 (e) → 46.1 R9 Ergänzung (T4) |
| 41 aus 24b/24c/24d | 3 | 41.1 A1–A12; 41.2 B1–B8; 41.3 C-Einträge | A10 → 46.2 R10 Ergänzung (T4); A11 **PRÄZISIERT durch 42.1** (D2, D3; Z. 8456); A12 ERGÄNZT durch 41.2 (B3, B6/B7); B4 **PRÄZISIERT durch 42.1 (D6)** (Z. 8497); B5 BERICHTIGT durch 42.1 (D1), ERGÄNZT durch 41.3 (C6); B8 BERICHTIGT durch 41.3 (C8); C5 BERICHTIGT durch 42.1 (D5) |
| 42 aus 25a/25b/25c | 3 | 42.1 D1–D12; 42.2 E-Einträge; 42.3 F-Einträge; 42.4/42.5 Tatsachennotizen | D6 ERGÄNZT durch 42.2 (E1, E2) und 42.3 (F7, F8); D2 ERGÄNZT durch 42.2 (E1), 42.3 (F8); D3/D7 **PRÄZISIERT durch 42.2 (E6)** (Z. 8749); D5 BERICHTIGT durch 42.2 (E3); D8 BERICHTIGT durch 42.2 (E5); 42 (Klasse (iv)) → 45.2 R2; 42.2 E2 → 45.4 R4 (T4) |
| 43 aus 25d/25e | 3 | 43.1, 43.2; 43.3 Berichtigung an 25e (3), vorläufig | 43.3 → 45.1 R1 „Marke an 43.3 (Bestätigung)“ (T4) |
| 44 Vollzug TB-111/112 | 4 | Tatsachennotizen | – |
| 45 aus 26a | 4 | R1–R8 (45.1–45.8), R11 (45.11) | R5, R7 → 46.7 R16 Ergänzungen |
| 46 aus 27a | 4 | R9–R17 (46.1–46.8); 46.9 Lesart; 46.11 Vollzug | – |

---

**Pflege:** Nach jedem Registerauftrag zusammen mit `registerkopie.py` erneuern. Die Marken misst das Skript neu,
die Ketten liest die Sitzung aus seiner Ausgabe. Die Teil-Nummern in der Spalte T stammen aus demselben Zuschnitt
wie die Kopie. Wird ein Teil neu geschnitten, ändern sie sich mit.

# TB-132 · V4 · Prüfung der Blöcke R66–R73 (Fable-Antwort 02.10.c) gegen den Registerwortlaut

Prüfhelfer, nur lesend. Register: `docs/VORREGISTRIERUNG_neuselektion.md`, 11 313 Zeilen, Abschnitte 0–52. Geprüft ist der Codeblock der Antwort 02c (Datei Z. 134–156) samt den Zeilen „Quelle des Grundes“. Gelesen mit Skripten: Überschriften, Zeilen nach Nummer, lange Zeilen in Ausschnitten bis 400 Zeichen. Jede Anführung („…“) der Blöcke wurde zusätzlich maschinell auf einem normalisierten Strom gesucht (Blockzitat-Präfix, `**`, Backticks und Zeilenumbrüche entfernt). „REG Z.“ ist die Registerzeile, in der die Fundstelle beginnt.

Maschinenlauf: Die Blöcke tragen 35 Anführungen. Zwei sind Fables eigene „lies“-Zielsätze (R69 (c), R71), also kein Registerzitat. Die übrigen 33 stehen zeichengleich im normalisierten Strom; darunter zweimal das blosse Wort „lies“ und einmal „Dafür“, das gross geschrieben nur an anderer Stelle steht (Nr. 59). Ob der Fundort der genannte ist, steht je Zeile unten.

Urteil: **T** = trifft im Wortlaut · **S** = trifft sinngemäss · **N** = trifft nicht. Bei Verweisen ohne Anführungszeichen heisst T: Der Ort sagt das, mit den Worten des Verweises.

---

## A. Anführungen und Verweise

### R66

| # | Stelle im Block | REG Z. | Wortlaut im Register (gekürzt) | Urteil |
|---|---|---|---|---|
| 1 | 1a „Flache Tage stehen mit Rendite 0 in der Reihe“ ((a), Quelle) | 1432 | zeichengleich | T. „Exposure 0“ in (a) steht nicht in 1a; Zusatz des Blocks, als solcher erkennbar. |
| 2 | 1c „aus den täglichen Netto-Renditen des Kapitalpfads“, je Falte, ohne Einschränkung | 1440–1441 | „Der Falten-Sharpe wird für jeden Parametersatz in jeder Falte aus den täglichen Netto-Renditen des Kapitalpfads gerechnet“ | T |
| 3 | 2a „Jeder Handelstag gehört zu der Falte, in die sein Datum fällt“ | 1475–1476 | zeichengleich | T |
| 4 | 29.3 (1. Januar der ersten Selektionsfalte) | 5384 | „Der Kapitalpfad eines Bots beginnt am 1. Januar seiner ersten Selektionsfalte …“ | T |
| 5 | 35.1 (Ende der Bestätigungsperiode) | 6351 | „… bis zum Go-Live-Schnitt (5.2), Ende ausschliesslich.“ | T |
| 6 | 15.4, Anmerkung 1 (Krypto Kalendertage) | 1514 | „‚Handelstage‘ heisst bei Krypto Kalendertage — der Markt läuft durch.“ | T |
| 7 | 17.5 „Der Handelskalender kommt nicht aus einer Datei, sondern aus dem Paket“ | 2826–2827 | „… sondern aus dem Paket pandas_market_calendars (gemessen TB-47: Fassung 4.6.1 …)“ | T (Zitat endet vor dem Paketnamen) |
| 8 | 17.5 „Umgebung, nicht Eingabe“; „im Lock“ | 2828–2829 | „Er ist damit Umgebung, nicht Eingabe, und liegt im Lock.“ | T |
| 9 | (b) „(TB-47, Feld kalender)“ | 2847 | „Die Einordnung ist gemessen worden (TB-47, eingaben.json, Feld kalender) und nicht geraten.“ | **S.** Das Feld steht im Register, aber nur in der Erläuterung unter 17.5 (kein Blockzitat), mit Datei `eingaben.json` (Z. 2600: `research/snapshotgrenze/ergebnisse/eingaben.json`). Gemessen ist dort die Einordnung „Umgebung“, nicht, welcher Kalender des Pakets benutzt wird. R66 (b) lässt den Dateinamen weg (38.2: Datei und Bezeichner). „NYSE“/„XNYS“: 0 Treffer im Register. |
| 10 | (b) „Universumsdatei des Bots (3a)“ | 1547–1548; 1570–1575; 1582–1584 | „Das Universum je Bot ist seine heutige Symbolliste (Datei und Hash im Register)“; „Die Universumsdateien (Tatsachennotiz zu 3a)“ | T. Zwei Dateien, nicht neun. |
| 11 | (b), (e): Bauart R33; Wache endet mit 2; „Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf trägt sie selbst“ | 10773; 11276 (R64 (c)); 10864 | R64 (c): zeichengleich dieselbe Formel | T |
| 12 | (c) Formel aus 15.3, 252 Perioden, Krypto 365 | 1449–1450 | „Mittel / Standardabweichung der täglichen Netto-Renditen der Falte × √252 (Krypto: √365 auf Kalendertagen)“ | T. `ddof` nennt die Formel nicht. |
| 13 | (c) „(2a; halboffen wie im Faltenplan)“ | 11276 (R64 (d)) | „(halboffen wie im Faltenplan; 2a)“ | T |
| 14 | R50 „Der Registertext legt keine dieser Definitionen neu fest“ (Quelle) | 10920 | zeichengleich | T |
| 15 | (c), (d) „registrierte Definition (R50)“ für Falten-Sharpe und DSR-Eingaben | 10920 | „Die Definitionen der Kennzahlen des Laufs — Falten-Sharpe (15.3), …, DSR-Eingaben (Sharpe, T, Schiefe, Wölbung, Streuung), … — sind im eingefrorenen Code registriert“ | T |
| 16 | (c) „den Bezeichner trägt die Tatsachennotiz nach R50 (38.2)“ | 10920; 7326, 7334 | R50: „Vor dem Tag wird je Kennzahl eine Tatsachennotiz eingetragen: Datei und Bezeichner (38.2)“. 38.2: „Registertext, Ersteintrag — Fundstellen: Datei und Bezeichner, Zeilennummern nur mit Commit“ | T. 38.2 gibt es, der Verweis passt; er steht so schon in R50. |
| 17 | (d) Drawdown der Nebenbedingung auf den Tagen des Benchmarks (24.2, R36) | 4303–4307; 10794 | 24.2: „auf denselben Tagen wie der Benchmark (3b (c))“; R36: „auf den Tagen des Benchmarks (3b (c))“ | T |
| 18 | (d) mittlere Exposure (R64) | 11276 | R64 (a): „die Tage des Zeitraums, an denen der Benchmark des Bots definiert ist (23.3)“ | T |
| 19 | (d) Beta-Bereinigung und Calmar-Vergleich (7 (c)) | 827–834 | „Beide Reihen werden auf gemeinsame Tage gebracht“; „über dieselben Tage. Verglichen wird Calmar gegen Calmar.“ | T |
| 20 | (d) R48 (g): „dieselben Tage wie 7 (c)“ | 10885 | „Zufalls-Timing (8.1): über die aneinandergehängten Selektionsfalten (dieselben Tage wie 7 (c))“ | T. Die Marke R54 (Z. 10892) berichtigt nur „Summe“, nicht die Tage. |
| 21 | (d) Selektionsstatistik (15.2) | 1420–1422 | „Selektionsstatistik ist der Median der Falten-Sharpes“ | T |
| 22 | (d) „Abschnitt 9 nennt keine Tage“ | 925–961 | Abschnitt 9 ganz gelesen: N, drei Werte, Clustering, Bericht; kein Satz zu Tagen | T |
| 23 | (f) „Die DSR ist Bericht, nicht Tor (Festlegung 11)“ | 955; 69 | zeichengleich | T |
| 24 | (e) „Tatsachennotiz zu 3b (c), Satz zur Zeitachse“ | 3957 | Kopfzeile: „Tatsachennotiz zu 3b (c), Satz zur Zeitachse (TB-71, 20.09.2026)“ | T |
| 25 | (e) „zweite Voraussetzung aus R64“ | 11276 (Ende) | „dass an einem Tag ohne Benchmark-Tag keine Zelle eine offene Position führen kann, ausser am Tag aus der Tatsachennotiz zu 23.3“ | T |
| 26 | (f) „in vier ersten Falten (33.2, 23.4)“ | 5972–5976; 4009–4014; 4061 | 33.2: erste Falten der fünf Krypto-Bots; 23.4, Wirkung 1 und 3: vier Bot-Falten mit teilweisem Benchmark | T (wie V1, B2) |
| 27 | (d), (f) „Nebenbefund der DSR-Einheiten (50.7 Nr. 3)“, „vor dem Tag“ | 11150 | „Nebenbefund DSR-Einheiten kennzahlen.py:222–224 (Vormessung 29.09.2026, Abschnitt 2) \| vor dem Tag“ | T |
| 28 | (f) „auswertung.py liest netto_sharpe aus zellen.csv“ | 11008–11010 | Vertrag: `zellen.csv` mit Feld `netto_sharpe` | T für das Feld; das Leseverhalten ist Code, nicht geprüft. |
| 29 | 3a „Symbole ohne Historie in einer Falte tragen 0 Trades und 0 Rendite bei“ | 1550–1551 | zeichengleich | T |
| 30 | 15.5, Lesart A „trägt für diese Tage 0 bei“ | 1631 | „… und trägt für diese Tage 0 bei, genau wie es der nächste Satz von 3a vorschreibt.“ | T. Rand: Erläuterung, kein Blockzitat; für die Faltenzählung gilt Lesart H (16.2, Z. 1968). Der Satz ist davon nicht berührt. |
| 31 | „die Tatsachennotiz zu 1c spricht von Falten ohne Trade“ | 1452–1458 | „… die Schärfung von Regel 5.1 Nr. 8 (‚Falten ohne Trade zählen mit Sharpe 0‘)“ | T (in V1 noch S; jetzt richtig gefasst) |
| 32 | 23.2, Grund 2 „der Schaden dort entsteht aus dem Vergleich zweier Reihen“ | 3908 | „Unter VH erzeugt Rang 3 Alpha aus Nichtteilnahme. Benchmark −88 %, Bot ≈ 0 ⇒ … daraus, dass der Bot nichts halten konnte.“ | **S.** Deutung; „Vergleich zweier Reihen“ steht dort nicht. Die Deutung trägt (Alpha ist ein Vergleich). |
| 33 | 24.1 und 24.2 (Bewertungsachse; Zeitachse für den Drawdown) | 4275–4277; 4309–4311 | „… aber nicht auf der Bewertungsachse“; „Er legt die Bewertungsachse fest … und die Zeitachse (dieselben Tage wie der Benchmark …)“ | T |
| 34 | 23.4, Wirkung 3 (Rendite 0 bewegt den Pfad nicht) | 4065 | „Ein Tag mit Rendite 0 bewegt den Kapitalpfad nicht; das ist der Grund, kein Zufall.“ | T |
| 35 | 23.3 „zur Entstehung: der Kapitalpfad hatte keinen Kalender“ | 3947–3953 | „Seine zweite Fassung band den Benchmark an den Kalender des Bot-Kapitalpfades — den es nicht gibt: der Pfad ist ereignisindiziert“ | T |
| 36 | R64 (c); R33; R46; Abschnitt 9 (Quelle) | 11276; 10773; 10864 | wie Nr. 11, 22 | T |
| 37 | „für die Entscheidung ohne Belang (Bauart 24.3)“ | 4327–4330 | „… wird gemessen und berichtet und ist für die Entscheidung ohne Belang.“ | T |

### R67

| # | Stelle im Block | REG Z. | Wortlaut im Register (gekürzt) | Urteil |
|---|---|---|---|---|
| 38 | R33 „Eine fehlende Zeile ist ein Befund über den Erzeuger, kein Ausgang“; „nie nichts“ | 10773 | zeichengleich | T |
| 39 | R39 (die Feldliste jeder Ausgabe ist Registertext) | 10815 | „Die Feldliste jeder dieser Dateien ist Registertext (Bauart 33.3, 41.1 A12)“ | T |
| 40 | `tagesreihen/<zelle>.csv`, `benchmark_tagesreihen/<bot>.csv`, Feld `datum` | 10815; 11015–11016; 11034–11035 | R39 nennt beide Namen; Vertrag: „datum, netto_rendite, exposure“ und „datum, netto_rendite“ | T. Rand: Der Vertrag schreibt `<zelle_id>.csv`, R39 und R67 `<zelle>.csv`. |
| 41 | Messung in 52.4 (lies_tagesreihe, lies_benchmark, beta_bereinigung) | 11296; 11309 | „Fehlende Werte und doppelte Daten werden dort weder behandelt noch geprüft (52.5)“ | T (die drei Funktionen jetzt genannt) |
| 42 | R64 (c) (Bauart), R46 | 11276; 10864 | wie Nr. 11 | T |

### R68

| # | Stelle im Block | REG Z. | Wortlaut im Register (gekürzt) | Urteil |
|---|---|---|---|---|
| 43 | R37 (i) „Die Bestätigungsstatistik des Gewinners beginnt am ersten Handelstag ab Beginn der Spanne, an dem keine vor der Spanne eröffnete simulierte Position des Gewinners mehr offen ist“ | 10801 | zeichengleich | T |
| 44 | R37 „Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle“ | 10801 | „… für jede Zelle (bestaetigung_ab_effektiv, R34)“ | T |
| 45 | R33 (genau eine Zeile je Zelle und Falte, Bestätigungsperiode eingeschlossen) | 10773–10774 | „für jede Zelle des Rasters und jede Falte des Faltenplans des Bots — Selektionsfalten und Bestätigungsperiode (35.1) — genau eine Zeile“ | T |
| 46 | 16.6 „ausdrückliche und seltene Ausnahme von der Ein-Pfad-Regel“ | 2305–2306 | „(Attribution je Position, ausdrückliche und seltene Ausnahme von der Ein-Pfad-Regel)“ | T. Einziger Treffer von „Ein-Pfad-Regel“ im Register. |
| 47 | „Attribution je Position (16.6, R37)“ | 2305; 10801 | 16.6 wie Nr. 46; R37: „eine am Deckeltag noch offene solche Position zählt nicht (Attribution je Position)“ | T |
| 48 | Tatsachennotiz: 2d in 15.4 (d) „Tage im Embargo gehören zu keiner Periode“ ist durch 16.6 vollständig ersetzt | 1487–1488; 1490–1493; 2294; 2308–2310 | 15.4 (d) zeichengleich; Marke „ERSETZT durch Abschnitt 16 …, 16.6“; 16.6-Kopf: „(ersetzt die Fassung aus 15.4 vollständig)“ | T (der Fehler N aus V1 ist behoben) |
| 49 | R63 (d) (Bauart: Exposure aus derselben Rechnung wie die MtM-Reihe) | 11269 | „die Spalte exposure aus derselben Rechnung wie die MtM-Reihe (R60 (c))“ | T |
| 50 | R64 (a); 35.1; `bestaetigung_ab_effektiv` | 11276; 6351; 10801, 10780 | — | T |
| 51 | (d) Gleichheitsproben nach R60 (c) und R64 (d), Nachrechnung nach R36 | 11196; 11276; 10794 | R60 (c): „Die Abnahme nach R46 prüft diese Gleichheit, mit Gegenprobe“; R64 (d): „prüft auch diese Gleichheit“; R36: „rechnet … nach und endet bei Abweichung mit 2“ | T |

### R69

| # | Stelle im Block | REG Z. | Wortlaut im Register (gekürzt) | Urteil |
|---|---|---|---|---|
| 52 | „25c (1), nach der Wiedergabe in R48 und R50“ | 10881 (R48 (c)); 10920 (R50) | R48 (c): „Abweichung ist ein Register-Code-Widerspruch nach 25c (1)“; R50: „… ein Register-Code-Widerspruch (25c (1)) und wird gemeldet, nicht eingetragen“ | T (in V1 noch S; jetzt als Wiedergabe gekennzeichnet). In R48 steht es in (c), nicht in (d). |
| 53 | R39: `<bot>.csv` gegen `<markt>.csv` | 10815 | „‚benchmark_tagesreihen/<markt>.csv‘ im Vertrag lies ‚<bot>.csv‘“ | T |
| 54 | R39 mit Grund (23.3; 16.7 (b)) | 10815; 3930–3931; 2352–2365 | „(23.3: Symbole, die der Loader des Bots handelbar macht; 16.7 (b): Schranken je Bot)“ | T (Fable setzt „die“ davor, ohne Anführungszeichen) |
| 55 | 37.3 „(Auftrag, Freigabe, alter und neuer Hash)“, neues Abbild | 6977 | „… wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz); er wird durch ein neues Abbild unter neuem Namen geschlossen“ | T (in V1 noch S wegen „Einzelfreigabe“; jetzt im Wortlaut) |
| 56 | „Nachweis mit Gegenprobe (Bauart R55, R64)“ | 10968; 11276 | R55: „Eine Prüfung für die leere Menge mit Gegenprobe (40.7) wird ergänzt (Handwerk)“; R64 (c): „prüft diese Wache, mit Gegenprobe“ | **S.** Beide nennen eine Prüfung „mit Gegenprobe“, keine den Nachweis einer beauftragten Änderung. Diese Bauart steht in R45 (Z. 10857: „Beauftragte Änderung nach 37.3 mit Nachweis in der Bauart von 10.1 …; Mutationsprobe“), das die Quelle richtig nennt. |
| 57 | „planmässige Öffnung von auswertung.py, die R36 …, R37 …, R34 … und R55 … verlangen“ | 10794; 10801; 10780; 10968 | R36: „auswertung.py rechnet … nach“; R37: „auswertung.py nimmt den Wert der Gewinnerzelle“; R34: „auswertung.py liest die Zeile des Plateau-Gewinners“; R55: „Umbenennung mit der nächsten planmässigen Öffnung“ | **S.** Von einer Öffnung spricht nur R55; R34, R36 und R37 beschreiben ein Soll-Verhalten. Dass es eine Öffnung „verlangt“, ist Schluss aus der Messung Teil 0 Nr. 1 (Code, hier nicht geprüft). |
| 58 | R64 (e) „auswertung.py wird für nichts davon geöffnet“ | 11276 | zeichengleich | T |
| 59 | „Dafür“ in R60 (c) | 11196 | „auswertung.py wird dafür nicht geöffnet.“ | **S.** Im Register klein, mitten im Satz. Gross steht „Dafür“ nur in Z. 4413 (anderer Ort). Für einen zeichengleichen Registertext: „dafür“. |
| 60 | R45 (Bauart einer beauftragten Änderung) | 10857 | siehe Nr. 56 | T |
| 61 | 50.1 und 50.2 (Stand des Vertrags) | 10985; 11034–11040 | 50.1, Zeile R36: „Der Vertrag führt heute nur kapital_drawdown_pct“; 50.2: `<markt>.csv`, keine Feldliste für `zellenbericht.csv` | T |
| 62 | 23.5 „ein Name, der etwas anderes verspricht als das Verhalten“, dort zu einem Docstring | 4082 | zeichengleich; Zeile „bh_tagesrenditen, Docstring“ | T (in V1 noch S; berichtigt) |

### R70

| # | Stelle im Block | REG Z. | Wortlaut im Register (gekürzt) | Urteil |
|---|---|---|---|---|
| 63 | „7 (c) trägt keine Marke zu R64“ | 810–820 | Marken in Abschnitt 7: 7 (d) R48, 7 (a) R51, 7 (d) R55, 7 (b) R37; keine zu R64 | T |
| 64 | Abschnitt 7 „gemeinsame Tage“, „über dieselben Tage“ | 830; 833–834 | zeichengleich (zweites über einen Zeilenumbruch) | T |
| 65 | R64 gibt das „lies“ R48 (d) und R60 (c), nennt 7 (c) als Geltungsbereich, bestätigt in (b) den Code | 11276 | (a) „‚Handelstage des Zeitraums‘ in R48 (d) lies“; (d) „‚Über die Tage der Falte‘ in R60 (c) lies“; (a) „und für die des Gewinners über seine Selektionsfalten (7 (c))“; (b) „… ist die Regel aus Abschnitt 7 … und kein Register-Code-Widerspruch“ | T |
| 66 | R61 (b), erster und zweiter Satz | 11209 | „Eine Marke steht dort, wo ein Block dem Wortlaut eines Ortes eine Bedeutung gibt oder ihm etwas hinzufügt (34). Keine Marke erhält ein Ort, der nur Quelle des Grundes, Statusliste, Plan oder Code ist, …“ | T |
| 67 | „die Zeile ‚R54 an 7 (c)‘“ | 11209 | „Ohne Marke bleiben, vom Index geführt: R27, R28, R30, R54 an 7 (c), R52 (b), …“ | Wortlaut T. **S** für „Zeile“: Es ist ein Glied einer Aufzählung im Fliesstext von R61 (b), keine Zeile. |
| 68 | R65 (a) (Tabelle von Befunden ist keine Statusliste; Bestätigung trägt ERGÄNZT mit Zusatz) | 11283 | „Eine Tabelle von Befunden ist keine Statusliste im Sinn von R61 (b), soweit ein Block den Befund einer Zeile ergänzt oder berichtigt. Eine Bestätigung trägt das Markenwort ERGÄNZT mit dem Zusatz, was bestätigt ist“ | T |
| 69 | 34 (Kopf: die Marke steht am alten Ort; nach der Wiedergabe in R61 und R65) | 6128–6131; 11210; 11284 | „die Marke steht AM ALTEN ORT“; R61-Quelle: „34 (Marke am alten Ort, nach der Wiedergabe in 43.0)“; R65-Quelle: „34 (Kopf: die Marke steht am alten Ort; 34.3: …)“ | T |
| 70 | „so 4.2 zu R64“; Wortlaut von 4.2 nennt die Tage nicht | 528–529; 486–491 | Marke „4.2 PRÄZISIERT durch R64 (52.2) (… Unterpunkt (a) …)“ | T |
| 71 | Wortlaut von 15.3 (a) und R33 nennt Kalender bzw. Tage nicht | 1430–1432; 10773 | 1a: „auf der Reihe der täglichen Netto-Mark-to-Market-Renditen des Kapitalpfads“; R33: eine Zeile je Zelle und Falte | T |
| 72 | (b) Indexzeile 50.7 Nr. 3 | 11150 | wie Nr. 27 | T |
| 73 | (c) 52.4, Zeile „R64 (52.2), zweite“ | 11297 | erste Zelle der Tabellenzeile: „R64 (52.2), zweite“ | T |
| 74 | (c) 52.4, Zeile „R64 (52.2) (a)“ | 11298 | erste Zelle: „R64 (52.2) (a)“; Befund: „auswertung.py wird nach R64 (e) nicht geöffnet (52.5)“ | T |
| 75 | (c) 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse; „unter dem Blockzitat der Notiz (Vorbild 25.2)“ | 3957–3964; 4655 | 25.2: Marke direkt unter dem Absatz mit dem berichtigten Satz, vor der älteren Marke (Z. 4658) | T |
| 76 | (c) „27 — ERGÄNZT durch R73“ | 11209; 5196 | R61 (b): „27 — ERGÄNZT durch R56“; gesetzte Marke: „Abschnitt 27 ERGÄNZT durch R56 (51.1)“ | T (Bauart) |
| 77 | (c) 48.7: „ERGÄNZT durch R69: R39 ist bestätigt“ | 11283; 11128 | R65 (a), letzter Satz; Vorbild: „50.4, Schlusssatz ERGÄNZT durch R57 (51.2): der Schlusssatz ist bestätigt“ | T (Hinweis aus V1 ist aufgenommen) |
| 78 | (c) 51.6 und 52.3 PRÄZISIERT durch R70 (a) | 11212 | Vorbild: „51.6 R61 (b) PRÄZISIERT durch R65 (52.3)“ | T |
| 79 | (c) Marke „ERGÄNZT durch R72“ an der Tatsachennotiz zu 3b (c); Kopf von R72: „Tatsachennotiz zu Registertext 3b (c) (23.3)“ | 3928–3939; 3957–3964 | Registertext 3b (c) ist das Blockzitat Z. 3928–3939; die Tatsachennotiz ist Z. 3959–3964 | **S.** R72 bezieht sich im Kopf auf den Registertext 3b (c); R70 (c) setzt die Marke nur an die Tatsachennotiz. Siehe Nr. 89 und Teil B, Anmerkung zu 23.3. |

### R71

| # | Stelle im Block | REG Z. | Wortlaut im Register (gekürzt) | Urteil |
|---|---|---|---|---|
| 80 | Ausgangssatz des „lies“: „Die Umsetzung lässt den ersten Kurstag je Falte aus, weil pct_change dort keine Rendite liefert“ | 3959–3960 | „> Die Umsetzung lässt den ersten Kurstag je Falte aus, weil \`pct_change\` dort / > keine Rendite liefert.“ | T. Zeichengleich bis auf die Backticks und den Zeilenumbruch nach „dort“; der Satz endet mitten in Z. 3960. |
| 81 | „höchstens ein Tag je Falte“ (klein) | 3960–3961 | „Abweichung gegenüber dem Satz: höchstens ein Tag je / Falte.“ | T (in V1 noch S; jetzt klein und als Satzteil bezeichnet) |
| 82 | R64 (a) („erster Kurstag“) | 11276 | „die Tatsachennotiz zu 23.3 (erster Kurstag) gilt mit“ | T |
| 83 | 23.4, Wirkung 3: vier Falten, je ein Tag, „der Tag des ersten Kurses, an dem noch keine Rendite vorliegt“ | 4061 | „C_lit … 4 Falten um je +1: … (der Tag des ersten Kurses, an dem noch keine Rendite vorliegt)“ | T |
| 84 | 23.5 „die erste Tagesrendite eines Symbols ist die vom Handelbar-Tag auf den Folgetag“ | 4079 | zeichengleich | T |

### R72

| # | Stelle im Block | REG Z. | Wortlaut im Register (gekürzt) | Urteil |
|---|---|---|---|---|
| 85 | 23.3 „nur eines darf im Register stehen, und es muss das sein, was der Code tut“ | 3970 | „*‚nur eines darf im Register stehen, und es muss das sein, was der Code tut. Vor dem Eintrag nachsehen.‘*“ | T. Rand: Der Satz ist ein Fable-Zitat im erläuternden Absatz von 23.3, der nach Z. 3953–3955 „als Vorgeschichte“ stehen bleibt; er steht nicht im Ersatztext. |
| 86 | 23.3 „Bot und Benchmark leben an jedem Tag in derselben Menge“ | 3938–3939 | zeichengleich (Ersatztext, letzter Satz) | T |
| 87 | „handelbar“ nach 3b (b) | 3934–3935; 3991–3996; 2352–2372 | „an denen mindestens ein Symbol des Bots nach 3b (b) handelbar ist“; „Ein Symbol ist an einem Tag handelbar, wenn seine Historie bis zu diesem Tag die registrierte Loader-Schranke erreicht“ | T. Rand zu (a): Bei `elliott_wave` zählt 3b (b) Kerzen; Z. 2367–2370: „Bei Kerzenzählung hängt die Handelbarkeit eines Symbols von der Lückenfreiheit der Reihe ab“. |
| 88 | 23.4 „der Rahmen kennt nur Tage, an denen mindestens ein Symbol einen Kurs hat“ | 4067–4068 | zeichengleich (Absatz unter der Tabelle zu Wirkung 3) | T. Rand: Der Satz beschreibt den Rahmen der W/C-Messung (warum `.fillna(0)` allein Fables alten Satz nur teilweise umsetzt), keine Definition des Benchmark-Tags. |
| 89 | (b) „Benchmark-Tag des Bots im Sinn von 23.3 … ein Tag, an dem mindestens ein nach 3b (b) handelbares Symbol des Bots einen Kurs trägt“ | 3933–3936 | 23.3: „Der Benchmark einer Falte ist an genau den Tagen definiert, an denen mindestens ein Symbol des Bots nach 3b (b) handelbar ist.“ | **S.** 23.3 kennt die Bedingung „einen Kurs trägt“ nicht; (b) ist enger als der Wortlaut. Der Block heisst Tatsachennotiz, wirkt hier aber wie eine Präzisierung von 3b (c). |
| 90 | 23.2 (die Menge, in der ein Bot lebt) | 3898 | „Die Menge, in der ein Bot lebt, ist tagesgenau“ | T |
| 91 | 17.5 (registrierte Umgebung, Abbruch bei Abweichung); (e) „Die Prüfung der Umgebung nach 5f deckt das im Lauf“ | 2820–2824; 3224–3225; 3238; 3249 | 5f: „Der Lauf beginnt mit einer Prüfung dieser drei Angaben und bricht bei Abweichung ab (Rückgabewert 2)“. Abschnitt 20: „prüft bei Start Interpreter, Paketfassungen und Plattform gegen diese Datei“; Lock führt `pandas==2.3.3`; Probe mit verfälschter pandas-Zeile endet mit 2 | T. Stützend ist Abschnitt 20 (Tatsachennotiz zu 5f), den R72 nicht nennt. |
| 92 | 24.6 (Bauart: fortgeschriebene Kurstage werden gezählt) | 4471 | Zeile „Grundlage“: „1d-Kurse decken jeden Tagesschluss mit offener Position (0 fortgeschriebene Kurstage bei … Positionstagen)“ | **S.** Der Begriff trifft. 24.6 berichtet eine Zählung in einer Messung an Trade-Listen (Forschungsskript), keine Regel; „Bauart“ ist Fables Schluss. |
| 93 | R48 (d) (bewertet wie die MtM-Reihe) | 10882 | „… am Tagesschluss, bewertet wie die MtM-Reihe (1a).“ | T |
| 94 | (d) Verfahrensmessung nach 27.2 | 5143 | „Zulässig sind Verfahrensmessungen — Kalender, Datenbestand, Faltenzahl, Handelbarkeit, Benchmark-Seite“ | T |
| 95 | `bh_tagesrenditen`; „zwei Universumsdateien“ | 10815; 3963; 1570–1584 | R39: „benchmark.py::bh_tagesrenditen (Sperrlistenpunkt 6, unverändert)“; „zwei Universen, nicht neun“ | T |

### R73

| # | Stelle im Block | REG Z. | Wortlaut im Register (gekürzt) | Urteil |
|---|---|---|---|---|
| 96 | „Tatsachennotiz zu 27 nach R56 (c)“ | 11168 | „(c) Ein eigener Block nach der Bauart von R32 bleibt nötig, wenn ein Chat mehr weiss, als Eröffnungstext und Leseprotokoll nennen: nach einer Verdichtung, bei Wissen aus einem Vorgängerchat, nach einer Treffermeldung mit Inhalt (27.7).“ | **S.** Der Fall hier (derselbe Chat beantwortet eine Eröffnung, die für einen neuen Chat geschrieben war) ist keiner der drei genannten; die Anwendung ist sinngemäss. |
| 97 | R56 (a), (b); 27.4; 27.1 | 11168; 5147; 5141 | (a) Anfangsbestand = Eröffnungstext und Leseprotokoll der ersten Antwort; (b) Schlusssatz „weitere Grössen nach 27.1 nicht kennt“; 27.4 Leseprotokoll | T |
| 98 | Bauart R32 (Tatsachennotiz zu 27) | 10760–10762 | „R32 — Tatsachennotiz zu 27 — Anfangsbestand des Verfahrensprüfers beim dritten Umzug“ | T |

**Nicht glatt (S):** Nr. 9, 32, 56, 57, 59, 67, 79, 89, 92, 96. **N:** keine.
Von Gewicht: Nr. 89 (mit 79) und Nr. 9. Reine Wortlautsache: Nr. 59, 67.

---

## B. Orte der Marken nach R70 (c)

Bauart der Marken in 47–52 und an alten Orten: Blockzitat-Zeile „> ⭐ **<Ort> <MARKENWORT> durch R.. (..)** (Fable …, TB-…, Datum).“, Folgezeile „> Eintrag und Stand oben bleiben zeichengleich.“, je eine Leerzeile davor und danach. In 47–52 steht die Marke nach dem Blockzitat des Blocks und vor „**Kette:**“.

| Ort (Marke nach R70 (c)) | Registerzeilen des Ortes | vorhandene Marken (Zeile + Folgezeile) | neue Marke nach Z. | danach folgt |
|---|---|---|---|---|
| 15.3 (a) — PRÄZISIERT durch R66 (a), (b) | Kopf 1428; Blockzitat 1430–1444; (a) = 1430–1432 | 1446/1447 „15.3 (b) ERGÄNZT durch R41 (48.9)“; 1460–1465 „Folge für den Lauf (43.2, 43-7 …)“ (andere Bauart, Schluss „Registertext und Tatsachennotiz oben bleiben zeichengleich.“); 1467/1468 „15.3 ERGÄNZT durch R35 (48.3)“ | **1447** (Vorbild: die Marke zu einem Unterpunkt steht direkt unter dem Blockzitat). Andere Lesart „nach allen Marken“: 1468. | Leerzeile 1448, dann 1449 Formelzeile. Bei 1468: Leerzeile 1469, dann „---“ 1470. |
| 15.3 (c) — PRÄZISIERT durch R66 (c) | (c) = 1439–1444 | wie oben | nach der Marke zu 15.3 (a), also nach 1447 + neue Marke | wie oben |
| 48.1 (R33) — PRÄZISIERT durch R68 | Kopf 10771; Blockzitat 10773–10774 | keine | **10774** | Leerzeile 10775, „**Kette:**“ 10776 |
| 48.5 (R37) — PRÄZISIERT durch R68 | Kopf 10799; Blockzitat 10801–10802 | keine | **10802** | Leerzeile 10803, „**Kette:**“ 10804 |
| 48.7 (R39) — ERGÄNZT durch R67; ERGÄNZT durch R69: R39 ist bestätigt | Kopf 10813; Blockzitat 10815–10816 | keine | **10816** | Leerzeile 10817, „**Kette:**“ 10818 |
| 48.16 (R48 (d)) — ERGÄNZT durch R72 (c) | Kopf 10876; Blockzitat 10878–10890; (d) = 10882 | 10892/10893 „48.16 R48 (g) BERICHTIGT durch R54 (49.2)“; 10895/10896 „48.16 R48 (d) ERGÄNZT durch R60 (51.5)“; 10898/10899 „48.16 R48 (d) PRÄZISIERT durch R64 (52.2)“ | **10899** | Leerzeile 10900, „**Kette:**“ 10901 |
| 51.5 (R60) — PRÄZISIERT durch R69 (c) | Kopf 11194; Blockzitat 11196–11197 | 11199/11200 „51.5 R60 (a) PRÄZISIERT durch R63 (52.1)“; 11202/11203 „51.5 R60 (b) und (c) PRÄZISIERT durch R64 (52.2)“ | **11203** | Leerzeile 11204, „**Kette:**“ 11205 |
| 51.6 (R61) — PRÄZISIERT durch R70 (a) | Kopf 11207; Blockzitat 11209–11210 | 11212/11213 „51.6 R61 (b) PRÄZISIERT durch R65 (52.3)“ | **11213** | Leerzeile 11214, „**Kette:**“ 11215 |
| 52.2 (R64) — ERGÄNZT durch R66; PRÄZISIERT durch R68, R69 (c), R71, R72 (b) | Kopf 11274; Blockzitat 11276–11277 | keine | **11277** | Leerzeile 11278, „**Kette:**“ 11279 |
| 52.3 (R65) — PRÄZISIERT durch R70 (a) | Kopf 11281; Blockzitat 11283–11284 | keine | **11284** | Leerzeile 11285, „**Kette:**“ 11286 |
| 52.4, Zeile „R64 (52.2), zweite“ — ERGÄNZT durch R66 (a), (e) | Kopf 11288; Tabelle 11292–11299; Zeile = 11297 | keine in 52.4 | **11299** (nach der Tabelle; Vorbild 50.1) | Leerzeile 11300, „### 52.5“ 11301 |
| 52.4, Zeile „R64 (52.2) (a)“ — BERICHTIGT durch R69 (c) | Zeile = 11298 | keine | nach der Marke zur zweiten Zeile (Reihenfolge der Tabelle), vor 11301 | wie oben |
| 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse — BERICHTIGT durch R71, ERGÄNZT durch R72 | Kopfzeile 3957; Blockzitat 3959–3964; berichtigter Satz 3959 bis Mitte 3960 | keine | **3964** | Leerzeile 3965, dann 3966 „**`handelstage`** bleibt unverändert …“ |
| 27 — ERGÄNZT durch R73 | Abschnitt 5124–5198; Registertext 5139–5152; 27.8 Tabelle 5184–5188 | 5154/5155 „27.3 ERGÄNZT durch R31 (47.14)“ (unter dem Blockzitat 27.1–27.5); mit „⭐“ beginnen ausserdem drei Textabsätze, die keine Marken dieser Bauart sind: 5126 „Neuer Registertext, keine Berichtigung.“, 5159 „Die Protokollkette beginnt nicht mit 21d …“, 5178 „Daraus ist 27.5 entstanden.“; am Abschnittsende: 5190/5191 „Messungen auf dem Selektionsraum nach dem Tag: siehe 45.6/45.7 …“ (Schluss „Abschnitt 27 oben bleibt zeichengleich.“); 5193/5194 „Abschnitt 27 ERGÄNZT durch R32 (47.15)“; 5196/5197 „Abschnitt 27 ERGÄNZT durch R56 (51.1)“ | **5197** | Leerzeile 5198, „---“ 5199 |

Anmerkung zu 23.3: Der Registertext 3b (c) selbst ist das Blockzitat Z. 3928–3939 (keine Marke; danach Z. 3941 „⭐ Geschlossen in TB-71 …“, erläuternder Absatz, keine Marke). R70 (c) nennt ihn nicht. Nach R65 (a) wäre zu fragen, ob R72 (b) („Benchmark-Tag … im Sinn von 23.3“) dem Satz „an genau den Tagen definiert …“ eine Bedeutung gibt und dort eine eigene Marke verlangt (dann nach Z. 3939). Das entscheidet Fable.

Ohne Marke nach R70: 7 (c) (Z. 807, 827–834), 17.5 (Z. 2818–2847), 50.7 Nr. 3 (Z. 11150), 24.2, 29.3 — nur Indexzeilen.

### Die zwei Vorbilder

1. **Marke zu einer Tabellenzeile** — REG Z. 10998–10999, direkt nach der Tabelle von 50.1 (Tabelle 10979–10996, Leerzeile 10997), vor „### 50.2“ (Z. 11001):
   `> ⭐ **50.1, Zeile R48 (d) ERGÄNZT durch R60 (51.5) und 51.8** (Fable 01a R60, Unterpunkt (d), nachgetragen nach Fable 02a R65 (b), TB-130, 02.10.2026).`
   `> Eintrag und Stand oben bleiben zeichengleich.`
   Die Zeile wird im fetten Teil mit „<Abschnitt>, Zeile <erste Zelle>“ benannt; die Tabelle selbst bleibt unberührt.
2. **Marke zu Abschnitt 27** — REG Z. 5196–5197, am Ende des Abschnitts nach der Tabelle 27.8 und nach den älteren Marken, vor „---“ (Z. 5199):
   `> ⭐ **Abschnitt 27 ERGÄNZT durch R56 (51.1)** (Fable 01a R56, zu 27.4 und 27.6, TB-129, 02.10.2026).`
   `> Eintrag und Stand oben bleiben zeichengleich.`
   R61 (b) schrieb dazu nur „27 — ERGÄNZT durch R56“; gesetzt wurde „Abschnitt 27 …“ mit dem Bezug in der Klammer.

Dazu, für 48.7: Vorbild einer Bestätigung — REG Z. 11128: `> ⭐ **50.4, Schlusssatz ERGÄNZT durch R57 (51.2): der Schlusssatz ist bestätigt** (Fable 01a R57, nachgetragen nach Fable 02a R65 (b), TB-130, 02.10.2026).`

---

## Nicht geprüft

- Kein Code (`auswertung.py`, `kennzahlen.py`, `benchmark.py`, Erzeuger, `mtm_kern.py`). Alle Tatsachen der Blöcke über Code und alle „Voraussetzung, zu messen“ sind offen: R66 (b), (c), (d) (DSR-Eingaben aus den Renditen der Beta-Bereinigung), (f); R69 (Teil 0 Nr. 1); R71 und R72 (Probe pandas 2.3.3 / 3.0.5, Bestand vom 02.10.2026).
- Teil 0, Teil 1, Leseprotokoll, Ampel und „Unsicher“ der Antwort: gelesen, aber nicht Stelle für Stelle gemessen. Die Anführungen in Teil 1 (R50, 16.6, 23.4, 17.5) sind dieselben wie in den Blöcken.
- Die Messungen des steuernden Chats zur Anfrage 02.10.c und die Leseprotokolle 02b/02c, auf die die Quellenzeilen verweisen.
- Fables Rechnung zur Richtung der Wirkung (R66, Quelle).
- „Umzugsschwelle“ (R73): 0 Treffer im Register; die Regel steht ausserhalb (nicht nachgeschlagen). `REGISTER_INDEX.md`, `ARBEITSWEISE.md`, `FABLE_DIALOG_INDEX.md` nicht gelesen.
- 25c (1) am Ursprung (42.3), 41.3 C1–C3, 21.4, 40.7, 10.1 im Wortlaut.
- Nichts unter `ergebnisse/`, keine Trade-Listen, kein `BACKLOG*.md`. Beim Lesen von 15.5, 23.4, 24.6 und 27 (Z. 5152) standen Zählungen und Grössen nach 27.1 im Ausschnitt; hier nicht wiedergegeben und nicht verwendet.

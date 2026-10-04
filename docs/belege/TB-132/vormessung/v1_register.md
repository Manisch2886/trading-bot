# TB-132 · V1 · Prüfung der Fable-Antwort 02.10.b gegen den Registerwortlaut

Prüfhelfer, nur lesend. Stand Register: `docs/VORREGISTRIERUNG_neuselektion.md`, 11 313 Zeilen, sha256 `a749678043f3…` (wie in Fables Leseprotokoll). Gelesen mit Skripten: Überschriften, Zeilen nach Nummer, in langen Zeilen Ausschnitte bis 400 Zeichen; Zitatsuche auf einem normalisierten Strom (Blockzitat-Präfix, `**`, Backticks und Zeilenumbrüche entfernt). „REG Z. n“ ist die Zeile im Register, in der die Fundstelle beginnt.

Nebenprüfung: Die Abschnittskopien 15, 16, 23, 24, 29, 34, 35, 37, 40, 48–52 in `ablage_tb130/` sind ab der Abschnittsüberschrift zeilengleich mit dem Register (14 von 14 geprüft). Was Fable aus den Kopien gelesen hat, ist also der Registertext.

---

## A. Zitate und Verweise (Teil 1 und „Quelle des Grundes“ R66–R71)

Urteil: **T** = trifft · **S** = trifft sinngemäss · **N** = trifft nicht.

| # | Stelle bei Fable | REG Z. | Wortlaut im Register (gekürzt) | Urteil |
|---|---|---|---|---|
| 1 | 1c „aus den täglichen Netto-Renditen des Kapitalpfads“, je Falte, ohne Einschränkung (Frage 1 (b) Nr. 1; R66) | 1439–1444 | „Der Falten-Sharpe wird für jeden Parametersatz in jeder Falte aus den täglichen Netto-Renditen des Kapitalpfads gerechnet, unabhängig von der Anzahl Trades.“ | T. Zusatz, den Fable nicht anführt: Formelzeile Z. 1449–1450 „…der täglichen Netto-Renditen der Falte × √252 (Krypto: √365 auf Kalendertagen)“ stützt R66 (b). |
| 2 | 1a „Flache Tage stehen mit Rendite 0 in der Reihe“ (R66) | 1432 | zeichengleich | T. „Exposure 0“ in R66 (a) steht nicht in 1a; Zusatz Fables. |
| 3 | 2a „Jeder Handelstag gehört zu der Falte, in die sein Datum fällt“ (R66) | 1475–1476 | zeichengleich | T |
| 4 | 29.3 (Kapitalpfad beginnt am 1. Januar der ersten Selektionsfalte) | 5384 | „Der Kapitalpfad eines Bots beginnt am 1. Januar seiner ersten Selektionsfalte mit dem registrierten Startkapital und ohne offene Position. Kein Einstieg liegt vor diesem Datum.“ | T |
| 5 | 3a „Symbole ohne Historie in einer Falte tragen 0 Trades und 0 Rendite bei“ | 1550–1551 | zeichengleich (15.5 (a), letzter Satz) | T. 15.5 (a) trägt keine ERSETZT-Marke; 16.7 „die Fassung in 15.5 bleibt stehen“ (Z. 2346). |
| 6 | 15.5, Lesart A „trägt für diese Tage 0 bei“ | 1628–1632 | „…das Symbol handelt dort ein paar Tage später und trägt für diese Tage 0 bei, genau wie es der nächste Satz von 3a vorschreibt.“ | T im Wortlaut. Rand: Lesart A ist Erläuterung (kein Blockzitat); die Tabellen von 15.5 sind durch 16.1.1 ersetzt (Z. 1600, 1865), für die Faltenzählung gilt Lesart H (16.2, Z. 1968). Der angeführte Satz ist davon nicht berührt. |
| 7 | 5.1 Nr. 8 (kein Trade ⇒ Sharpe 0) | 649 | „Falten ohne Trade zählen mit Sharpe 0.“ (602–603: Nr. 8 unberührt, 1c schärft nach) | T |
| 8 | Tatsachennotiz zu 1c (kein Trade: Sharpe 0; „Nichtteilnahme ist in der Selektionsstatistik ein Wert“) (R66) | 1452–1458; 1460–1465 | Notiz: 1c ist „die Schärfung von Regel 5.1 Nr. 8“. Das Wort „Wert“ steht nicht in der Notiz, sondern in der Marke darunter: „1c und 5.1 Nr. 8 machen ‚keine Trades‘ zu einem Wert, der in die Statistik eingeht“ (43-7). | S. Ort ungenau; und der Registersatz meint Falten/Läufe ohne Trades, nicht einzelne Tage ohne Benchmark — die Übertragung ist Fables Schluss. |
| 9 | 23.3: zweite Fassung band den Benchmark an einen Kalender des Kapitalpfads, „den es nicht gibt“ | 3947–3949 | „Seine zweite Fassung band den Benchmark an den Kalender des Bot-Kapitalpfades — den es nicht gibt: der Pfad ist ereignisindiziert“ | T |
| 10 | 15.4, Anmerkung 1 (Krypto Kalendertage) (Frage 1 (a); R66 (a)) | 1514–1515 | „‚Handelstage‘ heisst bei Krypto Kalendertage — der Markt läuft durch.“ | T. Ort: Anmerkung zur Embargo-Tabelle (Tatsachennotiz zu 2d). |
| 11 | 23.2, Grund 2 (Alpha aus dem Vergleich zweier Reihen) | 3908 | „Unter VH erzeugt Rang 3 Alpha aus Nichtteilnahme. Benchmark −88 %, Bot ≈ 0 ⇒ … daraus, dass der Bot nichts halten konnte.“ | T (Deutung, kein Zitat) |
| 12 | 24.1 (Bewertungsachse) | 4275–4277 | „…gilt dann auf der Symbol- und Zeitachse, aber nicht auf der Bewertungsachse.“ | T |
| 13 | 24.2 (Zeitachse für den Drawdown) | 4303–4307; 4309–4311 | „…auf denselben Tagen wie der Benchmark (3b (c))“; „Er legt die Bewertungsachse fest … und die Zeitachse“ | T |
| 14 | 23.4, Wirkung 3: „Ein Tag mit Rendite 0 bewegt den Pfad nicht“ | 4065 | „Ein Tag mit Rendite 0 bewegt den Kapitalpfad nicht; das ist der Grund, kein Zufall.“ | T |
| 15 | 23.4, Wirkung 3: vier Falten, je ein Tag; „der Tag des ersten Kurses, an dem noch keine Rendite vorliegt“ (Frage 6; R71) | 4061 | „C_lit … 4 Falten um je +1: [vier Bot-Falten] (der Tag des ersten Kurses, an dem noch keine Rendite vorliegt)“ | T. Die vier Falten sind die ersten Falten von vier Krypto-Bots; passt zu „einmal je Bot“. Stützend Z. 4067–4068: „Tage vor dem ersten Handelbar-Tag eines Bots stehen gar nicht darin“. |
| 16 | 23.5 „die erste Tagesrendite eines Symbols ist die vom Handelbar-Tag auf den Folgetag“ (R71) | 4079 | zeichengleich | T |
| 17 | 23.5 (ein Name, der etwas anderes verspricht als **der Inhalt**) (R69) | 4082 | „Dieselbe Fehlerklasse wie K1h und T44.10 — ein Name, der etwas anderes verspricht als **das Verhalten**.“ | S, Wortlaut weicht ab. Dort geht es um einen Docstring („Buy-and-Hold“), nicht um einen Dateinamen. In R69 „als das Verhalten“ schreiben oder die Klammer als eigene Worte kennzeichnen. |
| 18 | 24.3 (Bauart; „Bekannte Richtung der Wirkung, nicht Grund“) | 4327–4330; 4257; 11277 | „…die Grösse der Abweichung … wird gemessen und berichtet und ist für die Entscheidung ohne Belang.“ Kopf 24: „Die Richtung der Wirkung ist bekannt …; ihre Grösse ist nicht gemessen“. Gleiche Formel in R64. | T |
| 19 | „Das ist die Stelle, an der 23.2 Rauschen erwartet“ (Frage 1 (b), Berater-Absatz) | 3907 | „…die dünnen Falten sind genau die, in denen 3b (d) Rauschen erwartet“ | S. Die Erwartung schreibt 23.2 (Grund 1) dem Text 3b (d) zu (16.7 (d), Z. 2399), und sie gilt dünnen Falten (wenige Symbole), nicht Falten mit wenigen Benchmark-Tagen. Ohne Gewicht für die Entscheidung. |
| 20 | 7 (c), Präzisierungen: „gemeinsame Tage“, „über dieselben Tage“ (R70 (a); R66 (c)) | 829–831; 832–834 | „Beide Reihen werden auf gemeinsame Tage gebracht“; „…mittleren Exposure des Gewinners über dieselben Tage“ | T |
| 21 | 8.1 (Zufalls-Timing steht auf den Benchmark-Tagen) (R66 (c)) | 902–907; 10885 | 8.1: „…zyklisch verschoben und auf die Benchmark-Tagesrenditen gelegt“. Die Tage nennt erst R48 (g): „über die aneinandergehängten Selektionsfalten (dieselben Tage wie 7 (c))“. | S (der Tagebezug steht in R48 (g), nicht in 8.1) |
| 22 | R33 „Eine fehlende Zeile ist ein Befund über den Erzeuger, kein Ausgang“; „nie nichts“ (R67) | 10773 | zeichengleich (auch schon 45.5, R5 (b), Z. 10236) | T |
| 23 | R33 in Frage 2: „ein Mangel der Datei ist ein Befund über den Erzeuger“ | 10773 | R33 spricht nur von der fehlenden Zeile | S (Verallgemeinerung; im Block korrekt als „Bauart R33“) |
| 24 | R33: genau eine Zeile je Zelle und Falte, Bestätigungsperiode eingeschlossen (R68) | 10773–10774 | „…für jede Zelle des Rasters und jede Falte des Faltenplans des Bots — Selektionsfalten und Bestätigungsperiode (35.1) — genau eine Zeile“ | T |
| 25 | R39: Feldliste ist Registertext (Frage 2; R67) | 10815 | „Die Feldliste jeder dieser Dateien ist Registertext (Bauart 33.3, 41.1 A12)“ | T |
| 26 | R39 mit Grund (23.3: Symbole, die der Loader des Bots handelbar macht; 16.7 (b): Schranken je Bot; 37.5 (2)) (R69) | 10815–10816 | „Die Benchmark-Tagesreihe ist je Bot, nicht je Markt (23.3: Symbole, die der Loader des Bots handelbar macht; 16.7 (b): Schranken je Bot); ‚benchmark_tagesreihen/<markt>.csv‘ im Vertrag lies ‚<bot>.csv‘.“ Quelle: „23.3, 16.7 (b), 37.5 (2) (ein Wert, ein Ort) …“ | T. Rand: 16.7 (b) (Z. 2355–2365) führt für die vier Aktien-Bots denselben Wert; verschieden sind die Schranken bei Krypto (drei Werte, zwei Einheiten). Für „eine Datei je Markt kann sie nicht tragen“ reicht das. |
| 27 | 37.5 (2) (nach R39: „ein Wert, ein Ort“) | 7143 | „Der Laufpfad … liest registrierte Werte ausschliesslich aus diesem Modul — kein Laufmodul trägt eine eigene Kopie.“ | S (37.5 spricht von registrierten Zahlenwerten in Modulen; die Kurzform stammt aus R39) |
| 28 | R46 (Abnahme, ganze Kette) | 10864 | „…durch die ganze Kette bis auswertung.py und Bericht …“ | T |
| 29 | R37 „für jede Zelle“ / „Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle“ (Frage 3; R68) | 10801 | „Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle (bestaetigung_ab_effektiv, R34); auswertung.py nimmt den Wert der Gewinnerzelle (41.3 C3).“ | T |
| 30 | R37 (i): Bestätigungsstatistik des Gewinners (R68 (a)) | 10801 | „Die Bestätigungsstatistik des Gewinners beginnt am ersten Handelstag ab Beginn der Spanne, an dem keine vor der Spanne eröffnete simulierte Position des Gewinners mehr offen ist; Deckel je Bot nach 16.6/41.3 C2“ | T |
| 31 | 35.1 (Spanne; Ende der Bestätigungsperiode) (Frage 3; R66 (a); R68 (a)) | 6351 | „…die Datumsspanne von ‚Bestätigung ab‘ (21.4) bis zum Go-Live-Schnitt (5.2), Ende ausschliesslich.“ | T |
| 32 | 2d (15.4 (d)) „Tage im Embargo gehören zu keiner Periode“ (R68, Voraussetzung und Quelle) | 1487–1488; 1490–1493 | Wortlaut zeichengleich. Direkt darunter: „ERSETZT durch Abschnitt 16 …, 16.6.“ | **N als geltender Text** — siehe B1. |
| 33 | R60 (c) „eine Rechnung“: Exposure und Rendite im Deckelfall (Frage 3; R68 (c): „beide kommen aus einer Rechnung (R60 (c))“) | 11196 | „Der Zellen-Erzeuger schreibt beide Träger aus einer Rechnung: mittlere_exposure in zellen.csv ist je (Zelle, Falte) das Mittel der Spalte exposure der Tagesreihe dieser Zelle“ | **N als Beleg.** „Beide“ sind in R60 (c) die zwei Träger der mittleren Exposure (zellen.csv und Tagesreihe), nicht Rendite und Exposure. R68 (c) kann R60 (c) nur als Bauart anführen; der Satz selbst ist neu. |
| 34 | „Dafür“ in R60 (c) (R69 (c)) | 11196 | „Die Abnahme nach R46 prüft diese Gleichheit, mit Gegenprobe. auswertung.py wird dafür nicht geöffnet.“ | T |
| 35 | R64 (e) „auswertung.py wird für nichts davon geöffnet“ / „Für nichts davon“ (Frage 4; R69 (c)) | 11276 | „(e) Welche Tage die Tagesreihe über die Tage nach (a) hinaus führt, legt dieser Block nicht fest. auswertung.py wird für nichts davon geöffnet.“ | T |
| 36 | „52.4 liest den Satz zu weit“ | 11298 | Zeile R64 (52.2) (a): „Wann der Code den Namen je Bot liest, ist nicht festgelegt; auswertung.py wird nach R64 (e) nicht geöffnet (52.5)“ | T (so steht es dort) |
| 37 | R64 (a) nennt 7 (c) als Geltungsbereich; „lies“ gilt R48 (d) und R60 (c); (b) bestätigt den Code (Frage 5; R70 (a)) | 11276 | (a) „‚Handelstage des Zeitraums‘ in R48 (d) lies …“; „Das gilt für … (4.2) und für die des Gewinners über seine Selektionsfalten (7 (c))“; (b) „… ist die Regel aus Abschnitt 7 … und kein Register-Code-Widerspruch“; (d) „… in R60 (c) lies …“ | T |
| 38 | R64 (c) (Bauart: Wache, Ausgang 2, Abnahme mit Gegenprobe) (R67) | 11276 | „…ist ein Befund über den Erzeuger, kein Ausgang (Bauart R33). Der Zellen-Erzeuger prüft im Lauf …, und endet sonst mit 2. Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe“ | T |
| 39 | Messung in 52.4 (auswertung.py behandelt und prüft weder fehlende Werte noch doppelte Daten) (R67) | 11296; 11309 | „Fehlende Werte und doppelte Daten werden dort weder behandelt noch geprüft“ — „dort“ = lies_tagesreihe, lies_benchmark, beta_bereinigung | S (gemessen für diese drei Funktionen, nicht für die ganze Datei) |
| 40 | 25c (1) (Register-Code-Widerspruch) (Frage 4; R66 (e); R69 (a)) | 9262 (42.3, F1 (a)); 10920; 11196; 11269 | Ursprung: „Ein nicht leerer _bedingung-Text, den der Code nicht als Rasterbedingung erkennt, ist ein Widerspruch zwischen Register und Code und endet mit 2“. Die Form „wird gemeldet, nicht eingetragen“ steht erst in R50, R60, R63. | S (Fable folgt der Wiedergabe der späteren Blöcke; der Ursprungssatz regelt einen Einzelfall mit Ausgang 2) |
| 41 | 37.3 (beauftragte Änderung, Einzelfreigabe, Hash-Übergang, neues Abbild) (R69 (b)) | 6977 | „Ein Befund 1 … vor dem signierten Tag ist zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz); er wird durch ein neues Abbild unter neuem Namen geschlossen“ | S („Einzelfreigabe des Betreibers“ steht nicht in 37.3; dort „Freigabe“) |
| 42 | 40.7 (Nachweis mit Gegenprobe) (R69 (b)) | 8414 | „Jede Mutationsprobe hat eine Gegenprobe, die zeigt, dass sie rot werden kann … Eine Mutationsprobe ohne Gegenprobe zählt nicht als Prüfung.“ | S (40.7 gilt Mutationsproben; „Nachweis mit Gegenprobe“ ist die Bauart, wie in R55 und R64) |
| 43 | R45 (Bauart einer beauftragten Änderung) | 10857 | „Beauftragte Änderung nach 37.3 mit Nachweis in der Bauart von 10.1 …; Mutationsprobe …; Hash-Übergang Punkt 10, neues Abbild.“ | T |
| 44 | R36 (zwei Drawdown-Spalten, Nachrechnung mit Ausgang 2; auf den Tagen des Benchmarks) (Frage 4; R66 (c); R69 (b)) | 10794 | „…kapital_drawdown_mtm_pct — … auf den Tagen des Benchmarks (3b (c)) — und kapital_drawdown_ereignis_pct …“; „auswertung.py rechnet kapital_drawdown_mtm_pct aus tagesreihen/<zelle>.csv nach und endet bei Abweichung mit 2.“ | T |
| 45 | R34 (zellenbericht.csv) | 10780 | „Der Zellen-Erzeuger schreibt je Bot eine Datei zellenbericht.csv …; auswertung.py liest die Zeile des Plateau-Gewinners und berichtet sie“ | T |
| 46 | R55 („nächste planmässige Öffnung“; Umbenennung) | 10968 | „…ist ein Name, keine Regel; Umbenennung mit der nächsten planmässigen Öffnung.“ | S (gebeugt; im Nominativ steht die Wendung in Z. 9802) |
| 47 | 50.1 und 50.2 (Stand des Vertrags) (R69) | 10985; 11034–11040 | 50.1, Zeile R36: „Der Vertrag führt heute nur kapital_drawdown_pct; die zwei Spalten nach R36 kommen mit dem Zellen-Erzeuger“. 50.2: Vertrag nennt `<wurzel>/benchmark_tagesreihen/<markt>.csv`; „im Zitat lies ‚<bot>.csv‘ (R39)“. | T. Rand zu „Unsicher“ 6: `bestaetigung_ab_effektiv` kommt in Abschnitt 50 nicht vor (kein Treffer); 50.1 belegt nur die Drawdown-Spalte. |
| 48 | R61 (b), erster und zweiter Satz; „R54 an 7 (c)“ (Frage 5; R70) | 11209 | „Eine Marke steht dort, wo ein Block dem Wortlaut eines Ortes eine Bedeutung gibt oder ihm etwas hinzufügt (34). Keine Marke erhält ein Ort, der nur Quelle des Grundes, Statusliste, Plan oder Code ist, der im erzeugten Block liegt oder in Abschnitt 10.“ … „Ohne Marke bleiben, vom Index geführt: R27, R28, R30, R54 an 7 (c), …“ | T für die Fundstellen. S für den Grund: „Geltungsbereich“ steht in R61 (b) nicht; R61 (b) führt „R54 an 7 (c)“ ohne Begründung. R54 (Z. 10961) nennt 7 (c) tatsächlich nur als Reichweite („über die Selektionsfalten (7 (c))“). Der allgemeine Satz in R70 (a) ist neu (siehe Vorschlag V2). |
| 49 | R65 (a) | 11283 | „Gibt ein Block einem benannten Ort ein ‚lies‘, eine Ergänzung oder eine Bestätigung, trägt der Ort die Marke, auch wenn die Aufzählung des Blocks ihn nicht nennt; ausgenommen bleiben die Orte nach R61 (b), zweiter Satz. Eine Tabelle von Befunden ist keine Statusliste …, soweit ein Block den Befund einer Zeile ergänzt oder berichtigt. Eine Bestätigung trägt das Markenwort ERGÄNZT mit dem Zusatz, was bestätigt ist“ | T |
| 50 | 34.3 „direkt unter dem berichtigten Satz“ (R70 (c)) | 6130; 6204 | Die Wendung steht im Kopf von 34 (Z. 6128–6131). 34.3 selbst: „…trägt die Marke direkt unter 30.2 (2)“. | S (Wiedergabe aus R65, Z. 11284; Fable weist das aus) |
| 51 | 4.2 trägt die Marke zu R64; Wortlaut nennt die Tage nicht | 486–491; 528–529 | Marke „4.2 PRÄZISIERT durch R64 (52.2) … Unterpunkt (a)“ steht; 4.2 nennt keine Tage | T |
| 52 | R71, alter Satz: „Die Umsetzung lässt den ersten Kurstag je Falte aus, weil pct_change dort keine Rendite liefert“ | 3959–3960 | zeichengleich bis auf die Backticks um `pct_change` und den Zeilenumbruch nach „dort“ | T |
| 53 | R71: „Höchstens ein Tag je Falte“ | 3960–3961 | „Abweichung gegenüber dem Satz: höchstens ein Tag je Falte.“ | S (im Register klein, mitten im Satz, über einen Zeilenumbruch; als wörtliche Anführung im Registertext nicht zeichengleich) |
| 54 | R66 (d), R64: „Tatsachennotiz zu 23.3“ | 3957 | Überschrift: „Tatsachennotiz zu 3b (c), Satz zur Zeitachse (TB-71, 20.09.2026)“ in 23.3 | S (R70 (c) und R71 benennen sie richtig) |
| 55 | 16.7 (b) (Schranken je Bot) | 2352–2365 | „MIN_HISTORY_* ist je Bot mit seinem Namen und seiner Einheit fest auf dem heutigen Wert“ | T |
| 56 | 23.3 (Symbole, die der Loader des Bots handelbar macht) | 3930–3931 | „…aus den Symbolen gebildet, die der Loader des Bots an diesem Tag handelbar macht“ | T |

Nicht glatt: Nr. 8, 17, 19, 21, 23, 27, 32, 33, 39, 40, 41, 42, 46, 48 (Grund), 50, 53, 54. Sachlich erheblich sind Nr. 32 und 33; Wortlaut zu berichtigen in Nr. 17 und 53.

---

## B. Voraussetzungen am Register

### B1 (R68) — 16.6 und der Satz aus 2d

- 15.4 (d), REG Z. 1485–1488: „Die Bestätigungsperiode beginnt am Go-Live-Tag plus Embargo; Embargo = längste Zeitbremse des Bots in Handelstagen plus 1 (…). Tage im Embargo gehören zu keiner Periode.“
- Marke direkt darunter, Z. 1490–1493: „ERSETZT durch Abschnitt 16 (Registernachtrag TB-41, 16.09.2026), 16.6. Das Embargo ist dort keine feste Frist mehr, sondern eine Bedingung am Positionsbestand mit dieser Frist als Deckel.“
- 16.6, Überschrift Z. 2294: „Registertext 2d — Embargo (ersetzt die Fassung aus 15.4 vollständig)“. Neuer Text Z. 2296–2306: „Die Bestätigungsperiode eines Bots beginnt am ersten Handelstag nach Go-Live, an dem keine vor Go-Live eröffnete Position dieses Bots mehr offen ist. … Ist am Deckeltag noch eine vor Go-Live eröffnete Position offen, beginnt die Bestätigungsperiode trotzdem — diese Position wird in der Bestätigungsstatistik jedoch nicht gezählt“. Der Satz „Tage im Embargo …“ steht im neuen Text nicht.
- 16.6, Z. 2308–2310: „Was sich gegenüber 15.4 ändert: Das Embargo war dort eine feste Frist (Zeitbremse + 1, Tage im Embargo gehören zu keiner Periode). Jetzt ist es eine Bedingung am Bestand mit der alten Frist als Deckel.“

Befund: 16.6 ersetzt 15.4 (d) vollständig, wiederholt den Satz nicht und führt ihn in der Vergangenheitsform als Merkmal der alten Fassung. Die Voraussetzung „dass 16.6 den Satz nicht aufhebt“ trifft so nicht zu. Der Satz kommt im Register nur an diesen zwei Stellen vor.

Was R68 (a) trägt, ohne 2d: R37 (i), Z. 10801 — „Die Bestätigungsstatistik des Gewinners beginnt am ersten Handelstag ab Beginn der Spanne, an dem keine vor der Spanne eröffnete simulierte Position … mehr offen ist“. Danach liegen die Tage davor in der Spanne (35.1), aber vor der Statistik; genau das sagt R68 (a) („gehören zu keiner Statistik“). R37 (ii) ordnet den Wortlaut „15.4 2d (‚Go-Live-Tag plus Embargo‘)“ ausserdem der Bestätigungsperiode der Leiter (Papierpfad) zu. Folge: in R68 die Voraussetzung und die Quelle „2d (15.4 (d))“ auf R37 (i) / 16.6 umstellen; das entscheidet Fable.

### B2 („Unsicher“ 2) — Falten mit teilweisem Benchmark

Ja. Faltenplan 33.2, Tabelle Z. 5972–5976; die Tage stehen in 23.4, Wirkung 1 und 3 (Z. 4009–4014, 4061–4062), dazu 21 (Z. 3416) und 25.2 (Z. 4643):

| Bot | Falte (33.2) | Art |
|---|---|---|
| `turtle_soup_crypto` | 2018 (erste Falte) | erstes Symbol erst am 30.12.2018 handelbar; Benchmark an einem Tag der Falte definiert |
| `volatility_breakout_crypto` | 2018 (erste Falte) | ebenso |
| `elliott_wave` | 2018–2019 (erste Falte) | Benchmark an 133 von 730 Tagen |
| `t3_supertrend` | 2019 (erste Falte) | erstes Symbol am 17.08.2019 handelbar; Benchmark an 136 von 365 Tagen |

Nicht betroffen: `rsi2_crypto` (erste Falte 2019, erster Handelbar-Tag davor) und die vier Aktien-Bots (23.4, Z. 4064–4065: keine Abweichung, auch nicht in `handelstage`). Z. 6009–6016 bestätigt, dass die Benchmark-Tabelle genau die Falten aus 33.2 führt. Der Fall, den R66 regelt, tritt also in vier Falten von vier Bots ein. Abschnitt 25 fügt keinen weiteren Fall hinzu (25.2: `t3_supertrend` beginnt 2019, die leere Falte 2018 entfällt).

### B3 (R66 (a)) — Handelskalender der Aktien

Kein Registersatz legt den Kalender der Aktien-Tagesreihe oder „Handelstag“ für Aktien fest. „Börsentag“: 0 Treffer. „Handelstag“ 34, „Kurstag“ 13, „Kalendertag“ 7 Treffer; einschlägig sind nur:

- Z. 1514–1515 (15.4, Anmerkung 1): nur Krypto.
- Z. 1449–1450 (15.3, Formelzeile): „× √252 (Krypto: √365 auf Kalendertagen)“ — setzt für Aktien Handelstage voraus, nennt keinen Kalender.
- Z. 1523–1525 (15.4, Anmerkung 3): 130 Kalendertage „an der Kursreihe nachgemessen 89 Handelstage (…, Feiertage eingerechnet)“ — Messung an der Kursreihe, keine Regel.
- **Z. 2826–2829 (17.5, Registertext 5f, Tatsachennotiz im Blockzitat): „Der Handelskalender kommt nicht aus einer Datei, sondern aus dem Paket pandas_market_calendars (gemessen TB-47: Fassung 4.6.1 auf dem Betriebsrechner). Er ist damit Umgebung, nicht Eingabe, und liegt im Lock.“** Das Register kennt also schon einen Handelskalender mit anderer Quelle als dem Snapshot. R66 (a) („Kurstage des Marktes im Snapshot“) nennt eine zweite Quelle; ob beide dieselben Tage liefern und welcher Code den Paket-Kalender benutzt, ist zu messen.
- Z. 4470 (24.6): die TB-73-Messung rechnete „an jedem Kurstag der 1d-Dateien“ — Vorbild für R66 (a), aber Tatsachennotiz zu einem Forschungsskript.
- Z. 4066–4068 (23.4): der Benchmark-Rahmen „kennt nur Tage, an denen mindestens ein Symbol einen Kurs hat“.
- Z. 3966–3967: „`handelstage` bleibt unverändert die W-Spalte — die Länge des gemeinsamen Kalenders.“

### B4 — Wortlaut 3a

15.5 (a), REG Z. 1547–1551: „Das Universum je Bot ist seine heutige Symbolliste (Datei und Hash im Register). Je Selektionsfalte werden die Symbole dieser Liste ausgewertet, für die am 1. Januar der Falte Kursdaten einschliesslich Indikator-Vorlauf vorliegen. Symbole ohne Historie in einer Falte tragen 0 Trades und 0 Rendite bei.“ Die Dateien: Tatsachennotiz zu 3a, Z. 1570–1575 (`config/top25_symbols.txt`, `config/sp500_top150.txt`, je mit Hash), Korrektur der Krypto-Klammer Z. 1577–1580 (16.1.3), Z. 1582–1584 („zwei Universen, nicht neun“). Für R66 (a) heisst das: „Universumsdatei des Bots (3a)“ ist bei den vier Aktien-Bots dieselbe Datei.

---

## C. Orte für Marken nach R70 (c)

Marken stehen als Blockzitat-Zeile „> ⭐ …“ mit Folgezeile „> Eintrag und Stand oben bleiben zeichengleich.“ und je einer Leerzeile davor und danach.

| Ort | Blockzitat REG Z. | vorhandene Marken (REG Z.) | neue Marke nach Z. | danach folgt |
|---|---|---|---|---|
| 15.3 (c) — R66 | 1430–1444, (c) = 1439–1444 | 1446/1447 „15.3 (b) ERGÄNZT durch R41 (48.9)“. Weiter unten: 1460–1465 Folge-Marke 43-7 (andere Bauart, ohne die Folgezeile); 1467/1468 „15.3 ERGÄNZT durch R35 (48.3)“ | 1447 (hinter der R41-Marke, erste Gruppe direkt unter dem Blockzitat) | Leerzeile 1448, dann 1449 „*Formel für den Falten-Sharpe: …“. Zweite mögliche Stelle: nach 1468, vor „---“ (Z. 1470); dort steht bisher nur die Marke für 15.3 als Ganzes. |
| 52.2 (R64) — R66, R68, R69 (c) | 11276–11277 | keine | 11277 | Leerzeile 11278, dann 11279 „**Kette:** Marken: 4.2; 48.16 (R48); 51.5 (R60). …“ |
| 48.5 (R37) — R68 | 10801–10802 | keine | 10802 | Leerzeile 10803, dann 10804 „**Kette:** Marken: 5.1, Nr. 7; 16.4 (c); 16.4 (d); 16.6; 35.1.“ |
| 48.7 (R39) — R67, R69 | 10815–10816 | keine | 10816 | Leerzeile 10817, dann 10818 „**Kette:** Marken: 46.3. Feldliste: 50.2.“ |
| 51.5 (R60) — R69 (c) | 11196–11197 | 11199/11200 „51.5 R60 (a) PRÄZISIERT durch R63 (52.1)“; 11202/11203 „51.5 R60 (b) und (c) PRÄZISIERT durch R64 (52.2)“ | 11203 | Leerzeile 11204, dann 11205 „**Kette:** Marken: 4.2; 48.16 (R48). …“ |
| 23.3, Tatsachennotiz zu 3b (c) — R71 | Kopfzeile 3957; Blockzitat 3959–3964; berichtigter Satz 3959 bis Mitte 3960 | keine | 3964 | Leerzeile 3965, dann 3966 „**`handelstage`** bleibt unverändert die **W-Spalte** …“ |

Zu 23.3: Der berichtigte Satz endet mitten in Z. 3960. „Direkt unter dem Satz“ ist ohne Bruch des Zitats nur direkt unter dem Blockzitat möglich. Vorbild: 25.2, Marke Z. 4655 direkt unter dem Absatz, vor der älteren Marke Z. 4658.

Zu 48.7: R69 löst „zugunsten von R39“ auf und berichtigt R39 nicht — das ist der Sache nach eine Bestätigung. Nach R65 (a), letzter Satz (Z. 11283), trägt eine Bestätigung „ERGÄNZT mit dem Zusatz, was bestätigt ist“. R70 (c) nennt für R69 an 48.7 keinen Zusatz.

### Zusatzvorschläge nach R65 (a) — streng

| # | Ort | REG Z. | Was gibt welcher Block | Dagegen | Gewicht |
|---|---|---|---|---|---|
| V1 | 52.4, Zeile „R64 (52.2) (a)“ | 11298 (Marke nach der Tabelle, nach Z. 11299, vor „### 52.5“ Z. 11301; Vorbild 50.1, Z. 10998) | R69 berichtigt und ergänzt den Befund der Zeile: „auswertung.py wird nach R64 (e) nicht geöffnet“ ist nach R69 (c) zu weit gelesen; „Wann der Code den Namen je Bot liest, ist nicht festgelegt“ beantwortet R69 (b). R65 (a), dritter Satz, trifft genau diesen Fall. | Der Block R69 nennt 52.4 nicht; nur Teil 1 der Antwort sagt „52.4 liest den Satz zu weit“. | stark |
| V2 | 52.3 (R65 (a)) und 51.6 (R61 (b)) | 11283; 11209 (Marken nach 11284 bzw. nach 11213, je vor „**Kette:**“) | R70 (a) fügt der Ausnahmeliste einen allgemeinen Fall hinzu („nur als Geltungsbereich … bleibt ohne Marke“). R65 (a) nennt als Ausnahmen nur „die Orte nach R61 (b), zweiter Satz“; dort steht „Geltungsbereich“ nicht. Wer R65 (a) liest, sieht die neue Ausnahme nicht. Vorbild: R65 trägt selbst Marken an 48.19 und 51.6. | R70 führt R61 (b) und R65 (a) nur als Quelle des Grundes und versteht sich als Anwendung eines entschiedenen Falls. | stark |
| V3 | 52.2 (R64), zusätzlich „durch R71“ (zu (a)) | 11276 | R71: „R64 (a) und R66 (d) meinen diesen Tag“ — gibt der Klammer „(erster Kurstag)“ in R64 (a) und der zweiten Voraussetzung ihre Bedeutung. | R64 (a) verweist nur auf die Notiz; deren Marke steht an 23.3. | mittel |
| V4 | 52.4, Zeile „R64 (52.2), zweite“ | 11297 | R66 (a) legt den Kalender der Tagesreihe fest, R66 (d) macht die Voraussetzung zur Wache im Lauf; die Zeile sagt „nicht entscheidbar: Den Kalender der Tagesreihe legt noch kein Code fest“. | Der Befund (kein Code) bleibt wahr; „offen (52.5)“ ist Statusangabe; R66 nennt 52.4 nicht. | mittel |
| V5 | 15.3: Marke auf (a) und (c) beziehen | 1430–1432 | R66 (a) gibt der „Reihe“ aus 1a ihren Kalender und dehnt „flache Tage“ auf die Tage vor dem ersten Handelbar-Tag aus. | Kopf von R66 nennt nur 1c; 1a steht als Quelle. Dieselbe Stelle, nur ein Wort mehr in der Marke. | mittel |
| V6 | 48.1 (R33) | 10773 (Marke nach 10774, vor „**Kette:**“ 10776) | R68 (a) sagt, was die Zeile der Bestätigungsperiode trägt und auf welchen Tagen. Nach Fables eigenem Massstab zu 4.2 („sein Wortlaut nennt die Tage nicht, R64 gibt sie ihm“) gälte das auch hier. | Kopf von R68 richtet die Präzisierung an R37 und R64; R33 wird als Gegenstand genannt, sein Satz (eine Zeile je Zelle und Falte) bleibt. | schwach bis mittel |

Verworfen:

- 15.4, Anmerkung 1 (Z. 1514): nur angeführt; auch R48 (d) hat dort keine Marke hinterlassen.
- 35.1 (Z. 6351): R68 (a) sagt ausdrücklich „bleibt, was 35.1 sagt“; die Kette läuft über die R37-Marke Z. 6419.
- 15.4 (d) / 16.6: keine Marke, sondern Berichtigung der Quelle in R68 (B1).
- 50.1, Zeile R36 (Z. 10985) und 50.2 (Z. 11040): nur Quelle des Grundes; 50.2 ist gemessenes Code-Zitat, die Kette von 48.7 verweist schon darauf.
- 52.4, Zeile „R64, erste“ (Z. 11296): R67 führt die Messung nur als Quelle des Grundes; der Befund bleibt.
- 52.5 (Z. 11305–11313): Statusliste.
- 24.2, 29.3, 8.1, 7 (c): wie R70 (c).
- 48.4 (R36), 48.2 (R34), 49.3 (R55), 48.13 (R45): in R69 (b) nur als Anlass der Öffnung genannt.

---

## Nicht geprüft

- Kein Code (`auswertung.py`, `kennzahlen.py`, `benchmark.py`, Erzeuger). Alle Voraussetzungen „zu messen“ am Code sind offen: R66 (a) zweiter Teil, R66 (e), R68 (kein Urteil liest die Exposure der Bestätigungsperiode), R69 (b), R71.
- Teil 0, Leseprotokoll, Ampel und „Unsicher“ nur, soweit oben genannt (27.4, R56 (b) nicht geprüft).
- `REGISTER_INDEX.md`, `ARBEITSWEISE.md`, die Anfrage 02.10.b, frühere Antworten.
- 41.3 C1–C3 und 21.4 im Wortlaut (nur über die Marken in 16.6 und 35.1 gesehen); 16.1.1.
- Ob Fables Rechnung zur Richtung der Wirkung (Sharpe über alle Tage dem Betrag nach nie grösser) stimmt.
- Nichts unter `ergebnisse/`, keine Trade-Listen, kein `BACKLOG*.md`. Beim Lesen von 15.4, 15.5, 23.4 standen Grössen nach 27.1 im Ausschnitt (Symbolzahlen, Benchmark-Drawdowns); hier nicht wiedergegeben und nicht verwendet.

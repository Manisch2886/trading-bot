# REGISTER-KOPIE Abschnitt 48 (von 0–51) — Register-Z. 10755–10923 — Commit f63ad4cbd1230427305a24ac3d7467b83f088fd2 — 2026-10-02 — Original sha256 7f74b0e5a746cbc720b7b7c20af83acddd32d6652c3b57099f18769d3d4b16c4 — KOPIE, nicht das Register

## 48. Fable 29b — Registerblock R33–R52 (TB-126)

Reines Eintragen von Registertext, Bauart wie 47. Quelle: `docs/projektfuehrung/FABLE_ANTWORT_2026-09-29b_sammlung_erzeuger_kalter_leser.md`, md5 `898d5bd53b6617209b7ce4f7e8992941`, 73 703 B, am Commit `0f56aeb`, Abschnitt „Registerblock … (ab R33)“, Z. 190–267. Übertragen wie 27c (47). Die Marken für Register 0–12 setzt dieser Abschnitt nach R51 (48.19); darunter steht **eine Marke in Abschnitt 9** (R48 (b)), die R51 ausdrücklich verlangt. Der Verweis aus R8 (d) in Register 9 (45.8) ist ein anderer und kommt weiter nach dem Tag; die Sätze „in 9 steht … keine Marke“ in 45.8 und 46.0 (und die Listen in 45.10, 46.10) beschreiben den damaligen Stand, ihr einziger Grund war dieser Verweis. Für R48, R49 und R50 stehen Marken an allen Orten, die der Unterpunkt nennt, und an denen der R51-Liste (Vereinigung). Für Abschnitt 10 und den vollen Datenstand-Hash (17.3, 17.9, 18) verlangt R51 Indexzeilen statt Marken.

### 48.1 R33 — Berichtigung zu 45.5 (b) (Zeilen in zellen.csv)

> R33 — Berichtigung zu 45.5 (b) (Zeilen in zellen.csv). „zellen.csv enthält für jede Zelle des Rasters genau eine Zeile; die Zeilenzahl ist gleich der Zahl der Zellen“ lies: „zellen.csv enthält für jede Zelle des Rasters und jede Falte des Faltenplans des Bots — Selektionsfalten und Bestätigungsperiode (35.1) — genau eine Zeile; die Zeilenzahl je Bot ist Zellen × (Selektionsfalten + 1). Eine (Zelle, Falte) ohne Trades trägt die Nullzeile: Trade-Zahl 0, Sharpe 0 nach 1c, Drawdown 0, nie nichts.“ Eine fehlende Zeile ist ein Befund über den Erzeuger, kein Ausgang. Es gibt keine Trade-Liste je Zelle als Rohergebnis; „leere Trade-Liste“ in 45.5 (b) und 43-7 bezeichnet den Fall „keine Trades gefunden“, dessen Ergebnis beim Listen-Erzeuger eine leere Liste und beim Zellen-Erzeuger die Nullzeile ist. F-1, F-2.
> Quelle des Grundes: Datenvertrag von auswertung.py (Sperrlistenpunkte 3/5/14; „genau eine Zeile je (Zelle x Falte), fuer ALLE Falten des Faltenplans, Bestaetigungsperiode eingeschlossen“), 15.3 (1c: Falten-Sharpe je Falte), 43-7. Der Vertrag stand vor R5 (b); R5 (b) war Kurzform ohne Nachlesen — elfter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt“. Kein Ergebnis.

**Kette:** Marken: 45.5, Block R5, Punkt (b). Voraussetzung gemessen: 50.1.

### 48.2 R34 — Ergänzung zu 22.2 und 45.5 (Zellenbericht)

> R34 — Ergänzung zu 22.2 und 45.5 (Zellenbericht). Der Zellen-Erzeuger schreibt je Bot eine Datei zellenbericht.csv mit genau einer Zeile je Zelle und den Feldern: die drei Werte aus 22.2 (Ertragsanteil der besten Selektionsfalte, des besten Symbols, der fünf besten Trades), haltedauer_median_handelstage (15.3 (b), R41) und bestaetigung_ab_effektiv (R37). Grundlage der drei Anteile: realisierte Erträge der ausgeführten Trades (Summe pnl_pct), Faltenzuordnung nach dem Einstiegstag (2b), nur Selektionsfalten; Anteil = Beitrag ÷ Gesamtertrag; bei Gesamtertrag ≤ 0 wird kein Anteil gebildet, das Feld trägt „nicht definiert“. auswertung.py liest die Zeile des Plateau-Gewinners und berichtet sie (22.2: Bericht, kein Tor; N unverändert); es rechnet die Werte nicht. Die Feldliste von zellenbericht.csv ist Registertext (R39). F-3, F-4, F-6.
> Quelle des Grundes: 22.2 (Werte des Laufs für den Gewinner), 12 (auswertung.py hat keinen Schalter und liest Rohergebnisse), Punkt 14 (Reihenfolge Selektion → Bestätigung → Bericht), 2b. Kein Ergebnis.

**Kette:** Marken: 22.2; 45.5.

### 48.3 R35 — Ergänzung zu 15.3 (Bootstrap) und Tatsachennotiz

> R35 — Ergänzung zu 15.3 (Bootstrap) und Tatsachennotiz. 15.3 (a)/(b) regeln die Bauart eines Bootstrap-Intervalls; sie verlangen keines. Abschnitt 8 (Sperrlistenpunkt 13) führt keine Bootstrap-Zeile; der Lauf rechnet kein Intervall. Angewandt wird 15.3 auf die Messbitte R7 Nr. 6 (Block-Bootstrap-Band je Gewinnerzelle, nach dem Tag), gerechnet auf tagesreihen/<zelle>.csv mit L nach 15.3 (b) aus haltedauer_median_handelstage in zellenbericht.csv (R34). Tatsachennotiz: „im Auswertungsskript“ (15.3 (a)) trifft heute keinen Code (0 Treffer bootstrap, TB-120). F-4.
> Quelle des Grundes: 8 (abschliessende Berichtsliste), 15.3 im Wortlaut („jedes … wird … gerechnet“), R6/R7. Kein Ergebnis.

**Kette:** Marken: 15.3.

### 48.4 R36 — Präzisierung zu 24.2 und 45.5 (zwei Drawdown-Spalten; Konsistenzprüfung; Ausschnitt)

> R36 — Präzisierung zu 24.2 und 45.5 (zwei Drawdown-Spalten; Konsistenzprüfung; Ausschnitt). zellen.csv trägt je (Zelle, Falte) kapital_drawdown_mtm_pct — den Kapital-Drawdown der Nebenbedingung auf der täglichen MtM-Reihe (1a) auf den Tagen des Benchmarks (3b (c)) — und kapital_drawdown_ereignis_pct — den ereignisindizierten Drawdown, berichtet, nicht bewertet (24.2). Die Spalte kapital_drawdown_pct wird durch die zwei benannten ersetzt, nicht umgedeutet. auswertung.py rechnet kapital_drawdown_mtm_pct aus tagesreihen/<zelle>.csv nach und endet bei Abweichung mit 2. Der Drawdown je Falte ist der Ausschnitt eines durchgehenden Kapitalpfads (29.3, 2a): gemessen innerhalb der Falte, mit dem Kapitalstand am Faltenbeginn als erstem Hochpunkt, ohne Neustart des Kapitals. Festlegung 3 und Abschnitt 8 („drei tiefste Falten-Drawdowns“, „Kapital-Drawdown je Falte“) beziehen sich auf kapital_drawdown_mtm_pct; der ereignisindizierte Wert steht daneben als eigene Zeile. Vollzieht K4j (1) und (2); (3) folgt mit 40.8 (h). F-5, M49, M62.
> Quelle des Grundes: 24.2, 24 (Festlegung 1 präzisiert), 24.6 (Bauart der Faltenmessung), 29.3, 2a, 24b A2 (ein Wert, der nachgerechnet werden kann, tut nicht, als wäre er gemessen), 12. Kein Ergebnis.

**Kette:** Marken: 24.2; 45.5. Voraussetzung gemessen: 50.1.

### 48.5 R37 — Präzisierung zu 16.6, 35.1, 16.4 (c)/(d), 5.1 Nr. 7 (zwei Zeiträume, ein Name)

> R37 — Präzisierung zu 16.6, 35.1, 16.4 (c)/(d), 5.1 Nr. 7 (zwei Zeiträume, ein Name). Der Begriff „Bestätigungsperiode“ bezeichnet zwei Zeiträume. (i) Die Bestätigungsperiode des Selektionslaufs ist die Spanne nach 35.1 (Beginn „Bestätigung ab“, 21.4; Ende Go-Live-Schnitt, ausschliesslich; registrierter Bestand 2026-01-01/2026-09-01), gerechnet auf dem Snapshot; sie wächst nicht (5c: ein zweiter Snapshot ist ein neuer Lauf). Die Bedingung aus 16.6 gilt an ihrem Beginn: Die Bestätigungsstatistik des Gewinners beginnt am ersten Handelstag ab Beginn der Spanne, an dem keine vor der Spanne eröffnete simulierte Position des Gewinners mehr offen ist; Deckel je Bot nach 16.6/41.3 C2; eine am Deckeltag noch offene solche Position zählt nicht (Attribution je Position). Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle (bestaetigung_ab_effektiv, R34); auswertung.py nimmt den Wert der Gewinnerzelle (41.3 C3). (ii) Die Bestätigungsperiode der Leiter (16.4 (c)/(d)) ist der Papierpfad ab Go-Live; sie wächst; 5.1 Nr. 7 („wächst jeden Monat“), 15.4 2d („Go-Live-Tag plus Embargo“) und der Wortlaut von 16.6 („nach Go-Live“, „im Journal vermerkt“) beschreiben sie; dort gilt dieselbe Bedingung mit der Grenze Go-Live und den Positionsdaten des Papierpfads als Quelle. „Alle Falten“ in Abbruchkriterium (b) sind die Selektionsfalten (4.1); die Bestätigungsperiode ist keine Falte im Sinn von 4a (35.1) und wird ausgewertet, nachdem die Auswahl steht (5.1 Nr. 7). F-6, W39, M53.
> Quelle des Grundes: 15.1 (Out-of-Sample des Laufs ist allein die Bestätigungsperiode des gewählten Satzes), 5.2 (Forward-Test geht in keine Selektion ein, auch nicht in die Bestätigungsperiode), 35.1, 4.1, 16.4. Kein Ergebnis.

**Kette:** Marken: 5.1, Nr. 7; 16.4 (c); 16.4 (d); 16.6; 35.1.

### 48.6 R38 — Ergänzung zu 16.7 (d) (Ort der Berichtsgrössen)

> R38 — Ergänzung zu 16.7 (d) (Ort der Berichtsgrössen). Die Faltenkohärenz (Spearman-Rangkorrelation der Zellen-Rangfolge einer Falte gegen die Rangfolge nach dem Median der übrigen Selektionsfalten) rechnet auswertung.py aus zellen.csv, je Bot und Falte; sie braucht alle Zellen und existiert nur dort. Symbolzahl, Anteil am Universum und die Liste der ausgelassenen Symbole mit Grund schreibt der Zellen-Erzeuger je Bot und Falte in symbole_je_falte.csv aus dem Ladeprotokoll (42.1 D3/D7); auswertung.py berichtet sie. 16.11 Zeile 7 wird damit geschlossen. F-7.
> Quelle des Grundes: 16.7 (d) im Wortlaut („nach dem Lauf die Faltenkohärenz“), 5e. Kein Ergebnis.

**Kette:** Marken: 16.7 (d).

### 48.7 R39 — Ergänzung zu 46.3 (R12) und Berichtigung des Datenvertrags (Ausgaben des Zellen-Erzeugers; Feldliste als…

> R39 — Ergänzung zu 46.3 (R12) und Berichtigung des Datenvertrags (Ausgaben des Zellen-Erzeugers; Feldliste als Registertext). Ausgaben des Zellen-Erzeugers je Bot: zellen.csv (R33, R36), tagesreihen/<zelle>.csv, benchmark_tagesreihen/<bot>.csv, zellenbericht.csv (R34), symbole_je_falte.csv (R38), herkunft.json mit teile (37.4) und dem gerechneten Datenstand-Hash (46.7 (b)), Lese-Audit (5e). Die Benchmark-Tagesreihe ist je Bot, nicht je Markt (23.3: Symbole, die der Loader des Bots handelbar macht; 16.7 (b): Schranken je Bot); „benchmark_tagesreihen/<markt>.csv“ im Vertrag lies „<bot>.csv“. Sie wird über benchmark.py::bh_tagesrenditen (Sperrlistenpunkt 6, unverändert) gerechnet — derselbe Code wie für die Benchmark-Tabelle, kein zweiter Rechenweg. Die Feldliste jeder dieser Dateien ist Registertext (Bauart 33.3, 41.1 A12) und wird im Registerauftrag E-2 aus dem Docstring von auswertung.py gemessen eingetragen, nicht abgeschrieben. F-8, A68.
> Quelle des Grundes: 23.3, 16.7 (b), 37.5 (2) (ein Wert, ein Ort), 33.3, 41.1 A12, 5e. Kein Ergebnis.

**Kette:** Marken: 46.3. Feldliste: 50.2.

### 48.8 R40 — Ersteintrag — Schreibregel für Ausgaben der Erzeuger

> R40 — Registertext, Ersteintrag — Schreibregel für Ausgaben der Erzeuger. Die Ausgaben des Listen-Erzeugers und des Zellen-Erzeugers unterliegen 36.1 (2) und (3): --ziel ist Pflicht, die Voreinstellung ist nie ein Pfad, an dem etwas liegt; existiert eine Zieldatei, endet der Erzeuger mit 1 und schreibt nichts, auch nicht bei gleichem Inhalt. Ein zweiter Lauf schreibt an ein neues Ziel und ist als zweiter Lauf im Lese-Audit und im Protokoll (10.1) sichtbar. Die Hashes aller Ausgaben stehen im Bericht. F-9.
> Quelle des Grundes: 36.1 (1) deckt Ergebnisse nicht („für sie bestimmt“); 10.1 („Wer Vorher und Nachher vergleicht, hat wieder eine Wahl“ — ein überschriebenes Ergebnis macht den Vergleich unmöglich und unsichtbar zugleich), 5e, Prüfprinzip D6. Kein Ergebnis.

**Kette:** Marken: keine.

### 48.9 R41 — Ergänzung zu 41.2 B6/B7 und 15.3 (b) (haltedauer_balken)

> R41 — Registertext, Ergänzung zu 41.2 B6/B7 und 15.3 (b) (haltedauer_balken). haltedauer_balken ist die Zahl der Kerzen des Zeitrahmens des Bots von der Einstiegskerze bis zur Ausstiegskerze, beide eingeschlossen — die Zählregel, die positionen_holen.py heute anwendet (TB-120 C1). Einheit: Kerzen des Zeitrahmens (1d, 4h, 1h). Umrechnung in Handelstage für den Deckel (16.6) und für L (15.3 (b)): 1d-Bots Balken = Tage (Krypto: Kalendertage, 15.4 Anmerkung 1); 4h-Bots Balken ÷ 6, 1h-Bots Balken ÷ 24, aufgerundet (15.4 Anmerkung 4). Die Donchian-Untergrenze (41.2 B3, median_balken) nutzt dieselbe Einheit. [Voraussetzung, zu messen: ob TB-24 die Haltedauer in 15.4 (t3_supertrend 11,21 Tage) als Kerzenzahl oder als Zeitstempeldifferenz gebildet hat; bei Abweichung trägt die Neurechnung nach 41.3 C2 diese Zählregel, und 15.4 erhält eine Tatsachennotiz.] F-10.
> Quelle des Grundes: 15.4 Anmerkungen 1 und 4, 41.2 B3/B6/B7, 41.3 C2. Kein Ergebnis.

**Kette:** Marken: 15.3 (b); 15.4; 41.2, Eintrag B6/B7. Voraussetzung gemessen: 50.1.

### 48.10 R42 — Ergänzung zu 40.6, 45.3, 46.3 (Bindung der neuen Listen)

> R42 — Ergänzung zu 40.6, 45.3, 46.3 (Bindung der neuen Listen). Die neun neu erzeugten Trade-Listen werden als neuer Punkt 15 in Abschnitt 10 aufgenommen (Pfad, je Liste Hash; Fortschreibung des Listentexts vor dem Tag, neues Abbild nach 37.3) und stehen zugleich in herkunft.py::EINGEFROREN und der Gruppe eingefroren des Abbilds (R3, R12). Der Punkt ist die Regel, die Gruppe ihre Umsetzung; R3 erfüllt 40.6 nicht, weil ein Abbild den Registertext nicht ersetzt (30.2 (2)). Dass ein Pfad in einem Punkt und in eingefroren steht, gilt heute schon für faltenplan.py, benchmark.py und auswertung.py. F-11.
> Quelle des Grundes: 40.6 („als Punkt auf die Sperrliste“), 30.2 (2), 36.6, 37.3. Kein Ergebnis.

**Kette:** Marken: 40.6; 45.3; 46.3. Abschnitt 10: Indexzeile, keine Marke.

### 48.11 R43 — Registertext zum Zellen-Kern; Berichtigung zu 29.4/34.5 (Ort der Wache); Tatsachennotiz zu 11.2

> R43 — Registertext zum Zellen-Kern; Berichtigung zu 29.4/34.5 (Ort der Wache); Tatsachennotiz zu 11.2. Der Zellen-Erzeuger rechnet jede Zelle über den Signalpfad (collect_all_trades mit den Achsenwerten) und die Zuteilung (simulate_portfolio → shared/zuteilung.py::simuliere_portfolio, Punkt 10); evaluate_combination_multi der neun Optimierer bleibt ausserhalb des Laufs und wird nicht zum Zellen-Kern umgebaut (es verwirft Zellen und kennt keine Falten; 43-7). Die Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte“ (29.4, 34.5) steht im Zellen-Erzeuger — an einer Stelle, für alle neun Bots, mit dem Bericht je Bot aus 34.5 —, nicht in den neun multi_symbol_optimise.py; „in allen neun multi_symbol_optimise.py“ lies „im Zellen-Erzeuger, für alle neun Bots“; die neun Optimierer erhalten eine Tatsachennotiz „nicht im Laufpfad“. Tatsachennotiz zu 11.2: Die Voraussetzung „evaluate_combination_multi liefert den Kapital-Drawdown“ wird für den Lauf gegenstandslos; den Kapital-Drawdown liefert der Zellen-Kern (R36); Agent 2 ist Regelbetrieb. Posten 5 des Plans ist neu zu fassen (Handwerk). F-12, M60.
> Quelle des Grundes: 43-7 (null Trades ist ein Wert; ein Kern, der Zellen verwirft, rechnet ein anderes Raster), Prüfprinzip A8 (eine Wache ist, was ausgeführt wird), 29.3, 34.5 (Reichweite: alle neun Bots — sie bleibt), Punkt 11 (Optimierer nicht ohne Not öffnen). Kein Ergebnis.

**Kette:** Marken: 11.2; 29.4; 34.5.

### 48.12 R44 — Ergänzung zu 40.6 (Reihenfolge der Neuerzeugung)

> R44 — Ergänzung zu 40.6 (Reihenfolge der Neuerzeugung). Die neun Listen werden nach der letzten Änderung am Signalpfad erzeugt — nach TB-30b Posten 3 (Durchreichung der Achsen) und Posten 4 (Horizont je Bot, 26.2/29) —, am Stand, den der Tag signiert. Eine Erzeugung vor einer dieser Änderungen ist Probe, kein Nachweis. Danach: Ableitung der Faltenlänge nach 5.4 und Vergleich gegen 33.2 (40.6), dann das Abbild des Faltenplans (40.8 (g)). F-13.
> Quelle des Grundes: 40.6 („mit dem registrierten Code“), 37.3 (das letzte Abbild trägt die Hashes des Tag-Commits), 40.8 (g). Kein Ergebnis.

**Kette:** Marken: 40.6.

### 48.13 R45 — Registertext zu Sperrlistenpunkt 10 (ausgeführte Positionen)

> R45 — Registertext zu Sperrlistenpunkt 10 (ausgeführte Positionen). shared/zuteilung.py::simuliere_portfolio gibt zusätzlich die ausgeführten Positionen (Symbol, Einstiegs- und Ausstiegszeit, Grösse, Preise) heraus — additiv, als weiteres Feld oder weiteren Rückgabewert; Zuteilungsreihenfolge, SEED und Rechnung unverändert; kein Feld, das der Laufcode liest, wird beschrieben (A9). Beauftragte Änderung nach 37.3 mit Nachweis in der Bauart von 10.1: Trade-Listen und equity_curve aller neun Bots bytegleich vor und nach der Änderung; Mutationsprobe: Rückgabe entfernt ⇒ Zellen-Erzeuger endet mit 2; Hash-Übergang Punkt 10, neues Abbild. Eine Rekonstruktion der Positionen aus den Ereignissen der equity_curve ist ein zweiter Rechenweg und wird nicht gegangen. F-14.
> Quelle des Grundes: 24.2/1a (die MtM-Reihe braucht die Positionen), 37.3, 10.1 („bitidentisch“), 41.1 A9, 37.5 (2) (ein Wert, ein Ort). Kein Ergebnis.

**Kette:** Marken: keine. Abschnitt 10: Indexzeile, keine Marke.

### 48.14 R46 — Ersteintrag — Abnahme des Zellen-Erzeugers vor dem Tag

> R46 — Registertext, Ersteintrag — Abnahme des Zellen-Erzeugers vor dem Tag. Vor dem signierten Tag läuft der Zellen-Erzeuger nicht auf dem registrierten Snapshot mit dem registrierten Raster. Abgenommen wird er im Selektionsmodus gegen einen Test-Snapshot aus synthetischen Kursdaten (mit snapshot.py gezogen, eigener Hash, als Probe benannt; kein Lauf dieses Registers nach 5c/5e), durch die ganze Kette bis auswertung.py und Bericht (der Kettenlauf aus 25f A3 (1); Glied 2 aus 46.8 R17 (d)). Geprüft werden Struktur und Verfahren: Zeilenzahl nach R33, Nullzeile, Feldlisten nach R39, Lese-Audit, Ausgänge nach 36.5, Schreibregel R40, Nachrechnung R36 — nie eine Zahl des Selektionsraums. Der Hash des Test-Snapshots steht in der Tatsachennotiz der Abnahme. F-15.
> Quelle des Grundes: 27.1, 24.3 (die Regel steht vor der Messung), 23e und 41.3 C6 (der Nachweis geht denselben Weg wie der Lauf; ein Hilfsordner ist kein Modus-Lauf), 5c, Prüfprinzip A8. Kein Ergebnis.

**Kette:** Marken: keine.

### 48.15 R47 — Präzisierung zu 40.6 (Tatsachennotiz zu 5.4: „Parameterdateien“)

> R47 — Präzisierung zu 40.6 (Tatsachennotiz zu 5.4: „Parameterdateien“). Parameterdateien eines Bots sind die Module, aus denen sein Signalpfad zur Laufzeit Handelsparameter bezieht — gemessen am Import-Audit des Modus-Laufs des Listen-Erzeugers (Lauf-Typ nach 42.2 E5), nicht per Namensliste; heute mindestens live_params.py und backtest_*.py je Bot. Nach TB-30b Posten 3 ist SMA_TREND_PERIOD Rasterachse, keine Parameterdatei mehr. Die Tatsachennotiz zu 5.4 nennt je Bot die Liste mit Hash und Commit. F-17.
> Quelle des Grundes: 40.6, 5e (der Lauf belegt, woraus er gelesen hat), 37.5 (2). Kein Ergebnis.

**Kette:** Marken: 40.6.

### 48.16 R48 — Lesarten zu Register 0–12 (TB-121), je mit Fundstelle

> R48 — Lesarten zu Register 0–12 (TB-121), je mit Fundstelle.
> (a) Festlegung 4 trägt im Wortlaut kein Exposure-Argument; die registrierte Lesart ist 4.2 (12, Lesart 1). Marke an Festlegung 4 (R51). W42.
> (b) Abschnitt 9: N je Bot ist N_historisch(Bot) + Zellen(Bot) (Tabelle in 3: N nominal = Zellen + N historisch je Zeile, Summe 3 069); „N = 653 plus die Zellen dieses Laufs, je Bot getrennt“ ist die Kurzform. M47.
> (c) Abschnitt 7 (d): Ist der Gewinner eine Spitze und erfüllt der beste Nicht-Spitzen-Punkt (a) nicht, ist (d) nicht erfüllt; der Bot bleibt mit dem Plateau-Gewinner, die Spitze ist Markierung (6, 8); (d) tauscht den Gewinner nie aus (22.5). [Voraussetzung, zu messen: die von auswertung.py in diesem Fall ausgegebene Zelle; Abweichung ist ein Register-Code-Widerspruch nach 25c (1).] M48.
> (d) Exposure: DD_Toleranz(e) und DD_Benchmark(f, e) werden mit der mittleren Exposure des Parametersatzes in der jeweiligen Falte ausgewertet (4.2). Die mittlere Exposure der Kapitalregel (7.1, 7 (c), 16.4 (b), 15.6 (c)) ist die des Gewinners über seine Selektionsfalten (7 (c): „über dieselben Tage“). Mittlere Exposure = Mittel über die Handelstage des Zeitraums (Krypto Kalendertage, 15.4 Anmerkung 1) des Anteils des Kapitals in offenen Positionen am Tagesschluss, bewertet wie die MtM-Reihe (1a). [Voraussetzung, zu messen: Bildung von mittlere_exposure im Vertrag/auswertung.py und in mtm_kern.py; der Registertext folgt dem Code, wo er ihn hat.] M50, M54, A69.
> (e) Benchmark: Gewichte täglich gleich (23.3, 23.5), Höhe statisch in der mittleren Exposure (4.2, 7 (c)); „statische Position“ meint die Höhe, „point-in-time“ die Menge (23.7). M51.
> (f) Kante (2.5): jeder Gewinner, der auf mindestens einer Achse auf der ersten oder letzten Stufe liegt, Zusatzstufen („kein“, „structural“) und die Obergrenze des Positionslimits eingeschlossen; die Markierung sagt, wo der Gewinner liegt, nicht, ob erweitert würde. [Voraussetzung, zu messen: auswertung.py markierungen.] M52.
> (g) Zufalls-Timing (8.1): über die aneinandergehängten Selektionsfalten (dieselben Tage wie 7 (c)); verglichen wird die Summe der täglichen Renditen (2a) der zyklisch verschobenen Exposure-Reihe auf den Benchmark-Tagesrenditen mit der Rendite des Satzes über dieselben Tage; das 95. Perzentil ist das empirische Perzentil über alle T − 1 Verschiebungen. [Voraussetzung, zu messen: Perzentilbildung im Code.] M56.
> (h) haltedauer (2.2) ist eine Messung aus gefundenen Trades (Grenzsatz „gemessene Median-Haltedauer“; 41.2 B3); „Hypothese“ im Kopf von 3 ist erzeugter Text und bleibt. Bei elliott_wave gilt „gefunden“ ohne Ausnahme (41.3 C4). M57, M58.
> (i) Die Ziffernregel aus 2.1 gilt für Grenzsätze; Spaltenköpfe der Messgrössentabelle („Median 20-Balken-Spanne“) sind keine Grenzsätze. [Voraussetzung: pruefe_grenzsaetze.py prüft die Satzfelder.] M61.
> (j) Festlegung 3 bei weniger als drei Selektionsfalten: Der Fall tritt nicht ein — 4b verlangt mindestens 3, sonst 4c (keine Selektion). A75.
> (k) Präzisierung zu 10.1: „Stichproben-Hash-Vergleich“ lies „Hash-Vergleich aller Ausgabedateien des Laufs nach dem Lese-Audit“; eine Stichprobe hätte eine Ziehung, also eine Wahl, und der Vollvergleich kostet nichts. A74.
> Quelle des Grundes: die genannten Fundstellen; 22.5; 24b A2; Prüfprinzip C4. Kein Ergebnis.

> ⭐ **48.16 R48 (g) BERICHTIGT durch R54 (49.2)** (Fable 30a R54, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **48.16 R48 (d) ERGÄNZT durch R60 (51.5)** (Fable 01a R60, TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 1, Tabelle, Zeile 4; 1, Tabelle, Zeile 3; 2.1; 2.2; 2.5; 7, Tabelle, Zeile (d); 8.1; 9, erster Absatz. Voraussetzung gemessen: 50.1. Abschnitt 10: Indexzeile, keine Marke.

### 48.17 R49 — Tatsachennotizen zu Register 0–12 (TB-121), Marke je am alten Ort

> R49 — Tatsachennotizen zu Register 0–12 (TB-121), Marke je am alten Ort.
> (a) Zu 2.2: Der erzeugte Abschnitt 3 verwendet ableitung an zwei Stellen (Obergrenze Positionslimit; bb_squeeze_percentile oben) und methode an drei (take_profit_fib; Stop-Zusatzstufe „kein“; bb_lookback unten); 2.2 nennt je ein Beispiel. Massgeblich ist der erzeugte Block (registerbericht.py --pruefen). W40.
> (b) Zu 2.7: Die Quantil-Achsen (rsi_threshold, adx_threshold) folgen einer dritten Stufungsart — Quantile der gemessenen Verteilung (Grenzsätze in 3) —, die 2.7 nicht nennt. Messbitte (Verfahrensmessung, 27.2), nur das Wie: die Funktion in registerdaten.py, die die Quantil-Stufen bildet, und ihre Eingabe aus messgroessen.json (Zeitraum, Zeitrahmen, Universum); Ergebnis als Tatsachennotiz zu 2.7. W41, A71.
> (c) Zu 3 und 4.4: Zahlenteil und Beispiel zeigen den Stand 14.09.2026 (benchmark_drawdowns.json, a163c498…); die Tabelle, die der Lauf liest, ist ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json (39.2, 64fb2912…); der ERZEUGT-Block wird mit 40.8 (h) neu erzeugt (43-6); die in 40.8 (b) verlangte Tatsachennotiz an 4.4 steht dort noch nicht. W43.
> (d) Zu 12: Die Zahl der Prüfungen ist Tatsachennotiz mit Stand; die jüngste Marke gilt (41.1 A1: 196, db50e187…; Mutationsproben H1–H7, H6 offen nach 41.1 A4). W44.
> (e) Zu 38.2: Die Regel gilt auch für Marken. Die Marke in 6 nennt registerdaten.py:605 ohne Commit; die Zeile ist über 42.3 F1 gedeckt („unverändert seit vor 4faef05“). Künftig nennen Marken Bezeichner, nicht Zeilen. W45.
> (f) Zum Kopf des Registers: „Stand: 14.09.2026“ ist der Stand der Erstfassung; das Register ist append-only, sein Stand ist der Commit im Kopf der Kopie (27.3) beziehungsweise HEAD. W46.
> (g) Zu Abschnitt 10, Tatsachennotiz vom 15.09.2026: „nach dem Lauf“ bezeichnet den nativen Neuaufbau der 72 Krypto-Kursdateien (TB-34, shared/kursdaten_neuaufbau.py), keinen Selektionslauf. M59.
> (h) Zu 11: „die beiden Bug-Fixes“ sind 11.1 und 11.2; 11.3 ist eine dritte Voraussetzung des Laufs (ohne Durchreichung ist das registrierte Raster nicht rechenbar; TB-30b Posten 3, E-1). Stand: 11.1 erfüllt (42.3 F3), 11.2 für den Lauf gegenstandslos (R43), 11.3 offen (E-1). M60.
> Quelle des Grundes: Messungen TB-120/TB-121, die genannten Fundstellen. Kein Ergebnis.

**Kette:** Marken: Kopf, Absatz „Stand: 14.09.2026“; 2.2; 2.7; 3, Zahlenteil (nach ENDE ERZEUGT); 4.4; Abschnitt 11; Abschnitt 12; 38.2. Voraussetzung gemessen: 50.1. Abschnitt 10: Indexzeile, keine Marke.

### 48.18 R50 — Ergänzung zu 12 (Kennzahlendefinitionen im Code) und Tatsachennotiz zu TB-121

> R50 — Ergänzung zu 12 (Kennzahlendefinitionen im Code) und Tatsachennotiz zu TB-121. Die Definitionen der Kennzahlen des Laufs — Falten-Sharpe (15.3), Calmar und Annualisierung, Alpha/Beta, DSR-Eingaben (Sharpe, T, Schiefe, Wölbung, Streuung), mittlere Exposure, Korrelationsmass und Operator der Clusterschwelle, Zellenname und Gleichstandsschlüssel, Ausstiegskonvention je Ausstiegsart, Interpolation an den Rändern (43-2) — sind im eingefrorenen Code registriert (Sperrliste 3, 5, 7, 9; Abschnitt-0-Menge), nicht im Text von 0–12. Vor dem Tag wird je Kennzahl eine Tatsachennotiz eingetragen: Datei und Bezeichner (38.2), und wo das Register eine Formel nennt (15.3; 7 „Calmar bei Drawdown 0 ist 0,0“; 4.2; 9), die gemessene Übereinstimmung; eine Abweichung ist ein Register-Code-Widerspruch (25c (1)) und wird gemeldet, nicht eingetragen. Der Registertext legt keine dieser Definitionen neu fest. Messbitte (27.2), nur das Ob: trägt registerdaten.py für jede der 34 Rastergrenzen einen Grenzsatz, und fasst registerbericht.py gleiche Sätze zusammen? (Der erzeugte Block führt für t3_slow_length, donchian_period oben und stop_mode unten/oben keinen eigenen Satz; 2.1 verlangt einen je Grenze.) Tatsachennotiz zu TB-121: 85 Befunde (B 19, V 19, W 8, M 16, A 15, Z 8), jedes Zitat maschinell geprüft; Vollständigkeitstest kalt: 3 von 12 Bausteinen aus 0–12 schreibbar; die Sitzung hatte Zusammenfassungen der Abschnitte 15–46 im Gedächtnis (Claude Code MEMORY.md), deshalb ist die Befundliste eine Untergrenze und „3 von 12“ eine Obergrenze; ihre Vollständigkeit ist nicht belegt. A63, A64, A65, A72, A76, M55, A73, Frage 78.
> Quelle des Grundes: 13 („Das Urteil ist Code“), 12, Sperrliste 3/5/7/9, 38.2, 25c (1), 2.1, Messung TB-121. Kein Ergebnis.

**Kette:** Marken: Abschnitt 12. Voraussetzung gemessen: 50.1.

### 48.19 R51 — Marken am alten Ort für Register 0–12 (Handwerk im Registerauftrag; der alte Satz bleibt zeichengleich)

> R51 — Marken am alten Ort für Register 0–12 (Handwerk im Registerauftrag; der alte Satz bleibt zeichengleich). Festlegung 4 → 4.2 (12, Lesart 1) [W42]. Festlegung 2 und 7 (a) → 15.3 (c) und Formelzeile [A63]. 3, Zahlenteil und 4.4 → 39.2 (Tabelle des Laufs), 40.8 (h), R49 (c) [W43, A67]. 4.2 → 43-2 (Interpolation an den Rändern) [A70]. 5.3 und 15.6 → 33.2 (gültiger Faltenplan, alle neun Bots) [A66]. 9 → R48 (b) [M47]. 10, Tatsachennotiz 15.09. → R49 (g) [M59] — als Indexzeile, in Abschnitt 10 steht keine Marke. 11 → R49 (h) [M60]. 12 → R50. Kopf → R49 (f) [W46]. Datenstand-Hash voll: 17.3/17.9/18 — Indexzeile, keine Marke in 10 [A77].
> Quelle des Grundes: 34 (Marke am alten Ort), 27.3, REGISTER_INDEX. Kein Ergebnis.

**Kette:** Marken: 1, Tabelle, Zeile 2; 4.2; 5.3; 7, Tabelle, Zeile (a); 15.6. Abschnitt 10: Indexzeile, keine Marke.

### 48.20 R52 — Tatsachennotizen 29b

> R52 — Tatsachennotizen 29b. (a) 27b B3 („die datierten Kopien … sind im Repo committet“) war für vier von sechs Registerkopien falsch (TB-118 A3); zehnter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt“. (b) 45.5 (b) („für jede Zelle genau eine Zeile“) widersprach dem Datenvertrag; berichtigt in R33; elfter Fall. (c) Der Chat des Verfahrensprüfers ist zwischen 29a und 29b einmal verdichtet worden; die Registerteile 1–4, 27b und 25f wurden danach erneut vollständig gelesen; die Umzugsampel steht deshalb auf 🟡, Umzug nach E-2.
> Quelle des Grundes: Messungen TB-118, TB-120; Leseprotokoll 29b. Kein Ergebnis.

**Kette:** Marken: keine.


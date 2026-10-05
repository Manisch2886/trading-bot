# CLOUD_TB-135 — Anforderungen an den Zellen-Erzeuger aus R33–R73

**Commit:** `d781f1b` (`git rev-parse --short HEAD` = `origin/main`, Commit vom 2026-10-04 09:12 +0200) · Arbeitsbaum sauber, nichts geändert, nichts ausgeführt ausser Lese-/Suchbefehlen.
**Register:** `docs/VORREGISTRIERUNG_neuselektion.md`, 11 471 Zeilen, sha256 `9a2cefb77a394a0a1c87c63cb9437d5693f054e4516333f656fae97668ef71ff`
**Ergebnis TB-120:** `docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md`, 223 Zeilen, sha256 `9e1d5718b83d940dbde861d3598c27a07bbae55ef7e1b3eeb305f706d86ab7a3`

**Gelesene Dateien**
- `CLAUDE.md` (vom Werkzeug beim Start geladen)
- `docs/VORREGISTRIERUNG_neuselektion.md` — Z. 10785–11471; vollständig gelesen: alle Abschnitte `### <n>.<m> R33` … `R73` (48.1–48.20, 49.1–49.3, 51.1–51.7, 52.1–52.3, 53.1–53.8) sowie 50.2 (Feldliste zu R39, kein Block). Nicht inhaltlich gelesen: 50.1, 50.3–50.7, 51.8–51.10, 52.4–52.5, 53.9–53.10 (nur Überschriften; dort nur ⭐-Zeilen per Suche erfasst).
- `docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md` — Z. 1–32, 52–66, 110–223 gelesen; Z. 33–51, 67–109 nur Überschriften.
- `research/vorregistrierung/auswertung.py` — nur Z. 36–67 (Docstring „DIE ROHERGEBNISSE - DER VERTRAG“) gegen Commit `0f56aeb` verglichen: zeichengleich, d. h. das Zitat in 50.2 gilt auch für HEAD.
- `*.py` im Repo: nur Trefferzeilen aus `git grep` (Teil 4).
- Nicht gelesen: `ergebnisse/`, `*.db`, Kursdateien, Trade-Listen, `docs/belege/TB-120/*` (u. a. `b_offen.md`; Pfad nur genannt).

**Methode:** Je Block wurden die `>`-Zeilen in Sätze geteilt und nach den acht Suchwörtern gefiltert (66 Treffer, davon 3 in „Quelle des Grundes“). Danach wurden Sätze ohne Bezug zum Zellen-Erzeuger aussortiert und Sätze aus demselben Block ergänzt, die keines der Suchwörter enthalten, aber eine Spalte oder Datei des Erzeugers festlegen (in der Spalte „Art“ mit ¹ markiert). Jeder Wortlaut wurde per Skript aus der Registerzeile ausgeschnitten und muss dort zeichengleich vorkommen; Kürzung auf 300 Zeichen ist mit „…“ angezeigt.

---

## 1. Fundliste (83 Sätze)

Art: **D** = Datei oder Spalte · **W** = Wache im Lauf mit Ausgang · **P** = Probe in der Abnahme nach R46 · **S** = Sonstiges. ¹ = Satz ohne Suchwort.
Zählung nach Art: D 36 · S 27 · P 11 · W 9 (davon 1 ohne genannten Ausgang: R43).

| Block | Abschnitt | Unterpunkt | Registerzeile | Wortlaut | Art |
|---|---|---|---|---|---|
| R33 | 48.1 | — | 10791 | „zellen.csv enthält für jede Zelle des Rasters und jede Falte des Faltenplans des Bots — Selektionsfalten und Bestätigungsperiode (35.1) — genau eine Zeile; die Zeilenzahl je Bot ist Zellen × (Selektionsfalten + 1). | D |
| R33 | 48.1 | — | 10791 | Eine (Zelle, Falte) ohne Trades trägt die Nullzeile: Trade-Zahl 0, Sharpe 0 nach 1c, Drawdown 0, nie nichts.“ | D |
| R33 | 48.1 | — | 10791 | Eine fehlende Zeile ist ein Befund über den Erzeuger, kein Ausgang. | S |
| R33 | 48.1 | — | 10791 | Es gibt keine Trade-Liste je Zelle als Rohergebnis; „leere Trade-Liste“ in 45.5 (b) und 43-7 bezeichnet den Fall „keine Trades gefunden“, dessen Ergebnis beim Listen-Erzeuger eine leere Liste und beim Zellen-Erzeuger die Nullzeile ist. | D |
| R34 | 48.2 | — | 10801 | Der Zellen-Erzeuger schreibt je Bot eine Datei zellenbericht.csv mit genau einer Zeile je Zelle und den Feldern: die drei Werte aus 22.2 (Ertragsanteil der besten Selektionsfalte, des besten Symbols, der fünf besten Trades), haltedauer_median_handelstage (15.3 (b), R41) und bestaetigung_ab_effekt … | D |
| R34 | 48.2 | — | 10801 | Grundlage der drei Anteile: realisierte Erträge der ausgeführten Trades (Summe pnl_pct), Faltenzuordnung nach dem Einstiegstag (2b), nur Selektionsfalten; Anteil = Beitrag ÷ Gesamtertrag; bei Gesamtertrag ≤ 0 wird kein Anteil gebildet, das Feld trägt „nicht definiert“. | D ¹ |
| R34 | 48.2 | — | 10801 | auswertung.py liest die Zeile des Plateau-Gewinners und berichtet sie (22.2: Bericht, kein Tor; N unverändert); es rechnet die Werte nicht. | S ¹ |
| R34 | 48.2 | — | 10801 | Die Feldliste von zellenbericht.csv ist Registertext (R39). | S |
| R35 | 48.3 | — | 10808 | Abschnitt 8 (Sperrlistenpunkt 13) führt keine Bootstrap-Zeile; der Lauf rechnet kein Intervall. | S ¹ |
| R35 | 48.3 | — | 10808 | Angewandt wird 15.3 auf die Messbitte R7 Nr. 6 (Block-Bootstrap-Band je Gewinnerzelle, nach dem Tag), gerechnet auf tagesreihen/<zelle>.csv mit L nach 15.3 (b) aus haltedauer_median_handelstage in zellenbericht.csv (R34). | S |
| R36 | 48.4 | — | 10815 | zellen.csv trägt je (Zelle, Falte) kapital_drawdown_mtm_pct — den Kapital-Drawdown der Nebenbedingung auf der täglichen MtM-Reihe (1a) auf den Tagen des Benchmarks (3b (c)) — und kapital_drawdown_ereignis_pct — den ereignisindizierten Drawdown, berichtet, nicht bewertet (24.2). | D |
| R36 | 48.4 | — | 10815 | Die Spalte kapital_drawdown_pct wird durch die zwei benannten ersetzt, nicht umgedeutet. | D |
| R36 | 48.4 | — | 10815 | auswertung.py rechnet kapital_drawdown_mtm_pct aus tagesreihen/<zelle>.csv nach und endet bei Abweichung mit 2. | W (Ort: auswertung.py, nicht Erzeuger) |
| R36 | 48.4 | — | 10815 | Der Drawdown je Falte ist der Ausschnitt eines durchgehenden Kapitalpfads (29.3, 2a): gemessen innerhalb der Falte, mit dem Kapitalstand am Faltenbeginn als erstem Hochpunkt, ohne Neustart des Kapitals. | D ¹ |
| R36 | 48.4 | — | 10815 | Festlegung 3 und Abschnitt 8 („drei tiefste Falten-Drawdowns“, „Kapital-Drawdown je Falte“) beziehen sich auf kapital_drawdown_mtm_pct; der ereignisindizierte Wert steht daneben als eigene Zeile. | S ¹ |
| R37 | 48.5 | (i) | 10822 | Die Bestätigungsstatistik des Gewinners beginnt am ersten Handelstag ab Beginn der Spanne, an dem keine vor der Spanne eröffnete simulierte Position des Gewinners mehr offen ist; Deckel je Bot nach 16.6/41.3 C2; eine am Deckeltag noch offene solche Position zählt nicht (Attribution je Position). | D ¹ |
| R37 | 48.5 | (i) | 10822 | Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle (bestaetigung_ab_effektiv, R34); auswertung.py nimmt den Wert der Gewinnerzelle (41.3 C3). | D |
| R38 | 48.6 | — | 10832 | Die Faltenkohärenz (Spearman-Rangkorrelation der Zellen-Rangfolge einer Falte gegen die Rangfolge nach dem Median der übrigen Selektionsfalten) rechnet auswertung.py aus zellen.csv, je Bot und Falte; sie braucht alle Zellen und existiert nur dort. | S |
| R38 | 48.6 | — | 10832 | Symbolzahl, Anteil am Universum und die Liste der ausgelassenen Symbole mit Grund schreibt der Zellen-Erzeuger je Bot und Falte in symbole_je_falte.csv aus dem Ladeprotokoll (42.1 D3/D7); auswertung.py berichtet sie. | D |
| R39 | 48.7 | — | 10839 | Ausgaben des Zellen-Erzeugers je Bot: zellen.csv (R33, R36), tagesreihen/<zelle>.csv, benchmark_tagesreihen/<bot>.csv, zellenbericht.csv (R34), symbole_je_falte.csv (R38), herkunft.json mit teile (37.4) und dem gerechneten Datenstand-Hash (46.7 (b)), Lese-Audit (5e). | D |
| R39 | 48.7 | — | 10839 | Die Benchmark-Tagesreihe ist je Bot, nicht je Markt (23.3: Symbole, die der Loader des Bots handelbar macht; 16.7 (b): Schranken je Bot); „benchmark_tagesreihen/<markt>.csv“ im Vertrag lies „<bot>.csv“. | D |
| R39 | 48.7 | — | 10839 | Sie wird über benchmark.py::bh_tagesrenditen (Sperrlistenpunkt 6, unverändert) gerechnet — derselbe Code wie für die Benchmark-Tabelle, kein zweiter Rechenweg. | S ¹ |
| R39 | 48.7 | — | 10839 | Die Feldliste jeder dieser Dateien ist Registertext (Bauart 33.3, 41.1 A12) und wird im Registerauftrag E-2 aus dem Docstring von auswertung.py gemessen eingetragen, nicht abgeschrieben. | S ¹ |
| R40 | 48.8 | — | 10852 | Die Ausgaben des Listen-Erzeugers und des Zellen-Erzeugers unterliegen 36.1 (2) und (3): --ziel ist Pflicht, die Voreinstellung ist nie ein Pfad, an dem etwas liegt; existiert eine Zieldatei, endet der Erzeuger mit 1 und schreibt nichts, auch nicht bei gleichem Inhalt. | W (Ausgang 1) |
| R40 | 48.8 | — | 10852 | Ein zweiter Lauf schreibt an ein neues Ziel und ist als zweiter Lauf im Lese-Audit und im Protokoll (10.1) sichtbar. | S |
| R40 | 48.8 | — | 10852 | Die Hashes aller Ausgaben stehen im Bericht. | S ¹ |
| R41 | 48.9 | — | 10859 | Umrechnung in Handelstage für den Deckel (16.6) und für L (15.3 (b)): 1d-Bots Balken = Tage (Krypto: Kalendertage, 15.4 Anmerkung 1); 4h-Bots Balken ÷ 6, 1h-Bots Balken ÷ 24, aufgerundet (15.4 Anmerkung 4). | S ¹ |
| R43 | 48.11 | — | 10873 | Der Zellen-Erzeuger rechnet jede Zelle über den Signalpfad (collect_all_trades mit den Achsenwerten) und die Zuteilung (simulate_portfolio → shared/zuteilung.py::simuliere_portfolio, Punkt 10); evaluate_combination_multi der neun Optimierer bleibt ausserhalb des Laufs und wird nicht zum Zellen-Ke … | S |
| R43 | 48.11 | — | 10873 | Die Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte“ (29.4, 34.5) steht im Zellen-Erzeuger — an einer Stelle, für alle neun Bots, mit dem Bericht je Bot aus 34.5 —, nicht in den neun multi_symbol_optimise.py; „in allen neun multi_symbol_optimise.py“ lies „im Zellen-Erzeuger, für all … | W (Ausgang im Block nicht genannt) |
| R43 | 48.11 | — | 10873 | Tatsachennotiz zu 11.2: Die Voraussetzung „evaluate_combination_multi liefert den Kapital-Drawdown“ wird für den Lauf gegenstandslos; den Kapital-Drawdown liefert der Zellen-Kern (R36); | S ¹ |
| R45 | 48.13 | — | 10887 | Mutationsprobe: Rückgabe entfernt ⇒ Zellen-Erzeuger endet mit 2; | W (als Mutationsprobe im Nachweis der Änderung an Punkt 10) |
| R45 | 48.13 | — | 10887 | Eine Rekonstruktion der Positionen aus den Ereignissen der equity_curve ist ein zweiter Rechenweg und wird nicht gegangen. | S ¹ |
| R46 | 48.14 | — | 10894 | Vor dem signierten Tag läuft der Zellen-Erzeuger nicht auf dem registrierten Snapshot mit dem registrierten Raster. | P |
| R46 | 48.14 | — | 10894 | Abgenommen wird er im Selektionsmodus gegen einen Test-Snapshot aus synthetischen Kursdaten (mit snapshot.py gezogen, eigener Hash, als Probe benannt; kein Lauf dieses Registers nach 5c/5e), durch die ganze Kette bis auswertung.py und Bericht (der Kettenlauf aus 25f A3 (1); Glied 2 aus 46.8 R17 ( … | P ¹ |
| R46 | 48.14 | — | 10894 | Geprüft werden Struktur und Verfahren: Zeilenzahl nach R33, Nullzeile, Feldlisten nach R39, Lese-Audit, Ausgänge nach 36.5, Schreibregel R40, Nachrechnung R36 — nie eine Zahl des Selektionsraums. | P ¹ |
| R46 | 48.14 | — | 10894 | Der Hash des Test-Snapshots steht in der Tatsachennotiz der Abnahme. | P ¹ |
| R60 | 51.5 | (b) | 11229 | Die Bewertung der Spalte exposure legt dieser Code nicht fest; sie folgt R48 (d): Anteil des Kapitals in offenen Positionen am Tagesschluss, bewertet wie die MtM-Reihe (1a). | D ¹ |
| R60 | 51.5 | (c) | 11229 | (c) Der Zellen-Erzeuger schreibt beide Träger aus einer Rechnung: mittlere_exposure in zellen.csv ist je (Zelle, Falte) das Mittel der Spalte exposure der Tagesreihe dieser Zelle über die Tage der Falte. | D |
| R60 | 51.5 | (c) | 11229 | Die Abnahme nach R46 prüft diese Gleichheit, mit Gegenprobe. | P ¹ |
| R60 | 51.5 | (c) | 11229 | auswertung.py wird dafür nicht geöffnet. | S ¹ |
| R63 | 52.1 | (d) | 11308 | (d) Der Zellen-Erzeuger bezieht weder Positionen noch Exposure aus bot_lauf.py oder dessen Ausgabe; die Positionen kommen aus simuliere_portfolio (R45), die Spalte exposure aus derselben Rechnung wie die MtM-Reihe (R60 (c)). | S |
| R64 | 52.2 | (a) | 11315 | (a) „Handelstage des Zeitraums“ in R48 (d) lies: die Tage des Zeitraums, an denen der Benchmark des Bots definiert ist (23.3), wie benchmark_tagesreihen/<bot>.csv sie führt (R39); die Tatsachennotiz zu 23.3 (erster Kurstag) gilt mit. | D |
| R64 | 52.2 | (a) | 11315 | Das gilt für die mittlere Exposure je (Zelle, Falte) (4.2) und für die des Gewinners über seine Selektionsfalten (7 (c)). | D ¹ |
| R64 | 52.2 | (b) | 11315 | Ein Tag der Tagesreihe ohne Benchmark-Tag geht in keine mittlere Exposure ein; er ist kein Befund. | D |
| R64 | 52.2 | (c) | 11315 | (c) Ein Benchmark-Tag des Bots in einer Falte des Faltenplans, zu dem die Tagesreihe einer Zelle keine Zeile führt, ist ein Befund über den Erzeuger, kein Ausgang (Bauart R33). | S |
| R64 | 52.2 | (c) | 11315 | Der Zellen-Erzeuger prüft im Lauf für jede Tagesreihe, dass sie jeden solchen Tag führt (auch flache Tage, 1a), und endet sonst mit 2. | W (Ausgang 2) |
| R64 | 52.2 | (c) | 11315 | Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf trägt sie selbst. | P |
| R64 | 52.2 | (d) | 11315 | (d) „Über die Tage der Falte“ in R60 (c) lies: über die Tage nach (a), die in die Falte fallen (halboffen wie im Faltenplan; 2a). | D ¹ |
| R64 | 52.2 | (d) | 11315 | Der Wert des Gewinners in beta_bereinigung ist dann das mit der Zahl dieser Tage gewichtete Mittel seiner Werte je Selektionsfalte in zellen.csv; die Abnahme nach R46 prüft auch diese Gleichheit, mit Gegenprobe. | P |
| R64 | 52.2 | (e) | 11315 | (e) Welche Tage die Tagesreihe über die Tage nach (a) hinaus führt, legt dieser Block nicht fest. | S |
| R66 | 53.1 | (a) | 11384 | (a) Die Tagesreihe einer Zelle führt jeden Handelstag des Kapitalpfads, vom 1. Januar der ersten Selektionsfalte des Bots (29.3) bis zum Ende der Bestätigungsperiode (35.1), ohne Lücke. | D |
| R66 | 53.1 | (a) | 11384 | Handelstage sind bei Krypto die Kalendertage (15.4, Anmerkung 1), bei Aktien die Tage des Handelskalenders nach 17.5 (Umgebung, im Lock). | D ¹ |
| R66 | 53.1 | (a) | 11384 | Ein Tag, an dem die Zelle keine Position hält, steht mit Rendite 0 und Exposure 0 in der Reihe (1a), auch ein Tag vor dem ersten Handelbar-Tag des Bots. | D ¹ |
| R66 | 53.1 | (b) | 11384 | (b) Kalender und Kurse stimmen überein: Im Zeitraum nach (a) trägt an jedem Handelstag mindestens ein Symbol der Universumsdatei des Bots (3a) im Snapshot einen Kurs, und kein Symbol der Universumsdatei trägt einen Kurs an einem Tag, der kein Handelstag ist. | W (Bedingung der Wache) ¹ |
| R66 | 53.1 | (b) | 11384 | Der Zellen-Erzeuger prüft das im Lauf je Bot und endet sonst mit 2. | W (Ausgang 2) |
| R66 | 53.1 | (b) | 11384 | Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf trägt sie selbst. | P |
| R66 | 53.1 | (c) | 11384 | (c) Der Falten-Sharpe nach 1c wird über alle Tage der Tagesreihe gerechnet, die in die Falte fallen (2a; halboffen wie im Faltenplan), nicht nur über die Tage, an denen der Benchmark definiert ist. | D |
| R66 | 53.1 | (c) | 11384 | Ein Tag ohne Benchmark-Tag geht mit Rendite 0 ein. Dasselbe gilt für den Sharpe in der Zeile der Bestätigungsperiode, ab dem Tag nach R68. | D ¹ |
| R66 | 53.1 | (c) | 11384 | Der Zellen-Erzeuger bildet ihn mit der Sharpe-Funktion aus kennzahlen.py; sie ist die registrierte Definition (R50), ein zweiter Rechenweg wird nicht gebaut. | D |
| R66 | 53.1 | (d) | 11384 | (d) Auf den Tagen des Benchmarks stehen: der Drawdown der Nebenbedingung (24.2, R36), die mittlere Exposure (R64), Beta-Bereinigung und Calmar-Vergleich (7 (c)) und das Zufalls-Timing (R48 (g): dieselben Tage wie 7 (c)). | D ¹ |
| R66 | 53.1 | (d) | 11384 | Auf dem Kapitalpfad nach (a) steht der Falten-Sharpe und mit ihm die Selektionsstatistik (15.2). | D ¹ |
| R66 | 53.1 | (e) | 11384 | (e) Führt die Tagesreihe einer Zelle an einem Tag, der kein Benchmark-Tag des Bots ist (R72 (b)), eine Rendite ungleich 0 oder eine Exposure ungleich 0, ist das ein Befund über Erzeuger oder Daten, kein Ausgang (Bauart R33); ausgenommen ist der Tag aus der Tatsachennotiz zu 3b (c), Satz zur Zeita … | S (Bedingung der Wache) |
| R66 | 53.1 | (e) | 11384 | Der Zellen-Erzeuger prüft das im Lauf für jede Tagesreihe und endet sonst mit 2. | W (Ausgang 2) |
| R66 | 53.1 | (e) | 11384 | Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf trägt sie selbst. | P |
| R66 | 53.1 | (f) | 11384 | (f) Tatsachennotizen: Kein Code auf der Sperrliste oder im Laufbereich bildet den Falten-Sharpe aus der Tagesreihe oder rechnet ihn nach; die Sharpe-Funktion in kennzahlen.py hat heute keinen Aufrufer, auswertung.py liest netto_sharpe aus zellen.csv. | S |
| R67 | 53.2 | — | 11391 | In jeder Tagesreihe (tagesreihen/<zelle>.csv) und in jeder Benchmark-Tagesreihe (benchmark_tagesreihen/<bot>.csv) ist datum eindeutig, kein Feld leer und jeder Zahlenwert endlich. | D / Bedingung der Wache |
| R67 | 53.2 | — | 11391 | Ein flacher Tag trägt 0, nie nichts (1a). | D ¹ |
| R67 | 53.2 | — | 11391 | Ein Verstoss ist ein Befund über den Erzeuger, kein Ausgang (Bauart R33): Der Zellen-Erzeuger prüft jede dieser Dateien im Lauf, nachdem er sie geschrieben hat, und endet sonst mit 2. | W (Ausgang 2) |
| R67 | 53.2 | — | 11391 | Die Abnahme nach R46 prüft die Wache mit Gegenprobe, je für ein doppeltes Datum, ein leeres Feld und einen nicht endlichen Wert; der registrierte Lauf trägt die Wache selbst. | P |
| R67 | 53.2 | — | 11391 | Für zellen.csv gilt R33. | S |
| R68 | 53.3 | (a) | 11398 | (a) Die Zeile der Bestätigungsperiode (R33) trägt für jede Zelle die Bestätigungsstatistik, die R37 (i) für den Gewinner beschreibt. | D |
| R68 | 53.3 | (a) | 11398 | Alle Grössen dieser Zeile stehen auf den Tagen ab bestaetigung_ab_effektiv der Zelle bis zum Ende der Spanne (35.1). | D ¹ |
| R68 | 53.3 | (a) | 11398 | Die Spanne bleibt, was 35.1 sagt; ihre Tage vor diesem Tag gehören weder zu einer Selektionsfalte noch zur Bestätigungsstatistik. | D ¹ |
| R68 | 53.3 | (b) | 11398 | (b) R64 (a) gilt für die mittlere Exposure dieser Zeile: Mittel über die Benchmark-Tage des Bots innerhalb der Tage nach (a). Die Grösse ist Bericht; auswertung.py liest sie für kein Urteil. | D ¹ |
| R68 | 53.3 | (c) | 11398 | (c) Eine Position, die nach der Attribution je Position (16.6, R37) in der Bestätigungsstatistik nicht gezählt wird, geht in keine Grösse der Zeile ein, auch nicht in ihre Exposure. | D ¹ |
| R68 | 53.3 | (d) | 11398 | (d) Im Fall nach (c) ist die Zeile nicht der blosse Ausschnitt der Tagesreihe (16.6: „ausdrückliche und seltene Ausnahme von der Ein-Pfad-Regel“). Wie die Gleichheitsproben nach R60 (c) und R64 (d) und die Nachrechnung nach R36 diesen Fall behandeln, ist offen und geht vor der Öffnung nach R69 (b … | P |
| R69 | 53.4 | (a) | 11405 | (a) Dass auswertung.py benchmark_tagesreihen/<markt>.csv liest und R39 <bot>.csv verlangt, ist ein Register-Code-Widerspruch (25c (1), nach der Wiedergabe in R48 und R50). Er wird zugunsten von R39 aufgelöst; R39 ist damit bestätigt und wird nicht berichtigt. | D |
| R69 | 53.4 | (c) | 11405 | „Dafür“ in R60 (c) bindet ebenso nur die Gleichheit der zwei Träger. | S ¹ |
| R71 | 53.6 | — | 11419 | R64 (a) („erster Kurstag“) und R66 (e) meinen diesen Tag. | S ¹ |
| R72 | 53.7 | (b) | 11426 | (b) Benchmark-Tag des Bots im Sinn von 23.3, R64 und R66 ist ein Tag, an dem mindestens ein nach 3b (b) handelbares Symbol des Bots einen Kurs trägt; ausgenommen ist der Tag aus R71. Ein Handelstag, an dem kein handelbares Symbol einen Kurs trägt, ist kein Benchmark-Tag. | S (Begriff, von R66 (e) benutzt) ¹ |
| R72 | 53.7 | (c) | 11426 | (c) Der Zellen-Erzeuger bewertet eine offene Position an einem Tag ohne Kurs ihres Symbols zum letzten Kurs; die Position trägt an diesem Tag Rendite 0 und bleibt in der Exposure. | D |
| R72 | 53.7 | (c) | 11426 | Er berichtet je Bot die Zahl solcher Positionstage (Bauart 24.6). | S |
| R72 | 53.7 | (e) | 11426 | [Voraussetzung, vor dem Eintrag zu messen: die Wiederholung der Probe in der Lock-Umgebung auf dem Betriebsrechner; dass kein vorhandener Kern, den der Zellen-Erzeuger für die MtM-Reihe übernimmt, am Lückentag anders bewertet als (c).] | S |

**Durchgesehen, ohne Satz, der dem Zellen-Erzeuger etwas vorschreibt:**
- Suchwort-Treffer, die nicht den Zellen-Erzeuger betreffen: R41 Satz 1 („endet“ in „anwendet“; Zählregel `haltedauer_balken`, Listen-Erzeuger), R47 („Erzeuger“ = Listen-Erzeuger), R49 (a) („endet“ in „verwendet“), R57 („endet“ in „anwendet“), R70 (b) (Indexzeile „Handelskalender der Aktien-Tagesreihe“), R72 (a) („schreibt“ = `bh_tagesrenditen`), R72 (d) („endet“ = Kursreihe; Verfahrensmessung am Snapshot), drei Treffer in „Quelle des Grundes“ (R43, R67, R68).
- Ohne Suchwort-Treffer: R42, R44, R48, R50, R51, R52, R53, R54, R55, R56, R58, R59, R61, R62, R65, R73.

## 2. Dateien des Erzeugers und ihre Spalten/Felder

Liste der Ausgaben nach R39 (48.7, Z. 10839): `zellen.csv`, `tagesreihen/<zelle>.csv`, `benchmark_tagesreihen/<bot>.csv`, `zellenbericht.csv`, `symbole_je_falte.csv`, `herkunft.json`, Lese-Audit. Ergänzend: 50.2 (Z. 11036–11073) zitiert den Docstring `auswertung.py` Z. 36–67 (Stand `0f56aeb`, an HEAD zeichengleich); 50.2 ist kein Block.

### 2.1 `zellen.csv`

| Spalte / Feld | Fundstelle(n) |
|---|---|
| Zeilenmenge: je (Zelle, Falte), Selektionsfalten + Bestätigungsperiode; Zeilenzahl Zellen × (Selektionsfalten + 1) | R33 (Z. 10791); Docstring „genau eine Zeile je (Zelle x Falte) … Bestaetigungsperiode eingeschlossen“ (50.2, Z. 11045–11046); R46 (Probe „Zeilenzahl nach R33“) |
| Nullzeile: „Trade-Zahl 0, Sharpe 0 nach 1c, Drawdown 0“ | R33 (Z. 10791) |
| `zelle_id`, `<je Rasterachse eine Spalte>`, `falte`, `rolle` | nur 50.2 (Z. 11042) |
| `n_trades` | 50.2 (Z. 11042) ‖ R33: „Trade-Zahl“ (Z. 10791) |
| `netto_sharpe` | 50.2 (Z. 11043) ‖ R33 „Sharpe 0 nach 1c“ ‖ R66 (c) „Falten-Sharpe“, mit Sharpe-Funktion aus `kennzahlen.py`, über alle Tage der Tagesreihe in der Falte (Z. 11384) ‖ R66 (f) „auswertung.py liest netto_sharpe aus zellen.csv“ |
| `netto_rendite_pct` | nur 50.2 (Z. 11043) |
| `kapital_drawdown_pct` | 50.2 (Z. 11043) ‖ R36: „wird durch die zwei benannten ersetzt, nicht umgedeutet“ (Z. 10815) |
| `kapital_drawdown_mtm_pct` | R36 (Z. 10815; Tage des Benchmarks, Ausschnitt des durchgehenden Kapitalpfads); R66 (d) (Tage des Benchmarks) |
| `kapital_drawdown_ereignis_pct` | R36 (Z. 10815) |
| `mittlere_exposure` | 50.2 (Z. 11044) ‖ R60 (c) „Mittel der Spalte exposure der Tagesreihe … über die Tage der Falte“ (Z. 11229) ‖ R64 (a)/(d) „Tage …, an denen der Benchmark des Bots definiert ist“, „die in die Falte fallen (halboffen …)“ (Z. 11315) ‖ R68 (b) für die Bestätigungszeile (Z. 11398) |
| Zeile der Bestätigungsperiode: Bestätigungsstatistik je Zelle, Tage ab `bestaetigung_ab_effektiv`; nicht gezählte Positionen in keiner Grösse | R68 (a)–(c) (Z. 11398); R66 (c) Sharpe „ab dem Tag nach R68“ |

### 2.2 `tagesreihen/<zelle>.csv`

| Spalte / Feld | Fundstelle(n) |
|---|---|
| Dateiname | R35, R36, R39, R67: `tagesreihen/<zelle>.csv` ‖ 50.2 (Z. 11048): `<wurzel>/<bot>/tagesreihen/<zelle_id>.csv` |
| `datum` | 50.2 (Z. 11049) ‖ R67: „datum eindeutig“ (Z. 11391) |
| `netto_rendite` | 50.2 (Z. 11049) ‖ R66 (a) „Rendite 0“ an Tagen ohne Position (Z. 11384) ‖ R72 (c) „Rendite 0“ am Tag ohne Kurs (Z. 11426) |
| `exposure` | 50.2 (Z. 11049) ‖ R60 (b) „Spalte exposure“, Bewertung nach R48 (d) (Z. 11229) ‖ R63 (d) „aus derselben Rechnung wie die MtM-Reihe“ (Z. 11308) ‖ R66 (a) „Exposure 0“ (Z. 11384) ‖ R72 (c) „bleibt in der Exposure“ (Z. 11426) |
| Für welche Zellen | 50.2 (Z. 11050–11052): „Verlangt wird sie fuer jede ZULAESSIGE Zelle“ ‖ R39: `tagesreihen/<zelle>.csv` ohne Einschränkung (Z. 10839) ‖ R64 (c), R66 (e), R67: „jede Tagesreihe“ |
| Zeitraum / Tage | 50.2 (Z. 11050): „Tagesreihe ueber alle Falten“ ‖ R64 (e): „legt dieser Block nicht fest“ (Z. 11315) ‖ R66 (a): „vom 1. Januar der ersten Selektionsfalte des Bots (29.3) bis zum Ende der Bestätigungsperiode (35.1), ohne Lücke“ (Z. 11384) |
| Inhaltsregeln | R67: kein Feld leer, jeder Zahlenwert endlich, flacher Tag trägt 0 (Z. 11391) |

### 2.3 `benchmark_tagesreihen/<bot>.csv`

| Spalte / Feld | Fundstelle(n) |
|---|---|
| Dateiname | R39 (Z. 10839): `benchmark_tagesreihen/<bot>.csv`, „<markt>.csv … lies <bot>.csv“ ‖ 50.2 (Z. 11067): `<wurzel>/benchmark_tagesreihen/<markt>.csv` (Ordner unter `<wurzel>`, nicht unter `<bot>`) ‖ R64 (a), R67: `<bot>.csv` ‖ R69 (a) (Z. 11405): Widerspruch zugunsten R39 aufgelöst |
| `datum`, `netto_rendite` | 50.2 (Z. 11068) ‖ R67: `datum` eindeutig, kein Feld leer, endlich |
| Rechenweg | R39: über `benchmark.py::bh_tagesrenditen` |

### 2.4 `zellenbericht.csv`

| Spalte / Feld | Fundstelle(n) |
|---|---|
| Eine Zeile je Zelle | R34 (Z. 10801) |
| „die drei Werte aus 22.2 (Ertragsanteil der besten Selektionsfalte, des besten Symbols, der fünf besten Trades)“ — ohne Spaltennamen; bei Gesamtertrag ≤ 0 „nicht definiert“ | R34 (Z. 10801) |
| `haltedauer_median_handelstage` | R34 (Z. 10801); R35 (Z. 10808, Verwendung für L); Umrechnung Balken → Handelstage: R41 (Z. 10859) |
| `bestaetigung_ab_effektiv` | R34 (Z. 10801); R37 (i) (Z. 10822); R68 (a) (Z. 11398) |
| Feldliste im Docstring | 50.2 (Z. 11073): „führt der Docstring heute keine Feldliste“ |

### 2.5 `symbole_je_falte.csv`

| Spalte / Feld | Fundstelle(n) |
|---|---|
| je Bot und Falte: Symbolzahl, Anteil am Universum, Liste der ausgelassenen Symbole mit Grund — ohne Spaltennamen; Quelle Ladeprotokoll (42.1 D3/D7) | R38 (Z. 10832) |
| Feldliste im Docstring | 50.2 (Z. 11073): keine |

### 2.6 `herkunft.json`

| Spalte / Feld | Fundstelle(n) |
|---|---|
| `teile` (37.4), „gerechneter Datenstand-Hash (46.7 (b))“ | R39 (Z. 10839) |
| „Commit-Hash, Datenstand-Hash, Register-Hash - siehe herkunft.py“ | 50.2 (Z. 11055) |

### 2.7 Weitere Ausgaben ohne Datei- oder Feldnamen in den Blöcken

| Gegenstand | Fundstelle |
|---|---|
| Lese-Audit (5e); zweiter Lauf darin sichtbar | R39 (Z. 10839); R40 (Z. 10852); R46 (Probe) — Feldliste: 50.2 (Z. 11073) „keine“ |
| Bericht je Bot zur Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte“ (aus 34.5) | R43 (Z. 10873) |
| Hashes aller Ausgaben „im Bericht“ | R40 (Z. 10852) |
| Zahl der Positionstage ohne Kurs je Bot („berichtet“) | R72 (c) (Z. 11426) |
| Tatsachennotiz der Abnahme mit Hash des Test-Snapshots | R46 (Z. 10894) |

## 3. Marken unter zitierten Blöcken

Alle ⭐-Marken in den Abschnitten der Blöcke, deren Sätze in Teil 1 stehen:

| Block (Abschnitt) | Registerzeile | Marke (Wortlaut) |
|---|---|---|
| R33 (48.1) | 10794 | ⭐ **48.1 R33 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026). |
| R37 (48.5) | 10825 | ⭐ **48.5 R37 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026). |
| R39 (48.7) | 10842 | ⭐ **48.7 R39 ERGÄNZT durch R67 (53.2)** (Fable 02c R67, TB-132, 04.10.2026). |
| R39 (48.7) | 10845 | ⭐ **48.7 R39 ERGÄNZT durch R69 (53.4): R39 ist bestätigt** (Fable 02c R69, TB-132, 04.10.2026). |
| R60 (51.5) | 11232 | ⭐ **51.5 R60 (a) PRÄZISIERT durch R63 (52.1)** (Fable 02a R63, TB-130, 02.10.2026). |
| R60 (51.5) | 11235 | ⭐ **51.5 R60 (b) und (c) PRÄZISIERT durch R64 (52.2)** (Fable 02a R64, TB-130, 02.10.2026). |
| R60 (51.5) | 11238 | ⭐ **51.5 R60 PRÄZISIERT durch R69 (53.4)** (Fable 02c R69, Unterpunkt (c), TB-132, 04.10.2026). |
| R64 (52.2) | 11318 | ⭐ **52.2 R64 ERGÄNZT durch R66 (53.1)** (Fable 02c R66, zu (e), TB-132, 04.10.2026). |
| R64 (52.2) | 11321 | ⭐ **52.2 R64 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026). |
| R64 (52.2) | 11324 | ⭐ **52.2 R64 PRÄZISIERT durch R69 (53.4)** (Fable 02c R69, Unterpunkt (c), TB-132, 04.10.2026). |
| R64 (52.2) | 11327 | ⭐ **52.2 R64 PRÄZISIERT durch R71 (53.6): erster Kurstag** (Fable 02c R71, TB-132, 04.10.2026). |
| R64 (52.2) | 11330 | ⭐ **52.2 R64 PRÄZISIERT durch R72 (53.7): Benchmark-Tag** (Fable 02c R72, Unterpunkt (b), TB-132, 04.10.2026). |

Ohne Marke im eigenen Abschnitt: R34, R35, R36, R38, R40, R41, R43, R45, R46, R63, R66, R67, R68, R69, R71, R72.
Unter jeder Marke steht die Zeile „Eintrag und Stand oben bleiben zeichengleich.“
Weitere Marken in 48–53 an nicht zitierten Stellen (zur Vollständigkeit): 10922, 10925, 10928, 10931 (R48 (g)/(d)), 10963 (R51), 10984, 10987 (R53), 11031 (50.1), 11161 (50.4), 11170 (50.5), 11248, 11251 (R61), 11286 (51.9), 11340 (R65), 11358, 11361 (52.4).

## 4. Code: Treffer in `*.py` (`git grep`, versionierte Dateien, Gross-/Kleinschreibung beachtet)

### `zellen.csv` — 21 Treffer in 7 Dateien

| Datei | Anzahl | Zeilen |
|---|---|---|
| `docs/belege/TB-115/m3_kette.py` | 3 | 3, 48, 49 |
| `docs/belege/TB-88/m2_bezeichner_probe.py` | 1 | 63 |
| `docs/belege/TB-88/m2b_wege_a_b_probe.py` | 6 | 12, 14, 52, 58, 82, 84 |
| `research/vorregistrierung/auswertung.py` | 3 | 38, 321, 329 |
| `research/vorregistrierung/beispieldaten.py` | 2 | 25, 200 |
| `research/vorregistrierung/test_ersatzwerte.py` | 4 | 775, 783, 819, 828 |
| `research/vorregistrierung/test_vorregistrierung.py` | 2 | 206, 258 |

### `tagesreihen` — 33 Treffer in 6 Dateien (schliesst `benchmark_tagesreihen` und Bezeichner wie `_tagesreihen` ein)

| Datei | Anzahl | Zeilen |
|---|---|---|
| `docs/belege/TB-115/m3_kette.py` | 1 | 48 |
| `research/vorregistrierung/auswertung.py` | 4 | 45, 64, 362, 379 |
| `research/vorregistrierung/beispieldaten.py` | 9 | 146, 149, 172, 173, 205, 216, 233, 265, 283 |
| `research/vorregistrierung/test_ersatzwerte.py` | 8 | 292, 293, 296, 298, 792, 793, 796, 798 |
| `research/vorregistrierung/test_vorregistrierung.py` | 7 | 195, 425, 432, 465, 474, 491, 500 |
| `shared/zuteilung.py` | 4 | 266, 286, 629, 649 |

Davon `benchmark_tagesreihen`: `auswertung.py` 64, 379 (`f"{markt}.csv"`); `beispieldaten.py` 173, 233 (`f"{markt}.csv"`); `test_ersatzwerte.py` 293, 298, 793, 798 (`"aktien.csv"`); `test_vorregistrierung.py` 425, 465, 491 (`"aktien.csv"`); `m3_kette.py` 48. In `shared/zuteilung.py` ist es der Bezeichner `_tagesreihen` / `rechenzeit_tagesreihen_s`, kein Dateipfad.
Kein Treffer in einer Datei, deren Name oder Inhalt einen Zellen-Erzeuger trägt (Suche nur nach den zwei Wörtern).

## 5. Offene Punkte und Fragen in ERGEBNIS TB-120

Pfad: `docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md`. Abschnitt 6 „Für Fable“ (Z. 129) führt die Fragen F-1 … F-17. Z. 65: „**Offen, nicht entschieden:** O-1 … O-11 in `b_offen.md`; sie sind F-1 … F-11 unten.“ (`docs/belege/TB-120/b_offen.md`, nicht gelesen). Die letzte Spalte gibt nur an, welcher Block R33–R73 die Nummer in seiner Blockzeile nennt (gefunden, nicht bewertet).

| Nr. | Gegenstand (Kurztitel TB-120) | Zeile TB-120 | Genannt in Blockzeile |
|---|---|---|---|
| F-1 (O-1) | Zeilen in `zellen.csv` | 134 | R33 |
| F-2 (O-2) | Leere Trade-Liste | 137 | R33 |
| F-3 (O-3) | Kill-Test-Werte | 140 | R34 |
| F-4 (O-4) | Bootstrap | 143 | R34, R35 |
| F-5 (O-5) | Zwei Drawdowns | 146 | R36 |
| F-6 (O-6) | Embargo und Beginn der Bestätigung | 150 | R34, R37 |
| F-7 (O-7) | 3b (d) | 155 | R38 |
| F-8 (O-8) | Benchmark-Tagesreihe | 157 | R39 |
| F-9 (O-9) | 36.1 für Rohergebnisse | 160 | R40 |
| F-10 (O-10) | `haltedauer_balken` | 162 | R41 |
| F-11 (O-11) | Bindung der neuen Listen | 165 | R42 |
| F-12 | Ort des Zellen-Kerns | 167 | R43 |
| F-13 | Reihenfolge Listen gegen Posten 4 | 172 | R44 |
| F-14 | Ausgeführte Positionen | 175 | R45 |
| F-15 | Abnahme vor dem Tag ohne Ergebnis | 178 | R46 |
| F-16 | Übernahme von `mtm_kern.py` | 181 | — (im ganzen Register kein Treffer „F-16“) |
| F-17 | Parameterdateien | 184 | R47 |

Weitere Stellen in TB-120, die F-Nummern als wartend führen: Z. 117 (E-2 „Antworten auf F-1 … F-17“, „wartet“), Z. 121 (E-6 „wartet (F-13)“), Z. 122 (E-7 „wartet (F-12, F-14)“), Z. 191 (Übertrag F-1 … F-17 in die Fable-Sammlung), Z. 195 (`beispieldaten.py`-Docstring „hängt an F-5“).

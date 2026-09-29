# ERGEBNIS TB-121 — Kalter Leser: Register Abschnitte 0–12 ohne Vorwissen

**Auftrag:** `docs/auftraege/MAC_TB-121_kalter_leser_register_1_12.md` (Fable 25f V8/F3) · **Sitzung:** 29.09.2026 · **Ausgang:** `86e0d5e` (Schritt 0) · **Register:** `docs/VORREGISTRIERUNG_neuselektion.md`, sha256 `18e39ee29b9bd4f03a2ad4953c85c2e59558de3aaab26844ae58fb7590fca93c`, gelesen Zeilen **1–1225** (`## 13.` in Zeile 1226, wie Soll).
**Belege:** `docs/belege/TB-121/` — `0b_ausgang.txt`, `a_befunde.md` (alle 85 Befunde mit Zitat), `b_vollstaendigkeit.md`, `c_stichprobe.md`.
**Nichts geändert** ausser diesen Dateien und dem Journal: kein Code, kein Register, kein Regelwerk, nichts ausgeführt ausser `git`, `grep`, `sed`, `shasum`, `md5` und einem Prüfskript im Scratchpad, das die Zitate gegen das Register abgleicht.

## Kurzbefund

**85 Befunde:** B 19 · V 19 · W 8 · M 16 · A 15 · Z 8.

Jedes Zitat ist maschinell geprüft: zeichengleich als Teil einer Zeile in 1–1225 und höchstens 15 Wörter lang.

- **V (19):** Der Text 0–12 ist an zentralen Stellen nicht mehr selbsttragend. Faltenplan (3, 5.1, 5.3), führendes Mass (Festlegung 1), Benchmark-Tabelle (Sperrliste 4) und die Voraussetzungen (11) sind durch Marken auf die Abschnitte 15, 24, 30 und 36–46 verlegt.
- **A (15):** Die Kennzahlen, auf denen alles ruht (**Sharpe, Calmar, Exposure, DSR-Eingaben**), sind in 0–12 nicht definiert.
- **W (8) und M (16):** Die meisten betreffen Randfälle der Auswertung. Drei betreffen den Kern: welche Benchmark-Tabelle gilt, ob die Bestätigungsperiode wächst, und was Kriterium (d) bewirkt.

## Die zehn wichtigsten Befunde — „ein neuer Leser würde hier falsch bauen“

| # | Befund (Nr. in `a_befunde.md`) | Was ein kalter Leser bauen würde |
|---:|---|---|
| 1 | **Benchmark-Tabelle** (43, 32): 3 und 4.2 nennen `benchmark_drawdowns.json`, und 4.4 rechnet mit ihren Zahlen. Laut Sperrlistenpunkt 4 liest der Lauf dagegen `…_nach_wegA.json`. | Er schlägt in der historischen Tabelle nach. |
| 2 | **Faltenplan** (22, 23, 26, 31, 66): Die Tabelle in 3 und die Regeln 5.1 Nr. 1/2/3/5 und 5.3 sind ersetzt. Der gültige Plan („nach 4a“) steht ausserhalb, die Krypto-Falten fehlen in 0–12 ganz. | Er baut Verfahren A mit Trainingsfenster, Purge und Embargo — oder er kann Krypto gar nicht bauen. |
| 3 | **Führendes Mass** (21, 62): Festlegung 1 nennt die Kurve aus `equity_simulation.py`. Präzisiert wird das erst in Abschnitt 24 (tägliche MtM-Reihe). Offen bleibt, was davon in den Bericht geht. | Er rechnet die Drawdown-Bedingung auf der ereignisindizierten Kurve. |
| 4 | **Sharpe und Calmar undefiniert** (63, 64): Renditereihe, Frequenz, Annualisierung und Calmar-Formel fehlen. | Er wählt eine Definition — genau die Wahl, die das Register ausschliessen will. |
| 5 | **Exposure undefiniert, Tabellenrand offen** (69, 70): Die Exposure trägt Benchmark, Toleranz, Beta-Bereinigung und Kapitalregel. Unter 1 % und bei 0 ist das Nachschlagen nicht geregelt. | Er definiert die Exposure selbst. Den Rand behandelt er anders als der Code, der linear gegen 0 geht (C Nr. 11). |
| 6 | **Kriterium (d)** (48): Offen ist, was gilt, wenn der Gewinner eine Spitze ist, der beste Nicht-Spitzen-Punkt aber *nicht* (a) erfüllt. | Er legt eine von zwei Lesarten fest. |
| 7 | **Bestätigungsperiode** (39): Nach 5.1 Nr. 7 „wächst sie jeden Monat“, nach 5.2 endet sie am Go-Live-Schnitt. | Er nimmt Forward-Test-Daten auf oder lässt sie weg. |
| 8 | **DSR** (47, 65): Unklar ist, ob N je Bot 653 + Zellen oder der Bot-Anteil + Zellen ist. Die Eingaben der Formel fehlen. | Er errechnet drei DSR-Werte auf ungenannter Grundlage. |
| 9 | **Voraussetzungen** (60, 36): Der Text spricht von „den beiden Bug-Fixes“, Abschnitt 11 hat aber drei Unterabschnitte, und die Marke führt alle drei. | Er startet den Lauf mit 11.3 offen, oder er hält 11.2 für erledigt. |
| 10 | **Falten-Drawdown** (49): Unklar ist, ob der Pfad je Falte neu gestartet wird oder ob es ein Ausschnitt des durchgehenden Pfads ist. | Die Drawdowns unterscheiden sich systematisch, sobald eine Falte unter einem früheren Hoch beginnt. |

## Tabelle B — Vollständigkeitstest, kalt angewandt

| Baustein | aus 0–12 schreibbar | was fehlt |
|---|---|---|
| **Selektionsstatistik** (Median des Netto-Sharpe über die Selektionsfalten) | **nein** | Definition des Netto-Sharpe (Renditereihe, Frequenz, Annualisierung) — 63; welche Falten es sind (Aktien nur in einer ersetzten Tabelle, Krypto gar nicht) — 22, 23, 66; Format der Rohergebnisse — 68. Vorhanden: Median, „ohne Zinsabzug“, Falten ohne Trade = 0 (5.1 Nr. 8). |
| **Drawdown-Bedingung** | **teilweise** | Formel und „alle Selektionsfalten“ stehen (4.1, 4.2). Es fehlen: welche Kurve (Präzisierung in Abschnitt 24) — 21, 62; wie der Falten-Drawdown gemessen wird — 49; Definition der Exposure — 69; Nachschlagen unter 1 % und bei 0 — 70; bei welcher Exposure `DD_Toleranz` gilt — 50; welche Tabellendatei — 43, 32; Krypto-Tabelle — 67. |
| **Plateau-Regel** | **ja, bis auf eine Lücke** | Nachbarschaft, Selbstzählung, Spitzenformel, nicht existierende Zellen, unzulässige Nachbarn und Gleichstand sind festgelegt (6, 12). Es fehlt: Bildung des Zellennamens für den Gleichstand — 73; Reihenfolge der Zusatzstufen folgt nur aus der Tabellenreihenfolge in 3. |
| **Abbruchkriterium (a)** | **nein** (nur wegen Sharpe) | Wie Selektionsstatistik — 63. |
| **Abbruchkriterium (b)** | **ja** | Kleine Mehrdeutigkeit „alle Falten“ gegenüber „alle Selektionsfalten“ — 53. |
| **Abbruchkriterium (c)** | **nein** | Calmar und Annualisierung des Alpha — 64; Benchmark-Konstruktion statisch oder täglich gleichgewichtet — 51; point-in-time-Regel für Aktien — 4; mittlere Exposure — 69. Vorhanden: Kleinste Quadrate auf Tagesrenditen, gemeinsame Tage, weniger als drei ⇒ Abbruch, „BEIDES“, Calmar bei DD 0 = 0,0. |
| **Abbruchkriterium (d)** | **nein** (eine Lesart fehlt) | Was geschieht, wenn der beste Nicht-Spitzen-Punkt (a) *nicht* erfüllt — 48. „Bester Nicht-Spitzen-Punkt“ selbst ist definiert (7). |
| **Kapitalregel** | **ja** | Die drei Sätze stehen wörtlich in 7.1 und werden nur ausgegeben. Offen nur für die spätere Umsetzung, nicht für das Skript: welche mittlere Exposure — 54. |
| **Bericht** (Abschnitt 8) | **teilweise** | Die Kennzahlenliste steht vollständig, ebenso Festlegung 12 und die Regel „alles wird berichtet“. Es fehlen: Calmar — 64; Zufalls-Timing-Einzelheiten — 56; drei tiefste Falten-Drawdowns bei weniger als drei Falten — 75; Quelle der berichteten Drawdowns (MtM oder ereignisindiziert) — 62; Umfang der Bestätigungsperiode — 39; Ausgabeformat nur am Beispiel der Risikoappetit-Zeile; Ausgänge 0/2 erst über Marke 43.1 — 37. |
| **DSR** | **nein** | Eingaben der Formel — 65; welches N je Bot — 47, 78; Clusterregel ≥/> und Korrelationsmass — 55. Vorhanden: drei Werte, Sicherheitsabstand-Satz, Normalverteilung über `math.erf`, Umkehrung nach Acklam, „Bericht, nicht Tor“. |
| **Faltenplan** | **nein** | Die Tabelle in 3 und die Regeln in 5.1/5.3 sind durch Abschnitt 15 ersetzt — 22, 23, 26; gültig ist „der Plan nach 4a“ — 31; Krypto-Falten fehlen ganz — 66. Übrig aus 0–12: Go-Live-Schnitt 2026-09-01 ausschliesslich, 2020/2022 sind Testfalten, Faltenlänge 1 oder 2 Jahre (Schwelle 30), letzte Falte ist Bestätigungsperiode. |
| **Benchmark** | **nein** | Konstruktion (statisch gegen täglich gleichgewichtet) — 51; point-in-time-Regel — 4; Krypto — 67; welche Tabelle — 43; Exposure — 69; Interpolationsrand — 70. Vorhanden: Nachschlagen mit linearer Interpolation zwischen Stützstellen, `DD_Toleranz(e)` als Median. |

**Ergebnis:** Von zwölf Zeilen sind drei aus 0–12 schreibbar ((b), Kapitalregel, Plateau mit einer Lücke beim Zellennamen), zwei teilweise (Drawdown-Bedingung, Bericht) und sieben nicht (Selektionsstatistik, (a), (c), (d), DSR, Faltenplan, Benchmark). Die grössten Einzellücken sind die fehlenden Definitionen von **Sharpe, Calmar und Exposure** und dass der **Faltenplan** ausserhalb 0–12 steht.

*Zur Einordnung:* Abschnitt 12 beantwortet eine andere Frage mit Ja: ob das Skript *ohne ein Ergebnis gesehen zu haben* fertig wurde. Hier gefragt war, ob es *allein aus dem Text 0–12* entstehen könnte. Die Antworten widersprechen sich nicht: die Lücken oben sind vermutlich im Code oder in späteren Abschnitten geschlossen — geprüft wurde das nicht.

## Stichprobe C — Text gegen Code

⚠️ Die im Auftrag als Beispiele genannten `auswertung.py::kapitalregel` (Zeile 788) und `registerdaten.SPITZEN_SCHWELLE` (Zeile 926) liegen in Textreihenfolge auf Platz 13 und 14 und sind deshalb **nicht** in der Stichprobe. `SPITZEN_SCHWELLE = 0.50` wurde beim Lesen von `FESTLEGUNGEN` mitgesehen (`registerdaten.py:98`, direkt unterhalb) — nicht geprüft, nur vermerkt. `benchmark.py::erlaubt` ist Nr. 10.

| # | Bezeichner | genannt in Zeile | gefunden (Datei:Zeile am `86e0d5e`) | passt | Satz |
|---:|---|---:|---|---|---|
| 1 | `research/vorregistrierung/registerdaten.py::FESTLEGUNGEN` | 52 | ja, `registerdaten.py:69` | ja | Dict mit zwölf Einträgen, Nummern und Kurztexte entsprechen der Tabelle in 1; Nr. 6 trägt im Code die −28-%-Begründung aus 4.3, Nr. 12 den Satz ohne den kursiven Nachsatz. |
| 2 | `notifications/manual_close.py::allokation()` | 132 | ja, `manual_close.py:458` | ja | Liefert `ALLOCATION_PCT` als Anteil samt Quelldatei; `floor(1/…)` rechnet sie nicht selbst, das Register sagt auch nur „gelesen über“. |
| 3 | `strategies/elliott_wave/equity_simulation.py` ohne `max_concurrent_positions` | 154–155 | ja, Datei vorhanden; `max_concurrent` kommt **0-mal** vor | ja | Die behauptete Abwesenheit stimmt. |
| 4 | `strategies/elliott_wave_stocks/multi_symbol_optimise.py:39` `STOP_LOSS_RANGE` | 173–174 | ja, aber in **Zeile 44** | ja | Wert `[2.0, 3.0, 5.0, 8.0]` mit Kommentar „erweitert (bis 8%) nach Erkenntnis aus compare_exit_rules.py“ wie beschrieben; die Zeilennummer 39 gilt für einen ungenannten Commit (Abschnitt 0 erlaubt das für alte Abschnitte). |
| 5 | `auswertung.py` (`markierungen`) | 178 | ja, `auswertung.py:714` | ja | Schlüssel `markierungen` setzt „Spitze“, „Kante“, „nicht zulaessig“. ⚠️ Randbefund: „ohne Limitachse“ (2.4, 8) steht dort nicht, `grep` findet es in `auswertung.py` 0-mal; ob es anderswo gesetzt wird, ist nicht geprüft. |
| 6 | `backtest_rsi2.py` `SMA_TREND_PERIOD = 200` (rsi2_mean_reversion) | 203 | ja, `strategies/rsi2_mean_reversion/backtest_rsi2.py:88` | ja | Weiterhin Modulkonstante, passt zu „muss durchgereicht werden“ und zur Marke „11.3 offen“. |
| 7 | `live_params.py` `bb_squeeze_percentile`, `bb_lookback` (beide Volatility-Breakout-Bots) | 204–205 | ja, als `BB_SQUEEZE_PERCENTILE`/`BB_LOOKBACK` in `volatility_breakout/live_params.py:22–23` und `volatility_breakout_crypto/live_params.py:40–41` | ja | In beiden `multi_symbol_optimise.py` kommen die Namen 0-mal vor — passt zu „aber nicht im Optimierer“. Der Text schreibt die Namen klein, der Code gross. |
| 8 | `registerdaten.geometrische_stufen()` | 211 | ja, `registerdaten.py:238` | ja | Bricht ab bei Faktor ausserhalb 1,5–2,0 — und zusätzlich bei weniger als 3 oder mehr als 5 Stufen, was der Satz in 2.7 nicht nennt. |
| 9 | `lineare_stufen()` (registerdaten) | 212 | ja, `registerdaten.py:255` | ja | Bricht ab, wenn gerundete Stufen zusammenfallen; ebenfalls Stufenzahl 3–5 erzwungen. |
| 10 | `research/vorregistrierung/benchmark.py::erlaubt` | 447 | ja, `benchmark.py:324` | ja | `min(DD_RELATIVER_FAKTOR × dd_benchmark, dd_toleranz)`; nimmt die beiden Werte, nicht die Falte. |
| 11 | `benchmark.py::nachschlagen` | 465 | ja, `benchmark.py:224` | ja | Lineare Interpolation zwischen Stützstellen wie beschrieben. Der Code regelt zusätzlich, was der Text offen lässt (Befund 70): Exposure wird auf 0–1 begrenzt, bei 0 ist das Ergebnis 0, unter der ersten Stützstelle linear gegen 0. |
| 12 | `beispieldaten.py::jahre_aus_register_5_1_nr_4` | 582 | ja, `beispieldaten.py:68` | ja | Regulärer Ausdruck auf genau die Zeilenform aus 5.1 Nr. 4, genau ein Treffer, sonst `None` — wie die Marke sagt. |

**Ergebnis:** 12 von 12 gefunden, 12 von 12 passen zum beschriebenen Verhalten. Eine Zeilenangabe weicht ab (Nr. 4, 39 → 44), zwei Funktionen tun mehr, als der Text sagt (Nr. 8/9 Stufenzahl, Nr. 11 Randverhalten), und eine Markierung aus dem Text ist im genannten Schlüssel nicht zu sehen (Nr. 5).

## Für Fable

Jeder Befund der Arten W, M und A als Frage, mit Zeile und Zitat, ohne Neigung. Nummern wie in `a_befunde.md`.

### Widersprüche (W)

39. **Wächst die Bestätigungsperiode mit dem Forward-Test (5.1 Nr. 7), oder endet sie am Go-Live-Schnitt 2026-09-01 (5.2)?** — Zeile 596 / 617–619, Zitat: „Und sie wächst jeden Monat.“
40. **Sind `ableitung` bei `bb_squeeze_percentile` oben und `methode` bei der Stop-Zusatzstufe und bei `bb_lookback` unten weitere Ausnahmen neben den zwei in 2.2 benannten, oder fallen sie unter diese beiden?** — Zeile 119–126 / 264, 279, 340, 356, 360, Zitat: „Zwei Grenzen stützen sich auf keine davon.“
41. **Gilt die Stufungsregel aus 2.7 (geometrisch, Faktor 1,5–2,0) für die Quantil-Achsen `rsi_threshold` und `adx_threshold`, oder ist für sie eine andere Stufungsart vorgesehen, und wo steht sie?** — Zeile 209–213 / 254, 257, 272, Zitat: „für Skalenparameter (Faktor 1,5 bis 2,0, drei bis fünf“
42. **Hat Festlegung 4 in ihrem Wortlaut ein Exposure-Argument, oder ergibt es sich erst aus 4.2?** — Zeile 59 / 467–470, Zitat: „Da der Benchmark-Drawdown nach“
43. **Sind die Zahlen in Abschnitt 3 (Benchmark-Tabelle) und 4.4 die der Tabelle, die der Lauf liest, oder die des historischen Stands `benchmark_drawdowns.json`?** — Zeile 408, 461–465, 511 / 931–933, 945–951, Zitat: „Die vollständige Tabelle (1 % bis 100 % in Schritten von 1 %)“
44. **Welche Prüfungs- und Mutationsprobenzahl gilt für den Stand, an dem das Register gelesen wird: 165 und acht (Marke 40.7) oder 196 und sieben (Marke 41.1)?** — Zeile 1206–1208 / 1211–1214, Zitat: „der Test zählt heute 165 Prüfungen (40.1)“
45. **Gilt die Fundstellenregel aus Abschnitt 0 auch für Marken, die Wortlaut aus Abschnitten ab 38 wiedergeben, etwa `registerdaten.py:605` in der Marke aus 42.3?** — Zeile 16–21 / 730, Zitat: „die zweite Deutungsstelle (`registerdaten.py:605`)“
46. **Welcher Stand gilt für das Register: der im Kopf genannte 14.09.2026 oder der Stand der jüngsten Marke?** — Zeile 3 / 16–23 … 1220–1222, Zitat: „Stand: 14.09.2026. Dies ist das Register.“

### Mehrdeutigkeiten (M)

47. **Wird die DSR je Bot mit N = 653 plus den eigenen Zellen gerechnet, oder mit dem Bot-Anteil `N_historisch` plus den eigenen Zellen?** — Zeile 65 / 369–380, 845–848, Zitat: „N = 653 plus die Zellen dieses Laufs, je Bot getrennt.“
48. **Was gilt, wenn der Gewinner eine Spitze ist und der beste Nicht-Spitzen-Punkt (a) nicht erfüllt: bleibt der Bot mit der Spitze, oder wird der Nicht-Spitzen-Punkt gespielt?** — Zeile 753, Zitat: „der beste Nicht-Spitzen-Punkt erfüllt (a)“
49. **Wird der Kapital-Drawdown einer Falte auf einem je Falte neu gestarteten Kapitalpfad gemessen, oder als Ausschnitt eines durchgehenden Pfads?** — Zeile 443–445, Zitat: „Kapital-Drawdown in dieser Falte nicht tiefer liegt als“
50. **Wird `DD_Toleranz(e)` bei der Exposure der jeweiligen Falte ausgewertet oder bei einer über die Falten gemittelten Exposure?** — Zeile 455–456, 473, Zitat: „DD_Toleranz(e) = Median über die Selektionsfalten von DD_Benchmark(f, e)“
51. **Ist der Benchmark eine statische Position mit driftenden Gewichten oder eine täglich gleichgewichtete Tagesrendite?** — Zeile 453 / 958, Zitat: „gleichgewichtete Tagesrenditen,“
52. **Welche Rasterpunkte gelten als Kante: jede Achse an ihrer ersten oder letzten Stufe, auch die Zusatzstufen „kein“ und „structural“ und die Obergrenze des Positionslimits?** — Zeile 167–170, Zitat: „Liegt der Gewinner auf einer Rasterkante, wird“
53. **Meint (b) „alle Falten“ die Selektionsfalten oder schliesst es die Bestätigungsperiode ein?** — Zeile 750 / 445, Zitat: „erfüllt die Drawdown-Bedingung in allen Falten“
54. **Über welchen Zeitraum wird das mittlere Exposure der Kapitalregel gemessen?** — Zeile 781–782, Zitat: „mittleren Exposures — nicht in Kasse, nicht zu den Überlebenden.“
55. **Verbindet die Clusterschwelle Zellen bei Korrelation ≥ 0,9 oder > 0,9, und welches Korrelationsmass gilt?** — Zeile 862–866, Zitat: „transitiv fortgesetzt (Einfachverkettung)“
56. **Wird beim Zufalls-Timing über die aneinandergehängten Selektionsfalten oder je Falte verschoben, welche Rendite wird verglichen, und wie wird das 95. Perzentil gerechnet?** — Zeile 823–828, Zitat: „so erzeugten Renditen gegen die Rendite des Satzes.“
57. **Ist die Grundlage `haltedauer` eine Hypothese oder eine Messung, und wenn eine Messung: aus gefundenen oder aus ausgeführten Trades?** — Zeile 286 / 346, Zitat: „Ein Rueckblick kuerzer als die gemessene Median-Haltedauer dieses Bots“
58. **Heisst „gefunden“ bei `elliott_wave` „unter der Kapitalschranke ausgeführt“, oder ist es eine Ausnahme vom Grundsatz aus 5.4?** — Zeile 683–684, Zitat: „greift „gefundene" über die“
59. **Welcher Lauf ist mit „nach dem Lauf“ (15.09.2026) gemeint?** — Zeile 6 / 1035, Zitat: „Fortschreibung derselben Tatsache (15.09.2026, nach dem Lauf)“
60. **Welche zwei Bug-Fixes aus Abschnitt 11 sind Voraussetzung des Laufs, und gilt 11.3 ebenfalls als Voraussetzung?** — Zeile 1020–1021, 1087, 1182–1184 / 201, 1095–1157, Zitat: „Der Lauf darf nicht beginnen, bevor die beiden Bug-Fixes“
61. **Gilt die Regel „keine Ziffer, die mit einem Live-Wert zusammenfallen kann“ nur für Grenzsätze oder auch für erzeugte Tabellentexte wie „Median 20-Balken-Spanne“?** — Zeile 104–105 / 236, Zitat: „Median 20-Balken-Spanne“
62. **Kommen „Kapital-Drawdown je Falte“ und „drei tiefste Falten-Drawdowns“ im Bericht aus der täglichen MtM-Reihe oder aus der ereignisindizierten Kurve?** — Zeile 69 / 805–807, Zitat: „die Berichtswert bleibt“

### Nicht ausführbar (A)

63. **Wie ist der Netto-Sharpe einer Falte definiert (Renditereihe, Frequenz, Annualisierung, Kostenabzug)?** — Zeile 57, 750, 775, Zitat: „Median des Netto-Sharpe über die Selektionsfalten“
64. **Wie ist Calmar definiert, und mit welchem Faktor wird Alpha annualisiert?** — Zeile 58, 752, 762, 767, 773, Zitat: „Verglichen wird Calmar gegen Calmar.“
65. **Mit welchen Eingaben wird die DSR gerechnet (welcher Sharpe, Beobachtungszahl, Schiefe, Wölbung, Streuung der Versuchs-Sharpes)?** — Zeile 874–876, Zitat: „Gerechnet wird nach Bailey/López de Prado, ohne“
66. **Wo steht der gültige Krypto-Faltenplan, und soll 0–12 auf ihn verweisen?** — Zeile 396–400, 635–636, Zitat: „Der Krypto-Faltenplan wird geschrieben, sobald TB-31 gemeldet hat“
67. **Wie wird der Benchmark-Drawdown für die Krypto-Bots gebildet, insbesondere für die 1h- und 4h-Bots?** — Zeile 410–428, Zitat: „gilt für alle Bots dieses Marktes mit gleichem Faltenplan“
68. **Wo ist das Format der Rohergebnisse beschrieben, gegen das `auswertung.py` prüft?** — Zeile 804, 1189, Zitat: „Wo die Rohergebnisse den Vertrag verletzen, bricht es“
69. **Wie ist die mittlere Exposure definiert (Grösse, Zeitpunkt, Kalender- oder Handelstage)?** — Zeile 453–455, 765–767, 823, Zitat: „in Höhe der mittleren Exposure“
70. **Wie wird unter 1 % Exposure und bei Exposure 0 in der Benchmark-Tabelle nachgeschlagen?** — Zeile 461–464, Zitat: „beiden benachbarten Stützstellen“
71. **Wie entstehen die Zwischenstufen der Quantil-Achsen, und auf welcher Verteilung (Zeitraum, Zeitrahmen, Universum) sind die ADX- und RSI-Quantile gemessen?** — Zeile 254, 257, 272, 318, 330, Zitat: „Die Schwelle ist als Quantil der gemessenen ADX-Verteilung des Universums gesetzt“
72. **Welche Sätze begründen die Grenzen von `t3_slow_length`, `donchian_period` oben und `stop_mode` unten und oben?** — Zeile 253, 261, 262, 276, 277 / 286, Zitat: „Ein Satz je Grenze, der“
73. **Wie wird der Zellenname gebildet, der bei Gleichstand alphabetisch entscheidet?** — Zeile 739, Zitat: „dann der alphabetisch erste Zellenname“
74. **Wie gross ist die Stichprobe beim Hash-Vergleich nach 10.1, und wie wird sie gezogen?** — Zeile 1067–1069, Zitat: „Stichproben-Hash-Vergleich.“
75. **Wie wird der Mittelwert der drei tiefsten Falten-Drawdowns bei weniger als drei Selektionsfalten gebildet?** — Zeile 806, Zitat: „Mittelwert der **drei tiefsten** Falten-Drawdowns“
76. **Welche Fill-Konvention gilt für den Ausstieg?** — Zeile 983–985, Zitat: „je Order, Ein- und Ausstieg; Einstieg zum“
77. **Wie lautet der vollständige Datenstand-Hash, gegen den geprüft wird, und soll er in 0–12 stehen?** — Zeile 1044, Zitat: „d9449faf51bffaaa…“

## Was die Sitzung ausser 0–12 gesehen hat

- **`CLAUDE.md`** des Repos — von Claude Code von selbst geladen. Darauf stützt sich kein Befund.
- ⚠️ **Das Gedächtnisverzeichnis der Sitzung** (`MEMORY.md`, von Claude Code von selbst geladen). Es enthält einzeilige Zusammenfassungen früherer Sitzungen, etwa zu Registerabschnitten 15–46, Faltenplan, Sonde, Benchmark-Tabellen. **Die Sitzung war also nicht vollständig kalt.** Kein Befund stützt sich darauf. Verweise auf spätere Abschnitte sind als V aufgenommen und nicht aus dem Gedächtnis beantwortet. Ob das Vorwissen die *Auswahl* der Befunde gefärbt hat, lässt sich von innen nicht ausschliessen.
- **Der Git-Stand beim Sitzungsbeginn** (Zweig, geänderte Dateien, Betreff der letzten fünf Commits, TB-120) — ebenfalls von selbst eingeblendet.
- **`docs/auftraege/AKTUELLER_AUFTRAG.md`** — gelesen, weil der Einfügesatz es verlangt. Die Datei ist der Zeiger auf diesen Auftrag.
- **Dieser Auftrag.**
- **Schritt 0:** `git status`, md5 und numstat der fünf Dateien. Inhalt nicht gelesen.
- **Schritt C:** nur die zwölf Definitionen in `c_stichprobe.md`, dazu drei `grep`-Zählungen: `max_concurrent` in `elliott_wave/equity_simulation.py`, BB-Namen in den zwei Optimierern, „ohne Limitachse“ in `auswertung.py`. Dabei war `SPITZEN_SCHWELLE = 0.50` sichtbar (`registerdaten.py:98`), weil die Ausgabe über `FESTLEGUNGEN` hinaus bis Zeile 98 reichte.
- **Journal:** erst **nach** Fertigstellung der Befunde und dieses Dokuments, und nur, um den Eintrag zu schreiben: Blocküberschriften und der letzte Block als Formvorlage.
- Sonst nichts: keine Abschnitte ab 13, kein `REGISTER_INDEX.md`, keine Übergaben, kein Backlog, keine `ARBEITSWEISE`/`PRUEFPRINZIPIEN`, keine `ERGEBNIS_*`/`FABLE_*`/Belege, auch nicht die Sammlung.

## In einfacher Sprache

Ich habe die ersten zwölf Abschnitte des Regelwerks gelesen wie jemand, der das Projekt nicht kennt, und aufgeschrieben, wo ich hängenbleibe. Ergebnis: 85 Stellen.

- **Das Grundgerüst ist gut lesbar.** Das betrifft den Zweck, die zwölf Festlegungen, wie der Gewinner gewählt wird (Plateau) und wann ein Bot ausscheidet.
- **Allein aus diesen zwölf Abschnitten liesse sich das Auswertungsprogramm trotzdem nicht bauen.** Drei Gründe:
  - Die wichtigsten Kennzahlen (Sharpe, Calmar, „Exposure“) werden benutzt, aber nie genau definiert.
  - Der Faltenplan (welche Jahre wofür zählen) und die gültige Benchmark-Tabelle stehen in späteren Abschnitten. Der Text hier zeigt eine ältere Fassung und verweist nur mit einer Marke weiter.
  - Einige Stellen sagen Verschiedenes, etwa ob die Bestätigungsperiode mitwächst oder am 1. September endet.
- **Die Stichprobe im Code ging glatt.** Alle zwölf genannten Funktionen und Konstanten gibt es, und sie tun, was der Text sagt. Eine Zeilennummer ist verrutscht. Zwei Funktionen tun etwas mehr, als der Text beschreibt.

Die Fragen im Abschnitt „Für Fable“ sind so gestellt, dass Fable sie beantworten kann, ohne dass die Sitzung eine Antwort nahelegt.

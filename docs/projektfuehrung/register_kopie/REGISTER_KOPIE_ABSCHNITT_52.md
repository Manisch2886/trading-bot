# REGISTER-KOPIE Abschnitt 52 (von 0–54) — Register-Z. 11329–11407 — Commit 9b7b06065ebdae3f36f3102306c76bb844300e90 — 2026-10-05 — Original sha256 8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc — KOPIE, nicht das Register

## 52. Fable 02a — Registerblock R63–R65 (TB-130)

Reines Eintragen von Registertext, Bauart wie 51. Quelle: `docs/projektfuehrung/FABLE_ANTWORT_2026-10-02a_exposure_tage_laufbereich_marken.md`, md5 `a7821eeb4f61faad5f74f72ec7201797`, 21 709 B, im Repo seit Commit `b0c7a35`, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R63)“, Z. 112–119. Die Datei hat der steuernde Chat am 02.10.2026 aus Fables Ablage übertragen, zweifach unabhängig, `cmp` gleich; das Lesewerkzeug lieferte Text und keine Datei, die Bytegleichheit mit der Ablage ist deshalb nicht gemessen. Der Eröffnungstext des Chats (`docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02_eroeffnung.md`) und die Anfrage liegen seit `b0c7a35` im Repo; dieser Kopf nennt Datei, md5 und Commit, das ist die Bindung nach R56 (b). Je Block ein Unterabschnitt in der Reihenfolge des Codeblocks, der Block als Blockzitat, darunter die Kette. Die Nummern 52.1–52.3 hat der steuernde Chat vergeben (Auftrag TB-130, Einzelfreigabe des Betreibers), nicht Fable. Gesetzt sind zwölf Marken: die fünf, die R65 (b) aufzählt, und sieben nach der Regel in R65 (a) an den Orten, die R63, R64 und R65 selbst als Bezug nennen (4.2, 48.16, 48.19, 51.5 zweimal, 51.6, 51.9). Diese sieben hat der steuernde Chat bestimmt, nicht Fable. Die Marke an 25.2 steht direkt unter dem berichtigten Satz, vor der Marke aus R53 (R65, Quelle des Grundes, 34.3). ⛔ In Abschnitt 9, in Abschnitt 10 und im ERZEUGT-Block von Abschnitt 3 steht keine neue Marke (R65 (d)). Die Voraussetzungen, die Fable „zu messen“ nennt, stehen mit Befund in 52.4; was offen bleibt, steht in 52.5. 52.4 und 52.5 sind Text des steuernden Chats, nicht Fables.

### 52.1 R63 — Präzisierung zu R60 (a) (51.5) und Bestätigung der Lesart 51.9 (Reichweite: die Stelle, nicht der Ordner)

> R63 — Präzisierung zu R60 (a) (51.5) und Bestätigung der Lesart 51.9 (Reichweite: die Stelle, nicht der Ordner). (a) Massgeblich in R60 (a) ist, ob eine Stelle die Grösse bildet, nicht in welchem Ordner sie liegt. Eine Stelle bildet die mittlere Exposure, wenn sie je Tag den Anteil des Kapitals in offenen Positionen rechnet oder daraus ein Mittel; eine Stelle, die Positionen liefert, bildet sie nicht. (b) In der Voraussetzung von R60 (a) lies „research/exposure_messung/“ als „die Stellen, die die Grösse zum Einstand bilden: research/exposure_messung/exposure_kern.py und research/exposure_messung/auswertung.py (50.1)“. Sie liegen ausserhalb von Sperrliste und Laufbereich (51.8) und legen keine Definition fest; es gilt R48 (d) mit R60 (b). Die Lesart 51.9 ist damit bestätigt. (c) research/exposure_messung/bot_lauf.py gehört zum Laufbereich (51.8). [Voraussetzung, zu messen, durch Lesen des Codes und nicht durch Wortsuche: dass bot_lauf.py keinen Anteil des Kapitals in offenen Positionen und kein Mittel daraus rechnet.] Trifft sie nicht zu, ist das ein Register-Code-Widerspruch nach 25c (1) zur Bewertung in R48 (d) und R60 (b) und wird gemeldet, nicht eingetragen. (d) Der Zellen-Erzeuger bezieht weder Positionen noch Exposure aus bot_lauf.py oder dessen Ausgabe; die Positionen kommen aus simuliere_portfolio (R45), die Spalte exposure aus derselben Rechnung wie die MtM-Reihe (R60 (c)).
> Quelle des Grundes: R60 (a), erster und zweiter Satz (die Regel nennt Code und Grösse; den Ordner nennt nur die Voraussetzung), R48 (d) („der Registertext folgt dem Code, wo er ihn hat“), R50, 38.2 (Fundstellen als Datei und Bezeichner; hier nach R49 (e)), R45 (kein zweiter Rechenweg), 24.4 (bewertet zum Marktpreis, nicht zum Einstand), 25c (1). Kein Ergebnis.

**Kette:** Marken: 51.5 (R60); 51.9. Voraussetzung gemessen: 52.4. Offen: 52.5 Nr. 4.

### 52.2 R64 — Präzisierung zu R48 (d) (48.16) und zu R60 (b) und (c) (51.5) (über welche Tage die mittlere Exposure gemittelt wird)

> R64 — Präzisierung zu R48 (d) (48.16) und zu R60 (b) und (c) (51.5) (über welche Tage die mittlere Exposure gemittelt wird). (a) „Handelstage des Zeitraums“ in R48 (d) lies: die Tage des Zeitraums, an denen der Benchmark des Bots definiert ist (23.3), wie benchmark_tagesreihen/<bot>.csv sie führt (R39); die Tatsachennotiz zu 23.3 (erster Kurstag) gilt mit. Das gilt für die mittlere Exposure je (Zelle, Falte) (4.2) und für die des Gewinners über seine Selektionsfalten (7 (c)). (b) Der Schnitt auf die gemeinsamen Tage in auswertung.py::beta_bereinigung ist die Regel aus Abschnitt 7 („Beide Reihen werden auf gemeinsame Tage gebracht“; „über dieselben Tage“) und kein Register-Code-Widerspruch. Ein Tag der Tagesreihe ohne Benchmark-Tag geht in keine mittlere Exposure ein; er ist kein Befund. (c) Ein Benchmark-Tag des Bots in einer Falte des Faltenplans, zu dem die Tagesreihe einer Zelle keine Zeile führt, ist ein Befund über den Erzeuger, kein Ausgang (Bauart R33). Der Zellen-Erzeuger prüft im Lauf für jede Tagesreihe, dass sie jeden solchen Tag führt (auch flache Tage, 1a), und endet sonst mit 2. Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf trägt sie selbst. (d) „Über die Tage der Falte“ in R60 (c) lies: über die Tage nach (a), die in die Falte fallen (halboffen wie im Faltenplan; 2a). Der Wert des Gewinners in beta_bereinigung ist dann das mit der Zahl dieser Tage gewichtete Mittel seiner Werte je Selektionsfalte in zellen.csv; die Abnahme nach R46 prüft auch diese Gleichheit, mit Gegenprobe. (e) Welche Tage die Tagesreihe über die Tage nach (a) hinaus führt, legt dieser Block nicht fest. auswertung.py wird für nichts davon geöffnet. [Voraussetzung, zu messen: dass beta_bereinigung ausser dem Schnitt auf die gemeinsamen Tage keinen Tag weglässt; dass an einem Tag ohne Benchmark-Tag keine Zelle eine offene Position führen kann, ausser am Tag aus der Tatsachennotiz zu 23.3.]
> Quelle des Grundes: Abschnitt 7, Präzisierungen zu (c); 24.2 („auf denselben Tagen wie der Benchmark (3b (c))“); 23.3 („Bot und Benchmark leben an jedem Tag in derselben Menge“; ein Tag ohne handelbares Symbol „gehört nicht zum Benchmark“); 23.2, Grund 2 (keine Grösse aus Nichtteilnahme); 4.2; R36; 1a; 2a; R33; R46. Bekannte Richtung der Wirkung, nicht Grund: Unter der zweiten Voraussetzung ist in einer Falte, in der der Benchmark nicht an allen Tagen definiert ist, das Mittel nach (a) nie kleiner als das Mittel über alle Tage der Falte; die Grösse ist nicht gemessen und für die Entscheidung ohne Belang (Bauart 24.3). Kein Ergebnis.

> ⭐ **52.2 R64 ERGÄNZT durch R66 (53.1)** (Fable 02c R66, zu (e), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **52.2 R64 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **52.2 R64 PRÄZISIERT durch R69 (53.4)** (Fable 02c R69, Unterpunkt (c), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **52.2 R64 PRÄZISIERT durch R71 (53.6): erster Kurstag** (Fable 02c R71, TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **52.2 R64 PRÄZISIERT durch R72 (53.7): Benchmark-Tag** (Fable 02c R72, Unterpunkt (b), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **52.2 R64 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (d), TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 4.2; 48.16 (R48); 51.5 (R60). Voraussetzung gemessen: 52.4. Offen: 52.5 Nr. 1 bis 3, 5 bis 7 und 9.

### 52.3 R65 — Marken nach R61 (Regel und fünf Orte; eine Berichtigung in „lies“-Form)

> R65 — Marken nach R61 (Regel und fünf Orte; eine Berichtigung in „lies“-Form). (a) Die Aufzählungen in R51 und R61 (b) wenden die Regel aus 34 an und schliessen sie nicht ab. Gibt ein Block einem benannten Ort ein „lies“, eine Ergänzung oder eine Bestätigung, trägt der Ort die Marke, auch wenn die Aufzählung des Blocks ihn nicht nennt; ausgenommen bleiben die Orte nach R61 (b), zweiter Satz. Eine Tabelle von Befunden ist keine Statusliste im Sinn von R61 (b), soweit ein Block den Befund einer Zeile ergänzt oder berichtigt. Eine Bestätigung trägt das Markenwort ERGÄNZT mit dem Zusatz, was bestätigt ist (Bauart der Marke an 46.9). (b) Danach sind nachzutragen, der alte Satz bleibt zeichengleich: 47.9 (R26) — BERICHTIGT durch R61 (51.6), Unterpunkt (c). 47.13 (R30) — BERICHTIGT durch R61 (51.6), Unterpunkt (c). 25.2 — BERICHTIGT durch R62 (51.7), Unterpunkt (a), und durch diesen Block, Unterpunkt (c). 50.1, Zeile R48 (d) — ERGÄNZT durch R60 (51.5), Unterpunkt (d), und 51.8. 50.4, Schlusssatz — ERGÄNZT durch R57 (51.2): der Schlusssatz ist bestätigt. (c) Berichtigung zu 25.2: „der 150. Balken liegt am 2018-01-14“ lies „der Balken mit 150 Balken davor liegt am 2018-01-14; der 150. Balken ist der 2018-01-13“. Das Ergebnis von 25.2 (Bedingung (i) ist am 1. Januar 2018 nicht erfüllt) bleibt unberührt, ebenso „warm ab 2018-01-14“ (32.2, nach R62 (a)). (d) Die Marken zu R26 und R30 stehen in 47; in Abschnitt 10 steht weiter keine Marke, R30 bleibt dort Indexzeile.
> Quelle des Grundes: 34 (Kopf: die Marke steht am alten Ort; 34.3: ein „lies“ trägt die Marke direkt unter dem berichtigten Satz), 43.0, R61 (b), erster Satz, und (c), R62 (a) mit der Messung in 51.8 (Index 149 = 2018-01-13, Index 150 = 2018-01-14, zwei Dateien), R57, R60 (d), die Marken an 46.9 und unter 48.16. Kein Ergebnis.

> ⭐ **52.3 R65 PRÄZISIERT durch R70 (53.5)** (Fable 02c R70, Unterpunkt (a), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 48.19 (R51); 51.6 (R61); nachgetragen nach (b): 25.2; 47.9 (R26); 47.13 (R30); 50.1, Zeile R48 (d); 50.4, Schlusssatz. In Abschnitt 10 steht weiter keine Marke (R65 (d)).

### 52.4 Voraussetzungen und Befunde

Tatsachennotizen des steuernden Chats zu den Voraussetzungen, die Fable in 02a „zu messen“ nennt. Gemessen am 02.10.2026 am Stand `1833839`, nur lesend, durch einen Helfer des steuernden Chats, der den Code gelesen hat; die Sitzung TB-130 hat in Schritt 0 die genannten Zeilen und Zählungen am Commit `b0c7a35` nachgemessen (`docs/belege/TB-130/0d_vorpruefung.txt`). Aussagen über ein Fehlen (kein Tagesraster, kein Filter, kein Erzeuger) sind Lesung des Helfers; gezählt sind nur Aufrufe von `mean` (`.mean(`, `np.mean`) in `bot_lauf.py` und `dropna` in `auswertung.py`, je 0. Zeilenangaben gelten am Commit `b0c7a35`. Kein Ergebnis gelesen (27.1).

| R | Voraussetzung (Fable) | gemessen | Stand |
|---|---|---|---|
| R63 (52.1) (c) | `bot_lauf.py` rechnet keinen Anteil des Kapitals in offenen Positionen und kein Mittel daraus; zu messen durch Lesen, nicht durch Wortsuche | `research/exposure_messung/bot_lauf.py` ganz gelesen: Positionen Z. 227–231 (`allocation` Z. 229, `capital_after` Z. 230), geschrieben Z. 242 als `<BOT>_positionen.csv` mit den Spalten `trade_zeile`, `symbol`, `entry_time`, `exit_time`, `pnl_pct`, `allocation`, `capital_after`. Kapital kommt als `es.STARTING_CAPITAL` (Z. 135–136, 246, 254–255) und als `final_capital` (Z. 253–254) vor; Z. 254 teilt beide zur Gesamtrendite. Kein Tagesraster, kein Aufruf von `mean` | trifft: kein Anteil je Tag, kein Mittel |
| R63 (52.1) (d) | Bestand, keine Voraussetzung Fables | `shared/zuteilung.py:657` `def simuliere_portfolio` (R45: `shared/zuteilung.py::simuliere_portfolio`). Die neun `strategies/*/equity_simulation.py` führen je ein `simulate_portfolio`; `bot_lauf.py:133–136` ruft `es.simulate_portfolio` | R63 (d) nennt die Funktion aus R45 |
| R64 (52.2), erste | `beta_bereinigung` lässt ausser dem Schnitt auf die gemeinsamen Tage keinen Tag weg | `research/vorregistrierung/auswertung.py`: `lies_tagesreihe` (Z. 361–370) und `lies_benchmark` (Z. 378–386) lesen, prüfen Spalten und sortieren nach `datum`; kein `dropna`, kein Filter. `beta_bereinigung`: Fenstermaske Z. 510–514, Schnitt Z. 517, Auswahl Z. 522–524, Mittel Z. 528 | trifft. Fehlende Werte und doppelte Daten werden dort weder behandelt noch geprüft (52.5) |
| R64 (52.2), zweite | an einem Tag ohne Benchmark-Tag kann keine Zelle eine offene Position führen, ausser am Tag aus der Tatsachennotiz zu 23.3 | nicht entscheidbar: Den Kalender der Tagesreihe legt noch kein Code fest; `benchmark_tagesreihen` schreibt bisher kein Erzeuger des Laufs | offen (52.5). Nach 02a, „Unsicher“ 2: Trifft die Voraussetzung nicht zu, bleibt die Regel, und der Satz zur Richtung der Wirkung gilt dann nicht streng |
| R64 (52.2) (a) | Bestand, keine Voraussetzung Fables | R39 (48.7) nennt `benchmark_tagesreihen/<bot>.csv`; `auswertung.py:379` bildet `<markt>.csv` (`markt` aus `rd.BOTS[bot]["markt"]`, Z. 498); 50.2 schreibt dazu „im Zitat lies „`<bot>.csv`“ (R39)“ | Bestand. Wann der Code den Namen je Bot liest, ist nicht festgelegt; `auswertung.py` wird nach R64 (e) nicht geöffnet (52.5) |
| R65 (52.3) (c) | — | die Messung steht in 51.8 (Zeile R62 (a)): Index 149 = 2018-01-13, Index 150 = 2018-01-14, in beiden Kursdateien | trägt die „lies“-Form |

> ⭐ **52.4, Zeile „R64 (52.2), zweite“ ERGÄNZT durch R66 (53.1)** (Fable 02c R66, Unterpunkte (a) und (e), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **52.4, Zeile „R64 (52.2) (a)“ BERICHTIGT durch R69 (53.4)** (Fable 02c R69, Unterpunkt (c), TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 52.5 Was offen bleibt

| | offen | wann, wo |
|---|---|---|
| 1 | R64, zweite Voraussetzung: keine offene Position an einem Tag ohne Benchmark-Tag | Messung mit dem Zellen-Erzeuger, vor dem Tag |
| 2 | 02a, „Unsicher“ 1: Zeitachse des Falten-Sharpe in Falten mit teilweisem Benchmark (ob die Tagesreihe Tage vor dem ersten Handelbar-Tag führt); R64 (e) lässt es offen | Vorprüfung (16, 21, 29, 33), dann Anfrage an Fable; vor dem Zellen-Erzeuger |
| 3 | R64 (c) und (d): Wache im Lauf mit Ausgang 2; Probe über das tagegewichtete Mittel in der Abnahme nach R46 | mit dem Zellen-Erzeuger |
| 4 | R63 (d): der Zellen-Erzeuger bezieht weder Positionen noch Exposure aus `bot_lauf.py` | mit dem Zellen-Erzeuger (Abnahme) |
| 5 | `beta_bereinigung` behandelt und prüft weder fehlende Werte noch doppelte Daten (52.4) | Vorprüfung, ob der Datenvertrag beides ausschliesst; sonst an Fable |
| 6 | 02a, „Unsicher“ 4: ob `bestaetigung_ab_effektiv` (R37) den Beginn der Tage nach R64 für die Bestätigungsperiode verschiebt | Vorprüfung, dann an Fable |
| 7 | Benchmark-Datei: R39 nennt `<bot>.csv`, `auswertung.py:379` liest `<markt>.csv` (52.4) | Vorprüfung, dann an Fable |
| 8 | Von 51.10 sind Nr. 6 und Nr. 7 durch R63–R65 beantwortet; die Messung aus 51.10 Nr. 6 lebt in 52.5 Nr. 1 fort; 51.10 Nr. 1 bis 5 und Nr. 8 bleiben | wie dort |
| 9 | Marke an 7 (c) zu R64 (a): nicht gesetzt. Die Präzisierungen in Abschnitt 7 tragen die Regel selbst, und R61 (b) führt 7 (c) als Ort ohne Marke | nächste Anfrage an Fable |


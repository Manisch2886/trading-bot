# Bericht H2 — Fundstellen zu Fable 04.10.a, Frage 2 / Block R75 (gemessen 04.10.2026)

Nur gemessen, nichts gedeutet. Repo `$HOME/mnt/trading-bot`, HEAD `d781f1b`. Register `docs/VORREGISTRIERUNG_neuselektion.md`
(11 471 Zeilen, 906 766 Bytes). Kopien `docs/projektfuehrung/register_kopie/REGISTER_KOPIE_ABSCHNITT_<nn>.md`
(Kopfzeile jeder Kopie: Commit `ee43f5f…`, 2026-10-04). Index liegt unter `docs/projektfuehrung/REGISTER_INDEX.md`
(nicht in `register_kopie/`, wie im Auftrag genannt).

Schreibweise: „K16 Z.493“ = Kopie Abschnitt 16, Zeile 493; „Reg Z.2310“ = Zeile im Register selbst (per `grep -n` gegengeprüft).

## Ergebnistabelle

| Nr | Ergebnis | Ort |
|---|---|---|
| 1 | ja — Wortfolge gleich, aber über Zeilenumbruch mit Zitatzeichen `> `; `grep -c -F` einzeilig = 0 (Kopie und Register) | 16.6, K16 Z.493–494, Reg Z.2310–2311 |
| 2 | ja — Wortfolge gleich, über Zeilenumbruch; `grep -c -F` einzeilig = 0. Marke mit „Leck schliesst die Attribution je Position“ an 16.6: ja | 16.6, K16 Z.494–495, Reg Z.2311–2312; Marken K16 Z.518–528 (Reg Z.2335–2345) und Z.530 (Reg Z.2347) |
| 3 | ja (48.5 = R37; „zählt nicht“ 1× in (i); „keine Falte im Sinn von 4a“ wörtlich) | K48 Z.40, Reg Z.10822 |
| 4 | ja — C2-Zitat steht in 41.3 C2 selbst und zusätzlich in der Marke an 16.6; C3-Zitat in 41.3 C3 selbst und in der Marke an 16.6 | C2: K41 Z.329, Reg Z.8874; C3: K41 Z.345, Reg Z.8890; Marke 16.6: Reg Z.2338–2339 und Z.2341 |
| 5 | abweichend (A4: „Jede Mutationsprobe beisst **allein**“; A5: Überschrift „Störproben in beide Richtungen“) | 41.1 A4: K41 Z.86/89, Reg Z.8631/8634; A5: K41 Z.106/109, Reg Z.8651/8654 |
| 6 | 29.3 „ein Kapitalpfad“ wörtlich: nein. 2a: gefunden. „Ein-Pfad-Regel“ ausserhalb 16.6: ja, 1× (R68 (d)) | 29.3: K29 Z.45, Reg Z.5402; 2a = 15.4 (a): K15 Z.120–124, Reg Z.1480–1484; „Ein-Pfad-Regel“: Reg Z.2312 und Z.11398 |
| 7 | „zweiter Rechenweg“: abweichend. „Die Zuteilung läuft je Zelle einmal“: nein (nicht gefunden) | R45 = 48.13, K48 Z.105, Reg Z.10887 |
| 8 | ja | 35.1, K35 Z.29, Reg Z.6369 |
| 9 | ja (R63 (d) wörtlich „die Spalte exposure aus derselben Rechnung wie die MtM-Reihe (R60 (c))“) | R63 = 52.1, K52 Z.9, Reg Z.11308; R48 (d) = 48.16, K48 Z.130, Reg Z.10912 |
| 10 | ja (48.4 = R36; Nachrechnung im Blocktext; „24b A2“ in der Quelle des Grundes; `kapital_drawdown_mtm_pct` 3× im Blocktext) | K48 Z.33–34, Reg Z.10815–10816 |
| 11 | ja (48.2 = R34; Wortlaut „Plateau-Gewinners“) | K48 Z.19–20, Reg Z.10801–10802 |
| 12 | R33 „nie nichts“: ja; „kein Ausgang“: ja. R67 „nie leer“ wörtlich: nein (dort „kein Feld leer“ und „nie nichts (1a)“) | R33: K48 Z.9, Reg Z.10791; R67 = 53.2: K53 Z.16, Reg Z.11391 |
| 13 | ja (48.7 = R39) | R39: K48 Z.57, Reg Z.10839; 50.2: K50 Z.31/33, Reg Z.11034/11036 |
| 14 | gemessen (8 Registerzeilen, Liste unten) | s. u. |
| 15 | ja | R54 = 49.2, K49 Z.22, Reg Z.10994 |
| 16 | ja (53.3 = R68; Zitat wörtlich, Register 2×) | R68: K53 Z.23, Reg Z.11398; zweite Stelle 53.10 Nr. 2: K53 Z.86, Reg Z.11461 |
| 17 | ja (51.5 = R60, 52.2 = R64) | R60 (c): K51 Z.37, Reg Z.11229; R64 (d): K52 Z.16, Reg Z.11315 |
| 18 | ja; `bestaetigung_ab_effektiv` 7 Registerzeilen | R66 = 53.1: K53 Z.9, Reg Z.11384; Orte s. u. |
| 19 | abweichend („gezählt und berichtet“ wörtlich im Register 0×; R72 nennt 24.6 zweimal als „Bauart“) | R72 = 53.7: K53 Z.51–52, Reg Z.11426–11427; 24.6: K24 Z.224 ff., Tabellenzeile Z.249, Reg Z.4486 |
| 20 | ja (53.4 = R69) | K53 Z.30, Reg Z.11405 |
| 21 | „abschliessend“ nur in der Quelle des Grundes von R35, nicht im Blocktext; in Abschnitt 8 selbst 0×; `zellenbericht` in Abschnitt 8: 0 | R35 = 48.3: K48 Z.26–27, Reg Z.10808–10809; Abschnitt 8: K08, Reg Z.870–924 |
| 22 | gemessen: `mtm_kern.py` bildet keine Tagesrendite, nur Kapitalreihen | `research/mtm_drawdown/mtm_kern.py` (339 Zeilen) |
| 23 | gemessen | `research/vorregistrierung/auswertung.py` (860 Zeilen) |
| 24 | ja, alle acht | Überschriften in K48, K51, K52, K53; Index-Zeilen 270–390 |

## Ausschnitte je Nummer

### 1 / 2 — 16.6 (K16 Z.492–495, Reg Z.2309–2312)
Zeilen im Register (je eine Zeile, mit `> ` am Anfang):
- Z.2310: `> die Bestätigungsperiode trotzdem — diese Position wird in der`
- Z.2311: `> Bestätigungsstatistik jedoch nicht gezählt** (Attribution je Position,`
- Z.2312: `> ausdrückliche und seltene Ausnahme von der Ein-Pfad-Regel).`
Zwischen „gezählt“ und „(Attribution“ steht `**` (Ende Fettdruck). Wort in 16.6: „seltene“ (Fable-Text Z.93 schreibt „selten“).

Marken an 16.6 (nur diese zwei; kein ERSETZT, kein ERGÄNZT):
- K16 Z.518–528: „⭐⭐ **Zwei Präzisierungen zu 2d und eine Rücknahme (41.3 C1–C3, Fable 24d, TB-108, 25.09.2026):** (1) Der Deckel für Bots ohne Zeitbremse … er ist keine Leckschranke, das Leck schliesst die Attribution je Position (**41.3, C2**). (2) … **für den Gewinner auf dessen eigenen simulierten Positionen** ausgewertet …“ (Umbruch zwischen „das“ und „Leck“).
- K16 Z.530: „⭐ **16.6 PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, 01.10.2026).“

### 3 — R37 (K48 Z.40, 1482 Zeichen)
- (i), Anfang: „(i) Die Bestätigungsperiode des Selektionslaufs ist die Spanne nach 35.1 (Beginn „Bestätigung ab“, 21.4; Ende Go-Live-Schnitt, ausschliesslich; registrierter Bestand 2026-01-01/2026-09-01), gerechnet auf dem Snapshot; sie wächst nicht (5c: ein zweiter Snapshot ist ein neuer Lauf). Die Bedingun…“
- „zählt nicht“ (Zeichenposition 735; (i) beginnt bei 150, (ii) bei 920): „…Handelstag ab Beginn der Spanne, an dem keine vor der Spanne eröffnete simulierte Position des Gewinners mehr offen ist; Deckel je Bot nach 16.6/41.3 C2; eine am Deckeltag noch offene solche Position zählt nicht (Attribution je Position). Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle (bestaetigung_ab_effektiv, R34); auswertung.py nimmt den Wert der Gewinnerzelle (41.3 C3).“
- Falte (Blockende, nach (ii)): „„Alle Falten“ in Abbruchkriterium (b) sind die Selektionsfalten (4.1); die Bestätigungsperiode ist keine Falte im Sinn von 4a (35.1) und wird ausgewertet, nachdem die Auswahl steht (5.1 Nr. 7). F-6, W39, M53.“

### 4 — 41.3 C2 / C3
- C2 (K41 Z.329): „…Tatsachennotiz mit Hash der Liste, Snapshot-Hash und Commit. Der Deckel ist keine Leckschranke — das Leck schliesst die Attribution je Position —, und er ist deshalb ausdrücklich **nicht** als Maximum über alle Rasterzellen zu bemessen.“ Gegenprobe Register `grep -c -F 'das Leck schliesst die Attribution je Position'` = 1 (die Stelle in der Marke an 16.6 ist umbrochen).
- C3 (K41 Z.345): „> **Präzisierung zu 2d (Fassung 16.6), Auswertungsebene:** Die Bedingung wird im Selektionslauf **für den Gewinner auf dessen eigenen simulierten Positionen** ausgewertet; der Deckel ist je Bot eine Konstante über alle Zellen. Das Journal des Papierpfads ist dafür keine Quell…“ Gegenprobe Register = 2 (Z.2341, Z.8890).

### 5 — 41.1 A4, A5
- A4 (K41 Z.86, 89): „**A4 — Regel: jede Mutationsprobe beisst allein; H6** · Art: Registertext (Ergänzung zu 12/40.7)“; Text: „> **Regel (Ergänzung zu 12/40.7):** Jede Mutationsprobe beisst **allein**: Ihre Gegenprobe (nur ihre eigene Mutation weggelassen, alles andere im Grundzustand) scheitert. Eine Probe, die das nur im Verbund mit einer anderen leistet, wird vor dem Tag **eigenständig** gemacht — …“
- A5 (K41 Z.106, 109): „**A5 — Störproben in beide Richtungen** · Art: Registertext (Ergänzung zu 12)“; Text: „> **Registertext, Ergänzung zu 12 (Gegenproben) — Störproben:** Eine Störprobe nach „geht es ein?" wird in **beide** Richtungen geführt: klein genug, dass nichts passieren darf, und gross genug, dass etwas passieren muss. Eine Störprobe nur in eine Richtung belegt nichts.“

### 6 — 29.3, 2a, „Ein-Pfad-Regel“
- 29.3 (K29 Z.45): „> **Zu 4a / 26:** Der Kapitalpfad eines Bots beginnt am 1. Januar seiner ersten Selektionsfalte mit dem registrierten Startkapital und ohne offene Position. Kein Einstieg liegt vor diesem Datum. Die Grösse der Wirkung ist für diese Regel ohne Belang.“ Quelle Z.47–48: „4a (Falten sind ganze Kalenderjahre) und der Grund von 26 (kein Trade ausserhalb aller Falten im Kapitalpfad). Kein Ergebnis.“ In Abschnitt 29: 0 Treffer für „ein Kapitalpfad / einen Kapitalpfad / einzig“.
- 2a = 15.4 (a) (K15 Z.120–124): „> **(a)** Selektionsfalten sind Kalenderjahre (bzw. Doppeljahre nach der bestehenden Regel). **Jeder Handelstag gehört zu der Falte, in die sein Datum fällt.** Die Falten-Rendite ist die Summe der täglichen Netto-Mark-to-Market-Renditen dieser Tage. Positionen, die eine Faltengrenze überschreiten, werden **nicht zugeordnet, geschlossen oder ausgeschlossen**.“ Marke K15 Z.141: „⭐ **2a (15.4 (a)) BERICHTIGT durch R54 (49.2)**“. Das Wort „Pfad“ kommt in 15.4 nur als „Signalpfad“ vor (K15 Z.182).
- „Ein-Pfad-Regel“: Register gesamt 2 Zeilen. `REGISTER_KOPIE_ABSCHNITT_16.md`: 1 (16.6), `REGISTER_KOPIE_ABSCHNITT_53.md`: 1 (R68 (d), als Zitat von 16.6). Alle anderen Abschnittsdateien 0.

### 7 — R45 (K48 Z.105, 769 Zeichen)
- Anfang: „> R45 — Registertext zu Sperrlistenpunkt 10 (ausgeführte Positionen). shared/zuteilung.py::simuliere_portfolio gibt zusätzlich die ausgeführten Positionen (Symbol, Einstiegs- und Ausstiegszeit, Grösse, Preise) heraus — additiv, als weiteres Feld oder weiteren Rückgabewert; Zuteilungsreihenfolge, SEED und Rechnung unverändert; …“
- Tatsächlicher Wortlaut zum Rechenweg: „Eine Rekonstruktion der Positionen aus den Ereignissen der equity_curve ist ein zweiter Rechenweg und wird nicht gegangen. F-14.“
- „je Zelle einmal“: in R45 0× „einmal“, 0× „je Zelle“ („Zelle“ 1× in „Zellen-Erzeuger endet mit 2“, „Zuteilung“ 1× in „Zuteilungsreihenfolge“). In allen 54 Kopien 0 Treffer für `Zuteilung läuft|läuft je Zelle|je Zelle einmal|einmal je Zelle|je Zelle genau einmal`.

### 8 — 35.1 (K35 Z.29, 714 Zeichen)
„> **Ergänzung zu 33.2 (Bestätigungsperiode):** Die Bestätigungsperiode eines Bots ist die Datumsspanne von „Bestätigung ab" (21.4) bis zum Go-Live-Schnitt (5.2), Ende ausschliesslich. Sie ist keine Selektionsfalte und keine Falte im Sinn von 4a; ihre Länge ist von der Faltenlänge des Bots un…“; weiter in derselben Zeile: „Ihr **Bezeichner** in Plan, Abbild, `zellen.csv` und Berichten ist die Spanne selbst in der Form `JJJJ-MM-TT/JJJJ-MM-TT` (Beginn/Ende, Ende ausschliesslich); für den registrierten Bestand bei allen neun Bots `2026-01-01/2026-09-01`.“ Marke K35 Z.97: „35.1 PRÄZISIERT durch R37 (48.5)“.

### 9 — R63 (d), R48 (d)
- R63 (d) (K52 Z.9, ab Zeichen 1198): „(d) Der Zellen-Erzeuger bezieht weder Positionen noch Exposure aus bot_lauf.py oder dessen Ausgabe; die Positionen kommen aus simuliere_portfolio (R45), die Spalte exposure aus derselben Rechnung wie die MtM-Reihe (R60 (c)).“
- R48 (d) (K48 Z.130, 669 Zeichen): „> (d) Exposure: DD_Toleranz(e) und DD_Benchmark(f, e) werden mit der mittleren Exposure des Parametersatzes in der jeweiligen Falte ausgewertet (4.2). Die mittlere Exposure der Kapitalregel (7.1, 7 (c), 16.4 (b), 15.6 (c)) ist die des Gewinners über seine Selektionsfalten (7 (c): „über dieselben…“; später in derselben Zeile: „…Mittel über die Handelstage des Zeitraums (Krypto Kalendertage, 15.4 Anmerkung 1) des Anteils des Kapitals in offenen Positionen am Tagesschluss, bewertet wie die MtM-Reihe (1a). [Voraussetzung, zu messen: Bildung von mittlere_exposure im Vertrag/auswertung.py und in mtm_kern.py; …“

### 10 — R36 (K48 Z.33, 1038 Zeichen; Quelle Z.34)
- Anfang: „> R36 — Präzisierung zu 24.2 und 45.5 (zwei Drawdown-Spalten; Konsistenzprüfung; Ausschnitt). zellen.csv trägt je (Zelle, Falte) kapital_drawdown_mtm_pct — den Kapital-Drawdown der Nebenbedingung auf der täglichen MtM-Reihe (1a) auf den Tagen des Benchmarks (3b (c)) — und kapital_drawdown_…“
- Nachrechnung: „Die Spalte kapital_drawdown_pct wird durch die zwei benannten ersetzt, nicht umgedeutet. auswertung.py rechnet kapital_drawdown_mtm_pct aus tagesreihen/<zelle>.csv nach und endet bei Abweichung mit 2.“
- Ausschnitt/Hochpunkt: „Der Drawdown je Falte ist der Ausschnitt eines durchgehenden Kapitalpfads (29.3, 2a): gemessen innerhalb der Falte, mit dem Kapitalstand am Faltenbeginn als erstem Hochpunkt, ohne Neustart des Kapitals.“
- „24b A2“: im Blocktext 0×; in der Quelle des Grundes (Z.34): „> Quelle des Grundes: 24.2, 24 (Festlegung 1 präzisiert), 24.6 (Bauart der Faltenmessung), 29.3, 2a, 24b A2 (ein Wert, der nachgerechnet werden kann, tut nicht, als wäre er gemessen), 12. Kein Ergebnis.“
- `kapital_drawdown_mtm_pct` in R36: ja, 3× im Blocktext, 0× in der Quelle.

### 11 — R34 (K48 Z.19, 843 Zeichen; Quelle Z.20)
- Anfang: „> R34 — Ergänzung zu 22.2 und 45.5 (Zellenbericht). Der Zellen-Erzeuger schreibt je Bot eine Datei zellenbericht.csv mit genau einer Zeile je Zelle und den Feldern: die drei Werte aus 22.2 (Ertragsanteil der besten Selektionsfalte, des besten Symbols, der fünf besten Trades), haltedauer_median_handelstage (15.3 (b), R41) und bestaetigung_ab_effektiv (R37).“
- Bericht: „auswertung.py liest die Zeile des Plateau-Gewinners und berichtet sie (22.2: Bericht, kein Tor; N unverändert); es rechnet die Werte nicht. Die Feldliste von zellenbericht.csv ist Registertext (R39). F-3, F-4, F-6.“
- Wiedergabe von 12 (Quelle Z.20): „> Quelle des Grundes: 22.2 (Werte des Laufs für den Gewinner), 12 (auswertung.py hat keinen Schalter und liest Rohergebnisse), Punkt 14 (Reihenfolge Selektion → Bestätigung → Bericht), 2b. Kein Ergebnis.“ Gegenprobe Register `grep -c -F 'auswertung.py hat keinen Schalter'` = 1 (diese Zeile; in Abschnitt 8 und 12 steht der Name in Backticks: K12 Z.29 „dass `auswertung.py` keinen Schalter hat“, K08 Z.30–31 „`auswertung.py` hat keinen Schalter, der eine Zeile unterdrückt.“).

### 12 — R33, R67
- R33 (K48 Z.9): „…die Zeilenzahl je Bot ist Zellen × (Selektionsfalten + 1). Eine (Zelle, Falte) ohne Trades trägt die Nullzeile: Trade-Zahl 0, Sharpe 0 nach 1c, Drawdown 0, nie nichts.“ Eine fehlende Zeile ist ein Befund über den Erzeuger, kein Ausgang. Es gibt keine Trade-Liste je Zelle als Rohergebnis; …“
- R67 (K53 Z.16, 753 Zeichen): „> R67 — Registertext, Ersteintrag, Ergänzung zu R39 (48.7) (Eindeutigkeit und Vollständigkeit der Reihen). In jeder Tagesreihe (tagesreihen/<zelle>.csv) und in jeder Benchmark-Tagesreihe (benchmark_tagesreihen/<bot>.csv) ist datum eindeutig, kein Feld leer und jeder Zahlenwert endlich. Ein flacher Tag trägt 0, nie nichts (1a). Ein Verstoss ist ein Befund über den Erzeuger, kein Ausgang (Bauart R33): Der Zellen-Erzeuger prüft jede dieser Dateien im Lauf, nachdem er sie geschrieben hat, und endet sonst mit 2. Die Abnahme nach R46 prüft die Wache mit Gegenprobe, je für ein doppeltes Datu…“ In R67: „nie leer“ 0×, „leer“ 2×, „Wache“ 2×.

### 13 — R39, 50.2
- R39 (K48 Z.57, 955 Zeichen), Aufzählung: „Ausgaben des Zellen-Erzeugers je Bot: zellen.csv (R33, R36), tagesreihen/<zelle>.csv, benchmark_tagesreihen/<bot>.csv, zellenbericht.csv (R34), symbole_je_falte.csv (R38), herkunft.json mit teile (37.4) und dem gerechneten Datenstand-Hash (46.7 (b)), Lese-Audit (5e).“ → sieben Ausgaben: `zellen.csv`, `tagesreihen/<zelle>.csv`, `benchmark_tagesreihen/<bot>.csv`, `zellenbericht.csv`, `symbole_je_falte.csv`, `herkunft.json`, Lese-Audit (ohne Dateinamen).
- Feldliste: „Die Feldliste jeder dieser Dateien ist Registertext (Bauart 33.3, 41.1 A12) und wird im Registerauftrag E-2 aus dem Docstring von auswertung.py gemessen eingetragen, nicht abgeschrieben. F-8, A68.“
- Marken an R39: „ERGÄNZT durch R67 (53.2)“ (K48 Z.60), „ERGÄNZT durch R69 (53.4): R39 ist bestätigt“ (K48 Z.63).
- 50.2 (K50 Z.31, 33): Überschrift „### 50.2 R39 (48.7) — Feldliste der Ausgaben, gemessen aus dem Docstring von `auswertung.py`“; erster Satz: „R39 verlangt, die Feldliste jeder Ausgabe des Zellen-Erzeugers als Registertext „aus dem Docstring von auswertung.py gemessen“ einzutragen, nicht abgeschrieben. Gemessen am Commit `0f56aeb`, `research/vorregistrierung/auswertung.py` Z. 36–67, zeichengleich:“

### 14 — `zellenbericht.csv`: Orte (Register gesamt 8 Zeilen mit „zellenbericht“; Kopien 48: 3 Zeilen, 50: 2, 53: 3)
1. R34 (48.2), Reg Z.10801 — Datei, „genau eine Zeile je Zelle“, Felder: drei Werte aus 22.2, `haltedauer_median_handelstage`, `bestaetigung_ab_effektiv`; „Die Feldliste von zellenbericht.csv ist Registertext (R39).“
2. R35 (48.3), Reg Z.10808 — „…mit L nach 15.3 (b) aus haltedauer_median_handelstage in zellenbericht.csv (R34).“
3. R39 (48.7), Reg Z.10839 — als Ausgabe aufgezählt; Feldliste = Registertext, gemessen aus dem Docstring.
4. 50.2, K50 Z.70, Reg Z.11073 — „Für `zellenbericht.csv` (R34), `symbole_je_falte.csv` (R38) und das Lese-Audit führt der Docstring heute keine Feldliste; sie kommt mit dem Zellen-Erzeuger (R46) und wird dann hier nachgetragen.“
5. 50.7 Nr. 7, K50 Z.184, Reg Z.11187 — „| 7 | R39: Feldlisten für `zellenbericht.csv`, `symbole_je_falte.csv`, Lese-Audit | mit dem Zellen-Erzeuger |“
6. R69 (b) (53.4), Reg Z.11405 — planmässige Öffnung, „R34 (zellenbericht.csv)“.
7. R69 Quelle, Reg Z.11406 — „auswertung.py kennt weder zellenbericht noch kapital_drawdown_mtm_pct noch bestaetigung_ab_effektiv“.
8. 53.9 Tabelle, K53 Z.73, Reg Z.11448 — „`zellenbericht` 0 Treffer in `auswertung.py`; `kapital_drawdown_mtm_pct` und `bestaetigung_ab_effektiv` 0 Treffer in allen `*.py` des Repos (ohn…“

### 15 — R54 (K49 Z.22)
„> R54 — Berichtigung zu Registertext 2a (15.4) und zu R48 (g) (Aggregation von Tagesrenditen). „Die Falten-Rendite ist die Summe der täglichen Netto-Mark-to-Market-Renditen dieser Tage“ lies „Die Falten-Rendite ist die verkettete Rendite dieser Tage, ∏(1 + r_t) − 1 über die täglichen Netto-Mark-to-Market-Renditen“.“; weiter: „…für die konstante Exposure — werden überall verkettet; Drawdowns stehen auf dem verketteten Kapitalpfad (24.2). In R48 (g) lies „die Summe der täglichen Renditen (2a)“ als „die verkettete Rendite (2a)“.“

### 16 — R68 (K53 Z.23, 1359 Zeichen; Quelle Z.24)
- (a): „(a) Die Zeile der Bestätigungsperiode (R33) trägt für jede Zelle die Bestätigungsstatistik, die R37 (i) für den Gewinner beschreibt. Alle Grössen dieser Zeile stehen auf den Tagen ab bestaetigung_ab_effektiv der Zelle bis zum Ende der Spanne (35.1). Die Spanne bleibt, was 35.1 sagt; ihre Tage vor di…“
- (b): „(b) R64 (a) gilt für die mittlere Exposure dieser Zeile: Mittel über die Benchmark-Tage des Bots innerhalb der Tage nach (a). Die Grösse ist Bericht; auswertung.py liest sie für kein Urteil.“
- (c): „(c) Eine Position, die nach der Attribution je Position (16.6, R37) in der Bestätigungsstatistik nicht gezählt wird, geht in keine Grösse der Zeile ein, auch nicht in ihre Exposure.“
- (d): „(d) Im Fall nach (c) ist die Zeile nicht der blosse Ausschnitt der Tagesreihe (16.6: „ausdrückliche und seltene Ausnahme von der Ein-Pfad-Regel“). Wie die Gleichheitsproben nach R60 (c) und R64 (d) und die Nachrechnung nach R36 diesen Fall behandeln, ist offen und geht vor der Öffnung nach R69 (b) als Frage an den Verfahrensprüfer. Tatsachennotiz: Die Fassung von 2d in 15.4 (d) („Tage im Embargo gehören zu keiner Periode“) ist durch 16.6 vollständig ersetzt und trä…“
- Gegenprobe `grep -c -F 'Gleichheitsproben nach R60 (c) und R64 (d)'`: Register 2, K53 2 (Z.23 und Z.86 = 53.10 Nr. 2: „| 2 | Deckelfall (R68 (d)): Behandlung in den Gleichheitsproben nach R60 (c) und R64 (d) und in der Nachrechnung nach R36 | Frage an Fable vor der Öffnung nach R69 (b) |“).

### 17 — R60 (c), R64 (d)
- R60 (c) (K51 Z.37, ab Zeichen 1106): „(c) Der Zellen-Erzeuger schreibt beide Träger aus einer Rechnung: mittlere_exposure in zellen.csv ist je (Zelle, Falte) das Mittel der Spalte exposure der Tagesreihe dieser Zelle über die Tage der Falte. Die Abnahme nach R46 prüft diese Gleichheit, mit Gegenprobe. auswertung.py wird dafür nicht geöffnet.“
- R64 (d) (K52 Z.16, ab Zeichen 1209), erster Satz: „(d) „Über die Tage der Falte“ in R60 (c) lies: über die Tage nach (a), die in die Falte fallen (halboffen wie im Faltenplan; 2a).“ Zweiter Satz: „Der Wert des Gewinners in beta_bereinigung ist dann das mit der Zahl dieser Tage gewichtete Mittel seiner Werte je Selektionsfalte in zellen.csv; die Abnahme nach R46 prüft auch diese Gleichheit, mit Gegenprobe.“ Danach beginnt (e).

### 18 — R66 (c), (d); `bestaetigung_ab_effektiv`
- R66 (c) (K53 Z.9, ab Zeichen 1302): „(c) Der Falten-Sharpe nach 1c wird über alle Tage der Tagesreihe gerechnet, die in die Falte fallen (2a; halboffen wie im Faltenplan), nicht nur über die Tage, an denen der Benchmark definiert ist. Ein Tag ohne Benchmark-Tag geht mit Rendite 0 ein. Dasselbe gilt für den Sharpe in der Zeile der Bestä…“
- R66 (d) (ab Zeichen 1968): „(d) Auf den Tagen des Benchmarks stehen: der Drawdown der Nebenbedingung (24.2, R36), die mittlere Exposure (R64), Beta-Bereinigung und Calmar-Vergleich (7 (c)) und das Zufalls-Timing (R48 (g): dieselben Tage wie 7 (c)). Auf dem Kapitalpfad nach (a) steht der Falten-Sharpe und mit ihm die Selektions…“
- `bestaetigung_ab_effektiv`, Register 7 Zeilen: Z.10801 (R34, Feld von zellenbericht.csv), Z.10822 (R37 (i): „Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle (bestaetigung_ab_effektiv, R34); auswertung.py nimmt den Wert der Gewinnerzelle (41.3 C3).“), Z.11373 (52.5), Z.11398 (R68 (a)), Z.11405 (R69 (b)), Z.11406 (R69 Quelle), Z.11448 (53.9 Tabelle). Kopien: 48: 2, 52: 1, 53: 4.

### 19 — R72 (c), 24.6
- R72 (c) (K53 Z.51, ab Zeichen 879): „(c) Der Zellen-Erzeuger bewertet eine offene Position an einem Tag ohne Kurs ihres Symbols zum letzten Kurs; die Position trägt an diesem Tag Rendite 0 und bleibt in der Exposure. Er berichtet je Bot die Zahl solcher Positionstage (Bauart 24.6). Bot und Benchmark werden am Lückentag damit gleich bewertet.“
- R72 Quelle (K53 Z.52): „…17.5 (registrierte Umgebung, Abbruch bei Abweichung); 24.6 (Bauart: fortgeschriebene Kurstage werden gezählt); R48 (d) (bewertet wie die MtM-Reihe); …“
- 24.6 selbst (K24 Z.224 „### 24.6 Tatsachennotiz zu 24.3 und 24.4 — die gemessene Wirkung (TB-73, 20.09.2026)“), einzige Stelle mit „fortgeschrieb“/„gezählt“ (Z.249, Tabellenzeile „Grundlage“): „…1d-Kurse decken jeden Tagesschluss mit offener Position (0 fortgeschriebene Kurstage bei 149 000 Positionstagen) |“
- `grep -c -F 'gezählt und berichtet'` im Register: 0.

### 20 — R69 (b) (K53 Z.30, ab Zeichen 520)
„(b) Vor dem signierten Tag liest auswertung.py die Datei unter dem Namen des Bots. Das ist eine beauftragte Änderung nach 37.3 (Auftrag, Freigabe, alter und neuer Hash) mit neuem Abbild und einem Nachweis mit Gegenprobe (Bauart R55, R64). Sie gehört zur planmässigen Öffnung von auswertung.py, die R36 (zwei Drawdown-Spalten, Nachrechnung), R37 (bestaetigung_ab_effektiv), R34 (zellenbericht.csv) und R55 (Umbenennung) verlangen.“

### 21 — R35, Abschnitt 8
- R35 Blocktext (K48 Z.26, 567 Zeichen): „> R35 — Ergänzung zu 15.3 (Bootstrap) und Tatsachennotiz. 15.3 (a)/(b) regeln die Bauart eines Bootstrap-Intervalls; sie verlangen keines. Abschnitt 8 (Sperrlistenpunkt 13) führt keine Bootstrap-Zeile; der Lauf rechnet kein Intervall. Angewandt wird 15.3 auf die Messbitte R7 Nr. 6 (Block-Bootstrap-Band je Gewinnerzelle, nach dem Tag), …“ — „abschliessend“ im Blocktext: 0×.
- R35 Quelle (K48 Z.27): „> Quelle des Grundes: 8 (abschliessende Berichtsliste), 15.3 im Wortlaut („jedes … wird … gerechnet“), R6/R7. Kein Ergebnis.“
- Abschnitt 8 (K08, Reg Z.870–924), Gliederung: „## 8. Die Beurteilung — und die Regel, dass alles berichtet wird“ (Z.3); „### 8.1 Der Zufalls-Timing-Test“ (Z.33). Keine weiteren Überschriften.
- Einleitender Satz (K08 Z.5, Reg Z.872): „Berichtet wird je Bot, unabhängig davon, ob er bleibt oder geht:“; danach Tabelle „| Kennzahl | Quelle |“ mit 13 Zeilen (Z.9–21; letzte: „| Bestätigungsperiode: Sharpe, Rendite, Drawdown, Trades | zuletzt |“).
- Marken in 8: „8, Tabelle PRÄZISIERT durch R36 (48.4)“ (Z.23), „8, Tabelle ERGÄNZT durch R55 (49.3)“ (Z.26). Danach Z.29–31: „**Die Regel: alle werden berichtet, auch die unangenehmen.** Sie steht auf der Sperrliste. `auswertung.py` hat keinen Schalter, der eine Zeile unterdrückt.“
- `grep -c zellenbericht` in K08: 0. `grep -c -i abschliessend` in K08: 0.

### 22 — `research/mtm_drawdown/mtm_kern.py` (339 Zeilen; letzter Commit `5e9ef2b`, 2026-09-20)
- Funktionen: `ereignisreihenfolge` (Z.79), `ereigniskurve` (Z.123), `tagesraster` (Z.135), `kurse_auf_raster` (Z.151), `mtm_pfad` (Z.176), `drawdown_falte` (Z.263), `messe_falten` (Z.275), `median_selektion` (Z.331).
- Tagesstand (in `mtm_pfad`):
  - Z.209–210: `kapital_after = ereignisse["capital_after"].to_numpy(dtype=float)` / `buch = np.where(k > 0, kapital_after[np.maximum(k - 1, 0)], float(startkapital))`
  - Z.244: `unreal[a:b + 1] += allokation[i] * (schluss / einstand[i] - faktor_kosten)`
  - Z.251: `"mtm": buch + unreal,`
- Je Position geführt und summiert: ja für den unrealisierten Wert als Stand (Schleife Z.233 `for i in range(len(ereignisse)):`, Summe Z.244). Eine Wertänderung je Position und Tag (Tagesdifferenz) wird nicht gebildet. Das realisierte Ergebnis geht nicht je Position ein, sondern über `capital_after` des letzten Ausstiegs (Z.208–210).
- `gebunden`: Z.223 `gebunden = np.zeros(n)`, Z.246 `gebunden[a:b + 1] += allokation[i]`; Docstring Z.188: „gebunden    Summe ihrer Allokationen (Einstand)“.
- Tagesrendite: wird in der Datei nicht gebildet. `grep -n -i -E 'rendite|pct_change|\.diff\(|shift\(|exposure|cumprod'` trifft nur Z.204 (`np.diff(exit_np)`, Sortierprüfung). `mtm_pfad` gibt einen DataFrame mit den Spalten `buch`, `mtm`, `n_offen`, `gebunden`, `unrealisiert`, `fortgeschrieben` zurück (Z.249–256); eine Division durch einen Kapitalstand steht in `mtm_pfad` nicht. Docstring Z.178: „Tagesreihe des Kapitals in drei Lesarten“.
- 53.9 dazu (K53 Z.76): „Einziger vorhandener Kern für eine tägliche MtM-Reihe ist `research/mtm_drawdown/mtm_kern.py`; Z. 166–168 schreibt den letzten Kurs fort (`eigene.ffill()`), Z. 244–247 lässt die Position in `n_offen` und `gebunden` und zählt den Positionstag in `for…“

### 23 — `research/vorregistrierung/auswertung.py` (860 Zeilen; letzter Commit `852f253`, 2026-09-26)
- Docstring Z.2–89; Feldliste „DIE ROHERGEBNISSE - DER VERTRAG“ ab Z.36 (Z.38 `zellen.csv`, Z.45 `tagesreihen/<zelle_id>.csv` mit Z.46 `datum, netto_rendite, exposure`, Z.51 `herkunft.json`, Z.64 `benchmark_tagesreihen/<markt>.csv`).
- Treffer (Zeilen / Vorkommen): `tagesreihe` 6/6; `exposure` 14/18; `mittlere_exposure` 5/6 (Z.41, 134, 405, 537, 626); `kapital_drawdown_mtm_pct` 0; `zellenbericht` 0; `zellen.csv` 3/3; `bestaetigung_ab_effektiv` 0. Zusätzlich: `kapital_drawdown_pct` 8/9, `netto_rendite` 13/14.
- Leser: `lies_zellen` (Z.320), `lies_tagesreihe` (Z.361), `lies_benchmark` (Z.378), `beta_bereinigung` (Z.490).
- Zellen-Erzeuger: `git ls-files research/vorregistrierung` = 32 Dateien, darunter die Python-Dateien `auswertung.py`, `beispieldaten.py`, `benchmark.py`, `faltenplan.py`, `herkunft.py`, `kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`, `registerbericht.py`, `registerdaten.py`, `sperrliste_abbild.py`, `test_ersatzwerte.py`, `test_vorregistrierung.py`; keine Datei mit „zelle“ oder „erzeug“ im Namen. Repo-weit `*.py` mit „zelle|erzeug“ im Namen: `dashboard/erzeuge_icons.py`, `docs/belege/TB-92/d_zellenzahl.py`.
- Repo-weit `*.py` mit `zellenbericht` / `bestaetigung_ab_effektiv` / `kapital_drawdown_mtm_pct`: nur `docs/belege/TB-126/0g_vorpruefung.py` (2 Zeilen). `*.py` mit `netto_rendite`: `research/vorregistrierung/{auswertung,beispieldaten,test_ersatzwerte,test_vorregistrierung}.py` und sechs Dateien unter `research/turn_of_month/`. `*.py` mit `mtm_pfad`: `research/mtm_drawdown/{mtm_kern,grundlage,messung,test_mtm_kern}.py`, `docs/belege/TB-132/vormessung/p3_probe.py`.

### 24 — Zuordnung
Überschriften der Kopien: „### 48.2 R34 — Ergänzung zu 22.2 und 45.5 (Zellenbericht)“; „### 48.4 R36 — Präzisierung zu 24.2 und 45.5 …“; „### 48.5 R37 — Präzisierung zu 16.6, 35.1, 16.4 (c)/(d), 5.1 Nr. 7 …“; „### 48.7 R39 — Ergänzung zu 46.3 (R12) …“; „### 51.5 R60 — Bestätigung und Ergänzung zu R48 (d) (48.16) …“; „### 52.2 R64 — Präzisierung zu R48 (d) (48.16) und zu R60 (b) und (c) (51.5) …“; „### 53.3 R68 — Präzisierung zu R33 (48.1), zu R37 (48.5) und zu R64 (52.2) …“; „### 53.4 R69 — Auflösung des Widerspruchs zwischen R39 (48.7) und auswertung.py …“. Der Index führt dieselben Paare (z. B. Index Z.270 „16.6 | Z. 2347 | PRÄZISIERT | R37 (48.5)“, Z.275 „R36 (48.4)“, Z.274 „R34 (48.2)“, Z.298 „R39 (48.7)“, Z.318 „R60 (51.5)“, Z.350 „R64 (52.2)“, Z.380 „R68 (53.3)“, Z.385 „R69 (53.4)“).

## Nicht gemessen / Einschränkungen
- Ob die Kopien zeichengleich zum Register sind, ist nicht geprüft (kein `registerkopie.py`). Gegengeprüft sind die Zitate und die Zeilennummern per `grep -n -F` im Register.
- Kopfzeile der Kopien und Index nennen Commit `ee43f5f`; HEAD ist `d781f1b`. Ob das Register zwischen beiden geändert wurde, ist nicht gemessen (kein `git diff`).
- Aus Fables Liste „nach Wiedergabe zitiert“ sind 34, 37.3 und 37.5 (2) nicht Teil des Auftrags und nicht gelesen. Abschnitt 12 nur die eine Zeile mit „Schalter“ (K12 Z.29).
- Zu Nr. 22: Nur `mtm_kern.py` gelesen (Z.1–40 und Z.172–260 sowie die grep-Zeilen); `messe_falten` (Z.275–328) nur über grep, nicht im Wortlaut. Ob ein anderer Kern im Repo eine Tagesrendite bildet, ist über die Dateiliste mit `netto_rendite` hinaus nicht gemessen.
- Abweichung von der Ausgaberegel: Weil ältere Abschnitte hart bei unter 80 Zeichen umbrochen sind, habe ich beim Zeilenlisten (Schnitt bei 75–110 Zeichen je Zeile) grössere Stücke im Wortlaut ausgegeben als nötig: 16.6 (K16 Z.483–534) nahezu ganz, Abschnitt 8 Z.3–40, 24.6 Z.224–263, 41.1 Z.86–125, 41.3 Z.308–360 (Kopfzeilen), 50.2 Z.45–71. Nur Lesen, keine Datei berührt.

## Bestätigung
Kein `git status`, kein `git diff`, nichts im Repo angelegt, geändert oder gelöscht, kein Skript des Repos ausgeführt. git nur als `git --no-optional-locks ls-files | log | rev-parse | grep`.

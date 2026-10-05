# CLOUD_TB-134 — Offene Voraussetzungen im Register

- Commit: `d781f1b` (`git rev-parse --short HEAD`; gleich `origin/main`)
- Register: `docs/VORREGISTRIERUNG_neuselektion.md`, 11471 Zeilen, sha256 `9a2cefb77a394a0a1c87c63cb9437d5693f054e4516333f656fae97668ef71ff`
- Gelesene Dateien: nur `docs/VORREGISTRIERUNG_neuselektion.md` (dazu `CLAUDE.md`, vom System geladen). Nichts aus `ergebnisse/`, keine `*.db`, keine Kurs- oder Trade-Dateien. Kein Skript und kein Test des Repos ausgefuehrt; im Repo nichts angelegt oder geaendert.
- Verfahren: Wortlaute per Python-Skript aus der Datei geschnitten (Klammer = von "[Voraussetzung" bis zur naechsten "]"; die Klammern in R33–R73 sind nicht verschachtelt, je Zeile gleich viele "[" wie "]"). Unterpunkt = letzte Unterpunktmarke "(x)" des Blocks vor der Klammer; "—" = Klammer steht vor jeder Unterpunktmarke bzw. Block ohne Unterpunkte.

## 1. Klammern "[Voraussetzung …]" in R33 bis R73

| Nr. | Block | Ueberschrift | Unterpunkt | Registerzeile | Wortlaut der Klammer |
|---|---|---|---|---|---|
| K1 | R41 | 48.9 | — | 10859 | [Voraussetzung, zu messen: ob TB-24 die Haltedauer in 15.4 (t3_supertrend 11,21 Tage) als Kerzenzahl oder als Zeitstempeldifferenz gebildet hat; bei Abweichung trägt die Neurechnung nach 41.3 C2 diese Zählregel, und 15.4 erhält eine Tatsachennotiz.] |
| K2 | R56 | 51.1 | (e) | 11201 | [Voraussetzung, zu messen: dass sein Eröffnungstext mit Commit im Repo liegt.] |
| K3 | R57 | 51.2 | — | 11208 | [Voraussetzung, zu messen: dass BB_PERIOD + L − 1 in backtest_breakout.py ein nullbasierter Index ist und dass faltenplan.py einen Vorlauf v als „v Balken liegen davor“ anwendet; weicht eines ab, gilt diese Definition, und die Formel folgt ihr.] |
| K4 | R60 | 51.5 | (a) | 11229 | [Voraussetzung, zu messen: dass research/exposure_messung/ nicht zum Laufbereich gehört.] |
| K5 | R60 | 51.5 | (b) | 11229 | [Voraussetzung, zu messen: über welche Tage beta_bereinigung mittelt; R48 (d) und 7 (c) verlangen die Selektionsfalten des Gewinners; eine Abweichung ist ein Register-Code-Widerspruch nach 25c (1) und wird gemeldet.] |
| K6 | R61 | 51.6 | (c) | 11245 | [Voraussetzung, zu messen: der Wortlaut von Sperrlistenpunkt 14; hier nach REGISTER_INDEX.] |
| K7 | R63 | 52.1 | (c) | 11308 | [Voraussetzung, zu messen, durch Lesen des Codes und nicht durch Wortsuche: dass bot_lauf.py keinen Anteil des Kapitals in offenen Positionen und kein Mittel daraus rechnet.] |
| K8 | R64 | 52.2 | (e) | 11315 | [Voraussetzung, zu messen: dass beta_bereinigung ausser dem Schnitt auf die gemeinsamen Tage keinen Tag weglässt; dass an einem Tag ohne Benchmark-Tag keine Zelle eine offene Position führen kann, ausser am Tag aus der Tatsachennotiz zu 23.3.] |
| K9 | R66 | 53.1 | (b) | 11384 | [Voraussetzung, zu messen: welchen Kalender des Pakets der Code des Laufs benutzt (TB-47, Feld kalender); die Messung zur Anfrage 02.10.c verglich mit dem NYSE-Kalender.] |
| K10 | R66 | 53.1 | (c) | 11384 | [Voraussetzung, zu messen: dass der Aufruf mit 252 Perioden je Jahr, bei Krypto 365, die Formel aus 15.3 trifft; den Bezeichner trägt die Tatsachennotiz nach R50 (38.2).] |
| K11 | R71 | 53.6 | — | 11419 | [Voraussetzung, vor dem Eintrag zu messen: die Wiederholung der Probe in der Lock-Umgebung auf dem Betriebsrechner; weicht sie ab, wird gemeldet, nicht eingetragen.] |
| K12 | R72 | 53.7 | (e) | 11426 | [Voraussetzung, vor dem Eintrag zu messen: die Wiederholung der Probe in der Lock-Umgebung auf dem Betriebsrechner; dass kein vorhandener Kern, den der Zellen-Erzeuger für die MtM-Reihe übernimmt, am Lückentag anders bewertet als (c).] |

## 2. Eintrag in den Tabellen "Voraussetzungen und Befunde" (50.1, 51.8, 52.4, 53.9)

Durchsucht: die Tabellenzeilen in den Abschnitten 50 bis 53 (Registerzeilen 11006–11471), erste Spalte. Wiedergegeben ist die letzte Spalte ("Stand"), hoechstens 300 Zeichen, gekuerzt mit "[…]".

| Nr. | Block, Unterpunkt | Suchwort | Tabelle | Registerzeile | erste Spalte | letzte Spalte (Stand), Wortlaut |
|---|---|---|---|---|---|---|
| K1 | R41 — | `R41 (48.9)` | 50.1 | 11019 | R41 (48.9) | weicht ab ⇒ Abweichungsfall nach R41, von Fable bestätigt (30a, Teil 0); Marke an 15.4; Neurechnung nach 41.3 C2 offen (50.7) |
| K2 | R56 (e) | `R56 (51.1) (e)` | 51.8 | 11269 | R56 (51.1) (b), (e) | erfüllt für beide Fassungen, vor diesem Eintrag. Im Chat kam nach Angabe des Betreibers Fassung 2 an (Auswahlkarte, 02.10.2026); das gehört in die Tatsachennotiz nach R56 (e) (51.10) |
| K3 | R57 — | `R57 (51.2)` | 51.8 | 11270 | R57 (51.2) | trifft. Der Index ist nullbasiert, und die Bedingung liest die Vorkerze; beides zusammen ergibt L + 19 (01a, „Unsicher“ 1) |
| K3 | R57 — | `R57 (51.2)` | 51.8 | 11271 | R57 (51.2) | trifft: „warm ab“ ist der Balken mit Index v, v Balken liegen davor |
| K4 | R60 (a) | `R60 (51.5) (a)` | 51.8 | 11272 | R60 (51.5) (a) | trifft für den Ordner **nicht**; trifft für die zwei Stellen, die die Grösse bilden ⇒ Lesart 51.9, an Fable |
| K5 | R60 (b) | `R60 (51.5) (b)` | 51.8 | 11273 | R60 (51.5) (b) | Falten und Zelle: trifft (R48 (d): „die des Gewinners über seine Selektionsfalten (7 (c): „über dieselben Tage“)“). Tage: gemittelt wird über die gemeinsamen Tage mit dem Benchmark; ob das alle „Handelstage des Zeitraums“ nach R48 (d) sind, ist **nicht gemessen** ⇒ offen, an Fable mit R60 (c) (51.9, […] |
| K6 | R61 (c) | `R61 (51.6) (c)` | 51.8 | 11275 | R61 (51.6) (c) | trifft: gemeint ist Sperrlistenpunkt 14 |
| K7 | R63 (c) | `R63 (52.1) (c)` | 52.4 | 11351 | R63 (52.1) (c) | trifft: kein Anteil je Tag, kein Mittel |
| K8 | R64 (e) | `R64 (52.2) (e)` | 52.4 | 11353 | R64 (52.2), erste | trifft. Fehlende Werte und doppelte Daten werden dort weder behandelt noch geprüft (52.5) |
| K8 | R64 (e) | `R64 (52.2) (e)` | 52.4 | 11354 | R64 (52.2), zweite | offen (52.5). Nach 02a, „Unsicher“ 2: Trifft die Voraussetzung nicht zu, bleibt die Regel, und der Satz zur Richtung der Wirkung gilt dann nicht streng |
| K9 | R66 (b) | `R66 (53.1) (b)` | 53.9 | 11444 | R66 (53.1) (b) | nicht entscheidbar: Der Code des Laufs benutzt heute keinen Kalender; welchen Namen der Zellen-Erzeuger nimmt, ist offen (53.10 Nr. 1). Die Wache nach R66 (b) prüft die Wahl im Lauf |
| K10 | R66 (c) | `R66 (53.1) (c)` | 53.9 | 11445 | R66 (53.1) (c) | trifft für die Funktion; einen Aufruf gibt es noch nicht (der Zellen-Erzeuger fehlt). Den Nenner der Standardabweichung nennt das Register nicht; der Code legt n − 1 fest (R50). Ein nicht endlicher Wert in der Reihe ergäbe still 0; R67 schliesst ihn aus |
| K11 | R71 — | `R71 (53.6)` | 53.9 | 11449 | R71 (53.6) | trifft (Rückgabewert 0; bei Abweichung wäre dieser Abschnitt nicht entstanden) |
| K12 | R72 (e) | `R72 (53.7) (e)` | 53.9 | 11450 | R72 (53.7), erste | trifft |
| K12 | R72 (e) | `R72 (53.7) (e)` | 53.9 | 11451 | R72 (53.7), zweite | trifft für diesen Kern. Nicht von selbst erfüllt: `tagesraster` (Z. 135–148) lässt einen Tag aus, an dem kein übergebenes Symbol einen Kurs hat (das Raster nach R66 (a) gibt der Erzeuger); `gebunden` steht zum Einstand. Welchen Kern der Zellen-Erzeuger übernimmt, legt kein Registertext fest |

Hinweise zur Zuordnung (Befund, keine Deutung):
- K2 (R56 (e)): die Tabellenzeile 11269 fuehrt "(b), (e)" zusammen.
- K3 (R57) und K12 (R72 (e)): die Klammer nennt zwei Messgegenstaende; die Tabelle fuehrt je einen in eigener Zeile (11270/11271 bzw. 11450/11451 "erste"/"zweite").
- K8 (R64 (e)) und K12 (R72 (e)): das Suchwort mit Unterpunkt "R64 (52.2) (e)" bzw. "R72 (53.7) (e)" steht in keiner Tabellenzeile; die Zeilen tragen "R64 (52.2), erste/zweite" bzw. "R72 (53.7), erste/zweite" und geben die Klammer im Wortlaut (Spalte "Voraussetzung (Fable)") wieder. Zugeordnet ueber Blocknummer und Wortlaut.
- Zeile 11354 (K8, zweite) traegt die Marke 11358: "52.4, Zeile „R64 (52.2), zweite“ ERGÄNZT durch R66 (53.1)".
- Die Tabellen "Was offen bleibt" (50.7, 51.10, 52.5, 53.10) sind keine Messtabellen und hier nicht als Eintrag gezaehlt.

## 3. Zusatz

### 3.1 Wortlaut 41.3, Punkt C2 (Registerzeilen 8870–8884)

```text
8870: **C2 (b) — Deckel für Bots ohne Zeitbremse aus gefundenen Trades** · Art:
8871: Registertext (Präzisierung zu 2d, Fassung 16.6) · Quelle: 24d Abschnitt 1 ·
8872: berichtigt 41.2 (B2)
8873: 
8874: > **Präzisierung zu 2d (Fassung 16.6), Deckel für Bots ohne Zeitbremse:** Das 95. Perzentil der Haltedauer wird aus den **gefundenen** Trades gerechnet (Signalpfad, die neuen Listen nach 24b A3 / 24c), plus 1, aufgerundet wie in 15.4 Anmerkung 4; Tatsachennotiz mit Hash der Liste, Snapshot-Hash und Commit. Der Deckel ist keine Leckschranke — das Leck schliesst die Attribution je Position —, und er ist deshalb ausdrücklich **nicht** als Maximum über alle Rasterzellen zu bemessen. Der Zusatz aus 24c *„Maximum der gefundenen Trades über den gesamten Datenhorizont, mit Aufschlag"* ist zurückgenommen.
8875: 
8876: *Seine Quelle des Grundes, zeichengleich:*
8877: 
8878: > *Quelle des Grundes:* 24c, Registertext „Reichweite des Grundsatzes aus 5.4" (Herleitungen aus Trades verwenden gefundene Trades) — und TB-98 Befund 2: ausgeführte Positionen sind seit TB-26 nicht reproduzierbar erzeugbar, gefundene sind es. Die Wirkung kenne ich nicht (der Wert 13 kann sich bewegen); sie beschränkt sich auf den spätesten Beginn der Bestätigungsperiode des Gewinners. Kein Ergebnis.
8879: 
8880: **Stand, gemessen:** nicht gerechnet — der Deckel von `t3_supertrend` steht in
8881: 15.4 und 16.6 weiter mit dem Wert aus **ausgeführten** Positionen
8882: (`research/tb24_haltedauern/daten/t3_supertrend_positionen.csv`, TB-24). Neu zu rechnen, wenn
8883: die neuen Listen gefundener Trades vorliegen (Plan-Punkt 5, 24d Abschnitt 4).
8884: Marken bei 15.4 und 16.6.
```

### 3.2 Registerzeilen mit "Attribution je Position"

Umfeld: je 100 Zeichen vor und nach dem Treffer, per Skript geschnitten. Auch ueber Zeilenumbrueche gesucht: kein getrennter Treffer.

| Nr. | Registerzeile | Ueberschrift | Umfeld (200 Zeichen) |
|---|---|---|---|
| A1 | 2311 | 16.6 | > Bestätigungsstatistik jedoch nicht gezählt** (Attribution je Position, |
| A2 | 2339 | 16.6 | > Leck schliesst die Attribution je Position (**41.3, C2**). (2) Die Bedingung |
| A3 | 8862 | 41.3 | ge noch Embargo (2c) und vor der Bestätigungsperiode keine Lücke, sondern Bedingung plus Deckel mit Attribution je Position (16.6). Eine Grösse, die eine Trainingsgrenze oder eine Lücke bemisst, gehört zu Verfahren A und wi |
| A4 | 8874 | 41.3 | ash der Liste, Snapshot-Hash und Commit. Der Deckel ist keine Leckschranke — das Leck schliesst die Attribution je Position —, und er ist deshalb ausdrücklich **nicht** als Maximum über alle Rasterzellen zu bemessen. Der Zu |
| A5 | 10822 | 48.5 | en ist; Deckel je Bot nach 16.6/41.3 C2; eine am Deckeltag noch offene solche Position zählt nicht (Attribution je Position). Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle (bestaetigung_ab_effektiv, R34); auswertun |
| A6 | 11398 | 53.3 | ). Die Grösse ist Bericht; auswertung.py liest sie für kein Urteil. (c) Eine Position, die nach der Attribution je Position (16.6, R37) in der Bestätigungsstatistik nicht gezählt wird, geht in keine Grösse der Zeile ein, au |
| A7 | 11399 | 53.3 |  jede Zelle“), R33 (genau eine Zeile je Zelle und Falte, Bestätigungsperiode eingeschlossen), 16.6 (Attribution je Position), R64 (a), R63 (d) (Bauart: Exposure aus derselben Rechnung wie die MtM-Reihe), die Messung des ste |

7 Treffer in 7 Registerzeilen (A1 und A2: kurze, umbrochene Zeilen; das Umfeld endet am Zeilenende).

## 4. Schluss

| Block | Klammern |
|---|---|
| R41 | 1 |
| R56 | 1 |
| R57 | 1 |
| R60 | 2 |
| R61 | 1 |
| R63 | 1 |
| R64 | 1 |
| R66 | 2 |
| R71 | 1 |
| R72 | 1 |
| **Summe** | **12** |

Bloecke R33–R73 ohne Klammer "[Voraussetzung": 31 von 41.

- Mit Eintrag in einer Messtabelle (50.1, 51.8, 52.4, 53.9): **12** (davon 2 nur ueber Blocknummer und Wortlaut zugeordnet, Suchwort mit Unterpunkt ohne Treffer: K8, K12).
- Ohne Eintrag: **0**.

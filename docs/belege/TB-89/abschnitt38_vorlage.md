
## 38. Weg (A) — die letzte Falte heisst die Spanne, Fundstellen als Datei und Bezeichner, der Vollzug von Punkt 4 nach 37.3 in Form (ii), neun Importe statt überwachter Kostenkopien, zwei Berichtigungen des Verfahrensprüfers an sich selbst und die Messungen aus TB-88 (Fable 22h, TB-89, 23.09.2026)

⭐ **Reines Eintragen von Registertext**, wie 34 bis 37. Sechs Einträge des
Verfahrensprüfers — eine Berichtigung zu 35.1 (38.1), ein Ersteintrag für alle
künftigen Registertexte (38.2), eine Tatsachennotiz zu 21.9 und 10.1 (38.3),
die Form von Sperrlistenpunkt 4 (38.4), die Entscheidung zu den Kostenkopien
(38.5) und zwei Berichtigungen an seinem eigenen Text (38.6) —, alle Fable-Texte
zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22h_schluessel_und_vollzug.md`
(Antwort auf die Anfragen 22f und 22h). Dazu die Tatsachennotizen aus TB-88
(38.7; `docs/belege/TB-88/ERGEBNIS_TB-88.md`, Messstand `8851f67`) und der
Schlussteil (38.8). Auftrag `docs/auftraege/MAC_TB-89_register_38.md`; Belege
`docs/belege/TB-89/`; Eingang `c140ca9`, Schritt-0-Commit `da251da`.
⛔ **Keine `.py` geändert, kein neues Modul, kein Import, kein neues Abbild,
keine Sonde angepasst, kein Vollzug, kein Wert verschoben** — 38.8.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (Kopf von
Abschnitt 0; 35.1 dreimal; 21.9 zweimal; 10.1; Sperrlistenpunkte 4 und 7,
Punkt 9 zweimal; 23.7; 37.4; 37.5 — vierzehn). Die alten Sätze bleiben zeichengleich; `git diff --numstat`
auf dieses Register zeigt für TB-89 in der zweiten Spalte `0`. Die Marken in
Abschnitt 10 stehen, wie seit 37, als eingerückte `>`-Zeilen **ohne
Leerzeile** unter dem Punkt; die Sperrlisten-Sonde ist vor und nach dem
Eintrag **lesend** gelaufen (38.8).

⭐ **Dieser Abschnitt wendet 38.2 schon auf sich selbst an:** Fundstellen im
Code stehen hier als Datei und Bezeichner; wo eine Zeilennummer steht, steht
sie in einer Tatsachennotiz und trägt den Commit, an dem sie gemessen wurde.
In den **Zitaten** stehen Zeilennummern, wie Fable sie geschrieben hat —
zeichengleich heisst zeichengleich.

### 38.1 ⭐⭐ Berichtigung zu 35.1 (Folge/Handwerk) — Weg (A): die letzte Falte heisst die Spanne

**Fable, 22h Abschnitt 3, zeichengleich — sein Befund:**

«Q:33»

**Die Entscheidung, zeichengleich:**

«Q:37»

**Seine Quelle des Grundes, zeichengleich:**

«Q:39»

**Zu dem Einwand des steuernden Chats gegen (A), zeichengleich** (33.3 führt
die Selektionsfalten als Feld, die Bestätigungsperiode als eigenes Feld; der
Schrägstrich ist mit Absicht kein Bindestrich):

«Q:41»

**Sein Handwerk daraus, zeichengleich** (das Fertigkriterium darin betrifft
38.7 (d)):

«Q:43»

**Seine Unsicherheit, zeichengleich:**

«Q:73»

⚠️⚠️ **Tatsachennotiz — Weg (B) hätte einen Sperrlistenpunkt berührt (TB-88,
M2b, `m2b_wege_a_b_probe.py`, nur im Speicher, Messstand `8851f67`):**
`research/vorregistrierung/auswertung.py`, Funktion `lies_zellen`, vergleicht
die **Menge** der `falte`-Werte je Zelle gegen die Faltennamen des Plans
(`[f["name"] for f in plan[bot]["falten"]]`, Z. 177–182 am Stand `8851f67`).
Schreibt der Erzeuger unter (B) den Bezeichner in die Spalte `falte`, bricht
die Auswertung **dort** ab (*„Falten stimmen nicht mit dem Faltenplan
ueberein"*); schreibt er den Faltennamen (B′), bricht sie in der Funktion
`bestaetigungsperiode` ab. Weg (A) läuft in derselben Probe durch
(`falte: '2026-01-01/2026-09-01'`, gemessen für `turtle_soup_stocks` mit den
Tabellen aus `_vt.json`). ⇒ Weg (B) hätte eine Änderung an `auswertung.py`
verlangt — **Sperrlistenpunkt 5** (Abschnitt 10). *Damit steht Fables
Entscheidung nicht nur auf einem Grund, sondern auf einer Messung.* ⚠️ Fables
Begründung nennt diese Messung nicht; sie ist nicht sein Grund, sondern steht
daneben. Nicht gemessen ist, was in Registertext, Abbild und Berichten sonst
an Faltennamen hängt (TB-88, Antwort 1).

**Tatsachennotiz zu Fables Unsicherheit (TB-88, M1 (e), Messstand
`8851f67`):** Die einzige Prüfung in `test_vorregistrierung.py`, die den
Bezeichner der Bestätigungsperiode vergleicht, ist `A3`
(`bp["falte"] not in selektionsfalten`, in `teil_a`); sie bleibt mit jeder
Spanne wahr. Die Fehlerklasse, die Fable befürchtet, ist dort an der
Bestätigungsfalte **nicht** gemessen — an den Selektionsfalten ist sie schon
eingetreten (`G6`, 38.7 (d)).

**Marken am alten Ort:** bei **35.1**, unter der bestehenden Marke aus 36.1 (4)
und 36.3 — eine für 38.1, eine für 38.7 (c).

### 38.2 ⭐ Registertext, Ersteintrag — Fundstellen: Datei und Bezeichner, Zeilennummern nur mit Commit

**Fable, 22h Abschnitt 4, zeichengleich — der Anlass:**

«Q:47»

**Der Registertext, zeichengleich:**

«Q:49»

**Seine Quelle des Grundes, zeichengleich:**

«Q:51»

**Belegt durch 38.7 (a):** Die Fundstellen in 35.1 (Z. 336 und Z. 368) waren
noch am Tag des Eintrags um zwei bzw. zweiundneunzig Zeilen gewandert —
durch einen Commit, der den Registertext nicht berührte (`4daa254`). Schon 30.3 hatte
festgehalten: *„Eine Zeilenangabe im Register trägt ab hier ihren
Commit-Stand mit."* 38.2 macht aus dieser Beobachtung eine Regel.

⭐ **Wo die Regel steht, und warum dort:** als Marke **im Kopf von
Abschnitt 0** dieses Registers — nicht bei den Prüfprinzipien
(`docs/projektfuehrung/`). Drei Gründe: (1) Sie ist **Registertext** und
bindet jeden künftigen Registertext; ein Registertext gehört ins Register,
das append-only ist und mit seinem Hash in `herkunft.py::register()`
eingeht — die Prüfprinzipien sind ein Arbeitsdokument des steuernden Chats,
nicht registriert und nicht append-only. (2) Wer einen Registertext schreibt,
schreibt ihn in dieser Datei; der Kopf von Abschnitt 0 ist die Stelle, an der
jeder Leser und jeder Schreiber vorbeikommt, bevor er einen Abschnitt öffnet.
(3) Die Prüfprinzipien regeln, wie geprüft wird; diese Regel regelt, wie
geschrieben wird — geprüft wird sie nach den Prüfprinzipien wie jeder andere
Registertext. *Eine Kopie bei den Prüfprinzipien wäre eine zweite Fassung
derselben Regel an einem zweiten Ort — genau das, was 21j und 37.5 für Werte
ausschliessen.*

**Marken am alten Ort:** im **Kopf von Abschnitt 0** (die Regel) und bei
**35.1** (die Tatsachennotiz 38.7 (a), an der sie belegt ist).

### 38.3 ⭐⭐ Tatsachennotiz zu 21.9 und 10.1 — der Vollzug von Punkt 4 vor dem Tag ist eine beauftragte Änderung nach 37.3

**Fable, 22h Abschnitt 5, zeichengleich — welcher Satz gilt, und warum 10.1
hier nicht greift:**

«Q:55»

**Die Tatsachennotiz, zeichengleich:**

«Q:57»

⭐ **Was sich damit für 21.9 ändert:** Das Wort „Amendment" in der
Betreiberentscheidung 21.9 bleibt zeichengleich stehen; es bezeichnet nach
diesem Eintrag **keinen** Vorgang nach 10.1. Die **Reihenfolge**-Entscheidung
aus 21.9 gilt weiter und ist nach Fable erfüllt. **Tatsachennotiz (TB-88, M5,
Messstand `8851f67`):** `_vt.json` trägt für alle neun Bots `status:
endgueltig`; `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl`
existiert nicht (`test -f`) — es gibt vor dem ersten Lauf kein Protokoll, in
das ein Amendment einzutragen wäre, wie Fables Grund voraussetzt.

**Marken am alten Ort:** bei **21.9**, unter der Betreiberentscheidung, und
bei **10.1**, unter dem Absatz zum append-only-Protokoll.

### 38.4 ⭐ Sperrlistenpunkt 4 — Form (ii): Form steht fest, Vollzug steht aus

**Fable, 22h Abschnitt 5, zeichengleich — die Form und seine Ablehnung von (i)
und (iii):**

«Q:59»

**Sein Fertigkriterium für den Vollzug, zeichengleich:**

«Q:61»

⛔ **Festgelegt ist die Form, nicht vollzogen.** Punkt 4 in Abschnitt 10 bleibt
zeichengleich; `benchmark_drawdowns.json` (`a163c498…`) und
`benchmark_drawdowns_vt.json` (`4549395f…`) sind vor und nach diesem Eintrag
gleich (38.8). Der Vollzug ist **Plan-Punkt 8** und hängt an **zwei offenen
Fragen** an Fable (`FABLE_ANFRAGE_2026-09-22i_slippage_ja_und_gruen_nein.md`):
(1) ob „`test_vorregistrierung.py` grün" Fertigkriterium bleibt (Abschnitt 3
der Anfrage, hier 38.7 (d)); (2) welche Tabelle Punkt 4 für `t3_supertrend`
vollzieht — `_vt.json` trägt dort eine Falte `2018`, die der Plan seit TB-72
nicht mehr hat, und `dd_toleranz` ist in `_vt.json` und
`benchmark_drawdowns_tb72.json` verschieden (TB-88, M5; Werte nach 27.1 nicht
wiedergegeben) (Abschnitt 4 der Anfrage). **Beide sind hier nicht
beantwortet.**

**Tatsachennotiz (TB-88, M5, Messstand `8851f67`) — was der Vollzug berührt,
lesend:** `test_vorregistrierung.py` (Funktion `_tabellen`),
`auswertung.py` (`main`) und `registerbericht.py` lesen heute
`ergebnisse/benchmark_drawdowns.json`; `registerbericht.py` liest dort den
Schlüssel `symbole_point_in_time`, den `_vt.json` nicht trägt (23.5:
`symbole_handelbar_in_falte`). `auswertung.py` steht als Punkt 3 und 5 auf der
Sperrliste.

**Marke am alten Ort:** bei **Abschnitt 10, Punkt 4** — ⚠️ ausdrücklich
*„Form steht fest, Vollzug steht aus"*.

### 38.5 ⭐⭐ Kosten — kein Laufmodul trägt eine eigene Kopie: neun Importe, nicht neun überwachte Kopien

**Fable, 22h Abschnitt 2, zeichengleich — die Entscheidung:**

«Q:21»

**Seine Begründung, zeichengleich** (darin der Kernsatz *„Ein Import ist keine
Prüfung, sondern eine **Struktur**"*):

«Q:23»

**Zu Punkt 7, zeichengleich — seine Rücknahme des 22d-Kandidaten:**

«Q:25»

**Zu `messgroessen.py` / `GEBUEHR_PCT`, zeichengleich:**

«Q:27»

⭐ **Was damit gilt, zusammengefasst — die Zitate oben sind massgeblich:**

| Ort | Stellung nach 38.5 |
|---|---|
| neun `strategies/*/backtest_*.py` (Laufpfad) | ersetzen ihre Zuweisung von `TRADING_FEE_PCT` / `SLIPPAGE_PCT` durch einen **Import** aus einem neuen Modul — **kein Laufmodul trägt eine eigene Kopie** (37.5 (2)) |
| neun `strategies/*/forward_test.py` (Papierpfad) | behalten ihre Kopien; **überwachte** Kopie, die Sonde prüft auf Gleichheit |
| `research/vorregistrierung/messgroessen.py`, `GEBUEHR_PCT` | bleibt eingefroren; **überwachte** Kopie unter anderem Namen, kein Laufort |
| Punkt 7: `registerdaten.py`, `CLUSTER_SCHWELLE` und `N_HISTORISCH_JE_BOT` | **nichts zu verschieben** — der Ort existiert; Punkt 7 bekommt ihn nachgetragen, die Sonde prüft Datei plus Wert |

⛔ **Nicht Gegenstand dieses Eintrags:** das neue Modul, die neun Importe, der
Nachtrag des Orts bei Punkt 7 und 9 und die Gleichheitsprüfung der Sonde —
Handwerk, TB-90 (Freigabe des Betreibers liegt nach dem Auftrag vor,
22.09.2026). Die Werte `0,1` / `0,05` / `0,90` ändern sich nicht.

**Marken am alten Ort:** bei **Abschnitt 10, Punkt 9** und **Punkt 7**, je
unter der Marke aus 37.5, die zeichengleich bleibt; bei **37.5**, direkt unter
dem Registertext.

### 38.6 ⚠️ Fables zwei Berichtigungen an sich selbst — Z. 51, und acht statt fünf Stellen

**Fable, 22h Abschnitt 1, zeichengleich:**

«Q:9»

«Q:11»

**Der Ersatzsatz für 37.4, zeichengleich:**

«Q:13»

«Q:15»

⭐ **Der alte Satz in 37.4 bleibt stehen** — Fables Tatsachennotiz aus 22d,
zeichengleich, mit „Z. 41" und „an fünf Stellen". Er bekommt die
ERSETZT-Marke; die Tatsachennotiz TB-87 (M3) in 37.4, die beides gemessen
hatte, ist der Beleg. Fables Ersatzsatz nennt dieselben acht Abweichungen,
die 37.4 gemessen aufgezählt hat (vier fehlend, dazu der bestimmte Pfad; vier
zusätzlich) — gegen die Liste in 37.4 verglichen: dieselben neun Dateien;
einziger Schreibunterschied, dass 37.4 den bestimmten Pfad als
`ergebnisse/benchmark_drawdowns_vt.json` führt, Fable ohne Ordner.

**Marke am alten Ort:** bei **37.4**, direkt unter Fables Tatsachennotiz.

### 38.7 ⭐ Tatsachennotizen aus TB-88

Quelle: `docs/belege/TB-88/ERGEBNIS_TB-88.md`, Messstand `8851f67`, soweit
nicht anders gesagt. Zwischen `8851f67` und dem Eingang dieses Auftrags hat
sich unter `research/` keine Datei geändert (`git diff --quiet 8851f67 HEAD --
research/`, gemessen in TB-89).

**(a) Die Fundstellen aus 35.1, heute.** Die Erzeugung des Bezeichners
(`"bestaetigungsperiode": falten[-1]["name"] …`, in
`research/vorregistrierung/faltenplan.py`, Funktion `_plan`) steht am Stand
`8851f67` auf **Z. 338**, die Konsolenausgabe (`best =
p["bestaetigungsperiode"]`, Funktion `main`) auf **Z. 460**. 35.1 nennt Z. 336
und Z. 368 (gemessen in TB-83, HEAD `9dac8d4`; so gültig seit `76c20ec`,
TB-80). Verschoben hat sie
**`4daa254`** (TB-86 Schritt 2 und 3: `--ziel`, Voreinstellung,
Einmal-Schreibsperre) — nicht `ee4e65c`, das ist der Abschlussbeleg von TB-86.
⭐ *Damit ist 38.2 belegt.* Die Namensbildung der Bestätigungsfalte — die
Stelle, die Fable in 38.1 meint — ist die Zuweisung der Rolle `bestaetigung`
in derselben Funktion `_plan` (Z. 307 am Stand `8851f67`).

**(b) ⭐⭐ Slippage — Fables Messbitte aus 22h Abschnitt 2, zeichengleich:**

«Q:29»

**Gemessen: ja.** **9 von 9** `strategies/*/backtest_*.py` tragen
`SLIPPAGE_PCT = 0.05` (derselbe Name, derselbe Wert) neben
`TRADING_FEE_PCT = 0.1` und rechnen `2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)` —
**0,30 %** je Rundlauf, genau die Summe aus Punkt 9, Ein- und Ausstieg. ⚠️
**Formabweichung ohne Wertunterschied:** `t3_supertrend/backtest_trend.py`
zieht die Kosten als `pnl_pct -= 2 * (…)` ab statt über `total_cost_pct = 2 *
(…)`. ⇒ **Der Befund, den Fable befürchtet hat, tritt nicht ein**; die
Voraussetzung aus 22h Abschnitt 6 ist erfüllt. ⚠️ *Herkunft:* Diese Messung
steht **nicht** in `ERGEBNIS_TB-88.md`, sondern in der Anfrage 22i des
steuernden Chats (Abschnitt 1, HEAD `ec54618`); in TB-89 lesend nachgemessen
am Stand `da251da` (`docs/belege/TB-89/m_slippage_backtest.txt`), gleich.

**(c) ⚠️⚠️ Weg (B) hätte einen Sperrlistenpunkt berührt.** Steht in 38.1;
Marke bei 35.1.

**(d) ⚠️⚠️ „rot" heisst heute: der Test stürzt ab — und nach dem Vollzug
bleibt er 163/2.** `research/vorregistrierung/test_vorregistrierung.py` läuft
am Stand `8851f67` **keine einzige Prüfung**: Mit aktiviertem `trading-env`
endet er in `teil_a` mit `KeyError: '2017'` in `auswertung.py`, Funktion
`zulaessigkeit` — **0 bestanden, 0 gescheitert**, die Schlusszeile wird nie
gedruckt, rc `1`. Ursache: der Test liest `ergebnisse/benchmark_drawdowns.json`
(TB-30a-Stand, für `turtle_soup_stocks` Falten `2019`–`2026`), der Plan beginnt
bei `2017`. Ohne venv scheitert er schon früher am fehlenden Paket `binance`.
Die **Simulation des Vollzugs** (Kopie des Ordners, nur dort die Tabelle
getauscht; `m4_simulation_punkt8.sh`) ergibt **163 bestanden, 2 gescheitert**:

| Prüfung | hängt an |
|---|---|
| `G6` (*„2020 und 2022 sind Testfalten, keine Trainingsjahre"*) | **nicht an Punkt 4.** Sucht die Faltennamen `2020` und `2022`; `elliott_wave` hat seit TB-61 Zweijahresfalten `JJJJ-JJJJ` — eine Annahme aus TB-30a |
| `H3` (*„ohne die gesetzte Null aendert sich die Statistik"*) | **nicht an Punkt 4.** Die Probe setzt vier Falten ohne Trade und rechnet laut eigenem Kommentar mit sieben Selektionsfalten; seit der ersten Falte `2017` sind es neun, der Median kippt nicht mehr |

⇒ Beide hängen am **Faltenplan** (TB-56/TB-61/TB-72), nicht an der
Benchmark-Tabelle. ⚠️ **Damit ist Fables Fertigkriterium
„`test_vorregistrierung.py` grün" (22h Abschnitt 5, zitiert in 38.4, und
Abschnitt 3, zitiert in 38.1) heute nicht erreichbar.**

⚠️⚠️ **OFFENE FRAGE — eingetragen, nicht entschieden:** Bleibt „grün"
Fertigkriterium von Plan-Punkt 8? Die Anfrage 22i (Abschnitt 3) legt Fable
drei Lesarten vor — (1) fertig, wenn der Absturz weg ist, `G6`/`H3` werden ein
eigener Punkt; (2) Punkt 8 umfasst `G6`/`H3`; (3) „grün" bleibt, beide als
bekannt rot mit Grund, was A4 und 21.9 widerspräche. **Die Frage liegt bei
Fable; dieses Register beantwortet sie nicht**, auch nicht durch die
Reihenfolge der Lesarten oder die Neigung des steuernden Chats, die dort
steht. Bis zu seiner Antwort gilt 21.9 unverändert: der Test ist **„offen
durch eigene Änderung — blockierend für den Tag"**; neu ist nur die gemessene
Tatsache, dass „rot" dort einen Absturz bezeichnet. *Ein Registerabschnitt
darf eine offene Frage tragen — 21.6 hat es vorgemacht.*

**Marken am alten Ort:** (a) und (c) bei **35.1**; (b) bei **Abschnitt 10,
Punkt 9**; (d) bei **21.9**, unter der Tabelle der Folgen (wo der rote Test
geführt wird), und bei **23.7**, unter dem Nachtrag TB-71.

### 38.8 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Keine `.py` geändert** — weder `faltenplan.py` (Namensbildung, 38.1) noch die neun `backtest_*.py` (Importe, 38.5); **kein neues Modul**, kein Import gesetzt | TB-90 |
| ⛔ | **Kein Vollzug von Punkt 4** — nur die Form (38.4); `benchmark_drawdowns.json` bleibt byteweise dieselbe Datei | Plan-Punkt 8, nach Fables Antwort auf 22i |
| ⛔ | **Kein neues Abbild**, keine Sonde angepasst, `python3 faltenplan.py` nicht aufgerufen; `registerbericht.py` und `test_vorregistrierung.py` nicht angefasst | — |
| ⛔ | **Kein alter Registersatz umgeschrieben** — der alte Satz in 37.4, die Zeilennummern in 35.1 und das Wort „Amendment" in 21.9 bleiben zeichengleich; ERSETZT- und Hinweis-Marken, nichts entfernt | — |
| ⛔ | **Keine offene Frage beantwortet** — weder „grün" als Fertigkriterium (38.7 (d)) noch die Tabelle für `t3_supertrend` (38.4) | Fable |
| ⭐ | **Keine Zahl bewegt:** die drei Sperrlisten-Hashes `a163c498…` (`benchmark_drawdowns.json`), `0e54ac5c…` (`faltenplan.json`), `4549395f…` (`benchmark_drawdowns_vt.json`) vor und nach dem Eintrag gleich; die Sperrlisten-Sonde lesend vor und nach dem Eintrag gegen `sperrliste_abbild_2026-09-22.json`: Prüfung (ii) `0`, Listentext wie bei Erzeugung, unverändert `1` nur an Punkt 2 (37.3) | — |
| ⚠️ | **Offen:** 22i Abschnitt 3 (grün), Abschnitt 4 (`t3_supertrend`), und ob `G6`/`H3` als eigener Punkt in den Plan vor dem Tag gehören · das neue Modul und die neun Importe (38.5) · die Namensbildung (38.1) · der Vollzug von Punkt 4 (38.4) · das neue Abbild danach — ein Abbild für alle drei Dateigruppen (22h Abschnitt 6) | Fable / Betreiber / TB-90 |

*Dieser Abschnitt ist rein additiv: Er trägt eine Berichtigung, einen
Ersteintrag, eine Tatsachennotiz, eine Formfestlegung, eine Entscheidung und
zwei Selbstberichtigungen des Verfahrensprüfers zeichengleich ein; setzt
vierzehn Marken am alten Ort; hält die Messungen aus TB-88 samt einer offenen
Frage fest — und entfernt nichts. Gebaut wird nichts.*

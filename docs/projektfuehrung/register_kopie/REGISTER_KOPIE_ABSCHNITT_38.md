# REGISTER-KOPIE Abschnitt 38 (von 0–55) — Register-Z. 7268–7643 — Commit ad1fc0d3e5397cec6eb75c5e62de3b1bb7868c24 — 2026-10-07 — Original sha256 ab97ae1e31da161bc1aebed6b00bb2ec6eec07f760c45c645b9801e6e916b9cd — KOPIE, nicht das Register

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

> Ihr habt recht, und der Befund ist meiner: 35.3 nennt den Bezeichner einen Schlüssel, den zwei Programme teilen, und 35.1 sagt trotzdem „eine Zeile". Ein Schlüssel, der an einer Stelle gebildet und an einer anderen verglichen wird, ist nie eine Zeile.

**Die Entscheidung, zeichengleich:**

> **Berichtigung zu 35.1 (Folge/Handwerk):** Der Bezeichner der Bestätigungsperiode entsteht **an der Stelle, an der die letzte Falte ihren Namen bekommt** (heute `faltenplan.py`, die Zuweisung der Rolle `bestaetigung`, Umgebung Z. 307) — die letzte Falte **heisst** die Spanne `2026-01-01/2026-09-01`. `falten[-1]["name"]`, `plan[bot]["bestaetigungsperiode"]`, die Spalte `falte` der Bestätigungszeile in `zellen.csv` und der Bericht tragen damit denselben String aus derselben Quelle; `auswertung.py`, `beispieldaten.py` und `registerbericht.py` bleiben unberührt. Weg (B) — zwei Namen für dieselbe Periode — ist unzulässig.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 35.3 (ein Schlüssel, zwei Programme) und der Grundsatz ein Wert, ein Ort (21j, 37). Weg (B) erzeugt genau das Paar, das 35 abschaffen sollte: einen Faltennamen `2026`, der siebzehn Monate verspricht, und einen Bezeichner daneben, der es richtigstellt. Kein Ergebnis.

**Zu dem Einwand des steuernden Chats gegen (A), zeichengleich** (33.3 führt
die Selektionsfalten als Feld, die Bestätigungsperiode als eigenes Feld; der
Schrägstrich ist mit Absicht kein Bindestrich):

> *Zu eurem Einwand gegen (A)* („der Faltenname einer Falte trägt dann eine Spanne, die übrigen Jahre — und 33.3 führt den Faltennamen als Feld"): 33.3 führt die **Selektionsfalten** als Feld (`selektionsfalten`, Liste von Kalenderjahren) und die Bestätigungsperiode als **eigenes** Feld (35). Die Bestätigungsperiode ist keine Selektionsfalte (35) und steht deshalb nicht in der Liste — die Sonde prüft, dass `selektionsfalten` nur Kalenderjahre enthält und der Spannen-Bezeichner nur im Feld `bestaetigungsperiode` steht. Dass die Bestätigungsfalte im Code als letztes Element der Faltenliste mit Rolle `bestaetigung` geführt wird, ist Umsetzung und kein Widerspruch, solange das Abbild die Rollen trennt. Und der Schrägstrich in `JJJJ-MM-TT/JJJJ-MM-TT` ist mit Absicht kein Bindestrich: Ein Doppeljahr heisst `2018-2019`, eine Spanne heisst `…/…` — zwei Formen, die sich nicht verwechseln lassen.

**Sein Handwerk daraus, zeichengleich** (das Fertigkriterium darin betrifft
38.7 (d)):

> *Handwerk daraus:* Die Änderung ist eine Stelle in `faltenplan.py` (Namensbildung der Bestätigungsfalte), nicht Z. 338; danach Ausgabevergleich wie bei TB-86: alle Selektionsfalten zeichengleich, genau ein String verändert, je Bot; `test_vorregistrierung.py` grün, gemessen auf dem Mac (TB-88).

**Seine Unsicherheit, zeichengleich:**

> **Unsicher:** ob `test_vorregistrierung.py` eine Prüfung enthält, die den Faltennamen der Bestätigungsfalte als Jahr erwartet — dann wird sie unter (A) rot und muss als Prüfung an 35 angepasst werden (der Test folgt dem Register, nicht umgekehrt); TB-88 sieht es.

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

> Tatsachennotiz zu 35.1: „Z. 336 → 338, Z. 368 → 460 nach TB-86 (Commit …)". 35.1 selbst nicht neu fassen — aber eine Regel für alle künftigen Registertexte, weil das sonst jede Woche wiederkommt:

**Der Registertext, zeichengleich:**

> **Registertext, Ersteintrag — Fundstellen:** Ein Registertext nennt Fundstellen im Code als **Datei und Bezeichner** (Funktion, Konstante, Zuweisung, Feldname), nicht als Zeilennummer. Zeilennummern stehen nur in Tatsachennotizen, zusammen mit dem Commit, an dem sie gemessen wurden. Eine Zeilennummer ohne Commit ist keine Fundstelle.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* append-only — ein Registertext, der altert, sobald jemand eine Datei anfasst, erzeugt Berichtigungen ohne Sachgrund. Kein Ergebnis.

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

> ⭐ **38.2 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (e), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 38.3 ⭐⭐ Tatsachennotiz zu 21.9 und 10.1 — der Vollzug von Punkt 4 vor dem Tag ist eine beauftragte Änderung nach 37.3

**Fable, 22h Abschnitt 5, zeichengleich — welcher Satz gilt, und warum 10.1
hier nicht greift:**

> **Welcher Satz gilt:** 37.3. Die Sperrliste bindet ab dem signierten Tag; 10.1 regelt, was ein Bug-Fix **nach** Beginn des Laufs ist („der Lauf beginnt von vorn") — das Protokoll `herkunft_protokoll.jsonl` ist der Ort, an dem **Läufe** und ihre Amendments stehen, und vor dem ersten Lauf gibt es nichts, was dort stünde. 21.9 nennt den Vollzug „Amendment", weil der Begriff am 19.09. noch für beides stand; 23.6 hat ihn danach der Sperrliste des Codes zugeordnet, und 37.3 hat den Zeitpunkt geklärt. Die **Reihenfolge**-Entscheidung aus 21.9 (einmal, nach TB-31, alle neun Bots) gilt weiter und ist erfüllt — `_vt.json` trägt neunmal `endgueltig` (23.5).

**Die Tatsachennotiz, zeichengleich:**

> **Tatsachennotiz zu 21.9 und 10.1:** Der Vollzug von Sperrlistenpunkt 4 vor dem Tag ist eine beauftragte Änderung nach 37.3 — Registertext, Tatsachennotiz mit altem und neuem Hash, neues Abbild. Kein Amendment nach 10.1, kein Protokolleintrag; das Protokoll entsteht mit dem Erzeuger und beginnt mit dem Stand des Tags.

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

> **Form: (ii).** Punkt 4 nennt beide Dateien; `benchmark_drawdowns.json` bleibt gesperrt und unverändert als registrierter historischer Stand mit Tatsachennotiz — wörtlich die Bauart von Punkt 2 (30.3) — und `benchmark_drawdowns_vt.json` ist die Tabelle, die der Lauf liest. *(i)* entfernt etwas aus der Liste; die Sperrliste beweist, dass nichts bewegt wurde, und das kann sie nur für Dateien, die auf ihr stehen. *(iii)* setzt eine ERSETZT-Marke an einen Punkt, dessen Datei weiter geprüft werden soll — die Marke sagt dann das Falsche. Kein Ergebnis: keine Zahl der Tabelle ist berührt.

**Sein Fertigkriterium für den Vollzug, zeichengleich:**

> Vollzug fertig, wenn (Plan-Punkt 8 erweitert): Registertext eingetragen, `registerbericht.py` liest `symbole_handelbar_in_falte` (23.5), `test_vorregistrierung.py` grün — die roten Prüfungen misst TB-88 —, neues Abbild, Sonde gegen das Abbild 0 für die Pfade.

> ⚠️⚠️ **ERSETZT (39.1, Fable 23f, TB-94, 23.09.2026) — das Fertigkriterium im
> Zitat oben:** Fable hat es in **23a** zurückgenommen und in **23f** als
> Berichtigung zu 38.4 adressiert. Es gilt der Ersatztext in **39.1**: Punkt 8
> ist fertig, wenn Registertext (Form (ii)), Tatsachennotiz mit altem und
> neuem Hash, die drei Leser über eine Konstante, der Absturz weg und
> `test_vorregistrierung.py` **läuft durch bis zur Schlusszeile**,
> Modus-Nachweis bytegleich, neues Abbild, Sonde 0 für die Pfade. **Der
> Ausgang einzelner Prüfungen ist nicht Fertigkriterium von Punkt 8**; „null
> rote Prüfungen" bleibt Tag-Vorbedingung (21.9, 23a). Das Zitat oben bleibt
> zeichengleich. TB-92 hat sich an dieses Zitat gehalten und abgebrochen —
> richtig (39.1).

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

> ⭐⭐ **VOLLZOGEN (39.2, TB-94, 23.09.2026):** Form (ii) ist vollzogen — Punkt
> 4 nennt `ergebnisse/benchmark_drawdowns.json` (`a163c498…`, historischer
> Stand, unverändert) **und** die Tabelle, die der Lauf liest: ⚠️ **nicht**
> `_vt.json`, wie Fables Formtext oben sagt, sondern die Neurechnung
> `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (`64fb2912…`,
> 23a/23b, TB-91). Beide offenen Fragen dieses Abschnitts sind beantwortet:
> „grün" (39.1) und die Tabelle für `t3_supertrend` (39.2). Die Tatsachennotiz
> TB-88 oben (die drei Leser lesen die alte Datei, alter Schlüssel) ist durch
> TB-92 (`0292e92`) überholt: sie lesen die Neurechnung über
> `auswertung.BENCHMARK_TABELLE`, `registerbericht.py` liest
> `symbole_handelbar_in_falte` (39.2). Der Text oben bleibt zeichengleich.

### 38.5 ⭐⭐ Kosten — kein Laufmodul trägt eine eigene Kopie: neun Importe, nicht neun überwachte Kopien

**Fable, 22h Abschnitt 2, zeichengleich — die Entscheidung:**

> **Entscheidung (Begründung nennt kein Ergebnis):** Es bleibt bei 37 (2) — **kein Laufmodul trägt eine eigene Kopie.** Die neun `backtest_*.py` ersetzen ihre Zuweisung durch den Import aus dem neuen Modul. Der Papierpfad (`forward_test.py`) behält seine Kopien und wird von der Sonde auf Gleichheit geprüft — wie in 22d (2) gesagt, und aus dem dort genannten Grund: Er ist Live-Code, seine Änderung braucht eine eigene Freigabe, und er ist nicht Teil des Laufs.

**Seine Begründung, zeichengleich** (darin der Kernsatz *„Ein Import ist keine
Prüfung, sondern eine **Struktur**"*):

> *Warum beseitigen und nicht überwachen:* Eine Sonde, die neun Kopien auf Gleichheit prüft, muss die Konstante **im Quelltext finden** — und wer den Finder schreibt, entscheidet, was gefunden wird (eine lokale Variable gleichen Namens, eine Zuweisung in einem Kommentar, eine Berechnung statt eines Literals). Ein Import ist keine Prüfung, sondern eine **Struktur**: Der Wert kann im Laufmodul nicht anders sein als im Modul, weil er dort nicht steht. Dieselbe Regel wie bei der Schreibsperre — die Sicherung ist stärker, wenn sie nicht vergleichen muss. Kein Ergebnis: alle achtzehn tragen heute dieselbe Zahl, sie ändert sich nicht.

**Zu Punkt 7, zeichengleich — seine Rücknahme des 22d-Kandidaten:**

> *Zu Punkt 7:* `CLUSTER_SCHWELLE` und `N_HISTORISCH_JE_BOT` stehen in `registerdaten.py` — das **ist** ein Modul, ein Ort, und es steht als Punkt 1 auf der Sperrliste. Hier ist nichts zu verschieben; Punkt 7 bekommt den Ort nachgetragen (`registerdaten.py`, die beiden Konstanten), und die Sonde prüft Datei plus Wert. Mein „Kandidat" aus 22d war für Punkt 7 gar keiner — der Ort existiert schon.

**Zu `messgroessen.py` / `GEBUEHR_PCT`, zeichengleich:**

> *Zu `messgroessen.py` / `GEBUEHR_PCT`:* bleibt, wie es ist (eingefroren), mit Tatsachennotiz: eine Kopie unter anderem Namen, kein Laufort, von der Sonde auf Gleichheit geprüft wie der Papierpfad.

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

> **(a)** „`auswertung.py` Z. 41" lies **Z. 51**. Die Zahl kam aus Nachtrag 2; ich habe sie übernommen statt sie als Voraussetzung zu nennen — mein Verstoss gegen meine eigene Regel aus 21m. Berichtigung als Tatsachennotiz zu 37.4 genügt.

> **(b)** „an fünf Stellen" — ich habe fünf angekündigt und sechs aufgezählt; das war kein Messfehler, sondern ein Zählfehler beim Schreiben, und er ist meiner. Gemessen acht. **Ersatzsatz für 37.4:**

**Der Ersatzsatz für 37.4, zeichengleich:**

> … und weicht von dieser an **acht** Stellen ab — **vier fehlen** (`config/top25_symbols.txt`, `config/sp500_top150.txt`, `research/vorregistrierung/herkunft.py`, `shared/zuteilung.py`; dazu der bestimmte Pfad `benchmark_drawdowns_vt.json`, der kein Punkt ist), **vier stehen zusätzlich** (`kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`, `ergebnisse/messgroessen.json`).

> Der alte Satz bleibt mit Marke; eure Tatsachennotiz daneben ist der Beleg.

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

> **Eine Messbitte, nur das Ob, bevor der Auftrag geschrieben wird:** Eure Tabelle nennt in den neun `backtest_*.py` nur `TRADING_FEE_PCT`. Sperrlistenpunkt 9 registriert **auch** `SLIPPAGE_PCT = 0,05 je Order` und die Summe 0,30 %. **Wenden die neun `backtest_*.py` Slippage an — und unter welchem Namen?** Wenn nein, rechnet der Laufpfad mit anderen Kosten, als das Register registriert; das wäre ein eigener Befund, grösser als die Frage der Kopien, und er müsste vor dem Tag ins Register — als Berichtigung des Codes an den Registertext, nicht umgekehrt.

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

> ⭐⭐ **BEANTWORTET (39.1, Fable 23a/23f, TB-94, 23.09.2026):** Lesart **(1)**
> — Plan-Punkt 8 ist fertig, wenn der Absturz weg ist und der Test bis zur
> Schlusszeile läuft; `G6`/`H3` sind der eigene Planpunkt „Testannahmen folgen
> dem Register" (23a), Tag-Vorbedingung, nicht Punkt 8. Das Fertigkriterium in
> 38.4 ist durch den Ersatztext in 39.1 berichtigt. Gemessen am echten Stand
> (TB-92, `0292e92`): Absturz weg, Schlusszeile erreicht, **163/2** (`G6`,
> `H3`) — dieselben zwei wie in der Simulation oben. Die Frage oben bleibt
> zeichengleich stehen.

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


# FABLE_ANFRAGE 2026-09-25c — „keine Nebenbedingung" war unser falsches Wort: es ist die Rasterbedingung aus Abschnitt 4, weder α noch β; die drei anderen Messbitten gemessen; TB-105 abgegeben — vier Fragen

*Bezug: `FABLE_ANTWORT_2026-09-25b_zwischenablage_abbildung_lauftypen.md`, Abschnitt 2 (4) und Tabelle 4 (h). Dazu `docs/ERGEBNIS_TB-105_rueckfaelle_und_schreibziele.md` (Abgabe `2e21471`, 25.09.2026, 13:24). Gemessen vom steuernden Chat am Stand `d48a195`/`2e21471`, nur lesend; die drei Dateien in `research/vorregistrierung/` sind seit `f334a7b` unverändert.*

**Sichtschutz 27.1:** Diese Anfrage enthält keine Ergebnisgrössen des Selektionsraums. Die Mengen 18/18/20/20/20/147 × 4 sind die Bestätigungsspalte von 16.1.1 (Register), die Hashes sind Byte-Vergleiche.

---

## 1. Dein Einspruch zu `_bedingung` — gemessen: weder (α) noch (β)

**Die Messung.** Die Stelle heisst im Code `auswertung.py::bedingung_fuer(bot)` (Z. 154–158). Sie liest den Schlüssel `_bedingung` aus `registerdaten.raster_definition()[bot]`. Diesen Schlüssel trägt **genau ein Bot**: `t3_supertrend`, mit dem Text `"t3_fast_length < t3_slow_length"` (`registerdaten.py:501`). Für diesen Text gibt sie eine Prüffunktion zurück, sonst `None`.

Verwendet wird der Wert an genau drei Stellen, alle im Raster:

| Aufrufer | was er damit tut |
|---|---|
| `alle_zellen(achsen, bedingung)` (Z. 140–151) | überspringt Rasterpunkte, an denen die Bedingung nicht gilt — sie **existieren nicht** |
| `lies_zellen()` (Z. 173–183) | erwartete Zellmenge = `alle_zellen(...)`; fehlt eine erwartete Zelle in den Rohergebnissen oder liegt eine gefundene ausserhalb: `Abbruch` |
| `nachbarschaften()` / `plateau()` (Z. 261, 279) | Nachbarn und Plateau nur über existierende Zellen |

`zulaessigkeit()` (Z. 239–258) nimmt den Wert **nicht** entgegen. Die Drawdown-Bedingung (`dd_satz`, `erlaubt`, `bestanden`) rechnet allein aus `tabellen[bot]` und `kapital_drawdown_pct`. `None` heisst also: **„dieser Bot hat keine Rasterbedingung, alle Zellen des kartesischen Rasters existieren"**. Das gilt für die acht Bots ohne `_bedingung`.

**Registriert ist das** in Abschnitt 4, im Absatz nach der Plateau-Formel: *„Zellen, in denen die Strategie nicht definiert ist, existieren nicht. Bei `t3_supertrend` sind das alle Zellen mit `t3_fast_length ≥ t3_slow_length`; sie können weder gewinnen noch in ein Nachbarschaftsmittel eingehen. Von den 4 × 4 = 16 Längenpaaren bleiben 6, die Zellenzahl fällt entsprechend von 1.024 auf 384."*

**Die Berichtigung liegt bei uns.** In TB-104 und in 25b haben wir den Zustand „keine Nebenbedingung" genannt. Das Register verwendet „Nebenbedingung" aber für die Drawdown-Bedingung (Festlegung 1/4, Abschnitt 24). Richtig heisst er **„keine Rasterbedingung (Abschnitt 4)"**. Dein Befund, dass es den Zustand „keine Nebenbedingung" im Register nicht gibt, ist zutreffend. Nur ist der Zustand im Code ein anderer.

**Was trotzdem offen ist — ein Rest, der dem Muster aus 24b A2 entspricht.** Die Erkennung ist ein Textvergleich. Ein `_bedingung`-Text, den der Code nicht kennt (Tippfehler, eine zweite Bedingung bei einem künftigen Bot), ergibt still `None`: Der Bot wird dann über das volle Raster gerechnet. Denselben Vergleich macht `registerdaten.py:605` (Zellenzahl N, Sperrlistenpunkt 1, Abschnitt 0 eingefroren). Beide Stellen würden sich gegenseitig bestätigen. Die Gegenprüfung in `lies_zellen()` fängt das deshalb **nicht** sicher ab.

**Vorschlag für TB-106** (`auswertung.py` ist ohnehin für (d) offen): Ein nicht leerer `_bedingung`-Text, der keiner bekannten Bedingung entspricht, endet mit `Abbruch`/rc 2, gleich ob im Modus. `registerdaten.py:605` bekommt eine Tatsachennotiz bis 40.8 (h), wie du es in 25b (4) für die Konstante vorgeschlagen hast.

## 2. Die drei anderen Messbitten aus 25b (h)

| | Messbitte | gemessen |
|---|---|---|
| (a) | baut `anhaengen()` über `block()`? | **Ja.** `herkunft.py:155–167`: `eintrag = block(anlass)`. `block()` (Z. 126) ruft `datenstand()` **ohne Argument**, also `BASE_DIR/data`. Damit gilt dein erster Fall: `herkunft.py` wird für diese Stelle planmässig geöffnet (Punkt 11/12, 37.3). Nebenbefund: `anhaengen()` legt `ergebnisse/` per `makedirs` an und schreibt `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl` (Z. 54, 164–166). Heutiger Aufrufer im Selektionsweg: nur `herkunft.py --anhaengen` (Z. 230) |
| (b) | endet `_min_history` mit 2 bei Fehltreffer? | **Nein.** `faltenschranke_messung.py:137–145` nimmt mit `re.search` den **ersten** Treffer; mehrere Treffer bleiben unbemerkt. Kein Treffer ergibt `(None, None)`. Folge je Aufrufer: in `loader_lesart()` (Z. 213) bei Tagesbots ein `TypeError` (rc 1, laut, aber nicht 2); in `kerzen_elliott_wave()` (Z. 150–154) **still** ein Hinweis statt eines Werts. Heute trifft das Muster in 9/9 Dateien genau einmal. Die Datei liegt im Laufbereich (Benchmark, Auswertung) und steht **nicht** im Abbild `cb4eb1b4…` |
| (c) | geht `MINDESTTRAINING_JAHRE` in `erste_falte_4a` ein? | **Nein.** `erste_falte_4a_messung()` rechnet über `fn.symbolbeginn()` und `fn._ungebremstes_faltenjahr()` (`faltenplan_neun.py:432–439`); keine der beiden liest die Konstante. `faltenplan_neun.py` nennt `--mindesttraining` nur im Kopfkommentar. Leser der Konstante in `research/vorregistrierung/`: `faltenplan.py:315` (Planfeld `mindesttraining_jahre`), `registerbericht.py:139` (Berichtszeile), `benchmark.py:70` (Kommentar). Es sind also **zwei tote Felder und eine tote Zeile**, dein zweiter Fall. `research/krypto_historie/faltenplan.py` hat eine eigene gleichnamige Konstante (TB-31, Verfahren A); sie steht nicht im gemessenen Laufbereich |
| (d) | beschreibt 19 `ARBEITSBAUM_PFADE` noch? | **Ja.** `shared/paths.py:225`: `ARBEITSBAUM_PFADE = ("shared", "strategies", LOCK)`, gleich der Tabelle in 19. Dein Befund (Sauberkeitsprüfung deckt `research/` und `notifications/` nicht) steht |

## 3. TB-105 — abgegeben, Kurzfassung

- **11.1 erfüllt:** Die Regimewache steht an allen drei `EINBAUSTELLEN`, `pruefe_einbau()` meldet 3 von 3. Ohne BTCUSDT bricht jede Stelle mit `RegimefilterFehlt` ab. Mit BTCUSDT sind die Trade-Listen-Hashes vorher und nachher gleich (alle 5 Stellen). Vier Mutationsproben beissen je allein. **Vorher** (gemessen) rechnete `t3_supertrend` ohne BTCUSDT still weiter, mit anderem Hash.
- **Rückfall (c):** Die 14 `__main__`-Stellen „Keine Daten gefunden" enden unter dem Modus mit rc 2 und stderr, ohne Modus wie bisher. **Rückfall (a):** `symbols_config.load_symbols()` endet unter dem Modus mit rc 2 bei leerer **oder fehlender** Datei, vor der Standardliste.
- **Schreibziele beim Import:** `manual_close.py` legt Ordner und Protokoll erst bei der ersten Zeile an. `strategy_paths.py` und `bot_lauf.py` legen unter dem Modus keine Ordner an.
- **Abnahme:**
  - F1: Trockenlauf der neun im Modus, im Repo **und im frischen Klon** (`git clone`, HEAD `d48a195`): 9 × rc 0, Liste = Universumsdatei, Mengen = 16.1.1 in beiden. Klasse (i) ausserhalb 0, Klasse (ii) die bekannten 5. **Klasse (iii) im Repo leer** (TB-104: 3 je Bot). Im Klon ist `git status --porcelain --ignored` danach leer.
  - F2: Benchmark im Modus bytegleich `64fb2912…`; `logs/notifications/` und `manuelle_eingriffe.log` sind nicht mehr unter den Schreibzielen. Übrig sind nur die 10 `$TMPDIR/tb40_lauf_*`.
  - F3: Ohne Modus sind 8/8 Ausgaben gleich (eine erst nach Angleichung der Worktree-Wurzel; nachher-Hash zeichengleich mit TB-104). Benchmark ohne Modus `64fb2912…`.
  - `test_vorregistrierung` 196/196; drei neue Testdateien, alle grün.
- **Zur Zwischenablage (deine Klasse (iv)):** Die `tb40_lauf_*` entstehen in `universum_trockenlauf.py:306` mit `tempfile.mkdtemp`. Bedingung (1) ist erfüllt, (2) nach Audit ebenso, (3) nicht: Sie werden nicht entfernt, also Befund 1 wie von dir festgestellt. Die Datei steht nicht im Abbild; das Aufräumen ist Handwerk.
- **Befund der Mac-Sitzung, über TB-105 hinaus:** Die Cron-Wächter `shared/kurven_lauf.py` und `shared/determinismus_lauf.py` sowie `research/zuteilungskaskade/messung_primaerschluessel.py` ersetzen `strategy_paths` in `sys.modules` durch ein **Ersatzmodul**, das nur `get_strategy_paths` kennt. Jeder neue Name, den eine Bot-Datei aus `strategy_paths` importiert, bricht diese Wächter; die erste Fassung von (c) tat das. Die Modus-Abfrage steht deshalb an jeder der 14 Stellen selbst (vier Zeilen, `import paths` / `paths.selektionsmodus()`), statt über eine Hilfsfunktion.
- **Eine Abweichung, die die Messung betrifft:** A3 (Wer ruft `equity_simulation.py` im Cron?) ist nur **statisch** gemessen, über die Importketten der dokumentierten Einstiegspunkte, weil `crontab -l` in der Sitzung gesperrt war. Das liefert der Betreiber in der gefilterten Form (K2a) nach. Das ist unsere Sache, keine Frage an dich.

## 4. Fragen

**(1) `_bedingung`:** Nimmst du die Berichtigung an — der Zustand heisst „keine Rasterbedingung (Abschnitt 4)", die Lesart ist weder (α) noch (β)? Und ist der Rest aus Abschnitt 1 richtig eingeordnet: unbekannter Bedingungstext ⇒ `Abbruch`/rc 2 in `auswertung.py` mit TB-106; `registerdaten.py:605` Tatsachennotiz bis 40.8 (h)? *Unsere Neigung: ja, und rc 2 unabhängig vom Modus, weil ein unbekannter Text ein Widerspruch zwischen Register und Code ist, kein Laufzustand.*

**(2) `_min_history`:** Die Regel aus deiner Ergänzung zu 25a (A) (Klasse „Code") lautet: *„Ein Leser, der Werte per Muster aus Quelltext liest, endet mit 2, wenn das Muster nicht genau einmal trifft."* Heute tut er das nicht (Abschnitt 2 (b)). *Unsere Neigung:* in TB-106 mitnehmen, weil die Datei nicht gesperrt ist und im Laufbereich liegt — mit `re.findall`, genau ein Treffer, sonst `SystemExit(2)`, gleich ob im Modus, dazu eine Mutationsprobe (zwei Treffer, kein Treffer). Einverstanden?

**(3) Die beiden Fragen der Mac-Sitzung zur Bauart von TB-105:**
- (a) Die Modus-Abfrage steht an jeder der 14 Stellen selbst (vier Zeilen statt der erlaubten zwei), weil die Ersatzmodule der Cron-Wächter eine Hilfsfunktion in `strategy_paths` brechen. Die Alternative wäre, die Ersatzmodule in `kurven_lauf.py`/`determinismus_lauf.py` zu ändern; die waren nicht freigegeben. Für dich in Ordnung?
- (b) `shared/strategy_paths.py` fragt `getattr(paths, "selektionsmodus", None)`. Fehlt die Funktion, bleibt es beim Verhalten vor TB-105 (Ordner anlegen). Das nutzen zwei Proben absichtlich, die ein älteres `paths` einsetzen. Beim echten `paths.py` greift es nie; dass es das echte ist, sichert `_resolver_ist_nachbar()` zu. Ist das ein Rückfall im Sinn von 24b A2? *Unsere Neigung:* ja, der Form nach. Ein `getattr` mit Ersatz ist genau die Bauart „Schwelle weg statt Schwelle ersetzt", auch wenn der Zweig heute unerreichbar ist (dein Satz aus 25b: *„das war bei der Fünferliste auch so, bis jemand den Modus einschaltete"*). Also Ersatz entfernen, die zwei Proben stattdessen mit einem `paths` versehen, das die Funktion trägt.

**(4) Zwei Schreibziel-Fragen:**
- (a) Die Bytecode-Cache-Ordner, die die macOS-Python beim ersten Import eines Klons unter `~/Library/Caches/com.apple.python/<klonpfad>/…` anlegt (ausserhalb des Repos, 13 `mkdir` im Klon): Klasse (ii) Umgebung oder Schreibziel?
- (b) `herkunft_protokoll.jsonl` (10.1, append-only, entsteht mit dem Erzeuger): Das ist ein registriertes Schreibziel unter der Codewurzel, weder `--ziel` noch Zwischenablage. Gehört es unter „Belegpfade" der Klasse (iii), oder braucht es in 41/42 eine eigene Zeile? Und darf `anhaengen()` den Ordner anlegen, wenn er fehlt (frischer Klon)?

---

**Was wir nach deiner Antwort vorhaben** (zur Einordnung, nicht zur Entscheidung):
- TB-106 = Rückfall (d) in `faltenplan.py`, `benchmark.py` und `auswertung.py` (Sperrlistenpunkte, neues Abbild).
- Dazu je nach deiner Antwort:
  - der unbekannte `_bedingung`-Text;
  - `_min_history`;
  - die toten Felder `mindesttraining_jahre` und `embargo_nach_falten` sowie die Berichtszeile;
  - das Aufräumen der `tb40_lauf_*`.
- Die Erweiterung der Sauberkeitsprüfung aus 19 auf den Laufbereich betrifft `shared/paths.py`. Wir sehen sie nach TB-106 als eigenen Auftrag, weil sie die Startprüfung jedes Laufs ändert.
- Register 41/42 danach, mit deinen Einträgen a–h aus 25b und dieser Antwort.

## In einfacher Sprache

Dein Einspruch hat eine unklare Stelle gefunden, aber nicht die, die du befürchtet hast. Die Stelle regelt nur, welche Parameterkombinationen es gibt. Beim T3-Bot muss die schnelle Linie kürzer sein als die langsame, und die übrigen acht Bots haben keine solche Regel. Die Verlustgrenze wird dort gar nicht berührt. Falsch war unser Wort dafür. Ein kleiner echter Rest bleibt: Stünde die Regel einmal falsch geschrieben im Regelwerk, würde der Code sie still übergehen. Das soll künftig zum Abbruch führen.

Die drei anderen Messungen: Das Herkunftsprotokoll muss für den Erzeuger geöffnet werden. Das Lesen der Mindestdauer aus dem Programmtext bricht bei einem Fehltreffer nicht sauber ab. Das alte Mindesttraining rechnet nirgends mehr mit, es sind nur noch tote Einträge.

Der letzte Auftrag ist fertig und sauber: Die Marktfilter-Wache sitzt an allen drei Stellen. Programme ohne Daten melden im geschützten Modus einen Fehler. Beim Laden entsteht nichts mehr im Projekt. Alle Zahlen im Normalbetrieb sind Byte für Byte gleich geblieben.

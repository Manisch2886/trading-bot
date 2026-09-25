# TB-107 — Die nicht gesperrten Rückfälle: `_min_history` genau ein Treffer, die zweite Kopie in `faltenplan_neun.py`, das `getattr` in `strategy_paths.py`, die `tb40_lauf_*`-Ablagen; Gegenprobe über alle `__main__`-Stellen

**Sitzungstitel:** `TB-107` · **Angelegt:** 25.09.2026, 20:35, vom steuernden Chat
**Grundlage:**
- Fable 25c 4 (2): `_min_history` genau ein Treffer, sonst 2, unabhängig vom Modus; `kerzen_elliott_wave()` und `loader_lesart()` gehen mit;
- Fable 25c 4 (3)(a): Gegenprobe, dass jede `__main__`-Stelle im Laufbereich die Modus-Abfrage trägt;
- Fable 25c 4 (3)(b): der `getattr`-Ersatz in `strategy_paths.py` ist ein Rückfall, also entfernen;
- Fable 25b 3 (1): Klasse (iv) Zwischenablage, „nie entfernt“ ist Befund 1;
- Ergebnis TB-106, Befund 1: die zweite Kopie von A1/A2 in `faltenplan_neun.py`.

**Vorgänger:** TB-106 (`f22f91e`) · **Aufwand:** hoch (ARBEITSWEISE 22.1)
⚠️ **Fables Antwort auf die Anfrage 25d steht noch aus.** Block C (die Kopie in `faltenplan_neun.py`) folgt der Betreiberentscheidung von 20:27, **vor** Fables Antwort. Sagt Fable „nur Tatsachennotiz“, wird Block C mit einem eigenen Commit zurückgenommen. Deshalb bekommt Block C einen **eigenen** Commit.

> **In einfacher Sprache, vorweg:** In den nicht gesperrten Hilfsprogrammen stecken noch vier Notlösungen:
> - Ein Programm liest eine Zahl aus dem Programmtext und merkt nicht, wenn es sie nicht oder doppelt findet.
> - Ein zweites Programm enthält dieselbe Notlösung wie die, die TB-106 geschlossen hat.
> - Ein Pfadprogramm nimmt „Regelbetrieb“ an, wenn es eine Funktion nicht findet.
> - Ein Messprogramm lässt nach jedem Lauf Zwischenordner liegen.
>
> Alle vier werden geschlossen. Dazu kommt eine Prüfung, die künftig meldet, wenn ein neues Skript die Modus-Abfrage vergisst. Im normalen Betrieb darf sich an keiner Zahl etwas ändern.

---

## ⭐⭐ Freigabe des Betreibers, wörtlich

**25.09.2026, 18:09** (Schnitt, Karte „Wie schneiden wir die Arbeit?“): **„Zwei Aufträge (Empfohlen)“**, TB-107 = die nicht gesperrten Stellen (`_min_history`, `getattr` in `strategy_paths`, Zwischenablage aufräumen, Gegenprobe über alle `__main__`-Stellen).

**25.09.2026, 20:27, zwei Auswahlkarten im steuernden Chat:**

| Frage | Antwort |
|---|---|
| *„Welche Dateien gibst du für TB-107 frei? Keine davon steht auf der Sperrliste. strategy_paths.py läuft aber im Live-Betrieb, im Papierpfad bei jedem forward_test.py.“* | **„Alle vier (Empfohlen)“**: `faltenschranke_messung.py`, `shared/strategy_paths.py` (ohne Modus bytegleich), `universum_trockenlauf.py`, dazu eine neue Gegenprobe über alle `__main__`-Stellen, mit ihren Tests |
| *„Fables Antwort auf 25d fehlt noch. Soll die zweite Kopie der Notlösung in faltenplan_neun.py trotzdem schon in TB-107 mit (rc 2 statt Ersatzwert)?“* | **„Ja, mitnehmen (Empfohlen)“**: Die Datei ist nicht gesperrt, der Zweig wird mit echten Daten nicht erreicht, `fn.json` muss bytegleich bleiben |

| freigegeben | Pfad | Block |
|---|---|---|
| ✔ | `research/faltenplan_neun/faltenschranke_messung.py` | B |
| ✔ | `research/faltenplan_neun/faltenplan_neun.py` (nur `volle_jahre()`/`faltenlaenge()`) | C |
| ✔ | `shared/strategy_paths.py` (Live-Code) | D |
| ✔ | `research/universum_trockenlauf/universum_trockenlauf.py` (nur `messe_bot()`) | E |
| ✔ | die Tests dieser Module; die Gegenprobe als Erweiterung von `shared/test_rueckfaelle_modus.py` oder als neue Testdatei unter `shared/` | F |

⛔ **Nicht freigegeben:**
- alles unter `research/vorregistrierung/` (Sperrliste; TB-106 ist dort abgeschlossen), `shared/paths.py`, `shared/regimewache.py`;
- `research/universum_trockenlauf/loaderlauf.py`;
- die drei Cron-Wächter `shared/kurven_lauf.py`, `shared/determinismus_lauf.py`, `research/zuteilungskaskade/messung_primaerschluessel.py` (Betreiberentscheidung 18:09: vorerst nur Tatsachennotiz);
- alle `strategies/`, `forward_test.py`, `live_params.py`, `crontab`, das Register.

Braucht eine Änderung eine dieser Dateien: **Auswahlkarte an den Betreiber**; ohne Antwort nicht ändern. **Kein neues Abbild:** Keine freigegebene Datei steht auf der Sperrliste (Abbild `40ffe18d…`, Sonde vorher = nachher).

⚠️ **Live-Code (`strategy_paths.py`):** Ohne Modus liefert das Modul Byte für Byte dieselben Pfade und legt dieselben Ordner an wie vorher.

---

## 0. Schritt 0

**0a — Arbeitsbaum des steuernden Chats committen.** Erwartet:

| Datei | Stand |
|---|---|
| `docs/auftraege/MAC_TB-107_nicht_gesperrte_rueckfaelle.md` | dieser Auftrag |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | Zeiger auf TB-107 |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-25d_tb106_abgegeben_vier_fragen.md` | neu (20:04) |

Weicht der Arbeitsbaum davon ab: melden, nichts Fremdes mitcommitten.

**0b — nach 7c:** `.git/*.lock` keine; HEAD am Eingang **`f22f91e`**; Datenstand `d9449faf…`; `*.db` vorher; Hashes aller freigegebenen und gesperrten Dateien vorher (`docs/belege/TB-106/hashes.sh`); Sonde gegen **`sperrliste_abbild_2026-09-25b.json`** (`40ffe18d…`) vorher; Zahl der `tb40_lauf_*`-Ordner in `$TMPDIR` vorher (nur zählen, nichts löschen).

---

## Block A — Vormessung

⚠️ Vormessung des steuernden Chats, nur lesend am Stand `f22f91e`. **Weicht deine Messung ab, gilt deine.**

| | Stelle | heute | Vormessung |
|---|---|---|---|
| **A1** | `faltenschranke_messung.py:137-145` `_min_history()` | `re.search`: nimmt still den **ersten** Treffer; kein Treffer ⇒ `(None, None)` | heute in 9/9 Dateien genau ein Treffer |
| **A2** | `faltenschranke_messung.py:150-154` `kerzen_elliott_wave()` | Schranke nicht `MIN_HISTORY_HOURS` ⇒ still `"hinweis"` statt Wert | welcher Name steht heute in `strategies/elliott_wave/multi_symbol_optimise.py`? |
| **A3** | `faltenschranke_messung.py:213 ff.` `loader_lesart()` | `n = None` ⇒ `TypeError` bei `timedelta(days=None)`, rc 1 | nach B unerreichbar |
| **A4** | `faltenplan_neun.py:363-380` `volle_jahre()`/`faltenlaenge()` | ohne inneres Jahr ⇒ erstes Jahr als Ersatz; leere Zählung ⇒ `return 2, 0.0` | wird mit echten Daten nicht erreicht (TB-106 A1/A2, gleiche Eingabe); melden, ob das für **diese** Kopie mit ihrem `basis`-Argument ebenso gilt |
| **A5** | `strategy_paths.py:112-125` `_im_selektionsmodus()` | `getattr(paths, "selektionsmodus", None)`; fehlt die Funktion ⇒ Verhalten wie ohne Modus (Ordner anlegen) | genutzt nur von zwei Proben (`test_paths` Probe A mit der Fassung TB-52, `test_strategy_paths` C4) |
| **A6** | `universum_trockenlauf.py:306` `messe_bot()` | `tempfile.mkdtemp(prefix="tb40_lauf_")` je Bot, nie entfernt | im Benchmark-Lauf 10 `mkdir` + 10 `w` (TB-106 G1) |
| **A7** | die 14 `__main__`-Stellen aus TB-105 C | tragen die Abfrage `paths.selektionsmodus()` je Stelle | Laufbereich zuletzt gemessen in `docs/belege/TB-104/d1_laufbereich_vereinigung.txt` (80 Module, 25.09.) |

**A8 — Aufrufer im Regelbetrieb** der vier Dateien, statisch wie TB-106 A9. Für `strategy_paths.py` gilt der Stand aus TB-105 A3: jeder `forward_test.py`, dazu die drei Cron-Wächter über ihr Ersatzmodul. `crontab -l` bleibt gesperrt.

Belege: `a_vormessung.txt`, `a8_aufrufer.txt`.

---

## Bauart für alle neuen Abbrüche

Wie TB-106:
- Meldung auf `stderr`, die Fall und Stelle nennt, dann `SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)` (= 2).
- `paths` so importiert, wie die Datei es schon tut. **Kein** neuer Name aus `strategy_paths` (TB-105 Befund 1: Ersatzmodule der Cron-Wächter).
- **Unabhängig vom Modus** (Fable 25c 4 (2): ein Widerspruch zwischen Register und Code ist kein Laufzustand).
- Je Stelle eine Probe, eine Mutationsprobe und eine Gegenprobe; jede Mutation beisst **allein** (24b B3).

## Block B — `faltenschranke_messung.py` (Fable 25c 4 (2))

- **B1:** `_min_history()` mit `re.findall` (gleiches Muster, gleicher `re.M`). **Genau ein Treffer**, sonst rc 2; die Meldung nennt Datei und Trefferzahl.
- **B2:** `kerzen_elliott_wave()`: Ist die Schranke nicht `MIN_HISTORY_HOURS`, folgt rc 2 statt des stillen `"hinweis"`. Vorher A2 messen. Steht dort heute **nicht** `MIN_HISTORY_HOURS`, **vor dem Bau melden**: Dann wäre der Hinweis heute der echte Pfad.
- **B3:** `loader_lesart()`: Nach B1 ist `n` nie `None`. Der `TypeError`-Pfad ist damit unerreichbar; belegen, nicht eigens umbauen.
- **B4:** Proben „zwei Treffer ⇒ 2“, „kein Treffer ⇒ 2“, „elliott_wave mit `MIN_HISTORY_DAYS` ⇒ 2“, jeweils in einer Kopie der Bot-Datei im Wegwerfbaum; Mutationsproben „`re.search` zurück“ und „Hinweis zurück“.
- **Abnahme:** `fsm.json` und `lesart.json` (Ausgaben 3 und 4 aus `docs/belege/TB-106/g2_ausgaben.sh`) sind bytegleich.

## Block C — `faltenplan_neun.py`, die zweite Kopie (eigener Commit)

- **C1:** `volle_jahre()` ohne inneres Jahr ⇒ rc 2; `faltenlaenge()` bei leerer Zählung ⇒ rc 2. Bauart wie TB-106 B1. Sonst nichts an der Datei.
- **C2:** Proben, Mutationen und Gegenproben wie TB-106 `B-A1`/`B-A2`.
- **Abnahme:** `fn.json` (Ausgabe 1) und `eft.json` bytegleich; `test_faltenplan_neun` 156/156, `test_erste_falte_trockenlauf`, `test_horizontbeginn` grün.

## Block D — `shared/strategy_paths.py` (Fable 25c 4 (3)(b))

- **D1:** `_im_selektionsmodus()` ruft `paths.selektionsmodus()` **direkt**, ohne `getattr` und ohne Ersatz. Fehlt die Funktion, bricht das laut ab (`AttributeError`). Das ist gewollt: „Ein Nachbar ohne die Funktion ist kein Nachbar.“
- **D2:** Die beiden Proben bekommen ein `paths` **mit** der Funktion (liefert `None`):
  - `test_paths` Probe A, die Fassung TB-52: Weiter gilt **99 Pfade, 0 Unterschiede**.
  - `test_strategy_paths` C4, der nachgebaute Resolver.
- **D3:** Neue Probe: ein `paths` **ohne** `selektionsmodus` ⇒ Abbruch, keine Ordneranlage. Mutationsprobe „`getattr` zurück“ ⇒ Probe rot, mit Gegenprobe.
- **Abnahme, Live-Code:** Ohne Modus liefern `get_strategy_paths()` für alle neun Bots und die bekannten Aufrufer dieselben Pfade, und es werden dieselben Ordner angelegt. `test_paths` 35/35, `test_strategy_paths` 23/23 plus neue, `test_ergebniskurven` (die Cron-Wächter mit Ersatzmodul) unverändert grün.

## Block E — `universum_trockenlauf.py`, die Zwischenablage (Klasse (iv))

- **E1:** In `messe_bot()` wird der `mkdtemp`-Ordner **am Ende entfernt**, nachdem das Ergebnis gelesen ist (`try/finally`).
  - Bricht der Kindprozess ohne Ergebnis ab (der bestehende `RuntimeError`), bleibt der Ordner stehen, und sein **Pfad steht in der Meldung**. Das ist Bedingung (3) aus 25b: „entfernt **oder** Pfad im Beleg“.
  - Sonst ändert sich nichts an der Funktion.
- **E2:** Proben:
  - Normallauf ⇒ nach `messe_bot()` existiert der Ordner nicht mehr.
  - Kindprozess ohne Ergebnis ⇒ Ordner da, Pfad in der Meldung.
  - Mutation „Aufräumen weg“ ⇒ erste Probe rot, mit Gegenprobe.
- **Abnahme:** `ut.json` und `sf.json` (Ausgaben 5 und 6) bytegleich. Benchmark-Lauf im Modus: Die `tb40_lauf_*` erscheinen im Audit weiter als `mkdir`/`w`, **existieren nach dem Lauf aber nicht mehr** (Zahl in `$TMPDIR` vorher = nachher). Im Ergebnis stehen sie als Klasse (iv) mit Bedingung (1) `mkdtemp`, (2) nur vom Lauf gelesen, (3) entfernt.

## Block F — Laufbereich neu messen und die Gegenprobe (Fable 25c 4 (3)(a))

- **F1:** Den Laufbereich **am Endstand dieser Sitzung** neu messen, mit dem Werkzeug aus TB-104 D1 (`docs/belege/TB-104/d1_listen.py`, `d_auswerten.py`, Haken). Gemessen werden dieselben drei Lauf-Typen: Trockenlauf, Benchmark im Modus, `auswertung.py`-Import. Ergebnis mit Datum als `f1_laufbereich_vereinigung.txt`; Unterschied zu den 80 von TB-104 je Modul nennen (erwartet: u. a. `shared/regimewache.py` neu).
- **F2 — Gegenprobe:** Ein Test prüft für **jede** Datei der Liste aus F1, dass jede Stelle im `__main__`-Block, die bei fehlenden Daten mit `exit()`/`sys.exit()` endet, die Abfrage `paths.selektionsmodus()` trägt. Suchen per AST, nicht per Zeilennummer. Die Liste liest der Test **aus der Datei F1**, nicht aus einem Literal. Ein Tatsachenkommentar im Test sagt: Die Liste wird am Tag-Commit durch die Tag-Messung ersetzt (Fable 25b (5)).
- **F3:** Mutationsprobe: Eine Kopie einer der 14 Dateien **ohne** Abfrage, der Liste hinzugefügt ⇒ Gegenprobe rot. Zweite Mutation: eine fünfzehnte, erfundene Datei mit „Keine Daten gefunden“ + `exit()` ohne Abfrage ⇒ rot. Dazu eine Gegenprobe.
- **F4:** Findet die Gegenprobe am echten Stand eine Stelle **ohne** Abfrage, die nicht in den 14 aus TB-105 war: **nicht** selbst ändern (die Datei ist nicht freigegeben), sondern melden. Der Test bleibt dann mit dieser Stelle rot, und das Ergebnis nennt sie.

**Commits:** (2) Block B · (3) Block C · (4) Block D · (5) Block E · (6) Block F. Jeweils mit Tests, nach jedem pushen.

---

## Block G — Abnahme

| | Soll |
|---|---|
| **G1** | `benchmark.py --ziel <scratch>` **im Modus, im Repo und im frischen Klon**: bytegleich **`64fb2912…`**. Klasse (iii) nur `--ziel`; die `tb40_lauf_*` als Klasse (iv), nach dem Lauf entfernt; im Klon dazu der Apple-Bytecode-Cache (Klasse (ii), 25c 4 (4)(a)) |
| **G2** | Ohne Modus: die 8 Ausgaben aus `docs/belege/TB-106/g2_ausgaben.sh` **8/8 bytegleich** gegen den Stand `f22f91e` (der Plan ist seit TB-106 der neue); Benchmark ohne Modus `64fb2912…` |
| **G3** | Trockenlauf aller neun im Modus (Repo): 9 × rc 0, Mengen = 16.1.1, Klasse (iii) 0 |
| **G4** | Tests: `test_faltenplan_neun` 156/156, `test_universum_trockenlauf` 163/163, `test_paths` 35/35, `test_strategy_paths`, `test_rueckfaelle_modus`, `test_ergebniskurven`, `test_vorregistrierung` 196/196, `test_ersatzwerte` 40/40, dazu alle neuen mit **Namen** |
| **G5** | Sonde gegen `40ffe18d…` vorher = nachher (kein Sperrlistenpfad bewegt); `herkunft.register()` unverändert `0ece95e2…` |

⛔ Sichtschutz 27.1: keine Kennzahl, keine Trade-Zahl, keine Faltenlänge je Bot im Ergebnis; Hashes und rc sind zulässig.

## Block H — Abgabe

| | |
|---|---|
| **H1** | Hashes nachher: Geändert sind nur die freigegebenen Dateien, ihre Tests und `docs/`. Gesperrte Dateien, Datenstand, Snapshot, `ergebnisse/` und `*.db` (bis auf den Cron) gleich |
| **H2** | Ergebnisdokument `docs/ERGEBNIS_TB-107_nicht_gesperrte_rueckfaelle.md`, darin ein Abschnitt **„Für Fable“** (27.1) mit: A2 gemessen; A4 erreicht oder nicht; die neue Laufbereichsliste mit Unterschied zu den 80; das Ergebnis der Gegenprobe am echten Stand (F4); Klasse (iv) für `tb40_lauf_*` mit den drei Bedingungen |
| **H3** | „Für die Folgesitzung vorbereitet“, „In einfacher Sprache“, Journalblock, `git --no-optional-locks status --porcelain` nach dem letzten Commit leer |

**Commits:** (1) Schritt 0 · (2)–(6) Blöcke B–F · (7) Belege und Ergebnis.

## ⚠️ Abbruchkriterien

1. Ohne Modus ändert sich eine der 8 Ausgaben oder ein Pfad aus `strategy_paths` ⇒ die betreffende Änderung zurücknehmen, melden.
2. Die Benchmark-Tabelle ist nicht bytegleich ⇒ nicht weiterbauen, melden.
3. A2 zeigt heute nicht `MIN_HISTORY_HOURS` ⇒ B2 nicht bauen, melden.
4. Eine Änderung bräuchte eine nicht freigegebene Datei ⇒ Auswahlkarte.
5. `test_ergebniskurven` wird durch D rot (Ersatzmodul der Cron-Wächter) ⇒ D zurücknehmen, melden.

---

## In einfacher Sprache

Diese Sitzung räumt die letzten bekannten Notlösungen in den nicht gesperrten Hilfsprogrammen auf:
- **Die Mindestdauer aus dem Programmtext:** Wird die Zahl nicht genau einmal gefunden, bricht das Programm ab, statt still die erste zu nehmen oder weiterzumachen.
- **Die zweite Kopie der Notlösung,** die TB-106 in den gesperrten Programmen geschlossen hat, bekommt denselben Abbruch.
- **Das Pfadprogramm** nimmt nicht mehr still „Regelbetrieb“ an, wenn eine Funktion fehlt.
- **Die Zwischenordner** eines Messprogramms werden nach jedem Lauf wieder entfernt.

Dazu kommt eine dauerhafte Prüfung: Vergisst ein Skript im geschützten Bereich künftig die Abfrage des Modus, wird der Test rot. Im normalen Betrieb darf sich an keiner Zahl und an keinem Pfad etwas ändern. Die Vergleichstabelle muss wieder Byte für Byte gleich herauskommen.

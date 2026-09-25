# TB-106 — Rückfall (d) in den eingefrorenen Dateien, unbekannter Bedingungstext ⇒ 2, tote Verfahren-A-Felder, `herkunft.py` für den Datenpfad geöffnet; neues Abbild

**Sitzungstitel:** `TB-106` · **Angelegt:** 25.09.2026, 18:20, vom steuernden Chat
**Grundlage:**
- Fable 24b A2 (kein Fallback unter dem Modus, auch nicht für Schwellen);
- Fable 25a Abschnitt 4 Rang 3: *„Vorab je Stelle Tatsachennotiz, ob die registrierte Eingabe den Schlüssel je auslässt; unabhängig davon Ersatz durch Abbruch 2“*;
- Fable 25b (4) und 3 (4): tote Felder `mindesttraining_jahre`, `embargo_nach_falten` und die Berichtszeile;
- Fable 25c Abschnitt 1: unbekannter Bedingungstext ⇒ 2, unabhängig vom Modus;
- Fable 25c 2 (a): Berichtigung zu 37.4, `herkunft.py` einmal geöffnet;
- Fable 25c 4 (4)(b): registriertes Protokoll, Ordner nicht anlegen;
- Register 37.3: planmässige Änderung mit Auftrag, Freigabe, altem und neuem Hash und neuem Abbild.

**Vorgänger:** TB-105 (`2e21471`) · **Aufwand:** hoch (ARBEITSWEISE 22.1)
**Nachfolger:** TB-107, die **nicht gesperrten** Stellen: `_min_history` in `faltenschranke_messung.py`, das `getattr` in `strategy_paths.py`, das Aufräumen der `tb40_lauf_*` in `universum_trockenlauf.py` und die Gegenprobe über alle `__main__`-Stellen. **Nicht hier.**

> **In einfacher Sprache, vorweg:** In den drei Rechenprogrammen des Auswahllaufs stehen noch stille Ersatzwerte: Fehlt eine Zahl, nehmen sie 0 oder 2 und rechnen weiter. Diese Sitzung ersetzt jeden davon durch einen Abbruch. Ausserdem fliegen zwei tote Felder aus dem alten Verfahren raus. Das Herkunftsprogramm wird für genau eine Stelle geöffnet, damit es im geschützten Modus den richtigen Datenordner hasht. Mit vollständigen Daten darf sich an keiner Zahl etwas ändern.

---

## ⭐⭐ Freigabe des Betreibers, wörtlich

**25.09.2026, 18:09, drei Auswahlkarten im steuernden Chat:**

| Frage | Antwort |
|---|---|
| *„Fable hat 25c beantwortet und die nächsten Schritte bestätigt. Wie schneiden wir die Arbeit?“* | **„Zwei Aufträge (Empfohlen)“**: TB-106 die eingefrorenen Dateien (`faltenplan.py`, `benchmark.py`, `auswertung.py`, `herkunft.py`, dazu die tote Zeile in `registerbericht.py`) und ein neues Abbild; TB-107 die nicht gesperrten Stellen |
| *„Welche eingefrorenen Dateien gibst du für TB-106 frei?“* | **„Alle vier (Empfohlen)“**: `faltenplan.py`, `benchmark.py`, `auswertung.py` für die Ersatzwerte (d), die toten Felder und den unbekannten Bedingungstext; `herkunft.py` planmässig geöffnet **nur** für den Datenpfad in `block()`/`anhaengen()` und ohne `makedirs`; `registerbericht.py` ist nicht gesperrt und geht mit; danach ein neues Abbild |
| *„Drei nächtliche Prüfprogramme ersetzen strategy_paths … Jetzt mitmachen?“* | **„Jetzt nicht (Empfohlen)“**: vorerst nur eine Tatsachennotiz; `kurven_lauf.py`, `determinismus_lauf.py` und `messung_primaerschluessel.py` bleiben unberührt |

| freigegeben | Pfad | Sperrliste | was |
|---|---|---|---|
| ✔ | `research/vorregistrierung/faltenplan.py` | Punkt 2, `EINGEFROREN` | Block B |
| ✔ | `research/vorregistrierung/benchmark.py` | Punkte 4/6, `EINGEFROREN` | Block C |
| ✔ | `research/vorregistrierung/auswertung.py` | Punkte 3/5/14, `EINGEFROREN` | Block D |
| ✔ | `research/vorregistrierung/herkunft.py` | Punkte 11/12 | Block E, **nur** Datenpfad und `makedirs` |
| ✔ | `research/vorregistrierung/registerbericht.py` | — | Block B, eine Zeile |
| ✔ | die Tests dieser Module (`test_vorregistrierung.py` u. a.), neue Proben im selben Ordner | — | — |
| ✔ | **ein** neues Sperrlisten-Abbild unter neuem Namen (`sperrliste_abbild.py --ziel`) | 36.6 | Block F |

⛔ **Nicht freigegeben:**
- `research/vorregistrierung/registerdaten.py` (Punkt 1, Abschnitt 0; `:605` bekommt **nur** eine Tatsachennotiz bis 40.8 (h));
- `kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`, `sperrlistensonde.py`, `sperrliste_abbild.py`;
- **alle Dateien unter `ergebnisse/`** (keine Tabelle, kein Plan, keine Messgrösse neu schreiben; einzige Ausnahme ist das neue Abbild);
- `faltenschranke_messung.py`, `shared/strategy_paths.py`, `research/universum_trockenlauf/` (alles TB-107);
- `shared/paths.py`, die drei Cron-Wächter, alle `strategies/`, `crontab`, das Register.

Braucht eine Änderung eine dieser Dateien: **Auswahlkarte an den Betreiber**; ohne Antwort nicht ändern.

⚠️ **„Planmässig geöffnet heisst nicht offen“** (Fable 25c 2 (a)): Jede freigegebene Datei trägt **genau** die hier beauftragten Änderungen. Nebenbefunde werden gemessen und gemeldet, nicht mitgebaut.

---

## 0. Schritt 0

**0a — Arbeitsbaum des steuernden Chats committen.** Erwartet:

| Datei | Stand |
|---|---|
| `docs/auftraege/MAC_TB-106_ersatzwerte_eingefroren_und_herkunft.md` | dieser Auftrag |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | Zeiger auf TB-106 |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-25c_rasterbedingung_und_tb105.md` | neu (13:45) |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-09-25b_zwischenablage_abbildung_lauftypen.md` | neu, aus der Projektablage übernommen |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-09-25c_rasterbedingung_abschnitt6_protokoll.md` | neu, aus der Projektablage übernommen |

Weicht der Arbeitsbaum davon ab: melden, nichts Fremdes mitcommitten.

**0b — nach 7c:**
- keine `.git/*.lock`;
- HEAD am Eingang **`2e21471`**;
- Datenstand vorher (Soll `d9449faf…`);
- Quersummen der `*.db` vorher;
- Hashes aller freigegebenen und aller gesperrten Dateien vorher, dazu Einzelhashes unter `ergebnisse/` (`docs/belege/TB-105/hashes.sh` als Vorlage);
- `herkunft.register()` vorher (Hash und `teile`);
- Sonde gegen **`sperrliste_abbild_2026-09-25.json`** (`cb4eb1b4…`) vorher.

---

## Block A — Vormessung nachmessen

⚠️ Die Vormessung stammt vom steuernden Chat, aus `docs/belege/TB-104/d3_vier_rueckfaelle.txt` Rang 3 und nur lesend am Stand `2e21471`. Die drei Dateien sind seit `f334a7b` unverändert. **Weicht deine Messung ab, gilt deine.**

| | Stelle | was heute geschieht | Vormessung |
|---|---|---|---|
| **A1** | `faltenplan.py:152-153` `volle_jahre()` | ohne innere Jahre: das erste, angeschnittene Jahr als Ersatz (`or {jahre[0]: …}`) | am echten Bestand nicht erreicht |
| **A2** | `faltenplan.py:159-160` `faltenlaenge_jahre()` | leere Zählung ⇒ `return 2, 0.0, "keine vollen Kalenderjahre gemessen"` | dto. |
| **A3** | `benchmark.py:206-207` `drawdown_bei_exposure()` | leeres Renditefenster ⇒ `0.0` | Funktion läuft, Zweig nicht gemessen |
| **A4** | `benchmark.py:302` `je_bot()` | keine Selektionsfalte ⇒ `dd_toleranz` `0.0` | Zweig nicht erreicht |
| **A5** | `benchmark.py:221-222` `nachschlagen()` | `e <= 0 ⇒ 0.0` | ⚠️ **vermutlich Rechenregel, kein Ersatzwert:** Die Interpolation unterhalb der ersten Stufe lautet `tabelle[stufe0] · e / stufe0` und geht für `e → 0` selbst gegen 0. **Nicht ändern**, nur belegen (A8) |
| **A6** | `auswertung.py:284, 286` `plateau()` | `statistik.get(zid, 0.0)` und `statistik.get(n, 0.0)` | nach `lies_zellen()`-Prüfung vermutlich unerreichbar, nicht gemessen |
| **A7** | `auswertung.py:333-334` + `380-385` | Platzhalter ohne Selektionsfalten ⇒ `bestimmt: False` ⇒ Kriterium (c) still `False` | nach der Platzhalter-Weigerung (Z. ~470) unerreichbar |
| **A7b** | `auswertung.py:500-521` und `dsr_drei_werte(bereinigung.get("renditen", []), …)` | `.get(…)` ⇒ `None`/`[]` | dto. |
| **A7c** | `auswertung.py:154-158` `bedingung_fuer()` | nicht leerer, unbekannter `_bedingung`-Text ⇒ still `None` | nur `t3_supertrend` trägt einen Text |
| **A7d** | `faltenplan.py:308` `embargo_nach_falten`, `:315` `mindesttraining_jahre`; `registerbericht.py:139` Berichtszeile | tote Felder bzw. tote Zeile; `MINDESTTRAINING_JAHRE` geht **nicht** in `erste_falte_4a` ein (25c 2 (c)) | Leser: nur diese drei Stellen und ein Kommentar in `benchmark.py:70` |
| **A7e** | `herkunft.py:126` `block()` ruft `datenstand()` ohne Argument; `:155-167` `anhaengen()` ruft `block()`; `:164` `makedirs` | unter dem Modus hasht die Kette `BASE_DIR/data` statt des Snapshots | `ergebnisse/` trägt 14 versionierte Dateien, existiert also in jedem Klon |

**A8 — je Stelle eine Tatsachennotiz**, wie Fable 25a sie verlangt:
- Kann die **registrierte** Eingabe (Snapshot `63e4b6c8…`, `messgroessen.json`, der gerechnete Plan) diesen Zweig erreichen? Erreicht ihn einer der gemessenen Läufe?
- Für A5 zusätzlich: der Grenzwert der Interpolationsformel bei `e → 0`, belegt mit zwei, drei kleinen `e` an der echten Tabelle.

**A9 — Aufrufer ausserhalb des Modus:** Wer importiert oder startet die vier Dateien im Regelbetrieb (Cron gefiltert nach K2a, Dashboard, andere `research/`-Skripte)? Das bestimmt, ob „rc 2 unabhängig vom Modus“ (Block B–D) jemanden im Betrieb trifft.

**A10 — der heutige Rückgabewert von `auswertung.Abbruch`:** Die Klasse erbt von `SystemExit` und wird mit Text geworfen, endet also vermutlich mit **1**. Nur messen und melden, nicht ändern: Die 13 bestehenden `Abbruch`-Stellen sind nicht Gegenstand dieses Auftrags.

**A11 — `TB30A_BASE_DIR` in `herkunft.py:51`:** eine Ersatzwurzel neben dem Resolver. Nur messen: Wer setzt sie, und greift sie unter dem Modus? **Nicht ändern** (die Öffnung gilt nur für den Datenpfad); gehört als Befund ins Ergebnis.

Belege: `a_vormessung.txt`, `a8_tatsachennotizen.txt`, `a9_aufrufer.txt`, `a10_abbruch_rc.txt`, `a11_tb30a.txt`.

⛔ **Erreicht die registrierte Eingabe einen der Zweige A1–A4, A6–A7b** (der Ersatzwert wirkt also heute im echten Lauf): diese Stelle **nicht** ändern, vor dem Bau melden. Das wäre dann kein toter Fallback, sondern eine gerechnete Regel, und die Frage geht an Fable.

---

## Bauart für alle neuen Abbrüche in B–E

- Meldung auf `stderr`, die den Fall und die Stelle nennt, dann **`SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)`** (= 2). `paths` wird so importiert, wie die Dateien es seit TB-104 schon tun; **kein** neuer Import aus `strategy_paths` (TB-105 Befund 1).
- **Unabhängig vom Modus**, ausser wo unten anders gesagt. Grund (Fable 25c 1 und 4 (2)): Ein fehlender Wert in diesen Dateien ist ein Widerspruch zwischen Register und Code oder Eingabe, kein Laufzustand. Zeigt A9 einen Aufrufer im Regelbetrieb, der den Zweig mit echten Daten erreichen kann: **vor dem Bau melden**.
- Je Stelle **eine Probe** („Zweig erreicht ⇒ rc 2“) und **eine Mutationsprobe** („Ersatzwert zurück ⇒ Probe rot“) mit Gegenprobe. Jede Mutationsprobe beisst **allein** (24b B3).

## Block B — `faltenplan.py` und `registerbericht.py`

- **B1:** A1 und A2 ⇒ rc 2.
- **B2:** Die Felder `embargo_nach_falten` (je Falte) und `mindesttraining_jahre` (je Plan) kommen aus dem gerechneten Plan, sonst zeichengleich. `registerbericht.py:139`: Die Zeile „Mindesttraining … Jahre“ fällt weg. `rd.MINDESTTRAINING_JAHRE` bleibt in `registerdaten.py` stehen: Tatsachennotiz „tot, kein Leser, bis 40.8 (h)“ im Ergebnis.
- **B3:** `G8`/`G8M` in `test_vorregistrierung.py` **anpassen, nicht löschen**: Die Feldliste verliert die beiden Schlüssel. `G8M` prüft künftig, dass ein wieder eingefügtes `mindesttraining_jahre` den Test rot macht. Fable 25b 3 (3): Die Feldliste wandert später in den Registertext; bis dahin bleibt sie benannter Zwischenstand.

## Block C — `benchmark.py`

- **C1:** A3 und A4 ⇒ rc 2.
- **C2:** A5 **nicht ändern**; der Beleg aus A8 steht im Ergebnis.

## Block D — `auswertung.py`

- **D1:** A6: Fehlt die Statistik einer existierenden Zelle oder eines Nachbarn ⇒ rc 2, kein `0.0`.
- **D2:** A7/A7b: Ein Plan ohne Selektionsfalten ⇒ rc 2 in `beta_bereinigung()`, kein `bestimmt: False`. Danach greifen `abbruchkriterien()` und `ein_bot()` direkt auf die Schlüssel zu, ohne `.get(…)`, ohne `else: c = False`. Das Ergebnis-JSON bleibt bei vollständigen Eingaben **zeichengleich** (F3).
- **D3:** A7c: Ein nicht leerer `_bedingung`-Text, der keiner bekannten Rasterbedingung entspricht ⇒ rc 2, **unabhängig vom Modus**. Die Deutung bleibt an **einer** Stelle (`bedingung_fuer()`); jeder Leser in `auswertung.py` ruft sie (heute schon so, belegen). Im Code- und Meldungstext heisst der Zustand ohne Text **„keine Rasterbedingung (Register Abschnitt 6)“**, nicht „keine Nebenbedingung“. `registerdaten.py:605` wird **nicht** geändert, nur als zweite Deutungsstelle im Ergebnis genannt (Tatsachennotiz bis 40.8 (h)).

## Block E — `herkunft.py`, planmässig für den Datenpfad geöffnet

- **E1:** `block(anlass, daten_dir=None)` und `anhaengen(anlass, daten_dir=None)` reichen `daten_dir` an `datenstand()` durch.
  - **Unter dem Modus** ist `daten_dir` Pflicht: `None` ⇒ rc 2 („keine Voreinstellung unter dem Modus“, Fable 25c 2 (a)).
  - **Ohne Modus** bleibt die heutige Voreinstellung `BASE_DIR/data`, und `block()` liefert zeichengleich dasselbe wie vorher (Zeitstempel ausgenommen).
- **E2:** Die CLI `--anhaengen` übergibt unter dem Modus `paths.DATA_DIR`.
- **E3:** `os.makedirs` in `anhaengen()` fällt weg. Fehlt der Ordner des Protokolls, endet `anhaengen()` mit rc 2, **unabhängig vom Modus** (25c 4 (4)(b): ein fehlender registrierter Ort ist ein Baum, der nicht der registrierte ist).
- **E4:** Sonst ändert sich **nichts**: `EINGEFROREN`, `register()`, `SPERRLISTE_DATEIEN`, `kette_pruefen()`, `BASE_DIR` samt `TB30A_BASE_DIR` bleiben zeichengleich.
- **E5 — Proben, nur im Wegwerfbaum,** weil `PROTOKOLL` an `_HIER` hängt: Das echte `herkunft_protokoll.jsonl` wird in dieser Sitzung **nicht** beschrieben.
  - Modus mit `daten_dir` = Snapshot-Daten ⇒ `datenstand` gleich dem über den Snapshot gerechneten Wert. Mess ihn und melde, ob er dem registrierten Datenstand `d9449faf…` entspricht; nicht annehmen.
  - Modus ohne `daten_dir` ⇒ rc 2.
  - Ordner fehlt ⇒ rc 2, kein Ordner angelegt.
  - Ohne Modus ⇒ Block gleich wie vorher.
  - Mutationsproben „Voreinstellung zurück“ und „`makedirs` zurück“, je allein.

**Commits:** (2) Block B · (3) Block C · (4) Block D · (5) Block E. Jeweils mit Tests, nach jedem pushen.

---

## Block F — Abbild und Sonde

- **F1:** Das neue Abbild entsteht **nach dem letzten Code-Commit**: `research/vorregistrierung/sperrliste_abbild.py --ziel research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-25b.json` (Name frei, wenn belegt). Eigener Commit (6).
- **F2:** Die Sonde läuft zweimal.
  - Gegen das **alte** Abbild `cb4eb1b4…` erwartet: Befund genau an den Punkten der geänderten Dateien, also 2, 3, 4, 5, 6, 11, 12, 14. **Jeder andere Punkt ⇒ melden.**
  - Gegen das **neue** Abbild: Pfad-Bestandteile ohne Befund.
- **F3:** `herkunft.register()` vorher und nachher, Hash und `teile`. Er ändert sich erwartungsgemäss, weil drei `EINGEFROREN`-Dateien geändert sind. Beide Werte stehen im Ergebnis (37.3: alter und neuer Hash).

## Block G — Abnahme

| | Soll |
|---|---|
| **G1** | `benchmark.py --ziel <scratch>` **im Modus**, im echten Repo **und im frischen Klon** (Fable 25b Abschnitt 1): bytegleich **`64fb2912…`**. Klassen wie TB-105 F2; Klasse (iii) nur `--ziel` und die bekannten `tb40_lauf_*` (die sind TB-107) |
| **G2** | Ohne Modus: die 8 Ausgaben aus `docs/belege/TB-105/f3_ausgaben.sh`. Sieben bytegleich. `plan.json` unterscheidet sich **nur** um die beiden entfernten Schlüssel; nach deren Entfernen aus der Vorher-Fassung Unterschied 0. Benchmark ohne Modus `64fb2912…` |
| **G3** | `auswertung.py` gegen die Beispieldaten (`beispieldaten.py`, wie `test_vorregistrierung`): Ergebnis-JSON vorher = nachher, zeichengleich |
| **G4** | Tests: `test_vorregistrierung` (neue Zahl nennen; vorher 196/196), `test_faltenplan_neun`, `test_universum_trockenlauf`, `test_paths` 35/35, `test_strategy_paths` 23/23, dazu alle neuen. **Namen** der neuen Proben im Ergebnis |
| **G5** | Trockenlauf aller neun im Modus wie TB-105 F1 (nur im Repo): 9 × rc 0, Mengen = 16.1.1. Belegt, dass `faltenplan.py` beim Import nichts bricht |

⛔ Sichtschutz 27.1: keine Kennzahl, keine Trade-Zahl, keine Faltenlänge je Bot im Ergebnisdokument; Hashes und rc sind zulässig.

## Block H — Abgabe

| | |
|---|---|
| **H1** | Hashes nachher: Geändert sind nur die freigegebenen Dateien, ihre Tests, das neue Abbild und `docs/`. Gesperrte Dateien, Datenstand, Snapshot, `ergebnisse/` ausser dem Abbild und `*.db` (bis auf den Cron) gleich. **Das echte `herkunft_protokoll.jsonl` ist unverändert** |
| **H2** | Ergebnisdokument `docs/ERGEBNIS_TB-106_ersatzwerte_eingefroren_und_herkunft.md` mit einem Abschnitt **„Für Fable“** (27.1). Er enthält: je Stelle A1–A7c die Tatsachennotiz aus A8 und was jetzt geschieht; den Beleg zu A5 (Rechenregel); A10 (`Abbruch` rc); A11 (`TB30A_BASE_DIR`); `datenstand` des Snapshots aus E5; `register()` alt/neu; neues Abbild mit Hash; Sonde alt/neu; `registerdaten.py:605` als zweite Deutungsstelle |
| **H3** | „Für die Folgesitzung vorbereitet“ (TB-107: `_min_history` samt `kerzen_elliott_wave`/`loader_lesart`, `getattr` in `strategy_paths.py`, `tb40_lauf_*`, Gegenprobe `__main__`), „In einfacher Sprache“, Journalblock, `git --no-optional-locks status --porcelain` nach dem letzten Commit leer |

**Commits:** (1) Schritt 0 · (2)–(5) Blöcke B–E · (6) Abbild · (7) Belege und Ergebnis.

## ⚠️ Abbruchkriterien

1. Die Benchmark-Tabelle ist nicht bytegleich (G1/G2) ⇒ nicht weiterbauen, melden.
2. Die registrierte Eingabe erreicht einen Ersatzwert-Zweig (A8) ⇒ diese Stelle nicht ändern, melden.
3. Die Sonde gegen das alte Abbild meldet einen Punkt ausserhalb 2/3/4/5/6/11/12/14 ⇒ melden, kein neues Abbild.
4. Eine Änderung bräuchte eine nicht freigegebene Datei ⇒ Auswahlkarte.
5. Ein Test schreibt das echte `herkunft_protokoll.jsonl` ⇒ sofort anhalten, melden.

---

## In einfacher Sprache

Die drei Programme, die im Auswahllauf den Zeitplan, die Vergleichstabelle und das Urteil rechnen, haben an sieben Stellen stille Notlösungen: Fehlt ein Wert, nehmen sie 0 oder eine feste Zahl und rechnen weiter. Keine dieser Stellen wird heute mit den echten Daten erreicht. Trotzdem sollen sie im Ernstfall abbrechen statt still etwas anderes zu rechnen. Genau das baut diese Sitzung ein, jeweils mit einer Probe, die zeigt, dass der Abbruch wirklich greift.

Dazu kommen drei Aufräumarbeiten:
- Zwei Felder aus einem alten, verworfenen Verfahren fliegen aus dem Zeitplan.
- Eine unbekannte Parameterregel führt künftig zum Abbruch.
- Das Herkunftsprogramm bekommt den richtigen Datenordner übergeben und legt keinen fehlenden Ordner mehr still an.

Weil diese Dateien auf der Sperrliste stehen, wird danach ein neues Abbild gezogen. Am Ende muss die Vergleichstabelle Byte für Byte gleich herauskommen, im Projekt und in einer frischen Kopie.

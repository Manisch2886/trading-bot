# TB-111: Ergebnis. Die gesperrte Öffnung aus Fable 25d: `herkunft.py` zeigt die Prüfansicht im Modus (Snapshot `d9449faf…`) und verweigert `TB30A_BASE_DIR` dort mit 2, bevor es liest; `auswertung.Abbruch` endet mit 2, Meldung wortgleich; neues Abbild `e655c1c8…`; Benchmark im Modus bytegleich `64fb2912…`

**Sitzungstitel:** `TB-111` · **Stand:** 26.09.2026, ca. 08:35 · **Auftrag:**
`docs/auftraege/MAC_TB-111_herkunft_auswertung_oeffnung.md` · **Belege:** `docs/belege/TB-111/`
**Ort:** Worktree `~/trading-bot-tb111`, Zweig **`tb-111`**, Eingang `f4d6d6d` (Schritt-0-Commit von TB-109).
Commits: `6cacfa4` (Block B), `6c98c38` (Block C), `1dcf273` (Abbild) und der Abgabe-Commit (Belege, dieses Dokument).
Alle vier auf `origin/tb-111` gepusht. **Kein Merge nach `main`, `JOURNAL.md` und `AKTUELLER_AUFTRAG.md` nicht angefasst.**
**Grundlage:** Fable 25d 2 (2), (3), (4); Fable 25c 2 (a); Register 37.3. Freigabe des Betreibers 25.09.2026, 23:14 (zwei Auswahlkarten, wörtlich im Auftrag).
**Umgebung aller Messungen:** Mac, `~/trading-bot/trading-env/bin/python3` (3.9.6), aus dem Worktree heraus.

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | Worktree `tb-111`, sauber, HEAD `f4d6d6d`. Hashes wie erwartet: `herkunft.py` `351f24c2…`, `auswertung.py` `83c6bc3c…`, `register()` `c85dd6c3…`. Sonde gegen `40ffe18d…`: 25/0/0, (ii) 0 |
| **A** | A1: Die Prüfansicht ruft `block("pruefung")` ohne Pfad und endet heute im Modus mit 2 (alle drei Formen). A2: **Kein Test** setzt `TB30A_BASE_DIR` zusammen mit dem Modus. ⚠️ **Neu gemessen:** `_paths()` lädt `paths.py` aus `BASE_DIR/shared`. Mit Modus und Ersatzwurzel endet die Prüfansicht deshalb heute mit **rc 1** (`ModuleNotFoundError`), nicht mit 2. A3: 12 Stellen `raise Abbruch(`. **Kein Test erwartet rc 1 von `auswertung.py`.** A4: Der Import bleibt unter dem Modus unverändert (kein `paths` geladen) |
| ⭐⭐ **B** | Die Prüfansicht übergibt im Modus `paths.DATA_DIR` (rc 0, `d9449faf…`/223). Modus + `TB30A_BASE_DIR` ⇒ rc 2 in `commit()`, `register()` und `block()`; die Meldung nennt die Variable; **der Lesehaken sieht 0 Zugriffe unter der Ersatzwurzel.** Ohne Modus bleibt alles unverändert. `_paths()` lädt jetzt aus der eigenen Wurzel |
| ⭐⭐ **C** | `Abbruch` endet mit **2**. An vier Brüchen (leer, Spalte, Zelle, Tage) geht rc 1 ⇒ 2; **stderr und stdout sind per `cmp` byte-gleich** vorher/nachher. Die 12 Stellen sind zeichengleich. Beispieldaten aller neun Bots zeichengleich **`fc178106…`** |
| **D** | Neues Abbild `sperrliste_abbild_2026-09-26.json` **`e655c1c8…`**. Sonde gegen das alte `40ffe18d…`: Befund **genau** an 3, 5, 11, 12, 14 und in der Gruppe `eingefroren`. Gegen das neue: 25/0/0, (ii) 0. `register()` `c85dd6c3…` ⇒ `e7d82547…` |
| ⭐⭐ **E** | E1: Benchmark im Modus aus dem Worktree **bytegleich `64fb2912…`**. E2: ohne Modus 8/8 gleich; 7 davon bytegleich, `ut.json` nach Ersetzen der absoluten Wurzel bytegleich (Klon gegen Worktree, siehe 5). E3: Trockenlauf 9 × rc 0. E4: alle Tests grün (Liste unten). E5: Geändert sind nur die zwei Dateien, `test_ersatzwerte.py`, das Abbild und `docs/`; das echte Protokoll existiert nicht |

Kein Abbruchkriterium hat gegriffen.

---

## 0. Schritt 0

| | |
|---|---|
| 0a | `pwd` = `/Users/jaquelineloffler/trading-bot-tb111`, Zweig `tb-111`, HEAD `f4d6d6d701b179f0ebf7befcc12f2b5f40a20b18`, `status --porcelain` leer (`0_schritt0.txt`). `main` stand im Hauptordner auf `6a7996a` |
| 0b | `hashes.sh vorher` (Vorlage TB-106, angepasst an den Worktree): freigegebene und gesperrte Dateien einzeln, `ergebnisse/`, 1538 versionierte Dateien ausserhalb `docs/`, Snapshot Soll = Ist, Datenstand `d9449faf…`/223, **0 `*.db` im Worktree** (die Datenbanken liegen nur im Hauptordner), `register()` `c85dd6c3…` (`0_hashes_vorher.txt`). Sonde gegen `40ffe18d…`: 25/0/0, (ii) 0, rc 2 nur wegen NICHT PRÜFBAR wie immer (`0_sonde_vorher.txt`) |

## 1. Block A: Vormessung

Beleg: `a_vormessung.sh` / `a_vormessung.txt`.

| | Messung |
|---|---|
| A1 | `main()` ruft an **einer** Stelle `block("pruefung")` ohne `daten_dir` (Z. 273 alt). Ohne Argument, `--json` und `--pruefen` laufen durch sie hindurch (`--pruefen` hat keinen eigenen Zweig). Ohne Modus rc 0, im Modus rc 2 mit `ABBRUCH (herkunft.py::block): … ohne daten_dir …` |
| A2 | Setzer im Code: `test_vorregistrierung.py:810` (`dict(os.environ)` + TB30A = Repo-Wurzel), `test_ersatzwerte.py:73` (entfernt `TB_SELEKTIONS*`, setzt TB30A), `test_erste_falte_trockenlauf.py:173` (kein Modus). `test_ersatzwerte.py:393`, `test_vorregistrierung.py:1113/1221`, `test_faltenplan_neun.py:775` und `test_universum_trockenlauf.py:1405` **entfernen** TB30A, bevor sie den Modus setzen. ⇒ **Kein Test setzt beides**; kein Test musste angepasst werden (E4 bestätigt das) |
| ⚠️ A2b | Heute, Modus + `TB30A_BASE_DIR=/gibt/es/nicht`: Die Prüfansicht endet mit **rc 1**, `ModuleNotFoundError: No module named 'paths'`. `_paths()` sucht `paths.py` in `BASE_DIR/shared`, also **unter der Ersatzwurzel**. Mit TB30A = echte Wurzel endet sie mit 2 (die Meldung nennt dann `daten_dir`, nicht die Variable). Schon die Frage „Modus?“ las also unter der Ersatzwurzel. Das bestimmt die Bauart von B2 |
| A3 | `grep -c "raise Abbruch("` = **12**. In `test_vorregistrierung.py`, `test_ersatzwerte.py` und `beispieldaten.py` prüft kein Test den Wert 1 von `auswertung.py`. A9/A10 fangen `SystemExit` allgemein (bleibt gültig, `Abbruch` erbt weiter von `SystemExit`). H5 (`returncode == 1`) gilt `pruefe_grenzsaetze.py`. ⇒ **Nichts umzustellen** |
| A4 | Im Modus ohne TB30A: Import ok, `paths` danach **nicht** in `sys.modules`, `datenstand(Snapshot)` = `d9449faf…`/223. `snapshot.lade_herkunft()` und `research/etf_trendfolge/datenstand.py` laden das Modul ebenfalls ohne Fehler |

## 2. Block B: `herkunft.py` (Commit `6cacfa4`)

- **B1:** `main()` nimmt `resolver = _paths()` und übergibt `resolver.DATA_DIR`, wenn `selektionsmodus()` nicht `None` ist, sonst `None`. Das ist dieselbe Form wie `--anhaengen` seit TB-106.
- **B2:** Die neue Funktion `_ersatzwurzel_pruefen(stelle)` bricht mit `_abbruch_2` ab (rc aus `paths.RUECKGABEWERT_STARTPRUEFUNG`). Voraussetzung: `TB30A_BASE_DIR` steht in der Umgebung oder `BASE_DIR` weicht von der eigenen Wurzel ab, **und** der Modus ist aktiv. Die Meldung beginnt mit „TB30A_BASE_DIR ist unter dem Selektionsmodus gesetzt (…)“. Aufgerufen wird die Funktion als **erste Zeile** von `commit()`, `register()` und `block()`.
  - `_paths()` lädt `paths.py` jetzt aus `_WURZEL = dirname(dirname(_HIER))`, der Wurzel, in der `herkunft.py` selbst liegt. Vorher kam es aus `BASE_DIR`.
- **B3:** `EINGEFROREN`, `datenstand()`, `kette_pruefen()`, `anhaengen()` und `verankerung()` sind zeichengleich. Zeile 51 (`BASE_DIR = …`) ist unverändert.

**Die Wahl in B2, begründet:**
1. **Die Prüfung sitzt in einer kleinen Funktion, nicht am ersten Gebrauch von `BASE_DIR`.** `BASE_DIR` und `REGISTERDATEI` werden beim Import gebildet. Der Import soll aber unverändert bleiben (A4), `datenstand.py` und `snapshot.py` importieren das Modul. Der erste *lesende* Gebrauch verteilt sich auf drei Funktionen. Fable 25d (3) begründet die Öffnung ausdrücklich mit dem kommenden Erzeuger, der `register()` und `commit()` **direkt** ruft. Deshalb prüfen diese beiden selbst und nicht nur `block()`.
2. **`_paths()` aus der eigenen Wurzel ist Teil von B2, kein Beifang.** Ohne diese Änderung liest schon die Modus-Abfrage unter der Ersatzwurzel (A2b). Dann gibt es nie rc 2, sondern je nach Ersatzbaum rc 1 oder ein fremdes `paths.py`. Das verletzt „erst 2, dann lesen“. Bei allen heutigen Setzern ist TB30A gleich der echten Wurzel, also `_WURZEL == BASE_DIR`: Ohne Modus ändert sich für sie nichts (E4, F-c).
3. **Nicht in `datenstand()` und `verankerung()`**, wegen B3 (zeichengleich).
   - `verankerung()` wird nur aus `main()` **nach** `block()` erreicht und ist damit gedeckt.
   - `datenstand(None)` liest `BASE_DIR/data`, im Modus mit oder ohne TB30A. Das ist offener Punkt 1 unten. Alle Aufrufer ausserhalb der Tests übergeben einen Pfad. `block()` verlangt ihn im Modus schon seit TB-106.
4. **Ohne die Variable wird `paths` in `commit()`/`register()` nicht geladen.** Die Bedingung wird vor `_paths()` geprüft. Ohne TB30A hat `register()` also keinen neuen Nebeneffekt.

**Eine Verhaltensänderung ohne Modus, am Rand:** TB30A auf einen Baum **ohne** `shared/paths.py` endete bisher in `block()` mit `ModuleNotFoundError` (rc 1). Jetzt wird `paths` aus der eigenen Wurzel geladen und der Lauf scheitert erst beim Lesen, bei einem nicht existierenden Baum mit `FileNotFoundError` (rc 1). Der Rückgabewert bleibt gleich, nur der Traceback ist ein anderer. Ein solcher Aufruf kommt im Repo nicht vor.

**B4, Proben:** `test_ersatzwerte.py` Teil F, 15 neue Prüfungen. Die Bauart ist ein Wegwerfbaum mit echter `paths.py`, wie Teil E. Einzeln mit Zahlen stehen sie in `b4_proben_einzeln.txt`.

| Probe | Soll | gemessen |
|---|---|---|
| F-a | Modus, Prüfansicht `--json` am echten Snapshot | rc 0, `d9449faf…`, 223 |
| F-a2/F-a3 | an der Snapshot-Attrappe: Snapshot gehasht, nicht `data/`; Form ohne `--json` | rc 0 / rc 0 |
| F-b, F-b2, F-b3, F-b4 | Modus + TB30A: Prüfansicht, `commit()`, `register()`, `block(Snapshot)` | je rc 2, Stelle und Variable in der Meldung, **0 Zugriffe** unter der Ersatzwurzel |
| F-c | ohne Modus + TB30A | Commit, Datenstand und Registerdatei der Ersatzwurzel wie vorher |
| F-aM (+G) | Mutation „Prüfansicht ohne Pfad“ | mit: rc 2 an `block`; Gegenprobe: rc 0 |
| F-bM (+G) | Mutation „Prüfung von TB30A weg“ | mit: rc 0, **5 Zugriffe** (git ×2, stat, open der Registerdatei …); Gegenprobe: rc 2, 0 Zugriffe |
| F-bM2 (+G) | Mutation „`paths` wieder aus `BASE_DIR`“ | mit: rc 1 `ModuleNotFoundError`; Gegenprobe: rc 2 |
| F-e | echtes `herkunft_protokoll.jsonl` | unberührt (existiert nicht) |

Der Lesehaken ist eine `sitecustomize.py` über `PYTHONPATH`. Er zeichnet `open`, `listdir`, `scandir`, `stat` (damit auch `exists`/`isdir`) und jeden Unterprozess auf, dessen Argument oder `cwd` unter der Ersatzwurzel liegt. F-bM zeigt, dass er nicht blind ist.

## 3. Block C: `auswertung.py` (Commit `6c98c38`)

```python
class Abbruch(SystemExit):
    """Ein Vertragsbruch in den Rohergebnissen. Nie eine stille Annahme.

    Ausgaenge von `auswertung.py`: 0 oder 2, kein 1 (Fable 25d (4),
    Ergaenzung zu 36.5). TB-111: …"""

    def __init__(self, meldung):
        print(meldung, file=sys.stderr)
        super().__init__(paths.RUECKGABEWERT_STARTPRUEFUNG)
        self.meldung = meldung
```

- **C1, Meldung gleich:** `c_proben.sh` erzeugt mit `beispieldaten.py` die Rohergebnisse für `turtle_soup_stocks` und leitet daraus vier Brüche ab. Es lief **vor** Block C (`c_proben_vorher.txt`). `c_nochmal.sh` lief **nach** Block C auf **denselben Eingaben** (`c_proben_nachher.txt`). Je Fall werden stderr und stdout mit `cmp` verglichen:

  | Fall | vorher | nachher | stderr | stdout |
  |---|---|---|---|---|
  | `--rohergebnisse <leer>` | rc 1 | **rc 2** | wortgleich (197 B) | gleich |
  | fehlende Spalte `mittlere_exposure` | rc 1 | **rc 2** | wortgleich (72 B) | gleich |
  | Zelle `ausserhalb=1` | rc 1 | **rc 2** | wortgleich (96 B) | gleich |
  | Benchmark mit 2 Tagen (weniger als drei gemeinsame) | rc 1 | **rc 2** | wortgleich (184 B) | gleich |
  | Basis ohne Bruch | rc 0 | rc 0 | leer | gleich |

- **C2:** Der Kommentar steht an der Klasse (siehe oben).
- **C3:** `test_ersatzwerte.py` Teil G, 6 neue Prüfungen:
  - G-a: `auswertung.py --rohergebnisse <leer>` über die Kommandozeile ⇒ rc 2;
  - G-b/G-c/G-d: Spalte, Zelle, Tage je als eigener Prozess in einer Kopie ⇒ rc 2, Meldung auf stderr;
  - G-M: Mutation „Code 1 zurück“ ⇒ rc 1, Gegenprobe rc 2.

  Umgestellte Tests: **keine** (A3).
- **C4:** `docs/belege/TB-106/g3_auswertung.sh`, alle neun Bots: **`fc1781067e73bd7d…` zeichengleich** (`c4_auswertung_beispieldaten.txt`).

**Sichtbare Nebenwirkung:** Die Meldung wird jetzt beim **Erzeugen** von `Abbruch` ausgegeben, nicht mehr erst beim Prozessende. Tests, die `Abbruch` im eigenen Prozess fangen (A9, A10 in `test_vorregistrierung.py`), zeigen deshalb zwei Meldungszeilen auf stderr (`c_tests.txt`); die Zählung bleibt 196/196. `str(e)` eines gefangenen `Abbruch` ist jetzt `"2"`, die Meldung steht in `e.meldung`. Kein Code im Repo liest `str(e)` eines `Abbruch` (grep, A3).

## 4. Block D: Abbild und Sonde (Commit `1dcf273`)

| | |
|---|---|
| D2 vorher | Sonde gegen das alte `40ffe18d…` **auf dem Code-Stand `6c98c38`, vor dem Ziehen**: `[1 BEFUND]` genau an Punkt **3, 5, 11, 12, 14** und in der Gruppe **`eingefroren`**. Abweichend sind `auswertung.py` (`a864b216…`) und `herkunft.py` (`5bbfc9e0…`). Pfad-Bestandteile 25: 19/6/0. **Kein anderer Punkt** (`d2_sonde_alt.txt`) |
| D1 | `sperrliste_abbild.py --ziel research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26.json` auf HEAD `6c98c38`, Arbeitsbaum ausserhalb `docs/` sauber. rc 0, **9192 B, `e655c1c8c8e576faa1de8021357354b1d9f0b44e9adae3a176c944087b3aacd9`**; 14 Punkte aus Register Z. 894–1007, 15 Pfadnennungen, Gruppen bestimmt 0, eingefroren 10 (`d1_abbild.txt`). Der Name war im Worktree, im Hauptordner und auf `origin/main` frei |
| D2 nachher | Sonde gegen das neue: Pfad-Bestandteile **25/0/0**, (ii) **0**, Listentext wie bei Erzeugung. rc 2 nur NICHT PRÜFBAR, wie vorher (`d2_sonde_neu.txt`) |
| D3 | Hash-Übergänge voll in `d3_hashes_register.txt`, siehe Abschnitt 6 |

## 5. Block E: Abnahme

| | Soll | gemessen | Beleg |
|---|---|---|---|
| E1 | Benchmark im Modus aus dem Worktree bytegleich `64fb2912…` | **`64fb2912f1a2ffb02a36834857fe9a91529b7517a8a7185f5fd7b11642f873b7`**, rc 0, 69 s (`g_lauf.sh` aus TB-106, mit Haken TB-104) | `e1_e3_laeufe.txt` |
| E2 | ohne Modus die 8 Ausgaben bytegleich gegen den Eingangsstand | vorher = lokaler **Klon auf `f4d6d6d`** im Scratchpad, nachher = Worktree. `fn`, `embargo`, `fsm`, `lesart`, `plan`, `sf`, `eft` **bytegleich**. `ut.json` trägt die absolute Wurzel (`DATA_DIR`, `logs/`/`results/` je Bot, 90 diff-Zeilen, alle nur das Pfadpräfix); nach Ersetzen der Wurzel **bytegleich** (`c933b011…`) | `e2_ausgaben.txt`, `e2_ut_vergleich.py` |
| E3 | Trockenlauf aller neun im Modus | **9 × rc 0** | `e1_e3_laeufe.txt` |
| E4 | Tests | `test_vorregistrierung` **196/196** (959 s), `test_ersatzwerte` **61/61** (40 + F 15 + G 6), `test_paths` **35/35**, `test_startpruefungen` **44/44**, dazu `test_sperrlistensonde` 59/59 und `test_snapshot` 164/164. Nach Block B zusätzlich `test_abrufschutz` 77/77 und `test_stille_ausfaelle` 27/27 (beide laden `herkunft.py`) | `b_tests.txt`, `c_tests.txt`, `e4_tests.txt` |
| E5 | nur die freigegebenen Dateien geändert | `5_alle_vorher` gegen `5_alle_nachher` (1538 ⇒ 1539 Dateien): genau `herkunft.py`, `auswertung.py`, `test_ersatzwerte.py` und das neue Abbild. Snapshot-Summenhash und `--pruefen` Soll = Ist, Datenstand `d9449faf…`/223 gleich, 0 `*.db` im Worktree. `herkunft_protokoll.jsonl` **existiert nicht**, auch nach allen Tests nicht; `git status --ignored` ausserhalb `docs/` leer | `e5_hashes_nachher.txt`, `e4_tests.txt` |

## 6. Für Fable

- **A2:** Kein Test setzt `TB30A_BASE_DIR` zusammen mit dem Modus; kein Test musste angepasst werden. ⚠️ Nicht erwartet war A2b: Die Modus-Abfrage in `herkunft.py` las über `_paths()` unter der Ersatzwurzel (rc 1 statt 2).
- **A3:** 12 Stellen. Kein Test erwartete rc 1 von `auswertung.py`.
- **Die Wahl in B2:** Prüffunktion am Anfang von `commit()`, `register()` und `block()`; `_paths()` aus der eigenen Wurzel (Begründung in Abschnitt 2). Ohne diese zweite Änderung wäre B2 nicht erfüllbar gewesen.
- **C1:** Die Meldung ist vor und nach der Änderung wortgleich, an vier Fällen mit `cmp` gemessen. Neu ist nur der Zeitpunkt der Ausgabe (beim Erzeugen).
- **Hash-Übergänge (voll):**
  - `herkunft.py` `351f24c2d6a3a512dc1eb1a80b536b99d47c266db38f7dd93b9d1c0199397eef` ⇒ **`5bbfc9e085d7ec70f43eb8aaaf63b957de27e3647023e143d17e9dd8c60448fa`**
  - `auswertung.py` `83c6bc3c9b683d0bfd9d8c445492060f93759a551d0dcf329b2bd21b0f1cc5a1` ⇒ **`a864b2168a19405d5f1516a17146f78ef44bbca6f4f8d242c9ccb25f937467f3`**
  - `register()` `c85dd6c3b6de7a302627f84244226b9ba1ad5e22d6a8cc260cc5c48b588c12e2` ⇒ **`e7d82547bc6bddba77e9b668922953ecd10fc213567ef28d3e6d4f6e37838fc3`**. Von den 11 Teilen hat sich nur `auswertung.py` geändert; `herkunft.py` steht nicht in `EINGEFROREN`.
- **Abbild:** `sperrliste_abbild_2026-09-26.json` `e655c1c8…`, gezogen auf `6c98c38`.
- **Sonde:** Gegen das alte Abbild Befund genau an 3/5/11/12/14 und `eingefroren`; gegen das neue 25/0/0, (ii) 0.

**Offene Punkte, als Frage:**
1. **`datenstand(None)` im Modus** liest weiter `BASE_DIR/data`, mit oder ohne TB30A. Ich habe das wegen B3 (zeichengleich) nicht geändert. Die Aufrufer im Betrieb übergeben einen Pfad, und `block()` verlangt ihn im Modus. Soll `datenstand()` bei der nächsten Öffnung im Modus ohne Pfad ebenfalls mit 2 enden?
2. **Veralteter Satz im Docstring von `auswertung._abbruch_2`:** „(`Abbruch` oben endet mit 1 und bleibt, wie er ist.)“ ist seit Block C falsch. Die Freigabe lautete „Sonst nichts“, deshalb habe ich ihn **nicht** geändert. Soll er mit der nächsten Öffnung von `auswertung.py` gestrichen werden, oder als Tatsachennotiz stehen bleiben?
3. **`str(e)` eines gefangenen `Abbruch`** ist jetzt `"2"`, die Meldung steht in `e.meldung`. Heute liest niemand `str(e)`. Reicht das als Tatsachennotiz?

## 7. Für die Zusammenführung

- **Geändert auf `tb-111` gegenüber `f4d6d6d`:**
  - `research/vorregistrierung/herkunft.py`
  - `research/vorregistrierung/auswertung.py`
  - `research/vorregistrierung/test_ersatzwerte.py`
  - `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26.json` (neu)
  - `docs/belege/TB-111/` (neu) und dieses Dokument (neu)
- **Erwartete Konflikte mit `main`: keine.** `main` hat seit `f4d6d6d` sieben Commits (TB-109, TB-110) mit 82 Dateien; die Schnittmenge mit den Dateien oben ist **leer**. `git merge-tree --write-tree origin/main tb-111` endet mit rc 0 (gemessen um ca. 08:00 gegen `origin/main` = `6a7996a`).
  - ⚠️ TB-112 läuft parallel im Hauptordner. Vor dem Zusammenführen die Schnittmenge neu messen, besonders den Namen des Abbilds: Ein zweites `sperrliste_abbild_2026-09-26.json` auf `main` wäre ein Konflikt (add/add).
- **Nach dem Zusammenführen messen:**
  - `register()` wird **weder** `e7d82547…` noch `c92900a8…` (main) sein, weil sich Register und `auswertung.py` zugleich ändern. Neu messen.
  - Die Sonde gegen `e655c1c8…` auf dem zusammengeführten Baum laufen lassen. Das Abbild nennt Register-Z. 894–1007, auf `main` stehen die Punkte seit TB-110 in Z. 901–1014. TB-110 hat gezeigt, dass (ii) den Listentext vergleicht, nicht die Zeilen. Trotzdem nachmessen.
  - Im Register stehen seit TB-110 Einträge, die nach dem Zusammenführen überholt sind: 43-1 („heute rc 1“) und 43-4 (zweite Öffnung `herkunft.py` „geplant“). Dazu gehören Tatsachennotizen mit den Hash-Übergängen aus Abschnitt 6. Das Register ist hier nicht freigegeben und nicht angefasst.
- **Journalblock:** steht unten und wird beim Zusammenführen in `docs/projektfuehrung/JOURNAL.md` übertragen. Die Blockkennung vergibt die übertragende Sitzung: Der letzte Block auf `main` ist `DI`, und TB-112 kann `DJ` belegen.

## 8. In einfacher Sprache

Diese Sitzung hat in einer eigenen Kopie des Projekts gearbeitet, neben dem Hauptordner. Sie hat genau zwei geschützte Programme an genau den erlaubten Stellen geändert.

- **Das Herkunftsprogramm** zeigt seine Prüfansicht jetzt auch im geschützten Modus und rechnet dort mit den eingefrorenen Kursdaten. Setzt jemand im geschützten Modus die alte Test-Abkürzung, hört es sofort mit dem Wert 2 auf, **bevor** es irgendetwas liest. Ein Aufpasser-Programm hat das nachgeprüft. Dabei kam ein kleiner Fehler ans Licht: Schon die Frage „bin ich im geschützten Modus?“ hat bisher am falschen Ort nachgesehen. Auch das ist behoben.
- **Die Auswertung** meldet „konnte nicht rechnen“ jetzt mit dem Wert 2 statt 1. Der Meldungstext ist Zeichen für Zeichen derselbe.

Danach wurde das Schutzabbild neu gezogen. Die Vergleichstabelle ist Byte für Byte gleich geblieben, alle Tests sind grün. Zusammengeführt wird später in einem eigenen Schritt; dabei sind keine Konflikte zu erwarten.

---

## Journalblock zum Übertragen (nicht in `JOURNAL.md` eingetragen)

```markdown
## D? — TB-111: die gesperrte Öffnung aus Fable 25d — `herkunft.py` Prüfansicht im Modus (Snapshot `d9449faf…`) und `TB30A_BASE_DIR` im Modus rc 2 vor dem Lesen; `auswertung.Abbruch` endet mit 2, Meldung wortgleich; Abbild `e655c1c8…`; Benchmark im Modus bytegleich (26.09.2026)

*Quelle: `docs/ERGEBNIS_TB-111_herkunft_auswertung_oeffnung.md`*

**Quelle:** Mac-Sitzung **TB-111** (Sitzung B, parallel zu TB-109/TB-110 und TB-112), 26.09.2026, im Worktree
`~/trading-bot-tb111` auf Zweig `tb-111`, Eingang `f4d6d6d`. Commits `6cacfa4` (Block B), `6c98c38` (Block C),
`1dcf273` (Abbild) und der Abgabe-Commit. Belege `docs/belege/TB-111/`. Grundlage Fable 25d (2)–(4), 25c 2 (a),
Register 37.3. Freigabe 25.09.2026, 23:14 (zwei Auswahlkarten).

### Was gemessen und getan ist

| | |
|---|---|
| **0/A** | Worktree sauber, Hashes wie erwartet, Sonde 25/0/0. Kein Test setzt TB30A zusammen mit dem Modus; kein Test erwartet rc 1 von `auswertung.py`; 12 `raise Abbruch(`. ⚠️ `_paths()` lud `paths.py` aus `BASE_DIR/shared`: Modus + Ersatzwurzel endete deshalb mit rc 1 statt 2 |
| ⭐⭐ **B** | Prüfansicht übergibt im Modus `paths.DATA_DIR` (rc 0, `d9449faf…`/223). `_ersatzwurzel_pruefen()` am Anfang von `commit()`/`register()`/`block()`: Modus + TB30A ⇒ rc 2, Lesehaken 0 Zugriffe; `_paths()` aus der eigenen Wurzel. `test_ersatzwerte` Teil F 15 Prüfungen, drei Mutationen mit Gegenprobe |
| ⭐⭐ **C** | `Abbruch` ⇒ rc 2, Meldung wortgleich (4 Fälle mit `cmp`), 12 Stellen zeichengleich, Beispieldaten `fc178106…`; Teil G 6 Prüfungen; kein Test umgestellt |
| **D/E** | Abbild `e655c1c8…`; Sonde gegen alt Befund genau 3/5/11/12/14 + `eingefroren`, gegen neu 25/0/0; `register()` `c85dd6c3` ⇒ `e7d82547`. Benchmark im Modus `64fb2912…`, ohne Modus 8/8 (ut.json bis auf die Wurzel), Trockenlauf 9 × rc 0, `test_vorregistrierung` 196/196, `test_ersatzwerte` 61/61, `test_paths` 35/35, `test_startpruefungen` 44/44; Protokoll nicht angelegt |

### Was aus dieser Sitzung an Regeln bleibt

| | Regel |
|---|---|
| ⭐ | **Eine Wache, die fragt „bin ich im Modus?“, darf die Antwort nicht dort holen, wovor sie schützt.** Die Modus-Abfrage in `herkunft.py` lud `paths.py` aus der Ersatzwurzel. Das ist erst mit einem Lesehaken und einer nicht existierenden Ersatzwurzel aufgefallen, nicht mit der echten Wurzel als Ersatz |
| ⭐ | **„Wortgleich“ misst man auf denselben Eingaben, vorher und nachher, mit `cmp`**, nicht an zwei verschiedenen Scratch-Ordnern: der Pfad steht in der Meldung |

### Was offen bleibt

- Zusammenführen `tb-111` ⇒ `main` (eigener Auftrag): danach `register()` und Sonde neu messen, Tatsachennotizen zu 43-1/43-4. Fragen an Fable: `datenstand(None)` im Modus; veralteter Satz im Docstring von `_abbruch_2`; `str(e)` eines `Abbruch` ist jetzt `"2"`.

*Geschrieben 26.09.2026 von der Mac-Sitzung TB-111 im Worktree. Quellenvermerk: siehe Kopf.*
```

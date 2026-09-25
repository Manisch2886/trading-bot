# TB-105: Ergebnis. Drei Rückfälle geschlossen, keine Schreibziele beim Import mehr. Regimewache 3 von 3, im Modus rc 2 statt 0, Klasse (iii) im Trockenlauf leer, Benchmark im Modus und ohne Modus bytegleich `64fb2912…`

**Sitzungstitel:** `TB-105` · **Stand:** 25.09.2026, ca. 13:30 · **Auftrag:**
`docs/auftraege/MAC_TB-105_rueckfaelle_und_schreibziele.md` · **Belege:** `docs/belege/TB-105/`
**Eingang:** `516badc`. Commits: `b83e6b9` (Schritt 0), `f524327` (Block B), `f65c344` (Block C+D),
`d48a195` (Block E) und der Abgabe-Commit (Belege F/G, dieses Dokument, Journalblock DD).
**Grundlage:** Fable 24b A2, 25a Abschnitt 3 (A) (iii) und Abschnitt 4; Register 11.1.
Freigabe des Betreibers 25.09.2026, 10:52 (drei Auswahlkarten, wörtlich im Auftrag).
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **A** | Vormessung bestätigt: `pruefe_einbau()` meldete 0 von 3. `t3_supertrend` rechnete ohne BTCUSDT still weiter (anderer Trade-Hash), `volatility_breakout_crypto` brach schon ab, aber ohne die Wache. 14 `exit()`-Stellen, alle in `__main__`. ⚠️ **`crontab -l` war in dieser Sitzung gesperrt.** A3 ist deshalb nur statisch gemessen, über die Importketten der dokumentierten Einstiegspunkte. Keine freigegebene Datei steht in Abschnitt 10, in `EINGEFROREN` oder im Abbild. Punkt 11 sperrt den Commit beim Lauf, nicht die Datei |
| ⭐ **B** | Die Wache steckt an allen drei Stellen, **`pruefe_einbau()` meldet 3 von 3.** Mit BTCUSDT sind die Trade-Listen-Hashes vorher und nachher gleich (alle 5 Stellen). Ohne BTCUSDT bricht jede Stelle mit `RegimefilterFehlt` ab. 21 Prüfungen, darunter 4 Mutationsproben, jede beisst allein |
| ⭐ **C** | An den 14 Stellen gilt unter dem Modus: Meldung auf stderr und **Rückgabe 2**. Ohne Modus bleibt es bei `print` + `exit()` mit rc 0. ⚠️ Die Hilfsfunktion in `strategy_paths` musste wieder raus. Die Cron-Wächter `kurven_lauf.py`/`determinismus_lauf.py` **ersetzen dieses Modul** durch ein Ersatzmodul (Abschnitt 5, Befund 1) |
| ⭐ **D** | `symbols_config.py` fällt unter dem Modus nicht mehr auf die Standardliste zurück (rc 2, die Meldung nennt den Fall). Ohne Modus ist alles unverändert, auch die falsche Meldung „nicht gefunden“ (gemessen, Probe D2) |
| ⭐ **E** | `manual_close.py` legt Ordner und Protokoll erst bei der ersten Zeile an. Das Format ist zeichengleich mit `b83e6b9`. `strategy_paths.py` und `bot_lauf.py` legen unter dem Modus keine Ordner an; ohne Modus unverändert |
| ⭐⭐ **F** | Trockenlauf aller neun im Modus, **im Repo und im frischen Klon: 9 × rc 0**. Liste = Universumsdatei, Mengen 18/18/20/20/20/147 × 4. Klasse (i) ausserhalb 0, (ii) die bekannten 5. **Klasse (iii) im Repo leer** (vorher 3 je Bot). Benchmark im Modus **bytegleich `64fb2912…`**, dabei kein `manuelle_eingriffe.log` mehr. Ohne Modus: 8/8 Ausgaben gleich, Benchmark `64fb2912…`. `test_vorregistrierung` 196/196 |
| **G** | Geändert sind nur die 18 freigegebenen Dateien, ihre Tests und `docs/`. Gesperrte Dateien, Datenstand `d9449faf…`, Snapshot und `ergebnisse/` sind gleich, 11 von 12 `*.db` ebenso. Die zwölfte ist die Datenbank der Binance-Brücke, geändert vom Cron um 12:05. Die Sonde gegen `cb4eb1b4…` ist vorher und nachher zeichengleich |

---

## 0. Schritt 0

| | |
|---|---|
| 0a | Vier Dateien des steuernden Chats committet (`b83e6b9`), wie im Auftrag erwartet |
| 0b | Keine `.git/*.lock`. HEAD am Eingang `516badc`. Datenstand `d9449faf…` (223). Snapshot `--pruefen`: Soll = Ist. Hashes aller freigegebenen und gesperrten Dateien, der Ergebnisdateien, je versionierter Datei (1529) und der 12 `*.db` stehen in `0_hashes_vorher.txt` (Skript `hashes.sh`). Die Sonde gegen `…_2026-09-25.json` gibt rc 2 nur für NICHT PRÜFBAR; Pfad-Bestandteile 25/0/0 (`0_sonde_vorher.txt`) |

## 1. Block A: Vormessung nachgemessen

| | Vormessung | gemessen | Beleg |
|---|---|---|---|
| A1 | 0/3 | **0/3.** t3 ohne BTCUSDT: `collect_all_trades` und `evaluate_combination_multi` rechnen weiter, mit anderem Hash als mit BTCUSDT. vbc bricht in `apply_btc_regime_filter` mit eigenem `SystemExit` ab | `b3_vorher.txt` |
| A2 | 14, alle `__main__` | 14, alle `__main__` (AST) | `a2_exit_stellen.txt` |
| A3 | nicht gemessen | ⚠️ **`crontab -l` vom Werkzeug abgelehnt**, auch in der K2a-Form. Ersatz sind statische Importketten der 24 Einstiegspunkte aus dem Übergabeprotokoll: `equity_simulation`/`multi_symbol_optimise` laufen nur über die Cron-Wächter `ergebniskurven` (3:50) und `determinismus` (4:10), per `runpy` im `__main__`, und über `quarterly_review` (Cron unbestätigt). Über `forward_test.py` laufen sie nicht. `symbols_config` und `strategy_paths` lädt jeder `forward_test.py` (Papierpfad), `manual_close` der Dashboard-Dienst und `warteauftraege_ausfuehren.py`. `bot_lauf.py` lädt kein Einstiegspunkt. **BTCUSDT liegt in `data/` und in `all_data` beider Bots**, Abbruchkriterium 4 greift also nicht | `a3_aufrufer.txt`, `a3_importketten.py` |
| A4 | nicht gemessen | Es gibt drei Schreibfunktionen (`protokolliere_erfolg`, `_ablehnung`, `_warteauftrag`). Sie laufen in zwei Prozessen: Dashboard-Dienst und Warteauftrags-Cron. Der Modus-Weg zur Datei ist nur der Import über `registerdaten.py:62` | `a4_manual_close.txt` |
| A5 | nicht gemessen | Im gemessenen Modus-Lauf schreibt kein Aufrufer unter `results/<bot>`/`logs/<bot>` (dort gab es nur `mkdir`). Schreiben tun die `__main__`-Blöcke (71 Stellen): Unter dem Modus brechen sie jetzt mit `FileNotFoundError` ab, wie gewollt | `a5_strategy_paths.txt`, `a5_schreiber.txt` |
| A6 | nicht gemessen | 0 Treffer (Pfad und Name) in Abschnitt 10, `EINGEFROREN` und Abbild. `herkunft.SPERRLISTE_DATEIEN` nennt `strategies/*/equity_simulation.py` und `multi_symbol_optimise.py`, aber **kein Code liest diese Liste**. Punkt 11 lautet: *„Commit-Hashes von Simulation, Erkennung, Optimierern und Auswertungsskript — `herkunft.py::register()` und der Repo-Commit“*. Er sperrt den Commit beim Lauf, keinen Datei-Hash heute. Deshalb keine Auswahlkarte | `a6_sperrliste.txt` |

## 2. Block B: die Regimewache (Register 11.1)

- `from regimewache import btc_daten` steht im Kopf aller drei Dateien. Der Aufruf lautet `btc_daten(all_data, bot=…, holen=…)`, bei vbc mit `aktiv=BTC_REGIME_FILTER_ENABLED`. `regimewache.py` ist unverändert.
- **B2:** `pruefe_einbau()` → `vollstaendig: True`, 3 eingebaut (`b2_pruefe_einbau.txt`).
- **B3:** Ohne Modus und mit BTCUSDT sind die Hashes der Trade-Listen (JSON, sortierte Schlüssel) vorher und nachher gleich: t3 `collect_all_trades` `87760a15…`, t3 `evaluate_combination_multi` `d3c28444…`, vbc `collect_all_trades` `6c8b39b2…`, vbc `apply_btc_regime_filter` `e6673003…`. Ohne BTCUSDT bricht jede Einbaustelle mit `RegimefilterFehlt` ab (`b3_vorher.txt`, `b3_nachher.txt`).
- **B4, Proben** `shared/test_regimewache_einbau.py` (21/21):
  - A je Stelle: BTCUSDT fehlt ⇒ Abbruch durch die Wache;
  - B je Stelle: BTCUSDT da ⇒ kein Abbruch;
  - C-Gegenprobe: die unveränderte Kopie bricht ab;
  - **M1** t3 `equity_simulation` Einbau zurück, **M2** t3 `multi_symbol_optimise` Einbau zurück, **M3** vbc alte eigene Abfrage, **M4** vbc stilles Überspringen. Jede Mutation macht Probe A rot, die andere Stelle derselben Kopie bleibt grün.
- ⚠️ `shared/test_drawdown_beide_masse.py` angepasst (Test von `multi_symbol_optimise`). Seine Probedaten liessen BTCUSDT **absichtlich weg**, damit t3 den Filter still übersprang. Jetzt neutralisiert `stub_setzen()` Wache, Regime und Filter ausdrücklich, und `stub_loesen()` stellt sie vor Abschnitt 5 wieder her. t3 und vbc sind vorher und nachher gleich (21 OK, die 4 FEHLER in Abschnitt 5 gab es schon vorher; der Test ist seit TB-34 dauerhaft rot). Beleg `b_tests.txt`.

## 3. Block C und D: kein Rückfall unter dem Modus

- **C:** So sieht jede der 14 Stellen aus:
  ```python
  if not all_data:
      import paths
      if paths.selektionsmodus() is not None:
          sys.stderr.write(<dieselbe Meldung> + "\n")
          raise SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)
      print(<Meldung>)      # unverändert
      exit()                # unverändert
  ```
  Proben in `shared/test_rueckfaelle_modus.py` Teil C, im Wegwerfbaum (git-Repo) gegen eine Snapshot-Attrappe ohne Kursdateien:
  - **C1** je Datei: Modus ⇒ rc 2, Meldung auf stderr;
  - **C2** je Datei: ohne Modus ⇒ rc 0, Meldung auf stdout;
  - **C3** Mutation „Modus-Abfrage weg“ ⇒ rc 0 (rot), mit Gegenprobe.
- **D:** Unter dem Modus endet `load_symbols()` mit `SystemExit(2)`, wenn die Datei fehlt oder nach `EXCLUDE_SYMBOLS` leer ist. Das greift, **bevor** `DEFAULT_SYMBOLS` greift. Proben:
  - **D1** nur ausgeschlossene Symbole ⇒ rc 2, keine Standardliste;
  - **D2** ohne Modus ⇒ Standardliste und die Meldung „nicht gefunden“ wie bisher;
  - **D3** Gegenprobe: Modus mit echter Liste ⇒ rc 0, Liste = Datei;
  - **D4** Mutation „Modus-Zweig weg“ ⇒ rot.
- `research/tb27_kapitalsimulation/vergleich.py --pruefen` (Cron 4:40) bleibt rc 0: Die neun `__main__`-Blöcke haben sich gleichartig geändert, die Gruppen bleiben, wie sie waren.

## 4. Block E: Schreibziele beim Import

- **E1** `notifications/manual_close.py`: Neu ist `_protokoll_bereit()`. Nur wenn kein Handler hängt, legt es `PROTOKOLL_DIR` und den `RotatingFileHandler` an; die drei Schreibfunktionen rufen es. Proben in `notifications/test_manual_close_protokoll.py` (12/12):
  - **P1** Import allein: kein `mkdir`, kein `open` zum Schreiben (Audit-Haken);
  - **P2** eine Zeile: Datei entsteht, Zeile ohne Zeitstempel zeichengleich mit der Fassung `b83e6b9`;
  - **P3** zwei Zeilen: ein Handler, zwei Zeilen;
  - **M1** Mutation „Anlage beim Import“ ⇒ P1 rot, mit Gegenprobe;
  - **B1** die alte Fassung ist in P1 rot.

  `test_manual_close` und `test_dashboard` (784/784) sind grün.
- **E2** `shared/strategy_paths.py`: Unter dem Modus gibt es kein `makedirs`; die Pfade werden weiter zurückgegeben. Gefragt wird über `_im_selektionsmodus()` (Abschnitt 5, Befund 2). `test_paths` 35/35 (Probe A: 99 Pfade, 0 Unterschiede), `test_strategy_paths` 23/23.
- **E3** `research/exposure_messung/bot_lauf.py`: dasselbe für `daten/`.
- **E4** Proben in `test_rueckfaelle_modus.py` Teil E:
  - **E2** Modus ⇒ 0 angelegte Ordner im Baum;
  - **E3** ohne Modus ⇒ `results/<bot>`, `logs/<bot>`, `research/exposure_messung/daten`;
  - **E4**/**E5** je eine Mutation (`strategy_paths.py`, `bot_lauf.py`), jede allein, die andere Stelle bleibt stumm;
  - **E6** Gegenprobe.

  Im frischen Klon: siehe F1.

## 5. Für Fable (ohne Kontext lesbar) ⭐⭐

**Stand.** Register 11.1 ist erfüllt. Die Regimewache steht an allen drei Stellen aus `EINBAUSTELLEN`, und `pruefe_einbau()` meldet 3 von 3. Belegt ist das nicht nur am Quelltext, sondern am Verhalten: Jede Stelle bricht ohne BTCUSDT ab (`test_regimewache_einbau` A), rechnet mit BTCUSDT unverändert (Hash-Gleichheit B3), und vier Mutationsproben beissen je allein.

Rückfall (c) ist geschlossen: Die 14 `__main__`-Stellen geben unter dem Modus rc 2 (`test_rueckfaelle_modus` C1/C3). Rückfall (a) ist geschlossen: `symbols_config` gibt unter dem Modus rc 2, auch bei fehlender Datei (D1/D4).

**Klasse (iii) nach E:** im Trockenlauf aller neun **leer**, im Repo und im frischen Klon. Im Klon gibt es nur Bytecode-Cache-Ordner unter `~/Library/Caches/com.apple.python/<klon>/…`; die legt die macOS-Python-Installation beim ersten Import an, ausserhalb des Repos. Im Benchmark bleiben nur die 10 `$TMPDIR/tb40_lauf_*`-Ablagen (deine offene Frage aus 25b); `logs/notifications/` und `manuelle_eingriffe.log` sind weg.

**Was bleibt für TB-106:** Rückfall (d). Die Stellen am neuen Stand sind unverändert gegenüber `docs/belege/TB-104/d3_vier_rueckfaelle.txt` Rang 3, weil die drei Dateien seit `f334a7b` nicht geändert sind:
- `faltenplan.py:152-153` und `:159-160`;
- `benchmark.py:206-207`, `:221-222` und `:302`;
- `auswertung.py:284/286`, `:333-334 + 380-385` und `:500-521`.

**Zwei Befunde beim Bau, die über TB-105 hinaus gelten:**

1. ⭐ **`strategy_paths` ist in drei Werkzeugen ein Ersatzmodul.** `shared/kurven_lauf.py:118` und `shared/determinismus_lauf.py:151` (Cron 3:50/4:10) sowie `research/zuteilungskaskade/messung_primaerschluessel.py:110` setzen ein `types.ModuleType("strategy_paths")` in `sys.modules`, das nur `get_strategy_paths` kennt. **Jeder neue Name, den eine Bot-Datei aus `strategy_paths` importiert, bricht diese Wächter.** Die erste Fassung von C tat genau das, und `test_ergebniskurven` zeigte 17/32. Die Abfrage steht deshalb an jeder Stelle selbst und fragt `paths`.
2. `shared/strategy_paths.py` fragt `getattr(paths, "selektionsmodus", None)`. Zwei Proben setzen absichtlich ein `paths` ohne diese Funktion ein: `test_paths` Probe A mit der Fassung TB-52 und `test_strategy_paths` C4 mit einem nachgebauten Resolver. Für sie bleibt es beim Verhalten vor TB-105, also Anlage. Das echte `paths.py` führt die Funktion; dass es das echte ist, sichert `_resolver_ist_nachbar()` zu.

**Fragen:**

1. Ist die Bauart „Modus-Abfrage je Stelle, vier Zeilen“ in C für dich in Ordnung? Der Auftrag erlaubte „je Stelle zwei Zeilen“. Die Alternative wäre, die Ersatzmodule in `kurven_lauf.py`/`determinismus_lauf.py` zu ändern; diese Dateien sind nicht freigegeben.
2. Ist die Duldung in Befund 2 ein Rückfall im Sinn von 24b A2? Sie greift nur, wenn der Resolver die Funktion nicht hat, also nie beim echten `paths.py`.
3. Die Bytecode-Cache-Ordner der Apple-Python (`~/Library/Caches/com.apple.python/…`): Zählen sie als Klasse (ii) oder als Schreibziel?
4. A3 ist nur statisch gemessen, weil `crontab -l` gesperrt war. Soll der Betreiber `crontab -l | grep -c equity_simulation` (usw.) einmal von Hand nachliefern?

## 6. Block F: Abnahme

| | Soll | Ist | Beleg |
|---|---|---|---|
| F1 | 9 × rc 0, zweimal | **9 × rc 0 im Repo, 9 × rc 0 im frischen Klon** (`git clone`, HEAD `d48a195`) | `f1_trockenlauf.txt` |
| F1 | Liste = Universumsdatei | 9/9 ja, keine Standardliste | dto. |
| F1 | Mengen 18/18/20/20/20/147 × 4 | 18/18/20/20/20/147/147/147/147, in beiden Läufen | dto. |
| F1 | Klasse (i) ausserhalb 0 | 0 bei 18/18 Läufen | `f1_klassen_repo.txt`, `f1_klassen_klon.txt` |
| F1 | Klasse (ii) die bekannten 5 | `/dev/null`, `/dev/urandom`, `SystemVersion.plist`, `requirements.lock`, `zoneinfo/UTC`, bei 18/18 | dto. |
| F1 | ⭐ Klasse (iii) leer | **Repo: 0 bei 9/9** (TB-104: 3 je Bot). Klon: im Repo 0, das Listing vorher = nachher, `git status --porcelain --ignored` leer. Ausserhalb nur Apple-Bytecode-Cache (Frage 3) | dto. |
| F2 | Modus, bytegleich `64fb2912…` | **`64fb2912…`**, rc 0, 58 s. Klasse (iii) 20 statt 22: **kein** `logs/notifications`, **kein** `manuelle_eingriffe.log`; übrig nur `$TMPDIR/tb40_lauf_*`. Klasse (i) ausserhalb dieselben 21 wie TB-104 | `f2_benchmark.txt`, `f2_klassen_benchmark.txt` |
| F3 | ohne Modus 8 Ausgaben bytegleich | 7/8 hashgleich. `ut.json` unterscheidet sich nur in den **Wurzelpfaden** des Vorher-Worktrees, nach Angleichung 0 Unterschiede. Der Nachher-Hash `2546cadf…` ist zeichengleich mit TB-104 | `f3_ohne_modus.txt` |
| F3 | Benchmark ohne Modus `64fb2912…` | **`64fb2912…`**, rc 0 | dto. |
| F4 | Tests | `test_paths` 35/35, `test_strategy_paths` 23/23, `test_stille_ausfaelle` 27/27, `test_startpruefungen` 44/44, **`test_vorregistrierung` 196/196**. Neu: `test_regimewache_einbau` 21/21, `test_rueckfaelle_modus` 48/48, `test_manual_close_protokoll` 12/12 | `f4_tests.txt`, `cde_tests.txt`, `b_tests.txt` |

**Namen der neuen Proben:**
- `shared/test_regimewache_einbau.py`: A0, A0b, A/B je Stelle, C-Gegenprobe, M1–M4.
- `shared/test_rueckfaelle_modus.py`: C0–C3, D1–D4, E1–E6.
- `notifications/test_manual_close_protokoll.py`: P1, P1b, P2–P2d, P3, P3b, M1, B1.

## 7. Abweichungen vom Auftrag

| | |
|---|---|
| 1 | **A3 nur statisch:** `crontab -l` vom Werkzeug abgelehnt (auch gefiltert). Statt der Crontab zählen die im Übergabeprotokoll dokumentierten Einstiegspunkte |
| 2 | **C ohne Hilfsfunktion:** Die erlaubte Hilfsfunktion in `strategy_paths.py` scheiterte an den Ersatzmodulen der Cron-Wächter (Abschnitt 5, Befund 1). Jetzt stehen je Stelle vier Zeilen statt zwei |
| 3 | `shared/test_drawdown_beide_masse.py` geändert. Als Test von `multi_symbol_optimise` fällt er unter die Freigabe „die Tests dieser Module“; ohne die Änderung wäre er für t3 an der Wache abgebrochen |
| 4 | D greift unter dem Modus auch bei **fehlender** Datei, nicht nur bei „leer nach Ausschluss“ (24b A2: „gleich welcher Art“). Der Resolver fängt die fehlende Datei heute schon vorher ab |
| 5 | F2 lief nur im echten Repo (der Auftrag verlangt „zweimal“ nur für F1). F3 „vorher“ lief in einem `git worktree` von `b83e6b9`, der danach entfernt wurde |
| 6 | Der Gesamtlauf von `test_drawdown_beide_masse.py` (alle neun Bots, > 20 min allein für `elliott_wave`) wurde abgebrochen. Verglichen sind die beiden geänderten Bots einzeln, vorher gegen nachher |

## 8. Was NICHT geschah

- Nicht angefasst: `regimewache.py`, `paths.py`, `ladeprotokoll.py`, alles unter `research/vorregistrierung/` und `research/universum_trockenlauf/`, alle `forward_test.py` und `live_params.py`, die Crontab, das Register.
- Rückfall (d) ist nicht angefasst (TB-106).
- Kein neues Abbild. Keine Tabelle im Repo neu geschrieben. `python3 faltenplan.py` lief nie.

## 9. Für die Folgesitzung vorbereitet (TB-106)

- **Die Stellen von (d)** stehen in Abschnitt 5, am Stand `d48a195` nachgesehen: Die drei Dateien sind seit `f334a7b` unverändert, `d3_vier_rueckfaelle.txt` Rang 3 gilt Zeile für Zeile. Alle drei Dateien stehen in `EINGEFROREN` und im Abbild, daher braucht es ein neues Abbild (Auftrag TB-106).
- **Beachten:** Die Bauart „Abfrage an der Stelle, über `paths`“ aus C ist auf (d) übertragbar. Ein neuer Import aus `strategy_paths` ist es nicht (Befund 1).
- **Wiederverwendbar:**
  - `docs/belege/TB-105/f_lauf.sh`: Bot oder Benchmark im Modus, aus jeder Wurzel, auch aus einem Klon;
  - `f3_ausgaben.sh`: die 8 Ausgaben ohne Modus;
  - `hashes.sh`: mit Einzelhashes je Datei statt Summenhash, `diff`-bar;
  - `b3_trades.py`: Trade-Listen-Hashes;
  - `a3_importketten.py`: statische Importketten;
  - die Wegwerfbaum-Bauart in `shared/test_rueckfaelle_modus.py` (git-Repo, Attrappe ohne Kursdateien).

---

## In einfacher Sprache

Drei Notlösungen sind zu. Dem T3-Bot fehlte manchmal der Bitcoin-Kurs für seinen Marktfilter. Dann rechnete er still ohne Filter weiter und war damit ein anderer Bot. Jetzt bricht er in diesem Fall ab. Programme, die keine Daten finden, melden im geschützten Modus jetzt einen Fehler statt „fertig“. Eine leere Symbolliste wird dort nicht mehr still durch eine Notliste ersetzt.

Ausserdem legt ein geschützter Lauf beim Laden keine Ordner und keine Protokolldatei mehr im Projekt an. Die Protokolldatei für manuelle Eingriffe entsteht jetzt erst, wenn wirklich etwas protokolliert wird.

Im normalen Betrieb hat sich an keiner Zahl etwas geändert: Trades, Vergleichstabelle und die acht Prüfausgaben sind Byte für Byte gleich. Alle neun Bots laufen im geschützten Modus fehlerfrei, im Projekt und in einer frischen Kopie. Die Vergleichstabelle kommt dort Byte für Byte gleich heraus.

Unterwegs zeigte sich: Zwei nächtliche Prüfprogramme tauschen ein Hilfsmodul gegen einen eigenen Ersatz aus. Neue Funktionen dürfen deshalb nicht über dieses Modul laufen. Die Umsetzung wurde entsprechend angepasst.

# TB-107: Ergebnis. Die vier Notlösungen in den nicht gesperrten Hilfsprogrammen sind geschlossen: `_min_history` genau ein Treffer, zweite Kopie in `faltenplan_neun.py` rc 2, kein `getattr` mehr in `strategy_paths.py`, `tb40_lauf_*` werden entfernt. Laufbereich 81 Module, Gegenprobe über alle `__main__`-Stellen ohne Fund; Benchmark im Modus (Repo und Klon) und ohne Modus bytegleich `64fb2912…`

**Sitzungstitel:** `TB-107` · **Stand:** 25.09.2026, ca. 22:15 · **Auftrag:**
`docs/auftraege/MAC_TB-107_nicht_gesperrte_rueckfaelle.md` · **Belege:** `docs/belege/TB-107/`
**Eingang:** `f22f91e`. Commits: `404c7e4` (Schritt 0), `33d50f2` (Block B), `f5fdb53` (Block C, eigener Commit),
`5cfe472` (Block D), `a79e715` (Block E), `9827a3e` (Block F) und der Abgabe-Commit (Belege, dieses Dokument, Journalblock DF).
**Grundlage:** Fable 25b 3 (1) und (5), 25c 4 (2), 4 (3)(a)/(b); Ergebnis TB-106 Befund 1.
Freigabe des Betreibers 25.09.2026, 18:09 (Schnitt) und 20:27 (zwei Auswahlkarten, wörtlich im Auftrag).
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **A** | Vormessung bestätigt. A1: 9/9 Bot-Dateien genau ein Treffer. **A2: `elliott_wave` trägt heute `MIN_HISTORY_HOURS`** (Abbruchkriterium 3 greift nicht). A4: die Kopie in `faltenplan_neun.py` wird mit der echten Eingabe **nicht** erreicht, auch nicht über ihr `basis`-Argument. A5/A6 Zeilen wie vorgemessen. A8: kein Aufrufer im Regelbetrieb außer `strategy_paths.py` (alle Bots) |
| ⭐ **B** | `faltenschranke_messung.py`: `_min_history()` mit `re.findall`, genau ein Treffer, sonst rc 2 (Meldung nennt Datei und Trefferzahl); `kerzen_elliott_wave()` ohne `MIN_HISTORY_HOURS` ⇒ rc 2 statt stillem Hinweis. Der `TypeError`-Pfad in `loader_lesart()` ist damit unerreichbar (belegt, nicht umgebaut). `fsm.json`, `lesart.json` bytegleich |
| **C** | `faltenplan_neun.py` (eigener Commit `f5fdb53`): `volle_jahre()` ohne inneres Jahr und `faltenlaenge()` bei leerer Zählung ⇒ rc 2. `fn.json`, `eft.json` bytegleich; 156/156, 50/50, 61/61 |
| ⭐⭐ **D** | `strategy_paths.py` (Live-Code): `_im_selektionsmodus()` ruft `paths.selektionsmodus()` direkt. **Ohne Modus: 101 Aufrufer in 9 Bots, Pfade und angelegte Ordner vorher = nachher.** `test_paths` A weiter 99 Pfade/0 Unterschiede; neue Probe G. `test_ergebniskurven` 44/44 (Cron-Wächter unberührt) |
| ⭐ **E** | `universum_trockenlauf.messe_bot()` entfernt `tb40_lauf_*`, nachdem das Ergebnis gelesen ist; ohne Ergebnis bleibt der Ordner, und sein Pfad steht in der Meldung. `ut.json`, `sf.json` bytegleich; Zahl der `tb40_lauf_*` in `$TMPDIR` in jedem Lauf dieser Sitzung vorher = nachher (4765) |
| ⭐⭐ **F** | Laufbereich am Endstand: **81 Module**, gegenüber den 80 von TB-104 neu **nur `shared/regimewache.py`**. Gegenprobe `shared/test_main_gegenprobe.py` (AST, Liste aus der Messdatei): **14 Datenstellen, alle mit Abfrage, kein neuer Fund** (F4 greift nicht) |
| ⭐⭐ **G** | Benchmark im Modus **Repo und frischer Klon `64fb2912…`**, ohne Modus `64fb2912…`. **8/8 Ausgaben ohne Modus bytegleich** gegen `f22f91e`. Trockenlauf 9 × rc 0, Tabelle gleich TB-106. Sonde vorher = nachher, `register()` unverändert `0ece95e2…`. Tests siehe G4 |
| ⚠️ | **Nebenwirkung von D:** das eigenständige Werkzeug `research/resolver_selektion/pfadvergleich.py` (nicht freigegeben, unverändert) endet jetzt mit rc 1 statt 0. Es setzt die `paths.py` aus TB-52 ohne `selektionsmodus` ein. Die zwei Tests, die es importieren, sind grün. Frage 3 unten |

---

## 0. Schritt 0

| | |
|---|---|
| 0a | Drei Dateien des steuernden Chats committet (`404c7e4`); der Arbeitsbaum entsprach genau der Erwartung |
| 0b | Keine `.git/*.lock`. HEAD am Eingang `f22f91e` (= Soll). Datenstand `d9449faf…` (223), Snapshot `--pruefen` Soll = Ist. Einzelhashes aller freigegebenen und gesperrten Dateien, `ergebnisse/`, je versionierter Datei (1534) und der 12 `*.db` in `0_hashes_vorher.txt` (Skript `hashes.sh`). `register()` `0ece95e2…`. Sonde gegen `40ffe18d…`: Pfad-Bestandteile 25/0/0, rc 2 nur NICHT PRÜFBAR (`0_sonde_vorher.txt`). **`tb40_lauf_*` in `$TMPDIR` vorher: 4615** (nur gezählt) |
| Vorher-Lauf | `g2_ausgaben.sh` am Code-Stand `f22f91e`, bevor eine Datei geändert wurde (`g2_vorher.txt`): 8 × rc 0, Hashes gleich dem Nachher-Stand von TB-106. **Dieser eine Lauf der alten Fassung hinterließ 74 neue `tb40_lauf_*` (4615 ⇒ 4689)** – das ist der Befund, den E schließt |

## 1. Block A: Vormessung

Belege `a_vormessung.txt` (Skript `a_vormessung.py`), `a8_aufrufer.txt`. **Meine Messung weicht von der Vormessung nicht ab.**

| | Stelle | gemessen |
|---|---|---|
| A1 | `faltenschranke_messung.py:137-145` | `re.findall` mit demselben Muster: in allen 9 Bot-Dateien **genau ein** Treffer; `_min_history()` liefert je Bot denselben Namen |
| A2 | `strategies/elliott_wave/multi_symbol_optimise.py` | **`MIN_HISTORY_HOURS`** – der Hinweis war also nie der echte Pfad; B2 gebaut |
| A3 | `loader_lesart()` | `n = None` nur über `(None, None)` aus `_min_history()`; nach B unerreichbar (Probe `B-A3`) |
| A4 | `faltenplan_neun.py:363-380` | mit der echten Eingabe (`basis=None` ⇒ `BASE_DIR` = Repo) haben alle neun Bots innere Kalenderjahre, keine Zählung ist leer ⇒ **nicht erreicht**. `basis` kommt nur über `faltenplan(basis)` ⇒ `plan_fuer_bot(bot, basis)` ⇒ `faltenlaenge(bot, basis)`; kein Aufrufer im Repo übergibt ein `basis` außer den Tests (Ersatzwurzel, unter dem Modus rc 2 seit TB-104). `research/krypto_historie/faltenplan.py` hat ein eigenes `plan_fuer_bot` ohne diese Funktionen |
| A5 | `strategy_paths.py:112-123` | `getattr(paths, "selektionsmodus", None)` in Z. 122, genutzt von `test_paths` A und `test_strategy_paths` C4 – **und** vom eigenständigen `pfadvergleich.py` (siehe D) |
| A6 | `universum_trockenlauf.py:306` | `mkdtemp(prefix="tb40_lauf_")`; daneben zwei weitere Ablagen, **nicht** freigegeben und nicht geändert: `tb40_faltenplan_` (Z. 259, `hole_faltenplan()`) und `tb40_proben_` (Z. 671, Probeläufe `--stille-filter`) |
| A7 | 14 `__main__`-Stellen | gefunden per AST (F), alle mit Abfrage |
| A8 | Aufrufer im Regelbetrieb | statisch, `crontab -l` gesperrt. `faltenschranke_messung`, `faltenplan_neun`, `universum_trockenlauf`: **keiner** unter `system/ dashboard/ notifications/ broker/ strategies/ shared/`; Importeure sind `research/`-Werkzeuge und Tests. `strategy_paths`: 101 Dateien unter `strategies/` in allen 9 Bots (je `forward_test.py`), dazu `shared/` (u. a. `ergebniskurven.py`, `entscheidungskerze.py`); Ersatzmodule in `kurven_lauf.py`, `determinismus_lauf.py`, `messung_primaerschluessel.py` (TB-105 Befund 1) |

## 2. Block B: `faltenschranke_messung.py`

- **B1:** `_min_history()` mit `re.findall` (gleiches Muster, `re.M`); `len(treffer) != 1` ⇒ Meldung auf stderr mit Pfad, Trefferzahl und Namen, dann `SystemExit(fp.paths.RUECKGABEWERT_STARTPRUEFUNG)`. `paths` ist das Modul, das `faltenplan_neun` schon geladen hat (die Datei importiert `paths` nicht selbst; kein neuer Import, kein Name aus `strategy_paths`).
- **B2:** `kerzen_elliott_wave()`: Schranke nicht `MIN_HISTORY_HOURS` ⇒ rc 2. Die Ausgabe hat sich nicht geändert, weil der Hinweis-Zweig mit der echten Eingabe nie lief.
- **B3:** `loader_lesart()` unverändert; Probe `B-A3` zeigt rc 2 aus `_min_history()` statt `TypeError`, die Mutation `B-A3M` („`re.search` zurück“) führt wieder in den `TypeError` (rc 1).
- **B4 / Proben** `research/faltenplan_neun/test_min_history.py` **14/14** (1 s), Bot-Datei als Kopie im Wegwerfbaum über `TB36_BASE_DIR`: `B-0`, `B-0e`, `B-A1z` (zwei Treffer), `B-A1k` (kein Treffer), `B-A1zM`(+`-G`), `B-A1kM`(+`-G`), `B-A2`, `B-A2M`(+`-G`), `B-A3`, `B-A3M`(+`-G`).
- **Abnahme:** `fsm.json` `db72ca32…`, `lesart.json` `4bacd86f…` – bytegleich (`b_abnahme.txt`).

## 3. Block C: `faltenplan_neun.py`, die zweite Kopie (eigener Commit `f5fdb53`)

- **C1:** `_abbruch_2()` neu in der Datei (Bauart TB-106 B1, `paths` wie die Datei ihn schon importiert). `volle_jahre()` ohne inneres Jahr ⇒ rc 2; `faltenlaenge()` bei leerer Zählung ⇒ rc 2. Sonst nichts an der Datei.
- **C2:** `research/faltenplan_neun/test_volle_jahre.py` **7/7**: `C-A1`, `C-A1b`, `C-A1M`(+`-G`), `C-A2`, `C-A2M`(+`-G`). Wegwerfbaum mit Kopie und echter `shared/paths.py`.
- **Abnahme** (`c_abnahme.txt`): `fn.json` `93fbf09c…`, `eft.json` `1bf46797…` bytegleich; `test_faltenplan_neun` 156/156, `test_erste_falte_trockenlauf` 50/50, `test_horizontbeginn` 61/61.
- Sagt Fable zu 25d „nur Tatsachennotiz“: `git revert f5fdb53` nimmt Code und Probendatei gemeinsam zurück.

## 4. Block D: `shared/strategy_paths.py` (Live-Code)

- **D1:** `_im_selektionsmodus()` ist jetzt `return paths.selektionsmodus() is not None`. Fehlt die Funktion, bricht `get_strategy_paths()` mit `AttributeError` ab – nach der Nachbarprüfung, **vor** der Ordneranlage.
- **D2:** `test_paths` Probe A hängt an die Fassung TB-52 `def selektionsmodus(): return None` an: **99 Pfade, 0 Unterschiede**, Mutationsprobe A2 weiter 18. `test_strategy_paths` C4: der nachgebaute Resolver bekommt `paths.selektionsmodus = lambda: None`, C4 beißt weiter.
- **D3:** neue Probe G in `test_strategy_paths.py`: `G1` (ein `paths`, dem am Ende `selektionsmodus` entzogen ist ⇒ `AttributeError`, kein Pfad), `G2` (keine `results/<bot>`, `logs/<bot>`), `G3` Mutation „`getattr` zurück“ (Pfade kommen, beide Ordner angelegt) und `G3-G`.
- **Abnahme Live-Code** (`d_vergleich.txt`, Skript `d_vergleich.py`): `strategy_paths.py` aus `f5fdb53` gegen den neuen Stand, ohne Modus, je Aufrufer ein eigener Prozess in einem Wegwerfbaum mit der echten `paths.py`: **101 Aufrufer (alle Dateien unter `strategies/` mit `get_strategy_paths`, 9 Bots), alle 7 Schlüssel und die danach vorhandenen Verzeichnisse gleich, 0 Unterschiede, rc 0 vorher und nachher.** Tests (`d_tests.txt`): `test_paths` 35/35, `test_strategy_paths` **27/27** (23 + G1, G2, G3, G3-G), `test_ergebniskurven` 44/44, `test_rueckfaelle_modus` 48/48, `test_startpruefungen` 44/44.
- ⚠️ **Nebenwirkung** (`d_pfadvergleich.txt`): `research/resolver_selektion/pfadvergleich.py` eigenständig aufgerufen: am Stand `f22f91e` rc 0 („GRUEN“), jetzt **rc 1** mit `AttributeError: module 'paths' has no attribute 'selektionsmodus'`. Das Werkzeug legt die `paths.py` aus TB-52 neben die echte `strategy_paths.py`. Nicht freigegeben, nicht geändert. `test_paths` A und `test_startpruefungen` N4 importieren nur `vergleiche()` und sind grün (N4 nutzt `624853b`, das die Funktion schon führt). Frage 3.

## 5. Block E: `universum_trockenlauf.py`, die Zwischenablage

- **E1:** In `messe_bot()` `try: … return json.load(f) finally: shutil.rmtree(ordner)`. Ohne Ergebnis: `RuntimeError("Kindprozess … ohne Ergebnis (Rückgabe n), Ablage bleibt stehen: <ordner>…")`. `import shutil` steht **in** `messe_bot()` (freigegeben war nur die Funktion; die Datei importiert auch in `stichtage_der_falte()` lokal).
- **E2:** `research/universum_trockenlauf/test_zwischenablage.py` **4/4** (eigenes `TMPDIR` je Probe, Attrappe statt `loaderlauf.py`): `E-a`, `E-b`, `E-aM`(+`-G`).
- **Abnahme** (`e_abnahme.txt`): `ut.json` `2546cadf…`, `sf.json` `78e4f524…` bytegleich; `tb40_lauf_*` vor `ut` 4765, nach `ut` 4765, nach `sf` 4765; `test_universum_trockenlauf` 163/163.

## 6. Block F: Laufbereich und Gegenprobe

- **F1** (`f1_laufbereich_*.txt`, `f1_vereinigen.py`): gemessen am Code-Endstand `a79e715` (der Commit von F fügt nur die Testdatei hinzu) mit dem Werkzeug aus TB-104 D1 (`d1_listen.py`, Haken), dieselben drei Lauf-Typen im Modus: Trockenlauf aller neun (je rc 0), Benchmark (rc 0, `64fb2912…`), `auswertung.py`-Import (rc 0). **81 Module.** Unterschied zu den 80 von TB-104 (`f1_unterschied_tb104.txt`): **neu nur `shared/regimewache.py`** (Trockenlauf und Benchmark, eingebaut mit TB-105); keines weggefallen.
- **F2:** `shared/test_main_gegenprobe.py` liest die Liste aus `docs/belege/TB-107/f1_laufbereich_vereinigung.txt` (Einträge unter `docs/` sind Messumschläge und zählen nicht). Per AST je `__main__`-Block jedes `if`, dessen Rumpf mit `exit()`/`quit()`/`sys.exit()` endet und das bei fehlenden Daten greift (Leerprüfung eines Ergebnisses aus einem `load*`/`lade*`-Aufruf, oder „Keine Daten“ im Rumpf); verlangt wird `paths.selektionsmodus()` vor dem ersten Ausstieg. Tatsachenkommentar: die Liste wird am Tag-Commit durch die Tag-Messung ersetzt (Fable 25b (5)).
- **F3:** `F3a` Kopie von `strategies/elliott_wave/equity_simulation.py` ohne Abfrage ⇒ rot, `F3a-G` mit Abfrage ⇒ gezählt, kein Befund; `F3b` erfundene Datei „Keine Daten gefunden“ + `exit()` ⇒ rot, `F3b-G` mit Abfrage ⇒ gezählt. **7/7** (`f_gegenprobe.txt`).
- **F4:** am echten Stand **14 Datenstellen, alle mit Abfrage** – genau die 14 aus TB-105 C. Kein neuer Fund. Ausgewiesen, nicht gezählt: **10 Stellen `if trades.empty: … exit()`** in den `equity_simulation.py` (bei fehlenden **Trades**, nach einer Rechnung, kein Ladeaufruf; `volatility_breakout_crypto` zweimal). Frage 2.

## 7. Block G: Abnahme

| | Soll | Ist | Beleg |
|---|---|---|---|
| G1 | Modus, Repo und frischer Klon `64fb2912…` | **Repo `64fb2912…` rc 0 (62 s), Klon (`git clone`, HEAD `9827a3e`) `64fb2912…` rc 0 (61 s)**. Klasse (iii) außerhalb des Laufordners: Repo 20 = 10 `mkdir` + 10 `w` unter `$TMPDIR/tb40_lauf_*` – jetzt **Klasse (iv)**, nach dem Lauf entfernt (Zahl in `$TMPDIR` vor = nach dem Lauf, 4765); sonst nur `--ziel`. Klon: dieselben 20 + 16 `mkdir` im Apple-Bytecode-Cache (Klasse (ii), 25c 4 (4)(a)). Klon `git status --porcelain --ignored` vorher und nachher leer. Klasse (i): 225 im Snapshot, 31 außerhalb (TB-106: 21) – **die 10 zusätzlichen sind die Verzeichnis-Lesezugriffe von `shutil.rmtree` auf die eigenen `tb40_lauf_*`** (Aufrufstapel `universum_trockenlauf.py:334`); dazu wie vorher 9 TB-24-Listen, `messgroessen.json`, 10 Ergebnis-JSON der Ablage und die Tempfile-Probe von `mkdtemp` | `g1_benchmark.txt`, `g_klassen_bm_repo.txt`, `g_klassen_bm_klon.txt` |
| G2 | ohne Modus 8/8 gegen `f22f91e`, Benchmark `64fb2912…` | **8/8 bytegleich**, je rc 0; Benchmark ohne Modus **`64fb2912…`** | `g2_vorher.txt`, `g2_nachher.txt` |
| G3 | Trockenlauf 9 × rc 0, Mengen 16.1.1, (iii) 0 | **9 × rc 0**, Liste = Universumsdatei, keine Standardliste, Tabelle zeilengleich mit TB-106 G5; Klasse (i) außerhalb 0, **(iii) 0** bei 9/9 | `g3_trockenlauf.txt`, `g_klassen_bots.txt` |
| G4 | Tests | siehe unten | `g4_tests.txt` |
| G5 | Sonde vorher = nachher, `register()` `0ece95e2…` | **Sonde vorher = nachher** (Pfad-Bestandteile 25/0/0, rc 2 nur NICHT PRÜFBAR); `register()` **`0ece95e2…`** unverändert (`h1_hashes_nachher.txt` (9)) | `g5_sonde_nachher.txt` |

**G4 – Tests am Endstand `9827a3e`** (`g4_tests.txt`):

| Test | Ergebnis | Dauer |
|---|---|---|
| `test_faltenplan_neun` | **156/156** | 145 s |
| `test_erste_falte_trockenlauf` | 50/50 | 150 s |
| `test_horizontbeginn` | 61/61 | 61 s |
| `test_universum_trockenlauf` | **163/163** | 95 s |
| `test_paths` | **35/35** | 12 s |
| `test_strategy_paths` | **27/27** (23 + 4 neue) | 12 s |
| `test_rueckfaelle_modus` | 48/48 | 39 s |
| `test_ergebniskurven` | 44/44 | 31 s |
| `test_startpruefungen` | 44/44 | 14 s |
| `test_ersatzwerte` | **40/40** | 22 s |
| `test_vorregistrierung` | **196/196** | 926 s |
| neu `test_min_history` | 14/14 | 1 s |
| neu `test_volle_jahre` | 7/7 | 1 s |
| neu `test_zwischenablage` | 4/4 | 0 s |
| neu `test_main_gegenprobe` | 7/7 | 1 s |

Alle mit rc 0. `tb40_lauf_*` in `$TMPDIR` nach allen Tests: 4765, unverändert.

**Namen der neuen Proben:** `test_min_history.py` (B, 14), `test_volle_jahre.py` (C, 7), `test_strategy_paths.py` Probe G (`G1`, `G2`, `G3`, `G3-G`), `test_zwischenablage.py` (E, 4), `test_main_gegenprobe.py` (F, 7: `F0`, `F0b`, `F2`, `F3a`, `F3a-G`, `F3b`, `F3b-G`).

## 8. Block H: Hashes nachher

Siehe `h1_hashes_nachher.txt` und `h1_vergleich.txt` (Skript `hashes.sh`, Vergleich gegen 0b).

- **Geändert** sind nur:
  - die vier freigegebenen Dateien: `faltenschranke_messung.py`, `faltenplan_neun.py`, `strategy_paths.py`, `universum_trockenlauf.py`;
  - `test_paths.py`, `test_strategy_paths.py`;
  - die vier neuen Testdateien;
  - `docs/`.
- Versionierte Dateien außerhalb `docs/`: 1534 ⇒ 1538, das sind die vier neuen Tests.
- **Gleich** sind:
  - alle gesperrten und nicht freigegebenen Dateien (Abschnitt (2), darunter `research/vorregistrierung/*`, `paths.py`, `regimewache.py`, `loaderlauf.py`, die drei Cron-Wächter, alle `strategies/*/…`);
  - alle Dateien unter `ergebnisse/`;
  - der Snapshot (Summenhash, `--pruefen` Soll = Ist) und der Datenstand `d9449faf…` (223);
  - **alle 12 `*.db`** (in der Sitzungszeit schrieb kein Cron);
  - `register()` `0ece95e2…`.
- `herkunft_protokoll.jsonl` existiert vorher und nachher nicht.
- `tb40_lauf_*` in `$TMPDIR`: 4615 ⇒ 4765. Die 150 neuen stammen **alle** aus Läufen der alten Fassung **vor** dem Commit von E:
  - der Vorher-Lauf G2: 74;
  - die Abnahme von C (`erste_falte_trockenlauf.py` und drei Tests): 76.
- Seit E bleibt die Zahl in jedem Lauf gleich. Nichts gelöscht.

---

## 9. Für Fable (ohne Kontext lesbar) ⭐⭐

**Stand.** Die vier Rückfälle außerhalb der Sperrliste sind geschlossen, je mit Probe, Mutationsprobe und Gegenprobe; jede Mutation beißt allein. Ohne Modus hat sich keine Zahl und kein Pfad geändert: 8 von 8 Werkzeugausgaben bytegleich gegen `f22f91e`, `strategy_paths` bei 101 Aufrufern gleich, Benchmark `64fb2912` im Modus (Repo und Klon) und ohne Modus.

**A2 gemessen:** `strategies/elliott_wave/multi_symbol_optimise.py` trägt `MIN_HISTORY_HOURS = 17520`, genau einmal; alle anderen acht tragen `MIN_HISTORY_DAYS`, je genau einmal. Der Hinweis-Zweig war nie der echte Pfad. `_min_history()` und `kerzen_elliott_wave()` enden jetzt bei Abweichung mit 2, unabhängig vom Modus.

**A4 erreicht oder nicht:** **nicht erreicht.** Mit der echten TB-24-Eingabe haben alle neun Bots innere Kalenderjahre, keine Zählung ist leer. Das `basis`-Argument der Kopie reicht nur `faltenplan(basis)` durch; im Repo übergibt es niemand außer den Tests (Ersatzwurzel, unter dem Modus rc 2). Block C ist nach der Betreiberentscheidung von 20:27 **vor** deiner Antwort auf 25d gebaut, als eigener Commit `f5fdb53`; `git revert f5fdb53` nimmt ihn samt Probendatei zurück.

**Laufbereich neu (F1):** 81 Module, gemessen am Endstand mit dem Werkzeug aus TB-104 D1 und denselben drei Lauf-Typen. Unterschied zu den 80 von TB-104: **+ `shared/regimewache.py`**, sonst keiner. Die Liste steht in `docs/belege/TB-107/f1_laufbereich_vereinigung.txt`.

**Gegenprobe am echten Stand (F4):** 14 Stellen „fehlende Daten ⇒ `exit()`“ im `__main__` des Laufbereichs, alle 14 mit `paths.selektionsmodus()`, genau die aus TB-105 C. Keine Stelle ohne Abfrage. Der Test liest die Liste aus der Messdatei. Ausgewiesen, nicht gezählt: 10 Stellen `trades.empty ⇒ exit()` in den `equity_simulation.py` (fehlende Trades, keine fehlende Eingabe).

**Klasse (iv) für `tb40_lauf_*`:**
1. **(1) `mkdtemp`:** angelegt in `messe_bot()` mit `tempfile.mkdtemp(prefix="tb40_lauf_")`, je Bot ein Ordner (im Benchmark 10 `mkdir` + 10 `w`).
2. **(2) nur vom Lauf gelesen:** Der Kindprozess `loaderlauf.py` schreibt genau eine Datei `<bot>.json` hinein, `messe_bot()` liest sie. Im Benchmark-Audit gibt es keinen anderen Leser.
3. **(3) entfernt:** `shutil.rmtree` im `finally`, nachdem das Ergebnis gelesen ist. Ohne Ergebnis bleibt der Ordner, und sein Pfad steht in der Meldung.
- Gemessen: `$TMPDIR` vor und nach jedem Lauf dieser Sitzung gleich (4765). Vorher hinterließ ein G2-Lauf der alten Fassung 74 Ordner.
- Das Aufräumen liest die Ordner (10 Verzeichnis-Öffnungen in Klasse (i) außerhalb).

**Zwei weitere Ablagen derselben Datei, nicht freigegeben, nicht geändert:**
- `tb40_faltenplan_` in `hole_faltenplan()`: nur ohne `--faltenplan-json`, im Benchmark nicht gerufen.
- `tb40_proben_` in den Probeläufen `--stille-filter`.
- Beide bleiben weiter liegen.

**Fragen:**

1. Die zwei Ablagen `tb40_faltenplan_*` und `tb40_proben_*` in `universum_trockenlauf.py` bleiben liegen. Sind sie außerhalb des Benchmark-Laufs eine Tatsachennotiz, oder sollen sie wie `tb40_lauf_*` behandelt werden (dann in welchem Auftrag)?
2. Die 10 Stellen `if trades.empty: print(…); exit()` in den `equity_simulation.py` enden im Modus mit 0. Sie sind kein Datenmangel, sondern ein Rechenergebnis, und die Gegenprobe zählt sie nicht. Ist diese Abgrenzung richtig, oder gehören sie unter 24b A2?
3. `research/resolver_selektion/pfadvergleich.py` (TB-52-Werkzeug) endet eigenständig jetzt mit rc 1, weil es die `paths.py` aus TB-52 ohne `selektionsmodus` neben die echte `strategy_paths.py` legt. Soll es die Funktion anhängen, wie jetzt `test_paths` A es tut (eine Zeile, Datei nicht freigegeben)? Oder bleibt es ein historisches Werkzeug mit Tatsachennotiz?

## 10. Abweichungen vom Auftrag

| | |
|---|---|
| 1 | **Neue Proben je Block in eigenen Dateien** (`test_min_history.py`, `test_volle_jahre.py`, `test_zwischenablage.py`, `test_main_gegenprobe.py`). Damit bleiben die im Auftrag genannten Zahlen der bestehenden Tests (156, 163, 35) stehen. Probe G steht in `test_strategy_paths.py` („23/23 plus neue“). C hat eine eigene Datei, damit ein Revert von `f5fdb53` sie mitnimmt |
| 2 | **`import shutil` in `messe_bot()`** statt im Modulkopf (nur die Funktion war freigegeben) |
| 3 | **F1 am Code-Endstand `a79e715` gemessen**, nicht an `9827a3e`. Der Commit von F fügt nur `shared/test_main_gegenprobe.py` hinzu, keinen Code im Laufbereich. Die Datei lag während der Messung im Scratchpad (Modus verlangt sauberes `shared/`). G1/G3 liefen am Endstand `9827a3e` |
| 4 | **A8 und H1 für die Cron-Wächter nur statisch:** `crontab -l` gesperrt |
| 5 | `env -u …` im Bash-Einzeiler vom Werkzeug abgelehnt ⇒ `g2_gesamt.sh` |

## 11. Was NICHT geschah

- Nicht angefasst: alles unter `research/vorregistrierung/`, `shared/paths.py`, `shared/regimewache.py`, `loaderlauf.py`, die drei Cron-Wächter, `research/resolver_selektion/pfadvergleich.py`, alle `strategies/`, `forward_test.py`, `live_params.py`, `crontab`, das Register.
- Kein neues Abbild; die Sonde ist vorher und nachher gleich.
- Keine `tb40_*`-Ordner aus früheren Läufen gelöscht (4765 stehen weiter in `$TMPDIR`, nur gezählt).

---

## In einfacher Sprache

In den Hilfsprogrammen, die nicht auf der Sperrliste stehen, gab es noch vier Notlösungen. Alle vier sind jetzt geschlossen:

- **Die Mindestdauer aus dem Programmtext:** Ein Messprogramm liest aus jedem Bot eine Zahl. Findet es sie nicht oder doppelt, bricht es jetzt ab. Vorher nahm es still die erste oder rechnete ohne sie weiter.
- **Die zweite Kopie der Notlösung:** Die Regel, die TB-106 in den gesperrten Programmen geschlossen hat, stand ein zweites Mal in einem Hilfsprogramm. Sie bricht jetzt genauso ab. Mit echten Daten wird die Stelle nie erreicht.
- **Das Pfadprogramm:** Es läuft im Betrieb bei jedem Bot. Fehlt ihm eine Funktion, nimmt es nicht mehr still „Regelbetrieb“ an. Geprüft an 101 Programmstellen: Im Betrieb liefert es dieselben Pfade und legt dieselben Ordner an wie vorher.
- **Die Zwischenordner:** Ein Messprogramm hat bei jedem Lauf Ordner liegen lassen, zuletzt 74 in einem Durchgang. Es räumt sie jetzt selbst weg. Geht etwas schief, bleibt der Ordner stehen, und die Meldung nennt ihn.

Dazu gibt es eine neue, dauerhafte Prüfung. Sie liest die Liste aller Programme, die ein geschützter Lauf wirklich benutzt, und meldet jedes Skript, das bei fehlenden Daten die Modus-Abfrage vergisst. Heute findet sie keines.

Im normalen Betrieb hat sich an keiner Zahl und keinem Pfad etwas geändert. Die Vergleichstabelle kommt im Projekt, in einer frischen Kopie und ohne geschützten Modus Byte für Byte gleich heraus.

Eine Nebenwirkung: Ein altes Prüfwerkzeug aus TB-52, das nicht freigegeben war, meldet jetzt einen Fehler statt Grün. Die Tests, die es benutzen, sind grün. Wie damit umzugehen ist, fragt das Ergebnis Fable.

## Für die Folgesitzung vorbereitet

- **Fables Antwort auf 25d:** Heißt sie „nur Tatsachennotiz“, macht `git revert f5fdb53` Block C samt `test_volle_jahre.py` rückgängig.
- **Fragen 1–3 aus Abschnitt 9:** die Ablagen `tb40_faltenplan_`/`tb40_proben_`, die `trades.empty`-Stellen, `pfadvergleich.py`.
- **Die Gegenprobe `shared/test_main_gegenprobe.py`** liest `docs/belege/TB-107/f1_laufbereich_vereinigung.txt`. Am Tag-Commit ersetzt die Tag-Messung diese Liste (Fable 25b (5)). Dann den Pfad `LISTE` im Test umstellen oder die Datei als Argument übergeben.
- **Wiederverwendbar:**
  - `g_lauf.sh` kennt jetzt auch den Typ `auswertung`.
  - `f1_vereinigen.py` vereinigt die drei Listen und vergleicht mit TB-104.
  - `d_vergleich.py` vergleicht `strategy_paths` vorher/nachher je Aufrufer.
  - `g2_gesamt.sh` (8 Ausgaben + Benchmark ohne Modus), `g4_tests.sh`, `hashes.sh` (mit `tb40_lauf_*`-Zählung).

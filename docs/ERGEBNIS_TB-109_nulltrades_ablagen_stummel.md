# TB-109: Ergebnis. „Null Trades ist ein Wert“: die 10 Stellen `trades.empty ⇒ exit()` enden unter dem Modus mit 2, ohne Modus zeichengleich; `tb40_faltenplan_*` und `tb40_proben_*` werden entfernt; `pfadvergleich.py` mit benanntem Stummel wieder rc 0; Gegenprobe zählt 24 Stellen; Klasse (iv) im Audit. Benchmark im Modus (Repo und Klon) und ohne Modus bytegleich `64fb2912…`

**Sitzungstitel:** `TB-109` · **Stand:** 26.09.2026, ca. 00:40 · **Auftrag:**
`docs/auftraege/MAC_TB-109_nulltrades_ablagen_stummel.md` · **Belege:** `docs/belege/TB-109/`
**Eingang:** `486032d` (Abgabe-Commit TB-108). Commits: `f4d6d6d` (Schritt 0), `53896e4` (Block B), `29640ca` (Block C),
`8570ce8` (Block D), `a02f035` (Block E) und der Abgabe-Commit (Belege, dieses Dokument, Journalblock DH).
**Grundlage:** Fable 25e (1), (2), (3), 3 (b); Fable 25d (1). Freigabe des Betreibers 25.09.2026, 23:04 (zwei Auswahlkarten, wörtlich im Auftrag).
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | Arbeitsbaum wie erwartet, committet (`f4d6d6d`). **Worktree `../trading-bot-tb111` auf Zweig `tb-111` angelegt** (0c), danach nicht betreten |
| ⭐ **A** | Vormessung bestätigt. **A3 gemessen: kein Cron-Lauf erreicht heute eine der 10 Stellen** – an allen 10 ist die Trade-Liste nicht leer, alle neun `__main__`-Blöcke erreichen `simulate_portfolio` (Abbruchkriterium 3 greift nicht) |
| ⭐⭐ **B** | Live-Code, 9 Dateien: an den 10 Stellen unter dem Modus Meldung auf stderr und `SystemExit(2)`, Abfrage an der Stelle über `paths`. **Ohne Modus: Trade-Listen der neun Bots vorher = nachher, `vergleich.py --pruefen` rc 0, `test_ergebniskurven` 44/44.** Neue Proben `test_nulltrades_modus.py` 34/34 |
| ⭐ **C** | `hole_faltenplan()` und `stille_filter()` entfernen ihre Ablage nach dem Lesen; ohne Ergebnis bleibt sie mit Pfad in der Meldung. `ut.json`, `sf.json` bytegleich; eigenes `TMPDIR` vorher = nachher = 0. `test_zwischenablage` 12/12 |
| ⭐ **D** | `pfadvergleich.py` mit benanntem Stummel `selektionsmodus()` → `None`: **eigenständig rc 0, GRÜN**. ⚠️ **Die Probe mit `False` zeigt den Widerspruch nicht im Werkzeug** (auch dort 0 Unterschiede), sondern im Verhalten: `strategy_paths` legt dann **0 von 9** Ordnerpaaren an statt 9 von 9 |
| ⭐⭐ **E** | Gegenprobe zählt jedes vorzeitige `exit()` im `__main__` ohne vorher geschriebenes Ergebnis: **24 Stellen, alle mit Abfrage**, keine weitere gefunden; 16 Blockenden ausgewiesen. Audit: Zugriffe auf die eigene Ablage stehen unter (iv). ⚠️ (i) außerhalb ist damit **11, nicht 21** (Abschnitt 5) |
| ⭐⭐ **F** | Benchmark im Modus **Repo und frischer Klon `64fb2912…`**, ohne Modus `64fb2912…`. **8/8 Ausgaben ohne Modus bytegleich** gegen `f4d6d6d`. Trockenlauf 9 × rc 0. Sonde vorher = nachher, `register()` `c85dd6c3…` wie am Eingang. Tests siehe F4 |

---

## 0. Schritt 0

| | |
|---|---|
| 0a | Acht Dateien des steuernden Chats committet (`f4d6d6d`); der Arbeitsbaum entsprach genau der Erwartung |
| 0c | `git worktree add ../trading-bot-tb111 -b tb-111 HEAD` ⇒ `HEAD is now at f4d6d6d`. `worktree list` zeigt `/Users/jaquelineloffler/trading-bot-tb111 f4d6d6d [tb-111]`; `MAC_TB-111_…` liegt dort. Danach nur im Hauptordner gearbeitet |
| 0b | Keine `.git/*.lock`. HEAD am Eingang `486032d` (= Abgabe TB-108). Datenstand `d9449faf…` (223), Snapshot `--pruefen` Soll = Ist. Einzelhashes, `5_alle_vorher.txt`, 12 `*.db` in `0_hashes_vorher.txt` (`hashes.sh`). `register()` `c85dd6c3…` (= TB-108 D4). Sonde gegen `40ffe18d…`: 25/0/0, (ii) 0, rc 2 nur NICHT PRÜFBAR. **`tb40_*` in `$TMPDIR` vorher: `lauf_` 4765, `faltenplan_` 67, `proben_` 81** (dazu 456 `tb40_test_*` aus einer Testdatei; nur gezählt) |
| Vorher-Läufe | Am Code-Stand `f4d6d6d`, bevor eine Datei geändert wurde: `a3_b3_vorher.txt` (Trade-Listen der neun Bots, 9 × rc 0) und `g2_vorher.txt` (8 Ausgaben ohne Modus, 8 × rc 0). **Dieser eine G2-Lauf der alten Fassung hinterließ 1 `tb40_faltenplan_*` und 9 `tb40_proben_*`** (67 ⇒ 68, 81 ⇒ 90) – der Befund, den C schließt |

## 1. Block A: Vormessung

Beleg `a_vormessung.txt`. **Keine Abweichung von der Vormessung.**

| | Stelle | gemessen |
|---|---|---|
| A1 | die 10 Stellen | per Textsuche (`b1_einbau.py --probe`): genau 10 in 9 Dateien, Zeilen wie `TB-107/f_gegenprobe.txt` Z. 21–31 |
| A2 | Aufrufer im Betrieb | statisch wie TB-105 A3: `kurven_lauf.py:152` und `determinismus_lauf.py:602` rufen den `__main__`-Block per `runpy` (Cron 3:50/4:10). `crontab -l` nicht aufgerufen |
| ⭐ A3 | erreicht ein Cron-Lauf eine Stelle? | **nein.** `a3_b3_trades.py` importiert jedes Modul mit den Stubs von `kurven_lauf.py`, führt die Anweisungen des `__main__`-Blocks einzeln bis vor `simulate_portfolio` aus und hält vor jeder Stelle fest, ob die Liste leer ist: **10 × „leer nein“, 9 × `simulate_portfolio` erreicht** (Daten `data/`, Stand `d9449faf`). `determinismus.py` permutiert nur die Reihenfolge der vollen Symbolliste; leer ja/nein hängt davon nicht ab |
| A4 | `universum_trockenlauf.py` | `tb40_faltenplan_` (Z. 259) und `tb40_proben_` (Z. 681) ohne Aufräumen; `shutil` nur in `messe_bot` |
| A5 | `pfadvergleich.py` | rc 1, `AttributeError: module 'paths' has no attribute 'selektionsmodus'` |
| A6 | Gegenprobe | 7/7, 14 Stellen gezählt, 10 ausgewiesen |

## 2. Block B: die 10 Stellen (Live-Code)

- **B1:** Eingebaut per Textersetzung (`b1_einbau.py`, bricht bei ≠ 10 Stellen ab). An jeder Stelle **vor** dem bestehenden `print`/`exit()`: `import paths`; `if paths.selektionsmodus() is not None:` Meldung auf stderr, `raise SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)`. Kein Name aus `strategy_paths`. Ohne Modus laufen `print` und `exit()` wie vorher.
- **B2:** `shared/test_nulltrades_modus.py`, **34/34** (≈ 30 s). Wegwerfbaum und Snapshot-Attrappe aus `test_rueckfaelle_modus.py` (importiert, nicht kopiert). In der Kopie wird nur der **Erzeuger** ersetzt, die Stelle bleibt zeichengleich: `load_all_symbol_data()` liefert ein nicht leeres Attrappen-dict, `collect_all_trades(` wird zu `pd.DataFrame() if True else collect_all_trades(`. Für die zweite Stelle in `volatility_breakout_crypto` liefert der Erzeuger eine Zeile und der Filter gibt sie leer zurück.
  - N1 je Stelle: Modus ⇒ rc 2, Meldung auf stderr, nicht auf stdout (10/10);
  - N2 je Stelle: ohne Modus ⇒ rc 0, Meldung auf stdout (10/10);
  - N3: Mutation „Abfrage weg“ an einer Stelle ⇒ rc 0 statt 2, Gegenprobe am unveränderten Baum rc 2.
- **Nebenwirkung, mitgezogen:** `test_rueckfaelle_modus` C3 mutiert die Zeile `if paths.selektionsmodus() is not None:` + `sys.stderr.write(`, die jetzt in `elliott_wave/equity_simulation.py` zweimal steht; die Mutation griff nicht mehr. Das Muster nennt jetzt die Meldung (`"Keine Daten`) mit, 48/48.
- **B3 (`b3_abnahme.txt`):** Trade-Listen der neun Bots vorher = nachher (10 × gleicher sha256, „leer nein“, 9 × `simulate_portfolio` erreicht; nur die Zeilennummern verschoben um 7 bzw. 14); `vergleich.py --pruefen` rc 0 „UNVERAENDERT“; `test_ergebniskurven` 44/44; `test_rueckfaelle_modus` 48/48.

## 3. Block C: `universum_trockenlauf.py`

- `hole_faltenplan()`: `import shutil` lokal; ohne Ergebnis `RuntimeError` mit „Ablage bleibt stehen: <Pfad>“; sonst Lesen im `try`, `shutil.rmtree(ordner)` im `finally`.
- `stille_filter()`: `import shutil` lokal; scheitert `messe_bot` oder meldet der Probelauf `fehler`, `RuntimeError` mit dem Pfad von `tb40_proben_*`, der Ordner bleibt. Sonst wird das Ergebnis im `try` gebildet, `shutil.rmtree(ordner)` im `finally`.
- Proben in `test_zwischenablage.py` (jetzt **12/12**, vorher 4): je Ablage Normallauf (kein Ordner danach), „ohne Ergebnis“ (Ordner steht, Pfad in der Meldung), Mutation „Aufräumen weg“ mit Gegenprobe. Jede Probe mit eigenem `TMPDIR`. Die Mutation wird **nur im Rumpf der jeweiligen Funktion** gesetzt, weil dieselbe Zeile `shutil.rmtree(ordner)` jetzt in drei Funktionen steht.
- **Abnahme (`c_abnahme.txt`):** `ut.json`, `sf.json` bytegleich gegen `g2_vorher`. Eigenes `TMPDIR`: vorher 0, nach `ut --json` (ruft `hole_faltenplan()` ohne `--faltenplan-json`) 0, nach `--stille-filter` 0, Verzeichnis leer. System-`TMPDIR` vor und nach einem weiteren `ut --json`: gleich (4765/68/90). `test_universum_trockenlauf` 163/163.

## 4. Block D: `pfadvergleich.py`

- Konstante `STUMMEL = "\n\ndef selektionsmodus():\n    return None\n"` mit dem Kommentar aus dem Auftrag („Fassung TB-52 plus `selektionsmodus()` → None, weil der heutige Nachbar die Funktion verlangt (Fable 25e (3); `None` statt `False`, weil `strategy_paths` `is not None` fragt)“). `main()` hängt ihn an die alte Fassung an.
- **Abnahme:** eigenständig **rc 0, „GRUEN“** (99 Pfade, 0 Unterschiede, Selbstprobe beißt mit 18). `test_paths` 35/35 (A1 99/0), `test_startpruefungen` 44/44 (N4 144/0).
- ⚠️ **Probe `False` (`d_stummel_probe.txt`), anders als im Auftrag erwartet:**

| Stummel | Werkzeug | `strategy_paths` legt `results/<bot>` und `logs/<bot>` an |
|---|---|---|
| `None` (gebaut) | 99 verglichen, 0 Unterschiede ⇒ GRÜN | 9 von 9 (wie ohne Modus) |
| `lambda: False` (Fable 25e (3)) | 99 verglichen, **0 Unterschiede ⇒ ebenfalls GRÜN** | **0 von 9** (hält den Modus für aktiv) |

  Der Auftrag erwartete „der Stummel mit `False` ⇒ das Werkzeug meldet Unterschiede“. Das trifft nicht zu. `get_strategy_paths` gibt unter dem vermeintlichen Modus **dieselben Zeichenketten** zurück und lässt nur die Ordneranlage weg; das Werkzeug vergleicht nur Zeichenketten. **Der Widerspruch ist damit am Verhalten belegt, aber nicht an der Ausgabe des Werkzeugs:** mit `False` würde es grün melden und dabei einen anderen Zweig von `strategy_paths` durchlaufen als jeder echte Aufruf ohne Modus.

## 5. Block E: Gegenprobe und Audit

- **E1 (`e1_gegenprobe.txt`, 13/13):** `shared/test_main_gegenprobe.py` zählt jetzt **jeden Ausstieg in einem `if` des `__main__`-Blocks**, vor dem im Rumpf dieses `if` kein Schreibaufruf eines Ergebnisses steht (`json.dump`, `.to_csv`/`.to_json`/`.to_parquet`, `.write_text`, `open(…, "w"/"a"/"x")`). Die Art (Daten/Trades/sonst) wird nur ausgewiesen. Ausgewiesen, nicht gezählt: der Ausstieg als letzte Anweisung des Blocks (`sys.exit(main())` u. ä.).
  - **Am echten Stand: 24 Stellen (14 Daten + 10 Trades), alle mit Abfrage** (F2, F2b). **Keine weitere Stelle ohne Abfrage gefunden.** Ausgewiesen: 16 Blockenden, 0 „nach geschriebenem Ergebnis“.
  - Mutationen, je mit Gegenprobe: F3a (Datenstelle ohne Abfrage), **F3c (die 25. Stelle: „Keine Trades“ ohne Abfrage) ⇒ rot**, F3b (erfundene Datenstelle), **F3d (`exit()` ohne Daten-/Trades-Bezug) ⇒ rot**, **F3e (Ausnahme: `json.dump` vor dem `exit()` bzw. `sys.exit(main())` am Blockende ⇒ nicht gezählt)**.
- **E2 (`e2_abnahme.txt`):** neue Fassung `docs/belege/TB-109/d_auswerten.py`; die Fassung TB-104 bleibt. Regel: Ein Verzeichnis im Temp-Verzeichnis, das ein Prozess **dieses** Laufs selbst anlegt (`mkdir` im Protokoll), ist eine eigene Ablage. Jeder lesende Zugriff darauf oder darunter steht unter (iv), mit dem Vermerk, ob die Ablage bei der Auswertung noch existiert.

| Lauf | Werkzeug | (i) Snapshot | (i) außerhalb | (iii) | (iv) |
|---|---|---|---|---|---|
| Benchmark Repo | TB-104 | 225 | 31 | 20 | – |
| Benchmark Repo | **TB-109** | 225 | **11** | 20 | 10 Ablagen, 20 Zugriffe (10 Verzeichnis-Öffnungen durch `rmtree`, 10 Ergebnis-JSON), alle entfernt |
| Benchmark Klon | TB-109 | 225 | 11 | 36 | wie Repo |
| 9 Bots Trockenlauf | TB-109 | 27/153 | 0 | – | 0 |

  ⚠️ **Abweichung:** Der Auftrag erwartete „(i) außerhalb wieder 21 (wie TB-106); die 10 Öffnungen unter (iv)“. Das Werkzeug folgt dem Regeltext von E2 („Zugriffe eines Laufs auf seine eigene Klasse-(iv)-Ablage“) und führt **auch die 10 Lesezugriffe auf das Ergebnis-JSON in der Ablage** unter (iv). Diese 10 standen schon in den 21 von TB-106. Deshalb 21 − 10 = 11. Die 11 sind: 9 TB-24-Listen, `messgroessen.json` und die Tempfile-Probe von `mkdtemp` (von `tempfile` selbst angelegt und entfernt, kein `mkdir` im Protokoll ⇒ nach der Regel keine Ablage). Frage 2 unten.

## 6. Block F: Abnahme

| | | Beleg |
|---|---|---|
| F1 | Benchmark im Modus: **Repo `64fb2912…` rc 0 (57 s), frischer Klon (`git clone`, HEAD `a02f035`) `64fb2912…` rc 0 (57 s)**. Klon `status --porcelain --ignored` vorher und nachher leer. `tb40_*` in `$TMPDIR` vor = nach jedem Lauf | `g1_g3.txt` |
| F2 | Ohne Modus: **8/8 Ausgaben bytegleich** gegen `g2_vorher` (`f4d6d6d`); Benchmark ohne Modus `64fb2912…` | `g2_nachher.txt` |
| F3 | Trockenlauf im Modus 9 × rc 0 | `g1_g3.txt` |
| F4 | Tests | `g4_tests.txt` |
| F5 | Sonde gegen `40ffe18d…` vorher = nachher (25/0/0, (ii) 0); `register()` `c85dd6c3…` wie am Eingang | `f_sonde_nachher.txt`, `h1_hashes_nachher.txt` |

**F4 Tests (trading-env 3.9.6, alle rc 0):** `test_faltenplan_neun` 156/156, `test_erste_falte_trockenlauf` 50/50, `test_horizontbeginn` 61/61, `test_min_history` 14/14, `test_volle_jahre` 7/7, `test_universum_trockenlauf` 163/163, `test_zwischenablage` **12/12** (vorher 4), `test_paths` 35/35, **`test_nulltrades_modus` 34/34 (neu)**, `test_strategy_paths` 27/27, `test_rueckfaelle_modus` 48/48, `test_ergebniskurven` 44/44, `test_startpruefungen` 44/44, `test_main_gegenprobe` **13/13** (vorher 7), `test_ersatzwerte` 40/40, **`test_vorregistrierung` 196/196** (870 s). `tb40_*` in `$TMPDIR` nach den Tests unverändert (4765/68/90).

## 7. Hashes nachher

Beleg `h1_hashes_nachher.txt`, Vergleich `h1_vergleich.txt`.

- **Geändert (versioniert, außerhalb `docs/`):** die 9 `equity_simulation.py`, `universum_trockenlauf.py`, `test_zwischenablage.py`, `pfadvergleich.py`, `test_main_gegenprobe.py`, `test_rueckfaelle_modus.py`; neu `shared/test_nulltrades_modus.py` (1538 ⇒ 1539 Dateien). Alles freigegeben (Karte 23:04: „die Tests dieser Module“).
- **Unverändert:** alle gesperrten und nicht freigegebenen Dateien aus (2), darunter `shared/paths.py`, `shared/strategy_paths.py`, `regimewache.py`, `kurven_lauf.py`, `determinismus_lauf.py`, alle `forward_test.py`/`live_params.py`/`multi_symbol_optimise.py`, das Register; `ergebnisse/` einzeln; Snapshot und Datenstand `d9449faf…`; `herkunft.register()` `c85dd6c3…`; `docs/belege/TB-104/d_auswerten.py`.
- **`*.db`:** 11 von 12 gleich. `broker_testnet_t3_supertrend.db` geändert – die Binance-Brücke läuft per Cron alle 4 h zur Minute 5 (hier 00:05). Diese Sitzung hat die Brücke nicht aufgerufen.
- ⚠️ **Randbefund:** `tb40_test_*` 456 ⇒ 492. Diese Ordner legt die Testdatei `test_universum_trockenlauf.py` selbst an (`tempfile.mkdtemp(prefix="tb40_test_…")`, Z. 123/136/192), 18 je Lauf, zwei Läufe in dieser Sitzung. Eine Testdatei gehört nicht zum Laufbereich; nicht freigegeben als Gegenstand von C, deshalb nicht geändert.

## 8. Für Fable (ohne Kontext lesbar) ⭐⭐

**Stand.** Deine Antwort 25e ist umgesetzt, soweit sie Code betrifft. Ohne Modus hat sich keine Zahl und kein Pfad geändert: 8 von 8 Werkzeugausgaben bytegleich, Trade-Listen der neun Bots gleich, `vergleich.py --pruefen` rc 0, Benchmark `64fb2912` im Modus (Repo und Klon) und ohne Modus.

**A3 gemessen – erreicht ein Cron-Lauf heute eine der 10 Stellen?** **Nein.** Die `__main__`-Blöcke der neun `equity_simulation.py` wurden so ausgeführt, wie `kurven_lauf.py` (Cron 3:50) sie startet: gleiche Stubs, Daten `data/`, ohne Modus. Die Anweisungen liefen einzeln bis vor `simulate_portfolio`. An allen 10 Stellen war die Trade-Liste **nicht leer**, und alle neun Läufe erreichten `simulate_portfolio`. `determinismus.py` (4:10) permutiert nur die Reihenfolge der Symbolliste; leer ja/nein hängt nicht davon ab. Das ist eine Tatsache über den heutigen Datenstand.

**Die 24 Stellen.** Die Gegenprobe zählt jetzt jedes vorzeitige `exit()`/`sys.exit()`/`quit()` im `__main__`-Block eines Moduls des Laufbereichs (81 Module, Messung TB-107), vor dem im selben `if` kein Ergebnis geschrieben wird. Gefunden: **24 = 14 „keine Daten“ (TB-105) + 10 „keine Trades“ (TB-109), alle mit `paths.selektionsmodus()`**. Sonst gibt es im `__main__` des Laufbereichs nur 16 reguläre Blockenden (`sys.exit(main())`, `sys.exit(0)`, `sys.exit(1 if wache.melde() else 0)`), die die Rückgabe des Laufs nach außen tragen; sie sind ausgewiesen, nicht gezählt. **Grenze der Probe:** Was `main()` in sich tut, prüft sie nicht; ein `return 0` ohne Ausgabe in `main()` fände sie nicht.

**Der Widerspruch `False`/`None` in 25e (3), mit Verhaltensbeleg.** Dein Stummel `selektionsmodus = lambda: False` und `strategy_paths.py` (seit TB-107: `paths.selektionsmodus() is not None`) passen nicht zusammen: `False is not None` ist wahr. Mit `False` hält `strategy_paths` den Modus für aktiv. Gebaut ist deshalb `def selektionsmodus(): return None`, wie in `test_paths` Probe A. Gemessen (`d_stummel_probe.txt`):
- mit `None`: 0 Unterschiede, und `strategy_paths` legt in 9 von 9 Bots `results/` und `logs/` an, wie jeder echte Aufruf ohne Modus;
- mit `False`: **ebenfalls 0 Unterschiede**, aber `strategy_paths` legt in **0 von 9** Bots Ordner an – es läuft den Modus-Zweig.

Der Widerspruch zeigt sich also **nicht** in der Ausgabe des Werkzeugs, denn es vergleicht nur Zeichenketten, und die sind in beiden Zweigen gleich. Er zeigt sich im durchlaufenen Zweig. Mit `False` würde das Werkzeug grün melden und dabei nicht den Pfad messen, den es messen soll. Der steuernde Chat trägt das in TB-110 als vorläufige Berichtigung ein.

**Klasse (iv) im Audit.** Die neue Auswertung erkennt eine Ablage daran, dass ein Prozess des Laufs sie im Temp-Verzeichnis selbst angelegt hat (`mkdir` im Protokoll). Jeder lesende Zugriff darauf oder darin steht unter (iv), mit „entfernt ja/nein“ zum Zeitpunkt der Auswertung. Im Benchmark (Repo und Klon) ergibt das: 10 Ablagen `tb40_lauf_*`, 20 Zugriffe (10 Verzeichnis-Öffnungen durch `rmtree`, 10 Ergebnis-JSON), alle 10 entfernt. (i) außerhalb fällt von 31 auf **11**. Schreibzugriffe (`mkdir`, `w`) bleiben unter (iii), wie TB-104 sie definiert.

**Zwei Ablagen mehr entfernt.** `tb40_faltenplan_*` (`hole_faltenplan()` ohne JSON) und `tb40_proben_*` (`--stille-filter`) werden jetzt wie `tb40_lauf_*` behandelt: `finally`, und ohne Ergebnis Pfad in der Meldung. Ein Lauf der alten Fassung hinterließ 1 + 9 Ordner, seit C 0.

**Fragen:**

1. **Stummel und Probe.** Bestätigst du die Berichtigung `None` statt `False`? Soll das Werkzeug zusätzlich prüfen, dass der Stummel den Nicht-Modus-Zweig nimmt (z. B. die angelegten Ordner im Wegwerfbaum zählen)? Heute würde ein falscher Stummel grün durchgehen.
2. **(iv) im Audit – welche Zugriffe?** Gebaut ist: **alle** lesenden Zugriffe auf die eigene Ablage, also die Verzeichnis-Öffnung beim Aufräumen **und** das Lesen des Ergebnisses darin. Damit ist (i) außerhalb 11. Der Auftrag erwartete 21, also nur die Verzeichnis-Öffnungen umgeordnet. Welche Lesart meint 25e 3 (b)? Und gehört die Tempfile-Probe von `mkdtemp` (von `tempfile` angelegt und sofort entfernt, ohne `mkdir`) ebenfalls zu (iv)?
3. **Grenze der Gegenprobe.** Sie prüft `__main__`-Blöcke, nicht `main()`-Funktionen, die mit `return 0` ohne Ausgabe enden könnten. Soll die Erweiterung auf `main()` für den Laufcode (TB-30b) kommen, oder reicht der Satz aus 25e, dass der Erzeuger für eine Zelle ohne Trades die Nullzeile schreibt?

## 9. Abweichungen vom Auftrag

| | |
|---|---|
| 1 | **D: Die Probe `False` zeigt keine Unterschiede im Werkzeug** (Auftrag: „das Werkzeug meldet Unterschiede“). Belegt ist der Widerspruch am durchlaufenen Zweig (Ordneranlage 0/9 statt 9/9), Abschnitt 4 |
| 2 | **E2: (i) außerhalb 11 statt 21**, weil auch das Lesen des Ergebnisses in der eigenen Ablage unter (iv) steht (Regeltext von E2). Abschnitt 5, Frage 2 |
| 3 | **Neue Proben für B in eigener Datei** `shared/test_nulltrades_modus.py` (34). `test_rueckfaelle_modus` bleibt bei 48, nur ihr C3-Muster ist eindeutig gemacht (Nebenwirkung von B, Abschnitt 2) |
| 4 | **E: Commit (5) enthält den Test und das neue Audit-Werkzeug**; die Abnahme von E2 lief danach am Benchmark aus F, ihre Belege liegen im Abgabe-Commit. Der Modus verlangt ein sauberes `shared/`, deshalb wurde der Test vor den Modus-Läufen committet |
| 5 | **C-Abnahme mit eigenem `TMPDIR`**, zusätzlich ein Lauf mit dem System-`TMPDIR`: Sitzung B arbeitet parallel im Worktree und kann ins selbe System-`TMPDIR` schreiben |
| 6 | A2 wie in TB-105 nur statisch (`crontab -l` nicht aufgerufen) |

## 10. Was NICHT geschah

- Nicht angefasst: alles unter `research/vorregistrierung/`, `shared/paths.py`, `shared/strategy_paths.py`, `regimewache.py`, die Cron-Wächter, `forward_test.py`, `live_params.py`, Register, `crontab`, der Worktree `../trading-bot-tb111`.
- Kein neues Abbild; die Sonde ist vorher und nachher gleich.
- Keine `tb40_*`-Ordner aus früheren Läufen gelöscht (nur gezählt).
- Kein Abbruchkriterium ausgelöst ⇒ TB-110 folgt in dieser Sitzung (Block H).

---

## In einfacher Sprache

Findet ein Bot in der Simulation keine Geschäfte, ist das ein Ergebnis (null), kein Grund, still aufzuhören. Zehn Stellen hörten bisher still auf. Im geschützten Auswahlmodus melden sie das jetzt als Fehler; im normalen Betrieb bleibt alles, wie es war – nachgemessen an allen neun Bots. Heute erreicht übrigens keiner der nächtlichen Läufe eine dieser Stellen. Zwei weitere Zwischenordner werden nach Gebrauch aufgeräumt. Das alte Prüfwerkzeug für die Pfade meldet wieder „grün“. Der kleine Denkfehler im Vorschlag des Prüfers lässt sich am Verhalten zeigen, aber nicht an der Ausgabe des Werkzeugs – das steht als Frage an ihn im Bericht.

# TB-112: Ergebnis. Bündel: Sauberkeit über den Laufbereich (Register 19, 42.2 E2 / 42.3 F8) in `shared/paths.py`, nur unter dem Modus, mit der namentlichen Ausnahme `herkunft_protokoll.jsonl`; db-Sicherung als Skript nach iCloud (lesend, erster Lauf 12/12 `ok`); `test_universum_trockenlauf.py` räumt seine 18 Ordner je Lauf selbst auf. Benchmark im Modus (Repo und Klon) `64fb2912…`, ohne Modus 8/8 Ausgaben bytegleich

**Sitzungstitel:** `TB-112` · **Stand:** 26.09.2026, ca. 10:40 · **Auftrag:**
`docs/auftraege/MAC_TB-112_19_laufbereich_db_sicherung.md` · **Belege:** `docs/belege/TB-112/`
**Eingang:** `e731207` (Schritt 0 auf `6a7996a`, Abgabe TB-110). Commits: `e731207` (Schritt 0), `9d711dc` (Block A: Code und Tests),
`e65e57c` (Block B), `21f4cac` (Block C) und der Abgabe-Commit (Belege, dieses Dokument, Journalblock DJ).
**Grundlage:** Register 19 (Kasten „Sauberkeit über den Laufbereich — beschlossen, nicht vollzogen“), 42.2 E2, 42.3 F8; Fable 25f O6.
Freigabe des Betreibers 26.09.2026, ca. 06:40 und 07:00 (Auswahlkarten, wörtlich im Auftrag).
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6), `/usr/bin/sqlite3` 3.43.2.
**Parallel:** Sitzung B (TB-111) im Worktree `~/trading-bot-tb111`. Nicht betreten, nicht aufgeräumt.

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | Die vier erwarteten Dateien committet (`e731207`), gepusht. Eingang wie erwartet: `ARBEITSBAUM_PFADE` Z. 225 `("shared", "strategies", LOCK)`, `register()` `c92900a8…`, Sonde gegen `40ffe18d…` 25/0/0 und (ii) 0, `test_startpruefungen` 44/44 |
| ⭐ **A1** | **Befund aus E2 bestätigt:** Im frischen Klon unter dem Modus lief der Import mit einer uncommitteten Änderung in `benchmark.py`, `faltenplan_neun.py` und `manual_close.py` jeweils **durch (rc 0)**. Kontrolle unter `shared/` hielt an (rc 2). Kein Abbruchkriterium |
| **A2** | Laufbereich am Eingang: **81 Module, identisch mit TB-107 F1** (auch die Lauf-Typen je Modul), 12 davon außerhalb `shared/`/`strategies/` |
| ⭐⭐ **A3** | `ARBEITSBAUM_PFADE` + 12 Einzeldateien (15 Einträge), neue Konstante `REGISTRIERTE_PROTOKOLLE` als `:(exclude)`-Pfadangabe. Nur in `_pruefe_codeherkunft` wirksam, das nur unter dem Modus läuft. Keine neuen Importe |
| ⭐ **A4** | Neue Testdatei `shared/test_arbeitsbaum_laufbereich.py` **26/26** (≈ 17 s, frischer Klon): 12 Module einzeln rc 2 mit Dateiname; Protokoll neu **und** versioniert-verändert rc 0; `data/` und `ergebnisse/` rc 0; Gegenprobe aus der Messdatei grün; Mutationen G3 (14/14), P1 und T1 beißen |
| ⭐ **A5** | Ohne Modus nichts geändert: `test_startpruefungen` 44/44 mit **0/0/0** Aufrufen und **144 Pfaden zeichengleich**, `test_paths` 35/35, **8/8 Ausgaben bytegleich** gegen `e731207` |
| ⭐⭐ **A6** | Benchmark im Modus **Repo und frischer Klon `64fb2912…`**, Trockenlauf 9 × rc 0, Auswertungs-Import rc 0, beide Auditzeilen „arbeitsbaum sauber“. Sonde vorher = nachher, `register()` `c92900a8…` unverändert. **Lese-Audit: 0 Code-Zugriffe außerhalb von `ARBEITSBAUM_PFADE`** (Repo und Klon). Randbefund: 10 versionierte **Eingabe**dateien außerhalb der Liste (Abschnitt 1.6) |
| **A7** | Tatsachennotiz `arbeitsbaum_pfade.txt` neben `a2_laufbereich.txt` |
| ⭐⭐ **B** | `docs/werkzeuge/db_sicherung/db_sicherung.sh` und `LIESMICH.md`. **12 Datenbanken** gefunden (11 im Wurzelordner, 1 leere unter `strategies/volatility_breakout/`). Schlüssel-Prüfung: **0 Treffer**, Gegenprobe mit `api_key` beißt. Zwei Testläufe je 12/12 `ok`, Originale unverändert. **Erster Lauf ins iCloud-Ziel rc 0, 12/12 `ok`, 368 KiB** |
| ⭐ **C** | `tb40_test_*`: vorher **18 Ordner je Lauf** (1 `fp_` + 5 `ll_` + 12), nachher **0**; 163/163 vorher und nachher. `tb44_l_` war schon per `finally` abgebaut |
| **D** | Testreihe am Endstand: **17 Testdateien rc 0**, darunter `test_vorregistrierung` 196/196, `test_startpruefungen` 44/44, neu `test_arbeitsbaum_laufbereich` 26/26; `$TMPDIR` vorher = nachher |

---

## 0. Schritt 0

| | |
|---|---|
| 0a | `git status` am Eingang: genau die vier erwarteten Dateien (Auftrag, Zeiger, Übergabe Nachtrag 4, Entscheidungen 25f). Committet als `e731207`, gepusht |
| 0b | `worktree list`: `/Users/jaquelineloffler/trading-bot e731207 [main]`, `/Users/jaquelineloffler/trading-bot-tb111 49f0868 [tb-111]`. Nicht angefasst |
| 0c | `0c_eingang.txt`: `ARBEITSBAUM_PFADE` Z. 225 wie erwartet; `register()` `c92900a8…`, fehlend []; Sonde gegen `40ffe18d…`: 25/0/0, (ii) 0, rc 2 nur NICHT PRÜFBAR (Listentext Z. 901–1014); `test_startpruefungen` 44/44 (N1 0/0/0, N4 144 Pfade); `herkunft_protokoll.jsonl` existiert nicht; `git status` außerhalb `docs/` leer. In `$TMPDIR`: `tb40_lauf_` 4765, `tb40_faltenplan_` 70, `tb40_proben_` 108, `tb40_test_*` 492, `tb44_l_` 0 (nur gezählt) |

## 1. Block A: 19 auf den Laufbereich

### 1.1 A1 — Vorher-Probe (`a1_vorher.py`, `a1_vorher.txt`)

Frischer Klon am Eingangs-Commit, Einstiegspunkt `tb112_probe_einstieg.py` unversioniert in der Klonwurzel (er macht nur `import paths`), Modus auf den Snapshot des Klons, Commit = HEAD des Klons. Je Probe eine angehängte Kommentarzeile, danach `git checkout --`.

| Probe | rc |
|---|---|
| keine Änderung | 0 |
| Kontrolle `shared/zuteilung.py` | **2** (Meldung „nicht sauber“) |
| `research/vorregistrierung/benchmark.py` | **0** |
| `research/faltenplan_neun/faltenplan_neun.py` | **0** |
| `notifications/manual_close.py` | **0** |

Der Befund aus E2 beschreibt den Stand. Kein Abbruch.

### 1.2 A2 — Laufbereich (`a2_*.txt`, `a2_laeufe.sh`, `a2_vereinigen.py`)

Werkzeug TB-104 D1 (`d1_listen.py`, Haken `haken/sitecustomize.py`), dieselben drei Lauf-Typen wie TB-107 F1: Trockenlauf aller neun (9 × rc 0), Benchmark im Modus (rc 0, `64fb2912…`), `auswertung.py`-Import (rc 0). **81 Module, gemeinsam mit TB-107 81, neu 0, weggefallen 0**; die Listen ohne Kopfzeilen sind zeilengleich, auch die Lauf-Typen je Modul. Die Messumschläge unter `docs/belege/` sind ausgewiesen und zählen nicht. Kein Modul liegt außerhalb des Repos.

Die 12 Module außerhalb `shared/`/`strategies/`: `notifications/manual_close.py`; `research/exposure_messung/bot_lauf.py`; `research/faltenplan_neun/` `erste_falte_trockenlauf.py`, `faltenplan_neun.py`, `faltenschranke_messung.py`; `research/universum_trockenlauf/` `loaderlauf.py`, `universum_trockenlauf.py`; `research/vorregistrierung/` `auswertung.py`, `benchmark.py`, `faltenplan.py`, `kennzahlen.py`, `registerdaten.py`.

### 1.3 A3 — Bau (`shared/paths.py`, Commit `9d711dc`)

- `ARBEITSBAUM_PFADE`: `shared`, `strategies`, `requirements.lock` wie bisher, dazu die 12 Module **als einzelne Dateipfade**. Ein Tatsachenkommentar nennt die Messung, aus der die Liste stammt, und dass sie am Tag-Commit mit der Tag-Messung erneuert wird.
- **Warum Einzeldateien und nicht Ordner.** Fünf der zwölf liegen in `research/vorregistrierung/`, und dort liegt `ergebnisse/`, in das Läufe schreiben (`--ziel`, Klasse (iii)). Als Ordner geprüft würde die Ausgabe eines früheren Laufs den nächsten anhalten (Probe K4 und Mutation P1 zeigen genau das). Dasselbe gilt sinngemäß für `research/faltenplan_neun/` und `research/universum_trockenlauf/`, die Testdateien und Messausgaben neben dem Code tragen. **Einen besseren Schnitt sehe ich nicht.** Der Preis der Einzeldateien: Ein **neues** Modul im Laufbereich ist ungeprüft, bis die Liste nachgezogen ist. Dagegen steht die Gegenprobe G1, die gegen die Messdatei prüft, allerdings nur gegen die zuletzt gemessene.
- `REGISTRIERTE_PROTOKOLLE = ("research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl",)`, im `git status` als `:(exclude)`-Pfadangabe. Heute deckt kein geprüfter Pfad das Protokoll (Probe P2 zeigt: ohne die Ausnahme weiter rc 0). Die Ausnahme steht also **namentlich, nicht zufällig**, wie verlangt.
- `data/` bleibt ausgenommen, wie in 19.
- Meldung bei Verletzung: `… ist ueber die 15 Pfade in `paths.ARBEITSBAUM_PFADE` (shared, strategies, requirements.lock und 12 Einzeldateien des Laufbereichs; ausgenommen `paths.REGISTRIERTE_PROTOKOLLE`) nicht sauber (n Eintrag/Eintraege, die ersten: …)`. Die ersten drei `git status`-Zeilen nennen die Dateien.
- **Ohne Modus:** Die Liste wird nur in `_pruefe_codeherkunft` gelesen, und das läuft nur im `else`-Zweig des Modus. Keine neuen Importe, kein neuer Aufruf auf Modulebene. Der Kopf-Docstring (Bedingung 3) nennt die Erweiterung.

### 1.4 A4 — Proben (`shared/test_arbeitsbaum_laufbereich.py`, 26/26)

Bauart: ein **frischer Klon** des Repos (`git clone` in `$TMPDIR/tb112_klon_*`, am Ende per `shutil.rmtree` entfernt, Probe Z). Die Fassung von `paths.py` unter Prüfung wird im Klon committet („Prüfstand“), Einstiegspunkt wie in A1. Jeder Lauf ist ein eigener Prozess unter dem Modus.

| Probe | erwartet | gemessen |
|---|---|---|
| G0/G1 Gegenprobe: jeder Pfad der Messdatei `a2_laufbereich.txt` gedeckt (Präfix oder Datei) | grün | 81/81 gedeckt |
| G2 die Module außerhalb `shared`/`strategies` stehen als Einzeldateien im Tupel | grün | 12/12 |
| G3 Mutation: je ein Eintrag entfernt | Gegenprobe rot | **14/14** beißen (`requirements.lock` ausgenommen: kein Modul, stammt aus TB-58) |
| K0 sauberer Klon / K0b Kontrolle `shared/` | rc 0 / rc 2 | 0 / 2 |
| K1 je eines der 12 Module verändert, alle einzeln | rc 2, Meldung nennt die Datei | 12 × rc 2 mit Dateiname |
| K2a `herkunft_protokoll.jsonl` neu angelegt | rc 0 | 0 |
| K2b dasselbe versioniert (Wegwerf-Commit im Klon) und verändert (`git status` ` M`) | rc 0 | 0 |
| K3 neue Datei unter `data/` | rc 0 | 0 |
| K4 neue, unversionierte Datei in `research/vorregistrierung/ergebnisse/` | rc 0 | 0 |
| P1 Mutation: `REGISTRIERTE_PROTOKOLLE` aus der Pfadangabe raus, `ergebnisse/` als Ordner geprüft | Protokoll-Probe rot | **rc 2** |
| P2 Tatsache: nur die Ausnahme raus, kein Ordner | – | rc 0 (heute deckt kein Pfad das Protokoll) |
| T1 Mutation: Tupel wie vor TB-112, `benchmark.py` verändert | läuft durch | rc 0 (der Befund aus E2) |

Die Gegenprobe liest die Liste **aus der Messdatei**, nicht aus einem Literal (Bauart TB-107 G). Der Tatsachenkommentar im Kopf sagt: Am Tag-Commit ersetzt die Tag-Messung die Datei, dann `LAUFBEREICH` umstellen. `a2_laufbereich.txt` ist deshalb im Commit von A3/A4 enthalten, nicht erst in den Belegen.

### 1.5 A5 — Abnahme ohne Modus

- `test_startpruefungen` **44/44**: N1 „0 subprocess-Aufrufe, 0 Paketabfragen – subprocess 0 / importlib.metadata 0 / os.system,popen 0“, N3 keine Modulebene-Importe, N4 **144 Pfade (9 Bots), 0 Unterschiede** (`a5_test_startpruefungen.txt`).
- `test_paths` **35/35**, `test_strategy_paths` 27/27.
- **8 Ausgaben** (`g2_ausgaben.sh`, Kopie TB-109) nachher mit dem neuen `paths.py` und vorher mit dem `paths.py` von `e731207` (für den Vorher-Lauf vorübergehend aus git geholt, danach aus der Scratch-Kopie zurückgelegt und per `cmp` bestätigt): **8/8 BYTEGLEICH** (`a5_ausgaben.txt`). Die Hashes sind zudem dieselben wie in TB-109 `g2_vorher.txt`.

### 1.6 A6 — Abnahme mit Modus, am Endstand `21f4cac`

- `a6_laeufe.txt`: `git status` über alle 15 Einträge leer. Benchmark **Repo rc 0 `64fb2912…`**, **frischer Klon rc 0 `64fb2912…`** (Klon `status --ignored` vorher und nachher leer). Trockenlauf 9 × rc 0, `auswertung`-Import rc 0. Beide Benchmark-Läufe schreiben die Auditzeile `arbeitsbaum sauber` mit Commit `21f4cac…`.
- Laufbereich am Endstand erneut aus diesen Läufen: alle drei Listen gleich A2.
- Sonde gegen `40ffe18d…` vorher = nachher (Ausgabe ohne Kopfzeilen zeilengleich), `register()` **`c92900a8…`** unverändert (`0c_ausgang.txt`).
- ⭐ **Lese-Audit** (`a6_code_audit.py`, `a6_code_audit.txt`). `d_auswerten.py` (TB-109) hat keine Klasse „Code“; das Audit-Skript nutzt deshalb dieselben Protokolle, dieselbe Einteilung lesend/schreibend und dieselbe Rückführung von Bytecode auf die Quelle. Es zählt jeden **lesenden** Zugriff unter der Codewurzel, der nicht von `ARBEITSBAUM_PFADE` gedeckt ist. Nicht gezählt, aber ausgewiesen: Snapshot, `trading-env`, Messumschläge `docs/belege/`, `REGISTRIERTE_PROTOKOLLE`, Scratchpad, außerhalb des Repos.
  - **CODE (`.py`) außerhalb: 0** im Repo (22 178 lesende Zugriffe, 11 Läufe) und **0** im Klon (14 572). Erwartung erfüllt.
  - ⚠️ **Randbefund, nicht behoben:** Der Benchmark liest (in Repo **und** Klon) **10 versionierte Eingabedateien außerhalb der Liste**: `research/vorregistrierung/ergebnisse/messgroessen.json` und die neun `research/tb24_haltedauern/daten/<bot>_alle_trades.csv`. Das ist nicht Code, E2 bindet ihn also nicht. Eine uncommittete Änderung daran hielte die Startprüfung aber nicht an. `messgroessen.json` ist durch die Sonde gedeckt (Gruppe `eingefroren`, Hash gleich), die neun TB-24-Listen nicht. Frage 1 an Fable.
  - Im Klon liest der Lauf aus dem echten Repo nur `trading-env` (1498 Zugriffe), sonst nichts.
  - Handwerk: Die erste Fassung des Audit-Skripts sortierte den Klon als „Scratchpad“ aus, weil der Klon im Scratchpad liegt. Das Ergebnis war eine falsche 0 für die Eingaben. Die Reihenfolge ist berichtigt (erst Repo, dann Scratchpad); der Beleg ist die berichtigte Fassung.

### 1.7 A7 — Tatsachennotiz

`docs/belege/TB-112/arbeitsbaum_pfade.txt`: die 15 geprüften Einträge (per Import ohne Modus gelesen), je mit Art (Ordner / Lock / Datei des Laufbereichs), die eine Ausnahme und der Satz „nicht geprüft: `data/` und alles übrige“. Sie steht neben `a2_laufbereich.txt`. Der Registereintrag folgt in Register 44.

## 2. Block B: db-Sicherung (Fable 25f O6)

### 2.1 B1 — Skript (`docs/werkzeuge/db_sicherung/db_sicherung.sh`, Commit `e65e57c`)

- Findet `*.db` im Repo-Wurzelordner und unter `strategies/*/` und nennt sie im Protokoll.
- ⚠️ **Zählung weicht vom Auftrag ab:** Der Auftrag nennt „12 im Wurzelordner, 1 unter `strategies/volatility_breakout/`“. Gemessen: **11 im Wurzelordner** (9 `paper_trading_*`, `broker_testnet_t3_supertrend.db`, `benachrichtigungen_schliessung.db`) **+ 1 unter `strategies/volatility_breakout/` = 12 insgesamt.** Die zwölf aus TB-110 („12 `*.db` gleich“) sind diese Gesamtzahl. Die Datei unter `strategies/` ist **0 Byte**; ihre Sicherung ist eine leere SQLite-Datenbank (4096 B, `integrity_check ok`).
- Je Datei: `sqlite3 -readonly <db> ".backup '<zwischenkopie>'"`. Die Zwischenkopie liegt in einem eigenen `mktemp`-Ordner unter `$TMPDIR`, **nicht** im Ziel, damit eine Datei mit Schlüssel-Verdacht nie nach iCloud gelangt. Kein `cp`. `-readonly` ist eine Vorsicht über den Auftrag hinaus, denn die Originale werden nie schreibend geöffnet. Alle elf nicht leeren Datenbanken laufen im Rollback-Journal (Kopfbytes 18/19 = 1/1, kein WAL). Beim Lesen entstehen also keine `-wal`/`-shm`-Dateien neben dem Original.
- Schlüssel-Prüfung an der Zwischenkopie (B2), dann `mv -n` ins Ziel, `PRAGMA integrity_check` an der Kopie im Ziel, `sha256` in `SHA256SUMS`.
- Ziel `~/Library/Mobile Documents/com~apple~CloudDocs/trading-bot-db-sicherung/<JJJJ-MM-TT>/`, das **erste Argument ersetzt den Basisordner** (das Datum hängt weiter daran). Gibt es den Tagesordner schon, entsteht `<JJJJ-MM-TT>_<HHMMSS>/`: Ein zweiter Lauf am selben Tag überschreibt nichts.
- **Löscht nichts:** keine Sicherung, keine Datenbank, keine Zwischenkopie. Am Ende nur `rmdir` des eigenen, dann leeren Zwischenordners; das scheitert, wenn etwas darin liegt.
- Rückgabe 0 nur, wenn jede gefundene Datenbank gesichert und jede Kopie `ok` ist. Sonst 1, mit Dateinamen. Protokoll auf stdout und als `PROTOKOLL.txt` im Ziel. `PATH` ist fest gesetzt (für cron), `umask 077`.

### 2.2 B2 — Schlüssel-Prüfung (`b2_schema.sh`, `b2_schema.txt`)

Nur Schema der **Kopie** (`sqlite_master` + `pragma_table_info`): Tabellen- und Spaltennamen, nie ein Wert. Muster auf Spaltennamen: `key|secret|token|api|passw` (klein geschrieben verglichen).

- **0 Treffer in allen 12 Datenbanken** (170 Spaltennamen insgesamt, `sqlite_sequence` mitgezählt). Tabellen: `trades` (neun Bots), `gemeldet`/`zustand` (Benachrichtigung), `spiegelungen`/`versuche` (Brücke), `sqlite_sequence`.
- **Gegenprobe:** Wegwerf-Repo im Scratchpad mit `verdacht.db` (Spalte `api_key`) und `strategies/x/harmlos.db`. Ergebnis: `NICHT GESICHERT verdacht.db: Schluessel-Verdacht in 1 von 2 Spaltennamen: zugang.api_key`, rc 1. Im Ziel liegt nur `harmlos.db`, der Wert wurde nirgends ausgegeben und liegt nicht im Ziel.
- ⚠️ **Hinweis, kein Befund:** `benachrichtigungen_schliessung.db` hat die Tabelle `zustand(schluessel, wert)`. „Schlüssel“ auf Deutsch trifft das englische Muster nicht. Nachgesehen **im Code**, nicht in der Datenbank: Der einzige Schreiber ist `notifications/schliess_benachrichtigung.py:486`, und er schreibt nur die Marke `erstlauf_am` (Z. 154) mit einem Zeitstempel. Das ist ein Schlüssel-Wert-Speicher, kein Zugangsdatum. Gesichert; Frage 3 an den Betreiber bzw. Fable, ob das Muster deutsche Wörter (`schluessel`, `passwort`, `geheim`, `kennwort`) mitnehmen soll. Dann würde genau diese Datei zurückgehalten.

### 2.3 B3 — Test mit Testziel (`b3_test.sh`, `b3_test.txt`)

- Zwei Läufe hintereinander: Lauf 1 ⇒ `<testziel>/2026-09-26`, Lauf 2 ⇒ `<testziel>/2026-09-26_094721`, **je rc 0, je 12/12 `ok`, Laufzeit je 1 s**.
- Je Satz: `SHA256SUMS` 12 Zeilen, `shasum -c` 12 × OK, `integrity_check` erneut 12 × `ok`. Größe eines Satzes **368 KiB** (`du -sk`; Summe der Dateien 364 KiB).
- **Originale: sha256 und mtime aller 12 vorher = nachher.** Zum Sitzungsende (10:10) erneut gleich. Kein Cron schrieb dazwischen; die Brücke hatte `broker_testnet_t3_supertrend.db` zuletzt um 08:05 geändert (vor Sitzungsbeginn), die nächste Brücke läuft um 12:05.
- Zwischenordner `db_sicherung.*` in `$TMPDIR` vorher 0, nachher 0.
- ⚠️ **Abweichung:** Das Testziel liegt im **Scratchpad der Sitzung**, nicht unter `$TMPDIR`, und ist **nicht entfernt**. Der erste Aufruf mit `mktemp` unter `$TMPDIR` und `rm -rf` am Ende wurde vom Rechte-System abgelehnt. Das Scratchpad ist ein sitzungseigener Temp-Ordner.

### 2.4 B4 — echter Lauf nach iCloud (`b4_icloud.txt`)

`bash docs/werkzeuge/db_sicherung/db_sicherung.sh` ohne Argument, 09:48: **rc 0, 12/12 `ok`**, Ziel `~/Library/Mobile Documents/com~apple~CloudDocs/trading-bot-db-sicherung/2026-09-26/`, `shasum -c` 12 × OK, 368 KiB. **Kein „Operation not permitted“.** Das gilt aber für den Terminal-Prozess dieser Sitzung. Ob **cron** in den iCloud-Ordner schreiben darf, zeigt erst der erste Cron-Lauf; das LIESMICH sagt, was bei „Operation not permitted“ zu tun ist (Festplattenvollzugriff für `/usr/sbin/cron`).

### 2.5 B5 — `LIESMICH.md`

Zweck; was das Skript tut (Tabelle); Ziel und Satzgröße (~370 KiB, ein Jahr täglich ~130 MiB); **die eine Cron-Zeile**

```
20 5 * * * cd ~/trading-bot && /bin/bash docs/werkzeuge/db_sicherung/db_sicherung.sh >> logs/system/db_sicherung.log 2>&1
```

(05:20; `logs/` ist gitignoriert, `logs/system/` existiert); Festplattenvollzugriff; Zurückspielen in sechs Schritten (Bots anhalten, Satz prüfen, Original **umbenennen statt löschen**, mit `sqlite3 … .backup` zurückschreiben, `integrity_check`, Cron wieder an), mit dem Hinweis auf `DATENLUECKEN.md`. **Die Cron-Zeile ist nicht eingetragen.** Das tut der Betreiber, `crontab` wurde nicht aufgerufen.

## 3. Block C: `tb40_test_*` (`c_abnahme.sh`, `c_abnahme.txt`)

- `_trockenlauf_json` (`tb40_test_`, Z. 136) und `_loaderlauf_json` (`tb40_test_ll_`, Z. 192) entfernen ihren Ordner im `finally` nach dem Lesen des JSON. Die Aufrufer benutzen nur das gelesene dict, nie einen Pfad im Ordner (per Textsuche geprüft).
- `_faltenplan()` (`tb40_test_fp_`, Z. 123) wird einmal gerechnet und von mehreren Teilen benutzt. Sein Ordner wird am Ende von `main()` entfernt: `main()` ruft jetzt `_main()` im `try`, im `finally` `_faltenplan_aufraeumen()`.
- `tb44_l_` (Z. 902, jetzt Z. 911): **war schon** per `try/finally shutil.rmtree` abgebaut, keine Änderung. `$TMPDIR` am Eingang: 0 `tb44_l_*`.
- **Abnahme mit eigenem, leerem `TMPDIR`** je Lauf:
  - vorher (Fassung HEAD, für den Lauf aus git geholt): **163/163**, danach **18 Einträge** (1 `tb40_test_fp_`, 5 `tb40_test_ll_`, 12 `tb40_test_*` ohne Unterpräfix);
  - nachher (neue Fassung): **163/163**, danach **0**. Gleiche Probenzahl, gleich grün.
- Im System-`TMPDIR` blieb die Zahl `tb40_test_*` während beider Läufe bei 492. Die Gesamtzahl der Einträge stieg während des Nachher-Laufs um 1; der Test lief mit eigenem `TMPDIR`, der Eintrag stammt also von einem gleichzeitigen Prozess (A5 lief parallel).
- Die 492 alten `tb40_test_*` im System-`TMPDIR` sind **nicht** gelöscht, nur gezählt.

## 4. Testreihe am Endstand (`d_tests.sh`, `d_tests.txt`)

Am Endstand `21f4cac`, Arbeitsbaum außerhalb `docs/` leer, ohne Modus-Variablen. **17 Testdateien, alle rc 0:**

| Datei | Ergebnis | Dauer |
|---|---|---|
| `test_faltenplan_neun` | 156/156 | 137 s |
| `test_erste_falte_trockenlauf` | 50/50 | 136 s |
| `test_horizontbeginn` | 61/61 | 58 s |
| `test_min_history` / `test_volle_jahre` | 14/14 / 7/7 | 1 s |
| `test_universum_trockenlauf` | **163/163** (neue Fassung) | 94 s |
| `test_zwischenablage` | 12/12 | 2 s |
| `test_paths` / `test_strategy_paths` | 35/35 / 27/27 | 11 / 12 s |
| `test_nulltrades_modus` / `test_rueckfaelle_modus` | 34/34 / 48/48 | 28 / 38 s |
| `test_ergebniskurven` | 44/44 | 30 s |
| `test_startpruefungen` | **44/44** | 12 s |
| `test_main_gegenprobe` | 13/13 | 2 s |
| **`test_arbeitsbaum_laufbereich`** (neu) | **26/26** | 17 s |
| `test_ersatzwerte` | 40/40 | 20 s |
| `test_vorregistrierung` | **196/196** | 868 s |

`$TMPDIR` vor und nach der ganzen Reihe gleich: `tb40_lauf_` 4765, `tb40_faltenplan_` 70, `tb40_proben_` 108, **`tb40_test_*` 492 ⇒ 492** (vor Block C wären es +18 gewesen), `tb44_l_` 0, `tb112_klon_` 0.

## 5. Hashes und Stand nachher

- **Geändert außerhalb `docs/`** (`git diff --stat e731207..HEAD`): `shared/paths.py` (+49/−9), neu `shared/test_arbeitsbaum_laufbereich.py`, `research/universum_trockenlauf/test_universum_trockenlauf.py` (+48/−24). Alle drei freigegeben.
- **Unverändert:** alles unter `research/vorregistrierung/` (Sonde vorher = nachher, `register()` gleich), `shared/strategy_paths.py`, `regimewache.py`, alle `forward_test.py`/`live_params.py`/`equity_simulation.py`, die Cron-Wächter, Register und Sperrliste.
- **`*.db`:** alle 12 sha256 und mtime gleich (09:47 und 10:10); mtimes vor Sitzungsbeginn.
- `herkunft_protokoll.jsonl` existiert weiter nicht.
- `$TMPDIR`: keine neuen `tb112_klon_*` (der Test entfernt seinen Klon), `db_sicherung.*` 0.
- Liegen geblieben im Scratchpad (sitzungseigen): der A6-Klon, das B3-Testziel, das B2-Gegenprobe-Repo samt dessen Zwischenordner mit `verdacht.db` in `$TMPDIR` (eine Wegwerf-Datenbank mit Spalte `api_key` und dem Wert `NICHT-AUSGEBEN`, kein echtes Geheimnis).

## 6. Für Fable (ohne Kontext lesbar) ⭐⭐

**Stand.** Register 19 E2/F8 sind im Code vollzogen, nur unter dem Selektionsmodus. Die Sauberkeitsprüfung der Startprüfung (`git status --porcelain` beim Import von `shared/paths.py`) umfasst jetzt `shared/`, `strategies/`, `requirements.lock` und die **12 Module des Laufbereichs außerhalb** dieser Ordner, als Einzeldateien. `herkunft_protokoll.jsonl` ist namentlich ausgenommen (`:(exclude)`). Ohne Modus hat sich nichts geändert: 0 `git`-Aufrufe, 144 Pfade zeichengleich, 8 von 8 Werkzeugausgaben bytegleich. Im Modus: Benchmark `64fb2912` in Repo und frischem Klon, Trockenlauf 9 × rc 0, Sonde und `register()` unverändert.

**Nachweis.** Vorher (Eingangs-Commit, frischer Klon, Modus): eine uncommittete Änderung in `benchmark.py`, `faltenplan_neun.py` oder `manual_close.py` ließ den Import durchlaufen (rc 0). Nachher: jede der 12 Dateien einzeln ⇒ rc 2 mit Dateiname. Das Protokoll neu oder verändert ⇒ rc 0. `data/` und eine Ausgabe unter `ergebnisse/` ⇒ rc 0. Eine Gegenprobe liest die 81 Module aus der Messdatei und verlangt, dass jedes gedeckt ist; sie wird rot, sobald einer der 14 Code-Einträge fehlt. Das Lese-Audit der Modus-Läufe findet **0** gelesene `.py` unter der Codewurzel außerhalb der Liste.

**Der Schnitt.** Einzeldateien statt Ordner, weil `research/vorregistrierung/ergebnisse/` Laufausgaben aufnimmt (als Ordner geprüft: Mutation P1 zeigt rc 2 schon durch das Protokoll). Kosten: Ein neues Modul im Laufbereich ist ungeprüft, bis Liste und Messung nachgezogen sind. Die Gegenprobe fängt das nur gegen die jeweils letzte Messung. Einen besseren Schnitt sehe ich nicht.

**Fragen:**

1. **Eingaben außerhalb der Liste.** Das Audit findet 10 versionierte Dateien, die der Benchmark als **Daten** liest und die kein Pfad der Sauberkeitsprüfung deckt: `ergebnisse/messgroessen.json` (durch die Sonde gedeckt, Gruppe `eingefroren`) und die neun `research/tb24_haltedauern/daten/<bot>_alle_trades.csv` (von nichts gedeckt; sie gehen über die Faltenlängen in den Plan ein, TB-95). Eine uncommittete Änderung daran hielte die Startprüfung nicht an. Sollen die neun Listen in `ARBEITSBAUM_PFADE` (dann heißt die Liste „Laufbereich und seine versionierten Eingaben“) oder in das Abbild der Sperrliste? Oder bindet E2 bewusst nur Code?
2. **Pflege der Liste.** Die Liste ist eine Tatsache vom 26.09. und steht als Literal im Resolver; die Gegenprobe liest die Messdatei. Soll der Tag-Commit die Liste aus der Tag-Messung **erzeugen** (ein Schritt, der `paths.py` schreibt), oder bleibt es beim Literal mit Gegenprobe (heute gebaut)?
3. **Schlüssel-Muster der db-Sicherung.** Englisch nach 25f (`key|secret|token|api|passw`), 0 Treffer. Die Tabelle `zustand(schluessel, wert)` in `benachrichtigungen_schliessung.db` trifft es nicht; laut Code enthält sie nur `erstlauf_am` ⇒ Zeitstempel. Soll das Muster deutsche Wörter mitnehmen? Dann würde diese Datei zurückgehalten, bis der Betreiber entscheidet.

## 7. Abweichungen vom Auftrag

| | |
|---|---|
| 1 | **B1: 11 + 1 statt 12 + 1 Datenbanken.** Gemessen 11 im Wurzelordner und 1 (leer, 0 Byte) unter `strategies/volatility_breakout/`, zusammen 12 |
| 2 | **B3: Testziel im Scratchpad statt `$TMPDIR`, nicht entfernt.** `rm -rf` wurde vom Rechte-System abgelehnt |
| 3 | **B1: Zwischenkopie in `$TMPDIR`, dann `mv` ins Ziel** statt `.backup` direkt ins Ziel. Grund: B2 verlangt, eine Datei mit Schlüssel-Verdacht nicht zu sichern; direkt ins iCloud-Ziel kopiert, läge sie dort schon vor der Prüfung. `-readonly` zusätzlich |
| 4 | **B1: zweiter Lauf am selben Tag ⇒ `<JJJJ-MM-TT>_<HHMMSS>/`** (der Auftrag nennt nur `<JJJJ-MM-TT>/`). Sonst müsste ein zweiter Lauf überschreiben, und das Skript löscht nie |
| 5 | **A4: Die Messdatei `a2_laufbereich.txt` ist im Commit von A3/A4**, nicht erst bei den Belegen, weil der Test sie liest |
| 6 | **A5: Vorher-Lauf der 8 Ausgaben im Repo mit dem `paths.py` von `e731207`** (vorübergehend aus git geholt und zurückgelegt, per `cmp` bestätigt), nicht an einem Commit. Der Rest des Arbeitsbaums war in beiden Läufen gleich |
| 7 | **A6: Lese-Audit mit eigenem Skript** (`a6_code_audit.py`) auf den Protokollen des Hakens; `d_auswerten.py` (TB-109) kennt keine Klasse „Code“. Einteilung und Bytecode-Rückführung wie dort bzw. wie `d1_listen.py` |
| 8 | **A6 lief am Endstand `21f4cac`** (nach den Commits von A, B und C), nicht direkt nach dem Commit von A. B und C ändern keinen Pfad des Laufbereichs (Laufbereich am Endstand = A2) |

## 8. Was NICHT geschah

- Nicht angefasst: alles unter `research/vorregistrierung/` (nur gelesen), `shared/strategy_paths.py`, `regimewache.py`, `forward_test.py`/`live_params.py`/`equity_simulation.py`, die Cron-Wächter, Register und Sperrliste, der Worktree `../trading-bot-tb111`.
- **`crontab` nicht aufgerufen**, weder lesend noch schreibend. Die Cron-Zeile der db-Sicherung steht nur im LIESMICH.
- Keine `*.db` schreibend geöffnet; gelesen nur über `sqlite3 -readonly … .backup`, Schema und `integrity_check` an den Kopien.
- Keine alten `tb40_*`-Ordner gelöscht (nur gezählt).
- Kein neues Abbild, kein Registereintrag (Register 44 folgt).

---

## In einfacher Sprache

Bevor das Programm im geschützten Auswahlmodus rechnet, prüft es, ob sein Code genau dem eingecheckten Stand entspricht. Bisher schaute es dabei nur in zwei Ordner. Zwölf Programme, die im Lauf wirklich benutzt werden, lagen außerhalb, und eine Änderung daran wäre unbemerkt geblieben. Das ist jetzt geschlossen, einzeln Datei für Datei. Die eine Protokolldatei, die während des Laufs wachsen muss, ist ausdrücklich ausgenommen. Im normalen Betrieb ändert sich dadurch nichts; das ist nachgemessen. Dazu gibt es ein kleines Sicherungsskript. Es kopiert die zwölf Datenbanken mit den Papier-Handelsdaten nach iCloud, prüft jede Kopie und legt Prüfsummen daneben. Ein erster Lauf hat funktioniert. Täglich läuft es erst, wenn der Betreiber die eine Zeile in den Zeitplan einträgt. Und ein Test räumt seine Zwischenordner jetzt selbst auf.

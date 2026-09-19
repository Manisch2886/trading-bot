# TB-58 — Die Startprüfungen des Selektionsmodus

**Sitzung 19.09.2026, Mac** (`Darwin`, `trading-env/bin/python3` 3.9.6), Zweig `main`,
Basis `624853b`, Ergebnis **`d852bce`** (Lock) und **`6518e41`** (Startprüfungen), beide gepusht.
Sicherungsordner `~/Sicherungen/tb58_startpruefungen_20260919T144616Z/`,
ZIP `~/Downloads/TB-58_startpruefungen.zip`.

---

## Die Kurzfassung

| | |
|---|---|
| ⭐⭐ **SHA-256 der `requirements.lock`** | **`96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5`** — **67 Pakete**, `pandas==2.3.3`, `numpy==2.0.2`, `pandas-market-calendars==4.6.1`; Kopf: `3.9.6 (default, Apr 30 2025, 02:07:18) [Clang 17.0.0 (clang-1700.0.13.5)]`, `macOS-15.7.9-x86_64-i386-64bit`, `x86_64` — gemessen, nicht abgeschrieben |
| ⭐⭐ **Ohne Modus: null `git`-Aufrufe, null Paketabfragen — womit belegt?** | **0 / 0 / 0** mit einer zählenden Attrappe, die `subprocess.run/Popen/call/check_call/check_output`, `importlib.metadata.version/distribution/distributions/metadata` und `os.system/popen` **vor** dem Import ersetzt (Probe N1); dazu am Syntaxbaum: kein Import von `subprocess`/`importlib`/`platform`/`hashlib` auf Modulebene (N3, B5); dazu **144 Pfade über 9 Bots zeichengleich** gegen `624853b` (N4, A7/B3). Mutation (ein `git rev-parse` und ein `metadata.version` im Import): Attrappe zählt **2 / 2** — die Probe beisst |
| ⚠️ **Beissen alle Proben 4–8 einzeln, geht jede ohne ihre Prüfung durch?** | **Ja, alle.** Falscher Commit rc 2 / ohne HEAD-Prüfung rc 0 · fehlende Variable rc 2 / mit stillem HEAD-Rückfall rc 0 · gespaltener Baum rc 2 (beide Wurzeln genannt) / ohne Bedingung 1 rc 0 · schmutziger Baum rc 2 (Datei genannt) / ohne Bedingung 3 rc 0 · verfälschte Lock-Zeile rc 2 („pandas: Lock 0.0.1, installiert 2.3.3") / ohne die Prüfung rc 0. **44 / 44** in `shared/test_startpruefungen.py`, und **9 / 9** gegen den echten Arbeitsbaum (`nachweise_echt.py`) |
| **Wohin schreibt der Lauf die Auditzeilen, wie holt das Lese-Audit sie ab?** | **`stderr`, acht Zeilen `[paths] <schlüssel> <wert>`** direkt nach `[paths] SELEKTIONSMODUS AKTIV`, feste Reihenfolge (`AUDIT_SCHLUESSEL`); dieselben Werte über **`paths.startpruefung()`** (dict) und **`paths.audit_zeilen()`** (die Textzeilen — **eine** Funktion schreibt und liefert, nicht zwei) |
| **Sperrklinken und Basislauf gewachsen?** | Wanduhr **6 → 6**, eigener Pfadbau **29 → 29** (beide GRUEN vorher und nachher). Basislauf vorher **60/5/1/3/1 = 70, UNERWARTET 0**; nachher ****61/5/1/3/1 = 71, UNERWARTET 0** (16:47–17:17 UTC; einziger Unterschied `+ [OK] shared/test_startpruefungen.py`; `test_log_rotation` heute in beiden Läufen grün)** |
| **Datenstand vorher = nachher** | `d9449faf…`/**223** ✅ · Snapshot `--pruefen` **UNVERAENDERT** vorher und nachher · Registerprüfer **KEIN BEFUND** vorher und nachher |

> ⚠️⚠️ **Der eine Punkt, der nicht innerhalb der Freigabe ausführbar war:** Teil B
> wörtlich macht die bestehenden Modus-Proben in `shared/test_paths.py` (18/24) und
> `shared/test_strategy_paths.py` (18/23) rot — sie setzen nur zwei Variablen, starten
> mit `python -c` (kein `__file__`) und legen `paths.py` in einen Ordner ohne Git.
> Nachweis 13 verlangt „weiterhin grün". **Regel 6: gefragt, nicht entschieden.** Der
> Betreiber hat die Freigabe auf die **Aufrufumgebung** beider Dateien erweitert.
> Wortlaut der Rückfrage und Antwort stehen unten.

---

## Schritt −1 — Ortsprüfung (14:45:57 UTC)

| Prüfung | Soll | Ist |
|---|---|---|
| `uname -s` | `Darwin` | **`Darwin`** ✅ |
| `test -x trading-env/bin/python3` | 3.9.x | **3.9.6** ✅ |
| Arbeitsordner, Zweig | `~/trading-bot`, `main`, aktuell | `/Users/jaquelineloffler/trading-bot`, `main`, `HEAD` = `origin/main` = `624853b` ✅ |
| `git status --short` | 0 Zeilen | **0** ✅ (`logs/` ist gitignoriert — die Auftragsdateien unter `logs/auftraege/` erscheinen nicht) |
| Snapshot `63e4b6c8…cb2ceb2/MANIFEST.json` | vorhanden | **vorhanden** ✅ |

## Schritt 0 — Sichern und messen

| | Soll | Ist |
|---|---|---|
| `*.db` ausserhalb `trading-env/` | Quersummen + Kopie, gezählt | **12** (9 `paper_trading_*` in der Wurzel, `benachrichtigungen_schliessung.db`, `broker_testnet_t3_supertrend.db`, `strategies/volatility_breakout/paper_trading_volatility_breakout.db`); Kopien gegen `shasum -a 256 -c`: **12/12 OK** |
| Datenstand vorher (14:46:28 UTC, `--nur-hash`) | `d9449faf…`, 223 | **`d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, 223** ✅ |
| Snapshot `--pruefen` | `UNVERAENDERT` | **`UNVERAENDERT`**, rc 0 ✅ |
| Registerprüfer vorher (`--basis a1e7fb4`, A7) | KEIN BEFUND | **KEIN BEFUND**, rc 0 ✅ — **vor** jeder Änderung |
| Basislauf vorher (`--grenze 300`, 14:46–15:17 UTC) | Zahlen je Stufe | **grün 60 · rot 5 · flackernd 1 (heute grün) · ungeprüft 3 · Zeitgrenze 1 = 70, UNERWARTET 0** |
| Sperrklinken vorher | 6 / 29 | **6 / 29**, beide GRUEN |

Die fünf bekannten Roten wie in TB-53b (`dashboard/test_portfolio_sicht.py`,
`research/exposure_messung/test_exposure_kern.py`, `research/hrp_portfolio/test_hrp_core.py`,
`shared/test_stabile_sortierung.py`, `shared/test_wellenauswahl.py`).

---

## Teil A — Der Lock: geprüft, nicht erzeugt

**Der Entwurf** `logs/auftraege/requirements.lock.kandidat` (67 Pakete, aus den `dist-info`-Ordnern).
**Die Gegenprobe** `trading-env/bin/python3 -m pip freeze`, beide Seiten normalisiert
(Kleinschreibung, `_` → `-`):

| Schritt | Ergebnis |
|---|---|
| 1 | ⚠️ **Befund: `pip freeze` liefert 65 Zeilen, der Entwurf 67.** Nur im Entwurf: `pip==26.0.1`, `setuptools==58.0.4`. Nur in `pip freeze`: nichts. |
| 2 | **Benannt, nicht stillschweigend übernommen.** Ursache: `pip freeze` lässt `pip` und `setuptools` **absichtlich** aus (dokumentiertes Verhalten; `--all` nimmt sie mit). Mit `pip freeze --all`: **67 Zeilen, Unterschied leer in beide Richtungen.** Dritter, unabhängiger Weg `importlib.metadata.distributions()`: **67, Unterschied leer.** Die Schreibweise unterscheidet sich in 10 Zeilen (`APScheduler`/`apscheduler`, `pandas_market_calendars`/`pandas-market-calendars`, …) — Normalisierung, kein Unterschied. ⭐ Der Entwurf ist damit von **zwei** anderen Wegen bestätigt: eine Messung, keine Behauptung. |
| 3 | Kopfzeilen **gemessen**: `interpreter_voll  3.9.6 (default, Apr 30 2025, 02:07:18) [Clang 17.0.0 (clang-1700.0.13.5)]` (der Zeilenumbruch in `sys.version` auf ein Leerzeichen gefaltet — so vergleicht auch Teil C), `plattform  macOS-15.7.9-x86_64-i386-64bit`, `maschine  x86_64`. `pyvenv.cfg`: `version = 3.9.6` ✅ |
| 4 | `# ENTWURF …` entfernt; Herkunft: *„aus `pip freeze --all`, gegengeprüft gegen die dist-info-Ordner … und gegen importlib.metadata — drei unabhängige Wege, 0 Unterschiede"*; dazu drei Zeilen, **wer diese Datei wann prüft** (Teil C) |
| 5 | `requirements.lock` im Projektwurzelverzeichnis, **83 Zeilen** (16 Kopf, 67 Pakete), Commit **`d852bce`** |
| 6 | ⭐ **SHA-256: `96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5`** |

Gegenprüfung der genannten Zahlen: 67 Pakete ✅ · `pandas==2.3.3` ✅ · `numpy==2.0.2` ✅ ·
`pandas-market-calendars==4.6.1` ✅ · `version = 3.9.6` ✅. `requirements.txt` **unverändert**
(⚠️ sie hat **zwei `-r`-Zeilen und eine `>=`-Zeile**, nicht „drei Zeilen, alle `>=`" — Beobachtung, kein Befund).

---

## Teile B–D — Was in `shared/paths.py` steht (Commit `6518e41`, 356 / 1)

**Alles Neue liegt im `else`-Zweig** (Modus gesetzt) bzw. in Funktionen, die nur von dort
gerufen werden. `subprocess`, `importlib.metadata`, `platform`, `hashlib` werden **innerhalb**
der Funktionen importiert — der Regelfall bezahlt nicht einmal den Import.

### Die dritte Variable

```
TB_SELEKTIONSCOMMIT   der erwartete Commit der Codewurzel, 7–40 Hex-Zeichen
```

Fehlt sie bei gesetzten anderen beiden → **rc 2** („Ein halb gesetzter Modus ist gefährlicher als
keiner"). Steht sie **allein** → `Selektionsfehler` wie bei jedem anderen halben Modus (rc 1, C5).
⚠️ **Zweignamen (`main`) werden abgewiesen** — eine bewegliche Referenz beschreibt keinen Zustand
(B3, Probe C3). Ein abgekürzter Commit (≥ 7 Zeichen) wird angenommen, wenn `HEAD` damit beginnt (C4).

### Teil B — Codeherkunft, drei Bedingungen, in dieser Reihenfolge

| # | Bedingung | Umsetzung | Verletzung |
|---|---|---|---|
| 1 | Einstiegspunkt und `paths.py` unter derselben Git-Wurzel | `sys.modules["__main__"].__file__` und `__file__`, beide `realpath`, beide `git rev-parse --show-toplevel`, Ergebnis `realpath` | rc 2, Meldung nennt **beide** Wurzeln. ⚠️ **`python -c`** hat kein `__file__` → rc 2 („kein Einstiegspunkt"; A2: nicht prüfbar ist nicht grün). Aufrufer in einem Ordner **ohne** Git → rc 2 |
| 2 | `HEAD` ist der erwartete Commit | `git rev-parse HEAD`, `startswith` auf den kleingeschriebenen Bezeichner | rc 2, Meldung nennt HEAD und Soll |
| 3 | Arbeitsbaum sauber | `git status --porcelain -- shared strategies requirements.lock` (`ARBEITSBAUM_PFADE`), **untracked zählt** | rc 2, Meldung nennt Zahl und die ersten drei Einträge |

⚠️ **Zu Bedingung 3, eine Entscheidung innerhalb des Wortlauts:** Der Auftrag sagt „mindestens
`shared/` und `strategies/`". Geprüft werden diese beiden **plus die Lock-Datei** (ein veränderter,
nicht eingecheckter Lock beschreibt genau die Umgebung, gegen die gleich geprüft wird). **Nicht** der
ganze Baum: `data/` ist versioniert und wird vom Abruf-Cron laufend verändert — ein Lauf, der aus
dem Snapshot liest, darf daran nicht scheitern (Probe A4: eine neue Datei unter `data/` stört nicht).
Die Liste steht als Konstante mit Begründung im Modul.

### Teil C — Lock

`requirements.lock` neben `shared/` (aus `BASE_DIR`). Kopfzeilen `interpreter_voll` gegen
`" ".join(sys.version.split())`, `plattform` gegen `platform.platform()`; jede `name==version`-Zeile
gegen **`importlib.metadata.version(name)`** (kein `pip`, kein Kindprozess). Abweichungen werden
**gesammelt**; die Meldung nennt die Zahl und die **ersten drei** (Probe L3: vier verfälscht → „4
Abweichung/en", drei genannt). Fehlt die Datei → rc 2 („nicht prüfbar ist nicht grün", L5); eine
`>=`-Zeile → rc 2 („ist kein Lock", L6). ⚠️ **Nichts wird installiert oder repariert.**
Mit `/usr/bin/python3` (gleiche 3.9.6, andere Pakete): **rc 2, 24 Abweichungen**, die ersten drei
„installiert NICHT" (Nachweis 8b).

### Rückgabewert 2

Die Prüffunktionen werfen `Startpruefungsfehler` (Unterklasse von `Selektionsfehler`); **beim Import**
fängt der `else`-Zweig ihn, schreibt `[paths] STARTPRUEFUNG VERLETZT - …` und `[paths] Abbruch mit
Rueckgabewert 2.` auf `stderr` und wirft **`SystemExit(RUECKGABEWERT_STARTPRUEFUNG)`**. ⭐ `SystemExit`
statt Exception, damit kein `except Exception` im Aufrufer den Abbruch in einen stillen Weiterlauf
verwandelt (D1). Der Wert steht **genau einmal** (Probe R1/R2: kein `SystemExit(<Literal>)`). Der
bestehende `Selektionsfehler` für Wurzel/Hash bleibt unverändert (rc 1 mit Traceback — `test_paths.py`
Probe D und `test_strategy_paths.py` Probe C messen das weiter).

### Teil D — Das Audit

Nach bestandener Prüfung schreibt der Import **acht Zeilen** auf `stderr`, in der Form der
`[paths] SELEKTIONSMODUS AKTIV`-Zeile, und hält die Werte in `_STARTPRUEFUNG`:

```
[paths] codewurzel          /Users/jaquelineloffler/trading-bot
[paths] commit              6518e413b17dd4b7f5c624549aa145f94fca3a96
[paths] arbeitsbaum         sauber
[paths] lock_sha256         96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5
[paths] interpreter         3.9.6 (default, Apr 30 2025, 02:07:18) [Clang 17.0.0 (clang-1700.0.13.5)]
[paths] plattform           macOS-15.7.9-x86_64-i386-64bit
[paths] snapshot_wurzel     /Users/jaquelineloffler/trading-bot/snapshots/63e4b6c8…cb2ceb2
[paths] snapshot_hash       63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
```

(gemessen gegen den echten Arbeitsbaum, `nachweise_echt.py`, Nachweis 3). **Abrufbar:**
`paths.startpruefung()` → dict mit genau diesen acht Schlüsseln (ohne Modus `None`);
`paths.audit_zeilen()` → die Textzeilen in fester Reihenfolge (ohne Modus `[]`). ⭐ **Dieselbe
Funktion** erzeugt die `stderr`-Zeilen — das spätere Lese-Audit übernimmt sie, ohne eine zweite
Fassung zu pflegen (Probe S6: `stderr`-Zeilen == `audit_zeilen()`).

---

## ⚠️⚠️ Die Rückfrage (Regel 6) — wörtlich

Gemessen im Wegwerf-Worktree, **bevor** der Arbeitsbaum angefasst wurde: mit dem Entwurf werden
`shared/test_paths.py` **18 / 24** (B1, B2, C1–C3, E1 rot) und `shared/test_strategy_paths.py`
**18 / 23** (B1–B3, D1, D3 rot).

**Frage der Sitzung:**

> Teil B wörtlich (Abbruch rc 2 bei fehlender TB_SELEKTIONSCOMMIT; Einstiegspunkt =
> `__main__.__file__`) macht die bestehenden Modus-Proben rot: shared/test_paths.py 18/24 (B1, B2,
> C1–C3, E1 rot) und shared/test_strategy_paths.py 18/23 (B1–B3, D1, D3 rot) — gemessen im
> Wegwerf-Worktree. Grund: beide setzen nur die zwei alten Variablen, starten mit `python -c` (kein
> `__file__`, keine Codewurzel) und test_paths.py legt paths.py in einen mkdtemp-Ordner ohne Git.
> Nachweis 13 verlangt aber „weiterhin grün", und beide Dateien sind nicht freigegeben. Wie soll ich
> vorgehen?
>
> 1. **Freigabe erweitern (Recommended)** — shared/test_paths.py und shared/test_strategy_paths.py
>    dürfen in ihrer AUFRUFUMGEBUNG angepasst werden: dritte Variable setzen, Einstiegsdatei statt
>    -c, Wegwerfbaum als Git-Repo mit Commit. Prüflogik der Proben bleibt, Wortlaut von Teil B bleibt
>    vollständig.
> 2. **Wortlaut abschwächen** — Startprüfungen greifen nur, wenn TB_SELEKTIONSCOMMIT gesetzt ist;
>    zwei Variablen = alter Modus ohne Codeherkunft. Widerspricht „Fehlt die Variable: Abbruch" und
>    lässt den halben Modus durch — nicht empfohlen.
> 3. **Nur Teil A, B–D abbrechen** — requirements.lock committen und melden (Teilerfolg); der Entwurf
>    für B–D bleibt im Sicherungsordner, keine Änderung an paths.py.

**Antwort des Betreibers:** „**Freigabe erweitern (Recommended)**".

**Was daraufhin in den beiden Dateien geändert wurde — nur die Aufrufumgebung:**

| Datei | `--numstat` | Änderung |
|---|---|---|
| `shared/test_paths.py` | 48 / 3 | `baue_baum` macht den Wegwerfbaum zu einem Git-Repo mit **einem** Commit, legt `abfrage.py` (die bisherige `-c`-Abfrage) und die echte `requirements.lock` hinein; `frage` startet `abfrage.py` statt `-c` und setzt `TB_SELEKTIONSCOMMIT` = HEAD des Baums, **nur wenn** Wurzel und Hash gesetzt sind (Probe D5 „nur eine Variable" bleibt damit, was sie war); Probe E schreibt das Kind als `kind.py` in den Baum. Entfernte Zeilen: die drei `-c`-Aufrufe. Docstring: ein Absatz |
| `shared/test_strategy_paths.py` | 59 / 1 | dasselbe für `baue_baum`/`frage`; für den **echten** Baum (nur ohne Modus gefragt) eine Wegwerf-Einstiegsdatei. Entfernte Zeile: der `-c`-Aufruf. Probe C (falscher Hash, `-c`) und E (Wegwerfbaum-Muster, `-c`) **unverändert** — dort wirft `paths.py` vor der Startprüfung bzw. läuft ohne Modus |

Beide danach **24 / 24** und **23 / 23** — im Worktree und im Arbeitsbaum.

---

## Schritt 3 — Der Nachweis

Zwei Werkzeuge: **`shared/test_startpruefungen.py`** (44 Proben, Wegwerf-Repos, jede mit
Mutationsgegenprobe — im Repo) und **`nachweise_echt.py`** (im ZIP; misst gegen den **echten**
Arbeitsbaum mit dem echten Snapshot und `HEAD` = `6518e41`). Je Messung **ein eigener Prozess**,
nie importiert (TB-40); der Einstiegspunkt ist immer eine **Datei**.

| # | Nachweis | Soll | Ist |
|---|---|---|---|
| 1 | Ohne Modus: `subprocess` / `importlib.metadata` / `os.system,popen` gezählt | 0 / 0 | **0 / 0 / 0** (N1); Namensraum von `paths` ohne `subprocess`/`platform`/`hashlib`/`metadata` (N2); Syntaxbaum ohne Modulebenen-Import (N3). Mutation: **2 / 2** |
| 2 | Ohne Modus: alle Pfade zeichengleich wie vor TB-58 | unverändert | **144 Pfade, 9 Bots, 0 Unterschiede** gegen `624853b` (N4, `pfadvergleich.vergleiche`); Mutation `daten_verstellt` → 27 Unterschiede. Echt: ohne Modus rc 0, `DATA_DIR = …/trading-bot/data`, **stderr leer**, `startpruefung() is None` |
| 3 | Vollständiger, richtiger Modus | rc 0, Audit | **rc 0**, `DATA_DIR` im Snapshot, **8 Auditzeilen** auf stderr == `audit_zeilen()` (S1–S7); Kindprozess erbt alle drei und geht durch (S8). Echt: rc 0, Zeilen oben |
| 4 | Falscher Commit | rc 2 | **rc 2**, stdout leer, Meldung nennt HEAD und Soll (C1). Mutation ohne HEAD-Prüfung: rc 0. Echt: rc 2 |
| 5 | Fehlende `TB_SELEKTIONSCOMMIT` | rc 2 | **rc 2**, „TB_SELEKTIONSCOMMIT fehlt" (C2). Mutation mit stillem HEAD-Rückfall: rc 0. Echt: rc 2 |
| 6 | Gespaltener Baum | rc 2 | **rc 2** aus einem **anderen** Git-Repo (Meldung nennt beide Wurzeln, G1) **und** aus einem Ordner **ohne** Git (G2); derselbe Aufrufer im Baum → rc 0 (G3). Mutation ohne Bedingung 1: rc 0. Echt: **rc 2 / 2**, beide Wurzeln genannt |
| 7 | Schmutziger Arbeitsbaum | rc 2, dann sauber | **rc 2** bei veränderter Datei unter `shared/` (A1), neuer Datei unter `strategies/` (A2), verändertem Lock (A3) — Meldung nennt die Datei; neue Datei unter `data/` stört **nicht** (A4); zurückgesetzt rc 0, `arbeitsbaum sauber` (A5). Mutation ohne Bedingung 3: rc 0. Echt: untracked `shared/tb58_unfertig.tmp` → rc 2 (genannt), entfernt → rc 0; `git status` danach 0 |
| 8 | Abweichendes Paket | rc 2, nennt Paket | **rc 2**, „pandas: Lock 0.0.1, installiert 2.3.3" (L1); nicht installiert → „installiert NICHT" (L2); vier → „4 Abweichung/en", drei genannt (L3); Interpreter-Kopfzeile (L4), fehlende Datei (L5), `>=` (L6). Mutation ohne die Prüfung: rc 0. Echt: `_pruefe_lock` gegen verfälschte Kopie nennt pandas; **`/usr/bin/python3` → rc 2, 24 Abweichungen** |
| 9 | B1: jede Probe mit Mutationsgegenprobe | alle beissen | **9 Mutationen, alle beissen** (N, N3, N4, S, C1, C2, G, A, L, R). Gegen die **alte** `paths.py` (`624853b`): **7 grün / 36 rot / 9 NICHT PRUEFBAR** — die Datei misst etwas |
| 10 | Eigener Prozess je Messung | — | ja (`subprocess.run`, Einstiegsdatei) |
| 11 | Sperrklinken | ≤ 6, ≤ 29 | **6 / 29**, GRUEN vorher und nachher |
| 12 | Basislauf nachher | keine neue rote/flackernde Stufe | **61/5/1/3/1 = 71, UNERWARTET 0** (16:47–17:17 UTC); Diff zum Vorher: `+ [OK] shared/test_startpruefungen.py`, sonst nur Laufzeiten |
| 13 | `test_paths.py`, `test_strategy_paths.py` | grün | **24 / 24**, **23 / 23** |
| 9b | die neun echten Bot-Einstiegspunkte | — | `_pruefe_codeherkunft(HEAD, strategies/<bot>/multi_symbol_optimise.py)`: **9 / 9** (Wurzel, HEAD, sauber) |

⚠️ **Zwei Proben waren im ersten Entwurf der Testdatei falsch gebaut** — benannt statt still
korrigiert (B1): die Mutation zu S6 liess `_zeile` ungebunden (`NameError` im Mutanten, rc 1 statt
0 — die Mutation prüfte den Mutanten, nicht das Modul; daraufhin schreibt `paths.py` die acht Zeilen
in **einer** `write`-Operation ohne Schleifenvariable), und L3 nahm die Kommentarzeile mit „(==)"
als Paketzeile. Beide Korrekturen im Test bzw. in einer Zeile von `paths.py`, dann 44 / 44.

---

## Schritt 4 — Einchecken

| Commit | Dateien (`--numstat`) | Entfernte Zeilen |
|---|---|---|
| **`d852bce`** | `requirements.lock` 83 / 0 | — |
| **`6518e41`** | `shared/paths.py` **356 / 1** · `shared/test_startpruefungen.py` 846 / 0 · `shared/test_paths.py` 48 / 3 · `shared/test_strategy_paths.py` 59 / 1 | `paths.py`: **eine** Docstring-Zeile (`**Wie er gesetzt wird: ueber zwei Umgebungsvariablen.**` → drei). Im Code **keine** entfernte Zeile — alles Neue ist Zusatz im `else`-Zweig und in neuen Funktionen |

`git status --short` vor jedem Commit: nur die jeweiligen Dateien. `add` + `commit` + `push` je in einem
Zug (18:44:49 und 18:46:04 CEST — **vor** dem stündlichen `elliott_wave`-Cron um 19:00). `HEAD` =
`origin/main`, `git status` danach **0 Zeilen**. Kein eigener Zweig, kein Pull Request.

---

## Zum Schluss

| | Soll | Ist |
|---|---|---|
| 1 | Datenstand am Ende | **`d9449faf…`/223** ✅ (17:17:51 UTC) |
| 2 | Jede gesicherte `*.db` byteweise identisch | **12 von 12** byteweise identisch ✅ (`shasum -a 256 -c`) — der stündliche `elliott_wave`-Cron um 19:00 CEST lief währenddessen und hat keine Datenbank verändert; der 4-h-Cron (20:00/20:05 CEST) lag nach der Messung |
| 3 | Snapshot `--pruefen` | **UNVERAENDERT**, rc 0 ✅ |
| 4 | Registerprüfer nachher | **KEIN BEFUND**, rc 0 ✅ (`--basis a1e7fb4`) |
| 5 | dieses Dokument | `docs/ERGEBNIS_TB-58_startpruefungen.md` |
| 6 | ZIP | `~/Downloads/TB-58_startpruefungen.zip` |

---

## Beobachtungen, die NICHT ausgeführt wurden

1. ⚠️ **`python -c` unter dem Modus ist jetzt rc 2.** Jedes Werkzeug, das den Modus setzt und dann
   mit `-c` importiert, bricht ab — gewollt (kein Einstiegspunkt, keine Codewurzel), aber neu.
   Betroffen wären `research/resolver_selektion/kindprozess.py` (misst mit `-c` unter dem Modus;
   nicht Teil des Basislaufs, `research/` nicht freigegeben) und jede künftige Ad-hoc-Messung.
2. ⚠️ **`__main__.__file__` relativ + `os.chdir` vor dem Import** ergäbe eine falsche Codewurzel.
   Python 3.9 setzt `__main__.__file__` absolut; ein Skript, das vor `import paths` das Verzeichnis
   wechselt, liegt heute nicht vor (nicht gemessen — Beobachtung).
3. **Bedingung 3 zählt untracked Dateien unter `shared/` und `strategies/`.** Ein Selektionslauf,
   der Ergebnisse dort ablegte, machte den **nächsten** Lauf rot. `RESULTS_DIR`/`LOGS_DIR` liegen
   unter `results/`/`logs/` (Wurzel) — heute kein Fall; D4: stabil aus Umständen.
4. `research/resolver_selektion/pfadvergleich.py` entfernt in `_messen` nur die **zwei** alten
   Variablen aus der Umgebung. Steht `TB_SELEKTIONSCOMMIT` allein in der Shell, wirft die neue
   `paths.py` einen `Selektionsfehler` und der Vergleich meldet `RuntimeError`. Das Werkzeug bleibt
   GRUEN (heute gemessen: 0 Unterschiede, Selbstprobe 18); `test_startpruefungen.py` räumt alle drei
   aus seiner eigenen Umgebung, bevor es den Vergleich aufruft.
5. **`test_strategy_paths.py` Probe F** (`_VERBOTENE_KONSTANTEN`) prüft am Syntaxbaum, dass
   `strategy_paths.py` keinen zweiten Resolver trägt — die Liste kennt `TB_SELEKTIONSWURZEL` und
   `TB_SELEKTIONSHASH`, **nicht** `TB_SELEKTIONSCOMMIT`. Ausserhalb der erweiterten Freigabe
   („Aufrufumgebung"), daher nicht ergänzt.
6. **`/usr/bin/python3` ist derselbe Build wie `trading-env/bin/python3`** (`sys.version` und
   `platform.platform()` identisch) — die Lock-Prüfung unterscheidet die beiden allein über die
   Pakete (24 Abweichungen). Interpreter- und Plattformzeile allein hätten hier nichts bemerkt.
7. `docs/UMGEBUNGEN.md` und der Kopf von `paths.py` (TB-52-Abschnitt) nennen den Modus weiter mit
   „zwei Umgebungsvariablen" an weiteren Stellen (`ERGEBNIS_TB-52`, Backlog T46.3). Nicht angefasst —
   Registertexte folgen als TB-58b.
8. Die `requirements.txt` hat zwei `-r`-Zeilen und eine `>=`-Zeile, nicht „drei Zeilen, alle `>=`".
9. `basislauf.py` hinterlässt weiterhin den bekannten `test_drawdown_beide_masse`-Enkelprozess nach
   der Zeitgrenze (TB-46b); nach beiden Läufen war heute **kein** `drawdown`-Prozess mehr da (`pgrep` leer).
10. **Der Aufrufer in der Rückfrage-Messung**: die 6 bzw. 5 roten Proben waren **alle** Modus-Proben;
    alle Proben ohne Modus blieben grün — die Zusicherung „ohne Modus ändert sich nichts" galt also
    schon beim ersten Entwurf.

## Was ausdrücklich NICHT passiert ist

| | |
|---|---|
| ✅ | **Ohne Modus kein `git`, keine Paketabfrage, kein Import** — gemessen (N1–N4) |
| ✅ | `shared/strategy_paths.py`, `shared/snapshot.py`, Sperrliste, `research/`, Registertexte, `requirements.txt` **unberührt** |
| ✅ | `data/` (223, `d9449faf…`), `snapshots/` (UNVERAENDERT), Bot-DBs (siehe „Zum Schluss") |
| ✅ | Kein Netzabruf ausser `fetch`/`push`, keine Order, **kein Bot-Lauf durch diese Sitzung**, kein `pip install` |
| ✅ | Kein `cat` auf Konfigurationsdateien, keine Umgebungsvariablen ausgegeben; `pip freeze` nur Paketnamen und Versionen |
| ✅ | Der Arbeitsbaum wurde für die Nachweise nur mit **zwei untracked Dateien** für Sekunden berührt (`tb58_lauf.py` an der Wurzel, `shared/tb58_unfertig.tmp`), beide im `finally` entfernt; `git status` danach 0 |
| ✅ | Der Wegwerf-Worktree (`git worktree add --detach`) wurde nach Gebrauch entfernt; `git worktree list` zeigt nur den Arbeitsbaum |
| ✅ | **Kein Registertext** |

---

## In einfacher Sprache

**Was gemacht wurde.** Zwei Dinge. Erstens gibt es jetzt eine Datei, die **genau** aufschreibt, welche
Programmbibliotheken in welcher Fassung installiert sind — 67 Stück, auf drei voneinander unabhängigen
Wegen ermittelt, alle drei sagen dasselbe. Zweitens prüft der Auswahllauf beim Start selbst, dass sein
Programmcode aus **einem** Ordner kommt, dass dieser Ordner **genau** auf dem festgehaltenen Stand ist,
dass **nichts Unfertiges** darin herumliegt und dass die Umgebung **genau** die aufgeschriebene ist.
Stimmt eines davon nicht, hört der Lauf mit einer klaren Meldung auf. Er repariert nichts, er macht
nicht trotzdem weiter. Geht alles durch, schreibt er acht Zeilen auf, die zusammen sagen: dieser Code,
diese Umgebung, diese Daten.

**Was dabei aufgefallen ist.** Die vorbereitete Liste hatte 67 Einträge, `pip freeze` nur 65 — weil
`pip freeze` zwei Pakete absichtlich weglässt. Das wurde benannt und mit `--all` und einem dritten Weg
aufgelöst: 67, 67, 67. Und: die bestehenden Prüfprogramme setzten den Modus noch mit zwei Variablen und
starteten ohne Datei — mit der neuen Startprüfung wurden sie rot.

**Wie entschieden wurde.** Nicht von der Sitzung: nachgefragt. Der Betreiber hat gewählt, die
Aufrufumgebung der beiden Prüfprogramme anzupassen — was sie prüfen, blieb gleich. Danach: alle
Prüfprogramme grün, eines mehr (das neue mit 44 Proben), und im Normalbetrieb — ohne den Schalter —
tut das Programm **nichts** Neues: kein `git`, keine Paketabfrage, alle 144 Pfade Zeichen für Zeichen
wie vorher. Das ist gemessen, nicht angenommen.

**Was nicht passiert ist.** Keine Kursdatei, kein Snapshot, kein Registertext verändert; keine Order;
kein Bot von Hand gestartet. Alle zwölf gesicherten Datenbanken sind am Ende Byte für Byte gleich wie am Anfang.

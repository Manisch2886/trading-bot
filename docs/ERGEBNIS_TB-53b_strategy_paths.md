# TB-53b — `strategy_paths.py` an den Resolver

**Sitzung 19.09.2026, Mac** (`Darwin`, `trading-env/bin/python3` 3.9.6), Zweig `main`,
Basis `eaf2572`, Ergebnis **`29016cf`** (gepusht). Sicherungsordner
`~/Sicherungen/tb53b_strategy_paths_20260919T085518Z/`, ZIP `~/Downloads/TB-53b_strategy_paths.zip`.

---

## Die Kurzfassung

| | |
|---|---|
| ⭐⭐ **Wurzeln bei allen neun Bots gleich?** | **Ja — 9 von 9 zeichengleich**, gemessen vor der Änderung (Schritt 1), je Bot ein Prozess, mit `trading-env` **und** `/usr/bin/python3` |
| ⭐⭐ **… und im Quelltext zugesichert?** | ⚠️ **Nicht in der wörtlichen Form** — siehe „Die Entscheidung". Zugesichert ist im Quelltext, dass das antwortende `paths.py` **neben** `strategy_paths.py` liegt (`Resolverfehler`); die Wurzelgleichheit der neun Bots misst `shared/test_strategy_paths.py` Probe E1 bei jedem Lauf |
| ⭐ **Ohne Modus: alle neun `DATA_DIR` zeichengleich wie vorher?** | **9 / 9** (`CONFIG_DIR` ebenso 9/9; alle 7 Schlüssel × 9 Bots = 63 Pfade gegen `eaf2572`: **0 Unterschiede**) |
| ⭐ **Mit Modus: alle neun in der Snapshot-Wurzel?** | **9 / 9** in `snapshots/63e4b6c8…`; `RESULTS_DIR`/`LOGS_DIR`/`DB_FILE` bleiben im Repo (27 Werte, keiner im Snapshot) |
| ⚠️ **Falscher Hash beisst?** | **9 / 9** — `import strategy_paths` wirft `paths.Selektionsfehler`, **rc = 1**, nichts auf stdout |
| ⚠️ **`LIVE_DATA_DIR` wirft?** | **9 / 9** `Selektionsfehler`, unverändert aus TB-52 |
| **Wanduhr / eigener Pfadbau gewachsen?** | **Nein**: 6 → 6, 29 → 29 (beide GRUEN, rc 0) |
| **Basislauf: neue rote oder flackernde Stufe?** | **Nein** — vorher 59/5/1/3/1 = 69, UNERWARTET 0; nachher **60/5/1/3/1 = 70, UNERWARTET 0** (+1 grün = die neue Testdatei) |
| ⚠️ **Die zwei `os.makedirs` noch da?** | **Ja**, Zeilen 111–112, unangetastet |
| **`shared/test_paths.py`** | **24 / 24** weiterhin |
| **Neue Tests** | `shared/test_strategy_paths.py`: **23 / 23**, jede Probe mit Mutationsgegenprobe; gegen die alte Fassung **14 rot** (nicht blind) |
| **Datenstand vorher = nachher** | `d9449faf…`, **223** ✅ · Snapshot `--pruefen` **UNVERAENDERT** vorher und nachher · Registerprüfer **KEIN BEFUND** vorher und nachher |

> ⚠️⚠️ **Der eine Punkt, der nicht wie geschrieben ausgeführt wurde:** Die
> wörtliche Zusicherung „Wurzel des Aufrufers == Wurzel des Resolvers" hat im
> Basislauf **vier Tests unerwartet rot** gemacht und eine bekannte Rote verändert.
> Nach Regel 6 wurde **gefragt, nicht entschieden**; der Betreiber hat die
> Nachbar-Prüfung plus zwei Einzeiler in zwei Tests gewählt. Freigegeben waren
> damit **vier** Dateien statt einer. Alles Weitere unten.

---

## Schritt −1 — Ortsprüfung

| Prüfung | Soll | Ist |
|---|---|---|
| `uname -s` | `Darwin` | **`Darwin`** ✅ |
| `test -x trading-env/bin/python3` | 3.9.x | **3.9.6** ✅ |
| Arbeitsordner, Zweig | `~/trading-bot`, `main`, aktuell | `/Users/jaquelineloffler/trading-bot`, `main`, `HEAD` = `origin/main` = `eaf2572` ✅ |
| `git status --short` | 0 Zeilen | **0** ✅ |
| Snapshot `63e4b6c8…cb2ceb2/MANIFEST.json` | vorhanden | **vorhanden** ✅ |

## Schritt 0 — Sichern und messen

| | Soll | Ist |
|---|---|---|
| `*.db` ausserhalb `trading-env/` | Quersummen + Kopie, gezählt | **12** (9 `paper_trading_*` in der Wurzel, dazu `benachrichtigungen_schliessung.db`, `broker_testnet_t3_supertrend.db`, 0-Byte-`strategies/volatility_breakout/paper_trading_volatility_breakout.db`); Kopien gegen `shasum -a 256 -c`: **12/12 OK** |
| Datenstand vorher (08:55:24 UTC) | `d9449faf…`, 223 | **`d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, 223** ✅ |
| Snapshot `--pruefen` | `UNVERAENDERT` | **`UNVERAENDERT`**, rc 0 ✅ |
| Registerprüfer vorher (`--basis a1e7fb4`, A7) | KEIN BEFUND | **KEIN BEFUND**, rc 0 ✅ — **vor** jeder Änderung |
| Basislauf vorher (`--grenze 300`, 08:57–09:27 UTC) | Zahlen je Stufe | **grün 59 · rot 5 · flackernd 1 (heute grün) · ungeprüft 3 · Zeitgrenze 1 = 69, UNERWARTET 0** |

Die fünf bekannten Roten: `dashboard/test_portfolio_sicht.py`,
`research/exposure_messung/test_exposure_kern.py`, `research/hrp_portfolio/test_hrp_core.py`,
`shared/test_stabile_sortierung.py`, `shared/test_wellenauswahl.py` — alle mit
`BEKANNT_ROT`-Einordnung, wie im TB-52-Maclauf.

---

## Schritt 1 — Die Gleichheit der Wurzeln, gemessen bevor umgestellt wurde

Werkzeug `wurzelgleichheit.py` (im ZIP): je Bot **ein eigener Prozess**, der
`sys.path` genau wie `strategies/<bot>/multi_symbol_optimise.py` (Zeilen 16–19)
aufbaut, die **echte** `get_strategy_paths()` mit dem Pfad dieser Datei aufruft und
`paths` importiert. Vergleich mit `==`, also **zeichengleich**, nicht „gleicher Ordner".

| Bot | `base_dir` (aus dem Aufrufer) | `paths.BASE_DIR` | |
|---|---|---|---|
| alle neun | `/Users/jaquelineloffler/trading-bot` | `/Users/jaquelineloffler/trading-bot` | **gleich** |

**9 von 9** — mit `trading-env/bin/python3` **und** mit `/usr/bin/python3` (beide 3.9.6).
`DATA_DIR` und `CONFIG_DIR` beider Quellen ebenfalls 9/9 gleich; das antwortende
`paths.__file__` ist bei allen neun `…/trading-bot/shared/paths.py`.

⚠️ Vor der Messung wurde nachgesehen, dass `results/<bot>/` und `logs/<bot>/` für
alle neun existieren — der Aufruf legt sonst Ordner an. `git status` blieb bei 0.

---

## Schritt 2 — Die Änderung, und die Entscheidung dazu

### Was in `get_strategy_paths()` anders ist

```python
import paths                                   # ⚠️ über den Modulnamen, nicht den Dateipfad
…
"DATA_DIR": paths.DATA_DIR,                    # vorher: os.path.join(base_dir, "data")
"CONFIG_DIR": paths.CONFIG_DIR,                # vorher: os.path.join(base_dir, "config")
```

**Kein zweiter Resolver**: keine Umgebungsvariable, kein Manifest, kein Hash, kein
eigener `Selektionsfehler` — Probe F misst das am Syntaxbaum (B5), Mutation mit einer
eigenen `os.environ`-Lese beisst. `RESULTS_DIR`, `LOGS_DIR`, `DB_FILE` und die zwei
`os.makedirs` sind unangetastet.

**Warum `import paths` und nicht ein Laden über den Dateipfad:** nur so ist es
**dasselbe Modulobjekt** wie bei `symbols_config` und den Abrufskripten im selben
Prozess. Ein zweites Modulobjekt hätte einen eigenen `Selektionsfehler`-Typ (den ein
`except paths.Selektionsfehler` nicht fängt) und schriebe die Modus-Zeile zweimal.

### ⚠️⚠️ Die Entscheidung: Wurzelprüfung wörtlich — und was sie rot machte

Der erste Kandidat trug die Zusicherung **wörtlich** (`if base_dir != paths.BASE_DIR:
raise Wurzelfehler`). Vor dem Einspielen in den Arbeitsbaum lief er in einem
Wegwerf-`git worktree` (alle Proben grün), danach im Arbeitsbaum mit vollem Basislauf
(09:28–09:55 UTC). Ergebnis: **56/9/1/3/1 = 70, UNERWARTET 4** — vier Tests, die vorher
grün waren, plus eine veränderte bekannte Rote. **Zwei verschiedene Mechanismen:**

| Test | Mechanismus | Grund |
|---|---|---|
| `shared/test_determinismus.py` | **(1) Wurzelfehler** | `determinismus_lauf.py --basis <tmp>` lädt eine Bot-Kopie aus einem Wegwerfbaum mit der **echten** `shared/` auf `sys.path` |
| `shared/test_ladeprotokoll.py` | **(1) Wurzelfehler** | kopiert den Bot-Ordner nach `<tmp>/strategies/<bot>`, Symlinks auf `data/`/`config/`, echte `shared/` — 9 × „beide Laeufe gehen durch" rot |
| `shared/test_wellenauswahl.py` (bekannt rot, 1 Fehler) | **(1) Wurzelfehler** | Mutanten liegen in `<tmp>/strategies/<name>/`, geladen mit der echten `shared/`; **stürzte nach 1,3 s ab** statt wie bekannt mit 1 Fehler durchzulaufen (90 s) |
| `shared/test_entscheidungskerze.py` | **(2) `paths` fehlt** | Mini-Projekt kopiert `strategy_paths.py` **allein** nach `<tmp>/repo/shared/` — `import paths` → `ModuleNotFoundError`, der Bot im Abbild startet nicht |
| `shared/test_leeres_symbol.py` | **(2) `paths` fehlt** | dasselbe für die alte `zigzag_indicator.py` in `<tmp>/shared/` — 2 von 41 rot |

⭐ **Mechanismus (2) trifft jede Form**, in der `strategy_paths` den Resolver fragt:
wer die Datei allein kopiert, hat keinen Resolver daneben. Er ist innerhalb der
Freigabe „genau `strategy_paths.py`" nicht behebbar — ein stiller Rückfall auf den
eigenen Pfadbau wäre genau der zweite Resolver, den der Auftrag verbietet.

⭐ **Mechanismus (1) ist ein Muster dieses Projekts, kein Fehler:** drei Werkzeuge
bzw. Tests laden **absichtlich** eine Bot-Kopie aus einem Wegwerfbaum und nutzen die
echte `shared/` — Ergebnisse und Datenbank in der Kopie, Kursdaten aus dem Projekt.
Die wörtliche Wurzelprüfung verbietet genau das.

**Wortlaut (Regel 1, Bedingung 3) und Zweck (Nachweis 7: keine neue rote Stufe)
fielen auseinander → Regel 6: gefragt, nicht entschieden.** Der Arbeitsbaum war
währenddessen auf `HEAD` zurückgesetzt (Kandidat im Sicherungsordner), damit der
stündliche Cron den ungeprüften Stand nicht sah. Drei Wege standen zur Wahl:

1. ⭐ **Nachbar-Prüfung im Quelltext + zwei Einzeiler** — *gewählt.* Zugesichert wird,
   dass das antwortende `paths.py` **physisch neben** `strategy_paths.py` liegt
   (`os.path.realpath`, damit ein per Symlink eingebundenes `shared/` dieselbe ist);
   sonst `Resolverfehler`. Die Wurzelgleichheit der **neun echten Bots** wird in
   `test_strategy_paths.py` Probe E1 bei jedem Lauf gemessen. `test_entscheidungskerze.py`
   und `test_leeres_symbol.py` kopieren `paths.py` mit (1/1 bzw. 2/0 Zeilen).
2. Wörtliche Zusicherung + fünf Dateien (zusätzlich `test_wellenauswahl.py`,
   `test_ladeprotokoll.py`, Werkzeug `determinismus_lauf.py`) — nicht gewählt.
3. Abbruch, nur berichten — nicht gewählt.

**Was die Nachbar-Prüfung leistet und was nicht:** Ein fremdes `paths` (anderer Baum,
gleichnamiges Paket vor `shared/` auf `sys.path`) wirft mit einer Meldung, die beide
Orte nennt, statt still einen Pfad aus einem anderen Baum zu liefern (Probe E2/E3;
Mutation ohne die Prüfung liefert **still** `DATA_DIR` aus dem fremden Resolver, E5).
**Nicht** geprüft wird im Quelltext, ob der *Aufrufer* im selben Baum liegt — das ist
seit dem 19.09.2026 eine Messung (E1), keine Zusicherung. Das steht so im Kopf von
`strategy_paths.py`.

---

## Schritt 3 — Der Nachweis

Alle Messungen je Bot in **eigenen Prozessen**, nie importiert (TB-40). Werkzeuge im ZIP:
`wurzelgleichheit.py`, `nachweise_2_3_4.py`, dazu `shared/test_strategy_paths.py`.

| # | Nachweis | Soll | Ist |
|---|---|---|---|
| 1 | Ohne Modus: `DATA_DIR` je Bot vorher gegen nachher | 9/9 | **9/9** zeichengleich (`…/trading-bot/data`), `CONFIG_DIR` 9/9; Probe A1: **63 Pfade, 0 Unterschiede** gegen `eaf2572`; Mutation `daten_verstellt` → 9 Unterschiede |
| 2 | Mit Modus: `DATA_DIR` je Bot im Snapshot | 9/9 | **9/9** = `…/snapshots/63e4b6c8…`; `CONFIG_DIR` ebenso; `RESULTS_DIR`/`LOGS_DIR`/`DB_FILE` 27/27 im Repo; jeder der 9 Prozesse sagt `SELEKTIONSMODUS AKTIV` |
| 3 | Falscher Hash in `TB_SELEKTIONSHASH` | wirft, rc ≠ 0 | **9/9 rc = 1**, `paths.Selektionsfehler: … traegt den Hash 63e4b6c8…, TB_SELEKTIONSHASH nennt aber falscher_hash_0000`, stdout leer. Mutation „eigener Resolver" (SimpleNamespace ohne Hashprüfung): rc 0, `DATA_DIR` live — die Probe beisst |
| 4 | Mit Modus `LIVE_DATA_DIR` | `Selektionsfehler` | **9/9**, Meldung nennt Fundstelle und `DATA_DIR`; zusätzlich D2: kein Wert aus `get_strategy_paths()` zeigt unter dem Modus auf `data/` (0 Lecks; Mutation mit Zusatzschlüssel `LIVE_DATA_DIR` beisst) |
| 5 | Eigener Prozess je Bot | — | ja, in allen Werkzeugen und Proben (`subprocess.run`, `-c`) |
| 6 | Wanduhr ≤ 6, eigener Pfadbau ≤ 29 | nicht gewachsen | **6 / 29**, beide GRUEN vorher und nachher |
| 7 | Basislauf nachher gegen Schritt 0 | keine neue rote/flackernde Stufe | **60/5/1/3/1 = 70, UNERWARTET 0** (11:38–12:07 UTC); Diff zum Vorher: `+ [OK] shared/test_strategy_paths.py`, `test_log_rotation.py` flackernd heute rot (116/117 — das bekannte Muster) |
| 8 | `shared/test_paths.py` | grün | **24/24** |

Nachweise 1–4 wurden **auch mit `/usr/bin/python3`** gemessen: gleiche Zahlen.

**Zusätzlich:** `research/resolver_selektion/pfadvergleich.py` (TB-52) bleibt GRUEN, 0
Unterschiede — seine Selbstprobe findet jetzt **18** statt 9 Unterschiede, weil die
verstellte `paths.py` nun auch durch `strategy_paths` durchschlägt. Genau der Effekt,
um den es geht.

### Die 23 Proben in `shared/test_strategy_paths.py` (B1)

| Probe | prüft | Mutation | Ausgang ohne die Bedingung |
|---|---|---|---|
| **A** (3) | 63 Pfade alt/neu, Arbeitsbaum 9/9 | `paths.DATA_DIR` → `join(base_dir, "daten_verstellt")` | 9 Unterschiede |
| **B** (5) | Modus → Snapshot, Betrieb bleibt, stderr sagt es | `paths.DATA_DIR` → `join(base_dir, "data")` | `DATA_DIR` bleibt live |
| **C** (4) | falscher Hash: rc ≠ 0, `Selektionsfehler`, stdout leer | `import paths` → eigener `SimpleNamespace`-Resolver | rc 0, Pfad geliefert |
| **D** (3) | `LIVE_DATA_DIR` wirft; kein Leck im Ergebnis | Zusatzschlüssel `LIVE_DATA_DIR` | Live-Pfad im Ergebnis |
| **E** (5) | 9 echte Bots wurzelgleich; fremdes `paths` wirft; Werkzeugmuster läuft | `if not _resolver_ist_nachbar()` → `if False` | fremder Resolver liefert still |
| **F** (3) | kein zweiter Resolver (AST) | `os.environ.get("TB_SELEKTIONSHASH")` eingefügt | 2 Funde |

Gegen die **alte** `strategy_paths.py` (in einem Worktree): **8 von 22 bestanden, 14 rot,
6 × NICHT PRUEFBAR** — die Datei misst etwas.

Die Vorher-Messung in Probe A ist **inhaltsadressiert** (A7): `git show
eaf2572…:shared/strategy_paths.py`, Bezugscommit festgenagelt (B3).

---

## Schritt 4 — Einchecken

`git status --short` vor dem Commit: `M shared/strategy_paths.py`, `M shared/test_entscheidungskerze.py`,
`M shared/test_leeres_symbol.py`, `?? shared/test_strategy_paths.py` — **vier Dateien**, nach
der Entscheidung des Betreibers (Auftrag: eine plus Testdatei).

| Datei | `--numstat` | entfernte Zeilen |
|---|---|---|
| `shared/strategy_paths.py` | **89 / 2** | ⭐ `"DATA_DIR": os.path.join(base_dir, "data"),` und `"CONFIG_DIR": os.path.join(base_dir, "config"),` — ersetzt durch `paths.DATA_DIR` / `paths.CONFIG_DIR`. **Sonst keine.** Die zwei `os.makedirs` stehen. |
| `shared/test_strategy_paths.py` | neu, 602 Zeilen | — |
| `shared/test_entscheidungskerze.py` | 1 / 1 | die Kopierliste des Mini-Projekts: `"strategy_paths.py",` → `"strategy_paths.py", "paths.py",` |
| `shared/test_leeres_symbol.py` | 2 / 0 | `paths.py` wird neben `strategy_paths.py` in den Altbaum kopiert |

`add` + `commit` + `push` in einem Zug: **`29016cf`**, `HEAD` = `origin/main`,
`git status` danach **0 Zeilen**.

---

## Zum Schluss

| | Soll | Ist |
|---|---|---|
| 1 | Datenstand am Ende (12:08:39 UTC) | **`d9449faf…`/223** ✅ |
| 2 | Jede gesicherte `*.db` byteweise identisch | **11 von 12** ✅ — alle 9 `paper_trading_*` und `benachrichtigungen_schliessung.db` identisch. ⚠️ `broker_testnet_t3_supertrend.db`: **verändert durch den Cron `5 */4 * * *` (`broker/spiegel.py --echt`, 12:05 CEST)** — Tabelle `versuche` 345 → 351 Zeilen, `spiegelungen` 7 → 7; `logs/broker/cron.log`: „0 von 0 Spiegelung(en) (ECHT); 6 uebersprungen". Keine Order. Nicht von dieser Sitzung ausgelöst. |
| 3 | Snapshot `--pruefen` | **UNVERAENDERT**, rc 0 ✅ |
| 4 | Registerprüfer nachher | **KEIN BEFUND**, rc 0 ✅ |
| 5 | dieses Dokument | `docs/ERGEBNIS_TB-53b_strategy_paths.md` |
| 6 | ZIP | `~/Downloads/TB-53b_strategy_paths.zip` |

---

## Beobachtungen, die NICHT ausgeführt wurden

1. ⚠️ **Mass 2 (`test_eigener_pfadbau.py`) misst nach diesem Umbau semantisch Veraltetes.**
   Es zählt am Syntaxbaum die 29 `_P["DATA_DIR"]`-Bezüge der Selektionsmodule und nennt
   sie „Datenpfad aus `strategy_paths.py` — am Selektionsmodus vorbei". Seit `29016cf`
   gehen genau diese 29 **durch** den Resolver. Die Zahl bleibt 29 (die Module sind
   unverändert), die Deutung im Kopf von `masse.py`/`test_eigener_pfadbau.py` und der
   Satz „Keines der 90 Selektionsmodule importiert `shared/paths.py`" stimmen als
   Import-Aussage weiter, als Reichweiten-Aussage nicht mehr. `research/` war nicht
   freigegeben.
2. ⚠️ **Die zwei `os.makedirs` in `get_strategy_paths()`** (T46.8-Muster, TB-52-Beobachtung 2)
   stehen unverändert — wie verlangt nur berichtet. Sie greifen bei **jedem** Aufruf,
   auch aus Werkzeugen, die nur nachsehen wollen (`broker/bot_db.py` baut die
   DB-Namensregel deshalb nach, statt zu importieren).
3. ⚠️ **`CONFIG_DIR` zeigt unter dem Modus in den Snapshot** — jetzt auch für die 90
   Selektionsmodule. Richtig für die Symbollisten; `config/` enthält aber auch
   `email_config.py` und die Grössenfaktor-Datei. Ein Selektionslauf verschickt keine
   E-Mail (TB-52-Beobachtung 3), also heute kein Loch — aber D4: stabil aus Umständen.
4. **Drei Werkzeuge/Tests laden Bot-Kopien mit der echten `shared/`** (`determinismus_lauf.py
   --basis`, `test_ladeprotokoll.py`, `test_wellenauswahl.py`). Unter dem Modus lesen
   solche Kopien jetzt aus dem Snapshot — das ist gewollt. Wer das Muster je an die
   wörtliche Wurzelprüfung binden will, muss diesen drei Dateien einen eigenen
   `shared/`-Baum geben (Weg 2 oben).
5. **`test_leeres_symbol.py` zählt jetzt 45 statt 41 Prüfungen** — mit `paths.py` im
   Altbaum läuft die alte `zigzag_indicator.py`-Fassung wieder durch, und die zwei
   Bots liefern ihre vier Folgeprüfungen. Kein Befund, aber eine Zahl, die sich ändert.
6. `system/test_log_rotation.py` war im Basislauf nachher (beide Läufe) rot, 116/117 —
   das registrierte Flackern (~30 %), nicht dieser Umbau. Vorher heute grün.
7. **`ERGEBNIS_TB-52_resolver.md` und der Kopf von `paths.py` sagen „`strategy_paths.py`
   hängt nicht am Resolver"** — seit `29016cf` überholt. Registertexte und TB-52-Dokument
   wurden nicht angefasst.
8. Die Uhr: der Auftrag nennt keinen Zeitplan, aber der stündliche `elliott_wave`-Cron
   und `broker/spiegel.py` (alle 4 h) laufen mit dem Arbeitsbaum. Der ungeprüfte erste
   Kandidat lag deshalb nur 09:28–09:57 UTC im Arbeitsbaum (kein Cron-Lauf in dieser
   Zeit), während der Rückfrage war `HEAD` eingespielt; der geprüfte Stand ist seit
   11:30 UTC drin und der 12:00-UTC-Lauf des `elliott_wave`-Bots lief damit ohne
   Traceback.

## Was ausdrücklich NICHT passiert ist

| | |
|---|---|
| ✅ | **Kein zweiter Resolver** — Probe F misst es |
| ✅ | `shared/paths.py`, `shared/snapshot.py`, Sperrliste, `research/`, Registertexte **unberührt** |
| ✅ | `data/` (223, `d9449faf…`), `snapshots/` (UNVERAENDERT), alle 9 Bot-DBs byteweise gleich |
| ✅ | Kein Netzabruf ausser `fetch`/`push`, keine Order, **kein Bot-Lauf durch diese Sitzung** (die Cron-Läufe laufen von selbst) |
| ✅ | Kein `cat` auf Konfigurationsdateien |
| ✅ | Die zwei `os.makedirs` **nicht** angefasst |
| ✅ | Der Wegwerf-Worktree (`git worktree add --detach`) wurde nach Gebrauch entfernt, `git worktree list` zeigt nur den Arbeitsbaum |

---

## In einfacher Sprache

**Was gemacht wurde.** Die Hilfsdatei, über die alle 90 Auswahl-Programme ihre
Kursdaten finden, hat den Pfad bisher selbst zusammengesetzt — und zeigte damit immer
auf den laufenden Bestand, egal ob der Schalter für die eingefrorene Kopie stand.
Jetzt fragt sie die Stelle, die den Schalter kennt. Ist er aus (der Normalfall, auch
nachts im Cron), kommt für alle neun Bots **Zeichen für Zeichen derselbe Pfad wie
vorher** heraus — nachgemessen, nicht angenommen. Ist er an, zeigen alle neun in die
eingefrorene Kopie; ein falscher Kennwert bricht ab, und wer ausdrücklich nach den
lebenden Daten fragt, bekommt eine Fehlermeldung.

**Was dabei aufgefallen ist.** Der Auftrag wollte zusätzlich festschreiben, dass
Aufrufer und Pfad-Stelle immer im selben Ordnerbaum liegen. Das stimmt für alle neun
Bots — aber drei Prüfprogramme des Projekts legen absichtlich Kopien eines Bots in
einen Wegwerfordner und benutzen dazu die echte Hilfsdatei. Mit der wörtlichen
Festschreibung wären sie rot geworden. Zwei weitere Prüfprogramme kopieren die
Hilfsdatei allein in ein Mini-Projekt — dort fehlt dann die Stelle, die sie jetzt
fragen muss; das ist mit **keiner** Fassung des Umbaus vermeidbar.

**Wie entschieden wurde.** Nicht von der Sitzung: nachgefragt. Der Betreiber hat
gewählt, im Programm nur festzuschreiben, dass die *richtige* Pfad-Stelle antwortet
(die neben der Hilfsdatei), und die Gleichheit der neun Bot-Wurzeln bei jedem Testlauf
zu messen. Dazu zwei Einzeiler in den zwei Mini-Projekt-Tests. Danach: alle Tests des
Projekts genau wie vorher, einer mehr (der neue), keine unerwartete Röte.

**Was nicht passiert ist.** Keine Kursdatei, kein Snapshot, keine Bot-Datenbank
verändert; keine Order; kein Bot von Hand gestartet. Die einzige veränderte Datenbank
ist das Protokoll der Binance-Testnet-Brücke, das der planmässige Cron um 12:05
geschrieben hat — sechs übersprungene Spiegelversuche, keine Order.

# Backlog-Nachtrag 18.09.2026 (e) — TB-52

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
⚠️ **Setzt (a)–(d) voraus.** (a)–(c) sind eingearbeitet; **(d) liegt noch
uneingearbeitet im Repo** — ⭐ **(d) und (e) gehören in dieselbe Sitzung**, in
dieser Reihenfolge.

---

## Ersetzung — die Kette, Rang 0,85

**Zu finden** (Abschnitt 3 „Die Kette", die Zeile mit `0,85`):

⚠️ **Der Wortlaut kann abweichen** — massgeblich: **die Zeile mit `0,85`, die
von den 90 Selektionsmodulen spricht.**

**Zu ersetzen durch:**

```
| ~~0,85a~~ | ~~Resolver-Modus in `shared/paths.py` + zwei AST-Masse~~ | ⭐ **TB-52, Cloud fertig.** ⚠️ **Mac-Lauf und Merge offen.** Siehe Block **2k** |
| **0,85b** | ⭐ **TB-53 — die Selektionsseite auf den Resolver.** ⚠️ **NEU ZUZUSCHNEIDEN:** TB-52 hat gemessen, dass **keines der 90 Module `paths.py` importiert** und **71 von 90 ihre Pfade aus `shared/strategy_paths.py`** beziehen, das `DATA_DIR` selbst ableitet. **Erste Frage: bedient `strategy_paths.py` auch den Live-Pfad?** Wenn ja, braucht die Änderung dieselbe Zusicherung wie TB-52 | zu formulieren |
| **0,85c** | **TB-54 — Lese-Audit** als Gültigkeitsbedingung (Registertext 5e) · **Cache nach Snapshot-Hash UND Commit** (T46.7) | danach |
```

---

## Neuer Block 2k — aus TB-52

**Einzufügen NACH Block 2j.**

---

### 2k — Aus TB-52, Resolver und AST-Masse (Stand 18.09.2026)

**TB-52 ist in der Cloud fertig, Zweig `claude/new-session-7xve52`, Basis
`062bacf`.** ⚠️ **Mac-Lauf vor dem Merge.** Datenstand `d9449faf…`/223 vorher =
nachher, kein Snapshot, **genau eine bestehende Datei geändert**
(`shared/paths.py`, 246 +/4 −).

| # | Punkt |
|---|---|
| **T52.1** | ⭐⭐ **DIE BEDINGUNG DER FREIGABE IST ERFÜLLT: 99 Pfade über neun Bots, NULL Unterschiede** — beide Fassungen in je einem eigenen Prozess, gegen `062bacf`. ⭐ **Und der Vergleich wurde selbst mutationsgeprüft:** `"data" → "daten_verstellt"` in der alten Fassung ⇒ **9 Unterschiede, `gebissen: true`**. ⚠️ *Ohne diese Selbstprobe wäre „0 Unterschiede" nicht unterscheidbar von „der Vergleich hat nichts gemessen" — **A1***. Die fünf neuen Namen (`LIVE_DATA_DIR`, `LIVE_CONFIG_DIR`, `MANIFEST`, `UMGEBUNG_HASH`, `UMGEBUNG_WURZEL`) sind **Zugänge, keine Änderungen** |
| **T52.2** | ⭐ **Der Modus wird über ZWEI UMGEBUNGSVARIABLEN gesetzt, die den Snapshot-Hash tragen** (`TB_SELEKTIONSWURZEL`, `TB_SELEKTIONSHASH`). **Sieben Messungen an echten Unterprozessen:** Kind ohne Modus → Live ✅ · Kind mit Modus → Snapshot ✅ · **Enkel** → Snapshot ✅ · ⚠️ **prozesslokaler Modus → das Kind liest STILL den Live-Bestand, ohne Fehler, ohne Meldung** · ⭐ **Kind mit falschem Hash → `rc=1`, `Selektionsfehler`** · übriggebliebener Modus → meldet sich auf `stderr`. **Der prozesslokale Weg fällt damit gemessen aus, nicht vermutet** |
| **T52.3** | ⚠️ **Restrisiko, benannt statt versteckt:** eine Umgebungsvariable kann aus einer früheren Shell übrigbleiben. **Sie meldet sich dann** — aber sie verschwindet nicht von selbst. **Der Mac-Lauf prüft, ob der echte Cron sie nicht setzt** |
| **T52.4** | ⚠️⚠️⚠️ **DER BEFUND, DER GRÖSSER IST ALS DIE AUFGABE: KEINES der 90 Selektionsmodule importiert `shared/paths.py`.** Verteilung: **71 von 90** beziehen ihre Pfade aus **`shared/strategy_paths.py`** (42 ohne, 29 mit Datenpfad), 18 aus keiner der beiden Quellen, 1 nennt `DATA_DIR` ohne beide — ⭐ **0 über `paths.py`**. Und `strategy_paths.py:49` leitet selbst ab: `"DATA_DIR": os.path.join(base_dir, "data")`. ⚠️ **Der Modus wäre gesetzt, und alle 90 läsen weiter aus dem Live-Bestand — still.** *Fables Einwand eine Ebene höher: die Wache steht nicht dort, wo gefragt wird.* ⭐ **Das entwertet Schicht (1) nicht** — sie ist die Stelle, an der zentral umgebogen werden **kann**; dass heute niemand dort fragt, misst Mass 2, **bevor der Umbau stattfindet** |
| **T52.5** | ⭐ **FOLGE FÜR TB-53, und sie ist eine gute:** Der Umbau ist vermutlich **eine Datei statt neunzig.** `strategy_paths.py` an den Resolver zu hängen erledigt **71 von 90 auf einen Schlag** — *eine Stelle ist prüfbar, 90 richtige Kopien sind es nicht; und eine vergessene sieht aus wie eine erledigte.* ⚠️ **Vorher zu messen: bedient `strategy_paths.py` auch den Live-Pfad der neun Bots?** Wenn ja, braucht die Änderung dieselbe Zusicherung wie TB-52 — ohne Modus byteweise dieselben Pfade, über alle neun gemessen. **Nicht geraten** |
| **T52.6** | ⭐ **MASS 1 (Wanduhr): Ausgangszahl 6 — und Fables „wahrscheinlichste Falle" (T46.2) ist NICHT eingetreten.** Alle sechs liegen in `quarterly_review.py` von drei Bots, je zwei Zeilen, **beide schreiben einen Zeitstempel in einen Bericht**. ⭐ **Null im Datenschnitt**: keine kappt Historie, keine macht eine Frischeprüfung |
| **T52.7** | **MASS 2 (eigener Pfadbau): Ausgangszahl 29** — ⭐ **deckt sich mit der Erhebung aus TB-46.** ⚠️⚠️ **Und das ist der Grund, warum ein Beinahe-Fehler auffiel: Mass 2 meldete zuerst 127.** `RESULTS_DIR`/`LOGS_DIR`/`DB_FILE` galten fälschlich als nicht zentral bezogen, innere Syntaxbaumknoten wurden doppelt gezählt. ⭐ ***„Hätte niemand hingesehen, wäre 127 die festgeschriebene Ausgangszahl für TB-53 geworden"*** — **dann hätten 98 zusätzliche Verstösse unbemerkt unter der Sperrklinke Platz gehabt.** *Aufgefallen nur, weil die Erhebung im Repo 29 sagt* |
| **T52.8** | ⭐ **Die Masse sind Sperrklinken, keine Wachen:** grün, solange die Zahl nicht wächst; die Ausgabe nennt Ausgangszahl, heutigen Stand und **die Liste der Treffer mit Datei und Zeile**. **Wer die Sperrklinke aufdreht, steht als eigene Zeile im Diff.** Beide laufen **ohne Argument** (**A3**) und sind im Basislauf grün |
| **T52.9** | ⚠️ **DREI PROBEN WAREN IM ERSTEN ENTWURF FALSCH GEBAUT — benannt statt still berichtigt.** **(1)** `kindprozess.py` Messung 5: der Probeprozess **fing die Ausnahme selbst ab**, um sie melden zu können, und lieferte damit immer `rc=0` — geprüft wurde der Rückgabewert. **(2)** `test_paths.py` Probe E1 meldete „der Enkel erbt nicht" — in Wahrheit brach der Enkel mit `TypeError` ab, **leere Ausgabe wurde als Messergebnis gelesen**; sagt jetzt **NICHT PRÜFBAR**. **(3)** die 127 aus T52.7. ⭐ **Prüfprinzip A1 dreimal an einem Tag — gefunden, weil zwei Werkzeuge dieselbe Frage beantworteten und einander widersprachen (C2)** |
| **T52.10** | ⭐ **BASISLAUF: 53 grün / 11 rot / 1 flackernd / 3 ungeprüft / 1 Zeitgrenze = 69, 8 UNERWARTET — und alle acht sind gegengeprüft.** Jeder wurde zusätzlich in einem `git worktree` auf **`062bacf`** ausgeführt und ist **dort genauso rot**; Ursache durchweg fehlende Pakete dieser Cloud-Sitzung (`binance`, `yfinance`, `fastapi`, `tzdata`). ⭐ **Das ist die stärkste Form dieses Nachweises** — nicht „wird die Umgebung sein", sondern derselbe Test, derselbe Rechner, andere Codebasis. ⭐ **Und die Flackerstufe aus TB-51 arbeitet:** `system/test_log_rotation.py` steht als *flackernd, heute grün*, nicht als UNERWARTET |
| **T52.11** | ⭐ **T46.8 ist erledigt** — die beiden `os.makedirs`-Zeilen in `paths.py` sind entfernt, der Import legt **kein** Verzeichnis mehr an, mit eigener Probe an einem Wegwerf-Ordner. ⚠️ **ABER: `strategy_paths.get_strategy_paths()` legt bei JEDEM Aufruf `results/` und `logs/` an — dasselbe Muster, eine Datei weiter, dort nicht behoben** (nicht freigegeben). *Ein Import ist keine Leseoperation (**B6**)* |
| **T52.12** | ⚠️ **`CONFIG_DIR` zeigt unter dem Modus in den Snapshot.** Für die Symbollisten richtig — `config/` enthält aber auch `email_config.py`. **Heute kein Loch**, weil ein Selektionslauf keine E-Mail verschickt. ⭐ *Genau die Bauform aus **D4**: stabil aus Zufall der Umstände, nicht aus Entwurf* |
| **T52.13** | **Der Modus deckt `DATA_DIR`/`CONFIG_DIR` ab, nicht einzelne Dateinamen** — ein Modul, das eine Kursdatei **ausserhalb** von `data/` liest, sähe ihn nie. **Berichtet, nicht behoben** |

---

## Ergänzungen zu Abschnitt 4 („Laufend, klein")

| # | Punkt |
|---|---|
| **K1r** | ⚠️ **`strategy_paths.get_strategy_paths()` legt `results/` und `logs/` an** — T46.8-Muster, siehe **T52.11** |
| **K1s** | ⚠️ **`CONFIG_DIR` im Selektionsmodus umfasst `email_config.py`** — siehe **T52.12** |
| **K1t** | **Modus deckt Verzeichnisse ab, keine Einzeldateien** — siehe **T52.13** |

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — entfernte Zeilen **nur**
   aus der einen Kettenersetzung, zugeordnet.
2. ⚠️ **(d) zuerst, dann (e)** — (e) setzt Block 2j voraus.
3. `git status --short` vor dem Commit, `add`+`commit`+`push` in einem Zug,
   `git status` **danach**.

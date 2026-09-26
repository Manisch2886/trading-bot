# TB-113: Ergebnis. `tb-111` nach `main` zusammengeführt (`257e7db`, ohne Konflikt) und neu geprüft — Benchmark im Modus Repo und Klon `64fb2912…`, ohne Modus 8/8 bytegleich, Trockenlauf 9 × rc 0, 17 Testdateien grün; Register 44 (Tatsachennotizen TB-111/TB-112, 7 Marken, numstat 344/0, 13 Zitate `diff` rc 0); Arbeitsweise 22.1/22.9; Wächter `--effort high` committet; Worktree entfernt

**Sitzungstitel:** `TB-113` · **Stand:** 26.09.2026, ca. 15:45 · **Auftrag:**
`docs/auftraege/MAC_TB-113_zusammenfuehrung_tb111_register_44.md` · **Belege:** `docs/belege/TB-113/`
**Eingang:** `af6042f` (Abgabe TB-112) und Zweig `tb-111` auf `49f0868` (Abgabe TB-111). Commits: `656f04b` (Schritt 0),
`257e7db` (Merge), `dfc11a0` (Register 44 samt Marken), `e710bf9` (Arbeitsweise) und der Abgabe-Commit (Journal DK/DL, Belege,
dieses Dokument). Nach jedem Commit gepusht.
**Grundlage:** Ergebnisse TB-111 (Abschnitt 7 „Für die Zusammenführung“) und TB-112; Register 19, 36.5, 37.4, 42.2 E2,
42.3 F8, 43. Freigabe des Betreibers 26.09.2026, ca. 14:28 (Auswahlkarte, wörtlich im Auftrag).
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6), gestartet vom Wächter mit `claude --effort high --remote-control`.

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | Arbeitsbaum des steuernden Chats committet (`656f04b`; `starte_sitzung.sh` 1 Datei, 1/1 Zeile). `--effort` greift: `claude --help` kennt den Schalter, die eigene Prozesszeile lautet `claude --effort high --remote-control`. Vorbedingungen: Worktree-Index unverändert seit `49f0868` (08:26:20), Worktree sauber, `merge-tree` rc 0, Schnittmenge **0** (132 gegen 32 Dateien), kein zweites Abbild auf `main` |
| ⭐⭐ **A** | Merge `257e7db`, Baum `e44e1abf…` = Vorhersage von `merge-tree`. Nachgemessen: `herkunft.py` `5bbfc9e0…`, `auswertung.py` `a864b216…`, Abbild `e655c1c8…`; `register()` **`469272df…`** (weder `e7d82547…` noch `c92900a8…`); Sonde gegen `e655c1c8…` **25/0/0, (ii) 0**; Benchmark im Modus **Repo und frischer Klon `64fb2912…`**; ohne Modus **8/8 bytegleich**; Trockenlauf **9 × rc 0**; **17 Testdateien rc 0** (`test_vorregistrierung` 196/196, `test_ersatzwerte` 61/61, `test_startpruefungen` 44/44, `test_arbeitsbaum_laufbereich` 26/26). Wechselwirkung: `auswertung.py` ist von der Sauberkeitsprüfung gebunden, `herkunft.py` nicht |
| **B** | Journal **DK** (TB-111, wörtlich aus dem Ergebnis, nur `D?` ⇒ `DK`) und **DL** (dieser Auftrag) |
| ⭐⭐ **C** | Register **44** (44.0–44.4, Einträge 44-1 bis 44-12) und **7 Marken**: 19 · 36.5 · 37.4 · 42.2 E2 · 42.3 F8 · 43-1 · 43-4. numstat **344/0**, **13/13 Zitate** `diff` rc 0, Sonde vorher = nachher (byte-gleich), `register()` `469272df…` ⇒ **`a0e477fd…`**, `test_vorregistrierung` **196/196 rc 0** (952 s) |
| **D** | Arbeitsweise: Nachtrag unter **22.1** (Wächter startet mit `--effort high`, Beleg `0b_effort.txt`) und neuer Abschnitt **22.9** „Die Sitzung wird angelegt, bevor der Satz kommt“, mit dem Anlass aus dem Wächter-Log gemessen (2 h 28 min) |
| **E** | `git worktree remove ../trading-bot-tb111`; danach nur noch der Hauptordner. Zweig `tb-111` bleibt lokal und auf `origin` |

Kein Abbruchkriterium hat gegriffen.

---

## 0. Schritt 0

| | |
|---|---|
| 0a | `git status` am Eingang: genau die drei erwarteten Dateien. `git diff --numstat` auf `starte_sitzung.sh`: `1 1` (Zeile 327: `exec claude --remote-control` ⇒ `exec claude --effort high --remote-control`). Commit `656f04b` mit dem vorgegebenen Text, gepusht |
| 0b | `0b_effort.txt`: `claude` 2.1.283; `claude --help \| grep -c -- '--effort'` = **1** (`--effort <level>  Effort level for the current session`). ⚠️ Kopfzeile und `/status` sind aus der Sitzung heraus nicht lesbar (Slash-Befehle kann das Modell nicht auslösen). **Ersatzbeleg:** die Befehlszeile des Elternprozesses der Sitzungs-Shell, PID 32089, `claude --effort high --remote-control`. Der Schalter greift also beim Start; ob die Anzeige ihn nennt, hat hier niemand gesehen |
| 0c | `0c_vorbedingungen.txt`: `worktree list` zeigt beide Bäume; `.git/worktrees/trading-bot-tb111/index` mtime **08:26:20** = Commitzeit von `49f0868`; `status` im Worktree leer, kein Prozess mit offenem Pfad darin (`lsof +D`); `tb-111` = `origin/tb-111` = `49f0868`. `git merge-tree --write-tree main tb-111` ⇒ `e44e1abf…`, **rc 0**. Merge-Basis `f4d6d6d`; `f4d6d6d..main` 132 Dateien, `f4d6d6d..tb-111` 32, **Schnittmenge 0**. `sperrliste_abbild_2026-09-26.json` auf `main` 0-mal, auf `tb-111` einmal |

## 1. Block A: Zusammenführen und neu prüfen

`git merge --no-ff tb-111` mit dem vorgegebenen Text ⇒ **`257e7db`**, 32 Dateien, 4834+/5−; gepusht. Der Merge-Baum `e44e1abf…` ist der, den `merge-tree` vorhergesagt hat.

| Messung | Soll | gemessen | Beleg |
|---|---|---|---|
| Hashes | `herkunft.py` `5bbfc9e0…`, `auswertung.py` `a864b216…` | ✔ beide, Abbild `e655c1c8…` | `a_messung.txt` |
| `register()` | weder `e7d82547…` noch `c92900a8…` | **`469272dfbedf06492f1094bdb636295daeb76a9a7d4cc3fd98e89bcb400c0535`**, `fehlend []` | `a_messung.txt` |
| Sonde gegen `e655c1c8…` | 25/0/0, (ii) 0 | **25/0/0, (ii) 0**, Listentext Z. 901–1014 „wie bei Erzeugung: ja“; rc 2 nur NICHT PRÜFBAR (Punkte 1, 3, 4, 6–14) wie immer | `a_sonde_nach_merge.txt` |
| Benchmark im Modus, Repo | `64fb2912…` | **`64fb2912…`**, rc 0, 61 s; `git status` über alle 15 Pfade leer | `a6_laeufe.txt` |
| Benchmark im Modus, frischer Klon | `64fb2912…` | **`64fb2912…`**, rc 0, 61 s; Klon `status --ignored` vorher und nachher leer | `a6_laeufe.txt` |
| ohne Modus, 8 Ausgaben | bytegleich | **8/8 sha256 gleich** den Hashes aus TB-112 A5 (dort vorher = nachher, gemessen auf `e731207` bzw. mit dem `paths.py` von `9d711dc`). Zwischen `af6042f` und `257e7db` hat sich ausserhalb `docs/` nur der Merge geändert | `a5_ausgaben.txt` |
| Trockenlauf im Modus | 9 × rc 0 | **9 × rc 0**, `auswertung`-Import rc 0 | `a6_laeufe.txt` |
| Tests | grün | **17 Testdateien rc 0**, siehe unten | `d_tests.txt` |

**Tests am Merge-Commit** (`d_tests.sh`, Kopie TB-112; Arbeitsbaum ausserhalb `docs/` leer):

| Datei | Ergebnis | Dauer |
|---|---|---|
| `test_faltenplan_neun` / `test_erste_falte_trockenlauf` | 156/156 / 50/50 | 173 / 161 s |
| `test_horizontbeginn` / `test_min_history` / `test_volle_jahre` | 61/61 / 14/14 / 7/7 | 67 / 1 / 0 s |
| `test_universum_trockenlauf` / `test_zwischenablage` | 163/163 / 12/12 | 104 / 2 s |
| `test_paths` / `test_strategy_paths` | 35/35 / 27/27 | 14 / 13 s |
| `test_nulltrades_modus` / `test_rueckfaelle_modus` | 34/34 / 48/48 | 32 / 43 s |
| `test_ergebniskurven` / `test_main_gegenprobe` | 44/44 / 13/13 | 33 / 2 s |
| **`test_startpruefungen`** | **44/44** | 13 s |
| **`test_arbeitsbaum_laufbereich`** | **26/26** | 19 s |
| **`test_ersatzwerte`** | **61/61** (40 + F 15 + G 6 aus TB-111) | 74 s |
| **`test_vorregistrierung`** | **196/196** | 953 s |

`$TMPDIR` vor und nach der Reihe gleich (`tb40_test_` 492, `tb112_klon_` 0).

**Wechselwirkung TB-111 × TB-112, festgehalten** (`a_messung.txt`): `paths.ARBEITSBAUM_PFADE` hat 15 Einträge; `research/vorregistrierung/auswertung.py` steht darin (**True**), `herkunft.py` nicht (**False**). In der Laufbereichsmessung `docs/belege/TB-112/a2_laufbereich.txt` steht `auswertung.py` einmal, `herkunft.py` **0-mal**. Die Sauberkeitsprüfung bindet also die in TB-111 geänderte `auswertung.py`, nicht die ebenfalls geänderte `herkunft.py`. Das ist kein Fehler von TB-112: `herkunft.py` wird von keinem gemessenen Lauf-Typ geladen. Eingetragen als 44-6.

## 2. Block B: Journal

- **DK — TB-111:** der Block „Journalblock zum Übertragen“ aus `ERGEBNIS_TB-111` (30 Zeilen), wörtlich; einzige Änderung `## D? —` ⇒ `## DK —` (gemessen mit `diff`: genau Zeile 1).
- **DL — TB-113:** eigener Block. Beide stehen vor `## Wiederkehrende Lehren`.

## 3. Block C: Register 44

Bauart TB-110: Einsetzskript `eintrag_register_44.py` mit Vorlage `abschnitt44_vorlage.md`, vorher ein Probelauf gegen eine Kopie (`probelauf.sh`: 7 Marken, 13 Zitate, rc 0), dann genau ein echter Lauf. Das Skript fügt jede Marke hinter einer Ankerzeile ein, die im Zielabschnitt genau einmal vorkommt; es prüft Additivität, die Leserwachen (G6, `| **730** |`, ERZEUGT-Block …) und dass **Abschnitt 10 an derselben Stelle zeichengleich** bleibt. Neu gegenüber TB-110: eine Quelle `git:<commit>:<pfad>` (das Register am Merge-Commit, für das Teilzitat aus E2).

| | |
|---|---|
| Abschnitt | **44.0** Kopf (Anlass, Zweig, Merge, Kette zu 43) · **44.1** TB-111: 44-1 (43-1 vollzogen), 44-2 (43-4 vollzogen), 44-3 (Befund A2b), 44-4 (Hash-Übergänge), 44-5 (gültiges Abbild `e655c1c8…`, Sonde gegen das alte 3/5/11/12/14 + `eingefroren`), 44-6 (nach dem Merge gemessen, Wechselwirkung) · **44.2** TB-112: 44-7 (E2/F8 vollzogen, 15 Einträge, `:(exclude)`), 44-8 (`arbeitsbaum_pfade.txt` ist die Tatsachennotiz aus E2), 44-9 (Laufbereich 81 = TB-107), 44-10 (Audit 0, Randbefund 10 Eingaben), 44-11 (Nebennotiz db-Sicherung, `tb40_test_*`) · **44.3** offen: 44-12 die neun Fragen an Fable zeichengleich, Erzeuger, Faltenplan-Abbild · **44.4** was nicht getan wurde |
| Marken | **7**: 19 (unter dem Kasten) · 36.5 (unter der TB-110-Marke) · 37.4 (unter der TB-110-Marke) · 42.2 E2 und 42.3 F8 (je unter „Stand, gemessen“) · 43-1 und 43-4 (je unter der Kette). **Keine in Abschnitt 10** |
| numstat | **344/0** (`c1_numstat.txt`) |
| Zitate | **13/13** `diff` rc 0 (9 Zeilen, 4 Teile; `c2_zitate.txt`): 2 aus dem Code (`auswertung.py` Z. 121/127, `herkunft.py` Z. 160), 1 aus E2 (Register am Merge-Commit Z. 8813), 9 Fragen aus den Ergebnissen TB-109/111/112 |
| Sonde | gegen `e655c1c8…` vorher (`a_sonde_nach_merge.txt`) = nachher (`c_sonde_nach_register.txt`): **Datei byte-gleich** (`diff` leer); Listentext weiter Z. 901–1014, weil alle Marken hinter Abschnitt 10 liegen |
| `register()` | `469272df…` ⇒ **`a0e477fdc8ecace29c60a02de15a7060641fb3c17bec0f76bc2b4e3d0c09e78`** (`c_messung_nach_register.txt`). Selbstbezug: dieser Wert steht nicht im Register (44-4) |
| Test | `test_vorregistrierung` **196/196 rc 0** (952 s) (`c_test_vorregistrierung.txt`) |

## 4. Block D: Arbeitsweise

- **22.1, Nachtrag** mit dem Wortlaut aus dem Auftrag, dazu das Betreiberzitat von 09:36, der Commit `656f04b` und der Hinweis, dass der Beleg die Prozesszeile ist, nicht die Anzeige.
- **22.9 neu**, Wortlaut des Betreibers von 09:31, die Regel in vier Schritten (Auslöser anlegen → Log „Satz ins Fenster gelegt“ → vorher ein hängendes Fenster mit `schliesse_<HEAD>` schliessen → erst dann der Einfügesatz). ⭐ **Der Anlass ist nachgemessen**, nicht übernommen (`logs/sitzungswaechter/waechter.log`): Das erste TB-112-Fenster lag ab **05:04:34Z** (PID 98210); Sonden um 05:21 und 07:07 und der zweite Start um 07:31 wurden abgewiesen, weil es lief; `schliesse_…` beendete es um **07:33:07Z**, also nach **2 h 28 min** — bei rund 4 min Rechenzeit. Der dritte Start um 07:34:28Z lief sofort (`e731207` um 07:36Z).
- numstat 39/0.

## 5. Block E: Worktree

`e_worktree.txt`. Nach dem Push von `main` (`e710bf9` = `origin/main`): `status --porcelain --ignored` im
Worktree leer; `git worktree remove ../trading-bot-tb111` **rc 0**; `git worktree list` zeigt nur noch
`/Users/jaquelineloffler/trading-bot  e710bf9 [main]`; der Ordner existiert nicht mehr. Zweig `tb-111` lokal
**und** auf `origin` weiter `49f0868`. (Eine erste Zeile `git rev-parse --short tb-111 origin/tb-111` endete mit
„Needed a single revision“ — Bedienfehler, `--short` nimmt einen Namen; einzeln nachgemessen, im Beleg angehängt.)

## 6. Für Fable (ohne Kontext lesbar) ⭐⭐

**Stand.** Die Öffnung aus deiner Antwort 25d ((2), (3), (4)) lief als TB-111 auf einem eigenen Zweig und ist jetzt auf `main` (`257e7db`, konfliktfrei; die beiden Zweige hatten keine gemeinsam geänderte Datei). Auf dem zusammengeführten Stand: `herkunft.py` `5bbfc9e0…` und `auswertung.py` `a864b216…` wie auf dem Zweig; Sonde gegen das Abbild `e655c1c8…` 25/0/0 und (ii) 0; Benchmark-Tabelle im Modus in Repo und frischem Klon `64fb2912…`; ohne Modus acht Werkzeugausgaben bytegleich; Trockenlauf 9 × rc 0; 17 Testdateien grün. `herkunft.register()` ist nach dem Merge `469272df…` und nach dem Eintrag von Register 44 `a0e477fd…` (das Register hasht sich mit).

**Register 44** trägt nur Tatsachen ein: den Vollzug von 43-1 und 43-4 (TB-111), den Vollzug von 19 über den Laufbereich mit der Ausnahme aus F8 (TB-112), das gültige Abbild mit Hash, die Hash-Übergänge und — als eigenen Eintrag — den Befund A2b aus TB-111 (die Modus-Abfrage in `herkunft.py` las vorher unter der Ersatzwurzel und endete dort mit 1 statt 2). Marken stehen an sieben alten Stellen, keine in Abschnitt 10.

**Eine Wechselwirkung, die du kennen solltest:** Die neue Sauberkeitsprüfung bindet `auswertung.py`, aber nicht `herkunft.py`. Grund: Kein gemessener Lauf-Typ lädt `herkunft.py` (Laufbereich 81 Module, TB-107 = TB-112). Eine uncommittete Änderung an `herkunft.py` hielte die Startprüfung heute nicht an. Das ändert sich erst, wenn der Erzeuger `register()`/`commit()` ruft und die Tag-Messung das Modul im Laufbereich findet.

**Offen bei dir** (zeichengleich in 44.3 eingetragen): drei Fragen aus TB-109 (Stummel `None`/`False` und Probe; Reichweite von (iv) im Audit; Gegenprobe auch für `main()`), drei aus TB-111 (`datenstand(None)` im Modus; der veraltete Satz im Docstring von `auswertung._abbruch_2`; `str(e)` eines `Abbruch` ist `"2"`), drei aus TB-112 (versionierte Eingaben ausserhalb der Liste; Liste am Tag-Commit erzeugen oder Literal mit Gegenprobe; deutsches Schlüssel-Muster der db-Sicherung). Keine neue Frage aus dieser Sitzung.

## 7. Abweichungen vom Auftrag

| | |
|---|---|
| 1 | **0b: Kopfzeile bzw. `/status` nicht gelesen** — aus der Sitzung heraus nicht erreichbar. Ersatzbeleg ist die Befehlszeile des eigenen Elternprozesses (`claude --effort high --remote-control`). Weitergearbeitet, wie der Auftrag für diesen Fall sagt; der Schalter greift beim Start nachweislich |
| 2 | **A, 8 Ausgaben ohne Modus: kein eigener Vorher-Lauf.** Verglichen gegen die in TB-112 A5 festgehaltenen sha256 (dort vorher = nachher). Alle 8 gleich; ein Vorher-Lauf hätte nur dieselben Hashes ein drittes Mal erzeugt. Zwischen jenem Stand und dem Merge hat sich ausserhalb `docs/` nur der Merge selbst geändert |
| 3 | **C, ein Zitat aus einem früheren Registerstand** (E2, Register am Merge-Commit `257e7db` Z. 8813), weil sich die Zeilennummern im laufenden Register durch die Marken verschieben. Das Prüfskript liest diese Quelle per `git show` |

## 8. Was NICHT geschah

- Keine Code-Änderung ausser dem Merge; kein neues Abbild (gültig bleibt `e655c1c8…`); keine Marke in Abschnitt 10; `crontab` nicht aufgerufen.
- Der veraltete Satz im Docstring von `auswertung._abbruch_2` („`Abbruch` oben endet mit 1“) steht weiter (Frage an Fable).
- Der Zweig `tb-111` ist nicht gelöscht, weder lokal noch auf `origin`.
- Liegen geblieben im Scratchpad (sitzungseigen): der A6-Klon, die Messordner. `/tmp/x_main` (eine leere Datei aus einem abgebrochenen Befehl) liegt noch in `/tmp`; `rm` wird in dieser Sitzung abgelehnt.

---

## In einfacher Sprache

Die Nebenarbeit von heute Nacht (TB-111) war in einer eigenen Kopie des Projekts gemacht worden. Sie ist jetzt mit dem Hauptstand zusammengeführt, ohne dass sich irgendetwas in die Quere kam. Danach wurde alles neu geprüft: Die Vergleichstabelle ist Byte für Byte dieselbe, die Programme verhalten sich ohne den geschützten Modus unverändert, und alle Tests sind grün. Das Regelwerk hat Abschnitt 44 bekommen. Dort steht jetzt, was TB-111 und TB-112 tatsächlich umgesetzt haben, und an sieben alten Stellen steht ein Verweis darauf. Die Arbeitsweise hat zwei Ergänzungen: Der Wächter startet Sitzungen mit hohem Aufwand, und der steuernde Chat legt eine Sitzung an, bevor er den Auftragstext herausgibt — weil am Morgen ein Fenster zweieinhalb Stunden unbemerkt gewartet hatte. Zum Schluss wurde der Hilfsordner der Nebenarbeit entfernt; die Arbeit selbst bleibt im Verlauf erhalten.

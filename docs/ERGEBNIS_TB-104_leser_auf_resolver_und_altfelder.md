# TB-104 — Ergebnis: Alle Leser des Laufbereichs auf den Resolver, die Verfahren-A-Felder aus dem Faltenplan, der Laufbereich gemessen — Benchmark-Tabelle im Modus zweimal bytegleich `64fb2912…`

**Sitzungstitel:** `TB-104` · **Stand:** 25.09.2026, ca. 10:45 · **Auftrag:**
`docs/auftraege/MAC_TB-104_leser_auf_resolver_und_altfelder.md` · **Belege:** `docs/belege/TB-104/`
**Eingang:** `836865f` · Commits: `be31276` (Schritt 0), `572d725` (Block A+B), `f334a7b` (Block C),
`d96b352` (neues Abbild), Abgabe-Commit (Belege C5/D/E, dieses Dokument, Journalblock DC). Alle gepusht.
**Grundlage:** Fable 24c Abschnitt 2, 24d Abschnitt 3, 25a Abschnitte 1 (1), 3 (A), 3 (C), 4.
Freigabe des Betreibers 25.09.2026, 07:52 (alle genannten Dateien, ein neues Abbild).
⭐ **Zusatzfreigabe in dieser Sitzung:** `research/vorregistrierung/registerbericht.py`, nur die Spalte
„Purge = Embargo" der Faltenplan-Tabelle in `block()`, **25.09.2026, 09:10:49**, Auswahlkarte, Antwort
„Freigeben (Empfohlen)".
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **A** | Vier Module hatten eigene Pfadlogik für Kurs- oder Universumsdateien: `benchmark.py`, `faltenplan_neun.py`, `loaderlauf.py` (nur über `--daten`) und `universum_trockenlauf.py` (reicht `--daten` nur durch). `erste_falte_trockenlauf.py` hat keine eigene, es liest über `faltenplan_neun`. Die Verfahren-A-Felder haben **zwei Leser mehr** als vorgemessen: `faltenplan.py:464` (eigene Ausgabe) und **`G9`** |
| ⭐ **B** | Die vier Module holen ihre Pfade jetzt über `shared/paths.py`. Eine Ersatzwurzel (`TB36_BASE_DIR`, `--daten`) ist als Messwerkzeug benannt und **bricht unter dem Modus mit 2 ab**, bevor gelesen wird. Ohne Modus sind **alle 8 Ausgaben bytegleich** vor und nach, und `benchmark.py` ohne Modus ist bytegleich `64fb2912…`. 21 neue Prüfungen, davon 7 Mutationsproben mit Gegenprobe; jede beisst allein |
| ⭐ **C** | `purge_tage`, `embargo_tage` und `training_bis_ausschliesslich` sind aus dem gerechneten Plan entfernt. **C2: genau 9 + 9 + 77 Vorkommen weniger, alles andere zeichengleich, Faltengrenzen gleich.** `G8` prüft jetzt „keine Felder ausserhalb der Feldliste", `G9` „keins der drei Felder". Mutationsprobe `G8M` mit Gegenprobe. ⚠️ **Die Feldliste kommt aus dem Code**, weil 33.3 die Feldliste des *Abbilds* ist und nicht die des gerechneten Plans (Abschnitt 5, Frage 3) |
| ⭐⭐ **C5** | `benchmark.py` im Modus **zweimal bytegleich `64fb2912…`**. Kurse und Universum kommen nur aus dem Snapshot (222 + 2). Ausserhalb liest der Lauf nur, was erwartet war: 9 TB-24-Listen und `messgroessen.json`. ⚠️ **Zwei neue Klassen von Zugriffen:** 9 Bot-Quelltexte werden als *Daten* gelesen, und es gibt 11 Zwischenablagen in `$TMPDIR` (Abschnitt 4). **Umgebung:** 5 Dateien, dieselben wie in TB-103. **Schreibziele:** `logs/notifications/manuelle_eingriffe.log` wird im Modus `a` geöffnet, über **`registerdaten.py:62` → `notifications/manual_close.py:241-243`**. ⛔ Der Nachweis bleibt 2 |
| ⭐⭐ **D** | **Laufbereich = 80 Repo-Module**: 55 Bot-Dateien, 13 aus `shared/`, 11 aus `research/`, `notifications/manual_close.py`. `herkunft.py` und `shared/regimewache.py` gehören **nicht** dazu. Vom Rückfall-Inventar aus TB-103 liegen **30 von 51 Zeilen im Laufbereich**. **Alle vier Rückfälle** aus Fable 25a liegen in Dateien des Laufbereichs. Ausgeführt werden (b) und (a) sowie Teile von (d); (c) liegt nur in `__main__`-Blöcken |
| **E** | Geändert sind nur freigegebene Dateien und `docs/`, dazu das neue Abbild. Gesperrte Dateien, Datenstand `d9449faf…`, Snapshot, `ergebnisse/` (bis auf das Abbild) und alle 12 `*.db` sind gleich; der Summenhash (5) ohne die Freigegebenen und ohne das Abbild ist gleich. Neues Abbild `cb4eb1b4…`; die Sonde gegen das alte meldet 2/4/6, gegen das neue 0 Pfad-Bestandteile mit 1 |

---

## 0. Schritt 0

| | |
|---|---|
| 0a | Sieben Dateien des steuernden Chats committet (`be31276`), wie im Auftrag erwartet, sonst nichts im Arbeitsbaum |
| 0b | Keine `.git/*.lock`. HEAD am Eingang `836865f`. Datenstand `d9449faf…` (223 Dateien). Snapshot `--pruefen` UNVERÄNDERT. 12 `*.db`. Benchmark-Tabelle `64fb2912…`. Sonde gegen `…_2026-09-23.json` rc 2 (0 Pfad-Bestandteile mit 1). Belege `0_hashes_vorher.txt` (mit `hashes.sh`) und `0_sonde_vorher.txt` |

## 1. Block A — Vormessung nachgemessen, und Fables vier Unsicherheiten

| | Ergebnis (Beleg) |
|---|---|
| **A1** | Eigene Logik haben `benchmark.py` (`TB30A_BASE_DIR` → `data/`, Universum `BASE_DIR + rd.UNIVERSUM`), `faltenplan_neun.py` (`TB36_BASE_DIR`, dazu ein **eigenes `UNIVERSUM`-dict**, eine zweite Namensliste seit TB-36, und ein Parameter `basis` in 9 Funktionen, den kein Aufrufer ausserhalb der Tests setzt), `loaderlauf.py` (nur `--daten`). ⚠️ Abweichung: **`universum_trockenlauf.py` liest selbst keine Kurs- oder Universumsdatei**, sein `TB40_BASE_DIR` bestimmt nur die Wurzel für Code und Register. `erste_falte_trockenlauf.py`, `faltenschranke_messung.py` und `embargo_neun.py` (die letzten beiden nicht freigegeben) lesen über `faltenplan_neun` (`a_vormessung.txt`) |
| **A2** | `registerdaten`, `registerbericht`, `pruefe_grenzsaetze`, `auswertung` und `messgroessen` lesen über `BASE_DIR` keine Kurs- oder Universumsdatei. `herkunft` liest `data/` nur für den Hash. ⚠️ **Ergänzung:** `faltenplan.py` liest Kurs- und Universumsdateien **indirekt** über `faltenplan_neun` (`symbolbeginn`) und über die Loader-Kindprozesse. Damit tun es auch `benchmark`, `auswertung` und `registerbericht`, die `fp.faltenplan()` rufen. B2 deckt diese Wege mit ab |
| **A3** | Leser der Altfelder: `registerbericht.py:147`, `G8`, und zusätzlich **`faltenplan.py:464`** (Spalte „Purge" in `main()`) und **`G9`** („Purge und Embargo gleich lang"). `purge_tage()` hat nur einen Aufrufer (`_plan`). `mess["haltedauer"]` liest ausserdem nur `registerdaten.py:231` (`median_balken`) |
| **A4** | Siehe Abschnitt 5, (3) (`a4_datenende.txt`) |
| **A5** | Siehe Abschnitt 5, (1) (`a5_datenstand.txt`) |
| **A6** | Siehe Abschnitt 5, (2) (`a6_ordner.txt`, `a6_lauf.sh`) |
| **A7** | Siehe Abschnitt 5, (4) (`a7_get.txt`) |
| **A8** | `benchmark.py` steht auf den Punkten 4 und 6, `faltenplan.py` auf Punkt 2, **beide auch in `herkunft.py::EINGEFROREN`**. Die übrigen zehn freigegebenen Dateien stehen nirgends (`a8_sperrliste.txt`) |

## 2. Block B — die Leser auf den Resolver

| Modul | Änderung |
|---|---|
| `research/vorregistrierung/benchmark.py` | `DATA_DIR = paths.DATA_DIR`, `CONFIG_DIR = paths.CONFIG_DIR`, Universum = `CONFIG_DIR + os.path.basename(rd.UNIVERSUM[markt])`, also keine zweite Namensliste. `paths` wird aus `<BASE_DIR>/shared` importiert, weil die Mutationskopien in `test_vorregistrierung` den Ordner nach `/tmp` kopieren und `TB30A_BASE_DIR` auf die Repo-Wurzel setzen. `TB30A_BASE_DIR` ist damit nur noch Ersatz der Repo-Wurzel. Kommentar und `--help` sagen: kein Weg zum Snapshot |
| `research/faltenplan_neun/faltenplan_neun.py` | `universumsdatei()` (neu) und `kursdatei()` holen ihre Pfade ohne Ersatzwurzel über `paths`. `TB36_BASE_DIR`/`basis` heisst jetzt **`ERSATZWURZEL`** (Messwerkzeug, Kommentar und `--help`). Unter dem Modus **bricht `_ersatzwurzel()` mit `SystemExit(2)` ab**, bevor gelesen wird. `paths` kommt aus `<Datei>/../../shared` |
| `research/universum_trockenlauf/loaderlauf.py` | `--daten` unter dem Modus: **rc 2 vor dem Laden des Bots**. Das Ergebnis-JSON nennt den Grund (`MODUS: …`), gefragt wird über `paths.selektionsmodus()` aus `<BASIS>/shared`. Ohne `--daten` bekommt der Loader seinen `DATA_DIR` wie bisher vom Resolver |
| `research/universum_trockenlauf/universum_trockenlauf.py` | nur Kommentar und `--help` (`--stille-filter` ist Messwerkzeug) |
| `research/faltenplan_neun/erste_falte_trockenlauf.py` | **unverändert**: keine eigene Pfadlogik (B4 nach A1) |

**Proben (B5)**, alle in der Bauart von TB-103 Teil I: Wegwerfbaum als Git-Repo mit echter `paths.py`
und echten Modulen, erfundene Reihen in `data/`, Snapshot-Attrappe, eigener Lesehaken.

| Name | Datei | prüft |
|---|---|---|
| **J1** | `test_vorregistrierung.py` | `benchmark.py` im Modus: 0 Kursdateien aus `data/`, 0 Universumsdateien aus `config/`, Snapshot-CSV > 0, 2 Snapshot-Universumsdateien, rc 0 |
| **J2 / J2-G** | 〃 | Mutation „Resolver-Umstellung zurückgenommen" (die zwei Zuweisungen von vor TB-104) ⇒ liest aus `data/` **und** `config/`; die Gegenprobe ohne Mutation scheitert |
| **K1** / **K2** | `test_faltenplan_neun.py` | `faltenplan_neun` bzw. `erste_falte_trockenlauf` im Modus: dasselbe wie J1 |
| **K3** | 〃 | `TB36_BASE_DIR` unter dem Modus ⇒ rc 2, 0 Lesezugriffe |
| **K4**, **K5**, **K6**, **K7** (je mit `-G`) | 〃 | Mutationen: Kurspfad zurückgenommen (K4 an `faltenplan_neun`, K6 an `erste_falte_trockenlauf`), Universumspfad zurückgenommen (K5), Modus-Wache der Ersatzwurzel entfernt (K7). Jede beisst allein |
| **O1** | `test_universum_trockenlauf.py` | `loaderlauf.py` im Modus ohne `--daten` (Attrappen-Bot mit demselben `DATA_DIR`-Vertrag): liest aus dem Snapshot, 0 aus `data/`/`config/` |
| **O2** / **O3** | 〃 | `--daten` im Modus ⇒ rc 2 mit Grund, 0 Kursdateien (direkt bzw. über `messe_bot`) |
| **O4**, **O5** (je mit `-G`) | 〃 | Mutation „Modus-Wache für `--daten` entfernt" ⇒ liest aus dem Ersatzordner |

`test_faltenplan_neun`: `_mutiert()` legt die Werkzeugkopie jetzt unter `research/faltenplan_neun/`
ab, mit `shared/` als Verweis. Sonst fände die Kopie den Resolver nicht, und F–H würden aus dem falschen
Grund scheitern.

**Ohne Modus unverändert** (Abbruchkriterium 3; `b0_ausgaben.sh`, `b0_vorher.txt`, `b0_nach_B.txt`):
Die Ausgaben von `faltenplan_neun --json`, `embargo_neun --json`, `faltenschranke_messung --json`,
`loader_lesart` (9 Bots), dem Faltenplan im Speicher, `universum_trockenlauf --json`,
`--stille-filter --json` und `erste_falte_trockenlauf --json` sind **alle 8 bytegleich**.
`benchmark.py` ohne Modus nach B: `64fb2912…` (`b_tests.txt`).

**Tests nach B:** `test_vorregistrierung` **194/194** (vorher 191), `test_faltenplan_neun` **156/156**
(vorher 145), `test_universum_trockenlauf` **163/163** (vorher 156), `test_erste_falte_trockenlauf`
50/50, `test_horizontbeginn` 61/61, `test_paths` 35/35.

## 3. Block C — die Verfahren-A-Felder aus dem Faltenplan

- **C1** `faltenplan.py`: Die drei Felder, `purge_tage()` und das Lesen von `mess["haltedauer"]` sind
  entfernt. Ausserdem, weil nur dadurch benutzt: die Spalte „Purge" in `main()`, die Importe
  `math`/`timedelta` und die Schleifenvariable `von`. Kopfpunkt 5 trägt einen Vermerk; der Absatz
  bleibt als Verlauf stehen. Alter Hash `7aa0b8cc…`, neuer `d57fe9c9…`.
  `ergebnisse/faltenplan.json` ist unberührt (`0e54ac5c…` vor und nach).
- **C2** (`c2_vergleich.py`, `c2_ausgabevergleich.txt`), gerechnet im Speicher; `python3 faltenplan.py`
  lief nie. Vorher minus 9 × `purge_tage`, 9 × `embargo_tage`, 77 × `training_bis_ausschliesslich` ist
  **zeichengleich** mit nachher. Faltengrenzen (Name, von, bis, Rolle) sind je Bot gleich. rc 0.
- **C3** `G8`: je Plan und je Falte keine Felder ausserhalb von `FELDLISTE_PLAN` (16 Schlüssel) und
  `FELDLISTE_FALTE` (6 Schlüssel). `G9`: keins der drei Felder im Plan, in einer Falte oder in der
  Feldliste. `G9` las die Felder ebenfalls und ist deshalb mit angepasst, nicht gelöscht. **`G8M`**
  fügt `"purge_tage": 0` in einer Kopie von `faltenplan.py` wieder ein und rechnet den Plan in einem
  eigenen Prozess ⇒ `G8` wäre rot. `G8M-G` ist die Gegenprobe. **196/196.**
- **C4** `registerbericht.py`: nur die Spalte (freigegeben 09:10), `block()` läuft durch
  (`c4_registerbericht.txt`; die Tabellenwerte sind nach 27.1 nicht wiedergegeben). Alter Hash
  `dace1b01…`, neuer `de35a5a0…`.
- **Tests nach C** (Endstand, Code seit `f334a7b` unverändert): `test_vorregistrierung` 196/196,
  `test_faltenplan_neun` 156/156, `test_erste_falte_trockenlauf` 50/50, `test_horizontbeginn` 61/61,
  `test_universum_trockenlauf` 163/163, `test_paths` 35/35 (`c3_tests.txt`).

## 4. C5 — die Benchmark-Tabelle im Modus, mit den drei Klassen ⭐⭐

`benchmark.py --ziel <scratch>` im Modus: `TB_SELEKTIONS*` auf den echten Snapshot, HEAD `f334a7b`,
Arbeitsbaum sauber, Haken `docs/belege/TB-104/haken/sitecustomize.py` (öffnet, legt Ordner an, mit
Aufrufstapel, Modulliste). **Lauf 1 und 2: rc 0, 61 s bzw. 59 s, beide `64fb2912f1a2ffb0…`**
(`c5_laeufe.txt`). Je Lauf 11 Prozesse: der Hauptprozess und 10 Loader-Kindprozesse
(`t3_supertrend` zweimal, weil `erste_falte` zwei Kandidatenfalten prüft).

| Klasse | gemessen (Lauf 1 = Lauf 2) | Soll | Urteil |
|---|---|---|---|
| **(i) Eingaben, im Snapshot** | 222 Kurs-CSV, `config/top25_symbols.txt`, `config/sp500_top150.txt`, `MANIFEST.json` | Kurse und Universum nur von dort | ✔ |
| **(i) Eingaben, ausserhalb** | `research/vorregistrierung/ergebnisse/messgroessen.json` (`registerdaten.py:169`), die 9 TB-24-Listen `research/tb24_haltedauern/daten/<bot>_alle_trades.csv` (`faltenplan.py:138`) | genau diese (39.8) | ✔ erwartet, **Nachweis bleibt 2** |
| ⚠️ **(i) Zwischenablagen** | 11 × `$TMPDIR/tb40_lauf_*/<bot>.json` (das Ergebnis eines Loader-Kindprozesses, geschrieben vom Kind, gelesen vom Elternprozess, `universum_trockenlauf.py:323`) und 1 × die Schreibprobe von `tempfile` in `$TMPDIR` | in 25a nicht vorgesehen | **Frage an Fable** (Abschnitt 5, (6)) |
| ⚠️ **(i) Quelltext als Daten** | 9 × `strategies/<bot>/multi_symbol_optimise.py` wird **gelesen, nicht importiert**, von `faltenschranke_messung.py:140` (`_min_history`: `MIN_HISTORY_*` per regulärem Ausdruck), aufgerufen aus `benchmark.py:257` | in 25a nicht vorgesehen | **Frage an Fable** (Abschnitt 5, (5)) |
| **(ii) Umgebung** | 5 Dateien ausserhalb der Python-Installation: `requirements.lock` und `/dev/null` (`paths.py:470/501`, die Startprüfung), `/System/Library/CoreServices/SystemVersion.plist`, `/dev/urandom`, `/private/var/db/timezone/…/zoneinfo/UTC` (alle drei über `benchmark.py:90`, den Import von numpy/pandas). Dazu 10 684 Zugriffe in der Python-Installation, nur gezählt | Liste mit Stapel; Vergleich mit TB-103 | **dieselben 5 wie in TB-103** |
| **(iii) Schreibziele** | ⚠️ `mkdir logs/notifications` und **`open(…, "a")` auf `logs/notifications/manuelle_eingriffe.log`**. ⭐ **Welcher Import:** `benchmark.py:99` → `faltenplan.py:113` → **`registerdaten.py:62` (`from manual_close import allokation`)** → `notifications/manual_close.py:241` (`os.makedirs`) und `:242` (`RotatingFileHandler`), ausgeführt **beim Import**. Nichts geändert (`notifications/` ist nicht freigegeben). ⚠️ Dazu 11 × `mkdir $TMPDIR/tb40_lauf_*` (`universum_trockenlauf.py:306`, `mkdtemp`) und 11 × `open(…, "w")` darin (`loaderlauf.py:639`). Die Ordner werden **nie entfernt** | nur `--ziel` und Belege | **Befund 1** der Schreibziele-Sonde (25a (3)). Die Zwischenablagen: Frage (6) |

Belege: `c5_klassen_bm_lauf1.txt`, `c5_klassen_bm_lauf2.txt` (alles mit Aufrufstapel).

## 5. Für Fable — ohne Kontext lesbar ⭐⭐

*Kurzer Kontext:* In dieser Sitzung wurden die Programme, die im geschützten Lauf („Modus“) Kurs- oder
Universumsdateien lesen, auf die zentrale Pfadstelle `shared/paths.py` umgestellt. Aus dem Plan, den
`faltenplan.py` zur Laufzeit rechnet, wurden drei Felder eines abgeschafften Verfahrens entfernt. Dann
wurde gemessen, welche Module ein Modus-Lauf lädt. Unten stehen die Antworten auf deine vier
Unsicherheiten aus 25a und die Fragen, die daraus folgen. Es gibt keine Kennzahl und keine Trade-Zahl.

### Antworten auf deine vier Unsicherheiten (25a, Schluss)

**(1) `herkunft.py::datenstand()` — nimmt es das Verzeichnis als Argument?** **Ja.** Die Signatur ist
`datenstand(daten_dir=None)`. Die Voreinstellung ist `<BASE_DIR>/data` (Z. 98), und es zählt nur `*.csv`
der obersten Ebene. `datenstand(<Snapshot-Ordner>)` ergibt `d9449faf…/223` = der MANIFEST-Wert; so ruft
es auch `shared/snapshot.py:358`. ⚠️ **Aber `block()` (Z. 128) und damit `anhaengen()` rufen es ohne
Argument.** Wer unter dem Modus `block()` ruft, bekommt also den Hash von `data/`, nicht den des
Snapshots. Heute sind beide gleich (`d9449faf`), das ist aber keine Eigenschaft des Codes.
`herkunft.py` wird von keinem Modul des Laufbereichs importiert (D1). Nach deiner Regel bleibt es
geschlossen; der Erzeuger ruft `datenstand(paths.DATA_DIR)` selbst. Gemessen, nichts geändert.

**(2) Legt ein Modus-Lauf Ordner unter `results/` oder `logs/` an?** **Ja, wenn sie fehlen.** Die
Messung lief in einem frischen `git clone` von `be31276`: `logs/` ist gar nicht versioniert,
`results/elliott_wave/` auch nicht. Ein Modus-Lauf von `elliott_wave` (TB-103-Trockenlauf, echter
Snapshot, Haken auf das Ereignis `os.mkdir`) hat **`logs/`, `logs/elliott_wave/` und
`results/elliott_wave/` angelegt**. Die Stelle ist `shared/strategy_paths.py:129-130` (`os.makedirs`),
gerufen beim Import von fünf Bot-Modulen. Im echten Repo existieren alle 18 Ordner; dort versucht
`makedirs` es bei jedem Lauf (der Haken sieht den Versuch), legt aber nichts an. ⇒ Das ist ein
Schreibziel der Klasse (iii). Nebenbefund: Der Messumschlag `research/exposure_messung/bot_lauf.py:63`
legt beim Import `research/exposure_messung/daten/` an. Er ist Teil des Laufbereichs (D1) und damit
auch des künftigen Erzeugers.

**(3) Ruft der Trockenlauf den Loader am Datenende auf, so wie 16.1.1 gemessen wurde?** **Nein, die
Verfahren sind verschieden. Das Ergebnis ist am heutigen Stand trotzdem gleich.** TB-40 hat die Spalte
„Bestätigung" **am Faltenende** gemessen: Stichtag 2026-08-31T23:59:59, jedes `read_csv` auf den
Stichtag gekürzt (`universum_trockenlauf.trockenlauf()`; ERGEBNIS TB-40 Abschnitt 1: „Gemessen am
Faltenende"). Der Trockenlauf aus TB-103 lädt dagegen **ohne Datumsgrenze, am Datenende**. Nachgemessen
mit demselben Loader: **9/9 Bots ergeben an beiden Stichtagen dieselbe Menge** (18/18/20/20/20/147 × 4).
Kein Symbol wird zwischen dem 31.08. und dem Datenende des Snapshots handelbar oder fällt weg. Für
deinen Teil (2) aus 3 (B) heisst das: Die Voraussetzung „am Datenende wie 16.1.1" trifft wörtlich nicht
zu. Die Gleichheit ist am Stand `d9449faf`/`63e4b6c8` gemessen, nicht aus dem Verfahren gefolgert. Ein
Snapshot, der weit über den Go-Live-Schnitt reicht, könnte auseinanderlaufen. **Vorschlag:** Der
Tag-Trockenlauf misst am Stichtag 2026-08-31T23:59:59, also dem Verfahren von 16.1.1, statt am
Datenende.

**(4) Ist ein `.get(…, default)`-Ersatzwert in `auswertung.py` mit den registrierten Eingaben je
erreichbar?** **Nein, für alle Stellen, die eine Schwelle oder die Selektionsstatistik vertreten**
(Z. 284/286, 380, 500–521). Alle hängen an derselben Bedingung „Plan ohne Selektionsfalte". 4b schliesst
sie aus, und kein Bot erfüllt sie heute: `lies_zellen()` erzwingt ein vollständiges Raster, dieselben
Falten je Zelle und kein leeres `netto_sharpe` in Falten mit Trades. `beta_bereinigung()` setzt
`bestimmt` auf jedem Rückweg. Das ist **aus dem Quelltext gelesen, kein Lauf**; es gibt noch keine
Rohergebnisse. Z. 156 (`_bedingung`) ist erreichbar, aber kein Ersatzwert: `None` ist dort die
registrierte Bedeutung (keine Nebenbedingung).

### Der Laufbereich, gemessen (D1) — dein Registertext aus 25a Abschnitt 4

Gemessen sind drei Lauf-Typen im Modus, jeder mit Import-Audit. Das ist die Modulliste beim
Prozessende; Bytecode ist auf die Quelle zurückgeführt, und dazu kommen die Öffnungen von `.py`/`.pyc`
für Kindprozesse, deren eigener Schreibschutz die Liste nicht schreiben lässt:
(a) der Trockenlauf aller neun Bots (TB-103-Umschlag), (b) `benchmark.py` einschliesslich
`faltenplan.py` und der Loader-Kindprozesse, (c) `auswertung.py` nur als Import.
**Vereinigung: 80 Repo-Module** (`d1_laufbereich_vereinigung.txt`, je Modul mit Lauf-Typ):
55 unter `strategies/` (alle Bot-Module, die Loader und Simulation laden, auch `regime_filter.py`,
`fetch_4h_data.py`, `fetch_stock_data.py`, `stocks_symbols_config.py`), 13 unter `shared/`
(`abrufschutz`, `binance_historie`, `data_quality`, `fetch_binance_data`, `fetch_multi_data`,
`handelskosten`, `kursdaten`, `ladeprotokoll`, `messkette`, `paths`, `strategy_paths`, `symbols_config`,
`zuteilung`), 11 unter `research/` (`vorregistrierung/{auswertung, benchmark, faltenplan, kennzahlen,
registerdaten}`, `faltenplan_neun/{faltenplan_neun, faltenschranke_messung, erste_falte_trockenlauf}`,
`universum_trockenlauf/{universum_trockenlauf, loaderlauf}`, `exposure_messung/bot_lauf`) und
**`notifications/manual_close.py`**. ⚠️ **Nicht** darin: `herkunft.py`, `shared/regimewache.py`,
`messgroessen.py`. Letzteres ist selbst ein Modus-Lauf (TB-103), aber keiner der drei hier gemessenen
Lauf-Typen. Der Erzeuger (Plan-Punkt 3) existiert noch nicht. **Die Liste ist also die Menge dieser
drei Lauf-Typen, nicht der ganze Laufbereich deiner Definition.**

**Rückfall-Inventar (D2, `d2_rueckfaelle_im_laufbereich.txt`):** 30 der 51 Inventarzeilen liegen im
Laufbereich, 21 nicht. Nicht darin liegen `messgroessen` (3, siehe oben), `herkunft` (4),
`pruefe_grenzsaetze`, `registerbericht`, `entscheidungskerze` (3), `groessenfaktor`, `claude_client`,
`build_daily_crypto_data`, `ergebniskurven`, `portfolio_overview`, `sperrlistensonde`, `umstellungstag`,
`get_top_stocks`, `buy_and_hold_benchmark`.

**Die vier Rückfälle (D3, `d3_vier_rueckfaelle.txt`), alle nicht geändert:**

| Rang | Rückfall | Datei:Stelle (Stand `f334a7b`) | Datei im Laufbereich | Lauf-Typ | Stelle im gemessenen Lauf ausgeführt |
|---|---|---|---|---|---|
| 1 | **(b)** Regimefilter `t3_supertrend` | `strategies/t3_supertrend/equity_simulation.py:77-79` (`collect_all_trades`), `multi_symbol_optimise.py:130-132` (`evaluate_combination_multi`) | ja | Trockenlauf; `multi_symbol_optimise` auch im Benchmark (Loader) | **ja** (`collect_all_trades` über `bot_lauf.hole_trades`); der Optimierer nicht. `regimewache.pruefe_einbau()`: **0 von 3 Einbaustellen**, auch `volatility_breakout_crypto/equity_simulation.py` ist offen |
| 2 | **(c)** `exit()` mit rc 0 | 9 × `equity_simulation.py`, 5 × `multi_symbol_optimise.py` (Zeilen im Beleg), dazu 9 × `multi_symbol_walk_forward.py`, 7 × `buy_and_hold_benchmark.py` und Werkzeuge | die ersten 14 ja, die übrigen nein | Trockenlauf, Benchmark | **nein**: alle im Block `if __name__ == "__main__":`. Erreicht wird die Stelle nur von einem Modus-Lauf, der die Skripte direkt startet |
| 3 | **(d)** Ersatzwerte für Schwellen | `faltenplan.py:152-153`, `:159-160`; `benchmark.py:206-207`, `:302`; `auswertung.py:284/286`, `:333-334/380-385`, `:500-521` | ja | Benchmark, Auswertung | die Funktionen in `faltenplan`/`benchmark` ja, die Ersatzzweige am echten Bestand nicht; `auswertung` nur importiert (A7: unerreichbar). **B und C haben keine dieser Stellen berührt** |
| 4 | **(a)** leere Liste nach `EXCLUDE_SYMBOLS` | `shared/symbols_config.py:26-35`, beim Import (Z. 38) | ja | Trockenlauf, Benchmark (Krypto-Loader) | ja, beim Import; der Ersatzzweig am Snapshot nicht (24 von 25) |

### Fragen

1. **Zwischenablagen in `$TMPDIR` (C5, Klassen (i)/(iii)):** Der Modus-Lauf von `benchmark.py` legt je
   Loader-Kindprozess einen Ordner per `mkdtemp` an. Das Kind schreibt sein Ergebnis-JSON dort hinein,
   der Elternprozess liest es; 11 Ordner je Lauf, **nie entfernt**. Nach 25a (A) (iii) ist das ein
   Schreibziel ausserhalb `--ziel`, also Befund 1. **Gehört eine prozessinterne Zwischenablage zu
   (iii)**, oder ist sie eine vierte Klasse, zulässig, wenn sie unter `--ziel` liegt? Für das Handwerk
   liegt die Antwort nahe: Die Ablage kommt unter das Ziel oder in einen Ordner, der am Ende entfernt
   wird.
2. **Quelltext als Daten (C5, Klasse (i)):** `faltenschranke_messung._min_history` liest `MIN_HISTORY_*`
   per regulärem Ausdruck aus 9 Bot-Dateien, statt sie zu importieren (Absicht seit TB-56: „eine Quelle,
   keine Kopie"). Der Code ist über den Commit registriert (5e). **Zählt dieses Lesen als Eingabe der
   Klasse (i)** (dann ausserhalb des Snapshots, also Befund) **oder als Code** (über Commit und Abbild
   gedeckt)? Ich würde „Code" sagen, weil der Hash des Standes es bindet. Es steht aber in keiner
   Klasse.
3. **Feldliste von `G8`:** 33.3 ist die Feldliste des **Abbilds** mit 8 Feldern (`asof`, `bot`,
   `horizontbeginn`, `faltenlaenge_jahre`, `erste_selektionsfalte`, `selektionsfalten`, `quelle`,
   `bestaetigungsperiode`). Der gerechnete Plan trägt auch nach C1 **16 Schlüssel je Plan und 6 je
   Falte**, darunter `markt`, `status`, `trades_je_jahr`, `erste_falte_trockenlauf_H` und
   `faltenlaenge_begruendung`. Deine Präzisierung („der gerechnete Plan trägt keine Grösse, die
   33.2/33.3 nicht kennt") wäre also am heutigen Plan **mit 12 weiteren Feldern rot**, wenn man 33.3
   wörtlich als Plan-Feldliste nimmt. Ich habe die Rückfallregel des Auftrags angewandt: Die Feldliste
   von `G8` sind die Schlüssel des Plans **nach C1**, aus dem Code. **Soll der gerechnete Plan auf die
   33.3-Felder schrumpfen, oder vergleicht die Faltenplan-Sonde eine definierte Abbildung Plan → Abbild?**
   Im zweiten Fall bräuchte deine Präzisierung einen Satz dazu.
4. **Weitere Verfahren-A-Reste**, gemessen, nicht geändert (nicht Teil deiner drei): `mindesttraining_jahre`
   je Plan und **`embargo_nach_falten` je Falte** im gerechneten Plan, dazu die Zeile „Mindesttraining
   vor der ersten Falte: 4 Jahre" in `registerbericht.py:137-139`. Gehören sie zu derselben Berichtigung?
5. **Laufbereich:** Soll `messgroessen.py` (ein Modus-Lauf aus TB-103) ausdrücklich zu den Lauf-Typen
   deiner Definition gehören? Deine Aufzählung nennt es nicht, es erzeugt aber eine registrierte
   Eingabedatei.
6. **Schreibziel `manuelle_eingriffe.log`:** Der öffnende Import ist gefunden:
   `registerdaten.py:62` → `manual_close.py:241-243`. Er läuft in `benchmark`, `faltenplan` und
   `auswertung`, also in jedem Modus-Lauf der Vorregistrierung. Die Behebung braucht eine Freigabe für
   `notifications/` (Live-Code) oder für `registerdaten.py` (Sperrlistenpunkt 1): Entweder holt
   `registerdaten` die eine Funktion `allokation` ohne den Logger-Seiteneffekt, oder `manual_close`
   legt den Handler erst bei der ersten Protokollzeile an. Beides ist Handwerk; welcher Ort geöffnet
   wird, entscheidet der Betreiber.

## 6. Abweichungen vom Auftrag

| | |
|---|---|
| 1 | **`G9`** ist mit angepasst. Der Auftrag nannte nur `G8`, aber `G9` las die Felder ebenfalls und wäre abgebrochen. Neu: „keins der drei Felder in Plan, Falte oder Feldliste" |
| 2 | `faltenplan.py`: Ausser den drei Feldern sind auch die Ausgabespalte „Purge" in `main()` (sonst KeyError), die dadurch unbenutzten Importe `math`/`timedelta` und die Variable `von` entfernt. Der Kopfpunkt 5 hat einen Vermerk bekommen. Der Ausgabevergleich C2 ist davon unberührt |
| 3 | Die Proben für `erste_falte_trockenlauf.py` (K2, K6) stehen in `test_faltenplan_neun.py`, weil die Stelle, die sie prüfen, in `faltenplan_neun.py` liegt. `test_erste_falte_trockenlauf.py` und `test_horizontbeginn.py` sind unverändert |
| 4 | Die Proben für `loaderlauf.py` laufen mit einem Attrappen-Bot. Ein echter Bot im Wegwerfbaum hätte `shared/` und `strategies/` ganz gebraucht; der Attrappen-Bot hält denselben Vertrag (`DATA_DIR` als Modulvariable aus dem Resolver) |
| 5 | Die C5-Läufe schreiben ihre Tabelle nach `<scratch>/c5/bm_lauf{1,2}/benchmark.json`, nicht unter `ergebnisse/`. Keine neue Tabelle im Repo (Abbruchkriterium 1 greift nicht) |
| 6 | Die Vergleichsausgaben aus B0 (684 KB JSON) liegen nur im Scratchpad; im Beleg stehen ihre Hashes |
| 7 | Die Haken-Modulliste fehlt bei den Loader-Kindprozessen, weil ihr eigener Schreibschutz das Schreiben verweigert. D1 führt sie über die Öffnungen von `.py`/`.pyc` (`d1_listen.py`, Quelle (b)) |

## 7. Was NICHT geschah

Kein Registertext. Keine neuen Handelslisten, kein Erzeuger. Keiner der vier Rückfälle wurde behoben.
`herkunft.py`, `registerdaten.py`, `auswertung.py`, `shared/`, `strategies/`, `notifications/` und
`embargo_neun.py` sind unberührt. `faltenplan.json` ist unverändert, `python3 faltenplan.py` lief nie.
Keine neue Benchmark-Tabelle im Repo.

## 8. Für die Folgesitzung vorbereitet (TB-105; Register 41/42)

- **TB-105, die vier Rückfälle.** Rangfolge und Stellen aus Abschnitt 5 und `d3_vier_rueckfaelle.txt`.
  Die Dateien, die eine Freigabe brauchen:
  (b) `strategies/t3_supertrend/equity_simulation.py`, `multi_symbol_optimise.py`,
  `strategies/volatility_breakout_crypto/equity_simulation.py` (Einbau `regimewache.btc_daten`);
  (c) 9 × `equity_simulation.py` und 5 × `multi_symbol_optimise.py`, unter dem Modus `exit(2)`;
  (d) `faltenplan.py` (Punkt 2), `benchmark.py` (Punkte 4/6), `auswertung.py` (Punkte 3/5/14);
  (a) `shared/symbols_config.py`. Jeder mit einer Gegenprobe „Rückfall erreichbar gemacht ⇒ rc 2".
- **Dazu:** das Schreibziel `manuelle_eingriffe.log` (Frage 6), die Ordneranlage durch
  `strategy_paths.py:129-130` und `bot_lauf.py:63` unter dem Modus (A6) und die `$TMPDIR`-Ablagen
  (Frage 1).
- **Register 41/42:** Tatsachennotizen zu A4 (Verfahren verschieden, Ergebnis gleich), A5, A6, A7, zum
  Laufbereich (80 Module, drei Lauf-Typen) und zur Feldliste von `G8` (aus dem Code, Frage 3). Der Hash
  des neuen Abbilds `cb4eb1b4…` gehört ins Register.
- **Vorhanden zum Wiederverwenden:** `docs/belege/TB-104/haken/` (Lesen, Ordneranlage, Modulliste),
  `c5_lauf.sh` (Benchmark, Auswertungsimport, Bot im Modus), `d_auswerten.py` (drei Klassen),
  `d1_listen.py`, `d2_rueckfaelle.py`, `b0_ausgaben.sh` (8 Ausgaben ohne Modus).

---

## In einfacher Sprache

Mehrere Rechenprogramme haben ihre Dateipfade bisher selbst zusammengebaut. Jetzt fragen sie die zentrale
Pfadstelle. Im geschützten Modus lesen sie damit nur noch aus dem eingefrorenen Datenstand; wer ihnen
einen anderen Ordner unterschieben will, bekommt einen Abbruch. Ohne Modus rechnen alle Programme Byte
für Byte dasselbe wie vorher.

Aus dem Zeitplan der Auswertung sind drei Werte eines alten Verfahrens verschwunden, sonst hat sich
nichts bewegt. Die Vergleichstabelle ist im geschützten Modus zweimal neu gerechnet worden und Byte für
Byte gleich geblieben.

Gemessen wurde auch, welche Programme ein geschützter Lauf lädt: 80 Stück. Alle vier noch offenen
Notlösungen stecken in solchen Programmen, zwei davon werden im heutigen Lauf auch wirklich ausgeführt.
Nebenbei zeigte sich: Beim Laden öffnet der Lauf eine Protokolldatei im Repo zum Schreiben, und er legt
Zwischendateien im Temp-Ordner an, die liegen bleiben. Beides ist für den nächsten Auftrag notiert.

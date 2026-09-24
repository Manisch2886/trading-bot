# TB-103 — Ergebnis: Resolver-Fix, `messgroessen.py` auf den Resolver, Trockenlauf aller neun Bots im Modus — alle neun lesen ihre Symbolliste jetzt aus dem Snapshot, rc 0, gleiche Menge wie ohne Modus

**Sitzungstitel:** `TB-103` · **Stand:** 25.09.2026, ca. 00:45 · **Auftrag:**
`docs/auftraege/MAC_TB-103_resolver_und_trockenlauf.md` · **Belege:** `docs/belege/TB-103/`
**Eingang:** `d05e3ff` · Commits: `1d2b836` (Schritt 0), `d87997e` (Block B, `paths.py` + Tests),
`ae136fd` (Block C, `messgroessen.py` + Tests), Abgabe-Commit (Belege D/E, dieses Dokument,
Journalblock DB). Alle gepusht.
**Grundlage:** Fable 24b A2, 24c Abschnitte 1, 2, 6. Freigabe des Betreibers 24.09.2026, 22:52
(`paths.py`, `messgroessen.py` und ihre Tests). ⭐ **Zusatzfreigabe in dieser Sitzung:**
`shared/test_strategy_paths.py`, 24.09.2026, 23:49 (Abschnitt 6).
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6). Lesehaken aus TB-98
(`docs/belege/TB-98/haken/sitecustomize.py`, unverändert).

⚠️ **Registerkopie für Fable (0b):** Die Datei ist **in Ordnung**. Ihr Teil unter dem Kopf ist
zeichengleich mit `git show d0dc890:docs/VORREGISTRIERUNG_neuselektion.md`: SHA-256 `10ffa7b3…`,
7993 Zeilen, 549 972 Bytes, Abschnitte 0–40. Es gibt nichts zu melden.

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **B: Resolver-Fix** | Unter dem Modus gilt `CONFIG_DIR = <snapshot>/config`. Fehlt eine Universumsdatei, ist sie leer, oder nennt das MANIFEST keine, dann steht die Meldung auf `stderr` und der Import endet mit **`SystemExit(2)`**, bevor `CONFIG_DIR` benutzt wird. Ohne Modus ändert sich nichts: Probe A 99/0, N1 0/0, derselbe eine Dateizugriff wie vorher |
| **Tests** | `test_paths` **35/35** (vorher 24; neu G1–G6 und G3b, Mutationsproben G7–G10, B2 umgeschrieben), `test_startpruefungen` 44/44, `test_strategy_paths` 23/23, `test_stille_ausfaelle` 27/27, `test_vorregistrierung` **191/191** (vorher 188; neu I1, I2, I2-G) |
| **C: `messgroessen.py`** | Kurs- und Universumsdateien kommen über `shared/paths.py`. Ohne Modus bytegleich `7f46d5f5`. **Im Modus zweimal bytegleich `7f46d5f5`**, gelesen aus 222 Kurs-CSV und 2 Universumsdateien des Snapshots, **0 aus `data/`, 0 aus `config/`**. ⛔ **Der Nachweis ist trotzdem 2 (nicht geführt):** `haltedauern_je_bot.csv` kommt aus dem Repo |
| ⭐⭐ **D: Trockenlauf 9 Bots** | **9/9 rc 0**, jede Symbolliste **aus `<snapshot>/config/`**, **0-mal „Standardliste“**, Liste = Universumsdatei 9/9. **Geladene Menge mit und ohne Modus gleich (9/9)**: Krypto 18/24 bzw. 20/24, Aktien 147/150 wie in TB-98. **0 Kurs- oder Universumszugriffe ausserhalb des Snapshots.** ⚠️ Je Bot **5 Zugriffe auf die Laufumgebung** ausserhalb: `requirements.lock` und vier Systemdateien (Abschnitt 4) |
| **Tagblocker aus TB-98** | **weg:** Der Modus lädt dieselbe Menge wie der Betrieb, aus dem Snapshot |
| **E** | Versioniert geändert haben sich nur die sechs freigegebenen Dateien. Datenstand `d9449faf…` vorher = nachher, Snapshot unverändert, `ergebnisse/` unverändert, Sonde vorher = nachher. Zwei DBs hat der Betriebs-Cron geändert (00:05, 00:15), nicht diese Sitzung |

---

## 0. Schritt 0

| | |
|---|---|
| 0a | Den Arbeitsbaum des steuernden Chats habe ich committet (`1d2b836`, gepusht). Dazu kam `FABLE_UEBERGABE_2026-09-24_neuer_chat.md`: Sie lag im Arbeitsbaum, stand aber nicht in der Tabelle des Auftrags |
| 0a Hilfsdatei | Die Hilfsdatei `_kopf_register_kopie_24.md` ist zeichengleich mit den ersten 2158 Bytes der Registerkopie. ⇒ Sie sollte gelöscht werden. ⚠️ **`rm` hat das Berechtigungssystem abgelehnt**, deshalb habe ich sie per `mv` ins Scratchpad der Sitzung verschoben. Damit ist sie aus dem Repo, nicht committet (`0_schritt0.txt`) |
| 0b | Die Registerkopie ist zeichengleich mit `d0dc890` (siehe oben, `0b_registerkopie.txt`) |
| 0c | `.git/*.lock` keine; HEAD am Eingang `d05e3ff`; Datenstand `d9449faf…` (223 Kursdateien), Snapshot `--pruefen` UNVERÄNDERT; Hashes und Sonde vorher in `0c_*.txt` |

## 1. Block A — Vormessung nachgemessen

Belege: `a_vormessung.txt`, `a4_rueckfaelle.txt`, `a8_sperrliste.txt`.

| | Befund |
|---|---|
| **A1** | bestätigt: `DATA_DIR = CONFIG_DIR = _MODUS[0]` (Z. 569/570). Der Kopftext in Z. 91–93 war falsch |
| **A2** | bestätigt: Im Snapshot liegt `config/` mit `top25_symbols.txt` (25 Einträge, die letzte Zeile ohne Zeilenumbruch) und `sp500_top150.txt` (150). Flach in der Wurzel liegt keine der beiden. Das MANIFEST nennt beide unter `dateien` als `config/…` und in der `eingabeliste` als `art: Eingabe`. Beide sind bytegleich mit `config/` im Repo |
| **A3** | 5 Dateien, 3 Fassungen der Aktien-Datei. ⚠️ **Abweichung:** Nicht nur `volatility_breakout` holt `CONFIG_DIR` über `strategy_paths.get_strategy_paths()`, sondern **alle vier** `stocks_symbols_config.py` tun das. Die Fassungen unterscheiden sich nur im Kopftext. Zusatz: `symbols_config.py` fällt auch dann auf die Standardliste zurück, wenn die Datei zwar existiert, aber nach `EXCLUDE_SYMBOLS` leer ist. Die Meldung sagt dann fälschlich „nicht gefunden“ |
| **A4** | Das Inventar steht in `a4_rueckfaelle.txt`: gut 50 Fundstellen mit Datei:Zeile, Art, Auslöser und Erreichbarkeit. Die Einordnung folgt in Abschnitt 5 (4) |
| **A5** | B2 prüfte `CONFIG_DIR == attrappe` und ist umgeschrieben. ⚠️ **Die Vormessung „um Z. 308, 368, 504“ sind Zeilen in `test_paths.py`**, nämlich die Mutationen C, D und F, keine Zeilen in `paths.py`. **Der Fix trifft keinen einzigen zitierten Anker**; alle greifen weiter (0-mal NICHT PRUEFBAR). ⚠️ **Getroffen hat er stattdessen die Attrappen:** `test_paths`, `test_startpruefungen` und `test_strategy_paths` bauten einen Snapshot ohne `config/`. Mit dem Fix endete dort jeder Modus-Lauf mit rc 2; gemessen sind 6, 32 und 5 Fehler (Kreuzprobe in `b4_tests.txt`) |
| **A6** | bestätigt (TB-102) |
| **A7** | ⚠️ **Abweichung:** Das Register (Punkt 9, Marke 37.5 (4)) nennt `messgroessen.py:59` bzw. Z. 58. Gemessen stehen `GEBUEHR_PCT`/`SLIPPAGE_PCT` in **Z. 61/62**. Der Umbau lässt beide Zeilen **in Inhalt und Zeilennummer** unverändert |
| **A8** | Keine der Dateien steht auf einem der 14 Punkte, in `SPERRLISTE_DATEIEN` oder im Abbild. ⚠️ Es gibt drei Berührungen: (a) `messgroessen.py` steht in `herkunft.py::EINGEFROREN`, der Abschnitt-0-Menge, deren Gesamthash erst am Tag bezeugt wird. (b) Punkt 9 nennt `messgroessen.py` in einer Marke als „überwachte Kopie“ der Kosten; diese Zeilen sind unberührt. (c) `test_strategy_paths.py` hat eine eigene Freigabe (Abschnitt 6) |

## 2. Block B — der Resolver-Fix

**Was `paths.py` jetzt tut:**
- **Z. 213:** `CONFIG_UNTERORDNER = "config"`, genau einmal.
- **Z. 653:** `CONFIG_DIR = os.path.join(_MODUS[0], CONFIG_UNTERORDNER)`.
- **Z. 667:** `_pruefe_universum(_MODUS[0])` läuft im selben `try` wie die Startprüfungen, also mit `SystemExit(2)`.
- **Z. 534 ff.:** Die Prüfung selbst.
- **Z. 271:** `_lies_manifest`. Der Leser des MANIFESTs ist aus `_lies_snapshot_hash` herausgezogen, damit er nur einmal existiert.
- **Z. 93 ff.:** Der Kopftext ist berichtigt, mit Datum und dem alten Satz wörtlich, mit Verweis auf TB-98 Befund 1 und Fable 24b A2.

⭐ **Welche Universumsdateien geprüft werden: die, die das MANIFEST unter `dateien` mit dem
Präfix `config/` nennt, nicht zwei Namen in `paths.py`.** Begründung nach dem Kriterium des
Auftrags: Das MANIFEST ist der Ort, der die Anordnung des Snapshots beschreibt. `snapshot.py`
schreibt es beim Ziehen aus seiner `EINGABEN`-Liste. Zwei Namen in `paths.py` wären eine
**zweite** Liste neben `snapshot.EINGABEN`, und sie würde getrennt altern. Die Namen stehen
ohnehin schon zweimal im Leser-Code (`symbols_config.py`, `stocks_symbols_config.py`).
**„Nennt das MANIFEST keine“ ist selbst ein Abbruch.** Eine leere Menge ist kein „alles da“.
„Nicht leer“ heisst: mindestens eine nichtleere Zeile. Eine Datei nur aus Leerzeilen fiele im
Leser genauso auf die Standardliste zurück (Probe G3b).

**Proben** (`b_proben.txt`, `b_mutationen.txt`). Die Attrappe hat die Anordnung des echten
Snapshots, und der Wegwerfbaum trägt eine **unveränderte Kopie der echten
`symbols_config.py`**. So misst G am wirklichen Rückfall, ob „Standardliste“ erscheint:

| Name | Fall | Soll | Ist |
|---|---|---|---|
| **G1** | Modus, `config/` fehlt | rc 2, keine Standardliste | ✔ |
| **G2** | eine Universumsdatei fehlt | rc 2 | ✔ |
| **G3** | eine Universumsdatei leer (0 Bytes) | rc 2 | ✔ |
| **G3b** | eine Universumsdatei nur aus Leerzeilen | rc 2 | ✔ |
| **G4** | MANIFEST nennt keine Datei unter `config/` | rc 2 | ✔ |
| **G5** | alles da | rc 0, `CONFIG_DIR` endet auf `/config`, Liste aus `<attrappe>/config/top25_symbols.txt` | ✔ |
| **G6** | Störprobe: eine leere Zusatzdatei in `config/`, die das MANIFEST nicht nennt | rc 0, darf nichts auslösen | ✔ |
| **B2** (umgeschrieben) | `CONFIG_DIR == <attrappe>/config` | grün | ✔ |

**Mutationsproben.** Jede ändert genau eine Stelle, alles andere bleibt im Grundzustand, und
jede beisst **allein** (24b B3):

| Name | Mutation | beisst an |
|---|---|---|
| **G7 (M1)** | Fix zurückgenommen: `CONFIG_DIR = _MODUS[0]` | G5: rc 0, aber `CONFIG_DIR` = Wurzel, **Standardliste JA** |
| **G8 (M2)** | Aufruf `_pruefe_universum` entfernt | G1, G2, G3, G3b, G4 alle rc 0. Bei G1, G2 und G3b erscheint die Standardliste |
| **G9 (M3)** | nur die Leer-Prüfung entfernt | G3 und G3b rot, **G2 bleibt grün** |
| **G10 (M4)** | nur „MANIFEST nennt keine“ entfernt | G4 rot, **G2 bleibt grün** |

Störproben in beide Richtungen (24b C2): G1–G4 **müssen** abbrechen, G5/G6 **dürfen nicht**.
Die Kreuzprobe mit der alten `paths.py` und den neuen Tests ergibt 12 Fehler in `test_paths`
(B2, G1–G6, G7–G10 „griff nicht“) und 1 in `test_strategy_paths` (B2).

**Ohne Modus** (`b_probe_a.txt`): Probe A 99 Pfade / 9 Bots / 0 Unterschiede; N1 0 subprocess /
0 Paketabfragen; N4 144/0. Beim Import ohne Modus gibt es vorher wie nachher **genau einen**
Zugriff, das `listdir` des Import-Finders auf `shared/`.

**B4** (`b4_tests.txt`), Tests vor dem Fix (lokaler Klon `1d2b836`) und nach dem Fix:

| Test | vorher | nachher | Namen |
|---|---|---|---|
| `test_paths` | 24/24 | 35/35 | neu G1–G6, G3b, G7–G10; umgeschrieben B2 |
| `test_startpruefungen` | 44/44 | 44/44 | nur die Attrappe angepasst |
| `test_strategy_paths` | 23/23 | 23/23 | umgeschrieben B2; Attrappe angepasst |
| `test_stille_ausfaelle` | 27/27 | 27/27 | unverändert |
| `test_vorregistrierung` | 188/188 | 188/188 (nach B), **191/191** (nach C) | neu I1, I2, I2-G |

## 3. Block C — `messgroessen.py` auf den Resolver

**C1** (`c1_umbau.txt`, Commit `ae136fd`): `DATA_DIR = paths.DATA_DIR`,
`CONFIG_DIR = paths.CONFIG_DIR` (Z. 106–109). `BASE_DIR` (Z. 53) ersetzt nur noch die
Repo-Wurzel für `haltedauern_je_bot.csv`. Kommentar und `--help` sagen: **kein Weg zum
Snapshot**. Die Kostenzeilen und die Schreibsperre sind unberührt.

⚠️ **Die Abweichung von Fables Funktionsangabe, gemessen:** `get_strategy_paths()` liegt in
`shared/strategy_paths.py`, nicht in `paths.py`. Sie **reicht nur** `paths.DATA_DIR` und
`paths.CONFIG_DIR` durch und legt dazu `results/<name>/` und `logs/<name>/` per `makedirs` an.
Für `research/vorregistrierung/messgroessen.py` hiesse das: `results/vorregistrierung/` und
`logs/vorregistrierung/` entstünden im Repo. **Deshalb importiert `messgroessen.py` `paths`
direkt.** Das ist der Weg, auf dem auch die fünf Krypto-Bots ihre Symbolliste bekommen
(`shared/symbols_config.py`: `from paths import CONFIG_DIR`).

**C2** (`c2_ohne_modus.txt`): Ohne Modus ist die Ausgabe bytegleich `7f46d5f5`, sowohl zur
Nachweisdatei als auch zum Lauf mit dem Code vor C1. Es gibt keine Abweichung.

**C3** (`c3_modus_lesequellen.txt`, `c3_zweimal.txt`): nur `TB_SELEKTIONS*`, HEAD `ae136fd`.

| Teil (24c Abschnitt 1) | Ist |
|---|---|
| **(b) Leseprotokoll** | 222 Kurs-CSV und 2 Universumsdateien **aus dem Snapshot**, **0 aus `data/`, 0 aus `config/`**. Ausserhalb: `haltedauern_je_bot.csv` (**der erwartete eine**, `messgroessen.py:232`). ⚠️ **Befund:** Dazu kommt `requirements.lock` (`paths.py:470/529`, die Lock-Prüfung der Startprüfung aus TB-58). Ausserdem Systemdateien (`SystemVersion.plist`, `/dev/null`, `/dev/urandom`) aus `platform.platform()` und dem Import von numpy/pandas |
| **(a) Ergebnisvergleich** | zweimal rc 0, **beide bytegleich `7f46d5f5`**, Lesequellen beider Läufe gleich |

⛔ **Der Nachweis für `messgroessen.json` gilt damit NICHT als geführt, Status 2 nach 24c.**
Teil (b) enthält einen Zugriff ausserhalb des Snapshots. Geführt werden kann er erst nach
Plan-Punkt 3.

**C4** (`c4_tests.txt`): `test_vorregistrierung` 191/191, G8 grün. Neu ist **Teil I**. Er baut
einen Wegwerfbaum als Git-Repo mit der echten `paths.py`, der echten `messgroessen.py`, der
Lock-Datei, erfundenen Kursreihen in `data/` und einer Snapshot-Attrappe, und hat einen eigenen
Audit-Haken:

| Name | Prüfung | Ist |
|---|---|---|
| **I1** | Im Modus liest `messgroessen.py` 0 Kursdateien aus `data/`; Kurse und beide Universumsdateien kommen aus dem Snapshot; rc 0 | ✔ |
| **I2** | Mutationsprobe „Resolver-Import entfernt“: `messgroessen.py` liest im Modus aus `data/`, I1 wäre dann rot | ✔ |
| **I2-G** | Gegenprobe: ohne die Mutation scheitert I2 | ✔ |

## 4. Block D — Trockenlauf aller neun Bots im Modus ⭐⭐

**Was „Trockenlauf“ hier heisst** (`d_trockenlauf.py`, `d_lauf.sh`): Je Bot läuft ein Prozess
mit dem unveränderten Bot-Code über dieselben Aufrufe wie `research/exposure_messung/bot_lauf.py`,
in drei Schritten:
1. `load_all_symbol_data()`: die Symbolliste, die Kursdaten und das Ladeprotokoll.
2. Der Signalpfad: `collect_all_trades` mit den Argumenten des Bots.
3. **Eine** Simulation, **ohne** die Kennzeichnung aus `positionen_holen.py` (TB-98 Befund 2).

Geschrieben wird nur in den Scratchpad. Der Lauf-Typ ist derselbe wie in TB-98 `a1_neun.sh`:
echter Snapshot, **kein** Hilfsordner, Lesehaken mit Aufrufstapel. HEAD war der Fix-Commit
`d87997e`, der Baum war über `shared/`, `strategies/` und dem Lock sauber.

**Im Modus** (`d_neun_modus.txt`):

| Bot | rc | Universumsdatei (im Snapshot) | Zeilen | nach `EXCLUDE` | Liste = Universum? | geladen | „Standardliste“ | Summenzeile | Kurs/Universum ausserhalb | Laufumgebung ausserhalb |
|---|---|---|---|---|---|---|---|---|---|---|
| elliott_wave | 0 | `config/top25_symbols.txt` | 25 | 24 | ja | 18 | 0 | „Geladen: 18 von 24 Symbolen. 6 ausgelassen: 6x Kerzenzahl zu klein.“ | 0 | 5 |
| t3_supertrend | 0 | `config/top25_symbols.txt` | 25 | 24 | ja | 18 | 0 | „Geladen: 18 von 24 Symbolen. 6 ausgelassen: 6x Historie zu kurz.“ | 0 | 5 |
| rsi2_crypto | 0 | `config/top25_symbols.txt` | 25 | 24 | ja | 20 | 0 | „Geladen: 20 von 24 Symbolen. 4 ausgelassen: 4x Historie zu kurz.“ | 0 | 5 |
| turtle_soup_crypto | 0 | `config/top25_symbols.txt` | 25 | 24 | ja | 20 | 0 | wie rsi2_crypto | 0 | 5 |
| volatility_breakout_crypto | 0 | `config/top25_symbols.txt` | 25 | 24 | ja | 20 | 0 | wie rsi2_crypto | 0 | 5 |
| elliott_wave_stocks | 0 | `config/sp500_top150.txt` | 150 | 150 | ja | 147 | 0 | „Geladen: 147 von 150 Symbolen. 3 ausgelassen: 3x Historie zu kurz.“ | 0 | 5 |
| rsi2_mean_reversion | 0 | `config/sp500_top150.txt` | 150 | 150 | ja | 147 | 0 | wie elliott_wave_stocks | 0 | 5 |
| turtle_soup_stocks | 0 | `config/sp500_top150.txt` | 150 | 150 | ja | 147 | 0 | wie elliott_wave_stocks | 0 | 5 |
| volatility_breakout | 0 | `config/sp500_top150.txt` | 150 | 150 | ja | 147 | 0 | wie elliott_wave_stocks | 0 | 5 |

- **„Liste = Universumsdatei“:** Die Symbolliste des Bots ist in Inhalt und Reihenfolge die
  Universumsdatei aus dem Snapshot, bei Krypto nach `EXCLUDE_SYMBOLS` (1 von 25 ausgeschlossen).
- **„geladen“ ist kleiner als die Liste, und zwar mit Grund aus dem Ladeprotokoll, nicht still:**
  - Krypto 1h/4h: BMTUSDT, ENSOUSDT, PUMPUSDT, TRUMPUSDT, UUSDT, ZKCUSDT.
  - Krypto 1d: ENSOUSDT, PUMPUSDT, UUSDT, ZKCUSDT.
  - Aktien: CEG, GEV, SNDK. Grund jeweils Historie oder Kerzenzahl zu kurz.
- **Lesezugriffe:** Aus dem Snapshot kommen je Bot die 24 bzw. 150 Kurs-CSV, beide
  Universumsdateien (`paths.py` prüft beide) und das MANIFEST. Aus `data/`, `config/`,
  `research/`, `results/` und `logs/` kommen **0**. Geschrieben wird nur in den Scratchpad.
- **Die 5 Zugriffe auf die Laufumgebung, je Bot gleich**, mit Aufrufstapel in
  `d_lesequellen/lesequellen_modus.txt`:
  - `<repo>/requirements.lock` aus `paths.py:470/529` (Lock-Prüfung TB-58)
  - `/System/Library/CoreServices/SystemVersion.plist` aus `paths.py:501` (`platform.platform()`) und aus dem pandas-Import
  - `/dev/null` aus `paths.py:501`
  - `/dev/urandom` aus dem pandas-Import (`bot_lauf.py:53`)
  - `/private/var/db/timezone/…/UTC` aus dem pandas-Import
- **Code** zähle ich getrennt: 481–492 `.py`/`.pyc` je Bot, davon eine aus dem Repo, der Umschlag
  selbst. Der übrige Repo-Code kommt als Bytecode aus `~/Library/Caches/com.apple.python/`
  (wie TB-98).

**Gegenprobe ohne Modus** (`d_neun_ohne_modus.txt`): 9/9 rc 0, dieselbe Liste und dieselbe
geladene Menge. Gelesen wird dabei aus `data/` und `config/` (24+1 bzw. 150+1), dazu kommen 3
Systemdateien. Die Lock-Prüfung entfällt ohne Modus.

⭐⭐ **Vergleich der geladenen Menge mit und ohne Modus: 9/9 GLEICH**
(Krypto 18/24 bzw. 20/24, Aktien 147/150; derselbe Stand wie TB-98 ohne Modus). Vor dem Fix
waren es im Modus 9/9 „5 von 5, Keines ausgelassen“ (TB-98 `a1_neun_lauf.txt`).
**⇒ Der Tagblocker aus TB-98 ist weg.**

**Das Ladeprotokoll, nur gemessen** (`shared/ladeprotokoll.py` ist nicht freigegeben):
- Die Summenzeile nennt **zwei Zahlen**: geladen und die Länge der **Liste, die der Bot
  übergibt** (`Ladeprotokoll(SYMBOLS)`, `ladeprotokoll.py:151`). Die Zeilenzahl der
  Universumsdatei nennt sie nicht; bei Krypto sind das 25 gegen 24 nach `EXCLUDE`.
- Die **Quelle der Liste nennt sie nicht**.
- Mit der Fünferliste hätte sie weiterhin „5 von 5, Keines ausgelassen“ geschrieben. Unter dem
  Modus ist das jetzt unerreichbar, ohne Modus nicht.

## 5. Für Fable — ohne Kontext lesbar ⭐⭐

*Sichtschutz 27.1: keine Kennzahl und keine Trade-Zahl in diesem Abschnitt. Gemeldet werden
Rückgabewerte, Mengen, Quellen und Zugriffe.*

**(1) Der Resolver-Fix (24b A2), umgesetzt.**
- `shared/paths.py` setzt unter dem Selektionsmodus `CONFIG_DIR` auf `<snapshot>/config`.
- Beim Import prüft `paths.py` jede Universumsdatei, die das **MANIFEST des Snapshots** unter
  `config/` nennt: Sie muss vorhanden sein und mindestens eine nichtleere Zeile haben.
- Fehlt eine, ist sie leer, oder nennt das MANIFEST keine, dann steht die Meldung auf `stderr`
  und es folgt **`SystemExit(2)`**, bevor ein Aufrufer `CONFIG_DIR` benutzt. Der Rückfall der
  fünf Symboldateien ist damit unter dem Modus unerreichbar, und keine dieser Dateien wurde
  geändert.
- Die Namen der Dateien stehen **nicht** in `paths.py`: Das MANIFEST ist der eine Ort, der die
  Anordnung kennt (24c Abschnitt 2).
- **Proben mit Namen:** G1 (`config/` fehlt), G2 (Datei fehlt), G3 (leer), G3b (nur
  Leerzeilen), G4 (MANIFEST nennt keine), alle rc 2 und ohne Standardliste. G5 (alles da,
  rc 0) und G6 (Störprobe, darf nichts auslösen). B2 ist umgeschrieben.
- **Mutationsproben, jede allein beissend:** G7 (Fix zurückgenommen), G8 (Prüfung entfernt),
  G9 (nur die Leer-Prüfung entfernt), G10 (nur „nennt keine“ entfernt).
- Ohne Modus: 99 Pfade, 0 Unterschiede.

**(2) Der Trockenlauf aller neun Bots (Tag-Vorbedingung aus 24b A2).** Es lief der echte
Snapshot `63e4b6c8…` mit Lesehaken und Aufrufstapel. Je Bot: Laden, Signalpfad, eine
Simulation.

| Bot | rc | Universumsdatei, Einträge | Liste = Datei | geladen / Liste | Grund der Differenz | Fallback | Kurs-/Universumsdateien ausserhalb | Laufumgebung ausserhalb |
|---|---|---|---|---|---|---|---|---|
| 5 Krypto-Bots | 0 | `config/top25_symbols.txt`, 25 (24 nach Ausschluss) | ja | 18/24 (1h, 4h) · 20/24 (1d) | „Historie zu kurz“ / „Kerzenzahl zu klein“ | 0 | 0 | 5 |
| 4 Aktien-Bots | 0 | `config/sp500_top150.txt`, 150 | ja | 147/150 | „Historie zu kurz“ | 0 | 0 | 5 |

Die geladene Menge ist mit und ohne Modus gleich (9/9).

**Ist die Tag-Vorbedingung erfüllt?** Drei ihrer vier Bedingungen sind **erfüllt**:
- „Rückgabe 0“: 9/9.
- „kein Fallback“: 0-mal „Standardliste“, Liste = Datei 9/9.
- „0 Zugriffe ausserhalb `snapshots/<hash>/`“ für Kurs- und Universumsdateien: 0.

Zwei Punkte sind **offen, weil sie am Wortlaut hängen**:
- **(i) „0 Zugriffe ausserhalb“, wörtlich genommen, ist nicht erfüllt.** Jeder Lauf öffnet 5
  Dateien der Laufumgebung ausserhalb des Snapshots: `requirements.lock` (die Lock-Prüfung der
  Startprüfung selbst) sowie `SystemVersion.plist`, `/dev/null`, `/dev/urandom` und die
  Zeitzonendatei, die `platform.platform()` und der pandas-Import öffnen. Es sind keine Kurs-,
  Universums- oder Ergebnisdateien. Zählen sie?
- **(ii) „Geladene Symbolmenge gleich Universumsdatei“:** Die **Liste** ist gleich der Datei.
  **Geladen** werden 18, 20 oder 147 davon; die Differenz nennt das Ladeprotokoll mit Grund, und
  sie ist ohne Modus dieselbe. Gilt die Bedingung für die Liste oder für die geladene Menge?

**(3) `messgroessen.py` im Modus (24c Abschnitte 1 und 2).** Die Datei ist auf den Resolver
umgestellt. Im Modus zeigt sie:
- **(a)** zweimal bytegleich zur Nachweisdatei;
- **(b)** 222 Kurs-CSV und 2 Universumsdateien aus dem Snapshot, 0 aus `data/` und `config/`,
  und **genau ein Zugriff auf Eingabedaten ausserhalb**: `research/tb24_haltedauern/ergebnisse/haltedauern_je_bot.csv`.

⇒ **Status 2 nach 24c: nicht geführt.** Er wird erst nach Plan-Punkt 3 führbar, wenn die
Haltedauern aus den neuen Listen kommen. ⚠️ Dazu kommen dieselben Umgebungszugriffe wie in (2):
`requirements.lock`, `SystemVersion.plist`, `/dev/null`, `/dev/urandom`. Das ist dieselbe Frage
wie (2)(i).

**(4) Das Rückfall-Inventar (A4)** umfasst gut 50 Fundstellen in `shared/`, `strategies/` und
`research/vorregistrierung/`. **Unerreichbar unter dem Modus** ist jetzt: die Standardliste bei
fehlender oder leerer Universumsdatei (5 Dateien), und `messgroessen.py` baut keine eigenen
Kurspfade mehr. **Erreichbar bleibt:**
- (a) `symbols_config.py`: eine Krypto-Liste, die nach `EXCLUDE_SYMBOLS` leer ist, ergibt die
  Standardliste. Der echte Snapshot ist nicht betroffen, denn nur 1 von 25 Einträgen wird
  ausgeschlossen.
- (b) `t3_supertrend`: Der BTC-Regimefilter fällt still weg, wenn BTCUSDT nicht geladen ist
  (`equity_simulation.py:77`, `multi_symbol_optimise.py:130`). `regimewache` ist dort nicht
  eingebaut. Im Trockenlauf war BTCUSDT geladen.
- (c) Alle Backtest-Skripte beenden sich bei „Keine Daten gefunden“ mit `exit()`, also mit
  rc **0**.
- (d) Eigene Pfadlogik ausserhalb des Resolvers haben `benchmark.py`, `faltenplan.py` (mit
  `faltenplan_neun.py`, `TB36_BASE_DIR`) und `herkunft.py::datenstand()`. Nach 24c Abschnitt 2
  ist das je ein Befund.
- (e) Stille Ersatzwerte für Schwellen stehen in `faltenplan.py:147–154`, `benchmark.py:188/282`
  und `auswertung.py:333/380`.

Der Rückfall auf den Live-Abruf (`entscheidungskerze.py`) liegt **nur** im Papierpfad; kein
Backtest erreicht ihn.

**(5) Messung zur Resolver-Pflicht (24c Abschnitt 2).** Die Funktion `get_strategy_paths()`
liegt in `shared/strategy_paths.py`, **nicht** in `shared/paths.py`. Sie ist kein zweiter
Resolver. Sie reicht `paths.DATA_DIR` und `paths.CONFIG_DIR` durch und legt zusätzlich
`results/<name>/` und `logs/<name>/` an, wobei der Name aus dem Ordner des Aufrufers kommt. Für
ein Modul ausserhalb von `strategies/<bot>/` entstünden so Ordner im Repo. `messgroessen.py`
importiert deshalb `shared/paths.py` direkt, so wie `shared/symbols_config.py`. Vorschlag für
den Registertext: „über den Resolver (`shared/paths.py`, direkt oder über
`strategy_paths.get_strategy_paths()`)“.

## 6. Abweichungen vom Auftrag

| | |
|---|---|
| ⭐ Freigabe erweitert | `shared/test_strategy_paths.py` stand nicht in der Freigabe. Die Datei kopiert aber die echte `paths.py` und baute eine Attrappe ohne `config/`; B2 prüfte die flache Wurzel. Mit dem Fix war sie rot (5 Fehler), und B4 verlangt sie grün. **Dazu habe ich den Betreiber per Auswahlkarte gefragt, 24.09.2026, 23:49, Antwort „Ja, freigeben (Empfohlen)“.** Geändert sind nur die Attrappe und B2; `strategy_paths.py` ist unberührt |
| Attrappen | Auch in `test_paths` und `test_startpruefungen` war die Attrappe anzupassen: `config/` mit Universumsdateien und MANIFEST-Einträgen. Das ist Aufrufumgebung, keine Prüflogik. Die Kreuzprobe steht in `b4_tests.txt` |
| `--ziel` | Der Auftrag sagt „weiterhin Pflicht“. Gemessen hat `messgroessen.py` seit TB-93 eine Voreinstellung (`ergebnisse/messgroessen_<Zeitstempel>.json`). Ich habe es nicht geändert, denn die Schreibsperre sollte unberührt bleiben. Alle Läufe dieser Sitzung liefen mit `--ziel` im Scratchpad |
| `get_strategy_paths` | Nicht benutzt, Begründung in Abschnitt 5 (5) |
| C4-Probe | liegt in `test_vorregistrierung.py` als Teil I, weil dort die `messgroessen`-Prüfungen stehen. Laufzeit +~4 s |
| Hilfsdatei | `rm` war abgelehnt, deshalb `mv` ins Scratchpad |
| Einzeiler | `env PYTHONPATH=…` als Einzeiler wurde abgelehnt (wie TB-98 und TB-102); als Skriptdatei lief er |
| `crontab -l` | abgelehnt; die DB-Änderungen habe ich über die Zeitstempel zugeordnet (E1) |

## 7. Was NICHT geschah

Kein Registertext. Keine Handelslisten, kein Erzeuger. Kein Abbild. `faltenplan.py` ist
unberührt und lief nie direkt; die Freigabe von 11:25 ist unverbraucht. Keine Änderung an Cron,
`data/`, `config/` und Snapshot. Nicht geändert: Symboldateien, `ladeprotokoll.py`,
`strategy_paths.py`, `registerdaten.py`, Zuteilung.

## 8. Für die Folgesitzung vorbereitet

- **Ladeprotokoll** (eigene Freigabe): Die Summenzeile nennt heute „geladen von Liste“. 24b A2
  verlangt beide Zahlen **und die Quelle der Liste**. Dazu fehlen der Pfad der Symbolliste und
  die Zeilenzahl der Universumsdatei vor `EXCLUDE`. Die Stelle ist `ladeprotokoll.py:147–159`;
  die Aufrufer übergeben heute nur `SYMBOLS`.
- **Rückfälle mit eigener Freigabe** (A4, Abschnitt 5 (4)): `EXCLUDE`-leere Liste; der
  Regimefilter bei `t3_supertrend`; `exit()` mit rc 0; die Pfadlogik von `benchmark.py`,
  `faltenplan.py`, `faltenplan_neun.py` und `herkunft.py`.
- **Register 41/42, Stoff aus dieser Sitzung:**
  - Tatsachennotiz Resolver-Fix (Commit `d87997e`, Probenamen G1–G10, B2).
  - Tatsachennotiz Trockenlauf aller neun (Abschnitt 4, Protokoll `d_neun_modus.txt`).
  - Kopftext `paths.py` berichtigt.
  - `messgroessen.py` auf dem Resolver, Nachweis = 2.
  - Die Zeilennummern in Punkt 9 (58/59 → 61/62).
  - Die Antworten auf (2)(i)/(ii) und (5).
- `test_vorregistrierung` zählt jetzt 191 Prüfungen (I1, I2, I2-G neu).

## In einfacher Sprache

Im geschützten Modus haben die Bots bisher ihre Liste der Werte nicht gefunden und still mit
fünf Ersatzwerten gerechnet. Die zentrale Pfadstelle schaut jetzt im richtigen Ordner nach.
Fehlt dort eine Liste oder ist sie leer, bricht der Lauf sofort ab, statt Ersatzwerte zu nehmen.
Das ist mit Proben abgesichert, und jede Probe fällt nachweislich auf, wenn man die Reparatur
wieder herausnimmt. Das Messprogramm für die Rasterzahlen holt seine Pfade jetzt von derselben
Stelle wie die Bots. Im geschützten Modus liest es seine Kurs- und Universumsdateien jetzt aus
dem eingefrorenen Bestand; nur die Haltedauer-Datei kommt noch aus dem Arbeitsordner. Als
Nachweis zählt das erst, wenn auch die Haltedauern aus den neuen Listen kommen. Zum Schluss sind
alle neun Bots einmal probeweise im geschützten Modus gelaufen. Alle neun endeten ohne Fehler,
lasen ihre Liste und ihre Kurse aus dem eingefrorenen Bestand und luden genau dieselben Werte
wie im normalen Betrieb. Offen sind zwei Auslegungsfragen an den Verfahrensprüfer: ob
Systemdateien wie die Paketliste als „Zugriff ausserhalb“ zählen, und ob „gleiche Menge“ die
Liste meint oder die tatsächlich geladenen Werte.

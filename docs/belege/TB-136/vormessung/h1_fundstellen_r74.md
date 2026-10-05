# Bericht H1 — Fundstellen zu Fable 04a, Teil 0 und Frage 1 / R74 (Messung 2026-10-04)

Gemessen im Arbeitsbaum `$HOME/mnt/trading-bot`, HEAD `d781f1b8f86ca3b423b4032220ad4b304e4d131b`.
Abschnittskopien tragen im Kopf: Commit `ee43f5f1339549238c0da023db7c9f324b26d28e`, 2026-10-04.
Nur gelesen (grep, sed -n, awk, wc, ls, `git --no-optional-locks grep|log|ls-files|rev-parse`). Kein `git status`, kein `git diff`, nichts angelegt.

Kürzel: `K17` = `docs/projektfuehrung/register_kopie/REGISTER_KOPIE_ABSCHNITT_17.md` (entsprechend K27, K37, K47, K48, K51, K53); `REG` = `docs/VORREGISTRIERUNG_neuselektion.md`; `IDX` = `docs/projektfuehrung/REGISTER_INDEX.md` (liegt NICHT in `register_kopie/`, sondern eine Ebene höher).
Zeilenabbildung Kopie → Register: K17 Z. n = REG Z. n+2572; K53 Z. n = REG Z. n+11375; K37 Z. n = REG Z. n+6888.

## Ergebnistabelle

| Nr. | Befund | Ort |
|---|---|---|
| 1 | ja* (Wortfolge; mit `**`-Auszeichnung und Zeilenumbruch) | 17.5: K17 Z. 260–261 = REG Z. 2832–2833 |
| 2 | ja* (Wortfolge; mit `**` und Zeilenumbruch) | 17.5: K17 Z. 262–263 = REG Z. 2834–2835 |
| 3 | ja | 17.5: K17 Z. 261 („gemessen TB-47“) und Z. 281 („TB-47, `eingaben.json`, Feld `kalender`“) = REG Z. 2833, 2853 |
| 4 | ja (Zählung) | 17.5 (K17 Z. 252–284): `NYSE` 0, `XNYS` 0, `pandas_market_calendars` 1; ganzer Abschnitt 17: 0 / 0 / 2 |
| 5 | Feld gefunden, aber nicht in den vier genannten Dateien | `research/snapshotgrenze/ergebnisse/eingaben.json:96–106`; Importstelle/Dateipfad/`boersenkalender` darin: ja; Kalendername darin: nein |
| 6 (i) | ja | einzige Import-Anweisung: `notifications/boersenkalender.py:81` |
| 6 (ii) | ja | `notifications/boersenkalender.py:70` |
| 6 (iii) | ja | `notifications/boersenkalender.py:109` (einziges `get_calendar(`); `.schedule(` ebenda Z. 125 |
| 6 (iv) | ja | `research/vorregistrierung/`: 0 Treffer |
| 6 Lock | — | `requirements.lock:51` `pandas-market-calendars==4.6.1` |
| 7 | ja | 53.1 R66 (b): K53 Z. 9 = REG Z. 11384 (Byte 1172 der Zeile, innerhalb (b) = Byte 630–1315) |
| 8 | ja / ja | 53.1 R66 (b): K53 Z. 9 = REG Z. 11384 (Byte 951 und 1028; je ein zweites Vorkommen in (e), Byte 2879 / 3068) |
| 9 | ja (Wortlaut unten) | K53 Z. 9 = REG Z. 11384 |
| 10 | ja / ja / ja | 53.9: K53 Z. 69 = REG Z. 11444 |
| 11 | ja | 53.9: K53 Z. 76 = REG Z. 11451 (Zeile „R72 (53.7), zweite“) |
| 12 R59 (b) | ja | 51.4: K51 Z. 30 = REG Z. 11222 |
| 12 R28 | abweichend | 47.11: K47 Z. 82 („Kopie mit Probe“ 0, „Gegenprobe“ 0) |
| 13 | ja / ja | R72 (d): 53.7, K53 Z. 51 = REG Z. 11426; 27.2: K27 Z. 22 |
| 14 | abweichend (Satz) / ja (Test-Snapshot) | 48.14 R46: K48 Z. 112 |
| 15 | ja (R39, R45) / 37.5 (2) selbst führt die Worte nicht | R39: K48 Z. 58; R45: K48 Z. 106; 37.5 (2): K37 Z. 273 = REG Z. 7161 |
| 16 | ja | `v1_vormessung_04a.md` Z. 94, 125, 140, 328; Anfrage 04a Z. 15 |
| 17 | ja (Wortlaut unten) | 53.5 R70: K53 Z. 37 = REG Z. 11412 |
| 18 | ja | 51.1 R56 (b): K51 Z. 9 |
| 19 | ja | REG Z. 11382, 11396, 11403, 11410, 11431, 11438, 11456; IDX Z. 207 |
| 20 | ja | `FABLE_ANTWORT_2026-10-02c_…md` Z. 134, 137 |

## Ausschnitte und Zählungen

### 1, 2 (17.5)
K17 Z. 260–263, roh:
```
> ⭐ **Tatsachennotiz:** Der Handelskalender kommt **nicht aus einer Datei**,
> sondern aus dem Paket **`pandas_market_calendars`** (gemessen TB-47:
> Fassung **4.6.1** auf dem Betriebsrechner). Er ist damit **Umgebung, nicht
> Eingabe**, und liegt im Lock.
```
- Roh (`grep -o -F` auf K17 Z. 252–284, Zeilen verbunden): Zitat 1 = 0, Zitat 2 = 0.
- Nach Entfernen von `**` und des Zitatzeichens `> `, Zeilen verbunden: Zitat 1 = 1, Zitat 2 = 1.
- Gegenprobe im Register selbst: `grep -c -F` Zitat 1 = 1, Zitat 2 = 1 — die Trefferzeile ist in beiden Fällen REG Z. 11385 (Quelle des Grundes von R66 in 53.1), nicht 17.5. In 17.5 selbst (REG Z. 2832–2835) liefert `grep -F` wegen Auszeichnung/Umbruch 0.

### 3 (17.5)
K17 Z. 278–281:
```
⭐ **Warum der Kalender eigens genannt ist:** Er ist die einzige Eingabe des
Laufs, die **wie eine Datei aussieht und keine ist**. Wäre er Eingabe, gehörte
er in den Snapshot; als Paket gehört er in den Lock. Die Einordnung ist
gemessen worden (TB-47, `eingaben.json`, Feld `kalender`) und nicht geraten.
```
Zählung in 17.5: `TB-47` 2, `kalender` (klein) 2.

### 4 (17.5)
17.5 = K17 Z. 252–284: `NYSE` 0, `XNYS` 0, `pandas_market_calendars` 1.
Ganzer Abschnitt 17 (K17) und REG Z. 2575–3028: `NYSE` 0, `XNYS` 0, `pandas_market_calendars` 2.

### 5 (Feld `kalender`, TB-47)
Suche in den vier genannten Dateien (`grep -i kalender`):
- `docs/ERGEBNIS_TB-47_snapshotgrenze.md` (526 Z.): 9 Trefferzeilen, alle Fliesstext/Tabelle, kein Feld `kalender`. Z. 59: „| **Kommt der Handelskalender aus einer Datei oder aus einem Paket?** | ⭐ **Aus einem Paket.** `pandas_market_calendars`, `mcal.get_calendar()`. Keine Datei. Er ist **Umgebung**, gehört ins Lock — und er liegt **nicht** in der Hülle der 90. |“. Z. 89: „| NYSE-Handelskalender | `notifications/boersenkalender.py:81` | ⭐ **`pandas_market_calendars`** | — | **Umgebung** |“. Z. 104–105: „Die einzige Fundstelle im ganzen Repo ist `notifications/boersenkalender.py:81`:“. Z. 69: „**Rohdaten:** `research/snapshotgrenze/ergebnisse/eingaben.json`.“
- `docs/MACLAUF_TB-47_snapshotgrenze.md`: 0 Treffer.
- `docs/TESTAUFTRAG_TB-47_snapshotgrenze.md`: 0 Treffer.
- `research/datenordner_schnitt/ergebnisse/basislauf_tb47_mac.json`: 0 Treffer.
- `git grep -n -i kalender -- research/datenordner_schnitt docs/belege/TB-47*`: 1 Treffer: `research/datenordner_schnitt/erhebung.py:466:                "binance_historie.py", "boersenkalender.py"):`. `docs/belege/TB-47*`: keine verfolgten Dateien.

Das Feld steht (17.5 nennt die Datei: „TB-47, `eingaben.json`, Feld `kalender`“) in `research/snapshotgrenze/ergebnisse/eingaben.json`, Z. 96–106 (Commit der Datei: `fc38d25 TB-47 Teil 1: Erhebung der Nicht-Code-Eingaben der Selektionsseite`), wörtlich:
```
  "kalender": {
    "im_repo": [
      {
        "import": "pandas_market_calendars",
        "modul": "notifications/boersenkalender.py",
        "zeile": 81
      }
    ],
    "in_selektionshuelle": [],
    "paket_vorhanden": "5.4.0"
  },
```
- Importstelle genannt: ja (`"import": "pandas_market_calendars"`, `"zeile": 81`).
- Dateipfad genannt: ja (`"modul": "notifications/boersenkalender.py"`).
- `boersenkalender` genannt: ja.
- Kalendername (`NYSE`/`XNYS`) im Feld: nein (0).
- Erzeuger des Feldes: `research/snapshotgrenze/erhebung_eingaben.py:560` (`"kalender": kalenderfrage(wurzel, importe),`), Z. 609 (`"paket_vorhanden": _paketfassung("pandas_market_calendars"),`).
- 53.9 (K53 Z. 69) dazu wörtlich: „Das Feld `kalender` aus TB-47 (`research/snapshotgrenze/erhebung_eingaben.py:606–610`) führt Importstellen und Paketfassung, keinen Kalendernamen; 17.5 nennt keinen.“

### 6 (Code)
Vorgegebenes Kommando (`pandas_market_calendars|get_calendar|KALENDER_NAME|XNYS` in `*.py *.txt *.lock *.toml *.cfg`), 22 Trefferzeilen:
```
docs/belege/TB-58/teil_a/pip_freeze.txt:36:pandas_market_calendars==4.6.1
docs/belege/TB-58/teil_a/pip_freeze_all.txt:36:pandas_market_calendars==4.6.1
notifications/boersenkalender.py:38:GEWAEHLT: `pandas_market_calendars`. Begruendung siehe requirements.txt
notifications/boersenkalender.py:70:KALENDER_NAME = "NYSE"
notifications/boersenkalender.py:81:    import pandas_market_calendars as mcal
notifications/boersenkalender.py:87:        f"Die Bibliothek pandas_market_calendars ist nicht installiert "
notifications/boersenkalender.py:109:        _KALENDER = mcal.get_calendar(KALENDER_NAME)
notifications/boersenkalender.py:157:        "kalender": KALENDER_NAME,
notifications/boersenkalender.py:231:            "kalender": KALENDER_NAME,
requirements.txt:46:#   * exchange_calendars - dieselbe Datengrundlage (pandas_market_calendars
requirements.txt:57:# VERSION: Untergrenze 4.1 (ab da get_calendar/schedule in der hier benutzten
requirements.txt:65:pandas_market_calendars>=4.1,<5
research/registernachtrag_tb48/pruefe_abschnitt17.py:47:  * `pandas_market_calendars` **4.6.1** (17.5) - der Registertext sagt
research/snapshotgrenze/erhebung_eingaben.py:96:FREMDPAKETE = ("pandas_market_calendars", "exchange_calendars", "pandas",
research/snapshotgrenze/erhebung_eingaben.py:609:        "paket_vorhanden": _paketfassung("pandas_market_calendars"),
research/snapshotgrenze/erhebung_eingaben.py:669:          "`pandas_market_calendars` gebaut.")
shared/entscheidungskerze.py:362:                      "pandas_market_calendars fehlt).")
shared/snapshot.py:131:`pandas_market_calendars` (`mcal.get_calendar`), nicht aus einer Datei - er
shared/test_entscheidungskerze.py:33:`pandas_market_calendars` auf dem pruefenden Rechner liegt - und zusaetzlich,
shared/test_entscheidungskerze.py:169:                "grund": "Die Bibliothek pandas_market_calendars fehlt.",
shared/test_entscheidungskerze.py:328:        print("    uebersprungen: pandas_market_calendars ist hier nicht "
shared/test_entscheidungskerze.py:885:        print("    uebersprungen: ohne pandas_market_calendars kann der "
```
`XNYS`: 0 Treffer in diesen Dateitypen.

(i) Import-Anweisungen (`^\s*(import|from)\s+(pandas_market_calendars|exchange_calendars)`, `import_module(...)`, `__import__(...)` in allen `*.py`): genau 1 Treffer: `notifications/boersenkalender.py:81:    import pandas_market_calendars as mcal`. → ja. (Die übrigen Treffer oben sind Zeichenketten, Kommentare, Docstrings, Anforderungsdateien.)
(ii) `notifications/boersenkalender.py:70:KALENDER_NAME = "NYSE"` → ja. Zeichenkette `"NYSE"` in `*.py` insgesamt 2 Stellen: `notifications/boersenkalender.py:70` und `dashboard/test_dashboard.py:3998` (`offen.get("kalender") == "NYSE"`); `"XNYS"` 0.
(iii) Aufrufe (`mcal\.|get_calendar\(|\.valid_days\(|\.schedule\(` in allen `*.py`): `notifications/boersenkalender.py:109:        _KALENDER = mcal.get_calendar(KALENDER_NAME)`; `notifications/boersenkalender.py:125:        _FAHRPLAENE[schluessel] = _kalender().schedule(start_date=von, end_date=bis)`; `shared/snapshot.py:131` (Docstring-Text, kein Aufruf). `get_calendar(` als Aufruf: genau 1, in `boersenkalender.py:109` → ja.
(iv) `research/vorregistrierung/` (`pandas_market_calendars|exchange_calendars|get_calendar|mcal\.|KALENDER_NAME|boersenkalender|XNYS|NYSE`, ohne Gross/Klein): 0 Treffer → ja. (`kalender` ohne Gross/Klein in `research/vorregistrierung/*.py`: nur Wörter „Kalenderjahr(e)“, „Kalendertagen“.)
Wer importiert `boersenkalender` (`*.py`): `dashboard/pruefe_warteauftraege_kopie.py:48`, `dashboard/schliessen.py:130`, `dashboard/test_dashboard.py:62`, `dashboard/warteauftraege_ausfuehren.py:84`, `shared/entscheidungskerze.py:384`.
Lock: `requirements.lock:51:pandas-market-calendars==4.6.1` (Schreibweise mit Bindestrich; das vorgegebene Muster mit Unterstrich trifft den Lock nicht). Ferner `requirements.lock:37:exchange-calendars==4.5.6`; `docs/belege/TB-58/teil_a/requirements.lock.kandidat:47:pandas-market-calendars==4.6.1`; `requirements.txt:65:pandas_market_calendars>=4.1,<5`.

### 7, 8 (53.1 R66 (b))
K53 Z. 9 (R66-Block, 3860 Zeichen). (b) reicht von Byte 630 bis 1315.
„… Eine Abweichung ist ein Befund über Daten oder Umgebung, kein Ausgang (Bauart R33). Der Zellen-Erzeuger prüft das im Lauf je Bot und endet sonst mit 2. Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf trägt sie selbst. [Voraussetzung, zu messen: welchen Kalender des Pakets der Code des Laufs benutzt (TB-47, Feld kalender); die Messung zur Anfrage 02.10.c ver…“
Gegenprobe REG `grep -c -F`: „welchen Kalender des Pakets der Code des Laufs benutzt“ = 2 (Z. 11384, 11444); „kein Ausgang (Bauart R33)“ = 3 (Z. 11315, 11384, 11391); „endet sonst mit 2“ = 3 (Z. 11315, 11384, 11391).

### 9 (53.1 R66 (a), (b) — Anfang)
(a): „(a) Die Tagesreihe einer Zelle führt jeden Handelstag des Kapitalpfads, vom 1. Januar der ersten Selektionsfalte des Bots (29.3) bis zum Ende der Bestätigungsperiode (35.1), ohne Lücke. Handelstage sind bei Krypto die Kalendertage (15.4, Anmerkung 1), bei Aktien die Tage des Handelskalenders nach 17.5 (Umgebung, im Lock). Ein Tag, an dem die Zelle keine Position hält, steht mit Rendite 0 und Exposure 0 in der Reihe (1a), auch ein Tag vor dem ersten Handelbar-Tag des Bots.“
(b): „(b) Kalender und Kurse stimmen überein: Im Zeitraum nach (a) trägt an jedem Handelstag mindestens ein Symbol der Universumsdatei des Bots (3a) im Snapshot einen Kurs, und kein Symbol der Universumsdatei trägt einen Kurs an einem Tag, der kein Handelstag ist. Eine Abweichung ist ein Befund über Daten oder Umgebung, kein Ausgang (Bauart R33). …“

### 10 (53.9, Zeile R66 (53.1) (b))
K53 Z. 69 (2027 Zeichen), Anfang: „| R66 (53.1) (b) | welchen Kalender des Pakets der Code des Laufs benutzt (TB-47, Feld `kalender`) | Das Paket `pandas_market_calendars` importiert im Repo nur `notifications/boersenkalender.py` (Z. 81); dort stehen `KALENDER_NAME = "NYSE"` (Z. 70) und der einzige Aufruf `mcal.get_calendar(KALENDER_NAME)` (Z. 109). Die Datei steht nicht auf der Sperrlis…“
Schluss der Zeile: „… | nicht entscheidbar: Der Code des Laufs benutzt heute keinen Kalender; welchen Namen der Zellen-Erzeuger nimmt, ist offen (53.10 Nr. 1). Die Wache nach R66 (b) prüft die Wahl im Lauf |“
Weiter in derselben Zeile: „Im Fenster 2000-01-01 bis 2026-09-30 führt „XNYS“ gegenüber „NYSE“ einen Handelstag mehr (2025-01-09). Beide Kalendervergleiche sind Ersatzmessungen ausserhalb der Lock-Umgebung: Python 3.10 und pandas 2.3.3 des Systems, die Kalenderpakete in den Fassungen des Locks aus `trading-env`“.
Zählung in der Zeile: `NYSE` 3, `XNYS` 1, `boersenkalender` 2.

### 11 (53.9, Zeile R72 (53.7), zweite)
K53 Z. 76, Anfang: „| R72 (53.7), zweite | dass kein vorhandener Kern, den der Zellen-Erzeuger für die MtM-Reihe übernimmt, am Lückentag anders bewertet als (c) | Einziger vorhandener Kern für eine tägliche MtM-Reih…“
Stelle: „… | trifft für diesen Kern. Nicht von selbst erfüllt: `tagesraster` (Z. 135–148) lässt einen Tag aus, an dem kein übergebenes Symbol einen Kurs hat (das Raster nach R66 (a) gibt der Erzeuger); `gebunden` steht zum Einstand. Welchen Kern der Zellen-Erzeuger übernimmt, legt kein Registertext fest |“
REG `grep -c -F 'Nicht von selbst erfüllt'` = 1 (Z. 11451).

### 12 (R59 (b), R28)
R59 = 51.4, K51 Z. 30, in (b): „Jeder solche Eintrag ist die Kopie einer Konstante des Bot-Codes und trägt eine Probe gegen diese Konstante, mit Gegenprobe (40.7).“ REG `grep -c -F` dieses Satzes ohne „(40.7).“ = 1 (Z. 11222).
Die Wortfolge „Kopie mit Probe“: in R59 (b) (K51 Z. 30) 0; in der Quelle des Grundes von R59 (K51 Z. 31) 1: „Quelle des Grundes: R53, 32.5 (a) und (c), 26.6, R28 (Kopie mit Probe als benannter Zwischenstand), 37.5 (ein Wert, ein Ort), 40.7, 50.4. Kein Ergebnis.“ REG gesamt: 1 (Z. 11223).
R28 = 47.11, K47 Z. 82 (866 Zeichen): „Kopie mit Probe“ 0, „Gegenprobe“ 0, „Probe“ 3, „Kopie“ 2. Tatsächlicher Wortlaut: „… Das ist der Zustand aus 32.5 (c) — Literal mit Probe gegen den Registertext — und als benannter Zwischenstand zulässig, wenn jede Kopie ihre Probe hat; für `auswertung.py` ist es J-r (TB-117) [Voraussetzung, zu messen: ob `snapshot.py` eine Probe gegen Register 18 hat; wenn nein, Handwerk ohne Sperrlistennähe]. … `snapshot.py` bleibt ausserhalb des Laufbereichs und behält seine gebundene Kopie; ein Import zöge es hinein.“

### 13 (R72 (d), 27.2)
R72 (d), 53.7, K53 Z. 51 (ab Byte 1200): „(d) Nach dem letzten Kurs eines Symbols führte derselbe Code das Symbol an jedem Folgetag mit Rendite 0 im Mittel weiter. Das wäre mit 3b (c) nicht vereinbar: … Am Bestand vom 02.10.2026 endet keine Reihe früher. Vor dem signierten Tag wird am Snapshot gemessen (Verfahrensmessung nach 27.2), dass keine Kursreihe eines Symbols der zwei Universumsdateien vor dem letzten Kurstag ihres Marktes endet, und wie viele Symbol-Tage Lücke im Zeitraum nach R66 (a) liegen. Endet eine Reihe früher, wird gemeldet und vor …“
27.2, K27 Z. 22 (ganz, 247 Zeichen): „> **27.2** Zulässig sind Verfahrensmessungen — Kalender, Datenbestand, Faltenzahl, Handelbarkeit, Benchmark-Seite — und Wirkungen einer Regel auf die registrierten heutigen Parameter, wenn die Regel vor der Messung geschrieben stand (Bauart 24.3).“

### 14 (R46)
48.14, K48 Z. 112, Anfang: „> R46 — Registertext, Ersteintrag — Abnahme des Zellen-Erzeugers vor dem Tag. Vor dem signierten Tag läuft der Zellen-Erzeuger nicht auf dem registrierten Snapshot mit dem registrierten Raster. Abgenommen wird er im Selektionsmodus gegen einen Test-Snapshot aus synthetischen Kursdaten (mit snap…“
Schluss: „… nie eine Zahl des Selektionsraums. Der Hash des Test-Snapshots steht in der Tatsachennotiz der Abnahme. F-15.“
Fable-Wortfolge „der Erzeuger läuft vor dem Tag nicht auf dem registrierten Snapshot“: REG `grep -c -F` = 0 (auch „läuft vor dem Tag nicht auf dem registrierten Snapshot“ = 0). In der Fable-Antwort steht die Wortfolge in runden Klammern, nicht in Anführungszeichen.

### 15 (37.5 (2), R39, R45)
R39 (48.7), K48 Z. 58: „> Quelle des Grundes: 23.3, 16.7 (b), 37.5 (2) (ein Wert, ein Ort), 33.3, 41.1 A12, 5e. Kein Ergebnis.“
R45 (48.13), K48 Z. 106: „> Quelle des Grundes: 24.2/1a (die MtM-Reihe braucht die Positionen), 37.3, 10.1 („bitidentisch“), 41.1 A9, 37.5 (2) (ein Wert, ein Ort). Kein Ergebnis.“
37.5 (2) selbst, K37 Z. 273 = REG Z. 7161: „> **(2)** Der Laufpfad (Optimierer, Equity-Simulation, Erzeuger) liest registrierte Werte ausschliesslich aus diesem Modul — kein Laufmodul trägt eine eigene Kopie. Für den Papierpfad (`forward_test.py`) gilt das nicht als Sperre, aber als Konsistenzprüfung: Die Sonde meldet als Befund, wenn eine Kopie dort vom registrierten Wert abweicht.“
Wortfolge „ein Wert, ein Ort“: in 37.5 (2) (K37 Z. 273) 0; in 37.5 gesamt (K37 Z. 267–349) 1, in Z. 298: „> *Quelle des Grundes:* Zweck der Sperrliste (Übergabe Abschnitt 5) und A8; der Grundsatz ein Wert, ein Ort aus 21j. …“

### 16 (XNYS, ein Handelstag mehr)
`docs/belege/TB-133/vormessung/v1_vormessung_04a.md` (938 Z., von git nicht verfolgt):
- Z. 94 / 125 / 140 (Auszug aus REG Z. 11444): „Im Fenster 2000-01-01 bis 2026-09-30 führt „XNYS“ gegenüber „NYSE“ einen Handelstag mehr (2025-01-09).“
- Z. 328 (Auszug aus `docs/belege/TB-132/vormessung/v5_code_02c.md`, Z. 88): „`"XNYS"` führt gegenüber `"NYSE"` **einen Tag mehr: 2025-01-09** (in beiden Fenstern, 2010… und 2000…); kein Tag nur in `"NYSE"`. Das Paket kennt 193 Kalendernamen. …“
- Z. 322: „| `"XNYS"` | `pandas_market_calendars.class_registry.XNYS` (Spiegel von `exchange_calendars`) | 6 727 |“
- Z. 334: „2. **Kalendervergleich `"NYSE"` gegen `"XNYS"`** (1.5): Ersatzmessung mit dem Paket aus `trading-env/` unter fremdem Interpreter; nicht gegen die Kursdaten gehalten (das tat v3 nur für `"NYSE"`), und nur …“
- Z. 243: „Suchwort `XNYS`: 0 Trefferzeilen in 0 Dateien“; Z. 292: „„XNYS“ kommt in keiner `*.py` des Repos vor.“
`docs/projektfuehrung/FABLE_ANFRAGE_2026-10-04a_kalendername_deckelfall_zaehlung.md` (59 Z., von git nicht verfolgt):
- Z. 15: „Das Feld `kalender` aus TB-47 führt Importstellen und Paketfassung, keinen Namen. Im Fenster 2000-01-01 bis 2026-09-30 führt „XNYS“ gegenüber „NYSE“ einen Handelstag mehr (2025-01-09); gegen die Kurstage des Bestands vom 02.10.2026 weicht „NYSE“ an keinem Tag ab. Beide Vergleic…“
- Z. 17: „Als Kalendername steht „NYSE“ im Code an zwei Stellen (`boersenkalender.py:70`, `dashboard/test_dashboard.py:3998`), „XNYS“ an keiner.“
- Z. 21: „… (a), mit Marke an 17.5; 17.5 selbst bleibt zeichengleich. [Voraussetzung, vor dem Eintrag zu messen: der Vergleich „NYSE“ gegen „XNYS“ in der Lock-Umgebung.]“

### 17 (53.5 R70 (a) letzter Satz, (b))
K53 Z. 37 = REG Z. 11412. (a) hat 570 Zeichen; Schluss: „… Ein Ort, den ein Block nur als Geltungsbereich einer Regel nennt, deren „lies“ einem anderen Ort gilt, bleibt ohne Marke und wird vom Index geführt, wie R54 an 7 (c) (R61 (b)). Nennt der Wortlaut eines Ortes die Sache nicht und gibt der Block sie ihm, trägt der Ort die Marke: so 4.2 zu R64, 15.3 (a) zu R66 und 48.1 zu R68.“
(b) ganz (205 Zeichen): „(b) Indexzeilen ohne Marke: 7 (c) — mittlere Exposure des Gewinners, Tage nach R64 (a), (b) und (d). 17.5 — Handelskalender der Aktien-Tagesreihe, R66 (a) und (b). 50.7 Nr. 3 — Tagesbasis des DSR, R66 (f).“
Index dazu, IDX Z. 399: „- **17.5:** Handelskalender der Aktien-Tagesreihe → R66 (a) und (b) (53.1). Ohne Marke (R70 (b), 53.5).“

### 18 (R56 (b))
51.1, K51 Z. 9 (ab Byte 327): „(b) Bedingungen: Der Eröffnungstext liegt mit Commit im Repo, bevor die Antwort eingetragen wird. Das Leseprotokoll der ersten Antwort nennt, was der Chat vollständig gelesen hat, was nur als Ausschnitt, was nicht, … Die Antwortdatei liegt mit Commit im Repo; trägt sie Registertext, nennt der Kopf des Abschnitts Datei, md5 und Commit.“

### 19 (Zuordnung)
REG-Überschriften: Z. 11382 „### 53.1 R66 — …“; Z. 11389 „### 53.2 R67 — …“; Z. 11396 „### 53.3 R68 — …“; Z. 11403 „### 53.4 R69 — …“; Z. 11410 „### 53.5 R70 — …“; Z. 11417 „### 53.6 R71 — …“; Z. 11424 „### 53.7 R72 — …“; Z. 11431 „### 53.8 R73 — …“; Z. 11438 „### 53.9 Voraussetzungen und Befunde“; Z. 11456 „### 53.10 Was offen bleibt“.
IDX Z. 207: „| 53 aus 02c | 4 | R66–R73 (53.1–53.8); 53.9 Voraussetzungen und Befunde; 53.10 Offenes | – |“. IDX Z. 365: „Alle 21 Marken, die TB-132 gesetzt hat (alle am alten Ort: 20 nach R70 (c), eine an 23.3, Registertext 3b (c), vom …“.
Weitere Zuordnungen aus Überschriften: R28 = 47.11, R39 = 48.7, R45 = 48.13, R46 = 48.14, R56 = 51.1, R59 = 51.4.

### 20 (Antwort 02c)
`docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md` (157 Z.): „kein Ausgang (Bauart R33)“ `grep -c -F` = 2 (Z. 134, 137; 3 Vorkommen); „endet sonst mit 2“ `grep -c -F` = 2 (Z. 134, 137; 3 Vorkommen); „welchen Kalender des Pakets der Code des Laufs benutzt“ = 1 (Z. 134). Ausschnitt Z. 134: „… Eine Abweichung ist ein Befund über Daten oder Umgebung, kein Ausgang (Bauart R33). Der Zellen-Erzeuger prüft das im Lauf je Bot und endet sonst mit 2. Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf tr…“

## Nicht gemessen / Grenzen
- `docs/projektfuehrung/register_kopie/REGISTER_INDEX.md` gibt es nicht; der Index liegt unter `docs/projektfuehrung/REGISTER_INDEX.md` (420 Z., 40 183 Byte) und wurde dort gelesen.
- Ob Arbeitsbaum und HEAD für Register und Kopien übereinstimmen, nicht gemessen (kein `git status`/`git diff` erlaubt). Dateilesungen (grep/sed) messen den Arbeitsbaum; `git grep` die verfolgten Dateien im Arbeitsbaum.
- `docs/belege/TB-133/vormessung/v1_vormessung_04a.md`, `FABLE_ANFRAGE_2026-10-04a_…md` und `FABLE_ANTWORT_2026-10-04a_…md` sind von git nicht verfolgt (`git ls-files` = 0).
- Der Kalendervergleich „NYSE“ gegen „XNYS“ selbst wurde nicht nachgerechnet (kein Python des Repos, kein Lauf); gemessen sind nur die Textstellen, die ihn nennen.
- Abschrift der Fable-Antwort im Container nicht gegen die Datei im Repo (29 195 Byte) verglichen; nicht verlangt.

# ERGEBNIS TB-56 — Die Faltenschranke messen und entfernen (Mac-Lauf, 19.09.2026)

**Auftrag:** `logs/auftraege/TB-56.md` (versioniert als `docs/auftraege/TB-56.md`,
byteweise gleich). **Ausgeführt am MacBook**, Zweig `main`, Ausgang `d66a2ce`,
Ergebnis **`04b42b3`** (Teil A, die Messung samt Skript) und **`7387cc5`**
(Teil B, die Änderung samt neuem Plan), beide gepusht; dieses Dokument und die
letzten Belege folgen als dritter Commit. Interpreter durchgehend
`trading-env/bin/python3` = **Python 3.9.6**. Kein eigener Zweig, kein PR,
keine ZIP. Belege: `docs/belege/TB-56/` (mit `HERKUNFT.md`).

**Kurzfassung:** Die Schranke bindet bei **acht der neun** Bots, und ohne sie
liefert die Messung **nicht** dasselbe Jahr: **2017** (`elliott_wave_stocks`,
`turtle_soup_stocks`), **2018** (`elliott_wave`, `t3_supertrend`,
`turtle_soup_crypto`, `volatility_breakout_crypto`, `rsi2_mean_reversion`,
`volatility_breakout`), **2019** (`rsi2_crypto`, dort bindet die Datenlage).
**Die Zulassung nach 4b ändert sich für keinen Bot.** `elliott_wave` bekommt
**vier statt drei** Doppeljahr-Falten, und seine **Bestätigungsperiode
verschiebt sich** von 2025-01-01 auf 2026-01-01. Der Trockenlauf des Laufcodes
(Registertext 3b) zeigt zusätzlich: die Falte **2018 von `t3_supertrend` ist
nach 3b (a) leer** (0 Symbole vom Loader handelbar, `MIN_HISTORY_DAYS = 730`),
seine erste Falte „aus dem Trockenlauf" ist damit 2019, nicht 2018. Die
Konstante `ERSTE_MOEGLICHE_FALTE` ist aus dem Code entfernt; der neue Plan liegt
als **eigene Datei** neben dem alten, der byteweise unverändert ist. **Drei
Rückfragen** waren nötig (Regel 6) — die Schranke, die den registrierten Plan
tatsächlich erzeugt hat, liegt in einer **Kopie** ausserhalb der Freigabe, und
an ihr hängen Prüfer, die den Code gegen das Register halten. Ergebnis der
Antworten: `faltenplan_neun.py` bleibt **bis TB-56b unverändert**, und
`test_vorregistrierung.py` ist **bis TB-56b rot** (die gesperrte
Benchmark-Tabelle kennt die Falten 2017/2018 nicht) — benannt, nicht versteckt.

---

## Die acht Fragen des Auftrags, beantwortet

| Frage | Antwort |
|---|---|
| ⭐⭐ **Je Bot: erste Falte und Faltenzahl mit und ohne Schranke — als Tabelle?** | Ja, unten (Teil A). Erste Falte mit Schranke überall 2019; ohne: 2017 / 2018 / 2019 je nach Bot. Selektionsfalten mit → ohne: `elliott_wave` 3 → 4, `rsi2_crypto` 7 → 7, die beiden 2017er-Bots 7 → 9, die fünf 2018er-Bots 7 → 8 |
| ⚠️ **Ändert sich für irgendeinen Bot die Zulassung nach 4b?** | **Nein.** Alle neun haben mit und ohne Schranke mindestens 3 Selektionsfalten (kleinster Wert: `elliott_wave` 3 mit, 4 ohne). Auch nach dem Trockenlauf des Laufcodes (Lesart H, leere Falten abgezogen) bleibt jeder Bot über 3. **Keine stille Änderung; nichts zu benennen** |
| ⭐ **Was ergibt `elliott_wave` genau?** | Nach 4a (Kursdaten am 1. Januar, Vorlauf 0 Balken): erste Falte **2018** — der Plan wird **2018–2019, 2020–2021, 2022–2023, 2024–2025**, Bestätigung ab **2026-01-01** (vorher 2025-01-01). Die Doppeljahr-Parität kippt: 4 statt 3 Selektionsfalten, die Bestätigungsperiode schrumpft von 20 auf 8 Monate. Sein Loader zählt **Kerzen**: `MIN_HISTORY_HOURS = 17 520` erreicht **BTC/ETH am 2019-08-20** (17 520. Stundenkerze; bei lückenloser Reihe wäre es 2019-08-17 — **3 Tage Verzug durch 147 fehlende Kerzen**), BNB am 2019-11-09. Die Falte 2018–2019 hat deshalb nach 3b (a) **3 Symbole** (H), nach Lesart A ebenfalls 3. **Sechs** Symbole erreichen die Schranke bis heute nicht (`BMTUSDT`, `ENSOUSDT`, `PUMPUSDT`, `TRUMPUSDT`, `UUSDT`, `ZKCUSDT`). Tabelle je Symbol unten |
| ⚠️ **Liefert die Messung für die acht Bots dasselbe Jahr — oder nicht?** | **Nicht.** Drei verschiedene Jahre über die neun: 2017 (2 Bots), 2018 (6), 2019 (1). Fables Warnung trifft zu: `rsi2_mean_reversion` (200 Tage Vorlauf) und `volatility_breakout` (127) kommen ab dem Zehnjahresfenster 2016-09-01 nicht bis zum 1.1.2017 — erst 2018; die beiden Aktien-Bots ohne bzw. mit 30 Balken Vorlauf schaffen 2017 |
| **Kommt `ERSTE_MOEGLICHE_FALTE` irgendwo im Quelltext noch vor?** | **Als Bezeichner im Code: 0 Treffer** (am Syntaxbaum über `research/`, `shared/`, `strategies/`). Als Text: `faltenplan_neun.py:61` (Docstring) und `:119` (Kommentar `# registerdaten.py::ERSTE_MOEGLICHE_FALTE` — verweist jetzt auf eine Konstante, die es nicht mehr gibt; Datei nach Rückfrage 3 bis TB-56b unverändert), `faltenplan_neun/BERICHT.md:104`, sowie die beiden Erläuterungen in `faltenplan.py:20` und `faltenschranke_messung.py:15`, die die Entfernung beschreiben |
| **Beisst die Mutationsgegenprobe?** | **Ja, zweifach.** (a) Schranke 2019 im Speicher wieder eingesetzt: **8 von 9** Plänen ändern sich. (b) Wegwerf-Kopie von `research/vorregistrierung/` mit **einer** geänderten Zeile (`erste = max(2019, erste_falte(bot))`), eigener Prozess: **4 von 4** Aktienplänen beginnen dann 2019 statt 2017/2018 |
| **Ist `faltenplan.json` byteweise unverändert?** | **Ja.** SHA-256 `93fbf09c…7839` vorher, nachher und unter `d66a2ce`; `git status` für die Datei leer. Der neue Plan heisst **`research/faltenplan_neun/daten/faltenplan_ohne_schranke.json`** |
| **Beobachtungen, die NICHT ausgeführt wurden?** | elf, unten |

---

## Schritt −1 — Ortsprüfung (18:05 UTC)

| Prüfung | Soll | Ist |
|---|---|---|
| `uname -s` | `Darwin` | **`Darwin`** ✅ |
| `trading-env/bin/python3` | 3.9.x | **3.9.6** ✅ |
| Arbeitsordner, Zweig | `~/trading-bot`, `main`, aktuell | `/Users/jaquelineloffler/trading-bot`, `main`, nach `git fetch` `HEAD` = `origin/main` = `d66a2ce` ✅ |
| `git status --short` | 0 Zeilen | **0** ✅ |
| Snapshot | `snapshots/63e4b6c8…cb2ceb2/MANIFEST.json` vorhanden | vorhanden ✅ |

Vorher gelesen: `docs/UEBERGABEPROTOKOLL.md` (7, 8, 10), `docs/UMGEBUNGEN.md`,
`docs/PRUEFPRINZIPIEN.md` (A1, A2, A7, B1, B5, D5), das Register (5.1–5.4,
15.6, 16.1, 16.2, 16.7, Sperrliste 10), `registerdaten.py`, `faltenplan.py`,
`faltenplan_neun.py`, `test_faltenplan_neun.py` (Teile A, B, F, G),
`universum_trockenlauf.py`, `loaderlauf.py` (Kopf), `pruefe_register.py`
(Beleg-Modus), `benchmark.py`, `docs/ERGEBNIS_TB-58b_registereintraege.md`
als Vorlage.

## Schritt 0 — Sichern und messen

**Sicherungsordner:** `~/Sicherungen/tb56_faltenschranke_20260919T180604Z/`
(`kopien/` mit den zwölf Datenbanken).

| | Soll | Ist |
|---|---|---|
| `*.db` ausserhalb `trading-env/` | Quersummen + Kopie, gezählt | **12** (11 in der Wurzel, dazu `strategies/volatility_breakout/paper_trading_volatility_breakout.db`); Kopien gegen `shasum -a 256 -c`: **12/12 OK** ✅ |
| Datenstand vorher (`--nur-hash`, 18:06 UTC) | `d9449faf…`, 223 | **`d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, 223** ✅ |
| Snapshot `--pruefen` | `UNVERAENDERT` | **`UNVERAENDERT`**, rc 0 ✅ |
| Registerprüfer VORHER (`--basis a1e7fb4`, 18:06 UTC, vor jeder Änderung — A7) | KEIN BEFUND | **KEIN BEFUND**, rc 0, Quelle Beleg: `trockenlauf`, numstat `728 0` ✅ |
| Sperrklinken vorher | Wanduhr ≤ 6, Pfadbau ≤ 29 | **6 / 29**, beide GRUEN ✅ |
| Basislauf vorher (18:08–18:40 UTC) | Zahlen je Stufe | **61 grün / 5 rot (alle bekannt) / 1 flackernd (`test_log_rotation`, heute grün) / 3 ungeprüft / 1 Zeitgrenze (`test_drawdown_beide_masse`, bekannt) = 71, UNERWARTET 0** — `test_faltenplan_neun.py` 124,8 s OK, `test_vorregistrierung.py` 31,0 s OK ✅ |

---

## ⭐⭐ Teil A — Die Messung, rein lesend, vor jeder Änderung (18:11–18:15 UTC)

**Werkzeug:** `research/faltenplan_neun/faltenschranke_messung.py` (neu, reine
Standardbibliothek). Es schaltet die Schranke **im Speicher** aus
(`faltenplan_neun.FRUEHESTE_FALTE = 0` als Modulattribut, hinterher
zurückgesetzt) — die Datei auf der Platte bleibt, wie sie ist. Zuerst prüft es,
dass das Werkzeug **mit** Schranke heute denselben Plan liefert wie die
festgehaltene Messung `daten/faltenplan.json` (je Bot: erste Falte, Länge,
Faltenzahl, Faltennamen, Bestätigung, Symbolzahlen A und B): **9/9 gleich.**
Ohne diese Kontrolle hätte die Messung ein anderes Werkzeug gemessen als das,
das die Tatsachennotiz erzeugt hat.

**Warum `faltenplan_neun.py` und nicht `research/vorregistrierung/faltenplan.py`:**
Die Tabelle in 15.6 und `daten/faltenplan.json` stammen aus `faltenplan_neun.py`
(Verfahren B, alle neun Bots, Indikator-Vorlauf je Bot). Das
Vorregistrierungs-Werkzeug rechnet Verfahren A, führt Krypto als Platzhalter
ohne Falten und kennt keinen Vorlauf — an ihm liesse sich 4a für Krypto gar
nicht messen. Der Auftrag vermutete die Messung dort (Kopfzeile: „importiert
`pandas`"); gemessen wurde am Werkzeug der Registertabelle. Beides wurde
trotzdem gerechnet; die Vorregistrierung liefert für die vier Aktien-Bots
dieselben ersten Falten.

### Die Tabelle je Bot — mit und ohne Schranke

Lesart A wie in 15.6 (Kursdaten am 1. Januar, Indikator-Vorlauf läuft in die
Falte hinein). „H" = Trockenlauf des Laufcodes, Registertext 3b (a): Falten,
in denen der Loader mindestens ein Symbol handelbar macht.

| Bot | Markt | Länge | 1. Falte **mit** | 1. Falte **ohne** | # Sel. **mit** | # Sel. **ohne** | Bestätigung mit → ohne | 4b mit | 4b ohne | 1. Falte nach H | # Sel. nach H |
|---|---|---:|---:|---:|---:|---:|---|---|---|---:|---:|
| `elliott_wave` | krypto | 2 J | 2019 | **2018** | 3 | **4** | 2025-01-01 → **2026-01-01** | ja | ja | 2018–2019 | 4 |
| `t3_supertrend` | krypto | 1 J | 2019 | **2018** | 7 | **8** | 2026-01-01 → 2026-01-01 | ja | ja | ⚠️ **2019** | **7** |
| `rsi2_crypto` | krypto | 1 J | 2019 | 2019 | 7 | 7 | 2026-01-01 → 2026-01-01 | ja | ja | 2019 | 7 |
| `turtle_soup_crypto` | krypto | 1 J | 2019 | **2018** | 7 | **8** | 2026-01-01 → 2026-01-01 | ja | ja | 2018 | 8 |
| `volatility_breakout_crypto` | krypto | 1 J | 2019 | **2018** | 7 | **8** | 2026-01-01 → 2026-01-01 | ja | ja | 2018 | 8 |
| `elliott_wave_stocks` | aktien | 1 J | 2019 | **2017** | 7 | **9** | 2026-01-01 → 2026-01-01 | ja | ja | 2017 | 9 |
| `rsi2_mean_reversion` | aktien | 1 J | 2019 | **2018** | 7 | **8** | 2026-01-01 → 2026-01-01 | ja | ja | 2018 | 8 |
| `turtle_soup_stocks` | aktien | 1 J | 2019 | **2017** | 7 | **9** | 2026-01-01 → 2026-01-01 | ja | ja | 2017 | 9 |
| `volatility_breakout` | aktien | 1 J | 2019 | **2018** | 7 | **8** | 2026-01-01 → 2026-01-01 | ja | ja | 2018 | 8 |

**Schranke bindet bei 8 Bots**, Faltenzahl ändert sich bei 8, Bestätigungsperiode
bei **einem** (`elliott_wave`), Zulassung nach 4b bei **keinem**.

### Die Falten und Symbolzahlen ohne Schranke

Symbolzahl je Selektionsfalte → Bestätigung; Lesart A aus dem Faltenplan, H aus
dem Trockenlauf des Laufcodes (Bestätigung als letzter Wert).

| Bot | Selektionsfalten → Bestätigung | Lesart A | Trockenlauf H |
|---|---|---|---|
| `elliott_wave` | 2018–2019, 2020–2021, 2022–2023, 2024–2025 → 2026 | 3 / 9 / 13 / 17 → 23 | 3 / 9 / 13 / 17 → 18 |
| `t3_supertrend` | 2018, 2019, …, 2025 → 2026 | 3 / 6 / 9 / 13 / 13 / 13 / 17 / 18 → 23 | ⚠️ **0** / 3 / 6 / 9 / 13 / 13 / 13 / 17 → 18 |
| `rsi2_crypto` | 2019, …, 2025 → 2026 | 6 / 9 / 13 / 13 / 13 / 17 / 18 → 23 | 6 / 9 / 10 / 13 / 13 / 17 / 18 → 20 |
| `turtle_soup_crypto` | 2018, …, 2025 → 2026 | 3 / 6 / 9 / 13 / 13 / 13 / 17 / 18 → 23 | **2** / 6 / 9 / 10 / 13 / 13 / 17 / 18 → 20 |
| `volatility_breakout_crypto` | 2018, …, 2025 → 2026 | 3 / 6 / 9 / 13 / 13 / 13 / 17 / 18 → 23 | **2** / 6 / 9 / 10 / 13 / 13 / 17 / 18 → 20 |
| `elliott_wave_stocks` | 2017, …, 2025 → 2026 | 139 / 139 / 140 / 142 / 145 / 147 / 148 / 148 / 149 → 150 | 135 / 136 / 137 / 137 / 139 / 139 / 140 / 142 / 145 → 147 |
| `rsi2_mean_reversion` | 2018, …, 2025 → 2026 | 139 / 140 / 142 / 145 / 147 / 148 / 148 / 149 → 150 | 136 / 137 / 137 / 139 / 139 / 140 / 142 / 145 → 147 |
| `turtle_soup_stocks` | 2017, …, 2025 → 2026 | 139 / 139 / 140 / 142 / 145 / 147 / 148 / 148 / 149 → 150 | 135 / 136 / 137 / 137 / 139 / 139 / 140 / 142 / 145 → 147 |
| `volatility_breakout` | 2018, …, 2025 → 2026 | 139 / 140 / 142 / 145 / 147 / 148 / 148 / 149 → 150 | 136 / 137 / 137 / 139 / 139 / 140 / 142 / 145 → 147 |

Die H-Reihen ab 2019 sind **zeichengleich mit der Tatsachennotiz 16.1.1** —
der Trockenlauf misst auf dem Plan ohne Schranke dasselbe wie damals, nur mit
den zusätzlichen frühen Falten davor. Monotonie nicht verletzt, keine
Schreibversuche. Laufzeit des Trockenlaufs 1 min 39 s.

**Zwei Dinge, die diese Tabellen sagen und die in den Bericht gehören:**

1. ⚠️ **`t3_supertrend` 2018 ist nach 3b (a) keine Selektionsfalte.** Nach 4a
   (Lesart A: Kursdaten liegen vor, Vorlauf 1 Balken) beginnt sein Plan 2018.
   Sein Loader verlangt aber `MIN_HISTORY_DAYS = 730` Zeitspanne; BTC/ETH
   (Daten ab 2017-08-17) erreichen das erst am **2019-08-17**. In der Falte 2018
   macht der Loader **kein** Symbol handelbar — die Falte zählt nach 3b (a)
   nicht. „Die erste Falte aus dem Trockenlauf nach 4d" ist für diesen Bot
   also **2019**, nicht 2018. Das ist genau der Unterschied zwischen 4a
   (Universum + Indikator-Vorlauf) und 3b (b) (`MIN_HISTORY_*` des Loaders),
   und er ist eine Sachfrage für TB-56b, keine für den Code.
2. **Die 500-Tage-Bots haben 2018 zwei Symbole an zwei Tagen.** BTC/ETH werden
   für `turtle_soup_crypto` und `volatility_breakout_crypto` am **2018-12-30**
   handelbar (2017-08-17 + 500 Tage). Die Falte 2018 zählt nach 3b (a) — „an
   mindestens einem Handelstag" —, ist aber die dünnste Falte des ganzen Plans:
   zwei Symbole, zwei Tage. Das steht hier, damit TB-56b es weiss, nicht damit
   der Code es verhindert (Fable: eine Mindest-Symbolzahl wäre die Schranke
   „durch die Hintertür").

### `elliott_wave` ausdrücklich — Kerzen, nicht Tage

`MIN_HISTORY_HOURS = 17 520` (`strategies/elliott_wave/multi_symbol_optimise.py:50`,
gelesen, nicht angenommen). Je 1h-Symbol: Kerzen gezählt, Datum der 17 520.
Kerze, dasselbe Datum bei lückenloser Reihe (erster Tag + 730 Tage), Verzug.
„fehlend" = Spanne × 24 minus gezählte Kerzen (einschliesslich des
angeschnittenen ersten Tags — eine Obergrenze, keine Lückenzahl).

| Symbol | erster Tag | Kerzen | fehlend | 17 520. Kerze am | lückenlos ab | Verzug (Tage) |
|---|---|---:|---:|---|---|---:|
| `BTCUSDT` | 2017-08-17 | 79 461 | 147 | **2019-08-20** | 2019-08-17 | **3** |
| `ETHUSDT` | 2017-08-17 | 79 461 | 147 | **2019-08-20** | 2019-08-17 | **3** |
| `BNBUSDT` | 2017-11-06 | 77 524 | 140 | 2019-11-09 | 2019-11-06 | 3 |
| `ADAUSDT` | 2018-04-17 | 73 669 | 107 | 2020-04-18 | 2020-04-16 | 2 |
| `XRPUSDT` | 2018-05-04 | 73 257 | 111 | 2020-05-06 | 2020-05-03 | 3 |
| `TRXUSDT` | 2018-06-11 | 72 342 | 114 | 2020-06-13 | 2020-06-10 | 3 |
| `LINKUSDT` | 2019-01-16 | 67 115 | 85 | 2021-01-17 | 2021-01-15 | 2 |
| `ZECUSDT` | 2019-03-21 | 65 591 | 73 | 2021-03-21 | 2021-03-20 | 1 |
| `DOGEUSDT` | 2019-07-05 | 63 049 | 71 | 2021-07-06 | 2021-07-04 | 2 |
| `SOLUSDT` | 2020-08-11 | 53 407 | 41 | 2022-08-12 | 2022-08-11 | 1 |
| `UNIUSDT` | 2020-09-17 | 52 522 | 38 | 2022-09-17 | 2022-09-17 | 0 |
| `NEARUSDT` | 2020-10-14 | 51 872 | 40 | 2022-10-14 | 2022-10-14 | 0 |
| `AAVEUSDT` | 2020-10-15 | 51 850 | 38 | 2022-10-15 | 2022-10-15 | 0 |
| `PROMUSDT` | 2023-03-17 | 30 672 | 24 | 2025-03-16 | 2025-03-16 | 0 |
| `SUIUSDT` | 2023-05-03 | 29 541 | 27 | 2025-05-02 | 2025-05-02 | 0 |
| `PEPEUSDT` | 2023-05-05 | 29 487 | 33 | 2025-05-04 | 2025-05-04 | 0 |
| `WLDUSDT` | 2023-07-24 | 27 576 | 24 | 2025-07-23 | 2025-07-23 | 0 |
| `ENAUSDT` | 2024-04-02 | 21 505 | 23 | 2026-04-02 | 2026-04-02 | 0 |
| `TRUMPUSDT` | 2025-01-19 | 14 497 | 23 | — | 2027-01-19 | — |
| `BMTUSDT` | 2025-03-18 | 13 098 | 30 | — | 2027-03-18 | — |
| `PUMPUSDT` | 2025-09-11 | 8 853 | 27 | — | 2027-09-11 | — |
| `ZKCUSDT` | 2025-09-15 | 8 755 | 29 | — | 2027-09-15 | — |
| `ENSOUSDT` | 2025-10-14 | 8 064 | 24 | — | 2027-10-14 | — |
| `UUSDT` | 2026-01-13 | 5 881 | 23 | — | 2028-01-13 | — |

**Ergebnis:** Der Kerzenzähler reagiert auf Lücken — bei den 2017/2018er-Symbolen
kostet das **2–3 Tage**, bei den jüngeren nichts. Für die erste Falte ändert
das nichts: nach 4a (Vorlauf 0) beginnt `elliott_wave` 2018, und die Falte
2018–2019 hat nach H drei Symbole (BTC, ETH ab 2019-08-20, BNB ab 2019-11-09).
**Sechs Symbole** liegen heute unter der Schranke und tragen nirgends
Evidenz bei — dieselben sechs, die 16.1.2 als „ohne Faltenevidenz" führt.

### Nachrechnung der Loader-Lesart je Bot (3b (b)), nachrichtlich

Erster Kurstag + `MIN_HISTORY_DAYS` (bzw. Datum der N-ten Kerze) je Symbol,
Minimum über das Universum: `elliott_wave` 2019-08-20 → 2019, `t3_supertrend`
2019-08-17 → 2019, die drei 500-Tage-Bots 2018-12-30 → 2018. Für die
Aktien-Bots ergibt die Nachrechnung „1967" (Dateibeginn + 1 825 Tage) — eine
Zahl ohne Aussage, weil der Loader das Zehnjahresfenster auf die
durchgereichten Daten legt; **massgeblich ist der Trockenlauf**, und der sagt
2017/2018 (Tabelle oben). Die Nachrechnung steht im Skript als Gegenprobe,
nicht als Messung.

---

## Die drei Rückfragen — wörtlich in `docs/belege/TB-56/rueckfrage.md`

Regel 6 des Auftrags: „Fallen Wortlaut und Zweck auseinander und der Betreiber
ist erreichbar: fragen, nicht entscheiden." Dreimal war das der Fall; Fragen
und Antworten stehen wörtlich im Beleg, hier die Kurzform.

**Rückfrage 1 (nach Teil A):** Die Schranke, die den registrierten Plan erzeugt
hat, ist nicht `ERSTE_MOEGLICHE_FALTE` in `registerdaten.py`, sondern deren
**Kopie** `FRUEHESTE_FALTE = 2019` in `research/faltenplan_neun/faltenplan_neun.py:120`
(die Datei importiert `registerdaten.py` nicht). Nur die zwei freigegebenen
Dateien zu ändern, liesse das Werkzeug der Registertabelle mit Schranke
weiterrechnen. → **Antwort: „Ja, beide zusätzlich freigeben"** (`faltenplan_neun.py`
und `test_faltenplan_neun.py`). Zweite Frage, woher `plan_aktien()` die erste
Falte nimmt → **„Aus der Datenlage, Regel von faltenplan_neun"** (Pfad-Import,
eine Regel an einer Stelle).

**Rückfrage 2 (vor Teil B):** An `faltenplan_neun.py` hängen Prüfer, die den
Code **gegen das Register** halten — und das Register trägt die 2019 noch, bis
TB-56b es berichtigt: der Registerprüfer holt seinen Plan live über den
Trockenlauf und vergleicht mit 16.1.1; ohne Schranke stolpert die Druckfunktion
des Trockenlaufs über Falten, die im Register nicht stehen (gemessen:
`TypeError` in `drucke`, kein JSON), und der Prüfer fiele **still** auf den
Dokument-Beleg zurück — „KEIN BEFUND" ohne Messung (A1). `test_faltenplan_neun.py`
vergleicht gegen das TB-31-Werkzeug (eine **dritte** Kopie `FRUEHESTE_FALTE = 2019`
in `research/krypto_historie/faltenplan.py`, nicht freigegeben) und gegen die
Registertabelle — würde rot. → **Antwort: „Bis TB-56b unverändert lassen"**:
Code und Register wechseln im selben Zug; der neue Plan entsteht jetzt aus dem
Messskript, inhaltsgleich mit dem, was `faltenplan_neun.py` ohne Schranke
rechnet. Die Freigabe aus Rückfrage 1 wurde damit **nicht in Anspruch
genommen**.

**Rückfrage 3 (nach Teil B, vor Commit 2):** Nach der Angleichung von
`faltenplan.py` an 4a bricht `test_vorregistrierung.py` ab
(`auswertung.py:237 KeyError: '2017'`): die Verfahren-A-Auswertung liest die
**vorab berechneten Benchmark-Drawdowns** (`ergebnisse/benchmark_drawdowns.json`),
und die kennen nur Falten ab 2019. Die Datei steht auf der **Sperrliste**
(Register 10, Punkt 4) und ist nicht freigegeben. Probeweise neu gerechnet (in
den Scratchpad): alle registrierten Faltenzeilen 2019–2026 zeichengleich,
2017/2018 kommen hinzu — aber der gesperrte Wert **`DD_Toleranz`** (Median über
die Selektionsfalten) ändert sich bei `rsi2_mean_reversion` und
`volatility_breakout` von −4,33 % / −8,55 % auf **−6,61 % / −12,89 %** (@ 50 % /
100 %; acht statt sieben Falten, gerader Median); bei den zwei anderen
Aktien-Bots bleibt er zufällig gleich (neun Falten, 2017 tief, 2018 hoch).
→ **Antwort: „Tabelle daneben, Test rot bis TB-56b"**: die neue Tabelle als
eigene Datei `ergebnisse/benchmark_drawdowns_ohne_schranke.json`, die gesperrte
byteweise unverändert, `test_vorregistrierung.py` bis zur Amendment-Entscheidung
in TB-56b rot — benannt.

---

## Teil B — Entfernen (Commit `7387cc5`, 18:58 UTC)

| # | Auftrag | Getan |
|---|---|---|
| 1 | `ERSTE_MOEGLICHE_FALTE` aus `registerdaten.py` (Zeile 103) entfernen | **Entfernt.** An ihrer Stelle ein fünfzeiliger Kommentar, der sagt, wo die erste Falte jetzt herkommt und warum die Konstante ging |
| 2 | Die beiden Verwendungen in `faltenplan.py` (Zeilen 149, 197) an 4a angleichen | **Zeile 149:** `plan_aktien()` ruft `erste_falte(bot)` — das erste Kalenderjahr, in dem am 1. Januar Universum und Indikator-Vorlauf vorliegen, gerechnet mit der Regel aus `faltenplan_neun` (Pfad-Import der **unveränderten** Datei; aufgerufen wird `_ungebremstes_faltenjahr`, die schrankenfreie Fassung derselben Regel, mit Vermerk, dass der Aufruf nach TB-56b auf `erstes_faltenjahr` wechselt). Der Plan trägt jetzt `erste_falte` und `erste_falte_quelle`. **Zeile 197:** der Krypto-Platzhalter nennt `erste_falte_nach_4a` nachrichtlich mit |
| 3 | Die Meldung in Zeile 197 nennt die Konstante im Text | **Geändert:** „…mindestens {n} Jahre Kursdaten liegen, fruehestens {e}." → „…liegen - ohne feste Untergrenze (TB-56)." Die Ausgabe behauptet nichts mehr, was es nicht gibt |
| 4 | Neuen Faltenplan als eigene Datei neben `faltenplan.json` | **`research/faltenplan_neun/daten/faltenplan_ohne_schranke.json`** (454 637 B): Format von `faltenplan_neun --json` (`frueheste_falte: null`, `schranke`, `herkunft`, `plaene` je Bot mit Falten, Symbolen A/B) **plus** `trockenlauf_3b` je Bot (H und F je Falte, erste Falte mit Loader-Symbol, leere Falten nach 3b (a), Zulassung 4b nach H). Der Trockenlauf kann die Datei über `--faltenplan-json` direkt weiterverwenden |

**Dazu, aus Rückfrage 3:** `research/vorregistrierung/ergebnisse/benchmark_drawdowns_ohne_schranke.json`
(98 444 B) — `benchmark.je_bot()` auf dem neuen Verfahren-A-Plan, mit
`_herkunft`. Die gesperrte `benchmark_drawdowns.json` und die
`ergebnisse/faltenplan.json` (Beleg von TB-30a) sind byteweise unverändert
(`shasum -c`: 2/2 OK).

**Die Docstrings** von `faltenplan.py` (Regeln 2 und 3) beschreiben jetzt, was
der Code tut, und nennen die Entfernung mit Datum; die Regel „mindestens vier
Jahre Training" (Verfahren A) blieb stehen — sie ist nach F18 „keine von
dreien" und war nicht Gegenstand.

---

## Schritt 3 — Der Nachweis

| # | Nachweis | Soll | Ist |
|---|---|---|---|
| 1 | Neuer Plan = Messung Teil A, je Bot | 9 / 9 | **9 / 9** (`nachweise.py`: Kernfelder je Bot gleich; Datei ohne Schranke) ✅ |
| 2 | Kein Bot verliert seine Zulassung nach 4b stillschweigend | benannt | **Keiner verliert sie** — mit / ohne / nach H je Bot in `nachweise_1_3_4_8.txt`; kleinster Wert `elliott_wave` 3 → 4 ✅ |
| 3 | `ERSTE_MOEGLICHE_FALTE` im Quelltext | 0 Treffer ausser Dokumentation | **0 als Bezeichner** (Syntaxbaum, B5); 5 Textstellen, alle Docstring/Kommentar/Dokument — davon zwei in der bis TB-56b unveränderten `faltenplan_neun.py` (Zeilen 61, 119) ✅ |
| 4 | Mutationsgegenprobe (B1) | verändert den Plan | **Beisst:** im Speicher 8/9 Pläne; Wegwerf-Kopie der Vorregistrierung mit einer Zeile 4/4 Aktienpläne 2017/2018 → 2019 ✅ |
| 5 | Sperrklinken | Wanduhr ≤ 6, Pfadbau ≤ 29 | **6 / 29**, GRUEN vorher und nachher ✅ |
| 6 | Basislauf nachher | keine neue rote oder flackernde Stufe | ⚠️ **eine neue rote Datei, erwartet und benannt:** `research/vorregistrierung/test_vorregistrierung.py` (Rückfrage 3 — die gesperrte Benchmark-Tabelle kennt 2017/2018 nicht; rot bis zur Amendment-Entscheidung in TB-56b). Sonst unverändert: siehe Tabelle unten |
| 7 | Registerprüfer nachher | KEIN BEFUND | **KEIN BEFUND**, rc 0, Quelle Beleg **`trockenlauf`** (kein Rückfall) — dreimal: vorher, Arbeitsbaum, nach `7387cc5` ✅ |
| 8 | `faltenplan.json` byteweise unverändert | unverändert | **`93fbf09c…7839`** vorher = nachher = unter `d66a2ce`; `git status` leer ✅ |

**Basislauf nachher** (18:58–19:29 UTC): **60 grün / 6 rot / 1 flackernd / 3
ungeprüft / 1 Zeitgrenze = 71, UNERWARTET 1** — vorher 61/5/1/3/1, UNERWARTET 0.
Der Unterschied der beiden JSON-Berichte je Datei ist **genau eine Zeile**:
`research/vorregistrierung/test_vorregistrierung.py` grün → rot (26,4 s, `KeyError:
'2017'`). Keine weitere rote, keine neue flackernde Stufe; `test_faltenplan_neun.py`
122,9 s OK, `test_log_rotation.py` heute grün (flackernd), `test_drawdown_beide_masse.py`
Zeitgrenze wie bekannt.

**`test_faltenplan_neun.py` nachher: 145/145** (die Datei und ihr Werkzeug sind
unverändert; der neue Plan liegt daneben und wird von ihr nicht gelesen).
**`test_vorregistrierung.py` nachher: Abbruch** in Teil A (`KeyError: '2017'`),
0 Prüfungen gescheitert, weil keine gemessen wurde — der Test ist **rot, nicht
ungeprüft**: er läuft an und bricht ab.

## Schritt 4 — Einchecken

| Commit | Inhalt | `git status` danach |
|---|---|---|
| **`04b42b3`** (18:17 UTC) | Teil A: Messskript, Messung, Plan ohne Schranke, Trockenlauf, Rückfrage 1 samt Antwort, Auftrag nach `docs/auftraege/TB-56.md`, Belege Schritt 0 | nur die noch laufenden Basislauf-Dateien |
| **`7387cc5`** (18:58 UTC) | Teil B: `registerdaten.py`, `faltenplan.py`, neuer Plan, neue Benchmark-Tabelle, Rückfragen 2 und 3, Nachweise 1–5, 7 (Arbeitsbaum), 8 | nur die Basislauf-Dateien „nachher" |
| dritter | dieses Dokument, `HERKUNFT.md`, Basislauf nachher, Datenstand/DB/Snapshot am Ende, Registerprüfer nachher | 0 |

Vor jedem Commit `git status --short` gelesen; `add` + `commit` + `push` je in
einem Zug; `HEAD` = `origin/main` nach jedem Push.

## Zum Schluss

| | Soll | Ist (19:30 UTC) |
|---|---|---|
| Datenstand am Ende | `d9449faf…`/223 | **`d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, 223** ✅ |
| Jede gesicherte `*.db` byteweise identisch | mit Zahl | **12 / 12 OK** (`shasum -a 256 -c` gegen die Quersummen von 18:06 UTC; gemessen vor dem Aktien-Cron 22:15) ✅ |
| Snapshot `--pruefen` | `UNVERAENDERT` | **`UNVERAENDERT`**, rc 0 ✅ |
| `daten/faltenplan.json`, `ergebnisse/benchmark_drawdowns.json`, `ergebnisse/faltenplan.json` | unverändert | **3 / 3 OK** ✅ |
| Dieses Dokument | endet mit „In einfacher Sprache" | ja |
| Keine ZIP; Belege nach `docs/belege/TB-56/`, Auftrag nach `docs/auftraege/TB-56.md` | mitcommittet | ja (`04b42b3`, `7387cc5`, dritter Commit) |

---

## Beobachtungen, die NICHT ausgeführt wurden

1. ⚠️ **Drei Kopien derselben Schranke.** `registerdaten.py::ERSTE_MOEGLICHE_FALTE`
   (jetzt weg), `faltenplan_neun.py::FRUEHESTE_FALTE` (Zeile 120, bis TB-56b),
   `research/krypto_historie/faltenplan.py::FRUEHESTE_FALTE` (Zeile 64, TB-31).
   Der Kommentar über der zweiten verweist auf die erste, die es nicht mehr
   gibt. „Ein Wert, eine Quelle" (Übergabeprotokoll 7.11) galt hier nicht.
   TB-56b: alle drei im selben Zug.
2. ⚠️ **Der Trockenlauf des Laufcodes kann keinen Plan drucken, der Falten
   ausserhalb der Registertabelle hat** (`universum_trockenlauf.py:505`,
   `differenz_H` ist `None` → `TypeError` in `drucke`, **vor** dem JSON-Schreiben).
   Der Registerprüfer würde das als „nicht lauffähig" lesen und still auf das
   TB-40-Dokument zurückfallen (A1). Im Messskript umgangen (Aufruf von
   `trockenlauf()` statt `main()`); das Werkzeug selbst nicht angefasst.
3. ⚠️ **`t3_supertrend` 2018 ist nach 4a eine Falte und nach 3b (a) keine.**
   Die beiden Registertexte geben für diesen Bot verschiedene erste Falten
   (2018 / 2019). Welche gilt, entscheidet TB-56b — der Plan ohne Schranke
   führt beide Angaben nebeneinander.
4. **`elliott_wave` verliert 12 Monate Bestätigungsperiode**, wenn die
   Doppeljahr-Falten 2018 statt 2019 beginnen (2026-01-01 statt 2025-01-01).
   Das ist keine Verschlechterung, aber eine Folge der Parität, die niemand
   gewollt hat und die im Register stehen sollte.
5. **Die gesperrte Benchmark-Tabelle deckt die neuen Falten nicht**, und ihre
   Neuberechnung verschiebt `DD_Toleranz` bei zwei Bots (Rückfrage 3). Der
   Faltenplan (Sperrliste 10.2) und die Benchmark-Tabelle (10.4) hängen
   aneinander — wer den einen berichtigt, braucht ein Amendment für die
   andere. Nebenbei: Registertext 3b (c) rechnet den Benchmark ohnehin auf den
   je Falte geladenen Symbolen, nicht auf dieser Tabelle; ob die Tabelle noch
   massgeblich ist, steht nirgends als ERSETZT-Vermerk.
6. **`research/vorregistrierung/ergebnisse/faltenplan.json`** (Beleg von TB-30a)
   ist unverändert und stimmt nicht mehr mit dem, was `faltenplan.py` heute
   rechnet. Nach der Logik von Regel 2 nicht überschrieben; das Register
   (Abschnitt 3) zitiert die Datei in einem als ERSETZT markierten Abschnitt.
7. **`faltenplan.py` (Vorregistrierung) nennt jetzt in seinem Docstring die
   gemessenen Jahre 2017/2018.** Das ist eine Tatsachenangabe zum Messtag;
   ändert sich das Universum, veraltet sie — die Zahl im Plan selbst wird
   gerechnet.
8. **`benchmark.py` erzeugt auf pandas 2.3.3 je Falte eine `FutureWarning`**
   (`pct_change` mit `fill_method='pad'`, Zeile 119). Ein Termin, kein
   Fehler; unter einer künftigen pandas-Fassung würde die Rechnung anders
   auffüllen.
9. **`pgrep -f basislauf.py` trifft die eigene Warteschleife** (bekannt aus
   TB-46b für `pkill`). Die Wartebefehle dieser Sitzung hingen deshalb nach
   dem Ende des Basislaufs weiter; beendet, ohne Folgen. Beim Warten auf
   einen Python-Prozess: `pgrep -f "Python.*basislauf.py"`.
10. **`test_vorregistrierung.py` bricht mit einer Ausnahme ab statt eine
    Prüfung rot zu melden** (`KeyError` in `auswertung.py`), und der
    Basislauf zählt das als rot — richtig, aber ein Test, der bei einer
    fehlenden Falte im Benchmark mit einer benannten Prüfung fiele, wäre
    lesbarer.
11. **Der Auftrag vermutete die Messung im Vorregistrierungs-Werkzeug**
    („`faltenplan.py` importiert `pandas`"). Das Werkzeug der Registertabelle
    ist `faltenplan_neun.py` (reine Standardbibliothek); die Messung braucht
    `trading-env` nur für den Trockenlauf des Laufcodes (Bot-Loader mit
    pandas).

---

## In einfacher Sprache

**Im Programm stand eine Zahl: Die Auswertung beginnt frühestens 2019.** Die
Regeln sagen das nicht — dort beginnt sie im ersten Jahr, für das ein Bot genug
Daten hat. Vor dem Entfernen wurde gemessen, was die Zahl bewirkt: **Bei acht
von neun Bots hält sie den Beginn zurück**, und ohne sie beginnen die Bots
**nicht alle im selben Jahr** — zwei 2017, sechs 2018, einer 2019, je nachdem,
wie viel Vorlauf ihr Indikator braucht. **Kein Bot verliert dadurch seine
Zulassung**; jeder hat mehr Falten als vorher, nicht weniger. Nur bei einem
Bot, der Zweijahresblöcke nutzt, verschiebt sich der Anfang so, dass sein
Bestätigungszeitraum kürzer wird — das steht im Bericht.

**Der Bot, der Kerzen statt Tage zählt**, braucht wegen kleiner Lücken in
seinen Daten zwei bis drei Tage länger als gedacht; an seinem ersten Jahr
ändert das nichts. Dafür zeigte sich etwas anderes: Bei einem Bot ist das
Jahr 2018 nach der einen Regel eine Falte und nach der anderen leer, weil sein
Datenlader zwei volle Jahre Vorgeschichte verlangt. Das muss die
Registerberichtigung entscheiden, nicht der Code.

**Die Zahl ist jetzt aus dem Programm entfernt.** Der neue Plan liegt als
eigene Datei neben dem alten; der alte ist unverändert. **Welcher gilt,
entscheidet die Berichtigung des Regelwerks** — die ist eine eigene Aufgabe.

**Dreimal musste nachgefragt werden**, weil der Auftrag an einer anderen
Stelle ansetzte als dort, wo die Zahl tatsächlich wirkt, und weil an dieser
Stelle Prüfungen hängen, die Programm und Regelwerk vergleichen. Die
Antworten: Das Werkzeug des Regelwerks wird erst zusammen mit dem Regelwerk
umgestellt, und eine Prüfung bleibt bis dahin rot — offen ausgewiesen, nicht
kaschiert.

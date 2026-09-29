# TB-122: Ergebnis. TB-30b Posten 3 (E-1) — drei Rasterachsen bis zur Indikatorberechnung durchgereicht (`sma_trend_filter` bei `rsi2_mean_reversion`, `bb_lookback` und `bb_squeeze_percentile` bei beiden Volatility-Breakout-Bots); mit Voreinstellungen 13/13 bytegleich, Wertprobe je Bot mit Gegenprobe

**Sitzungstitel:** `TB-122` · **Stand:** 29.09.2026 · **Auftrag:**
`docs/auftraege/MAC_TB-122_posten3_achsen_durchreichen.md` · **Belege:** `docs/belege/TB-122/`
**Eingang:** `04f07ef` (Abgabe TB-121). Commits: `c064405` (Schritt 0), `ab31314` (B), `08153e4` (C1/C2 mit den drei
Testdateien), der Abgabe-Commit (C3–C5, D: dieses Dokument, Journal DU). Gepusht nach 0 und nach der Abgabe.
**Freigabe** (wörtlich im Auftrag): 27.09.2026, ca. 20:20, Auswahlkarte „E-1: TB-30b Posten 3 (Empfohlen)“;
Nachtrag 29.09.2026, ca. 14:52, Auswahlkarte „Ja, bis 3 Testdateien (Empfohlen)“.
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6), ohne Modus. **Kein Abbruchkriterium ausgelöst.**
**Rückfragen an den Betreiber: keine.** **Sichtschutz 27.1:** Alle Vergleichsausgaben liegen unter `$TMPDIR/tb122_*`
(ausserhalb des Repos). Von ihnen wurden nur `cmp` und sha256 genommen. Keine Kennzahl und keine Trade- oder
Zeilenzahl wurde gelesen oder gedruckt.

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | `git status` genau die acht erwarteten Einträge ⇒ `c064405`, gepusht. Ausgang: `register()` `01f5997a…` = Soll, Sonde gegen `46f0ad5d…` rc 2 mit 0 Befunden (Punkt 11 „nicht prüfbar“), die sieben Dateien in **keinem** Abbildeintrag und **nicht** in `EINGEFROREN`. db-Sicherung 12/12 rc 0 |
| **0d** | Code = `live_params.py` bei den Breakout-Bots (126 / 25.0). **Befund:** `rsi2_mean_reversion` führt die Achse **nicht** in `live_params.py`; `SMA_TREND_PERIOD = 200` steht zweimal (`backtest_rsi2.py:88`, `forward_test.py:64`). Nicht angeglichen |
| **A** | Je Bot 4–5 Ausgaben (B6 wortgleich TB-90, Signalpfad über alle Symbole, Kapitalkurve, Optimierer-Kurzlauf auf die heutige Kombination): **13 Dateien**. Zwei Vorher-Läufe hashgleich. B6-Hashes = TB-90 (`8971aa62…`, `de5f6339…`, `e913fe74…`) |
| ⭐⭐ **B** | 7 Dateien, numstat 63/17. Achsen als Parameter von `collect_all_trades` ⇒ `get_trades_for_symbol` ⇒ `compute_indicators` (bei `rsi2` auch ⇒ `run_backtest`, dort `start_i`). Voreinstellung = heutiger Wert. `evaluate_combination_multi`, Raster und `load_all_symbol_data` unverändert ⇒ `ab31314` |
| ⭐⭐ **C1** | **13/13 bytegleich** (`cmp`) |
| ⭐⭐ **C2** | Wertprobe mit der ersten Registerstufe (26 / 20 / 5, aus `registerdaten.raster()`): **16/16, 12/12, 12/12**. Gegenprobe am Stand `c064405`: **rc 1** bei allen drei (14 / 10 / 9 Prüfungen rot) |
| **C3** | *(siehe Abschnitt C3)* |
| **C4** | Trockenlauf ohne Modus: 9/9 rc 0, **18/18 Dateien zeichengleich** |
| **C5** | Sondenausgabe vorher = nachher (`cmp` rc 0, sha256 `dd4b4b95…`). `register()` unverändert `01f5997a…`. **Kein Befund an irgendeinem Punkt** — auch nicht an Punkt 11, weil die Sonde ihn nicht prüfen kann (siehe C5) |

---

## 1. Schritt 0 — Sicherung und Ausgang

- **0a:** Die acht erwarteten Einträge, keiner mehr. `UEBERGABE.md` numstat 361/0 (nur angehängt). Commit `c064405`,
  gepusht.
- **0b** (`0b_ausgang.txt`, Skript `0b_ausgang.sh`): HEAD `c0644058…`. sha256 der sieben Dateien (siehe Tabelle in
  Abschnitt 6). `herkunft.register()` = `01f5997a9a13b4b30162e2a04965670a9ffa8d725a93d579e530dc0708ec2a70` (gemessen,
  = ERGEBNIS_TB-117 Zeile F), `fehlend` leer, 23 Teile. Die Sonde gegen `sperrliste_abbild_2026-09-26_tb117.json`
  (`46f0ad5d…`) liefert rc 2, Pfad-Bestandteile 37/0/0, (ii) 0 und „NICHT PRUEFBAR: Punkt(e) [1, 3, 4, 6, 7, 8, 9, 10,
  11, 12, 13, 14]“. `git status --porcelain` vor und nach der Sonde je 1 Zeile (der Belegordner).
  **Stellung der sieben Dateien, gemessen:** 0 Treffer im Abbild-JSON, 0 in `herkunft.EINGEFROREN` (22 Einträge).
  Sperrliste Punkt 11 lautet „Commit-Hashes von Simulation, Erkennung, Optimierern und Auswertungsskript —
  `herkunft.py::register()` und der Repo-Commit“. `register()` hasht aber nur das Register und `EINGEFROREN`, keine
  der sieben Dateien.
- **0c** (`0c_db_sicherung.txt`): `db_sicherung.sh`, 12/12 Datenbanken, `docs.tar.gz` (Commit `c064405`), rc 0.
- **0d** (`0d_register.txt`): 11.3 (Z. 1143–1160), die fünf Achsenzeilen aus Abschnitt 3 (Z. 264, 265, 273, 279,
  280) und 2.6 letzter Absatz, zeichengleich. Die heutigen Werte je Achse mit Datei:Zeile und der Befund zu
  `SMA_TREND_PERIOD` (oben).

## 2. Schritt A — Vorher-Läufe

**Werkzeug** `a_lauf.py`, Bauart TB-90 B6: je Bot ein eigener Unterprozess mit cwd = Strategieordner und sys.path
= [Strategieordner, shared/]. Die B6-Bauart allein prüft nur das Backtest-Modul. Für die Breakout-Bots ist das
keine der sieben Dateien, der Umbau läge also ausserhalb dessen, was B6 sieht. Deshalb liefen je Bot zusätzlich
**gleichwertige Aufrufe des Signalpfads** mit Zielordner in `$TMPDIR`:

| Datei | Aufruf |
|---|---|
| `b6.csv` | wortgleich TB-90 B6 (ein Symbol, `compute_indicators` + `run_backtest`) |
| `trades.csv` | `equity_simulation.load_all_symbol_data()` + `collect_all_trades(...)` mit den heutigen Parametern, wie der `__main__`-Zweig |
| `trades_regimefilter.csv` | nur `volatility_breakout_crypto`: `apply_btc_regime_filter`, wie `__main__` |
| `equity_curve.csv` | `simulate_portfolio(...)` wie `__main__`; `RESULTS_DIR` bleibt unbenutzt |
| `optimierer.csv` | **A2:** `run_multi_optimisation(all_data)`, Raster von aussen (Modulattribut im Unterprozess, keine Codeänderung) auf die heutige Kombination begrenzt |

**A3** (`a_vorher_hashes.txt`): 13 sha256. Ein zweiter Vorher-Lauf (`$TMPDIR/tb122_vorher2/`) war hashgleich. Alle
13 Dateien sind über 200 B groß, also nicht leer. Die Zeilenzahl ist absichtlich nicht gezählt.

## 3. Schritt B — Umbau (`ab31314`)

**Bauart.** Das Vorbild `rsi2_crypto` reicht die Achse als Parameter von `collect_all_trades` über
`get_trades_for_symbol` bis `compute_indicators` und `run_backtest` durch. `get_trades_for_symbol` rechnet dort die
Indikatoren je Aufruf aus den Rohkursen, die der Lader liefert. So ist es jetzt gebaut:

| Bot | Datei | Änderung |
|---|---|---|
| `rsi2_mean_reversion` | `backtest_rsi2.py` | `compute_indicators(price_df, sma_trend_period=SMA_TREND_PERIOD)`; `run_backtest(..., sma_trend_period=SMA_TREND_PERIOD)`, dort `start_i = sma_trend_period` |
| | `multi_symbol_optimise.py` | `get_trades_for_symbol(..., sma_trend_period=SMA_TREND_PERIOD)` ⇒ `compute_indicators(df_ind, sma_trend_period)` und `run_backtest(..., sma_trend_period=...)` |
| | `equity_simulation.py` | `collect_all_trades(..., sma_trend_period=SMA_TREND_PERIOD)`; Import der Voreinstellung aus `backtest_rsi2` |
| `volatility_breakout` | `multi_symbol_optimise.py` | `get_trades_for_symbol(..., squeeze_lookback_days=SQUEEZE_LOOKBACK_DAYS, squeeze_percentile=SQUEEZE_PERCENTILE)` ⇒ `compute_indicators(df_ind, …)`; Import der beiden Namen aus `backtest_breakout` (dort aus `live_params.py`) |
| | `equity_simulation.py` | `collect_all_trades(..., squeeze_lookback_days=BB_LOOKBACK, squeeze_percentile=BB_SQUEEZE_PERCENTILE)`; Import aus `live_params.py` |
| `volatility_breakout_crypto` | `multi_symbol_optimise.py`, `equity_simulation.py` | wie `volatility_breakout`; `get_trades_for_symbol` rechnete die Indikatoren schon je Aufruf, es fehlten nur die Argumente |

**Wo die Bauart abweicht, und warum:**
1. **Neue Parameter hängen hinten an, mit Voreinstellung.** Beim Vorbild steht `sma_trend_period` positionell
   in der Mitte und ohne Voreinstellung. Hier rufen Walk-Forward, `evaluate_combination_multi`, `bot_lauf.py`, der
   TB-103-Trockenlauf und eine Reihe von Research-Skripten die Funktionen positionell auf (z. B.
   `research/exposure_messung/bot_lauf.py`, `research/order_sensitivity/run_one_bot.py`,
   `research/drawdown_reihenfolge/adapters.py`). Eine Umstellung der Reihenfolge hätte diese Aufrufer gebrochen, und die meisten
   liegen ausserhalb der sieben Dateien.
2. **Die Aktien-Bots rechnen die Indikatoren in `get_trades_for_symbol` neu**, obwohl `load_all_symbol_data()` sie
   schon mit der Voreinstellung vorberechnet. Der Lader bleibt unverändert, weil andere Leser die vorberechneten
   Spalten aus `all_data` lesen: die Zuteilung (`kursdaten`), `research/trailing_stops` (`bb_upper`, `is_squeeze`)
   und `research/volatility_scaled_sizing`. Nimmt stattdessen der Lader die Achse, gibt es **zwei** Stellen für
   einen Wert (Lader und `collect_all_trades`), die auseinanderlaufen können. Die Neuberechnung aus dem übergebenen
   Frame ist mit der Voreinstellung zahlengleich (C1). Geprüft ist auch, dass alle Aufrufer volle, nicht
   gekürzte Frames übergeben: Walk-Forward kürzt nur die Trades (`entry_cutoff`/`cutoff_end`), nicht die Kurse.
   Kosten: Der Optimierer rechnet die Indikatoren je Kombination neu. Gemessen: Signalpfad plus Optimierer-Kurzlauf
   `volatility_breakout` 11 s ⇒ 14 s, `rsi2_mean_reversion` 10 s ⇒ 11 s.

**B2 — Leser von `SMA_TREND_PERIOD`** (`b2_leser.txt`, vor B gemessen): `backtest_rsi2.py` selbst (Z. 88, 100,
122); `multi_symbol_optimise.py:35` importiert den Namen (bis B unbenutzt, jetzt Voreinstellung); `forward_test.py:64`
führt eine **eigene** Konstante gleichen Namens; `docs/belege/TB-120/c_messung.py:94` liest die Quellzeile
`SMA_TREND_PERIOD = …`, die erhalten bleibt; `research/faltenplan_neun/faltenplan_neun.py:212` zitiert die
Quellzeile `start_i = SMA_TREND_PERIOD` als Text (siehe Befund F2). Die `es.SMA_TREND_PERIOD`-Treffer in
`research/` betreffen `rsi2_crypto`. **Der Name bleibt deshalb als Voreinstellung stehen.**

**B3/B4:** Kein Aufräumen, keine Umbenennung. Der Docstring von `compute_indicators` nennt weiter „SMA(200)“. In
den beiden `multi_symbol_optimise.py` der Aktien-Bots sind nur `get_trades_for_symbol` und die Importzeile
geändert. `evaluate_combination_multi`, `run_multi_optimisation`, `*_RANGE` und `load_all_symbol_data` stehen im
Diff mit 0 Codezeilen (`b_diff.txt`). Für C1 und C2 musste dort nichts geändert werden.

## 4. Schritt C — Nachweis

**C1** (`c1_vergleich.txt`): `a_lauf.py` am Stand `ab31314` nach `$TMPDIR/tb122_nachher/`, `cmp` je Datei ⇒
**13/13 IDENTISCH** (B6 3/3, dazu `trades`, `trades_regimefilter`, `equity_curve`, `optimierer`).

**C2** (`c2_wertprobe.txt`, Testdateien `strategies/<bot>/test_posten3_durchreichung.py`): Monkeypatch auf
`multi_symbol_optimise.compute_indicators` und `.run_backtest`, synthetische Kursreihe, kein Lesen aus `data/`.
Der Probewert ist die erste Stufe aus `registerdaten.raster()` (Abschnitt 3); er steht nicht als Zahl im Test.
- `rsi2_mean_reversion` **16/16**: Signalpfad und Optimierer-Pfad übergeben 26 an `compute_indicators` und
  `run_backtest`; `sma_trend` = SMA(26); ohne Argument kommt 200 an; vier Signaturen mit Voreinstellung 200; der
  Scan beginnt bei der Stufe (konstruierter Fall: Signal an Balken 30 wird mit 26 gefunden, mit 200 nicht).
- `volatility_breakout` und `volatility_breakout_crypto` **je 12/12**: (20, 5) kommt in `compute_indicators` an;
  `squeeze_thresh` ist das Quantil mit (20, 5) und nicht das mit (126, 25.0); ohne Argument kommen (126, 25.0) an;
  drei Signaturen mit diesen Voreinstellungen.
- **Gegenprobe (40.7):** `c2_probe.sh` packt `c064405` per `git archive` nach `$TMPDIR/tb122_c2_gegenprobe` aus
  und legt dieselben Testdateien hinein. Ergebnis **rc 1 / rc 1 / rc 1** (2 bestanden, 14 rot / 2, 10 / 3, 9).
  Die Probe scheitert jeweils an `unexpected keyword argument`, am fehlenden Aufruf von `compute_indicators` im
  Optimierer-Pfad und an den fehlenden Signaturparametern.

**C3** (`c3_vorher.txt`, `c3_nachher.txt`, Skript `c3_tests.sh`): Testmenge wie TB-117 E, dazu die acht
Research-Tests, die einen der drei Bots nennen. `test_vorregistrierung` lief mit einer Zeitgrenze von 2400 s.
PLATZHALTER_C3

**C4** (`c4_trockenlauf.txt`): Der TB-103-Trockenlauf (`d_trockenlauf.py`, wie in TB-117 E) lief **ohne Modus**,
ohne Snapshot und ohne Lesehaken, für alle neun Bots. Vorher (zweimal, hashgleich) und nachher: 9/9 rc 0,
**18/18 Dateien zeichengleich**. Den Modus-Lauf aus TB-117 E (Snapshot `63e4b6c8…`) habe ich **nicht** gefahren,
weil er nicht freigegeben ist.

**C5** (`c5_nachher.txt`): Die Sonde gegen `46f0ad5d…` liefert nach B **dieselbe Ausgabe Byte für Byte** wie in 0b
(sha256 `dd4b4b95…`, 84 Zeilen, rc 2, 37/0/0). `register()` bleibt `01f5997a…`, `fehlend` leer. Erwartet war laut
Auftrag „Befunde nur an Punkt 11, alter ⇒ neuer Hash“. Tatsächlich gibt es **gar keinen Befund**, weil die Sonde
Punkt 11 nicht prüfen kann („NICHT PRUEFBAR“) und keine der sieben Dateien in Abbild oder `EINGEFROREN` steht.
Das ist kein Abbruchkriterium, denn es gibt keinen Befund an einem anderen Punkt. Es heisst aber: **Der
Hash-Übergang dieser sieben Dateien ist maschinell nirgends festgehalten.** Er steht nur im Commit und im Entwurf
unten (Befund F4, Frage an Fable).

## 5. Befunde neben dem Auftrag (`befunde.txt`, nichts geändert)

- **F1 — Der Scanbeginn der Breakout-Bots hängt weiter an der Voreinstellung.** In `backtest_breakout.py` (beide
  Bots, **ausserhalb der sieben Dateien**) gilt `WARMUP_PERIOD = max(20, SQUEEZE_LOOKBACK_DAYS, 20)` = 126 als
  Modulkonstante, und `run_backtest` beginnt bei Balken 127, egal welches `bb_lookback` ankommt. Bei den Stufen über
  126 ist das unschädlich: Bis zur Stufe ist `squeeze_thresh` NaN, und `bb_width <= NaN` ist falsch, also entsteht
  kein Signal. Bei den Stufen **20 und 97** beginnt der Scan dagegen später, als die Indikatoren es erlauben. Krypto
  übergibt kein `entry_cutoff`, dort fehlen je Symbol die Balken 21…126. Bei den Aktien überdeckt `entry_cutoff`
  (10 Jahre) das, ausser bei Symbolen mit kürzerer Historie. Die Achse erreicht also die Indikatorberechnung (der
  Auftrag), aber noch nicht vollständig den Backtest. Die Behebung ginge nur in `backtest_breakout.py`, einer
  achten Datei, und ist deshalb gemeldet statt getan. Mit Voreinstellungen würde sie keine Ausgabe ändern. Das
  Vorbild `rsi2_crypto` hat die Lücke nicht (`start_i = sma_trend_period`), `rsi2_mean_reversion` nach B auch nicht
  mehr.
- **F2 — Der Vorlauf ist jetzt achsenabhängig, steht im Faltenplan-Werkzeug aber als feste Zahl.**
  `faltenplan_neun.py` führt `vorlauf_balken` 200 (`rsi2_mean_reversion`), 127 (beide Breakout-Bots) und 150
  (`rsi2_crypto`) samt Quellzeile als Text. Nach Posten 3 reicht der Vorlauf bis zur grössten Stufe (252, 252/365,
  365). Für `rsi2_crypto` gilt das schon länger. Der Text „`backtest_rsi2.py:117 'start_i = SMA_TREND_PERIOD'`“ ist
  seit B auch wörtlich überholt (jetzt Z. 129 `start_i = sma_trend_period`; die 117 stimmte schon vorher nicht).
- **F3 — `SMA_TREND_PERIOD` steht nicht in `live_params.py` und zweimal im Code** (`backtest_rsi2.py:88`,
  `forward_test.py:64`). Das widerspricht der Projektregel „jeder Handelsparameter genau einmal in
  `live_params.py`“. Der Krypto-Zwilling führt `SMA_TREND_FILTER` in `live_params.py`.
- **F4 — Punkt 11 ist blind für den Signalpfad** (siehe C5).

## 6. Entwurf der Tatsachennotiz für den Registerauftrag E-2

> ⚠️ **ENTWURF — nicht im Register.** Wortlaut zur Übernahme durch E-2; Register und Regelwerk waren in TB-122
> nicht freigegeben.
>
> **Vollzug TB-30b Posten 3 (11.3) in TB-122 (Tatsachennotiz nach 37.3)**
>
> **Gemessen in TB-122, 29.09.2026** (Belege `docs/belege/TB-122/`, Ergebnis
> `docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md`). Eingang `04f07ef`, Schritt 0 `c064405`. Freigabe des
> Betreibers 27.09.2026, ca. 20:20 (Auswahlkarte „E-1: TB-30b Posten 3“), Nachtrag 29.09.2026, ca. 14:52 (bis zu drei
> Testdateien; 27c R31 (b)). Kein Abbruchkriterium ausgelöst.
>
> **Grund:** 11.3 — `sma_trend_filter` war bei `rsi2_mean_reversion` eine Konstante; `bb_squeeze_percentile` und
> `bb_lookback` erreichten bei beiden Volatility-Breakout-Bots die Indikatorberechnung nicht. Ohne die Durchreichung
> ist das registrierte Raster (Abschnitt 3) für diese drei Bots nicht rechenbar (R49 (h): 11.3 ist E-1).
>
> **Hash-Übergänge nach 37.3** (Sperrlistenpunkt 11, „Commit-Hashes von Simulation, Erkennung, Optimierern“):
>
> | Datei | vorher | nachher | Commit | vollzieht |
> |---|---|---|---|---|
> | `strategies/rsi2_mean_reversion/backtest_rsi2.py` | `c0a59a43…` | `836b032a…` | `ab31314` | 11.3 |
> | `strategies/rsi2_mean_reversion/multi_symbol_optimise.py` | `9b2d2a2f…` | `777f5cb0…` | `ab31314` | 11.3 |
> | `strategies/rsi2_mean_reversion/equity_simulation.py` | `3a29a4f1…` | `864907fb…` | `ab31314` | 11.3 |
> | `strategies/volatility_breakout/multi_symbol_optimise.py` | `93799bdd…` | `f0a4ee43…` | `ab31314` | 11.3 |
> | `strategies/volatility_breakout/equity_simulation.py` | `fde65dbb…` | `7cbc7f00…` | `ab31314` | 11.3 |
> | `strategies/volatility_breakout_crypto/multi_symbol_optimise.py` | `e7710d4d…` | `02548e2e…` | `ab31314` | 11.3 |
> | `strategies/volatility_breakout_crypto/equity_simulation.py` | `c760c6b8…` | `11094387…` | `ab31314` | 11.3 |
>
> Neu (kein Vorher), Commit `08153e4`: `strategies/rsi2_mean_reversion/test_posten3_durchreichung.py` `1b4edfbc…`,
> `strategies/volatility_breakout/test_posten3_durchreichung.py` `50e872e2…`,
> `strategies/volatility_breakout_crypto/test_posten3_durchreichung.py` `3f78f6da…`.
>
> **`herkunft.register()`:** `01f5997a…` vorher = nachher. Die sieben Dateien gehören nicht zu den eingefrorenen
> Teilen; die Sonde gegen `46f0ad5d…` ist vorher und nachher byte-gleich (Punkt 11 „nicht prüfbar“). Der Übergang
> steht deshalb nur hier und im Commit.
>
> **Nachweis:** Mit den Voreinstellungen (200; 126 / 25.0) sind die Ausgaben von B6, Signalpfad, Kapitalkurve und
> Optimierer-Kurzlauf **13/13 bytegleich**; der Trockenlauf ohne Modus ist 18/18 zeichengleich. Die erste
> Registerstufe (26; 20 / 5) kommt nachweislich in der Indikatorberechnung an (16/16, 12/12, 12/12); am Stand vor
> dem Umbau scheitert dieselbe Probe (40.7).
>
> **Folge aus R47 (Fable 29b, F-17):** Nach Posten 3 ist `SMA_TREND_PERIOD` bei `rsi2_mean_reversion` **Rasterachse**
> (`sma_trend_filter`), nicht Parameterdatei; der Name in `backtest_rsi2.py` bleibt als Voreinstellung.
>
> **Stand 11.3:** geschlossen bis zur Indikatorberechnung; offen der Scanbeginn der Breakout-Bots
> (`backtest_breakout.py::WARMUP_PERIOD`, TB-122 Befund F1).

## 7. Für Fable

*(Vom steuernden Chat nach dem Fable-Filter vorzuprüfen, `UEBERGABE.md` Nachtrag 29.09.2026, 13:20.)*

1. **F1 — Gehört der Scanbeginn der Breakout-Bots zu 11.3?** `WARMUP_PERIOD` in `backtest_breakout.py` hängt an der
   Voreinstellung 126. Bei den Stufen 20 und 97 beginnt der Scan später, als die Indikatoren es erlauben (Krypto je
   Symbol ab Balken 127). Neigung: ja, als Nachtrag zu Posten 3 in `backtest_breakout.py` beider Bots (achte und
   neunte Datei), mit derselben Nachweisform. Mit Voreinstellungen ist das bytegleich. Ist „bis zur
   Indikatorberechnung“ (Auftrag) die Grenze von 11.3, oder der ganze Backtest?
2. **F2 — Welcher Vorlauf gilt für den Faltenplan, wenn er achsenabhängig ist?** Heute steht in
   `faltenplan_neun.py` der Vorlauf der Voreinstellung (200, 127, 150). Die grösste Stufe liegt darüber (252,
   252/365, 365). Zählt für Lesart A die grösste Stufe des Rasters oder die Voreinstellung?
3. **F4 — Soll der Signalpfad maschinell zur Sperrliste gehören?** Punkt 11 ist für die Sonde „nicht prüfbar“, und
   `register()` hasht die Bot-Dateien nicht. Ein Übergang wie in TB-122 ist nur im Commit und in der Tatsachennotiz
   sichtbar. Soll das Abbild vor dem Tag (37.3) eine Gruppe für die Signalpfad-Dateien der neun Bots führen?
4. **F3 — Soll die Voreinstellung von `sma_trend_filter` nach `live_params.py`?** Das wäre wie beim Krypto-Zwilling
   `SMA_TREND_FILTER`, samt der zweiten Kopie in `forward_test.py`. Das ist eine Parameterdatei-Änderung ausserhalb
   des Laufs und braucht deshalb eine eigene Freigabe.
5. **Bauart:** Die Aktien-Bots rechnen die Indikatoren in `get_trades_for_symbol` je Aufruf neu, der Lader
   berechnet sie weiterhin mit den Voreinstellungen vor (Abschnitt 3). Ist das als Zellen-Kern-Eingang (R43) so
   recht, oder soll der Lader Rohkurse liefern wie beim Krypto-Zwilling? Das hätte Folgen für die Zuteilung und für
   Research-Leser.

## 8. Nicht getan

- Register und Regelwerk nicht geändert; die Tatsachennotiz steht nur als Entwurf oben.
- Kein neues Sperrlisten-Abbild (37.3: nach Bündeln).
- `backtest_breakout.py`, `forward_test.py`, `live_params.py`, `faltenplan_neun.py` nicht geändert (F1–F3).
- `evaluate_combination_multi`, `run_multi_optimisation`, die Raster (`*_RANGE`) und `load_all_symbol_data` nicht geändert.
- Posten 4 und 5, `shared/zuteilung.py`, `herkunft.py`, `paths.py` nicht angefasst.
- Kein Lauf im Modus, kein Lauf auf dem Snapshot. Nichts unter `research/**/ergebnisse/` oder `research/**/daten/`
  geschrieben. Kein `crontab`, keine Datenbank ausser der lesenden Sicherung 0c.
- Die `$TMPDIR`-Ordner sind **nicht gelöscht**: `$TMPDIR` = `/var/folders/b_/yqcfpq996cxb1_v02m180f580000gn/T/`,
  darin `tb122_vorher`, `tb122_vorher2`, `tb122_nachher`, `tb122_c2_gegenprobe`, `tb122_c3_vorher`,
  `tb122_c3_nachher`, `tb122_c4_vorher`, `tb122_c4_vorher2`, `tb122_c4_nachher` und die zugehörigen `.txt`.

## 9. In einfacher Sprache

Drei Einstellungen, die der grosse Lauf durchprobieren soll, kamen bisher nicht bei den Bots an. Beim
RSI-2-Aktienbot war die Länge des Trendfilters fest eingebaut. Bei den beiden Ausbruchs-Bots blieben zwei
Squeeze-Einstellungen unterwegs stecken. Jetzt lassen sich alle drei von aussen übergeben. Ohne Angabe gilt genau
der bisherige Wert.

Die 13 Ausgabedateien mit den heutigen Werten sind **Byte für Byte gleich** wie vorher. Ein Test pro Bot zeigt,
dass ein anderer Wert aus dem Register wirklich bis zur Indikatorberechnung durchkommt. Mit dem alten Code
scheitert derselbe Test.

Zwei Dinge sind noch offen und nur gemeldet, weil sie Dateien ausserhalb des Auftrags betreffen: Bei den
Ausbruchs-Bots hängt der Startpunkt des Durchlaufs noch am alten Wert. Und die Kontrollsonde sieht Änderungen an
diesen Bot-Dateien grundsätzlich nicht.

# TB-115: Ergebnis. Drei Verfahrensmessungen vor dem Tag, nur lesend — M1 alle neun Bots entscheiden auf der geschlossenen Kerze (Papier 9/9 über `entscheidungskerze.lade`, Selektion 9/9 ohne Teilkerze am gelesenen Rand; ⚠️ eine Teilkerze liegt im Snapshot, `XAUTUSDT_1h.csv`, von keinem Leser gelesen); M2 die 150 Aktienreihen sind split- **und** dividendenbereinigt (`auto_adjust=True`, kein `Adj Close`), keine Bot-Regel nutzt ein absolutes Preisniveau, ⚠️ aber Stufe 3 der Zuteilungskaskade vergleicht Dollar-Volumen über Symbole, und das verschiebt die Dividendenbereinigung; M3 die Sonde deckt von der Kette nur `auswertung.py` und seine Tabellen — Snapshot, Erzeuger, `zellen.csv` und Bericht sind nicht an sie gebunden, und `auswertung.py` liest `herkunft.json` nicht

**Sitzungstitel:** `TB-115` · **Stand:** 26.09.2026, ca. 20:15 · **Auftrag:**
`docs/auftraege/MAC_TB-115_drei_verfahrensmessungen.md` · **Belege:** `docs/belege/TB-115/`
**Eingang:** `90307cb` (Abgabe TB-114). Commits: `da64869` (Schritt 0), der Abgabe-Commit (Belege, Journal DN, dieses
Dokument). Nach jedem Commit gepusht.
**Grundlage:** Register 45.7 (R7, Liste der Verfahrensmessungen nach 27.2), Fable 26a Abschnitt 2 (b). Freigabe des
Betreibers 26.09.2026, ca. 16:20 und 18:40 (Auswahlkarten, wörtlich im Auftrag).
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6). Ein Wegwerflauf (M1, vorhandener Test) in einem frischen Klon im
Scratchpad; im Hauptordner nur lesende Skripte.

⛔ **Sichtschutz 27.1 eingehalten:** Kein Lauf hat ein Ergebnis des Selektionsraums gerechnet oder gelesen. Gezählt
wurden Dateien, Spalten, Codezeilen und Kerzen-Zeitstempel; gelesen wurden Kurswerte nur an den acht Split-Tagen der
Stichprobe. Keine Sharpe-Werte, keine Trade-Zahlen, keine Zeilenzahlen von Trade-Listen.

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | Schritt 0 committet (`da64869`, md5 beider Betreiberdateien ✔), keine weiteren uncommitteten Dateien. 0b vorher = nachher: `register()` `5acb4c19…`, Sonde gegen `5e5ad109…` 34/0/0 (rc 2 wie immer: 12 Punkte nicht dateibezogen), Arbeitsbaum ausserhalb `docs/` leer |
| ⭐⭐ **M1** | **Papier: 9 × ja.** Jeder `forward_test.py` lädt jede Kursreihe über `entscheidungskerze.lade` (je 1 Aufruf), kein Abruf an der Schicht vorbei, keine zweite Datenquelle; jeder `iloc[-1]`/`iloc[-2]` in einer Entscheidung sitzt auf der gefilterten Tabelle. Vorhandener Test im Wegwerfklon 130/130 (drei Bots wirklich gestartet, 9/9 per AST). **Selektion: 9 × ja** — der Lader liest die ganze Datei ohne eigenen Filter, aber die letzte Kerze jeder gelesenen Datei ist abgeschlossen (Zeitstempel: geschrieben 2 h 19 min bis 10 h 19 min nach Kerzenschluss, ein gemeinsamer Stand 15.09. 09:00–09:59 UTC für alle 72 Krypto-Dateien). ⚠️ **Befund:** `XAUTUSDT_1h.csv` im Snapshot endet auf einer **Teilkerze** (geschrieben 21 min vor Kerzenschluss); gelesen wird sie von keinem Bot, weil vier Ausschlusslisten das Symbol streichen |
| ⭐⭐ **M2** | (a) 174 `_1d.csv`, davon 24 Krypto und **150 Aktien** = `config/sp500_top150.txt`; Quelle **yfinance**, `yf.download(…, period="max", interval="1d", auto_adjust=True)`, `actions`/`back_adjust` nicht gesetzt. Die Dateien sind **älter als das Repo** (geschrieben 02.09.2026, 04:20–04:22 UTC; Initial-Commit `0f6491b` 21:12 UTC, seither unverändert). (b) Spalten `open_time,open,high,low,close,volume`, **kein `Adj Close`**; Split-Stichprobe 8/8 ohne Sprung (**split-bereinigt**); Dividenden: bei den Zahlern liegt der letzte Bereinigungsschnitt im Juni–August 2026 (**dividendenbereinigt**). (c) **Kein absolutes Preisniveau** in den Regeln der vier Aktien-Bots (P1 = 0 Fundstellen). ⚠️ **Befund:** Die Zuteilungskaskade (`shared/zuteilung.py`, Sperrlistenpunkt 10) reiht auf Stufe 3 nach dem Median von `close * volume` — ein Währungsniveau über Symbole hinweg; die Dividendenbereinigung drückt `close` rückwärts, `volume` nicht. Bei drei Aktien-Bots ohne Signalspalte entscheidet Stufe 3, sobald das Buch leer ist. Randbefund im Papierpfad: abgelegte absolute Niveaus gegen später neu bereinigte Kurse |
| ⭐⭐ **M3** | Die Sonde prüft Datei-Hashes gegen das Abbild: 14 Punkte (11 Pfade) und 19 eingefrorene Dateien, **aus dem Abbild heraus**. Von der Kette gebunden ist nur **Glied 4** (`auswertung.py` S+A+E+W, seine Importe und Tabellen). **Snapshot** nur über die Startprüfung, und die **liest** den Hash aus dem MANIFEST, statt ihn nachzurechnen; **Erzeuger** gibt es nicht; **`zellen.csv`** und **Bericht** haben keinen festen Pfad. ⚠️ **Befund:** `auswertung.py` nennt `<wurzel>/<bot>/herkunft.json` in seinem Vertrag, **liest es aber nirgends** — und `auswertung.py` ist eingefroren |

---

## 0. Schritt 0 und Ausgangswerte

**0a.** Vorgefunden: `AKTUELLER_AUFTRAG.md` (geändert), der Auftrag und die zwei Betreiberdateien (unversioniert). md5
`AF-F0_BESTANDSAUFNAHME_2026-09-26.md` = `8dc52a75…` ✔, `FABLE_ANFRAGE_2026-09-26a_…` = `06a84efd…` ✔. Keine
weiteren uncommitteten Dateien. Commit `da64869`, gepusht.

**0b** (`0b_ausgang.sh`, `0b_ausgang.txt`, gemessen **nach** dem Schritt-0-Commit, deshalb HEAD `da64869` statt
`90307cb`; der letzte Commit ausserhalb `docs/` ist weiter `e07fefd`):

| Wert | Soll | vorher | nachher |
|---|---|---|---|
| `herkunft.register()` | `5acb4c19…` | `5acb4c19…`, 20 Teile, `fehlend` leer | gleich |
| Sonde gegen `sperrliste_abbild_2026-09-26_tb114.json` | 34/0/0 | 34/0/0, (ii) 0, rc 2 | gleich |
| Abbild-Datei | `5e5ad109…` | `5e5ad109…` | gleich |
| Arbeitsbaum ausserhalb `docs/` | leer | leer | leer |

---

## 1. M1 — Liest jeder der neun Bots die geschlossene Kerze?

### 1.1 Papierpfad (`forward_test.py`)

**Suche** (`m1_papier.py` → `m1_papier.txt`, AST, Muster im Kopf des Skripts): (1) `entscheidungskerze.lade`/`.melde`;
(2) `fetch_historical_data` ausserhalb des `abruf=`-Lambdas; (3) jede andere Datenquelle (`read_csv`, `yf.*`,
`Client()`, `requests.*`); (4) Zugriffe auf die letzte Zeile — M-a `iloc[negativ]`, M-b `.tail()`, M-c `[negativ:]`,
M-d `iat`/`values`/`[-1]`, M-e `.max()`; dazu M-f Wanduhr (`utcnow`, `now`, `time`).

**Messung:** alle neun `lade` 1, `melde` 1, **Abruf an der Schicht vorbei 0, andere Datenquelle 0**. Jede Kursreihe,
die ein Bot benutzt — auch `BTCUSDT` für den Regimefilter von `t3_supertrend` und `volatility_breakout_crypto` —
kommt aus derselben Schleife über `lade()`. `lade()` gibt die Tabelle **bis einschliesslich** der Entscheidungskerze
zurück (`nur_entscheidbar`), für `data/` und für den Rückfall-Abruf durch dieselben Zeilen.

**Einordnung jeder Fundstelle aus (4), gelesen:**

| Fundstelle | Bots | Art | Warum |
|---|---|---|---|
| `row = df.iloc[-1]` (und `prev = df.iloc[-2]`) in `find_new_signals` | rsi2_crypto Z.174, rsi2_mean_reversion Z.185, t3_supertrend Z.146/147, turtle_soup_crypto Z.171, turtle_soup_stocks Z.173, volatility_breakout Z.177/178, volatility_breakout_crypto Z.184/185 | **Entscheidung** (Signal, Einstiegskurs, Stop) | `df` ist die Rückgabe von `lade()` bzw. `compute_indicators(lade(…))` — die letzte Zeile **ist** die Entscheidungskerze |
| `latest_price_row.iloc[-1]` in `find_new_signals` | elliott_wave Z.175/176, elliott_wave_stocks Z.208/209 | **Entscheidung** (Einstiegskurs, Einstiegszeit) | `latest_price_row = df[df["open_time"] > end_time]`, eine Zeilenauswahl aus der gefilterten Tabelle |
| `…["supertrend_dir"].iloc[-1]` / `btc_regime["btc_regime"].iloc[-1]` | t3_supertrend Z.225, volatility_breakout_crypto Z.276 | **Entscheidung** (Regimefilter sperrt alle Einstiege) | aus `indicator_data["BTCUSDT"]` bzw. `raw_data["BTCUSDT"]`, beide aus `lade()` |
| `closed_trades.tail(5)` in `print_summary` | alle neun | **Anzeige** | Datenbankzeilen, keine Kursdaten |
| `datetime.utcnow()` im Kopf des Laufs | alle neun | **Protokoll** | nur `print` |
| `pd.Timestamp.utcnow()` in `find_new_signals` | elliott_wave Z.150, elliott_wave_stocks Z.166 | **Entscheidung, aber keine Kerzenwahl** — siehe Randbefund R1 | Frische-Grenze `SIGNAL_FRESHNESS_HOURS` an der Wanduhr |

Die Ausstiegsprüfungen (`check_open_trades`) laufen über `df[df["open_time"] > entry_time]` derselben gefilterten
Tabelle; kein zweiter Zugriff.

**Wegwerflauf:** Die Zuordnung folgt aus dem Code; als Gegenprobe lief der vorhandene Test
`shared/test_entscheidungskerze.py` (TB-38, mit Mutationsproben, Abschnitt 12) im frischen Klon
(`m1_test_entscheidungskerze.txt`): **130/130, rc 0**. Abschnitte 8–10 starten `t3_supertrend`,
`turtle_soup_crypto` und `turtle_soup_stocks` **wirklich** gegen eine Kursreihe mit einer laufenden Kerze, die einen
Stop auslösen und ein Signal eröffnen **würde**; Abschnitt 13 prüft alle neun per AST auf `lade`/`melde` und auf
Direktaufrufe. Die übrigen sechs Bots sind nur per Code und AST belegt, nicht wirklich gestartet — sie haben dieselbe
Bauart (gleiche Ladeschleife, gleiche `find_new_signals`-Form).

**Aktien:** Der Kalender antwortet im `trading-env` (`pandas_market_calendars` 4.6.1): `letzter_handelstag` am
25.09.2026 20:15 UTC ⇒ `2026-09-25`, kein Rückfall auf die sichere Schranke. Die Aktien-Bots nehmen um 22:15 Uhr die
Kerze des Tages.

### 1.2 Selektionspfad (Laufbereich: `equity_simulation.py`, `multi_symbol_optimise.py`, `backtest_*.py`)

`multi_symbol_walk_forward.py` steht **nicht** im gemessenen Laufbereich (TB-112, `a2_laufbereich.txt`) und wurde
deshalb nicht bewertet. Alle neun `load_all_symbol_data()` lesen `DATA_DIR/<symbol>_<intervall>.csv` **vollständig**
(unter dem Modus = Snapshot-Wurzel), streichen nur Kerzen ohne Kurs und haben **keinen** eigenen Filter auf
abgeschlossene Kerzen. Ob eine Teilkerze gelesen wird, hängt also allein am Bestand.

**Messung** (`m1_letzte_kerze.py` → `.txt`; je Datei nur Kopfzeile und Zeitstempel der letzten Zeile, dazu mtime):

| Gruppe | Dateien | letzte Kerze | geschrieben (mtime, UTC) | Abstand zum Kerzenschluss (kleinster) |
|---|---|---|---|---|
| Aktien 1d | 150 | `2026-09-01` (alle) | 02.09. 04:20:40 – 04:22:43 | 4 h 20 min nach der sicheren Schranke D 23:59:59 (nach NYSE-Schluss 20:00 UTC also > 8 h) |
| Krypto 1d | 24 | `2026-09-14` (alle) | 15.09. 10:19 – 10:30 | 10 h 19 min |
| Krypto 4h | 24 | `2026-09-15 04:00` (alle) | 15.09. 10:19 – 10:30 | 2 h 19 min |
| Krypto 1h | 25 | `2026-09-15 08:00` (24), **`2026-08-30 18:00` (1)** | 30.08. 18:39 – 15.09. 10:29 | ⚠️ **−21 min** bei `XAUTUSDT_1h.csv` |

- mtime der Snapshot-Kopien = mtime in `data/` (223/223); die Aktiendateien stehen seit `0f6491b` unverändert im Git.
- Ohne `XAUTUSDT_1h.csv` vertragen alle 72 Krypto-Dateien **einen** gemeinsamen Stand, 15.09.2026 09:00:00–09:59:59.999
  UTC — das passt zum TB-34-Neuaufbau (`--stand`, Filter `close_time <= stand`, `kursdaten_neuaufbau.abgeschlossene_kerzen`).
- Die Teilkerzen-Prüfung des Snapshots (`snapshot.py`, TB-47/49) sieht `rand_letzte` nur dort, wo ein feinerer Zeuge
  liegt (Krypto 1d/4h, 48 Dateien); **die 175 Dateien ohne Zeugen** (150 Aktien, 25 Krypto-1h) sind allein durch den
  Schreibpfad und die Zeitstempel belegt.

**Die letzte Kerze im Selektionspfad wird gelesen**, und zwar nicht nur als Rechenzeile: als Anker
`df["open_time"].max() - RECENT_YEARS_ONLY` (die vier Aktien-`multi_symbol_optimise.py`), als Ausstieg zum letzten verfügbaren
Preis bei `elliott_wave`/`elliott_wave_stocks` (`simulate_trade`, `future.iloc[-1]`), und als Ende des Scans
(`max_offset = min(MAX_HOLD, n - 1 - i)`, sonst Scan-Ende). An allen neun gelesenen Beständen ist sie abgeschlossen.

### 1.3 Die Tabelle 9 × 2

| Bot | Intervall | Papier (`forward_test.py`) | Selektion (Snapshot-Rand) |
|---|---|---|---|
| elliott_wave | 1h | **ja** — `lade` Z.236; Entscheidung Z.175/176 | **ja** — 24 Dateien enden `09-15 08:00`, gemeinsamer Stand; kein Zeuge, Beleg Zeitstempel. `XAUTUSDT` ausgeschlossen (`shared/symbols_config.py:24`) |
| t3_supertrend | 4h | **ja** — `lade` Z.209; Z.146/147, Regime Z.225; Test Abschnitt 8 gestartet | **ja** — `rand_letzte` geprüft (Zeuge 1h), Zeitstempel |
| rsi2_crypto | 1d | **ja** — `lade` Z.245; Z.174 | **ja** — Zeuge 1h, Zeitstempel |
| turtle_soup_crypto | 1d | **ja** — `lade` Z.250; Z.171; Test Abschnitt 9 gestartet | **ja** — Zeuge 1h, Zeitstempel |
| volatility_breakout_crypto | 1d | **ja** — `lade` Z.258; Z.184/185, Regime Z.276 | **ja** — Zeuge 1h, Zeitstempel |
| elliott_wave_stocks | 1d | **ja** — `lade` Z.271; Z.208/209 | **ja** — kein Zeuge, Zeitstempel (> 8 h nach Börsenschluss) |
| rsi2_mean_reversion | 1d | **ja** — `lade` Z.256; Z.185 | **ja** — wie oben |
| turtle_soup_stocks | 1d | **ja** — `lade` Z.252; Z.173; Test Abschnitt 10 gestartet | **ja** — wie oben |
| volatility_breakout | 1d | **ja** — `lade` Z.249; Z.177/178 | **ja** — wie oben |

**Nicht eindeutig: keine Zelle.** Die Selektionsspalte stützt sich bei 175 Dateien auf Zeitstempel, nicht auf eine
Prüfung, die beim Lauf mitläuft (Frage F1-2).

### 1.4 Befunde und Randbefunde zu M1

- ⚠️ **B1 — Teilkerze im Snapshot:** `XAUTUSDT_1h.csv`, letzte Kerze `2026-08-30 18:00`, Schluss 18:59:59.999,
  geschrieben 18:39:01 UTC. Sie ist Teil des Datenstand-Hashes `d9449faf…` und damit eingefroren. Gelesen wird sie
  nicht: `XAUTUSDT` steht in `config/top25_symbols.txt` (Zeile 16), wird aber an **vier** Stellen ausgeschlossen —
  `shared/symbols_config.py::EXCLUDE_SYMBOLS` (alle Krypto-Bots), `messgroessen.py::AUSGESCHLOSSEN`,
  `faltenplan_neun.py::KRYPTO_AUSSCHLUSS`, `benchmark.py:145` (Literal). Vier Kopien derselben Menge.
- **R1 — zweite Uhr bei Elliott:** `find_new_signals` der beiden Elliott-Bots misst die Frische
  (`SIGNAL_FRESHNESS_HOURS = 48`) an `pd.Timestamp.utcnow()`, nicht an `entscheidungskerze.laufbeginn()`. Keine
  Kerzenwahl; die Abweichung ist die Laufzeit bis zu dieser Zeile, wirksam nur an der 48-h-Grenze.
- **R2 — Endgültigkeit der Aktienkerze:** Die Regel sagt, *welche* Kerze; ob yfinance um 20:15 UTC schon den
  endgültigen Schlusskurs liefert (Schlussauktion, spätere Korrekturen), misst sie nicht. Nicht gemessen.

---

## 2. M2 — Adjustierung und Herkunft der Aktienreihen; Preisniveaus je Bot

### 2.1 (a) Herkunft (`m2_adjustierung.txt`, Git)

| Frage | Messung |
|---|---|
| Wie viele `_1d.csv` sind Aktien? | **174** `_1d.csv`, davon **24** Krypto (`…USDT`), **150** Aktien; Menge gleich `config/sp500_top150.txt` des Snapshots (150 Zeilen, bytegleich mit der Repo-Datei) |
| Quelle | **yfinance** |
| Aufruf, am Stand der Dateien | Die Dateien sind **vor dem ersten Commit** geschrieben: mtime 02.09.2026 04:20:40–04:22:43 UTC, Initial-Commit `0f6491b` 02.09.2026 21:12 UTC, seither **unverändert** (`git log -- data/AAPL_1d.csv` = nur `0f6491b`; Snapshot-Kopien bytegleich, `260fce65…`). Der nächstliegende versionierte Abrufcode ist `0f6491b:strategies/elliott_wave_stocks/fetch_stock_data.py` (damals die einzige `fetch_stock_data.py`): `yf.download(ticker, period="max", interval="1d", progress=False, auto_adjust=True)`, danach Umbenennung auf `open_time,open,high,low,close,volume`. **`actions` und `back_adjust` nicht gesetzt** (Vorgabe `False`). Heute tragen die vier `fetch_stock_data.py` (md5 gleich) denselben Aufruf, dazu seit TB-35 Teilkerzenfilter und Streichen leerer Kerzen |
| yfinance-Fassung beim Abruf | **nicht belegbar.** Heute `requirements.lock` und `trading-env` 1.2.0; der Lock entstand später (TB-58) |

⚠️ Der Code, der die Dateien tatsächlich geschrieben hat, ist **nicht versioniert** — `0f6491b` ist der nächstliegende
Stand, 17 Stunden später. Dass er derselbe war, folgt aus dem Schema der Dateien, nicht aus dem Git.

### 2.2 (b) Adjustierungsstand

- **Spalten:** alle 150 (und alle 223 Kursdateien) `open_time,open,high,low,close,volume`. **Kein `Adj Close`.** Mit
  `auto_adjust=True` ist `close` selbst der bereinigte Kurs; `open/high/low` sind mit demselben Faktor skaliert.
- **Splits** (öffentlich bekannte Split-Tage als Literal im Skript, nicht aus dem Repo): Quotient Schluss am Split-Tag /
  Schluss am Vortag — AAPL 4:1 `1,034`, NVDA 10:1 `1,008`, TSLA 3:1 `0,997`, AMZN 20:1 `1,020`, GOOGL 20:1 `0,975`,
  WMT 3:1 `1,019`, AVGO 10:1 `1,008`, BRK-B 50:1 `1,046`. Unbereinigt wäre er `1/Faktor` (0,25 … 0,02). **8/8
  split-bereinigt.**
- **Dividenden** — aus den Spalten nicht direkt ablesbar, deshalb über die Zahldarstellung: yfinance liefert float32;
  ein **unbereinigter** Kurs ist `float32(zweistelliger Dezimalwert)` („sauber"), ein mit einem Faktor multiplizierter
  nicht. Die letzte unsaubere Zeile markiert den letzten Bereinigungsschnitt. Gemessen: 149 von 150 Dateien haben einen
  Schnitt, danach 149/149 zu 100 % sauber, davor 1,45 % sauber (Zufallstreffer). **Monat des letzten Schnitts:
  Juni 2026 50, Juli 31, August 46, September 1** — das Quartalsmuster der Ex-Dividenden-Tage. Der eine
  September-Fall ist ABNB, dessen **letzte** Zeile (`2026-09-01`, `182.545`) drei Nachkommastellen trägt — kein
  Bereinigungsschnitt (ABNB zahlt keine Dividende), sondern ein unrunder letzter Kurs. Nichtzahler zeigen den
  Schnitt am letzten Split (TSLA `2022-08-24`, AMZN `2022-06-02`) oder gar keinen (UBER). ⇒ **dividendenbereinigt**,
  rückwärts, Stand 02.09.2026. Das deckt sich mit Register 15.7 (*„wird bei jeder Dividendenzahlung zu Recht neu
  skaliert"*) und T35.4 (Abweichungen *„ausschliesslich vor dem letzten Ex-Dividenden-Tag"*).

### 2.3 (c) Preisniveaus je Bot (`m2c_preisniveaus.py` → `.txt`)

Gesucht in `forward_test`, `backtest_*`, `indicators`, `zigzag_indicator`, `elliott_wave_counter`,
`equity_simulation`, `multi_symbol_optimise`, `live_params` der vier Aktien-Bots: P1 Vergleich Preis/Volumen gegen ein
Zahl-Literal, P2 Preis ± Literal, P3 `int/round/floor/ceil` bzw. `//` auf einem Preis, P4 Preis × ÷ Literal, P5 im
Papierpfad ein abgelegtes Niveau gegen eine spätere Kerze. 47 Fundstellen, alle gelesen:

| Muster | Fundstellen | Einordnung |
|---|---|---|
| **P1** feste Schwelle, Mindestpreis, runde Zahl | **0** | — |
| P2 | Stopps `entry_price * (1 - PCT / 100)` (8×), Indexrechnung `i = exit_idx + 1` (3×) | relativ bzw. kein Preis |
| P3 | `int(wave["entry_idx"])`, `int((open_time < cutoff).sum())`, `round(rsi, 2)` | Index bzw. RSI, kein Preis |
| P4 | `pnl_pct`, Zigzag-Ausschlag in %, `win_rate` | relativ |
| P5 | elliott_wave_stocks Z.135/140 (dazu gleichbauend, vom Muster nicht erfasst: volatility_breakout, rsi2_mean_reversion, turtle_soup_stocks über `stop_price = trade["stop_price"]`) | siehe Randbefund R3 |

Alle Regeln sind relativ: Stopps in Prozent vom Einstieg, RSI(2), SMA-Vergleiche, Donchian-Tief gegen Tagestief,
Bollinger-Breite normiert auf das Mittelband, Squeeze-Perzentil, Volumen als Vielfaches des 20-Tage-Mittels,
Zigzag-Schwelle in Prozent, Fibonacci-Verhältnisse. `live_params.py` der vier Bots: nur Prozente, Perioden, Anzahlen.
Die Positionsgrösse ist `ALLOCATION_PCT` des Kapitals, keine Stückzahl aus dem Preis. **Eine Rückwärts-Adjustierung
mit einem gemeinsamen Faktor ändert keine Regel-Entscheidung eines Bots**; über einen Ex-Tag hinweg ändert sie die
Reihe so, wie Bereinigung es soll (die Dividendenlücke fehlt). Die eine Stelle, an der ein Niveau über Symbole hinweg
verglichen wird, liegt nicht im Bot, sondern in der gemeinsamen Zuteilung (B2).

- ⚠️ **B2 — Zuteilungskaskade, Stufe 3 (Selektionspfad, alle vier Aktien-Bots):** `shared/zuteilung.py` (Sperrlistenpunkt
  10) entscheidet unter gleichzeitigen Kandidaten in vier Stufen; Stufe 3 ist *„Liquiditaet - Median des
  Dollar-Volumens der letzten 20 Handelstage. Hoeher zuerst"* (Z. 43), gebildet als `umsatz = (close * menge)` (Z. 273)
  und verglichen **über Symbole hinweg** (`waehle`, Z. 568 ff.). Das ist ein Niveau in Währung. Gemessen am Snapshot
  (`m2c_zuteilung.txt`): das Volumen ist **split**-bereinigt (kein Sprung um den Split-Faktor an den Split-Tagen von
  AAPL, TSLA, NVDA), `close * volume` ist also split-invariant. Die
  **Dividenden**bereinigung skaliert dagegen nur `close` rückwärts, je Symbol mit dem Produkt seiner späteren
  Ausschüttungen — das Dollar-Volumen eines Zahlers ist in der Vergangenheit kleiner ausgewiesen als gehandelt, das
  eines Nichtzahlers nicht. Stufe 3 entscheidet, wenn Stufe 1 und 2 nicht trennen: `SIGNALSPALTE = None` bei
  `volatility_breakout`, `elliott_wave_stocks`, `turtle_soup_stocks` (Stufe 1 entfällt), und bei leerem Buch entfällt
  Stufe 2 (Z. 41, Z. 558). `rsi2_mean_reversion` hat Stufe 1 (`rsi_at_entry`). Wie oft Stufe 3 tatsächlich entscheidet,
  wäre eine Messung auf dem Selektionsraum — **nicht gemessen** (Sichtschutz 27.1). Krypto ist nicht betroffen
  (Binance-Kurse sind unbereinigt). **Nur benannt, nicht bewertet.**
- **R3 — Papierpfad, abgelegte Niveaus:** `forward_test.py` legt `entry_price` und `stop_price` (Elliott auch
  `target_price`) als **absolute** Zahlen in der Datenbank ab und vergleicht sie in späteren Läufen gegen eine **neu
  abgerufene** Reihe. Seit `data/` für Aktien auf dem 01.09. steht, fällt jeder Aktienlauf auf den Live-Abruf zurück
  (`auto_adjust=True`). Liegt ein Ex-Tag oder Split in einer offenen Position, sind die Kerzen **vor** dem Ex-Tag in der
  neuen Reihe herunterskaliert, das abgelegte Niveau nicht. Aktiv betroffen sind die Bots mit Stop:
  `volatility_breakout` (8 %) und `elliott_wave_stocks` (3 %; Ziel nur bei `USE_TAKE_PROFIT`, heute aus); dazu bei allen
  vier `pnl_pct` aus abgelegtem Einstieg und neuem Ausstieg. Der Selektionspfad ist davon frei (ein Rahmen, ein
  Faktor). **Nur benannt, nicht bewertet.**

### 2.4 Folge, nur benannt

Der Adjustierungsstand der Aktienreihen im Snapshot (split- und dividendenbereinigt, rückwärts, Schnitt je Symbol am
letzten Ex-Tag vor dem 02.09.2026; Abrufcode nicht versioniert, nächstliegend `0f6491b`; yfinance-Fassung nicht belegbar)
steht **nirgends als Tatsache des Snapshots**. Er wirkt an genau einer Stelle auf eine Entscheidung, die Stufe 3 der Zuteilungskaskade (B2). Register 15.7/17.x nennen `auto_adjust=True` als Eigenschaft des
**Abrufs** und als Grund für den Snapshot, nicht als Eigenschaft **dieser** 150 Dateien; `MANIFEST.json` führt keine
Adjustierung. Ob das als Tatsachennotiz neben 5e gehört: **Frage an Fable (F2-1).**

---

## 3. M3 — Deckt die Sperrlisten-Sonde die Kette Erzeuger → Auswertung?

### 3.1 Was die Sonde tatsächlich prüft (`shared/sperrlistensonde.py`, Abbild `5e5ad109…`)

| Teil | Gegenstand | Wie |
|---|---|---|
| (i) Punkte | 14 Punkte aus Abschnitt 10, **11 verschiedene Pfade** | SHA-256 der Datei gegen den Hash **im Abbild**; Punkt mit Nicht-Dateibezogenem ⇒ 2 (Punkte 1, 3, 4, 6–14) |
| (ii) Register | Abbild gegen den Listentext von Abschnitt 10 | Punktzahl, Titel, Pfade, Wortlaut — **nicht** die Hashes der Dateien |
| Gruppe `bestimmt` | 0 Einträge | Hash gegen Abbild |
| Gruppe `eingefroren` | 19 Einträge | Hash gegen Abbild; **die Liste kommt aus dem Abbild**, nicht aus `herkunft.py::EINGEFROREN` von heute (`_pruefe_gruppe`, Z. 418–463). Heute sind beide gleich (19 = 19); ein Zuwachs in `EINGEFROREN` erscheint erst mit einem neuen Abbild (TB-114 C) |

Die Sonde kennt **keine** Pfade unter `snapshots/`, `strategies/` oder `shared/` ausser `shared/zuteilung.py` (Punkt 10).

### 3.2 Die Kette am Tag — Glied × Bindung (`m3_kette.py` → `.txt`)

Spalten: **S** Sperrlistenpunkt (über das Abbild), **A** Abbild-Gruppe `eingefroren`, **E** `EINGEFROREN` heute,
**W** `ARBEITSBAUM_PFADE` (Sauberkeit unter dem Modus, Startprüfung), **SP** sonstige Startprüfung, **G** versioniert.

| Glied | Datei | S | A | E | W | SP | G | Bindung zusammengefasst |
|---|---|---|---|---|---|---|---|---|
| **1 Snapshot** | `snapshots/63e4…/` (223 Kursdateien, `config/`, `MANIFEST.json`) | – | – | – | – | **ja**, eingeschränkt | ja | Startprüfung: `TB_SELEKTIONSHASH` gegen `snapshot_hash` **aus dem MANIFEST gelesen** (`paths._lies_snapshot_hash`, kein Hash über Dateien; T1); `_pruefe_universum` prüft nur Vorhandensein/nicht leer. Punkt 12 nennt den Datenstand als `herkunft.py::datenstand()` ⇒ nicht dateibezogen, Sonde 2. `snapshot.py --pruefen` rechnet nach (heute UNVERAENDERT, rc 0), läuft aber in keiner Wache mit |
| | `config/top25_symbols.txt`, `config/sp500_top150.txt` (Repo) | 8 | – | – | – | – | ja | Sperrliste bindet die **Repo**-Dateien; unter dem Modus liest der Lauf die **Snapshot**-Kopien. Heute bytegleich (`3afc95a4…`, `6acba892…`) |
| **2 Erzeuger** | nicht gebaut (41.1 A12, 45.10 (2)); Pfad nicht registriert (TB-114 B3) | – | – | – | – | – | – | keine. Sein Unterbau: `strategies/*` und `shared/paths.py` W + Commit-Prüfung (`TB_SELEKTIONSCOMMIT`); `faltenplan.py`, `registerdaten.py` S+A+E+W; `faltenplan.json` S+A+E; `zuteilung.py` S (10) + W |
| **3 `zellen.csv`** | `<rohergebnisse>/<bot>/zellen.csv`, dazu `tagesreihen/<zelle>.csv`, `herkunft.json`, `benchmark_tagesreihen/<markt>.csv` | – | – | – | – | – | – | keine; kein fester Pfad (`--rohergebnisse`). Einzige Wache: der Vertrag in `auswertung.py` (Pflichtspalten, fehlende Falte/Zelle/Tagesreihe ⇒ 2) |
| **4 `auswertung.py`** | `research/vorregistrierung/auswertung.py` | 3, 5, 14 | ja | ja | ja | – | ja | **gebunden** (Punkte 3/14 als Ganzes 2, weil nicht dateibezogen; der Datei-Hash ist geprüft) |
| | Importe `kennzahlen.py` · `benchmark.py` · `faltenplan.py` · `registerdaten.py` | –/4,6/2/1 | ja | ja | ja | – | ja | gebunden |
| | gelesen: `ergebnisse/messgroessen.json` (über `registerdaten._mess`) | – | ja | ja | – | – | ja | gebunden (A/E) |
| | gelesen: `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` | 4 | – | – | – | – | ja | gebunden (S) |
| | Import `shared/paths.py` (nur `RUECKGABEWERT_STARTPRUEFUNG`) | – | – | – | ja | – | ja | W |
| **5 Bericht** | Standardausgabe von `auswertung.py`, optional `--json PFAD` | – | – | – | – | – | – | keine; kein fester Pfad. `registerbericht.py` ist der Registerblock, nicht dieser Bericht |

⚠️ **T2 — `herkunft.json` wird nicht gelesen.** `auswertung.py` nennt `<wurzel>/<bot>/herkunft.json` (*„Commit-Hash,
Datenstand-Hash, Register-Hash"*) im Modul-Docstring als Teil des Vertrags (Z. 51–52); ausserhalb des Docstrings kommt
`herkunft` weder als String noch als Name vor. Die Rohergebnisse werden also nicht gegen Snapshot, Commit oder Register
geprüft, und der Bericht trägt keine Herkunft. `beispieldaten.py:210` schreibt die Datei für die Tests.

### 3.3 Lücken je Glied — und wann

Das Kriterium des Auftrags: **vor dem Tag**, wenn der Tag-Commit die Lücke sonst mit einfriert; **mit dem Erzeuger
(R5)**, wenn sie erst mit ihm entsteht. Eingeordnet, nicht bewertet:

| Glied | Lücke (ein Satz) | wann |
|---|---|---|
| 1 Snapshot | Der Snapshot ist an keinen Sondenpunkt gebunden, und die Startprüfung vergleicht nur den im MANIFEST **notierten** Hash, rechnet die Dateien nicht nach; dazu bindet Punkt 8 die Repo- statt der Snapshot-Universumsdateien. | **vor dem Tag** — der Snapshot steht fest (TB-55), die Bindung ginge jetzt; nach dem Tag wäre sie eine Änderung an Sperrliste oder Startprüfung |
| 2 Erzeuger | Es gibt ihn nicht; sein Pfad ist nicht registriert, er steht weder in `EINGEFROREN` noch im Abbild. | **mit dem Erzeuger (R5)** — dazu ein neues Abbild, weil die Gruppe `eingefroren` aus dem Abbild geprüft wird |
| 3 `zellen.csv` | Keine Datei-Bindung möglich (entsteht erst im Lauf); die vorgesehene Bindung über `herkunft.json` wird von `auswertung.py` nicht gelesen. | Datei: **mit dem Erzeuger**; die Prüfung in `auswertung.py`: **vor dem Tag**, weil `auswertung.py` eingefroren ist (Punkte 3/5/14, `EINGEFROREN`) |
| 4 `auswertung.py` | Keine Lücke; nur die Grenze aus 3.1: Punkte 3/14 bleiben 2 (nicht dateibezogen), die Datei selbst ist gehasht. | — |
| 5 Bericht | Kein fester Pfad und keine Herkunft im Bericht (folgt aus T2). | wie Glied 3 |

---

## 4. Abschluss — 0b wiederholt

`0b_ausgang.sh` am Ende (`0b_nachher.txt`, 20:06), vor dem Abgabe-Commit; `diff` gegen `0b_ausgang.txt` ohne die
Kopfzeile leer: **`register()` `5acb4c19…` = vorher; Sonde 34/0/0,
(ii) 0, rc 2 = vorher; Abbild `5e5ad109…` = vorher; Arbeitsbaum ausserhalb `docs/` leer.** Die Sitzung hat nichts
ausserhalb von `docs/belege/TB-115/`, dem Journal und diesem Dokument verändert. Der Wegwerfklon liegt im Scratchpad.

---

## 5. Für Fable

**M1**
- **F1-1** `XAUTUSDT_1h.csv` ist eine Datei mit Teilkerze im eingefrorenen Datenstand `d9449faf…`. Folgenlos, solange
  **jede** der vier Ausschlusslisten das Symbol streicht. Reicht das, oder gehört die Tatsache (Datei, Kerze,
  Schreibzeit) als Tatsachennotiz zum Snapshot — und die vier Kopien von `{"XAUTUSDT", "PAXGUSDT"}` auf eine?
- **F1-2** Für 175 Dateien ohne feineren Zeugen (150 Aktien, 25 Krypto-1h) ist „letzte Kerze abgeschlossen" nur durch
  Schreibpfad und Zeitstempel belegt; `snapshot.py` prüft `rand_letzte` dort nicht. Genügt der Zeitstempel-Beleg dieser
  Sitzung als Vorbedingung des Tags, oder soll die Prüfung ihn führen?
- **F1-3** R1: Die Elliott-Frische an der Wanduhr statt an `laufbeginn()` — Handwerk bei der nächsten Öffnung, oder
  gleichgültig?

**M2**
- **F2-1** Gehört der Adjustierungsstand (split- und dividendenbereinigt, rückwärts, Stand 02.09.2026; Abrufcode
  unversioniert, nächstliegend `0f6491b`; yfinance-Fassung unbekannt) als Tatsachennotiz neben 5e?
- **F2-3** B2: Stufe 3 der Zuteilungskaskade vergleicht dividendenbereinigtes Dollar-Volumen über Symbole. `zuteilung.py`
  steht auf der Sperrliste (Punkt 10). Ist das eine Eigenschaft, die als Tatsachennotiz neben Punkt 10 und 5e steht,
  oder ein Grund, Stufe 3 vor dem Tag anders zu fassen (etwa mit unbereinigtem Kurs oder Stückzahl × Split-Faktor)?
- **F2-2** R3 (Papierpfad, abgelegte absolute Niveaus gegen neu bereinigte Reihen) berührt den Live-Record, der die
  einzige Out-of-Sample-Evidenz ist, nicht die Selektion. Ein Registerthema oder ein Backlog-Punkt?

**M3**
- **F3-1** Snapshot-Bindung: Soll die Startprüfung den Snapshot nachrechnen (wie `snapshot.py --pruefen`), soll das
  Abbild den MANIFEST-Hash führen, oder beides — und vor dem Tag?
- **F3-2** Punkt 8 bindet `config/*.txt` im Repo; gelesen werden unter dem Modus die Kopien im Snapshot. Soll Punkt 8
  (oder das Abbild) die Snapshot-Kopien nennen?
- **F3-3** `auswertung.py` liest `herkunft.json` nicht, ist aber eingefroren. Ist die Prüfung der Herkunft der
  Rohergebnisse Sache von `auswertung.py` (dann Öffnung vor dem Tag), des Erzeugers oder einer eigenen Stufe zwischen
  beiden?

---

## 6. In einfacher Sprache

Drei Prüfungen, nichts geändert.

**Erstens, fertige Kerzen:** Alle neun Bots entscheiden auf einer Kerze, die schon vorbei ist — im täglichen Betrieb,
weil jede Kursreihe durch dieselbe Tür kommt, die die laufende Kerze abschneidet, und in der Auswahlrechnung, weil die
eingefrorenen Kursdateien an ihrem Ende nur fertige Kerzen haben. Mit einer Ausnahme: Die Datei für den Gold-Token
XAUT wurde 21 Minuten zu früh geschrieben und endet auf einer halben Stunde. Kein Bot liest sie, weil das Symbol an
vier Stellen ausgeschlossen ist.

**Zweitens, Aktienkurse:** Die 150 Aktienreihen sind um Splits und Dividenden bereinigt, so wie Yahoo sie am
2. September geliefert hat. Kein Aktien-Bot rechnet in seinen Regeln mit festen Dollarbeträgen; alles ist in Prozent oder Verhältnissen. Eine
Stelle gibt es aber: Wenn mehrere Aktien am selben Tag um Kapital konkurrieren, bevorzugt die Zuteilung die mit dem
grösseren Handelsumsatz in Dollar — und diesen Umsatz rechnet die Dividendenbereinigung für die Vergangenheit bei
Dividendenzahlern etwas kleiner, als er war.
Nebenbei aufgefallen: Im täglichen Betrieb merkt sich ein Bot seinen Stopp als festen Betrag und vergleicht ihn später
mit frisch bereinigten Kursen — nach einer Dividende oder einem Split passt das nicht mehr ganz zusammen.

**Drittens, die Kette vom Rechnen bis zum Bericht:** Das Prüfwerkzeug bewacht das Auswertungsprogramm und seine
Tabellen gut. Den Datenstand, das (noch nicht gebaute) Rechenprogramm, die Zwischenergebnisse und den Bericht bewacht
es nicht. Und das Auswertungsprogramm, das schon eingefroren ist, schaut nicht nach, woher die Zahlen kommen, die es
bekommt, obwohl seine eigene Beschreibung dafür eine Datei vorsieht. Das sind die Fragen an Fable.

*Geschrieben 26.09.2026 von der Mac-Sitzung TB-115.*

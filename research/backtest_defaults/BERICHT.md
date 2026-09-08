# backtest_*.py-Defaults: nur die tatsächlich wirksamen an `live_params.py` koppeln

**Stand:** 2026-09-08 · **Branch:** `claude/backtest-defaults-sync`

---

## Kurzfassung

| | |
|---|---|
| Untersucht | alle 9 Bots, 141 Funktions-Parameter mit Default plus alle Modulkonstanten mit Gegenstück in `live_params.py` |
| Wirksam über ihren Default im Live-Pfad | 29 Parameter |
| Davon gekoppelt | **9 Konstanten in 5 Bots** |
| Neue Wertabweichung unter den wirksamen | **keine** — alle 9 stimmten bereits überein |
| Regressionscheck | 5 Bots, Ergebnis **exakt identisch** (stdout + `equity_curve.csv`-Prüfsumme) |
| Gegenprobe | Live-Wert verändert → Ergebnis ändert sich bei allen 5 Bots (die Kopplung greift wirklich) |
| `forward_test.py` / `live_params.py` | bei **keinem** Bot angefasst |

Zusätzlich: **drei Befunde, die eine eigene Entscheidung brauchen** (Abschnitt 5) — darunter ein echter
Fehler in `elliott_wave_stocks/oos_equity_simulation.py`, der beim Durchgehen des Aufrufgraphen auffiel.

---

## 1. Warum die naheliegende Analyse hier falsche Antworten gibt

Drei Fallen, an denen ein einfacherer Ansatz gescheitert wäre — jede davon ist im Werkzeug
und in `test_backtest_defaults.py` abgesichert:

**a) „`equity_simulation.py` ist live, `multi_symbol_optimise.py` ist Grid-Search."**
Falsch. `equity_simulation.py` importiert aus `multi_symbol_optimise.py` die Funktion
`get_trades_for_symbol()`, und **genau darin** steht der `run_backtest()`-Aufruf, der die
live gemeldeten Zahlen erzeugt. Eine Einteilung nach Dateiname hätte diesen Aufruf als
Grid-Search abgetan — und damit ausgerechnet `MAX_HOLD_DAYS` und die Squeeze-Parameter
übersehen, also die Fälle, um die es in dieser Aufgabe geht. Das Werkzeug baut deshalb einen
**Aufrufgraphen** über den ganzen Bot-Ordner und markiert von `equity_simulation.py` und
`forward_test.py` aus transitiv.

**b) „Ein Default wirkt, wenn niemand `name=` übergibt."**
Falsch. `get_trades_for_symbol(df, entry_cutoff, stop_loss_pct, max_hold_days, use_volume_filter)`
übergibt fünf Parameter **positionell**. Eine Textsuche nach `max_hold_days=` findet davon
nichts. Das Werkzeug zählt deshalb Positions-Argumente mit.

**c) „Nur Funktions-Defaults sind relevant."**
Falsch. `rsi2_mean_reversion/backtest_rsi2.py` liest `MAX_HOLD_DAYS` **direkt im Rumpf** von
`run_backtest()` — der Wert ist dort nie Parameter. Ein reiner Default-Scan meldet hier nichts,
obwohl die Zahl die Trades bestimmt. Dieser 9. Fall kam erst durch den zusätzlichen
`konstanten_scan.py` ans Licht.

Und der Gegenpol dazu: bei **beiden Elliott-Bots** sehen `STOP_LOSS_PCT` und `TAKE_PROFIT_FIB`
nach dramatischer Abweichung aus (0.382 gegen live 0.236 bzw. 0.618), sind aber folgenlos —
`equity_simulation.py` überschreibt sie zur Laufzeit von außen
(`backtest_elliott.TAKE_PROFIT_FIB = take_profit_fib`). Wer nur Zahlen vergleicht, meldet hier
einen Fehlalarm; das Werkzeug sucht deshalb auch nach solchen Zuweisungen.

---

## 2. Was umgestellt wurde (9 Konstanten, 5 Bots)

Alle neun wirken tatsächlich über ihren Default bzw. direkten Lesezugriff, werden von **keinem**
Optimierungs-Skript variiert, und ihr Wert stimmte bereits mit `live_params.py` überein.

| Bot | Modul | Konstante | Wert | kommt jetzt aus | Wirkungsweg |
|---|---|---|---|---|---|
| `rsi2_mean_reversion` | `backtest_rsi2.py` | `MAX_HOLD_DAYS` | 10 | `live_params.MAX_HOLD_DAYS` | direkt im Rumpf von `run_backtest()` gelesen |
| `turtle_soup_crypto` | `backtest_turtle_soup.py` | `MAX_HOLD_DAYS` | 10 | `live_params.MAX_HOLD_DAYS` | Default von `run_backtest()` |
| `turtle_soup_stocks` | `backtest_turtle_soup.py` | `MAX_HOLD_DAYS` | 10 | `live_params.MAX_HOLD_DAYS` | Default von `run_backtest()` |
| `volatility_breakout` | `backtest_breakout.py` | `MAX_HOLD_DAYS` | 15 | `live_params.MAX_HOLD_DAYS` | Default von `run_backtest()` |
| `volatility_breakout` | `backtest_breakout.py` | `SQUEEZE_LOOKBACK_DAYS` | 126 | `live_params.BB_LOOKBACK` | Default von `compute_indicators()` |
| `volatility_breakout` | `backtest_breakout.py` | `SQUEEZE_PERCENTILE` | 25.0 | `live_params.BB_SQUEEZE_PERCENTILE` | Default von `compute_indicators()` |
| `volatility_breakout_crypto` | `backtest_breakout.py` | `MAX_HOLD_DAYS` | 15 | `live_params.MAX_HOLD_DAYS` | Default von `run_backtest()` |
| `volatility_breakout_crypto` | `backtest_breakout.py` | `SQUEEZE_LOOKBACK_DAYS` | 126 | `live_params.BB_LOOKBACK` | Default von `compute_indicators()` |
| `volatility_breakout_crypto` | `backtest_breakout.py` | `SQUEEZE_PERCENTILE` | 25.0 | `live_params.BB_SQUEEZE_PERCENTILE` | Default von `compute_indicators()` |

**Namensunterschied:** die beiden Squeeze-Größen heißen in `live_params.py` `BB_LOOKBACK` und
`BB_SQUEEZE_PERCENTILE`. Der Import benennt sie per Alias um, damit die übrigen
Verwendungsstellen im Modul unverändert bleiben. Eine Einheiten-Umrechnung war bei keiner der
neun nötig (anders als bei `ALLOCATION_PCT`, das in Prozent gegen Anteil steht).

### Regressionscheck

`regression.py` führt das **echte** `equity_simulation.py` je Bot in einem eigenen Prozess aus
(gleichnamige Module der 9 Bots würden sich sonst über `sys.modules` gegenseitig überschreiben)
und leitet `RESULTS_DIR`/`LOGS_DIR`/`DB_FILE` in ein temporäres Verzeichnis um — die echten
`results/`-Dateien und Datenbanken bleiben unberührt.

| Bot | Endkapital vorher | Endkapital nachher | stdout + CSV-Prüfsumme |
|---|---|---|---|
| `rsi2_mean_reversion` | 13.675,20 | 13.675,20 | identisch |
| `turtle_soup_crypto` | 27.759,42 | 27.759,42 | identisch |
| `turtle_soup_stocks` | 24.559,08 | 24.559,08 | identisch |
| `volatility_breakout` | 32.441,42 | 32.441,42 | identisch |
| `volatility_breakout_crypto` | 17.126,14 | 17.126,14 | identisch |

### Gegenprobe: greift die Kopplung überhaupt?

„Identisch" allein beweist wenig — dasselbe Ergebnis käme heraus, wenn die Kopplung gar nicht
griffe. `kopplungsnachweis.py` verringert deshalb `live_params.MAX_HOLD_DAYS` im Testprozess um
eins (nur im Speicher, die Datei bleibt unangetastet) und prüft, dass sich das Ergebnis ändert:

| Bot | `MAX_HOLD_DAYS` | Endkapital regulär | Endkapital mit −1 |
|---|---|---|---|
| `rsi2_mean_reversion` | 10 → 9 | 13.675,20 | 13.804,11 |
| `turtle_soup_crypto` | 10 → 9 | 27.759,42 | 23.260,28 |
| `turtle_soup_stocks` | 10 → 9 | 24.559,08 | 19.269,21 |
| `volatility_breakout` | 15 → 14 | 32.441,42 | 23.024,71 |
| `volatility_breakout_crypto` | 15 → 14 | 17.126,14 | 16.293,57 |

Beides zusammen ist der Beweis: Live-Wert unverändert → Ergebnis unverändert; Live-Wert
verändert → Ergebnis verändert.

---

## 3. Was bewusst NICHT gekoppelt wurde

Jeder dieser Fälle hat jetzt einen Kommentar im Code, damit ein späterer Blick ihn nicht für
eine übersehene Sync-Lücke hält.

### a) Von Optimierungs-Skripten absichtlich variiert

| Bot | Konstante | Wert dort | live | variiert von |
|---|---|---|---|---|
| `turtle_soup_crypto` / `_stocks` | `DONCHIAN_PERIOD` | 20 | 10 | `DONCHIAN_PERIOD_RANGE = [10, 20, 40]` |
| `t3_supertrend` | `T3_FAST_LENGTH` | 12 | 16 | Suchraster `multi_symbol_optimise.py` |
| `t3_supertrend` | `T3_SLOW_LENGTH` | 25 | 30 | dito |
| `t3_supertrend` | `ADX_THRESHOLD` | 25.0 | 20.0 | dito |
| `t3_supertrend` | `STOP_LOSS_PCT` | 3.0 | 4.0 | dito |
| `volatility_breakout` | `stop_loss_pct` (Literal) | 5.0 | 8.0 | `STOP_LOSS_RANGE = [3.0, 5.0, 8.0, None]` |
| `volatility_breakout_crypto` | `stop_loss_pct` (Literal) | 8.0 | 5.0 | dito |

Alle sieben werden im Live-Pfad ohnehin explizit übergeben — der Default wird nie wirksam. Die
Zahlen sind Startwerte des Suchrasters, nicht die Live-Einstellung.

> Nebenbei aufgefallen: die beiden Breakout-Bots haben ihre `stop_loss_pct`-Startwerte **über
> Kreuz** (Aktien 5.0 bei live 8.0, Krypto 8.0 bei live 5.0). Das sieht nach einem
> Copy-Paste-Dreher aus, ist aber folgenlos, weil beide Werte immer überschrieben werden. Nicht
> angefasst, nur kommentiert.

### b) Zur Laufzeit von außen überschrieben (Monkey Patching)

`elliott_wave` und `elliott_wave_stocks`: `STOP_LOSS_PCT` und `TAKE_PROFIT_FIB` werden von
`equity_simulation.py`, `multi_symbol_optimise.py` und `optimise_elliott.py` per
`backtest_elliott.KONSTANTE = ...` gesetzt. Ein Import würde daran nichts ändern und nur den
Eindruck erwecken, die Zuweisung von außen sei entfallen.

### c) Kein Gegenstück in `live_params.py`

Diese wirken tatsächlich über ihren Default, es gibt aber schlicht nichts, woran man sie koppeln
könnte — siehe Abschnitt 5, Punkt 2.

---

## 4. Korrigierte Docstring-Aussagen

In `volatility_breakout/backtest_breakout.py` stand: *„SQUEEZE_LOOKBACK_DAYS und
SQUEEZE_PERCENTILE sind Parameter, Startwerte 126 / 25 — werden in `multi_symbol_optimise.py`
testweise variiert."* Das trifft **nicht** zu: das dortige Raster variiert ausschließlich
`STOP_LOSS_RANGE`. Die Aussage ist korrigiert; analog die „Startwert"-Formulierungen zu
`MAX_HOLD_DAYS` und `stop_loss_pct` in beiden Breakout-Bots.

---

## 5. NEU ENTDECKT — braucht eine eigene Entscheidung

Keiner dieser drei Punkte ist in dieser Änderung angefasst worden.

### 5.1 `elliott_wave_stocks/oos_equity_simulation.py` verwirft `use_take_profit` — vermutlich ein Fehler

Das Skript optimiert auf dem In-Sample-Zeitraum und rechnet die Kapitalsimulation dann mit dem
Gewinner. Dabei übernimmt es `deviation_pct`, `stop_loss_pct` und `take_profit_fib` — aber
**nicht** `best["use_take_profit"]`, obwohl das Suchraster genau über diese Dimension optimiert
(`multi_symbol_optimise.py:181`) und der Wert im Ergebnis steht (`:154`).

Folge: die Out-of-Sample-Prüfung läuft **immer mit** Take-Profit (Default `True`), während der
Live-Bot seit dem 2026-09-03 bewusst **ohne** läuft (`USE_TAKE_PROFIT = False`). Die OOS-Zahlen
dieses Bots validieren damit eine andere Strategie als die, die läuft.

Zum Vergleich: `multi_symbol_walk_forward.py:78` reicht den Wert korrekt durch. Der Krypto-Elliott-Bot
ist nicht betroffen — er kennt die `use_take_profit`-Dimension gar nicht.

**Vorschlag** (nicht ausgeführt): in `oos_equity_simulation.py` ein
`use_take_profit=best["use_take_profit"]` ergänzen, analog zum Walk-Forward-Skript. Das ändert
die OOS-Zahlen dieses Bots und gehört deshalb in einen eigenen PR mit Vorher/Nachher-Vergleich.

### 5.2 Wirksame Parameter ohne Eintrag in `live_params.py`

Diese bestimmen den Live-Backtest, tauchen aber in der Live-Konfiguration nicht auf — es gibt
also keine einzige Datei, in der der Anwender sie sehen oder ändern würde:

| Bot | Modul | Konstante | Wert |
|---|---|---|---|
| `t3_supertrend` | `backtest_trend.py` | `T3_FACTOR` | 0.7 |
| `t3_supertrend` | `backtest_trend.py` | `DI_LENGTH` | 14 |
| `t3_supertrend` | `backtest_trend.py` | `ADX_LENGTH` | 14 |
| `t3_supertrend` | `backtest_trend.py` | `ATR_LENGTH` | 22 |
| `t3_supertrend` | `backtest_trend.py` | `ATR_MULT` | 3.0 |
| `t3_supertrend` | `backtest_trend.py` | `use_t3_exit` / `use_vwap_filter` | True / False |
| `t3_supertrend` | `regime_filter.py` | `atr_length` / `atr_mult` | 22 / 3.0 (Literale) |
| `volatility_breakout` / `_crypto` | `backtest_breakout.py` | `VOLUME_FILTER_MULTIPLIER` | 1.5 |
| `volatility_breakout_crypto` | `regime_filter.py` | `BTC_ATR_LENGTH` / `BTC_ATR_MULT` | 22 / 3.0 |

**Frage an den Nutzer:** sollen diese in `live_params.py` aufgenommen werden (dann wären sie
sichtbar und zentral änderbar), oder bleiben sie bewusst Implementierungsdetail? Eine Aufnahme
in `live_params.py` ist eine Änderung an genau der Datei, die diese Aufgabe nicht anfassen darf —
deshalb nur vorgelegt.

### 5.3 `rsi2_crypto`: `MAX_HOLD_DAYS` steht zweimal da, ohne Live-Quelle

`MAX_HOLD_DAYS = 10` steht in `backtest_rsi2.py:49` **und** in `forward_test.py:50` — als zwei
unabhängige Zahlen. `live_params.py` dieses Bots führt `MAX_HOLD_DAYS` gar nicht. Damit ist es der
einzige der drei Zeit-Exit-Bots ohne gemeinsame Quelle: bei `rsi2_mean_reversion`,
`turtle_soup_*` und `volatility_breakout*` liest `forward_test.py` den Wert aus `live_params.py`.

Nicht behoben, weil die Lösung `MAX_HOLD_DAYS` in `live_params.py` aufnehmen und `forward_test.py`
darauf umstellen hieße — beides ausdrücklich außerhalb dieser Aufgabe.

---

## 6. Prüfungen

| Prüfung | Ergebnis |
|---|---|
| `python3 test_backtest_defaults.py` | 59/59 bestanden |
| `py_compile` aller geänderten Dateien | fehlerfrei |
| `regression.py nachher` | 5/5 identisch |
| `kopplungsnachweis.py` | 5/5 reagieren |
| `git diff` auf `forward_test.py` / `live_params.py` | keine Treffer bei keinem der 9 Bots |

Die Selbsttests decken auch das Werkzeug selbst ab: dass ein Positions-Argument als
Überschreibung zählt, ein Aufruf im Kommentar nicht, der Live-Pfad transitiv erkannt wird,
`**kwargs` als *unentscheidbar* gemeldet statt stillschweigend entschieden wird, und dass ein
Default in der Signatur nicht als Rumpf-Lesezugriff durchgeht.

### Eine Stelle, die statisch nicht entscheidbar ist

Beide Breakout-Bots rufen `run_backtest(..., **kwargs)` auf, wobei `kwargs` genau dann
`max_hold_days` enthält, wenn der Aufrufer einen Wert ungleich `None` übergeben hat. Das Werkzeug
meldet das als unklar statt zu raten. **Von Hand aufgelöst:** `equity_simulation.py` ruft
`collect_all_trades(all_data, STOP_LOSS_PCT)` ohne `max_hold_days` auf → `kwargs` bleibt leer →
der Default aus `backtest_breakout.py` wirkt. Genau deshalb ist er ein Kopplungs-Kandidat.

---

## 7. Dateien

| Datei | Zweck |
|---|---|
| `default_scan.py` | Aufrufgraph + Funktions-Defaults je Bot |
| `konstanten_scan.py` | Modulkonstanten, die im Rumpf gelesen werden, inkl. Monkey-Patch-Erkennung |
| `kandidaten.py` | Bewertung: Kandidat / Abweichung / variiert / kein Gegenstück |
| `regression.py` | Vorher/Nachher-Lauf der echten `equity_simulation.py` |
| `kopplungsnachweis.py` | Gegenprobe, dass die Kopplung wirklich greift |
| `test_backtest_defaults.py` | Selbsttests (Werkzeug + Ergebnis im Repo) |
| `results/bestandsaufnahme.md` | vollständige Tabelle aller 141 Funktions-Parameter |
| `results/*.json` | Rohdaten der Läufe |

---

## 8. Vollständige Bestandsaufnahme (Auszug: alle `backtest_*.py` plus alles, was live über den Default wirkt)

Die komplette Tabelle über alle 141 Parameter steht in `results/bestandsaufnahme.md`.

*Zur Spalte „von Optimierung variiert": `DONCHIAN_PERIOD` und `stop_mode` der Turtle-Soup-Bots
stehen dort auf „nein", obwohl das Raster sie variiert. Grund: die Übergabe erfolgt in
`get_trades_for_symbol()`, und diese Funktion gehört gleichzeitig zum Live-Pfad — die Spalte
„im Live-Pfad überschrieben" ist bei ihnen deshalb „ja". Für die Entscheidung zählt ohnehin nur,
ob ein Default im Live-Pfad wirkt.*

| Bot | Modul | Funktion(Parameter) | Default | im Live-Pfad überschrieben? | wirkt über Default? | von Optimierung variiert? | Einordnung |
|---|---|---|---|---|---|---|---|
| elliott_wave_stocks | `backtest_elliott.py` | `simulate_trade(use_take_profit)` | `True` | ja | nein | nein | - |
| elliott_wave_stocks | `backtest_elliott.py` | `run_backtest(use_take_profit)` | `True` | ja | nein | nein | - |
| t3_supertrend | `backtest_trend.py` | `run_backtest(t3_fast_length)` | `<T3_FAST_LENGTH>` | ja | nein | ja | - |
| t3_supertrend | `backtest_trend.py` | `run_backtest(t3_slow_length)` | `<T3_SLOW_LENGTH>` | ja | nein | ja | - |
| t3_supertrend | `backtest_trend.py` | `run_backtest(t3_factor)` | `<T3_FACTOR>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `backtest_trend.py` | `run_backtest(di_length)` | `<DI_LENGTH>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `backtest_trend.py` | `run_backtest(adx_length)` | `<ADX_LENGTH>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `backtest_trend.py` | `run_backtest(adx_threshold)` | `<ADX_THRESHOLD>` | ja | nein | ja | - |
| t3_supertrend | `backtest_trend.py` | `run_backtest(atr_length)` | `<ATR_LENGTH>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `backtest_trend.py` | `run_backtest(atr_mult)` | `<ATR_MULT>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `backtest_trend.py` | `run_backtest(stop_loss_pct)` | `<STOP_LOSS_PCT>` | ja | nein | ja | - |
| t3_supertrend | `backtest_trend.py` | `run_backtest(use_t3_exit)` | `True` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `backtest_trend.py` | `run_backtest(use_vwap_filter)` | `False` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `indicators.py` | `calculate_vwap_daily(bars_per_day)` | `6` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `regime_filter.py` | `compute_btc_regime(atr_length)` | `22` | nein | **ja** | nein | KEIN GEGENSTUECK |
| t3_supertrend | `regime_filter.py` | `compute_btc_regime(atr_mult)` | `3.0` | nein | **ja** | nein | KEIN GEGENSTUECK |
| rsi2_crypto | `backtest_rsi2.py` | `run_backtest(stop_loss_pct)` | `None` | ja | nein | nein | - |
| rsi2_crypto | `backtest_rsi2.py` | `run_backtest(entry_cutoff)` | `None` | ja | nein | nein | - |
| rsi2_crypto | `multi_symbol_optimise.py` | `get_trades_for_symbol(entry_cutoff)` | `None` | nein | **ja** | nein | KEIN STRATEGIEPARAMETER |
| rsi2_mean_reversion | `backtest_rsi2.py` | `run_backtest(stop_loss_pct)` | `None` | ja | nein | nein | - |
| rsi2_mean_reversion | `backtest_rsi2.py` | `run_backtest(entry_cutoff)` | `None` | ja | nein | nein | - |
| turtle_soup_crypto | `backtest_turtle_soup.py` | `compute_indicators(donchian_period)` | `<DONCHIAN_PERIOD>` | ja | nein | nein | - |
| turtle_soup_crypto | `backtest_turtle_soup.py` | `run_backtest(stop_mode)` | `None` | ja | nein | nein | - |
| turtle_soup_crypto | `backtest_turtle_soup.py` | `run_backtest(entry_cutoff)` | `None` | ja | nein | nein | - |
| turtle_soup_crypto | `backtest_turtle_soup.py` | `run_backtest(max_hold_days)` | `<MAX_HOLD_DAYS>` | nein | **ja** | nein | GEKOPPELT |
| turtle_soup_crypto | `backtest_turtle_soup.py` | `run_backtest(donchian_period)` | `<DONCHIAN_PERIOD>` | ja | nein | nein | - |
| turtle_soup_crypto | `multi_symbol_optimise.py` | `get_trades_for_symbol(entry_cutoff)` | `None` | nein | **ja** | nein | KEIN STRATEGIEPARAMETER |
| turtle_soup_stocks | `backtest_turtle_soup.py` | `compute_indicators(donchian_period)` | `<DONCHIAN_PERIOD>` | ja | nein | nein | - |
| turtle_soup_stocks | `backtest_turtle_soup.py` | `run_backtest(stop_mode)` | `None` | ja | nein | nein | - |
| turtle_soup_stocks | `backtest_turtle_soup.py` | `run_backtest(entry_cutoff)` | `None` | ja | nein | nein | - |
| turtle_soup_stocks | `backtest_turtle_soup.py` | `run_backtest(max_hold_days)` | `<MAX_HOLD_DAYS>` | nein | **ja** | nein | GEKOPPELT |
| turtle_soup_stocks | `backtest_turtle_soup.py` | `run_backtest(donchian_period)` | `<DONCHIAN_PERIOD>` | ja | nein | nein | - |
| volatility_breakout | `backtest_breakout.py` | `compute_indicators(squeeze_lookback_days)` | `<SQUEEZE_LOOKBACK_DAYS>` | nein | **ja** | nein | GEKOPPELT |
| volatility_breakout | `backtest_breakout.py` | `compute_indicators(squeeze_percentile)` | `<SQUEEZE_PERCENTILE>` | nein | **ja** | nein | GEKOPPELT |
| volatility_breakout | `backtest_breakout.py` | `run_backtest(stop_loss_pct)` | `5.0` | ja | nein | nein | - |
| volatility_breakout | `backtest_breakout.py` | `run_backtest(entry_cutoff)` | `None` | ja | nein | nein | - |
| volatility_breakout | `backtest_breakout.py` | `run_backtest(max_hold_days)` | `<MAX_HOLD_DAYS>` | nein | **ja** | nein | GEKOPPELT |
| volatility_breakout | `backtest_breakout.py` | `run_backtest(use_volume_filter)` | `False` | ja | nein | nein | - |
| volatility_breakout | `backtest_breakout.py` | `run_backtest(volume_filter_multiplier)` | `<VOLUME_FILTER_MULTIPLIER>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout | `equity_simulation.py` | `collect_all_trades(max_hold_days)` | `None` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout | `equity_simulation.py` | `collect_all_trades(use_volume_filter)` | `False` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout_crypto | `backtest_breakout.py` | `compute_indicators(squeeze_lookback_days)` | `<SQUEEZE_LOOKBACK_DAYS>` | nein | **ja** | nein | GEKOPPELT |
| volatility_breakout_crypto | `backtest_breakout.py` | `compute_indicators(squeeze_percentile)` | `<SQUEEZE_PERCENTILE>` | nein | **ja** | nein | GEKOPPELT |
| volatility_breakout_crypto | `backtest_breakout.py` | `run_backtest(stop_loss_pct)` | `8.0` | ja | nein | nein | - |
| volatility_breakout_crypto | `backtest_breakout.py` | `run_backtest(entry_cutoff)` | `None` | ja | nein | nein | - |
| volatility_breakout_crypto | `backtest_breakout.py` | `run_backtest(max_hold_days)` | `<MAX_HOLD_DAYS>` | nein | **ja** | nein | GEKOPPELT |
| volatility_breakout_crypto | `backtest_breakout.py` | `run_backtest(use_volume_filter)` | `False` | ja | nein | nein | - |
| volatility_breakout_crypto | `backtest_breakout.py` | `run_backtest(volume_filter_multiplier)` | `<VOLUME_FILTER_MULTIPLIER>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout_crypto | `equity_simulation.py` | `collect_all_trades(max_hold_days)` | `None` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout_crypto | `equity_simulation.py` | `collect_all_trades(use_volume_filter)` | `False` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout_crypto | `multi_symbol_optimise.py` | `get_trades_for_symbol(entry_cutoff)` | `None` | nein | **ja** | nein | KEIN STRATEGIEPARAMETER |
| volatility_breakout_crypto | `regime_filter.py` | `compute_btc_regime(atr_length)` | `<BTC_ATR_LENGTH>` | nein | **ja** | nein | KEIN GEGENSTUECK |
| volatility_breakout_crypto | `regime_filter.py` | `compute_btc_regime(atr_mult)` | `<BTC_ATR_MULT>` | nein | **ja** | nein | KEIN GEGENSTUECK |
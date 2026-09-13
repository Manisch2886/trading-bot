# TB-27 — Bestandsaufnahme der neun `equity_simulation.py`

**Stand: 13.09.2026.** Vorarbeit zur Mass-Reparatur. Diese Untersuchung fasst
**keinen** Bot-Code an: der Vergleich läuft rein auf dem Quelltext, es wird
nichts ausgeführt, nichts importiert und nichts überschrieben. Alles Neue liegt
unter `research/tb27_kapitalsimulation/` und `docs/`.

Anlass ist der erste Arbeitstag, den die externe Analyse für die
Mass-Reparatur vorsieht: ein `diff` über die neun `equity_simulation.py`, um zu
entscheiden, ob die Reparatur **eine** Stelle anfasst oder **neun** — und um
stille Divergenzen zu finden, bevor sie neunmal mitwandern.

---

## 1. Die Antwort zuerst

> **Innerhalb der neun `equity_simulation.py` sind es zwei Stellen, nicht neun
> — und beide sind bereits gemeinsam oder wortgleich.** Die Kapitalrechnung
> steht seit TB-26 einmal in `shared/zuteilung.py`. Das Drawdown-Mass steht
> neunmal da, aber **zeichengleich**: `calculate_max_drawdown()` ist in allen
> neun Dateien Zeichen für Zeichen dasselbe. Die Renditeformel ebenso.
>
> **Die Zahl, die eine Entscheidung trägt, entsteht aber gar nicht in diesen
> neun Dateien.** Parameter werden nach `robustness_score` ausgewählt, und der
> entsteht in `multi_symbol_optimise.py` — dort **neunmal**, plus **sechsmal**
> in den `multi_symbol_walk_forward.py`, plus **dreimal** in den älteren
> `optimise_*.py`. Eine Mass-Reparatur, die nur die neun
> `equity_simulation.py` anfasst, ändert die ausgewiesenen Zahlen und **nicht**
> die Auswahl.

Die Behauptung der Analyse — *„das Messproblem sitzt in jeder Fassung an
derselben Stelle, dem Aufruf, der aus der Trade-Liste eine Kennzahl macht"* —
ist damit **für die neun `equity_simulation.py` bestätigt** (es ist überall
dieselbe Stelle, sogar zeichengleich) und **für die Mass-Reparatur als Ganzes
zu eng gefasst**: die entscheidende Stelle liegt eine Datei weiter. Einzelheiten
in Abschnitt 4.

**Stille Divergenzen: eine mit möglicher Zahlenwirkung** (U5), dazu drei in der
Dokumentation (U6/U8, U9, U10 — die letzte ausserhalb der neun Dateien) und ein
Punkt, der aus dem Code **nicht entscheidbar** ist und deshalb als unklar
gemeldet wird (U11). Alle übrigen Unterschiede sind bot-eigen nötig.
Einzelheiten in Abschnitt 3.

---

## 2. Der vollständige Vergleich, Funktion für Funktion

### 2.1 Womit verglichen wurde

Ein `diff` über ganze Dateien war ausdrücklich nicht gefragt und wäre hier auch
wertlos: die `collect_all_trades()` haben verschiedene Signaturen, die
Kopfkommentare sind je Bot verschieden lang, die Importreihenfolge weicht ab.
`diff` meldet dann alles und damit nichts.

Verglichen wurde deshalb **je Funktion** und auf **vier Stufen**, mit
`research/tb27_kapitalsimulation/vergleich.py`:

| Stufe | Name | was gleich sein muss |
|---|---|---|
| 1 | `zeichengleich` | dieselben Zeichen, Kommentare und Umbrüche inbegriffen |
| 2 | `ohne Kommentar` | gleich nach Abzug von Kommentaren, Umbrüchen, Einrückung (Docstrings zählen noch mit) |
| 3 | **`sachlich gleich`** | gleicher AST ohne Docstrings — **nur was hier abweicht, kann das Ergebnis verändern** |
| 4 | `ohne Ausgabe` | wie 3, zusätzlich sind alle `print(...)`-Argumente durch einen Platzhalter ersetzt: rechnen sie verschieden oder reden sie nur verschieden? |

Stufe 3 ist das Mass, an dem der Bericht seine Aussagen festmacht. Vorbild ist
TB-17, das per AST belegt hat, dass an einer Stelle nur ein Docstring geändert
wurde. Stufe 4 steht bewusst **neben** Stufe 3 und nicht an ihrer Stelle: was
auf dem Bildschirm steht, war in genau diesen Dateien schon einmal falsch (der
Klammerzusatz zu den übersprungenen Trades, PR #48).

Der `if __name__ == "__main__"`-Block wird wie eine Funktion behandelt und
mitverglichen — bei diesen Dateien ist er der Ort, an dem aus der Trade-Liste
eine Zahl wird.

### 2.2 Welche Funktion kommt wo vor

```
python3 research/tb27_kapitalsimulation/vergleich.py
```

| Funktion | in wie vielen | wo nicht |
|---|---:|---|
| `collect_all_trades` | 9/9 | — |
| `simulate_portfolio` | 9/9 | — |
| `calculate_max_drawdown` | 9/9 | — |
| `__main__` | 9/9 | — |
| `apply_btc_regime_filter` | 1/9 | nur `volatility_breakout_crypto` |

Es gibt **keine** Funktion, die in einem Teil der Bots fehlt und anderswo
stillschweigend anders heisst. Die Dateien haben denselben Bauplan.

### 2.3 Das Ergebnis in einer Tabelle

| Funktion | Gruppen (Stufe 3) | Befund |
|---|---:|---|
| `calculate_max_drawdown` | **1** | alle neun **zeichengleich** |
| `simulate_portfolio` | **2** | acht **zeichengleich**; `elliott_wave` allein (kein Positionslimit-Argument) |
| `apply_btc_regime_filter` | 1 | existiert nur einmal |
| `__main__` | 8 | `turtle_soup_crypto` + `turtle_soup_stocks` zeichengleich, die übrigen sieben je für sich |
| `collect_all_trades` | **9** | jede Fassung für sich |

Die beiden Zeilen, auf die es für die Mass-Reparatur ankommt, sind damit die
freundlichsten des ganzen Befunds: **das Drawdown-Mass und die Kapitalrechnung
sind bereits einheitlich.**

### 2.4 Die neun `__main__`-Blöcke: drei Unterschiede, sonst nichts

Acht Gruppen klingen nach viel. Zieht man die Bildschirmausgabe ab (Stufe 4)
und vergleicht die verbleibenden Anweisungen gegeneinander, bleiben **genau
drei** Unterschiede übrig — reproduzierbar über den Vergleich der
normalisierten Blöcke:

1. **Die Argumentliste von `collect_all_trades(...)`** — bei jedem Bot andere
   Strategieparameter (`DEVIATION_PCT, STOP_LOSS_PCT, TAKE_PROFIT_FIB` gegen
   `T3_FAST, T3_SLOW, ADX_THRESHOLD, STOP_LOSS_PCT` gegen `DONCHIAN_PERIOD,
   STOP_MODE` …). Die beiden Turtle-Soup-Bots sind hier identisch, alle
   anderen verschieden.
2. **`elliott_wave` ruft `simulate_portfolio` ohne `MAX_CONCURRENT_POSITIONS`
   auf** — dieser Bot hat bewusst kein Positionslimit.
3. **`volatility_breakout_crypto` schiebt `apply_btc_regime_filter(...)`
   dazwischen** — die Backtest-Entsprechung dessen, was `forward_test.py` live
   tut (PR #57).

Dazu zwei reine Ausgabe-Unterschiede: die beiden Elliott-Bots drucken
zusätzlich die letzten zehn abgeschlossenen Trades, und der Klammerzusatz zu
den übersprungenen Trades lautet bei drei Bots verschieden (siehe U7/U8).

**Die Messkette selbst ist in allen neun identisch:**

```python
result = simulate_portfolio(trades, STARTING_CAPITAL, ALLOCATION_PCT, [MAX_CONCURRENT_POSITIONS,] all_data)
total_return_pct = (result["final_capital"] / STARTING_CAPITAL - 1) * 100
max_dd = calculate_max_drawdown(result["equity_curve"], STARTING_CAPITAL)
```

| Bot | Rendite-Zeile | Drawdown-Zeile |
|---|---:|---:|
| `elliott_wave` | 164 | 169 |
| `elliott_wave_stocks` | 188 | 209 |
| `rsi2_crypto` | 150 | 154 |
| `rsi2_mean_reversion` | 181 | 185 |
| `t3_supertrend` | 153 | 158 |
| `turtle_soup_crypto` | 133 | 137 |
| `turtle_soup_stocks` | 172 | 176 |
| `volatility_breakout` | 166 | 170 |
| `volatility_breakout_crypto` | 186 | 190 |

### 2.5 `collect_all_trades`: neunmal verschieden — woran genau

Neun Gruppen, aber nicht neun Willküren. Aufgeschlüsselt nach Ursache:

| Ursache | betroffen | Art |
|---|---|---|
| Signatur/Strategieparameter | alle neun | strategieeigen |
| Schleifenform `for symbol, (df, entry_cutoff) in …` statt `for symbol, price_df in …` | `rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout` | folgt der Rückgabeform von `load_all_symbol_data()` desselben Bots |
| Parameter per Modulvariable statt Argument (`backtest_elliott.STOP_LOSS_PCT = …`) | beide Elliott-Bots | folgt der Signatur von `get_trades_for_symbol()` desselben Bots |
| NaN-Kursfilter mit `melde_uebersprungene_balken()` | die vier **Aktien**-Bots | siehe U4 |
| BTC-Regimefilter im Rumpf | `t3_supertrend` | siehe U5 |
| `use_take_profit`-Durchreichung | `elliott_wave_stocks` | strategieeigen |

Auffällig ist, dass `elliott_wave_stocks` als einziger Aktien-Bot **keinen**
`entry_cutoff` führt. Der Grund liegt nicht in dieser Datei: sein
`multi_symbol_optimise.py` kappt die Historie schon **vor** der
Indikatorberechnung, während die drei anderen Aktien-Bots ausdrücklich nur den
Einstiegszeitpunkt kappen (`„KEINE Kappung auf RECENT_YEARS_ONLY vor der
Indikatorberechnung"`). Das ist ein Unterschied ausserhalb des Auftragsrahmens;
er ist unter U11 nur vermerkt, nicht bewertet.

### 2.6 Modulebene

| Grösse | Befund |
|---|---|
| `STARTING_CAPITAL` | `10_000.0`, neunmal identisch |
| `RESULTS_DIR` | `_P["RESULTS_DIR"]`, neunmal identisch |
| `SIGNALSPALTE` | siebenmal `None`, zweimal `("rsi_at_entry", AUFSTEIGEND)` — genau wie in TB-26 festgelegt |
| `ALLOCATION_PCT` | dreimal hart (`0.10` bei `elliott_wave`, `elliott_wave_stocks`, `t3_supertrend`), sechsmal `_ALLOCATION_PCT_PROZENT / 100` aus `live_params.py` — siehe U6 |
| Pfadaufbau (`_STRATEGY_DIR`, `_SHARED_DIR`, `sys.path.insert`) | neunmal identisch |
| Import von `zuteilung` | neunmal; zwei Bots holen zusätzlich `AUFSTEIGEND` (die beiden mit Primärschlüssel) |
| Import von `data_quality` | nur die vier Aktien-Bots (folgt U4) |

---

## 3. Je sachlichem Unterschied: nötig, still divergent, oder unklar

| # | Fundstelle | Einordnung |
|---|---|---|
| **U1** | `simulate_portfolio` bei `elliott_wave` ohne `max_concurrent_positions`, reicht `None` durch | **bot-spezifisch nötig.** Nicht bloss zulässig, sondern tragend: **zwölf** Stellen im Repo erkennen genau daran, welcher Bot kein Limit hat (Abschnitt 5). |
| **U2** | `collect_all_trades`: neun Signaturen, neun Aufrufe | **bot-spezifisch nötig.** Jede Strategie hat andere Parameter; `get_trades_for_symbol()` ist in jedem Bot eine andere Funktion. |
| **U3** | Schleifenform mit `entry_cutoff` bei drei Aktien-Bots | **bot-spezifisch nötig.** Folgt zwingend der Rückgabeform von `load_all_symbol_data()` desselben Bots. |
| **U4** | NaN-Kursfilter nur in den vier Aktien-Bots | **bot-spezifisch nötig — die Begründung steht aber nicht in diesen Dateien.** `shared/data_quality.py` sagt es ausdrücklich: „Die Krypto-Dateien (Binance) haben keine Lücken … Strukturell anfällig sind die vier Aktien-Bots." Die Trennlinie ist also sauber und begründet. **Anmerkung:** in keiner der fünf Krypto-Dateien steht ein Verweis darauf. Wer nur eine davon liest, kann Entscheidung nicht von Auslassung unterscheiden. |
| **U5** | Fehlt `BTCUSDT` in den Kursdaten, überspringt `t3_supertrend` seinen Regimefilter **stillschweigend** (`if "BTCUSDT" in all_data`); `volatility_breakout_crypto` **bricht ab** (`raise SystemExit`) und begründet das im Docstring: „Fehlt BTCUSDT, wird NICHT stillschweigend ungefiltert weitergerechnet". | **stille Divergenz.** Dieselbe Frage, zwei entgegengesetzte Antworten, ohne dass irgendwo eine Entscheidung dazu steht. **Eingrenzung, damit der Befund nicht grösser wirkt als er ist:** `t3_supertrend/forward_test.py` verhält sich live genauso (`btc_regime_bullish = True`, wenn BTCUSDT fehlt) — es ist **keine** Backtest-gegen-Live-Abweichung, sondern eine zwischen zwei Bots. Erreichbar wird sie, wenn `data/BTCUSDT_4h.csv` fehlt; dann rechnet `t3_supertrend` ohne Filter weiter und meldet es nicht. |
| **U6** | `ALLOCATION_PCT` dreimal hart verdrahtet | **Zustand nötig** (diese drei Bots führen den Wert nicht in `live_params.py`; `shared/portfolio_overview.py` löst das ausdrücklich auf). **Aber:** `elliott_wave_stocks` und `t3_supertrend` tragen dazu einen erklärenden Kommentar („dokumentierte Lücke, Sync-Check PR #24"), `elliott_wave` **nicht**. Dokumentations-Divergenz, keine Rechnung betroffen. |
| **U7** | Die beiden Elliott-Bots drucken zusätzlich die letzten zehn Trades | **kosmetisch.** Auf Stufe 4 verschwindet der Unterschied. |
| **U8** | Klammerzusatz zu den übersprungenen Trades: `elliott_wave_stocks` erklärt beide Gründe vollständig, `elliott_wave` nennt nur „nicht genug freies Kapital", die übrigen sieben nennen gar keinen | **Dokumentations-Divergenz.** Bei `elliott_wave` ist der Text sachlich richtig (dieser Bot hat kein Limit, also *kann* nur Kapital der Grund sein). Die in PR #48 als falsch erkannte Halbwahrheit ist nirgends mehr stehen geblieben — die **richtige** Erklärung ist aber nur bei einem der acht Limit-Bots angekommen. |
| **U9** | `rsi2_mean_reversion/equity_simulation.py:48` verweist auf „`run_from_walk_forward_best()` unten". **Diese Funktion existiert im ganzen Repo nicht.** | **stille Divergenz (Dokumentation).** Harmlos in der Wirkung, irreführend beim Lesen: ein Kommentar beschreibt eine Datei, die es so nicht mehr gibt — derselbe Fehlertyp, den die Kurven-Erneuerung an den abgelegten Kurven gefunden hat, nur in Prosa. |
| **U10** | Drei Kopien von `calculate_max_drawdown()` unter `research/` behaupten „identisch zur Hilfsfunktion in jedem Bot-eigenen `equity_simulation.py`". `research/volatility_scaled_sizing/vol_sizing_core.py` ist es (AST-gleich); `research/trailing_stops/atr_core.py` und `research/vbc_deepdive/vbc_core.py` sind es **nicht** — sie wickeln das Ergebnis zusätzlich in `float()`. | **stille Divergenz ausserhalb der neun Dateien, ohne erkennbare Zahlenwirkung.** `round(np.float64, 2)` und `round(float(x), 2)` liefern denselben Wert, nur einen anderen Typ. **Nicht nachgemessen** — in dieser Umgebung fehlt pandas (Abschnitt 7). Die Aussage „identisch" ist trotzdem falsch und sollte entweder stimmen oder anders lauten. |
| **U11** | `elliott_wave_stocks` kappt die Historie **vor** der Indikatorberechnung, die drei anderen Aktien-Bots **nur den Einstiegszeitpunkt** — und begründen genau das ausdrücklich | **unklar, ausserhalb des Auftragsrahmens.** Die Stelle liegt in `multi_symbol_optimise.py`, nicht in den neun Dateien; sie fällt hier nur auf, weil sich die Schleifenform von `collect_all_trades` daran entscheidet. Ob die Elliott-Variante nötig ist (Zigzag braucht lange Historie) oder ein Rückstand, ist **aus dem Code nicht entscheidbar**. **Fehlende Information:** ob die Abweichung je bewusst entschieden wurde — in `docs/` und `research/` findet sich dazu nichts. Nicht Gegenstand dieser Aufgabe, hier nur vermerkt. |

**Was ausdrücklich NICHT gefunden wurde:** keine abweichende Rechenformel,
keine abweichende Rundung, keine abweichende Reihenfolge, kein zweiter
Startkapital-Wert, keine Funktion, die in einem Bot etwas anderes tut als ihr
Name in den anderen sagt.

---

## 4. Wo aus einer Trade-Liste eine Zahl wird

### 4.1 In den neun Dateien: zwei Stellen, beide schon einheitlich

| Schritt | wo | wie oft |
|---|---|---:|
| Trade-Liste → Kapitalpfad | `simulate_portfolio()` → `shared/zuteilung.simuliere_portfolio()` | **1** (seit TB-26) |
| Kapitalpfad → Rendite | `(result["final_capital"] / STARTING_CAPITAL - 1) * 100` im `__main__` | 9, **zeichengleich** |
| Kapitalpfad → Drawdown | `calculate_max_drawdown()` | 9, **zeichengleich** |

Es ist überall **dieselbe** Stelle, im wörtlichen Sinn. Wer das Mass hier
ändern wollte, müsste neun identische Textstellen ändern — mechanisch, ohne
Fallunterscheidung, und der Wächter aus Abschnitt 7 meldet jede vergessene.

### 4.2 Ausserhalb der neun Dateien: das vollständige Inventar

**Auf demselben Kapitalpfad (ereignisbasiert):**

| Stelle | was sie tut |
|---|---|
| `strategies/{elliott_wave,elliott_wave_stocks}/oos_equity_simulation.py` | **importieren** `calculate_max_drawdown` — keine eigene Fassung |
| `shared/ergebniskurven.py::kennzahlen()` (Zeile 210–231) | **rechnet die Formel nach**, statt sie zu importieren (ausdrücklich so kommentiert: „nach der Formel aus ihrem `calculate_max_drawdown()`") |
| `shared/determinismus_lauf.py` (Zeile 623–625) | **rechnet die Renditeformel nach** und liest den Drawdown als Variable `max_dd` aus den `__main__`-Globalen des Bots |
| `shared/portfolio_overview.py::max_drawdown_pct()` | eigene Fassung auf einer **normierten Reihe**, andere Signatur |
| `research/volatility_scaled_sizing/vol_sizing_core.py` | wörtliche Kopie (AST-gleich) |
| `research/trailing_stops/atr_core.py`, `research/vbc_deepdive/vbc_core.py` | fast wörtliche Kopien (U10) |
| `research/exposure_messung/exposure_kern.py`, `research/hrp_portfolio/run_walk_forward.py`, `research/trend_overlay/run_overlay_analysis.py` | eigene Fassungen auf einer Kurve |

Bemerkenswert an `shared/determinismus_lauf.py`: es greift den Drawdown über den
**Variablennamen** `max_dd` aus dem `__main__`-Block ab. Benennt ein Bot diese
Variable um, meldet der Determinismus-Test stillschweigend `None` statt einer
Zahl. Dasselbe gilt für `trades` und `result`. Das ist eine unsichtbare
Namensschnittstelle, die keine der neun Dateien erwähnt.

### 4.3 Die Zahl, die *entscheidet*, steht woanders — und das ist der Punkt

Die Kennzahl, nach der **Parameter ausgewählt** werden, ist der
`robustness_score`. Er entsteht **nicht** in `equity_simulation.py`, sondern in
`multi_symbol_optimise.py::evaluate_combination_multi()` — und zwar aus der
**naiven Summierung der Trade-Prozente**:

```python
cum_returns = combined["pnl_pct"].cumsum()
max_drawdown = (cum_returns - cum_returns.cummax()).min()
```

Genau das, wovor Methodik-Prinzip 2 des Übergabeprotokolls warnt („Naive
Summierung von Trade-Prozenten ≠ echtes Kapitalwachstum"). Die
event-basierte Rechnung aus `equity_simulation.py` liefert die **ausgewiesenen**
Zahlen; die **auswählenden** Zahlen kommen von woanders.

Wie viele Stellen es sind, wenn man die Auswahl meint:

| Stelle | Anzahl | Block-Mass | chronologisches Mass |
|---|---:|:--:|:--:|
| `multi_symbol_optimise.py::evaluate_combination_multi` | **9** | ja | ja (seit M1 / PR #90) |
| `multi_symbol_walk_forward.py::evaluate_combination_multi_windowed` | **6** | ja | **nein** |
| `optimise_elliott.py` (2×), `optimise_trend.py` (1×) | **3** | ja | **nein** |
| `shared/param_search_agent.py` | 1 | — | rechnet den chronologischen Score aus den Spalten nach (TB-22) |

Die drei Bots `elliott_wave`, `elliott_wave_stocks` und `t3_supertrend` haben
keinen eigenen Walk-Forward-Rechner: ihre `multi_symbol_walk_forward.py`
importiert `evaluate_combination_multi` und bekommt beide Masse mit. Die
übrigen **sechs** Bots rechnen im Walk-Forward eine eigene Fassung — und die
kennt `max_drawdown_chronologisch_pct` nicht.

> **Befund:** M1 (PR #90) hat beide Masse in die Rastersuche gebracht, den
> Walk-Forward-Schritt aber bei sechs von neun Bots nicht erreicht. Der
> Walk-Forward ist Pflichtstufe der Methodik (Prinzip 7: Backtest →
> Walk-Forward → Equity-Simulation → Buy-and-Hold). Fällt die Entscheidung für
> das chronologische Mass, wählt der Walk-Forward bei sechs Bots weiterhin nach
> dem alten.

Das ist **über den Auftragsrahmen von TB-27 hinaus** und deshalb hier nicht
bewertet, nur belegt — aber es gehört vor die Entscheidung, weil es die Frage
„eine Stelle oder neun?" verschiebt: für die Mass-Reparatur lautet die Antwort
weder eine noch neun, sondern **neun plus sechs plus drei**.

---

## 5. Die Abhängigkeiten von aussen

Erhoben mit `research/tb27_kapitalsimulation/abhaengigkeiten.py`. **154**
Python-Dateien nennen `equity_simulation`; **125** fassen sie als Code an,
davon **123 von aussen**. TB-26 nannte fünf und hielt die Liste ausdrücklich
für unvollständig — sie war es.

### 5.1 Wer die Signatur abfragt (`inspect.signature` / `co_varnames`)

Das ist die Abhängigkeit, die TB-26 als tragend benannt hat: mehrere Werkzeuge
erkennen an der **Abwesenheit** des Arguments `max_concurrent_positions`, dass
`elliott_wave` kein Positionslimit hat. Genannt waren zwei. Es sind **zwölf**:

| Stelle | Zeile | Art |
|---|---:|---|
| `shared/portfolio_overview.py` | 348 | `inspect.signature(...).parameters` |
| `shared/determinismus_lauf.py` | 652 | `co_varnames` auf den `__main__`-Globalen |
| `shared/test_zuteilung.py` | 832 | `inspect.signature(...).parameters` |
| `research/order_sensitivity/run_one_bot.py` | 142 | `co_varnames` |
| `research/elliott_wave_lookahead/run_one_bot.py` | 221 | `co_varnames` |
| `research/elliott_wave_lookahead/decisions.py` | 81 | `co_varnames` |
| `research/elliott_wave_params/engine.py` | 83 | `co_varnames` |
| `research/exposure_messung/bot_lauf.py` | 190 | `co_varnames` |
| `research/hrp_portfolio/corrected_curves.py` | 199 | `co_varnames` |
| `research/sync_check/impact.py` | 135 | `co_varnames` |
| `research/tb24_haltedauern/positionen_holen.py` | 199 | `co_varnames` |
| `research/trend_overlay/corrected_curves.py` | 199 | `co_varnames` |

Dazu **eine** Abfrage auf `collect_all_trades`:
`research/pnl_2025_fixed_size/extract.py:103` prüft auf `use_take_profit` und
erkennt daran den Aktien-Elliott-Bot.

### 5.2 Wer die Datei als *Datei* braucht — je Bot eine, an genau diesem Pfad

| Stelle | wozu |
|---|---|
| `shared/ergebniskurven.py:154, 424` | **Bot-Liste**: „alle Ordner unter `strategies/`, die eine `equity_simulation.py` haben" |
| `shared/determinismus.py:142, 309` | dieselbe Bot-Liste |
| `research/zuteilungskaskade/messung_primaerschluessel.py:168` | dieselbe Bot-Liste |
| **`notifications/manual_close.py:401, 471`** | liest `ALLOCATION_PCT` **per AST als Literal aus der Datei** — und ist damit für `elliott_wave`, `elliott_wave_stocks` und `t3_supertrend` die **einzige** Quelle der angezeigten Positionsgrösse (deren `live_params.py` führt den Wert nicht). Diese Zahl steht im Bestätigungsdialog des Dashboards, mit dem Positionen geschlossen werden. |
| `research/sync_check/sync_table.py:182` | liest die Datei je Bot für den Sync-Vergleich |
| **`research/parameter_doku/pruefe_fundstellen.py`** | hängt an **Zeilennummern** in drei der neun Dateien — siehe 5.2b |
| `research/backtest_defaults/default_scan.py` | zählt sie zu den „Live-Einstiegspunkten" |

`notifications/manual_close.py` ist die schwerwiegendste der bisher nicht
gelisteten Abhängigkeiten: sie hängt nicht nur am Pfad, sondern daran, dass
`ALLOCATION_PCT` dort ein **Zahlen-Literal** ist. Die sechs Bots mit
`_ALLOCATION_PCT_PROZENT / 100` liefern dort bewusst `None` und fallen auf
`live_params.py` zurück; bei den drei anderen gibt es keinen Rückfallweg.

### 5.2b Eine Abhängigkeit an Zeilennummern — und sie ist heute schon rot

`research/parameter_doku/pruefe_fundstellen.py` hält dokumentierte Fundstellen
(Datei **plus Zeilennummer**) gegen die Wirklichkeit. Drei davon zeigen in
`equity_simulation.py`-Dateien. **Auf unverändertem `main` schlägt die Prüfung
fehl** (35 von 38 bestanden, Rückgabewert 1):

| dokumentiert | soll dort stehen | steht dort heute | steht wirklich in Zeile |
|---|---|---|---:|
| `t3_supertrend/equity_simulation.py:66` | `compute_btc_regime` | Leerzeile | 70 |
| `volatility_breakout/equity_simulation.py:160` | `collect_all_trades` | Leerzeile | 58 (Definition) / 152 (Aufruf) |
| `volatility_breakout_crypto/equity_simulation.py:176` | `collect_all_trades` | `exit()` | 54 (Definition) / 167 (Aufruf) |

Der Befund ist **vorbestehend** und nicht durch diese Untersuchung entstanden
(sie legt nur neue Dateien an). Er ist auch nicht neu in seiner Art —
`docs/UEBERSICHT_RESEARCH.md` hält fest, dass beim Schreiben bereits 2 von 20
Angaben falsch waren. Neu ist, **welche** heute falsch sind: alle drei zeigen
in die Dateien, um die es hier geht, und der Zeilenversatz passt zu den
Einfügungen aus TB-26 (`SIGNALSPALTE`-Block plus neuer Docstring).

Für die Mass-Reparatur ist das dreifach relevant:

1. Es gibt eine Abhängigkeitsklasse, die TB-26 nicht auf dem Zettel hatte:
   **Zeilennummern**. Jede Änderung an diesen Dateien — Weg A wie Weg B —
   verschiebt sie weiter.
2. Diese Prüfung ist einer der wenigen Wächter im Repo, die ohne `pandas`
   laufen. Dass sie seit TB-26 rot ist und niemandem aufgefallen ist, ist ein
   Argument dafür, den Wächter aus Abschnitt 7 in denselben Durchlauf zu
   hängen.
3. Sie lässt sich in derselben Reparatur mit richtigstellen — drei Zahlen.

### 5.3 Wer sie ausführt

| Weg | Stellen |
|---|---|
| **Unterprozess** (`sys.executable`, wegen der `sys.modules`-Kollision gleichnamiger Module) | `shared/ergebniskurven.py` → `shared/kurven_lauf.py`; `shared/determinismus.py` → `shared/determinismus_lauf.py`; `shared/portfolio_overview.py` (`-c`-Skript, `cwd=strategy_dir`) |
| **`runpy.run_path(..., run_name="__main__")`** | `shared/kurven_lauf.py:152`, `shared/determinismus_lauf.py:590`, `research/backtest_defaults/{kopplungsnachweis,regression}.py`, `research/forward_test_sync/backtest_regression.py`, `research/zuteilungskaskade/messung_primaerschluessel.py:122` |
| **`importlib.util.spec_from_file_location`** | `research/uebersprungene_trades/aufschluesselung.py:87` |
| **Direktimport** nach `sys.path`-Umbiegung (`import equity_simulation as es`) | **65** Dateien: 37 unter `strategies/` (Experiment-, Report- und OOS-Skripte), 25 unter `research/`, 3 unter `shared/` (darunter `shared/portfolio_overview.py`) |

Zahlen je Klasse, wie das Werkzeug sie meldet: IMPORT 65, LADEN 8, PROZESS 34,
SIGNATUR 17 (davon 13 mit Bezug auf `equity_simulation` — die übrigen vier
fragen `run_backtest`, `get_trades_for_symbol` oder `schliessen.ausfuehren` ab
und stehen nur deshalb in der Liste, weil dieselbe Datei die Simulation
anderswo anfasst), PFAD 81.

Die `sys.modules`-Kollision ist der Grund, warum fast alles über Unterprozesse
läuft: neun gleichnamige Module im selben Prozess würden einander lautlos
überschreiben — ein Fehler, den das Projekt schon einmal hatte
(`shared/portfolio_overview.py`, Kommentar bei Zeile 295).

### 5.4 Wie gesucht wurde, und was entgangen sein könnte

Gesucht wurde nach dem Zeichenketten-Stamm `equity_simulation` in allen
`.py`-Dateien des Repos (ausser `.git`, `__pycache__`, `data`, `results`,
`logs`) und anschliessend nach Klassen sortiert. Zusätzlich von Hand geprüft:

* **zusammengesetzte Namen** (`"equity_" + "simulation.py"`, f-Strings mit
  Variablenteil): keine gefunden;
* **Verzeichnis-Listings**, die alle `.py` eines Bot-Ordners einsammeln und die
  Datei so mitnehmen, ohne sie zu nennen: keine gefunden;
* `.sh`, `.plist`, `.md`, `.txt` mitdurchsucht.

**Was entgangen sein kann:** die **Crontab** und die **launchd-Vorlagen des
Nutzers** liegen nicht im Repo und wurden nicht geprüft (das Übergabeprotokoll
weist ohnehin aus, dass sich die Crontab am 12.09.2026 nicht ändern liess).
Ebenfalls nicht geprüft: heruntergeladene Kopien im Downloads-Ordner des
Nutzers (Abschnitt 10.5 des Protokolls) — dort liegen nummerierte Duplikate
`strategies-2` bis `strategies-12`.

---

## 6. Die zwei Wege — beide durchgespielt

**Nicht entschieden.** Das ist eine Entscheidung des Nutzers; die Frist steht
auf dem 13.12.2026.

### Weg A — die neun Dateien zusammenlegen

Eine gemeinsame `shared/kapitalsimulation.py`; je Bot bleibt eine dünne Datei
mit `SIGNALSPALTE`, `ALLOCATION_PCT` und dem bot-eigenen `collect_all_trades`.

| | |
|---|---|
| **Was es löst** | Das Mass stünde einmal da. Die `sys.modules`-Kollision, wegen der heute fast alles über Unterprozesse läuft, verschwände für den gemeinsamen Teil. |
| **Was es kostet** | Der gemeinsame Teil ist **schon heute einheitlich** (Abschnitt 2.3) — der Gewinn ist also klein. Der bot-eigene Teil (`collect_all_trades`, neunmal verschieden, plus die drei `__main__`-Unterschiede) muss trotzdem je Bot bleiben. |
| **Was bricht** | **U1 zwölfmal.** Zwölf Stellen fragen die Signatur von `simulate_portfolio` ab. Eine gemeinsame Fassung hätte **eine** Signatur — die Unterscheidung „hat dieses Bot ein Limit?" wäre weg und müsste an zwölf Stellen anders gebaut werden, bevor die Zusammenlegung greift. Ein Limit-Argument mit Vorbelegung `None` wäre für alle zwölf eine stille Falschauskunft. |
| | **Die Bot-Liste dreier Werkzeuge.** `ergebniskurven.py`, `determinismus.py` und `messung_primaerschluessel.py` bestimmen „welche Bots gibt es" über die Existenz genau dieser Datei. |
| | **`notifications/manual_close.py`.** Verschwände `ALLOCATION_PCT` als Literal aus der Datei, zeigte der Schliess-Dialog für drei Bots keine Positionsgrösse mehr — in einem **schreibenden** Weg. |
| | **Die Namensschnittstelle `max_dd`/`result`/`trades`** zu `determinismus_lauf.py`, die nirgends dokumentiert ist. |
| | **Drei dokumentierte Zeilennummern** (`research/parameter_doku/`), die heute schon nicht mehr stimmen (5.2b). |
| **Grössenordnung** | 9 Dateien umgebaut, ≥ 12 Signaturabfragen ersetzt, 3 Bot-Listen umgestellt, 1 schreibender Dashboard-Pfad nachgezogen, 2 Testsuiten (`shared/test_zuteilung.py`, `shared/test_determinismus.py`) angepasst — und danach neun Kurven neu erzeugt und geprüft. |

### Weg B — die Zielfunktion an den vorhandenen Stellen tauschen

| | |
|---|---|
| **Was es löst** | Genau das, was die Mass-Reparatur will, ohne die Architektur anzufassen. |
| **Was es kostet** | Die neun **zeichengleichen** Stellen in `equity_simulation.py` sind mechanisch: derselbe Text neunmal. Der Wächter (Abschnitt 7) meldet jede vergessene. |
| **Was bricht** | Nichts von dem, was unter Weg A steht. Aber: `shared/ergebniskurven.py` und `shared/determinismus_lauf.py` rechnen die Formel **nach** und müssten mit, sonst laufen die abgelegten Kurven gegen die neuen Zahlen — das ist genau der Zustand, den PR #86 aufgeräumt hat. |
| **Was er NICHT löst** | Die auswählende Kennzahl (Abschnitt 4.3). Wer nur `equity_simulation.py` anfasst, ändert die ausgewiesenen Zahlen und nicht die Parameterwahl. |
| **Grössenordnung** | 9 zeichengleiche Stellen + 2 Nachrechnungen in `shared/`; **wenn die Auswahl mitgemeint ist**, zusätzlich 9 + 6 + 3 Stellen in `multi_symbol_optimise.py`, `multi_symbol_walk_forward.py` und `optimise_*.py`. |

### Der kleinste Eingriff, der die Zusicherung trägt

Wenn die Zusicherung lautet *„das Mass steht ab jetzt an einer Stelle"*, dann
ist der kleinste Eingriff **nicht** die Zusammenlegung der neun Dateien,
sondern:

1. `calculate_max_drawdown()` und die Renditeformel **einmal** nach
   `shared/` ziehen (nach dem Muster von `shared/zuteilung.py`), die neun
   Dateien importieren sie. Das lässt Signatur, Dateipfad, `ALLOCATION_PCT`
   und alle zwölf Signaturabfragen unberührt — es fällt nur der neunfach
   kopierte Rumpf weg.
2. `shared/ergebniskurven.py::kennzahlen()` und
   `shared/determinismus_lauf.py` auf dieselbe Quelle umstellen, statt
   nachzurechnen.
3. Erst danach, als **getrennte** Entscheidung: welches Mass führt — und ob
   die 9 + 6 + 3 auswählenden Stellen mitwandern (Abschnitt 4.3).

Schritt 1 und 2 sind rein strukturell und ändern **keine Zahl**; das ist
prüfbar, weil `shared/ergebniskurven.py` danach weiterhin `9× AKTUELL` melden
muss. Schritt 3 ändert Zahlen und gehört deshalb hinter den Vergleich, nicht
davor.

---

## 7. Belastbarkeit

### Womit verglichen wurde, und wo die Methode an Grenzen stösst

* **AST (Stufe 3) ist das tragende Mass**, Text und Tokenstrom stehen daneben.
  Der AST-Vergleich beweist **Gleichheit des Codes, nicht Gleichheit des
  Verhaltens**: zwei zeichengleiche `collect_all_trades()` können sich
  verschieden verhalten, weil `get_trades_for_symbol()` in jedem Bot eine
  andere Funktion ist. Umgekehrt gilt der Befund streng — was als verschieden
  gemeldet wird, **ist** verschieden.
* **Nichts wurde ausgeführt.** In dieser Umgebung fehlen `pandas`, `numpy`,
  `binance`, `scipy`, `fastapi`, `yfinance`. Kein Bot, kein Backtest, keine
  Kurve ist gelaufen. Aussagen über Zahlenwirkung (etwa bei U10) sind deshalb
  als **nicht nachgemessen** gekennzeichnet.
* **Basislauf auf unverändertem `main`** (zur Abgrenzung vorbestehender
  Fehlschläge):

  | Prüfung | Rückgabe | Grund |
  |---|---|---|
  | `notifications/test_manual_close.py` | **0** | läuft |
  | `shared/test_zuteilung.py` | 1 | `numpy` fehlt |
  | `shared/test_ergebniskurven.py` | 1 | `pandas` fehlt |
  | `shared/test_determinismus.py` | 1 | `pandas` fehlt |
  | `dashboard/test_dashboard.py` | 1 | `pandas` fehlt |
  | `research/parameter_doku/pruefe_fundstellen.py` | **1** | **echter Befund**, kein Umgebungsproblem — siehe 5.2b |

  Die vier `pandas`/`numpy`-Fehlschläge sind vorbestehend und umgebungsbedingt.
  Der fünfte ist ein inhaltlicher Befund, ebenfalls vorbestehend: er tritt auf
  unverändertem `main` genauso auf. Diese Untersuchung fügt nur Dateien unter
  `research/` und `docs/` hinzu und kann keinen davon beeinflussen.

### Vollständigkeit der Abhängigkeitsliste

Siehe Abschnitt 5.4. Kurz: mechanisch über den Namensstamm gesucht, von Hand
auf zusammengesetzte Namen und Verzeichnis-Listings gegengeprüft, Crontab und
launchd-Vorlagen des Nutzers nicht erreichbar.

### Reproduktionsbefehle

```
python3 research/tb27_kapitalsimulation/vergleich.py
python3 research/tb27_kapitalsimulation/vergleich.py --pruefen
python3 research/tb27_kapitalsimulation/vergleich.py --zeige calculate_max_drawdown
python3 research/tb27_kapitalsimulation/vergleich.py --datei multi_symbol_optimise.py
python3 research/tb27_kapitalsimulation/abhaengigkeiten.py --ohne-erwaehnung
python3 research/tb27_kapitalsimulation/test_vergleich.py
python3 research/parameter_doku/pruefe_fundstellen.py     # bestehendes Werkzeug, zu 5.2b
```

Die ersten sechs laufen ohne `pandas`, ohne Kursdaten und ohne Netz; keiner
schreibt etwas. Das siebte ist ein vorhandenes Werkzeug des Repos und ebenfalls
rein lesend.

Einzelbelege, die im Bericht behauptet werden und sich mit einer Zeile prüfen
lassen:

```
grep -l melde_uebersprungene_balken strategies/*/equity_simulation.py       # U4 -> 4 (die Aktien-Bots)
grep -rn "co_varnames\|inspect.signature" --include=*.py . | grep -c max_concurrent   # -> 11
ls strategies/*/multi_symbol_walk_forward.py | wc -l                        # -> 9
grep -l 'pnl_pct"\].cumsum' strategies/*/multi_symbol_walk_forward.py | wc -l  # -> 6
grep -rn run_from_walk_forward_best --include=*.py . | wc -l                # U9 -> 1 (nur der Kommentar)
```

Zur zweiten Zeile: sie findet **11** der **12** Signaturabfragen aus 5.1. Die
zwölfte, `shared/determinismus_lauf.py`, verteilt den Ausdruck über die Zeilen
651 und 652 und entgeht dem einzeiligen `grep` — genau die Sorte Lücke, wegen
der `abhaengigkeiten.py` dateiweise statt zeilenweise klassifiziert.

### Warum es ein Testdokument gibt

Der Auftrag stellt es frei: nötig nur, wenn ausführbarer Code entsteht, der
bleiben soll. **Er entsteht.** `vergleich.py --pruefen` ist ein Wächter: er
hält den Stand vom 13.09.2026 fest und meldet, wenn eine der neun Dateien
später still auseinanderläuft. Ein Wächter, der nie rot werden kann, ist
schlimmer als keiner — deshalb weist `test_vergleich.py` (23 Prüfungen, alle
grün) am Verhalten nach, dass er

* bei einer verfälschten `calculate_max_drawdown()` **rot** wird und Bot und
  Funktion benennt,
* bei neuen Kommentaren und geänderten Docstrings **grün** bleibt (sonst würde
  er bei jeder Doku-Pflege stören und binnen Wochen ignoriert),
* eine neu hinzugekommene und eine verschwundene Funktion meldet,
* Rechnen von Reden unterscheidet (Stufe 4).

Das ist Methodik-Prinzip 12 des Übergabeprotokolls: eine grüne Prüfung muss
auch rot werden können.

---

## 8. Scope-Grenzen

**Angefasst:** ausschliesslich neue Dateien unter
`research/tb27_kapitalsimulation/` und `docs/`.

**Gelesen, nicht geändert:** die neun `equity_simulation.py`, die neun
`live_params.py`, `multi_symbol_optimise.py`, `multi_symbol_walk_forward.py`,
`forward_test.py`, `shared/zuteilung.py`, `shared/ergebniskurven.py`,
`shared/determinismus*.py`, `shared/portfolio_overview.py`,
`notifications/manual_close.py`, `dashboard/*`.

**Nicht angefasst:** keine `results/*/equity_curve.csv`, nichts unter
`broker/`, keine Crontab, keine launchd-Vorlage, keine Datenbank, keine
Kursdatei.

**Nicht entschieden:** welcher der beiden Wege gegangen wird, und welches Mass
künftig führt. Beides gehört dem Nutzer.

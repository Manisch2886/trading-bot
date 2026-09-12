# Welche Parameterwahlen hängen an der Drawdown-Reihenfolge?

> ## DIES IST EINE UNTERSUCHUNG, KEINE KORREKTUR
>
> Es wurde **nichts geändert** — kein `live_params.py`, kein
> `forward_test.py`, kein `equity_simulation.py`, kein
> `multi_symbol_optimise.py` und keine Ergebnisdatei eines Bots. Belegt
> per `git status` und `git diff` als Prüfung 16 und 17 in
> `test_drawdown.py`; alles Geschriebene liegt unter
> `research/drawdown_reihenfolge/`.
>
> Ob aus den hier gezeigten Zahlen eine Änderung folgt, **entscheidet der
> Nutzer**. Derselbe Hinweis steht in jeder Ergebnisdatei unter dem
> Schlüssel `hinweis` und wird von jedem Skript beim Start und am Ende
> ausgegeben (`botenv.HINWEIS`, nicht abschaltbar).

---

## 0. Entscheidungsgrundlage

### Die Kernfrage (Frage 4) zuerst: Ja — bei vier von neun Bots

Bei **vier** Bots wählt die Stufe, die die Parameter dokumentiert
bestimmt hat, unter dem erlebbaren Drawdown eine **andere** Kombination
als unter dem heute benutzten:

| Bot | heute live | Wahl unter dem chronologischen Drawdown | Abstand |
|---|---|---|---|
| `turtle_soup_crypto` | Donchian 10 / Stop **structural** | Donchian 10 / **kein Stop** | Rang 1 ↔ 2 vertauscht, Sieger 21 % vor dem Zweiten |
| `turtle_soup_stocks` | Donchian 10 / **kein Stop** | Donchian 10 / **Stop 5 %** | Rang 1 ↔ 2 vertauscht, Sieger 17 % vor dem Zweiten |
| `elliott_wave_stocks` | dev 5 % / Stop 3 % / kein Ziel | dev 5 % / **Stop 2 %** / kein Ziel — die Live-Kombination **steigt** von Rang 6 auf Rang 2 | Sieger 12 % vor dem Zweiten |
| `elliott_wave` | dev 10 % / Stop 6 % / Fib 0,618 | die Kandidatenliste, aus der diese Wahl stammt, enthält sie **nicht mehr**: In-Sample-Top-5 rutschen von Stop 4–6 % auf Stop **2–4 %** | Live-Kombination fällt von Rang 2 auf Rang 6 von 37 |

Bei **fünf** Bots ändert sich nichts: `rsi2_crypto`, `rsi2_mean_reversion`,
`volatility_breakout`, `volatility_breakout_crypto` und `t3_supertrend` —
letzterer aus einem Grund, den niemand beabsichtigt hat (Abschnitt 2.3).

**Der Befund ist kein Rauschen.** Der chronologische Drawdown liegt bei
11 von 13 gemessenen Bot-Fenstern **außerhalb** der Spanne, die 200
zufällige Vertauschungen der Symbol-Blockreihenfolge erzeugen — der
Unterschied ist also größer als die Willkür, die im Bot-Maß selbst
steckt. Umgekehrt ist das Bot-Maß gegen seine eigene Willkür oft nicht
stabil: bei `elliott_wave_stocks` gewinnt in nur **17,5 %** von 200
Symbol-Reihenfolgen dieselbe Kombination, bei `turtle_soup_stocks` in
30,5 %, bei `volatility_breakout` in 40,0 %. In den übrigen
Reihenfolgen gewinnt eine andere. Einzelheiten in Abschnitt 5.

### Frage 5 in einem Satz, und sie fällt anders aus als erwartet

Die Symbol-Blockreihenfolge ist nicht zu verteidigen — aber der
chronologische Drawdown auf der **kumulierten PnL-Summe** ist auch nicht
die Wahrheit, sondern nur der nähere Näherungswert. Beide Maße addieren
Einzeltrade-Prozente zu je einer ganzen Einheit; ein Wert wie −2135 % ist
als Kapitalverlust unmöglich. Den erlebbaren Verlauf hat das Projekt
längst: `equity_simulation.py` jedes Bots. Gegen deren Kapital-Drawdown
gemessen (Abschnitt 6):

| Bot | Rangkorrelation \|Drawdown\| zum Kapital-Drawdown: **Blockreihenfolge** | **chronologisch** |
|---|---|---|
| `rsi2_crypto` | 0,371 | **0,886** |
| `rsi2_mean_reversion` | **−0,314** | **0,829** |
| `turtle_soup_crypto` | **−0,333** | **0,690** |
| `turtle_soup_stocks` | 0,259 | **0,559** |
| `volatility_breakout` | −0,200 | **0,800** |
| `volatility_breakout_crypto` | 0,400 | **1,000** |
| `elliott_wave` | 0,871 | **0,983** |
| `elliott_wave_stocks` | 0,707 | 0,706 |

Die Blockreihenfolge steht bei zwei Bots in **umgekehrtem** Verhältnis
zum echten Kapital-Drawdown: wer sie minimiert, wählt dort systematisch
den schlechteren Kapitalverlauf. Empfehlung samt Gegenargument und Preis
in Abschnitt 6.

### Woher die Zahlen kommen

Diese Untersuchung rechnet **nicht** mit einer eigenen Backtest-Kopie.
Sie ruft die echten Bot-Funktionen auf:

| Aufgabe | verwendete Bot-Funktion |
|---|---|
| Kursdaten und Fensterzuschnitt | `multi_symbol_optimise.load_all_symbol_data` |
| Trades je Symbol | `multi_symbol_optimise.get_trades_for_symbol` |
| BTC-Regimefilter (nur `t3_supertrend`) | `regime_filter.compute_btc_regime` / `filter_trades_by_regime` |
| Bewertungsmaß | `multi_symbol_optimise.calculate_robustness_score` (per Aufruf, nicht nachgebaut) |
| Mindestfilter | `MIN_TRADES` / `MIN_SYMBOLS_CONTRIBUTING` / `MIN_AVG_RETURN_PCT` des Bots |
| Suchraster | `DEVIATION_RANGE`, `STOP_LOSS_RANGE`, … des Bots |
| In-Sample-Fenster | `multi_symbol_walk_forward.split_all_symbols` + `TRAIN_SPLIT_RATIO` des Bots |
| Kapitalsimulation | `equity_simulation.simulate_portfolio` / `calculate_max_drawdown` |

Neu ist genau eines: derselbe Drawdown wird auf **vier**
Zeilenreihenfolgen derselben Trade-Menge gerechnet — der des Bots
(`dd_bot`), der Symbol-Blockreihenfolge (`dd_block`), stabil nach
`entry_time` (`dd_entry`, das Maß von `equity_simulation`) und stabil
nach `exit_time` (`dd_exit`, die Reihenfolge, in der Gewinne und
Verluste wirklich im Konto landen).

### Pflicht-Gegenchecks

`python3 test_drawdown.py <bot>` — **18/18 Prüfungen** bei allen
geprüften Bots. Enthalten sind fünf **Gegenproben** (Projekt-Prinzip 12:
eine grüne Prüfung ist erst etwas wert, wenn belegt ist, dass sie auch
rot werden kann):

| Prüfung | Ergebnis |
|---|---|
| Kennzahlen Feld für Feld identisch zu `evaluate_combination_multi` des Bots | ja, bei jeder geprüften Kombination |
| `dd_bot` und `score_bot` identisch zum Bot | ja |
| Score kommt unverändert aus `calculate_robustness_score` | ja, 200 Zufallsfälle |
| Filterentscheidung (None/nicht-None) identisch zum Bot | ja |
| In-Sample-Fenster identisch zu `evaluate_combination_multi_windowed` | ja (sechs Prototyp-Bots) |
| **Gegenprobe:** vertauschte Blockreihenfolge bricht die Gleichheit | ja |
| **Gegenprobe:** falsche Score-Formel weicht ab | ja |
| **Gegenprobe:** Umsortieren ändert nur den Drawdown, nicht Anzahl/Rendite | ja |
| **Gegenprobe:** bei nur einem Symbol-Block gibt es keine Streuung | ja |
| **Gegenprobe:** Drawdown hängt wirklich an der Reihenfolge | ja |
| `git status` / `git diff` außerhalb dieses Ordners leer | ja |

Dazu der stärkste verfügbare Beleg: `python3 historie.py <bot>` stellt
die **gespeicherte** Rasterausgabe jedes Bots
(`results/<bot>/multi_symbol_optimisation_results.csv` — die Datei, auf
die sich die Prototyp-Berichte berufen) Zeile für Zeile gegen die heute
nachgerechneten Werte. Sechs Bots reproduzieren **bitgenau**, bei
`t3_supertrend` gelingt es nach Abschalten des später hinzugefügten
Regimefilters ebenfalls bitgenau (Abschnitt 2.3). Einzelheiten:
Abschnitt 2.

Und als unabhängige Bestätigung des Befundes, der diese Untersuchung
ausgelöst hat: für `elliott_wave_stocks` bei dev 5 % / Stop 3 % / kein
Ziel ergibt sich **−82,50 %** (Blockreihenfolge) gegen **−259,86 %**
(chronologisch) — genau die −82,5 % gegen −259,9 % aus
`research/elliott_wave_params/BERICHT.md`, Abschnitt 6.

### Belastbarkeit

* **Datenbasis** je Bot in Abschnitt 3. Zwischen 4 und 81 Kombinationen
  je Raster, 18 bis 147 Symbole, 150 bis 17 809 Trades je Kombination.
* **Streuung**: 200 Permutationen der Blockreihenfolge und 200
  Vertauschungen gleichzeitiger Einstiege je Kombination, fester
  Startwert 20260912. Abschnitt 5 weist aus, wo die Grenze liegt.
* **Dünn ist**: `volatility_breakout` und `volatility_breakout_crypto`
  haben nur **vier** Rasterpunkte. Eine Rangkorrelation über vier Punkte
  ist keine belastbare Zahl — in Abschnitt 6 entsprechend gekennzeichnet.
* **Nicht reproduzierbar** ist die historische Rasterausgabe von
  `elliott_wave_stocks`: die Look-Ahead-Korrektur (PR #26) hat dessen
  Trades vollständig verändert. Die Herkunft der Parameterwahl ist dort
  aus den Berichten und `live_params.py`-Kommentaren belegt, nicht aus
  der Zahl (Abschnitt 2.4).
* **Kursdatenlücken**: Die APH-Lücke berührt diese Zahlen **nicht** —
  gemessen, nicht angenommen (Abschnitt 7, A-5).

### Reproduktion

```
cd research/drawdown_reihenfolge
python3 run_all.py                       # alles, rund 2,5 Stunden
python3 test_drawdown.py turtle_soup_crypto        # Selbsttests, ein Bot
python3 test_drawdown.py turtle_soup_crypto --alle # jede Rasterkombination
python3 analyse.py turtle_soup_crypto              # Raster, Gesamtfenster
python3 analyse.py turtle_soup_crypto --fenster is # Raster, In-Sample
python3 analyse.py t3_supertrend --ohne-regimefilter   # historischer Stand
python3 historie.py turtle_soup_crypto             # gegen die gespeicherte Datei
python3 kapitalkurve.py turtle_soup_crypto         # gegen den Kapitalverlauf
python3 einzelsymbol.py turtle_soup_crypto         # Einzelsymbol-Optimierer
python3 uebersicht.py                              # die Tabellen dieses Berichts
```

Ein Prozess je Bot ist Pflicht: die neun Bots haben gleichnamige,
inhaltlich verschiedene Module (`backtest_elliott.py`,
`multi_symbol_optimise.py`, …). Ein Import zweier Bots im selben Prozess
würde über `sys.modules` still den falschen laden. `run_all.py` startet
deshalb je Bot und Schritt einen eigenen Prozess.

---

## 1. Frage 1 — Wo genau geht der Drawdown in die Auswahl ein?

### Die Formel

`multi_symbol_optimise.calculate_robustness_score` ist bei **allen neun
Bots wörtlich identisch**:

```python
def calculate_robustness_score(row: dict) -> float:
    drawdown_penalty = abs(row["max_drawdown_pct"]) if row["max_drawdown_pct"] != 0 else 1.0
    return round((row["avg_return_pct"] * (row["num_trades"] ** 0.5)) / drawdown_penalty, 3)
```

Der Drawdown steht **allein im Nenner**. Er geht also nicht gewichtet
ein, sondern **voll multiplikativ**: verdoppelt sich der Drawdown,
halbiert sich der Score. Zwei Kombinationen mit gleicher Rendite und
gleicher Trade-Zahl werden ausschließlich über ihren Drawdown geordnet.
Das ist der Grund, warum der Reihenfolge-Befund die Rangfolge überhaupt
verschieben kann.

Zähler und Nenner werden **gerundet, bevor** sie in die Formel gehen
(`round(avg_return, 2)`, `round(max_drawdown, 2)`) — diese Untersuchung
rundet genauso, weil nur diese Zahl die bisherige Parameterwahl getragen
hat.

### Wie der Drawdown entsteht

Ebenfalls bei allen neun Bots wörtlich dieselben zwei Zeilen, in
`evaluate_combination_multi`:

```python
cum_returns = combined["pnl_pct"].cumsum()
max_drawdown = (cum_returns - cum_returns.cummax()).min()
```

`combined` ist `pd.concat` über die Symbol-Blöcke, in der Reihenfolge,
in der `all_data.items()` sie liefert — also der Reihenfolge der
Symbolliste (`config/top25_symbols.txt` bzw. `config/sp500_top150.txt`).
Diese Reihenfolge ist kein Verlauf, sondern ein Nebenprodukt.

### Wo nach dem Score sortiert oder gefiltert wird

`sort_values("robustness_score", ascending=False)` steht an **18**
Stellen unter `strategies/`:

| Stelle | Anzahl | wirkt auf |
|---|---|---|
| `multi_symbol_optimise.py` | 9 (alle Bots) | die Rastersuche selbst — die Stufe, die die Parameterwahl getragen hat |
| `multi_symbol_walk_forward.py` | 6 (die Prototyp-Bots) | die Wahl der In-Sample-besten Kombination, die dann Out-of-Sample geprüft wird |
| `optimise_elliott.py` / `optimise_trend.py` | 3 (die drei ältesten Bots) | Einzelsymbol-Raster — **nicht betroffen**, siehe unten |

Die Walk-Forward-Skripte der drei ältesten Bots (`elliott_wave`,
`elliott_wave_stocks`, `t3_supertrend`) sortieren nicht selbst, sondern
rufen `run_multi_optimisation(train_data)` auf — die Sortierung
passiert dort in `multi_symbol_optimise`. Betroffen sind sie genauso.

Dazu zwei Stellen außerhalb von `strategies/`:

* **`shared/param_search_agent.py:162`** — `max(valid_results, key=lambda r:
  r["robustness_score"])`. Das ist die **Zielfunktion von Agent 2**. Der
  Agent bekommt die bisherigen Ergebnisse als Tabelle und schlägt danach
  die nächste Kombination vor; der Score bestimmt also nicht nur, was am
  Ende gewinnt, sondern auch, wohin der Agent sucht.
* **`quarterly_review.py` (drei Bots), `format_wf_result`** — schreibt
  `Score {r['robustness_score']}` für In-Sample und Out-of-Sample sowohl
  der Live- als auch der vorgeschlagenen Parameter in den Berichtstext.
  Dieser Text ist die Eingabe für `quarterly_interpreter`
  (Sonnet 5), der daraus die Empfehlung „Parameter behalten / Wechsel
  erwägen" formuliert. Der Score wirkt dort also auch auf die
  vierteljährliche Einordnung.

### Die Einzelsymbol-Optimierer sind nicht betroffen — gemessen

`optimise_elliott.py` und `optimise_trend.py` rechnen denselben Score mit
demselben `cumsum`-Drawdown, aber auf **einem** Symbol. `einzelsymbol.py`
prüft, ob die Trade-Liste eines Symbols, so wie die Bot-Funktion sie
liefert, bereits nach `entry_time` steigt. Ergebnis über acht Bots:

| Bot | Symbole | davon `entry_time` bereits monoton |
|---|---|---|
| `t3_supertrend` | 18 | 18 |
| `rsi2_crypto` | 18 | 18 |
| `turtle_soup_crypto` | 20 | 20 |
| `volatility_breakout_crypto` | 20 | 20 |
| `rsi2_mean_reversion` | 147 | 147 |
| `turtle_soup_stocks` | 147 | 147 |
| `volatility_breakout` | 147 | 147 |
| `elliott_wave_stocks` | 137 | 137 |

Innerhalb eines Symbols **ist** die Zeilenreihenfolge die Zeit. Der
Befund betrifft ausschließlich die Multi-Symbol-Auswertung.

---

## 2. Frage 2 — Welche Bots sind betroffen? Belegt, nicht vermutet

### 2.1 Alle neun benutzen dieselbe Stelle

Der Code ist eindeutig: alle neun `multi_symbol_optimise.py` enthalten
dieselbe Formel und dieselben zwei `cumsum`-Zeilen, und alle neun
sortieren danach. Die Frage ist deshalb nicht, ob ein Bot den Score
benutzt, sondern ob seine dokumentierte Parameterwahl über ihn gelaufen
ist.

### 2.2 Sechs Bots: die gespeicherte Rasterausgabe reproduziert bitgenau

`historie.py` findet jede Zeile der gespeicherten
`results/<bot>/multi_symbol_optimisation_results.csv` wieder und
vergleicht sieben Spalten:

| Bot | Zeilen | `num_trades` | `win_rate` | `total_return_pct` | `avg_return_pct` | `max_drawdown_pct` ↔ `dd_block` | `robustness_score` ↔ `score_block` |
|---|---|---|---|---|---|---|---|
| `rsi2_crypto` | 6 | 6/6 | 6/6 | 6/6 | 6/6 | **6/6** | **6/6** |
| `rsi2_mean_reversion` | 6 | 6/6 | 6/6 | 6/6 | 6/6 | **6/6** | **6/6** |
| `turtle_soup_crypto` | 8 | 8/8 | 8/8 | 8/8 | 8/8 | **8/8** | **8/8** |
| `turtle_soup_stocks` | 12 | 12/12 | 12/12 | 12/12 | 12/12 | **12/12** | **12/12** |
| `volatility_breakout` | 4 | 4/4 | 4/4 | 4/4 | 4/4 | **4/4** | **4/4** |
| `volatility_breakout_crypto` | 4 | 4/4 | 4/4 | 4/4 | 4/4 | **4/4** | **4/4** |

Damit ist belegt und nicht vermutet: bei diesen sechs Bots ist die
Parameterwahl über `multi_symbol_optimise` und über genau den Drawdown
auf der Symbol-Blockreihenfolge gelaufen. Die zugehörigen
`PROTOTYPE_FINDINGS.md` sagen es zusätzlich wörtlich, etwa
`turtle_soup_crypto`, Abschnitt 4: „Validierte Basiskonfiguration:
Donchian 10, Stop ‚structural' (**Gesamtzeitraum-bester Score**)".

Auch die **In-Sample-Zahlen** der Prototyp-Berichte reproduzieren
bitgenau, und zwar über einen zweiten, unabhängigen Codepfad
(`multi_symbol_walk_forward`): `rsi2_crypto` In-Sample-Score 0,241 bei
169 Trades, `turtle_soup_stocks` 0,263 bei 8441 Trades,
`volatility_breakout` 0,249 bei 3180 Trades, `rsi2_mean_reversion`
0,033 bei 3674 Trades — alle vier identisch zu den dortigen Tabellen.

### 2.3 `t3_supertrend`: betroffen war er, betroffen ist er nicht mehr — versehentlich

Zwei Befunde, beide belegt.

**Erstens: heute rechnet dieser Bot bereits chronologisch.** Nach dem
Zusammenfügen läuft in `evaluate_combination_multi` noch der
BTC-Regimefilter, und `regime_filter.filter_trades_by_regime` sortiert
intern nach `entry_time` — es braucht das für `pd.merge_asof`. Die
Zeilenreihenfolge, auf der anschließend der Drawdown entsteht, ist damit
die chronologische. Gemessen: über **alle 81** Rasterkombinationen ist
`dd_bot == dd_entry`, und bei keiner einzigen `dd_bot == dd_block`. Das
steht nirgends im Code als Absicht und nirgends in der Dokumentation. Es
ist ein Nebeneffekt einer Zeile, die aus einem ganz anderen Grund dort
steht.

**Zweitens: zur Zeit der Parameterwahl war er es noch nicht.** Die
gespeicherte `results/t3_supertrend/multi_symbol_optimisation_results.csv`
lässt sich mit dem heutigen Code **nicht** reproduzieren (Kombination
16/30/ADX 20/Stop 4: 1448 gegen 980 Trades). Schaltet man den
Regimefilter ab, reproduziert sie **bitgenau, alle 23 Zeilen und alle
sieben Spalten** — inklusive `max_drawdown_pct` −162,28 und Score 0,159.
Die Datei entstand also vor dem Regimefilter, als der Drawdown noch auf
der Blockreihenfolge lief.

Für die Kernfrage zählt dieser historische Stand, und dort lautet die
Antwort **nein**: Sieger unter beiden Maßen ist T3 16/30 / ADX 30 /
Stop 4 % (Block-Score 0,188 / chronologisch 0,083), und das ist auch die
erste Zeile der gespeicherten Datei. Die Live-Kombination
(ADX **20**) ist unter beiden Maßen nicht der Sieger — sie steht dort auf
Rang 3 (Block) bzw. 5 (chronologisch) von 23. Das ist kein Widerspruch:
laut Übergabeprotokoll Abschnitt 3.2 fiel die T3-Wahl über
Positionslimit-Versuche, Regimefilter-Test und Equity-Simulation, nicht
über die erste Zeile des Rasters.

### 2.4 Die beiden Elliott-Bots: Herkunft belegt, Zahl nicht reproduzierbar

`elliott_wave_stocks`: die gespeicherte Rasterausgabe reproduziert
**nicht** (Live-Punkt: 519 gegen 510 Trades, Ø PnL 14,80 % gegen 4,80 %,
Drawdown −33,0 gegen −82,5, Score 10,272 gegen 1,314). Der Grund ist
bekannt und dokumentiert: die Look-Ahead-Korrektur aus PR #26 hat
Einstiegspreise und Wellenauswahl geändert, damit jeden Trade. Die Datei
ist ein Beleg für die **Herkunft** der Wahl, nicht für ihre Zahlen — und
die Herkunft steht ausdrücklich im Kopf von `live_params.py`: „Zigzag 5%,
Stop-Loss 2%, Ziel 0.236, Top 100 Aktien (erste robuste Validierung)",
später „Aktualisiert auf Top 150 Aktien mit Stop-Loss 3%". Die erste
Zeile der gespeicherten Datei ist genau dev 5 % / Stop 3 % / Fib 0,236.

`elliott_wave` (Krypto): seine heutigen Parameter stammen **nicht** aus
dem eigenen Raster, sondern aus `research/elliott_wave_params/` (PR
#28/#30) — dort lag ein weiteres Raster (252 Kombinationen, dev 2–10 %,
Stop 2–12 %) und ein eigenes Urteil über fünf Bedingungen B1–B5. Dessen
Rangfolge benutzte laut dortiger Annahme P-A1 aber **denselben**
`robustness_score` „wörtlich übernommen, damit die Ergebnisse mit den
früheren vergleichbar bleiben" — also denselben Blockreihenfolge-Drawdown.
Abschnitt 4.4 rechnet diese Auswahl noch einmal.

---

## 3. Frage 3 — Wie groß ist der Unterschied je Bot?

Jeweils für den Sieger des Bot-Maßes auf dem Gesamtfenster. „Faktor" ist
`|chronologisch| / |Blockreihenfolge|`.

| Bot | Symbole | Trades | Drawdown Blockreihenfolge | chronologisch (`entry_time`) | realisiert (`exit_time`) | Faktor |
|---|---|---|---|---|---|---|
| `rsi2_crypto` | 18 | 439 | −57,89 | −115,75 | −124,89 | **2,0** |
| `volatility_breakout_crypto` | 20 | 359 | −105,65 | −192,97 | −187,67 | **1,8** |
| `t3_supertrend` (vor Regimefilter) | 18 | 428 | −120,91 | −272,82 | −273,74 | **2,3** |
| `turtle_soup_crypto` | 20 | 1 599 | −164,66 | −629,00 | −645,89 | **3,8** |
| `elliott_wave_stocks` | 137 | 738 | −94,41 | −623,30 | −809,46 | **6,6** |
| `rsi2_mean_reversion` | 147 | 10 342 | −129,53 | −1 200,43 | −1 214,59 | **9,3** |
| `turtle_soup_stocks` | 147 | 12 069 | −163,70 | −2 135,83 | −2 135,83 | **13,1** |
| `volatility_breakout` | 147 | 4 510 | −115,78 | −423,56 | −429,36 | **3,7** |

Der Faktor drei aus `research/elliott_wave_params/` ist **kein
Ausreißer, sondern die Untergrenze**. Er fällt umso größer aus, je mehr
Symbole parallel laufen und je mehr Trades zusammenkommen: bei den
Krypto-Bots (18–20 Symbole) liegt er bei 1,8 bis 3,8, bei den
Aktien-Bots (147 Symbole) bei 3,7 bis 13,1.

Der Mechanismus ist einfach. Hängt man Symbol für Symbol an, wechseln
sich Gewinn- und Verlustphasen verschiedener Märkte ab und kürzen sich
gegenseitig weg; die kumulierte Reihe pendelt um ihre Steigung.
Chronologisch fallen die Verlustphasen **aller** Symbole zusammen — 2020,
2022, der Krypto-Winter —, und genau das ist der Punkt: das gleichzeitige
Verlieren korrelierter Positionen ist das Risiko, das die Kennzahl
messen soll. Die Blockreihenfolge mittelt es heraus.

`exit_time` liegt fast immer noch etwas tiefer als `entry_time` — das ist
plausibel, weil ein Verlust dem Konto zum Ausstieg zufällt, nicht zum
Einstieg. Der Unterschied zwischen beiden ist aber klein gegenüber dem
zur Blockreihenfolge.

---

## 4. Frage 4 — Ändert sich die Rangfolge?

Gerechnet wurde auf **zwei** Fenstern, weil bei den Prototyp-Bots nicht
immer das Gesamtfenster entschieden hat: das Gesamtfenster (wie
`multi_symbol_optimise.py`) und das In-Sample-Fenster des Walk-Forward
(wie `multi_symbol_walk_forward.py`, mit dem `split_all_symbols` und
`TRAIN_SPLIT_RATIO` des jeweiligen Bots).

### 4.1 Die Übersicht

| Bot / Fenster | Kombis, die die Mindestfilter bestehen | Sieger Blockreihenfolge | Sieger chronologisch | kippt? | Block-Sieger stabil über 200 Symbol-Reihenfolgen |
|---|---|---|---|---|---|
| `t3_supertrend` / gesamt, vor Regimefilter | 23 von 81 | T3 16/30 / ADX 30 / Stop 4 % | T3 16/30 / ADX 30 / Stop 4 % | nein | 38,5 % |
| `t3_supertrend` / gesamt, heutiger Code | 64 von 81 | (T3 16/21 / ADX 20 / Stop 2 %) | T3 12/30 / ADX 30 / Stop 4 % | — | 45,5 % |
| `rsi2_crypto` / gesamt | 6 von 18 | SMA 150 / RSI 10 / kein Stop | SMA 150 / RSI 10 / kein Stop | **nein** | 59,5 % |
| `rsi2_crypto` / In-Sample | 6 von 18 | SMA 200 / RSI 5 / kein Stop | SMA 150 / RSI 5 / kein Stop | ja | 85,0 % |
| `turtle_soup_crypto` / gesamt | 8 von 12 | **Donchian 10 / structural** | **Donchian 10 / kein Stop** | **JA** | 94,5 % |
| `turtle_soup_crypto` / In-Sample | 5 von 12 | Donchian 10 / kein Stop | Donchian 10 / kein Stop | nein | 96,0 % |
| `volatility_breakout_crypto` / gesamt | 4 von 4 | Stop 5 % | Stop 5 % | **nein** | 92,5 % |
| `volatility_breakout_crypto` / In-Sample | 4 von 4 | Stop 5 % | Stop 3 % | ja | 63,0 % |
| `elliott_wave_stocks` / gesamt | 17 von 64 | **dev 4 % / Stop 8 % / kein Ziel** | **dev 5 % / Stop 2 % / kein Ziel** | **JA** | **17,5 %** |
| `rsi2_mean_reversion` / gesamt | 6 von 6 | RSI 10 / kein Stop | RSI 5 / kein Stop | ja | 53,0 % |
| `rsi2_mean_reversion` / In-Sample | 2 von 6 | **RSI 5 / kein Stop** | **RSI 5 / kein Stop** | **nein** | 69,5 % |
| `turtle_soup_stocks` / gesamt | 12 von 12 | **Donchian 10 / kein Stop** | **Donchian 10 / Stop 5 %** | **JA** | **30,5 %** |
| `turtle_soup_stocks` / In-Sample | 12 von 12 | Donchian 10 / kein Stop | Donchian 10 / Stop 5 % | ja | 44,0 % |
| `volatility_breakout` / gesamt | 4 von 4 | Stop 8 % | Stop 8 % | **nein** | 40,0 % |
| `volatility_breakout` / In-Sample | 4 von 4 | Stop 8 % | Stop 8 % | nein | 39,5 % |

Fett steht die Zeile, die die Parameterwahl des Bots dokumentiert
getroffen hat. Die Zeile „`t3_supertrend` / heutiger Code" ist in
Klammern, weil die Blockreihenfolge dort nichts mehr ist, was der Bot
rechnet — siehe 2.3.

**Was sich nicht ändert:** die Menge der Kandidaten. Die Mindestfilter
(`MIN_TRADES`, `MIN_SYMBOLS_CONTRIBUTING`, `MIN_AVG_RETURN_PCT`) enthalten
keinen Drawdown; welche Kombinationen überhaupt in die Rangfolge kommen,
ist unter beiden Maßen identisch. Nur ihre Ordnung ändert sich.

### 4.2 Die vier Bots, bei denen es kippt — im Einzelnen

**`turtle_soup_crypto`** — die klarste Umkehr, weil hier ausdrücklich der
„Gesamtzeitraum-beste Score" die Wahl getroffen hat.

| Kombination | Trades | Ø PnL | DD Block | Score Block | DD chrono | Score chrono |
|---|---|---|---|---|---|---|
| Donchian 10 / **structural** (live) | 1 599 | 0,76 % | −164,66 | **0,185** (Rang 1) | −629,00 | 0,048 (Rang 2) |
| Donchian 10 / **kein Stop** | 1 107 | 1,21 % | −249,89 | 0,161 (Rang 2) | −690,20 | **0,058** (Rang 1) |

Bemerkenswert: der eigene Walk-Forward dieses Bots hatte In-Sample
schon „kein Stop" als beste Kombination — der Bericht notierte das als
„plausibel bei einem kleineren Teilfenster". Unter dem chronologischen
Maß verschwindet die Unstimmigkeit: dann wählen **beide** Fenster „kein
Stop". Die Abweichung lag nicht am Fenster, sondern am Maß.

**`turtle_soup_stocks`** — dieselbe Umkehr, in beiden Fenstern.

| Kombination | Trades | Ø PnL | DD Block | Score Block | DD chrono | Score chrono |
|---|---|---|---|---|---|---|
| Donchian 10 / **kein Stop** (live) | 12 069 | 0,69 % | −163,70 | **0,463** (Rang 1) | −2 135,83 | 0,035 (Rang 2) |
| Donchian 10 / **Stop 5 %** | 13 714 | 0,56 % | −160,71 | 0,408 (Rang 2) | −1 605,47 | **0,041** (Rang 1) |

Hier zeigt sich der Mechanismus besonders deutlich: auf der
Blockreihenfolge liegen die beiden Drawdowns praktisch gleich (−163,7
gegen −160,7), chronologisch dagegen 530 Prozentpunkte auseinander. Der
5 %-Stop begrenzt genau das, was die Blockreihenfolge wegmittelt — das
gleichzeitige Verlieren vieler Positionen. Der Kapital-Drawdown bestätigt
das unabhängig (Abschnitt 6): −17,89 % mit Stop gegen −23,35 % ohne.

**`elliott_wave_stocks`** — hier verbessert sich die Live-Kombination.

| Kombination | Trades | Ø PnL | DD Block | Score Block | DD chrono | Score chrono |
|---|---|---|---|---|---|---|
| dev 4 % / Stop 8 % / kein Ziel | 738 | 5,79 % | −94,41 | **1,660** (Rang 1) | −623,30 | 0,251 (Rang 9) |
| dev 5 % / Stop 2 % / kein Ziel | 510 | 3,48 % | −57,50 | 1,367 (Rang 5) | −167,85 | **0,468** (Rang 1) |
| dev 5 % / Stop 3 % / kein Ziel (live) | 510 | 4,80 % | −82,50 | 1,314 (Rang 6) | −259,86 | 0,417 (Rang **2**) |

Der Block-Sieger stürzt auf Rang 9, die Live-Kombination steigt von Rang
6 auf Rang 2. Für diesen Bot spricht der Wechsel des Maßes also **für**
die heutige Einstellung, nicht gegen sie. Und er ist der Bot mit der
unzuverlässigsten Block-Rangfolge überhaupt: in nur 17,5 % von 200
Symbol-Reihenfolgen gewinnt dieselbe Kombination.

**`elliott_wave`** — siehe 4.4.

### 4.3 Die fünf Bots, bei denen es nicht kippt

* **`rsi2_crypto`**: Gesamtfenster-Sieger ist unter beiden Maßen SMA 150 /
  RSI 10 / kein Stop, also die Live-Einstellung — mit 33 % Vorsprung
  unter dem Block-Maß und noch 15 % chronologisch. (Das In-Sample-Fenster
  kippt von SMA 200 auf SMA 150, aber diese Stufe hat die Wahl nicht
  getroffen: der Prototyp-Bericht nennt ausdrücklich die
  Gesamtzeitraum-Tabelle.)
* **`rsi2_mean_reversion`**: der umgekehrte Fall. Das Gesamtfenster kippt
  von RSI 10 auf RSI 5 — aber entschieden hat hier das
  **In-Sample-Fenster** („Beste Kombination: RSI<5, kein Stop",
  Prototyp-Bericht Abschnitt 3), und dort gewinnt RSI 5 unter beiden
  Maßen. Die Live-Wahl bleibt. Nebenbei: unter dem chronologischen Maß
  wählt auch das Gesamtfenster RSI 5, die beiden Stufen wären dann
  erstmals einig.
* **`volatility_breakout`**: Stop 8 % unter beiden Maßen, in beiden
  Fenstern. Allerdings **knapp**: chronologisch nur 2,8 % vor „kein
  Stop" (0,111 gegen 0,108), gegenüber 9,1 % unter dem Block-Maß. Der
  Abstand schrumpft, das Vorzeichen bleibt.
* **`volatility_breakout_crypto`**: Stop 5 % unter beiden Maßen auf dem
  Gesamtfenster, mit 40 % Vorsprung chronologisch. (In-Sample kippt es
  auf Stop 3 %, aber auch hier hat das Gesamtfenster entschieden.)
* **`t3_supertrend`**: siehe 2.3 — im historischen Stand identischer
  Sieger, im heutigen Code rechnet der Bot ohnehin chronologisch.

### 4.4 `elliott_wave`: die Kandidatenliste wechselt komplett

Die heutigen Parameter dieses Bots stammen aus
`research/elliott_wave_params/`. Dort waren die Kandidaten **die fünf
besten In-Sample-Kombinationen plus die damalige Live-Kombination**
(Annahme P-A6), und über diese Kandidaten entschieden dann die fünf
Bedingungen B1–B5.

Dieselbe Rangfolge, einmal mit jedem Drawdown — gerechnet aus den in PR
#28 gespeicherten Rasterdateien, die beide Drawdowns bereits enthalten
(`research/elliott_wave_params/results/<bot>_grid_is.csv`, Spalten
`robustness_score` und `robustness_score_chronologisch`):

| Rang | Kandidatenliste unter der Blockreihenfolge | unter dem chronologischen Drawdown |
|---|---|---|
| 1 | dev 10 % / Stop 6 % / Fib 0,5 (1,069) | dev 10 % / **Stop 2 %** / Fib 0,382 (0,548) |
| 2 | **dev 10 % / Stop 6 % / Fib 0,618 (1,043) ← heute live** | dev 10 % / **Stop 2 %** / Fib 0,5 (0,548) |
| 3 | dev 10 % / Stop 6 % / Fib 0,382 (1,040) | dev 10 % / **Stop 3 %** / Fib 0,5 (0,532) |
| 4 | dev 10 % / Stop 4 % / Fib 0,5 (0,966) | dev 10 % / Stop 4 % / Fib 0,5 (0,511) |
| 5 | dev 10 % / Stop 6 % / Fib 1,0 (0,939) | dev 10 % / **Stop 3 %** / Fib 0,382 (0,503) |

Die Zigzag-Schwelle bleibt bei 10 % — der eigentliche Fund von PR #28
hält also. Der **Stop** wandert von 4–6 % auf 2–4 %, und die heute live
genutzte Kombination (Stop 6 %) fällt aus den Top 5 heraus: sie steht
chronologisch auf **Rang 6 von 37**. Sie wäre unter diesem Maß nicht
Kandidat gewesen.

Was daraus gefolgt wäre, sagt diese Untersuchung **nicht**. Die
Bedingungen B1–B5 (insbesondere B3 „positiver Ø PnL in jeder
Walk-Forward-Falte" und B4 „schlägt Buy-and-Hold im Calmar") hätten die
neuen Kandidaten erst prüfen müssen, und der dortige Bericht hält für
dev 10 % / Stop 4 % ausdrücklich fest, dass er an B2, B3 und B4
scheitert. Über dev 10 % / Stop 2–3 % ist nichts bekannt — diese Punkte
wurden nie bis zum Urteil geführt. Das nachzuholen wäre eine eigene
Aufgabe (Abschnitt 9).

Auf dem **Gesamtfenster** und **Out-of-Sample** wechselt der Sieger
dieses Bots dagegen nicht (dev 10 % / Stop 6 % / Fib 0,618 bzw. dev 10 %
/ Stop 8 % / kein Ziel, jeweils Rang 1 unter beiden Maßen).

Für `elliott_wave_stocks` ist dieselbe Rechnung noch deutlicher: dort
wechselt die In-Sample-Kandidatenliste von „dev 2–6 % / Stop 16 %"
geschlossen auf „**dev 8 %** / Stop 2–16 %", und der
Gesamtfenster-Sieger des Block-Maßes fällt von Rang 1 auf **Rang 43 von
116**.

### 4.5 Das eigene Raster des Krypto-Elliott-Bots

ELLIOTT_WAVE_EIGENES_RASTER

---

## 5. Ist das Rauschen? Die Streuung

Der Auftrag nennt die Messlatte: „Der Elliott-Wave-Bericht zeigt über 200
Permutationen der Zeilenreihenfolge eine Spanne von 297 Prozentpunkten.
Eine Rangfolge, die innerhalb dieser Streuung kippt, ist kein Befund,
sondern Rauschen."

Die 297 Prozentpunkte aus PR #28 sind allerdings eine andere Größe: dort
wurde die **Kapitalrendite** über 200 Vertauschungen gleichzeitiger
Einstiege bei Positionslimit 8 gemessen. Für die hier gestellte Frage
sind zwei andere Streuungen einschlägig, und beide wurden gerechnet:

1. **Die Willkür des Block-Maßes selbst**: 200 zufällige Permutationen
   der Symbol-Blockreihenfolge (die Reihenfolge innerhalb eines Symbols
   bleibt unangetastet — sie ist die Zeit).
2. **Die Rest-Willkür des chronologischen Maßes**: 200 Vertauschungen
   von Trades mit **identischem** `entry_time`. Mehr Willkür als diese
   hat das chronologische Maß nicht.

Beides je Kombination, fester Startwert 20260912.

| Bot (Sieger des Bot-Maßes, Gesamtfenster) | Spanne über 200 Blockreihenfolgen | Spanne über 200 Vertauschungen gleichzeitiger Einstiege | liegt der chronologische Wert in der Block-Spanne? |
|---|---|---|---|
| `rsi2_crypto` | −138,19 .. −54,81 (83 pp) | −122,07 .. −115,38 (6,7 pp) | ja |
| `volatility_breakout_crypto` | −186,09 .. −78,42 (108 pp) | −198,27 .. −192,97 (5,3 pp) | **nein** |
| `t3_supertrend` (vor Regimefilter) | −288,72 .. −91,34 (197 pp) | −272,82 .. −272,82 (0 pp) | ja |
| `turtle_soup_crypto` | −392,40 .. −154,59 (238 pp) | −656,03 .. −626,56 (29 pp) | **nein** |
| `elliott_wave_stocks` | −320,79 .. −87,52 (233 pp) | −623,30 .. −623,30 (0 pp) | **nein** |
| `rsi2_mean_reversion` | −255,63 .. −90,96 (165 pp) | −1 201,12 .. −1 200,43 (0,7 pp) | **nein** |
| `turtle_soup_stocks` | −293,57 .. −162,39 (131 pp) | −2 154,52 .. −2 135,83 (19 pp) | **nein** |

Zwei Ergebnisse, und sie zeigen in dieselbe Richtung:

**Die Rest-Willkür des chronologischen Maßes ist klein** — 0 bis 29
Prozentpunkte, gegenüber Unterschieden zwischen den Maßen von 60 bis
1 970 Prozentpunkten. Die chronologische Zahl ist als Zahl also scharf.

**Die Willkür des Block-Maßes ist groß und verschluckt den Unterschied
nicht.** Ihre Spanne beträgt 83 bis 238 Prozentpunkte — in derselben
Größenordnung wie die 297 aus PR #28 —, aber der chronologische Wert
liegt bei **fünf von sieben** Bots trotzdem **außerhalb** dieser Spanne.
Selbst die günstigste Symbol-Reihenfolge kommt dort nicht an den
chronologischen Wert heran. Bei den beiden Ausnahmen (`rsi2_crypto`,
`t3_supertrend` vor Regimefilter) kippt der Sieger ohnehin nicht.

Die härtere Prüfung ist die dritte Spalte der Tabelle in 4.1: **Wie oft
gewinnt unter 200 Symbol-Reihenfolgen dieselbe Kombination?**

| Bot / Fenster | Block-Sieger stabil | Bewertung |
|---|---|---|
| `turtle_soup_crypto` / gesamt | 94,5 % | stabil — der Sieger kippt hier **nicht** aus Rauschen, sondern weil das Maß etwas anderes misst |
| `volatility_breakout_crypto` / gesamt | 92,5 % | stabil |
| `rsi2_crypto` / gesamt | 59,5 % | wackelig |
| `rsi2_mean_reversion` / gesamt | 53,0 % | wackelig |
| `volatility_breakout` / gesamt | 40,0 % | in 3 von 5 Reihenfolgen gewinnt etwas anderes |
| `turtle_soup_stocks` / gesamt | 30,5 % | die Rangfolge ist überwiegend Zufall der Symbolliste |
| `elliott_wave_stocks` / gesamt | **17,5 %** | in mehr als vier von fünf Reihenfolgen gewinnt eine andere Kombination |

Das ist der eigentliche Befund dieses Abschnitts, und er ist stärker als
die Ausgangsfrage: bei `elliott_wave_stocks`, `turtle_soup_stocks` und
`volatility_breakout` ist die Rangfolge des Block-Maßes **schon gegen die
eigene Symbollisten-Reihenfolge nicht stabil**. Hätte jemand die Zeilen
in `config/sp500_top150.txt` anders sortiert — nach Alphabet statt nach
Marktkapitalisierung —, wäre bei diesen Bots eine andere Kombination
Sieger geworden. Nicht weil die Strategie anders wäre, sondern weil die
Datei anders sortiert ist.

Umgekehrt bei `turtle_soup_crypto`: dort ist der Block-Sieger zu 94,5 %
stabil, und **trotzdem** kippt die Wahl gegen das chronologische Maß.
Das ist der reine Fall: kein Rauschen, sondern zwei Maße, die
verschiedene Dinge messen.

---

## 6. Frage 5 — Welcher Drawdown ist der richtige?

### Die Symbol-Blockreihenfolge: nicht zu verteidigen

Der Satz aus PR #28 gilt uneingeschränkt. Die Reihenfolge entsteht aus
`pd.concat` über `all_data.items()`, also aus der Zeilenfolge von
`config/top25_symbols.txt` bzw. `config/sp500_top150.txt`. Sie ist:

* **kein Verlauf** — der 500. Trade von AAPL steht vor dem ersten von
  MSFT, egal wann sie stattfanden;
* **nicht stabil** — eine andere Sortierung der Symboldatei ergibt einen
  anderen Wert (83–238 pp Spanne, Abschnitt 5) und bei drei Bots einen
  anderen Sieger;
* **systematisch zu klein** — sie mittelt gerade das heraus, was die
  Kennzahl messen soll: das gleichzeitige Verlieren korrelierter
  Positionen. Faktor 1,8 bis 13,1 (Abschnitt 3).

Dazu kommt, dass sie sich nur zufällig noch so verhält: bei
`t3_supertrend` hat eine Sortierzeile in `filter_trades_by_regime` das
Maß bereits stillschweigend zum chronologischen gemacht (2.3). Ein Maß,
das sich durch eine fremde Zeile ändert, ohne dass es jemandem auffällt,
ist als gemeinsame Grundlage über neun Bots ohnehin nicht tragfähig.

### Das Gegenargument: chronologisch ist nicht automatisch richtig

Beide Maße rechnen auf der **Summe der Einzeltrade-Prozente**. Jeder
Trade zählt mit einer ganzen Einheit, obwohl der Bot mit einem
Kapitalanteil je Trade (2–10 %) und meist einem Positionslimit arbeitet.
Der chronologische Wert von `turtle_soup_stocks`, −2 135 %, ist als
Kapitalverlust **unmöglich** — er ist keine erlebbare Zahl, sondern nur
eine besser geordnete.

Den erlebbaren Verlauf hat das Projekt schon, in `equity_simulation.py`
jedes Bots. `kapitalkurve.py` lässt diese echte Rechnung je
Rasterkombination mitlaufen (auf der chronologisch sortierten
Trade-Menge, so wie `collect_all_trades` sie übergibt) und vergleicht die
Rangfolgen:

| Bot | Kombis | Spanne Block | Spanne chrono | Spanne **Kapital** | Rangkorr. \|DD\| zum Kapital-DD: Block | chrono | Sieger Kapital-Calmar |
|---|---|---|---|---|---|---|---|
| `rsi2_crypto` | 6 | −103 .. −56 | −182 .. −83 | **−17,1 .. −9,3** | 0,371 | **0,886** | SMA 150 / RSI 10 / kein Stop = beide Maße |
| `rsi2_mean_reversion` | 6 | −346 .. −130 | −1 602 .. −561 | **−27,1 .. −19,9** | **−0,314** | **0,829** | RSI 5 / kein Stop = **chronologisch** |
| `turtle_soup_crypto` | 8 | −438 .. −165 | −966 .. −427 | **−51,0 .. −35,0** | **−0,333** | 0,690 | Donchian 10 / structural = **Block** |
| `turtle_soup_stocks` | 12 | −185 .. −139 | −2 214 .. −1 387 | **−33,3 .. −17,9** | 0,259 | 0,559 | Donchian 10 / Stop 5 % = **chronologisch** |
| `volatility_breakout` | 4 | −184 .. −113 | −449 .. −373 | **−27,4 .. −14,9** | −0,200 | 0,800 | Stop 3 % = **keines von beiden** |
| `volatility_breakout_crypto` | 4 | −187 .. −106 | −469 .. −168 | **−34,0 .. −14,8** | 0,400 | **1,000** | Stop 5 % = beide Maße |
| `elliott_wave` | 32 | −224 .. −47 | −390 .. −73 | **−32,8 .. −7,2** | 0,871 | **0,983** | dev 10 / Stop 8 / kein Ziel = beide Maße |
| `elliott_wave_stocks` | 116 | −245 .. −53 | −1 269 .. −99 | **−38,3 .. −9,2** | 0,707 | 0,706 | ELLIOTT_STOCKS_KAPITAL_SIEGER |

(Die beiden Elliott-Zeilen stammen aus den in PR #28 gespeicherten
Rasterdateien, die die Kapitalkennzahlen je Kombination schon enthalten;
die übrigen sechs sind hier gerechnet. Bei
`volatility_breakout`/`-_crypto` beruht die Rangkorrelation auf **vier**
Punkten und ist entsprechend wenig belastbar.)

Drei Dinge stehen darin:

1. **Der Kapital-Drawdown bewegt sich in einer völlig anderen
   Größenordnung** — zweistellige Prozente statt drei- bis vierstelliger.
   Keines der beiden Rastermaße ist eine Kapitalkennzahl.
2. **Der chronologische Drawdown ordnet in sieben von acht Fällen
   deutlich näher am Kapital-Drawdown** (0,56 bis 1,00 gegen −0,33 bis
   0,87). Bei `rsi2_mean_reversion`, `turtle_soup_crypto` und
   `volatility_breakout` ist die Korrelation der Blockreihenfolge sogar
   **negativ**: wer dort den Block-Drawdown minimiert, wählt
   systematisch den schlechteren Kapitalverlauf.
3. **Aber er ist nicht die Wahrheit.** Bei `turtle_soup_crypto` stimmt
   der Kapital-Calmar mit dem **Block**-Sieger überein, nicht mit dem
   chronologischen; bei `volatility_breakout` mit keinem von beiden
   (Stop 3 %, den beide Maße auf Rang 3–4 setzen); bei
   `elliott_wave_stocks` sind die beiden Korrelationen praktisch gleich
   (0,707 gegen 0,706).

### Empfehlung

**Kurzfristig: die Blockreihenfolge aufgeben, den chronologischen
Drawdown daneben ausweisen.** Er kostet eine Zeile
(`combined = combined.sort_values("entry_time", kind="stable")` vor der
`cumsum`), ist bei sieben von acht Bots näher am erlebbaren Verlauf, hat
eine kleine Rest-Willkür (0–29 pp statt 83–238 pp) und ist gegen die
Sortierung der Symboldatei unempfindlich. Das ist eine Verbesserung, die
nichts an der Methodik ändert.

**Eigentlich richtig ist aber die Kapitalkurve.** Die Kennzahl, die das
Projekt in seinen Entscheidungen ohnehin als maßgeblich behandelt, ist
der Calmar auf der `equity_simulation`-Kurve — genau der steht in jeder
Buy-and-Hold-Tabelle und in Bedingung B4 von PR #28. Der `robustness_score`
ist ein **Vorfilter** über die Rastersuche, kein Urteil, und seine
Aufgabe ist, aus 252 Kombinationen eine Handvoll Kandidaten zu machen.
Für diese Aufgabe wäre der Kapital-Drawdown die saubere Wahl; er kostet
je Kombination einen Lauf von `simulate_portfolio` (gemessen: 0,1 bis
2 s), also das 1,5- bis 2-Fache der bisherigen Rechenzeit.

**Der Preis, und er gehört benannt.** Ein Wechsel des Bewertungsmaßes
macht **alle** früheren Scores untereinander unvergleichbar. Betroffen
sind: die neun gespeicherten `multi_symbol_optimisation_results.csv`,
alle Score-Angaben in den sechs `PROTOTYPE_FINDINGS.md`, die
Score-Angaben in `results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md`,
die Rangfolgen in `research/elliott_wave_params/` und
`research/elliott_wave_lookahead/`, die Zielfunktion von Agent 2 und die
Score-Zeilen in jedem künftigen Quartalsbericht — der Vergleich „Score
0,118 gegen 0,084" aus Übergabeprotokoll Abschnitt 3.2 wäre dann nicht
mehr mit einem neuen Wert vergleichbar. Das ist derselbe Bruch, den die
Look-Ahead-Korrektur schon einmal erzeugt hat, und er ist teurer als die
eine Sortierzeile aussieht.

Ein mittlerer Weg, der den Bruch vermeidet: **beide Werte ausweisen und
den bisherigen weiter als `robustness_score` führen** — genau, was
`research/elliott_wave_params/` schon getan hat (`max_drawdown_pct` und
`max_drawdown_chronologisch_pct` nebeneinander). Dann bleibt jede alte
Zahl vergleichbar, und jede neue Entscheidung sieht beide. Welcher der
drei Wege genommen wird, entscheidet der Nutzer.

---

## 7. Getroffene Annahmen

**A-1 — „Chronologisch" heißt `entry_time`, stabil sortiert.** Das ist
die Reihenfolge, die `equity_simulation.collect_all_trades` bei allen
neun Bots benutzt (`combined.sort_values("entry_time")`), und damit die,
gegen die PR #28 seinen Vergleich gestellt hat. `kind="stable"` statt der
pandas-Vorgabe, damit gleichzeitige Einstiege reproduzierbar in derselben
Reihenfolge stehen. Weil ein Verlust dem Konto aber erst zum Ausstieg
zufällt, wird `exit_time` **zusätzlich** ausgewiesen; es liegt fast immer
etwas tiefer und ändert keine der Antworten.

**A-2 — Bot-Dateien werden gelesen und als Bibliothek eingebunden, nie
als Programm ausgeführt.** Der Auftrag sagt „Bot-Dateien werden gelesen,
nie importiert" und zugleich „ruft die echten Bot-Funktionen auf … eine
Nachbildung, die abweicht, beantwortet die Frage nicht". Beides zugleich
ist wörtlich nicht möglich. Gewählt wurde der Weg des Vorbilds
(`research/elliott_wave_params/botenv.py`): `import
multi_symbol_optimise` als Bibliothek, wobei der `__main__`-Block des
Bots **nicht** läuft — genau der würde
`results/<bot>/multi_symbol_optimisation_results.csv` überschreiben, und
diese Dateien sind hier Beweismittel. Ein Ausführen der Bot-Skripte findet
nicht statt; dass nichts außerhalb dieses Ordners verändert wurde, weisen
Prüfung 16 und 17 per `git status`/`git diff` nach.

**A-3 — Das Raster ist das des Bots, nicht ein eigenes.** Die
Kombinationen werden aus den `*_RANGE`-Konstanten des jeweiligen
`multi_symbol_optimise.py` abgeleitet (ein Wert, eine Quelle —
Protokoll-Prinzip 11). Ein feineres Raster hätte die Frage verändert:
gefragt ist, ob die **damalige** Auswahl anders ausgefallen wäre.

**A-4 — Das In-Sample-Fenster ist nur dort gerechnet, wo es exakt
ableitbar ist.** Die sechs Prototyp-Bots bilden ihr IS-Fenster über einen
Trade-Filter (`trades[trades["entry_time"] < cutoff_end]`), das ist exakt
nachbildbar. Die drei älteren Bots schneiden die **Kursreihe**
(`df.iloc[:split_idx]`), wodurch sich auch die Indikatoren ändern; dort
wäre eine Ableitung aus der Gesamtmenge falsch, und `analyse.py`
verweigert sie mit Begründung statt sie zu schätzen.

**A-5 — Die APH-Kurslücke berührt diese Zahlen nicht; gemessen, nicht
angenommen.** Erwartet war, dass ein Trade mit `pnl_pct = NaN` die
kumulierte Reihe abbricht. Gemessen (Prüfung 14) gilt das **nicht**:
`Series.cumsum()` überspringt NaN (`skipna=True`), ein solcher Trade
wirkt wie 0, und der Drawdown bleibt unberührt. Über alle Raster hinweg
treten NaN-PnL-Trades nur bei `elliott_wave_stocks` auf (32 Stück, einer
je Kombination — der letzte, leere APH-Balken), und die Drawdowns mit und
ohne diese Trades sind auf zwei Stellen **identisch**: 0 von 64
Kombinationen weichen ab, weder in der Block- noch in der
chronologischen Reihenfolge. Was die Lücke verschiebt, ist `mean()` —
dort fällt der NaN-Trade aus dem Nenner, während `num_trades` ihn
mitzählt. Das ist ein Effekt in der vierten Stelle und ändert keine
Rangfolge. Behoben wird hier nichts; das bleibt die eigene Aufgabe.

**A-6 — Der Score wird mit der gerundeten Eingabe gerechnet**, so wie
der Bot es tut (`round(avg_return, 2)`, `round(max_drawdown, 2)` vor dem
Aufruf). Eine ungerundete Rechnung wäre näher am Ideal, aber nicht mehr
die Zahl, die die Parameterwahl getragen hat.

**A-7 — Die Live-Kombination je Bot ist aus `live_params.py` abgelesen**
und steht in `test_drawdown.py::LIVE` bzw. `uebersicht.py::LIVE_LABEL`.
Sie ist keine Rechengröße, sondern der Bezugspunkt für „ändert sich
etwas". Bei `elliott_wave` liegt sie außerhalb des eigenen Bot-Rasters
(dev 10 % gegen `DEVIATION_RANGE = [2, 3, 4, 5]`) — sie stammt ja aus dem
weiteren Raster von PR #28; deshalb Abschnitt 4.4.

---

## 8. Scope-Grenzen — was diese Untersuchung ausdrücklich nicht beantwortet

* **Sie ändert nichts und empfiehlt keine Übernahme.** Welche
  Kombination künftig live läuft, ist keine Aussage dieses Berichts.
* **Sie sagt nicht, welche Parameter „besser" sind.** Sie sagt nur,
  welche Kombination ein anderes Bewertungsmaß auf **dieselbe**
  Trade-Menge an die Spitze setzt. Ob die dann auch besser handelt,
  entscheidet die volle Kette (Walk-Forward → Equity-Simulation →
  Buy-and-Hold), und die ist hier nicht gelaufen.
* **Sie führt die Bedingungen B1–B5 aus PR #28 nicht neu durch.** Für
  `elliott_wave` (4.4) bedeutet das: die Kandidatenliste wechselt
  belegbar, das **Urteil** über die neuen Kandidaten ist offen.
* **Sie prüft keinen Walk-Forward über mehrere Falten**, keine
  Out-of-Sample-Fenster der sechs Prototyp-Bots und keine
  Buy-and-Hold-Vergleiche.
* **Sie behebt die APH-Kurslücke nicht** (A-5) und rührt den Bot-Code
  nicht an, der sie hat.
* **Sie bewertet die Zielfunktion von Agent 2 nicht neu.** Dass der Score
  auch dessen Suchrichtung bestimmt (Abschnitt 1), ist festgestellt,
  nicht durchgerechnet.
* **Sie prüft nicht, ob das Positionslimit oder der Kapitalanteil je Bot
  richtig gewählt ist.** Der Kapital-Drawdown in Abschnitt 6 ist mit den
  heutigen Live-Werten gerechnet, nicht optimiert.
* **Die Rangkorrelationen für `volatility_breakout` und
  `volatility_breakout_crypto` beruhen auf vier Rasterpunkten** und sind
  als Zahl nicht belastbar; sie stehen dort, damit die Tabelle
  vollständig ist.

---

## 9. Offene Punkte

Beobachtungen, keine Aufträge — die Entscheidung liegt beim Nutzer:

1. **Die vier Bots aus Abschnitt 4.1 durch die volle Validierungskette
   schicken.** Erst dann steht fest, ob die chronologisch besseren
   Kombinationen auch die besseren Bots sind. Für `turtle_soup_crypto`
   und `turtle_soup_stocks` ist das die naheliegendste Folgeaufgabe, weil
   dort jeweils nur der Stop-Modus wechselt.
2. **`elliott_wave`: B1–B5 auf die neue Kandidatenliste anwenden.** dev
   10 % / Stop 2–3 % ist nie bis zum Urteil geführt worden.
3. **Die Sortierzeile in `filter_trades_by_regime` festhalten.** Sie
   bestimmt heute stillschweigend das Bewertungsmaß eines Bots. Wer sie
   je entfernt oder durch etwas anderes ersetzt, ändert damit dessen
   Score — ohne dass irgendein Kommentar davor warnt.
4. **Die gespeicherten `multi_symbol_optimisation_results.csv` sind
   unterschiedlich alt.** Die von `t3_supertrend` stammt von vor dem
   Regimefilter, die von `elliott_wave_stocks` von vor der
   Look-Ahead-Korrektur. Beide werden in Berichten weiter als aktuelle
   Zahlen zitiert. Ein Datum im Dateikopf oder eine Zeile im jeweiligen
   Findings-Dokument würde das entschärfen.
5. **Wenn das Maß wechselt, wechselt es an 18 Stellen plus zwei
   außerhalb von `strategies/`** (Abschnitt 1). Eine gemeinsame Funktion
   in `shared/` wäre der Ort dafür — dieselbe Überlegung wie bei
   `live_params.py` und `empfehlung_format.py`.
6. **`volatility_breakout`: der Kapital-Calmar bevorzugt Stop 3 %**, den
   beide Rastermaße auf Rang 3–4 setzen. Das ist kein
   Reihenfolge-Befund, sondern ein Hinweis, dass der Vorfilter bei diesem
   Bot in eine andere Richtung zeigt als die Kapitalkurve. Eigene Frage.

---

## 10. Dateien

| Datei | Rolle |
|---|---|
| `botenv.py` | Bot-Umgebung je Prozess, Stubs (werfen bei Aufruf), fester Hinweis |
| `engine.py` | die vier Drawdowns, der Score über die Bot-Funktion, die Permutationen |
| `adapters.py` | je Bot: sein Raster, seine Trade-Sammlung, sein Gegenprobe-Aufruf |
| `analyse.py` | Hauptlauf je Bot und Fenster → `<bot>[_fenster]_raster.csv` + `_ergebnis.json` |
| `historie.py` | Zeilenvergleich gegen die gespeicherte Bot-Ergebnisdatei (Frage 2) |
| `kapitalkurve.py` | Gegencheck gegen `equity_simulation` (Frage 5) |
| `einzelsymbol.py` | sind die Einzelsymbol-Optimierer betroffen? (Frage 1) |
| `uebersicht.py` | fasst alle `*_ergebnis.json` zu den Tabellen dieses Berichts zusammen |
| `test_drawdown.py` | Selbsttests gegen den Bot-Code, mit fünf Gegenproben |
| `run_all.py` | alles nacheinander, ein Prozess je Bot und Schritt |
| `results/<bot>[_fenster]_raster.csv` | jede Rasterkombination mit allen vier Drawdowns und Scores |
| `results/<bot>[_fenster]_ergebnis.json` | Rangfolgen je Maß, Rangwechsel, Streuung, Urteil |
| `results/<bot>_kapitalkurve.csv/.json` | Kapitalkennzahlen je Kombination und die Rangkorrelationen |
| `ERGEBNIS.md` | die Kurzfassung zum Kopieren |

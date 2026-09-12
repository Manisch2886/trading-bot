# Drawdown-Reihenfolge: Ergebnis auf einer Seite

**Untersuchung, keine Korrektur.** Es wurde nichts geändert — kein
`live_params.py`, kein `forward_test.py`, kein `equity_simulation.py`,
kein `multi_symbol_optimise.py`, keine Bot-Ergebnisdatei. Ob etwas
geändert wird, entscheidet der Nutzer. Vollständiger Bericht:
`research/drawdown_reihenfolge/BERICHT.md`.

---

## 1. Die Kernfrage: Ändert sich eine Parameterwahl? — Ja, bei vier von neun Bots

| Bot | heute live | Wahl unter dem erlebbaren (chronologischen) Drawdown |
|---|---|---|
| **`turtle_soup_crypto`** | Donchian 10 / Stop **structural** | Donchian 10 / **kein Stop** |
| **`turtle_soup_stocks`** | Donchian 10 / **kein Stop** | Donchian 10 / **Stop 5 %** |
| **`elliott_wave_stocks`** | dev 5 % / Stop 3 % / kein Ziel | dev 5 % / **Stop 2 %** / kein Ziel — die Live-Einstellung **verbessert** sich dabei von Rang 6 auf Rang 2 |
| **`elliott_wave`** | dev 10 % / Stop 6 % / Fib 0,618 | die Kandidatenliste, aus der diese Wahl stammt (PR #28), enthält sie nicht mehr: die In-Sample-Top-5 rutschen von Stop 4–6 % auf Stop **2–4 %**. Die Zigzag-Schwelle von 10 % hält |

**Unverändert bleibt es bei fünf Bots:** `rsi2_crypto`,
`rsi2_mean_reversion`, `volatility_breakout`,
`volatility_breakout_crypto` und `t3_supertrend`.

Drei Einzelfälle, die zum Bild gehören:

* **`rsi2_mean_reversion`** kippt auf dem Gesamtfenster (RSI 10 → RSI 5),
  aber entschieden hat bei diesem Bot das In-Sample-Fenster des
  Walk-Forward — und dort gewinnt RSI 5 unter **beiden** Maßen. Die
  Live-Wahl bleibt, und die beiden Stufen wären unter dem
  chronologischen Maß erstmals einig.
* **`elliott_wave`**: sein **eigenes** Raster (dev 2–5 %, Stop 2–4 %)
  liefert auf kausal sauberer Grundlage **keine einzige** zulässige
  Kombination — alle 36 scheitern an `MIN_AVG_RETURN_PCT = 2.0`. Dort
  stellt sich die Frage also gar nicht; entschieden hat das weitere
  Raster aus PR #28.
* **`t3_supertrend`** rechnet heute schon chronologisch — aber
  versehentlich: `regime_filter.filter_trades_by_regime` sortiert
  intern nach `entry_time`, weil `pd.merge_asof` das braucht. Gemessen
  über alle 81 Rasterkombinationen: `dd_bot == dd_entry`, kein einziges
  Mal `dd_bot == dd_block`. Zur Zeit seiner Parameterwahl war das noch
  nicht so; dort kippt der Sieger aber ebenfalls nicht.

---

## 2. Das ist kein Rauschen — und der eigentliche Befund ist größer

Gefragt war, ob die Rangfolge innerhalb der bekannten Streuung kippt.
Gemessen wurden 200 Permutationen der Symbol-Blockreihenfolge je
Kombination (fester Startwert):

* Der chronologische Drawdown liegt bei **13 von 15** gerechneten
  Bot-Fenstern **außerhalb** dieser Spanne (über alle 177 zulässigen
  Kombinationen: 140 von 177). Selbst die günstigste Symbol-Reihenfolge
  kommt dort nicht an ihn heran.
* Die Rest-Willkür des chronologischen Maßes (Vertauschung gleichzeitiger
  Einstiege) beträgt **0 bis 29 Prozentpunkte** — gegenüber
  Unterschieden zwischen den Maßen von 58 bis 1972 Prozentpunkten.

Die härtere Prüfung ist die Gegenrichtung: **Wie oft gewinnt unter 200
Symbol-Reihenfolgen dieselbe Kombination?**

| Bot | Block-Sieger stabil |
|---|---|
| `turtle_soup_crypto` | 94,5 % |
| `volatility_breakout_crypto` | 92,5 % |
| `rsi2_crypto` | 59,5 % |
| `rsi2_mean_reversion` | 53,0 % |
| `volatility_breakout` | 40,0 % |
| `t3_supertrend` (vor Regimefilter) | 38,5 % |
| `elliott_wave_stocks` | **34,5 %** |
| **`turtle_soup_stocks`** | **30,5 %** |

Bei `turtle_soup_stocks`, `elliott_wave_stocks` und
`volatility_breakout` ist die Rangfolge des heutigen Maßes **schon gegen
die Sortierung der eigenen Symboldatei nicht stabil**. Wäre
`config/sp500_top150.txt` alphabetisch statt nach Marktkapitalisierung
sortiert, wäre dort eine andere Kombination Sieger geworden. Nicht weil
die Strategie anders wäre, sondern weil die Datei anders sortiert ist.

Bei `turtle_soup_crypto` ist es umgekehrt: der Block-Sieger ist zu
94,5 % stabil — und kippt trotzdem gegen das chronologische Maß. Das ist
der reine Fall: kein Rauschen, sondern zwei Maße, die verschiedene Dinge
messen.

---

## 3. Wie groß ist der Unterschied? Faktor drei war die Untergrenze

Sieger des Bot-Maßes je Bot, Gesamtfenster:

| Bot | Symbole | Drawdown heute | chronologisch | Faktor |
|---|---|---|---|---|
| `volatility_breakout_crypto` | 20 | −105,65 | −192,97 | 1,8 |
| `rsi2_crypto` | 18 | −57,89 | −115,75 | 2,0 |
| `t3_supertrend` (vor Regimefilter) | 18 | −120,91 | −272,82 | 2,3 |
| `volatility_breakout` | 147 | −115,78 | −423,56 | 3,7 |
| `turtle_soup_crypto` | 20 | −164,66 | −629,00 | 3,8 |
| `elliott_wave_stocks` | 137 | −94,41 | −623,30 | 6,6 |
| `rsi2_mean_reversion` | 147 | −129,53 | −1 200,43 | 9,3 |
| `turtle_soup_stocks` | 147 | −163,70 | −2 135,83 | **13,1** |

Der Krypto-Elliott-Bot fehlt: sein eigenes Raster liefert keine
zulässige Kombination. Für seine Live-Kombination aus PR #28 gilt
−56,22 gegen −93,50, also Faktor 1,7.

Der Faktor wächst mit der Zahl parallel laufender Symbole. Grund:
chronologisch fallen die Verlustphasen **aller** Symbole zusammen — und
genau dieses gleichzeitige Verlieren korrelierter Positionen ist das
Risiko, das die Kennzahl messen soll. Die Blockreihenfolge mittelt es
heraus.

---

## 4. Welcher Drawdown ist der richtige? — Nicht so einfach wie erwartet

**Die Symbol-Blockreihenfolge ist nicht zu verteidigen.** Sie ist kein
Verlauf, nicht stabil gegen die Sortierung der Symboldatei, systematisch
zu klein, und sie hat sich bei einem Bot schon durch eine fremde
Sortierzeile stillschweigend geändert.

**Aber der chronologische Drawdown ist auch nicht die Wahrheit.** Beide
Maße addieren Einzeltrade-Prozente zu je einer ganzen Einheit, obwohl
der Bot mit 2–10 % Kapital je Trade und meist einem Positionslimit
arbeitet. −2135 % ist als Kapitalverlust unmöglich.

Den erlebbaren Verlauf hat das Projekt längst: `equity_simulation.py`.
Gegen deren Kapital-Drawdown gemessen (Rangkorrelation der Beträge):

| Bot | Blockreihenfolge | chronologisch |
|---|---|---|
| `volatility_breakout_crypto` | 0,400 | **1,000** |
| `elliott_wave` | 0,871 | **0,983** |
| `rsi2_crypto` | 0,371 | **0,886** |
| `rsi2_mean_reversion` | **−0,314** | **0,829** |
| `volatility_breakout` | −0,200 | **0,800** |
| `turtle_soup_crypto` | **−0,333** | 0,690 |
| `elliott_wave_stocks` | 0,265 | 0,645 |
| `turtle_soup_stocks` | 0,259 | 0,559 |

Bei drei Bots steht das heutige Maß in **umgekehrtem** Verhältnis zum
echten Kapital-Drawdown (`rsi2_mean_reversion`, `turtle_soup_crypto`,
`volatility_breakout`): wer es dort minimiert, wählt systematisch den
schlechteren Kapitalverlauf. Näher am Kapital-Drawdown als die
chronologische Reihenfolge liegt es bei **keinem** Bot.

Das Gegenargument bleibt trotzdem stehen: bei `turtle_soup_crypto`
stimmt der Kapital-Calmar mit dem **Block**-Sieger überein, bei
`volatility_breakout` mit **keinem** von beiden, und bei
`elliott_wave_stocks` sind beide Korrelationen praktisch gleich.

### Drei Wege, zur Auswahl

1. **Nur die Blockreihenfolge aufgeben** — eine Zeile
   (`sort_values("entry_time", kind="stable")` vor der `cumsum`). Näher
   am erlebbaren Verlauf, scharfe Zahl, unempfindlich gegen die
   Symbolliste.
2. **Auf den Kapital-Drawdown umstellen** — die Kennzahl, die das
   Projekt in seinen Entscheidungen ohnehin als maßgeblich behandelt
   (Calmar in jeder Buy-and-Hold-Tabelle). Kostet je Kombination einen
   Lauf von `simulate_portfolio`, gemessen das 1,5- bis 2-Fache der
   Rechenzeit.
3. **Beide Werte ausweisen, den bisherigen weiter als `robustness_score`
   führen** — so wie `research/elliott_wave_params/` es schon tut. Dann
   bleibt jede alte Zahl vergleichbar, und jede neue Entscheidung sieht
   beide.

**Der Preis von Weg 1 und 2 gehört benannt:** ein Wechsel des
Bewertungsmaßes macht alle früheren Scores untereinander
unvergleichbar — die neun gespeicherten
`multi_symbol_optimisation_results.csv`, alle Score-Angaben in den sechs
`PROTOTYPE_FINDINGS.md` und in `EXPERIMENT_FINDINGS.md`, die Rangfolgen
in `research/elliott_wave_params/` und `research/elliott_wave_lookahead/`,
die Zielfunktion von Agent 2 und jede Score-Zeile künftiger
Quartalsberichte. Derselbe Bruch, den die Look-Ahead-Korrektur schon
einmal erzeugt hat.

---

## 5. Wie belastbar ist das?

* **Keine eigene Backtest-Kopie.** Trades, Score, Mindestfilter, Raster,
  Fenster-Split und Kapitalsimulation kommen aus den **echten
  Bot-Funktionen**.
* **18 von 18 Selbsttests** je Bot, darunter fünf **Gegenproben** (eine
  vertauschte Blockreihenfolge bricht die Gleichheit mit dem Bot, eine
  falsche Score-Formel weicht ab, …).
* **Bitgenaue Reproduktion der gespeicherten Bot-Ergebnisdateien** bei
  sechs Bots (alle sieben Spalten, alle Zeilen); bei `t3_supertrend`
  bitgenau nach Abschalten des später hinzugefügten Regimefilters — was
  gleichzeitig belegt, dass jene Datei aus der Zeit vor dem Filter
  stammt.
* **Der Auslöser dieser Untersuchung ist unabhängig bestätigt**:
  `elliott_wave_stocks` bei dev 5 % / Stop 3 % ergibt −82,50 % gegen
  −259,86 % — genau die −82,5 gegen −259,9 aus
  `research/elliott_wave_params/BERICHT.md`. Und für die
  Live-Kombination des Krypto-Elliott-Bots treffen alle sieben dort
  gespeicherten Zahlen bis auf die letzte Stelle: 130 Trades, Ø 4,19 %,
  Drawdown −56,22 (Score 0,850) und chronologisch −93,50 (Score 0,511).
  Zwei getrennt gebaute Nachbildungen, dasselbe Ergebnis.
* **Gerechnet nach PR #81** (Kurslücken im Trade-Pfad), der während
  dieser Untersuchung in `main` gemergt wurde und `load_all_symbol_data`
  aller neun Bots ändert. Wirkung gemessen: im ganzen `data/`-Ordner ist
  **eine** Kerze betroffen (APH, letzter Balken); für acht Bots sind die
  Raster-CSVs vor und nach dem Merge byteweise identisch; bei
  `elliott_wave_stocks` bleiben Trade-Zahl, Trefferquote, alle vier
  Drawdowns und beide Sieger gleich, sechs von 64 Ø-PnL-Werten
  verschieben sich um 0,01 Prozentpunkte, `num_nan_pnl` fällt von 32 auf
  0. Alle Selbsttests bestehen auch gegen den geänderten Bot-Code.
* **Eine abgeleitete Zahl ist selbst empfindlich:** der Stabilitätsanteil
  von `elliott_wave_stocks` springt durch diese 0,01 Prozentpunkte von
  17,5 % auf 34,5 %. Die qualitative Aussage bleibt dieselbe — in der
  Mehrheit der Reihenfolgen gewinnt eine andere Kombination —, aber der
  Einzelwert sollte nicht auf die Stelle genau gelesen werden.
* **Dünn**: `volatility_breakout` und `volatility_breakout_crypto` haben
  nur vier Rasterpunkte; deren Rangkorrelationen sind nicht belastbar.
* **Nicht reproduzierbar** ist die historische Rasterausgabe von
  `elliott_wave_stocks` — die Look-Ahead-Korrektur (PR #26) hat dessen
  Trades vollständig verändert.

---

## 6. Was diese Untersuchung nicht beantwortet

* Ob die chronologisch besseren Kombinationen auch die besseren Bots
  sind. Dafür bräuchte es die volle Kette (Walk-Forward →
  Equity-Simulation → Buy-and-Hold), und die ist hier nicht gelaufen.
* Bei `elliott_wave`: die Kandidatenliste wechselt belegbar, das
  **Urteil** über die neuen Kandidaten (Bedingungen B1–B5 aus PR #28)
  ist offen. dev 10 % / Stop 2–3 % wurde nie bis zum Urteil geführt.
* Sie behebt die APH-Kurslücke nicht und rührt den Bot-Code nicht an.
* Sie bewertet die Zielfunktion von Agent 2 nicht neu, obwohl der Score
  auch dessen Suchrichtung bestimmt.

---

## 7. Reproduktion

```
cd research/drawdown_reihenfolge
python3 run_all.py                                 # alles, rund 2,5 Stunden
python3 test_drawdown.py turtle_soup_crypto        # Selbsttests
python3 analyse.py turtle_soup_crypto              # Raster, Gesamtfenster
python3 analyse.py turtle_soup_crypto --fenster is # Raster, In-Sample
python3 historie.py turtle_soup_crypto             # gegen die gespeicherte Datei
python3 kapitalkurve.py turtle_soup_crypto         # gegen den Kapitalverlauf
python3 uebersicht.py                              # alle Tabellen
```

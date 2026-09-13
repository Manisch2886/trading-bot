# Übergabe: TB-18 — beide Drawdown-Masse (Schritt M1)

**Stand: 2026-09-13** · Branch `claude/new-session-lk19ti` · Basis `main`
Umsetzung von **M1** aus `research/drawdown_reihenfolge/BERICHT.md`.

---

## 1. Die Zusicherung

> **Der bestehende `robustness_score` und die Rangfolge sind unverändert —
> für alle neun Bots belegt, am Verhalten geprüft, nicht am Diff.**

Zwei unabhängige Nachweise:

**(a) Am Verhalten, alle neun Bots, ohne Kursdaten.** Derselbe Bot bewertet
zweimal dieselbe Trade-Menge: einmal mit den ursprünglichen `entry_time`-Werten,
einmal mit **denselben** Zeitstempeln, nur anders auf die Zeilen verteilt. PnL,
Zeilenreihenfolge und Trade-Anzahl bleiben Zeile für Zeile gleich. Ergebnis:
`robustness_score`, `max_drawdown_pct` und **jede** weitere Spalte sind
identisch, die Reihenfolge der Zeilen ebenso — während sich
`max_drawdown_chronologisch_pct` nachweislich unterscheidet (sonst prüfte der
Vergleich nichts, und auch das prüft der Test).

**(b) An echten Kursdaten, gegen die Zahlen von vorher.** Die Raster in
`research/drawdown_reihenfolge/results/*_raster.csv` sind **vor** dieser
Änderung entstanden. Für je eine Rasterkombination je Bot liefert der geänderte
Code weiterhin denselben `max_drawdown_pct` (`dd_bot`) und denselben
`robustness_score` (`score_bot`) — und als neuen Wert genau das dort
ausgewiesene `dd_entry`:

| Bot | geprüfte Kombination | `max_drawdown_pct` (= vorher) | neu: chronologisch |
|---|---|---|---|
| `elliott_wave` | dev 2 % / Stop 2 % / Fib 0.236 | −993,19 | −996,75 |
| `t3_supertrend` | T3 8/21 / ADX 20 / Stop 3 % | −296,68 | −296,68 |
| `rsi2_crypto` | SMA 100 / RSI 5 / kein Stop | −87,24 | −82,70 |
| `turtle_soup_crypto` | Donchian 10 / kein Stop | −249,89 | −690,20 |
| `volatility_breakout_crypto` | Stop 3 % | −142,91 | −168,38 |
| `elliott_wave_stocks` | dev 5 % / Stop 3 % / kein Ziel | **−82,50** | **−259,86** |
| `rsi2_mean_reversion` | RSI 5 / kein Stop | −166,97 | −560,70 |
| `turtle_soup_stocks` | Donchian 10 / kein Stop | −163,70 | −2 135,83 |
| `volatility_breakout` | Stop 3 % | −184,12 | −373,39 |

Die Zeile für `elliott_wave_stocks` ist der Ankerwert, den der Bericht nennt.

---

## 2. Was geändert wurde

**Neun Dateien** `strategies/*/multi_symbol_optimise.py`, je dieselbe Ergänzung:

```python
    chronologisch = combined.sort_values("entry_time", kind="stable")
    cum_chrono = chronologisch["pnl_pct"].cumsum()
    max_drawdown_chrono = (cum_chrono - cum_chrono.cummax()).min()
```

und, **nach** dem Setzen des `robustness_score`:

```python
    result["max_drawdown_chronologisch_pct"] = round(max_drawdown_chrono, 2)
```

* Der Name ist aus `research/elliott_wave_params/engine.py` **übernommen**, wo
  beide Drawdowns schon nebeneinander stehen.
* Die neue Spalte steht **hinter** `robustness_score` — die bisherige
  Spaltenreihenfolge der `multi_symbol_optimisation_results.csv` bleibt damit
  unverändert, alte und neue Dateien lassen sich Spalte für Spalte vergleichen.
* Bei den drei Bots mit „Beste Kombination"-Block (`elliott_wave`,
  `elliott_wave_stocks`, `t3_supertrend`) zeigt eine zusätzliche Zeile beide
  Masse nebeneinander.
* `kind="stable"` ist gesetzt (Befund **N1** der Untersuchung) und im Test
  eigens abgesichert.

**Kein `robustness_score_chronologisch`.** Der Auftrag nennt einen Wert; die
Zahl ist aus `avg_return_pct`, `num_trades` und dem neuen Drawdown exakt
ableitbar. Eine zweite Score-Spalte wäre die Einladung, nach ihr zu sortieren —
das gehört zu M2 und der Entscheidung danach.

**Neu: `shared/test_drawdown_beide_masse.py`** (Selbsttest, 181 Prüfungen) und
**`docs/TESTAUFTRAG_drawdown_beide_masse.md`** (eigenständig ausführbar).

---

## 3. Sind die neun `multi_symbol_optimise.py` identisch?

**Nein.** Neun verschiedene Dateien, 143 bis 234 Zeilen, neun verschiedene
Prüfsummen — schon vor dieser Änderung.

| Baustein | Fassungen |
|---|---|
| `calculate_robustness_score` | **1** (identisch in allen neun; `rsi2_crypto` hat zusätzlich einen Docstring) |
| `evaluate_combination_multi` | **9** (eigene Parameterlisten; `t3_supertrend` mit BTC-Regimefilter, sechs Bots mit `avg_holding_days`) |
| `run_multi_optimisation` | **8** (`turtle_soup_crypto` und `turtle_soup_stocks` teilen eine Fassung) |

Die betroffene Stelle selbst — die zwei Zeilen der Drawdown-Berechnung — stand
in allen neun **zeichengleich** da; deshalb ist die Ergänzung überall dieselbe.
**Vereinheitlicht wurde nichts**; das wäre eine eigene Entscheidung.

---

## 4. Rechenzeit — gemessen

**Der zusätzliche Schritt selbst** (stabile Sortierung + `cumsum`/`cummax`),
isoliert gemessen auf Trade-Mengen in der Breite, die die Bots tatsächlich
führen (Median aus 25 Läufen):

| Trades je Kombination | Zusatzschritt |
|---|---|
| 205 | 0,5 ms |
| 1 107 | 0,6 ms |
| 1 786 | 0,7 ms |
| 4 821 | 1,1 ms |
| 12 069 (grösste Menge im Projekt) | **2,1 ms** |

**Von Ende zu Ende**, dieselbe Rasterkombination mit der alten und der neuen
Datei, je fünf Läufe, Median (zwei unabhängige Messreihen, wo angegeben):

| Bot | Trades | vorher | nachher |
|---|---|---|---|
| `turtle_soup_stocks` | 12 069 | 0,929 / 0,917 s | 0,958 / 0,951 s |
| `rsi2_mean_reversion` | 5 391 | 0,999 / 1,005 s | 1,016 / 1,057 s |
| `volatility_breakout` | 4 821 | 0,917 / 0,924 s | 0,956 / 0,947 s |
| `t3_supertrend` | 1 152 | 0,688 s | 0,694 s |
| `turtle_soup_crypto` | 1 107 | 0,075 / 0,081 s | 0,078 / 0,084 s |
| `volatility_breakout_crypto` | 379 | 0,142 / 0,144 s | 0,153 / 0,138 s |
| `rsi2_crypto` | 205 | 0,130 / 0,127 s | 0,128 / 0,126 s |

**Nicht spürbar — und die Ende-zu-Ende-Zahlen sind vorsichtig zu lesen.** Die
Unterschiede liegen bei wenigen Prozent und zeigen in beide Richtungen (bei
`rsi2_crypto` und `volatility_breakout_crypto` misst der neue Code in je einer
Reihe schneller). Das ist Laufzeitrauschen zwischen Prozessen: der Schritt
selbst kostet nach der isolierten Messung höchstens **2 ms** je Kombination,
die Ende-zu-Ende-Differenzen sind zehnmal grösser als das. Über ein ganzes
Raster gerechnet: 12 Kombinationen × 2 ms = **25 ms** beim teuersten Bot.

**Zwei Anmerkungen zur Methode.** Erstens kehrt `evaluate_combination_multi`
für Kombinationen, die den **Mindestfilter** nicht bestehen, zurück, *bevor* der
Drawdown gerechnet wird — solche Kombinationen taugen für diese Messung nicht
und sind hier keine. Zweitens liess sich `elliott_wave` deshalb nicht messen:
**keine** seiner Kombinationen besteht die eigenen Mindestfilter. Bei ihm gehen
von ~175 s je Kombination praktisch alle in die Wellenerkennung; der
Zusatzschritt auf seinen 2 057 Trades liegt nach obiger Tabelle unter 1 ms.
`elliott_wave_stocks` (1 786 Trades, ~23 s je Kombination) zeigt dasselbe Bild:
die Differenz verschwindet im Rauschen der Wellenerkennung.

Zum Vergleich: für den **Kapital**-Drawdown — das Mass, das der Bericht als
eigentlich richtiges nennt — nennt die Untersuchung das **1,5- bis 2-Fache**
der bisherigen Rechenzeit.

---

## 5. Tests

```bash
python3 shared/test_drawdown_beide_masse.py          # ca. 7 Minuten
python3 shared/test_drawdown_beide_masse.py --ohne-kursdaten   # ca. 1 Minute
```

Aufbau (Einzelheiten im Testauftrag):

| Abschnitt | prüft | Umfang |
|---|---|---|
| 1 | **die Zusicherung**: Score, Werte und Rangfolge hängen nicht an `entry_time` | 7 Prüfungen × 9 Bots |
| 2 | der neue Wert **ist** der chronologische Drawdown (konstruierter Fall: −14 gegen −24, zusätzlich in reinem Python gegengerechnet) | 5 × 9 |
| 3 | **stabile Sortierung** bei gleichen Zeitstempeln, inklusive Nachweis, dass der Fall überhaupt unterscheidet | 5 × 9 |
| 4 | **Mutationsproben**: jede Wache einzeln entfernt, die zugehörige Prüfung muss anschlagen | 3 × 9 |
| 5 | Gegenprobe an echten Kursdaten gegen `research/drawdown_reihenfolge/` | 6 × 9 |
| 6 | `git status` vor und nach dem Lauf identisch | 1 |

Zur Falle „selbstbestätigende Probe": nirgends wird ein Ergebnis von Hand
hingeschrieben und wiedererkannt. Die Vergleichswerte kommen aus einem zweiten
Lauf desselben Bots, aus einer Gegenrechnung in reinem Python ohne
`cumsum`/`cummax`, aus einer von Hand nachrechenbaren Konstruktion oder aus den
vor der Änderung entstandenen Ergebnisdateien der Untersuchung. Zur Falle
„zweite Wache verdeckt die erste": Abschnitt 2 fällt schon durch, wenn gar nicht
sortiert wird, sagt aber nichts über Gleichstände; Abschnitt 3 kann **nur** über
die stabile Sortierung bestehen; Abschnitt 1 fällt nur, wenn der alte Wert an
`entry_time` hängt. Abschnitt 4 belegt am Verhalten, dass all das greift.

**Bestehende Tests.** Unverändert bestanden: `broker/test_broker.py` (163/163),
`notifications/test_manual_close.py` (118), `.../test_schliess_benachrichtigung.py`
(99/99), `shared/test_empfehlung_format.py` (70/70),
`shared/test_ergebniskurven.py` (44/44), `shared/test_live_params_werte.py`
(69/69), `system/test_caffeinate_plist.py` (53/53),
`system/test_log_rotation.py` (117/117), `system/test_dienst_plists.py`
(Rückgabewert 2 = 0 Fehler, 4 offen — wie vorher).

**Vorbestehende Fehlschläge dieser Cloud-Umgebung**, mit Basislauf auf
unverändertem `main` nachgewiesen und von dieser Änderung nicht berührt:
`dashboard/test_dashboard.py` (kein `fastapi`), `dashboard/test_portfolio_sicht.py`
(2 von 68, kein `node`/`fastapi`), `broker/test_ibkr.py` (keine Zeitzonendaten),
`shared/test_kursdaten.py` (fehlende Bot-Abhängigkeiten).

---

## 6. Nicht angefasst

`live_params.py`, `forward_test.py`, `equity_simulation.py`, jede gespeicherte
`multi_symbol_optimisation_results.csv`, die Formel des `robustness_score`,
alles unter `broker/`, Crontab und launchd-Vorlagen.
`research/drawdown_reihenfolge/` wurde **gelesen**.

---

## 7. Was als Nächstes ansteht

1. **M2** — volle Kette (Backtest → Walk-Forward → Equity-Simulation →
   Buy-and-Hold) für die vier Bots, deren Wahl unter dem chronologischen Mass
   kippen würde: `turtle_soup_crypto`, `turtle_soup_stocks`,
   `elliott_wave_stocks`, `elliott_wave`.
2. **Danach die Entscheidung**, welches Mass führt. Ab jetzt liefert jede
   Optimierung beide Zahlen.

**Zwei Beobachtungen am Rand, nicht Gegenstand dieser Aufgabe:**

* `t3_supertrend` rechnet **heute schon** chronologisch — sein Regimefilter
  sortiert nach `entry_time`, bevor der Drawdown gebildet wird. Beide Werte sind
  dort gleich (−296,68). Der Bericht hält denselben Befund fest.
* `docs/UEBERSICHT_RESEARCH.md` (Stand 12.09.2026) kennt
  `research/drawdown_reihenfolge/` noch nicht — dort stehen 18 Ordner, `ls`
  zeigt inzwischen 19. Ebenso fehlt die Untersuchung in
  `docs/UEBERGABEPROTOKOLL.md`. Bewusst nicht nachgetragen: das wäre eine
  eigene Aufgabe mit eigener Sorgfalt.
* Befund **N1** der Untersuchung (`sort_values` ohne `kind="stable"` in
  `portfolio_correlation_analysis.py` und `shared/portfolio_overview.py`, dort
  0,07 Prozentpunkte) bleibt offen. Die neue Stelle ist von Anfang an stabil
  sortiert.

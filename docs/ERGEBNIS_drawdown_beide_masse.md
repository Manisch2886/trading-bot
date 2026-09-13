# Ergebnis: beide Drawdown-Masse werden ausgewiesen (TB-18 / Schritt M1)

**Stand: 2026-09-13** · Umsetzung von Schritt **M1** aus
`research/drawdown_reihenfolge/BERICHT.md`. **Kein Mass wurde gewechselt, keine
Parametrisierung geändert, keine gespeicherte Ergebnisdatei überschrieben.**

---

## Die Zusicherung zuerst

> **Der `robustness_score` und die Rangfolge sind unverändert — belegt für alle
> neun Bots, am Verhalten geprüft, nicht am Diff.**

Wer heute optimiert, bekommt dieselben Parameter wie gestern. Jede frühere
Score-Angabe bleibt mit jeder neuen vergleichbar; der Bruch, den ein
Masswechsel erzeugt hätte, ist nicht eingetreten.

Der Nachweis läuft auf zwei unabhängigen Wegen:

1. **Am Verhalten, ohne Kursdaten, für alle neun Bots.** Derselbe Bot bewertet
   zweimal dieselbe Trade-Menge — einmal mit den ursprünglichen
   `entry_time`-Werten, einmal mit denselben Zeitstempeln, nur anders auf die
   Zeilen verteilt. PnL, Zeilenreihenfolge und Trade-Zahl sind Zeile für Zeile
   gleich. Ergebnis: `robustness_score`, `max_drawdown_pct`, jede weitere Spalte
   und die gesamte Rangfolge sind in beiden Läufen identisch — während sich der
   neue Wert nachweislich unterscheidet.

2. **An echten Kursdaten, gegen die Zahlen von vorher.** Die Untersuchung
   `research/drawdown_reihenfolge/` hat ihre Raster **vor** dieser Änderung
   gerechnet und abgelegt. Der geänderte Bot liefert für dieselbe Kombination
   weiterhin denselben `max_drawdown_pct` und denselben `robustness_score` —
   für jeden der neun Bots geprüft.

---

## Was neu ist

`evaluate_combination_multi` weist **zusätzlich** aus:

```
max_drawdown_chronologisch_pct
```

Derselbe Drawdown, gerechnet auf der nach `entry_time` **stabil** sortierten
Trade-Menge — also auf der Reihenfolge, die `equity_simulation` benutzt und die
als einzige einen Verlauf beschreibt, den jemand hätte erleben können. Der
bisherige Wert bleibt `max_drawdown_pct` und bleibt Grundlage des
`robustness_score`.

Die Benennung ist **übernommen**, nicht neu erfunden:
`research/elliott_wave_params/engine.py` führt `max_drawdown_pct` und
`max_drawdown_chronologisch_pct` seit jeher nebeneinander.

Der neue Wert steht
* in der Ergebnistabelle jedes Bots (die `print`-Ausgabe des Rasters),
* in `results/<bot>/multi_symbol_optimisation_results.csv` (als **letzte**
  Spalte — die Reihenfolge der bisherigen Spalten bleibt damit unverändert),
* bei den drei Bots mit „Beste Kombination"-Block zusätzlich in einer eigenen
  Zeile, beide Masse nebeneinander.

**Nicht** ergänzt wurde ein `robustness_score_chronologisch`. Der Auftrag nennt
einen Wert, und die Zahl ist aus den vorhandenen Spalten ohnehin exakt
ableitbar (`avg_return_pct × √num_trades ÷ |Drawdown|`). Eine zweite
Score-Spalte hätte dagegen genau die Einladung geschaffen, nach ihr zu sortieren
— das ist Gegenstand von M2 und der Entscheidung danach, nicht von M1.

---

## Sind die neun Dateien identisch?

**Nein — und sie waren es schon vorher nicht.** Neun verschiedene Dateien mit
143 bis 234 Zeilen, jede mit eigener Prüfsumme.

| Baustein | Fassungen über die neun Bots |
|---|---|
| `calculate_robustness_score` | **1** — identisch in allen neun (nur `rsi2_crypto` trägt zusätzlich einen erklärenden Docstring) |
| `evaluate_combination_multi` | **9** — je eigene Parameterliste; `t3_supertrend` filtert zusätzlich nach BTC-Regime, sechs Bots führen `avg_holding_days` |
| `run_multi_optimisation` | **8** — `turtle_soup_crypto` und `turtle_soup_stocks` teilen eine Fassung |

Gemeinsam war ihnen aber genau die Stelle, um die es hier geht: die zwei Zeilen
der Drawdown-Berechnung standen in allen neun **zeichengleich** da. Die
Änderung ist deshalb in allen neun dieselbe.

**Vereinheitlicht wurde nichts.** Das wäre eine eigene Entscheidung.

---

## Rechenzeit

**Der zusätzliche Schritt kostet 0,5 bis 2,1 ms je Rasterkombination** —
isoliert gemessen, von 205 bis 12 069 Trades (die grösste Trade-Menge im
Projekt). Über ein ganzes Raster des teuersten Bots sind das rund **25 ms**.

Von Ende zu Ende, dieselbe Kombination mit alter und neuer Datei, je fünf
Läufe, Median:

| Bot | Trades | vorher | nachher |
|---|---|---|---|
| `turtle_soup_stocks` | 12 069 | 0,93 s | 0,96 s |
| `rsi2_mean_reversion` | 5 391 | 1,00 s | 1,02 s |
| `volatility_breakout` | 4 821 | 0,92 s | 0,96 s |
| `t3_supertrend` | 1 152 | 0,69 s | 0,69 s |
| `rsi2_crypto` | 205 | 0,130 s | 0,128 s |

**Nicht spürbar.** Die Ende-zu-Ende-Unterschiede liegen bei wenigen Prozent und
zeigen in beide Richtungen — sie sind Laufzeitrauschen, denn der Schritt selbst
ist zehnmal kleiner als sie. Bei den Elliott-Bots verschwindet er vollends: dort
gehen 23 bzw. 175 Sekunden je Kombination in die Wellenerkennung.

Zum Vergleich: der **Kapital**-Drawdown, den der Bericht als eigentlich
richtiges Mass nennt, hätte laut Untersuchung das 1,5- bis 2-Fache der
Rechenzeit gekostet.

---

## Ein Nebenbefund, der zur Einordnung gehört

Bei `t3_supertrend` sind beide Werte **gleich** (geprüft: −296,68 % gegen
−296,68 % bei T3 8/21 / ADX 20 / Stop 3 %). Das ist kein Fehler: dieser Bot
filtert nach dem Zusammenfügen nach BTC-Regime, und `filter_trades_by_regime`
sortiert dabei selbst nach `entry_time`. Er rechnet **heute schon**
chronologisch — nur hat das nie jemand entschieden. Der Bericht hält denselben
Befund fest (Abschnitt 2.3).

Umgekehrt ist der Abstand anderswo gross: bei `turtle_soup_stocks` stehen
−163,70 % (Blöcke) gegen −2 135,83 % (chronologisch).

---

## Was ausdrücklich nicht geändert wurde

* keine `live_params.py`, keine `forward_test.py`, keine `equity_simulation.py`;
* keine gespeicherte `multi_symbol_optimisation_results.csv` — die acht
  abgelegten Dateien sind der Beleg dafür, worauf frühere Entscheidungen
  standen, und bleiben unangetastet (der Selbsttest weist per `git status`
  nach, dass ein Testlauf an Bot-Code, Ergebnisdateien, Kursdaten, Logs und
  Datenbanken nichts verändert);
* die **Formel** des `robustness_score` — Zeichen für Zeichen dieselbe;
* nichts unter `broker/`, keine Crontab, keine launchd-Vorlage;
* `research/drawdown_reihenfolge/` wurde **gelesen**, nicht geändert.

---

## Wie es weitergeht

Dies ist **M1**. Der Bericht sieht danach vor:

* **M2** — die volle Kette (Backtest → Walk-Forward → Equity-Simulation →
  Buy-and-Hold-Vergleich) für die vier Bots, deren Parameterwahl unter dem
  chronologischen Mass gekippt wäre: `turtle_soup_crypto`,
  `turtle_soup_stocks`, `elliott_wave_stocks`, `elliott_wave`.
* **Danach die Entscheidung**, welches Mass künftig führt — mit beiden Zahlen
  vor Augen, was ab jetzt jede neue Optimierung liefert.

Offen bleibt ausserdem der Befund **N1** der Untersuchung: `sort_values`
**ohne** `kind="stable"` in `portfolio_correlation_analysis.py` und
`shared/portfolio_overview.py` (dort 0,07 Prozentpunkte Unterschied). Die neue
Stelle in den neun Bots ist von Anfang an stabil sortiert und im Test
abgesichert; die beiden alten Stellen sind **nicht** Gegenstand dieser Aufgabe.

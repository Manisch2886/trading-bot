# Ergebnis: Agent 2 wählt jetzt auf dem chronologischen Drawdown (TB-22)

**Stand: 2026-09-13** · `shared/param_search_agent.py` und die sechs Aufrufer.
**Kein Parameter übernommen, keine `live_params.py` angefasst, keine
Ergebnisdatei überschrieben, nichts automatisch geändert.**

---

## Die Zusicherung zuerst

> **Führen die beiden Drawdown-Maße zu verschiedenen Rangfolgen, wählt Agent 2
> die chronologische — am Verhalten geprüft, nicht am Vorhandensein eines
> Feldnamens im Quelltext.**

Nachgewiesen über 31 erzeugte Datensätze, in denen die beiden Maße
nachweislich auseinandergehen, plus eine Probe, die ganz ohne Formel auskommt:
zwei Zeilen mit gleicher Rendite und gleicher Trade-Zahl, Drawdowns über Kreuz —
es gewinnt der kleinere **chronologische** Rückgang.

Und die Gegenprobe: führen beide Maße zur selben Rangfolge, ändert sich nichts.

---

## Der Befund, der vor der Änderung stand

**Agent 2 liest keine abgelegte CSV.** Alle sechs Aufrufer
(`agent_optimise.py` und `quarterly_review.py` bei `elliott_wave`,
`elliott_wave_stocks`, `t3_supertrend`) reichen eine Funktion herein, die zu
`evaluate_combination_multi` führt; die Zahlen entstehen bei jedem Lauf neu.

**Die Rangfolge entstand an zwei getrennten Stellen:**

| | wer entschied | worauf |
|---|---|---|
| **Auswahl** — wer von den getesteten gewinnt | Code: `max(valid_results, key=lambda r: r["robustness_score"])` | Blockmaß |
| **Suchrichtung** — was überhaupt getestet wird | das Modell, anhand der Tabelle | „auch … Max Drawdown (kleiner = robuster)" — ohne zu sagen, welcher |

Seit PR #90 sah das Modell `max_drawdown_chronologisch_pct` bereits in der
Tabelle. Es stand nur nirgends, was damit anzufangen wäre.

**Abgelegte Vorschläge aus früheren Läufen: im Repo keine.** `run_agent_search`
gibt sein Ergebnis zurück, `agent_optimise.py` druckt es, `quarterly_review.py`
verschickt es — keiner schreibt eine Datei. Auf dem Rechner des Nutzers können
welche in `logs/<bot>/` (gitignored) und in den Telegram-Verläufen stehen.
Was auf dem alten Maß beruht, bleibt **unangetastet**: diese Logs, die acht
`results/<bot>/multi_symbol_optimisation_results.csv` (die Rangfolge der
Rastersuche) und die Rasterergebnisse unter `research/`. Ab jetzt trägt jeder
neue Vorschlag die Zielgrößen-Angabe und ist von den älteren unterscheidbar.

---

## Was geändert wurde

| Stelle | vorher | nachher |
|---|---|---|
| Auswahl (`max(...)`) | `robustness_score` | `robustness_score_chronologisch` |
| Prompt | Tabelle ohne Angabe des Maßes | zusätzlich Abschnitt **„ZIELGROESSE DER AUSWAHL"** |
| Ausgabe | — | ein fest verdrahteter Satz mit **beiden** Zahlen und dem Hinweis, welche galt |

Der neue Score wird **in `param_search_agent.py`** aus den vorhandenen Spalten
gerechnet — `avg_return_pct × √num_trades ÷ |max_drawdown_chronologisch_pct|`,
zeichengleich zu `calculate_robustness_score` bis auf den Nenner.
`multi_symbol_optimise.py` bleibt unberührt: eine zweite Score-Spalte dort
landete in jeder `results/*.csv` und wäre die Einladung, nach ihr zu sortieren,
die TB-18 bewusst vermieden hat.

**Beide Varianten der Aufgabenstellung sind umgesetzt** — Score neu rechnen
*und* beide Werte zeigen. Nicht als Kompromiss: die Auswahl trifft Code, die
Suchrichtung steuert das Modell. Nur eine der beiden Stellen umzustellen hätte
Prompt und Mechanik gegeneinander laufen lassen. Der Feldname steht deshalb
**einmal** (`FELD_SCORE_CHRONO`) und wird von Rechnung, Prompt und Ausgabe
importiert.

---

## So sieht es aus

Im Prompt:

```
ZIELGROESSE DER AUSWAHL:
Massgeblich ist ausschliesslich 'robustness_score_chronologisch'
(avg_return_pct x Wurzel(num_trades) / |max_drawdown_chronologisch_pct|) -
also der Drawdown auf der CHRONOLOGISCHEN Reihenfolge der Trades. Je hoeher
dieser Wert, desto besser.
'robustness_score' und 'max_drawdown_pct' stehen in der Tabelle weiterhin zum
Vergleich. [...] Sie sind NICHT das Auswahlkriterium; wenn beide Masse in
verschiedene Richtungen zeigen, gilt das chronologische.
```

Im Quartals-Bericht, direkt unter dem Pflichthinweis:

```
⚠️ PARAMETER-VORSCHLAG (UNVALIDIERT)
Dieser Vorschlag wurde NICHT durch Walk-Forward-Validierung geprüft.
Keine automatische Umsetzung. [...]
============================================================
  {'deviation_pct': 10.0, 'stop_loss_pct': 6.0, 'take_profit_fib': 0.618}

  Auswahl-Zielgroesse: robustness_score_chronologisch
  (avg_return_pct x Wurzel(num_trades) /
  |max_drawdown_chronologisch_pct|) - der Drawdown auf der
  chronologischen Reihenfolge. Gewaehlt mit 1.624
  (chronologisch) gegen 0.245 auf Blockreihenfolge -
  letzterer nur zum Vergleich, nicht Auswahlgrundlage.
```

Die Angabe ist **fest verdrahtet**, nicht vom Modell formuliert — aus demselben
Grund, aus dem der Unvalidiert-Pflichthinweis eine Konstante ist: ein Modell
könnte sie variieren, abschwächen oder vergessen, ein Konstanten-String nicht.

---

## Was ausdrücklich **nicht** geändert wurde

* **Der Agent ändert weiterhin nichts automatisch.** Vorschläge sind und bleiben
  unvalidiert und brauchen Walk-Forward.
* Der Unvalidiert-Pflichthinweis in `shared/empfehlung_format.py` — unverändert,
  mit einer Testprobe, die anschlägt, wenn er verschwindet.
* Die **Rastersuche**: `multi_symbol_optimise.py` wählt weiter auf dem Blockmaß.
  Die Übergangsregel „beide Maße ausweisen" gilt für Ausgaben und Berichte;
  Agent 2 war die benannte Ausnahme, weil er eine **Auswahl** trifft.
* `live_params.py`, `forward_test.py`, `equity_simulation.py`, `results/*`,
  alles unter `broker/`, Crontab, launchd-Vorlagen, `research/*`.

---

## Tests

`python3 shared/test_agent2_zielfunktion.py` → **41 von 41 Prüfungen bestanden**,
~4 Sekunden, **kein einziger echter API-Aufruf** (der Sendeweg ist ein
Parameter; zusätzlich wirft `call_claude` für die Dauer jedes Laufs eine
Ausnahme). Darunter **5 Mutationsproben**: jede Wache wird einzeln aus einer
Kopie entfernt, und die zugehörige Prüfung muss dann anschlagen.

Alle bestehenden Tests laufen unverändert. Belegt gegen einen Basislauf auf
unverändertem `main` (`0f39e3b`):

| Test | `main` | Branch |
|---|---|---|
| `shared/test_drawdown_beide_masse.py --ohne-kursdaten` | 181/181 | 181/181 |
| `shared/test_empfehlung_format.py` | 70/70 | 70/70 |
| `shared/test_live_params_werte.py` | 69/69 | 69/69 |
| `shared/test_wellenauswahl.py` | 323/323 | 323/323 |
| `shared/test_ergebniskurven.py` | 44/44 | 44/44 |
| `shared/test_stabile_sortierung.py` | 46/46 | 46/46 |
| `notifications/test_schliess_benachrichtigung.py` | 99/99 | 99/99 |
| `notifications/test_manual_close.py` | alle | alle |
| `broker/test_broker.py` | 163/163 | 163/163 |
| `system/test_log_rotation.py` | 117/117 | 117/117 |
| `system/test_caffeinate_plist.py` | 53/53 | 53/53 |
| `system/test_dienst_plists.py` | 140/144 (4 Platzhalter) | identisch |
| `shared/test_kursdaten.py` | 62/66 (`yfinance` fehlt) | identisch |
| `dashboard/test_portfolio_sicht.py` | 66/68 (`fastapi` fehlt) | identisch |
| `dashboard/test_dashboard.py` | Abbruch (`fastapi` fehlt) | identisch |
| `broker/test_ibkr.py` | Abbruch (Zeitzone `US/Eastern` fehlt) | identisch |

**Jeder Fehlschlag ist vorbestehend und rein umgebungsbedingt** — kein einziger
entsteht durch diese Änderung.

---

## Wie es weitergeht

* Schritt **M2** aus `research/drawdown_reihenfolge/BERICHT.md` bleibt offen: die
  volle Kette für die vier Bots, deren Parameterwahl unter dem chronologischen
  Maß kippen würde (`turtle_soup_crypto`, `turtle_soup_stocks`,
  `elliott_wave_stocks`, `elliott_wave`).
* Die Frist für die Entscheidung, welches Maß im Repo insgesamt führt, läuft
  weiter. Diese Änderung greift ihr nicht vor — sie betrifft nur die eine
  Stelle, an der Warten aktiv geschadet hätte.
* Die sechs Prototyp-Bots haben Agent 2 gar nicht; betroffen sind drei Bots.

# TB-23 Determinismus: Ergebnis auf einer Seite

**Messung, keine Korrektur.** Es wurde nichts behoben — kein `live_params.py`,
kein `forward_test.py`, kein `equity_simulation.py`, kein
`multi_symbol_optimise.py`, keine Symboldatei, keine Ergebnisdatei. Neu sind
ausschliesslich Dateien unter `shared/` und `research/`. Ob etwas geändert
wird, entscheidet der Nutzer. Vollständiger Bericht:
`research/determinismus/BERICHT.md`.

---

## 1. Die Bestandsaufnahme: acht von neun Bots sind nicht deterministisch

20 Permutationen der Symbolreihenfolge, sonst alles identisch — dieselben
Kursdaten, dieselben Parameter, derselbe Code.

| Bot | Urteil | umstrittene Trades | Rendite-Spanne | Drawdown-Spanne |
|---|---|---|---|---|
| `elliott_wave` | **NUR REIHENFOLGE** | 0,0 % | 67,77 .. 67,77 % | −10,17 .. −10,17 % |
| `elliott_wave_stocks` | **NICHT DETERMINISTISCH** | 28,2 % | 321,80 .. 424,42 % | −23,22 .. −22,19 % |
| `rsi2_crypto` | **NICHT DETERMINISTISCH** | 14,4 % | 25,58 .. 34,07 % | −13,96 .. −12,66 % |
| `rsi2_mean_reversion` | **NICHT DETERMINISTISCH** | 27,1 % | 27,90 .. 45,62 % | −22,15 .. −18,93 % |
| `t3_supertrend` | **NICHT DETERMINISTISCH** | 14,6 % | 117,87 .. 138,12 % | −22,57 .. −22,14 % |
| `turtle_soup_crypto` | **NICHT DETERMINISTISCH** | 30,6 % | 123,77 .. 190,23 % | −41,24 .. −32,40 % |
| `turtle_soup_stocks` | **NICHT DETERMINISTISCH** | 36,4 % | 121,84 .. 164,68 % | −30,58 .. −28,45 % |
| `volatility_breakout` | **NICHT DETERMINISTISCH** | 46,6 % | 145,16 .. 269,47 % | −25,64 .. −22,89 % |
| `volatility_breakout_crypto` | **NICHT DETERMINISTISCH** | 11,6 % | 46,29 .. 73,45 % | −16,29 .. −16,29 % |

„Umstritten" = Trades, die nur in einem Teil der Permutationen ausgeführt
werden, weder immer noch nie (dieselbe Definition wie in
`research/order_sensitivity/`).

**`elliott_wave` ist der einzige Sonderfall:** alle 130 Trades werden in jeder
Permutation ausgeführt, Endkapital und Drawdown sind auf den Cent identisch.
Nur die **Zeilenreihenfolge** seiner `equity_curve.csv` unterscheidet sich —
wirtschaftlich folgenlos, aber relevant, weil `shared/ergebniskurven.py` diese
Datei Zeile für Zeile vergleicht.

---

## 2. Drei Zahlen, die die Sache greifbar machen

* **`volatility_breakout`: 145 % bis 269 % Rendite.** Die abgelegte Kurve
  nennt 224,41 %. Welche der zwanzig Zahlen dort steht, entscheidet allein die
  Sortierung von `config/sp500_top150.txt`.
* **`volatility_breakout_crypto`: Max Drawdown in allen zwanzig Permutationen
  exakt −16,29 %, exakt 207 ausgeführte Trades — und die Rendite schwankt
  zwischen 46,3 % und 73,5 %.** Wer nur Kennzahlen vergleicht, sieht hier
  nichts. Deshalb ist das Leitkriterium die **Menge der ausgeführten Trades**,
  nicht die Kennzahl.
* **`turtle_soup_stocks` hat gar kein Positionslimit — und ist mit 36,4 % der
  zweitstärkste Fall.** Bindend ist dort die Kapitalschranke: bei 2 %
  Allokation sind höchstens 50 Positionen finanzierbar, gemessen stehen 50–51
  offen und über 3100 Trades werden abgelehnt.

---

## 3. Woran es liegt — und woran nicht

**Die Ursache sitzt an einer einzigen Stelle: der Zuteilung in
`simulate_portfolio()`.** Wird ein Platz knapp (Positionslimit oder freies
Kapital), entscheidet die Zeilenreihenfolge des Trade-DataFrames, wer ihn
bekommt — und die ist die Symbolreihenfolge. Es gibt **kein benanntes
Zweitkriterium**. Die fehlende stabile Sortierung (`combined.sort_values(
"entry_time")` ohne `kind="stable"`, in allen neun Bots) kommt hinzu, ist aber
nicht die Wurzel: auch eine stabile Sortierung würde die Eingabereihenfolge
erhalten — also die Symbolreihenfolge.

**Nicht die Ursache ist die Signalerzeugung.** Bei allen neun Bots ist die
Menge der erzeugten Trades über alle zwanzig Permutationen **bitidentisch**.
`get_trades_for_symbol()` läuft je Symbol unabhängig. Der Fehler ist damit an
einer Stelle behebbar, nicht in neun Strategien verstreut.

**Wie oft es eng wird:**

| bindend ist … | Bots |
|---|---|
| das **Positionslimit** (in 20/20 Läufen erreicht) | `elliott_wave_stocks`, `rsi2_crypto`, `rsi2_mean_reversion`, `t3_supertrend`, `turtle_soup_crypto`, `volatility_breakout_crypto` |
| die **Kapitalschranke** | `turtle_soup_stocks` (kein Limit), `volatility_breakout` (Limit 15, aber nur 10 finanzierbar — das Limit greift nie) |
| **nichts** | `elliott_wave` (0 abgelehnte Trades) |

---

## 4. Die offene Frage: eine Zuteilung nach Signalstärke reicht nicht

Gemessen (`research/determinismus/signalstaerke.py`):

* Bei **`elliott_wave_stocks`** kann der `fib_score` oberhalb seiner Schwelle
  nur **fünf** Werte annehmen (0,33 / 0,34 / 0,66 / 0,67 / 1,0). 300 der 510
  Trades teilen ihren Einstiegszeitpunkt mit mindestens einem anderen, die
  grösste Gruppe umfasst 20 Titel. **Nach einer Rangregel auf dem `fib_score`
  bleiben 144 Trades (48,0 % der gleichzeitigen) weiterhin gleichauf.**
* **Sieben der neun Bots führen überhaupt kein Mass für Signalstärke mit.**
  Eines einzuführen wäre eine Strategieänderung, keine Rangregel.
* Das TB-20-Zweitkriterium (`end_time` absteigend) hilft hier nicht: es
  entscheidet zwischen Wellenmustern **eines** Symbols. Bei der Zuteilung
  konkurrieren verschiedene Symbole zum **selben** Balken.

**Benannt, nicht gelöst.** Was stattdessen zu tun ist, ist eine eigene
Aufgabe.

---

## 5. Das Werkzeug

```bash
python3 shared/determinismus.py --schnell       # alle 9 Bots, 101 s, Rückgabewert 1 bei Befund
python3 shared/determinismus.py --voll --perms 20   # die Bestandsaufnahme, ~13 min
python3 shared/test_determinismus.py            # 49 Selbsttests, ~40 s
```

* Die Symboldateien werden **nur gelesen**; permutiert wird im Speicher.
* `RESULTS_DIR` zeigt während jedes Laufs in einen temporären Ordner — das
  Werkzeug kann `results/<bot>/equity_curve.csv` gar nicht überschreiben.
  Nach dem Lauf meldet `shared/ergebniskurven.py` weiterhin **9× AKTUELL**.
* Ein Subprozess je Bot (neun gleichnamige `equity_simulation.py` kollidieren
  in `sys.modules`); ausgeführt wird der `__main__`-Block des Bots selbst.
* **Pflicht-Gegencheck bestanden:** Lauf 0 (Originalreihenfolge) trifft bei
  **9 von 9** Bots die abgelegte `equity_curve.csv` exakt — Zeilenzahl und
  Endkapital.
* **Gegenprobe bestanden:** eine gehärtete Kopie von `turtle_soup_crypto`
  (totale Sortierung, kein Limit, Allokation 0,01 %) wird als
  *deterministisch* gemeldet. Dieselbe Kopie plus genau einem eingebauten
  Fehler (Zuteilung nach Dateirang bei 3 Plätzen für 24 Symbole) wieder als
  Befund.
* **Falsche Entwarnung ausgeschlossen:** eine Kopie, die die Permutation
  ignoriert, wird als `UNKLAR` gemeldet, nicht als `DETERMINISTISCH`.

---

## 6. Offene Punkte für Folgeaufgaben

1. Eine Zuteilungsregel, die auch dort greift, wo es kein Mass für
   Signalstärke gibt (sieben von neun Bots).
2. Die 19 weiteren `sort_values`-Aufrufe ohne `kind="stable"` (TB-19).
3. `volatility_breakout`: `MAX_CONCURRENT_POSITIONS = 15` bei rechnerisch
   höchstens 10 finanzierbaren Positionen — das Limit greift nie.
4. `shared/determinismus.py --schnell` als nächtlicher Cronjob. Diese Arbeit
   legt keinen an; `system/` und Crontab bleiben unberührt.

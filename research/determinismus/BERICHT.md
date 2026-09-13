# Determinismus der Backtests unter permutierter Symbolreihenfolge — alle 9 Bots

**Status: Messung, keine Korrektur.** Es wurde nichts behoben — kein
`live_params.py`, kein `forward_test.py`, kein `equity_simulation.py`, kein
`multi_symbol_optimise.py`, keine Symboldatei, keine Ergebnisdatei. Neu sind
ausschliesslich Dateien unter `shared/` und `research/`. Verifiziert
per `git status` und `git diff --stat` (Abschnitt 8).

---

## 0. Entscheidungsgrundlage

### Die Frage

> Ein Backtest, der mit 20 zufälligen Permutationen der Symboldatei läuft,
> muss **bitidentische** Ergebnisse liefern. Ist er das nicht, gibt es
> versteckten Zustand.

### Datenbasis

Alle neun Bots, jeder mit seinem **unveränderten** `equity_simulation.py`,
ausgeführt über `runpy.run_path(..., run_name="__main__")` — also genau das,
was `python3 strategies/<bot>/equity_simulation.py` tut. Zwischen den Läufen
ändert sich **ausschliesslich die Reihenfolge der Symbolliste**.

| | |
|---|---|
| Bots | 9 von 9 |
| Permutationen | 20 je Bot (Lauf 0 = Originalreihenfolge) |
| Zufalls-Startwert | 20260913, fest |
| Modus | `--voll` — **kein** Zwischenspeicher, jede Permutation komplett neu gerechnet |
| Laufzeit | 800 s für alle neun Bots |
| Umgebung | Python 3.11.15, pandas 3.0.5, numpy 2.4.6 |
| Kursstand | `data/`, Stand 2026-09-13 |

Reproduktion:

```bash
python3 shared/determinismus.py --voll --perms 20     # die Messung, ~13 min
python3 shared/determinismus.py --schnell             # dieselben Urteile, 101 s
python3 shared/test_determinismus.py                  # 49 Selbsttests
python3 research/determinismus/signalstaerke.py       # Abschnitt 6
```

### Pflicht-Gegencheck: rechnet diese Messung dasselbe wie die Bots?

Lauf 0 läuft in der unveränderten Originalreihenfolge. Er **muss** deshalb die
abgelegte `results/<bot>/equity_curve.csv` treffen — Zeilenzahl und
Endkapital.

**Ergebnis: 9 von 9 exakt getroffen** (`ergebnisse/gegencheck_lauf0.txt`):

| Bot | Lauf 0 | abgelegte Kurve | Zeilen |
|---|---|---|---|
| `elliott_wave` | 16 777,45 | 16 777,45 | 130/130 |
| `elliott_wave_stocks` | 45 272,24 | 45 272,24 | 395/395 |
| `rsi2_crypto` | 12 837,09 | 12 837,09 | 392/392 |
| `rsi2_mean_reversion` | 13 675,20 | 13 675,20 | 4232/4232 |
| `t3_supertrend` | 22 963,95 | 22 963,95 | 656/656 |
| `turtle_soup_crypto` | 27 759,42 | 27 759,42 | 1414/1414 |
| `turtle_soup_stocks` | 24 559,08 | 24 559,08 | 8915/8915 |
| `volatility_breakout` | 32 441,42 | 32 441,42 | 1454/1454 |
| `volatility_breakout_crypto` | 14 902,58 | 14 902,58 | 207/207 |

Das ist die Absicherung gegen den Fehler, an dem der HRP-Bericht zweimal
gekippt ist: eine Untersuchung, die eine zweite, leicht abweichende Fassung
des Bots rechnet. Hier wird der `__main__`-Block des Bots selbst ausgeführt,
aus demselben Grund und mit demselben Mittel wie in `shared/kurven_lauf.py`.

### Belastbarkeit

Der Effekt ist **kein Schätzproblem, sondern eine deterministische
Willkür**: bei gegebener Symbolreihenfolge steht das Ergebnis eindeutig fest.
Gemessen wird, wie stark es sich ändert, wenn man ausschliesslich diese eine,
inhaltlich beliebige Grösse variiert. Es gibt hier keine
Stichprobenunsicherheit zu quantifizieren; die berichtete Spanne ist die
Bandbreite von 20 gleichermassen legitimen Ergebnissen — die wahre Bandbreite
über alle 24! bzw. 150! Reihenfolgen ist mindestens so gross.

### Was NICHT untersucht wurde

* **Ob eine bestimmte Zuteilungsregel besser wäre.** Abschnitt 6 misst nur,
  ob die naheliegende Regel (nach Signalstärke) das Problem überhaupt lösen
  *kann*.
* **Ob die heutigen Live-Parameter unter anderer Symbolreihenfolge dieselben
  wären.** Das misst `research/drawdown_reihenfolge/` (Antwort: bei drei Bots
  nicht).
* **Die Live-Bots.** Gemessen wird der Backtest-Pfad. Der Live-Pfad
  (`forward_test.py`) wurde nicht angefasst; die Verarbeitungsreihenfolge dort
  beschreibt `research/order_sensitivity/`, Abschnitt 6.

---

## 1. Kurzfassung

**Acht von neun Bots sind nicht deterministisch. Der neunte ist es
wirtschaftlich, aber nicht bitidentisch.**

| Bot | Urteil | umstrittene Trades | Rendite-Spanne | Drawdown-Spanne |
|---|---|---|---|---|
| `elliott_wave` | **NUR REIHENFOLGE** | 0,0 % | 67,77 .. 67,77 % | −10,17 .. −10,17 % |
| `elliott_wave_stocks` | NICHT DETERMINISTISCH | **28,2 %** | 321,80 .. 424,42 % | −23,22 .. −22,19 % |
| `rsi2_crypto` | NICHT DETERMINISTISCH | 14,4 % | 25,58 .. 34,07 % | −13,96 .. −12,66 % |
| `rsi2_mean_reversion` | NICHT DETERMINISTISCH | 27,1 % | 27,90 .. 45,62 % | −22,15 .. −18,93 % |
| `t3_supertrend` | NICHT DETERMINISTISCH | 14,6 % | 117,87 .. 138,12 % | −22,57 .. −22,14 % |
| `turtle_soup_crypto` | NICHT DETERMINISTISCH | 30,6 % | 123,77 .. 190,23 % | −41,24 .. −32,40 % |
| `turtle_soup_stocks` | NICHT DETERMINISTISCH | **36,4 %** | 121,84 .. 164,68 % | −30,58 .. −28,45 % |
| `volatility_breakout` | NICHT DETERMINISTISCH | **46,6 %** | 145,16 .. 269,47 % | −25,64 .. −22,89 % |
| `volatility_breakout_crypto` | NICHT DETERMINISTISCH | 11,6 % | 46,29 .. 73,45 % | −16,29 .. −16,29 % |

Drei Zahlen zur Einordnung:

* **`volatility_breakout`**: die Rendite reicht von 145 % bis 269 %. Die
  abgelegte Kurve nennt 224,41 %. Welche der zwanzig Zahlen in
  `results/` steht, entscheidet allein die Sortierung von
  `config/sp500_top150.txt`.
* **`volatility_breakout_crypto`**: der Max Drawdown ist in **allen zwanzig**
  Permutationen exakt −16,29 %, die Zahl der ausgeführten Trades exakt 207 —
  und die Rendite schwankt trotzdem zwischen 46,3 % und 73,5 %. Wer nur die
  Kennzahlen vergleicht, sieht hier zwei Drittel eines Kennzahlensatzes
  unverändert und übersieht, dass es **andere Trades** sind.
* **`elliott_wave_stocks`**: 28,2 % umstrittene Trades. Die in
  `research/order_sensitivity/` gemessenen 21,8 % beziehen sich auf die
  Permutation der **Trade-Reihenfolge** bei festem Trade-Satz; hier wird die
  Symboldatei permutiert, was zusätzlich die Zusammensetzung des Trade-Satzes
  in der Zeilenreihenfolge verschiebt. Die beiden Zahlen messen verwandte,
  aber nicht identische Dinge; dass die hiesige grösser ausfällt, ist
  erwartbar.

---

## 2. Was verglichen wird — und warum nicht die Kennzahlen

„Bitidentisch" ist das Ziel. Aber bitidentisch **worin**? Die Antwort
entscheidet, ob die Prüfung etwas taugt.

Verglichen wird auf **drei Ebenen**:

| Ebene | Was | Vergleich |
|---|---|---|
| **1. Signalmenge** | alle erzeugten Trades, bevor das Kapital darüber entscheidet — Symbol, Ein- und Ausstieg, Kurse, Ergebnis, Ausstiegsgrund | als **Multimenge**, reihenfolgeunabhängig |
| **2. Ausgeführte Trades** | welche Trades tatsächlich Kapital bekommen haben | als **Multimenge**, reihenfolgeunabhängig |
| **3. Kapitalpfad** | die Zeilen der `equity_curve.csv` mit Allokation und Kapitalstand | **in ihrer Reihenfolge** |

**Ebene 2 ist das Leitkriterium.** Weicht sie ab, hat die Symbolreihenfolge
entschieden, *wer gehandelt wird* — das ist der Befund, um den es geht.
Weicht Ebene 1 ab, hätte die Signalerzeugung selbst symbolübergreifenden
Zustand; das wäre der schwerste denkbare Fall und tritt bei **keinem** der
neun Bots auf (Abschnitt 3, „Was NICHT die Ursache ist"). Weicht nur Ebene 3 ab, sind es dieselben Trades
in anderer Abrechnungsreihenfolge — ein Befund, aber ein schwächerer.

### Warum die Kennzahlen kein Kriterium sind

Der Auftrag nennt es selbst: „Ein Vergleich der Kennzahlen allein würde
Reihenfolge-Unterschiede verdecken, die sich gerade herausmitteln." Dass das
kein theoretisches Bedenken ist, zeigt `volatility_breakout_crypto` oben:
identischer Drawdown, identische Trade-Zahl, 27 Prozentpunkte Unterschied in
der Rendite. Die Kennzahlen werden deshalb **ausgewiesen**, gehen aber in kein
Urteil ein.

### Warum Ebene 1 und 2 reihenfolgeunabhängig verglichen werden

Die Zeilenreihenfolge des zusammengehängten Trade-DataFrames ist ein
Nebenprodukt der Symbolblöcke und beschreibt keinen Verlauf, den jemand hätte
erleben können. Genau diese Begründung steht seit
`research/drawdown_reihenfolge/` bereits im Kommentar von
`multi_symbol_optimise.py`. Würde man sie als Kriterium nehmen, wären alle
neun Bots aus einem Grund ohne inhaltlichen Gehalt rot — und eine Prüfung,
die immer anschlägt, liest bald niemand mehr. Ebene 3 hält den
Reihenfolgeaspekt dort fest, wo er eine Datei betrifft, auf die sich andere
Programme berufen.

---

## 3. Woran es liegt

### Ursache A — die Zuteilung bei knappen Plätzen (acht von neun Bots)

`simulate_portfolio()` arbeitet die Ein- und Ausstiegsereignisse
chronologisch ab und lehnt einen Einstieg ab, wenn entweder
`MAX_CONCURRENT_POSITIONS` erreicht ist **oder** das freie Kapital nicht
reicht. Bei Gleichstand im Zeitstempel entscheidet die Zeilenreihenfolge des
Trade-DataFrames, wer zuerst drankommt — und die entsteht so:

```
Symboldatei  →  SYMBOLS  →  for symbol in SYMBOLS  →  pd.concat(Symbolblöcke)
             →  combined.sort_values("entry_time")  →  events.sort(...)
             →  wer bekommt den Platz
```

Zwei Stellen tragen bei:

1. **`combined.sort_values("entry_time")` ohne `kind="stable"`** — in allen
   neun `equity_simulation.py` identisch (Zeile 52 bis 101, je nach Bot).
   Quicksort vertauscht Gleichstände abhängig von Feldlänge und Feldinhalt.
2. **Auch mit stabiler Sortierung bliebe der Effekt.** Eine stabile Sortierung
   erhält die *Eingabereihenfolge* — und die ist die Symbolreihenfolge. Die
   fehlende `kind="stable"` ist ein eigenes Problem (TB-19), aber nicht die
   Wurzel dieses hier. Die Wurzel ist, dass es **gar kein benanntes
   Zweitkriterium** gibt.

Wie oft es überhaupt eng wird, ist gemessen:

| Bot | Limit | max. gleichzeitig offen | Limit erreicht | abgelehnte Trades | knapp wird … |
|---|---|---|---|---|---|
| `elliott_wave` | keins | 7 | nie | **0** | nie |
| `elliott_wave_stocks` | 8 | 8 | in 20/20 Läufen | 111 .. 118 | das Limit |
| `rsi2_crypto` | 8 | 8 | in 20/20 Läufen | 46 .. 47 | das Limit |
| `rsi2_mean_reversion` | 20 | 20 | in 20/20 Läufen | 1152 .. 1171 | das Limit |
| `t3_supertrend` | 5 | 5 | in 20/20 Läufen | 321 .. 327 | das Limit |
| `turtle_soup_crypto` | 8 | 8 | in 20/20 Läufen | 184 .. 196 | das Limit |
| `turtle_soup_stocks` | **keins** | 51 | nie | 3149 .. 3157 | **das Kapital** |
| `volatility_breakout` | 15 | **10** | **nie** | 3050 .. 3063 | **das Kapital** |
| `volatility_breakout_crypto` | 8 | 8 | in 20/20 Läufen | 26 | das Limit |

Drei Beobachtungen, die sonst untergehen:

* **`turtle_soup_stocks` hat kein Positionslimit — und ist trotzdem der
  zweitstärkste Fall (36,4 %).** Die Annahme aus dem Auftrag, „ein Bot ohne
  bindendes Limit kann diesen Fehler gar nicht haben", trifft für das *Limit*
  zu, nicht für die Knappheit. Bei 2 % Allokation sind rechnerisch höchstens
  50 Positionen finanzierbar; gemessen stehen 50 bis 51 gleichzeitig offen und
  über 3100 Trades werden abgelehnt. Die Kapitalschranke ist dort die
  bindende — und teilt nach derselben willkürlichen Reihenfolge zu.
* **Bei `volatility_breakout` ist das Limit von 15 wirkungslos.** Bei 10 %
  Allokation sind höchstens 10 Positionen finanzierbar; der Höchststand liegt
  in allen zwanzig Läufen bei genau 10, das Limit wird nie erreicht. Alle
  3050+ Ablehnungen gehen auf das Kapital zurück. Der Bot mit dem grössten
  Streuungsproblem (46,6 %) ist damit zugleich der, bei dem die vorhandene
  Schutzgrösse gar nicht greift.
* **Umgekehrt bei `elliott_wave_stocks`, `rsi2_crypto`, `t3_supertrend`,
  `turtle_soup_crypto`, `volatility_breakout_crypto`**: dort ist
  `Allokation × Limit ≤ 1`, das Limit greift also immer zuerst. Der Kommentar
  in `elliott_wave_stocks/equity_simulation.py` („im gemessenen Lauf gingen
  ALLE 115 übersprungenen Trades auf das Limit zurück") wird durch diese
  Messung bestätigt: 111 bis 118 Ablehnungen, Höchststand konstant 8.

### Ursache B — die Abrechnungsreihenfolge bei gleichem Zeitstempel (`elliott_wave`)

`elliott_wave` ist der einzige Bot, bei dem nie etwas knapp wird: kein
Positionslimit, Höchststand 7 gleichzeitig offene Positionen bei 10 möglichen,
**null** abgelehnte Trades. Alle 130 Trades werden in **jeder** Permutation
ausgeführt; Endkapital und Max Drawdown sind auf den Cent identisch.

Trotzdem liefert er **zwanzig verschiedene Kapitalpfade**. Der Grund: bei
gleichem Ausstiegszeitpunkt entscheidet die Zeilenreihenfolge, in welcher
Folge die Ausstiege verbucht werden. Zwischenstände von `allocation` und
`capital_after` unterscheiden sich, das Ende nicht.

Das ist wirtschaftlich folgenlos — aber nicht folgenlos für das Repo:
`results/equity_curve.csv` dieses Bots ist die Grundlage der Montags-Mail und
der Dashboard-Portfolio-Sicht, und `shared/ergebniskurven.py` vergleicht sie
**Zeile für Zeile**. `config/top25_symbols.txt` wird von
`shared/get_top_symbols.py` nach Volumen neu erzeugt; ändert sich dabei die
Rangfolge zweier Coins, meldet `ergebniskurven.py` diese Kurve als
**ABWEICHEND** — aus einem Grund ohne inhaltlichen Gehalt. Zum Zeitpunkt
dieser Messung ist das nicht eingetreten (`ergebniskurven.py` meldet 9×
AKTUELL, Abschnitt 8).

### Was NICHT die Ursache ist

Die Signalerzeugung. Bei allen neun Bots ist die Signalmenge über alle zwanzig
Permutationen **bitidentisch** — dieselbe Zahl Trades, dieselben Symbole,
dieselben Ein- und Ausstiegszeitpunkte und -kurse, dieselben Ausstiegsgründe.
`get_trades_for_symbol()` läuft je Symbol unabhängig, ohne symbolübergreifenden
Zustand. Das ist die gute Nachricht dieses Berichts: der Fehler sitzt an
**einer** Stelle, in der Portfolio-Simulation, und nicht verstreut in neun
Strategien.

Bestätigt wird das zweimal unabhängig: durch den Vergleich der Signal-Ebene
über alle Permutationen, und durch die Selbstprüfung des Zwischenspeichers im
Schnellmodus (Abschnitt 5), die jedes Symbolergebnis nachrechnet und
vergleicht — **0 Abweichungen** bei allen neun Bots.

---

## 4. Die Streuung im Einzelnen

| Bot | Trades gesamt | immer ausgeführt | nie ausgeführt | umstritten | ausgeführt (min..max) |
|---|---|---|---|---|---|
| `elliott_wave` | 130 | 130 | 0 | **0** | 130 .. 130 |
| `elliott_wave_stocks` | 510 | 328 | 38 | 144 | 392 .. 399 |
| `rsi2_crypto` | 439 | 352 | 24 | 63 | 392 .. 393 |
| `rsi2_mean_reversion` | 5391 | 3511 | 419 | 1461 | 4220 .. 4239 |
| `t3_supertrend` | 980 | 588 | 249 | 143 | 653 .. 659 |
| `turtle_soup_crypto` | 1599 | 1088 | 22 | 489 | 1403 .. 1415 |
| `turtle_soup_stocks` | 12069 | 6979 | 702 | 4388 | 8912 .. 8920 |
| `volatility_breakout` | 4510 | 686 | 1722 | 2102 | 1447 .. 1460 |
| `volatility_breakout_crypto` | 233 | 198 | 8 | 27 | 207 .. 207 |

„Umstritten" ist dieselbe Grösse wie in `research/order_sensitivity/`: weder
immer noch nie ausgeführt. Ein Bot kann viele Trades ablehnen und trotzdem
unempfindlich sein — nämlich dann, wenn es immer dieselben sind.

**Die Zahl der ausgeführten Trades ist fast konstant, die Auswahl nicht.**
`volatility_breakout_crypto` führt in jeder Permutation exakt 207 von 233
Trades aus — aber nicht dieselben 207. `turtle_soup_stocks` schwankt zwischen
8912 und 8920 von 12069, und 4388 Trades sind umstritten. Wer die Zahl der
Trades als Stabilitätsindiz liest, liest sie falsch.

---

## 5. Laufzeit — wie das beherrschbar wird

Der Auftrag rechnet mit „175 Sekunden je Kombination" bei
`elliott_wave_stocks`. Gemessen wurde in der Cloud-Umgebung **12,9 s für einen
vollständigen `equity_simulation.py`-Lauf** dieses Bots. Der Unterschied hat
zwei Gründe, und beide gehören in den Bericht:

1. `equity_simulation.py` rechnet **eine** Parameterkombination, nicht das
   Raster von `multi_symbol_optimise.py` (dort sind es 64 Kombinationen).
   Die 175 s beziehen sich auf eine Rasterkombination samt Wellenerkennung
   über alle 150 Titel.
2. Die Cloud-Maschine ist schneller als der Mac des Nutzers. Die absoluten
   Zahlen unten sind deshalb als **Verhältnisse** zu lesen.

Gemessene Laufzeiten je Bot (`--voll`, 20 Permutationen):

| Bot | ein Lauf | 20 Läufe |
|---|---|---|
| `elliott_wave_stocks` | 12,9 s | 260 s |
| `turtle_soup_stocks` | 6,3 s | 130 s |
| `volatility_breakout` | 5,9 s | 130 s |
| `rsi2_mean_reversion` | 5,5 s | 121 s |
| `elliott_wave` | 4,0 s | 81 s |
| `t3_supertrend` | 1,5 s | 30 s |
| `turtle_soup_crypto` | 0,6 s | 12 s |
| `rsi2_crypto` | 0,4 s | 8 s |
| `volatility_breakout_crypto` | 0,4 s | 7 s |
| **gesamt** | | **800 s** |

### Drei Stellschrauben, begründet

**(a) Die Zahl N.** Voreinstellung **20** — die Zahl aus der Analyse. Sie ist
nicht statistisch begründet und muss es nicht sein: gesucht wird kein
Erwartungswert, sondern ein **Gegenbeispiel**. Schon zwei Permutationen mit
verschiedenem Ergebnis beweisen versteckten Zustand. Die 20 sind da, um die
Streuung mit einer brauchbaren Spanne zu beziffern. Gemessen: der
**Schnellmodus mit fünf Permutationen liefert bei allen neun Bots dasselbe
Urteil**, nur engere Spannen (z. B. `volatility_breakout` 145..226 statt
145..269).

**(b) Ein Zwischenspeicher je Symbol — der sich zuerst beweisen muss.** Der
teure Teil (Kursdaten einlesen, Indikatoren, Wellenerkennung) läuft je Symbol
unabhängig. Ein Speicher darüber macht die Läufe 2..N fast kostenlos — setzt
aber genau das voraus, was hier gemessen werden soll. Deshalb rechnet der
Speicher die ersten `--pruef-laeufe` Wiederholungen **trotzdem voll durch**
und vergleicht jedes Symbolergebnis mit dem gespeicherten. Eine Abweichung
wäre ein Befund („Signalerzeugung reihenfolgeabhängig"), kein Speicherfehler.

Mindestens **eine** echte Wiederholung ist erzwungen (`max(1, pruef_laeufe)`),
und das nicht nur wegen des Speichers: nur in einem echten Ladevorgang sieht
die Wache die **tatsächliche** Ladereihenfolge des Bots (Abschnitt 7).

**(c) `--voll` für die Bestandsaufnahme, Speicher für die Routine.** Die
Zahlen dieses Berichts stammen alle aus `--voll`. Dass beide Wege dasselbe
liefern, prüft `shared/test_determinismus.py` (Abschnitt 7 dort) und
Schritt 7 des Testauftrags.

**Der Schnellmodus läuft in 101 s** — alle neun Bots, fünf Permutationen, ein
Prüflauf. Damit ist er für einen nächtlichen Cronjob geeignet
(`python3 shared/determinismus.py --schnell`, Rückgabewert 1 bei Befund).

---

## 6. Die offene Frage zur Zuteilungsregel — benannt, nicht gelöst

Der naheliegende nächste Schritt ist eine **Zuteilung nach Signalstärke**
statt nach Dateireihenfolge. Ob das trägt, hängt an einer Zahl: wie viele
verschiedene Werte die Signalstärke überhaupt annehmen kann. Gemessen
(`research/determinismus/signalstaerke.py`):

| Bot | Trades | mit gleichem Einstieg | grösste Gruppe | Stärkemass | Stufen | bleibt gleichauf |
|---|---|---|---|---|---|---|
| `elliott_wave` | 130 | 44 (33,8 %) | 4 | `fib_score` | 5 | 9 (20,5 %) |
| `elliott_wave_stocks` | 510 | 300 (58,8 %) | 20 | `fib_score` | 5 | **144 (48,0 %)** |
| `rsi2_crypto` | 439 | 289 (65,8 %) | 9 | — | — | — |
| `rsi2_mean_reversion` | 5391 | 4888 (90,7 %) | 46 | — | — | — |
| `t3_supertrend` | 980 | 429 (43,8 %) | 9 | — | — | — |
| `turtle_soup_crypto` | 1599 | 1349 (84,4 %) | 20 | — | — | — |
| `turtle_soup_stocks` | 12069 | 11641 (96,5 %) | 68 | — | — | — |
| `volatility_breakout` | 4510 | 3955 (87,7 %) | 24 | — | — | — |
| `volatility_breakout_crypto` | 233 | 142 (60,9 %) | 8 | — | — | — |

Zwei Befunde:

**Erstens: bei `elliott_wave_stocks` löst eine Rangregel auf dem `fib_score`
knapp die Hälfte der Fälle nicht.** Der Score kann oberhalb seiner Schwelle
nur fünf Werte annehmen (0,33 / 0,34 / 0,66 / 0,67 / 1,0 — gemessen, genau die
im Auftrag genannten). 300 der 510 Trades teilen ihren Einstiegszeitpunkt mit
mindestens einem anderen, die grösste Gruppe umfasst 20 Titel. Nach einer
Rangregel auf dem `fib_score` bleiben **144 Trades (48,0 % der gleichzeitigen,
28,2 % aller)** gleichauf. Für sie müsste weiterhin etwas anderes entscheiden.

Dass dieser Rest zahlengleich mit den 144 umstrittenen Trades aus Abschnitt 4
ausfällt, ist Zufall — es sind zwei unabhängig gerechnete Grössen über
verschiedene Mengen (dort: Trades, deren Ausführung über die Permutationen
schwankt; hier: Trades, die eine Rangregel nicht entscheidet). Aus der
Gleichheit folgt nichts; die Grössenordnung ist die Aussage: eine Rangregel
auf fünf Stufen räumt bei diesem Bot etwa die Hälfte der Konkurrenzfälle
nicht aus.

Das in TB-20 eingeführte Zweitkriterium (`end_time` absteigend) hilft hier
nicht: es entscheidet zwischen mehreren Wellenmustern **eines** Symbols. Bei
der Zuteilung konkurrieren **verschiedene Symbole zum selben Balken** — alle
Bewerber haben denselben Einstiegszeitpunkt.

**Zweitens: sieben der neun Bots führen überhaupt kein Mass für Signalstärke
mit.** RSI-2, Turtle Soup, Volatility Breakout und T3/SuperTrend erzeugen
Trades ohne Güte-Spalte. Eine Zuteilung nach Signalstärke müsste dort erst
eine einführen — und das wäre eine **Strategieänderung**, keine Rangregel.
Dieselbe Unterscheidung hat TB-20 schon einmal getroffen, als „grössere
Amplitude" als Zweitkriterium verworfen wurde, weil es über
`target_price = entry + total_move * TAKE_PROFIT_FIB` das Kursziel verschoben
hätte.

**Nicht gelöst, sondern benannt.** Die naheliegende Regel greift bei zwei
Bots nur zur Hälfte und bei sieben gar nicht. Was stattdessen zu tun ist, ist
eine eigene Aufgabe.

---

## 7. Wie die Prüfung sich selbst absichert

Prinzip 7.12 des Übergabeprotokolls: *„Eine grüne Prüfung ist erst dann etwas
wert, wenn belegt ist, dass sie auch rot werden kann."* Hier ist die Lage
umgekehrt — das Werkzeug meldet fast überall rot. Die gefährlichere Frage
lautet deshalb: **kann es überhaupt grün?** Und: **meldet es grün, wenn es
gar nicht gemessen hat?**

`shared/test_determinismus.py` (**49 Prüfungen, alle bestanden**, ~40 s)
beantwortet beides an **echtem Bot-Code**: eine wegwerfbare Kopie von
`turtle_soup_crypto` in einem temporären Projektbaum, dreimal in
unterschiedlichem Zustand.

| Zustand | Erwartung | Ergebnis |
|---|---|---|
| **unverändert** | Befund | NICHT DETERMINISTISCH, Ursache Zuteilung |
| **gehärtet** — totale Sortierung (`entry_time, symbol, exit_time`, stabil), kein Positionslimit, Allokation 0,01 % | **kein** Befund | DETERMINISTISCH, Kapitalpfad Zeile für Zeile gleich, 0 umstrittene Trades |
| **gehärtet + genau ein Fehler** — Zuteilung nach Dateirang bei 3 Plätzen für 24 Symbole | Befund | NICHT DETERMINISTISCH, Signalmenge weiterhin identisch |

Der dritte Zustand ist die Mutationsprobe in ihrer strengen Form: er geht vom
**nachweislich grünen** Fall aus und ändert genau eine Sache. Wäre der rote
Fall stattdessen der unveränderte Bot mit seinen mehreren gleichzeitigen
Ursachen, könnte eine zweite Wache das Fehlen der ersten verdecken — der Test
wäre rot, ohne dass klar wäre, welche Zusicherung ihn rot gemacht hat. Beide
Einzelteile sind für sich genommen harmlos: das Limit allein entscheidet
nichts, weil die gehärtete Sortierung total ist; die Rangsortierung allein
entscheidet nichts, weil ohne knappe Plätze jeder Trade zum Zug kommt.

### Die falsche Entwarnung

Der teuerste Fehler dieses Werkzeugs wäre nicht ein falscher Alarm, sondern
eine falsche Entwarnung: kommt die Permutation gar nicht im Bot an, rechnet es
N-mal dasselbe und meldet neun deterministische Bots. Dagegen stehen zwei
Dinge:

* `_ladeordnung_pruefen()` vergleicht nach **jedem** Lauf die tatsächlich
  geladene Symbolfolge mit der angeforderten Permutation und meldet **UNKLAR**
  statt DETERMINISTISCH, wenn sie nicht übereinstimmt. UNKLAR zählt als
  Befund; ein Lauf, der nicht durchlief, ist keine Entwarnung.
* Der Test setzt genau diesen Zustand künstlich her — eine Kopie, deren
  `load_all_symbol_data()` die Symbole immer alphabetisch durchläuft — und
  verlangt UNKLAR. Bei der ersten Fassung des Zwischenspeichers ist dieser
  Test **tatsächlich fehlgeschlagen**: der Speicher baute den Datensatz in der
  angeforderten Reihenfolge nach und machte damit die Wache blind. Behoben,
  indem ein frisch geladener Datensatz unverändert durchgereicht wird.

**Bekannte Grenze:** ein Bot, der sein Universum absichtlich selbst sortiert,
würde als UNKLAR gemeldet, nicht als DETERMINISTISCH. Das ist bewusst so — bei
ihm misst die Permutation nichts, und ein grünes Licht wäre irreführend. Keiner
der neun Bots tut das; alle neun laufen `for symbol in SYMBOLS`.

### Der Ablauf, nicht nur das Ergebnis

Eine Probe, deren Zustand der Test selbst herstellt, bestätigt sich selbst.
Deshalb beobachtet der Test den **Ablauf**: die Kopie schreibt bei jedem
Ladevorgang mit, welche Symbolreihenfolge sie tatsächlich gesehen hat. Geprüft
wird daran, dass der Bot N-mal mit N **verschiedenen** Reihenfolgen derselben
Symbolmenge aufgerufen wurde und dass der erste Aufruf die unveränderte
Originalreihenfolge sah.

---

## 8. Es wurde nichts verändert

```
$ git status --porcelain
?? research/determinismus/
?? shared/determinismus.py
?? shared/determinismus_lauf.py
?? shared/test_determinismus.py

$ git diff origin/main HEAD --name-only
research/determinismus/BERICHT.md
research/determinismus/ERGEBNIS.md
research/determinismus/TESTAUFTRAG_TB-23.md
research/determinismus/ergebnisse/...
research/determinismus/signalstaerke.py
shared/determinismus.py
shared/determinismus_lauf.py
shared/test_determinismus.py
```

Ausschliesslich **neue** Dateien unter `shared/` und `research/`. Keine
bestehende Datei wurde geändert.

Strukturell abgesichert, nicht bloss versprochen:

* **`RESULTS_DIR` zeigt während jedes Laufs in einen temporären Ordner** —
  dasselbe Mittel wie in `shared/kurven_lauf.py`. Das Werkzeug kann
  `results/<bot>/equity_curve.csv` gar nicht überschreiben.
* **Die Symboldateien werden nur gelesen.** Permutiert wird im Speicher, an
  der Stelle, an der die Liste in den Bot eintritt
  (`multi_symbol_optimise.SYMBOLS`).
* **`shared/ergebniskurven.py` meldet nach dem Lauf 9× AKTUELL**,
  Rückgabewert 0 — alle neun Kurven Zeile für Zeile identisch zur
  abgelegten Fassung.
* **`shared/test_determinismus.py`, Abschnitt 8** prüft `git status` und
  zusätzlich Grösse und Zeitstempel aller Symboldateien und abgelegten
  Ergebnisdateien vor und nach dem Testlauf.
* **Die Bot-Module werden nie in den Prozess des Werkzeugs importiert** — ein
  Subprozess je Bot, wie in `shared/portfolio_overview.py` und
  `shared/ergebniskurven.py`. Neun gleichnamige `equity_simulation.py` würden
  in `sys.modules` kollidieren.
* **`shared/kursdaten.py` greift** — nicht von hier aus, sondern dort, wo die
  Daten ins Programm kommen: alle neun `load_all_symbol_data()` rufen seit
  PR #81 `entferne_unvollstaendige()` auf, und das ist der Weg, über den jeder
  `__main__`-Block seine Daten holt. Eine zweite Filterung im Werkzeug wäre
  eine zweite Wahrheit über dieselben Daten.

### Bestehende Tests

Basislauf auf unverändertem `main` (Cloud-Umgebung) und nach dieser Arbeit:
**identisch**. Rot waren vorher wie nachher `broker/test_ibkr.py` (`tzdata`),
`dashboard/test_dashboard.py` und `dashboard/test_portfolio_sicht.py`
(`fastapi`, zusätzlich fehlt `node`), `shared/test_kursdaten.py` (`yfinance`)
und `research/hrp_portfolio/test_hrp_core.py` (`scipy`) — alle wegen
fehlender Abhängigkeiten, keiner wegen dieser Arbeit. `test_drawdown.py` und
`test_params.py` liefern ohne Bot-Argument nur ihre Nutzungszeile.

---

## 9. Was daraus folgt — und was nicht

**Folgt daraus:**

* Jede Zahl in `results/<bot>/equity_curve.csv` und jede daraus abgeleitete
  Aussage ist **eine von vielen gleichermassen legitimen**. Bei
  `volatility_breakout` liegt die Bandbreite bei 124 Prozentpunkten Rendite.
* Die Ursache sitzt an **einer** Stelle — der Zuteilung in
  `simulate_portfolio()` —, nicht verstreut in neun Strategien. Die
  Signalerzeugung ist sauber.
* Bei `volatility_breakout` greift das Positionslimit von 15 nie; bindend ist
  dort die Kapitalschranke bei 10 Positionen. Das ist unabhängig von dieser
  Frage einen eigenen Blick wert.

**Folgt daraus NICHT:**

* Dass die Live-Bots betroffen wären. Gemessen wurde der Backtest-Pfad.
* Dass eine bestimmte Reparatur die richtige ist. Abschnitt 6 zeigt, dass die
  naheliegende es nicht ist.
* Dass die heutigen Live-Parameter falsch sind. Diese Frage beantwortet
  `research/drawdown_reihenfolge/`.

**Offene Punkte für Folgeaufgaben:**

1. Eine Zuteilungsregel, die auch dort greift, wo es kein Mass für
   Signalstärke gibt (sieben von neun Bots).
2. Die 19 weiteren `sort_values`-Aufrufe ohne `kind="stable"` (TB-19).
3. `volatility_breakout`: Limit 15 bei rechnerisch höchstens 10 finanzierbaren
   Positionen.
4. `shared/determinismus.py --schnell` als nächtlicher Cronjob — dieser
   Bericht legt keinen an (`system/` und Crontab bleiben unberührt).

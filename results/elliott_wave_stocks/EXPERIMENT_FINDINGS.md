# Experimente: Offene Punkte aus dem Übergabeprotokoll (Abschnitt 9, Punkte 1 & 2)

Stand: 2026-09-02. Beide Experimente nutzen die aktuellen Live-Parameter
(`live_params.py`: Zigzag 5%, Stop-Loss 3%, Take-Profit-Fib 0.236,
Positionslimit 8) als Fixpunkt und variieren jeweils **nur eine** Dimension —
analog zum isolierten VWAP-Filter-Test beim T3-Bot. Jede Variante wurde sowohl
über den **gesamten** Datenzeitraum (`RECENT_YEARS_ONLY=10`) als auch **isoliert
auf Out-of-Sample-Daten** (letzte 30% je Symbol, keine Re-Optimierung) geprüft,
damit ein Effekt nicht auf Overfitting beruhen kann.

Reproduzierbar mit:
```
python3 strategies/elliott_wave_stocks/experiment_position_limit.py
python3 strategies/elliott_wave_stocks/experiment_no_take_profit.py
```

---

## 1. MAX_CONCURRENT_POSITIONS (Punkt 2)

| Limit | Endkapital (gesamt) | Rendite (gesamt) | Max DD (gesamt) | Endkapital (OOS) | Rendite (OOS) | Max DD (OOS) |
|---|---|---|---|---|---|---|
| 3 | 74.666 | +646,7% | -1,32% | 18.013 | +80,1% | -1,32% |
| 5 | 120.960 | +1109,6% | -1,65% | 19.801 | +98,0% | -1,65% |
| **8 (aktuell live)** | 160.053 | +1500,5% | -1,90% | 20.787 | +107,9% | -1,65% |
| unbegrenzt | 177.556 | +1675,6% | -2,52% | 20.939 | +109,4% | -1,65% |

**Befund:** Anders als beim T3-Bot (Krypto, Sweet Spot bei 5, kein Zusatznutzen
über 5 hinaus) steigt die Rendite bei Aktien **monoton** mit höherem Limit, bei
weiterhin sehr kleinem Drawdown (selbst unbegrenzt nur -2,52%). Grund
vermutlich geringere Korrelation zwischen 150 Aktien aus unterschiedlichen
Sektoren vs. 25 stark mitlaufenden Kryptos — das Klumpenrisiko, das
`MAX_CONCURRENT_POSITIONS` eigentlich adressiert, tritt hier kaum auf; das
Limit kostet stattdessen hauptsächlich entgangene Trades (mehr "skipped
trades" bei niedrigerem Limit). Aktuelles Limit von 8 ist eher konservativ,
nicht zu aggressiv gewählt.

**Einordnung:** OOS bestätigt den Trend (kein Overfitting-Warnsignal), aber
die Unterschiede sind auf OOS-Basis absolut kleiner (nur 132 Trades) als auf
dem Gesamtzeitraum — bei einer Entscheidung für "unbegrenzt" sollte man sich
bewusst sein, dass eine echte Marktkrise mit branchenübergreifendem Abverkauf
(anders als in den Testdaten) das Klumpenrisiko-Argument wieder relevanter
machen könnte, auch wenn es historisch hier nicht sichtbar wurde.

---

## 2. Take-Profit aus ("Gewinne laufen lassen", Punkt 1)

| Variante | Trades | Win Rate | Ø PnL/Trade | Endkapital (gesamt) | Rendite (gesamt) | Max DD (gesamt) | Endkapital (OOS) | Rendite (OOS) | Max DD (OOS) |
|---|---|---|---|---|---|---|---|---|---|
| **Mit Take-Profit (aktuell live)** | 519 | 86,7% | 6,47% | 160.053 | +1500,5% | -1,90% | 20.787 | +107,9% | -1,65% |
| Ohne Take-Profit | 519 | 43,9% | 14,88% | 318.409 | **+3084,1%** | -9,79% | 30.366 | **+203,7%** | -5,04% |

**Befund:** Bestätigt die früheren isolierten Tests (Ø-Gewinn 14,88% vs.
6,47%), und zeigt jetzt zusätzlich in Kombination mit dem validierten
Top-150-Setup: Rendite verdoppelt sich in etwa (sowohl Gesamtzeitraum als auch
OOS), Drawdown steigt deutlich, bleibt aber absolut klein und weit unter dem
Buy-and-Hold-Drawdown (-34,83%). Win Rate sinkt stark (86,7%→43,9%), da ohne
festes Ziel viele kleine/mittlere Gewinne nicht mehr realisiert werden,
sondern bis Stop-Loss oder Zeitlimit laufen — dafür sind die realisierten
Gewinne im Schnitt deutlich größer. Auch hier bestätigt der OOS-Check den
Effekt unabhängig (kein Overfitting-Muster: Rendite-Verhältnis und
Drawdown-Verhältnis bleiben in ähnlicher Größenordnung wie im Gesamtzeitraum).

**Nebeneffekt:** Ohne Take-Profit bleiben Positionen im Schnitt länger offen
→ mehr "skipped trades" durchs Positionslimit (231 statt 50 im Gesamtzeitraum).
Die naheliegende Folgefrage — profitiert "kein Take-Profit" besonders stark
von einem höheren Limit? — wird in Abschnitt 3 beantwortet.

---

## 3. Kombinierter Test: Take-Profit x Positionslimit (Folgeschritt)

Volle 2×4-Matrix (`experiment_combined.py`), gleiche feste Parameter wie oben.

**Gesamtzeitraum:**

| Take-Profit | Limit | Endkapital | Rendite | Trades ausgeführt/übersprungen | Max DD |
|---|---|---|---|---|---|
| mit | 3 | 74.666 | +646,7% | 354 / 165 | -1,32% |
| mit | 5 | 120.960 | +1109,6% | 426 / 93 | -1,65% |
| mit | 8 (aktuell live) | 160.053 | +1500,5% | 469 / 50 | -1,90% |
| mit | unbegrenzt | 177.556 | +1675,6% | 483 / 36 | -2,52% |
| ohne | 3 | 58.240 | +482,4% | 118 / 401 | -3,89% |
| ohne | 5 | 131.670 | +1216,7% | 189 / 330 | -7,03% |
| ohne | 8 | 318.409 | +3084,1% | 288 / 231 | -9,79% |
| **ohne** | **unbegrenzt** | **452.202** | **+4422,0%** | 330 / 189 | -10,71% |

**Out-of-Sample (letzte 30%, keine Re-Optimierung):**

| Take-Profit | Limit | Endkapital | Rendite | Trades ausgeführt/übersprungen | Max DD |
|---|---|---|---|---|---|
| mit | 3 | 18.013 | +80,1% | 108 / 24 | -1,32% |
| mit | 5 | 19.801 | +98,0% | 125 / 7 | -1,65% |
| mit | 8 (aktuell live) | 20.787 | +107,9% | 131 / 1 | -1,65% |
| mit | unbegrenzt | 20.939 | +109,4% | 132 / 0 | -1,65% |
| ohne | 3 | 20.263 | +102,6% | 34 / 98 | -2,86% |
| ohne | 5 | 26.245 | +162,5% | 49 / 83 | -3,79% |
| ohne | 8 | 30.366 | +203,7% | 74 / 58 | -5,04% |
| **ohne** | **unbegrenzt** | **32.575** | **+225,8%** | 87 / 45 | -4,97% |

**Befund:** Die Hypothese bestätigt sich klar. Bei Limit 3 schneidet "ohne
Take-Profit" sogar **schlechter** ab als "mit Take-Profit" (weniger Rendite,
mehr Drawdown) — die langen Haltedauern ohne festes Ziel lassen zu viele
Trades am engen Limit scheitern (401 übersprungen bei Limit 3 vs. 165 bei
"mit Take-Profit"). Erst mit steigendem Limit dreht sich das Bild: bei
unbegrenztem Limit erzielt "ohne Take-Profit" sowohl im Gesamtzeitraum
(+4422% statt +1676%) als auch Out-of-Sample (+226% statt +109%) klar das
beste Ergebnis der gesamten Matrix — bei OOS-Drawdown von -4,97%, kaum
höher als bei Limit 8 (-5,04%) und weiterhin weit unter dem
Buy-and-Hold-Drawdown von -34,83%. Die Kombination beider Änderungen ist
also kein Nullsummenspiel, sondern verstärkt sich gegenseitig.

---

## 4. Vertiefung vor Entscheidung: Kapitalallokation, Exit-Logik, Concurrency

Auf Nutzerwunsch vor der Entscheidung genauer geklärt (`experiment_concurrency_stats.py`):

**Kein simuliertes Leverage möglich.** `simulate_portfolio` (`equity_simulation.py`)
berechnet `allocation = capital * allocation_pct` (10% des *aktuellen
Gesamtkapitals*) und führt einen Entry nur aus, wenn `allocation <=
free_capital`. Das begrenzt die gebundene Kapitalsumme implizit auf ≤100% des
Kapitals — bei "unbegrenztem" Positionslimit werden also nicht beliebig viele
Positionen gleichzeitig eröffnet, sondern die 10%-Allokation selbst wirkt als
natürliche Obergrenze von rechnerisch ~10 Positionen.

**Exit ohne Take-Profit:** Nur zwei Wege — Stop-Loss oder Zeit-Exit nach
`MAX_HOLD_HOURS` (90 Handelstage) zum Schlusskurs des letzten Balkens. Kein
Gegensignal-Exit (`backtest_elliott.py`, `simulate_trade`).

**Tatsächliche Concurrency, "ohne Take-Profit"-Varianten (gemessen bei jedem Entry-Event):**

| Variante | Ø offene Positionen | Median | Maximum | Ø Kapitalauslastung | Max. Kapitalauslastung |
|---|---|---|---|---|---|
| mit TP, Limit 8 (live) | 2,88 | 2 | 8 | 28,6% | 80,0% |
| ohne TP, Limit 8 | 5,72 | 6 | 8 | 56,1% | 81,4% |
| **ohne TP, unbegrenzt** | **6,70** | **7** | **11** | **65,4%** | **100,0%** |

"Unbegrenzt" bedeutet in der Praxis also **maximal 11 statt 8 gleichzeitig
offene Positionen** (im Schnitt ~7) — nicht 15+ oder tatsächlich unbeschränkt.
Der Renditeunterschied zu Limit 8 kommt daher, dass in seltenen Phasen mit
9–11 gleichzeitigen Signalen (bei "ohne TP" häufiger als bei "mit TP", da
Positionen länger offen bleiben) diese zusätzlichen Trades nicht mehr am
Limit scheitern.

**⚠️ Wichtiger Zusatzbefund — `forward_test.py` (Live-Skript) unterstützt
aktuell keine der beiden Änderungen:**
- Kein `USE_TAKE_PROFIT`-Schalter: `target_price` wird immer gesetzt und
  immer geprüft (Zeilen ~170, ~111) — ein reiner `live_params.py`-Wertewechsel
  hätte hier keine Wirkung.
- `MAX_CONCURRENT_POSITIONS = None` würde bei `if open_count >=
  MAX_CONCURRENT_POSITIONS:` (Zeile ~155) einen `TypeError` auslösen und den
  Cronjob abbrechen lassen.

Eine Übernahme braucht also zusätzlich zu `live_params.py` eine kleine
Anpassung in `forward_test.py` (Take-Profit-Schalter ergänzen, `None`-Fall
beim Limit behandeln) — sonst weicht das Live-Verhalten vom getesteten
Backtest-Verhalten ab bzw. der Cronjob bricht ab.

---

## Empfehlung (zur Entscheidung, nicht automatisch übernommen)

Alle drei getesteten Varianten zeigen ein konsistentes Out-of-Sample-Signal
(Prinzip aus Protokoll Abschnitt 7.1: OOS zählt am meisten). Die stärkste
Variante ist die Kombination **kein Take-Profit + unbegrenztes Positionslimit**
(praktisch: max. 11 statt 8 Positionen) — bestes Rendite-Ergebnis auf beiden
Zeiträumen, Drawdown steigt gegenüber dem aktuellen Live-Stand deutlich
(-1,9%→-10,7% Gesamtzeitraum bzw. -1,65%→-4,97% OOS), bleibt aber in beiden
Fällen weit unter dem Buy-and-Hold-Risiko. Kein simuliertes Leverage in
keinem der Fälle (siehe Abschnitt 4). `live_params.py` **und**
`forward_test.py` wurden bewusst **nicht** verändert — das bleibt wie im
Protokoll (Abschnitt 8) festgelegt ein manueller Freigabe-Schritt, und
`forward_test.py` braucht ohnehin eine eigene Anpassung (siehe Abschnitt 4).
Rohdaten liegen als CSV in diesem Ordner:
`experiment_position_limit_full.csv`, `experiment_position_limit_oos.csv`,
`experiment_no_take_profit_full.csv`, `experiment_no_take_profit_oos.csv`,
`experiment_combined_full.csv`, `experiment_combined_oos.csv`.

---

## 5. Trailing-Take-Profit (Folgeexperiment nach Live-Rollout von "kein Take-Profit")

Stand: 2026-09-03. **Rein analytisch — `live_params.py` und `forward_test.py`
wurden für dieses Experiment NICHT verändert.** Vergleicht den seit
2026-09-03 live laufenden Stand (kein festes Take-Profit-Ziel, Positionslimit
8) gegen einen nachziehenden Stop-Loss: Der Stop wandert mit dem seit
Einstieg erreichten Kurshöchststand nach oben mit (fester Abstand X%
darunter), der ursprüngliche feste Stop (3% unter Einstieg) bleibt aktiv, bis
der Trailing-Stop ihn überholt. Implementiert in
`experiment_trailing_take_profit.py` (eigene, von `backtest_elliott.py`
unabhängige Simulationslogik, um die produktiv genutzten Backtest-Dateien
nicht anzufassen). Positionslimit für alle Varianten fix bei 8, identisch
zum Live-Stand, für einen fairen Vergleich.

**Gesamtzeitraum:**

| Variante | Trades ausgeführt | Endkapital | Rendite | Max DD | Ø Haltedauer (Tage) |
|---|---|---|---|---|---|
| Baseline: kein Take-Profit (live) | 288 | 318.409 | +3084,1% | -9,79% | 71,4 |
| Trailing 5% (ab Einstieg) | 455 | 318.122 | +3081,2% | **-0,10%** | 13,3 |
| Trailing 8% (ab Einstieg) | 411 | 307.729 | +2977,3% | -0,95% | 28,9 |
| Trailing 12% (ab Einstieg) | 365 | 236.655 | +2266,6% | -3,48% | 46,9 |
| Trailing 15% (ab Einstieg) | 331 | 287.971 | +2779,7% | -4,37% | 57,2 |
| Trailing 8%, aktiv erst ab +8% Gewinn | 408 | **330.211** | **+3202,1%** | -1,40% | 30,0 |
| Trailing 12%, aktiv erst ab +10% Gewinn | 365 | 236.655 | +2266,6% | -3,48% | 46,9 |

**Out-of-Sample (letzte 30%, keine Re-Optimierung):**

| Variante | Trades ausgeführt | Endkapital | Rendite | Max DD | Ø Haltedauer (Tage) |
|---|---|---|---|---|---|
| Baseline: kein Take-Profit (live) | 74 | 30.366 | **+203,7%** | -5,04% | 66,6 |
| Trailing 5% (ab Einstieg) | 125 | 24.283 | +142,8% | **-0,04%** | 12,3 |
| Trailing 8% (ab Einstieg) | 110 | 25.584 | +155,8% | -0,95% | 30,7 |
| Trailing 12% (ab Einstieg) | 98 | 25.442 | +154,4% | -3,48% | 49,4 |
| Trailing 15% (ab Einstieg) | 89 | 27.166 | +171,7% | -4,37% | 57,6 |
| Trailing 8%, aktiv erst ab +8% Gewinn | 110 | 25.427 | +154,3% | -1,40% | 30,8 |
| Trailing 12%, aktiv erst ab +10% Gewinn | 98 | 25.442 | +154,4% | -3,48% | 49,4 |

### Beantwortung der drei Leitfragen

**1. Gibt es eine Variante mit besserer Rendite UND geringerem Drawdown als der Live-Stand?**
Im **Gesamtzeitraum** ja: "Trailing 8%, aktiv erst ab +8% Gewinn" schlägt die
Baseline auf beiden Achsen (+3202% statt +3084% Rendite, -1,40% statt -9,79%
Drawdown). **Out-of-Sample zeigt sich das genaue Gegenteil**: Dort ist die
Baseline (kein Take-Profit) bei der Rendite die **beste** aller sieben
Varianten (+203,7%), jede Trailing-Variante liegt OOS bei der Rendite
darunter (142,8%–171,7%) — nur beim Drawdown bleiben die Trailing-Varianten
OOS weiterhin klar überlegen. Es gibt also **keine** Variante, die OOS auf
beiden Achsen gleichzeitig besser ist als die Baseline.

**2. Ist der Effekt Out-of-Sample stabil?**
**Nein, nicht bei der Rendite — die Rangfolge kehrt sich nahezu um.**
Gesamtzeitraum-Rangfolge nach Rendite: Trailing 8%/+8%-Aktivierung >
Baseline > Trailing 5% > Trailing 8% > Trailing 15% > Trailing 12%.
Out-of-Sample-Rangfolge nach Rendite: **Baseline** > Trailing 15% >
Trailing 8% > Trailing 12% > Trailing 8%/+8%-Aktivierung > **Trailing 5%**
(im Gesamtzeitraum die Nummer 3, OOS die Nummer 6/letzte). Nach Prinzip 7.1
des Übergabeprotokolls ("nur Out-of-Sample-Ergebnisse zählen für
Entscheidungen") ist das ein klares Overfitting-Warnsignal (siehe auch
Prinzip 7.7, Parameter-Instabilität) — die im Gesamtzeitraum vielversprechend
wirkende Kombination ist auf ungesehenen Daten nicht die beste.
**Stabil ist dagegen die Drawdown-Reduktion selbst**: Jede Trailing-Variante
senkt den Drawdown sowohl im Gesamtzeitraum als auch OOS deutlich und in
konsistenter Größenordnung gegenüber der Baseline — dieser Teil des Effekts
ist robust, nur die Renditeseite nicht.

**3. Wie verändert sich die durchschnittliche Haltedauer?**
Deutlich kürzer, proportional zum Trailing-Abstand: von Ø 71,4 Tagen (Baseline,
Gesamtzeitraum) auf 13,3 Tage (Trailing 5%) bis 57,2 Tage (Trailing 15%) —
engere Trailing-Abstände realisieren Gewinne viel früher, was auch die
Vermutung stützt, warum sie OOS bei starken, anhaltenden Trends (wie im
OOS-Fenster 2023–2026) Rendite auf dem Tisch liegen lassen.

### Einordnung

Die "Trailing 8%, aktiv erst ab +8%"-Kombination sieht im Gesamtzeitraum wie
der gesuchte Free-Lunch-Fall aus, hält dieser Prüfung Out-of-Sample aber
**nicht** stand — nach der im Projekt etablierten Methodik (OOS zählt am
meisten) ist das kein belastbarer Fund, sondern ein Beispiel für genau das
Overfitting-Muster, vor dem Prinzip 7 warnt. Die robusteste, OOS-bestätigte
Erkenntnis ist die **Drawdown-Reduktion** selbst: Wer bereit ist, auf einen
Teil der Rendite zu verzichten (OOS ca. 143–172% statt 204%), kann den
Drawdown mit einem Trailing-Stop deutlich (auf einstellige Prozentwerte)
senken. Eine Variante, die "kostenlos" sowohl mehr Rendite als auch weniger
Risiko liefert, wurde in dieser Matrix nicht gefunden. `live_params.py` und
`forward_test.py` bleiben unverändert; keine Empfehlung zur Übernahme aus
diesem Experiment. Rohdaten:
`experiment_trailing_take_profit_full.csv`,
`experiment_trailing_take_profit_oos.csv`.

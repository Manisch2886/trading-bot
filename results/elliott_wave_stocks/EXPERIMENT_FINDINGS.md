# Experimente: Offene Punkte aus dem Übergabeprotokoll (Abschnitt 9, Punkte 1 & 2)

> ## ⚠️ ALLE ZAHLEN IN DIESER DATEI STAMMEN VON EINER BACKTEST-GRUNDLAGE MIT LOOK-AHEAD
>
> **Nachtrag vom 2026-09-13 (Befund TB-17). Der Text unterhalb dieses Kastens
> ist unverändert — er beschreibt einen Lauf, der so stattgefunden hat.**
>
> Die Experimente liefen im September 2026 gegen einen Backtest, der zum Preis
> des Wellenende-Pivots einstieg. Ein Zigzag-Pivot **ist** aber erst dann ein
> Pivot, wenn der Kurs sich danach um `deviation_pct` in die Gegenrichtung
> bewegt hat — der Einstieg erfolgte also zu einem Kurs, der zu diesem
> Zeitpunkt noch nicht als Signal bekannt sein konnte, und der Stop-Loss war
> bis zur Bestätigung mathematisch unerreichbar. Das ist der Grund für die
> durchweg sehr kleinen Drawdowns unten (−1,32 % bis −2,52 %): sie waren ein
> Rechenfehler, keine Strategieeigenschaft. Behoben in **PR #26**
> (`research/elliott_wave_lookahead/BERICHT.md`).
>
> **Was heute für die Live-Konfiguration gilt** (dev 5 % / Stop 3 % / kein
> Kursziel / Limit 8), gemessen auf kausal sauberer Grundlage:
>
> | | Rendite (10 Jahre) | Max Drawdown | Calmar |
> |---|---:|---:|---:|
> | Buy-and-Hold | **+755,69 %** | −34,83 % | 21,70 |
> | Live-Konfiguration | **+330,18 %** | **−22,70 %** | 14,55 |
>
> Quelle: `research/elliott_wave_params/BERICHT.md` Abschnitt 4 (PR #28).
> **Buy-and-Hold schlägt diesen Bot** in der Rendite und im Calmar-Verhältnis;
> keine der 252 dort geprüften Kombinationen kommt an die +755 % heran. Die
> erneuerte Ergebniskurve des Bots weist **+352,72 % bei −22,44 %** aus
> (PR #86) — die Differenz zu den +330,18 % ist kein Widerspruch, sondern die
> Zeilenreihenfolge bei gleichzeitigen Einstiegen: identischer Trade-Satz,
> stabile gegen instabile Sortierung (BERICHT.md, P-A5).
>
> ### Diese Zahlen bitte NICHT „korrigieren"
>
> Sie haben eine aktive Aufgabe: `research/elliott_wave_lookahead/` benutzt
> sie als **veröffentlichte Baseline** und weist damit nach, dass die
> Look-Ahead-Reproduktion den damaligen Lauf wirklich trifft — siehe
> `decisions.py` (`PUBLISHED_CELLS`: +1500,53 % / −1,90 % für „mit
> Take-Profit, Limit 8"; +3084,09 % / −9,79 % für „ohne Take-Profit,
> Limit 8") und `verify_baseline.py` (`PUBLISHED`). Wer die Tabellen unten
> überschreibt, zerstört diesen Nachweis. Deshalb steht hier ein Warnhinweis
> und keine Umrechnung.
>
> ### Was von den Befunden bleibt
>
> * **`USE_TAKE_PROFIT = False` hält** — die Entscheidung ruht seit PR #28
>   nicht mehr auf den Zahlen unten, sondern auf einer Rangfolge: unter den
>   116 Kombinationen, die die fünf Mindestbedingungen bestehen, arbeiten die
>   vorderen zehn praktisch ausnahmslos ohne festes Kursziel. Ein sauber
>   gerechnetes Gegenstück zum Paar „mit/ohne Kursziel" existiert dagegen
>   **nicht** — der gemessene Hebel der Entscheidung ist unbekannt.
> * **Die Empfehlung „unbegrenztes Positionslimit" (Abschnitt 3 und
>   Empfehlung) ist auf dieser Grundlage nicht mehr belastbar** und wurde nie
>   übernommen; `MAX_CONCURRENT_POSITIONS` steht weiter auf 8. Ob 8 die
>   richtige Zahl ist, ist nach wie vor ungeprüft (Übergabeprotokoll
>   Abschnitt 9, Punkt 1).
> * **Der Zusatzbefund zu `forward_test.py` in Abschnitt 4 gilt unverändert**
>   — er betrifft die Code-Struktur, nicht die Kennzahlen.
>
> **Eine Falle, die hier schon zugeschlagen hat:** Die abgelegte
> Ergebniskurve des Bots trug bis PR #86 die **+1500,53 % bei −1,90 %** aus
> Abschnitt 1/3 — also die Zahl der Variante **mit** Take-Profit, obwohl
> `USE_TAKE_PROFIT` am 2026-09-03 auf `False` gesetzt wurde. Sie war damit aus
> **zwei** unabhängigen Gründen veraltet: dem Look-Ahead und einer nach dem
> Parameterwechsel nie neu erzeugten Kurve. Die 469 ausgeführten Trades der
> alten Kurve entsprechen genau der Zelle „mit Take-Profit, Limit 8".

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

> ⚠️ **Look-Ahead-Grundlage — die Zahlen dieses Abschnitts gelten nicht mehr.** Siehe den Kasten am Dateianfang.

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

> ⚠️ **Look-Ahead-Grundlage — die Zahlen dieses Abschnitts gelten nicht mehr.** Siehe den Kasten am Dateianfang.

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

> ⚠️ **Look-Ahead-Grundlage — die Zahlen dieses Abschnitts gelten nicht mehr.** Siehe den Kasten am Dateianfang.

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

> ⚠️ **Look-Ahead-Grundlage — die Kennzahlen dieses Abschnitts gelten nicht mehr.** Der Zusatzbefund zu `forward_test.py` am Ende des Abschnitts gilt dagegen unverändert: er betrifft die Code-Struktur, nicht die Zahlen.

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

> ⚠️ **Diese Empfehlung ist auf Look-Ahead-Grundlage entstanden und wurde nie übernommen.** `MAX_CONCURRENT_POSITIONS` steht weiter auf 8. `USE_TAKE_PROFIT = False` wurde übernommen, hält aber aus einem anderen Grund als hier genannt — siehe den Kasten am Dateianfang.

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

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
Eine Kombination "kein Take-Profit + höheres/unbegrenztes Positionslimit"
wurde hier noch nicht gemeinsam getestet und wäre der naheliegende nächste
Schritt, falls beide Änderungen übernommen werden sollen.

---

## Empfehlung (zur Entscheidung, nicht automatisch übernommen)

Beide Änderungen zeigen ein konsistentes Out-of-Sample-Signal (Prinzip aus
Protokoll Abschnitt 7.1: OOS zählt am meisten) und sprechen für sich klar für
eine Übernahme. `live_params.py` wurde bewusst **nicht** verändert — das
bleibt wie im Protokoll (Abschnitt 8) festgelegt ein manueller
Freigabe-Schritt. Rohdaten liegen als CSV in diesem Ordner:
`experiment_position_limit_full.csv`, `experiment_position_limit_oos.csv`,
`experiment_no_take_profit_full.csv`, `experiment_no_take_profit_oos.csv`.

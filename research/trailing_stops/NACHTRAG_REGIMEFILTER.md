# Nachtrag: `volatility_breakout_crypto` mit aktiviertem BTC-Regimefilter

**Punktuelle Korrektur eines einzigen Bots dieser Studie. `t3_supertrend` und
`volatility_breakout` sind nicht betroffen und wurden nicht neu gerechnet.**
Reine Backtest-Untersuchung, keine Live-Datei verändert, keine Aktivierungsempfehlung.

Skript: [`nachtrag_regimefilter.py`](nachtrag_regimefilter.py) ·
Ergebnis: `results/volatility_breakout_crypto_atr14_regimefilter_nachtrag.json`

---

## 0. Entscheidungsgrundlage

**Der Anlass.** Der Sync-Check (PR #24) hat belegt: die `equity_simulation.py`
von `volatility_breakout_crypto` wendet den in `live_params.py` aktivierten
`BTC_REGIME_FILTER_ENABLED = True` **nicht an**. Die Einstiegssignale dieser
Studie stammen aus derselben Quelle — die hier berichteten Zahlen für diesen Bot
beruhen also auf einer Trade-Grundlage, die der Live-Bot nie handelt.

**Diese Studie hat den Befund selbst vorhergesagt.** Abschnitt 0.4 nannte als
offenen Punkt: *„Für `volatility_breakout_crypto`: eine Aktivierung des
BTC-Regimefilters in der Backtest-Kette — ebenfalls ein
Risikoreduktions-Mechanismus, der mit dem Trailing-Stop **überlappen dürfte**."*
Dieser Nachtrag prüft genau das und beziffert die Überlappung.

**Warum nur dieser Bot.** Bei `t3_supertrend` und `volatility_breakout` fehlt im
Backtest kein Regimefilter (`research/sync_check/BERICHT.md`, Schritt 1); ihre
Befunde bleiben unverändert gültig. Die beiden Elliott-Wave-Bots waren schon in
der Erstfassung als nicht auswertbar eingestuft (Zigzag-Look-Ahead) — daran
ändert der Filter nichts.

**Was ausgetauscht wurde.** Allein die Trade-Grundlage. Es laufen die
unveränderten Funktionen dieser Studie (`run_one_bot.prepare`, `collect_trades`,
`evaluate`, `slice_period`, `decision_basis`) und die unveränderten
Regimefilter-Funktionen des Bots. **`k = 0,8956`, Trennzeitpunkt, Kalenderfenster,
Bootstrap-Seed, 2000 Replikate und 500 Permutationen bleiben identisch** — sonst
änderten sich mehrere Bezugsgrössen gleichzeitig.

**Regressionscheck vorweg.** Der ungefilterte Lauf reproduziert **28/28**
veröffentlichte Werte dieser Studie exakt (k, Rendite, Drawdown und ausgeführte
Trades für alle drei Varianten in allen drei Perioden). Ohne das bricht das
Skript ab.

**Stichprobengrösse.** Der Filter streicht **35,1 %** der Baseline-Trades
(359 → 233), beim ATR-Trailing 33,1 % (396 → 265). Out-of-Sample fällt die Basis
von **103 auf 64** bzw. von **140 auf 95** ausgeführte Trades — und genau darauf
stand der einzige positive Calmar-Befund dieser Studie.

---

## 1. Was sich ändert — und was nicht

Rendite % / Max Drawdown % / **Calmar**:

| Periode | Grundlage | A Baseline | B Fix-Trailing | C ATR-Trailing |
|---|---|---|---|---|
| Gesamt | ohne Filter | 71,26 / −16,77 / **4,25** | 48,15 / −7,39 / **6,52** | 45,65 / −5,76 / **7,93** |
| Gesamt | **mit Filter** | 49,03 / −16,29 / **3,01** | 21,75 / −7,84 / **2,77** | 30,29 / −5,41 / **5,60** |
| In-Sample | ohne Filter | 40,89 / −16,77 / **2,44** | 13,73 / −7,39 / **1,86** | 12,96 / −5,76 / **2,25** |
| In-Sample | **mit Filter** | 20,47 / −16,29 / **1,26** | 4,08 / −7,84 / **0,52** | 9,29 / −5,41 / **1,72** |
| Out-of-Sample | ohne Filter | 20,23 / −11,33 / **1,79** | 30,43 / −6,13 / **4,96** | 28,12 / −5,58 / **5,04** |
| Out-of-Sample | **mit Filter** | 23,00 / −7,76 / **2,96** | 17,13 / −5,44 / **3,15** | 19,20 / −5,09 / **3,77** |

**Belastbarkeit** — studieneigener Block-Bootstrap, 2000 Replikate, gepaart.
P(ATR-Trailing besser als Baseline), gesamt / IS / OOS:

| Grundlage | **Calmar** | **Max Drawdown** |
|---|---|---|
| ohne Filter | 73,8 % / 48,8 % / **95,0 %** | **100,0 % / 99,9 % / 99,2 %** |
| **mit Filter** | 61,1 % / 50,8 % / **64,6 %** | **99,2 % / 99,3 % / 97,3 %** |

**Die Drawdown-Aussage hält, die Calmar-Aussage fällt.** Der Satz aus
Abschnitt 0.3 — *„`volatility_breakout_crypto`: die Drawdown-Reduktion ist
praktisch sicher"* — gilt unverändert (P ≥ 97,3 %). Der zweite Teil des Urteils
(*„Calmar nur OOS"*, P = 95,0 %) trägt dagegen nicht mehr: **64,6 %** ist von
Rauschen nicht zu unterscheiden.

---

## 2. Die Zerlegung dreht sich um

Aus Abschnitt „A→B→C" dieser Studie:

| Grundlage | A | B | C | A→B (Nachziehen) | B→C (ATR-Kalibrierung) |
|---|---|---|---|---|---|
| ohne Filter | 4,25 | 6,52 | 7,93 | **+2,27** | +1,41 |
| **mit Filter** | 3,01 | **2,77** | 5,60 | **−0,24** | **+2,83** |

Die Erstfassung folgerte: *„Der weitaus grösste Teil des Effekts kommt vom
Nachziehen des Stops selbst, nicht von der Volatilitäts-Kalibrierung."* **Für
diesen Bot gilt das unter der Live-Konfiguration nicht mehr.** Das blosse
Nachziehen bringt gar nichts mehr (4,25 → 6,52 wird zu 3,01 → 2,77); der gesamte
verbleibende Vorteil entsteht erst durch die ATR-Kalibrierung.

Der Grund liegt auf der Hand, sobald man die Zeilen nebeneinander legt: der
fixe Trailing-Stop verliert mit Filter über den Gesamtzeitraum massiv Rendite
(48,15 % → 21,75 %) bei fast unverändertem Drawdown. Der Filter entfernt genau
die Phasen, in denen sich das enge Nachziehen ausgezahlt hatte.

Für `t3_supertrend` und `volatility_breakout` bleibt die Aussage der Erstfassung
unberührt — dort ist kein Filter im Spiel.

---

## 3. Reihenfolge-Empfindlichkeit auf gefilterter Grundlage

500 Permutationen, Calmar über den Gesamtzeitraum:

| Variante | berichtet | min … max | Median |
|---|---|---|---|
| A Baseline | 3,01 | 2,78 … 4,58 | **3,85** |
| B Fix-Trailing | 2,77 | 2,52 … 3,97 | 3,22 |
| C ATR-Trailing | 5,60 | 5,03 … 6,70 | 5,81 |

Zwei Beobachtungen:

* **Die Streubereiche von A und C überlappen sich nicht** (4,58 < 5,03). Über den
  Gesamtzeitraum ist der Calmar-Unterschied also grösser als die
  Reihenfolge-Willkür — genau wie ohne Filter (dort 2,98 … 4,90 gegen 6,65 … 8,95).
* **Der berichtete Baseline-Wert 3,01 liegt deutlich unter seinem eigenen Median
  (3,85).** Die zufällige Einlese-Reihenfolge stellt die Baseline also zu
  schlecht dar und den Trailing-Stop entsprechend zu gut. Beim Median-Vergleich
  schrumpft der Abstand von +2,59 auf +1,96. Die Perzentil-Einordnung dazu steht
  in PR #22, Nachtrag N6 (17,6. Perzentil).

---

## 4. Konsequenz für die Urteilstabellen dieser Studie

| Bot | Urteil Erstfassung | Urteil mit Live-Konfiguration |
|---|---|---|
| `t3_supertrend` | Verbesserung: **nein** (P = 2,4 %) | unverändert |
| `volatility_breakout` | **kein belastbarer Unterschied** | unverändert |
| `volatility_breakout_crypto` | Drawdown **ja** (P ≥ 99,2 %), Calmar **nur OOS** (P = 95,0 %) | Drawdown **ja** (P ≥ 97,3 %), **Calmar: nein** (P = 64,6 %) |

Der Schlusssatz der Erstfassung — *„die Drawdown-Wirkung lässt sich beziffern,
die risikoadjustierte Vorteilhaftigkeit nicht"* — **gilt damit für alle drei
auswertbaren Bots ohne Ausnahme.** In der Erstfassung war
`volatility_breakout_crypto` die einzige Teilausnahme; sie fällt weg.

Ebenfalls betroffen ist die Gegenüberstellung zur Vol-Sizing-Studie:
*„`volatility_breakout_crypto` ist sowohl der Vol-Sizing- als auch der
Trailing-Stop-Gewinner."* Unter der Live-Konfiguration ist er **keines von
beidem** — der Vol-Sizing-Befund kippt in PR #18 ebenfalls (siehe
`research/volatility_scaled_sizing/NACHTRAG_REGIMEFILTER.md`).

---

## 5. Getroffene Annahmen

**A1 — Der Filter wird nachträglich angewendet** (`filter_trades_by_regime`),
die Konvention des Projekts und die einzige referenzfähige Variante. Live
blockiert der Filter schon den Einstieg, sodass das Symbol frei bleibt. Der
Unterschied ist in PR #22 (Nachtrag N0) gemessen: **8 Trades (3,4 %)**, ohne
Auswirkung auf die Schlussfolgerung.

**A2 — `k` wird nicht nachkalibriert** (bleibt 0,8956) und **A3 — Trennzeitpunkt
und Kalenderfenster stammen aus dem ungefilterten Satz.** Beides, damit der
gemessene Unterschied allein dem Filter zuzuordnen ist.

**A4 — Buy-and-Hold bleibt unverändert übernommen** (19,45 % / −67,90 % / 0,29
über den Gesamtzeitraum). Es hängt weder am Stop noch am Filter, nur am Zeitraum
und an den Symbolen — beide unverändert.

**A5 — Die Robustheits-Illustration mit ATR-22 wurde nicht wiederholt.** Sie
diente der Frage, ob der Befund an der Fensterwahl hängt; diese Frage ist von der
Trade-Grundlage unabhängig und auftragsgemäss nicht Teil dieses Nachtrags.

---

## 6. Unabhängiger Gegencheck gegen PR #22

Dieser Nachtrag und die Vertiefungsstudie (PR #22, Nachtrag N) beantworten
dieselbe Frage über **zwei getrennte Kernmodule**: hier `atr_core.py` +
`decision_basis.py` dieser Studie, dort das eigenständig zusammengeführte
`vbc_core.py` + `bootstrap.py`. Die Ergebnisse sind **zahlengleich**:

| Grösse | dieser Nachtrag | PR #22 Nachtrag N |
|---|---|---|
| Trades nach Filter (Baseline / ATR) | 233 / 265 | 233 / 265 |
| Gesamt Baseline / ATR-Trailing (Calmar) | 3,01 / 5,60 | 3,01 / 5,60 |
| OOS Baseline / ATR-Trailing (Calmar) | 2,96 / 3,77 | 2,96 / 3,77 |
| P(Calmar besser), gesamt / IS / OOS | 61,1 / 50,8 / 64,6 | 61,1 / 50,8 / 64,6 |
| P(Drawdown besser), gesamt / IS / OOS | 99,2 / 99,3 / 97,3 | 99,2 / 99,3 / 97,3 |
| Reihenfolge-Streuung Baseline (Calmar) | 2,78 … 4,58 | 2,78 … 4,58 |

Zwei unabhängig geschriebene Implementierungen, dieselben Zahlen bis auf die
zweite Nachkommastelle. Die Konsistenz ist damit belegt, nicht behauptet.

---

## 7. Reproduktion

```
python3 nachtrag_regimefilter.py
```

Der Lauf bricht ab, falls der Regressionscheck gegen
`results/volatility_breakout_crypto_atr14.json` nicht durchgeht.

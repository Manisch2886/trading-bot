# Nachtrag: `volatility_breakout_crypto` mit aktiviertem BTC-Regimefilter

**Punktuelle Korrektur einer einzigen Zeile dieser Studie. Die übrigen acht Bots
sind nicht betroffen und wurden nicht neu gerechnet.** Reine Backtest-Untersuchung,
keine Live-Datei verändert, keine Aktivierungsempfehlung.

Skript: [`nachtrag_regimefilter.py`](nachtrag_regimefilter.py) ·
Ergebnis: `results/volatility_breakout_crypto_regimefilter_nachtrag.json`

---

## 0. Entscheidungsgrundlage

**Was der Anlass ist.** Der Sync-Check (PR #24) hat belegt: die
`equity_simulation.py` von `volatility_breakout_crypto` wendet den in
`live_params.py` aktivierten `BTC_REGIME_FILTER_ENABLED = True` **nicht an**.
Diese Studie hat ihre Trades für diesen Bot über genau jene Funktion bezogen —
die im Abschnitt „volatility_breakout_crypto" berichteten Zahlen beruhen also auf
einer Trade-Grundlage, die der Live-Bot nie handelt.

**Warum nur dieser eine Bot.** Laut `research/sync_check/BERICHT.md` (Schritt 1)
ist der Regimefilter die einzige Abweichung dieser Art; die übrigen vier
abweichenden Bots unterscheiden sich in Konstanten, die diese Studie ohnehin aus
`live_params.py` liest. Die vier synchronen Bots sind gar nicht betroffen.
**Die Kernaussage dieser Studie — Vol-Skalierung schadet bei 7 von 9 Bots — ist
davon unberührt.** Betroffen ist ausschliesslich einer der beiden Gewinner.

**Was verändert wurde und was nicht.** Ausgetauscht wurde **allein die
Trade-Grundlage**. Es laufen die unveränderten Funktionen dieser Studie
(`run_one_bot.load_bot_data`, `run_one_bot.analyze_period`, `vol_sizing_core`)
und die unveränderten Regimefilter-Funktionen des Bots
(`regime_filter.compute_btc_regime` / `filter_trades_by_regime`) — dieselben, die
`forward_test.py` live benutzt. Vol-Fenster 90, Allokation, Positionslimit,
Trennverhältnis, Gewichts-Normalisierung: alles unverändert.

**Regressionscheck vorweg (sonst zählt nichts).** Der ungefilterte Lauf
reproduziert **11/11** veröffentlichte Werte dieser Studie exakt — Trade-Anzahl,
Rendite, Drawdown und ausgeführte Trades in beiden Perioden, beide Varianten.
Erst danach zählt der gefilterte Lauf.

**Stichprobengrösse.** Der Filter streicht **35,1 %** der Trades (359 → 233). Die
Out-of-Sample-Basis fällt von **103 auf 64** ausgeführte Trades. Jede Aussage
über diese Periode trägt entsprechend wenig — in beide Richtungen.

---

## 1. Der Befund kippt

| Periode | Grundlage | ausgeführt | Rendite fix → vol | Max DD fix → vol | **Calmar fix → vol** | Urteil |
|---|---|---|---|---|---|---|
| In-Sample | ohne Filter | 209 | 40,89 % → 37,86 % | −16,77 % → −15,17 % | 2,44 → **2,50** | vol besser |
| In-Sample | **mit Filter** | 144 | 20,47 % → 11,65 % | −16,29 % → −16,09 % | 1,26 → **0,72** | **vol schlechter** |
| Out-of-Sample | ohne Filter | 103 | 20,23 % → 16,20 % | −11,33 % → −8,04 % | 1,79 → **2,01** | vol besser |
| Out-of-Sample | **mit Filter** | 64 | 23,00 % → 18,28 % | −7,76 % → −6,82 % | 2,96 → **2,68** | **vol schlechter** |

**Das Kriterium dieser Studie war „Verbesserung in-sample UND out-of-sample".
Ohne Filter: erfüllt. Mit Filter: in beiden Perioden nicht erfüllt.**

Die betroffene Passage des Berichts (Abschnitt „volatility_breakout_crypto")
lautet: *„**Verbesserung: ja** (in beiden Perioden verbessert sich die
Calmar-Ratio, … insbesondere Out-of-Sample: -11,3 % → -8,0 %)."* Unter der
Live-Konfiguration ist das **nicht mehr haltbar**: die Calmar-Ratio verschlechtert
sich in beiden Perioden.

---

## 2. Warum der Befund kippt

Die ursprüngliche Begründung stützte sich fast ganz auf die
Out-of-Sample-Drawdown-Verbesserung −11,3 % → −8,0 %. **Genau diese Verbesserung
liefert der Regimefilter bereits selbst**: mit Filter liegt der Drawdown der
fixen Variante schon bei −7,76 % — besser als das, was die Vol-Skalierung ohne
Filter erreichte. Was die Vol-Skalierung darüber hinaus noch beitragen kann
(−7,76 % → −6,82 %), wiegt den Renditeverlust (23,00 % → 18,28 %) nicht mehr auf.

Der Wert **−7,76 %** ist kein Ergebnis dieses Nachtrags, sondern steht seit dem
04.09.2026 in `live_params.py` als Begründung für die Filter-Aktivierung
(*„70/30: -11,33% -> -7,76%"*). Der Nachtrag rechnet ihn nach und trifft ihn
exakt — beide Seiten der dortigen Aussage. Das ist zugleich der stärkste
Regressionscheck dieses Nachtrags, weil die Zahl aus einer ganz anderen Rechnung
stammt.

**Die Vol-Skalierung war für diesen Bot also nie ein eigener Effekt, sondern eine
zweite Messung derselben Schutzwirkung** — nur die schlechtere von beiden, weil
sie mehr Rendite kostet.

---

## 3. Konsequenz für die Zusammenfassungstabelle

Die Zeile

| Bot | IS Rendite (fix→vol) | OOS Rendite (fix→vol) | OOS Drawdown (fix→vol) | Verbesserung | WF-stabil |
|---|---|---|---|---|---|
| volatility_breakout_crypto | 40,9→37,9 % | 20,2→16,2 % | -11,3→-8,0 % | **ja** | ja |

lautet unter der Live-Konfiguration:

| Bot | IS Rendite (fix→vol) | OOS Rendite (fix→vol) | OOS Drawdown (fix→vol) | Verbesserung | WF-stabil |
|---|---|---|---|---|---|
| volatility_breakout_crypto (Filter aktiv) | 20,5→11,7 % | 23,0→18,3 % | −7,8→−6,8 % | **nein** | hier nicht neu geprüft |

**Damit bleibt genau ein Gewinner statt zwei: `rsi2_crypto`.** Die Aussage des
Berichts, beide Gewinner seien Krypto-Bots mit kurzer Haltedauer, verliert ihre
zweite Stütze. Die Gesamtaussage der Studie verschiebt sich dadurch von „schadet
bei 7 von 9" auf **„schadet bei 8 von 9"**.

Die Walk-Forward-Stabilität wurde für die gefilterte Grundlage in **diesem**
Nachtrag bewusst nicht neu bewertet — sie ist auftragsgemäss Teil der
Vertiefungsstudie (PR #22, Nachtrag N5), wo alle vier Fenster mit Filter
gerechnet sind.

---

## 4. Getroffene Annahmen

**A1 — Der Filter wird nachträglich angewendet.** `filter_trades_by_regime`
streicht die Einstiege im BTC-Abwärtstrend aus dem fertigen Trade-Satz. Das ist
die Konvention des Projekts (auch `experiment_btc_regime_filter.py` arbeitet so)
und die einzige Variante, die gegen den Sync-Check und gegen `live_params.py`
referenzfähig ist. Live blockiert der Filter dagegen schon den Einstieg, sodass
das Symbol frei bleibt und ein späteres Signal annehmen kann. Der Unterschied ist
in PR #22 (Nachtrag N0) gemessen: **8 Trades (3,4 %)**, ohne Auswirkung auf die
Schlussfolgerung.

**A2 — Der Trennzeitpunkt bleibt der der Erstfassung**, berechnet auf dem
ungefilterten Trade-Satz. So bleiben In-Sample und Out-of-Sample dieselben
Kalenderfenster und der Unterschied ist allein dem Filter zuzuordnen.

**A3 — Die Buy-and-Hold-Referenz wird nicht mitgeführt.** Sie hängt in dieser
Studie am Zeitfenster der jeweiligen Trades, nicht am Trade-Satz selbst, und
verschöbe sich durch den Filter nur um wenige Tage. Der vollständige
Buy-and-Hold-Gegencheck auf gefilterter Grundlage steht in PR #22, Nachtrag N4.

**A4 — Die Regime-Parameter sind Bot-Konstanten** (`BTC_ATR_LENGTH = 22`,
`BTC_ATR_MULT = 3,0`) und wurden nicht variiert.

---

## 5. Konsistenz mit PR #22

Die hier berichteten gefilterten Werte sind **zahlengleich** mit denen der
Vertiefungsstudie (`research/vbc_deepdive/BERICHT.md`, Nachtrag N3): 233 Trades,
In-Sample 20,47 % / −16,29 % / 1,26 und 11,65 % / −16,09 % / 0,72, Out-of-Sample
23,00 % / −7,76 % / 2,96 und 18,28 % / −6,82 % / 2,68. Beide Studien rechnen
unabhängig voneinander — die eine über `equity_simulation.collect_all_trades`,
die andere über die vendorierte Einstiegslogik der Vertiefungsstudie — und kommen
auf dieselben Zahlen. Die Übereinstimmung ist damit nicht behauptet, sondern
belegt.

---

## 6. Reproduktion

```
python3 nachtrag_regimefilter.py
```

Der Lauf bricht ab, falls der Regressionscheck gegen
`results/volatility_breakout_crypto.json` nicht durchgeht.

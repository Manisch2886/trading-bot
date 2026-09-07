# P&L 2025 bei fixer Positionsgrösse von 1000 USD — alle neun Bots

Reine Informationsauswertung. **Keine Bewertung, kein Ranking, keine
Handelsempfehlung** — die Zeilenreihenfolge der Tabelle ist in
`konfiguration.py` festgelegt und folgt nicht dem Ergebnis. Kein Bot-Code wurde
verändert (leerer `git diff` auf `strategies/`, in `test_pnl.py` geprüft).

---

## 0. Entscheidungsgrundlage

### Was gerechnet wurde

Für jeden Bot: alle Trades, deren **Einstieg** zwischen dem 01.01.2025 und dem
31.12.2025 liegt, jeder mit einer festen Positionsgrösse von 1000 USD.

```
P&L je Trade = 1000 USD × (exit_price − entry_price) / entry_price
```

So in der Aufgabe vorgegeben — das ist die **Brutto**-Rechnung, ohne Gebühren
und Slippage. Alle neun Bots modellieren Kosten in ihrer eigenen Spalte
`pnl_pct`, und zwar einheitlich mit 0,30 % je Rundlauf (0,1 % Gebühr + 0,05 %
Slippage, je einmal für Ein- und Ausstieg) — bei 1000 USD also **exakt 3,00 USD
pro Trade**, für alle neun nachgerechnet. Weil dieser Abzug bei einem Bot mit
1197 Trades etwas völlig anderes bedeutet als bei einem mit 31, steht die
Netto-Summe als zweite Spalte daneben statt in einer Fussnote.

**1000 USD wird vereinfachend mit 1000 USDT gleichgesetzt** — keine
EUR-Umrechnung, keine Wechselkursdaten. Bei den vier Aktien-Bots sind die Kurse
ohnehin USD.

### Woher die Trades kommen

Kein nachgebauter Backtest: die Trades kommen aus
`equity_simulation.collect_all_trades` des jeweiligen Bots. Diese Untersuchung
entscheidet nur, **mit welchen Parametern** er aufgerufen wird — und genau das
ist der heikle Teil:

* **Parameter aus `live_params.py`**, nicht aus den gleichnamigen Konstanten in
  `equity_simulation.py`. `forward_test.py` liest ausschliesslich aus
  `live_params.py`; wer die anderen nimmt, rechnet einen Bot nach, der so gar
  nicht läuft (Sync-Check, PR #24).
* Was sich nicht als Argument durchreichen lässt, wird als **Modulkonstante
  gesetzt** — und zwar *vor* dem Laden der Daten, weil mehrere Bots ihre
  Indikatoren bereits beim Laden berechnen. Jede Abweichung wird protokolliert.
* **BTC-Regimefilter bei `volatility_breakout_crypto` nachgezogen**:
  `live_params.BTC_REGIME_FILTER_ENABLED` ist `True`, aber dessen
  `collect_all_trades` wendet den Filter nicht an (PR #22-Nachtrag). Bei
  `t3_supertrend` tut `collect_all_trades` das bereits selbst — dort wurde
  nichts nachgezogen, sonst wäre der Filter doppelt drin.
* **Beide Elliott-Wave-Bots auf der kausal korrigierten Grundlage** aus PR #26
  (Einstieg zum Schlusskurs des Bestätigungsbalkens, keine rückwirkend
  verdrängten Wellen).

### Pflicht-Gegenchecks

| Prüfung | Ergebnis |
|---|---|
| Selbsttests `test_pnl.py` | **93/93** |
| Parameter jeder Zeile stimmen mit `live_params.py` überein | ja, einzeln geprüft |
| Modulkonstanten gegen `live_params` abgeglichen | 7 geprüft, **0 abweichend** |
| P&L aus der CSV nachgerechnet | stimmt auf den Cent |
| Gewinnrate aus der CSV nachgerechnet | stimmt |
| nur Einstiege im Jahr 2025 enthalten | ja, je Bot geprüft |
| keine fehlenden Kurse in der Auswertung | ja |
| `git diff` auf `strategies/` | **leer** |

### Belastbarkeit

* Das sind **Backtest-Zahlen**, keine Live-Ergebnisse. Für 2025 existieren keine
  echten Live-Trades in dieser Menge; die Bots liefen im Papierbetrieb erst
  später an.
* Die Brutto-Formel **begünstigt systematisch Bots mit vielen Trades**, weil sie
  deren Kosten weglässt. Der Vergleich Brutto/Netto in der Tabelle macht das
  sichtbar — bei `turtle_soup_crypto` dreht der Abzug das Vorzeichen.
* **Eine feste Positionsgrösse ist keine Portfolio-Simulation.** Sie kennt kein
  Kapital, keinen Zinseszins und kein Positionslimit. Bei acht der zehn Zeilen
  war das Limit 2025 tatsächlich bindend (siehe Abschnitt 3) — die Tabelle
  zählt diese Trades trotzdem mit, so wie es die Aufgabe vorgibt.

### Scope-Grenzen

Keine Parameter-Änderung, keine Aktivierungsempfehlung, kein Urteil über
einzelne Bots. Alles unterhalb `research/pnl_2025_fixed_size/`.

### Reproduktion

```
cd research/pnl_2025_fixed_size
python3 run_all.py                       # alles, rund 10 Minuten
python3 extract.py volatility_breakout   # eine einzelne Zeile
python3 summary.py                       # nur die Tabelle
```

---

## 1. Die Tabelle

Alle Beträge in USD. **Brutto** ist die in der Aufgabe vorgegebene Formel,
**netto** dieselben Trades mit dem Kostenmodell des jeweiligen Bots
(−3,00 USD je Trade).

| Bot / Stand | Trades 2025 | Symbole | Gewinnrate | **P&L brutto** | P&L netto | Reihenfolge relevant |
|---|---:|---:|---:|---:|---:|---|
| `elliott_wave` — alt (Zigzag 4 % / Stop 2 % / Fib 0,236) | 181 | 18 | 30,4 % | **+418,88** | −124,20 | kein Limit |
| `elliott_wave` — neu (Zigzag 10 % / Stop 6 % / Fib 0,618) | 31 | 13 | 29,0 % | **+369,52** | +276,40 | kein Limit |
| **`elliott_wave`: neu minus alt** | **−150** | | | **−49,36** | **+400,60** | |
| `elliott_wave_stocks` | 65 | 47 | 20,0 % | **+7 488,51** | +7 293,60 | ja (15 Trades) |
| `t3_supertrend` | 203 | 18 | 31,0 % | **−125,36** | −734,30 | ja (67 Trades) |
| `rsi2_crypto` | 137 | 18 | 63,5 % | **+1 902,96** | +1 492,30 | ja (19 Trades) |
| `rsi2_mean_reversion` | 481 | 136 | 69,0 % | **+2 605,11** | +1 162,40 | ja (34 Trades) |
| `turtle_soup_crypto` | 422 | 20 | 23,9 % | **+108,04** | −1 159,40 | ja (78 Trades) |
| `turtle_soup_stocks` | 1197 | 147 | 58,1 % | **+11 102,54** | +7 511,20 | kein Limit |
| `volatility_breakout` | 481 | 147 | 52,0 % | **+4 815,80** | +3 372,50 | ja (265 Trades) |
| `volatility_breakout_crypto` | 41 | 18 | 43,9 % | **+2 346,13** | +2 223,30 | ja (7 Trades) |

---

## 2. Der Elliott-Wave-Krypto-Vergleich

Der Punkt, an dem die beiden Spalten auseinandergehen:

| | alt | neu | Differenz |
|---|---:|---:|---:|
| Trades 2025 | 181 | 31 | **−150** |
| Gewinnrate | 30,4 % | 29,0 % | −1,4 pp |
| P&L brutto | +418,88 | +369,52 | **−49,36** |
| Handelskosten (3 USD je Trade) | −543,00 | −93,00 | **+450,00** |
| P&L netto | −124,20 | +276,40 | **+400,60** |

**Brutto war 2025 der alte Parametersatz minimal besser** (+49 USD). Netto
dreht sich das Bild um 400 USD zugunsten des neuen — und der ganze Unterschied
kommt aus der Trade-Zahl: 150 Trades weniger sind 450 USD weniger Kosten.

Zwei Dinge gehören dazu, damit die Zahl nicht überinterpretiert wird:

* **2025 war für die alte Kombination ein gutes Jahr.** Über die vollen fünf
  Jahre liegt sie bei −25,7 % Portfoliorendite (Calmar −0,96), die neue bei
  +67,8 % (Calmar 6,66) — siehe PR #28. Ein einzelnes Kalenderjahr taugt nicht
  als Prüfstein für eine Parameterentscheidung, in keine der beiden Richtungen.
* **31 Trades sind wenig.** Die neue Kombination erzeugt im ganzen Jahr 2025
  weniger Signale als die alte in zwei Monaten. Das ist gewollt (grober Zigzag),
  macht die 2025er-Zahl aber statistisch dünn.

---

## 3. Reihenfolge-Empfindlichkeit 2025

Wie in der Aufgabe verlangt, nur die Feststellung *wo* es relevant war — nicht
quantifiziert. Simuliert wurde chronologisch über alle Trades (eine Ende 2024
eröffnete Position belegt im Januar 2025 noch einen Platz); übersprungene Trades
belegen keinen Platz.

| Bot | Limit | 2025 bindend? | Trades ohne Platz | Zeitpunkte am Limit | davon mit mehreren Signalen **gleichzeitig** |
|---|---:|---|---:|---:|---:|
| `elliott_wave` (beide Stände) | — | kein Limit | — | — | — |
| `turtle_soup_stocks` | — | kein Limit | — | — | — |
| `volatility_breakout` | 15 | **ja** | 265 | 86 | **72** |
| `turtle_soup_crypto` | 8 | **ja** | 78 | 29 | **17** |
| `t3_supertrend` | 5 | **ja** | 67 | 40 | **23** |
| `rsi2_mean_reversion` | 20 | **ja** | 34 | 8 | **8** |
| `rsi2_crypto` | 8 | **ja** | 19 | 9 | **8** |
| `elliott_wave_stocks` | 8 | **ja** | 15 | 6 | **4** |
| `volatility_breakout_crypto` | 8 | **ja** | 7 | 3 | **2** |

Die letzte Spalte ist die entscheidende: nur dort, wo **mehrere Signale denselben
Einstiegszeitpunkt teilen und das Limit bereits ausgeschöpft ist**, entscheidet
die Verarbeitungsreihenfolge, welcher Trade den letzten Platz bekommt. Am
stärksten betrifft das `volatility_breakout` (72 solcher Zeitpunkte), am
schwächsten `volatility_breakout_crypto` (2).

Für die Tabelle in Abschnitt 1 spielt das keine Rolle — dort zählt jeder Trade
mit 1000 USD, unabhängig vom Limit. Relevant wird es erst, sobald jemand diese
Zahlen mit einer Portfolio-Simulation vergleicht: dort führen dieselben Signale
je nach Reihenfolge zu unterschiedlichen Ergebnissen (PR #23).

---

## 4. Welche Konfiguration je Bot gerechnet wurde

Zur Nachvollziehbarkeit, welche Sync-Korrekturen eingeflossen sind.

| Bot | Parameter (aus `live_params.py`) | `live_params` zuletzt geändert | Besonderheit |
|---|---|---|---|
| `elliott_wave` alt | Zigzag 4 %, Stop 2 %, Fib 0,236 | — | fest gesetzt: Stand **vor** der Übernahme |
| `elliott_wave` neu | Zigzag 10 %, Stop 6 %, Fib 0,618 | — | fest gesetzt: übernommener Stand (PR #28) |
| `elliott_wave_stocks` | Zigzag 5 %, Stop 3 %, kein Ziel (`USE_TAKE_PROFIT=False`) | 2026-09-03 | unverändert; kausaler Backtest aus PR #26 |
| `t3_supertrend` | T3 16/30, ADX 20, Stop 4 % | 2026-08-31 | BTC-Regimefilter steckt bereits in `collect_all_trades` |
| `rsi2_crypto` | RSI 10, SMA-Trendfilter 150, **kein Stop** | 2026-09-03 | — |
| `rsi2_mean_reversion` | RSI 5, **kein Stop**, max. Haltedauer 10 | 2026-09-03 | 1 Konstante abgeglichen, keine Abweichung |
| `turtle_soup_crypto` | Donchian 10, Stop „structural", max. Haltedauer 10 | 2026-09-04 | 1 Konstante abgeglichen, keine Abweichung |
| `turtle_soup_stocks` | Donchian 10, **kein Stop**, max. Haltedauer 10, **kein Limit** | 2026-09-04 | 1 Konstante abgeglichen, keine Abweichung |
| `volatility_breakout` | Squeeze-Perzentil 25, Rückblick 126, Stop 8 %, max. Haltedauer 15 | 2026-09-03 | 2 Konstanten abgeglichen, keine Abweichung |
| `volatility_breakout_crypto` | Squeeze-Perzentil 25, Rückblick 126, Stop 5 %, max. Haltedauer 15 | 2026-09-04 | **BTC-Regimefilter nachgezogen** |

**Was der Sync-Abgleich ergeben hat:** von sieben geprüften Modulkonstanten wich
**keine einzige** vom Live-Wert ab. Die eine Sync-Korrektur, die das Ergebnis
tatsächlich verändert hat, ist der **BTC-Regimefilter bei
`volatility_breakout_crypto`**: er blockiert **126 von 359 Trades** über die
gesamte Historie. Deutlich sichtbar wird das im Jahr 2025 — der letzte Einstieg
dieses Bots liegt am **13.08.2025**; danach war das BTC-Regime bis zum
Jahresende bärisch, und der Bot hätte keine Position mehr eröffnet.

---

## 5. Getroffene Annahmen

**N-A1 — 1000 USD = 1000 USDT.** Keine EUR-Umrechnung, keine Wechselkursdaten,
wie in der Aufgabe vorgegeben.

**N-A2 — Die Brutto-Formel ist massgeblich, die Netto-Zahl steht daneben.** Die
Aufgabe gibt `1000 × (exit − entry) / entry` vor. Da alle neun Bots ein
Kostenmodell mitbringen und die Trade-Zahlen um den Faktor 39 auseinanderliegen
(31 bis 1197), wäre eine reine Brutto-Tabelle irreführend. Beide Spalten stehen
gleichwertig nebeneinander; die Brutto-Spalte ist die geforderte.

**N-A3 — Das Positionslimit wird in der Tabelle nicht angewendet.** „Jede
eröffnete Position mit einer fixen Grösse von 1000 USD" heisst: kein Kapital,
keine Konkurrenz um Plätze. Wo das Limit 2025 gebunden hätte, steht es in
Abschnitt 3.

**N-A4 — Die Trade-Auswahl folgt der Sortierung des jeweiligen Bots.** Für die
Brutto-Summe ist die Reihenfolge ohnehin bedeutungslos, weil jeder Trade dieselbe
Grösse bekommt.

**N-A5 — Der BTC-Regimefilter wird nachträglich auf den Trade-Satz angewendet**
(`filter_trades_by_regime`), so wie in den bestehenden Untersuchungen des Projekts
(PR #22-Nachtrag). Das ist gleichwertig zum Blockieren beim Einstieg: ein
blockierter Einstieg findet nicht statt, und da hier kein Positionslimit greift,
gibt ein blockierter Trade auch keinen Platz für einen anderen frei.

**N-A6 — Trades mit fehlendem Kurs würden gestrichen und gezählt.** In dieser
Auswertung trat kein solcher Fall auf (0 Streichungen bei allen zehn Zeilen); die
Absicherung ist trotzdem drin, weil derselbe Datenfehler in `APH` die
Auswertung in PR #28 betroffen hat.

**N-A7 — Der Zeitraum wird über `entry_time` abgegrenzt.** Ein im Dezember 2025
eröffneter Trade zählt vollständig zu 2025, auch wenn er erst 2026 schliesst.
So in der Aufgabe vorgegeben.

---

## 6. Offene Punkte

Beobachtungen, keine Aufträge:

1. **Alle neun Bots rechnen mit demselben Kostenmodell** (0,1 % Gebühr +
   0,05 % Slippage je Order) — auch die vier Aktien-Bots, obwohl das ein
   Binance-Spot-Tarif ist. Ob das für Aktien passt, ist offen.
2. **`volatility_breakout_crypto` hat nach dem 13.08.2025 keinen Einstieg
   mehr.** Der BTC-Regimefilter wirkt also stark; ob das im Sinne des
   Auftraggebers ist, ist eine Frage an ihn, keine Feststellung hier.
3. **Diese Zahlen sind kein Live-Ergebnis.** Wer sie mit den Zahlen im
   Wochenbericht vergleichen will, muss die dortige Kennzeichnung beachten
   (PR #27).

---

## 7. Dateien

| Datei | Rolle |
|---|---|
| `botenv.py` | Bot-Umgebung, Stubs (werfen bei Aufruf) |
| `konfiguration.py` | welche `live_params`-Werte wohin gehen — der Kern der Auswertung |
| `extract.py` | eine Zeile der Tabelle: Trades holen, 2025 filtern, rechnen |
| `summary.py` | die Tabelle, die Konfigurationsübersicht, die Reihenfolge-Frage |
| `test_pnl.py` | Selbsttests (93 Prüfungen) |
| `run_all.py` | alles nacheinander, ein Prozess je Zeile |
| `results/<zeile>_pnl.json` | Kennzahlen und verwendete Konfiguration je Zeile |
| `results/<zeile>_trades_2025.csv` | jeder einzelne Trade, nachrechenbar |
| `results/zusammenfassung.json` | alle zehn Zeilen zusammen |

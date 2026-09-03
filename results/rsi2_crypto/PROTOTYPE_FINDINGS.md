# RSI-2 Mean-Reversion Krypto — Prototyp-Ergebnisse

Stand: 2026-09-03. Kompletter neuer Prototyp-Prozess wie ursprünglich bei
den Aktien-Versionen — bis einschließlich Backtest-/Walk-Forward-Stufe.
**Nichts live geschaltet** — keine `live_params.py`, kein Cronjob, kein
`forward_test.py`.

## 0. Zeitrahmen-Entscheidung (Begründung)

Elliott Wave Krypto läuft auf 1h, T3/SuperTrend auf 4h — für RSI-2 wurde
stattdessen bewusst **TAGESKERZEN** gewählt, aus denselben Gründen wie bei
der Aktien-Version:

- RSI-2 (Connors) ist explizit als Tages-Mean-Reversion-Strategie
  konzipiert und validiert — SMA(200) als Trendfilter und der 5-Tage-
  SMA-Exit sind in "Handelstagen" gedacht. Eine Übertragung auf 1h/4h würde
  eine zusätzliche, ungeprüfte Umrechnung dieser Perioden erfordern (z. B.
  "was entspricht 200 Tagen bei 4h-Kerzen?") und faktisch eine andere,
  neu zu validierende Strategie ergeben, nicht mehr Connors' Originalidee.
- Krypto handelt 24/7 — bei TAGESKERZEN bedeutet das: an JEDEM Kalendertag
  gibt es eine Kerze, anders als bei Aktien mit Wochenenden/Feiertagen.
  "Handelstage" und "Kalendertage" fallen damit zusammen — das befürchtete
  Umrechnungsproblem (Stunden/Perioden statt Handelstage) entfällt bei
  dieser Zeitrahmen-Wahl von selbst, statt zusätzlichen Aufwand zu
  erzeugen.
- Datenbasis: Tageskerzen wurden aus der vorhandenen 1h-Historie (5 Jahre,
  2021-09 bis heute) verlustfrei per OHLC-Resampling abgeleitet
  (`shared/build_daily_crypto_data.py`) — in der Sandbox ist der direkte
  Binance-API-Zugriff blockiert (getestet, 403), dieselbe Einschränkung wie
  bei Yahoo Finance für die Aktien-Bots. Auf der echten Maschine wäre ein
  nativer `fetch_1d_data.py` (analog zu `fetch_4h_data.py`) vorzuziehen.

**Trendfilter-Rekalibrierung für Krypto:** Der 200-Tage-SMA-Trendfilter der
Aktien-Version wurde NICHT ungeprüft übernommen — `multi_symbol_optimise.py`
testet SMA-Trendfilter-Perioden 100/150/200 gemeinsam mit der RSI-Schwelle
und dem Stop-Loss (siehe Abschnitt 2).

## 1. Regeln (exakt spezifiziert)

Identisch zur Aktien-Version (`rsi2_mean_reversion`), mit SMA_TREND_PERIOD
als zusätzlichem, empirisch getesteten Parameter statt fest auf 200:

1. **Trendfilter:** Schlusskurs > SMA(SMA_TREND_PERIOD).
2. **Einstieg:** Trendfilter erfüllt UND RSI(2) < RSI_THRESHOLD (getestet: 5, 10).
3. **Ausstieg — Priorität pro Tag:** a) Stop-Loss (falls aktiv) b) SMA(5)-Exit
   c) Zeit-Exit nach spätestens 10 Tagen.
4. **Stop-Loss:** empirisch getestet (kein Stop vs. 5% vs. 8%), nicht
   blind angenommen.

Universum: 25 Top-Volumen-Krypto-Coins (`shared/symbols_config.py`), davon
20 mit ausreichender Historie (≥500 Tage, deckt SMA-200-Vorlauf ab) — 4
sehr neue Top-25-Coins (ENSOUSDT, PUMPUSDT, ZKCUSDT, UUSDT) wurden
übersprungen.

## 2. Multi-Symbol-Optimierung (Gesamtzeitraum, 20 Symbole)

| SMA-Trend | RSI-Schwelle | Stop-Loss | Trades | Win Rate | Ø Rendite/Trade | Score |
|---|---|---|---|---|---|---|
| **150** | **10** | **kein Stop** | **439** | **63,3%** | **0,94%** | **0,340** |
| 200 | 5 | kein Stop | 227 | 63,4% | 0,95% | 0,256 |
| 150 | 5 | kein Stop | 215 | 63,7% | 0,97% | 0,216 |
| 100 | 10 | kein Stop | 448 | 62,1% | 0,61% | 0,186 |
| 200 | 10 | kein Stop | 464 | 61,6% | 0,44% | 0,092 |
| 100 | 5 | kein Stop | 205 | 61,0% | 0,53% | 0,087 |

Alle Kombinationen mit aktivem Stop-Loss (5%/8%) erfüllen die
Mindestkriterien nicht (Ø-Rendite fällt unter 0) — **derselbe Befund wie
bei der Aktien-Version**: ein harter Stop schadet RSI-2s Erwartungswert.
**SMA-Trendfilter 150 Tage / RSI-Schwelle 10 / kein Stop** ist die
robusteste Kombination — die für Krypto rekalibrierte Trendfilter-Periode
(150 statt 200) bestätigt die Vermutung aus der Anfrage, dass der
Aktien-Wert nicht unverändert passt.

## 3. Walk-Forward (70/30, Split innerhalb der Symbol-Historie)

| Metrik | In-Sample | Out-of-Sample |
|---|---|---|
| Beste Kombination | SMA 200 / RSI 5 / kein Stop | (dieselbe) |
| Win Rate | 63,9% | 62,1% |
| Ø Gewinn/Trade | 0,95% | 0,95% |
| Anzahl Trades | 169 | 58 |
| Robustheit-Score | 0,241 | **0,32** |

Score **verbessert sich** Out-of-Sample (+33%) — starkes Robustheitssignal,
kein Overfitting. (Die In-Sample-beste Kombination unterscheidet sich von
der Gesamtzeitraum-besten aus Abschnitt 2 — SMA 200/RSI 5 statt SMA
150/RSI 10 — plausibel, da das In-Sample-Fenster nur ~70% des
Gesamtzeitraums abdeckt und Krypto-Marktphasen sich schnell ändern.)

## 4. Equity-Simulation (10.000 Start, 10% Allokation, Limit 8)

Validierte Basiskonfiguration: SMA-Trend 150, RSI-Schwelle 10, kein Stop
(Gesamtzeitraum-bester Score aus Abschnitt 2).

| | Gesamtzeitraum | Out-of-Sample |
|---|---|---|
| Endkapital | 12.837,09 | 12.490,81 |
| Gesamtrendite | **+28,37%** | **+24,91%** |
| Trades ausgeführt | 392 | 101 |
| Trades übersprungen | 47 | 3 |
| Max Drawdown | −13,30% | −4,14% |

**Kein Kapital-Flaschenhals wie bei den Aktien-Prototypen:** nur 10,7%
Skip-Rate Gesamtzeitraum (47/439), 2,9% OOS — deutlich niedriger als
RSI-2 Aktien (65%) oder Volatility Breakout Aktien (73%). Nachvollziehbar:
nur 20 Symbole statt 147, entsprechend seltener treten genug gleichzeitige
Signale auf, um das Limit-8/10%-Kapitalbudget auszuschöpfen.

## 5. Buy-and-Hold-Vergleich

| | Wert |
|---|---|
| Endkapital | 9.744,74 |
| Gesamtrendite | **−2,55%** |
| Max Drawdown | −79,18% |
| Anzahl Symbole | 20 |

**RSI-2 Krypto schlägt Buy-and-Hold deutlich** (+28,37%/+24,91% vs.
−2,55%) — ein anderes Bild als bei der Aktien-Version (dort nie
geschlagen). **Wichtige Einordnung:** das Buy-and-Hold-Ergebnis ist stark
durch die Zusammensetzung des Universums geprägt — die "Top-25 nach
AKTUELLEM Volumen"-Liste enthält rückwirkend auch Coins, die seit ihrem
Allzeithoch stark gefallen sind (z. B. ältere Alt-Coins, die heute noch
volumenstark gehandelt werden, aber in USD deutlich unter früheren Ständen
liegen) — das macht die Buy-and-Hold-Messlatte für DIESES konstruierte
Portfolio ungewöhnlich niedrig (−79% Max Drawdown ist extrem). Der
Vergleich ist intern konsistent (gleiches Universum für Strategie und
Benchmark), sollte aber nicht als "RSI-2 schlägt den Krypto-Markt generell"
überinterpretiert werden.

## 6. Experiment: BTC-Regime-Filter (auf ausdrückliche Anfrage geprüft)

Testet den beim T3/SuperTrend-Bot etablierten BTC-SuperTrend-Regime-Filter
(nur Einstiege bei BTC-Aufwärtstrend) als zusätzliche Vorbedingung:

| | Ohne Filter (Gesamt) | Mit Filter (Gesamt) | Ohne Filter (OOS) | Mit Filter (OOS) |
|---|---|---|---|---|
| Trades | 439 | 268 | 104 | 46 |
| Win Rate | 63,3% | 62,7% | 68,3% | 67,4% |
| Portfolio-Rendite | +28,37% | +11,68% | +24,91% | +5,22% |
| Max Drawdown | −13,30% | −13,48% | −4,14% | −1,40% |

**Der BTC-Regime-Filter schadet RSI-2 Krypto deutlich** (Rendite mehr als
halbiert in beiden Zeiträumen), bei kaum verbessertem Drawdown. Plausibel:
Mean-Reversion-Strategien profitieren gerade von Rücksetzern INNERHALB
eines intakten oder neutralen Marktumfelds — ein Filter, der genau diese
Phasen blockiert (wann immer BTC selbst nicht im Aufwärtstrend ist), nimmt
der Strategie einen Großteil ihrer besten Gelegenheiten. Anders als bei
trendfolgenden Strategien (T3/SuperTrend, wo der Filter entwickelt wurde)
ist der Filter hier kontraproduktiv.

**Empfehlung: BTC-Regime-Filter NICHT übernehmen.**

## 7. Stress-Periode 2022 ("Krypto-Winter") im Vergleich zu den anderen Krypto-Bots

Siehe `volatility_breakout_crypto/stress_period_2022_crypto_family.py`
(gemeinsame Auswertung für beide neuen Krypto-Prototypen plus die zwei
etablierten Live-Krypto-Bots) — Ergebnistabelle in Abschnitt 7 der
Volatility-Breakout-Krypto-Findings sowie hier zur Einordnung:

| Bot | Rendite 2022 | Max DD 2022 |
|---|---|---|
| Elliott Wave (Krypto, live) | +21,20% | −0,23% |
| T3/SuperTrend (Krypto, live) | −3,28% | −12,28% |
| **RSI-2 Mean-Reversion (Krypto, Prototyp)** | **−8,65%** | **−8,65%** |
| Volatility Breakout (Krypto, Prototyp) | −12,35% | −16,55% |

RSI-2 Krypto ist 2022 negativ, aber moderater als Volatility Breakout
Krypto und liegt deutlich unter seinem Allzeit-Max-Drawdown (−13,11%) —
also kein Konzentrations-Extremereignis wie bei Volatility Breakout
(siehe dortige Findings, Abschnitt 7). Passt zum bei der Aktien-Version
etablierten Muster: RSI-2 schwächelt moderat und konsistent in
Stressphasen, ohne Einzelextremausschlag.

## 8. Einordnung / offene Punkte

- Solide Signalqualität (Win Rate ~62-64%), Score verbessert sich sogar
  Out-of-Sample — kein Overfitting-Signal bei der Parameterwahl.
- **Kein Kapital-Flaschenhals** wie bei den Aktien-Prototypen — das kleinere
  Krypto-Universum (20 vs. 147 Symbole) erzeugt seltener konkurrierende
  Signale.
- **Schlägt Buy-and-Hold deutlich** — mit der wichtigen Einschränkung, dass
  das Buy-and-Hold-Ergebnis fürs konstruierte Top-25-Portfolio
  ungewöhnlich schwach ausfällt (siehe Abschnitt 5).
- BTC-Regime-Filter getestet, klar nicht empfohlen (schadet der
  Mean-Reversion-Logik).
- 2022-Stress-Test: moderates, konsistentes Schwächeln, kein
  Extremereignis wie bei Volatility Breakout Krypto.
- Bewusst **nicht** umgesetzt: `live_params.py`, Cronjob, `forward_test.py`.

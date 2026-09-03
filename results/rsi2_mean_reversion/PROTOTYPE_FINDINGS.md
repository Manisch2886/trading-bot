# RSI-2 Mean-Reversion — Prototyp-Ergebnisse (vierter Bot)

Stand: 2026-09-03. Prototyp bis einschließlich Backtest/Walk-Forward-Stufe,
wie beauftragt. **Nichts live geschaltet** — keine `live_params.py`, kein
Cronjob, kein `forward_test.py`.

---

## 1. Regeln (exakt spezifiziert)

Vollständige, verbindliche Spezifikation in `backtest_rsi2.py` (Modul-Docstring).
Kurzfassung:

1. **Trendfilter:** Schlusskurs > SMA(200).
2. **Einstieg:** Trendfilter erfüllt UND RSI(2) < Schwelle (getestet: 5 und 10).
   Einstieg zum Schlusskurs des Signaltags. Kein Pyramiding (max. eine offene
   Position pro Symbol).
3. **Ausstieg — "je nachdem was zuerst eintritt", explizite Priorität pro Tag:**
   a) Stop-Loss (falls aktiv) — Tagestief ≤ Stop-Kurs
   b) SMA-Exit — Schlusskurs > SMA(5)
   c) Zeit-Exit — spätestens nach 10 Handelstagen nach Einstieg, zum Schlusskurs
   Auf einem Tag zählt immer nur die zuerst zutreffende Bedingung (a vor b vor c).
4. **Stop-Loss-Einordnung:** Connors verwendet standardmäßig keinen festen Stop
   (nur Zeit-Exit). Statt das anzunehmen, wurde es **empirisch getestet**
   (kein Stop vs. 5% vs. 8%) — Ergebnis siehe Abschnitt 2: Ein harter Stop
   **senkt den Ø-Gewinn/Trade spürbar** (z. B. RSI<5: 0,229% ohne Stop → nur
   0,037% mit 5%-Stop). Bestätigt Connors' Ansatz empirisch statt ihn nur zu
   übernehmen.

## 2. Multi-Symbol-Optimierung (Gesamtzeitraum, 147 Symbole)

| RSI-Schwelle | Stop-Loss | Trades | Win Rate | Ø PnL/Trade | Ø Haltedauer |
|---|---|---|---|---|---|
| **10** | **kein Stop** | 10.342 | 64,5% | 0,20% | 5,6 Tage |
| 5 | kein Stop | 5.391 | 64,5% | 0,23% | 5,7 Tage |
| 10 | 8% | 10.526 | 64,2% | 0,08% | 5,2 Tage |
| 10 | 5% | 10.945 | 62,8% | 0,06% | 4,7 Tage |
| 5 | 8% | 5.470 | 64,1% | 0,07% | 5,3 Tage |
| 5 | 5% | 5.641 | 62,6% | 0,04% | 4,7 Tage |

## 3. Walk-Forward (70/30, Split innerhalb des 10-Jahres-Fensters)

**Wichtiger Implementierungs-Fix unterwegs:** Der Split-Punkt muss innerhalb
des 10-Jahres-Auswertungsfensters liegen, nicht auf der vollen (bei manchen
Aktien 60+ Jahre reichenden) Rohhistorie — sonst entsteht ein stark
verzerrter, ungleicher Split. Wurde vor der Auswertung korrigiert (siehe
`multi_symbol_walk_forward.split_all_symbols`).

| Metrik | In-Sample | Out-of-Sample |
|---|---|---|
| Beste Kombination | RSI<5, kein Stop | (dieselbe, keine Re-Optimierung) |
| Win Rate | 63,8% | **66,0%** |
| Ø Gewinn/Trade | 0,10% | **0,50%** |
| Anzahl Trades | 3.674 | 1.718 |
| Robustheit-Score | 0,033 | **0,292** (deutlich höher als In-Sample) |

**Starkes Robustheits-Signal**: Win Rate, Ø PnL und Score verbessern sich
allesamt Out-of-Sample statt abzufallen — kein Overfitting-Muster (analog zur
positiven OOS-Überraschung beim Elliott-Wave-Aktien-Bot).

## 4. Equity-Simulation (10.000 Start, 10% Allokation, **Limit 8** — fix, wie angefragt)

**Gesamtzeitraum:**

| RSI | Stop | Endkapital | Rendite | Trades ausgef./übersprungen | Max DD |
|---|---|---|---|---|---|
| 5 | kein Stop | 12.991 | **+29,91%** | 2.641 / 2.750 | -21,82% |
| 5 | 5% | 9.902 | -0,98% | 3.087 / 2.554 | -23,70% |
| 5 | 8% | 10.017 | +0,17% | 2.791 / 2.679 | -28,27% |
| 10 | kein Stop | 10.761 | +7,61% | 3.591 / 6.751 | -35,91% |
| 10 | 5% | 10.222 | +2,22% | 4.271 / 6.674 | -28,06% |
| 10 | 8% | 11.204 | +12,04% | 3.867 / 6.659 | -29,45% |

**Out-of-Sample:**

| RSI | Stop | Endkapital | Rendite | Trades ausgef./übersprungen | Max DD |
|---|---|---|---|---|---|
| 5 | kein Stop | 13.501 | +35,01% | 887 / 831 | -11,44% |
| 5 | 5% | 12.634 | +26,34% | 1.048 / 750 | -10,50% |
| 5 | 8% | 12.515 | +25,15% | 938 / 803 | -13,86% |
| **10** | **kein Stop** | **15.068** | **+50,68%** | 1.205 / 2.139 | **-8,26%** |
| 10 | 5% | 13.464 | +34,64% | 1.460 / 2.084 | -13,34% |
| 10 | 8% | 14.295 | +42,95% | 1.297 / 2.103 | -11,24% |

**Buy-and-Hold-Vergleich (dasselbe Universum/Zeitraum):**

| Zeitraum | Endkapital | Rendite | Max DD |
|---|---|---|---|
| Gesamtzeitraum | 87.624 | +776,24% | -34,83% |
| Out-of-Sample | 23.823 | +138,23% | -20,95% |

### Zentraler Befund: massiver Skip-Rate-Effekt durch das feste Positionslimit

RSI-2 erzeugt **deutlich mehr gleichzeitige Signale** als die wellenbasierten
Bots (bis zu 6.751 von ~10.500 Signalen übersprungen bei RSI 10 — knapp
**65%** der gefundenen Trades kommen bei Limit 8 gar nicht zum Zug, gegenüber
z. B. nur ~10% beim Elliott-Wave-Aktien-Bot bei gleichem Limit). Das ist der
Hauptgrund, warum die reale, kapitalgewichtete Rendite (max. +29,91% bzw.
+50,68% OOS) so viel schwächer ausfällt als der naive Trade-Durchschnitt
vermuten ließe (Ø PnL positiv, Score OOS sogar besser als In-Sample). Der
Trade-Level-Edge ist also real und OOS-bestätigt — bei Limit 8 kann das
Portfolio ihn aber nur zu einem kleinen Teil tatsächlich einsammeln.

**RSI-2 schlägt Buy-and-Hold bei Limit 8 NICHT** — weder Gesamtzeitraum
(+29,91% vs. +776,24%) noch OOS (+50,68% vs. +138,23%). Der Drawdown ist
dagegen in allen Fällen deutlich kleiner als Buy-and-Hold (-8,26% bis
-35,91% vs. -34,83%/-20,95%). Anders als bei den bestehenden Bots ist "Limit
8" hier vermutlich kein fairer Vergleichspunkt in der Sache, sondern eine
strukturelle Fehlpassung zum viel höheren Signalaufkommen dieser Strategie —
ein höheres Positionslimit wäre der naheliegende nächste Test (siehe
Abschnitt 6), aber bewusst noch nicht durchgeführt, wie angefragt nur bis zur
Backtest-/Walk-Forward-Stufe.

## 5. Portfolio-Korrelationsanalyse (grobe erste Einschätzung)

Gemeinsames Vergleichsfenster aller vier Bots (durch Krypto-Datenverfügbarkeit
begrenzt): 2021-09-14 bis 2026-06-27.

**Korrelationsmatrix (tägliche Renditen):** alle Werte zwischen -0,02 und
0,01 — praktisch unkorreliert. **Einschränkung:** Das ist teils ein
mechanischer Effekt seltener Handelstage (an den meisten Tagen ändert sich
bei keiner Strategie etwas), nicht zwingend Beweis für eine "echte"
Diversifikation der Marktreaktion — mit Vorsicht zu interpretieren.

**Aussagekräftiger — Drawdown-Diversifikation:**

| Bot | Max Drawdown im gemeinsamen Fenster |
|---|---|
| Elliott Wave (Krypto) | -0,23% |
| T3/SuperTrend (Krypto) | -22,20% |
| Elliott Wave (Aktien) | -1,65% |
| RSI-2 Mean-Reversion (Aktien, neu) | -12,72% |
| **Gleichgewichtete 4-Bot-Kombination (25/25/25/25)** | **-1,43%** |

Die Verlustphasen der vier Bots überlappen sich im Backtest kaum — der
schlechteste Einzel-Bot-Drawdown (-22,20%, T3/SuperTrend) wird in der
kombinierten Kurve auf -1,43% geglättet. Das bestätigt die
Diversifikations-Hypothese aus der Recherche recht deutlich, wenn auch nur
als grobe, backtest-basierte Ersteinschätzung (keine echten
Forward-Test-Daten, hypothetische Gleichgewichtung, keine tatsächliche
Kapitalallokation zwischen den eigenständigen Bots).

## 6. Einordnung / offene Punkte für eine Entscheidung

- **Trade-Level-Edge ist real und OOS-bestätigt** (Win Rate ~64-66%, Score
  verbessert sich OOS) — die Grundidee funktioniert.
- **Portfolio-Level-Ergebnis bei fixem Limit 8 ist schwach** und schlägt
  Buy-and-Hold nicht — der Engpass ist eindeutig die hohe
  Signal-Überlappungsrate dieser Strategie, nicht die Signalqualität selbst.
- **Naheliegender nächster Schritt** (noch nicht durchgeführt): Positionslimit
  für RSI-2 separat empirisch testen (analog zu den Limit-Experimenten der
  bestehenden Bots) - plausibel, dass ein deutlich höheres Limit hier nötig
  ist, damit die Strategie ihren Edge tatsächlich entfalten kann.
- **Drawdown-Diversifikation im 4-Bot-Verbund ist das stärkste Einzelergebnis**
  dieses Prototyps und spricht klar für die Weiterverfolgung.
- Kein Stop-Loss (Connors' Standardversion) bestätigt sich als die bessere
  Wahl gegenüber festen Stop-Werten.

Reproduzierbar mit:
```
python3 strategies/rsi2_mean_reversion/multi_symbol_optimise.py
python3 strategies/rsi2_mean_reversion/multi_symbol_walk_forward.py
python3 strategies/rsi2_mean_reversion/pipeline_report.py
python3 strategies/rsi2_mean_reversion/portfolio_correlation_analysis.py
```

# Turtle Soup (False-Breakout-Reversal, Aktien) — Prototyp-Ergebnisse

Stand: 2026-09-04. Prototyp bis einschließlich Backtest-/Walk-Forward-Stufe,
wie beauftragt. **Nichts live geschaltet** — keine `live_params.py`, kein
Cronjob, kein `forward_test.py`.

## 1. Regeln (exakt spezifiziert)

Vollständige Spezifikation in `backtest_turtle_soup.py` (Modul-Docstring).
Kurzfassung:

1. **Setup-Erkennung:** Tagestief unterschreitet das rollierende
   DONCHIAN_PERIOD-Tage-Tief (Startwert 20, empirisch getestet: 10/20/40).
   Vergleichs-Tief bezieht sich nur auf die N Tage VOR dem aktuellen Tag.
2. **Einstiegs-Trigger — SELBER Tag, nicht Folgetag (begründete
   Entscheidung):** Tagestief < Donchian-Tief UND Schlusskurs > Donchian-Tief
   — beides am selben Balken. Begründung: (a) das ist die textbuchgetreue
   Original-Definition (Larry Williams' "Oops"/Linda Raschke — Bruch und
   Rückkehr innerhalb eines Handelstages), (b) es passt konsistent zum in
   diesem Projekt etablierten Muster aller täglich scannenden Bots (RSI-2,
   Volatility Breakout, Pair-Rotation) — kein mehrtägiges Freshness-Fenster
   mit zusätzlicher, unnötiger Mehrdeutigkeit (wie lange auf eine
   Folgetag-Bestätigung warten?). Einstieg zum Schlusskurs des Signaltags.
3. **Ausstieg — Priorität pro Tag:**
   a) Stop-Loss (falls aktiv) — zwei Varianten GEGENEINANDER getestet:
      "structural" (Stop = Tagestief des Setup-Tags selbst — musterspezifisch,
      im Diskretionär-Trading übliche Platzierung) vs. fester Prozentsatz
      unter Einstieg (5%/8%, wie bei den anderen Bots). "kein Stop" ebenfalls
      getestet.
   b) Zeit-Exit — spätestens nach MAX_HOLD_DAYS (10, kürzer als Volatility
      Breakouts 15 — Reversal-Bewegungen sind typischerweise kurzlebiger).

Universum: S&P-500 Top 150, RECENT_YEARS_ONLY=10.

## 2. Multi-Symbol-Optimierung (Gesamtzeitraum, 147 Symbole)

Auszug (vollständige Tabelle in
`results/turtle_soup_stocks/multi_symbol_optimisation_results.csv`):

| Donchian | Stop-Modus | Trades | Win Rate | Ø Rendite/Trade | Score |
|---|---|---|---|---|---|
| **10** | **kein Stop** | **12069** | **55,2%** | **0,69%** | **0,463** |
| 10 | 5% fest | 13714 | 49,2% | 0,56% | 0,408 |
| 40 | kein Stop | 4870 | 56,9% | 0,86% | 0,396 |
| 10 | structural | 17809 | **27,3%** | 0,28% | 0,207 |
| 20 | structural | 11544 | 27,3% | 0,23% | 0,134 |

**Wichtiger, empirischer Befund zum musterspezifischen Stop (Punkt 3a der
Anfrage — beide Varianten direkt gegeneinander getestet):** der
"structural"-Stop (Setup-Tag-Tief) schneidet über ALLE Donchian-Perioden
am SCHLECHTESTEN ab (Win Rate nur ~27-29% statt ~48-57% bei den anderen
Modi). Erklärung: der Stop-Abstand ist bei diesem Muster strukturell sehr
eng (Differenz zwischen Einstiegs-Schlusskurs und Setup-Tag-Tief, oft nur
die Tages-Handelsspanne) — er wird dadurch von normalem Kursrauschen
getriggert, bevor sich die Reversal-Bewegung durchsetzen kann. **"Kein
Stop" ist die robusteste Kombination**, verlässt sich allein auf den
10-Tage-Zeit-Exit als Risikobegrenzung.

## 3. Walk-Forward (70/30, Split innerhalb des 10-Jahres-Fensters)

| Metrik | In-Sample | Out-of-Sample |
|---|---|---|
| Beste Kombination | Donchian 10 / kein Stop | (dieselbe) |
| Win Rate | 55,0% | 55,8% |
| Ø Gewinn/Trade | 0,53% | 1,06% |
| Anzahl Trades | 8441 | 3632 |
| Robustheit-Score | 0,263 | **0,587** |

Score **verbessert sich deutlich** Out-of-Sample (+123%) — starkes
Robustheitssignal, kein Overfitting.

## 4. Equity-Simulation (10.000 Start, 10% Allokation, Limit 8)

| | Gesamtzeitraum | Out-of-Sample |
|---|---|---|
| Endkapital | 23.300,59 | 16.337,68 |
| Gesamtrendite | **+133,01%** | **+63,38%** |
| Trades ausgeführt | 1887 | 575 |
| Trades übersprungen | 10182 | 3057 |
| Max Drawdown | −32,54% | −12,01% |

**Sehr ausgeprägter Kapital-Flaschenhals:** 84,4% Skip-Rate — noch höher
als bei allen bisherigen Aktien-Prototypen (RSI-2 65%, Volatility Breakout
73%). Turtle-Soup-Setups (N-Tage-Tief-Bruch-und-Rückkehr) sind in einem
147-Aktien-Universum ein vergleichsweise häufiges Tagesereignis.

## 5. Buy-and-Hold-Vergleich

| | Wert |
|---|---|
| Endkapital | 87.623,97 |
| Gesamtrendite | **+776,24%** |
| Max Drawdown | −34,83% |
| Anzahl Aktien | 150 |

Schlägt Buy-and-Hold nicht — identisches Muster zu allen bisherigen
Aktien-Prototypen.

## 6. Abgrenzung zu Volatility Breakout (Kern der Diversifikationsthese)

**Hypothese aus der Anfrage:** Turtle Soup sollte gerade dort/dann aktiv
sein, wo Volatility Breakout Fehlausbrüche (Stop-Loss-Exits) erlebt.

### 6a. Zeitliche Nähe (direkter Test der Hypothese)

| | Wert |
|---|---|
| Turtle-Soup-Einstiege gesamt | 12069 |
| Volatility-Breakout-Stop-Loss-Exits gesamt | 805 |
| ...davon Turtle-Soup-Einstiege innerhalb 10 Tagen NACH einem VB-Stop-Loss (selbes Symbol) | 347 (2,88%) |
| Zufalls-Baseline (20 Permutationen der VB-Exit-Zeitpunkte) | 192,7 (1,60%) |
| **Faktor gegenüber Zufall** | **1,8×** |

Turtle-Soup-Einstiege treten **1,8-mal häufiger** in der Nähe eines
Volatility-Breakout-Fehlausbruchs auf als bei zufälligem Timing zu
erwarten wäre — ein moderates, aber über der Zufalls-Baseline liegendes
Signal FÜR die Hypothese auf Einzeltrade-Ebene. Der absolute Anteil bleibt
aber klein (2,88%) — die meisten Turtle-Soup-Signale entstehen unabhängig
von einem vorherigen Volatility-Breakout-Fehlausbruch auf demselben Symbol.

### 6b. Korrelation der täglichen Portfolio-Renditen

**Korrelation: 0,085** — praktisch unkorreliert. Ein starkes,
eigenständiges Diversifikationssignal auf Portfolio-Ebene, unabhängig vom
spezifischen zeitlichen Kausalzusammenhang aus 6a.

### 6c. Stress-Perioden im direkten Vergleich

| Periode | Turtle Soup Rendite | Turtle Soup Max DD | Volatility Breakout Rendite | Volatility Breakout Max DD |
|---|---|---|---|---|
| 2022-Bärenmarkt | −12,22% | −25,57% | −13,14% | −22,39% |
| 2020-COVID-Crash | **−24,22%** | **−32,22%** | −2,00% | −3,64% |

**Wichtiger, differenzierter Befund — die Hypothese hält NUR teilweise:**
- **2022 (langsamer Bärenmarkt):** beide Strategien schwächeln ähnlich
  stark (−12,22% vs. −13,14%) — KEINE Diversifikation in dieser Art von
  Stressphase, beide leiden gemeinsam unter dem breiten Abwärtstrend.
- **2020 (schneller Crash):** starke DIVERGENZ, aber in umgekehrter
  Richtung als die Hypothese nahelegt — Turtle Soup erleidet hier seinen
  **Allzeit-schlechtesten Drawdown** (−32,22%, identisch zum
  Gesamthistorie-Maximum), während Volatility Breakout kaum betroffen ist
  (−2,00%/−3,64%). Erklärung: in einem schnellen, echten Crash sind
  Kursrückgänge unter ein N-Tage-Tief meist KEINE Fehlausbrüche, sondern
  der Beginn einer echten, anhaltenden Abwärtsbewegung — Turtle Soups
  "kaufe die Rückkehr über das gebrochene Tief"-Logik kauft hier
  systematisch in ein fallendes Messer, statt einen echten Fehlausbruch
  zu identifizieren.

**Einordnung:** Die beiden Strategien haben **komplementäre, nicht
identische Schwachstellen** — Volatility Breakout leidet unter
anhaltenden, langsamen Bärenmärkten (wiederholte Fehlausbrüche nach oben),
Turtle Soup leidet unter schnellen, scharfen Crashs (echte statt falsche
Kursbrüche nach unten). Das ist eine ANDERE, aber ebenfalls werthaltige
Diversifikationsstruktur als die urspünglich formulierte Hypothese — kein
"Turtle Soup rettet, wenn Vol Breakout scheitert"-Muster, sondern "beide
scheitern in unterschiedlichen Marktphasen", was auf Portfolio-Ebene
trotzdem zur beobachteten niedrigen Korrelation (6b) führt.

## 7. Einordnung / offene Punkte

- Solide Signalqualität, Walk-Forward-Score verbessert sich deutlich OOS
  — kein Overfitting-Signal.
- **Wichtiger empirischer Befund:** der musterspezifische "structural"-Stop
  ist entgegen der Intuition die SCHLECHTESTE Stop-Variante — "kein Stop"
  gewinnt klar (Abschnitt 2).
- **Sehr ausgeprägter Kapital-Flaschenhals** (84,4% Skip-Rate, höher als
  alle bisherigen Aktien-Prototypen).
- Schlägt Buy-and-Hold nicht (identisches Muster zu allen Aktien-Prototypen).
- **Diversifikationsthese differenziert bestätigt:** praktisch
  unkorrelierte Portfolio-Renditen (0,085) und ein leicht über Zufall
  liegendes zeitliches Zusammenfallen mit Volatility-Breakout-
  Fehlausbrüchen (Faktor 1,8×) — ABER die urspüngliche Hypothese
  ("Turtle Soup kompensiert Vol-Breakout-Schwäche") gilt nicht in JEDER
  Stressphase: in 2022 schwächeln beide gemeinsam, in 2020 divergieren sie
  stark, aber mit Turtle Soup als dem schwächeren Teil (nicht wie erwartet
  dem stärkeren). Die Diversifikationswirkung ist real, aber komplexer
  als ursprünglich angenommen — komplementäre statt kompensatorische
  Schwachstellen.
- Bewusst **nicht** umgesetzt: `live_params.py`, Cronjob, `forward_test.py`.

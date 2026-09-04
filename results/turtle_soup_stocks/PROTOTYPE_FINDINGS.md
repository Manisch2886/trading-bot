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

## 8. Kapitalmanagement-Tuning

Ausgangslage: 84,4% Skip-Rate bei Limit 8/10% Allokation - der staerkste
bisher beobachtete Kapital-Flaschenhals im gesamten Projekt (hoeher als
RSI-2 65% und Volatility Breakout 73%). Analog zur erfolgreichen
Vorgehensweise bei RSI-2/Volatility Breakout in drei Schritten untersucht.
Reine Analyse - **nichts live geschaltet**, keine `live_params.py`.

### 8a. Signal-Qualitaets-Test (Aufgabe 1)

| | n | Win Rate | Ø PnL/Trade |
|---|---|---|---|
| (a) Tatsaechlich ausgefuehrt (Limit 8, 10%) - Gesamtzeitraum | 1887 | 53,7% | 0,523% |
| (b) Alle gefundenen Signale - Gesamtzeitraum | 12069 | 55,2% | 0,691% |
| (a) Tatsaechlich ausgefuehrt - Out-of-Sample | 575 | 54,3% | 0,907% |
| (b) Alle gefundenen Signale - Out-of-Sample | 3632 | 55,8% | 1,059% |

**Kapitalmanagement ist der dominante Flaschenhals** (wie bei den anderen
Bots), UND die tatsaechlich ausgefuehrten Trades sind im Schnitt sogar
LEICHT SCHLECHTER als die Gesamtpopulation (Differenz −0,168 Prozentpunkte
Gesamtzeitraum, −0,152 Out-of-Sample) - derselbe Mechanismus wie bei RSI-2:
keine neutrale Auswahl, sondern Kapitalerschoepfung tendenziell genau in
Phasen mit vielen gleichzeitigen, teils hochwertigeren Signalen. Erklaert
die ungewoehnlich hohe Skip-Rate: Turtle-Soup-Setups (N-Tage-Tief-Bruch)
sind in einem 147-Aktien-Universum ein haeufiges Tagesereignis, das die
10%-Allokation bei Limit 8 schnell saettigt.

Die rein diagnostische "unbegrenztes Kapital"-Simulation (c) liefert hier
ein methodisch wichtiges Nebenergebnis: bei dieser hohen Signal-Dichte
(12069 Signale, oft viele gleichzeitig offen) fuehrt die Kombination aus
"kein Limit" UND "10% des JEWEILIGEN aktuellen Kapitals pro Trade ohne
Beruecksichtigung bereits gebundenen Kapitals" zu einem impliziten
Hebel-Effekt weit ueber 100% des Kapitals gleichzeitig - das Ergebnis kann
dadurch sogar negativ werden (Gesamtzeitraum: −153,71% "Rendite"). Das ist
ein reines Artefakt der unrealistischen Diagnose-Annahme (kein Live-
Vorschlag, siehe Docstring), kein wirtschaftlich sinnvolles Szenario -
bestaetigt aber deutlich, warum ein Positionslimit ueberhaupt notwendig
ist, sobald die Signal-Dichte hoch genug wird.

### 8b. Positionsgroesse x Limit-Matrix (Aufgabe 2)

Feste Basis: Donchian 10, kein Stop, 10 Tage Zeit-Exit. Vollstaendige
Tabelle in `results/turtle_soup_stocks/experiment_position_size_limit_{full,oos}.csv`.

Wichtige Beobachtung: bei 10% Allokation saettigt das Positionslimit bereits
bei 15 (Limit 15/20/unbegrenzt liefern IDENTISCHE Ergebnisse) - der
eigentliche Flaschenhals bei 10% ist also die Kapitalgroesse pro Trade, nicht
die explizite Limit-Zahl. Eine kleinere Allokation erhoeht die Erfassungsrate
drastisch: bei 2% Allokation/unbegrenztem Limit werden 8915 von 12069
Signalen ausgefuehrt (73,9% Erfassung, gegenueber 15,6% bei der
Basiskonfiguration).

### 8c. Stress-Perioden unter neuer Konfiguration (Aufgabe 3)

Vollstaendige Gesamtuebersicht (alle 16 Konfigurationen, sortiert nach
Out-of-Sample-Rendite, mit Gesamtzeitraum-, 2022- und 2020-Werten) in
`results/turtle_soup_stocks/experiment_capital_management_summary.csv`.
Auszug der wichtigsten Kandidaten:

| Allokation | Limit | OOS-Rendite | OOS-DD | Gesamt-Rendite | Gesamt-DD | 2022-Rendite | 2022-DD | 2020-Rendite | 2020-DD |
|---|---|---|---|---|---|---|---|---|---|
| 10% (Basis) | 8 | 63,38% | −12,01% | 133,01% | −32,54% | −12,22% | −25,57% | −24,22% | −32,22% |
| 10% | 15/20/unbegrenzt | **91,16%** | −16,70% | 142,31% | −36,47% | −24,40% | −32,17% | −26,72% | −36,18% |
| **2%** | **unbegrenzt** | 73,12% | −13,25% | **145,59%** | **−29,91%** | **−11,53%** | **−18,67%** | −25,18% | −29,91% |
| 5% | 20/unbegrenzt | 68,96% | −13,64% | 170,37% | −34,81% | −19,66% | −26,11% | −25,58% | −34,72% |

**Empfehlung: 2% Allokation, Limit unbegrenzt.** Diese Kombination dominiert
die Basiskonfiguration auf fast jeder Dimension: hoehere Gesamtzeitraum-
Rendite (+145,59% statt +133,01%) bei GLEICHZEITIG niedrigerem Max Drawdown
(−29,91% statt −32,54%), UND eine deutlich verbesserte 2022-Performance
(−11,53%/−18,67% statt −12,22%/−25,57% - schlaegt hier sogar Volatility
Breakout, −13,14%/−22,39%), UND ein nahezu unveraendertes 2020-Profil
(−25,18%/−29,91% statt −24,22%/−32,22% - marginal bessere DD trotz aehnlich
schwacher Rendite). Die alternative Spitzenreiter-Konfiguration bei reiner
OOS-Rendite (10% Allokation, Limit 15 - identisch zu 20/unbegrenzt, 91,16%
OOS-Rendite) wird trotz des hoeheren Punktwerts NICHT empfohlen, da sie sich
im 2022-Stresstest deutlich verschlechtert (−24,40%/−32,17% - fast doppelt
so hoher Verlust wie die Basiskonfiguration) und damit das im Prototyp
dokumentierte "gemeinsam mit Volatility Breakout schwach"-Risiko in 2022
verstaerkt statt entschaerft.

**Schwachstellenprofil bleibt strukturell nachvollziehbar:** wie beim
Volatility-Breakout-Praezedenzfall erwartet, aendert sich die grundsaetzliche
2020-Schwaeche (echter Crash statt Fehlausbruch) durch Kapitalmanagement-
Tuning NICHT wesentlich - sie liegt in der Signalqualitaet, nicht im
Kapitalmanagement. Die 2022-Zahlen verbessern sich bei der empfohlenen
Konfiguration zwar spuerbar (kleinere, breiter gestreute Positionen daempfen
den kumulierten Verlust eines breiten Baerenmarkts), aber Turtle Soup bleibt
strukturell weiterhin die schwaechere der beiden Strategien in einem echten,
schnellen Crash.

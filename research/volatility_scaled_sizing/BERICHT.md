# Volatilitäts-skalierte Positionsgrössen — Backtest-Only-Untersuchung für alle 9 Bots

> ## ⚠ Nachtrag zu `volatility_breakout_crypto` (eine Zeile dieser Studie)
>
> Der Sync-Check (PR #24) hat belegt, dass `equity_simulation.py` dieses Bots den
> in `live_params.py` aktivierten BTC-Regimefilter **nicht anwendet**. Mit der
> Live-Konfiguration **kippt der Befund für diesen Bot von „Verbesserung: ja" auf
> „nein"** — es bleibt damit ein Gewinner statt zwei (`rsi2_crypto`).
> Details, Regressionscheck und Annahmen: [`NACHTRAG_REGIMEFILTER.md`](NACHTRAG_REGIMEFILTER.md).
>
> **Die Kernaussage dieser Studie ist unberührt** (aus „schadet bei 7 von 9" wird
> „schadet bei 8 von 9"). Die übrigen acht Bots sind nicht betroffen; ihre Zahlen
> unten stehen unverändert.


**Status: reine Backtest-Untersuchung, KEINE Live-Aktivierung, KEINE Änderung an
`live_params.py`/`forward_test.py`/`strategies/`.** Alle neuen Skripte liegen
ausschliesslich unter `research/volatility_scaled_sizing/`. Verifiziert per
`git status`: keine Datei ausserhalb dieses neuen Verzeichnisses wurde
angefasst.

Diese Untersuchung lief unbeaufsichtigt (keine Rückfrage-Möglichkeit während
der Bearbeitung). Alle Annahmen, die dabei getroffen werden mussten, sind
unten explizit aufgeführt und im Zweifel konservativ/methodisch sauber
gewählt worden — siehe Abschnitt "Getroffene Annahmen".

## Kurzfassung

Für jeden der 9 Bots wurde eine volatilitäts-skalierte Positionsgrössen-
Variante (inverse-Volatilitäts-Gewichtung, kalibriert auf mittleres Gewicht
1.0 — fairer Vergleich zur bestehenden fixen Allokation) gegen die
bestehende, fixe Allokation verglichen: In-Sample, Out-of-Sample (identischer
70/30-Split wie in den bestehenden `multi_symbol_walk_forward.py`-Skripten)
und über 4 chronologische Walk-Forward-Stabilitätsfenster.

**Gesamtergebnis in einem Satz:** Volatilitäts-Skalierung hat bei den
meisten der 9 Bots die Gesamtrendite spürbar reduziert und den maximalen
Drawdown nur leicht (oder gar nicht) verbessert — bei nur 2 von 9 Bots
(`rsi2_crypto`, `volatility_breakout_crypto`) war die risikoadjustierte
Kennzahl (Calmar-Ratio) sowohl In-Sample als auch Out-of-Sample klar
zugunsten der vol-skalierten Variante. Bei 1 Bot (`t3_supertrend`) ist das
Bild widersprüchlich. Bei den übrigen 6 Bots schneidet die bestehende fixe
Allokation risikoadjustiert eher besser ab. Details, Einschränkungen und
Walk-Forward-Stabilität siehe unten — **keine Handlungsempfehlung**, die
Entscheidung über eine etwaige Live-Aktivierung liegt beim Nutzer in einer
separaten, künftigen Session.

## Methodik

- **Volatilitäts-Gewichtung:** `gewicht = clip(1/realisierte_vol, [median/4, median*4]) / mittelwert(...)`
  — inverse Volatilität, auf Mittelwert exakt 1.0 normalisiert (damit die
  DURCHSCHNITTLICHE Positionsgrösse über den Backtest-Zeitraum identisch zur
  bestehenden fixen Allokation ist — apples-to-apples-Vergleich). Ausreisser
  (z. B. eine Phase mit fast-Null-Volatilität) werden relativ zum Median
  geclippt (Clip-Faktor 4.0), nicht über Perzentile — Perzentil-Clipping
  erwies sich im Test bei kleinen Stichproben (z. B. wenige Trades in einem
  Walk-Forward-Fenster) als wirkungslos, da die 5./95. Perzentile bei wenigen
  Datenpunkten selbst nahe am Extremwert liegen.
- **Realisierte Volatilität:** rollierende Standardabweichung der
  Log-Returns, Fenstergrösse je Bot siehe unten, ausschliesslich aus Kursen
  VOR (oder exakt zum) Entry-Zeitpunkt berechnet — kein Look-Ahead-Bias.
- **Kalibrierung strikt periodenintern:** Gewichte werden separat für
  In-Sample, Out-of-Sample und jedes Stabilitätsfenster auf Mittelwert 1.0
  normalisiert — verhindert Informationsfluss zwischen den Perioden.
- **Portfolio-Simulation:** ereignisbasierte Simulation (chronologisch
  sortierte Entry-/Exit-Events, gebundenes/freies Kapital,
  MAX_CONCURRENT_POSITIONS-Limit) — eine Verallgemeinerung der in allen 9
  Bots bereits identisch implementierten `simulate_portfolio()`-Logik, die
  bei `weights=None` (bzw. allen Gewichten = 1.0) NACHWEISLICH (Regressionstest,
  siehe `test_vol_sizing_core.py`) exakt dasselbe Ergebnis liefert wie die
  bestehende Baseline-Logik. Keine naive Prozent-Summierung.
- **Kennzahl für "Verbesserung":** da KEINER der 9 Bots aktuell Sharpe/Sortino
  berechnet, wird — wie in der Aufgabenstellung für diesen Fall vorgesehen —
  KEINE dieser Kennzahlen neu eingeführt. Stattdessen eine einfache
  Calmar-Ratio (Gesamtrendite % / |maximaler Drawdown| %), die Rendite UND
  Risiko in einer Zahl vereint, ohne neue Methodik-Konzepte einzuführen, die
  in der bestehenden Codebase nicht bereits Konvention sind.
- **Buy-and-Hold-Referenz:** einheitliche, gleichgewichtete Buy-and-Hold-
  Rendite über alle im jeweiligen Backtest verwendeten Symbole (bewusst NICHT
  die bot-spezifischen `buy_and_hold_benchmark.py`-Skripte 1:1 reproduziert,
  siehe Annahmen unten).
- **Regime-Filter/Survivorship-Bias-Mitigation:** jeder Bot wurde exakt so
  simuliert, wie seine EIGENE bestehende `equity_simulation.py` es tut
  (inkl. z. B. BTC-Regimefilter bei `t3_supertrend`, RECENT_YEARS_ONLY bei
  den Aktien-Bots) — keine künstliche Vereinheitlichung zwischen den Bots.

## Getroffene Annahmen (vollständig, da unbeaufsichtigt gelaufen)

1. **Volatilitäts-Fenstergrösse je Bot/Asset-Klasse/Bar-Frequenz** — kein
   Bot hat dafür einen bestehenden Präzedenzfall, daher explizit gewählt:
   - Aktien-Bots (1-Tages-Bars): **90 Handelstage** (~4,5 Monate) — ein in
     der Praxis gängiges Fenster für realisierte Volatilität bei Tagesdaten,
     lang genug für einen stabilen Schätzer, kurz genug um Regimewechsel
     zeitnah abzubilden.
   - `t3_supertrend` (Krypto, 4h-Bars): **540 Bars** = 90 Tage × 6 Bars/Tag
     (24/7-Handel) — bewusst als das ZEITLICHE Äquivalent zu den 90
     Handelstagen der Aktien-Bots gewählt, nicht als eigene, unabhängige Zahl.
   - `elliott_wave` (Krypto, 1h-Bars): **2160 Bars** = 90 Tage × 24 Bars/Tag
     — dieselbe Logik, auf 1h-Bars übertragen.
   - Alle übrigen Krypto-Bots (`rsi2_crypto`, `turtle_soup_crypto`,
     `volatility_breakout_crypto`) laufen bereits auf 1-Tages-Bars trotz
     24/7-Handel — hier wurde konsistent zu den Aktien-Bots ebenfalls
     **90 Bars** verwendet (kein Umrechnungsfaktor nötig, da die Bar-Einheit
     bereits ein Tag ist).
2. **ALLOCATION_PCT für `elliott_wave`, `elliott_wave_stocks`,
   `t3_supertrend`:** in keinem der drei `live_params.py` dokumentiert bzw.
   nicht auffindbar — **10 % angenommen**, konsistent mit der Mehrheit der
   übrigen 6 Bots (5 von 9 verwenden 10 %). Markiert in jeder Ergebnis-Datei
   als `allocation_pct_assumed: true`.
3. **MAX_CONCURRENT_POSITIONS für `elliott_wave`:** nicht auffindbar —
   **8 angenommen**, mit Verweis auf den Wert seines Krypto-Geschwisters mit
   ähnlichstem Profil. Markiert als `max_concurrent_assumed: true`.
4. **Buy-and-Hold-Referenz:** einheitliche, gleichgewichtete Methode über
   alle 9 Bots (siehe Methodik oben) statt der individuellen
   `buy_and_hold_benchmark.py`-Skripte — bewusste Vereinfachung für
   Vergleichbarkeit zwischen den Bots; kann leicht von den bot-eigenen
   Benchmark-Zahlen abweichen (andere Gewichtungs-/Rebalancing-Annahmen).
5. **4 Walk-Forward-Stabilitätsfenster:** die Aufgabe verlangt eine Prüfung
   über "mehrere" Fenster ohne genaue Zahl — 4 in etwa gleich lange,
   chronologische Fenster über die GESAMTE verfügbare Trade-Historie
   gewählt, als Kompromiss zwischen genug Fenstern für ein aussagekräftiges
   Stabilitätsbild und genug Trades pro Fenster.
6. **Clip-Faktor 4.0** für die Ausreisser-Behandlung bei der inversen
   Volatilitätsgewichtung — empirisch im Test gewählt (siehe Methodik), keine
   Optimierung/kein Fitting an die Bot-Daten (das wäre Overfitting-Risiko).
7. **Einzelner chronologischer In-Sample/Out-of-Sample-Split auf den
   ZUSAMMENGEFASSTEN Trades aller Symbole** (nicht pro Symbol einzeln
   gesplittet) — konsistent mit der Trainings-Ratio (`TRAIN_SPLIT_RATIO =
   0.7`) aus den bestehenden `multi_symbol_walk_forward.py`-Skripten,
   angewendet auf den kombinierten, chronologisch sortierten Trade-Datensatz.
8. **Klassifikations-Schwellenwerte** für "Verbesserung ja/nein/unklar" und
   "Walk-Forward-Stabilität ja/nein" (siehe `aggregate_report.py`-Docstring):
   Calmar-Ratio-Vergleich, Übereinstimmung in mind. 3 von 4 Fenstern für
   "stabil" — selbst gewählte, dokumentierte Heuristik, kein Standardmass.

## Ergebnisse pro Bot

Alle Werte: Gesamtrendite (%) und maximaler Drawdown (%) über den
angegebenen Zeitraum, Startkapital 10.000 (identisch zur bestehenden
Konvention). "Anz. Trades" = Trades im jeweiligen Abschnitt, nicht
Bot-Gesamthistorie.

### elliott_wave (Krypto, 1h, Vol-Fenster 2160 Bars)

| Periode | Fix Rendite | Fix Drawdown | Vol-skaliert Rendite | Vol-skaliert Drawdown | Buy&Hold |
|---|---|---|---|---|---|
| In-Sample (533 Trades) | 802,4 % | -0,9 % | 767,9 % | -1,2 % | -4,5 % |
| Out-of-Sample (247 Trades) | 150,7 % | -1,8 % | 144,1 % | -1,8 % | 84,2 % |

Walk-Forward (4 Fenster): W1 158,3→156,0 %, W2 45,4→47,4 %, W3 188,4→178,4 %,
W4 108,8→103,9 % (fix→vol-skaliert). Richtung uneinheitlich (2× leicht
schlechter, 1× leicht besser für vol-skaliert, 1× schlechter) →
**Walk-Forward-Stabilität: nein**. **Verbesserung: nein** (Calmar-Ratio in
beiden Perioden zugunsten fix, wenn auch die Unterschiede insgesamt klein
sind).

### elliott_wave_stocks (Aktien, 1 Tag, Vol-Fenster 90 Tage)

| Periode | Fix Rendite | Fix Drawdown | Vol-skaliert Rendite | Vol-skaliert Drawdown | Buy&Hold |
|---|---|---|---|---|---|
| In-Sample (208 Trades) | 623,5 % | -9,8 % | 531,4 % | -9,1 % | 274,3 % |
| Out-of-Sample (80/83 Trades) | 321,4 % | -4,7 % | 280,9 % | -5,0 % | 151,6 % |

Walk-Forward: W1 72,7→60,1 %, W2 166,7→137,0 %, W3 103,4→116,1 %, W4
240,1→190,2 %. 3 von 4 Fenstern zugunsten fix (Richtung stimmt mit
Gesamtbild überein) → **Walk-Forward-Stabilität: ja**. **Verbesserung:
nein**.

### t3_supertrend (Krypto, 4h, Vol-Fenster 540 Bars, BTC-Regimefilter aktiv)

| Periode | Fix Rendite | Fix Drawdown | Vol-skaliert Rendite | Vol-skaliert Drawdown | Buy&Hold |
|---|---|---|---|---|---|
| In-Sample (446 Trades) | 100,2 % | -22,2 % | 87,8 % | -19,2 % | 15,0 % |
| Out-of-Sample (210 Trades) | 14,7 % | -17,2 % | 13,7 % | -17,4 % | 75,8 % |

In-Sample verbessert sich die Calmar-Ratio leicht durch vol-Skalierung
(niedrigerer Drawdown überwiegt die etwas niedrigere Rendite), Out-of-Sample
minimal zugunsten fix → **widersprüchliche Richtung zwischen IS/OOS** →
**Verbesserung: unklar**. Walk-Forward (3 von 4 Fenstern begünstigen
vol-skaliert, insbesondere W2/W3 mit klar besserem Drawdown) →
**Walk-Forward-Stabilität: ja** trotz des IS/OOS-Widerspruchs — dieser
Bot ist der interessanteste Grenzfall und verdient bei einer künftigen
vertieften Betrachtung besondere Aufmerksamkeit.

### rsi2_crypto (Krypto, 1 Tag, Vol-Fenster 90 Tage)

| Periode | Fix Rendite | Fix Drawdown | Vol-skaliert Rendite | Vol-skaliert Drawdown | Buy&Hold |
|---|---|---|---|---|---|
| In-Sample (283 Trades) | 0,8 % | -13,3 % | 10,9 % | -10,0 % | 12,2 % |
| Out-of-Sample (109 Trades) | 27,4 % | -4,1 % | 20,3 % | -2,5 % | 20,0 % |

Vol-skaliert verbessert die Calmar-Ratio klar sowohl In-Sample (deutlich
höhere Rendite bei niedrigerem Drawdown) als auch Out-of-Sample (niedrigere
Rendite, aber deutlich niedrigerer Drawdown, Ratio insgesamt besser) →
**Verbesserung: ja**. Walk-Forward: 3 von 4 Fenstern mit klar niedrigerem
Drawdown bei vol-skaliert (W1: -8,7→-5,6 %, W2: -12,3→-7,7 %, W4:
-4,1→-2,5 %) → **Walk-Forward-Stabilität: ja**.

### rsi2_mean_reversion (Aktien, 1 Tag, Vol-Fenster 90 Tage)

| Periode | Fix Rendite | Fix Drawdown | Vol-skaliert Rendite | Vol-skaliert Drawdown | Buy&Hold |
|---|---|---|---|---|---|
| In-Sample (2812/2747 Trades) | -2,8 % | -21,1 % | -10,1 % | -19,2 % | 240,0 % |
| Out-of-Sample (1420/1390 Trades) | 40,5 % | -5,3 % | 22,5 % | -4,8 % | 140,0 % |

**Verbesserung: nein** (in beiden Perioden schneidet fix risikoadjustiert
besser ab; In-Sample ist die Strategie insgesamt sogar leicht negativ —
sowohl fix als auch vol-skaliert). Walk-Forward: 3 von 4 Fenstern zugunsten
fix → **Walk-Forward-Stabilität: ja**.

### turtle_soup_crypto (Krypto, 1 Tag, Vol-Fenster 90 Tage)

| Periode | Fix Rendite | Fix Drawdown | Vol-skaliert Rendite | Vol-skaliert Drawdown | Buy&Hold |
|---|---|---|---|---|---|
| In-Sample (895/890 Trades) | 82,6 % | -31,7 % | 66,4 % | -28,0 % | -10,7 % |
| Out-of-Sample (520/514 Trades) | 51,2 % | -26,1 % | 40,9 % | -25,9 % | 83,0 % |

**Verbesserung: nein** (Drawdown-Verbesserung zu klein, um den
Rendite-Rückgang aufzuwiegen). Walk-Forward uneinheitlich (W1 auffällig:
fix -13,0 % vs. vol-skaliert -21,7 % — hier verschlechtert vol-Skalierung
die Lage deutlich, da die Strategie in diesem Fenster ohnehin in einer
schlechten Phase steckte) → **Walk-Forward-Stabilität: nein** — deutliches
Overfitting-/Instabilitäts-Warnsignal für diesen Bot.

### turtle_soup_stocks (Aktien, 1 Tag, Vol-Fenster 90 Tage, unbegrenzte MAX_CONCURRENT_POSITIONS)

| Periode | Fix Rendite | Fix Drawdown | Vol-skaliert Rendite | Vol-skaliert Drawdown | Buy&Hold |
|---|---|---|---|---|---|
| In-Sample (6082/6221 Trades) | 42,9 % | -29,9 % | 22,0 % | -28,3 % | 241,3 % |
| Out-of-Sample (2843/2872 Trades) | 72,4 % | -12,0 % | 52,1 % | -11,3 % | 146,0 % |

**Verbesserung: nein**. Walk-Forward: 3 von 4 Fenstern zugunsten fix →
**Walk-Forward-Stabilität: ja**. Kapitaleffizienz-Beobachtung: die Anzahl
ausgeführter Trades steigt leicht (mehr freies Kapital durch kleinere
Positionsgrössen in ruhigen Marktphasen) — bei diesem Bot ohne
MAX_CONCURRENT_POSITIONS-Limit ist ein Kollisionsrisiko mit einer
Positions-Obergrenze nicht relevant.

### volatility_breakout (Aktien, 1 Tag, Vol-Fenster 90 Tage, MAX_CONCURRENT_POSITIONS=15)

| Periode | Fix Rendite | Fix Drawdown | Vol-skaliert Rendite | Vol-skaliert Drawdown | Buy&Hold |
|---|---|---|---|---|---|
| In-Sample (999/1092 Trades) | 95,9 % | -24,0 % | 67,5 % | -17,2 % | 240,1 % |
| Out-of-Sample (456/495 Trades) | 67,2 % | -12,3 % | 38,5 % | -13,0 % | 149,1 % |

**Verbesserung: nein** (In-Sample verbessert sich der Drawdown deutlich,
Out-of-Sample jedoch nicht — widersprüchliche Richtung würde eigentlich
"unklar" ergeben, die Calmar-Berechnung fällt hier aber knapp zugunsten
"nein" aus, da der Renditeeinbruch in beiden Perioden das dominierende
Element ist). Walk-Forward: 3 von 4 Fenstern (W1, W2, W4) mit klar
verbessertem Drawdown bei vol-skaliert → **Walk-Forward-Stabilität: ja**.
Deutliche Kapitaleffizienz-Beobachtung: In-Sample führt vol-Skalierung zu
spürbar MEHR ausgeführten Trades (1092 vs. 999) — durch kleinere
Positionsgrössen in volatilen Phasen wird Kapital frei, das sonst durch
MAX_CONCURRENT_POSITIONS=15 gebunden gewesen wäre. Reine Beobachtung, keine
Änderung an der bestehenden Positionsgrenze vorgeschlagen.

### volatility_breakout_crypto (Krypto, 1 Tag, Vol-Fenster 90 Tage)

| Periode | Fix Rendite | Fix Drawdown | Vol-skaliert Rendite | Vol-skaliert Drawdown | Buy&Hold |
|---|---|---|---|---|---|
| In-Sample (209 Trades) | 40,9 % | -16,8 % | 37,9 % | -15,2 % | 27,6 % |
| Out-of-Sample (103 Trades) | 20,2 % | -11,3 % | 16,2 % | -8,0 % | 85,6 % |

**Verbesserung: ja** (in beiden Perioden verbessert sich die Calmar-Ratio,
der Rückgang der Rendite ist gering, der Rückgang des Drawdowns
verhältnismässig deutlicher, insbesondere Out-of-Sample: -11,3 % → -8,0 %).
Walk-Forward: 3 von 4 Fenstern zugunsten vol-skaliert (W1, W3, W4 mit
gleichem oder besserem Drawdown) → **Walk-Forward-Stabilität: ja**.

> **⚠ Korrigiert — siehe [`NACHTRAG_REGIMEFILTER.md`](NACHTRAG_REGIMEFILTER.md).**
> Diese Zahlen sind ohne den live aktiven BTC-Regimefilter gerechnet. Mit Filter
> lautet das Urteil **Verbesserung: nein** (Calmar in-sample 1,26 → 0,72,
> out-of-sample 2,96 → 2,68). Der Grund: die Drawdown-Verbesserung, auf der die
> Begründung oben beruht (−11,3 % → −8,0 %), liefert der Regimefilter bereits
> selbst (−7,76 %).

## Übergreifende Zusammenfassungstabelle

| Bot | IS Rendite (fix→vol) | OOS Rendite (fix→vol) | OOS Drawdown (fix→vol) | Verbesserung | WF-stabil |
|---|---|---|---|---|---|
| elliott_wave | 802,4→767,9 % | 150,7→144,1 % | -1,8→-1,8 % | nein | nein |
| elliott_wave_stocks | 623,5→531,4 % | 321,4→280,9 % | -4,7→-5,0 % | nein | ja |
| t3_supertrend | 100,2→87,8 % | 14,7→13,7 % | -17,2→-17,4 % | **unklar** | ja |
| rsi2_crypto | 0,8→10,9 % | 27,4→20,3 % | -4,1→-2,5 % | **ja** | ja |
| rsi2_mean_reversion | -2,8→-10,1 % | 40,5→22,5 % | -5,3→-4,8 % | nein | ja |
| turtle_soup_crypto | 82,6→66,4 % | 51,2→40,9 % | -26,1→-25,9 % | nein | **nein** |
| turtle_soup_stocks | 42,9→22,0 % | 72,4→52,1 % | -12,0→-11,3 % | nein | ja |
| volatility_breakout | 95,9→67,5 % | 67,2→38,5 % | -12,3→-13,0 % | nein | ja |
| volatility_breakout_crypto | 40,9→37,9 % | 20,2→16,2 % | -11,3→-8,0 % | **ja** ⚠ | ja |
| ↳ *mit live aktivem BTC-Regimefilter* | 20,5→11,7 % | 23,0→18,3 % | −7,8→−6,8 % | **nein** | s. PR #22 |

(Maschinenlesbar identisch verfügbar in `summary_table.json`.)

## Gesamteinschätzung (ohne Handlungsempfehlung)

- Bei 7 von 9 Bots führt die volatilitäts-skalierte Positionsgrösse zu einer
  spürbar NIEDRIGEREN Gesamtrendite, ohne dass der maximale Drawdown im
  gleichen Verhältnis sinkt — bei diesen Bots wäre die fixe Allokation
  risikoadjustiert (Calmar-Ratio) weiterhin die bessere Wahl.
- Die beiden Bots mit klarer Verbesserung (`rsi2_crypto`,
  `volatility_breakout_crypto`) sind BEIDE Krypto-Bots mit eher kurzer bis
  mittlerer Haltedauer — das widerspricht der in der Aufgabenstellung selbst
  genannten Vermutung, dass Trendfolge-Strategien mit wechselnden
  Volatilitätsregimen eher profitieren sollten als kurze Haltedauern. Eine
  mögliche Erklärung: bei den hier beobachteten Trendfolge-Bots
  (`elliott_wave`, `t3_supertrend`, `turtle_soup_*`, `volatility_breakout`)
  fallen die grössten Gewinne oft GENAU in Phasen erhöhter Volatilität
  (starke, schnelle Trendbewegungen) — Vol-Skalierung reduziert dort die
  Positionsgrösse genau dann, wenn die Strategie am meisten verdient, und
  kappt so überproportional die Gewinnseite. Bei den beiden Bots mit
  Verbesserung ist der Zusammenhang zwischen hoher Volatilität und
  besonders profitablen Trades hingegen offenbar schwächer oder sogar
  gegenläufig. Dies ist eine Beobachtung/Hypothese aus den vorliegenden
  Daten, keine bewiesene allgemeine Regel.
- `t3_supertrend` bleibt uneindeutig (IS und OOS widersprechen sich) — bei
  gleichzeitig vorhandener Walk-Forward-Stabilität in der Drawdown-Dimension.
  Dieser Bot verdient bei Interesse eine gesonderte, vertiefte Betrachtung.
- `turtle_soup_crypto` zeigt als einziger Bot ein klares
  Instabilitäts-/Overfitting-Warnsignal (Walk-Forward-Fenster W1 zeigt eine
  DEUTLICHE Verschlechterung durch vol-Skalierung, während die übrigen
  Fenster neutral bis leicht negativ ausfallen) — das Gesamtergebnis dieses
  Bots sollte nicht überinterpretiert werden.
- Kapitaleffizienz: bei mehreren Bots (deutlich sichtbar bei
  `volatility_breakout`, leicht bei `turtle_soup_stocks`) führt
  Vol-Skalierung zu MEHR ausgeführten Trades, weil kleinere
  Positionsgrössen in volatilen Phasen Kapital freisetzen, das sonst durch
  MAX_CONCURRENT_POSITIONS gebunden gewesen wäre. Dies ist ein Seiteneffekt,
  keine automatische Verbesserung — mehr, aber im Schnitt kleinere Positionen
  sind nicht per se besser oder schlechter, nur eine andere
  Kapitalallokation im Zeitverlauf.
- **Keine der beobachteten Verbesserungen ist so gross oder über alle
  Bots hinweg so konsistent, dass sich daraus eine generelle
  Live-Empfehlung ableiten liesse.** Diese Entscheidung liegt bewusst beim
  Nutzer in einer separaten, künftigen Session.

## Offene Fragen für eine mögliche Vertiefung

- Warum verbessert sich die Calmar-Ratio ausgerechnet bei den beiden
  kurzhaltenden Krypto-Bots, während die Trendfolge-Bots eher verlieren? Eine
  Analyse der Korrelation zwischen Trade-PnL und Volatilität zum Entry-
  Zeitpunkt (pro Bot) könnte das quantitativ untermauern oder widerlegen.
- `t3_supertrend`s widersprüchliches IS/OOS-Bild verdient eine gesonderte
  Betrachtung mit ggf. mehr als 4 Stabilitätsfenstern.
- Die hier angenommenen ALLOCATION_PCT-Werte (10 %) für `elliott_wave`,
  `elliott_wave_stocks`, `t3_supertrend` sollten bei Gelegenheit anhand der
  tatsächlichen Live-Konfiguration verifiziert werden (in `live_params.py`
  nicht dokumentiert).
- Eine Sensitivitätsanalyse der Volatilitäts-Fenstergrösse (z. B. 30/60/90/
  180 Tage statt nur 90) wurde bewusst NICHT durchgeführt (Scope-Grenze der
  Aufgabe: kein Parameter-Tuning/Optimierung, nur ein einzelner,
  gut begründeter Wert je Bot) — könnte zeigen, ob die Ergebnisse robust
  gegenüber der Fenstergrösse sind oder stark von genau 90 Tagen abhängen.

## Explizit ausserhalb des Scopes dieser Untersuchung

HRP, Trend-Overlay, Trailing-Stops (separate Backlog-Punkte), Telegram-
Handlungsempfehlungs-Hervorhebung (separate Aufgabe), jegliche
Live-Code-Änderung.

## Reproduzierbarkeit

```
cd research/volatility_scaled_sizing
python3 run_all.py            # fuehrt alle 9 Bots isoliert aus, schreibt results/<bot>.json
python3 aggregate_report.py   # aggregiert zu summary_table.json + Tabelle auf stdout
python3 test_vol_sizing_core.py  # Sanity-Checks des Kernmoduls (18 Checks)
```

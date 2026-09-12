# Trading-Bot-Projekt — Vollständige Übergabedokumentation

**Zweck dieses Dokuments:** Technisches Übergabe-/Gedächtnisdokument für die Fortsetzung der Arbeit in einem neuen Claude-Projekt-Chat. Enthält alle Entscheidungen, Architektur, Code-Struktur, Erkenntnisse und offenen Punkte. Wo Informationen unklar oder nicht abschließend bestätigt sind, ist das explizit gekennzeichnet.

**Stand: 2026-09-11.** Das Dokument beschreibt den Stand von `main` (nach dem Merge von PR #73). Die vorige Fassung stammte vom 2026-09-09 (PR #63) und hinkte den Merges #64–#73 hinterher; nachgezogen wurden das manuelle Schliessen, die Warteauftraege, die beiden Broker-Bruecken, der caffeinate-Dienst und die dreistufige Notbremse. Offene, noch nicht gemergte Pull Requests sind — wo überhaupt erwähnt — ausdrücklich als „in Entwicklung, nicht aktiv" gekennzeichnet und dürfen nicht als laufende Funktion gelesen werden.

---

## 1. Projektziel

Aufbau mehrerer unabhängiger, automatisierter Trading-Bots (aktuell Krypto und Aktien), die:
- auf regelbasierten, backtesteten Strategien laufen (kein Machine-Learning-Modell, sondern klassische technische Analyse: Elliott Wave, T3/ADX/SuperTrend, RSI-2-Mean-Reversion, Turtle Soup, Bollinger-Band-Squeeze)
- rigoros validiert werden (Backtest → Walk-Forward-Analyse → Equity-Simulation → Buy-and-Hold-Vergleich → Signal-Qualitäts-Test), bevor Parameter als "live" gelten
- aktuell im **Paper-Trading-Modus** (Forward Testing, kein echtes Geld) laufen, vollautomatisiert per Cronjob auf dem Mac des Nutzers
- durch **vier** Claude-API-Agenten ergänzt werden (tägliche Einordnung, intelligente Parameter-Suche, Marktkontext via Web-Suche, wöchentliche Portfolio-Einordnung) sowie den Quartals-Interpreter, die informativ unterstützen, aber **nie automatisch** Handelsparameter oder Trades verändern
- über eine gemeinsame **Beobachtungsebene** überwacht werden: ein Telegram-Bot (rein lesend) und ein Web-Dashboard (liest **und schreibt** — manuelles Schliessen und Warteaufträge, siehe Abschnitt 4.3)

**Es sind inzwischen NEUN Bots, nicht drei.** Das Dokument beschrieb bis 2026-09-09 nur die drei ursprünglichen; die sechs später hinzugekommenen Prototypen sind seit Anfang September ebenfalls live im Paper-Trading (siehe Abschnitt 2 und 3.4).

Ursprünglicher Auslöser: Ein Diagramm einer "AI Trading Agent"-Pipeline (Research → Build → Optimise → Forward Test → Risk → Live Trade) mit mehreren Claude-Agenten als Pipeline-Stufen. Die tatsächliche Umsetzung hat sich davon entfernt: Es läuft **kein** Claude-Agent zur Laufzeit der eigentlichen Handelslogik — die Backtest-/Optimierungs-/Signalerkennung ist reiner, deterministischer Python-Code. Claude-Agenten wurden **später gezielt ergänzt** (siehe Abschnitt 6), sind aber vom Kern-Trading-Loop entkoppelt.

**Live-Trading mit echtem Kapital ist explizit noch NICHT umgesetzt** — nur konzeptionell besprochen (siehe Abschnitt 10). Seit PR #68/#70 gibt es allerdings **zwei Broker-Brücken** unter `broker/`, die Orders an das Binance-**Testnet** bzw. ein IBKR-**Paper**-Konto senden (Abschnitt 4.4): virtuelles Geld, aber echte Gegenstellen und der erste Schreibzugriff des Projekts nach aussen.

---

## 2. Die neun Bots im Überblick

| Bot | Ordner | Markt | Zeitrahmen | Datenquelle | Cron-Takt |
|---|---|---|---|---|---|
| Elliott Wave (Krypto) | `strategies/elliott_wave/` | 25 Top-Volumen-Kryptos (Binance USDT-Paare) | 1 Stunde | Binance API | stündlich |
| T3/ADX/SuperTrend (Krypto) | `strategies/t3_supertrend/` | dieselben 25 Kryptos | 4 Stunden | Binance API | alle 4h |
| RSI-2 (Krypto) | `strategies/rsi2_crypto/` | 20 Kryptos | 1 Tag | Binance API (Tageskerzen aus 1h abgeleitet) | täglich |
| Turtle Soup (Krypto) | `strategies/turtle_soup_crypto/` | Kryptos | 1 Tag | Binance API | täglich |
| Volatility Breakout (Krypto) | `strategies/volatility_breakout_crypto/` | Kryptos | 1 Tag | Binance API | täglich |
| Elliott Wave (Aktien) | `strategies/elliott_wave_stocks/` | Top 150 S&P-500-Werte nach Marktkap. | 1 Tag | yfinance | werktags **22:15 Uhr** |
| RSI-2 Mean Reversion (Aktien) | `strategies/rsi2_mean_reversion/` | S&P-500-Auswahl | 1 Tag | yfinance | werktags |
| Turtle Soup (Aktien) | `strategies/turtle_soup_stocks/` | S&P-500-Auswahl | 1 Tag | yfinance | werktags |
| Volatility Breakout (Aktien) | `strategies/volatility_breakout/` | S&P-500-Auswahl | 1 Tag | yfinance | werktags |

Die Zuordnung Bot → Anlageklasse und der erwartete Lauf-Takt stehen **maschinenlesbar** in `notifications/monitor.py` (`ASSET_CLASS`, `DISPLAY_NAMES`, `EXPECTED_INTERVAL_HOURS`); nur `elliott_wave` (1 h) und `t3_supertrend` (4 h) weichen vom Tages-Takt ab. Wer einen zehnten Bot ergänzt, muss ihn dort eintragen, sonst taucht er weder in Telegram noch im Dashboard auf.

Alle neun sind **komplett unabhängig**: eigene Datenbank, eigene Parameter, eigener Cronjob. Sie teilen sich nur gemeinsame Infrastruktur (siehe Abschnitt 4). Es gibt bewusst **kein gemeinsames Kapitalkonto** — die Portfolio-Sicht in `shared/portfolio_overview.py` ist eine reine Beobachtungsrechnung mit hypothetischer Gewichtung, kein zentrales Konto (siehe Abschnitt 8).

---

## 3. Bot-Details

### 3.1 Elliott Wave (Krypto)

**Strategie-Logik:**
1. **Zigzag-Indikator** (`zigzag_indicator.py`) filtert signifikante Kurswendepunkte (Pivots) heraus, Schwellenwert `deviation_pct` einstellbar
2. **Wellenzählung** (`elliott_wave_counter.py`): sucht in den Pivots nach gültigen 5-Wellen-Impulsmustern unter Einhaltung der drei Elliott-Grundregeln:
   - Welle 2 darf nicht unter den Start von Welle 1 zurückfallen
   - Welle 3 darf nie die kürzeste von Welle 1/3/5 sein
   - Welle 4 darf nicht in das Preisgebiet von Welle 1 eindringen
   - Zusätzlich: Fibonacci-Score (0–1) bewertet, wie gut die Wellenverhältnisse zu typischen Fibonacci-Erwartungen passen (Welle 2 Retracement 50–61.8%, Welle 3 Extension ~1.618×, Welle 4 Retracement 23.6–38.2%)
3. **Überlappungsbereinigung** (`remove_overlapping`): bei sich überschneidenden Wellenmustern wird nur das mit dem besten Fib-Score behalten
4. **Handelslogik**: **Long-only**. Bärischer Impuls beendet → erwartete Korrektur nach oben → Long-Einstieg. Bullische Impulse werden übersprungen (würden zu Short führen, bewusst nicht gehandelt).
5. **Backtest** (`backtest_elliott.py`): Einstieg zum **Schlusskurs des Bestätigungsbalkens**, Ausstieg über Stop-Loss, Take-Profit (Fibonacci-Ziel der Gesamtbewegung) oder maximale Haltedauer (`MAX_HOLD_HOURS` = 240 **Balken**, nicht Stunden — Balken-Anzahl über `.head(max_hold_hours)` in `simulate_trade`)

**⚠️ Der wichtigste behobene Fehler des Projekts: Look-Ahead im Backtest (PR #26).**

Hier stand bis 2026-09-09: „Einstieg zum Preis am Wellenende". Genau das war der Fehler. Ein Zigzag-Pivot **ist** erst dann ein Pivot, wenn der Kurs sich danach um `deviation_pct` in die Gegenrichtung bewegt hat — der Backtest stieg aber zum Zeitpunkt **und Preis** des Pivots ein, also zu einem Kurs, der zu diesem Zeitpunkt noch gar nicht als Signal bekannt sein konnte. Nebenwirkung: der Stop-Loss war bis zur Bestätigung mathematisch unerreichbar, ein enger Stop kostete im Backtest also nichts.

Zwei Kanäle, beide behoben (`research/elliott_wave_lookahead/`):
- **Einstiegspreis**: jetzt Schlusskurs des Bestätigungsbalkens statt Pivot-Preis
- **Wellenauswahl**: jetzt kausal über `elliott_wave_counter.find_causal_waves` — vorher konnten spätere Wellen frühere rückwirkend verdrängen

Nachgewiesen: **1301 Trades einzeln geprüft, 0 Kausalitätsverletzungen.** `forward_test.py` und `live_params.py` blieben bei der Korrektur unverändert — der Live-Betrieb war von diesem Fehler nie betroffen, nur die Backtest-Kennzahlen und die daraus abgeleitete Parameterwahl.

**Wirkung auf die Kennzahlen (alle vorher genannten Zahlen beider Elliott-Bots sind damit Geschichte):**

| Bot | vorher (mit Look-Ahead) | nachher (kausal sauber) |
|---|---|---|
| `elliott_wave` | +2184,96 % | **−24,44 %** |
| `elliott_wave_stocks` | +3084,09 % (Calmar 315,02) | **+338,26 %** (Calmar 15,24) |

Aus einer der vermeintlich profitabelsten Strategien wurde beim Krypto-Bot eine verlustbringende. Das ist der Grund für die Parameter-Neubestimmung vom 2026-09-07 (siehe unten).

**Separat davon, weiterhin gültig:** `forward_test.py` nutzte ursprünglich den **historischen** Preis vom Wellenende als Einstiegspreis, obwohl das Signal erst später (bis zu 48h Freshness-Fenster) erkannt wurde — behoben, indem der **aktuelle** Marktpreis zum Erkennungszeitpunkt verwendet wird. Dafür wurde das Datenbankschema um `signal_time` (Wellenende, für Duplikat-Erkennung) getrennt von `entry_time` (tatsächlicher Ausführungszeitpunkt) erweitert. Das war eine Einstiegspreis-Korrektur, **keine** Bestätigungs-Verzögerung — und damit nicht dasselbe wie der Backtest-Look-Ahead oben.

**Zusätzlicher Konsistenz-Fix:** Cronjob wurde von täglich auf **stündlich** umgestellt, da der Backtest auf Stundenkerzen-Auflösung läuft — ein täglicher Check hätte die meisten Signale verpasst bzw. mit veraltetem Preis erfasst.

**Validierte Live-Parameter** (`live_params.py`, Stand 2026-09-07):
```python
DEVIATION_PCT = 10.0
STOP_LOSS_PCT = 6.0
TAKE_PROFIT_FIB = 0.618
```

Bis 2026-09-07 standen hier `4.0 / 2.0 / 0.236`. Diese Kombination stammte aus einer Rasteroptimierung auf der Look-Ahead-behafteten Grundlage und bestand auf sauberer Grundlage **keine einzige** der fünf projekteigenen Mindestbedingungen: der 2-%-Stop löste bei **72,6 %** der Trades aus, bevor die erwartete Korrektur überhaupt Zeit hatte, und nur 4 von 18 Coins trugen positiv bei. Die neue Kombination ist die erste Parameterwahl dieses Bots auf kausal sauberer Grundlage (`research/elliott_wave_params/`, PR #28/#30).

**Validierungsergebnis (kausal sauber, Zigzag 10 % / Stop 6 % / Fib 0,618):**

| | Gesamt (5 Jahre) | Out-of-Sample (18 Monate) |
|---|---|---|
| **Strategie** | **+67,77 %** / MaxDD −10,17 % / Calmar **6,66** | +9,83 % / −4,30 % / Calmar **2,29** |
| Buy-and-Hold | +12,19 % / −79,76 % / Calmar 0,15 | **+88,28 %** / −60,15 % / Calmar 1,47 |

**Ehrliche Einordnung:** Über den Gesamtzeitraum ist der Vorsprung eindeutig — in Rendite **und** Drawdown. Im Out-of-Sample-Fenster (achtzehn Monate stark steigender Markt) verliert die Strategie an reiner Rendite um den Faktor neun und gewinnt nur noch knapp am risikoadjustierten Mass. **Vorbehalt: nur 130 Trades in fünf Jahren, davon 31 out-of-sample** — eine dünne Datenbasis.

### 3.2 T3/ADX/SuperTrend (Krypto)

**Herkunft:** Nutzer stellte ein TradingView-Pine-Script ("Manisch Profit Hunter Strategy") zur Verfügung, ursprünglich für den **15-Minuten-Chart** entwickelt. Analyse ergab mehrere Bugs im Original:
- **Doppelte SuperTrend-Implementierung** (eingebaute `ta.supertrend()` UND eine manuell nachgebaute Version parallel, inkonsistent genutzt)
- **Toter Code**: `entry_filter`/`exit_filter` sollten Trade-Häufigkeit begrenzen, aber die zugehörigen Zähler (`bars_since_last_entry`/`exit`) wurden nie zurückgesetzt — Filter griff faktisch nie
- **Redundante, doppelte Einstiegsbedingungen** (`long_signal_Trend` und `long_signal_T3` fast identisch, beide lösten unabhängig `strategy.entry()` aus)
- **Kein echter Stop-Loss** — Ausstieg hing nur an Crossunder-Signalen

**Sauberer Python-Nachbau** (`indicators.py`, `backtest_trend.py`):
- **T3 (Tillson T3)**: sechsfache EMA-Glättung mit Gewichtungsfaktor, reaktionsschneller als einfacher gleitender Durchschnitt
- **ADX**: Standard-Wilder-Formel (RMA-Glättung von +DM/−DM/TR), misst Trendstärke unabhängig von Richtung
- **SuperTrend**: EINE korrekte, ATR-basierte Implementierung (NumPy-optimiert, siehe Performance-Hinweis unten)
- **Einstieg**: T3 Fast kreuzt T3 Slow von unten nach oben UND ADX > Schwelle
- **Ausstieg**: Stop-Loss ODER SuperTrend-Richtungswechsel ODER T3-Crossunder (per `use_t3_exit`-Flag umschaltbar; Test ergab keinen relevanten Unterschied, blieb aktiviert)

**Performance-Optimierung:** Ursprüngliche Implementierung nutzte pandas `.iloc`-Zugriff in Schleifen — bei mehreren zehntausend Kerzen extrem langsam (>60s Timeout). Umgestellt auf NumPy-Arrays: 5-Jahres-Backtest (43.800 Kerzen) läuft in ~0,12s statt Timeout.

**Zeitrahmen-Odyssee (wichtig für Kontext):**
1. Erst auf 1h getestet → schlechte Ergebnisse (Whipsaws, hohe "Win Rate" aber Netto-Verlust nach Kosten — künstlich durch zu enge Parameter erzeugt)
2. Nutzer wies darauf hin, dass Original-Script auf 15-Minuten-Chart lief → 15m-Datenpipeline gebaut (`fetch_15m_data.py`; **im aktuellen Stand nicht mehr vorhanden**, geprüft — ersetzt durch `fetch_4h_data.py`, siehe unten)
3. 15-Minuten als **unpraktikabel verworfen**: Cronjob müsste alle 15 Min laufen, Handelskosten fressen dünne Margen bei kurzen Haltezeiten auf, Laptop-Abhängigkeit wird kritischer
4. **Entscheidung: 4-Stunden-Chart** — klassischer Zeitrahmen für T3/ADX/SuperTrend als Trendfolge-Indikatoren, passt besser zu Cronjob-Infrastruktur. Datei `fetch_4h_data.py` ersetzte `fetch_15m_data.py` im finalen Code.

**Drawdown-Problem und Lösung:**
- Ohne Schutzmechanismen: Max Drawdown **-39,94%** (naive Positionsgrößen-Simulation ohne Limit) — Ursache: bei breiten Krypto-Markttrends öffnen viele der 25 (korrelierten) Coins gleichzeitig Positionen, die beim Umschwung gemeinsam verlieren
- **`MAX_CONCURRENT_POSITIONS`** eingeführt und empirisch getestet (3 / 5 / 8 / unbegrenzt): **5 war der Sweet Spot** (Rendite 102,7%, Drawdown -31,2% — bei 3 zu wenig Marktteilnahme, bei 8/unbegrenzt kein zusätzlicher Rendite-Nutzen mehr, nur mehr Risiko)
- **BTC-Markt-Regime-Filter** ergänzt (`regime_filter.py`): neue Long-Einstiege werden komplett blockiert, wenn BTC selbst (eigener SuperTrend) im Abwärtstrend ist. Kombiniert mit Positionslimit: Rendite **129,64%**, Max Drawdown **-22,2%** (bestes Ergebnis)
- **VWAP-Filter getestet und wieder verworfen**: isolierter Test auf Out-of-Sample-Teilfenster zeigte Verbesserung (Win Rate 30,6%→35,1%, Ø PnL 0,86%→1,68%), aber volle 5-Jahres-Equity-Simulation mit denselben Parametern zeigte **geringere** Gesamtrendite (129,6%→77,4%) bei fast gleichem Drawdown — VWAP-Filter bringt weniger Trades/Compoundierungsmöglichkeiten, ohne das Risiko zu senken. **Standardmäßig deaktiviert** (`use_vwap_filter=False`), Code bleibt als Option erhalten.

**Validierte Live-Parameter** (`live_params.py`, Stand 2026-08-31):
```python
T3_FAST_LENGTH = 16
T3_SLOW_LENGTH = 30
ADX_THRESHOLD = 20.0
STOP_LOSS_PCT = 4.0
MAX_CONCURRENT_POSITIONS = 5
T3_FACTOR = 0.7            # seit PR #51 hier zentral gefuehrt statt doppelt
DI_LENGTH = 14
ADX_LENGTH = 14
ATR_LENGTH = 22
ATR_MULT = 3.0
```
Regime-Filter: **aktiv**. VWAP-Filter: **deaktiviert**.

Die fünf Indikator-Werte `T3_FACTOR` bis `ATR_MULT` standen bis PR #51 doppelt (einmal in `forward_test.py`, einmal in `backtest_trend.py`) — mit identischen Zahlen, aber zwei Quellen. Sie sind jetzt zentral in `live_params.py` und werden von beiden Seiten importiert. Dieses Muster wurde in der Sync-Reihe (PR #38–#42, #45, #51, #52, #58, #59) für alle neun Bots durchgezogen.

**Erste echte Quartals-Review-Erkenntnis (siehe Abschnitt 6.4):** Agent-2-Vorschlag (T3 12/25, ADX 30, Stop-Loss 3%) sah In-Sample besser aus (Score 0,118 vs. 0,084), aber Out-of-Sample **schlechter** (Score 0,034 vs. 0,046, nur 98 statt 301 Trades) — klassisches Overfitting-Muster, korrekt erkannt und **nicht übernommen**. Aktuelle Parameter unverändert.

### 3.3 Elliott Wave (Aktien)

Gleiche Kern-Wellenerkennungslogik wie Bot 3.1, aber:
- **Datenquelle**: `yfinance` statt Binance (keine offizielle API, gelegentliche Datenqualitätsprobleme, siehe Bug unten)
- **Zeitrahmen**: **Tageskerzen** statt Stunden — klassisch für Elliott Wave bei Aktien, und yfinance liefert Intraday-Daten ohnehin nur für ~2 Jahre zurück, Tagesdaten dagegen oft Jahrzehnte
- **Zeitkonstanten angepasst**: `MAX_HOLD_HOURS` (eigentlich Balken-Anzahl) auf 90 Handelstage gesetzt (nicht 1:1 von Krypto übernommen); `SIGNAL_FRESHNESS_DAYS = 5` statt Stunden

**Aktien-Universum-Entwicklung (Top 25 → 50 → 100 → 150):**
- Start bei Top 25 S&P-500-Werte nach Marktkapitalisierung (`get_top_stocks.py`: scraped Wikipedia-Liste, rankt via `yfinance`-Marktkapitalisierung)
- **Massives Survivorship-Bias-Problem entdeckt**: Buy-and-Hold-Vergleich zeigte, dass simples Halten der 25 Aktien die Strategie um das **20-Fache** schlug (1759% vs. 78% Rendite) — weil "die heutigen Top-25-Aktien" per Definition die Gewinner der Vergangenheit sind
- **Gegenmaßnahmen**: `RECENT_YEARS_ONLY = 10` (begrenzt Backtest-Fenster auf letzte 10 Jahre statt 60+, reduziert aber löst nicht vollständig den Bias) + `buy_and_hold_benchmark.py` als Pflicht-Gegencheck bei jeder Parameter-Bewertung
- **Signal-Qualitäts-Test** (`signal_quality_test.py`) gebaut: vergleicht echte Strategie-Trades mit passivem Halten **während exakt derselben Zeitfenster** (Ein-/Ausstiegszeitpunkt identisch, aber Ausstiegspreis = Schlusskurs statt Stop/Ziel-Preis). Ergebnis (konsistent über alle Universumsgrößen hinweg): **die exakten Stop-Loss-/Take-Profit-Regeln selbst bringen keinen Mehrwert** — passives Halten während derselben Fenster war im Schnitt gleich gut oder minimal besser. Der eigentliche Mehrwert der Strategie kommt aus **Timing** (wann überhaupt investiert sein) und **Kapitalmanagement** (Positionsgröße + -limit), nicht aus der Ausstiegs-Feinjustierung.
- Schrittweise Erweiterung auf Top 50, 100, 150 — bei jeder Erweiterung `MIN_TRADES`/`MIN_SYMBOLS_CONTRIBUTING` proportional angehoben; `MIN_HISTORY_DAYS`-Filter bewusst **zeitraum-basiert** (Tage), nicht kerzenzahl-basiert (Lehre aus Krypto-Entwicklung, da unterschiedliche Zeitrahmen unterschiedliche Kerzendichte pro Kalendertag haben)
- **`use_take_profit`-Dimension** in die Optimierung integriert (Grid-Search testet jetzt auch "kein festes Kursziel, laufen lassen bis Stop/max. Haltedauer" als Option, analog zur Erkenntnis vom T3-Bot)
- **`MAX_CONCURRENT_POSITIONS = 8`** nachgerüstet (fehlte ursprünglich, im Gegensatz zum T3-Bot) — **der WERT ist weiterhin nicht empirisch wie beim T3-Bot getestet** (3/5/8/unbegrenzt), sondern als plausibler Startwert übernommen; das bleibt ein offener Punkt (Abschnitt 9). Die *Anwendung* des Limits ist dagegen inzwischen korrekt: `oos_equity_simulation.py` reichte es zunächst gar nicht durch und lief anschliessend ohne Limit — behoben in PR #48, der Wert kommt jetzt per Import aus `live_params.py`. **14 von 128 OOS-Trades (10,9 %) sind vom Limit betroffen**, nicht 8 wie zuvor geschätzt. OOS danach: +72,39 % / −9,69 % / Calmar 7,47.
- **NaN-Bug gefunden und behoben**: `buy_and_hold_benchmark.py` summierte rohe Schlusskurse; eine einzelne Aktie mit fehlerhaftem/fehlendem yfinance-Kurswert (identifiziert: **APH**, Amphenol) machte die GESAMTE Portfolio-Summe zu `NaN`. Fix: pro Aktie auf `NaN` prüfen, betroffene Aktie überspringen, ihren Kapitalanteil unverändert als "Cash" zur Endsumme addieren (damit Start-/Endkapital vergleichbar bleiben).

**Aktuelle Live-Parameter** (`live_params.py`, Stand 2026-09-03):
```python
DEVIATION_PCT = 5.0
STOP_LOSS_PCT = 3.0
TAKE_PROFIT_FIB = 0.236
USE_TAKE_PROFIT = False     # seit 2026-09-03: Gewinne laufen lassen
MAX_CONCURRENT_POSITIONS = 8
```

**⚠️ Die früher hier dokumentierte Erfolgsmeldung ist überholt.** Hier stand: „Equity-Simulation +1458,12 %, Max Drawdown −1,32 %, Buy-and-Hold +755,69 % → Strategie schlägt Buy-and-Hold klar auf BEIDEN Dimensionen — das stärkste, überzeugendste Ergebnis über die gesamte Entwicklung hinweg."

Diese Zahlen beruhten auf derselben Look-Ahead-Grundlage wie beim Krypto-Bot (siehe 3.1). Auf kausal sauberer Grundlage (`research/elliott_wave_params/`) gilt:

| Gesamtzeitraum (10 Jahre) | Rendite | Max Drawdown | Calmar |
|---|---|---|---|
| **Buy-and-Hold** | **+755,69 %** | −34,83 % | **21,70** |
| dev 5 % / Stop 3 % (live) | +330,18 % | −22,70 % | 14,55 |
| bester geprüfter Kandidat (dev 2 % / Stop 16 % / kein Ziel) | +398,23 % | −34,16 % | 11,66 |

**Buy-and-Hold schlägt die Strategie über den Gesamtzeitraum in Rendite UND im Calmar-Verhältnis.** Keine der 252 geprüften Kombinationen kommt an die +755 % heran, und der beste Kandidat verliert im Walk-Forward in zwei von drei Falten risikoadjustiert gegen Buy-and-Hold. Die aktuelle Live-Kombination ist **nicht schlechter** als die Alternativen — sie ist nur genauso wenig überzeugend. Die Parameter wurden deshalb bewusst **nicht** getauscht: ein Wechsel hätte keinen belegbaren Vorteil gebracht.

**Weiterhin gültig (unabhängig vom Look-Ahead):**
- **Out-of-Sample Walk-Forward** der Live-Kombination: 132 Trades über 79 Symbole, Win Rate 69,7 %, Ø PnL 7,37 % pro Trade — höher als In-Sample (~6,7 %), also kein Overfitting-Muster
- **`USE_TAKE_PROFIT = False`** (2026-09-03): „Gewinne laufen lassen" wurde empirisch getestet und übernommen — Rendite etwa verdoppelt bei moderat höherem, weiterhin klar unter Buy-and-Hold liegendem Drawdown. Der frühere offene Punkt „kein Take-Profit noch nicht getestet" ist damit **erledigt**. Details: `results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md`. Die Look-Ahead-Korrektur hat diese Entscheidung ausdrücklich **bestätigt** und sogar besser begründet.

**Bewusst NICHT (mehr) verfolgt:** Erweiterung auf alle 503 S&P-500-Werte wurde diskutiert und explizit verworfen (löst Survivorship-Bias nicht, ~10× Rechenzeit, yfinance-Zuverlässigkeit bei dieser Größenordnung fraglich, fehlendes Positionslimit hätte Risiko verschärft — Positionslimit wurde stattdessen nachgerüstet und bei moderaterer Größe (150) belassen).

### 3.4 Die sechs später hinzugekommenen Bots

Anfang September 2026 kamen sechs weitere Bots dazu — drei Strategien, jeweils in einer Aktien- und einer Krypto-Fassung. Alle durchliefen dieselbe Validierungskette wie die ersten drei (Backtest → Walk-Forward → Equity-Simulation → Buy-and-Hold → strategie-spezifische Zusatztests) und laufen seither live im Paper-Trading. Ausführliche Begründung je Bot in `results/<bot>/PROTOTYPE_FINDINGS.md`, die jeweilige Historie im Kopf der `live_params.py`.

| Bot | Kernlogik | Live-Parameter | Bemerkenswert |
|---|---|---|---|
| `rsi2_mean_reversion` (Aktien) | RSI-2 unter Schwelle, Rückkehr zum Mittel, Zeit-Exit | `RSI_THRESHOLD=5.0`, `STOP_LOSS_PCT=None`, `MAX_HOLD_DAYS=10`, `ALLOCATION_PCT=5`, `MAX_CONCURRENT_POSITIONS=20` | **Kein Stop-Loss** — empirisch belegt, dass ein harter Stop den Ø-Gewinn senkt. 5 % Allokation / Limit 20 aus der Kapitalmanagement-Nachprüfung statt des Startwerts 8 |
| `rsi2_crypto` | dasselbe, für Krypto rekalibriert | `SMA_TREND_FILTER=150`, `RSI_THRESHOLD=10.0`, `STOP_LOSS_PCT=None`, `MAX_HOLD_DAYS=10`, `ALLOCATION_PCT=10`, `MAX_CONCURRENT_POSITIONS=8` | SMA-Trendfilter auf 150 Tage statt 200 (Aktien-Fassung). **BTC-Regime-Filter NICHT übernommen** — er schadet der Mean-Reversion-Logik deutlich. Kein Kapital-Flaschenhals festgestellt, deshalb Standard-Kapitalmanagement belassen |
| `turtle_soup_stocks` | False-Breakout-Reversal an Donchian-Extremen | `DONCHIAN_PERIOD=10`, `STOP_MODE=None`, `MAX_HOLD_DAYS=10`, `ALLOCATION_PCT=2`, `MAX_CONCURRENT_POSITIONS=None` | **Kein Positionslimit** — bei 2 % Allokation sättigt die Kapitalbindung rechnerisch bei ~50 offenen Positionen, ein Limit wäre kein Risikohebel mehr, sondern würde nur Signale blockieren. Der musterspezifische „structural"-Stop war bei Aktien empirisch die **schlechteste** Variante |
| `turtle_soup_crypto` | dasselbe, für Krypto | `DONCHIAN_PERIOD=10`, `STOP_MODE='structural'`, `MAX_HOLD_DAYS=10`, `ALLOCATION_PCT=10`, `MAX_CONCURRENT_POSITIONS=8` | Hier gewinnt der **structural**-Stop (Stop = Tagestief des Setup-Tags) — umgekehrt zur Aktien-Fassung. Kapitalmanagement bewusst **unverändert**: jede getestete Lockerung verschlechterte Rendite, Drawdown und die 2022-Krypto-Winter-Performance gleichzeitig |
| `volatility_breakout` (Aktien) | Bollinger-Band-Squeeze mit Ausbruch | `BB_SQUEEZE_PERCENTILE=25.0`, `BB_LOOKBACK=126`, `STOP_LOSS_PCT=8.0`, `MAX_HOLD_DAYS=15`, `ALLOCATION_PCT=10`, `MAX_CONCURRENT_POSITIONS=15` | Volumen-Filter und Trailing-Stop getestet und **verworfen** (Trailing-Stop zeigte dasselbe Overfitting-Muster wie beim Elliott-Aktien-Bot). Bekanntes, dokumentiertes Restrisiko: ausgeprägte **2022-Bärenmarkt-Schwäche**, die auch das angepasste Kapitalmanagement nicht mildert |
| `volatility_breakout_crypto` | dasselbe, für Krypto | `STOP_LOSS_PCT=5.0`, `BTC_REGIME_FILTER_ENABLED=True`, sonst wie oben, `MAX_CONCURRENT_POSITIONS=8` | **BTC-Regime-Filter aktiv — als Risikomassnahme, nicht als Rendite-Hebel.** Bei einem von drei Split-Punkten war die Rendite MIT Filter niedriger (+18,45 % vs. +20,04 %); übernommen wurde er, weil der Max Drawdown in **allen drei** Splits sinkt (z. B. −11,33 % → −7,76 %) und die 2022-Schwäche gedämpft wird |

**Muster, die sich über diese sechs Bots gezeigt haben** (und die für künftige Prototypen gelten sollten):
- **Aktien und Krypto verlangen unterschiedliche Antworten auf dieselbe Frage.** Beim Turtle-Soup-Stop und beim Kapitalmanagement fiel die Entscheidung jeweils **entgegengesetzt** aus. Eine Krypto-Fassung ist nie eine blosse Parameter-Kopie der Aktien-Fassung.
- **„Kein Stop-Loss" ist bei Mean-Reversion-Logiken empirisch oft die bessere Wahl** (beide RSI-2-Bots, `turtle_soup_stocks`) — der Zeit-Exit trägt dort allein.
- **Der BTC-Regime-Filter ist kein Universalwerkzeug**: hilfreich bei `t3_supertrend` und `volatility_breakout_crypto`, schädlich bei `rsi2_crypto`.

---

## 4. Gemeinsame Architektur

### 4.1 Ordnerstruktur und Pfad-Auflösung

```
trading-bot/
├── trading-env/                        (Python-3.9-venv)
├── shared/                             (von ALLEN neun Strategien genutzt)
│   ├── paths.py                        (BASE_DIR/DATA_DIR/CONFIG_DIR-Auflösung für strategie-unabhängige Skripte)
│   ├── strategy_paths.py               (Kernstück: get_strategy_paths(__file__) leitet automatisch
│   │                                     RESULTS_DIR, LOGS_DIR, DB_FILE aus dem STRATEGIE-ORDNERNAMEN ab —
│   │                                     neue Strategie hinzufügen = Ordner kopieren, keine Shared-Code-Änderung nötig)
│   ├── fetch_binance_data.py           (Krypto: Einzelsymbol-Abruf-Funktion — gitignored, liegt nur auf
│   │                                     dem Rechner des Nutzers, enthält Zugangsdaten)
│   ├── fetch_multi_data.py             (Krypto: Multi-Symbol-Abruf, 1h, von elliott_wave genutzt)
│   ├── get_top_symbols.py              (Krypto: rankt Binance-USDT-Paare nach 24h-Volumen,
│   │                                     filtert Stablecoins/gehebelte Token, → top25_symbols.txt)
│   ├── symbols_config.py               (Krypto: SYMBOLS-Liste aus top25_symbols.txt)
│   ├── claude_client.py                (Anthropic-API-Wrapper, siehe Abschnitt 6)
│   ├── daily_interpreter.py            (Agent 1)
│   ├── market_context_agent.py         (Agent 3)
│   ├── param_search_agent.py           (Agent 2)
│   ├── quarterly_interpreter.py        (Quartals-Empfehlungs-Agent)
│   ├── portfolio_interpreter_agent.py  (Agent 4: wöchentliche Portfolio-Einordnung)
│   ├── portfolio_overview.py           (Beobachtungs-Portfolio über alle Bots, rein lesend, KEIN gemeinsames Konto)
│   ├── weekly_portfolio_email.py       (orchestriert Agent 4 um portfolio_overview.py)
│   ├── empfehlung_format.py            (EINZIGE Stelle für die Hervorhebung von Handlungsempfehlungen, 13 Versandstellen)
│   ├── data_quality.py                 (erkennt unvollständige Kursbalken — Lehre aus dem APH-Vorfall)
│   ├── build_daily_crypto_data.py      (leitet Tageskerzen aus vorhandenen 1h-Daten ab, für die Krypto-Prototypen)
│   ├── status_overview.py              (kostenloser Multi-Bot-Statuscheck ohne API-Aufrufe)
│   └── test_empfehlung_format.py       (Selbsttests der Empfehlungs-Hervorhebung)
├── notifications/                      (Beobachtungsebene 1: Telegram, rein lesend — siehe 4.3)
│   ├── monitor.py                      (Lese-/Erkennungslogik, öffnet alle Bot-DBs read-only)
│   ├── telegram_bot.py                 (Befehle /status /positions /pnl /help + periodischer Ereignis-Job)
│   ├── notify.py                       (send_alert() ohne Zusatz-Abhängigkeit, für beliebige Skripte)
│   ├── telegram_config.py              (TELEGRAM_BOT_TOKEN/TELEGRAM_USER_ID aus .env)
│   ├── manual_close.py                 (die EINE schreibende Kernfunktion: schliesst genau eine Position,
│   │                                     BEGIN IMMEDIATE + erneute Prüfung in der Transaktion, PR #62)
│   ├── boersenkalender.py              (echter NYSE-Kalender; beantwortet nur "ist die Börse offen", PR #69/#71)
│   ├── warteauftraege.py               (persistente Auftragsverwaltung: anlegen, auflisten, stornieren,
│   │                                     abschliessen; JSON + eigene Sperrdatei, PR #69/#71)
│   ├── test_manual_close.py            (Selbsttests der Schreibfunktion)
│   └── com.manisch.telegram-tradesignal-bot.plist   (launchd-Vorlage)
├── dashboard/                          (Beobachtungsebene 2: Web/PWA — LIEST UND SCHREIBT, siehe 4.3)
│   ├── server.py, app.py, konfig.py, datenquelle.py
│   ├── schliessen.py                   (Schliess-Wege: eine Position, alle eines Bots, alle aller Bots;
│   │                                     Warteauftrags-Fallunterscheidung — ruft manual_close.py)
│   ├── warteauftraege_ausfuehren.py    (eigenständiges Cronjob-Programm: das EINZIGE, das zeitversetzt
│   │                                     schreibt — siehe 4.3 und Abschnitt 8)
│   ├── pruefe_warteauftraege_kopie.py  (Selbstprüfung gegen eine Arbeitskopie, nur mit .probe-kopie)
│   ├── test_dashboard.py, test_gewichtung.js, test_zeitzone.js, test_zustandsmaschine.js
│   └── static/                         (index.html, bot.html, app.js, style.css, sw.js, manifest.json, Icons)
├── broker/                             (Broker-Brücken — der EINZIGE Code, der Orders sendet, siehe 4.4)
│   ├── bot_db.py                       (gemeinsamer, schreibgeschützter Leser beider Brücken, mode=ro)
│   ├── zugang.py, binance_testnet.py, spiegel.py, abgleich.py    (Binance-Testnet, PR #68)
│   ├── ibkr_zugang.py, ibkr_paper.py, ibkr_spiegel.py, ibkr_abgleich.py   (IBKR-Paper, PR #70)
│   ├── test_broker.py, test_ibkr.py
│   ├── requirements.txt                (eigene Liste, NICHT in der Wurzel-requirements.txt eingebunden)
│   ├── README.md, README_IBKR.md
│   └── STOP / STOP_IBKR                (Notbremsen — je Brücke eine eigene Datei; nicht im Repo)
├── system/                             (Systemdienste des Mac, PR #72)
│   ├── com.manisch.caffeinate.plist    (launchd-Vorlage: hält den Mac wach, siehe 4.5)
│   ├── README_CAFFEINATE.md, TESTAUFTRAG_CAFFEINATE.md
│   └── test_caffeinate_plist.py
├── research/                           (abgeschlossene Untersuchungen, je ein BERICHT.md — NIE Bot-Code)
│   └── elliott_wave_lookahead/, elliott_wave_params/, sync_check/, hrp_portfolio/, … (17 Ordner)
├── strategies/                         (NEUN Bots, siehe Abschnitt 2)
│   ├── elliott_wave/                   (Krypto, 1h)
│   ├── t3_supertrend/                  (Krypto, 4h)
│   ├── rsi2_crypto/                    (Krypto, 1 Tag)
│   ├── turtle_soup_crypto/             (Krypto, 1 Tag)
│   ├── volatility_breakout_crypto/     (Krypto, 1 Tag)
│   ├── elliott_wave_stocks/            (Aktien, 1 Tag)
│   ├── rsi2_mean_reversion/            (Aktien, 1 Tag)
│   ├── turtle_soup_stocks/             (Aktien, 1 Tag)
│   └── volatility_breakout/            (Aktien, 1 Tag)
│       [jeweils mit strategie-eigenen Dateien, siehe Abschnitt 5]
├── data/                               (gemeinsamer Ordner für Kursdaten-CSVs, z.B. BTCUSDT_1h.csv,
│                                         AAPL_1d.csv — Dateinamen verhindern Kollisionen zwischen Strategien)
├── config/
│   ├── email_config.py                 (SMTP-Zugangsdaten IONOS/1&1 + ANTHROPIC_API_KEY, siehe Abschnitt 6.5
│   │                                     — gitignored, liegt nur auf dem Rechner des Nutzers)
│   ├── top25_symbols.txt               (Krypto-Symbolliste)
│   └── sp500_top150.txt                (Aktien-Symbolliste, aktueller Stand; daneben sp500_top50.txt
│                                         und sp500_top25.txt aus früheren Zuschnitten)
├── requirements.txt                    (Wurzel-Liste: bindet notifications/ und dashboard/ ein und ergänzt
│                                         pandas_market_calendars>=4.1,<5 — die Obergrenze ist nötig, weil die
│                                         5.x-Reihe auf dem Python 3.9.6 des Nutzers beim Import abbricht.
│                                         broker/requirements.txt steht bewusst daneben, nicht darin)
├── .env                                (TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID, DASHBOARD_ACCESS_TOKEN,
│                                         Binance-Testnet- und IBKR-Paper-Zugänge — gitignored)
├── docs/UEBERGABEPROTOKOLL.md          (dieses Dokument)
├── docs/UEBERGABE_*.md                 (Übergaben einzelner PRs: Warteaufträge #71, Positionsanzahl/Notbremse #73)
├── CLAUDE.md                           (wird von jeder Session zuerst gelesen, verweist hierher)
├── results/<strategie_name>/           (Backtest-/Optimierungs-Ergebnis-CSVs, PROTOTYPE_FINDINGS.md)
├── logs/<strategie_name>/              (Cronjob-Log-Dateien)
└── paper_trading_<strategie_name>.db   (neun Stück, gitignored)
```

**Design-Prinzip `strategy_paths.py`:** Jedes Strategie-Skript beginnt mit diesem Boilerplate:
```python
import os, sys
_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
_SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
sys.path.insert(0, _SHARED_DIR)
from strategy_paths import get_strategy_paths
_P = get_strategy_paths(__file__)
DB_FILE = _P["DB_FILE"]          # automatisch: paper_trading_<ordnername>.db
STRATEGY_NAME = _P["STRATEGY_NAME"]
RESULTS_DIR = _P["RESULTS_DIR"]  # automatisch: results/<ordnername>/
LOGS_DIR = _P["LOGS_DIR"]        # automatisch: logs/<ordnername>/
CONFIG_DIR = _P["CONFIG_DIR"]
```
Dieses Muster hat sich bewährt und sollte für **jede zukünftige Strategie** genauso verwendet werden.

**`live_params.py`-Muster:** Jede Strategie hat eine kleine, von der restlichen Logik getrennte Datei mit den aktuell aktiven Parametern, importiert von `forward_test.py`, `equity_simulation.py`, `oos_equity_simulation.py`, `quarterly_review.py`, `agent_optimise.py`. Zweck: Parameter-Übernahme nach Validierung soll so einfach und risikoarm wie möglich sein (eine kleine, übersichtliche Datei bearbeiten statt tief im Code zu suchen).

### 4.2 Ein Wert, eine Quelle — die Sync-Reihe

**Die Sync-Reihe (PR #38–#42, #45, #48, #51, #52, #58, #59).** Über mehrere Runden wurde bei allen neun Bots jede Doppelführung von Handelsparametern beseitigt: Werte, die sowohl in `live_params.py` als auch in einem Backtest-/Simulationsskript standen, werden jetzt **importiert** statt zweimal geschrieben. Der Anlass war real — Backtest und Live liefen bei fünf Bots messbar auseinander, ohne dass es jemandem aufgefallen wäre.

**Aktueller Stand: synchron.** `research/sync_check/sync_table.py` prüft alle neun Bots automatisch und meldet **keine** Abweichung mehr. Was in der Tabelle bewusst NICHT als Abweichung erscheint:

| Fall | Warum kein Befund |
|---|---|
| `DONCHIAN_PERIOD` (beide Turtle-Bots) | wird von `multi_symbol_optimise.py` über `DONCHIAN_PERIOD_RANGE = [10, 20, 40]` **absichtlich variiert** — eine Kopplung nähme dem Suchraster seine Freiheit |
| `ALLOCATION_PCT` (Elliott-Bots) | steht dort nicht in `live_params.py`; diese Bots haben bewusst kein Positionslimit-Konzept dieser Art |
| ATR-Literale in `t3_supertrend/regime_filter.py` | der Regimefilter rechnet auf **BTC**, nicht auf dem Handelssymbol — gleiche Zahlen, andere Grösse |

Eine wichtige methodische Lehre daraus (Nachtrag S des Berichts): die letzten 15 gemeldeten „Abweichungen" waren **keine** — der Prüfer las nur `ast.Assign`, nicht die Importe, und meldete damit bereits gekoppelte Werte als offen. Geändert wurde der **Prüfer**, nicht der Bot. Die Abweichung bestand zwischen Wirklichkeit und Messung.

### 4.3 Beobachtungsebene: Telegram-Bot und Dashboard

**Diese Einleitung stand bis 2026-09-11 falsch hier.** Sie lautete „Beide lesen ausschliesslich; keiner von beiden verändert einen Bot, eine Datenbank oder einen Parameter." Für den **Telegram-Bot gilt das weiterhin**. Für das **Dashboard nicht mehr** — seit PR #62 schreibt es, seit PR #71 sogar zeitversetzt:

| Ebene | Liest | Schreibt |
|---|---|---|
| `notifications/` — Telegram | ja | **nein**, unverändert rein lesend |
| `dashboard/` — Web/PWA | ja | **ja**: Positionen manuell schliessen (PR #62), Warteaufträge anlegen und ausführen lassen (PR #71) |

Der Telegram-Weg zum Schliessen (`/schliessen`, PR #61) wurde gebaut, aber **nicht gemergt** — der Pull Request ist am 2026-09-10 ohne Merge geschlossen worden. Im Quelltext von `telegram_bot.py` steht ausdrücklich, dass das bewusst nicht vorbereitet ist. Der Dashboard-Weg hat ihn abgelöst.

Beide Ebenen ersetzen die früheren täglichen E-Mails (siehe Abschnitt 5, `daily_summary_email.py`).

**Die schreibenden Wege des Dashboards im Überblick** (Einzelheiten: `dashboard/README.md`, `docs/UEBERGABE_PR71_WARTEAUFTRAEGE.md`):

| Weg | Bestätigung | Freigeschaltet für |
|---|---|---|
| eine einzelne Position | ein Tap auf die Zusammenfassung (Vorgangs-Kennung als eigentliche Absicherung) | **alle neun Bots** |
| alle Positionen EINES Bots (Notfallweg) | zwei Klicks auf zwei verschiedene Knöpfe | alle neun Bots |
| alle Positionen ALLER Bots (Crash-Weg) | zwei Klicks **und** der getippte Text `CRASH` | alle neun Bots |
| **Warteauftrag** bei geschlossener Börse | zusätzlicher Warnschritt; Ausführung später **ohne erneute Rückfrage** | die vier Aktien-Bots |

Geschrieben wird immer über **eine** Funktion: `notifications/manual_close.py::schliesse_position()` — mit `BEGIN IMMEDIATE`, erneuter Prüfung *innerhalb* der Transaktion, `rowcount == 1` und eigenem Protokoll (`logs/notifications/manuelle_eingriffe.log`, Marke `MANUELLER-EINGRIFF`). Auch das Cronjob-Programm ruft dieselbe Funktion; eine zweite Schreiblogik gibt es bewusst nicht. Manuelle Ausstiege sind dauerhaft an `result='manual_close'` erkennbar — ein Wert, den kein Bot je selbst schreibt.

**Warteaufträge (PR #69/#71) — die folgenreichste Eigenschaft.** Bei den vier Aktien-Bots erschien der Schliessen-Knopf früher auch ausserhalb der Börsenzeiten und schloss dann zum letzten Tages-Schlusskurs aus yfinance — über ein Wochenende zweieinhalb Tage alt. Jetzt entscheidet ein echter NYSE-Kalender (`pandas_market_calendars`) über drei Zustände: **offen** → sofort schliessen, **geschlossen** → vormerken, **unbekannt** → weder noch. Der dritte Zustand ist Absicht: ein Warteauftrag ohne funktionierenden Kalender wäre eine Absicht, die niemand einlösen kann, weil das Ausführungsskript am selben Kalender hängt. Eine Faustregel als Rückfallebene wurde bewusst **nicht** eingebaut — sie schlüge genau dann zu, wenn niemand hinsieht.

`dashboard/warteauftraege_ausfuehren.py` ist das einzige Programm des Projekts, das **zeitversetzt und ohne gleichzeitige menschliche Bestätigung** schreibt. **Ohne den Cronjob passiert nichts**: Aufträge werden angelegt, angezeigt und nie ausgeführt. Wer den Cronjob einrichtet, erteilt damit eine Vorab-Erlaubnis für alle künftigen Warteaufträge — siehe Abschnitt 8 und 9.

**`notifications/` — Telegram (PR #16, #34).** Ein eigenständiger Dienst (launchd), der
- die Befehle `/status`, `/positions`, `/pnl` und `/help` beantwortet, je optional gefiltert nach `krypto`, `aktien` oder einem Bot-Namen,
- periodisch (`poll_job`) die Live-Datenbanken auf Ereignisse prüft und **Push-Nachrichten** schickt: neuer Trade, Stop-Loss, ausgebliebener Cronjob-Lauf,
- die Rolle der früheren täglichen Bot-E-Mails übernimmt: nicht indem er sie zustellt, sondern indem dieselben Zahlen jederzeit **auf Abruf** verfügbar sind. Deshalb konnten die neun täglichen Cronjobs abgeschaltet werden (PR #36).

**Welcher Bericht über welchen Kanal läuft** — bewusst nicht einheitlich:

| Bericht | Kanal | Status |
|---|---|---|
| Tageszahlen je Bot | Telegram, auf Abruf (`/status`, `/positions`, `/pnl`) + Dashboard | aktiv |
| Ereignisse (neuer Trade, Stop-Loss, ausgebliebener Lauf) | Telegram-Push | aktiv |
| `daily_summary_email.py` (9×) | E-Mail (SMTP/IONOS) | **Cronjob deaktiviert**, Skript manuell lauffähig |
| `weekly_portfolio_email.py` (Agent 4) | E-Mail | aktiv |
| `quarterly_review.py` | E-Mail | aktiv (Cron-Eintrag je Bot unbestätigt, siehe Abschnitt 9) |

Die Quartals- und Wochenberichte sind lange, zum Nachlesen gedachte Texte — dafür ist E-Mail das passendere Medium als eine Chat-Nachricht. Alle drei Mail-Wege nutzen `shared/empfehlung_format.py` für die Hervorhebung von Handlungsempfehlungen.

Zugriffsschutz ist die `TELEGRAM_USER_ID` aus `.env` (`restricted()`-Decorator); jeder andere Absender wird ignoriert und geloggt. Die Lese-/Erkennungslogik liegt in `monitor.py`, das alle Bot-Datenbanken im SQLite-Modus `ro` öffnet — dieselbe Quelle nutzt auch das Dashboard, damit beide nie unterschiedliche Zahlen zeigen können.

Zwei Eigenheiten, die viel Diagnosezeit gekostet haben und deshalb im Code ausführlich dokumentiert sind: `CommandHandler` erkennt einen Befehl nur, wenn Telegram die erste MessageEntity als `bot_command` markiert — deshalb wird stattdessen `MessageHandler(filters.Regex(...))` benutzt. Und blockierende Kursabfragen dürfen aus einer async-Funktion **niemals** direkt aufgerufen werden, sondern nur über `asyncio.to_thread()` mit hartem Timeout, sonst friert der ganze Event-Loop ein.

**`dashboard/` — Web-Dashboard und PWA (PR #35, #44, #46, #53, #60).** FastAPI-Backend plus kleines Frontend ohne Framework und ohne nachgeladene Fremdressourcen (die PWA soll offline funktionieren). Funktionsumfang:
- Übersicht aller neun Bots, Verlaufsdiagramm, Detailseite je Bot mit offenen Positionen und letzten Trades
- **Automatische Aktualisierung** (PR #44): zwei Takte — Datenbankdaten jede Minute, Live-Kurse alle 2,5 Minuten (externe API-Aufrufe sind teurer); hängt an `document.visibilityState`, überlappende Läufe werden verhindert, ein fehlgeschlagener Lauf leert die Anzeige nicht, sondern markiert sie dezent als veraltet
- **Ladeindikator** (PR #46) mit drei sich gegenseitig ausschliessenden Zuständen (normal / lädt / veraltet), Rücksicht auf `prefers-reduced-motion`
- **Zeitzonen-Korrektheit** (PR #53): der Server liefert eigene Zeitstempel als ISO-8601 **mit Offset**, der Browser rechnet in seine Zeitzone um. Vorher kam der „Stand" naiv in UTC und die Anzeige stand zwei Stunden zurück. Kerzen-Zeitstempel aus den Bot-Datenbanken werden bewusst **nicht** verschoben — sie sind Marktzeiten, keine Wanduhrzeit des Nutzers
- **Visuelle Überarbeitung** (PR #60): gestaffelte Flächen statt Schlagschatten, grössere Kachelwerte auf gemeinsamer Grundlinie, und eine **farbenblind-sichere Diagramm-Palette** (die bisherige Reihenfolge stellte Orange neben Grün — ΔE 1,9 für Protanopie, also praktisch dieselbe Linie)

Zugriffsschutz ist ein `DASHBOARD_ACCESS_TOKEN` aus `.env`, geprüft über `hmac.compare_digest`; der Server startet ohne Token gar nicht (fail closed) und bindet standardmässig nur an `127.0.0.1`.

### 4.4 Broker-Brücken: der erste Schreibzugriff auf eine Börse

Unter `broker/` liegt der **einzige Code des Projekts, der Orders an eine externe Gegenstelle sendet**. Kein Bot tut das, kein Agent tut das. Es sind zwei voneinander unabhängige Brücken; gemeinsam ist ihnen nur der schreibgeschützte Leser `broker/bot_db.py`.

| | Binance-Testnet (PR #68) | IBKR-Paper (PR #70) |
|---|---|---|
| Spiegelt | `t3_supertrend` (Krypto) | `volatility_breakout` (Aktien) |
| Gegenstelle | Binance **SPOT-Testnet**, virtuelles Guthaben | **IBKR-Paper-Konto** über lokal laufende TWS / IB Gateway |
| Weg | REST, Endpunkt als Literal im Code | Socket `127.0.0.1:7497` bzw. `4002` |
| Hauptdatei | `broker/spiegel.py` | `broker/ibkr_spiegel.py` |
| Nachverfolgung | `broker_testnet_t3_supertrend.db` | `broker_ibkr_volatility_breakout.db` |
| Notbremse | `broker/STOP` | `broker/STOP_IBKR` |
| Cronjob | alle 4 h zur Minute 5 (hinter dem Bot) | alle 30 min während der US-Sitzung, Mo–Fr |
| **Stand** | **produktiv** | **gemergt, aber nie gegen eine echte TWS gelaufen** |

**Was unverändert bleibt:** `forward_test.py`, `live_params.py` und die `trades`-Tabelle jedes Bots. Die Brücken lesen die Bot-Datenbank über `file:…?mode=ro` — SQLite verweigert dort jeden Schreibversuch, auch einen versehentlichen. Ihre eigene Nachverfolgung liegt je in einer eigenen Datei.

**Was sie nicht sind:** kein Live-Trading. Der Endpunkt steht jeweils als Literal im Code, es gibt keine Umgebungsvariable, die ihn verschieben könnte, und die echten Handelsendpunkte bzw. Live-Ports stehen namentlich auf Verbotslisten. Der **Trockenlauf ist der Standard**; gesendet wird nur mit `--echt`.

**Die Notbremse wird auf drei Ebenen geprüft** (Ebene 1 seit PR #73):

| Ebene | Wo | Greift wann |
|---|---|---|
| 1 | `lauf(echt=True)`, zu Beginn | die Bremse lag schon vor dem Lauf — meldet sichtbar und beendet den Lauf, **bevor** Testnet bzw. TWS überhaupt kontaktiert werden |
| 2 | `spiegle_eine()`, je Aufgabe | die Datei wird **mitten im Lauf** angelegt, und genau dann wird sie angelegt |
| 3 | `binance_testnet.marktorder()` / `ibkr_paper.marktorder()` | letzte Rückfallebene |

Ebene 1 kam hinzu, weil ein gebremster Lauf **ohne offene Aufgabe** vorher von einem gewöhnlichen Leerlauf nicht zu unterscheiden war: keine Zeile, Rückgabewert 0. Das hatte bereits zu der falschen Meldung geführt, die Bremse greife nicht. Zur Wahl des Rückgabewerts siehe Abschnitt 8.

**Zwei Einschränkungen, die zum Stand gehören:**

1. **Die IBKR-Brücke ist nie gegen eine echte TWS gelaufen.** Sie wurde vollständig gegen eine Attrappe geprüft, aber niemand hat je eine TWS gestartet. Der häufigste Ausfall wird deshalb kein Fehler der Brücke sein, sondern eine abgemeldete TWS nach deren täglichem Neustart.
2. **`ib_async` verlangt Python 3.10+**, der Rechner des Nutzers läuft auf 3.9.6 (`trading-env`). Die IBKR-Brücke ist dort derzeit **nicht lauffähig**; die Selbsttests laufen auch ohne die Bibliothek, überspringen dann aber den Abschnitt, der die Annahmen über deren Schnittstelle prüft.

Ein Binance-Testnet-Konto wird periodisch (etwa monatlich, ohne Vorankündigung) zurückgesetzt; Schlüssel und Bestände sind danach neu zu erzeugen. Das ist normal und kein Fehler der Brücke.

Einzelheiten und die gestaffelten Inbetriebnahme-Anleitungen: `broker/README.md` und `broker/README_IBKR.md`.

### 4.5 Betrieb auf dem Mac: drei launchd-Dienste und der Schlaf

Alles läuft auf dem Mac des Nutzers. Neben den Cronjobs gibt es inzwischen **drei** launchd-Dienste:

| Dienst | Zweck | Vorlage im Repo |
|---|---|---|
| Dashboard | FastAPI-Server der Beobachtungsebene 2 | — |
| Telegram-Bot | Befehle und Push-Nachrichten | `notifications/com.manisch.telegram-tradesignal-bot.plist` |
| **`com.manisch.caffeinate`** (PR #72) | hält den Mac wach, damit Cron überhaupt läuft | `system/com.manisch.caffeinate.plist` |

**Warum der dritte Dienst existiert — der Vorfall vom 11.09.2026.** Nach einem macOS-Update war das von Hand gestartete `caffeinate` ersatzlos verschwunden, ohne Hinweis. Der Mac schlief zwischen etwa **08:50 und 12:06**. In dieser Zeit fielen aus: der **12:05-Lauf der Binance-Brücke** komplett und mehrere **stündliche `elliott_wave`-Forward-Tests**.

Das ist mehr als eine Lücke im Log. **Cron holt verpasste Läufe nicht nach** — ein schlafender Mac bedeutet nicht „später", sondern „gar nicht". Ein Signal, das während einer Schlafphase entsteht, wird **nie** erkannt; die Paper-Trading-Auswertung zeigt danach eine Strategie, die so nie gelaufen ist. Fehlende Läufe verfälschen die Ergebnisse still und ohne Fehlermeldung.

**Die Folge für die Daten steht in [`docs/DATENLUECKEN.md`](DATENLUECKEN.md)** — einem fortlaufenden Register, das je Ausfall festhält, was ausgefallen ist, was nachgeholt wurde und was das für die Auswertung bedeutet. Der Brücken-Lauf von 12:05 wurde später von Hand nachgeholt, die Forward-Tests nicht: sie sind an ihre Kerzenzeit gebunden. Wer Forward-Test-Zahlen auswertet, sollte dort zuerst nachsehen.

Der Dienst ruft `/usr/bin/caffeinate -i -m -s` (Idle-Sleep, Platten-Sleep, Sleep bei Netzbetrieb), startet bei jeder Anmeldung (`RunAtLoad`) und wird bei Prozessende neu gestartet (`KeepAlive`). `-d`/`-u` (Display wachhalten bzw. einschalten) sind bewusst **nicht** gesetzt: ein dunkles Display ist kein Schlaf, die Cronjobs laufen davon unberührt.

**Vier dokumentierte Grenzen, bewusst nicht gelöst** (`system/README_CAFFEINATE.md`):

1. **Ein zugeklapptes MacBook schläft trotzdem** (Clamshell-Sleep ohne externen Monitor). `caffeinate` verhindert Idle-Sleep, nicht den vom Nutzer ausgelösten — der Mac muss aufgeklappt bleiben.
2. **Ein LaunchAgent startet erst nach der grafischen Anmeldung.** Nach einem Neustart muss sich jemand anmelden. Das gilt für Dashboard und Telegram-Bot schon heute und ist damit keine neue Einschränkung.
3. **Ein LaunchDaemon in `/Library/LaunchDaemons` würde schon beim Systemstart greifen** — braucht aber `sudo`, Eigentümer `root` und andere Rechte. Nur als **Option erwähnt, bewusst nicht umgesetzt**.
4. **Bei reinem Batteriebetrieb wirkt `-s` nicht.** Für den Dauerbetrieb gehört der Mac ans Netzteil.

Das Repo enthält nur die Vorlage; das Kopieren nach `~/Library/LaunchAgents/` führt der Nutzer selbst aus. `python3 system/test_caffeinate_plist.py` prüft die Datei (gültiges XML, erwartete Schlüssel, korrekte Flags, kein `-d`/`-u`) und läuft auch ohne macOS.

### 4.6 Log-Rotation (PR #79)

Mehrere Logdateien unter `logs/` wuchsen unbegrenzt. Das Problem war nicht der Platz, sondern die **Lesbarkeit**: in einer Datei, die zu neun Zehnteln aus wiederholten Routinemeldungen besteht, geht eine echte Fehlermeldung unter — und genau danach wurde beim Vorfall vom 11.09.2026 gegriffen.

`system/log_rotation.py` rotiert nach **Grösse** (Schwelle 1 MB), behält **5 Stände** und läuft per Cron oder von Hand. Kein Zustand, keine Datenbank: die Entscheidung fällt allein anhand der aktuellen Dateigrösse, der Lauf ist beliebig oft wiederholbar. Gesucht wird nach `logs/**/*.log` — gesucht statt aufgelistet, damit kein neuer Bot vergessen wird; alles, was nicht auf `.log` endet, bleibt damit automatisch aussen vor (Datenbanken, `state.json`, `.env`).

**Kopieren und leeren, nicht umbenennen.** Dashboard, Telegram-Bot und `caffeinate` halten ihre Logdatei dauerhaft offen. Ein `mv` nimmt das offene Dateihandle mit: der Dienst schreibt weiter in die umbenannte Datei, die neue bleibt für immer leer — und es fällt erst beim nächsten Fehler auf, wenn man in der falschen Datei sucht. Stattdessen wird kopiert und die Datei anschliessend geleert (`truncate`); sie behält ihren **Inode**, jedes offene Handle zeigt weiter auf dieselbe, nun leere Datei. Voraussetzung ist `O_APPEND`, und das ist bei allen Schreibern dieses Projekts nicht Annahme, sondern Funktionsweise: Cron schreibt mit `>>`, launchd öffnet anhängend, `logging.FileHandler` benutzt `mode="a"`.

**Die Restlücke ist benannt und beziffert.** Zwischen dem letzten Lesevorgang und dem Leeren kann eine Zeile verloren gehen — die bekannte Eigenschaft jedes Kopieren-und-Leeren-Verfahrens, ohne Mitwirkung der schreibenden Prozesse nicht auflösbar. Gemessen: bei 200 Zeilen/s **null** von 6.092 Zeilen über 60 Rotationen, bei 5.000 Zeilen/s höchstens **eine** Zeile je 10 Rotationen (~0,1 je Rotation). In der ersten Fassung stand der `fsync` *nach* dem letzten Lesevorgang und kostete knapp **eine Zeile pro Rotation** — jetzt liegt alles Teure davor, und der Selbsttest sichert die Reihenfolge über einen Zähler und ein künstlich verlangsamtes `fsync` deterministisch ab.

**Zwei Abweichungen von der Standardbehandlung, beide begründet:**

| Datei | Behandlung | Grund |
|---|---|---|
| `logs/broker/testnet_spiegel.log`, `logs/broker/ibkr_paper_spiegel.log` | **20 Stände** statt 5 | Dort stehen Order-IDs, Ausführungspreise, Gebühren und der Verlauf fehlgeschlagener Versuche. Tragfähig ist die Rotation nur, weil das **Endergebnis jeder Order zusätzlich in der Broker-Datenbank** steht (`spiegelungen`, Fehlversuche in `versuche`) — das Protokoll ist die ausführliche Fassung, nicht die einzige. |
| `logs/notifications/telegram_bot.log`, `logs/notifications/manuelle_eingriffe.log` | **ausgenommen** | Sie rotieren sich selbst über einen `RotatingFileHandler` (2 MB × 3 bzw. 1 MB × 5) und sind damit bereits nach oben begrenzt. Ein zweiter Rotator würde zwei konkurrierende Namensschemata für dieselbe Datei einführen. Die Zahlen werden nicht doppelt geführt: der Selbsttest liest sie **per AST aus den echten Quelldateien** und vergleicht sie. |

Archive heissen `<name>.log.<Zeitmarke>` statt `.1`, `.2`, `.3`. Damit entfällt das Umbenennen einer ganzen Kette bei jeder Rotation — jedes Umbenennen wäre eine weitere Stelle, an der ein Lauf abbrechen und einen Stand überschreiben kann —, die Sortierung ist lexikalisch wie chronologisch, und der Name endet nicht auf `.log`, wird also nie selbst zum Kandidaten.

**Gegen `newsyslog` entschieden**, das macOS mitbringt: es braucht `sudo` und eine Konfigurationsdatei unter `/etc/newsyslog.d/` — dieselbe Abwägung wie bei `caffeinate` (Abschnitt 4.5), hier mit mehr Gewicht, weil eine Rotation *löscht*. Die Konfiguration läge zudem ausserhalb des Repos, wäre also nicht versioniert und nicht testbar, und für den entscheidenden Fall hat `newsyslog` keine bessere Antwort: sein Standardverfahren ist Umbenennen, und für das Neuöffnen bräuchte es eine PID-Datei und ein Signal, die hier niemand liefert.

Die **Cron-Zeile steht als Vorschlag im README und ist nicht eingetragen** (`30 3 * * *`). Einzelheiten: `system/README_LOG_ROTATION.md`, Testauftrag: `system/TESTAUFTRAG_LOG_ROTATION.md`, Selbsttests: `python3 system/test_log_rotation.py`.

---

## 5. Datei-Inventar pro Strategie (Kernskripte)

Gemeinsames Muster in den `strategies/<name>/`-Ordnern (Dateinamen variieren zwischen den Strategie-Familien; wo eine Datei **nicht** bei allen neun Bots liegt, steht das in der Zeile):

| Datei | Zweck |
|---|---|
| `zigzag_indicator.py` / `indicators.py` | Kern-Indikator-Berechnung (Zigzag bzw. T3/ADX/SuperTrend bzw. RSI/Donchian/Bollinger) |
| `elliott_wave_counter.py` | (nur Elliott-Wave-Varianten) Wellenzählung + Fibonacci-Score + Überlappungsbereinigung |
| `backtest_elliott.py` / `backtest_trend.py` | Einzelsymbol-Backtest-Engine |
| `optimise_elliott.py` / `optimise_trend.py` | Einzelsymbol-Parameter-Grid-Search (Demo/Diagnose, nicht die Haupt-Optimierung) |
| `multi_symbol_optimise.py` | **Haupt-Optimierungsskript**: lädt alle Symbole, Grid-Search über Parameterraum, robuste Kombination finden |
| `multi_symbol_walk_forward.py` | Teilt Daten 70/30 (In-Sample/Out-of-Sample), validiert Optimierungsergebnis auf ungesehenen Daten |
| `equity_simulation.py` | Event-basierte Portfolio-Simulation (echtes Kapital, Positionsgröße, ggf. Positionslimit) statt naiver Summierung |
| `oos_equity_simulation.py` | Equity-Simulation beschränkt auf den Out-of-Sample-Zeitraum, mit den auf dem In-Sample-Fenster optimierten Parametern (nicht mit den Live-Werten — das ist der Sinn der Prüfung). Vorhanden bei `elliott_wave` **und** `elliott_wave_stocks`; die frühere Angabe „nur Krypto-Varianten" war falsch und hat mit dazu beigetragen, dass ein Fehler in der Aktien-Fassung lange unbemerkt blieb (PR #45/#47) |
| `forward_test.py` | **Live-Skript**: prüft offene Positionen, sucht neue Signale, schreibt in DB — das läuft per Cron |
| `daily_summary_email.py` | Liest DB, baut Zusammenfassung, ruft Agent 1 + Agent 3 auf, verschickt den Bericht — **alle neun Cronjobs seit 2026-09-08 deaktiviert** (PR #36). Die reinen Zahlen sind jederzeit über `/status`, `/positions`, `/pnl` und das Dashboard abrufbar; der Mehrwert einer zusätzlichen täglichen KI-Einordnung stand dem laufenden API-Verbrauch nicht klar gegenüber. Deaktiviert wurde **nur die Auslösung**: die Cron-Zeilen auf dem Mac sind auskommentiert, nicht gelöscht, und die Skripte bleiben manuell lauffähig. Der Name „…_email" ist historisch — die Berichte laufen seit PR #16 über Telegram |
| `live_params.py` | Aktuell aktive, validierte Parameter (siehe Abschnitt 4) |
| `agent_optimise.py` | Nutzt Agent 2 (`param_search_agent.py`) als Alternative zum vollen Grid-Search. **Nur bei den drei ursprünglichen Bots** (`elliott_wave`, `elliott_wave_stocks`, `t3_supertrend`) — die sechs Prototypen haben ihn nicht |
| `quarterly_review.py` | Vierteljährlicher automatisierter Review-Prozess (siehe Abschnitt 6.4). **Ebenfalls nur bei den drei ursprünglichen Bots.** Die frühere Darstellung als Teil des gemeinsamen Musters aller neun war falsch; sie betrifft auch Abschnitt 9, Punkt 2 — für sechs der neun Strategien kann es gar keinen Quartals-Cronjob geben |

**Strategie-spezifische Zusatzdateien:**
- `t3_supertrend/`: `fetch_4h_data.py`, `regime_filter.py`
- `elliott_wave_stocks/`: `get_top_stocks.py`, `stocks_symbols_config.py`, `fetch_stock_data.py`, `buy_and_hold_benchmark.py`, `signal_quality_test.py`
- die sechs Prototyp-Bots: je ein `PROTOTYPE_FINDINGS.md` unter `results/<bot>/` mit der vollständigen Validierungskette und den verworfenen Varianten
- `volatility_breakout_crypto/`: BTC-Regimefilter, seit PR #57 **strukturell** in `equity_simulation.py` eingebaut (davor nur in einer Studie nachgebildet)

**`research/` — abgeschlossene Untersuchungen.** Ein eigener Ordner je Frage, jeweils mit `BERICHT.md` und eigenen Skripten. Verbindliche Regel: **Untersuchungen fassen keinen Bot-Code an.** Jeder Bericht belegt das per `git status`/`git diff`. Die für spätere Entscheidungen wichtigsten sind `elliott_wave_lookahead/` (der Look-Ahead-Fund), `elliott_wave_params/` (die Parameter-Neubestimmung darauf) und `sync_check/` (Backtest-vs-Live-Gleichstand).

---

## 6. Claude-Agenten (KI-Zusatzfunktionen)

**Wichtiges Grundprinzip für alle Agenten:** Rein informativ/unterstützend. **Kein Agent verändert automatisch Handelsparameter oder platziert Trades.** Diese Trennung war eine explizite, bewusste Design-Entscheidung (siehe Abschnitt 8).

Es sind inzwischen **vier nummerierte Agenten** plus der Quartals-Interpreter. Agent 4 (wöchentliche Portfolio-Einordnung) fehlte in diesem Dokument bis 2026-09-09.

**Hervorhebung von Handlungsempfehlungen (PR #34).** Mehrere Agenten erzeugen Freitext, der de facto Handlungsempfehlungen enthält („eine Überprüfung der Parametrisierung sollte in Betracht gezogen werden") — bis dahin stand das undifferenziert im Fliesstext, also genau dort, wo es überlesen wird. `shared/empfehlung_format.py` ist seither die **einzige** Stelle, an der die Hervorhebung definiert wird; alle 13 Versandstellen bauen ihre Blöcke über die Funktionen dort.

### 6.1 Agent 1 — Tägliche Einordnung (`daily_interpreter.py`)
- Modell: **Haiku 4.5** (günstig, für einfache Zusammenfassung ausreichend)
- Läuft: automatisch bei jedem `daily_summary_email.py`-Aufruf — **seit 2026-09-08 nicht mehr automatisch**, da dessen Cronjob deaktiviert wurde (nur noch bei manuellem Aufruf)
- Funktion: `generate_interpretation(strategy_name, summary_text)` → 2-4 Sätze sachliche Einordnung der Tageszahlen
- Kosten: ~0,001-0,002 $/Aufruf, geschätzt unter 0,20 €/Monat gesamt
- Kein Handlungsbedarf für den Nutzer — reine Lese-Information in der E-Mail

### 6.2 Agent 2 — Intelligente Parameter-Suche (`param_search_agent.py`)
- Modell: **Sonnet 5**
- Läuft: **nicht automatisch** — nur bei manuellem Aufruf von `agent_optimise.py`, oder eingebettet in `quarterly_review.py`
- Funktion: `run_agent_search(evaluate_fn, param_spec, seed_combos, max_iterations)` — iterativer Prozess: Claude sieht bisherige Testergebnisse (als kompakte Tabelle), schlägt nächste vielversprechende Kombination vor (JSON: `{"action": "test"|"stop", "params": {...}, "reasoning": "..."}`), Ergebnis wird evaluiert, wiederholt bis `max_iterations` oder `action: "stop"`
- **Bug gefunden und behoben**: `max_tokens` zu niedrig (erst 500, dann 800) führte zu abgeschnittenen JSON-Antworten bei ausführlichen Begründungen → `max_tokens=1000` UND System-Prompt-Anweisung "reasoning maximal 15 Wörter" behoben das zuverlässig
- Kosten: ~0,10-0,40 €/vollständigem Lauf (10-15 Iterationen)
- **Ergebnisse sind NIEMALS direkt vertrauenswürdig** — müssen immer zusätzlich per Walk-Forward validiert werden, bevor Übernahme in `live_params.py` erwogen wird (das reine In-Sample-Ergebnis des Agenten ist genauso overfitting-anfällig wie Grid-Search-Ergebnisse)

### 6.3 Agent 3 — Marktkontext (`market_context_agent.py`)
- Modell: **Sonnet 5** + `web_search_20250305`-Tool (server-seitige Websuche über die Anthropic-API)
- Läuft: automatisch bei `daily_summary_email.py`, **aber nur wenn der jeweilige Bot offene Positionen hat** (sonst übersprungen, keine Kosten) — **seit 2026-09-08 nicht mehr automatisch**, da dessen Cronjob deaktiviert wurde; dieser Agent war der teurere der beiden täglichen Aufrufe
- Funktion: `get_market_context(symbols, context_label)` → 3-5 Sätze zu aktuellen Nachrichten/Ereignissen zu den Symbolen mit offenen Positionen
- Kosten: ~0,02-0,03 $ pro Auslösung (inkl. Websuch-Gebühr), 0 € an Tagen ohne offene Positionen
- **Bewusst rein informativ** — blockiert oder löst niemals Trades aus (explizite Design-Entscheidung, da eine validierte "News-Veto"-Logik ein eigenständiges, noch nicht getestetes Feature wäre)

### 6.3b Agent 4 — Wöchentliche Portfolio-Einordnung (`portfolio_interpreter_agent.py`)
- Modell: **Sonnet 5**
- Läuft: wöchentlich über `shared/weekly_portfolio_email.py`
- Funktion: nimmt die Textausgabe von `shared/portfolio_overview.py` (Live-Portfolio-Kurve, Kurve inkl. Prototypen, Einzel-Bot-Drawdowns, Korrelationswerte je Bot-Paar samt „zu wenig Datenbasis"-Fällen) und ordnet sie ein: Läuft die Diversifikation wie im Backtest erwartet? Gibt es auffällige Verschiebungen? Werden Korrelationsschwellen bald erreicht?
- Wichtig: `weekly_portfolio_email.py` **dupliziert die Analyse nicht**, sondern ruft `portfolio_overview.main()` auf und fängt deren Ausgabe ab — eine zweite Rechenlogik wäre genau die Doppelführung, die dieses Projekt an anderer Stelle schon Geld an Aussagekraft gekostet hat
- Wie alle anderen: **rein informativ**, ändert nie `live_params.py`, Cronjobs oder irgendetwas anderes

### 6.4 Quartals-Review-System (`quarterly_review.py` + `quarterly_interpreter.py`)
Automatisierter, aber bewusst **nicht selbst-ändernder** Prozess, der auf ausdrücklichen Wunsch des Nutzers entstand (er wollte ursprünglich monatliche Vollautomatisierung inkl. automatischer Parameter-Übernahme — davon wurde abgeraten, siehe Abschnitt 8).

Ablauf bei jedem Lauf:
1. Validiert die **aktuellen** Live-Parameter per Walk-Forward (In-Sample + Out-of-Sample)
2. Lässt **Agent 2** eine neue Kombination vorschlagen
3. Validiert den **Vorschlag** genauso streng per Walk-Forward (fairer Vergleich, gleiche Methodik)
4. Liest die **echten** Forward-Test-Ergebnisse aus der Live-Datenbank (unabhängige Realitäts-Prüfung — diese Trades sind bereits geschehen, können nicht überoptimiert sein)
5. Ruft **`quarterly_interpreter.generate_recommendation()`** auf: Sonnet-5-Agent mit expliziter Regel "Out-of-Sample zählt weit mehr als In-Sample", erkennt und benennt Overfitting-Muster, gibt klare Empfehlung (Parameter behalten / Wechsel erwägen / zu wenig Daten)
6. Verschickt vollständigen Bericht per Mail
7. **Ändert NIEMALS automatisch `live_params.py`** — Übernahme bleibt manueller Schritt

**Intervall-Entscheidung:** Vierteljährlich (Jan/Apr/Jul/Okt, jeweils am 1., 9 Uhr), **nicht monatlich** — bewusste Empfehlung, da (a) Forward-Test braucht Zeit für aussagekräftige echte Trade-Daten, (b) monatliches Nachjustieren würde eher Rauschen als echten Fortschritt verfolgen, (c) Kosten-Nutzen.

**Erster echter Testlauf** (T3/SuperTrend-Bot, manuell ausgeführt): Bestätigte den Sinn des Systems eindrücklich — Agent-2-Vorschlag sah In-Sample überlegen aus, brach aber Out-of-Sample ein (klassisches Overfitting). Aktuelle Parameter korrekt beibehalten.

**Cron-Zeile (Muster, pro Strategie mit angepasstem Pfad):**
```
0 9 1 1,4,7,10 * <python-pfad> <strategie-pfad>/quarterly_review.py >> <log-pfad> 2>&1
```
**⚠️ UNKLAR / vom Nutzer zu verifizieren:** Es wurde die Anleitung gegeben, diese Cron-Zeile je Strategie einzutragen. Bestätigt ist nur der **manuelle Testlauf** für `t3_supertrend` — **nicht bestätigt**, für welche Strategien die Cron-Zeilen tatsächlich eingetragen sind. Mit `crontab -l` prüfen.

*Eingrenzung vom 2026-09-11:* `quarterly_review.py` existiert überhaupt nur bei **drei** Bots — `elliott_wave`, `elliott_wave_stocks` und `t3_supertrend`. Die sechs später hinzugekommenen Prototypen haben die Datei nicht, für sie kann es also gar keinen Quartals-Cronjob geben. Der frühere Satz, die Frage sei „mit sechs weiteren Bots grösser geworden", war damit falsch: sie ist kleiner, als sie aussah. Ob das Quartals-Review auf die sechs Prototypen ausgeweitet werden soll, ist eine **offene Entscheidung des Nutzers** und keine vergessene Einrichtung.

### 6.5 API-Key-Verwaltung
`claude_client.py`s `get_client()`-Funktion sucht den Key in dieser Reihenfolge:
1. Umgebungsvariable `ANTHROPIC_API_KEY`
2. Fallback: `ANTHROPIC_API_KEY`-Variable in `config/email_config.py` (löst `CONFIG_DIR` **selbstständig** relativ zum eigenen Skript-Pfad auf — wichtig, da nicht jedes aufrufende Skript den `config`-Pfad kennt, siehe Bug-Historie unten)

**Bug-Historie:** Ursprüngliche Version verließ sich darauf, dass der Aufrufer bereits `CONFIG_DIR` zu `sys.path` hinzugefügt hat (funktionierte zufällig bei `daily_summary_email.py`, **nicht** bei `agent_optimise.py`, das nie mit `email_config` in Berührung kommt) → behoben, `claude_client.py` löst den Pfad jetzt selbst relativ zu seinem eigenen Ordner (`shared/`) auf.

**⚠️ SICHERHEITSVORFALL (wichtig für neuen Chat):** Der Nutzer hat im bisherigen Gespräch **zweimal versehentlich einen echten Anthropic-API-Key im Klartext im Chat gepostet** (einmal direkt beim Einfügen einer Zeile, einmal via `cat email_config.py`, was auch das E-Mail-Passwort offenlegte). Beide Male wurde empfohlen, den Key umgehend zu widerrufen und neu zu erstellen. Der aktuell genutzte Key ist der **dritte, regenerierte** (108 Zeichen lang). **Für den neuen Chat:** Falls der Nutzer wieder Dateiinhalte mit Zugangsdaten zeigen will, empfehle `grep -c "SCHLÜSSELNAME" datei` statt `cat datei`, um Preisgabe zu vermeiden.

---

## 7. Methodik — etablierte Arbeitsweise (wichtig für Konsistenz)

Diese Prinzipien haben sich über die gesamte Entwicklung etabliert und sollten in der Fortsetzung beibehalten werden:

1. **In-Sample vs. Out-of-Sample strikt trennen.** Nur Out-of-Sample-Ergebnisse zählen für Entscheidungen. Diese Regel wurde mehrfach explizit verletzt-und-korrigiert im Verlauf (z.B. beim ersten T3-Test, beim ersten Aktien-Test) — daher jetzt in Prompts und Code-Kommentaren wiederholt verankert.

2. **Naive Summierung von Trade-Prozenten ≠ echtes Kapitalwachstum.** Mehrfach als Fehlerquelle aufgetreten (z.B. "657% Rendite", die sich als bedeutungslos herausstellte). Immer die event-basierte `equity_simulation.py` (mit Positionsgröße + Zinseszins-Effekt) für belastbare Zahlen nutzen.

3. **Survivorship Bias bei Aktien ist real und nicht vollständig lösbar** mit kostenlosen Datenquellen (heutige Indexmitglieder werden rückwirkend getestet). Mitigation: Buy-and-Hold-Vergleich als Pflicht-Gegencheck, begrenztes Rückblick-Fenster (`RECENT_YEARS_ONLY`).

4. **Signal-Qualitäts-Test** (Strategie-Trades vs. passives Halten während derselben Fenster) ist ein wertvolles Diagnose-Werkzeug, um "bringt das Timing etwas" von "bringt das Kapitalmanagement etwas" zu trennen. Wiederkehrender Befund: Exit-Feinjustierung bringt selten viel, Entry-Timing + Positionsgrößen-Disziplin schon.

5. **Korreliertes Klumpenrisiko** bei mehreren ähnlichen Assets ist ein reales, wiederkehrendes Problem — gelöst über `MAX_CONCURRENT_POSITIONS` (empirisch getestet für Krypto: 3/5/8/unbegrenzt) und ggf. Markt-Regime-Filter.

6. **Universumsgröße korreliert mit statistischer Robustheit.** Bei jeder Erweiterung (Krypto 5→18→25, Aktien 25→50→100→150) mussten `MIN_TRADES`/`MIN_SYMBOLS_CONTRIBUTING`-Schwellen proportional mit angehoben werden.

7. **Parameter-Instabilität** (die "beste" Kombination ändert sich zwischen Optimierungsläufen deutlich) ist ein wiederkehrendes, erwartbares Muster bei diesen Datenmengen — wird als echtes Overfitting-Warnsignal behandelt, nicht ignoriert.

8. **Zeitraum-basierte statt kerzenzahl-basierte Mindest-Historie-Filter** (`MIN_HISTORY_DAYS` statt Kerzen-Zählung), da unterschiedliche Zeitrahmen unterschiedliche Kerzendichte pro Kalendertag haben (Lehre aus der Krypto→Aktien-Übertragung).

9. **Jede neue Idee wird empirisch zu Ende getestet, auch wenn ein Zwischenergebnis enttäuschend oder verlockend aussieht** (Beispiele: VWAP-Filter beim T3-Bot erst vielversprechend, dann verworfen nach vollständigem Test; "kein Take-Profit"-Idee beim Aktien-Bot erst als offener Punkt markiert statt vorschnell übernommen — und später sauber nachgeholt).

10. **Kausalität im Backtest ist keine Selbstverständlichkeit, sondern muss geprüft werden.** Der Look-Ahead im Zigzag (Abschnitt 3.1) lag zwei Jahre unbemerkt im Code und hat die Parameterwahl beider Elliott-Bots verdorben. Eine Kennzahl, die zu gut aussieht, ist ein Anlass zur Prüfung, nicht zur Freude. Prüfbar ist das mechanisch: für jeden Trade belegen, dass der Einstiegszeitpunkt **nach** dem Zeitpunkt liegt, zu dem das Signal überhaupt bekannt sein konnte.

11. **Ein Wert, eine Quelle.** Jeder Handelsparameter steht genau einmal — in `live_params.py` — und wird überall sonst importiert. Doppelt geführte Zahlen laufen früher oder später auseinander, ohne dass es jemandem auffällt; genau das war bei fünf von neun Bots passiert (Abschnitt 4.2).

12. **Eine grüne Prüfung ist erst dann etwas wert, wenn belegt ist, dass sie auch rot werden kann.** Wiederholt sind in diesem Projekt Prüfungen aufgefallen, die etwas anderes gemessen haben als gemeint: abgestürzte Läufe als „identisch" gewertet (beide Ausgaben leer), ein `<fehlt>` gegen ein `<fehlt>` verglichen, ein Kommentar statt des Codes durchsucht, eine fehlende Test-Attrappe als positives Signal gelesen. Gegenmittel: **Gegenprobe** — die Schutzmassnahme gezielt entfernen und prüfen, ob der Test anschlägt.

13. **Aktien- und Krypto-Fassungen derselben Strategie brauchen eigene Antworten.** Bei Stop-Wahl und Kapitalmanagement fielen die Entscheidungen zwischen `turtle_soup_stocks` und `turtle_soup_crypto` entgegengesetzt aus (Abschnitt 3.4). Eine Krypto-Fassung ist nie eine blosse Parameter-Kopie.

14. **Untersuchungen fassen keinen Bot-Code an.** Alles unter `research/` ist les- und rechnend, nie ändernd; jeder Bericht belegt das per `git status`/`git diff`. Parameterübernahme ist immer ein getrennter, ausdrücklich freigegebener Schritt.

---

## 8. Wichtige Entscheidungen (mit Begründung)

| Entscheidung | Begründung |
|---|---|
| Kein Live-Trading-Code bisher | Nutzer wollte das explizit auf später verschieben, nachdem die konzeptionellen Anforderungen (API-Keys ohne Auszahlungsrecht, Notausschalter, Tagesverlust-Limit, Monitoring, kleines Startkapital) besprochen wurden |
| Vollautomatische Agent-2-Übernahme abgelehnt | Nutzer wollte ursprünglich monatliche Vollautomatisierung inkl. automatischer Parameter-Übernahme; nach Diskussion der Risiken (Parameter-Instabilität, fehlender menschlicher Kontrollpunkt) auf "Vorschlag per Mail, manuelle Freigabe nötig" geeinigt |
| Vierteljährlich statt monatlich für Quartals-Review | Siehe Abschnitt 6.4 — mehr Zeit für aussagekräftige echte Forward-Test-Daten zwischen Reviews |
| Alle-503-Aktien-Universum abgelehnt, Top 150 gewählt | Löst Survivorship-Bias nicht zusätzlich, hoher Rechenaufwand, yfinance-Zuverlässigkeit bei dieser Größe fraglich — moderate Erweiterung nimmt den Großteil des Nutzens mit |
| 4-Stunden- statt 15-Minuten-Chart für T3-Bot | 15-Minuten technisch/praktisch nicht sinnvoll umsetzbar mit Cronjob-Infrastruktur (siehe Abschnitt 3.2) |
| `live_params.py` als separate Datei pro Strategie | Risikoarme, übersichtliche Parameter-Übernahme nach Validierung, ohne tief in Code eingreifen zu müssen |
| VWAP-Filter deaktiviert (Code bleibt) | Volle Equity-Simulation zeigte Netto-Nachteil trotz vielversprechendem Teiltest — Infrastruktur bleibt für künftige Experimente erhalten |
| Elliott-Krypto-Parameter nach der Look-Ahead-Korrektur getauscht (4/2/0,236 → 10/6/0,618) | Die alte Kombination bestand auf sauberer Grundlage **keine einzige** der fünf Mindestbedingungen; der 2-%-Stop löste bei 72,6 % der Trades vorzeitig aus (Abschnitt 3.1) |
| Elliott-Aktien-Parameter trotz enttäuschender Zahlen **nicht** getauscht | Keine der 252 geprüften Alternativen ist belegbar besser; der beste Kandidat verliert im Walk-Forward in zwei von drei Falten gegen Buy-and-Hold. Ein Wechsel ohne Vorteil wäre reine Bewegung (Abschnitt 3.3) |
| Tägliche Bot-E-Mails abgeschaltet (PR #36) | Die Zahlen sind über Telegram und Dashboard jederzeit abrufbar; eine zusätzliche tägliche KI-Einordnung rechtfertigte den laufenden API-Verbrauch nicht. Nur die Cron-Auslösung ist auskommentiert, die Skripte bleiben lauffähig |
| Berichte von E-Mail auf Telegram umgestellt (PR #16) | Push statt Postfach; die Bot-Berichte kamen vorher nur per Mail und wurden entsprechend spät gelesen |
| Bots bleiben dauerhaft getrennt, **kein** gemeinsames Kapitalkonto | Ein zentrales Konto bräuchte Locking und ein Vergütungssystem in `shared/` — hoher Aufwand, hohes Risiko. Stattdessen `portfolio_overview.py` als reine **Beobachtungsrechnung** mit hypothetischer Gewichtung, die keine einzige Zeile in einem Bot-Ordner anfasst |
| Beide Beobachtungsebenen (Telegram, Dashboard) lesen über dieselbe `monitor.py` | Zwei Leseimplementierungen würden früher oder später unterschiedliche Zahlen zeigen — dieselbe Begründung wie beim `live_params.py`-Muster |
| Manuelles Schliessen über das **Dashboard** gemergt (PR #62), über **Telegram nicht** (PR #61 ohne Merge geschlossen) | Zwei Wege für denselben Schreibzugriff wären zwei Stellen, an denen die Absicherung auseinanderlaufen kann. Der Dashboard-Weg zeigt Kurs und PnL vor der Bestätigung im Zusammenhang; der Telegram-Weg hätte dieselbe Kernfunktion über eine zweite Oberfläche angesprochen. Die Kernfunktion `manual_close.py` stammt aus PR #61 und wird weiterverwendet — abgelöst wurde nur die Bedienoberfläche |
| Freigeschaltet sind **alle neun Bots**, nicht nur `t3_supertrend` | Der erste Bot war ein bewusster Anfang mit dem einfachsten Schema. Die Erweiterung ist ein Eintrag in `SCHLIESSBARE_BOTS` und braucht keine Codeänderung; jeder Bot wurde einzeln gegen sein `forward_test.py` geprüft, und die Prüfung läuft bei jedem Testlauf erneut |
| **Zeitversetzte Ausführung ohne erneute Bestätigung** eingeführt (Warteaufträge, PR #69/#71) | Der Schliessen-Knopf der Aktien-Bots schloss ausserhalb der Börsenzeiten zu einem Tages-Schlusskurs, den es „gerade jetzt" gar nicht gibt — über ein Wochenende zweieinhalb Tage alt. Die Alternative wäre gewesen, den Knopf dort ganz zu sperren; dann hätte der Nutzer im Ernstfall bis zur Eröffnung gar keine Handhabe. Gewählt wurde der Warteauftrag: zu einem **echten** Kurs schliessen statt zu einem veralteten. **Der Preis ist eine Vorab-Erlaubnis** — wer den Cronjob einrichtet, erlaubt alle künftigen Warteaufträge, nicht einen einzelnen, und eine Eröffnungslücke am Montag trifft den Auftrag voll. Das ist der erste Schreibvorgang des Projekts ohne gleichzeitige menschliche Bestätigung und die folgenreichste Einzelentscheidung seit dem Dashboard |
| Bei unbekanntem Börsenstatus **weder schliessen noch vormerken** | Ein Warteauftrag ohne funktionierenden Kalender wäre eine Absicht, die niemand einlösen kann — das Ausführungsskript hängt am selben Kalender. Bewusst **keine Faustregel als Rückfallebene**: eine Näherung, die nur greift, wenn die genaue Antwort fehlt, schlüge genau dann zu, wenn niemand hinsieht |
| Zwei Broker-Brücken gebaut, beide nur gegen **Testnet bzw. Paper-Konto** (PR #68, #70) | Der erste Schreibzugriff auf eine Börse sollte nicht zugleich der erste mit echtem Geld sein. Endpunkt als Literal im Code, echte Handelsendpunkte und Live-Ports namentlich auf Verbotslisten, Trockenlauf als Standard, Grenzen je Lauf und je Tag im Code statt in der `.env` |
| **Notbremse auf drei Ebenen**, Rückgabewert **0** ohne offene Aufgabe (PR #73) | Vorher wurde nur je Aufgabe geprüft. Lag keine Aufgabe an, kam die Prüfung nie dran: keine Zeile, Rückgabewert 0 — ein gebremster Lauf war von einem gewöhnlichen Leerlauf nicht zu unterscheiden, was bereits zu der falschen Meldung geführt hatte, die Bremse greife nicht. **Zum Rückgabewert:** eine gezogene Bremse ist eine befolgte Anweisung des Nutzers, kein Fehlschlag; ohne offene Aufgabe ist nichts liegengeblieben, deshalb **0**. Eine Fehlermail bei jedem Lauf — beim 4-Stunden-Takt sechs am Tag, tagelang — würde genau die Mails entwerten, auf die es ankommt. **Mit** offener Aufgabe bleibt es bei **1**: da wurde tatsächlich etwas nicht ausgeführt. Dass die Bremse wirkt, steht sichtbar im Protokoll, nicht im Rückgabewert |
| Im Crash-Dialog wird die **Positionsanzahl je Bot** ausgewiesen (PR #73) | Die gewichtete Gesamt-Zahl rechnet korrekt, sagt aber nicht, woraus sie besteht. `elliott_wave` hat als einziger Bot kein `MAX_CONCURRENT_POSITIONS` und kann sie praktisch allein tragen — rechnerisch richtig, faktisch die Aussage *eines* Bots, und zwar genau in dem Moment, in dem eine Notfallentscheidung fällt. Ausgewiesen, nicht neu berechnet: die Zahlen fielen bei der Gewichtung ohnehin an |
| `caffeinate` als **launchd-Dienst** statt als Terminalbefehl (PR #72) | Ein von Hand gestartetes `caffeinate` hängt am Terminalfenster und überlebt weder Neustart noch macOS-Update — beim Update vom 11.09.2026 war es ersatzlos weg, und der Mac verschlief drei Stunden Cronjobs. Cron holt verpasste Läufe **nicht** nach; fehlende Läufe verfälschen die Paper-Trading-Auswertung still (Abschnitt 4.5) |

---

## 9. Offene Punkte / nächste sinnvolle Schritte

1. **`MAX_CONCURRENT_POSITIONS = 8` beim Elliott-Aktien-Bot nicht empirisch getestet** (im Gegensatz zum T3-Bot, wo 3/5/8/unbegrenzt systematisch verglichen wurden). Der Wert wirkt inzwischen nachweislich — 14 von 128 OOS-Trades sind davon betroffen (PR #48) —, aber ob **8** die richtige Zahl ist, wurde nie geprüft. Sollte nachgeholt werden.

2. **Quartals-Review-Cronjobs**: Anleitung wurde gegeben, aber **nicht bestätigt**, für welche Strategien sie tatsächlich eingetragen sind (nur `t3_supertrend` wurde manuell getestet). Mit `crontab -l` verifizieren. *Eingrenzung vom 2026-09-11:* `quarterly_review.py` existiert überhaupt nur bei **drei** Bots (`elliott_wave`, `elliott_wave_stocks`, `t3_supertrend`) — die Frage betrifft also drei mögliche Einträge, nicht neun.

3. **Live-Trading mit echtem Kapital**: rein konzeptionell besprochen, keine Code-Umsetzung. Bei Bedarf: API-Keys mit Handelsrechten (ohne Auszahlungsrecht), Notausschalter/Kill-Switch, Tagesverlust-Limit, Monitoring/Alarmierung, sehr kleines Startkapital für die ersten Wochen.

4. **Der Elliott-Aktien-Bot schlägt Buy-and-Hold nicht.** Auf kausal sauberer Grundlage liegt er über den Gesamtzeitraum in Rendite **und** Calmar hinter passivem Halten (Abschnitt 3.3), und keine der 252 geprüften Parameterkombinationen ändert das. Das ist keine Aufgabe mit bekannter Lösung, sondern eine offene strategische Frage: Bot weiterlaufen lassen und beobachten, Strategie überarbeiten, oder abschalten? **Bewusst noch nicht entschieden.**

5. **Der Elliott-Krypto-Bot steht auf dünner Datenbasis.** 130 Trades in fünf Jahren, davon 31 out-of-sample. Der Vorsprung über den Gesamtzeitraum ist deutlich, im Out-of-Sample-Fenster nur noch knapp und allein risikoadjustiert. Braucht schlicht mehr Forward-Test-Zeit, bevor sich mehr sagen lässt.

6. **Die 2022-Bärenmarkt-Schwäche von `volatility_breakout` (Aktien)** ist identifiziert, dokumentiert und **nicht behoben** — das angepasste Kapitalmanagement mildert sie nicht. Gilt als bekanntes, akzeptiertes Risiko dieses Bots.

7. **Manuelles Schliessen einer Position — inzwischen AKTIV.** *Dieser Punkt stand bis 2026-09-11 falsch hier*: er beschrieb die Funktion als „gebaut, aber nicht gemergt" und Dashboard wie Telegram als rein lesend. Tatsächlich ist **PR #62 gemergt** und die Funktion im Dashboard für **alle neun Bots** in Betrieb (Abschnitt 4.3). **PR #61** (Telegram-Befehl `/schliessen`) wurde am 2026-09-10 **ohne Merge geschlossen**; der Telegram-Bot bleibt rein lesend. Offen ist hier nur noch: der Cronjob-Status der Warteaufträge (Punkt 10) und die iOS-Safari-Prüfung (Punkt 8).

8. **Der Schliess-Dialog wurde nie in echtem iOS-Safari geprüft.** Der Bestätigungsdialog (PR #62) benutzt das native `<dialog>`-Element und wurde in Chromium im iPhone-Format (390 px) vollständig durchgespielt — aber nicht in Safari auf dem Gerät selbst. `<dialog>` setzt dort iOS 15.4+ voraus; das ist praktisch überall vorhanden, doch bei einer schreibenden Funktion sollte „praktisch" nicht genügen. Beim nächsten Aufruf des Dashboards auf dem iPhone gezielt prüfen: öffnet sich der Dialog überhaupt, liegt der Fokus darin, verwirft die Zurück-Geste den Vorgang (der `cancel`-Handler sollte greifen), und lässt sich `BESTAETIGEN` auf der iOS-Tastatur eingeben (Autokorrektur und automatische Grossschreibung sind im Feld abgeschaltet, `font-size: 16px` verhindert das Hineinzoomen). Falls `<dialog>` dort nicht trägt, wäre der Rückfallweg ein einfaches Overlay — dann müssten Fokusfang und Esc-Taste allerdings von Hand nachgebaut werden, was genau der Grund war, `<dialog>` zu nehmen. **Seit PR #71 und #73 gilt dasselbe für die Warteauftrags-Dialoge und die Positionsanzahl-Zeile im Crash-Dialog** — auch sie sind nur über die erzeugte Ausgabe geprüft, nie am Gerät.

9. **Versandzeiten**: die früher hier notierte Überschneidung der beiden Krypto-Bot-E-Mails um 8:05 Uhr ist gegenstandslos, seit die täglichen Mails abgeschaltet sind (PR #36). Nur zur Kenntnis, falls die Cron-Zeilen je wieder aktiviert werden.

10. **Der Cronjob der Warteaufträge ist nicht bestätigt** — analog zu Punkt 2. `dashboard/warteauftraege_ausfuehren.py` ist das einzige Programm, das zeitversetzt und ohne erneute Rückfrage schreibt; der Eintrag dafür (`*/5 * * * *`, Testanleitung Schritt 17) muss der Nutzer selbst setzen. **Ohne ihn passiert nichts**: Warteaufträge werden angelegt, im Dashboard angezeigt und nie ausgeführt — ein bewusst möglicher Zwischenschritt. Mit `crontab -l | grep warteauftraege` verifizieren. Ist er gesetzt, gilt die Vorab-Erlaubnis aus Abschnitt 8.

11. **Die IBKR-Brücke ist nie gegen eine echte TWS gelaufen** und auf dem Rechner des Nutzers derzeit **nicht lauffähig**: `ib_async` verlangt Python 3.10+, das `trading-env` steht auf 3.9.6 (Abschnitt 4.4). Vor einer Inbetriebnahme ist also zweierlei nötig — eine Python-Version ab 3.10 und ein Durchlauf der gestaffelten Anleitung in `broker/README_IBKR.md` mit laufender TWS. Bis dahin ist die Brücke gemergter, geprüfter, aber **unerprobter** Code. Die Binance-Brücke ist davon nicht betroffen und läuft produktiv.

12. **Die Bots protokollieren ihre Läufe nicht mit Zeitstempel.** Nach einem Ausfall ist deshalb nicht belegbar, welche Läufe tatsächlich stattgefunden haben — und genau das braucht man, um einen Eintrag in `docs/DATENLUECKEN.md` zu belegen. Ein einheitliches Lauf-Protokoll (eine Zeile je Start und Ende, mit Zeitstempel) wäre die Voraussetzung dafür. **Nicht umgesetzt, als Aufgabe vorgemerkt.**

    Der Punkt ist beim ersten Registereintrag aufgeschlagen und dort belegt: von den drei ursprünglich offenen Fragen zum 11.09.2026 liessen sich mit `crontab -l` zwei klären (die täglichen Krypto-Bots lagen nachts, also ausserhalb; Bot und Brücke stehen in getrennten Cron-Einträgen), aber die Zahl der ausgefallenen `elliott_wave`-Läufe bleibt „drei bis vier". **Neu hinzugekommen ist dabei eine Frage:** `t3_supertrend` läuft laut `crontab -l` um `0 */4 * * *`, hat also einen Lauf um **12:00** — mitten im Schlaffenster (ca. 08:50–12:06). Ob der stattgefunden hat, ist aus demselben Grund offen. Einzelheiten im Register.

14. **Der Cronjob der Log-Rotation ist nicht eingetragen** — wie Punkt 2 und 10. Die Zeile (`30 3 * * *`) steht als Vorschlag in `system/README_LOG_ROTATION.md`. Unkritisch, weil `system/log_rotation.py` nach **Grösse** entscheidet und kein Intervall braucht: von Hand aufgerufen tut es genau dasselbe. **Erschwerend:** die Crontab des Nutzers liess sich am 12.09.2026 nicht ändern (`crontab -` scheitert mit `Operation not permitted`, macOS-Berechtigung nach einem Update zurückgesetzt) — das betrifft auch die offenen Einträge aus Punkt 2, 10 und den Vorschlag aus PR #78 und sollte zuerst behoben werden.

13. **Die Warteaufträge und die Broker-Brücken sind im Dauerbetrieb ungeprüft.** Beide sind vollständig gegen Attrappen getestet; was keine Attrappe zeigt, ist das Verhalten über Wochen — ein dauerhaft scheiternder Warteauftrag bleibt stehen (Absicht, fällt aber nur auf, wenn man hinsieht), und ein Binance-Testnet-Konto wird periodisch zurückgesetzt, wonach Schlüssel und Bestände neu zu erzeugen sind.

---

## 10. STARTPUNKT FÜR DIE WEITERE ARBEIT

### 1. Wo wir aktuell stehen
**Neun** Bots sind aufgebaut, validiert und laufen automatisiert per Cronjob im Paper-Trading-Modus (Abschnitt 2). **Vier** Claude-Agenten sind produktiv im Einsatz, dazu das Quartals-Review-System. Zwei Beobachtungsebenen laufen: der Telegram-Bot (`/status`, `/positions`, `/pnl` plus Push-Nachrichten bei neuem Trade, Stop-Loss und ausgebliebenem Cronjob-Lauf) und das Web-Dashboard als PWA auf dem iPhone.

**Was sich seit der vorigen Fassung grundlegend geändert hat:** das Dashboard ist **nicht mehr rein lesend**. Es kann Positionen aller neun Bots manuell schliessen und bei geschlossener Börse Warteaufträge anlegen, die ein Cronjob später **ohne erneute Rückfrage** ausführt (Abschnitt 4.3). Dazu senden zwei **Broker-Brücken** Orders an das Binance-Testnet bzw. ein IBKR-Paper-Konto (Abschnitt 4.4) — der erste Schreibzugriff des Projekts auf eine Börse, wenn auch ohne echtes Geld. Der Telegram-Bot bleibt rein lesend.

Backtest- und Live-Konfiguration sind bei allen neun Bots **synchron** (Abschnitt 4.2). Die täglichen Bot-E-Mails sind abgeschaltet (PR #36); die wöchentliche Portfolio-Mail mit Agent 4 läuft weiter.

**Die wichtigste inhaltliche Veränderung** gegenüber früheren Fassungen dieses Dokuments: der Look-Ahead im Elliott-Wave-Backtest ist gefunden und behoben (Abschnitt 3.1). Beide Elliott-Bots stehen damit auf völlig neuen Zahlen. Der Krypto-Bot hat neue Parameter bekommen, der Aktien-Bot schlägt Buy-and-Hold **nicht** mehr. Wer ältere Notizen mit +1458 % oder +113,99 % findet: diese Zahlen sind widerlegt.

### 2. Was zuletzt gemacht wurde
Am 2026-09-08/09 lief eine ungewöhnlich lange Reihe von Änderungen, alle als einzelne Pull Requests gemergt (#26 bis #60). Schwerpunkte:

| Thema | PRs | Ergebnis |
|---|---|---|
| Look-Ahead im Elliott-Backtest | #26, #28, #30 | gefunden, behoben, Krypto-Parameter neu bestimmt und übernommen |
| Sync Backtest ↔ Live bei allen neun Bots | #38–#42, #45, #48, #51, #52, #58, #59 | keine Abweichung mehr; der Prüfer selbst wurde korrigiert |
| Dashboard | #35, #44, #46, #53, #60 | gebaut, Auto-Aktualisierung, Ladeindikator, Zeitzonen-Korrektur, visuelle Überarbeitung |
| Berichte auf Telegram, tägliche Mails aus | #16, #34, #36 | Push statt Postfach; Hervorhebung von Handlungsempfehlungen zentralisiert |
| Datenqualität | #33, #43 | APH-Kurslücke, `shared/data_quality.py` |
| Studien ohne Code-Änderung | #18–#25, #29, #49, #54–#57 | HRP-Portfolio, Trend-Overlay, Order-Sensitivität, VBC-Regimefilter u. a. |

**Am 2026-09-10/11 folgte eine zweite Reihe (#62 bis #73)**, die den Charakter des Projekts verändert hat — vom rein beobachtenden zum teilweise handelnden System:

| Thema | PRs | Ergebnis |
|---|---|---|
| Manuelles Schliessen im Dashboard | #62, #64–#67 | gemergt und aktiv, alle neun Bots; gewichteter Gesamt-PnL im Crash-Dialog |
| Broker-Brücke Binance-Testnet | #68 | produktiv, Cronjob alle 4 h |
| Warteaufträge für Aktien-Positionen | #69, #71 | Börsenkalender, zeitversetzte Ausführung; Cronjob-Status offen (Abschnitt 9, Punkt 10) |
| Broker-Brücke IBKR-Paper | #70 | gemergt, nie gegen echte TWS gelaufen, auf Python 3.9 nicht lauffähig |
| `caffeinate` als launchd-Dienst | #72 | Lehre aus dem Schlaf-Vorfall vom 11.09.2026 (Abschnitt 4.5) |
| Positionsanzahl je Bot + Notbremse zu Beginn | #73 | dreistufige Notbremse, Rückgabewert begründet (Abschnitt 8) |
| Protokoll-Aktualisierung | #63 | die vorige Fassung dieses Dokuments |

**Der SSH-Fernzugriff über Tailscale ist eingerichtet und getestet** — der frühere offene Punkt ist damit erledigt. Zusätzlich ist das Dashboard über den Browser erreichbar, was denselben Zweck für den Alltag besser erfüllt als eine SSH-Sitzung.

**Nicht gemergt:** PR #61 (Telegram-Befehl `/schliessen`), am 2026-09-10 ohne Merge geschlossen. Der Dashboard-Weg hat ihn abgelöst; die Kernfunktion `notifications/manual_close.py` stammt aber aus diesem PR und ist in Betrieb.

### 3. Welche Aufgaben noch offen sind
Alle Punkte aus Abschnitt 9. Keine davon ist blockierend — die Bots laufen.

### 4. Was als Nächstes konkret getan werden sollte
Keine feste Reihenfolge vom Nutzer vorgegeben. Sinnvolle Kandidaten, nach Aufwand sortiert:

1. **`crontab -l` prüfen** (Abschnitt 9, Punkte 2 und 10) — eine Minute, klärt zwei offene Unsicherheiten auf einmal: die Quartals-Reviews und den Warteauftrags-Cronjob. Für den zweiten ist die Antwort besonders wichtig, weil davon abhängt, ob zeitversetzte Schreibvorgänge überhaupt stattfinden.
2. **Den `caffeinate`-Dienst einrichten**, falls noch nicht geschehen (`system/README_CAFFEINATE.md`) — fünf Minuten, und die Lehre aus dem Vorfall vom 11.09.2026 ist gezogen. `pmset -g assertions` zeigt danach, ob er wirkt.
3. **Das Dashboard einmal auf dem iPhone durchspielen** (Abschnitt 9, Punkt 8) — die schreibenden Dialoge sind nie auf dem Gerät geprüft worden, auf dem sie im Ernstfall bedient werden.
4. **Positionslimit des Elliott-Aktien-Bots empirisch prüfen** (Abschnitt 9, Punkt 1) — die Methodik dafür existiert beim T3-Bot bereits.
5. **Entscheiden, ob die IBKR-Brücke in Betrieb gehen soll** (Abschnitt 9, Punkt 11). Braucht zuerst Python 3.10+ im `trading-env` — das ist ein eigener, nicht ganz kleiner Schritt, der alle neun Bots betrifft.
6. **Die strategische Frage zum Elliott-Aktien-Bot beantworten** (Abschnitt 9, Punkt 4). Braucht eine Entscheidung des Nutzers, keine Rechnung.

### 5. Informationen, die für die Fortsetzung unbedingt im Kontext bleiben müssen
- **Nutzer-Kenntnisstand**: Grundlegend terminal-erfahren, aber wiederholt Schwierigkeiten mit: mehrzeiligem Copy-Paste (Zeilen rutschen zusammen), vim-Bedienung (nano wird bevorzugt), Verwechslung von Downloads-Ordnerpfaden (durch viele ZIP-Downloads sind nummerierte Duplikate wie `strategies-2` bis `strategies-12` entstanden — bei Dateiabgleichen IMMER mit `find`/`grep` verifizieren, nicht blind auf `cp`-Erfolg vertrauen)
- **Sprache**: Durchgehend Deutsch, Nutzer sitzt in Donaueschingen, Deutschland
- **E-Mail-Provider**: IONOS/1&1 (`smtp.ionos.de`, Port 587, STARTTLS)
- **Sicherheitsvorfall-Historie**: Zwei versehentliche API-Key-Preisgaben im Chat — bei zukünftigen "zeig mir den Inhalt der Datei"-Situationen mit Zugangsdaten IMMER `grep -c` statt `cat` vorschlagen. Das gilt inzwischen auch für `.env` (Telegram-Token, Dashboard-Token)
- **Alle neun `live_params.py`-Inhalte** exakt wie in Abschnitt 3 dokumentiert — diese sind der aktuelle "Wahrheitsstand" der Live-Konfiguration. Im Zweifel gilt die Datei, nicht dieses Dokument
- **Cronjob-Zeitplan** wie in Abschnitt 6.4 (Quartals-Reviews) und der Bot-Tabelle (Abschnitt 2) dokumentiert
- **Methodik-Prinzipien aus Abschnitt 7** sollten bei jeder neuen Analyse/Optimierung konsequent angewendet werden — das ist der etablierte Qualitätsstandard dieses Projekts. Besonders Punkt 10 (Kausalität) und Punkt 12 (eine grüne Prüfung muss auch rot werden können) sind teuer erlernt
- **Bekannte Datenlücken stehen in `docs/DATENLUECKEN.md`.** Cron holt verpasste Läufe nicht nach; wer Forward-Test-Zahlen auswertet oder mit einem Backtest vergleicht, sieht dort zuerst nach, ob der Zeitraum überhaupt lückenlos gelaufen ist
- **`broker/` sendet echte Orders an echte Gegenstellen.** `--echt` wird **nie** ohne ausdrückliche Zustimmung des Nutzers aufgerufen; der Trockenlauf ist der Standard. Notbremse: `touch broker/STOP` bzw. `broker/STOP_IBKR` (Abschnitt 4.4)
- **Das Dashboard schreibt.** Wer es anfasst, fasst einen Schreibpfad in die Live-Datenbanken an — und mit den Warteaufträgen einen, der zeitversetzt und ohne erneute Rückfrage wirkt (Abschnitt 4.3)
- **Arbeitsweise**: neuer Branch je Aufgabe, eigener Pull Request, **nie selbst mergen**. Untersuchungen unter `research/` fassen keinen Bot-Code an
- Terminal-Befehle immer **einzeln, mit Bestätigung zwischen den Schritten** anbieten, nicht mehrere Befehle auf einmal zum Copy-Paste geben (hat wiederholt zu Fehlern geführt)

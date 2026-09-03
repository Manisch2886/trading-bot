# Trading-Bot-Projekt — Vollständige Übergabedokumentation

**Zweck dieses Dokuments:** Technisches Übergabe-/Gedächtnisdokument für die Fortsetzung der Arbeit in einem neuen Claude-Projekt-Chat. Enthält alle Entscheidungen, Architektur, Code-Struktur, Erkenntnisse und offenen Punkte aus der bisherigen, sehr langen Entwicklungs-Konversation. Wo Informationen unklar oder nicht abschließend bestätigt sind, ist das explizit gekennzeichnet.

---

## 1. Projektziel

Aufbau mehrerer unabhängiger, automatisierter Trading-Bots (aktuell Krypto und Aktien), die:
- auf regelbasierten, backtesteten Strategien laufen (kein Machine-Learning-Modell, sondern klassische technische Analyse: Elliott Wave, T3/ADX/SuperTrend)
- rigoros validiert werden (Backtest → Walk-Forward-Analyse → Equity-Simulation → Buy-and-Hold-Vergleich → Signal-Qualitäts-Test), bevor Parameter als "live" gelten
- aktuell im **Paper-Trading-Modus** (Forward Testing, kein echtes Geld) laufen, vollautomatisiert per Cronjob auf dem Mac des Nutzers
- durch drei Claude-API-Agenten ergänzt werden (tägliche Einordnung, intelligente Parameter-Suche, Marktkontext via Web-Suche), die informativ unterstützen, aber **nie automatisch** Handelsparameter oder Trades verändern

Ursprünglicher Auslöser: Ein Diagramm einer "AI Trading Agent"-Pipeline (Research → Build → Optimise → Forward Test → Risk → Live Trade) mit mehreren Claude-Agenten als Pipeline-Stufen. Die tatsächliche Umsetzung hat sich davon entfernt: Es läuft **kein** Claude-Agent zur Laufzeit der eigentlichen Handelslogik — die Backtest-/Optimierungs-/Signalerkennung ist reiner, deterministischer Python-Code. Claude-Agenten wurden **später gezielt ergänzt** (siehe Abschnitt 6), sind aber vom Kern-Trading-Loop entkoppelt.

**Live-Trading mit echtem Kapital ist explizit noch NICHT umgesetzt** — nur konzeptionell besprochen (siehe Abschnitt 10).

---

## 2. Die drei Bots im Überblick

| Bot | Ordner | Markt | Zeitrahmen | Datenquelle | Cron-Takt |
|---|---|---|---|---|---|
| Elliott Wave (Krypto) | `strategies/elliott_wave/` | 25 Top-Volumen-Kryptos (Binance USDT-Paare) | 1 Stunde | Binance API | stündlich |
| T3/ADX/SuperTrend (Krypto) | `strategies/t3_supertrend/` | dieselben 25 Kryptos | 4 Stunden | Binance API | alle 4h |
| Elliott Wave (Aktien) | `strategies/elliott_wave_stocks/` | Top 150 S&P-500-Werte nach Marktkap. | 1 Tag | yfinance (Yahoo Finance) | werktags 22 Uhr |

Alle drei sind **komplett unabhängig**: eigene Datenbank, eigene Parameter, eigener Cronjob, eigene E-Mail. Sie teilen sich nur gemeinsame Infrastruktur (siehe Abschnitt 4).

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
5. **Backtest** (`backtest_elliott.py`): Einstieg zum Preis am Wellenende, Ausstieg über Stop-Loss, Take-Profit (Fibonacci-Ziel der Gesamtbewegung) oder maximale Haltedauer (`MAX_HOLD_HOURS` = 240 **Balken**, nicht Stunden — Balken-Anzahl über `.head(max_hold_hours)` in `simulate_trade`)

**Wichtiger behobener Bug:** `forward_test.py` nutzte ursprünglich den **historischen** Preis vom Wellenende als Einstiegspreis, obwohl das Signal erst später (bis zu 48h Freshness-Fenster) erkannt wurde. Das ist unrealistisch — behoben, indem stattdessen der **aktuelle** Marktpreis zum Erkennungszeitpunkt verwendet wird. Dafür wurde das Datenbankschema um `signal_time` (Wellenende, für Duplikat-Erkennung) getrennt von `entry_time` (tatsächlicher Ausführungszeitpunkt) erweitert.

**Zusätzlicher Konsistenz-Fix:** Cronjob wurde von täglich auf **stündlich** umgestellt, da der Backtest auf Stundenkerzen-Auflösung läuft — ein täglicher Check hätte die meisten Signale verpasst bzw. mit veraltetem Preis erfasst.

**Validierte Live-Parameter** (`live_params.py`):
```python
DEVIATION_PCT = 4.0
STOP_LOSS_PCT = 2.0
TAKE_PROFIT_FIB = 0.236
```

**Validierungsergebnis:** Out-of-Sample-Rendite (Portfolio-Simulation, 10.000 Startkapital, 10% Positionsgröße, max. 5 gleichzeitige Positionen — Regime-Filter/Positionslimit-Konzept wurde primär beim T3-Bot entwickelt und dort ausführlicher getestet): **+113,99%** über den Out-of-Sample-Zeitraum, Max Drawdown sehr gering (im niedrigen einstelligen Prozentbereich), da Trades selten und weitgehend unabhängig sind.

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
2. Nutzer wies darauf hin, dass Original-Script auf 15-Minuten-Chart lief → 15m-Datenpipeline gebaut (`fetch_15m_data.py`, jetzt vermutlich nicht mehr im finalen Code, siehe unten)
3. 15-Minuten als **unpraktikabel verworfen**: Cronjob müsste alle 15 Min laufen, Handelskosten fressen dünne Margen bei kurzen Haltezeiten auf, Laptop-Abhängigkeit wird kritischer
4. **Entscheidung: 4-Stunden-Chart** — klassischer Zeitrahmen für T3/ADX/SuperTrend als Trendfolge-Indikatoren, passt besser zu Cronjob-Infrastruktur. Datei `fetch_4h_data.py` ersetzte `fetch_15m_data.py` im finalen Code.

**Drawdown-Problem und Lösung:**
- Ohne Schutzmechanismen: Max Drawdown **-39,94%** (naive Positionsgrößen-Simulation ohne Limit) — Ursache: bei breiten Krypto-Markttrends öffnen viele der 25 (korrelierten) Coins gleichzeitig Positionen, die beim Umschwung gemeinsam verlieren
- **`MAX_CONCURRENT_POSITIONS`** eingeführt und empirisch getestet (3 / 5 / 8 / unbegrenzt): **5 war der Sweet Spot** (Rendite 102,7%, Drawdown -31,2% — bei 3 zu wenig Marktteilnahme, bei 8/unbegrenzt kein zusätzlicher Rendite-Nutzen mehr, nur mehr Risiko)
- **BTC-Markt-Regime-Filter** ergänzt (`regime_filter.py`): neue Long-Einstiege werden komplett blockiert, wenn BTC selbst (eigener SuperTrend) im Abwärtstrend ist. Kombiniert mit Positionslimit: Rendite **129,64%**, Max Drawdown **-22,2%** (bestes Ergebnis)
- **VWAP-Filter getestet und wieder verworfen**: isolierter Test auf Out-of-Sample-Teilfenster zeigte Verbesserung (Win Rate 30,6%→35,1%, Ø PnL 0,86%→1,68%), aber volle 5-Jahres-Equity-Simulation mit denselben Parametern zeigte **geringere** Gesamtrendite (129,6%→77,4%) bei fast gleichem Drawdown — VWAP-Filter bringt weniger Trades/Compoundierungsmöglichkeiten, ohne das Risiko zu senken. **Standardmäßig deaktiviert** (`use_vwap_filter=False`), Code bleibt als Option erhalten.

**Validierte Live-Parameter** (`live_params.py`):
```python
T3_FAST_LENGTH = 16
T3_SLOW_LENGTH = 30
ADX_THRESHOLD = 20.0
STOP_LOSS_PCT = 4.0
MAX_CONCURRENT_POSITIONS = 5
```
Regime-Filter: **aktiv**. VWAP-Filter: **deaktiviert**.

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
- **`MAX_CONCURRENT_POSITIONS = 8`** nachgerüstet (fehlte ursprünglich, im Gegensatz zum T3-Bot) — **nicht empirisch wie beim T3-Bot getestet** (3/5/8/unbegrenzt), sondern als plausibler Startwert übernommen. **Offener Punkt**, siehe Abschnitt 9.
- **NaN-Bug gefunden und behoben**: `buy_and_hold_benchmark.py` summierte rohe Schlusskurse; eine einzelne Aktie mit fehlerhaftem/fehlendem yfinance-Kurswert (identifiziert: **APH**, Amphenol) machte die GESAMTE Portfolio-Summe zu `NaN`. Fix: pro Aktie auf `NaN` prüfen, betroffene Aktie überspringen, ihren Kapitalanteil unverändert als "Cash" zur Endsumme addieren (damit Start-/Endkapital vergleichbar bleiben).

**Finales, aktuell bestes validiertes Ergebnis (Top 150, Stand Ende der Konversation):**

Live-Parameter (`live_params.py`):
```python
DEVIATION_PCT = 5.0
STOP_LOSS_PCT = 3.0
TAKE_PROFIT_FIB = 0.236
MAX_CONCURRENT_POSITIONS = 8
```

- **Out-of-Sample Walk-Forward**: 132 Trades über 79 Symbole, Win Rate 69,7%, Ø PnL 7,37% pro Trade (sogar **höher** als In-Sample ~6,7% — starkes Robustheits-Signal statt Overfitting)
- **Equity-Simulation** (10.000 Start, 10% Positionsgröße, Limit 8): Endkapital **155.811,94** (+1458,12%), Max Drawdown nur **-1,32%**
- **Buy-and-Hold-Vergleich** (147 Aktien nach NaN-Bereinigung): +755,69% Rendite, Max Drawdown -34,83%
- **Strategie schlägt Buy-and-Hold klar auf BEIDEN Dimensionen** (höhere Rendite UND deutlich kleineres Risiko) — das stärkste, überzeugendste Ergebnis über die gesamte Entwicklung aller drei Bots hinweg

**Bewusst NICHT (mehr) verfolgt:** Erweiterung auf alle 503 S&P-500-Werte wurde diskutiert und explizit verworfen (löst Survivorship-Bias nicht, ~10× Rechenzeit, yfinance-Zuverlässigkeit bei dieser Größenordnung fraglich, fehlendes Positionslimit hätte Risiko verschärft — Positionslimit wurde stattdessen nachgerüstet und bei moderaterer Größe (150) belassen).

---

## 4. Gemeinsame Architektur

```
trading-bot/
├── trading-env/                        (Python-3.9-venv)
├── shared/                             (von ALLEN drei Strategien genutzt)
│   ├── paths.py                        (BASE_DIR/DATA_DIR/CONFIG_DIR-Auflösung für strategie-unabhängige Skripte)
│   ├── strategy_paths.py               (Kernstück: get_strategy_paths(__file__) leitet automatisch
│   │                                     RESULTS_DIR, LOGS_DIR, DB_FILE aus dem STRATEGIE-ORDNERNAMEN ab —
│   │                                     neue Strategie hinzufügen = Ordner kopieren, keine Shared-Code-Änderung nötig)
│   ├── fetch_binance_data.py           (Krypto: Einzelsymbol-Abruf-Funktion)
│   ├── fetch_multi_data.py             (Krypto: Multi-Symbol-Abruf, 1h, von elliott_wave genutzt)
│   ├── get_top_symbols.py              (Krypto: rankt Binance-USDT-Paare nach 24h-Volumen,
│   │                                     filtert Stablecoins/gehebelte Token, → top25_symbols.txt)
│   ├── symbols_config.py               (Krypto: SYMBOLS-Liste aus top25_symbols.txt)
│   ├── claude_client.py                (Anthropic-API-Wrapper, siehe Abschnitt 6)
│   ├── daily_interpreter.py            (Agent 1)
│   ├── market_context_agent.py         (Agent 3)
│   ├── param_search_agent.py           (Agent 2)
│   ├── quarterly_interpreter.py        (Quartals-Empfehlungs-Agent)
│   └── status_overview.py              (NEU, zuletzt gebaut: kostenloser Multi-Bot-Statuscheck ohne API-Aufrufe)
├── strategies/
│   ├── elliott_wave/                   (Krypto, 1h)
│   ├── t3_supertrend/                  (Krypto, 4h)
│   └── elliott_wave_stocks/            (Aktien, 1 Tag)
│       [jeweils mit strategie-eigenen Dateien, siehe Abschnitt 5]
├── data/                               (gemeinsamer Ordner für Kursdaten-CSVs, z.B. BTCUSDT_1h.csv,
│                                         AAPL_1d.csv — Dateinamen verhindern Kollisionen zwischen Strategien)
├── config/
│   ├── email_config.py                 (SMTP-Zugangsdaten IONOS/1&1 + ANTHROPIC_API_KEY, siehe Abschnitt 6.5)
│   ├── top25_symbols.txt               (Krypto-Symbolliste)
│   └── sp500_top150.txt                (Aktien-Symbolliste, aktueller Stand)
├── results/<strategie_name>/           (Backtest-/Optimierungs-Ergebnis-CSVs)
├── logs/<strategie_name>/              (Cronjob-Log-Dateien)
├── paper_trading_elliott_wave.db
├── paper_trading_t3_supertrend.db
└── paper_trading_elliott_wave_stocks.db
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

**`live_params.py`-Muster:** Jede Strategie hat eine kleine, von der restlichen Logik getrennte Datei mit den aktuell aktiven Parametern, importiert von `forward_test.py`, `equity_simulation.py`, `quarterly_review.py`, `agent_optimise.py`. Zweck: Parameter-Übernahme nach Validierung soll so einfach und risikoarm wie möglich sein (eine kleine, übersichtliche Datei bearbeiten statt tief im Code zu suchen).

---

## 5. Datei-Inventar pro Strategie (Kernskripte)

Gemeinsames Muster in jedem der drei `strategies/<name>/`-Ordner (Dateinamen variieren leicht zwischen Elliott-Wave- und T3-Varianten):

| Datei | Zweck |
|---|---|
| `zigzag_indicator.py` / `indicators.py` | Kern-Indikator-Berechnung (Zigzag bzw. T3/ADX/SuperTrend) |
| `elliott_wave_counter.py` | (nur Elliott-Wave-Varianten) Wellenzählung + Fibonacci-Score + Überlappungsbereinigung |
| `backtest_elliott.py` / `backtest_trend.py` | Einzelsymbol-Backtest-Engine |
| `optimise_elliott.py` / `optimise_trend.py` | Einzelsymbol-Parameter-Grid-Search (Demo/Diagnose, nicht die Haupt-Optimierung) |
| `multi_symbol_optimise.py` | **Haupt-Optimierungsskript**: lädt alle Symbole, Grid-Search über Parameterraum, robuste Kombination finden |
| `multi_symbol_walk_forward.py` | Teilt Daten 70/30 (In-Sample/Out-of-Sample), validiert Optimierungsergebnis auf ungesehenen Daten |
| `equity_simulation.py` | Event-basierte Portfolio-Simulation (echtes Kapital, Positionsgröße, ggf. Positionslimit) statt naiver Summierung |
| `oos_equity_simulation.py` | (nur Krypto-Varianten) Equity-Simulation beschränkt auf Out-of-Sample-Zeitraum |
| `forward_test.py` | **Live-Skript**: prüft offene Positionen, sucht neue Signale, schreibt in DB — das läuft per Cron |
| `daily_summary_email.py` | Liest DB, baut Zusammenfassung, ruft Agent 1 + Agent 3 auf, verschickt Mail — läuft täglich per Cron |
| `live_params.py` | Aktuell aktive, validierte Parameter (siehe Abschnitt 4) |
| `agent_optimise.py` | Nutzt Agent 2 (`param_search_agent.py`) als Alternative zum vollen Grid-Search |
| `quarterly_review.py` | Vierteljährlicher automatisierter Review-Prozess (siehe Abschnitt 6.4) |

**Strategie-spezifische Zusatzdateien:**
- `t3_supertrend/`: `fetch_4h_data.py`, `regime_filter.py`
- `elliott_wave_stocks/`: `get_top_stocks.py`, `stocks_symbols_config.py`, `fetch_stock_data.py`, `buy_and_hold_benchmark.py`, `signal_quality_test.py`

---

## 6. Claude-Agenten (KI-Zusatzfunktionen)

**Wichtiges Grundprinzip für alle Agenten:** Rein informativ/unterstützend. **Kein Agent verändert automatisch Handelsparameter oder platziert Trades.** Diese Trennung war eine explizite, bewusste Design-Entscheidung (siehe Abschnitt 8).

### 6.1 Agent 1 — Tägliche Einordnung (`daily_interpreter.py`)
- Modell: **Haiku 4.5** (günstig, für einfache Zusammenfassung ausreichend)
- Läuft: automatisch bei jedem `daily_summary_email.py`-Aufruf (3×/Tag über alle Bots)
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
- Läuft: automatisch bei `daily_summary_email.py`, **aber nur wenn der jeweilige Bot offene Positionen hat** (sonst übersprungen, keine Kosten)
- Funktion: `get_market_context(symbols, context_label)` → 3-5 Sätze zu aktuellen Nachrichten/Ereignissen zu den Symbolen mit offenen Positionen
- Kosten: ~0,02-0,03 $ pro Auslösung (inkl. Websuch-Gebühr), 0 € an Tagen ohne offene Positionen
- **Bewusst rein informativ** — blockiert oder löst niemals Trades aus (explizite Design-Entscheidung, da eine validierte "News-Veto"-Logik ein eigenständiges, noch nicht getestetes Feature wäre)

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
**⚠️ UNKLAR / zu verifizieren im neuen Chat:** Es wurde dem Nutzer die Anleitung gegeben, diese Cron-Zeile für **alle drei** Strategien einzutragen. Im Gesprächsverlauf ist nur der **manuelle Testlauf** für `t3_supertrend` bestätigt worden — **nicht explizit bestätigt**, ob die Cron-Zeilen für alle drei Strategien tatsächlich in die Crontab eingetragen wurden. Sollte im neuen Chat zuerst geprüft werden (`crontab -l`).

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

9. **Jede neue Idee wird empirisch zu Ende getestet, auch wenn ein Zwischenergebnis enttäuschend oder verlockend aussieht** (Beispiele: VWAP-Filter beim T3-Bot erst vielversprechend, dann verworfen nach vollständigem Test; "kein Take-Profit"-Idee beim Aktien-Bot als offener Punkt markiert statt vorschnell übernommen).

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

---

## 9. Offene Punkte / nächste sinnvolle Schritte

1. **"Gewinne laufen lassen" (kein Take-Profit) für den Aktien-Bot (Top 150) noch nicht getestet.** Frühere isolierte Tests zeigten deutlich höheren Ø-Gewinn (14,80% vs. 6,47%) bei größerem Drawdown — nicht in Kombination mit dem aktuellen validierten Top-150-Setup getestet. Analog zur erfolgreichen Erkenntnis beim T3-Bot (dort ebenfalls Exit-Mechanik-Experimente durchgeführt).

2. **`MAX_CONCURRENT_POSITIONS = 8` beim Aktien-Bot nicht empirisch getestet** (im Gegensatz zum T3-Bot, wo 3/5/8/unbegrenzt systematisch verglichen wurden). Sollte nachgeholt werden.

3. **Quartals-Review-Cronjobs für `elliott_wave` und `elliott_wave_stocks`**: Anleitung wurde gegeben, aber **nicht explizit bestätigt**, ob sie tatsächlich eingetragen wurden (nur `t3_supertrend` wurde manuell getestet). Mit `crontab -l` verifizieren.

4. **SSH-Fernzugriff (Tailscale) — in Arbeit, nicht abgeschlossen.** Siehe Abschnitt 10, "Startpunkt für die weitere Arbeit".

5. **Live-Trading mit echtem Kapital**: rein konzeptionell besprochen, keine Code-Umsetzung. Bei Bedarf: API-Keys mit Handelsrechten (ohne Auszahlungsrecht), Notausschalter/Kill-Switch, Tagesverlust-Limit, Monitoring/Alarmierung, sehr kleines Startkapital für die ersten Wochen.

6. **E-Mail-Versandzeiten beider Krypto-Bots überschneiden sich** (beide 8:05 Uhr) — wurde einmal als mögliche Unannehmlichkeit angesprochen, aber nie eine Änderung gewünscht/umgesetzt. Kein akuter Handlungsbedarf, nur zur Kenntnis.

---

## 10. STARTPUNKT FÜR DIE WEITERE ARBEIT

### 1. Wo wir aktuell stehen
Alle drei Bots sind vollständig aufgebaut, validiert und laufen automatisiert per Cronjob im Paper-Trading-Modus. Der Aktien-Bot wurde zuletzt auf sein bisher bestes Ergebnis gebracht (Top 150, Positionslimit 8, schlägt Buy-and-Hold klar). Drei Claude-Agenten sind produktiv im Einsatz, ein viertes Quartals-Review-System ist gebaut und mindestens für einen Bot getestet.

### 2. Was zuletzt gemacht wurde
Der Nutzer wollte einen sofortigen, manuellen Statusabruf aller drei Bots ohne auf die geplanten Mails zu warten. Dafür wurde `shared/status_overview.py` gebaut, getestet und erfolgreich beim Nutzer installiert (bestätigt: "Hat geklappt"). Danach wurde nach Möglichkeiten für mobiles Tracking gefragt — zwei Optionen aufgezeigt: (a) bestehende E-Mails aufs Handy (bereits funktionsfähig, keine weitere Aktion nötig), (b) SSH-Fernzugriff via Tailscale für spontanen, interaktiven Zugriff. Nutzer entschied sich für Option (b) und die Einrichtung wurde begonnen:
- **Schritt 1 abgeschlossen**: Tailscale auf Mac UND Handy installiert und beide eingeloggt (vom Nutzer bestätigt: "installiert und eingelegt auf mobiltelefon und laptop mac")
- **Schritt 2 gerade begonnen**: Anleitung gegeben, "Entfernte Anmeldung" (SSH) in macOS-Systemeinstellungen → Allgemein → Freigabe zu aktivieren, und den Tailscale-Gerätenamen des Macs zu notieren. **Auf die Antwort des Nutzers wurde noch nicht reagiert** — die Konversation wurde an dieser Stelle für den Projekt-Wechsel unterbrochen.

### 3. Welche Aufgaben noch offen sind
- SSH-Fernzugriff-Einrichtung fertigstellen (siehe Abschnitt 9, Punkt 4, und unten "nächster Schritt")
- Alle Punkte aus Abschnitt 9 (offene Punkte)

### 4. Was als Nächstes konkret getan werden sollte
**Unmittelbar:** SSH-Einrichtung fortsetzen, an der Stelle weitermachen, wo unterbrochen wurde:
1. Bestätigung einholen, ob "Entfernte Anmeldung" in den macOS-Systemeinstellungen aktiviert ist
2. Den Tailscale-Gerätenamen des Macs erfragen (sichtbar im Tailscale-Menüleisten-Symbol unter "Meine Geräte")
3. Auf dem Handy eine SSH-Client-App installieren (z.B. Termius)
4. Verbindung vom Handy zum Mac über den Tailscale-Namen aufbauen und testen (Login mit Mac-Benutzername/-Passwort)
5. Testen: `cd ~/trading-bot && python3 shared/status_overview.py` vom Handy aus erfolgreich ausführen

**Danach, je nach Präferenz des Nutzers**, eines der offenen Themen aus Abschnitt 9 angehen — keine feste Reihenfolge vom Nutzer vorgegeben, vermutlich sinnvoll: zuerst die Quartals-Review-Cronjob-Verifizierung (Punkt 3, schnell zu prüfen), dann inhaltliche Experimente (Punkte 1-2).

### 5. Informationen, die für die Fortsetzung unbedingt im Kontext bleiben müssen
- **Nutzer-Kenntnisstand**: Grundlegend terminal-erfahren, aber wiederholt Schwierigkeiten mit: mehrzeiligem Copy-Paste (Zeilen rutschen zusammen), vim-Bedienung (nano wird bevorzugt), Verwechslung von Downloads-Ordnerpfaden (durch viele ZIP-Downloads sind nummerierte Duplikate wie `strategies-2` bis `strategies-12` entstanden — bei Dateiabgleichen IMMER mit `find`/`grep` verifizieren, nicht blind auf `cp`-Erfolg vertrauen)
- **Sprache**: Durchgehend Deutsch, Nutzer sitzt in Donaueschingen, Deutschland
- **E-Mail-Provider**: IONOS/1&1 (`smtp.ionos.de`, Port 587, STARTTLS)
- **Sicherheitsvorfall-Historie**: Zwei versehentliche API-Key-Preisgaben im Chat — bei zukünftigen "zeig mir den Inhalt der Datei"-Situationen mit Zugangsdaten IMMER `grep -c` statt `cat` vorschlagen
- **Alle drei `live_params.py`-Inhalte** exakt wie in Abschnitt 3 dokumentiert — diese sind der aktuelle "Wahrheitsstand" der Live-Konfiguration
- **Cronjob-Zeitplan** exakt wie in Abschnitt 6.4 (Quartals-Reviews) und den Bot-Tabellen (Abschnitt 2) dokumentiert
- **Methodik-Prinzipien aus Abschnitt 7** sollten bei jeder neuen Analyse/Optimierung konsequent angewendet werden — das ist der etablierte Qualitätsstandard dieses Projekts
- Terminal-Befehle immer **einzeln, mit Bestätigung zwischen den Schritten** anbieten, nicht mehrere Befehle auf einmal zum Copy-Paste geben (hat wiederholt zu Fehlern geführt)

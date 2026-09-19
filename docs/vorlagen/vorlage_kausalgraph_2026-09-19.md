Claude Prompt – Market Causal Graph & Market Physics Engine

Kontext

Wir bauen bereits eine größere AI-gestützte Trading-Research-Plattform mit mehreren strategischen Ebenen:

1. Autonomous Trading Strategy Research & Bot Evolution
    * Research Agents
    * Strategy Generation
    * Backtesting
    * Walk-Forward Validation
    * Robustness Testing
    * Adversarial Review
    * Strategy Genome
    * Evolutionary Research
    * Strategy Registry
2. AI Market Intelligence & Adaptive Strategy Allocation
    * Market Intelligence
    * AI Event Extraction
    * Market Regime Detection
    * Market Memory
    * Historical Episode Matching
    * Strategy Performance by Regime
    * Adaptive Strategy Allocation
    * Information Arbitrage
3. AI Quant Research OS / Alpha Discovery Lab
    * Alpha Discovery
    * Hypothesis Registry
    * Research Agents
    * Prediction Ledger
    * Agent Calibration
    * Anomaly Detection
    * Causal Research
    * Information Arbitrage
    * Multiple Testing / FDR
    * Edge Decay Monitoring
    * Self-Healing Strategy Pool

Ich möchte nun eine vierte strategische Forschungsschicht hinzufügen:

Market Causal Graph & Market Physics Engine

Wichtig:

Noch nichts implementieren.

Analysiere zuerst das bestehende Repository, die aktuelle Architektur, die vorhandenen Komponenten und den bestehenden Backlog.

Danach sollst du dieses Konzept als eigenständige Erweiterung in die Gesamtarchitektur und den Backlog integrieren.

⸻

1. Grundidee

Die Plattform soll nicht nur fragen:

Welche Strategie funktioniert?

oder:

Welches Marktregime herrscht gerade?

oder:

Wo gibt es statistische Anomalien?

Sie soll zusätzlich erforschen:

Welche Ereignisse und Marktmechanismen führen typischerweise zu welchen Folgebewegungen?

Das System soll deshalb einen dynamischen Market Causal Graph aufbauen.

Beispiel:

Macro Event
    ↓
Interest Rate Expectations
    ↓
USD
    ↓
Crypto / Equities / Gold
    ↓
Volatility
    ↓
Liquidations
    ↓
Order Flow
    ↓
Liquidity
    ↓
Price Impact

Das ist zunächst nur eine Hypothese.

Das System darf solche Beziehungen nicht als kausal betrachten, nur weil sie korrelieren.

Jede behauptete Beziehung muss anschließend quantitativ untersucht und möglichst falsifiziert werden.

⸻

2. Ziel

Baue eine Forschungsarchitektur, die automatisch nach folgenden Strukturen sucht:

* Cause → Effect
* Lead → Lag
* Event → Market Reaction
* Market State → Reaction
* Liquidity → Price Impact
* Volatility → Positioning
* Positioning → Liquidations
* Liquidations → Volatility
* Cross-Asset Transmission
* Feedback Loops
* Regime-dependent relationships
* Event-dependent relationships
* Temporal relationships
* Structural breaks

Das Ziel ist nicht, eine künstliche „Wahrheit über Märkte“ zu behaupten.

Das Ziel ist:

Eine reproduzierbare Forschungsmaschine zu bauen, die überprüfbare Hypothesen über Marktmechanismen erzeugt und diese quantitativ testet.

⸻

3. Market Causal Graph

Entwirf einen persistenten Graphen.

Nodes können beispielsweise sein:

Asset
Market
Exchange
Macro Event
News Event
Economic Indicator
Order Flow
Funding
Open Interest
Liquidation
Volatility
Liquidity
Spread
Volume
Options Flow
Interest Rate
FX
Commodity
Sentiment
Regime
Strategy
Market State

Edges können beispielsweise sein:

LEADS
FOLLOWS
CORRELATES_WITH
REACTS_TO
AMPLIFIES
SUPPRESSES
TRANSMITS_TO
PRECEDES
CO-MOVES_WITH
BREAKS_DOWN_WITH

Wichtig:

Unterscheide klar zwischen:

* beobachteter Korrelation
* zeitlicher Reihenfolge
* statistischer Abhängigkeit
* kausaler Hypothese
* bestätigtem robustem Zusammenhang

Ein Graph-Eintrag sollte deshalb beispielsweise enthalten:

relationship_id
source_node
target_node
relationship_type
hypothesis
confidence
observation_count
sample_period
time_lag_distribution
market_regimes
asset_classes
statistical_tests
out_of_sample_results
transaction_cost_adjusted_results
stability_score
last_validated_at
decay_status

⸻

4. Lead/Lag Discovery Engine

Entwickle ein Research-Modul, das automatisch nach zeitlichen Beziehungen sucht.

Beispiele:

Asset A
   ↓ 2 min
Asset B
Asset B
   ↓ 7 min
Asset C

oder:

Funding
   ↓
Liquidations
   ↓
Volatility
   ↓
Price

Untersuche unter anderem:

* Cross-correlation
* lagged correlations
* Granger-style predictive relationships
* information flow
* event-time alignment
* rolling relationships
* regime-specific relationships
* structural breaks

Wichtig:

Ein statistischer Lead/Lag darf nicht automatisch als handelbares Signal betrachtet werden.

Berücksichtige:

* execution latency
* spread
* slippage
* fees
* liquidity
* market impact
* signal decay
* timestamp quality

⸻

5. Event Reaction Engine

Baue eine historische Event-Reaktionsdatenbank.

Für jedes relevante Ereignis sollen beispielsweise gespeichert werden:

event_type
event_timestamp
event_magnitude
surprise
market_state
volatility_state
liquidity_state
asset_prices_before
asset_prices_after
reaction_30s
reaction_1m
reaction_5m
reaction_15m
reaction_1h
reaction_4h
reaction_1d
volume_response
volatility_response
liquidity_response
funding_response
open_interest_response

Beispiele für Events:

* CPI
* FOMC
* ECB
* employment data
* inflation data
* ETF-related events
* exchange incidents
* major crypto liquidations
* large protocol events
* earnings
* geopolitical events
* major regulatory announcements
* unusual market movements
* extreme positioning changes

Die konkrete Datenverfügbarkeit muss anhand des bestehenden Systems geprüft werden.

⸻

6. Historical Event Similarity

Wenn ein neues Ereignis auftritt, soll das System historische Ereignisse suchen, die strukturell ähnlich sind.

Nicht nur nach Event-Typ.

Beispielsweise:

Event:
CPI surprise +0.5σ
Current State:
High volatility
High positioning
Low liquidity
Strong USD
Risk-off regime

Suche dann historische Situationen mit ähnlichem:

* Event
* Surprise magnitude
* Market regime
* volatility
* liquidity
* positioning
* cross-asset state

und ermittle:

historical reaction distribution
median reaction
tail reaction
reaction variance
time-to-reaction
failure frequency
regime dependency

Das System soll also nicht einfach sagen:

„CPI ist bullish/bearish.“

Sondern:

„Unter diesen historischen Bedingungen trat Reaktion X mit dieser empirischen Verteilung auf.“

⸻

7. Market Physics Engine

Entwirf zusätzlich eine Forschungsabstraktion namens:

Market Physics Engine

Das ist kein Anspruch auf echte physikalische Gesetzmäßigkeiten.

Es ist eine Sammlung empirisch untersuchter Marktmechanismen.

Beispiele:

Liquidity Feedback Loop

Liquidity ↓
    ↓
Price Impact ↑
    ↓
Volatility ↑
    ↓
Liquidations ↑
    ↓
Liquidity ↓

Volatility Feedback

Volatility ↑
    ↓
Risk Reduction
    ↓
Position Unwinding
    ↓
Price Pressure
    ↓
Volatility ↑

Positioning Feedback

Crowded Positioning
        ↓
Small Shock
        ↓
Stop/Liquidation Cascade
        ↓
Forced Orders
        ↓
Price Acceleration

Cross-Asset Transmission

Macro Shock
    ↓
Rates
    ↓
USD
    ↓
Equities / Crypto / Commodities

Das System soll automatisch nach solchen möglichen Feedback-Loops suchen.

⸻

8. Feedback Loop Discovery

Entwickle ein Research-Konzept, das nach selbstverstärkenden oder selbstabschächenden Marktmechanismen sucht.

Beispiele:

A → B → C → A

oder:

A ↑
 ↓
B ↑
 ↓
C ↑
 ↓
A further ↑

Untersuche:

* Verstärkung
* Dämpfung
* Stabilität
* Zeitverzögerung
* Regimeabhängigkeit
* Sättigung
* Breakpoints
* Failure Conditions

Wichtig:

Nicht jede gefundene Schleife ist real.

Sie muss gegen alternative Erklärungen getestet werden.

⸻

9. Causal Hypothesis Engine

Die AI soll aus Daten und Beobachtungen strukturierte Hypothesen erzeugen.

Beispiel:

Hypothesis:
When liquidity is unusually low,
a moderate external shock causes
larger short-term price impact.
Variables:
liquidity
spread
depth
volume
volatility
price impact
Expected relationship:
low liquidity → higher price impact
Required tests:
historical
out-of-sample
regime-specific
cross-market
transaction-cost adjusted

Die AI erzeugt also:

Hypothese

nicht:

Trading Decision

⸻

10. Counterfactual Research

Ergänze eine Counterfactual Research Layer.

Frage beispielsweise:

Wäre die beobachtete Marktbewegung auch ohne das identifizierte Event wahrscheinlich gewesen?

Beispiel:

Observed:
News
+
High Volume
+
BTC +3%
Possible explanations:
A) News caused movement
B) Existing trend caused movement
C) Short squeeze caused movement
D) News amplified an existing move
E) News was irrelevant

Das System soll alternative Erklärungen explizit erzeugen und quantitativ untersuchen.

Wichtig:

Keine unbegründeten kausalen Behauptungen.

⸻

11. Causal Graph + Alpha Discovery

Der Market Causal Graph soll direkt mit dem bestehenden:

AI Quant Research OS / Alpha Discovery Lab

verbunden werden.

Beispiel:

Causal Observation
       ↓
Hypothesis
       ↓
Alpha Discovery
       ↓
Backtest
       ↓
Validation
       ↓
Strategy Candidate

Der Causal Graph selbst darf niemals als Beweis für Profitabilität betrachtet werden.

⸻

12. Causal Graph + Regime Engine

Verbindungen müssen regimeabhängig analysiert werden.

Beispielsweise:

Relationship A → B
Bull Market:
strong
Bear Market:
weak
High Volatility:
strong
Low Volatility:
weak

Deshalb soll jede Relationship möglichst einen Kontext enthalten:

relationship
+
market regime
+
volatility regime
+
liquidity regime
+
asset class
+
time horizon

⸻

13. Market Episode Memory

Verbinde den Causal Graph mit der bereits geplanten Market Memory.

Eine Episode könnte enthalten:

Market State
+
Events
+
Relationships
+
Order Flow
+
Liquidity
+
Volatility
+
Positioning
+
Cross Asset State
+
Subsequent Reaction

Damit kann das System später fragen:

„Welche historischen Marktphasen ähneln der aktuellen Situation?“

und:

„Welche Beziehungen waren in diesen Situationen relevant?“

⸻

14. Relationship Lifecycle

Jede entdeckte Beziehung braucht einen Lifecycle.

Beispiel:

DISCOVERED
    ↓
HYPOTHESIS
    ↓
TESTING
    ↓
VALIDATED
    ↓
MONITORED
    ↓
WEAKENING
    ↓
DECAYED
    ↓
RESEARCH AGAIN

Eine Relationship darf also nicht für immer als gültig gelten.

⸻

15. Relationship Decay Detection

Baue ein Konzept für:

Causal Relationship Decay

Überwache:

* Effektgröße
* statistische Stabilität
* Lead/Lag
* regime dependency
* transaction-cost-adjusted edge
* prediction error
* distribution shift
* market structure changes

Wenn eine Beziehung schwächer wird:

Relationship weakening
        ↓
Re-validation
        ↓
Alternative explanations
        ↓
Regime analysis
        ↓
Retire / Modify / Reactivate

⸻

16. Research Council

Integriere mehrere spezialisierte AI Research Agents.

Beispielsweise:

Macro Researcher

Sucht nach:

* rates
* inflation
* monetary policy
* economic data

Market Structure Researcher

Sucht nach:

* liquidity
* spreads
* order book
* market impact

Crypto Microstructure Researcher

Sucht nach:

* funding
* OI
* liquidations
* exchange flows

Cross-Asset Researcher

Sucht nach:

* equities
* bonds
* FX
* commodities
* crypto

Event Researcher

Sucht nach:

* news
* announcements
* event reactions

Statistical Researcher

Sucht nach:

* correlations
* lead/lag
* anomalies
* change points
* structural breaks

Die Agents dürfen unterschiedliche Hypothesen entwickeln.

Ein Research Council kann anschließend:

* Hypothesen zusammenführen
* Widersprüche identifizieren
* alternative Erklärungen erzeugen
* Research priorisieren

Die quantitative Engine bleibt die Instanz für empirische Validierung.

⸻

17. Prediction vs Causality

Trenne strikt:

Predictive Relationship

von:

Causal Hypothesis

Ein Feature kann Vorhersagekraft besitzen, ohne dass seine Ursache verstanden wurde.

Umgekehrt kann eine plausible kausale Hypothese keine ausreichende kurzfristige Vorhersagekraft für Trading besitzen.

Beide Fälle müssen separat gespeichert werden.

⸻

18. Falsification First

Ein zentraler Bestandteil des Systems soll sein:

Versuche zuerst, die gefundene Beziehung zu zerstören.

Für jede neue Relationship sollen möglichst automatisch geprüft werden:

* alternative Erklärung
* look-ahead bias
* data leakage
* timestamp errors
* survivorship bias
* selection bias
* multiple testing
* data snooping
* regime dependence
* structural breaks
* transaction costs
* slippage
* liquidity
* sample size
* out-of-sample stability

Nur robuste Relationships dürfen in nachgelagerte Strategy Research Pipelines gelangen.

⸻

19. Multiple Testing

Der Causal Graph wird potentiell eine enorme Anzahl von Beziehungen erzeugen.

Deshalb muss Multiple Testing ein First-Class-Problem sein.

Tracke mindestens:

number_of_relationships_tested
number_of_hypotheses
number_of_significant_results
number_of_validated_relationships
false_discovery_controls
research_iteration
data_version

Berücksichtige geeignete Verfahren zur Kontrolle von False Discoveries und Backtest Overfitting.

⸻

20. AI darf keine direkte Kapitalentscheidung treffen

Architekturprinzip:

AI
 ↓
Observation
 ↓
Interpretation
 ↓
Hypothesis
 ↓
Quantitative Validation
 ↓
Strategy
 ↓
Risk Engine
 ↓
Execution

Nicht:

AI
 ↓
BUY / SELL

Die Risk Engine bleibt unabhängig.

Die Causal Engine liefert Research und Informationen.

⸻

21. Integration mit den bisherigen drei Systemen

Analysiere Überschneidungen und definiere klare Verantwortlichkeiten.

Strategy Factory

Frage:

Welche Strategien können aus validierten Erkenntnissen entstehen?

Market Intelligence

Frage:

Was passiert aktuell im Markt?

Alpha Discovery

Frage:

Wo gibt es möglicherweise eine statistische Ineffizienz?

Market Causal Graph

Frage:

Welche Marktmechanismen und zeitlichen Beziehungen könnten erklären, was wir beobachten?

Diese Systeme sollen sich gegenseitig verbessern.

⸻

22. Gesamtarchitektur

Prüfe folgende Zielarchitektur:

                         WORLD
                           │
                           ▼
                  ┌─────────────────┐
                  │ Information     │
                  │ Intelligence    │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Market Episode  │
                  │ Memory          │
                  └────────┬────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        Alpha Discovery  Regime     Causal Graph
              │          Engine          │
              │            │             │
              └────────────┼─────────────┘
                           ▼
                  ┌─────────────────┐
                  │ Research        │
                  │ Council         │
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │ Quant Validation│
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │ Strategy Factory│
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │ Strategy Pool   │
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │ AI Allocation   │
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │ Risk Engine     │
                  └────────┬────────┘
                           ▼
                       Execution
                           │
                           ▼
                  ┌─────────────────┐
                  │ Edge / Causal   │
                  │ Decay Monitor   │
                  └────────┬────────┘
                           │
                           └──────→ Research

⸻

23. Technische Architektur

Analysiere, welche Teile davon mit der bestehenden Architektur umgesetzt werden können.

Prüfe insbesondere:

* Python
* PostgreSQL
* TimescaleDB oder vergleichbare Time-Series Storage
* Redis
* Queue / Event Bus
* Vector Database
* Graph Database
* Feature Store
* Experiment Tracking
* Model Registry
* Claude Agent SDK
* xAI / Grok API
* Market Data APIs
* News APIs
* Order Book Data
* Options Data
* On-Chain Data
* Backtesting Engine
* Paper Trading
* Execution Layer

Entscheide nicht automatisch, dass jede Technologie notwendig ist.

Begründe:

* warum
* wann
* welche Alternative
* welche Abhängigkeit
* welche Kosten
* welche Skalierungsprobleme

⸻

24. Data Lineage

Jede Relationship und jede Hypothese muss reproduzierbar sein.

Speichere möglichst:

data_source
data_version
timestamp
feature_version
model_version
prompt_version
agent_version
research_run_id
hypothesis_id
relationship_id
test_configuration
result

Eine spätere Analyse muss nachvollziehen können:

Wie genau wurde diese Hypothese erzeugt und validiert?

⸻

25. Research Cost

Analysiere auch die Kosten.

Tracke:

LLM cost
API cost
market data cost
compute cost
backtest cost
storage cost
research time

Mögliche Kennzahl:

cost_per_hypothesis
cost_per_test
cost_per_validated_relationship
cost_per_strategy_candidate

Ziel ist nicht maximale AI-Aktivität.

Ziel ist:

möglichst viel qualitativ hochwertige Research-Information pro Einheit Kosten zu erzeugen.

⸻

26. MVP

Definiere ein möglichst kleines, aber wissenschaftlich sinnvolles MVP.

Das MVP sollte NICHT sofort den kompletten Causal Graph bauen.

Beispielsweise:

1. wenige hochwertige Datenquellen
2. wenige Asset-Klassen
3. Event Database
4. Lead/Lag Discovery
5. Event Reaction Analysis
6. einfache Relationship Registry
7. Historical Episode Matching
8. OOS Validation
9. Multiple Testing Controls
10. Relationship Decay Monitoring

Das MVP soll primär beantworten:

Können wir tatsächlich robuste und wiederkehrende Marktbeziehungen identifizieren, die über einfache Korrelationen hinausgehen?

Nicht:

Können wir sofort eine profitable Tradingstrategie bauen?

⸻

27. Backlog-Struktur

Erstelle daraus einen strukturierten Backlog.

Empfohlene Epics:

1. Market Causal Graph
2. Relationship Registry
3. Lead/Lag Discovery
4. Event Reaction Engine
5. Event Reaction Database
6. Historical Event Similarity
7. Market Physics Engine
8. Feedback Loop Discovery
9. Causal Hypothesis Engine
10. Counterfactual Research
11. Causal Research Council
12. Market Episode Integration
13. Relationship Validation
14. Multiple Testing / FDR
15. Relationship Decay
16. Data Lineage
17. Research Cost Analytics
18. Strategy Factory Integration
19. Market Intelligence Integration
20. Alpha Discovery Integration

Bewerte jede Komponente nach:

* Impact
* Research Value
* Implementation Complexity
* Data Requirements
* Dependencies
* Risk of False Discoveries
* Compute Cost
* LLM Cost
* Priority

Keine subjektive „Profitability Score“-Bewertung erfinden. Priorisiere nach nachvollziehbaren technischen und wissenschaftlichen Kriterien.

⸻

28. Governance

Definiere klare Grenzen.

Insbesondere:

* AI darf Hypothesen generieren.
* AI darf Research priorisieren.
* AI darf Beziehungen analysieren.
* AI darf Strategiekandidaten erzeugen.
* Quantitative Tests müssen unabhängig nachvollziehbar sein.
* Risk Engine muss unabhängig bleiben.
* Live-Kapitalallokation benötigt explizite Governance.
* Keine autonome Änderung kritischer Risk Limits.
* Keine automatische Promotion einer unbekannten Relationship zu Live Trading.

⸻

29. Was ich von dir erwarte

Analysiere zuerst das bestehende Projekt.

Danach liefere:

A. Existing Architecture

Welche bestehenden Komponenten können bereits verwendet werden?

B. New Architecture

Welche neuen Komponenten sind notwendig?

C. Overlap Analysis

Welche Funktionen überschneiden sich mit:

* Strategy Factory
* AI Market Intelligence
* Alpha Discovery

und welche sollten zusammengelegt werden?

D. Target Architecture

Wie sieht die integrierte Gesamtarchitektur aus?

E. Backlog

Erstelle:

Epic
  └── Feature
       └── Task
            └── Subtask

F. Dependencies

Zeige Abhängigkeiten und mögliche Blocker.

G. MVP

Definiere das kleinste sinnvolle MVP.

H. V2 / Future Research

Welche fortgeschrittenen Komponenten kommen später?

I. Technical Risks

Identifiziere:

* data leakage
* false causality
* spurious correlations
* multiple testing
* overfitting
* structural breaks
* timestamp problems
* survivorship bias
* execution assumptions
* data quality
* AI hallucination
* LLM cost explosion

J. Top 10 Next Tickets

Gib die zehn sinnvollsten nächsten Tickets an, nachdem du das bestehende Projekt analysiert hast.

⸻

30. Wichtigstes Architekturprinzip

Das System soll nicht versuchen, eine allwissende AI zu bauen.

Es soll eine wissenschaftlich arbeitende automatisierte Research-Maschine werden.

Der wichtigste Loop lautet:

OBSERVE
   ↓
DETECT
   ↓
CONNECT
   ↓
HYPOTHESIZE
   ↓
FALSIFY
   ↓
VALIDATE
   ↓
UNDERSTAND
   ↓
IMPLEMENT
   ↓
MONITOR
   ↓
DETECT DECAY
   ↓
RESEARCH AGAIN

Die zentrale Idee ist:

Nicht nur herausfinden, WAS der Markt macht, sondern systematisch untersuchen, WELCHE beobachtbaren Mechanismen und zeitlichen Beziehungen damit verbunden sind – und welche davon unter strenger Out-of-Sample- und Robustness-Prüfung Bestand haben.

Das System soll dabei niemals Korrelation automatisch mit Kausalität verwechseln.

Die AI ist der Researcher.

Die quantitative Engine ist der Prüfer.

Die Risk Engine ist der Gatekeeper.

Die Execution Engine führt nur Entscheidungen aus, die die dafür vorgesehenen Validierungs- und Governance-Prozesse bestanden haben.

Das langfristige Ziel ist eine integrierte Research-Plattform:

Market Intelligence
        +
Market Memory
        +
Causal Graph
        +
Alpha Discovery
        +
Strategy Factory
        +
Regime Intelligence
        +
Strategy Evolution
        +
Portfolio Intelligence
        +
Edge Decay Detection

die kontinuierlich neue Markt-Hypothesen entdeckt, testet, falsifiziert, validiert und bei Bedarf in reproduzierbare Strategiekandidaten überführt.

Bitte erst analysieren und planen. Nicht direkt implementieren.
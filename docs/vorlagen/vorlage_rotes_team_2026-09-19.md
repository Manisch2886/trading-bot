Claude Prompt – Autonomous Adversarial Trading Lab / Strategy Red Team

Kontext

Wir bauen eine umfangreiche AI-gestützte quantitative Research-Plattform.

Bisher existieren bzw. sind geplant:

1. Autonomous Trading Strategy Research & Bot Evolution
2. AI Market Intelligence & Adaptive Strategy Allocation
3. AI Quant Research OS / Alpha Discovery Lab
4. Market Causal Graph & Market Physics Engine

Ich möchte nun eine weitere eigenständige strategische Forschungsschicht ergänzen:

Autonomous Adversarial Trading Lab

Die Grundidee:

Statt AI nur neue Tradingstrategien finden zu lassen, soll ein autonomes Red-Team-System versuchen, jede Strategie systematisch zu zerstören.

Eine Strategie soll nicht deshalb als interessant gelten, weil sie einen hohen Backtest-Return besitzt.

Sie soll als interessant gelten, wenn sie eine große Anzahl gezielter adversarialer Tests überlebt.

⸻

1. Grundprinzip

Der klassische Research Loop ist:

Idea
 ↓
Strategy
 ↓
Backtest
 ↓
Validation
 ↓
Deploy

Das neue System soll daraus machen:

Strategy
 ↓
Attack
 ↓
Find Weakness
 ↓
Explain Failure
 ↓
Repair / Modify
 ↓
Attack Again
 ↓
Robustness Validation
 ↓
Paper Trading
 ↓
Continuous Attack

Die zentrale Frage lautet:

„Wie können wir diese Strategie möglichst überzeugend zum Scheitern bringen?“

Nicht:

„Wie können wir die Strategie möglichst gut aussehen lassen?“

⸻

2. Adversarial Research Agent

Entwickle einen spezialisierten Agenten:

Strategy Red Team Agent

Dieser erhält:

* Strategy Specification
* Code
* Backtest Results
* Dataset
* Feature Definitions
* Entry/Exit Rules
* Position Sizing
* Risk Rules
* Execution Assumptions
* Market Regimes
* Historical Performance
* OOS Results

und versucht anschließend systematisch, Schwachstellen zu finden.

⸻

3. Attack Categories

Das System soll unterschiedliche Angriffskategorien besitzen.

A. Data Attacks

Teste:

* Look-ahead bias
* Data leakage
* Survivorship bias
* Selection bias
* Timestamp errors
* Incorrect corporate actions
* Missing data
* Bad data
* Delisted assets
* Future information accidentally available
* Incorrect feature construction

⸻

B. Execution Attacks

Simuliere:

* higher slippage
* wider spreads
* delayed execution
* partial fills
* missed fills
* latency
* liquidity deterioration
* market impact
* order queue effects
* exchange downtime

Frage:

Ist die Strategie nur unter unrealistisch perfekten Ausführungsbedingungen profitabel?

⸻

4. Parameter Attack

Versuche herauszufinden, ob die Strategie nur aufgrund einer sehr spezifischen Parametrisierung funktioniert.

Beispiel:

Lookback = 37
Threshold = 1.73
Stop = 2.14
Take Profit = 4.87

Teste:

Lookback:
20 → 60
Threshold:
1.2 → 2.2
Stop:
1.0 → 3.0

Erzeuge Parameter Stability Maps.

Eine robuste Strategie sollte nicht nur an einem winzigen Parameterpunkt funktionieren.

⸻

5. Regime Attacks

Zerlege Performance nach:

* Bull Market
* Bear Market
* Sideways
* High Volatility
* Low Volatility
* High Liquidity
* Low Liquidity
* Risk-On
* Risk-Off
* Crisis
* Post-Crisis
* Event-driven periods

Frage:

In welchen Marktbedingungen versagt die Strategie?

Nicht nur:

In welchen Marktbedingungen funktioniert sie?

⸻

6. Time Attacks

Teste:

* verschiedene Jahrzehnte
* verschiedene Jahre
* verschiedene Monate
* verschiedene Wochentage
* verschiedene Uhrzeiten
* verschiedene Sessions

Untersuche:

performance stability
trade frequency
drawdown
volatility
correlation

Suche insbesondere nach:

„Die Strategie funktioniert eigentlich nur in einem kleinen historischen Zeitfenster.“

⸻

7. Asset Attacks

Wenn eine Strategie auf mehreren Assets funktioniert, teste:

* Einzelasset
* Asset Groups
* Cross-Asset
* unterschiedliche Exchanges
* unterschiedliche Market Structures

Frage:

Ist der Edge tatsächlich allgemein oder nur auf einem einzelnen Markt vorhanden?

⸻

8. Randomization Attacks

Verwende kontrollierte Randomisierung.

Beispielsweise:

* shuffle trade sequence
* bootstrap trades
* randomized entry timing
* randomized execution
* randomized slippage
* randomized transaction costs
* randomized parameter perturbation
* block bootstrap
* regime resampling

Ziel:

Die Strategie soll nicht nur auf einer einzigen historischen Realisierung funktionieren.

⸻

9. Monte-Carlo Stress Testing

Erzeuge viele alternative Realisierungen des Strategie-Tradingverlaufs.

Untersuche:

Expected Drawdown
Worst Drawdown
Recovery Time
Loss Streak
Capital Requirement
Risk of Ruin
Return Distribution

Speichere nicht nur einen Backtest-Wert.

Speichere eine Verteilung.

⸻

10. Synthetic Market Attack

Entwickle eine Research-Schicht für synthetische Marktszenarien.

Beispielsweise:

Scenario A:
Trend + low volatility
Scenario B:
Trend + volatility expansion
Scenario C:
Sudden gap
Scenario D:
Liquidity collapse
Scenario E:
High correlation breakdown
Scenario F:
Extreme spread widening
Scenario G:
Flash crash
Scenario H:
Persistent mean reversion
Scenario I:
False breakout environment

Teste, wie die Strategie reagiert.

Wichtig:

Synthetic data darf nicht als Beweis für reale Profitabilität verwendet werden.

Sie dient als Stress- und Failure-Research.

⸻

11. Adversarial Market Generator

Langfristig soll das System automatisch Marktbedingungen erzeugen, unter denen die Strategie wahrscheinlich versagt.

Beispiel:

Strategy:
Trend Following
Red Team:
Find market characteristics that maximize losses.
Result:
High-frequency reversals
+
low trend persistence
+
high transaction costs

Das System lernt dadurch:

Unter welchen Marktbedingungen ist diese Strategie besonders verwundbar?

⸻

12. Strategy Weakness Profile

Jede Strategie bekommt ein dynamisches Weakness Profile.

Beispiel:

Strategy: Momentum_042
Strengths:
- persistent trends
- moderate volatility
- liquid markets
Weaknesses:
- rapid reversals
- high transaction costs
- low liquidity
- volatility spikes
Critical Failure Mode:
high-volatility mean-reverting environments

Dieses Profil soll später von der AI Allocation Engine genutzt werden.

⸻

13. Strategy Kill Tests

Definiere harte Tests.

Beispielsweise:

KILL TEST 1
Performance disappears after realistic transaction costs.
KILL TEST 2
Edge exists only in-sample.
KILL TEST 3
Performance depends on one year.
KILL TEST 4
Performance depends on one asset.
KILL TEST 5
Tiny parameter changes destroy performance.
KILL TEST 6
One market event explains most returns.
KILL TEST 7
Removing top 5 trades destroys the strategy.
KILL TEST 8
Small execution delay destroys the edge.

Wenn ein Kill Test anschlägt, muss die Strategie in einen entsprechenden Status wechseln.

Beispielsweise:

ACTIVE
↓
UNDER_ATTACK
↓
WEAKNESS_FOUND
↓
RESEARCH_REQUIRED
↓
REPAIRED
↓
RETESTING

oder:

ACTIVE
↓
UNDER_ATTACK
↓
FAILED
↓
RETIRED

⸻

14. Top-Trades Dependency Test

Ein wichtiger Test:

Wie stark hängt die Strategie von wenigen außergewöhnlichen Trades ab?

Teste:

* Top 1 trade removed
* Top 5 trades removed
* Top 10 trades removed
* best month removed
* best year removed
* extreme event removed

Erzeuge anschließend eine Performance-Verteilung.

Eine Strategie, deren gesamte historische Performance aus wenigen Trades stammt, soll entsprechend gekennzeichnet werden.

⸻

15. Drawdown Forensics

Nicht nur den maximalen Drawdown speichern.

Untersuche jeden Drawdown:

start
duration
depth
market regime
volatility
liquidity
cross-asset state
strategy state
recovery

Die AI soll anschließend versuchen zu erklären:

Warum ist dieser Drawdown entstanden?

und:

Welche Bedingungen gingen ihm voraus?

⸻

16. Failure Mode Database

Baue eine zentrale Datenbank aller beobachteten Failure Modes.

Beispiel:

Failure Mode:
Volatility Shock
Affected Strategies:
Momentum
Breakout
Mean Reversion
Trigger:
Volatility + liquidity collapse
Observed Impact:
Large drawdowns

Dadurch entsteht langfristig ein:

Strategy Failure Knowledge Graph

Strategien können mit Failure Modes verbunden werden.

Strategy A
 ├── vulnerable_to → Liquidity Shock
 ├── vulnerable_to → False Breakouts
 └── vulnerable_to → Volatility Spike
Strategy B
 ├── vulnerable_to → Mean Reversion
 └── vulnerable_to → High Fees

⸻

17. Strategy Repair Agent

Nach einer gefundenen Schwachstelle darf ein separater Agent versuchen, die Strategie zu verbessern.

Beispiel:

Original Strategy
       ↓
Failure:
High volatility drawdown
       ↓
Repair Hypothesis:
Reduce position size during volatility spikes
       ↓
Modified Strategy
       ↓
Full Validation Again

Wichtig:

Eine Reparatur darf nicht einfach die historische Performance maximieren.

Sie muss die ursprüngliche Failure Mode adressieren und anschließend erneut vollständig validiert werden.

⸻

18. Adversarial Evolution

Verbinde das Red-Team-System mit dem bestehenden Strategy Genome.

Evolution soll nicht nur bedeuten:

Strategy → mutation → better backtest

sondern:

Strategy
 ↓
Mutation
 ↓
Backtest
 ↓
Red Team
 ↓
Robustness
 ↓
Survival

Die Fitness einer Strategie soll deshalb nicht nur Performance enthalten.

Berücksichtige beispielsweise:

Return Quality
+
Robustness
+
Parameter Stability
+
Regime Coverage
+
Execution Robustness
+
Drawdown Stability
+
Failure Resistance

Keine einzelne Kennzahl soll automatisch über die anderen dominieren.

⸻

19. Strategy Immune System

Entwickle langfristig die Idee eines:

Strategy Immune System

Jede Strategie besitzt:

* bekannte Schwachstellen
* bekannte Failure Modes
* historische Drawdowns
* Stress Tests
* adversarial scenarios
* robustness score
* current health state

Neue Marktbedingungen werden kontinuierlich gegen dieses Profil geprüft.

Beispiel:

New Market State
       ↓
Strategy Vulnerability Check
       ↓
Potential Failure Risk
       ↓
Allocator Warning

Das bedeutet nicht automatisch, dass eine Strategie deaktiviert wird.

Die Information wird an die Risk/Allocation-Schicht weitergegeben.

⸻

20. Live Shadow Red Team

Auch nach erfolgreicher Backtest-Validierung soll das Red Team weiterlaufen.

Im Paper-/Shadow-Modus:

Live Market
   ↓
Strategy
   ↓
Expected Behavior
   ↓
Observed Behavior
   ↓
Red Team Monitor

Suche nach:

* performance degradation
* execution degradation
* regime mismatch
* unexpected behavior
* increased correlation
* new failure modes

⸻

21. Strategy Health

Definiere einen dynamischen Health State.

Beispiel:

RESEARCH
VALIDATING
ROBUST
PAPER
LIVE_CANDIDATE
LIVE
DEGRADED
UNDER_REVIEW
QUARANTINED
RETIRED

Zusätzlich:

Known Weaknesses
Unknown Risk
Recent Stress
Execution Quality
Regime Compatibility

⸻

22. Continuous Red Teaming

Das System soll nicht einmal testen und anschließend „fertig“ sein.

Sondern:

Strategy
 ↓
Research
 ↓
Validation
 ↓
Deployment
 ↓
Monitoring
 ↓
New Market Conditions
 ↓
New Attacks
 ↓
New Failure Modes
 ↓
Research

Damit wird Robustness zu einem kontinuierlichen Prozess.

⸻

23. Integration mit dem Market Causal Graph

Nutze den Causal Graph, um Failure Modes zu erklären.

Beispiel:

Liquidity ↓
    ↓
Spread ↑
    ↓
Slippage ↑
    ↓
Strategy Performance ↓

Der Red Team Agent kann daraus neue Stressszenarien generieren.

⸻

24. Integration mit Alpha Discovery

Alpha Discovery sucht:

Welche Beziehungen könnten funktionieren?

Red Team fragt:

Unter welchen Bedingungen verschwindet diese Beziehung?

Dadurch entsteht:

Alpha Discovery
       ↓
Hypothesis
       ↓
Validation
       ↓
Red Team
       ↓
Failure Analysis
       ↓
Robust Alpha

⸻

25. Integration mit Market Intelligence

Market Intelligence erkennt:

Welcher Markt befindet sich gerade in welchem Zustand?

Red Team beantwortet:

Welche Strategien sind in diesem Zustand besonders verwundbar?

Damit kann die Allocation Engine zusätzliche Informationen erhalten.

⸻

26. Integration mit Strategy Factory

Strategy Factory erzeugt:

Strategy Candidates

Red Team erzeugt:

Attack Scenarios
Failure Modes
Repair Hypotheses

Zusammen entsteht:

Generate
   ↓
Test
   ↓
Attack
   ↓
Repair
   ↓
Attack Again
   ↓
Validate

⸻

27. Research Ledger

Jeder Angriff muss reproduzierbar gespeichert werden.

Beispielsweise:

attack_id
strategy_id
strategy_version
dataset_version
market_period
attack_type
parameters
scenario
result
failure_mode
severity
timestamp
agent_version
model_version
prompt_version

Dadurch entsteht eine vollständige Historie.

⸻

28. Red-Team Agent Performance

Auch die Red-Team Agents selbst sollen evaluiert werden.

Tracke:

* gefundene echte Failure Modes
* False Positives
* False Negatives
* redundante Tests
* Kosten
* Zeit
* später bestätigte Schwachstellen

So kann das System langfristig lernen:

Welche Angriffsarten finden tatsächlich relevante Probleme?

⸻

29. Research Budget

Verhindere unkontrollierte AI-Kosten.

Implementiere konzeptionell:

Research Budget
      ↓
Attack Priority
      ↓
High-risk strategies first
      ↓
High-value tests first

Priorisierung kann berücksichtigen:

* Kapitalrelevanz
* Strategy exposure
* bekannte Schwächen
* Unsicherheit
* neue Marktbedingungen
* historische Failure Frequency
* Testkosten

⸻

30. Wichtig: Keine triviale Optimierung

Das System darf nicht versuchen:

„Finde Parameter, die die Strategie besser aussehen lassen.“

Es soll versuchen:

„Finde Bedingungen, unter denen die Strategie nicht funktioniert.“

Eine Verbesserung darf nur akzeptiert werden, wenn sie:

1. eine identifizierte Schwäche adressiert,
2. out-of-sample getestet wird,
3. nicht lediglich einen historischen Zeitraum optimiert,
4. robuste Parameter besitzt,
5. realistische Execution Costs überlebt,
6. erneut durch das Red Team getestet wurde.

⸻

31. Backlog

Erstelle folgende mögliche Epics:

1. Red Team Framework
2. Strategy Attack Engine
3. Data Integrity Attacks
4. Execution Stress Testing
5. Parameter Stability Testing
6. Regime Attacks
7. Time/Asset Attacks
8. Randomization Engine
9. Monte Carlo Engine
10. Synthetic Market Stress
11. Adversarial Market Generator
12. Strategy Weakness Profiles
13. Kill Tests
14. Drawdown Forensics
15. Failure Mode Database
16. Strategy Repair Agent
17. Adversarial Strategy Evolution
18. Strategy Immune System
19. Live Shadow Red Team
20. Strategy Health Monitoring
21. Red-Team Agent Evaluation
22. Research Cost/Budget Management

Ordne diese nach:

* Dependencies
* Complexity
* Research Value
* Risk Reduction
* Data Requirements
* Compute Cost
* LLM Cost

⸻

32. MVP

Definiere ein kleines MVP.

Es sollte mindestens enthalten:

1. Strategy Registry Integration
2. Automated Attack Runner
3. Transaction Cost Stress
4. Parameter Perturbation
5. Time/Regime Splitting
6. Top-Trades Dependency Test
7. Monte Carlo Trade Resampling
8. Failure Mode Registry
9. Strategy Health State
10. Automated Red-Team Report

Der MVP soll zunächst zeigen:

Finden systematische adversariale Tests tatsächlich Schwächen, die durch einen normalen Backtest nicht sichtbar werden?

⸻

33. Zielarchitektur

Prüfe folgende Gesamtarchitektur:

                 ┌──────────────────────┐
                 │   Market Intelligence│
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │   Alpha Discovery    │
                 └──────────┬───────────┘
                            │
                 ┌──────────▼───────────┐
                 │   Strategy Factory   │
                 └──────────┬───────────┘
                            │
                            ▼
                    Strategy Candidate
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Quant Validation     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   RED TEAM LAB       │
                 │                      │
                 │ Attack                │
                 │ Stress                │
                 │ Falsify               │
                 │ Break                 │
                 └──────────┬───────────┘
                            │
                    ┌───────┴───────┐
                    │               │
                 FAILED          SURVIVED
                    │               │
                    ▼               ▼
               Research        Robustness
                    │               │
                    ▼               ▼
                 Repair          Paper
                    │               │
                    └───────┬───────┘
                            ▼
                     Strategy Pool
                            │
                            ▼
                      Allocation
                            │
                            ▼
                       Risk Engine
                            │
                            ▼
                        Execution
                            │
                            ▼
                   Live Monitoring
                            │
                            ▼
                      Red Team Again

⸻

34. Claude Output

Nachdem du das bestehende Repository und den aktuellen Backlog analysiert hast, liefere:

A. Existing Components

Welche bestehenden Komponenten können wir wiederverwenden?

B. New Components

Welche neuen Komponenten brauchen wir?

C. Architecture

Wie integriert sich das Red-Team-System in die bisherige Gesamtarchitektur?

D. Overlap Analysis

Welche bestehenden Komponenten überschneiden sich?

E. Backlog

Erstelle Epics → Features → Tasks → Subtasks.

F. Dependencies

Welche Abhängigkeiten existieren?

G. MVP

Was ist die kleinste sinnvolle Version?

H. V2

Welche fortgeschrittenen Fähigkeiten kommen später?

I. Risks

Welche technischen und wissenschaftlichen Risiken existieren?

J. Top 10 Tickets

Welche zehn Tickets sollten nach Analyse des bestehenden Projekts als nächstes erstellt werden?

⸻

35. Übergeordnetes Prinzip

Das System soll nicht möglichst viele Backtests produzieren.

Es soll möglichst viele falsche Strategien frühzeitig eliminieren und gleichzeitig robuste Strategien identifizieren.

Die zentrale Research-Philosophie lautet:

GENERATE
   ↓
TEST
   ↓
ATTACK
   ↓
BREAK
   ↓
UNDERSTAND
   ↓
REPAIR
   ↓
ATTACK AGAIN
   ↓
VALIDATE
   ↓
MONITOR
   ↓
ATTACK AGAIN

Oder kurz:

Don’t ask whether a strategy works. Ask how hard it is to break.

Die Plattform soll dadurch langfristig nicht nur eine Strategy Factory werden, sondern ein autonomes adversariales Forschungslabor für quantitative Strategien.

Wichtig:

Noch nichts implementieren.

Zuerst Repository, Architektur und bestehenden Backlog analysieren, anschließend dieses Konzept sauber integrieren, Überschneidungen reduzieren und eine priorisierte Roadmap erstellen.
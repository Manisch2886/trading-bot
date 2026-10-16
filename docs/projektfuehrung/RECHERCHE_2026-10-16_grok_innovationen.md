# Recherche 16.10.2026 — Grok: neue belegte Entwicklungen bei regelbasierten Strategien (Tagesdaten)

*Quelle: Grok (grok.com, Modus „Schnell“), Chat „Neue regelbasierte Handelsstrategien 2025–2026 für Tagesdaten“, https://grok.com/c/90bb9a9d-fa26-4e31-aad0-7771df3cca2b, gesendet 16.10.2026, 07:58 vom steuernden Chat 30 nach Karte des Betreibers (Text sc/chat30/grok/SENDETEXT_grok_innovationen.txt, md5 188340ca…). Antwort per Skript aus dem Sitzungsprotokoll übernommen (get_page_text), nicht abgetippt; Grok nennt 65 Quellen, im Text stehen die Links der Funde. **Ungeprüft:** weder Quellen noch Zahlen sind nachgemessen; Prüfung durch Fable und eigene Websuche folgt (Betreiber 16.10.2026: „Beides und die Ergebnisse von fable prüfen lassen“). Kein Registertext, keine Vorregistrierung.*

---

Gearbeitet für 22s

Belegte Entwicklungen (letzte 12–18 Monate, Stand Okt. 2026)

Sortiert nach Belegstärke (OOS/Walk-Forward/Live + Kosten/Slippage > reine In-Sample-Claims). Maximal 8 Funde; Hype und reine Verkaufsseiten weggelassen. Klar getrennt: Belegtes vs. Behauptetes.

1. Simple Rule-Based vs. ML unter realistischen Annahmen (Earnings-Momentum & 52-Wochen-Hoch)

Kernidee: Einfache, interpretierbare Regeln (Earnings-Momentum; Nähe zum 52-Wochen-Hoch; Hybrid) werden gegen XGBoost und Benchmarks (Buy-and-Hold, Volatilitäts-gemanagter Markt) auf 39 Large-Cap-US-Aktien (2015–März 2026) getestet. Earnings-Momentum liefert den stärksten risk-adjusted Return (Sharpe 1,185, Newey-West t=4,49); ML zeigt OOS praktisch Zufallsniveau (AUC ≈ 0,51).

Quelle: Tay, Shu Shuang (NTU, 2026) – https://dr.ntu.edu.sg/entities/publication/26008d76-157e-4434-8117-488b269fabfe.

Belegstärke: Realistische Umsetzung (Next-Day-Execution, 8 bp Transaktionskosten, 100 % Gross-Exposure-Cap). OOS-Klassifikation für ML schwach; Regeln robuster. Kein volles Walk-Forward dokumentiert, aber strenge Constraints.

Passt zu Tagesdaten/regelbasiertem Bot: Ja – klar regelbasiert, Daily-Daten, US-Aktien/ETFs-kompatibel, kein ML-Blackbox.

2. Systematische Evaluation Turtle Trend-Following (Original + Modifikationen)

Kernidee: Klassische Turtle-Breakout-Regeln (20-/55-Tage-Donchian) und Varianten (Long-only, 200-Tage-MA-Filter, reduziertes Risiko, Profit-Harvesting, Volatilitäts-Sizing) werden auf Futures (2004–2026) und Krypto-Korb (2016–2026) geprüft. Original schwach (hohe DD); modifizierte Version verbessert CAGR (Futures ~21 %, Krypto ~38,7 %) und halbiert Drawdowns relativ zum Original/Buy-and-Hold.

Quelle: Bilal Khan, SSRN (Okt. 2025/2026) – https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7573918; Zusammenfassung via QuantifiedStrategies (Okt. 2026).

Belegstärke: Lange Perioden, Cross-Asset-Transfer, Regime-Filter/Volatilitäts-Konditionierung. Kosten implizit berücksichtigt (realistische Futures/Krypto); kein explizites Live, aber robuste OOS-artige Splits.

Passt: Ja – klassisch regelbasiert, Daily/4h optimal, direkt Turtle-Soup/Breakout-nah, Krypto + Futures/Aktien übertragbar.

3. Do Simple Technical Trading Rules Survive Realistic Costs? (Walk-Forward + Deflated Sharpe)

Kernidee: MA-, Breakout-Trend-, RSI(2)-Mean-Reversion- und Opening-Range-Breakout-Regeln auf S&P 500/ASX 200 (Daily 1996–2026) und 5-Min-Daten. Nach Kosten/Financing unterperformen alle Buy-and-Hold absolut; Breakout-Trend erreicht höheren Sharpe (0,60 vs. 0,49) und deutlich niedrigeres DD (−4,9 % vs. −57 %), überlebt Deflated-Sharpe/Multiple-Testing, liefert aber nur ~0,4 % CAGR nach Financing. Mean-Reversion und Intraday ohne signifikanten Edge.

Quelle: Udaya Wijesinghe, SSRN (Juni 2026) – https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6977700.

Belegstärke: Walk-Forward, Deflated Sharpe, Bootstrap, Monte-Carlo, explizite CFD-Kosten/Leverage. Sehr streng.

Passt: Ja – RSI-2 und Breakout direkt relevant, Daily-Daten, rein regelbasiert.

4. KSE Sentinel – Rule-Based Trend-Continuation (PSX)

Kernidee: Mechanische Regel: zwei aufeinanderfolgende Kerzen gleicher Richtung, die auf der „richtigen“ Seite einer kurzen EMA schließen; Exit-Strenge abhängig vom Trend-Regime. 30-Symbol-Universum, ~1009 Trades (2021–2026).

Quelle: Ertiza Abbas, SSRN (Juli 2026) – https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7093159.

Belegstärke: Netto nach realistischen Kosten (22,5 bp pro Leg inkl. Slippage/Spread); OOS gegen 2000–2020-Archiv; laufendes 60-Tage-Live-Paper-Trading (ab Juli 2026) mit dokumentierten Incidents. Sharpe ~2,08, Max-DD 2,91 %, Profit-Factor 2,51.

Passt: Bedingt ja – klar regelbasiert, Daily-fähig; Markt (Pakistan) abweichend von US/EU/Krypto, aber Methodik (Regime + mechanische Regeln) übertragbar.

5. QuantifiedStrategies Algorithmic Trading Strategies 2026 (Multi-Rule-Set)

Kernidee: Fünf klar definierte Daily-Regeln (u. a. Decline-from-High mit 25-Tage-Range-Band; Turnaround-Tuesday-ähnlich; weitere Mean-Reversion/Momentum-Varianten) auf S&P-ähnlichen Daten; kombiniert ~11,5 % CAGR bei niedriger Investitionsquote.

Quelle: Oddmund Groette / QuantifiedStrategies (aktualisiert März 2026) – https://www.quantifiedstrategies.com/algorithmic-trading-strategies-backtests/.

Belegstärke: Lange Backtests mit expliziten Regeln und Charts bis 2026; Kosten nicht immer detailliert ausgewiesen, aber Praktiker-Ansatz mit Fokus auf Robustheit statt Overfitting. Kein akademisches OOS/Walk-Forward im strengen Sinne.

Passt: Ja – rein regelbasiert, Daily, Mean-Reversion/Breakout-nah, US-Aktien/ETFs.

6. Opening-Range-Breakout Robustheitstest (225 Konfigurationen)

Kernidee: Systematischer Test von 225 Opening-Range-Breakout-Varianten auf 9 liquiden US-Futures (1-Min-Daten 2010–2025). Nach realistischen Kosten (Kommissionen, Spreads, Slippage) bleibt keine profitabel.

Quelle: QuantifiedStrategies-Zusammenfassung (Okt. 2026) eines Forschungs-Tests – X-Post verweist auf prüfbare Methodik.

Belegstärke: Sehr hohe Parameter-Robustheit + explizite Kosten; Ergebnis negativ (wichtig als Warnung). Intraday-Daten, daher nur bedingt Daily-relevant.

Passt: Nein (für reines Daily-System) – Intraday/Opening-Range; zeigt aber, dass Breakout-Regeln nach Kosten oft kollabieren.

7. Regime-Adaptive Framework (Trend/Momentum/Mean-Reversion)

Kernidee: Regelbasierter Regime-Klassifikator steuert zwischen Trend-Following, Momentum und Mean-Reversion auf indischen Large-Caps (2021–2024); feste Fractional-Risk-Management. Positive Nominalreturns, aber unter Benchmark, negative Sharpe relativ zum risikofreien Zins.

Quelle: Vaibhav Prakhar, SSRN (Mai 2026) – https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6769178.

Belegstärke: Modular, realistische Stop-Logik (Intraday-Lows); begrenzte Periode, kein starkes OOS.

Passt: Ja – regelbasiert, Daily-fähig, multi-Strategy-Switching relevant für dein 9-Bot-System.

8. Bias/Mean-Reversion-Filter-Vergleich (Bitcoin Daily)

Kernidee: Einfache Bias(20)-Mean-Reversion vs. Version mit zusätzlichen RSI/ATR-Filtern auf BTC Daily (2021–2026). Gefilterte Version verbessert Return und senkt DD, bleibt aber hinter Buy-and-Hold.

Quelle: Coinquant (Okt. 2026) – https://www.coinquant.ai/blog/simple-vs-complex-crypto-trading-strategy-backtest.

Belegstärke: Matched Backtest, wenige Trades → begrenzte statistische Power; Kosten berücksichtigt. Kein Walk-Forward.

Passt: Ja – Daily, regelbasiert, Krypto-Mean-Reversion (RSI-ähnlich).

Belegtes vs. Behauptetes

Belegt sind vor allem die negativen oder relativierenden Befunde (Kosten fressen Edges, einfache Regeln oft robuster als ML, Turtle-Modifikationen verbessern DD) sowie die strengen Walk-Forward/Deflated-Sharpe-Tests. Positive CAGRs und hohe Sharpes sind meist In-Sample oder auf spezifischen Universen; Live-Paper-Ergebnisse (KSE) und echte OOS-Klassifikation (Tay) sind rar. Viele „2026-Updates“ von Praktiker-Seiten wiederholen ältere Regeln ohne neue Robustheits-Checks.

Zwei Funde, die ich für eine Vorregistrierung am ehesten prüfen würde

Tay 2026 (Earnings-Momentum + 52-Wochen-Hoch unter realistischen Kosten) – klare Regeln, US-Aktien, Kosten explizit, ML als Kontrolle.
Khan Turtle-Evaluation 2026 – direkte Relevanz zu Turtle Soup/Breakout, Cross-Asset (inkl. Krypto), dokumentierte Modifikationen und Regime-Filter.

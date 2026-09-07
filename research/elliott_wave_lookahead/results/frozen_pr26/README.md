# Eingefrorene Trade-Sätze aus PR #26

Diese beiden CSVs sind die Ausgabe der **damals noch unkorrigierten**
`strategies/<bot>/equity_simulation.collect_all_trades` — also des
Backtests **mit** beiden Look-Ahead-Kanälen.

Sie liegen hier, weil dieses Verhalten im Bot-Code nicht mehr existiert:
`backtest_elliott.py` und `multi_symbol_optimise.py` wurden inzwischen
korrigiert (Einstieg zum Bestätigungskurs, kausale Wellenerkennung). Ohne
diese Dateien gäbe es keinen unabhängigen Bezugspunkt mehr, gegen den sich
der Nachbau in `run_one_bot.py` prüfen lässt.

`verify_baseline.py` vergleicht den Nachbau Trade für Trade gegen genau
diese Dateien. Damals lief derselbe Vergleich gegen den lebenden Bot-Code
und ging bei allen 1302 Trades ohne Abweichung durch — nachzulesen in der
PR-Beschreibung von #26.

**Nicht verändern.** Sie sind ein historischer Beleg, kein Zwischenstand.

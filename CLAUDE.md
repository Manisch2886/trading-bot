# Trading-Bot-Projekt

**Vor jeder Arbeit an diesem Repo zuerst lesen:** [`docs/UEBERGABEPROTOKOLL.md`](docs/UEBERGABEPROTOKOLL.md)

Das Übergabeprotokoll ist die verbindliche Grundlage für dieses Projekt. Es enthält Architektur, Strategie-Logik, validierte Live-Parameter, getroffene Entscheidungen (inkl. Begründung), etablierte Methodik-Prinzipien und offene Punkte. Änderungen an Strategien, Parametern oder Architektur sollen konsistent mit den dort dokumentierten Prinzipien (Abschnitt 7) erfolgen und die dortigen Entscheidungen (Abschnitt 8) nicht ohne triftigen, dokumentierten Grund revidieren.

## Kurzüberblick

Drei unabhängige, regelbasierte (kein ML) Paper-Trading-Bots, die per Cronjob laufen:

| Bot | Ordner | Markt | Zeitrahmen |
|---|---|---|---|
| Elliott Wave (Krypto) | `strategies/elliott_wave/` | 25 Top-Volumen-Kryptos | 1h |
| T3/ADX/SuperTrend (Krypto) | `strategies/t3_supertrend/` | dieselben 25 Kryptos | 4h |
| Elliott Wave (Aktien) | `strategies/elliott_wave_stocks/` | Top 150 S&P-500-Werte | 1 Tag |

Gemeinsame Infrastruktur in `shared/` (inkl. drei Claude-API-Agenten — rein informativ, verändern nie automatisch Parameter oder Trades) und `config/`. Details siehe Übergabeprotokoll.

**Wichtige Grundregeln:**
- Live-Trading mit echtem Kapital ist NICHT implementiert (nur Paper-Trading/Forward-Testing).
- Kein Agent darf automatisch `live_params.py` ändern oder Trades auslösen — Parameterübernahme bleibt manuell.
- Neue Parameter/Strategien immer per Backtest → Walk-Forward → Equity-Simulation → Buy-and-Hold-Vergleich validieren, bevor sie als "live" gelten (siehe Protokoll Abschnitt 7).
- `config/email_config.py` und `shared/fetch_binance_data.py` enthalten Zugangsdaten und sind absichtlich in `.gitignore` — niemals Klartext-Secrets committen. Bei Dateiinhalten mit Zugangsdaten `grep -c` statt `cat` verwenden.

Offene Punkte und der aktuelle Arbeitsstand stehen in Abschnitt 9 und 10 des Übergabeprotokolls.

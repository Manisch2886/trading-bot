# Trading-Bot-Projekt

**Vor jeder Arbeit an diesem Repo zuerst lesen:** [`docs/UEBERGABEPROTOKOLL.md`](docs/UEBERGABEPROTOKOLL.md)

Das Übergabeprotokoll ist die verbindliche Grundlage für dieses Projekt. Es enthält Architektur, Strategie-Logik, validierte Live-Parameter, getroffene Entscheidungen (inkl. Begründung), etablierte Methodik-Prinzipien und offene Punkte. Änderungen an Strategien, Parametern oder Architektur sollen konsistent mit den dort dokumentierten Prinzipien (Abschnitt 7) erfolgen und die dortigen Entscheidungen (Abschnitt 8) nicht ohne triftigen, dokumentierten Grund revidieren.

## Kurzüberblick

**Neun** unabhängige, regelbasierte (kein ML) Paper-Trading-Bots, die per Cronjob laufen:

| Bot | Ordner | Markt | Zeitrahmen |
|---|---|---|---|
| Elliott Wave (Krypto) | `strategies/elliott_wave/` | 25 Top-Volumen-Kryptos | 1h |
| T3/ADX/SuperTrend (Krypto) | `strategies/t3_supertrend/` | dieselben 25 Kryptos | 4h |
| RSI-2 (Krypto) | `strategies/rsi2_crypto/` | Kryptos | 1 Tag |
| Turtle Soup (Krypto) | `strategies/turtle_soup_crypto/` | Kryptos | 1 Tag |
| Volatility Breakout (Krypto) | `strategies/volatility_breakout_crypto/` | Kryptos | 1 Tag |
| Elliott Wave (Aktien) | `strategies/elliott_wave_stocks/` | Top 150 S&P-500-Werte | 1 Tag |
| RSI-2 Mean Reversion (Aktien) | `strategies/rsi2_mean_reversion/` | S&P-500-Auswahl | 1 Tag |
| Turtle Soup (Aktien) | `strategies/turtle_soup_stocks/` | S&P-500-Auswahl | 1 Tag |
| Volatility Breakout (Aktien) | `strategies/volatility_breakout/` | S&P-500-Auswahl | 1 Tag |

Gemeinsame Infrastruktur in `shared/` (inkl. **vier** Claude-API-Agenten plus Quartals-Interpreter — rein informativ, verändern nie automatisch Parameter oder Trades) und `config/`. Dazu zwei rein lesende Beobachtungsebenen: `notifications/` (Telegram-Bot) und `dashboard/` (Web/PWA). Abgeschlossene Untersuchungen liegen unter `research/`, je mit eigenem `BERICHT.md`. Details siehe Übergabeprotokoll.

**Wichtige Grundregeln:**
- Live-Trading mit echtem Kapital ist NICHT implementiert (nur Paper-Trading/Forward-Testing).
- Kein Agent darf automatisch `live_params.py` ändern oder Trades auslösen — Parameterübernahme bleibt manuell.
- Neue Parameter/Strategien immer per Backtest → Walk-Forward → Equity-Simulation → Buy-and-Hold-Vergleich validieren, bevor sie als "live" gelten (siehe Protokoll Abschnitt 7).
- Untersuchungen unter `research/` fassen **keinen** Bot-Code an; Parameterübernahme ist immer ein getrennter, ausdrücklich freigegebener Schritt.
- Jeder Handelsparameter steht genau einmal (in `live_params.py`) und wird überall sonst importiert — doppelt geführte Zahlen sind hier schon einmal unbemerkt auseinandergelaufen.
- `config/email_config.py` und `shared/fetch_binance_data.py` enthalten Zugangsdaten und sind absichtlich in `.gitignore` — niemals Klartext-Secrets committen. Bei Dateiinhalten mit Zugangsdaten `grep -c` statt `cat` verwenden.

Offene Punkte und der aktuelle Arbeitsstand stehen in Abschnitt 9 und 10 des Übergabeprotokolls.

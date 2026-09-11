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

Gemeinsame Infrastruktur in `shared/` (inkl. **vier** Claude-API-Agenten plus Quartals-Interpreter — rein informativ, verändern nie automatisch Parameter oder Trades) und `config/`. Dazu zwei Beobachtungsebenen: `notifications/` (Telegram-Bot, **rein lesend**) und `dashboard/` (Web/PWA, **liest und schreibt** — siehe unten). Zwei Broker-Brücken liegen unter `broker/`, Systemdienste unter `system/`. Abgeschlossene Untersuchungen liegen unter `research/`, je mit eigenem `BERICHT.md`. Details siehe Übergabeprotokoll.

## ⚠️ `broker/` — echte Orders an echte Gegenstellen

Unter `broker/` liegt der **einzige Code des Projekts, der Orders an eine externe Gegenstelle sendet**. Kein Bot tut das, kein Agent tut das — nur diese beiden Brücken:

| Brücke | Spiegelt | Gegenstelle | Stand |
|---|---|---|---|
| `broker/spiegel.py` | `t3_supertrend` | Binance **SPOT-Testnet** (virtuelles Guthaben) | produktiv, Cronjob alle 4 h zur Minute 5 |
| `broker/ibkr_spiegel.py` | `volatility_breakout` | **IBKR-Paper-Konto** über lokale TWS | gemergt, aber **nie gegen eine echte TWS gelaufen** |

**Grundregeln für jede Sitzung:**

- **`--echt` wird NIE ohne ausdrückliche Zustimmung des Nutzers aufgerufen.** Der Standard ist der Trockenlauf; `--echt` sendet wirklich. Das gilt auch dann, wenn eine Aufgabe es nahezulegen scheint.
- Beide Gegenstellen sind **Test- bzw. Paper-Umgebungen ohne echtes Geld**. Der Endpunkt steht jeweils als Literal im Code, die echten Handelsendpunkte stehen namentlich auf Verbotslisten. Das bleibt so.
- **Notbremse**: `touch broker/STOP` (Binance) bzw. `touch broker/STOP_IBKR` (IBKR) stoppt jede Order. Sie wird auf **drei** Ebenen geprüft: zu Beginn jedes echten Laufs, je Aufgabe und in der Orderfunktion selbst.
- Die Brücken lesen die Bot-Datenbanken über den gemeinsamen, schreibgeschützten Leser `broker/bot_db.py` (`mode=ro`). Sie fassen **keinen** Bot-Code an.
- **Bekannte Einschränkung:** `ib_async` verlangt Python 3.10+, auf dem Rechner des Nutzers läuft 3.9.6. Die IBKR-Brücke ist dort derzeit **nicht lauffähig**.

Einzelheiten: `broker/README.md` und `broker/README_IBKR.md`, Übergabeprotokoll Abschnitt 4.4.

**Wichtige Grundregeln:**
- Live-Trading mit echtem Kapital ist NICHT implementiert (nur Paper-Trading/Forward-Testing). Die beiden Broker-Brücken unter `broker/` senden Orders, aber ausschliesslich an Testnet bzw. Paper-Konto — siehe Abschnitt oben.
- Das **Dashboard ist seit PR #62/#71 nicht mehr rein lesend**: es kann Positionen manuell schliessen (alle neun Bots, doppelte Bestätigung) und bei geschlossener Börse **Warteaufträge** anlegen, die ein Cronjob später **ohne erneute Rückfrage** ausführt. Der Telegram-Bot bleibt rein lesend.
- Abhängigkeiten stehen in `requirements.txt` (bindet `notifications/` und `dashboard/` ein, ergänzt den Börsenkalender); `broker/requirements.txt` ist separat.
- Kein Agent darf automatisch `live_params.py` ändern oder Trades auslösen — Parameterübernahme bleibt manuell.
- Neue Parameter/Strategien immer per Backtest → Walk-Forward → Equity-Simulation → Buy-and-Hold-Vergleich validieren, bevor sie als "live" gelten (siehe Protokoll Abschnitt 7).
- **Bei Auswertungen und Backtests zuerst `docs/DATENLUECKEN.md` ansehen.** Cron holt verpasste Läufe nicht nach; dort steht, für welche Zeiträume Forward-Test-Daten lückenhaft sind. Eine Lücke sieht in den Zahlen genauso aus wie "kein Signal" und fällt sonst nicht auf.
- Untersuchungen unter `research/` fassen **keinen** Bot-Code an; Parameterübernahme ist immer ein getrennter, ausdrücklich freigegebener Schritt.
- Jeder Handelsparameter steht genau einmal (in `live_params.py`) und wird überall sonst importiert — doppelt geführte Zahlen sind hier schon einmal unbemerkt auseinandergelaufen.
- `config/email_config.py` und `shared/fetch_binance_data.py` enthalten Zugangsdaten und sind absichtlich in `.gitignore` — niemals Klartext-Secrets committen. Bei Dateiinhalten mit Zugangsdaten `grep -c` statt `cat` verwenden.

Offene Punkte und der aktuelle Arbeitsstand stehen in Abschnitt 9 und 10 des Übergabeprotokolls.

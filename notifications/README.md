# Telegram-Bot fuer das Trading-System (Phase 1 - Lesen + Benachrichtigungen)

Eigenstaendiger, rein lesender Dienst. Fasst die neun bestehenden
Paper-Trading-Bots unter `strategies/` nicht an - liest nur ihre
Live-Datenbanken (`paper_trading_<bot>.db`, read-only geoeffnet) und
ihre Cronjob-Logs (`logs/<bot>/*.log`). Bot-Name in Telegram:
`Manisch_TradeSignal_Bot`.

Nicht Teil dieser Phase: schreibender Zugriff (z.B. Positionen ueber
Telegram schliessen) - kommt erst in Phase 3.

## Struktur

| Datei | Zweck |
|---|---|
| `telegram_bot.py` | Haupt-Script: Befehle entgegennehmen, periodisch `monitor.py` abfragen |
| `telegram_config.py` | liest `TELEGRAM_BOT_TOKEN` + `TELEGRAM_USER_ID` aus `.env` |
| `notify.py` | `send_alert(text)` - von jedem anderen Script importierbar, keine Extra-Abhaengigkeit |
| `monitor.py` | liest die neun Bot-DBs/-Logs, erkennt neue Trades/Stop-Loss/Fehler, liefert die Daten fuer `/status`, `/positions`, `/pnl` |

## Einrichtung

1. **Abhaengigkeit installieren** (nur fuer `telegram_bot.py` noetig,
   `notify.py`/`monitor.py` kommen ohne diese Abhaengigkeit aus):
   ```
   pip3 install -r notifications/requirements.txt
   ```
2. **`.env` im Projekt-Root pruefen** (bereits vorhanden laut Vorgabe) -
   muss enthalten:
   ```
   TELEGRAM_BOT_TOKEN=<Token von @BotFather>
   TELEGRAM_USER_ID=<deine numerische Telegram-User-ID, z.B. von @userinfobot>
   ```
   `.env` steht in `.gitignore` - niemals committen. Zum Pruefen, OHNE
   den Token im Terminal anzuzeigen:
   ```
   grep -c TELEGRAM_BOT_TOKEN .env
   grep -c TELEGRAM_USER_ID .env
   ```
   (Erwartete Ausgabe jeweils `1`.)
3. **Manuell testen** (im Vordergrund, `Strg+C` zum Beenden):
   ```
   python3 notifications/telegram_bot.py
   ```
   Dann in Telegram an `Manisch_TradeSignal_Bot` `/status` schicken.
4. **Als launchd-Dienst einrichten** (dauerhafter Betrieb, siehe
   `com.manisch.telegram-tradesignal-bot.plist` fuer Details/Pfade-Check):
   ```
   cp notifications/com.manisch.telegram-tradesignal-bot.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.manisch.telegram-tradesignal-bot.plist
   ```
   Stoppen: `launchctl unload ~/Library/LaunchAgents/com.manisch.telegram-tradesignal-bot.plist`

## Befehle (nur `TELEGRAM_USER_ID` wird akzeptiert)

- `/status [filter]` - Kurzueberblick: letzter Lauf, offene Positionen, Tages-PnL
- `/positions [filter]` - offene Positionen, gruppiert nach Krypto/Aktien
- `/pnl [filter]` - Performance-Zusammenfassung (Win Rate, Ø PnL, Summe PnL)

`filter` ist optional: `krypto`, `aktien`, oder ein konkreter Bot-Name
(z.B. `elliott_wave`) - siehe `monitor.ASSET_CLASS` fuer alle neun
gueltigen Namen. Ohne Filter wird immer die Gesamtuebersicht gezeigt.

## Automatische Push-Benachrichtigungen

Laufen rund um die Uhr, ohne Ruhezeiten (bewusste Entscheidung - siehe
Absprache):
- Neuer Trade eroeffnet/geschlossen (mit Bot-Name, Symbol, Ergebnis)
- Stop-Loss ausgeloest (separat hervorgehoben)
- Cronjob-Fehler/Script-Abbruch (Traceback im Log) oder ein Bot, der
  deutlich laenger nicht gelaufen ist als fuer seinen Zeitrahmen zu
  erwarten waere

Poll-Intervall standardmaessig 300 Sekunden, ueberschreibbar per
Umgebungsvariable `TELEGRAM_POLL_INTERVAL_SECONDS`.

## Logs

Eigener Log unter `logs/notifications/telegram_bot.log` (rotierend),
getrennt von den bestehenden Bot-Logs unter `logs/<bot>/`. Der
launchd-Dienst selbst schreibt zusaetzlich `logs/notifications/launchd.out.log`
und `.err.log`. Keine dieser Log-Dateien enthaelt jemals den Bot-Token.

## Sicherheit

- `.env` darf niemals ins Repo gelangen (steht in `.gitignore`) und
  wird an keiner Stelle geloggt oder ausgegeben - `telegram_config.py`
  gibt bei fehlenden/ungueltigen Zugangsdaten nur `None` zurueck, nie
  den Inhalt.
- Nur `TELEGRAM_USER_ID` darf Befehle senden - jeder andere Absender
  wird ignoriert, aber mit seiner User-ID geloggt (siehe `restricted()`
  in `telegram_bot.py`).
- `monitor.py` oeffnet alle neun Bot-Datenbanken explizit read-only
  (SQLite-URI-Modus `mode=ro`) - selbst ein Programmierfehler kann
  dadurch keine der neun Live-Datenbanken veraendern.

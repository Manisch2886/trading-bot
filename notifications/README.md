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

**Wo nachschauen:** Alle Log-Ausgaben von `telegram_bot.py` (Start-Meldung,
Warnungen, Fehler aus `error_handler()`/`_reply_for_selector()`) erscheinen
seit dem /pnl-Diagnose-Fix an **zwei** Stellen gleichzeitig:
1. **Direkt im Terminal** (Konsole), wenn der Bot manuell im Vordergrund
   laeuft (`python3 notifications/telegram_bot.py`) - das ist der
   richtige Ort fuer einen manuellen Live-Test.
2. **`logs/notifications/telegram_bot.log`** (rotierend) - fuer den
   dauerhaften launchd-Betrieb, wo niemand ein Terminal offen haelt.

(Vorher gab es nur (2) - dadurch blieb ein Fehler beim manuellen Testen
im Terminal komplett unsichtbar, obwohl er korrekt geloggt wurde.)

Seit dem neuesten Fix gilt das auch fuer interne Meldungen von
`python-telegram-bot`/`httpx` selbst (z.B. `Conflict: terminated by
other getUpdates request` - siehe naechster Absatz), nicht nur fuer
unsere eigenen Log-Zeilen.

## WICHTIG vor jedem Neustart: nur EIN Bot-Prozess darf laufen

Telegram erlaubt pro Bot-Token nur EINEN aktiven Long-Poller
gleichzeitig. Laeuft noch ein alter Prozess (z.B. von einem vorherigen
Test, der nicht sauber mit `Strg+C` beendet wurde) im Hintergrund,
antwortet der Bot auf GAR KEINEN Befehl mehr - der neue Prozess laeuft
zwar (sichtbar in `ps aux`, mit etwas CPU-Zeit durch wiederholte
Verbindungsversuche), bekommt aber nie Updates zugeteilt.

**Vor jedem Neustart pruefen:**
```
pgrep -fl telegram_bot.py
```
Falls das MEHR als einen Prozess zeigt: alle mit `kill <PID>` beenden,
dann `pgrep -fl telegram_bot.py` erneut ausfuehren bis die Liste leer
ist, und erst DANACH `python3 notifications/telegram_bot.py` neu
starten.

Getrennt von den bestehenden Bot-Logs unter `logs/<bot>/`. Der
launchd-Dienst selbst schreibt zusaetzlich `logs/notifications/launchd.out.log`
und `.err.log`. Keine dieser Log-Dateien enthaelt jemals den Bot-Token.

## Netzwerk-Diagnose (falls der Bot trotz laufendem Prozess auf gar nichts reagiert)

Der komplette Code (echte `Application`, echtes `run_polling()`, echte
`JobQueue` mit echtem `poll_job()`-Lauf) wurde gegen einen echten
lokalen HTTP-Server Ende-zu-Ende getestet und funktioniert dort
nachweislich fehlerfrei. Bleibt der Bot live trotzdem stumm, ist der
naechstliegende Verdacht KEIN Code-Fehler mehr, sondern eine
Netzwerk-Eigenheit zwischen diesem Mac und `api.telegram.org`, die
`httpx` (von `python-telegram-bot` genutzt) anders behandelt als
`curl` - z.B. ein System-Proxy, eine TLS-inspizierende
Sicherheits-Software/VPN, oder ein IPv4/IPv6-Unterschied.

**Fuer GENAU EINEN Testlauf** (nicht dauerhaft einbauen - sehr
gespraechig):
```
TELEGRAM_DEBUG_HTTP=1 python3 notifications/telegram_bot.py
```
Zeigt jede HTTP-Verbindung von `httpx`/`httpcore`/`telegram` im Detail
(Verbindungsaufbau, Request, Response) - so laesst sich unterscheiden
zwischen "es wird ueberhaupt keine Verbindung zu Telegram versucht" und
"eine Verbindung wird versucht, haengt aber an einer bestimmten
Stelle" (z.B. TLS-Handshake, DNS-Aufloesung).

**Zum Vergleich hilfreich:**
```
curl -v "https://api.telegram.org/bot<TOKEN>/getUpdates"
```
Falls `curl -v` z.B. eine andere IP-Adresse, einen Proxy, oder ein
anderes TLS-Verhalten zeigt als die `TELEGRAM_DEBUG_HTTP=1`-Ausgabe,
ist das ein starker Hinweis auf eine Netzwerk-/Sicherheits-Software-
Eigenheit auf diesem Mac, die spezifisch `httpx` betrifft - nicht auf
einen Fehler in diesem Code.

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

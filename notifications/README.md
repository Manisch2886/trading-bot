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

1. **Abhaengigkeiten installieren:**
   ```
   pip3 install -r notifications/requirements.txt
   ```
   (`python-telegram-bot` fuer `telegram_bot.py`; `requests` und
   `yfinance` fuer die Live-Kursabfrage in `monitor.py`, siehe Abschnitt
   "Live-Kurse in /status" unten. `notify.py` kommt weiterhin ohne
   Extra-Abhaengigkeit aus - reine Standardbibliothek.)
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

- `/status [filter]` - je Bot: letzter Lauf, Anzahl offener Positionen,
  Tages-PnL, KUMULIERTER PnL (alle geschlossenen Trades), sowie je
  offener Position Symbol/Entry/Stop und der AKTUELLE Gewinn/Verlust in
  % (Live-Kurs via Binance-API fuer Krypto-Bots, yfinance fuer
  Aktien-Bots - siehe Abschnitt "Live-Kurse in /status" unten)
- `/positions [filter]` - offene Positionen, gruppiert nach Krypto/Aktien
  (nur Symbol-Liste, KEINE Live-Kurse - siehe `/status` dafuer)
- `/pnl [filter]` - Performance-Zusammenfassung (Win Rate, Ø PnL, Summe PnL)

`filter` ist optional: `krypto`, `aktien`, oder ein konkreter Bot-Name
(z.B. `elliott_wave`) - siehe `monitor.ASSET_CLASS` fuer alle neun
gueltigen Namen. Ohne Filter wird immer die Gesamtuebersicht gezeigt.

## Live-Kurse in /status

Fuer jede aktuell offene Position ruft `/status` den AKTUELLEN Kurs ab
und zeigt den Gewinn/Verlust seit Entry in %:
- **Krypto-Bots:** oeffentlicher, unauthentifizierter Binance-Endpunkt
  `GET /api/v3/ticker/price?symbols=[...]` - EIN gebuendelter Request
  fuer ALLE offenen Krypto-Positionen ueber alle Bots hinweg (nicht
  einer pro Symbol). Kein API-Key noetig. Rate-Limit bei der hier zu
  erwartenden Nutzung (gelegentliche manuelle `/status`-Aufrufe, nicht
  automatisiert) nicht relevant - siehe Kommentar bei
  `monitor.fetch_binance_prices()` fuer die Einordnung.
- **Aktien-Bots:** `yfinance` (`yf.download()` mit mehreren Tickern in
  einem Aufruf), letzter verfuegbarer Tages-Schlusskurs.

**Fehlertoleranz:** Schlaegt eine Kursabfrage fehl (Netzwerkfehler,
unbekanntes Symbol, Zeitueberschreitung), zeigt die betroffene Position
"Preis nicht verfuegbar" - der Rest der `/status`-Antwort (kumulierter
PnL, alle anderen Positionen) bleibt davon unberuehrt. Die komplette
Kursabfrage hat eine harte Gesamt-Obergrenze von 12 Sekunden
(`LIVE_PRICE_TIMEOUT_SECONDS` in `telegram_bot.py`) - danach zeigt
`/status` alle Positionen ohne Live-Kurs, statt beliebig lange zu warten.

**Event-Loop-Sicherheit:** Die Binance-/yfinance-Abfragen sind ECHTE,
blockierende synchrone Netzwerk-Aufrufe (wie schon `notify.send_alert()`
zuvor) - sie laufen deshalb IMMER ueber `asyncio.to_thread()`, NIE
direkt in einer async-Funktion. Siehe die ausfuehrlichen Kommentare in
`status_command()` (`telegram_bot.py`) und `fetch_live_prices_for_bots()`
(`monitor.py`) - ein einziger uebersehener Blocking-Call an dieser
Stelle hatte den Bot bereits einmal komplett eingefroren (siehe
Git-Historie).

**Nachrichtenlaenge:** Mit Live-Kursen fuer viele Bots/Positionen kann
die volle `/status`-Antwort Telegrams 4096-Zeichen-Limit pro Nachricht
ueberschreiten - `format_status_message()` teilt die Ausgabe in diesem
Fall automatisch in mehrere aufeinanderfolgende Nachrichten auf
(Sicherheitsmarge: `MAX_MESSAGE_LENGTH = 3500` Zeichen pro Nachricht in
`monitor.py`). `/positions` und `/pnl` sind davon nicht betroffen -
schicken weiterhin immer genau eine Nachricht.

**Sandbox-Einschraenkung (Transparenz):** Diese Aenderung wurde OHNE
echten Netzwerkzugriff auf die Binance-API oder Yahoo Finance
entwickelt/getestet - die Entwicklungsumgebung hat keinen Netzwerk-Egress
zu diesen externen APIs (`curl` gegen beide liefert hier keine
Verbindung). Verifiziert wurde deshalb ausschliesslich mit gemockten
Kursdaten (siehe Tests).

**Bereits im Live-Test gefunden und behoben:** `fetch_binance_prices()`
lieferte anfangs fuer JEDE echte Krypto-Position "Preis nicht
verfuegbar", obwohl `curl` auf demselben Mac problemlos funktionierte -
Netzwerk/Firewall waren also nicht die Ursache. Root Cause: `requests`
kodiert ein Leerzeichen in einem Query-Parameter als `+`
(form-urlencoded-Konvention), `json.dumps()` fuegt aber standardmaessig
nach jedem Komma ein Leerzeichen ein - die tatsaechlich gesendete URL
enthielt dadurch ein woertliches `+` MITTEN im `symbols`-JSON-Array.
Behoben durch `separators=(",", ":")` beim `json.dumps()`-Aufruf
(erzeugt exakt Binances dokumentiertes, leerzeichenfreies Format
`["BTCUSDT","BNBUSDT"]`). Fehlgeschlagene Kursabfragen werden jetzt
ausserdem ueber `logging` statt `print(..., file=sys.stderr)` geloggt
(`logging.getLogger("notifications.monitor")`, an dieselben Konsole-
und Datei-Handler wie alle anderen Bot-Logs angehaengt) - inkl. des
Response-Bodys bei einem HTTP-Fehler, damit ein aehnlicher stiller
Fehler kuenftig sofort sichtbar ist statt erst nach einer eigenen
Diagnose-Runde.

**"+0,0%" bei einzelnen Aktienpositionen:** erwartungsgemaess, kein Bug
- die Aktien-Bots handeln auf Tagesbasis und eroeffnen Positionen zum
Schlusskurs. Faellt der `/status`-Aufruf auf ein Wochenende oder eine
sehr frisch (noch am selben Handelstag) eroeffnete Position, liefert
`yfinance`s "letzter verfuegbarer Schlusskurs" exakt denselben Wert wie
der bereits bekannte `entry_price` - 0,0% ist dann schlicht korrekt.

**Weiterhin fuer den naechsten Live-Test auf dem Mac zu pruefen:** ob
die 12-Sekunden-Obergrenze im Alltag ausreicht (bei vielen gleichzeitig
offenen Positionen ggf. anpassen).

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

**TRACE-Breadcrumbs:** Jede Zeile mit `TRACE:` markiert einen Schritt
im Aufruf-Pfad eines Befehls (`restricted()`-Wrapper erreicht →
Autorisierung OK → `_reply_for_selector()` betreten →
`discover_bots()`/`filter_bots()` fertig → `formatter()` fertig → vor/
nach `reply_text()`). Bei einem erneuten "keine Antwort"-Fall zeigt
`grep TRACE logs/notifications/telegram_bot.log` (oder das Terminal)
GENAU, an welcher Stelle die Verarbeitung stehen geblieben ist - fehlt
z.B. sogar die allererste TRACE-Zeile ("restricted()-Wrapper erreicht"),
wurde der Handler von `python-telegram-bot` gar nicht erst aufgerufen
(Dispatch-Problem); erscheint sie, aber die naechste TRACE-Zeile fehlt,
haengt genau der Schritt dazwischen.

**Vor dem naechsten Test unbedingt verifizieren, dass der aktuelle Code
auch wirklich laeuft:**
```
git log -1 --format="%H %s" notifications/telegram_bot.py
grep -c "TRACE:" notifications/telegram_bot.py
```
(Die zweite Zeile sollte mehrere Treffer zeigen - falls 0, laeuft eine
aeltere Version der Datei.)

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

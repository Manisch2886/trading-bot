# Web-Dashboard (Phase 2) - rein lesend

Kleines Web-Dashboard fuer die neun Paper-Trading-Bots, installierbar auf
dem iPhone (PWA). Zeigt dieselben Daten wie der Telegram-Bot, nur
visuell aufbereitet: Uebersicht aller Bots, Verlaufsdiagramm, Detailseite
je Bot mit offenen Positionen und den letzten Trades.

**Rein lesend.** Es gibt keinen Endpunkt, der irgendetwas veraendert -
keine Moeglichkeit, eine Position zu schliessen, einen Parameter zu
setzen oder einen Bot zu starten. Das ist Phase 3 und ausdruecklich
nicht Teil dieser Anwendung. Die einzige Nicht-GET-Route ist
`POST /login`, die nur ein Cookie setzt. Die Bot-Datenbanken werden
ueber `notifications/monitor.py` im SQLite-Modus `ro` geoeffnet.

## Struktur

| Datei | Zweck |
|---|---|
| `server.py` | Start (uvicorn), Bindung an 127.0.0.1, Warnhinweise |
| `app.py` | FastAPI-App: Endpunkte, Token-Pruefung, Auslieferung des Frontends |
| `datenquelle.py` | duenne Leseschicht ueber `notifications/monitor.py` |
| `konfig.py` | Token/Host/Port aus `.env` bzw. Umgebung |
| `static/` | Frontend (HTML/CSS/JS), `manifest.json`, `sw.js`, Icons |
| `erzeuge_icons.py` | erzeugt die beiden PWA-Icons neu (keine Fremdbibliothek noetig) |
| `test_dashboard.py` | Selbsttests gegen den echten Server, synthetische Daten |

## Erste Inbetriebnahme (Schritt fuer Schritt)

1. **Abhaengigkeiten installieren**
   ```
   pip3 install -r dashboard/requirements.txt
   ```
   (FastAPI und uvicorn. `pandas` ist ueber die Bots schon da,
   `requests`/`yfinance` fuer die Live-Kurse kommen aus
   `notifications/requirements.txt` und sind fuer den Telegram-Bot
   bereits installiert.)

2. **Zugriffs-Token erzeugen**
   ```
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Token in die `.env` im Projekt-Root eintragen** (dieselbe Datei wie
   `TELEGRAM_BOT_TOKEN`, steht in `.gitignore`):
   ```
   DASHBOARD_ACCESS_TOKEN=<die eben erzeugte Zeichenfolge>
   ```
   Pruefen, ohne das Token im Terminal anzuzeigen:
   ```
   grep -c DASHBOARD_ACCESS_TOKEN .env
   ```
   (Erwartete Ausgabe: `1`.)

4. **Selbsttests laufen lassen** (dauert wenige Sekunden, fasst keine
   echten Daten an):
   ```
   python3 dashboard/test_dashboard.py
   ```
   Erwartet: `79/79 Pruefungen bestanden.`

5. **Dashboard starten** (laeuft im Vordergrund, `Strg+C` beendet):
   ```
   python3 dashboard/server.py
   ```
   Ausgabe nennt die Adresse, standardmaessig `http://127.0.0.1:8787/`.

6. **Im Browser oeffnen:** `http://127.0.0.1:8787/` - es erscheint die
   Anmeldeseite. Token einfuegen, "Anmelden". Danach merkt sich der
   Browser die Anmeldung ueber ein Cookie (90 Tage).

7. **Was zu sehen sein sollte:** oben die Kennzahlen-Kacheln (Anzahl
   Bots, offene Positionen, geschlossene Trades, heutiger PnL), darunter
   das Verlaufsdiagramm, darunter die Liste aller Bots. Ein Klick auf
   einen Bot fuehrt zur Detailseite. Die Spalte "Aktuell" (Live-Kurse)
   erscheint mit ein paar Sekunden Verzoegerung - das ist Absicht, siehe
   unten.

## Fernzugriff vom iPhone - noch NICHT nutzbar

Das Dashboard lauscht standardmaessig **nur auf 127.0.0.1**, ist also
ausschliesslich auf dem Mac selbst erreichbar. Der urspruengliche Plan
war, die Erreichbarkeit ueber das Tailscale-Netz zu regeln; **Tailscale/
SSH ist auf diesem Mac noch nicht eingerichtet** (eigener, offener
Punkt). Solange das so ist, gibt es keinen sinnvollen Weg, das
Dashboard sicher aus dem Netz erreichbar zu machen - deshalb bleibt es
bewusst lokal.

Sobald Tailscale laeuft, genuegt es, den Server an die Tailscale-Adresse
zu binden:
```
DASHBOARD_HOST=0.0.0.0 python3 dashboard/server.py
```
Der Start weist dann ausdruecklich darauf hin, dass das Dashboard im
Netzwerk erreichbar ist. Wer das VOR Tailscale tut, macht es allen
Geraeten im selben WLAN zugaenglich - dann ist das Token die einzige
Huerde. Es ist als zusaetzliche Verteidigungsebene gedacht, nicht als
Ersatz fuer die Netzwerkabsicherung.

## Zum Home-Bildschirm hinzufuegen (PWA)

Sobald das Dashboard vom iPhone aus erreichbar ist (siehe oben):
Safari oeffnen -> Adresse aufrufen -> anmelden -> Teilen-Symbol ->
"Zum Home-Bildschirm". Danach startet es wie eine eigenstaendige App
(eigenes Icon, ohne Safari-Leiste). Der Service Worker haelt nur die
Huelle (HTML/CSS/JS/Icons) im Cache - **Kurs- und PnL-Daten werden
niemals zwischengespeichert**, weil veraltete Zahlen, die aussehen wie
aktuelle, schlimmer waeren als gar keine.

Praktisch beim ersten Aufruf auf dem Telefon: die Adresse einmal mit
angehaengtem Token aufrufen
(`http://<adresse>:8787/?token=<token>`) - das setzt gleich das Cookie,
danach ist das Token nicht mehr noetig.

## Endpunkte (alle GET, alle lesend)

| Endpunkt | Zweck |
|---|---|
| `/api/health` | Lebenszeichen |
| `/api/portfolio` | alle Bots mit Kennzahlen (ohne Netzwerkzugriff) |
| `/api/portfolio?live=1` | dieselbe Uebersicht inkl. Live-Kursen der offenen Positionen |
| `/api/bots` | Kurzliste (Name, Anzeigename, Anlageklasse) |
| `/api/bots/{name}` | ein Bot: Kennzahlen, offene Positionen, letzte Trades |
| `/api/bots/{name}?live=1` | dito, mit aktuellen Kursen |
| `/api/bots/{name}/trades?limit=N` | geschlossene Trades, neueste zuerst |
| `/api/verlauf` | kumulierte Trade-Ergebnisse je Bot und zusammengefasst |
| `/api/live-kurse[?bot=name]` | nur die aktuellen Kurse der offenen Positionen |

Seiten: `/` (Uebersicht), `/bot?name=<bot>` (Detail), `/login`,
`/abmelden`, `/manifest.json`, `/sw.js`, `/statisch/*`.

## Warum die Live-Kurse getrennt geladen werden

Binance- und yfinance-Abfragen sind echte, blockierende
Netzwerkaufrufe. FastAPI laeuft asynchron in einem einzigen Event-Loop:
ein direkter Aufruf wuerde den gesamten Server fuer alle gleichzeitigen
Anfragen einfrieren, solange die langsamste Abfrage laeuft - genau der
Fehler, der den Telegram-Bot schon einmal komplett blockiert hat. Sie
laufen deshalb ausschliesslich ueber `asyncio.to_thread()`, mit einer
harten Obergrenze von 12 Sekunden (`asyncio.wait_for`). Laeuft die
Abfrage in einen Fehler oder ins Zeitlimit, antwortet der Endpunkt
trotzdem mit HTTP 200, einem leeren Kurs-Objekt und einem Hinweistext -
die Seite bleibt vollstaendig, nur ohne aktuelle Kurse.

Das Frontend laedt deshalb in zwei Schritten: erst die schnelle
Datenbank-Fassung (sofort sichtbar), dann im Hintergrund die Fassung
mit Live-Kursen.

## Was die Zahlen bedeuten (und was nicht)

- **Summe PnL** ist die Summe der Prozentergebnisse aller geschlossenen
  Trades eines Bots - Prozentpunkte, keine Rendite.
- **Aktuell** kommt aus derselben Funktion wie die Zeile "Aktuelles
  Gesamtergebnis" in `/status` in Telegram
  (`monitor._current_total_result`): kumulierter PnL der geschlossenen
  Trades plus der **Mittelwert** der Buchgewinne/-verluste der offenen
  Positionen.
- **Der Verlauf** ist die kumulierte Summe der Trade-Ergebnisse in
  Prozentpunkten, **keine Equity-Kurve**: die Bots speichern keine
  Positionsgroesse pro Trade, eine kapitalgewichtete Kurve laesst sich
  daraus nicht bilden. Geschlossene Trades ohne lesbares Ergebnis in der
  Datenbank gehen mit 0 ein und werden im Hinweistext gezaehlt, statt
  still zu verschwinden.
- Alles ist **Paper-Trading** - es ist kein echtes Kapital im Spiel.

## Getroffene Annahmen

1. **Fail closed statt "laeuft halt ohne Schutz":** Ohne gesetztes
   `DASHBOARD_ACCESS_TOKEN` startet der Server gar nicht. Ein
   versehentlich ungeschuetzt laufendes Dashboard wuerde man im Betrieb
   nicht bemerken.
2. **Mindestlaenge 16 Zeichen** fuer das Token, damit ein
   "test"-Token nicht versehentlich produktiv wird.
3. **Token auch per `?token=`**, nicht nur per Header: ohne das waere
   der erste Aufruf auf dem iPhone unnoetig umstaendlich. Der Wert
   landet dann einmalig in der Browser-Historie; das wurde gegen die
   Bedienbarkeit abgewogen und als vertretbar eingestuft, da es sich um
   ein Geraet des Nutzers handelt.
4. **Cookie ohne `secure`-Flag**, weil das Dashboard ueber `http://`
   auf localhost bzw. spaeter im Tailscale-Netz laeuft - mit `secure`
   wuerde der Browser es dort gar nicht erst setzen. `HttpOnly` und
   `SameSite=strict` sind gesetzt. Sobald es jemals ueber echtes HTTPS
   laeuft, gehoert `secure=True` in `app.py`.
5. **Kein Chart.js.** Statt einer externen Bibliothek zeichnet das
   Frontend das Liniendiagramm als SVG selbst (rund 60 Zeilen in
   `static/app.js`). Gruende: die PWA soll auch ohne Internet
   funktionieren (ein CDN-Skript waere dann weg), eine mitgelieferte
   Kopie waeren ~200 KB fremder Code im Repo, und gebraucht wird genau
   eine Linie ueber der Zeit.
6. **`shared/portfolio_overview.py` wird nicht verwendet.** Es startet
   je Bot einen eigenen Python-Subprozess und rekonstruiert
   Equity-Kurven - Laufzeit im Sekunden- bis Minutenbereich, fuer eine
   Web-Anfrage unbrauchbar. Das Dashboard nutzt dieselbe leichtgewichtige
   Kennzahlen-Logik wie der Telegram-Bot (`monitor.py`), damit beide
   nicht auseinanderlaufen.
7. **`monitor._read_trades` und `monitor._current_total_result` werden
   trotz fuehrendem Unterstrich benutzt.** Die Alternative waere eine
   zweite SQLite-Lese- und Kennzahlen-Logik gegen dieselben neun
   Live-Datenbanken gewesen - genau die Doppelfuehrung, die das Projekt
   an anderer Stelle schon Fehler gekostet hat. Dasselbe gilt fuer
   `telegram_config._parse_env_file`: es gibt genau eine `.env`, und
   zwei Parser wuerden frueher oder spaeter unterschiedlich mit
   Anfuehrungszeichen umgehen.
8. **Kein `python-multipart`.** Der Login-Formularkoerper wird mit
   `urllib.parse.parse_qs` gelesen; FastAPIs `Form(...)` haette dafuer
   ein zusaetzliches Paket verlangt.
9. **Kein Hintergrunddienst.** Kein launchd-Eintrag, kein Autostart -
   genau wie beim Telegram-Bot erst nach einem erfolgreichen manuellen
   Test, und dann als eigener Schritt.

## Bekannte Grenzen

- **Keine Ratenbegrenzung** an der Anmeldung. Bei einem zufaelligen
  Token mit 32 Byte Entropie ist Durchprobieren praktisch aussichtslos;
  ein kurzes, selbst ausgedachtes Token waere es nicht - deshalb die
  Mindestlaenge und die Empfehlung, `secrets.token_urlsafe(32)` zu
  benutzen.
- **Kein HTTPS.** Innerhalb von localhost bzw. eines Tailscale-Netzes
  ist der Verkehr ohnehin nicht oeffentlich; ueber ein fremdes Netz
  sollte das Dashboard nicht ohne TLS betrieben werden.
- **Die Live-Kurse konnten in der Entwicklungsumgebung nicht gegen die
  echten APIs geprueft werden** (kein Netzwerk-Egress zu Binance/Yahoo,
  dieselbe Einschraenkung wie beim Telegram-Bot). Getestet wurde mit
  gemockten Kursen inklusive Zeitueberschreitung und Fehlerfall; die
  Abrufe selbst sind unveraenderter, im Telegram-Betrieb bereits
  bewaehrter Code aus `monitor.py`.

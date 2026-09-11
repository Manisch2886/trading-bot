# Web-Dashboard - lesend, mit genau einer Ausnahme

Kleines Web-Dashboard fuer die neun Paper-Trading-Bots, installierbar auf
dem iPhone (PWA). Zeigt dieselben Daten wie der Telegram-Bot, nur
visuell aufbereitet: Uebersicht aller Bots, Verlaufsdiagramm, Detailseite
je Bot mit offenen Positionen und den letzten Trades.

**Hier stand bis zuletzt "rein lesend - es gibt keinen Endpunkt, der
irgendetwas veraendert".** Das gilt so nicht mehr, und der Satz soll nicht
stillschweigend falsch werden.

**Lesend, ausser einem einzigen Zweck:** offene Positionen von Hand
schliessen - in drei Abstufungen:

| Weg | Reichweite | Bestaetigung | Wo |
|---|---|---|---|
| einzeln | eine Position | EIN Tap | Bot-Detailseite |
| bot-weit | alle Positionen eines Bots | ZWEI Klicks | Bot-Detailseite |
| global (Crash) | alle Positionen ALLER Bots | ZWEI Klicks + Text `CRASH` | Uebersichtsseite |

Alle drei sind eng gefasst und teilen dieselbe Absicherung:

* nur fuer die Bots in `manual_close.SCHLIESSBARE_BOTS` - inzwischen alle
  neun. Jeder wurde davor EINZELN gegen sein `forward_test.py` geprueft
  (Schema, PnL-Formel, `result`-Werte), und die Pruefung laeuft bei jedem
  Testlauf erneut. Ein Bot, der nicht in der Liste steht, antwortet mit 403,
* nur ueber **zwei getrennte HTTP-Aufrufe** (`…/vorbereiten`, dann
  `…/ausfuehren`), der zweite mit einer zufaelligen, einmaligen, nach 120
  Sekunden verfallenden Vorgangs-Kennung, die nur fuer genau diesen Bot und
  diese Position(en) und diese Vorgangsart gilt. Ein einzelner Aufruf kann
  nichts schliessen - das ist die Absicherung. In der Oberflaeche ist es
  **ein Tap** fuer eine Position (die Zusammenfassung ist bereits der erste
  Aufruf) und **zwei Klicks** fuer alle - groessere Tragweite, deshalb eine
  zusaetzliche Rueckfrage. (Bis PR #62 war zusaetzlich der Text
  `BESTAETIGEN` einzutippen; das ist entfallen - Paper-Trading ohne echtes
  Kapital, und im schnellen Kryptomarkt kostet der Tippschritt Zeit. Die
  Telegram-Variante behaelt ihre zwei Stufen.)
* und nur ueber `notifications/manual_close.py` - dasselbe Modul, das auch
  die Telegram-Variante benutzt, mit Transaktion, Nebenlaeufigkeits-
  Absicherung und eigenem Protokoll. Auch der Notfallweg ruft dort je
  Position EINZELN auf; es gibt keine Sammelschreibung und keine zweite
  Schreiblogik.

Alles andere ist unveraendert lesend: kein Parameter laesst sich aendern,
keine Position eroeffnen, kein Bot-Lauf anstossen. Ausserhalb dieses einen
Pfades werden die Bot-Datenbanken weiterhin ueber
`notifications/monitor.py` im SQLite-Modus `ro` geoeffnet.

## Ausserhalb der Boersenzeiten: Warteauftraege (Aktien-Bots)

**Das ist die einzige Funktion des Projekts, bei der zeitversetzt und ohne
erneute Rueckfrage geschrieben wird. Bitte vor der Einrichtung des Cronjobs
den entsprechenden Abschnitt der
[Testanleitung](TESTANLEITUNG_SCHLIESSEN.md#teil-2-warteauftraege-ausserhalb-der-boersenzeiten)
lesen.**

Vorher schloss ein Tap bei einem Aktien-Bot auch nachts oder am Wochenende
sofort - zum letzten verfuegbaren **Tages-Schlusskurs**, also zu einem Kurs,
den es "gerade jetzt" nicht gibt. Jetzt gilt:

| Lage | Was passiert |
|---|---|
| Krypto-Bot, immer | sofort schliessen, zum aktuellen Kurs - **unveraendert** |
| Aktien-Bot, Boerse offen | sofort schliessen, zum aktuellen Kurs - **unveraendert** |
| Aktien-Bot, Boerse zu | **Warteauftrag** nach zusaetzlicher Bestaetigung; ausgefuehrt bei der naechsten Oeffnung |
| Aktien-Bot, Kalender nicht lesbar | **weder noch** - abgelehnt mit Begruendung (fail closed) |

Die Unterscheidung trifft der **Server** anhand eines echten
NYSE-Handelskalenders (`notifications/boersenkalender.py`, Bibliothek
`pandas_market_calendars`, siehe `requirements.txt`) - inklusive
beweglicher Feiertage und verkuerzter Handelstage. Der Browser bestaetigt
sie nur; er waehlt sie nicht.

**Was ein Warteauftrag ist:** eine gespeicherte Absicht, kein Ergebnis. Er
nennt Bot, Position, Symbol, Zeitpunkt der Anforderung und Quelle - aber
ausdruecklich **keinen Kurs**, denn den gibt es noch nicht. Er liegt in
`notifications/warteauftraege.json` (eine Datei fuer alle Bots, gitignored,
gegen gleichzeitigen Zugriff gesperrt) und ueberlebt jeden Neustart von
Dashboard und Ausfuehrungsskript.

**Ausgefuehrt** wird er von einem eigenstaendigen Programm, nicht vom
Dashboard und nicht von einem Bot:

```
python3 dashboard/warteauftraege_ausfuehren.py [--trockenlauf] [--jetzt <ISO>]
```

Es prueft den Kalender, holt bei offener Boerse den aktuellen Kurs ueber
dieselbe Funktion wie das Dashboard (`monitor.fetch_stock_prices`) und
schliesst ueber dieselbe Kernfunktion wie jeder andere manuelle Eingriff
(`manual_close.schliesse_position`, mit Transaktion, erneuter Pruefung und
Protokoll). Im Protokoll traegt die Zeile `quelle=warteauftrag`.

Der noetige Cronjob-Eintrag steht in der Testanleitung, Schritt 17. **Ohne
ihn wird kein Auftrag ausgefuehrt** - sie sammeln sich dann sichtbar im
Dashboard an.

**Stornieren** entfernt einen wartenden Auftrag - ohne zweite Bestaetigung,
weil es eine Ausfuehrung *verhindert* statt eine auszuloesen. Die Listen
stehen auf der Bot-Detailseite (nur dieser Bot) und auf der Uebersichtsseite
(alle Bots).

**Vor dem ersten Einsatz:** die gestaffelte Anleitung in
[`TESTANLEITUNG_SCHLIESSEN.md`](TESTANLEITUNG_SCHLIESSEN.md) durchgehen -
Schritte 0-3 sind gefahrlos, Schritt 4 testet an einer Kopie der Datenbank,
erst Schritt 5 fasst die echte an. Dort stehen auch die bekannten
Restrisiken.

## Struktur

| Datei | Zweck |
|---|---|
| `server.py` | Start (uvicorn), Bindung an 127.0.0.1, Warnhinweise |
| `app.py` | FastAPI-App: Endpunkte, Token-Pruefung, Auslieferung des Frontends |
| `datenquelle.py` | duenne Leseschicht ueber `notifications/monitor.py` (enthaelt bewusst keinen Schreibpfad) |
| `schliessen.py` | der eine schreibende Weg: Zustand zwischen den beiden Bestaetigungen, ruft `notifications/manual_close.py` |
| `konfig.py` | Token/Host/Port aus `.env` bzw. Umgebung |
| `static/` | Frontend (HTML/CSS/JS), `manifest.json`, `sw.js`, Icons |
| `erzeuge_icons.py` | erzeugt die beiden PWA-Icons neu (keine Fremdbibliothek noetig) |
| `warteauftraege_ausfuehren.py` | eigenstaendiges Programm (Cronjob): fuehrt wartende Ausstiege aus, sobald die Boerse offen ist |
| `test_dashboard.py` | Selbsttests gegen den echten Server, synthetische Daten |
| `pruefe_warteauftraege_kopie.py` | Selbstpruefung der Warteauftraege gegen eine **Arbeitskopie** (laeuft nur mit Markierungsdatei `.probe-kopie`) |
| `test_zustandsmaschine.js` | Verhaltenstest der Aktualisierungs-Zustaende (node, wird mitgestartet) |
| `test_zeitzone.js` | Verhaltenstest der Zeitanzeige in vier Zeitzonen (node, wird mitgestartet) |
| `TESTANLEITUNG_SCHLIESSEN.md` | gestaffelte Anleitung fuer den manuellen Test des Schliessens (Teil 2: Warteauftraege) |
| `TESTPLAN_WARTEAUFTRAEGE_AGENT.md` | derselbe Test, aber als Arbeitsanweisung fuer eine lokale Claude-Code-Sitzung |

## Erste Inbetriebnahme (Schritt fuer Schritt)

1. **Abhaengigkeiten installieren**
   ```
   pip3 install -r requirements.txt
   ```
   (Die Datei im Projekt-Root bindet die Listen von Dashboard und
   Telegram-Bot ein und ergaenzt den Boersenkalender
   `pandas_market_calendars`, ohne den Aktien-Positionen weder sofort
   geschlossen noch vorgemerkt werden koennen.)
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
   Erwartet: `738/738 Pruefungen bestanden.`

   Die beiden Node-Tests werden davon mitgestartet, sofern `node`
   vorhanden ist. Fehlt es, sagen die Selbsttests das ausdruecklich und
   nennen, was dadurch ungeprueft bleibt - sie melden es nicht als
   Fehlschlag.

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

## Endpunkte (lesend)

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
| `/api/warteauftraege[?bot=name]` | wartende Ausstiegsauftraege, je mit Angabe, ob die Position noch offen ist |

Seiten: `/` (Uebersicht), `/bot?name=<bot>` (Detail), `/login`,
`/abmelden`, `/manifest.json`, `/sw.js`, `/statisch/*`.

## Endpunkte des manuellen Schliessens

| Endpunkt | Methode | Schreibt? |
|---|---|---|
| `/api/bots/{name}/schliessbare-positionen[?live=1]` | GET | nein - Zeilen-IDs, Kurs, geschaetzter PnL |
| `/api/bots/{name}/schliessen/vorbereiten` | POST | nein - legt nur einen Vorgang im Arbeitsspeicher an |
| `/api/bots/{name}/schliessen/abbrechen` | POST | nein - verwirft ihn wieder (beide Vorgangsarten) |
| `/api/bots/{name}/schliessen/ausfuehren` | POST | **ja** - schliesst eine Position |
| `/api/bots/{name}/alle-schliessen/vorbereiten` | POST | nein - nur Arbeitsspeicher |
| `/api/bots/{name}/alle-schliessen/ausfuehren` | POST | **ja** - schliesst alle bestaetigten Positionen, jede einzeln |
| `/api/warteauftraege/stornieren` | POST | nein - entfernt einen wartenden Auftrag |

Bei geschlossener Boerse haben die drei `ausfuehren`-Endpunkte einen
**vierten Ausgang**, der gar nichts schreibt: sie legen Warteauftraege an.
Dafuer muss das Feld `warteauftrag_bestaetigt: true` mitkommen - der
zusaetzliche Warnschritt aus dem Dialog. Fehlt es, wird mit 409 abgelehnt
und **nichts** angelegt und nichts geschrieben.

`vorbereiten` erwartet `{"trade_id": <ID>}` und antwortet mit Symbol,
Einstiegs- und aktuellem Kurs, geschaetztem PnL sowie einer Vorgangs-Kennung.
`ausfuehren` erwartet `{"vorgang": "<Kennung>"}` - nichts weiter. Jeder
Fehlversuch verbraucht die Kennung; abgelehnt wird mit 409 (Konflikt), ein
nicht freigeschalteter Bot mit 403.

### Notfallweg: alle Positionen

`alle-schliessen/vorbereiten` braucht keinen Koerper und antwortet mit allen
offenen Positionen samt Kursen, dem **Durchschnitt je Position** (bewusst
keine Summe - die Summe von Trade-Prozenten ist keine Portfolio-Rendite,
siehe Methodik-Grundsatz 2 im Uebergabeprotokoll) und einer Kennung eigener
Art. Eine Kennung des Einzelwegs loest hier nichts aus und umgekehrt.

Dazu - in `vorbereiten` wie in `ausfuehren` - das Feld `pnl_gewichtet` mit dem
nach **Positionsgroesse gewichteten** Durchschnitt:

```
"pnl_gewichtet": {
  "wert_pct": -2.59,                  // Summe(Allokation*PnL) / Summe(Allokation)
  "ungewichtet_schnitt_pct": 0.5,     // dieselben Positionen ohne Gewichtung
  "anzahl": 4,
  "grundlage": "angenommene Positionsgroesse je Bot (ALLOCATION_PCT ...)",
  "hinweis": "... Annahme, KEINE live getrackte Kapitalbindung ...",
  "gewichte": [{"bot": ..., "allokation_pct": 10.0, "quelle": "live_params.py",
                "anzahl": 2}],
  "nicht_gewichtbar": [{"bot": ..., "grund": ..., "anzahl": 1,
                        "pnl_schnitt_pct": 1.0}]
}
```

Die Gewichte kommen je Bot aus dessen eigenen Dateien - `ALLOCATION_PCT` aus
`live_params.py` (in **Prozent**) oder, wo es dort bewusst nicht steht, aus
`equity_simulation.py` (als **Anteil**); dieselbe Konvention wie in
`shared/portfolio_overview.py`. Das ist eine **Backtest-Annahme**, keine live
getrackte Kapitalbindung und keine Portfolio-Rendite - die Oberflaeche schreibt
das sichtbar dazu. Ein Bot ohne dokumentierte Groesse wird **nicht** mit einem
angenommenen Wert mitgerechnet, sondern steht mit Grund unter
`nicht_gewichtbar`. `pnl_schnitt_pct` und die Spannweite bleiben unveraendert
daneben, damit der Unterschied der beiden Zahlen selbst sichtbar ist.

`alle-schliessen/ausfuehren` liest den **tatsaechlichen** Stand neu und
schliesst den Schnitt aus "bestaetigt" und "noch offen" - jede Position
einzeln ueber dieselbe Kernfunktion wie der Einzelweg, mit eigener
Protokollzeile. Scheitert eine, laufen die uebrigen weiter; die Antwort nennt
`geschlossen`, `fehlgeschlagen`, `uebersprungen` (vom Bot selbst geschlossen)
und `nicht_bestaetigt` (nach der Uebersicht eroeffnet, deshalb nicht
angefasst) vollstaendig. **Ein Teilausfall ist kein HTTP-Fehler**, sondern
ein Ergebnis mit `erfolg: false` - ein 409 wuerde verschweigen, was bereits
geschlossen wurde.

In der Oberflaeche braucht dieser Weg **zwei Klicks** (Uebersicht, dann
Rueckfrage), der Einzelweg einen. Beide ohne Texteingabe.

### Globaler Crash-Weg: alle Bots

`POST /api/alle-bots-schliessen/vorbereiten` (kein Koerper) liest ueber ALLE
freigeschalteten Bots hinweg die offenen Positionen zusammen und antwortet
nach Bot gruppiert, je Bot mit Durchschnitt und Spannweite - **keine
aufsummierte Gesamtzahl ueber alle Bots**, aus demselben Grund wie oben.
Bot-uebergreifend steht dort genau eine Kennzahl, `pnl_gewichtet` (siehe
oben): der nach Positionsgroesse **gewichtete** Durchschnitt mit Angabe
seiner Grundlage. Hier ist er inhaltlich relevant, weil 10 %, 5 % und 2 %
Positionsgroesse aufeinandertreffen - ein einfacher Durchschnitt ueber alle
Positionen wuerde sie gleich gewichten. `ausfuehren` traegt dieselbe Angabe
ueber die tatsaechlich geschriebenen Werte. Ein Bot, dessen
Datenbank fehlt, wird stillschweigend uebergangen (er lief noch nie); ein
Bot, dessen Datenbank vorhanden aber unlesbar ist, wird als `lesefehler`
ausgewiesen.

`POST /api/alle-bots-schliessen/ausfuehren` erwartet
`{"vorgang": "<Kennung>", "bestaetigung": "CRASH"}`. Der Text wird
case-sensitiv geprueft, NACH dem Einloesen der Kennung - ein falscher
Versuch verbraucht sie also. Geschlossen wird je Bot ueber dieselbe Schleife
wie beim bot-weiten Weg, je Position ueber dieselbe Kernfunktion wie beim
Einzelweg.

**Teilausfall in zwei Dimensionen:** scheitert eine Position, laufen die
uebrigen Positionen des Bots weiter; scheitert ein ganzer Bot (Datenbank
gesperrt oder unlesbar), laufen die uebrigen Bots weiter. Die Antwort nennt
`bots` (je Bot das volle Ergebnis) und `bots_fehlgeschlagen` getrennt. Ein
Teilausfall ist auch hier kein HTTP-Fehler.

Im Protokoll traegt jede Zeile dieses Wegs `quelle=dashboard-crash` statt
`quelle=dashboard` - so ist hinterher unterscheidbar, was der eine
Crash-Klick angefasst hat.

Jeder Versuch - erfolgreich wie abgelehnt - landet in
`logs/notifications/manuelle_eingriffe.log`, jede Zeile mit der Marke
`MANUELLER-EINGRIFF` und dem Feld `quelle=dashboard`. Es ist bewusst
dasselbe Protokoll wie fuer die Telegram-Variante: die Frage "wer hat diese
Position wann von Hand geschlossen" soll sich aus EINER Datei beantworten
lassen.

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

- **Ein Warteauftrag wird ohne erneute Rueckfrage ausgefuehrt.** Das ist
  seine Aufgabe, aber es ist neu in diesem Projekt: zwischen Bestaetigung
  und Schreibzugriff koennen Stunden bis Tage liegen, und der Kurs steht
  beim Bestaetigen noch nicht fest. Wer den Cronjob einrichtet, erlaubt das
  fuer alle kuenftigen Auftraege.
- **Ohne `pandas_market_calendars` lassen sich Aktien-Positionen gar nicht
  mehr manuell schliessen** - weder sofort noch vorgemerkt. Das ist Absicht
  (fail closed); die Meldung nennt die fehlende Bibliothek. Krypto ist nicht
  betroffen.
- **Die Auftragsdatei liegt nur lokal** und ist gitignored. Sie ueberlebt
  Neustarts, aber keinen Rechnerwechsel.

- **Das Zugriffs-Token kann jetzt mehr als lesen.** Es liegt nach dem
  ersten Login 90 Tage als Cookie im Browser. Wer Zugriff auf das
  entsperrte Geraet hat, kann eine Position schliessen; die beiden
  Bestaetigungen schuetzen vor Versehen, nicht vor einer fremden Person.
  Das war vorher schon so, wog aber weniger - bis jetzt konnte man mit
  dem Token nur lesen. Dasselbe gilt fuer `DASHBOARD_HOST`: wer die
  Bindung von localhost weg aendert, macht auch den schreibenden Endpunkt
  im Netz erreichbar.
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

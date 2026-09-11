# Broker-Brücke: Paper-Trades auf dem Binance SPOT-Testnet spiegeln

> **Es gibt inzwischen zwei Brücken.** Diese hier spiegelt den Krypto-Bot
> `t3_supertrend` auf das Binance-Testnet. Die zweite spiegelt den Aktien-Bot
> `volatility_breakout` auf ein **IBKR-Paper-Konto** — siehe
> [`README_IBKR.md`](README_IBKR.md). Gemeinsam ist beiden der
> schreibgeschützte Leser `bot_db.py`; alles andere ist getrennt, inklusive der
> Notbremse (`broker/STOP` gegen `broker/STOP_IBKR`).

Diese Komponente ist der **erste Schreibzugriff dieses Projekts auf eine Börse**.
Sie platziert echte Orders — aber auf dem **Testnet**, mit virtuellem Guthaben,
ohne echtes Geld und ohne Marktwirkung.

```
Bot (unverändert)            Brücke (neu)                     Binance SPOT-TESTNET
forward_test.py  ──────►  paper_trading_t3_supertrend.db
                                   │  nur lesend (mode=ro)
                                   ▼
                             broker/spiegel.py  ──────────►  MARKET BUY / SELL
                                   │
                                   ▼
                          broker_testnet_t3_supertrend.db     (eigene Nachverfolgung)
```

**Was unverändert bleibt:** `forward_test.py`, `live_params.py` und die
`trades`-Tabelle. Die Brücke liest die Bot-Datenbank über `file:...?mode=ro` —
SQLite verweigert dort jeden Schreibversuch, auch einen versehentlichen. Ihre
eigene Nachverfolgung liegt in einer eigenen Datei.

**Was sie nicht ist:** kein Live-Trading, kein Schritt dorthin, den man aus
Versehen macht. Der Endpunkt steht als Literal im Code, es gibt keine
Umgebungsvariable, die ihn verschieben könnte, und jede einzelne Anfrage läuft
durch eine Prüfung des geparsten Hostnamens.

---

## 1. Voraussetzung: Testnet-Konto und Schlüssel (machst du selbst)

Das geht nicht aus der Entwicklungsumgebung heraus — `testnet.binance.vision`
ist dort durch die Netzwerk-Richtlinie gesperrt (siehe Abschnitt 8).

1. **https://testnet.binance.vision/** öffnen.
2. Oben rechts **„Log In with GitHub"** — das Testnet hat keine eigene
   Registrierung, es nutzt einen GitHub-Login. Es entsteht dabei **kein**
   Binance-Konto und es wird nichts verknüpft.
3. Nach dem Login: **„Generate HMAC_SHA256 Key"**, eine Beschreibung eintragen
   (z. B. `trading-bot-bruecke`), bestätigen.
4. Es erscheinen **API Key** und **Secret Key**. Das Secret wird **nur einmal**
   angezeigt — jetzt kopieren. Geht es verloren, einfach einen neuen Schlüssel
   erzeugen und den alten löschen.
5. Das Konto ist automatisch mit virtuellem Guthaben ausgestattet (USDT, BTC
   u. a.). Dieses Guthaben lässt sich weder ein- noch auszahlen, und Binance
   **setzt die Testnet-Daten periodisch zurück** (etwa monatlich, ohne
   Vorankündigung). Danach sind Schlüssel und Bestände neu zu erzeugen — das ist
   normal und kein Fehler der Brücke.

### In die `.env` eintragen

Die `.env` liegt im Projekt-Root (`~/trading-bot/.env`) und steht in
`.gitignore`. Dieselbe Datei, die schon `TELEGRAM_BOT_TOKEN` enthält:

```bash
cd ~/trading-bot
cat >> .env <<'EOF'
BINANCE_TESTNET_API_KEY=hier-der-API-Key
BINANCE_TESTNET_API_SECRET=hier-das-Secret
# optional, Standard 100, harte Obergrenze 1000:
BINANCE_TESTNET_BETRAG_USDT=100
EOF
chmod 600 .env
```

**Eigene Variablennamen, mit Absicht.** Die bestehenden Schlüssel für den
Kursdatenabruf (`BINANCE_API_KEY` / `BINANCE_API_SECRET`, benutzt von
`shared/fetch_binance_data.py`) gehören zu einem **echten** Binance-Konto und
werden hier nie gelesen. Mehr noch: stimmt ein Testnet-Schlüssel mit einem davon
überein, bricht die Brücke ab, bevor irgendetwas gesendet wird.

---

## 2. Was die Brücke tut

| Der Bot … | … die Brücke |
|---|---|
| eröffnet eine Position (`status='open'`) | `MARKET BUY` über `BINANCE_TESTNET_BETRAG_USDT` |
| schließt sie (`status='closed'`) | `MARKET SELL` **genau der gekauften Menge** |
| eröffnet **und** schließt, bevor die Brücke lief | **nichts** — wird als „nicht gespiegelt" ausgewiesen |
| läuft auf einem anderen Bot | **nichts** — freigeschaltet ist nur `t3_supertrend` |

**Warum nichts nachgespiegelt wird:** zwei Orders zu *heutigen* Kursen für eine
Entscheidung, die längst vorbei ist, wären kein Spiegel, sondern ein eigener,
zufälliger Trade. Solche Fälle verschwinden nicht still — sie stehen im
Abgleichsbericht.

**Die Menge** kommt **nicht** aus `ALLOCATION_PCT`. Der Bot führt keine
Positionsgrößen (seine 10 % sind eine Backtest-Annahme), und das Testnet hat
ein künstliches Orderbuch — eine große Order dort zu messen sagt nichts. Es ist
deshalb ein fester, kleiner Gegenwert je Order, abgerundet auf die Schrittweite
des Symbols (`LOT_SIZE`) und geprüft gegen Mindestmenge und Mindestgegenwert
(`NOTIONAL`), beides aus der Börse gelesen statt geraten.

---

## 3. Die Sicherungen

| Sicherung | Wo |
|---|---|
| Endpunkt als **Literal**, keine Umgebungsvariable | `zugang.py`, `TESTNET_BASIS` |
| Prüfung des **geparsten Hostnamens** bei jeder Anfrage | `binance_testnet.pruefe_url()` |
| Die echten Handelsendpunkte stehen namentlich auf einer Verbotsliste | `zugang.VERBOTENE_HOSTS` |
| Nur Pfade unter `/api/` — `/sapi/`-Pfade (dort liegen **Auszahlungen**) sind strukturell unerreichbar | `pruefe_url()` |
| **Trockenlauf ist der Standard**, Senden verlangt `--echt` | `spiegel.py` |
| **Notbremse**: `touch broker/STOP` stoppt jede Order, `rm broker/STOP` gibt wieder frei | **zweimal** geprüft: zu Beginn jedes Laufs *und* vor **jeder** Order |
| Höchstens 5 Orders je Lauf, 20 in 24 Stunden | `zugang.MAX_ORDERS_PRO_*` |
| Betrag je Order höchstens 1000 USDT — die Grenze steht im Code, nicht in der `.env` | `zugang.betrag_usdt()` |
| Getrennte Schlüssel, Verwechslung wird erkannt | `zugang.get_zugang()` |
| Bot-Datenbank schreibgeschützt geöffnet | `spiegel.lies_trades()` |
| Keine doppelte Order: `UNIQUE(bot, trade_id, seite)` **und** eine aus dem Trade abgeleitete `newClientOrderId`, die eine bereits gesendete Order wiedererkennt | `spiegel.py` |
| Jede Order einzeln im Protokoll, mit Menge, Kurs, Order-ID, Gebühren | `logs/broker/testnet_spiegel.log` |
| Rückgabewert 1 bei jedem Fehlschlag, damit Cron per Mail anschlägt | `spiegel.main()` |
| Gezogene Notbremse **ohne** offene Aufgabe: Rückgabewert **0** — sie ist eine befolgte Anweisung, kein Fehlschlag; mit offener Aufgabe bleibt es bei 1 | `spiegel.main()` |

Der Schlüssel kann auf dem Testnet ohnehin nicht abheben — das Konto hält keine
echten Werte. Die `/sapi/`-Sperre ist trotzdem drin: sie kostet nichts und gilt
auch dann noch, wenn diese Brücke irgendwann die Vorlage für etwas Echtes ist.

---

## 4. Gestaffelte Einführung — in dieser Reihenfolge

### Schritt 1 — Selbsttests (kein Netz, keine Schlüssel nötig)

```bash
cd ~/trading-bot
python3 broker/test_broker.py
```

Erwartet: `148 von 148 Pruefungen bestanden, 0 fehlgeschlagen.`

### Schritt 2 — Verbindung und Schlüssel prüfen (liest nur)

```bash
python3 broker/spiegel.py --pruefen
```

Erwartet:

```
Endpunkt (fest im Code): https://testnet.binance.vision
Erreichbar: ja
Zeitversatz zur Boerse: ... ms
Schluessel akzeptiert: ja (kann handeln: True, kann abheben: False)
Guthaben > 0 in N Waehrung(en): BTC ..., USDT ...
Notbremse: nicht gesetzt
Betrag je Order: 100 USDT
```

`/api/v3/account` ist signiert, aber ein reiner Lesezugriff — dieser Schritt
kann **keine** Order auslösen. Er ist der richtige erste, weil ein falscher
Schlüssel hier auffällt und nicht erst mitten in einem Handelsversuch.

**Wenn „Invalid Api-Key ID" (Code −2008) kommt:** siehe Abschnitt 8.

### Schritt 3 — Was zu tun wäre, ohne es zu tun

```bash
python3 broker/spiegel.py --status      # welche Trades offen sind
python3 broker/spiegel.py               # TROCKENLAUF, sendet nichts
```

Der Trockenlauf rechnet alles durch — Kurs, Menge, Schrittweite, Gegenwert — und
protokolliert, was gesendet *würde*. Prüfe die Ausgabe gegen die Bot-Datenbank:

```bash
sqlite3 paper_trading_t3_supertrend.db \
  "SELECT id, symbol, entry_price, status FROM trades WHERE status='open';"
```

Dieselben Symbole, plausible Mengen? Dann weiter.

### Schritt 4 — Die erste echte Order, von Hand und einzeln

Vorher absichern, dass es höchstens **eine** wird: die Notbremse setzen, den
Trockenlauf ansehen, dann entscheiden.

```bash
touch broker/STOP                       # Sicherung
python3 broker/spiegel.py --echt        # muss "NOTBREMSE aktiv" melden
                                        # (auch bei NULL offenen Aufgaben)
rm broker/STOP                          # Sicherung lösen
python3 broker/spiegel.py --echt        # jetzt geht EINE Order raus
```

Danach **drei** Kontrollen:

```bash
# 1. Das eigene Protokoll
tail -5 logs/broker/testnet_spiegel.log

# 2. Die eigene Nachverfolgung
sqlite3 broker_testnet_t3_supertrend.db \
  "SELECT trade_id, seite, symbol, order_id, menge_brutto, menge_netto,
          ausfuehrungspreis, simulationspreis FROM spiegelungen;"

# 3. Die Bot-Datenbank ist unberührt (Zeilenzahl und Zustand wie vorher)
sqlite3 paper_trading_t3_supertrend.db \
  "SELECT status, COUNT(*) FROM trades GROUP BY status;"
```

Und in der Weboberfläche von `testnet.binance.vision` unter **Orders** muss
genau diese Order mit derselben Order-ID stehen.

**Gegenprobe, die sich lohnt:** `python3 broker/spiegel.py --echt` noch einmal
aufrufen. Es darf **keine** zweite Order entstehen („Der zweite Lauf sendet gar
nichts") — das ist die Sperre, die im Cron-Betrieb am wichtigsten ist.

### Schritt 5 — Den Abgleich ansehen

```bash
python3 broker/abgleich.py
```

Vollständig wird eine Zeile erst, wenn der Bot die Position auch wieder
geschlossen und die Brücke das gespiegelt hat. Beispiel siehe Abschnitt 6.

### Schritt 6 — Erst jetzt automatisieren

Die Brücke läuft **nach** dem Bot, nicht parallel: sie liest dessen Ergebnis.
Der t3-Bot läuft auf 4h-Kerzen; die Brücke direkt danach einzuhängen hält den
Zeitversatz klein (und damit die gemessene Abweichung aussagekräftig).

`crontab -e`, und die Brücke an die bestehende Bot-Zeile anhängen:

```cron
# Bestehende Zeile (Beispiel) ... und die Bruecke direkt danach, im selben
# Eintrag: && statt ; damit sie nur laeuft, wenn der Bot durchgelaufen ist.
5 */4 * * * cd ~/trading-bot && /usr/bin/python3 strategies/t3_supertrend/forward_test.py >> logs/t3_supertrend/cron.log 2>&1 && /usr/bin/python3 broker/spiegel.py --echt >> logs/broker/cron.log 2>&1
```

Falls du Bot und Brücke getrennt halten willst, ein eigener Eintrag ein paar
Minuten später:

```cron
15 */4 * * * cd ~/trading-bot && /usr/bin/python3 broker/spiegel.py --echt >> logs/broker/cron.log 2>&1
```

Prüfen und wieder ausschalten:

```bash
crontab -l | grep spiegel          # steht der Eintrag?
touch ~/trading-bot/broker/STOP    # Notbremse: Cron läuft weiter, sendet nichts
rm ~/trading-bot/broker/STOP       # wieder frei
```

Der Pfad zu `python3` muss vollständig sein — Cron hat ein anderes `PATH` als
die Anmeldesitzung. `which python3` gibt den richtigen.

---

## 5. Tägliche Kontrolle

```bash
python3 broker/spiegel.py --status     # offene Aufgaben, Zähler des Tages
python3 broker/abgleich.py             # Simulation gegen Ausführung
grep FEHLGESCHLAGEN logs/broker/testnet_spiegel.log | tail
```

---

## 6. Beispiel eines Abgleichsberichts

Mit **synthetischen** Daten erzeugt (Börsen-Attrappe, kein Netz), damit die Form
vor der ersten echten Order sichtbar ist:

```
====================================================================================================
ABGLEICH Simulation <-> Binance SPOT-TESTNET - Bot t3_supertrend
====================================================================================================
Gespiegelte Trades: 3 (vollstaendig, also Kauf UND Verkauf: 2)
Kostenannahme der Simulation: 0.30 Prozentpunkte je Trade (Gebuehr + Slippage, pauschal)

Trade Symbol      Einstieg sim /  echt   Abw %   Ausstieg sim /  echt   Abw %    PnL sim  PnL echt   Diff pp   PnL Kap.   Restmenge
--------------------------------------------------------------------------------------------------------------------------
    1 BTCUSDT      50000.0000   50030.0000   0.060   51500.0000   51530.9000   0.060      2.70      2.79      0.09      2.38  0.00000800
    2 ETHUSDT       2000.0000    2001.2000   0.060    1900.0000    1901.1400   0.060     -5.30     -5.19      0.11     -5.28  0.00005000
    3 BTCUSDT      49000.0000   50030.0000   2.102            -            -       -         -         -         -         -           -
--------------------------------------------------------------------------------------------------------------------------
Mittlere Abweichung: Einstieg   0.741 %, Ausstieg   0.060 %; mittlerer PnL-Unterschied   0.102 Prozentpunkte (je Einheit),  -0.151 Prozentpunkte auf das eingesetzte Kapital

NICHT gespiegelt (1):
  Trade     4 eroeffnung   ETHUSDT    Trade war schon geschlossen, bevor die Eroeffnung gespiegelt wurde - es wird NICHT nachgekauft

Fehlversuche (neueste zuerst, hoechstens 20):
  ... Trade 2 schliessung (echt): Testnet lehnt /api/v3/order ab (HTTP 400, Code -2010): Account has insufficient balance. | Hinweis: ...
```

**Die drei Zahlen, auf die es ankommt:**

* **`Diff pp`** — wie weit die pauschale Kostenannahme von 0,30 Prozentpunkten
  von der Wirklichkeit abweicht, **je Einheit** gerechnet und damit direkt mit
  `pnl_pct` der Simulation vergleichbar.
* **`PnL Kap.`** — dieselbe Rendite auf das *eingesetzte Kapital*. Sie ist
  schlechter, und zwar nicht wegen Slippage, sondern wegen der **Restmenge**:
  verkauft werden darf nur ein Vielfaches der Schrittweite, und nach der Gebühr
  in der Basiswährung bleibt fast immer ein Rest liegen. Bei 0,002 BTC sind das
  0,000008 BTC — **0,4 % der Position, mehr als die gesamte Slippage**. Beide
  Zahlen nicht zu trennen hieße, Rundung für Slippage zu halten. (Genau dieser
  Fehler steckte in der ersten Fassung und ist erst im Test aufgefallen.)
* **`Einstieg Abw %`** enthält neben der Ausführungsabweichung den
  **Zeitversatz** zwischen Bot-Lauf und Brücken-Lauf — Trade 3 oben mit 2,1 %
  ist praktisch reine Marktbewegung, kein Börseneffekt. Deshalb Schritt 6:
  Brücke direkt nach dem Bot.

---

## 7. Was diese Anbindung **nicht** beantwortet

Das SPOT-Testnet hat ein **eigenes, künstliches Orderbuch** — eigene Kurse,
eigene Liquidität, periodisch zurückgesetzt. Eine dort gemessene Slippage prüft
die Anbindung, die Mengenrechnung und die eigene Buchführung. Sie sagt **nichts**
darüber, wie viel Slippage an der echten Börse entsteht.

---

## 8. Befund zur Testnet-Adresse (nachgeprüft, und es ist nicht eindeutig)

Die Aufgabe bat darum, die Adresse zu verifizieren. Das Ergebnis ist
zweiteilig — es gibt inzwischen **zwei** Nicht-Produktiv-Umgebungen:

| | SPOT-Testnet | Demo Mode („Demo Trading") |
|---|---|---|
| REST-Basis | `https://testnet.binance.vision/api` | `https://demo-api.binance.com/api` |
| Schlüssel | auf `testnet.binance.vision`, GitHub-Login, **kein** Binance-Konto | **im echten Binance-Konto**, unter Demo Trading → API Key Management |
| Orderbuch | eigenes, künstliches | spiegelt die echten Kurse und Orderbücher |
| Rücksetzung | automatisch, etwa monatlich | selbst gesteuert |
| Besonderheit | kann Funktionen enthalten, die es live noch nicht gibt | gleiche Filter und Limits wie die Produktion |

Die offizielle Dokumentation führt **beide** — `testnet/` nennt unverändert
`testnet.binance.vision/api`, `demo-mode/` nennt `demo-api.binance.com/api`.
Gleichzeitig berichten Nutzer (ccxt-Issue #27266, November 2025), signierte
Anfragen gegen `testnet.binance.vision` würden mit **Code −2008 („Invalid
Api-Key ID")** abgelehnt. Die plausibelste Erklärung: dort wurden Schlüssel der
einen Umgebung gegen die andere benutzt — die sind **nicht** austauschbar. Ich
konnte es nicht nachmessen: `testnet.binance.vision` ist aus der
Entwicklungsumgebung durch die Netzwerk-Richtlinie gesperrt (HTTP 403 am Proxy).

**Eingebaut ist deshalb nur das SPOT-Testnet**, wie die Aufgabe es verlangt.
`demo-api.binance.com` steht ausdrücklich auf der **Verbotsliste** — nicht weil
es echter Handel wäre, sondern weil seine Schlüssel in einem echten
Binance-Konto liegen. Das ist eine andere Risikolage und deine Entscheidung,
nicht meine.

**Wenn Schritt 2 mit −2008 scheitert**, dann in dieser Reihenfolge:

1. Schlüssel wirklich auf `testnet.binance.vision` erzeugt? (Nicht im
   Binance-Konto.)
2. Key und Secret nicht vertauscht, keine Leerzeichen, kein Zeilenumbruch in der
   `.env`?
3. Daten zurückgesetzt? Dann neuen Schlüssel erzeugen.
4. Hält es danach an, ist wahrscheinlich doch der Demo Mode die aktive
   Umgebung. **Sag es mir** — dann baue ich ihn als zweite, ausdrücklich
   freigegebene Umgebung ein (eigene Variablennamen, eigener Host, dieselbe
   Wache). Das ist eine bewusste Freigabe, keine Konfigurationsänderung.

---

## 9. Dateien

| Datei | Inhalt |
|---|---|
| `broker/zugang.py` | Schlüssel aus `.env`, Endpunkt-Literale, Notbremse, Grenzen |
| `broker/binance_testnet.py` | signierte Aufrufe, URL-Wache, Mengenrechnung, Auswertung der Ausführung |
| `broker/spiegel.py` | die Brücke: liest den Bot, entscheidet, sendet, protokolliert |
| `broker/abgleich.py` | Bericht Simulation ↔ Ausführung |
| `broker/test_broker.py` | Selbsttests, ohne Netz |
| `broker_testnet_t3_supertrend.db` | eigene Nachverfolgung (in `.gitignore`, wie alle `*.db`) |
| `logs/broker/testnet_spiegel.log` | jede Order mit vollem Kontext |
| `broker/STOP` | existiert diese Datei, wird nichts gesendet |

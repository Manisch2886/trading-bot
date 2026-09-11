# Broker-Brücke 2: Paper-Trades auf einem IBKR-Paper-Konto spiegeln

Gegenstück zur Binance-Testnet-Brücke (`broker/README.md`), für den **Aktien**-Bot
`volatility_breakout`. Gespiegelt wird auf ein **IBKR-Paper-Trading-Konto**:
virtuelles Geld, aber echte Kurse und echte Orderbücher.

```
Bot (unverändert)              Brücke (neu)                      TWS / IB Gateway        IBKR Paper
forward_test.py ──► paper_trading_volatility_breakout.db              (lokal)
                             │ nur lesend (mode=ro)
                             ▼
                   broker/ibkr_spiegel.py ──── Socket 127.0.0.1:7497 ────► MARKET BUY / SELL
                             │
                             ▼
                 broker_ibkr_volatility_breakout.db   (eigene Nachverfolgung)
```

**Der architektonische Unterschied zu Binance:** es gibt keine REST-API. Die
Brücke redet mit einer Software, die **auf deinem Mac läuft** und dort am
Paper-Konto angemeldet ist. Läuft sie nicht, passiert nichts — eine
Fehlermeldung, keine Order.

---

## 1. Warum `volatility_breakout` als erster Aktien-Bot

| Kriterium | `volatility_breakout` | `turtle_soup_stocks` | Elliott / RSI-2 (Aktien) |
|---|---|---|---|
| Schema | **11 Spalten, keine Zusatzspalten** | 11 Spalten, keine Zusatzspalten | Zusatzspalten (`target_price`/`fib_score` bzw. `rsi_at_entry`) |
| Positionslimit | **15** | **keines** (sättigt rechnerisch bei ~50) | 20 bzw. vorhanden |
| Ausgeführte Trades im Backtest | **1236** (OOS 385) | 1887 (OOS 575) | — |
| Ausstiegswege | `stop_loss` (8 %) **und** `time_exit` | nur Zeit-Exit (`STOP_MODE=None`) | mehrere |
| Positionsgröße dokumentiert | ja, 10 % in `live_params.py` | ja, 2 % | ja |

Die beiden einfachsten Schemata sind gleichauf; entschieden haben das
**Positionslimit** und die **Handelsfrequenz**. Für eine erste Broker-Anbindung
ist eine nach oben begrenzte Zahl gleichzeitiger Positionen der entscheidende
Unterschied — sie begrenzt auch die Zahl der Orders. Und `volatility_breakout`
hat **zwei** klar benannte Ausstiegswege, womit sich prüfen lässt, ob die Brücke
beide spiegelt. Zahlen aus `results/*/PROTOTYPE_FINDINGS.md` und Abschnitt 3.4
des Übergabeprotokolls.

---

## 2. Voraussetzung: TWS oder IB Gateway (machst du selbst)

Das geht nicht aus der Entwicklungsumgebung: IBKR verlangt eine lokal laufende
GUI-Anwendung mit Anmeldung.

### 2.1 Paper-Konto

In der **Client Portal** deines IBKR-Kontos: *Einstellungen → Kontoeinstellungen
→ Paper Trading Account*. Gibt es noch keins, dort anfordern. Du bekommst einen
**eigenen Benutzernamen** — wenn dein Live-Login `U12345678` ist, lautet der
Paper-Login `DU12345678`. Die Kontonummer trägt dasselbe Präfix, und genau daran
erkennt die Brücke später, dass sie am richtigen Konto hängt.

### 2.2 TWS oder IB Gateway installieren

* **IB Gateway** ist das schlankere von beiden: kein Charting, nur die
  API-Verbindung. Für diesen Zweck die bessere Wahl.
* **TWS** (Trader Workstation) tut es auch und zeigt die Orders in einer
  Oberfläche — praktisch für die ersten Kontrollen.

Beide von der IBKR-Website herunterladen, installieren und **mit dem
Paper-Benutzernamen** anmelden (nicht mit dem Live-Login; es sind getrennte
Anmeldungen).

### 2.3 API-Verbindung freigeben

In TWS: *Datei → Globale Konfiguration → API → Einstellungen*
(in IB Gateway: *Configure → Settings → API → Settings*):

| Einstellung | Wert |
|---|---|
| **Enable ActiveX and Socket Clients** | **an** |
| **Read-Only API** | **aus** (sonst kann die Brücke keine Order senden — für `--pruefen` allein würde „an" genügen) |
| **Socket port** | **7497** bei TWS, **4002** bei IB Gateway |
| **Trusted IPs** | `127.0.0.1` |
| Allow connections from localhost only | an |

### 2.4 Die Ports — nachgeprüft

| | Live | **Paper** |
|---|---|---|
| **TWS** | 7496 | **7497** |
| **IB Gateway** | 4001 | **4002** |

Stand der Prüfung September 2026, Quelle: IBKRs eigene Dokumentation
([TWS API: Initial Setup](https://interactivebrokers.github.io/tws-api/initial_setup.html),
[Installing & Configuring TWS for the API](https://www.interactivebrokers.com/campus/trading-lessons/installing-configuring-tws-for-the-api/)).
Die Brücke verbindet **ausschließlich** auf 7497 oder 4002; die beiden
Live-Ports stehen namentlich auf einer Verbotsliste. Wenn du den Port in TWS
verstellst, muss das bewusst im Code nachgezogen werden — nicht in der `.env`.

### 2.5 Bibliothek installieren

```bash
pip3 install ib_async        # braucht Python 3.10 oder neuer
python3 -c "import ib_async; print(ib_async.__version__)"
```

### 2.6 In die `.env` eintragen

```bash
cd ~/trading-bot
cat >> .env <<'EOF'
IBKR_PAPER_KONTO=DU1234567        # deine Paper-Kontonummer (Pflicht für echte Orders)
IBKR_PAPER_PORT=7497              # optional; nur 7497 (TWS) oder 4002 (Gateway)
IBKR_PAPER_STUECK=1               # optional, Standard 1 Stück je Order
IBKR_PAPER_CLIENT_ID=42           # optional
EOF
chmod 600 .env
```

Es gibt **kein Passwort und keinen API-Schlüssel**: die Anmeldung passiert in
TWS, die API vertraut der lokalen Verbindung. Deshalb ist der Host im Code ein
Literal (`127.0.0.1`) — eine Variable dafür wäre die Möglichkeit, sich mit einer
TWS auf einem fremden Rechner zu verbinden, von der niemand weiß, an welchem
Konto sie hängt.

---

## 3. Die Sicherungen

| Sicherung | Wo |
|---|---|
| **Port**: nur 7497/4002, Live-Ports namentlich abgelehnt — geprüft bei jedem Verbindungsaufbau, nicht nur im Konstruktor | `ibkr_zugang.pruefe_port()` |
| **Konto**: jedes von TWS gemeldete Konto muss Paper sein (`DU`/`DF`), und das erwartete muss darunter sein — sonst wird sofort getrennt | `ibkr_zugang.pruefe_konten()` |
| Beide **unabhängig**: richtiger Port + Live-Konto → Abbruch; richtiges Konto + Live-Port → Abbruch | je ein Test |
| Host als **Literal** `127.0.0.1` | `ibkr_zugang.HOST` |
| `--pruefen` verbindet mit IBKRs **readonly-Flag** — diese Sitzung kann strukturell nicht handeln | `ibkr_spiegel._pruefen()` |
| **Trockenlauf ist der Standard**, Senden verlangt `--echt` | `ibkr_spiegel.main()` |
| **Keine Order außerhalb der Handelszeiten** — und die Zeiten kommen von IBKR selbst, nicht aus einem eigenen Kalender | `ibkr_paper.in_handelszeiten()` |
| **Notbremse**: `touch broker/STOP_IBKR` (eigene Datei, unabhängig von Binance) | **zweimal** geprüft: zu Beginn jedes Laufs — dann wird TWS gar nicht erst kontaktiert — *und* vor jeder Order |
| 5 Orders je Lauf, 20 in 24 h, höchstens 50 Stück je Order | `ibkr_zugang` |
| **Symbol-Übersetzung** nur für ausdrücklich hinterlegte Fälle (`BRK-B` → `BRK B`); jedes andere Sonderzeichen wird **abgelehnt**, nicht geraten | `ibkr_zugang.ibkr_symbol()` |
| **Kontrakt nur bei genau einem Treffer** — ein mehrdeutiges Kürzel wird abgelehnt | `ibkr_paper.kontrakt()` |
| Die Order trägt das bestätigte Konto **ausdrücklich**, `tif=DAY`, `outsideRth=False` | `ibkr_paper._marktorder()` |
| Keine doppelte Order: `UNIQUE(bot, trade_id, seite)` **und** eine abgeleitete `orderRef`, an der eine bereits gesendete Order wiedererkannt wird | `ibkr_spiegel` |
| Eine Order, die **draußen aber nicht ausgeführt** ist, wird **nicht** als Spiegelung eingetragen | `ibkr_spiegel.spiegle_eine()` |
| Bot-Datenbank über `file:…?mode=ro` | `broker/bot_db.py` |
| Rückgabewert 1 bei Fehlschlägen, damit Cron per Mail anschlägt | `ibkr_spiegel.main()` |

---

## 4. Handelszeiten — was wirklich passiert, und was ich nicht nachmessen konnte

**Was die Dokumentation sagt:** `MKT`- und `STP`-Orders funktionieren bei IBKR
**nur während der regulären Handelszeiten**. Außerhalb gehen nur `LMT` und
`STP LMT`, und das auch nur mit dem Order-Attribut `outsideRth = true`
([Outside RTH](https://www.interactivebrokers.com/campus/glossary-terms/outside-rth/),
[Trading Outside Regular Trading Hours](https://www.interactivebrokers.com/campus/trading-lessons/trading-outside-regular-trading-hours/)).

**Was daraus folgt — und worauf ich mich NICHT verlassen habe:** ob eine
Market-Order außerhalb der Zeiten *abgelehnt* wird oder als `PreSubmitted` bis
zur Eröffnung *liegen bleibt*, berichten Praktiker unterschiedlich, und ich
konnte es **nicht nachmessen**: IBKR braucht eine lokal laufende TWS mit
Anmeldung, und aus dieser Entwicklungsumgebung gibt es keine. Eine Brücke, die
auf der Antwort aufbaut, hätte also auf einer Vermutung gestanden.

**Deshalb stellt sich die Frage nicht.** Die Brücke **fragt die Börse selbst**:
`reqContractDetails` liefert `liquidHours` (die reguläre Sitzung) und
`timeZoneId`. Liegt der Zeitpunkt in keinem dieser Fenster, wird **nicht
gesendet** — die Aufgabe bleibt stehen und der nächste Lauf innerhalb der
Sitzung erledigt sie. Das deckt Feiertage und Halbtage automatisch ab, weil
IBKR sie in denselben Angaben mitteilt (`20260911:CLOSED`).

**Du kannst die empirische Antwort gefahrlos selbst erzeugen:**

```bash
python3 broker/ibkr_spiegel.py --zeitfenster AAPL
```

Das verbindet **nur lesend** und zeigt, was IBKR für dieses Symbol meldet:

```
AAPL -> AAPL  Zeitzone US/Eastern
liquidHours (regulaere Sitzung): 20260910:0930-20260910:1600;20260911:CLOSED;...
tradingHours (mit erweiterten Zeiten): 20260910:0400-20260910:2000;...
Jetzt handelbar: NEIN - ausserhalb der regulaeren Handelszeiten (naechste Sitzung 2026-09-14T09:30:00-04:00)
```

Wenn du es genau wissen willst, was IBKR mit einer Market-Order nach Schluss
macht: ruf das einmal abends auf und einmal während der US-Sitzung und
vergleiche. Ein Order-Versuch ist dafür **nicht** nötig.

### Die Folge, die man kennen muss: die Übernacht-Lücke

Der Bot arbeitet auf **Tageskerzen** und rechnet mit dem **Schlusskurs**. Läuft
sein Cronjob nach dem US-Schluss, entstehen seine Signale bei geschlossener
Börse. Die Brücke kauft dann **in der nächsten Sitzung** — also zu einem anderen
Kurs. Diese Differenz ist die Übernacht-Lücke, und sie ist **kein Fehler der
Brücke**, sondern die Grenze dessen, was sich an einer Tagesstrategie überhaupt
spiegeln lässt. Der Abgleichsbericht weist sie mit der Spalte **Verzug** aus,
damit sie nicht als Ausführungsqualität missverstanden wird.

Wer das enger haben will, bräuchte eine **MOC-Order** (Market-on-Close, füllt
zum offiziellen Schlusskurs, Annahmeschluss ca. 15:50 ET). Das wäre der
genauere Spiegel für eine Tagesstrategie — aber ein eigener Schritt mit eigener
Fristen-Logik. Nicht eingebaut; sag Bescheid, wenn du ihn willst.

---

## 5. Gestaffelte Einführung — in dieser Reihenfolge

### Schritt 1 — Selbsttests (keine TWS, keine Verbindung nötig)

```bash
cd ~/trading-bot
python3 broker/test_ibkr.py
```

Erwartet **mit** installiertem `ib_async`:
`200 von 200 Pruefungen bestanden, 0 fehlgeschlagen.`

Erwartet **ohne** `ib_async`:
`168 von 168 Pruefungen bestanden, 0 fehlgeschlagen.`,
davor eine Zeile `UEBERSPRUNGEN: test_gegen_echte_bibliothek`.

Die kleinere Zahl ist **kein Fehler**: ohne die Bibliothek läuft alles außer
Abschnitt 13, und das wird sichtbar als „uebersprungen" gemeldet. Abschnitt 13
ist der einzige, der die Bibliothek braucht — er prüft, ob deren Schnittstelle
noch zu den Annahmen dieses Codes passt.

### Schritt 2 — Verbindung und Konto (verbindet NUR LESEND)

TWS/Gateway starten, am Paper-Konto anmelden, dann:

```bash
python3 broker/ibkr_spiegel.py --pruefen
```

Erwartet:

```
Host (fest im Code): 127.0.0.1
Port: 7497 (TWS), erlaubt sind (4002, 7497)
Erwartetes Konto (IBKR_PAPER_KONTO): DU1234567
Verbindung steht, NUR LESEND (IBKRs readonly-Flag gesetzt).
Bestaetigtes Paper-Konto: DU1234567
Notbremse: nicht gesetzt
Stueck je Order: 1
```

Beim **ersten** Verbindungsaufbau zeigt TWS eine Rückfrage
(„Incoming connection attempt … Allow?"). Bestätigen und „Don't ask again"
setzen, sonst hängt der Cronjob später an diesem Dialog.

Fehlermeldungen und was sie bedeuten:

| Meldung | Ursache |
|---|---|
| „Laeuft TWS bzw. IB Gateway …" | Anwendung nicht gestartet, oder „Enable ActiveX and Socket Clients" nicht gesetzt, oder falscher Port |
| „ist kein Paper-Konto" | TWS ist am **Live**-Konto angemeldet — ausloggen, mit dem `DU`-Login neu anmelden |
| „das erwartete Konto … ist nicht unter den gemeldeten" | `IBKR_PAPER_KONTO` in der `.env` stimmt nicht mit der Sitzung |
| „Port … ist der LIVE-Port" | `IBKR_PAPER_PORT` zeigt auf 7496/4001 |

### Schritt 3 — Handelszeiten ansehen (liest nur)

```bash
python3 broker/ibkr_spiegel.py --zeitfenster AAPL
```

### Schritt 4 — Was zu tun wäre, ohne es zu tun

```bash
python3 broker/ibkr_spiegel.py --status    # welche Trades offen sind
python3 broker/ibkr_spiegel.py             # TROCKENLAUF, sendet nichts
```

Gegen die Bot-Datenbank halten:

```bash
sqlite3 paper_trading_volatility_breakout.db \
  "SELECT id, symbol, entry_price, status FROM trades WHERE status='open';"
```

### Schritt 5 — Die erste echte Order, von Hand, **während der US-Sitzung**

Zwischen 15:30 und 22:00 deutscher Zeit (Winterzeit: 15:30–22:00, Sommerzeit
ebenso — maßgeblich ist, was `--zeitfenster` sagt). Vorher die Notbremse
ausprobieren:

```bash
touch broker/STOP_IBKR                      # Sicherung
python3 broker/ibkr_spiegel.py --echt       # muss "NOTBREMSE aktiv" melden
                                            # (auch bei NULL offenen Aufgaben)
rm broker/STOP_IBKR                         # Sicherung lösen
python3 broker/ibkr_spiegel.py --echt       # jetzt geht EINE Order raus
```

Drei Kontrollen danach:

```bash
# 1. Das eigene Protokoll
tail -5 logs/broker/ibkr_paper_spiegel.log

# 2. Die eigene Nachverfolgung
sqlite3 broker_ibkr_volatility_breakout.db \
  "SELECT trade_id, seite, symbol, ibkr_symbol, konto, order_id, stueck,
          ausfuehrungspreis, simulationspreis, gebuehr FROM spiegelungen;"

# 3. Die Bot-Datenbank ist unberührt
sqlite3 paper_trading_volatility_breakout.db \
  "SELECT status, COUNT(*) FROM trades GROUP BY status;"
```

Und in TWS unter **Trades / Orders**: genau diese Order, mit derselben
Order-ID, im Konto `DU…`.

**Gegenprobe, die sich lohnt:** `--echt` noch einmal aufrufen. Es darf **keine**
zweite Order entstehen — das ist die Sperre, die im Cron-Betrieb am wichtigsten
ist.

### Schritt 6 — Abgleich ansehen

```bash
python3 broker/ibkr_abgleich.py
```

### Schritt 7 — Erst jetzt automatisieren, und **anders als bei Binance**

Krypto läuft 24/7, da gehört die Brücke direkt hinter den Bot. **Hier nicht:**
der Aktien-Bot läuft nach dem US-Schluss, die Börse ist dann zu. Die Brücke
braucht einen **eigenen** Eintrag, der während der US-Sitzung greift:

```cron
# Bruecke alle 30 Minuten waehrend der US-Sitzung (15:30-22:00 MEZ/MESZ),
# montags bis freitags. Die Bruecke prueft selbst, ob die Boerse offen ist -
# der Zeitplan ist die Bequemlichkeit, die Pruefung ist die Sicherung.
*/30 15-21 * * 1-5 cd ~/trading-bot && /usr/bin/python3 broker/ibkr_spiegel.py --echt >> logs/broker/ibkr_cron.log 2>&1
```

Prüfen und abschalten:

```bash
crontab -l | grep ibkr_spiegel
touch ~/trading-bot/broker/STOP_IBKR    # Cron läuft weiter, sendet nichts
rm ~/trading-bot/broker/STOP_IBKR
```

**TWS muss dafür laufen.** Eine abgemeldete TWS heißt: kein Spiegel, und im
Protokoll eine Zeile „Laeuft TWS …". TWS trennt die API-Sitzung außerdem
standardmäßig einmal täglich beim Neustart (*Configure → Lock and Exit → Auto
restart*) — IB Gateway ist dafür die robustere Wahl.

---

## 6. Beispiel eines Abgleichsberichts

Synthetisch erzeugt (Attrappe statt TWS), damit die Form vor der ersten echten
Order sichtbar ist:

```
======================================================================================================================
ABGLEICH Simulation <-> IBKR PAPER - Bot volatility_breakout
======================================================================================================================
Konto: DU1234567
Gespiegelte Trades: 3 (vollstaendig, also Kauf UND Verkauf: 2)
Kostenannahme der Simulation: 0.30 Prozentpunkte je Trade (Gebuehr + Slippage, pauschal)

Trade Symbol   Einstieg sim /  echt   Abw %  Verzug   Ausstieg sim /  echt   Abw %    PnL sim  PnL echt   Diff pp
----------------------------------------------------------------------------------------------------------------------
    1 AAPL          200.00      201.70    0.85       1      212.00      211.21   -0.37      5.70      4.21     -1.49
    2 MSFT          400.00      404.40    1.10       1      368.00      366.87   -0.31     -8.30     -9.52     -1.22
    3 AAPL          198.00      201.70    1.87       0           -           -       -         -         -         -
----------------------------------------------------------------------------------------------------------------------
Mittelwerte: Einstiegsabweichung 1.274 %, Ausstiegsabweichung -0.340 %, PnL-Unterschied -1.355 Prozentpunkte, Verzug 0.7 Tage

NICHT gespiegelt (1):
  Trade 4 eroeffnung MSFT  Trade war schon geschlossen, bevor die Eroeffnung gespiegelt wurde - es wird NICHT nachgekauft
```

**Wie man das liest:** der PnL-Unterschied von −1,3 Prozentpunkten ist **nicht**
die Ausführungsqualität. Die Spalte **Verzug** zeigt 1 Tag — die Brücke hat am
Tag nach dem Signal gekauft, und der Kurs war über Nacht um ~1 % gestiegen.
Genau deshalb steht der Verzug in der Tabelle. Bei Verzug 0 wäre die Abweichung
aussagekräftig.

Die zwei getrennten Renditen der Binance-Brücke (je Einheit gegen eingesetztes
Kapital) braucht es hier **nicht**: IBKR rechnet die Provision in USD ab, nicht
in der Aktie. Es bleibt keine Restmenge liegen, gekaufte und verkaufte
Stückzahl sind gleich — eine Stolperfalle weniger als bei Krypto.

---

## 7. Tägliche Kontrolle

```bash
python3 broker/ibkr_spiegel.py --status
python3 broker/ibkr_abgleich.py
grep -E "FEHLGESCHLAGEN|OFFEN" logs/broker/ibkr_paper_spiegel.log | tail
```

---

## 8. Dateien

| Datei | Inhalt |
|---|---|
| `broker/ibkr_zugang.py` | `.env`, Port- und Konto-Regeln, Notbremse, Grenzen, Symbol-Übersetzung |
| `broker/ibkr_paper.py` | die einzige Stelle mit `ib_async`: Verbindung, Kontrakt, Handelszeiten, Order |
| `broker/ibkr_spiegel.py` | die Brücke: liest den Bot, entscheidet, sendet, protokolliert |
| `broker/ibkr_abgleich.py` | Bericht Simulation ↔ Ausführung |
| `broker/test_ibkr.py` | **200** Prüfungen mit `ib_async`, **168** ohne (Abschnitt 13 wird dann sichtbar übersprungen) — in beiden Fällen ohne TWS und ohne Verbindung |
| `broker/bot_db.py` | der gemeinsame, schreibgeschützte Leser beider Brücken |
| `broker_ibkr_volatility_breakout.db` | eigene Nachverfolgung (`.gitignore`) |
| `logs/broker/ibkr_paper_spiegel.log` | jede Order mit vollem Kontext |
| `broker/STOP_IBKR` | existiert diese Datei, wird nichts gesendet |

---

## 9. Größte verbleibende Risiken

1. **Nie gegen eine echte TWS gelaufen.** Ich konnte keine starten — deshalb die
   gestaffelte Anleitung, der readonly-Prüfschritt und die Notbremse. Abschnitt
   13 der Selbsttests prüft wenigstens, dass die Schnittstelle von `ib_async`
   noch zu den Annahmen dieses Codes passt.
2. **TWS muss laufen und angemeldet sein.** Der häufigste Ausfall wird kein
   Fehler der Brücke sein, sondern eine abgemeldete TWS nach dem täglichen
   Neustart.
3. **Die Übernacht-Lücke dominiert die Messung** (Abschnitt 4). Ohne die Spalte
   Verzug wäre der Bericht irreführend.
4. **Ein Paper-Konto ist eine Simulation.** IBKR füllt gegen echte Kurse und
   Orderbücher, aber die eigene Order bewegt den Markt nicht — genau das tut
   eine echte.
5. **Cron läuft unbeaufsichtigt.** Rückgabewert 1 bei Fehlschlägen, Grenzen im
   Code, Notbremse als Datei. Nach dem Einrichten ein paar Läufe mitlesen.

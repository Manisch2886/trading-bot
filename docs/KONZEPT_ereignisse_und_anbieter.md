# Konzept: zentrale Ereignis-Datenbank und Anbieter-Schnittstelle

**Entwurfsdokument, kein Produktivcode.** Stand 12.09.2026, Basis `origin/main`
(`e93ae56`, nach Merge von #81). Alle Code-Ausschnitte sind **Skizzen im
Dokument**, keine Dateien im Repo.

Geschrieben für eine Entscheidung. Abschnitt 1 listet, was zu entscheiden ist;
alles Weitere ist Begründung.

---

## 1. Was zu entscheiden ist

Zwölf Fragen. Bei jeder steht eine Empfehlung — aber keine ist getroffen.

| # | Frage | Empfehlung | steht in |
|---|---|---|---|
| **E1** | Ereignis-DB: **eine** Tabelle oder eine je Bereich? | eine, mit `art`-Spalte | 2.4 |
| **E2** | Feste Spalten oder freies JSON für Ereignisdetails? | **beides**: feste Spalten für alles Abfragbare, JSON nur für den Rest | 2.4 |
| **E3** | Zählen **Läufe** als Ereignisse (auch ohne Signal)? | **ja** — sonst bleibt offener Punkt 12 ungelöst | 2.3, 2.8 |
| **E4** | Wer schreibt: jeder direkt oder eine gemeinsame Funktion? | gemeinsame Funktion in `shared/`, aber **nicht** in den Bots | 2.5 |
| **E5** | Die drei vorhandenen DBs migrieren oder Stichtag? | **Stichtag**, die drei bleiben liegen | 2.6 |
| **E6** | Aufbewahrung: wie lange, was wird verdichtet? | Rohdaten 400 Tage, dann Tagesverdichtung | 2.8 |
| **A1** | Registrierung statt Konfiguration — hält das? | **ja**, mit einer benannten Ausnahme | 3.2 |
| **A2** | Wie wird „liest" von „handelt" unterschieden? | zwei getrennte Basisklassen, nicht ein Flag | 3.4 |
| **A3** | Wie wird Echtgeld von Paper getrennt? | eigene DB-Datei je Welt, keine gemeinsame Tabelle | 3.5 |
| **A4** | Crash-Knopf bei mehreren Anbietern? | **nicht** erweitern — Begründung in 3.6 | 3.6 |
| **A5** | Welche Anbieter zuerst? | keiner — erst E1–E6 | 3.8 |
| **R1** | Wird der Mac zum Server, oder bleibt die Grenze? | Entscheidung offen, Folgen in 1.1 benannt | 1.1 |

**Was dieser Entwurf nicht entscheiden kann:** R1. Alles andere hängt daran nur
im Umfang, nicht in der Richtung.

---

## 1.1 Zwei Rahmenbedingungen, die durchschlagen

### Alles hängt an einem MacBook

Cron, Dashboard, Telegram-Bot und beide Brücken laufen auf einem Laptop, der
aufgeklappt und wach bleiben muss. Am 11.09.2026 schlief er von etwa 08:50 bis
12:06; der 12:05-Lauf der Binance-Brücke fiel komplett aus, mehrere stündliche
Forward-Tests ebenfalls. **Cron holt nichts nach.**

Wo das im Entwurf durchschlägt — vier Stellen, an denen kein Code hilft:

1. **Die Ereignis-DB kann nur aufzeichnen, was passiert ist.** Ein Bot, der nie
   lief, erzeugt kein Ereignis. Eine Lücke im Zeitstrahl ist deshalb
   zweideutig — „nichts passiert" oder „nichts lief" —, solange nicht jeder
   Lauf selbst ein Ereignis ist (**E3**). Das ist das stärkste Argument für E3
   und zugleich der Grund, warum offener Punkt 12 des Übergabeprotokolls ohne
   sie nicht lösbar ist.
2. **„Immer erreichbar" ist nicht erreichbar.** Eine App, die Push-Nachrichten
   verschickt, verschickt keine, während der Rechner schläft. Jede Zusage in
   diese Richtung wäre unehrlich.
3. **Aufbewahrung ist an den Rechner gebunden.** Verliert man den Mac, verliert
   man den gesamten Zeitstrahl. Ein Auslagern in die Cloud löst das, reisst
   aber ein neues Fass auf (Zugangsdaten, Datenschutz, Kosten) und ist bewusst
   nicht Teil dieses Entwurfs.
4. **Nebenläufigkeit bleibt lokal.** Alles, was in 2.7 zu SQLite steht, gilt für
   genau einen Rechner. Auf zwei Rechnern gälte es nicht mehr — das ist die
   erste Stelle, an der R1 den Entwurf umwirft.

### Das Dashboard ist kein Anzeigewerkzeug mehr

Seit PR #62 liegt der Crash-Knopf darin, seit #71 legen Warteaufträge Arbeit an,
die ein Cronjob später **ohne Rückfrage** ausführt. Benutzt wird fast
ausschliesslich ein iPhone mit 390 px.

Eine Notfalloberfläche muss in zwei Sekunden bedienbar sein. Jede Verdichtung,
jeder Filter, jede Kachel arbeitet dagegen. Der Entwurf zieht daraus eine
Konsequenz, die überall wiederkehrt: **der Ereignis-Zeitstrahl gehört auf eine
eigene Seite**, nicht auf die Übersicht — so wie die Portfolio-Sicht aus PR #80,
und aus demselben Grund. Die Übersichtsseite darf durch nichts, was hier
entworfen wird, langsamer oder länger werden.

---

# Teil 1 — Zentrale Ereignis-Datenbank

## 2.1 Bestandsaufnahme: die drei vorhandenen Nachverfolgungen

| | `broker/spiegel.py` | `broker/ibkr_spiegel.py` | `notifications/schliess_benachrichtigung.py` |
|---|---|---|---|
| Datei | `broker_testnet_<bot>.db` | `broker_ibkr_<bot>.db` | `benachrichtigungen_schliessung.db` |
| Haupttabelle | `spiegelungen` | `spiegelungen` | `gemeldet` |
| Eindeutigkeit | `UNIQUE(bot, trade_id, seite)` | `UNIQUE(bot, trade_id, seite)` | `UNIQUE(bot, trade_id)` |
| zweite Tabelle | `versuche` (jeder Versuch, auch Fehlschlag) | `versuche` | `zustand` (Schlüssel/Wert) |
| Zustände | keine Spalte; `status` = Börsenstatus | dito | `wird_gesendet` / `gesendet` / `erstlauf_uebersprungen` |
| Anspruch-Verfahren | keins — die Order **ist** der Anspruch, Wiedererkennung über `client_order_id` | dito über `order_ref` | **dreistufig**: Anspruch → senden → bestätigen |
| Zeitstempel | `zeitpunkt TEXT` (UTC-Text) | dito | dito |
| Rohantwort | `antwort TEXT` (JSON) | `antwort TEXT` | — |

**Drei Gemeinsamkeiten, die das gemeinsame Schema tragen:**

1. **Ein fachlicher Schlüssel mit `UNIQUE`, nicht eine `if`-Abfrage.** Alle drei
   verhindern Doppelarbeit strukturell. Zwei gleichzeitig gestartete Läufe
   scheitern an der Datenbank, nicht an einer Prüfung, die dazwischen veralten
   kann.
2. **Erfolg und Versuch sind getrennt.** Beide Brücken führen `versuche` neben
   `spiegelungen` — ausdrücklich, weil ein Fehlschlag den `UNIQUE`-Platz nicht
   belegen darf, sonst wäre der nächste Versuch blockiert. Das ist die
   wichtigste Einzelerkenntnis für den Entwurf.
3. **Zeitstempel als UTC-Text**, nicht als lokale Zeit, nicht als Zahl.

**Der Unterschied, der erklärungsbedürftig ist:** nur die
Schliess-Benachrichtigung kennt Zustände. Sie braucht sie, weil ihr Anspruch
und ihre Ausführung auseinanderfallen — zwischen „ich melde diesen Trade" und
„die Nachricht ist raus" liegt ein Netzaufruf, der scheitern kann. Bei den
Brücken übernimmt die `client_order_id` diese Rolle: die Börse selbst weiss,
ob die Order schon da ist. **Die gemeinsame Tabelle braucht deshalb Zustände**
— sie muss beide Fälle tragen.

## 2.2 Der Gegenentwurf und was er lehrt

`notifications/monitor.py` mit `notifications/state.json` ist die ältere
Bauart, und sie wurde wegen ihrer Schwächen abgelöst (PR #78):

* **Mengenvergleich statt Vermerk je Vorgang.** `known_open_ids` und `max_id`
  beschreiben einen Zustand, nicht eine Historie. Was zwischen zwei Läufen
  auf- und wieder zuging, kommt darin nicht vor — die bekannte
  5-Minuten-Lücke.
* **Ein verlorener Zustand verschluckt still.** Fehlt `state.json`, schreibt
  die Baseline-Logik einen neuen Anfangszustand, und alles im Fenster ist weg.
  Ohne Fehlermeldung.
* **Die Reihenfolge war einmal falsch herum.** Der Docstring dokumentiert den
  Vorfall: `state.json` wurde gespeichert, **bevor** der Versand bestätigt war.
  Ergebnis: ein Ereignis galt als gemeldet, ohne je verschickt worden zu sein.

**Drei Lehren für den Entwurf**, alle drei bindend:

1. **Je Vorgang eine Zeile, nie eine Zustandsmenge.** Eine Ereignis-DB, die
   „was ist neu seit dem letzten Mal?" über einen Mengenvergleich beantwortet,
   hat denselben Fehler eingebaut.
2. **Der Vermerk wird erst bestätigt, wenn die Wirkung eingetreten ist.** Und
   zwischen Anspruch und Bestätigung darf ein Abbruch nicht zu „gilt als
   erledigt" führen.
3. **Ein verlorener Zustand muss auffallen, nicht stillschweigend neu
   beginnen.** Die Schliess-Benachrichtigung löst das mit der Marke
   `erstlauf_am`: fehlt sie bei vorhandenen Vermerken, wird der Erstlauf
   **abgelehnt** und laut gemeldet.

## 2.3 Welche Ereignisarten es gibt

Vollständig aus dem heutigen Repo erhoben. Die Spalte „heute" sagt, wo es
derzeit landet.

| Art | Auslöser | heute |
|---|---|---|
| `trade_eroeffnet` | Bot öffnet Position | Telegram (`monitor.check_for_events`) |
| `trade_geschlossen` | Bot schliesst Position | Telegram (`schliess_benachrichtigung.py`) |
| `lauf_begonnen` / `lauf_beendet` | Cronjob eines Bots | **nirgends** (offener Punkt 12) |
| `lauf_fehler` | Traceback im Cron-Log | Telegram (`_scan_log_for_errors`) |
| `lauf_ueberfaellig` | Bot älter als erwarteter Takt | Telegram (Staleness-Prüfung) |
| `bruecken_order` | Order an Testnet/Paper-Konto | `spiegelungen` + Telegram |
| `bruecken_versuch` | Trockenlauf, Fehlschlag, Übersprungenes | `versuche` |
| `bruecken_abweichung` | Ausführungs- ≠ Simulationspreis | nur in `spiegelungen`, Spalte `Abw %` |
| `notbremse` | `broker/STOP` gezogen | Cron-Log |
| `manueller_eingriff` | Position von Hand geschlossen | `logs/notifications/manuelle_eingriffe.log` |
| `warteauftrag_angelegt` / `_ausgefuehrt` / `_storniert` | Dashboard bei geschlossener Börse | `warteauftraege.json` + Protokoll |
| `agenten_hinweis` | vier Claude-Agenten + Quartals-Interpreter | E-Mail |
| `datenluecke_kurse` | unvollständige Kerze (PR #81) | Ausgabe des Laders |
| `datenluecke_lauf` | Ausfall, weil der Mac schlief | `docs/DATENLUECKEN.md`, **von Hand** |
| `dienst_neustart` | launchd startet Dashboard/Bot/caffeinate neu | `logs/*/launchd.*.log` |
| `log_rotation` | Rotation hat geschnitten (PR #79) | `logs/system/log_rotation.log` |
| `portfolio_berechnet` | Portfolio-Sicht neu gerechnet (PR #80) | Zwischenspeicher |

**Siebzehn Arten, verteilt auf sieben Ablageorte** — Telegram, zwei
Nachverfolgungs-DBs, eine JSON-Datei, zwei Logdateien, E-Mail und ein
Markdown-Dokument, das von Hand gepflegt wird. Genau das ist das Problem.

**Die drei, die heute nirgends abfragbar landen**, sind zugleich die, die am
meisten fehlen: `lauf_begonnen`/`lauf_beendet` (blockiert Punkt 12 und die
Systemgesundheits-Seite), `agenten_hinweis` (verschwindet im Postfach) und
`bruecken_abweichung` (steht in einer Spalte, die niemand ansieht).

## 2.4 Das Schema

### Entscheidung E1: eine Tabelle

```sql
CREATE TABLE IF NOT EXISTS ereignisse (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    art           TEXT NOT NULL,      -- aus der Liste in 2.3
    quelle        TEXT NOT NULL,      -- 'bot:t3_supertrend', 'bruecke:binance', 'dashboard'
    bot           TEXT,               -- NULL bei botfremden Ereignissen
    symbol        TEXT,
    trade_id      INTEGER,
    schwere       TEXT NOT NULL,      -- 'info' | 'warnung' | 'fehler'
    zeitpunkt     TEXT NOT NULL,      -- UTC-Text, wie in allen drei Vorbildern
    text          TEXT NOT NULL,      -- eine Zeile, menschenlesbar
    details       TEXT,               -- JSON, siehe E2
    schluessel    TEXT,               -- fachlicher Schluessel, siehe unten
    UNIQUE(art, schluessel)
);
CREATE INDEX ereignisse_zeit ON ereignisse (zeitpunkt);
CREATE INDEX ereignisse_bot  ON ereignisse (bot, zeitpunkt);
```

*Alternative:* eine Tabelle je Bereich (Trades, Brücke, System). **Verworfen**,
weil der Zweck der Übung ein **einziger** Zeitstrahl ist; drei Tabellen
bedeuten drei Abfragen und drei Gelegenheiten, eine zu vergessen. Der Preis:
viele Spalten sind für viele Arten `NULL`. Das ist in SQLite billig.

### Entscheidung E2: feste Spalten **und** JSON

Die Abwägung, die der Auftrag verlangt:

| | nur feste Spalten | nur JSON | beides |
|---|---|---|---|
| Abfragbar | ja | nur mit `json_extract`, ohne Index | ja, für das Wesentliche |
| Neue Ereignisart | Migration nötig | kostenlos | kostenlos, solange keine neue Abfrage nötig |
| Schema-Disziplin | hoch | keine — jedes Skript erfindet eigene Feldnamen | mittel |
| Lesbar im Notfall | ja | ja | ja |

**Empfehlung: beides, mit einer klaren Grenze.** Alles, wonach die Oberfläche
je filtern soll, bekommt eine eigene Spalte — `art`, `bot`, `symbol`,
`trade_id`, `schwere`, `zeitpunkt`. Alles andere (Ausführungspreis, Order-ID,
Gebühren, Abweichung, Traceback-Ausschnitt) geht als JSON in `details`.

Die Gefahr bei JSON ist nicht die Abfragbarkeit, sondern der Wildwuchs: fünf
Skripte, die dasselbe Feld `preis`, `price` und `ausfuehrungspreis` nennen. Die
Gegenmassnahme steht in E4 — nur eine Funktion schreibt, und sie kennt je Art
die erwarteten Felder.

### Der fachliche Schlüssel — der Kern der Übung

`UNIQUE(art, schluessel)` überträgt das, was alle drei Vorbilder richtig
machen. Je Art ist der Schlüssel festgelegt, zum Beispiel:

| Art | `schluessel` |
|---|---|
| `trade_geschlossen` | `t3_supertrend:1487` |
| `bruecken_order` | `t3_supertrend:1487:eroeffnung` |
| `lauf_beendet` | `t3_supertrend:2026-09-12T12:00Z` |
| `lauf_ueberfaellig` | `t3_supertrend:2026-09-12` (einmal am Tag, nicht je Prüflauf) |

Damit gilt für die gemeinsame Tabelle dieselbe strukturelle Zusicherung wie
heute je Einzelfall: **dasselbe Ereignis kann nicht zweimal drinstehen**, auch
wenn zwei Cronjobs gleichzeitig starten.

Für Arten ohne natürlichen Schlüssel (`lauf_fehler` mit wechselndem Text)
bleibt `schluessel` `NULL` — und `UNIQUE` greift in SQLite bei `NULL` nicht,
mehrere Zeilen sind also erlaubt. Das ist gewollt und muss im Code
kommentiert stehen, sonst wirkt es wie ein Loch.

### Zustände: nur wo sie gebraucht werden

Die Tabelle oben hat **keine** Zustandsspalte. Zustände gehören nicht zum
Ereignis, sondern zu seiner **Zustellung** — und die betrifft nur einen Teil
der Arten. Deshalb eine zweite Tabelle:

```sql
CREATE TABLE IF NOT EXISTS zustellungen (
    ereignis_id INTEGER NOT NULL REFERENCES ereignisse(id),
    kanal       TEXT NOT NULL,        -- 'telegram' | 'mail' | 'dashboard'
    zustand     TEXT NOT NULL,        -- 'offen' | 'wird_gesendet' | 'gesendet' | 'fehlgeschlagen'
    versuche    INTEGER NOT NULL DEFAULT 0,
    zeitpunkt   TEXT NOT NULL,
    grund       TEXT,
    UNIQUE(ereignis_id, kanal)
);
```

Das ist genau das dreistufige Verfahren der Schliess-Benachrichtigung,
verallgemeinert: **Anspruch nehmen → senden → bestätigen**, je Kanal getrennt.
Ein fehlgeschlagener Telegram-Versand blockiert dann nicht die Anzeige im
Dashboard, und das Ereignis selbst bleibt unabhängig davon bestehen.

*Der bekannte Grenzfall bleibt bestehen:* bricht ein Lauf zwischen Senden und
Bestätigen ab, steht `wird_gesendet` da und der Kanal versucht es nicht erneut.
Ob die Nachricht raus war, ist dann unbekannt. Das ist in PR #78 bewusst so
entschieden worden und wird hier übernommen — eine Auflösung bräuchte einen
Lesezugriff auf den Telegram-Verlauf.

## 2.5 Wer schreibt — und die harte Randbedingung

**`forward_test.py` und `live_params.py` dürfen nicht angefasst werden.** Damit
können die neun Bots **nichts melden**. Das ist keine Nebenbedingung, das ist
die formende Kraft des ganzen Entwurfs.

Daraus folgt eine Zweiteilung, die im Dokument bleiben muss:

| | wer schreibt | wie |
|---|---|---|
| **Selbstmelder** | Brücken, Dashboard, Benachrichtigungsskripte, Agenten, Log-Rotation, Portfolio-Sicht | rufen die gemeinsame Schreibfunktion direkt auf |
| **Fremdbeobachtete** | die neun Bots | ein **Sammler** liest ihre Spuren und schreibt die Ereignisse |

### Der Sammler

Ein eigener Cronjob (Vorschlag: `shared/ereignis_sammler.py`, alle 15 Minuten),
der genau das tut, was `monitor.py` heute tut — nur mit Vermerk je Vorgang
statt Mengenvergleich:

* **Trades**: liest die neun Bot-DBs schreibgeschützt über `broker/bot_db.py`
  und erzeugt `trade_eroeffnet` / `trade_geschlossen`. Der `UNIQUE`-Schlüssel
  macht Wiederholungen folgenlos — der Sammler darf beliebig oft laufen.
* **Läufe**: hier wird es unangenehm ehrlich. Ohne Änderung an
  `forward_test.py` gibt es **keine** verlässliche Quelle für „Lauf
  stattgefunden". Drei mögliche Ersatzquellen, alle mit Mängeln:

| Quelle | taugt für | Mangel |
|---|---|---|
| Änderungszeit von `logs/<bot>/cron.log` | „irgendwann lief etwas" | ein Lauf ohne Ausgabe ändert nichts; Log-Rotation setzt sie zurück |
| Neue Zeilen im Cron-Log | Läufe mit Ausgabe | ein stiller Lauf bleibt unsichtbar |
| `launchd`/Cron-Mail | Fehlläufe | nur bei Fehlern, und die Mails sind abgeschaltet |

**Damit ist E3 eine echte Entscheidung mit Preis:** „Läufe als Ereignisse" ist
richtig und löst offenen Punkt 12 — aber **sauber lösbar ist es nur mit einer
Zeile in `forward_test.py`**, und die ist verboten. Der Entwurf empfiehlt
deshalb:

> **Kurzfristig** den Sammler mit der Log-Heuristik bauen und die Ereignisse
> ausdrücklich als `quelle='heuristik'` kennzeichnen — eine Aussage mit
> angeschriebener Unsicherheit ist mehr wert als keine.
> **Mittelfristig** dem Nutzer die eine Zeile in `forward_test.py` als eigene,
> kleine Entscheidung vorlegen (ein `ereignis(...)`-Aufruf am Anfang und am
> Ende des Laufs). Sie wäre der Unterschied zwischen „vermutlich gelaufen" und
> „gelaufen".

Das ist bewusst als **Frage** formuliert und nicht als Vorgriff.

### Die gemeinsame Schreibfunktion (E4)

```python
# shared/ereignisse.py - Skizze, keine Datei
def schreibe(art, quelle, text, *, bot=None, symbol=None, trade_id=None,
             schwere="info", schluessel=None, details=None) -> int | None:
    """Schreibt ein Ereignis. Gibt die id zurueck - oder None, wenn es
    bereits da war oder das Schreiben scheiterte. Wirft NIE."""
```

*Alternative:* jeder schreibt selbst per SQL. **Verworfen** — dann gibt es
sieben Fassungen der Regel, welcher Schlüssel zu welcher Art gehört, und der
JSON-Wildwuchs aus E2 ist unvermeidbar.

Die Funktion lebt in `shared/`, weil die drei Schreiber-Gruppen (Brücken,
Benachrichtigungen, Dashboard) sonst keinen gemeinsamen Ort haben. Sie
importiert **nichts** aus `strategies/` — dieselbe Namenskollision wie überall.

## 2.6 Migration oder Stichtag (E5)

**Empfehlung: Stichtag.** Die drei vorhandenen Datenbanken bleiben, wo sie
sind, und werden **nicht** übernommen.

*Begründung:* sie sind keine Ereignis-Historien, sondern Arbeitsvermerke.
`spiegelungen` beantwortet „ist diese Order schon draussen?" — eine Frage, die
die Brücke bei jedem Lauf neu stellt und die sie weiterhin selbst beantworten
muss. Würde man sie in die Ereignis-DB überführen, hinge die
Doppelversand-Sicherung der Brücke plötzlich an einer Tabelle, die auch das
Dashboard beschreibt. Das ist genau die Kopplung, die dieses Projekt
sonst überall vermeidet.

*Die Alternative* (Migration) hätte einen echten Vorteil: der Zeitstrahl
begänne nicht bei null, sondern mit der Geschichte beider Brücken. Wer das
will, kann sie **nachträglich** als Einmal-Import einspielen — die Schlüssel
sind kompatibel (`bot:trade_id:seite`), es ist also kein Entweder-oder,
sondern eine Reihenfolge. Deshalb steht Migration in 4. als **optionaler**
Schritt 7 und nicht als Voraussetzung.

**Was der Stichtag kostet:** in den ersten Wochen ist der Zeitstrahl dünn, und
eine „Was ist seit gestern passiert?"-Ansicht zeigt wenig. Bei ~22 geschlossenen
Trades über alle neun Bots bis heute ist das aber ohnehin die Lage.

## 2.7 Nebenläufigkeit — mit Zahlen

Die heutigen Takte, aus den READMEs und dem Übergabeprotokoll:

| Schreiber | Takt | Starts/Tag |
|---|---|---|
| Warteaufträge ausführen | `*/5` | 288 |
| Schliess-Benachrichtigung | `*/15` | 96 |
| Telegram-Bot (Dienst) | alle 5 min | 288 |
| Elliott Wave (Krypto) | stündlich | 24 |
| IBKR-Brücke | `*/30 15-21 Mo-Fr` | ~14 (werktags) |
| T3/SuperTrend + Binance-Brücke | alle 4 h | 6 + 6 |
| sechs weitere Bots | täglich | 6 |
| Log-Rotation, Portfolio-Sicht | täglich 3:30 / 3:40 | 2 |

**Rund 730 Prozessstarts am Tag, die schreiben könnten.** Die Kollisionsgefahr
ist aber nicht proportional dazu, sondern zur **Schreibdauer**: ein
`INSERT` mit Commit auf lokaler SSD liegt im einstelligen Millisekunden-Bereich.
Bei grosszügig geschätzten 2.000 Schreibvorgängen am Tag à 5 ms ist die
Datenbank rund **10 Sekunden von 86.400** beschäftigt — 0,01 %.

Das ist nicht der eigentliche Punkt. **Cronjobs starten auf der Minute**, nicht
gleichverteilt: zur vollen Viertelstunde starten `*/5` und `*/15` zusammen, zur
vollen Stunde kommt der stündliche Bot dazu, um 3:30 und 3:40 die
Tagesaufgaben. Kollisionen sind also selten, aber **gebündelt** — und damit
genau dann, wenn ohnehin viel los ist.

**Was heute passiert, wenn es kollidiert:** SQLite sperrt die ganze Datei.
Python wartet dann bis `timeout` (Voreinstellung 5 s) und wirft sonst
`database is locked`. **Bemerkenswert:** von allen Schreibpfaden im Repo setzt
nur `notifications/manual_close.py` das ausdrücklich (`busy_timeout`,
`isolation_level=None`). Die drei Nachverfolgungs-DBs laufen auf der
Voreinstellung, und **WAL benutzt niemand**.

**Empfehlung für die Ereignis-DB:**

```python
conn = sqlite3.connect(pfad, timeout=10.0, isolation_level=None)
conn.execute("PRAGMA journal_mode = WAL")      # Leser blockieren Schreiber nicht
conn.execute("PRAGMA busy_timeout = 10000")
conn.execute("PRAGMA synchronous = NORMAL")     # mit WAL ausreichend
```

WAL ist hier fast wichtiger als der Timeout: das Dashboard **liest** die
Tabelle bei jedem Seitenaufruf, und ohne WAL blockiert ein laufender Lesevorgang
einen gleichzeitigen Schreibvorgang. Genau diese Kombination — häufige Leser,
seltene Schreiber — ist der Fall, für den WAL gebaut ist.

*Was WAL kostet:* zwei zusätzliche Dateien (`-wal`, `-shm`) neben der
Datenbank, und es funktioniert nicht über Netzlaufwerke. Beides hier
unproblematisch — solange R1 „ein Rechner" bleibt.

## 2.8 Wachstum und Aufbewahrung (E6)

Rechnung für den heutigen Betrieb:

| Art | pro Tag |
|---|---|
| `lauf_begonnen` + `lauf_beendet` (bei E3 = ja) | 2 × 37 = **74** |
| `trade_eroeffnet` / `trade_geschlossen` | ~1 (22 Trades bisher insgesamt) |
| `bruecken_order` / `bruecken_versuch` | ~6 |
| `lauf_fehler`, `lauf_ueberfaellig` | 0–5 |
| `warteauftrag_*`, `manueller_eingriff` | 0–3 |
| `agenten_hinweis` | 1 (täglich), +1 wöchentlich |
| System (Rotation, Portfolio, Neustart) | ~3 |
| **Summe** | **rund 90** |

**Rund 33.000 Zeilen im Jahr** — bei geschätzten 300 Byte je Zeile sind das
etwa **10 MB**. SQLite merkt davon nichts; die Tabelle wird nicht unhandlich,
sondern *unlesbar*, lange bevor sie langsam wird.

Auffällig ist die Verteilung: **über 80 % der Zeilen wären Lauf-Ereignisse**,
also genau die, die einzeln niemanden interessieren und in Summe alles
beantworten (lief Bot 7 gestern?). Daraus die Empfehlung:

* **Rohdaten 400 Tage behalten.** Etwas mehr als ein Jahr, damit ein
  Jahresvergleich vollständig ist.
* **Danach verdichten statt löschen:** je Bot und Tag eine Zeile
  `lauf_tagesbilanz` (Anzahl Läufe, Fehler, erster/letzter Zeitpunkt), die
  Einzelzeilen entfallen. Das ist genau die Information, die man nach einem
  Jahr noch braucht.
* **Nie verdichtet werden** Trades, Brücken-Orders, manuelle Eingriffe und
  Datenlücken — sie sind einzeln relevant und zusammen wenige hundert im Jahr.
* **Die Verdichtung ist ein eigener Cronjob**, kein Nebeneffekt des Schreibens.
  Gleiche Begründung wie bei der Log-Rotation in PR #79: ein Aufräumvorgang,
  der beiläufig passiert, passiert irgendwann zum falschen Zeitpunkt.

## 2.9 Ausfallverhalten

**Die harte Regel:** ein Ereignis, das nicht protokolliert werden kann, darf
keinen Bot-Lauf und keine Brücken-Order verhindern.

Daraus folgt für `shared/ereignisse.schreibe()`:

1. **Sie wirft nie.** Jeder Fehler wird abgefangen, auf `stderr` gemeldet (und
   landet damit im Cron-Log) und mit `None` quittiert.
2. **Sie wird nie zur Voraussetzung.** Kein Aufrufer darf seinen weiteren
   Ablauf vom Rückgabewert abhängig machen. Das ist eine Regel für Menschen,
   keine, die Code erzwingt — ein Selbsttest kann sie aber prüfen (AST: kein
   `if schreibe(...)` in einem Brückenpfad).
3. **Sie schreibt zuletzt.** In den Brücken wird die Order gesendet und in
   `spiegelungen` vermerkt; das Ereignis kommt **danach**. Fällt die
   Ereignis-DB aus, fehlt eine Zeile im Zeitstrahl — die Order ist trotzdem
   korrekt nachverfolgt. Das ist der Grund, warum E5 (Stichtag statt
   Migration) auch sicherheitstechnisch die richtige Wahl ist: die Brücke
   hängt nicht an der neuen Tabelle.
4. **Der Ausfall selbst wird sichtbar.** Ein Zähler `ereignisse_verloren` in
   einer kleinen Datei neben der DB, den das Dashboard anzeigt. Sonst wäre das
   Schweigen der Ereignis-DB nicht von „nichts passiert" zu unterscheiden —
   derselbe Fehler, den 2.2 bei `state.json` beschreibt.

---

# Teil 2 — Anbieter-Schnittstelle

## 3.1 Das Spannungsfeld, wörtlich belegt

Die heutige Sicherheit steht in Literalen im Code:

| Brücke | fest verdrahtet |
|---|---|
| Binance | `TESTNET_BASIS = "https://testnet.binance.vision"`, `VERBOTENE_HOSTS` als `frozenset`, Hostname wird bei **jeder** Anfrage geparst und geprüft, nur `/api/`-Pfade (damit `/sapi/` mit den Auszahlungen unerreichbar bleibt), `MAX_ORDERS_PRO_LAUF = 5`, `MAX_ORDERS_PRO_TAG = 20`, Notbremse `broker/STOP` auf drei Ebenen |
| IBKR | `HOST = "127.0.0.1"`, `ERLAUBTE_PORTS = (4002, 7497)`, Live-Ports namentlich auf der Verbotsliste, jedes gemeldete Konto muss mit `DU`/`DF` beginnen, Notbremse `broker/STOP_IBKR` |

**Der Punkt ist nicht, dass diese Werte stimmen — sondern dass sie nicht
einstellbar sind.** Eine Zeile in einer `.env` könnte sonst erreichen, was
heute strukturell unmöglich ist.

## 3.2 Registrierung statt Konfiguration — hält das? (A1)

**Ja, mit einer benannten Ausnahme.**

Der Entwurf folgt der Vorgabe: jeder Anbieter ist ein Modul im Repo, neue
Anbieter kommen per Pull Request. Die Schnittstelle regelt, **wie** gefragt
wird — nie, **wen**.

```python
# shared/anbieter/__init__.py - Skizze
REGISTRIERT = {}                    # name -> Klasse, gefuellt beim Import

def hole(name):
    if name not in REGISTRIERT:
        raise AnbieterUnbekannt(name)   # kein Laden aus Konfiguration
    return REGISTRIERT[name]
```

Entscheidend ist, was **nicht** dasteht: kein `importlib.import_module(name)`,
kein Lesen eines Ordners, kein Eintrag aus einer `.env`. Ein unbekannter Name
ist ein Fehler, kein Ladebefehl.

**Die Ausnahme, die benannt gehört:** IBKR liest Port, Stückzahl und Client-ID
**heute schon** aus der Umgebung (`IBKR_PAPER_PORT` und andere). Das ist keine
Aufweichung, weil jeder Wert durch eine Prüfung geht, die nur eine Auswahl aus
zwei Werten zulässt — aber es zeigt die Bruchlinie: **konfigurierbar darf sein,
was aus einer endlichen, im Code stehenden Menge stammt.** Diese Regel ist die
eigentliche Formulierung von A1, und sie ist schärfer als „nichts ist
konfigurierbar":

> Ein Wert darf aus der Umgebung kommen, wenn seine **zulässige Menge** im Code
> steht und die Prüfung bei jedem Gebrauch stattfindet. Alles andere — vor allem
> Hostnamen, Endpunkte und Kontonummern — steht als Literal im Modul.

## 3.3 Die gemeinsame Schnittstelle

Abgeleitet aus dem Vergleich beider Brücken. Sie sind heute schon fast gleich
gebaut — dieselben Funktionsnamen in derselben Reihenfolge:

| gleich in beiden | nur Binance | nur IBKR |
|---|---|---|
| `spiegel_db_pfad`, `oeffne_spiegel_db` | `bot_db_pfad` | — |
| `client_order_id` / `order_ref` (gleiche Rolle) | | |
| `notiere_versuch`, `notbremse_grund`, `gespiegelt`, `orders_heute` | | |
| `lies_trades`, `aufgaben`, `spiegle_eine`, `lauf` | `_zugangsdaten` | `_zeitfenster` (Handelszeiten) |
| `_meldung`, `_pruefen`, `_status`, `main` | | |

Daraus die Schnittstelle:

```python
class Anbieter:                      # nur lesen
    name: str
    welt: str                        # 'paper' | 'echt' - siehe A3
    def positionen(self) -> list: ...
    def kurse(self, symbole) -> dict: ...
    def status(self) -> dict: ...    # erreichbar? seit wann? Konto?

class HandelnderAnbieter(Anbieter):  # zusaetzlich handeln
    max_orders_pro_lauf: int
    max_orders_pro_tag: int
    notbremse_datei: str
    def handelbar_jetzt(self, symbol) -> tuple[bool, str]: ...
    def marktorder(self, symbol, seite, menge, kennung) -> dict: ...
    def order_nach_kennung(self, symbol, kennung) -> dict | None: ...
```

**`handelbar_jetzt` ist die Antwort auf die Handelszeiten-Frage** aus dem
Auftrag: Krypto gibt immer `(True, "durchgehend handelbar")` zurück, IBKR
fragt den Börsenkalender. Der aufrufende Spiegel-Code muss den Unterschied
dann nicht mehr kennen — heute steht er als `_zeitfenster` nur in der einen
Brücke.

**`order_nach_kennung` ist die zweite tragende Säule**: sie erlaubt beiden
Brücken, eine bereits gesendete Order wiederzuerkennen, statt sie erneut zu
senden. Ohne sie wäre die Doppelsende-Sicherung eine reine Datenbankfrage —
und die Datenbank weiss nicht, was die Börse gesehen hat.

## 3.4 Lesende und handelnde Anbieter (A2)

**Strukturell, nicht als Einstellung:** `Anbieter` kann nicht handeln, weil die
Methode nicht existiert. Trade Republic erbt von `Anbieter`, Binance-Testnet und
IBKR-Paper von `HandelnderAnbieter`.

*Alternative:* ein Feld `kann_handeln = False` mit einer Prüfung in
`marktorder`. **Verworfen** — eine Prüfung kann man vergessen, eine fehlende
Methode nicht. Dieselbe Begründung, mit der PR #78 seine `UNIQUE`-Sperre einer
`if`-Abfrage vorzieht.

Die Oberfläche fragt dann nicht „darf dieser Anbieter handeln?", sondern
`isinstance(anbieter, HandelnderAnbieter)` — und ein Knopf, den es nicht geben
darf, wird gar nicht erst gezeichnet.

## 3.5 Echtgeld und Paper-Trading trennen (A3)

Der Nutzer hält echte manuelle Positionen bei Trade Republic und Binance.
Vermischen sich die mit den Bot-Zahlen, ist jede Strategie-Bewertung wertlos.

**Empfehlung: getrennte Datenbankdateien, nicht getrennte Spalten.**

```
daten/paper/ereignisse.db      <- alles, was die Bots und Bruecken erzeugen
daten/echt/ereignisse.db       <- manuelle Positionen, nur lesend erfasst
```

*Alternative:* eine Datei, eine Spalte `welt`. **Verworfen.** Eine Spalte
schützt nur, solange jede einzelne Abfrage sie im `WHERE` hat — und die
Portfolio-Rechnung aus PR #80 zieht ihre Zahlen aus mehreren Quellen. Eine
vergessene Bedingung fiele niemandem auf, weil das Ergebnis plausibel aussähe.
Genau dieses Fehlerbild — plausibel, aber falsch — ist in PR #81 gerade
untersucht worden.

Zwei Dateien machen den Fehler dagegen sichtbar: wer echte Zahlen in eine
Paper-Auswertung bekommen will, muss eine zweite Datei **öffnen**. Das tut
niemand versehentlich.

Zusätzlich, als zweite Wache: `Anbieter.welt` ist ein Literal im jeweiligen
Modul, und die Schreibfunktion nimmt die Weltzugehörigkeit **aus dem Anbieter**,
nicht aus einem Aufrufparameter.

**Was der Entwurf hier nicht kann:** er kann nicht verhindern, dass jemand die
Zahlen in einer Anzeige addiert. Er kann nur erzwingen, dass es eine bewusste
Handlung ist.

## 3.6 Der Crash-Knopf bei mehreren Anbietern (A4)

**Empfehlung: nicht erweitern.** Der Crash-Knopf bleibt, was er ist — er
schliesst Positionen in den **Bot-Datenbanken**, in der Paper-Welt.

Drei Gründe:

1. **Für Trade Republic könnte er technisch nichts tun.** Ein Knopf, der
   Schliessen suggeriert, es aber nicht kann, ist im Notfall schlimmer als
   keiner. Das ist der stärkste Grund und er allein trägt die Empfehlung.
2. **Für Binance wäre es technisch möglich — und würde die Wand einreissen.**
   Echte Positionen liegen auf `api.binance.com`, und dieser Host steht
   namentlich auf `VERBOTENE_HOSTS`. Ihn erreichbar zu machen, hiesse die
   tragende Sicherheitsannahme des gesamten Broker-Bereichs aufzugeben — für
   eine Funktion, die der Nutzer auch in der Binance-App hat.
3. **Zwei Welten an einem Knopf sind im Notfall eine Frage zu viel.** Die
   Oberfläche müsste im Bestätigungsdialog unterscheiden, was geschlossen wird.
   Auf 390 px, in zwei Sekunden, unter Stress.

**Was stattdessen:** die Oberfläche zeigt echte Positionen **an** (aus
`daten/echt/`), deutlich abgesetzt, mit dem ausdrücklichen Hinweis „nur
Anzeige — schliessen in der App des Anbieters". Eine Anzeige, die ihre Grenze
benennt, ist ehrlicher als ein Knopf, der sie verschweigt.

*Wenn der Nutzer anders entscheidet*, wäre der kleinstmögliche Weg: ein
**eigener** Anbieter `binance_echt` als getrenntes Modul mit eigener
Verbotsliste, eigener Notbremse und eigener Tagesgrenze — und ausdrücklich
**ohne** Anbindung an den vorhandenen Crash-Knopf, sondern mit einem eigenen.
Das ist aber ein Projekt für sich, kein Zusatz.

## 3.7 Anbieter und Ereignis-Datenbank

Jede Order, jede Abweichung, jeder Verbindungsfehler ist ein Ereignis (2.3).
Die Kopplung ist bewusst **einseitig**:

* Die Brücke schreibt **zuerst** in ihre eigene `spiegelungen`-Tabelle (das ist
  ihre Doppelsende-Sicherung) und **danach** das Ereignis.
* Die Ereignis-DB ist nie Voraussetzung für eine Order (2.9).
* Der `schluessel` des Ereignisses ist derselbe fachliche Schlüssel, den die
  Brücke ohnehin bildet (`bot:trade_id:seite`) — dadurch ist die spätere
  Migration (E5, optionaler Schritt 7) ein reines Kopieren.

## 3.8 Welche Anbieter realistisch infrage kämen (A5)

Belegt, soweit im Repo belegbar; alles andere ausdrücklich als Einschätzung
gekennzeichnet.

| Anbieter | Lage | Einordnung |
|---|---|---|
| **Binance Testnet** | **angebunden, produktiv** (`broker/spiegel.py`, Cronjob alle 4 h) | — |
| **IBKR Paper** | **angebunden, nie gegen echte TWS gelaufen**; `ib_async` verlangt Python 3.10+, der Mac läuft 3.9.6 | blockiert durch die Python-Version, nicht durch die Schnittstelle |
| **Trade Republic** | keine öffentliche API (im Backlog geprüft und verworfen) | nur CSV-Import oder manuelle Eingabe, rein lesend |
| **justTRADE, Smartbroker** | geprüft und verworfen — keine öffentliche Handels-API bzw. kein US-Aktienzugang | — |

**Empfehlung zu A5: zunächst keinen neuen Anbieter anbinden.** Die beiden
vorhandenen decken beide Anlageklassen ab, und einer davon ist noch nicht
einmal einmal echt gelaufen. Ein dritter Anbieter erhöht die Fläche, ohne eine
offene Frage zu schliessen.

Die Schnittstelle aus 3.3 lohnt sich trotzdem — nicht wegen künftiger
Anbieter, sondern weil sie die **Handelszeiten-Frage** aus dem Spiegel-Code
herauszieht und in PR #77 bereits ein zweites Mal beantwortet werden musste.

---

# 4. Umsetzungsreihenfolge

Jeder Schritt ist ein eigener PR. Die Aufwände sind Schätzungen einer
Cloud-Sitzung mit Tests und Dokumentation, keine Zusagen.

| # | Schritt | setzt voraus | Aufwand | Unsicherheit |
|---|---|---|---|---|
| **1** | `shared/ereignisse.py`: Schema, `schreibe()`, Leseabfragen, Selbsttests. Noch **kein** Aufrufer. | E1, E2, E4 | **mittel** | gering — die drei Vorbilder tragen |
| **2** | Erster Schreiber: die **Brücken**. Sie sind die Stelle mit den klarsten Schlüsseln und ändern ihr Verhalten nicht. | 1 | klein | gering |
| **3** | Zweiter Schreiber: Dashboard (manuelle Eingriffe, Warteaufträge) und `schliess_benachrichtigung.py`. | 1 | klein | gering |
| **4** | **Sammler** für die Bot-Trades (schreibgeschützt über `bot_db.py`). Ersetzt den Trade-Teil von `monitor.py` noch nicht, läuft daneben. | 1 | mittel | gering |
| **5** | **Zeitstrahl-Seite** im Dashboard, eigene Seite, filterbar nach Bot und Art. | 1–4 | mittel | gering — Muster aus PR #80 |
| **6** | `monitor.py` liest aus der Ereignis-DB statt selbst zu vergleichen; `state.json` entfällt. **Der eigentliche Gewinn.** | 4, 5 | mittel | **mittel** — hier wird ein laufender Meldeweg umgehängt |
| **7** | *(optional)* Einmal-Import der drei vorhandenen DBs. | 1 | klein | gering |
| **8** | Verdichtung + Aufbewahrung als eigener Cronjob. | 1 | klein | gering |
| **9** | `shared/anbieter/`: die beiden Basisklassen, beide Brücken dahinter. **Kein** neuer Anbieter. | — | **gross** | **hoch** — fasst produktiven Brücken-Code an |
| **10** | Lesender Anbieter für manuelle Positionen (CSV-Import), getrennte Welt. | 9, A3 | mittel | mittel |

**Die Reihenfolge ist nicht beliebig.** Schritt 6 ist der Punkt, an dem das
Projekt etwas gewinnt statt nur etwas hinzuzufügen — vorher laufen alter und
neuer Weg parallel. Schritt 9 steht bewusst **hinten**: er fasst als einziger
produktiven Brücken-Code an, und er wird erst wertvoll, wenn es einen dritten
Anbieter gibt.

**Ein Zwischenstand, an dem man aufhören kann:** nach Schritt 5 ist der
Zeitstrahl da und nützlich, ohne dass ein bestehender Meldeweg verändert wurde.
Das ist der natürliche Haltepunkt, falls sich die Prioritäten verschieben.

---

# 5. Was dieser Entwurf nicht kann

* **Er löst offenen Punkt 12 nicht vollständig.** Ohne eine Zeile in
  `forward_test.py` bleibt „Lauf stattgefunden" eine Heuristik über Logdateien
  (2.5). Der Entwurf macht die Unsicherheit sichtbar, statt sie zu verstecken —
  mehr kann er unter der Randbedingung nicht.
* **Er macht die App nicht erreichbar, während der Mac schläft** (1.1).
* **Er kann nicht verhindern, dass jemand Echt- und Paper-Zahlen addiert**,
  nur erzwingen, dass es eine bewusste Handlung ist (3.5).
* **Er hat den Migrationspfad nicht erprobt.** Schritt 7 ist auf dem Papier
  einfach, weil die Schlüssel kompatibel sind; ob die Zeitstempel der beiden
  Brücken tatsächlich durchgängig im selben Format vorliegen, ist **nicht**
  geprüft.
* **Er schätzt die Ereignismenge, statt sie zu messen.** Die Zahlen in 2.8
  beruhen auf Cron-Takten und 22 bisher geschlossenen Trades. Ein Bot, der in
  eine aktive Marktphase gerät, kann das Trade-Aufkommen vervielfachen — an der
  Grössenordnung (10 MB/Jahr) ändert das nichts.

# 6. Offene Fragen an den Nutzer

Fragen, die dieser Entwurf bewusst nicht beantwortet, weil sie
Nutzerentscheidungen sind:

1. **R1:** Soll das System langfristig auf einen dauerhaft laufenden Rechner
   umziehen? Davon hängt ab, ob SQLite mit WAL (2.7) die richtige Grundlage
   bleibt.
2. **E3:** Ist Ihnen ein Lauf-Protokoll wichtig genug, um eine Ausnahme für
   `forward_test.py` zu erwägen — zwei Zeilen, ein Aufruf am Anfang und am
   Ende? Ohne sie bleibt der Zeitstrahl an dieser Stelle ungenau.
3. **A4:** Bleibt es dabei, dass der Crash-Knopf nur die Paper-Welt betrifft?
4. **E6:** Sind 400 Tage Rohdaten die richtige Grenze, oder wollen Sie alles
   dauerhaft behalten? (Der Platz spricht nicht dagegen — die Lesbarkeit schon.)
5. **Schritt 6:** Soll `monitor.py` tatsächlich umgehängt werden, oder darf der
   alte Meldeweg dauerhaft parallel laufen? Parallel ist sicherer, aber dann
   gibt es wieder zwei Wahrheiten — genau der Zustand, den PR #78 beseitigt hat.

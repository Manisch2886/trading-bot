# Log-Rotation für `logs/`

`system/log_rotation.py` begrenzt die Größe der Logdateien unter `logs/`.
Kein zusätzliches Paket, kein `sudo`, kein Dienst — ein Skript, das per Cron
oder von Hand läuft.

**Der Zweck ist Lesbarkeit, nicht Platz.** In einer Datei, die zu neun Zehnteln
aus wiederholten Routinemeldungen besteht, geht eine echte Fehlermeldung unter.
Genau danach wurde am 11.09.2026 bei der Fehlersuche gegriffen.

---

## Benutzung

```bash
python3 system/log_rotation.py --status        # Übersicht inkl. alter Stände
python3 system/log_rotation.py --trockenlauf   # zeigt nur, was fällig wäre
python3 system/log_rotation.py                 # rotiert
```

Das Skript hat keinen Zustand: es entscheidet allein anhand der aktuellen
Dateigröße und ist beliebig oft wiederholbar.

### Cron-Zeile — Vorschlag, **nicht eingetragen**

```cron
30 3 * * * cd ~/trading-bot && /usr/bin/python3 system/log_rotation.py >> logs/system/log_rotation.log 2>&1
```

Einmal täglich um 3:30 Uhr. Begründung: rotiert wird nach Größe, nicht nach
Zeit — der Cron-Takt bestimmt also nur, wie oft *nachgesehen* wird. Bei den
heutigen Wachstumsraten (größte Datei rund 262 KB über Monate) reicht einmal
täglich mit großem Abstand, und 3:30 Uhr liegt zwischen den 4-Stunden-Läufen
der Bots. Ein engerer Takt würde nichts verbessern, ein weiterer (wöchentlich)
ließe eine plötzlich volllaufende Datei zu lange wachsen.

> **Hinweis:** Die Crontab des Nutzers ließ sich am 12.09.2026 nicht ändern
> (`crontab -` scheitert mit `Operation not permitted`, macOS-Berechtigung nach
> einem Update zurückgesetzt). Bis das behoben ist, wird die Rotation von Hand
> aufgerufen — das ist vollständig ausreichend, weil sie nach Größe entscheidet
> und kein Intervall braucht.

Den Ordner vorher anlegen: `mkdir -p logs/system`.

---

## Warum ein eigenes Skript und nicht `newsyslog`

macOS bringt `newsyslog` mit. Es wurde geprüft und **nicht** gewählt:

1. **Es braucht `sudo` und eine Datei unter `/etc/newsyslog.d/`.** Das Projekt
   hat bei `caffeinate` dieselbe Abwägung schon einmal getroffen und sich
   bewusst gegen den Weg mit `sudo` entschieden (LaunchAgent statt
   LaunchDaemon, siehe `README_CAFFEINATE.md`). Hier gilt derselbe Grund, und
   er wiegt sogar schwerer: eine Rotation *löscht* Dateien. Ein Tippfehler im
   Pfad einer root-Konfiguration löscht sie außerhalb von `logs/`.
2. **Die Konfiguration läge außerhalb des Repos.** Sie wäre nicht versioniert,
   nicht reviewbar und nicht testbar. Der gesamte Abschnitt "Tests" unten
   existiert nur, weil die Regeln im Repo stehen.
3. **`newsyslog` hat für den entscheidenden Fall keine bessere Antwort.**
   Sein Standardverfahren ist Umbenennen; damit ein dauerhaft laufender Dienst
   danach in die neue Datei schreibt, braucht es eine PID-Datei und ein Signal.
   Dashboard, Telegram-Bot und `caffeinate` liefern keine PID-Datei, und
   launchd öffnet seine Logdateien nicht auf Signal neu. `newsyslog` müsste
   also ebenfalls kopieren-und-leeren — mit derselben Restlücke wie hier, nur
   unsichtbar.
4. **Von Hand aufrufbar.** Solange die Crontab klemmt (siehe oben), ist genau
   das der Unterschied zwischen "läuft" und "läuft nicht".

Nicht gewählt wurde auch **`logrotate`** (nicht in macOS enthalten, wäre eine
Homebrew-Abhängigkeit) und **Kompression der Archive** mit `gzip` (wäre ohne
Zusatzpaket möglich, macht aber `grep` über alte Stände umständlich — und
Suchbarkeit ist hier der ganze Zweck).

---

## Warum kopiert und geleert wird, statt umbenannt

Dashboard, Telegram-Bot und `caffeinate` halten ihre Logdatei **dauerhaft
offen**. Ein `mv datei datei.alt` nimmt das offene Dateihandle mit: der Dienst
schreibt weiter in `datei.alt`, die neue `datei` bleibt für immer leer — und
niemand merkt es, bis man beim nächsten Fehler in die falsche Datei schaut.

Deshalb wird die Datei **kopiert und anschließend geleert** (`truncate`). Sie
behält dabei ihren **Inode**; jedes offene Handle zeigt weiter auf dieselbe,
nun leere Datei. Der Selbsttest prüft das mit einem echten zweiten Prozess, der
während der Rotation weiterschreibt.

Voraussetzung ist, dass die Schreiber im Anhängemodus (`O_APPEND`) schreiben,
denn nur dann wird der Schreib-Offset bei jedem Schreibvorgang neu auf das
Dateiende gesetzt. Das ist bei allen Schreibern dieses Projekts der Fall:
Cronjobs schreiben mit `>>`, launchd öffnet `StandardOutPath` /
`StandardErrorPath` anhängend, und Pythons `logging.FileHandler` benutzt
standardmäßig `mode="a"`.

### Die Restlücke — benannt und beziffert

Zwischen dem letzten Lesevorgang und dem Leeren kann eine Zeile verloren gehen.
Das ist die bekannte Eigenschaft jedes Kopieren-und-Leeren-Verfahrens
(`logrotate` dokumentiert sie bei `copytruncate` genauso). Ohne Mitwirkung der
schreibenden Prozesse ist sie nicht auflösbar — es gibt keine Sperre, die ein
`launchd`-Log respektieren würde.

Was dagegen getan wurde: das Fenster wurde so klein gemacht, wie es geht. Alles
Teure — `fsync` des Inhalts, `fsync` des Verzeichnisses, die Größenprüfung —
liegt **vor** dem letzten Lesevorgang. Zwischen dem leeren Lesevorgang und dem
`truncate` liegen nur zwei Abfragen.

Dass das nicht kosmetisch ist, zeigt die Messung: in der ersten Fassung stand
der `fsync` *nach* dem letzten Lesevorgang, und das kostete **knapp eine Zeile
pro Rotation**. Gemessen:

| Schreibrate | verlorene Zeilen je Rotation |
|---|---|
| 200 Zeilen/s (weit über allem im Projekt) | **0** von 6.092, über 60 Rotationen |
| 5.000 Zeilen/s | **~0,1** — höchstens **1** je 10 Rotationen, über 6 Durchgänge |
| 5.000 Zeilen/s, `fsync` hinter dem letzten Lesevorgang | **~0,8** — 6 bis 10 je 10 Rotationen |
| 5.000 Zeilen/s, erste Fassung (`fsync` in der Schleife danach) | ~1,0 (0,71 %) |

Die Logdateien dieses Projekts schreiben wenige Zeilen je Lauf. Das Risiko
liegt damit rechnerisch bei Bruchteilen eines Prozents einer einzelnen Zeile je
Rotation, und die Rotation findet pro Datei höchstens einmal am Tag statt.

Wer für ein Log **null** Verlust braucht, rotiert es in-process mit
`logging.handlers.RotatingFileHandler` — so wie `telegram_bot.py` und
`manual_close.py` es tun. Dort gibt es kein Fenster, weil derselbe Prozess
schreibt und rotiert. Für Logs, die von Cron oder launchd per Umleitung
geschrieben werden, existiert dieser Weg nicht.

### Was nie passiert

* Geleert wird nur, wenn das Archiv nachweislich vollständig ist (Größe des
  Archivs == Zahl der kopierten Bytes) und auf der Platte steht (`fsync` auf
  Inhalt **und** Verzeichniseintrag).
* Alte Stände werden erst **nach** dieser Prüfung gelöscht.
* Wächst eine Datei schneller, als die Rotation kopieren kann, bricht sie nach
  20 Nachlese-Runden ab und leert **nichts**. Lieber keine Rotation als eine,
  die Zeilen verliert.
* Ein vorhandenes Archiv wird nie überschrieben (`open(..., "xb")`).
* Ein Fehlschlag bei einer Datei stoppt weder die Rotation der anderen noch
  irgendeinen Dienst.

---

## Was rotiert wird — und was nicht

Gesucht wird nach `logs/**/*.log`. **Gesucht statt aufgelistet**, weil eine
Liste eine Stelle wäre, an der ein neuer Bot oder ein neuer Dienst vergessen
wird. Alles, was nicht auf `.log` endet, bleibt dadurch automatisch außen vor:
Datenbanken, `state.json`, `.env`. Eigene Archive heißen
`<name>.log.<Zeitmarke>` und enden nicht auf `.log` — sie werden also nie
selbst zum Kandidaten.

| | Schwelle | Stände | Obergrenze |
|---|---|---|---|
| alle `logs/**/*.log` | 1 MB (1.000.000 Bytes) | 5 | 6 MB je Datei |
| `logs/broker/testnet_spiegel.log` | 1 MB | **20** | 21 MB |
| `logs/broker/ibkr_paper_spiegel.log` | 1 MB | **20** | 21 MB |
| `logs/notifications/telegram_bot.log` | — | — | **ausgenommen** |
| `logs/notifications/manuelle_eingriffe.log` | — | — | **ausgenommen** |

**Schwelle 1 MB.** Die größte Logdatei des Projekts lag am 12.09.2026 bei rund
262 KB (`forward_test.log`) und ist über Monate gewachsen. 1 MB lässt also
reichlich Luft, und die Rotation bleibt ein seltenes Ereignis — wichtig, weil
jede Rotation eine Schnittstelle im Protokoll ist, an der man beim Suchen eine
Datei weiterblättern muss. Nach oben begrenzt die Lesbarkeit: 1 MB Text sind
gut 10.000 Zeilen; `grep` und `tail` stört das nicht, ein Mensch scrollt da
nicht mehr durch — und um diesen Menschen geht es.

**5 Stände.** 1 MB × (1 + 5) = 6 MB Obergrenze je Datei. Das deckt den
Zeitraum ab, in dem man nach einem Vorfall überhaupt noch nachsieht. Mehr
Stände kosten kaum Platz, machen aber das Durchsuchen umständlicher.

**Zeitmarke statt `.1`, `.2`, `.3`.** Kein Umbenennen einer ganzen Kette bei
jeder Rotation — jedes Umbenennen wäre eine weitere Stelle, an der ein Lauf auf
halber Strecke abbrechen und einen Stand überschreiben kann. Außerdem sortiert
die Zeitmarke lexikalisch wie chronologisch, und man sieht am Namen, wann
geschnitten wurde.

### Die beiden Brücken-Protokolle: 20 Stände statt Ausnahme

`logs/broker/testnet_spiegel.log` und `logs/broker/ibkr_paper_spiegel.log` sind
**keine Wegwerf-Logs**: dort stehen Order-IDs, Ausführungspreise,
Teilausführungen, Gebühren und — anders als in der Datenbank — der *Verlauf*
fehlgeschlagener Versuche samt Traceback.

Ausgenommen werden sie trotzdem nicht, denn "ausgenommen" heißt hier "wächst
weiter unbegrenzt", und das ist der Zustand, der behoben werden soll. Gewählt
wurde deshalb die zweite Variante: **deutlich mehr Stände**, 20 statt 5, also
bis zu 21 MB Verlauf je Brücke.

Tragfähig ist das, weil das **Endergebnis jeder Order zusätzlich in der
Broker-Datenbank** steht — Tabelle `spiegelungen` mit `order_id`,
`ausfuehrungspreis`, `gebuehr` und der rohen Antwort je Trade und Seite,
Fehlversuche in `versuche`. Das Protokoll ist die ausführliche Fassung, nicht
die einzige. Wäre es die einzige, wäre die Antwort eine Ausnahme.

### Die beiden Dateien, die sich selbst rotieren

| Datei | rotiert durch | Grenze |
|---|---|---|
| `logs/notifications/telegram_bot.log` | `RotatingFileHandler` in `notifications/telegram_bot.py` | 2 MB × 3 Stände |
| `logs/notifications/manuelle_eingriffe.log` | `RotatingFileHandler` in `notifications/manual_close.py` | 1 MB × 5 Stände |

Beide sind durch `maxBytes × backupCount` **bereits nach oben begrenzt** — also
genau das, was diese Aufgabe erreichen will. Ein zweiter Rotator würde nichts
verbessern und zwei konkurrierende Namensschemata für dieselbe Datei einführen
(`.log.1` vom Handler neben `.log.<Zeitmarke>` von hier). Bei
`manuelle_eingriffe.log` kommt hinzu, dass es das Protokoll manueller
Eingriffe ist — die Datei, in der man nachliest, wer wann eine Position
geschlossen hat.

Die Zahlen in der Tabelle stehen nicht doppelt: der Selbsttest liest die echten
Handler-Argumente per AST aus den beiden Quelldateien und vergleicht sie mit den
Angaben in `log_rotation.py`. Ändert dort jemand `maxBytes`, schlägt der Test
fehl.

---

## Nicht rotiert

Datenbanken (`*.db`), `notifications/state.json`,
`notifications/warteauftraege.json`, `.env`, alles außerhalb von `logs/`.
Symlinks werden nicht angefasst — auch nicht, wenn sie innerhalb von `logs/`
liegen und nach außen zeigen.

## Tests

```bash
python3 system/test_log_rotation.py
```

Geprüft wird am Verhalten gegen echte Dateien in einem Wegwerf-Ordner unter
`/tmp`, nie gegen das echte `logs/`. Der Kern ist Abschnitt 5: ein **echter
zweiter Prozess** hält die Logdatei während der Rotation offen und schreibt
durchgehend weiter; danach müssen seine neuen Zeilen in der neuen Datei stehen,
das Archiv darf nicht mehr wachsen und der Inode muss derselbe sein.
Abschnitt 6 beziffert die Restlücke mit zwei Schreibraten.

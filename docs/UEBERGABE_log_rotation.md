# Übergabe: Log-Rotation für die Projektlogs

**Branch** `claude/new-session-uqjk8h`, Basis `origin/main` (`b4b7acd`, nach
Merge von #78).

Neu: `system/log_rotation.py`, `system/test_log_rotation.py`,
`system/README_LOG_ROTATION.md`, `system/TESTAUFTRAG_LOG_ROTATION.md`.
**Kein bestehender Code wurde geändert** — keine Zeile in `broker/`,
`strategies/`, `notifications/`, `dashboard/`, keine launchd-Vorlage, keine
Crontab.

---

## 1. Die drei Entscheidungen, die begründet werden müssen

### Eigenes Skript, nicht `newsyslog`

Vier Gründe, der erste ist der vom Auftrag vorgezeichnete:

1. **`sudo` und eine Konfigurationsdatei unter `/etc/newsyslog.d/`.** Das
   Projekt hat bei `caffeinate` dieselbe Abwägung getroffen und sich bewusst
   gegen `sudo` entschieden (LaunchAgent statt LaunchDaemon). Hier wiegt der
   Grund schwerer als dort: eine Rotation *löscht* Dateien. Ein Tippfehler im
   Pfad einer root-Konfiguration löscht sie außerhalb von `logs/`.
2. **Die Konfiguration läge außerhalb des Repos** — nicht versioniert, nicht
   reviewbar, nicht testbar. Die 117 Prüfungen unten existieren nur, weil die
   Regeln im Repo stehen.
3. **`newsyslog` hat für den entscheidenden Fall keine bessere Antwort.** Sein
   Standardverfahren ist Umbenennen; damit ein Dauerdienst danach in die neue
   Datei schreibt, braucht es eine PID-Datei und ein Signal. Dashboard,
   Telegram-Bot und `caffeinate` liefern keine PID-Datei, und launchd öffnet
   seine Logdateien nicht auf Signal neu. `newsyslog` müsste hier also ebenfalls
   kopieren-und-leeren — mit derselben Restlücke, nur unsichtbar.
4. **Von Hand aufrufbar.** Die Crontab des Nutzers lässt sich derzeit nicht
   ändern (`Operation not permitted`). Solange das so ist, ist genau das der
   Unterschied zwischen „läuft" und „läuft nicht".

Ebenfalls geprüft und verworfen: `logrotate` (nicht in macOS enthalten, wäre
eine Homebrew-Abhängigkeit) und Kompression der Archive mit `gzip` (ginge ohne
Zusatzpaket, macht aber `grep` über alte Stände umständlich — und Suchbarkeit
ist der ganze Zweck der Aufgabe).

### Schwelle: 1 MB

Die größte Logdatei lag am 12.09.2026 bei rund 262 KB (`forward_test.log`),
gewachsen über Monate. 1 MB lässt also reichlich Luft, und die Rotation bleibt
ein seltenes Ereignis — wichtig, weil jede Rotation eine Schnittstelle im
Protokoll ist, an der man beim Suchen eine Datei weiterblättern muss.

Nach oben begrenzt die Lesbarkeit: 1 MB Text sind gut 10.000 Zeilen. `grep` und
`tail` stört das nicht, ein Mensch scrollt da nicht mehr durch — und um diesen
Menschen geht es bei dieser Aufgabe.

### Stände: 5 — außer bei den zwei Brücken-Protokollen

5 × 1 MB plus die laufende Datei = **6 MB Obergrenze je Datei**. Das deckt den
Zeitraum ab, in dem man nach einem Vorfall überhaupt noch nachsieht. Mehr Stände
kosten kaum Platz, machen aber das Durchsuchen umständlicher.

**Nebenentscheidung: Zeitmarke statt `.1`, `.2`, `.3`.** Archive heißen
`<name>.log.2026-09-12T03-30-00`. Damit fällt das Umbenennen einer ganzen Kette
bei jeder Rotation weg — jedes Umbenennen wäre eine weitere Stelle, an der ein
Lauf auf halber Strecke abbrechen und einen Stand überschreiben kann. Außerdem
sortiert die Zeitmarke lexikalisch wie chronologisch, man sieht am Namen, wann
geschnitten wurde, und der Name endet **nicht** auf `.log`, wird also nie selbst
zum Rotationskandidaten.

---

## 2. `logs/broker/testnet_spiegel.log` — geprüft, wie verlangt

**Befund: dort stehen tatsächlich Ausführungsdaten.** Order-IDs,
Ausführungspreise, Teilausführungen, Gebühren — und, anders als in der
Datenbank, der *Verlauf* fehlgeschlagener Versuche samt Traceback:

```
TESTNET ERFOLG - t3_supertrend Trade 1 eroeffnung (BTCUSDT): Order 700001
FILLED, ausgefuehrt 0.002 zu 50030 (netto 0.001998, 2 Teilausfuehrung(en),
Gebuehren {'BTC': 2e-06}), Abweichung zum Simulationspreis +0.060 %
```

**Entscheidung: nicht ausnehmen, sondern 20 Stände** (= bis 21 MB Verlauf je
Brücke), für `testnet_spiegel.log` und `ibkr_paper_spiegel.log`.

Begründung in zwei Teilen. Gegen die Ausnahme: „ausgenommen" heißt hier „wächst
weiter unbegrenzt", und das ist der Zustand, der behoben werden soll. Für die
Tragfähigkeit: das **Endergebnis jeder Order steht zusätzlich in der
Broker-Datenbank** — Tabelle `spiegelungen` mit `order_id`,
`ausfuehrungspreis`, `gebuehr` und der rohen Antwort je Trade und Seite,
Fehlversuche in `versuche`. Das Protokoll ist die ausführliche Fassung, nicht
die einzige. Wäre es die einzige, wäre die Antwort eine Ausnahme.

---

## 3. Ein Befund, den der Auftrag nicht vorhersah

Zwei der genannten Dateien **rotieren sich längst selbst**:

| Datei | rotiert durch | Grenze |
|---|---|---|
| `logs/notifications/telegram_bot.log` | `RotatingFileHandler` in `telegram_bot.py` | 2 MB × 3 |
| `logs/notifications/manuelle_eingriffe.log` | `RotatingFileHandler` in `manual_close.py` | 1 MB × 5 |

Der Auftrag führt `logs/notifications/*.log` unter „wächst unbegrenzt". Für
diese beiden trifft das nicht zu: sie sind durch `maxBytes × backupCount`
bereits nach oben begrenzt — genau das, was die Aufgabe erreichen will.

Sie sind deshalb **ausgenommen**. Ein zweiter Rotator würde nichts verbessern
und zwei konkurrierende Namensschemata für dieselbe Datei einführen (`.log.1`
vom Handler neben `.log.<Zeitmarke>` von hier). Bei `manuelle_eingriffe.log`
kommt hinzu, dass es das Protokoll manueller Eingriffe ist.

Damit die Zahlen nicht doppelt geführt werden (Grundsatz aus dem
Übergabeprotokoll): der Selbsttest liest `maxBytes` und `backupCount` **per AST
aus den beiden echten Quelldateien** und vergleicht sie mit den Angaben in
`log_rotation.py`. Ändert dort jemand einen Wert, schlägt der Test fehl.

---

## 4. Wie das Verfahren arbeitet

Kein Zustand, keine Datenbank, keine Marke: die Entscheidung fällt allein anhand
der aktuellen Dateigröße. Der Lauf ist damit beliebig oft wiederholbar.

Gesucht wird nach `logs/**/*.log` — **gesucht statt aufgelistet**, weil eine
Liste eine Stelle wäre, an der ein neuer Bot vergessen wird. Alles, was nicht
auf `.log` endet, bleibt automatisch außen vor: Datenbanken, `state.json`,
`warteauftraege.json`, `.env`. Symlinks werden nicht angefasst.

### Kopieren und leeren, nicht umbenennen

Dashboard, Telegram-Bot und `caffeinate` halten ihre Logdatei dauerhaft offen.
Ein `mv` nimmt das offene Dateihandle mit: der Dienst schreibt weiter in die
umbenannte Datei, die neue bleibt für immer leer — und niemand merkt es, bis man
beim nächsten Fehler in die falsche Datei schaut.

Deshalb: kopieren, dann `truncate`. Die Datei behält ihren **Inode**, jedes
offene Handle zeigt weiter auf dieselbe, nun leere Datei. Voraussetzung ist
`O_APPEND`, und das ist bei allen Schreibern dieses Projekts nicht Annahme,
sondern Funktionsweise: Cron schreibt mit `>>`, launchd öffnet anhängend,
`logging.FileHandler` benutzt `mode="a"`.

### Die Restlücke — und was sie mich gekostet hat

Zwischen dem letzten Lesevorgang und dem Leeren kann eine Zeile verloren gehen.
Das ist die bekannte Eigenschaft jedes Kopieren-und-Leeren-Verfahrens
(`logrotate` dokumentiert sie bei `copytruncate` genauso) und ohne Mitwirkung
der schreibenden Prozesse nicht auflösbar — es gibt keine Sperre, die ein
launchd-Log respektieren würde.

**Meine erste Fassung war deutlich schlechter, als ich dachte.** Ich hatte die
Lücke für ein Mikrosekunden-Fenster gehalten. Die Messung zeigte **knapp eine
verlorene Zeile pro Rotation** — systematisch, nicht zufällig. Ursache: der
`fsync` stand *nach* dem letzten Lesevorgang, und ein `fsync` dauert Hunderte
Mikrosekunden. Das Fenster war selbstgemacht.

Jetzt liegt alles Teure — `fsync` des Inhalts, `fsync` des Verzeichnisses, die
Größenprüfung — **vor** dem letzten Lesevorgang. Erlaubt ist das, weil ein
leerer Lesevorgang beweist, dass seit der Prüfung nichts dazukam. Zwischen ihm
und dem `truncate` liegen nur zwei Abfragen.

Gemessen:

| Schreibrate | verlorene Zeilen je Rotation |
|---|---|
| 200 Zeilen/s (weit über allem im Projekt) | **0** von 6.092, über 60 Rotationen |
| 5.000 Zeilen/s | **~0,1** — höchstens **1** je 10 Rotationen, über 6 Durchgänge |
| 5.000 Zeilen/s, `fsync` hinter dem letzten Lesevorgang | **~0,8** — 6 bis 10 je 10 Rotationen |
| 5.000 Zeilen/s, erste Fassung (`fsync` in der Schleife danach) | ~1,0 (0,71 %) |

Damit der Fehler nicht zurückkehrt, prüft der Test die **Reihenfolge**
deterministisch statt per Timing-Glück: er macht `fsync` künstlich langsam
(20 ms bzw. 100 ms). Liegt irgendein `fsync` zwischen dem letzten Lesen und dem
Leeren, kostet das bei 200 Zeilen/s sofort ein Dutzend Zeilen; liegt keines
dort, kostet es null — beliebig langsam. Zugesichert wird genau das.

Wer für ein Log **null** Verlust braucht, rotiert es in-process mit
`RotatingFileHandler`, so wie `telegram_bot.py` und `manual_close.py` es tun.
Für Logs, die Cron oder launchd per Umleitung schreiben, existiert dieser Weg
nicht.

### Was nie passiert

* Geleert wird nur, wenn das Archiv nachweislich vollständig ist (Größe ==
  kopierte Bytes) und auf der Platte steht (`fsync` auf Inhalt **und**
  Verzeichniseintrag).
* Alte Stände werden erst **nach** dieser Prüfung gelöscht.
* Wächst eine Datei schneller, als kopiert werden kann, bricht die Rotation nach
  20 Nachlese-Runden ab und leert **nichts**.
* Ein vorhandenes Archiv wird nie überschrieben (`open(..., "xb")`).
* Ein Fehlschlag bei einer Datei stoppt weder die Rotation der anderen noch
  irgendeinen Dienst. Rückgabewert 1 nur bei echtem Fehlschlag — ein Lauf ohne
  fällige Datei ist der Normalfall und keine Cron-Mail wert.

---

## 5. Cron

```cron
30 3 * * * cd ~/trading-bot && /usr/bin/python3 system/log_rotation.py >> logs/system/log_rotation.log 2>&1
```

**Vorschlag im README, nicht eingetragen.** Einmal täglich, weil nach Größe und
nicht nach Zeit rotiert wird — der Takt bestimmt nur, wie oft *nachgesehen*
wird. Bei den heutigen Wachstumsraten reicht das mit großem Abstand; 3:30 Uhr
liegt zwischen den 4-Stunden-Läufen der Bots. Wöchentlich wäre zu selten, wenn
eine Datei plötzlich vollläuft.

Dass die Crontab derzeit klemmt, ist unkritisch: das Skript entscheidet nach
Größe und braucht kein Intervall. Von Hand aufgerufen tut es genau dasselbe.

---

## 6. Tests

`python3 system/test_log_rotation.py` — **117 Prüfungen** in 14 Abschnitten,
gegen echte Dateien in einem Wegwerf-Ordner unter `/tmp`, nie gegen das echte
`logs/`.

Der Kern ist Abschnitt 5: ein **echter zweiter Prozess** (`subprocess`) hält die
Logdatei offen und schreibt durchgehend weiter, während rotiert wird. Danach
wird geprüft, dass die neue Datei wächst, das Archiv **nicht** mehr wächst, der
Inode derselbe ist und am Dateianfang keine Nullbytes stehen. Abschnitt 6
beziffert die Restlücke mit zwei Schreibraten, einem `fsync`-Zähler und einem
künstlich verlangsamten `fsync`.

Weiter geprüft: Schwelle genau auf der Grenze · Archiv byteweise identisch ·
Stände behalten/löschen und *welche* überleben · fremde `.log.1` unberührt ·
Datenbanken, `.json` und `.env` werden nie gefunden · Symlink nach außen
unberührt · Fehlschlag leert nichts, löscht keinen alten Stand und lässt die
anderen Dateien weiterlaufen · unvollständiges Archiv gibt das Leeren nicht frei
· belegter Archivname wird nicht überschrieben · zwei Rotationen in derselben
Sekunde · AST-Abgleich der Handler-Zahlen · keine verbotenen Importe.

**17 Mutationsproben, alle 17 erkannt** (Ablauf und Skript im Testauftrag,
Abschnitt 7). Drei davon prüfen genau den Fehler, den ich selbst gemacht hatte —
und **drei Proben gingen im ersten Durchlauf durch**, was den Tests mehr
eingebracht hat als die dreizehn, die sofort auffielen (Abschnitt 7 unten).

Keine Regression in den bestehenden Suiten — Liste im Ergebnisdokument.

---

## 7. Was die Mutationsproben aufgedeckt haben

Im **ersten** Durchlauf wurden nur 13 von 16 Proben erkannt. Die drei
entgangenen haben mehr an den Tests verbessert als die dreizehn, die sofort
auffielen — deshalb hier vollständig:

**M12 (Symlinks werden mitrotiert) war von einer zweiten Wache verdeckt.** Mein
Symlink-Test legte einen Link, der aus `logs/` heraus zeigte. Entfernt man den
Symlink-Schutz, greift dann immer noch die Pfadgrenze (`_innerhalb`) — der Test
blieb grün, obwohl die geprüfte Zusicherung weg war. Derselbe Fehlertyp wie in
PR #73 (M7/M12), wo eine dritte Notbremsen-Prüfung das Fehlen der zweiten
verdeckte. Behoben durch einen zweiten Fall: ein Symlink **innerhalb** von
`logs/`, bei dem nur der Symlink-Schutz greifen kann.

**M15/M16 (`fsync` an der falschen Stelle) entgingen, weil meine Probe sich
selbst blind machte.** Sie verlangsamte `os.fsync` global. Damit konvergiert die
Nachlese-Schleife nicht mehr — bei jedem langsamen `fsync` kommen neue Zeilen
dazu —, die Rotation bricht nach 20 Runden ab und erreicht das Leeren **nie**.
Kein Leeren, kein Verlust, Probe grün. Behoben durch zwei Änderungen: verlangsamt
wird nur noch der Verzeichnis-`fsync` (die Schleife läuft normal), und ein Zähler
prüft, dass es **genau einen** davon je Rotation gibt — null und zwei fallen
damit beide auf, deterministisch und ohne Timing.

**M17 brauchte eine gemessene Grenze statt einer geschätzten.** Meine erste
Obergrenze (höchstens 5 verlorene Zeilen bei 5 Rotationen) hätte die Mutation
durchgelassen. Also gemessen, je sechs Durchgänge à 10 Rotationen:

| | verlorene Zeilen je 10 Rotationen |
|---|---|
| richtige Reihenfolge | 1, 1, 0, 1, 1, 1 → **max 1** |
| `fsync` hinter dem letzten Lesevorgang | 8, 6, 8, 6, 9, 10 → **min 6** |

Die Grenze liegt jetzt bei **3** — mit Abstand zwischen beidem. Damit ist die
Zusicherung eine Messung und kein Timing-Glück.

Dazu kommt der Befund, der überhaupt zur Umstellung führte: **meine erste
Fassung verlor knapp eine Zeile pro Rotation**, systematisch. Gefunden nicht
durch Nachdenken, sondern weil der Test vollständige Zeilenfolgen einforderte
und sie nicht bekam. Hätte ich die Lücke nur *dokumentiert*, wie es der Auftrag
zugelassen hätte, wäre sie fünfmal größer geblieben als nötig.

---

## 8. Offene Punkte

* **Der neue Cronjob aus PR #78** (`schliess_benachrichtigung.py`) schreibt nach
  `logs/notifications/schliess_benachrichtigung.log`. Diese Datei wird von der
  Rotation erfasst, sobald sie existiert — nichts zu tun. Wer dort **null**
  Verlust will, könnte das Skript stattdessen selbst über einen
  `RotatingFileHandler` protokollieren lassen; das wäre eine eigene, kleine
  Änderung und ist hier absichtlich nicht mitgemacht.
* **Die Wiederholungen in `logs/broker/cron.log`** (dieselben übersprungenen
  Trade-Eröffnungen bei jedem Lauf) sind durch die Rotation nur *gedeckelt*, nicht
  behoben. Die Ursache liegt in `broker/spiegel.py` und steht als eigener
  Backlog-Punkt — laut Auftrag hier ausdrücklich nicht angefasst.
* **Kein Test auf einem Nicht-`O_APPEND`-Schreiber.** Ein solcher Schreiber
  existiert im Projekt nicht; der Fall ist im README benannt (Loch aus Nullbytes,
  kein Datenverlust) und wird durch die Nullbyte-Prüfung in Abschnitt 5
  indirekt bewacht.

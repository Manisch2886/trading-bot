# Übergabe: Konzeptpapier Ereignis-DB und Anbieter-Schnittstelle

**Branch** `claude/new-session-uqjk8h`, Basis `origin/main` (`e93ae56`, nach
Merge von #81). **PR #82.**

**Kein Produktivcode.** Der Diff enthält ausschliesslich drei neue Dateien
unter `docs/`. Keine Datenbank angelegt, keine Migration ausgeführt, kein
bestehender Code angefasst.

---

## Die zwölf Entscheidungen — vorne, wie verlangt

Jede hat im Konzept eine Empfehlung mit Alternative und Begründung. **Keine ist
getroffen.**

| # | Frage | Empfehlung |
|---|---|---|
| **E1** | Eine Ereignis-Tabelle oder eine je Bereich? | eine, mit `art`-Spalte |
| **E2** | Feste Spalten oder freies JSON? | **beides**, mit klarer Grenze |
| **E3** | Zählen **Läufe** als Ereignisse? | ja — sonst bleibt offener Punkt 12 ungelöst |
| **E4** | Wer schreibt? | eine gemeinsame Funktion in `shared/` |
| **E5** | Die drei vorhandenen DBs migrieren? | **nein**, Stichtag; Import optional später |
| **E6** | Aufbewahrung? | 400 Tage roh, danach Tagesverdichtung |
| **A1** | Registrierung statt Konfiguration — hält das? | ja, mit einer benannten Bruchlinie |
| **A2** | „Liest" gegen „handelt"? | zwei Basisklassen, kein Flag |
| **A3** | Echtgeld gegen Paper? | **zwei Datenbankdateien**, keine Spalte |
| **A4** | Crash-Knopf bei mehreren Anbietern? | **nicht erweitern** |
| **A5** | Welchen Anbieter zuerst? | **keinen** |
| **R1** | Wird der Mac zum Server? | **kann dieser Entwurf nicht entscheiden** |

R1 ist die einzige, an der die *Richtung* hängt. Alle anderen betreffen nur den
Umfang.

---

## Die drei Empfehlungen, bei denen ich Widerspruch erwarte

### E5 — die drei vorhandenen Datenbanken **nicht** übernehmen

Naheliegend wäre, `spiegelungen` und `gemeldet` in die neue Tabelle zu
überführen. Dagegen spricht etwas Strukturelles: **das sind keine
Ereignis-Historien, sondern Arbeitsvermerke.** `spiegelungen` beantwortet „ist
diese Order schon draussen?" — eine Frage, die die Brücke bei jedem Lauf neu
stellt und selbst beantworten können muss. Überführt man sie, hängt die
Doppelsende-Sicherung einer produktiv laufenden Brücke plötzlich an einer
Tabelle, die auch das Dashboard beschreibt.

Der Preis: der Zeitstrahl beginnt bei null. Weil die Schlüssel kompatibel sind
(`bot:trade_id:seite`), ist ein Nachimport aber jederzeit möglich — deshalb
steht er als **optionaler** Schritt 7 und nicht als Voraussetzung.

### A4 — den Crash-Knopf nicht erweitern

Der Wunsch, manuelle Trades dort zu hinterlegen, ist verständlich. Drei Gründe
dagegen, der erste trägt allein:

1. Für Trade Republic könnte der Knopf **technisch nichts tun**. Ein Knopf, der
   Schliessen suggeriert und es nicht kann, ist im Notfall schlimmer als keiner.
2. Für Binance ginge es — und würde die Wand einreissen. `api.binance.com`
   steht namentlich auf `VERBOTENE_HOSTS` (zusammen mit neun weiteren Hosts).
   Ihn erreichbar zu machen hiesse, die tragende Sicherheitsannahme des
   gesamten Broker-Bereichs aufzugeben, für eine Funktion, die die Binance-App
   ohnehin hat.
3. Zwei Welten an einem Knopf sind im Notfall eine Frage zu viel — auf 390 px,
   in zwei Sekunden.

Stattdessen: echte Positionen **anzeigen**, deutlich abgesetzt, mit dem
ausdrücklichen Hinweis „schliessen in der App des Anbieters".

### A3 — zwei Datenbankdateien statt einer Spalte `welt`

Eine Spalte schützt nur, solange **jede** Abfrage sie im `WHERE` hat. Eine
vergessene Bedingung fiele niemandem auf, weil das Ergebnis plausibel aussähe —
genau das Fehlerbild, das in PR #81 gerade untersucht wurde. Zwei Dateien machen
den Fehler sichtbar: wer echte Zahlen in eine Paper-Auswertung bekommen will,
muss eine zweite Datei **öffnen**.

---

## Was die Bestandsaufnahme ergeben hat

### Drei Muster, die das Schema tragen

Aus `spiegel.py`, `ibkr_spiegel.py` und `schliess_benachrichtigung.py`:

1. **Ein fachlicher Schlüssel mit `UNIQUE`**, keine `if`-Abfrage. Zwei
   gleichzeitige Läufe scheitern an der Datenbank, nicht an einer Prüfung, die
   dazwischen veralten kann.
2. **Erfolg und Versuch sind getrennte Tabellen.** Beide Brücken führen
   `versuche` neben `spiegelungen` — ausdrücklich, damit ein Fehlschlag den
   `UNIQUE`-Platz nicht belegt und den nächsten Versuch blockiert. Das ist die
   wichtigste Einzelerkenntnis.
3. **Zeitstempel als UTC-Text.**

Nur die Schliess-Benachrichtigung kennt **Zustände** — weil bei ihr Anspruch und
Wirkung auseinanderfallen (ein Netzaufruf dazwischen). Bei den Brücken
übernimmt die `client_order_id` diese Rolle. Die gemeinsame Tabelle muss beides
tragen, deshalb sind Zustände im Entwurf in eine **zweite** Tabelle
(`zustellungen`) ausgelagert: sie gehören zur Zustellung, nicht zum Ereignis.

### Siebzehn Ereignisarten, sieben Ablageorte

Vollständig erhoben. Telegram, zwei Nachverfolgungs-DBs, eine JSON-Datei, zwei
Logdateien, E-Mail und ein Markdown-Dokument, das **von Hand** gepflegt wird.

**Die drei, die heute nirgends abfragbar landen**, sind die, die am meisten
fehlen: `lauf_begonnen`/`lauf_beendet` (blockiert Punkt 12 und die
Systemgesundheits-Seite), `agenten_hinweis` (verschwindet im Postfach),
`bruecken_abweichung` (steht in einer Spalte, die niemand ansieht).

### Was `monitor.py` und `state.json` lehren

Der Gegenentwurf, und sein Docstring dokumentiert den Vorfall selbst:
`state.json` wurde einmal gespeichert, **bevor** der Versand bestätigt war —
ein Ereignis galt als gemeldet, ohne je verschickt worden zu sein. Dazu die
bekannte Schwäche des Mengenvergleichs (was zwischen zwei Läufen auf- und
zuging, kommt nicht vor) und das stille Neu-Anfangen bei verlorener Datei.

Drei bindende Lehren im Entwurf: **je Vorgang eine Zeile**, **erst bestätigen,
wenn die Wirkung eingetreten ist**, **ein verlorener Zustand muss auffallen**.

---

## Die Randbedingung, die den Entwurf formt

**`forward_test.py` und `live_params.py` dürfen nicht angefasst werden — also
können die neun Bots nichts melden.** Daraus folgt eine Zweiteilung:
Selbstmelder (Brücken, Dashboard, Benachrichtigungen) rufen die Schreibfunktion
direkt; die Bots werden von einem **Sammler** fremdbeobachtet.

Für Trades funktioniert das sauber (schreibgeschützter Zugriff auf die
Bot-DBs, `UNIQUE` macht Wiederholungen folgenlos). **Für Läufe nicht.** Drei
mögliche Ersatzquellen, alle mangelhaft:

| Quelle | Mangel |
|---|---|
| Änderungszeit von `cron.log` | ein Lauf ohne Ausgabe ändert nichts; Rotation setzt sie zurück |
| Neue Zeilen im Cron-Log | ein stiller Lauf bleibt unsichtbar |
| Cron-Mail | nur bei Fehlern — und die Mails sind abgeschaltet |

**Deshalb ist E3 eine echte Entscheidung mit Preis.** Empfehlung: kurzfristig
die Heuristik bauen und die Ereignisse als `quelle='heuristik'` kennzeichnen —
eine Aussage mit angeschriebener Unsicherheit ist mehr wert als keine.
Mittelfristig liegt die Frage beim Nutzer, ob zwei Zeilen in `forward_test.py`
die Ausnahme wert sind.

---

## Zahlen, die den Entwurf tragen

**Nebenläufigkeit:** rund **730 Prozessstarts am Tag**, die schreiben könnten.
Bei ~2.000 Schreibvorgängen à 5 ms ist die Datenbank rund **10 Sekunden von
86.400** beschäftigt — 0,01 %. Kollisionen sind selten, aber **gebündelt**, weil
Cronjobs auf der Minute starten.

**Ein Nebenbefund aus der Bestandsaufnahme:** von allen Schreibpfaden im Repo
setzt **nur `manual_close.py`** ausdrücklich `busy_timeout` und
`isolation_level=None`. Die drei Nachverfolgungs-DBs laufen auf der
Voreinstellung, **WAL benutzt niemand.** Für die Ereignis-DB ist WAL fast
wichtiger als der Timeout, weil das Dashboard bei jedem Seitenaufruf liest.

**Wachstum:** rund **90 Ereignisse am Tag**, **33.000 im Jahr**, etwa **10 MB**.
Über **80 % davon wären Lauf-Ereignisse** — genau die, die einzeln niemanden
interessieren und in Summe alles beantworten. Daraus die Verdichtungsregel in
E6.

---

## Umsetzung in zehn Schritten

Vollständig im Konzept, Abschnitt 4. Zwei Punkte für die Review:

* **Schritt 6 ist der Punkt, an dem das Projekt etwas gewinnt** statt nur etwas
  hinzuzufügen: `monitor.py` liest aus der Ereignis-DB, `state.json` entfällt.
  Vorher laufen alter und neuer Weg parallel. Es ist auch der Schritt mit der
  höchsten Unsicherheit — ein laufender Meldeweg wird umgehängt.
* **Nach Schritt 5 kann man aufhören.** Der Zeitstrahl ist da und nützlich, ohne
  dass ein bestehender Meldeweg verändert wurde. Der natürliche Haltepunkt,
  falls sich die Prioritäten verschieben.

Schritt 9 (Anbieter-Schnittstelle) steht bewusst **hinten**: er fasst als
einziger produktiven Brücken-Code an und wird erst wertvoll, wenn es einen
dritten Anbieter gibt — den es laut A5 vorerst nicht geben soll.

---

## Was der Entwurf nicht kann

* **Offenen Punkt 12 nicht vollständig lösen** — ohne Zeile in
  `forward_test.py` bleibt „Lauf stattgefunden" eine Heuristik.
* **Die App nicht erreichbar machen, während der Mac schläft.** Vier Stellen,
  an denen das durchschlägt, stehen in Abschnitt 1.1 des Konzepts.
* **Nicht verhindern, dass jemand Echt- und Paper-Zahlen addiert** — nur
  erzwingen, dass es eine bewusste Handlung ist.
* **Den Migrationspfad nicht erprobt.** Schritt 7 ist auf dem Papier einfach,
  weil die Schlüssel kompatibel sind; ob die Zeitstempel beider Brücken
  durchgängig im selben Format vorliegen, ist **nicht geprüft**.
* **Die Ereignismenge geschätzt, nicht gemessen** — auf Basis der Cron-Takte
  und 22 bisher geschlossenen Trades.

## Fünf Fragen, die offen bleiben müssen

1. **R1:** Umzug auf einen dauerhaft laufenden Rechner?
2. **E3:** Zwei Zeilen in `forward_test.py` wert?
3. **A4:** Bleibt der Crash-Knopf bei der Paper-Welt?
4. **E6:** 400 Tage Rohdaten — oder alles behalten?
5. **Schritt 6:** `monitor.py` umhängen, oder alten Weg dauerhaft parallel
   lassen? Parallel ist sicherer, bedeutet aber wieder zwei Wahrheiten — genau
   der Zustand, den PR #78 beseitigt hat.

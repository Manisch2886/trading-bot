# Testplan Warteauftraege — zur autonomen Ausfuehrung durch eine Claude-Code-Sitzung

**Dieses Dokument ist NICHT fuer einen Menschen zum Abtippen gedacht.** Es ist
die Arbeitsanweisung fuer eine eigenstaendige Claude-Code-Sitzung, die lokal
auf dem Mac laeuft (`claude` im Terminal, im Ordner `~/trading-bot`).

Die menschliche Fassung derselben Pruefungen steht in
[`TESTANLEITUNG_SCHLIESSEN.md`](TESTANLEITUNG_SCHLIESSEN.md), Teil 2. Wer
lieber selbst tippt, nimmt die. Beide pruefen dasselbe.

**Startbefehl fuer den Nutzer** (im Terminal, im Projektordner):

```
claude "Lies dashboard/TESTPLAN_WARTEAUFTRAEGE_AGENT.md und arbeite ihn ab."
```

---

## 0. Auftrag und Grundregeln

**Dein Auftrag:** Die Warteauftrags-Funktion aus Pull Request #71 auf diesem
Rechner pruefen und am Ende einen Bericht abgeben, aus dem hervorgeht, ob sie
in Betrieb genommen werden kann.

**Arbeite die Phasen 1 bis 6 selbstaendig ab.** Halte nicht nach jedem Befehl
an und frage nicht nach Erlaubnis fuer Schritte, die dieses Dokument
ausdruecklich vorsieht. Halte nur an, wo unten **STOPP** steht.

### Harte Grenzen — diese gelten ausnahmslos

| Verboten | Warum |
|---|---|
| In eine **echte** Bot-Datenbank schreiben (`~/trading-bot/paper_trading_*.db`) | Das ist der Live-Stand des Paper-Tradings. Geschrieben wird ausschliesslich in der Arbeitskopie aus Phase 4 |
| `crontab` aendern | Die Einrichtung des Cronjobs ist eine bewusste Entscheidung des Nutzers (Phase 7) |
| `git commit`, `git push`, `git merge`, Branch wechseln | Du pruefst, du entwickelst nicht |
| `cat ~/trading-bot/.env` oder den Token sonst irgendwo ausgeben | Die Datei enthaelt Zugangsdaten. Es hat in diesem Projekt schon zwei versehentliche Preisgaben gegeben. Pruefe Vorhandensein ausschliesslich mit `grep -c` |
| Dateien im echten Projekt loeschen oder veraendern | Ausnahme: die Arbeitskopie und Dateien unterhalb von `~/trading-bot-probe-warteauftraege` |

**Wenn eine Pruefung fehlschlaegt:** brich die laufende Phase ab, fuehre die
folgenden Phasen **nicht** aus, raeume gemaess Phase 8 auf und schreibe den
Bericht mit dem Befund. Repariere **keinen** Code — die Aufgabe ist Pruefen,
nicht Beheben. Ein Fehlschlag ist ein Ergebnis, kein Hindernis.

**Wenn ein Befehl unerwartet ausgibt, was hier nicht vorgesehen ist** (fehlende
Datei, fehlendes Programm, anderer Wortlaut): behandle das als Fehlschlag mit
Begruendung. Rate nicht.

### Ausgabeformat waehrend der Arbeit

Nach jeder Phase genau eine Zeile:

```
PHASE <n> <PASS|FAIL|UEBERSPRUNGEN>: <ein Satz>
```

Die Einzelbefunde sammelst du fuer den Abschlussbericht (Phase 9).

---

## Phase 1 — Bestandsaufnahme

```bash
cd ~/trading-bot && pwd && git branch --show-current && git log --oneline -1
```

**Erwartung:** Der Branch heisst `claude/admiring-turing-74tohm` (oder `main`,
falls PR #71 bereits gemergt wurde). Der letzte Commit erwaehnt
`Warteauftraege`.

**PASS-Bedingung:** Einer der beiden Branches, und die Dateien aus dem
naechsten Befehl existieren.

```bash
ls -1 notifications/boersenkalender.py notifications/warteauftraege.py dashboard/warteauftraege_ausfuehren.py requirements.txt
```

**Erwartung:** Alle vier Pfade werden ausgegeben, kein `No such file`.

**FAIL bedeutet hier:** Der Branch aus PR #71 ist nicht ausgecheckt. Sag dem
Nutzer, er soll `git checkout claude/admiring-turing-74tohm` ausfuehren, und
halte an.

```bash
which python3 && python3 --version
```

**Erwartung:** Python 3.9 oder neuer. **Merke dir diesen Interpreter** und
benutze in allen folgenden Phasen genau ihn — das Dashboard und der Cronjob
laufen ebenfalls mit `python3`.

---

## Phase 2 — Abhaengigkeiten

```bash
python3 -c "import pandas_market_calendars, fastapi, uvicorn; print('ok')"
```

**Erwartung:** `ok`.

**Bei `ModuleNotFoundError`:** einmal installieren und den Befehl wiederholen:

```bash
pip3 install -r ~/trading-bot/requirements.txt
```

**PASS-Bedingung:** Der Import-Befehl gibt am Ende `ok` aus. Wenn die
Installation scheitert (kein Netz, Rechteproblem), ist das FAIL — notiere die
Fehlermeldung wortwoertlich; ohne die Bibliothek ist die Funktion nicht
betriebsbereit.

```bash
python3 -c "import pandas_market_calendars as m; print(m.__version__)"
```

**Erwartung:** eine Version >= 4.1 (auf Python 3.9 typischerweise 4.x, auf
3.10+ 5.x). Beides ist richtig — notiere, welche es ist.

---

## Phase 3 — Statische Pruefungen (fassen nichts an)

```bash
cd ~/trading-bot && python3 -m py_compile notifications/*.py dashboard/*.py && echo "py_compile ok"
```

**Erwartung:** `py_compile ok`, keine Ausgabe davor.

```bash
cd ~/trading-bot && git diff --stat main -- strategies/ ; echo "ENDE"
```

**Erwartung:** Zwischen dem Befehl und `ENDE` steht **nichts**. Das ist der
Nachweis, dass die Bot-Handelslogik unangetastet ist.

**FAIL-Bedingung:** Es erscheint irgendeine Datei unterhalb von `strategies/`.
Das waere ein schwerer Befund — brich sofort ab und berichte ihn.

*(Falls der Branch bereits gemergt ist und `main` deshalb identisch ist, gibt
der Befehl ebenfalls nichts aus. Das ist dann kein Beleg, sondern nur kein
Widerspruch — notiere das im Bericht.)*

---

## Phase 4 — Selbsttests

```bash
cd ~/trading-bot && python3 dashboard/test_dashboard.py 2>&1 | tail -20
```

**Laufzeit:** etwa 30 bis 90 Sekunden. Warte ab.

**Erwartung:** Die letzte Zeile lautet

```
738/738 Pruefungen bestanden.
```

**PASS-Bedingung:** Beide Zahlen sind gleich und die Zeile endet auf
`bestanden.`. Die genaue Zahl darf abweichen, wenn der Branch inzwischen
weiterentwickelt wurde — **gleich muessen die beiden Zahlen sein**.

**FAIL-Bedingung:** Irgendwo steht `[FEHLER]` oder `FEHLGESCHLAGEN`. Notiere
die betroffene Zeile vollstaendig.

Diese Tests fassen weder echte Datenbanken noch die echte Auftragsdatei an —
sie laufen gegen ein synthetisches Projekt in einem temporaeren Ordner.

---

## Phase 5 — Der Boersenkalender

Reine Rechnung, kein Netz, kein Schreibzugriff. Fuehre die fuenf Befehle aus
und vergleiche jeweils das Feld `"offen"`.

```bash
cd ~/trading-bot
python3 notifications/boersenkalender.py "2026-09-10 17:00"
python3 notifications/boersenkalender.py "2026-09-12 17:00"
python3 notifications/boersenkalender.py "2026-11-26 17:00"
python3 notifications/boersenkalender.py "2026-11-27 17:30"
python3 notifications/boersenkalender.py "2026-11-27 18:30"
```

| Zeitpunkt (UTC) | Was das ist | `"offen"` muss sein |
|---|---|---|
| 2026-09-10 17:00 | normaler Donnerstag, 13:00 New York | `true` |
| 2026-09-12 17:00 | Samstag | `false` |
| 2026-11-26 17:00 | **Thanksgiving**, Donnerstag mitten in der Handelszeit | `false` |
| 2026-11-27 17:30 | Tag nach Thanksgiving, 12:30 New York | `true` |
| 2026-11-27 18:30 | derselbe Tag, 13:30 New York — **verkuerzter Handelstag** | `false` |

**PASS-Bedingung:** Alle fuenf stimmen. Die letzten beiden sind der eigentliche
Beleg: derselbe Kalendertag, einmal offen und einmal zu — eine Zeitregel
`bis 22:00 deutscher Zeit` waere hier drei Stunden lang falsch.

Zusaetzlich beim dritten Befehl:

**Erwartung:** `"letzter_handelstag": "2026-11-25"` — also der Mittwoch davor.

Und der aktuelle Stand, den du fuer Phase 7 brauchst:

```bash
cd ~/trading-bot && python3 notifications/boersenkalender.py
```

**Merke dir:** ob `"offen"` gerade `true` oder `false` ist. Davon haengt ab,
welchen Zweig du in Phase 7 siehst.

---

## Phase 6 — Arbeitskopie: der vollstaendige Ablauf mit echten Bot-Dateien

Hier wird geschrieben — ausschliesslich in der Kopie.

**6.1 Kopie anlegen**

```bash
rm -rf ~/trading-bot-probe-warteauftraege
cp -R ~/trading-bot ~/trading-bot-probe-warteauftraege
touch ~/trading-bot-probe-warteauftraege/.probe-kopie
```

**6.2 Eigenes Token fuer die Kopie** — das echte wird dabei ueberschrieben und
nicht gelesen:

```bash
cd ~/trading-bot-probe-warteauftraege
python3 -c "import secrets; print('DASHBOARD_ACCESS_TOKEN=' + secrets.token_urlsafe(32))" > .env
printf 'TELEGRAM_BOT_TOKEN=nur-fuer-die-probe\nTELEGRAM_USER_ID=0\n' >> .env
grep -c DASHBOARD_ACCESS_TOKEN .env
```

**Erwartung:** `1`. **Gib den Inhalt der Datei nicht aus.**

**6.3 Nachweisen, dass die Kopie wirklich eigene Datenbanken hat**

```bash
ls -l ~/trading-bot-probe-warteauftraege/paper_trading_volatility_breakout.db ~/trading-bot/paper_trading_volatility_breakout.db
```

**Erwartung:** zwei verschiedene Pfade, beide existieren. Falls die Datei im
echten Projekt fehlt (der Bot lief noch nie), legt das Pruefskript in der
Kopie selbst eine an — dann ist auch das in Ordnung, notiere es.

**6.4 Zustand der ECHTEN Datenbank festhalten** (nur lesend, als Gegenprobe
fuer Phase 8):

```bash
cd ~/trading-bot && sqlite3 paper_trading_volatility_breakout.db "SELECT COUNT(*), SUM(status='open') FROM trades;"
```

**Merke dir die Ausgabe.** Sie muss am Ende unveraendert sein.

**6.5 Das Pruefskript laufen lassen**

```bash
cd ~/trading-bot-probe-warteauftraege && python3 dashboard/pruefe_warteauftraege_kopie.py
```

**Laufzeit:** wenige Sekunden.

**Erwartung:** Die letzte Zeile lautet `32/32 Pruefungen bestanden.` (beide
Zahlen gleich), und der Rueckgabewert ist 0. Jede Einzelzeile beginnt mit
`[PASS]`.

Das Skript prueft in dieser Reihenfolge:

| Abschnitt | Was belegt wird |
|---|---|
| Vorbedingungen | Schreibkern und Auftragsdatei zeigen auf die **Kopie** |
| 1) Boerse geschlossen | Vorgang wird zum Warteauftrag; **ohne** Bestaetigung passiert nichts; **mit** Bestaetigung entsteht ein Auftrag und die Datenbank bleibt unveraendert; der Auftrag enthaelt keinen Kurs |
| 2) Feiertag | auch dann wird nichts geschlossen |
| 3) Boerse offen | Trockenlauf schreibt nichts; der Ernstfall schliesst zum Kurs des Ausfuehrungszeitpunkts, vermerkt `manual_close`, PnL nach der Bot-Formel |
| 4) Der Bot war schneller | der Auftrag wird **uebersprungen**, nicht ausgefuehrt; die Zeile des Bots bleibt unberuehrt |
| 5) Stornieren | verhindert die spaetere Ausfuehrung; die Position bleibt offen |
| 6) Krypto | am Samstag sofort handelbar; ein Krypto-Warteauftrag wird abgelehnt |

**FAIL-Bedingung:** irgendein `[FAIL]`, oder Rueckgabewert 1 oder 2.
Rueckgabewert 2 heisst: die Markierungsdatei aus 6.1 fehlt — dann hast du
Schritt 6.1 unvollstaendig ausgefuehrt, hole ihn nach.

**6.6 Gegenprobe: das Skript verweigert den echten Projektordner**

```bash
cd ~/trading-bot && python3 dashboard/pruefe_warteauftraege_kopie.py ; echo "Rueckgabewert=$?"
```

**Erwartung:** `ABBRUCH: keine Markierungsdatei .probe-kopie …` und
`Rueckgabewert=2`. Es darf **keine** Pruefzeile erscheinen.

Diese Gegenprobe ist wichtig: sie belegt, dass die Sperre wirkt und die
gruenen Ergebnisse aus 6.5 nicht daher kommen, dass ohnehin alles erlaubt ist.

---

## Phase 7 — Die API der Kopie (curl, ohne Browser)

**7.1 Dashboard der Kopie starten**, auf einem eigenen Port, im Hintergrund:

```bash
cd ~/trading-bot-probe-warteauftraege && DASHBOARD_PORT=8799 nohup python3 dashboard/server.py > /tmp/probe-dashboard.log 2>&1 &
sleep 6 && tail -3 /tmp/probe-dashboard.log
```

**Erwartung:** Das Log nennt eine Adresse mit Port 8799 und keinen Fehler.
Falls der Port belegt ist, nimm 8801 und passe die folgenden Befehle an.

**7.2 Token der Kopie in eine Variable holen** (ohne es auszugeben):

```bash
cd ~/trading-bot-probe-warteauftraege && T=$(grep DASHBOARD_ACCESS_TOKEN .env | cut -d= -f2-)
```

**7.3 Die vier Pruefungen**

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8799/api/warteauftraege
```
**Erwartung:** `401` — ohne Token geht nichts.

```bash
curl -s -H "X-Dashboard-Token: $T" http://127.0.0.1:8799/api/warteauftraege
```
**Erwartung:** JSON mit `"auftraege"`, `"anzahl"` und einem `"boerse"`-Block.
Der Wert von `boerse.offen` muss zu dem passen, was Phase 5 zuletzt ausgegeben
hat. **Widerspruch = FAIL.**

```bash
curl -s -w "\n%{http_code}\n" -X POST -H "X-Dashboard-Token: $T" -H "Content-Type: application/json" \
  -d '{"vorgang":"frei-erfunden","warteauftrag_bestaetigt":true}' \
  http://127.0.0.1:8799/api/bots/volatility_breakout/schliessen/ausfuehren
```
**Erwartung:** `409` und eine Meldung, die mit `Keine gueltige Bestaetigung
offen` beginnt. Das ist die wichtigste Einzelpruefung dieser Phase: **ein
einzelner Aufruf kann nichts ausloesen**, auch nicht mit gesetztem
Bestaetigungsfeld.

```bash
curl -s -w "\n%{http_code}\n" -X POST -H "X-Dashboard-Token: $T" -H "Content-Type: application/json" \
  -d '{"id":"gibtsnicht"}' http://127.0.0.1:8799/api/warteauftraege/stornieren
```
**Erwartung:** `409` und `Es gibt keinen Warteauftrag mit der Kennung`.

**7.4 Die Positionsliste eines Aktien-Bots**

```bash
curl -s -H "X-Dashboard-Token: $T" "http://127.0.0.1:8799/api/bots/volatility_breakout/schliessbare-positionen" \
 | python3 -c "import json,sys; d=json.load(sys.stdin); print('schliessbar:', d['schliessbar'], '| offen:', d['boerse']['offen'], '| warteauftrag_noetig:', d['boerse']['warteauftrag_noetig'], '| positionen:', len(d['positionen']))"
```

**Erwartung:** `schliessbar: True`. Und **genau eine** der beiden folgenden
Kombinationen, passend zum aktuellen Kalenderstand aus Phase 5:

| Boerse laut Kalender | `offen` | `warteauftrag_noetig` |
|---|---|---|
| offen | `True` | `False` |
| geschlossen | `False` | `True` |

**FAIL:** beide `False` (das hiesse "Kalender unbekannt" — dann ist die
Bibliothek nicht erreichbar) oder eine andere Kombination.

**7.5 Server wieder beenden**

```bash
pkill -f "trading-bot-probe-warteauftraege/dashboard/server.py" ; sleep 1 ; echo "beendet"
```

---

## Phase 8 — Beweisen, dass das echte Projekt unberuehrt ist

```bash
cd ~/trading-bot && sqlite3 paper_trading_volatility_breakout.db "SELECT COUNT(*), SUM(status='open') FROM trades;"
```

**Erwartung:** exakt dieselbe Ausgabe wie in Schritt 6.4.

```bash
ls ~/trading-bot/notifications/warteauftraege.json 2>&1
```

**Erwartung:** `No such file or directory` — **es sei denn**, der Nutzer hatte
schon vorher einen echten Warteauftrag angelegt. Falls die Datei existiert:
gib ihren Inhalt aus (sie enthaelt keine Zugangsdaten) und weise im Bericht
darauf hin, dass sie **vor** deinem Lauf schon da war.

```bash
cd ~/trading-bot && git status --short
```

**Erwartung:** keine Ausgabe. Falls doch etwas erscheint, hast du versehentlich
im echten Projekt geschrieben — das gehoert in den Bericht.

**Trockenlauf im echten Projekt** (liest nur, schreibt garantiert nichts):

```bash
cd ~/trading-bot && python3 dashboard/warteauftraege_ausfuehren.py --trockenlauf
```

**Erwartung, wenn kein Auftrag wartet:** eine Zeile `Keine Warteauftraege -
nichts zu tun.` Wenn einer wartet: eine Zeile, die entweder den Kalenderstand
nennt oder mit `TROCKENLAUF (nichts geschrieben):` beginnt. In **keinem** Fall
darf `GESCHLOSSEN:` erscheinen.

**Aufraeumen:**

```bash
rm -rf ~/trading-bot-probe-warteauftraege && echo "Kopie entfernt"
```

---

## Phase 9 — STOPP: visuelle Pruefung im Browser (nur ein Mensch kann das)

Ab hier hoerst du auf, Befehle auszufuehren. Gib dem Nutzer **wortwoertlich**
die folgende Liste und bitte ihn, sie durchzugehen und dir die Ergebnisse zu
nennen. Erklaere dabei in einem Satz, warum du das nicht selbst kannst: es
geht um Aussehen und Bedienbarkeit, nicht um Werte.

> **Bitte im Browser pruefen.** Dashboard starten mit
> `python3 ~/trading-bot/dashboard/server.py`, dann `http://127.0.0.1:8787/`
> oeffnen und anmelden.
>
> **A. Waehrend die Boerse geschlossen ist** (abends oder am Wochenende), eine
> Bot-Detailseite eines Aktien-Bots oeffnen (`volatility_breakout`,
> `turtle_soup_stocks`, `rsi2_mean_reversion` oder `elliott_wave_stocks`):
> 1. Heisst der Knopf in der Positionszeile **"Vormerken"** statt "Schliessen"?
> 2. Nennt die Fussnote darunter, dass die Boerse geschlossen ist und wann sie
>    wieder oeffnet?
> 3. Knopf antippen: erscheint die Zusammenfassung mit dem Titel
>    **"Position vormerken?"** und dem Knopf **"Weiter"**?
> 4. "Weiter" antippen: erscheint ein **zusaetzlicher blauer Warnblock** mit
>    dem letzten Handelstag, der naechsten Oeffnung und dem Satz, dass spaeter
>    **ohne erneute Rueckfrage** ausgefuehrt wird?
> 5. Mit Esc abbrechen: ist danach **nichts** passiert (keine neue Tabelle,
>    Position weiterhin offen)?
> 6. Von vorn, diesmal "Verstanden - Warteauftrag anlegen": erscheint die
>    Tabelle **"Wartende Auftraege"**, und steht die Position in der oberen
>    Tabelle weiterhin als **offen** mit dem Vermerk "Warteauftrag steht"?
> 7. Uebersichtsseite: steht derselbe Auftrag dort in der bot-uebergreifenden
>    Liste?
> 8. "Stornieren" klicken: verschwindet er ohne Rueckfrage, und bleibt die
>    Position offen?
>
> **B. Waehrend die Boerse offen ist** (Mo-Fr, 15:30-22:00 deutscher Zeit,
> ausser an US-Feiertagen), dieselbe Seite:
> 9. Heisst der Knopf wieder **"Schliessen"**, gibt es **keinen** Warnschritt,
>    und ist es wieder **ein** Tap?
>
> **C. Krypto-Gegenprobe**, zu beliebiger Zeit, z. B. `t3_supertrend`:
> 10. Steht dort weiterhin "Schliessen", ohne Warnschritt und ohne wartende
>     Auftraege?
>
> **D. Auf dem iPhone** (der eigentliche Einsatzort, Safari):
> 11. Oeffnet sich der Dialog mit dem zusaetzlichen Schritt sauber, sind beide
>     Knoepfe erreichbar, und verwirft die Zurueck-Geste den Vorgang?

Notiere die Antworten fuer den Bericht. Ungeprueft gebliebene Punkte sind
**nicht** bestanden, sondern offen — schreibe sie als solche auf.

---

## Phase 10 — STOPP: die Entscheidungen, die dem Nutzer gehoeren

Fuehre **nichts** davon aus. Lege dem Nutzer beides vor und warte auf seine
Antwort.

**Entscheidung 1 — Cronjob einrichten?** Erklaere in eigenen Worten, was der
Eintrag bedeutet, und stuetze dich dabei auf diese Punkte:

- Er erteilt eine **Vorab-Erlaubnis fuer alle kuenftigen Warteauftraege**,
  nicht fuer einen einzelnen.
- Zwischen Bestaetigung und Schreibzugriff koennen Stunden bis Tage liegen.
- Der Ausstiegskurs steht beim Bestaetigen **nicht** fest; eine
  Eroeffnungsluecke am Montag trifft den Auftrag voll.
- Der einzige Weg, das zu verhindern, ist **Stornieren**, solange der Auftrag
  wartet.
- **Ohne** den Cronjob werden Auftraege angelegt und angezeigt, aber nie
  ausgefuehrt — ein moeglicher Zwischenschritt zum Beobachten.

Sagt er ja, gib ihm die Befehle aus
[`TESTANLEITUNG_SCHLIESSEN.md`](TESTANLEITUNG_SCHLIESSEN.md), Schritt 17 —
**einzeln, mit einem Blick dazwischen**, nicht als Block zum Kopieren. Fuehre
sie nicht selbst aus: `crontab -e` oeffnet einen Editor und gehoert dem
Nutzer.

**Entscheidung 2 — Pull Request mergen?** Das entscheidet der Nutzer nach
deinem Bericht. Du mergst nicht.

---

## Phase 11 — Abschlussbericht

Gib genau diese Struktur aus, gefuellt mit dem, was du gemessen hast. Keine
Schaetzungen, keine Vermutungen; was du nicht geprueft hast, steht als
"nicht geprueft".

```
# Testbericht Warteauftraege (PR #71)

Datum:            <Datum, Uhrzeit>
Rechner/Pfad:     <Ausgabe von pwd>
Branch/Commit:    <Branch, Kurz-Hash>
Python:           <Version>, pandas_market_calendars <Version>
Boerse waehrend des Laufs: <offen|geschlossen> (laut Kalender)

## Ergebnis je Phase
| Phase | Gegenstand | Ergebnis |
|---|---|---|
| 1 | Bestandsaufnahme | PASS/FAIL |
| 2 | Abhaengigkeiten | PASS/FAIL |
| 3 | Statische Pruefungen, Bot-Code unveraendert | PASS/FAIL |
| 4 | Selbsttests (<x>/<y>) | PASS/FAIL |
| 5 | Boersenkalender, 5 Zeitpunkte | PASS/FAIL |
| 6 | Arbeitskopie, Pruefskript (<x>/<y>) | PASS/FAIL |
| 7 | API der Kopie, 4 Pruefungen | PASS/FAIL |
| 8 | Echtes Projekt unberuehrt | PASS/FAIL |
| 9 | Visuelle Pruefung (Mensch) | PASS/FAIL/offen |

## Befunde
<Jeder Fehlschlag mit Befehl, erwarteter und tatsaechlicher Ausgabe.
 Wenn es keine gab: "Keine.">

## Was NICHT geprueft wurde
<z. B.: der Zweig "Boerse offen" in der Oberflaeche, weil der Lauf abends
 stattfand; iPhone-Safari; der Cronjob selbst.>

## Empfehlung
<Eine von dreien, mit Begruendung in zwei Saetzen:
 - "Bereit zur Inbetriebnahme" (alles PASS, visuelle Pruefung durch)
 - "Bereit, aber ohne Cronjob" (alles PASS, Nutzer will erst beobachten)
 - "Nicht bereit" (mindestens ein FAIL - welcher)>
```

**Wichtig fuer den Schluss:** Empfiehl die Inbetriebnahme nur, wenn die Phasen
1 bis 8 alle PASS sind **und** die visuelle Pruefung aus Phase 9 tatsaechlich
stattgefunden hat. Eine nicht durchgefuehrte Pruefung ist kein Erfolg.

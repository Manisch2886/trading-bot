# Testauftrag caffeinate-Dienst — zur autonomen Ausfuehrung durch eine Claude-Code-Sitzung

**Dieses Dokument ist NICHT zum Abtippen fuer einen Menschen gedacht.** Es ist
die Arbeitsanweisung fuer eine eigenstaendige Claude-Code-Sitzung, die lokal
auf dem Mac laeuft (`claude` im Terminal, im Ordner `~/trading-bot`). Nur dort
ist die Pruefung ueberhaupt moeglich: `launchctl`, `pmset` und `caffeinate`
gibt es nur unter macOS.

**Startbefehl fuer den Nutzer** (im Terminal, im Projektordner):

```
claude "Lies system/TESTAUFTRAG_CAFFEINATE.md und arbeite ihn ab."
```

---

## 0. Auftrag und Grundregeln

**Dein Auftrag:** Pruefen, ob die caffeinate-launchd-Vorlage aus diesem Branch
auf diesem Mac das tut, was sie soll — den Rechner wachhalten, ohne
Terminalfenster, und nach einem Prozessabbruch von selbst wiederkommen. Am
Ende gibst du den Bericht aus Phase 9 aus.

**Arbeite die Phasen 1 bis 9 selbstaendig ab.** Halte nicht nach jedem Befehl
an und frage nicht nach Erlaubnis fuer Schritte, die dieses Dokument
ausdruecklich vorsieht. Halte nur an, wo unten **STOPP** steht.

### Harte Grenzen — diese gelten ausnahmslos

| Verboten | Warum |
|---|---|
| `crontab` aendern | Die Cron-Eintraege sind der Live-Betrieb des Paper-Tradings. Dieser Auftrag fasst sie nicht an |
| Die bestehenden Dienste `com.manisch.telegram-tradesignal-bot` und einen etwaigen Dashboard-Dienst laden, entladen oder aendern | Sie laufen produktiv. Du liest ihren Zustand, mehr nicht |
| In eine Bot-Datenbank schreiben (`~/trading-bot/paper_trading_*.db`) | Live-Stand des Paper-Tradings |
| `sudo`, `/Library/LaunchDaemons`, Systemeinstellungen aendern | Ein LaunchDaemon ist in `README_CAFFEINATE.md` bewusst nur als Option erwaehnt und ausdruecklich nicht Teil dieser Aufgabe |
| `cat ~/trading-bot/.env` oder Zugangsdaten sonst ausgeben | Es hat in diesem Projekt schon versehentliche Preisgaben gegeben. Vorhandensein nur mit `grep -c` pruefen |
| `git commit`, `git push`, `git merge`, Branch wechseln | Du pruefst, du entwickelst nicht |
| Dateien im Projekt aendern oder loeschen | Ausnahme: die Log-Dateien unter `logs/system/`, die der Dienst selbst anlegt |

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

```bash
ls -l system/
```

**Erwartung:** Branch `claude/caffeinate-launchd-service-e95487` (oder `main`,
falls der Pull Request bereits gemergt wurde). In `system/` liegen
`com.manisch.caffeinate.plist`, `README_CAFFEINATE.md`,
`TESTAUFTRAG_CAFFEINATE.md` und `test_caffeinate_plist.py`.

**PASS-Bedingung:** Einer der beiden Branches, und alle vier Dateien sind da.

---

## Phase 2 — Automatisierte Selbsttests

Zuerst der Test zu dieser Aufgabe:

```bash
cd ~/trading-bot && python3 system/test_caffeinate_plist.py; echo "EXIT=$?"
```

**Erwartung:** `EXIT=0`, kein `[FEHLER]`. Notiere die Zahl bestandener
Pruefungen ("<x> von <y>").

Dann die uebrigen Selbsttests des Projekts — sie duerfen durch diese Aufgabe
nicht schlechter geworden sein. Fuehre sie einzeln aus und notiere je Datei
den Exit-Code:

```bash
cd ~/trading-bot && for t in shared/test_empfehlung_format.py notifications/test_manual_close.py broker/test_broker.py dashboard/test_dashboard.py; do echo "--- $t"; python3 "$t" >/tmp/caffeinate_test_$(basename "$t").log 2>&1; echo "EXIT=$?"; done
```

**Erwartung:** Ueberall `EXIT=0`. Schlaegt einer fehl, sieh in der
zugehoerigen Log-Datei unter `/tmp/` nach und pruefe mit
`git stash list; git status --porcelain`, ob der Fehlschlag ueberhaupt mit
dieser Aufgabe zu tun hat. Ein Test, der auch auf `main` fehlschlaegt, ist
ein Vorbefund und kein FAIL dieser Aufgabe — dann so im Bericht vermerken.

**PASS-Bedingung:** `test_caffeinate_plist.py` mit Exit 0, und kein anderer
Test ist durch diese Aufgabe kaputtgegangen.

---

## Phase 3 — Nichts angefasst, was nicht angefasst werden durfte

```bash
cd ~/trading-bot && git diff --stat main -- strategies/ config/ shared/ notifications/ dashboard/ broker/
```

**Erwartung:** **leere Ausgabe.** Keine `live_params.py`, keine
`forward_test.py`, keine bestehende plist ist veraendert.

```bash
cd ~/trading-bot && git status --porcelain
```

**Erwartung:** leer (oder ausschliesslich ignorierte Laufzeitdateien).

**PASS-Bedingung:** Beide Ausgaben wie erwartet.

---

## Phase 4 — Ist-Zustand des Mac (vor der Installation)

```bash
pmset -g assertions
```

Notiere die Werte von `PreventUserIdleSystemSleep`, `PreventSystemSleep` und
`PreventUserIdleDisplaySleep`.

```bash
pgrep -fl caffeinate
```

Notiere, ob und mit welchen Argumenten ein `caffeinate` laeuft.

```bash
launchctl list | grep com.manisch
```

Notiere alle gefundenen Dienste **mit ihrer PID** — dieselbe Liste vergleichst
du in Phase 8 wieder. Die bestehenden Dienste muessen unveraendert
weiterlaufen.

```bash
pmset -g log | grep -iE "Sleep|Wake" | tail -40
```

Das ist die Gegenprobe zum Anlass dieser Aufgabe: sieh nach, ob der Mac in den
letzten Tagen geschlafen hat, und notiere die letzte Schlafphase mit Uhrzeit.

**PASS-Bedingung:** Die Befehle laufen durch und du hast den Ausgangszustand
notiert. Ein schlafender Mac in der Vergangenheit ist hier **kein** FAIL,
sondern der erwartete Befund.

---

## Phase 5 — STOPP: Installation nur mit ausdruecklicher Zustimmung

Die naechsten Befehle schreiben **ausserhalb des Projektordners**, naemlich
nach `~/Library/LaunchAgents/`, und veraendern das Schlafverhalten des Mac.
Das entscheidet der Nutzer, nicht du.

**Lege ihm Folgendes vor und warte auf seine Antwort:**

- Was installiert wird: ein LaunchAgent, der `/usr/bin/caffeinate -i -m -s`
  dauerhaft laufen laesst und bei jeder Anmeldung automatisch startet.
- Was das bedeutet: der Mac schlaeft im Netzbetrieb nicht mehr von selbst ein.
  Das **Display** darf weiterhin schlafen (kein `-d`, kein `-u`).
- Was es nicht kann: ein zugeklapptes MacBook schlaeft trotzdem; nach einem
  Neustart greift der Dienst erst nach der grafischen Anmeldung; auf reinem
  Batteriebetrieb wirkt `-s` nicht.
- Wie er es rueckgaengig macht: `launchctl unload` plus `rm`, beides in
  `README_CAFFEINATE.md`.
- Dass du nach der Installation (Phase 7) fragen wirst, ob der Dienst laufen
  bleiben oder wieder entfernt werden soll.

**Sagt er nein:** Phasen 6 und 7 als UEBERSPRUNGEN ausgeben, direkt zu Phase 9
springen und im Bericht festhalten, dass die Wirkung auf dem echten System
ungeprueft geblieben ist. Das ist ein zulaessiges Ergebnis, kein FAIL.

**Sagt er ja:** weiter mit Phase 6. Fuehre die Befehle **einzeln** aus und sieh
dir jede Ausgabe an.

---

## Phase 6 — Installation

```bash
mkdir -p ~/trading-bot/logs/system && ls -ld ~/trading-bot/logs/system
```

Falls Phase 4 ein von Hand gestartetes `caffeinate` gefunden hat, jetzt
beenden — sonst laufen zwei Prozesse parallel:

```bash
pkill -x caffeinate; sleep 1; pgrep -fl caffeinate
```

**Erwartung:** keine Ausgabe von `pgrep` mehr. (Gab es in Phase 4 keinen
Prozess, ueberspringe diesen Befehl.)

```bash
cp ~/trading-bot/system/com.manisch.caffeinate.plist ~/Library/LaunchAgents/
```

```bash
plutil -lint ~/Library/LaunchAgents/com.manisch.caffeinate.plist
```

**Erwartung:** `OK`. Das ist Apples eigener Parser — er prueft dieselbe Datei
noch einmal dort, wo launchd sie liest.

```bash
launchctl load ~/Library/LaunchAgents/com.manisch.caffeinate.plist
```

**Erwartung:** keine Ausgabe. Eine Meldung wie `service already loaded` heisst,
dass schon ein Dienst dieses Labels laeuft — dann erst
`launchctl unload ~/Library/LaunchAgents/com.manisch.caffeinate.plist`, dann
erneut laden.

**PASS-Bedingung:** `plutil -lint` sagt `OK` und `launchctl load` laeuft ohne
Fehlermeldung durch.

---

## Phase 7 — Wirkung pruefen

**7a — Dienst laeuft:**

```bash
launchctl list | grep com.manisch.caffeinate
```

**Erwartung:** eine Zeile, links eine PID (keine `-`), in der Mitte `0`.
Notiere die PID.

**7b — Prozess und Flags:**

```bash
pgrep -fl caffeinate
```

**Erwartung:** **genau eine** Zeile, und zwar `/usr/bin/caffeinate -i -m -s`.
Zwei Zeilen sind ein FAIL (paralleler Prozess, siehe Phase 6).

**7c — Der eigentliche Nachweis:**

```bash
pmset -g assertions
```

**Erwartung, beide auf `1`:**

```
   PreventUserIdleSystemSleep     1
   PreventSystemSleep             1
```

und `PreventUserIdleDisplaySleep` weiterhin auf `0` — das Display darf
schlafen. Steht es auf `1`, ist irgendwo doch `-d` oder `-u` im Spiel: FAIL.
Pruefe in der Ausgabe ausserdem, dass `caffeinate` als verantwortlicher
Prozess genannt wird.

**7d — KeepAlive, das Kernversprechen:** Stirbt der Prozess, muss launchd ihn
neu starten. Genau das ist am 11.09.2026 mit dem manuellen Aufruf nicht
passiert.

```bash
pkill -x caffeinate; sleep 5; pgrep -fl caffeinate; launchctl list | grep com.manisch.caffeinate
```

**Erwartung:** `caffeinate` laeuft wieder, mit einer **anderen** PID als in 7a.
Kommt nach 5 Sekunden nichts, noch einmal `sleep 5` und erneut pruefen; bleibt
es leer, ist das ein FAIL.

```bash
pmset -g assertions | grep -E "PreventSystemSleep|PreventUserIdleSystemSleep"
```

**Erwartung:** beide wieder auf `1` — der Schutz ist nach dem Neustart des
Prozesses zurueck.

**7e — Logs:**

```bash
ls -l ~/trading-bot/logs/system/ && wc -c ~/trading-bot/logs/system/caffeinate.err.log
```

**Erwartung:** beide Dateien existieren, `caffeinate.err.log` ist **leer**
(0 Bytes). Steht etwas drin, gehoert es in den Bericht.

**PASS-Bedingung:** 7a bis 7e alle wie erwartet, insbesondere der
PID-Wechsel in 7d.

---

## Phase 8 — Aufraeumen und Gegenprobe

**8a — Die anderen Dienste sind unberuehrt:**

```bash
launchctl list | grep com.manisch
```

**Erwartung:** Dieselben Dienste wie in Phase 4, `com.manisch.caffeinate` neu
dazu. Der Telegram-Dienst hat **dieselbe PID** wie in Phase 4 — er wurde also
nicht neu gestartet.

**8b — Das Projekt ist unveraendert:**

```bash
cd ~/trading-bot && git status --porcelain && git diff --stat main -- strategies/
```

**Erwartung:** beide Ausgaben leer.

**8c — STOPP: soll der Dienst laufen bleiben?** Frage den Nutzer. Er hat zwei
Moeglichkeiten, beide sind zulaessig:

- **Laufen lassen** (der Zweck der Aufgabe): nichts weiter tun.
- **Wieder entfernen** (falls er erst beobachten will): dann diese beiden
  Befehle ausfuehren und die Gegenprobe machen —

```bash
launchctl unload ~/Library/LaunchAgents/com.manisch.caffeinate.plist
```

```bash
rm ~/Library/LaunchAgents/com.manisch.caffeinate.plist
```

```bash
pmset -g assertions | grep -E "PreventSystemSleep|PreventUserIdleSystemSleep"
```

**Erwartung nach dem Entfernen:** beide Werte auf `0`. Weise den Nutzer dann
ausdruecklich darauf hin, dass der Mac ab jetzt wieder einschlafen und damit
wieder Cronjobs verpassen kann.

**PASS-Bedingung:** 8a und 8b wie erwartet, und die Entscheidung aus 8c ist
umgesetzt und im Bericht festgehalten.

---

## Phase 9 — Abschlussbericht

Gib genau diese Struktur aus, gefuellt mit dem, was du gemessen hast. Keine
Schaetzungen, keine Vermutungen; was du nicht geprueft hast, steht als
"nicht geprueft".

```
# Testbericht caffeinate-Dienst

Datum:            <Datum, Uhrzeit>
Rechner/Pfad:     <Ausgabe von pwd>
Branch/Commit:    <Branch, Kurz-Hash>
macOS:            <sw_vers -productVersion>
Stromversorgung:  <Netzbetrieb|Batterie>   (pmset -g batt)
Installiert:      <ja|nein, vom Nutzer abgelehnt>

## Ergebnis je Phase
| Phase | Gegenstand | Ergebnis |
|---|---|---|
| 1 | Bestandsaufnahme | PASS/FAIL |
| 2 | Selbsttests (<x>/<y>), uebrige Tests | PASS/FAIL |
| 3 | Bot-Code und Dienste unveraendert | PASS/FAIL |
| 4 | Ist-Zustand erfasst | PASS/FAIL |
| 5 | Zustimmung des Nutzers | erteilt/verweigert |
| 6 | Installation, plutil -lint | PASS/FAIL/UEBERSPRUNGEN |
| 7 | Wirkung (assertions, KeepAlive) | PASS/FAIL/UEBERSPRUNGEN |
| 8 | Aufraeumen, Gegenprobe | PASS/FAIL |

## Messwerte
Vorher  — PreventSystemSleep: <0|1>, PreventUserIdleSystemSleep: <0|1>, Display: <0|1>
Nachher — PreventSystemSleep: <0|1>, PreventUserIdleSystemSleep: <0|1>, Display: <0|1>
caffeinate-Prozesse nachher: <Anzahl>, Argumente: <...>
KeepAlive-Test: PID vorher <...> -> PID nachher <...>, Neustart nach <n> Sekunden
caffeinate.err.log: <leer|Inhalt>
Letzte Schlafphase laut pmset -g log: <Zeitraum oder "keine gefunden">

## Befunde
<Jeder Fehlschlag mit Befehl, erwarteter und tatsaechlicher Ausgabe.
 Wenn es keine gab: "Keine.">

## Was NICHT geprueft wurde
<z. B.: Verhalten nach einem echten Neustart; zugeklappter Deckel;
 Batteriebetrieb; ob der Dienst ueber Tage stabil bleibt.>

## Empfehlung
<Eine von dreien, mit Begruendung in zwei Saetzen:
 - "Bereit zur Inbetriebnahme" (Phasen 1-8 PASS, Dienst laeuft)
 - "Bereit, aber nicht installiert" (Phasen 1-4 PASS, Nutzer wollte erst beobachten)
 - "Nicht bereit" (mindestens ein FAIL - welcher)>
```

**Wichtig fuer den Schluss:** "Bereit zur Inbetriebnahme" nur, wenn Phase 7
tatsaechlich gelaufen ist **und** der KeepAlive-Test aus 7d bestanden wurde.
Eine nicht durchgefuehrte Pruefung ist kein Erfolg. Weise im Bericht in jedem
Fall auf die vier Grenzen aus `README_CAFFEINATE.md` hin — sie bleiben auch
bei durchweg gruenem Ergebnis bestehen.

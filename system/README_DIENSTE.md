# Die drei launchd-Dienste

Auf dem Mac laufen neben den Cronjobs **drei** Dauerdienste als
*LaunchAgents*. Diese Anleitung gilt fuer alle drei: was jeder tut,
Installation, Pruefen, Neustarten, Entfernen.

| Dienst (Label) | Was er tut | Vorlage | Stand im Repo |
|---|---|---|---|
| `com.manisch.caffeinate` | haelt den Mac wach, damit Cron ueberhaupt laeuft | `system/com.manisch.caffeinate.plist` | vollstaendig |
| `com.manisch.telegram-tradesignal-bot` | Telegram-Bot: Befehle und Push-Nachrichten | `system/com.manisch.telegram-tradesignal-bot.plist` | vollstaendig |
| `com.manisch.trading-dashboard` | FastAPI-Server des Dashboards | `system/com.manisch.trading-dashboard.plist` | **noch Platzhalter** — siehe [Die Dashboard-Vorlage befuellen](#die-dashboard-vorlage-befuellen) |

Die Flag-Wahl von `caffeinate` und der Schlaf-Vorfall vom 11.09.2026
stehen ausfuehrlich in [`README_CAFFEINATE.md`](README_CAFFEINATE.md);
hier steht nur, was fuer alle drei gilt.

> **Das Repo enthaelt Vorlagen, keine aktiven Dienste.** Nichts unter
> `~/Library/LaunchAgents/` wird von einer Claude-Sitzung angefasst. Das
> Kopieren dorthin fuehrt der Nutzer selbst aus.

---

## Warum die Vorlagen ueberhaupt im Repo liegen

Ein LaunchAgent ist eine einzelne Datei unter `~/Library/LaunchAgents/`.
Geht sie verloren — Systemwechsel, Neuinstallation, versehentliches
Loeschen —, muss sie aus dem Gedaechtnis neu geschrieben werden. Genau das
ist bei `caffeinate` am 11.09.2026 passiert: nach einem macOS-Update war
der von Hand gestartete Prozess ersatzlos weg, der Mac schlief gut drei
Stunden, und in dieser Zeit fielen Cronjobs aus. **Cron holt verpasste
Laeufe nicht nach** (siehe [`docs/DATENLUECKEN.md`](../docs/DATENLUECKEN.md)).

Die Vorlage im Repo ist die Versicherung dagegen. `python3
system/test_dienst_plists.py` prueft sie auf jedem Rechner, auch ohne
macOS.

---

## Installation (je Dienst, einmalig)

```
cp system/com.manisch.caffeinate.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.manisch.caffeinate.plist
```

Fuer die beiden anderen genauso, nur mit dem jeweiligen Dateinamen:

```
cp system/com.manisch.telegram-tradesignal-bot.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.manisch.telegram-tradesignal-bot.plist
```

**Vorher pruefen** (die Vorlagen enthalten absolute Pfade eines bestimmten
Mac):

1. Der Projektpfad in der Vorlage stimmt mit dem tatsaechlichen Ort
   ueberein (`pwd` im Projektordner).
2. Der Pfad zum `python3` stimmt (`which python3` bzw. der Pfad der
   virtuellen Umgebung).
3. **Der Log-Ordner existiert** — sonst startet der Dienst nicht:
   ```
   mkdir -p ~/trading-bot/logs/system ~/trading-bot/logs/notifications
   ```

---

## Pruefen: laeuft alles?

```
launchctl list | grep manisch
```

Erwartete Ausgabe — drei Zeilen, drei Spalten:

```
1234    0       com.manisch.caffeinate
5678    0       com.manisch.telegram-tradesignal-bot
9012    -15     com.manisch.trading-dashboard
```

| Spalte | Bedeutung |
|---|---|
| 1 — PID | Prozess-ID. Eine Zahl heisst: laeuft gerade. Ein `-` heisst: laeuft nicht. |
| 2 — Status | Exit-Status des **letzten beendeten** Laufs. |
| 3 — Label | der Dienstname. |

### Die mittlere Spalte richtig lesen — hier wird am haeufigsten falsch geschlossen

Eine **negative Zahl** in der mittleren Spalte ist **kein Fehler**. Sie ist
der Exit-Status des **Vorgaengerprozesses**, und negativ heisst: er wurde
durch ein Signal beendet, nicht durch einen eigenen Fehler-Exit.

- **`-15`** = Signal 15 (`SIGTERM`). Also genau das, was ein
  `launchctl kickstart -k` tut: es beendet den alten Prozess mit
  Signal 15 und startet einen neuen. Nach jedem Neustart steht dort
  deshalb `-15` — der Dienst laeuft trotzdem, erkennbar an der PID in der
  ersten Spalte.
- **`-9`** = Signal 9 (`SIGKILL`), hart abgeschossen.
- **`0`** = der Vorgaenger endete regulaer.
- **Positive Zahlen** (z.B. `1`, `2`) sind echte Fehler-Exits — dann ins
  Log sehen.

**Die eigentliche Frage ist immer die erste Spalte:** steht dort eine PID,
laeuft der Dienst. Steht dort ein `-`, laeuft er nicht.

---

## Neustarten

```
launchctl kickstart -k gui/$(id -u)/com.manisch.trading-dashboard
```

`-k` beendet den laufenden Prozess (Signal 15) und startet ihn neu.
`gui/$(id -u)` ist die Sitzung des angemeldeten Nutzers — `id -u` liefert
die eigene Benutzer-ID, sie muss nicht von Hand eingesetzt werden.

Fuer die anderen beiden Dienste dasselbe mit ihrem Label:

```
launchctl kickstart -k gui/$(id -u)/com.manisch.telegram-tradesignal-bot
launchctl kickstart -k gui/$(id -u)/com.manisch.caffeinate
```

### Wann ein Neustart noetig ist

| Aenderung | Neustart noetig? |
|---|---|
| `git pull`, der `dashboard/` anfasst | **ja**, Dashboard neu starten |
| `git pull`, der `notifications/` anfasst | **ja**, Telegram-Bot neu starten |
| Aenderung an der `.env` (Token, Bindung) | **ja**, betroffenen Dienst neu starten |
| reine Dokumentations-Aenderungen (`docs/`, `*.md`) | nein |
| Aenderungen unter `research/` | nein |
| Aenderungen an `strategies/` (laufen per Cron) | nein |

Der Grund: beide Python-Dienste laden ihren Code **einmal beim Start**.
Ein `git pull` aendert die Dateien auf der Platte, nicht den laufenden
Prozess — das Dashboard liefert danach weiter die alte Fassung aus, ohne
dass irgendetwas darauf hinweist.

---

## Entfernen

```
launchctl unload ~/Library/LaunchAgents/com.manisch.caffeinate.plist
rm ~/Library/LaunchAgents/com.manisch.caffeinate.plist
```

Ohne das `rm` kommt der Dienst bei der naechsten Anmeldung wieder.

---

## Das Dashboard erreichen — zwei wiederkehrende Fehlschluesse

### 1. Es lauscht nicht auf `localhost`

Der Dienst lauscht auf **`100.106.38.8:8787`** — der Tailscale-Adresse des
Mac, nicht auf `127.0.0.1`. Ein `curl http://localhost:8787/` laeuft
deshalb ins Leere, obwohl der Dienst einwandfrei laeuft.

Das ist kein Zufall, sondern muss ausdruecklich gesetzt werden: die
Grundeinstellung im Code ist `STANDARD_HOST = "127.0.0.1"` (siehe
`dashboard/konfig.py`). Die Adresse kommt entweder aus `DASHBOARD_HOST` in
der Vorlage (`EnvironmentVariables`) oder aus der `.env` im Projekt-Root.

Richtig ist:

```
curl -I http://100.106.38.8:8787/
```

### 2. `303` ist die richtige Antwort, kein Fehler

Ein Aufruf **ohne gueltiges Token** wird mit **`303 See Other`** auf
`/login` umgeleitet (`dashboard/app.py`). Das ist das gewuenschte
Verhalten — das Dashboard startet grundsaetzlich nicht ohne
Zugriffsschutz (`fail closed`, siehe `dashboard/konfig.py`).

```
HTTP/1.1 303 See Other
location: /login
```

**Eine `303` beweist also, dass der Dienst laeuft und richtig arbeitet.**
Erst *keine* Antwort (Verbindung abgelehnt, Zeitueberschreitung) ist ein
Hinweis auf ein Problem.

---

## Alle drei starten erst nach der grafischen Anmeldung

LaunchAgents laufen in der Sitzung des angemeldeten Nutzers. **Nach einem
Neustart des Mac muss sich jemand anmelden**, sonst laeuft keiner der drei
Dienste — kein Dashboard, kein Telegram-Bot, und `caffeinate` haelt den
Mac nicht wach, also laufen auch die Cronjobs nicht.

Ein `LaunchDaemon` unter `/Library/LaunchDaemons` wuerde schon beim
Systemstart greifen, braucht aber `sudo`, Eigentuemer `root` und andere
Rechte. Das ist **bewusst nicht umgesetzt** und nur als Option erwaehnt
(siehe [`README_CAFFEINATE.md`](README_CAFFEINATE.md), Abschnitt
„Grenzen").

Praktische Folge: ein unbeaufsichtigter Neustart (etwa durch ein
macOS-Update ueber Nacht) haelt alle drei Dienste an, bis sich jemand
anmeldet. Das ist dieselbe Klasse von stillem Ausfall wie der Schlaf —
und gehoert bei der naechsten Auswertung nach
[`docs/DATENLUECKEN.md`](../docs/DATENLUECKEN.md).

---

## Die Dashboard-Vorlage befuellen

Die Vorlage `system/com.manisch.trading-dashboard.plist` ist **noch ein
Platzhalter**. Ihre laufende Fassung liegt nur unter
`~/Library/LaunchAgents/` auf dem Mac; sie war nie im Repo, und eine
Cloud-Sitzung hat keinen Zugriff darauf.

Die offenen Werte sind deshalb mit `PLATZHALTER__` markiert und
**ausdruecklich nicht geraten**: eine erfundene Fassung wuerde launchd
klaglos annehmen, und der Dienst liefe danach anders als bisher, ohne dass
es jemand bemerkt. Was belegt, was erschlossen und was offen ist, steht im
Kommentarkopf der Vorlage.

### Schritt 1 — aus der laufenden Fassung uebernehmen

```
cp ~/Library/LaunchAgents/com.manisch.trading-dashboard.plist system/
```

### Schritt 2 — gegenpruefen

```
python3 system/test_dienst_plists.py
```

Der Test kennt **drei** Ergebnisse und meldet einen Platzhalter
ausdruecklich, statt ihn gruen durchzuwinken:

| Rueckgabewert | Bedeutung |
|---|---|
| `0` | alles geprueft und in Ordnung — das Ziel nach Schritt 1 |
| `1` | mindestens eine Pruefung ist fehlgeschlagen |
| `2` | keine Fehler, aber offene Platzhalter — der heutige Zustand |

### Schritt 3 — von Hand nachsehen

Nach dem Kopieren stimmen **Label und Pfade** — der Test prueft, dass das
Label `com.manisch.trading-dashboard` lautet, dass der Einstiegspunkt
`dashboard/server.py` ist und dass diese Datei im Repo wirklich existiert.
Zwei Dinge sieht sich der Nutzer trotzdem selbst an:

1. **Zeigt die Datei auf `dashboard/server.py`?** `server.py` holt
   `erzeuge_app()` aus `app.py` und startet uvicorn — `app.py` allein
   startet keinen Server und waere der falsche Einstiegspunkt.
2. **Woher kommt `DASHBOARD_HOST`?** Steht die Adresse in der Vorlage
   (`EnvironmentVariables`) oder in der `.env`? Beides funktioniert; nur
   sollte man wissen, welches von beidem gilt, wenn die Bindung sich
   einmal aendern soll.

Der vollstaendige Ablauf mit Gegenproben steht in
[`TESTAUFTRAG_DIENSTE.md`](TESTAUFTRAG_DIENSTE.md).

---

## Logs

| Dienst | Logs |
|---|---|
| `caffeinate` | `logs/system/caffeinate.log`, `caffeinate.err.log` |
| Telegram-Bot | `logs/notifications/launchd.out.log`, `launchd.err.log` |
| Dashboard | steht in der laufenden Fassung (in der Vorlage noch offen) |

Alle drei halten ihre Logdatei **dauerhaft offen**. Wer sie rotiert, darf
sie deshalb **nicht umbenennen**, sondern muss kopieren und leeren —
`system/log_rotation.py` tut genau das, Begruendung in
[`README_LOG_ROTATION.md`](README_LOG_ROTATION.md).

---

## Test

```
python3 system/test_dienst_plists.py     # alle drei Vorlagen
python3 system/test_caffeinate_plist.py  # zusaetzlich die caffeinate-Flags
```

Beide pruefen **Dateien, keine laufenden Dienste**, und laufen auf jedem
Rechner — auch ohne macOS.

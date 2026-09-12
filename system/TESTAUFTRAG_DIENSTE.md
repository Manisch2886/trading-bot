# Testauftrag launchd-Dienste — zur autonomen Ausfuehrung durch eine Claude-Code-Sitzung

**Sitzungstitel:** `TB-15 Test Dienst-Vorlagen`
**Repo:** `Manisch2886/trading-bot`, Branch `main` (nach dem Merge von TB-15)
**Voraussetzung:** Die Sitzung laeuft **auf dem Mac des Nutzers**. Nur dort
gibt es `~/Library/LaunchAgents/` und `launchctl`; eine Cloud-Sitzung kann
die Phasen 4 bis 7 nicht ausfuehren.

---

## 0. Auftrag und Grundregeln

Pruefe die drei launchd-Dienst-Vorlagen unter `system/`, **befuelle die
Dashboard-Vorlage aus der laufenden Fassung** und weise nach, dass die
uebernommene Datei zu dem passt, was tatsaechlich laeuft.

### Harte Grenzen — diese gelten ausnahmslos

| Verboten | Warum |
|---|---|
| Eine der drei Dateien unter `~/Library/LaunchAgents/` **aendern, loeschen oder ueberschreiben** | Sie sind der Produktivstand. Gelesen und kopiert wird nur **von dort ins Repo**, nie umgekehrt |
| Einen der drei Dienste **entladen** (`launchctl unload`) | Dashboard und Telegram-Bot laufen produktiv; `caffeinate` haelt den Mac wach, und ohne ihn fallen Cronjobs aus |
| Die Werte in einer Vorlage **erraten**, um den Test gruen zu bekommen | Genau das soll die Platzhalter-Markierung verhindern. Ein gruener Test ueber erfundenen Werten ist schlimmer als ein roter |
| `live_params.py`, `forward_test.py`, `equity_simulation.py` anfassen | Handelsparameter und Bot-Logik gehoeren nicht zu diesem Auftrag |
| `dashboard/app.py` oder `dashboard/server.py` **aendern** | Sie werden **gelesen**, um den Einstiegspunkt zu belegen |
| Crontab, `broker/`, `strategies/` anfassen | Ausserhalb des Auftrags |
| `--echt` bei irgendeiner Broker-Bruecke | Sendet echte Orders. Nie ohne ausdrueckliche Zustimmung |

### Ausgabeformat waehrend der Arbeit

Je Phase eine Zeile pro Schritt:

```
[PHASE 2] python3 system/test_dienst_plists.py -> Rueckgabewert 2, 0 Fehler, 4 offen
```

Am Ende der Bericht aus Phase 8.

---

## Phase 1 — Bestandsaufnahme im Repo

```
ls -la system/*.plist
git log --oneline -3
```

**Erwartet:** drei `.plist`-Dateien unter `system/`:
`com.manisch.caffeinate.plist`,
`com.manisch.telegram-tradesignal-bot.plist`,
`com.manisch.trading-dashboard.plist`.

Halte fest, welche davon noch Platzhalter enthaelt:

```
grep -l "PLATZHALTER__" system/*.plist
```

**Erwartet vor dem Befuellen:** nur `com.manisch.trading-dashboard.plist`.

---

## Phase 2 — Automatisierte Selbsttests (Ausgangsstand)

```
python3 system/test_dienst_plists.py ; echo "Rueckgabewert: $?"
python3 system/test_caffeinate_plist.py ; echo "Rueckgabewert: $?"
python3 system/test_log_rotation.py ; echo "Rueckgabewert: $?"
```

**Erwartet vor dem Befuellen:**

| Test | Ergebnis |
|---|---|
| `test_dienst_plists.py` | **Rueckgabewert 2** — 0 Fehler, 4 offen (Platzhalter) |
| `test_caffeinate_plist.py` | Rueckgabewert 0 — alle Pruefungen bestanden |
| `test_log_rotation.py` | Rueckgabewert 0 — alle Pruefungen bestanden |

> Die `2` ist **kein Fehler**, sondern der dokumentierte Ausgangszustand:
> die Dashboard-Vorlage ist noch nicht befuellt. Wird daraus eine `0`,
> ohne dass Phase 5 gelaufen ist, hat jemand die Werte erraten — dann
> abbrechen und melden.

---

## Phase 3 — Nichts angefasst, was nicht angefasst werden durfte

```
git status --short
git diff --stat
```

**Erwartet:** keine Aenderungen ausser denen, die dieser Auftrag vorsieht.
Insbesondere **keine** Aenderung an `dashboard/app.py`,
`dashboard/server.py`, `live_params.py`, `strategies/`, `broker/`.

---

## Phase 4 — Ist-Zustand der Dienste auf dem Mac

```
launchctl list | grep manisch
ls -la ~/Library/LaunchAgents/ | grep manisch
```

**Erwartet:** drei Zeilen bzw. drei Dateien.

Notiere je Dienst PID und Status-Spalte. Zur Erinnerung (siehe
`README_DIENSTE.md`):

- **Erste Spalte** ist die entscheidende: eine PID heisst „laeuft", ein
  `-` heisst „laeuft nicht".
- Eine **negative Zahl** in der mittleren Spalte ist der Exit-Status des
  **Vorgaengers**, kein Fehler. `-15` = durch Signal 15 beendet, also
  genau das, was ein `kickstart -k` tut.

Erreichbarkeit des Dashboards:

```
curl -s -o /dev/null -w "%{http_code}\n" http://100.106.38.8:8787/
```

**Erwartet: `303`.** Das ist die *richtige* Antwort — ohne gueltiges Token
leitet der Server auf `/login` um. Eine `303` beweist, dass der Dienst
laeuft. Ein `000` (keine Verbindung) waere das Problem.

Gegenprobe, damit der haeufigste Fehlschluss dokumentiert ist:

```
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8787/
```

**Erwartet: `000`** oder „Connection refused" — der Dienst lauscht
**nicht** auf localhost. Auch das ist kein Fehler.

---

## Phase 5 — Die Dashboard-Vorlage aus der laufenden Fassung befuellen

Das ist der Kern dieses Auftrags. **Kopierrichtung beachten:** aus
`~/Library/LaunchAgents/` **ins Repo**, nie umgekehrt.

### 5a — vorher ansehen, nicht blind kopieren

```
plutil -lint ~/Library/LaunchAgents/com.manisch.trading-dashboard.plist
cat ~/Library/LaunchAgents/com.manisch.trading-dashboard.plist
```

**Erwartet:** `OK` von `plutil`. Halte fest, welche Werte dort stehen fuer
`Label`, `ProgramArguments`, `WorkingDirectory`, `RunAtLoad`, `KeepAlive`,
`StandardOutPath`, `StandardErrorPath` und — falls vorhanden —
`EnvironmentVariables`.

### 5b — kopieren

```
cp ~/Library/LaunchAgents/com.manisch.trading-dashboard.plist system/
```

### 5c — gegenpruefen

```
python3 system/test_dienst_plists.py ; echo "Rueckgabewert: $?"
```

**Erwartet jetzt: Rueckgabewert 0**, 0 Fehler, 0 offen.

Schlaegt stattdessen etwas fehl, ist das ein **echter Befund** und nicht
durch Anpassen der Vorlage zu „reparieren". Die drei wahrscheinlichsten:

| Meldung | Bedeutung |
|---|---|
| `Label ist com.manisch.trading-dashboard` fehlgeschlagen | Die laufende Fassung benutzt ein anderes Label als angenommen — melden |
| `Einstiegspunkt aus der Vorlage existiert im Repo` fehlgeschlagen | Der Dienst startet eine Datei, die es im Repo nicht (mehr) gibt — der wichtigste moegliche Befund, sofort melden |
| `Alle drei Vorlagen nehmen denselben Projektpfad an` fehlgeschlagen | Der Dashboard-Dienst laeuft aus einem anderen Ordner als die anderen beiden — melden |

### 5d — die drei Fragen aus Phase 5a beantworten

1. **Zeigt die laufende Fassung auf `dashboard/server.py`?**
   Falls sie auf `app.py` oder auf `uvicorn` mit `app:erzeuge_app` zeigt:
   festhalten und melden, **nicht** aendern. `server.py` holt
   `erzeuge_app()` aus `app.py` und startet uvicorn; nachpruefbar mit
   ```
   grep -n "from app import" dashboard/server.py
   grep -n "uvicorn.run" dashboard/server.py
   ```
2. **Woher kommt `DASHBOARD_HOST=100.106.38.8`?** Aus der Vorlage oder aus
   der `.env`?
   ```
   grep -c DASHBOARD_HOST ~/Library/LaunchAgents/com.manisch.trading-dashboard.plist
   grep -c DASHBOARD_HOST .env
   ```
   (`grep -c`, nicht `cat` — die `.env` enthaelt Zugangsdaten.)
   Beide Wege sind zulaessig; festhalten, welcher gilt.
3. **Wohin schreibt der Dienst seine Logs?** Die Pfade aus der
   uebernommenen Datei in `README_DIENSTE.md`, Abschnitt „Logs",
   nachtragen — dort steht bisher „in der Vorlage noch offen".

---

## Phase 6 — Neustart-Ablauf pruefen (nur Dashboard)

Erst **nach** Phase 5 und nur mit Zustimmung des Nutzers, weil das
Dashboard dabei kurz nicht erreichbar ist.

```
launchctl list | grep trading-dashboard
launchctl kickstart -k gui/$(id -u)/com.manisch.trading-dashboard
launchctl list | grep trading-dashboard
curl -s -o /dev/null -w "%{http_code}\n" http://100.106.38.8:8787/
```

**Erwartet:**

- Vor dem `kickstart`: eine PID.
- Nach dem `kickstart`: eine **andere** PID und in der mittleren Spalte
  `-15`.
- Die `-15` ist **der Beleg dafuer, dass es funktioniert hat**, kein
  Fehler: `kickstart -k` beendet den Vorgaenger mit Signal 15.
- `curl` liefert wieder `303`.

Kommt nach dem Neustart **keine** PID zurueck, im Log nachsehen (Pfade aus
Phase 5d) und melden.

---

## Phase 7 — Gegenprobe: erkennt der Test einen kaputten Stand ueberhaupt?

Ein Test, der immer gruen ist, sagt nichts. Diese Phase weist nach, dass
er anschlaegt — **ohne** eine Datei im Repo zu beschaedigen.

```
python3 system/test_dienst_plists.py 2>&1 | sed -n '/Mutationsproben/,$p'
```

**Erwartet:** Der Abschnitt „7) Mutationsproben" besteht vollstaendig. Die
Proben verbiegen eine Kopie der Telegram-Vorlage in einem temporaeren
Ordner und pruefen, dass **genau** die erwarteten Wachen anschlagen —
darunter die Platzhalter-Meldung, der falsche Boolean `<string>true</string>`
statt `<true/>` und ein Einstiegspunkt, den es im Repo nicht gibt.

Zusaetzliche Handprobe (veraendert nichts Dauerhaftes):

```
cp system/com.manisch.trading-dashboard.plist /tmp/probe.plist
sed -i '' 's|<true/>|<string>true</string>|' system/com.manisch.trading-dashboard.plist
python3 system/test_dienst_plists.py ; echo "Rueckgabewert: $?"
cp /tmp/probe.plist system/com.manisch.trading-dashboard.plist
python3 system/test_dienst_plists.py ; echo "Rueckgabewert: $?"
```

**Erwartet:** in der Mitte **Rueckgabewert 1** mit den fehlgeschlagenen
Pruefungen `RunAtLoad ist der Boolean true` und `KeepAlive ist der Boolean
true`; danach wieder **Rueckgabewert 0**. Pruefe mit `git status --short`,
dass die Datei am Ende unveraendert ist.

---

## Phase 8 — Abschlussbericht

Erzeuge diesen Bericht und haenge ihn als Datei an:

```markdown
# Testbericht launchd-Dienste

**Datum:** …
**Rechner:** … (macOS-Version)
**Repo-Stand:** … (git log --oneline -1)

## Ergebnis je Phase

| Phase | Ergebnis | Bemerkung |
|---|---|---|
| 1 Bestandsaufnahme | … | … |
| 2 Selbsttests (vorher) | … | Rueckgabewert erwartet: 2 |
| 3 Nichts angefasst | … | … |
| 4 Ist-Zustand | … | … |
| 5 Vorlage befuellt | … | Rueckgabewert erwartet: 0 |
| 6 Neustart | … | … |
| 7 Gegenprobe | … | … |

## Die uebernommene Dashboard-Vorlage

| Schluessel | Wert aus der laufenden Fassung | wich von der Platzhalter-Vorlage ab? |
|---|---|---|
| Label | … | … |
| ProgramArguments[0] (python3) | … | war Platzhalter |
| ProgramArguments[1] (Skript) | … | … |
| WorkingDirectory | … | … |
| RunAtLoad / KeepAlive | … | … |
| StandardOutPath | … | war Platzhalter |
| StandardErrorPath | … | war Platzhalter |
| EnvironmentVariables | … | … |

**Kam DASHBOARD_HOST aus der Vorlage oder aus der .env?** …

## Messwerte

- `curl http://100.106.38.8:8787/` → … (erwartet 303)
- `curl http://localhost:8787/` → … (erwartet keine Verbindung)
- PID vor / nach dem Neustart: … / …
- Status-Spalte nach dem Neustart: … (erwartet -15)

## Befunde

…

## Was NICHT geprueft wurde

…

## Empfehlung

…
```

---

## Hinweis zu `dashboard/test_dashboard.py`

Ohne `node` ueberspringt dieser Test vier Pruefungen und meldet **780/780
statt 784**. Das sieht gruen aus, ist aber unvollstaendig — auf dem
Rechner des Nutzers ist `node` derzeit nicht installiert. Wer die Zahl im
Bericht nennt, sollte sie so nennen: „780/780, vier Pruefungen mangels
`node` uebersprungen".

# Testauftrag TB-32 — Wächter melden

**Stand: 2026-09-14.** Dieses Dokument ist **eigenständig ausführbar**: alles
Nötige steht hier, es ist kein anderes Dokument zu lesen. Ergebnisbericht:
`docs/ERGEBNIS_TB-32_waechter_melden.md`.

**Was geprüft wird:** dass `notifications/waechter_melden.py` bei einem Befund
meldet, bei Rückgabewert `0` **schweigt**, einen Absturz **unterscheidbar**
meldet — und dass nichts davon den Wächter selbst beeinträchtigen kann.

**Voraussetzungen:** Python 3.9+. Die Selbsttests brauchen **weder `pandas`
noch `numpy` noch Netz**. Alle Befehle werden **aus dem
Projektwurzelverzeichnis** gestartet. Nichts davon sendet eine Order, schreibt
in eine Bot-Datenbank, verändert `results/` oder ändert die Crontab.

> **Ein Schritt verschickt wirklich eine Telegram-Nachricht** — Schritt 6, und
> er ist ausdrücklich als solcher gekennzeichnet. Alle übrigen Schritte
> benutzen eine Attrappe oder `--trockenlauf`.

---

## 0. Vorbereitung — der Basislauf auf unverändertem `main`

Mehrere Prüfungen dieses Repos schlagen **vorbestehend** fehl. Ohne einen
Basislauf ist hinterher nicht zu unterscheiden, was TB-32 verursacht hat und
was schon vorher so war.

```bash
git stash push -u                          # die TB-32-Aenderungen beiseitelegen
python3 notifications/test_schliess_benachrichtigung.py | tail -3; echo "RC=$?"
python3 dashboard/test_dashboard.py        | tail -3; echo "RC=$?"
python3 system/test_log_rotation.py        | tail -3; echo "RC=$?"
git stash pop                              # zurueckholen
```

**Erwartet auf dem Rechner des Nutzers:** alle drei bestehen; `test_dashboard.py`
meldet **780/780 statt 784**, weil `node` dort bewusst nicht installiert ist.

**Erwartet in einer Cloud-Umgebung ohne Bot-Abhängigkeiten:** die ersten beiden
brechen mit `ModuleNotFoundError: No module named 'pandas'` ab. Das ist
vorbestehend und hat mit TB-32 nichts zu tun — TB-32 fasst keine dieser Dateien
an.

---

## 1. Die Hauptzusicherung: die Selbsttests

```bash
python3 notifications/test_waechter_melden.py; echo "RC=$?"
```

**Erwartet:** `149 von 149 Pruefungen bestanden, 0 fehlgeschlagen.`, `RC=0`.
Laufzeit rund zwei bis drei Minuten (die Mutationsproben starten die Testdatei
neunmal erneut).

Die Abschnitte im Einzelnen — jeder misst **genau eine** Regel:

| Abschnitt | Zusicherung |
|---|---|
| 1 | Rückgabewert 1 → **eine** Nachricht, Klartext-Name, Befund, Nachsehen-Befehl |
| 2 | Rückgabewert 0 → **keine** Nachricht, auch nach zehn Läufen nicht |
| 2b | Befund → 0: keine „behoben"-Meldung, Vermerk geräumt, ein späterer Befund gilt wieder als neu |
| 3 | Rückgabewert 2 / 127 / Ausnahme / nicht startbar / Signal → `[ABGESTUERZT]`, nie derselbe Text wie ein Befund |
| 4 | Kaputter Sendeweg → Wächter läuft durch, eigener Rückgabewert, Ausgabe im Log |
| 4b | Die Ausgabe steht im Log, **bevor** der Meldeteil beginnt |
| 5 | Dämpfung: Tag 0 meldet, Tag 1–6 still, Tag 7 erinnert; geänderter Befund geht sofort durch |
| 5b | Wechselnde Laufzeiten heben die Dämpfung **nicht** auf |
| 5c | Was nicht ankam, gilt nicht als gemeldet → Nachholung am nächsten Tag |
| 6 | Höchstens zwei Ausgabezeilen, Kürzung sichtbar, fehlende Marke wird benannt |
| 6b | Dieselbe Sache zweimal wird entdoppelt |
| 7 | `--trockenlauf` sendet nichts, vermerkt nichts, zeigt dieselbe Entscheidung |
| 8 | `--zeitlimit`: hängender Wächter → Absturz, Rückgabewert 124 |
| 9 | Die vier Dämpfungsregeln einzeln, inklusive der Grenze bei genau 7 Tagen |
| 10 | Kein Wächter importiert, kein zweiter Sendeweg, `notify.py` unverändert |
| 10b | Jede der fünf Cron-Zeilen steht im README |
| 11 | **Mutationsproben** — siehe Schritt 2 |

---

## 2. Die Mutationsproben: schlagen die Tests überhaupt an?

Abschnitt 11 baut neun kaputte Fassungen des Wrappers und lässt die Testdatei
gegen jede laufen. Erwartet wird **genau**, welche Abschnitte dabei
fehlschlagen — nicht mehr und nicht weniger. „Nicht mehr" ist der schärfere
Teil: er belegt, dass die Abschnitte unabhängig voneinander messen.

```bash
python3 notifications/test_waechter_melden.py 2>&1 | sed -n '/Mutationsproben/,$p'
```

**Erwartet:** neun Zeilen `[OK ] Mutante '…': genau die erwarteten Abschnitte
schlagen an   fehlt: -; zuviel: -`.

| Mutante | schlägt an in |
|---|---|
| die Null-Regel fällt weg (jeder Lauf meldet) | 2, 2b, 7, 9 |
| die Dämpfung fällt weg (täglich dieselbe Meldung) | 5, 5b, 5c, 9 |
| die wöchentliche Erinnerung fällt weg | 5, 9 |
| ein fehlgeschlagener Versand gilt als zugestellt | 4, 5, 5c |
| ein Absturz wird wie ein Befund gemeldet | 3, 8 |
| eine Traceback mit Rückgabewert 1 gilt als Befund | 3 |
| erst melden, dann das Log schreiben | 4, 4b |
| ein Sendefehler wird weitergereicht | 4 |
| der Fingerabdruck läuft über die ganze Ausgabe | 5b |

> **Warum das hier steht.** Zwei Fallen sind in diesem Repo wiederholt
> aufgetreten (#73, #77–#79, #81, #86, TB-15, TB-20, TB-22, TB-26, TB-30a):
> eine Probe, deren Zustand der Test von Hand herstellt, bestätigt sich selbst;
> und eine zweite Wache verdeckt das Fehlen der ersten. Gegen die erste
> schreibt **kein** Test hier eine Zustandsdatei — jeder Zustand entsteht durch
> einen vorherigen echten Lauf. Gegen die zweite ist jeder Prüffall so gewählt,
> dass nur die geprüfte Zusicherung greifen kann.
>
> Die Proben haben dabei einen echten Fehler **im Wrapper** gefunden: die Regel
> „0 heisst schweigen" stand anfangs an zwei Stellen. Eine davon zu entfernen
> änderte nichts — genau Falle 2, im eigenen Code. Sie steht jetzt einmal.

---

## 3. Die drei Ausgänge von Hand nachstellen

Ohne Telegram, ohne die echten Wächter. Der Befehl baut sich eine Attrappe und
ruft den Wrapper dreimal.

```bash
cat > /tmp/tb32_probe.py <<'PY'
import os, sys
sys.stdout.write(os.environ.get("AUS", ""))
sys.stderr.write(os.environ.get("ERR", ""))
sys.exit(int(os.environ.get("RC", "0")))
PY

python3 - <<'PY'
import datetime, os, sys
sys.path.insert(0, "notifications")
import waechter_melden as wm

w = wm.Waechter("probe", "Probe-Waechter", ("/tmp/tb32_probe.py",),
                "logs/system/probe.log", ("BEFUND",), "-")
texte = []
senden = lambda t: (texte.append(t), True)[1]
zustand = "/tmp/tb32_zustand.json"
if os.path.exists(zustand):
    os.remove(zustand)

for titel, umgebung in [
        ("Rueckgabewert 0", {"RC": "0", "AUS": "Alles in Ordnung.\n"}),
        ("Rueckgabewert 1", {"RC": "1", "AUS": "BEFUND: 3 von 9 Kurven passen nicht.\n"}),
        ("Rueckgabewert 2", {"RC": "2", "ERR": "--perms muss mindestens 2 sein.\n"})]:
    os.environ.update({"RC": "0", "AUS": "", "ERR": ""})
    os.environ.update(umgebung)
    vorher = len(texte)
    rc = wm.lauf(w, senden=senden, zustand_pfad=zustand,
                 jetzt=datetime.datetime(2026, 9, 14, 3, 50))
    print(f"\n=== {titel}: rc={rc}, Nachrichten={len(texte) - vorher} ===")
    if len(texte) > vorher:
        print(texte[-1])
PY
```

**Erwartet — wörtlich:**

```
Alles in Ordnung.

=== Rueckgabewert 0: rc=0, Nachrichten=0 ===
BEFUND: 3 von 9 Kurven passen nicht.

=== Rueckgabewert 1: rc=1, Nachrichten=1 ===
[BEFUND] Probe-Waechter - neu
BEFUND: 3 von 9 Kurven passen nicht.
Nachsehen: tail -n 60 ~/trading-bot/logs/system/probe.log
--perms muss mindestens 2 sein.

=== Rueckgabewert 2: rc=2, Nachrichten=1 ===
[ABGESTUERZT] Probe-Waechter - geaendert gegenueber der letzten Meldung
Rueckgabewert 2 - weder 0 (in Ordnung) noch 1 (Befund). Das Werkzeug selbst ist gescheitert, es liegt KEIN Befund vor.
--perms muss mindestens 2 sein.
Nachsehen: tail -n 60 ~/trading-bot/logs/system/probe.log
```

**Worauf zu achten ist:**

1. Bei `0` steht die Ausgabe des Wächters im Log und **keine** Nachricht geht
   raus.
2. Der Rückgabewert des Wrappers ist jedes Mal der des Wächters.
3. Die Absturz-Nachricht trägt `[ABGESTUERZT]` und sagt **KEIN Befund** — sie
   ist nicht dieselbe wie bei einem Befund.
4. Der dritte Lauf heisst `geaendert`, nicht `neu`: der Wechsel Befund →
   Absturz fällt unter Regel 2 und wird deshalb gemeldet, obwohl er am selben
   Tag passiert.

Aufräumen: `rm -f /tmp/tb32_probe.py /tmp/tb32_zustand.json`

---

## 4. Die echten fünf Wächter im Trockenlauf

`--trockenlauf` führt den Wächter **wirklich** aus, zeigt die Nachricht, die
entstehen würde — und verschickt nichts und vermerkt nichts.

```bash
mkdir -p logs/system
for w in log_rotation ergebniskurven determinismus versuchsregister kapitalsimulation; do
  echo "########## $w"
  python3 notifications/waechter_melden.py "$w" --trockenlauf --zustand /tmp/tb32_trocken.json
  echo "RC=$?"
done
rm -f /tmp/tb32_trocken.json
```

**Erwartet auf dem Rechner des Nutzers:** jeder Block endet mit
`Entscheidung: SCHWEIGEN (still)` und `RC=0`, **solange kein Wächter etwas
findet**. Findet einer etwas, steht dort `Entscheidung: MELDEN (neu)` und
darunter die Nachricht — das ist dann kein Fehler dieses Testauftrags, sondern
der Befund selbst, und er gehört nachgegangen.

> ⚠️ **Der eigentliche Zweck dieses Schritts.** Welche ein bis zwei Zeilen in
> die Nachricht wandern, entscheidet je Wächter eine Liste von Marken in
> `waechter_melden.py` (`WAECHTER`). Diese Listen sind gegen die Ausgabe der
> Wächter geschrieben, aber die Befund-Ausgabe von `ergebniskurven.py` und
> `determinismus.py` liess sich in der Cloud nicht erzeugen (dort fehlt
> `pandas`). **Wenn hier ein Wächter meldet, bitte hinsehen:** steht in der
> Nachricht die Befundzeile — oder steht dort
> `(keine bekannte Befundzeile erkannt - letzte Ausgabezeilen:)`? Im zweiten
> Fall gehört die Markenliste des betreffenden Wächters nachgezogen. Der
> Wrapper sagt das ausdrücklich; still falsch ist er nie.

**Ein Befund lässt sich auch erzwingen** — `ergebniskurven.py` schlägt an,
sobald eine abgelegte Kurve nicht mehr passt:

```bash
python3 shared/ergebniskurven.py --nur-abweichung >/dev/null 2>&1; echo "roher Waechter: RC=$?"
```

Liefert dieser Befehl `RC=1`, muss der Trockenlauf aus Schritt 4 für
`ergebniskurven` ebenfalls `MELDEN` zeigen und die Befundzeile enthalten.
Liefert er `RC=0`, zeigt der Trockenlauf `SCHWEIGEN`. **Die beiden müssen
übereinstimmen** — der Wrapper darf den Rückgabewert nicht verändern.

---

## 5. Die harte Bedingung: ein kaputter Sendeweg kostet nichts

Ohne Netz und ohne Zugangsdaten. Geprüft wird der **Ablauf**.

```bash
python3 - <<'PY'
import contextlib, datetime, io, os, sys
sys.path.insert(0, "notifications")
import waechter_melden as wm

open("/tmp/tb32_befund.py", "w").write(
    "import sys\nprint('BEFUND: etwas stimmt nicht.')\nsys.exit(1)\n")
w = wm.Waechter("probe", "Probe-Waechter", ("/tmp/tb32_befund.py",),
                "logs/system/probe.log", ("BEFUND",), "-")

def kaputt(text):
    raise ConnectionError("api.telegram.org nicht erreichbar")

aus, err = io.StringIO(), io.StringIO()
with contextlib.redirect_stdout(aus), contextlib.redirect_stderr(err):
    rc = wm.lauf(w, senden=kaputt, zustand_pfad="/tmp/tb32_z.json",
                 jetzt=datetime.datetime(2026, 9, 14, 3, 50))

print("Rueckgabewert:", rc)
print("Im Log steht:", repr(aus.getvalue()))
print("Protokolliert:", err.getvalue().strip())
os.remove("/tmp/tb32_befund.py"); os.remove("/tmp/tb32_z.json")
PY
```

**Erwartet:**

```
Rueckgabewert: 1
Im Log steht: 'BEFUND: etwas stimmt nicht.\n'
Protokolliert: [waechter_melden] Der Versand ist gescheitert (ConnectionError: api.telegram.org nicht erreichbar). Die Meldung gilt als NICHT zugestellt und wird beim naechsten Lauf erneut versucht.
```

Drei Dinge zugleich: der **Rückgabewert** ist der des Wächters, seine
**Ausgabe** ist vollständig im Log, und der Sendefehler ist **protokolliert,
nicht weitergereicht**. Im Cronjob landet die Protokollzeile in derselben
Logdatei wie alles andere (`2>&1`).

---

## 6. ⚠️ Der eine Schritt, der wirklich sendet

Nur ausführen, wenn eine Telegram-Nachricht ankommen **soll**. Er prüft, dass
Zugangsdaten und Sendeweg auf diesem Rechner stimmen.

```bash
grep -c TELEGRAM_BOT_TOKEN .env      # erwartet: 1
grep -c TELEGRAM_USER_ID  .env      # erwartet: 1

cat > /tmp/tb32_echt.py <<'PY'
import sys
print("BEFUND: Dies ist eine Probemeldung aus dem Testauftrag TB-32.")
sys.exit(1)
PY
python3 - <<'PY'
import sys
sys.path.insert(0, "notifications")
import waechter_melden as wm
w = wm.Waechter("tb32_probe", "TB-32 Probemeldung", ("/tmp/tb32_echt.py",),
                "logs/system/probe.log", ("BEFUND",), "-")
print("Rueckgabewert:", wm.lauf(w, zustand_pfad="/tmp/tb32_echt_zustand.json"))
PY
rm -f /tmp/tb32_echt.py /tmp/tb32_echt_zustand.json
```

**Erwartet:** `Rueckgabewert: 1`, und in Telegram kommt an:

```
[BEFUND] TB-32 Probemeldung - neu
BEFUND: Dies ist eine Probemeldung aus dem Testauftrag TB-32.
Nachsehen: tail -n 60 ~/trading-bot/logs/system/probe.log
```

Kommt nichts an, steht der Grund in der Fehlerausgabe (`[waechter_melden]` bzw.
eine Zeile aus `notify.py`). Der Token selbst wird nirgends ausgegeben.

**Ein zweites Mal ausführen**, ohne die Zustandsdatei zu löschen, muss
**schweigen** — das ist die Dämpfung im scharfen Betrieb. Dazu die beiden
`rm -f` weglassen und den Block erneut starten; erwartet: `Rueckgabewert: 1`
und **keine** zweite Telegram-Nachricht.

---

## 7. Die fünf Crontab-Zeilen (zum Kopieren)

**Die Crontab wurde von dieser Änderung nicht angefasst.** Die folgenden Zeilen
**ersetzen** die am 14.09.2026 eingetragenen: gleiche Zeiten, gleiche
Logdateien, gleiche Rückgabewerte — nur mit Meldung.

Vorher einmalig:

```bash
mkdir -p ~/trading-bot/logs/system
```

Dann `crontab -e` und die fünf alten Zeilen durch diese ersetzen:

```cron
30 3 * * * cd ~/trading-bot && /usr/bin/python3 notifications/waechter_melden.py log_rotation >> logs/system/log_rotation.log 2>&1
50 3 * * * cd ~/trading-bot && /usr/bin/python3 notifications/waechter_melden.py ergebniskurven >> logs/system/ergebniskurven.log 2>&1
10 4 * * * cd ~/trading-bot && /usr/bin/python3 notifications/waechter_melden.py determinismus >> logs/system/determinismus.log 2>&1
30 4 * * * cd ~/trading-bot && /usr/bin/python3 notifications/waechter_melden.py versuchsregister >> logs/system/versuchsregister.log 2>&1
40 4 * * * cd ~/trading-bot && /usr/bin/python3 notifications/waechter_melden.py kapitalsimulation >> logs/system/kapitalsimulation.log 2>&1
```

Danach prüfen:

```bash
crontab -l | grep waechter_melden | wc -l      # erwartet: 5
crontab -l | grep -c 'log_rotation.py'         # erwartet: 0 (ersetzt)
```

**Am Morgen nach dem ersten Lauf:**

```bash
python3 notifications/waechter_melden.py --status
tail -n 20 ~/trading-bot/logs/system/determinismus.log
```

`--status` zeigt je Wächter, ob etwas offensteht und wann es zuletzt gemeldet
wurde. `NIE - steht aus` bedeutet: ein Befund liegt vor, die Nachricht ist aber
nicht zugestellt worden — dann ins Log sehen.

---

## 8. Was nicht angefasst wurde

```bash
git diff --stat main
```

**Erwartet:** genau diese Dateien.

| Datei | Art |
|---|---|
| `notifications/waechter_melden.py` | neu |
| `notifications/test_waechter_melden.py` | neu |
| `notifications/README_WAECHTER_MELDEN.md` | neu |
| `docs/TESTAUFTRAG_TB-32_waechter_melden.md` | neu (dieses Dokument) |
| `docs/ERGEBNIS_TB-32_waechter_melden.md` | neu |
| `docs/UEBERGABE_TB-32_waechter_melden.md` | neu |
| `notifications/README.md` | eine Zeile in der Struktur-Tabelle |
| `docs/UEBERGABEPROTOKOLL.md` | Abschnitt 4.7, offene Punkte 22 und 23 |
| `.gitignore` | Zustandsdatei ausgenommen |

**Nicht** in der Liste stehen dürfen: `notify.py`, einer der fünf Wächter,
`live_params.py`, `forward_test.py`, `equity_simulation.py`, irgendetwas unter
`broker/` oder `results/`.

```bash
git diff main --name-only | grep -E 'notify\.py|live_params|forward_test|equity_simulation|^broker/|^results/|log_rotation\.py|ergebniskurven\.py|determinismus\.py|versuchsregister\.py|vergleich\.py'
```

**Erwartet:** keine Ausgabe.

---

## 9. Abschliessender Gesamtlauf

```bash
for t in $(find . -name "test_*.py" | sort); do
  printf '%-62s' "$t"
  python3 "$t" >/dev/null 2>&1 && echo "OK" || echo "FEHLER"
done
```

**Erwartet:** dieselben `FEHLER` wie im Basislauf aus Schritt 0 — kein
zusätzlicher. `notifications/test_waechter_melden.py` steht auf `OK`.

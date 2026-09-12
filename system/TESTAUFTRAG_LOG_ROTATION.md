# Testauftrag: Log-Rotation

**Für eine lokale Claude-Code-Sitzung auf dem Mac.** Ablegeort neben
`TESTAUFTRAG_CAFFEINATE.md`, weil das Thema dasselbe Verzeichnis betrifft.

Geprüfter Stand: Branch `claude/new-session-uqjk8h`, Basis `origin/main`
(`b4b7acd`, nach Merge von #78).

> ## Was diese Sitzung darf und was nicht
>
> **Die Schritte 0–5 und 7–8 laufen ohne Rückfragen durch.** Sie fassen die
> echten Logdateien nicht an: die Selbsttests arbeiten in Wegwerf-Ordnern unter
> `/tmp`, `--status` und `--trockenlauf` lesen nur.
>
> **Schritt 6 verändert echte Logdateien** (kopiert ihren Inhalt in ein Archiv
> und leert sie). Verloren geht dabei nichts — der Inhalt steht anschließend im
> Archiv daneben. Trotzdem: **vorher fragen**, Ergebnis der Schritte 0–5
> vorlegen, dann erst Schritt 6.
>
> **Nicht anfassen:** Crontab, launchd-Vorlagen, `broker/`, `strategies/`,
> `live_params.py`, `forward_test.py`, `equity_simulation.py`. Kein `--echt`
> irgendwo. Keine Zugangsdaten in Ausgaben oder Notizen übernehmen.

---

## Schritt 0 — Umgebung

```bash
cd ~/trading-bot
git status --short              # muss LEER sein
git rev-parse --abbrev-ref HEAD
python3 --version
```

Erwartet: keine Ausgabe bei `git status`. Python 3.9 genügt — das Skript
benutzt nur die Standardbibliothek.

---

## Schritt 1 — Selbsttests

```bash
python3 system/test_log_rotation.py | tail -3
```

Erwartet: **117 von 117 Prüfungen bestanden, 0 fehlgeschlagen.**

Der Lauf dauert rund 15 Sekunden, weil er echte Nebenläufigkeit prüft: mehrere
Abschnitte starten einen zweiten Python-Prozess, der durchgehend in eine
Logdatei schreibt, während rotiert wird.

Zwei Meldungen im Lauf sind **erwartet und kein Fehler**:

```
m/dauer.log NICHT rotiert: ... waechst schneller als die Rotation kopieren kann
```

Das ist die Schutzabschaltung bei absichtlich zähem `fsync` (Abschnitt 6c). Sie
soll dort greifen: ein Abbruch leert nichts, verliert also nichts.

---

## Schritt 2 — Was im echten `logs/` liegt (liest nur)

```bash
python3 system/log_rotation.py --status
```

Erwartet: eine Zeile je `*.log` unter `logs/`, mit Größe und Begründung.
Erwartete Begründungen:

| Datei | erwartet |
|---|---|
| `notifications/telegram_bot.log` | `rotiert selbst: RotatingFileHandler in notifications/telegram_bot.py, 2000 KB x 3 Staende` |
| `notifications/manuelle_eingriffe.log` | dieselbe Form, `manual_close.py`, `1000 KB x 5` |
| alle übrigen | `unter der Schwelle (... < 1000000 Bytes)` |

**Bitte notieren:** die größte angezeigte Datei mit ihrer Größe. Der Auftrag
nennt rund 262 KB für die größte `forward_test.log`; weicht das stark ab, ist
das ein Befund für die Rückmeldung.

Steht bei einer Datei etwas anderes als die drei Formen oben — insbesondere
`ueber der Schwelle` —, ist das ebenfalls ein Befund: dann ist im echten `logs/`
etwas deutlich schneller gewachsen als angenommen.

---

## Schritt 3 — Trockenlauf (verändert nichts)

```bash
python3 system/log_rotation.py --trockenlauf
```

Erwartet: `TROCKENLAUF - es wird nichts veraendert.` und am Ende
`0 von N Dateien waere faellig.`

Ist die Zahl **nicht** 0, Schritt 6 nicht ohne Rückfrage ausführen, sondern
melden, welche Datei fällig ist.

```bash
git status --short                     # muss noch LEER sein
ls logs/*/*.log.* 2>/dev/null | head   # nur Fremdarchive (.log.1 o.ä.), keine Zeitmarken
```

---

## Schritt 4 — Der Kernfall von Hand: offener Schreibzugriff

Das ist die eigentliche Zusicherung dieser Änderung. Vollständig in einem
Wegwerf-Ordner, **das echte `logs/` ist nicht beteiligt**.

```bash
PROBE=$(mktemp -d) && mkdir -p "$PROBE/dienst" && echo "$PROBE"

# Ein Prozess, der die Datei offen HÄLT und durchgehend schreibt -
# so wie Dashboard, Telegram-Bot und caffeinate es tun.
python3 -c '
import os, sys, time
pfad, stopp = sys.argv[1], sys.argv[2]
n = 0
with open(pfad, "a", buffering=1) as d:
    while not os.path.exists(stopp):
        n += 1
        d.write("ZEILE %08d\n" % n)
        time.sleep(0.002)
open(pfad + ".anzahl", "w").write(str(n))
' "$PROBE/dienst/dauer.log" "$PROBE/STOPP" &
SCHREIBER=$!

sleep 3
ls -li "$PROBE/dienst/"          # Inode notieren (erste Spalte)
wc -l "$PROBE/dienst/dauer.log"
```

Jetzt rotieren, **während** der Prozess weiterschreibt:

```bash
python3 system/log_rotation.py --wurzel "$PROBE" --schwelle 1000
ls -li "$PROBE/dienst/"          # Inode der .log MUSS derselbe sein
wc -c "$PROBE/dienst/dauer.log"  # klein - die Datei ist geleert
sleep 2
wc -c "$PROBE/dienst/dauer.log"  # GEWACHSEN: der Prozess schreibt in die NEUE Datei
```

**Die drei Punkte, auf die es ankommt:**

1. Der **Inode** der `.log` ist vor und nach der Rotation derselbe.
2. Die `.log` ist direkt nach der Rotation fast leer und **wächst danach
   weiter**. Bliebe sie bei 0, wäre der Fehler eingetreten, den diese Änderung
   vermeidet (der Dienst schreibt ins Archiv weiter).
3. Das **Archiv wächst nicht mehr**:

```bash
ARCHIV=$(ls "$PROBE"/dienst/dauer.log.2* | head -1)
wc -c "$ARCHIV"; sleep 2; wc -c "$ARCHIV"     # beide Male gleich
```

Vollständigkeit prüfen und aufräumen:

```bash
touch "$PROBE/STOPP"; wait $SCHREIBER
GESCHRIEBEN=$(cat "$PROBE/dienst/dauer.log.anzahl")
GEFUNDEN=$(cat "$PROBE"/dienst/dauer.log.2* "$PROBE/dienst/dauer.log" | grep -c '^ZEILE ')
echo "geschrieben: $GESCHRIEBEN   wiedergefunden: $GEFUNDEN"
head -c 64 "$PROBE/dienst/dauer.log" | od -c | head -2   # keine \0 am Anfang
rm -rf "$PROBE"
```

Erwartet: **beide Zahlen gleich.** Bei 500 Zeilen/s und einer Rotation ist ein
Verlust von 0 zu erwarten; eine einzelne fehlende Zeile wäre die im README
bezifferte Restlücke und kein Fehler — mehr als eine wäre ein Befund.

---

## Schritt 5 — Echter Lauf (heute ein Nichts-Tun)

```bash
python3 system/log_rotation.py
```

Erwartet, solange keine Datei über 1 MB liegt:
`Log-Rotation: 0 von N Dateien rotiert, 0.0 KB gesichert, 0 alte Stand(e) geloescht, 0 fehlgeschlagen.`

```bash
echo "Rueckgabewert: $?"        # 0
ls logs/*/*.log.2* 2>/dev/null  # keine Ausgabe - es wurde nichts angelegt
```

Der Rückgabewert ist 1 **nur** bei echtem Fehlschlag. Ein Lauf ohne fällige
Datei ist der Normalfall und darf keine Cron-Mail auslösen.

---

## Schritt 6 — Eine echte Logdatei rotieren ⚠️ **erst nach Rückfrage**

Verändert echte Dateien unter `logs/`. Inhalt geht nicht verloren, er liegt
danach im Archiv daneben. Zweck: den Kernfall an einem echten Dauerdienst
nachweisen — am `launchd`-Fehlerlog des Dashboards, das uvicorn offen hält.

```bash
ls -li logs/dashboard/launchd.err.log      # Inode notieren
wc -c logs/dashboard/launchd.err.log
python3 system/log_rotation.py --schwelle 1000
```

Danach:

```bash
ls -li logs/dashboard/launchd.err.log      # Inode UNVERÄNDERT
wc -c logs/dashboard/launchd.err.log       # klein
ls -l logs/dashboard/launchd.err.log.2*    # Archiv mit dem alten Inhalt
```

Jetzt eine Anfrage an das Dashboard schicken, damit uvicorn etwas protokolliert
(Seite im Browser neu laden oder `curl -s localhost:8000/api/portfolio >
/dev/null`), dann:

```bash
wc -c logs/dashboard/launchd.err.log       # GEWACHSEN
```

**Wächst die Datei nicht**, obwohl das Dashboard Anfragen beantwortet, ist das
der wichtigste mögliche Befund dieses Testauftrags: dann schreibt uvicorn nicht
im Anhängemodus, und das README-Kapitel „Warum kopiert und geleert wird" muss
korrigiert werden. Bitte melden, statt weiterzumachen.

Den Zustand danach so lassen — das Archiv ist der alte Inhalt und gehört nicht
gelöscht. Beim nächsten regulären Lauf mit der echten Schwelle passiert nichts
weiter, weil die Datei jetzt klein ist.

---

## Schritt 7 — Mutationsproben

Baut nacheinander plausible Fehler ein und prüft, dass der Selbsttest jeden
erkennt. Der Urzustand wird in jedem Fall wiederhergestellt — am Ende steht
`git status --short` wieder leer.

Dauer: rund 5 Minuten (jede Mutation lässt die ganze Suite laufen).

```bash
cat > /tmp/mut_logrot.py <<'PY'
import subprocess, sys
ZIEL = "system/log_rotation.py"
TEST = "system/test_log_rotation.py"
MUTATIONEN = [
    ("M1  umbenennen statt kopieren-und-leeren",
     '        gesichert = sichere_und_leere(eintrag["pfad"], ziel)',
     '        gesichert = os.path.getsize(eintrag["pfad"])\n'
     '        os.replace(eintrag["pfad"], ziel)\n'
     '        open(eintrag["pfad"], "wb").close()'),
    ("M2  Groessenpruefung des Archivs entfaellt",
     '                    if echte_groesse != gesichert:', '                    if False:'),
    ("M3  genau auf der Grenze wird nicht rotiert",
     '        elif eintrag["groesse"] < schwelle:', '        elif eintrag["groesse"] <= schwelle:'),
    ("M4  ein Stand zu viel geloescht",
     '    ueberzaehlig = vorhanden[:-staende] if staende > 0 else list(vorhanden)',
     '    ueberzaehlig = vorhanden[:-(staende + 1)] if staende > 0 else list(vorhanden)'),
    ("M5  die NEUESTEN Staende werden geloescht",
     '    ueberzaehlig = vorhanden[:-staende] if staende > 0 else list(vorhanden)',
     '    ueberzaehlig = vorhanden[staende:] if staende > 0 else list(vorhanden)'),
    ("M6  Archivmuster zu weit - trifft fremde .log.1",
     'STAND_MUSTER = re.compile(r"\\.log\\.\\d{4}-\\d{2}-\\d{2}T\\d{2}-\\d{2}-\\d{2}(-\\d+)?$")',
     'STAND_MUSTER = re.compile(r"\\.log\\.")'),
    ("M7  Suchmuster erfasst Datenbanken und .env",
     '    muster = os.path.join(log_wurzel, "**", "*.log")',
     '    muster = os.path.join(log_wurzel, "**", "*")'),
    ("M8  selbstrotierende Dateien werden angefasst",
     '    if rel in SELBSTROTIEREND:', '    if False:'),
    ("M9  alte Staende werden VOR dem Sichern geloescht",
     '        ziel = archivname(eintrag["pfad"])\n'
     '        gesichert = sichere_und_leere(eintrag["pfad"], ziel)',
     '        ziel = archivname(eintrag["pfad"])\n'
     '        ergebnis["geloescht"] = raeume_staende_auf(eintrag["pfad"],\n'
     '                                                  eintrag["staende"])\n'
     '        gesichert = sichere_und_leere(eintrag["pfad"], ziel)'),
    ("M10 ein Fehler reisst den ganzen Lauf mit",
     '    except Exception as fehler:                                # noqa: BLE001\n'
     '        ergebnis["grund"] = str(fehler)',
     '    except ZeroDivisionError as fehler:\n        ergebnis["grund"] = str(fehler)'),
    ("M11 vorhandenes Archiv wird ueberschrieben",
     '        with open(ziel, "xb") as archiv:', '        with open(ziel, "wb") as archiv:'),
    ("M12 Symlinks werden mitrotiert",
     '        elif os.path.islink(pfad):', '        elif False:'),
    ("M13 Fehlschlag wird als Erfolg gemeldet",
     '    return 1 if fehler else 0', '    return 0'),
    ("M14 truncate ohne 0 - nie geleert",
     '                quelle.truncate(0)', '                quelle.truncate()'),
    ("M15 kein fsync auf den Verzeichniseintrag",
     '            _fsync_ordner(ziel)\n', '            pass\n'),
    ("M16 fsync des Verzeichnisses in den heiklen Teil verschoben",
     '                # Nichts nachgekommen, nichts ungesichert: jetzt und nur jetzt.\n'
     '                quelle.truncate(0)',
     '                # Nichts nachgekommen, nichts ungesichert: jetzt und nur jetzt.\n'
     '                _fsync_ordner(ziel)\n                quelle.truncate(0)'),
    ("M17 fsync des Inhalts hinter den letzten Lesevorgang",
     '                # Nichts nachgekommen, nichts ungesichert: jetzt und nur jetzt.\n'
     '                quelle.truncate(0)',
     '                # Nichts nachgekommen, nichts ungesichert: jetzt und nur jetzt.\n'
     '                archiv.flush()\n                os.fsync(archiv.fileno())\n'
     '                quelle.truncate(0)'),
]
ur = open(ZIEL, encoding="utf-8").read()
erkannt, entgangen = [], []
try:
    for name, alt, neu in MUTATIONEN:
        if ur.count(alt) != 1:
            entgangen.append(f"{name} (Vorlage {ur.count(alt)}x)"); print(f"[?] {name}"); continue
        open(ZIEL, "w", encoding="utf-8").write(ur.replace(alt, neu))
        lauf = subprocess.run([sys.executable, TEST], capture_output=True, text=True)
        open(ZIEL, "w", encoding="utf-8").write(ur)
        if lauf.returncode != 0:
            erkannt.append(name); print(f"[erkannt] {name}")
            for z in [z for z in lauf.stdout.splitlines() if "[FEHLER]" in z][:2]:
                print(f"          {z.strip()}")
        else:
            entgangen.append(name); print(f"[ENTGANGEN] {name}")
finally:
    open(ZIEL, "w", encoding="utf-8").write(ur)
print(f"\n{len(erkannt)} von {len(MUTATIONEN)} Mutationen erkannt.")
for n in entgangen:
    print(f"  NICHT erkannt: {n}")
sys.exit(1 if entgangen else 0)
PY
python3 /tmp/mut_logrot.py
git status --short                # muss wieder LEER sein
```

Erwartet: **17 von 17 Mutationen erkannt.**

M15, M16 und M17 sind die interessanten: sie prüfen die *Reihenfolge* von
`fsync` und `truncate`. In der ersten Fassung dieser Änderung stand der `fsync`
an der falschen Stelle und kostete knapp eine Zeile pro Rotation. M15/M16
werden über einen Zähler erkannt (genau ein Verzeichnis-`fsync` je Rotation),
M17 über die Verlustmessung bei 5.000 Zeilen/s.

Entgeht eine Mutation, ist das die wichtigste Rückmeldung dieses
Testauftrags — dann ist die betreffende Zusicherung nur behauptet.

---

## Schritt 8 — Keine Regression

```bash
python3 system/test_caffeinate_plist.py       | tail -1
python3 notifications/test_schliess_benachrichtigung.py | tail -2
python3 notifications/test_manual_close.py    | tail -1
python3 dashboard/test_dashboard.py           | tail -1
python3 broker/test_broker.py                 | tail -1
python3 broker/test_ibkr.py                   | tail -1
python3 shared/test_empfehlung_format.py      | tail -1
```

| Suite | Erwartet |
|---|---|
| `system/test_caffeinate_plist.py` | 52 von 52 |
| `notifications/test_schliess_benachrichtigung.py` | 99 von 99 |
| `notifications/test_manual_close.py` | alle bestanden |
| `dashboard/test_dashboard.py` | 784/784 (780 ohne `node`) |
| `broker/test_broker.py` | 163 von 163 |
| `broker/test_ibkr.py` | 200 von 200 (168 ohne `ib_async`) |
| `shared/test_empfehlung_format.py` | 70 von 70 |

Diese Änderung fasst keinen bestehenden Code an; jede Abweichung hier hat eine
andere Ursache und gehört trotzdem gemeldet.

---

## Rückmeldung

Bitte zurückgeben:

1. Zahl aus Schritt 1 (erwartet 117/117) und Schritt 7 (erwartet 17/17).
2. Aus Schritt 2: die größte Logdatei mit Größe, und ob eine Datei über der
   Schwelle liegt.
3. Aus Schritt 4: `geschrieben` und `wiedergefunden` — und ob der Inode gleich
   blieb.
4. Falls Schritt 6 gelaufen ist: ob `logs/dashboard/launchd.err.log` nach einer
   Dashboard-Anfrage wieder gewachsen ist. **Das ist die wichtigste Einzelzahl**
   des ganzen Auftrags.
5. Jede entgangene Mutation, wörtlich.

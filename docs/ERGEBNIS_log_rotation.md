# Ergebnis — Log-Rotation für die Projektlogs

**PR #79** · Branch `claude/new-session-uqjk8h`, Basis `origin/main` (`b4b7acd`,
nach Merge von #78).

---

## Was gebaut wurde

`system/log_rotation.py` — ein eigenes Skript, keine zusätzliche Abhängigkeit,
**kein `sudo`**. Rotiert nach Größe, nicht nach Datum.

```bash
python3 system/log_rotation.py --status        # Übersicht inkl. alter Stände
python3 system/log_rotation.py --trockenlauf   # zeigt nur, was fällig wäre
python3 system/log_rotation.py                 # rotiert
```

Kein bestehender Code wurde geändert — keine Zeile in `broker/`, `strategies/`,
`notifications/`, `dashboard/`, keine launchd-Vorlage, keine Crontab.

---

## Die drei begründungspflichtigen Entscheidungen

**Eigenes Skript statt `newsyslog`.** Es bräuchte `sudo` und eine Datei unter
`/etc/newsyslog.d/` — dieselbe Abwägung wie bei `caffeinate`, hier mit mehr
Gewicht, weil eine Rotation *löscht*: ein Tippfehler im Pfad einer
root-Konfiguration löscht außerhalb von `logs/`. Die Konfiguration läge zudem
außerhalb des Repos, wäre also nicht versioniert und nicht testbar. Und für den
entscheidenden Fall hat `newsyslog` keine bessere Antwort: sein Standardverfahren
ist Umbenennen, und zum Neuöffnen bräuchte es eine PID-Datei und ein Signal, die
Dashboard, Telegram-Bot und launchd nicht liefern.

**Schwelle 1 MB.** Die größte Logdatei lag bei rund 262 KB, gewachsen über
Monate — 1 MB lässt reichlich Luft, und jede Rotation ist eine Schnittstelle, an
der man beim Suchen eine Datei weiterblättern muss. Nach oben begrenzt die
Lesbarkeit: 1 MB Text sind gut 10.000 Zeilen.

**5 Stände** (= 6 MB Obergrenze je Datei). Deckt den Zeitraum ab, in dem man
nach einem Vorfall noch nachsieht. Archive heißen `<name>.log.<Zeitmarke>` statt
`.1`, `.2`, `.3`: kein Umbenennen einer Kette, lexikalische = chronologische
Sortierung, und der Name endet nicht auf `.log`, wird also nie selbst zum
Kandidaten.

---

## Zwei Abweichungen — beide geprüft, nicht geraten

**`logs/broker/testnet_spiegel.log` enthält tatsächlich Ausführungsdaten**
(Order-IDs, Ausführungspreise, Teilausführungen, Gebühren, Tracebacks
fehlgeschlagener Versuche). Entscheidung: **nicht ausnehmen, sondern 20 Stände**
— auch für `ibkr_paper_spiegel.log`. „Ausgenommen" hieße hier „wächst weiter
unbegrenzt", und das ist der Zustand, der behoben werden soll. Tragfähig ist es,
weil das **Endergebnis jeder Order zusätzlich in der Broker-Datenbank** steht
(Tabelle `spiegelungen`, Fehlversuche in `versuche`). Das Protokoll ist die
ausführliche Fassung, nicht die einzige.

**Zwei der genannten Dateien rotieren sich längst selbst.**
`telegram_bot.log` (2 MB × 3) und `manuelle_eingriffe.log` (1 MB × 5) hängen an
einem `RotatingFileHandler` und sind damit schon begrenzt — der Auftrag führte
sie unter „wächst unbegrenzt". Sie sind **ausgenommen**; ein zweiter Rotator
würde zwei konkurrierende Namensschemata für dieselbe Datei einführen. Die
Zahlen werden nicht doppelt geführt: der Test liest sie **per AST aus den echten
Quelldateien** und vergleicht.

---

## Der Kern: kopieren und leeren, nicht umbenennen

Dashboard, Telegram-Bot und `caffeinate` halten ihre Logdatei dauerhaft offen.
Ein `mv` nimmt das offene Dateihandle mit — der Dienst schreibt weiter in die
umbenannte Datei, die neue bleibt für immer leer, und es fällt erst auf, wenn man
beim nächsten Fehler in der falschen Datei sucht.

Stattdessen wird kopiert und dann geleert (`truncate`). Die Datei behält ihren
**Inode**, jedes offene Handle zeigt weiter auf dieselbe, nun leere Datei.
Geprüft mit einem **echten zweiten Prozess**, der während der Rotation
durchgehend weiterschreibt.

### Die Restlücke — und der Fehler, den ich selbst gemacht habe

Zwischen dem letzten Lesevorgang und dem Leeren kann eine Zeile verloren gehen.
Das ist die bekannte Eigenschaft jedes Kopieren-und-Leeren-Verfahrens und ohne
Mitwirkung der schreibenden Prozesse nicht auflösbar.

**Meine erste Fassung war fünfmal schlechter als nötig.** Ich hatte die Lücke für
ein Mikrosekunden-Fenster gehalten; gemessen waren es **knapp eine verlorene
Zeile pro Rotation**, systematisch. Ursache: der `fsync` stand *nach* dem letzten
Lesevorgang, und ein `fsync` dauert Hunderte Mikrosekunden. Jetzt liegt alles
Teure davor — erlaubt, weil ein leerer Lesevorgang beweist, dass seit der
Prüfung nichts dazukam.

| Schreibrate | verlorene Zeilen |
|---|---|
| 200 Zeilen/s (weit über allem im Projekt) | **0** von 6.092, über 60 Rotationen |
| 5.000 Zeilen/s | **höchstens 1** je 10 Rotationen |
| 5.000 Zeilen/s, `fsync` an der falschen Stelle | 6 bis 10 je 10 Rotationen |

Hätte ich die Lücke nur *dokumentiert*, wie der Auftrag es zugelassen hätte, wäre
sie fünfmal größer geblieben.

### Was nie passiert

Geleert wird nur, wenn das Archiv nachweislich vollständig ist und auf der Platte
steht. Alte Stände werden erst **danach** gelöscht. Wächst eine Datei schneller
als kopiert werden kann, bricht die Rotation ab und leert **nichts**. Ein
vorhandenes Archiv wird nie überschrieben. Ein Fehlschlag bei einer Datei stoppt
weder die anderen noch irgendeinen Dienst.

---

## Tests

| Suite | Ergebnis |
|---|---|
| `system/test_log_rotation.py` *(neu)* | **117 / 117** ✅ |
| `system/test_caffeinate_plist.py` | 52 / 52 ✅ |
| `notifications/test_schliess_benachrichtigung.py` | 99 / 99 ✅ |
| `notifications/test_manual_close.py` | alle ✅ |
| `dashboard/test_dashboard.py` | 784 / 784 ✅ |
| `broker/test_broker.py` | 163 / 163 ✅ |
| `broker/test_ibkr.py` | 200 / 200 ✅ |
| `shared/test_empfehlung_format.py` | 70 / 70 ✅ |

**17 Mutationsproben, 17 erkannt** — im ersten Durchlauf nur 13. Die drei
Entgangenen waren die lehrreichen:

- **Symlink-Schutz** war von der Pfadgrenze verdeckt (mein Link zeigte nach
  außen). Derselbe Fehlertyp wie in PR #73. Behoben mit einem Link **innerhalb**
  von `logs/`.
- **Die `fsync`-Reihenfolge** entging, weil meine Probe `os.fsync` global
  verlangsamte — dann konvergiert die Nachlese nicht, die Rotation bricht ab und
  erreicht das Leeren nie. Jetzt: nur der Verzeichnis-`fsync` wird langsam, plus
  ein Zähler auf **genau einen** davon je Rotation.
- **Die Verlustgrenze** war geschätzt und hätte die Mutation durchgelassen. Jetzt
  gemessen (max 1 richtig gegen min 6 mutiert) und auf 3 gesetzt.

---

## Was du noch tun musst

**1. Nichts — es läuft nichts von allein an.** Die Rotation ist ein Skript, das
niemand aufruft, solange die Cron-Zeile fehlt. Nichts wird dadurch schlechter
als vorher.

**2. Den Cronjob eintragen, wenn du willst** (Zeile im README, **nicht**
eingetragen):

```cron
30 3 * * * cd ~/trading-bot && /usr/bin/python3 system/log_rotation.py >> logs/system/log_rotation.log 2>&1
```

Vorher `mkdir -p logs/system`. Unkritisch, dass die Crontab derzeit klemmt
(`Operation not permitted`): das Skript entscheidet nach **Größe** und braucht
kein Intervall — von Hand aufgerufen tut es genau dasselbe.

**3. Einmal `--status` ansehen.** Heute liegt keine Datei über 1 MB, ein echter
Lauf tut also nichts. Steht dort etwas anderes, ist das ein Befund.

Der vollständige Ablauf steht in `system/TESTAUFTRAG_LOG_ROTATION.md`. Dort ist
**Schritt 6** der einzige, der echte Logdateien anfasst (Inhalt bleibt im Archiv
erhalten) und ausdrücklich als rückfragepflichtig gekennzeichnet.

---

## Offene Punkte

- **Die Wiederholungen in `logs/broker/cron.log`** sind durch die Rotation nur
  *gedeckelt*, nicht behoben — die Ursache liegt in `broker/spiegel.py` und war
  laut Auftrag ausdrücklich nicht anzufassen.
- **Kein Test auf einem Schreiber ohne `O_APPEND`.** Ein solcher existiert im
  Projekt nicht; der Fall ist im README benannt (Loch aus Nullbytes, kein
  Datenverlust) und wird durch die Nullbyte-Prüfung indirekt bewacht.
- **Wer für ein Log null Verlust braucht**, lässt es in-process über einen
  `RotatingFileHandler` rotieren, so wie die beiden ausgenommenen Dateien. Für
  Cron- und launchd-Logs existiert dieser Weg nicht.

## Geänderte Dateien

```
system/log_rotation.py              (neu)
system/test_log_rotation.py         (neu, 117 Prüfungen)
system/README_LOG_ROTATION.md       (neu)
system/TESTAUFTRAG_LOG_ROTATION.md  (neu)
docs/UEBERGABE_log_rotation.md      (neu)
docs/ERGEBNIS_log_rotation.md       (neu, dieses Dokument)
docs/UEBERGABEPROTOKOLL.md          (Abschnitt 4.6 neu, offener Punkt 14 neu)
```

Das Übergabeprotokoll wurde ergänzt, obwohl der Auftrag es nicht verlangt: ein
neuer Systemdienst ohne Eintrag dort wäre genau die Drift, die PR #74 beseitigt
hat, und `CLAUDE.md` erklärt das Protokoll zur verbindlichen Grundlage.

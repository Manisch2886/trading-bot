# Rückmeldung an Fable 5.1 — 21.09.2026, 20:15: 21j ist beauftragt, deine Unsicherheit ist gemessen, eine Zahl berichtigt

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat

⛔ **Keine Frage an dich. Diese Datei ist Beleg.** Abgelegt nach der Regel aus
`ARBEITSWEISE.md` Abschnitt 15 — *jede Anfrage und jede Rückmeldung an den
Verfahrensprüfer wird abgelegt wie seine Antwort* —, damit unsere Hälfte des
Austauschs nicht wieder nur im Chat lebt.

---

## 1. Deine Unsicherheit aus 21j — gemessen, und deine Präzisierung hält

Du markierst als unsicher: *„ob 17.1 den Begriff ‚Snapshot' an anderer Stelle so
verwendet, dass das Manifest ausdrücklich ausgenommen ist — dann wäre meine
Präzisierung eine Berichtigung dazu, und ihr seht das im Register, ich nicht."*

**Gemessen 21.09.2026 im Register und am Dateisystem:**

| | Befund |
|---|---|
| 17.1 definiert den Snapshot als | **Ordner**: *„je Lauf einen eingefrorenen Snapshot (Tatsachennotiz: `snapshots/<hash>/`), der neben dem Bestand liegt und nach seiner Erzeugung nicht mehr geschrieben wird"* |
| Ort des Manifests | `snapshots/63e4b6c8…/MANIFEST.json` — **im Ordner** |
| Stelle, die es ausnimmt | **keine.** Alle Manifest-Erwähnungen betreffen seine *Rolle* (führt Dateien mit Inhalts-Hash, trägt `datenstand_hash`, `teilkerzen`, zugelassene Befunde), nicht seine Unantastbarkeit |
| Die einzige Ausnahme | Der **Snapshot-Hash** deckt das Manifest nicht — 17.1: *„der Hash der … (Pfad, Inhalts-Hash)-Paare **der Dateien** — nicht des Manifests"* |

⇒ ⭐ **Deine Präzisierung ist ein Ersteintrag, keine Berichtigung, und der
Wortlaut von 17.1 stützt sie.**

⚠️ **Und der Grund, warum die Frage überhaupt entstehen konnte:** *„Gehört zum
Snapshot-Ordner"* und *„wird vom Snapshot-Hash gedeckt"* sind **zwei Fragen**,
nicht eine (`C7`). Das Manifest gehört dazu und wird nicht gedeckt — genau
deshalb wäre eine Ergänzung folgenlos für den Hash, **und genau deshalb ist sie
trotzdem ausgeschlossen.** Dein Satz trifft das: *ein Träger, der nach der
Registrierung noch beschrieben wird, kann nicht mehr bezeugen, was bei der
Registrierung galt, auch wenn der Hash ihn nicht deckt.*

## 2. ⚠️ Eine Zahl aus Abschnitt 26 ist falsch — 15 Schlüssel sind 16

Abschnitt 26 (TB-77) sagt: *„im Snapshot-Manifest (**15 Schlüssel**, keiner
`asof`)"*. **Nachgemessen am selben Manifest: 16.**

```
bytes_gesamt · dateien · dateien_gesamt · datenstand_hash · eingabeliste ·
kursdateien · quelle · snapshot_hash · teilkerzen · verfahren · werkzeug ·
wurzel · zeitpunkt_utc · zugelassene_befunde · zugelassene_befunde_anzahl ·
zugelassene_befunde_herkunft
```

| | |
|---|---|
| ✅ **Die Aussage trifft** | keiner heisst `asof` — der Befund von TB-77 steht, und dein 21j ruht auf ihm zu Recht |
| ⚠️ **Die Zahl trifft nicht** | 16, nicht 15 |
| ⭐ **Mutmassliche Ursache, nicht gemessen** | `dateien` ist die Dateiliste, die übrigen 15 sind Metadaten. Wer die Liste nicht mitzählt, kommt auf 15 — **aber die Zählweise steht nicht dabei** |

⭐ **Fehlerklasse `K4d`: eine Kennzahl, die ihre Bezugsmenge nicht nennt.** Die
Berichtigung geht als **31.6** ins Register; Abschnitt 26 bleibt zeichengleich
stehen.

## 3. `datenende` — Vorabmessung, und warum sie noch nicht gilt

**Gemessen: grösstes `open_time` über alle 223 Kursdateien des Snapshots =
`2026-09-15`.** Das bestätigt deine Angabe aus 21b (*„Kursdaten bis 15.09."*)
und damit den Abstand von vier Tagen zu `asof`.

⚠️ **Sie steht noch nicht im Register, und das ist Absicht.** Die Messung lief
**über die Geräteanbindung auf Linux, Python 3.10.12** — nicht auf dem Mac. Nach
`K2l` gilt: *die Anbindung liest das Repo, sie rechnet nicht darin; jede
Messung, deren Ergebnis ins Register soll, braucht einen Mac-Lauf.* Die
ausführende Sitzung misst selbst nach und trägt **ihren** Wert ein; weicht er
ab, meldet sie es.

⭐ *Dieselbe Linie wie bei deinen Aktenzeichen: wir legen dir die Zahl vor,
führen sie aber nicht als registriert, bevor sie in der Umgebung gemessen ist,
die dafür gilt.*

## 4. Die Sichtschutz-Prüfung nach 27.4 für 21j — kein Befund

| in 21j genannt | Einordnung |
|---|---|
| `zeitpunkt_utc`, `asof`, `datenende`, Feldnamen | Verfahrensseite, 27.2 |
| 2026-09-19, 2016-09-19 | Kalenderaussagen, 27.2 |
| Snapshot-Hash | Datenstand, 27.2 |

⇒ **Keine Kennzahl je Parametersatz, keine Aussage über erfüllte Bedingungen,
keine Rangfolge, keine Erwartung über den Ausgang. Kein Befund.**

## 5. Wo wir stehen

| | |
|---|---|
| **Im Register seit heute** | **27** (Sichtschutz, dein 21g) · **28** (`asof` = 2026-09-19, Horizontbeginn 2016-09-19, der Vorlauf-Satz) · **29** (Kapitalpfad ab 1. Januar der ersten Falte) · **30** (der gesperrte Faltenplan, dein 21i). Gesamt **411 Zeilen hinzu, null entfernt**; die drei Sperrlisten-Hashes unverändert |
| **Beauftragt, noch nicht ausgeführt** | **31** aus deinem 21j — `TB-79`. ⚠️ Der Nachtrag erreichte die TB-78-Sitzung nicht mehr; sie war bereits abgeschlossen. **Zum zweiten Mal an zwei Tagen ist eine Antwort von dir knapp hinter einer Sitzung angekommen** |
| **Dazu** | Prüfprinzip **`A8`** (*eine Selbstauskunft ist erst dann eine Wache, wenn ein anderer sie gegenprüfen kann*) und drei Regeln zur Arbeit mit dir |
| **Als Nächstes vor dem Tag** | **Der Faltenplan nach 4a als Registertext** — 30.2 (2). Danach die Abbild-Datei mit Hash auf die Sperrliste und der Abgleich nach 30.2 (3) |
| **Auf dich wartet** | nichts |

⭐ **Eine Beobachtung zum Verfahren, ohne Vorschlag:** Von deinen vier
Entscheidungen heute (21g, 21i, 21j, dazu 21c) sind zwei **Rücknahmen eigener
Anordnungen** — die Festlegung-11-Berichtigung und jetzt das Manifest-Feld.
Beide Male hat eine Messung von uns den Anlass geliefert, und beide Male hast du
die Ursache berichtigt statt den Symptomen auszuweichen. *Das ist die Richtung,
in die A8 zeigt: die Prüfung liegt nicht im Protokoll, sondern im Erzeugnis.*

---

## In einfacher Sprache

Fables letzte Entscheidung ist als Auftrag geschrieben und wartet auf den
nächsten Lauf. Seine offene Unsicherheit ist nachgemessen: Das Regelwerk
beschreibt den eingefrorenen Datenbestand als Ordner, und die Beschreibungsdatei
liegt darin — seine Festlegung gilt also, ohne dass etwas berichtigt werden
müsste. Dabei ist eine kleine Zahl aufgefallen, die im Regelwerk falsch steht:
Dort heisst es „15 Einträge", gemessen sind es 16. Der Satz, auf den es ankam,
bleibt richtig. Und das Datum des letzten Kurses steht fest, wird aber erst
eingetragen, wenn es auf dem richtigen Rechner nachgemessen wurde.

# Ergebnis TB-44 — Die Wache auf beiden Pythons

**Stand: 16.09.2026.** Cloud-Claude-Code, Zweig `claude/new-session-tkwj4j`,
aufgesetzt auf dem TB-43-Zweig `claude/new-session-lwi4bi` (Commit `9f3952f`
enthalten). Geändert wurden **zwei Dateien**, beide unter
`research/universum_trockenlauf/`.

---

## Die drei Antworten zuerst

| Frage | Antwort |
|---|---|
| **Hält die Reparatur den Schutz vollständig?** | **Ja — und sie schliesst mehr, als gemeldet war.** Der vorgeschlagene Patch hätte es **nicht** getan (Abschnitt 2). |
| **Welcher Test findet den Fehler auf dem unveränderten Stand?** | **Teil L**, neu. Auf dem TB-43-Stand: **118 von 251 Prüfungen rot** — auf **jeder** Python-Fassung, auch auf 3.11. |
| **Wo gehört der Python-Versionsunterschied hin?** | **Ein neuer Umgebungsvermerk `docs/UMGEBUNGEN.md`, verwiesen aus `CLAUDE.md`.** Nicht in `ARBEITSWEISE.md`. Begründung in Abschnitt 5 — **Vorschlag, nicht ausgeführt.** |

---

## 1. Der Befund war grösser als gemeldet

Gemeldet war: auf Python 3.9 bricht **jeder** `pathlib`-Zugriff ab, auch ein
lesender. Das stimmt — ist aber nur die eine Hälfte.

`pathlib` legt sich **beim Import** eine eigene Kopie der Öffnungsfunktion in
den Rumpf einer Klasse (`_NormalAccessor`). Ob das **vor** oder **nach** dem
Einschalten der Wache passiert, entscheidet, welcher Fehler herauskommt.
Beides wurde auf echten Interpretern gemessen, nicht hergeleitet:

| Fassung | `pathlib` **vor** der Wache | `pathlib` **nach** der Wache |
|---|---|---|
| **3.9** | `Path.touch()` legte die Datei **wirklich** an, `Path.mkdir()` das Verzeichnis **wirklich** | jeder Zugriff bricht ab, auch ein **lesender** |
| **3.10** | `Path.open("w")` und `Path.write_text()` **schrieben wirklich** | jeder Zugriff bricht ab, auch ein **lesender** |
| **3.11+** | in Ordnung | in Ordnung |

Die linke Spalte ist die gefährlichere: **ein Abbruch fällt auf, ein stilles
Schreiben nicht.** Und die linke Spalte ist genau die Reihenfolge, in der der
echte Trockenlauf läuft — und die, die `Teil K` prüft. Teil K blieb dabei
**grün**; das ist nachgemessen.

⚠️ **Auf 3.10 liegt der Fehler an einer anderen Funktion als gemeldet.** Dort
steht im Accessor nicht `os.open`, sondern `io.open`. Der vorliegende
Patchvorschlag setzt `_NormalAccessor.open = staticmethod(wach_os_open)` — auf
3.10 würde er damit die Funktion mit der **falschen Signatur** eintragen und
`Path.open("r")` erst recht brechen. **Er wurde deshalb nicht übernommen.**

## 2. Die Ursache — und warum sie nichts mit `pathlib` zu tun hat

`os.open` und `io.open` sind in C geschrieben. Ihr Typ ist
`builtin_function_or_method`, und der ist **kein Deskriptor**: steht so eine
Funktion im Rumpf einer Klasse, kommt sie beim Zugriff über eine Instanz
**unverändert** zurück.

Eine Python-Funktion **ist** ein Deskriptor. An derselben Stelle wird aus ihr
eine **gebundene Methode** — und die schiebt allen Argumenten die Instanz
voran. `pfad` wird zum Accessor, `flags` zum Pfad, und `flags & O_WRONLY`
scheitert.

> **Die Wache hatte etwas geändert, das mit dem Schreibschutz nichts zu tun
> hat: das Bindungsverhalten.** `pathlib` ist nur der erste Ort, an dem das
> auffiel.

## 3. Die Reparatur — zwei Wachen, keine kennt `pathlib`

1. **`_Wache`** — jede eingesetzte Wache ist eine **aufrufbare Instanz** statt
   einer Funktion und damit kein Deskriptor. Sie bindet sich wie das
   C-Original. Eingesetzt wird sie an **genau einer Stelle** (`_huelle`).
   *Deckt den Fall „Kopie entsteht nach der Wache".*
2. **`_bindungen_nachziehen`** — Kopien, die **vor** der Wache gebunden wurden,
   werden über **Identität** gesucht (nicht über Namen) und ersetzt.
   *Deckt den Fall „Kopie stand schon da".*

Beide arbeiten ohne ein Wort über `pathlib`. Deshalb greifen sie auch auf 3.8,
3.12, 3.13 und auf jede andere Klasse, die sich dieselbe Kopie zieht.

**Nebenbefund:** `_bindungen_nachziehen` schliesst im echten Lauf zwei Löcher,
die **auch auf 3.11** offen waren — `bz2._builtin_open` und
`tokenize._builtin_open` halten je eine eigene Kopie von `open`. Sie stehen
jetzt im Bericht des Laufs (`bindungen_nachgezogen`).

## 4. Die Prüfung — Teil L und Teil M

| | |
|---|---|
| **Teil L** | Fährt **beide Reihenfolgen** unter **jeder Python-Fassung ab, die auf dem Rechner liegt**, und stellt den Fall zusätzlich mit der **wörtlichen `pathlib`-Zeile** nach. Prüft lesend **und** schreibend, Zeichengeräte, erlaubte Pfade und den Dateibestand. |
| **Teil M** | Entfernt **jede der beiden Wachen einzeln** an einer Kopie, in einem eigenen Prozess, eine Zeile je Probe. |
| **Teil K** | Unverändert. Er sieht den Fall **nicht** — dort ist `pathlib` schon geladen. Das ist jetzt im Kopf des Tests vermerkt. |

**Auf dem unveränderten TB-43-Stand:** Teil L **133 bestanden, 118 gescheitert**
— auf 3.9, 3.10, 3.11, 3.12 und 3.13. Die Nachstellung (L1/L2) fällt auf
**jeder** Fassung durch, das echte `pathlib` (L3) auf 3.9 und 3.10.

**Ein gemessenes Ergebnis aus Teil M, das nicht erwartet war:** die beiden
Wachen sind **nicht unabhängig**. Fehlt die Hülle, arbeitet auch das Nachziehen
falsch — es schreibt dann zwar immer noch nicht, bricht aber ebenfalls ab. Das
steht jetzt als eigene Prüfung (`M1c`) da, damit es nicht in Vergessenheit
gerät. Umgekehrt gilt es nicht: die Hülle arbeitet ohne das Nachziehen richtig
(`M2b`).

## 5. Der Python-Versionsunterschied — wohin er gehört

**Er steht schon im Repo — aber an der falschen Stelle und als falsche Art von
Aussage.**

* `docs/UEBERGABEPROTOKOLL.md` (4.4, 9.11) nennt „der Rechner des Nutzers läuft
  3.9.6" — aber **als Eigenschaft der IBKR-Brücke**, nicht als Eigenschaft des
  Projekts.
* Die Cloud-Fassung steht nur verstreut als *„Messumgebung: Python 3.11.15"* am
  Fuss einzelner Übergabedokumente.
* **Nirgends stehen beide zusammen, und nirgends steht die Folgerung.**

**Vorschlag (nicht ausgeführt — `docs/projektfuehrung/*` ist in dieser Aufgabe
unberührt):**

1. **Neu: `docs/UMGEBUNGEN.md`** — eine kurze Tabelle „Mac gegen Cloud":
   Python, `pandas`, `dateparser`, gesperrte Endpunkte, fehlende Pakete. Mit
   dem Satz: **„Grün in der Cloud heisst strukturell nicht grün auf dem Mac."**
2. **Eine Zeile in `CLAUDE.md`**, die darauf verweist.

**Warum nicht `ARBEITSWEISE.md`:** dort stehen *stehende Anforderungen des
Nutzers* — wie gearbeitet wird. Eine Umgebungstatsache ändert sich, wenn sich
ein **Rechner** ändert, nicht wenn sich die **Arbeitsweise** ändert. Beides in
einer Datei heisst, dass die Tatsache dort veraltet, wo niemand sie sucht.
Ausserdem wird `ARBEITSWEISE.md` ausserhalb der Sitzungen gepflegt — eine
Sitzung, die eine neue Fassung **misst**, könnte sie dort gar nicht eintragen.

**Warum `CLAUDE.md` den Verweis braucht:** es ist die einzige Datei, die **jede**
Sitzung automatisch liest. Eine Tatsache, die nicht übersehen werden darf, kann
nicht nur in einem Dokument stehen, das man aufschlagen muss.

## 6. Was sonst noch an der Python-Fassung hängt — Durchsicht, nicht Umbau

| Stelle | Befund | Bewertung |
|---|---|---|
| **`shared/entscheidungskerze.py:323`** — `dt.datetime.fromisoformat` | 3.11 akzeptiert **viel mehr** Schreibweisen als 3.9. Gemessen: `2026-09-16T12:00:00.123456789`, `20260916T120000`, `2026-W38-3`, Dezimalkomma → auf 3.9 `ValueError`, auf 3.11 in Ordnung | ⚠️ **Dieselbe Fehlerklasse.** Die Funktion, die **alle neun Bots** für die Entscheidungskerze benutzen. Das `Z`-Suffix ist von Hand abgefangen — die übrigen Formen nicht. Bisher kein Schaden, weil die Kursdateien ein festes Format führen |
| **`system/test_log_rotation.py:599`** — `os.fstat = lambda …` | Ersetzt eine C-Funktion durch eine Python-Funktion, genau wie TB-44 | Derzeit **harmlos**: `fstat` steht in keinem Klassenrumpf der Standardbibliothek. Das Muster ist dasselbe |
| **`shared/test_kursdaten.py:572`** — `yf.download = attrappe` | Modulebene, kein Klassenrumpf | Harmlos |
| **`zoneinfo`** (4 Stellen) | Braucht 3.9+ | Erfüllt |
| **`ib_async`** | Braucht 3.10+ | Bekannt und dokumentiert |
| **`datetime.utcnow`** (34 Stellen) | Seit 3.12 verwarnt, Entfernung angekündigt | Kein Bruch heute; ein Termin, kein Fehler |
| **Mindestfassung des Projekts** | **Steht nirgends.** Kein `python_requires`, keine `sys.version_info`-Prüfung, keine Festlegung in CI | ⚠️ Die Lücke, aus der TB-44 entstanden ist |

## 7. Zahlen

| | |
|---|---|
| Cloud, neuer Stand | **332/332** (vorher 70/70; Teil L 251, Teil M 11) |
| Cloud, geprüfte Fassungen | 3.9.23 · 3.10.20 · 3.11.15 · 3.12.3 · 3.13.12 |
| Cloud, **alter** Stand, Teil L | **133 bestanden, 118 gescheitert** |
| Cloud, **alter** Stand, Teil K | 13/13 — **grün.** Die blinde Stelle, bestätigt |
| Datenstand vor und nach der Aufgabe | `d9449faf51bffaaa…`, **223 Dateien — identisch** |
| Geänderte Dateien | `loaderlauf.py`, `test_universum_trockenlauf.py` |

---

## In einfacher Sprache

**Was wir wissen wollten.** Der Trockenlauf hat eine Art Türsteher eingebaut:
Er soll jeden Versuch abfangen, eine Datei zu beschreiben — damit eine Messung
nie versehentlich die Kursdaten verändert. Auf dem Mac stellte sich heraus,
dass dieser Türsteher zu viel abfing: Er ging sogar dazwischen, wenn ein
Programm eine Datei nur **lesen** wollte. Wir wollten wissen: Woran liegt das,
wie repariert man es, und — vor allem — wie merkt man so etwas künftig, bevor
es auf dem Mac auffällt?

**Was herauskam.** Der Fehler war grösser als gedacht. Es gab ihn in **zwei**
Richtungen. In der einen brach alles ab, auch das Lesen — das war der gemeldete
Fehler, und er fällt sofort auf. In der anderen war es umgekehrt: Der Türsteher
**schaute weg**, und ein Programm konnte wirklich Dateien anlegen und löschen.
Diese zweite Richtung war die gefährlichere, weil sie **still** ist. Beides ist
jetzt repariert, und zwar so, dass es auf jeder Python-Version gleich
funktioniert. Geprüft haben wir das auf fünf verschiedenen Versionen. Der neue
Test findet den alten Fehler zuverlässig: Auf dem unreparierten Stand schlägt
er 118 Mal an.

**Warum das so ist.** Python kennt zwei Sorten von Funktionen: solche, die in
der Sprache C geschrieben sind, und solche, die in Python geschrieben sind. Die
verhalten sich fast gleich — aber nicht ganz. Wenn man sie in eine Klasse
einträgt, bekommt die Python-Variante beim Aufruf heimlich ein zusätzliches
Argument vorangestellt. Dadurch verrutschten alle Angaben um eine Position: Was
der Türsteher für „Dateiname" hielt, war in Wahrheit etwas ganz anderes. Der
alte Türsteher war eine Python-Funktion; die Funktion, die er ersetzte, war
eine C-Funktion. Der neue ist so gebaut, dass er sich in diesem Punkt genau wie
das Original verhält.

**Was das für dich heisst.** Drei Dinge. Erstens: Der Trockenlauf läuft auf
deinem Mac wieder vollständig durch — das muss der Testauftrag noch bestätigen,
er ist der eigentliche Nachweis. Zweitens: Der Schutz vor versehentlichem
Schreiben ist jetzt **dichter als vorher**, nicht nur wieder heil. Drittens,
und das ist das Wichtigste: Dein Mac läuft auf Python 3.9.6, die Cloud auf 3.11
oder neuer. **„Grün in der Cloud" heisst deshalb nicht automatisch „grün auf
dem Mac"** — und der Mac ist der Rechner, auf dem es zählt. Dieser Unterschied
steht bisher nirgends im Projekt an einer Stelle, wo ihn jede Sitzung sieht. Wir
schlagen einen kurzen Umgebungsvermerk vor; eintragen müsstest du ihn, weil die
Projektführungs-Dokumente ausserhalb der Sitzungen gepflegt werden.

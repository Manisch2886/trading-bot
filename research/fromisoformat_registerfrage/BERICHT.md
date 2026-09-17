# `fromisoformat` im Live-Pfad — eine Registerfrage, keine Entwurfsfrage

**TB-45, Teil 5. Gemessen am 17.09.2026 in der Cloud (Python 3.11.15 gegen
3.9.23). Der Mac-Testauftrag holt die Messung auf 3.9.6 nach.**

> ⚠️ **Diese Untersuchung ändert `shared/entscheidungskerze.py` NICHT.** Sie
> misst und berichtet. Eine Änderung an der Entscheidungskerze ist eine
> Änderung am Live-Pfad aller neun Bots und braucht eine eigene Freigabe.

Werkzeug: `messung.py` (liest nur, fasst keinen Bot-Code an).

```
python3 research/fromisoformat_registerfrage/messung.py \
        --zweite-fassung trading-env/bin/python3
```

---

## Die Ausgangslage

`shared/entscheidungskerze.py:323` benutzt `dt.datetime.fromisoformat` — in
`_als_zeitpunkt()`, also in der Funktion, mit der **alle neun Bots seit dem
Umstellungstag (16.09.2026, 04:42:24Z) ihre Entscheidungskerze bestimmen**.
Python 3.11 nimmt dort deutlich mehr Schreibweisen an als 3.9, und der
Betrieb läuft auf 3.9.6.

---

## A — Was heute wirklich ankommt

**Mitgeschrieben, nicht angenommen.** `dt.datetime.fromisoformat` wurde im
Namensraum von `entscheidungskerze` durch einen Mitschreiber ersetzt; danach
lief `lade()` für fünf echte Symbole beider Märkte, einschließlich des
Rückfallwegs auf den Live-Abruf.

| | |
|---|---|
| Aufrufe | **4** |
| **verschiedene Werte** | **genau 1** |
| Der Wert | `'2026-09-16T00:00:00'` (Typ `str`) |

**Und woher er kommt:** Der Code baut ihn selbst — `f"{tag}T00:00:00"`, wobei
`tag` das Datum der letzten geschlossenen NYSE-Sitzung aus
`notifications/boersenkalender.py` ist (`shared/entscheidungskerze.py:434`
und `:525`). Es ist ein **maschinell erzeugter, kanonischer Wert**, keine
Eingabe von außen.

⭐ **Zwei Dinge, die vorher nicht festgehalten waren:**

1. **Die Zeitstempel der Kursdateien kommen hier gar nicht an.** Sie werden
   von `pandas` gelesen (`parse_dates`) und von
   `abrufschutz.oeffnungszeiten_ms` verarbeitet — `fromisoformat` sieht sie
   nie. Die Sorge „der Datenordner-Umbau berührt den Weg, auf dem diese
   Datumswerte entstehen" trifft damit **nicht** den Weg der Kursdaten,
   sondern nur den Weg des **Börsenkalenders**.
2. **Der Krypto-Pfad erreicht `fromisoformat` überhaupt nicht.** Er rechnet
   die Kerzengrenze aus dem Intervall (`(stand_ms // laenge - 1) * laenge`).
   Nur der **Aktien-Pfad** geht über den Kalender und damit über
   `fromisoformat`. Betroffen sind also **vier von neun Bots**, nicht neun.

---

## B — Welche Formen scheitern auf 3.9, gehen auf 3.11 aber durch

Derselbe Katalog, beiden Fassungen vorgelegt:

| Form | wozu sie im Katalog steht | 3.11.15 | 3.9.23 |
|---|---|---|---|
| `2026-09-16T00:00:00` | **kanonisch — genau das, was der Code heute baut** | ok | **ok** |
| `2026-09-16 00:00:00` | Leerzeichen statt `T` — so führen die Kursdateien es | ok | ok |
| `2026-09-16T00:00:00.123456` | Mikrosekunden, sechs Stellen | ok | ok |
| `2026-09-16T00:00` | Stunde und Minute, ohne Sekunden | ok | ok |
| `2026-09-16` | nur das Datum | ok | ok |
| `2026-09-16T00:00:00+00:00` | Offset ausgeschrieben | ok | ok |
| **`2026-09-16T00:00:00.123456789`** | Nanosekunden, neun Stellen | ok | ⚠️ **scheitert** |
| **`2026-09-16T00:00:00Z`** | `Z`-Suffix | ok | ⚠️ **scheitert** |
| **`20260916T000000`** | Grundform ohne Trennzeichen | ok | ⚠️ **scheitert** |
| **`20260916`** | nur das Datum, ohne Trennzeichen | ok | ⚠️ **scheitert** |
| **`2026-W38-3`** | Wochendatum nach ISO 8601 | ok | ⚠️ **scheitert** |
| **`2026-09-16T00:00:00,123`** | Dezimalkomma statt Punkt | ok | ⚠️ **scheitert** |
| `2026-260` | Ordinaldatum | scheitert | scheitert |
| `2026-09-16T24:00:00` | `24:00` als Tagesende | scheitert | scheitert |

**Sechs Formen** gehen auf 3.11 durch und scheitern auf 3.9. ⚠️ **Das
`Z`-Suffix ist darunter** — es wird heute in `_als_zeitpunkt` von Hand
abgefangen (`text[:-1] + "+00:00"`), **bevor** `fromisoformat` es sieht. Diese
Handarbeit ist also nicht Kosmetik, sondern der Grund, warum eine der sechs
Formen heute keinen Schaden anrichtet.

> *Gemessen auf 3.9.23, nicht auf den 3.9.6 des Betriebs. Die Grammatik von
> `fromisoformat` hat sich innerhalb der 3.9-Reihe nicht geändert; der
> Mac-Testauftrag prüft es trotzdem nach, weil „hat sich vermutlich nicht
> geändert" in diesem Projekt schon einmal falsch war.*

---

## C — Was passiert dann: Abbruch, stiller Rückfall oder falsche Kerze?

**Gemessen auf drei Ebenen**, indem genau die Form eingespeist wurde, die auf
3.9 scheitert:

| Ebene | Ausgang |
|---|---|
| `nur_entscheidbar()` | **`ValueError`** — wird nicht abgefangen |
| `lade()` (Aktien) | **`ValueError`** — kommt beim Bot an |
| `lade()` (Krypto) | **durchgelaufen** — der Krypto-Pfad ist nicht betroffen |
| **Der ganze Bot** (`elliott_wave_stocks`, 3 Symbole) | **läuft durch**; je Symbol eine Zeile `Fehler bei <SYM>: Invalid isoformat string: …`; **0 offene Positionen** |

**Die Antwort auf die Frage der Aufgabe, in einem Satz:**

> **Kein stiller Rückfall. Keine falsche Kerze. Kein Abbruch des Laufs.**
> Der Fehler landet in der Ladeschleife des Bots, die ihn je Symbol abfängt
> und meldet — und weil der kaputte Datumswert für **jedes** Symbol derselbe
> ist, fällt **jedes** Symbol heraus. Der Bot läuft zu Ende und handelt an
> diesem Tag **gar nicht**.

⚠️ **Und genau das ist die Form des Ausfalls, gegen die diese Aufgabe
geschrieben ist:** In den Zahlen sieht „alle 150 Symbole ausgelassen"
genauso aus wie „kein Signal". Sichtbar ist es nur in 150 Logzeilen, die
niemand liest.

**Betroffen wären die vier Aktien-Bots**, nicht alle neun — Krypto rechnet
ohne Kalender.

---

## Die Registerfrage — Vorlage, keine Entscheidung

Die Aufgabe formuliert sie so: *„Ein Bot, der ein Datum nicht versteht, darf
nicht auf einer falschen Kerze handeln — aber er darf auch nicht die anderen
acht mitreißen."*

**Was die Messung dazu beiträgt:**

| | |
|---|---|
| **Handelt er auf einer falschen Kerze?** | **Nein.** Es gibt keinen Rückfall auf eine Näherung; die Ausnahme fliegt. |
| **Reißt er die anderen mit?** | **Nein.** Jeder Bot ist ein eigener Cronjob; der Krypto-Pfad erreicht die Stelle gar nicht. |
| **Fällt es auf?** | ⚠️ **Nur in den Logzeilen.** Es gibt keine Telegram-Meldung und keinen Rückgabewert ≠ 0. |

**Drei Wege stehen offen — zu entscheiden, nicht hier zu wählen:**

1. **So lassen.** Der heutige Ausgang ist bereits „lieber nicht handeln als
   falsch handeln", und der kanonische Wert kann die Stelle gar nicht
   erreichen. Kosten: die Sichtbarkeit bleibt bei 150 Logzeilen.
2. **Den Wert nicht mehr über `fromisoformat` führen.** `tag` ist ein Datum
   aus dem Kalender; `dt.datetime.combine(tag, dt.time())` bzw.
   `dt.datetime.strptime(str(tag)[:10], "%Y-%m-%d")` kommt ohne die
   Fassungsunterschiede aus. Der kleinste Eingriff — aber er sitzt im
   Live-Pfad und braucht deshalb eine eigene Freigabe.
3. **Melden statt nur loggen.** Ein unlesbares Datum geht über dieselbe
   Telegram-Leitung wie `entscheidungskerze.melde()` (TB-32/TB-38). Ändert
   am Handeln nichts, macht den Tag aber sichtbar, an dem ein Bot nichts tat.

⭐ **Unabhängig davon empfehlenswert und ohne Freigabe nicht machbar:** eine
Mindestfassungsprüfung. `docs/UMGEBUNGEN.md` hält fest, dass die
Mindestfassung des Projekts **nirgends steht** — kein `python_requires`, keine
`sys.version_info`-Prüfung. Solange das so ist, ist jede Aussage der Form
„läuft auf 3.9" eine Beobachtung, keine Zusicherung.

---

## D — Nebenbefund aus TB-44: `os.fstat` in `system/test_log_rotation.py:599`

**Die Frage:** Dort wird `os.fstat` durch eine **Python-Funktion** ersetzt —
dasselbe Deskriptor-Muster, das in TB-44 zum Befund wurde. Ist das stabil?

**Der Kern des TB-44-Befundes:** Eine C-Funktion ist **kein** Deskriptor, eine
Python-Funktion schon. Steht sie in einem **Klassenrumpf**, wird sie beim
Zugriff zur gebundenen Methode — und die Argumente verrutschen. Genau das
passierte bei `pathlib._NormalAccessor.open`, und zwar **nur auf 3.9 und
3.10**.

**Gemessen auf jeder Fassung, die auf diesem Rechner liegt** (dieselbe
Methode wie Teil L des Trockenlaufs), durchsucht wurden die Klassenrümpfe von
`pathlib`, `io`, `tempfile`, `shutil`, `os`, `zipfile`, `tarfile`, `gzip`,
`mmap`, `socket`, `subprocess`:

| Python | `os.fstat` ist ein | Klassenrümpfe mit `os.fstat` |
|---|---|---|
| 3.9.23 | `builtin_function_or_method` | **keiner** |
| 3.10.20 | `builtin_function_or_method` | **keiner** |
| 3.11.15 | `builtin_function_or_method` | **keiner** |
| 3.12.3 | `builtin_function_or_method` | **keiner** |
| 3.13.12 | `builtin_function_or_method` | **keiner** |

**Die Antwort, ehrlich formuliert:**

> **Heute stabil — auf allen fünf Fassungen, gemessen.** Aber stabil aus
> demselben Grund, aus dem `_ist_geraet` harmlos war (TB-45, Teil 3):
> **Zufall der Umstände, nicht des Entwurfs.** Die Bedingung, an der es
> hängt, ist „keine Standardbibliotheks-Klasse bindet sich `os.fstat` in
> ihren Rumpf" — und genau diese Bedingung hat sich bei
> `pathlib._NormalAccessor` zwischen zwei Fassungen geändert.

⚠️ **Der Unterschied zu TB-44:** Dort war der Ersatz **produktiver
Schutzcode**, hier steht er in einem **Test**. Bricht er, wird der Test rot —
er lässt nichts still durch. Das Risiko ist damit klein, aber nicht null: ein
rot gewordener Test, den niemand zuordnen kann, kostet einen Basislauf
(T38.10 ist genau so ein Fall).

**Empfehlung, nicht dringend:** dieselbe `_Wache`-Hülle benutzen, die TB-44
in `loaderlauf.py` eingeführt hat. Das macht die Frage gegenstandslos, statt
sie je Fassung neu zu beantworten. `system/test_log_rotation.py` ist nicht
Gegenstand dieser Aufgabe und wurde **nicht angefasst**.

---

## In einfacher Sprache

**Was wir wissen wollten.**
Neun Programme entscheiden jeden Tag, welche Kursdaten sie benutzen dürfen.
An einer Stelle lesen sie dafür ein Datum aus einem Text — zum Beispiel
`2026-09-16T00:00:00`. Das Werkzeug, das diesen Text liest, heißt
`fromisoformat`. Es gibt davon zwei Ausgaben: eine ältere auf dem Rechner
des Betreibers (Python 3.9) und eine neuere in der Cloud (3.11). Die neuere
versteht mehr Schreibweisen als die ältere. Die Frage war: **Kann daraus ein
Schaden entstehen — und was passiert, wenn doch?**

**Was herauskam.**
An dieser Stelle kommt heute **genau eine einzige Schreibweise** an, und die
verstehen beide Ausgaben. Das Programm baut den Text selbst zusammen;
niemand von außen kann ihn beeinflussen. Sechs andere Schreibweisen würden
die ältere Ausgabe nicht verstehen — aber keine davon kann heute an dieser
Stelle ankommen. Die Zeitangaben aus den Kursdateien laufen über einen ganz
anderen Weg und berühren diese Stelle nie. Und die fünf Krypto-Programme
kommen an dieser Stelle überhaupt nicht vorbei; betroffen wären nur die vier
Aktien-Programme.

**Warum das so ist.**
Der Text entsteht aus dem Börsenkalender: „letzter Handelstag der New Yorker
Börse" plus „00:00:00". Das ergibt immer dieselbe, einfachste Form. Sollte
dort je eine ungewöhnliche Schreibweise auftauchen, haben wir gemessen, was
dann geschieht: Das Programm **rechnet nicht falsch weiter** und es **stürzt
nicht ab**. Es lässt jedes Symbol aus, schreibt für jedes eine Zeile ins
Protokoll und beendet den Tag, ohne zu handeln.

**Was das für dich heißt.**
Heute ist hier nichts kaputt, und es ist auch nicht knapp — es ist mit
Abstand in Ordnung. Zwei Dinge solltest du trotzdem wissen. Erstens: Wenn es
je schiefginge, würde ein Programm **stillschweigend nichts tun** und das nur
in seinem Protokoll vermerken. In der Auswertung sähe das genauso aus wie
„es gab heute kein Kaufsignal". Zweitens: Es gibt drei Wege, das zu
verbessern — den Text gar nicht mehr über dieses Werkzeug lesen, oder eine
Meldung per Telegram schicken, oder alles so lassen. **Welcher Weg genommen
wird, ist deine Entscheidung, nicht unsere** — deshalb steht hier eine
Vorlage und keine Änderung. An den Programmen selbst wurde für diesen Teil
**nichts** geändert.

# Anfrage an Fable 5.1 — 23.09.2026, 18:00: Eine bezeugte Datei beschreibt einen Datenstand, den es nicht mehr gibt

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD zur Messzeit:** `ad94b38` (TB-93 Abgabe)
**Bezug:** deine Antwort 23c, Abschnitt 2 — der Determinismusnachweis, den du für
`messgroessen.py` verlangt hast

**Sichtschutz:** Verfahrensmessungen — 27.2. ⛔ Keine Kennzahl des Selektionsraums.

⚠️ **Diese Anfrage kommt zusammen mit 23e** (die dritte Leserin), die noch
unbeantwortet ist.

---

## 1. ⭐ Deine Bedingung hat genau das getan, wofür sie da war

Du hast verlangt: *„ein Lauf mit `--ziel` auf einen neuen Pfad reproduziert
`ergebnisse/messgroessen.json` **bytegleich** — sonst Befund und Stopp."*

⛔ **Er reproduziert sie nicht.** 48 von 127 Blattwerten weichen ab. Nichts wurde
nachgebessert, Block C ist entfallen, kein Vollzug.

⭐⭐ **Aber die Sitzung hat die Ursache ausgemessen, statt sie zu vermuten** — mit
einer Gegenprobe, die nicht im Auftrag stand:

| | |
|---|---|
| **Eingaben** | der alte Stand aus der Git-Historie (`git archive a2fcf01 data config …`), umgelenkt ins Scratchpad |
| **Code** | HEAD, die **neu abgesicherte** Fassung von `messgroessen.py` |
| **Ziel** | Scratchpad — ⛔ **nicht** `ergebnisse/` |
| **Ergebnis** | ⭐⭐ **bytegleich** mit der eingefrorenen Datei, `rc 0` |

⇒ ⭐ **Code und Ausgabeformat sind deterministisch, auch nach der Absicherung.**
Deine Bedingung ist als Prüfung bestanden; was sie aufgedeckt hat, ist etwas
anderes.

## 2. ⚠️⚠️ Der Befund: die Eingaben sind weg

**Die Abweichungen verteilen sich nicht zufällig:**

| Gruppe | Blätter | abweichend |
|---|---|---|
| `datenbereiche.krypto_{1d,4h,1h}` | je 5 | je **3** |
| `volatilitaet.krypto_{1d,4h,1h}` | je 14 | je **13** |
| ⭐ `datenbereiche.aktien_1d`, `volatilitaet.aktien_1d` | 19 | **0** |
| ⭐ `kosten`, `datenfrequenz`, `haltedauer`, `universum` | 51 | **0** |

**Erste abweichende Stelle:** `datenbereiche.krypto_1d.frueheste`,
`2021-09-01` → `2017-08-17`.

**Die Ursache ist ein einzelner Commit:** `90e3cbd` (TB-34, 15.09., *„BTC/ETH ab
2017-08-17"*) berührte 91 Dateien unter `data/` — **keine davon eine
Aktiendatei**. Genau das Muster der Abweichungen.

⇒ ⚠️⚠️ **`ergebnisse/messgroessen.json` ist nur noch aus der Git-Historie
reproduzierbar, nicht aus dem heutigen Arbeitsstand.** Die Kursdaten, aus denen
sie entstand, liegen so nicht mehr in `data/`.

## 3. Warum das mehr ist als eine alte Datei

⭐ **Gemessen:** `registerdaten.py` Zeile 64 liest `ergebnisse/messgroessen.json`
— und der **Faltenplan** hängt daran. Die Datei ist keine Randnotiz, sondern
Eingabe des Verfahrens.

⚠️ **Und nach deiner eigenen Präzisierung aus 23c** ist sie gesperrt, *„weil ihr
Hash am Tag bezeugt wird"* (`EINGEFROREN`, `register()`, 37.4).

⇒ **Am signierten Tag würde das Register einen Hash bezeugen, dessen Eingaben im
Arbeitsstand nicht mehr existieren.** Ein Lauf am Tag misst über andere Daten,
als die bezeugte Datei beschreibt.

## 3b. ⚠️⚠️ NACHGEMESSEN 18:20 — es geht an die Rastergrenzen

**Nach dem Schreiben dieser Anfrage haben wir weitergemessen.** Der Befund ist
grösser, als Abschnitt 3 ihn beschreibt.

`registerdaten.py::achse_werte` — im Quelltext überschrieben mit *„Die Stufen
einer Achse – gerechnet, nie getippt"* — liest `mess["volatilitaet"][…]`.
**Das sind genau die Felder, die abweichen.**

**Gemessen, eingefrorener Stand gegen heutigen Datenstand:**

| | |
|---|---|
| Rasterachsen **gleich** | 22 |
| ⚠️⚠️ Rasterachsen **verschieden** | **12** |
| Betroffene Bots | `elliott_wave`, `rsi2_crypto`, `t3_supertrend`, `turtle_soup_crypto`, `volatility_breakout_crypto` — ⭐ **die fünf Krypto-Bots** |
| Unberührt | die vier Aktien-Bots |
| Stufen**zahl** je Achse | unverändert (4/4, 5/5, 6/6) |
| ⭐ Zellenzahl je Bot | **unverändert bei allen neun** |
| ⭐ Faltenpläne | **unverändert bei allen neun** |

⇒ ⚠️⚠️ **Der Selektionsraum hätte dieselbe Form, aber andere Gitterpunkte.** Die
Parameterwerte, über die am Tag gesucht wird, hängen am Datenstand — und bezeugt
wird der vom 14.09.

⛔ **Sichtschutz 27.1:** Die Stufenwerte selbst nennen wir nicht, nur dass sie
abweichen und wo.

### ⭐ Und eine Berichtigung an uns, bevor sie jemand als Befund liest

Wir hatten vermutet, der rote Test (`KeyError: '2017'`, Plan-Punkt 8) habe
dieselbe Wurzel — die Krypto-Historie reicht neuerdings bis `2017-08-17` zurück.
⛔ **Gemessen: falsch.** Die Falte `2017` stammt von der **Aktienseite**
(`aktien_1d.frueheste` = `1962-01-02`, in beiden Ständen gleich), und die
Faltenpläne sind unter beiden Datenständen identisch. **Punkt 8 und dieser
Befund hängen nicht zusammen.** *Wir melden den widerlegten Verdacht mit, damit
niemand ihn später neu aufstellt.*

---

## Die Frage

| | |
|---|---|
| **(1)** | Darf eine Datei, deren Hash am Tag bezeugt wird, einen Datenstand beschreiben, der **nicht mehr im Arbeitsstand liegt**? ⭐ Wir halten das für den Kern: Die Bezeugung sagt „so war es", der Arbeitsstand sagt „so ist es", und beides fällt auseinander |
| **(2)** | Falls nein: Wird `messgroessen.json` **neu gerechnet** (und damit der Faltenplan, und damit alles, was daran hängt) — oder wird der **Datenstand** auf `a2fcf01` zurückgeführt? ⚠️ Das Erste rührt an den Faltenplan vor dem Tag; das Zweite verwirft zwei Wochen Krypto-Historie |
| **(3)** | Falls ja (die Datei bleibt): Was genau bezeugt der Hash dann — die Messung, oder den Zustand? ⭐ Und genügt eine Tatsachennotiz, die den Eingabestand (`a2fcf01`) benennt, damit die Datei aus der Historie reproduzierbar bleibt? |
| **(4)** | ⚠️ **Und die allgemeine Form:** Gilt für **jede** eingefrorene Ergebnisdatei, dass ihr Eingabestand mitbezeugt werden muss? `ergebnisse/faltenplan.json` und `ergebnisse/benchmark_drawdowns.json` stehen in derselben Liste — ⭐ ihre Eingaben haben wir **nicht** geprüft |

⭐ *Wir neigen zu (3) mit Tatsachennotiz plus (4) als Regel: Eine bezeugte
Ergebnisdatei ohne benannten Eingabestand ist ein Hash ohne Herkunft. Aber ob
das vor dem Tag genügt oder ob neu gerechnet werden muss, ist deine
Entscheidung.*

---

## 4. ⚠️ Ein zweiter Befund, aus derselben Messung

Beim Prüfen von `A-N6` (erscheint ein Genehmigungsdialog?) hat die Sitzung
nachgemessen und gefunden: **Vier der zehn `EINGEFROREN`-Einträge standen in
keiner Regel der Berechtigungsdatei** — `messgroessen.py`, `kennzahlen.py`,
`pruefe_grenzsaetze.py` und `ergebnisse/messgroessen.json`.

⚠️ **Das ist ein Fehler des steuernden Chats.** Die Lockerung vom 22.09. kannte
die Sperrliste, nicht `EINGEFROREN` — deine Präzisierung aus 23c ist einen Tag
jünger. ⭐ **Geschlossen am 23.09., 17:48:** alle sieben Programmdateien unter
`ask`, alle drei Ergebnisdateien unter `deny`, als `Edit`-Regel. Gegenprobe:
**0 von 10 ungeschützt.**

*Kein Antwortbedarf — wir melden es, weil es deine Präzisierung in der Praxis
prüfbar macht und weil es zeigt, dass die Berechtigungsdatei der Liste
hinterherläuft, wenn niemand sie abgleicht.*

⭐ **Für deine Sonde „Schreibziele" aus 23c heisst das:** Sie sollte auch prüfen,
ob jeder Pfad der drei Gruppen in der Berechtigungsdatei steht. Das ist
derselbe Abgleich, nur an anderer Stelle.

---

## In einfacher Sprache

**Die Probe, die du verlangt hast, hat funktioniert — und etwas aufgedeckt, das
niemand gesucht hat.**

Das Programm sollte seine eigene alte Ausgabedatei Byte für Byte wiederholen.
Das tut es nicht. Aber die Sitzung hat nachgemessen, woran es liegt: **Nicht am
Programm.** Holt man den Datenstand von vor zwei Wochen aus der Versionshistorie
zurück und lässt dasselbe Programm darüber laufen, kommt exakt die alte Datei
heraus.

**Was sich geändert hat, sind die Kursdaten.** Vor acht Tagen wurde die
Krypto-Historie um vier Jahre nach hinten erweitert. Genau die Werte, die davon
betroffen sind, weichen ab — die Aktienseite und alles andere ist unverändert.

**Das Unangenehme daran:** Diese Datei wird am Stichtag mit ihrer Prüfsumme
bezeugt, und der Faltenplan baut auf ihr auf. Sie beschreibt damit einen
Zustand, den es im Arbeitsverzeichnis nicht mehr gibt — nur noch in der
Versionshistorie. Ob das zulässig ist, ob neu gerechnet werden muss oder ob eine
Notiz über die Herkunft genügt, entscheidet der Verfahrensprüfer.

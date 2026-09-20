# TB-63 Die fünf Epics auslagern — an: Claude Code am Mac (lokale Sitzung)

**Sitzungstitel für Claude Code: `TB-63 Epics auslagern`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main` — kein Zweig, kein PR
(Regelweg für Dokumentation, `ARBEITSWEISE.md` Abschnitt 5b).

⭐ **Rechnet nicht.** Reine Dokumentationsarbeit.

⚠️⚠️ **SETZT TB-62 VORAUS.** Beide ändern `BACKLOG.md`. Läuft TB-62 noch oder
ist sein Commit nicht auf `origin/main`, **brich ab und melde es.**

---

## 0. Warum es diese Aufgabe gibt — gemessen am 20.09.2026 an `e5720ed`

**Die Pflichtlektüre jeder neuen Sitzung steht bei 327 576 Bytes**, davon
`BACKLOG.md` **225 194 B = 69 %**. Darin:

| Abschnitt | Bytes | Anteil am Backlog |
|---|---:|---:|
| 2 — Vor TB-30b | 107 135 | 47,6 % |
| ⭐ **2t–2y — die fünf Epics** | **64 643** | **28,7 %** |
| 4 — Laufend, klein | 18 831 | 8,4 % |
| übrige | 34 585 | 15,3 % |

⭐⭐ **Der Befund: Alle fünf Epic-Blöcke sind ausdrücklich hinter dem signierten
Tag geparkt — und sagen das in ihrem jeweils ersten Punkt selbst.**

| Block | Epic | erster Punkt sagt |
|---|---|---|
| `2t` | AF | *„AF0 — DAS EPIC IST AUFGENOMMEN UND HINTER DEM SIGNIERTEN TAG GEPARKT"* |
| `2u` | MI | *„MI0 — AUFGENOMMEN, GEPARKT — und zwar HINTER Epic AF"* |
| `2v` | QR | *„QR0 …"*, Reihenfolge hinter AF (QR6) |
| `2w` | KG | Einordnung *„hinter AF, QR und vor MI"* |
| `2x` | RT | Einordnung *„direkt hinter AF und vor QR"* |
| `2y` | Querschnitt über (n)–(r) | gehört zu den fünf |

⇒ **Sie entscheiden heute nichts, und jede Sitzung liest sie vollständig.**

⭐ **Die Datei verlangt das selbst.** Ihre zweite Zeile lautet seit jeher:
*„Nur **aktive Punkte**."* **Geparkte Arbeit ist nicht aktiv.**

⚠️⚠️ **Betreiberentscheidung 20.09.2026: auslagern nach `BACKLOG_EPICS.md`,
mit Verschiebenachweis.**

---

## 1. Die Beweisregel — dieselbe wie bei TB-60

> ⭐ **Jede aus `BACKLOG.md` entfernte Zeile erscheint zeichengleich in
> `BACKLOG_EPICS.md`.**

**Nachgewiesen durch einen Vergleich der beiden Zeilenmengen, der leer
herauskommen muss.** Gegenprobe in die andere Richtung: die Zeilen, die nur im
Ziel stehen, sind **Kopf und Verweise** — nenne ihre Zahl und ihren Zweck.

⚠️⚠️ **Der Filter darf keine entfernten Markdown-Trennlinien `---` mit
Diff-Kopfzeilen verwechseln.** *Bei TB-60 zählte der erste Prüflauf deshalb 546
statt 561 Zeilen; erst der `numstat` als zweite Zählung hat es aufgedeckt.*

⭐ **Halte das Ergebnis gegen `git diff --numstat`**, bevor du es als Nachweis
abgibst.

---

## 2. Was verschoben wird

**Sechs Blöcke, vom Ankertext**

```
## 2t — Epic AF: Autonome Strategie-Forschungspipeline
```

**bis ausschliesslich zum Ankertext**

```
## 3 — Die Kette (Ränge 1 bis 5)
```

⛔ **Dieser Auftrag nennt bewusst KEINE Zeilennummern und keine Zeilenzahl.**
TB-62 verändert `BACKLOG.md` vor dir; jede Zahl von heute wäre morgen falsch.
*In den letzten drei Aufträgen standen vier Zahlen, die geschätzt statt gezählt
waren, und TB-59 hat zweimal zu Recht widersprochen.* **Arbeite an den
Ankertexten und zähle selbst.**

⚠️ **Prüfe vorher, ob TB-62 einen der sechs Blöcke verändert hat** — Nachtrag (v)
bringt einen neuen Block `2z`, der **nicht** zu den Epics gehört und **bleibt**.

### ⛔ Was ausdrücklich NICHT mitgeht

| | |
|---|---|
| **Block `2z`** (aus TB-62) | gehört nicht zu den Epics |
| **Abschnitt 3, Ränge 6, 7, 8** | die Kettenzeilen für AF, QR und MI **bleiben im Backlog** — sie sind die Stelle, an der die Reihenfolge steht, und sie sind kurz |
| **Kettenzeilen 0,96 / 0,97 / 0,98** | `AF-F0`, die Backlog-Sichtung und `MI-F0 / MI-T0.1` sind als **ortsunabhängig und rein lesend** markiert, also **nicht geparkt** — sie bleiben |
| **Alles in Abschnitt 4** | auch die K-Nummern, die aus den Epic-Nachträgen stammen (`K2p`–`K3j`) — sie sind allgemeine Regeln, nicht Epic-Arbeit |

⭐ **Die Unterscheidung, an der du dich orientierst:** *Was heute etwas
entscheidet, bleibt. Was erst nach dem Tag stattfindet, geht.*

---

## 3. Der Kopf von `BACKLOG_EPICS.md`

Nach dem Muster von `BACKLOG_ARCHIV.md`: was die Datei enthält, wann sie zu
lesen ist (**nur wenn es um die Epics geht**), der Verweis auf das
Ergebnisdokument, und der Satz, dass nichts gelöscht wurde.

⭐ **Dazu die Reihenfolge, weil sie sonst verlorengeht:**

> **`AF → RT → QR → KG → MI`** *(begründet in Nachtrag (r), RT9 — nicht nach
> Anspruch, sondern nach Voraussetzungen: RT braucht fast keine und macht AFs
> Ausgabe erst glaubwürdig).*

---

## 4. Was im `BACKLOG.md` an ihrer Stelle bleibt

**Eine Verweistabelle**, wie bei den Rückblicken `2b`–`2r`:

| Block | Epic | Datei |
|---|---|---|
| `2t` | AF — Autonome Forschungspipeline | `BACKLOG_EPICS.md`, Abschnitt `2t` |
| … | … | … |

**Darüber zwei Sätze:** dass alle fünf hinter dem signierten Tag geparkt sind,
und dass die Datei nur gelesen wird, wenn es um die Epics geht.

⚠️ **Die Blockbezeichner bleiben unverändert** — `2t` heisst auch in der neuen
Datei `2t`. *Ein umbenannter Bezeichner bricht jeden Verweis, und es gibt
welche.*

⭐ **Prüfe das:** Suche im ganzen `docs/`-Baum nach Verweisen auf `2t` bis `2y`
und nenne im Bericht, wie viele du gefunden hast und ob sie noch stimmen.

---

## 5. Die Schritte

### Schritt 0 — vor allem anderen

**Committe, was im Arbeitsbaum liegt.** Der Nachweis „Arbeitsbaum sauber" wird
**danach** geprüft. Findest du nichts, sag es und mach weiter.

⚠️ **Und prüfe hier:** Ist TB-62 auf `origin/main`? Wenn nein, **abbrechen**.

### Schritt 1 — `BACKLOG_EPICS.md` anlegen, Blöcke verschieben

**Sichern: commit und push.**

### Schritt 2 — Verweistabelle in `BACKLOG.md`, Kopf in der neuen Datei

**Sichern: commit und push.**

### Schritt 3 — die Nachweise rechnen

**Sichern: commit und push.**

### Schritt 4 — die Abgabe

`docs/ERGEBNIS_TB-63_epics_auslagern.md` und ein Journal-Nachtrag.

**Sichern: commit und push.**

---

## 6. Die Nachweise, die diese Aufgabe schuldet

| # | Nachweis |
|---:|---|
| **1** | `git status --short` **vor** dem ersten Schreiben |
| **2** | ⭐⭐ **Verschiebenachweis** — entfernte Zeilen, davon wie viele **nicht** zeichengleich in `BACKLOG_EPICS.md` (erwartet **0**); Gegenprobe: wie viele Zielzeilen sind Kopf und Verweise |
| **3** | `git diff --numstat` je Datei — **als zweite, unabhängige Zählung gegen Nachweis 2** |
| **4** | `BACKLOG.md` vorher → nachher: Zeilen **und** Bytes, selbst gezählt |
| **5** | ⭐ **Pflichtlektüre vorher → nachher.** ⚠️ **Die Menge ist: `UEBERGABE_2026-09-19.md`, `ARBEITSWEISE.md`, `PRUEFPRINZIPIEN.md`, `BACKLOG.md` — VIER Dokumente**, so nennt sie der Eröffnungstext in `UMZUG.md` Abschnitt 6. *Am 20.09. wurde dieselbe Zahl dreimal über sechs Dokumente gerechnet und war dreimal falsch.* **Lies die Menge dort nach, bevor du rechnest** — ⚠️ *Nachtrag TB-68, 20.09.2026: seither sind es **FÜNF**, `UMZUG.md` ist dazugekommen; die Zahl „VIER“ oben ist überholt, das Nachlesen gilt* |
| **6** | Kollisionsprobe über **beide** Dateien: Blockbezeichner und K-Nummern, jede genau einmal. ⚠️ **Muster `^\| \*\*(K\d[a-z])\*\*` ohne schliessenden Balken, kein `sort -u`** — siehe TB-62 Abschnitt 5 |
| **7** | Verweise auf `2t`–`2y` im `docs/`-Baum: wie viele, und stimmen sie noch |
| **8** | Nichts ausserhalb `docs/` geändert |

---

## 7. Die harten Auflagen

| | |
|---|---|
| ⛔ | **Nichts wird gelöscht.** Jede Zeile steht zeichengleich in der neuen Datei |
| ⛔ | **Blockbezeichner bleiben unverändert** |
| ⭐ | **Sichern nach jedem fertigen Teil** — vier Commits sind oben benannt |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block** |
| ⭐ | **Jede Zahl im Bericht ist gezählt und gegen eine zweite Zählung gehalten** |
| ⚠️ | **Widersprich diesem Auftrag, wo er falsch ist.** Er beruht auf dem Stand `e5720ed`, vor TB-62 |

---

## 8. Was diese Aufgabe NICHT tut

| | |
|---|---|
| ⛔ | **Abschnitt 2 aufräumen.** Mit 107 135 B der grössere Posten — aber eine eigene Entscheidung, weil dort Aktives und Erledigtes vermischt sind und ein falscher Griff etwas Laufendes trifft |
| ⛔ | **Inhalte der Epics ändern, kürzen oder bewerten** |
| ⛔ | **An `research/` oder am Register arbeiten** |
| ⛔ | **TB-61 berühren** |

---

## In einfacher Sprache

**Was wir wissen wollten:** Warum muss jede neue Sitzung 225 Kilobyte
Aufgabenliste lesen, bevor sie anfangen kann?

**Was herauskam:** Fast ein Drittel davon sind fünf grosse Vorhaben, die
ausdrücklich erst nach dem signierten Tag stattfinden — sie sagen das selbst in
ihrem ersten Satz. Sie entscheiden heute nichts und werden trotzdem jedes Mal
mitgelesen.

**Was diese Aufgabe macht:** Sie zieht die fünf in eine eigene Datei um, die nur
aufgeschlagen wird, wenn es wirklich um sie geht. Im Backlog bleibt eine
Tabelle, die sagt, wo sie stehen.

**Was du davon hast:** Jede künftige Sitzung startet um rund 65 Kilobyte
billiger. **Und es geht nichts verloren** — jede verschobene Zeile wird
maschinell dagegen geprüft, dass sie zeichengleich am neuen Ort steht, so wie
beim Archiv.

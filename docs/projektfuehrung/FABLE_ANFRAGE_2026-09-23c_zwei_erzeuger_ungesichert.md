# Anfrage an Fable 5.1 — 23.09.2026, 10:35: Weg (A) steht im Code, deine Bedingung ist messbar — und deine Schreibregel ist an **zwei von vier** Erzeugern nicht umgesetzt

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD zur Messzeit:** `40bda97` (nach TB-90)

**Sichtschutz:** Codefundstellen, Testausgänge, Zählungen — 27.2. ⛔ Keine
`dd_benchmark`- oder `dd_toleranz`-Werte; der Tabellenvergleich wird dir nur als
„gleich" oder „an Stelle X verschieden" gemeldet.

---

## 1. ⭐⭐ TB-90 ist durch — und deine Unsicherheit aus 22h ist ausgeräumt

**Weg (A) steht im Code.** `faltenplan.py`, in `_plan`, bei der Rollenzuweisung;
`numstat 2 0`. Die drei Sperrlisten-Tabellen unverändert.

| | gemessen, auf dem Mac mit `trading-env` |
|---|---|
| **A1** | ⭐ **9/9** Bots tragen `2026-01-01/2026-09-01` — die Zahl aus 35.1 |
| **A2** | je Bot **ein** Faltenname ersetzt; gemeinsame Falten ungleich **0**, übrige Planfelder ungleich **0**, an der umbenannten Falte ausser dem Namen ungleich **0** |
| **A3** | `selektionsfalten` bei allen neun **ohne** Spanne — genau dein Argument aus 22h |
| **A5** | **dieselbe** Abbruchstelle wie vorher, Belege bis auf die Kopfzeile zeichengleich |
| ⭐⭐ **A6** | **163 / 2 — vorher wie nachher, dieselben zwei (`G6`, `H3`), keine dritte** |

⇒ ⭐ **Deine Unsicherheit** (*„ob `test_vorregistrierung.py` eine Prüfung
enthält, die den Faltennamen der Bestätigungsfalte als Jahr erwartet — dann wird
sie unter (A) rot"*) **ist gemessen beantwortet: nein.**

⭐ **Und die Kosten sind strukturell erledigt:** neun Importe statt neun Kopien;
die Mutationsprobe (Wert nur im Modul verstellt) zeigt, dass **alle neun**
mitziehen, und neun Backtests vorher/nachher sind **byte-identisch**.

## 2. ⭐⭐ Deine Bedingung aus 23b ist jetzt scharf messbar

**Block C, nach Weg (A), je Bot und Tabelle:**

| | `_tb72.json` | `_vt.json` |
|---|---|---|
| **Selektionsfalten** | ⭐⭐ **gleich bei allen NEUN** | bei `t3_supertrend` Übermenge, sonst gleich |
| **Bestätigungszeile** | verschieden bei allen neun | verschieden bei allen neun |

⇒ **Alle achtzehn Zeilen stehen auf „verschieden" — ausschliesslich wegen der
Bestätigungszeile.** Genau der Zustand, für den du **(ii)** entschieden hast.

⭐ **Damit ist deine Determinismusbedingung nicht nur eine Regel, sondern eine
scharfe Probe:** Die Neurechnung darf **genau eine Zeile je Bot** verändern.
Jede weitere Abweichung ist ein Befund mit Bot, Falte und Feld.

⭐ **Und deine zweite Unsicherheit ist ebenfalls beantwortet:** `benchmark.py`
übernimmt den Faltennamen **aus dem Plan** (`eintrag["falten"][f["name"]]`,
per AST geprüft: genau **eine** Zuweisung an dieser Stelle). Es bildet keinen
eigenen Namen. ⇒ **`benchmark.py` muss für (A) nicht geändert werden** — jedenfalls
nicht deswegen. Siehe Abschnitt 3.

---

## 3. ⚠️⚠️ Der Befund: deine Schreibregel 36.1 ist an **zwei von vier** Erzeugern nicht umgesetzt

**Beim Vorbereiten der Neurechnung haben wir gemessen, wer im
Vorregistrierungs-Zweig nach `ergebnisse/` schreibt:**

| Erzeuger | Einmal-Schreibsperre (36.1 (2)) | Voreinstellung (36.1 (3)) |
|---|---|---|
| `faltenplan.py` | ✔ `O_CREAT\|O_EXCL` | ✔ Zeitstempel (TB-86) |
| `sperrliste_abbild.py` | ✔ `O_CREAT\|O_EXCL` | ✔ `--ziel` (TB-85) |
| ⛔ **`benchmark.py`** | **keine** — `open(ziel, "w")` | ⛔⛔ **`ergebnisse/benchmark_drawdowns.json` — Sperrlistenpunkt 4** |
| ⛔⛔ **`messgroessen.py`** | **keine** — `open(ziel, "w")` | ⛔⛔ **fest verdrahtet, KEIN `--ziel`**; Ziel `ergebnisse/messgroessen.json` steht in `EINGEFROREN` |

### (a) `benchmark.py` — die Falle, die ihr Kommentar selbst beschreibt

```python
# --ziel (TB-61): … Ohne Angabe die registrierte Datei - unveraendertes Verhalten.
# … Register 21.9 haelt benchmark_drawdowns.json byteweise fest, und ohne
# diesen Schalter ueberschriebe jeder Lauf sie.
"--ziel", default=os.path.join(_HIER, "ergebnisse", "benchmark_drawdowns.json")
```

⚠️ **Der Kommentar nennt die Gefahr und lässt die Voreinstellung stehen.** Ein
`python3 benchmark.py` ohne Argument überschreibt Sperrlistenpunkt 4. ⭐ *Das ist
dieselbe Lage wie bei `faltenplan.py` am 22.09. — sie hält nur, weil niemand den
Befehl tippt.*

⇒ ⭐ **Der Betreiber hat die Absicherung freigegeben; TB-91 macht sie vor der
Neurechnung, nach dem Muster von TB-86.** Der Hash von `benchmark.py` ändert
sich dabei — planmässig nach 37.3.

### (b) ⚠️⚠️ `messgroessen.py` — schlimmer, und wir fassen es nicht an

`messgroessen.py:283` schreibt **fest verdrahtet** nach
`ergebnisse/messgroessen.json` — **ohne Schalter, ohne Sperre**. Es gibt keinen
Weg, den Lauf auszuweichen; wer es aufruft, überschreibt.

⚠️ **Und das Ziel ist Abschnitt-0-eingefroren** (`herkunft.py::EINGEFROREN`, in
37.4 gemessen).

⚠️ **Du hast `messgroessen.py` in 22h ausdrücklich stehen lassen:** *„bleibt, wie
es ist (eingefroren), mit Tatsachennotiz"*. Das bezog sich auf `GEBUEHR_PCT` —
**auf die Schreibsperre bezog es sich nicht**, und wir deuten es nicht.

### Die Frage

| | |
|---|---|
| **(1)** | Gilt 36.1 für **jeden** Erzeuger im Laufbereich, also auch für `messgroessen.py`? ⭐ Wir lesen deinen Text so (*„Kein Programm im Repo schreibt an einen Pfad, der auf dieser Liste steht oder für sie bestimmt ist"*) — aber dann muss eine eingefrorene Datei geändert werden, und das entscheidest du |
| **(2)** | Falls ja: vor dem Tag, mit Freigabe und Tatsachennotiz (37.3)? Oder reicht es, den **Aufruf** zu sperren und die Datei stehen zu lassen? |
| **(3)** | Falls nein: Was schützt `ergebnisse/messgroessen.json` dann — ausser dass niemand den Befehl tippt? |

⭐ *Wir neigen zu (1) mit (2) „ändern": Eine Regel, die den einen Erzeuger
erfasst und den anderen nicht, weil dessen Datei älter ist, schützt den
schwächeren Punkt nicht. Aber dein Satz aus 22h steht dagegen, und deshalb
fragen wir.*

---

## 4. ⚠️ Eine Berichtigung an uns

Wir schrieben im TB-90-Auftrag, die Sonde melde nach Weg (A) **einen zweiten
Befund**. ⚠️ **Gemessen: derselbe Befund an Punkt 2, nur mit neuem Ist-Hash.**
Das Abbild trägt noch den Stand **vor** TB-86; seit `4daa254` weicht
`faltenplan.py` ab — der erste Anwendungsfall von 37.3. Die **Zahl** der Befunde
ist unverändert (1 in Ordnung, 1 Befund, 12 nicht prüfbar, (ii) `0`).

---

## 5. Was auf dich wartet

| | |
|---|---|
| ⭐ ohne Antwortbedarf | Weg (A) im Code, A1–A6 bestanden, keine dritte rote Prüfung · Kosten strukturell erledigt · `_tb72` Selektionsfalten 9/9 gleich · `benchmark.py` bildet keinen eigenen Faltennamen |
| ⚠️⚠️ **Entscheidung** | Abschnitt 3: Gilt 36.1 auch für `messgroessen.py` — und wenn ja, darf die eingefrorene Datei dafür geändert werden? |

---

## In einfacher Sprache

**Die Umbenennung des Bestätigungszeitraums ist im Programm, und sie ist sauber:**
Alle neun Bots tragen den richtigen Namen, bei jedem hat sich genau dieser eine
Name geändert, und das Prüfprogramm bricht an derselben Stelle ab wie vorher —
keine einzige Prüfung ist durch die Änderung rot geworden. Damit ist die Sorge
des Verfahrensprüfers gegenstandslos.

**Beim Vorbereiten des nächsten Schritts kam aber etwas heraus.** Vor zwei Tagen
wurde eine Regel beschlossen: Kein Programm darf eine geschützte Datei
überschreiben, und jedes muss sich weigern, wenn die Zieldatei schon existiert.
⚠️ **Gemessen sind von vier solchen Programmen nur zwei abgesichert.** Eines
davon — das die Vergleichstabelle rechnet — zielt voreingestellt genau auf die
geschützte Datei, und in seinem eigenen Kommentar steht, dass jeder Lauf sie
überschreiben würde. Das wird jetzt repariert.

⚠️ **Das vierte Programm ist der unangenehmere Fall:** Es schreibt fest auf einen
geschützten Pfad und hat nicht einmal die Möglichkeit, woanders hinzuschreiben.
Es zu reparieren hiesse, eine eingefrorene Datei zu ändern — und ob das vor dem
Stichtag zulässig ist, entscheidet der Verfahrensprüfer, nicht wir.

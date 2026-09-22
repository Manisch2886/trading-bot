# Anfrage an Fable 5.1 — 22.09.2026, 09:35: unsere Klassifikation war an drei Stellen falsch — und die Sperrliste nennt Werte, deren Ort sie nicht nennt

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD zur Messzeit:** `082c7b1` (TB-85 Schritt 0/1)

⚠️ **Du hast unsere Zahlen in der Hand** — sie stehen in Anfrage 22c Abschnitt 3
als Grundlage deiner Sondenentscheidung. **Drei davon sind falsch.**

**Sichtschutz:** Codefundstellen, Registerzitate, Zählungen — 27.2.

---

## 1. ⚠️ Berichtigung: unsere Vorarbeit war zu optimistisch

**Gemessen von der TB-85-Sitzung** (Beleg `docs/belege/TB-85/schritt1_klassifikation.txt`,
mit ausgeschriebenen Leseregeln R1–R6), **gegen unsere Vorarbeit:**

| | wir sagten | ⚠️ gemessen |
|---|---|---|
| **V1** | Punkte **1, 2, 5, 8** allein über Datei-Hashes prüfbar — **vier** | ⚠️ **nur 2 und 5 — zwei.** Punkt 1 nennt zusätzlich *„Abschnitt 3 dieses Registers"*; Punkt 8 zusätzlich *„vier Jahre Vorlauf je Symbol"* (laut Notiz ersetzt, steht aber zeichengleich im Punkt) |
| **V2** | Punkte **6, 11, 12** meinen *„eine Funktion, nicht die Datei"* — kein Pfad | ⚠️ **Falsch gelesen.** `benchmark.py::bh_tagesrenditen`, `herkunft.py::register()`, `herkunft.py::datenstand()` **nennen die Datei ausdrücklich** — sie wird gehasht, nur die Funktion bleibt unmessbar ⇒ `herkunft.py` ist der **zehnte** Pfad (wir sagten neun) |
| **V3** | Punkt **14** meint *„einen Docstring, nicht die Datei als ganze"* | ⚠️ Dieselbe Sache: `auswertung.py` ist genannt und wird gehasht; der Docstring-Anteil bleibt unmessbar |

**Bestätigt** wurden dagegen: Punkt **7** (nur Konstanten), Punkt **9** (keine
Datei), Punkt **13** (reiner Registertext) und dass
`benchmark_drawdowns_vt.json` in **keinem** der 14 Punkte vorkommt
(`grep -c` auf die Zeilen 822–871 = **0**).

### ⇒ Die berichtigte Bilanz

| | Punkte | Anzahl |
|---|---|---:|
| ⭐ rein dateibezogen (Sonde → **0**) | **2, 5** | **zwei** |
| ⚠️ Datei **plus** Unmessbares (Sonde → **2**) | 1, 3, 4, 6, 8, 10, 11, 12, 14 | **neun** |
| ⚠️⚠️ **keine Datei** (Sonde → **2**) | 7, 9, 13 | **drei** |
| | **eindeutige Dateipfade** | **zehn** |

⇒ ⭐ **Erwarteter Nullpunkt-Lauf: 0 Punkte mit `1`, zwölf mit `2`, zwei mit
`0` — Gesamtrückgabe `2`.** ⚠️ **Nicht `0`.** Das ist kein Fehler, sondern der
gemessene Zustand des Registertexts.

---

## 2. ⚠️⚠️ Der neue Befund: die Kosten stehen an zehn Stellen im Code — der Registertext nennt keine davon

**Sperrlistenpunkt 9, zeichengleich:**

> *„Kosten (0,30 %) und Fill-Konvention — `TRADING_FEE_PCT = 0,1` und `SLIPPAGE_PCT = 0,05` je Order, Ein- und Ausstieg; Einstieg zum Schlusskurs des Bestätigungsbalkens"*

**Gemessen von der Sitzung:**

| Konstante | wo sie tatsächlich steht |
|---|---|
| `TRADING_FEE_PCT = 0.1` | ⚠️ **`strategies/*/forward_test.py`** — bei neun Bots |
| `SLIPPAGE_PCT = 0.05` | `research/vorregistrierung/messgroessen.py:59` |

⇒ ⚠️⚠️ **Der Registertext nennt keinen dieser Orte.** Er nennt den **Wert**, nicht
die Stelle.

⭐ **Die Sitzung hat daraus die richtige Folge gezogen, wörtlich:** *„die Sonde
erfindet keinen"* — sie trägt für Punkt 9 **keinen Pfad** ein und meldet ihn mit
`2`.

⚠️ **Die Folge, die uns Sorge macht, und die deine ist:** Ändert jemand
`TRADING_FEE_PCT` in einer der neun `forward_test.py`, **merkt es kein
Sperrlistenpunkt.** Die Kosten sind als Zahl registriert, aber an keiner Datei
verankert. Dasselbe gilt für Punkt **7** (`CLUSTER_SCHWELLE`,
`N_HISTORISCH_JE_BOT` — beide gemessen in `registerdaten.py:99` und `:115`,
**im Punkt nicht genannt**).

⇒ ⭐ **Zwölf von vierzehn Punkten liefern `2` nicht, weil die Sonde schlecht
gebaut ist, sondern weil der Registertext an diesen Stellen nichts Messbares
enthält.** Das ist der Befund, den dein `2` sichtbar machen sollte — und er ist
grösser, als wir gedacht hatten.

**Wir schlagen nichts vor.** Drei Wege sind denkbar (Ort je Punkt nachtragen ·
Werte in **eine** Datei ziehen und die sperren · es so lassen und die Lücke als
Tatsachennotiz führen), und die Wahl ist Verfahren vor dem Tag, nicht Handwerk.

---

## 3. Was auf dich wartet

| | |
|---|---|
| ⚠️ **Zur Kenntnis** | unsere drei Fehler (Abschnitt 1) — deine Sondenentscheidung ruht nicht darauf, aber deine Erwartung an ihr Ergebnis schon |
| ⚠️⚠️ **Zur Entscheidung** | Abschnitt 2 — die Punkte 7 und 9 registrieren Werte ohne Ort |
| ⭐ **läuft** | TB-85: Abbild, Sonde, Selbstprüfung, Nullpunkt-Lauf. Die drei Sperrlisten-Hashes sind vor Beginn gemessen und stimmen alle |

---

## In einfacher Sprache

Zwei Dinge.

**Erstens ein Eingeständnis:** Unsere Aufstellung von heute Morgen, die Fable als
Grundlage bekommen hat, war an drei Stellen falsch — wir hatten vier Punkte als
„einfach prüfbar" gezählt, **gemessen sind es zwei**. Der Grund ist banal: Wir
hatten Kleingedrucktes überlesen (ein Punkt verweist zusätzlich auf einen
Abschnitt des Regelwerks, ein anderer auf eine Zusatzregel) und eine Schreibweise
falsch gedeutet. Die ausführende Sitzung hat es nachgemessen und uns berichtigt —
genau dafür stand die Nachmess-Pflicht in ihrem Auftrag.

**Zweitens ein Fund, der schwerer wiegt:** Die Schutzliste nennt bei zwei Punkten
**Zahlenwerte, aber nicht, wo sie stehen**. Die Handelskosten zum Beispiel stehen
tatsächlich in **zehn** Programmdateien — und keine davon wird von der Schutzliste
genannt. Ändert jemand eine davon, fällt es nirgends auf.

⭐ Die ausführende Sitzung hat sich korrekt verhalten: Sie trägt keinen Ort ein,
den das Regelwerk nicht nennt — **sie erfindet nichts**. Aber damit meldet das
neue Prüfprogramm bei **zwölf von vierzehn** Punkten „nicht prüfbar". Das ist
kein Mangel des Prüfprogramms, sondern die ehrliche Auskunft darüber, wie viel
von der Schutzliste sich heute überhaupt maschinell nachprüfen lässt.

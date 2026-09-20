# TB-68 Der Eröffnungstext steht zweimal — und die zwei Fassungen widersprechen sich

**an: Claude Code am Mac (lokale Sitzung)**

**Sitzungstitel für Claude Code: `TB-68 Eroeffnungstext`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main`.

⭐ **Rechnet nicht.** Klein, aber er behebt einen Fehler, der jede neue Sitzung
trifft.

---

## 0. Warum es diese Aufgabe gibt — gemessen am 20.09.2026, 16:05

**Der Eröffnungstext — der Text, den eine neue Sitzung als Erstes liest — steht
an zwei Stellen. Und die beiden Fassungen sind nicht gleich.**

| | `UMZUG.md` Abschnitt 6, Z. 228 ff. | `UEBERGABE_2026-09-19.md` Block 9, Z. 286 ff. |
|---|---|---|
| Zahl der Dokumente | **vier** | **fünf** |
| `UMZUG.md` selbst | ⛔ **fehlt** | ✅ als Nr. 2, mit dem Hinweis *„Abschnitt 10 ist überholt"* |
| Übergabe | `UEBERGABE_<datum>.md` (Platzhalter) | `UEBERGABE_2026-09-19.md` (fest) |

⚠️⚠️ **Das ist keine Kopie mehr, sondern ein Widerspruch.** Welche Sitzung welche
Fassung bekommt, hängt davon ab, wo der Betreiber gerade nachsieht.

⚠️⚠️ **Und beide tragen denselben Fehler:** Zeile 3 bzw. 4 lautet
`projektfuehrung/PRUEFPRINZIPIEN.md`. **Die Datei liegt in `docs/`, nicht in
`docs/projektfuehrung/`** — sie hat dort nie gelegen (über alle Commits
gemessen: 0 Treffer). ⭐ **Ein zweites Projekt, das sich das Regelwerk ziehen
sollte, ist am 20.09. genau daran gescheitert** und hat gemeldet, es finde die
Datei nicht.

⚠️ **Dasselbe gilt für `docs/UEBERGABEPROTOKOLL.md`** — ebenfalls eine Ebene
höher, in keinem der beiden Texte genannt.

⭐⭐ **Die Folge, die das teuer macht:** Die Pflichtlektüre wurde am 20.09.
**viermal** gerechnet und **dreimal falsch**, weil niemand wusste, welche Menge
gilt. *Ein Text, der festlegt, was zu lesen ist, darf nicht zwei Fassungen
haben.*

---

## 1. ⛔ Was diese Aufgabe NICHT tut, obwohl es im Backlog stand

**Die geplante zweite Hälfte ist gegenstandslos.** Der Auftrag sollte auch
*„«In einfacher Sprache» steht an vier Stellen"* beheben. **Nachgemessen am
20.09., 16:05:**

| Fundstelle | was es ist |
|---|---|
| `ARBEITSWEISE.md` Abschnitt **4** | die Regel für den **Abschluss** |
| `ARBEITSWEISE.md` Abschnitt **17** | die Regel für den **Einstieg** — ausdrücklich gegen Abschnitt 4 abgegrenzt |
| `ARBEITSWEISE.md` Z. 138, 738 | Verweise auf Abschnitt 4 |
| `DOKUMENTATIONSSTANDARD.md` Z. 150, 168 | ⭐ **Verweise** auf `ARBEITSWEISE.md §4` — keine Kopie |
| `UMZUG.md` Z. 267 | ⭐ die **Anwendung** der Regel im Dokument selbst |

⇒ **Es gibt keine Kopie.** ⛔ **Nichts daran ändern.**

*Festgehalten, weil die Behauptung aus einer Chat-Messung stammt, die ein zu
grobes Muster benutzt hat — dieselbe Familie wie `K4a` und `K4d`.*

---

## 2. Was zu tun ist

### Schritt 0 — vor allem anderen

**Committe, was im Arbeitsbaum liegt.** Nachweis „sauber" wird **danach**
geprüft.

### Schritt 1 — messen, welche Fassung gilt

⚠️ **Nicht raten, welche die richtige ist.** **Miss:**

1. Welche Dokumente nennt jede Fassung, in welcher Reihenfolge?
2. ⭐ **Welche Fassung hat der Betreiber zuletzt tatsächlich benutzt?**
   `UMZUG.md` Abschnitt 4 beschreibt das Umzugsverfahren — **sieh nach, welche
   Fassung es als die maßgebliche bezeichnet.**
3. Welche Dateien liegen wirklich wo? **Prüfe jeden der genannten Pfade einzeln
   mit `test -f`** und berichte das Ergebnis je Zeile.

**Sichern: commit und push.**

### Schritt 2 — eine Fassung, ein Ort

⭐ **`UMZUG.md` Abschnitt 6 ist die maßgebliche** — das Dokument heißt *„Umzug
in einen neuen Chat — das Verfahren"*, und ein Verfahrenstext gehört in das
Verfahrensdokument.

⚠️ **Widerspricht dein Messergebnis aus Schritt 1 dieser Zuordnung, gilt deine
Messung** — dann sag es und begründe.

**In `UEBERGABE_2026-09-19.md` Block 9 steht danach kein zweiter Text mehr,
sondern ein Verweis** — nach `DOKUMENTATIONSSTANDARD.md` Regel 9: *was abgelöst
wird, wird entfernt, nicht danebengestellt.*

⚠️ **Die Übergabe ist keine der vier Ausnahmen von Regel 9** (das sind Register,
`JOURNAL.md`, Backlog-Abschnitt 8, `PRUEFPRINZIPIEN.md`). **Der Block darf
gekürzt werden.**

### Schritt 3 — die Pfade berichtigen

**In der bleibenden Fassung:**

| | |
|---|---|
| `projektfuehrung/PRUEFPRINZIPIEN.md` | ⇒ **`PRUEFPRINZIPIEN.md`** (liegt in `docs/`) |
| ⚠️ `docs/UEBERGABEPROTOKOLL.md` | **prüfen, ob es in den Lesepfad gehört.** Es trägt Betriebswissen (Cronjobs, Neustarts, Schlüsselbund). ⛔ **Nicht selbst entscheiden** — messen, wie oft es in den letzten Sitzungen gebraucht wurde, und vorlegen |
| ⚠️ `UEBERGABE_<datum>.md` gegen `UEBERGABE_2026-09-19.md` | Der Platzhalter ist robuster, der feste Name eindeutig. **Beide Formen benennen, empfehlen, nicht entscheiden** |

⭐ **Der Text sagt künftig ausdrücklich, dass er die verbindliche Fassung ist** —
ein Satz genügt.

**Sichern: commit und push.**

### Schritt 4 — die dritte Fassung suchen

⚠️ **Zwei Fassungen wurden gefunden, weil jemand danach gesucht hat.** ⭐ **Such
nach weiteren:** `Lies in dieser Reihenfolge`, `Neue Sitzung zum
Trading-Bot-Projekt`, `Das Projekt "Trading Bots" ist angehängt` — im ganzen
`docs/`-Baum **und** in `logs/auftraege/`.

**Nenne die Trefferzahl je Muster, auch wenn sie null ist** (`A1`).

**Sichern: commit und push.**

### Schritt 5 — eine Zeile im Backlog und die Abgabe

**Eine** Zeile in Abschnitt 4 mit gemessener K-Nummer (Muster
`^\| \*\*(K\d[a-z])\*\*` **ohne schliessenden Balken**, **kein `sort -u`**), dann
`docs/ERGEBNIS_TB-68_eroeffnungstext.md` und ein Journal-Nachtrag
⭐ **mit der Quellenzeile aus TB-67**, falls TB-67 schon gelaufen ist.

**Sichern: commit und push.**

---

## 3. Die Nachweise

| # | Nachweis |
|---:|---|
| **1** | `git status --short` vor dem ersten Schreiben |
| **2** | ⭐ Die beiden Fassungen aus Schritt 1, **Zeile für Zeile gegenübergestellt** |
| **3** | ⭐ Jeder genannte Pfad einzeln mit `test -f` geprüft, Ergebnis je Zeile |
| **4** | Schritt 4: Trefferzahl je Suchmuster, **auch die Nullen** |
| **5** | `git diff --numstat` je Datei; für die Übergabe ist Spalte zwei **nicht** null — die Kürzung wird einzeln begründet |
| **6** | Was du dem Betreiber vorlegst statt es zu entscheiden (Schritt 3) |
| **7** | Nichts ausserhalb `docs/` geändert |

---

## 4. Die harten Auflagen

| | |
|---|---|
| ⛔ | **„In einfacher Sprache" bleibt unangetastet** — Abschnitt 1 |
| ⛔ | **Nicht entscheiden, ob `UEBERGABEPROTOKOLL.md` in den Lesepfad gehört** — messen und vorlegen |
| ⭐ | **Sichern nach jedem fertigen Teil** |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block** |
| ⚠️ | **Widersprich diesem Auftrag, wo er falsch ist.** ⭐ *Die letzten fünf Aufträge lagen je an mehreren Stellen daneben, und jedes Mal hatte die ausführende Sitzung recht* |

---

## In einfacher Sprache

**Was schiefgelaufen ist:** Der Text, den jede neue Sitzung als Allererstes
liest, steht an zwei Stellen — und die beiden sagen inzwischen etwas
Verschiedenes. Die eine nennt vier Dokumente, die andere fünf.

**Und beide schicken die Sitzung an eine Stelle, an der eine der Dateien nicht
liegt.** Genau daran ist heute ein zweites Projekt gescheitert, das sich das
Regelwerk ziehen sollte: Es hat die Prüfprinzipien nicht gefunden — die Datei
liegt eine Ebene höher, als der Text behauptet.

**Was diese Aufgabe macht:** Sie lässt eine Fassung stehen, korrigiert die
Pfade, und ersetzt die zweite durch einen Verweis. Und sie sucht, ob es noch
eine dritte gibt.

**Was du danach entscheidest:** Ob das Betriebshandbuch mit in die Leseliste
gehört. Die Aufgabe misst, wie oft es zuletzt wirklich gebraucht wurde, und legt
es dir vor.

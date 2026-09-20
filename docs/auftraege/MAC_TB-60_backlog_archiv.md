# TB-60 Backlog-Archiv — an: Claude Code am Mac (lokale Sitzung)

**Sitzungstitel für Claude Code: `TB-60 Backlog-Archiv`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main` — kein Zweig, kein PR
(Regelweg für Dokumentation, `ARBEITSWEISE.md` Abschnitt 5b).

⚠️ **Setzt TB-59 voraus.** Der Arbeitsbaum muss committet sein, bevor diese
Aufgabe beginnt — siehe Schritt 0.

---

## 0. Warum es diese Aufgabe gibt — gemessen, nicht vermutet

**`BACKLOG.md` ist nach TB-59 auf 1 959 Zeilen und 350 403 Bytes gewachsen und
macht damit 75,7 % der Pflichtlektüre jeder neuen Sitzung aus** (Summe der sechs
Dokumente aus dem Eröffnungstext: 462 594 Bytes).

**Gemessen am 20.09.2026, was darin nichts mehr entscheidet:**

| | Bytes | Anteil |
|---|---:|---:|
| Abschnitte `2b` bis `2r` — Rückblicke auf erledigte Aufgaben TB-34 bis TB-55 | 110 052 | 31,4 % |
| ERLEDIGT-Zeilen in Abschnitt 2 (neun Stück) | 14 120 | 4,0 % |
| Abschnitt 9 „Arbeitsregeln" — inhaltlich Doppel zu `ARBEITSWEISE.md` | 5 946 | 1,7 % |
| Abschnitt 6 „Geparkt, null Arbeit" | 1 122 | 0,3 % |
| **zusammen** | **131 240** | **37,5 %** |

⭐ **Die Datei verlangt das selbst.** Ihre zweite Zeile lautet seit jeher: *„Nur
**aktive Punkte**. Alles Abgeschlossene steht im `JOURNAL.md` und wird von dort
**nicht** zurückgeholt."* **Diese Regel wird seit Wochen gebrochen.**

⚠️⚠️ **Betreiberentscheidung 20.09.2026:** Archiv anlegen, **mit
Verschiebenachweis**.

---

## 1. ⭐⭐ Die Beweisregel für diese Aufgabe — sie ersetzt „null entfernte Zeilen"

**Das Projekt weist Dokumentationsarbeit sonst über `numstat`-Spalte zwei = 0
nach. Hier wird verschoben, also greift diese Null nicht. Sie wird durch eine
schärfere ersetzt:**

> ⭐ **Jede aus `BACKLOG.md` entfernte Zeile erscheint zeichengleich in
> `BACKLOG_ARCHIV.md`.**
>
> **Nachweis, zwingend:**
> 1. `git diff` auf `BACKLOG.md`, alle entfernten Zeilen (`^-`) in eine Datei
>    geschrieben, Steuerzeichen abgezogen;
> 2. dieselben Zeilen aus `BACKLOG_ARCHIV.md` gezogen;
> 3. **`diff` der beiden muss leer sein** — das Ergebnis wörtlich in den
>    Bericht;
> 4. **Summe über beide Dateien: entfernte Zeilen minus hinzugefügte
>    Archivzeilen = 0**, abzüglich der im Archiv neu geschriebenen
>    Überschriften und Verweiszeilen, die einzeln aufzuführen sind.

⚠️ **Ein Vertrauen auf „ich habe es kopiert" genügt nicht.** *Grund: Am
19.09.2026 hat ein Ablagewerkzeug „written" gemeldet und die Datei nicht
verändert.*

---

## 2. Was verschoben wird

**Ziel: `docs/projektfuehrung/BACKLOG_ARCHIV.md`** (neu).

| # | Was | Was in `BACKLOG.md` zurückbleibt |
|---:|---|---|
| **1** | **Abschnitte `2b` bis `2r` vollständig** | ⭐ **Je Abschnitt genau eine Zeile** in einer Sammeltabelle: Bezeichner, Titel, Datum, Verweis ins Archiv |
| **2** | **Die neun ERLEDIGT-Zeilen aus Abschnitt 2** — gemessen: `TB-36`, `T36.5`, `TB-38`, `TB-39`, `TB-40`, `TB-41`, `TB-42`, `TB-43`, `TB-44`. ⚠️ **Miss sie selbst nach, verlass dich nicht auf diese Liste** | Je Zeile **ein Einzeiler**: *„`TB-40` erledigt 16.09.2026, PR #113 — Befunde im Archiv"* |
| **3** | **Abschnitt 6 „Geparkt, null Arbeit"** | Eine Zeile mit Verweis |
| **4** | **Abschnitt 9 „Arbeitsregeln"** | ⚠️ **Kein Archiveintrag, sondern ein Verweis auf `ARBEITSWEISE.md`** — der Inhalt ist dort bereits geführt. ⭐ **Vorher prüfen und berichten, ob Abschnitt 9 etwas enthält, das in `ARBEITSWEISE.md` NICHT steht.** Findest du so etwas: **melden, nicht löschen** — es wandert dann ins Archiv statt in den Verweis |

### ⛔ Was ausdrücklich NICHT verschoben wird

| | |
|---|---|
| ⛔ | **Abschnitt 8 „Gestrichen"** (1 990 B). Er verhindert, dass verworfene Ideen erneut vorgeschlagen werden, und hat sich am 19.09. zweimal bewährt. **Er bleibt vollständig, wo er ist** |
| ⛔ | **Abschnitte 0, 1, 3, 4, 5, 7** und die aktiven Punkte in Abschnitt 2 |
| ⛔ | **Die neuen Abschnitte `2s` bis `2y`** — sie sind von gestern und aktiv |
| ⛔ | **`PRUEFPRINZIPIEN.md`, `JOURNAL.md`, das Register** — nicht Gegenstand |

---

## 3. Der Kopf von `BACKLOG.md` wird angepasst

⚠️ **Die einzige inhaltliche Änderung ausserhalb des Verschiebens.** Die zweite
Zeile sagt heute, Abgeschlossenes stehe im `JOURNAL.md`. Nach dieser Aufgabe
stimmt das nur noch halb. **Einzufügen unmittelbar darunter:**

```markdown
> ⭐ **Rückblicke auf abgeschlossene Aufgaben stehen in
> `BACKLOG_ARCHIV.md`** (angelegt 20.09.2026, TB-60), Messprotokolle im
> `JOURNAL.md`. **Beide werden nur gelesen, wenn es um eine konkrete
> frühere Messung geht** — diese Datei trägt die aktiven Punkte.
> ⚠️ **Nichts davon ist gelöscht:** jede verschobene Zeile steht
> zeichengleich im Archiv, nachgewiesen in
> `docs/ERGEBNIS_TB-60_backlog_archiv.md`.
```

**Und der Kopf von `BACKLOG_ARCHIV.md` sagt, was es ist:** ein Archiv, das
**nicht** in jede Sitzung gehört, mit dem Datum der Anlage, dem Verweis zurück
auf `BACKLOG.md` und dem Satz, dass hier nichts entschieden wird.

---

## 4. Die harten Auflagen

| | |
|---|---|
| ⚠️⚠️ | **Nur `docs/`.** Nichts ausserhalb. Sperrliste gilt unverändert |
| ⚠️⚠️ | **Kein Wort umformuliert.** Verschoben wird **zeichengleich**. ⭐ *Findest du beim Verschieben einen Sachfehler: melden, nicht korrigieren* |
| ⚠️ | **Keine Nummer neu vergeben, keine Nummer entfernt.** Bezeichner wandern mit ihrem Text; die Kollisionsprobe aus TB-59 muss danach weiterhin aufgehen |
| ⚠️ | **`git status --porcelain` NACH dem letzten Commit** |
| ⛔ | **Kein ZIP, nichts nach `~/Downloads`.** Ergebnisse ins Repo |

---

## 5. Schritt 0 — vor allem anderen

**Im Arbeitsbaum liegt die unfertige TB-59-Arbeit** (gemessen 20.09.2026:
`BACKLOG.md` `1008 / 0`, `ARBEITSWEISE.md` `23 / 67`, `HEAD` = `aa05cc1`).

⚠️ **Ist sie beim Start dieser Aufgabe noch nicht committet, committe sie
zuerst** — als eigenen Commit mit eigener Nachricht, **getrennt** von dieser
Aufgabe. Erst danach beginnt TB-60, und erst danach wird „Arbeitsbaum sauber"
geprüft.

⚠️ **Und TB-59 schuldet noch zwei Dokumente** —
`docs/ERGEBNIS_TB-59_backlog_einarbeitung.md` und
`docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-19g.md`. **Sind sie
nicht da, melde das**, bevor du TB-60 beginnst; hol sie nur nach, wenn du die
Messwerte dafür wirklich hast, und schreibe ausdrücklich dazu, dass sie
nachgeholt wurden (Prüfprinzip A7).

---

## 6. Die Nachweise, die diese Aufgabe schuldet

| # | Nachweis |
|---:|---|
| **1** | `git diff --numstat` je Datei — **hier ist Spalte 2 bewusst nicht 0** |
| **2** | ⭐ **Der Verschiebenachweis aus Abschnitt 1, Punkt 3: der leere `diff`, wörtlich** |
| **3** | **Bytes und Zeilen von `BACKLOG.md` vorher und nachher.** Vorher gemessen: **1 959 Zeilen / 350 403 Bytes** |
| **4** | **Bytes und Zeilen von `BACKLOG_ARCHIV.md`** |
| **5** | ⭐ **Die neue Summe der Pflichtlektüre** — die sechs Dokumente des Eröffnungstextes, vorher **462 594 Bytes** |
| **6** | **Kollisionsprobe wie in TB-59:** jeder Blockbezeichner und jede K-Nummer in `BACKLOG.md` **und** `BACKLOG_ARCHIV.md` zusammen genau einmal |
| **7** | **Befundbericht zu Abschnitt 9:** was darin steht und in `ARBEITSWEISE.md` fehlt |
| **8** | `git status --porcelain` nach dem letzten Commit; nichts ausserhalb `docs/` |

**Ablage:** `docs/ERGEBNIS_TB-60_backlog_archiv.md`, committet. Journal-Nachtrag
als `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-20a.md` —
⚠️ **miss den nächsten freien Buchstaben selbst** (K2i). Am Ende des
Ergebnisdokuments **„In einfacher Sprache"**.

---

## 7. Was diese Aufgabe NICHT tut

| | |
|---|---|
| ⛔ | **Nichts wird gelöscht.** Es wird ausschliesslich verschoben, und das wird bewiesen |
| ⛔ | **Keine neue Regel** über künftige Nachträge. *Der Betreiber hat am 20.09.2026 bewusst die Variante ohne stehende Regel gewählt; das künftige Wachstum bleibt damit offen und ist als Punkt im Backlog vermerkt* |
| ⛔ | **Kein Registertext, kein Amendment, kein signierter Tag** |
| ⛔ | **`JOURNAL.md` wird nicht umgebaut** — nur der Nachtrag kommt dazu |

---

## In einfacher Sprache

**Was zu tun ist:** Die Aufgabenliste des Projekts ist auf 350 KB gewachsen und
macht drei Viertel von dem aus, was jede neue Sitzung lesen muss, bevor sie
etwas tun kann. **Gut 37 % davon sind Rückblicke auf Aufgaben, die längst fertig
sind** — sie kosten in jeder Sitzung Lesezeit und entscheiden nichts mehr.

**Was dagegen getan wird:** Diese Teile ziehen in eine zweite Datei um, die nur
gelesen wird, wenn jemand eine konkrete frühere Messung sucht. In der
Aufgabenliste bleibt je Abschnitt eine Zeile mit einem Verweis.

**Warum das nichts verliert:** Es wird **nichts gelöscht**, nur verschoben — und
das wird bewiesen: Jede Zeile, die aus der einen Datei verschwindet, muss
**zeichengleich** in der anderen auftauchen. Ein maschineller Vergleich der
beiden Mengen muss leer ausgehen. **Das ist ein strengerer Nachweis als die
bisherige Regel „es wurde nichts entfernt"**, weil er beide Seiten prüft statt
nur einer.

**Was ausdrücklich bleibt:** Die Liste der verworfenen Ideen. Sie ist zwei
Kilobyte gross und verhindert, dass jemand in einem halben Jahr etwas
vorschlägt, das schon einmal durchgerechnet und begründet abgelehnt wurde.

---

## 8. Nachgetragen 20.09.2026 — Löschungen, ausdrücklich freigegeben

⚠️ **Betreiberanweisung 20.09.2026** (`DOKUMENTATIONSSTANDARD.md` Regel 9, neu):
Obsolete Informationen ohne Relevanz **dürfen gelöscht werden**. Für diese
Aufgabe gilt das für **genau zwei Dateien**:

| Datei | Nachweis vor dem Löschen |
|---|---|
| `docs/belege/TB-56b/abschnitt_21.md` (269 Z.) | Inhalt steht **wörtlich** als Abschnitt 21 in `docs/VORREGISTRIERUNG_neuselektion.md` |
| `docs/belege/TB-56b/abschnitt_22.md` (204 Z.) | Inhalt steht **wörtlich** als Abschnitt 22 ebenda |

⚠️⚠️ **Vor dem Löschen zwingend nachweisen**, je Datei: Die Datei ist
zeichengleich im Register enthalten — Vergleich der Dateizeilen gegen den
entsprechenden Registerabschnitt, **das Ergebnis muss leer sein**, wörtlich in
den Bericht. **Schlägt der Vergleich für eine Datei fehl, wird sie NICHT
gelöscht**, sondern gemeldet.

⛔ **Sonst nichts löschen.** Alles Übrige dieser Aufgabe wird **verschoben**,
nach der Beweisregel in Abschnitt 1.

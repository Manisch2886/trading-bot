# TB-62 Einarbeitung der Nachträge (m) und (v) — an: Claude Code am Mac (lokale Sitzung)

**Sitzungstitel für Claude Code: `TB-62 Nachtraege m und v`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main` — kein Zweig, kein PR
(Regelweg für Dokumentation, `ARBEITSWEISE.md` Abschnitt 5b).

⭐ **Diese Aufgabe rechnet nicht.** Sie braucht kein `trading-env`, keine
Kursdaten. Sie läuft **parallel zu TB-61** — aber nicht gleichzeitig in
derselben Arbeitskopie.

---

## 0. Warum es diese Aufgabe gibt — gemessen am 20.09.2026 an `28eea5c`

Zwei Nachträge sind nicht eingearbeitet. **Der eine seit einem Tag, der andere
seit zwei — und der ältere hat bereits Schaden angerichtet.**

| Nachtrag | Nummern | Kollisionen mit dem Backlog |
|---|---:|---|
| `BACKLOG_NACHTRAG_2026-09-19v.md` | ⚠️ **selbst zählen** (`K3k` aufwärts) | am 20.09. gemessen: **keine** — nachprüfen |
| `BACKLOG_NACHTRAG_2026-09-19m.md` | **6** (`K2l`–`K2q`) | ⚠️⚠️ **alle sechs** |

### ⚠️⚠️ Der Befund zu (m), und er ist der Grund für diese Aufgabe

**`K2l` bis `K2q` sind im Backlog vergeben — an andere Inhalte.** Die Zeilen
`K2l`–`K2o` tragen dort Punkte aus den Nachträgen **(s)/(t)**, `K2p`/`K2q`
tragen Punkte aus **(n)**. Nachtrag (m) wurde übersprungen, und seine Nummern
sind darüber hinweggewachsen.

**Vier seiner sechs Regeln stehen inhaltlich anderswo** — gemessen mit je
mehreren Mustern:

| aus (m) | Regel | steht in |
|---|---|---|
| `K2l` | Aufträge nie nach `~/Downloads` | `ARBEITSWEISE.md`, `UMZUG.md`, Protokoll |
| `K2m` | jeder Auftrag trägt `[ortsunabhängig]` oder `[Mac-pflichtig]` | Backlog |
| `K2p` | nicht am Repo arbeiten, solange eine Mac-Sitzung läuft | `UMZUG.md` |
| `K2q` | über die Geräteanbindung nur lesend | `ARBEITSWEISE.md` |

⚠️⚠️ **Zwei stehen nirgends im Repo** — mit vier verschiedenen Mustern gesucht,
0 Treffer:

> **(1)** *„Jede Rückfrage an den Betreiber und seine Antwort kommen wörtlich in
> den Bericht — sonst leben sie nur im Sitzungsverlauf, der mit der Sitzung
> verschwindet."*
>
> **(2)** *„Die Sitzung committet ihren eigenen Auftrag mit (`docs/auftraege/`)
> und ihre Belege (`docs/belege/TB-xx/`)."*

⭐⭐ **Regel (1) ist die Pointe dieser Aufgabe: Sie ist genau die Vorschrift, die
verhindern soll, dass Betreiberentscheidungen nur im Chat leben — und sie ist
selbst im Chat geblieben.** *Eine Regel, die ihre eigene Einarbeitung nicht
überlebt hat.*

---

## 1. Die Beweisregel für diese Aufgabe

**Hier wird nur hinzugefügt, nichts verschoben und nichts entfernt.** Es gilt
also wieder die alte Null:

> ⭐ **`git diff --numstat` zeigt für `BACKLOG.md` in Spalte zwei eine `0`.**

⚠️ **Mit einer Ausnahme, die zu nennen ist, falls sie eintritt:** Bemerkst du
beim Einarbeiten, dass ein neuer Punkt einen bestehenden **ablöst**, gilt
`DOKUMENTATIONSSTANDARD.md` Regel 9 — das Abgelöste wird entfernt. **Dann ist
die Null nicht mehr erreichbar, und das ist richtig.** Berichte in dem Fall
jede entfernte Zeile einzeln mit ihrer Begründung.

---

## 2. ⛔ Was dieser Auftrag NICHT vorgibt

**Keine einzige SOLL-Zeilenzahl.** Nicht für `BACKLOG.md`, nicht für den Zuwachs,
nicht für die Zahl der Hunks.

⭐ **Der Grund, gemessen:** In den letzten beiden Aufträgen standen vier Zahlen,
die geschätzt und nicht gezählt waren — `3108/92`, `256`, **`70` entfernte
Zeilen** (es waren 67) und *„drei Doppelbelegungen"* (es waren vier). **TB-59 hat
zweimal der Vorgabe widersprochen und lag beide Male richtig.** Eine Zahl in
einem *Auftrag* liest die ausführende Sitzung als **Anweisung**, nicht als
Schätzung.

⇒ **Du zählst selbst und berichtest, was du gezählt hast.**

---

## 3. Die Schritte

### Schritt 0 — vor allem anderen

**Committe, was im Arbeitsbaum liegt.** Der Nachweis „Arbeitsbaum sauber" wird
**danach** geprüft. Findest du nichts, sag es und mach weiter.

### Schritt 1 — Nachtrag (v) einarbeiten, Nummern unverändert

**Neuer Block am Ende von Abschnitt 2**, unmittelbar **vor** dem Ankertext

```
## 3 — Die Kette (Ränge 1 bis 5)
```

**Überschrift:** `## 2z — Der Sitzungstag 20.09.2026: Start, Dokumentationsregel, Verbindungsabbrüche`

⭐ **`2z` ist gemessen die nächste freie** (höchster Block: `2y`).
⚠️ **Damit ist auch der `2x`-Namensraum erschöpft** — nenne im Bericht, welchen
Bezeichner du für den nächsten Block vorschlägst.

⭐ **Die Nummern ab `K3k` werden UNVERÄNDERT übernommen**, sofern deine eigene
Messung bestätigt, dass keine davon im Backlog oder Archiv belegt ist. Am
20.09.2026 war das der Fall. **Dann kein Vergabevermerk nötig.**

⚠️⚠️ **Der Nachtrag ist am 20.09. mehrfach gewachsen, während dieser Auftrag
schon geschrieben war.** Verlass dich auf keine Nummer und keine Anzahl aus
diesem Dokument — **zähle beides am Nachtrag selbst.**

⚠️ **Prüfe das selbst nach**, bevor du schreibst. Findest du eine Kollision,
vergib neu und setze den Vermerk in der Form aus TB-59:
*„(im Nachtrag (v) als `X` vorgeschlagen; `X` war belegt — vergeben als `Y`,
gemessen)"*.

**Sichern: commit und push.**

### Schritt 2 — die zwei fehlenden Regeln aus (m) an ihren richtigen Platz

⭐ **Sie gehören in `ARBEITSWEISE.md`, nicht ins Backlog** — es sind
Arbeitsregeln, keine offenen Punkte. *Das Backlog führt, was zu tun ist; die
Arbeitsweise führt, wie gearbeitet wird.*

| Regel | Ort |
|---|---|
| **(1)** Rückfrage und Antwort des Betreibers kommen wörtlich in den Bericht | `ARBEITSWEISE.md`, in oder bei **Abschnitt 15** („Was mit ‚zukünftig' gesagt wird") — dort steht schon, dass der Chatverlauf kein Träger ist |
| **(2)** Die Sitzung committet ihren eigenen Auftrag und ihre Belege mit | `ARBEITSWEISE.md`, in oder bei **Abschnitt 14, Regel 3** (sichern nach jedem fertigen Teil) |

⚠️ **Lies beide Abschnitte, bevor du schreibst.** Steht die Regel dort sinngemäss
schon, **schreibe sie nicht zweimal hin** — ergänze den vorhandenen Satz und sag
im Bericht, dass du das getan hast.

**Sichern: commit und push.**

### Schritt 3 — die vier übrigen (m)-Regeln: ein Vermerk, keine Zeilen

**Sie stehen inhaltlich schon im Repo** (Tabelle in Abschnitt 0). ⛔ **Nicht
noch einmal ins Backlog schreiben.**

Stattdessen **eine einzige Zeile** im neuen Block `2z`, die festhält, dass (m)
nachträglich geprüft wurde, welche vier Regeln wo stehen und welche zwei
nachgetragen wurden. ⛔ **Dieser Auftrag nennt die nächste freie K-Nummer bewusst NICHT** — er hat
schon einmal eine genannt, und sie war beim Schreiben richtig und eine halbe
Stunde später falsch. **Miss sie mit dem Muster aus Abschnitt 5.**

**Sichern: commit und push.**

### Schritt 4 — die ZIP-Pflicht abbauen (Betreiberentscheidung 20.09.2026)

**Die Entscheidung, wörtlich:** *ZIP wird überall abgeschafft, nicht nur beim
Umzug. Ergebnisse kommen als Commit im Repo und als einzelne Dateien im Chat,
nie als Archiv.*

⚠️⚠️ **Der Anlass war ein Widerspruch in EINER Datei:**
`ARBEITSWEISE.md` Abschnitt 1 verlangte „Immer gebündelt als ZIP“,
Abschnitt 10 nannte ZIP „überholt“. Beides stand seit dem 19.09. nebeneinander.

#### ⭐ Was NICHT wegfällt — lies das, bevor du löschst

**Fast jede ZIP-Stelle trägt einen Zweck, der bleibt:**

> *Ein Beleg muss die Sitzung überleben.*

**Das Archiv war das Mittel; der Commit ist das neue.** ⭐ **Und er ist das
stärkere:** ein Archiv in `~/Downloads` liegt in keiner Version, ein Commit
schon. *Dieselbe Begründung, aus der TB-59 und TB-60 Arbeit verloren haben.*

⛔ **Also nicht die Sätze streichen, sondern das Mittel austauschen.** Wo steht
„am Ende als ZIP gesichert“, muss künftig stehen: in eine Datei unter `docs/`
geschrieben und committet.

#### Wie du vorgehst

**1. Selbst zählen.** Such in `docs/projektfuehrung/ARBEITSWEISE.md` nach

```
ZIP|Zip|zip|Archiv
```

⛔ **Dieser Auftrag nennt bewusst KEINE Fundstellenzahl** — siehe Abschnitt 2.
Berichte, wie viele du gefunden hast.

**2. Jede Fundstelle einzeln einordnen**, in drei Gruppen:

| Gruppe | Behandlung |
|---|---|
| **A — Vorschrift** (*verlangt ein Archiv*) | Mittel austauschen: Commit statt ZIP. Nach Regel 9 wird der alte Wortlaut **entfernt**, nicht danebengestellt |
| **B — Beispiel oder Redewendung** (*„ich warte auf das Archiv“*) | umformulieren auf den neuen Weg |
| **C — historischer Beleg** (*„ZIP hat immer funktioniert“, Berichtigungsvermerke, Zitate des Betreibers*) | ⛔ **unverändert stehen lassen.** Ein Beleg über die Vergangenheit wird nicht umgeschrieben, wenn sich die Regel ändert — sonst fälscht die Dokumentation ihre eigene Geschichte |

⚠️ **Gruppe C ist die, bei der man sich vergreift.** Im Zweifel: stehen lassen
und im Bericht nennen.

**3. Abschnitt 10 eingrenzen.** Dort steht, das Umzugsverfahren ersetze die
ZIP-Übergabe. **Das ist jetzt kein Sonderfall mehr, sondern die allgemeine
Regel** — der Satz verweist künftig auf Abschnitt 1 statt eine eigene Ausnahme
zu behaupten.

**4. Dieselbe Suche in den übrigen Trägern**: `DOKUMENTATIONSSTANDARD.md`,
`UMZUG.md`, `UEBERGABEPROTOKOLL.md`, `BACKLOG.md`. Gleiche drei Gruppen.
⭐ **Der Anlass dieser Aufgabe war genau, dass zwei Träger auseinanderliefen** —
sie jetzt nur in einem zu berichtigen, wäre derselbe Fehler noch einmal.

**5. Die Aufgabendokumente.** `docs/auftraege/*.md` und `docs/belege/` werden
**nicht rückwirkend** geändert — sie sind Belege über das, was damals galt
(Gruppe C).

**Sichern: commit und push.**

### Schritt 5 — die Abgabe

`docs/ERGEBNIS_TB-62_nachtraege_m_v.md` und ein Journal-Nachtrag.

**Sichern: commit und push.**

---

## 4. Die Nachweise, die diese Aufgabe schuldet

| # | Nachweis |
|---:|---|
| **1** | `git status --short` **vor** dem ersten Schreiben |
| **2** | `git diff --numstat` je geänderter Datei — Spalte zwei bei `BACKLOG.md` erwartet `0`; jede Abweichung einzeln begründet |
| **3** | Zeilenzahl `BACKLOG.md` vorher und nachher, **beide selbst gezählt** |
| **4** | ⭐⭐ **Kollisionsprobe, und zwar mit dem richtigen Muster** — siehe Abschnitt 5. Erwartet: jede K-Nummer genau einmal, jeder Blockbezeichner genau einmal |
| **5** | Die zwei Regeln aus Schritt 2: Fundstelle vorher (erwartet: keine) und nachher |
| **6** | Nichts ausserhalb `docs/` geändert |
| **7** | `git status --porcelain` nach dem letzten Commit |
| **8** | ⭐ **Der ZIP-Umbau aus Schritt 4: wie viele Fundstellen gefunden, wie viele in Gruppe A, B und C** — und **jede Fundstelle der Gruppe C einzeln benannt**, mit dem Satz, warum sie stehen bleibt. ⚠️ *Eine veränderte Gruppe-C-Stelle ist der einzige Fehler dieser Aufgabe, der nicht auffällt* |

---

## 5. ⭐⭐ Die Kollisionsprobe — lies das, bevor du sie schreibst

⚠️⚠️ **Dieselbe Probe ist am 20.09.2026 ZWEIMAL falsch ausgefallen. Beide Male
lag es am Muster, nicht an den Daten.**

| | Muster | Fehler |
|---|---|---|
| **1** | `K2[a-z]` | sah `K3`-Nummern **strukturell nicht** — meldete drei Doppelbelegungen, es waren vier |
| **2** | `^\| \*\*K[0-9][a-z]\*\* \|` | verlangte den **schliessenden Balken** und übersah jede Zeile mit Vergabevermerk `| **K2p** *(…)* |` — meldete 43 Zeilen / 41 Nummern, es sind **64 / 62** |

⭐ **Das Muster, das gilt:**

```
^\| \*\*(K\d[a-z])\*\*
```

**Ohne Abschluss nach dem Bezeichner**, damit Vergabevermerke mitgezählt werden.

⛔ **Und kein `-u` in der Probe.** Eine Kollisionsprobe **zählt**; `sort -u`
entfernt genau die Duplikate, die sie finden soll. *Das war der Fehler in der
Probe von TB-60, die „38 K-Nummern, keine doppelt" meldete.*

⭐ **Halte das Ergebnis gegen eine zweite, unabhängig geschriebene Zählung**
(anderes Werkzeug, anderer Weg), bevor du es als Nachweis abgibst.

### Ein bekanntes Ergebnis, das du bestätigen oder widerlegen sollst

⚠️ **`K1o` und `K1q` stehen in `BACKLOG.md` je ZWEIMAL** (Zeilen 1331/1335 und
1333/1336, Stand `28eea5c`). **In der Sache sind es Fortschreibungen** desselben
Punktes von TB-50 zu TB-51; die zweite Zeile trägt *„(unverändert)"*.

⚠️ **In der Form ist es ein Verstoss gegen Regel 9** — die ältere Zeile steht
daneben statt entfernt.

⇒ **Führe die vier Zeilen zu zwei zusammen**, je eine Zeile pro Nummer, mit dem
Fortschreibungsvermerk **innerhalb** der Zeile. ⚠️ **Das ist eine Entfernung —
dokumentiere sie nach Regel 9**, und dann trägt `numstat` für `BACKLOG.md` genau
diese zwei Zeilen in Spalte zwei.

---

## 6. Die harten Auflagen

| | |
|---|---|
| ⭐ | **Sichern nach jedem fertigen Teil.** Fünf Commits sind oben benannt |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block** |
| ⭐ | **Jede Zahl im Bericht ist gezählt, nicht geschätzt** — und gegen eine zweite Zählung gehalten |
| ⛔ | **Nichts ausserhalb `docs/`** |
| ⚠️ | **Widersprich diesem Auftrag, wo er falsch ist.** Er enthält gemessene Zahlen aus dem Stand `28eea5c`; stimmt eine nicht mehr, gilt deine Messung |

---

## 7. Was diese Aufgabe NICHT tut

| | |
|---|---|
| ✅ | ~~Den ZIP-Widerspruch auflösen~~ — **entschieden am 20.09.2026: ZIP wird überall abgeschafft.** Der Umbau ist **Schritt 4 dieser Aufgabe**, nicht mehr offen |
| ⛔ | **Etwas an `research/` oder am Register ändern** |
| ⛔ | **TB-61 berühren.** Läuft eine TB-61-Sitzung, warte oder melde es |

---

## In einfacher Sprache

**Was wir wissen wollen:** Zwei Notizzettel sind nie in die Aufgabenliste
übertragen worden. Beim einen ist das nur Arbeit — beim anderen ist etwas
verlorengegangen.

**Was schiefgelaufen ist:** Der ältere Zettel wurde übersprungen, und seine
Nummern wurden später an andere Punkte vergeben. Vier seiner sechs Regeln stehen
zum Glück woanders im Projekt. **Zwei stehen nirgends** — darunter ausgerechnet
die Regel, dass deine Rückfragen und Antworten wörtlich in den Bericht gehören,
damit sie nicht nur im Chat leben. Sie ist selbst im Chat geblieben.

**Was du danach hast:** Beide Zettel eingearbeitet, die zwei verlorenen Regeln
an ihrem richtigen Platz, und zwei doppelte Einträge zusammengeführt. Die
Aufgabenliste wächst dabei, aber nur um das, was wirklich fehlt.

**Und noch etwas, das du schon entschieden hast:** Die Arbeitsweise verlangte an
einer Stelle, dir alles als ZIP zu schicken, und sagte an einer anderen, ZIP sei
erledigt. **Du hast entschieden: ZIP fällt ganz weg.** Diese Aufgabe baut das um —
vorsichtig, denn hinter fast jeder ZIP-Zeile steht ein Satz, der weiter gilt:
*ein Ergebnis muss die Sitzung überleben.* Das übernimmt jetzt der Commit, und der
ist sicherer als eine Datei in deinem Download-Ordner.

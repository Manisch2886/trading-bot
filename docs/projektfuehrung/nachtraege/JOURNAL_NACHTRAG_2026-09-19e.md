# Journal-Nachtrag 19.09.2026 (e) — TB-55b und TB-54

**Anzufügen am Ende von `docs/projektfuehrung/JOURNAL.md`, NACH den Blöcken aus
Nachtrag (c) und (d).** Nichts wird umgeschrieben.

> ⚠️ **Zum Blockbuchstaben: messen, nicht raten.**

---

## Block ⟨nächster⟩ — TB-55b: der Snapshot steht im Register

**19.09.2026. `main`, `4c80588` → `0fe61d7`, gepusht. Python 3.9.6.**

`docs/VORREGISTRIERUNG_neuselektion.md` hat einen neuen **Abschnitt 18** —
eine **Tatsachennotiz** zu Registertext 5 / 5a, in der Form von 15.6.
**62 Zeilen hinzugefügt, 0 entfernt.**

⭐⭐ **Keine Zahl im Eintrag ist getippt.** Ein Skript liest `MANIFEST.json`
per `json.load`, holt den Commit aus `git log -- snapshots/`, prüft
`origin/main` per `git branch -r --contains` und misst die höchste
Abschnittsnummer selbst (`assert neu == 18`). Vorher **8/8 Werte maschinell**
gegen die Auftragsliterale verglichen, String- **und** Typgleichheit.

### ⭐⭐ Aus einer Falle wurde Dokumentation

Abschnitt **17.9** führt `snapshot_hash` = **`4fee547d…`** — die TB-47-Messung
über die **223 Kursdateien allein**, vor dem Ziehen. ⚠️ **Das ist die Stelle,
an der später jemand die falsche Zahl abschreibt.**

Abschnitt 18 grenzt sie ausdrücklich ab: *„`63e4b6c8…` läuft über die 225
Dateien; `4fee547d…` lief nur über die 223 Kursdateien und bezeichnet nicht
diesen Snapshot. Beide bleiben richtig; sie beantworten verschiedene Fragen."*

### ⚠️⚠️ Und dort wurde gegen den Wortlaut eines Abbruchkriteriums entschieden

Der Auftrag sagte: *„Gibt es einen Snapshot-Abschnitt **mit einer Zahl darin**:
ABBRUCH."* 17.9 enthält eine. ⭐ **Die Sitzung entschied nach dem Zweck, schrieb
es hin und nannte den Commit zur Nachprüfung.**

| | |
|---|---|
| ⭐ | **Die Entscheidung war richtig** — `4fee547d…` ist kein Duplikat |
| ⚠️⚠️ | **Die Regel war schlecht geschrieben, und das liegt beim Auftraggeber.** *„Eine Zahl darin"* war ein **Stellvertreter** für *„ein Eintrag, der DIESEN Snapshot bezeichnet"* |

⇒ **Zwei Regeln:** *Ein Abbruchkriterium benennt die Sache, nie ihren
Stellvertreter.* · *Fallen Wortlaut und Zweck auseinander und ist der Betreiber
erreichbar — fragen, nicht entscheiden.*

⚠️ **Ein Befund über ein Dokument des Betreuers:** Die Angabe „Python 3.11.15"
in Abschnitt 18 hat **keinen Beleg im Repo**. ⇒ **Jede Behauptung im Register
braucht ihren Beleg im Repo. Ein Beleg in `~/Downloads` ist kein Beleg.**

⭐ **Warum Abschnitt 18 und nicht 17.12** — besser begründet als beauftragt:
Abschnitt 17 ist der TB-48-Nachtrag vom 18.09. und sagt in **17.11**
ausdrücklich *„Kein Snapshot gezogen"*.

---

## Block ⟨übernächster⟩ — TB-54: acht Nachträge, eine Rückfrage

**19.09.2026. `main`, `1124880` → `d9f3c4b` (d–g) → `3121ec2` (h–k), gepusht.**

**`BACKLOG.md` 764 → 929 Zeilen, 167 hinzu / 2 entfernt.** Sieben neue Blöcke
**2j, 2k, 2m, 2n, 2o, 2p, 2q**, sechs ersetzte Kettenzeilen — ⭐ **jede alte
Zeile steht wörtlich darunter**, als ersetzt gekennzeichnet und datiert.

### ⭐⭐ Die Regel aus TB-55b hielt, eine Stunde nach ihrer Formulierung

Nachtrag (h) wollte die Faltenschranke als **`0,87`** eintragen. **`0,87` war
belegt.** ⭐ **Die Sitzung fragte, statt zu entscheiden.** Betreiberentscheidung:
**`0,88` mit Vermerk.** **(d)–(g) waren bereits als Teilerfolg committet** —
der Teilerfolg war der eingebaute Weg, kein Notbehelf.

### ⭐⭐ Ein A1-Fall, den die Sitzung selbst fand

Vier Nachträge ersetzen Kettenzeilen, die **derselbe Arbeitsbaum** erst angelegt
hatte. ⚠️ **Gegen `HEAD` sind solche Ersetzungen unsichtbar** — `numstat` hätte
„0 entfernt" gemeldet. ⭐ **Deshalb zweifach gemessen**: kumulativ gegen `HEAD`
**und** gegen eine Kopie des Standes davor. **171/6 in Schritten, 167/2 gesamt;
die Differenz 4/4 vollständig zugeordnet.**

⭐ **Jede Einfügung lief über einen Anker, der genau einmal vorkommen muss** —
zwei Abbrüche **vor dem Schreiben**, Datei unverändert.

### ⚠️⚠️ Drei Nummernkollisionen, alle aus Nachträgen des Betreuers

`0,87` doppelt · **`V1` jetzt zweimal** (Abschnitt 2 und Block 2o) ·
**„TB-54" bezeichnet zwei Vorhaben** (Lese-Audit und Backlog-Nachträge).

⇒ ⭐ **Ein Nachtrag nennt keine konkrete Nummer, die er nicht selbst gemessen
hat.** Er sagt *„die nächste freie Nummer, gemessen"*; die Nummer vergibt die
ausführende Sitzung.

### ⚠️⚠️ Und ein Befund über die Arbeitsweise selbst

**Die Kette ist numerisch unsortiert** — `0,87` vor `0,86`, ersetzte Zeilen
zwischen aktiven. ⭐ **Die Sitzung hat bewusst nicht umsortiert**, weil das
entfernte Zeilen erzeugt hätte.

> ⭐⭐ **Der Kern: Wir wenden Register-Disziplin auf ein Arbeitsdokument an.**
> „Nur hinzufügen" ist richtig für `VORREGISTRIERUNG_neuselektion.md` — dort
> schützt es die Nachvollziehbarkeit des Laufs. ⚠️ **`BACKLOG.md` ist kein
> Registertext; dort schützt dieselbe Regel nichts und kostet Lesbarkeit.**

**Betreiberentscheidung erforderlich.**

⭐ **Ohne Auftrag getan, und richtig:** Sieben Nachtragsdateien wanderten nach
`docs/projektfuehrung/nachtraege/`, byteidentisch per `cmp` — *„Ein Beleg in
`~/Downloads` ist kein Beleg."*

---

### Der Stand am Ende des 19.09.

| | |
|---|---|
| Snapshot | ⭐ gezogen (`1075dec`), **registriert** (Abschnitt 18), `--pruefen` `UNVERAENDERT` |
| Backlog | ⭐ **(d)–(k) eingearbeitet**, 929 Zeilen |
| Datenstand | `d9449faf…`/223 — an diesem Tag **neunmal** gemessen, neunmal gleich |
| 12 Datenbanken | in allen drei Sitzungen **12/12** byteweise identisch |
| Registerprüfer | in jeder Sitzung vorher und nachher **KEIN BEFUND**, `Quelle beleg: trockenlauf` |
| Offen | Journal · A7 · die drei Kollisionen · die Kettensortierung · F1b/Q2 · TB-53 · die Faltenschranke |

---

### In einfacher Sprache

**Das Regelwerk weiss jetzt, worauf gerechnet wird**, und die Vorhabenliste ist
auf dem Stand von heute. Nichts ist verloren gegangen: Wo eine Zeile ersetzt
wurde, steht die alte darunter, mit Datum.

⭐ **Zweimal an diesem Tag hat eine Sitzung gefragt, statt zu entscheiden** —
einmal beim Ziehen, einmal bei einer doppelt vergebenen Nummer. **Beide Male
war die Frage die richtige Antwort.**

⚠️ **Und dreimal haben sich Nummern überschnitten, alle drei durch den
Betreuer**, der Nummern vergab, ohne den Zielstand zu kennen. Ab jetzt sagt er
nur noch „die nächste freie" und begründet, wohin etwas gehört.

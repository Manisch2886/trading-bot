# Backlog-Nachtrag 18.09.2026 (d) — TB-51

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
⚠️ **Setzt (a), (b) und (c) voraus** — alle drei sind eingearbeitet
(`02de1f7`, `29216cd`).

> ⚠️ **Nichts wird entfernt** ausser der einen benannten Ersetzung.

---

## Berichtigung — die Kettenzeile 0,84 trägt die Betreiberentscheidung nicht

⚠️ **Der Befund:** Die Entscheidung vom 18.09.2026 — *der Snapshot wird erst am
Tag des signierten Tags gezogen* — steht in `docs/START_HIER.md` und in den
Aufträgen, **nicht in `BACKLOG.md`.** ⚠️ *Und nach Abschnitt 5 ist `BACKLOG.md`
die kanonische Quelle: „Bei Widerspruch zu Notizen gilt die Datei."*

**Zu finden** (Abschnitt 3 „Die Kette", die Zeile mit `0,84`):

```
| **0,84** | **Snapshot ziehen** | ⭐ **nach dem Merge nicht mehr blockiert.** ⚠️ **Eigene Entscheidung mit eigener Freigabe** — TB-49 hat ihn ausdrücklich nicht gezogen |
```

**Zu ersetzen durch:**

```
| **0,84** | **Snapshot ziehen** | ⭐ **Technisch möglich seit TB-49** (`2f241d1`), auf beiden Rechnern nachgewiesen. ⚠️⚠️ **BETREIBERENTSCHEIDUNG 18.09.2026: er wird NICHT jetzt gezogen, sondern am Tag des signierten Tags** — Registertext 5 / **F1a**: *„Snapshot am Tag des signierten Tags ziehen; ein zweiter Snapshot ist ein neuer Lauf."* **Ein früherer Snapshot wäre entweder veraltet, wenn der Tag kommt, oder der Tag friert einen Zustand ein, den das Register nicht beschreibt** |
```

---

## Neuer Block 2j — aus TB-51

**Einzufügen NACH Block 2i.**

---

### 2j — Aus TB-51, Startdatei und Flackerstufe (Stand 18.09.2026)

**TB-51 ist erledigt — Mac-Sitzung, gepusht `58c0ab9..29216cd`.**
Datenstand `d9449faf…`/223 vorher = nachher, neun Datenbanken byteweise
identisch, `pruefe_register.py` rc 0 vorher wie nachher, kein Snapshot,
`git status` nach dem letzten Commit leer.

| # | Punkt |
|---|---|
| **T51.1** | ⭐ **`docs/START_HIER.md` existiert** — 95 Zeilen, `numstat` **95/0**. Sie trägt: was das Projekt ist · die Lesereihenfolge der fünf Führungsdokumente · die Kette mit Stand · die Sperrliste und die vier verankerten Zahlen · was beim Betreiber offen ist. **`ARBEITSWEISE.md` §10 führt sie im Übergabepaket — jetzt zu Recht** |
| **T51.2** | ⭐⭐ **`basislauf.py` hat eine fünfte Stufe: `FLACKERND`.** Ein Eintrag darin ist **weder rot noch grün UNERWARTET**; die Zeile nennt **Rate, Datum, Herkunft und das Ergebnis dieses Laufs**, und die Stufe **zählt eigens**, nicht unter grün oder rot. Im echten Einzellauf: `[~~~~] system/test_log_rotation.py 6.4s flackernd (Mac ~30 %, …): heute gruen`, `SUMME 1 von 1`, `UNERWARTET 0`. **Damit ist T50.4 erledigt** |
| **T51.3** | ⭐⭐ **DER NACHWEIS IST STÄRKER ALS GEFORDERT: Gegenprobe gegen die echte Vorgängerfassung** (`git show 58c0ab9`), nicht nur gegen gebaute Mutanten. **Dort scheitern die Proben** — und Probe 3.3 zeigt genau den alten Befund: *„dort ist der rote Lauf UNERWARTET — der alte Befund (T50.4)"*. Dazu drei Mutationen (`M1_ohne_stufe`, `M2_zu_weit`, `M3_summe_ohne_flackernd`) und vier Prüfungen, dass der Eintrag **in keiner anderen Liste** steht. **24/24, rc 0.** ⭐ *Ein künstlicher Mutant zeigt, dass eine Prüfung theoretisch beisst; der echte Vorgänger zeigt, dass sie das Problem gefunden hätte, das es wirklich gab* |
| **T51.4** | **Nachtrag (c) eingearbeitet:** Kettenzeile 0,82 (Widerspruch „gemergt" neben „Merge offen") berichtigt, Kopf von Block 2h berichtigt, Block 2i eingefügt, **`ARBEITSWEISE.md` §5b „Der feste Ablauf" auf die Mac-Sitzung umgestellt** — einschliesslich des Hinweises, dass Fassung v2.1.276 den Auftragstext nicht aus dem `--remote-control`-Einzeiler mitnimmt. **Acht entfernte Zeilen insgesamt, alle acht zugeordnet** |
| **T51.5** | ⚠️ **`STRATEGIEN_uebersicht.md` existiert weiterhin nirgends im Repo** (`find` und `git ls-files` leer), und `ARBEITSWEISE.md` §10 führt sie weiter im Übergabepaket. **Dieselbe Betreiberentscheidung wie bei T50.3.** ⭐ **Empfehlung: aus §10 streichen und stattdessen auf die Backlog-Abschnitte verweisen** (K2, K3, Abschnitt 8 führen die Zellen, die Kandidaten und die verworfenen Strategien bereits) — *eine eigene Übersichtsdatei veraltet, sobald sie nicht bei jeder Übergabe mitgeschrieben wird* |
| **T51.6** | **Drei gealterte Angaben im Docstring von `basislauf.py`, berichtet statt geändert** (nicht freigegeben): *„drei Dinge auseinanderhalten"* — es sind jetzt **fünf** · die **1 312** und die **62**. ⭐ **Die Sitzung hat die heutige Zahl selbst nachgemessen statt sie aus T50.6 zu übernehmen: 66 Testdateien** (65 plus die neue `test_flackerstufe.py`) |
| **T51.7** | ⚠️ **Meine dritte Fehlschätzung dieser Art an einem Tag:** Für `ARBEITSWEISE.md` hatte ich **vier** entfernte Zeilen angekündigt, es waren **fünf** — mein eigener Suchtext umfasste fünf. **Immer in dieselbe Richtung: ich zähle die Blöcke, die ich umschreibe, nicht die Zeilen, die git als geändert sieht.** *Die Angabe bleibt trotzdem sinnvoll — sie ist widerlegbar, und genau deshalb fällt die Abweichung auf* |

---

## Ergänzungen zu Abschnitt 4 („Laufend, klein")

| # | Punkt |
|---|---|
| ~~K1n~~ | ~~`basislauf.py` braucht eine vierte Stufe~~ **ERLEDIGT durch TB-51 (T51.2)** |
| **K1o** | *(unverändert)* gealterte Zahlen im Docstring von `basislauf.py` — jetzt **drei** Angaben, siehe **T51.6** |
| **K1q** | *(unverändert)* `STRATEGIEN_uebersicht.md` — Entscheidung offen, siehe **T51.5** |

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — **genau eine entfernte
   Zeile** (die Kettenzeile 0,84), zugeordnet.
2. `git branch --show-current && git status --short` **vor** dem Commit.
3. `git add` + `commit` + `push` **in einem Zug**, `git status` **danach**.

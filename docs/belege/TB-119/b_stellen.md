# TB-119 Schritt B — Stellen im Regelwerk (27b Teil E)

*Erzeugt von `docs/belege/TB-119/b_einsetzen.py --nur-protokoll HEAD`. Je Stelle: die ganze Zeile davor und danach (erste nicht-leere Zeile vor der ersten bzw. nach der letzten beruehrten Zeile, am Stand vor der Stelle) und jede entfernte Zeile woertlich. „entfernt: keine“ heisst: reine Einfuegung.*

## docs/projektfuehrung/ARBEITSWEISE.md — 7b: docs.tar.gz

- **berührt ab Z. 1103** (Stand vor der Stelle) · **davor:** `| **Dashboard über Tailscale** | ˋDASHBOARD_HOSTˋ steht **nur** in der ˋ.envˋ — geht sie verloren, ist der einzige Fernzugriffsweg weg (**F6/O2**) |`
- **danach**: `⚠️ **Zusammengetragen am 18.09.2026 — bisher stand jeder dieser Punkte einzeln`
- **hinzugefügt:** 16 Zeilen
- **entfernt:** keine

## docs/projektfuehrung/ARBEITSWEISE.md — 8: Füllstandszeile der Wochenrückmeldung

- **berührt ab Z. 1148** (Stand vor der Stelle) · **davor:** `  Erinnerungen-App des Nutzers. Hinein gehören **gemessene Ergebnisse** und`
- **danach**: `---`
- **hinzugefügt:** 4 Zeilen
- **entfernt:** keine

## docs/projektfuehrung/ARBEITSWEISE.md — 15: Indexpflicht FABLE_DIALOG_INDEX.md

- **berührt ab Z. 1586** (Stand vor der Stelle) · **davor:** `sieht neun Entscheidungen ohne die Fragen, die sie ausgelöst haben — und kann`
- **danach**: `**Anweisung des Betreibers, 21.09.2026.** Der Regelfall ist: **nichts`
- **hinzugefügt:** 12 Zeilen
- **entfernt:** keine

## docs/projektfuehrung/ARBEITSWEISE.md — 23 (neu): Projektablage

- **berührt ab Z. 2085** (Stand vor der Stelle) · **davor:** `eine Sitzung, die niemand findet. Deshalb zuerst das Fenster, dann der Satz —`
- **danach**: `(Dateiende)`
- **hinzugefügt:** 93 Zeilen
- **entfernt:** keine

## docs/projektfuehrung/UMZUG.md — 1: UEBERGABE.md ohne Datum

- **berührt ab Z. 27** (Stand vor der Stelle) · **davor:** `> unerwarteter Abbruch Arbeit vernichtet. Wer sie laufend pflegt, hat keins.**`
- **danach**: `⭐ **Folge, und sie ist der ganze Gewinn:** Eine überraschende Komprimierung des`
- **hinzugefügt:** 4 Zeilen
- **entfernt:** 2 Zeilen, woertlich:

```
⇒ **`UEBERGABE_<datum>.md` wird an jedem sauberen Stand fortgeschrieben** — nicht
am Ende.
```

## docs/projektfuehrung/UMZUG.md — 2: Träger

- **berührt ab Z. 46** (Stand vor der Stelle) · **davor:** `| ⭐ **Erinnerung** (ˋ/projects/<id>/preferences.mdˋ) | **Wie der Betreiber arbeiten will.** Wird beim Sitzungsstart von selbst gelesen, ohne dass er etwas tun muss | Fachstand, Zahlen, Befunde. **Keine Belege** — die Erinnerung ist keine Beweisführung |`
- **danach**: `⚠️⚠️ **Die Regel, die daraus folgt, und sie ist die wichtigste dieses`
- **hinzugefügt:** 9 Zeilen
- **entfernt:** 2 Zeilen, woertlich:

```
| ⭐ **Projektdokumente** (claude.ai-Projekt „Trading Bots") | **Den Stand und die Führungsdokumente.** Sichtbar in **jedem** Chat des Projekts **und für Fable** | Nichts, was git prüfen muss — kein `numstat`, keine Versionsgeschichte |
| ⭐ **Das Repo** (`Manisch2886/trading-bot`) | **Die Belege.** Versioniert, mit Commit, prüfbar | Es wird von einem neuen Chat **nicht automatisch gelesen** — es braucht einen Verweis |
```

## docs/projektfuehrung/UMZUG.md — Schritt 3: UEBERGABE.md ohne Datum

- **berührt ab Z. 165** (Stand vor der Stelle) · **davor:** `### Schritt 3 — Die Übergabe fortschreiben`
- **danach**: `Blöcke:**`
- **hinzugefügt:** 3 Zeilen
- **entfernt:** 1 Zeilen, woertlich:

```
`docs/projektfuehrung/UEBERGABE_<datum>.md`, **und sie enthält immer diese neun
```

## docs/projektfuehrung/UMZUG.md — Schritt 4: Soll/Ist-Abgleich und Füllstand

- **berührt ab Z. 182** (Stand vor der Stelle) · **davor:** `| **9** | ⭐ **Verweis auf den Eröffnungstext in Abschnitt 6** — dort steht die einzige Fassung | ⚠️ **kein zweiter Text in der Übergabe.** *Bis TB-68 (20.09.2026) verlangte diese Zeile eine Kopie; die beiden Fassungen widersprachen sich vom ersten Commit an* |`
- **danach**: `### Schritt 5 — Die Erinnerung nachziehen`
- **hinzugefügt:** 18 Zeilen
- **entfernt:** 6 Zeilen, woertlich:

```
### Schritt 4 — In die Projektablage schreiben
**Die Übergabe und dieses Dokument gehen zusätzlich in das claude.ai-Projekt**
(`projektfuehrung/UEBERGABE_<datum>.md`, `projektfuehrung/UMZUG.md`).
⭐ **Warum zusätzlich und nicht stattdessen:** Das Projekt ist der Träger, den ein
neuer Chat **von selbst** sieht. Das Repo ist der Träger, der **Beweiskraft**
hat. Beides ist nötig, und sie müssen gleich lauten.
```

## docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md — 6: Träger neu bestimmt

- **berührt ab Z. 133** (Stand vor der Stelle) · **davor:** `am häufigsten gebrochen wird:**`
- **danach**: `⚠️⚠️ **ˋlogs/auftraege/ˋ ist kein Träger** — über ˋ.gitignore:27ˋ (ˋlogs/ˋ)`
- **hinzugefügt:** 9 Zeilen
- **entfernt:** 3 Zeilen, woertlich:

```
| **Repo** | die Belege, versioniert |
| **Projektablage** | der Stand, sichtbar für jeden Chat und für Fable |
| **Erinnerung** | wie gearbeitet wird |
```

## docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md — 9: gilt auch für die Ablage

- **berührt ab Z. 186** (Stand vor der Stelle) · **davor:** `dürfen natürlich gerne gelöscht werden."*`
- **danach**: `| ⭐ darf gelöscht werden | ⚠️ darf NICHT gelöscht werden |`
- **hinzugefügt:** 5 Zeilen
- **entfernt:** keine

## docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md — 9: Ausnahme Backlog Abschnitt 8 -> BACKLOG_ERLEDIGT_2026-09.md

- **berührt ab Z. 198** (Stand vor der Stelle) · **davor:** `| Rückblicke auf erledigte Aufgaben, **deren Lehre bereits als Regel geführt wird** | **ˋJOURNAL.mdˋ** — ergänzen, nie umschreiben |`
- **danach**: `| Zwischenlager-Dateien mit erfüllter Bringschuld | **ˋPRUEFPRINZIPIEN.mdˋ** |`
- **hinzugefügt:** 1 Zeilen
- **entfernt:** 1 Zeilen, woertlich:

```
| Überholte Fassungen einer Regel, sobald die neue steht | **Backlog-Abschnitt 8** (Gestrichen) |
```


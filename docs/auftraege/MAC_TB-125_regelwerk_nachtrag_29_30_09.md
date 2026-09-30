# TB-125 Regelwerk-Nachtrag 29./30.09.2026 — ARBEITSWEISE, UMZUG, BACKLOG: Text wörtlich an benannten Ankern (Sonnet-Probe nach 22.12)

**Sitzungstitel:** `TB-125` · **Modell:** Sonnet 5.5, Aufwand hoch — **Probe** nach dem Betreiberentscheid 29.09.2026, ca. 14:05 („Nur Mechanik, erst Probe (Empfohlen)“): reiner Dokumentationsauftrag mit wörtlich vorgegebenem Text. Der Wächter startet ohne Modellwahl (Lücke, Nachtrag 29.09., 14:10; dort vorgesehen: `claude --help` prüfen und den Wächter je Auftrag steuerbar machen, Handwerk mit Freigabe). **Vorgabe des steuernden Chats (30.09.2026), bis dahin:** Der Betreiber setzt das Modell in der Sitzung selbst (`/model sonnet`), bevor er den Einfügesatz schickt. Schritt 0 hält fest, welches Modell tatsächlich läuft; läuft Opus, wird der Auftrag trotzdem abgearbeitet, zählt aber nicht als Probe. · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 30.09.2026, ca. 22:00, vom steuernden Chat
**Vorgänger:** TB-124. **Dieser Auftrag:** `docs/auftraege/MAC_TB-125_regelwerk_nachtrag_29_30_09.md`, er wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3`. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei** (Betreiberentscheid 26.09.2026). Nur drei Dateien werden geändert: `docs/projektfuehrung/ARBEITSWEISE.md`, `docs/projektfuehrung/UMZUG.md` und `docs/projektfuehrung/BACKLOG.md`. Die Regeln selbst hat der Betreiber am 29./30.09. per Auswahlkarte bzw. mit „zukünftig“ entschieden; die Fundstelle steht je Einfügung. Dieser Auftrag trägt sie nur ein (ARBEITSWEISE 15, 5b).

⛔ **Nicht erlaubt, mit Grund:**
- **Umformulieren, Kürzen, „Glätten“ oder Zusammenlegen** des vorgegebenen Texts. *Grund:* Die Probe misst genau, ob der Text zeichengleich ankommt (22.12).
- Jede Datei ausser den drei genannten und den Belegen, dem Ergebnis und dem Journal. *Grund:* Das ist ein Dokumentationsauftrag (5b).
- Register, `docs/VORREGISTRIERUNG_*`, Code, `research/`, `strategies/`. *Grund:* E-2 ist ein eigener Auftrag (TB-126) mit Einzelfreigabe.
- `UEBERGABE.md` und `UEBERGABE_ARCHIV.md` ändern. *Grund:* Das sind die Quellen; sie bleiben, wie sie sind.

**Sichtschutz:** entfällt, es werden keine Ergebnisse gelesen. `BACKLOG.md` wird nur an der benannten Stelle geändert.

In einfacher Sprache: Am 29. und 30.09. hat der Betreiber rund vierzig Arbeitsregeln neu beschlossen. Bisher stehen sie nur in der Übergabe und in der Erinnerung. Diese Sitzung trägt sie wörtlich an festen Stellen in die Arbeitsweise, die Umzugsanleitung und das Backlog ein. Sie formuliert nichts um. Nebenbei prüft der Lauf, ob Sonnet so eine Abschreibarbeit sauber schafft.

## Verfahren je Einfügung (gilt für E1 bis E24)

*Vorgezählt vom steuernden Chat am 30.09.2026, ca. 21:55, über die Geräteanbindung (Python `str.count` am Arbeitsbaum): jeder Anker E1–E22 und E24 genau 1 (E5: beide Anker je 1, dazwischen einschliesslich 32 Zeilen); `| **K4s** |` und `| **K4t** |` kommen in `BACKLOG.md` noch nicht vor. Die Sitzung zählt selbst nach — ihre Zahl gilt.*

1. **Vorher:** Den Anker in der genannten Datei zählen (`grep -cF -- '<Anker>'`, bzw. Python `str.count` bei Sonderzeichen). **Soll: genau 1.**
   - Weicht die Zahl ab: diese Einfügung **nicht** ausführen, in der Tabelle vermerken, weitermachen. Das ist kein Abbruch.
2. **Ausführen**, wie unter „Art“ angegeben:
   - „nach der Zeile“ heisst: nach der ganzen Zeile, die den Anker enthält.
   - „vor der Zeile“ entsprechend davor.
   - „ersetzt die Zeile“ heisst: die ganze Zeile, die den Anker enthält, wird durch den Text ersetzt.
   - Der Text ist der Inhalt des Codeblocks unter der Einfügung, ohne die Zäune. Bei E21 sind die Zäune `~~~` statt ```.
   - Leerzeilen: Der Text wird genau so eingefügt, wie er im Block steht, einschliesslich einer Leerzeile an seinem Ende (E18, E21).
   - Tabellenzeilen (E1, E7–E17, E22–E24) werden ohne Leerzeilen eingefügt.
   - Absätze (E2, E3, E6, E19, E20) bekommen davor und danach genau eine Leerzeile. Eine schon vorhandene Leerzeile wird nicht verdoppelt.
3. **Nachher:** Die **erste Zeile** des eingefügten Texts zählen. **Soll: genau 1.**
4. **Werkzeug:** Die Einfügungen per Skript ausführen (`docs/belege/TB-125/einfuegen.py`). Das Skript liest die Texte aus **diesem Auftrag** (Codeblock unter der Überschrift der Einfügung) und nicht aus dem Gedächtnis des Modells. Das ist der Kern der Probe.

Ergebnis je Einfügung in `docs/belege/TB-125/einfuegungen.txt`: `E<n> · Datei · Anker vorher (Zahl) · ausgeführt ja/nein · Text nachher (Zahl)`.

## Schritt 0 — Sicherung und Ausgang

0a. `git status --short` — genau die Einträge, die der steuernde Chat beim Ablegen hier einträgt:
*Eingetragen vom steuernden Chat am 30.09.2026, ca. 22:45 (gemessen über die Geräteanbindung mit `git --no-optional-locks diff --name-only HEAD` und `ls-files --others --exclude-standard`): drei geänderte Dateien, nichts Neues. `UEBERGABE.md` trägt den Umzugsblock 22:15 und den Nachtrag 22:40; `AKTUELLER_AUFTRAG.md` zeigt auf TB-125.*

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/auftraege/MAC_TB-125_regelwerk_nachtrag_29_30_09.md
 M docs/projektfuehrung/UEBERGABE.md
```

Weicht etwas ab ⇒ Abbruch. Commit `TB-125 Schritt 0`, pushen.

0b. Modell der Sitzung festhalten (Kopfzeile bzw. Selbstauskunft) ⇒ `docs/belege/TB-125/0b_modell.txt`.

0c. sha256 und Zeilenzahl der drei Dateien ⇒ `docs/belege/TB-125/0c_ausgang.txt`.

Keine db-Sicherung, kein Datenstand, kein Basislauf: Es wird kein Code berührt (7c gilt für Testaufträge).

## Schritt A — Die Einfügungen

### Datei `docs/projektfuehrung/UMZUG.md`

#### E1 — UMZUG 3, Auslöser 6 (Betreiber 29.09.2026, 07:55)

Anker: `| **5** | **Der Betreiber fragt danach** | dann gilt Abschnitt 4 |` · Art: **nach der Zeile**

```
| **6** | ⭐ **Der mitgezählte Verlauf erreicht etwa 200 000–250 000 Tokens** — das Zwei- bis Dreifache der Einlesekosten (Betreiber 29.09.2026) | am nächsten sauberen Stand oder vor dem nächsten grossen Block; Vorschlag mit Uhrzeit. Gezählt wird, was im Chat gelesen und geschrieben wurde (Bytes der Werkzeugausgaben ÷ ~3,3). ⚠️ **Schätzung, kein Messwert** — der Kontextfüllstand ist nicht ablesbar; die Zahl steht bei jedem Hinweis dabei |
```

#### E2 — UMZUG 3, Umzugsampel (Betreiber 29.09.2026, 09:20)

Anker: `⭐ **Der Hinweis wird ausgesprochen, nicht abgewartet**` · Art: **vor der Zeile** (als eigener Absatz)

```
⭐ **Umzugsampel** (Betreiber 29.09.2026, Form wie Fable 29a Abschnitt 2): letzte Zeile jeder Antwort des steuernden Chats —
`Umzugsampel: <Farbe> · <geschätzte Tokens im Verlauf> · <Empfehlung>`
🟢 unter 200 000 — bleiben · 🟡 200 000–300 000 — Umzug am nächsten sauberen Stand oder vor dem nächsten grossen Block, mit Uhrzeit · 🔴 über 300 000, nach einer Komprimierung, oder wenn der Chat merkt, dass er Gelesenes verliert — Umzug vor dem nächsten Auftrag. Schätzung (Bytes ÷ ~3,3), kein Messwert.
```

#### E3 — UMZUG 4, Schritt 3: der jüngste Block ist selbsttragend (Betreiber 29.09.2026, 07:55)

Anker: `| | Block | ⚠️ |` · Art: **vor der Zeile** (als eigener Absatz)

```
⭐ **Der jüngste Block der Übergabe ist selbsttragend** (Betreiber 29.09.2026): Er enthält alle neun Blöcke und wird beim Umzug als einziger Teil der Übergabe gelesen. Ältere Blöcke werden nur verwiesen, nicht vorausgesetzt. Seit 30.09.2026 (T5) stehen sie in `docs/projektfuehrung/UEBERGABE_ARCHIV.md`, nur im Repo; in der Projektablage liegt nur `UEBERGABE.md`.
```

#### E4 — UMZUG 4, Schritt 6: Eröffnungstext als erste Nachricht (Betreiber 29.09.2026, 14:10, „zukünftig“)

Anker: `⚠️ **Als Kopierblock in der Antwort** — kein Download, keine Datei, kein Anhang.` · Art: **ersetzt die Zeile**

```
⚠️ **Als Kopierblock, als ERSTE Nachricht im laufenden Chat** — eine eigene Nachricht vor allen Erläuterungen (Betreiber 29.09.2026, 14:10: *„Schicke mir zukünftig immer den Text der Übergabe für den neuen Chat als erste Nachricht direkt im laufenden Chat zum kopieren“*); kein Download, keine Datei, kein Anhang.
```

#### E5 — UMZUG 6, der Eröffnungstext (Fassung 30.09.2026; ersetzt die Fassung von TB-68)

Anker (Anfang): `Neue Sitzung zum Trading-Bot-Projekt. Das Projekt "Trading Bots" ist angehängt,` · Anker (Ende): `und was gerade auf wen wartet. Dann fangen wir an.` · Art: **ersetzt alle Zeilen vom Anfangsanker bis einschliesslich Endanker** (beide innerhalb des Codeblocks in Abschnitt 6; die Zäune des Codeblocks bleiben stehen). Beide Anker vorher je genau 1.

Quellen: Eröffnungstext 30.09.2026 (UEBERGABE, Umzugsblock 30.09., Block 9); Kernlektüre mit Abschnittsfilter (29.09., 14:52 und 20:48, Block 7 Nr. 1); erste Brückenmessung nur mit `--no-optional-locks` (30.09., Nachtrag 19:50, Fehler Nr. 6); Prüfung des Ablage-Zugriffs (30.09., Nachtrag 19:50: diesem Chat fehlte der Ablage-Zugriff); erster Handwerksschritt in derselben Antwort (29.09., 20:48, Block 7 Nr. 3). Der Platzhalter `<Überschrift des ersten Blocks der Kernlektüre>` wird beim Umzug vom steuernden Chat mit der Überschrift gefüllt, ab der der neue Chat lesen soll (etwa ein Nachtrag vor dem Umzugsblock).

```
Neue Sitzung zum Trading-Bot-Projekt (steuernder Chat). Das Projekt "Trading Bots" ist angehängt.

Prüfe als Erstes, ob du über die Geräteanbindung auf ~/trading-bot lesen kannst — nenne mir HEAD und die Zeilenzahl von docs/projektfuehrung/BACKLOG.md als Beleg. Wenn das nicht geht, sag es ausdrücklich, denn dann müssen wir Messungen wieder über mich laufen lassen. Schon für diese erste Messung gilt: git über die Brücke nur mit --no-optional-locks (rev-parse, log, show, ls-files, diff --name-only, worktree list), nie git status. Prüfe ausserdem, ob du die Projektablage lesen kannst (project_info); wenn nicht, sag es — dann kommen Fable-Antworten als Anhang.

Lies dann nur die Kernlektüre, aus dem Repo über die Geräteanbindung mit Abschnittsfilter (project_read liefert immer die ganze Datei):
1. docs/projektfuehrung/UEBERGABE.md — ab der Überschrift „<Überschrift des ersten Blocks der Kernlektüre>“ bis Dateiende. Ältere Blöcke nur bei Bedarf (auch in UEBERGABE_ARCHIV.md).
2. docs/projektfuehrung/ARBEITSWEISE.md — nur Abschnitt 0 (von „## 0.“ bis vor „## 1.“).
3. docs/projektfuehrung/UMZUG.md — nur Abschnitt 3 (von „## 3.“ bis vor „## 4.“).
Nur wenn die Geräteanbindung fehlt: dieselben Stellen über den Projects-Zugriff (projektfuehrung/…).

PRUEFPRINZIPIEN.md (docs/PRUEFPRINZIPIEN.md — NICHT unter projektfuehrung/) und BACKLOG.md gezielt nachlesen, wenn der Anlass kommt. Grosse Dateien über einen Helfer lesen, der nur eine Kurzfassung zurückgibt. docs/UEBERGABEPROTOKOLL.md nur für den Betrieb (Cronjobs, Neustarts, Schlüsselbund).

Sag mir in wenigen Sätzen, was du verstanden hast — Stand, nächster Schritt, und was gerade auf wen wartet. Fang danach in derselben Antwort mit dem ersten Handwerksschritt an.
```

#### E6 — UMZUG 6, Vermerk zur neuen Fassung

Anker: `> ⭐ **Der letzte Satz ist Absicht.**` · Art: **vor der Zeile** (als eigener Absatz)

```
⭐ **Fassung vom 30.09.2026 (TB-125)** — ersetzt die Fassung von TB-68. Geändert: nur die Kernlektüre statt fünf ganzer Dokumente (Betreiber 29.09.2026, 07:55: „Ja, Kernlektüre ~40 KB (Empfohlen)“), gelesen mit Abschnittsfilter aus dem Repo (29.09.2026: `project_read` liefert immer die ganze Datei, ~190 KB statt ~40 KB); die erste Brückenmessung nur mit `--no-optional-locks` (30.09.2026: ein `git status` hinterliess eine `index.lock`, die die Brücke nicht löschen konnte); Prüfung des Ablage-Zugriffs (30.09.2026: einem Chat fehlte `project_read`); der erste Handwerksschritt folgt in derselben Antwort (29.09.2026). Der Platzhalter für die Überschrift wird beim Umzug gefüllt. Der Vermerk unten („Der letzte Satz ist Absicht“) meint jetzt den Satz „Sag mir in wenigen Sätzen …“.
```

### Datei `docs/projektfuehrung/ARBEITSWEISE.md`

#### E7 — Abschnitt 0, „Immer“: kurze Antworten und keine Behauptung über das Handeln des Betreibers

Anker: `in derselben Antwort in alle Träger eingetragen, ohne Rückfrage` · Art: **nach der Zeile**

```
| ☐ | Kurz: „In einfacher Sprache“ im Chat ein bis zwei Zeilen, ausführlich nur in Dokumenten (T6, Betreiber 30.09.2026) | 4 |
| ☐ | Was der Betreiber abgeschickt hat, wird nicht behauptet — „als Kopierblock ausgegeben“; ob gesendet, zeigt erst die Antwort. Vor einer Karte, die einen versendeten Stand ändern will, zuerst fragen, ob schon gesendet (29.09.2026) | 9 |
```

#### E8 — Abschnitt 0, „Am Anfang einer Aufgabe“: nach der Übernahme gleich weiter

Anker: `Ein bis zwei Sätze in einfacher Sprache, was jetzt passiert` · Art: **nach der Zeile**

```
| ☐ | Nach der Übernahme in einem neuen Chat: in derselben Antwort mit dem ersten Handwerksschritt beginnen, nicht auf ein Startzeichen warten (29.09.2026) | 13; UMZUG 6 |
```

#### E9 — Abschnitt 0, „Am Ende jeder Antwort“: Umzugsampel und Karte zuletzt

Anker: `Die Aufgabenliste so kurz wie möglich` · Art: **nach der Zeile**

```
| ☐ | Letzte Zeile: Umzugsampel (Farbe · Tokens · Empfehlung) | UMZUG 3 |
| ☐ | Eine Auswahlkarte kommt erst danach, als letzter Schritt: Ergebnis, Dateien, Kopierblöcke, „Deine Aufgaben“ und Umzugsampel sind vorher zugestellt (M1, Betreiber 30.09.2026) | 6d |
```

#### E10 — Abschnitt 0, „Wenn ein Arbeitsabschnitt endet …“: Umzug nach Tokenverbrauch (Betreiber 29.09.2026, 07:55)

Anker: `Ein nötiger Umzug wird frühzeitig angekündigt` · Art: **ersetzt die Zeile**

```
| ☐ | Ein nötiger Umzug wird frühzeitig angekündigt — auch nach Tokenverbrauch: Verlauf mitzählen, ab ~200–250k am nächsten sauberen Stand vorschlagen, mit Zahl und Uhrzeit | 10; UMZUG 3 |
| ☐ | Beim Umzug: der Eröffnungstext als ERSTE Nachricht im laufenden Chat, als eigener Kopierblock vor allen Erläuterungen (Betreiber 29.09.2026, „zukünftig“) | UMZUG 6 |
```

#### E11 — Abschnitt 0, „Wenn eine Entscheidung beim Betreiber liegt“: M1–M3 (Betreiber 30.09.2026, 19:13)

Anker: `Als anklickbare Multiple-Choice-Frage — nicht als Absatz, nicht als Tabelle, nicht gesammelt ans Ende der Antwort` · Art: **ersetzt die Zeile**

```
| ☐ | Karte nur für echte Betreiberentscheide: Freigaben (Register, Sperrliste, Signalpfad, Parameterdateien), Löschen und Ablage entfernen, Umzug, Geld, Unumkehrbares. Handwerk entscheidet der steuernde Chat selbst: „Vorgabe: X — gilt, wenn du nicht widersprichst“ (M3, 30.09.2026) | 6d |
| ☐ | Als anklickbare Karte, nicht als Absatz und nicht als Tabelle; höchstens **eine** Karte je Antwort, bis zu vier Fragen gebündelt, als letzter Schritt der Antwort (M1, M2, 30.09.2026) | 6d, Form |
```

#### E12 — Abschnitt 0, dieselbe Tabelle: „auch bei zwei Wegen“ im Rahmen von M3

Anker: `Auch bei zwei Wegen, auch wenn sie klein wirkt` · Art: **ersetzt die Zeile**

```
| ☐ | Auch bei zwei Wegen, auch wenn sie klein wirkt — sofern es ein Betreiberentscheid nach M3 ist | 6d, Form |
```

#### E13 — Abschnitt 0, „Wenn Terminalbefehle drin sind“: Brücke nur lesend und ohne Sperrdatei

Anker: `über die Geräteanbindung; die zwei lesenden Befehle` · Art: **ersetzt die Zeile**

```
| ☐ | Kein `git status` über die Geräteanbindung — auch nicht bei der allerersten Messung eines neuen Chats. git über die Brücke nur mit `--no-optional-locks` (`rev-parse`, `log`, `show`, `ls-files`, `diff --name-only`, `worktree list`), dazu md5 (30.09.2026: ein `git status` hinterliess eine `.git/index.lock`, die die Brücke nicht löschen konnte) | 14, Regel 4 |
```

#### E14 — Abschnitt 0, „Wenn eine Mac-Sitzung startet, endet oder abbricht“: nach dem Auslöser und vor dem Schliessen

Anker: `dann die passenden Blöcke ohne Rückfrage` · Art: **nach der Zeile**

```
| ☐ | Nach dem Auslöser: Ist Schritt 0 committet? Ohne Commit ist der Satz nicht angekommen ⇒ einmal Hinweis an den Betreiber, dann warten; keine Nachschau-Kette (29.09.2026) | 22.5 |
| ☐ | Vor dem Schliess-Auslöser das Alter des letzten Commits messen (`git --no-optional-locks log -1 --format=%ct`), erst ab 600 s auslösen (29.09.2026) | 22.8 |
```

#### E15 — Abschnitt 0, „Wenn ich ein fremdes Ergebnis bewerte“: „Widerspruch“ erst nach Wortlautprüfung

Anker: `Jede Zahl aus dem fremden Bericht an der Rohausgabe nachgerechnet` · Art: **nach der Zeile**

```
| ☐ | Vor dem Urteil „Widerspruch“ prüfen, ob die Registerstelle den gerechneten Fall wörtlich trifft (30.09.2026) | 9 |
```

#### E16 — Abschnitt 0, „Wenn ich einen Auftrag schreibe“: Fundstellen, Gegenleser, Übernahmegrenzen

Anker: `Belegt, erschlossen und offen getrennt` · Art: **nach der Zeile**

```
| ☐ | Eine Erwartung an ein Werkzeug nur mit Fundstelle im Werkzeug, sonst „vom Werkzeug abhängig, im Ergebnis beschreiben“ (Übergabe, Umzug 29.09.2026, Block 7 Nr. 1) | 18, P.4 |
| ☐ | Zahlen aus früheren Ergebnissen nur mit Fundstelle im Ergebnis (29.09.2026) | 18, P.4 |
| ☐ | `faltenplan.faltenplan()` ist kein Lesen (es startet einen Trockenlauf) — in nur lesenden Aufträgen verboten (29.09.2026) | 11 |
| ☐ | Übernahmegrenzen werden aus der Datei gemessen (Überschrift, Dateiende), nie als Zeilenzahl vorgegeben; der Gegenleser prüft gegen die Quelle (29.09.2026) | 22.10 |
| ☐ | Vor dem Übergeben liest ein frischer Helfer gegen — jede Zahl, Fundstelle und Werkzeug-Erwartung an der Quelle, bei Fable-Anfragen auch gegen 27.1; gestuft nach T2 | 22.10 |
```

#### E17 — Abschnitt 0, „Wenn ein Dokument mitgeht“: Fable-Anfrage als Kopierblock, Fable-Filter und Fable-Umzug

Anker: `Bei Fable: bestehender oder neuer Chat — in der Überschrift und im Text` · Art: **nach der Zeile**

```
| ☐ | Fable-Anfrage: Steht ihr voller Text als Kopierblock in DIESER Antwort? Repo und Ablage sind Archiv, nicht die Übergabe (Rüge 24.09.2026; erneut 29./30.09.2026) | 15, Austausch Nr. 5 |
| ☐ | An Fable nur vorgeprüfte Verfahrensfragen; vor der nächsten Anfrage Fables letzte Umzugsampel prüfen — über 300 000 zieht Fable zuerst um (30.09.2026) | 22.11 |
```

#### E18 — Abschnitt 0, neue Tabelle „Wenn Dateien abgelegt oder aus der Ablage gelesen werden“

Anker: `**Wenn ich ein fremdes Ergebnis bewerte (Cloud, Mac, Fable)**` · Art: **vor der Zeile** (als eigener Block)

```
**Wenn Dateien abgelegt oder aus der Ablage gelesen werden**

| | Regel | steht in |
|---|---|---|
| ☐ | Nach jedem `device_commit_files`: md5 und `wc -c` auf beiden Seiten, **vor** dem Auslöser. Jede Ablage aus einem frischen Stage-Pfad — auch wenn die Datei nach dem Bereitstellen noch geändert wurde (T7; am 29. und 30.09.2026 kam dreimal eine alte Fassung an, obwohl „written“ gemeldet war) | 23 |
| ☐ | Dateien für die Projektablage zuerst ins Arbeitsverzeichnis kopieren, md5 prüfen, dann `project_write` (29.09.2026) | 23 |
| ☐ | Abschriften aus der Ablage zweifach unabhängig, lange Texte in Teilen, `cmp` vor dem Ablegen (29.09.2026) | 23 |
| ☐ | Grosse Ablage-Dateien liest ein Helfer (Fundstellen); der Chat liest nur, was er für eine Entscheidung im Wortlaut braucht (29.09.2026) | 22.10 |
| ☐ | Aufträge, die eine 27.5-Streichung vollziehen, gehen nicht in die Ablage (29.09.2026) | 23 |
| ☐ | In der Ablage liegt von der Übergabe nur `UEBERGABE.md`; `UEBERGABE_ARCHIV.md` und abgeschlossene Dialoge und Aufträge nur im Repo (T5, Betreiber 30.09.2026) | 23 |
| ☐ | Kernlektüre beim Umzug aus dem Repo mit Abschnittsfilter; `project_read` nur als Rückfall — es liefert immer die ganze Datei (29.09.2026) | UMZUG 6 |

```

#### E19 — Abschnitt 3, Modellwahl: Verweis auf 22.12

Anker: `Ermessensspielraum.` (Satzende im Absatz „**Modell:** Standard ist …“) · Art: **nach der Zeile** (als eigener Absatz)

```
⭐ **Seit 29.09.2026 gilt dafür 22.12:** Sonnet nur für Mechanik — Fundstellen- und Zählhelfer, Dokumentationsaufträge mit wörtlich vorgegebenem Text —, und für Aufträge erst nach bestandener Probe. Register, Code, Messungen, Gegenleser, Bewertung und der steuernde Chat bleiben Opus mit Aufwand hoch.
```

#### E20 — Abschnitt 6d: M1–M3 schränken den Abschnitt ein (Betreiber 30.09.2026, 19:13)

Anker: `## 6d. Jede Entscheidung wird als anklickbare Frage gestellt — mit Empfehlung` · Art: **nach der Zeile** (als eigener Absatz)

```
> ⚠️⚠️ **Eingeschränkt durch den Betreiberentscheid vom 30.09.2026, 19:13** („Wir setzten es wie von dir Vorgeschlagen um“; Wortlaut: `UEBERGABE.md` bzw. `UEBERGABE_ARCHIV.md`, Nachtrag 30.09.2026, 19:13). Anlass: Der steuernde Chat hing wiederholt an der Auswahlkarte.
> - **M1:** Die Karte ist immer der letzte Schritt einer Antwort. Ergebnis, Dateien, Kopierblöcke, „Deine Aufgaben“ und Ampel sind vorher zugestellt (`SendUserMessage`). Hängt die Karte, fehlt nur die Karte.
> - **M2:** Höchstens eine Karte je Antwort, bis zu vier Fragen gebündelt.
> - **M3:** Karten nur für echte Betreiberentscheide: Freigaben für Register, Sperrliste, Signalpfad und Parameterdateien; Löschen und Ablage entfernen, Umzug, Geld, Unumkehrbares. Bei Handwerk entscheidet der steuernde Chat selbst und schreibt: „Vorgabe: X — gilt, wenn du nicht widersprichst“.
>
> Wo dieser Abschnitt „jede Entscheidung“ sagt, gilt er in diesem Rahmen. Wo er „nicht gesammelt ans Ende der Antwort“ sagt, gilt M1/M2: eine gebündelte Karte als letzter Schritt.
```

#### E21 — Abschnitt 22.10, 22.11, 22.12 (neu), vor Abschnitt 23

Anker: `## 23. Die Projektablage — Arbeitsfläche, nicht Träger` · Art: **vor der Zeile** (als eigener Block; der Block endet mit `---` und einer Leerzeile). Der Text ist ein `~~~`-Block.

~~~
### 22.10 Helfer-Agenten — ein Regelwerk für alle drei Rollen (Betreiber 29.09.2026)

Grundsatz (Fable 29a, Abschnitt 3): Ein Helfer darf finden, zählen und belegen —
nie deuten. Seine Ausgabe ist Fundstelle, Zahl oder Quelle. Eine Zusammenfassung
dient höchstens der Orientierung („wo steht was“); was in eine Anfrage, einen
Auftrag, einen Bericht oder eine Entscheidung eingeht, liest der Auftraggeber
selbst im Wortlaut an der Fundstelle. Jeder Einsatz bekommt eine Protokollzeile
(Art, Suchwort oder Frage, erlaubte Dateien, Ergebnis); jeder Auftrag an einen
Helfer nennt die erlaubten Dateien und das Leseverbot.

Steuernder Chat: (1) Web-Recherche — Quellen mit URL, selbst gegengelesen;
(2) Fundstellen- und Zählaufträge in Repo und Ablage; (3) Gegenleser vor jedem
Übergeben einer Fable-Anfrage und eines Auftrags: ein frischer Helfer, der den
Text nicht geschrieben hat, liefert eine Liste Satz · Behauptung · Quelle ·
stimmt/weicht ab — für jede Zahl, Fundstelle und Werkzeug-Erwartung; bei
Fable-Anfragen zusätzlich gegen Register 27.1 (steht ein Wert darin, den Fable
nicht sehen darf?). Befunde werden vor dem Übergeben eingearbeitet.

Fable: wie FABLE_ANTWORT_2026-09-29a, Abschnitt 3 (Fundstellen, Mechanik,
Websuche mit Einzelfreigabe; Leseverbot `docs/belege/`, `ergebnisse/`,
Trade-Listen, `BACKLOG*.md`).

Mac-Sitzungen: Helfer nur zum Suchen und Lesen innerhalb der Sitzung. Messung,
Beleg und Commit macht die Sitzung selbst; jeder Helfereinsatz steht im
Ergebnisdokument. Nicht gemessen: ob Sperrliste und `deny` aus
`.claude/settings.local.json` auch für die Helfer der Sitzung greifen — die
erste Sitzung, die einen Helfer einsetzt, prüft das als Schritt 0 und bricht
ab, wenn nicht.

Belege bleiben A8/A10: die Aussage eines Helfers ist eine Selbstauskunft.
Nie für Register, Commits, Aufträge schreiben oder Freigaben; ein Helfer
schreibt nichts ins Repo.

Probe statt Regel (Fable 29a: „Die Entscheidung fällt an der Messung, nicht an
der Ersparnis“): Über die ersten drei Gegenlese-Durchgänge zählt der steuernde
Chat je Durchgang die Befunde, die er selbst übersehen hätte, und die
geschätzten Tokens. Hat keiner der drei einen solchen Befund, fällt das
Gegenlesen weg; sonst wird es Regel. Das Ergebnis steht in der Übergabe.

⭐ **Ergebnis der Probe (29.09.2026, 14:52): Das Gegenlesen ist Regel.** 3 von 3
Durchgängen fanden Befunde, die sonst übergeben worden wären (Übergabe,
Nachträge 29.09.2026, 12:25, 13:20 und 14:52).

⭐ **Ergänzung 30.09.2026, 19:13 — Tokens sparen, ohne dem Projekt zu schaden
(Betreiberentscheid, T1–T4):**
- **T1:** Helfer schreiben ihren Volltext in eine Datei (Scratchpad oder
  Ausgabeordner). Dem Chat geben sie nur rund 20 Zeilen zurück: Urteile,
  Abweichungen, Offenes.
- **T2:** Gegenlesen gestuft: zwei unabhängige Parallelläufe nur für Zahlen und
  Zitate, die ins Register oder an Fable gehen; sonst ein Gegenleser auf das
  fertige Ergebnis.
- **T3:** Helfer bekommen Zeilenbereiche aus `REGISTER_INDEX.md` und die
  bekannten Fundstellen mit.
- **T4:** Sonnet-Probe beim Fundstellen-Check — Sonnet und Opus parallel, dann
  Vergleich (Ergebnis in 22.12).
- Grosse Ablage-Dateien liest ein Helfer; der Chat liest nur, was er für eine
  Entscheidung im Wortlaut braucht (29.09.2026).

### 22.11 Fable-Filter — nur Verfahrensfragen, vorgeprüft (Betreiber 29.09.2026)

1. An Fable gehen nur Verfahrensfragen vor dem signierten Tag: Registertext,
   seine Lesart, der Sichtschutz (27). Handwerk nach 6d — Arbeitsweise, Ablage,
   Umzug, Agenten, Dateinamen, Lesarten eigener Werkzeuge — entscheiden der
   steuernde Chat und der Betreiber (Auswahlkarte). Reine Kenntnis geht nicht
   hin oder als eine Zeile.
2. Vorprüfung durch Opus (Mac-Sitzung oder Helfer nach 22.10): Jede Frage wird
   vorher gegen das ganze Register und den Code geprüft. Fable bekommt nur, was
   dort offen ist — je Frage mit Fundstelle und Neigung des steuernden Chats.
3. Form: nur Fragen mit Fundstellen, keine kopierten Sammlungen; Antwort je
   Frage „einverstanden“ oder „anders, weil …“, Registertext nur als R-Block;
   „In einfacher Sprache“ schreibt der steuernde Chat.
4. Takt nach Bedarf: wenn eine Frage einen Auftrag blockiert oder genug echte
   Verfahrensfragen beisammen sind — nicht täglich.
5. Fables Probe aus 29a (Register Teil 1–3 über einen Fundstellen-Helfer) wird
   unterstützt; die Übergabe an einen neuen Fable-Chat nennt sie.

⭐ **Ergänzung 30.09.2026:** Vor der nächsten Anfrage an Fable prüft der
steuernde Chat Fables letzte Umzugsampel nach den Schwellen von UMZUG 3. Steht
sie über 300 000 (🔴), zieht Fable zuerst um. Anlass: Fable meldete in 30a
„🟡 · ca. 450 000“.

### 22.12 Sonnet 5.5 — nur Mechanik, erst eine Probe (Betreiber 29.09.2026)

Betreiberentscheid 29.09.2026, ca. 14:05, per Auswahlkarte: „Nur Mechanik, erst
Probe (Empfohlen)“ — ausdrücklich nur, wenn die Qualität des Projekts nicht
leidet.

- Sonnet übernimmt Fundstellen- und Zählhelfer (Agent mit `model: sonnet`) und
  reine Dokumentationsaufträge mit wörtlich vorgegebenem Text.
- Für Dokumentationsaufträge läuft zuerst **ein** Probeauftrag, abgenommen mit
  `numstat`, `diff` gegen den Auftragstext und der Zahl der Treffer je
  Einfügestelle. Hält er, wird es Regel für diese Klasse.
- Register, Code, Messungen, Gegenleser, Bewertung und der steuernde Chat
  bleiben Opus mit Aufwand hoch.
- Es gibt keinen eigenen Sonnet-Chat (29.09.2026, 14:10: vom steuernden Chat
  auf eine Betreiberfrage verneint, mit Begründung). Sonnet läuft
  nur als Helfer oder als Mac-Sitzung je Auftrag, mit dem Modell im Kopf des
  Auftrags (Abschnitt 3). Umzug und Ampel betreffen Sonnet nicht.
- ⚠️ Lücke: Der Wächter (`docs/werkzeuge/sitzungswaechter/starte_sitzung.sh`)
  startet ohne Modellwahl, also mit Opus. Bis zu einem Umbau (Handwerk mit
  Freigabe, weil der Wächter geändert wird) setzt der Betreiber das Modell in
  der Sitzung selbst (Vorgabe des steuernden Chats, 30.09.2026); Schritt 0 hält
  fest, welches Modell läuft.
- **Probe Helfer (T4), 30.09.2026:** E-2-Inventar, Sonnet und Opus parallel mit
  demselben Auftrag. Beide fanden alle 38 R-Blöcke ohne Lücke; Sonnet brauchte
  rund 253 000 Tokens und 9 Minuten, Opus rund 196 000 und 5 Minuten (Angaben
  der Werkzeugrückmeldung). Die Zählungen der Regeln wichen in der Körnung ab
  (45 gegen 54), der Befund war gleich. Sonnet war hier nicht billiger. Eine
  Probe, noch keine Regel. Fundstelle: Übergabe, Nachtrag 30.09.2026, ca. 22:05.
- **Probe Dokumentationsauftrag:** TB-125; Ergebnis in
  `docs/ERGEBNIS_TB-125_regelwerk_nachtrag.md`.

---

~~~

### Datei `docs/projektfuehrung/BACKLOG.md`

#### E22 — Abschnitt 4, K4s (Betreiber 29.09.2026, 07:55)

Anker: `| **K4r** |` (Zeilenanfang) · Art: **nach der Zeile**

```
| **K4s** | ⭐ **UMZUG NACH TOKENVERBRAUCH (29.09.2026, Betreiberentscheidung per Auswahlkarte).** Der steuernde Chat zählt den Verlauf mit und schlägt ab ~200–250k Tokens den Umzug am nächsten sauberen Stand vor (UMZUG 3, Zeile 6). Die Eröffnung liest nur noch die Kernlektüre (~40 KB statt 267 KB, gemessen). ⚠️ Die Zählung ist eine Schätzung, der Kontextfüllstand ist nicht ablesbar. **Preis, benannt:** Eine Regel ausserhalb von ARBEITSWEISE 0 greift erst, wenn ihr Abschnitt nachgeschlagen wird. Wortlaut und Messung: `UEBERGABE_ARCHIV.md`, Nachtrag 29.09.2026, 07:55. Eingearbeitet mit TB-125 |
```

#### E23 — Abschnitt 4, K4t (Betreiber 29.09.2026, 09:20; ersetzt die Fassung 08:50)

*Gegenüber der Quelle beabsichtigt geändert: „als Probe über drei Durchgänge“ ⇒ „seit 29.09.2026, 14:52 Regel (3 von 3)“; Pfad `UEBERGABE_ARCHIV.md`; Einarbeitungsvermerk. E22 ebenso: Pfad und Einarbeitungsvermerk.*

Anker: der erste Satz von E22, `| **K4s** | ⭐ **UMZUG NACH TOKENVERBRAUCH` · Art: **nach der Zeile** (also direkt nach E22)

```
| **K4t** | ⭐ **HELFER-AGENTEN, EIN REGELWERK FÜR ALLE DREI ROLLEN, UND UMZUGSAMPEL (29.09.2026, zwei Auswahlkarten).** Grundsatz „finden, zählen, belegen — nie deuten“ (Fable 29a) für steuernden Chat, Fable und Mac-Sitzungen; Gegenleser vor jeder Übergabe — seit 29.09.2026, 14:52 Regel (3 von 3). Offen: ob `deny` für Helfer der Mac-Sitzung greift (erste Nutzung misst). Umzugsampel als letzte Zeile jeder Antwort des steuernden Chats. Wortlaut: `UEBERGABE_ARCHIV.md`, Nachtrag 29.09.2026, 09:20; eingearbeitet mit TB-125 (ARBEITSWEISE 22.10, UMZUG 3) |
```

#### E24 — Abschnitt 0, „Wenn ein Dokument mitgeht“: Ausnahme für Fable-Anfragen

Anker: `Als Datei, nie als Chat-Text zum Herauskopieren — für alle vier Wege` · Art: **ersetzt die Zeile**. Grund: Die Zeile stand ohne Ausnahme und widersprach der Kopierblock-Regel (ARBEITSWEISE 15, Austausch Nr. 5; Rüge 24.09.2026).

```
| ☐ | Als Datei, nie als Chat-Text zum Herauskopieren — für alle vier Wege. Ausnahme: Eine Fable-Anfrage steht als Kopierblock in der Antwort (15, Austausch Nr. 5) | 2 |
```

## Schritt B — Nachweis

B1. `docs/belege/TB-125/einfuegungen.txt` (siehe oben). **Soll:** jede der 24 Einfügungen E1–E24 mit Anker vorher 1, ausgeführt, Text nachher 1.

B2. `git diff --numstat` je Datei ⇒ `b2_numstat.txt`. Entfernte Zeilen dürfen **nur** aus den Ersetzungen stammen:
- UMZUG: E4 (1 Zeile) und E5 (die Zeilen zwischen den Ankern einschliesslich);
- ARBEITSWEISE: E10, E11, E12, E13, E24 (je 1 Zeile);
- BACKLOG: keine.

Die Sitzung zählt die Soll-Zahl für E5 vorher aus der Datei und schreibt Soll und Ist hin.

B3. **Zeichengleichheit (Kern der Probe):** Ein Skript (`docs/belege/TB-125/b3_vergleich.py`) liest je Einfügung den Text aus diesem Auftrag und prüft, dass er in der Zieldatei **genau einmal als zusammenhängender Block** vorkommt (Bytevergleich, keine Normalisierung) ⇒ `b3_vergleich.txt`, je E-Nummer „gleich“ oder „abweichend“ mit der ersten abweichenden Stelle.

B4. `git diff` der drei Dateien ⇒ `b4_diff.txt` (für den steuernden Chat zur Abnahme).

Commit `TB-125 A/B: Regelwerk-Nachtrag eingetragen, Nachweis`, pushen.

## Schritt C — Abgabe

C1. `docs/ERGEBNIS_TB-125_regelwerk_nachtrag.md` enthält:
- Kopf wie üblich, mit dem Modell aus 0b;
- Kurz-Tabelle: Einfügungen ausgeführt/nicht ausgeführt, B2 Soll/Ist, B3 gleich/abweichend;
- ein Abschnitt „Probe nach 22.12“: Modell, Zahl der Werkzeugaufrufe, was nicht auf Anhieb gelang;
- „Nicht getan“: Die Einarbeitungspunkte ohne vorbereiteten Wortlaut bleiben für einen späteren Auftrag:
  - K2h/K2f (PRUEFPRINZIPIEN);
  - die drei Trägerstellen (TB-119 Nr. 2);
  - der kalte Leser ohne Gedächtnis;
  - Fables 29a Abschnitt 1–3;
  - „neue Fable-Antworten über `project_info` finden“ (Übergabe, Umzug 29.09.2026, 07:15, Block 9);
  - Fables Umzugshinweis aus 30a (gehört zum Fable-Umzug, nicht ins Regelwerk);
- „In einfacher Sprache“.

C2. Journalblock ans Ende von `JOURNAL.md`; Buchstabe gemessen: letzter Block plus eins (nach TB-124 voraussichtlich **DW**). Mit Quellenzeile.

C3. Abgabe-Commit `TB-125 Abgabe: Ergebnis, Journal`, pushen. Danach `git status --porcelain` nach dem letzten Commit ⇒ `docs/belege/TB-125/c3_porcelain.txt`, kleiner letzter Commit, pushen.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a weicht ab.
- Eine Datei ausserhalb der drei Zieldateien (und der Belege, des Ergebnisses und des Journals) müsste geändert werden.
- `git push` scheitert zweimal.

Eine einzelne Einfügung mit Ankerzahl ≠ 1 ist **kein** Abbruch: Sie wird ausgelassen und benannt. Bei Abbruch: committen, was an Belegen da ist, Grund in `docs/belege/TB-125/abbruch.txt`, pushen, melden.

## In einfacher Sprache

Die Regeln, die in den letzten zwei Tagen entstanden sind, kommen jetzt an ihren festen Platz. Die Sitzung schreibt nur ab, und zwar per Skript direkt aus diesem Auftrag. Danach wird maschinell geprüft, dass jeder Text genau so angekommen ist, wie er hier steht. Hält das mit Sonnet, darf Sonnet künftig solche Abschreibarbeiten übernehmen.

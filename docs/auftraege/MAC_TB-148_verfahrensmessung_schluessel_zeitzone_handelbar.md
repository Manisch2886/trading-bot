# TB-148 Verfahrensmessung durch Lesen: Schlüssel der Zuteilung, Zeitzone des Schnitts, Träger der Ausstiege, Handelbar-Tag — an: Mac-Sitzung (Claude Code)

**Stand:** Gebaut am 09.10.2026 von einem Helfer des steuernden Chats, gegengelesen (Helfer GEGEN148); ausgelegt wird nach TB-147, HEAD und Fundstellen setzt der Bau dann neu.

**Sitzungstitel:** `TB-148` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main` am HEAD `3ecde8747cb94b6ec14b70aa07e8c735fbea11e6` · **Start:** über den Sitzungswächter (`starte_TB-148`), nicht von Hand; er legt keinen Satz ins Fenster, den fügt der Betreiber in der App ein.
**Dieser Auftrag:** `docs/auftraege/MAC_TB-148_verfahrensmessung_schluessel_zeitzone_handelbar.md`, wird in Schritt 0 mitcommittet. **Belege:** `docs/belege/TB-148/`. **Ergebnis:** `docs/ERGEBNIS_TB-148_verfahrensmessung_schluessel_zeitzone_handelbar.md`. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.
**Ziel:** Fünf Fragen des Verfahrensprüfers (Fable) sind durch Lesen des Codes beantwortet — je Frage nur das Wie oder nur das Ob, jede Aussage mit Fundstelle. Es läuft kein Programm, keine Trade-Liste wird geöffnet, keine Ergebniszahl genannt.
**Bauart:** Verfahrensmessung nach Register 27.2 wie TB-138 und TB-140 (`docs/auftraege/MAC_TB-138_verfahrensmessung_snapshot.md`, `docs/auftraege/MAC_TB-140_verfahrensmessung_voraussetzungen.md`, dort Teil 2 „Lesen des Codes“, Z. 1083–1085); Schritt 0 und Abgabe in der Form von TB-146. **Anders als alle drei:** kein Messskript, kein eigenes Werkzeug des Auftrags, kein Interpreter — die Sitzung liest mit dem Lese- und dem Suchwerkzeug von Claude Code und schreibt Fundstellen auf. Es gelten nur die Schritte, die hier stehen.
**Reihenfolge:** Schritt 0 → A (Modus) → M1, M2, M3, M4, M5 (nach jedem Messpunkt Commit und Push) → D (Messblöcke, Ergebnis, Journalblock, Abgabe).

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei** (Betreiberentscheid 26.09.2026; Formel wie TB-138, `docs/auftraege/MAC_TB-138_verfahrensmessung_snapshot.md` Z. 10, und TB-140, `docs/auftraege/MAC_TB-140_verfahrensmessung_voraussetzungen.md` Z. 14). Betreiber am 09.10.2026, 22:53: „Ich möchte nun dass du die kommenden 8 Stunden selbstständig ohne meine Bestätigungen weiterarbeitest. Stehen Fragen an verwende deine Empfehlung. Alle Fragen die du nicht beurteilen kannst, sammle diese und stelle mir diese bei meiner Rückkehr.“ und 22:57: „fahre ansonsten im Backlog fort“ (`docs/projektfuehrung/UEBERGABE.md` im Arbeitsbaum beim Bau, Z. 2934 und Z. 2939). Dass TB-148 diese fünf Fragen durch Lesen misst, ist Vorgabe des steuernden Chats: `UEBERGABE.md`, Nachtrag „Nachtrag 09.10.2026, 23:51 — Fable 09.10.a bewertet (Eintrag empfohlen); TB-147 gebaut, gegengelesen, ausgelegt, Sitzung angelegt; TB-148 und TB-149 im Bau; Cloud-Auftrag TB-150 ausgegeben; vier weitere Betreibersätze“ (Z. 2937), dort Z. 2944, wörtlich:

> - **TB-148 — Vorgabe des steuernden Chats:** Die Messungen, die Fable vor dem Bau der zwei Erzeuger und vor der Neuerzeugung der Listen verlangt, und die Messbitte aus Register 55.8 Nr. 5 gehen als **ein** Mac-Auftrag TB-148, Verfahrensmessung durch Lesen nach 27.2: M1 Schlüssel der Zuteilung (55.8 Nr. 5) · M2 Zeitzone von `open_time` und Go-Live-Schnitt (55.8 Nr. 5; Antwort 09.10.a, R86 (e)) · M3 Träger der Ausstiege (R84 (e)) · M4 Einstieg vor dem Handelbar-Tag, je Bot (R87 (d)) · M5 Quelle des Handelbar-Tags („Unsicher“ 7). Kein Lauf, kein Import, keine Trade-Liste, keine Ergebniszahl; Dateien der Sperrliste nur lesen; geändert wird nur Dokumentation. Er startet nach TB-147; er hängt nicht am Registereintrag (Vorbild: TB-140 gab am 07.10.2026, 11:07 ab, die Antwort 07.10.a kam 22:57 ins Repo, Register 55 um 23:16; 36.3 nennt Messung und Registereintrag nicht — Aussagen des Helfers BAU148). […] (gekürzt nach 905 von 1093 Zeichen)

**An der Sperrliste gemessen** (Helfer BAU148, 10.10.2026, am HEAD `3ecde87`): Im gültigen Abbild `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json` (sha256 beginnt `46f0ad5d1d83a253`, dasselbe wie in TB-140 Z. 16; das jüngste von 7 Abbildern) liegt keiner der 22 Pfade der Liste `eingefroren` und keiner der 11 Pfade in `hashes` der 14 Punkte unter `docs/belege/TB-148/`, auf dem Ergebnis, auf `docs/projektfuehrung/JOURNAL.md` oder auf einem der drei Pfade aus 0a; die Liste `bestimmt` ist leer. Dieser Auftrag schreibt nur unter `docs/`. Von den 63 **Startdateien** — so heissen hier die Dateien der Tabellen M1 bis M5 und „Neun Bots“ (ohne die „Weiteren Treffer“), bei denen die Sitzung zu lesen beginnt — stehen 4 auf dem Abbild — in `eingefroren`: `research/vorregistrierung/registerdaten.py`, `research/vorregistrierung/faltenplan.py`, `research/vorregistrierung/benchmark.py`; in `hashes` (dazu, nicht in `eingefroren`): `shared/zuteilung.py`. **Nur lesen.**

**Am Register gemessen** (Helfer BAU148, am HEAD): Abschnitt 10 „Die Sperrliste“ steht in `docs/VORREGISTRIERUNG_neuselektion.md` Z. 971–1177. Von den 63 Startdateien nennt der Haupttext der Punkte 1 bis 14 diese 4 mit Namen — **nur lesen:**

- `shared/zuteilung.py` — Abschnitt 10 Punkt 10 (Register Z. 1101); herkunft.py `SPERRLISTE_DATEIEN`
- `research/vorregistrierung/registerdaten.py` — Abschnitt 10 Punkt 1 (Register Z. 996), Punkt 3 (Register Z. 1017), Punkt 7 (Register Z. 1052); herkunft.py `EINGEFROREN`
- `research/vorregistrierung/faltenplan.py` — Abschnitt 10 Punkt 2 (Register Z. 999); herkunft.py `EINGEFROREN`
- `research/vorregistrierung/benchmark.py` — Abschnitt 10 Punkt 4 (Register Z. 1019), Punkt 6 (Register Z. 1050); herkunft.py `EINGEFROREN`

Nur in einer Tatsachennotiz zu Punkt 9 genannt (`backtest_*.py`, Register Z. 1083, 1089, 1095) — **nur lesen:** die 9 Backtest-Module der Tabelle „Neun Bots“. Über `research/vorregistrierung/herkunft.py::SPERRLISTE_DATEIEN` (Z. 102–106) erfasst, in Abschnitt 10 ohne Dateinamen (Punkt 11, Register Z. 1103) — **nur lesen:** je Bot `equity_simulation.py`, `multi_symbol_optimise.py` und `multi_symbol_walk_forward.py` (27 Dateien). Für die Sitzung gilt dasselbe für jede Datei ausserhalb von `docs/`: lesen, nie ändern.

**Die Sitzung darf ändern, und nichts sonst:**

| Pfad | was |
|---|---|
| neu: `docs/belege/TB-148/…` | Rohausgaben aus Schritt 0, A und D; je Messpunkt `m<n>_fundstellen.md`; `leseprotokoll.md` |
| neu: `docs/ERGEBNIS_TB-148_verfahrensmessung_schluessel_zeitzone_handelbar.md` | das Ergebnis |
| `docs/projektfuehrung/JOURNAL.md` | ein Block, nur eingefügt (Schritt D2) |

Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt (die Einträge aus 0a); das ist kein Ändern im Sinn dieser Liste.

⛔ **Nicht erlaubt, je mit dem, wovor es schützt:**

- **Ein Programm des Repos ausführen oder importieren** — auch nicht `python -c`, `pytest`, `faltenplan`, ein Backtest, ein Lader, `trading-env/bin/python3` in irgendeiner Form. *Schützt:* vor einem Lauf, der rechnet oder schreibt (27.2 erlaubt die Messung, nicht den Lauf; `faltenplan.faltenplan()` startet einen Trockenlauf: TB-138 Z. 23), und vor `__pycache__` im Arbeitsbaum.
- **Eine Trade-Liste oder etwas unter `ergebnisse/` öffnen** — keine `*.csv`, `*.parquet`, `*.db`, nichts unter `data/`, `snapshots/`, `logs/`, `research/tb24_haltedauern/daten/` und unter keinem Ordner `ergebnisse/`; auch nicht über eine Suche. *Schützt:* den Sichtschutz des Verfahrensprüfers (Register 27.1). Gesucht wird nur in benannten Dateien, nie rekursiv über einen Ordner (so entstand die Abweichung in TB-140: `docs/ERGEBNIS_TB-140_verfahrensmessung_voraussetzungen.md` Z. 427).
- **Eine Zahl nennen, die Ergebnis eines Laufs ist** — keine Trade-Zahl, Rendite, Kennzahl, kein Kurs; aus `live_params.py` kein Text (so TB-140: `docs/ERGEBNIS_TB-140_verfahrensmessung_voraussetzungen.md` Z. 425). *Schützt:* 27.1. Zulässig sind Dateinamen, Funktionsnamen, Zeilennummern, Quelltext als Wortlaut und Konstanten des Verfahrens. Steht in einem Kommentar oder Docstring des gelesenen Quelltexts eine Ergebniszahl eines Laufs, liest die Sitzung weiter, schreibt die Zahl nirgends hin und nennt im Leseprotokoll nur den Ort (Datei:Zeile) mit dem Vermerk ‚Ergebniszahl im Quelltext, nicht wiedergegeben‘; im Feld „Wortlaut“ steht an ihrer Stelle „[…]“.
- **Eine Datei ausserhalb der Tabelle oben ändern,** besonders eine Datei der Sperrliste, Register, Registerkopie, `UEBERGABE.md` nach Schritt 0, `BACKLOG.md`, frühere Belegordner. *Schützt:* Der Auftrag misst; ein Befund wird gemeldet, nicht behoben.
- **`git add -A`, `git add .`** *Schützt:* vor einem Commit mit Dateien, die niemand genannt hat; jeder Commit nennt seine Dateien mit Namen.
- **Ein Hilfsskript anlegen,** eine Schleife oder einen Befehl bauen, der hier nicht wörtlich steht — Ausnahmen: das Anhängen weiterer Pfade in den zwei Blöcken von D0 und das Füllen der Platzhalter `<n>`, `<Kennung>`, `<⟨S0⟩>`, `<⟨F⟩>`. *Schützt:* vor einer Form, die Claude Code ablehnt (TB-146 endete so: Commit `e39cc44`, „TB-146 Abbruch in Schritt E: Claude Code lehnte einen Aufruf ab; 14 Stücke eingefügt, Belege“), und vor Fehler Nr. 39.
- **Unter-Agenten einsetzen.** Die Sitzung liest selbst. Das Such- und das Lesewerkzeug von Claude Code sind erlaubt, aber nur auf den erlaubten Pfaden — nie über `ergebnisse/`, Trade-Listen, `BACKLOG*.md`, `docs/belege/` (ausser dem eigenen Ordner `docs/belege/TB-148/`). *Schützt:* vor einem Lese-Helfer wie in TB-140 (`docs/ERGEBNIS_TB-140_verfahrensmessung_voraussetzungen.md` Z. 427–429).
- **Etwas ins Scratchpad oder ausserhalb des Repos schreiben** — Ausnahme: `$TMPDIR/tb148_*.txt` für `git status --porcelain`. *Schützt:* 0a und D3 zählen die Einträge des Arbeitsbaums; was ausserhalb liegt, sieht niemand.
- **Ein Urteil über Folgen.** Was aus einem Fund folgt — etwa ein Register-Code-Widerspruch nach R87 (d) —, entscheidet der Verfahrensprüfer. *Schützt:* die Trennung von Messung und Entscheid; das Ergebnis nennt Fundstellen, keine Empfehlung.

## Belegt · erschlossen · offen

- **Belegt** (Helfer BAU148, am HEAD `3ecde87` per `git show HEAD:<pfad>` und `ast.parse`, nichts ausgeführt): jede Zeilenangabe dieses Auftrags; die Wortlaute der fünf Fragen (per Skript aus der Quelle, zeichengleich); die Liste der neun Bots aus `research/vorregistrierung/registerdaten.py::BOTS` (Z. 130–140) und das Backtest-Modul je Bot aus `research/mtm_drawdown/messung.py::BACKTEST_MODUL` (Z. 72–82), beide Schlüsselmengen gleich. Die Antwort 09.10.a lag beim Bau am HEAD verfolgt im Repo.
- **Erschlossen:** dass die Einstiegspunkte die richtigen Anfänge sind — sie stammen aus Namenssuchen über 481 der 482 verfolgten `*.py` ausserhalb von `docs/`, `data/`, `snapshots/`, `logs/`, `ergebnisse/` (eine Datei mit „trades“ im Namen blieb ungeöffnet), nicht aus einem verfolgten Aufrufpfad. Die Sitzung folgt den Aufrufen selbst. Welches Skript die neun Trade-Listen erzeugt (der „Listen-Erzeuger“ der Antwort), hat der Helfer nicht gesucht; `research/mtm_drawdown/messung.py` Z. 71 nennt als Herkunft der Listen `collect_all_trades -> get_trades_for_symbol`.
- **Wortprüfung gegen die Berechtigungslisten** (Bauskript, bei jedem Bau neu): `.claude/settings.local.json` führt in `permissions.deny` 70 und in `permissions.ask` 14 Einträge (davon `Bash(…)`: 45 und 0). Von den 16 Befehlswörtern dieses Auftrags (erstes Wort jedes Befehls und jedes Wort nach `;`, `&&`, `|`, `$(`; aus 33 Befehlszeilen) ist **eines (deny: `git`; 10 Muster beginnen mit `git`)** erstes Wort eines Musters dort; kein Muster trifft eine Befehlszeile. Gegenprobe: `chmod` (nach dem Gegenleser von TB-147 im abgelehnten Aufruf von TB-146) ist in `deny` erstes Wort eines Musters: ja. Die Muster für `Edit`/`Write` treffen keinen der Schreibpfade (Näherung per `fnmatch`). `permissions.allow` führt 83 Einträge, darunter pauschal `Bash(*)`, `Read(*)`, `Edit(*)`, `Write(*)`, `Glob(*)`, `Grep(*)`, `WebFetch(*)`, `TodoWrite(*)`; ein eigenes `Bash`-Muster haben dort `cp`, `echo`, `git`, `grep`, `md5`, `tr`, `wc`, nur über `Bash(*)` laufen `cmp`, `ps`. Einen Eintrag `defaultMode` führt die Datei nicht.
- **Offen — misst die Sitzung, nie raten:** Modus der Sitzung (Schritt A) · Kennung des Journalblocks (am HEAD ist die letzte EM, `JOURNAL.md` Z. 10332; diesen Block hat TB-147 gesetzt) · die fünf Antworten.
- **R84 bis R89 sind noch nicht im Register eingetragen.** Die Sitzung zitiert sie als „Antwort 09.10.a, R84 (e)“ usw. mit Datei und Zeile, nie als Registerstelle.

## Schritt 0 — Sicherung, Ausgang

**0a.** Zuerst, vor allem anderen und bevor `docs/belege/TB-148/` entsteht, diese drei Blöcke:

```
git status --porcelain > "$TMPDIR/tb148_0a.txt"
```

```
git status --porcelain
```

```
git rev-parse HEAD
```

Soll: HEAD `3ecde8747cb94b6ec14b70aa07e8c735fbea11e6` und in der Ausgabe des zweiten Blocks genau diese drei Einträge (Reihenfolge egal); jeder andere oder weitere Eintrag: **ABBRUCH**.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-148_verfahrensmessung_schluessel_zeitzone_handelbar.md
```

Dann der Commit, die drei Pfade mit Namen:

```
git add docs/auftraege/AKTUELLER_AUFTRAG.md docs/projektfuehrung/UEBERGABE.md docs/auftraege/MAC_TB-148_verfahrensmessung_schluessel_zeitzone_handelbar.md
git commit -m "TB-148 Schritt 0: Stand des steuernden Chats vor TB-148"
git push
git rev-parse HEAD
```

Der Commit heisst im Folgenden **⟨S0⟩**; die letzte Zeile gibt seine Kennung. Für jeden Commit dieses Auftrags gilt: Die Schlusszeilen, die Claude Code selbst an eine Commit-Nachricht hängt, sind erlaubt, in der Form, die Claude Code dafür üblicherweise nimmt; das Verbot von Heredoc, `cat >` und `echo >` gilt für Dateien, nicht für die Commit-Nachricht. Der Beleg zu 0a wird in Schritt A abgelegt, sobald der Ordner da ist. **0b entfällt:** Mit dem HEAD aus 0a und ohne weiteren geänderten Pfad steht jede Datei, die dieser Auftrag nennt, am Stand der Zeilenangaben; Zeilen und md5 der gelesenen Dateien misst die Sitzung am Schluss in D0.

## Schritt A — Modus messen, bevor gelesen wird

Ein Aufruf, eine Zeile (`$p` lebt nur in dieser einen Shell):

```
p=$$; while [ "$p" -gt 1 ]; do case "$(ps -o comm= -p "$p")" in claude|*/claude) break ;; esac; p=$(ps -o ppid= -p "$p" | tr -d ' '); done; echo "EIGEN=$p"; ps -o command= -p "$p"
```

Die Ausgabe schreibt die Sitzung wörtlich nach `docs/belege/TB-148/a_modus.txt` (Schreibwerkzeug). Soll: Die Prozesszeile trägt `--permission-mode manual`; sonst **ABBRUCH** — nichts ist gelesen, das in der Meldung als Erstes sagen. Dazu die eigene Aussage der Sitzung zu ihrem Berechtigungsmodus (oder „nicht bekannt“), als Aussage gekennzeichnet. Mit dieser Datei entsteht der Ordner `docs/belege/TB-148/`; erst jetzt den Beleg zu 0a ablegen:

```
cp "$TMPDIR/tb148_0a.txt" docs/belege/TB-148/0a_status.txt
cmp "$TMPDIR/tb148_0a.txt" docs/belege/TB-148/0a_status.txt
```

Soll: `cmp` ohne Ausgabe. *Schützt (Modus):* vor einer Sitzung, die anders läuft, als der Auftrag sie voraussetzt (Form wie TB-146, dort Schritt A).

## Schritt M — die fünf Messpunkte

**So wird gelesen.** Mit dem Lesewerkzeug von Claude Code (Datei, Zeilenbereich) — kein Shell-Aufruf je Datei. Gesucht wird mit dem Suchwerkzeug von Claude Code: in einer benannten Datei oder mit dem Dateimuster `*.py` unter `strategies/` oder `shared/`; unter `research/` nur in benannten Dateien. Keine Unter-Agenten. Zeilen und md5 der gelesenen Dateien misst die Sitzung am Schluss in zwei Blöcken (D0).

**Einstiegspunkte — die Sitzung folgt den Aufrufen selbst weiter und nennt jede weitere gelesene Datei.** Die Tabellen sagen, wo sie beginnt. „Wie gefunden“ beschreibt die Suche des Helfers, nicht den Inhalt; der Helfer hat keine der fünf Fragen beantwortet. **SL** = Nähe zur Sperrliste wie unter „Freigabe“: S1 im Haupttext von Abschnitt 10 genannt, S2 nur in einer Tatsachennotiz, S3 nur über `herkunft.py`. Passt eine Zeilenangabe nicht (anderer Name an der Stelle): die Funktion über ihren Namen suchen und es unter „Abweichungen“ nennen.

**Form der Antwort,** je Messpunkt in `docs/belege/TB-148/m<n>_fundstellen.md` (Schreibwerkzeug, nie Heredoc) und ebenso im Ergebnis:

| Nr. | Aussage | Fundstelle (Datei, Zeile) | Wortlaut (höchstens 200 Zeichen) | belegt · erschlossen · offen |
|---|---|---|---|---|

„Belegt“: Die Aussage steht in der zitierten Zeile. „Erschlossen“: Sie folgt aus mehreren zitierten Zeilen; die Kette steht dabei. „Offen“: nicht gelesen oder nicht entscheidbar. Kann die Sitzung eine Frage durch Lesen nicht entscheiden, schreibt sie **„durch Lesen nicht entscheidbar“** und warum — sie führt nichts aus, um es zu entscheiden. Jede Aussage sagt nur das Wie oder das Ob, das die Frage verlangt: nicht wie oft, nicht mit welcher Wirkung, nicht was daraus folgt.

**Leseprotokoll** `docs/belege/TB-148/leseprotokoll.md`: jede gelesene Datei mit gelesenem Zeilenbereich und Messpunkt, dazu die Vermerke ‚Ergebniszahl im Quelltext, nicht wiedergegeben‘ mit Datei:Zeile; fortgeschrieben nach jedem Messpunkt. Zeilen und md5 je Datei trägt die Sitzung in D0 nach.

**Nach jedem Messpunkt** committen und pushen, jede Datei mit Namen — für M1 (mit den zwei Belegen aus Schritt 0 und A):

```
git add docs/belege/TB-148/0a_status.txt docs/belege/TB-148/a_modus.txt docs/belege/TB-148/m1_fundstellen.md docs/belege/TB-148/leseprotokoll.md
git commit -m "TB-148 M1: Fundstellen"
git push
```

für M2 bis M5 mit `<n>` = 2 … 5:

```
git add docs/belege/TB-148/m<n>_fundstellen.md docs/belege/TB-148/leseprotokoll.md
git commit -m "TB-148 M<n>: Fundstellen"
git push
```

### Neun Bots — für M2, M3 und M4

Liste aus `research/vorregistrierung/registerdaten.py::BOTS` (Z. 130–140), Backtest-Modul aus `research/mtm_drawdown/messung.py::BACKTEST_MODUL` (Z. 72–82); jede Datei liegt unter `strategies/<Bot>/`. `mso` = `multi_symbol_optimise.py` (S3), `es` = `equity_simulation.py` (S3), `wf` = `multi_symbol_walk_forward.py` (S3); das Backtest-Modul ist S2. Zahlen sind Zeilen am HEAD.

| Bot | Markt, Zeitrahmen | `mso`: Lader · Scan `get_trades_for_symbol` · `open_time` · `MIN_HISTORY` | Backtest-Modul: `run_backtest` · weitere | `es`: `collect_all_trades` · `simulate_portfolio` | `wf`: Lader |
|---|---|---|---|---|---|
| `elliott_wave` | krypto, 1h | 53–90 · 93–112 · 63 · 50, 83, 84 | `backtest_elliott.py` 103–164 · `simulate_trade` 75–100 | 70–90 · 112–138 | — |
| `t3_supertrend` | krypto, 4h | 50–87 · 90–100 · 59, 79 · 46, 80, 81 | `backtest_trend.py` 67–137 | 61–87 · 106–132 | — |
| `rsi2_crypto` | krypto, 1d | 59–93 · 96–99 · 66, 85 · 16, 56, 86, 87 | `backtest_rsi2.py` 75–136 · `compute_indicators` 67–72 | 59–73 · 100–126 | `load_all_symbol_data_split` 41–43 |
| `turtle_soup_crypto` | krypto, 1d | 42–74 · 77–80 · 49, 67 · 39, 68, 69 | `backtest_turtle_soup.py` 113–180 · `compute_indicators` 107–110 | 51–64 · 83–109 | — |
| `volatility_breakout_crypto` | krypto, 1d | 44–78 · 81–93 · 51, 70 · 41, 71, 72 | `backtest_breakout.py` 104–183 · `compute_indicators` 84–95 | 67–85 · 138–164 | `load_all_symbol_data_split` 32–34 |
| `elliott_wave_stocks` | aktien, 1d | 60–104 · 107–126 · 72, 93, 94, 96 · 52, 97, 98 | `backtest_elliott.py` 112–176 · `simulate_trade` 79–109 | 77–113 · 135–161 | — |
| `rsi2_mean_reversion` | aktien, 1d | 55–99 · 102–112 · 67, 86, 93 · 51, 87, 88 | `backtest_rsi2.py` 112–179 · `compute_indicators` 99–109 | 70–103 · 135–161 | `load_all_symbol_data_split` 47–51 |
| `turtle_soup_stocks` | aktien, 1d | 49–86 · 89–92 · 56, 74, 81 · 45, 75, 76 | `backtest_turtle_soup.py` 109–176 · `compute_indicators` 103–106 | 76–105 · 122–148 | — |
| `volatility_breakout` | aktien, 1d | 53–95 · 98–110 · 63, 82, 89 · 49, 83, 84 | `backtest_breakout.py` 141–224 · `compute_indicators` 117–132 | 69–105 · 123–149 | `load_all_symbol_data_split` 38–40 |

### M1 — Schlüssel der Zuteilung

**Frage, zeichengleich** — Register `docs/VORREGISTRIERUNG_neuselektion.md` Z. 11722 (Abschnitt 55.8, Kopf Z. 11714; Posten 5, mittlere Spalte bis zum Satz „Dazu aus Nr. 6“):

> Messbitte aus „Unsicher“ Nr. 2 der Antwort 07.10.a: wie `shared/zuteilung.py` den Schlüssel aus `exit_time`, `exit_price` und `pnl_pct` bildet — als Streuwert über die Felder oder als Ordnung nach einem von ihnen; nur das Wie (27.2), durch Lesen, Punkt 10 bleibt zu.

**Nur das Wie.** Die Antwort sagt, welche der zwei genannten Bauarten vorliegt — oder eine dritte, dann mit Wortlaut — und zeigt es an den Zeilen. Nicht gefragt und nicht zu sagen: wie oft der Schlüssel entscheidet. „Punkt 10 bleibt zu“: `shared/zuteilung.py` wird nicht geändert.

| Nr. | Datei | Ziel | Z. | wie gefunden | SL |
|---|---|---|---|---|---|
| M1.1 | `shared/zuteilung.py` | Kopftext des Moduls | 1–154 | Datei aus Register 55.8 Nr. 5 | S1 |
| M1.2 | `shared/zuteilung.py` | `SEED` | 174 | Register 10 Punkt 10 nennt `SEED` | S1 |
| M1.3 | `shared/zuteilung.py` | `STUFE_ZUFALL` | 207 | Wortsuche „ZUFALL“ in der Datei | S1 |
| M1.4 | `shared/zuteilung.py` | `zufallsschluessel()` | 411–426 | Namenssuche „schluessel“ per ast; einzige Funktion mit dem Wort | S1 |
| M1.5 | `shared/zuteilung.py` | `Zuteiler.__init__()` | 461–502 | Zeilen mit `exit_time`/`exit_price`/`pnl_pct`: Z. 492, 493; mit `zufallsschluessel` oder `_zufall`: Z. 470, 495, 497 | S1 |
| M1.6 | `shared/zuteilung.py` | `Zuteiler.ausstiegsreihenfolge()` | 529–540 | nennt `zufallsschluessel`, `_zufall` oder `STUFE_ZUFALL` in Z. 540 | S1 |
| M1.7 | `shared/zuteilung.py` | `Zuteiler.waehle()` | 543–578 | nennt `zufallsschluessel`, `_zufall` oder `STUFE_ZUFALL` in Z. 577, 578 | S1 |
| M1.8 | `shared/zuteilung.py` | `simuliere_portfolio()` | 657–793 | Namenssuche `simuliere_portfolio`: genannt in 9 von 9 `strategies/<Bot>/equity_simulation.py` | S1 |

### M2 — Zeitzone von `open_time` und Go-Live-Schnitt

**Frage, zeichengleich** — derselbe Posten, Register Z. 11722, Rest der mittleren Spalte:

> Dazu aus Nr. 6: ob `open_time` und der Go-Live-Schnitt in derselben Zeitzone gelesen werden, ist nicht gemessen

und Antwort 09.10.a (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-09a_beitrag_aus_r45_listen_geschnitten_handelbar_tag.md` Z. 222), R86 (e), in eckigen Klammern:

> [Voraussetzung, vor der Neuerzeugung der Listen zu messen, nur das Wie (27.2): dass open_time und der Go-Live-Schnitt in derselben Zeitzone gelesen werden (Antwort 07.10.a, „Unsicher“ 6); sonst wird gemeldet.]

**Nur das Wie, am Signalpfad.** Gemessen wird an den Dateien des Signalpfads: den neun `mso`, den neun Backtest-Modulen, den neun `wf`, den neun `es` und jeder Datei, die sie — auch mittelbar — importieren. Den Importbaum hat der Helfer per `ast` bestimmt, nichts ausgeführt: 78 Dateien (36 Baumwurzeln — je Bot `mso`, Backtest-Modul, `wf`, `es` —, 14 unter `shared/`, 28 weitere in den Bot-Ordnern); `open_time` führen davon 39. Importe zur Laufzeit sieht `ast` nicht: Aufgelöst wird ein Modulname im Ordner der Datei, unter `shared/` und in der Repo-Wurzel, nicht über `sys.path`. `importlib` steht im Baum in `shared/paths.py` Z. 538 (`from importlib import metadata`) — Standardbibliothek, kein Modul des Repos; `import_module`, `__import__` oder `spec_from_file_location` nennt keine Datei des Baums. **Die Frage an die Sitzung:** an welchen dieser Stellen `open_time` in einen Zeitstempel gewandelt, mit einer Zeitzone versehen oder mit einem Datum verglichen wird, und wie der Go-Live-Schnitt gelesen wird (Stellen mit `GO_LIVE_SCHNITT` unter `research/`). Je solcher Stelle eine Zeile: zonenlos oder mit welcher Zeitzone. Am Schluss ein Satz: dieselbe Zeitzone · verschieden · durch Lesen nicht entscheidbar; findet die Sitzung keine Stelle, an der `open_time` gegen den Schnitt verglichen wird, ist das die Aussage. „Sonst wird gemeldet“ heisst hier: Es steht im Ergebnis; mehr tut die Sitzung nicht.

Zeilen mit `open_time` in den Baumwurzeln (nur Zeilennummern; die neun `es` führen `open_time` nicht):

| Bot | `mso` | Backtest-Modul | `wf` |
|---|---|---|---|
| `elliott_wave` | 63 | 82, 87, 89, 92, 94, 99, 125, 204 | 47, 49 |
| `t3_supertrend` | 59, 79 | 89, 111, 130 | 42, 44 |
| `rsi2_crypto` | 66, 85 | 68, 83, 88, 101, 126, 129, 148 | 28, 29 |
| `turtle_soup_crypto` | 49, 67 | 108, 121, 126, 142, 170, 173, 192 | 22, 23 |
| `volatility_breakout_crypto` | 51, 70 | 86, 114, 131, 152, 173, 176, 195 | 22, 23 |
| `elliott_wave_stocks` | 72, 93, 94, 96 | 91, 96, 98, 101, 103, 108, 134, 216 | 47, 49 |
| `rsi2_mean_reversion` | 67, 86, 93 | 105, 126, 131, 144, 169, 172, 191 | 37, 38 |
| `turtle_soup_stocks` | 56, 74, 81 | 104, 117, 122, 138, 166, 169, 188 | 22, 23 |
| `volatility_breakout` | 63, 82, 89 | 123, 155, 172, 193, 214, 217, 236 | 28, 29 |

Die Stellen des Schnitts und die weiteren Dateien des Importbaums mit `open_time`:

| Nr. | Datei | Ziel | Z. | wie gefunden | SL |
|---|---|---|---|---|---|
| M2.1 | `research/vorregistrierung/registerdaten.py` | Zeilen mit `GO_LIVE_SCHNITT =` | 102 (in Modulebene) | Namenssuche `GO_LIVE_SCHNITT`, `GO_LIVE` über 481 verfolgte `*.py` | S1 |
| M2.2 | `research/faltenplan_neun/erste_falte_trockenlauf.py` | Zeilen mit `GO_LIVE_SCHNITT`, `GO_LIVE` | 197, 202 (in `messung`) | dieselbe Namenssuche (Leser des Schnitts) | — |
| M2.3 | `research/faltenplan_neun/faltenplan_neun.py` | Zeilen mit `GO_LIVE_SCHNITT`, `GO_LIVE` | 138, 139, 444, 466, 467, 471, 472, 566, 622 (in Modulebene, `erstes_faltenjahr`, `falten`, `main`) | dieselbe Namenssuche (Leser des Schnitts) | — |
| M2.4 | `research/faltenplan_neun/faltenschranke_messung.py` | Zeilen mit `GO_LIVE_SCHNITT`, `GO_LIVE` | 298, 341, 507 (in `messung`, `trockenlauf_ohne_schranke`, `main`) | dieselbe Namenssuche (Leser des Schnitts) | — |
| M2.5 | `research/vorregistrierung/faltenplan.py` | Zeilen mit `GO_LIVE_SCHNITT`, `GO_LIVE` | 285, 326, 339, 475 (in `erste_falte`, `_plan`, `main`) | dieselbe Namenssuche (Leser des Schnitts) | S1 |
| M2.6 | `research/vorregistrierung/registerbericht.py` | Zeilen mit `GO_LIVE_SCHNITT`, `GO_LIVE` | 137 (in `block`) | dieselbe Namenssuche (Leser des Schnitts) | — |
| M2.7 | `shared/abrufschutz.py` | Zeilen mit `open_time` | 39, 43, 54, 136, 159, 215 (in Modulebene, `_oeffnungszeiten_ms`, `oeffnungszeiten_ms`) | im Importbaum des Signalpfads, dort importiert von 3 Dateien | — |
| M2.8 | `shared/binance_historie.py` | Zeilen mit `open_time` | 101, 272, 285, 323, 331, 488, 547, 549, 582, 589 (in Modulebene, `erste_kerze_ms`, `kerzen_laden`, `als_dataframe`, `_zeilen_aus_dataframe`, `verlaengere_datei`) | im Importbaum des Signalpfads, dort importiert von 1 Datei | — |
| M2.9 | `shared/fetch_binance_data.py` | Zeilen mit `open_time` | 96, 98, 107, 122, 317, 332, 339 (in Modulebene, `als_dataframe`) | im Importbaum des Signalpfads, dort importiert von 2 Dateien | — |
| M2.10 | `shared/kursdaten.py` | Zeilen mit `open_time` | 147, 148 (in `pruefe_ordner`) | im Importbaum des Signalpfads, dort importiert von 11 Dateien | — |
| M2.11 | `shared/zuteilung.py` | Zeilen mit `open_time` | 219, 233, 268 (in `kursrahmen`, `Kursvorrat._tagesreihen`) | im Importbaum des Signalpfads, dort importiert von 9 Dateien | S1 |
| M2.12 | `strategies/elliott_wave_stocks/fetch_stock_data.py` | Zeilen mit `open_time` | 74, 78, 88, 93 (in `fetch_historical_data`) | im Importbaum des Signalpfads, dort importiert von 1 Datei | — |
| M2.13 | `strategies/rsi2_crypto/indicators.py` | Zeilen mit `open_time` | 98 (in `calculate_supertrend`) | im Importbaum des Signalpfads, dort importiert von 1 Datei | — |
| M2.14 | `strategies/volatility_breakout_crypto/indicators.py` | Zeilen mit `open_time` | 85 (in `calculate_supertrend`) | im Importbaum des Signalpfads, dort importiert von 2 Dateien | — |
| M2.15 | `strategies/t3_supertrend/regime_filter.py` | Zeilen mit `open_time` | 22, 38, 43, 46 (in `compute_btc_regime`, `filter_trades_by_regime`) | im Importbaum des Signalpfads, dort importiert von 2 Dateien | — |
| M2.16 | `strategies/volatility_breakout_crypto/regime_filter.py` | Zeilen mit `open_time` | 23, 34, 39, 42 (in `compute_btc_regime`, `filter_trades_by_regime`) | im Importbaum des Signalpfads, dort importiert von 1 Datei | — |
| M2.17 | `strategies/<Bot>/zigzag_indicator.py` für `elliott_wave`, `elliott_wave_stocks` | Zeilen mit `open_time` | 40, 136, 207 (in `calculate_zigzag`, `calculate_zigzag_with_confirmation`, Modulebene) | im Importbaum des Signalpfads, dort importiert von 2 Dateien | — |

Weitere Treffer derselben Namenssuche in anderen Arbeitssträngen und in Testdateien (keine Einstiegspunkte): `research/etf_trendfolge/register.py` Z. 350; `research/faltenplan_neun/test_erste_falte_trockenlauf.py` Z. 94; `research/krypto_historie/faltenplan.py` Z. 63, 125, 139, 141, 143, 224, 250, 311; `research/krypto_historie/test_faltenplan.py` Z. 140, 170, 172; `research/vorregistrierung/test_vorregistrierung.py` Z. 739, 741.

Von den vier eigens geprüften Dateien unter `shared/` liegt im Importbaum: `shared/abrufschutz.py`. **Nicht im Signalpfad, nicht gemessen:** `shared/entscheidungskerze.py` (Z. 498); `shared/kursdaten_neuaufbau.py` (Z. 113, 463); `shared/zeitabdeckung.py` (Z. 25, 30, 209, 212, 213, 227, 228, 296) — sie führen `open_time`, liegen aber nicht im Importbaum. Ebenso nicht gemessen: die übrigen der 148 Dateien mit `open_time`, darunter `research/vorregistrierung/benchmark.py` und `research/mtm_drawdown/grundlage.py`.

### M3 — Träger der Ausstiege

**Frage, zeichengleich** — Antwort 09.10.a (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-09a_beitrag_aus_r45_listen_geschnitten_handelbar_tag.md` Z. 216), R84 (e), der Teil in eckigen Klammern:

> [Voraussetzung, vor dem Bau der Attribution zu messen, durch Lesen, nur das Wie (27.2): ob ereignisreihenfolge in research/mtm_drawdown/mtm_kern.py die Reihenfolge der Ausstiege aus capital_after zurückgewinnt; ob eine ausgeführte Position bei jedem der neun Bots genau einen Ausstieg hat. Trifft das Erste zu, übernimmt der Erzeuger diese Funktion nicht. Hat eine Position mehrere Ausstiege, gilt (c) je Ausstieg, und es wird gemeldet.]

**Nur das Wie, in zwei Teilen.** (a) Ob `ereignisreihenfolge` die Reihenfolge der Ausstiege aus `capital_after` zurückgewinnt, und wenn nicht, woraus sie sie nimmt. (b) **Je Bot eine Zeile, alle neun:** ob eine ausgeführte Position genau einen Ausstieg hat — „genau einer“, „mehrere möglich“ oder „durch Lesen nicht entscheidbar“, je mit Fundstelle. Die zwei Schlusssätze der Klammer („Trifft das Erste zu …“, „Hat eine Position mehrere Ausstiege …“) sind Entscheide des Verfahrensprüfers; die Sitzung wendet sie nicht an.

| Nr. | Datei | Ziel | Z. | wie gefunden | SL |
|---|---|---|---|---|---|
| M3.1 | `research/mtm_drawdown/mtm_kern.py` | Kopftext des Moduls | 1–59 | Datei aus der Antwort 09.10.a, R84 (e) | — |
| M3.2 | `research/mtm_drawdown/mtm_kern.py` | `KETTEN_TOLERANZ` | 72 | Konstante vor `ereignisreihenfolge` | — |
| M3.3 | `research/mtm_drawdown/mtm_kern.py` | `ereignisreihenfolge()` | 79–120 | Name aus R84 (e); `capital_after` in Z. 88, 109, 116, 119 | — |
| M3.4 | `research/mtm_drawdown/mtm_kern.py` | `ereigniskurve()` | 123–128 | Nachbar; `capital_after` in Z. 124, 127, 128 | — |
| M3.5 | `research/mtm_drawdown/grundlage.py` | Zeilen mit `ereignisreihenfolge` | 198 (in `pruefe_bot`) | Namenssuche `ereignisreihenfolge` (Aufrufer, Test) | — |
| M3.6 | `research/mtm_drawdown/messung.py` | Zeilen mit `ereignisreihenfolge` | 142 (in `main`) | Namenssuche `ereignisreihenfolge` (Aufrufer, Test) | — |
| M3.7 | `research/mtm_drawdown/richtungsfall.py` | Zeilen mit `ereignisreihenfolge` | 65 (in `fall`) | Namenssuche `ereignisreihenfolge` (Aufrufer, Test) | — |
| M3.8 | `research/mtm_drawdown/test_mtm_kern.py` | Zeilen mit `ereignisreihenfolge` | 41, 101, 231, 236 (in Modulebene, `messe`, `gegenproben`) | Namenssuche `ereignisreihenfolge` (Aufrufer, Test) | — |
| M3.9 | `shared/zuteilung.py` | `simuliere_portfolio()` | 657–793 | einzige Stelle der Datei mit `capital_after`: Z. 734; `exit_time` Z. 704 | S1 |
| M3.10 | `shared/zuteilung.py` | `Zuteiler.ausstiegsreihenfolge()` | 529–540 | Namenssuche „ausstieg“ per ast | S1 |

Dazu je Bot: `run_backtest` und „weitere“ im Backtest-Modul, `get_trades_for_symbol` in `mso`, `collect_all_trades` und `simulate_portfolio` in `es`.

### M4 — Einstieg vor dem Handelbar-Tag

**Frage, zeichengleich** — Antwort 09.10.a (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-09a_beitrag_aus_r45_listen_geschnitten_handelbar_tag.md` Z. 225), R87 (d), der Teil in eckigen Klammern:

> [Voraussetzung, vor dem Bau der zwei Erzeuger zu messen, nur das Ob (27.2), durch Lesen des Signalpfads der neun Bots, ohne Lauf und ohne eine Trade-Liste zu öffnen: ob der Scan eines geladenen Symbols vor dessen Handelbar-Tag einen Einstieg bilden kann. Kann er es bei keinem Bot, ist das Tatsachennotiz, und die Wache bleibt. Kann er es bei einem, ist das ein Register-Code-Widerspruch (25c (1), nach der Wiedergabe in R48 und R50) und kommt vor dem Bau mit der Fundstelle als Frage an den Verfahrensprüfer; die Regel nach (a) steht dann schon. Trades mit Einstieg vor dem Handelbar-Tag nachträglich aus Listen oder Ausgaben zu streichen, gilt nicht als Vollzug, solange nicht gemessen ist, dass ein gestrichener Trade keinen späteren verdrängt oder verschoben hat.]

**Nur das Ob, je Bot eine Zeile, alle neun:** „kann“, „kann nicht“ oder „durch Lesen nicht entscheidbar“, je mit den Zeilen des Signalpfads (Lader → Scan → Einstieg), an denen es hängt. Was „Handelbar-Tag“ heisst, nimmt die Sitzung aus R87 (a) und (b) derselben Zeile der Antwort und aus den Stellen, an denen der Code den Tag bestimmt (unten); sie nennt die Stelle, die sie zugrunde legt. Kein Lauf, keine Trade-Liste. Ob ein Fund Tatsachennotiz oder Register-Code-Widerspruch ist, sagt die Sitzung nicht.

| Nr. | Datei | Ziel | Z. | wie gefunden | SL |
|---|---|---|---|---|---|
| M4.1 | `research/vorregistrierung/benchmark.py` | Kopftext des Moduls | 1–80 | nennt den Handelbar-Tag (Z. 51, 52, 62, 63, 66) | S1 |
| M4.2 | `research/vorregistrierung/benchmark.py` | `tagesgenau()` | 164–188 | Wortsuche „handelbar“ | S1 |
| M4.3 | `research/faltenplan_neun/faltenschranke_messung.py` | `loader_lesart()` | 223–258 | in `benchmark.py` Z. 268 genannt (`fsm.loader_lesart`) | — |
| M4.4 | `research/faltenplan_neun/faltenschranke_messung.py` | `_min_history()` | 147–162 | Nachbar von `loader_lesart` | — |
| M4.5 | `research/faltenplan_neun/faltenschranke_messung.py` | `kerzen_elliott_wave()` | 165–217 | Nachbar von `loader_lesart` | — |
| M4.6 | `research/faltenplan_neun/faltenplan_neun.py` | `warm_ab()` | 402–412 | Wortsuche „handelbar“ (als Teilwort): Z. 403 in der Funktion; weitere Treffer der Datei: Z. 92 in Modulebene, Z. 435 in `erstes_faltenjahr` | — |
| M4.7 | `research/faltenplan_neun/faltenplan_neun.py` | `symbolbeginn()` | 415–428 | Nachbar von `warm_ab` | — |
| M4.8 | `shared/kursdaten.py` | `unvollstaendige_maske()` | 57–70 | Datei im Importbaum des Signalpfads; Wortsuche „handelbar“: Z. 61 in der Funktion; von keiner der 36 Baumwurzeln beim Namen importiert | — |
| M4.9 | `shared/kursdaten.py` | `Zaehler()` | 95–122 | Datei im Importbaum des Signalpfads; aus `kursdaten` importiert von 9 der 36 Baumwurzeln | — |
| M4.10 | `shared/kursdaten.py` | `entferne_unvollstaendige()` | 73–92 | Datei im Importbaum des Signalpfads; aus `kursdaten` importiert von 9 der 36 Baumwurzeln | — |

Dazu je Bot: Lader und `MIN_HISTORY` in `mso`, `get_trades_for_symbol`, `run_backtest` und „weitere“, `collect_all_trades`, die Lader in `wf`. Die Wortsuche „handelbar“ trifft als Teilwort 25 der 481 durchsuchten Dateien; Einstiegspunkte sind nur die genannten — Messprogramme wie `research/universum_trockenlauf/universum_trockenlauf.py` gehören nicht zum Signalpfad.

### M5 — Quelle des Handelbar-Tags

**Frage, zeichengleich** — Antwort 09.10.a (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-09a_beitrag_aus_r45_listen_geschnitten_handelbar_tag.md`), Abschnitt „Unsicher“ (Z. 198–209), Nr. 7 = Z. 206:

> 7. **Quelle des Handelbar-Tags für die Wache.** R87 (c) setzt voraus, dass die Benchmark-Rechnung des Laufs den Tag je Symbol herausgibt, wie 23.5 es für die Benchmark-Tabelle beschreibt. Für `bh_tagesrenditen` im Erzeuger ist das nicht gemessen.

**Lesart des steuernden Chats, vorläufig: nur das Ob und wo.** Die Quelle (oben wörtlich) sagt weder „nur das Wie“ noch „nur das Ob“ und spricht von `bh_tagesrenditen` „im Erzeuger“. Der Erzeuger ist nicht gebaut — gemessen wird die vorhandene Benchmark-Rechnung (`research/vorregistrierung/benchmark.py`, `je_bot`, `bh_tagesrenditen`; dazu die gleichnamige Funktion in `research/exposure_messung/exposure_kern.py`): ob sie den Handelbar-Tag je Symbol herausgibt; wenn ja: Datei, Funktion, Zeile und Form (Rückgabewert, Feld, Datei); wenn nein: welche Funktion ihn hält. Die Sitzung sagt es für beide Funktionen und nennt, welche die Benchmark-Rechnung ruft. Zeitpunkt, ebenfalls Lesart des steuernden Chats, vorläufig: vor dem Bau der zwei Erzeuger, mit M4 (`docs/projektfuehrung/UEBERGABE.md` Z. 2966, Vorgabe V5 im Nachtrag Z. 2950; Arbeitsbaum beim Bau).

| Nr. | Datei | Ziel | Z. | wie gefunden | SL |
|---|---|---|---|---|---|
| M5.1 | `research/vorregistrierung/benchmark.py` | `bh_tagesrenditen()` | 191–205 | Name aus „Unsicher“ Nr. 7; Register 10 Punkt 6 nennt `benchmark.py::bh_tagesrenditen` | S1 |
| M5.2 | `research/vorregistrierung/benchmark.py` | `tagesgenau()` | 164–188 | Parameter `handelbar` in der Kopfzeile der Funktion | S1 |
| M5.3 | `research/vorregistrierung/benchmark.py` | `je_bot()` | 251–321 | nennt `bh_tagesrenditen` in Z. 272 und `handelbar` in Z. 269, 270, 271, 276, 281, 303 | S1 |
| M5.4 | `research/vorregistrierung/benchmark.py` | `schreibe_tabellen()` | 363–400 | Namenssuche „tabellen“ per ast | S1 |
| M5.5 | `research/vorregistrierung/benchmark.py` | `main()` | 403–459 | `main` des Moduls | S1 |
| M5.6 | `research/faltenplan_neun/faltenschranke_messung.py` | `loader_lesart()` | 223–258 | in `je_bot` genannt (Z. 268) | — |
| M5.7 | `research/exposure_messung/auswertung.py` | Zeilen mit `bh_tagesrenditen` | 456 (in `main`) | Namenssuche `bh_tagesrenditen` | — |
| M5.8 | `research/exposure_messung/exposure_kern.py` | `bh_tagesrenditen()` | 211–222 | zweite Funktion gleichen Namens (Namenssuche `bh_tagesrenditen`) | — |
| M5.9 | `research/exposure_messung/test_exposure_kern.py` | Zeilen mit `bh_tagesrenditen` | 146 (in Modulebene) | Namenssuche `bh_tagesrenditen` | — |

## Schritt D — Messblöcke, Ergebnis, Journalblock, Abgabe

**D0. Zeilen und md5 der gelesenen Dateien** — zwei Blöcke über die 63 Startdateien; jede weitere gelesene Datei hängt die Sitzung in beiden Blöcken hinter der letzten an, sonst ändert sie nichts:

```
wc -l shared/zuteilung.py research/vorregistrierung/registerdaten.py research/faltenplan_neun/erste_falte_trockenlauf.py research/faltenplan_neun/faltenplan_neun.py research/faltenplan_neun/faltenschranke_messung.py research/vorregistrierung/faltenplan.py research/vorregistrierung/registerbericht.py shared/abrufschutz.py shared/binance_historie.py shared/fetch_binance_data.py shared/kursdaten.py strategies/elliott_wave_stocks/fetch_stock_data.py strategies/rsi2_crypto/indicators.py strategies/volatility_breakout_crypto/indicators.py strategies/t3_supertrend/regime_filter.py strategies/volatility_breakout_crypto/regime_filter.py strategies/elliott_wave/zigzag_indicator.py strategies/elliott_wave_stocks/zigzag_indicator.py strategies/elliott_wave/multi_symbol_optimise.py strategies/elliott_wave/backtest_elliott.py strategies/elliott_wave/multi_symbol_walk_forward.py strategies/elliott_wave/equity_simulation.py strategies/t3_supertrend/multi_symbol_optimise.py strategies/t3_supertrend/backtest_trend.py strategies/t3_supertrend/multi_symbol_walk_forward.py strategies/t3_supertrend/equity_simulation.py strategies/rsi2_crypto/multi_symbol_optimise.py strategies/rsi2_crypto/backtest_rsi2.py strategies/rsi2_crypto/multi_symbol_walk_forward.py strategies/rsi2_crypto/equity_simulation.py strategies/turtle_soup_crypto/multi_symbol_optimise.py strategies/turtle_soup_crypto/backtest_turtle_soup.py strategies/turtle_soup_crypto/multi_symbol_walk_forward.py strategies/turtle_soup_crypto/equity_simulation.py strategies/volatility_breakout_crypto/multi_symbol_optimise.py strategies/volatility_breakout_crypto/backtest_breakout.py strategies/volatility_breakout_crypto/multi_symbol_walk_forward.py strategies/volatility_breakout_crypto/equity_simulation.py strategies/elliott_wave_stocks/multi_symbol_optimise.py strategies/elliott_wave_stocks/backtest_elliott.py strategies/elliott_wave_stocks/multi_symbol_walk_forward.py strategies/elliott_wave_stocks/equity_simulation.py strategies/rsi2_mean_reversion/multi_symbol_optimise.py strategies/rsi2_mean_reversion/backtest_rsi2.py strategies/rsi2_mean_reversion/multi_symbol_walk_forward.py strategies/rsi2_mean_reversion/equity_simulation.py strategies/turtle_soup_stocks/multi_symbol_optimise.py strategies/turtle_soup_stocks/backtest_turtle_soup.py strategies/turtle_soup_stocks/multi_symbol_walk_forward.py strategies/turtle_soup_stocks/equity_simulation.py strategies/volatility_breakout/multi_symbol_optimise.py strategies/volatility_breakout/backtest_breakout.py strategies/volatility_breakout/multi_symbol_walk_forward.py strategies/volatility_breakout/equity_simulation.py research/mtm_drawdown/mtm_kern.py research/mtm_drawdown/grundlage.py research/mtm_drawdown/messung.py research/mtm_drawdown/richtungsfall.py research/mtm_drawdown/test_mtm_kern.py research/vorregistrierung/benchmark.py research/exposure_messung/auswertung.py research/exposure_messung/exposure_kern.py research/exposure_messung/test_exposure_kern.py > docs/belege/TB-148/lese_zeilen.txt 2>&1; echo "rc $?" >> docs/belege/TB-148/lese_zeilen.txt
```

```
md5 shared/zuteilung.py research/vorregistrierung/registerdaten.py research/faltenplan_neun/erste_falte_trockenlauf.py research/faltenplan_neun/faltenplan_neun.py research/faltenplan_neun/faltenschranke_messung.py research/vorregistrierung/faltenplan.py research/vorregistrierung/registerbericht.py shared/abrufschutz.py shared/binance_historie.py shared/fetch_binance_data.py shared/kursdaten.py strategies/elliott_wave_stocks/fetch_stock_data.py strategies/rsi2_crypto/indicators.py strategies/volatility_breakout_crypto/indicators.py strategies/t3_supertrend/regime_filter.py strategies/volatility_breakout_crypto/regime_filter.py strategies/elliott_wave/zigzag_indicator.py strategies/elliott_wave_stocks/zigzag_indicator.py strategies/elliott_wave/multi_symbol_optimise.py strategies/elliott_wave/backtest_elliott.py strategies/elliott_wave/multi_symbol_walk_forward.py strategies/elliott_wave/equity_simulation.py strategies/t3_supertrend/multi_symbol_optimise.py strategies/t3_supertrend/backtest_trend.py strategies/t3_supertrend/multi_symbol_walk_forward.py strategies/t3_supertrend/equity_simulation.py strategies/rsi2_crypto/multi_symbol_optimise.py strategies/rsi2_crypto/backtest_rsi2.py strategies/rsi2_crypto/multi_symbol_walk_forward.py strategies/rsi2_crypto/equity_simulation.py strategies/turtle_soup_crypto/multi_symbol_optimise.py strategies/turtle_soup_crypto/backtest_turtle_soup.py strategies/turtle_soup_crypto/multi_symbol_walk_forward.py strategies/turtle_soup_crypto/equity_simulation.py strategies/volatility_breakout_crypto/multi_symbol_optimise.py strategies/volatility_breakout_crypto/backtest_breakout.py strategies/volatility_breakout_crypto/multi_symbol_walk_forward.py strategies/volatility_breakout_crypto/equity_simulation.py strategies/elliott_wave_stocks/multi_symbol_optimise.py strategies/elliott_wave_stocks/backtest_elliott.py strategies/elliott_wave_stocks/multi_symbol_walk_forward.py strategies/elliott_wave_stocks/equity_simulation.py strategies/rsi2_mean_reversion/multi_symbol_optimise.py strategies/rsi2_mean_reversion/backtest_rsi2.py strategies/rsi2_mean_reversion/multi_symbol_walk_forward.py strategies/rsi2_mean_reversion/equity_simulation.py strategies/turtle_soup_stocks/multi_symbol_optimise.py strategies/turtle_soup_stocks/backtest_turtle_soup.py strategies/turtle_soup_stocks/multi_symbol_walk_forward.py strategies/turtle_soup_stocks/equity_simulation.py strategies/volatility_breakout/multi_symbol_optimise.py strategies/volatility_breakout/backtest_breakout.py strategies/volatility_breakout/multi_symbol_walk_forward.py strategies/volatility_breakout/equity_simulation.py research/mtm_drawdown/mtm_kern.py research/mtm_drawdown/grundlage.py research/mtm_drawdown/messung.py research/mtm_drawdown/richtungsfall.py research/mtm_drawdown/test_mtm_kern.py research/vorregistrierung/benchmark.py research/exposure_messung/auswertung.py research/exposure_messung/exposure_kern.py research/exposure_messung/test_exposure_kern.py > docs/belege/TB-148/lese_md5.txt 2>&1; echo "rc $?" >> docs/belege/TB-148/lese_md5.txt
```

Soll: je Schlusszeile `rc 0`. Die Werte trägt die Sitzung ins Leseprotokoll nach. Lehnt Claude Code einen der zwei Blöcke ab oder verlangt es dafür eine Bestätigung: nicht wiederholen, nicht umformen; die Werte heissen „nicht gemessen“, die Ablehnung steht mit Wortlaut unter „Abweichungen vom Auftrag“.

**D1. Ergebnis** `docs/ERGEBNIS_TB-148_verfahrensmessung_schluessel_zeitzone_handelbar.md` (Schreibwerkzeug), in dieser Gliederung: Kopf (Stand, ⟨S0⟩ und die Commits bis M5; die Kennung von ⟨F⟩ nennt die Schlussmeldung) · **„Kurz“** (je Messpunkt eine Zeile; dazu 0a, A, D3 mit Soll und Ist) · **je Messpunkt die Tabelle** aus `m<n>_fundstellen.md`, für M3 (b) und M4 je Bot eine Zeile · **„Leseprotokoll“** (wie der Beleg: jede gelesene Datei, Zeilenbereich, Messpunkt, Zeilen, md5) · **„Belege“** (Tabelle Datei · Befehl · Bytes · md5; Kopfdateien gibt es nicht) · **„Abweichungen vom Auftrag“** (jede, auch kleine; sonst „keine“ mit der Liste der geprüften Sollwerte) · **„Nicht getan“** · **„In einfacher Sprache“**. Das Ergebnis muss der Verfahrensprüfer lesen dürfen (Register 27): keine Ergebniszahl, keine Trade-Zahl, kein Verweis auf `BACKLOG*.md` mit Inhalt, keine Empfehlung. Bytes und md5 je Beleg liest die Sitzung aus den zwei Blöcken unter diesem Absatz ab. `f_porcelain.txt` und `f_numstat.txt` entstehen erst nach dem Abgabe-Commit: In „Kurz“ steht dazu „nach der Abgabe gemessen, siehe Beleg“, die Werte nennt die Schlussmeldung.

```
wc -c docs/belege/TB-148/0a_status.txt docs/belege/TB-148/a_modus.txt docs/belege/TB-148/m1_fundstellen.md docs/belege/TB-148/m2_fundstellen.md docs/belege/TB-148/m3_fundstellen.md docs/belege/TB-148/m4_fundstellen.md docs/belege/TB-148/m5_fundstellen.md docs/belege/TB-148/leseprotokoll.md docs/belege/TB-148/lese_zeilen.txt docs/belege/TB-148/lese_md5.txt
```

```
md5 docs/belege/TB-148/0a_status.txt docs/belege/TB-148/a_modus.txt docs/belege/TB-148/m1_fundstellen.md docs/belege/TB-148/m2_fundstellen.md docs/belege/TB-148/m3_fundstellen.md docs/belege/TB-148/m4_fundstellen.md docs/belege/TB-148/m5_fundstellen.md docs/belege/TB-148/leseprotokoll.md docs/belege/TB-148/lese_zeilen.txt docs/belege/TB-148/lese_md5.txt
```

**D2. Journalblock** in `docs/projektfuehrung/JOURNAL.md`, mit dem Bearbeitungswerkzeug eingefügt, nichts sonst geändert: nach dem letzten Buchstabenblock, vor `## Wiederkehrende Lehren` (am HEAD Z. 10376; davor stehen `---` und eine Leerzeile, die Folge `---`, Leerzeile, `## Wiederkehrende Lehren` gibt es genau einmal). Kennung messen:

```
grep -n '^## Wiederkehrende Lehren' docs/projektfuehrung/JOURNAL.md
```

Dann mit dem Lesewerkzeug die Zeilen davor lesen: Die letzte Zeile der Form `## <zwei Grossbuchstaben> — …` ist der Kopf des letzten Blocks (am HEAD EM, Z. 10332); der neue Block trägt die nächste Kennung (erwartet EN; den Block davor hat TB-147 gesetzt). Gliederung wie der letzte Block: Kopfzeile `## <Kennung> — TB-148: …`, Quellenzeile, Absatz „**Quelle:**“, `### Was gemessen ist`, `### Was offen bleibt`, Schlusszeile `*Geschrieben … von der Mac-Sitzung TB-148. Quellenvermerk: siehe Kopf.*`, dahinter Leerzeile und `---`. Nie `JOURNAL.md` mit Platzhalter.

**D3. Abgabe.** Jede Datei mit Namen:

```
git add docs/ERGEBNIS_TB-148_verfahrensmessung_schluessel_zeitzone_handelbar.md docs/projektfuehrung/JOURNAL.md docs/belege/TB-148/leseprotokoll.md docs/belege/TB-148/lese_zeilen.txt docs/belege/TB-148/lese_md5.txt
git commit -m "TB-148 Abgabe: Ergebnis, Journal <Kennung>"
git push
git rev-parse HEAD
```

Der Commit heisst **⟨F⟩**. Danach, mit den Kennungen von ⟨S0⟩ und ⟨F⟩:

```
git status --porcelain > "$TMPDIR/tb148_f.txt"
cp "$TMPDIR/tb148_f.txt" docs/belege/TB-148/f_porcelain.txt
cmp "$TMPDIR/tb148_f.txt" docs/belege/TB-148/f_porcelain.txt
git diff --numstat <⟨S0⟩> <⟨F⟩> > docs/belege/TB-148/f_numstat.txt 2>&1; echo "rc $?" >> docs/belege/TB-148/f_numstat.txt
```

Soll: `f_porcelain.txt` 0 B, `cmp` ohne Ausgabe; in `f_numstat.txt` die Schlusszeile `rc 0`, davor nur Pfade unter `docs/belege/TB-148/`, das Ergebnis und `docs/projektfuehrung/JOURNAL.md` mit 0 entfernten Zeilen. Dann der kleine letzte Commit und die Schlussprobe, deren Rohausgabe wörtlich in der Schlussmeldung steht:

```
git add docs/belege/TB-148/f_porcelain.txt docs/belege/TB-148/f_numstat.txt
git commit -m "TB-148 F: porcelain und numstat nach der Abgabe"
git push
git status --porcelain
```

## Abbruchkriterien — melden, nicht reparieren

- 0a weicht ab (Einträge oder HEAD).
- Schritt A: Die Prozesszeile trägt nicht `--permission-mode manual`.
- **Claude Code lehnt einen Aufruf aus Schritt 0, A, M (die Commits je Messpunkt) oder D ab oder verlangt dafür eine Bestätigung:** melden, nicht umgehen. Verlangt schon Schritt 0 oder der Abbruchweg selbst (Belege committen, pushen) eine Bestätigung: nichts weiter versuchen, den Wortlaut der Frage als Antwort im Chat melden. Für die zwei Blöcke aus D0 gilt der Satz dort. *Schützt:* vor einem halben Bau wie in TB-142 und TB-146.
- Eine Trade-Liste oder eine Datei unter `ergebnisse/` wurde geöffnet (ausser dem Abbild der Sperrliste): anhalten, nichts davon aufschreiben, melden, was geöffnet wurde. Eine Ergebniszahl in einem Kommentar oder Docstring des Quelltexts ist kein Abbruch (Regel unter „Nicht erlaubt“).
- Eine Datei ausserhalb der Liste unter „Freigabe“ müsste geändert werden; `git push` scheitert zweimal.

**Kein Abbruch:** jeder Befund aus M1 bis M5 · „durch Lesen nicht entscheidbar“ · eine Zeilenangabe passt nicht oder ein Einstiegspunkt fehlt · die Kennung ist nicht EN · `f_numstat.txt` oder `f_porcelain.txt` weicht ab (unter „Abweichungen“ nennen). **Bei Abbruch nach Schritt 0:** committen, was an Belegen da ist (jede Datei mit Namen), Grund in `docs/belege/TB-148/abbruch.txt` (Schreibwerkzeug), pushen, melden. Fertige Messpunkte bleiben stehen.

## Nicht in TB-148

- (a) der Registereintrag der Blöcke R84 bis R89 und jede Marke im Register;
- (b) der Bau des Zellen-Erzeugers und des Listen-Erzeugers, die Neuerzeugung der Trade-Listen;
- (c) eine Frage an den Verfahrensprüfer — sie stellt der steuernde Chat mit den Fundstellen dieses Ergebnisses;
- (d) `BACKLOG.md`, Dialog-Index, Registerkopie, `UEBERGABE.md`;
- (e) wie oft der Schlüssel aus M1 entscheidet und jede andere Frage, die nur ein Lauf beantwortet.

## In einfacher Sprache

Bevor zwei neue Programme gebaut und die Handelslisten neu erzeugt werden, will der Verfahrensprüfer fünf Dinge wissen, die im vorhandenen Code stehen: Wie wird bei Gleichstand ausgelost, welche Position zum Zug kommt? Werden Kurszeiten und der Stichtag des Echtbetriebs in derselben Zeitzone gelesen? Woher kennt die Rechnung die Reihenfolge der Verkäufe, und hat jede Position genau einen Verkauf? Kann ein Bot eine Aktie oder Münze kaufen, bevor sie nach den Regeln als handelbar gilt? Und gibt die Vergleichsrechnung diesen Tag je Wert heraus? Dieser Auftrag beantwortet das nur durch Lesen: Er zeigt die Zeilen, an denen es steht. Es läuft kein Programm, es wird keine Handelsliste geöffnet, und es wird nichts am Code geändert. Was aus den Antworten folgt, entscheidet der Verfahrensprüfer.

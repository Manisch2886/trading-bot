# TB-147 Rest von TB-146: numstat-Beleg, Journalblock, Ergebnis — an: Mac-Sitzung (Claude Code)

**Stand:** Gebaut am 09.10.2026 von einem Helfer des steuernden Chats, gegengelesen (Helfer GEGEN147), ausgelegt 09.10.2026, 23:22.

**Sitzungstitel:** `TB-147` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main` am HEAD `e39cc44c1b419a21512c9a6e9492f66233c366fb` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-147`), nicht von Hand; er legt keinen Satz ins Fenster, den fügt der Betreiber in der App ein.
**Dieser Auftrag:** `docs/auftraege/MAC_TB-147_rest_tb146_journal_ergebnis.md`, wird in Schritt 0 mitcommittet. **Vorgänger:** `docs/auftraege/MAC_TB-146_regelwerk_dokunachtrag_0910.md` (unten kurz „TB-146“). Er brach in Schritt E nach Vorschrift ab (`docs/belege/TB-146/abbruch.txt`; Commits `7f0b59d` Schritt 0, `e39cc44` Abbruch). TB-147 holt nach, was fehlt, und verweist auf TB-146, statt abzuschreiben; bei Widerspruch gilt dieser Auftrag, und es gelten nur die Schritte, die hier stehen.
**Werkzeug:** `docs/belege/TB-146/tb146_einfuegen.py`, wie es im Repo liegt — es wird nicht geändert, nicht kopiert und nicht neu ausgelesen. **Belege:** neue Dateien in `docs/belege/TB-146/`, nur mit den Namen aus diesem Auftrag (die 13 vorhandenen bleiben, wie sie sind). **Ergebnis:** `docs/ERGEBNIS_TB-146_regelwerk_dokunachtrag_0910.md`; es gilt für TB-146 und TB-147. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.
**Ziel:** Der numstat-Beleg zu TB-146 liegt vor, der Journalblock steht mit dem Nachtrag J1 im Journal, und das Ergebnis für beide Aufträge ist geschrieben.
**Reihenfolge:** Schritt 0 → A (Modus) → N (numstat, Vergleich) → J (Journalblock, Commit) → F (Ergebnis, Abgabe).

## Drei Regeln für jeden Aufruf (aus dem Abbruch von TB-146, Fehler Nr. 39)

1. **Jeder Shell-Befehl steht unten wörtlich in einem eigenen Codeblock mit der Marke `sh`** (Blöcke mit der Marke `text` sind Soll-Ausgaben, keine Befehle). Genau so ausführen, ein Block je Aufruf: keinen Befehl umbauen, zusammenfassen, ergänzen oder ersetzen; keinen weiteren Shell-Befehl erfinden. Platzhalter gibt es nur für Commit-Kennungen: ⟨S0⟩, ⟨J⟩, ⟨F⟩ — je die 40 Zeichen aus `git rev-parse HEAD`. Die Schlusszeilen, die Claude Code selbst an eine Commit-Nachricht hängt (`Co-Authored-By`, `Claude-Session`), sind erlaubt, in der Form, die Claude Code dafür üblicherweise nimmt (so entstanden `7f0b59d` und `e39cc44`). Das Verbot von Heredoc, `cat >` und `echo >` gilt für Dateien, nicht für die Commit-Nachricht. Der Titel bleibt wörtlich.
2. **Kein Hilfsskript, nichts ins Scratchpad, nichts ausserhalb des Repos** — einzige Ausnahme `$TMPDIR/tb147_0a.txt` und `$TMPDIR/tb147_f.txt` für `git status --porcelain`. **Keine Kopfdateien** (`*.kopf.txt`), auch nicht zu den vier Ausgaben `e_*` aus TB-146; an ihre Stelle tritt die Tabelle „Belege“ im Ergebnis.
3. **Rohausgaben entstehen nur durch die Umleitung, die im Codeblock steht.** Was die Sitzung selbst verfasst (`j_block.md`, das Ergebnis, bei Abbruch `abbruch_tb147.txt`), schreibt sie mit dem Schreibwerkzeug von Claude Code — nie per Heredoc, `cat >` oder `echo >` in der Shell. Belege liest sie mit dem Lesewerkzeug von Claude Code, nicht mit einem Shell-Befehl.

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei (Betreiber 26.09.2026)** — der Auftrag fügt nur Dokumentation ein; kein Werkzeug und kein Programm wird geändert. Am HEAD gemessen: Register `docs/VORREGISTRIERUNG_neuselektion.md` Abschnitt 10 „Die Sperrliste“ (Z. 971–1177) und die Tabelle „Die Sperrliste, Stand 18.09.2026“ in `ARBEITSWEISE.md` (Z. 1188–1197) enthalten `projektfuehrung`, `auftraege`, `ARBEITSWEISE`, `UMZUG`, `BACKLOG`, `JOURNAL`, `belege`, `ERGEBNIS` und `docs/` je 0-mal.

**Die Sitzung darf ändern, und nichts sonst:** `docs/projektfuehrung/JOURNAL.md` — nur der eine Block, nur über das Werkzeug (Block + 7 + 1 + 3 Zeilen, entfernt 0) · neu: das Ergebnis · neu: Dateien unter `docs/belege/TB-146/` mit den Namen aus diesem Auftrag. Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt (die Einträge aus 0a); das ist kein Ändern im Sinn dieser Liste.
**Nicht erlaubt:** `ARBEITSWEISE.md`, `UMZUG.md`, `BACKLOG.md` (die drei Zieldateien von TB-146 — sie sind fertig); die 13 vorhandenen Belege in `docs/belege/TB-146/`, auch das Werkzeug; alles unter `docs/werkzeuge/`; `docs/projektfuehrung/FABLE_DIALOG_INDEX.md`; `UEBERGABE.md` nach Schritt 0; Register und Registerkopie; `research/`, `shared/`, `strategies/`; frühere Belegordner (`docs/belege/` ausser `TB-146/`). Nie `git add -A`, nie `git add .`; jeder Commit nennt seine Dateien mit Namen.

## Belegt · erschlossen · offen

- **Belegt** (am HEAD gemessen, Helfer BAU147, 09.10.2026, 23:37): HEAD `e39cc44`, sein Elter `7f0b59d`. Die drei Zieldateien, `JOURNAL.md` und das Werkzeug liegen im Arbeitsbaum wie am HEAD (Werte in 0b). Letzte Journalkennung EL (`JOURNAL.md` Z. 10291); vor `## Wiederkehrende Lehren` (Z. 10332) stehen `---` und eine Leerzeile. `docs/belege/TB-146/` hat 13 verfolgte Dateien, kein neuer Name kommt darin vor.
- **Angabe des steuernden Chats, vom Helfer nicht gemessen** (`git status` ist dem Helfer am Repo untersagt): beim Bau (09.10.2026, 22:49) war im Arbeitsbaum nur `UEBERGABE.md` geändert, unverfolgt nichts; Stand beim Auslegen: wie 0a.
- **Erschlossen:** 0a erwartet auch `AKTUELLER_AUFTRAG.md` geändert — der steuernde Chat ändert sie, wenn er diesen Auftrag auslegt (wie in TB-145 und TB-146); sonst endet 0a mit ABBRUCH.
- **Simulation des Helfers** (eigenes git-Repo mit den Ständen `7f0b59d` und `e39cc44`; Linux, Python 3.10): `numstat 7f0b59d e39cc44` rc 0 (die Kopie zeigt dieselben 16 numstat-Zeilen wie `git show --numstat e39cc44` am Repo); `vergleich` rc 0; `journal --probe` rc 0 und `journal` rc 0 mit einer Attrappe als Block (8 Bedingungen `ja`, Kennung EM, Block direkt vor `## Wiederkehrende Lehren`, sonst jede Zeile unverändert); zweiter `journal`-Lauf rc 2; fünf Gegenproben am Block: nichts geschrieben; Schluss-numstat rc 1. **Nicht simuliert:** macOS (`md5`, `wc`, `ps`, `cp`, `cmp`), Claude Code und seine Erlaubnisregeln, der Sitzungswächter, `git push`, Python 3.9. Die Sitzung zählt selbst nach; ihre Zahl gilt.
- Die Erlaubnisregeln der Sitzung (`.claude/settings.local.json`, Listen `deny` mit 70 und `ask` mit 14 Einträgen, vom Gegenleser des steuernden Chats am 09.10.2026 gelesen) treffen keinen Befehl dieses Auftrags. Der in TB-146 abgelehnte Aufruf enthielt `chmod +x`; `Bash(chmod:*)` steht in `deny`. Ein Heredoc und die Umleitung nach `$TMPDIR` liefen in TB-146 Schritt 0a.
- **Offen — zeigt nur der Mac:** ob Claude Code im Modus `manual` für einen Befehl ausserhalb von `deny` und `ask` nachfragt — dann gilt das Abbruchkriterium.

## Schritt 0 — Sicherung, Ausgang

**0a.** Zuerst, vor allem anderen, diese drei Blöcke:

```sh
git status --porcelain > "$TMPDIR/tb147_0a.txt"
```

```sh
git status --porcelain
```

```sh
git rev-parse HEAD
```

Soll: HEAD `e39cc44c1b419a21512c9a6e9492f66233c366fb` und genau diese drei Einträge (Reihenfolge egal); jeder andere oder weitere Eintrag: **ABBRUCH**.

```text
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-147_rest_tb146_journal_ergebnis.md
```

Dann Schritt 0 committen ⇒ **⟨S0⟩** (die Ausgabe des vierten Blocks):

```sh
git add docs/projektfuehrung/UEBERGABE.md docs/auftraege/AKTUELLER_AUFTRAG.md docs/auftraege/MAC_TB-147_rest_tb146_journal_ergebnis.md
```

```sh
git commit -m "TB-147 Schritt 0: Stand des steuernden Chats vor TB-147"
```

```sh
git push
```

```sh
git rev-parse HEAD
```

Erst jetzt den Beleg zu 0a ablegen:

```sh
cp "$TMPDIR/tb147_0a.txt" docs/belege/TB-146/t147_0a_status.txt
```

```sh
cmp "$TMPDIR/tb147_0a.txt" docs/belege/TB-146/t147_0a_status.txt; echo "rc $?"
```

Soll: `rc 0`, sonst keine Ausgabe.

**0b. Ausgang** — Zeilen und md5 der drei Zieldateien von TB-146 und von `JOURNAL.md`, md5 des Werkzeugs:

```sh
wc -l docs/projektfuehrung/ARBEITSWEISE.md docs/projektfuehrung/UMZUG.md docs/projektfuehrung/BACKLOG.md docs/projektfuehrung/JOURNAL.md > docs/belege/TB-146/t147_0b_ausgang.txt 2>&1; echo "rc $?" >> docs/belege/TB-146/t147_0b_ausgang.txt
```

```sh
md5 docs/projektfuehrung/ARBEITSWEISE.md docs/projektfuehrung/UMZUG.md docs/projektfuehrung/BACKLOG.md docs/projektfuehrung/JOURNAL.md docs/belege/TB-146/tb146_einfuegen.py > docs/belege/TB-146/t147_0b_md5.txt 2>&1; echo "rc $?" >> docs/belege/TB-146/t147_0b_md5.txt
```

Soll (beide Belege lesen): `ARBEITSWEISE.md` 2 531 Z., `b856395e6c1df8581cf9a44ca33c441e` · `UMZUG.md` 392 Z., `017136adf27c96b861cab1357276b41c` · `BACKLOG.md` 395 Z., `3caf2260ef772e453b80a4fbdb3491a6` · `JOURNAL.md` 10 669 Z., `c5102f2d0aace7e1821017f757c92225` · Zeile `total` 13 987 · Werkzeug md5 `483dae103b6611ad0f074297294fc9b9`. Weicht ein Wert der vier Dateien ab: vermerken, weiter — das Werkzeug prüft selbst. Weicht der md5 des Werkzeugs ab: **ABBRUCH**. Der sha256 des Werkzeugs wird nicht gemessen (keine belegte Befehlsform); dass das Werkzeug wie am HEAD liegt, zeigt 0a.

## Schritt A — Modus messen

Genau die Zeile, die in TB-146 lief (`docs/belege/TB-146/a_modus.kopf.txt` Z. 2); die Ausgabe wird nicht umgeleitet, ihre zwei Zeilen stehen wörtlich im Ergebnis:

```sh
p=$$; while [ "$p" -gt 1 ]; do case "$(ps -o comm= -p "$p")" in claude|*/claude) break ;; esac; p=$(ps -o ppid= -p "$p" | tr -d ' '); done; echo "EIGEN=$p"; ps -o command= -p "$p"
```

Soll: Die Prozesszeile trägt `--permission-mode manual`; sonst **ABBRUCH**. Dazu die eigene Aussage der Sitzung zu ihrem Berechtigungsmodus (oder „nicht bekannt“), als Aussage gekennzeichnet.

## Schritt N — der numstat-Beleg, der in TB-146 fehlt; Vergleich

```sh
trading-env/bin/python3 -B docs/belege/TB-146/tb146_einfuegen.py numstat 7f0b59d e39cc44 > docs/belege/TB-146/e_numstat.txt 2>&1; echo "rc $?" >> docs/belege/TB-146/e_numstat.txt
```

Soll (Beleg lesen): 23 Zeilen — die Kopfzeile, 16 Zeilen `roh:` (die 13 Belege von TB-146 und die drei Zieldateien), dann genau (⇥ steht für einen Tabulator):

```text
Soll docs/projektfuehrung/ARBEITSWEISE.md 16⇥0 · Ist [16, 0] · gleich
Soll docs/projektfuehrung/BACKLOG.md 9⇥0 · Ist [9, 0] · gleich
Soll docs/projektfuehrung/UMZUG.md 10⇥0 · Ist [10, 0] · gleich
weitere Dateien ausser Belegen und Ergebnis: keine
Gesamt: wie Soll, keine entfernte Zeile in den Zieldateien
rc 0
```

Endet der Beleg anders: melden, weiter — **kein Abbruch,** keine Zeile von Hand richten.

```sh
trading-env/bin/python3 -B docs/belege/TB-146/tb146_einfuegen.py vergleich > docs/belege/TB-146/t147_n_vergleich.txt 2>&1; echo "rc $?" >> docs/belege/TB-146/t147_n_vergleich.txt
```

Soll: 17 Zeilen — die Kopfzeile, 14 Zeilen `… · Vorkommen 1 · GLEICH`, `Gesamt: alle zeichengleich, je genau einmal`, `rc 0`; der Beleg ist bytegleich mit `e_vergleich.txt` aus TB-146 (derselbe md5 in Schritt F). Sonst: melden, weiter.

## Schritt J — Journalblock

Die Sitzung schreibt ihren Block mit dem Schreibwerkzeug nach `docs/belege/TB-146/j_block.md`. Gliederung wie in TB-146, Schritt J (Vorbild: Block EL, `JOURNAL.md` ab Z. 10291): Kopfzeile, Quellenzeile (`*Quelle: …*` mit dem Pfad des Ergebnisses), Absatz „**Quelle:**“ (Sitzung TB-147, Eingang `e39cc44`, Commits `7f0b59d`, `e39cc44`, ⟨S0⟩; die späteren in Worten), `### Was gemessen ist`, `### Was offen bleibt`, Schlusszeile `*Geschrieben <Datum> von der Mac-Sitzung TB-147. Quellenvermerk: siehe Kopf.*`. In eigenen Worten: was TB-146 tat (Schritt 0, A, E), **der Abbruch von TB-146** mit dem Grund aus `abbruch.txt`, **der Abschluss mit TB-147** (numstat-Beleg, dieser Block, Ergebnis). Nicht in den Block: der Nachtrag J1 — den setzt das Werkzeug ein.

Was das Werkzeug am Block prüft (Z. = Zeile im Werkzeug):

| Bedingung | Z. |
|---|---|
| Die Kopfzeile beginnt mit `## EM — TB-146` — also etwa `## EM — TB-146 und TB-147: …`. Mit `## EM — TB-147` weist das Werkzeug ab (rc 2). | 198 |
| genau eine Zeile `### Was gemessen ist`, direkt davor eine Leerzeile | 199 |
| genau eine Zeile `### Was offen bleibt` | 200 |
| keine Zeile, die nur aus `---` besteht (die Trennzeile einer Tabelle ist erlaubt); die letzte Zeile beginnt mit `*Geschrieben` | 201 |
| die erste Zeile von J1 steht weder im Block noch im Journal | 202 |
| die Datei endet mit einem Zeilenende | 29 |

Drei weitere Bedingungen betreffen nicht den Block: das Journal (Z. 203), den BACKLOG (Z. 204) und die Zahl der J1-Zeilen gegen den Sollwert im Auftrag TB-146 (Z. 205).

```sh
trading-env/bin/python3 -B docs/belege/TB-146/tb146_einfuegen.py journal docs/belege/TB-146/j_block.md --probe > docs/belege/TB-146/j_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-146/j_journal_probe.txt
```

Soll: 12 Zeilen — die Kopfzeile, 8 Bedingungen mit `· ja`, `Kennung EM (erwartet EM) · Blockzeilen <b> · J1-Zeilen 7 · Zeilen +<n> (= Block + J1 + 1 + 3)` mit n = b + 11, `Gesamt: nichts geschrieben (Probe)`, `rc 0`. **rc 2:** die Bedingung mit `NEIN` lesen, den Block mit dem Schreibwerkzeug richten, denselben Block noch einmal ausführen — kein Abbruch. **rc 3** und die Zeile `ABBRUCH: …` beginnt mit `docs/belege/TB-146/j_block.md`: ebenso. **rc 3 sonst, rc 1 oder ein Traceback: ABBRUCH.** Nennt das Werkzeug eine andere Kennung als EM: diese nehmen und melden.

Erst nach `rc 0` der Probe, und **genau einmal** (ein zweiter Lauf wird mit rc 2 abgewiesen und überschriebe den Beleg):

```sh
trading-env/bin/python3 -B docs/belege/TB-146/tb146_einfuegen.py journal docs/belege/TB-146/j_block.md > docs/belege/TB-146/j_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-146/j_journal.txt
```

Soll: wie die Probe, nur die Kopfzeile ohne ` (Probe)` und die vorletzte Zeile `Gesamt: geschrieben und zurueckgelesen: docs/projektfuehrung/JOURNAL.md`, `rc 0`; `JOURNAL.md` hat danach 10 669 + n Zeilen. Dann der Commit ⇒ **⟨J⟩**:

```sh
git add docs/projektfuehrung/JOURNAL.md docs/belege/TB-146/t147_0a_status.txt docs/belege/TB-146/t147_0b_ausgang.txt docs/belege/TB-146/t147_0b_md5.txt docs/belege/TB-146/e_numstat.txt docs/belege/TB-146/t147_n_vergleich.txt docs/belege/TB-146/j_block.md docs/belege/TB-146/j_journal_probe.txt docs/belege/TB-146/j_journal.txt
```

```sh
git commit -m "TB-147 J: Journalblock zu TB-146 und TB-147, numstat-Beleg"
```

```sh
git push
```

```sh
git rev-parse HEAD
```

## Schritt F — Ergebnis, Abgabe

**Masse für die Tabelle „Belege“** (ein Block; die Ausgabe wird nicht umgeleitet):

```sh
wc -l docs/belege/TB-146/e_probe.txt docs/belege/TB-146/e_einfuegen.txt docs/belege/TB-146/e_vergleich.txt docs/belege/TB-146/e_zweitlauf.txt docs/belege/TB-146/t147_0a_status.txt docs/belege/TB-146/t147_0b_ausgang.txt docs/belege/TB-146/t147_0b_md5.txt docs/belege/TB-146/e_numstat.txt docs/belege/TB-146/t147_n_vergleich.txt docs/belege/TB-146/j_block.md docs/belege/TB-146/j_journal_probe.txt docs/belege/TB-146/j_journal.txt; md5 docs/belege/TB-146/e_probe.txt docs/belege/TB-146/e_einfuegen.txt docs/belege/TB-146/e_vergleich.txt docs/belege/TB-146/e_zweitlauf.txt docs/belege/TB-146/t147_0a_status.txt docs/belege/TB-146/t147_0b_ausgang.txt docs/belege/TB-146/t147_0b_md5.txt docs/belege/TB-146/e_numstat.txt docs/belege/TB-146/t147_n_vergleich.txt docs/belege/TB-146/j_block.md docs/belege/TB-146/j_journal_probe.txt docs/belege/TB-146/j_journal.txt
```

Soll, soweit vorhersagbar: `t147_0a_status.txt` 3 Z., `703b1ea2c5ac33476e1e319529d86d8b` · `e_numstat.txt` 23 Z., `9c732eaf8f71c26e812dfc2ab3dea1a3` · `t147_n_vergleich.txt` und `e_vergleich.txt` je 17 Z., `ee1e663299efeb79d2425a18ed56aeeb` · `e_probe.txt` 21, `e_einfuegen.txt` 24, `e_zweitlauf.txt` 29 Z.

**Ergebnis** `docs/ERGEBNIS_TB-146_regelwerk_dokunachtrag_0910.md`, mit dem Schreibwerkzeug; die Überschrift nennt TB-146 und TB-147:

- **Kopf:** Stand; Commits von TB-146: `7f0b59d` (Schritt 0), `e39cc44` (Abbruch); von TB-147: ⟨S0⟩, ⟨J⟩ und ⟨F⟩ als „der Commit, der dieses Ergebnis trägt“ (seine Kennung steht in `t147_f_numstat.txt` Z. 1 und in der Schlussmeldung, nicht in ihm selbst).
- **„Kurz“:** Tabelle Schritt · Soll · Ist für **beide** Aufträge. Die Zeilen zu TB-146 Schritt 0, A und E kommen aus den Belegen dort, je mit Dateiname (`0a_status.txt`, `0b_ausgang.txt`, `a_modus.txt`, `e_probe.txt`, `e_einfuegen.txt`, `e_vergleich.txt`, `e_zweitlauf.txt`, `abbruch.txt`). Dann TB-147: 0a, 0b, A (beide Ausgabezeilen wörtlich), N, J, F. Zu `t147_f_porcelain.txt` und `t147_f_numstat.txt` steht „nach der Abgabe gemessen, siehe Beleg“; die Werte nennt die Schlussmeldung.
- **„Belege“:** Tabelle Datei · Befehl wörtlich · Zeilen · md5 für die 12 Dateien des Blocks oben. In der Spalte Befehl steht für die vier `e_*` aus TB-146: „wie Auftrag TB-146, Schritt E (dort als `PY WZ …`)“; für die Belege von TB-147 der Befehl wörtlich aus diesem Auftrag; zu `j_block.md`: „von der Sitzung geschrieben“.
- **„Abweichungen vom Auftrag“** — mindestens: der Abbruch von TB-146 mit dem Grund aus `abbruch.txt`; Commit ⟨E⟩ ist durch den Abbruch-Commit `e39cc44` ersetzt; keine Kopfdateien zu `e_*`; der Rest (numstat-Beleg, Journalblock, Ergebnis) kam mit TB-147. Dazu jede Abweichung von TB-147 selbst, auch kleine.
- **„Nicht getan“:** die Posten (a) bis (g) aus TB-146, `## Nicht in TB-146` (dort Z. 125–131), wörtlich; dazu die Posten unter „Nicht in TB-147“ unten.
- **„In einfacher Sprache“;** Rückfragen an den Betreiber samt Antwort wörtlich.

**Abgabe** ⇒ **⟨F⟩** (die Ausgabe des vierten Blocks):

```sh
git add docs/ERGEBNIS_TB-146_regelwerk_dokunachtrag_0910.md
```

```sh
git commit -m "TB-147 Abgabe: Ergebnis zu TB-146 und TB-147"
```

```sh
git push
```

```sh
git rev-parse HEAD
```

**Nach der Abgabe:**

```sh
git status --porcelain > "$TMPDIR/tb147_f.txt"
```

```sh
cp "$TMPDIR/tb147_f.txt" docs/belege/TB-146/t147_f_porcelain.txt
```

```sh
cmp "$TMPDIR/tb147_f.txt" docs/belege/TB-146/t147_f_porcelain.txt; echo "rc $?"
```

Soll: `rc 0`; der Beleg ist leer (0 B).

```sh
trading-env/bin/python3 -B docs/belege/TB-146/tb146_einfuegen.py numstat 7f0b59d ⟨F⟩ docs/belege/TB-146/j_block.md > docs/belege/TB-146/t147_f_numstat.txt 2>&1; echo "rc $?" >> docs/belege/TB-146/t147_f_numstat.txt
```

**Hier sind `Gesamt: ABWEICHUNG` und `rc 1` das Soll:** Das Werkzeug kennt die drei Dateien aus Schritt 0 von TB-147 nicht und nennt sie als „weitere Dateien“. Soll: die Kopfzeile, 29 Zeilen `roh:` (ohne Sollwert), dann genau (⇥ = Tabulator, n aus Schritt J):

```text
Soll docs/projektfuehrung/ARBEITSWEISE.md 16⇥0 · Ist [16, 0] · gleich
Soll docs/projektfuehrung/BACKLOG.md 9⇥0 · Ist [9, 0] · gleich
Soll docs/projektfuehrung/JOURNAL.md <n>⇥0 · Ist [<n>, 0] · gleich
Soll docs/projektfuehrung/UMZUG.md 10⇥0 · Ist [10, 0] · gleich
weitere Dateien ausser Belegen und Ergebnis: docs/auftraege/AKTUELLER_AUFTRAG.md docs/auftraege/MAC_TB-147_rest_tb146_journal_ergebnis.md docs/projektfuehrung/UEBERGABE.md
Gesamt: ABWEICHUNG
rc 1
```

Jede andere Zeile mit `ABWEICHUNG`, ein anderer Name unter „weitere Dateien“ oder `rc 0`: melden — kein Abbruch. Dann der Schluss-Commit:

```sh
git add docs/belege/TB-146/t147_f_porcelain.txt docs/belege/TB-146/t147_f_numstat.txt
```

```sh
git commit -m "TB-147 F: porcelain und numstat nach der Abgabe"
```

```sh
git push
```

```sh
git rev-parse HEAD
```

```sh
git status --porcelain
```

**Schlussmeldung:** die Rohausgabe des letzten Blocks wörtlich (Soll: leer); ⟨S0⟩, ⟨J⟩, ⟨F⟩ und die Kennung des Schluss-Commits (Ausgabe des Blocks davor); die letzten 7 Zeilen von `t147_f_numstat.txt`; jede Abweichung.

## Abbruchkriterien — melden, nicht reparieren

- 0a weicht ab (Einträge oder HEAD), oder der md5 des Werkzeugs in 0b weicht ab.
- Schritt A: Die Prozesszeile trägt nicht `--permission-mode manual`.
- Schritt J: `journal` (Probe oder Lauf) endet mit rc 3 und einer Zeile `ABBRUCH: …`, die nicht mit dem Pfad der Blockdatei beginnt, mit rc 1 oder mit einem Traceback.
- **Claude Code lehnt einen Aufruf ab oder verlangt eine Bestätigung** (ganze Sitzung): melden, nicht umgehen, nicht in anderer Form wiederholen. Verlangt schon Schritt 0 oder der Abbruchweg selbst eine Bestätigung: nichts weiter versuchen, den Wortlaut der Frage als Antwort im Chat melden.
- Eine Datei ausserhalb der Liste müsste geändert werden; `git push` scheitert zweimal.

**Kein Abbruch** (weiter, unter „Abweichungen“ nennen): `numstat 7f0b59d e39cc44` oder `vergleich` endet nicht wie Soll; 0b weicht bei einer der vier Dateien ab; `journal` endet mit rc 2 oder mit rc 3 und einer Meldung, die mit dem Pfad der Blockdatei beginnt (richten, neu); die Kennung ist nicht EM; `cmp` meldet einen Unterschied; `t147_f_porcelain.txt` ist nicht leer; der Schluss-numstat endet nicht wie Soll.

**Bei Abbruch** — nur diese Formen: Grund, Wortlaut der Ablehnung und Stand mit dem Schreibwerkzeug nach `docs/belege/TB-146/abbruch_tb147.txt`, dann die vier Blöcke unten. Vor dem Commit dazu je ein Block der Form `git add <Pfad>` für jede Datei dieses Auftrags, die entstanden und noch nicht committet ist (Pfad wörtlich wie oben). Was geschrieben ist, bleibt stehen, nichts zurückdrehen. `JOURNAL.md` geht nur mit, wenn `journal` sie geschrieben hat und der erste Block nicht weniger als 10 669 Zeilen zeigt; sonst bleibt sie liegen und steht in der Meldung an erster Stelle.

```sh
wc -l docs/projektfuehrung/JOURNAL.md
```

```sh
git add docs/belege/TB-146/abbruch_tb147.txt
```

```sh
git commit -m "TB-147 Abbruch nach Vorschrift, Grund in abbruch_tb147.txt"
```

```sh
git push
```

## Nicht in TB-147

- Alles unter `## Nicht in TB-146` (dort (a) bis (g)) bleibt auch hier ungetan.
- Die vier Kopfdateien zu `e_*` — sie entfallen; die Tabelle „Belege“ ersetzt sie.
- Die Abnahme von TB-146 und TB-147, `AKTUELLER_AUFTRAG.md` umstellen, die Ablage und die Projekt-Erinnerung (macht der steuernde Chat).

## In einfacher Sprache

Der vorige Auftrag (TB-146) hat die neuen Regeln ins Regelwerk eingetragen, hielt aber kurz vor dem Ende an, weil die Sitzung sich ein Hilfsmittel bauen wollte, das Claude Code nicht zuliess. Es fehlen ein Nachweis, der Eintrag im Journal und der Abschlussbericht. Dieser Auftrag holt genau das nach, mit Wort für Wort vorgegebenen Befehlen; am Regelwerk selbst ändert er nichts.

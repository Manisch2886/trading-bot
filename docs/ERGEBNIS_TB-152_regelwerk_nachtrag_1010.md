# ERGEBNIS TB-152 — Regelwerk-Nachtrag 10.10.2026

**Stand:** 11.10.2026, 11:16 · **Auftrag:** `docs/auftraege/MAC_TB-152_regelwerk_nachtrag_1010.md` · **Sitzung:** Mac, Claude Code, Opus 5.5, Prozesszeile `--permission-mode manual`
**Commits:** ⟨S0⟩ `415044cefed47c3a0e8751139aea52ef499295eb` (Schritt 0) · ⟨E⟩ `60cf33902cafe5e6826b93405c065153a63897c2` (36 Stücke) · ⟨F⟩ Abgabe-Commit `TB-152 Abgabe: Ergebnis, Journal EQ` · danach `TB-152 F: porcelain und numstat nach der Abgabe` — die Hashes der beiden letzten nennt die Schlussmeldung (ein Commit kann seinen eigenen Hash nicht tragen). Alle gepusht auf `main`.
**Base:** HEAD beim Start `6d700d4233712dab6f57c55cca2205b57a4f842a` (wie Soll).

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a Arbeitsbaum | HEAD `6d700d4`, genau 4 Einträge | wie Soll (`0a_status.txt`) |
| 0a Eröffnungsdatei verfolgt | eine Zeile | `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` |
| 0a `grep -c` in `ablage_soll.py` | ≥ 1 | 2 |
| 0a Werkzeug ableiten | sha256 `d5855393…f70f5` | gleich; Kopie im Belegordner noch einmal gemessen, gleich |
| 0a Commit ⟨S0⟩, Push | 4 Pfade | `415044c`, Push rc 0; `cmp` 0a-Datei gleich |
| 0b Ausgang | ARBEITSWEISE 2531/`b856395e…`, UMZUG 392/`017136ad…`, BACKLOG 422/`1cf506eb…`, JOURNAL 10816/`ec8f1995…` | alle vier gleich; UEBERGABE 3712 Z., `9316bfa06a84ca7db3d657d32312ded7` (ohne Soll) |
| A Modus | `--permission-mode manual` | `claude --permission-mode manual --effort high --remote-control --no-chrome` |
| E Probe | rc 0, 36 Stücke, 131 Zeilen, drei Dateien gleich | wie Soll; Ankerzeilen und Zeilen je Stück gleich den Angaben „Am HEAD“ in Anhang A (36/36, per Skript abgeglichen) |
| E Einfügen | rc 0, drei Dateien zurückgelesen | wie Soll |
| E Vergleich | rc 0, 36× `Vorkommen 1 · GLEICH` | wie Soll |
| E Zweiter Lauf | rc 2, alle 36 Kennungen, md5 gleich | wie Soll |
| E Commit ⟨E⟩, Push | 11 Pfade | `60cf339`, Push rc 0 |
| E numstat | 43/0, 47/0, 41/0, JOURNAL nicht dabei, keine weiteren Dateien | wie Soll, rc 0 (`e_numstat.txt`) |
| J Probe | acht Bedingungen `ja`, Kennung EQ, J1-Zeilen 24, rc 0 | wie Soll; Blockzeilen 21, Zeilen +49 |
| J Journal | rc 0 | wie Soll, Block **EQ**, `JOURNAL.md` +49/0 |
| F Vergleich | wie in E | rc 0, 36× gleich (`f_vergleich.txt`, bytegleich zu `e_vergleich.txt`) |
| F UEBERGABE | wie 0b | 3712 Z., `9316bfa0…` — gleich |
| F porcelain, numstat | 0 B; Zieldateien wie E, JOURNAL +49/0 | nach der Abgabe gemessen, siehe Beleg |

## Belege

Ordner `docs/belege/TB-152/`. Bytes, Zeilen und md5 vor dem Abgabe-Commit gemessen; `f_porcelain.txt` und `f_numstat.txt` entstehen erst danach.

| Datei | was | Befehl | Bytes | Zeilen | md5 |
|---|---|---|---|---|---|
| `0a_status.txt` | Arbeitsbaum beim Start | `git status --porcelain` (über `$TMPDIR/tb152_0a.txt`, `cmp` gleich) | 186 | 4 | `676846b82453019666daa28f5c957728` |
| `tb152_einfuegen.py` | Werkzeug, abgeleitet aus TB-146 | Ableitungsbefehl aus 0a | 12515 | 242 | `78209a33b43e4731136799161213dadc` |
| `0b_ausgang.txt` | Zeilen und md5 der vier Zieldateien und der UEBERGABE an ⟨S0⟩ | `wc -l`, `md5 -q` | 354 | 5 | `4ffdc3204cfa53cd2f53d0342f2aac1c` |
| `a_modus.txt` | Prozesszeile der Sitzung. **Aussage der Sitzung:** Ihr Berechtigungsmodus ist ihr nicht bekannt; sie stützt sich allein auf die Prozesszeile. | Befehl aus Schritt A | 87 | 2 | `489268b77b632a36383e77b3c40da3de` |
| `e_probe.txt` | Probe | `PY WZ probe` | 6744 | 43 | `9c0f979959c628836ff3a55c50d0af37` |
| `e_einfuegen.txt` | Einfügen | `PY WZ einfuegen` | 6935 | 46 | `6531d3bc278f6d6a311a9312077f2223` |
| `e_vergleich.txt` | Vergleich nach dem Einfügen | `PY WZ vergleich` | 3534 | 39 | `857f73f4293b71cd3813f95b47678dfe` |
| `e_zweitlauf.txt` | zweiter Lauf mit md5 davor und danach | `md5`, `PY WZ einfuegen`, `md5` | 7699 | 51 | `a6255ed49e406de39d29bee4b576e88d` |
| `e_numstat.txt` | numstat ⟨S0⟩..⟨E⟩ gegen Soll | `PY WZ numstat 415044c… 60cf339…` | 940 | 18 | `21ed00fbcc8493e6c53c39269d7085b1` |
| `j_block.md` | Journalblock der Sitzung, ohne J1/J2 | geschrieben von der Sitzung | 1982 | 21 | `6161b60077d2deb514bce0694fa9bf04` |
| `j_journal_probe.txt` | Journal, Probe | `PY WZ journal … --probe` | 679 | 12 | `b1d32dc969101aa2d84908d786da1c53` |
| `j_journal.txt` | Journal, geschrieben | `PY WZ journal …` | 708 | 12 | `e51466a0fad7168870b0290a5e2171ab` |
| `f_vergleich.txt` | Vergleich nach dem Journal | `PY WZ vergleich` | 3534 | 39 | `857f73f4293b71cd3813f95b47678dfe` |
| `f_uebergabe.txt` | Zeilen und md5 der UEBERGABE | `wc -l`, `md5 -q` | 72 | 1 | `8c0f16692257daca5a83ac926191f587` |
| `f_porcelain.txt` | Arbeitsbaum nach der Abgabe | `git status --porcelain` (über `$TMPDIR/tb152_f.txt`) | nach der Abgabe | | |
| `f_numstat.txt` | numstat ⟨S0⟩..⟨F⟩ | `PY WZ numstat 415044c… ⟨F⟩ docs/belege/TB-152/j_block.md` | nach der Abgabe | | |

## Abweichungen vom Auftrag

Keine bei den Sollwerten. Geprüft und gleich: HEAD und die vier Einträge in 0a; `git ls-files` der Eröffnungsdatei; `grep -c` ≥ 1; sha256 des Werkzeugs (zweimal); Zeilen und md5 der vier Zieldateien in 0b; Prozesszeile in A; rc und Schlusszeilen von Probe, Einfügen, Vergleich und zweitem Lauf; md5 vor und nach dem zweiten Lauf; numstat 43/41/47 mit 0 entfernten Zeilen; acht Bedingungen, Kennung EQ und J1-Zeilen 24 in J; Vergleich und UEBERGABE-md5 in F.

Kleine Abweichungen im Vorgehen, ohne Wirkung auf eine Datei:

1. Neben den Befehlen des Auftrags liefen lesende Befehle: ein `ls docs/belege/TB-152` mit dem 0a-Befehl (bestätigte, dass der Ordner noch fehlte), `git diff -U0` und `git diff --numstat` vor dem Commit ⟨E⟩ (Reihenfolge der Stücke an den gemeinsamen Ankern angesehen), ein `grep` und ein Lesen im Werkzeug (Bedingungen von `journal`), `date` und `git log` (Uhrzeit), ein Abgleichskript in Python für die Ankerzeilen gegen Anhang A und `wc`/`md5` über die Belege für die Tabelle oben.
2. Die Commits ⟨S0⟩ und ⟨E⟩ tragen unter dem Betreff die Zeilen `Co-Authored-By` und `Claude-Session` (Vorgabe der Umgebung).

Claude Code hat in dieser Sitzung keinen Aufruf abgelehnt und keine Bestätigung verlangt.

## Nicht getan

Nach „Nicht in TB-152“ im Auftrag, unverändert beim steuernden Chat bzw. Betreiber:

- (a) S40 „Zu prüfen, nicht untersucht“ — E8
- (b) S46 Entscheide des Betreibers ohne Eile (b) bis (d) — E8
- (c) S47 „Später“, darin die 27 Formhinweise aus TB-146 und Nr. 9 bis 11 aus TB-141 — E8
- (d) S02 Fehler Nr. 39, Erstfassung — E1
- (e) S09, S10 Fehler Nr. 45 und 46 ohne Zeile in Abschnitt 0 — E2 (stehen in J2)
- (f) S49 nur im Journal (J2) — E2
- (g) S32, S33, S48 schon im Ziel — E9
- (h) V6 „erfüllt“ nur mit Nachweis der Sitzung — geht in den Bau von TB-154
- (i) S45 falsche Fundstelle im Ergebnis TB-148 — Befund in B2
- (j) S50 — keine Regel in der Quelle
- (k) S01, S23–S27, S22 — Einzelfälle, Zählungen oder schon im Ziel; Auswahl des Helfers strittig
- (l) S11 zweiter Satz — Einzelfall
- (m) S19 der `jq`-Befehl im Wortlaut — R03 verweist auf die UEBERGABE
- (n) S28 Zusammenfassung zur Anweisung 09:16 — ersetzt durch den Wortlaut (R05, U3)
- (o) E10 Ersetzungen in bestehenden Zeilen (UMZUG Z. 228, 260, 270–272; ARBEITSWEISE Z. 118, 212, 2480) — strittig, **Entscheid offen**
- (p) Ablage, Projekt-Erinnerung, `ablage_soll.py` (TB-151) und der Codeblock der alten Fassung in `UMZUG.md` Abschnitt 6 — macht der steuernde Chat

**Für den Betreiber:** nichts zu tun aus dieser Sitzung; Entscheid zu (o) liegt beim steuernden Chat. Die drei Dateien in `$TMPDIR` (`tb152_0a.txt`, `tb152_einfuegen.py`, `tb152_f.txt`) bleiben liegen.

## In einfacher Sprache

Die neuen Regeln und Befunde vom 9. bis 11. Oktober standen bisher nur in der Übergabe. Jetzt stehen sie dort, wo man sie sucht: 36 Stücke im Regelwerk, in der Umzugsanleitung und im Backlog, dazu ein Journaleintrag (EQ). Ein kleines Programm hat die fertigen Texte eingefügt, vorher geprüft, dass jede Stelle eindeutig ist, und danach nachgezählt. Es wurde nur ergänzt, keine Zeile gelöscht oder geändert, und kein Programm des Projekts angefasst. Alles hat beim ersten Mal so geklappt, wie der Auftrag es vorhergesagt hat.

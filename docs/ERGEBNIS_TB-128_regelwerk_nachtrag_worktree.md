# TB-128: Ergebnis. Regelwerk-Nachtrag 01.10.2026, zweiter Teil (Fehlerregeln, Fable-Ablage, kalter Leser, R31 (b), R49 (e), 5b-Bewertung) — E1–E7 zeichengleich; Worktree `tb123_vorher` nach drei erfüllten Messungen entfernt

**Sitzungstitel:** `TB-128` · **Stand:** 02.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-128_regelwerk_nachtrag_worktree.md` ·
**Belege:** `docs/belege/TB-128/`
**Eingang:** `eeee21d` (TB-127 D3). Commits: `7238842` (Schritt 0: Stand des steuernden Chats), `472a788` (A/C:
Regelwerk-Nachtrag, Nachweis), der Abgabe-Commit (D: dieses Dokument, Journal DZ) und ein kleiner Commit mit
`d3_porcelain.txt`. Nach jedem Commit gepusht.
**Freigabe:** pauschal für Handwerk ohne Sperrlistennähe (Betreiber 26.09.2026); Worktree per Karte 01.10.2026, ca.
22:20 („TB-128 entfernt (Empfohlen)“). **Keine Rückfrage an den Betreiber in dieser Sitzung.**
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6). Modell laut Selbstauskunft Opus 5.5.
**Kein Abbruchkriterium ausgelöst.**

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | genau die 7 Einträge des steuernden Chats | **7/7 gleich**, in `$TMPDIR/tb128_0a.txt` **bevor** `docs/belege/TB-128/` entstand, danach nach `0a_status.txt` kopiert ⇒ `7238842` |
| ⭐ 0b (1) | `git -C <pfad> status --porcelain`: genau vier `??`-Zeilen (`data_sicherung`, `logs`, `research/turn_of_month/daten`, `trading-env`), keine `M` | **genau diese vier, rc 0, 0 `M`-Zeilen** |
| 0b (2) | jeder der vier ein Symlink (`test -L`) | **4/4 rc 0**, alle auf den gleichnamigen Pfad im Hauptordner |
| 0b (3) | `git merge-base --is-ancestor <HEAD des Worktrees> main` rc 0 | HEAD `c0644058efb0…` ⇒ **rc 0** |
| ⭐ 0b Entfernen | bei drei erfüllten Messungen `git worktree remove --force`, `prune`, `list` | `remove --force` **rc 0**, `prune` rc 0 (keine Ausgabe), `git worktree list` zeigt **eine Zeile**: `/Users/jaquelineloffler/trading-bot  7238842 [main]`. Ordner existiert nicht mehr; die vier Symlink-Ziele im Hauptordner sind alle vorhanden |
| 0c | sha256/Zeilen der zwei Zieldateien | `0c_ausgang.txt` (ARBEITSWEISE 2375 Z., BACKLOG 242 Z.) |
| E1–E7 | Anker vorher 1, ausgeführt, erste Zeile nachher 1 | **7/7**: je Anker 1, ausgeführt ja, Text nachher 1 (`einfuegungen.txt`, Skript `einfuegen.py` liest Zieldatei, Anker, Art und Text aus dem Auftrag; vorher Probelauf `--probe` ohne Schreiben) |
| Vorzählung | `Aus der Abnahme TB-127`, `Aus Fable 27c, 29a und 29b`, `Fehler Nr. 14`, `project_info`, `kalter Leser` in den Zieldateien 0 | vor A in beiden Zieldateien je **0** — deckt sich mit dem steuernden Chat |
| C1 | `einfuegungen.txt` E1–E7 | wie E1–E7 oben |
| C2 numstat | entfernt 0 in beiden Dateien | ARBEITSWEISE **14/0**, BACKLOG **12/0** (`c2_numstat.txt`). 14 = 13 Textzeilen (E1–E4, E6: 10; E5: 3) + 1 Leerzeile nach E5; 12 = 11 Textzeilen E7 + 1 Leerzeile davor/danach (die andere war schon da) |
| C3 | jeder Text genau einmal als Block, Bytevergleich | **7/7 GLEICH**, je Vorkommen 1 und an Zeilengrenzen 1 (`c3_vergleich.py`, eigener Parser, unabhängig von `einfuegen.py`) |

## Einfügestellen

| | Datei | nach/vor Zeile (vor dem Einfügen) |
|---|---|---|
| E1 | ARBEITSWEISE | nach 80 (Abschnitt 0, „Fable-Übergabetexte kurz“) |
| E2 | ARBEITSWEISE | nach 100 („Karte nur für echte Betreiberentscheide“) |
| E3 | ARBEITSWEISE | nach 159 (`project_read` nie zur Prüfung …) |
| E4 | ARBEITSWEISE | nach 193 („Gegenleser eng zuschneiden“), sechs Tabellenzeilen |
| E5 | ARBEITSWEISE | nach 2251 (22.11, „🟡 · ca. 450 000“.), zwei Absätze; die Leerzeile danach war schon da |
| E6 | ARBEITSWEISE | nach 2282 (22.12, Probe TB-125), Fortsetzungszeile ohne Leerzeilen |
| E7 | BACKLOG | vor 231 (`## 6 — Geparkt, null Arbeit`), zwei `###`-Blöcke; die Leerzeile davor war schon da |

## Abweichungen und Lesarten

- **Anker in doppelten Backticks** (E3, E6) sind als Markdown-Codespanne gelesen: Inhalt ohne die je eine
  Leerstelle innen, also `` `project_read` nie zur Prüfung grosser Ablagedateien `` bzw.
  `` `docs/ERGEBNIS_TB-125_regelwerk_nachtrag.md`. ``. Gezählt jeweils 1.
- `c3_vergleich.py` scheiterte im ersten Lauf an seinem eigenen Zerleger (Schnitt an `### Aus Fable …` **im**
  E7-Codeblock — dieselbe Falle wie in TB-127). Korrigiert auf Schnitte nur an `#### E<n>` und `## `, danach 7/7.
- `git worktree list` nach `prune`: Das Werkzeug gibt nur noch die Hauptordnerzeile aus (Pfad, Kurz-Hash, `[main]`);
  ein Hinweis auf den entfernten Worktree erscheint nicht, auch `prune` meldet nichts.
- **Journal:** letzter Block vorher **DY** (TB-127) ⇒ neuer Block **DZ**, eingefügt nach DY und vor `---` /
  `## Wiederkehrende Lehren` (Lesart wie seit TB-50). **Nächste Kennung nach DZ: EA** — gemessen am Muster im Journal
  (`AZ` → `BA`, `BZ` → `CA`, `CZ` → `DA`); ein `E?`-Block existiert noch nicht.
- Der Worktree stand auf einem losgelösten HEAD (`detached HEAD`); es gab keinen Zweig dazu, der zu löschen wäre.

## Nicht getan

Einem späteren Auftrag vorbehalten:

- K2h/K2f (Wortlaut „Stellvertreter“ in `BACKLOG_ENTSCHEIDUNGEN.md` gegen „Merkmal“ in Fable 29b klären; K2f nach
  PRUEFPRINZIPIEN Reihe C);
- die drei Trägerstellen nach G1 (TB-119 Nr. 2);
- Fables 29a Abschnitt 1 (Umzugstakt des Verfahrensprüfers);
- Sonnet-Probe mit wirksam gesetztem Modell;
- `BACKLOG.md` in der Ablage erneuern (vorher 27.4-Prüfung);
- `docs/werkzeuge/registerkopie_abschnitte.py` entfernen — Betreiberentscheid, liegt nicht vor; die Datei ist
  unverändert.

Ausserdem nicht angefasst: Register, `UMZUG.md`, `PRUEFPRINZIPIEN.md`, `UEBERGABE*.md`, die `FABLE_*`-Dateien (nur
in Schritt 0 so committet, wie sie im Arbeitsbaum lagen).

## In einfacher Sprache

Die Regeln vom Abend des 01.10. stehen jetzt wörtlich im Regelwerk: Der steuernde Chat legt Unterlagen für Fable
selbst ab; aus den Fehlern Nr. 8, 9, 10 und 14 sind Prüfhaken in `ARBEITSWEISE.md` Abschnitt 0 geworden; dazu der
kalte Leser ohne Gedächtnis, die `project_info`-Regel und R31 (b) und R49 (e). In 22.12 steht jetzt, dass die
Sonnet-Probe aus TB-125 keine gültige war. In `BACKLOG.md` steht, wie die drei Fable-Antworten vom 27. bis 29.09.
bewertet wurden und was aus der Abnahme TB-127 offen ist. Ein Skript hat jeden Text aus dem Auftrag eingesetzt, ein
zweites, unabhängiges hat nachgeprüft, dass jeder Text genau einmal und Zeichen für Zeichen gleich dasteht.

Den alten Arbeitsordner `tb123_vorher` gibt es nicht mehr. Diesmal stand die richtige Prüfung davor: git zeigte nur
die vier erwarteten Verknüpfungen und keine geänderte Datei, und sein Stand ist vollständig in `main` enthalten.
Gelöscht wurden nur die Verknüpfungen selbst, nicht das, worauf sie zeigen.

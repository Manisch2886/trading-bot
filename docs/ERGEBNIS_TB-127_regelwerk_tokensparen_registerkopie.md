# TB-127: Ergebnis. Regelwerk-Nachtrag 01.10.2026 (Ampel, S1–S7, F1–F6, Abnahme TB-126) — E1–E9 zeichengleich; `registerkopie.py --abschnitte` 51/51 md5-gleich; Worktree `tb123_vorher` nicht entfernt (Messung ≠ Soll)

**Sitzungstitel:** `TB-127` · **Stand:** 01.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-127_regelwerk_tokensparen_registerkopie.md` ·
**Belege:** `docs/belege/TB-127/`
**Eingang:** `69b9ced` (Abgabe TB-126). Commits: `eaea530` (Schritt 0: Stand des steuernden Chats), `0e8b361` (A/C:
Regelwerk-Nachtrag, Nachweis), `02806ea` (B: `registerkopie --abschnitte`, Nachweis), der Abgabe-Commit (D: dieses
Dokument, Journal DY) und ein kleiner Commit mit `d3_porcelain.txt`. Nach jedem Commit gepusht.
Ausführungsreihenfolge wie vorgegeben: 0, A, C, B, D.
**Freigabe:** pauschal für Handwerk ohne Sperrlistennähe (Betreiber 26.09.2026); Regeln per Auswahlkarte 01.10.2026
(20:10 S1–S7, 21:25 F1–F6, 21:35 Ampel); Worktree per Karte 01.10.2026, ca. 20:45 („TB-127 entfernt mit --force
(Empfohlen)“). **Keine Rückfrage an den Betreiber in dieser Sitzung.**
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6). Modell laut Selbstauskunft Opus 5.5.
**Kein Abbruchkriterium ausgelöst.**

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | genau die 12 Einträge des steuernden Chats (optional `FABLE_UEBERGABE_2026-10-01_neuer_chat.md`) | **12/12 gleich** (sortierter Vergleich per Python), in den Scratch **bevor** `docs/belege/TB-127/` entstand; die optionale Datei lag **nicht** vor ⇒ `eaea530` |
| ⚠️ 0b Worktree | ausser `.git` genau 4 Einträge, alle Symlinks ⇒ `git worktree remove --force`, `prune` | **35 Einträge** (17 Symlinks, 13 Verzeichnisse, 5 Dateien) ⇒ **nicht entfernt**, kein `prune`. Befund siehe unten. Kein Abbruch |
| 0c | sha256/Zeilen der vier Zieldateien | `0c_ausgang.txt` (ARBEITSWEISE 2367 Z., UMZUG 374, BACKLOG 235, registerkopie.py 237) |
| E1–E9 | Anker vorher 1, ausgeführt, erste Zeile nachher 1 | **9/9**: je Anker 1, ausgeführt ja, Text nachher 1 (`einfuegungen.txt`, Skript `einfuegen.py` liest Datei, Anker, Art und Text aus dem Auftrag) |
| C2 numstat | entfernt nur E3/E4 (je 1 in ARBEITSWEISE); UMZUG, BACKLOG 0 | ARBEITSWEISE **10/2**, UMZUG **4/0**, BACKLOG **7/0**; die zwei entfernten Zeilen sind wörtlich die beiden ersetzten (in `c2_numstat.txt`) |
| C3 | jeder Text genau einmal als Block, Bytevergleich | **9/9 GLEICH**, je Vorkommen 1 und an Zeilengrenzen 1 (`c3_vergleich.py`, eigener Parser, unabhängig von `einfuegen.py`) |
| B2 (1) | `--abschnitte --ziel $TMPDIR/tb127_abschnitte`: 51 Dateien, md5 = Referenz | rc 0, **51 Dateien, md5 51 gleich / 0 ungleich**, keine Datei zusätzlich; Selbstprüfung BYTEGLEICH (829 231 B, Register am `db108a68ec57`, sha256 `b58046592205bfac…`) |
| B2 (2) | `--abschnitte --pruefen` (Standardziel) rc 0 | **rc 0**, BYTEGLEICH |
| B2 (3) | Teile-Modus `--pruefen` wie vorher (0, BYTEGLEICH) | vorher rc 0 BYTEGLEICH, nachher **rc 0 BYTEGLEICH**, Ausgabe gleich |
| B2 (4) | `git diff --numstat` | **126/6** (`registerkopie.py`; die 6 entfernten Zeilen sind Docstring-Zeilen und `--ziel`-Standard, der jetzt je Modus aufgelöst wird) |
| B2 (5) zusätzlich | Gegenproben | `--abschnitte --marken` rc 2; ein Byte an Abschnitt 17 angehängt ⇒ rc 1 (UNGLEICH); Abschnitt 33 fehlt ⇒ rc 1 (FEHLT); wiederhergestellt ⇒ rc 0 |
| B2 (6) | Referenzordner unberührt | `git status` nach B2: nur `registerkopie.py` und der Beleg |

## Befund 0b — Worktree `tb123_vorher` liegt weiter

Gemessen nach Auftrag (`find <pfad> -mindepth 1 -maxdepth 1 ! -name .git`, je mit Typ): **35 Einträge, davon 17
Symlinks** — Soll waren genau 4, alle Symlinks. Nach dem Wortlaut („Stimmt es nicht: nicht entfernen, Befund
benennen“) ist der Worktree **nicht entfernt** und `git worktree prune` nicht gelaufen. Alles in `0b_worktree.txt`.

**Lesart der Abweichung (gemessen, nicht ausgeführt):** Die „vier Symlinks“ aus der Abnahme TB-126 (B6) und der Karte
von 20:45/20:50 sind die vier **unverfolgten** Einträge laut `git -C <pfad> status --porcelain`: `data_sicherung`,
`logs`, `research/turn_of_month/daten`, `trading-env` — alle vier Symlinks auf den Hauptordner (der dritte liegt eine
Ebene tiefer und fällt aus dem `find` heraus). Daneben liegen der vollständige, unveränderte Checkout `c064405`
(„TB-122 Schritt 0“) und **14 weitere Symlinks**, die `git` ignoriert (`git check-ignore`: 14 ignoriert, 3 nicht;
keiner versioniert) — zehn Paper-Trading-/Broker-DBs, `benachrichtigungen_schliessung.db`, zwei Logs, `.env`, alle
auf den Hauptordner. Die im Auftrag vorgeschriebene `find`-Messung zählt den
Checkout mit und kann das Soll nie erreichen — der Auftrag hat die Prüfung falsch formuliert, nicht der Ordner hat
sich verändert.

⇒ **Für den nächsten Auftrag:** Messung als `git -C <pfad> status --porcelain` (Soll: genau die vier `??`-Zeilen, alle
Symlinks; keine `M`-Zeilen) formulieren, dann `git worktree remove --force <pfad>`. `--force` entfernt dabei nur die
Links selbst, nicht deren Ziele.

## Abweichungen und Lesarten

- **Journalblock DY** steht nach dem letzten Block (DX) und vor `---` / `## Wiederkehrende Lehren`, wie alle Blöcke
  seit TB-50 — „ans Ende“ als „nach dem letzten Block“ gelesen.
- **`--ziel`-Standard je Modus:** `argparse` hat jetzt `default=None`; der Teile-Modus und `--marken` setzen
  `docs/projektfuehrung`, der Abschnitts-Modus `docs/projektfuehrung/register_kopie`.
- **`--abschnitte --pruefen` ist strenger als die Vorlage:** Es prüft im Kopf auch Abschnittsnummer, `m`, Commit,
  Datum, sha256 und die Register-Zeilen `a–b` gegen die tatsächliche Lage des Bodys, und meldet Dateien mit Nummer
  über `m` als VERALTET (nichts gelöscht). Abschnittsnummern, die nicht bei 0 beginnen, ergeben rc 2 (Kopf „von 0–<m>“).
- `c3_vergleich.py` scheiterte im ersten Lauf an seinem eigenen Zerleger (er schnitt am `### Aus der Abnahme` **im**
  E9-Codeblock); korrigiert auf Schnitte nur an `### Datei` und `#### E<n>`, danach 9/9. Der Entwurf hatte zudem einen
  Backslash in einem f-String-Ausdruck — auf Python 3.9 ein Syntaxfehler, vor dem ersten Lauf behoben.

## Nicht getan

Ausdrücklich einem späteren Auftrag vorbehalten (Block 4 Nr. 4 des Umzugsblocks 01.10.2026, 08:20; Wortlaute noch
nicht vorbereitet):

- 5b-Bewertung zu 27c, 29a, 29b;
- K2h/K2f;
- die drei Trägerstellen;
- der kalte Leser ohne Gedächtnis;
- 29a Abschnitt 1–3;
- die `project_info`-Regel;
- R31 (b) und R49 (e) ins Regelwerk;
- Sonnet-Probe mit wirksam gesetztem Modell;
- `BACKLOG.md` in der Ablage erneuern (vorher 27.4-Prüfung).

Ausserdem:

- **Worktree `tb123_vorher` nicht entfernt** (siehe Befund 0b) — braucht einen Auftrag mit passender Messung.
- **`FABLE_UEBERGABE_2026-10-01_neuer_chat.md` ist noch nicht im Repo** — sie lag in 0a nicht im Arbeitsbaum.
- `registerkopie_abschnitte.py` (Vorlage) bleibt liegen; ihre Aufgabe übernimmt jetzt `registerkopie.py --abschnitte`.
  Entfernen ist nicht Gegenstand dieses Auftrags.
- Register, `REGISTER_INDEX.md`, die 51 Abschnittsdateien, `UEBERGABE*.md`: unverändert (B2 (6), `git status`).

## In einfacher Sprache

Die neuen Sparregeln vom Abend stehen jetzt wörtlich im Regelwerk: in `UMZUG.md` (die Ampel misst den Verlauf ohne
die feste Grundlast; ein Chat je Auftragsrunde), in `ARBEITSWEISE.md` Abschnitt 0 (sieben neue oder geänderte
Haken) und in `BACKLOG.md` (K4u und die offenen Punkte aus der Abnahme TB-126). Ein Skript hat jeden Text aus dem
Auftrag eingesetzt, ein zweites, davon unabhängiges hat nachgeprüft, dass jeder Text genau einmal und Zeichen für
Zeichen gleich dasteht.

Das Werkzeug `registerkopie.py` kann das Register jetzt selbst in eine Datei je Abschnitt schneiden. Es erzeugt
genau dieselben 51 Dateien, die schon in der Ablage liegen (alle 51 Prüfsummen gleich), und die alte Aufteilung in
vier Teile funktioniert unverändert.

Den alten Arbeitsordner `tb123_vorher` hat die Sitzung **nicht** gelöscht: Die vorgeschriebene Messung erwartete vier
Einträge und fand 35, und der Auftrag sagt für diesen Fall ausdrücklich „nicht entfernen“. Der Grund ist harmlos —
die Messung zählte den ganzen Arbeitsordner statt nur der vier zusätzlichen Verknüpfungen —, aber das zu korrigieren
ist eine Entscheidung für den nächsten Auftrag.

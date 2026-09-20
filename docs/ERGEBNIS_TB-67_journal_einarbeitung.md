# ERGEBNIS TB-67 — Die Journal-Seite nachgezogen (Mac-Sitzung, 20.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-67_journal_einarbeitung.md`. **Ausgeführt am
MacBook**, Zweig `main`, Ausgang `fe76857` (= `origin/main` beim Start), **reine
Dokumentation** — kein Interpreter ausser `python3` für Zählskripte, keine
Kursdaten, nichts ausserhalb `docs/`. Dieses Dokument wächst mit jedem Schritt
und wird je Schritt committet; die Commit-Liste steht am Ende.

*In einfacher Sprache, zu Beginn:* Acht Notizdateien, die seit dem 19.09. neben
dem Journal lagen, werden in das Journal übertragen, jeder neue Eintrag sagt,
aus welcher Notiz er stammt, und die vier schon übertragenen Notizen bekommen
diese Zeile nachträglich.

---

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

Beim Sitzungsstart (vor Schritt 0), wörtlich:

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20b_wortlaut_nulltage.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20c_kapitalpfad.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-09-20b_kalender.md
```

Vier Betreiber-Dateien, keine davon aus dieser Sitzung. **Schritt 0:** unverändert
committet als `481b9f7` (der Fall von `K2p`, wie in TB-62 gehandhabt). Danach
`git status --short`: **0 Zeilen** — erst dann wurde geschrieben.

⚠️ **`git push` wurde in dieser Sitzung vom Berechtigungsfilter der
Claude-Code-Umgebung abgelehnt** (Meldung: *„denied by the Claude Code auto mode
classifier"*). Alle Commits liegen lokal auf `main`; der Push ist am Ende
gesammelt vom Betreiber nachzuholen (`git push`, allein). Das ist eine
Abweichung von der Auflage *„Sichern: commit und push"* je Schritt — die
Commits sind gesetzt, die Pushes nicht.

---

## Nachweis 2 — Schritt 1: welche Journal-Nachträge wirklich offen sind

**Gemessen am 20.09.2026 gegen `JOURNAL.md` im Stand `481b9f7` (6 526 Zeilen,
letzter Block `BJ`).** Im Ordner `docs/projektfuehrung/nachtraege/` liegen
**elf** `JOURNAL_NACHTRAG_*.md` — nicht zehn, wie Abschnitt 0 des Auftrags
zählt: **`(20f)` ist um 16:50 aus TB-66 hinzugekommen.**

Zwei Muster, je Nachtrag beide angewandt:

- **Muster A** — die TB-Nummer aus dem Titel des Nachtrags in einer
  `## `-Kopfzeile des Journals (`grep -c "^## .*TB-NN[: ]"`).
- **Muster B** — zwei bis vier charakteristische Sätze aus dem Nachtrag, wörtlich
  im ganzen Journal (Whitespace und Blockquote-Präfix `> ` normalisiert, damit
  Zeilenumbrüche nicht trennen; Skript `docs/belege/TB-67/messung1.py`, Zählung mit `grep -c`
  gegengehalten).

| Nachtrag | TB im Titel | Muster A (Kopfzeilen, Block) | Muster B (wörtlicher Satz: Treffer) | Urteil |
|---|---|---|---|---|
| `(c)` 19.09. | TB-55 | **2** (BG, BH) | „die Sitzung, deren Ergebnis ein Nichthandeln ist": **1** · „Der Zug ist nicht wiederholbar; der Abbruch ist es": **1** | **eingearbeitet** — B trifft in **BG**, A bestätigt |
| `(d)` 19.09. | TB-55 | **2** (BG, BH) | „der Eingabezustand existiert": **1** · „1 Commit, 4 Trees, 1 Blob": **1** | **eingearbeitet** — B trifft in **BH**, A bestätigt |
| `(e)` 19.09. | TB-55b, TB-54 | **1** (BI), **1** (BJ) | „der Snapshot steht im Register": **1** · „acht Nachträge, eine Rückfrage": **1** | **eingearbeitet** — zwei Blöcke, **BI** und **BJ**, A und B treffen |
| `(f)` 19.09. | — *(keine im Titel)* | A nicht anwendbar; ersatzweise die TB-Nummern seiner drei Blocküberschriften: TB-53b **0**, TB-58 **0**, TB-58b **0** | „der Resolver erreicht die Selektionsseite": **0** · „Der Engpass war eine Datei, nicht 90 Module": **0** · „Codeherkunft und Lock": **0** · „Abschnitte 19 und 20": **0** | ⭐ **offen** — B ist anwendbar und trifft nicht (siehe Widerspruch unten) |
| `(g)` 19./20.09. | TB-59 | **0** | „Sichern ist keine Abgabe, sondern ein Schritt": **0** · „die Backlog-Einarbeitung": **0** | **offen** |
| `(20a)` | TB-60 | **0** | „Verschieben ist beweisbarer als Behalten": **0** · „das Backlog-Archiv": **0** | **offen** |
| `(20b)` | TB-61, TB-62 | **0**, **0** | „ZIP wird überall abgeschafft": **0** · „fünf Messfehler derselben Familie": **0** | **offen** |
| `(20c)` | TB-61 | **0** | „Der Krypto-Benchmark ist bis 2021 leer": **0** · „drei Befunde, die keiner bestellt hat": **0** | **offen** |
| `(20d)` | TB-65 | **0** | „Der Faktor ist nicht die Nachricht": **0** · „welche Schranke für den Benchmark gilt": **0** | **offen** |
| `(20e)` | TB-62 | **0** | „das Ende der ZIP-Pflicht": **0** · „die Nachträge (m) und (v)": **0** | **offen** |
| `(20f)` | TB-66 | **0** | „der Benchmark wird tagesgenau": **0** · „Ein Platzhalter im Register ist ehrlicher": **0** | **offen** — ⚠️ *im Auftrag nicht gezählt* |

**Zweite Zählung:** dieselben Kopfzeilen-Treffer mit `grep -c "^## .*TB-NN[: ]"`
(TB-55 → 2, TB-55b → 1, TB-54 → 1, alle übrigen → 0) und dieselben Sätze mit
`grep -c` auf Zeilenebene (die vier eingearbeiteten → je 1, die acht offenen → je
0). **Beide Zählungen stimmen überein.**

**Ergebnis: 3 eingearbeitet (4 Blöcke BG–BJ), 8 offen, 0 nicht prüfbar.**

### ⚠️ Widerspruch zum Auftrag: `(f)` ist offen, nicht „nicht prüfbar"

Der Auftrag stuft `(f)` als *nicht prüfbar (A2)* ein, weil sein Titel keine
TB-Nummer nennt. **Das gilt nur für Muster A.** Muster B — der wörtliche Satz —
ist auf `(f)` genauso anwendbar wie auf jeden anderen Nachtrag, und es liefert
mit vier verschiedenen Sätzen viermal 0. Zusätzlich tragen die drei
Blocküberschriften *in* `(f)` die Nummern TB-53b, TB-58 und TB-58b, und keine
davon steht in einer Journal-Kopfzeile. **`(f)` ist damit gemessen offen** —
*nicht prüfbar* wäre es nur, wenn beide Muster versagt hätten (Auftrag,
Schritt 1), und das tut keines.

### ⭐ Befund: `(f)` ist bereits die Journalfassung des Rückblick-Blocks aus `(m)`

Schritt 3 des Auftrags verlangt *„drei Journalblöcke für TB-53b, TB-58 und
TB-58b, aus den 20 Zeilen des Blocks `2s` in `BACKLOG_NACHTRAG_2026-09-19m.md`"*.
**Genau diese drei Blöcke enthält `(f)` schon** — als `## Block ⟨nächster⟩ —
TB-53b …`, `## Block ⟨danach⟩ — TB-58 …`, `## Block ⟨danach⟩ — TB-58b …`, mit
demselben Datum (19.09.2026, 19:48 Uhr Dateizeit, `(m)` ebenfalls 19:48) und
denselben Zahlen (71/19, 0 von 90, `96a5c572…`, N1/N3/N4, 44/44, 160/0). Die
`B`-Zeilen aus `(m)` stehen dort verkürzt als Tabelle *„Was der Nachmittag über
die Arbeitsweise ergab"*.

⇒ **Schritt 2 (Einarbeitung von `(f)`) und Schritt 3 (drei Blöcke aus `(m)`)
sind dieselben drei Blöcke.** Sie werden **einmal** angelegt, nicht zweimal.
Damit das Messprotokoll aus `(m)` (die 13 `T`-Zeilen) wörtlich im Journal steht
und nicht nur die Prosa aus `(f)`, bekommt jeder der drei Blöcke am Ende eine
Tabelle mit seinen `T`-Zeilen aus `(m)`, zeichengleich übernommen, und **zwei
Quellenzeilen** — `(f)` und `(m)`. Die sieben `B`-Zeilen werden, wie der Auftrag
verlangt, **nicht** als Regeln eingetragen, sondern in Nachweis 6 geprüft.

*Was `(f)` gegenüber den `T`-Zeilen nicht enthält, gezählt:* `T58.2` (Fables
drei Fälle) fehlt in `(f)` ganz; `T53.3` steht in `(f)` ohne die Zahlen 63 /
9/9 / 23 / 14. Beides ist der Grund, die `T`-Tabellen mitzunehmen.

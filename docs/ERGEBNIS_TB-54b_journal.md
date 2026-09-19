# Ergebnis TB-54b — Journal-Nachträge (c)–(e), Prüfprinzip A7, Backlog-Nachtrag (l)

**19.09.2026, MacBook (Darwin), `~/trading-bot`, Zweig `main`, Interpreter
`trading-env/bin/python3` = Python 3.9.6.** Basis `5a01e8b` → drei Commits
**`fade02c`** (Journal) → **`2c4a20b`** (Prüfprinzipien) → **`fef279c`**
(Backlog), alle gepusht; dazu dieser Bericht mit den vier Nachtragsdateien.
Auftrag: `~/Downloads/tb54b/MAC_TB-54b_journal_und_pruefprinzipien.md`.

**Kurz:** Alle drei Teile ausgeführt, kein Teilerfolg nötig. **468 Zeilen
hinzu, 0 entfernt** über drei Dateien. Nichts umnummeriert. Datenstand,
Snapshot, Datenbanken und Register unberührt.

---

## Schritt −1 — Ortsprüfung

| Prüfung | Soll | Ist |
|---|---|---|
| `uname -s` | `Darwin` | **`Darwin`** ✅ |
| `test -x trading-env/bin/python3` | vorhanden | vorhanden, **Python 3.9.6** ✅ |
| Arbeitsordner, Zweig | `~/trading-bot`, `main`, aktuell mit `origin` | `/Users/jaquelineloffler/trading-bot`, `main`, HEAD = `origin/main` = `5a01e8b` nach `git fetch` ✅ |
| `git status --short` | 0 Zeilen | **0** ✅ |

---

## Schritt 0 — Sichern und messen

**Sicherungsordner:** `/Users/jaquelineloffler/Sicherungen/tb54b_journal_20260919T080837Z/`
(Liste, Quersummen, Kopien, alle Prüfprotokolle vorher/nachher).

| | Soll | Ist |
|---|---|---|
| `*.db` ausserhalb `trading-env/` | 12, davon 9 `paper_trading_*` | **12**, davon **9** `paper_trading_*` in der Wurzel (plus die 0-Byte-Doppelgängerin `strategies/volatility_breakout/…`, macht 10 mit diesem Namensteil) ✅ — Kopien gegen `shasum -a 256 -c`: **12/12 OK** |
| Datenstand vorher (`--nur-hash`, 08:08:48 UTC) | `d9449faf…`, 223 | **`d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, 223** ✅ |
| `snapshot.py --pruefen snapshots/63e4b6c8…` | `UNVERAENDERT` | **`UNVERAENDERT`**, rc 0, Soll = Ist für beide Hashes ✅ |
| Registerprüfer vorher (`--basis a1e7fb4`), **08:08:59 UTC** | KEIN BEFUND | **KEIN BEFUND**, rc 0, `Quelle beleg: trockenlauf` ✅ — **vor** der ersten Änderung (erster Schreibzugriff 08:1x, erster Commit `fade02c` danach), nicht nachgeholt (A7) |

**Ausgangswerte (Zeilen / Bytes):** `JOURNAL.md` **6096 / 324 883** ·
`PRUEFPRINZIPIEN.md` **347 / 16 822** · `BACKLOG.md` **929 / 254 860**.

**Nachtragsdateien gegen `00_INHALT.txt`:** (c) 7764 ✅ · (d) 6362 ✅ ·
(e) 6504 ✅ · (l) 8080 ✅ — alle vier stimmen. **Kopien an anderen Orten
(gemeldet, nicht benutzt):** `~/Downloads/tb55_bewertung/JOURNAL_NACHTRAG_2026-09-19c.md`
(7764 B) und `~/Downloads/tb55final/JOURNAL_NACHTRAG_2026-09-19d.md` (6362 B) —
genau die in `00_INHALT.txt` genannten Herkunftsorte, gleiche Grösse.

---

## Teil A — Journal (430 / 0), Commit `fade02c`

### ⭐ Welcher Blockbuchstabe war der letzte — gemessen wie?

**BF.** Gemessen mit `grep -nE '^## [A-Z]{1,2} — '` über die ganze Datei
(nicht durch Blättern): 46 Treffer vor dem Einfügen, der mit der höchsten
Zeilennummer **und** der alphabetisch höchste ist
`5489:## BF — TB-49: das Werkzeug lernt die Ausnahme`. Nachtrag (c) hatte BF
als Erwartung genannt; die Messung bestätigt es. ⚠️ Mein erstes Muster
(`^#+ +Block `, nach dem Wortlaut der Nachträge) traf **null** Zeilen — die
Blöcke heissen im Dokument `## BF — …`, nicht `## Block BF — …` (Formentscheidung
aus TB-50). Ein Muster, das nichts trifft, ist kein Messergebnis (A1); erst das
zweite Muster war eines.

**Vorbelegung geprüft:** BG, BH, BI, BJ kamen weder als Überschrift noch als
Verweis (`BG.1`, `Block BG`) vor: 0 Treffer.

### ⚠️ Auf welcher Überschriftenebene stehen die Blöcke wirklich?

**`##` (Ebene 2)**, Unterabschnitte `###`. Die Nachträge schreiben ebenfalls
`## Block ⟨nächster⟩ — …`; übernommen wurde die Ebene des Dokuments und die
Form `## BG — …` ohne das Wort „Block", wie TB-50 es für BA–BF entschieden hat
(`ERGEBNIS_TB-50_dokumentationspflege.md`, Formentscheidung 2). Ausser dem
Buchstaben ist an keiner Überschrift etwas verändert; die `###`-Unterüberschriften
stehen wörtlich wie in den Nachträgen.

### Einfügestelle

Die Nachträge sagen „am Ende der Datei". Die Datei endet mit
`## Wiederkehrende Lehren` (Kopf: *„Am Ende: die wiederkehrenden Lehren."*),
und BA–BF wurden in TB-50 **vor** diesen Abschnitt gesetzt (dokumentierte
Formentscheidung 1). Die vier neuen Blöcke stehen deshalb ebenfalls am Ende des
chronologischen Teils, unmittelbar vor „Wiederkehrende Lehren". Nicht als
offene Frage behandelt, weil die Entscheidung bereits dokumentiert ist.

### Je Nachtrag: eingefügt / entfernt — zweifach gemessen

| Nachtrag | Block | Zeilen | kumulativ gegen `HEAD` | gegen Kopie des Standes davor |
|---|---|---|---|---|
| (c) | **BG** — TB-55: die Sitzung, deren Ergebnis ein Nichthandeln ist | Z. 5759 | **161 / 0** | **161 / 0** |
| (d) | **BH** — TB-55: der Eingabezustand existiert | Z. 5920 | **298 / 0** | **137 / 0** |
| (e) | **BI** — TB-55b: der Snapshot steht im Register · **BJ** — TB-54: acht Nachträge, eine Rückfrage | Z. 6057 / 6106 | **430 / 0** | **132 / 0** |

⚠️ **Nachtrag (e) enthält zwei Blöcke** („nächster" und „übernächster"); aus
drei Nachträgen wurden deshalb **vier** Blöcke BG–BJ. Die Abschnitte „Der Stand
am Ende des 19.09." und „In einfacher Sprache" am Ende von (e) gehören
strukturell zu BJ.

**Duplikatsprüfung:** je Nachtrag 4–5 kennzeichnende Zeichenfolgen gesucht
(z. B. *„deren Ergebnis ein Nichthandeln ist"*, *„1 Commit, 4 Trees, 1 Blob"*,
*„Wir wenden Register-Disziplin auf ein Arbeitsdokument an"*): **0 Treffer** vor
dem Einfügen — keiner war eingearbeitet. **Gegenprobe des Inhalts:** die 286
nichtleeren eingefügten Textzeilen (ohne Trenner) sind bis auf die vier
Überschriftszeilen byteidentisch mit den Quellen (`diff` leer).

**Vorgehen:** ein Skript je Nachtrag mit Anker `## Wiederkehrende Lehren`
(muss genau einmal vorkommen, Umgebung `---`/Leerzeile geprüft), Abbruch vor
dem Schreiben bei jeder Abweichung; kein Abbruch trat auf. `JOURNAL.md`
6096 → **6526** Zeilen.

---

## Teil B — Prüfprinzip A7 (16 / 0), Commit `2c4a20b`

### ⭐ War A7 schon vergeben?

**Nein.** `grep -nE '\bA7\b' docs/PRUEFPRINZIPIEN.md`: **0 Treffer**; auch
„nachgeholt", „Vorher-Messung", `7e48e1f` kamen nicht vor. Gruppe A endete mit
A6 (Z. 74). Keine Ausweichnummer nötig.

**Einfügestelle:** nach dem letzten Absatz von A6, **vor** dem Trennstrich
`---`, der `## B` vorausgeht — wie TB-50 es für A6 begründet hat (sonst stünde
das Prinzip optisch in Abschnitt B). Jetzt Z. 110–126, `## B` in Z. 128.

**Form:** Überschrift `### A7 — Eine nachgeholte Vorher-Messung` (Ebene und
Form der 25 vorhandenen Prinzipien; der Schlusspunkt aus dem Auftragstext
entfällt, weil keine Prinzip-Überschrift einen trägt). Der Körper (Regel,
Herkunft, Grenze) ist **wörtlich** der Auftragstext ohne die `>`-Zeichen —
per `diff` gegen den aus dem Auftrag extrahierten Text geprüft, Z. 2–13
identisch. Gegen `HEAD` und gegen die Kopie vorher: **16 / 0**.
`PRUEFPRINZIPIEN.md` 347 → **363** Zeilen.

---

## Teil C — Backlog-Nachtrag (l) (22 / 0), Commit `fef279c`

### Stehen die drei Vermerke, ohne dass etwas umnummeriert wurde?

**Ja.** Byteweiser Vergleich der betroffenen Originalzeilen gegen `HEAD~1`:
beide `| **V1** |`-Zeilen (Abschnitt 2, Z. 54; Block 2o, Z. 592) **identisch**,
`| **0,85c** |` **identisch**, `| **0,88** …` **identisch**. `numstat` **22 / 0**
gegen `HEAD` **und** gegen die Kopie vorher.

| Vermerk | Stelle | Wie ergänzt |
|---|---|---|
| 1 | `V1` in Abschnitt 2 **und** `V1` in Block 2o | je eine **neue Tabellenzeile direkt darunter**: `\| **V1** *(Vermerk 19.09.2026, Nachtrag (l))* \| ⚠️ *„Die \`V\`-Nummern in Block 2o stammen aus der Vorprüfung … keine wird geändert."* \|` — Text wörtlich aus dem Nachtrag |
| 2 | Kette `0,85c` | neue Zeile darunter: `\| **0,85c** *(Vermerk 19.09.2026, Nachtrag (l))* \| ⚠️ *„Die Aufgabennummer TB-54 wurde am 19.09.2026 … eine neue Nummer."* \| — \|` — keine neue Nummer erfunden |
| 3 | Kette `0,88` | **stand bereits wörtlich** in der Rang-Zelle (*„im Nachtrag (h) als 0,87 vergeben; 0,87 war bereits belegt — Betreiberentscheidung 19.09.2026: 0,88"*) — **nur bestätigt, nichts geändert** |

⚠️ **Eine Formentscheidung, offengelegt:** Ein Vermerk *in* der bestehenden
Zelle hätte die Zeile verändert (`numstat` 1 / 1) und damit „entfernte Zeilen:
0" verletzt. In einer Markdown-Tabelle ist die einzige hinzufügende Form eine
weitere Zeile; sie trägt dieselbe Nummer plus Klammerzusatz, in der Form, die
TB-54 mit `**0,84** *(alter Wortlaut — …)*` eingeführt hat. **Folge:** `grep
'^| **V1**'` zählt jetzt **4** Zeilen (2 Original + 2 Vermerk); wer V-Nummern
maschinell erhebt, muss den Klammerzusatz ausschliessen.

### ⭐ Die neue Kettenzeile: 0,86c — gemessen, nicht geraten

Der Nachtrag nennt bewusst keine Nummer („die nächste freie unterhalb von
0,86b"). Gemessen mit `grep -oE '^\| ~*\*\*0,86[a-z]?\*\*'`: **0,86** (3 Zeilen,
1 aktiv + 2 alte Wortlaute), **0,86a** (2), **0,86b** (1) — **0,86c** kommt weder
im Backlog noch sonst im Repo vor (0 Treffer). Vergeben: **`0,86c`**, eingefügt
**direkt unter 0,86b** (beide Lesarten von „unterhalb" fallen dort zusammen:
numerisch und in der Tabelle). Die Rang-Zelle trägt den Zusatz *(Nummer am
19.09.2026 in TB-54b gemessen und vergeben — Nachtrag (l) nannte bewusst
keine)*; Schritt- und Stand-Zelle wörtlich aus dem Nachtrag.

### Block 2r und K2i–K2k

* **Block 2r** (T54.1–T54.8, 8 Zeilen + Kopf + Tabellenkopf + Trenner = 15
  Zeilen) nach 2q, vor `## 3 — Die Kette`. ⚠️ Der Nachtrag schreibt `### 2r`;
  alle Nachbarn (2j–2q) stehen auf `##` — **die Ebene des Dokuments gewinnt**,
  jetzt `## 2r — TB-54: die acht Nachträge, und was dabei sichtbar wurde`
  (Z. 634). Tabellenzeilen wörtlich aus der Quelle gelesen, nicht abgetippt.
* **K2i, K2j, K2k** nach K2h am Ende von Abschnitt 4 (vorher K2a–K2h gemessen,
  K2i–k 0 Treffer). 3 Zeilen, wörtlich.

`BACKLOG.md` 929 → **951** Zeilen. Fünf Einfügungen, jede über einen Anker mit
Pflicht „genau einmal"; kein Abbruch.

---

## Schritt 3 — Einchecken

| # | Datei | `git status --short` vor dem Commit | Commit | Push |
|---|---|---|---|---|
| 1 | `docs/projektfuehrung/JOURNAL.md` | nur diese Datei (` M`) | `fade02c` | ✅ HEAD = origin/main |
| 2 | `docs/PRUEFPRINZIPIEN.md` | nur diese Datei | `2c4a20b` | ✅ |
| 3 | `docs/projektfuehrung/BACKLOG.md` | nur diese Datei | `fef279c` | ✅ |

`git status --short` nach jedem Push: **0 Zeilen**. Kein eigener Zweig, kein PR.
Gesamt `git diff --stat 5a01e8b fef279c`: **3 files changed, 468 insertions(+)**,
keine Löschung.

---

## Zum Schluss

| # | Prüfung | Ergebnis |
|---|---|---|
| 1 | Datenstand am Ende (08:18:11 UTC) | **`d9449faf51bf…a995f84`, 223** — gleich ✅ |
| 2 | Gesicherte `*.db` byteweise identisch | **12/12 OK** (`shasum -a 256 -c`), keine Abweichung ✅ |
| 3 | `snapshot.py --pruefen` am Ende | **`UNVERAENDERT`**, rc 0 ✅ |
| 4 | Registerprüfer nachher (`--basis a1e7fb4`, 08:18:29 UTC) | **KEIN BEFUND**, rc 0, `Quelle beleg: trockenlauf` ✅ |
| 5 | Nachtragsdateien ins Repo | **vier** Dateien nach `docs/projektfuehrung/nachtraege/`, je `cmp` identisch (7764 / 6362 / 6504 / 8080 B), `git check-ignore` rc 1 — ⚠️ **eine mehr als beauftragt:** auch (l), weil TB-54 die Backlog-Nachträge dorthin gelegt hat und *„ein Beleg in `~/Downloads` kein Beleg ist"* (T54.5); in diesem Commit |
| 6 | Dieses Dokument | `docs/ERGEBNIS_TB-54b_journal.md` |
| 7 | ZIP | `~/Downloads/TB-54b_journal.zip` |

**Unberührt:** `data/`, `snapshots/`, `shared/*`, Sperrliste,
`docs/VORREGISTRIERUNG_neuselektion.md` — `git diff --stat 5a01e8b HEAD` über
diese Pfade **leer**. Kein Netzabruf ausser `fetch`/`push`, keine Order, kein
Bot-Lauf, kein Basislauf, kein `cat` auf Konfigurationsdateien.

---

## Beobachtungen, die NICHT ausgeführt wurden

1. **Die Inhaltstabelle am Kopf von `JOURNAL.md`** (Z. 17 ff.) endet bei
   Block **AG**; AH–BJ fehlen dort. Nicht nachgetragen — kein Auftrag, und TB-50
   hat sie ebenfalls nicht fortgeschrieben.
2. **Der Kopf von `JOURNAL.md`** sagt *„rund 3 500 Zeilen"*; die Datei hat jetzt
   **6526**. Nicht geändert (Text unangetastet).
3. **`0,86c` (Kette sortieren) steht selbst in der unsortierten Kette** —
   numerisch zwischen 0,86b und 0,86a-alt, tabellarisch direkt unter 0,86b.
   Das ist genau der Zustand, den T54.7 beschreibt; die Betreiberentscheidung
   dazu ist offen.
4. **Der `0,86b`-Eintrag** nennt TB-54b als „Journal (c)–(e) und Prüfprinzip A7"
   und steht auf *„als nächstes, vor TB-53"*. TB-54b ist mit dieser Sitzung
   erledigt; die Zeile wurde **nicht** ersetzt (der Nachtrag (l) sieht es nicht
   vor, und eine Ersetzung hätte eine entfernte Zeile erzeugt).
5. **Die drei Journal-Nachtragsdateien tragen keinen Beleg-Kopf** („EINGEARBEITET
   als Block …") — bewusst, wie T54.8 es für die sieben aus TB-54 begründet
   (Grössen bleiben gegen `00_INHALT.txt` prüfbar). Die Zuordnung steht hier:
   (c) → BG, (d) → BH, (e) → BI + BJ, (l) → 2r / 0,86c / K2i–k.
6. **Mein Messmuster für den Blockbuchstaben** (`Block `) traf nichts — hätte
   ich den ersten leeren Treffer als „kein Block vorhanden" gelesen, wäre der
   nächste Buchstabe falsch geworden. Der Auftrag verlangte ein Muster auf die
   Überschriften; wie diese aussehen, war zuerst nachzusehen. Verallgemeinerbar
   als Nachtrag zu A1.
7. **`git rev-parse --short HEAD origin/main`** schlug erneut fehl (`--short`
   nimmt nur eine Revision) — derselbe Werkzeugfehler wie in T54.8, mit zwei
   Aufrufen nachgeprüft. Kein Befund am Repo.
8. **`0,85c` bleibt inhaltlich offen:** Der Vermerk sagt nur, dass das
   Lese-Audit eine neue Nummer bekommt; welche, vergibt die Sitzung, die es
   formuliert.

---

## In einfacher Sprache

**Was gemacht wurde:** Vier neue Tagebuchblöcke (BG bis BJ) stehen im Journal —
aus drei Nachträgen, weil der dritte zwei Blöcke enthielt. Die neue Prüfregel
A7 steht in den Prüfprinzipien; die Nummer war frei. Im Backlog gibt es den
Block 2r, drei kleine Regeln K2i–K2k, eine neue Aufgabe „Kette sortieren" mit
der gemessenen Nummer 0,86c und Hinweise an den drei Stellen, wo Nummern
doppelt vergeben sind.

**Was nicht passiert ist:** Keine Zeile wurde gelöscht oder umnummeriert —
468 Zeilen kamen hinzu, null gingen weg. Die Hinweise stehen als eigene Zeile
unter der betroffenen Stelle. Kursdaten, Snapshot, Datenbanken und das
Register sind unverändert, vorher und nachher geprüft.

**Die gefährlichste Stelle:** Der Buchstabe des letzten Tagebuchblocks wurde
gemessen und war BF. Mein erstes Suchmuster fand gar nichts, weil die
Überschriften anders aussehen als in den Nachträgen — das hätte man falsch
lesen können. Erst das zweite Muster, das zu den Überschriften passt, hat
gezählt. Genau davor warnte der Auftrag.

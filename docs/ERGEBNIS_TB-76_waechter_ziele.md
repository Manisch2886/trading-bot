# ERGEBNIS TB-76 — Der Wächter liest seine Zielmenge, statt sie aufzuzählen (Mac-Sitzung, 21.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-76_waechter_ziele.md`. **Ausgeführt am
MacBook**, Zweig `main`, Ausgang `437428d` (= `origin/main` beim Start, TB-63
erledigt), Interpreter `/usr/bin/python3` **3.9.6** — derselbe, den die
Cron-Zeile des Wächters aufruft. Geändert nur `system/` (Wächter, Selbsttest,
README) und `docs/` (dieses Dokument, Journalblock, Backlog-Zeile, zwei
Regeltexte, Belege). Sitzung ab 12:42 Ortszeit; Commits `6f5f986`
(Schritt 0), `bad7dc7` (Schritt 1), `cf22316` (Schritt 2+3), `bd3e559`
(Mutationsprobe und Schritt 4) und der Abgabe-Commit. Belege
`docs/belege/TB-76/`.

*In einfacher Sprache, zu Beginn:* Die Wache, die meldet, wenn eine Messnotiz
liegenbleibt, kannte ihre Zieldateien auswendig — zwei Namen im Code. Gestern
kam eine dritte Datei dazu, und die Wache meldete drei Notizen als verloren,
die längst angekommen waren. Jetzt liest sie im Backlog selbst nach, wohin
ausgelagert wurde. Die nächste ausgelagerte Datei kostet keine Codeänderung
mehr — und die Wache meldet heute wieder richtig: nichts offen, nichts
verloren, morgen früh um 04:50 zum ersten Mal automatisch.

---

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

Beim Sitzungsstart, 12:42, `HEAD` = `437428d`
(`docs/belege/TB-76/schritt0_status_vorher.txt`):

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
?? docs/auftraege/MAC_TB-76_waechter_ziele.md
```

Zwei Betreiber-Dateien, geschrieben 12:33 Ortszeit (mtime,
`schritt0_mtime.txt`), nach dem TB-63-Abschluss `437428d` (11:38): der
Auftrag und der Zeiger auf ihn (numstat 3/3). Secrets-Probe über Diff und
neue Datei (`api key`, `passwort`, `password`, `secret`, `token`): 0 Treffer.
**Schritt 0:** unverändert committet als **`6f5f986`**, gepusht. Danach
`git status --short` (`nachweis1_status_vor_schreiben.txt`): **eine Zeile**,
`?? docs/belege/TB-76/` — der Belegordner dieser Sitzung. Erst dann wurde
geschrieben.

⚠️ **Widerspruch zum Auftrag, Kopf und Abschnitt 0:** Der Auftrag sagt, die
Cron-Zeile sei *„seit dem 21.09., 10:50 eingetragen“*; der Backlog-Punkt `K4o`
und TB-63 sagen *„nicht eingetragen“*. Gemessen 12:42: `crontab -l` enthält
die Zeile (Zeile 41: `50 4 * * * cd ~/trading-bot && /usr/bin/python3
notifications/waechter_melden.py nachtraege >> logs/system/nachtraege.log
2>&1`), `logs/system/nachtraege.log` existiert noch nicht — **der Auftrag hat
recht, K4o ist überholt**; der erste automatische Lauf ist der 22.09., 04:50.

## Nachweis 2 — ⭐ Schritt 1: der Befund vor der Änderung

`/usr/bin/python3 system/nachtragswaechter.py` auf `6f5f986`, 12:44
(`schritt1_befund_vorher.txt`, vollständige Ausgabe samt rc):

| | gemessen |
|---|---|
| rc | **1** |
| Kopfzeile | `Ziel: BACKLOG.md 600 Zeilen, BACKLOG_ARCHIV.md 566, JOURNAL.md 7948 (23 Quellenzeilen)` — **`BACKLOG_EPICS.md` kommt nicht vor** |
| Zusammenfassung | `0x OFFEN UEBER DER FRIST, 0x offen in der Frist, 4x NICHT PRUEFBAR, 3x FALSCH VERSCHOBEN, 0x DOPPELBELEGUNG` |
| BEFUND | `3 falsch verschoben (B-09-19n, B-09-19o, B-09-19p)` |
| `(19n)` | Nummern 4, nicht angekommen 1: `Block 2t FEHLT — Nummer nicht im Ziel, Kern 'Epic AF: Autonome Strategie-Forschungspi' nirgends` |
| `(19o)` | Nummern 5, nicht angekommen 1: `Block 2u FEHLT — … Kern 'Epic MI: KI-Marktverständnis und adaptiv' nirgends` |
| `(19p)` | Nummern 5, nicht angekommen 1: `Block 2v FEHLT — … Kern 'Epic QR: Alpha-Discovery-Labor' nirgends` |
| die vier `[?]` | `19q`, `19q_r_berichtigung`, `19r`, `19u` — nicht prüfbar, keine Nummer der drei Formen |

**Deckt sich mit Abschnitt 0 des Auftrags** und mit
`docs/belege/TB-63/schritt4_waechter_befund.txt` — Nummern, Blöcke und
Begründung gleich; nur die Alterswerte sind eine Stunde grösser. Keine
Abweichung.

## Nachweis 3 — ⭐ Schritt 2: woran eine Zieldatei erkannt wird

**Gemessen vor der Entscheidung** (`schritt2_zielregel_messung.txt`, 12:46):

| Kandidat | gemessen | Urteil |
|---|---|---|
| **Namensmuster** `docs/projektfuehrung/BACKLOG*.md` | trifft **7** Dateien: `BACKLOG.md`, `_ARCHIV`, `_EPICS` **und vier alte Nachträge** `BACKLOG_NACHTRAG_2026-09-18{,b,c,d}.md` im Wurzelordner. Eine davon, `…-18.md` **ohne Buchstaben**, erkennt `RE_DATEINAME` des Wächters **nicht** als Nachtrag — sie trüge **9 K-, 3 Block- und 10 Kettennummern** ins Ziel, und ein Nachtrag prüfte sich selbst. `BACKLOG_*.md` ohne `_NACHTRAG_` träfe die richtigen zwei — aber eine fremde Datei mit passendem Namen würde **still** zum Ziel | ⛔ trifft heute Falsches; Fehler wäre leise |
| **Was `BACKLOG.md` selbst nennt** (`BACKLOG_*.md`, mit oder ohne Backticks — beide Zählungen gleich) | **`BACKLOG_ARCHIV.md` 34×, `BACKLOG_EPICS.md` 11×**, dazu einmal der Nachtrag `BACKLOG_NACHTRAG_2026-09-19m.md` (Abschlussvermerk). `BACKLOG_ARCHIV.md` steht seit TB-60 im Kopf (Zeile 7), `BACKLOG_EPICS.md` seit TB-63 in der Verweistabelle (Zeile 335 ff.) und in `K4o`. Alle anderen `*.md` in Backticks (`ARBEITSWEISE.md` 29×, `JOURNAL.md` 6× …) tragen nicht das Präfix | ⭐ **gewählt** |
| **Aufzählung, erweitert** | nicht gemessen — der Auftrag nennt sie als den Fehler, der wiederkommt | ⛔ |

**Die Regel, wie sie im Code steht** (`system/nachtragswaechter.py`,
`zieldateien()`, Docstring-Abschnitt *„Das Ziel wird GELESEN, nicht
aufgezählt“*):

> Zieldatei ist `BACKLOG.md` selbst und jede Datei `BACKLOG_<name>.md`, die
> `BACKLOG.md` mit blossem Dateinamen nennt (`RE_ZIELNENNUNG`, nicht als Pfad-
> oder Wortbestandteil), die neben `BACKLOG.md` liegt und keine Nachtragsdatei
> ist (kein `_NACHTRAG_` im Namen). Reihenfolge: `BACKLOG.md`, dann
> alphabetisch. Genannt, aber nicht vorhanden → **rc 2** (Werkzeugfehler, wie
> ein fehlendes Journal — der Verweis zeigt ins Leere).

**Begründung:** Wer aus dem Backlog auslagert, lässt dort einen Verweis zurück
— TB-60 (Kopf + Verweistabelle) und TB-63 (Verweistabelle) haben das beide
getan, und `DOKUMENTATIONSSTANDARD.md` Regel 9 verlangt es („nichts wird
gelöscht“). Das Backlog ist damit das Verzeichnis seiner eigenen
Auslagerungen. Beide Fehlerrichtungen sind **laut**: eine Datei, die existiert,
aber nicht genannt ist, ist kein Ziel → die dorthin verschobenen Nummern
werden „nicht angekommen“ (rc 1), und der Wächter zeigt damit auf den
fehlenden Verweis; eine genannte Datei, die fehlt, ist rc 2. Beim Namensmuster
wäre der Fehler in einer Richtung leise (falsches Grün).

⚠️ **Was der Weg beim nächsten Mal kostet:** Die nächste ausgelagerte Datei
muss `BACKLOG_<name>.md` heissen und in `BACKLOG.md` mit Namen stehen.
Beides tut eine Auslagerung nach dem bisherigen Muster ohnehin; **das Präfix
ist die eine Konvention, die bleibt** (eine Datei `EPICS.md` würde nicht
gefunden). Gelesen wird nur `BACKLOG.md`, nicht, was die ausgelagerten Dateien
ihrerseits nennen (`BACKLOG_EPICS.md` nennt `BACKLOG_ARCHIV.md` — ohne
Wirkung, weil das Backlog es selbst nennt). Die Kopfzeile jedes Laufs nennt
die gelesene Menge mit Zeilenzahlen, damit man sieht, was der Wächter für das
Ziel hält.

**Was sich NICHT geändert hat:** `Ziel.pruefe_nummer()` und
`Ziel.vergabevermerk()` — die dreistufige Ankunftsprüfung — sind zeichengleich
(`git diff cf22316~1 cf22316 -- system/nachtragswaechter.py` berührt sie
nicht; die Änderung liegt in `zieldateien()`, `Ziel.__init__`, Kopfzeile,
`main()` und Docstring: numstat 82/23). `Ziel.__init__` nimmt jetzt eine
Pfadliste statt `(backlog, archiv)`; `--archiv` und `STANDARD_ARCHIV`
entfallen, `waechter_melden.py` ruft ohne Argumente auf und ist unberührt.

## Nachweis 4 — ⭐⭐ Die drei Testfälle aus Schritt 3 (`schritt3_selbsttest.txt`)

`system/test_nachtragswaechter.py`, **82 bestanden, 0 fehlgeschlagen** auf
3.9.6 (vorher 62; die zwölf alten Fälle laufen unverändert, ihr
Wegwerf-Backlog nennt jetzt `BACKLOG_ARCHIV.md` im Kopf wie der echte).

| Fall | Aufbau (Wegwerf-Verzeichnis unter `$TMPDIR`) | Erwartung | Ergebnis |
|---|---|---|---|
| **13** | Nachtrag `(n)` mit Block `2t` unter `_eingearbeitet/`; `BACKLOG.md` nennt `BACKLOG_EPICS.md`, dort steht `## 2t — Epic AF …` | grün | **rc 0**, kein `FEHLT`; Kopfzeile `BACKLOG.md … BACKLOG_ARCHIV.md … BACKLOG_EPICS.md`, `zieldateien()` liefert die drei, nichts fehlt. Gegenprobe: `Ziel([backlog, archiv])` ohne EPICS → `2t` **FEHLT** (der alte Fehler, im Test festgehalten) — 5/5 |
| **14** | wie 13, aber `BACKLOG_EPICS.md` trägt nur `## 2u`, nicht `2t` | rot | **rc 1**, `Block 2t FEHLT`, `Kern 'Epic AF: …' nirgends`, EPICS war im Ziel (`BACKLOG_EPICS.md 5` in der Kopfzeile — dort wurde gesucht), BEFUND nennt `(B-09-01n)` — 5/5 |
| **15** | eine **weitere** Datei `BACKLOG_ZUKUNFT.md` — der Name kommt im Quelltext des Wächters **0×** vor (geprüft), und `BACKLOG_ARCHIV`/`BACKLOG_EPICS` kommen **nur im Docstring** vor, nicht im Code (per `ast`, Modul-Docstring abgezogen, Kommentare ausgenommen) | grün **ohne Codeänderung** | (1) Datei vorhanden, nicht genannt → **rc 1**, Kopfzeile nennt sie nicht; (2) `BACKLOG.md` nennt sie, ohne Backticks → **rc 0**, `BACKLOG_ZUKUNFT.md 5` in der Kopfzeile; (3) genannter Nachtrag `BACKLOG_NACHTRAG_…n.md` ist kein Ziel; (4) `alt/BACKLOG_ALT.md` und `XBACKLOG_X.md` sind keine Nennung; (5) genannt, aber fehlend → **rc 2**, stderr nennt die Datei — 10/10 |

## Nachweis 5 — Mutationsprobe (`schritt3_mutationen.txt`)

Je Mutation: Änderung an `system/nachtragswaechter.py`, Selbsttest, `git
checkout -- system/nachtragswaechter.py`, `git diff --numstat`. Stand
`cf22316`.

| Mutation | Meldung | zurückgenommen |
|---|---|---|
| **M1** genannte Dateien ignoriert (`for name in sorted(())`) | **73/9 rot** — Fall 13 (rc 0, Kopfzeile, `zieldateien()`), 14 („Datei war im Ziel“), 15 (rc 0 nach Nennung, rc 2 bei fehlender) | numstat leer |
| **M2** die alte feste Aufzählung `[backlog, BACKLOG_ARCHIV.md]` | **72/10 rot** — wie M1 plus *„ARCHIV/EPICS kommen im Code nicht vor“* | numstat leer |
| **M3** Nachtragsdateien nicht mehr ausgeschlossen | **81/1 rot** — *„genannter Nachtrag ist kein Ziel“* | numstat leer |
| **M4** Nennung nur mit Backticks | **80/2 rot** — Fall 15 (2), Nennung ohne Backticks | numstat leer |

Kontrolle nach allen vier: **82/0**, `git status --short` nur der Beleg.
Jede Mutation trifft mindestens eine Probe, die die zwölf alten Fälle nicht
hatten — die neuen Fälle beissen.

## Nachweis 6 — Schritt 4: rc 0 gegen den echten Bestand (`schritt4_lauf_echt.txt`, `.json`)

`/usr/bin/python3 system/nachtragswaechter.py --json …` auf `cf22316`, 12:52:

| | gemessen |
|---|---|
| rc | **0** — `Kein Befund: nichts liegt ueber der Frist, nichts ist falsch verschoben, keine Nummer doppelt.` |
| Kopfzeile | `Ziel (aus BACKLOG.md gelesen): BACKLOG.md 600, BACKLOG_ARCHIV.md 566, BACKLOG_EPICS.md 961 Zeilen; JOURNAL.md 7948 (23 Quellenzeilen)` |
| Zusammenfassung | `0x OFFEN UEBER DER FRIST, 0x offen in der Frist, 4x NICHT PRUEFBAR, 0x FALSCH VERSCHOBEN, 0x DOPPELBELEGUNG` |
| die vier `[?]` | `19q`, `19q_r_berichtigung`, `19r`, `19u` — **unverändert** |
| Vergleich mit Nachweis 2, zeilenweise (Alter ausgeblendet) | **genau drei Zeilen anders**: `19n`, `19o`, `19p` von `[!!] … nicht angekommen 1` auf `OK … nicht angekommen 0`. Sonst nichts — 34 Zeilen gleich |

Erwartung des Auftrags erfüllt: 0 offen, 0 falsch verschoben, 0 doppelt, die
vier `[?]` unverändert.

## Nachweis 7 — `git diff --numstat` je Datei, nichts ausserhalb `system/` und `docs/`

`git diff --numstat 437428d HEAD` (Abgabe-Commit eingeschlossen, siehe
`nachweis7_numstat.txt`):

| Datei | numstat |
|---|---|
| `system/nachtragswaechter.py` | 82 / 23 |
| `system/test_nachtragswaechter.py` | 123 / 9 |
| `system/README_NACHTRAGSWAECHTER.md` | 17 / 3 |
| `docs/…` | Auftrag und Zeiger (Betreiber, Schritt 0), dieses Dokument, Journalblock `CD`, Backlog-Zeile `K4p`, je eine Zeile in `DOKUMENTATIONSSTANDARD.md` 10 und `UEBERGABEPROTOKOLL.md` (Cron-Zeile ist eingetragen), Belege |

`git diff --name-only 437428d HEAD | grep -vE '^(system|docs)/'` → **0**.
Nichts in `research/`, `strategies/`, `shared/`, `notifications/`.

---

## Abweichungen vom Auftrag

| Stelle | Auftrag | gemessen / getan |
|---|---|---|
| Kopf, Abschnitt 0 | Cron-Zeile seit 10:50 eingetragen | **stimmt** (`crontab -l`, Zeile 41) — `K4o` und TB-63 sagten „nicht eingetragen“; `K4o` ist damit in diesem Punkt überholt, `UEBERGABEPROTOKOLL.md` (Zeile 562) nachgezogen |
| Schritt 2 und 3, je „Sichern“ | zwei Commits | **ein Commit `cf22316`** für beide: der Wächter ohne `--archiv` hätte die alten Tests mit `SystemExit` aus `argparse` abgebrochen — ein Zwischenstand mit rotem Selbsttest auf `main` wäre schlechter als ein Commit für beide Teile. Mutationsprobe und Schritt 4 danach getrennt (`bd3e559`) |
| Schritt 3, „eine Mutationsprobe“ | eine | **vier** — die Regel hat vier Teile (Nennung lesen, keine Aufzählung, Nachtrag ausschliessen, Backticks nicht verlangen), jeder wird einzeln getroffen |
| Abschnitt 1, „nur `system/`“ | Kurzzeile im Zeiger | Schritt 5 des Auftrags selbst verlangt `docs/`; dazu zwei Einzeiler in Regeltexten (Nachweis 7) |
| `K4o`, „`README_NACHTRAGSWAECHTER.md` und `DOKUMENTATIONSSTANDARD.md` 10 nachziehen“ | Einzeiler `--epics` | Zielregel statt Einzeiler (Schritt 2 des Auftrags); README und Standard nachgezogen |

## Fehler → Regel

| Fehler | Regel |
|---|---|
| Der erste Beleg der Mutationsprobe zeigte statt der Zählzeile die Zeile `FEHLGESCHLAGEN: …` — `tail -1` traf die letzte Zeile, und die ist bei rotem Lauf nicht die Zählung | ⭐ **Eine Zählzeile wird über ihr Muster gegriffen (`bestanden,`), nicht über ihre Position** — dieselbe Klasse wie TB-63 (`split` vs. `splitlines`): das Instrument, nicht der Bestand. Beleg neu erzeugt, alter überschrieben |
| Die erste Fassung der Probe *„ARCHIV/EPICS nur im Docstring“* war ein dreifach verschachtelter Ausdruck, den niemand lesen konnte | ⭐ **Eine Probe, die man nicht lesen kann, kann auch nicht falsch sein — sie kann nur nicht auffallen.** Ersetzt durch `ast`: Modul-Docstring abziehen, Kommentare ausnehmen, dann suchen |

## ⚠️ Offen — nicht Teil dieses Auftrags

| | |
|---|---|
| **1** | `notifications/README_WAECHTER_MELDEN.md` (Zeile 188) sagt weiter „ebenfalls nicht eingetragen“ zur Cron-Zeile — liegt ausserhalb `system/` und `docs/`, nicht angefasst |
| **2** | Der erste automatische Lauf **22.09.2026, 04:50** — erwartet rc 0, keine Telegram-Meldung, eine Zeile in `logs/system/nachtraege.log`. **Das ist die eigentliche Probe dieser Aufgabe und liegt in der Zukunft** |
| **3** | Die Lücke aus TB-75 bleibt: für Mac-Journalblöcke gibt es keine Wache (*„Ergebnisdokument ohne Quellenzeile“* ist nicht gebaut) |
| **4** | Der Kopf von `BACKLOG.md` nennt `BACKLOG_EPICS.md` weiter nicht (TB-63, Offen 1) — für den Wächter reicht die Verweistabelle, für eine neue Sitzung nicht |

---

## In einfacher Sprache

**Was schiefstand:** Die Wache für liegengebliebene Notizen kannte zwei
Zieldateien auswendig. Seit gestern gibt es eine dritte, und die Wache meldete
drei Notizen als verloren, die dort längst angekommen waren. Ab morgen früh
läuft sie automatisch — eine Wache, die jeden Tag dasselbe Falsche sagt, wird
nach einer Woche überlesen.

**Was jetzt gilt:** Die Wache liest im Backlog selbst nach, wohin etwas
ausgelagert wurde — das Backlog sagt es an jeder Stelle, an der ausgelagert
wurde. Drei Proben zeigen, dass das trägt: angekommen in der neuen Datei ist
grün, nirgends angekommen ist rot, und eine vierte Datei, deren Namen der
Code nie gesehen hat, ist grün, ohne dass jemand den Code anfasst. Vier
absichtliche Beschädigungen der Regel machten die Proben rot.

**Was das für dich heisst:** Der Lauf um 04:50 wird morgen keine Meldung
schicken — das ist richtig so. Die nächste ausgelagerte Datei muss nur
`BACKLOG_<name>.md` heissen und im Backlog genannt sein; beides passiert beim
Auslagern sowieso.

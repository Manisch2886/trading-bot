# ERGEBNIS TB-58b — Die Registereinträge zu Codeherkunft und Lock (Mac-Lauf, 19.09.2026)

**Auftrag:** `logs/auftraege/TB-58b_v2.md` (Fassung v2; jetzt versioniert als
`docs/auftraege/TB-58b.md`). **Ausgeführt am MacBook**, Zweig `main`, Ausgang
`6236c95`, Ergebnis **`409d71d`** (Register) und **`be6e72c`** (Belege und
Aufträge), beide gepusht. Interpreter durchgehend `trading-env/bin/python3` =
**Python 3.9.6**. Kein eigener Zweig, kein PR, keine ZIP.

**Kurzfassung:** Das Register `docs/VORREGISTRIERUNG_neuselektion.md` hat zwei
neue Abschnitte — **19** (Registertext 5e, Ergänzung Codeherkunft; nach F17
eine **Entscheidung**) und **20** (Tatsachennotiz zu Registertext 5f, der
Lock). **160 Zeilen hinzugefügt, 0 entfernt.** Fables Wortlaut steht
zeichengleich darin, die fünf Platzhalter sind mit selbst gemessenen Werten
gefüllt. Ein Lauf unter dem Selektionsmodus mit absichtlich abweichendem Lock
bricht mit **rc 2** ab — gemessen vor und nach dem Commit. Datenstand, zwölf
Datenbanken und Snapshot sind vorher und nachher identisch; der Registerprüfer
meldet dreimal **KEIN BEFUND**. Keine Rückfrage war nötig.

---

## Die sechs Fragen des Auftrags, beantwortet

| Frage | Antwort |
|---|---|
| ⭐ **Welche Abschnittsnummern wurden vergeben, und wie gemessen?** | **19** und **20**. Gemessen: `grep "^## [0-9]"` über das Register, Nummer per `sed` herausgelöst, `sort -n \| tail -1` → **18** (19 nummerierte `##`-Überschriften, 0 bis 18; „19." und „Abschnitt 19/20" kamen nirgends vor). Die Gegenprüfung des Auftrags („nach TB-55b war es 18") stimmt mit der Messung überein. Zwei Abschnitte statt einem, weil die beiden Einträge nach F17 **verschiedener Art** sind (Entscheidung / Tatsachennotiz) und Abschnitt 18 — die Vorlage — je Notiz ein eigener `##`-Abschnitt ist |
| ⭐⭐ **SHA-256 der `requirements.lock`, selbst gerechnet?** | **`96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5`** — zweimal unabhängig: `shasum -a 256` und `hashlib.sha256` unter `trading-env/bin/python3`; derselbe Wert steht in der Auditzeile `lock_sha256` der Kontrollläufe. Dazu gemessen: 83 Zeilen, **67** Paketzeilen, 0 ohne `==`, gegen `importlib.metadata` **0 Abweichungen**; `pandas==2.3.3`, `pandas-market-calendars==4.6.1` (= Tatsachennotiz in 17.5); Kopf `3.9.6 (default, Apr 30 2025, 02:07:18) [Clang 17.0.0 (clang-1700.0.13.5)]`, `macOS-15.7.9-x86_64-i386-64bit`; Commit `d852bce637ba82ddb60330a7219c6e36a40539c3` (einziger Commit der Datei, auf `origin/main`); Blob im Arbeitsbaum = Blob unter `HEAD` (`863197fb…`) |
| ⚠️ **Gab es schon einen Abschnitt zu Codeherkunft oder Lock?** | **Nein.** 23 Zeichenfolgen geprüft (u. a. `Codeherkunft`, `Git-Wurzel`, `Arbeitsbaum`, `Wegwerfbaum`, `Einstiegspunkt`, `TB_SELEKTIONSCOMMIT`, `TB-58`, `96a5c572`, `d852bce`, `6518e41`, `lock_sha256`, `Startprüfung`): alle 0 Treffer. `requirements.lock` 2 Treffer, beide **Regeltext ohne Hash** (17.5 = Registertext 5f, „dessen Hash im Register steht" — er stand nirgends; 17.10 Zeile 4 = Befund „kein `requirements.lock`", Stand 18.09.). Kein Abschnitt hält dasselbe fest → nicht verdoppelt, ergänzt |
| **`numstat`: entfernte Zeilen wirklich 0?** | **Ja.** `git diff --numstat` vor dem Commit `160 0`; `git diff HEAD~1 HEAD --numstat` nach dem Commit `160 0`; `grep -c "^-[^-]"` auf dem Diff 0; der Diff besteht aus **einem** Hunk `@@ -2633,0 +2634,160 @@` am Dateiende. Registerprüfer (`null_entfernte_zeilen`, Basis `a1e7fb4`): `728 0` |
| ⭐ **Bricht ein Lauf mit abweichendem Lock wirklich mit rc 2 ab?** | **Ja**, siehe „Die Probe" unten: `pandas==0.0.1` committet, Baum sauber → **rc 2**, Meldung „1 Abweichung/en … pandas: Lock 0.0.1, installiert 2.3.3"; Kontrolle mit unverändertem Lock rc 0. Gemessen gegen `6236c95` **vor** dem Eintrag und gegen `409d71d` **nach** dem Commit, beide Male gleich |
| **Beobachtungen, die NICHT ausgeführt wurden?** | zehn, unten |

---

## Schritt −1 — Ortsprüfung (17:26 UTC)

| Prüfung | Soll | Ist |
|---|---|---|
| `uname -s` | `Darwin` | **`Darwin`** ✅ |
| `test -x trading-env/bin/python3` | 3.9.x | **3.9.6** ✅ |
| Arbeitsordner, Zweig | `~/trading-bot`, `main`, aktuell | `/Users/jaquelineloffler/trading-bot`, `main`, nach `git fetch`: `HEAD` = `origin/main` = `6236c95` ✅ |
| `git status --short` | 0 Zeilen | **0** ✅ |
| ⚠️⚠️ TB-58 ist durch | `requirements.lock` versioniert, Startprüfungen in `shared/paths.py` | `requirements.lock` 2109 B in der Wurzel, `git log` nennt `d852bce`; `shared/paths.py` trägt `startpruefung()`, `audit_zeilen()`, `TB_SELEKTIONSCOMMIT`, `_startpruefungen` (Zeilen 51, 156, 182, 500, 534, 544, 583) ✅ — **kein Abbruchgrund** |

Vorher gelesen: `docs/UEBERGABEPROTOKOLL.md` (Abschnitte 7–10), das Register
(17.4, 17.5, 17.10, 17.11, 18), `docs/ERGEBNIS_TB-58_startpruefungen.md`,
`shared/paths.py` (Kopf, `_pruefe_codeherkunft`, `_lies_lock`, `_pruefe_lock`,
`_startpruefungen`, der `else`-Zweig), F17 im Backlog-Nachtrag (g),
`docs/PRUEFPRINZIPIEN.md` (A1, A2, A7, D5, D6).

## Schritt 0 — Sichern und messen

**Sicherungsordner:** `~/Sicherungen/tb58b_registereintraege_20260919T172832Z/`
(Liste, Quersummen, Kopien, alle Messprotokolle — die Protokolle liegen auch
unter `docs/belege/TB-58b/`).

| | Soll | Ist |
|---|---|---|
| `*.db` ausserhalb `trading-env/` | Quersummen + Kopie, gezählt | **12** (11 in der Wurzel, dazu `strategies/volatility_breakout/paper_trading_volatility_breakout.db`); Kopien gegen `shasum -a 256 -c`: **12/12 OK** ✅ |
| Datenstand vorher (`--nur-hash`, 17:28:39 UTC) | `d9449faf…`, 223 | **`d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, 223** ✅ |
| Snapshot `--pruefen` | `UNVERAENDERT` | **`UNVERAENDERT`**, rc 0 ✅ |
| Registerprüfer VORHER (`--basis a1e7fb4`, 17:28:47 UTC) | KEIN BEFUND, vor jeder Änderung (A7) | **KEIN BEFUND**, rc 0; numstat `568 0` ✅ — der Commit kam um 17:37 UTC |
| `requirements.lock` | SHA-256 selbst, Pakete gezählt, `pandas` gelesen | siehe Kurzfassung ✅ |

## Schritt 1 — Wohin, gemessen

1. **Höchste Nummer 18** (Messung oben). Dateiende: Abschnitt 18 endet mit
   dem Vermerk *„Nachgetragen in TB-55b …"* und einem Zeilenumbruch
   (`tail -c 1` = `0a`), 2633 Zeilen.
2. **Duplikatprüfung:** kein Treffer, siehe Kurzfassung.
3. **Form von Abschnitt 18 übernommen:** Überschrift `## N. <Art> zu
   Registertext X — <Gegenstand> (TB, Datum)`, Einleitungsabsatz „Datiert
   angehängt. Nichts entfernt …", Blockzitat des Registertexts, Tabelle der
   Messwerte, nummerierte „Punkte, die diese Tabelle tragen", Absatz „Was
   diese Notiz nicht tut", kursiver Schlussvermerk.

## Schritt 2 — Die beiden Einträge

**Abschnitt 19** (Zeile 2637): Registertext 5e, Ergänzung Codeherkunft —
Fables Wortlaut (A) als Blockzitat, **zeichengleich** mit dem Auftrag
(maschinell: `skripte/wortlaut_vergleich.py`, `A woertlich gleich: True`).
Dazu, ausserhalb des Zitats: die F17-Einordnung (Entscheidung, vor dem Tag,
Begründung ohne Ergebnis, keine Wirkung auf die Zulassung eines Bots), eine
Tabelle „Satz des Registertexts → Umsetzung → Gemessen" (sechs Zeilen, alle
Messwerte aus TB-58), drei tragende Punkte und der Absatz „Was diese
Ergänzung nicht tut". ⚠️ Punkt 2 benennt ausdrücklich, dass der **Lese-Audit
als Ganzes (5e) weiterhin nicht gebaut ist** (17.10, Zeile 3 gilt fort) — der
Registertext beschreibt zum Teil etwas, das der Code noch nicht kann, und das
steht da, statt verschwiegen zu werden.

**Abschnitt 20** (Zeile 2716): Tatsachennotiz zu Registertext 5f — Fables
Wortlaut (B) als Blockzitat, die fünf Platzhalter ⟨⟩ gefüllt (Commit, SHA-256,
Paketzahl, Interpreter, Plattform); alle festen Textsegmente in Reihenfolge
vorhanden (maschinell, 6 Segmente / 5 Platzhalter). Dazu die Messtabelle, die
Probentabelle (fünf Zustände) und drei tragende Punkte — darunter der eine,
der die Kette der Zusicherung genau benennt: **geprüft wird die Umgebung gegen
die Datei, nicht die Datei gegen den Registereintrag**; der SHA-256 der Datei
steht in der Auditzeile `lock_sha256`, und ein anderer Lock wäre ein anderer
Commit (Abschnitt 19, Bedingung 2).

**Eine Entscheidung innerhalb des Wortlauts, benannt:** zwei `##`-Abschnitte
statt eines Abschnitts mit zwei Unterabschnitten. Grund: verschiedene
F17-Kategorien, und die Vorlage (18) ist je Notiz ein Abschnitt. Der Auftrag
fragt nach „Abschnittsnummern" in der Mehrzahl; ein Widerspruch zwischen
Wortlaut und Zweck lag nicht vor, also keine Rückfrage.

## Schritt 3 — Einchecken

| | Soll | Ist |
|---|---|---|
| `git status --short` | nur das Register | `M docs/VORREGISTRIERUNG_neuselektion.md`, 1 Zeile ✅ |
| `git diff --numstat` | entfernte Zeilen 0 | **`160 0`** ✅ |
| Registerprüfer auf dem Arbeitsbaum | KEIN BEFUND | **KEIN BEFUND**, numstat `728 0` ✅ |
| `add` + `commit` + `push` in einem Zug | — | **`409d71d`**, 17:37:20 UTC; `HEAD` = `origin/main`; `git status` danach **0** ✅ |

Zweiter Commit (Punkt 7 und 8): **`be6e72c`**, 48 Dateien, +5847 / −0,
17:42 UTC, gepusht, `git status` danach 0. Dieses Dokument folgt als dritter.

## Die Probe — ein Lauf mit absichtlich abweichendem Lock

**Aufbau** (`docs/belege/TB-58b/skripte/probe_lock.sh`): `git clone` des Repos
in einen **Wegwerf-Klon** im Sitzungs-Scratchpad (kein Objekt, kein Worktree,
keine Datei im Arbeitsbaum von `~/trading-bot`), Interpreter
`trading-env/bin/python3` des Hauptrepos, `TB_SELEKTIONSWURZEL` = der Snapshot
`63e4b6c8…` **im Klon**, `TB_SELEKTIONSHASH` = `63e4b6c8…`,
`TB_SELEKTIONSCOMMIT` = jeweils `HEAD` des Klons, Einstiegspunkt eine
committete `probe.py` in der Klonwurzel (`import paths`, Ausgabe von
`DATA_DIR` und `startpruefung()["lock_sha256"]`). Der Klon wird am Ende
entfernt; `git worktree list` im Hauptrepo zeigt danach 1 Eintrag, `git
status` 0.

| # | Zustand im Klon | rc | Meldung (gekürzt) |
|---|---|---|---|
| 0 | Lock unverändert (Kontrolle) | **0** | acht Auditzeilen; `lock_sha256 96a5c572…`; `DATA_DIR` = Snapshot |
| 1 | `pandas==2.3.3` → `pandas==0.0.1`, **committet**, Baum sauber (SHA-256 des falschen Locks `2d19644b…`) | **2** | `STARTPRUEFUNG VERLETZT - Die Umgebung weicht von …/requirements.lock ab (1 Abweichung/en, die ersten drei: pandas: Lock 0.0.1, installiert 2.3.3). Hier wird nichts installiert und nichts repariert - der Lauf bricht ab.` |
| 2 | dieselbe Verfälschung, **nicht** committet | **2** | `Der Arbeitsbaum … ist ueber shared, strategies, requirements.lock nicht sauber (1 Eintrag/Eintraege, die ersten:  M requirements.lock)` — Bedingung 3 greift **vor** der Lock-Prüfung |
| 3 | Lock gelöscht und committet | **2** | `requirements.lock fehlt. Ohne Lock ist die Umgebung nicht pruefbar - und \`nicht pruefbar\` ist nicht gruen.` |
| 4 | Lock richtig, Interpreter `/usr/bin/python3` | **2** | `24 Abweichung/en, die ersten drei: aiohappyeyeballs: Lock 2.6.1, installiert NICHT \| aiohttp … \| aiosignal …` |

Zweimal gelaufen, identisches Ergebnis: **17:33 UTC gegen `6236c95`** (vor
dem Registereintrag — damit der Eintrag nur behauptet, was schon gemessen war)
und **17:37 UTC gegen `409d71d`** (nach dem Commit, wie der Auftrag es
verlangt). Protokolle: `probe_lock_vorher.txt`, `probe_lock_nachher.txt`.

⚠️ **Der erste Entwurf des Probeskripts war falsch gebaut** — benannt, nicht
still berichtigt: `git revert -q` gibt es nicht, der Revert lief nicht, und die
Proben 2 und 4 massen dadurch denselben Zustand wie Probe 1 bzw. 3 (rc 2 aus
dem falschen Grund). Probe 1 (die geforderte) und Probe 3 waren davon nicht
betroffen. Korrigiert auf `git revert --no-edit HEAD`, beide Läufe oben sind
mit der korrigierten Fassung gemessen; die versionierte `probe_lock.sh` ist
die korrigierte.

## Zum Schluss

| | Soll | Ist |
|---|---|---|
| 1 | Datenstand am Ende | **`d9449faf…`/223** ✅ (17:37:59 UTC) |
| 2 | Jede gesicherte `*.db` byteweise identisch | **12 von 12** (`shasum -a 256 -c` 12 OK, dazu `cmp` je Datei 12 identisch) ✅ — im Fenster 17:28–17:40 UTC liefen laut Crontab nur `*/5` (`warteauftraege_ausfuehren`) und `*/15` (`schliess_benachrichtigung`), keine Datenbank hat sich verändert; der 4-h-Cron (18:00/18:05 UTC) lag nach der Messung |
| 3 | Snapshot `--pruefen` | **UNVERAENDERT**, rc 0 ✅ |
| 4 | Registerprüfer nachher | **KEIN BEFUND**, rc 0, numstat `728 0` ✅ (17:39 UTC, nach dem Commit) |
| 5 | Probe mit abweichendem Lock → rc 2 | **rc 2** ✅ (Tabelle oben) |
| 6 | dieses Dokument | `docs/ERGEBNIS_TB-58b_registereintraege.md`, endet mit „In einfacher Sprache" |
| 7 | keine ZIP; Belege und Auftrag ins Repo | **`docs/belege/TB-58b/`** (14 Protokolle, 4 Skripte, `HERKUNFT.md`), **`docs/auftraege/TB-58b.md`** = `logs/auftraege/TB-58b_v2.md` byteweise (`cp -p`) ✅ — Commit `be6e72c` |
| 8 | TB-58 nachholen | **`docs/belege/TB-58/`**: 25 Dateien aus `~/Downloads/TB-58_startpruefungen.zip` (SHA-256 `3dd53a96…`, 33 Dateien); **8 weggelassen, weil byteweise identisch mit versionierten Ständen** (je `cmp`: ERGEBNIS, `requirements.lock`, `entwurf/paths_neu.py` = `shared/paths.py`, `entwurf/test_startpruefungen.py` = `shared/…`, `paths_alt`/`test_paths_alt`/`test_strategy_paths_alt` = `624853b:shared/…`, `auftrag_TB-58.md` = `logs/auftraege/TB-58.md`); Liste und Begründung in `HERKUNFT.md`. **`docs/auftraege/TB-58.md`** = `logs/auftraege/TB-58.md` byteweise ✅ — Commit `be6e72c`. ⚠️ `~/Downloads` war in dieser Sitzung **lesbar** (anders als in TB-58 vermerkt) |

**Nachgesehen, weil TB-58 es als offen benannt hatte:** die Datenbankkopien
der TB-58-Sitzung (`db/` im Sicherungsordner) sind **nicht** ins Repo gekommen —
Sicherung, kein Beleg. Secret-Suche über alle übernommenen Dateien
(`grep -r -i -l -E "api_key|secret|passw|token|BINANCE_API"`): ein Treffer,
das Wort „Secrets" in der Regelzeile des TB-58-Auftrags.

## Beobachtungen, die NICHT ausgeführt wurden

1. ⚠️ **17.10, Zeilen 3 und 4 beschreiben den Stand vom 18.09.** Zeile 4
   („kein `requirements.lock`") ist seit `d852bce`/`6518e41` geschlossen,
   Zeile 3 (Lese-Audit) offen. Nach Regel 1 („NUR HINZUGEFÜGT") **nicht
   umgeschrieben**; die Abschnitte 19 und 20 sagen es an ihrer Stelle.
2. **17.5 nennt die Python-Fassung als „3.9.6"**, der Lock die volle
   `sys.version`-Zeile. Kein Widerspruch — die Notiz 20 trägt die volle
   Zeile, 17.5 bleibt.
3. **Der Lese-Audit (5e) ist als Ganzes nicht gebaut** — heute gibt es die
   acht Startzeilen; wer den Audit baut, übernimmt sie über
   `paths.audit_zeilen()`. In 19 benannt, nicht angefasst.
4. `research/resolver_selektion/kindprozess.py` misst weiter mit `python -c`
   unter dem Modus (TB-58, Beobachtung 1) — unter dem Modus jetzt rc 2, nicht
   Teil des Basislaufs, `research/` nicht freigegeben. Unverändert.
5. **Die Probe hat den Klon per `git clone` gebaut, nicht per `git worktree`.**
   Ein Worktree hätte die Probe-Commits als Objekte im Hauptrepo hinterlassen;
   der Klon hinterlässt nichts. `git count-objects` im Hauptrepo wurde deshalb
   nicht gemessen.
6. **`logs/auftraege/TB-58b.md` (v1) liegt neben v2.** Einziger Unterschied
   (`diff`): Punkt 7 verlangte in v1 eine ZIP nach `~/Downloads`; v2 ersetzt
   das durch Punkt 7 (mitcommitten) und Punkt 8 (TB-58 nachholen). v1 wurde
   nicht ausgeführt und nicht kopiert.
7. Der Auftrag nennt das Muster „`git diff --numstat` — entfernte Zeilen: 0".
   Der Registerprüfer prüft dasselbe gegen `a1e7fb4` (`null_entfernte_zeilen`)
   — beide Wege wurden gegangen, beide 0. Ein Prüfer, der `--basis` nicht
   bekommt, nähme `merge-base HEAD origin/main` = `HEAD` und meldete einen
   leeren Vergleich als Befund (TB-50-Gedächtnis); deshalb `--basis a1e7fb4`.
8. **`docs/belege/` und `docs/auftraege/` sind mit dieser Sitzung neu** —
   vorher gab es keinen der beiden Ordner im Repo (`git ls-files` leer,
   `git check-ignore` rc 1). Die Backlog-Nachträge liegen weiter unter
   `docs/projektfuehrung/nachtraege/`; ob die beiden neuen Ordner ein Muster
   für alle künftigen Sitzungen sind, ist eine Entscheidung des Betreibers.
9. Die Auditzeilen nennen die Codewurzel als absoluten Pfad — im Klon also
   den Scratchpad-Pfad. Für den Vergleich zweier Läufe auf zwei Maschinen
   (17.5, Reproduktionstest) ist `commit` die tragende Zeile, nicht
   `codewurzel`. Beobachtung, keine Änderung.
10. Zwischen 17:28 und 17:45 UTC lief kein Bot-Cron (der stündliche
    `elliott_wave` liegt auf `0 * * * *` = 17:00 und 18:00 UTC). Die
    DB-Gleichheit ist damit **nicht** gegen einen Bot-Lauf gemessen, sondern
    nur gegen die 5-/15-Minuten-Dienste — das ist der Fall, der eintrat, nicht
    ein stärkerer Nachweis.

## Was ausdrücklich NICHT passiert ist

| | |
|---|---|
| ✅ | **Kein bestehender Registertext umgeschrieben** — ein Hunk am Dateiende, 0 entfernte Zeilen, drei Wege gemessen |
| ✅ | `data/` (223, `d9449faf…`), `snapshots/` (UNVERAENDERT), jede `*.db` (12/12), Sperrliste, `shared/*` **unberührt** — ausser dem Register hat diese Aufgabe im Arbeitsbaum nur die neuen Ordner `docs/belege/`, `docs/auftraege/` und dieses Dokument angelegt |
| ✅ | Keine Zahl abgeschrieben: SHA-256 zweimal gerechnet, Paketzahl gezählt, Kopfzeilen gelesen, Commit aus `git log`, Abschnittsnummer aus den Überschriften |
| ✅ | Kein Netzabruf ausser `git fetch`/`push` (der `git clone` war lokal), keine Order, **kein Bot-Lauf**, kein `pip install`, kein `--ziehen` |
| ✅ | Kein `cat` auf Konfigurationsdateien; die Crontab nur nach Zeitfeldern gefiltert ausgegeben |
| ✅ | Keine Rückfrage — Wortlaut und Zweck fielen an keiner Stelle auseinander |
| ✅ | Keine ZIP |

---

## In einfacher Sprache

**Was gemacht wurde.** Das Regelwerk der Neuselektion hat zwei neue Einträge
bekommen, beide nur angehängt, nichts Altes verändert. Der erste sagt: Der
Auswahllauf muss beim Start beweisen, aus welchem Verzeichnis sein Programmcode
stammt, dass dieser Code genau der festgehaltene Stand ist und dass dort nichts
Unfertiges herumliegt — sonst bricht er ab. Der zweite hält fest, welche
Programmbibliotheken in welcher genauen Fassung installiert waren, mit einer
Prüfsumme, die diese Sitzung selbst gerechnet hat.

**Wie geprüft wurde, dass der Text stimmt.** Nicht mit Vertrauen, sondern mit
einem Lauf, der absichtlich falsch aufgesetzt war: in einer Wegwerfkopie des
Projekts wurde eine Zeile der Bibliotheksliste verfälscht. Der Lauf hat das
gemerkt, die Zeile beim Namen genannt und mit dem Fehlercode abgebrochen, den
der Regeltext verspricht. Dasselbe passierte bei einer fehlenden Liste, bei
einem unaufgeräumten Verzeichnis und bei einem fremden Python. Mit der
richtigen Liste lief er durch. Das wurde zweimal gemessen: bevor der Eintrag
geschrieben wurde und nachdem er eingecheckt war.

**Was dabei aufgefallen ist.** Mein erstes Prüfskript hatte einen Tippfehler in
einem Git-Befehl, wodurch zwei von fünf Proben dasselbe massen wie ihre
Nachbarn. Das ist benannt und korrigiert, nicht still ausgebessert. Und: die
Belege der Vorgängersitzung lagen bisher nur als ZIP im Download-Ordner —
jetzt liegen sie im Repo, ohne die Kopien, die es dort ohnehin schon gab.

**Was nicht passiert ist.** Keine Kursdatei, kein Snapshot, keine Datenbank
verändert; kein Bot gestartet; keine Order; kein alter Regeltext umgeschrieben.
Zwei kleine Stellen im Regelwerk, die den Stand von vorgestern beschreiben,
sind absichtlich stehen geblieben — die neuen Einträge sagen an ihrer Stelle,
was sich geändert hat.

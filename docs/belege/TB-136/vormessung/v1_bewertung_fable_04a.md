# Vormessung TB-136 — Fable-Antwort 04.10.a gegen Register und Code gemessen und bewertet — an: steuernder Chat, Mac-Sitzung TB-136

*Steuernder Chat, 04.10.2026, 11:24 MESZ. Gemessen am HEAD `d781f1b` (= `origin/main`), Register am Commit `ee43f5f`. Drei Helfer, nur lesend über die Geräteanbindung (kein `git status`, nichts im Repo angelegt, kein Skript des Repos ausgeführt); ihre Berichte liegen daneben: `h1_fundstellen_r74.md`, `h2_fundstellen_r75.md`, `h3_fundstellen_r76_r77_leseprotokoll.md`. Eine Messung aus der VM ist kein Nachweis; die Mac-Sitzung misst nach.*

## 1. Die Datei

- Ablage: `projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md`, über `project_info` gefunden (angelegt 2026-10-04 08:44:06 UTC).
- Zwei unabhängige Abschriften (zwei Helfer, 8 und 7 Teile), `cmp` gleich: 29 195 B, 167 Zeilen, md5 `856b2c158e4bb6870876de129ce71f76`.
- Im Repo: `docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md`, md5 und Bytes auf dem Gerät nachgemessen, gleich. Unverfolgt.
- Grenze: Fable nennt keine md5 der Antwortdatei; der Vergleich „mit Fables Angabe“ entfällt. Das Werkzeug liefert Text; unsichtbare Zeichen (geschütztes Leerzeichen in Zifferngruppen, sechs Stellen) sind daran nicht zu unterscheiden. Geschrieben ist U+0020 wie in 02c und in `UEBERGABE.md` (dort gemessen).

## 2. Zählung am Block (nicht an „Kurz“)

| Block | Unterpunkte | Voraussetzungen in eckigen Klammern |
|---|---|---|
| R74 | (a)–(f) | 1, in (b): „vor dem Eintrag zu messen“ |
| R75 | (a)–(h) | 2, in (a) und (g): „zu messen“ |
| R76 | (a)–(e) | 0 |
| R77 | (a)–(c) | 0 |

Vier Blöcke, R74 bis R77; Kopf, „Kurz“ und Block nennen dieselben vier. Der Block hat acht nicht leere Zeilen (je Block eine Zeile und eine Zeile „Quelle des Grundes“). R77 (a) führt 13 Marken: 8 PRÄZISIERT, 5 ERGÄNZT. Höchster Block danach: R77; R frei ab R78.

## 3. Die drei Voraussetzungen

| | Voraussetzung | Messung | Ergebnis |
|---|---|---|---|
| V1 | R74 (b): Feld `kalender` der Messung TB-47 führt als Importstelle `notifications/boersenkalender.py` | `research/snapshotgrenze/ergebnisse/eingaben.json:96–106`: `"kalender": {"im_repo": [{"import": "pandas_market_calendars", "modul": "notifications/boersenkalender.py", "zeile": 81}], "in_selektionshuelle": [], "paket_vorhanden": "5.4.0"}` | **trifft** |
| V2 | R75 (a): der Kern, der die MtM-Reihe bildet, bildet die Tagesrendite als Summe der Beiträge der Positionen über einem Kapitalstand | `research/mtm_drawdown/mtm_kern.py` (339 Zeilen): Z. 251 `"mtm": buch + unreal`; Z. 244 `unreal[a:b + 1] += allokation[i] * (schluss / einstand[i] - faktor_kosten)`; Z. 210 `buch` aus `kapital_after`; Z. 246 `gebunden[a:b + 1] += allokation[i]`. Die Datei bildet keine Tagesrendite und keine Exposure, nur Kapitalreihen; keine Division durch einen Kapitalstand in `mtm_pfad` | **trifft im Wortlaut nicht:** Der Kern bildet keine Tagesrendite. Unrealisiertes ist je Position summiert; Realisiertes kommt über `kapital_after`, nicht je Position |
| V3 | R75 (g): der Bericht der Zeile aus `zellenbericht.csv` nach R34 verlangt keine eigene Zeile in der Berichtsliste von Abschnitt 8 | Abschnitt 8: Tabelle mit 13 Zeilen, `zellenbericht` 0-mal, „Haltedauer“ 0-mal; R34 (48.2): „auswertung.py liest die Zeile des Plateau-Gewinners und berichtet sie (22.2: Bericht, kein Tor; N unverändert)“ | **trifft am Bestand:** R34 berichtet schon heute ohne Zeile in Abschnitt 8 |

V2 hält den Eintrag nicht auf: R75 (a) verlangt die Meldung, „bevor der Zellen-Erzeuger die Attribution baut“, nicht vor dem Eintrag. Die Meldung ist fällig.

Beifang zu V1: Das Feld nennt `paket_vorhanden` 5.4.0; `requirements.lock:51` führt `pandas-market-calendars==4.6.1`, 17.5 nennt 4.6.1. Nicht bewertet; von Belang für die Messung nach R74 (e) in der Lock-Umgebung.

## 4. Zitate und Verweise

65 Messpunkte in drei Berichten (20, 24, 21). Jedes wörtliche Zitat ist gefunden; zwei stehen im Register über Zeilenumbruch und Fettdruck (17.5, 16.6). Kein Verweis führt ins Leere. Sinngemäss statt wörtlich, keiner davon in Anführungszeichen:

| | Stelle bei Fable | im Register |
|---|---|---|
| S1 | R75 (a): „Die Zuteilung läuft je Zelle einmal (R45)“ | R45 (48.13): „Eine Rekonstruktion der Positionen aus den Ereignissen der equity_curve ist ein zweiter Rechenweg und wird nicht gegangen.“ „einmal“ und „je Zelle“ stehen in R45 nicht |
| S2 | R75 (a), Quelle: „29.3 (ein Kapitalpfad)“ | 29.3 legt den Beginn fest: „Der Kapitalpfad eines Bots beginnt am 1. Januar seiner ersten Selektionsfalte …“; die Regel steht in 2a |
| S3 | R74, Quelle: „R59 (b) und R28 (Bauart: Kopie mit Probe)“ | R28 (47.11): „Literal mit Probe gegen den Registertext — und als benannter Zwischenstand zulässig, wenn jede Kopie ihre Probe hat“; die Wortfolge steht in der Quelle von R59 |
| S4 | R75 (b): „nie leer (R67)“ | R67: „kein Feld leer“ |
| S5 | R77 (c): „53.10 (Statusliste)“ | 53.10 heisst „Was offen bleibt“ |
| S6 | R77 (c): „der Index führt die Zählung, wie 45.1 zu R52“ | `REGISTER_INDEX.md`: 0 Treffer für „ter Fall“, „Zählung“, „Bestand behauptet“ |
| S7 | „Unsicher“ 5: „R35 nennt seine Berichtsliste abschliessend“ | „abschliessend“ steht nur in der Quelle des Grundes von R35 |

Code zu Frage 1: einziger Import `notifications/boersenkalender.py:81`, `KALENDER_NAME = "NYSE"` Z. 70, einziger Aufruf Z. 109; `research/vorregistrierung/` 0 Treffer. Code zu Frage 2: `research/vorregistrierung/auswertung.py` (860 Zeilen) führt die Tagesreihe als `datum, netto_rendite, exposure` (Docstring Z. 46); `kapital_drawdown_mtm_pct`, `zellenbericht`, `bestaetigung_ab_effektiv` kommen dort 0-mal vor; kein Zellen-Erzeuger im Repo. Zählung zu Frage 3: neunter Fall 45.1, zehnter 48.20 R52 (a), elfter 48.1 und R52 (b); „zwölfter Fall“ 0-mal im Register.

## 5. Bewertung (ARBEITSWEISE 5b)

**R74–R77 tragen. Kein Widerspruch in dem, was gemessen ist.** Sie werden als Abschnitt 54 eingetragen, nach Einzelfreigabe (TB-136). Die Vorbedingung aus R56 (b) erledigt Schritt 0 des Auftrags: Eröffnungstext und Antwortdatei liegen mit Commit im Repo, bevor eingetragen wird.

Gemessen: die Datei, die Zählung, drei Voraussetzungen, 65 Fundstellen, der Code an den genannten Stellen. Nicht gemessen: der Vergleich „NYSE“ gegen „XNYS“ selbst (nur die Textstellen in der Vormessung zur Anfrage); die Zeichengleichheit der Abschnittskopien mit dem Register; die Wiedergaben von 12, 24.6, 24b A2, 34 und 37.3 an ihrem eigenen Ort; was `project_search` Fable als Ausschnitt geliefert hat.

Lesarten des steuernden Chats, vorläufig:

1. **S1:** Die Regel „je Zelle einmal“ setzt R75 (a) selbst; R45 stützt sie nur für die Rekonstruktion aus der `equity_curve`. Die Entscheidung ruht auf 16.6, R37 (i) und 41.3 C2/C3, die im Wortlaut treffen.
2. **S6:** Vorgabe für die Indexzeile, kein Bestand. Der Index trägt nach dem Eintrag die Zählung bei 48.20.
3. **Marken über R77 (a) hinaus (R65 (a)):** 48.14 (R46) — R75 (d) und (f) geben der Abnahme eine weitere Prüfung und einen Deckelfall im Test-Snapshot; R77 (a) nennt 48.14 nicht. 48.7 (R39) trägt bei Fable nur Unterpunkt (b); R75 (g) erweitert die Feldliste von `zellenbericht.csv`, die nach R34 „Registertext (R39)“ ist. Der Auftrag TB-136 bestimmt die Marken und weist sie als meine aus.
4. **Leseprotokoll, Ausschnitt aus `BACKLOG.md`:** nach R56 (b) genannt („was nur als Ausschnitt“), Vorbild R32 (47.15). Ein eigener Block nach R56 (c) ist nach dieser Lesart nicht nötig. Das Suchwort „Ein-Pfad-Regel“ steht in `BACKLOG.md` nicht. Im Bereich mit Fables Stichworten (Z. 49–63, je die ersten 260 Zeichen) stehen „N gesamt, nominal 658“ und „Der Kandidat auf Rang 4“.

S1, S6, Lesart 3 und 4 und das Ergebnis zu V2 gehen als Kenntnis in die nächste Anfrage an Fable.

## 6. Für BACKLOG und JOURNAL (Inhalt; der Wortlaut mit Ankertext steht im Auftrag TB-136)

- **JOURNAL, Block EE:** Fable 04.10.a (R74–R77) geholt, gemessen, bewertet: trägt; V1 und V3 treffen, V2 trifft im Wortlaut nicht; eingetragen als Abschnitt 54.
- **BACKLOG, neu:** (1) Meldung zu V2 vor dem Bau des Zellen-Erzeugers; die Anforderung geht in die Anforderungsliste aus TB-135. (2) Verfahrensmessung nach R74 (e) in der Lock-Umgebung am Snapshot, zusammen mit R72 (d), vor dem Tag. (3) `eingaben.json` nennt `paket_vorhanden` 5.4.0, der Lock 4.6.1. (4) Fable stand nach einer Anfrage bei 468 406 (rot): Befund zur Probe „ein Fable-Chat je Anfrage“ (F4). (5) `project_search` liefert Ausschnitte gesperrter Dateien.

## 7. Projekt-Erinnerung (R56 (d))

Fable las `preferences.md` (9 241 B) und `ways-of-working.md` (2 232 B, Stand 01.10.), wie in der Eröffnung genannt. `ways-of-working.md` trägt seit 2026-10-04 08:53:00 UTC einen neuen Stand: der Werkzeugkopf nennt 2 482 B (die Übergabe nennt 2 503 B; der Unterschied ist nicht geklärt). Neu ist eine Zeile zur Cloud-Sitzung unter „Delegation“. Gelesen am 04.10.2026, 10:58; keine Grösse nach 27.1 gesehen. Vor der nächsten Eröffnung wird die Zahl neu gemessen und genannt.

## 8. Fehler des steuernden Chats in dieser Messung (ohne Nummer)

- Den Helfern den Pfad des Index aus dem Gedächtnis gegeben (`register_kopie/REGISTER_INDEX.md`); er liegt unter `docs/projektfuehrung/REGISTER_INDEX.md`. Alle drei haben es gemeldet und am richtigen Ort gelesen.
- 27.3 im Helferauftrag falsch beschrieben („was bei Kenntnis einer gesperrten Grösse gilt“); 27.3 sagt, dass der Verfahrensprüfer das Register vollständig lesen darf.
- Helfer H2 hat 16.6 und Teile von 8, 24.6, 41.1 und 50.2 über die Grenze von 300 Zeichen hinaus ausgegeben (in seinem Arbeitsbereich, nicht im Chat).

# TB-117 — Bündel „Wachen vor dem Tag“ (Fable 27a): Register 45.11 und 46 (R9–R17), Sonde zweiseitig, vierte Öffnung `herkunft.py`, Öffnung `auswertung.py` (Herkunftsprüfung), neues Abbild

**Sitzungstitel:** `TB-117` · **Angelegt:** 26.09.2026, 22:30, vom steuernden Chat
**Vorgänger:** TB-116 (`8b342ab`) · **Aufwand:** hoch (ARBEITSWEISE 22.1)
**Grundlage:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27a_sonde_zweiseitig_herkunft_in_auswertung.md`, md5 `d4367c65a9dcad4b28cceb6f50706d59`, 30 836 Bytes. Wird in Schritt 0 committet. Der Registerblock R9–R17 steht am Ende der Datei als Codeblock. Fables Einordnung steht in Abschnitt 4 der Antwort: *„Ein Bündel, eine Freigabekarte je Sperrlistendatei (`herkunft.py`, `auswertung.py`, Sonde), dann ein Abbild.“*

## ⭐⭐ Freigabe des Betreibers, wörtlich

**26.09.2026, ca. 22:20, Auswahlkarte im steuernden Chat:** *„Meine Empfehlung: alle vier Teile zusammen als TB-117, wie Fable das Bündel angelegt hat. Keiner ändert eine Schwelle oder ein Ergebnis. Am wichtigsten ist auswertung.py: Es verspricht eine Herkunftsprüfung, die es nicht macht, und ohne Öffnung friert der Tag diesen Widerspruch ein. Eine Lesart lege ich im Auftrag fest und benenne sie für Fable: Die Herkunftsprüfung bricht nur im Selektionsmodus ab, ohne Modus zeigt sie die Herkunft nur an. Freigeben?“* ⇒ **„Alle vier freigeben (Empfohlen)“**. Gemeint sind die vier Teile der vorigen Karte:
- Regelwerk 45.11 + 46;
- Prüfsonde zweiseitig;
- `herkunft.py`, vierte Öffnung;
- `auswertung.py` öffnen.

| freigegeben | Pfad / Handlung |
|---|---|
| ✔ | `docs/VORREGISTRIERUNG_neuselektion.md`: 45.11 und Abschnitt 46 **anhängen**, Marken additiv |
| ✔ | `shared/sperrlistensonde.py` und `shared/test_sperrlistensonde.py`, **nur** Block B. Gemessen vom steuernden Chat: Die Sonde steht weder auf der Sperrliste noch im Abbild; sie ist in keinem Punkt des Abbilds `5e5ad109…` genannt |
| ✔ | `research/vorregistrierung/herkunft.py` und seine Tests, **nur** Block C |
| ✔ | `research/vorregistrierung/auswertung.py` und seine Tests, **nur** Block D. Dazu `beispieldaten.py`, **nur** wenn die Tests sonst nicht zu bauen sind; jede Änderung einzeln im Ergebnis |
| ✔ | ein **neues** Abbild unter neuem Namen (Block E) |
| ✔ | `docs/projektfuehrung/JOURNAL.md` (Block **DP**), `docs/belege/TB-117/`, `docs/ERGEBNIS_TB-117_wachen_vor_dem_tag.md` |

⛔ **Nicht freigegeben:**
- jede andere Code-Änderung, besonders `paths.py`, `faltenplan.py`, `benchmark.py`, die vier Ausschlussmengen (R13 (a): nur die **Probe**, keine Zusammenlegung), `forward_test.py`, `zuteilung.py`;
- jede Marke im Listentext von Abschnitt 10. Die Tatsachennotiz „an Punkt 8“ aus R15 (a) steht deshalb **in 46**, mit Verweis auf Punkt 8, nicht im Listentext;
- ein Eintrag in Register 9;
- das Überschreiben eines Abbilds;
- Datenbanken, `crontab`.

---

## 0. Schritt 0

**0a — committen.** Erwartet uncommittet, sonst nichts:

| Datei | Stand |
|---|---|
| `docs/auftraege/MAC_TB-117_wachen_vor_dem_tag.md` | dieser Auftrag |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | Zeiger TB-117 |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27a_sonde_zweiseitig_herkunft_in_auswertung.md` | md5 `d4367c65a9dcad4b28cceb6f50706d59` |

Weitere Dateien: melden, nicht mitcommitten. Commit „TB-117 Schritt 0: Auftrag, Zeiger, Fable-Antwort 27a“, Push.

**0b — Ausgangswerte** (`0b_ausgang.txt`):
- `register()` `5acb4c19…`, `fehlend` leer;
- Hashes `herkunft.py` `ed521ac1…`, `sperrlistensonde.py` `f88e54ee…` und `auswertung.py`, die Werte aus TB-116 0b;
- Sonde gegen `5e5ad109…` 34/0/0;
- Benchmark `64fb2912…`.

## Block A — Register 45.11 und Abschnitt 46

Bauart TB-114: Zitate werden eingesetzt, nicht abgetippt; vorher Probelauf gegen eine Kopie.

- **45.11** ans Ende von 45 (45 ist heute der letzte Abschnitt): **R11 zeichengleich**, samt „Quelle des Grundes“.
- **`## 46.`** sinngemäss „Sonde zweiseitig, `fehlend` im Modus, zwei Erzeuger, Snapshot-Bindung, Herkunftsprüfung in `auswertung.py` — die Einträge aus Fable 27a (TB-117, 26.09.2026)“:
  - **46.0 Kopf:** Anlass, Quelle mit md5, Kette zu 45.
  - **46.1–46.8:** R9, R10, R12, R13, R14, R15, R16, R17 **zeichengleich**, je mit „Quelle des Grundes“.
  - **46.9 Lesart des steuernden Chats, von Fable zu bestätigen (Tatsachennotiz):** *„R14 unter dem Modus vollständig: Jede der fünf Bedingungen endet mit 2. Ohne Modus liest `auswertung.py` `herkunft.json`, wenn vorhanden, und zeigt Commit, Datenstand und Register-Hash im Kopf des Berichts, bricht aber nicht ab. Grund: Ohne Modus laufen Beispieldaten und Tests, und `beispieldaten.py` schreibt Nullwerte (Z. 210 ff.). Dieselbe Bauart wie R10 (`fehlend` ⇒ 2 nur unter dem Modus).“*
  - **46.10 Was offen bleibt:** TB-116 (Leiter-Lesarten, fünf Stellen) bei Fable; der Listen-Erzeuger nach 40.6; der Zellen-Erzeuger (Stufe V); Stufe IV.
- **Marken** (additiv; direkt unter dem Anker, nie in ein Zitat hinein, **nie im Listentext von 10**):

| Wo | Marke |
|---|---|
| **40.8** (Unterpunkt (e), wo die Sonde die Gruppen aus dem Abbild liest) | „zweite Seite: siehe 46.1“ |
| **41.1 A10** | „`fehlend` im Modus: siehe 46.2“ |
| **40.6**, **41.1 A12** und **45.3** | „zwei Erzeuger; Bindung der Listen: siehe 46.3“ |
| **12** (Vollständigkeitstest) und **36.5** | „Herkunftsprüfung in `auswertung.py`: siehe 46.5, Lesart 46.9“ |
| **16.4** (unter „Prüfung vor dem Tag“) | „Evidenz der Leiter: siehe 46.4 (f); Lesarten: TB-116“ |
| **45.7** (R7) | „Nr. 7: siehe 46.7 (a)“ |
| **45.10** | „beantwortet und fortgeschrieben in 45.11 und 46“ |

  Wo ein Anker nicht eindeutig ist (z. B. 40.8 (e)): im Ergebnis nennen, wo die Marke steht, und warum.
- **Nachweise:**
  - numstat zweite Spalte 0;
  - 9 × `diff` rc 0 gegen den Codeblock der Fable-Datei (R9–R17), dazu eine Mutationsprobe;
  - Zitate `diff` rc 0;
  - Sonde gegen `5e5ad109…` vorher = nachher;
  - `register()` alt/neu;
  - `test_vorregistrierung`.

Commit, Push.

## Block B — Sonde zweiseitig (R9)

- `sperrlistensonde.py` vergleicht **zusätzlich** die Menge `lies_eingefroren(wurzel)` (heute, `herkunft.py::EINGEFROREN`) mit der Gruppe `eingefroren` des Abbilds. Ein Eintrag nur auf einer Seite ist ein Befund ⇒ 1, mit Nennung des Eintrags und der Seite („Liste → Abbild fehlt“ bzw. „Abbild → Liste fehlt“). Die bestehende Prüfung Abbild → Dateien bleibt unverändert.
- **Vorher lesen:** `_pruefe_gruppe` (Z. 418 ff.) und `lies_eingefroren` (Z. 258 ff.) am Stand `8b342ab`. Die Stelle des Einbaus steht im Ergebnis.
- **Proben** mit Mutationsgegenprobe:
  1. gegen `5e5ad109…` kein Mengenbefund;
  2. im Wegwerfbaum ein Eintrag mehr in `EINGEFROREN` ⇒ 1, Seite genannt;
  3. ein Eintrag weniger ⇒ 1;
  4. Mutation „Vergleich aus“ ⇒ Probe 2 rot.
- **Messung, nicht Erwartung:** Die Sonde läuft gegen das alte Abbild `e655c1c8…`, und die Sitzung beschreibt, was sie meldet. Nach dem Wortlaut von R9 sind die neun TB-24-Listen als „nur in der Liste“ zu **erwarten**. Meldet die Sonde es anders, ist das ein Befund, **kein Abbruch**.

Commit, Push.

## Block C — `herkunft.py`, vierte Öffnung (R10, R15 (a), R17 (a))

1. **R10:** `register()` und `block()` enden unter dem Modus mit 2 (`_abbruch_2` bzw. die bestehende Abbruchform dieser Datei, im Ergebnis nennen), wenn `fehlend` nicht leer ist. Die Meldung nennt die fehlenden Einträge. Ohne Modus: unverändert.
2. **R15 (a):** In `EINGEFROREN` kommen hinzu:
   - `snapshots/<registrierter Snapshot-Hash>/MANIFEST.json`;
   - die Snapshot-Kopien von `config/top25_symbols.txt` und `config/sp500_top150.txt`.

   **Vorher messen:**
   - Liegen die drei Dateien im Snapshot-Ordner und sind sie versioniert?
   - Wie heissen die Pfade genau?
   - Löst die Pfadregel aus TB-114 B1 (enthält `/`, nicht `ergebnisse/` ⇒ repo-relativ) sie richtig auf, in `herkunft.py` **und** in der Sonde? Das ist Fables zweites „Unsicher“.

   Braucht es eine dritte Auflösung: **Abbruch, melden** (Code ausserhalb der Freigabe).
3. **R17 (a):** Der Modulkopf nennt, was `register()` hasht, einschliesslich der TB-24-Listen und der Snapshot-Dateien.

**Proben** mit Mutationsgegenprobe:
- Modus + fehlende eingefrorene Datei ⇒ 2, an `register` und an `block`;
- ohne Modus ⇒ rc 0 mit `fehlend` gefüllt;
- `register()` im Repo: `fehlend` leer, 23 Teile (20 + 3).

Testannahmen, die Anzahlen fest kodieren, werden nach Grundsatz 40 nachgezogen. Jede Änderung steht einzeln im Ergebnis, mit dem Nachweis, dass die alte Fassung genau dort bricht.

Hash-Übergänge: `herkunft.py`, `register()`. Commit, Push.

## Block D — `auswertung.py`, Öffnung (R14, R8 (a), Lesart 46.9)

1. **Vorher lesen:** den Vertrag im Docstring (Z. 51–52), `main()` (Z. 637 ff.), `_abbruch_2` (Z. 131 ff.), Register 12 und 36.5. Wo R14 und der heutige Code sich reiben, steht das im Ergebnis.
2. **Unter dem Modus** endet `auswertung.py` mit 2, wenn:
   - `<wurzel>/<bot>/herkunft.json` für einen Bot fehlt;
   - der Commit nicht zum Tag-Commit passt (`TB_SELEKTIONSCOMMIT`, 7–40 Hex-Zeichen, Präfixvergleich);
   - der Datenstand nicht der registrierte ist. Den Wert nimmt die Sitzung aus dem Register (Fundstelle nennen), nicht aus diesem Auftrag;
   - der Register-Hash nicht `herkunft.register()["register"]` zur Laufzeit entspricht;
   - die neun Dateien untereinander abweichen.
   
   Die Meldung nennt Bot, Feld, erwarteten und gefundenen Wert.
3. **Ohne Modus** (Lesart 46.9): lesen, wenn vorhanden; im Berichtskopf anzeigen; kein Abbruch.
4. **Bericht:** Der Kopf trägt Commit, Datenstand und Register-Hash (Text und `--json`).
5. **R8 (a):** Den Satz *„`Abbruch` … endet mit 1“* im Docstring von `_abbruch_2` streichen bzw. berichtigen. Er ist falsch seit TB-111.

**Proben** mit Mutationsgegenprobe (Bauart `test_ersatzwerte`):
- je Bedingung ein Fall ⇒ 2;
- der gute Fall ⇒ rc 0 mit Herkunft im Kopf;
- ohne Modus mit Nullwerten ⇒ rc 0, Kopf zeigt die Nullwerte.

Braucht der gute Fall unter dem Modus gültige `herkunft.json` in Beispieldaten, erzeugt der Test sie im Wegwerfbaum. `beispieldaten.py` wird nur geändert, wenn das nicht geht.

Hash-Übergang `auswertung.py`. Commit, Push.

## Block E — Neues Abbild und Nachmessung

- **Abbild** mit `sperrliste_abbild.py`:
  - neuer Name, z. B. `sperrliste_abbild_2026-09-26_tb117.json`;
  - `test -f` vorher;
  - `eingefroren` hat so viele Einträge wie `EINGEFROREN`.
- **Sonde gegen das neue Abbild:** 0 Befunde, (ii) 0, kein Mengenbefund.
- **Sonde gegen `5e5ad109…`:** **beschreiben**, was sie meldet. Ursache der Einträge: die in diesem Auftrag geänderten Dateien und die neuen Einträge. Keine Erwartung, kein Abbruch; das Ergebnis ordnet jeden Eintrag einer Änderung dieses Auftrags zu. Ein Eintrag ohne Zuordnung ist ein Befund.
- **Unverändert:**
  - Benchmark im Modus, Repo **und** frischer Klon `64fb2912…`;
  - ohne Modus 8/8 bytegleich;
  - Trockenlauf 9 × rc 0;
  - `faltenplan.json` gleich;
  - Laufbereich: messen und mit TB-114 (81) vergleichen, jede Abweichung erklären.
- **Tests:**
  - `test_vorregistrierung`, `test_ersatzwerte`, `test_sperrlistensonde`, `test_startpruefungen`, `test_arbeitsbaum_laufbereich` und die übrigen Testdateien unter `research/vorregistrierung/` und `shared/`: rc 0;
  - bekannte Rote aus TB-114 C (`test_drawdown_beide_masse`, `test_stabile_sortierung`, `test_wellenauswahl`) nur mit Bestätigung „ohne Bezug“.
- **Neue Probe R13 (a)**, Handwerk: Die vier Ausschlussmengen werden eingelesen und müssen gleich sein. Ort nach Wahl der Sitzung, ausserhalb der Sperrlistendateien, mit Mutationsgegenprobe. Die Mengen werden **nur gelesen**, keine davon geändert.

Commit, Push.

## Block F — Register 46.11 (Vollzug), Journal, Ergebnis

- **46.11 Vollzug in TB-117** (Tatsachennotiz):
  - B, C, D mit Hash-Übergängen;
  - gültiges Abbild (Name, sha256);
  - Sonde gegen das alte Abbild mit der Zuordnung;
  - die Probe R13 (a);
  - `register()` neu.
  
  Nachweise wie Block A.
- Journalblock `## DP — TB-117: …`.
- `docs/ERGEBNIS_TB-117_wachen_vor_dem_tag.md` mit „Für Fable“ (jede Reibung zwischen R14 und dem Code, die Pfade aus C2, jede nachgezogene Testannahme, Lesart 46.9 zur Bestätigung) und „In einfacher Sprache“.

## Commits

1. Schritt 0;
2. A;
3. B;
4. C;
5. D;
6. E;
7. F.

Nach jedem Commit Push.

## ⚠️ Abbruchkriterien — melden, nicht reparieren

- numstat des Registers mit zweiter Spalte ≠ 0; `diff` eines R-Bausteins rc ≠ 0.
- Benchmark ≠ `64fb2912…`, eine Ausgabe ohne Modus verändert, der Trockenlauf nicht 9 × rc 0, ein Test rot mit Bezug zu dieser Sitzung.
- Ein Abbild würde überschrieben.
- Eine Änderung wäre nötig ausserhalb der freigegebenen Dateien, etwa eine dritte Pfadauflösung in `paths.py`.

**Kein Abbruch sind:**
- was die Sonde gegen ein altes Abbild meldet (beschreiben);
- Reibungen zwischen Fables Text und dem Code (melden, im Rahmen der Freigabe lösen oder offen lassen);
- abweichende Anzahlen (beschreiben).

## In einfacher Sprache

Fable hat die Lücken aus den letzten zwei Prüfungen beantwortet; diese Sitzung schliesst sie in einem Zug.
- **Regelwerk:** Die neuen Textbausteine kommen wörtlich hinein, und das neue Abbild gilt.
- **Prüfwerkzeug:** Es vergleicht künftig in beide Richtungen.
- **`herkunft.py`:** Das Programm, das Prüfsummen festhält, bricht im Selektionsmodus ab, wenn eine festgehaltene Datei fehlt, und hält künftig auch die Beschreibungsdatei des Datenstands fest.
- **`auswertung.py`:** Das Auswertungsprogramm prüft endlich, woher die Zahlen kommen, die es auswertet, so wie es seine eigene Beschreibung verspricht.

Am Ergebnis des Laufs ändert sich nichts. Danach wird alles nachgemessen und ein neues Abbild geschrieben.

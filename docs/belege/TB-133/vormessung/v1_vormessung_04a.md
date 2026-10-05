# Vormessung 04a — v1 (Wortlaut-Auszüge und Fundstellen)

- Gemessen: 2026-10-04 07:49:53 UTC
- HEAD: d781f1b
- Register: docs/VORREGISTRIERUNG_neuselektion.md; sha256 9a2cefb77a394a0a1c87c63cb9437d5693f054e4516333f656fae97668ef71ff; 906766 Bytes; 11471 Zeilen
- weitere Quellen: docs/belege/TB-132/vormessung/v5_code_02c.md (sha256 c68e7eead0a28cf620fc7665a6c30590fe3a134d5aaffc898252435d1b61d098); docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md (sha256 aa4cf09ec6f694ac52a5bc37c42bdde75aef9f7e4f460404ee9f13bc7ed59ac2); docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md (sha256 ca5977e0118756574ea82aab02d70ed389607ae4c5646b32b98b9aa8f04bb1cd)
- Schnittregel: Wortlaute per Skript ausgeschnitten. Unterpunkt (x) = Blockzeile ab „(x)“ bis vor den nächsten Unterpunkt (Endleerzeichen entfernt). Umfeld n = n/2 Zeichen vor und n/2 Zeichen nach dem Treffer, über Zeilengrenzen hinweg, auf den Suchbereich begrenzt; überlappende Fenster sind zu einem Auszug vereinigt. Mehrwort-Suchwörter werden auch über einen Zeilenumbruch gefunden.
- Schreibzugriffe auf das Repo: keine

## A1 Register 17.5

Unterabschnitt 17.5: Z. 2824–2855 (nächste Überschrift Z. 2857); 1703 Zeichen

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 2824 (Überschriftzeile)

```text
### 17.5 Registertext 5f — die registrierte Umgebung *(neu)*
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 2826–2855 (Unterabschnitt 17.5 ohne Überschriftzeile)

```text
> Der Selektionslauf findet auf einer **registrierten Umgebung** statt:
> **Python-Fassung** (Tatsachennotiz: 3.9.6), ein **`requirements.lock`** mit
> exakten Versionen aller Pakete, dessen Hash im Register steht, und die
> **Plattform**. Der Lauf beginnt mit einer Prüfung dieser drei Angaben und
> **bricht bei Abweichung ab (Rückgabewert 2)**.
>
> ⭐ **Tatsachennotiz:** Der Handelskalender kommt **nicht aus einer Datei**,
> sondern aus dem Paket **`pandas_market_calendars`** (gemessen TB-47:
> Fassung **4.6.1** auf dem Betriebsrechner). Er ist damit **Umgebung, nicht
> Eingabe**, und liegt im Lock.
>
> Der Reproduktionstest gilt als bestanden, wenn ein zweiter Lauf **auf
> derselben registrierten Umgebung** auf einer anderen Maschine bitidentisch
> ist. Eine Reproduktion auf anderer Umgebung wird **berichtet**, ist aber
> weder Bedingung noch Widerlegung.

⚠️ **Das schärft die Prüfung aus 16.3 nach.** Dort stand: der Lauf „muss auf
einer zweiten Maschine bitidentisch reproduzieren". **Ohne Umgebungsbegriff war
das nicht entscheidbar** — eine Abweichung konnte am Snapshot liegen oder an
einer anderen Paketfassung, und beides sah gleich aus. Erst mit der
registrierten Umgebung trennt der Test die beiden Fälle. Der Satz in 16.3
bleibt stehen und gilt weiter; 17.5 sagt, **auf welcher Grundlage** er gemessen
wird.

⭐ **Warum der Kalender eigens genannt ist:** Er ist die einzige Eingabe des
Laufs, die **wie eine Datei aussieht und keine ist**. Wäre er Eingabe, gehörte
er in den Snapshot; als Paket gehört er in den Lock. Die Einordnung ist
gemessen worden (TB-47, `eingaben.json`, Feld `kalender`) und nicht geraten.

---
```

Suchwort „Kalender“: 1 Treffer in 1 Zeilen; Z. 2850

Suchwort „pandas_market_calendars“: 1 Treffer in 1 Zeilen; Z. 2833

Suchwort „NYSE“: 0 Treffer

Suchwort „XNYS“: 0 Treffer

Suchwort „Handelstag“: 0 Treffer

Zusatzzählung ohne Gross-/Kleinschreibung „kalender“: 3 Treffer in 3 Zeilen; Z. 2832, 2850, 2853


## A2 R66 (a), (b)

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11384, R66 (a) [bis vor (b); Zeichen 146–623 der Zeile; Block unter Z. 11382: ### 53.1 R66 —]

```text
(a) Die Tagesreihe einer Zelle führt jeden Handelstag des Kapitalpfads, vom 1. Januar der ersten Selektionsfalte des Bots (29.3) bis zum Ende der Bestätigungsperiode (35.1), ohne Lücke. Handelstage sind bei Krypto die Kalendertage (15.4, Anmerkung 1), bei Aktien die Tage des Handelskalenders nach 17.5 (Umgebung, im Lock). Ein Tag, an dem die Zelle keine Position hält, steht mit Rendite 0 und Exposure 0 in der Reihe (1a), auch ein Tag vor dem ersten Handelbar-Tag des Bots.
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11384, R66 (b) [bis vor (c); Zeichen 623–1301 der Zeile; Block unter Z. 11382: ### 53.1 R66 —]

```text
(b) Kalender und Kurse stimmen überein: Im Zeitraum nach (a) trägt an jedem Handelstag mindestens ein Symbol der Universumsdatei des Bots (3a) im Snapshot einen Kurs, und kein Symbol der Universumsdatei trägt einen Kurs an einem Tag, der kein Handelstag ist. Eine Abweichung ist ein Befund über Daten oder Umgebung, kein Ausgang (Bauart R33). Der Zellen-Erzeuger prüft das im Lauf je Bot und endet sonst mit 2. Die Abnahme nach R46 prüft diese Wache, mit Gegenprobe; der registrierte Lauf trägt sie selbst. [Voraussetzung, zu messen: welchen Kalender des Pakets der Code des Laufs benutzt (TB-47, Feld kalender); die Messung zur Anfrage 02.10.c verglich mit dem NYSE-Kalender.]
```


## A3 Register 53.9 — Zeilen mit Kalender / NYSE / XNYS

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11440, 53.9 (enthält: Kalender; Absatz)

```text
Tatsachennotizen des steuernden Chats zu den Voraussetzungen, die Fable in 02c „zu messen“ nennt, und zu den Tatsachen, die die Blöcke über Code und Daten führen. Gemessen am 02.10.2026 am Stand `0779453`, nur lesend, durch Helfer des steuernden Chats; die Berichte liegen unter `docs/belege/TB-132/vormessung/` (`v1_register.md` bis `v5_code_02c.md`, dazu zwei Proben und die zwei Ausgaben der Probe zu R71). Die Sitzung TB-132 hat in Schritt 0 die genannten Zeilen und Zählungen an Code und Register am Commit `57ae0d8` nachgemessen (`docs/belege/TB-132/0d_vorpruefung.txt`) und die Probe zu R71 in der Lock-Umgebung wiederholt. Die Zählungen am Datenbestand und die Kalendervergleiche hat sie nicht wiederholt. Zeilenangaben zum Code gelten am Commit `57ae0d8`. „REG Z.“ nennt Registerzeilen am Stand `ad351d5`, also vor diesem Eintrag. Aussagen über ein Fehlen (kein Aufrufer, kein Kalender im Lauf, kein Zellen-Erzeuger) sind Lesung der Helfer, soweit keine Zählung genannt ist. Gezählt sind Datumszeilen, Zeilennummern und Fassungen. Kein Ergebnis gelesen (27.1).
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11444, 53.9 (enthält: Kalender, NYSE, XNYS; Tabellenzeile)

```text
| R66 (53.1) (b) | welchen Kalender des Pakets der Code des Laufs benutzt (TB-47, Feld `kalender`) | Das Paket `pandas_market_calendars` importiert im Repo nur `notifications/boersenkalender.py` (Z. 81); dort stehen `KALENDER_NAME = "NYSE"` (Z. 70) und der einzige Aufruf `mcal.get_calendar(KALENDER_NAME)` (Z. 109). Die Datei steht nicht auf der Sperrliste und nicht im Laufbereich, weder in `ARBEITSBAUM_PFADE` (`shared/paths.py:239–253`) noch in der gemessenen Hülle (`docs/belege/TB-112/a2_laufbereich.txt`, 84 Pfadzeilen, davon 3 Messumschläge). `shared/entscheidungskerze.py` erreicht sie in Z. 384 (`import boersenkalender`). Diese Datei zählt über den Ordner `shared` zu `ARBEITSBAUM_PFADE`; zur gemessenen Hülle zählt sie nicht. Importiert wird sie von den neun `strategies/*/forward_test.py`, von Tests und von Forschungsskripten, von keinem Modul der gemessenen Hülle: Der Aufruf kommt aus dem Live-Pfad, nicht aus dem Selektionslauf. In den Pfaden der Hülle und in den neun Dateien der Sperrliste und der Gruppe „eingefroren“ steht kein Import und kein Aufruf des Pakets (vier Treffer der Suche in der Hülle sind Kommentar oder Docstring). Das Feld `kalender` aus TB-47 (`research/snapshotgrenze/erhebung_eingaben.py:606–610`) führt Importstellen und Paketfassung, keinen Kalendernamen; 17.5 nennt keinen. Am Bestand vom 02.10.2026 (nur Datumsspalten, nicht der Snapshot des Laufs): 16 275 Kurstage des Aktienmarktes von 1962-01-02 bis 2026-09-01; gegen den Kalender „NYSE“ des Pakets (4.6.1) 0 Tage nur im Kalender und 0 Tage nur in den Daten. Im Fenster 2000-01-01 bis 2026-09-30 führt „XNYS“ gegenüber „NYSE“ einen Handelstag mehr (2025-01-09). Beide Kalendervergleiche sind Ersatzmessungen ausserhalb der Lock-Umgebung: Python 3.10 und pandas 2.3.3 des Systems, die Kalenderpakete in den Fassungen des Locks aus `trading-env` | nicht entscheidbar: Der Code des Laufs benutzt heute keinen Kalender; welchen Namen der Zellen-Erzeuger nimmt, ist offen (53.10 Nr. 1). Die Wache nach R66 (b) prüft die Wahl im Lauf |
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11454, 53.9 (enthält: kalender — nur ohne Gross-/Kleinschreibung; Tabellenzeile)

```text
| R66–R73, Zitate und Verweise | — | 98 Stellen gegen den Wortlaut gemessen (`docs/belege/TB-132/vormessung/v4_register_02c.md`). Sinngemäss treffen zehn: R72 (b) fasst den Benchmark-Tag enger als der Wortlaut von 23.3 (REG Z. 3933–3936), das ist der Inhalt der Präzisierung; R72 nennt im Kopf den Registertext 3b (c), R70 (c) setzt die Marke nur an die Tatsachennotiz (53.10 Nr. 8); „TB-47, Feld kalender“ steht nur in der Erläuterung unter 17.5 (REG Z. 2847); „Dafür“ steht in R60 (c) klein (REG Z. 11196); „Bauart R55, R64“ in R69 (b) meint Prüfungen mit Gegenprobe, die Bauart der beauftragten Änderung steht in R45 (REG Z. 10857); von einer Öffnung spricht unter R36, R37, R34 und R55 nur R55; „R54 an 7 (c)“ ist in R61 (b) ein Glied der Aufzählung, keine Zeile (REG Z. 11209); 24.6 (REG Z. 4471) berichtet eine Zählung in einer Messung; R56 (c) (REG Z. 11168) nennt drei Fälle, der von R73 ist keiner davon; 23.2, Grund 2 (REG Z. 3908) ist Deutung des Verfahrensprüfers | keine Stelle trifft nicht; die sinngemässen gehen zur Kenntnis an Fable (53.10 Nr. 9) |
```

53.9: Z. 11438–11455; Zeilen mit Treffer: 3


## A4 Ganzes Register — NYSE, XNYS, pandas_market_calendars, Handelskalender (Umfeld 160)

Suchwort „NYSE“: 5 Treffer in 3 Zeilen; Z. 11384, 11444, 11460

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11384 (Treffer im Auszug: 1; Auszug reicht Z. 11384–11384) Suchwort „NYSE“

```text
enutzt (TB-47, Feld kalender); die Messung zur Anfrage 02.10.c verglich mit dem NYSE-Kalender.] (c) Der Falten-Sharpe nach 1c wird über alle Tage der Tagesreihe ger
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11444 (Treffer im Auszug: 1; Auszug reicht Z. 11444–11444) Suchwort „NYSE“

```text
o nur `notifications/boersenkalender.py` (Z. 81); dort stehen `KALENDER_NAME = "NYSE"` (Z. 70) und der einzige Aufruf `mcal.get_calendar(KALENDER_NAME)` (Z. 109). D
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11444 (Treffer im Auszug: 2; Auszug reicht Z. 11444–11444) Suchwort „NYSE“

```text
5 Kurstage des Aktienmarktes von 1962-01-02 bis 2026-09-01; gegen den Kalender „NYSE“ des Pakets (4.6.1) 0 Tage nur im Kalender und 0 Tage nur in den Daten. Im Fenster 2000-01-01 bis 2026-09-30 führt „XNYS“ gegenüber „NYSE“ einen Handelstag mehr (2025-01-09). Beide Kalendervergleiche sind Ersatzmessun
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11460 (Treffer im Auszug: 1; Auszug reicht Z. 11460–11461) Suchwort „NYSE“

```text
agesreihe (R66 (a), (b)): Der Code des Laufs benutzt keinen; im Repo steht nur „NYSE“ im Live-Pfad (53.9) | nächste Anfrage an Fable |
| 2 | Deckelfall (R68 (d)): B
```

Suchwort „XNYS“: 1 Treffer in 1 Zeilen; Z. 11444

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11444 (Treffer im Auszug: 1; Auszug reicht Z. 11444–11444) Suchwort „XNYS“

```text
lender und 0 Tage nur in den Daten. Im Fenster 2000-01-01 bis 2026-09-30 führt „XNYS“ gegenüber „NYSE“ einen Handelstag mehr (2025-01-09). Beide Kalendervergleiche 
```

Suchwort „pandas_market_calendars“: 3 Treffer in 3 Zeilen; Z. 2610, 2833, 11444

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 2610 (Treffer im Auszug: 1; Auszug reicht Z. 2609–2610) Suchwort „pandas_market_calendars“

```text
e Gegenprobe zu den 11 Symbolen | `docs/projektfuehrung/BACKLOG.md`, T34.9 |
| `pandas_market_calendars` 4.6.1, beide Hashes | `docs/MACLAUF_TB-47_snapshotgrenze.md` (TB-47-Maclauf) |
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 2833 (Treffer im Auszug: 1; Auszug reicht Z. 2832–2834) Suchwort „pandas_market_calendars“

```text
Der Handelskalender kommt **nicht aus einer Datei**,
> sondern aus dem Paket **`pandas_market_calendars`** (gemessen TB-47:
> Fassung **4.6.1** auf dem Betriebsrechner). Er ist damit 
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11444 (Treffer im Auszug: 1; Auszug reicht Z. 11444–11444) Suchwort „pandas_market_calendars“

```text
der des Pakets der Code des Laufs benutzt (TB-47, Feld `kalender`) | Das Paket `pandas_market_calendars` importiert im Repo nur `notifications/boersenkalender.py` (Z. 81); dort stehen
```

Suchwort „Handelskalender“: 4 Treffer in 4 Zeilen; Z. 2832, 11384, 11385, 11412

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 2832 (Treffer im Auszug: 1; Auszug reicht Z. 2830–2833) Suchwort „Handelskalender“

```text
> **bricht bei Abweichung ab (Rückgabewert 2)**.
>
> ⭐ **Tatsachennotiz:** Der Handelskalender kommt **nicht aus einer Datei**,
> sondern aus dem Paket **`pandas_market_calen
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11384 (Treffer im Auszug: 1; Auszug reicht Z. 11384–11384) Suchwort „Handelskalender“

```text
e sind bei Krypto die Kalendertage (15.4, Anmerkung 1), bei Aktien die Tage des Handelskalenders nach 17.5 (Umgebung, im Lock). Ein Tag, an dem die Zelle keine Position hält, 
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11385 (Treffer im Auszug: 1; Auszug reicht Z. 11385–11385) Suchwort „Handelskalender“

```text
der Handelstag gehört zu der Falte, in die sein Datum fällt“); 29.3; 17.5 („Der Handelskalender kommt nicht aus einer Datei, sondern aus dem Paket“; „Umgebung, nicht Eingabe“)
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11412 (Treffer im Auszug: 1; Auszug reicht Z. 11412–11412) Suchwort „Handelskalender“

```text
7 (c) — mittlere Exposure des Gewinners, Tage nach R64 (a), (b) und (d). 17.5 — Handelskalender der Aktien-Tagesreihe, R66 (a) und (b). 50.7 Nr. 3 — Tagesbasis des DSR, R66 (f
```


## A5 Code (*.py ohne .git, trading-env, __pycache__) und Lock-/Requirements-Dateien

durchsuchte *.py: 694

Suchwort `pandas_market_calendars`: 13 Trefferzeilen in 6 Dateien (notifications/boersenkalender.py, research/registernachtrag_tb48/pruefe_abschnitt17.py, research/snapshotgrenze/erhebung_eingaben.py, shared/entscheidungskerze.py, shared/snapshot.py, shared/test_entscheidungskerze.py)

```text
notifications/boersenkalender.py:38: GEWAEHLT: `pandas_market_calendars`. Begruendung siehe requirements.txt
notifications/boersenkalender.py:81:     import pandas_market_calendars as mcal
notifications/boersenkalender.py:87:         f"Die Bibliothek pandas_market_calendars ist nicht installiert "
research/registernachtrag_tb48/pruefe_abschnitt17.py:47:   * `pandas_market_calendars` **4.6.1** (17.5) - der Registertext sagt
research/snapshotgrenze/erhebung_eingaben.py:96: FREMDPAKETE = ("pandas_market_calendars", "exchange_calendars", "pandas",
research/snapshotgrenze/erhebung_eingaben.py:609:         "paket_vorhanden": _paketfassung("pandas_market_calendars"),
research/snapshotgrenze/erhebung_eingaben.py:669:           "`pandas_market_calendars` gebaut.")
shared/entscheidungskerze.py:362:                       "pandas_market_calendars fehlt).")
shared/snapshot.py:131: `pandas_market_calendars` (`mcal.get_calendar`), nicht aus einer Datei - er
shared/test_entscheidungskerze.py:33: `pandas_market_calendars` auf dem pruefenden Rechner liegt - und zusaetzlich,
shared/test_entscheidungskerze.py:169:                 "grund": "Die Bibliothek pandas_market_calendars fehlt.",
shared/test_entscheidungskerze.py:328:         print("    uebersprungen: pandas_market_calendars ist hier nicht "
shared/test_entscheidungskerze.py:885:         print("    uebersprungen: ohne pandas_market_calendars kann der "
```

Suchwort `get_calendar`: 2 Trefferzeilen in 2 Dateien (notifications/boersenkalender.py, shared/snapshot.py)

```text
notifications/boersenkalender.py:109:         _KALENDER = mcal.get_calendar(KALENDER_NAME)
shared/snapshot.py:131: `pandas_market_calendars` (`mcal.get_calendar`), nicht aus einer Datei - er
```

Suchwort `mcal`: 4 Trefferzeilen in 2 Dateien (notifications/boersenkalender.py, shared/snapshot.py)

```text
notifications/boersenkalender.py:81:     import pandas_market_calendars as mcal
notifications/boersenkalender.py:85:     mcal = None
notifications/boersenkalender.py:109:         _KALENDER = mcal.get_calendar(KALENDER_NAME)
shared/snapshot.py:131: `pandas_market_calendars` (`mcal.get_calendar`), nicht aus einer Datei - er
```

Suchwort `"NYSE"`: 2 Trefferzeilen in 2 Dateien (dashboard/test_dashboard.py, notifications/boersenkalender.py)

```text
dashboard/test_dashboard.py:3998:           offen and offen.get("kalender") == "NYSE", str(offen.get("kalender")))
notifications/boersenkalender.py:70: KALENDER_NAME = "NYSE"
```

Suchwort `'NYSE'`: 0 Trefferzeilen in 0 Dateien

Suchwort `XNYS`: 0 Trefferzeilen in 0 Dateien

Suchwort `exchange_calendars`: 1 Trefferzeilen in 1 Dateien (research/snapshotgrenze/erhebung_eingaben.py)

```text
research/snapshotgrenze/erhebung_eingaben.py:96: FREMDPAKETE = ("pandas_market_calendars", "exchange_calendars", "pandas",
```

Lock-/Requirements-Dateien (nach Dateiname gesucht, 18 Dateien geprüft): 8 Trefferzeilen für pandas_market_calendars / pandas-market-calendars / exchange_calendars / exchange-calendars

geprüfte Dateien: broker/requirements.txt, requirements.txt, docs/belege/TB-75/schritt2_blockbuchstaben.txt, docs/belege/TB-58b/probe_lock_vorher.txt, docs/belege/TB-58b/probe_lock_nachher.txt, docs/belege/TB-58b/lock_gegen_metadata.txt, docs/belege/TB-94/b_sonde_nach_blockB_altes_abbild.txt, docs/belege/TB-58/teil_a/requirements.lock.kandidat, docs/belege/TB-132/probe_lock_r71_rc.txt, docs/belege/TB-132/probe_lock_r71.txt, docs/belege/TB-132/probe_lock_r71_stderr.txt, docs/belege/TB-91/vormessung_blockA_absicherung_2026-09-23.txt, docs/belege/TB-91/sonde_nach_blockA_vormessung.txt, dashboard/requirements.txt, logs/auftraege/_erledigt/requirements.lock.kandidat, notifications/requirements.txt, notifications/warteauftraege.json.lock, requirements.lock

```text
requirements.txt:46: #   * exchange_calendars - dieselbe Datengrundlage (pandas_market_calendars
requirements.txt:65: pandas_market_calendars>=4.1,<5
docs/belege/TB-58/teil_a/requirements.lock.kandidat:33: exchange-calendars==4.5.6
docs/belege/TB-58/teil_a/requirements.lock.kandidat:47: pandas-market-calendars==4.6.1
logs/auftraege/_erledigt/requirements.lock.kandidat:33: exchange-calendars==4.5.6
logs/auftraege/_erledigt/requirements.lock.kandidat:47: pandas-market-calendars==4.6.1
requirements.lock:37: exchange-calendars==4.5.6
requirements.lock:51: pandas-market-calendars==4.6.1
```


## A6 v5_code_02c.md — R66 (b) / Kalender

Abschnitt „## P1“: Z. 25–92; 6646 Zeichen

**Fundstelle:** docs/belege/TB-132/vormessung/v5_code_02c.md, Z. 25 (Überschriftzeile)

```text
## P1 (R66 (b)) — welchen Kalender des Pakets benutzt der Code des Laufs?
```

**Fundstelle:** docs/belege/TB-132/vormessung/v5_code_02c.md, Z. 27 (enthält: NYSE; ganze Zeile)

```text
**Urteil: nicht entscheidbar aus dem Code des Laufs — er benutzt heute keinen Kalender.** Die einzige Stelle im Repo, die einen Kalender des Pakets baut, nennt `"NYSE"`; sie liegt ausserhalb von Laufbereich und Sperrliste. Das Feld `kalender` aus TB-47 nennt keinen Kalendernamen.
```

**Fundstelle:** docs/belege/TB-132/vormessung/v5_code_02c.md, Z. 33 (enthält: NYSE; ganze Zeile)

```text
- `notifications/boersenkalender.py:70` `KALENDER_NAME = "NYSE"` (Kommentar Z. 65–69: „Der NASDAQ-Kalender waere fuer diesen Zweck identisch“)
```

**Fundstelle:** docs/belege/TB-132/vormessung/v5_code_02c.md, Z. 38 (enthält: XNYS; ganze Zeile)

```text
„XNYS“ kommt in keiner `*.py` des Repos vor.
```

**Fundstelle:** docs/belege/TB-132/vormessung/v5_code_02c.md, Z. 44 (enthält: NYSE; ganze Zeile)

```text
| `notifications/boersenkalender.py` | der Aufruf, `"NYSE"` | nein (aus `notifications/` nur `manual_close.py`) | nein | nein |
```

**Fundstelle:** docs/belege/TB-132/vormessung/v5_code_02c.md, Z. 61 (enthält: NYSE, XNYS; ganze Zeile)

```text
- Register 17.5, Z. 2826–2829: „Der Handelskalender kommt **nicht aus einer Datei**, sondern aus dem Paket **`pandas_market_calendars`** (gemessen TB-47: Fassung **4.6.1** auf dem Betriebsrechner). Er ist damit **Umgebung, nicht Eingabe**, und liegt im Lock.“ Z. 2844–2847: „Die Einordnung ist gemessen worden (TB-47, `eingaben.json`, Feld `kalender`) und nicht geraten.“ Abschnitt 17 (Z. 2600–3200) nennt weder „NYSE“ noch „XNYS“.
```

**Fundstelle:** docs/belege/TB-132/vormessung/v5_code_02c.md, Z. 84 (enthält: NYSE; ganze Zeile)

```text
| `"NYSE"` | `pandas_market_calendars.calendars.nyse.NYSEExchangeCalendar` | 6 726 |
```

**Fundstelle:** docs/belege/TB-132/vormessung/v5_code_02c.md, Z. 85 (enthält: NYSE; ganze Zeile)

```text
| `"NASDAQ"` | dieselbe Klasse (`name: NYSE`) | 6 726, 0 Unterschiede |
```

**Fundstelle:** docs/belege/TB-132/vormessung/v5_code_02c.md, Z. 86 (enthält: XNYS; ganze Zeile)

```text
| `"XNYS"` | `pandas_market_calendars.class_registry.XNYS` (Spiegel von `exchange_calendars`) | 6 727 |
```

**Fundstelle:** docs/belege/TB-132/vormessung/v5_code_02c.md, Z. 88 (enthält: NYSE, XNYS, 2025-01-09; ganze Zeile)

```text
`"XNYS"` führt gegenüber `"NYSE"` **einen Tag mehr: 2025-01-09** (in beiden Fenstern, 2010… und 2000…); kein Tag nur in `"NYSE"`. Das Paket kennt 193 Kalendernamen. v3 (e) hat `"NYSE"` gegen die Kurstage gemessen (0 Unterschiede in beiden Richtungen); mit `"XNYS"` wäre der 09.01.2025 ein Handelstag ohne Kurs, also ein Befund nach R66 (b).
```

**Fundstelle:** docs/belege/TB-132/vormessung/v5_code_02c.md, Z. 239 (enthält: NYSE, XNYS; ganze Zeile)

```text
2. **Kalendervergleich `"NYSE"` gegen `"XNYS"`** (1.5): Ersatzmessung mit dem Paket aus `trading-env/` unter fremdem Interpreter; nicht gegen die Kursdaten gehalten (das tat v3 nur für `"NYSE"`), und nur für das Fenster 2000–2026.
```

Zeilen der Datei mit „NYSE“, „XNYS“ oder „2025-01-09“: 10


## B1 R68 (a)–(d)

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11398, R68 (a) [bis vor (b); Zeichen 115–495 der Zeile; Block unter Z. 11396: ### 53.3 R68 —]

```text
(a) Die Zeile der Bestätigungsperiode (R33) trägt für jede Zelle die Bestätigungsstatistik, die R37 (i) für den Gewinner beschreibt. Alle Grössen dieser Zeile stehen auf den Tagen ab bestaetigung_ab_effektiv der Zelle bis zum Ende der Spanne (35.1). Die Spanne bleibt, was 35.1 sagt; ihre Tage vor diesem Tag gehören weder zu einer Selektionsfalte noch zur Bestätigungsstatistik.
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11398, R68 (b) [bis vor (c); Zeichen 495–686 der Zeile; Block unter Z. 11396: ### 53.3 R68 —]

```text
(b) R64 (a) gilt für die mittlere Exposure dieser Zeile: Mittel über die Benchmark-Tage des Bots innerhalb der Tage nach (a). Die Grösse ist Bericht; auswertung.py liest sie für kein Urteil.
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11398, R68 (c) [bis vor (d); Zeichen 686–868 der Zeile; Block unter Z. 11396: ### 53.3 R68 —]

```text
(c) Eine Position, die nach der Attribution je Position (16.6, R37) in der Bestätigungsstatistik nicht gezählt wird, geht in keine Grösse der Zeile ein, auch nicht in ihre Exposure.
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11398, R68 (d) [bis Zeilenende; Zeichen 868–1359 der Zeile; Block unter Z. 11396: ### 53.3 R68 —]

```text
(d) Im Fall nach (c) ist die Zeile nicht der blosse Ausschnitt der Tagesreihe (16.6: „ausdrückliche und seltene Ausnahme von der Ein-Pfad-Regel“). Wie die Gleichheitsproben nach R60 (c) und R64 (d) und die Nachrechnung nach R36 diesen Fall behandeln, ist offen und geht vor der Öffnung nach R69 (b) als Frage an den Verfahrensprüfer. Tatsachennotiz: Die Fassung von 2d in 15.4 (d) („Tage im Embargo gehören zu keiner Periode“) ist durch 16.6 vollständig ersetzt und trägt diesen Block nicht.
```


## B2 Register 16.6 — Deckel, Attribution, je Position, Bestätigungsperiode (Umfeld 500); Marken-Zeilen

Unterabschnitt 16.6: Z. 2300–2351

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 2300 (Überschriftzeile)

```text
### 16.6 Registertext 2d — Embargo *(ersetzt die Fassung aus 15.4 vollständig)*
```

Suchwort „Deckel“: 4 Treffer in 4 Zeilen; Z. 2309, 2316, 2331, 2336

Suchwort „Attribution“: 2 Treffer in 2 Zeilen; Z. 2311, 2339

Suchwort „je Position“: 2 Treffer in 2 Zeilen; Z. 2311, 2339

Suchwort „Bestätigungsperiode“: 4 Treffer in 4 Zeilen; Z. 2302, 2310, 2329, 2331

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 2302, 2309, 2310, 2311, 2316 (Treffer im Auszug: 6; Auszug reicht Z. 2300–2321) alle vier Suchwörter, überlappende Fenster vereinigt

```text
### 16.6 Registertext 2d — Embargo *(ersetzt die Fassung aus 15.4 vollständig)*

> Die Bestätigungsperiode eines Bots beginnt am **ersten Handelstag nach
> Go-Live, an dem keine vor Go-Live eröffnete Position dieses Bots mehr offen
> ist.** Der Tag wird aus den Positionsdaten bestimmt und im Journal vermerkt.
> **Obere Schranke** ist die Zeitbremse des Bots, falls vorhanden; **für Bots
> ohne Zeitbremse das 95. Perzentil der Haltedauer plus 1** — für
> `t3_supertrend` **13 Handelstage** (P95 = 11,21).
>
> ⚠️ **Ist am Deckeltag noch eine vor Go-Live eröffnete Position offen, beginnt
> die Bestätigungsperiode trotzdem — diese Position wird in der
> Bestätigungsstatistik jedoch nicht gezählt** (Attribution je Position,
> ausdrückliche und seltene Ausnahme von der Ein-Pfad-Regel).

**Was sich gegenüber 15.4 ändert:** Das Embargo war dort eine **feste Frist**
(Zeitbremse + 1, Tage im Embargo gehören zu keiner Periode). Jetzt ist es eine
**Bedingung am Bestand** mit der alten Frist als **Deckel**. Der Grund: die
feste Frist verschenkt Bestätigungstage, wenn der Bot früher flach ist, und sie
reicht nicht, wenn er es nicht ist — beides ohne Not.

**Die gemessenen Embargo-Werte aus 15.4 bleiben** als obere Schranken gültig,
soweit sie der neu
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 2329, 2331, 2336, 2339 (Treffer im Auszug: 6; Auszug reicht Z. 2324–2342) alle vier Suchwörter, überlappende Fenster vereinigt

```text
MAX_HOLD_HOURS =
90` wird bei diesem Bot als **90 Tagesbalken** gelesen — der Kommentar im Bot
sagt es ausdrücklich („entspricht ~90 Handelstage"), und 15.4 Anmerkung 3 hat
es an der Kursreihe nachgemessen.

> **Folge, die ins Register gehört:** Die Bestätigungsperiode beginnt für
> `elliott_wave_stocks` **rund vier Monate später als für die anderen acht**
> (91 Handelstage Deckel gegen 11 bis 16). Wer die neun Bestätigungsperioden
> nebeneinander liest, liest für diesen einen Bot einen deutlich kürzeren
> Zeitraum — das ist kein Fehler, sondern seine Haltedauer.

> ⭐⭐ **Zwei Präzisierungen zu 2d und eine Rücknahme (41.3 C1–C3, Fable 24d,
> TB-108, 25.09.2026):** (1) Der Deckel für Bots ohne Zeitbremse — das 95.
> Perzentil der Haltedauer plus 1 — wird aus den **gefundenen** Trades
> gerechnet, nicht als Maximum über das Raster; er ist keine Leckschranke, das
> Leck schliesst die Attribution je Position (**41.3, C2**). (2) Die Bedingung
> („keine vor Go-Live eröffnete Position mehr offen") wird im Selektionslauf
> **für den Gewinner auf dessen eigenen simulierten Positionen** ausgewertet;
> das Journal des Papierpfads ist dafür keine Quelle (**41.3
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 2335–2345 (Marke; Marken-Zeile Z. 2335, Folgezeilen bis vor Leer-/Trennzeile)

```text
> ⭐⭐ **Zwei Präzisierungen zu 2d und eine Rücknahme (41.3 C1–C3, Fable 24d,
> TB-108, 25.09.2026):** (1) Der Deckel für Bots ohne Zeitbremse — das 95.
> Perzentil der Haltedauer plus 1 — wird aus den **gefundenen** Trades
> gerechnet, nicht als Maximum über das Raster; er ist keine Leckschranke, das
> Leck schliesst die Attribution je Position (**41.3, C2**). (2) Die Bedingung
> („keine vor Go-Live eröffnete Position mehr offen") wird im Selektionslauf
> **für den Gewinner auf dessen eigenen simulierten Positionen** ausgewertet;
> das Journal des Papierpfads ist dafür keine Quelle (**41.3, C3**). (3) Fables
> Berichtigung aus 24c, `purge_tage` als Schranke über das Raster zu bemessen,
> ist zurückgenommen und nie eingetragen worden (**41.2 B2, 41.3 C1**). Der
> Registertext oben bleibt zeichengleich.
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 2347–2348 (Marke; Marken-Zeile Z. 2347, Folgezeilen bis vor Leer-/Trennzeile)

```text
> ⭐ **16.6 PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.
```

Marken-Zeilen („> ⭐“) in 16.6: 2


## B3 R36, R60 (c), R64 (d)

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 10813 (Überschrift über R36)

```text
### 48.4 R36 — Präzisierung zu 24.2 und 45.5 (zwei Drawdown-Spalten; Konsistenzprüfung; Ausschnitt)
```

R36: Z. 10815, 1038 Zeichen

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 10815, R36 (ganze Zeile)

```text
> R36 — Präzisierung zu 24.2 und 45.5 (zwei Drawdown-Spalten; Konsistenzprüfung; Ausschnitt). zellen.csv trägt je (Zelle, Falte) kapital_drawdown_mtm_pct — den Kapital-Drawdown der Nebenbedingung auf der täglichen MtM-Reihe (1a) auf den Tagen des Benchmarks (3b (c)) — und kapital_drawdown_ereignis_pct — den ereignisindizierten Drawdown, berichtet, nicht bewertet (24.2). Die Spalte kapital_drawdown_pct wird durch die zwei benannten ersetzt, nicht umgedeutet. auswertung.py rechnet kapital_drawdown_mtm_pct aus tagesreihen/<zelle>.csv nach und endet bei Abweichung mit 2. Der Drawdown je Falte ist der Ausschnitt eines durchgehenden Kapitalpfads (29.3, 2a): gemessen innerhalb der Falte, mit dem Kapitalstand am Faltenbeginn als erstem Hochpunkt, ohne Neustart des Kapitals. Festlegung 3 und Abschnitt 8 („drei tiefste Falten-Drawdowns“, „Kapital-Drawdown je Falte“) beziehen sich auf kapital_drawdown_mtm_pct; der ereignisindizierte Wert steht daneben als eigene Zeile. Vollzieht K4j (1) und (2); (3) folgt mit 40.8 (h). F-5, M49, M62.
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11227 (Überschrift über R60)

```text
### 51.5 R60 — Bestätigung und Ergänzung zu R48 (d) (48.16) (mittlere Exposure: Registertext und Code; zwei Träger)
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11229, R60 (c) [bis vor (d); Zeichen 1105–1411 der Zeile; Block unter Z. 11227: ### 51.5 R60 —]

```text
(c) Der Zellen-Erzeuger schreibt beide Träger aus einer Rechnung: mittlere_exposure in zellen.csv ist je (Zelle, Falte) das Mittel der Spalte exposure der Tagesreihe dieser Zelle über die Tage der Falte. Die Abnahme nach R46 prüft diese Gleichheit, mit Gegenprobe. auswertung.py wird dafür nicht geöffnet.
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11313 (Überschrift über R64)

```text
### 52.2 R64 — Präzisierung zu R48 (d) (48.16) und zu R60 (b) und (c) (51.5) (über welche Tage die mittlere Exposure gemittelt wird)
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11315, R64 (d) [bis vor (e); Zeichen 1208–1550 der Zeile; Block unter Z. 11313: ### 52.2 R64 —]

```text
(d) „Über die Tage der Falte“ in R60 (c) lies: über die Tage nach (a), die in die Falte fallen (halboffen wie im Faltenplan; 2a). Der Wert des Gewinners in beta_bereinigung ist dann das mit der Zahl dieser Tage gewichtete Mittel seiner Werte je Selektionsfalte in zellen.csv; die Abnahme nach R46 prüft auch diese Gleichheit, mit Gegenprobe.
```


## B4 Register ab Abschnitt 16 — „Deckel“ (Umfeld 140)

Suchbereich: Z. 1820 bis Dateiende

Suchwort „Deckel“: 23 Treffer in 19 Zeilen; Z. 2309, 2316, 2331, 2336, 8548, 8818, 8862, 8870, 8874, 8880, 8890, 9494, 9521, 10713, 10822, 10859, 11175, 11461, 11471

Zusatzzählung, Kleinschreibung „deckel“: 1 Treffer in 1 Zeilen; Z. 8853

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 2309 (Treffer im Auszug: 1; Auszug reicht Z. 2306–2310)

```text
r
> `t3_supertrend` **13 Handelstage** (P95 = 11,21).
>
> ⚠️ **Ist am Deckeltag noch eine vor Go-Live eröffnete Position offen, beginnt
> die Best
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 2316 (Treffer im Auszug: 1; Auszug reicht Z. 2315–2317)

```text
 Jetzt ist es eine
**Bedingung am Bestand** mit der alten Frist als **Deckel**. Der Grund: die
feste Frist verschenkt Bestätigungstage, wenn der B
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 2331 (Treffer im Auszug: 1; Auszug reicht Z. 2330–2332)

```text
*rund vier Monate später als für die anderen acht**
> (91 Handelstage Deckel gegen 11 bis 16). Wer die neun Bestätigungsperioden
> nebeneinander l
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 2336 (Treffer im Auszug: 1; Auszug reicht Z. 2335–2337)

```text
ne Rücknahme (41.3 C1–C3, Fable 24d,
> TB-108, 25.09.2026):** (1) Der Deckel für Bots ohne Zeitbremse — das 95.
> Perzentil der Haltedauer plus 1 
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 8548 (Treffer im Auszug: 1; Auszug reicht Z. 8546–8548)

```text
rd nichts.*

## 41. Nachweis mit zwei Teilen, Resolver ohne Rückfall, Deckel statt Purge, Mutationsproben einzeln — die Einträge aus Fable 24b, 24
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 8818 (Treffer im Auszug: 1; Auszug reicht Z. 8817–8821)

```text
ter)** ·
Art: Berichtigung — ⭐⭐ **ZURÜCKGENOMMEN durch 41.3 (C1), der Deckel neu
gefasst durch 41.3 (C2)** · Quelle: 24c Abschnitt 4

> **Berichti
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 8862 (Treffer im Auszug: 1; Auszug reicht Z. 8862–8862)

```text
) und vor der Bestätigungsperiode keine Lücke, sondern Bedingung plus Deckel mit Attribution je Position (16.6). Eine Grösse, die eine Trainingsgr
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 8870 (Treffer im Auszug: 1; Auszug reicht Z. 8868–8871)

```text
ter geschrankte `purge_tage`") ist damit zurückgenommen."

**C2 (b) — Deckel für Bots ohne Zeitbremse aus gefundenen Trades** · Art:
Registertext 
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 8874 (Treffer im Auszug: 1; Auszug reicht Z. 8871–8874)

```text
nitt 1 ·
berichtigt 41.2 (B2)

> **Präzisierung zu 2d (Fassung 16.6), Deckel für Bots ohne Zeitbremse:** Das 95. Perzentil der Haltedauer wird aus
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 8874 (Treffer im Auszug: 1; Auszug reicht Z. 8874–8874)

```text
g 4; Tatsachennotiz mit Hash der Liste, Snapshot-Hash und Commit. Der Deckel ist keine Leckschranke — das Leck schliesst die Attribution je Positi
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 8880 (Treffer im Auszug: 1; Auszug reicht Z. 8878–8881)

```text
Gewinners. Kein Ergebnis.

**Stand, gemessen:** nicht gerechnet — der Deckel von `t3_supertrend` steht in
15.4 und 16.6 weiter mit dem Wert aus **
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 8890 (Treffer im Auszug: 1; Auszug reicht Z. 8890–8890)

```text
Gewinner auf dessen eigenen simulierten Positionen** ausgewertet; der Deckel ist je Bot eine Konstante über alle Zellen. Das Journal des Papierpfa
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 9494 (Treffer im Auszug: 1; Auszug reicht Z. 9494–9494)

```text
alpfad** (41.1 A12, 41.2 B3/B6/B7) — und mit ihm die neun Listen, der Deckel von `t3_supertrend` (41.3 C2), die Donchian-Eingabe, `messgroessen.js
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 9521 (Treffer im Auszug: 1; Auszug reicht Z. 9521–9522)

```text
Nr. 4 · 5.4 · 6 · 11 (am Ende, in 11.3) · 12 · 15.4 (2d, Tabelle des Deckels)
· 16.6 · 19 (zweimal: unter dem Registertext 5e und unter der Tabel
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 10713 (Treffer im Auszug: 2; Auszug reicht Z. 10713–10713)

```text
e Teilung nach Zahl der Bots je Zelle liesse Bots Zellen bewegen. Ein Deckel je Bot gehört nach 4.3 in das Netting (Rang 5), das nicht existiert; ein Deckel vor Netting wäre ein neuer, als willkürlich gekennzeichneter Register
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 10713 (Treffer im Auszug: 1; Auszug reicht Z. 10713–10714)

```text
eidungsvorlage: (a) so lassen — Empfehlung des Verfahrensprüfers; (b) Deckel je Bot vor Netting — Betreiber.
> *Quelle des Grundes:* (h) „die einz
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 10822 (Treffer im Auszug: 2; Auszug reicht Z. 10822–10822)

```text
er Spanne eröffnete simulierte Position des Gewinners mehr offen ist; Deckel je Bot nach 16.6/41.3 C2; eine am Deckeltag noch offene solche Position zählt nicht (Attribution je Position).
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 10859 (Treffer im Auszug: 1; Auszug reicht Z. 10859–10859)

```text
erzen des Zeitrahmens (1d, 4h, 1h). Umrechnung in Handelstage für den Deckel (16.6) und für L (15.3 (b)): 1d-Bots Balken = Tage (Krypto: Kalendert
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11175 (Treffer im Auszug: 1; Auszug reicht Z. 11175–11177)

```text
achtrag 29.09.2026, 12:25, und Umzug 29.09.2026, 20:48, Block 6). Ein Deckel je Bot vor dem Netting ist damit nicht registriert.

### 50.7 Was off
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11461 (Treffer im Auszug: 1; Auszug reicht Z. 11460–11461)

```text
eht nur „NYSE“ im Live-Pfad (53.9) | nächste Anfrage an Fable |
| 2 | Deckelfall (R68 (d)): Behandlung in den Gleichheitsproben nach R60 (c) und R
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11471 (Treffer im Auszug: 1; Auszug reicht Z. 11471–11471)

```text
ssetzung zu R64) wird nach R66 (e) im Lauf geprüft. Nr. 3 bleibt; der Deckelfall (R68 (d), hier Nr. 2) berührt die Probe dort. Nr. 4 und 8 bleiben
```


## B5 Register 52.5 — Tabellenzeile Nr. 3

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11370, 52.5 Nr. 3

```text
| 3 | R64 (c) und (d): Wache im Lauf mit Ausgang 2; Probe über das tagegewichtete Mittel in der Abnahme nach R46 | mit dem Zellen-Erzeuger |
```


## C1 Register 53.9 — letzte Tabellenzeile / letzter Absatz

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11454, 53.9 (Tabellenzeile; nächste Überschrift Z. 11456)

```text
| R66–R73, Zitate und Verweise | — | 98 Stellen gegen den Wortlaut gemessen (`docs/belege/TB-132/vormessung/v4_register_02c.md`). Sinngemäss treffen zehn: R72 (b) fasst den Benchmark-Tag enger als der Wortlaut von 23.3 (REG Z. 3933–3936), das ist der Inhalt der Präzisierung; R72 nennt im Kopf den Registertext 3b (c), R70 (c) setzt die Marke nur an die Tatsachennotiz (53.10 Nr. 8); „TB-47, Feld kalender“ steht nur in der Erläuterung unter 17.5 (REG Z. 2847); „Dafür“ steht in R60 (c) klein (REG Z. 11196); „Bauart R55, R64“ in R69 (b) meint Prüfungen mit Gegenprobe, die Bauart der beauftragten Änderung steht in R45 (REG Z. 10857); von einer Öffnung spricht unter R36, R37, R34 und R55 nur R55; „R54 an 7 (c)“ ist in R61 (b) ein Glied der Aufzählung, keine Zeile (REG Z. 11209); 24.6 (REG Z. 4471) berichtet eine Zählung in einer Messung; R56 (c) (REG Z. 11168) nennt drei Fälle, der von R73 ist keiner davon; 23.2, Grund 2 (REG Z. 3908) ist Deutung des Verfahrensprüfers | keine Stelle trifft nicht; die sinngemässen gehen zur Kenntnis an Fable (53.10 Nr. 9) |
```


## C2 Register 23.3 — Marken mit „R72“; R72 (b), R70 (c), R65 (a)

Unterabschnitt 23.3: Z. 3932–4014

Zeilen in 23.3 mit „R72“: 2; Z. 3947, 3978

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 3947–3948, 23.3 (erste Zeile beginnt mit „> ⭐“: ja; „R72“ in Z. 3947)

```text
> ⭐ **23.3, Registertext 3b (c) PRÄZISIERT durch R72 (53.7)** (Fable 02c R72, Unterpunkt (b), vom steuernden Chat nach R65 (a) bestimmt, TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 3978–3979, 23.3 (erste Zeile beginnt mit „> ⭐“: ja; „R72“ in Z. 3978)

```text
> ⭐ **23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse ERGÄNZT durch R72 (53.7)** (Fable 02c R72, TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11426, R72 (b) [bis vor (c); Zeichen 606–878 der Zeile; Block unter Z. 11424: ### 53.7 R72 —]

```text
(b) Benchmark-Tag des Bots im Sinn von 23.3, R64 und R66 ist ein Tag, an dem mindestens ein nach 3b (b) handelbares Symbol des Bots einen Kurs trägt; ausgenommen ist der Tag aus R71. Ein Handelstag, an dem kein handelbares Symbol einen Kurs trägt, ist kein Benchmark-Tag.
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11412, R70 (c) [bis Zeilenende; Zeichen 878–1979 der Zeile; Block unter Z. 11410: ### 53.5 R70 —]

```text
(c) Marken zu dieser Antwort, der alte Satz bleibt zeichengleich: 15.3 (a) — PRÄZISIERT durch R66, Unterpunkte (a) und (b). 15.3 (c) — PRÄZISIERT durch R66, Unterpunkt (c). 48.1 (R33) — PRÄZISIERT durch R68. 48.5 (R37) — PRÄZISIERT durch R68. 48.7 (R39) — ERGÄNZT durch R67; ERGÄNZT durch R69: R39 ist bestätigt. 48.16 (R48 (d)) — ERGÄNZT durch R72, Unterpunkt (c). 51.5 (R60) — PRÄZISIERT durch R69, Unterpunkt (c). 51.6 (R61) — PRÄZISIERT durch R70, Unterpunkt (a). 52.2 (R64) — ERGÄNZT durch R66 (zu (e)), PRÄZISIERT durch R68, durch R69, Unterpunkt (c), und durch R71 und R72, Unterpunkt (b) (Benchmark-Tag; erster Kurstag). 52.3 (R65) — PRÄZISIERT durch R70, Unterpunkt (a). 52.4, Zeile „R64 (52.2), zweite“ — ERGÄNZT durch R66, Unterpunkte (a) und (e). 52.4, Zeile „R64 (52.2) (a)“ — BERICHTIGT durch R69, Unterpunkt (c). 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse — BERICHTIGT durch R71 und ERGÄNZT durch R72; die Marke steht unter dem Blockzitat der Notiz (Vorbild 25.2). 27 — ERGÄNZT durch R73. Ohne Marke bleiben 24.2, 29.3 und 7 (c) zu R66 (Geltungsbereich oder Quelle des Grundes).
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 11337, R65 (a) [bis vor (b); Zeichen 81–639 der Zeile; Block unter Z. 11335: ### 52.3 R65 —]

```text
(a) Die Aufzählungen in R51 und R61 (b) wenden die Regel aus 34 an und schliessen sie nicht ab. Gibt ein Block einem benannten Ort ein „lies“, eine Ergänzung oder eine Bestätigung, trägt der Ort die Marke, auch wenn die Aufzählung des Blocks ihn nicht nennt; ausgenommen bleiben die Orte nach R61 (b), zweiter Satz. Eine Tabelle von Befunden ist keine Statusliste im Sinn von R61 (b), soweit ein Block den Befund einer Zeile ergänzt oder berichtigt. Eine Bestätigung trägt das Markenwort ERGÄNZT mit dem Zusatz, was bestätigt ist (Bauart der Marke an 46.9).
```


## D1 Register 45.1 (R1) und 48.20 (R52) — „Bestand behauptet“, „Fall“ mit Ordnungszahl (Umfeld 400)

Unterabschnitt 45.1: Z. 10203–10211

Suchwort „Bestand behauptet [45.1]“: 1 Treffer in 1 Zeilen; Z. 10205

Muster „Fall + Ordnungszahl (erster … sechzehnter, je Beugung) innerhalb 60 Zeichen [45.1]“: 1 Treffer in 1 Zeilen; Z. 10205

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 10205 (Treffer im Auszug: 2; Auszug reicht Z. 10205–10206) 45.1

```text
essen tut das nur `None` (`strategy_paths` legt 9 von 9 Ordner an), `False` nimmt den Modus-Zweig und meldet trotzdem 0 Unterschiede. Fables Beispiel `lambda: False` in 25e 3 war ungemessen — neunter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt". Handwerk als Beifang: Das Werkzeug zählt künftig die angelegten Ordner im Wegwerfbaum und meldet den durchlaufenen Zweig.
> *Quelle des Grundes:* Messung TB-109/TB-113, 
```

Unterabschnitt 48.20: Z. 10968–10974

Suchwort „Bestand behauptet [48.20]“: 1 Treffer in 1 Zeilen; Z. 10970

Muster „Fall + Ordnungszahl (erster … sechzehnter, je Beugung) innerhalb 60 Zeichen [48.20]“: 2 Treffer in 1 Zeilen; Z. 10970

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 10970 (Treffer im Auszug: 3; Auszug reicht Z. 10968–10970) 48.20

```text
### 48.20 R52 — Tatsachennotizen 29b

> R52 — Tatsachennotizen 29b. (a) 27b B3 („die datierten Kopien … sind im Repo committet“) war für vier von sechs Registerkopien falsch (TB-118 A3); zehnter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt“. (b) 45.5 (b) („für jede Zelle genau eine Zeile“) widersprach dem Datenvertrag; berichtigt in R33; elfter Fall. (c) Der Chat des Verfahrensprüfers ist zwischen 29a und 29b einmal verdichtet worden; die Registerteile 1–4, 27b und 25f wurden danach erneut vollständig gelesen; die Umzugsampel steht deshalb auf 🟡
```

Zählung im ganzen Register, Suchwort „Bestand behauptet“: 5 Treffer in 5 Zeilen; Z. 8510, 8513, 10205, 10792, 10970

Zählung im ganzen Register, Muster „Fall + Ordnungszahl neunter … sechzehnter (je Beugung) innerhalb 60 Zeichen“: 4 Treffer in 3 Zeilen; Z. 10205, 10792, 10970

Zusatz (nicht verlangt): Treffer beider Zählungen ausserhalb 45.1 und 48.20: 4

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 8510, 8513 (Treffer im Auszug: 2; Auszug reicht Z. 8506–8518) Zusatz, ausserhalb 45.1/48.20

```text
ist mit zwei Dateien erfüllt.
>
> **(c)** TB-94 → TB-96 für `messgroessen.json`. Angenommen; 39.8.
>
> Alle drei sind dieselbe Klasse wie die sechs Rücknahmen der ersten Woche: eine Tatsache über den Bestand behauptet statt als Voraussetzung genannt. Ich zähle sie mit.

⭐ **Er zählt sie mit** — dieselbe Klasse wie die sechs Rücknahmen der ersten
Woche: eine Tatsache über den Bestand behauptet statt als Voraussetzung
genannt.

⚠️⚠️ **Zu (c) — die Nummer ist wieder gerückt, und das gehört hierher, damit
die Ablage lesbar bleibt:** 39.8 hat „TB-94 → TB-96" berichtigt, und Fable hat
es angeno
```

**Fundstelle:** docs/VORREGISTRIERUNG_neuselektion.md, Z. 10792 (Treffer im Auszug: 2; Auszug reicht Z. 10792–10797) Zusatz, ausserhalb 45.1/48.20

```text
e x Falte), fuer ALLE Falten des Faltenplans, Bestaetigungsperiode eingeschlossen“), 15.3 (1c: Falten-Sharpe je Falte), 43-7. Der Vertrag stand vor R5 (b); R5 (b) war Kurzform ohne Nachlesen — elfter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt“. Kein Ergebnis.

> ⭐ **48.1 R33 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 45.
```


## D2 FABLE_ANTWORT_2026-10-01a — Z. 108; „25.2“; „14“ nahe R26/R30 (Umfeld 400)

**Fundstelle:** docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md, Z. 108 (ganze Zeile)

```text
6. **Zählung.** Der Satz in 25.2 und die „14“ in R26/R30 sind Ungenauigkeiten aus Fable-Texten. Ob sie in die Fehlerklasse zählen, zählst du.
```

Suchwort „25.2“: 10 Treffer in 8 Zeilen; Z. 19, 21, 50, 108, 116, 117, 131, 132

**Fundstelle:** docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md, Z. 19, 21 (Treffer im Auszug: 2; Auszug reicht Z. 17–25) Suchwort „25.2“

```text
ekt. Ihr Inhalt ist mir unbekannt; ich behandle sie wie `BACKLOG.md` (Frage 1, R56 (d)).

**Helfer, Suchläufe:** keine. **Mechanik (Skript):** Chatgrösse aus dem Sitzungsprotokoll; Kalenderzählung zu 25.2; Eszett-Zählung, Bytes und md5 dieser Datei.

**Grössen, die an 27.1 grenzen**, alle aus dem Register (27.3): Benchmark-Drawdowns und `DD_Toleranz` (3, 4.4, 25.4); „gefundene Trades/Jahr“ je Bot mit heutigen Parametern (3, 5.4); der Drawdown des T3-Bots mit und ohne Regimefilter (11.1); Symbolzahlen je Falte (16.1.1); Faltenzahlen (25.2, 32.2); Budgetanteile aus aufgezählten Stufentabellen (R24). **Ergebnisgrössen nach 27.1: keine. Weitere Grössen nach 27.1 kenne ich nicht.**

## Teil 0. Kenntnis

1. R28-Nebenbefund (`pruefe_abschni
```

**Fundstelle:** docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md, Z. 50 (Treffer im Auszug: 2; Auszug reicht Z. 48–52) Suchwort „25.2“

```text
h nicht als Bestand: sie hängt daran, wie der Index zählt, und die Herleitung liegt in `docs/belege/`. R57 schreibt deshalb die Zählweise fest, nicht die Zahl.

Die Zählweise steht schon im Register. 25.2 nennt für `rsi2_crypto` 150 Balken Vorlauf, Daten ab 17.08.2017, 137 Balken bis 31.12.2017; 32.2 nennt „warm ab“ 2018-01-14. Nachgerechnet (Kalender): Der 14.01.2018 ist der Balken mit **150 Balken davor**, also der 151. Der Satz in 25.2 „der 150. Balken liegt am 2018-01-14“ ist um eins daneben; der 150. Balken ist der 13.01. Die Sache trägt, der Satz nicht (R62 (a)).

### Frage 3 — (a) einverstanden; (b) ja, und die Lesart wird dadu
```

**Fundstelle:** docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md, Z. 108 (Treffer im Auszug: 1; Auszug reicht Z. 107–113) Suchwort „25.2“

````text
t, kann „steht nicht im Register“ nicht mehr aus eigener Suche sagen. Solche Sätze von mir sind dann Voraussetzungen, die du im Repo misst. In dieser Antwort steht keiner.
6. **Zählung.** Der Satz in 25.2 und die „14“ in R26/R30 sind Ungenauigkeiten aus Fable-Texten. Ob sie in die Fehlerklasse zählen, zählst du.

## Registerblock — zeichengleich kopierbar, nummeriert (ab R56)

```
R56 — Ergänzung zu 2
````

**Fundstelle:** docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md, Z. 116 (Treffer im Auszug: 1; Auszug reicht Z. 116–116) Suchwort „25.2“

```text
züglich der festen Fenster“ in R53 nennt die Bestandteile, nicht die Rechenart. Der Vorlauf des Bots ist der grösste Vorlauf über die Zellen, die nach Abschnitt 6 existieren. Dieselbe Zählweise trägt 25.2 mit 32.2: 150 Balken Vorlauf, warm ab dem Balken mit 150 Balken davor. Die Lesart in 50.5 und der Schlusssatz von 50.4 sind damit bestätigt. [Voraussetzung, zu messen: dass BB_PERIOD + L − 1 in backt
```

**Fundstelle:** docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md, Z. 117 (Treffer im Auszug: 1; Auszug reicht Z. 116–119) Suchwort „25.2“

```text
ines ab, gilt diese Definition, und die Formel folgt ihr.]
Quelle des Grundes: R53 („Der Scanbeginn einer Zelle liegt nie vor ihrem Vorlauf“), 25.3 (i) („am 1. Januar der Indikator-Vorlauf erfüllt“), 25.2, 32.2, 28.6, 26.2, Abschnitt 6. Kein Ergebnis.

R58 — Tatsachennotiz zu 25.3 (i) (Verhältnis der Marken 26.2 und R53). Bedingung (i) hat zwei Teile. „Im registrierten Datenhorizont des Bots“ ist präz
```

**Fundstelle:** docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md, Z. 131 (Treffer im Auszug: 2; Auszug reicht Z. 129–131) Suchwort „25.2“

```text
Quelle des Grundes: 34 (Marke am alten Ort, nach der Wiedergabe in 43.0), R51, Kopf von 48 („Vereinigung“), Wortlaut der genannten Orte, Abschnitt 14. Kein Ergebnis.

R62 — Tatsachennotizen 01a. (a) 25.2: „der 150. Balken liegt am 2018-01-14“ ist um einen Balken ungenau. Bei Daten ab 2017-08-17 und 137 Balken bis 2017-12-31 ist der 150. Balken der 2018-01-13; der 2018-01-14 ist der Balken mit 150 Balken davor. „Warm ab 2018-01-14“ (32.2) bleibt richtig; die Zählweise steht in R57. Der Satz in 25.2 bleibt zeichengleich. [Kalenderrechnung des Verfahrensprüfers; zu messen: dass die Tagesdatei im Januar 2018 lückenlos ist.] (b) Das Literal SOLL_DATENSTAND in research/registernachtrag_tb48/pruefe_a
```

**Fundstelle:** docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md, Z. 132 (Treffer im Auszug: 1; Auszug reicht Z. 131–133) Suchwort „25.2“

````text
REGISTER_KOPIE_ABSCHNITT_<nn>.md, Commit db108a6, sha256 b5804659…, KOPIE): 24 von 51 Abschnitten vollständig, die übrigen nicht. Er hat keinen Helfer und keinen Suchlauf benutzt.
Quelle des Grundes: 25.2, 32.2, R28, 50.1, Leseprotokoll 01a. Kein Ergebnis.
```
````

Muster „„14“ / "14" / ␠14␠“: 6 Treffer in 4 Zeilen; Z. 91, 106, 108, 128

Muster „R26 | R30“: 9 Treffer in 5 Zeilen; Z. 89, 91, 93, 108, 128

davon mit „R26“ oder „R30“ innerhalb von 400 Zeichen vor oder nach dem Treffer: 6; Z. 91, 106, 108, 128, 128, 128

**Fundstelle:** docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md, Z. 91 (Treffer „14“ im Auszug: 1; Fenster bis zur nächsten Nennung R26/R30 erweitert)

```text
 41.2 B3; R47 (die Marke in 5.4 zeigt auf 40.6, dort steht R47); R48 (h); R49 (c), (e); R31 (a), (e); R39, R43, R25.

Ein Beifang: R30 heisst „Ergänzung zu 14“, R26 schreibt „12: … ; 14: …“. Abschnitt 14 ist der Nulltest S-E1. Gemeint ist Sperrlistenpunkt 14. Berichtigt in R61 (c).

Handwerk, nur empfohlen: eine Indexzeile „Tag-Vorbedingungen“ (R15 (b), R27, R30, R29), damit sie vor dem Tag an einer S
```

**Fundstelle:** docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md, Z. 106, 108 (Treffer „14“ im Auszug: 2; Fenster bis zur nächsten Nennung R26/R30 erweitert)

````text
en sechs Änderungen) mit Commit im Repo liegt, weiss ich nicht. R56 (b) setzt es voraus.
4. **Abschnitt 34 und 10 nicht gelesen.** Die Markenregel kenne ich aus 43.0, den Wortlaut von Sperrlistenpunkt 14 aus dem Index.
5. **Preis der Probe „ein Chat je Anfrage“** (als Berater; der Prüfer hat nichts dagegen). Ein Chat, der nur die genannten Abschnitte öffnet, kann „steht nicht im Register“ nicht mehr aus eigener Suche sagen. Solche Sätze von mir sind dann Voraussetzungen, die du im Repo misst. In dieser Antwort steht keiner.
6. **Zählung.** Der Satz in 25.2 und die „14“ in R26/R30 sind Ungenauigkeiten aus Fable-Texten. Ob sie in die Fehlerklasse zählen, zählst du.

## Registerblock — zeichengleich kopierbar, nummeriert (ab R56)

```
R56 — Ergänzung zu 27.4 und 27.6 
````

**Fundstelle:** docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md, Z. 128 (Treffer „14“ im Auszug: 3; Fenster bis zur nächsten Nennung R26/R30 erweitert)

```text
om Index geführt: R27, R28, R30, R54 an 7 (c), R52 (b), R38, R41 an 41.2 B3, R47 an 5.4, R48 (h), R49 (c) und (e), R31 (a) und (e), R39, R43, R25. (c) Berichtigung: In R26 (47.9) und R30 (47.13) lies „14“ als „Sperrlistenpunkt 14 (Abschnitt 10)“; Abschnitt 14 des Registers ist der Nulltest S-E1 und nicht gemeint. [Voraussetzung, zu messen: der Wortlaut von Sperrlistenpunkt 14; hier nach REGISTER_INDEX.]
Quelle des Grundes: 34 (Marke am alten Ort, nach der 
```


## D3 FABLE_ANTWORT_2026-10-02c — Z. 41 und Z. 51

**Fundstelle:** docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md, Z. 41 (ganze Zeile)

```text
4. Zitate: Alle genannten Stellen sind in den neuen Fassungen berichtigt. Die zwei, die nicht treffen, sind meine Fehler: Ich habe in R68 eine ersetzte Fassung (2d aus 15.4) als Quelle des Grundes geführt, obwohl die Marke darunter in dem stand, was ich gelesen hatte, und ich habe „beide Träger“ in R60 (c) falsch gelesen. Ob das Fälle der Klasse „Bestand behauptet“ sind, zählt der steuernde Chat.
```

**Fundstelle:** docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md, Z. 51 (ganze Zeile)

```text
Grund: 1a und 2a sprechen von Handelstagen. Woher der Handelskalender des Laufs kommt, sagt 17.5 ausdrücklich: aus dem Paket, „Umgebung, nicht Eingabe“, im Lock. Mein R66 (a) hätte demselben Begriff eine zweite Quelle gegeben; das war dein Gegengrund, und er trifft. Ich kannte 17.5 nicht.
```


## D4 Register Abschnitte 51, 52, 53 — Fehlerklasse, Bestand behauptet, zwölfter, dreizehnter (Umfeld 200)

Suchbereich: Z. 11195–11471

Suchwort „Fehlerklasse“: 0 Treffer

Suchwort „Bestand behauptet“: 0 Treffer

Suchwort „zwölfter“: 0 Treffer

Suchwort „dreizehnter“: 0 Treffer

Zusatzzählung ohne Gross-/Kleinschreibung, Wortstamm „fehlerklasse“: 0 Treffer

Zusatzzählung ohne Gross-/Kleinschreibung, Wortstamm „bestand behauptet“: 0 Treffer

Zusatzzählung ohne Gross-/Kleinschreibung, Wortstamm „zwölft“: 0 Treffer

Zusatzzählung ohne Gross-/Kleinschreibung, Wortstamm „dreizehnt“: 0 Treffer

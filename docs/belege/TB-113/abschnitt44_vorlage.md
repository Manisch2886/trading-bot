## 44. Vollzug: `herkunft.py` im Modus, `auswertung.py` endet mit 2, 19 über den Laufbereich — Tatsachennotizen TB-111 und TB-112 (TB-113, 26.09.2026)

### 44.0 Was dieser Abschnitt ist

⭐ **Reines Eintragen von Tatsachen**, Bauart wie **43** (TB-110). Kein
Fable-Wortlaut ist neu hinzugekommen; eingetragen wird, **was zwei Aufträge
vollzogen haben**, deren Plan schon im Register steht:

- **TB-111** (Fable 25d (2)–(4), Register **43-1** und **43-4**): die zweite
  planmässige Öffnung von `herkunft.py` und die Umstellung von
  `auswertung.Abbruch` auf 2. TB-111 lief **auf einem eigenen Zweig**
  (`tb-111`, Worktree `~/trading-bot-tb111`, Eingang `f4d6d6d`, Commits
  `6cacfa4`, `6c98c38`, `1dcf273`, `49f0868`) und ist mit dem Auftrag dieses
  Abschnitts nach `main` zusammengeführt (`257e7db`, `git merge --no-ff`,
  `merge-tree` vorher rc 0, Schnittmenge der geänderten Dateien leer,
  `docs/belege/TB-113/0c_vorbedingungen.txt`).
- **TB-112** (Register **19**, **42.2 E2**, **42.3 F8**; Fable 25f O6): die
  Sauberkeitsprüfung der Startprüfung über den Laufbereich, nur unter dem
  Modus, mit der namentlichen Ausnahme des registrierten Protokolls
  (`e731207`, `9d711dc`, `e65e57c`, `21f4cac`, `af6042f`, direkt auf `main`).

Die Nummer hat der steuernde Chat vergeben
(`docs/auftraege/MAC_TB-113_zusammenfuehrung_tb111_register_44.md`, Freigabe
des Betreibers 26.09.2026, 14:28). **Die Kette zu 43:** 43.5 führt (1)
`auswertung.Abbruch` ⇒ 2, (2) die zweite Öffnung von `herkunft.py` und (7) die
Erweiterung von 19 als offen. **Alle drei sind hier als vollzogen eingetragen**
(44.1, 44.2). Die Zeilen in 43 bleiben zeichengleich; Marken darunter verweisen
hierher.

**Bauart je Eintrag:** Kennung (44-1 bis 44-12) · Art · Stand, gemessen im
genannten Ergebnisdokument und nach dem Zusammenführen in TB-113
(`docs/belege/TB-113/`), ohne Ergebnisgrössen (27.1) · Kette. Wo ein Wortlaut
aus einem Ergebnisdokument, dem Code oder einem früheren Registerstand
übernommen ist, ist er **eingesetzt, nicht abgetippt**; je Zitat ein `diff`
gegen die Quelle mit rc 0 (`docs/belege/TB-113/c2_zitate.txt`).

⭐ **Die Regel aus 34 gilt weiter:** Marken am alten Ort, der alte Satz
zeichengleich, `git diff --numstat` auf dieses Register mit `0` in der zweiten
Spalte. ⛔ **In Abschnitt 10 steht keine Marke** (Sonde, Prüfung (ii)).

### 44.1 TB-111 — `herkunft.py` im Modus und `auswertung.py` endet mit 2

*Eigene Fassung der Sitzung TB-111, gemessen
(`docs/ERGEBNIS_TB-111_herkunft_auswertung_oeffnung.md`, Belege
`docs/belege/TB-111/`); nach dem Zusammenführen nachgemessen in TB-113.*

**44-1 — 43-1 vollzogen: `auswertung.Abbruch` endet mit 2** · Art:
Tatsachennotiz (Vollzug) · Commit `6c98c38`

`class Abbruch(SystemExit)` setzt im eigenen `__init__` den Rückgabewert aus
`paths.RUECKGABEWERT_STARTPRUEFUNG`; die Zeile im Code, zeichengleich:
„⟦T:ausw:127|super().__init__(paths.RUECKGABEWERT_STARTPRUEFUNG)⟧". Der
Kommentar an der Klasse nennt die Regel aus 43-1, zeichengleich: „⟦T:ausw:121|Ausgaenge von `auswertung.py`: 0 oder 2, kein 1⟧".

- **12 Stellen** `raise Abbruch(`, zeichengleich wie vorher (TB-111 A3;
  nachgezählt in TB-113: 12).
- **Meldung byte-gleich:** An vier Brüchen (leere Rohergebnisse, fehlende
  Spalte, Zelle ausserhalb des Rasters, weniger als drei gemeinsame Tage) geht
  der Rückgabewert von 1 auf **2**; stderr und stdout sind vorher und nachher
  auf **denselben Eingaben** per `cmp` gleich (TB-111 C1,
  `c_proben_vorher.txt`/`c_proben_nachher.txt`). Der Fall ohne Bruch bleibt rc 0.
- Kein Test erwartete rc 1 von `auswertung.py`; kein Test wurde umgestellt.
  Neue Proben: `test_ersatzwerte.py` Teil G (6, mit Mutation und Gegenprobe).
- **Sichtbar geändert:** Die Meldung wird beim **Erzeugen** von `Abbruch`
  ausgegeben, nicht erst beim Prozessende; `str(e)` eines gefangenen `Abbruch`
  ist `"2"`, die Meldung steht in `e.meldung` (Frage an Fable, 44.3).

**Kette:** vollzieht **43-1** (Ergänzung zu 36.5); beantwortet damit die offene
Zeile der Marke unter **36.5** (TB-108) auch im Code. **Marken am alten Ort:**
unter **43-1** und unter der TB-110-Marke in **36.5**.

**44-2 — 43-4 vollzogen: die zweite planmässige Öffnung von `herkunft.py`** ·
Art: Tatsachennotiz (Vollzug) · Commit `6cacfa4`

- **Prüfansicht:** `main()` übergibt unter dem Modus `paths.DATA_DIR` an
  `block("pruefung", …)`, dieselbe Form wie `--anhaengen` seit TB-106; ohne
  Modus `None` wie vorher. Gemessen: im Modus rc 0, Datenstand `d9449faf…`/223.
- **`TB30A_BASE_DIR` unter dem Modus rc 2 vor dem Lesen:** eine neue Funktion
  `_ersatzwurzel_pruefen()` ist die **erste Zeile** von `commit()`,
  `register()` und `block()`; sie bricht unter dem Modus mit 2 ab, wenn die
  Variable gesetzt ist oder `BASE_DIR` von der eigenen Wurzel abweicht. Die
  Meldung beginnt, zeichengleich: „⟦T:herk:160|TB30A_BASE_DIR ist unter dem Selektionsmodus gesetzt⟧".
  Ein Lesehaken sieht dabei **0 Zugriffe** unter der Ersatzwurzel (Proben
  F-b bis F-b4 in `test_ersatzwerte.py`).
- **`_paths()` aus der eigenen Wurzel:** `paths.py` wird aus `_WURZEL` (dem
  Baum, in dem `herkunft.py` liegt) geladen, nicht mehr aus `BASE_DIR`.
- `EINGEFROREN`, `datenstand()`, `kette_pruefen()`, `anhaengen()` und
  `verankerung()` zeichengleich; der Import bleibt unter dem Modus unverändert
  (kein `paths` geladen). Neue Proben: Teil F (15, drei Mutationen je mit
  Gegenprobe).

**Kette:** vollzieht **43-4** (Fable 25d (2), (3)) — die zweite planmässige
Öffnung nach **42.3 F2** (erste: TB-106). Die Entscheidung in **37.4** („Nicht
öffnen"), ihre Berichtigung durch 42.3 F2 und die TB-110-Marke dort bleiben
zeichengleich. **Marken am alten Ort:** unter **43-4** und unter der
TB-110-Marke in **37.4**.

**44-3 — Befund A2b: die Modus-Abfrage las unter der Ersatzwurzel** · Art:
Tatsachennotiz (Befund, vor dem Vollzug gemessen)

Vor TB-111 lud `_paths()` die Datei `paths.py` aus `BASE_DIR/shared`, also
**unter** `TB30A_BASE_DIR`. Unter dem Modus mit einer nicht existierenden
Ersatzwurzel endete die Prüfansicht deshalb mit **rc 1**
(`ModuleNotFoundError`), **nicht mit 2**; schon die Frage „Modus?“ las unter
der Ersatzwurzel (TB-111 A2b, `docs/belege/TB-111/a_vormessung.txt`). Mit der
echten Wurzel als Ersatz fiel das nicht auf. Die Umstellung von `_paths()` in
44-2 ist die Folge; ohne sie wäre „erst 2, dann lesen“ (24d Abschnitt 3) nicht
erfüllbar gewesen. Kein Test setzte `TB30A_BASE_DIR` zusammen mit dem Modus.

**44-4 — Hash-Übergänge** · Art: Tatsachennotiz

| Datei bzw. Wert | vorher | nachher | durch |
|---|---|---|---|
| `research/vorregistrierung/herkunft.py` | `351f24c2d6a3a512dc1eb1a80b536b99d47c266db38f7dd93b9d1c0199397eef` | `5bbfc9e085d7ec70f43eb8aaaf63b957de27e3647023e143d17e9dd8c60448fa` | TB-111 `6cacfa4` |
| `research/vorregistrierung/auswertung.py` | `83c6bc3c9b683d0bfd9d8c445492060f93759a551d0dcf329b2bd21b0f1cc5a1` | `a864b2168a19405d5f1516a17146f78ef44bbca6f4f8d242c9ccb25f937467f3` | TB-111 `6c98c38` |
| `herkunft.register()` auf `tb-111` | `c85dd6c3…` | `e7d82547…` | TB-111 (nur `auswertung.py` hat sich von den elf Teilen geändert; `herkunft.py` steht nicht in `EINGEFROREN`) |
| `herkunft.register()` auf `main` | `c92900a8…` (nach Register 43) | **`469272dfbedf06492f1094bdb636295daeb76a9a7d4cc3fd98e89bcb400c0535`** | Zusammenführen `257e7db` (Register mit 43 **und** `auswertung.py` `a864b216…`; weder `e7d82547…` noch `c92900a8…`) |

⚠️ **Selbstbezug:** `register()` hasht dieses Register mit (42.5). Der Wert
**nach** dem Eintrag dieses Abschnitts kann hier nicht stehen; er steht im
Ergebnisdokument von TB-113.

**44-5 — Das gültige Abbild der Sperrliste: `e655c1c8…`** · Art:
Tatsachennotiz (36.6: „Das aktuelle Abbild steht selbst mit Hash im Register")

`research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26.json`,
**9192 B, `e655c1c8c8e576faa1de8021357354b1d9f0b44e9adae3a176c944087b3aacd9`**,
gezogen von TB-111 auf `6c98c38` (Commit `1dcf273`); 14 Punkte, 15
Pfadnennungen, Gruppen `bestimmt` 0, `eingefroren` 10. Es löst
`sperrliste_abbild_2026-09-25b.json` (`40ffe18d…`, 43.6) ab; das alte bleibt
(36.6).

- **Sonde gegen das alte `40ffe18d…`** auf dem Code-Stand von TB-111:
  Befund **genau** an Punkt **3, 5, 11, 12, 14** und in der Gruppe
  **`eingefroren`** — die Punkte, die `auswertung.py` oder `herkunft.py`
  nennen; kein anderer (`docs/belege/TB-111/d2_sonde_alt.txt`). Das ist der
  Befund `1` vor dem Tag nach **37.3**: beauftragt (Freigabe 25.09.2026,
  23:14), geschlossen durch ein **neues** Abbild.
- **Sonde gegen das neue, nach dem Zusammenführen auf `main`** (TB-113,
  `a_messung.txt`, `a_sonde_nach_merge.txt`): Pfad-Bestandteile **25/0/0**,
  (ii) **0**, Listentext wie bei Erzeugung. Das Abbild nennt Register-Z.
  894–1007; auf `main` steht der Listentext seit TB-110 in Z. 901–1014 —
  (ii) vergleicht den Listentext, nicht die Zeilen. rc 2 nur wegen der Punkte,
  die die Sonde nicht prüfen kann, wie in TB-110, TB-111 und TB-112.

**44-6 — Nach dem Zusammenführen gemessen (TB-113)** · Art: Tatsachennotiz

Am Merge-Commit `257e7db` (Baum `e44e1abf…` = Vorhersage von `merge-tree`):
Hashes `herkunft.py`/`auswertung.py` wie in 44-4; Benchmark-Tabelle im Modus im
Repo **und** in einem frischen Klon bytegleich **`64fb2912…`**; ohne Modus
acht Werkzeugausgaben bytegleich; Trockenlauf aller neun Bots im Modus 9 × rc
0; `herkunft_protokoll.jsonl` existiert nicht. Tests und Einzelheiten:
`docs/ERGEBNIS_TB-113_zusammenfuehrung_tb111_register_44.md`.

**Wechselwirkung TB-111 × TB-112, festgehalten:** Die in TB-112 erweiterte
Sauberkeitsprüfung (44.2) **bindet `research/vorregistrierung/auswertung.py`**
— die Datei liegt im Laufbereich und steht als Einzeldatei in
`ARBEITSBAUM_PFADE`. **`herkunft.py` bindet sie nicht:** Kein Lauf-Typ des
Laufbereichs lädt das Modul (Laufbereich 81 Module, TB-107 F1 = TB-112 A2; dort
0 Zeilen `herkunft.py`). Eine uncommittete Änderung an `herkunft.py` hielte die
Startprüfung also heute nicht an. Kommt das Modul in den Laufbereich (mit dem
Erzeuger, der `register()` und `commit()` ruft, 43-4), zeigt es die nächste
Laufbereichsmessung, und die Liste wird mit ihr erneuert (44-8).

### 44.2 TB-112 — Sauberkeit über den Laufbereich

*Eigene Fassung der Sitzung TB-112, gemessen
(`docs/ERGEBNIS_TB-112_19_laufbereich_db_sicherung.md`, Belege
`docs/belege/TB-112/`).*

**44-7 — E2 und F8 vollzogen** · Art: Tatsachennotiz (Vollzug) · Commit
`9d711dc`

- **`shared/paths.py` `ARBEITSBAUM_PFADE`: 15 Einträge** — `shared`,
  `strategies`, `requirements.lock` wie bisher, dazu die **12 Module des
  Laufbereichs ausserhalb** dieser Ordner **als einzelne Dateien** (11 unter
  `research/`, 1 unter `notifications/`). Einzeldateien statt Ordner, weil
  `research/vorregistrierung/ergebnisse/` Laufausgaben aufnimmt; der Preis: ein
  **neues** Modul im Laufbereich ist ungeprüft, bis Liste und Messung
  nachgezogen sind.
- **`REGISTRIERTE_PROTOKOLLE`** = genau
  `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl`, im
  `git status` als `:(exclude)`-Pfadangabe — **namentlich**, nicht zufällig
  (ohne die Ausnahme deckt heute kein geprüfter Pfad das Protokoll). `data/`
  bleibt ausgenommen wie in 19.
- **Nur unter dem Modus wirksam:** gelesen nur in `_pruefe_codeherkunft`, das
  nur im Modus-Zweig läuft; ohne Modus 0/0/0 `git`-, Paket- und
  `os.system`-Aufrufe, 144 Pfade zeichengleich, acht Werkzeugausgaben
  bytegleich.
- **Vorher/nachher:** Am Eingang lief der Import unter dem Modus mit einer
  uncommitteten Änderung in `benchmark.py`, `faltenplan_neun.py` oder
  `manual_close.py` durch (rc 0) — der Befund aus E2 beschrieb den Stand.
  Nachher: jede der 12 Dateien einzeln rc 2 mit Dateiname; Protokoll neu oder
  verändert rc 0; `data/` und eine Ausgabe unter `ergebnisse/` rc 0. Proben:
  `shared/test_arbeitsbaum_laufbereich.py` 26/26 (frischer Klon, Mutationen
  mit Gegenprobe).
- `shared/paths.py` `b8bb5cf97fdf2d5908cc7019cdd2a40c8d3085a509f86e335bf1adbf965961fd`
  ⇒ `1478d9a09895614e90246f781b3c4dc5979121318c7e9a79b3aded4a778dc404`.

**Kette:** vollzieht **42.2 E2** und **42.3 F8** und damit den Kasten
„Sauberkeit über den Laufbereich — beschlossen, nicht vollzogen“ in **19**;
schliesst **43.5 (7)**. Die Reihenfolge, die F8 verlangt (die Ausnahme vor der
Erweiterung im Register), ist eingehalten. **Marken am alten Ort:** unter dem
Kasten in **19**, unter „Stand, gemessen“ in **42.2 E2** und in **42.3 F8**.

**44-8 — Die Tatsachennotiz neben der Laufbereichsmessung** · Art:
Tatsachennotiz

E2 verlangt, zeichengleich: „⟦T:reg:8813|Die Liste der geprüften Pfade steht als Tatsachennotiz neben der Laufbereichsmessung und wird mit ihr am Tag-Commit erneuert.⟧"

**Das ist diese Datei:** `docs/belege/TB-112/arbeitsbaum_pfade.txt` (die 15
geprüften Einträge je mit Art, die eine Ausnahme, „nicht geprüft: `data/` und
alles übrige“), gelesen per Import ohne Modus am Stand `21f4cac`. Sie steht
neben `docs/belege/TB-112/a2_laufbereich.txt`, der Laufbereichsmessung, die
`shared/test_arbeitsbaum_laufbereich.py` als Gegenprobe liest. Am Tag-Commit
ersetzt die Tag-Messung beide.

**44-9 — Laufbereich 81 = TB-107** · Art: Tatsachennotiz

Laufbereich am Eingang von TB-112 (Werkzeug TB-104 D1, drei Lauf-Typen:
Trockenlauf aller neun, Benchmark im Modus, `auswertung.py`-Import): **81
Module, identisch mit TB-107 F1**, auch die Lauf-Typen je Modul; 12 davon
ausserhalb `shared/`/`strategies/`. Am Endstand von TB-112 erneut gleich.

**44-10 — Lese-Audit: 0 Code-Zugriffe ausserhalb der Liste; Randbefund 10
Eingaben** · Art: Tatsachennotiz (Befund offen bei Fable)

- In den Modus-Läufen (Repo und frischer Klon) liest **kein** Prozess eine
  `.py` unter der Codewurzel, die `ARBEITSBAUM_PFADE` nicht deckt (**0**).
- ⚠️ **Randbefund, nicht behoben:** Der Benchmark liest **10 versionierte
  Eingabedateien ausserhalb der Liste** — `research/vorregistrierung/ergebnisse/messgroessen.json`
  (durch die Sonde gedeckt, Gruppe `eingefroren`) und die neun
  `research/tb24_haltedauern/daten/<bot>_alle_trades.csv` (von nichts
  gedeckt; sie gehen über die Faltenlängen in den Plan ein, TB-95). E2 bindet
  Code, nicht Eingaben; eine uncommittete Änderung daran hielte die
  Startprüfung nicht an. **Offen bei Fable** (44.3).

**44-11 — Nebennotiz: db-Sicherung und `tb40_test_*`** · Art: Tatsachennotiz
(ausserhalb des Selektionsverfahrens)

Mit TB-112 kamen zwei Dinge, die das Verfahren nicht berühren und nur der
Vollständigkeit halber hier stehen: `docs/werkzeuge/db_sicherung/db_sicherung.sh`
sichert die Datenbanken der Bots lesend nach iCloud (Fable 25f O6; die
Cron-Zeile trägt der Betreiber ein), und
`research/universum_trockenlauf/test_universum_trockenlauf.py` räumt seine
Wegwerfordner selbst auf (vorher 18 je Lauf, nachher 0). Keine Datei des
Laufbereichs, der Sperrliste oder von `EINGEFROREN` ist dabei geändert.

### 44.3 Was offen bleibt

**44-12 — Fragen an Fable aus TB-109, TB-111 und TB-112, zeichengleich aus den
Ergebnisdokumenten:**

*TB-109* (`docs/ERGEBNIS_TB-109_nulltrades_ablagen_stummel.md`, Abschnitt 8):

> ⟦Z:e109:133⟧
> ⟦Z:e109:134⟧
> ⟦Z:e109:135⟧

*TB-111* (`docs/ERGEBNIS_TB-111_herkunft_auswertung_oeffnung.md`, Abschnitt 6):

> ⟦Z:e111:146⟧
> ⟦Z:e111:147⟧
> ⟦Z:e111:148⟧

*TB-112* (`docs/ERGEBNIS_TB-112_19_laufbereich_db_sicherung.md`, Abschnitt 6):

> ⟦Z:e112:206⟧
> ⟦Z:e112:207⟧
> ⟦Z:e112:208⟧

| | Sache | wohin |
|---|---|---|
| (1) | **Die Fragen oben**, dazu die Bestätigung der vorläufigen Berichtigung **43-11** (TB-109 Frage 1) | Fable |
| (2) | **Der Erzeuger** auf dem Signalpfad (43.5 (8)); mit ihm wird `herkunft.py` Teil des Laufbereichs (44-6) | Plan-Punkte 3 und 5 |
| (3) | **Das Faltenplan-Abbild** und die Faltenplan-Sonde (43.5 (8)) | Plan-Punkt 7 (TB-101) |
| (4) | Weiter offen aus 43.5: (3) die Kopie in `faltenplan_neun.py`, (4) der ERZEUGT-Block, (5) die Nullzeile im Erzeuger, (9) Fable 25f | wie in 43.5 |

**Aus 43.5 geschlossen:** (1) `auswertung.Abbruch` ⇒ 2 (44-1), (2) die zweite
Öffnung von `herkunft.py` (44-2), (7) 19 über den Laufbereich (44-7). (6) ist
in (1) oben aufgegangen.

### 44.4 Was hier ausdrücklich NICHT getan wurde

| | | gehört zu |
|---|---|---|
| ⛔ | **Keine `.py` geändert, nichts gerechnet** ausser den Nachmessungen nach dem Zusammenführen; die einzige Codeänderung auf `main` ist der Merge selbst (`257e7db`) | — |
| ⛔ | **Kein neues Abbild** — gültig bleibt `e655c1c8…` (44-5); Sonde vorher und nachher gleich (`docs/belege/TB-113/`) | — |
| ⛔ | **Kein alter Registersatz umgeschrieben** — Marken sind neue Zeilen, nichts entfernt | — |
| ⛔ | **Keine Marke in Abschnitt 10** | — |
| ⛔ | **Keine Antwort an Fable vorweggenommen**; der veraltete Satz im Docstring von `auswertung._abbruch_2` steht weiter im Code (TB-111 Frage 2) | 44.3 |
| ⭐ | **Sichtschutz 27.1:** keine Ergebnisgrösse des Selektionsraums | — |

**Die Marken am alten Ort** (je neue Zeilen, der alte Satz zeichengleich): 19
· 36.5 · 37.4 · 42.2 E2 · 42.3 F8 · 43-1 · 43-4.

*Dieser Abschnitt ist rein additiv: Er trägt die Tatsachen aus zwei Aufträgen
ein, die zwei Pläne aus 43 und einen Beschluss aus 42 vollzogen haben, und
entfernt nichts.*

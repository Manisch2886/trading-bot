# REGISTER-KOPIE Teil 4 von 4 — Abschnitte 44–46 — Commit 1e1145702ba8b6ee6ad4cecaecb75591463faa48 — 2026-09-27 — Original sha256 18e39ee29b9bd4f03a2ad4953c85c2e59558de3aaab26844ae58fb7590fca93c — KOPIE, nicht das Register

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
„super().__init__(paths.RUECKGABEWERT_STARTPRUEFUNG)". Der
Kommentar an der Klasse nennt die Regel aus 43-1, zeichengleich: „Ausgaenge von `auswertung.py`: 0 oder 2, kein 1".

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
  Meldung beginnt, zeichengleich: „TB30A_BASE_DIR ist unter dem Selektionsmodus gesetzt".
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

E2 verlangt, zeichengleich: „Die Liste der geprüften Pfade steht als Tatsachennotiz neben der Laufbereichsmessung und wird mit ihr am Tag-Commit erneuert."

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

> 1. **Stummel und Probe.** Bestätigst du die Berichtigung `None` statt `False`? Soll das Werkzeug zusätzlich prüfen, dass der Stummel den Nicht-Modus-Zweig nimmt (z. B. die angelegten Ordner im Wegwerfbaum zählen)? Heute würde ein falscher Stummel grün durchgehen.
> 2. **(iv) im Audit – welche Zugriffe?** Gebaut ist: **alle** lesenden Zugriffe auf die eigene Ablage, also die Verzeichnis-Öffnung beim Aufräumen **und** das Lesen des Ergebnisses darin. Damit ist (i) außerhalb 11. Der Auftrag erwartete 21, also nur die Verzeichnis-Öffnungen umgeordnet. Welche Lesart meint 25e 3 (b)? Und gehört die Tempfile-Probe von `mkdtemp` (von `tempfile` angelegt und sofort entfernt, ohne `mkdir`) ebenfalls zu (iv)?
> 3. **Grenze der Gegenprobe.** Sie prüft `__main__`-Blöcke, nicht `main()`-Funktionen, die mit `return 0` ohne Ausgabe enden könnten. Soll die Erweiterung auf `main()` für den Laufcode (TB-30b) kommen, oder reicht der Satz aus 25e, dass der Erzeuger für eine Zelle ohne Trades die Nullzeile schreibt?

*TB-111* (`docs/ERGEBNIS_TB-111_herkunft_auswertung_oeffnung.md`, Abschnitt 6):

> 1. **`datenstand(None)` im Modus** liest weiter `BASE_DIR/data`, mit oder ohne TB30A. Ich habe das wegen B3 (zeichengleich) nicht geändert. Die Aufrufer im Betrieb übergeben einen Pfad, und `block()` verlangt ihn im Modus. Soll `datenstand()` bei der nächsten Öffnung im Modus ohne Pfad ebenfalls mit 2 enden?
> 2. **Veralteter Satz im Docstring von `auswertung._abbruch_2`:** „(`Abbruch` oben endet mit 1 und bleibt, wie er ist.)“ ist seit Block C falsch. Die Freigabe lautete „Sonst nichts“, deshalb habe ich ihn **nicht** geändert. Soll er mit der nächsten Öffnung von `auswertung.py` gestrichen werden, oder als Tatsachennotiz stehen bleiben?
> 3. **`str(e)` eines gefangenen `Abbruch`** ist jetzt `"2"`, die Meldung steht in `e.meldung`. Heute liest niemand `str(e)`. Reicht das als Tatsachennotiz?

*TB-112* (`docs/ERGEBNIS_TB-112_19_laufbereich_db_sicherung.md`, Abschnitt 6):

> 1. **Eingaben außerhalb der Liste.** Das Audit findet 10 versionierte Dateien, die der Benchmark als **Daten** liest und die kein Pfad der Sauberkeitsprüfung deckt: `ergebnisse/messgroessen.json` (durch die Sonde gedeckt, Gruppe `eingefroren`) und die neun `research/tb24_haltedauern/daten/<bot>_alle_trades.csv` (von nichts gedeckt; sie gehen über die Faltenlängen in den Plan ein, TB-95). Eine uncommittete Änderung daran hielte die Startprüfung nicht an. Sollen die neun Listen in `ARBEITSBAUM_PFADE` (dann heißt die Liste „Laufbereich und seine versionierten Eingaben“) oder in das Abbild der Sperrliste? Oder bindet E2 bewusst nur Code?
> 2. **Pflege der Liste.** Die Liste ist eine Tatsache vom 26.09. und steht als Literal im Resolver; die Gegenprobe liest die Messdatei. Soll der Tag-Commit die Liste aus der Tag-Messung **erzeugen** (ein Schritt, der `paths.py` schreibt), oder bleibt es beim Literal mit Gegenprobe (heute gebaut)?
> 3. **Schlüssel-Muster der db-Sicherung.** Englisch nach 25f (`key|secret|token|api|passw`), 0 Treffer. Die Tabelle `zustand(schluessel, wert)` in `benachrichtigungen_schliessung.db` trifft es nicht; laut Code enthält sie nur `erstlauf_am` ⇒ Zeitstempel. Soll das Muster deutsche Wörter mitnehmen? Dann würde diese Datei zurückgehalten, bis der Betreiber entscheidet.

| | Sache | wohin |
|---|---|---|
| (1) | **Die Fragen oben**, dazu die Bestätigung der vorläufigen Berichtigung **43-11** (TB-109 Frage 1) | Fable |
| (2) | **Der Erzeuger** auf dem Signalpfad (43.5 (8)); mit ihm wird `herkunft.py` Teil des Laufbereichs (44-6) | Plan-Punkte 3 und 5 |
| (3) | **Das Faltenplan-Abbild** und die Faltenplan-Sonde (43.5 (8)) | Plan-Punkt 7 (TB-101) |
| (4) | Weiter offen aus 43.5: (3) die Kopie in `faltenplan_neun.py`, (4) der ERZEUGT-Block, (5) die Nullzeile im Erzeuger, (9) Fable 25f | wie in 43.5 |

**Aus 43.5 geschlossen:** (1) `auswertung.Abbruch` ⇒ 2 (44-1), (2) die zweite
Öffnung von `herkunft.py` (44-2), (7) 19 über den Laufbereich (44-7). (6) ist
in (1) oben aufgegangen.

> ⭐ **Beantwortet in Fable 26a, siehe 45** (TB-114, 26.09.2026): die Fragen
> aus TB-109, TB-111 und TB-112 in 45.1 bis 45.8, die Bestätigung von 43-11 in
> 45.1. Fragen und Tabelle oben bleiben zeichengleich.

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

## 45. Messbitten nach dem Tag, Reichweite (iv), Eingaben im Abbild, Pflege der Pfadliste, Abnahmebedingungen des Erzeugers — die Einträge aus Fable 26a (TB-114, 26.09.2026)

### 45.0 Was dieser Abschnitt ist

⭐ **Reines Eintragen von Registertext und Tatsachen**, Bauart wie **43**
(TB-110). Anlass ist die **erste gesammelte Tagesanfrage** an den
Verfahrensprüfer — Fable, zeichengleich: „Erste gesammelte Tagesanfrage."
— mit dem neuen Fable-Takt, einmal je Tag: „diese Antwort ist die erste im neuen Takt."
Sie beantwortet die Ergebnisse TB-109 bis TB-113 und die Fragen, die
**44.3** (44-12) zeichengleich sammelt.

**Quelle:**
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-26a_dreizehn_fragen_nullbefund_registerblock.md`
(md5 `e2a492165d44f6ee3d02eba99d2acf2c`, 22 331 Bytes, committet in TB-114
Schritt 0, `79c2dfa`), Abschnitt „Registerblock — zeichengleich kopierbar,
nummeriert", R1–R8. ⚠️ **Tatsachennotiz zur Herkunft (wie 41.0, 43.0):** Die
Datei hat der steuernde Chat übertragen; die Zitate hier sind zeichengleich
mit der Datei im Repo, ob diese zeichengleich mit Fables Ablage ist, ist nicht
gemessen.

**Die Kette zu 43 und 44:** 43.3 führt die Berichtigung „`None` statt
`False`" als **vorläufig**; 44.3 (1) führt die Fragen aus TB-109, TB-111 und
TB-112 als offen bei Fable. **Beide sind hier beantwortet** (45.1 bis 45.8).
Die Zeilen in 43 und 44 bleiben zeichengleich; Marken darunter verweisen
hierher. Die Nummer hat der steuernde Chat vergeben
(`docs/auftraege/MAC_TB-114_register_45_herkunft_pfadregel_tb24_listen.md`,
Freigabe des Betreibers 26.09.2026, ca. 16:30), nicht Fable.

**Bauart je Eintrag:** 45.1 bis 45.8 tragen je einen Baustein R1 bis R8
**zeichengleich** aus dem Codeblock am Ende der Fable-Antwort, samt seiner
„Quelle des Grundes", als Blockzitat, **eingesetzt, nicht abgetippt**; je
Baustein ein `diff` gegen die Quelle mit rc 0
(`docs/belege/TB-114/a2_r_diff.txt`). Nichts ist umformuliert. Darunter steht
je Eintrag die Kette (wohin die Marke am alten Ort zeigt). 45.9 ist eine
Tatsachennotiz des steuernden Chats, 45.10 die Liste des Offenen; der Vollzug
in TB-114 folgt als 45.11.

**Einordnung von R6 — Fables drittes „Unsicher", zeichengleich:**
„Ob R6 eine Ergänzung zu 27 oder zu 7.1 ist — ich schlage 27 vor (es geht um Lesen nach dem Tag); Handwerk der Einordnung."
Eingeordnet ist R6 als Ergänzung zu **27**, wie sein Titel sagt; die Marke
steht **an beiden Orten** (am Ende von 27 und unter 7.1), weil 7.1 die Regel
ist, auf die R6 sich für „Bleibt oder Geht" beruft.

⭐ **Die Regel aus 34 gilt weiter:** Marken am alten Ort, der alte Satz
zeichengleich, `git diff --numstat` auf dieses Register mit `0` in der zweiten
Spalte. ⛔ **In Abschnitt 10 steht keine Marke** (Sonde, Prüfung (ii)).

### 45.1 R1 — Marke an 43.3 (Bestätigung)

> **R1 — Marke an 43.3 (Bestätigung).** Die Berichtigung „`selektionsmodus = lambda: None` statt `lambda: False`" ist von Fable bestätigt (26a 3 (1)). Grund: Der Stummel soll das Werkzeug so laufen lassen wie am Stand TB-52; gemessen tut das nur `None` (`strategy_paths` legt 9 von 9 Ordner an), `False` nimmt den Modus-Zweig und meldet trotzdem 0 Unterschiede. Fables Beispiel `lambda: False` in 25e 3 war ungemessen — neunter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt". Handwerk als Beifang: Das Werkzeug zählt künftig die angelegten Ordner im Wegwerfbaum und meldet den durchlaufenen Zweig.
> *Quelle des Grundes:* Messung TB-109/TB-113, Prüfprinzip A5. Kein Ergebnis.

**Kette:** bestätigt **43-11** (43.3, „vorläufig, von Fable nicht
bestätigt"); die Überschrift und der Text von 43.3 bleiben zeichengleich, die
Marke steht darunter. Die Zweigprüfung im Werkzeug ist Beifang, kein Auftrag.

### 45.2 R2 — Ergänzung zu 42 (Klasse (iv), Reichweite)

> **R2 — Ergänzung zu 42 (Klasse (iv), Reichweite).** Klasse (iv) umfasst jeden lesenden Zugriff eines Laufs auf seine eigene Zwischenablage: die Verzeichnis-Öffnung beim Aufräumen und das Lesen des darin abgelegten Ergebnisses. Die Probe, die `tempfile` beim Anlegen einer Ablage selbst macht (kein `mkdir` im Protokoll, sofort entfernt), ist Umgebung — Klasse (ii) — und wird als Tatsachennotiz geführt.
> *Quelle des Grundes:* 25b (Definition von (iv): angelegt mit `mkdtemp`, vom Lauf selbst gelesen, entfernt oder im Beleg), 25e 3 (b). Kein Ergebnis.

**Kette:** ergänzt **42.2 E1** (Klasse (iv)); beantwortet TB-109 Frage 2
(44.3). Marke unter 42.2 E1.

### 45.3 R3 — Ergänzung zu 30.2 (3) / 33.3 (Abbild der Sperrliste, Gruppe `eingefroren`)

> **R3 — Ergänzung zu 30.2 (3) / 33.3 (Abbild der Sperrliste, Gruppe `eingefroren`).** Versionierte Dateien, die ein Lauf des Laufbereichs als Daten liest und die kein Code sind, gehören mit ihrem Hash in die Gruppe `eingefroren` des Abbilds — namentlich die neun Listen `research/tb24_haltedauern/daten/<bot>_alle_trades.csv`, aus denen der Faltenplan seine Faltenlängen herleitet (TB-95). Die Startprüfung nach 19/E2 bindet Code; das Abbild bindet Eingaben. Dass eine Änderung der Listen den Plan und damit dessen Abbild änderte, ersetzt die Bindung der Eingabe nicht: Der Nachweis verlangt die Eingabe bytegleich und gelesen (24c).
> *Quelle des Grundes:* 25b (Klasse „Code" gegen Eingaben), 24c (zwei Teile des Nachweises), 24c B1. Kein Ergebnis.

**Kette:** ergänzt **30.2 (3)** und **33.3**; beantwortet TB-112 Frage 1
(44.3). Marken unter 30.2 und 33.3. Die Voraussetzung dafür, dass die Gruppe
`eingefroren` diese Pfade aufnehmen kann, ist in **45.9** gemessen; der
Vollzug steht in **45.11**.

> ⭐ **Zwei Erzeuger; Bindung der Listen: siehe 46.3** (Fable 27a R12, TB-117,
> 26.09.2026). Zitat und Kette oben bleiben zeichengleich.

### 45.4 R4 — Ergänzung zu 19 / 42.2 E2 (Pflege von `ARBEITSBAUM_PFADE`)

> **R4 — Ergänzung zu 19 / 42.2 E2 (Pflege von `ARBEITSBAUM_PFADE`).** Die Liste der Pfade der Sauberkeitsprüfung steht als Literal im Resolver; eine Gegenprobe liest die Laufbereichsmessung aus der Messdatei und vergleicht. Am Tag-Commit wird der Laufbereich neu gemessen; weicht die Messung von der Liste ab, ist das ein Befund: Die Liste wird vor dem Tag nachgezogen, nie durch ihn. Die Liste wird nicht aus der Messung erzeugt.
> *Quelle des Grundes:* Prüfprinzip B3 (ein Gegenbeweis gegen eine bewegliche Referenz prüft nichts), 25b E5 (Messung am Tag-Commit). Kein Ergebnis.

**Kette:** ergänzt **19** und **42.2 E2**; beantwortet TB-112 Frage 2 (44.3).
Heute gebaut ist genau diese Form (Literal in `shared/paths.py`, Gegenprobe
in `shared/test_arbeitsbaum_laufbereich.py` gegen
`docs/belege/TB-112/a2_laufbereich.txt`, 44-8). Marken unter 19 (unter der
TB-113-Marke) und unter 42.2 E2.

### 45.5 R5 — Abnahmebedingungen des Erzeugers

> **R5 — Abnahmebedingungen des Erzeugers (Ergänzung zu 24b A12 / Plan-Punkt 10).**
> (a) Die Laufbereichsmessung nach dem Einbau des Erzeugers enthält `research/vorregistrierung/herkunft.py`; `ARBEITSBAUM_PFADE` ist danach nachgezogen (R4). Bis dahin ist `herkunft.py` am committeten Stand über die Sperrliste (Punkte 11/12) und das Abbild gebunden; die Lücke im Arbeitsbaum ist als Tatsachennotiz in 44 benannt.
> (b) `zellen.csv` enthält für jede Zelle des Rasters genau eine Zeile; die Zeilenzahl ist gleich der Zahl der Zellen; eine Zelle ohne Trades trägt die Nullzeile (Sharpe 0 nach Registertext 1c, leere Trade-Liste), nie nichts. Eine fehlende Zeile ist ein Befund über den Erzeuger, kein Ausgang.
> (c) `herkunft.datenstand()` endet unter dem Modus ohne übergebenen Pfad mit 2; Beifang der nächsten Öffnung von `herkunft.py`, kein eigener Auftrag.
> *Quelle des Grundes:* 24b A10 (kein Fallback unter dem Modus), 25e (2) (null Trades ist ein Wert), 36.5, 26a 5. Kein Ergebnis.

**Kette:** ergänzt **41.1 A12** und die Zeile **(5)** in **42.6** (der
Erzeuger auf dem Signalpfad); beantwortet TB-109 Frage 3 (b) und TB-111
Frage 1 (c) (44.3) und Fables Punkt (5) zur Wechselwirkung (a). **(c) ist in
TB-114 vollzogen** (Block B, 45.11). Marken unter 41.1 A12 und in 42.6
Zeile (5).

### 45.6 R6 — Ergänzung zu 27 (Messungen auf dem Selektionsraum nach dem Tag)

> **R6 — Ergänzung zu 27 (Messungen auf dem Selektionsraum nach dem Tag).** Nach dem signierten Tag werden auf dem Selektionsraum dieses Durchgangs nur die Messungen gerechnet, die vor dem Tag als Messbitte registriert sind (R7). Jede weitere Messung auf denselben Zellen ist ein Versuch: Sie wird im Versuchsregister geführt und zählt in N des nächsten Durchgangs. Keine Messung nach dem Tag — registriert oder nicht — ändert Bleibt oder Geht; das sagt 7.1. Registrierte Messbitten sind Bericht, nicht Tor.
> *Quelle des Grundes:* 7.1, Festlegung 11, Literatur (Story-telling und Data Snooping nach dem Ergebnis, López de Prado; „every backtest must be reported with all trials"). Kein Ergebnis.

**Kette:** ergänzt **27**; beruft sich auf **7.1**. Registertext **vor** dem
Tag, weil er am Tag danach schon gelten muss (Fable 26a 3 (6)). Marken am
Ende von 27 und unter 7.1.

### 45.7 R7 — Liste der registrierten Messbitten für nach dem Tag (Anhang zu R6), Stand 26a

> **R7 — Liste der registrierten Messbitten für nach dem Tag (Anhang zu R6), Stand 26a.**
> 1. PBO je Bot über alle Zellen (CSCV, S = 16) — 25f V3.
> 2. MinTRL und Lo-Standardfehler je Gewinnerzelle — 25f V7.
> 3. Netto-Sharpe der Gewinnerzellen unter 0,5 %, 1,0 % und 1,6 % Roundtrip — 25f K2.
> 4. Implizite Kelly-Fraktion je Bot gegen die feste Positionsgrösse — 25f P5.
> 5. Krypto-Umkehr-Bots nach Liquiditätsdrittel des Universums — 25f S8.
> 6. Block-Bootstrap-Band je Gewinnerzelle für den Vergleich mit der Bestätigungsperiode — 25f O2.
> Verfahrensmessungen nach 27.2 (vor dem Tag zulässig, nicht Teil dieser Liste): Adjustierungsstand und Herkunft der 150 Aktienreihen im Snapshot; Nutzung von Preisniveaus je Bot; ob alle neun Bots die geschlossene Kerze lesen; ob TB-85 die Kette Erzeuger → Auswertung deckt. Ergänzungen dieser Liste vor dem Tag sind zulässig und werden datiert; nach dem Tag ist die Liste geschlossen.
> *Quelle des Grundes:* R6. Kein Ergebnis.

**Kette:** Anhang zu **45.6**. Die vier Verfahrensmessungen nach 27.2 sind
nicht Teil der Liste; drei davon sind in 45.10 als offen geführt. Ergänzungen
vor dem Tag werden datiert angehängt, hier oder in einem späteren Abschnitt
mit Marke hier.

> ⭐ **Nr. 7: siehe 46.7 (a)** (Fable 27a R16 (a), TB-117, 26.09.2026). Zitat
> und Kette oben bleiben zeichengleich.

### 45.8 R8 — Tatsachennotizen 26a

> **R8 — Tatsachennotizen 26a.**
> (a) `auswertung._abbruch_2`: Der Docstring sagt „`Abbruch` … endet mit 1"; falsch seit TB-111, stehen geblieben wegen der Freigabe „sonst nichts"; Streichung mit der nächsten planmässigen Öffnung.
> (b) `str(e)` eines gefangenen `Abbruch` ist `"2"`, die Meldung steht in `e.meldung`; im Laufbereich (81 Module, Stand TB-113) liest kein Aufrufer `str(e)` — Suchmuster in der Notiz nennen, Messung am Tag-Commit wiederholen.
> (c) db-Sicherung (25f O6): Schlüssel-Muster `key|secret|token|api|passw`, 0 Treffer über 12 Datenbanken; die Tabelle `zustand(schluessel, wert)` in `benachrichtigungen_schliessung.db` enthält laut Code nur `erstlauf_am`; deutsche Wörter nicht aufgenommen — Betrieb, nicht Lauf.
> (d) N = 653 (Register 9): Was das Versuchsregister nicht zählt und nicht rekonstruieren kann, steht dort in 3.4 und 5.1–5.4; ein Verweis aus Register 9 auf Abschnitt 5 des Versuchsregisters wird nach dem Tag eingetragen. Folge für die Lesart: N_nominal ist eine Untergrenze.
> (e) Berichtigung zu 25f A2 und C3 Entscheidung 8: Das Zellenbudget steht in 16.4 (g)–(m); offen ist nur der Vollzug im Code (16.11, Zeile 3; Stufe IV). Fables Satz „keinen Abschnitt gefunden" war aus dem Gedächtnis; Fables Regel: Vor „steht nicht im Register" wird im Text gesucht, nicht erinnert, und das Suchwort genannt.
> *Quelle des Grundes:* Messungen TB-111, TB-112, TB-113, 26a 3 (a)/(b). Kein Ergebnis.

**Kette:** (a) und (b) beantworten TB-111 Fragen 2 und 3, (c) TB-112 Frage 3
(44.3). ⛔ **(a) ist nicht vollzogen:** Der Docstring von
`auswertung._abbruch_2` bleibt bis zur nächsten planmässigen Öffnung von
`auswertung.py` stehen. ⛔ **(d) ist nicht vollzogen:** Der Verweis aus
Register 9 kommt **nach** dem Tag; in 9 steht deshalb heute keine Marke.

### 45.9 Tatsachennotiz des steuernden Chats zu R3 — zwei Pfadregeln

Fables erstes „Unsicher", zeichengleich:
„Ob die Gruppe `eingefroren` des Abbilds heute Dateien ausserhalb `research/vorregistrierung/` aufnehmen kann"

**Gemessen am 26.09.2026 über die Brücke am Stand `0df8c64`, nur lesend** (vom
steuernden Chat; in TB-114 am Stand `79c2dfa` wiederholt, beide Dateien
unverändert):

- `herkunft.register()` löst jeden Eintrag von `EINGEFROREN` mit
  `os.path.join(_HIER, rel)` auf, also immer relativ zu
  `research/vorregistrierung/` — die Zeile, zeichengleich:
  `pfad = os.path.normpath(os.path.join(_HIER, rel))`
- `shared/sperrlistensonde.py::_aufloesen` löst einen Eintrag nur dann
  relativ zu `research/vorregistrierung/` auf, wenn er kein `/` enthält oder
  mit `ergebnisse/` beginnt; sonst repo-relativ (Feld `pfadregel` im Abbild) —
  die Zeile, zeichengleich:
  `if "/" not in pfad or pfad.startswith("ergebnisse/"):`
- **Folge:** Ein Eintrag für `research/tb24_haltedauern/daten/…` wäre in einem
  der beiden Programme nicht auffindbar. `register()` führt eine nicht
  gefundene Datei in `fehlend` und rechnet ohne sie weiter:
  `fehlend.append(rel)`
- Die zehn heutigen Einträge sind von der Abweichung nicht betroffen: jeder
  hat entweder kein `/` oder das Präfix `ergebnisse/`, beide Regeln liefern
  denselben Ort.
- **Vollzug:** Block B von TB-114 (45.11).

### 45.10 Was offen bleibt

| | Sache | wohin |
|---|---|---|
| (1) | Die drei Verfahrensmessungen nach 27.2: ob alle neun Bots die **geschlossene Kerze** lesen; **Adjustierungsstand und Herkunft der 150 Aktienreihen** im Snapshot; ob **TB-85** die Kette Erzeuger → Auswertung deckt | TB-115 |
| (2) | **Der Erzeuger** auf dem Signalpfad, mit den Abnahmebedingungen aus 45.5 (a) und (b) | Plan-Punkte 3 und 5 |
| (3) | **Das Faltenplan-Abbild** und die Faltenplan-Sonde | Plan-Punkt 7, TB-101 |
| (4) | **Stufe IV** (Leiter-Skript, 16.11 Zeile 3; Fable 26a 2 (a), R8 (e)) | Stufe IV |
| (5) | R8 (a) Docstring `auswertung._abbruch_2`; R8 (d) Verweis in Register 9 | nächste Öffnung von `auswertung.py`; nach dem Tag |

**Die Marken am alten Ort** (je neue Zeilen, der alte Satz zeichengleich):
7.1 · 19 · 27 · 30.2 · 33.3 · 41.1 A12 · 42.2 E1 · 42.2 E2 · 42.6 Zeile (5)
· 43.3 · 44.3. ⛔ Keine in Abschnitt 10, keine in 9.

> ⭐ **Beantwortet und fortgeschrieben in 45.11 und 46** (Fable 27a, TB-117,
> 26.09.2026). Tabelle und Text oben bleiben zeichengleich.

### 45.11 R11 — Abbild gültig; Tatsachennotiz zum Abbruch TB-114 (Fable 27a, TB-117, 26.09.2026)

> **R11 — 45.11 (Abbild gültig; Tatsachennotiz zum Abbruch TB-114).** Gültiges Abbild ist `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb114.json`, `5e5ad109…` (10 805 B, 14 Punkte, `eingefroren` 19, HEAD `0b7ab4b`); Sonde dagegen 34/0/0, (ii) 0, gemessen TB-114 C und TB-115 0b (vorher = nachher). Tatsachennotiz: TB-114 endete in Block C mit Abbruchkriterium, weil der Auftrag gegen das alte Abbild `e655c1c8…` „die neun neuen Einträge in `eingefroren`" als Befund erwartete; die Sonde meldet Zuwachs in `EINGEFROREN` gegen ein altes Abbild nur mittelbar über den Hash von `herkunft.py` (Punkte 11/12). Zwei Ursachen: eine ungemessene Erwartung im Auftrag (Regel des steuernden Chats: Erwartungen an ein Werkzeug nur mit Fundstelle) und eine einseitige Sonde (R9). Der Abbruch war regelgerecht; nichts wurde repariert. Nach dem Bündel (R9, R10, R14, R15) folgt ein neues Abbild nach 37.3.
> *Quelle des Grundes:* Messungen TB-114/TB-115, Nachtrag 6d (Abbruchkriterium führt zu Abbruch, nie zu Rückfrage). Kein Ergebnis.

**Kette:** Vollzug der in **45.0** angekündigten Nummer 45.11 — nicht durch
TB-114 (Abbruch in Block C, `e07fefd`/`90307cb`), sondern mit Fables Antwort
27a (T114-2) in TB-117. Das Abbild ist seit TB-114 unverändert; gemessen am
Eingang von TB-117 (`753ec11`, `docs/belege/TB-117/0b_ausgang.txt`): sha256
`5e5ad1097909b3531e19b238153cabc46e7b551bb25e369ddc6735836e71cd06`, Sonde
dagegen 34/0/0. Der Satz in R11 „Nach dem Bündel (R9, R10, R14, R15) folgt
ein neues Abbild nach 37.3" wird in TB-117 Block E vollzogen; das Ergebnis
steht in **46.11**. Bis dahin gilt `5e5ad109…`. Die Marke unter 45.10 zeigt
hierher und auf 46.

## 46. Sonde zweiseitig, `fehlend` im Modus, zwei Erzeuger, Snapshot-Bindung, Herkunftsprüfung in `auswertung.py` — die Einträge aus Fable 27a (TB-117, 26.09.2026)

### 46.0 Was dieser Abschnitt ist

⭐ **Reines Eintragen von Registertext und Tatsachen**, Bauart wie **45**
(TB-114). Anlass ist die Tagesanfrage 27a an den Verfahrensprüfer
(`FABLE_ANFRAGE_2026-09-27a_tagesanfrage_tb114_tb115.md`) zu den Ergebnissen **TB-114** (Register 45,
dritte Öffnung von `herkunft.py`, Abbruch in Block C) und **TB-115** (drei
Verfahrensmessungen, nur lesend). Fables Einordnung, zeichengleich:
„**Ein Bündel, eine Freigabekarte je Sperrlistendatei** (`herkunft.py`, `auswertung.py`, Sonde), dann ein Abbild."

**Quelle:**
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-27a_sonde_zweiseitig_herkunft_in_auswertung.md`
(md5 `d4367c65a9dcad4b28cceb6f50706d59`, 30 836 Bytes, committet in TB-117
Schritt 0, `753ec11`), Abschnitt „Registerblock — zeichengleich kopierbar,
nummeriert", R9–R17. ⚠️ **Tatsachennotiz zur Herkunft (wie 41.0, 43.0,
45.0):** Die Datei hat der steuernde Chat übertragen; die Zitate hier sind
zeichengleich mit der Datei im Repo, ob diese zeichengleich mit Fables Ablage
ist, ist nicht gemessen.

**Die Kette zu 45:** R11 ist die in 45.0 angekündigte Nummer **45.11** und
steht deshalb am Ende von 45, nicht hier. R9, R10, R12 bis R17 stehen als
**46.1 bis 46.8** in der Reihenfolge des Codeblocks. 45.7 (R7) bekommt mit
R16 (a) eine Nummer 7 der Liste; 45.5 (R5) mit R16 (b) einen Punkt (d); 45.8
(R8 (a)) wird mit der Öffnung von `auswertung.py` in TB-117 vollzogen (46.11).
Die Nummer 46 hat der steuernde Chat vergeben
(`docs/auftraege/MAC_TB-117_wachen_vor_dem_tag.md`, Freigabe des Betreibers
26.09.2026, ca. 22:20), nicht Fable.

**Bauart je Eintrag:** 45.11 und 46.1 bis 46.8 tragen je einen Baustein
**zeichengleich** aus dem Codeblock am Ende der Fable-Antwort, samt seiner
„Quelle des Grundes", als Blockzitat, **eingesetzt, nicht abgetippt**; je
Baustein ein `diff` gegen die Quelle mit rc 0
(`docs/belege/TB-117/a2_r_diff.txt`). Nichts ist umformuliert. Darunter steht
je Eintrag die Kette (wohin die Marke am alten Ort zeigt). 46.9 ist eine
Lesart des steuernden Chats, 46.10 die Liste des Offenen; der Vollzug in
TB-117 folgt als 46.11.

⭐ **Die Regel aus 34 gilt weiter:** Marken am alten Ort, der alte Satz
zeichengleich, `git diff --numstat` auf dieses Register mit `0` in der zweiten
Spalte. ⛔ **In Abschnitt 10 steht keine Marke** (Sonde, Prüfung (ii)); die
Tatsachennotiz „an Punkt 8" aus R15 (a) steht deshalb in **46.6**, mit
Verweis auf Punkt 8. ⛔ **In Abschnitt 9 steht keine Marke.**

### 46.1 R9 — Ergänzung zu 40.8 (e) (Sonde, zweite Seite)

> **R9 — Ergänzung zu 40.8 (e) (Sonde, zweite Seite).** Die Sonde prüft die Gruppe `eingefroren` aus dem Abbild heraus (Abbild → Dateien) **und** vergleicht die heutige Menge `herkunft.py::EINGEFROREN` mit der Gruppe `eingefroren` des Abbilds (Liste → Abbild). Ein Eintrag, der in einer der beiden Mengen fehlt, ist ein Befund ⇒ 1, mit Nennung des Eintrags und der Seite. Die Gruppen kommen weiter aus dem Abbild; neu ist nur der Vergleich der Mengen.
> *Quelle des Grundes:* Prüfprinzip C4 (eine Prüfung, die nicht sagt, gegen was sie prüft; zweiseitiger Nachweis), Messung TB-114 Block C. Kein Ergebnis.

**Kette:** ergänzt **40.8 (e)** (die Sonde liest die Gruppen aus dem Abbild);
beantwortet T114-2 (Fable 27a Abschnitt 2). Marke in 40.8 als eigene
Tabellenzeile direkt unter der Zeile (e). **Fables erstes „Unsicher",
zeichengleich:**
„Ob `sperrlistensonde.py` selbst im Abbild oder auf der Sperrliste steht — wenn ja, folgt der Sonden-Öffnung ein Abbild nach 37.3; wenn nein, nicht. Nicht gemessen."
**Gemessen (TB-117, am Stand `753ec11`, nur lesend):** Der Listentext von
Abschnitt 10 nennt `sperrlistensonde` 0-mal; das Abbild `5e5ad109…` nennt die
Sonde einmal, und zwar nur als Parser im Feld `erzeugt`
(`"parser": "shared/sperrlistensonde.py::lies_abschnitt_10"`), in keinem
Punkt und in keiner Gruppe. Das neue Abbild nach dem Bündel folgt trotzdem, weil
`herkunft.py` und `auswertung.py` geöffnet werden (R11). Vollzug in TB-117
Block B (46.11).

### 46.2 R10 — Ergänzung zu 41.1 A10 (`herkunft.py`, `fehlend`)

> **R10 — Ergänzung zu 41.1 A10 (`herkunft.py`, `fehlend`).** `register()` und `block()` enden unter dem Modus mit 2, wenn `fehlend` nicht leer ist; die Meldung nennt die fehlenden Einträge. Ohne Modus bleibt `fehlend` ein Feld und eine Druckzeile der Prüfansicht. Die neun TB-24-Listen werden nicht in `ARBEITSBAUM_PFADE` aufgenommen (R3: die Sauberkeitsprüfung bindet Code); eine fehlende Liste wird über `register()` ⇒ 2, die Sonde (Gruppe `eingefroren`) und den Abbruch in `faltenplan.py` sichtbar. Umsetzung mit der nächsten Öffnung von `herkunft.py`, zusammen mit dem Nachtrag im Modulkopf (R17 a).
> *Quelle des Grundes:* 24b A2 (ein Wert, der so tut, als wäre er gemessen), 41.1 A10. Kein Ergebnis.

**Kette:** ergänzt **41.1 A10** (kein Fallback unter dem Modus); beantwortet
T114-1. Marke unter dem „Stand, gemessen" von A10. Der Nachtrag im Modulkopf
(R17 (a), 46.8) gehört zu derselben Öffnung. Vollzug in TB-117 Block C
(46.11).

### 46.3 R12 — Tatsachennotiz zu 40.6 / 41.1 A12 / 45.3 (zwei Erzeuger; Bindung der Listen)

> **R12 — Tatsachennotiz zu 40.6 / 41.1 A12 / 45.3 (zwei Erzeuger; Bindung der Listen).** Es gibt zwei Erzeuger: den **Listen-Erzeuger** auf dem Signalpfad (40.6, 41.1 A12; heute `research/tb24_haltedauern/positionen_holen.py`, `--ziel`, Einmal-Schreibsperre), der die Trade-Listen vor dem Tag einmal auf dem Snapshot neu erzeugt, und den **Zellen-Erzeuger** (Plan-Punkt 10, R5), der `zellen.csv`, `tagesreihen/` und `herkunft.json` schreibt. `herkunft.py::EINGEFROREN` bindet die neun heutigen Listen unter `research/tb24_haltedauern/daten/`, bis die Listen nach 40.6 neu erzeugt sind und `faltenplan.py` sie über die registrierte Pfadkonstante liest; dann treten die neuen Listen an ihre Stelle, die alten bleiben als historischer Stand liegen und verlassen `EINGEFROREN` (gebunden wird, was gelesen wird, R3); ihre Hashes stehen in `docs/belege/TB-114/`. Die Öffnung von `herkunft.py` dafür erfolgt mit der Neuerzeugung, nicht davor. Der Pfad der neuen Listen ist bis dahin nicht registriert (TB-114 B3).
> *Quelle des Grundes:* 40.6, 41.1 A12, R3, R5. Kein Ergebnis.

**Kette:** Tatsachennotiz zu **40.6**, **41.1 A12** und **45.3**; beantwortet
T114-3 und berichtigt die Lesart der Anfrage („folgt dann dem Pfad des
Erzeugers (R5)" — gemeint ist 40.6). Marken am Ende von 40.6, unter der
TB-114-Marke von 41.1 A12 und am Ende von 45.3. ⛔ **Nicht vollzogen und nicht
Teil von TB-117:** Die Listen werden nicht neu erzeugt, `EINGEFROREN` behält
die neun heutigen Listen.

### 46.4 R13 — Tatsachennotizen zum Snapshot und zu den Eingaben (neben 5e, 28, 31; Punkt 10; 16.4)

> **R13 — Tatsachennotizen zum Snapshot und zu den Eingaben (neben 5e, 28, 31; Punkt 10; 16.4).**
> (a) `XAUTUSDT_1h.csv` im Datenstand `d9449faf…` endet auf einer Teilkerze (letzte Kerze `2026-08-30 18:00`, geschrieben 18:39:01 UTC, 21 min vor Kerzenschluss). Kein Lauf liest sie, weil vier Ausschlussmengen das Symbol streichen: `shared/symbols_config.py::EXCLUDE_SYMBOLS`, `messgroessen.py::AUSGESCHLOSSEN`, `faltenplan_neun.py::KRYPTO_AUSSCHLUSS`, `benchmark.py:145`. Wache: eine Probe liest die vier Mengen ein und verlangt Gleichheit (Handwerk, keine Sperrlistennähe). Zusammenlegung auf einen Ort mit der jeweils nächsten planmässigen Öffnung, nicht vor dem Tag.
> (b) 175 Dateien des Datenstands (150 Aktien-1d, 25 Krypto-1h) haben keinen feineren Zeugen für `rand_letzte`; ihr Rand ist durch Schreibpfad und Zeitstempel belegt (TB-115 M1: Aktien letzte Kerze `2026-09-01`, geschrieben 02.09. 04:20–04:22 UTC; Krypto gemeinsamer Stand 15.09. 09:00–09:59 UTC). Der Beleg gilt als Tag-Vorbedingung erfüllt; keine laufende Prüfung eingefrorener Daten.
> (c) Adjustierungsstand der 150 Aktienreihen: split- und dividendenbereinigt, rückwärts, Schnitt je Symbol am letzten Ex-Tag vor dem 02.09.2026 (`yf.download(…, auto_adjust=True)`, kein `Adj Close`); Abrufcode nicht versioniert, nächstliegend `0f6491b`; yfinance-Fassung nicht belegbar; keine Regel eines Aktien-Bots nutzt ein absolutes Preisniveau (P1 = 0 Fundstellen, TB-115 M2 (c)). Schliesst die Verfahrensmessung D3 aus R7.
> (d) Stufe 3 der Zuteilungskaskade (`shared/zuteilung.py`, Punkt 10) reiht nach dem Median von `close × volume` über 20 Tage über Symbole hinweg; `volume` ist split-bereinigt, `close` split- und dividendenbereinigt — das Dollar-Volumen eines Dividendenzahlers ist in der Vergangenheit um das Produkt seiner späteren Ausschüttungen zu klein ausgewiesen. Stufe 3 entscheidet bei `volatility_breakout`, `elliott_wave_stocks`, `turtle_soup_stocks` (keine Signalspalte) bei leerem Buch; Krypto nicht betroffen. Eigenschaft der eingefrorenen Eingabe; **keine Änderung vor dem Tag** (die Korrektur bräuchte Daten, die der Snapshot nicht hat; Ersatzgrössen änderten die Bedeutung der Regel). Wie oft Stufe 3 entscheidet, ist Messbitte R7 Nr. 7.
> (e) Papierpfad: Die beiden Elliott-Bots messen die Signalfrische (`SIGNAL_FRESHNESS_HOURS`) an `pd.Timestamp.utcnow()` statt an `entscheidungskerze.laufbeginn()`; keine Kerzenwahl, wirksam nur an der 48-h-Grenze. Betrieb, mit der nächsten Öffnung von `forward_test.py`, nach dem Tag.
> (f) Tatsachennotiz zu 16.4 (Evidenz der Leiter): `forward_test.py` legt `entry_price`/`stop_price` (Elliott auch `target_price`) als absolute Zahlen ab und vergleicht sie in späteren Läufen mit neu bereinigten Reihen; über einen Ex-Tag oder Split hinweg passen Niveau und Reihe nicht mehr zusammen. Betroffen sind die Bots mit Stop (`volatility_breakout`, `elliott_wave_stocks`) und `pnl_pct` aller vier Aktien-Bots. Der Selektionspfad ist frei davon. Behebung im Betrieb nach dem Tag, vor dem ersten Stufenwechsel der Leiter, der sich auf Papier-Evidenz stützt.
> *Quelle des Grundes:* Messungen TB-115 M1/M2, 31.3, 37.3, Plan-Punkt 6, 16.4 (i). Kein Ergebnis.

**Kette:** beantwortet F1-1 bis F2-3 (Fable 27a Abschnitt 3, M1 und M2).
Marke unter **16.4** („Prüfung vor dem Tag") für (f). Die Notizen (a) bis (e)
stehen hier und nicht an 5e, 28, 31 und Punkt 10, weil diese Stellen
Registertext bzw. Sperrlistentext sind (Punkt 10 liegt in Abschnitt 10, dort
steht keine Marke). ⭐ **(a) Die Probe** (vier Ausschlussmengen gleich) wird
in TB-117 Block E gebaut, ausserhalb der Sperrlistendateien; die Mengen
werden nur gelesen (46.11). ⛔ **(d) ändert vor dem Tag nichts** an
`shared/zuteilung.py`; die Messbitte steht als R7 Nr. 7 in 46.7 (a).

### 46.5 R14 — Ergänzung zu 12 und 36.5 (Herkunftsprüfung in `auswertung.py`)

> **R14 — Ergänzung zu 12 und 36.5 (Herkunftsprüfung in `auswertung.py`).** `auswertung.py` liest `<wurzel>/<bot>/herkunft.json` für jeden Bot und endet mit 2, wenn die Datei fehlt, wenn der Commit-Hash vom Tag-Commit (5e, `TB_SELEKTIONSCOMMIT`) abweicht, wenn der Datenstand-Hash vom registrierten Datenstand `d9449faf…` abweicht, wenn der Register-Hash von `herkunft.register()` zur Laufzeit der Auswertung abweicht, oder wenn die neun `herkunft.json` untereinander abweichen. Der Bericht trägt Commit, Datenstand und Register-Hash in seinem Kopf. Der Schreiber von `herkunft.json` (Zellen-Erzeuger) prüft sich nicht selbst; der Auswerter prüft ihn. Umsetzung: eine Öffnung von `auswertung.py` (Punkte 3/5/14) vor dem Tag, zusammen mit der Streichung aus R8 (a); Hash-Übergang nach 37.3.
> *Quelle des Grundes:* Docstring von `auswertung.py` Z. 51–52 (nennt `herkunft.json` als Teil des Vertrags), Abschnitt 12 (Vertragsbruch ⇒ Abbruch), 36.5, 25c (1) (Register-Code-Widerspruch ist 2), Prüfprinzip A8. Kein Ergebnis.

**Kette:** ergänzt **12** (Vollständigkeitstest; `auswertung.py` bricht bei
jeder Verletzung des Datenvertrags ab) und **36.5** (Ausgänge); beantwortet
F3-3. Marken am Ende von 12 und am Ende von 36.5. Was R14 ohne Modus
bedeutet, sagt R14 nicht; die Lesart des steuernden Chats steht in **46.9**.
Vollzug in TB-117 Block D (46.11), zusammen mit R8 (a) (45.8).

### 46.6 R15 — Ergänzung zu den Tag-Vorbedingungen (Snapshot-Bindung) und Tatsachennotiz zu Punkt 8

> **R15 — Ergänzung zu den Tag-Vorbedingungen (Snapshot-Bindung) und Tatsachennotiz zu Punkt 8.**
> (a) Das Abbild der Sperrliste führt in der Gruppe `eingefroren` zusätzlich `snapshots/<hash>/MANIFEST.json` und die Snapshot-Kopien von `config/top25_symbols.txt` und `config/sp500_top150.txt` (heute bytegleich mit dem Repo, `3afc95a4…`, `6acba892…`). Punkt 8 bleibt im Wortlaut (bindet die Repo-Dateien); Tatsachennotiz an Punkt 8: unter dem Modus liest der Lauf die Snapshot-Kopien, gebunden über das Abbild.
> (b) Tag-Vorbedingung: `snapshot.py --pruefen` endet am Tag-Commit mit UNVERAENDERT (rc 0), Beleg im Tag-Ordner. Die Startprüfung vergleicht `TB_SELEKTIONSHASH` weiter mit dem im MANIFEST notierten Hash; sie rechnet den Snapshot nicht nach — den gerechneten Datenstand trägt die Kette (R5 (d), R14).
> *Quelle des Grundes:* R3 (das Abbild bindet Eingaben), Prüfprinzip A8 (Selbstauskunft ist keine Wache), 25f A3 (keine Wache doppelt). Kein Ergebnis.

**Kette:** beantwortet F3-1 und F3-2. ⭐ **Tatsachennotiz an Punkt 8 der
Sperrliste (Abschnitt 10), hier statt dort, weil in 10 keine Marke steht:**
Punkt 8 bleibt im Wortlaut und bindet die Repo-Dateien
`config/top25_symbols.txt` und `config/sp500_top150.txt`; unter dem Modus
liest der Lauf die Snapshot-Kopien, gebunden über das Abbild (Gruppe
`eingefroren`, R15 (a)). (a) wird in TB-117 Block C vollzogen
(`herkunft.py::EINGEFROREN`) und im neuen Abbild (Block E) gebunden
(46.11). (b) ist Tag-Vorbedingung und wird am Tag-Commit gemessen, nicht in
TB-117.

### 46.7 R16 — Ergänzungen zu R5 und R7

> **R16 — Ergänzungen zu R5 und R7.**
> (a) R7 Nr. 7: Wie oft entscheidet Stufe 3 der Zuteilungskaskade je Aktien-Bot und Falte, und wie oft wäre die Rangfolge unter Stückzahl × Split-Faktor eine andere? Bericht, kein Tor (R13 d).
> (b) R5 (d): Der Zellen-Erzeuger schreibt in `herkunft.json` den mit `herkunft.datenstand(<Snapshot-Datenordner>)` **gerechneten** Datenstand-Hash, nicht den im MANIFEST notierten, dazu Commit und `herkunft.register()`.
> *Quelle des Grundes:* R6/R7, R14, R15. Kein Ergebnis.

**Kette:** (a) ist **Nr. 7** der Liste in **45.7** (R7), vor dem Tag
ergänzt und damit nach 45.7 zulässig, datiert 26.09.2026 (Fable 27a);
Marke unter 45.7. (b) ist Punkt **(d)** zu **45.5** (R5); gilt für den
Zellen-Erzeuger, der noch nicht gebaut ist.

### 46.8 R17 — Tatsachennotizen 27a

> **R17 — Tatsachennotizen 27a.**
> (a) Modulkopf von `herkunft.py` beschreibt `register` als Hash über „die Registerdatei, die Module dieses Ordners und die vorab berechneten Tabellen"; seit TB-114 B3 gehören die neun TB-24-Listen dazu. Nachtrag mit der nächsten Öffnung (R10).
> (b) Testannahmen TB-114 nach Grundsatz 40: `test_ersatzwerte.py` E-bM (Mutation der ersten Wache endet an der zweiten mit 2 statt 0; Ort `block` weiter verlangt), `test_sperrlistensonde.py` 8a (10 ⇒ 19), H7f (25 ⇒ 34); die Fassungen am Stand `77147f7` brechen genau dort (60/61, 57/59).
> (c) M1 (TB-115): 9/9 Bots entscheiden auf der geschlossenen Kerze — Papierpfad über `entscheidungskerze.lade` (je 1 Aufruf, 0 Abrufe an der Schicht vorbei), Selektionspfad über den Rand des Datenstands. Schliesst die Verfahrensmessung aus R7. Randbefund R2 (Endgültigkeit des yfinance-Schlusskurses um 20:15 UTC) ist Betrieb, nicht gemessen.
> (d) M3 (TB-115): Die Sonde bindet von der Kette Datenstand → Zellen-Erzeuger → `zellen.csv` → `auswertung.py` → Bericht nur Glied 4 samt Importen und Tabellen; Glieder 1, 3 und 5 werden über R14 und R15 gebunden, Glied 2 mit dem Zellen-Erzeuger (R5). Damit ist die vierte Verfahrensmessung aus R7 („deckt TB-85 die Kette") beantwortet: nein.
> *Quelle des Grundes:* Messungen TB-114/TB-115. Kein Ergebnis.

**Kette:** (a) wird mit der Öffnung von `herkunft.py` in TB-117 Block C
vollzogen (46.11). (b) bis (d) sind Tatsachen; (c) und (d) schliessen die
Verfahrensmessungen aus 45.7 (R7) und damit Zeile (1) von 45.10.

### 46.9 Lesart des steuernden Chats zu R14 ohne Modus — von Fable zu bestätigen (Tatsachennotiz)

R14 nennt die fünf Abbruchbedingungen, sagt aber nicht, ob sie auch ohne
Selektionsmodus gelten. Der steuernde Chat hat im Auftrag eine Lesart
festgelegt und für Fable benannt, zeichengleich
(`docs/auftraege/MAC_TB-117_wachen_vor_dem_tag.md`, Freigabe des Betreibers
26.09.2026, ca. 22:20):

„R14 unter dem Modus vollständig: Jede der fünf Bedingungen endet mit 2. Ohne Modus liest `auswertung.py` `herkunft.json`, wenn vorhanden, und zeigt Commit, Datenstand und Register-Hash im Kopf des Berichts, bricht aber nicht ab. Grund: Ohne Modus laufen Beispieldaten und Tests, und `beispieldaten.py` schreibt Nullwerte (Z. 210 ff.). Dieselbe Bauart wie R10 (`fehlend` ⇒ 2 nur unter dem Modus)."

⚠️ **Vorläufig, bis Fable bestätigt.** TB-117 setzt diese Lesart in Block D
um; weicht Fables Antwort ab, ist das eine weitere Öffnung von
`auswertung.py`.

### 46.10 Was offen bleibt

| | Sache | wohin |
|---|---|---|
| (1) | **Leiter-Lesarten** zu 16.4 (TB-116, fünf Stellen L1–L5) | Fable |
| (2) | **Der Listen-Erzeuger** nach 40.6 (41.1 A12, 45.5, 46.3) | Plan-Punkte 3 und 5 |
| (3) | **Der Zellen-Erzeuger** (Stufe V; 45.5, 46.7 (b)) | Stufe V |
| (4) | **Stufe IV** (Leiter-Skript, 16.11 Zeile 3) | Stufe IV |
| (5) | Bestätigung der Lesart **46.9** | Fable |
| (6) | R15 (b) `snapshot.py --pruefen` als Tag-Vorbedingung | am Tag-Commit |

**Die Marken am alten Ort** (je neue Zeilen, der alte Satz zeichengleich):
12 · 16.4 · 36.5 · 40.6 · 40.8 (e) · 41.1 A10 · 41.1 A12 · 45.3 · 45.7 ·
45.10. ⛔ Keine in Abschnitt 10, keine in 9.

### 46.11 Vollzug in TB-117 (Tatsachennotiz)

**Gemessen in TB-117, 26./27.09.2026** (Belege `docs/belege/TB-117/`, Ergebnis
`docs/ERGEBNIS_TB-117_wachen_vor_dem_tag.md`). Eingang `8b342ab`, Schritt 0
`753ec11`, Block A `4c5615d` (45.11 und 46.0–46.10). Freigabe des Betreibers
26.09.2026, ca. 22:20 (Auswahlkarte, wörtlich im Auftrag). Kein
Abbruchkriterium ausgelöst.

**Hash-Übergänge nach 37.3:**

| Block | Datei | vorher | nachher | Commit | vollzieht |
|---|---|---|---|---|---|
| B | `shared/sperrlistensonde.py` | `f88e54ee…` | `98c02e0e…` | `42ef509` | R9 (46.1) |
| C | `research/vorregistrierung/herkunft.py` | `ed521ac1…` | `c6c13388…` | `ff2f254` | R10 (46.2), R15 (a) (46.6), R17 (a) (46.8) |
| D | `research/vorregistrierung/auswertung.py` | `a864b216…` | `8ec45123…` | `852f253` | R14 (46.5), Lesart 46.9, R8 (a) (45.8) |

**`herkunft.register()`:** `5acb4c19…` (Eingang) ⇒ `6bcb4f58…` (nach
Block A) ⇒ `b8f2cc33…` (nach Block C; 23 Teile, `fehlend` leer) ⇒
`e87a4d8e…` (nach Block D, gemessen vor diesem Eintrag). Der Wert nach
diesem Eintrag kann hier nicht stehen (er hasht diesen Text); er steht im
Ergebnis.

**B (R9):** Die Sonde vergleicht zusätzlich die heutige Liste
`herkunft.py::EINGEFROREN` mit der Gruppe `eingefroren` des Abbilds; ein
Eintrag nur auf einer Seite ist Befund 1 mit Eintrag und Seite
(„Liste → Abbild fehlt“ bzw. „Abbild → Liste fehlt“). Gegen das alte Abbild
`e655c1c8…` meldet sie die neun TB-24-Listen „nur in der Liste“ — die Zeile,
die R11 als fehlend beschreibt.

**C (R10, R15 (a), R17 (a)):** `register()` und `block()` enden unter dem
Modus mit 2, wenn `fehlend` nicht leer ist (je eigene Fundstelle, Meldung
nennt die Einträge); ohne Modus unverändert. `EINGEFROREN` führt zusätzlich
`snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/MANIFEST.json`
und die beiden Kopien `…/config/top25_symbols.txt` und
`…/config/sp500_top150.txt` des Snapshots aus Register 18 — versioniert,
repo-relativ, in `herkunft.py` und Sonde gleich aufgelöst; **keine dritte
Pfadauflösung**. Die `config/`-Kopien stecken im Snapshot-Hash (225 Dateien),
nicht im Datenstand (223). Die Tatsachennotiz an Punkt 8 steht in 46.6.

**D (R14, Lesart 46.9, R8 (a)):** `auswertung.py` liest `herkunft.json`
unter dem Modus für alle neun Bots und endet mit 2 bei jeder der fünf
Bedingungen; der registrierte Datenstand steht als Konstante
`REGISTRIERTER_DATENSTAND` mit Fundstelle Register 18. Ohne Modus: nur
Anzeige. Der Kopf des Berichts trägt Commit, Datenstand und Register-Hash.
Der Satz „`Abbruch` … endet mit 1“ ist berichtigt; damit ist Zeile (5) von
45.10 für R8 (a) erledigt.

**Gültiges Abbild ab jetzt** (nach R11 „nach dem Bündel ein neues Abbild“):
`research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json`,
sha256 `46f0ad5d1d83a253baa5523f5657881e0d825cebd734f24a42ef5d4fa74f281f`
(11 432 B, 14 Punkte, `eingefroren` 22 = `EINGEFROREN`, HEAD `852f253`).
Sonde dagegen 37/0/0, (ii) 0, Mengenvergleich 22/22 ohne Befund. Es ersetzt
`5e5ad109…` (45.11); nichts ist überschrieben.

**Sonde gegen `5e5ad109…`, jeder Eintrag zugeordnet:** Punkte 3, 5, 14 und
Gruppe `eingefroren`: `auswertung.py` (Block D); Punkte 11, 12:
`herkunft.py` (Block C); Gruppe `eingefroren`, „Liste → Abbild fehlt“:
MANIFEST und die zwei Snapshot-`config/`-Kopien (Block C). Kein Eintrag ohne
Zuordnung.

**Probe R13 (a):** `shared/test_ausschlussmengen.py` liest die vier
Ausschlussmengen mit `ast` (keine importiert, keine geändert) und verlangt
Gleichheit samt `XAUTUSDT` — 9/9, drei Mutationen je mit Gegenprobe. Die
Zusammenlegung bleibt der jeweils nächsten planmässigen Öffnung.

**Unverändert gemessen:** Benchmark im Modus Repo und frischer Klon
`64fb2912…`; acht Ausgaben ohne Modus bytegleich mit TB-114; Trockenlauf
9 × rc 0; `faltenplan.json` `0e54ac5c…`; Laufbereich 81 Module (= TB-114).
Tests am Stand `54ce889`:
44 Dateien, 41 rc 0 (darunter `test_vorregistrierung` 196/196,
`test_ersatzwerte` 99/99, `test_sperrlistensonde` 65/65,
`test_ausschlussmengen` 9/9, `test_startpruefungen` 44/44,
`test_arbeitsbaum_laufbereich` 26/26); ohne rc 0 nur die drei bekannten
ohne Bezug zu diesem Auftrag (`test_drawdown_beide_masse` terminiert nicht,
`test_stabile_sortierung` 43/3, `test_wellenauswahl` 322/1 — dieselben
Stellen wie TB-114).

**Nicht vollzogen in TB-117:** R12 (Neuerzeugung der Listen), R15 (b) (am
Tag-Commit), R16 (a) (nach dem Tag) und (b) (mit dem Zellen-Erzeuger), die
Bestätigung von 46.9 durch Fable.

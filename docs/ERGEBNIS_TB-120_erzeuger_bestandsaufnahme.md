# TB-120: Ergebnis. Erzeuger-Bestandsaufnahme, nur lesend — 61 Anforderungen aus dem Register an Listen- und Zellen-Erzeuger, Bestand im Code gemessen, 17 Lücken, Schnitt in neun Aufträge, 17 Fragen für Fable; vorab UMZUG 6 auf `UEBERGABE.md`

**Sitzungstitel:** `TB-120` · **Stand:** 27.09.2026 · **Auftrag:**
`docs/auftraege/MAC_TB-120_erzeuger_bestandsaufnahme.md` · **Belege:** `docs/belege/TB-120/`
**Eingang:** `d9e3600` (Abgabe TB-119). Commits: `5f819c1` (Schritt 0), `aab641e` (A), `3265b3a` (B), `42f507a` (C),
`d173ad4` (D), der Abgabe-Commit (E: dieses Dokument, Journal DS). Gepusht nach 0, A, D und nach der Abgabe.
**Freigabe** (wörtlich im Auftrag): 27.09.2026, 18:08, Chat, und ca. 18:25, Auswahlkarte „Was soll bis Dienstag ohne
Fable laufen?“ ⇒ „Wir arbeiten alles strukturiert ab“. Nicht freigegeben: Code ändern, Läufe, Schreiben in
`research/**/ergebnisse|daten/`, Register, Sperrliste, Abbilder, `crontab`, Datenbanken — nichts davon getan.
**Umgebung:** Mac, `/usr/bin/python3` für die Lesewerkzeuge (nur Standardbibliothek, `ast`). Kein Abbruchkriterium
ausgelöst. **Rückfragen an den Betreiber: keine.** **Sichtschutz 27.1:** Keine Ergebnisgrösse des Selektionsraums
erzeugt oder gelesen; von den neun TB-24-Listen nur sha256. Keine Erwartung über den Ausgang.

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | `git status` genau die drei erwarteten Dateien, md5 der Sammlung `d08f5431…` = Soll, numstat 32/0 ⇒ `5f819c1`. Ausgang Register `18e39ee2…`, db-Sicherung 12/12 rc 0 |
| **A** | UMZUG 6, Eröffnungstext Z. 257–258: zwei Stellen `UEBERGABE_2026-09-25.md` ⇒ `UEBERGABE.md`, numstat 2/2, danach **0** Treffer für den alten Namen in `UMZUG.md` |
| ⭐⭐ **B** | **61 Anforderungen** (AN-01 … AN-62, AN-29 nicht vergeben): 22 Listen-Erzeuger, 6 beide, 33 Zellen-Erzeuger (davon 5 ohne klaren Ort). **112 Zitate** maschinell gegen die Quellen geprüft, 0 fehlen; in der Fundstellen-Spalte keines über 15 Wörter. **11 offene Stellen** mit beiden Wortlauten (`b_offen.md`) |
| ⭐⭐ **C** | Listen-Erzeuger: 36.1-Teil **vorhanden**, Signalpfad-Teil **teilweise** (zweifache Simulation mit Kennzeichnung, `ausgefuehrt`, kein `bot`, kein `haltedauer_balken`, keine Parameter-Hashes). **Zellen-Erzeuger: kein Ansatz.** Der heutige Kern `evaluate_combination_multi` simuliert nicht und **verwirft Zellen** (`return None`, 3–4 Stellen je Bot); Kapital-Drawdown 0/9, MtM-Tagesreihe 0/9 im Laufcode. Posten 3: 1 fehlt, 2 teilweise; Posten 4: 4/4 Aktien fehlt; Posten 5: 0/9; Posten 8: fehlt. Listen-Hashes 9/9 gleich TB-114 |
| ⭐⭐ **D** | **17 Lücken** (G1–G17), **neun Aufträge** (E-1 … E-9), davon **ohne Fable baubar: E-1, E-8 als Gerüst, E-3 zum Teil**. Zellenzahl 2 416 = Register Abschnitt 3 |
| **Durchgehend** | Register sha256 vorher = nachher · Datenbanken 12/12 gleich wie 0c · **0 Dateien ausserhalb `docs/`** geändert (`e_schluss.txt`) |

⚠️ **Ein Vorfall, ohne Folge:** Der erste Versuch, die Zellenzahl zu zählen, rief `faltenplan.faltenplan()` auf. Das
startet intern einen Loader-Trockenlauf (Kindprozess `loaderlauf.py`). Er brach mit `/usr/bin/python3` sofort am
fehlenden `binance` ab, bevor Kursdaten geladen wurden. Nachgeprüft: `git status` leer, kein neuer `tb40_*`-Ordner.
Nicht wiederholt; gezählt wurde danach nur über `registerdaten.raster()`, die Faltenzahl aus Register 15.6
(`d_zellenzahl.txt`).

---

## 1. Schritt 0 — Sicherung und Ausgang

- **0a:** `?? MAC_TB-120_…`, ` M AKTUELLER_AUFTRAG.md` (Zeile TB-119 ⇒ TB-120, numstat 1/1), ` M FABLE_SAMMLUNG_…`
  md5 `d08f5431b0bcfc459cec5a6e1056e408` = Soll, numstat **32/0** = Soll. Keine weitere Datei ⇒ Commit `5f819c1`,
  gepusht.
- **0b** (`0b_ausgang.txt`): HEAD `5f819c14…`, Register `18e39ee29b9b…` (10 347 Zeilen), `git status --porcelain`
  1 — das ist der eben angelegte Ordner `docs/belege/TB-120/`, vorher 0.
- **0c** (`0c_db_sicherung.txt`): `db_sicherung.sh` ins iCloud-Ziel, 12/12 Datenbanken, `docs.tar.gz` 1 615 Dateien
  = `git ls-tree`, rc 0; sha256 der Originale festgehalten.

## 2. Schritt A — UMZUG 6 (`aab641e`)

`docs/projektfuehrung/UMZUG.md`, Eröffnungstext: Z. 257 `projektfuehrung/UEBERGABE_2026-09-25.md` ⇒
`projektfuehrung/UEBERGABE.md`, Z. 258 `(docs/projektfuehrung/UEBERGABE_2026-09-25.md)` ⇒
`(docs/projektfuehrung/UEBERGABE.md)`. Der alte Name kam im Eröffnungstext genau zweimal vor und sonst nirgends in
der Datei; danach `grep -n` **0 Treffer**. Die Zeile „Übergabe-Name“ (Z. 295) nennt den alten Namen nicht und ist
unverändert. Die Spalte des Gedankenstrichs in Z. 257 ist nicht nachgerückt („Nichts sonst.“). Nachweis
`a1_nachweis.txt`.

## 3. Schritt B — Anforderungen (`3265b3a`)

Tabelle mit 61 Zeilen: `docs/belege/TB-120/b_anforderungen.md` (zu lang für hier). Gelesen: 40.6, 41.1 (A3, A8–A12),
41.2 (B1, B3–B7), 41.3 (C1–C8), 45.3, 45.4, 45.5, 46.3–46.9, 11, 12, 15.1–15.6, 16.6, 16.7, 17.4, 19, 22.2, 24.2,
26.1/26.2, 29.3/29.4, 34.5, 36.1/36.5, 37.4, 38.1, 43.2, dazu `PLAN_VOR_DEM_TAG.md` (Stufe V, TB-30b Posten 1–8) und
Kopf/Docstring von `research/vorregistrierung/auswertung.py`. Ketten über `REGISTER_INDEX.md`.

- **Fundstelle „22d / Feld `teile`“:** Register **37.4**, Fables Entscheidung aus 22d Abschnitt 3 („Folge für
  `herkunft.py`“): der Erzeuger schreibt in `herkunft.json` auch das Feld `teile` aus `register()`.
- **„vor dem Tag“:** alle 61 ja. Für den Listen-Erzeuger steht es im Register (40.6), für den Zellen-Erzeuger nur
  im Plan (Stufe V vor Stufe VI) und mittelbar in 37.3 (letztes Abbild nach der letzten Codeänderung).
- **Zitate:** `b_zitate_pruefen.py` prüft jedes „…“ in B gegen Register, Plan, `auswertung.py`, `beispieldaten.py`,
  `positionen_holen.py` — 112 gefunden, 0 fehlen (`b_zitate_pruefen.txt`).
- **Offen, nicht entschieden:** O-1 … O-11 in `b_offen.md`; sie sind F-1 … F-11 unten.

## 4. Schritt C — Bestand (`42f507a`)

Einordnung je AN in `docs/belege/TB-120/c_bestand.md`, Messung `c_messung.py` → `c_messung.txt`, Suche
`c2_suche.txt`, Hashes `c1_listen_hashes.txt`. Das Wichtigste:

**C1 Listen-Erzeuger (`positionen_holen.py`, `46e3ed0`).** `--ziel` Pflicht, `O_CREAT|O_EXCL`, Ausgänge 1/2:
vorhanden. Gezählt werden die gefundenen Trades (`alle_trades` vor der Simulation), auch bei `elliott_wave`. Aber das
Skript simuliert zweimal und schreibt im zweiten Lauf `symbol#zeile` in das Symbolfeld (A9 verbietet das; TB-98 Befund
2: 9/9 brechen genau daran ab), schreibt `ausgefuehrt` (A12 verbietet das), hat kein Feld `bot` und statt
`haltedauer_balken` die Spalte `kerzen`. Modus und Resolver: ja, über `equity_simulation.load_all_symbol_data` →
`strategy_paths`. Parameter kommen aus `live_params.py` (über die Modulglobalen von `equity_simulation.py`); die
Herkunftsnotiz führt Commit und Startprüfung (mit `snapshot_hash`), aber **keine Hashes der Parameterdateien**.
Listen-Hashes 9/9 gleich `docs/belege/TB-114/b3_register.txt`.

**C2 Zellen-Erzeuger.** Kein Ansatz. `zellen.csv`/`tagesreihen` nur in `auswertung.py`, `beispieldaten.py` und zwei
Tests; `teile` liefert `herkunft.register()`, liest nur ein Test; Lese-Audit nur als die acht Startzeilen
`paths.audit_zeilen()`. `beispieldaten.py::erzeuge` gibt die Gestalt von `zellen.csv`, `tagesreihen/`,
`benchmark_tagesreihen/` und `herkunft.json` vollständig vor, **soweit der Vertrag reicht** — gegen sie lässt sich
bauen. Nicht vorgegeben: `teile`, Lese-Audit, Trade-Liste je Zelle, mediane Haltedauer, ereignisindizierter
Drawdown, Werte nach 22.2 und 16.7 (d).

**C3 Rechenkern.** `evaluate_combination_multi` (neun Optimierer) ist **kein** Zellen-Kern: keine Simulation, keine
Falten, Summen von `pnl_pct` über die ganze Historie, und `return None` bei `MIN_TRADES`, `MIN_SYMBOLS_CONTRIBUTING`,
`MIN_AVG_RETURN_PCT` oder ohne Trades — also genau das „nichts“, das R5 (b) und 43-7 verbieten. Brauchbar sind
`collect_all_trades` (Signalpfad, nimmt die Achsenwerte, ausser den drei Achsen aus Posten 3) und
`simulate_portfolio` → `shared/zuteilung.py::simuliere_portfolio`; dieses gibt die ausgeführten Positionen aber nicht
heraus (Grund für die Kennzeichnung in TB-24). Die tägliche MtM-Bewertung je Falte gibt es als Research-Kern
`research/mtm_drawdown/mtm_kern.py` (TB-73), ausserhalb des Laufbereichs, auf ausgeführten Positionen. Je Bot:
Kapital-Drawdown **fehlt 9/9**, MtM-Tagesreihe **fehlt 9/9** (im Laufcode), Trades mit Ein- und Ausstieg **ja**,
Balkenzahl **nein**.

**C4 TB-30b.** Posten 3: `rsi2_mean_reversion` **fehlt** (`SMA_TREND_PERIOD = 200` Konstante), beide Breakout-Bots
**teilweise** (Backtest nimmt die Argumente, Optimierer und Simulation reichen sie nicht durch). Posten 4: vier
Aktien-Bots **fehlt** (Fenster je Symbol ab dem Ende der Kursdatei; `faltenplan.HORIZONTBEGINN` existiert, wird nicht
gelesen), Krypto nicht betroffen. Posten 5: **0/9**.

**C5 Posten 8.** **Fehlt.** Kein `selektionsmodus` in den neun `multi_symbol_walk_forward.py`, kein Hinweis in
`paths.py`/`strategy_paths.py`; über den Import von `multi_symbol_optimise` liefen sie im Modus auf dem Snapshot.

**C6 Laufbereich.** Von den 81 Modulen (44-8) würde ein Erzeuger auf heutigem Bestand die Bot-Module, `shared/`-Module
und `registerdaten`, `faltenplan`, `kennzahlen`, `benchmark`, `auswertung`, `bot_lauf` importieren; **neu** hinzu
kämen das Erzeuger-Modul, `herkunft.py` (R5 (a), T117-5) und gegebenenfalls `mtm_kern.py`.

## 5. Schritt D — Plan (`d173ad4`)

Lückenliste G1–G17 und Abhängigkeiten: `docs/belege/TB-120/d_plan.md`. Der Schnitt, Umfang **geschätzt** (K2o):

| Auftrag | Gegenstand | Sperrliste / `EINGEFROREN` | Umfang (geschätzt) | Fable? |
|---|---|---|---|---|
| **E-1** | TB-30b Posten 3, Ausgabe bytegleich mit Voreinstellungen | Punkt 11 (Commit) | mittel, 7 Dateien | **nein** |
| **E-2** | Registerauftrag mit den Antworten auf F-1 … F-17, Feldliste der neuen Listen | Register | mittel | wartet |
| **E-3** | Listen-Erzeuger nur Signalpfad, Feldliste, Parameter-Hashes | — | klein, 2–3 Dateien | **zum Teil nein** |
| **E-4** | Listen neu erzeugen, Modus, zweimal bytegleich, Leseprotokoll | Eingabe nach 23d | klein; Lauf mit Freigabe | wartet |
| **E-5** | Folgen: `EINGEFROREN`, `TB24_DATEN` (zweimal), `messgroessen.py`, 33.2-Vergleich, Deckel, Donchian, Abbild | ⚠️ `herkunft.py` (11/12), `faltenplan.py` (2), `messgroessen.*` (`EINGEFROREN`) | gross | nach E-4 |
| **E-6** | Posten 4, Horizont je Bot | Punkt 11 | klein, 4 Dateien | wartet (F-13) |
| **E-7** | Zellen-Kern: ausgeführte Positionen, MtM-Tagesreihe, Kapitalpfad ab erster Falte, Posten 2, Wache 29.4 | ⚠️ `shared/zuteilung.py` (Punkt 10, im Abbild); Optimierer Punkt 11 | gross, 10–12 Dateien | wartet (F-12, F-14) |
| **E-8** | Zellen-Erzeuger: Schreiber, `herkunft.json` mit `teile`, Lese-Audit, Startprüfung, Walk-Forward-Wache | neues Modul in den Laufbereich | gross | **Gerüst nein**, Rest wartet |
| **E-9** | Laufbereich messen, `ARBEITSBAUM_PFADE`, letztes Abbild | `paths.py`; Abbild neu (37.3) | klein | wartet (T117-5) |

**27c:** Leiter L2–L5 (T116) berühren den Erzeuger nicht. T117-5 hält E-9 an. T117-6 und T117-1 betreffen Reihenfolge
am Tag und Tests von E-8, nicht den Bau.

## 6. Für Fable

Ohne Neigung. F-1 … F-11 sind O-1 … O-11 aus `b_offen.md`; dort stehen die Wortlaute vollständig und geprüft, hier
gekürzt. Herkunft jeweils: diese Sitzung, `docs/belege/TB-120/`.

- **F-1 (O-1) Zeilen in `zellen.csv`.** R5 (b): „`zellen.csv` enthält für jede Zelle des Rasters genau eine Zeile; die
  Zeilenzahl ist gleich der Zahl der Zellen“ — Vertrag `auswertung.py`: „genau eine Zeile je (Zelle x Falte), fuer ALLE
  Falten des Faltenplans, Bestaetigungsperiode eingeschlossen.“ Welcher Mengenbegriff gilt für die Abnahme?
- **F-2 (O-2) Leere Trade-Liste.** R5 (b) „(Sharpe 0 nach Registertext 1c, leere Trade-Liste)“, 43-7 „(leere Liste,
  Sharpe 0 nach 1c)“; der Vertrag kennt keine Trade-Liste je Zelle. Gibt es sie als Rohergebnis, in welcher Datei, mit
  welchen Feldern?
- **F-3 (O-3) Kill-Test-Werte.** 22.2: „Der Lauf berichtet je Bot für den Plateau-Gewinner drei Werte“. `auswertung.py`
  rechnet sie nicht; bestes Symbol und fünf beste Trades brauchen Daten, die der Vertrag nicht führt. Zellen-Erzeuger
  oder `auswertung.py` (Öffnung der Punkte 3/5/14)?
- **F-4 (O-4) Bootstrap.** 15.3 (a): „Jedes Bootstrap-Intervall im Auswertungsskript wird auf der Reihe der täglichen
  Netto-Mark-to-Market-Renditen des Kapitalpfads gerechnet“; 15.3 (b) L = max(„mediane Haltedauer des Parametersatzes in Handelstagen“, …). Im Code 0 Treffer für `bootstrap`; der Vertrag führt keine Haltedauer. Wo entsteht
  das Intervall, und liefert der Erzeuger die Haltedauer je Zelle?
- **F-5 (O-5) Zwei Drawdowns.** 24.2: MtM-Drawdown bewertet, „Der ereignisindizierte Drawdown aus
  `equity_simulation.py` wird berichtet, nicht bewertet.“ — `beispieldaten.py`: „der Kapital-Drawdown einer Falte
  steht in `zellen.csv`, weil er im echten Lauf aus `equity_simulation.py` kommt“. Der Vertrag hat eine Spalte. Wo steht
  der ereignisindizierte Wert?
- **F-6 (O-6) Embargo und Beginn der Bestätigung.** 16.6: „Die Bestätigungsperiode eines Bots beginnt am ersten
  Handelstag nach Go-Live, an dem keine vor Go-Live eröffnete Position dieses Bots mehr offen ist.“; 41.3 C3: „für den
  Gewinner auf dessen eigenen simulierten Positionen“ — 15.6/38.1: Bestätigungsfalte `2026-01-01/2026-09-01`,
  Go-Live-Schnitt „2026-09-01, ausschliesslich“. (1) Wo wird die Bedingung ausgewertet, wenn der Gewinner erst in
  `auswertung.py` feststeht? (2) Wie verhält sich „nach Go-Live“ zu dieser Spanne?
- **F-7 (O-7) 3b (d).** Symbolzahl, Anteil, Auslassungen mit Grund und Faltenkohärenz „Berichtet je Bot und Falte“;
  16.11 Z. 7: „Der spätere Auswerter tut es noch nicht“. Die Kohärenz braucht die Rangfolge aller Zellen. Wo?
- **F-8 (O-8) Benchmark-Tagesreihe.** Vertrag: `benchmark_tagesreihen/<markt>.csv`, „das gleichgewichtete
  point-in-time-Universum, taeglich.“ — 23.3: „aus den Symbolen gebildet, die der Loader des Bots an diesem Tag
  handelbar macht“. 46.3 nennt diese Datei nicht als Ausgabe. Wer schreibt sie, je Markt oder je Bot?
- **F-9 (O-9) 36.1 für Rohergebnisse.** 36.1 gilt für Pfade, die „auf der Sperrliste steht oder für sie bestimmt ist“;
  der Plan: „unterliegt der Schreibregel 36.1 von Anfang an“. Genügt der Plan, oder braucht es einen Registersatz?
- **F-10 (O-10) `haltedauer_balken`.** Name registriert (B6/B7), Zählregel und Einheit nicht; `positionen_holen.py`
  zählt `kerzen` „beide Enden eingeschlossen“. Welche Zählregel, welche Einheit, welche Umrechnung für den Deckel in
  Handelstagen?
- **F-11 (O-11) Bindung der neuen Listen.** 40.6: „und als Punkt auf die Sperrliste aufgenommen“ — R3: „gehören mit
  ihrem Hash in die Gruppe `eingefroren` des Abbilds“. Beides, oder erfüllt R3 den Satz aus 40.6?
- **F-12 Ort des Zellen-Kerns.** 11.2: `evaluate_combination_multi` liefere den Kapital-Drawdown „noch nicht“ mit,
  „Das nachzurüsten ist TB-30b.“; 29.4/34.5: die Wache „wird in allen neun `multi_symbol_optimise.py` eingebaut“ —
  `PLAN_VOR_DEM_TAG.md`, Posten 2: „im Erzeuger (10)“. Gemessen: `evaluate_combination_multi` simuliert nicht und
  verwirft Zellen. Wird es zum Zellen-Kern umgebaut, oder rechnet der Erzeuger über `collect_all_trades` und
  `simulate_portfolio` — und schützt die Wache in den Optimierern dann den Lauf?
- **F-13 Reihenfolge Listen gegen Posten 4.** 40.6 verlangt die Listen „mit dem registrierten Code“. Posten 4 (26.2,
  Horizont je Bot) ändert den Signalpfad der vier Aktien-Bots. Werden die Listen vor oder nach Posten 4 erzeugt?
  (Posten 3 mit unveränderten Voreinstellungen ändert keine Ausgabe; das ist messbar.)
- **F-14 Ausgeführte Positionen.** `simuliere_portfolio` gibt sie nicht heraus; A9 verbietet die Kennzeichnung; die
  MtM-Tagesreihe (1a, 24.2) braucht sie. Ist eine zusätzliche Rückgabe aus `shared/zuteilung.py` (Sperrlistenpunkt 10,
  Rechnung unverändert) als beauftragte Änderung nach 37.3 der Weg, oder ein anderer?
- **F-15 Abnahme vor dem Tag ohne Ergebnis.** R5 (b) (Zeilenzahl, Nullzeile) ist erst an einem Lauf prüfbar; ein Lauf
  des Zellen-Erzeugers auf dem Snapshot erzeugt vor dem Tag Ergebnisgrössen des Selektionsraums. Womit wird er vor dem
  Tag abgenommen (synthetische Eingaben, Teilraster, nur Struktur)?
- **F-16 Übernahme von `mtm_kern.py`.** Der MtM-Kern liegt in `research/mtm_drawdown/` (TB-73). Import aus dort
  (Laufbereich wächst um ein Research-Modul) oder Verlagerung nach `shared/`? *Kann auch Handwerk sein; hier genannt,
  weil es den Laufbereich (R4) ändert.*
- **F-17 Parameterdateien.** 40.6 (Folgerung TB-96): „je Bot die Hashes der Parameterdateien“. Gemessen stehen
  Handelsparameter auch als Konstanten in `backtest_*.py` (z. B. `SMA_TREND_PERIOD = 200` in
  `rsi2_mean_reversion/backtest_rsi2.py`; 15.4 zitiert `MAX_HOLD_HOURS` aus `backtest_elliott.py`). Welche Dateien sind
  „Parameterdateien“?

## 7. Für den steuernden Chat

- **Fable-Sammlung:** F-1 … F-17 nach `FABLE_SAMMLUNG_fuer_2026-09-29.md`, Abschnitt D, übertragen (die Sitzung hat
  dort nicht geschrieben).
- **Ablage:** `UMZUG.md` geändert, md5 `33645d43fcabfcfd9b3d0a9def3660b5` — neu ablegen. Damit ist der Befund zum Eröffnungstext aus ERGEBNIS_TB-119, Abschnitt 7, erledigt.
- **`beispieldaten.py`, Docstring:** beschreibt den Kapital-Drawdown noch als Wert aus `equity_simulation.py` (Stand
  vor 24.2). Tatsache, nicht geändert (Code nicht freigegeben; hängt an F-5).
- **Vorfall `faltenplan.faltenplan()`:** Die Funktion startet einen Loader-Trockenlauf. Für künftige nur lesende
  Aufträge gehört das in die Liste der Aufrufe, die nicht „lesen“ sind (neben `faltenplan.py main()`). Vorschlag für
  einen Backlog- oder Prüfprinzip-Eintrag; hier nicht eingetragen.
- **Nächster Auftrag ohne Fable:** E-1 oder E-8 als Gerüst (Abschnitt 5). Beide ändern Code und brauchen eine
  Freigabe.

## 8. Nicht getan, und warum

- **Kein Lauf** von `positionen_holen.py`, Optimierern, Simulationen oder Erzeuger: nicht freigegeben. AN-01/02/13,
  AN-54/55 sind deshalb „nicht prüfbar ohne Lauf“.
- **Keine Codeänderung**, auch nicht am veralteten Docstring von `beispieldaten.py`: nicht freigegeben.
- **Kein Inhalt der TB-24-Listen gelesen**, auch keine Zeilenzahl ausgegeben (die Zeilenzahlen in TB-114 wurden nicht
  wiederholt): Sichtschutz 27.1; nur sha256.
- **Kein Eintrag in die Fable-Sammlung**: Auftrag („Die Sitzung schreibt dort nicht hinein“).
- **Keine Entscheidung an den offenen Stellen**: Auftrag („nicht entscheiden“).
- **Sonde nicht gelaufen**: für diesen Gegenstand nicht nötig; der Sperrlisten-Stand ist aus dem Abbild `46f0ad5d…`
  gelesen.

## 9. In einfacher Sprache

Bevor der grosse Lauf starten darf, braucht es zwei Programme, die Ergebnisse schreiben: eines, das die neun
Handelslisten neu erzeugt, und eines, das für jede der 2 416 Einstellungen und jedes Jahr die Kennzahlen aufschreibt.
Diese Sitzung hat nur gelesen und gezählt. Das Ergebnis: Das erste Programm gibt es schon halb. Es schreibt sicher,
aber es macht noch Dinge, die das Regelwerk inzwischen verbietet. Vom zweiten Programm gibt es nur Bausteine. Der
Rechenteil, der heute in den Bots steckt, lässt ausgerechnet die Einstellungen ohne Trades weg, und genau die
müssen aufgeschrieben werden. Die Arbeit lässt sich in neun Aufträge teilen. Drei davon gehen ohne Fable. Für den Rest
liegen 17 Fragen für Dienstag bereit, jede mit der Stelle im Regelwerk, an der sie entsteht. Nebenbei zeigt das
Umzugsdokument jetzt auf die richtige Übergabe.

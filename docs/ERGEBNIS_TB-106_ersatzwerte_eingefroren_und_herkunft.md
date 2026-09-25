# TB-106: Ergebnis. Rückfall (d) geschlossen: sieben stille Ersatzwerte in den eingefrorenen Dateien enden mit 2, unbekannter Bedingungstext mit 2, tote Felder raus, `herkunft.py` hasht im Modus den Snapshot; neues Abbild `40ffe18d…`; Benchmark im Modus (Repo und Klon) und ohne Modus bytegleich `64fb2912…`

**Sitzungstitel:** `TB-106` · **Stand:** 25.09.2026, ca. 19:45 · **Auftrag:**
`docs/auftraege/MAC_TB-106_ersatzwerte_eingefroren_und_herkunft.md` · **Belege:** `docs/belege/TB-106/`
**Eingang:** `2e21471`. Commits: `327bc79` (Schritt 0), `abeca36` (Block B), `a08c13a` (Block C),
`5cc1de4` (Block D), `5791b4c` (Block E), `e1e6652` (Abbild) und der Abgabe-Commit (Belege, dieses Dokument, Journalblock DE).
**Grundlage:** Fable 24b A2, 25a Abschnitt 4 Rang 3, 25b (4) und 3 (4), 25c Abschnitte 1, 2 (a), 4 (4)(b); Register 37.3.
Freigabe des Betreibers 25.09.2026, 18:09 (drei Auswahlkarten, wörtlich im Auftrag).
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **A** | Vormessung bestätigt, Zeile für Zeile (die Dateien waren seit `f334a7b` unverändert). **Keine Stelle wird von der registrierten Eingabe erreicht** (Abbruchkriterium 2 greift nicht). A5 ist eine Rechenregel (Grenzwert 0), kein Ersatzwert. Kein Aufrufer im Regelbetrieb. `Abbruch` endet mit **1**. `TB30A_BASE_DIR` greift in `herkunft.py` auch unter gesetzten Modus-Variablen |
| ⭐ **B** | `faltenplan.py`: `volle_jahre()` ohne inneres Jahr und `faltenlaenge_jahre()` ohne Zählung ⇒ rc 2. `embargo_nach_falten` und `mindesttraining_jahre` sind aus dem Plan, die Berichtszeile aus `registerbericht.py`. G8/G8M angepasst |
| ⭐ **C** | `benchmark.py`: leere Renditereihe und Bot ohne Selektionsfalte ⇒ rc 2. `nachschlagen()` unverändert |
| ⭐ **D** | `auswertung.py`: fehlende Statistik (Zelle oder Nachbar), Plan ohne Selektionsfalten, unbekannter `_bedingung`-Text ⇒ rc 2. `abbruchkriterien()`/`ein_bot()` ohne `.get(…)`, ohne `else: c = False` |
| ⭐⭐ **E** | `herkunft.py`: `block()`/`anhaengen()` reichen `daten_dir` an `datenstand()` durch; unter dem Modus Pflicht (sonst 2); `--anhaengen` übergibt `paths.DATA_DIR`; kein `makedirs` mehr (fehlender Ordner ⇒ 2). **Im Modus hasht die Kette den Snapshot: `d9449faf…`, gleich dem registrierten Datenstand** (gemessen, nicht angenommen). Ohne Modus liefert `block()` dasselbe wie vorher |
| **F** | Neues Abbild `sperrliste_abbild_2026-09-25b.json` **`40ffe18d…`**. Sonde gegen das alte `cb4eb1b4…`: Befund **genau** an 2, 3, 4, 5, 6, 11, 12, 14. Gegen das neue: Pfad-Bestandteile 25/0/0. `register()` `57ec6573…` ⇒ `0ece95e2…` |
| ⭐⭐ **G** | Benchmark im Modus **im Repo und im frischen Klon bytegleich `64fb2912…`**. Ohne Modus: 7/8 Ausgaben bytegleich, `plan.json` **nur** um die zwei Schlüssel verschieden. Benchmark ohne Modus `64fb2912…`. Auswertung auf Beispieldaten zeichengleich `fc178106…`. Trockenlauf 9 × rc 0. Tests grün, `test_ersatzwerte` 40/40 neu |
| **H** | Geändert sind nur die fünf freigegebenen Dateien, ihre Tests, das neue Abbild und `docs/`. Das echte `herkunft_protokoll.jsonl` **existiert nicht** und wurde nicht angelegt |

---

## 0. Schritt 0

| | |
|---|---|
| 0a | Fünf Dateien des steuernden Chats committet (`327bc79`); der Arbeitsbaum entsprach genau der Erwartung |
| 0b | Keine `.git/*.lock`. HEAD am Eingang `2e21471` (= Soll). Datenstand `d9449faf…` (223). Snapshot `--pruefen` Soll = Ist. Einzelhashes aller freigegebenen und gesperrten Dateien, aller Dateien unter `ergebnisse/`, je versionierter Datei (1532) und der 12 `*.db` in `0_hashes_vorher.txt` (Skript `hashes.sh`). `register()` vorher `57ec6573eb44f18b…` mit 11 Teilen. Sonde gegen `cb4eb1b4…`: Pfad-Bestandteile 25/0/0, rc 2 nur NICHT PRÜFBAR (`0_sonde_vorher.txt`). Beleg `0_schritt0.txt` |

## 1. Block A: Vormessung nachgemessen

Beleg `a_vormessung.txt` (Zeilen), `a8_messung.txt` (Messung), `a8_tatsachennotizen.txt` (Notizen), `a9_aufrufer.txt`, `a10_abbruch_rc.txt`, `a11_tb30a.txt`. **Meine Messung weicht von der Vormessung nicht ab** – alle Zeilennummern stimmen.

| | Stelle | erreicht die registrierte Eingabe den Zweig? | jetzt |
|---|---|---|---|
| A1 | `faltenplan.py:152-153` `volle_jahre()` | **nein** – alle neun Bots haben innere Kalenderjahre in `research/tb24_haltedauern/daten` | rc 2 |
| A2 | `faltenplan.py:159-160` `faltenlaenge_jahre()` | **nein** – keine Zählung leer | rc 2 |
| A3 | `benchmark.py:206-207` `drawdown_bei_exposure()` | **nein** – die Tabelle `64fb2912` führt je Falte `handelstage` = Länge des Fensters: 77 Falten (alle Rollen), keine mit 0; ihre Falten sind Name für Name die des gerechneten Plans | rc 2 |
| A4 | `benchmark.py:302` `je_bot()` | **nein** – jeder der neun Pläne hat Selektionsfalten | rc 2 |
| A5 | `benchmark.py:221-222` `nachschlagen()` | Rechenregel, siehe unten | **unverändert** (C2) |
| A6 | `auswertung.py:284, 286` `plateau()` | Rohergebnisse gibt es noch nicht. Beispieldaten aller neun Bots, instrumentiert: 0 Treffer. `lies_zellen()` erzwingt vorher jede Zelle mit genau den Falten des Plans | rc 2 |
| A7 | `auswertung.py:333-334`, `380-385` | **nein** – alle neun Pläne `endgueltig` mit Selektionsfalten; Beispieldaten 0 Treffer | rc 2; `c` direkt gerechnet |
| A7b | `auswertung.py:500-521` | nur über A7 erreichbar ⇒ nein | Zugriff ohne `.get` |
| A7c | `auswertung.py:154-158` `bedingung_fuer()` | **nein** – genau ein Bot trägt Text (`t3_supertrend`), und das ist der bekannte | unbekannter Text ⇒ rc 2 |
| A7d | `faltenplan.py:308/315`, `registerbericht.py:139` | Leser: keine im Code außer G8/G8M; `benchmark.py:70` ist Kommentartext | entfernt |
| A7e | `herkunft.py:126-167` | `herkunft.py` importierte `paths` nicht: unter dem Modus hashte die Kette `BASE_DIR/data` – heute gleich dem Snapshot, aber keine Eigenschaft des Codes | Block E |

**A9 – Aufrufer im Regelbetrieb:** keiner. ⚠️ `crontab -l` war auch in dieser Sitzung vom Werkzeug abgelehnt; gemessen ist statisch. Unter `system/`, `dashboard/`, `notifications/`, `broker/`, `strategies/` und in `shared/` (ohne Tests) importiert oder startet niemand die vier Dateien. `shared/snapshot.py` lädt `herkunft.py` und ruft nur `datenstand(ordner)` **mit** Pfad, unberührt von E. `block()`/`anhaengen()` ruft nur `herkunft.py::main`. Importeure sind sonst `research/`-Werkzeuge und Tests (`erste_falte_trockenlauf`, `test_horizontbeginn`, `test_erste_falte_trockenlauf`, `test_universum_trockenlauf`, `etf_trendfolge/datenstand.py` nur `datenstand`). Deshalb „rc 2 unabhängig vom Modus“ ohne Rückfrage gebaut.

## 2. Block B: `faltenplan.py` und `registerbericht.py`

- **B1:** `volle_jahre()` bricht ab, wenn kein inneres Jahr bleibt; die leere Zählung gibt weiter `{}` zurück, und `faltenlaenge_jahre()` bricht dann ab. Meldung auf stderr nennt Stelle und den früheren Ersatzwert, dann `SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)`. `paths` ist wie in `benchmark.py` importiert (`sys.path` + `import paths`), kein Import aus `strategy_paths`.
- **B2:** `embargo_nach_falten` (je Falte) und `mindesttraining_jahre` (je Plan) sind aus dem gerechneten Plan. Der Verlaufsabsatz im Modulkopf nennt das. `registerbericht.py` druckt die Zeile „Mindesttraining vor der ersten Falte“ nicht mehr. **Tatsachennotiz:** `rd.MINDESTTRAINING_JAHRE` (`registerdaten.py:108`) ist jetzt tot, kein Leser; bleibt stehen bis 40.8 (h).
- **B3:** `FELDLISTE_PLAN`/`FELDLISTE_FALTE` ohne die beiden Schlüssel (benannter Zwischenstand, Kommentar verweist auf 25b 3 (3)). `G8M` fügt jetzt `mindesttraining_jahre` wieder ein und zeigt, dass G8 rot wird, mit Gegenprobe.
- ⚠️ **Nebenbefund:** `registerbericht.py --pruefen` war **schon vorher rot** (rc 1, „die Zahlen dort sind veraltet“). Der erzeugte Block unterscheidet sich vorher/nachher nur um diese eine Zeile (`b2_registerbericht.txt`). Das Register trägt die alte Zeile in Z. 392; es ist nicht freigegeben.

## 3. Block C: `benchmark.py`

- **C1:** `drawdown_bei_exposure()` mit leerer Reihe und `je_bot()` ohne Selektionsfalte (Wache vor der Medianschleife) ⇒ rc 2. Der Kommentar in `je_bot()` („definiert dafür 0.0“) ist nachgezogen.
- **C2 – A5 bleibt:** Unterhalb der ersten Stufe (0,01) rechnet `nachschlagen()` `tabelle[0,01] · e / 0,01`. Gemessen an allen 86 Tabellen der neun Bots (je `dd_toleranz` und `dd_benchmark` je Falte) gilt für e = 10⁻³, 10⁻⁴, 10⁻⁶, 10⁻⁹: `nachschlagen(t,e)/nachschlagen(t,0,01) = e/0,01`, Abweichung höchstens 1,4·10⁻¹⁷. Der Betrag fällt linear mit e gegen 0. `nachschlagen(t, 0) = 0` bei allen 86. Der Zweig `e <= 0 ⇒ 0.0` ist also der Grenzwert der Formel, kein Ersatzwert. Probe `C-A5` hält ihn fest.

## 4. Block D: `auswertung.py`

- **D1:** Neu ist `_statistik_von()`. `plateau()` holt Zelle und Nachbarn darüber; fehlt einer ⇒ rc 2, die Meldung sagt „Zelle“ oder „Nachbarn“.
- **D2:** `beta_bereinigung()` ohne Selektionsfalten ⇒ rc 2 (die Reihenfolge davor – Tagesreihe und Benchmark lesen – ist unverändert). `abbruchkriterien()` rechnet `c` direkt; `ein_bot()` liest die Bereinigung mit `[…]` (8 Stellen). Ergebnis-JSON auf den Beispieldaten aller neun Bots **zeichengleich `fc178106…`** (G3).
- **D3:** `bedingung_fuer()` ist die einzige Deutung: kein Text ⇒ `None` („keine Rasterbedingung (Register Abschnitt 6)“ im Code), bekannter Text ⇒ die Bedingung, sonst rc 2 – ohne Modus-Abfrage. Leser in `auswertung.py`: `lies_zellen()` (Z. 174) und `ein_bot()` (Z. 475), beide über die Funktion; `beispieldaten.py:160` ebenso. **Zweite Deutungsstelle bleibt `registerdaten.py:605`** (`zellen()`, eigener Stringvergleich; Punkt 1, nicht geöffnet; Tatsachennotiz bis 40.8 (h)).
- `auswertung.Abbruch` und seine 12 Stellen sind unverändert (A10).

## 5. Block E: `herkunft.py`, planmässig für den Datenpfad geöffnet

- **E1:** `block(anlass, daten_dir=None)` und `anhaengen(anlass, daten_dir=None)`. Unter dem Modus ohne `daten_dir` ⇒ rc 2. `paths` wird **erst bei Bedarf** geladen (`_paths()`), damit der Import von `herkunft.py` unverändert bleibt – `etf_trendfolge` und die Tests laden das Modul auch mit einer `TB30A_BASE_DIR` ohne `shared/`.
- **E2:** `--anhaengen` übergibt unter dem Modus `paths.DATA_DIR`, ohne Modus `None` (Voreinstellung).
- **E3:** `os.makedirs` ist weg; fehlt der Ordner des Protokolls ⇒ rc 2, ohne Modus-Abfrage.
- **E4:** `EINGEFROREN`, `register()`, `SPERRLISTE_DATEIEN`, `kette_pruefen()`, `commit()`, `datenstand()`, `BASE_DIR` samt `TB30A_BASE_DIR` sind zeichengleich.
- **E5 (`e5_herkunft.txt`)**, im Wegwerfbaum, das echte Protokoll unberührt:
  - Modus auf den **echten** Snapshot `63e4b6c8…`, `--anhaengen`: rc 0. Die Zeile trägt `datenstand` **`d9449faf51bffaaa…`**, 223 Dateien. Das ist gleich `herkunft.datenstand(<Snapshot>)` **und gleich dem registrierten Datenstand**. Das erfundene `data/` des Baums ist nicht gehasht.
  - Modus, `block()` ohne `daten_dir`: rc 2.
  - Ohne Modus: `block()` der neuen Fassung = `block()` der Fassung `327bc79`, beide mit dem echten `_HIER`, ohne Zeitstempel: **gleich**.
  - Ordner fehlt ⇒ rc 2, kein Ordner angelegt; Mutationen „Voreinstellung zurück“ und „`makedirs` zurück“, je allein: Proben E-b/E-c in `test_ersatzwerte.py`.
- ⚠️ **Folge, die der Auftrag nicht nennt:** Die Prüfansicht `python3 herkunft.py` (ohne `--anhaengen`) ruft `block("pruefung")` ohne Pfad und endet **unter dem Modus jetzt mit 2**. Vorher hashte sie dort still `data/`. Ohne Modus ist sie unverändert. Nicht mitgebaut („planmässig geöffnet heisst nicht offen“) – Frage 2 unten.

## 6. Block F: Abbild und Sonde

| | |
|---|---|
| F1 | `sperrliste_abbild.py --ziel …/sperrliste_abbild_2026-09-25b.json` nach dem letzten Code-Commit `5791b4c`: **`40ffe18d6a6345d1ab88aa993535cfb10264d8cf2e02e804406bbe85236642c8`**, 9191 Bytes, 14 Punkte, 15 Pfadnennungen, eingefroren 10. Commit `e1e6652` |
| F2 | Sonde gegen das **alte** Abbild `cb4eb1b4…`: rc 1, BEFUND in Punkten **[2, 3, 4, 5, 6, 11, 12, 14]** und in der Gruppe `eingefroren` (drei `EINGEFROREN`-Dateien geändert); Pfad-Bestandteile 14/11/0. Kein Punkt außerhalb der erwarteten (`f2_sonde_alt.txt`). Gegen das **neue**: Pfad-Bestandteile 25/0/0, rc 2 nur NICHT PRÜFBAR wie vorher (`f2_sonde_neu.txt`) |
| F3 | `herkunft.register()` vorher **`57ec6573eb44f18bccaa461da41ac0b835ba1afa1446ef27b4c3409ead56e46e`**, nachher **`0ece95e2fd4f5bd2787ea40f6a12988aadb0a414c5132553522b55000c6052d7`**. Geändert sind drei der 11 Teile: `faltenplan.py` `d57fe9c9…`⇒`63dafeb4…`, `benchmark.py` `4c923cd9…`⇒`aeeec9b8…`, `auswertung.py` `c3b4e69d…`⇒`83c6bc3c…`. `herkunft.py` selbst ist kein Teil von `register()`: `56a1c2e1…`⇒`351f24c2…` (`0_hashes_vorher.txt` (9), `f3_register_nachher.txt`) |

## 7. Block G: Abnahme

| | Soll | Ist | Beleg |
|---|---|---|---|
| G1 | Modus, Repo und frischer Klon, `64fb2912…` | **Repo `64fb2912…` rc 0 (67 s); Klon (`git clone`, HEAD `e1e6652`) `64fb2912…` rc 0 (74 s).** Klasse (i) 246/225 im Snapshot/21 außerhalb, wie TB-105. (ii) die 5. (iii) im Repo 20 = 10 `mkdir` + 10 `w` unter `$TMPDIR/tb40_lauf_*` (TB-107); im Klon dieselben 20 + 16 `mkdir` im Apple-Bytecode-Cache (`~/Library/Caches/com.apple.python/<klon>/…`, Klasse (ii) nach 25c 4 (4)(a)). Im Klon `git status --porcelain --ignored` vorher und nachher leer | `g1_benchmark.txt`, `g_klassen_repo.txt`, `g_klassen_klon.txt` |
| G2 | ohne Modus 8 Ausgaben | 7/8 hashgleich. `plan.json` `3dad5615…`⇒`5988abd1…`; nach Entfernen von `mindesttraining_jahre` (9 ×) und `embargo_nach_falten` (77 ×) aus der Vorher-Fassung **zeichengleich**. Benchmark ohne Modus **`64fb2912…`** | `g2_ohne_modus.txt`, `g2_plan_vergleich.py` |
| G3 | Auswertung Beispieldaten vorher = nachher | **`fc178106…` = `fc178106…`**, `cmp` zeichengleich (alle neun Bots) | `g3_auswertung.txt` |
| G4 | Tests | `test_vorregistrierung` **196/196** (Zahl unverändert: G8M ersetzt, nicht ergänzt), `test_faltenplan_neun` **156/156**, `test_universum_trockenlauf` **163/163**, dazu `test_horizontbeginn` 61/61 und `test_erste_falte_trockenlauf` 50/50 (beide importieren `faltenplan.py`), `test_paths` 35/35, `test_strategy_paths` 23/23, **neu `test_ersatzwerte` 40/40** (22 s) | `g4_tests.txt` |
| G5 | Trockenlauf 9 × rc 0 im Modus | **9 × rc 0**, Liste = Universumsdatei, keine Standardliste, geladen 18/18/20/20/20/147 × 4 (16.1.1). Klasse (i) außerhalb 0, (iii) 0 bei 9/9 | `g5_trockenlauf.txt`, `g_klassen_repo.txt` |

**Namen der neuen Proben** (`research/vorregistrierung/test_ersatzwerte.py`):
- B: `B-A1`, `B-A1b`, `B-A1M`(+`-G`), `B-A2`, `B-A2M`(+`-G`);
- C: `C-A3`, `C-A3M`(+`-G`), `C-A4`, `C-A4M`(+`-G`), `C-A5`;
- D: `D-A6`, `D-A6n`, `D-A6M`(+`-G`), `D-A7`, `D-A7M`(+`-G`), `D-A7b`, `D-A7bM`(+`-G`), `D-A7b2`, `D-A7b2M`(+`-G`), `D-A7c`, `D-A7c2`, `D-A7cM`(+`-G`);
- E: `E-a`, `E-b`, `E-bM`(+`-G`), `E-c`, `E-cM`(+`-G`), `E-d`, `E-e` (echtes Protokoll unberührt).

Jede Mutation stellt genau eine Stelle auf den alten Ersatzwert zurück, in einer Kopie; die anderen Stellen bleiben.

## 8. Block H: Hashes nachher

`h1_hashes_nachher.txt`, Vergleich `h1_vergleich.txt`; Zusammenfassung in Abschnitt 12.

---

## 9. Für Fable (ohne Kontext lesbar) ⭐⭐

**Stand.** Rückfall (d) in den eingefrorenen Dateien ist geschlossen. Jede Stelle bricht mit 2 ab statt still weiterzurechnen: `faltenplan.py` A1/A2, `benchmark.py` A3/A4, `auswertung.py` A6/A7/A7b, dazu der unbekannte Bedingungstext A7c. Die Meldung steht auf stderr, der Rückgabewert kommt aus `paths.RUECKGABEWERT_STARTPRUEFUNG`, ohne Modus-Abfrage. Je Stelle gibt es eine Probe und eine Mutationsprobe mit Gegenprobe; jede beisst allein. Mit vollständigen Eingaben ändert sich keine Zahl: Benchmark `64fb2912` im Modus (Repo und Klon) und ohne Modus, Auswertung auf Beispieldaten `fc178106`, sieben von acht Werkzeugausgaben bytegleich, der Plan nur um die zwei toten Schlüssel kürzer.

**Tatsachennotizen A8** (Frage „erreicht die registrierte Eingabe den Zweig?“):

| | Notiz | jetzt |
|---|---|---|
| A1 | nein: alle neun Bots haben innere Kalenderjahre in der TB-24-Eingabe | 2 |
| A2 | nein: keine Zählung leer | 2 |
| A3 | nein: 77 Falten in `64fb2912`, keine mit 0 Handelstagen; Falten = Plan | 2 |
| A4 | nein: jeder Plan hat Selektionsfalten | 2 |
| A5 | Rechenregel: `t[0,01]·e/0,01` → 0 für e → 0, an 86 Tabellen bis 1,4·10⁻¹⁷ belegt | unverändert |
| A6 | Rohergebnisse gibt es noch nicht; Beispieldaten 0 Treffer; `lies_zellen()` schliesst den Zweig bei nicht leeren Selektionsfalten aus | 2 |
| A7/A7b | nein: alle Pläne endgültig mit Selektionsfalten; Beispieldaten 0 Treffer | 2 / direkter Zugriff |
| A7c | nein: nur `t3_supertrend` trägt Text, den bekannten | 2 |

**A10:** `auswertung.Abbruch` erbt von `SystemExit` und wird mit Text geworfen. Er endet mit **1**, direkt wie im Ablauf (`auswertung.py --rohergebnisse <leer>`). 12 Stellen `raise Abbruch` (der Auftrag nannte 13). Nicht geändert.

**A11:** `TB30A_BASE_DIR` setzen nur Tests (`test_vorregistrierung` `_umgebung`, `test_erste_falte_trockenlauf`); drei Tests löschen sie ausdrücklich. In `herkunft.py:51` greift sie **auch bei gesetzten Modus-Variablen**. Gemessen mit `TB30A_BASE_DIR=/gibt/es/nicht`: `BASE_DIR`, `REGISTERDATEI` und `commit()` folgen ihr. `register()` meldet dann die Registerdatei als `fehlend` und liefert trotzdem einen Hash; `commit()` liefert `"unbekannt"`. Nach E hängt der Datenstand im Modus nicht mehr daran (Pflichtargument), Commit und Registerdatei schon. Nicht geändert (die Öffnung galt nur dem Datenpfad).

**E5:** Im Modus hasht `--anhaengen` den Snapshot: `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, 223 Dateien = der registrierte Datenstand. Gemessen im Wegwerfbaum auf den echten Snapshot.

**Hashes nach 37.3:** `register()` `57ec6573…` ⇒ `0ece95e2…`. Neues Abbild `sperrliste_abbild_2026-09-25b.json` `40ffe18d…`. Die Sonde gegen das alte Abbild zeigt Befund genau an 2, 3, 4, 5, 6, 11, 12, 14; gegen das neue ist sie ohne Befund an den Pfaden.

**Zweite Deutungsstelle:** `registerdaten.py:605` (`zellen()`) vergleicht den `_bedingung`-String selbst. Nicht geändert (Punkt 1), Tatsachennotiz bis 40.8 (h), wie 25c 1 es sagt.

**Drei Befunde beim Bau:**

1. ⭐ **Die Regel aus A1/A2 steht ein zweites Mal, mit denselben Ersatzwerten:** `research/faltenplan_neun/faltenplan_neun.py:363-380` (`volle_jahre()` mit `or {jahre[0]: …}`, `faltenlaenge()` mit `return 2, 0.0`). `faltenplan.py` und `benchmark.py` rufen diese Kopie nicht (sie nutzen aus `faltenplan_neun` nur `BOTS`, `symbolbeginn`, `_ungebremstes_faltenjahr`; `benchmark.py` nichts davon); gerufen wird sie über `plan_fuer_bot()` → `faltenplan_neun.faltenplan()`, also vom Werkzeug `faltenplan_neun.py --json` (G2 Ausgabe 1). Sie ist nicht freigegeben und nicht geändert.
2. **`registerbericht.py --pruefen` war schon vor TB-106 rot:** Der Zahlenteil im Register (Z. 392 ff.) ist veraltet. B2 ändert am erzeugten Block genau eine Zeile.
3. **Die Prüfansicht `herkunft.py` endet unter dem Modus jetzt mit 2** (Abschnitt 5). Das ist die Folge von „keine Voreinstellung unter dem Modus“.

**Fragen:**

1. Soll die zweite Kopie in `faltenplan_neun.py` (Befund 1) mit TB-107 dieselbe Behandlung bekommen, oder ist sie ausserhalb des Laufbereichs eine Tatsachennotiz?
2. Soll die Prüfansicht `herkunft.py` unter dem Modus ebenfalls `paths.DATA_DIR` übergeben (eine Zeile, wie `--anhaengen`)? Oder ist rc 2 dort richtig, weil die Prüfansicht kein Lauf ist?
3. `TB30A_BASE_DIR` in `herkunft.py` (A11) wirkt unter dem Modus weiter auf Commit und Registerdatei. Gehört sie unter dem Modus verboten wie `TB36_BASE_DIR` (TB-104), und dann in welchem Auftrag?

## 10. Abweichungen vom Auftrag

| | |
|---|---|
| 1 | **A9 nur statisch:** `crontab -l` vom Werkzeug abgelehnt |
| 2 | **A7b-Probe mit rc ≠ 0 statt rc 2:** Nach D2 ist der Zweig unerreichbar. Die Probe zeigt, dass eine unvollständige Bereinigung nicht mehr still `c = False` ergibt (`KeyError`, rc 1), und statisch, dass `ein_bot()` kein `bereinigung.get(` mehr trägt; beide mit Mutationsprobe |
| 3 | **Die neuen Proben stehen in einer eigenen Datei** `test_ersatzwerte.py` im selben Ordner (freigegeben: „neue Proben im selben Ordner“). Sie ist mit Block E committet, weil sie B–E gemeinsam enthält; B–D liefen vor ihrem Commit je Teil grün |
| 4 | **G2 Plan im Speicher** (`plan.json` aus `faltenplan.faltenplan()`), wie TB-105 F3; `python3 faltenplan.py` lief nie |
| 5 | Der Auftrag nannte 13 `Abbruch`-Stellen; gezählt sind 12 |
| 6 | Die Prüfansicht `herkunft.py` unter dem Modus (Abschnitt 5, Frage 2): Folge von E1, nicht eigens beauftragt |

## 11. Was NICHT geschah

- Nicht angefasst: `registerdaten.py`, `kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`, `sperrlistensonde.py`, `sperrliste_abbild.py`, `faltenschranke_messung.py`, `shared/strategy_paths.py`, `shared/paths.py`, `research/universum_trockenlauf/`, `research/faltenplan_neun/`, die drei Cron-Wächter, alle `strategies/`, `crontab`, das Register.
- Unter `ergebnisse/` ist nur das neue Abbild dazugekommen; keine Tabelle, kein Plan, keine Messgrösse neu geschrieben.
- `herkunft_protokoll.jsonl` wurde nicht beschrieben und nicht angelegt; es existiert weiterhin nicht.
- `auswertung.Abbruch` (rc 1) nicht geändert.

## 12. Hashes nachher (H1)

Siehe `h1_vergleich.txt`: geändert gegenüber `5_alle_vorher.txt` sind nur die fünf freigegebenen Dateien, `test_vorregistrierung.py`, die neuen `test_ersatzwerte.py` und `sperrliste_abbild_2026-09-25b.json`. Gleich sind: alle gesperrten und nicht freigegebenen Dateien (Abschnitt (2)), alle Dateien unter `ergebnisse/` ausser dem neuen Abbild, der Snapshot (Summenhash und `--pruefen` Soll = Ist), der Datenstand `d9449faf…` (223) und **alle 12 `*.db`** (kein Cron-Schreiber in der Sitzungszeit). `herkunft_protokoll.jsonl` existiert vorher und nachher nicht. `git status` ausserhalb `docs/` leer. `register()` wie in F3.

## 13. Für die Folgesitzung vorbereitet (TB-107)

- **`_min_history`** in `research/faltenplan_neun/faltenschranke_messung.py`, samt `kerzen_elliott_wave()` (stiller Hinweis) und `loader_lesart()` (`TypeError`, rc 1): Regel aus 25c 4 (2) – `re.findall`, genau ein Treffer, sonst 2, unabhängig vom Modus; Mutationsproben „zwei Treffer“ und „kein Treffer“.
- **`getattr(paths, "selektionsmodus", None)`** in `shared/strategy_paths.py` entfernen (25c 4 (3)(b)); die zwei Proben `test_paths` A und `test_strategy_paths` C4 brauchen dann ein `paths` mit der Funktion.
- **`$TMPDIR/tb40_lauf_*`** in `research/universum_trockenlauf/universum_trockenlauf.py`: im Benchmark-Lauf 10 `mkdir` + 10 `w` (G1, unverändert seit TB-104).
- **Gegenprobe über alle `__main__`-Stellen** des Laufbereichs (25c 4 (3)(a)).
- Dazu aus diesem Ergebnis: Befund 1 (die Kopie von A1/A2 in `faltenplan_neun.py`), falls Fable sie in TB-107 haben will.
- **Wiederverwendbar:** die Bauart von `test_ersatzwerte.py` (Kopie + eine Mutation je Stelle; Wegwerfbaum mit echter `paths.py` und Snapshot-Attrappe für `herkunft.py`), `g_lauf.sh` (Modus-Lauf; aus einem Klon mit dem Skript des Repos aufrufen), `g2_ausgaben.sh`, `g3_auswertung.sh`, `hashes.sh` (mit Einzelhashes unter `ergebnisse/` und `register()`), `e5_herkunft.py`.

---

## In einfacher Sprache

Die drei Programme, die im Auswahllauf den Zeitplan, die Vergleichstabelle und das Urteil rechnen, hatten sieben stille Notlösungen: Fehlte ein Wert, nahmen sie 0 oder eine feste Zahl und rechneten weiter. Jetzt brechen sie an jeder dieser Stellen mit einer klaren Meldung ab. Für jede Stelle gibt es eine Probe, die das zeigt, und eine Gegenprobe, die zeigt, dass die Probe die alte Notlösung wirklich erkennen würde. Mit den echten Daten wird keine dieser Stellen erreicht – deshalb hat sich an keiner Zahl etwas geändert.

Eine achte Stelle sah wie eine Notlösung aus, ist aber eine echte Rechenregel. Sie bleibt, und der Beleg dafür steht oben.

Zwei Felder aus einem verworfenen Verfahren sind aus dem Zeitplan verschwunden, ebenso die passende Berichtszeile. Ein unbekannter Parametertext führt jetzt zum Abbruch.

Das Herkunftsprogramm bekommt im geschützten Modus den Datenordner des eingefrorenen Datenstands übergeben. Es legt keinen fehlenden Ordner mehr still an. Gemessen: Es hasht dann genau den registrierten Datenstand.

Weil diese Dateien auf der Sperrliste stehen, gibt es ein neues Abbild der Sperrliste. Die Vergleichstabelle kommt im Projekt, in einer frischen Kopie und ohne geschützten Modus Byte für Byte gleich heraus.

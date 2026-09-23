# TB-92 — Ergebnis: Vollzug Punkt 8 — die drei Leser lesen die Neurechnung, der Modus-Nachweis ist bytegleich, ⛔ `test_vorregistrierung.py` bleibt ROT (163/2) ⇒ Block C und D entfallen

**Sitzungstitel:** `TB-92` · **Stand:** 23.09.2026 · **Auftrag:**
`docs/auftraege/MAC_TB-92_vollzug_punkt8.md` · **Belege:** `docs/belege/TB-92/`
**Eingang:** `ad94b38` · Commits: `d136251` (Schritt 0, Arbeitsbaum des steuernden
Chats), **`0292e92`** (Block A/A1a in **einem** Commit, dazu die Belege A1–A5 und A1b),
Abgabe-Commit (Beleg B, dieses Dokument, Journalblock CU).
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Kurz:** Block A, A1a und A1b sind ausgeführt und belegt. Der Test läuft
jetzt **bis zur Schlusszeile durch**, der Absturz `KeyError: '2017'` ist weg. Er
ist aber **nicht grün**: **163 bestanden, 2 gescheitert** (`G6`, `H3`), rc 1,
501 s. ⇒ Nach B3 **entfallen Block C und D**. Damit fehlen auch Registertext,
Marken, neues Abbild und Tatsachennotizen (Fables Schritte 1, 2, 4 und 5). Der
Vollzug ist **im Code** erfolgt, **im Register nicht**.

---

## 0. Schritt 0

| | |
|---|---|
| Arbeitsbaum | 4 geänderte und 2 neue Dateien des steuernden Chats → `d136251` (`settings.local.json` mit `add -f`). Danach **leer** |
| Git-Sperrdateien | `find .git -name '*.lock'` → **keine**. Im Scratchpad eine fremde `requirements.lock` (andere Sitzung, kein git-Lock) |
| Freigaben | (1) Fable 23c ✔ (Datei im Repo), (2) Betreiber 18:12 ✔ (laut Auftrag), (3) Fable 23d und (4) Messbitte (b) ✔ (laut Auftrag und Anfrage 23g). ⚠️ **Die Antworten 23d und 23e liegen NICHT im Repo** (`FABLE_ANTWORT_2026-09-23d/e` fehlen). Ihr Wortlaut ist nur als Zitat im Auftrag vorhanden. Ich habe danach gearbeitet und vermerke es hier |

⚠️ **Während der Sitzung** hat der Betreiber `ARBEITSWEISE.md` (Abschnitt 17,
+51) und `sitzungswaechter/LIESMICH.md` (+75) geändert. Dazu gab es keine
Anweisung. Ich habe beide **nicht** committet (ARBEITSWEISE: eine Datei ohne
Anweisung ist keine Sitzungsentscheidung).

## 1. Block A/A1a — der Vollzug im Code (`0292e92`)

⚠️⚠️ **Der Auftrag widerspricht sich an drei Stellen. Aufgelöst habe ich sie
nach der jüngeren und verbindlichen Stelle (Fable 23c Schritt 1 „Form (ii)“,
Fable 23d):**

| Stelle im Auftrag | Widerspruch | wie ausgeführt |
|---|---|---|
| A2 „wird die registrierte Datei“, 1(c) „Henne-Ei“ | Beides setzt voraus, dass die Datei **ersetzt** wird (Form (i)). Nach 5b/23c gilt aber Form (ii): `benchmark_drawdowns.json` bleibt, und sie ist `deny` | Nicht ersetzt, `a163c498…` vorher = nachher. **Die Leser wurden umgelenkt** |
| A3 „nur diese eine Stelle“ (Z. 178) | Unter Form (ii) liest `registerbericht.py` in Z. 64 den **festen alten Pfad**. Nur Z. 178 zu ändern hätte an der alten Tabelle gebrochen (`symbole_handelbar_in_falte` fehlt dort) | Drei Stellen: Z. 64 liest `aw.BENCHMARK_TABELLE`, Z. 157 (Pfadnennung im Block) kommt aus der Konstante, Z. 178 heisst jetzt `symbole_handelbar_in_falte`. ✔ Der alte Schlüssel kam genau **1**-mal vor |
| 1(d)/§3/§7 „`auswertung.py` wird nicht angefasst“, §7 „keine Änderung an `test_vorregistrierung.py`“, Abbruch 4 | Überholt durch A1a (Fable 23d), das beide Änderungen **verlangt** | ausgeführt nach A1a |
| A1a-2 gegen A1a-4 | Wenn `main` die Konstante liest, **kann** sein Körper nicht unverändert bleiben | gemessen, siehe unten: genau diese eine Stelle |

| | Ergebnis | Beleg |
|---|---|---|
| **A1** Hashes vorher | `benchmark_drawdowns.json` `a163c498…`, `…_nach_wegA.json` `64fb2912…`, `registerbericht.py` `2b1ce24a…`, `auswertung.py` `1c2e2dae…`, `test_vorregistrierung.py` `55553739…` | `a1_hashes_vorher.txt` |
| **A1a-1/2** | `auswertung.py`: `BENCHMARK_TABELLE = os.path.join(_HIER, "ergebnisse", "benchmark_drawdowns_2026-09-23_nach_wegA.json")` direkt nach `BASE_DIR`. `main` öffnet sie. **Kein** argparse-Argument | `git show 0292e92` |
| **A1a-3** | `test_vorregistrierung.py::_tabellen` und `registerbericht.py::block` lesen `aw.BENCHMARK_TABELLE`. ⚠️ **`beispieldaten.py` liest keine Tabelle** (grep 0 Treffer; es erzeugt Rohergebnisse und Benchmark-Tagesreihen) ⇒ dort ist nichts umzustellen, Hash `3e547014…` unverändert. Repo-weit gibt es genau drei Leser (wie in TB-88) | grep in der Sitzung |
| ⭐ **A1a-4** AST | 27 Funktionen/Klassen (mit `ast.walk`): **26 gleich**, verschieden nur `main`, und zwar nur im Argument von `open`. Auf Modulebene 17 → 18, **genau eine neue Zuweisung** `BENCHMARK_TABELLE`, keine entfernt | `a1a_ast_vergleich.py/.txt` |
| **A1a-5** Hashes | `auswertung.py` `1c2e2daec562d9973f87809fd29ef369db76614ee4bc31c04c6ca201c52a3db0` → **`c3b4e69d8f207d0c1982a538203dcf184072554fdc1beb0f612bf054cd2a0062`** · `registerbericht.py` `2b1ce24a…` → `dace1b01…` · `test_vorregistrierung.py` `55553739…` → `6e7defef…` | `a5_hashes_nachher.txt` |
| **A1a-6** | `herkunft.py` **nicht geöffnet**, `56a1c2e1…` unverändert. ⚠️ **Tatsache:** `register()` hasht über `EINGEFROREN` damit weiter `ergebnisse/benchmark_drawdowns.json`, **nicht** die Tabelle, die der Lauf liest. Nach Fable 23d schützen Punkt 4 und das Abbild die neue Tabelle. **Beides steht noch aus** (Block D) | `herkunft.py` Z. 57–61, 109–123 |
| **A4** | `registerbericht.py` rc **0**. Der Benchmark-Block nennt **alle neun** Bots (fünf Tabellen und vier Zeilen „teilt Universum und Faltenplan“) und den Pfad der Neurechnung | `a4_registerbericht_ausgabe.txt` |
| ⚠️ `--pruefen` | vorher **rc 1**, nachher **rc 1**. Der ERZEUGT-Block im Register (Z. 230–430) war **schon vor TB-92 veraltet**: 26 Differenzzeilen gegen den alten Code, darunter die Falten-Tabelle mit „Platzhalter (TB-31)“. Gegen den neuen Code sind es 95. Nicht neu erzeugt (das wäre eine Ersetzung im Register, nicht beauftragt) | `registerbericht_pruefen_vorher.txt`, `a4_…_nachher.txt` |
| **A5** | Hashes nachher: alle Tabellen gleich, `benchmark.py` und `faltenplan.py` gleich. Die Marke bei Abschnitt 10 Punkt 4 ist **nicht** berichtigt (Block D entfällt) | `a5_hashes_nachher.txt` |
| **A6** | Die Sonde gegen `sperrliste_abbild_2026-09-22.json` meldet jetzt **rc 1 an den Punkten 2, 3, 4, 5, 6, 14**, vorher 2, 4, 6. **Neu sind 3, 5, 14**: Das ist **ein** Übergang, `auswertung.py` `1c2e2dae…` → `c3b4e69d…`, planmässig nach 37.3. Punkt 4 ändert sich **nicht** durch die Tabelle (sie ist noch kein Pfad des Punkts), sondern bleibt 1 wegen `benchmark.py`. Prüfung (ii) bleibt 0 | `sonde_vorher.txt`, `sonde_nachher.txt` |

## 2. ⭐ Block A1b — der Modus-Nachweis (Fable 23e): BYTEGLEICH

| | |
|---|---|
| Hilfsordner | Scratchpad: `data/` enthält 223 Einzelverknüpfungen auf die CSV der Snapshot-Wurzel `snapshots/63e4b6c8bb71dc37…/`, `config/` verknüpft `<Snapshot>/config/`, alle anderen Repo-Ordner sind verknüpft (Code). `TB30A_BASE_DIR=<Hilfsordner>` |
| Code-Commit | `d136251` (`benchmark.py` `d6bdd558…`, `faltenplan.py` `7aa0b8cc…`). Datenstand: Snapshot `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2`, MANIFEST-`datenstand_hash` `d9449faf…` (Anfrage 23g, 225/225) |
| ⭐ **Ergebnis** | **Vier Läufe, alle rc 0, je 51–52 s, alle bytegleich** `64fb2912f1a2ffb02a36834857fe9a91529b7517a8a7185f5fd7b11642f873b7` mit `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json`. Ziel von Lauf 1: `docs/belege/TB-92/benchmark_modusnachweis.json`, die übrigen im Scratchpad, **nichts in `ergebnisse/`** |
| ⭐ Lesequellen | Lesehaken über `sys.addaudithook`. Lauf 3/4 laufen prozessübergreifend über `sitecustomize`, **11 Prozesse**. Ergebnis: **0 Lesezugriffe auf `data/` oder `config/` des Repos**, 222 CSV und 2 Universumsdateien aus dem Snapshot. Dazu kommen Eingaben **ausserhalb** des Snapshots: `ergebnisse/messgroessen.json` und die neun `research/tb24_haltedauern/daten/*_alle_trades.csv` (über den Faltenplan) |
| Modus | `TB_SELEKTIONSWURZEL` wirkt hier nicht (0 Treffer in `research/vorregistrierung/`). Der „Modus“ ist die Umlenkung über `TB30A_BASE_DIR` auf den Snapshot, wie in TB-93 |
| Anläufe | Der erste Hilfsordner mit nur drei Code-Verknüpfungen scheiterte am Import von `universum_trockenlauf`, ohne etwas zu schreiben. Die erste Fassung des Kinderhakens verlor ihr Protokoll an der Schreibsperre von `loaderlauf.py`. Beides ist verworfen, die Reste liegen als `_verworfen_*` im Scratchpad |

⭐ **A1b-6, der Pfad-Befund für Fables Sonde „Lesequellen“ (kein Auftrag hier):**

1. `benchmark.py` (Z. 93/95) und `messgroessen.py` lesen an `shared/paths.py`
   vorbei (bestätigt).
2. ⚠️ **Neu:** Die Kindprozesse des Faltenplans folgen **eigenen**
   Umgebungsvariablen, `faltenplan_neun.py` `TB36_BASE_DIR` (Z. 110) und
   `universum_trockenlauf.py`/`loaderlauf.py` `TB40_BASE_DIR`. Gemessen haben sie
   hier trotzdem aus dem Snapshot gelesen, vermutlich über den übergebenen
   Datenordner. Der Weg ist aber ein anderer als `TB30A_BASE_DIR`.
3. ⚠️ **Neu:** Der Lauf öffnet `logs/notifications/manuelle_eingriffe.log` im
   Modus `a` (Import aus `notifications/`). Die Datei blieb unverändert (mtime
   11.09.).
4. Zwei Eingaben des Laufs (`messgroessen.json`, TB-24-Trades) liegen **nicht**
   im Snapshot. Das gehört zu TB-94 und Anfrage 23f (4).

## 3. ⛔ Block B — der Test ist ROT

| | |
|---|---|
| Aufruf | `trading-env/bin/python3 research/vorregistrierung/test_vorregistrierung.py`, HEAD `0292e92`, Start 16:42:40Z |
| ⭐ | **Teil A bis H durchlaufen, Schlusszeile erreicht.** Der `KeyError: '2017'` ist weg |
| ⛔ **Ergebnis** | **rc 1 · 163 bestanden, 2 GESCHEITERT · 501 s** |
| `G6` | `elliott_wave - 2020 und 2022 sind Testfalten, keine Trainingsjahre - ['2018-2019', '2020-2021', '2022-2023', '2024-2025', '2026-01-01/2026-09-01']` |
| `H3` | `ohne die gesetzte Null aendert sich die Statistik - 'Netto-Sharpe (Med.) 0.1000' / 'Netto-Sharpe (Med.) 0.1000'` |

⇒ **Nach B2/B3: rot, so gemeldet, nicht nachgebessert. Block C und D
entfallen.** Nur zur Einordnung, ausdrücklich nicht als Block C: Es sind
**dieselben zwei Namen und dieselbe Zahl** wie in den Simulationen von TB-88 und
TB-90 (163/2). Zum ersten Mal sind sie aber **am echten Stand** gemessen, nicht
in einer Wegwerf-Kopie.

⚠️ **Zur Entscheidung (Fable/Betreiber):** Fables 23c Schritt 3 verlangt, dass
der Test *„durch bis zur Schlusszeile“* läuft, und hält `G6`/`H3` als eigenen
Punkt aus 23a. **Das ist erfüllt.** Der Auftrag (B3, Block D) und das
Fertigkriterium in 38.4 (Register Z. 6775) verlangen dagegen **„grün“**. **Das
ist nicht erfüllt.** Ich bin dem Auftrag gefolgt und habe abgebrochen. Welches
Kriterium gilt, entscheidet nicht diese Sitzung.

## 4. Was deshalb NICHT geschehen ist

- **Kein Registertext** (kein Abschnitt 39), keine Marke bei 10/4, 37.2 oder 38.4, keine Tatsachennotizen (Fables Schritte 1, 2, 5; A1a-5, A1b-4, A6 und die Notiz zu N stehen nur hier).
- **Kein neues Abbild** (Schritt 4). Die Sonde meldet deshalb weiter rc 1 an sechs Punkten.
- **Sonde nicht geändert:** Die Zusammenfassung je Datei (Fables Handwerksregel) und die leere Gruppe „bestimmt“ waren gebaut und getestet (**53/53**, vorher 49/49). Ihr Text verweist aber auf den Registerabschnitt, der nicht geschrieben ist. Deshalb habe ich den Entwurf als `sonde_je_datei_entwurf.patch` gesichert und per `git apply -R` zurückgenommen (ein `git checkout` war abgelehnt worden). `shared/sperrlistensonde.py` entspricht HEAD.
- Nicht angefasst: `benchmark.py`, `faltenplan.py`, `messgroessen.py`, `herkunft.py`, `beispieldaten.py`, alle Dateien in `ergebnisse/`. `python3 faltenplan.py` wurde nicht aufgerufen. `benchmark.py` lief nur mit `--ziel` ausserhalb von `ergebnisse/` (A1b, beauftragt).

## 5. Für die Folgesitzung vorbereitet (gemessen, nicht eingetragen)

| | |
|---|---|
| Zellenzahl | je Bot 80/384/400/96/320/320/400/96/320, **Summe 2416**, wie Register Z. 380. N = 653 (Festlegung 10) unberührt (`d_zellenzahl.txt`) |
| Hash-Übergänge für 37.3 | `faltenplan.py` `6f96b95d…` → `fd3e5018…` (TB-86, `4daa254`, in 37.3 notiert) → `7aa0b8cc…` (TB-90, `303a7fd`, Freigabe 22.09.) · `benchmark.py` `3960375a…` → `d6bdd558…` (TB-91, `31008b6`, Freigabe 23.09. 10:40), Punkte 4 und 6 · `auswertung.py` `1c2e2dae…` → `c3b4e69d…` (TB-92, `0292e92`, Freigabe 23.09. 18:12 + Fable 23d), Punkte 3, 5, 14. Keiner davon steht bisher im Register |
| Einfügestelle Punkt 4 | nach Z. 870 (`   Interpolationsregel**`) eine Pfadzeile, Marke nach Z. 880. **Vor** dem neuen Abbild setzen (die Sonde vergleicht den Listentext) |

---

## In einfacher Sprache

Die drei Programme, die die Vergleichstabelle lesen, lesen jetzt die neu
gerechnete Tabelle. Umgestellt ist das über **einen** festen Eintrag, ohne
Schalter. Das eingefrorene Auswertungsprogramm hat sich dabei an genau einer
Stelle geändert, sonst nirgends. Die neue Tabelle lässt sich aus dem
eingefrorenen Datenbestand Byte für Byte wiederherstellen. Nachgeprüft ist
auch, dass dabei keine einzige Kursdatei aus dem Arbeitsverzeichnis gelesen
wurde.

Das Prüfprogramm stürzt nicht mehr ab und läuft bis zum Ende. **Grün ist es
aber nicht:** Zwei von 165 Prüfungen scheitern, dieselben zwei, die schon
vorher bekannt waren. Der Auftrag sagt für diesen Fall: aufhören und melden.
Der Registereintrag und das neue Schutzabbild sind deshalb nicht gemacht.
Ob „läuft bis zum Ende“ genügt oder ob es „grün“ sein muss, entscheiden
Verfahrensprüfer und Betreiber.

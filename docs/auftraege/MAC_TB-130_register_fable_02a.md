# TB-130 Register — Fable 02a (R63–R65) als Abschnitt 52, zwölf Marken am alten Ort; Registerkopie, Index und Dialog-Index nachziehen

**Sitzungstitel:** `TB-130` · **Modell:** Opus 5.5, Aufwand hoch (Registerauftrag, wie TB-129) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 02.10.2026 vom steuernden Chat
**Vorgänger:** TB-129 (`1833839`). **Dieser Auftrag:** `docs/auftraege/MAC_TB-130_register_fable_02a.md`, er wird in Schritt 0 mitcommittet. **Interpreter:** immer `trading-env/bin/python3` (7c). **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15). Ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.
**Prüfwerkzeuge:** Jedes Skript dieser Sitzung liegt unter `docs/belege/TB-130/` und wird mitcommittet, auch Vergleichsskripte.
**Bauart: TB-129.** Der Auftrag `docs/auftraege/MAC_TB-129_register_fable_01a.md` und die Skripte unter `docs/belege/TB-129/` sind die Vorlage; sie werden übernommen und angepasst, nicht neu erfunden. Wo dieser Auftrag „wie TB-129“ sagt, gilt der dortige Schritt mit den hier genannten Werten. Wo beide sich widersprechen, gilt dieser Auftrag. **Massgeblich für Überschriften, Ketten, Marken und Fundstellen ist Anhang A** (Daten-Block), gebaut und geprüft vom steuernden Chat am 02.10.2026 am Register `f63ad4c`.

## ⭐⭐ Freigabe des Betreibers, wörtlich

**02.10.2026, Auswahlkarte im steuernden Chat (gestellt 14:52, Antwort eingetragen 15:09).** Kartentext: *„Gibst du TB-130 frei? Das umfasst: Register Abschnitt 52 anhängen (R63–R65 zeichengleich, dazu 52.4–52.5 mit den Messungen des steuernden Chats), zwölf Marken am alten Ort (fünf nach R65 (b), sieben vom steuernden Chat nach R65 (a) bestimmt; keine in Abschnitt 9, 10 und im ERZEUGT-Block), Registerkopie, Index und Dialog-Index neu, BACKLOG-Block, Journal EB. Kein Code, kein neues Abbild.“* Gewählt: **„Freigeben wie beschrieben (Empfohlen)“**.

| freigegeben | Pfad / Handlung |
|---|---|
| Register **anhängen** (Abschnitt 52: 52.0 Kopf, 52.1–52.3 = R63–R65 zeichengleich, 52.4–52.5 Text des steuernden Chats) und **zwölf Marken additiv** am alten Ort (Anhang A) | `docs/VORREGISTRIERUNG_neuselektion.md` |
| neu erzeugen, nachziehen | `docs/projektfuehrung/register_kopie/REGISTER_KOPIE_ABSCHNITT_<nn>.md`, `docs/projektfuehrung/REGISTER_KOPIE_teil<n>.md` (beide über `docs/werkzeuge/registerkopie.py`), `docs/projektfuehrung/REGISTER_INDEX.md` |
| die Zeile für 02a, die Zeile 01a (offen → nein) und die Schlusszeile (das Werkzeug `docs/werkzeuge/dialog_index.py` schreibt die Datei neu; was es dabei sonst ändert, steht im Ergebnis) | `docs/projektfuehrung/FABLE_DIALOG_INDEX.md` |
| ein Block (Schritt B) | `docs/projektfuehrung/BACKLOG.md` |
| Journalblock (Kennung messen, erwartet **EB**) | `docs/projektfuehrung/JOURNAL.md` |
| committen in Schritt 0 | dieser Auftrag, `docs/auftraege/AKTUELLER_AUFTRAG.md`, `docs/projektfuehrung/UEBERGABE.md` und, unter `docs/projektfuehrung/`, die drei Dateien `FABLE_ANFRAGE_2026-10-02a_…`, `FABLE_ANTWORT_2026-10-02a_…`, `FABLE_UEBERGABE_2026-10-02_eroeffnung.md` |
| Belege, Ergebnis | `docs/belege/TB-130/`, `docs/ERGEBNIS_TB-130_register_fable_02a.md` |
| verwerfen, nur nach rotem Nachweis in A5 und nachdem der Diff als `abbruch_register.diff` gesichert ist | die eigene, uncommittete Änderung am Register (`git checkout -- docs/VORREGISTRIERUNG_neuselektion.md`) |

⛔ **Nicht freigegeben, mit Grund:**
- **Jede Zeile im Listentext von Abschnitt 10** und **im ERZEUGT-Block von Abschnitt 3.** *Grund:* Sonde (36.6, Prüfung (ii)) und `registerbericht.py --pruefen` vergleichen sie; R65 (d) verlangt ausdrücklich, dass in Abschnitt 10 weiter keine Marke steht.
- **Jede Änderung oder Löschung einer bestehenden Registerzeile.** *Grund:* Das Register ist append-only; Marken sind neue Zeilen (34). Nachweis: numstat zweite Spalte 0. Die bestehenden `**Kette:**`-Zeilen bleiben, wie sie sind.
- **Eine Marke, die nicht in Anhang A steht.** *Grund:* Die Sitzung baut die Markentabelle nicht selbst (ARBEITSWEISE 0, Fehler Nr. 9).
- **Code jeder Art**, insbesondere `research/`, `shared/`, `strategies/`, `docs/werkzeuge/`. *Grund:* Textauftrag. Die Wache aus R64 (c) und die Probe aus R64 (d) sind **nicht** Gegenstand; sie kommen mit dem Zellen-Erzeuger.
- **Ein neues Abbild der Sperrliste.** *Grund:* Keine Sperrlistendatei bewegt sich.
- **Läufe von `auswertung.py`, Zellen-Erzeugern oder Backtests.** *Grund:* Sichtschutz. `registerbericht.py --pruefen` ist kein solcher Lauf und in 0b und A5 verlangt.
- Löschen oder Verwerfen ausser dem einen Fall in der Tabelle; `crontab`, Datenbanken; `UEBERGABE.md`, `UEBERGABE_ARCHIV.md` und die Dateien `FABLE_ANTWORT_*`, `FABLE_ANFRAGE_*`, `FABLE_UEBERGABE_*` ändern (ausser dem Commit in Schritt 0). *Grund:* Das sind die Quellen.

**Sichtschutz 27.1:** Diese Sitzung liest keine Kennzahl, keine Trade- und keine Zeilenzahl aus Ergebnisdateien. Aus Testausgaben nur rc, Dauer und Schlusszeile. Code wird nur gelesen, wo Anhang A eine Fundstelle nennt.

## Belegt · erschlossen · offen

*Gemessen vom steuernden Chat am 02.10.2026, 14:20–15:00, über die Geräteanbindung, nur lesend, an HEAD `1833839` (= `origin/main`).*

**Belegt:**
- Register: 11 225 Zeilen, sha256 `7f74b0e5a746cbc720b7b7c20af83acddd32d6652c3b57099f18769d3d4b16c4`, md5 `b4764e4e140caa37ecef515d73743e1f` (ERGEBNIS_TB-129; `docs/belege/TB-129/a5_messung_nachher.txt`). Letzter Commit, der es änderte: `f63ad4c`. Letzter Abschnitt: 51 (letzter Unterabschnitt 51.10). Die Datei endet mit einem Zeilenumbruch.
- Quelle der R-Blöcke: `docs/projektfuehrung/FABLE_ANTWORT_2026-10-02a_exposure_tage_laufbereich_marken.md`, md5 `a7821eeb4f61faad5f74f72ec7201797`, 21 709 B, 120 Zeilen, uncommittet bis Schritt 0. Codezaun Z. 111 bis Z. 120; Blöcke R63–R65 in Z. 112–119. Zwei unabhängige Abschriften aus der Ablage, `cmp` gleich; `project_read` lieferte Text, keine Datei.
- **Schnittregel (maschinell geprüft, 3/3):** wie TB-129. Ein Block beginnt mit der Zeile, die mit `R<n> — ` beginnt, und endet einschliesslich der ersten folgenden Zeile, die mit `Quelle des Grundes:` beginnt; je Block genau zwei Zeilen. Geschnitten wird **nur** in Z. 112–119.
- Ausgangswerte (ERGEBNIS_TB-129; `docs/belege/TB-129/a5_messung_nachher.txt`): `herkunft.register()` `a1e1366ab55719fe4724b9da3d9425f3029628d56460bcda8e2e4476dce8cc40`, `fehlend []`, 23 Teile · gültiges Abbild `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json`, sha256 `46f0ad5d1d83a253baa5523f5657881e0d825cebd734f24a42ef5d4fa74f281f` · Sonde dagegen: rc 2 (Normalfall), 37/0/0, (ii) 0, „Listentext wie bei Erzeugung: ja“, sha256 des JSON-Berichts ohne das Feld `zeilen` `9f7364ef32fd80ffba6931c776f3bdf43dc257a1f6aeac304cf818c89023f35e` · `registerbericht.py --pruefen`: rc 1 (bekannter Befund; verglichen wird nachher gegen vorher) · `test_vorregistrierung` 196/196, rc 0, 865 s, mit diesem Register (`docs/belege/TB-129/a5_test_vorregistrierung.txt`).
- Seit `1e13135` ist unter `research/`, `shared/`, `strategies/`, `config/`, `data/` nichts geändert (TB-129 0c; seither nur `docs/`).
- `registerkopie.py --pruefen` und `--abschnitte --pruefen` am `1833839`: je rc 0, 52 Abschnittsdateien.
- `FABLE_DIALOG_INDEX.md`: 51 Antworten, Zeile `01a` mit offen = ja, keine Zeile `02a`. `BACKLOG.md`: 271 Zeilen, der Anker `## 6 — Geparkt, null Arbeit` zählt 1, `Aus Fable 02a` zählt 0.
- Nummern: TB frei ab 131 · Journal **EB** (die Sitzung misst) · R-Blöcke nach diesem Auftrag frei ab R66.

**Erschlossen:** Eine der zwölf Marken steht vor Abschnitt 10 (4.2, drei Zeilen); der Abschnitt wandert um drei Zeilen, der ERZEUGT-Block in Abschnitt 3 nicht. Der Text der Sonde ist dann nicht mehr bytegleich, der JSON-Bericht ohne das Feld `zeilen` schon (wie TB-129).

**Offen (die Sitzung misst, nimmt nichts an):** die Journal-Kennung; die neuen Zeilenbereiche und Teilgrenzen der Registerkopie; welche weiteren Zeilen `dialog_index.py` ändert.

## Schritt 0 — Sicherung, Ausgang, Vorprüfung

**0a. Zuerst, bevor `docs/belege/TB-130/` entsteht:** `git status --porcelain > "$TMPDIR/tb130_0a.txt"`. Soll: genau die Einträge unten; die Reihenfolge zählt nicht. Weicht etwas ab ⇒ Abbruch. Danach die Datei nach `docs/belege/TB-130/0a_status.txt` kopieren.

*Eingetragen vom steuernden Chat am 02.10.2026 beim Ablegen:*

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-130_register_fable_02a.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-10-02a_exposure_tage_laufbereich_marken.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-10-02a_exposure_tage_laufbereich_marken.md
?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02_eroeffnung.md
```

Commit `TB-130 Schritt 0: Stand des steuernden Chats 02.10.2026, Nachmittag`, pushen. Danach steht für alle Quellenangaben der Commit von Schritt 0, im Folgenden **⟨S0⟩** (kurz, 7 Zeichen).

**0b. Ausgangswerte** ⇒ `docs/belege/TB-130/0b_ausgang.txt`, mit `0b_ausgang.sh` nach der Vorlage `docs/belege/TB-129/0b_ausgang.sh`. Soll: die Werte unter „Belegt“; dazu md5 und Bytes der Quelle 02a, `0b_abschnitt10_vorher.txt` und `0b_erzeugt_vorher.txt`. Weicht ein Wert mit Soll ab ⇒ Abbruch.

**0c. Basis `test_vorregistrierung`:** `git diff --name-only 1e13135 HEAD -- research/ shared/ strategies/ config/ data/` ⇒ `0c_basis.txt`. Leer ⇒ die Basis ist der Beleg `docs/belege/TB-129/a5_test_vorregistrierung.txt` (196/196). Nicht leer ⇒ Basislauf am Stand ⟨S0⟩ ohne Zeitgrenze, Soll 196/196, sonst Abbruch.

**0d. Vorprüfung vor jedem Registereintrag** ⇒ `docs/belege/TB-130/0d_vorpruefung.txt`, Skript `0d_vorpruefung.py`; das Prüfskript aus Anhang A darf übernommen werden. Alles am Commit ⟨S0⟩.
1. **Marken:** Jeder Anker aus dem Daten-Block kommt im Register genau 1-mal vor, steht am Anfang der genannten Ankerzeile, und jede Einfügestelle „nach Zeile N“ beginnt mit dem angegebenen Anfang. Weicht eine Marke ab ⇒ **Abbruch vor Schritt A**.
2. **Quelle:** md5 der Antwortdatei; die Schnittregel ergibt genau R63–R65, je zwei Zeilen, in Z. 112–119.
3. **Noch nicht vergeben:** Im Register zählt `## 52.` 0, und keine Zeile beginnt mit `> R63 — `.
4. **Fundstellen für 52.4:** jede Zeile der Liste `fundstellen` (Datei, Zeile, Teilzeichenkette: die Zeile enthält sie) und jede Zählung aus `zaehlungen` (Datei, Muster, Soll) und `glob_zaehlungen` (Dateimuster, Muster, Soll je Datei, Zahl der Dateien). **Weicht hier etwas ab ⇒ Abbruch vor Schritt A.**

Commit `TB-130 0: Ausgang, Vorprüfung`, pushen.

## Schritt A — Abschnitt 52 und die Marken, in einem Lauf

**A1. Gliederung (vom steuernden Chat vergeben):** 52.0 Kopf · 52.1–52.3 = R63–R65 in der Reihenfolge des Codezauns (52.n = R(62 + n)) · 52.4–52.5 Text des steuernden Chats (A3). Überschriften und Ketten stehen exakt im Daten-Block von Anhang A. Form je R-Block wie in 51 (TB-129, A1): Überschrift, Leerzeile, die zwei Blockzeilen je mit `> ` davor, Leerzeile, Kette. Abschnitt 52 wird ans Dateiende angehängt, mit einer Leerzeile nach der letzten bestehenden Zeile.

**A2. Marken am alten Ort.** Die zwölf Marken stehen fertig in Anhang A; massgeblich ist der Daten-Block. Die Sitzung baut die Tabelle **nicht** selbst. Je Marke: eine Leerzeile, Markenzeile 1, Markenzeile 2. ⟨DATUM⟩ ist der Tag des Eintrags (TT.MM.JJJJ). Eingesetzt wird von unten nach oben; an derselben Einfügestelle steht die Marke mit der kleineren R-Nummer zuerst.

Regeln, nach denen Anhang A gebaut ist (zur Prüfung, nicht zum Neubauen): Fünf Marken zählt R65 (b) auf. Sieben weitere folgen aus R65 (a): „Gibt ein Block einem benannten Ort ein „lies“, eine Ergänzung oder eine Bestätigung, trägt der Ort die Marke, auch wenn die Aufzählung des Blocks ihn nicht nennt“. Die Orte sind die, die R63, R64 und R65 im Titel oder in (a) als Bezug nennen: 4.2 (R64 (a): „Das gilt für die mittlere Exposure je (Zelle, Falte) (4.2)“; 4.2 trägt schon die Marken aus R48 (d) und R60), 51.5 (R60 (a), R63), 51.9 (Bestätigung, R63), 48.16 (R48 (d), R64), 51.5 (R60 (b) und (c), R64), 51.6 (R61 (b), R65), 48.19 (R51, R65). Keine Marke tragen 51.8 und 51.10 (dort ändert sich der Stand einer Frage, nicht ein Befund) sowie 7 (c): R64 (a) nennt den Ort neben 4.2, aber die Präzisierungen in Abschnitt 7 tragen die Regel schon selbst („Beide Reihen werden auf gemeinsame Tage gebracht“), R64 folgt ihr, und R61 (b) führt 7 (c) als Ort ohne Marke (R54). Das geht als Frage an Fable (52.5 Nr. 9). Eine Bestätigung trägt ERGÄNZT mit dem Zusatz, was bestätigt ist (R65 (a)). Block in 47–51: nach dem Blockzitat und den dort stehenden Marken, vor der Zeile `**Kette:**`. 25.2: direkt unter dem berichtigten Satz, vor der Marke aus R53 (R65, Quelle des Grundes, 34.3). 50.1: nach der Tabelle. 50.4: nach dem Zitatblock mit dem Schlusssatz. 51.9 und 4.2: am Ende des Unterabschnitts, nach den dort stehenden Marken.

**A3. Text des steuernden Chats** — zeichengleich, mit ⟨S0⟩ und ⟨DATUM⟩ ersetzt; ⟨S0⟩ steht im Register in Backticks, wie in 51 (dieselbe Ersetzung macht das Prüfskript in A5). Der Kopf steht vor 52.1, der Schluss nach 52.3.

Kopf:

````
## 52. Fable 02a — Registerblock R63–R65 (TB-130)

Reines Eintragen von Registertext, Bauart wie 51. Quelle: `docs/projektfuehrung/FABLE_ANTWORT_2026-10-02a_exposure_tage_laufbereich_marken.md`, md5 `a7821eeb4f61faad5f74f72ec7201797`, 21 709 B, im Repo seit Commit ⟨S0⟩, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R63)“, Z. 112–119. Die Datei hat der steuernde Chat am 02.10.2026 aus Fables Ablage übertragen, zweifach unabhängig, `cmp` gleich; das Lesewerkzeug lieferte Text und keine Datei, die Bytegleichheit mit der Ablage ist deshalb nicht gemessen. Der Eröffnungstext des Chats (`docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02_eroeffnung.md`) und die Anfrage liegen seit ⟨S0⟩ im Repo; dieser Kopf nennt Datei, md5 und Commit, das ist die Bindung nach R56 (b). Je Block ein Unterabschnitt in der Reihenfolge des Codeblocks, der Block als Blockzitat, darunter die Kette. Die Nummern 52.1–52.3 hat der steuernde Chat vergeben (Auftrag TB-130, Einzelfreigabe des Betreibers), nicht Fable. Gesetzt sind zwölf Marken: die fünf, die R65 (b) aufzählt, und sieben nach der Regel in R65 (a) an den Orten, die R63, R64 und R65 selbst als Bezug nennen (4.2, 48.16, 48.19, 51.5 zweimal, 51.6, 51.9). Diese sieben hat der steuernde Chat bestimmt, nicht Fable. Die Marke an 25.2 steht direkt unter dem berichtigten Satz, vor der Marke aus R53 (R65, Quelle des Grundes, 34.3). ⛔ In Abschnitt 9, in Abschnitt 10 und im ERZEUGT-Block von Abschnitt 3 steht keine neue Marke (R65 (d)). Die Voraussetzungen, die Fable „zu messen“ nennt, stehen mit Befund in 52.4; was offen bleibt, steht in 52.5. 52.4 und 52.5 sind Text des steuernden Chats, nicht Fables.
````

Schluss:

````
### 52.4 Voraussetzungen und Befunde

Tatsachennotizen des steuernden Chats zu den Voraussetzungen, die Fable in 02a „zu messen“ nennt. Gemessen am 02.10.2026 am Stand `1833839`, nur lesend, durch einen Helfer des steuernden Chats, der den Code gelesen hat; die Sitzung TB-130 hat in Schritt 0 die genannten Zeilen und Zählungen am Commit ⟨S0⟩ nachgemessen (`docs/belege/TB-130/0d_vorpruefung.txt`). Aussagen über ein Fehlen (kein Tagesraster, kein Filter, kein Erzeuger) sind Lesung des Helfers; gezählt sind nur Aufrufe von `mean` (`.mean(`, `np.mean`) in `bot_lauf.py` und `dropna` in `auswertung.py`, je 0. Zeilenangaben gelten am Commit ⟨S0⟩. Kein Ergebnis gelesen (27.1).

| R | Voraussetzung (Fable) | gemessen | Stand |
|---|---|---|---|
| R63 (52.1) (c) | `bot_lauf.py` rechnet keinen Anteil des Kapitals in offenen Positionen und kein Mittel daraus; zu messen durch Lesen, nicht durch Wortsuche | `research/exposure_messung/bot_lauf.py` ganz gelesen: Positionen Z. 227–231 (`allocation` Z. 229, `capital_after` Z. 230), geschrieben Z. 242 als `<BOT>_positionen.csv` mit den Spalten `trade_zeile`, `symbol`, `entry_time`, `exit_time`, `pnl_pct`, `allocation`, `capital_after`. Kapital kommt als `es.STARTING_CAPITAL` (Z. 135–136, 246, 254–255) und als `final_capital` (Z. 253–254) vor; Z. 254 teilt beide zur Gesamtrendite. Kein Tagesraster, kein Aufruf von `mean` | trifft: kein Anteil je Tag, kein Mittel |
| R63 (52.1) (d) | Bestand, keine Voraussetzung Fables | `shared/zuteilung.py:657` `def simuliere_portfolio` (R45: `shared/zuteilung.py::simuliere_portfolio`). Die neun `strategies/*/equity_simulation.py` führen je ein `simulate_portfolio`; `bot_lauf.py:133–136` ruft `es.simulate_portfolio` | R63 (d) nennt die Funktion aus R45 |
| R64 (52.2), erste | `beta_bereinigung` lässt ausser dem Schnitt auf die gemeinsamen Tage keinen Tag weg | `research/vorregistrierung/auswertung.py`: `lies_tagesreihe` (Z. 361–370) und `lies_benchmark` (Z. 378–386) lesen, prüfen Spalten und sortieren nach `datum`; kein `dropna`, kein Filter. `beta_bereinigung`: Fenstermaske Z. 510–514, Schnitt Z. 517, Auswahl Z. 522–524, Mittel Z. 528 | trifft. Fehlende Werte und doppelte Daten werden dort weder behandelt noch geprüft (52.5) |
| R64 (52.2), zweite | an einem Tag ohne Benchmark-Tag kann keine Zelle eine offene Position führen, ausser am Tag aus der Tatsachennotiz zu 23.3 | nicht entscheidbar: Den Kalender der Tagesreihe legt noch kein Code fest; `benchmark_tagesreihen` schreibt bisher kein Erzeuger des Laufs | offen (52.5). Nach 02a, „Unsicher“ 2: Trifft die Voraussetzung nicht zu, bleibt die Regel, und der Satz zur Richtung der Wirkung gilt dann nicht streng |
| R64 (52.2) (a) | Bestand, keine Voraussetzung Fables | R39 (48.7) nennt `benchmark_tagesreihen/<bot>.csv`; `auswertung.py:379` bildet `<markt>.csv` (`markt` aus `rd.BOTS[bot]["markt"]`, Z. 498); 50.2 schreibt dazu „im Zitat lies „`<bot>.csv`“ (R39)“ | Bestand. Wann der Code den Namen je Bot liest, ist nicht festgelegt; `auswertung.py` wird nach R64 (e) nicht geöffnet (52.5) |
| R65 (52.3) (c) | — | die Messung steht in 51.8 (Zeile R62 (a)): Index 149 = 2018-01-13, Index 150 = 2018-01-14, in beiden Kursdateien | trägt die „lies“-Form |

### 52.5 Was offen bleibt

| | offen | wann, wo |
|---|---|---|
| 1 | R64, zweite Voraussetzung: keine offene Position an einem Tag ohne Benchmark-Tag | Messung mit dem Zellen-Erzeuger, vor dem Tag |
| 2 | 02a, „Unsicher“ 1: Zeitachse des Falten-Sharpe in Falten mit teilweisem Benchmark (ob die Tagesreihe Tage vor dem ersten Handelbar-Tag führt); R64 (e) lässt es offen | Vorprüfung (16, 21, 29, 33), dann Anfrage an Fable; vor dem Zellen-Erzeuger |
| 3 | R64 (c) und (d): Wache im Lauf mit Ausgang 2; Probe über das tagegewichtete Mittel in der Abnahme nach R46 | mit dem Zellen-Erzeuger |
| 4 | R63 (d): der Zellen-Erzeuger bezieht weder Positionen noch Exposure aus `bot_lauf.py` | mit dem Zellen-Erzeuger (Abnahme) |
| 5 | `beta_bereinigung` behandelt und prüft weder fehlende Werte noch doppelte Daten (52.4) | Vorprüfung, ob der Datenvertrag beides ausschliesst; sonst an Fable |
| 6 | 02a, „Unsicher“ 4: ob `bestaetigung_ab_effektiv` (R37) den Beginn der Tage nach R64 für die Bestätigungsperiode verschiebt | Vorprüfung, dann an Fable |
| 7 | Benchmark-Datei: R39 nennt `<bot>.csv`, `auswertung.py:379` liest `<markt>.csv` (52.4) | Vorprüfung, dann an Fable |
| 8 | Von 51.10 sind Nr. 6 und Nr. 7 durch R63–R65 beantwortet; die Messung aus 51.10 Nr. 6 lebt in 52.5 Nr. 1 fort; 51.10 Nr. 1 bis 5 und Nr. 8 bleiben | wie dort |
| 9 | Marke an 7 (c) zu R64 (a): nicht gesetzt. Die Präzisierungen in Abschnitt 7 tragen die Regel selbst, und R61 (b) führt 7 (c) als Ort ohne Marke | nächste Anfrage an Fable |
````

**A4. Einsetzen** und **A5. Nachweis:** wie TB-129 (dort A4 und A5), mit `docs/belege/TB-129/a4_*` und `a5_*` als Vorlage und diesen Werten: Eingangszeilenzahl 11 225 · `## 52.` noch nicht vergeben · R-Diff **3/3** rc 0, Mutationsprobe an einer Kopie rc 1 · Zitate (Kopf und Schluss aus diesem Auftrag) 2/2 rc 0 · Überschriften und Ketten 3/3 · Marken 12/12 · numstat des Registers zweite Spalte **0** · Abschnitt 10 und ERZEUGT-Block bytegleich gegen `0b_*_vorher.txt` · `registerbericht.py --pruefen` nachher = vorher · Sonde: JSON ohne `zeilen` nachher = vorher, (ii) 0, „Listentext wie bei Erzeugung: ja“ · `herkunft.register()` nachher ≠ vorher, `fehlend []`, 23 Teile, der neue Wert nur im Ergebnis (42.5) · `test_vorregistrierung` am echten Register vor dem Commit, ohne Zeitgrenze, 196/196. Zuerst Probelauf an einer Kopie, dann einmal echt, danach `cmp` gegen die Kopie. Wachen im Einsetzskript wie TB-129. Ist ein Nachweis am echten Register rot: Diff als `docs/belege/TB-130/abbruch_register.diff` sichern, Register mit `git checkout -- docs/VORREGISTRIERUNG_neuselektion.md` zurücksetzen, Abbruch. **Das Register wird nur committet, wenn alle Nachweise grün sind.**

Commit `TB-130 A: Register 52 (R63–R65 zeichengleich, Tatsachennotizen 02a), Marken`, pushen. **Das ist der einzige Commit, der das Register ändert.**

## Schritt B — BACKLOG (5b)

Verfahren wie TB-129 Schritt B (Vorlage `docs/belege/TB-129/b_einfuegen.py` und `b_vergleich.py`; Belege `b_einfuegung.txt`, `b_numstat.txt`, `b_vergleich.txt`): Anker vorher zählen (Soll genau 1; sonst nicht ausführen, vermerken, weitermachen), Text aus **diesem Auftrag** einfügen, erste Textzeile nachher zählen (Soll 1), numstat zweite Spalte 0, Bytevergleich des Blocks.

#### E1 — Abschnitt 5: Bewertung von Fable 02a (5b)

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Anker: `## 6 — Geparkt, null Arbeit` · Art: **vor der Zeile** (genau eine Leerzeile davor und danach; eine vorhandene wird nicht verdoppelt)

```
### Aus Fable 02a (02.10.2026) — Bewertung nach 5b, eingetragen mit TB-130

- **Bewertung:** Die Antwort trägt. 34 von 37 Registerzitaten stehen wörtlich im Register, drei sind Umschreibungen (zweimal der Schluss von R61 (b), einmal „2 = nicht gerechnet“ zu 43.1); keine Zahl ist falsch. Frage 1 und 4 einverstanden (25.2 als BERICHTIGT), Frage 2 und 3 anders als die Neigung: gemittelt wird über die Benchmark-Tage, der Schnitt auf die gemeinsamen Tage ist Registertext (7, 24.2, 23.3). R63–R65 stehen seit TB-130 im Register, Abschnitt 52; Befunde in 52.4, Offenes in 52.5. Leseprotokoll vollständig nach R56 (b); kein Treffer nach 27.1.
- **Offen:** R64, zweite Voraussetzung (nicht entscheidbar, solange kein Code den Kalender der Tagesreihe festlegt; Messung mit dem Zellen-Erzeuger, vor dem Tag). Vor dem Zellen-Erzeuger: 02a, „Unsicher“ 1 (Zeitachse des Falten-Sharpe bei teilweisem Benchmark): vorprüfen in 16, 21, 29, 33, dann an Fable; „Unsicher“ 4 (Bestätigungsperiode, `bestaetigung_ab_effektiv`).
- **Anforderungen an den Zellen-Erzeuger aus 02a:** Wache im Lauf, Ausgang 2, wenn einer Tagesreihe ein Benchmark-Tag fehlt (R64 (c)); Probe „Wert des Gewinners = tagegewichtetes Mittel der Faltenwerte“ in der Abnahme nach R46 (R64 (d)); nichts aus `bot_lauf.py` beziehen (R63 (d)).
- **Vorprüfen:** `beta_bereinigung` behandelt und prüft weder fehlende Werte noch doppelte Daten. Benchmark-Datei: R39 nennt `<bot>.csv`, `auswertung.py:379` liest `<markt>.csv`. Vom Helfer gemeldet, vom steuernden Chat nicht nachgelesen: Die Tatsachennotiz zu 23.3 („lässt den ersten Kurstag je Falte aus“) gegen `research/vorregistrierung/benchmark.py` (die Reihe entsteht einmal über alle Falten; die Rendite fehlt am ersten Punkt je Symbol).
- **Fables Ampel:** 🔴, gemessen 332 931 nach einer Anfrage (überschritten beim Lesen der Abschnitte 4, 24 und 43). Jede Anfrage geht an einen neuen Fable-Chat (F4); die Abschnittsliste der Anfrage knapp halten.
- **Regel für Registeraufträge aus R65 (a):** Die Aufzählung eines Blocks schliesst die Regel aus 34 nicht ab. Der steuernde Chat bestimmt die Marken an allen Orten, denen ein Block ein „lies“, eine Ergänzung oder eine Bestätigung gibt, und weist sie im Auftrag als seine aus.
- **Regelwerk, nächster Dokumentationsauftrag (ARBEITSWEISE 0):** aus Fehler Nr. 17 (Nummern am Block zählen), Nr. 18 (vor dem Lesen die Bytes messen, ÷ 1,6 gegen die Ampel), Nr. 19 (der Text für die Aufgabe der Claude-Code-Sitzung steht am Ende jeder Antwort; Betreiber 02.10.2026, 10:45).
```

Soll numstat: `10	0` (9 Zeilen des Blocks und eine Leerzeile danach).

## Schritt C — Registerkopie, Index, Dialog-Index

**C1. Registerkopie:** wie TB-129 C1 (fünf Aufrufe, je Ausgabe und rc nach `c1_*.txt`). Soll: rc 0 je Aufruf; 53 Abschnittsdateien `_00` bis `_52`. Schreiblauf mit rc 2 oder 3 oder `--pruefen` mit rc ≠ 0 ⇒ festhalten, Kopien nicht committen, melden (kein Abbruch; C2 und C3 entfallen dann).

**C2. `docs/projektfuehrung/REGISTER_INDEX.md` nachziehen**, nach der Bauart von TB-129 C2 (Vorlagen `docs/belege/TB-129/c2_*`, sonst `docs/belege/TB-126/c2_*`): Kopf (Commit, „Abschnitte 0–52“, Zeilenzahl, sha256, „nachgezogen in TB-130“, der Verweis auf die Abschnittsdateien bis `_52.md`) · „Wie gemessen“ (Zahlen je Art und Belegpfad neu aus `c1`) · Abschnittstabelle mit neuer Zeile 52 und der Teil-Zuordnung · alle Zeilenangaben „Z. n“ auf den neuen Stand · in der Tabelle der Registertexte ab Abschnitt 18 eine Zeile „52 aus 02a“ (R63–R65 = 52.1–52.3; 52.4 Voraussetzungen; 52.5 Offenes) und die Verweise an den Orten mit neuer Marke (4.2 in der Tabelle der Abschnitte 2–14; 25, 47, 48, 50, 51) · neuer Abschnitt `## 7. Die Marken aus Fable 02a (TB-130)` in der Form von Abschnitt 6, vor der letzten Trennlinie `---` und dem Pflegeblock · Pflegezeile.

**C3. Indexzeilen aus Fable 01a anpassen:** Im Block `### Indexzeilen aus Fable 01a` (Abschnitt 6 des Index) enden fünf Zeilen mit `Ohne Marke; an Fable (51.10 Nr. 7).` Dieser Schluss wird je Zeile ersetzt durch `Marke gesetzt in TB-130 (R65 (b), 52.3).` Die Zeile „Tag-Vorbedingungen“ bleibt. Vorher zählen: Soll 5.

**C4. Dialog-Index.** Die Datei `docs/belege/TB-130/c4_handfelder.json` mit genau diesem Inhalt anlegen:

```
{"01a": {"offen": "nein"}, "02a": {"frage": "Gilt die Lesart 51.9 zu R60 (a), über welche Tage wird die mittlere Exposure gemittelt, und tragen die fünf Orte ohne Marke Marken?", "entscheidung": "51.9 gilt je Stelle, nicht je Ordner (R63); gemittelt wird über die Benchmark-Tage, der Schnitt auf die gemeinsamen Tage ist Registertext, dazu eine Wache im Lauf (R64); alle fünf Orte tragen Marken, 25.2 als BERICHTIGT, die Aufzählungen schliessen die Regel aus 34 nicht ab (R65).", "offen": "ja"}}
```

Dann `trading-env/bin/python3 docs/werkzeuge/dialog_index.py --handfelder docs/belege/TB-130/c4_handfelder.json`, danach `--pruefen` ⇒ `c4_dialog_index.txt`. Soll (Docstring Z. 6–30; die Handfelder je Schlüssel werden zusammengeführt, Z. 115–116): `--pruefen` rc 0; Zeile `02a` mit Fundstelle 52 und Status „offen“ (offen = ja: die zweite Voraussetzung von R64 ist nicht entschieden, und 02a bittet um eine Vorprüfung); Zeile `01a` mit Status „registriert“ (ihre Fragen zu R60 sind durch 02a beantwortet; die offene Messung läuft unter 02a weiter), Frage und Entscheidung unverändert; 52 Antworten. `git diff --numstat` festhalten; weitere geänderte Zeilen im Ergebnis nennen (kein Abbruch).

Commit `TB-130 B/C: BACKLOG, Registerkopie, Index, Dialog-Index`, pushen.

## Schritt D — Abgabe

**D1.** `docs/ERGEBNIS_TB-130_register_fable_02a.md`, Bau wie ERGEBNIS_TB-129: Kopfzeile, Stand und Commits, Kurz-Tabelle je Schritt (Soll | Ist), Markentabelle (zwölf Marken mit Zeile nachher), `herkunft.register()` vorher und nachher, **Für Fable** (52.5 Nr. 2, 5, 6, 7, 9; jede Reibung beim Setzen), **Nicht getan** (52.5; die Ablage macht der steuernde Chat), **In einfacher Sprache**.

**D2. Journal:** Block nach dem letzten Buchstabenblock von `docs/projektfuehrung/JOURNAL.md`, vor `## Wiederkehrende Lehren`. Kennung vorher messen (erwartet **EB**), mit Quellenzeile.

**D3.** Abgabe-Commit `TB-130 Abgabe: Ergebnis, Journal <Kennung>`, pushen. Danach `git status --porcelain` in den Scratch und als `docs/belege/TB-130/d3_porcelain.txt`, kleiner letzter Commit, pushen.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a weicht ab; ein Ausgangswert aus 0b mit Soll weicht ab; der Basislauf in 0c (falls nötig) ist nicht 196/196.
- 0d: Nr. 1, 2, 3 oder 4 weicht ab (auch eine einzelne Marke).
- Ein Nachweis aus A5 ist rot, jeder der dort genannten.
- Eine Datei ausserhalb der Freigabetabelle müsste geändert werden.
- `git push` scheitert zweimal.

**Kein Abbruch:** der BACKLOG-Anker ≠ 1 (nicht einfügen, nennen) · die fünf Indexzeilen in C3 zählen nicht 5 (nicht ersetzen, nennen) · `registerkopie.py` mit rc ≠ 0 (Kopien nicht committen, nennen; C2 und C3 entfallen, C4 nicht) · weitere geänderte Zeilen im Dialog-Index (nennen) · eine Reibung zwischen Fable-Text und Code oder Register (unter „Für Fable“ nennen).

**Bei Abbruch:** committen, was an Belegen da ist, **nie** `JOURNAL.md` mit Platzhalter, Grund in `docs/belege/TB-130/abbruch.txt`, pushen, melden. Kein Registertext mit einem Befund, den dieser Auftrag nicht vorsieht.

## In einfacher Sprache

Fable hat am 02.10. drei weitere Regeltexte geschrieben (R63–R65). Sie klären, an welchen Tagen die durchschnittliche Auslastung eines Bots gemessen wird, und dass fünf alte Stellen einen Hinweis auf spätere Berichtigungen brauchen. Diese Sitzung kopiert die Texte per Skript ins Register, Zeichen für Zeichen, als Abschnitt 52, und setzt zwölf Hinweise an alten Stellen. Dazu kommt eine Tabelle mit dem, was im Code nachgelesen wurde; ein Punkt lässt sich erst prüfen, wenn das Programm für die Zellen gebaut ist, und steht offen da. Am Code ändert sich nichts.

---

## Anhang A — TB-130: Überschriften, Ketten, Marken und Fundstellen (Vorlage für die Mac-Sitzung)

**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `f63ad4c` (11 225 Zeilen, sha256 `7f74b0e5…`), HEAD `1833839`. Gebaut vom steuernden Chat am 02.10.2026 mit einem Skript, das Ankerzeilen, Einfügestellen und Zeilenanfänge am Register misst. **Alle Zeilennummern gelten am Original, vor jeder Einfügung.** Einsetzen deshalb von unten nach oben. **Massgeblich für Skripte ist der JSON-Block am Ende.**

### Tabelle 1 — Überschriften und Ketten (3)

| x.n | Überschriftzeile (exakt) | Kette (exakt) |
|---|---|---|
| 52.1 | `### 52.1 R63 — Präzisierung zu R60 (a) (51.5) und Bestätigung der Lesart 51.9 (Reichweite: die Stelle, nicht der Ordner)` | `**Kette:** Marken: 51.5 (R60); 51.9. Voraussetzung gemessen: 52.4. Offen: 52.5 Nr. 4.` |
| 52.2 | `### 52.2 R64 — Präzisierung zu R48 (d) (48.16) und zu R60 (b) und (c) (51.5) (über welche Tage die mittlere Exposure gemittelt wird)` | `**Kette:** Marken: 4.2; 48.16 (R48); 51.5 (R60). Voraussetzung gemessen: 52.4. Offen: 52.5 Nr. 1 bis 3, 5 bis 7 und 9.` |
| 52.3 | `### 52.3 R65 — Marken nach R61 (Regel und fünf Orte; eine Berichtigung in „lies“-Form)` | `**Kette:** Marken: 48.19 (R51); 51.6 (R61); nachgetragen nach (b): 25.2; 47.9 (R26); 47.13 (R30); 50.1, Zeile R48 (d); 50.4, Schlusssatz. In Abschnitt 10 steht weiter keine Marke (R65 (d)).` |

### Tabelle 2 — Marken (12)

Sortiert nach Einfügestelle, an derselben Stelle nach R aufsteigend. Jede Marke: Leerzeile, Markenzeile 1, Markenzeile 2 `> Eintrag und Stand oben bleiben zeichengleich.` „Zahl“ = `str.count` des Ankers über den ganzen Registertext. „Grund“ nennt, ob R65 (b) die Marke aufzählt oder der steuernde Chat R65 (a) angewandt hat.

| Nr | Grund | Registerstelle | Anker (Ankerzeile) | Zahl | Einfügestelle | Markenzeile 1 (exakt) |
|---|---|---|---|---|---|---|
| 1 | R65 (a), angewandt: R64 (a) „Das gilt für die mittlere Exposure je (Zelle, Falte) (4.2)“ | 4.2 | `### 4.2 Warum` (Z. 484) | 1 | nach Zeile 526: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **4.2 PRÄZISIERT durch R64 (52.2)** (Fable 02a R64, Unterpunkt (a), TB-130, ⟨DATUM⟩).` |
| 2 | R65 (b): 25.2 — BERICHTIGT durch R62 (51.7), Unterpunkt (a), und durch diesen Block, Unterpunkt (c) | 25.2, unter dem berichtigten Satz | `### 25.2 Die Instanz` (Z. 4626) | 1 | nach Zeile 4650: `**2018-01-14**. Fables Nachrechnung trif` | `> ⭐ **25.2 BERICHTIGT durch R62 (51.7) und R65 (52.3)** (Fable 01a R62, Unterpunkt (a), und Fable 02a R65, Unterpunkt (c), TB-130, ⟨DATUM⟩).` |
| 3 | R65 (b): 47.9 (R26) — BERICHTIGT durch R61 (51.6), Unterpunkt (c) | 47.9 (R26) | `### 47.9 R26` (Z. 10701) | 1 | nach Zeile 10704: `> *Quelle des Grundes:* 12, 14, R14 „für` | `> ⭐ **47.9 R26 BERICHTIGT durch R61 (51.6)** (Fable 01a R61, Unterpunkt (c), nachgetragen nach Fable 02a R65 (b), TB-130, ⟨DATUM⟩).` |
| 4 | R65 (b): 47.13 (R30) — BERICHTIGT durch R61 (51.6), Unterpunkt (c) | 47.13 (R30) | `### 47.13 R30` (Z. 10729) | 1 | nach Zeile 10732: `> *Quelle des Grundes:* 14 (Reihenfolge)` | `> ⭐ **47.13 R30 BERICHTIGT durch R61 (51.6)** (Fable 01a R61, Unterpunkt (c), nachgetragen nach Fable 02a R65 (b), TB-130, ⟨DATUM⟩).` |
| 5 | R65 (a), angewandt: R64 ist „Präzisierung zu R48 (d) (48.16)“ | 48.16 (R48) | `### 48.16 R48 — Lesarten` (Z. 10864) | 1 | nach Zeile 10884: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **48.16 R48 (d) PRÄZISIERT durch R64 (52.2)** (Fable 02a R64, TB-130, ⟨DATUM⟩).` |
| 6 | R65 (a), angewandt: „Die Aufzählungen in R51 und R61 (b) … schliessen sie nicht ab“ | 48.19 (R51) | `### 48.19 R51` (Z. 10910) | 1 | nach Zeile 10913: `> Quelle des Grundes: 34 (Marke am alten` | `> ⭐ **48.19 R51 PRÄZISIERT durch R65 (52.3)** (Fable 02a R65, Unterpunkt (a), TB-130, ⟨DATUM⟩).` |
| 7 | R65 (b): 50.1, Zeile R48 (d) — ERGÄNZT durch R60 (51.5), Unterpunkt (d), und 51.8 | 50.1, nach der Tabelle | `### 50.1 Voraussetzungen und Befunde` (Z. 10959) | 1 | nach Zeile 10978: `\| R55 (49.3) \| Nebenfall „keine Zelle zu` | `> ⭐ **50.1, Zeile R48 (d) ERGÄNZT durch R60 (51.5) und 51.8** (Fable 01a R60, Unterpunkt (d), nachgetragen nach Fable 02a R65 (b), TB-130, ⟨DATUM⟩).` |
| 8 | R65 (b): 50.4, Schlusssatz — ERGÄNZT durch R57 (51.2): der Schlusssatz ist bestätigt | 50.4, nach dem Zitatblock | `### 50.4 Vollzug TB-124` (Z. 11067) | 1 | nach Zeile 11105: `` > Breakout-Bots `BB_PERIOD + L − 1`, nie `` | `> ⭐ **50.4, Schlusssatz ERGÄNZT durch R57 (51.2): der Schlusssatz ist bestätigt** (Fable 01a R57, nachgetragen nach Fable 02a R65 (b), TB-130, ⟨DATUM⟩).` |
| 9 | R65 (a), angewandt: R63 ist „Präzisierung zu R60 (a) (51.5)“ | 51.5 (R60) | `### 51.5 R60` (Z. 11170) | 1 | nach Zeile 11173: `> Quelle des Grundes: R48 (d), R50 (Defi` | `> ⭐ **51.5 R60 (a) PRÄZISIERT durch R63 (52.1)** (Fable 02a R63, TB-130, ⟨DATUM⟩).` |
| 10 | R65 (a), angewandt: R64 ist Präzisierung „zu R60 (b) und (c) (51.5)“ | 51.5 (R60) | `### 51.5 R60` (Z. 11170) | 1 | nach Zeile 11173: `> Quelle des Grundes: R48 (d), R50 (Defi` | `> ⭐ **51.5 R60 (b) und (c) PRÄZISIERT durch R64 (52.2)** (Fable 02a R64, TB-130, ⟨DATUM⟩).` |
| 11 | R65 (a), angewandt: R65 (a) deutet die Aufzählung in R61 (b) | 51.6 (R61) | `### 51.6 R61` (Z. 11177) | 1 | nach Zeile 11180: `> Quelle des Grundes: 34 (Marke am alten` | `> ⭐ **51.6 R61 (b) PRÄZISIERT durch R65 (52.3)** (Fable 02a R65, Unterpunkt (a), TB-130, ⟨DATUM⟩).` |
| 12 | R65 (a), angewandt: R63 ist „Bestätigung der Lesart 51.9“ | 51.9 | `### 51.9 Lesart` (Z. 11208) | 1 | nach Zeile 11212: `` R60 (a) setzt voraus, dass `research/exp `` | `> ⭐ **51.9 ERGÄNZT durch R63 (52.1): die Lesart ist bestätigt** (Fable 02a R63, TB-130, ⟨DATUM⟩).` |

### Prüfsumme

```
Marken: 12 an 11 Einfuegestellen
je Abschnitt: 4: 1, 25: 1, 47: 2, 48: 2, 50: 2, 51: 4
Anker mit Zahl 1 (Original): 12 von 12
Anker mit Zahl 1 (nach Simulation): 12 von 12
Bloecke: 3 | Ueberschriften: 3 max. Laenge 132
Fundstellen: 33 | Zaehlungen: 7 | Kalender: 0 Dateien
rc 0: alles wie angegeben
```

Prüfskript (liest den JSON-Block unten; Aufruf `python3 pruefe_anhang_tb130.py <dieser Auftrag> <repo-wurzel>`; rc 0 = alles wie angegeben).

```python
#!/usr/bin/env python3
"""Prueft Anhang A von TB-130 gegen das Register am Stand f63ad4c und die Fundstellen fuer 52.4.

Aufruf:  python3 pruefe_anhang_tb130.py <MAC_TB-130_register_fable_02a.md> <repo-wurzel>
Liest den JSON-Block des Auftrags (zwischen den Zeilen 'DATEN-ANFANG' und 'DATEN-ENDE'), zaehlt jeden
Anker mit str.count ueber den ganzen Registertext, prueft Ankerzeile und Einfuegestelle, schneidet die
Quelle nach der Schnittregel, simuliert das Einsetzen (Marken + angehaengter Abschnitt 52) und zaehlt
erneut; prueft Fundstellen, Zaehlungen und den Kalender. rc 0 = alles wie angegeben, rc 1 = Abweichung.
"""
import csv, datetime, hashlib, json, re, sys

md, repo = sys.argv[1], sys.argv[2].rstrip("/") + "/"
roh = open(md, encoding="utf-8").read()
daten = json.loads(roh.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
reg = open(repo + daten["register"], encoding="utf-8").read()
L = reg.split("\n")
fehler = []
def f(x): fehler.append(x)

if hashlib.sha256(reg.encode()).hexdigest() != daten["register_sha256"]: f("Register-sha256 weicht ab")
if len(reg.splitlines()) != daten["register_zeilen"]: f("Register-Zeilenzahl weicht ab")
a9 = next(i for i, s in enumerate(L, 1) if s.startswith("## 9."))
a11 = next(i for i, s in enumerate(L, 1) if s.startswith("## 11."))
ea = next(i for i, s in enumerate(L, 1) if s.startswith("<!-- ERZEUGT:"))
ee = next(i for i, s in enumerate(L, 1) if s.startswith("<!-- ENDE ERZEUGT -->"))
if reg.count("## 52.") != 0: f("## 52. ist schon vergeben")
if any(s.startswith("> R63 — ") for s in L): f("R63 steht schon im Register")

FORM = re.compile(r"^> ⭐ \*\*.+ (PRÄZISIERT|ERGÄNZT|BERICHTIGT) durch .+\*\* \(.+, TB-130, ⟨DATUM⟩\)\.$")
marken = daten["marken"]
for m in marken:
    n = reg.count(m["anker"])
    if n != 1: f(f"Nr {m['nr']}: Anker {m['anker']!r} zaehlt {n}")
    if not L[m["ankerzeile"] - 1].startswith(m["anker"]): f(f"Nr {m['nr']}: Anker beginnt nicht Zeile {m['ankerzeile']}")
    if not L[m["nach"] - 1].startswith(m["anfang40"]): f(f"Nr {m['nr']}: Zeile {m['nach']} beginnt nicht wie angegeben")
    if a9 <= m["nach"] < a11: f(f"Nr {m['nr']}: Einfuegestelle in Abschnitt 9 oder 10")
    if ea <= m["nach"] < ee: f(f"Nr {m['nr']}: Einfuegestelle im ERZEUGT-Block")
    if L[m["nach"] - 1].startswith(">") and L[m["nach"]].startswith(">"): f(f"Nr {m['nr']}: mitten im Zitat")
    if L[m["nach"] - 1].startswith("|") and L[m["nach"]].startswith("|"): f(f"Nr {m['nr']}: mitten in Tabelle")
    if L[m["nach"]] != "": f(f"Nr {m['nr']}: nach der Einfuegestelle steht keine Leerzeile")
    if not FORM.match(m["m1"]): f(f"Nr {m['nr']}: Markenzeile 1 nicht in der Form")
    if m["m2"] != "> Eintrag und Stand oben bleiben zeichengleich.": f(f"Nr {m['nr']}: Markenzeile 2")
schl = [(m["nach"], m["R"]) for m in marken]
if schl != sorted(schl): f("Reihenfolge nicht nach Einfuegestelle/R")
if [m["nr"] for m in marken] != list(range(1, len(marken) + 1)): f("Nummern nicht fortlaufend")

# Quelle schneiden
q = daten["quelle"]
qroh = open(repo + q["pfad"], "rb").read()
if hashlib.md5(qroh).hexdigest() != q["md5"]: f("Quelle: md5 weicht ab")
if len(qroh) != q["bytes"]: f("Quelle: Bytes weichen ab")
z = qroh.decode("utf-8").split("\n")
bl, cur = {}, None
for i in range(q["von"], q["bis"] + 1):
    s = z[i - 1]
    mm = re.match(r"^R(\d+) — ", s)
    if mm: cur = int(mm.group(1)); bl[cur] = [s]; continue
    if cur is not None:
        bl[cur].append(s)
        if s.startswith("Quelle des Grundes:"): cur = None
if sorted(bl) != list(range(63, 66)): f("Schnitt ergibt nicht R63-R65")
if any(len(v) != 2 or not v[1].endswith("Kein Ergebnis.") for v in bl.values()): f("ein Block hat nicht zwei Zeilen")

# Ueberschriften: Bezug = Anfang des Blocks bis zum ersten Punkt nach dem Bezug
for u in daten["ueberschriften"]:
    kern = u["zeile"].split(" ", 2)[2]                      # "R56 — ..."
    if not bl[u["R"]][0].startswith(kern + "."): f(f"{u['xn']}: Ueberschrift ist nicht der Blockanfang")
    if not u["kette"].startswith("**Kette:** "): f(f"{u['xn']}: Kette nicht in der Form")

# Simulation: Marken von unten nach oben einsetzen, Abschnitt 52 anhaengen
neu = L[:]
for m in sorted(marken, key=lambda m: (m["nach"], m["R"], m["nr"]), reverse=True):
    neu[m["nach"]:m["nach"]] = ["", m["m1"], m["m2"]]
anhang = ["## 52. Fable 02a — Registerblock R63–R65 (TB-130)", ""]
for u in daten["ueberschriften"]:
    anhang += [u["zeile"], ""] + ["> " + s for s in bl[u["R"]]] + ["", u["kette"], ""]
sim = "\n".join(neu[:-1] + [""] + anhang)
for m in marken:
    n = sim.count(m["anker"])
    if n != 1: f(f"Nr {m['nr']}: Anker nach Simulation {n}")
zz = [u["zeile"] for u in daten["ueberschriften"]]
if len(set(zz)) != 3 or any(sim.count(x) != 1 for x in zz): f("Ueberschriften nicht eindeutig")
if any(len(x) > 140 for x in zz): f("Ueberschrift laenger als 140 Zeichen")
it = iter(neu)
if not all(any(x == y for y in it) for x in L): f("alte Zeilen nicht in Reihenfolge erhalten")

# Fundstellen, Zaehlungen, Kalender
for d, znr, teil in daten["fundstellen"]:
    zl = open(repo + d, encoding="utf-8").read().split("\n")
    if znr > len(zl) or teil not in zl[znr - 1]: f(f"Fundstelle {d}:{znr} enthaelt nicht {teil!r}")
import glob
for d, muster, soll in daten["zaehlungen"]:
    ist = len(re.findall(muster, open(repo + d, encoding="utf-8").read(), re.M))
    if ist != soll: f(f"Zaehlung {d} /{muster}/: {ist} statt {soll}")
for gl, muster, soll, dateien in daten["glob_zaehlungen"]:
    pf = sorted(glob.glob(repo + gl))
    if len(pf) != dateien: f(f"Glob {gl}: {len(pf)} Dateien statt {dateien}")
    for p in pf:
        ist = len(re.findall(muster, open(p, encoding="utf-8").read(), re.M))
        if ist != soll: f(f"Zaehlung {p} /{muster}/: {ist} statt {soll}")
k = daten["kalender"]
for d in k["dateien"]:
    tage = [r[0][:10] for r in csv.reader(open(repo + d, encoding="utf-8"))][1:]
    bis = [t for t in tage if t <= "2018-01-31"]
    tag = datetime.date.fromisoformat
    ist = {"erster": tage[0], "balken_bis_2017-12-31": sum(t <= "2017-12-31" for t in tage),
           "index_149": tage[149], "index_150": tage[150],
           "tage_januar_2018": sum("2018-01-01" <= t <= "2018-01-31" for t in tage),
           "luecken_bis_2018-01-31": sum((tag(b) - tag(a)).days != 1 for a, b in zip(bis, bis[1:])),
           "doppelte_bis_2018-01-31": len(bis) - len(set(bis))}
    if ist != k["soll"]: f(f"Kalender {d}: {ist}")

je = {}
for m in marken:
    kk = next(int(re.match(r"## (\d+)\.", L[i - 1]).group(1)) for i in range(m["nach"], 0, -1) if re.match(r"## \d+\.", L[i - 1]))
    je[kk] = je.get(kk, 0) + 1
print("Marken:", len(marken), "an", len({m["nach"] for m in marken}), "Einfuegestellen")
print("je Abschnitt:", ", ".join(f"{a}: {v}" for a, v in sorted(je.items())))
print("Anker mit Zahl 1 (Original):", sum(reg.count(m["anker"]) == 1 for m in marken), "von", len(marken))
print("Anker mit Zahl 1 (nach Simulation):", sum(sim.count(m["anker"]) == 1 for m in marken), "von", len(marken))
print("Bloecke:", len(bl), "| Ueberschriften:", len(zz), "max. Laenge", max(len(x) for x in zz))
print("Fundstellen:", len(daten["fundstellen"]), "| Zaehlungen:", len(daten["zaehlungen"]), "| Kalender:", len(k["dateien"]), "Dateien")
if fehler:
    print("ABWEICHUNG:"); [print("  -", x) for x in fehler]; sys.exit(1)
print("rc 0: alles wie angegeben")
```

### Daten (maschinenlesbar, massgeblich für Skripte)

```
DATEN-ANFANG
{
 "stand": "f63ad4c (HEAD 1833839)",
 "register": "docs/VORREGISTRIERUNG_neuselektion.md",
 "register_sha256": "7f74b0e5a746cbc720b7b7c20af83acddd32d6652c3b57099f18769d3d4b16c4",
 "register_zeilen": 11225,
 "quelle": {
  "pfad": "docs/projektfuehrung/FABLE_ANTWORT_2026-10-02a_exposure_tage_laufbereich_marken.md",
  "md5": "a7821eeb4f61faad5f74f72ec7201797",
  "bytes": 21709,
  "von": 112,
  "bis": 119
 },
 "ueberschriften": [
  {
   "xn": "52.1",
   "R": 63,
   "zeile": "### 52.1 R63 — Präzisierung zu R60 (a) (51.5) und Bestätigung der Lesart 51.9 (Reichweite: die Stelle, nicht der Ordner)",
   "kette": "**Kette:** Marken: 51.5 (R60); 51.9. Voraussetzung gemessen: 52.4. Offen: 52.5 Nr. 4."
  },
  {
   "xn": "52.2",
   "R": 64,
   "zeile": "### 52.2 R64 — Präzisierung zu R48 (d) (48.16) und zu R60 (b) und (c) (51.5) (über welche Tage die mittlere Exposure gemittelt wird)",
   "kette": "**Kette:** Marken: 4.2; 48.16 (R48); 51.5 (R60). Voraussetzung gemessen: 52.4. Offen: 52.5 Nr. 1 bis 3, 5 bis 7 und 9."
  },
  {
   "xn": "52.3",
   "R": 65,
   "zeile": "### 52.3 R65 — Marken nach R61 (Regel und fünf Orte; eine Berichtigung in „lies“-Form)",
   "kette": "**Kette:** Marken: 48.19 (R51); 51.6 (R61); nachgetragen nach (b): 25.2; 47.9 (R26); 47.13 (R30); 50.1, Zeile R48 (d); 50.4, Schlusssatz. In Abschnitt 10 steht weiter keine Marke (R65 (d))."
  }
 ],
 "marken": [
  {
   "nr": 1,
   "R": 64,
   "ziel": "R65 (a), angewandt: R64 (a) „Das gilt für die mittlere Exposure je (Zelle, Falte) (4.2)“",
   "stelle": "4.2",
   "anker": "### 4.2 Warum",
   "ankerzeile": 484,
   "nach": 526,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **4.2 PRÄZISIERT durch R64 (52.2)** (Fable 02a R64, Unterpunkt (a), TB-130, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 2,
   "R": 62,
   "ziel": "R65 (b): 25.2 — BERICHTIGT durch R62 (51.7), Unterpunkt (a), und durch diesen Block, Unterpunkt (c)",
   "stelle": "25.2, unter dem berichtigten Satz",
   "anker": "### 25.2 Die Instanz",
   "ankerzeile": 4626,
   "nach": 4650,
   "anfang40": "**2018-01-14**. Fables Nachrechnung trif",
   "m1": "> ⭐ **25.2 BERICHTIGT durch R62 (51.7) und R65 (52.3)** (Fable 01a R62, Unterpunkt (a), und Fable 02a R65, Unterpunkt (c), TB-130, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 3,
   "R": 61,
   "ziel": "R65 (b): 47.9 (R26) — BERICHTIGT durch R61 (51.6), Unterpunkt (c)",
   "stelle": "47.9 (R26)",
   "anker": "### 47.9 R26",
   "ankerzeile": 10701,
   "nach": 10704,
   "anfang40": "> *Quelle des Grundes:* 12, 14, R14 „für",
   "m1": "> ⭐ **47.9 R26 BERICHTIGT durch R61 (51.6)** (Fable 01a R61, Unterpunkt (c), nachgetragen nach Fable 02a R65 (b), TB-130, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 4,
   "R": 61,
   "ziel": "R65 (b): 47.13 (R30) — BERICHTIGT durch R61 (51.6), Unterpunkt (c)",
   "stelle": "47.13 (R30)",
   "anker": "### 47.13 R30",
   "ankerzeile": 10729,
   "nach": 10732,
   "anfang40": "> *Quelle des Grundes:* 14 (Reihenfolge)",
   "m1": "> ⭐ **47.13 R30 BERICHTIGT durch R61 (51.6)** (Fable 01a R61, Unterpunkt (c), nachgetragen nach Fable 02a R65 (b), TB-130, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 5,
   "R": 64,
   "ziel": "R65 (a), angewandt: R64 ist „Präzisierung zu R48 (d) (48.16)“",
   "stelle": "48.16 (R48)",
   "anker": "### 48.16 R48 — Lesarten",
   "ankerzeile": 10864,
   "nach": 10884,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **48.16 R48 (d) PRÄZISIERT durch R64 (52.2)** (Fable 02a R64, TB-130, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 6,
   "R": 65,
   "ziel": "R65 (a), angewandt: „Die Aufzählungen in R51 und R61 (b) … schliessen sie nicht ab“",
   "stelle": "48.19 (R51)",
   "anker": "### 48.19 R51",
   "ankerzeile": 10910,
   "nach": 10913,
   "anfang40": "> Quelle des Grundes: 34 (Marke am alten",
   "m1": "> ⭐ **48.19 R51 PRÄZISIERT durch R65 (52.3)** (Fable 02a R65, Unterpunkt (a), TB-130, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 7,
   "R": 60,
   "ziel": "R65 (b): 50.1, Zeile R48 (d) — ERGÄNZT durch R60 (51.5), Unterpunkt (d), und 51.8",
   "stelle": "50.1, nach der Tabelle",
   "anker": "### 50.1 Voraussetzungen und Befunde",
   "ankerzeile": 10959,
   "nach": 10978,
   "anfang40": "| R55 (49.3) | Nebenfall „keine Zelle zu",
   "m1": "> ⭐ **50.1, Zeile R48 (d) ERGÄNZT durch R60 (51.5) und 51.8** (Fable 01a R60, Unterpunkt (d), nachgetragen nach Fable 02a R65 (b), TB-130, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 8,
   "R": 57,
   "ziel": "R65 (b): 50.4, Schlusssatz — ERGÄNZT durch R57 (51.2): der Schlusssatz ist bestätigt",
   "stelle": "50.4, nach dem Zitatblock",
   "anker": "### 50.4 Vollzug TB-124",
   "ankerzeile": 11067,
   "nach": 11105,
   "anfang40": "> Breakout-Bots `BB_PERIOD + L − 1`, nie",
   "m1": "> ⭐ **50.4, Schlusssatz ERGÄNZT durch R57 (51.2): der Schlusssatz ist bestätigt** (Fable 01a R57, nachgetragen nach Fable 02a R65 (b), TB-130, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 9,
   "R": 63,
   "ziel": "R65 (a), angewandt: R63 ist „Präzisierung zu R60 (a) (51.5)“",
   "stelle": "51.5 (R60)",
   "anker": "### 51.5 R60",
   "ankerzeile": 11170,
   "nach": 11173,
   "anfang40": "> Quelle des Grundes: R48 (d), R50 (Defi",
   "m1": "> ⭐ **51.5 R60 (a) PRÄZISIERT durch R63 (52.1)** (Fable 02a R63, TB-130, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 10,
   "R": 64,
   "ziel": "R65 (a), angewandt: R64 ist Präzisierung „zu R60 (b) und (c) (51.5)“",
   "stelle": "51.5 (R60)",
   "anker": "### 51.5 R60",
   "ankerzeile": 11170,
   "nach": 11173,
   "anfang40": "> Quelle des Grundes: R48 (d), R50 (Defi",
   "m1": "> ⭐ **51.5 R60 (b) und (c) PRÄZISIERT durch R64 (52.2)** (Fable 02a R64, TB-130, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 11,
   "R": 65,
   "ziel": "R65 (a), angewandt: R65 (a) deutet die Aufzählung in R61 (b)",
   "stelle": "51.6 (R61)",
   "anker": "### 51.6 R61",
   "ankerzeile": 11177,
   "nach": 11180,
   "anfang40": "> Quelle des Grundes: 34 (Marke am alten",
   "m1": "> ⭐ **51.6 R61 (b) PRÄZISIERT durch R65 (52.3)** (Fable 02a R65, Unterpunkt (a), TB-130, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 12,
   "R": 63,
   "ziel": "R65 (a), angewandt: R63 ist „Bestätigung der Lesart 51.9“",
   "stelle": "51.9",
   "anker": "### 51.9 Lesart",
   "ankerzeile": 11208,
   "nach": 11212,
   "anfang40": "R60 (a) setzt voraus, dass `research/exp",
   "m1": "> ⭐ **51.9 ERGÄNZT durch R63 (52.1): die Lesart ist bestätigt** (Fable 02a R63, TB-130, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  }
 ],
 "fundstellen": [
  [
   "research/exposure_messung/bot_lauf.py",
   133,
   "def simuliere(es, trades, allocation_pct, max_concurrent):"
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   135,
   "return es.simulate_portfolio(trades, es.STARTING_CAPITAL, allocation_pct)"
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   136,
   "return es.simulate_portfolio(trades, es.STARTING_CAPITAL, allocation_pct, max_concurrent)"
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   227,
   "positionen = trades.loc[kennungen.values, [\"symbol\", \"entry_time\", \"exit_time\", \"pnl_pct\"]].copy()"
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   228,
   "rename(columns={\"index\": \"trade_zeile\"})"
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   229,
   "positionen[\"allocation\"] = equity[\"allocation\"].values"
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   230,
   "positionen[\"capital_after\"] = equity[\"capital_after\"].values"
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   240,
   "positionen = positionen.drop(columns=[\"exit_time_equity\"])"
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   242,
   "positionen.to_csv(os.path.join(DATEN_DIR, f\"{BOT}_positionen.csv\"), index=False)"
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   246,
   "\"startkapital\": es.STARTING_CAPITAL,"
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   253,
   "\"endkapital\": ergebnis[\"final_capital\"],"
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   255,
   "\"max_drawdown_pct_bot\": es.calculate_max_drawdown(equity, es.STARTING_CAPITAL),"
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   254,
   "\"rendite_pct\": round((ergebnis[\"final_capital\"] / es.STARTING_CAPITAL - 1) * 100, 2),"
  ],
  [
   "shared/zuteilung.py",
   657,
   "def simuliere_portfolio("
  ],
  [
   "research/vorregistrierung/auswertung.py",
   361,
   "def lies_tagesreihe("
  ],
  [
   "research/vorregistrierung/auswertung.py",
   370,
   "return df.sort_values(\"datum\").reset_index(drop=True)"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   378,
   "def lies_benchmark("
  ],
  [
   "research/vorregistrierung/auswertung.py",
   379,
   "pfad = os.path.join(wurzel, \"benchmark_tagesreihen\", f\"{markt}.csv\")"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   386,
   "return df.sort_values(\"datum\").reset_index(drop=True)"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   498,
   "markt = rd.BOTS[bot][\"markt\"]"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   510,
   "def im_fenster(d):"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   513,
   "maske_s = reihe[\"datum\"].map(im_fenster)"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   514,
   "maske_b = bench[\"datum\"].map(im_fenster)"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   517,
   "gemeinsam = s.index.intersection(b.index)"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   522,
   "sr = s.loc[gemeinsam, \"netto_rendite\"].to_numpy(dtype=float)"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   524,
   "br = b.loc[gemeinsam, \"netto_rendite\"].to_numpy(dtype=float)"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   528,
   "exposure_mittel = float(np.mean(se))"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   10845,
   "shared/zuteilung.py::simuliere_portfolio"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   10803,
   "benchmark_tagesreihen/<bot>.csv"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   11019,
   "im Zitat lies „`<bot>.csv`“ (R39)."
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   11204,
   "Index 149 (nullbasiert) = 2018-01-13, Index 150 = 2018-01-14"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-02a_exposure_tage_laufbereich_marken.md",
   112,
   "R63 — Präzisierung zu R60 (a) (51.5)"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-02a_exposure_tage_laufbereich_marken.md",
   119,
   "Quelle des Grundes: 34 (Kopf"
  ]
 ],
 "zaehlungen": [
  [
   "research/exposure_messung/bot_lauf.py",
   "\\.mean\\(|np\\.mean",
   0
  ],
  [
   "research/vorregistrierung/auswertung.py",
   "dropna",
   0
  ],
  [
   "docs/projektfuehrung/BACKLOG.md",
   "^## 6 — Geparkt, null Arbeit",
   1
  ],
  [
   "docs/projektfuehrung/BACKLOG.md",
   "Aus Fable 02a",
   0
  ],
  [
   "docs/projektfuehrung/FABLE_DIALOG_INDEX.md",
   "^\\| 02a \\|",
   0
  ],
  [
   "docs/projektfuehrung/FABLE_DIALOG_INDEX.md",
   "^\\| 01a \\|",
   1
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   "Ohne Marke; an Fable \\(51\\.10 Nr\\. 7\\)\\.",
   5
  ]
 ],
 "glob_zaehlungen": [
  [
   "strategies/*/equity_simulation.py",
   "^def simulate_portfolio\\(",
   1,
   9
  ]
 ],
 "kalender": {
  "dateien": [],
  "soll": {}
 }
}
DATEN-ENDE
```

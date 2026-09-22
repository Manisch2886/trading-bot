# TB-85 — Die Sperrlisten-Sonde: Abbild, Sonde, Nullpunkt

**Sitzung:** Mac-Sitzung `TB-85 Sperrlisten-Sonde — Abbild, Sonde, Nullpunkt`,
22.09.2026
**Auftrag:** `docs/auftraege/MAC_TB-85_sperrlisten_sonde.md`
**Eingang:** `03e544e` (TB-84) · **Ausgang:** siehe Abschnitt 9
**Belege:** `docs/belege/TB-85/`
**Freigabe:** Betreiberfreigabe 22.09.2026, 07:50 für Schritt 1 und 2 von
Fables Reihenfolge (36.3). **Dieser Auftrag war Schritt 1 allein.**

⚠️ **Die Sitzung wurde durch einen Verbindungsabbruch geteilt.** Teil 1
(Schritt 0/1) endete mit `082c7b1`; die drei Quelldateien lagen danach
vollständig, aber uncommittet im Arbeitsbaum, das Abbild war noch nicht
erzeugt. Teil 2 hat **vor allem anderen die drei Sperrlisten-Hashes erneut
gemessen** und gegen `schritt0_hashes_vorher.txt` gehalten — alle drei
zeichengleich — und dann bei Schritt 3 weitergearbeitet.

---

## 1. Die Klassifikation der 14 Punkte, wie sie gemessen wurde

Gemessen aus `docs/VORREGISTRIERUNG_neuselektion.md`, `## 10. Die Sperrliste`,
Liste Z. 824–871. Vollständige Tabelle mit Titeln und Wortlauten:
`docs/belege/TB-85/schritt1_klassifikation.txt`.

| | Punkte | Zahl |
|---|---|---|
| **allein über Datei-Hashes prüfbar** (`nicht_dateibezogen` leer) | **2, 5** | **zwei** |
| Datei(en) genannt, dazu Nicht-Dateibezogenes | 1, 3, 4, 6, 8, 10, 11, 12, 14 | neun |
| **keine Datei genannt** | **7, 9, 13** | drei |

**Eindeutige Dateipfade: ZEHN** —
`research/vorregistrierung/{registerdaten.py, faltenplan.py,
ergebnisse/faltenplan.json, auswertung.py, benchmark.py,
ergebnisse/benchmark_drawdowns.json, herkunft.py}`,
`config/top25_symbols.txt`, `config/sp500_top150.txt`, `shared/zuteilung.py`.
Auf sie entfallen **14 Pfadnennungen** (`auswertung.py` dreimal, `benchmark.py`
und `herkunft.py` je zweimal).

### Abweichungen zur Vorarbeit (`docs/projektfuehrung/VORARBEIT_sperrlisten_sonde.md`)

Der Auftrag verlangte ausdrücklich, die Vorarbeit **nachzumessen statt zu
übernehmen** (A2). Drei ihrer Aussagen halten der Messung nicht stand:

| | Vorarbeit | gemessen |
|---|---|---|
| **V1** | Punkte **1, 2, 5, 8** sind allein über Datei-Hashes prüfbar (vier) | **nur 2 und 5.** Punkt 1 nennt zusätzlich „Abschnitt 3 dieses Registers" (Registerverweis), Punkt 8 zusätzlich „vier Jahre Vorlauf je Symbol" (eine Regel — laut gebundener Notiz durch Abschnitt 15 ersetzt, der Halbsatz steht aber zeichengleich im Punkt). Beide sind **2**, nicht 0 |
| **V2** | Punkte 6, 11, 12 meinen „eine Funktion, nicht die Datei" — kein Pfad | die Tokens `benchmark.py::bh_tagesrenditen`, `herkunft.py::register()`, `herkunft.py::datenstand()` **nennen die Datei ausdrücklich**. Sie wird gehasht, die Funktion bleibt unmessbar → Punkt **2**. Folge: **`herkunft.py` ist zehnter Pfad** (Vorarbeit: neun) |
| **V3** | Punkt 14 meint „den Docstring, nicht die Datei als ganze" | `auswertung.py` ist genannt und wird gehasht (dieselbe Datei wie in 3 und 5); der Docstring-Anteil bleibt unmessbar → **2** |

Bestätigt wurden: Punkt 7 und 9 nennen nur Konstanten (V5/V4), Punkt 13 ist
reiner Registertext (V6), und `benchmark_drawdowns_vt.json` kommt in **keinem**
der 14 Punkte vor (V7; `grep -c` auf Z. 822–871 = 0, Positivkontrolle geführt).

⭐ **Warum das mehr ist als eine Zählkorrektur:** Die Vorarbeit hätte vier
Punkte als „grün prüfbar" geführt, die es nicht sind. Genau diese Art von
stiller Aufwertung — ein Punkt gilt als geprüft, weil ein Teil von ihm messbar
war — ist der Fehler, der das ganze Thema ausgelöst hat.

---

## 2. Der Nullpunkt-Lauf im Wortlaut

Vollständige Ausgabe: `docs/belege/TB-85/nullpunkt.txt` (Rückgabewert in
Zeile 1). Die Bilanz:

```
(ii) Abbild gegen den Registertext von Abschnitt 10:  [0 in Ordnung]
  Registertext: 14 Punkte, Z. 824-871, Listentext wie bei Erzeugung: ja

Bestimmt, nicht eingetragen (kein Punkt des Abschnitts 10; nicht geprueft, nur genannt):
  research/vorregistrierung/ergebnisse/benchmark_drawdowns_vt.json  4549395f…
  (Register 21.9/23.7 - fuer die Sperrliste bestimmt, Vollzug steht aus)

Bilanz: 2 Punkte in Ordnung (0), 0 mit Befund (1), 12 nicht pruefbar (2); (ii) 0 in Ordnung
RUECKGABEWERT 2 NICHT PRUEFBAR - NICHT PRUEFBAR: Punkt(e) [1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14]
```

⭐ **Kein Punkt mit `1`.** Abbruchkriterium 2 ist nicht eingetreten. Alle **14
Pfadnennungen wurden gemessen** und standen auf `gleich` — keine fehlende,
keine unlesbare, keine abweichende Datei. Die Bilanz ist **exakt die, die
Schritt 1 vorhergesagt hatte** (0 × `1`, 12 × `2`, 2 × `0` → Gesamt `2`).

---

## 3. ⭐ Welche Punkte `2` liefern und warum — der eigentliche Befund

**Zwölf von vierzehn Punkten sind nicht prüfbar.** Die Sonde unterscheidet
dabei zwei Gründe, und das ist der Kern:

| Grund | Punkte | was die Sonde meldet |
|---|---|---|
| **kein Dateipfad im Registertext** — es gibt nichts zu hashen | **7, 9, 13** | `kein Dateipfad im Registertext - nicht messbar: <Wortlaut>` |
| **nennt Nicht-Dateibezogenes** — die Dateien sind gemessen und stehen mit Hash im Bericht, der **Punkt als Ganzes** ist trotzdem nicht abgedeckt | **1, 3, 4, 6, 8, 10, 11, 12, 14** | `nennt Nicht-Dateibezogenes - nicht messbar: <Wortlaut>` |

Was der Registertext über Dateien hinaus nennt, und was keine Prüfsumme je
erfassen wird: einen Registerverweis (1: „Abschnitt 3 dieses Registers";
13: „Abschnitt 8"), Konstanten (3: `registerdaten.SPITZEN_SCHWELLE`;
7: `N_HISTORISCH_JE_BOT`, `CLUSTER_SCHWELLE = 0,9`; 9: `TRADING_FEE_PCT`,
`SLIPPAGE_PCT`; 10: `SEED = 20260913`), Funktionen (6:
`benchmark.py::bh_tagesrenditen`; 11: `herkunft.py::register()`;
12: `herkunft.py::datenstand()`), eine Rechenregel (4: „einschliesslich der
Interpolationsregel"), eine Datenregel (8: „vier Jahre Vorlauf je Symbol"),
einen Ablauf im Docstring (14) und den Repo-Commit (11), der **ausserhalb** des
Repos liegt.

⚠️ **Eine Datei kann die Sonde hashen. Eine Konstante, eine Funktion, eine
Regel oder einen Registerverweis kann sie nicht messen, ohne etwas zu
erfinden.** Ein Punkt, der beides nennt, ist deshalb `2` und nicht `0`: seine
Dateien stehen gemessen im Bericht, sein Rest nicht. `0` bekommen nur die
Punkte **2** und **5**, die nichts als Dateien nennen — bei ihnen und nur bei
ihnen heisst „geprüft und in Ordnung" wirklich, dass der ganze Punkt gedeckt
ist.

⭐ **Das ist die Antwort auf die Frage, die den Auftrag ausgelöst hat:** Die
Sperrliste ist zu **zwei Vierzehnteln** maschinell prüfbar. Die übrigen zwölf
Punkte hängen weiterhin an der Sorgfalt dessen, der sie liest — nur sagt das
jetzt ein Programm laut, statt dass es eine stille Annahme bleibt.

---

## 4. Die sieben Selbstprüfungen

`shared/test_sperrlistensonde.py`, **49 Proben, 49 bestanden**, Rückgabewert 0.
Vollständige Ausgabe mit jeder einzelnen Probe:
`docs/belege/TB-85/schritt5_selbstpruefung.txt`.

| B5 | Fall | erwartet | gemessen |
|---:|---|---|---|
| **1** | Abbild stimmt mit Repo und Registertext | `0` oder `2` | **`2`** — 2 Punkte auf `0`, kein Punkt auf `1`, (ii) auf `0` (7 Proben) |
| **2** | Eine Datei verändert (ein Byte angehängt) | `1`, Punkt genannt | **`1`**, Punkt 1 trägt den Befund, der Grund nennt die Datei, kein zweiter `1`er; nach dem Zurücksetzen wieder `2` (6 Proben) |
| **3** | Ein Punkt fehlt im Abbild | `1` | **`1`**, (ii) nennt „13 gegen 14" (2 Proben) |
| **4** | Ein Punkt zu viel im Abbild | `1` | **`1`**, (ii) nennt 15; das `1` aus (ii) schlägt das `2` des erfundenen Punktes (3 Proben) |
| **5** | Abbilddatei fehlt | `2` | **`2`**, kein Punkt als geprüft geführt; ebenso bei kaputtem JSON (4 Proben) |
| **6** | Registerdatei nicht lesbar | `2` | **`2`** — fehlend und ohne Leserecht; (i) wird trotzdem gemessen; ein Register mit 15. Punkt gibt `1` (6 Proben) |
| **7** | Ein Punkt ohne Pfade (13) | `2`, mit Nennung | **`2`**, Grund nennt „kein Dateipfad" und den Wortlaut „Abschnitt 8"; 7 und 9 ebenso (5 Proben) |

Dazu **fünfzehn weitere Mutationsproben** (Teil H): `1` schlägt `2` (H1);
veränderter Titel im Abbild → `1` mit Feldnennung (H2); ein zusätzlicher Pfad
im Abbild → `1` aus (ii), obwohl (i) gleich ist (H3); eine im Abbild genannte
Datei fehlt → `2` mit „Datei fehlt", **nie `0`** (H4); ein verfälschter Hash
im Abbild → `1`, obwohl die Datei unverändert ist (H5); der Erzeuger schreibt
nur einmal (H6a–d); die Befehlszeile liefert denselben Wert wie die Funktion
und `--json` ist gültiges JSON (H7a–e); **die Sonde schreibt nichts** —
Dateiliste und Grössen vorher = nachher (H8). Dazu `fall_0`, der das
Probe-Abbild in der Kopie anlegt.

⚠️⚠️ **Alles lief auf Kopien** in einem Wegwerf-Ordner unter `$TMPDIR`
(`tempfile.mkdtemp`, Präfix `tb85_sonde_`), der am Ende entfernt wurde — nie
gegen die echten gesperrten Dateien. Unmittelbar nach dem Lauf wurden die drei
Sperrlisten-Hashes erneut gemessen: unverändert.

---

## 5. Die Mutationsprobe am Erzeuger (Schritt 7)

`docs/belege/TB-85/schritt7_mutationsprobe.txt`. Der zweite Aufruf gegen
dasselbe, bereits vorhandene Ziel:

```
ABBRUCH (36.1 (2)): Ziel existiert, nichts geschrieben.
  Pfad:   research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-22.json
  SHA-256: 6a1b732ed662d339a99785933ba130085069884be2d2d5990fd081124767298c
Rückgabewert 1
```

Hash und Grösse vorher = nachher (`6a1b732e…`, 6948 Bytes): **nichts
geschrieben, auch nicht mit identischem Inhalt.** Die Ausgabe ging nach
`stderr`. Die Sperre hängt nicht allein an `os.path.exists`: geöffnet wird mit
`O_CREAT|O_EXCL`, was auch ein Ziel abfängt, das zwischen Prüfung und Schreiben
entsteht.

---

## 6. Die drei Hashes vorher und nachher

| Datei | vorher (08:33) | nachher (17:37) |
|---|---|---|
| `ergebnisse/faltenplan.json` | `0e54ac5c…d32339` | **gleich** |
| `ergebnisse/benchmark_drawdowns.json` | `a163c498…36d1ee` | **gleich** |
| `ergebnisse/benchmark_drawdowns_vt.json` | `4549395f…18745d` | **gleich** |

**Vier Messungen an diesem Tag**, alle gleich: Schritt 0, zu Beginn der
Fortsetzung nach dem Verbindungsabbruch, unmittelbar nach der Selbstprüfung
und Schritt 8. Belege: `schritt0_hashes_vorher.txt`,
`schritt5_selbstpruefung.txt`, `schritt8_hashes_nachher.txt`.

Zwei dieser Hashes stehen zusätzlich **im Abbild selbst** (Punkt 2 und Punkt 4)
und wurden dort frisch gemessen — sie stimmen zeichengleich mit Schritt 0.

---

## 7. Das Handwerk — drei neue Dateien, nichts Vorhandenes angefasst

| Datei | Zeilen | was sie ist |
|---|---:|---|
| `research/vorregistrierung/sperrliste_abbild.py` | 107 | der **Erzeuger** (36.6/33.3). Einmal-Schreibsperre nach 36.1 (2), kein Ziel als Voreinstellung nach 36.1 (3) |
| `shared/sperrlistensonde.py` | 502 | die **Sonde** (36.2/36.5/36.6), drei Ausgänge nach Bauart `shared/snapshot.py` |
| `shared/test_sperrlistensonde.py` | 385 | die **Selbstprüfung**, 49 Mutationsproben auf Kopien |
| `ergebnisse/sperrliste_abbild_2026-09-22.json` | 6948 B | das **Abbild**, `6a1b732e…`, 14 Punkte |

**Warum `shared/`:** Es ist der Ort der gemeinsamen Werkzeuge (`snapshot.py`,
`regimewache.py`). Nicht `herkunft.py` — Fable 22c: *„`herkunft.py` scheidet
als Ort aus"*, es steht selbst auf der Sperrliste (Punkt 11/12).

**Der Parser steht genau einmal.** Erzeuger und Prüfung (ii) lesen Abschnitt 10
mit derselben Funktion `lies_abschnitt_10`. ⚠️ **Das ist eine bewusst gewählte
Schwäche mit benanntem Gegengewicht:** Ein Parserfehler wäre für (ii) unsichtbar,
weil beide Seiten denselben Fehler machten. Dagegen stehen die **von Hand
gemessene Klassifikation** (Schritt 1, unabhängig vom Code erhoben) und die
Mutationsproben, die den Registertext selbst verändern (Fall 6e). Die Alternative
— zwei Parser — hätte zwei Lesarten erzeugt, die auseinanderlaufen können; das
Projekt führt jede Grösse genau einmal.

**Die Leseregeln (R1–R6)** stehen im Kopf von `sperrlistensonde.py` und
zeichengleich in `schritt1_klassifikation.txt`. Zwei sind nicht selbstverständlich:
**R2** — eingerückte Blockquote-Zeilen (`   > …`) sind Tatsachennotizen und Marken
am alten Ort, nicht Teil des Punktes (betrifft Punkt 2 und Punkt 8); **R4** — ein
`datei::funktion`-Token nennt die Datei **und** die Funktion, `modul.KONSTANTE`
ist kein Pfad.

**Ein Commit für Schritt 2 und 4 zusammen** (`cf8b3fa`): Der Erzeuger liest den
Parser der Sonde ein, ein Commit mit dem Erzeuger allein wäre nicht lauffähig
gewesen. Die Schritte bleiben in den Belegen getrennt nachgewiesen.

---

## 8. ⚠️ Offen und benannt

| | offen |
|---|---|
| ⚠️⚠️ | **Fables Antwort auf Anfrage 22c steht aus.** Zwei Fragen hängen daran (beide unten), und beide sind so gebaut, dass die Sonde ohne die Antwort auskommt |
| **(a)** | **Prüft die Sonde auch „für die Sperrliste bestimmte" Pfade?** `ergebnisse/benchmark_drawdowns_vt.json` (`4549395f…`) ist **kein Punkt** des Abschnitts 10, sondern nach 21.9/23.7 *„für die Sperrliste bestimmt"* — der Vollzug steht aus. Wie A3 verlangt, steht die Datei **nicht im Abbild**, sondern im Bericht der Sonde in einem eigenen Abschnitt „bestimmt, nicht eingetragen", mit ihrem heutigen Hash und **ohne Wertung** (sie geht in keinen Rückgabewert ein) |
| **(b)** | **Gilt `2` auch für nicht-messbare Registerpunkte?** Das ist der Vorschlag des steuernden Chats (22c, Abschnitt 4), hier umgesetzt: jeder Punkt ohne Messbares wird **einzeln mit `2` gemeldet und benannt**; Gesamtwert `1` vor `2` vor `0`. Entscheidet Fable anders, ist die Sonde **neu und nicht gesperrt** — also änderbar. Nach heutiger Messung hinge daran der Gesamtwert von **zwölf** der vierzehn Punkte |
| | **Der Registereintrag des Abbild-Hashes ist TB-87**, nicht dieser Auftrag. `6a1b732e…` steht bisher nur in den Belegen und im Journal |
| | **Schritt 2 von 36.3** (`faltenplan.py main()` absichern) ist **TB-86**. Freigabe dafür liegt vor (22.09., 07:50), der Auftrag ist noch nicht geschrieben |
| ⚠️ | **Der Auftrag nennt `docs/auftraege/ERGEBNIS_TB-85.md`**, die Reihe liegt aber seit TB-80 unter `docs/ERGEBNIS_TB-NN_<thema>.md`. Dieses Dokument folgt der Reihe; TB-84 hat es ebenso gehandhabt. Sollte der Auftragspfad gemeint sein, ist es ein Verschieben |

---

## 9. ⛔ Was NICHT getan wurde

| ⛔ | |
|---|---|
| ⛔ | **Keine vorhandene `.py` geändert.** `git diff --numstat 082c7b1 HEAD` zeigt neun Dateien, jede mit **0** in der zweiten Spalte — ausschliesslich Neuanlagen. (Gegen `03e544e` gerechnet kommt `docs/auftraege/AKTUELLER_AUFTRAG.md` mit `3 3` dazu; das ist der Zeiger, den der **Betreiber** in `1b9c96f` gesetzt hat, nicht diese Sitzung — sie hat ihn nur gelesen) |
| ⛔ | **`python3 faltenplan.py` nicht aufgerufen** — `main()` überschreibt `ergebnisse/faltenplan.json` (Sperrlistenpunkt 2). Die Datei hat vor und nach der Sitzung denselben Hash |
| ⛔ | **`herkunft.py` nicht angefasst** — weder gelesen zum Ändern noch als Ort für die Sonde. Ihre Listen `EINGEFROREN` und `SPERRLISTE_DATEIEN` kennt die Sonde nicht (36.6: sie sind nicht das Abbild) |
| ⛔ | **Keine gesperrte Datei geschrieben.** Die Sonde schreibt überhaupt nichts (H8 misst das); der Erzeuger schreibt genau eine neue Datei, die vorher nicht existierte |
| ⛔ | **Kein Registereintrag, kein Hash auf die Sperrliste.** Das Register kommt in **keinem** Diff dieser Sitzung vor (`git diff --numstat … -- docs/VORREGISTRIERUNG_neuselektion.md` = 0 Zeilen) |
| ⛔ | **Nichts repariert.** Es gab nichts zu reparieren — hätte die Sonde eine `1` gemeldet, wäre das nach 36.2 eine Tatsachennotiz gewesen, keine stille Korrektur |

---

## 10. Commits

| Commit | Inhalt |
|---|---|
| `082c7b1` | Schritt 0/1 — Nullmessung, Abschnitt 10 ausgelesen, 14 Punkte klassifiziert (Teil 1, vor dem Verbindungsabbruch) |
| `cf8b3fa` | Schritt 2 und 4 — Erzeuger und Sonde |
| `f3dc9a2` | Schritt 3 und 5–8 — Abbild erzeugt, Selbstprüfung, Nullpunkt, Mutationsprobe, Hashes nachher |
| Abgabe | Ergebnisdokument, Journalblock CM, Abschlussbeleg |

*Geschrieben 22.09.2026 von der Mac-Sitzung TB-85 selbst.*

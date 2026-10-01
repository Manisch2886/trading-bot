# Inventar E-2 / TB-126 — Fable-Blöcke R18–R55 für das Register

*Helfer des steuernden Chats, 01.10.2026. Nur gelesen, nichts geändert. Grundlage: lokaler Abzug
`/mnt/user-data/uploads/trading-bot/` (Stand laut Auftrag HEAD `41864d4`; ohne `.git`, HEAD dort nicht messbar).
Kennzeichnung: **[belegt]** = mit Fundstelle gelesen · **[erschlossen]** = Schluss des Helfers · **[PLATZHALTER]** = unklar,
nicht geraten. Sichtschutz 27.1: keine Ergebnisgrösse gelesen oder zitiert; Zahlen unten sind Zeilen, Bytes, Hashes,
Balkenindizes.*

## 0. Quellen und Hashes (gemessen)

| Kürzel | Datei | md5 | Zeilen |
|---|---|---|---|
| 27c | `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md` | `ff96392e…` | 210 |
| 29b | `docs/projektfuehrung/FABLE_ANTWORT_2026-09-29b_sammlung_erzeuger_kalter_leser.md` | `898d5bd5…` | 268 |
| 30a | `docs/projektfuehrung/FABLE_ANTWORT_2026-09-30a_vorgepruefte_fragen_e2.md` | `f9cdbbef…` (= UEBERGABE Z. 193) | 32 |
| VM | `docs/projektfuehrung/VORMESSUNG_E-2_2026-09-29.md` (Abschnitte 1–3, Nachtrag Abschnitt 4, Nachtrag 20:15) | `ae4d5233…` | 60 |
| TB-122 | `docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md` | `17cf553b…` | 375 |
| TB-124 | `docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md` | `50ce291d…` | 382 |
| UEB | `docs/projektfuehrung/UEBERGABE.md` | `d5f6ca30…` | 391 |
| BL | `docs/projektfuehrung/BACKLOG.md` | `75f4577f…` (= UEB Z. 387) | 230 |
| REG | `docs/VORREGISTRIERUNG_neuselektion.md` | sha256 `18e39ee2…` (= REGISTER_INDEX Z. 4) | 10 347 |

R53–R55 gegen die Ablage: md5 je Block mit abschliessendem Zeilenumbruch nachgerechnet — R53 `cbaeea5b…` 1 047 B,
R54 `914ddd1d…` 1 241 B, R55 `1f3e534b…` 1 016 B; gleich den Werten in UEB Z. 391 **[belegt]**.
27c und 29b: Repo-Fassung gegen Ablage **nicht maschinell verglichen** (Ablage über `project_read` sichtbar, kein
Byte-Vergleich gemacht) — Vorbehalt wie Register 46.0 **[PLATZHALTER: cmp der R-Blöcke 27c/29b gegen Ablage]**.

## 1. Zählung und Schnittregel

**38 Blöcke R18–R55, ohne Lücke, ohne Dopplung** (27c: 15, 29b: 20, 30a: 3) — maschinell nachgezählt **[belegt]**.
Kein Zeilenanfang `R<n> — ` ausserhalb der drei Registerblöcke.

| Quelle | Zaun | Beginn eines Blocks (Regex) | Ende eines Blocks | Form |
|---|---|---|---|---|
| 27c | ja: Z. 160 ```` ```markdown ```` bis Z. 210 ```` ``` ```` | `^\*\*R(\d+) — ` (fett, Gedankenstrich U+2014) | einschliesslich der ersten Folgezeile `^\*Quelle des Grundes:\*` | Markdown (Fett/Kursiv), Zitate „…" mit geradem Schlusszeichen |
| 29b | ja: Z. 189 ```` ``` ```` (ohne Sprache) bis Z. 268 ```` ``` ```` | `^R(\d+) — ` | einschliesslich der ersten Folgezeile `^Quelle des Grundes:` | Klartext ohne Auszeichnung, Zitate „…“ |
| 30a | **kein Zaun**; Überschrift Z. 24 „Registerblock — …“ ohne `##` (Abschrift aus `.txt`, UEB Z. 193) | `^R(\d+) — ` | einschliesslich der ersten Folgezeile `^Quelle des Grundes:`; R55 endet mit Dateiende (Z. 32, mit `\n`) | Klartext |

Geprüft: In jedem Block gibt es **genau eine** Zeile, die mit „Quelle des Grundes:“ beginnt, und sie ist zugleich die
einzige, die auf „Kein Ergebnis.“ endet (38/38). Blöcke vor einem Zaunende (R32, R52) enden damit **vor** der
Zaunzeile; die Leerzeile zwischen Blöcken gehört zu keinem Block. Mehrzeilige Blöcke: R31 (7 Z.), R48 (13 Z.,
Unterzeilen `(a)`–`(k)`), R49 (10 Z., `(a)`–`(h)`); alle übrigen 2 Zeilen. Unterzeilen beginnen nie mit `R<n> — `.
*[erschlossen]* Die Quellen unterscheiden sich in der Auszeichnung (27c fett/kursiv, 29b/30a ohne); „zeichengleich“
heisst also: je Quelle so, wie sie ist (Bauart 46.0: Blockzitat `> `, `diff` je Baustein rc 0).

## 2. Inventar je Block

Spalten: **Ort** = was Fable als Bezug nennt (Überschrift „… zu X“) und ob eine Marke am alten Ort verlangt ist
(„ausdrücklich“ = im Block/R51 genannt; „Regel 34“ = folgt nur aus der Registerpraxis, REG Z. 5899ff., 46.0
Z. 10119–10124 **[erschlossen]**). Fable nennt **für keinen Block** eine Abschnittsnummer. **Vor.** = Voraussetzung,
die Fable nennt, und Stand. **TN** = zusätzliche Tatsachennotiz.

| R | Quelle, Zeilen | Gegenstand | Ort laut Fable | Voraussetzung → Stand (Beleg) | TN nötig? Wortlaut |
|---|---|---|---|---|---|
| R18 | 27c Z. 161–162 | Leiter L1: erst Anlagen, dann Zellen | Präzisierung zu 16.4 (m), (h), (l); Marke 16.4 nach Regel 34 | keine | nein |
| R19 | 27c Z. 164–165 | Leiter L2: Zahl der Zellen = Zeilen (g) | Präzisierung zu 16.4 (h), (j), (k) | keine | nein |
| R20 | 27c Z. 167–168 | Leiter L3: Anlage ohne aktive Zelle | Ergänzung zu 16.4 (l), (j) | keine | nein |
| R21 | 27c Z. 170–171 | Leiter L4: Schatten nach Herkunft, Prüfung 4⁹ | Präzisierung zu 16.4 (b), (i), (j); Ergänzung zu 7.1 | Im Block keine; in der Prosa 27c Z. 75 „Voraussetzung, kein Bestand“ (Leiter-Skript fehlt, 16.11 Z. 3; Journal-Herkunft = Anforderung an Stufe IV); Unsicher Z. 138–140. → **offen, aber kein Bestand** | nein; später TN zu 16.4 nach Bau des Leiter-Skripts (27c Z. 125) |
| R22 | 27c Z. 173–174 | Leiter L5: Faktor 2 vor Netting | Präzisierung zu 16.4 (a), (i) | keine | nein |
| R23 | 27c Z. 176–177 | Budgetanteil und Höhe der Benchmark-Position | Präzisierung zu 16.4 (b), 7.1, 15.6 (c) | keine | nein |
| R24 | 27c Z. 179–180 | Gleichteilung bei ungleicher Besetzung, Deckel | Tatsachennotiz zu 16.4 (h), (g), mit Entscheidungsvorlage (a)/(b) | keine Messung. Betreiberentscheid „(a) So lassen“ laut 29b Z. 26 **[PLATZHALTER: Fundstelle des Entscheids, vermutlich UEBERGABE_ARCHIV, nicht im Abzug]** | nicht in der Liste; *[erschlossen]* Vermerk zum Entscheid unter dem Block sinnvoll |
| R25 | 27c Z. 182–183 | 46.9 bestätigt: Herkunft nur unter Modus Vertrag | Bestätigung 46.9; Ergänzung zu 12 und R14 (46.5); Marken 12/46.5/46.9 nach Regel 34 | Docstring „unter dem Modus“ seit Block D → **erfüllt, Fundstelle abweichend**: AW Z. 53–62 statt 51–52, Wortlaut „Selektionsmodus“ (VM Z. 14) | **ja** (Liste): „R25 Z. 53–62“. Wortlaut **fehlt**, zu schreiben aus VM Z. 14. Schliesst 46.10 (5) |
| R26 | 27c Z. 185–186 | alle neun unter Modus; `--bot` kein Bericht | Ergänzung zu 12, R14 (46.5), 35.4 | `--bot` läuft unter Modus bis Bericht → **erfüllt in der Sache an `852f253`** (TB-117 E, `docs/belege/TB-117/e_auswertung_modus.txt` Z. 1, 5), Fundstelle E statt J-7 (VM Z. 15); an HEAD **nicht neu gemessen** (VM Z. 33); Laufwrapper (35.4) nicht gefunden (VM Z. 15). Fable quittiert E (30a Z. 5) | **ja** (Liste): „R26 TB-117 E“. Wortlaut **fehlt**, aus VM Z. 15 |
| R27 | 27c Z. 188–189 | Bedingung 5 bleibt; voller Commit-Hash am Tag | Tatsachennotiz zu R14 Bed. 5; Ergänzung zu den Tag-Vorbedingungen | keine | nein |
| R28 | 27c Z. 191–192 | drei Orte des Datenstands, je mit Probe | Tatsachennotiz zu 18 und Plan-Punkt 6 | Probe `snapshot.py` gegen 18 → VM: Nein-Fall (Z. 16) ⇒ Handwerk; **inzwischen erfüllt** durch TB-124 D (`shared/test_verankerter_datenstand.py` 3/3, `7453469`; TB-124 Z. 239–282; abgenommen UEB Z. 357–363). **Abweichung in der Bestandsangabe [erschlossen]:** Block nennt zwei Codekopien; gemessen gibt es eine dritte, `research/registernachtrag_tb48/pruefe_abschnitt17.py:97` ohne Registerprobe (VM Z. 16, TB-124 Z. 268–270, 279–280). Ob Fable das kennt: **[PLATZHALTER]** | nicht in der Liste; Entwurf **vorhanden**: TB-124 Z. 273–282 „Satz zu R28 für E-2“ (Liste, 10 Z., 820 B), in Prosa zu bringen |
| R29 | 27c Z. 194–195 | `herkunft.py` im Laufbereich; E5 als Lauf | Ergänzung zu 42.2 E5, R4 (45.4), R5 (a) (45.5); Tatsachennotiz zu 44-6 (im Block) | keine eckige Voraussetzung (stützt sich auf TB-117 E). *[erschlossen]* „Sonde im Laufwrapper (36.2 (b))“ betrifft den Tag; Laufwrapper laut VM Z. 15 heute nicht gefunden | TN zu 44-6 ist Teil des Blocks |
| R30 | 27c Z. 197–198 | Erzeuger und Auswertung am Tag-Commit | Ergänzung zu 14 und zu den Tag-Vorbedingungen | keine | nein |
| R31 | 27c Z. 200–206 | Tatsachennotizen 27c (a)–(e) | (a) zu R8 (a) (45.8); (b) Tests 8a/H7f; (d) zu 27.3; (e) zu 45 | keine; (d) nennt Kopie am `1e11457` — mit E-2 überholt, bleibt zeichengleich | Block selbst |
| R32 | 27c Z. 208–209 | Anfangsbestand Verfahrensprüfer, dritter Umzug | Tatsachennotiz zu 27 | keine | Block selbst |
| R33 | 29b Z. 190–191 | `zellen.csv` je Zelle × Falte, Nullzeile | Berichtigung zu 45.5 (b) („lies“) ⇒ Marke 45.5 (b) nach Regel 34; Bezug 43-7 | (Prosa 29b Z. 85, 165) Trade-Zahl-Feld im Vertrag → **erfüllt**: `n_trades` AW Z. 39, Pflichtspalte Z. 133 (VM Z. 17) | nicht in der Liste; *[erschlossen]* nach Bauart 34.0 (REG Z. 5911–5914) Messung mitführen; Wortlaut fehlt |
| R34 | 29b Z. 193–194 | `zellenbericht.csv`: 22.2-Anteile, Haltedauer, Beginn | Ergänzung zu 22.2 und 45.5 | keine | nein |
| R35 | 29b Z. 196–197 | Bootstrap: Bauart, kein Intervall im Lauf | Ergänzung zu 15.3 und Tatsachennotiz (im Block, TB-120) | keine | Block selbst |
| R36 | 29b Z. 199–200 | zwei Drawdown-Spalten, Nachrechnung, Ausschnitt | Präzisierung zu 24.2 und 45.5; vollzieht K4j (1)(2) | (Unsicher 29b Z. 166) MtM-Drawdown wie beschrieben → **erfüllt** in `mtm_kern.py:296–304`, Raster Z. 135–139 (VM Z. 18); Vertrag führt heute nur `kapital_drawdown_pct` (erwartet) | nicht in der Liste; *[erschlossen]* wie R33 |
| R37 | 29b Z. 202–203 | „Bestätigungsperiode“: zwei Zeiträume | Präzisierung zu 16.6, 35.1, 16.4 (c)/(d), 5.1 Nr. 7 | (Unsicher Z. 170) Einordnung Lesart/Ergänzung; keine Bestandsfrage, nicht gemessen | nein |
| R38 | 29b Z. 205–206 | Faltenkohärenz, `symbole_je_falte.csv` | Ergänzung zu 16.7 (d); schliesst 16.11 Z. 7 | keine | nein |
| R39 | 29b Z. 208–209 | Ausgaben Zellen-Erzeuger; Feldliste als Registertext | Ergänzung zu 46.3 (R12); Berichtigung des Datenvertrags (Code-Docstring, „`<markt>`“ lies „`<bot>`“) | **offen:** Block verlangt, dass „im Registerauftrag E-2 aus dem Docstring von auswertung.py gemessen eingetragen“ wird — keine solche Messung in VM oder Nachträgen gefunden. *[erschlossen]* `zellenbericht.csv`, `symbole_je_falte.csv` sind neu, haben im Docstring keine Feldliste **[PLATZHALTER: Messung AW-Docstring, laut 29b Z. 146 Z. 40–58 am `cc096e1`]** | **ja, Registertext** (Feldliste) — zu messen und zu schreiben |
| R40 | 29b Z. 211–212 | Schreibregel: Erzeuger-Ausgaben einmalig | Ersteintrag (bezieht 36.1 (2)/(3)) | keine | nein |
| R41 | 29b Z. 214–215 | `haltedauer_balken`: Kerzenzählung, Umrechnung | Ergänzung zu 41.2 B6/B7, 15.3 (b); bei Abweichung TN an 15.4 | **weicht ab:** TB-24 rechnete Zeitstempeldifferenz (`research/faltenplan_neun/embargo_neun.py:36–37, 236–238`, VM Z. 20). Abweichungsfall im Block vorgesehen und **von Fable quittiert** (30a Z. 5). **Offen:** Neurechnung nach 41.3 C2 als Mac-Messung (UEB Z. 109; VM Z. 31) | **ja** (Liste): „R41 Zeitstempeldifferenz“ → TN zu 15.4. Wortlaut **fehlt**, aus VM Z. 20 |
| R42 | 29b Z. 217–218 | Bindung neue Listen: Punkt 15 und `eingefroren` | Ergänzung zu 40.6, 45.3, 46.3; neuer Punkt 15 in Abschnitt 10 erst „vor dem Tag“ | keine. *[erschlossen]* In Abschnitt 10 steht nach Praxis keine Marke (46.0 Z. 10122) — der Punkt 15 ist Listentext-Fortschreibung, nicht Teil von E-2 | nein |
| R43 | 29b Z. 220–221 | Zellen-Kern; Wache 29.4 im Erzeuger; 11.2 | Registertext; Berichtigung zu 29.4/34.5 („lies“) ⇒ Marken 29.4, 34.5 nach Regel 34; TN zu 11.2; TN „nicht im Laufpfad“ für neun Optimierer | keine | Block selbst |
| R44 | 29b Z. 223–224 | Listen erst nach Posten 3 und 4 | Ergänzung zu 40.6 | keine | nein |
| R45 | 29b Z. 226–227 | additive Positionsrückgabe `zuteilung.py` | Registertext zu Sperrlistenpunkt 10 (Abschnitt 10: keine Marke nach Praxis) | keine | nein |
| R46 | 29b Z. 229–230 | Abnahme Zellen-Erzeuger auf Test-Snapshot | Ersteintrag | keine | später TN der Abnahme |
| R47 | 29b Z. 232–233 | Parameterdateien per Import-Audit | Präzisierung zu 40.6 (TN zu 5.4) | keine. Bezug: Betreiberentscheid F3 „bleibt so; Fables R47 regelt es in E-2“ (UEB Z. 33); TB-122 0d | nein (TN zu 5.4 kommt mit dem Listen-Erzeuger) |
| R48 | 29b Z. 235–247 | Lesarten zu 0–12, (a)–(k) | je Unterpunkt: (a) Festl. 4 (Marke ausdrücklich, via R51); (b) 9; (c) 7 (d); (d) 4.2/7.1/7 (c); (e) 23.3/4.2; (f) 2.5; (g) 8.1; (h) 2.2; (i) 2.1; (j) Festl. 3/4b; (k) Präzisierung zu 10.1 (liegt in Abschnitt 10, REG Z. 1061 ⇒ keine Marke, *[erschlossen]* Indexzeile wie 42.3 F8) | (c) **erfüllt** AW Z. 554–556, 710–719; Randfall → R55 (VM Z. 21). **(d) offen/abweichend:** `mittlere_exposure` im Code nicht gebildet (AW Z. 405 Eingabe); vorhandene Grössen bewerten zum Einstand, nicht wie MtM (VM Z. 19); „bleibt offen, bis es den Zellen-Erzeuger gibt“ (VM Z. 33); Fable führt sie offen (30a Z. 16). (f) **erfüllt** nach Lesart „zählt als Stufe mit“ (30a Z. 6; VM Z. 48: REG Z. 342, 350). **(g) abweichend** Summe ↔ Produkt (VM Z. 23, berichtigt Z. 44–47) → von Fable aufgelöst durch **R54**; T − 1 und Perzentil passen. (i) **erfüllt** (`pruefe_grenzsaetze.py` Z. 100–148, VM Z. 24) | **ja** (Liste): R48 (f), Wortlaut **fehlt** (Quelle VM Z. 22 + Z. 48). *[erschlossen]* auch (c), (d), (g) brauchen einen Vermerk |
| R49 | 29b Z. 249–258 | Tatsachennotizen zu 0–12, (a)–(h) | „Marke je am alten Ort“ (ausdrücklich): 2.2, 2.7, 3/4.4, 12, 38.2 (Marke in 6), Kopf, 11; (g) Abschnitt 10 → **Indexzeile** (R51) | (b) Messbitte **gemessen, Ort weicht ab:** Stufen gebildet in `messgroessen.py::je_zeitrahmen` (Z. 169–219), `registerdaten.py:558–565` liest nur (VM Z. 25); laut VM Z. 31 in E-2 mit TN. *[erschlossen]* (h) „11.3 offen (E-1)“ ist mit TB-122/TB-124 überholt | **ja** (Liste): R49 (b). Wortlaut **fehlt**, aus VM Z. 25 |
| R50 | 29b Z. 260–261 | Kennzahldefinitionen im Code; TN TB-121 | Ergänzung zu 12; TN zu TB-121 | Messbitte „Ob“: **ja/ja** (`registerdaten.py:270`, `registerbericht.py:111–120`); Zahl „34“ **nicht gemessen** (Zählweise offen); Orte anders als Fables Prosa (Zellenname `AW::zelle_id` Z. 272–274; Cluster `kennzahlen.py::cluster_anzahl`) (VM Z. 26). **Offen, braucht Lauf:** „34“, Ausstiegskonvention der neun `backtest_*.py` (VM Z. 33). **Offen:** DSR-Einheiten `kennzahlen.py:222–224` „vor R50 prüfen“ (VM Z. 34, UEB Z. 285). Die Kennzahl-TN selbst sind „vor dem Tag“ verlangt, nicht in E-2 | **ja** (Liste): „R50 Orte“. Wortlaut **fehlt**, aus VM Z. 26 |
| R51 | 29b Z. 263–264 | Marken am alten Ort für 0–12 | Handwerk im Registerauftrag: Festl. 4; Festl. 2, 7 (a); 3/4.4; 4.2; 5.3, 15.6; **9**; 10 (Indexzeile); 11; 12; Kopf; 17.3/17.9/18 (Indexzeile) | keine Messung. *[erschlossen]* Marke in 9 gegen „keine in 9“ (45.10 Z. 10062, 46.10 Z. 10266); Grund dort nur R8 (d) „nach dem Tag“ (Z. 10021) **[PLATZHALTER: ob Marke in 9 zulässig]** | nein; Indexzeilen in REGISTER_INDEX |
| R52 | 29b Z. 266–267 | Tatsachennotizen 29b (zehnter/elfter Fall) | Tatsachennotiz; (b) zu 45.5 (b)/R33 | keine | Block selbst |
| R53 | 30a Z. 25–26 | Indikator-Vorlauf = grösster Vorlauf des Rasters | Präzisierung zu 4a (i) (25.3, 28.6); TN zu 25.2, 15.5, 21.4 (im Block) | (30a Z. 18) Stufen und feste Fenster maschinell aus `registerdaten.py`? → **teilweise** (VM Z. 58): Stufen und Bollinger-Fenster ja; `VOLUME_AVG_PERIOD`, Turtle-Soup-Warm-up nein. **Abweichung [erschlossen]:** Block sagt „nicht als Literal gesetzt“; Fables Rückfall „Literal mit Test nach 32.5 (c)“ steht nur im Unsicher (Z. 18), nicht im Block; Entscheid „E-2 bzw. Auftrag R53 (a)“ (VM Z. 58). **Offen:** Zählweise L + 20 / L + 19 (unten (b)); `faltenplan_neun.py` (BL Z. 213) | *[erschlossen]* Messung mitführen; Zählweise-Notiz zu schreiben |
| R54 | 30a Z. 28–29 | Renditen verkettet statt summiert | Berichtigung zu 2a (15.4 (a), REG Z. 1364; Zitat auch in 24.1 Z. 4091) und zu R48 (g) („lies“) ⇒ Marken 15.4 und an R48 (g) | (30a Z. 19) `netto_rendite_pct` ohne Leser im Urteil → **trifft zu** (VM Z. 57: Pflichtspalte AW Z. 134, gelesen nur Bestätigungsperiode Z. 624, berichtet Z. 823) | *[erschlossen]* Messung mitführen |
| R55 | 30a Z. 31–32 | 7 (d) bei leerer Menge: nicht erfüllt | Ergänzung zu 7 (d) und TN (Schlüsselname) | Code rechnet `None ⇒ False` (VM Z. 21) → passt. Nebenfall „keine Zelle zulässig“ laut 30a Z. 14 „erschlossen … bis eine Probe es misst“ → **nicht gemessen**; Probe Handwerk offen (BL Z. 217) | TN im Block |

**Blöcke mit offener oder abweichender Voraussetzung (Kurzliste):**
- abweichend: **R41** (Zeitstempeldifferenz; Abweichungsfall im Block, von Fable quittiert; Neurechnung offen),
  **R48 (g)** (Summe/Produkt; aufgelöst durch R54), **R48 (d)** (Grösse fehlt im Code, Vorhandenes zum Einstand —
  offen bis Zellen-Erzeuger), **R49 (b)** (Ort), **R53** (feste Fenster nicht lesbar vs. „kein Literal“; Zählweise),
  **R28** (vierte Fundstelle des Datenstands, im Block nicht genannt).
- offen: **R26** an HEAD, **R39** (Feldliste in E-2 zu messen), **R50** („34“, Ausstieg, DSR-Einheiten), **R55**
  (Nebenfall), **R21** (Anforderung an Stufe IV, kein Bestand).
- erfüllt mit anderer Fundstelle: **R25** (Z. 53–62), **R26** (TB-117 E).
- *[erschlossen]* Regel „abweichend ⇒ melden, nicht eintragen“ (29b Z. 166; R50-Text): R48 als **ganzer Block** hängt
  an (d); R41 und R48 (g) sind schon gemeldet und von Fable beantwortet. Entscheidung, ob R48 mit Vermerk „(d) offen“
  eingetragen oder zurückgehalten wird: **[PLATZHALTER: steuernder Chat]**.

## 3. Gesondert

### (a) Gliederung des neuen Abschnitts und Reihenfolge

**Fable sagt [belegt]:**
- 27c Z. 122: „Registerauftrag mit 27c (… E-2) | Verfahren: R18–R32 zeichengleich; **Nummer vergibt der steuernde
  Chat** | R18–R30“ (Registertext-Spalte nennt R18–R30; R31/R32 sind Tatsachennotizen).
- 29b Z. 25: „R18–R32 nach E-2; die drei Voraussetzungen (R25, R26, R28) misst die Sitzung vor dem Eintrag“.
- 29b R39 (Z. 208): Feldliste „im Registerauftrag E-2 … gemessen eingetragen“. R51 (Z. 263): Marken sind „Handwerk im
  Registerauftrag; der alte Satz bleibt zeichengleich“, für 10 und den Datenstand-Hash Indexzeilen.
- 30a Z. 2: „Registertext nur als R-Block ab R53“; Kopfzeilen „zeichengleich kopierbar, nummeriert“.
- Zur Abschnittsnummer (47) und zur Reihenfolge: **nichts**. Keine Aussage, ob ein Abschnitt oder drei.

**Erschlossen:**
- Register endet mit `## 46.` (REG Z. 10082; letzte Unterüberschrift 46.11 Z. 10268); nächste freie Nummer 47 —
  nach der Regel 24/1 vor Vergabe neu messen.
- Vorbild 46.0 (Z. 10084–10124): ein Abschnitt je Fable-Antwort, Blöcke in der Reihenfolge des Codeblocks als
  46.1 ff., Blockzitat, `diff` je Baustein, darunter „Kette“ mit Marke; Nummer vergibt der steuernde Chat. Gegenbeispiele:
  41–43 bündeln je drei bzw. zwei Antworten in einem Abschnitt. Also beides belegt: 47 (27c) / 48 (29b) / 49 (30a)
  oder ein Abschnitt 47 mit 38 Einträgen **[PLATZHALTER: Entscheid steuernder Chat]**.
- Reihenfolge-Zwänge aus den Blöcken: R54 berichtigt R48 (g), R55 ergänzt R48 (c), R52 (b) verweist auf R33, R34/R35
  auf R37/R39/R41 — numerische Reihenfolge R18 → R55 erfüllt alle Rückverweise. Die Tatsachennotizen TB-122/TB-124
  gehören hinter R49 (h) (sie überholen dessen „11.3 offen“) und hinter R53 (TB-124 beruft sich auf R53).

### (b) R53-Zählweise: wörtlich L + 20 gegen hergeleitet L + 19

- **Wortlaut R53** (30a Z. 25): „je Rückblick-Achse die oberste registrierte Stufe (Abschnitt 3) zuzüglich der festen
  Fenster des Bots (etwa Bollinger-Fenster, Donchian-Zusatz)“ ⇒ wörtlich L + 20 (Bollinger 20).
- **Herleitung, Beleg vorhanden [belegt]:** `docs/belege/TB-124/b1_herleitung.txt` (11 Z.): für beide Breakout-Bots
  und je Stufe von `bb_lookback` plus Voreinstellung: `bb_width` ab Index 19, `squeeze_thresh` ab 19 + L − 1, erster
  Einstiegsindex = `BB_PERIOD + L − 1` = L + 19, Spalte „woertlich L+BB_PERIOD“ je um 1 höher; alle zehn Zeilen „gleich“
  (keine „ABWEICHUNG“). Skript `b1_herleitung.py` (29 Z., synthetische Reihe, Stufen aus `registerdaten.raster()`).
  Text: TB-124 Z. 107–129 (Herleitung, Tabelle), Z. 325–332 (Befund für E-2); Nachtrag 1
  `docs/auftraege/NACHTRAG_1_MAC_TB-124_scanbeginn_vorlauf.md` Z. 13–17; UEB Z. 198 (20:20), BL Z. 215.
- Grund der Differenz (TB-124 Z. 329–330): zwei hintereinanderliegende rollende Fenster (Bollinger 20 über `close`,
  Squeeze L über `bb_width`) teilen sich einen Balken; `rolling` ohne `min_periods`.
- Einordnung UEB Z. 198: „Frage der Zählweise, keine Fable-Frage, solange die Herleitung aus dem Code trägt“; 30a Z. 18:
  „R53 nennt die Regel, nicht die Werte — die Sitzung rechnet sie aus registerdaten.py“.
- *[erschlossen]* Das alte Faltenplan-Feld `vorlauf_balken` war der Scanbeginn-Index (127 = `WARMUP_PERIOD + 1`,
  TB-122 Z. 221–224) — dieselbe Index-Konvention wie L + 19.
- *[erschlossen]* Der TB-124-Entwurf (Z. 320–323, „Scanbeginn … an ihrem Vorlauf … `BB_PERIOD + L − 1`“) setzt die
  hergeleitete Lesart voraus; Eintrag des Entwurfs und Entscheid zur Zählweise müssen zusammenpassen.
- **Lücke:** Herleitung nur für die zwei Breakout-Bots. Der Vorlauf ist bei sechs Bots achsenabhängig (VM Z. 50);
  für die übrigen vier (u. a. `rsi2_*`, `turtle_soup_*`, Donchian-Zusatz) gibt es keinen Herleitungsbeleg
  **[PLATZHALTER]**.

### (c) Tatsachennotizen TB-122 und TB-124

| | Fundstelle | Länge | Zustand |
|---|---|---|---|
| TB-122 | `docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md` Abschnitt 6, Überschrift Z. 230, Entwurf Z. 235–275 | 41 Z., 3 116 B, ~360 Wörter, als Blockzitat `> ` | fast fertig; zuzuschneiden (s. u.) |
| TB-124 | `docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md` Abschnitt 6, Überschrift Z. 284, Entwurf Z. 289–323 | 35 Z., 2 696 B, ~360 Wörter, Blockzitat | fast fertig; zuzuschneiden |
| dazu R28 | TB-124 Abschnitt 5 Z. 273–282 „Satz zu R28 für E-2“ | 10 Z., 820 B, Aufzählung | Stoff, kein fertiger Wortlaut |
| dazu R53 | TB-124 Abschnitt 7 Z. 325–332 | 8 Z. | Befund, kein Wortlaut |

Beide Entwürfe haben die Bauart von 46.11 (Gemessen in …, Grund, Hash-Übergänge nach 37.3 als Tabelle, `register()`,
Nachweis, Stand 11.3). Zuschnitt **[erschlossen]**:
1. Zeilen „ENTWURF — nicht im Register …“ (TB-122 Z. 232–233, TB-124 Z. 286–287) entfallen.
2. TB-122 „Stand 11.3: … offen der Scanbeginn“ (Z. 274–275) ist durch TB-124 („geschlossen“, Z. 320–323) überholt —
   als datierter Stand belassen oder zusammenführen; ebenso R49 (h) „11.3 offen“.
3. TB-122 erwähnt den C3-Befund `test_sync_check` 30/3 (TB-122 Z. 18–28, durch TB-124 A behoben) nicht.
4. Verweise „R47 (Fable 29b, F-17)“, „R49 (h)“, „27c R31 (b)“, „Fable 30a R53“ müssen auf die vergebenen
   Registerstellen passen.
5. Keiner der Entwürfe nennt eine Marke; *[erschlossen]* Ort wäre 11.3 (REG Z. 1143).
6. Abnahmebefunde TB-124 (UEB Z. 364–369) berühren keinen Satz des Entwurfs (keine DB-Zahl darin); Befund 5
   (zwei `research/`-Scan-Schleifen) betrifft nicht den Signalpfad.

### (d) Blöcke, die nicht ins Register gehören

**Kein R-Block** wird von Fable als Regelwerk, BACKLOG oder „kein Registertext“ bezeichnet **[belegt, alle 38 gelesen]**.
Handwerk-/Regelanteile **innerhalb** von Blöcken (bleiben im Wortlaut, Folgearbeit gehört woandershin):
R31 (b) „Regel: Eine Freigabe je Sperrlistendatei nennt deren Tests ausdrücklich mit“ (Regelwerk; 27c Z. 113 „an den
steuernden Chat“) · R43 „Posten 5 des Plans ist neu zu fassen (Handwerk)“ · R49 (e) „Künftig nennen Marken
Bezeichner“ · R51 ganz „Handwerk im Registerauftrag“ · R53 „TB-122 F1, Handwerk“ (erledigt in TB-124) und R53 (a)
(BL Z. 213) · R55 „Prüfung … wird ergänzt (Handwerk)“ (BL Z. 217).
Von Fable ausdrücklich als Nicht-Registertext bezeichnet, aber **ausserhalb** der R-Blöcke: 29b B1–B9 („Handwerk;
kein Registertext“), D2 K2h/K2f („Handwerk (Regelwerk); kein Registertext“, PRUEFPRINZIPIEN), 27.4 für Aufträge, F-16
(„Kein eigener Registertext; R4 deckt es“), W44 Indexzeile, Teil 3 Nr. 2 (kalter Leser, ARBEITSWEISE), Teil 0 Nr. 4
(Gegenleser gegen die Quelle); 27c Z. 111 T117-7, §4-Tabelle. Laut UEB Z. 229 nicht in TB-125: K2h/K2f, Trägerstellen,
kalter Leser, 29a 1–3, `project_info`-Regel.

### BACKLOG: 5b-Block zu 27c, 29a, 29b?

**Nein [belegt].** `BACKLOG.md` (230 Z., md5 `75f4577f…`) hat genau einen Fable-Folgeblock:
`### Aus Fable 30a (30.09.2026) — Folgen von R53–R55, vor bzw. mit E-2` (Z. 211–217; eingefügt von TB-124, 8/0).
Zu 27c/29b/29a nur Erwähnungen (K4t Z. 194 nennt Fable 29a). Der zwischengelagerte Block „### Aus der Abnahme
TB-124 (30.09.2026)“ (UEB Z. 372) steht noch nicht im BACKLOG; laut UEB Z. 390 kommt er in TB-126 Schritt 0.
Wo die 5b-Bewertung von 27c/29b steht: **[PLATZHALTER: vermutlich UEBERGABE_ARCHIV, nicht im Abzug]**.

## 4. Weitere Befunde (erschlossen)

- **Abschnitt 10 / Marken:** R42 (Punkt 15), R45 (Punkt 10), R48 (k) (10.1), R49 (g) betreffen Abschnitt 10; dort
  steht nach Praxis keine Marke (46.0, 42.3) — R51 sieht für (g) selbst eine Indexzeile vor; für R48 (k) fehlt eine
  solche Aussage.
- **Weitere Tatsachennotizen nach Bauart 34.0** (Messung, die der Text voraussetzt, beim Eintrag mitführen): über die
  Liste hinaus R28, R33, R36, R48 (c)/(d)/(g)/(i), R53, R54.
- **Umzugsblock 22:15, Block 4 Nr. 3 [belegt]:** Inhalt TB-126 = R18–R55 zeichengleich; R53–R55 gegen Ablage (erledigt,
  UEB Z. 391); TN TB-122/TB-124; R53-Zählweise; offene Voraussetzungen; Registerkopie Teil 1–4 neu und Ablage-Abgleich;
  38 Blöcke. Dazu Nachtrag 23:20 (Z. 379, 390): Schritt 0 = Worktrees `tb123_vorher*` entfernen, Nachtrag
  committen, BACKLOG-/Journal-Wortlaut aus 22:40 als eigene Einfügung. REGISTER_INDEX nach dem Eintrag pflegen
  (Z. 133–135).

## 5. Platzhalter

1. Byte-Vergleich 27c/29b Repo gegen Ablage. 2. Fundstelle Betreiberentscheid R24 (a). 3. Ob Fable den vierten
Datenstand-Ort (R28) kennt. 4. Messung der Feldliste aus dem AW-Docstring (R39). 5. Umgang mit R48 (d) beim Eintrag.
6. Marke in Abschnitt 9 (R51). 7. Abschnittsnummer(n) und Gliederung. 8. Vorlauf-Herleitung für die vier übrigen
Bots (R53). 9. Fundstelle der 5b-Bewertung von 27c/29b.

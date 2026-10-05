# Bericht H3 — Fundstellen der Fable-Antwort 04a gegen Register und 02b/02c

Gemessen am 04.10.2026 über `device_bash`, Repo `$HOME/mnt/trading-bot`, HEAD `d781f1b`.
Registerkopien tragen im Kopf Commit `ee43f5f…`, sha256 `9a2cefb7…`; letzter Commit des Registers: `ee43f5f`.
Nur gelesen (grep/awk/sed -n/wc/ls, `git --no-optional-locks ls-files|log|grep|rev-parse`). Kein `git status`, nichts angelegt.

Kürzel: `A<nn>` = `docs/projektfuehrung/register_kopie/REGISTER_KOPIE_ABSCHNITT_<nn>.md`;
`02b` = `docs/projektfuehrung/FABLE_ANTWORT_2026-10-02b_zeitachse_vertrag_benchmarkdatei.md` (155 Z., 23 904 B);
`02c` = `docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md` (157 Z., 30 216 B);
`REG` = `docs/VORREGISTRIERUNG_neuselektion.md` (906 766 B).

Abweichung vom Auftrag (Ort): `REGISTER_INDEX.md` liegt unter `docs/projektfuehrung/REGISTER_INDEX.md` (420 Z., 40 183 B), nicht in `register_kopie/`.

## Ergebnistabelle

| Nr. | Behauptung | Befund | Ort |
|---|---|---|---|
| 1 | 02b R68 (c) „beide kommen aus einer Rechnung (R60 (c))“ | ja, wörtlich (1 Treffer) | 02b:144 |
| 2 | 02b-Leseprotokoll führt 51 und 15 als gelesen | ja / ja | 02b:17 und 02b:16 |
| 3 | 02b „Unsicher“ 1, Satz zum Handelskalender | ja, wörtlich (1 Treffer) | 02b:124 |
| 4 | 02b R68: 2d (15.4 (d)) als Quelle; Voraussetzung „dass 16.6 den Satz … nicht aufhebt“; „Unsicher“ 4 | ja / ja / ja | 02b:145, 02b:144, 02b:128 |
| 5 | 02b R66 (a) „Kurstage des Marktes im Snapshot“ | ja, wörtlich (1 Treffer) | 02b:138 |
| 6 | 02c „falsch gelesen“; Teil 0 Nr. 4 | ja (1 Treffer) | 02c:41 (= Teil 0 Nr. 4) |
| 7 | R60 (c) spricht von zwei Trägern der Exposure; R63 (d) | ja / ja | A51:37 (51.5); A52:9 (52.1) |
| 8 | ERSETZT-Marke unter 2d in 15.4 (d) | ja | A15:136–139 (Satz: A15:131–134) |
| 9 | 25.2 „der 150. Balken“, als Messung TB-72 mit Beleg | ja | A25:81–86 |
| 10 | R62 (a) und R65 (c) berichtigen 25.2 | ja / ja | A51:66 (51.7); A52:38 (52.3); Marke A25:88 |
| 11 | R61 (c) nennt „14“ in R26 und R30; 51.8 | ja / ja | A51:53 (51.6); A51:83 (51.8) |
| 12 | 53.9 letzte Zeile: zehn sinngemässe Verweise | ja | A53:79 |
| 13 | Zählung der Fälle | siehe unten | A45:52, A48:10, A48:188 |
| 14 | R8 (e) | ja | A45:159 (45.8) |
| 15 | Kette unter 48.20 „Marken: keine“ | ja | A48:191 |
| 16 | 13 Marken-Orte aus R77 (a) | alle 13 Orte vorhanden, Zuordnung stimmt | siehe unten |
| 17 | R61 (b), R65 (a), R70 (a); Abschnitt 34 „Marke am alten Ort“ | ja (4×) | A51:53; A52:38; A53:37; A34:17 |
| 18 | Orte ohne Marke: 53.10, 50.2, 9, 10, ERZEUGT-Block in 3 | ja (5×); das Wort „Statusliste“ steht in 53.10 nicht | A53:81; A50:31; A09:3; A10:3; A03:11–211 |
| 19 | Sichtschutz Abschnitt 27 | siehe unten | A27 |
| 20 | `BACKLOG.md` im Repo; „Ein-Pfad-Regel“ darin | Datei ja; Suchwort **0 Vorkommen** | `docs/projektfuehrung/BACKLOG.md` |
| 21 | Zahlenliste in der Eröffnung 04.10. | ja (alle vier) | Eröffnung Z. 39–42; Sperre Z. 47 |

## Ausschnitte je Nummer

### 1
02b:144 (Zeile beginnt mit „R68 — Präzisierung zu R37 (48.5) und zu R64 (52.2) (Zeile der Bestätigungsperiode in zellen.csv).“):
> „… Mittel über die Benchmark-Tage des Bots innerhalb der Tage nach (a). (c) Was nach der Attribution je Position (R37) in die Rendite der Zeile nicht eingeht, geht auch in ihre Exposure nicht ein; beide kommen aus einer Rechnung (R60 (c)). (d) Die mittlere Exposure der Zeile ist Bericht; kein Urteil liest sie. [Vorau…“

Im Satz davor stehen „die Rendite der Zeile“ und „ihre Exposure“.

### 2
02b:9 „**Vollständig gelesen** (Ablage, `project_read`; Registerdateien je mit Kopf Commit `ad351d5`, sha256 `a7496780…`, KOPIE):“
02b:16 „| Abschnitte 15, 23, 24, 29, 48 | 25,9 / 29,2 / 25,5 / 4,7 / 28,7 KB (nach Anfrage) |“
02b:17 „| Abschnitte 7, 51, 49, 4 | 3,7 / 22,4 / 5,1 / 6,0 KB (nach Anfrage) |“
Dazu 02b:27 „**Nicht gelesen:** alle übrigen Registerabschnitte — darunter 16 (16.6, 16.7), 21, 25, 33, 34, 35, 37, 40, 41, 43. …“ (17 steht in keiner der beiden Listen namentlich).
02b:31 „**Kein Helfer, kein Suchlauf** (`project_search` nicht benutzt). …“

### 3
02b:124 „1. **Aktienkalender (R66 (a)).** Ich habe keinen Registersatz gelesen, der den Handelskalender der Aktien-Tagesreihe festlegt. Der Block nennt „Kurstage im Snapshot“ als Voraussetzung. Lässt sich das nicht eindeutig bestimmen, kommt es zurück.“

### 4
02b:145 „Quelle des Grundes: R37 („Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle“), R33 (genau eine Zeile je Zelle und Falte, Bestätigungsperiode eingeschlossen), 2d (15.4 (d)), R60 (c), R64 (a). Kein Ergebnis.“
02b:144 „[Voraussetzung, zu messen: dass 16.6 den Satz „Tage im Embargo gehören zu keiner Periode“ aus 2d (15.4 (d)) nicht aufhebt; dass kein Urteil in auswertung.py die mittlere Exposure der Bestätigungspe…“
02b:128 „4. **16.6 nicht gelesen.** R68 stützt sich auf R37 im Wortlaut und auf 2d in der Fassung 15.4 („Tage im Embargo gehören zu keiner Periode“). Ob 16.6 diesen Satz hält, steht als Voraussetzung im Block.“

### 5
02b:138 „… bis zum Ende der Bestätigungsperiode (35.1), ohne Lücke. Handelstage sind bei Krypto die Kalendertage (15.4, Anmerkung 1), bei Aktien die Kurstage des Marktes im Snapshot. Ein Tag, an dem die Zelle keine Position hält, steht mit Rendite 0 und Exposure 0 in der Reihe (1a) …“
Im selben Block: „[Voraussetzung, zu messen: dass sich die Kurstage des Aktienmarktes aus dem Snapshot eindeutig bestimmen lassen, als die Tage, an denen mindestens ein Symbol der Universumsdatei des Bots (3a) einen Kurs trägt, und dass jeder Benchmark-Tag …“

### 6
02c:41 (unter „## Teil 0. Kenntnis“, 02c:36): „4. Zitate: Alle genannten Stellen sind in den neuen Fassungen berichtigt. Die zwei, die nicht treffen, sind meine Fehler: Ich habe in R68 eine ersetzte Fassung (2d aus 15.4) als Quelle des Grundes geführt, obwohl die Marke darunter in dem stand, was ich gelesen hatte, und ich habe „beide Träger“ in R60 (c) falsch gelesen. Ob das Fälle der Klasse „Bestand behauptet“ sind, zählt der steuernde Chat.“ (412 Zeichen, in zwei Stücken gemessen)

### 7
A51:35 „### 51.5 R60 — Bestätigung und Ergänzung zu R48 (d) (48.16) (mittlere Exposure: Registertext und Code; zwei Träger)“
A51:37 „(c) Der Zellen-Erzeuger schreibt beide Träger aus einer Rechnung: mittlere_exposure in zellen.csv ist je (Zelle, Falte) das Mittel der Spalte exposure der Tagesreihe dieser Zelle über die Tage der Falte. Die Abnahme nach …“ (REG: 1 Treffer für „Der Zellen-Erzeuger schreibt beide Träger aus einer Rechnung“)
A52:9 (52.1, R63) „(d) Der Zellen-Erzeuger bezieht weder Positionen noch Exposure aus bot_lauf.py oder dessen Ausgabe; die Positionen kommen aus simuliere_portfolio (R45), die Spalte exposure aus derselben Rechnung wie die MtM-Reihe (R60 (c)).“ (REG: 1 Treffer)

### 8
A15:131–134 „> **(d)** Die Bestätigungsperiode beginnt am Go-Live-Tag plus Embargo; Embargo = / längste Zeitbremse des Bots in Handelstagen plus 1 (Bots ohne Zeitbremse: 95. / Perzentil der Haltedauer plus 1). **Tage im Embargo gehören zu keiner / Periode.**“ (Satz über zwei Zeilen umbrochen)
A15:136–139 „> ⚠️ **ERSETZT durch Abschnitt 16 (Registernachtrag TB-41, 16.09.2026), 16.6.** Das Embargo ist dort keine feste Frist mehr, sondern eine Bedingung am Positionsbestand mit dieser Frist als Deckel. Die Embargo-Tabelle unten gilt als **obere Schranke** weiter.“ (REG: 1 Treffer für die Markenzeile)

### 9
A25:62 „### 25.2 Die Instanz — `t3_supertrend` beginnt 2019“
A25:81–86 „⭐ **`rsi2_crypto` bleibt 2019**, an der Konjunktion nachgemessen (`docs/belege/TB-72/schritt2_rsi2_crypto_bedingung_i.txt`): (ii) ist 2018 erfüllt (`H = 2`, BTC/ETH ab 2018-12-30), **(i) nicht** — 150 Tagesbalken Vorlauf am 1. Januar 2018 brauchen Daten ab August 2017, BTC/ETH beginnen am 17.08.2017 und haben bis zum 31.12.2017 **137** Balken; der 150. Balken liegt am **2018-01-14**. Fables Nachrechnung trifft.“
A25:3 Überschrift des Abschnitts: „25. Berichtigung zu Registertext 4a und zu 21.3 (b) …“; A25:20 „Die Messung in Schritt 1 von TB-72“.

### 10
A51:66 (51.7, R62) „(a) 25.2: „der 150. Balken liegt am 2018-01-14“ ist um einen Balken ungenau. Bei Daten ab 2017-08-17 und 137 Balken bis 2017-12-31 ist der 150. Balken der 2018-01-13; der 2018-01-14 ist der Balken mit 150 Balken davor. „Warm ab 2018-01-14“ (32.2) bleibt richtig; die Zählweise steht in R57.“
A52:38 (52.3, R65) „(c) Berichtigung zu 25.2: „der 150. Balken liegt am 2018-01-14“ lies „der Balken mit 150 Balken davor liegt am 2018-01-14; der 150. Balken ist der 2018-01-13“. Das Ergebnis von 25.2 (Bedingung (i) ist am 1. Januar 2018 nicht erfüllt) bleibt unberührt, ebenso „warm ab 2018-01-14“ (32.2 …“
A25:88 „> ⭐ **25.2 BERICHTIGT durch R62 (51.7) und R65 (52.3)** (Fable 01a R62, Unterpunkt (a), und Fable 02a R65, Unterpunkt (c), TB-130, 02.10.2026).“

### 11
A51:53 (51.6, R61) „(c) Berichtigung: In R26 (47.9) und R30 (47.13) lies „14“ als „Sperrlistenpunkt 14 (Abschnitt 10)“; Abschnitt 14 des Registers ist der Nulltest S-E1 und nicht gemeint. [Voraussetzung, zu messen: der Wortlaut von Sperrlistenpunkt 14; hier nach REG…“
A51:83 (51.8) „| R61 (51.6) (c) | der Wortlaut von Sperrlistenpunkt 14 | Abschnitt 10, Punkt 14: „Die Reihenfolge Selektion → Bestätigungsperiode → Bericht — im Kopftext von `auswertung.py` als Ablauf festgeschrieben“. Abschnitt 14 heisst „Der Nulltest S-E1“. R26 (47.9) schreibt „(12: keine Option, die einen Bot ausnimmt; 14: Selektion → Bestätigungsperiode → Bericht für alle neun)“; R30 (47.13) heisst „Ergänzung zu 14 und zu den Tag-Vorbedingungen“ | trifft: gem…“ (482 Zeichen, in zwei Stücken gemessen)

### 12
A53:79 „| R66–R73, Zitate und Verweise | — | 98 Stellen gegen den Wortlaut gemessen (`docs/belege/TB-132/vormessung/v4_register_02c.md`). Sinngemäss treffen zehn: R72 (b) fasst den Benchmark-Tag enger als der Wortlaut von 23.3 (REG Z. 3933–3936), das ist der Inhalt der Präzisierung; R72 nennt im Kop…“
Zeilenende: „… | keine Stelle trifft nicht; die sinngemässen gehen zur Kenntnis an Fable (53.10 Nr. 9) |“
A53:93 „| 9 | Die sinngemässen Verweise aus 53.9 (letzte Zeile) | nächste Anfrage an Fable, zur Kenntnis |“

### 13 — Zählung „Bestand behauptet statt Voraussetzung genannt“
Volle Wendung in den Abschnittskopien: 3 Zeilen (A45: 1, A48: 2); REG-Gegenprobe: 3 Zeilen (Z. 10205, 10792, 10970).

| Ort | Fallnummer | Ausschnitt |
|---|---|---|
| A45:52 (45.1, R1) | neunter | „Fables Beispiel `lambda: False` in 25e 3 war ungemessen — neunter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt".“ |
| A48:188 (48.20, R52 (a)) | zehnter | „(a) 27b B3 („die datierten Kopien … sind im Repo committet“) war für vier von sechs Registerkopien falsch (TB-118 A3); zehnter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt“.“ |
| A48:10 (48.1, R33, Quelle des Grundes) | elfter | „Der Vertrag stand vor R5 (b); R5 (b) war Kurzform ohne Nachlesen — elfter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt“. Kein Ergebnis.“ |
| A48:188 (48.20, R52 (b)) | elfter | „(b) 45.5 (b) („für jede Zelle genau eine Zeile“) widersprach dem Datenvertrag; berichtigt in R33; elfter Fall.“ |
| A41:248 | achter | „… über `strategy_paths.get_strategy_paths()`)" — Fables achter Fall. ⭐“ |
| A41:402 | siebter | „Eine Auftragsnummer, nicht gemessen — dieselbe Klasse wie TB-94/TB-96 in 24a. **Angenommen; siebter Fall.**“ |
| A40:375 | vierter | „⚠️ **Ein vierter Fall derselben Klasse ist in 40.6 vorgelegt, nicht“ |
| A40:360 / 363 | (Klasse) | „> Alle drei sind dieselbe Klasse wie die sechs Rücknahmen der ersten Woche: eine Tatsache über den Bestand behauptet statt als Voraussetzung genannt. Ich zähle sie mit.“ |

- „zwölfter Fall“: 0 Treffer in allen Abschnittskopien und im Register.
- R52 (A48:188, 548 Zeichen): Kopf „R52 — Tatsachennotizen 29b.“, Unterpunkte (a) zehnter Fall, (b) elfter Fall, (c) Verdichtung des Chats zwischen 29a und 29b. Wörter „gezählt“, „Zählung“, „Massstab“ in R52: 0 Treffer. A48:189 „Quelle des Grundes: Messungen TB-118, TB-120; Leseprotokoll 29b. Kein Ergebnis.“
- `REGISTER_INDEX.md`: 0 Treffer für „Bestand behauptet“, „ter Fall“, „Fall der Klasse“, „Zählung“. „R52“/„48.20“ je 1 Treffer (Z. 202: „| 48 aus 29b | 4 | R33–R52 (48.1–48.20); R51 = Marken für Register 0–12 | …“); „45.1“ Z. 197 und 199 (Marke an 43.3; R1–R8).

### 14
A45:159 (45.8, „R8 — Tatsachennotizen 26a“): „> (e) Berichtigung zu 25f A2 und C3 Entscheidung 8: Das Zellenbudget steht in 16.4 (g)–(m); offen ist nur der Vollzug im Code (16.11, Zeile 3; Stufe IV). Fables Satz „keinen Abschnitt gefunden" war aus dem Gedächtnis; Fables Regel: Vor „steht nicht im Register" wird im Text gesucht, nicht erinnert, und das Suchwort genann…“ (325 Zeichen)

### 15
A48:186 „### 48.20 R52 — Tatsachennotizen 29b“; A48:191 „**Kette:** Marken: keine.“ (REG: 6 Treffer für diese Kettenzeile, u. a. auch A51:69 unter 51.7 R62 „**Kette:** Marken: keine. Voraussetzung gemessen: 51.8.“)

### 16 — die 13 Marken-Orte aus R77 (a)

| Ort (R77 (a)) | vorhanden | Überschrift / Zeile | Marken, die der Ort heute trägt |
|---|---|---|---|
| 53.1 (R66) | ja | A53:7 „### 53.1 R66 — Präzisierung zu Registertext 1a und 1c …“ | keine (A53 enthält 0 ⭐-Zeilen) |
| 17.5 | ja | A17:252 „### 17.5 Registertext 5f — die registrierte Umgebung *(neu)*“ | keine „… durch“-Marke (A17: 0 Markenzeilen); A17:260 „> ⭐ **Tatsachennotiz:** Der Handelskalender kommt **nicht aus einer Datei**,“ |
| 53.9, Zeile „R66 (53.1) (b)“ | ja | A53:69 „| R66 (53.1) (b) | welchen Kalender des Pakets der Code des Laufs benutzt (TB-47, Feld `kalender`) | …“ | keine |
| 16.6 | ja | A16:483 „### 16.6 Registertext 2d — Embargo *(ersetzt die Fassung aus 15.4 vollständig)*“ | A16:530 „> ⭐ **16.6 PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, 01.10.2026).“; dazu A16:518 „> ⭐⭐ **Zwei Präzisierungen zu 2d und eine Rücknahme (41.3 C1–C3, Fable 24d,“ |
| 48.5 (R37) | ja | A48:38 „### 48.5 R37 — Präzisierung zu 16.6, 35.1, 16.4 (c)/(d), 5.1 Nr. 7 …“ | A48:43 „> ⭐ **48.5 R37 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026).“ |
| 53.3 (R68) | ja | A53:21 „### 53.3 R68 — Präzisierung zu R33 (48.1), zu R37 (48.5) und zu R64 (52.2) …“ | keine |
| 48.4 (R36) | ja | A48:31 „### 48.4 R36 — Präzisierung zu 24.2 und 45.5 (zwei Drawdown-Spalten; …)“ | keine |
| 51.5 (R60) | ja | A51:35 „### 51.5 R60 — Bestätigung und Ergänzung zu R48 (d) (48.16) …“ | A51:40 „51.5 R60 (a) PRÄZISIERT durch R63 (52.1)“; A51:43 „51.5 R60 (b) und (c) PRÄZISIERT durch R64 (52.2)“; A51:46 „51.5 R60 PRÄZISIERT durch R69 (53.4)“ |
| 52.2 (R64) | ja | A52:14 „### 52.2 R64 — Präzisierung zu R48 (d) (48.16) und zu R60 (b) und (c) (51.5) …“ | A52:19 „ERGÄNZT durch R66 (53.1)“; :22 „PRÄZISIERT durch R68 (53.3)“; :25 „PRÄZISIERT durch R69 (53.4)“; :28 „PRÄZISIERT durch R71 (53.6): erster Kurstag“; :31 „PRÄZISIERT durch R72 (53.7): Benchmark-Tag“ |
| 48.7 (R39) | ja | A48:55 „### 48.7 R39 — Ergänzung zu 46.3 (R12) und Berichtigung des Datenvertrags …“ | A48:60 „48.7 R39 ERGÄNZT durch R67 (53.2)“; A48:63 „48.7 R39 ERGÄNZT durch R69 (53.4): R39 ist bestätigt“ |
| 48.2 (R34) | ja | A48:17 „### 48.2 R34 — Ergänzung zu 22.2 und 45.5 (Zellenbericht)“ | keine |
| 53.4 (R69) | ja | A53:28 „### 53.4 R69 — Auflösung des Widerspruchs zwischen R39 (48.7) und auswertung.py …“ | keine |
| 53.5 (R70) | ja | A53:35 „### 53.5 R70 — Marken zu R64 (7 (c)) und zu R66 bis R73; Präzisierung zu R61 (b) (51.6) und R65 (a) (52.3)“ | keine |

Zuordnung Unterabschnitt ↔ R-Block stimmt an allen Orten, die R77 (a) mit R-Nummer nennt (10 von 10). 17.5, 16.6 und die Zeile in 53.9 nennt R77 (a) ohne R-Nummer.
Dazu: A53:12 (Kette unter 53.1) „… Indexzeilen ohne Marke (R70 (b)): 17.5; 50.7 Nr. 3. …“

### 17
A51:53 R61 „(b) Eine Marke steht dort, wo ein Block dem Wortlaut eines Ortes eine Bedeutung gibt oder ihm etwas hinzufügt (34). Keine Marke erhält ein Ort, der nur Quelle des Grundes, Statusliste, Plan oder Code ist, der im erzeugten Block liegt oder in Abschnitt 10. Danach sind nachzutragen, der alte Satz b…“
A52:38 R65 „(a) Die Aufzählungen in R51 und R61 (b) wenden die Regel aus 34 an und schliessen sie nicht ab. Gibt ein Block einem benannten Ort ein „lies“, eine Ergänzung oder eine Bestätigung, trägt der Ort die Marke, auch wenn die Aufzählung des Blocks ihn nicht nennt; ausgenommen bleiben die Orte na…“; weiter: „Eine Tabelle von Befunden ist keine Statusliste im Sinn von R61 (b), soweit ein Block den Befund einer Zeile ergänzt oder berichtigt. Eine Bestätigung trägt das Markenwort ERGÄNZT mit dem …“
A53:37 R70 „(a) 7 (c) trägt keine Marke zu R64. Abschnitt 7 nennt seine Tage selbst („gemeinsame Tage“, „über dieselben Tage“); R64 gibt das „lies“ R48 (d) und R60 (c), nennt 7 (c) als Geltungsbereich und bestätigt in (b) den Code, nicht den Wortlaut von 7. Ein Ort, den ein Block nur als Geltungs…“; weiter: „… bleibt ohne Marke und wird vom Index geführt, wie R54 an 7 (c) (R61 (b)). Nennt der Wortlaut eines Ortes die Sache nicht und gibt der Block sie ihm, trägt der Ort die Marke: so 4.2 zu R64, 15.3 (a) zu R66 und 48.1 zu R68.“
A53:37 R70 „(b) Indexzeilen ohne Marke: 7 (c) — mittlere Exposure des Gewinners, Tage nach R64 (a), (b) und (d). 17.5 — Handelskalender der Aktien-Tagesreihe, R66 (a) und (b). 50.7 Nr. 3 — Tagesbasis des DSR, R66 (f).“
A34:17–20 „⭐⭐ **Neu in diesem Abschnitt — die Marke steht AM ALTEN ORT.** Jeder der sechs Einträge ist an zwei Stellen sichtbar: hier mit vollem Text, Herkunft und Grund, und **direkt unter dem berichtigten Satz** als eingerückter Hinweisblock mit Verweis auf 34.x. Der alte Satz bleibt zeichengleich; d…“ (Wendung „Marke am alten Ort“ ferner A34:51, 79, 94, 121, 147, 193, 210)

### 18
- 53.10: ja — A53:81 „### 53.10 Was offen bleibt“, Tabelle mit Kopf „| | offen | wann, wo |“, 10 Zeilen. Das Wort „Statusliste“ steht in 53.10 nicht (Treffer nur in A51:53, A52:38, A53:38).
- 50.2: ja — A50:31 „### 50.2 R39 (48.7) — Feldliste der Ausgaben, gemessen aus dem Docstring von `auswertung.py`“; keine Markenzeile in A50:31–71.
- Abschnitt 9: ja — A09:3 „## 9. Die DSR-Buchführung“ (42 Z.).
- Abschnitt 10: ja — A10:3 „## 10. Die Sperrliste“ (209 Z.), A10:184 „### 10.1 Die Amendment-Regel“.
- ERZEUGT-Block in Abschnitt 3: ja — A03:11 „<!-- ERZEUGT: registerbericht.py -- nicht von Hand aendern -->“ bis A03:211 „<!-- ENDE ERZEUGT -->“.
- Zusätzlich (R77 (c) nennt sie): A29:43 „### 29.3 Der Registertext, zeichengleich“; A41:308 „### 41.3 Aus Fable 24d (…)“; A35:25 „### 35.1 Ergänzung zu 33.2 — die Bestätigungsperiode und ihr Bezeichner“; 27.2 siehe Nr. 19.

### 19 — Abschnitt 27 (A27, 82 Z., 6 507 B)
Überschriften: A27:3 „## 27. Sichtschutz des Verfahrensprüfers (Fable 21g, 21.09.2026)“; A27:16 „### 27.1 bis 27.5 — der Registertext, zeichengleich“; A27:36 „### 27.6 Wo der Nullpunkt liegt“; A27:50 „### 27.7 Ein Verstoss beim Melden des Verstosses — festgehalten, nicht geglättet“; A27:61 „### 27.8 Was hier ausdrücklich NICHT getan wird“. 27.1–27.5 haben keine eigenen Überschriften, sie stehen als Zitatblock.

- A27:20 „> **27.1** Der Verfahrensprüfer erhält vor dem signierten Tag keine Ergebnisgrössen des Selektionsraums: keine Kennzahl eines Parametersatzes (Sharpe, Rendite, Drawdown, Trefferquote, Anzahl Trades), keine Aussage, welche oder wie viele Sätze eine Bedingung erfüllen, keine Rangfolge, keine Plateau-Lage — **und keine Erwartung, Schätzung oder Prognose über den Ausgang des Laufs**, gleich ob als Zahl oder als …“ (416 Zeichen)
- A27:22 „> **27.2** Zulässig sind Verfahrensmessungen — Kalender, Datenbestand, Faltenzahl, Handelbarkeit, Benchmark-Seite — und Wirkungen einer Regel auf die registrierten heutigen Parameter, wenn die Regel vor der Messung geschrieben stand (Bauart 24.3).“
- A27:24 „> **27.3** Das Register darf der Verfahrensprüfer vollständig lesen; was darin steht, hat dieses Tor bereits passiert (gemessen 21.09.: keine Kennzahl je Parametersatz im Registertext). Eine Ablage-Kopie trägt Commit-Hash, Datum und die Kennzeichnung KOPIE.“
- A27:26 „> **27.4** Der Verfahrensprüfer führt in jeder Antwort ein Leseprotokoll (welche Dateien er in diesem Chat gelesen hat). Das Protokoll ist Selbstauskunft. Die Prüfung, ob seine Begründungen Grössen nach 27.1 enthalten, ist Pflicht des steuernden Chats (Prüfprinzipien).“
- A27:28 „> **27.5** Wer dem Verfahrensprüfer einen Treffer nach 27.1 in einer Datei meldet, nennt Datei und Fundstelle, nicht den Inhalt.“
- A27:30–31 „> **Tatsachennotiz zu 27 — Anfangsbestand des Verfahrensprüfers beim Inkrafttreten (21.09.2026):** Der Chat des Verfahrensprüfers wurde am 21.09. neu begonnen; er kennt aus dem Vorgängerchat nichts. …“

Abweichung zur Auftragsbeschreibung: 27.3 regelt nach Wortlaut das Lesen des Registers und die Kennzeichnung der Kopie; einen Satz „was bei Kenntnis einer gesperrten Grösse gilt“ trägt 27.3 nicht.

`BACKLOG` in A27: 4 Treffer, keiner in 27.1–27.5 selbst:
- A27:14 „… Parametersatz), `BACKLOG.md` ist es nicht (Z. 190 `W14`, Z. 170 `T39.2`).“ (Vorsatz A27:12: „das Register ist rein“)
- A27:31 „… am 21.09. durch eine Treffermeldung mitgeteilt: der Wortlaut der Erwartung in `BACKLOG.md` Zeile 190 (W14) über die Zahl der Bots auf Schatten — eine Erwartung nach 27.1, keine Messung; …“
- A27:53 „zitiert (`BACKLOG.md` Z. 190 wörtlich) statt seiner Fundstelle.“
- A27:66 „| ⛔ | **`BACKLOG.md` bereinigen oder verschieben.** 27.1 verlangt es nicht; die Regel liegt beim Leser, nicht bei der Datei | — |“

„Suche“ / „project_search“ / „Ausschnitt“ in A27: 0 Treffer. `project_search` in allen 54 Abschnittskopien: 0 Treffer.

Spätere Blöcke zu 27 (Index Z. 181, 278, 279, 324, 379; Marken in A27):
- A27:33 „> ⭐ **27.3 ERGÄNZT durch R31 (47.14)** (Fable 27c R31, Unterpunkt (d), TB-126, 01.10.2026).“
- A27:69 „> ⭐ **Messungen auf dem Selektionsraum nach dem Tag: siehe 45.6/45.7** (Fable“ — A45:123 „### 45.6 R6 — Ergänzung zu 27 (Messungen auf dem Selektionsraum nach dem Tag)“
- A27:72 „> ⭐ **Abschnitt 27 ERGÄNZT durch R32 (47.15)**“ — A47:116 „### 47.15 R32 — Tatsachennotiz zu 27 — Anfangsbestand des Verfahrensprüfers beim dritten Umzug (29.09.2026)“
- A27:75 „> ⭐ **Abschnitt 27 ERGÄNZT durch R56 (51.1)** (Fable 01a R56, zu 27.4 und 27.6, TB-129, 02.10.2026).“
- A27:78 „> ⭐ **Abschnitt 27 ERGÄNZT durch R73 (53.8)** (Fable 02c R73, TB-132, 04.10.2026).“
- Index Z. 181: „| 27 Sichtschutz | 2 | 27.1–27.5 | 45.6 R6 Ergänzung zu 27 (T4); 27.3: Z. 5169 ERGÄNZT durch R31 (47.14); Z. 5208 ERGÄNZT durch R32 (47.15) (T4); Z. 5211 ERGÄNZT durch R56 (51.1) (T4); Z. 52… ERGÄNZT durch R73 (53.8) (T4) |“

R56 (A51:9, 51.1 „R56 — Ergänzung zu 27.4 und 27.6 (Anfangsbestand eines neu begonnenen Chats des Verfahrensprüfers)“):
- „(a) Der Anfangsbestand eines neu begonnenen Chats wird festgehalten durch den Wortlaut seines Eröffnungstextes und durch das Leseprotokoll seiner ersten Antwort; ein eigener Registerblock je Chat ist dafür nicht nötig.“
- „(b) Bedingungen: Der Eröffnungstext liegt mit Commit im Repo, bevor die Antwort eingetragen wird. Das Leseprotokoll der ersten Antwort nennt, was der Chat vollständig gelesen hat, was nur als Ausschnitt, was nicht, was die Plattform ohne sein Zutun geladen hat (Projekt-Erinnerung, Dateiliste), die Grössen, die an 27.1 grenzen, und schliesst mit dem Satz, dass er weitere Grössen nach 27.1 nicht kennt. Die Antwortdatei liegt mit Commit im Repo; trägt sie Registertext, nennt der Kopf des Abschnitts Datei, md5 …“
- „(c) Ein eigener Block nach der Bauart von R32 bleibt nötig, wenn ein Chat mehr weiss, als Eröffnungstext und Leseprotokoll nennen: nach einer Verdichtung, bei Wissen aus einem Vorgängerchat, nach einer Treffermeldung mit Inhalt (27.7).“
- „(d) Die Projekt-Erinnerung der Plattform ist ein Träger zwischen Chats. Der Verfahrensprüfer liest aus ihr nur Dateien, die der steuernde Chat auf Grössen nach 27.1 gemessen und im Eröffnungstext genannt hat; alle anderen stehen unter derselben Sperre wie BACKLOG.md.“

Weitere Fundstellen zum Thema Suchausschnitt (Abschnittskopien):
- A47:118 (47.15, R32) „… die Dateiliste der Ablage (43 Dokumente); als Suchausschnitt gesehen, nicht geöffnet: `BACKLOG_ENTSCHEIDUNGEN.md` (Einträge F2, Q1, E2) und `FABLE_UEBERGABE_2026-09-24_neuer_chat.md` (Abschnitt 2). D…“ und „`BACKLOG.md`, `BACKLOG_ENTSCHEIDUNGEN.md`, `FABLE_ANTWORT_2026-09-25f_…`, `docs/belege/`, `ergebnisse/` und Trade-Listen: nicht gelesen.“
- A51:66 (R62) „… Er hat keinen Helfer und keinen Suchlauf benutzt.“; A53:58 (R73) „… Er hat keinen Helfer und keinen Suchlauf benutzt. Weitere Grössen nach 27.1, als die Leseprotokolle von 02b und 02c nennen, kennt er nicht.“
- „BACKLOG“ + „Sperre“/„gesperrt“ im selben Satz: nur A51:9 (R56 (d)).

### 20 — `BACKLOG.md`
- `docs/projektfuehrung/BACKLOG.md`: vorhanden, 297 Zeilen, 69 113 B, im Index von git geführt, letzter Commit `12010b2` (2026-10-04 09:10:36 +0200).
- „Ein-Pfad-Regel“: `grep -c` = 0 Zeilen, 0 Vorkommen. Varianten „Ein-Pfad“ (ohne Gross/Klein), „Ein Pfad“, „ein Pfad“, „Einpfad“, „Pfad-Regel“, „Pfadregel“, „ein Rechenweg“: je 0. Es gibt deshalb keinen Treffer, dessen Umgebung sich zeigen liesse.
- Wörter aus Fables Beschreibung des Ausschnitts (nur Zähler und Zeilennummern, kein Inhalt ausgegeben): „Kandidat“ 6 (Z. 49 zweimal, 51, 63, 76, 191), „Leiter“ 2 (Z. 53, 62), „versuch“ (ohne Gross/Klein) 1 (Z. 40).
- Wo das Suchwort im Repo steht (`git grep -c -F`, geführte Dateien): A16:495 (16.6: „> ausdrückliche und seltene Ausnahme von der Ein-Pfad-Regel).“), A53:23 (R68), REG 2 Zeilen, 02c:75 und 02c:140, `docs/ERGEBNIS_TB-41_registernachtrag.md` 1, `docs/belege/TB-132/vormessung/v4_register_02c.md` 1, sechs ältere Registerkopien je 1. Nicht von git geführt: `FABLE_ANFRAGE_2026-10-04a_…md` Z. 29 und Z. 35 (2 Zeilen).
- In den von Fable als Trefferquellen genannten Dateien: `ERGEBNIS_TB-114_register_45_herkunft_pfadregel.md` 0, `DOKUMENTATIONSSTANDARD.md` 0, A03 0, A06 0, A41 0, `BACKLOG.md` 0; `PRUEFPRINZIPIEN.md` liegt nicht unter `docs/projektfuehrung/` und erscheint in der `git grep`-Liste nicht.

### 21 — Eröffnung 04.10. (`docs/projektfuehrung/FABLE_UEBERGABE_2026-10-04_eroeffnung.md`, 136 Z., 9 259 B)
- Z. 37–43: „Projekt-Erinnerung (R56 (d)): Du liest nur die Dateien, die der steuernde Chat hier mit Stand und Grösse nennt: gemessen am 04.10.2026, zuletzt 09:53, gegen 27.1, je 0 Treffer: im Projekt preferences.md (Stand 02.10.2026, 10:46 MESZ = 08:46 UTC, 9 241 B) und ways-of-working.md (Stand 01.10.2026, 21:51 MESZ = 19:51 UTC, 2 232 B); kontoweit profile.md (Stand 26.09.2026, 385 B) und preferences.md (Stand 20.09.2026, 673 B), die die Plattform ohne dein Zutun lädt (Rolle und Ablageform, keine Ergebnisse). Nur diese vier.“
- `grep -c -F`: „9 241“ 1, „2 232“ 1, „385“ 1, „673“ 1. Stände 08:46 UTC / 19:51 UTC / 26.09. / 20.09. wie im Leseprotokoll 04a.
- „gesperrt“: 0 Treffer. „Sperre“: 1 Treffer, Z. 47: „Alle anderen Erinnerungsdateien stehen unter derselben Sperre wie BACKLOG.md.“ Eine Liste gesperrter Dateien mit Namen nennt die Eröffnung nicht; namentlich steht dort nur `BACKLOG.md`.
- `project_search` / „Suchlauf“ / „Suche“: 0 Treffer. Z. 34–36: „… Öffne, was du brauchst, und nur das. Kein Lesen in Auszügen, wo eine Entscheidung am Wortlaut hängt; kein zusammenfassender Helfer.“
- Z. 50: „Gemessen vom steuernden Chat am 04.10.2026, 09:35, am Repo (HEAD d781f1b):“

## Beifang (gemessen, ohne Deutung)
- `git --no-optional-locks ls-files` und `git log -1 -- <Datei>` liefern nichts für: `FABLE_UEBERGABE_2026-10-04_eroeffnung.md`, `FABLE_UEBERGABE_2026-10-04_neuer_chat.md`, `FABLE_ANFRAGE_2026-10-04a_…md`, `FABLE_ANTWORT_2026-10-04a_…md` (alle unter `docs/projektfuehrung/`). Die vier Dateien liegen im Ordner, sind am HEAD `d781f1b` aber nicht geführt. (Positivprobe: `BACKLOG.md` wird gelistet.)
- Leseprotokoll 04a nennt 13 Abschnitte als vollständig gelesen (53, 16, 17, 23, 45, 48, 51, 52, 41, 15, 29, 50, 25); im Ordner liegen 54 Abschnittsdateien (00–53).
- Kopf der Abschnittskopien: „Commit ee43f5f1339549238c0da023db7c9f324b26d28e — 2026-10-04 — Original sha256 9a2cefb77a39…“ (wie im Leseprotokoll 04a genannt).

## Nicht messbar
- Was `project_search` dem Verfahrensprüfer als Ausschnitt aus `BACKLOG.md` geliefert hat: am Repo nicht nachstellbar (die Suche der Ablage arbeitet nicht über grep; das Suchwort steht in der Datei nicht).
- „Gesucht hat es nicht“ (Frage 3 Nr. 3) und „94 Namen“ der Dateiliste: Selbstauskunft, am Repo nicht messbar. Messbar war nur 02b:31 („kein Suchlauf“).
- Byte-Grössen und Stände der Erinnerungsdateien selbst: nicht im Repo; gemessen wurde nur die Zahlenliste der Eröffnung.
- „die Zählung des steuernden Chats zur Anfrage 04.10.a, Frage 3“ (Quelle des Grundes R76): nicht Teil des Auftrags, nicht gemessen.

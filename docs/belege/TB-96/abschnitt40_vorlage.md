## 40. Testannahmen folgen dem Register, und die neun Handelslisten sind Eingabedateien — `G6`/`H3`, die Kopplung an 5.1 Nr. 4, jede Mutationsprobe mit Gegenprobe, was TB-97/TB-98 tun, und drei angenommene Berichtigungen an den Verfahrensprüfer (Fable 24a, TB-96, 24.09.2026)

⭐ **Reines Eintragen von Registertext und Tatsachen**, wie 34 bis 39. Der Test
ist seit TB-95 grün (40.1–40.4); Fable hat in **24a** geantwortet und dazu
**zwei neue Registertexte** gesetzt: die neun Handelslisten als
Eingabedateien nach 23d (40.6) und die Gegenprobe jeder Mutationsprobe als
Ergänzung zu 12 (40.7). Was daraus beschlossen, aber nicht ausgeführt ist,
steht in 40.8; drei Berichtigungen an ihn, die er angenommen hat, in 40.9.
Fable-Texte zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md`
— **eingesetzt, nicht abgetippt** (Beleg `docs/belege/TB-96/d2_zitate.txt`, je
Zitat `diff` rc 0). Anfrage
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-24a_punkt8_vollzogen_test_gruen_neun_listen.md`;
Auftrag `docs/auftraege/MAC_TB-96_register_40.md`; Belege
`docs/belege/TB-96/`; Schritt-0-Commit `fc8d44c`. Messungen des Vorgängers:
TB-95 (`docs/ERGEBNIS_TB-95_testannahmen_und_lesehaken.md`, Belege
`docs/belege/TB-95/`), in TB-96 an Hashes und Register nachgemessen
(`a_messungen.txt`).
⛔ **Keine `.py` geändert, nichts gerechnet** — 40.10.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (5.1 Nr. 4; 5.4;
12; 21.9; 33.2; 33.5; 36.6; 37.2; 39.6; dazu der Nachtrag in 39.8 — zehn
Stellen). Die alten Sätze bleiben zeichengleich; `git diff --numstat` auf
dieses Register zeigt für TB-96 in der zweiten Spalte `0`.

**Fables Kenntnisnahme, 24a Abschnitt 1, zeichengleich:**

> ⟦Z:9⟧

### 40.1 Tatsachennotiz — der Test ist grün

`research/vorregistrierung/test_vorregistrierung.py` (`73c9b837…`, Commit
`9e2a071`, TB-95) läuft am 23.09.2026 **165/165, rc 0**, 534 s, in einem Zug
am echten Stand (`docs/belege/TB-95/c_test.txt`). ⇒ **Die Tag-Vorbedingung
„null rote Prüfungen, null ‚bekannt rot'" (21.9, A4; 23a, Wortlaut in 39.1) ist
für diesen Test erfüllt.** Geändert ist nur diese eine Datei
(`6e7defef…` → `73c9b837…`); keine Prüfung entfallen, keine Ausnahme für einen
Bot, keine Toleranz, `auswertung.py` unberührt; kein Sperrlistenhash bewegt;
Sonde gegen `sperrliste_abbild_2026-09-23.json` 0 Befunde, 15/15 Pfade gleich
(`docs/belege/TB-95/c_hashes.txt`, `c_sonde.txt`). In TB-96 nachgemessen:
Hash und letzter Commit unverändert (`a_messungen.txt`, A2).

**Fable, 24a Abschnitt 1, zeichengleich:**

> ⟦Z:11⟧

⚠️ **Was „erfüllt" hier heisst und was nicht:** Die Vorbedingung gilt für den
Stand von heute. 40.8 beschliesst weitere Änderungen an genau diesem Test
(`F4`, die vier Literale, Gegenproben); jede davon muss ihn wieder grün
hinterlassen. Und ein grüner Test ist nach 40.7 erst dann ein Nachweis, wenn
jede seiner Mutationsproben eine Gegenprobe hat — für `H3` ist sie geführt
(40.3), für die übrigen sieben steht sie aus (40.8 (c)).

**Marke am alten Ort:** bei **21.9**, unter der Tabelle der Folgen.

### 40.2 `G6` — die Jahre aus dem Register, die Abdeckung gerechnet

**Wie gebaut (TB-95, `9e2a071`):** `G6` liest die Jahre aus dem Registertext
**5.1 Nr. 4** (Funktion `_testjahre_aus_register`) und rechnet die Abdeckung
aus `von`/`bis_ausschliesslich` der Falten mit Rolle `selektion`
(`_abgedeckte_jahre`); die Bestätigungsperiode zählt nicht. Bis TB-95 stand
dort `"2020" in namen` — seit den Zweijahresfalten von `elliott_wave` traf das
nichts mehr.

**Gemessen vor der Änderung (TB-95, `a2_g6.txt`):** 2020 und 2022 lagen bei
**allen neun** Bots in genau einer Selektionsfalte, bei `elliott_wave` in
`2020-2021` und `2022-2023`. ⇒ **Die Sache hinter 5.1 Nr. 4 war erfüllt; rot war
nur die Formulierung.** Die Probe beisst (TB-95, `b_probe.txt`): Falte
`2020-2021` als Bestätigung ⇒ genau ein `G6` rot; Registersatz fehlt (Kopie) ⇒
neun `G6` rot.

⚠️⚠️ **Die Kopplung, gemessen (TB-96, `a_messungen.txt`, A6):** Die Funktion
sucht im ganzen Register **zeilenweise, am Zeilenanfang verankert**, die Zeile,
die mit `4. **JJJJ und JJJJ sind Testfalten, keine Trainingsjahre.**` beginnt
(Muster `^4\. \*\*(\d{4}) und (\d{4}) sind Testfalten, keine Trainingsjahre\.\*\*`).
Heute: **genau ein Treffer**, der Listenpunkt 5.1 Nr. 4; Ergebnis `[2020, 2022]`.
Kein Treffer **oder zwei** ⇒ `None` ⇒ `G6` rot für alle neun Bots. Daraus
folgt zweierlei:

| | |
|---|---|
| (1) | **Wer 5.1 Nr. 4 umformuliert** — auch gut gemeint, auch nur Satzzeichen oder Hervorhebung —, **macht `test_vorregistrierung.py` rot.** Eine Änderung der Sache (andere Jahre) braucht einen eigenen Registereintrag **und** die Anpassung von `G6` im selben Auftrag |
| (2) | **Wer irgendwo im Register eine zweite Zeile mit diesem Anfang schreibt**, etwa ein Zitat von 5.1 Nr. 4 in Spalte 0, macht ihn ebenso rot. Zitate dieser Zeile stehen deshalb eingerückt oder als Blockzitat (`> `) — so auch in diesem Abschnitt |

⭐ **Das ist eine Kopplung, die bis heute niemand sah:** Registertext wird
sonst gelesen, nicht geparst; die Sperrlisten-Sonde liest Abschnitt 10, und
dort steht es seit 36 im Register. Für 5.1 Nr. 4 stand es nirgends. **Die
Marke bei 5.1 Nr. 4 ist der eigentliche Schutz** — sie steht dort, wo jemand
ändern würde.

**Marke am alten Ort:** bei **5.1 Nr. 4**, direkt unter dem Listenpunkt.

### 40.3 `H3` — strikte Mehrheit statt fester Zahl

**Wie gebaut (TB-95, `9e2a071`):** `ohne` = die ersten `len(sel) // 2 + 1`
Selektionsfalten des Plans — eine **strikte Mehrheit**, die bei jeder Parität
beisst; beim Plan von TB-95 für `turtle_soup_stocks` fünf von neun
(`2017`–`2021`).

**Gemessen vor der Änderung (TB-95, `a3_h3.txt`):** Die vier alten Namen
(`2019`–`2022`) **trafen alle** — die Probe griff nicht ins Leere. Aber vier
Nullen verschieben den Median über **neun** Falten nicht (`0.1000` /
`0.1000`); bei sieben Falten, für die die Zahl einst gewählt war, reichten
vier. Allgemein ist das kleinste wirksame k = ⌈n/2⌉. **Die Probe beisst
wieder** (`0.0000` / `9.0000`), und **die Gegenprobe mit leerer Menge
scheitert** (`0.1000` / `0.1000`) — sie beisst aus dem richtigen Grund.

⭐ **Fables Einordnung, 24a Abschnitt 1, zeichengleich:**
*„⟦T:11|H3 griff nicht ins Leere, sondern die **Zahl** war gealtert (vier reichten bei sieben, nicht bei neun) — dieselbe Klasse wie der Name, nur unsichtbarer⟧"* — und weiter:
*„⟦T:11|Die Bauart von G6 (Jahre maschinell aus 5.1 Nr. 4, sonst `None` ⇒ rot) und H3 (strikte Mehrheit, paritätsfest) ist genau das, was 23a verlangt hat⟧"*.

### 40.4 Die weiteren Literale und `F4`

**Die Liste aus TB-95 (`a4_literale.txt`), in TB-95 nicht geändert, weil heute
grün:**

| Stelle (Datei, Teil) | Literal | Zustand | warum es trotzdem gealtert ist |
|---|---|---|---|
| `test_vorregistrierung.py`, Teil D | `ruhig, krise = "2021", "2020"` | grün | nur weil `BOT` Einjahresfalten hat; die Jahreswahl ist Registerinhalt 4.4. ⚠️ Bekommt `BOT` Zweijahresfalten, **bricht Teil D mit `KeyError`** |
| `test_vorregistrierung.py`, Teil F | `ohne = "2022"` | grün | aus demselben Grund; F1/F2 würden rot |
| `beispieldaten.py`, Krisen-Drawdown | `falte in ("2020", "2022")` | keine Prüfung | trifft bei `elliott_wave` nie |
| `beispieldaten.py`, Exposure | dasselbe | keine Prüfung | bei `elliott_wave` konstant; der Zufalls-Timing-Test ist dann nach dem eigenen Docstring **entartet** |

(Zeilennummern am Stand `9e2a071`: Teil D Z. 246, Teil F Z. 442,
`beispieldaten.py` Z. 69 und 77 — nach 38.2 nur mit Commit.)

⚠️ **Dazu `F4` (TB-95, Zusatzbefund):** Die Prüfung sagt „Median mit der Null
liegt **unter** …", prüft aber mit `<=`. Bei einer Null unter neun (oder
sieben) Falten sind beide Mediane gleich. **`F4` hat nie gebissen** — und das
hängt nicht am Plan.

**Fable, 24a Abschnitt 5, zeichengleich:**

> ⟦Z:49⟧

**Und zu den Literalen, 24a Abschnitt 6, zeichengleich:**

> ⟦Z:57⟧

⇒ **Beides ist beschlossen (40.7, 40.8 (a)–(c)), nicht erledigt.**

### 40.5 ⛔ Entfällt als eigener Unterabschnitt — steht als Nachtrag in 39.8

Die Antwort auf Fables Messbitte zu den neun Handelslisten (23f Abschnitt 6)
steht als **Nachtrag am Ende von 39.8**, nicht hier. **Fable, 24a Abschnitt 4,
zeichengleich:**

> ⟦Z:45⟧

⭐ *Diese Nummer steht trotzdem hier, damit niemand später 40.5 sucht und das
Register für lückenhaft hält.* Die Einordnung, mit der der Nachtrag endet,
steht in **40.6**.

### 40.6 ⭐⭐ Die neun Handelslisten — Eingabedateien nach 23d

**Was gemessen ist** (TB-95, Nachtrag in 39.8): `benchmark.py` öffnet die neun
`research/tb24_haltedauern/daten/<bot>_alle_trades.csv` über
`faltenplan.py::faltenlaenge_jahre`; ihre Inhalte gehen **über eine
Schwellenentscheidung** — die Faltenlänge nach 5.4 — in Faltenplan und Tabelle
ein. Sie stammen aus `78e2bc6` (TB-24, 13.09.2026), liegen nicht im Snapshot,
nicht auf der Sperrliste. Die Frage an Fable (Anfrage 24a): Genügt dafür ein
Hash-Eintrag, oder gilt die volle Regel aus 23d?

**Der Registertext — Fable, 24a Abschnitt 3, zeichengleich:**

> ⟦Z:33⟧

**Sein Grund, zeichengleich:**

> ⟦Z:29⟧

**Seine Antwort auf unseren Einwand — 23d verlangt „aus", nicht „im" Snapshot,
zeichengleich:**

> ⟦Z:31⟧

**Seine Quelle des Grundes, zeichengleich:**

> ⟦Z:35⟧

**Zu unserem zweiten Umstand („über `git` reproduzierbar"), zeichengleich:**

> ⟦Z:39⟧

**Zu unserem ersten Umstand (die Kippung würde am Abbild sichtbar),
zeichengleich:**

> ⟦Z:37⟧

**Die Folge für 5.4, zeichengleich:**

> ⟦Z:41⟧

⚠️ **Kein Ergebnis — ausdrücklich:** Fable verlangt die Ableitung, **ohne zu
wissen**, ob sie 33.2 bestätigt, und er braucht danach nur das Ob je Bot
(Faltenlänge 1 oder 2), **keine Trade-Zahlen** (27.1). Gleich ⇒
Tatsachennotiz; verschieden ⇒ Berichtigung von 33.2 und allem, was daran hängt
— keine Wahl. Die Regel steht hier, **bevor** gerechnet ist (Bauart 24.3).

**Tatsachennotiz zu 5.4 — Fables Unsicherheit, gemessen (`a_messungen.txt`,
A4/A5).** Seine Unsicherheit, 24a, zeichengleich:

> ⟦Z:81⟧

| | gemessen |
|---|---|
| ⭐ **Die Schwelle ist registriert** | „30 Trades je Jahr" ist **Festlegung 7** (Tabelle am Registeranfang) und steht als Regel in **5.1 Nr. 6** („Faltenlänge ein Jahr, zwei Jahre bei unter 30 gefundenen Trades je Jahr."); 5.4 wertet sie aus. `faltenplan.py::faltenlaenge_jahre` liest sie als `registerdaten.ZWEIJAHRES_SCHWELLE_TRADES`, **nicht** als Literal (0 Treffer für einen Vergleich mit `30`) |
| ⚠️ **Der Parameterstand der Erzeugung ist es nicht** | 5.4 nennt die Listen als Pfad (`<bot>_alle_trades.csv`) ohne Hash und ohne Commit und sagt nur, die Trades seien **„gefunden, nicht ausgeführt"**, weil das Positionslimit ein Rasterparameter ist. Mit welchen Parametern die Listen am 13.09.2026 erzeugt wurden, steht **nirgends im Register** (`78e2bc6`: 0 Treffer; „heutige Parameter" in 5.4: 0 Treffer). 5.4 sagt auch **nicht** „mit heutigen Parametern" |
| ausserhalb des Registers | Der TB-24-Bericht sagt „mit den heutigen `live_params.py` über die heutigen Bot-Funktionen" (Stand 13.09.). Die `<bot>_meta.json` daneben tragen Kapital, Allokation, Positionslimit und Zählungen, **keine Strategieparameter**. Die neun `live_params.py` haben sich seit `78e2bc6` nur in drei Kommentarzeilen geändert, **keine Zuweisung**; der übrige Code (Bots, Simulation, Entscheidungskerze TB-38, Kostenmodul TB-90) ist hier **nicht** gemessen |

⇒ **Nach Fables eigener Bedingung gehört der Parameterstand der Neu-Erzeugung
als Tatsachennotiz zu 5.4**, sonst ist die Ableitung nicht reproduzierbar: je
Bot die Hashes der Parameterdateien, der Code-Commit, der Snapshot-Hash und der
Modus — neben dem Hash der neuen Liste. ⛔ **Der Regeltext von 5.4 bleibt
unverändert.**

⚠️ **Tatsachennotiz zu einer Voraussetzung in Fables Einwand-Antwort (TB-96
gemessen, kein Registertext geändert):** Der Satz „TB-90 hat gezeigt, dass
diese Backtests byte-identisch reproduzieren" stützt sich auf **TB-90 B6**
(`docs/ERGEBNIS_TB-90_wegA_und_kostenmodul.md`, Beleg
`docs/belege/TB-90/b6_vergleich.txt`): je Bot **ein** Backtest vor und nach dem
Kostenmodul, `cmp` 9/9 identisch — am selben Tag, auf `data/`, mit den
Backtest-Skripten der Bots. **Der Erzeuger der TB-24-Listen**
(`research/tb24_haltedauern/alle_bots.py` → `positionen_holen.py`, der
**gefundene** statt ausgeführter Trades schreibt) **war daran nicht
beteiligt**, und ein Lauf auf dem Snapshot ebenfalls nicht. ⇒ Die Regel trägt
trotzdem: Sie verlangt ihren **eigenen** Reproduzierbarkeitsnachweis — den
Modus-Lauf zweimal, bytegleich (23e) —, nicht den aus TB-90. Die Voraussetzung
ist damit **Voraussetzung der Neu-Erzeugung (TB-98)**, keine gemessene
Tatsache. *Vorgelegt, nicht berichtigt — es ist Fables Satz.*

⚠️ **Tatsachennotiz zum Erzeuger (TB-96 gemessen):** `positionen_holen.py`
schreibt **fest** nach `research/tb24_haltedauern/daten/` (Konstante
`DATEN_DIR`, `to_csv` ohne Ziel-Schalter, `os.makedirs(…, exist_ok=True)`) —
es ist **kein** Erzeuger nach 36.1 (`--ziel`, Einmal-Schreibsperre). ⛔ **Ein
unveränderter Aufruf überschriebe die alten Listen**, die nach dem Registertext
oben als historischer Stand liegen bleiben. Die Neu-Erzeugung braucht deshalb
einen Erzeuger unter 36.1 (Handwerk mit Freigabe, TB-98).

**Folge für den Plan — Plan-Punkt 7 rückt vor.** Das Abbild des Faltenplans
(33.3) und die Faltenplan-Sonde sind die Wache, die genau diese Klasse fängt
(ein Schwellenübertritt, der den Faltenplan eines Bots verschiebt), und sie
fehlen (33.5). ⚠️ **Das Abbild wird NACH der Ableitung erzeugt, nicht vorher**
— sonst bildet es einen Stand ab, der gerade geprüft wird.

**Marken am alten Ort:** bei **5.4** (Listen sind Eingabedateien, werden neu
erzeugt; Parameterstand fehlt), bei **33.2** (Faltenlänge wird neu abgeleitet
und gegen diesen Text verglichen), bei **33.5** (Abbild rückt vor, nach der
Ableitung), bei **39.6** (Eingabestand: zweiter Anwendungsfall).

### 40.7 ⭐ Ergänzung zu 12 — jede Mutationsprobe hat eine Gegenprobe

**Der Registertext — Fable, 24a Abschnitt 5, zeichengleich:**

> ⟦Z:51⟧

**Seine Quelle des Grundes, zeichengleich:**

> ⟦Z:53⟧

⚠️ **Die Tatsache, die ihn ausgelöst hat:** **`F4` hat drei Wochen
„bestanden", ohne je gemessen zu haben** (40.4) — `<=`, wo der Text „unter"
sagt, bei gleichen Medianen. Und `H3` hat gezeigt, dass eine Probe auch dann
nicht beisst, wenn alle ihre Namen treffen (40.3).

⇒ **Vor dem Tag wird die Gegenprobe für alle acht Mutationsproben einmal
geführt und als Tatsachennotiz festgehalten** (40.8 (c)). Geführt ist sie
heute für **eine**: `H3` (TB-95, `ohne` leer ⇒ scheitert). ⚠️ **Welche acht
Prüfungen „die acht Mutationsproben" aus Abschnitt 12 sind, ist hier nicht
gemessen** — Abschnitt 12 nennt die Zahl, nicht die Namen; die Liste gehört in
die Tatsachennotiz von TB-97.

**Marke am alten Ort:** bei **12**, unter dem Absatz über den Schalter.

### 40.8 Beschlossen, nicht ausgeführt — was TB-97, TB-98, TB-100 und TB-101 tun

Damit das Register sagt, was offen ist und warum:

| | Sache | Auftrag |
|---|---|---|
| (a) | `F4`: `<=` → `<`, Probe mit Mehrheit wie `H3`, Gegenprobe „leere Menge ⇒ scheitert" | TB-97 |
| (b) | Die vier Literale (40.4) bauartgleich umstellen, nach Fables Regel (Zitat unten). Für 4.4: Tatsachennotiz, dass seine Beispieljahre der Stand vom 14.09. sind, und die Prüfung liest den **heutigen** Plan | TB-97 |
| (c) | Gegenproben für **alle acht** Mutationsproben, mit Tatsachennotiz (40.7) | TB-97 |
| (d) | Sonde: **getrennte Schlusszeilen** — „Pfad-Bestandteile: n geprüft, davon 0 / 1 / 2" und „Regel-Bestandteile: m nicht prüfbar (2), je mit Verweis auf die Tatsachennotiz". Der Gesamtwert bleibt, wie 36.5 ihn definiert | TB-97 |
| (e) | ⚠️ **Befund:** Die Gruppe „bestimmt" steht **fest verdrahtet** in `shared/sperrlistensonde.py` (`BESTIMMT_NICHT_EINGETRAGEN`, 39.3). Sie liest künftig **alle drei Gruppen** (Abschnitt 10, „bestimmt", `EINGEFROREN`) **aus dem Abbild**; Gegenprobe: Abbild mit erfundenem „bestimmt"-Pfad ⇒ Sonde meldet ihn | TB-97 |
| (f) | Neun Listen auf dem Snapshot neu erzeugen (Erzeuger unter 36.1), Sperrlistenpunkt, Tatsachennotizen; Faltenlänge nach 5.4 ableiten, gegen 33.2 vergleichen (40.6) | TB-98 |
| (g) | Abbild des Faltenplans (33.3) und Faltenplan-Sonde — **nach** (f) | TB-100 |
| (h) | `messgroessen.json` auf dem Snapshot (23d/23e), `registerdaten.py`, die zwölf Rasterachsen | TB-101 |

⚠️ **(b) vor (f):** Teil D bricht mit `KeyError`, sobald `BOT` Zweijahresfalten
bekommt — und **ob er das nach (f) bekommt, weiss vor der Ableitung niemand.**
(g) nach (f), weil das Abbild sonst einen Stand abbildet, der gerade geprüft
wird. ⚠️ **TB-99 ist kein Auftrag** — die Nummer ist für die Wächter-Sonde
reserviert (`ARBEITSWEISE` 22.2).

**Zu (b), Fable 24a Abschnitt 6, zeichengleich:**

> ⟦Z:59⟧

**Zu (d) und (e), Fable 24a Abschnitt 7, zeichengleich:**

> ⟦Z:63⟧
>
> ⟦Z:65⟧

**Marken am alten Ort:** bei **37.2** und **36.6** (die Gruppen kommen aus dem
Abbild).

### 40.9 ⚠️ Drei Berichtigungen an den Verfahrensprüfer — angenommen

| | gemessen | Fables Annahme, zeichengleich |
|---|---|---|
| (a) | `benchmark.py` an **zwei** Punkten (4 und 6; 39.5) | „⟦T:15|Mein „drei" war nicht gemessen⟧" |
| (b) | `beispieldaten.py` liest **keine** Benchmark-Tabelle (39.2) | „⟦T:17|Ich habe es als Leserin **angenommen**, weil es die Testdaten erzeugt — nicht gemessen⟧" |
| (c) | TB-94 → TB-96 für `messgroessen.json` (39.8) | „⟦T:19|TB-94 → TB-96 für `messgroessen.json`. Angenommen; 39.8.⟧" |

**Fable, 24a Abschnitt 2, zeichengleich:**

> ⟦Z:15⟧
>
> ⟦Z:17⟧
>
> ⟦Z:19⟧
>
> ⟦Z:21⟧

⭐ **Er zählt sie mit** — dieselbe Klasse wie die sechs Rücknahmen der ersten
Woche: eine Tatsache über den Bestand behauptet statt als Voraussetzung
genannt.

⚠️⚠️ **Zu (c) — die Nummer ist wieder gerückt, und das gehört hierher, damit
die Ablage lesbar bleibt:** 39.8 hat „TB-94 → TB-96" berichtigt, und Fable hat
es angenommen. Seitdem ist **TB-96 dieser Eintrag** (Abschnitt 40), und
`messgroessen.json` ist **TB-101** (40.8 (h); `docs/auftraege/AKTUELLER_AUFTRAG.md`,
Stand 24.09.2026). Die Sache ist dieselbe, nur die Nummer nicht — *eine Nummer,
die zwei Sachen meint, ist schlimmer als eine verschobene* (39.8). ⇒ Wo 39.6,
39.8 oder 39.10 „TB-96" für `messgroessen.json` sagen, gilt **TB-101**; die
Sätze bleiben zeichengleich.

⚠️ **Ein vierter Fall derselben Klasse ist in 40.6 vorgelegt, nicht
berichtigt:** „TB-90 hat gezeigt, dass diese Backtests byte-identisch
reproduzieren" — TB-90 B6 hat die Backtest-Skripte der Bots gezeigt, nicht den
Erzeuger der Listen. Die Regel trägt davon unabhängig.

### 40.10 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Keine `.py` geändert** — weder `test_vorregistrierung.py` (`F4`, die vier Literale, Gegenproben) noch `beispieldaten.py`, `shared/sperrlistensonde.py`, `faltenplan.py`, `benchmark.py` noch die Erzeuger unter `research/tb24_haltedauern/` | TB-97 / TB-98 |
| ⛔ | **Nichts gerechnet** — keine Liste neu erzeugt, keine Faltenlänge abgeleitet, der Test nicht erneut ausgeführt; in `research/vorregistrierung/ergebnisse/` nichts geschrieben | TB-98 |
| ⛔ | **Kein neues Abbild** — keine Sperrlistendatei hat sich bewegt; das gültige Abbild bleibt `sperrliste_abbild_2026-09-23.json` (`2f23f76c…`), Sonde vorher und nachher gleich (`d3_sonde.txt`) | — |
| ⛔ | **Kein alter Registersatz umgeschrieben** — 5.1 Nr. 4 (Wortlaut für `G6`), 5.4 (Regeltext), 12, 21.9, 33.2, 33.5, 36.6, 37.2, 39.6 und 39.8 bleiben zeichengleich; Marken und ein Nachtrag, nichts entfernt | — |
| ⛔ | **Die Listen nicht auf die Sperrliste genommen** — das geschieht mit den neu erzeugten Listen (40.6), nicht mit den alten | TB-98 |
| ⭐ | **N = 653 (Festlegung 10) unberührt**; Festlegung 7 (Schwelle 30) unberührt | — |
| ⚠️ | **Offen:** 40.8 (a)–(h) · der Parameterstand der Neu-Erzeugung als Tatsachennotiz zu 5.4 (40.6) · die Liste der acht Mutationsproben (40.7) · die Voraussetzung „TB-90 hat gezeigt" (40.6, bei Fable) · der Registertext „Eingabestand" (23d) selbst ist weiter **nicht** eingetragen (39.6) | TB-97 / TB-98 / TB-101 / Fable |

*Dieser Abschnitt ist rein additiv: Er trägt zwei Registertexte des
Verfahrensprüfers zeichengleich ein, hält eine Kopplung zwischen Registertext
und Test fest, die bisher niemand sah, beschliesst die nächsten vier Aufträge
mit ihrer Reihenfolge, setzt Marken an zehn Stellen — und entfernt nichts.
Gebaut und gerechnet wird nichts.*

# REGISTER-KOPIE Abschnitt 23 (von 0–50) — Register-Z. 3819–4200 — Commit db108a68ec57316250ca792a0673b5932dd0f0e8 — 2026-10-01 — Original sha256 b58046592205bfac803f2e590385924dc5c0fd80fa7943c9a9d5cff40cfbbea1 — KOPIE, nicht das Register

## 23. Berichtigung zu Registertext 3b (c) — der Benchmark wird tagesgenau (TB-66, 20.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Satz wird umgeschrieben —
der berichtigte Satz bleibt in Abschnitt 16.7 stehen** (dort seit heute mit der
Marke *„(c) ERSETZT durch Abschnitt 23"*), wird hier wörtlich zitiert und von
der Festlegung, der Messung und dem Ersatztext gefolgt. Das ist die Form aus
`docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md`, Regel 4, und die Form von
Abschnitt 21.

**Anlass:** `docs/ERGEBNIS_TB-65_benchmarkschranke.md` hat gemessen, dass der
Wortlaut *„in dieser Falte geladen"* zwei Lesarten zulässt — **VH** (geladen,
ganze Falte) und **VT** (geladen, ab dem Tag, an dem der Loader das Symbol
handelbar macht) — und dass beide in den frühen Krypto-Falten weit
auseinanderliegen (`turtle_soup_crypto` 2018: **−87,92 %** gegen **−3,60 %**
bei 100 % Exposure). Die Frage ging an Fable
(`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20_benchmarkfenster.md`); seine
Antwort vom 20.09.2026, 15:19 Ortszeit, liegt wörtlich in
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-20_benchmarkfenster.md`. **Er legt
VT fest.** Die Umsetzung ist `docs/auftraege/MAC_TB-66_benchmark_tagesgenau.md`,
das Ergebnis `docs/ERGEBNIS_TB-66_benchmark_tagesgenau.md`.

**Art der Änderung nach der Drei-Kategorien-Regel (F17): eine Berichtigung.**
Der Grund kommt aus dem Registertext selbst — aus seinem eigenen Zweck-Satz
*„Bot und Benchmark leben in derselben Menge"* —, nicht aus der Wirkung. ⚠️
**Die Wirkung ist bekannt und geht gegen die Bots** (VT ist in den frühen
Krypto-Falten die strengere Lesart); sie steht in 23.4 vermerkt. **Sie ist nicht
der Grund.** Es hat kein Selektionslauf stattgefunden; kein Parametersatz ist
bewertet, kein Ergebnis erzeugt.

---

### 23.1 Der berichtigte Satz, wörtlich

Aus **Abschnitt 16.7**, Registertext 3b, Ergänzung (c) (Commit `1bc2d57`,
16.09.2026):

> **(c)** ⭐ **Der Benchmark einer Falte** — für die Drawdown-Nebenbedingung
> (Abschnitt 4) und für Rang 3 — **wird auf den in dieser Falte geladenen
> Symbolen des Bots gerechnet, nicht auf dem vollen Universum. Bot und
> Benchmark leben in derselben Menge.**

⚠️ **Was daran unpräzise ist — und was ausdrücklich nicht.** Richtig und
unverändert ist die Menge: die vom Loader des Bots geladenen Symbole, nicht das
volle Universum. Richtig und unverändert ist der Zweck-Satz. **Unpräzise ist
der Zeitbezug** *„in dieser Falte geladen"*: er sagt nicht, ob ein Symbol, das
der Loader am 30. Dezember handelbar macht, für den 30. und 31. Dezember zählt
oder für das ganze Jahr. Fable dazu, wörtlich: *„Der Wortlaut ‚in dieser Falte
geladen' war meiner, und er war unpräzise. Der Begründungssatz war es nicht."*

---

### 23.2 Die Festlegung und ihre Gründe (Fable, 20.09.2026)

> **VT — und der Grund steht im Registertext selbst, nicht in der Wirkung.**
>
> *Die Menge, in der ein Bot lebt, ist tagesgenau — er kann ein Symbol an
> keinem Tag halten, an dem sein Loader es nicht geladen hat. Ein Benchmark,
> der es für die ganze Falte hält, ist eine Alternative, die dem Bot nicht
> offenstand, und genau dagegen war 3b (c) geschrieben.*

**Zwei Gründe, beide aus dem Register, keiner aus der Messung:**

| | |
|---|---|
| **1** | ⚠️ **Unter VH ist die Nebenbedingung dort leer, wo sie binden soll.** In Falte 2018 hat der Bot vor dem 30.12. keine Position, sein Drawdown ist nahe null; der zulässige wäre 1,25 × −87,9 % — **jeder Parametersatz besteht, egal was er tut.** Eine Nebenbedingung, die in dünnen Falten automatisch erfüllt ist, prüft nichts — und die dünnen Falten sind genau die, in denen 3b (d) Rauschen erwartet |
| **2** | ⚠️⚠️ **Unter VH erzeugt Rang 3 Alpha aus Nichtteilnahme.** Benchmark −88 %, Bot ≈ 0 ⇒ **+88 Prozentpunkte Alpha daraus, dass der Bot nichts halten *konnte*.** Rang 3 misst dann, wie lange der Loader gebraucht hat — die Nullen-als-Diversifikation-Fehlerklasse aus `L1` in neuer Kleidung |

**Zu Lesart H (16.2) — kein Widerspruch:** H beantwortet, **ob** eine Falte
zählt (ab einem handelbaren Tag). VT beantwortet, **was der Benchmark an jedem
Tag hält**. H mit VH zusammen wäre der Widerspruch: eine Falte, die wegen eines
Tages zählt, bekäme einen Benchmark aus 365 Tagen, an denen der Bot nicht dabei
war.

**Rang 3 — dieselbe Lesart, zwingend:** *„Es ist ein Benchmark-Objekt mit zwei
Verwendungen, nicht zwei Benchmarks."* Ein Satz in 3b (c) genügt; keine eigene
Festlegung.

**Form — Registertext, nicht Tatsachennotiz:** *„Eine Tatsachennotiz kann sie
festhalten, nicht schaffen"* (Fable, 19.09.2026, Frage c). 3b (c) selbst wird neu
gefasst; die gemessenen Zahlen kommen in die Berichtigungsnotiz (23.4).

---

### 23.3 Der Ersatztext

> **Registertext 3b (c), Fassung 20.09.2026 — ersetzt die Fassung in 16.7.**
>
> Der Benchmark einer Falte wird **tagesgenau** aus den Symbolen gebildet, die
> der Loader des Bots an diesem Tag handelbar macht: gleichgewichtet, täglich
> rebalanciert (Konvention; sie ist die einzige Gewichtung, die bei wechselnder
> Menge ohne weitere Regel auskommt). Der Benchmark einer Falte ist an genau
> den Tagen definiert, an denen mindestens ein Symbol des Bots nach 3b (b)
> handelbar ist. Ein Tag, an dem kein Symbol handelbar ist, gehört nicht zum
> Benchmark — er wird nicht mit Rendite 0 geführt, sondern gar nicht.
> Derselbe Benchmark gilt für die
> Drawdown-Nebenbedingung (Abschnitt 4) und für Rang 3. Bot und Benchmark leben
> an jedem Tag in derselben Menge.

⭐ **Geschlossen in TB-71, 20.09.2026 — der Platzhalter ist gefallen.** An
seiner Stelle steht der Satz zur Zeitachse, verankert an Registertext 3b (b),
der Grösse, die es gibt und die registriert ist. Er ist **nicht** Fables erste
Fassung: seine lautete *„Tage, an denen kein Symbol handelbar ist, tragen
Rendite 0"* und wurde von ihm selbst zurückgezogen, weil sie einen Mechanismus
vorschrieb statt ein Prinzip (`docs/projektfuehrung/FABLE_ANTWORT_2026-09-20b_kalender.md`,
Teil 2). Seine zweite Fassung band den Benchmark an den Kalender des
Bot-Kapitalpfades — **den es nicht gibt**: der Pfad ist ereignisindiziert
(`shared/zuteilung.py:720–735`, gemessen 20.09.2026). Die dritte Fassung, die
jetzt hier steht, wurde in `FABLE_ANFRAGE_2026-09-20c_kapitalpfad.md`
vorgeschlagen und von Fable übernommen (`FABLE_ANTWORT_2026-09-20c_kapitalpfad.md`,
Teil 1): *„Meine Fassung hat einen Kalender vorausgesetzt, den der Kapitalpfad
nicht hat; eure setzt nichts voraus."* Die Absätze und die Tabelle W/C darunter
bleiben als Vorgeschichte stehen (append-only); die Tabelle trägt die Marke
ERSETZT.

**Tatsachennotiz zu 3b (c), Satz zur Zeitachse (TB-71, 20.09.2026):**

> Die Umsetzung lässt den ersten Kurstag je Falte aus, weil `pct_change` dort
> keine Rendite liefert. Abweichung gegenüber dem Satz: höchstens ein Tag je
> Falte. Wirkung auf jede registrierte Zahl: null — 0 abweichende Stufen in
> Drawdown und `DD_Toleranz` über 78 × 100 (TB-66, Nachweis 4). Wird
> `bh_tagesrenditen` je aus anderem Grund angefasst, ist `fillna(0)` auf diesem
> Tag eine Berichtigung des Codes an den Satz.

**`handelstage`** bleibt unverändert die **W-Spalte** — die Länge des
gemeinsamen Kalenders.

**Der Wortlaut ist Fables**, mit einer Ausnahme, die er selbst verlangt hat:
*„nur eines darf im Register stehen, und es muss das sein, was der Code tut.
Vor dem Eintrag nachsehen."* Nachgesehen: Fables Satz *„Tage, an denen kein
Symbol handelbar ist, tragen Rendite 0"* **trifft den Code nicht** —
`benchmark.py::bh_tagesrenditen` schliesst mit `.dropna()` solche Tage aus,
statt sie mit 0 zu führen. ⚠️ **Ein Registertext, der etwas anderes sagt als
der Code, ist genau der Fehler, den Abschnitt 21 berichtigt hat.** Deshalb steht
an dieser Stelle ein sichtbarer Platzhalter und keine der beiden Fassungen, bis
der Betreiber entscheidet:

> ⚠️ **ERSETZT (TB-71, 20.09.2026) durch den Satz zur Zeitachse oben — keine der beiden Fassungen ist gewählt worden.** Die Tabelle bleibt stehen: sie hält fest, wogegen entschieden wurde, und sie enthält die Messung, die C_voll ausgeschlossen hat (`t3_supertrend` 2018 hätte 365 Handelstage statt 0; 23.4, Wirkung 3).

| | Fassung | Folge |
|---|---|---|
| **W** | Wortlaut an den Code: *„Tage, an denen kein Symbol handelbar ist, gehen nicht in den Benchmark ein."* | keine Codeänderung; `handelstage` zählt nur Tage mit Rendite |
| **C** | Code an den Wortlaut: *„Tage, an denen kein Symbol handelbar ist, tragen Rendite 0."* — `.dropna()` durch `.fillna(0)` ersetzt | ⚠️ ändert `bh_tagesrenditen` (Sperrliste Punkt 6) und die berichtete `handelstage`-Zahl; `.fillna(0)` allein setzt den Wortlaut nur teilweise um (23.4, Tabelle) |

**Gemessen, ob es einen Zahlenunterschied macht (23.4):** für den **Drawdown
keinen** — auf keiner der 7 800 Falte-Stufen-Kombinationen, bei keinem Bot in
der `DD_Toleranz`; für **`handelstage` einen**, in vier bzw. fünf frühen
Krypto-Falten. **Hier wird nicht entschieden.**

**Was „handelbar an diesem Tag" heisst — Registertext 3b (b), nicht neu:** Ein
Symbol ist an einem Tag handelbar, wenn seine Historie bis zu diesem Tag die
registrierte Loader-Schranke erreicht — `MIN_HISTORY_DAYS` **500 / 730 / 1 825**
als Zeitspanne, bei `elliott_wave` `MIN_HISTORY_HOURS` **17 520** als
Kerzenzahl. Das ist die Schranke aus 3b (b), tagesgenau gelesen; sie wird hier
angewendet, nicht neu festgelegt.

---

### 23.4 Die Berichtigungsnotiz — Lesart, Wirkung, Grund, Herkunft

| | |
|---|---|
| **Lesart** | **VT** — geladen, ab dem Tag, an dem der Loader das Symbol handelbar macht; innerhalb der Falte wechselt die Menge |
| **Grund** | der Zweck-Satz von 3b (c): *„Bot und Benchmark leben in derselben Menge"* — die Menge des Bots ist tagesgenau |
| **Herkunft** | Fables Antwort vom 20.09.2026 (`FABLE_ANTWORT_2026-09-20_benchmarkfenster.md`), umgesetzt in TB-66 |
| **Wirkung, gemessen** | siehe die drei Tabellen unten; Lauf `research/vorregistrierung/benchmark.py` (Commit `19a1996`, 20.09.2026, 14:30 UTC), Ergebnis `research/vorregistrierung/ergebnisse/benchmark_drawdowns_vt.json` **daneben** — `benchmark_drawdowns.json` (`a163c498…36d1ee`) und `benchmark_drawdowns_neu.json` (`e06812d2…4a062`) byteweise unverändert |

**Wirkung 1 — die Falte, um die es ging** (100 % Exposure): `turtle_soup_crypto`
und `volatility_breakout_crypto` 2018: **−3,60 %** (VT, **1** Handelstag, BTC
und ETH handelbar ab 2018-12-30) statt **−87,92 %** (VH, 365 Tage). `elliott_wave`
2018–2019: **−42,14 %** (133 Tage) statt −84,67 %; `t3_supertrend` 2019:
**−42,21 %** (136 Tage) statt −59,56 %; `t3_supertrend` 2018 bleibt **leer**
(kein Symbol erreicht 730 Tage vor 2019-08-17; Register 21.3 (b), 21.4).

**Wirkung 2 — `DD_Toleranz` je Bot, drei Fassungen nebeneinander** (25 / 50 /
100 % Exposure; gesperrt = TB-30a, TB-61 = `_neu.json` mit Vierjahresfilter, TB-66
= VT):

| Bot | Sel.-Falten gesperrt / TB-61 / TB-66 | gesperrt | TB-61 | **TB-66 (VT)** | Faktor TB-66 / TB-61 bei 25 / 50 / 100 % |
|---|---|---|---|---|---|
| `elliott_wave` | 0 / 4 / 4 | *Platzhalter* | −6,07 / −11,89 / −22,42 | **−16,42 / −31,21 / −55,91** | ×2,71 / ×2,62 / ×2,49 |
| `t3_supertrend` | 0 / 8 / 8 | *Platzhalter* | −3,24 / −6,32 / −12,01 | **−12,89 / −24,73 / −45,16** | ×3,98 / ×3,91 / ×3,76 |
| `rsi2_crypto` | 0 / 7 / 7 | *Platzhalter* | −6,48 / −12,64 / −24,02 | **−17,26 / −32,59 / −57,29** | ×2,66 / ×2,58 / ×2,39 |
| `turtle_soup_crypto` | 0 / 8 / 8 | *Platzhalter* | −3,24 / −6,32 / −12,01 | **−16,13 / −30,52 / −54,05** | ×4,98 / ×4,83 / ×4,50 |
| `volatility_breakout_crypto` | 0 / 8 / 8 | *Platzhalter* | −3,24 / −6,32 / −12,01 | **−16,13 / −30,52 / −54,05** | ×4,98 / ×4,83 / ×4,50 |
| `elliott_wave_stocks` | 7 / 9 / 9 | −2,18 / −4,33 / −8,55 | −2,18 / −4,33 / −8,55 | **−2,18 / −4,33 / −8,55** | ×1,00 |
| `rsi2_mean_reversion` | 7 / 8 / 8 | −2,18 / −4,33 / −8,55 | −3,35 / −6,61 / −12,89 | **−3,32 / −6,55 / −12,77** | ×0,99 |
| `turtle_soup_stocks` | 7 / 9 / 9 | −2,18 / −4,33 / −8,55 | −2,18 / −4,33 / −8,55 | **−2,18 / −4,33 / −8,55** | ×1,00 |
| `volatility_breakout` | 7 / 8 / 8 | −2,18 / −4,33 / −8,55 | −3,35 / −6,61 / −12,89 | **−3,32 / −6,55 / −12,77** | ×0,99 |

⚠️ **Die Krypto-Toleranzen werden gegenüber TB-61 um das 2,4- bis 5,0-fache
tiefer** (gemessen ×2,39 bis ×4,98 je nach Bot und Stufe). Das ist die in TB-65
vorgerechnete Richtung: TB-61 hatte in 17 der 35 Krypto-Selektionsfalten einen
**leeren** Benchmark (Vierjahresfilter, Drawdown 0,00), der den Median nach oben
zog. ⚠️ **Die Toleranz wird damit nachgiebiger — und das ist die Wirkung, nicht
der Grund** (F17, siehe Kopf dieses Abschnitts).

⚠️ **Die vier Aktien-Bots sind gegenüber TB-61 NICHT auf allen Stufen
unverändert** — anders als der Auftrag erwartete, der die Zeichengleichheit
aus TB-65 auf VT übertrug; zeichengleich war dort **VH**. Unter VT ändern sich
bei allen vier die Falten **2019** (92 Stufen; 100 %: −7,30 → **−7,23**), **2025**
(99 Stufen; −17,23 → **−16,99**) und **2026** (97 Stufen; −6,40 → **−6,31**),
weil `ANET` (handelbar ab 2019-06-05), `PLTR`/`DASH`/`ABNB` (2025-09-29 /
2025-12-08 / 2025-12-09) und `APP` (2026-04-14) **mitten in der Falte** handelbar
werden und TB-61 sie — Kursdaten vier Jahre vor Faltenbeginn — für die ganze
Falte mitzählte, also auch während der Peak-Trough-Episode davor. In 2021, 2023
und 2024 liegen die Eintritte **vor** der Episode, dort sind beide Pfade
identisch; 2018 fällt `ABBV` genau auf den Faltenbeginn. **`DD_Toleranz` ändert
sich dadurch bei `rsi2_mean_reversion` und `volatility_breakout`** (acht Falten,
Median als Mittel aus 2019 und 2023) **auf 98 von 100 Stufen** — von −12,89 auf
−12,77 bei 100 %, also **strenger** als TB-61 und weiterhin nachgiebiger als die
gesperrte Tabelle —, bei `elliott_wave_stocks` und `turtle_soup_stocks` (neun
Falten, Median = 2023) **auf keiner**. Beleg:
`docs/belege/TB-66/schritt4_aktien_gegenprobe.txt`.

**Wirkung 3 — die Messung zur offenen Formulierung (W gegen C):**

| Fassung | Drawdown, alle 78 Falten × 100 Stufen | `DD_Toleranz`, 9 Bots × 100 Stufen | `handelstage` |
|---|---|---|---|
| **C_lit** — `.fillna(0)` wörtlich | **0** Abweichungen | **0** Abweichungen | **4 Falten** um je +1: `elliott_wave` 2018–2019 133 → 134, `t3_supertrend` 2019 136 → 137, `turtle_soup_crypto` und `volatility_breakout_crypto` 2018 1 → 2 (der Tag des ersten Kurses, an dem noch keine Rendite vorliegt) |
| **C_voll** — der Wortlaut ganz: Kalender der Falte, fehlende Tage 0 | **0** Abweichungen | **0** Abweichungen | **5 Falten**: `elliott_wave` 2018–2019 133 → 730, `t3_supertrend` 2018 0 → 365 und 2019 136 → 365, `turtle_soup_crypto` und `volatility_breakout_crypto` 2018 1 → 365 |

⭐ **Die Differenz ist überall null ausser bei `handelstage`** — bei den vier
Aktien-Bots auch dort. ⚠️ Ein Tag mit Rendite 0 bewegt den Kapitalpfad nicht;
das ist der Grund, kein Zufall. **Und `.fillna(0)` allein setzt Fables Satz nur
teilweise um**: der Rahmen kennt nur Tage, an denen mindestens ein Symbol einen
Kurs hat; Tage **vor** dem ersten Handelbar-Tag eines Bots stehen gar nicht darin.
Wer C wählt, wählt zwischen C_lit und C_voll mit. Werkzeug und Rohausgabe:
`docs/belege/TB-66/tb66_dropna_gegen_fillna.py`, `schritt3_dropna_gegen_fillna.txt`,
`schritt3_dropna_gegen_fillna.json`.

---

### 23.5 Was der Code seit heute tut — Tatsachennotiz

| | gemessen / gelesen |
|---|---|
| `research/vorregistrierung/benchmark.py`, Commit `19a1996` | Der Vierjahresfilter `point_in_time(…, MINDESTTRAINING_JAHRE)` ist **entfernt** (Fable: *„das Verfahren-A-Artefakt, das mit `MINDESTTRAINING` schon einmal gegangen ist; Code an registrierte Regel, Berichtigung"*). Neu: `tagesgenau(reihen, handelbar)` schneidet jede Kursreihe ab ihrem Handelbar-Tag ab; die erste Tagesrendite eines Symbols ist die vom Handelbar-Tag auf den Folgetag |
| Das Handelbar-Datum | **gelesen, nicht nachgebaut**: `research/faltenplan_neun/faltenschranke_messung.py::loader_lesart` (TB-56-Werkzeug; liest `MIN_HISTORY_*` aus der Bot-Datei; TB-65: Mengen in **78 von 78** Falten gleich der Trockenlauf-Spalte H). Erster Kurstag + `MIN_HISTORY_DAYS`; `elliott_wave`: Tag der 17 520. 1h-Kerze. Vorab geprüft: keine 1h-Datei enthält unvollständige Kerzen, keine 1d/4h-Datei beginnt mit einer — Zählung und erster Kurstag des Werkzeugs sind die des Loaders (`entferne_unvollstaendige`) |
| Die vier gesperrten Rechenfunktionen | `bh_tagesrenditen`, `drawdown_bei_exposure`, `nachschlagen`/`erlaubt`, Medianbildung: **im Code unverändert** (Diff-Hunks berühren keine Zeile ihrer Körper) |
| `bh_tagesrenditen`, Docstring | *„Gleichgewichteter Buy-and-Hold"* → *„Gleichgewichtet, täglich rebalanciert"*. Der Mittelwert der Tagesrenditen ist ein täglich auf Gleichgewicht zurückgesetztes Portfolio, kein Buy-and-Hold; Fable hat es als Unsicherheit benannt, nachgesehen am 20.09.: seine Formulierung trifft den Code. ⚠️ Dieselbe Fehlerklasse wie `K1h` und `T44.10` — ein Name, der etwas anderes verspricht als das Verhalten. `research/exposure_messung/exposure_kern.py::bh_tagesrenditen` trägt denselben Docstring **weiter** (ausserhalb dieses Auftrags, benannt) |
| Ausgabe | `benchmark_drawdowns_vt.json`: **neunmal `status: endgueltig`**; je Bot neu `benchmark`, `loader_schranke`, `handelbar_ab` je Symbol; je Falte `symbole_handelbar_in_falte` statt `symbole_point_in_time`. ⚠️ `registerbericht.py:178` liest den alten Schlüssel aus der **gesperrten** Datei und läuft deshalb heute unverändert; **beim Vollzug der Sperrlisten-Änderung ist er nachzuziehen** |
| Gegen TB-65, Spalte VT | **78 / 78** Falten gleich — alle 100 Stufen, `handelstage`, Symbolzahl; `DD_Toleranz` bei allen neun Bots auf allen Stufen gleich (`docs/belege/TB-66/schritt4_vergleich_tb65_vt.txt`) |
| `research/krypto_historie/faltenplan.py:65` (`MINDESTTRAINING_JAHRE = 4`, `K4f`) | **nicht angefasst**; gemessen: wird von nichts importiert, was hier rechnet (`research/vorregistrierung/`, `research/faltenplan_neun/faltenplan_neun.py`, `faltenschranke_messung.py`) — nur `test_faltenplan_neun.py` nennt den Pfad als Werkzeug. Gehört zu `T56b.6` |
| `registerdaten.MINDESTTRAINING_JAHRE` | bleibt stehen — `faltenplan.py:208` schreibt sie weiter in jeden Plan, `registerbericht.py:140` druckt sie als *„Mindesttraining vor der ersten Falte"*. Beides ist der ersetzte Verfahren-A-Satz (TB-65, Beobachtung 2); ausserhalb dieses Auftrags |

> ⭐ **Stand der letzten Zeile (42.2 E4, Fable 25b/25c, TB-108, 25.09.2026):**
> `faltenplan.py` schreibt `mindesttraining_jahre` **nicht mehr** in den Plan,
> und `registerbericht.py` druckt die Zeile „Mindesttraining vor der ersten
> Falte" **nicht mehr** (TB-106, `abeca36`; ebenso `embargo_nach_falten` je
> Falte). Die Konstante `registerdaten.MINDESTTRAINING_JAHRE` steht weiter, ohne
> Leser — tot bis 40.8 (h). Die Tabelle bleibt zeichengleich.

---

### 23.6 Begriffsberichtigung — „Amendment" gehört zur Sperrliste des Codes, nicht zum Register

**Fable, 20.09.2026, wörtlich:** *„Vor dem Tag ist es eine **Berichtigung des
Registers** und ein **Bug-Fix am Auswerter**; ‚Amendment' gehört zur Sperrliste
des Codes, nicht zum Register — die Unterscheidung bleibt wichtig, sobald der
Tag steht."*

**Gemessen** (Stand Commit `ec7eff4`, vor diesem Eintrag): „Amendment" steht
**24×** in diesem Register (24 Zeilen) und **11×** in `docs/projektfuehrung/BACKLOG.md` (10 Zeilen; `T56b.3` trägt zwei).
**Die meisten Stellen sind richtig** — sie sagen *„kein Amendment"* (Zeilen 855,
1040, 1212, 1442, 1451, 2096, 2116, 2125, 2550, 2570, 2628, 2706, 2786, 3027,
3091, 3268: kein Lauf, also kein Amendment) oder sie beschreiben die Regel selbst
(887–897, 10.1). ⚠️ **Zu berichtigen sind die Stellen, die den bevorstehenden
Vorgang — die neue Benchmark-Tabelle wird die registrierte, der Registertext
verweist auf sie — als „Amendment" bezeichnen.** Nach Fable ist dieser Vorgang
vor dem Tag eine **Berichtigung des Registers** (der Registertext) und ein
**Bug-Fix am Auswerter** (`benchmark.py`); „Amendment" bleibt der Begriff für
die Sperrliste **nach** dem Tag (10.1: *„der Lauf beginnt von vorn"*).

**Das Register ist append-only; die alten Sätze bleiben stehen. Hier steht je
Stelle der Satz, wie er dasteht, und der Satz, wie er zu lesen ist:**

| Fundstelle (Zeile, Stand `ec7eff4`) | Satz, wie er dasteht | Satz, wie er seit dieser Berichtigung zu lesen ist |
|---|---|---|
| **21.6**, Z. 2947–2949 | *„`DD_Toleranz` und die vorab berechneten Benchmark-Drawdowns stehen auf der Sperrliste (Abschnitt 10, Punkt 4), und eine Änderung dort ist ein **Amendment** nach 10.1."* | *„… und eine Änderung dort ist **vor dem Tag eine Berichtigung** (Register) samt **Bug-Fix am Auswerter** (`benchmark.py`), **nach dem Tag ein Amendment** nach 10.1."* |
| **21.6**, Z. 2991, Weg A | *„**Amendment vollziehen**: die neue Tabelle wird die registrierte, die alte bleibt als ERSETZT stehen, …"* | *„**Berichtigung vollziehen**: die neue Tabelle wird die registrierte, …"* — der Weg selbst ist unverändert, nur sein Name |
| **21.9**, Z. 3071–3073 | *„Das Amendment wird **einmal** vollzogen, **nach** der Berechnung der Krypto-Falten (TB-31), und umfasst dann **alle neun Bots**."* | *„Die **Berichtigung der Benchmark-Tabelle** (Sperrliste Punkt 4) wird **einmal** vollzogen, nach der Berechnung der Krypto-Falten, und umfasst dann alle neun Bots."* — die Reihenfolge-Entscheidung des Betreibers ist unberührt |
| **21.9**, Z. 3081 | *„Ein Amendment jetzt bewegte eine gesperrte Zahl, die kurz darauf erneut bewegt werden müsste"* | *„Eine Berichtigung jetzt bewegte …"* |
| **21.9**, Z. 3088 | *„Er wird mit demselben Amendment geschlossen"* | *„Er wird mit derselben Berichtigung geschlossen"* |

**Ausdrücklich unverändert und richtig:** *„Kein Amendment"* in 21.8, 21.9
(Z. 3091) und 22.7 — es hat keinen Lauf gegeben. ⚠️ **`benchmark_drawdowns.json`
selbst** steht auf der Sperrliste (Punkt 4); dass ihre Änderung **nach dem Tag**
ein Amendment wäre, bleibt richtig und ist der Grund, warum die neue Tabelle bis
zur Betreiberfreigabe **daneben** liegt.

**Im Backlog** (kein append-only-Dokument; dort ist der Wortlaut geändert, die
alte Fassung entfernt nach `DOKUMENTATIONSSTANDARD.md` Regel 9):
`T56b.3` und der Satz *„Das Amendment selbst braucht danach eine eigene
Betreiberfreigabe"* im Schlussblock von Abschnitt 2 — je Stelle mit Satz davor
und danach in `docs/ERGEBNIS_TB-66_benchmark_tagesgenau.md`, Nachweis 7.

---

### 23.7 Was diese Berichtigung ausdrücklich NICHT tut

| | |
|---|---|
| ⚠️ | **Die Sperrlisten-Änderung nicht vollzogen.** `benchmark_drawdowns.json` ist byteweise dieselbe Datei; `benchmark_drawdowns_vt.json` liegt daneben. Der Vollzug braucht die eigene Betreiberfreigabe aus 21.9 — **und die Entscheidung W oder C aus 23.3 davor**, weil bei C der Lauf wiederholt werden muss (andere `handelstage`) |
| ⚠️ | **Die Formulierungsfrage nicht entschieden.** Der Platzhalter in 23.3 ist sichtbar und bleibt, bis der Betreiber entscheidet; die Messung liegt in 23.4 |
| ⚠️ | **Registertext 3b (a), (b), (d), (e) unverändert.** Ebenso 4.2 und Sperrliste Punkt 6, die den Benchmark weiter *„point-in-time"* nennen: **die Menge bestimmt seit dem 16.09. 3b (c)**, und 3b (c) sagt jetzt, wann ein Symbol dazugehört. Der Begriff *point-in-time* bleibt richtig — tagesgenau ist die genauere Zeitauflösung desselben Prinzips |
| ⚠️ | **Kein Registertext zur ersten Falte.** Register 21.3 (b) lässt 3b (a) binden; `faltenplan.py` rechnet weiter nur 4a, `t3_supertrend` trägt deshalb weiter die leere Falte 2018 (TB-61 Befund 2). Der Median in 23.4 ist **mit** dieser Falte gerechnet — ohne sie (21.4) läge er bei −13,90 / −26,57 / −48,10 (TB-65, Tabelle C1, VT) |
| ⚠️ | **`T56b.6` nicht erledigt** (die Konstantenkopien `MINDESTTRAINING_JAHRE`, `FRUEHESTE_FALTE`); **G6/H3 aus TB-61 nicht repariert**; `docs/VORREGISTRIERUNG_S-E1_nulltest.md` nicht geändert (`K4f`) |
| ⚠️ | **`registerbericht.py` nicht angefasst** — es liest die gesperrte Datei; der neue Schlüssel `symbole_handelbar_in_falte` ist beim Vollzug nachzuziehen (23.5) |
| | **Kein Selektionslauf, kein signierter Tag, kein Zeitanker.** Der Tag bleibt der nächste Meilenstein und gehört dem Betreiber (Abschnitt 13) |

⭐ *Nachtrag TB-71, 20.09.2026: Die erste und die zweite Zeile dieser Tabelle
sind überholt — der Platzhalter in 23.3 ist gefallen, die Wahl W oder C ist
durch den Satz zur Zeitachse gegenstandslos (keine der beiden Fassungen, keine
Codeänderung, kein wiederholter Lauf); der Vollzug der Sperrlisten-Änderung
braucht nur noch die Betreiberfreigabe aus 21.9. Die vierte Zeile (die leere
Falte `t3_supertrend` 2018) ist als Berichtigung nach 21.3 (b) entschieden und
wird in TB-72 vollzogen (`FABLE_ANTWORT_2026-09-20c_kapitalpfad.md`, Teil 2).
Die Bewertungsachse des Bot-Drawdowns, die 23 nicht behandelt, steht in
Abschnitt 24.*

> ⚠️⚠️ **Tatsachennotiz (38.7 (d), TB-88, Messstand `8851f67`, eingetragen
> TB-89, 23.09.2026):** Der Vollzug der Sperrlisten-Änderung braucht nach 38.3
> kein Amendment (37.3) und hat seit 38.4 seine Form (ii). Fables
> Fertigkriterium „`test_vorregistrierung.py` grün" ist heute **nicht
> erreichbar**: der Test stürzt ab (`KeyError: '2017'`), nach dem simulierten
> Vollzug bleibt er **163/2** (`G6`, `H3`, beide am Faltenplan). Die fünfte
> Zeile oben („G6/H3 aus TB-61 nicht repariert") gilt fort. ⚠️ **OFFENE FRAGE
> bei Fable (Anfrage 22i), nicht entschieden.** Einzelheiten in **38.7 (d)**.

> ⭐⭐ **Die Tabelle folgt dem Plan (39.2–39.4, Fable 23a/23b, TB-94,
> 23.09.2026):** Die Sperrlisten-Änderung ist vollzogen — in Form (ii), aber
> **nicht** mit `benchmark_drawdowns_vt.json`: Nach 23a ist die Tabelle, die
> der Lauf liest, auf dem registrierten Faltenplan (33.2) gerechnet, für alle
> neun Bots, ohne Mischung; `_vt.json` trägt bei `t3_supertrend` die leere
> Falte 2018 (vierte Zeile oben). Gelesen wird die Neurechnung
> `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (`64fb2912…`),
> die `_tb72.json` in allen 9750 Blattwerten reproduziert (39.4). Erledigt sind
> damit die erste Zeile (Vollzug) und die sechste (`registerbericht.py` liest
> `symbole_handelbar_in_falte`, TB-92); aus der fünften ist `G6`/`H3` der
> eigene Planpunkt „Testannahmen folgen dem Register" (39.1, TB-95).
> `benchmark_drawdowns.json` ist byteweise dieselbe Datei (`a163c498…`).

---

### In einfacher Sprache

**Worum es ging:** Jeder Bot wird an einem Vergleichswert gemessen — einem
einfachen Korb aus den Kursen, die er handeln darf. Bisher stand im Regelwerk
nur, dass der Korb aus den Kursen besteht, die der Bot „in diesem Jahr" laden
kann. Nicht gesagt war, was mit einem Kurs geschieht, den der Bot erst am
30. Dezember laden darf: zählt er für zwei Tage oder für das ganze Jahr?

**Was entschieden ist:** Er zählt ab dem Tag, an dem der Bot ihn laden darf —
nicht rückwirkend. Fable hat das festgelegt, und zwar aus dem Satz, der schon im
Regelwerk stand: Bot und Vergleichskorb leben in derselben Menge. Ein Korb, der
ein Jahr lang etwas hält, das der Bot nicht halten durfte, ist nicht sein Korb.

**Warum das wichtig ist:** Unter der anderen Lesart wäre die Verlustgrenze in
den frühen Krypto-Jahren wirkungslos gewesen — der Korb hätte 88 % verloren,
der Bot hätte nichts gehalten, und jeder Parametersatz hätte bestanden. Und der
Bot hätte sich 88 Prozentpunkte Vorsprung anrechnen lassen, nur weil er nicht
dabei war.

**Was jetzt anders ist:** Der alte Satz bleibt stehen und ist als ersetzt
markiert; der neue steht hier. Das Programm rechnet den Korb seit heute
tagesgenau, die gesperrte Tabelle ist unberührt, die neue liegt daneben. Die
Verlustgrenzen der fünf Krypto-Bots werden dadurch **deutlich nachgiebiger** als
in der Rechnung vom Vormittag — das steht hier, obwohl es unbequem ist, und es
war nicht der Grund.

**Was offen bleibt und warum:** Eine einzige Formulierung. Fable hat geschrieben,
Tage ohne handelbaren Kurs sollen „Rendite 0 tragen"; das Programm lässt sie
stattdessen weg. Für die Verlustzahlen ist das gleichwertig — gemessen, nicht
vermutet —, für die Angabe, wie viele Handelstage ein Jahr hatte, nicht. Im
Regeltext steht an dieser Stelle ein sichtbarer Platzhalter, bis der Betreiber
gewählt hat.

*Nachgetragen in TB-66, 20.09.2026. Berichtigung: sie nennt den unpräzisen Satz,
die Festlegung, die Messung und den Ersatztext — und entfernt nichts.*

---


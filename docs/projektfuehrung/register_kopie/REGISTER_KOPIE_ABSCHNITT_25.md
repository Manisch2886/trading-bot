# REGISTER-KOPIE Abschnitt 25 (von 0–53) — Register-Z. 4585–4814 — Commit ee43f5f1339549238c0da023db7c9f324b26d28e — 2026-10-04 — Original sha256 9a2cefb77a394a0a1c87c63cb9437d5693f054e4516333f656fae97668ef71ff — KOPIE, nicht das Register

## 25. Berichtigung zu Registertext 4a und zu 21.3 (b) — die erste Falte ist eine Konjunktion, und der Plan leitet sie aus dem Trockenlauf ab (TB-72, 20.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Satz wird umgeschrieben**
— Registertext 4a bleibt in Abschnitt 15.6 stehen (dort seit heute mit der
Marke *„(a) ERSETZT durch Abschnitt 25"*), der Ersatztext 21.3 (b) bleibt in
Abschnitt 21 stehen (Marke *„(b) ERSETZT durch Abschnitt 25"*), die
Tatsachennotiz 21.4 bleibt unverändert gültig. Das ist die Form aus
`docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md`, Regel 4, und die Form der
Abschnitte 21, 23 und 24.

**Anlass:** Zwei Implementierungen derselben Frage liefen auseinander, und eine
davon war die registrierte Regel. `research/vorregistrierung/faltenplan.py`
rechnete die erste Falte allein nach 4a nach und sagte in seinem Modulkopf
selbst, dass es 21.3 (b) nicht umsetzt (25.1). Fables vierte Antwort vom
20.09.2026 (`FABLE_ANTWORT_2026-09-20d_mtm_messung.md`, Abschnitt 2) entschied
beides: die Berichtigung für `t3_supertrend` (die *Instanz*) und die Ableitung
des Plans aus dem Trockenlauf (die *Schliessung der Klasse*) — *„dieselbe
Berichtigung, zwei Notizen, ein Vorgang"*. Die Messung in Schritt 1 von TB-72
(`docs/ERGEBNIS_TB-72_schritt1_erste_falte.md`) hat den Auftrag angehalten:
das Auseinanderlaufen war nicht einseitig. Fables fünfte Antwort vom 20.09.2026,
19:54 (`FABLE_ANTWORT_2026-09-20e_konjunktion.md`) nimmt seinen Vorschlag
zurück und fasst 4a und 21.3 (b) als **Konjunktion** neu (25.3). Umsetzung
`docs/auftraege/MAC_TB-72_erste_falte_aus_trockenlauf.md`, Ergebnis
`docs/ERGEBNIS_TB-72_erste_falte_aus_trockenlauf.md`.

**Art der Änderung nach der Drei-Kategorien-Regel (F17): eine Berichtigung mit
Ersatztext.** Fable, wörtlich: *„21.3 (b) ist registrierte Regel … Plan an
registrierte Regel: `t3_supertrend` beginnt 2019, sieben Falten. … Dass die
Richtung diesmal zugunsten des Bots geht, ändert an der Kategorie nichts — die
Quelle des Grundes ist die Regel."* ⚠️ **Die Wirkung ist bekannt und geht
zugunsten des Bots** — `DD_Toleranz` von `t3_supertrend` wird nachgiebiger
(25.4). **Sie ist nicht der Grund.** Es hat kein Selektionslauf stattgefunden;
kein Parametersatz ist bewertet, kein Ergebnis erzeugt.

---

### 25.1 Der Befund — zwei Rechenwege, eine Regel, kein Code

| | |
|---|---|
| **Registertext 4a** (15.6) | erste Falte = erstes Kalenderjahr, in dem am 1. Januar Daten für Universum und Indikator-Vorlauf vorliegen. `faltenplan.py::erste_falte` rechnete das aus der Datenlage nach (`erste_falte_quelle`: *„Datenlage nach Registertext 4a … keine Konstante"*) |
| **Registertext 3b (a)** (16.7) | eine Falte zählt, wenn der Loader des Bots in ihr mindestens ein Symbol an mindestens einem Handelstag handelbar macht — über den Trockenlauf des Laufcodes (TB-40) |
| **Register 21.3 (b)** | ergeben beide verschiedene erste Falten, bindet 3b (a) |
| ⛔ **Gemessen: kein Code setzte 21.3 (b) um** | `faltenplan.py`, Modulkopf Z. 38–42 im Stand `7b73584`, wörtlich: *„⚠️ Diese Regel ist Registertext 4a allein. Register 21.3 (b) laesst bei Abweichung 3b (a) binden (Trockenlauf des Laufcodes); das rechnet dieses Modul nicht, und fuer `t3_supertrend` weichen beide ab (4a: 2018, 3b (a): 2019, weil `MIN_HISTORY_DAYS = 730` in der Falte 2018 kein Symbol handelbar macht)"* |
| **Die Folge** | `benchmark_drawdowns_vt.json` führte für `t3_supertrend` eine Selektionsfalte **2018 mit 0 Symbolen und 0 Handelstagen** (Drawdown 0,00 auf allen 100 Stufen), und der Median `DD_Toleranz` war mit ihr gerechnet. ⚠️ **Register 21.4 sagte für denselben Bot seit TB-56b „2019, 7 Falten"** — der Code hinkte der eigenen Tatsachennotiz hinterher |

**Was Schritt 1 dazu gemessen hat** (`ERGEBNIS_TB-72_schritt1_erste_falte.md`,
Trockenlauf des Laufcodes in beide Richtungen, zwei Anläufe byteweise gleich,
zweite Methode `loader_lesart` 9/9): 4a und 3b (a) laufen bei **sechs** Bots
auseinander — `t3_supertrend` **später** (2018 → 2019), `rsi2_crypto`
**früher** (2019 → 2018, `H = 2`), die vier Aktien-Bots **früher** (2017/2018 →
**1967**, `H = 16`). 21.3 (b) *„bindet 3b (a)"* hatte keine Richtung; seine
Begründung deckte nur die leere Falte. Wörtlich umgesetzt hätte die Ableitung
vier Aktien-Bots Selektionsfalten ab 1967 gegeben. **Das war nicht gemeint, und
es war nicht von der ausführenden Sitzung zu entscheiden** — deshalb der Halt
und die Anfrage an Fable.

---

### 25.2 Die Instanz — `t3_supertrend` beginnt 2019

| | vorher (Plan nach 4a allein) | nachher (25.3) |
|---|---|---|
| erste Falte | 2018 | **2019** |
| Selektionsfalten | 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 (**8**) | 2019, 2020, 2021, 2022, 2023, 2024, 2025 (**7**) |
| Bestätigungsperiode | 2026 (ab 2026-01-01) | 2026 — unverändert |
| Falte 2018 | Selektionsfalte, `H = 0` (Trockenlauf), 0 Handelstage, Benchmark-Drawdown 0,00 | **entfällt** — sie erfüllt Bedingung (ii) nicht |
| Zulassung nach 4b | erfüllt (8 ≥ 3) | erfüllt (7 ≥ 3) |

Gemessen: `H` je 4a-Kandidatenfalte **0** / 3 / 6 / 9 / 13 / 13 / 13 / 17 / 18
(2018 … 2026; `docs/belege/TB-72/schritt1_erste_falte_trockenlauf.txt`,
bestätigt im Test `research/faltenplan_neun/test_erste_falte_trockenlauf.py`
durch einen eigenen Aufruf von `universum_trockenlauf.messe_bot`). BTC und ETH
(Daten ab 2017-08-17) erreichen `MIN_HISTORY_DAYS = 730` am 2019-08-17. **Die
Zeile in 21.4 war schon richtig; der Plan folgt ihr jetzt.** Bei den acht
anderen Bots ändert sich nichts (25.4, Gegenprobe) — bei ihnen liegt (ii) nicht
später als (i).

⭐ **`rsi2_crypto` bleibt 2019**, an der Konjunktion nachgemessen
(`docs/belege/TB-72/schritt2_rsi2_crypto_bedingung_i.txt`): (ii) ist 2018
erfüllt (`H = 2`, BTC/ETH ab 2018-12-30), **(i) nicht** — 150 Tagesbalken
Vorlauf am 1. Januar 2018 brauchen Daten ab August 2017, BTC/ETH beginnen am
17.08.2017 und haben bis zum 31.12.2017 **137** Balken; der 150. Balken liegt am
**2018-01-14**. Fables Nachrechnung trifft.

> ⭐ **25.2 BERICHTIGT durch R62 (51.7) und R65 (52.3)** (Fable 01a R62, Unterpunkt (a), und Fable 02a R65, Unterpunkt (c), TB-130, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **25.2 ERGÄNZT durch R53 (49.1)** (Fable 30a R53, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

---

### 25.3 Der Ersatztext — die Schliessung der Klasse

**Fables Wortlaut, zeichengleich übernommen** (`FABLE_ANTWORT_2026-09-20e_konjunktion.md`, Abschnitt (1)) —
**ersetzt Registertext 4a in 15.6 und den Ersatztext 21.3 (b); beide bleiben
als ersetzt stehen:**

> **Registertext 4a / 21.3 (b), Neufassung als ein Satz.** Ein Kalenderjahr ist
> Selektionsfalte eines Bots, wenn (i) es im registrierten Datenhorizont des
> Bots liegt und am 1. Januar der Indikator-Vorlauf erfüllt ist, **und** (ii)
> der Loader des Bots in ihm an mindestens einem Handelstag mindestens ein
> Symbol handelbar macht (Trockenlauf, 3b (b)). Die erste Selektionsfalte ist
> das erste Jahr, das beide Bedingungen erfüllt.
>
> ⭐ **(i) „im registrierten Datenhorizont des Bots" PRÄZISIERT durch Abschnitt 26 (TB-77, 21.09.2026), 26.2 — der Wortlaut bleibt stehen.** Der Horizont ist ein absolutes Datum je Bot (`asof` minus `RECENT_YEARS_ONLY`), nicht je Symbol; sein Wert ist ein Platzhalter, bis `asof` gesetzt ist (26.3).

> ⭐ **4a (i) in 25.3 PRÄZISIERT durch R53 (49.1)** (Fable 30a R53, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **25.3 (i) ERGÄNZT durch R58 (51.3)** (Fable 01a R58, TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Herkunft — seine Rücknahme, wörtlich:** *„‚Der Plan bezieht die erste Falte
aus dem Trockenlauf' hätte den Aktien-Bots 1967 gegeben. Ich hatte den
Mechanismus als einseitig angenommen (der Loader verschiebt nach hinten) und
nicht bedacht, dass der Trockenlauf gegen den ganzen Kursbestand misst — und
der reicht bei yfinance bis 1962. Die Messung in beide Richtungen war die
richtige Reihenfolge; zurückgenommen."* Und warum die Konjunktion stärker ist
als die vorgelegte Lesart `max(4a, 3b (a))`: *„Damit kann (ii) den Beginn nie
vorziehen, weil (i) weiter gelten muss — und (i) kann ihn nie vorziehen, weil
(ii) weiter gelten muss. 21.3 (b) ist der Sonderfall, in dem (ii) später liegt;
seine Begründung beschreibt genau diesen Fall und keinen anderen."* Und: *„Es
gibt keine Lesart, in der 3b (a) allein bindet; sie war nie gemeint, und sie ist
nach der Neufassung auch nicht mehr formulierbar."*

**Was der Code seit heute tut — Tatsachennotiz** (Commit `e7a4108`, 20.09.2026):

| | |
|---|---|
| `research/vorregistrierung/faltenplan.py::erste_falte` | ist die Konjunktion: Kandidaten sind die Kalenderjahr-Falten ab `erste_falte_4a` (Bedingung (i), bisher `erste_falte`, Rechnung unverändert: Datenlage über `faltenplan_neun`, keine Konstante) bis zum Go-Live-Schnitt; die erste Kandidatenfalte, in der der Loader mindestens ein Symbol handelbar macht, ist die erste Falte |
| Bedingung (ii) | **gemessen, nicht nachgerechnet**: `research/faltenplan_neun/erste_falte_trockenlauf.py::erste_falte_nach_3b` ruft den Loader des Bots im Kindprozess des TB-40-Werkzeugs (`universum_trockenlauf.messe_bot`, mit Schreibschutz) am letzten Zeitpunkt der Falte auf (Lesart H, 16.2). `MIN_HISTORY_*` steht nirgends im Plan — es wirkt im Bot-Code, im Kindprozess (`T56b.6`: keine Konstantenkopie) |
| Bedingung (i) | **bleibt, wie der Plan sie heute rechnet** — Fables Präzisierung (*„im Datenhorizont" = `asof` minus `RECENT_YEARS_ONLY`*) und der Befund *je Symbol gegen je Markt* sind **TB-74** und nicht Gegenstand dieser Berichtigung. Für `t3_supertrend` ändert die Präzisierung nichts |
| Der Plan | trägt je Bot neu `erste_falte_4a` und `erste_falte_trockenlauf_H` (die Menge H je geprüfter Kandidatenfalte) — damit steht im Plan, **warum** er dort beginnt; `erste_falte_quelle` nennt die Neufassung |
| `ergebnisse/faltenplan_tb72.json` | der neue Plan, **daneben**; `faltenplan.json` (`0e54ac5c…`) unberührt — die Datei ist TB-30a-Stand (`K4k`) |
| Der Test | `research/faltenplan_neun/test_erste_falte_trockenlauf.py`, 50/50: neun Zahlen Plan = Trockenlauf (eigener `messe_bot`-Aufruf) = Register 21.4; erste Falte ≥ 4a; Mutationsprobe im eigenen Prozess (4a-Nachrechnung statt Ableitung → `t3_supertrend` 2018, rot). Fable: er ist *„nicht mehr eine Wache gegen Abweichung, sondern der Nachweis, dass die Ableitung nicht regrediert"* — so steht es in seinem Docstring |

⭐ *Fables Schluss zum Plan: „(i) ist keine Nachrechnung des Loaders, sondern
Arithmetik auf registrierten Konstanten; (ii) kommt aus dem Trockenlauf und
wird nicht nachgerechnet. Der Plan führt beide in einer Funktion zusammen — eure
Form — und kann in keiner Richtung verfehlen, weil er nichts selbst misst."*

---

### 25.4 Die Wirkung — gemessen und bekannt

**Lauf:** `research/vorregistrierung/benchmark.py --ziel ergebnisse/benchmark_drawdowns_tb72.json`
(Commit `27c58a2`, 20.09.2026, 20:29–20:31 Ortszeit, `trading-env` 3.9.6, `rc 0`),
Ergebnis **daneben**. `benchmark_drawdowns.json` (`a163c498…36d1ee`) und
`benchmark_drawdowns_vt.json` (`4549395f…8745d`) **byteweise unverändert**,
vorher wie nachher gemessen (`docs/belege/TB-72/nachweis3_sha256_*`).

**Gegenprobe der acht anderen Bots** (`docs/belege/TB-72/schritt4_gegenprobe_vt.txt`):
gegen `_vt.json` **zeichengleich** — 69 Falten × 100 Stufen = **6 900** Stufen,
`handelstage` und Symbolzahl je Falte, `handelbar_ab`, `DD_Toleranz` 8 × 100;
`json.dumps(sort_keys=True)` je Bot identisch. **Genau ein Bot ändert sich.**

**`t3_supertrend`** — Falten 2019 bis 2026 auf allen 100 Stufen gleich wie in
`_vt.json`; die Falte 2018 (0 Tage, 0 Symbole, 0,00) entfällt; der Median
`DD_Toleranz` über die Selektionsfalten:

| Exposure | `_vt.json` (mit 2018) | **`_tb72.json` (ohne 2018)** | Erwartung TB-65, Tabelle C1 *„ohne 2018"* |
|---|---|---|---|
| 25 % | −12,89 | **−13,90** | −13,90 ✅ |
| 50 % | −24,73 | **−26,57** | −26,57 ✅ |
| 100 % | −45,16 | **−48,10** | −48,10 ✅ |

**100 von 100 Stufen** verschieden; die Erwartung aus TB-65 trifft auf allen
drei ausgewiesenen Stufen.

⚠️ **`DD_Toleranz` wird damit nachgiebiger** — die Grenze, die ein
Parametersatz von `t3_supertrend` einhalten muss, liegt tiefer, weil der Median
nicht mehr eine Falte mit Drawdown 0,00 enthält. **Die Richtung geht zugunsten
des Bots, und das ändert an der Kategorie nichts: die Quelle des Grundes ist
die Regel** (F17; Fable wörtlich, siehe Kopf). Die Regel stand fest, bevor die
Zahl gerechnet wurde — in 21.3 (b) seit dem 19.09., in 21.4 mit genau dieser
Zeile, und in Fables Antwort (d), die *„Wirkung bekannt"* schreibt, bevor sie
den Vollzug anordnet.

---

### 25.5 Was diese Berichtigung ausdrücklich NICHT tut

| | |
|---|---|
| ⛔ | **Die Sperrlisten-Änderung nicht vollzogen** — `benchmark_drawdowns.json` und `benchmark_drawdowns_vt.json` sind byteweise dieselben Dateien, die neue Tabelle heisst `benchmark_drawdowns_tb72.json` und liegt daneben. Der Vollzug braucht die eigene Betreiberfreigabe aus 21.9 |
| ⛔ | **Den Tag nicht gesetzt.** Kein Selektionslauf, kein signierter Tag, kein Zeitanker |
| ⛔ | **`faltenplan.json` nicht überschrieben** (`0e54ac5c…`); der neue Plan heisst `faltenplan_tb72.json` |
| ⛔ | **Die MtM-Wirkung nicht gemessen** — TB-73, nach 24.3 |
| ⚠️ | **Bedingung (i) nicht präzisiert** — *„Datenhorizont"*, `RECENT_YEARS_ONLY = 10` als Datenuhr, `entry_cutoff` je Symbol gegen `fensteranker` je Markt: **TB-74** (Fables Antwort (3) und der dritte Befund). Bis dahin rechnet der Plan (i) wie bisher |
| ⚠️ | **`auswertung.py` eingefroren** (15.8 Nr. 3); die vier gesperrten Rechenfunktionen in `benchmark.py` unverändert; `T56b.6` (`registerdaten.MINDESTTRAINING_JAHRE`), G6/H3 aus TB-61, `registerbericht.py:178` (23.5) unverändert offen |

---

### In einfacher Sprache

**Was schiefstand:** Das Regelwerk sagt seit dem 19.09., wann das erste Jahr
eines Bots zählt — sobald sein Programm wenigstens einen Kurs überhaupt handeln
darf. Das Programm, das den Plan schreibt, rechnete das aber auf einem zweiten,
eigenen Weg nach und sagte in seinem eigenen Kopf, dass es die Regel nicht
anwendet. Bei einem Bot kamen beide Wege zu verschiedenen Ergebnissen: Er führte
ein Jahr, in dem er gar nichts handeln konnte.

**Was gemessen wurde, bevor etwas geändert wurde:** Ob es wirklich nur ein Bot
ist. In der erwarteten Richtung ja. In der anderen Richtung — das Programm dürfte
früher handeln, als das Regelwerk meint — sind es fünf Bots, vier davon ab 1967.
Das war nicht gemeint. Fable hat seinen eigenen Vorschlag daraufhin
zurückgenommen und die Regel neu gefasst: Ein Jahr zählt nur, wenn **beide**
Bedingungen gelten — die Datenlage **und** das Programm. Dann kann keine der
beiden den Beginn nach vorn ziehen.

**Was jetzt anders ist:** Der eine Bot beginnt 2019 statt 2018, mit sieben
Jahren statt acht. Und der zweite Rechenweg ist abgeschafft: Der Plan fragt das
Programm, was es kann, statt es nachzurechnen. Die beiden können nicht mehr
auseinanderlaufen; ein Test beweist das, indem er die alte Rechnung künstlich
wieder einsetzt und dabei rot wird.

**Was sich an Zahlen ändert:** Die Verlustgrenze dieses einen Bots wird etwas
weiter — von −45,2 auf −48,1 Prozent bei voller Investition. Das ist die
Wirkung, nicht der Grund; der Grund ist die Regel, und die stand vorher fest.
Die gesperrten Tabellen sind unberührt, die neue liegt daneben, und ob sie die
gesperrte ablöst, entscheidet der Betreiber.

*Nachgetragen in TB-72, 20.09.2026. Berichtigung mit Ersatztext: sie nennt den
Befund, die Instanz, den Ersatztext mit seiner Herkunft, die gemessene Wirkung
und das, was nicht getan wird — und entfernt nichts.*

---


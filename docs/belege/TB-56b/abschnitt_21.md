
---

## 21. Berichtigung zu Registertext 4 — die Faltenschranke (TB-56b, 19.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Satz wird umgeschrieben —
der berichtigte Satz bleibt in Abschnitt 15.6 stehen** und wird hier wörtlich
zitiert, gefolgt von der Messung und dem Ersatztext. Das ist die Form aus
`docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md`, Regel 4, und dieselbe Form,
in der die Abschnitte 18 bis 20 angehängt wurden.

**Anlass:** `docs/ERGEBNIS_TB-56_faltenschranke.md` hat gemessen und die Schranke
aus dem Code entfernt, ausdrücklich **ohne** einen Registertext anzufassen. Die
Berichtigung war als eigene Aufgabe angekündigt; dies ist sie.

**Art der Änderung nach der Drei-Kategorien-Regel (F17): eine Berichtigung.**
Der Grund stammt aus einer Messung an der Datenlage (TB-56, Teil A, rein lesend,
**vor** jeder Änderung am Code), nicht aus der Kenntnis eines Selektionsergebnisses
— es hat kein Selektionslauf stattgefunden. *„Die Grenze zwischen Berichtigung und
nachträglicher Wahl ist nicht die Zeit, sondern die Quelle des Grundes."*

---

### 21.1 Der berichtigte Satz, wörtlich

Aus **Abschnitt 15.6**, Punkt 2 der vier Punkte, die die Faltentabelle tragen:

> **Die erste Falte ist 2019, und die Schranke dafür ist das Register, nicht
> die Datenlage.** `ERSTE_MOEGLICHE_FALTE = 2019` gilt unverändert. Ohne diese
> Schranke begänne der Plan bei acht der neun Bots schon 2017 oder 2018 —
> Bitcoin-Daten reichen bis 2017-08-17 zurück. Nur bei `rsi2_crypto` bindet die
> Datenlage selbst (150 Tagesbalken Vorlauf, erst ab 2019 erfüllt); bei den
> anderen acht bindet die Registerschranke.

⚠️ **Was daran falsch ist — und was ausdrücklich nicht.** Der Satz beschreibt
richtig, **dass** eine Schranke wirkte, und er sagt richtig voraus, **dass** der
Plan ohne sie früher begänne; beides hat TB-56 bestätigt. Falsch ist seine
**Gegenwartsform und seine Begründung**:

| | |
|---|---|
| ⚠️ **Gegenwartsform** | `ERSTE_MOEGLICHE_FALTE` ist seit Commit `7387cc5` (19.09.2026, 18:58 UTC) aus `research/vorregistrierung/registerdaten.py` entfernt. Der Satz behauptet eine Schranke, die es im Code nicht mehr gibt |
| ⚠️⚠️ **Begründung** | *„die Schranke dafür ist das Register"* — **gemessen: kein Registertext nennt eine Jahreszahl.** Registertext 4a (Abschnitt 15.6) sagt *„vom ersten Jahr, in dem am 1. Januar Daten für Universum und Indikator-Vorlauf vorliegen"*, Registertext 3b (a) (Abschnitt 16.7) sagt *„ab einem handelbaren Symbol"*. Die Zahl 2019 stand **nur im Code und in diesem Begründungssatz** |

⭐ **Damit trug die Faltentabelle in 15.6 eine Begründung, die auf sich selbst
zeigte.** Das ist die Fehlerklasse, gegen die Prüfprinzip C4 geschrieben ist:
eine Angabe, die nicht sagt, gegen **was** sie prüft.

---

### 21.2 Die Messung, auf der die Berichtigung ruht

**Fundstelle:** `docs/ERGEBNIS_TB-56_faltenschranke.md`, Teil A (Messung
18:11–18:15 UTC am 19.09.2026), Werkzeug
`research/faltenplan_neun/faltenschranke_messung.py`. Die Schranke wurde **im
Speicher** ausgeschaltet, die Datei auf der Platte blieb unverändert; vorab wurde
geprüft, dass das Werkzeug **mit** Schranke denselben Plan liefert wie die
festgehaltene Messung `daten/faltenplan.json` — **9/9 gleich**. Ohne diese
Kontrolle hätte die Messung ein anderes Werkzeug gemessen als das, das die
Tatsachennotiz erzeugt hat.

| | gemessen |
|---|---|
| Schranke bindet bei | **8 von 9** Bots |
| Faltenzahl ändert sich bei | **8 von 9** |
| Bestätigungsperiode ändert sich bei | **1** (`elliott_wave`) |
| ⭐ **Zulassung nach Registertext 4b ändert sich bei** | **keinem** — alle neun erreichen die Mindestzahl 3 vorher wie nachher |
| Frühestes Datum in den Krypto-Daten | **2017-08-17** (BTC/ETH) |
| H-Reihen ab 2019 | **zeichengleich mit der Tatsachennotiz 16.1.1** — derselbe Trockenlauf misst dasselbe wie damals, nur mit den frühen Falten davor |

---

### 21.3 Der Ersatztext

> **Berichtigung zu Abschnitt 15.6, Punkt 2 (19.09.2026).**
>
> **(a)** Die erste Selektionsfalte je Bot folgt **allein aus Registertext 4a
> und Registertext 3b (a)**. Es gibt **keine Registerschranke auf ein
> Kalenderjahr.** Die frühere Konstante `ERSTE_MOEGLICHE_FALTE = 2019` war eine
> Festlegung im Code **ohne Entsprechung in einem Registertext**; sie ist mit
> Commit `7387cc5` entfernt.
>
> **(b)** Ergeben 4a und 3b (a) für einen Bot **verschiedene** erste Falten,
> bindet **3b (a)**. *Begründung: Eine Falte, in der der Loader kein Symbol
> handelbar macht, erzeugt keinen Trade und damit keinen Falten-Sharpe; sie
> könnte zum Faltenmedian nichts beitragen. Die Begründung folgt aus der
> Struktur des Selektionsmasses, nicht aus einem erwarteten Ergebnis.*
> *(Betreiberentscheidung 19.09.2026, auf Entscheidungsvorlage mit gemessenen
> Zahlen und benannter Empfehlung.)*
>
> **(c)** Die erste Falte ist damit **je Bot verschieden** und hängt am
> Indikator-Vorlauf und an `MIN_HISTORY_*` des jeweiligen Loaders. Die Aussage
> *„alle Bots eines Marktes teilen einen Faltenplan"* gilt **nicht mehr**;
> siehe 21.5.

---

### 21.4 Die berichtigte Faltenliste — Tatsachennotiz zu 4d

⚠️ **Diese Tabelle ersetzt die Tatsachennotiz-Tabelle in Abschnitt 15.6.** Die
dortige Tabelle bleibt stehen und gilt als **ERSETZT**; sie wird nicht entfernt.

Erste Falte und Faltenzahl nach **3b (a)** (Trockenlauf des Laufcodes, Spalte „H"
in TB-56 Teil A). Bestätigungsperiode unverändert bis `2026-09-01`,
ausschliesslich (Abschnitt 5.2).

| Bot | Markt | Faltenlänge | erste Falte | # Selektionsfalten | Bestätigung ab | 4b erfüllt |
|---|---|---:|---:|---:|---|---|
| `elliott_wave` | krypto | 2 J | **2018–2019** | **4** | ⚠️ **2026-01-01** | ja |
| `t3_supertrend` | krypto | 1 J | **2019** | **7** | 2026-01-01 | ja |
| `rsi2_crypto` | krypto | 1 J | 2019 | 7 | 2026-01-01 | ja |
| `turtle_soup_crypto` | krypto | 1 J | **2018** | **8** | 2026-01-01 | ja |
| `volatility_breakout_crypto` | krypto | 1 J | **2018** | **8** | 2026-01-01 | ja |
| `elliott_wave_stocks` | aktien | 1 J | **2017** | **9** | 2026-01-01 | ja |
| `rsi2_mean_reversion` | aktien | 1 J | **2018** | **8** | 2026-01-01 | ja |
| `turtle_soup_stocks` | aktien | 1 J | **2017** | **9** | 2026-01-01 | ja |
| `volatility_breakout` | aktien | 1 J | **2018** | **8** | 2026-01-01 | ja |

⭐ **`t3_supertrend` steht unverändert bei 2019 und 7 Falten.** Nach 4a begänne
sein Plan 2018; sein Loader verlangt jedoch `MIN_HISTORY_DAYS = 730`, und BTC/ETH
(Daten ab 2017-08-17) erreichen das erst am **2019-08-17** — in der Falte 2018
macht er **kein** Symbol handelbar (Trockenlauf: 0 Symbole). Nach (b) bindet
3b (a); seine Zeile bleibt, wie sie war. **Die Berichtigung ändert für diesen Bot
nichts ausser der Begründung.**

⚠️ **Die dünnste Falte des ganzen Plans**, ausdrücklich benannt, damit sie
niemand für einen Fehler hält: `turtle_soup_crypto` und
`volatility_breakout_crypto` haben in der Falte **2018 zwei Symbole an zwei
Tagen** — BTC und ETH werden am **2018-12-30** handelbar (2017-08-17 + 500 Tage).
Nach 3b (a) („an mindestens einem Handelstag") zählt die Falte. **Eine
Mindest-Symbolzahl wird ausdrücklich nicht eingeführt**; Fable hat sie am
16.09.2026 als *„die Schranke durch die Hintertür"* verworfen (Registertext 3b,
Ergänzung (a), Abschnitt 16.7), und sie träfe genau die frühen Falten, die als
einzige eine Bärenmarkt-Vorgeschichte haben. Registertext 3b (d)
(Faltenkohärenz) misst die Folge **nach** dem Lauf, ohne dass vorher jemand eine
Falte für unwürdig erklärt.

---

### 21.5 Was sich dadurch ändert — vollständig, auch das Unangenehme

| | Änderung | ⚠️ |
|---|---|---|
| **Zulassung nach 4b** | **keine** — alle neun erreichen die Mindestzahl 3 vorher wie nachher | der Grund, warum diese Berichtigung keine Auswahl trifft |
| ⚠️ **Bestätigungsperiode `elliott_wave`** | **2025-01-01 → 2026-01-01**, also **12 Monate kürzer** | Folge der Doppeljahr-Parität. **Berichtet, nicht als Grund benutzt** — eine kürzere Bestätigungsperiode ist ein Nachteil, und ihn zum Argument für die alte Schranke zu machen hiesse, das Register nach erwartetem Effekt zu schreiben |
| ⚠️⚠️ **Die vier Aktien-Bots teilen keinen Faltenplan mehr** | `elliott_wave_stocks` und `turtle_soup_stocks` beginnen **2017**, `rsi2_mean_reversion` und `volatility_breakout` **2018** | Abschnitt 3 sagt heute: *„gilt für alle Bots dieses Marktes mit gleichem Faltenplan"* und dreimal *„teilt Universum und Faltenplan mit den übrigen aktien-Bots — dieselbe Tabelle"*. **Diese Prämisse trägt nicht mehr.** Siehe 21.6 |
| **Krypto-Benchmark** | unverändert offen | Die Benchmark-Tabelle führt die fünf Krypto-Bots als `status: platzhalter` mit **leerer** `dd_toleranz` — gemessen in beiden Tabellenfassungen. Das hängt an TB-31 und ist **nicht** Gegenstand dieser Berichtigung, gehört aber vor den Tag |

---

### 21.6 Die Folge für Sperrliste Punkt 4 — Entscheidungsvorlage, nicht vollzogen

⚠️⚠️ **Hier wird nichts entschieden. Dieser Abschnitt legt die gemessenen Zahlen
vor; die Entscheidung gehört dem Betreiber.** Grund: `DD_Toleranz` und die vorab
berechneten Benchmark-Drawdowns stehen auf der Sperrliste (Abschnitt 10,
Punkt 4), und eine Änderung dort ist ein **Amendment** nach 10.1.

**Was TB-56 getan hat (Betreiberentscheidung 19.09.2026, Option a):** die neu
gerechnete Tabelle liegt als **eigene Datei** daneben
(`research/vorregistrierung/ergebnisse/benchmark_drawdowns_ohne_schranke.json`);
die gesperrte Datei ist **byteweise unverändert** — gemessen: SHA-256
`a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee`, letzte
Änderung 14.09.2026, letzter Commit `a2fcf01` (TB-30a). `test_vorregistrierung.py`
ist seither rot, geführt als **„offen durch eigene Änderung — blockierend für den
Tag"**, ausdrücklich **nicht** als „bekannt rot".

**Die gemessene Differenz**, gerechnet über beide JSON-Dateien:

| Bot | Selektionsfalten alt → neu | `DD_Toleranz` |
|---|---|---|
| `elliott_wave_stocks` | 2019–2025 (7) → **2017–2025 (9)** | **unverändert** |
| `turtle_soup_stocks` | 2019–2025 (7) → **2017–2025 (9)** | **unverändert** |
| ⚠️ `rsi2_mean_reversion` | 2019–2025 (7) → **2018–2025 (8)** | **ändert sich auf allen 100 Exposure-Stufen** |
| ⚠️ `volatility_breakout` | 2019–2025 (7) → **2018–2025 (8)** | **ändert sich auf allen 100 Exposure-Stufen** |

**Die Richtung, unbequem und deshalb zuerst genannt:** Die Toleranz wird bei
beiden Bots **tiefer, also nachgiebiger**.

| Exposure-Stufe | gesperrt | neu | Delta |
|---:|---:|---:|---:|
| 25 % | −2,18 | −3,35 | **−1,17** |
| 50 % | −4,33 | −6,61 | **−2,28** |
| 100 % | −8,55 | −12,89 | **−4,34** |

⚠️⚠️ **Das ist eine Lockerung einer Zulassungsschranke, und sie muss als solche
entschieden werden.** Der Grund dafür ist **strukturell** — 2018 war für den
Aktien-Benchmark ein schlechtes Jahr und zieht den Median nach unten —, und er
darf **nicht** damit begründet werden, dass eine nachgiebigere Schranke mehr
Parametersätze durchlässt. *Warum die beiden anderen Aktien-Bots unverändert
bleiben, ist **erschlossen, nicht gemessen**: sie gewinnen zwei Falten (7 → 9),
und der Median sitzt danach zwischen denselben beiden Werten; die anderen beiden
gewinnen eine (7 → 8), und der Median wird zum Mittel aus zwei anderen.*

**Die drei Wege, mit dem Preis jedes einzelnen:**

| | Weg | Preis |
|---|---|---|
| ⭐ **A** *(Empfehlung)* | **Amendment vollziehen**: die neue Tabelle wird die registrierte, die alte bleibt als ERSETZT stehen, `benchmark_drawdowns.json` wird **nicht** überschrieben, sondern der Registertext verweist auf die neue Datei | Eine gesperrte Zahl ändert sich vor dem Tag. **Kein Lauf ist davon berührt** — es hat keinen gegeben, also beginnt auch keiner von vorn (10.1 greift ins Leere). Der Preis ist Aufmerksamkeit, nicht Evidenz |
| **B** | **Alte Tabelle behalten**, Faltenliste berichtigen, Benchmark auf dem alten Stand lassen | ⚠️ **Widerspruch bleibt bestehen**, nur an anderer Stelle: der Plan kennt 2017/2018, die Benchmark-Tabelle nicht — und `test_vorregistrierung.py` bliebe dauerhaft rot. **Ein dauerhaft roter Test ist keine Wache** (Prüfprinzip A4) |
| **C** | **An Fable** | Kostet eine Runde. Inhaltlich ist es dieselbe Frage wie seine Frage 2 aus der laufenden Anfrage, nur vor dem Tag statt danach |

**Warum A empfohlen wird, und was daran schlechter ist als an B:** A stellt die
Übereinstimmung zwischen Register und Rechnung wieder her und lässt den Prüfer
wieder beissen. Schlechter ist A darin, dass eine Zahl der Sperrliste sich
bewegt, **bevor** der Tag sie einfriert — und wer das einmal tut, hat den Vorgang
normalisiert. ⚠️ **Genau deshalb steht hier eine Vorlage und keine Ausführung.**

---

### 21.7 Prüfung der Abschnitte 18 und 20 gegen den Tatsachennotiz-Test

**Der Test, wörtlich (Fable):** *„Eine Tatsachennotiz hält fest, sie schafft
nicht."* Jeder Satz ist Messwert mit Herkunft oder Verweis.

| Abschnitt | Prüfung | Ergebnis |
|---|---|---|
| **18** (Snapshot, TB-55) | Jede Zahl der Tabelle nennt ihr Feld im `MANIFEST.json` und ist „gelesen, nicht abgeschrieben". Der Name wurde **viermal unabhängig** gerechnet. Die Abgrenzung gegen `4fee547d…` steht im Abschnitt selbst. Der Schlussabsatz nennt ausdrücklich, was die Notiz **nicht** tut | ⭐ **besteht** |
| **20** (Lock, TB-58b) | SHA-256 zweimal unabhängig gerechnet; jede Tabellenzeile mit Messung hinterlegt; die Probe-Tabelle führt fünf Zustände mit Rückgabewert und Meldung; Schlussabsatz nennt die Grenzen | ⭐ **besteht** |

⚠️ **Ein Befund an der Form, kein Fehler an den Zahlen:** Beide Abschnitte sind
mit *„in der Form von Abschnitt 18"* bzw. *„in der Form der Tatsachennotiz zu 4d
(Abschnitt 15.6)"* aufeinander bezogen. **Die Tatsachennotiz zu 4d in 15.6 ist
diejenige, die diese Berichtigung soeben ersetzt.** Der Formverweis bleibt
gültig — er zeigt auf die *Form*, nicht auf den *Inhalt* —, aber wer ihm folgt,
landet ab heute in einer als ERSETZT gekennzeichneten Tabelle. **Hier
festgehalten, damit der Verweis nicht stillschweigend in die Irre führt.**

---

### 21.8 Was diese Berichtigung ausdrücklich NICHT tut

| | |
|---|---|
| ⚠️ | **Kein Amendment.** Sperrliste Punkt 4 ist unberührt; `benchmark_drawdowns.json` ist byteweise dieselbe Datei. 21.6 ist eine Vorlage |
| ⚠️ | **Keine Codeänderung.** Die drei Kopien der Schranke werden hier **benannt, nicht angefasst**: `research/faltenplan_neun/faltenplan_neun.py:120` (`FRUEHESTE_FALTE = 2019`, mit einem Kommentar in Zeile 119, der auf die entfernte Konstante verweist) und `research/krypto_historie/faltenplan.py:64`. *Grund für die Reihenfolge: Das Register sagt, was der Code tun soll — also wird zuerst das Register berichtigt und danach der Code nachgezogen, mit Mac-Lauf. Umgekehrt hiesse es, den Code zum Massstab des Registers zu machen* |
| ⚠️ | **Kein Registertext 0.** Die Drei-Kategorien-Regel (F17) als allgemeine Registeranforderung einzutragen, hängt an **Fables Fragen 1 und 3** (`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-19_pruefungsregistrierung.md`), die genau entscheiden, ob das ein Registertext wird. Sie ist heute **einmal** im Register genannt (Abschnitt 19, als Einordnung einer Änderung), nicht als Regel |
| ⚠️ | **Keine Änderung an Registertext 5f.** Die Übergabe vom 19.09. nennt sie als Punkt; **gemessen: im gesamten Repo steht nirgends, worin sie bestehen soll.** Was an 5f offen war — der fehlende Lock-Hash — ist mit Abschnitt 20 geschlossen. **Bis eine Spezifikation vorliegt, wird hier nichts an 5f geändert**, statt eine zu erfinden |
| | **Kein Selektionslauf, kein signierter Tag, kein Zeitanker.** Der Tag bleibt der nächste Meilenstein und gehört dem Betreiber (Abschnitt 13) |

---

### In einfacher Sprache

**Im Regelwerk stand ein Satz, der sich selbst begründete.** Er sagte: Die
Auswertung beginnt 2019, und zwar weil das Regelwerk es so will. Nachgesehen
wurde: **Kein einziger Regeltext nennt eine Jahreszahl.** Die 2019 stand nur im
Programm — und in diesem Satz, der auf sie zeigte.

**Das Programm ist gestern korrigiert worden, der Satz bis heute nicht.** Solange
beides nebeneinandersteht, widerspricht das Programm dem Regelwerk, und niemand
kann sagen, welches von beiden gilt. Dieser Abschnitt schliesst die Lücke: Der
alte Satz bleibt stehen, damit nachvollziehbar ist, was dastand; daneben steht,
was gemessen wurde und was künftig gilt.

**Was sich praktisch ändert:** Die meisten Bots dürfen jetzt ein oder zwei Jahre
früher ausgewertet werden, weil ihre Daten so weit zurückreichen. **Kein einziger
Bot verliert dadurch seine Zulassung** — jeder hat mehr Auswertungsjahre als
vorher, nicht weniger. Ein Bot bekommt dadurch einen kürzeren Bewährungszeitraum;
das steht hier, obwohl es unangenehm ist, und es ist ausdrücklich **kein**
Argument gegen die Korrektur gewesen.

**Was offen bleibt und warum:** Zwei Bots bekämen durch das zusätzliche Jahr eine
**nachgiebigere** Verlustschranke. Eine Schranke zu lockern, nachdem man weiss,
dass sie sich lockern würde, ist genau die Art Entscheidung, die dieses Regelwerk
verhindern soll. Deshalb steht hier eine Vorlage mit Zahlen und einer Empfehlung
— entschieden wird sie vom Betreiber, nicht von mir.

*Nachgetragen in TB-56b, 19.09.2026. Berichtigung: sie nennt den falschen Satz,
die Messung und den Ersatztext — und entfernt nichts.*

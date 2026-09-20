# ERGEBNIS TB-65 — Welche Schranke gilt für den Benchmark? (Mac-Lauf, 20.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-65_benchmarkschranke_pruefen.md`. **Ausgeführt
am MacBook**, Zweig `main`, Ausgang `ff98f0a`, Interpreter
`trading-env/bin/python3` = **Python 3.9.6** (pandas 2.3.3, numpy 2.0.2),
Kursdateien `data/` = **223**. **Rein lesend am Code und am Register**: kein
Byte in `research/vorregistrierung/`, kein Registertext geändert. Gerechnet wurde
nachrichtlich in einer Wegwerf-Kopie `research/_tb65_kopie/` (zwei Ebenen unter
der Repo-Wurzel, wie TB-61), die am Ende entfernt ist. Zwei Commits: **`9ad37e4`**
(Teil 1, Frage C mit Belegen) und der Abgabe-Commit (dieses Dokument,
Journal-Nachtrag). Rohausgaben und das Rechenskript unter `docs/belege/TB-65/`.

---

## Das Ergebnis zuerst — in fünf Sätzen, jeder mit Fundstelle

1. ⭐ **Kein Registertext sieht vier Jahre Vorlauf für den Benchmark vor.**
   Gesucht mit acht Mustern (Trefferzahlen unten, auch die Nullen): Die Zahl
   „vier Jahre" steht im Register an **acht Zeilen**, und **jede** davon liegt in
   einem Block, der als **ERSETZT** gekennzeichnet ist oder einen
   Ersetzungsvermerk trägt (Abschnitt 3 Faltenplan-Block Z. 381, 5.1 Z. 537/551,
   5.3 Z. 592–608, Sperrliste 8 Z. 829–830). Der Bezeichner `MINDESTTRAINING`
   kommt im Register **nullmal** vor.
2. ⭐⭐ **Die Lesart der Chat-Sitzung trifft im Ergebnis, aber nicht in der
   Fundstelle.** Abschnitt 5.3 **allein** trägt sie nicht — hier hat die
   Gegenthese A2 recht: 5.3 regelt den Faltenplan und die Bewertungsmenge des
   Bots und nennt den Benchmark mit keinem Wort. Getragen wird die Lesart von
   **drei anderen Stellen**: Sperrliste Punkt 8 (der Halbsatz „vier Jahre Vorlauf
   je Symbol" der **Universums**-Regel ist ersetzt, Z. 830), Registertext 3b (c)
   (der Benchmark rechnet auf den **geladenen** Symbolen, Z. 1944–1947) und
   15.1 / T34.10 (*„Es gibt kein Mindesttraining … der Begriff existiert unter
   Verfahren B nicht"*, Fable 18.09.2026).
3. ⚠️ **„Verstoss" ist nicht das Wort des Registers.** Das Register führt genau
   diesen Zustand seit dem 16.09.2026 selbst — **16.11, Zeile 7**: *„3b (a)–(e) —
   Loader entscheidet, **Benchmark auf geladenen Symbolen** … Der spätere
   Auswerter tut es noch nicht"*, Schliesser **TB-30b**. Kein **registrierter**
   Zahlenwert ist berührt: die gesperrte Tabelle `a163c498…` führt die fünf
   Krypto-Bots als `platzhalter`. Berührt ist die **Vorlage**
   `benchmark_drawdowns_neu.json` aus TB-61 — und ein Amendment, das sie
   registriert, registrierte Krypto-Zahlen auf einer Menge, die kein Registertext
   vorsieht. **Insoweit trifft die Folgerung der Chat-Sitzung** (vor dem
   Amendment neu rechnen), **und TB-61s Rahmung als offene Wahl „4 behalten / 0
   / andere Regel" trifft nicht** — keine der drei Optionen ist 3b (c).
4. ⚠️⚠️ **Was das Register NICHT entscheidet — und was zahlenmässig gross ist:**
   ob ein in der Falte geladenes Symbol für die **ganze Falte** in den Benchmark
   eingeht (Fassung **VH**) oder **ab dem Tag**, an dem der Loader es lädt
   (Fassung **VT**). 3b (c) sagt „in dieser Falte geladen", Lesart H (16.2) sagt
   „an mindestens einem Handelstag" — beide Lesarten sind mit dem Wortlaut
   vereinbar. Gemessen: `t3_supertrend` bei 25 % **−16,13** (VH) gegen **−12,89**
   (VT); die Falte 2018 von `turtle_soup_crypto` **−87,92 %** (VH: BTC und ETH das
   ganze Jahr) gegen **−3,60 %** (VT: ein Handelstag, weil der Loader sie erst am
   30.12.2018 lädt).
5. ⭐ **Gemessen, Frage C:** Bei den **vier Aktien-Bots ändert sich nichts** —
   V0 (vier Jahre) und VH (geladen) sind auf allen 100 Stufen und in allen 40
   Falten **zeichengleich**, weil „vier Jahre vor dem 1. Januar" arithmetisch
   dieselbe Menge ergibt wie „1 825 Tage vor dem 31. Dezember". Bei den **fünf
   Krypto-Bots** liegt die DD_Toleranz bei 100 % Exposure je nach Fassung beim
   **2,4- bis 5,0-fachen** der TB-61-Zahl; „rund dreimal" (Chat-Sitzung) ist die
   Grössenordnung, nicht die Zahl. **Wo es beisst:** in den Falten 2019–2021 ist
   `erlaubt(f)` unter V0 gleich der DD_Toleranz (**−12,01 %** bei 100 %), unter
   VT **−72 bis −78 %** — dort handeln die Bots mit 6 bis 10 Symbolen, der
   Benchmark von TB-61 ist leer.

---

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

Leer. Ausgang `ff98f0a`, Arbeitsbaum sauber (12:38 UTC).

---

## Nachweis 2 — Frage A: Hebt Abschnitt 5.3 den point-in-time-Ausschluss auf, und für was?

**Der Vermerk, wörtlich** (`docs/VORREGISTRIERUNG_neuselektion.md`, Z. 588–594,
Commit `bbb0109`, 15.09.2026, TB-36):

> ⚠️ **ERSETZT durch Abschnitt 15 (Registernachtrag TB-36, 15.09.2026),
> Registertext 3 und 4.** … Die hier zitierte Regel („mindestens vier Jahre
> Kursdaten je Symbol", point-in-time-Ausschluss) gilt **nicht mehr** — es gibt
> kein Mindesttraining, und kein Symbol wird aus einer Falte ausgeschlossen.

**Die Regel, die er ersetzt** (5.3, Z. 601–608, Commit `a2fcf01`, 14.09.2026):
*„Erste Testfalte ist das erste volle Kalenderjahr, vor dem je Symbol mindestens
vier Jahre Kursdaten liegen, frühestens 2019. … Ein Symbol geht in eine Falte nur
ein, wenn seine Kursdaten mindestens vier Jahre vor Faltenbeginn einsetzen
(point-in-time)."*

**Was am selben Tag im selben Commit `a2fcf01` entstand:** `benchmark.py`, dessen
Kopf (Z. 48–54) die Universumsregel des Benchmarks so beschreibt: *„point-in-time:
ein Symbol geht in eine Falte nur ein, wenn seine Kursdaten mindestens
`MINDESTTRAINING_JAHRE` vor dem Faltenbeginn einsetzen"* — **derselbe Satz** wie
der letzte Satz von 5.3, mit der Konstante an der Stelle der Zahl. Die Konstante
selbst (`registerdaten.py:108`) trägt den Kommentar `# vor der ersten Falte` —
das ist die Rolle aus 5.1 Nr. 2 (Training vor der ersten Falte, Verfahren A).
**Eine Konstante, drei Rollen** am 14.09.: (i) Mindesttraining vor der ersten
Falte (5.1 Nr. 2), (ii) Mitgliedschaft je Falte für die Bewertung des Bots
(5.3, letzter Satz), (iii) Mitgliedschaft je Falte im Benchmark (`benchmark.py`,
4.2 *„gleichgewichtetes point-in-time-Universum"*, Sperrliste 6 und 8, und
wortgleich `docs/VORREGISTRIERUNG_S-E1_nulltest.md:57–59` *„dieselbe Regel wie
im Hauptregister"*).

| | Lesart | dafür spricht (Fundstelle) | dagegen spricht (Fundstelle) |
|---|---|---|---|
| **A1** | Der Satz hebt den Ausschluss **überall** auf, also auch im Benchmark | ① **Sperrliste Punkt 8** (Z. 828–832): *„Universumsdateien und point-in-time-Regel … vier Jahre Vorlauf je Symbol"* → Vermerk desselben Commits `bbb0109`: *„Der Halbsatz ‚vier Jahre Vorlauf je Symbol' ist **ersetzt** (Abschnitt 15, Registertext 3)."* Das ist die **Universums**-Regel, nicht der Faltenplan — und der Benchmark ist nach 4.2 (Z. 442–443) *„eine statische Position … im gleichgewichteten point-in-time-Universum"*. Punkt 6 (*„Benchmark-Definitionen — … point-in-time"*) nennt keine Dauer; die Dauer stand nur in Punkt 8. ② **15.1** (Z. 1082–1084): *„Es gibt **kein Mindesttraining**"* — als Folge von Verfahren B, ohne Ausnahme für den Benchmark. ③ **T34.10, Fable 18.09.2026** (`BACKLOG_ARCHIV.md:76`): *„Nicht vier Jahre, nicht zwei, nicht null als dritte Wahl — der Begriff existiert unter Verfahren B nicht. … Die vier Jahre sind ein Artefakt von Verfahren A."* ④ Die Benchmark-Regel in `benchmark.py:50–52` ist **kein eigener Registertext**, sondern die Anwendung des 5.3-Satzes; wird der Satz ersetzt, verliert die Anwendung ihren Text. ⑤ **17.3** (Z. 2283–2299): der *„beschlossene Wortlaut"* *„Die erste Selektionsfalte beginnt 2022 — reiner Vorlauf"* — 2022 ist genau das Jahr, das die Vier-Jahres-Regel liefert (2017-08-17 + 4 J.) — hält dort *„der Nachrechnung nicht stand"*: *„Nicht der Vorlauf schützt, sondern die Mindesthistorie des Loaders (Registertext 3b (a))."* | ① **Der Vermerk steht in Kapitel 5 „Der Faltenplan"**, unter der Überschrift *„Krypto: Platzhalter mit Regel"*, und ersetzt durch **Registertext 3 und 4** — Universum und Falten. Der Benchmark hat ein eigenes Kapitel (4) und eigene Sperrlistenpunkte (4, 6); **keiner davon trägt einen ERSETZT-Vermerk**. ② *„kein Symbol wird aus einer Falte ausgeschlossen"* meint Registertext 3a (Z. 1193–1197): Symbole ohne Historie tragen **0 Trades und 0 Rendite** bei. Auf einen Benchmark ist das nicht übertragbar — ein Symbol ohne Kurse kann in keinem Benchmark stehen. Der Satz ist erkennbar über die **Bewertungsmenge des Bots** geschrieben. ③ **Praxis des Registers nach dem Vermerk:** TB-56 (`benchmark_drawdowns_ohne_schranke.json`) und TB-61 (`_neu.json`) rechneten mit `benchmark.py` **unverändert** mit vier Jahren; **21.6** legt diese Zahlen als Amendment-Vorlage vor, **21.9** (Betreiber, 19.09.) entscheidet die Reihenfolge des Amendments — ohne die Vier-Jahres-Regel zu erwähnen. Niemand hat den Vermerk bis TB-61 auf den Benchmark bezogen. |
| **A2** | Er betrifft nur den **Faltenplan** (wann eine Falte beginnt) und die Bewertungsmenge des Bots, nicht die Menge, auf der der **Benchmark** rechnet | ① Ort und Überschrift (s. o.). ② Der Ersatz ist **Registertext 3 und 4** — 3a regelt *„je Selektionsfalte werden die Symbole … ausgewertet"*, 4a *„vom ersten Jahr, in dem am 1. Januar Daten … vorliegen"*; **beides Bewertung und Faltenbeginn**, kein Wort zum Benchmark. ③ 15.6 Punkt 4 (Z. 1364–1369): *„Symbole ohne Historie in einer Falte werden nicht ausgeschlossen … Berichtszahl, keine Auswahl"* — dieselbe Denkfigur, dieselbe Menge (Bot). ④ Sperrliste 6 nennt `benchmark.py` **weiter** als gesperrte Benchmark-Definition mit „point-in-time"; ⚠️ die Sperre gilt allerdings erst *„ab dem signierten Tag"* (Abschnitt 10, Z. 811) — sie schützt heute nichts. | ① **Sperrliste Punkt 8** (oben, A1 ①): die Dauer „vier Jahre" stand als **Universumsregel** auf der Sperrliste und ist **dort** ersetzt — nicht nur im Faltenplan. Wer A2 vertritt, muss erklären, welche Dauer Punkt 6 nach dem Vermerk zu Punkt 8 noch hat; **das Register nennt keine**. ② **3b (c)** (Z. 1944–1947, Commit `1bc2d57`, 16.09.): der einzige Registertext, der die Menge des Benchmarks **positiv** bestimmt — *„auf den in dieser Falte geladenen Symbolen des Bots"* — nennt **eine andere Menge** als die Vier-Jahres-Regel. ③ **16.11 Zeile 7** (Z. 2066): das Register führt „Benchmark auf geladenen Symbolen" selbst als Stelle, an der *„Registertext und Umsetzung auseinanderfallen"*. Unter A2 wäre das keine Lücke. ④ **S-B1** (`VORREGISTRIERUNG_S-B1_etf_trendfolge.md:47`) beschreibt den Hauptregister-Benchmark als *„gleichgewichtetes point-in-time-Universum des Bots (§7c, §10 Nr. 6)"* — **des Bots**, nicht des Marktes; das ist die 3b (c)-Menge. |

**Der ausdrückliche Satz, den der Auftrag verlangt:** Die Quellenlage trägt
**A1 im Ergebnis** — nach dem 15.09.2026 steht **kein** Registertext mehr hinter
einer Vier-Jahres-Regel für den Benchmark, und der einzige Registertext, der die
Benchmark-Menge positiv bestimmt (3b (c)), nennt eine andere. Sie trägt **A1
aber nicht über 5.3 allein**: 5.3 ist die Fundstelle für Faltenplan und
Bot-Bewertung; die Fundstellen für den Benchmark sind **Sperrliste 8 (Vermerk),
3b (c) und 15.1 / T34.10**. Die Chat-Sitzung hat also mit der Folgerung recht
und mit der Herleitung nur zur Hälfte. Was A2 richtig sieht, bleibt bestehen:
5.3 sagt nicht, was der Benchmark **stattdessen** nimmt — das sagt erst 3b (c),
zwei Tage später, und auch der nur bis zur Frage „ganze Falte oder ab
Ladetag" (Frage C).

---

## Nachweis 3 — Frage B: Schreibt Registertext 3b (c) die Loader-Schranke für den Benchmark vor?

**Der Text, wörtlich** (16.7, Z. 1944–1947, Commit `1bc2d57`, 16.09.2026, TB-41):

> **(c)** ⭐ **Der Benchmark einer Falte** — für die Drawdown-Nebenbedingung
> (Abschnitt 4) und für Rang 3 — **wird auf den in dieser Falte geladenen
> Symbolen des Bots gerechnet, nicht auf dem vollen Universum. Bot und Benchmark
> leben in derselben Menge.**

### B.1 — Was heisst „geladen"?

| Fundstelle | Wortlaut | Was folgt |
|---|---|---|
| 3b (a), Z. 1905–1907 | *„wenn der **Loader des Bots** in ihr mindestens ein Symbol an mindestens einem Handelstag handelbar macht"* | „geladen" = vom Loader handelbar gemacht |
| 3b (b), Z. 1909–1921 | *„`MIN_HISTORY_*` ist **je Bot mit seinem Namen und seiner Einheit** fest auf dem heutigen Wert"* — Tabelle 17 520 Kerzen / 730 / 500 / 1 825 Tage | die Schranke des Loaders ist registriert, je Bot |
| 16.2, Z. 1599–1622 | *„Es gilt Lesart H: ‚an mindestens einem Handelstag der Falte handelbar.'"* — und: *„H ist nicht nur das Registrierte, sondern das, was der Loader tut"* (F11) | „in dieser Falte geladen" = irgendwann in der Falte handelbar, **nicht** am Faltenbeginn |
| 17.3, Z. 2295–2299 | *„Nicht der Vorlauf schützt, sondern die **Mindesthistorie des Loaders** (Registertext 3b (a))"* | das Register **rechnet** selbst mit dem Loader als der Schranke |
| 21.3 (c), Z. 2884–2886 | *„hängt am Indikator-Vorlauf und an `MIN_HISTORY_*` des jeweiligen Loaders"* | dito, für die erste Falte |
| 15.8 Nr. 4, Z. 1421–1429 | *„Die Bots selbst überspringen kurze Historien (`MIN_HISTORY_DAYS` …). … Auch diese Angleichung gehört in TB-30b."* | schon am 15.09. war benannt, dass Werkzeuge und Loader auseinanderliegen |

**Zu „oder lässt der Text offen, dass eine zusätzliche Schranke danebensteht":**
Der Text sagt es nicht ausdrücklich — es steht nirgends *„und keine andere"*.
Aber das Register hat eine Regel dafür, was eine Schranke ohne Text ist:
**21.3 (a)** (Z. 2870–2873): *„Die frühere Konstante `ERSTE_MOEGLICHE_FALTE =
2019` war eine Festlegung im Code **ohne Entsprechung in einem Registertext**"*
— und wurde deshalb entfernt. `MINDESTTRAINING_JAHRE = 4` in `benchmark.py:183`
ist nach B.3 (unten) in derselben Lage. ⚠️ **Ein Name ist kein Messwert
(K3e):** dass die Konstante „Mindesttraining" heisst, sagt nichts; entscheidend
ist, dass **kein Text** ihre Zahl für den Benchmark nennt.

### B.2 — Ist `point_in_time(…, 4 Jahre)` „geladene Symbole", „volles Universum" oder ein dritter Fall?

**Ein dritter Fall — gemessen, nicht erschlossen** (`docs/belege/TB-65/frage_c_lauf.txt`):

| Markt | Menge V0 (vier Jahre vor Faltenbeginn) gegen „geladen" (Lesart H, Trockenlauf TB-56) | gegen „volles Universum" |
|---|---|---|
| **Krypto**, 5 Bots | **kleiner** — in 17 von 35 Selektionsfalten **leer** (0 Symbole); in 16 davon lädt der Loader 2 bis 10 Symbole (nur `t3_supertrend` 2018 ist auch beim Loader leer); ab 2022 3/6/9/13 gegen 13/13/13–17/17–18 | kleiner (Universum 24) |
| **Aktien**, 4 Bots | **zeichengleich** in **40 von 40** Falten (Symbolzahl **und** alle 100 DD-Stufen) — ⭐ **arithmetisch, nicht zufällig**: „Kursdaten ≥ 4 Jahre vor dem 1. Januar der Falte" und „≥ 1 825 Tage vor dem 31. Dezember der Falte" (H) grenzen dieselben Symbole ab; nur `elliott_wave_stocks`/`turtle_soup_stocks` 2017 VF ≠ V0 (Lesart F, siehe C) | kleiner (Universum 150) |

⇒ Der Satz stellt „geladene Symbole" gegen „volles Universum"; **V0 ist keines
von beiden**. Die **positive** Formulierung (*„wird auf … gerechnet"*) lässt für
eine dritte Menge keinen Raum — aber der Text **benennt** sie nicht, und er
sagt auch nicht, ob ein in der Falte geladenes Symbol für die **ganze Falte**
oder **ab dem Ladetag** zählt. **Das ist die Stelle, die 3b (c) wirklich nicht
regelt** (Frage C, VH gegen VT). Dass bei den Aktien-Bots V0 und „geladen"
zusammenfallen, ist zugleich der Grund, warum die Divergenz **bis TB-61 nicht
auffiel**: alle vorherigen Benchmark-Zahlen (Register Abschnitt 3, 21.6) waren
Aktienzahlen, und dort sind beide Regeln dieselbe Menge.

### B.3 — Gibt es einen Registertext, der `MINDESTTRAINING_JAHRE` für den Benchmark ausdrücklich vorsieht?

**Nein.** Gemessen auf `ff98f0a` (`docs/belege/TB-65/nachweis3_suchmuster.txt`,
jede Trefferzeile dort mit Zeilennummer):

| Muster | Treffer im Register (Zeilen) | davon **für den Benchmark mit Dauer** | davon in ERSETZT-Blöcken / mit Ersetzungsvermerk | Treffer `docs/**/*.md` gesamt | Treffer `research/vorregistrierung/*.py` |
|---|---:|---:|---|---:|---:|
| `Mindesttraining` | **4** (381, 594, 597, 1084) | **0** | 381 (Abschnitt-3-Block, ERSETZT), 594/597 (5.3, ERSETZT); 1084 = *„kein Mindesttraining"* | 30 | 2 |
| `MINDESTTRAINING` | **0** | **0** | — | 10 | 6 |
| `vier Jahre` | **7** (537, 551, 592, 604, 607, 829, 830) | **0** | **alle 7**: 5.1 (ERSETZT), 5.3 (ERSETZT), Sperrliste 8 (Vermerk „ersetzt") | 17 | 1 |
| `4 Jahre` | **1** (381) | **0** | 381 (ERSETZT-Block) | 8 | 0 |
| `point-in-time` | **12** (401, 443, 593, 608, 685, 695, 738, 825, 828, 1210, 1268, 1553) | **0** — 401/443/685/695/738/825 nennen den Benchmark als „point-in-time", **keine nennt eine Dauer**; 1210/1268/1553 = 3d (anderer Lauf) | 593/608 (5.3), 828 (Sperrliste 8) | 29 | 6 |
| `Vorlauf` | **19** | **0** — 17× Indikator-Vorlauf, 829/830 Sperrliste 8, 2268–2303 = 17.3 (dort wird „Vorlauf" als Begründung **verworfen**) | 829/830 | 63 | 5 |
| `Benchmark` | **29** | **0** mit Dauer; **1** mit Menge: **Z. 1944–1947 = 3b (c), „geladene Symbole"** | — | 103 | 27 |
| `geladen` | **4** (1423, 1945, 2066, 2295) | 1945 = 3b (c); 2066 = 16.11 Zeile 7 (Lücke benannt) | — | 94 | 1 |

**Ausserhalb des Registers** steht die Vier-Jahres-Regel für einen Benchmark
genau **einmal** als Registertext: `docs/VORREGISTRIERUNG_S-E1_nulltest.md:57–59`
(*„point-in-time (ein Titel geht in einen Monat nur ein, wenn seine Kursdaten
mindestens vier Jahre vor Monatsbeginn einsetzen — dieselbe Regel wie im
Hauptregister)"*, Stand 14.09.2026, **ohne** ERSETZT-Vermerk). Das ist das
Register des Nulltests S-E1, nicht das der Neuselektion; es verweist auf eine
Hauptregister-Regel, die dort ersetzt ist. **Beobachtung, nicht Gegenstand.**

**Der ausdrückliche Satz:** 3b (c) schreibt dem Benchmark die Menge der
**geladenen** Symbole vor, und „geladen" ist über 3b (a), 3b (b) und 16.2 als
**Loader mit `MIN_HISTORY_*`, Lesart H** bestimmt. Eine zweite Schranke daneben
hat keinen Text. **Nicht bestimmt** ist, ob die Mitgliedschaft im Benchmark je
Falte **ganz** oder **ab Ladetag** gilt.

---

## Nachweis 4 — Frage C: die Tabelle aus TB-61 mit der Loader-Schranke statt vier Jahren

### Wie gerechnet — und die drei Gegenproben, die vor jeder Zahl liefen

`research/vorregistrierung/` wurde nach `research/_tb65_kopie/` kopiert; dort lief
`tb65_rechnung.py` (im Repo abgelegt unter `docs/belege/TB-65/tb65_rechnung.py`),
das `bh_tagesrenditen`, `drawdown_bei_exposure`, `point_in_time`, `EXPOSURE_STUFEN`
und `faltenplan()` **unverändert aus der Kopie importiert**; die Medianbildung ist
die aus `je_bot` (Median über **alle** Selektionsfalten, leere Falte = 0,0). Vier
Fassungen je Bot und Falte:

| Fassung | Menge im Benchmark | Woher die Menge kommt |
|---|---|---|
| **V0** vorher | Symbole mit Kursdaten ≥ 4 Jahre vor Faltenbeginn, ganze Falte | `benchmark.py` wie in TB-61 |
| **VH** geladen, ganze Falte | Symbole, die der Loader **in dieser Falte** an ≥ 1 Handelstag lädt (Lesart H), für die **ganze** Falte | **gelesen**, nicht nachgebaut: `research/faltenplan_neun/daten/faltenplan_ohne_schranke.json` → `trockenlauf_3b.je_bot.<bot>.falten[].H_symbole` — der Trockenlauf des Laufcodes (TB-56, *„das einzig zulässige Werkzeug"*, 3b) |
| **VT** geladen, täglich | dasselbe Symbol geht **ab dem Tag nach** seinem Handelbar-Datum ein; die Menge wechselt innerhalb der Falte | Handelbar-Datum nachgerechnet mit `faltenschranke_messung.loader_lesart` (TB-56-Werkzeug): erster Kurstag + `MIN_HISTORY_DAYS`; `elliott_wave`: **Datum der 17 520. 1h-Kerze** |
| VF Loader-Schranke am Faltenbeginn | Symbole mit Handelbar-Datum ≤ Faltenbeginn, ganze Falte | mechanische Lesart „vier Jahre durch `MIN_HISTORY_*` ersetzen" = Lesart **F**, die das Register **nicht** gewählt hat (16.2); nur zur Einordnung |

| Gegenprobe | Ergebnis |
|---|---|
| **V0 gegen `benchmark_drawdowns_neu.json`** (TB-61): Symbolzahl, Handelstage, alle 100 Stufen je Falte, `dd_toleranz` je Bot | **0 Abweichungen** — die Kopie rechnet, was TB-61 gerechnet hat |
| **VH-Symbolzahl gegen Trockenlauf-Spalte H** | **78 / 78** Falten gleich |
| **VT-Symbolzahl („irgendwann in der Falte") gegen Spalte H** | **78 / 78** gleich — die nachgerechneten Handelbar-Daten ergeben in **jeder** Falte dieselbe Menge wie der Loader selbst |
| VF-Symbolzahl gegen Spalte F | 74 / 78; die vier Abweichungen sind **eine** Aktie: `ABBV`, handelbar genau am **2018-01-01** (erster Kurstag 2013-01-02 + 1 825) — VF zählt „≤ Faltenbeginn", der Trockenlauf prüft F am ersten Handelstag |

⭐ **`elliott_wave` ist NICHT ausgelassen.** Seine Schranke ist eine Kerzenzahl,
und genau so wurde sie gerechnet: je Symbol das Datum der 17 520. Kerze der
1h-Datei (`docs/belege/TB-65/frage_c_handelbar_ab.txt`). Der Unterschied zur
Zeitspanne ist gemessen, nicht angenommen: BTC/ETH erreichen die Kerzenzahl am
**2019-08-20**, drei Tage nach dem lückenlosen Datum 2019-08-17 (147 fehlende
Kerzen); die Verzögerung liegt bei allen Symbolen zwischen **0 und 3 Tagen**.
Für VH stammt seine Menge ohnehin aus dem Trockenlauf seines eigenen Loaders.

### Tabelle C1 — leere Selektionsfalten und `DD_Toleranz` (25 / 50 / 100 %), vorher gegen nachher

„leer" = 0 Symbole oder 0 Handelstage. Vollständig je Falte und Stufe in
`docs/belege/TB-65/frage_c_rechnung.json`; die Falten-Tabelle in
`frage_c_tabellen.md`.

| Bot | Sel.-Falten | leer **V0** | leer **VH** | leer **VT** | leer VF | `DD_Toleranz` **V0 (vorher, TB-61)** | **VH** geladen, ganze Falte | **VT** geladen, täglich | VF Loader-Schranke am Faltenbeginn |
|---|---:|---:|---:|---:|---:|---|---|---|---|
| `elliott_wave` | 4 | **2** | 0 | 0 | 1 | −6,07 / −11,89 / −22,42 | **−20,09 / −37,90 / −65,77** | **−16,42 / −31,21 / −55,91** | −16,51 / −31,36 / −56,12 |
| `t3_supertrend` | 8 | **4** | 1 | 1 | 2 | −3,24 / −6,32 / −12,01 | **−16,13 / −30,94 / −55,19** | **−12,89 / −24,73 / −45,16** | −11,57 / −22,54 / −42,20 |
| `rsi2_crypto` | 7 | **3** | 0 | 0 | 0 | −6,48 / −12,64 / −24,02 | **−16,30 / −31,95 / −59,06** | **−17,26 / −32,59 / −57,29** | −17,00 / −32,19 / −56,88 |
| `turtle_soup_crypto` | 8 | **4** | 0 | 0 | 1 | −3,24 / −6,32 / −12,01 | **−17,40 / −33,28 / −59,77** | **−16,13 / −30,52 / −54,05** | −16,00 / −30,32 / −53,84 |
| `volatility_breakout_crypto` | 8 | **4** | 0 | 0 | 1 | −3,24 / −6,32 / −12,01 | **−17,40 / −33,28 / −59,77** | **−16,13 / −30,52 / −54,05** | −16,00 / −30,32 / −53,84 |
| `elliott_wave_stocks` | 9 | 0 | 0 | 0 | 0 | −2,18 / −4,33 / −8,55 | −2,18 / −4,33 / −8,55 | −2,18 / −4,33 / −8,55 | −2,26 / −4,49 / −8,86 |
| `rsi2_mean_reversion` | 8 | 0 | 0 | 0 | 0 | −3,35 / −6,61 / −12,89 | −3,35 / −6,61 / −12,89 | −3,32 / −6,55 / −12,77 | −3,35 / −6,63 / −12,92 |
| `turtle_soup_stocks` | 9 | 0 | 0 | 0 | 0 | −2,18 / −4,33 / −8,55 | −2,18 / −4,33 / −8,55 | −2,18 / −4,33 / −8,55 | −2,26 / −4,49 / −8,86 |
| `volatility_breakout` | 8 | 0 | 0 | 0 | 0 | −3,35 / −6,61 / −12,89 | −3,35 / −6,61 / −12,89 | −3,32 / −6,55 / −12,77 | −3,35 / −6,63 / −12,92 |
| `t3_supertrend` **ohne 2018** (21.4: 3b (a) bindet, 7 Falten) | 7 | 3 | 0 | 0 | 1 | −6,48 / −12,64 / −24,02 | −17,26 / −33,43 / −59,56 | −13,90 / −26,57 / −48,10 | −14,07 / −26,87 / −48,56 |

Die eine leere Falte, die bleibt (`t3_supertrend` 2018), ist unter VH und VT
**richtig** leer — der Loader lädt dort kein Symbol (Trockenlauf H = 0), und nach
Register 21.3 (b) / 21.4 ist sie für diesen Bot keine Falte; die Zeile „ohne
2018" zeigt die Zahl nach 21.4.

### Tabelle C2 — das Verhältnis nachher / vorher bei 100 % Exposure (Krypto)

| Bot | V0 | VH | VT | VF | Faktor VH | Faktor VT | Faktor VF |
|---|---:|---:|---:|---:|---:|---:|---:|
| `elliott_wave` | −22,42 | −65,77 | −55,91 | −56,12 | ×2,9 | ×2,5 | ×2,5 |
| `t3_supertrend` | −12,01 | −55,19 | −45,16 | −42,20 | ×4,6 | ×3,8 | ×3,5 |
| `rsi2_crypto` | −24,02 | −59,06 | −57,29 | −56,88 | ×2,5 | ×2,4 | ×2,4 |
| `turtle_soup_crypto` | −12,01 | −59,77 | −54,05 | −53,84 | ×5,0 | ×4,5 | ×4,5 |
| `volatility_breakout_crypto` | −12,01 | −59,77 | −54,05 | −53,84 | ×5,0 | ×4,5 | ×4,5 |

Die Richtung ist bei allen fünf dieselbe: V0 ist die **strengere** Toleranz,
weil jede leere Falte mit 0,00 — dem am wenigsten negativen Wert überhaupt — in
den Median eingeht. Bei den vier Aktien-Bots ist der Faktor unter VH und VT
**1,00** (VT weicht bei zwei Bots um 0,12 Punkte ab, weil dort Symbole mitten
in einer Falte handelbar werden).

### Tabelle C3 — wo der Unterschied beisst: `erlaubt(f)` bei 100 % Exposure (Festlegung 4, nachrichtlich)

`erlaubt(f) = min(1,25 × DD_Benchmark(f), DD_Toleranz)`; Auszug für die drei
Krypto-Tagesbots (`turtle_soup_crypto` = `volatility_breakout_crypto`), vollständig
in `frage_c_tabellen.md`, Tabelle C4:

| Falte | `erlaubt` **V0** | bindet unter V0 | `erlaubt` **VT** | `erlaubt` **VH** |
|---|---:|---|---:|---:|
| 2018 (`turtle_soup_crypto`) | **−12,01** | DD_Toleranz (Benchmark leer) | −54,05 | −109,90 |
| 2019 | **−12,01** | DD_Toleranz (Benchmark leer) | −71,61 | −77,04 |
| 2020 | **−12,01** | DD_Toleranz (Benchmark leer) | −78,39 | −75,60 |
| 2021 | **−12,01** | DD_Toleranz (Benchmark leer) | −75,81 | −73,83 |
| 2022 | −82,20 | relative Grenze | −87,05 | −88,61 |
| 2023 | −30,02 | relative Grenze | −54,05 | −59,77 |
| 2024 | −41,64 | relative Grenze | −54,05 | −59,77 |
| 2025 | −60,70 | relative Grenze | −63,51 | −64,90 |

⚠️ **Das ist die eigentliche Folge der leeren Falten, und sie steht nicht im
Faktor:** In 2019, 2020 und 2021 — Jahren, in denen der Loader dieser Bots 6, 9
und 10 Symbole lädt — müsste ein Parametersatz bei voller Exposure unter V0
seinen Kapital-Drawdown über **−12,01 %** halten, weil `DD_Benchmark(f) = 0`
die relative Grenze auf 0 setzt und allein die Toleranz bleibt. Der
gleichgewichtete Benchmark dieser Jahre verlor **−57 bis −63 %**. Unter V0 wäre
Abbruchkriterium (b) (*„kein Parametersatz erfüllt die Drawdown-Bedingung in
allen Falten"*) für die Krypto-Bots nicht eine Frage der Parameter, sondern der
leeren Benchmark-Falten. *Erschlossen, nicht gemessen: ob ein Satz das
überstünde — es gibt keinen Lauf.* Die Werte jenseits von −100 % unter VH
(−109,90) sind formal (1,25 × −87,92); ein Drawdown kann −100 % nicht
unterschreiten.

### Was zwischen VH und VT steht — die Entscheidung, die 3b (c) offen lässt

| Falte | VH: geladen, ganze Falte | VT: geladen, ab Ladetag | Woran es liegt |
|---|---|---|---|
| `turtle_soup_crypto` / `volatility_breakout_crypto` **2018** | 2 Symbole, 365 Tage, **−87,92 %** | 2 Symbole, **1** Handelstag, **−3,60 %** | BTC/ETH werden am **2018-12-30** handelbar (2017-08-17 + 500 Tage; Register 21.4 nennt genau das). VH rechnet ihnen das ganze Krypto-Jahr 2018 zu, das der Bot nicht handeln konnte |
| `elliott_wave` **2018–2019** | 3 Symbole, 730 Tage, −84,67 % | 3 Symbole, 133 Tage, −42,14 % | Kerzenzahl erreicht am 2019-08-20 (BTC/ETH), 2019-11-09 (BNB) |
| `t3_supertrend` **2019** | 3 Symbole, 365 Tage, −59,56 % | 3 Symbole, 136 Tage, −42,21 % | 730 Tage erreicht am 2019-08-17 |

*„Bot und Benchmark leben in derselben Menge"* spricht für VT (dieselbe Menge
**zur selben Zeit**); *„in dieser Falte geladen"* mit Lesart H lässt sich als VH
lesen. **Hier entschieden ist nichts** — der Unterschied ist bei drei Bots in
der ersten Falte gross und in der `DD_Toleranz` bei `t3_supertrend` 3,2 Punkte
(25 %) bzw. 10 Punkte (100 %).

---

## Nachweise 5 bis 7

| # | Nachweis | Ergebnis |
|---:|---|---|
| **5** | SHA-256 `benchmark_drawdowns.json` | **`a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee`** — vor der Aufgabe (12:38 UTC) und nach dem letzten Schreiben **gleich** ✅ |
| **5** | SHA-256 `benchmark_drawdowns_neu.json` | **`e06812d2f5c26e73aee7265039e6b320b3de253837483c29e164ea07d404a062`** — vor und nach der Aufgabe **gleich** ✅ (Wert wie in TB-61, Schritt 4) |
| **6** | `git diff --numstat ff98f0a..HEAD` | **nur** Dateien unter `docs/` — Liste in `docs/belege/TB-65/nachweis6_numstat.txt` ✅ |
| **7** | `git status --short` nach dem letzten Commit; Wegwerf-Kopie entfernt | siehe `docs/belege/TB-65/nachweis7_status.txt` — leer, `research/_tb65_kopie/` existiert nicht mehr ✅ |

---

## Beobachtungen am Rande — NICHT ausgeführt, hier nur benannt

| | Beobachtung | Warum liegen gelassen |
|---|---|---|
| ⚠️ | **Die Vier-Jahres-Regel steht ohne Vermerk in einem zweiten Register:** `docs/VORREGISTRIERUNG_S-E1_nulltest.md:57–59` (*„dieselbe Regel wie im Hauptregister"*). Das Hauptregister hat sie ersetzt; der Verweis zeigt seit dem 15.09. auf einen ersetzten Satz | Registertext; ⛔ dieser Auftrag ändert keinen |
| ⚠️ | `benchmark.py:48–54` (Kopf, „DAS UNIVERSUM") und `registerbericht.py:138–140` (*„Mindesttraining vor der ersten Falte: 4 Jahre"*, erzeugt Z. 381 des Registers) tragen den ersetzten Satz weiter; `faltenplan.py:28–30` sagt selbst *„(Verfahren A)"* und `:208` schreibt `mindesttraining_jahre` in jeden Plan | Code; ⛔ rein lesend |
| ⚠️ | `research/krypto_historie/faltenplan.py:65` führt eine **weitere Kopie** `MINDESTTRAINING_JAHRE = 4` (mit ihr entstand die 2022 aus 17.3 / T34.10) | ausserhalb `research/vorregistrierung/`, eigene Aufgabe (T56b.6-Klasse) |
| | Der Trockenlauf-Wert F und VF weichen bei `ABBV` um einen Tag ab (handelbar exakt am 2018-01-01) | Randfall der Lesart F, die nicht gilt |
| | `pandas` `FutureWarning` (`pct_change`, `fill_method='pad'`) — im Lauf mit `-W ignore` unterdrückt, damit die Rohausgabe lesbar bleibt; Rechenweg unverändert (TB-56 Beobachtung 8, TB-61) | Sperrliste 6 |
| | Die VH-Zahl 2018 (−87,92 %) zeigt, dass „ganze Falte" bei einem Ladetag am Jahresende ein Jahr misst, das der Bot nicht handeln konnte — ein Argument in der Sache, **kein** Grund für eine Wahl hier (K3f: Kriterium nach dem Blick aufs Ergebnis) | Entscheidung, nicht Messung |

---

## Was diese Aufgabe ausdrücklich NICHT entschieden hat — und welche Entscheidung ansteht

**Nicht entschieden:** welche Lesart gilt. Nicht entschieden, ob die Krypto-Zahlen
aus TB-61 neu gerechnet werden. Nicht entschieden, ob der Benchmark ein geladenes
Symbol für die ganze Falte (VH) oder ab dem Ladetag (VT) trägt. Nicht angefasst:
`benchmark.py`, `faltenplan.py`, `registerdaten.py`, beide Tabellen, jeder
Registertext, die roten Tests G6 und H3.

**Was gemessen ist und Entscheidung nicht ersetzt:** (1) Kein Registertext nennt
vier Jahre für den Benchmark; alle acht Zeilen mit „vier Jahre" sind ersetzt.
(2) Der einzige Text, der die Benchmark-Menge positiv nennt, ist 3b (c) —
geladene Symbole. (3) Das Register führt den Abstand zwischen 3b (c) und
Umsetzung seit dem 16.09. selbst als Lücke (16.11 Zeile 7, Schliesser TB-30b).
(4) Bei den Aktien-Bots ist der Abstand null; bei den Krypto-Bots ist er
ergebnisbestimmend — und zwar weniger über die Toleranz als über `erlaubt(f)`
in 2019–2021.

**Die Entscheidung, die ansteht — Betreiber oder Fable, vor dem Amendment nach
21.9:**

| | Frage | Was dranhängt |
|---|---|---|
| **1** | Rechnet der Krypto-Benchmark auf den **geladenen** Symbolen (3b (c)), oder bleibt `MINDESTTRAINING_JAHRE = 4` in `benchmark.py` — und wenn ja, mit welchem Registertext? | Ohne Text ist die Konstante in der Lage von `ERSTE_MOEGLICHE_FALTE` (21.3 (a)). **Empfehlung dieser Sitzung, als Empfehlung gekennzeichnet:** an Fable, in einem Zug mit TB-61 Befund 2 (21.3 (b) im Code) — *nicht* weil das Ergebnis nachgiebiger wäre, sondern weil die Regel textlich schon steht und nur ihre Umsetzung und ihr Zeitbezug fehlen |
| **2** | Wenn geladen: **ganze Falte (VH) oder ab Ladetag (VT)?** | 3b (c) sagt es nicht. Der Unterschied ist gemessen (Tabelle oben). Die Antwort gehört als Registertext **vor** die Rechnung, sonst ist sie eine Wahl nach dem Ergebnis (K3f) |
| **3** | Gilt die Antwort auch für den **Rang-3-Benchmark** (`auswertung.py` liest heute eine Reihe **je Markt**, `benchmark_tagesreihen/<markt>.csv`)? | 3b (c) nennt beide ausdrücklich; 16.11 Zeile 7 weist beide TB-30b zu |

---

## In einfacher Sprache

**Worum es ging:** Zwei Sitzungen waren sich uneins, ob die Vier-Jahres-Regel
im Vergleichsmassstab der Krypto-Bots eine offene Frage oder ein Regelverstoss
ist. Ich sollte das nachlesen und nachrechnen — und durfte ausdrücklich zu dem
Schluss kommen, dass die Chat-Sitzung sich irrt.

**Was ich gefunden habe:** Die Chat-Sitzung hat mit dem **Ergebnis** recht und
mit der **Begründung** nur zur Hälfte. Die Stelle, die sie nennt (Abschnitt 5.3),
handelt vom Faltenplan und sagt nichts über den Massstab. Aber drei andere
Stellen sagen es: Die Vier-Jahres-Regel ist im Register **überall** als ersetzt
markiert — auch dort, wo sie als Universumsregel auf der Sperrliste stand —, und
der einzige Regeltext, der sagt, worauf der Massstab rechnet, nennt **die
Symbole, die der Bot in dieser Falte tatsächlich lädt**. Das Register selbst
führt diesen Punkt seit vier Tagen als „Regel steht, Programm tut es noch
nicht". „Verstoss" ist deshalb das falsche Wort — „bekannte Lücke, die vor dem
Amendment zu schliessen ist" das richtige. Und TB-61s Angebot „vier Jahre
behalten, null Jahre, oder etwas anderes" trifft auch nicht: keine dieser drei
Möglichkeiten ist das, was im Register steht.

**Was es zahlenmässig ausmacht:** Für die vier Aktien-Bots **nichts** — dort
ergeben beide Regeln zufällig dieselben Aktien, das ist der Grund, warum es bis
jetzt niemandem auffiel. Für die fünf Krypto-Bots ist die Verlustschranke je
nach Lesart **zweieinhalb- bis fünfmal** so tief wie in der TB-61-Tabelle.
Wichtiger als der Faktor: In den Jahren 2019 bis 2021, in denen die Bots mit
sechs bis zehn Symbolen handeln, dürfte ein Parametersatz nach der TB-61-Tabelle
nur **12 Prozent** verlieren, während der Markt selbst 60 Prozent verlor.

**Was ich nicht gefunden habe — und du entscheiden musst:** Das Register sagt
nicht, ob ein Symbol, das der Bot mitten im Jahr zu laden beginnt, im Massstab
für das **ganze Jahr** oder **ab diesem Tag** zählt. Der Unterschied ist bei drei
Bots im ersten Jahr riesig. Das ist die Entscheidung, die vor der Neurechnung
steht; ich habe sie nicht getroffen und keine Zahl im Repo verändert.

*Ausgeführt am 20.09.2026 von der Mac-Sitzung TB-65. Rein lesend; ein
Belege-Commit (`9ad37e4`) und der Abgabe-Commit.*

# REGISTER-KOPIE Teil 2 von 4 — Abschnitte 24–37 — Commit 1e1145702ba8b6ee6ad4cecaecb75591463faa48 — 2026-09-27 — Original sha256 18e39ee29b9bd4f03a2ad4953c85c2e59558de3aaab26844ae58fb7590fca93c — KOPIE, nicht das Register

## 24. Präzisierung zu Registertext 4 und zu Festlegung 1 — der Drawdown der Nebenbedingung wird Mark-to-Market gerechnet, und die Regel steht vor der Messung (TB-71, 20.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Satz wird umgeschrieben**
— Festlegung 1 bleibt in Abschnitt 1 stehen (Z. 47, dort seit heute mit der
Marke *„PRÄZISIERT durch Abschnitt 24"*), Registertext 1a bleibt in 15.3,
Registertext 4 in 15.6 und 21. Das ist die Form aus
`docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md`, Regel 4, und die Form der
Abschnitte 21 und 23.

**Anlass:** Bei der Messung zu Abschnitt 23 (Kalender des Bot-Kapitalpfades,
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20c_kapitalpfad.md`) fiel auf,
dass der Kapitalpfad, aus dem `equity_simulation.py` den Drawdown rechnet,
**keinen Tageskalender hat** — er ist ereignisindiziert. Fables dritte Antwort
vom 20.09.2026, 18:00 Ortszeit (`FABLE_ANTWORT_2026-09-20c_kapitalpfad.md`,
Teil 1) benennt daraus einen Widerspruch **innerhalb des Registers**: Festlegung
1 (*„Führendes Mass: Kapital-Drawdown aus `equity_simulation.py`"*, Z. 47) gegen
Registertext 1a (*„Reihe der täglichen Netto-Mark-to-Market-Renditen des
Kapitalpfads"*, 15.3, Z. 1102–1104 im Stand `cc096e1`) und 2a (*„Summe der täglichen
Netto-Mark-to-Market-Renditen"*, 15.4). Seine vierte Antwort vom 20.09.2026,
18:08 (`FABLE_ANTWORT_2026-09-20d_mtm_messung.md`) macht die **Reihenfolge**
zur Bedingung: die Entscheidungsregel steht im Register, **bevor** jemand einen
Mark-to-Market-Pfad rechnet. Umsetzung: `docs/auftraege/MAC_TB-71_register_schliessen.md`,
Ergebnis `docs/ERGEBNIS_TB-71_register_schliessen.md`.

**Art der Änderung nach der Drei-Kategorien-Regel (F17):** Fable ordnet den
Registerwiderspruch als **Berichtigung** ein (*„aufzulösen zugunsten der Seite
mit dem Grund (L1)"*). Weil Festlegung 1 aber eine der zwölf
Betreiberfestlegungen vom 14.09.2026 ist, wurde sie **dem Betreiber vorgelegt,
nicht als Berichtigung vollzogen** — Fable: *„Sie wird ihm vorgelegt, nicht als
Berichtigung vollzogen. Beides übernehme ich."* **Betreiberentscheidung
20.09.2026, 18:15 Ortszeit, per anklickbarer Frage: erst die Regel, dann die
Messung** (überliefert in `docs/auftraege/MAC_TB-71_register_schliessen.md`, Abschnitt 3; Einzelheiten in 24.4). ⚠️ **Die
Richtung der Wirkung ist bekannt und geht gegen alle neun Bots** — der tägliche
Drawdown ist nie flacher als der ereignisweise; **ihre Grösse ist nicht
gemessen** und ist nach 24.3 für die Entscheidung ohne Belang. Es hat kein
Selektionslauf stattgefunden; kein Parametersatz ist bewertet, kein Ergebnis
erzeugt; der Laufcode, der die Tagesreihe je Zelle erzeugt, **existiert nicht**
(24.5).

---

### 24.1 Der Befund

**Wörtlich aus Fables dritter Antwort (20.09.2026, 18:00):**

> Der Drawdown der Nebenbedingung wird auf einem Objekt gerechnet, das das
> Register ausschliesst. `calculate_max_drawdown` läuft über `capital_after` je
> Ereignis — eine Kurve, die sich nur an Ein- und Ausstiegen bewegt. … **Sie
> sieht keinen unrealisierten Verlust.** Eine Position, die zwischen Einstieg und
> Ausstieg 20 % unter Wasser war und mit −3 % geschlossen wurde, trägt −3 % zum
> Drawdown bei. Der Benchmark daneben ist tagesgenau bewertet. … „Bot und
> Benchmark leben in derselben Menge" gilt dann auf der Symbol- und Zeitachse,
> aber nicht auf der Bewertungsachse.

**Die Fundstellen, gemessen am 20.09.2026** (Stand Commit `cc096e1`; gelesen,
nicht ausgeführt):

| Fundstelle | was dort steht |
|---|---|
| `shared/zuteilung.py:720–735` | `equity_curve.append({"time": …, "capital_after": …})` je Ereignis (Ausstieg). Kein Tageskalender |
| `shared/messkette.py:139–153` | `calculate_max_drawdown` rechnet über `equity_df["capital_after"]` — die Funktion, die bis TB-28 neunmal zeichengleich in den `strategies/*/equity_simulation.py` stand |
| `research/vorregistrierung/beispieldaten.py:24–26` | *„der Kapital-Drawdown einer Falte steht in `zellen.csv`, weil er im echten Lauf aus `equity_simulation.py` kommt, und **nicht aus der Tagesreihe** nachgerechnet wird. Das ist auch im echten Lauf so."* |
| `research/vorregistrierung/auswertung.py:246–247` | die Nebenbedingung vergleicht genau dieses `kapital_drawdown_pct` gegen die Benchmark-Grenze (`dd_satz`, `bestanden`) |
| Register Z. 47 (Festlegung 1) | *„Führendes Mass — Kapital-Drawdown aus `equity_simulation.py`"* |
| Register 15.3, Registertext 1a (Z. 1102–1104 im Stand `cc096e1`) | *„auf der Reihe der täglichen Netto-Mark-to-Market-Renditen des Kapitalpfads gerechnet, nie auf Trade-Listen. Flache Tage stehen mit Rendite 0 in der Reihe."* |
| Register 15.4 (Registertext 2a) | *„Die Falten-Rendite ist die Summe der täglichen Netto-Mark-to-Market-Renditen dieser Tage."* |

**Was der Widerspruch bedeutet, in Fables Worten:** *„Sonst wird auf einem
Objekt selektiert (Sharpe, täglich) und auf einem anderen beschränkt (Drawdown,
ereignisweise) — genau die Inkonsistenz aus M.3, eine Ebene tiefer."* Und:
*„Der Drawdown gehört aus derselben Tagesreihe wie der Sharpe."*

---

### 24.2 Der Registertext — Präzisierung zu Registertext 4

**Fables Wortlaut, unverändert:**

> **Registertext 4, Präzisierung.** Der Kapital-Drawdown einer Falte für die
> Nebenbedingung wird auf der täglichen Mark-to-Market-Reihe des Kapitalpfads
> gerechnet (1a), auf denselben Tagen wie der Benchmark (3b (c)). Der
> ereignisindizierte Drawdown aus `equity_simulation.py` wird berichtet, nicht
> bewertet.

**Was der Satz festlegt und was nicht:** Er legt die **Bewertungsachse** fest
(täglich, zum Marktpreis, 1a) und die **Zeitachse** (dieselben Tage wie der
Benchmark, 3b (c) in der Fassung aus 23.3). Er ändert nichts an der Formel der
Nebenbedingung (Festlegung 4, Abschnitt 4), nichts an `DD_Toleranz`
(Festlegung 5), nichts am Benchmark (Abschnitt 23). Der ereignisindizierte
Drawdown bleibt als **Berichtswert** bestehen — er verschwindet nicht, er
entscheidet nicht.

---

### 24.3 ⭐⭐ Die Entscheidungsregel — vor jeder Messung

**Wörtlich (Fable, vierte Antwort, Punkt 1 seiner empfohlenen Reihenfolge) —
und sie steht hier, bevor jemand einen Mark-to-Market-Pfad gerechnet hat:**

> Der Drawdown der Nebenbedingung wird auf der täglichen
> Mark-to-Market-Reihe gerechnet (1a); die Grösse der Abweichung zur
> ereignisindizierten Kurve wird gemessen und berichtet und ist für die
> Entscheidung ohne Belang.

**Warum die Reihenfolge zählt — Fable wörtlich:**

> Eure Lesart ist richtig: Der Grund kommt aus 1a und L1 und steht fest, bevor
> die Zahl existiert. Die Zahl beziffert, sie entscheidet nicht. Aber das ist nur
> dann wahr, wenn es **vor** der Messung aufgeschrieben ist — sonst ist die Zahl,
> sobald sie da ist, ein Argument, und zwar in beide Richtungen: „ändert wenig,
> also nicht die Mühe" oder „ändert viel, also zu riskant vor dem Tag". … **Eine
> Zahl, die nichts entscheiden darf, sollte nicht auf dem Tisch liegen, während
> entschieden wird.**

⚠️ **Die Warnung, die dazugehört — Fable wörtlich:**

> Eine kleine Abweichung im Mittel sagt nichts über die Falten, in denen die
> Nebenbedingung binden soll — 2020 und 2022 sind die Falten mit den grössten
> unrealisierten Verlusten innerhalb offener Positionen.

**Was daraus für die Messung folgt:** Sie ist zulässig und vorgesehen — **nach**
diesem Eintrag, als Forschungsskript ausserhalb des Laufcodes, je Bot an den
TB-24-Trade-Listen und den Kursdateien (`AKTUELLER_AUFTRAG.md`: TB-73, *„erst
nach TB-71 (b)"*). Ihr Ergebnis geht als bekannte Wirkung in die Notiz zu
Festlegung 1 (24.4) — **nie in eine Entscheidung**. Wer die Zahl später liest
und daraus *„zu klein für die Mühe"* oder *„zu gross vor dem Tag"* folgert,
trifft die nachträgliche Wahl, gegen die F17 steht.

---

### 24.4 Was mit Festlegung 1 geschieht

⭐ **Sie wird nicht gestrichen, sie wird präzisiert.** Register Z. 47 bleibt
stehen; hier steht daneben:

| | |
|---|---|
| **Führendes Mass bleibt der Kapital-Drawdown** | unverändert |
| ⭐ **Präzisiert ist, worauf er gerechnet wird** | auf der täglichen Mark-to-Market-Reihe des Kapitalpfads (1a), nicht auf der Ereigniskurve |
| **Der ereignisweise Drawdown** aus `equity_simulation.py` | bleibt **Berichtswert** |
| **Betreiberentscheidung** | 20.09.2026, 18:15 Ortszeit, per anklickbarer Frage: erst die Regel (dieser Abschnitt), dann die Messung (TB-73) |
| **Wirkung, gemessen** | *noch nicht* — der Eintrag steht absichtlich vor der Zahl (24.3). Bekannt ist die Richtung: gegen alle neun Bots, am stärksten bei langen Haltedauern und hoher Exposure (`turtle_soup_stocks`: 100 % im Markt, 14 Tage Median). Die Zahl wird hier nachgetragen, wenn TB-73 gelaufen ist |

> ⭐ **NACHGETRAGEN in Abschnitt 24.6 (TB-73, 20.09.2026):** die Wirkung ist gemessen — je Bot und je Falte, mit den fünf Falten, in denen die Richtung *nicht* gegen den Bot geht. Die Zeile oben bleibt, wie sie war.

**Die Vorgeschichte gehört ausdrücklich dazu, sonst liest sich dieser Abschnitt
wie ein Widerruf:** `research/drawdown_reihenfolge/` (Commits vom 12.09.2026,
`26bdd97`, `971c001`, `027fe2b`) hat **drei** Drawdown-Begriffe verglichen —
Symbol-Blockreihenfolge, chronologisch auf der kumulierten PnL-Summe,
Kapitalkurve aus `equity_simulation.py` — und die Kapitalkurve als *„den
erlebbaren Verlauf"* gewählt (`BERICHT.md`, Abschnitt 0). Daher Festlegung 1.
**Mark-to-Market war unter den dreien nicht dabei.** Fable dazu, wörtlich:

> Das Kriterium war richtig; nur war die vierte Definition nicht im Vergleich —
> und sie ist die, die das Kriterium am besten erfüllt. **Erlebbar ist, was das
> Konto an jedem Tag zeigt, und das Konto zeigt offene Positionen zum
> Marktpreis, nicht zum Einstandskurs.** Die Ereigniskurve ist der *realisierte*
> Verlauf; der erlebbare ist der bewertete.

Und, ebenfalls Fable: *„Meine Kritik widerspricht der Messung nicht, sie
ergänzt den Vergleich um das Objekt, das 1a schon vorschreibt."* — Das ist
dieselbe Lehre wie `L1` im Journal (12.09.2026): Die Ereigniskurve erzeugte
Korrelationen nahe null, bis zu Marktpreisen bewertet wurde; für den Drawdown
tut sie dasselbe mit umgekehrtem Vorzeichen.

---

### 24.5 Was dieser Abschnitt ausdrücklich NICHT tut — und was ihm folgen muss

| | |
|---|---|
| ⚠️ | **Kein Code geändert.** `auswertung.py` ist eingefroren (15.8 Nr. 3, TB-30b) und bleibt es, auch ihr Docstring; `beispieldaten.py`, `registerdaten.py`, `benchmark.py`, `shared/zuteilung.py`, `shared/messkette.py` sind unberührt |
| ⚠️ | **Nichts gerechnet.** Kein Mark-to-Market-Pfad, keine Tabelle, kein Lauf; `benchmark_drawdowns.json` (`a163c498…36d1ee`) und `benchmark_drawdowns_vt.json` (`4549395f…8745d`) byteweise unverändert |
| ⭐ | **Drei Code-Stellen müssen 24.2 folgen, sobald der Laufcode geschrieben wird** — geführt als **eine** Backlog-Zeile (`K4j`, `docs/projektfuehrung/BACKLOG.md` Abschnitt 4): **(1)** `auswertung.py`, Datenvertrag Z. 40–58 — `kapital_drawdown_pct` kommt aus derselben Tagesreihe wie der Sharpe (eingefroren, gehört zu TB-30b); **(2)** `beispieldaten.py` Z. 24–26 und Z. 125 — rechnet den Drawdown heute ausdrücklich **nicht** aus der Tagesreihe und sagt im Kopf, das sei auch im echten Lauf so; **(3)** `registerdaten.py:70`, `FESTLEGUNGEN[1]` — Text präzisieren, sobald 1 und 2 stehen |
| ⭐ | **Der Laufcode selbst existiert nicht** — gemessen am 20.09.2026 (`FABLE_ANFRAGE_2026-09-20d_tagesreihe.md`): kein Code im Repo schreibt `zellen.csv` oder `tagesreihen/<zelle_id>.csv` ausser `beispieldaten.py` (erfundene Werte). Deshalb ist 24.2 eine **Spezifikation** für ungeschriebenen Code, kein Umbau — und *„Lauf wiederholen"* kostet nichts, weil der Lauf nicht begonnen hat |
| ⚠️ | **`t3_supertrend` nicht auf 2019 umgestellt** — das ist TB-72 (Berichtigung nach 21.3 (b) plus Ableitung der ersten Falte aus dem Trockenlauf; Fable, dritte Antwort Teil 2, vierte Antwort Punkt (2)) |
| ⚠️ | **Die MtM-Wirkung nicht gemessen** — das ist TB-73, und es darf erst nach diesem Abschnitt laufen (24.3) |
| ⚠️ | **Die Sperrlisten-Änderung nicht vollzogen** (21.9, 23.7): `benchmark_drawdowns_vt.json` liegt weiter daneben |
| | **Kein Selektionslauf, kein signierter Tag, kein Zeitanker.** Der Tag bleibt der nächste Meilenstein und gehört dem Betreiber (Abschnitt 13) |

---

### In einfacher Sprache

**Worum es ging:** Jeder Bot muss eine Verlustgrenze einhalten — er darf in
einem Jahr nicht tiefer fallen als ein Vielfaches des Vergleichskorbs. Dafür
muss man messen, wie tief der Bot gefallen ist. Im Regelwerk standen dazu zwei
Sätze, die sich widersprachen: Der eine sagte, der Verlust wird jeden Tag zum
Marktpreis gemessen. Der andere nannte ein Programm, das nur bei Käufen und
Verkäufen misst — und dazwischen nichts sieht. Eine Position, die zwischendurch
20 % im Minus war und mit −3 % verkauft wurde, zählt dort als −3 %.

**Was entschieden ist:** Die tägliche Messung gilt — weil nur sie zeigt, was
das Konto an einem Tag wirklich wert ist. Das alte Mass verschwindet nicht,
es wird weiter berichtet; nur entscheiden tut es nichts mehr. Die frühere
Untersuchung, aus der die alte Festlegung kam, war nicht falsch: Sie hatte
drei Messarten verglichen, und die vierte — die tägliche — war nur nicht
dabei.

**Warum dieser Abschnitt vor der Zahl steht:** Wie gross der Unterschied
zwischen beiden Messarten ist, weiss noch niemand. Das wird gemessen — aber
erst jetzt, nachdem hier steht, dass die Grösse für die Entscheidung keine
Rolle spielt. Sonst würde die Zahl, sobald sie da ist, zum Argument: „ändert
wenig, also nicht der Mühe wert" oder „ändert viel, also zu riskant". Eine Zahl,
die nichts entscheiden darf, soll nicht auf dem Tisch liegen, während
entschieden wird.

**Was jetzt anders ist:** Nichts am Programm — der Teil, der diese Zahlen
einmal berechnen wird, ist noch nicht geschrieben. Drei Stellen, die ihm
folgen müssen, stehen im Backlog. Und was bekannt ist, steht hier, obwohl es
unbequem ist: Die neue Messung ist für alle neun Bots strenger, nie milder.

*Nachgetragen in TB-71, 20.09.2026. Präzisierung nach Betreiberentscheidung:
sie nennt den Widerspruch, die Fundstellen, den Registertext, die
Entscheidungsregel und die Vorgeschichte — und entfernt nichts.*

---

### 24.6 Tatsachennotiz zu 24.3 und 24.4 — die gemessene Wirkung (TB-73, 20.09.2026)

**Datiert angehängt. Nichts entfernt, kein bestehender Satz umgeschrieben.**
Die Zeile *„Wirkung, gemessen — noch nicht"* in 24.4 bleibt stehen; hier steht
die Zahl, die sie ankündigt. **Diese Notiz berichtet. 24.3 hat entschieden,
bevor sie existierte, und sie wirft nichts erneut auf.** Kein Satz hier ist
eine Bewertung, eine Empfehlung oder eine Abwägung; keine Bot-Zahl steht neben
`erlaubt(f)`, `DD_Benchmark` oder `DD_Toleranz`.

**Herkunft:** `research/mtm_drawdown/` (Forschungsskript ausserhalb des
Laufcodes, `BERICHT.md` dort), gemessen am 20.09.2026 auf dem Mac
(`trading-env/bin/python3` 3.9.6) an den TB-24-Trade-Listen
(`research/tb24_haltedauern/daten/<bot>_positionen.csv`) und den Kursdateien in
`data/`; Falten aus `research/vorregistrierung/ergebnisse/faltenplan_tb72.json`
(TB-72). Ergebnisdokument `docs/ERGEBNIS_TB-73_mtm_wirkung.md`. Nichts in
`research/vorregistrierung/`, `shared/`, `strategies/` berührt; die drei
Sperrlisten-Hashes (`a163c498…`, `4549395f…`, `0e54ac5c…`) und die beiden
`_tb72`-Dateien byteweise unverändert.

**Was gemessen wurde, in einem Satz je Grösse:**

| | |
|---|---|
| **E** | der ereignisindizierte Drawdown je Falte — `capital_after` je Ausstieg aus `shared/zuteilung.py::simuliere_portfolio` (TB-24-Liste), Drawdown mit `shared/messkette.py::max_drawdown_ungerundet`, Basis der Kapitalstand vor Faltenbeginn. Das ist die Grösse, die Festlegung 1 bis 24.2 meinte |
| **M** | der tägliche Mark-to-Market-Drawdown je Falte auf **denselben ausgeführten Positionen**: an jedem Kurstag der 1d-Dateien Buchwert plus Bewertung der am Tagesschluss offenen Positionen zum Schlusskurs (`allocation · (close/entry − 1 − Kosten_Seite)`), Ausstiege mit dem realisierten `pnl_pct`; Kosten aus dem Backtest-Modul des Bots importiert. Das ist die Grösse aus 24.2 / Registertext 1a |
| **Grundlage** | die neun TB-24-Listen: Kapitalkette schliesst bei allen neun, `entry_price` = Schlusskurs der Einstiegskerze (max. Abweichung 2,2e-16), 1d-Kurse decken jeden Tagesschluss mit offener Position (0 fortgeschriebene Kurstage bei 149 000 Positionstagen) |

⚠️ **Was nicht messbar ist:** Die fünf Krypto-Listen beginnen zwischen
2021-09-01 und 2022-03-17 (Datenstand vor dem TB-34-Neuaufbau, 1 826
Tageszeilen). **Die Falten 2018, 2019 und 2020 aller Krypto-Bots haben keine
Grundlage** (dazu 2021 bei `rsi2_crypto` und `volatility_breakout_crypto`), je
eine Falte ist nur teilweise gedeckt. **2020 ist bei keinem Krypto-Bot
messbar.** Diese Falten tragen keine Zahl. Die Aktien-Listen (ab 2016-09-01)
decken alle Falten.

**Die Wirkung, je Bot und je Falte** (E → M, Prozent; **fett: 2020 und 2022**;
ᵗ = Liste beginnt in der Falte; ⚠️ = M flacher als E; „keine" = keine
Grundlage; „″" = zweites Jahr einer Zweijahresfalte; 2026 = Bestätigungsperiode
bis 2026-09-01 ausschliesslich, nicht im Median):

| Bot | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | Median Sel. E → M |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `elliott_wave` | · | keine | ″ | **-2,81** → **-4,48** ᵗ | ″ | **-10,17** → **-15,40** | ″ | -4,51 → -7,43 | ″ | -3,11 → -3,34 | -4,51 → -7,43 |
| `t3_supertrend` | · | · | keine | keine | -5,58 → -8,67 ᵗ | **-12,28** → **-14,11** | -11,55 → -11,25 ⚠️ | -6,20 → -10,79 | -16,41 → -19,61 | -9,92 → -11,79 | -11,55 → -11,25 |
| `rsi2_crypto` | · | · | keine | keine | keine | **-8,65** → **-10,15** ᵗ | -2,75 → -4,01 | -13,30 → -16,53 | -11,43 → -12,71 | -3,14 → -4,28 | -10,04 → -11,43 |
| `turtle_soup_crypto` | · | keine | keine | keine | -15,29 → -16,43 ᵗ | **-27,86** → **-30,38** | -20,68 → -21,53 | -18,00 → -19,42 | -27,42 → -35,29 | -16,03 → -22,25 | -20,68 → -21,53 |
| `volatility_breakout_crypto` | · | keine | keine | keine | keine | **-6,07** → **-10,39** ᵗ | -12,90 → -12,84 ⚠️ | -14,40 → -15,42 | -5,22 → -7,86 | -7,27 → -9,63 | -9,48 → -11,62 |
| `elliott_wave_stocks` | -0,99 → -5,26 | -4,85 → -9,22 | -4,86 → -8,61 | **-13,35** → **-9,45** ⚠️ | -3,88 → -5,34 | **-19,31** → **-18,11** ⚠️ | -1,96 → -4,53 | -3,26 → -6,14 | -8,92 → -11,91 | -5,74 → -11,71 | -4,85 → -8,61 |
| `rsi2_mean_reversion` | · | -11,49 → -14,92 | -6,46 → -7,66 | **-9,01** → **-11,28** | -3,53 → -5,53 | **-10,52** → **-11,93** | -8,69 → -9,21 | -4,45 → -5,48 | -5,33 → -7,49 | -3,84 → -5,51 | -7,57 → -8,44 |
| `turtle_soup_stocks` | -1,26 → -2,42 | -12,15 → -14,93 | -4,74 → -6,86 | **-29,91** → **-34,45** | -3,30 → -6,39 | **-18,73** → **-20,69** | -4,54 → -7,07 | -5,19 → -7,42 | -12,02 → -18,74 | -3,81 → -6,24 | -5,19 → -7,42 |
| `volatility_breakout` | · | -14,78 → -15,36 | -7,85 → -9,05 | **-9,41** → **-12,60** | -3,38 → -5,55 | **-23,97** → **-25,80** | -10,70 → -12,08 | -5,39 → -6,15 | -12,31 → -15,36 | -4,90 → -4,37 ⚠️ | -10,05 → -12,34 |

**Die beiden Falten aus Fables Warnung (24.3), einzeln:**

| Bot | 2020: E → M | Differenz | Faktor M/E | 2022: E → M | Differenz | Faktor M/E |
|---|---|---:|---:|---|---:|---:|
| `elliott_wave` | 2020-2021 (ab 2021-09-22): −2,81 → −4,48 | −1,67 pp | 1,59 | 2022-2023: −10,17 → −15,40 | −5,23 pp | 1,51 |
| `t3_supertrend` | keine Grundlage | | | −12,28 → −14,11 | −1,83 pp | 1,15 |
| `rsi2_crypto` | keine Grundlage | | | (ab 2022-02-11) −8,65 → −10,15 | −1,50 pp | 1,17 |
| `turtle_soup_crypto` | keine Grundlage | | | −27,86 → −30,38 | −2,52 pp | 1,09 |
| `volatility_breakout_crypto` | keine Grundlage | | | (ab 2022-03-17) −6,07 → −10,39 | −4,32 pp | 1,71 |
| `elliott_wave_stocks` | −13,35 → −9,45 ⚠️ | +3,90 pp | 0,71 | −19,31 → −18,11 ⚠️ | +1,20 pp | 0,94 |
| `rsi2_mean_reversion` | −9,01 → −11,28 | −2,27 pp | 1,25 | −10,52 → −11,93 | −1,41 pp | 1,13 |
| `turtle_soup_stocks` | −29,91 → −34,45 | −4,54 pp | 1,15 | −18,73 → −20,69 | −1,96 pp | 1,11 |
| `volatility_breakout` | −9,41 → −12,60 | −3,19 pp | 1,34 | −23,97 → −25,80 | −1,83 pp | 1,08 |

**Die Zahlen, zusammengefasst — und nur neben den Faltenwerten oben gültig:**
In **59 von 64** Falten mit Grundlage ist M tiefer als E. Der Median der
Differenzen je Bot über seine Selektionsfalten mit Grundlage liegt zwischen
**−1,39 pp** (`rsi2_crypto`) und **−3,09 pp** (`t3_supertrend`); der Faktor
M/E je Falte zwischen 1,04 (10.-Perzentil) und 1,88 (90.-Perzentil), Median
1,30. Die grössten Differenzen in Prozentpunkten liegen nicht in 2020 oder
2022, sondern in 2025 (`turtle_soup_crypto` −7,87 pp, `turtle_soup_stocks`
−6,72 pp) und in der Bestätigungsperiode 2026 (`turtle_soup_crypto` −6,22 pp,
`elliott_wave_stocks` −5,97 pp). Bei den vier Aktien-Bots ist 2020 in drei
Fällen die Falte mit der grössten oder zweitgrössten Differenz des Bots.

⚠️ **Tatsachennotiz zur Richtung — der Satz im Kopf dieses Abschnitts
(*„der tägliche Drawdown ist nie flacher als der ereignisweise"*) ist eine
Näherung, keine Eigenschaft der Rechnung.** Gemessen: in **5 von 64** Falten
ist M flacher als E — `t3_supertrend` 2023 (+0,30 pp),
`volatility_breakout_crypto` 2023 (+0,06 pp), `elliott_wave_stocks` **2020**
(+3,90 pp) und **2022** (+1,20 pp), `volatility_breakout` 2026 (+0,53 pp).
In jedem der fünf Fälle liegen am Tiefpunkt der Ereigniskurve **unrealisierte
Gewinne** in offenen Positionen (`elliott_wave_stocks` 2020: +2 055 in sechs
März-Einstiegen, die E erst beim Ausstieg im Juli/August sieht; das Tief von M
liegt am 18.03.2020 bei −9,45 %, das von E am 13.05.2020 bei −13,35 %). Die
Ereigniskurve bewertet offene Positionen zum Einstand — das lässt sie
unrealisierte Verluste **und** unrealisierte Gewinne nicht sehen; welche
Richtung die Abweichung nimmt, hängt davon ab, was am Tiefpunkt im Buch liegt.
Von Hand nachgerechnet in `research/mtm_drawdown/test_mtm_kern.py`, Probe 3;
jeder Fall zerlegt in `research/mtm_drawdown/ergebnisse/richtungsfaelle.md`.
Der Pfad ist in keinem der fünf Fälle falsch: ein Pfad, der „M ≤ E" erzwänge,
müsste unrealisierte Gewinne ignorieren und wäre nicht mehr Mark-to-Market.
Gegenprobe: in 0 von 64 Falten ist E flacher als die Ereigniskurve am
Tagesende (E_tag) — erwartet, jeder Tagesendwert ist ein E-Punkt.

**Zwei Feststellungen zum Auftrag, gemessen statt übernommen:** (a) Der
Auftrag verlangte E gegen M *„bei 25 / 50 / 100 % Exposure"*. Diese Stufen
sind das Argument des **Benchmarks** (`DD_Benchmark(f, e)`, Abschnitt 4.2); ein
Bot hat je Falte **eine** Exposure, die aus seinen Positionen folgt — sie
steht in `research/mtm_drawdown/ergebnisse/messung.md` neben jeder Falte (z. B.
`turtle_soup_stocks` 0,66–0,86; `elliott_wave` 0,04–0,06). Sie auf drei Stufen
zu setzen hiesse andere Positionen oder Hebel; beides wäre eine erfundene
Zahl. (b) Der Bot-Median über die Selektionsfalten führt zu keiner Grösse
dieses Registers — `DD_Toleranz` ist der Median der **Benchmark**-Drawdowns
(Festlegung 5). Er steht oben als Beschreibung, nicht als Grösse der Regel.

**Was diese Notiz ausdrücklich NICHT tut:** Sie bewertet nichts, empfiehlt
nichts, wirft 24.3 nicht erneut auf. Sie vergleicht keine Bot-Zahl mit einer
Grenze. Sie ändert keinen Code, keine Sperrlisten-Datei, keinen Registertext;
`K4j` (drei Code-Stellen, sobald der Laufcode geschrieben wird) bleibt, wie
es ist, und die Grösse der Abweichung ist für keine dieser Stellen ein
Argument (24.3). Sie ersetzt die fehlenden Krypto-Falten 2018–2020 nicht durch
neue Backtests. Sie setzt keinen Tag.

*Nachgetragen in TB-73, 20.09.2026. Tatsachennotiz: sie nennt die Grundlage,
die Lücke, die Zahlen je Falte, die fünf Gegenfälle mit ihrem Grund — und
entscheidet nichts.*

> ⭐ **Nachtrag zur Lücke (TB-77, 21.09.2026; Fable, Kurzfassung vom 21.09., Teil 2 (5)):** Die Lücke *„Krypto 2018–2020 nicht messbar"* betrifft **nur die TB-24-Trade-Listen dieser Messung**, nicht den Lauf. Fable stellt klar: *„der Snapshot enthält Krypto 2018–2020, die Nebenbedingung wird dort gerechnet."* Nachgemessen 21.09.2026 am gezogenen Snapshot `63e4b6c8…` (Abschnitt 18): `BTCUSDT_1d.csv` und `ETHUSDT_1d.csv` beginnen am **2017-08-17** (3 317 Zeilen bis 2026-09-14); **6 der 24** Krypto-1d-Dateien beginnen vor dem 01.01.2019. Der Selektionslauf rechnet die Nebenbedingung in den Falten 2018–2020 auf diesem Bestand; was oben fehlt, ist allein die Vorab-Messung der MtM-Wirkung für diese Falten. Die Tabelle oben bleibt, wie sie ist.

---

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

## 26. Präzisierung zu Registertext 4a, Bedingung (i) — der Datenhorizont ist ein absolutes Datum je Bot, nicht je Symbol (TB-77, 21.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Satz wird umgeschrieben**
— die Neufassung 4a / 21.3 (b) in 25.3 bleibt stehen (dort seit heute mit der
Marke *„(i) PRÄZISIERT durch Abschnitt 26"*), Registertext 3 (c) in 15.5 bleibt
stehen (Marke *„ERGÄNZT durch Abschnitt 26, 26.4"*), die Tatsachennotiz 21.4
bleibt unverändert gültig. Das ist die Form aus
`docs/projektfuehrung/DOKUMENTATIONSSTANDARD.md`, Regel 4, und die Form der
Abschnitte 21, 23, 24 und 25.

**Anlass:** Fables fünfte Antwort vom 20.09.2026
(`FABLE_ANTWORT_2026-09-20e_konjunktion.md`, Abschnitt (3)) hatte *„im
Datenhorizont"* als `asof` minus `RECENT_YEARS_ONLY` präzisiert und einen
dritten, ungefragten Befund danebengelegt: die Bots rechnen das Fenster **je
Symbol**, der Faltenplan **je Markt**. Abschnitt 25 hat beides ausdrücklich
offen gelassen (25.3, Tatsachennotiz Zeile „Bedingung (i)"; 25.5: *„Bedingung
(i) nicht präzisiert — TB-74"*). Die Anfrage
`FABLE_ANFRAGE_2026-09-21a_horizont_und_grenzfall.md` (Teil 1, Fragen (1) und
(2)) hat die Entscheidung erbeten; Fable hat sie am 21.09.2026 getroffen.

⚠️ **Herkunft des Wortlauts, nicht geglättet:** Fables Antwort vom 21.09. liegt
**nicht im Repo** — gemessen 21.09.2026 (`find` über das Repo: 0 Treffer für
`FABLE_ANTWORT_2026-09-21a*`; die Anfrage hatte um Ablage in der Projektablage
gebeten, `FABLE_UEBERGABE_2026-09-21_neuer_chat.md` Z. 9: *„sie kam als Datei
zurück"*). Der Wortlaut in 26.1 und 26.2 ist **zeichengleich aus
`docs/auftraege/MAC_TB-77_horizont_je_bot.md`, Abschnitt 0**, übernommen, das
ihn aus der Antwort zitiert. Das ist der einzige Träger im Repo; die Ablage der
Antwort selbst ist eine offene Bringschuld des steuernden Chats (26.6).

**Art der Änderung nach der Drei-Kategorien-Regel (F17): eine Präzisierung,
Quelle des Grundes ist die Regel** — Registertext 4a (*„im registrierten
Datenhorizont"*) und Registertext 5e (der Lese-Audit, 17.4: kein Lesezugriff
ausserhalb des registrierten Horizonts). Eine Wirkung auf eine Zahl ist **nicht
bekannt und nicht gemessen** (26.6): es hat kein Selektionslauf stattgefunden,
kein Parametersatz ist bewertet, kein Ergebnis erzeugt. ⛔ **Dieser Abschnitt
rechnet nicht und fasst keinen Code an** — die vier `multi_symbol_optimise.py`
und `auswertung.py` sind unberührt (Nachweis: `git diff --numstat` in
`docs/ERGEBNIS_TB-77_horizont_je_bot.md`).

---

### 26.1 Der Befund — das Fenster je Symbol erzeugt Einstiege ausserhalb aller Falten, und sie laufen durch den Kapitalpfad

**Was der Code tut, gemessen 21.09.2026 (Stand `2e9cdf9`):**

| | Fundstelle | Wortlaut |
|---|---|---|
| Die Konstante | `strategies/elliott_wave_stocks/multi_symbol_optimise.py:54`, `rsi2_mean_reversion/…:52`, `turtle_soup_stocks/…:46`, `volatility_breakout/…:49` | `RECENT_YEARS_ONLY = 10`, bei allen vier Aktien-Bots, in Jahren (`pd.DateOffset(years=…)`). Die fünf Krypto-Bots haben keine |
| Der Bezug | dieselben Dateien, Z. 93 / 93 / 81 / 88 | `entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)` — relativ zum **letzten Kurs der Datei**, nicht zum Laufdatum (Datenuhr) |
| ⚠️ **Je Symbol** | dieselben Zeilen, **innerhalb der Ladeschleife** `for symbol in SYMBOLS`; abgelegt je Symbol (`data[symbol] = (df_ind, entry_cutoff)`, Z. 96 / 83 / 91; `elliott_wave_stocks` kappt in Z. 94 die Kursreihe des Symbols selbst) | Jedes Symbol bekommt sein eigenes Fenster, das an **seinem** letzten Kurstag hängt |
| Der Plan | `research/faltenplan_neun/faltenplan_neun.py::fensteranker`, Z. 271, Docstring Z. 272–278 | *„Genommen wird der SPAETESTE letzte Kurstag des Marktes, damit alle Symbole desselben Bots auf demselben Fenster liegen."* — **je Markt** |

**Das ist nicht dasselbe.** Ein Symbol, dessen Datei früher endet — delistet,
Datenlücke, stehengebliebene Datei —, bekommt beim Bot ein früheres Fenster und
liefert Trades aus einem Zeitraum, den der Plan für ausgeschlossen hält (so
gestellt in `FABLE_ANFRAGE_2026-09-21a…`, Teil 1 (c)).

⭐⭐ **Fables Begründung, und sie ist der eigentliche Befund — wörtlich** (aus
seiner Antwort vom 21.09.2026, zitiert nach `MAC_TB-77_horizont_je_bot.md`,
Abschnitt 0): Ein Symbol mit früherem Fenster erzeugt Trades aus Jahren **vor
der ersten Falte**. Die tauchen in keiner Falte auf —

> *„aber sie laufen durch den Kapitalpfad, belegen Plätze, verändern das
> Kapital, mit dem die erste Falte beginnt. Das ist ein Lesezugriff auf Zeiten
> ausserhalb des registrierten Horizonts, nur nicht über eine Datei, sondern
> über ein Fenster. Der Lese-Audit (5e) sieht ihn nicht, weil die Datei im
> Manifest steht."*

Deshalb ist die Frage *„je Bot oder je Symbol"* keine Handwerksfrage: Ein
Fenster je Symbol ist eine Lücke in Registertext 5e, die keine Datei und kein
Hash sichtbar macht — der Kapitalpfad (Registertext 1a) beginnt die erste
Falte mit einem Kapitalstand, der aus nicht registrierten Jahren stammt.

---

### 26.2 Der Registertext — Fables Präzisierung vom 21.09.2026, zeichengleich

**Ersetzt seine Fassung vom 20.09.2026** (`FABLE_ANTWORT_2026-09-20e_konjunktion.md`,
Abschnitt (3): *„4a, Präzisierung. ‚Im Datenhorizont' heisst: ab dem
Horizontbeginn des Bots, berechnet als registriertes `asof` (5a) minus
`RECENT_YEARS_ONLY` des Bots; das Ergebnis steht je Bot als absolutes Datum in
der Tatsachennotiz zu 4d. Der Vorlauf wird gegen dieses Datum gerechnet, nicht
gegen den ersten Kurs im Bestand."*). ⭐ **Gemessen 21.09.2026: diese Fassung
vom 20.09. ist nie in einen Registertext übernommen worden** — `grep -c` im
Register: `Horizontbeginn` **0**, `4a, Präzisierung` **0**; 25.3 und 25.5
verweisen sie ausdrücklich an TB-74. Es gibt darum im Register keine Stelle,
die als ERSETZT zu markieren wäre; ersetzt wird ein Wortlaut, der nur in
Fables Antwortdatei steht. Präzisiert wird die Neufassung in **25.3**,
Bedingung (i) *„im registrierten Datenhorizont des Bots"*, die stehen bleibt.

> **4a, Präzisierung (ersetzt die Fassung vom 20.09.).** Der Datenhorizont eines
> Bots ist ein absolutes Datum je Bot: Horizontbeginn = `asof` (5a) minus
> `RECENT_YEARS_ONLY` des Bots; Bots ohne diese Konstante haben keinen Horizont
> (Krypto). Das Datum steht je Bot in der Tatsachennotiz zu 4d. Es gilt für alle
> Symbole des Bots gleich; ein Symbol trägt vor dem Horizontbeginn keinen
> Einstieg bei, unabhängig davon, wann seine Kursdatei beginnt oder endet. Das
> Ende der Kursdatei eines Symbols bestimmt nach 3b (b), an welchen Tagen es
> handelbar ist — nie sein Fenster.

**Was der Text festlegt, in drei Sätzen:** Das Fenster ist eine Zahl **je
Bot**, und der Code muss nachgeben, nicht der Plan (Antwort auf Frage (1) der
Anfrage). Es hängt an `asof` aus Registertext 5a — dem Bezugsdatum, das *„aus
dem Register, nie aus der Uhr"* kommt (17.1) —, nicht am letzten Kurs einer
Datei. Und das Ende einer Kursdatei behält genau eine Rolle: es entscheidet
nach 3b (b), an welchen Tagen das Symbol handelbar ist.

⚠️ **Was der Text braucht und was es heute nicht gibt:** `asof`. Registertext
5a sagt seit TB-48, woher es kommt; **es steht nirgends als Wert** — gemessen
21.09.2026 in allen `.py` (8 Zeilen, alle pandas `merge_asof`), allen `.json`
(1 Eintrag, derselbe Bezeichner), im Register (3 Zeilen, Formel und Herkunft),
in `ergebnisse/`, im Snapshot-Manifest (15 Schlüssel, keiner `asof`), in
`registerdaten.py` und in `docs/` (`docs/belege/TB-77/schritt1_blocker_nachgemessen.md`,
Nachweis 2). *Ein Registertext, der auf einen Wert zeigt, den es nicht gibt,
ist kein Fehler — solange er sagt, dass es ihn nicht gibt.* Das tut 26.3.

---

### 26.3 Tatsachennotiz zu 4d — der Horizontbeginn je Bot: ⚠️ Platzhalter, weil `asof` nicht gesetzt ist

Nach 26.2 steht das Datum je Bot in der Tatsachennotiz zu 4d (21.4). **Es kann
heute nicht eingetragen werden**, weil der Minuend fehlt. Nach dem Muster von
23.3 (Fassung TB-66) steht hier ein sichtbarer Platzhalter und **keine
erfundene Zahl**:

| Bot | Markt | `RECENT_YEARS_ONLY` | Horizontbeginn = `asof` − Konstante |
|---|---|---:|---|
| `elliott_wave` | krypto | keine | **kein Horizont** (26.2) |
| `t3_supertrend` | krypto | keine | **kein Horizont** |
| `rsi2_crypto` | krypto | keine | **kein Horizont** |
| `turtle_soup_crypto` | krypto | keine | **kein Horizont** |
| `volatility_breakout_crypto` | krypto | keine | **kein Horizont** |
| `elliott_wave_stocks` | aktien | 10 Jahre | ⚠️ **[PLATZHALTER — `asof` ist nicht gesetzt; Datum folgt, sobald 5a einen Wert hat]** |
| `rsi2_mean_reversion` | aktien | 10 Jahre | ⚠️ **[PLATZHALTER — `asof` ist nicht gesetzt; Datum folgt, sobald 5a einen Wert hat]** |
| `turtle_soup_stocks` | aktien | 10 Jahre | ⚠️ **[PLATZHALTER — `asof` ist nicht gesetzt; Datum folgt, sobald 5a einen Wert hat]** |
| `volatility_breakout` | aktien | 10 Jahre | ⚠️ **[PLATZHALTER — `asof` ist nicht gesetzt; Datum folgt, sobald 5a einen Wert hat]** |

Die Konstante je Bot ist aus dem Code **gelesen** (Fundstellen 26.1), nicht
registriert; ob sie als registrierte Grösse in `registerdaten.py` gehört, ist
Teil von 26.6.

⚠️ **Abgegrenzt, damit es niemand für den Wert hält:** 15.6, Punkt 3, nennt
seit dem 15.09.2026 *„gemessen vom letzten Kurstag (2026-09-01) zurück auf
2016-09-01 — so rechnen die vier Aktien-Bots selbst."* Das ist die **Datenuhr**
(letzter Kurs im damaligen Bestand), also genau der Bezug, den 26.2 ablöst —
**kein `asof`** und kein Horizontbeginn im Sinne dieses Abschnitts. Der Wert
wandert nicht in die Tabelle. Wann und wodurch `asof` gesetzt wird, ist als
Frage (1) in `FABLE_UEBERGABE_2026-09-21_neuer_chat.md`, Abschnitt 4, an Fable
gestellt (Lesart des steuernden Chats dort: *„mit dem Snapshot und dem
signierten Tag zugleich"* — **nicht entschieden, hier nicht vorweggenommen**).

**Was der Platzhalter für den Faltenplan bedeutet:** Bedingung (i) wird bis
zum Eintrag *„wie bisher"* gerechnet (25.3, Tatsachennotiz), also mit dem
Fenster aus `faltenplan_neun.fensteranker` (je Markt, Datenuhr). Die
Faltenliste 21.4 ist damit **vorläufig in (i)** und **endgültig in (ii)**; nach
15.6 Punkt 3 *„bindet das Fenster die Faltenliste nicht"* — ob das mit einem
registrierten `asof` so bleibt, ist erst mit dem Wert prüfbar.

---

### 26.4 Ergänzung zu Registertext 3 (c) — die Reichweite des Survivorship-Vorbehalts

Registertext 3 (c) (15.5) trägt den Vorbehalt *„Beide sind
survivorship-behaftet … Grösse unbekannt"*. Er bleibt zeichengleich stehen und
wird ergänzt:

> **3 (c), Ergänzung (TB-77, 21.09.2026):** Der Survivorship-Vorbehalt gilt für
> die Jahre im Horizont; dass der Horizont zehn Jahre umfasst, begrenzt die
> Reichweite des Vorbehalts, ändert ihn nicht.

*Warum die Ergänzung nötig ist:* `RECENT_YEARS_ONLY` steht im Code als
Gegenmassnahme gegen den Survivorship-Bias (`multi_symbol_optimise.py:52`
und `:49`: *„reduziert Survivorship Bias"*; `UEBERGABEPROTOKOLL.md` Z. 170).
Ein Leser könnte den Horizont darum für eine **Milderung** des Vorbehalts
halten. Er ist keine: Innerhalb der zehn Jahre ist das Universum dieselbe
heutige Liste, mit derselben erwarteten Richtung (*„Bevorzugung von Sätzen mit
weiten oder fehlenden Stops und langen Zeitbremsen"*). Der Horizont sagt nur,
**für welche Jahre** der Vorbehalt ausgesprochen wird.

---

### 26.5 Tatsachennotiz zur Herkunft — alle bisherigen Ergebnisdateien der vier Aktien-Bots sind mit Fenstern je Symbol gerechnet

Gemessen 21.09.2026 (`docs/belege/TB-77/schritt1_blocker_nachgemessen.md`,
letzter Abschnitt): `results/<bot>/multi_symbol_optimisation_results.csv` hat
bei jedem der vier Aktien-Bots genau **einen** Commit und ist seitdem
unverändert; im selben Commit steht der Optimierer bereits mit
`df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)` innerhalb der
Ladeschleife, und `git log -S` kennt keinen älteren Stand des Ausdrucks:

| Bot | Ergebnisdatei (Commit) | Optimierer je Symbol seit |
|---|---|---|
| `elliott_wave_stocks` | `0f6491b`, 02.09.2026 | `0f6491b` |
| `rsi2_mean_reversion` | `f56c6d2`, 03.09.2026 | `f56c6d2` |
| `turtle_soup_stocks` | `88b9050`, 04.09.2026 | `88b9050` |
| `volatility_breakout` | `b603861`, 03.09.2026 | `b603861` |

**Folge:** Jede dieser Tabellen ist mit einem Fenster **je Symbol** an dessen
letztem Kurstag gerechnet — nicht mit dem Horizont aus 26.2. Das ist **ein
Grund mehr**, warum sie mit den Zahlen des Laufs nicht vergleichbar sind; die
anderen Gründe stehen in Registertext 7 (Backtester-Prüfung, 16.5) und in der
Warnung zu den Papierpfaden vor dem Umstellungstag (`CLAUDE.md`, TB-38). Sie
bleiben liegen, wo sie liegen, und werden nicht neu gerechnet (26.6). *Nicht
gemessen:* ob weitere, abgeleitete Ergebnisse unter `research/` dieselben
Loader importiert haben; wo sie es taten, gilt dasselbe.

---

### 26.6 Was folgen muss — und hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **`asof` setzen.** Wann und wodurch, ist Fables Frage (1) im neuen Chat; die Lesart *„mit Snapshot und Tag zugleich"* ist nicht entschieden. Bis dahin bleibt 26.3 ein Platzhalter | Betreiber / Fable, vor dem Tag |
| ⛔ | **Tatsachennotiz 4d füllen:** vier Daten in 26.3, je `asof` minus zehn Jahre, mit Fundstelle des `asof`-Wertes. Danach prüfen, ob das Fenster die Faltenliste 21.4 in (i) weiterhin nicht bindet | Registernachtrag, sobald `asof` steht |
| ⛔ | **Die vier Optimierer:** `entry_cutoff` **einmal je Bot aus dem Register** statt je Symbol aus `df["open_time"].max()` (Fundstellen 26.1). Sie brauchen denselben Wert; ohne `asof` gibt es nichts einzutragen | **TB-30b** (Umstellung des Laufcodes) |
| ⛔ | **Die Wache** *„kein Einstieg eines Bots liegt vor dessen Horizontbeginn"* — Fable schlägt sie *„billig, in den Auswerter"* vor. `auswertung.py` ist **eingefroren** (Abschnitt 0, Z. 31; 15.8 Nr. 3; Sperrliste 10 Nr. 5); ein eingefrorenes Skript, das einmal geöffnet wird, ist nicht mehr eingefroren. **Samt Mutationsprobe:** Fenster je Symbol wieder einschalten → die Wache muss rot werden | **TB-30b**, mit den Optimierern |
| ⛔ | **Fables Antwort vom 21.09. ablegen** (`FABLE_ANTWORT_2026-09-21a_horizont_und_grenzfall.md`) — sie liegt in keinem Träger; bis dahin trägt Abschnitt 0 des Auftrags den Wortlaut | steuernder Chat |
| ⚠️ | **`RECENT_YEARS_ONLY` als registrierte Grösse** (`registerdaten.py`) statt als Codekonstante, die aus vier Dateien gelesen wird — Fable nennt sie *„registrierte Konstante"* (20.09., Abschnitt (3)); eingetragen ist sie nur als Tatsachennotiz (15.6 Punkt 3, 26.3). Ob das eine Registeränderung oder eine Codekopie ist, entscheidet der Betreiber (vgl. `T56b.6`: keine Konstantenkopien) | Entscheidungsvorlage, nicht vollzogen |
| ⚠️ | **Nicht gemessen:** ob und wie viele Einstiege in den bisherigen Ergebnisdateien vor einem Horizontbeginn liegen. Ohne `asof` gibt es die Grenze nicht, gegen die man zählen könnte; und die Zahl wäre eine Aussage über Ergebnisse, die mit dem Lauf ohnehin nicht vergleichbar sind (26.5) | — |

⛔ **Nicht getan:** kein Bot-Code, kein `auswertung.py` (auch nicht der
Docstring), kein `registerdaten.py`, keine Sperrlisten-Datei
(`benchmark_drawdowns.json` `a163c498…`, `faltenplan.json` `0e54ac5c…`
byteweise unverändert), kein Tag, kein Lauf.

---

### 26.7 Der Grenzfall — was gilt, wenn für einen Bot kein Parametersatz besteht: die Kette (b) → Festlegung 11 → Registertext 6 (b) → Schatten

**Das ist ein Verweis, keine Berichtigung.** Fables Teil 2 vom 21.09.2026
(Antwort auf `FABLE_ANFRAGE_2026-09-21a…`, Teil 2, Fragen (3) und (4))
entscheidet den Fall, den die Anfrage für ungeregelt hielt — und die
Entscheidung steht bereits im Register, an vier Stellen, die bisher niemand als
Kette gelesen hat. **Jede Stelle nachgemessen 21.09.2026 (Stand `2e9cdf9`):**

| Glied | Fundstelle | Wortlaut |
|---|---|---|
| **1. Der Fall ist ein Abbruchkriterium** | Abschnitt 7, **(b)**, Z. 686; Präzisierung Z. 692–694 | *„**(b)** Kein Parametersatz erfüllt die Drawdown-Bedingung in allen Falten"* — *„Gewinnen kann nur ein zulässiger Punkt. Ist keiner zulässig, greift (b); berichtet wird dann der Plateau-Gewinner über alle Zellen, ausdrücklich mit der Markierung ‚nicht zulässig'."* |
| **2. Bleibt/Geht läuft über die Abbruchkriterien** | Abschnitt 1, **Festlegung 11** (`registerdaten.FESTLEGUNGEN[11]`) | *„DSR ist Bericht, nicht Tor — Bleibt-Geht läuft über die Abbruchkriterien."* Ein Bot, der (b) erfüllt, **bleibt nicht** |
| **3. Die Stufe** | 16.4, **Registertext 6, Buchstabe (b)** | *„jeder, der eines erfüllt, auf **Schatten** — sein Budgetanteil hält die statische Benchmark-Position in Höhe seines mittleren Exposures. Die Zuweisung ist Ergebnis des eingefrorenen Skripts, keine Lesung."* |
| **4. Was Schatten heisst, und der Weg zurück** | Registertext 6 (a) und (d), 16.4; Abschnitt 7.1 | Schatten: *„läuft, kein Portfoliogewicht, nicht in Portfolio-Zahlen und nicht am Crash-Knopf"* — mit seinen heutigen Parametern. Kapital: *„statische Benchmark-Position in Höhe des mittleren Exposures — nicht in Kasse, nicht zu den Überlebenden."* Rückkehr: *„nur über einen neuen registrierten Lauf"* (6 (d)); *„Kein ‚vorerst behalten'"* (7.1) |
| **5. Das Ergebnis ist zulässig, auch bei mehreren oder allen** | **Festlegung 12** (wörtlich, Abschnitt 1) und 7.1 | *„Es kann sein, dass kein einziger Bot die Schwelle erreicht."* — *„Die Anzahl ausscheidender Bots ist KEIN Grund, eine Schwelle zu ändern."* |

**Die Kette ist im eingefrorenen Skript bereits Code:** `auswertung.py::kapitalregel`
(Z. 554–576) gibt `kapitalregel`, `schattenregel`, `schwellenregel` und
`zulaessiges_ergebnis` (`rd.FESTLEGUNGEN[12][1]`) am Ende jeder Bleibt-Geht-Liste
aus; `test_vorregistrierung.py` Teil D prüft
`b_kein_satz_besteht_die_drawdown_bedingung` (Z. 288, 348–350). **Fällt ein
Bot nach (b), gibt es nach dem Lauf keine Entscheidung, nur eine Lektüre**
(Abschnitt 0).

⚠️ **Zwei Aktenzeichen aus Fables Antwort, nachgemessen und nicht übernommen**
(`registerdaten.FESTLEGUNGEN`, `docs/belege/TB-77/schritt1_blocker_nachgemessen.md`,
Nachweis 4): Fable nannte *„Festlegung 10"* für Bleibt/Geht über die
Abbruchkriterien — das ist **11** (10 ist die DSR-Basis, N = 653); und
*„Festlegung 11"* für „mehrere oder alle" — das ist **12**. Sein Vorbehalt
*„fehlt (b) im Registertext"* ist gegenstandslos: (b) steht in Abschnitt 7,
wörtlich.

⚠️ **Quelle, nicht geglättet:** Fable verweist für Teil 2 auf ein Dokument
`FABLE_ANTWORT_2026-09-20a_grenzfall`. **Es existiert nicht** — weder im Repo
(gemessen 21.09.2026, 13:50 durch den steuernden Chat; hier nachgemessen:
`find` 0 Treffer für `*grenzfall*` ausser der Anfrage vom 21.09.) noch in der
Projektablage (`FABLE_UEBERGABE_2026-09-21_neuer_chat.md`, Abschnitt 4 (3)).
Vom 20.09. liegen vier Antworten vor: Kalender, Kapitalpfad, MtM-Messung,
Konjunktion. **Quelle dieses Abschnitts ist allein seine Kurzfassung vom
21.09.2026**, wie sie der Auftrag (`MAC_TB-77_horizont_je_bot.md`, Schritt 3)
und die Übergabe an den neuen Chat (`FABLE_UEBERGABE…`, Abschnitt 3 (e))
wiedergeben — das fehlende Dokument wird nicht zitiert.

⭐ **Und die Antwort auf Frage (4) der Anfrage — ob vorab gemessen werden darf,
wie viele Sätze die härtere Bedingung kostet:** *nein.* Fable, nach
`FABLE_UEBERGABE…` Abschnitt 3 (e): *„Die Zahl der zulässigen Sätze je Bot ist
der Ausgang des Laufs — die erste Hälfte des Laufs selbst."* Das ist dieselbe
Linie wie 24.3 (*„vor jeder Messung"*), nur eine Stufe strenger: dort war die
Zahl folgenlos, hier wäre sie eine Aussage über den Ausgang. **Es wird nicht
gemessen.** Diese Sitzung hat es nicht getan (26.6, letzte Zeile).

---

### In einfacher Sprache

**Was entschieden ist:** Die „letzten zehn Jahre", auf die ein Aktien-Bot bei
der Auswahl schaut, gelten künftig für den ganzen Bot — nicht für jedes
Wertpapier einzeln. Heute rechnet jeder Bot das Fenster für jedes Wertpapier
von dessen letztem Kurs aus zurück. Endet die Kursdatei eines Wertpapiers
früher, liegt sein Fenster früher — und der Bot handelt darin in Jahren, die
offiziell gar nicht ausgewertet werden. Diese Geschäfte tauchen in keiner
Jahresfalte auf, aber sie verändern still das Kapital, mit dem das erste
ausgewertete Jahr beginnt. Der Lesewächter merkt das nicht, weil die Datei
selbst erlaubt ist.

**Was dabei auffiel:** Die neue Regel braucht ein Stichtagsdatum (`asof`), von
dem aus die zehn Jahre zurückgerechnet werden. Das Regelwerk sagt seit dem
18.09., dass es dieses Datum aus dem Register bekommt — **aber es steht
nirgends.** Gesucht wurde im ganzen Code, in allen Ergebnisdateien, im
Datenschnappschuss und im Register selbst. Und die Wache, die Fable
vorschlägt, gehört in eine Datei, die eingefroren ist und bis zum Umbau
(TB-30b) nicht angefasst wird.

**Was dieser Abschnitt deshalb tut:** Er schreibt die Regel wörtlich auf und
setzt dort, wo das Datum stehen müsste, einen sichtbaren Platzhalter — statt
eine Zahl zu erfinden. Das Datum, das dem Wert am nächsten kommt (2016-09-01
aus dem Jahr 2026 zurück), steht ausdrücklich daneben als das, was es ist: der
alte Bezug, nicht der neue. Ausserdem hält er fest, dass alle bisherigen
Auswahltabellen der vier Aktien-Bots noch mit dem alten Fenster je Wertpapier
gerechnet sind — ein Grund mehr, sie nicht mit dem Lauf zu vergleichen.

**Und der Grenzfall:** Was passiert, wenn für einen Bot am Ende gar keine
Einstellung die Verlustgrenze in allen Jahren einhält? Die Antwort stand
schon da, verteilt auf vier Stellen: Das ist Abbruchkriterium (b); der Bot
bleibt nicht; er läuft mit seinen heutigen Einstellungen als Schatten ohne
Geld weiter; sein Geld geht in eine feste Marktposition; zurück kommt er nur
über einen neuen, vorher registrierten Lauf. Und vorher nachzuzählen, wie
viele Einstellungen die härtere Grenze kostet, ist verboten — die Zahl verriete
den Ausgang.

*Nachgetragen in TB-77, 21.09.2026. Präzisierung mit Registertext, Platzhalter
und Verweis: sie nennt den Befund mit seinen Fundstellen, den Registertext mit
seiner Herkunft, den fehlenden Wert als fehlend, die Ergänzung zu 3 (c), die
Herkunft der bisherigen Ergebnisse, die Kette des Grenzfalls und das, was
nicht getan wird — und entfernt nichts.*

---

## 27. Sichtschutz des Verfahrensprüfers (Fable 21g, 21.09.2026)

⭐ **Neuer Registertext, keine Berichtigung.** Er regelt, was der
Verfahrensprüfer vor dem signierten Tag wissen darf — und damit, ob seine
Registerentscheidungen nachträgliche Wahlen sein können. Quelle des Grundes
nach F17; die Regel nennt kein Ergebnis.

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21g_sichtschutz_nullpunkt.md`,
Abschnitt 3, zeichengleich übernommen. Vorgeschichte: 21d (Fables Vorschlag),
dazu zwei Messungen des steuernden Chats vom 21.09. — das Register ist rein
(24 Sharpe-Erwähnungen, alle Regeltext, keine gemessene Kennzahl je
Parametersatz), `BACKLOG.md` ist es nicht (Z. 190 `W14`, Z. 170 `T39.2`).

### 27.1 bis 27.5 — der Registertext, zeichengleich

> **27. Sichtschutz des Verfahrensprüfers**
>
> **27.1** Der Verfahrensprüfer erhält vor dem signierten Tag keine Ergebnisgrössen des Selektionsraums: keine Kennzahl eines Parametersatzes (Sharpe, Rendite, Drawdown, Trefferquote, Anzahl Trades), keine Aussage, welche oder wie viele Sätze eine Bedingung erfüllen, keine Rangfolge, keine Plateau-Lage — **und keine Erwartung, Schätzung oder Prognose über den Ausgang des Laufs**, gleich ob als Zahl oder als Satz.
>
> **27.2** Zulässig sind Verfahrensmessungen — Kalender, Datenbestand, Faltenzahl, Handelbarkeit, Benchmark-Seite — und Wirkungen einer Regel auf die registrierten heutigen Parameter, wenn die Regel vor der Messung geschrieben stand (Bauart 24.3).
>
> **27.3** Das Register darf der Verfahrensprüfer vollständig lesen; was darin steht, hat dieses Tor bereits passiert (gemessen 21.09.: keine Kennzahl je Parametersatz im Registertext). Eine Ablage-Kopie trägt Commit-Hash, Datum und die Kennzeichnung KOPIE.
>
> **27.4** Der Verfahrensprüfer führt in jeder Antwort ein Leseprotokoll (welche Dateien er in diesem Chat gelesen hat). Das Protokoll ist Selbstauskunft. Die Prüfung, ob seine Begründungen Grössen nach 27.1 enthalten, ist Pflicht des steuernden Chats (Prüfprinzipien).
>
> **27.5** Wer dem Verfahrensprüfer einen Treffer nach 27.1 in einer Datei meldet, nennt Datei und Fundstelle, nicht den Inhalt.
>
> **Tatsachennotiz zu 27 — Anfangsbestand des Verfahrensprüfers beim Inkrafttreten (21.09.2026):**
> Der Chat des Verfahrensprüfers wurde am 21.09. neu begonnen; er kennt aus dem Vorgängerchat nichts. Sein Wissensstand beim Inkrafttreten ist vollständig: der Wortlaut von `FABLE_UEBERGABE_2026-09-21_neuer_chat.md` (Fassung 2) und die Dateien `FABLE_ANTWORT_2026-09-20e_konjunktion.md`, `FABLE_ANTWORT_2026-09-21a_horizont_und_grenzfall.md`, `FABLE_ANTWORT_2026-09-21b_asof_und_wache.md`, alle in der Projektablage. Darin enthaltene Grössen, die an 27.1 grenzen: die Wirkung von Abschnitt 23 auf die DD-Toleranz der fünf Krypto-Bots (2,4- bis 5,0-fach); die Zahlen aus 24.6 (59 von 64 Falten tiefer, Mediane je Bot −1,39 bis −3,09 Prozentpunkte, fünf Falten flacher; Krypto 2018–2020 nicht enthalten). Beides sind Wirkungen auf die heutigen Parameter, gemessen nach der jeweils vorher geschriebenen Regel (27.2). Dazu, am 21.09. durch eine Treffermeldung mitgeteilt: der Wortlaut der Erwartung in `BACKLOG.md` Zeile 190 (W14) über die Zahl der Bots auf Schatten — eine Erwartung nach 27.1, keine Messung; sie lag nach Festlegung 12 als Möglichkeit bereits vor. Weitere Grössen nach 27.1 kennt der Verfahrensprüfer nicht.

### 27.6 Wo der Nullpunkt liegt

⭐ **Die Protokollkette beginnt nicht mit 21d, sondern mit der Tatsachennotiz
oben.** Fable, 21g Abschnitt 4: *„Der Sichtschutz regelt den Grund, nicht den
Zugriff — und ein Grund lässt sich nicht rückwirkend entkennen."* Die
Rückwirkung ist deshalb **Bestandsaufnahme, kein Pflichtenrückbau**: *„Was ich
beim Inkrafttreten wusste, wird festgehalten, nicht bewertet."*

**Für den Vorgängerchat des Verfahrensprüfers** gilt: seine Entscheidungen
(Abschnitte 23–26) sind registriert, und die Reihenfolge Regel → Messung ist im
Register selbst dokumentiert (24.3 vor 24.6). Was er sonst wusste, ist nicht
mehr feststellbar und muss es nicht sein — die Prüfung nach 27.4 ist auf seine
Begründungen genauso anwendbar, und sie liegen vollständig vor.

### 27.7 Ein Verstoss beim Melden des Verstosses — festgehalten, nicht geglättet

⚠️ Der steuernde Chat hat Fable am 21.09. den **Inhalt** des Sichtschutz-Treffers
zitiert (`BACKLOG.md` Z. 190 wörtlich) statt seiner Fundstelle. Fable hat es
selbst gemeldet und in die Tatsachennotiz eingetragen: *„Durch das Zitat kenne
ich die Zeile jetzt."*

⭐ **Daraus ist 27.5 entstanden.** Der Fehler steht hier, weil er die Regel
erzeugt hat und weil die Fehlerklasse benannt gehört: **wer prüft, fasst an** —
dieselbe Klasse, gegen die `A1` und `B1` gebaut sind.

### 27.8 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Register-KOPIE in die Projektablage legen** (mit Commit-Hash, Datum, Kennzeichnung KOPIE nach 27.3). Sie wird erst gezogen, **nachdem** alle Abschnitte dieser Aufgabe stehen — eine Kopie des Zwischenstands liefe sofort auseinander | steuernder Chat, nach TB-78 |
| ⛔ | **`BACKLOG.md` bereinigen oder verschieben.** 27.1 verlangt es nicht; die Regel liegt beim Leser, nicht bei der Datei | — |
| ⚠️ | **Die Prüfung nach 27.4** (Fables Begründungen gegen verbotene Grössen lesen) ist eine stehende Pflicht des steuernden Chats, kein Schritt dieser Aufgabe. Sie steht ab jetzt als Prüfprinzip `A8` (Schritt 4) | laufend |

> ⭐ **Messungen auf dem Selektionsraum nach dem Tag: siehe 45.6/45.7** (Fable
> 26a R6/R7, TB-114, 26.09.2026). Abschnitt 27 oben bleibt zeichengleich.

---

## 28. `asof` ist gesetzt — Berichtigung zu 26.3 und 26.6, und der Vorlauf-Satz gilt fort (TB-78, 21.09.2026)

⭐ **Drei Berichtigungen, Kategorie „Berichtigung" nach F17** (Registertext an
Registertext; die Quelle des Grundes ist eine Entscheidung des
Verfahrensprüfers, kein Ergebnis).

⚠️ **Abschnitt 26 bleibt zeichengleich stehen.** Was dort überholt ist, wird
hier benannt und trägt seine ERSETZT-Marke an dieser Stelle.

### 28.1 Warum es eine Berichtigung braucht — der Auftrag lief mit überholter Prämisse

**Gemessen 21.09.2026:** TB-77 hat durchgehend gegen die ursprüngliche
Auftragsfassung gearbeitet; der Nachtrag, der zwei Blocker aufhob, ist nie
angekommen (`grep` über Ergebnisdokument und `docs/belege/TB-77/` nach
*„Nachtrag zu TB-77"* und `FABLE_ANTWORT_2026-09-21b`: **0 Treffer**).

⭐ **Regel daraus, festgehalten, weil sie teuer war:** *Nach jeder Antwort des
Verfahrensprüfers werden die **laufenden** Aufträge gegen sie geprüft, nicht nur
die kommenden. Ein Nachtrag in eine laufende Sitzung ist billiger als eine
Berichtigung im Register.*

### 28.2 Registertext 5a, Ergänzung — woher `asof` kommt

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21b_asof_und_wache.md`,
Abschnitt (2), zeichengleich.

> **Registertext 5a, Ergänzung:** asof ist das UTC-Datum des Erstellungszeitpunkts des registrierten Snapshots. Es wird im `MANIFEST.json` als Feld `asof` geführt und im Register als Tatsachennotiz neben dem Snapshot-Hash eingetragen. Ein neuer Snapshot (5c) setzt ein neues asof.

**Fables Begründung, warum das Erstellungsdatum und nicht das Datenende** — im
Wortlaut, weil sie den Unterschied trägt:

> *„Das Datenende (grösstes `open_time` über alle Kursdateien) wäre eine zweite aus dem Inhalt abgeleitete Grösse — genau die Bauart, die ich bei `fensteranker` abgelehnt habe, weil sie mit den Daten wandert. […] Dieser Abstand ist eine Frische-Tatsache und gehört als eigenes Manifest-Feld (`datenende`) dorthin, nicht in asof. Das Erstellungsdatum ist bereits registriert, von niemandem anders berechenbar und unabhängig davon, welches Symbol zuletzt eine Kerze hatte."*

**Bekannte Wirkung auf die Zulässigkeit, aus derselben Quelle:** Der
Horizontbeginn verschiebt sich gegenüber dem Datenende um vier Tage (19.09.
statt 15.09.). Die erste Falte nach 4a beginnt am 1. Januar eines Jahres; eine
Verschiebung im September ändert das Jahr nicht. ⭐ *Das ist eine
Kalenderaussage, keine Ergebnisaussage.*

### 28.3 Tatsachennotiz — der Wert von `asof`

| | Wert | Fundstelle |
|---|---|---|
| **`asof`** | **`2026-09-19`** | Abschnitt 18, `zeitpunkt_utc` = `2026-09-19T06:49:32+00:00`, gelesen aus `snapshots/63e4b6c8…/MANIFEST.json` |
| Snapshot | `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` | Abschnitt 18, Commit `1075dec` |

⭐ **Der Wert ist keine neue Messung.** Er stand seit dem 19.09. als Tatsache im
Register; was fehlte, war die Zeile, die ihn `asof` nennt.

### 28.4 ⚠️ ERSETZT: die Platzhalter-Tabelle in 26.3

**Die vier Platzhalter-Zeilen in 26.3** — *„[PLATZHALTER — `asof` ist nicht
gesetzt; Datum folgt, sobald 5a einen Wert hat]"* — **gelten als ERSETZT.** Sie
bleiben dort zeichengleich stehen (append-only). Die gültige Fassung:

| Bot | Markt | `RECENT_YEARS_ONLY` | Horizontbeginn = `asof` − Konstante |
|---|---|---:|---|
| `elliott_wave` | krypto | keine | **kein Horizont** (26.2) |
| `t3_supertrend` | krypto | keine | **kein Horizont** |
| `rsi2_crypto` | krypto | keine | **kein Horizont** |
| `turtle_soup_crypto` | krypto | keine | **kein Horizont** |
| `volatility_breakout_crypto` | krypto | keine | **kein Horizont** |
| `elliott_wave_stocks` | aktien | 10 Jahre | **2016-09-19** |
| `rsi2_mean_reversion` | aktien | 10 Jahre | **2016-09-19** |
| `turtle_soup_stocks` | aktien | 10 Jahre | **2016-09-19** |
| `volatility_breakout` | aktien | 10 Jahre | **2016-09-19** |

⚠️ **Die Konstante ist aus dem Code gelesen** (Fundstellen 26.1), nicht
registriert. Ob sie als registrierte Grösse nach `registerdaten.py` gehört,
bleibt offen — siehe 28.7.

⚠️ **Abgegrenzt, damit es niemand verwechselt:** 15.6 Punkt 3 nennt
*„gemessen vom letzten Kurstag (2026-09-01) zurück auf 2016-09-01"*. Das ist die
**Datenuhr**, genau der Bezug, den 26.2 ablöst — **kein `asof`**. Die
Ähnlichkeit der beiden Daten (2016-09-01 gegen 2016-09-19) ist Zufall des
Kalenders und kein Hinweis darauf, dass es dasselbe wäre.

### 28.5 ⚠️ ERSETZT: die zwei Zeilen in 26.6, die `asof` als offen führen

**Zeile 1 von 26.6** — *„`asof` setzen. Wann und wodurch, ist Fables Frage (1)
im neuen Chat; die Lesart ‚mit Snapshot und Tag zugleich' ist nicht entschieden.
Bis dahin bleibt 26.3 ein Platzhalter"* — **ist ERSETZT.** Entschieden seit
21b: **durch den Snapshot, nicht durch den Tag.** Fable, wörtlich: *„Nicht mit
dem signierten Tag — der Tag friert ein, was das Register sagt; er erzeugt keine
Zahl."*

**Zeile 2 von 26.6** — *„Tatsachennotiz 4d füllen: vier Daten in 26.3"* — **ist
mit 28.4 erledigt.**

**Zeile 4 von 26.6** (die Wache in `auswertung.py`) — **ist ERSETZT.** Fable hat
seinen eigenen Vorschlag am 21.09. zurückgezogen: *„Mein Vorschlag ‚in den
Auswerter' war falsch adressiert."* Die Wache geht in die vier
`multi_symbol_optimise.py` (TB-30b). ⚠️ **Und sie prüft nicht gegen den
Horizontbeginn, sondern gegen den Beginn der ersten Selektionsfalte** —
siehe Abschnitt 29.

**Zeile 5 von 26.6** (`FABLE_ANTWORT_2026-09-21a` liegt in keinem Träger) — **ist
mit Schritt 0 dieser Aufgabe erledigt**; die Datei liegt unter
`docs/projektfuehrung/`.

⭐ **Unverändert offen bleiben:** Zeile 3 (die vier Optimierer, TB-30b), Zeile 6
(`RECENT_YEARS_ONLY` als registrierte Grösse, Entscheidungsvorlage) und Zeile 7
(nicht gemessen, wie viele Einstiege vor einem Horizontbeginn liegen).

### 28.6 Registertext 4a, Präzisierung, Ergänzung — der Vorlauf-Satz gilt fort

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21c_uebergabe_und_vorlauf.md`,
Abschnitt 3.1, zeichengleich.

> **4a, Präzisierung, Ergänzung:** Der Indikator-Vorlauf nach (i) wird gegen den Horizontbeginn des Bots gerechnet, nicht gegen den ersten Kurs im Bestand. Der Satz aus der Fassung vom 20.09. gilt fort; die Fassung vom 21.09. hat ihn nicht ersetzt, sondern ausgelassen.

**Quelle des Grundes,** Fable wörtlich: *„Ein Vorlauf, der auf Kursen vor dem
Horizontbeginn rechnet, ist derselbe Zugriff"*, den Abschnitt 26 verbietet.
Kategorie: **Berichtigung** (Registertext an Registertext). Kein Ergebnis.

**Die Messung dazu, 21.09.2026, 17:48 durch den steuernden Chat:** Der Satz
*„Der Vorlauf wird gegen dieses Datum gerechnet, nicht gegen den ersten Kurs im
Bestand"* steht im Register **genau einmal**, in **Z. 4307** — und zwar
**innerhalb des Zitats der als ersetzt markierten Fassung** in 26.2. Er steht
also im Register ausschliesslich als Teil dessen, was ausser Kraft ist.

⭐ **Und die Tatsache, die Fables Unsicherheit auflöst** (*„ob ich den Satz
absichtlich gestrichen habe"*): Die Fassung vom 20.09. ist **nie** in einen
Registertext übernommen worden — gemessen, `grep` im Register: *„Horizontbeginn"*
**0 Treffer**, *„4a, Präzisierung"* **0 Treffer**. Es gab nichts zu streichen;
der Satz ist zwischen zwei Antworten verlorengegangen, nicht im Register.

### 28.7 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Das Feld `asof` ins `MANIFEST.json` schreiben.** 28.2 verlangt es, aber der Snapshot ist nach 17.1 *„nach seiner Erzeugung nicht mehr geschrieben"*. Ob das Manifest Teil dieses Schreibverbots ist, sagt kein Registertext. ⭐ *Fable hält in 21b fest, dass der Snapshot-Hash über den Dateien liegt und nicht über dem Manifest — eine Ergänzung änderte den Hash also nicht.* **Das ist eine Verfahrensfrage vor dem Tag und wird nicht nebenbei entschieden** | Verfahrensprüfer / Betreiber |
| ⛔ | **Das Feld `datenende` ins `MANIFEST.json`** — derselbe Grund | dito |
| ⛔ | **`registerdaten.py` anfassen** | — |
| ⛔ | **Den Faltenplan nach 4a ableiten.** Er hängt an einer offenen Frage an den Verfahrensprüfer (Status des gesperrten `faltenplan.json`, `FABLE_ANFRAGE_2026-09-21b`, Abschnitt C) | eigene Aufgabe, nach seiner Antwort |

---

## 29. Der Kapitalpfad beginnt am 1. Januar der ersten Selektionsfalte (TB-78, 21.09.2026)

⭐ **Neuer Registertext, keine Berichtigung** — gemessen: das Register regelt
den Beginn des Kapitalpfads bisher nicht (siehe 29.2).
⭐ **Bauart 24.3: die Regel steht vor der Messung.**

### 29.1 Der Befund — eine Lücke zwischen Horizontbeginn und erster Falte

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21c_uebergabe_und_vorlauf.md`,
Abschnitt 3.2.

Abschnitt 26 verbietet Einstiege **vor dem Horizontbeginn** (28.4: `2016-09-19`
für die vier Aktien-Bots). Die erste Selektionsfalte beginnt nach 4a am
**1. Januar**. Dazwischen liegen dreieinhalb bis fünfzehn Monate, in denen ein
Einstieg nach 26 **zulässig** ist, in **keiner Falte** auftaucht — und durch den
Kapitalpfad läuft.

⭐ **Fable, wörtlich:** *„Das ist genau der Schaden, mit dem (d) begründet wurde
(‚verändern das Kapital, mit dem die erste Falte beginnt'), nur kürzer."*

⚠️ **Dasselbe kann bei Krypto auftreten**, wo Bedingung (i) wegen des Vorlaufs
später liegt als der erste handelbare Tag — `rsi2_crypto`: 2018 handelbar, erste
Falte 2019.

⚠️⚠️ **Und die Wache aus 21b sieht es nicht**, weil sie gegen den Horizontbeginn
prüft. Deshalb ändert sich mit diesem Abschnitt auch die Wache (29.4).

### 29.2 Die Messung — das Register regelt es nicht

| gesucht | Treffer | was der Treffer sagt |
|---|---:|---|
| `Kapitalpfad` + Beginn/Start/1. Januar/erste Falte | **1** (Z. 4296) | beschreibt den **Schaden**: *„der Kapitalpfad (Registertext 1a) beginnt die erste Falte mit einem Kapitalstand, der aus nicht registrierten Jahren stammt"* |
| `Startkapital` | **0** | — |

⇒ **Der Text unten ist eine Neuaufnahme.** *Fable hatte das in 21c ausdrücklich
offengelassen: „Steht im Register bereits ein Satz, der den Beginn des
Kapitalpfads festlegt, legt ihn mir im Wortlaut vor — dann ist mein Vorschlag
gegenstandslos oder eine Berichtigung dazu, und das kann ich von hier nicht
sehen."*

### 29.3 Der Registertext, zeichengleich

> **Zu 4a / 26:** Der Kapitalpfad eines Bots beginnt am 1. Januar seiner ersten Selektionsfalte mit dem registrierten Startkapital und ohne offene Position. Kein Einstieg liegt vor diesem Datum. Die Grösse der Wirkung ist für diese Regel ohne Belang.

**Quelle des Grundes:** 4a (Falten sind ganze Kalenderjahre) und der Grund von
26 (kein Trade ausserhalb aller Falten im Kapitalpfad). Kein Ergebnis.

⭐ **Der letzte Satz ist Absicht.** Er schliesst aus, dass die Regel später mit
dem Hinweis *„die Wirkung ist ja klein"* aufgeweicht wird — dieselbe Bauart wie
24.3.

### 29.4 Die Wache in TB-30b — geändert gegenüber 21b

⚠️ **Die Fassung aus 21b (Prüfung gegen den Horizontbeginn) ist ERSETZT.** Es
gilt:

> **Wache (TB-30b), angepasst:** frühester Einstieg ≥ **Beginn der ersten Selektionsfalte** (nicht nur ≥ Horizontbeginn). Der Bericht führt je Bot drei Daten nebeneinander: Horizontbeginn, Beginn der ersten Falte, frühester Einstieg.

⚠️ **Ort der Wache unverändert:** in den vier `multi_symbol_optimise.py`, **nicht**
in `auswertung.py` (eingefroren, Abschnitt 0 Z. 31; Fables Rücknahme in 21b).

> ⚠️ **Berichtigt (34.5, TB-82, 22.09.2026):** „in den vier `multi_symbol_optimise.py`"
> lies **„in allen neun"** — Fable 21l, Punkt 4 (b), zeichengleich: *„Die Wache
> „frühester Einstieg ≥ Beginn der ersten Selektionsfalte" wird in **allen neun**
> `multi_symbol_optimise.py` eingebaut, nicht nur in den vier Aktien-Optimierern."*
> Der Absatz oben bleibt zeichengleich; unverändert gilt: **nicht** in `auswertung.py`.
> Gemessen (TB-82, Beleg M4): heute in keinem der neun eine Wache — Ersteinbau, TB-30b.

### 29.5 Was noch zu messen ist — nur das Ob, nicht die Wirkung

| | zu messen | ⚠️ |
|---|---|---|
| 1 | Wo der Kapitalpfad der neun Optimierer **heute** beginnt | — |
| 2 | Ob es in den vorhandenen Trade-Listen Einstiege zwischen Horizontbeginn (bzw. erstem handelbarem Tag) und dem 1. Januar der ersten Falte **gibt** | ⛔ **Nur das Ob, nicht die Wirkung auf Kennzahlen** — eine Zahl über Kennzahlen fiele unter 27.1 |
| | | ⚠️ **Und jede Messung an den neun `paper_trading_*.db` läuft auf einer KOPIE** |

⛔ **Nicht Gegenstand dieser Aufgabe.** Eigene Aufgabe, nach TB-78.

---

## 30. Was der gesperrte Faltenplan ist — und was der Plan nach 4a ist (Fable 21i, 21.09.2026)

⭐ **Neuer Registertext.** Er trennt zwei Dinge, die bis heute denselben Namen
trugen: die **gesperrte Datei** `ergebnisse/faltenplan.json` und den
**Faltenplan nach 4a**. Dazu zwei Präzisierungen zu den Abschnitten 28 und 29,
die aus derselben Antwort stammen (30.6, 30.7).

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21i_gesperrter_faltenplan.md`,
zeichengleich. Anlass: die Messmeldung
`FABLE_ANFRAGE_2026-09-21b_messmeldung_vorlauf_und_kapitalpfad.md`, Abschnitt (C).

### 30.1 Der Befund — die gesperrte Datei stammt aus einem anderen Verfahrensstand

**Gemessen 21.09.2026 an
`research/vorregistrierung/ergebnisse/faltenplan.json` (`0e54ac5c…`):**

| | |
|---|---|
| ⚠️ | Die Datei führt je Falte ein Feld **`training_bis_ausschliesslich`** (Beispiel `2018-12-14`) und ein Feld **`embargo_tage: 18`**. ⭐⭐ **Verfahren B hat ausdrücklich KEIN Trainingsfenster** (V5c, Fable 15.09.2026) |
| ⚠️ | Erste Selektionsfalte `turtle_soup_stocks` im gesperrten Plan: **2019** — nicht 2017 oder 2018 |
| ⚠️ | TB-72 hat einen neuen Plan **daneben** gelegt (`ergebnisse/faltenplan_tb72.json`); der gesperrte ist unberührt, aber er ist **nicht** der Plan nach 4a |

⇒ **Die Frage, die Fable stellte, war an dieser Datei nicht beantwortbar.** Nach
`A2` ist *„konnte nicht messen"* ein eigenes Ergebnis, nicht grün und nicht rot.

### 30.2 Der Registertext, zeichengleich

> **Registertext (zu 26 / Sperrliste):**
> **(1)** `faltenplan.json` (0e54ac5c…) bleibt gesperrt und unverändert. Er ist der **registrierte historische Stand** eines früheren Verfahrensstands (Trainingsfenster, Embargo); er ist **nicht** der Faltenplan nach 4a und wird vom Lauf nicht gelesen. Sperrlistenpunkt 2 erhält eine Tatsachennotiz mit diesem Satz — kein Ersatz, keine Streichung.
> **(2)** Der Faltenplan nach 4a ist **Registertext**: je Bot die Liste der Selektionsfalten (Kalenderjahre), abgeleitet aus asof, `RECENT_YEARS_ONLY`, dem Indikator-Vorlauf gegen den Horizontbeginn und dem Trockenlauf nach 3b (b). Der Registertext ist die Quelle; jede Datei, die ihn maschinenlesbar wiedergibt, ist Abbild.
> > ⚠️ **Berichtigt (34.3, TB-82, 22.09.2026):** „Trockenlauf nach 3b (b)" lies **„3b (a)"** — Fable 21m, Frage 3, zeichengleich: *„Gemeint ist der Trockenlauf aus 3b (a), der die `MIN_HISTORY_*`-Tabelle aus 3b (b) anwendet; ein zweiter Trockenlauf existiert nicht."* Der Satz oben bleibt zeichengleich stehen; 16.7: 3b (a) ist der Trockenlauf-Satz, 3b (b) die `MIN_HISTORY_*`-Tabelle.
> **(3)** Genau **eine** solche Datei wird vor dem Tag mit Hash in die Sperrliste aufgenommen (neuer Punkt), und der Lauf liest genau diese. Ihr Inhalt muss dem Registertext aus (2) entsprechen; der Abgleich (Datei gegen Registertext, je Bot, je Jahr) ist eine Prüfung vor dem Tag und wird als Tatsachennotiz mit Ergebnis eingetragen. Trägt eine Datei Felder, die 4a nicht kennt (Trainingsgrenzen, Embargo), ist sie nicht dieses Abbild.
> > ⭐ **Präzisiert (35.4, TB-83, 22.09.2026):** „und der Lauf liest genau diese" — Fable 22a, zeichengleich: *„Der Lauf verwendet den Plan, den `faltenplan.py` zur Laufzeit bildet. Die Sonde vergleicht diesen Plan **vor dem Start des Laufs** mit dem Abbild (Feldmenge und Werte); bei Abweichung bricht der Laufwrapper ab, bevor `auswertung.py` aufgerufen wird. Das Abbild ist damit der registrierte Sollzustand, gegen den der gerechnete Plan geprüft wird — nicht die Datei, die `auswertung.py` öffnet."* Gemessen (Beleg M3): `auswertung.py` rechnet den Plan über genau einen Aufruf, `fp.faltenplan(mess)`, Z. 589. Der Satz oben bleibt zeichengleich; Sonde und Wrapper sind nicht geschrieben.
> **(4)** Ob `faltenplan_tb72.json` diese Datei ist, entscheidet allein der Abgleich nach (3) — nicht ihre Herkunft.

> ⭐ **Eingaben in der Gruppe `eingefroren`: siehe 45.3, vollzogen in 45.11**
> (Fable 26a R3, TB-114, 26.09.2026). Der Registertext oben bleibt
> zeichengleich.

**Quelle des Grundes,** Fable wörtlich: *„Das Register ist append-only …
Ersetztes bleibt mit Marke stehen — das gilt für Dateien in der Sperrliste
genauso wie für Sätze. Und 4a definiert die Falten als Funktion registrierter
Konstanten plus Trockenlauf … ein Plan, der ein Trainingsfenster kennt, kann
diese Funktion nicht sein."* Kein Ergebnis; **welche Jahre herauskommen, spielt
für die Regel keine Rolle.**

⭐⭐ **Warum nicht „ersetzen und den alten von der Sperrliste nehmen",** wörtlich:

> *„Die Sperrliste beweist, dass nichts bewegt wurde. Einen Punkt zu entfernen, weil er obsolet ist, öffnet die Frage, wer ‚obsolet' entscheidet — und das ist genau die Stelle, an der später jemand einen unbequemen Punkt für obsolet erklären könnte. Ergänzen, markieren, stehen lassen."*

### 30.3 Die Tatsachennotiz zu Sperrlistenpunkt 2 — und warum sie dort steht

⭐ **Handwerksentscheidung, gemessen:** Die Sperrliste kennt die Form bereits.
**Punkt 8** trägt seit Abschnitt 15 eine eingerückte Notiz unter dem Punkt
(*„⚠️ Der Halbsatz ‚vier Jahre Vorlauf je Symbol' ist ersetzt (Abschnitt 15,
Registertext 3) …"*). **Kein neues Element** — Punkt 2 bekommt dieselbe Form.
*Fable hatte das offengelassen: „ob die Sperrliste heute schon eine Form für
‚Tatsachennotiz zu einem Punkt' kennt … Handwerk, eure Wahl."*

⚠️ **Es ist ein reiner Zusatz** — Abschnitt 10 verliert keine Zeile.

⚠️ **Folge der Einfügung, gemessen beim Eintragen (TB-78):** Die sieben
Notizzeilen unter Punkt 2 verschieben jede Zeilennummer unterhalb von Z. 818
um **+7**. Alle Zeilenangaben in den Abschnitten 26 bis 29 (etwa Z. 4296,
Z. 4307, Z. 3897) gelten für den Stand `83e3a85`; im aktuellen Stand liegen
sie sieben Zeilen tiefer. *Eine Zeilenangabe im Register trägt ab hier ihren
Commit-Stand mit.*

### 30.4 Fables Rückfrage nach der Herkunft der Faltenmenge — beantwortet: steht

Er fragt, **nur das Ob**, gegen welchen Plan die 64 Falten aus 24.6 und die
„sieben statt acht" für `t3_supertrend` aus 25 gezählt wurden — *„damit die
Zahlen dort nicht mit dem Plan nach 4a verwechselt werden"*.

| | steht dort schon? | Fundstelle |
|---|---|---|
| **24.6** | ✅ **ja, wörtlich** | Z. 3897 (Stand `83e3a85`): *„Falten aus `research/vorregistrierung/ergebnisse/faltenplan_tb72.json` (TB-72)"* |
| **25** | ✅ **ja, und stärker** | Abschnitt 25 ist der Abschnitt, der `faltenplan_tb72.json` **erzeugt** hat (25.4; *„der neue Plan, daneben; `faltenplan.json` (`0e54ac5c…`) unberührt"*) |

⇒ ⭐ **Seine Bedingung ist erfüllt** (*„Wenn sie schon dort steht, genügt
‚steht'"*). **Keine Nachtragszeile an 24.6 oder 25** — beide sind append-only
abgeschlossen.

⚠️ **Festgehalten, weil es die Verwechslung benennt:** Weder 24.6 noch 25 zählt
gegen den **gesperrten** Plan (`0e54ac5c…`); beide zählen gegen
`faltenplan_tb72.json`. ⛔ **Und keiner von beiden ist der Plan nach 4a** — der
existiert noch nicht.

### 30.5 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Den Faltenplan nach 4a ableiten und als Registertext eintragen** (30.2 (2)) | eigene Aufgabe, nächster Schritt vor dem Tag |
| ⛔ | **Eine Abbild-Datei auf die Sperrliste nehmen** (30.2 (3)) — setzt (2) voraus | dieselbe Aufgabe |
| ⛔ | **Den Abgleich `faltenplan_tb72.json` gegen den Registertext** — es gibt noch keinen Registertext, gegen den abzugleichen wäre. ⚠️ **Gemessen 21.09.2026 (TB-78, beim Eintragen):** die Datei trägt `training_bis_ausschliesslich` (77 Vorkommen) und `embargo_tage` (9 Vorkommen) — dieselben Felder wie der gesperrte Plan. *Der Nachtrag v2 hatte „trägt keine Trainingsfelder" angenommen; das ist an der Datei widerlegt und nicht übernommen.* Ob sie das Abbild ist, entscheidet nach 30.2 (4) allein der Abgleich; 30.2 (3) spricht in ihrer heutigen Form dagegen | dieselbe Aufgabe |
| ⛔ | **`faltenplan.json` anfassen** — byteweise `0e54ac5c…` | nie |

### 30.6 Präzisierung zu 28.6 — der Vorlauf-Satz ist ein Ersteintrag

⚠️ **28.6 trägt die Kategorie „Berichtigung (Registertext an Registertext)".
Sie ist präzisiert, und 28.6 bleibt zeichengleich stehen.**

**Fable, 21i Abschnitt 1 (A), wörtlich:**

> *„Eure Tatsache aus 26.2 löst meine Unsicherheit: Es gab im Register nichts zu streichen, der Satz ist zwischen zwei meiner Antworten verlorengegangen. Damit ist auch die Kategorie präziser als in 21c: kein Berichtigung *eines Registersatzes*, sondern **Ersteintrag** — der Satz kommt mit der 4a-Präzisierung erstmals in Registertext (26). Quelle des Grundes unverändert 4a/26; F17 ist erfüllt, die Kategorie ist Handwerk."*

⇒ **Gültig ist: Ersteintrag.** ⭐ **Die Einordnung folgt damit der Messung des
steuernden Chats** (*„Horizontbeginn" 0 Treffer, „4a, Präzisierung" 0 Treffer im
Register*) **und nicht der ersten Vermutung — auch nicht Fables eigener.**

⚠️ **Warum das mehr ist als ein Etikett:** Eine Berichtigung setzt einen Satz
voraus, der berichtigt wird. Gäbe es ihn, wäre er irgendwo in Kraft gewesen —
und dann müsste geprüft werden, was auf ihm ruht. **Es gab ihn nie.** *Die
Kategorie ist die Frage, ob etwas ersetzt wurde oder zum ersten Mal gilt.*

### 30.7 Ergänzung zu 29.2 — die Reihenfolge ist der Beleg, nicht die Zahl

**Fable, 21i Abschnitt 1 (B), wörtlich:**

> *„Die Zeile 4296 ist der Beleg, dass der Schaden im Register benannt war, bevor die Regel dagegen stand — das ist die richtige Reihenfolge, und sie soll so in der Tatsachennotiz zu 26 stehen."*

⭐⭐ **Damit ist Z. 4296 nicht bloss der einzige Treffer einer Suche, sondern
der Nachweis der Bauart 24.3:** *eine Regel, die vor der Messung steht, kann
durch die Messung nicht gewählt worden sein.* ⚠️ **Wäre es umgekehrt** — erst
die Wirkung gemessen, dann die Regel geschrieben —, **wäre 29.3 eine
nachträgliche Wahl**, gleich wie gut sie begründet wäre.

⚠️ **Und die Grenze, damit der Beleg nicht überdehnt wird:** Z. 4296 belegt,
dass der **Schaden** benannt war. Sie belegt **nicht**, dass jemand seine Grösse
kannte — die ist bis heute nicht gemessen (29.5) und soll es nach 27.1 vor dem
Tag auch nicht werden.

---

## 31. Berichtigung zu 28.2 — das Manifest bekommt kein Feld `asof` (Fable 21j, 21.09.2026)

⭐ **Berichtigung eines Registersatzes, der am selben Tag eingetragen wurde**,
plus eine Präzisierung zu 5a / 17.1 (Ersteintrag) und zwei Tatsachennotizen.

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21j_manifest_asof.md`,
Abschnitt 2, zeichengleich. Anlass:
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-21c_einarbeitung_21i_und_manifest.md`,
Punkt 5.

⚠️ **28.2 bleibt zeichengleich stehen.** Der Halbsatz, der ersetzt wird, ist
hier benannt.

### 31.1 Der Befund — der Wert steht im Manifest, unter einem anderen Namen

**Gemessen am `MANIFEST.json` des registrierten Snapshots
(`snapshots/63e4b6c8…/MANIFEST.json`):**

| | |
|---|---|
| Das Feld, das `asof` tragen sollte | existiert bereits als **`zeitpunkt_utc`** = `2026-09-19T06:49:32+00:00` |
| Ein Feld `asof` | **gibt es nicht** |

⇒ **Es fehlte kein Wert, nur ein zweiter Feldname für denselben Wert.**

### 31.2 Der Ersatztext zu 28.2, zeichengleich

> **Berichtigung zu 28.2 (Registertext 5a, Ergänzung), Ersatztext:**
> asof ist das UTC-Datum des Felds `zeitpunkt_utc` im `MANIFEST.json` des registrierten Snapshots. Es wird im Register als Tatsachennotiz neben dem Snapshot-Hash eingetragen. Ein neuer Snapshot (5c) setzt ein neues asof. **Das Manifest erhält kein Feld `asof`**; der Halbsatz „Es wird im `MANIFEST.json` als Feld `asof` geführt" ist ersetzt.

⚠️ **Der ersetzte Halbsatz steht in 28.2 und bleibt dort stehen**, mit dieser
Marke. **Der Wert von `asof` ändert sich nicht:** weiterhin **2026-09-19**.

### 31.3 Präzisierung zu 5a / 17.1 — Ersteintrag, zeichengleich

> **Präzisierung zu 5a / 17.1 (Ersteintrag):** „Wird nach seiner Erzeugung nicht mehr geschrieben" gilt für den Snapshot **einschliesslich seines Manifests**. Tatsachen über einen Snapshot, die nach seiner Erzeugung festgestellt werden — darunter `datenende` (grösstes `open_time` über alle Kursdateien des Snapshots) — stehen als Tatsachennotiz im Register, nicht im Snapshot. Ein Manifest darf `datenende` nur tragen, wenn es **bei der Erzeugung** geschrieben wird (5c, künftige Snapshots).

**Quelle des Grundes,** Fable wörtlich: *„17.1 im Wortlaut … und die Rolle des
Manifests als Träger, aus dem Abschnitt 18 seine Zahlen liest — ein Träger, der
nach der Registrierung noch beschrieben wird, kann nicht mehr bezeugen, was bei
der Registrierung galt, auch wenn der Hash ihn nicht deckt. Und der Grundsatz
ein Wert, ein Ort."* Kein Ergebnis.

**Seine Begründung gegen die drei vorgelegten Wege, wörtlich:**

> *„Warum nicht a: a lässt 28.2 stehen und liest es ‚für den nächsten Snapshot' — ein Registertext, der den Bestand nicht beschreibt, mit einer Lesart daneben. Das ist derselbe Zustand wie beim Vorlauf-Satz heute Vormittag, nur absichtlich. Warum nicht b: Der Preis ist genau der, den ihr nennt: ‚unverändert seit Erzeugung' gilt danach nicht mehr wörtlich, und ein Register, das wörtlich gelesen wird, verträgt keine folgenlosen Ausnahmen. Warum nicht c: zweiter Träger."*

### 31.4 Tatsachennotiz — seine Unsicherheit, gemessen

Fable markiert in 21j als unsicher, *„ob 17.1 den Begriff ‚Snapshot' an anderer
Stelle so verwendet, dass das Manifest ausdrücklich ausgenommen ist — dann wäre
meine Präzisierung eine Berichtigung dazu, und ihr seht das im Register, ich
nicht."*

**Gemessen 21.09.2026 im Register und am Dateisystem:**

| | Befund |
|---|---|
| 17.1 definiert den Snapshot als | **Ordner**: *„je Lauf einen eingefrorenen Snapshot (Tatsachennotiz: `snapshots/<hash>/`), der neben dem Bestand liegt und nach seiner Erzeugung nicht mehr geschrieben wird"* |
| Ort des Manifests | `snapshots/63e4b6c8…/MANIFEST.json` — **im Ordner** |
| Stelle, die es ausnimmt | **keine.** Alle Manifest-Erwähnungen im Register betreffen seine *Rolle* (führt Dateien mit Inhalts-Hash, trägt `datenstand_hash`, `teilkerzen`, zugelassene Befunde), nicht seine Unantastbarkeit |
| ⭐ **Die einzige Ausnahme, und sie ist eine andere Frage** | Der **Snapshot-Hash** deckt das Manifest nicht (17.1: *„der Hash der … (Pfad, Inhalts-Hash)-Paare **der Dateien** — nicht des Manifests"*) |

⇒ ⭐⭐ **Seine Präzisierung ist ein Ersteintrag, keine Berichtigung — und der
Wortlaut von 17.1 stützt sie.** ⚠️ *„Gehört zum Snapshot-Ordner" und „wird vom
Snapshot-Hash gedeckt" sind **zwei Fragen**, nicht eine (`C7`). Das Manifest
gehört dazu und wird nicht gedeckt; genau deshalb wäre eine Ergänzung folgenlos
für den Hash — und genau deshalb ist sie trotzdem ausgeschlossen.*

### 31.5 Tatsachennotiz — `datenende` des registrierten Snapshots

| | Wert | Herkunft |
|---|---|---|
| **`datenende`** | **2026-09-15** — grösstes `open_time` über alle **223** Kursdateien in `snapshots/63e4b6c8…/` (letzte Kerze `2026-09-15 08:00:00`, in 24 Krypto-1h-Dateien) | Mac-Lauf, `trading-env/bin/python3` (Python 3.9.6, macOS 15.7.9), Mac-Sitzung TB-79, 21.09.2026; zwei Zählungen (`csv`-Modul und pandas 2.3.3) gleich — `docs/belege/TB-78/schritt3c_messung_31_5_31_6.txt` |
| **`asof`** | **2026-09-19** | `zeitpunkt_utc` im Manifest, Abschnitt 18 |
| Abstand | **4 Tage** (2026-09-19 − 2026-09-15) | — |

⭐ **Messnotiz der Mac-Sitzung (TB-79), nicht Teil des Nachtrags:** Die 223
Kursdateien enden nicht am selben Tag — die **150 Aktien-Tagesdateien** enden
am **2026-09-01**, die 24 Krypto-Tagesdateien am 2026-09-14, die 48
Krypto-4h- und -1h-Dateien am 2026-09-15 (Ausnahme `XAUTUSDT_1h.csv`:
2026-08-30). `datenende` ist das Maximum über alle Dateien; das Datenende der
vier Aktien-Bots liegt **18 Tage** vor `asof`. Eine Kalenderaussage, keine
Ergebnisaussage.

### 31.6 ⚠️ Berichtigung einer Zahl aus Abschnitt 26 — 15 Schlüssel sind 16

**Abschnitt 26 (TB-77) sagt:** *„es steht nirgends als Wert — gemessen
21.09.2026 in allen `.py` …, im **Snapshot-Manifest (15 Schlüssel, keiner
`asof`)**, in `registerdaten.py` und in `docs/`"*.

**Nachgemessen 21.09.2026 am selben Manifest:** **16 Schlüssel.**

```
bytes_gesamt · dateien · dateien_gesamt · datenstand_hash · eingabeliste ·
kursdateien · quelle · snapshot_hash · teilkerzen · verfahren · werkzeug ·
wurzel · zeitpunkt_utc · zugelassene_befunde · zugelassene_befunde_anzahl ·
zugelassene_befunde_herkunft
```

⭐ **Eigene Nachmessung der Mac-Sitzung (TB-79), Zählweise genannt:** gezählt
sind die Schlüssel der **obersten Ebene** des JSON-Objekts, `dateien` (die
Dateiliste mit 225 Einträgen) **mitgezählt** — **16**; ohne `dateien` **15**.
Zwei Zählungen (`json.load`, Textmuster auf Einrückung 2) gleich; `asof` kommt
weder als Schlüssel noch sonst im Text vor. `trading-env/bin/python3`
(Python 3.9.6), 21.09.2026.

| | |
|---|---|
| ✅ **Die Aussage trifft** | **keiner** der Schlüssel heisst `asof` — der Befund von TB-77 steht |
| ⚠️ **Die Zahl trifft nicht** | 16, nicht 15 |
| ⭐ **Mutmassliche Ursache, nicht gemessen** | `dateien` ist die Dateiliste, die übrigen 15 sind Metadaten. Wer die Liste nicht mitzählt, kommt auf 15 — **aber die Zählweise steht nicht dabei** |

⭐⭐ **Fehlerklasse `K4d`: eine Kennzahl, die ihre Bezugsmenge nicht nennt.**
*Die Zahl war womöglich richtig gerechnet — über eine Menge, die niemand
benennt. Eine Kennzahl nennt die Menge, über die sie läuft.*

⚠️ **Abschnitt 26 bleibt zeichengleich stehen**; die Zahl gilt als berichtigt
durch diesen Unterabschnitt.

### 31.7 Was hier ausdrücklich NICHT getan wird

| | | |
|---|---|---|
| ⛔ | **Das Manifest anfassen** — weder `asof` noch `datenende` | 31.2, 31.3 |
| ⛔ | **Ein Beiblatt neben dem Manifest anlegen** (Weg c der Vorlage) — zweiter Träger | Fable 21j |
| ⛔ | **28.2 oder Abschnitt 26 umschreiben** — append-only | — |
| ⛔ | **Den Snapshot neu ziehen** | — |
| ⭐ | **Was entfällt:** die Manifest-Ergänzung, die in 28.7 als *„nicht getan"* geführt war, ist jetzt *„nicht zu tun"* | Fable 21j |

---

## 32. Bedingung (i) rechnet gegen den Horizontbeginn aus 28.4 — Umstellung des Faltenplans von der Datenuhr auf das absolute Datum (TB-80, 21.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Satz wird umgeschrieben.**
Kein neuer Registertext: 25.3 (Konjunktion), 26.2 (Horizont als absolutes
Datum je Bot) und 28.4 (die vier Daten) bleiben zeichengleich stehen und
werden hier **umgesetzt**, nicht geändert. Was dieser Abschnitt trägt, sind
ein Befund, drei Tatsachennotizen und eine Entscheidungsvorlage.

**Anlass:** `docs/auftraege/MAC_TB-80_bedingung_i_auf_asof.md`. Betreiberfreigabe
vom 21.09.2026, 21:47 Ortszeit, für **genau eine** Datei:
`research/vorregistrierung/faltenplan.py`. Ergebnis
`docs/ERGEBNIS_TB-80_bedingung_i_auf_asof.md`, Belege `docs/belege/TB-80/`.

⭐⭐ **Die Regel stand vor der Messung.** Gemessen an der Git-Historie:
Abschnitt 26.2 ist mit Commit `729443c` am 21.09.2026, **17:13** Ortszeit
eingetragen worden (der Auftrag nennt 19:19; der Commit liegt früher), 28.4
mit Commit `003f894` um **19:20** Ortszeit; die Messung in 32.2 lief am
21.09.2026 ab 20:17 UTC (**22:17** Ortszeit). **Was herauskommt, ist keine
Wahl** — Bauart 24.3.

---

### 32.1 Der Befund — Bedingung (i) rechnete gegen die Datenuhr, 26.2 verlangt das absolute Datum

**Gemessen 21.09.2026 am Stand `41db199` (vor Schritt 1), Fundstellen:**

| | Fundstelle | Wortlaut / Wert |
|---|---|---|
| Was das Register verlangt | **26.2**, Z. 4323–4329 (Registertext 4a, Präzisierung) | *„Der Datenhorizont eines Bots ist ein absolutes Datum je Bot: Horizontbeginn = `asof` (5a) minus `RECENT_YEARS_ONLY` des Bots; Bots ohne diese Konstante haben keinen Horizont (Krypto). […] Es gilt für alle Symbole des Bots gleich"* |
| Der Wert | **28.4**, Z. 4684–4687 (gültige Fassung der Tatsachennotiz zu 4d) | `elliott_wave_stocks`, `rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout`: **2016-09-19**; die fünf Krypto-Bots: **kein Horizont** (Z. 4679–4683) |
| Woher der Wert kommt | **28.3** | `asof` = **2026-09-19** (`zeitpunkt_utc` des Snapshots `63e4b6c8…`, Abschnitt 18) |
| Was der Code tat | `research/vorregistrierung/faltenplan.py::erste_falte_4a`, Z. 175 (Stand `41db199`) | `beginn = fn.symbolbeginn(bot, fn.fensteranker(eig["markt"]))` |
| Was `fensteranker` ist | `research/faltenplan_neun/faltenplan_neun.py:271–295` | zehn Jahre vor dem **spätesten letzten Kurstag des Marktes** — die **Datenuhr**; gemessen am 21.09.2026: `aktien` **2016-09-01**, `krypto` `None` (`docs/belege/TB-80/schritt0_ausgangsstand.txt`) |
| Der Abstand | — | **18 Tage** (2016-09-01 → 2016-09-19). 28.4, „Abgegrenzt": *„Die Ähnlichkeit der beiden Daten (2016-09-01 gegen 2016-09-19) ist Zufall des Kalenders"* |

**Was geändert wurde (Commit `76c20ec`, Diff vollständig im Ergebnisdokument):**
`erste_falte_4a()` nimmt den Anker aus `HORIZONTBEGINN = {"aktien":
date(2016, 9, 19), "krypto": None}` — ein **benanntes Literal je Markt mit der
Registerfundstelle (26.2 / 28.4) im Kommentar**, wie der Auftrag es vorgibt:
**nicht** `asof` minus Konstante gerechnet, **nicht** aus den vier
`multi_symbol_optimise.py` gelesen (Sperrliste; `T56b.6`, keine
Konstantenkopie). Neu daneben `horizontbeginn(bot)` und
`erste_falte_4a_messung(bot)`; der Plan trägt je Bot die zwei neuen Felder
`horizontbeginn` und `erste_falte_4a_warm_ab` (das früheste Warm-Datum, auf
Tagesebene — damit im Plan steht, gegen welches Datum (i) gerechnet wurde).
**Unverändert:** Bedingung (ii) (`erste_falte_trockenlauf.erste_falte_nach_3b`),
die Konjunktion in `erste_falte()` (25.3), die Signaturen von `erste_falte_4a`
und `erste_falte`. **`fensteranker` bleibt bestehen** — gemessen, wer ihn
sonst benutzt: `faltenplan_neun.py::plan_fuer_bot` (Z. 415, 445),
`embargo_neun.py:176`, `faltenschranke_messung.py:220, 236`.

---

### 32.2 Tatsachennotiz — die Wirkung je Bot

**Gemessen 21.09.2026, `trading-env/bin/python3` (Python 3.9.6), vorher am
Stand `41db199` (`docs/belege/TB-80/schritt0_ausgangsstand.txt`,
`schritt0_warm_ab.txt`), nachher am Stand `76c20ec`
(`docs/belege/TB-80/schritt2_wirkung.txt`). Beides aus dem Code gerechnet,
nicht aus einer Datei gelesen.**

| Bot | Markt | `erste_falte_4a` vorher | nachher | `erste_falte` vorher | nachher | Zahl der Selektionsfalten vorher → nachher |
|---|---|---:|---:|---:|---:|---|
| `elliott_wave` | krypto | 2018 | 2018 | 2018 | 2018 | 4 → 4 |
| `t3_supertrend` | krypto | 2018 | 2018 | 2019 | 2019 | 7 → 7 |
| `rsi2_crypto` | krypto | 2019 | 2019 | 2019 | 2019 | 7 → 7 |
| `turtle_soup_crypto` | krypto | 2018 | 2018 | 2018 | 2018 | 8 → 8 |
| `volatility_breakout_crypto` | krypto | 2018 | 2018 | 2018 | 2018 | 8 → 8 |
| `elliott_wave_stocks` | aktien | 2017 | 2017 | 2017 | 2017 | 9 → 9 |
| `rsi2_mean_reversion` | aktien | 2018 | 2018 | 2018 | 2018 | 8 → 8 |
| `turtle_soup_stocks` | aktien | 2017 | 2017 | 2017 | 2017 | 9 → 9 |
| `volatility_breakout` | aktien | 2018 | 2018 | 2018 | 2018 | 8 → 8 |

**Bots mit Änderung an `erste_falte_4a`, `erste_falte` oder Selektionsfalten:
0. Geänderte, neue oder entfallene Falten (Grenzen, Rolle, Training, Embargo):
0.** Die neun Zahlen stimmen mit 21.4 überein.

**Dieselbe Messung eine Ebene tiefer** — das früheste Datum, an dem ein Symbol
des Bots ab dem Anker warm ist (die Grösse hinter `erste_falte_4a`):

| Bot | Anker vorher (Datenuhr) | Horizontbeginn nachher | warm ab vorher | warm ab nachher | Verschiebung |
|---|---|---|---|---|---:|
| fünf Krypto-Bots | `None` | `None` | 2017-08-17 / 2017-08-17 / 2018-01-14 / 2017-09-16 / 2017-12-22 | unverändert | **+0 Tage** |
| `elliott_wave_stocks` | 2016-09-01 | 2016-09-19 | 2016-09-01 | 2016-09-19 | +18 Tage |
| `rsi2_mean_reversion` | 2016-09-01 | 2016-09-19 | 2017-06-20 | 2017-07-06 | +16 Tage |
| `turtle_soup_stocks` | 2016-09-01 | 2016-09-19 | 2016-10-14 | 2016-10-31 | +17 Tage |
| `volatility_breakout` | 2016-09-01 | 2016-09-19 | 2017-03-07 | 2017-03-22 | +15 Tage |

⭐ **Die fünf Krypto-Bots haben keinen Horizont (26.2), und bei ihnen ändert
sich nichts** — weder ein Jahr noch ein Tag. Das ist der Nachweis, dass die
Umstellung nur (i) trifft (Abbruchkriterium 4 des Auftrags, nicht
eingetreten). Ihre Einträge im neuen Plan unterscheiden sich vom
Ausgangsstand ausschliesslich im Text `erste_falte_quelle` und in den zwei
neuen Feldern.

⛔ **Nicht gemessen und nicht zu messen:** wie sich die Umstellung auf eine
Kennzahl eines Parametersatzes auswirkt (27.1, vor dem Tag).

---

### 32.3 Tatsachennotiz — der neue Plan daneben, die gesperrten Dateien unverändert

| Datei | SHA-256 | Stand |
|---|---|---|
| **`research/vorregistrierung/ergebnisse/faltenplan_tb80.json`** (neu, Commit `cadb968`) | **`2dd28291497e1233f6854651688f77d5d0a268370ef1ce423a42820917316794`** | Plan nach der Umstellung; zwei Läufe byteweise gleich; geschrieben vom Belegskript `docs/belege/TB-80/schritt2_faltenplan_tb80.py`, **nicht** von `faltenplan.py::main` (das schreibt immer nach `faltenplan.json`) |
| `research/vorregistrierung/ergebnisse/faltenplan.json` (Sperrliste Punkt 2) | `0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339` | **byteweise unverändert**, vorher und nachher gemessen |
| `research/vorregistrierung/ergebnisse/faltenplan_tb72.json` | `19e8cbca874d6e7455f2f3bc0723def9ea058d0b314fa1772e04cd64ff1c9d24` | **byteweise unverändert**; der Speicherstand vor TB-80 (`docs/belege/TB-80/faltenplan_stand_vor_tb80.json`, aus dem Code gerechnet) hat **denselben Hash** — der Plan von TB-72 war am Ausgang reproduzierbar |
| `research/vorregistrierung/ergebnisse/benchmark_drawdowns.json` (Sperrliste) | `a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee` | unverändert |
| `research/vorregistrierung/ergebnisse/benchmark_drawdowns_vt.json` (Sperrliste) | `4549395fb3ac30f852362ba586b3ac73cdb6b32e5e944a921f0adb239818745d` | unverändert |

⚠️ **`faltenplan_tb80.json` ist kein Sperrlistenpunkt und kein Registertext.**
Was der Plan nach 4a ist und wie er ins Register kommt, regelt Abschnitt 30
(genau eine Abbild-Datei, als neuer Sperrlistenpunkt, Betreiber). Diese Datei
liegt daneben, wie `faltenplan_tb72.json` daneben liegt.

---

### 32.4 Die Mutationsprobe — in beide Richtungen

**`docs/belege/TB-80/schritt3_mutationsprobe.py` / `.txt`, 21.09.2026, 20:25 UTC,
im Speicher (`HORIZONTBEGINN` ersetzt, `faltenplan.py` unverändert, nichts
committet), 49/49 Proben, `rc 0`.**

| Richtung | Eingriff | Ergebnis |
|---|---|---|
| **1 — die Datenuhr wieder eingesetzt** | `HORIZONTBEGINN = {markt: fn.fensteranker(markt)}` = `aktien 2016-09-01`, `krypto None` | Der Plan liefert **Bot für Bot den alten Stand** aus Schritt 0: `erste_falte_4a`, `erste_falte`, Selektionsfalten, alle Falten (Grenzen/Rolle/Training/Embargo) **und** die Warm-Daten auf Tagesebene (9 × 3 Proben). Gegen den neuen Plan weichen **alle vier Aktien-Bots** in `horizontbeginn` und `erste_falte_4a_warm_ab` ab; die fünf Krypto-Bots sind zeichengleich |
| ⚠️ **Wo Richtung 1 nicht beisst** | — | **Auf Jahresebene sind alter und neuer Stand gleich** (32.2: 0 Bots mit Änderung). Dort kann diese Richtung nichts verwerfen. **Sie beisst auf Tagesebene** — deshalb trägt der Plan seit TB-80 das Warm-Datum, und deshalb wurde es in Schritt 0 vor der Änderung gemessen |
| **2 — der Horizontbeginn ein Jahr nach hinten** | `aktien 2017-09-19` | **Alle vier Aktien-Bots bewegen sich um ein Jahr**: `erste_falte_4a` und `erste_falte` `elliott_wave_stocks` 2017 → 2018, `rsi2_mean_reversion` 2018 → 2019, `turtle_soup_stocks` 2017 → 2018, `volatility_breakout` 2018 → 2019; die Konjunktion hält (`erste_falte ≥ erste_falte_4a`, `H` in der ersten Kandidatenfalte 136/137); Krypto unverändert |
| Original wiederhergestellt | `{"aktien": 2016-09-19, "krypto": None}` | `erste_falte_4a_messung` je Bot = `faltenplan_tb80.json` (9/9) |

**Der Test** `research/faltenplan_neun/test_horizontbeginn.py` (Commit
`cb7f495`, 61/61 auf `trading-env/bin/python3` 3.9.6) prüft dauerhaft: die vier Aktien-Bots gegen 2016-09-19 und nicht
gegen die Datenuhr; die fünf Krypto-Bots gegen den Ausgangsstand aus Schritt 0;
die Konjunktion; und **das Literal gegen den Registertext 28.4** — der Test
liest die Tabelle in 28.4 und vergleicht sie mit `faltenplan.horizontbeginn(bot)`.
Gegenprobe: mit dem Literal auf 2016-09-01 wird er rot (15 Prüfungen,
`docs/belege/TB-80/schritt4_gegenprobe_test_rot.txt`).

---

### 32.5 ⭐ Entscheidungsvorlage, nicht vollzogen — wo der Horizontbeginn dauerhaft leben soll

**Heute (Zwischenstand, so benannt):** ein Literal je Markt in
`research/vorregistrierung/faltenplan.py` (`HORIZONTBEGINN`), mit der
Registerfundstelle im Kommentar und einem Test, der es gegen den Registertext
28.4 hält. Register 26.6 (letzte Zeile, „Entscheidungsvorlage, nicht
vollzogen") und 28.7 führen die Frage *„`RECENT_YEARS_ONLY` als registrierte
Grösse"* seit TB-77 offen; sie ist mit dieser Aufgabe nicht entschieden.

| Möglichkeit | Was es ist | Preis |
|---|---|---|
| **(a) `registerdaten.py` als registrierte Grösse** | `HORIZONTBEGINN` (oder `asof` und `RECENT_YEARS_ONLY` getrennt, mit dem Datum als Ableitung) wandert in das Modul, das *„die einzige Quelle für alles, was die Vorregistrierung festschreibt"* ist; `faltenplan.py` importiert es wie `GO_LIVE_SCHNITT` | Eine **Registeränderung** — `registerdaten.py` ist Träger der Festlegungen, die Änderung braucht den Betreiber (26.6). Und es entsteht die Frage, ob dort das Datum steht (eine Zahl, wie 28.4) oder die Formel (zwei Zahlen, eine davon aus den gesperrten Bot-Dateien — `T56b.6`) |
| **(b) aus dem Registertext gelesen** | Der Faltenplan liest die Tabelle in 28.4 zur Laufzeit, so wie der Test es heute tut | **Ein Parser auf Fliesstext** im Rechenpfad: das Register ist append-only, eine spätere Berichtigung stünde in einem neuen Abschnitt, und der Parser müsste wissen, welche Tabelle gilt. Was heute eine Prüfung ist, würde eine Abhängigkeit |
| **(c) Literal mit Test gegen das Register** | der heutige Stand | Die Zahl steht **zweimal** (Register, Code); der Test hält beide zusammen, solange er läuft. Läuft er nicht, ist es eine Konstante, die niemand gegenprüft |

⛔ **Keine Empfehlung nach Aufwand.** Die Vorlage nennt die drei Wege mit ihrem
Preis; die Wahl liegt beim Betreiber, gegebenenfalls nach Rückfrage beim
Verfahrensprüfer.

---

### 32.6 Was ausdrücklich NICHT getan wurde

| | |
|---|---|
| ⛔ | **Kein Bot-Code** — `strategies/`, `shared/` unberührt; die vier `multi_symbol_optimise.py` (TB-30b) unverändert |
| ⛔ | **Keine Sperrlisten-Datei** — `faltenplan.json`, `benchmark_drawdowns.json`, `benchmark_drawdowns_vt.json` byteweise unverändert (32.3); `faltenplan_tb72.json` unverändert; `auswertung.py` unberührt (auch nicht der Docstring) |
| ⛔ | **Kein `registerdaten.py`** — die Vorlage 32.5 ist nicht vollzogen |
| ⛔ | **Kein Tag, kein Lauf** — kein Selektionslauf, kein Parametersatz bewertet, keine Kennzahl gemessen (27.1) |
| ⛔ | **`fensteranker` nicht entfernt** — drei andere Aufrufer (32.1); ob er dort noch die richtige Grösse ist, ist eine andere Aufgabe |
| ⛔ | **Der Plan nach 4a nicht ins Register** — `faltenplan_tb80.json` liegt daneben; die Abbild-Datei nach Abschnitt 30 ist eine eigene, freizugebende Aufgabe |

---

### In einfacher Sprache

**Was schiefstand:** Das Regelwerk sagt seit dem Abend des 21.09., ab welchem
Tag jeder Aktien-Bot rechnen darf — dem 19. September 2016. Das Programm, das
die Auswertungsjahre bestimmt, nahm dafür noch ein anderes Datum: den letzten
Tag, für den Kursdaten vorliegen, zehn Jahre zurück, also den 1. September
2016. Achtzehn Tage Unterschied.

**Was gemacht wurde:** Das Datum aus dem Regelwerk steht jetzt im Programm,
mit Verweis auf die Stelle, aus der es kommt. Es wird nicht ausgerechnet und
nicht aus den Bot-Programmen abgeschrieben, sondern so genommen, wie das
Regelwerk es nennt. Ein Test liest die Tabelle im Regelwerk und prüft, dass
beide übereinstimmen.

**Was sich dadurch ändert:** Bei den Jahren — nichts. Alle neun Bots beginnen
in denselben Jahren wie vorher, mit denselben Auswertungsjahren. Achtzehn Tage
weniger Vorlauf haben bei keinem Bot gereicht, um ein Jahr zu verlieren. Auf
Tagesebene sieht man die Verschiebung: der Tag, an dem das erste Wertpapier
eines Aktien-Bots bereit ist, liegt jetzt 15 bis 18 Tage später. Bei den fünf
Krypto-Bots, die kein solches Fenster haben, ändert sich nicht einmal ein Tag.

**Warum das eine Zahl ist und keine Wahl:** Die Regel stand im Regelwerk,
bevor gemessen wurde, was sie kostet. Dass sie nichts kostet, ist ein
Ergebnis — es hätte auch anders ausgehen können, und dann hätte es genauso
dagestanden.

**Was noch offen ist:** Wo das Datum dauerhaft hingehört — in das Modul, das
alle Festlegungen trägt, oder als Literal mit Test. Das ist eine Entscheidung
des Betreibers; hier stehen die Wege mit ihrem Preis, ohne Empfehlung.

*Nachgetragen in TB-80, 21.09.2026. Umsetzung mit Befund, Tatsachennotizen,
Mutationsprobe und Entscheidungsvorlage: sie nennt, was der Code tat, was das
Register verlangt, was sich dadurch ändert (nichts an den Jahren, 15 bis 18
Tage darunter), was gesperrt bleibt und was offen ist — und entfernt nichts.*

---

## 33. Der Faltenplan als Registertext, und was die Abbild-Datei tragen muss (Fable 21k, 21.09.2026)

⭐ **Zwei Dinge in einem Abschnitt:** der Faltenplan nach 4a als Registertext
(Fables 30.2 (2)) und die **Berichtigung** seines Kriteriums aus 30.2 (3), das
er selbst zurückgenommen hat.

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21k_abbild_schema.md`,
zeichengleich. Anlass: `FABLE_ANFRAGE_2026-09-21e_abbilddatei_felder.md`.

### 33.1 Berichtigung zu 30.2 (3) — ein Symptom war zum Kriterium geworden

⚠️ **Der Satz in 30.2 (3)** — *„Trägt eine Datei Felder, die 4a nicht kennt
(Trainingsgrenzen, Embargo), ist sie nicht dieses Abbild"* — **ist ERSETZT.**
Er bleibt dort zeichengleich stehen.

**Der Anlass, gemessen 21.09.2026:** Alle drei vorhandenen Pläne tragen
`training_bis_ausschliesslich` (60 verschiedene Werte) und `embargo_nach_falten`
(29 verschiedene) — der gesperrte `faltenplan.json`, `faltenplan_tb72.json`
**und** der am selben Abend erzeugte `faltenplan_tb80.json`. ⭐ **Und: kein
Laufcode liest sie** — `training_bis_ausschliesslich` hat genau einen Treffer im
Repo, `faltenplan.py:306`, und das ist die Stelle, die es **schreibt**.

⭐⭐ **Fables Grund, warum „die Felder wirken ja nicht" trotzdem kein Kriterium
ist — wörtlich:**

> *„Das ist eine Aussage über Code, der **noch nicht eingefroren ist** (TB-30b
> steht aus). Ein Registertext, der davon abhängt, was der Code heute nicht
> liest, wandert mit dem Code — dieselbe Klasse wie die Datenuhr. Und: Ein
> Abbild ist nicht nur für den Lauf da, sondern für jeden, der später nachliest,
> was der Plan war. Sechzig verschiedene Trainingsgrenzen in einer Datei
> beschreiben ein Verfahren mit Trainingsfenster. Dass niemand sie liest, sieht
> man der Datei nicht an."*

### 33.2 Der Registertext — der Faltenplan nach 4a

> **Registertext (30.2 (2)), Faltenplan.** Der Faltenplan ist Registertext. Je
> Bot gelten: der Horizontbeginn (absolutes Datum oder ausdrücklich „kein
> Horizont"), die Faltenlänge in Jahren, die erste Selektionsfalte und die
> vollständige Liste der Selektionsfalten. Die Falten sind zusammenhängende
> Kalenderjahre in Schritten der Faltenlänge, aufsteigend und lückenlos vom
> Beginn der ersten Falte bis zum Go-Live-Schnitt. Eine Datei, die diesen Text
> maschinenlesbar wiedergibt, ist sein **Abbild** (33.3); der Registertext ist
> die Quelle.

> ⭐ **Ergänzt (34.1 und 34.2, TB-82, 22.09.2026):** Zwei Sätze von Fable (21m,
> Frage 1) schliessen diesen Registertext, Wortlaut in 34: **34.1** — bei
> Faltenlänge L > 1 werden (i) und (ii) am **ersten Jahr** der Falte geprüft, die
> Falte umfasst J bis J + L − 1, die folgenden schliessen lückenlos an; **34.2** —
> ein Rest von weniger als L Kalenderjahren zwischen der letzten vollen Falte und
> dem Go-Live-Schnitt ist **keine** Selektionsfalte. Der Text oben bleibt
> zeichengleich; die Tabelle unten ändert sich um nichts (Beleg M5).

> ⭐ **Ergänzt (35.1, TB-83, 22.09.2026):** Fable 22a fügt diesem Registertext die
> **Bestätigungsperiode** hinzu, Wortlaut in 35.1: die Datumsspanne von „Bestätigung
> ab" (21.4) bis zum Go-Live-Schnitt (5.2), Ende ausschliesslich; keine Falte im Sinn
> von 4a, (1b)/34.2 betrifft sie nicht. Ihr **Bezeichner** in Plan, Abbild,
> `zellen.csv` und Berichten ist die Spanne selbst, `JJJJ-MM-TT/JJJJ-MM-TT` — für
> alle neun Bots `2026-01-01/2026-09-01` (gemessen, Beleg M1/M2). Der heutige
> Faltenname in `faltenplan.py:336` ist danach unzulässig; die Umstellung ist nicht
> Teil von TB-83. Text und Tabelle oben bleiben zeichengleich (Beleg M5).

**Tatsachennotiz — der Plan, gemessen am 21.09.2026 (TB-81, HEAD `a0c6eb0`) aus
`research/vorregistrierung/ergebnisse/faltenplan_tb80.json` (Commit `cadb968`,
SHA-256 `2dd28291497e1233f6854651688f77d5d0a268370ef1ce423a42820917316794`;
Messung `docs/belege/TB-81/schritt1_faltenlisten.txt`, zwei unabhängige
Zählungen — aus `selektionsfalten` und aus `falten` mit `rolle == "selektion"` —
mit 0 Abweichungen, gegen 21.4 0 Abweichungen):**

| Bot | Markt | Horizontbeginn | Faltenlänge | erste Falte | Selektionsfalten | # |
|---|---|---|---:|---:|---|---:|
| `elliott_wave` | krypto | kein Horizont | 2 J | 2018–2019 | 2018–2019 · 2020–2021 · 2022–2023 · 2024–2025 | 4 |
| `t3_supertrend` | krypto | kein Horizont | 1 J | 2019 | 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 7 |
| `rsi2_crypto` | krypto | kein Horizont | 1 J | 2019 | 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 7 |
| `turtle_soup_crypto` | krypto | kein Horizont | 1 J | 2018 | 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 8 |
| `volatility_breakout_crypto` | krypto | kein Horizont | 1 J | 2018 | 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 8 |
| `elliott_wave_stocks` | aktien | 2016-09-19 | 1 J | 2017 | 2017 · 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 9 |
| `rsi2_mean_reversion` | aktien | 2016-09-19 | 1 J | 2018 | 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 8 |
| `turtle_soup_stocks` | aktien | 2016-09-19 | 1 J | 2017 | 2017 · 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 9 |
| `volatility_breakout` | aktien | 2016-09-19 | 1 J | 2018 | 2018 · 2019 · 2020 · 2021 · 2022 · 2023 · 2024 · 2025 | 8 |

*Lesehilfe zur Tabelle:* „kein Horizont" steht in der gemessenen Datei als
JSON-`null` unter dem Schlüssel `horizontbeginn` (Schlüssel gesetzt, Wert
null); der Go-Live-Schnitt ist bei allen neun Bots `2026-09-01`
(ausschliesslich, 5.2). Bei `t3_supertrend` trägt die Datei daneben
`erste_falte_4a = 2018`: Bedingung (i) allein ergäbe 2018, die Konjunktion mit
dem Trockenlauf (25.3) hebt die erste Selektionsfalte auf 2019 — der in 21.4
beschriebene Fall.

⚠️ **Zur Herkunft:** Die Werte ruhen auf `asof` = 2026-09-19 (28.3), dem
Horizontbeginn je Bot (28.4), dem Vorlauf gegen den Horizontbeginn (28.6), der
Konjunktion aus 25.3 und dem Trockenlauf nach 3b (b). ⭐ **Abschnitt 32 hat
gemessen, dass die Umstellung von der Datenuhr auf `asof` keine einzige Falte
bewegt** — die Liste ist also dieselbe wie vor der Umstellung, und das ist
belegt, nicht angenommen.

*Zitierhinweis (TB-81, gemessen):* „Trockenlauf nach 3b (b)" übernimmt den
Wortlaut aus 30.2 (2). In 16.7 ist **3b (a)** der Satz zum Trockenlauf („ein
Symbol an mindestens einem Handelstag handelbar"), **3b (b)** die
`MIN_HISTORY_*`-Tabelle, die der Trockenlauf anwendet; 21.3 (a), 21.4 und
`erste_falte_quelle` in der Datei zitieren den Trockenlauf als 3b (a). Gemeint
ist an beiden Stellen derselbe Trockenlauf; der Wortlaut von 30.2 (2) wird hier
nicht geändert (append-only), der Hinweis steht, damit niemand nach einem
zweiten Trockenlauf sucht.
⭐ *Nachtrag (TB-82, 22.09.2026):* Die ausdrückliche Berichtigung — „3b (b)" lies
„3b (a)" — steht jetzt als eigener Registersatz in **34.3** (Fable 21m, Frage 3);
die Marke am Satz selbst steht unter 30.2 (2).

> ⭐⭐ **Die Benchmark-Tabelle folgt diesem Plan (39.2/39.4, Fable 23a, TB-94,
> 23.09.2026):** Registertext zu Sperrlistenpunkt 4 / 23 / 33 (23a, Wortlaut in
> **39.2**): Die Tabelle, die der Lauf liest, hat je Bot genau die
> Selektionsfalten dieses Registertexts (plus Bestätigungsperiode) — nicht
> mehr, nicht weniger. Gemessen an der vollzogenen Tabelle gegen den Plan aus
> `faltenplan.py` (`7aa0b8cc…`) im Speicher (TB-91 Block D): **18/18 gleich**,
> Bestätigungszeile 9/9 `2026-01-01/2026-09-01`. Text und Tabelle oben bleiben
> zeichengleich.

> ⭐⭐ **Die Faltenlänge wird neu abgeleitet und gegen diesen Text verglichen
> (40.6, Fable 24a, TB-96, 24.09.2026):** Die Faltenlänge je Bot oben ruht auf
> den neun TB-24-Listen (`78e2bc6`), die nicht auf dem registrierten Snapshot
> erzeugt sind. Sie werden neu erzeugt (TB-98), die Faltenlänge wird nach 5.4
> abgeleitet und **gegen diesen Text verglichen**: gleich ⇒ Tatsachennotiz;
> verschieden ⇒ **Berichtigung dieses Texts** und allem, was daran hängt
> (Benchmark-Tabelle, Abbild), mit dem Grund „Eingabe war auf nicht-registriertem Datenstand erzeugt"
> — keine Wahl. Text und Tabelle oben bleiben bis dahin zeichengleich.

### 33.3 Die Feldliste des Abbilds — abschliessend

**Fables Ersatztext für 30.2 (3), zeichengleich:**

> Das Abbild trägt **genau** die Grössen, die der Registertext des Faltenplans nach 30.2 (2) nennt — nicht mehr, nicht weniger. Der Registertext 30.2 (2) zählt diese Grössen **abschliessend** auf (die Feldliste). Eine Datei ist das Abbild, wenn (i) ihre Feldmenge gleich der Feldliste ist und (ii) ihre Werte je Bot und je Jahr dem Registertext entsprechen. Beides prüft die Sonde nach 30.2 (3); ein zusätzliches Feld ist ein Fehlschlag wie ein fehlendes. Wie die Datei erzeugt wird, ist Handwerk; der erzeugende Code wird mit der Datei registriert (5e).

**Die Feldliste:**

| | Feld | Inhalt |
|---|---|---|
| | `asof` | das Datum aus 28.2/28.3 |
| je Bot | `bot` | der Name |
| je Bot | `horizontbeginn` | Datum **oder** ausdrücklich „kein Horizont" — ⭐ **gesetzt, nicht weggelassen** |
| | ↳ ⭐ **Ergänzt (34.4, TB-82, 22.09.2026)** | Der Wert ist entweder ein Datum im Format `JJJJ-MM-TT` oder die Zeichenkette `"kein Horizont"` — genau eine der beiden Formen; JSON-`null`, ein fehlender Schlüssel oder eine leere Zeichenkette sind Fehlschläge der Sonde, die den Wert **positiv** gegen die zwei Formen prüft (Fable 21m, Frage 4, Wortlaut in 34.4). `faltenplan_tb80.json` (`null`) ist auch daran kein Abbild |
| je Bot | ⭐ **`faltenlaenge_jahre`** | ⚠️ **Ergänzung gegenüber Fables Vorschlag — Begründung in 33.4** |
| je Bot | `erste_selektionsfalte` | die erste Falte |
| je Bot | `selektionsfalten` | die Liste, aufsteigend und lückenlos |
| | `quelle` | der Registerabschnitt, dessen Wortlaut die Datei abbildet |
| je Bot | ⭐ **`bestaetigungsperiode`** | ⚠️ **Angefügt (35.2, TB-83, 22.09.2026)** — der Bezeichner nach 33.2/35.1, genau in der Form `JJJJ-MM-TT/JJJJ-MM-TT` (Beginn/Ende, Ende ausschliesslich; registrierter Bestand: `2026-01-01/2026-09-01` bei allen neun); die Sonde prüft ihn positiv gegen die aus 21.4 und 5.2 gebildete Spanne. Fable 22a; Grund in 35.3 — ersetzt 33.4 Punkt 3 |

⛔ **Nicht in der Liste und damit nicht in der Datei:** Trainingsgrenzen,
Embargo, Purge. ⭐ *Fable, zwei Sätze aus 21k, je wörtlich:* *„Verfahren B hat
kein Trainingsfenster (Übergabe Abschnitt 1); eine Grösse, die das Verfahren
nicht kennt, kann nicht im Registertext stehen und darf deshalb nicht in der
Datei stehen."* — und zur Feldliste: *„das ist die Folge der Regel, nicht die
Regel."*

⇒ ⚠️ **Keine der drei vorhandenen Dateien ist danach das Abbild** — auch
`faltenplan_tb80.json` nicht, und zwar **nicht wegen ihrer Herkunft**, sondern
weil ihre Feldmenge nicht die Feldliste ist. *Nachgemessen (TB-81, Beleg
Schritt 1): `faltenplan_tb80.json` trägt je Bot 18 Felder und auf oberster
Ebene weder `asof` noch `quelle`.*

> ⭐⭐ **Gerechneter Plan und Abbild — die registrierte Abbildung (42.1 D5,
> 42.2 E3, 42.3 F4, Fable 25a–25c, TB-108, 25.09.2026):** Diese Feldliste ist
> die des **Abbilds**. Der Plan, den `faltenplan.py` zur Laufzeit bildet, trägt
> mehr — seine Herleitungsfelder (25.3/32.1) — und **schrumpft nicht**; er trägt
> aber keine Grösse, die das Verfahren nicht kennt (Trainingsgrenzen, Embargo,
> Purge, Mindesttraining; entfernt in TB-104 und TB-106). Die Sonde vergleicht
> Plan und Abbild über eine **registrierte Abbildung**; die **Feldliste des
> gerechneten Plans** ist Registertext (**42.2, E3** — die Zuordnung je
> Schlüssel steht aus, 42.6). Mit dem Abbild wird die **Erzeugerkette des
> Trockenlaufs** registriert (**42.3, F4**). Tabelle und Text oben bleiben
> zeichengleich.

> ⭐ **Eingaben in der Gruppe `eingefroren`: siehe 45.3, vollzogen in 45.11**
> (Fable 26a R3, TB-114, 26.09.2026). Tabelle, Text und die Marke oben bleiben
> zeichengleich.

### 33.4 ⚠️ Zwei Anpassungen an Fables Feldliste, und warum

**Er hat sie ausdrücklich zur Prüfung gestellt** (*„ich prüfe dann Text und
Feldliste zusammen"*) und eine Unsicherheit benannt.

| | Befund | Folge |
|---|---|---|
| **1** | ⚠️⚠️ **`selektionsfalten` als „Liste von Kalenderjahren" deckt `elliott_wave` nicht ab.** Gemessen: Seine vier Falten sind **Doppeljahre** (`2018-2019`, `2020-2021`, `2022-2023`, `2024-2025`), die der acht übrigen Bots Einzeljahre | Der Registertext in 33.2 sagt **„zusammenhängende Kalenderjahre in Schritten der Faltenlänge"** statt „Kalenderjahre" |
| **2** | ⭐ **Ohne `faltenlaenge_jahre` ist die Liste nicht prüfbar.** Aus `['2018-2019', …]` allein folgt nicht, ob die Faltenlänge 2 ist oder ob zwei Einzeljahre zusammengeschrieben wurden | Das Feld kommt in die Liste |
| **3** | **Seine Unsicherheit — die Bestätigungsperiode je Bot:** Sie steht **bereits** in Register 21.4 und folgt aus Faltenlänge und Go-Live-Schnitt (`elliott_wave` `2026-2027`, die acht übrigen `2026`) | ⭐ **Nicht in die Feldliste.** *Ein Abbild bildet ab, was sein Abschnitt sagt; eine Grösse, die anderswo registriert ist, wäre ein zweiter Ort für denselben Wert* — die Bauart, die er in 21j selbst abgelehnt hat |
| | ⚠️ **Berichtigt (34.6, TB-82, 22.09.2026):** Die Fundstelle „21.4" trägt den Satz nicht — 21.4 führt „Bestätigung ab" `2026-01-01` bei allen neun Bots (gemessen, Beleg M3); `2026-2027` und `2026` sind Faltennamen aus `faltenplan.py:336`, nicht aus dem Register (Beleg M2). Registriert ist die Bestätigungsperiode als **Datumsspanne**: Beginn 21.4 (`2026-01-01`), Ende 5.2 (`2026-09-01`, ausschliesslich) | Die Folge bleibt: **kein Feld** — Fables Halbsatz *„33.2 nennt sie nicht"* trägt allein. ⚠️ Welche der zwei Formen (Datumsspanne / Faltenname) gilt, ist **offen** — bei Fable, Anfrage 21g Punkt 3 (34.6) |
| | ⚠️ **ERSETZT (35.3, TB-83, 22.09.2026):** „Nicht in die Feldliste" gilt nicht mehr — Fable 22a, zeichengleich: *„Die Bestätigungsperiode ist Feld des Abbilds — weil 33.2 sie nennen muss (siehe 3), nicht weil 21.4 sie registriert. Mein Massstab bleibt; seine Anwendung ändert sich mit der Tatsache, dass der Name operativ ist."* Der Name ist ein Schlüssel, den `auswertung.py` (Z. 432) und der Erzeuger teilen (sechste Rücknahme). Feld `bestaetigungsperiode` in 33.3 angefügt (35.2); Punkt 3 oben bleibt zeichengleich | — |

⚠️ **Alle drei sind dem Verfahrensprüfer vorzulegen.** Punkt 1 und 2 ändern
seinen Wortlaut; Punkt 3 beantwortet seine Unsicherheit. ⛔ **Der Abschnitt gilt
bis dahin mit diesem Vermerk** — er ist nicht vorläufig, aber die Prüfung steht
aus.

### 33.5 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Abbild-Datei erzeugen** | eigene Aufgabe, nach Fables Prüfung von 33.2/33.3 und mit Betreiberfreigabe |
| ⛔ | **Die Sonde schreiben** (Feldmenge und Werte gegen den Registertext) | dieselbe Aufgabe |
| ⛔ | **Eine Datei mit Hash auf die Sperrliste nehmen** | dieselbe Aufgabe |
| ⛔ | **`faltenplan.py` ändern** — die Freigabe vom 21.09. galt für Bedingung (i) und ist verbraucht | — |
| ⚠️ | **Entscheidungsvorlage, nicht vollzogen:** ob die Abbild-Datei aus einem geänderten `faltenplan.py` entsteht oder aus einem **neuen, kleinen Schreiber**, der genau die Feldliste ausgibt. ⭐ *Fable: „gleichwertig, solange der Code registriert ist."* Beides berührt Sperrlisten-nahen Code und braucht eine eigene Freigabe | Betreiber |

> ⭐⭐ **Plan-Punkt 7 rückt vor (40.6/40.8 (g), Fable 24a, TB-96,
> 24.09.2026):** Das Abbild des Faltenplans (33.3) und die Faltenplan-Sonde
> sind die Wache gegen einen Schwellenübertritt, der den Faltenplan eines Bots
> verschiebt — und sie fehlen. ⚠️ **Erzeugt wird das Abbild NACH der
> Neu-Ableitung der Faltenlänge (TB-98), nicht vorher** — sonst bildet es einen
> Stand ab, der gerade geprüft wird (TB-100). Die Tabelle oben bleibt
> zeichengleich; die Freigaben, die sie verlangt, gelten weiter.

---

## 34. Fünf Einträge des Verfahrensprüfers aus 21l/21m und eine Berichtigung eines eigenen Satzes — Faltenregeln, `horizontbeginn`, „vier" → „neun" (TB-82, 22.09.2026)

⭐ **Reines Eintragen von Registertext.** Fünf Einträge sind zeichengleich von
Fable (vier aus 21m, einer aus 21l), der sechste berichtigt einen Satz des
steuernden Chats in 33.4. **Kein Code, keine Abbild-Datei, keine Sonde, kein
Hash, keine Wache** — 34.7.

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21m_faltenplan_pruefung.md`
(34.1–34.4) und `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21l_standpruefung.md`
(34.5), zeichengleich; 34.6 aus
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-21g_berichtigung_und_bestaetigungsperiode.md`
Punkt 2 und 3. Auftrag `docs/auftraege/MAC_TB-82_register_34.md`; Messungen
`docs/belege/TB-82/` (M1–M5), alle **vor** dem Eintrag gemessen, HEAD `9614624`.

⭐⭐ **Neu in diesem Abschnitt — die Marke steht AM ALTEN ORT.** Jeder der sechs
Einträge ist an zwei Stellen sichtbar: hier mit vollem Text, Herkunft und Grund,
und **direkt unter dem berichtigten Satz** als eingerückter Hinweisblock mit
Verweis auf 34.x. Der alte Satz bleibt zeichengleich; die Marke fügt nur hinzu
(dieselbe Bauart wie die Tatsachennotiz unter Sperrlistenpunkt 2, Abschnitt 10
und 30.3). *Fables Grund, 21m Frage 3, wörtlich:* *„Wer 30.2 (2) liest und
abschreibt, sieht 33.2 nicht — genau der Fehler aus 21h. Eine Marke am falschen
Satz kostet eine Zeile; ein Hinweis drei Abschnitte weiter kostet irgendwann
eine Rücknahme."* Prüfbar: `git diff --numstat` auf dieses Register zeigt für
TB-82 in der zweiten Spalte `0`.

⭐ **Fables Regel aus dem Vorab von 21m, die ab hier für jeden seiner Texte gilt,
wörtlich:** *„Wo mein Registertext eine Tatsache über den Bestand voraussetzt (ein Feld, eine Datei, eine Zahl von Modulen), nenne ich sie als Voraussetzung, und ihr messt sie, bevor der Text eingetragen wird."* — deshalb tragen 34.1, 34.2, 34.5 und 34.6 je eine
Tatsachennotiz mit der Messung, die der Text voraussetzt.

### 34.1 Ergänzung zu 33.2 — Falten mit Faltenlänge L > 1

**Fable, 21m Frage 1 (1a), zeichengleich:**

> **Ergänzung zu 33.2:** Bei Faltenlänge L > 1 ist ein Kalenderjahr J erstes Jahr einer Selektionsfalte, wenn J die Bedingungen (i) und (ii) nach 25 erfüllt; die Falte umfasst J bis J + L − 1. Die erste Selektionsfalte beginnt mit dem ersten Kalenderjahr, das (i) und (ii) erfüllt; die folgenden Falten schliessen lückenlos an.

**Fables Grund, zeichengleich:**

> *Grund:* (i) prüft den Vorlauf am 1. Januar — der einzige 1. Januar, an dem eine Falte beginnt, ist der ihres ersten Jahres. (ii) muss am ersten Jahr geprüft werden, weil die Falte sonst mit Jahren beginnen könnte, in denen der Bot nichts handelt — der Kapitalpfad (29) startet am 1. Januar der ersten Falte und braucht dort Handelbarkeit.

**Tatsachennotiz (TB-82, gemessen vor dem Eintrag, `m5_faltenlisten.txt`):**
Betroffen ist nur `elliott_wave` (L = 2); die acht übrigen Bots haben L = 1,
für sie ist 34.1 die Regel aus 25 unverändert. Für `elliott_wave` ergibt der
Text, auf das erste Jahr 2018 angewandt und lückenlos fortgesetzt, genau die
vier Falten aus 33.2 (2018–2019 · 2020–2021 · 2022–2023 · 2024–2025).
⭐ **Die Faltenliste in 33.2 ändert sich durch diese Ergänzung nicht** — die
neun Tabellenzeilen sind vor und nach dem Eintrag zeichengleich (SHA-256 der
Zeilen im Beleg) und gegen 21.4 mit 0 Abweichungen.

**Marke am alten Ort:** unter 33.2, nach dem Registertext-Block.

### 34.2 Ergänzung zu 33.2 — der Rest vor dem Go-Live-Schnitt

**Fable, 21m Frage 1 (1b), zeichengleich:**

> **Ergänzung zu 33.2:** Ein Rest von weniger als L Kalenderjahren zwischen der letzten vollen Selektionsfalte und dem Go-Live-Schnitt ist keine Selektionsfalte. Sein Verhältnis zur Bestätigungsperiode regelt 21.4; 33.2 trifft dazu keine Aussage.

**Fables Grund, zeichengleich:**

> *Grund:* 4a kennt nur ganze Falten; eine Teilfalte hätte weniger Beobachtungen als die übrigen und ginge mit gleichem Gewicht in den Faltenmedian — eine Verzerrung, die 4a nirgends zulässt. Kein Ergebnis: Für den registrierten Bestand tritt der Fall nicht ein; die Faltenliste ändert sich um nichts.

⭐⭐ **Tatsachennotiz — Antwort auf Fables ausdrückliche Unsicherheit** (21m:
*„ob 21.4 den Rest vor Go-Live bereits regelt — dann ist (1b) ein Verweis statt
einer Regel"*), **gemessen von TB-82 vor dem Eintrag** (`m1_rest.txt`, HEAD
`9614624`; die Zahl des steuernden Chats vom 21.09. an `ad020b5` wurde nicht
übernommen, sondern nachgemessen): Gesucht wurde im ganzen Register nach
`Rest` (als ganzes Wort, mit Positivkontrolle der Wortgrenze), `Teilfalte` und
`angebrochene` — **null Treffer**, in zwei Lesungen (`\b` und `-w`). 21.4 führt
je Bot ausschliesslich Markt, Faltenlänge, erste Falte, Anzahl der
Selektionsfalten, „Bestätigung ab" und „4b erfüllt" (`m3_bestaetigung_ab.txt`).
⇒ **(1b) ist eine Regel, kein Verweis.** Für den registrierten Bestand tritt
der Fall nicht ein: Bei allen neun Bots enden die Selektionsfalten mit 2025;
zwischen der letzten vollen Falte und dem Go-Live-Schnitt `2026-09-01` liegt bei
allen neun derselbe Rest, `2026-01-01` bis `2026-09-01` — kürzer als L bei
jedem Bot, also nach 34.2 keine Selektionsfalte. Die Faltenliste ändert sich
um nichts (34.1, Beleg M5).

**Marke am alten Ort:** unter 33.2, zusammen mit 34.1.

### 34.3 Berichtigung zu 30.2 (2) — `3b (b)` lies `3b (a)`

**Fable, 21m Frage 3, zeichengleich:**

> **Berichtigung zu 30.2 (2):** Die Fundstelle „Trockenlauf nach 3b (b)" lies „3b (a)". Gemeint ist der Trockenlauf aus 3b (a), der die `MIN_HISTORY_*`-Tabelle aus 3b (b) anwendet; ein zweiter Trockenlauf existiert nicht.

**Fables Grund, warum ein eigener Satz und nicht nur der Zitierhinweis in 33.2,
zeichengleich:**

> *Warum nicht nur der Hinweis in 33.2:* Wer 30.2 (2) liest und abschreibt, sieht 33.2 nicht — genau der Fehler aus 21h. Eine Marke am falschen Satz kostet eine Zeile; ein Hinweis drei Abschnitte weiter kostet irgendwann eine Rücknahme. Meine Zitierregel (nur vorgelegte Fundstellen) hat hier versagt, weil ich „3b (b)" aus 20e übernommen hatte, wo es um die Handelbarkeitstage ging — dieselbe Unternummer, andere Sache.

⚠️⚠️ **Der Satz „Trockenlauf nach 3b (b)" in 30.2 (2) bleibt zeichengleich
stehen** (append-only) und trägt die Marke **direkt unter 30.2 (2)** — genau
dieser Eintrag ist der Anlass für die Regel „Marke am alten Ort" im Kopf dieses
Abschnitts. Der Zitierhinweis in 33.2 (TB-81) bleibt ebenfalls zeichengleich
stehen und bekommt einen Satz, dass die ausdrückliche Berichtigung in 34.3
steht. Gemessen (TB-81, Beleg Schritt 2, unverändert): In 16.7 ist **3b (a)**
der Trockenlauf-Satz, **3b (b)** die `MIN_HISTORY_*`-Tabelle; 21.3 (a), 21.4
und `erste_falte_quelle` zitieren 3b (a).

### 34.4 Ergänzung zu 33.3, Feld `horizontbeginn` — Zeichenkette oder Datum

**Fable, 21m Frage 4, zeichengleich:**

> **Ergänzung zu 33.3, Feld `horizontbeginn`:** Der Wert ist entweder ein Datum im Format `JJJJ-MM-TT` oder die Zeichenkette `"kein Horizont"` — genau eine der beiden Formen. JSON-`null`, ein fehlender Schlüssel oder eine leere Zeichenkette sind Fehlschläge der Sonde. Die Sonde prüft den Wert positiv gegen diese zwei Formen, nicht das Vorhandensein des Schlüssels.

**Fables Grund, zeichengleich:**

> *Grund:* Derselbe wie bei der Feldliste — eine **positive** Prüfung gegen eine abschliessende Menge ersetzt ein Urteil über Abwesenheit. `null` ist genau das Gegenteil: ein Wert, der „nichts" bedeutet und in einer Bibliothek von „fehlt" unterscheidbar ist, in der nächsten nicht (euer Befund). „Gesetzt, nicht weggelassen" hiess: Wer die Datei liest, soll *lesen*, dass der Bot keinen Horizont hat — nicht schliessen, dass ihm einer fehlt. Eine Zeichenkette tut das; `null` verlangt Kenntnis der Konvention. Folge: `faltenplan_tb80.json` (Schlüssel mit `null`) ist auch daran kein Abbild; das war es nach 33.3 schon nicht.

⭐ **Folge, die Fable selbst zieht und die hier eingetragen wird:**
`research/vorregistrierung/ergebnisse/faltenplan_tb80.json` — Schlüssel
`horizontbeginn` mit JSON-`null` bei den fünf Krypto-Bots (33.2, Lesehilfe;
TB-81 Schritt 1) — ist **auch daran** kein Abbild; *„das war es nach 33.3 schon
nicht"* (Feldmenge 18 statt der Feldliste). Damit ist die in TB-81 offen
gelassene Frage, ob `null` das „ausdrücklich gesetzt" aus 33.3 ist,
**entschieden: nein.** Die Zeile in 33.2 („kein Horizont" steht in der
gemessenen Datei als JSON-`null`) bleibt als Tatsachennotiz zur gemessenen
Datei richtig; für das Abbild gilt 34.4.

**Marke am alten Ort:** in der Feldliste 33.3, als eigene Zeile direkt unter
`horizontbeginn`.

### 34.5 Berichtigung zu 29.4 — „vier" → „neun" `multi_symbol_optimise.py`

**Fable, 21l Punkt 4 (b), zeichengleich:**

> **Berichtigung zu 29.4:** Die Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte" wird in **allen neun** `multi_symbol_optimise.py` eingebaut, nicht nur in den vier Aktien-Optimierern. Der Bericht führt je Bot Horizontbeginn (oder „kein Horizont"), Beginn der ersten Selektionsfalte und frühesten Einstieg nebeneinander auf.

**Fables Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* Die Regel 29 (Kapitalpfad beginnt am 1. Januar der ersten Selektionsfalte) gilt je Bot für alle neun; 21c 3.2 hat den Fall für Krypto ausdrücklich benannt („rsi2_crypto: 2018 handelbar, erste Falte 2019"). „Die vier" stammt aus 21b, als die Wache noch gegen den Horizontbeginn prüfte, den nur Aktien-Bots haben. Mit dem Wechsel des Prüfdatums in 21c/29.4 hätte die Zahl mitwandern müssen; sie ist es nicht — mein Versehen, dieselbe Art wie der verlorene Vorlauf-Satz. Kein Ergebnis: Ob die Wache bei einem Krypto-Bot je anschlägt, ist für die Regel gleichgültig.

*Fables Einordnung, 21l, zeichengleich:* *„Kategorie: Berichtigung mit Ersatzwort, „vier" → „neun"; 29.4 bleibt stehen, Marke wie üblich."*

⭐ **Tatsachennotiz (TB-82, gemessen vor dem Eintrag, `m4_wachen_optimierer.txt`,
nur lesend):** In **keinem** der neun `strategies/<bot>/multi_symbol_optimise.py`
steht heute eine Wache — `assert `, `raise `, „Wache" je Datei **0**, in einer
zweiten, weiter gefassten Lesung (`assert`, `raise`, `wache` ohne Rücksicht auf
Gross-/Kleinschreibung, `Selektionsfalte`) ebenfalls **0**; neun Dateien, alle
vorhanden, SHA-256 je Datei im Beleg. ⇒ Der Einbau ist ein **Ersteinbau**, keine
Änderung — und er gehört zu **TB-30b**, nicht zu diesem Auftrag. Der Satz
„Ort der Wache unverändert: in den vier `multi_symbol_optimise.py`" in 29.4
bleibt zeichengleich stehen und trägt die Marke; unverändert gilt daraus:
**nicht** in `auswertung.py`.

**Marke am alten Ort:** unter 29.4, direkt am Absatz „in den vier
`multi_symbol_optimise.py`".

### 34.6 ⚠️ Berichtigung zu 33.4 Punkt 3 — eine Fundstelle des steuernden Chats trug ihren Satz nicht

⚠️ **Kein Fable-Eintrag, sondern die Berichtigung eines eigenen Satzes.** Was
in 33.4 Punkt 3 steht, bleibt zeichengleich: *„Sie steht **bereits** in
Register 21.4 und folgt aus Faltenlänge und Go-Live-Schnitt (`elliott_wave`
`2026-2027`, die acht übrigen `2026`)."*

> **Berichtigung zu 33.4 Punkt 3 (steuernder Chat, 21.09.2026; nachgemessen
> von TB-82 vor dem Eintrag, `m2_2026-2027.txt` und `m3_bestaetigung_ab.txt`).**
> Die Fundstelle „21.4" trägt den Satz nicht. **Gemessen:** 21.4 führt die
> Spalte **„Bestätigung ab"** mit dem Wert `2026-01-01` **für alle neun Bots**
> (9/9); die Werte `2026-2027` und `2026` als Faltenname kommen dort nicht vor
> (0 Treffer in den neun Zeilen, beide Strichformen). Gegenprobe über das ganze
> Register: `2026-2027` hat **genau einen** Treffer (Z. 5431 im Stand
> `9614624`), und das ist der berichtigte Satz selbst. **Die Werte stammen aus
> `research/vorregistrierung/faltenplan.py:336`** (`falten[-1]["name"]`, nur
> gelesen), also aus dem Code. **Registriert ist die Bestätigungsperiode
> gleichwohl** — ihr **Beginn** in 21.4 (`2026-01-01`), ihr **Ende** in 5.2
> (Go-Live-Schnitt `2026-09-01`, ausschliesslich), also als **Datumsspanne
> statt als Faltenname**. ⭐ **Fables Schluss in 21m Frage 2 (3) bleibt davon
> unberührt:** Sein erster Halbsatz — *„33.2 nennt sie nicht"* — trägt allein;
> die Bestätigungsperiode ist **kein Feld** der Feldliste.

⚠️⚠️ **Offen — hier eingetragen, nicht entschieden:**

> **Offen (an Fable, Anfrage 21g Punkt 3):** Der Begriff „Bestätigungsperiode"
> trägt zwei Formen — im Register eine **Datumsspanne** (`2026-01-01` bis
> `2026-09-01`), in `faltenplan.py` einen **Faltennamen**. Für `elliott_wave`
> klaffen sie: Der Name lautet `2026-2027`, die Periode endet am `2026-09-01`.
> ⚠️ **Welche Form gilt, ist nicht registriert.** Die Frage liegt bei Fable
> (Anfrage 21g); **dieser Abschnitt entscheidet sie nicht.**

> ⭐ **Beantwortet und ersetzt (35.1 / 35.3, TB-83, 22.09.2026):** Fable 22a hat
> entschieden — **die Datumsspanne gilt**; der Bezeichner ist die Spanne selbst,
> `JJJJ-MM-TT/JJJJ-MM-TT`, für alle neun Bots `2026-01-01/2026-09-01`; der Faltenname
> `2026-2027` ist unzulässig (35.1). Und der Schluss oben *„die Bestätigungsperiode
> ist **kein Feld** der Feldliste"* ist **ERSETZT**: `bestaetigungsperiode` ist Feld
> (35.2/35.3, Fables sechste Rücknahme — der Name ist ein Schlüssel, den
> `auswertung.py` und der Erzeuger teilen). Der Block oben bleibt zeichengleich.

**Marke am alten Ort:** in der Tabelle 33.4, als eigene Zeile direkt unter
Punkt 3.

### 34.7 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Abbild-Datei erzeugen** | eigene Aufgabe, eigene Betreiberfreigabe (33.5) |
| ⛔ | **Die Sonde schreiben** — auch nicht die positive Prüfung aus 34.4 | dieselbe Aufgabe |
| ⛔ | **Einen Hash auf die Sperrliste nehmen** | dieselbe Aufgabe |
| ⛔ | **`faltenplan.py` oder irgendeine `.py` ändern** — keine Freigabe; die vom 21.09. galt für Bedingung (i) und ist verbraucht | — |
| ⛔ | **Die Wache aus 29.4/34.5 einbauen** — sie ist Ersteinbau in allen neun Optimierern | TB-30b |
| ⛔ | **Die offene Frage aus 34.6 beantworten** | Fable (Anfrage 21g) |
| ⭐ | **Keine Zahl bewegt:** Faltenliste 33.2 vor und nach dem Eintrag zeichengleich (Beleg M5); die drei Sperrlisten-Hashes `0e54ac5c…`, `a163c498…`, `4549395f…` unverändert | — |

*Dieser Abschnitt ist rein additiv: Er trägt fünf Texte des Verfahrensprüfers
zeichengleich ein, berichtigt einen eigenen Satz, setzt zu jedem der sechs eine
Marke am alten Ort — und entfernt nichts.*

---

## 35. Die Bestätigungsperiode bekommt ihren Bezeichner und wird Feld des Abbilds, und 30.2 (3) wird präzisiert — die Sonde prüft den gerechneten Plan vor dem Start (Fable 22a, TB-83, 22.09.2026)

⭐ **Reines Eintragen von Registertext**, wie 34. Vier Einträge, alle
zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22a_bestaetigungsperiode.md` (Antwort
auf die Anfrage 21g des steuernden Chats, Punkte 2 und 3). Auftrag
`docs/auftraege/MAC_TB-83_register_35.md`; Messungen `docs/belege/TB-83/`
(M1–M6), alle **vor** dem Eintrag gemessen, HEAD `9dac8d4`. ⛔ **Kein Code,
kein Aufruf von `faltenplan.py`, keine Abbild-Datei, keine Sonde, kein
Wrapper, kein Hash** — 35.5.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text, Herkunft
und Grund **und** als Marke direkt beim alten Satz (33.2, 33.3, 33.4 Punkt 3,
34.6, 30.2 (3)). Die alten Sätze bleiben zeichengleich; `git diff --numstat`
auf dieses Register zeigt für TB-83 in der zweiten Spalte `0`.

⭐ **Damit ist die in 34.6 offen eingetragene Frage entschieden** — welche der
zwei Formen der Bestätigungsperiode gilt: **die Datumsspanne** (35.1). Und
**33.4 Punkt 3 („Nicht in die Feldliste") ist ERSETZT** (35.3) — Fables sechste
Rücknahme, aus einem Grund, den weder 21m noch 34.6 kannten: der Name ist ein
Schlüssel, den zwei Programme teilen.

### 35.1 Ergänzung zu 33.2 — die Bestätigungsperiode und ihr Bezeichner

**Fable, 22a Abschnitt 3, zeichengleich:**

> **Ergänzung zu 33.2 (Bestätigungsperiode):** Die Bestätigungsperiode eines Bots ist die Datumsspanne von „Bestätigung ab" (21.4) bis zum Go-Live-Schnitt (5.2), Ende ausschliesslich. Sie ist keine Selektionsfalte und keine Falte im Sinn von 4a; ihre Länge ist von der Faltenlänge des Bots unabhängig, und dass sie kürzer als eine Faltenlänge ist, ist gewollt — (1b) betrifft sie nicht. Ihr **Bezeichner** in Plan, Abbild, `zellen.csv` und Berichten ist die Spanne selbst in der Form `JJJJ-MM-TT/JJJJ-MM-TT` (Beginn/Ende, Ende ausschliesslich); für den registrierten Bestand bei allen neun Bots `2026-01-01/2026-09-01`. Ein Bezeichner, der Kalenderjahre ausserhalb der Spanne nennt, ist unzulässig.

**Fables Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 21.4 und 5.2 registrieren die Spanne; Verfahren B definiert die Bestätigungsperiode als den einzigen Out-of-Sample-Zeitraum (Übergabe Abschnitt 1). Ein Name, der mehr verspricht als die Spanne, würde beim Lesen der Ergebnisse — nach dem Lauf, wenn niemand mehr nachrechnet — als Zeitraum verstanden. Kein Ergebnis: Die Spanne ist unverändert, es ändert sich nur, wie sie heisst.

**Tatsachennotiz (TB-83, gemessen vor dem Eintrag — die Grundlage des
Bezeichners wird nicht übernommen, sondern gemessen):** 21.4 führt in der
Spalte „Bestätigung ab" bei **allen neun** Bots `2026-01-01` (9/9, Tabellenkopf
Z. 2917, Datenzeilen 2919–2927; `m1_bestaetigung_ab.txt`); 5.2 setzt den
Go-Live-Schnitt `2026-09-01`, **ausschliesslich** (`m2_go_live_schnitt.txt`),
und 21.4 wiederholt ihn im Vorsatz („Bestätigungsperiode unverändert bis
`2026-09-01`, ausschliesslich"). ⇒ Der Bezeichner nach 35.1 lautet für den
registrierten Bestand bei allen neun Bots **`2026-01-01/2026-09-01`** — aus 21.4
und 5.2 gebildet.

⚠️ **Ausdrücklich eingetragen:** Der **heutige** Bezeichner in
`research/vorregistrierung/faltenplan.py:336` ist der **Faltenname**
(`falten[-1]["name"]`: `2026-2027` bei `elliott_wave`, `2026` bei den acht
übrigen; gemessen, nur gelesen, `m4_faltenplan_bezeichner.txt` — zwei
Fundstellen, Z. 336 Erzeugung und Z. 368 Konsolenausgabe in `main()`) und damit
nach diesem Registertext **unzulässig**, weil er Kalenderjahre ausserhalb der
Spanne nennt. ⛔ **Die Umstellung ist Handwerk mit eigener Freigabe und nicht
Teil von TB-83**; sie hängt an Fables Antwort auf
`FABLE_ANFRAGE_2026-09-22a_sperrlistenfalle.md` (35.5). *Fable dazu,
zeichengleich:*

> *Folge, Handwerk:* `faltenplan.py:336` bildet den Namen heute aus dem Faltennamen; die Änderung ist eine Zeile und braucht eine Betreiberfreigabe. `auswertung.py` bleibt unberührt — es liest den Namen aus dem Plan, wie auch immer er lautet. Der Erzeuger schreibt denselben Bezeichner in `zellen.csv`; er ist noch nicht geschrieben, es kostet dort nichts. Die ⚠️-Markierung in 21.4 bei `elliott_wave`: bitte den ganzen Eintrag vorlegen, bevor jemand sie als Beleg nimmt — ich habe nur eure Vermutung dazu.

> ⚠️ **Marke (36.1 (4) und 36.3, Fable 22b, TB-84, 22.09.2026):** Die Umstellung
> von `faltenplan.py:336` (und der Ausgabe Z. 368) auf den Bezeichner ist
> **Schritt 3** der Reihenfolge in 36.3 und kommt **erst nach Schritt 2** —
> Voreinstellung von `main()` weg von `ergebnisse/faltenplan.json` und
> Einmal-Schreibsperre (36.1 (4)); davor Schritt 1, die Sperrlisten-Sonde.
> Fable, 22b: *„Wer Schritt 3 vor Schritt 2 macht, hat genau den Fall, den ihr beschreibt."*
> Betreiberfreigabe für alle vier Schritte steht aus (Stand 22.09.2026). Bis
> dahin: `python3 faltenplan.py` nicht aufrufen.

> ⭐⭐ **Berichtigung (38.1, Fable 22h, TB-89, 23.09.2026) — Weg (A):** Der
> Satz „die Änderung ist eine Zeile" im Handwerkszitat oben ist berichtigt.
> Der Bezeichner entsteht **dort, wo die letzte Falte ihren Namen bekommt**
> (`faltenplan.py`, Funktion `_plan`, Zuweisung der Rolle `bestaetigung`): die
> letzte Falte **heisst** die Spanne `2026-01-01/2026-09-01`; Faltenname,
> `bestaetigungsperiode`, Spalte `falte` und Bericht tragen denselben String
> aus derselben Quelle. Weg (B) — zwei Namen für dieselbe Periode — ist
> unzulässig. Umsetzung: TB-90, Freigabe liegt vor.

> ⚠️ **Tatsachennotiz zu den Zeilennummern oben (38.7 (a), TB-88, belegt
> 38.2):** Am Stand `8851f67` steht die Erzeugung auf **Z. 338**, die
> Konsolenausgabe auf **Z. 460** von `faltenplan.py` (Funktionen `_plan` und
> `main`); verschoben durch **`4daa254`** (TB-86 Schritt 2/3). Die Zahlen 336
> und 368 oben bleiben zeichengleich; sie gelten für den Stand, an dem TB-83
> sie gemessen hat.

> ⚠️⚠️ **Tatsachennotiz (38.7 (c), TB-88, Messstand `8851f67`):** Weg (B)
> hätte einen Sperrlistenpunkt berührt — `auswertung.py`, Funktion
> `lies_zellen`, vergleicht die Menge der `falte`-Werte gegen die Faltennamen
> des Plans und bricht unter (B) ab (Sperrlistenpunkt 5). Weg (A) läuft in der
> Probe durch. Einzelheiten in **38.1**.

⚠️ Zur ⚠️-Markierung bei `elliott_wave` in 21.4: Die Zelle lautet wörtlich
`⚠️ **2026-01-01**`; 21.4 trägt keinen Satz, der sie begründet. Fable bat, den
ganzen Eintrag vorzulegen, bevor jemand sie als Beleg nimmt (Anfrage 22a
Punkt 1) — hier nur gemessen, nicht gedeutet.

**Marke am alten Ort:** unter 33.2, nach der Marke aus 34. **Kein** Eintrag in
21.4 — 21.4 bleibt unberührt, 35.1 zitiert es nur.

### 35.2 Ergänzung zu 33.3 — `bestaetigungsperiode` wird Feld

**Fable, 22a Abschnitt 3, zeichengleich:**

> **Ergänzung zu 33.3 (Feldliste), je Bot:** `bestaetigungsperiode` — der Bezeichner nach 33.2, genau in dieser Form; die Sonde prüft ihn positiv gegen die aus 21.4 und 5.2 gebildete Spanne.

Die Feldliste in 33.3 wächst damit um **eine Zeile je Bot**; die Sonde prüft
den Wert **positiv** gegen die aus 21.4 und 5.2 gebildete Spanne — dieselbe
Bauart wie bei `horizontbeginn` (34.4). Der Grund, warum die Bestätigungsperiode
nun doch Feld ist, steht in 35.3.

**Marke am alten Ort:** in der Feldliste 33.3, als neue, angefügte
Tabellenzeile — keine bestehende Zeile geändert.

### 35.3 ⭐⭐ Fables sechste Rücknahme — warum die Bestätigungsperiode doch Feld ist

⚠️ **Das ERSETZT 33.4 Punkt 3 („Nicht in die Feldliste") und den Schluss von
34.6 („kein Feld der Feldliste").** Beide Sätze bleiben dort zeichengleich
stehen und tragen die Marke.

**Fables Begründung, 22a Abschnitt 2, zeichengleich:**

> **Aber Punkt 3 eurer Anfrage liefert eine Tatsache, die (3) trotzdem kippt** — nicht die Fundstelle, sondern die Rolle des Namens: Nach Nachtrag 2 (Z. 432–435) liest `auswertung.py` den Namen der Bestätigungsperiode aus dem Plan und sucht damit die Zeile in `zellen.csv`. **Der Name ist ein Schlüssel, den zwei Programme teilen müssen** — das eingefrorene `auswertung.py` und der noch zu schreibende Erzeuger. Ein Schlüssel, den zwei registrierte Programme teilen, ist eine Grösse des Verfahrens und gehört in den Registertext; und was 33.2 nennt, ist nach 33.3 Feld. Damit:

**Und der Registersatz, zeichengleich:**

> **(3), berichtigt:** Die Bestätigungsperiode ist Feld des Abbilds — weil 33.2 sie nennen muss (siehe 3), nicht weil 21.4 sie registriert. Mein Massstab bleibt; seine Anwendung ändert sich mit der Tatsache, dass der Name operativ ist.

**Fable selbst dazu, zeichengleich:**

> Das ist die sechste Rücknahme, und sie hat denselben Grund wie die fünf davor: Ich kannte den Bestand nicht — hier, dass der Name als Schlüssel dient.

**Tatsachennotiz (TB-83, gemessen, nur gelesen, `m3_auswertung_faltenplan.txt`):**
Der Schlüssel ist im eingefrorenen `auswertung.py` sichtbar — Z. 432
`name = plan[bot]["bestaetigungsperiode"]` in der Funktion
`bestaetigungsperiode()` (Z. 430), weitergereicht in Z. 550 und Z. 638. Der
Massstab aus 21m („ein Abbild trägt genau die Grössen seines Abschnitts") bleibt;
was sich ändert, ist die Tatsache, dass 33.2 die Bestätigungsperiode seit 35.1
nennt.

**Marken am alten Ort — zwei:** bei 33.4 Punkt 3 (als eigene Tabellenzeile
unter der Marke aus 34.6) und unter dem Offen-Block in 34.6.

### 35.4 Präzisierung zu 30.2 (3) — wann die Sonde prüft

**Fable, 22a Abschnitt 4, zeichengleich:**

> **Präzisierung zu 30.2 (3):** Der Lauf verwendet den Plan, den `faltenplan.py` zur Laufzeit bildet. Die Sonde vergleicht diesen Plan **vor dem Start des Laufs** mit dem Abbild (Feldmenge und Werte); bei Abweichung bricht der Laufwrapper ab, bevor `auswertung.py` aufgerufen wird. Das Abbild ist damit der registrierte Sollzustand, gegen den der gerechnete Plan geprüft wird — nicht die Datei, die `auswertung.py` öffnet.

**Fables Grund, zeichengleich (zwei Absätze aus 22a):**

> *Quelle des Grundes:* 21b (3) — das Einfrieren von `auswertung.py` hat Vorrang; die Prüfung wandert dorthin, wo geändert werden darf (Wrapper, `faltenplan.py`), wie schon bei der Wache. Kein Ergebnis.

> Ohne diese Präzisierung wäre 30.2 (3) beim ersten Lauf falsch: Es gäbe eine gesperrte Datei, die niemand liest, und einen gerechneten Plan, den niemand prüft.

**Tatsachennotiz (TB-83, aus Nachtrag 1 bestätigt, `m3_auswertung_faltenplan.txt`):**
`auswertung.py` bezieht den Plan über **genau einen** Aufruf,
`plan = fp.faltenplan(mess)` in **Z. 589** (`import faltenplan as fp`, Z. 96) —
es **rechnet** ihn zur Laufzeit; die einzige Plandatei, die es öffnet, ist
`benchmark_drawdowns.json` (Z. 590, Sperrlistenpunkt 4), keine
`faltenplan*.json`. ⇒ 30.2 (3) „der Lauf liest genau diese" ist ab hier so zu
lesen, wie 35.4 es sagt: Das Abbild ist der **Sollzustand**, gegen den der
gerechnete Plan **vor dem Start** geprüft wird; bei Abweichung bricht der
Laufwrapper ab, bevor `auswertung.py` aufgerufen wird. Sonde und Wrapper sind
**nicht** geschrieben (35.5).

**Marke am alten Ort:** direkt unter 30.2 (3), innerhalb des
Registertext-Blocks — wie die Marke aus 34.3 unter (2).

> ⭐ **„Feldmenge und Werte" heisst: über die registrierte Abbildung (42.2 E3,
> Fable 25b, TB-108, 25.09.2026):** Die Sonde vergleicht den gerechneten Plan
> mit dem Abbild je Feld des Abbilds über den Planschlüssel, aus dem es gebildet
> wird; ein Planschlüssel ausserhalb der registrierten Feldliste des Plans ist
> ein Befund, ein fehlender ebenso. Fables erste Fassung dazu (25a, „trägt keine
> Grösse, die 33.2/33.3 nicht kennt") ist berichtigt (**42.1 D5 → 42.2 E3**).
> Der Text oben bleibt zeichengleich.

### 35.5 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **`faltenplan.py:336` auf den neuen Bezeichner umstellen** — keine Freigabe; hängt an Fables Antwort auf die Sperrlistenfalle (Anfrage 22a Punkt 3: `main()` schreibt nach `ergebnisse/faltenplan.json`, Sperrlistenpunkt 2) | Betreiber, nach Fable |
| ⛔ | ⚠️⚠️ **`python3 faltenplan.py` ausführen** — in dieser Sitzung **nicht geschehen**; der Hash von `ergebnisse/faltenplan.json` ist vor **und** nach der Arbeit `0e54ac5c…` (`m6_sperrlisten_hash.txt`) | — |
| ⛔ | **Die Abbild-Datei erzeugen** — jetzt mit dem Feld `bestaetigungsperiode` | eigene Aufgabe, Betreiberfreigabe (33.5) |
| ⛔ | **Die Sonde schreiben** — Feldmenge, Werte, die positiven Prüfungen aus 34.4 und 35.2, der Zeitpunkt aus 35.4 | dieselbe Aufgabe |
| ⛔ | **Den Laufwrapper mit dem Abbruch aus 35.4 bauen** | dieselbe Aufgabe |
| ⛔ | **Einen Hash auf die Sperrliste nehmen** | dieselbe Aufgabe |
| ⛔ | **Irgendeine `.py` ändern** | — |
| ⭐ | **Keine Zahl bewegt:** Faltenliste 33.2 vor und nach dem Eintrag zeichengleich (Beleg M5); die drei Sperrlisten-Hashes unverändert | — |
| ⚠️ | **Offen bei Fable:** *„**Unsicher:** ob `faltenplan.py` den Namen der Bestätigungsperiode noch an anderer Stelle verwendet als Z. 336 (dann mehr als eine Zeile) — Handwerk, zu messen vor der Freigabe."* — die Anfrage 22a Punkt 2 hat dazu gemessen (zwei Fundstellen in `faltenplan.py`, Z. 336 und 368; im Laufkreis zieht alles mit); seine Antwort steht aus | Fable |

*Dieser Abschnitt ist rein additiv: Er trägt vier Texte des Verfahrensprüfers
zeichengleich ein, setzt fünf Marken am alten Ort, entscheidet die in 34.6
offene Frage durch Fables Text — und entfernt nichts.*

---

## 36. Die Schreibregel für Sperrlistenpfade, die Sperrlisten-Sonde mit drei Ausgängen, das Abbild der Sperrliste als neue Datei und die Reihenfolge der Handwerksschritte — und eine Tatsachennotiz zur ⚠️-Markierung in 21.4 (Fable 22b und 22c, TB-84, 22.09.2026)

⭐ **Reines Eintragen von Registertext**, wie 34 und 35. Sechs Einträge — vier
Ersteinträge (36.1, 36.2, 36.5, 36.6), eine Reihenfolge (36.3) und eine
Tatsachennotiz (36.4) —, alle Fable-Texte zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22b_schreibregel_sperrliste.md`
(Antwort auf die Anfrage 22a des steuernden Chats, die Sperrlistenfalle:
`faltenplan.py main()` schreibt nach `ergebnisse/faltenplan.json`,
Sperrlistenpunkt 2) und
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22c_drei_ausgaenge_und_abbild.md`
(Antwort auf die Anfrage 22b, Frage 1 und 2; **berichtigt einen Satz aus 22b
am selben Tag**, 36.5). Auftrag `docs/auftraege/MAC_TB-84_register_36.md`
(erweitert um 36.5 und 36.6, bevor Abschnitt 36 eingetragen war); Messungen
`docs/belege/TB-84/` (M1–M6), alle **vor** dem Eintrag gemessen, HEAD `4bbd720`.
⛔ **Kein Code, keine Sonde, kein Umbau von `main()`, kein Aufruf von
`faltenplan.py`, keine Abbild-Datei, kein Hash, keine Freigabe** — 36.7.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (Sperrliste
Punkt 2, Überschrift von Abschnitt 10, 35.1, 21.4 — und für die Berichtigung
aus 36.5 an den zwei Sätzen in 36.1 und 36.2, die sie berichtigt). Die alten
Sätze bleiben zeichengleich; `git diff --numstat` auf dieses Register zeigt für
TB-84 in der zweiten Spalte `0`.

⚠️ **Was dieser Abschnitt ist:** Er schliesst die Lücke, die die Anfrage 22a
gemessen hat — *Fable, 22b Abschnitt 2, zeichengleich:* *„Was ihr gemessen habt, ist nicht ein Fehler in `faltenplan.py`, sondern **das Fehlen einer Regel**: Nirgends steht, dass ein Programm eine gesperrte Datei nicht schreiben darf. Die Sperrliste sagt, *was* unverändert bleiben muss; sie sagt nicht, *wer* es sicherstellt. Acht Tage lang war das der Zufall."* Die Regel steht ab hier
(36.1); wer sie ausführt, steht ebenfalls (36.2), mit welchen Ausgängen (36.5)
und gegen welches Abbild (36.6); und in welcher Reihenfolge das Handwerk folgt,
steht in 36.3. ⚠️ **Gebaut ist davon nichts** — die Freigabe des Betreibers
für die vier Handwerksschritte steht aus (36.3, 36.7), und bei Fable stehen
eine Tatsachennotiz und eine Frage aus (36.6).

### 36.1 Schreibregel für Sperrlistenpfade — Ersteintrag

**Fable, 22b Abschnitt 2, zeichengleich:**

> **Registertext, Ersteintrag — Schreibregel für Sperrlistenpfade:**
> **(1)** Kein Programm im Repo schreibt an einen Pfad, der auf der Sperrliste steht oder für sie bestimmt ist. **(2)** Jeder Erzeuger einer solchen Datei schreibt **einmalig**: Existiert die Zieldatei bereits, bricht er ab (Rückgabewert ≠ 0), nennt Pfad und Hash der vorhandenen Datei und schreibt nichts. Er überschreibt nie, auch nicht mit identischem Inhalt. **(3)** Ein anderes Ziel nur durch ausdrückliches Argument; die Voreinstellung eines Erzeugers ist nie ein Pfad, der auf der Sperrliste steht. **(4)** Für `faltenplan.py main()`: Voreinstellung weg von `ergebnisse/faltenplan.json` (Sperrlistenpunkt 2) auf einen nicht gesperrten Pfad, und die Einmal-Schreibsperre nach (2). Beides vor jeder weiteren Änderung an `faltenplan.py`, insbesondere vor Z. 336.
>
> > ⚠️ **Präzisiert durch 36.5 (Fable 22c, TB-84, 22.09.2026):** „bricht er ab (Rückgabewert ≠ 0)" in (2) — der Wert ist **1**: der Erzeuger hat geprüft und einen Befund („Ziel existiert, Hash …"), nicht 2. Der Satz oben bleibt zeichengleich stehen.

**Fables Abwägung der drei Wege aus der Anfrage 22a, zeichengleich:**

> **Zu den drei Wegen:** (c) fällt nach A8 — eine Regel, die niemand ausführt, ist keine Wache; ihr sagt es selbst. (a) allein beseitigt den Fall, nicht die Klasse: Der neue Zielname landet, sobald er Abbild ist, selbst auf der Sperrliste — und `main()` überschreibt ihn beim nächsten Aufruf genauso. (b) allein lässt ein Programm stehen, dessen **Voreinstellung** eine gesperrte Datei ist, mit einer Sicherung davor; die Sicherung muss dann die Sperrliste kennen, und das ist ein zweiter Ort, an dem die Sperrliste steht.

**Fables Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* Zweck der Sperrliste („nichts Gesperrtes ist bewegt worden", Übergabe Abschnitt 5) und A8 (eine Wache ist, was jemand ausführt). Die Einmal-Schreibsperre braucht keine Sperrlistenkenntnis — sie schützt auch die Abbild-Datei, die noch nicht auf der Liste steht, und sie schützt gegen den Fall, den niemand vorausgesehen hat. 21b (3): Prüfungen wandern dorthin, wo geändert werden darf. Kein Ergebnis: Kein Inhalt einer Datei ist berührt; es geht darum, dass keiner berührt werden kann.

**Und sein Satz zur Härte der Sperre, zeichengleich:**

> *Warum „nie überschreiben, auch nicht mit identischem Inhalt":* Eine Sperre, die bei gleichem Inhalt durchlässt, muss den Inhalt vergleichen — und wer den Vergleich programmiert, entscheidet, was „gleich" heisst (Schlüsselreihenfolge, Zeilenende, `sort_keys`). Die Sperre ist stärker, wenn sie dümmer ist.

⭐ **Fables Tatsachennotiz, zeichengleich:**

> **Tatsachennotiz dazu:** `ergebnisse/faltenplan.json` (Hash `0e54ac5c…`) ist seit dem 14.09. unverändert, obwohl `faltenplan.py main()` seit demselben Tag bei jedem Aufruf dorthin schreibt; TB-72 und TB-80 haben eigene Belegskripte verwendet. Der Bestand hielt durch Übung, nicht durch Regel. Der Hash ist am 22.09. gemessen und stimmt.

**Tatsachennotiz (TB-84, gemessen vor dem Eintrag, `m2_sperrlisten_hash.txt`
— Fables Notiz wird nicht übernommen, sondern nachgemessen):**
`research/vorregistrierung/ergebnisse/faltenplan.json` hat SHA-256
`0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339`, mtime
14.09.2026 17:55, letzter berührender Commit `a2fcf01` (TB-30a, 14.09.2026) —
**keine** Änderung seit dem Ersteintrag, obwohl `faltenplan.py` selbst seither
geändert wurde (letzter Commit `76c20ec`, 21.09.2026, TB-80). Die Schreibstelle
in `main()` ist, nur gelesen: Z. 372 `ziel = os.path.join(_HIER, "ergebnisse",
"faltenplan.json")`, Z. 373 `with open(ziel, "w", …)`, Z. 374 `json.dump(…)` —
Voreinstellung ohne Argument, ohne Abfrage, ob die Datei besteht: genau der
Fall, den (2), (3) und (4) ausschliessen. Der Hash ist **nach** dem Eintrag
erneut gemessen und gleich (36.7). ⇒ Fables Notiz stimmt in jedem Wort: *Der
Bestand hielt durch Übung, nicht durch Regel.*

⚠️ **Was (4) heute bedeutet, ausdrücklich:** Die in 35.1 eingetragene
Umstellung von `faltenplan.py:336` auf den Bezeichner `JJJJ-MM-TT/JJJJ-MM-TT`
darf nach (4) **erst nach** der Voreinstellungs-Änderung und der
Einmal-Schreibsperre in `main()` kommen — das ist Schritt 3 nach Schritt 2 in
36.3. Bis dahin gilt weiter: `python3 faltenplan.py` wird nicht aufgerufen.

**Marke am alten Ort:** unter **Sperrliste Punkt 2** (Abschnitt 10), als
eingerückter Block **unter** der Tatsachennotiz aus Abschnitt 30 — diese bleibt
zeichengleich stehen. Dazu die Marke aus 36.5 direkt unter dem Registertext
oben, am „(Rückgabewert ≠ 0)" in (2).

### 36.2 Die Sperrlisten-Sonde — Ersteintrag

**Fable, 22b Abschnitt 2, zeichengleich:**

> **Registertext, Ersteintrag — Sperrlisten-Sonde:**
> Vor dem signierten Tag existiert ein Prüfskript, das für **jeden** Sperrlistenpunkt Pfad und Hash gegen den Registertext prüft und bei einer Abweichung mit Rückgabewert ≠ 0 endet und den Punkt nennt. Der Registertext der Sperrliste ist die Quelle; eine maschinenlesbare Fassung ist Abbild und wird von der Sonde selbst gegen den Registertext geprüft (Bauart 33.3). Die Sonde läuft (a) als Nachweis vor dem Tag, (b) im Laufwrapper vor `auswertung.py`, (c) am Ende jedes Auftrags, der Sperrlisten-nahen Code berührt. Ein Sperrlistenbruch, den die Sonde findet, ist eine Tatsachennotiz — nie eine stille Reparatur.
>
> > ⚠️ **Berichtigt durch 36.5 (Fable 22c, TB-84, 22.09.2026):** „mit Rückgabewert ≠ 0 endet und den Punkt nennt" lies „mit Rückgabewert 1 endet und den Punkt nennt; kann ein Punkt nicht geprüft werden (Datei fehlt, Registertext nicht lesbar), endet sie mit 2 und nennt ihn". Der Satz oben bleibt zeichengleich stehen; die drei Ausgänge gelten nach 36.5 für jede Sonde und jede Wache.
>
> > ⚠️⚠️ **Ergänzt durch 37.3 (Fable 22g, TB-87, 22.09.2026):** „bei einer Abweichung … endet" — **was ein Befund bedeutet, hängt vom Tag ab.** Vor dem signierten Tag ist ein Befund `1` zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz), und wird durch ein neues Abbild unter neuem Namen geschlossen; **nach** dem Tag ist er ein Sperrlistenbruch und wird nach 10.1 behandelt (Amendment, Lauf von vorn). Der Satz oben bleibt zeichengleich stehen.

**Fables Unsicherheit dazu, 22b, zeichengleich:**

> **Unsicher:** ob es bereits ein Prüfskript für die Sperrliste gibt (etwa nach dem Muster `snapshot.py --pruefen`) — dann ist Schritt 1 eine Erweiterung, kein Neubau; ihr seht es im Repo.

⭐⭐ **Drei Tatsachennotizen des steuernden Chats (Anfrage 22b, 22.09.2026,
07:35), von TB-84 vor dem Eintrag nachgemessen (M3–M5, `m3_snapshot_ausgaenge.txt`,
`m4_herkunft_listen.txt`, `m5_vt_in_listen.txt`, HEAD `4bbd720`).** Sie waren
Fable mit `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-22b_sonde_bestand.md`
vorgelegt; seine Antwort (22c) liegt vor und ist in 36.5 und 36.6 eingetragen:

> **(a) Das Muster existiert, die Sache nicht.** `shared/snapshot.py --pruefen`
> (1306 Zeilen) prüft **Datenstände**, nicht die Sperrliste, und hat **drei**
> Ausgänge — gemessen im Kopf der Datei, Z. 217–219: `0` *„in Ordnung: gezogen,
> oder `--pruefen` findet den Stand unveraendert"*, `1` *„Befund: `--pruefen`
> findet den Snapshot VERAENDERT"*, **`2` *„NICHT PRUEFBAR / abgebrochen"***.
> Begründung ebendort (Z. 221–224), wörtlich: *„Die 2 ist der Grund, warum es
> sie gibt. In TB-45 haben zwei Wachen "bestanden" gemeldet, ohne etwas gemessen
> zu haben - ein gescheiterter Aufruf und ein leeres Ergebnis sahen gleich aus.
> Hier nicht: wer nicht messen konnte, sagt es mit einem eigenen Wert."*
> ⚠️ Der Registertext oben sagt nur „Rückgabewert ≠ 0" und unterscheidet die
> beiden roten Fälle nicht — nach `A2` („konnte nicht messen" ist ein eigenes
> Ergebnis, nicht grün und nicht rot) und `A8` sind sie verschieden.
> **Frage 1 an Fable** (drei Ausgänge?) — ⭐ **beantwortet: ja, in 36.5.**
>
> **(b) `herkunft.py` scheidet als Ort aus.** `research/vorregistrierung/herkunft.py`
> (260 Zeilen): sein `--pruefen` meldet die vier Verankerungen (append-only-Kette,
> GPG, OpenTimestamps), nicht Sperrlisten-Hashes — **und die Datei steht selbst
> auf der Sperrliste** (Punkte **11** `herkunft.py::register()` und **12**
> `herkunft.py::datenstand()`, gemessen M1: 14 Punkte in Abschnitt 10). Die
> Sonde kann dort nicht eingebaut werden, ohne gesperrten Code zu öffnen; sie
> braucht eine **eigene Datei**. ⇒ Schritt 1 in 36.3 ist ein **Neubau nach
> vorhandenem Muster**, keine Erweiterung. ⭐ Fable 22c, Abschnitt 0: *„angenommen, und es bestätigt die Bauart aus 22b (Sonde als eigene, nicht gesperrte Datei)"*.
>
> **(c) ⚠️ Zwei maschinenlesbare Listen liegen bereits in `herkunft.py`** und
> decken sich **nicht** mit dem Registertext: `EINGEFROREN` (Z. 57, **zehn**
> Einträge: `registerdaten.py`, `faltenplan.py`, `benchmark.py`, `kennzahlen.py`,
> `auswertung.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`,
> `ergebnisse/messgroessen.json`, `ergebnisse/faltenplan.json`,
> `ergebnisse/benchmark_drawdowns.json`) und `SPERRLISTE_DATEIEN` (Z. 66,
> **fünf** Muster: `shared/messkette.py`, `shared/zuteilung.py`,
> `strategies/*/equity_simulation.py`, `strategies/*/multi_symbol_optimise.py`,
> `strategies/*/multi_symbol_walk_forward.py`) gegen **14** Registerpunkte (M1).
> Gemessen (M5, 0 Treffer, Positivkontrolle `faltenplan.json` 1 Treffer):
> `ergebnisse/benchmark_drawdowns_vt.json` (Sperrlisten-Hash `4549395f…`) steht
> in **keiner** der beiden Listen, ebenso wenig die beiden Universumsdateien aus
> Punkt 8 (`config/top25_symbols.txt`, `config/sp500_top150.txt`); umgekehrt
> führt `EINGEFROREN` Dateien, die der Registertext nicht als eigene Punkte nennt
> (`kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`,
> `ergebnisse/messgroessen.json`). ⛔ **Nicht bewertet** — ob `EINGEFROREN`
> überhaupt als Sperrlisten-Abbild gemeint war oder für Abschnitt 0 („vor dem
> Lauf geschrieben und eingefroren"), steht nirgends. Genau der Zustand, gegen
> den die Sonde nach 36.2 schützen soll — eine maschinenlesbare Fassung, die vom
> Registertext abweicht und nie dagegen geprüft wurde —, besteht damit heute
> schon. **Frage 2 an Fable** (welche Liste wird Abbild?) — ⭐ **beantwortet:
> keine, in 36.6**; die Tatsachennotiz zu den beiden Listen steht bei Fable aus.

⭐ Die Antwort auf Fables Unsicherheit lautet damit, gemessen: **Das Muster
gibt es, die Sache nicht.** Die Sonde selbst ist Schritt 1 in 36.3 und
**nicht** freigegeben.

**Marke am alten Ort:** unter der **Überschrift von Abschnitt 10**, als
Hinweisblock, zusammen mit der Marke aus 36.6.

### 36.3 Die Reihenfolge der Handwerksschritte

**Fable, 22b Abschnitt 3, zeichengleich — Vorsatz und die vier Schritte:**

> Alle mit Betreiberfreigabe; die Reihenfolge ist Verfahren, weil jeder Schritt den nächsten absichert:
>
> 1. **Sperrlisten-Sonde** schreiben und einmal laufen lassen — Nachweis, dass heute alles stimmt (der Nullpunkt).
> 2. **`faltenplan.py main()`:** Voreinstellung ändern, Einmal-Schreibsperre einbauen. **Mutationsprobe:** `main()` gegen eine Kopie von `faltenplan.json` am neuen Zielpfad aufrufen → muss abbrechen; Sonde danach → grün.
> 3. **Erst jetzt** Z. 336 (Bezeichner der Bestätigungsperiode, 22a). Prüfen über `main()` ist ab jetzt ungefährlich; Sonde danach → grün.
> 4. Abbild-Datei, Faltenplan-Sonde (33.3), Hash auf die Sperrliste — wie geplant; der Erzeuger des Abbilds unterliegt der Schreibregel von Anfang an.

**Fables Satz dazu, zeichengleich:**

> Wer Schritt 3 vor Schritt 2 macht, hat genau den Fall, den ihr beschreibt. Deshalb steht die Reihenfolge hier und nicht nur im Auftrag.

⛔ **Eingetragen, ausdrücklich:** Alle vier Schritte brauchen
**Betreiberfreigabe**. Am 22.09.2026, 07:40 (Erstellung des Auftrags TB-84)
ist **keine** erteilt; TB-84 hat keine erhalten und keinen der vier Schritte
begonnen (36.7). Die Reihenfolge ist **Verfahren**, nicht Empfehlung: Schritt 3
(Z. 336, 35.1) ist ohne Schritt 2 genau die in Anfrage 22a gemessene Falle, und
Schritt 2 ohne Schritt 1 hat keinen Nullpunkt, gegen den seine Mutationsprobe
gemessen würde. Der Erzeuger der Abbild-Datei (Schritt 4, 33.3/35.2)
unterliegt der Schreibregel 36.1 von seinem ersten Aufruf an; seine Ausgänge
regelt 36.5, das Abbild der Sperrliste 36.6.

**Marke am alten Ort:** in **35.1**, direkt beim Absatz über den heutigen
unzulässigen Bezeichner (*„Die Umstellung ist Handwerk mit eigener Freigabe"*)
— Verweis, dass die Umstellung nach 36.3 erst nach Schritt 2 kommt.

### 36.4 Tatsachennotiz zu 21.4 — die ⚠️-Markierung ohne Erklärung

**Fable, 22b Abschnitt 1 (Kenntnisnahme zu Punkt 1 der Anfrage 22a),
zeichengleich:**

> Die ⚠️-Markierung in 21.4 hat keinen Text. Dann ist sie eine Markierung ohne Bedeutung, und das gehört als Tatsachennotiz zu 21.4: „⚠️ bei `elliott_wave`, Spalte Bestätigung ab, trägt keine Erklärung; nicht als Beleg verwendbar." Sonst nimmt sie in einem Jahr jemand für einen Vorbehalt, den es nie gab.

**Tatsachennotiz zu 21.4 (TB-84, 22.09.2026; Messung `m1_bestaetigung_ab.txt`
aus TB-83, unverändert):** Die Zelle bei `elliott_wave` in der Spalte
„Bestätigung ab" lautet wörtlich `⚠️ **2026-01-01**`; 21.4 trägt keinen Satz,
der die Markierung begründet, und kein anderer Abschnitt des Registers
erklärt sie. **⚠️ bei `elliott_wave`, Spalte Bestätigung ab, trägt keine
Erklärung; nicht als Beleg verwendbar.**

⭐ **Rücknahme des steuernden Chats, eingetragen:** Die Deutung aus
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-21g_berichtigung_und_bestaetigungsperiode.md`
Punkt 3 — zeichengleich: **(Möglicherweise ist das der Grund für die ⚠️-Markierung, die 21.4 ausgerechnet bei `elliott_wave` in der Spalte „Bestätigung ab" trägt.)** — ist **zurückgezogen.** Sie war eine
Vermutung und taugt nicht als Beleg; Fable hatte in 22a ausdrücklich gebeten,
den ganzen Eintrag vorzulegen, bevor jemand sie als Beleg nimmt (35.1). Die
Tabellenzeile in 21.4 bleibt zeichengleich stehen, **samt `⚠️`** — die
Markierung wird nicht entfernt, sondern erklärt: sie erklärt nichts.

**Marke am alten Ort:** ⚠️ **direkt in 21.4**, als Zeile unter der Tabelle —
die Tabellenzeile selbst bleibt zeichengleich, samt `⚠️`.

### 36.5 ⭐⭐ Drei Ausgänge für jede Sonde und jede Wache — Ersteintrag, und die Berichtigung zu 36.2

⚠️ **Fable berichtigt hier seinen eigenen Text aus 22b (36.2), nachdem ihm
`shared/snapshot.py` vorgelegt war (Anfrage 22b, Frage 1; Messung M3).**
*Seine Begründung, 22c Frage 1, zeichengleich:*

> Mein „Rückgabewert ≠ 0" war zu grob, und der Kopf von `snapshot.py` sagt genau, warum: Ein gescheiterter Aufruf und ein Befund sahen in TB-45 gleich aus. A2 verlangt, dass „konnte nicht messen" ein eigenes Ergebnis ist; ein Rückgabewert, der Befund und Nichtprüfbarkeit zusammenlegt, ist keine Wache im Sinn von A8, weil niemand am Wert erkennen kann, ob gemessen wurde.

**Fable, 22c Frage 1, zeichengleich — Registertext und Berichtigung:**

> **Registertext, Ersteintrag — Ausgänge von Sonden und Wachen:**
> Jede Sonde und jede Wache des Verfahrens (Sperrlisten-Sonde, Faltenplan-Sonde nach 33.3, Einmal-Schreibsperre der Erzeuger, Wache nach 29.4, Laufwrapper) endet mit genau einem von drei Rückgabewerten, Bauart `snapshot.py --pruefen`: **0** = geprüft und in Ordnung; **1** = geprüft und **Befund** (Abweichung, Verweigerung, Abbruch nach Regel); **2** = **nicht prüfbar** (Eingabe fehlt, Quelle nicht lesbar, Aufruf gescheitert). Ein Wrapper behandelt 1 und 2 verschieden: 1 ist eine Tatsachennotiz mit dem genannten Punkt; 2 ist kein Ergebnis und darf nirgends als „bestanden" oder „nicht bestanden" geführt werden. Kein Aufruf endet mit 0, ohne dass gemessen wurde.
>
> **Berichtigung zu 22b, Sperrlisten-Sonde:** „mit Rückgabewert ≠ 0 endet und den Punkt nennt" lies „mit Rückgabewert 1 endet und den Punkt nennt; kann ein Punkt nicht geprüft werden (Datei fehlt, Registertext nicht lesbar), endet sie mit 2 und nennt ihn".
>
> > ⚠️ **Präzisiert durch 37.1 (Fable 22d, TB-87, 22.09.2026):** Die Sperrlisten-Sonde meldet **je Punkt je Bestandteil** — für jeden genannten Pfad 0 oder 1, für jeden nicht messbaren Bestandteil 2 unter Nennung des Wortlauts; der Punkt ist 1, wenn ein Bestandteil 1 ist, sonst 2, wenn einer 2 ist, sonst 0. Am Tag: kein Pfad-Bestandteil mit 1, jede 2 mit Tatsachennotiz. Der Text oben bleibt zeichengleich stehen.

**Fables Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* A2 und A8, im Register vorhanden; der Vorfall TB-45, im Kopf von `snapshot.py` dokumentiert. Kein Ergebnis.

**Und sein Zusatz zur Einmal-Schreibsperre (36.1 (2)), zeichengleich:**

> *Zur Einmal-Schreibsperre:* Der Erzeuger, der wegen vorhandener Zieldatei nicht schreibt, endet mit **1** — er hat geprüft und einen Befund („Ziel existiert, Hash …"). Nicht mit 2: Er konnte prüfen. Das ist die Wache, die ihre Arbeit tut; der Wert 1 sagt es dem Aufrufer.

**Tatsachennotiz (TB-84, M3, `m3_snapshot_ausgaenge.txt`):** Die Bauart, auf
die der Registertext verweist, ist im Kopf von `shared/snapshot.py` Z. 217–219
(`0` in Ordnung · `1` Befund · `2` NICHT PRUEFBAR / abgebrochen) mit der
Begründung Z. 221–224 (TB-45: *„wer nicht messen konnte, sagt es mit einem
eigenen Wert"*) — gemessen, nur gelesen. Der Registertext dehnt sie auf **jede**
Sonde und Wache des Verfahrens aus; keine davon ist gebaut (36.7).

**Marken am alten Ort — zwei, beide in diesem Abschnitt:** in **36.2**, direkt
unter dem Registertext, am Satz *„mit Rückgabewert ≠ 0 endet und den Punkt
nennt"* — **berichtigt durch 36.5**, der Satz bleibt zeichengleich stehen; und
in **36.1**, direkt unter dem Registertext, am *„bricht er ab (Rückgabewert
≠ 0)"* in (2) — dasselbe, der Wert ist **1**.

> ⭐ **Wofür die drei Ausgänge gelten, und was seitdem mit 2 endet (42.1 D8/D12,
> 42.2 E5, 42.3 F4, Fable 25a–25c, TB-108, 25.09.2026):** Die drei Ausgänge
> gelten mit „kein Fallback" und der Resolver-Pflicht für den **Laufbereich** —
> die Vereinigung aller registrierten Lauf-Typen, gemessen am Tag-Commit
> (**42.2, E5**). In TB-105 bis TB-107 sind Stellen, die still weiterrechneten
> oder mit 0 endeten, auf 2 umgestellt: unter dem Modus „Keine Daten gefunden"
> (14 Stellen) und eine leere Symbolliste; die stillen Ersatzwerte in
> `faltenplan.py`, `benchmark.py`, `auswertung.py` und `faltenplan_neun.py`;
> `_min_history` bei Fehltreffer (**42.1 D12, 42.3 F4**). Ob
> `auswertung.Abbruch` mit 1 statt 2 endet, ist offen (25d (4), 42.4 G5). Der
> Text oben bleibt zeichengleich.

> ⭐⭐ **Ergänzungen zu 36.5 — Ausgänge von `auswertung.py` und null Trades
> (43.1, 43-1; 43.2, 43-7; Fable 25d/25e, TB-110, 26.09.2026):** Die offene
> Frage in der Marke darüber ist beantwortet: `auswertung.py` endet mit 0 oder
> **2**, nie mit 1 (**43-1**; vollzogen erst mit der nächsten Öffnung von
> `auswertung.py`). Und: ein Lauf des Laufbereichs, der keine Trades findet,
> schreibt dieses Ergebnis und endet mit 0; unter dem Modus endet ein `exit()`
> ohne geschriebenes Ergebnis mit 2 (**43-7**; zehn weitere Stellen in TB-109,
> Gegenprobe über 24). Beide Texte oben bleiben zeichengleich.

> ⭐ **`Abbruch` endet mit 2 seit TB-111, siehe 44.1 (44-1; TB-113,
> 26.09.2026):** Vollzogen in `6c98c38` (Zweig `tb-111`, zusammengeführt in
> `257e7db`): `auswertung.py` endet mit 0 oder 2; die zwölf Stellen und die
> Meldung sind zeichengleich. Die Texte oben bleiben zeichengleich.

> ⭐ **Herkunftsprüfung in `auswertung.py`: siehe 46.5, Lesart 46.9** (Fable
> 27a R14, TB-117, 26.09.2026). Die Texte und die Marken oben bleiben
> zeichengleich.

### 36.6 Das Abbild der Sperrliste ist eine neue Datei — Ersteintrag

**Fable, 22c Frage 2, zeichengleich:**

> **Registertext, Ersteintrag — Abbild der Sperrliste:**
> Das Abbild der Sperrliste ist eine **eigene, neue Datei** (Handwerk: Name, Form), die genau die Punkte des Registerabschnitts 10 mit Pfad und Hash trägt — nicht mehr, nicht weniger (Bauart 33.3). Sie wird einmalig geschrieben (Schreibregel 22b); jede Fortschreibung der Sperrliste vor dem Tag erzeugt ein neues Abbild unter neuem Namen, das alte bleibt. Das aktuelle Abbild steht selbst mit Hash im Register. Die Sperrlisten-Sonde prüft (i) jeden Punkt des Abbilds gegen die Datei im Repo und (ii) das Abbild gegen den Registertext von Abschnitt 10; weicht das Abbild vom Registertext ab, ist das ein Befund (1), kein Anlass zur Anpassung des Abbilds ohne Registereintrag.
>
> `herkunft.py` `EINGEFROREN` (Z. 57) und `SPERRLISTE_DATEIEN` (Z. 66) sind **nicht** das Abbild der Sperrliste und werden nicht dazu. Beide erhalten eine Tatsachennotiz zu Abschnitt 10: Was sie sind, wer sie liest, was daraus entsteht, und dass sie mit dem Registertext an fünf Stellen nicht übereinstimmen (zwei Dateien fehlen, drei stehen zusätzlich).
>
> > ⚠️ **Ergänzt durch 37.2 (Fable 22d, TB-87, 22.09.2026):** Das Abbild führt **zwei Gruppen** — die **Punkte** des Abschnitts 10 und die **bestimmten** Pfade (heute `ergebnisse/benchmark_drawdowns_vt.json`); die Sonde prüft beide gleich und weist die Gruppe aus; am Tag ist die zweite Gruppe leer. Der Satz oben bleibt zeichengleich stehen.
>
> > ⚠️⚠️ **Ergänzt durch 37.3 (Fable 22g, TB-87, 22.09.2026):** „jede Fortschreibung … erzeugt ein neues Abbild unter neuem Namen, das alte bleibt" — ein Befund `1` **vor** dem signierten Tag ist zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz), und wird durch ein **neues** Abbild geschlossen, nie durch Anpassung des alten; **nach** dem Tag ist derselbe Befund ein Sperrlistenbruch nach 10.1. Das letzte Abbild vor dem Tag trägt die Hashes des Tag-Commits. Erster Anwendungsfall: `faltenplan.py` in TB-86 (37.3).
>
> > ⭐ **Ergänzt durch 40.8 (e) (Fable 24a, TB-96, 24.09.2026):** Die Sonde liest **alle drei Gruppen** — die Punkte des Abschnitts 10, die Gruppe „bestimmt" (37.2) und `herkunft.py::EINGEFROREN` (39.7) — **aus dem Abbild**, nicht aus ihrem eigenen Code; „Eine Gruppe, die im Code der Sonde steht, ist ein Literal in einer Wache". Vollzug TB-97, mit Gegenprobe. Der Satz oben bleibt zeichengleich.

**Seine drei Gründe, zeichengleich:**

> *Quelle des Grundes — drei, alle aus dem Bestand:* **(1)** Beide Listen liegen in `herkunft.py`, das mit Punkt 11/12 auf der Sperrliste steht. Ein Abbild, das mit der Sperrliste wachsen muss (Abbild-Datei, Erzeuger, Sonde kommen noch hinzu), kann nicht in einer Datei liegen, die nicht geöffnet werden darf. **(2)** Sie weichen heute vom Registertext ab, und ihr Zweck ist nirgends registriert — eine Liste, von der man nicht weiss, was sie darstellen soll, kann nicht zum Abbild von etwas erklärt werden. **(3)** Der Registertext ist die Quelle (30.2 (2) sinngemäss): Ein Abbild wird aus ihm gebildet und gegen ihn geprüft, nicht aus einer vorhandenen Datei übernommen, weil sie schon da ist. Kein Ergebnis.

**Was der Fund aus 36.2 (c) bedeutet und was nicht — Fable, zeichengleich:**

> **Was der Fund bedeutet, und was er nicht bedeutet:** Der Zustand „maschinenlesbare Fassung weicht vom Registertext ab, und niemand hat sie geprüft" besteht — ihr sagt es richtig — heute schon. Er ist **kein Sperrlistenbruch**: Die Dateien selbst sind unverändert (Hashes stimmen). Er ist eine **Lücke im Nachweis**, wenn `herkunft.py` aus diesen Listen die Hashes bildet, die in `herkunft.json` als Herkunft des Laufs stehen — dann fehlen dort `benchmark_drawdowns_vt.json` und die beiden Universumsdateien, und drei Dateien stehen drin, die kein Sperrlistenpunkt sind. Ob das so ist, weiss ich nicht — **das ist die Messung, die ich brauche:**

⚠️⚠️ **Die Tatsachennotiz zu den zwei Listen (`EINGEFROREN`,
`SPERRLISTE_DATEIEN`), die der Registertext oben verlangt, wird in diesem
Abschnitt NOCH NICHT geschrieben.** Fable hat dafür eine Messung erbeten,
zeichengleich:

> **Nur das Ob:** Welche Funktionen von `herkunft.py` lesen `EINGEFROREN` und `SPERRLISTE_DATEIEN`, und in welche Ausgabe (Datei, Feld) gehen die daraus gebildeten Hashes ein? Läuft `register()` oder `datenstand()` (Punkt 11/12) über diese Listen?

⭐ Die Messung ist am 22.09.2026 vom steuernden Chat gemacht und Fable mit
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-22c_herkunft_gemessen.md` vorgelegt;
**seine Tatsachennotiz folgt** und wird als eigener Eintrag eingetragen.
Eingetragen ist hier nur, **dass** sie aussteht — mit dieser Fundstelle. Die
beiden Listen selbst bleiben unberührt: `herkunft.py` steht auf der Sperrliste
(Punkte 11, 12), und ob es vor dem Tag geöffnet werden muss, entscheidet Fable
nach der Messung — 22c, zeichengleich:
„**Meine Linie dazu, vorab und nicht als Entscheidung:** Nach 21b (3) nicht öffnen, wenn die Sperrlisten-Sonde die Lücke schliesst".

**Fables Unsicherheit, 22c, zeichengleich:**

> **Unsicher:** ob Abschnitt 10 in einer Form vorliegt, aus der ein Programm Pfad und Hash je Punkt zuverlässig lesen kann (Prüfung (ii) der Sonde). Wenn nicht, ist der Abgleich Abbild↔Registertext eine Prüfung mit Beleg im Auftrag statt einer Codezeile — Handwerk, aber ihr müsst es wissen, bevor ihr die Sonde beauftragt.

⚠️ Auch dazu liegt Fable eine Messung vor (Anfrage 22c Abschnitt 3,
`docs/projektfuehrung/VORARBEIT_sperrlisten_sonde.md`, lesend, HEAD `fdb181a`);
sie ist hier **nicht** eingetragen — sie gehört zur ausstehenden Antwort.

**Marke am alten Ort:** unter der **Überschrift von Abschnitt 10**, zusammen
mit der Marke aus 36.2.

### 36.7 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Sperrlisten-Sonde schreiben** (Schritt 1 in 36.3) — keine Freigabe; ihre Ausgänge sind seit 36.5 festgelegt, ihr Gegenstand (das Abbild) seit 36.6 | Betreiber |
| ⛔ | **`faltenplan.py main()` absichern** — Voreinstellung, Einmal-Schreibsperre (Ausgang 1 nach 36.5), Mutationsprobe (Schritt 2) — keine Freigabe | Betreiber |
| ⛔ | **`faltenplan.py:336` umstellen** (Schritt 3) — nach 36.1 (4) und 36.3 **erst nach Schritt 2** | Betreiber, nach Schritt 2 |
| ⛔ | **Abbild-Datei der Sperrliste (36.6), Abbild des Faltenplans, Faltenplan-Sonde (33.3), Hash auf die Sperrliste** (Schritt 4) | eigene Aufgabe, Betreiberfreigabe (33.5) |
| ⛔ | ⚠️⚠️ **`python3 faltenplan.py` ausführen** — in dieser Sitzung **nicht geschehen**; der Hash von `ergebnisse/faltenplan.json` ist vor **und** nach der Arbeit `0e54ac5c…` (`m2_sperrlisten_hash.txt`). Ein Hashbruch wäre nach 36.2 eine Tatsachennotiz, nie eine stille Reparatur | — |
| ⛔ | **`herkunft.py` anfassen** — auch nicht die beiden Listen aus 36.2 (c); die Datei steht selbst auf der Sperrliste (Punkte 11, 12) | Fable (Tatsachennotiz), dann Betreiber |
| ⛔ | **Die Tatsachennotiz zu `EINGEFROREN` und `SPERRLISTE_DATEIEN` schreiben** (36.6) — nur eingetragen, dass sie aussteht | Fable (Anfrage 22c) |
| ⛔ | **Irgendeine `.py` ändern** | — |
| ⭐ | **Keine Zahl bewegt:** Faltenliste 33.2 vor und nach dem Eintrag zeichengleich (Beleg M6); die drei Sperrlisten-Hashes `0e54ac5c…`, `a163c498…`, `4549395f…` unverändert | — |
| ⚠️ | **Offen bei Fable:** die Tatsachennotiz zu den zwei Listen (36.6); die Frage der Anfrage 22c, ob die Sonde auch Pfade prüft, die für die Sperrliste **bestimmt** sind (`benchmark_drawdowns_vt.json`, 21.9/23.7 — von 36.1 (1) gedeckt, vom Wortlaut in 36.2 „für jeden Sperrlistenpunkt" nicht); seine Unsicherheit aus 22c, ob Abschnitt 10 maschinenlesbar ist (Messung vorgelegt); seine Unsicherheit aus 35.5 (weitere Fundstellen des Bezeichners, in Anfrage 22a Punkt 2 gemessen) | Fable |
| ⚠️ | **Offen beim Betreiber:** die Freigabe für die vier Schritte aus 36.3 — keine erteilt | Betreiber |

*Dieser Abschnitt ist rein additiv: Er trägt vier Ersteinträge, eine
Reihenfolge und eine Tatsachennotiz des Verfahrensprüfers zeichengleich ein,
darunter eine Berichtigung, die er am selben Tag an seinem eigenen Text
vorgenommen hat; setzt sechs Marken am alten Ort; hält drei nachgemessene
Tatsachen zum Bestand und das Ausstehende fest — und entfernt nichts. Gebaut
wird nichts.*

## 37. Die Sonde meldet je Bestandteil, das Abbild führt zwei Gruppen, was ein Befund `1` bedeutet, hängt vom Tag ab, die Tatsachennotiz zu den zwei Listen in `herkunft.py` und der Ort registrierter Werte (Fable 22d und 22g, TB-87, 22.09.2026)

⭐ **Reines Eintragen von Registertext**, wie 34 bis 36. Fünf Einträge — zwei
Präzisierungen bzw. Ergänzungen zu 36.5 und 36.6 (37.1, 37.2), eine Ergänzung
zu 36.2/36.6 (37.3), eine Tatsachennotiz zu Abschnitt 10 (37.4) und ein
Ersteintrag (37.5) —, alle Fable-Texte zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22d_wert_ohne_ort.md` (Antwort auf
die Anfragen 22c und 22d) und
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22g_sonde_vor_dem_tag.md` (Antwort
auf die Meldung des steuernden Chats zu TB-86 und zum Sondenbefund an
Sperrlistenpunkt 2). Auftrag `docs/auftraege/MAC_TB-87_register_37.md` (Stufe I,
Punkt 4 aus `PLAN_VOR_DEM_TAG.md`); Messungen `docs/belege/TB-87/` (M1–M6),
M1–M4 **vor** dem Eintrag gemessen, HEAD `40aa715`. ⛔ **Keine `.py` geändert,
kein neues Abbild, keine Sonde angepasst, keine Werte verschoben** — 37.6.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (36.5; 36.6 zweimal;
36.2; Überschrift von Abschnitt 10; Sperrlistenpunkte 7 und 9). Die alten Sätze
bleiben zeichengleich; `git diff --numstat` auf dieses Register zeigt für TB-87
in der zweiten Spalte `0`. ⚠️ Die Marken in Abschnitt 10 stehen als eingerückte
`>`-Zeilen **ohne Leerzeile** unter dem Punkt — so liest die Sperrlisten-Sonde
sie als Notiz und nicht als Punkttext (`shared/sperrlistensonde.py`
`lies_abschnitt_10`, R2); die Sonde ist vor und nach dem Eintrag lesend
gelaufen, Prüfung (ii) beide Male `0`, Listentext wie bei Erzeugung (37.6).

⚠️ **Die Fable-Texte stehen hier in voller Quellform**, auch wo der Auftrag sie
gekürzt zitiert (der Zusatz „, Vorschlag" in den Kopfzeilen von 22d Abschnitt 1
und 22g; „Folge für `herkunft.py`, Entscheidung:"; zwei Begründungen mit „…"):
Eingetragen wird der Quellwortlaut, nicht die Kurzform.

### 37.1 Präzisierung zu 36.5 — die Sonde meldet je Punkt je Bestandteil

**Fable, 22d Abschnitt 1, zeichengleich:**

> **Präzisierung zu 36.5 (Sonden-Ausgänge), Vorschlag:** Die Sperrlisten-Sonde meldet **je Punkt je Bestandteil**: für jeden genannten Pfad 0 oder 1 (Hash gegen Abbild), für jeden nicht messbaren Bestandteil 2 unter Nennung des Wortlauts. Der Gesamtwert eines Punktes ist 1, wenn ein Bestandteil 1 ist; sonst 2, wenn ein Bestandteil 2 ist; sonst 0. Der Gesamtwert des Laufs entsprechend. Am Tag gilt: Kein Pfad-Bestandteil darf 1 sein, und jeder Bestandteil mit 2 hat eine Tatsachennotiz, die sagt, wie er stattdessen geprüft wurde (Lesen, Beleg im Auftrag) — oder der Punkt wird bis zum Tag so nachgetragen, dass er messbar ist.

**Fables Grund, 22d Abschnitt 1, zeichengleich:**

> **Eine Präzisierung zur Sonde, damit die `2` nicht mehr verdeckt als sie zeigt:** Ein Punkt wie 14 („`auswertung.py` … Docstring") hat einen messbaren Teil (der Datei-Hash) und einen unmessbaren (der Docstring-Anteil). Eine Sonde, die den ganzen Punkt mit `2` meldet, macht den messbaren Teil unsichtbar.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* A2 (nicht prüfbar ist ein eigenes Ergebnis — aber je Sache, nicht je Punkt) und 22c. Kein Ergebnis.

**Tatsachennotiz (TB-87, M1, `m1_sonde_je_bestandteil.txt`):** Die Sonde aus
TB-85 (`shared/sperrlistensonde.py`) **gibt bereits je Bestandteil aus** — im
Nullpunkt-Lauf `docs/belege/TB-85/nullpunkt.txt` zeigt Punkt 1 in einer Zeile
den Datei-Hash (`research/vorregistrierung/registerdaten.py`, `gleich`,
`141fa14b…`) und in der nächsten daneben den unmessbaren Teil (`-> nennt
Nicht-Dateibezogenes - nicht messbar: …`). ⚠️ **Was ihr fehlt, ist der
Rückgabewert je Bestandteil:** Sie meldet den Ausgang je Punkt (Punkt 1 steht
auf `2 NICHT PRUEFBAR`, obwohl sein einziger Pfad `gleich` ist) und einmal je
Lauf. Genau das ist der Fall, den Fables Grund beschreibt — der messbare Teil
verschwindet im Ausgang hinter dem unmessbaren. Das nachzuziehen ist Handwerk
mit eigener Freigabe, **nicht** dieser Eintrag.

**Marke am alten Ort:** in **36.5**, direkt unter dem Registertext.

### 37.2 Ergänzung zu 36.6 — das Abbild führt zwei Gruppen

**Fable, 22d Abschnitt 2, zeichengleich:**

> **Ergänzung zu 36.6 (Abbild der Sperrliste):** Das Abbild führt zwei Gruppen: die **Punkte** des Abschnitts 10 und die **bestimmten** Pfade — Dateien, die das Register für die Sperrliste vorsieht, deren Vollzug aber aussteht (heute: `ergebnisse/benchmark_drawdowns_vt.json`, 21.9/23.7). Die Sonde prüft beide Gruppen gleich (Hash gegen Abbild) und weist die Gruppe im Bericht aus. **Am Tag ist die zweite Gruppe leer:** Jeder bestimmte Pfad hat bis dahin seinen Punkt in Abschnitt 10, oder das Register sagt, warum nicht.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* Schreibregel 22b (1) („oder für sie bestimmt ist") — was die Schreibregel schützt, muss die Sonde sehen; sonst ist der Schutz eine Regel ohne Wache (A8). Und die Sperrliste ist am Tag vollständig oder sie ist keine. Kein Ergebnis.

**Tatsachennotiz (TB-87, M1):** Das Abbild `sperrliste_abbild_2026-09-22.json`
(`6a1b732e…`) führt heute die Punkte; die Sonde **nennt** den bestimmten Pfad
`ergebnisse/benchmark_drawdowns_vt.json` am Ende ihres Berichts mit Hash
`4549395f…`, **prüft ihn aber nicht** — ihr eigener Wortlaut: „Bestimmt, nicht
eingetragen (kein Punkt des Abschnitts 10; nicht geprueft, nur genannt)".
Der Unterschied zum Registertext oben (beide Gruppen gleich prüfen, Gruppe
ausweisen) ist Handwerk mit eigener Freigabe; hier nur festgehalten.

> ⭐ **Gruppenwechsel und Vollzug (39.3/39.2, Fable 23a/23b, TB-94,
> 23.09.2026):** Die Gruppe „bestimmt" **wechselt** von
> `ergebnisse/benchmark_drawdowns_vt.json` auf die Neurechnung
> `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (`64fb2912…`) —
> und deren Pfad steht seit 39.2 in Sperrlistenpunkt 4. **Nach dem
> Registertext ist die Gruppe damit leer.** `_vt.json` und `_tb72.json` kommen
> nicht auf die Liste (Tatsachennotizen in 39.3). ⚠️ Die Sonde führt die
> Gruppe als feste Konstante und nennt weiter `_vt.json` mit „Vollzug steht
> aus" (39.3, Ausgabe in 39.9); das zu ändern ist Handwerk mit eigener
> Freigabe.

> ⭐ **Die Gruppen kommen aus dem Abbild (40.8 (e), Fable 24a, TB-96,
> 24.09.2026):** Dass die Sonde die Gruppe „bestimmt" als feste Konstante führt
> (`BESTIMMT_NICHT_EINGETRAGEN`), ist nach Fable „ein Befund, vor dem Tag zu beheben"
> — nicht mehr Handwerk ohne Frist. Die Sonde liest alle drei Gruppen aus dem
> Abbild; das Abbild führt „bestimmt" heute leer (39.3). Gegenprobe: Abbild mit
> erfundenem „bestimmt"-Pfad ⇒ Sonde meldet ihn. TB-97.

**Marke am alten Ort:** in **36.6**, direkt unter dem Registertext.

### 37.3 ⭐⭐ Ergänzung zu 36.2/36.6 — was ein Befund `1` bedeutet, hängt vom Tag ab

⚠️ **Das ist die Lücke, die TB-86 sichtbar gemacht hat:** Die Sonde meldet
seit TB-86 an Sperrlistenpunkt 2 den Befund `1` — und bis hier stand nirgends,
ob das ein Sperrlistenbruch ist.

**Fable, 22g, zeichengleich:**

> **Ergänzung zu 36.2/36.6, Vorschlag:** Ein Befund 1 der Sperrlisten-Sonde **vor dem signierten Tag** ist zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz); er wird durch ein **neues Abbild unter neuem Namen** geschlossen, nie durch Anpassung des alten. Ein Befund 1 **nach dem Tag** ist ein Sperrlistenbruch und wird nach 10.1 behandelt (Amendment, Lauf von vorn). Das **letzte Abbild vor dem Tag** wird nach der letzten Codeänderung erzeugt, trägt die Hashes des Tag-Commits und steht selbst mit Hash im Register; der Tag setzt voraus, dass die Sonde gegen dieses Abbild 0 liefert (oder 2 mit Tatsachennotiz nach 22d).

**Fables Grund, 22g, zeichengleich:**

> **Der Satz, der fehlt — und den der Befund verlangt:** Die Sperrliste sagt „**ab dem signierten Tag** sind unveränderlich". Vor dem Tag ändern sich Sperrlistenpfade planmässig (TB-86 heute, Z. 336 morgen, die Werte-Module nach 22d). Die Sonde kann diesen Unterschied nicht kennen; sie meldet 1, und was 1 **bedeutet**, hängt vom Datum ab. Das gehört ins Register, sonst liest jemand den heutigen Befund als Bruch — oder, schlimmer, einen Bruch nach dem Tag als „planmässig".

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* der Wortlaut von Abschnitt 10 („ab dem signierten Tag") und 36.6 (Abbild einmalig, neu statt angepasst). Kein Ergebnis.

⭐ **Und sein Satz zur Sonde, 22g, zeichengleich:**

> *„Eine Sonde, die den neuen Hash von selbst übernähme, wäre keine Sonde."*

(Aus 22g, Absatz „Punkt 2b — ja, genauso", voller Absatz:)

> **Punkt 2b — ja, genauso:** Sperrlistenpunkt 2 nennt zwei Pfade; `faltenplan.py` hat sich durch beauftragte Änderung bewegt; die Sonde meldet 1 und repariert nichts — richtig, denn das Abbild trägt den alten Hash, und ein Abbild wird nach 36.6 nicht angepasst, sondern **neu** geschrieben, unter neuem Namen, das alte bleibt. Eine Sonde, die den neuen Hash von selbst übernähme, wäre keine Sonde.

**Sein Hinweis zum Handwerk, ausdrücklich nicht Verfahren, zeichengleich:**

> *Handwerk daraus, nicht Verfahren:* Nicht nach jeder Änderung ein neues Abbild ziehen, sondern nach Bündeln (etwa nach 2+3 zusammen, nach 6, vor 11) — jedes Abbild bleibt ohnehin liegen. Wie viele es werden, ist gleichgültig; dass das letzte zum Tag-Commit passt, ist alles.

⭐⭐ **Tatsachennotiz — der erste Anwendungsfall (TB-87, M2,
`m2_faltenplan_hash.txt`):** TB-86 hat `research/vorregistrierung/faltenplan.py`
**beauftragt und freigegeben** geändert — Auftrag
`docs/auftraege/MAC_TB-86_faltenplan_schreibsperre.md`, Betreiberfreigabe
22.09.2026, 07:50 (Schritt 1 und 2 aus 36.3), Commit `4daa254`. Der Hash ging
von **`6f96b95d13563f73b11be69c2bd6996037854df794da61315029216ad0b22bd9`** (so im
Abbild `sperrliste_abbild_2026-09-22.json`, `6a1b732e…`, Punkt 2) auf
**`fd3e5018ae930c2e29747562a140506d5d9a6bb70b87e96cf5c0089e09afdd79`** (heute,
gemessen). Die Sonde meldet seither an Punkt 2 **`1 BEFUND`**, Lauf gesamt `1`
(`docs/belege/TB-86/schritt8_sonde.txt`; lesend wiederholt vor diesem Eintrag,
`docs/belege/TB-87/sonde_vorher.txt`). ⭐ **Nach dem Registertext oben ist das
der planmässige Fall vor dem Tag** — Auftrag, Freigabe, alter und neuer Hash
stehen hiermit als Tatsachennotiz. **Geschlossen wird er mit einem neuen Abbild
unter neuem Namen** (Plan Punkt 2b); das ist **nicht** Gegenstand dieses
Eintrags, und das alte Abbild bleibt.

> ⭐⭐ **Die weiteren Übergänge und ihr Abbild (39.5/39.9, TB-94,
> 23.09.2026):** Nach TB-86 haben sich planmässig bewegt: `faltenplan.py`
> `fd3e5018…` → `7aa0b8cc…` (TB-90, `303a7fd`, Punkt 2), `benchmark.py`
> `3960375a…` → `d6bdd558…` (TB-91, `31008b6`, Punkte 4 und 6),
> `auswertung.py` `1c2e2dae…` → `c3b4e69d…` (TB-92, `0292e92`, Punkte 3, 5
> und 14); dazu `registerbericht.py` und `test_vorregistrierung.py` (TB-92,
> auf keinem Punkt). Auftrag, Freigabe und volle Hashes stehen in **39.5**.
> Geschlossen werden der Fall oben und diese Übergänge mit **einem** neuen
> Abbild (**39.9**); `sperrliste_abbild_2026-09-22.json` bleibt.

> ⭐⭐ **Die Übergänge seit 39.5 und ihre Abbilder (42.5, TB-108, 25.09.2026):**
> Planmässig bewegt haben sich `messgroessen.py` (TB-103, `EINGEFROREN`),
> `benchmark.py` und `faltenplan.py` (TB-104 und TB-106, Punkte 2, 4, 6),
> `auswertung.py` (TB-106, Punkte 3, 5, 14) und `herkunft.py` (TB-106, Punkte 11
> und 12). Auftrag, Freigabe und volle Hashes stehen in **42.5**. Geschlossen
> durch `sperrliste_abbild_2026-09-25.json` (`cb4eb1b4…`, TB-104) und
> `sperrliste_abbild_2026-09-25b.json` (`40ffe18d…`, TB-106); die älteren
> Abbilder bleiben.

**Marken am alten Ort — zwei:** in **36.2**, direkt unter dem Registertext
(unter der Marke aus 36.5), und in **36.6**, direkt unter dem Registertext
(unter der Marke aus 37.2).

### 37.4 Tatsachennotiz zu Abschnitt 10 — die zwei Listen in `herkunft.py`

⭐ Das ist die Tatsachennotiz, die 36.6 als **ausstehend** eingetragen hat
(„wird in diesem Abschnitt NOCH NICHT geschrieben"). **Fables eigene
Tatsachennotiz, 22d Abschnitt 3, zeichengleich:**

> **Tatsachennotiz zu Abschnitt 10 (22.09.2026):** `research/vorregistrierung/herkunft.py` trägt zwei Listen. **`EINGEFROREN`** (Z. 57, zehn Einträge) ist die Eingabe von `register()` (Z. 114): ein Gesamthash über die Registerdatei plus diese zehn Dateien, laut Docstring „über die eingefrorenen Festlegungen" — sie bildet die Menge aus **Abschnitt 0** ab, nicht die Sperrliste aus Abschnitt 10, und weicht von dieser an fünf Stellen ab (fehlend: `benchmark_drawdowns_vt.json`, `config/top25_symbols.txt`, `config/sp500_top150.txt`; zusätzlich: `kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`). **`SPERRLISTE_DATEIEN`** (Z. 66) wird von keiner Stelle gelesen — toter Code. Keine der beiden Listen ist das Abbild der Sperrliste (36.6). `herkunft.py` wird in `research/vorregistrierung/` von keinem Modul importiert; `herkunft.json` und `herkunft_protokoll.jsonl` existieren nicht; die einzigen Aufrufer von `block()` gehören zu `research/turn_of_month/`. Sperrlistenpunkte 11 und 12 verweisen damit auf Funktionen, die im Laufbereich heute niemand aufruft; der Datenvertrag (`auswertung.py` Z. 41) verlangt `herkunft.json` als Pflichteingabe. Der Erzeuger (Nachtrag 2) ist die Stelle, an der `register()` und `datenstand()` erstmals aufgerufen werden.

> ⚠️ **ERSETZT (38.6, Fable 22h, TB-89, 23.09.2026) — zwei Stellen dieses
> Satzes, der Satz selbst bleibt zeichengleich:** (a) „`auswertung.py` Z. 41"
> lies **Z. 51** (Fables Berichtigung (a)). (b) Der Halbsatz „weicht von dieser
> an fünf Stellen ab (fehlend: …; zusätzlich: …)" ist ersetzt durch Fables
> Ersatzsatz — acht Stellen, vier fehlend und vier zusätzlich; der Wortlaut
> steht zeichengleich in **38.6**. Beleg ist die Tatsachennotiz TB-87 (M3)
> unten.

**Und seine Entscheidung dazu, zeichengleich:**

> **Folge für `herkunft.py`, Entscheidung:** **Nicht öffnen.** Der Erzeuger ruft `register()` auf und schreibt in `herkunft.json` **auch das Feld `teile`** (das `register()` liefert und `block()` weglässt) — dann ist lesbar, welche Dateien in den Gesamthash eingingen, ohne dass `block()` oder `herkunft.py` geändert wird. `herkunft.json` bezeugt damit die Abschnitt-0-Menge (zehn Dateien plus Register); die Sperrlisten-Sonde bezeugt Abschnitt 10; die Tatsachennotiz oben sagt, welches Dokument was bezeugt. Zwei Nachweise mit verschiedenem Gegenstand sind kein Widerspruch — zwei Nachweise mit demselben Gegenstand und verschiedenem Inhalt wären einer. *Quelle des Grundes:* 21b (3), Einfrieren vor Umbau; der Erzeuger ist neuer Code, dort darf alles stehen. Kein Ergebnis.

> ⭐⭐ **BERICHTIGT durch 42.3 F2 (Fable 25c, TB-108, 25.09.2026):** `herkunft.py`
> ist **einmal planmässig geöffnet** worden (TB-106, `5791b4c`), um
> `datenstand()` den Datenpfad durch `block()` und `anhaengen()` durchzureichen;
> sonst gilt die Entscheidung oben: `EINGEFROREN` bleibt, `register()` bezeugt
> die Abschnitt-0-Menge, die Sonde Abschnitt 10. **Planmässig geöffnet heisst
> nicht offen.** Hash `56a1c2e1…` → `351f24c2…` (42.5). Die Entscheidung oben
> bleibt zeichengleich.

> ⭐ **Zweite planmässige Öffnung geplant (43.1, 43-4, Fable 25d, TB-110,
> 26.09.2026):** `herkunft.py` wird ein zweites Mal geöffnet, für zwei Dinge in
> **einer** Öffnung — die Prüfansicht übergibt unter dem Modus
> `paths.DATA_DIR`, und `TB30A_BASE_DIR` endet unter dem Modus mit 2, bevor
> gelesen wird —, mit dem Erzeuger oder vor ihm. **Noch nicht vollzogen**
> (`351f24c2…` unverändert). Die Entscheidung oben und ihre Berichtigung
> bleiben zeichengleich.

> ⭐ **Zweite Öffnung `herkunft.py` vollzogen, TB-111, siehe 44.1 (44-2;
> TB-113, 26.09.2026):** In `6cacfa4` (zusammengeführt in `257e7db`): die
> Prüfansicht übergibt unter dem Modus `paths.DATA_DIR`, `TB30A_BASE_DIR`
> endet unter dem Modus mit 2 vor dem Lesen, `paths.py` kommt aus der eigenen
> Wurzel. `351f24c2…` ⇒ `5bbfc9e0…`. `EINGEFROREN` bleibt; die Entscheidung
> oben, ihre Berichtigung und die Marke darüber bleiben zeichengleich.

**Tatsachennotiz (TB-87, M3, `m3_herkunft_listen.txt`) — nachgemessen, nicht
übernommen:**

| Aussage in Fables Notiz | gemessen | |
|---|---|---|
| `EINGEFROREN` Z. 57, zehn Einträge | **Z. 57**, zehn Einträge | ✔ |
| `SPERRLISTE_DATEIEN` Z. 66, von keiner Stelle gelesen | **Z. 66**, fünf Muster; ausser der Definition nur in einem **Kommentar** von `shared/sperrlistensonde.py:70` genannt, nirgends gelesen | ✔ |
| Eingabe von `register()` (Z. 114) | **Z. 114** `for rel in ([…REGISTERDATEI…] + EINGEFROREN):` | ✔ |
| `herkunft.py` in `research/vorregistrierung/` von keinem Modul importiert | **0** `import`/`from`; zwei Textfundstellen (Docstring `auswertung.py`, Beispieldaten-Schreiber `beispieldaten.py:142/145`) | ✔ |
| `herkunft.json`, `herkunft_protokoll.jsonl` existieren nicht | **existieren nicht** | ✔ |
| einzige Aufrufer von `block()` in `research/turn_of_month/` | **`auswertung.py:206`, `staging.py:127`**, beide dort | ✔ |
| Datenvertrag `auswertung.py` **Z. 41** | ⚠️ **Z. 51** (`<wurzel>/<bot>/herkunft.json`), Z. 52 „siehe herkunft.py"; Z. 41 ist `mittlere_exposure` | **abweichend** |
| „weicht … an **fünf** Stellen ab (fehlend: drei; zusätzlich: drei)" | ⚠️ siehe unten | **abweichend** |

⚠️ **Die Abweichungszahl, gemessen:** Fable schreibt „fünf Stellen" und nennt
sechs Namen. Der mechanische Mengenvergleich der zehn `EINGEFROREN`-Einträge
(auf Repo-Pfade aufgelöst) gegen die zehn Pfade der vierzehn Punkte (aus dem
Abbild `6a1b732e…`, das die Sonde mit Prüfung (ii) `0` gegen Abschnitt 10 prüft)
ergibt:

- **in Abschnitt 10, nicht in `EINGEFROREN` — vier:** `config/top25_symbols.txt`,
  `config/sp500_top150.txt`, `research/vorregistrierung/herkunft.py` (Punkte 11,
  12), `shared/zuteilung.py` (Punkt 10); **dazu** der bestimmte Pfad
  `ergebnisse/benchmark_drawdowns_vt.json` (kein Punkt, 37.2);
- **in `EINGEFROREN`, kein Pfad eines Punktes — vier:** `kennzahlen.py`,
  `messgroessen.py`, `pruefe_grenzsaetze.py` **und**
  `ergebnisse/messgroessen.json`.

Alle sechs Namen in Fables Notiz stimmen; **nicht genannt** sind dort
`herkunft.py`, `shared/zuteilung.py` und `ergebnisse/messgroessen.json`. Das
ändert seine Folgerung nicht — `EINGEFROREN` bildet die Abschnitt-0-Menge ab,
nicht Abschnitt 10 —, aber die Zahl „fünf" gilt so nicht; **eingetragen ist,
was gemessen ist**, Fables Satz bleibt zeichengleich stehen. Gemeldet im
Ergebnisdokument.

**Randbefund aus TB-84, nachgemessen:** `research/etf_trendfolge/datenstand.py`
Z. 43–49 lädt `research/vorregistrierung/herkunft.py` über
`reg.lade_fremdes_modul(…)` und ruft `herkunft.datenstand(…)` auf — ein Nutzer
ausserhalb von `turn_of_month/` und ausserhalb des Laufbereichs der
Vorregistrierung. Fables Satz über den **Laufbereich** bleibt damit richtig;
vollständig beantwortet „wer liest `herkunft.py`" er nicht.

> ⚠️ **Ergänzung (39.7, Fable 23d, TB-94, 23.09.2026) — `EINGEFROREN` ist nach
> dem Vollzug nicht vollständig:** `EINGEFROREN` hasht weiter
> `ergebnisse/benchmark_drawdowns.json` (historischer Stand), **nicht** die
> Tabelle, die der Lauf liest (`ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json`,
> 39.2). `herkunft.py` bleibt ungeöffnet (`56a1c2e1…`). Der Satz, um den Fable
> diese Tatsachennotiz ergänzt (23d Abschnitt 1 (2)), zeichengleich:
> „`register()` bezeugt die Abschnitt-0-Menge vom 14.09.; die vollzogene Benchmark-Tabelle bezeugt Sperrlistenpunkt 4 über die Sonde."
> Nach Fables Präzisierung zu 36.1 (1) (23c) ist auch jeder Pfad in
> `EINGEFROREN` gesperrt — Wortlaut in **39.7**.

**Marke am alten Ort:** unter der **Überschrift von Abschnitt 10**, unter dem
Hinweis aus 36.2/36.6 (der „ihre Tatsachennotiz steht bei Fable aus" sagt —
bleibt zeichengleich stehen).

### 37.5 Registertext „Ort registrierter Werte" — Ersteintrag

**Fable, 22d Abschnitt 4, zeichengleich:**

> **Registertext, Ersteintrag — Ort registrierter Werte:**
> **(1)** Jeder Sperrlistenpunkt, der einen Zahlenwert registriert (heute 7 und 9), nennt **genau ein** Modul und dort **genau eine** Konstante, aus der der Lauf diesen Wert liest. Dieses Modul steht mit Hash auf der Sperrliste; die Sonde prüft für den Punkt Datei-Hash **und** Wert der Konstante (Bauart „Datei plus Konstante", wie Punkte 3, 4, 10).
> **(2)** Der Laufpfad (Optimierer, Equity-Simulation, Erzeuger) liest registrierte Werte ausschliesslich aus diesem Modul — kein Laufmodul trägt eine eigene Kopie. Für den Papierpfad (`forward_test.py`) gilt das nicht als Sperre, aber als Konsistenzprüfung: Die Sonde meldet als Befund, wenn eine Kopie dort vom registrierten Wert abweicht.
> **(3)** Für Punkt 9: `TRADING_FEE_PCT` und `SLIPPAGE_PCT` in einem Modul; für Punkt 7: `CLUSTER_SCHWELLE` und `N_HISTORISCH_JE_BOT` in einem Modul. Welche Module (Kandidaten nach heutiger Messung: `messgroessen.py` für 9, `registerdaten.py` für 7) und ob eines der beiden Module bereits Abschnitt-0-eingefroren ist und deshalb ein neues kleines Modul die Werte tragen muss — **Handwerk mit Freigabe**, aber die Tatsachennotiz zu 7 und 9 nennt am Ende Modul, Zeile und Wert.
> **(4)** Tatsachennotiz zu 7 und 9, jetzt: die heute gemessenen Orte (neun `forward_test.py`; `messgroessen.py:59`; `registerdaten.py:99`, `:115`) mit dem Vermerk, dass der Registertext keinen davon nennt und der Zustand bis zur Umsetzung von (1)–(3) ungeschützt war.

> ⭐⭐ **Entscheidung zu (2) und (3) (38.5, Fable 22h, TB-89, 23.09.2026):** Es
> bleibt bei (2) — **kein Laufmodul trägt eine eigene Kopie.** Die neun
> `backtest_*.py` beziehen `TRADING_FEE_PCT` / `SLIPPAGE_PCT` künftig per
> Import aus einem **neuen** Modul (die Kandidaten aus (3) sind blockiert); der
> Papierpfad und `messgroessen.py` / `GEBUEHR_PCT` bleiben überwachte Kopien.
> **Für Punkt 7 ist (3) schon erfüllt:** `registerdaten.py` ist der Ort, nichts
> wird verschoben. Wortlaut und Begründung in **38.5**.

**Fables Befund, aus dem der Eintrag folgt, zeichengleich** (darin sein
Kernsatz *„Ein Sperrlistenpunkt, der einen Wert nennt und keinen Ort, sperrt
nichts — er legt fest."*):

> **Der Befund in einem Satz:** Ein Sperrlistenpunkt, der einen Wert nennt und keinen Ort, sperrt nichts — er legt fest. Festlegen ist Aufgabe der Festlegungen und des Registertexts; die Sperrliste soll sagen, **was unverändert bleibt**, und das ist immer eine Datei (oder ein Ort in einer). „Ändert jemand `TRADING_FEE_PCT` in einer der neun `forward_test.py`, merkt es kein Sperrlistenpunkt" ist genau der Zustand, den der Tag ausschliessen soll.

**Seine Abwägung der drei Wege, zeichengleich:**

> **Zu den drei Wegen:** *(iii) so lassen und Notiz* — nein: eine Tatsachennotiz macht eine Lücke sichtbar, sie schliesst sie nicht; der Tag friert dann eine Sperrliste ein, von der man weiss, dass sie zwei Werte nicht schützt. *(i) Ort je Punkt nachtragen* allein — nicht ausreichend, denn der Ort, den man heute misst (neun `forward_test.py`), ist nicht notwendig der Ort, aus dem der **Lauf** den Wert liest: `forward_test.py` ist der Papierpfad; die Optimierer und der noch zu schreibende Erzeuger sind der Laufpfad. Neun Kopien eines Werts als Sperrlistenorte einzutragen registriert die Kopien, nicht die Quelle. *(ii) Werte in eine Datei ziehen und sperren* — das ist der Kern, aber „ziehen" darf keine Kopie mehr erzeugen.

**Seine Quelle des Grundes — und der Satz, der Missverständnisse ausschliesst,
zeichengleich:**

> *Quelle des Grundes:* Zweck der Sperrliste (Übergabe Abschnitt 5) und A8; der Grundsatz ein Wert, ein Ort aus 21j. **Kein Ergebnis — und das ist hier wichtig zu sagen:** Die Werte selbst (0,1 / 0,05 / die beiden aus Punkt 7) ändern sich nicht um ein Zeichen; es ändert sich nur, wo sie stehen und dass jemand es merkt, wenn sie sich ändern.

**Tatsachennotiz zu Punkt 7 und 9 nach (4) (TB-87, M4, `m4_werte_orte.txt`) —
die heute gemessenen Orte:**

| Wert (Punkt) | Ort | Zeile | Wert im Code |
|---|---|---|---|
| `TRADING_FEE_PCT` (9) | neun `strategies/*/forward_test.py` | je eine Zuweisung (Z. 57–72) | `0.1` |
| `SLIPPAGE_PCT` (9) | neun `strategies/*/forward_test.py` | je eine Zuweisung (Z. 58–73) | `0.05` |
| `SLIPPAGE_PCT` (9) | `research/vorregistrierung/messgroessen.py` | **:59** | `0.05` |
| ⚠️ Gebühr (9) | `research/vorregistrierung/messgroessen.py` | **:58**, Name **`GEBUEHR_PCT`** — nicht `TRADING_FEE_PCT` | `0.1` |
| `CLUSTER_SCHWELLE` (7) | `research/vorregistrierung/registerdaten.py` | **:99** | `0.90` |
| `N_HISTORISCH_JE_BOT` (7) | `research/vorregistrierung/registerdaten.py` | **:115** (neun Einträge bis Z. 125, Summe 653) | Wörterbuch |

⚠️ **Zwei Abweichungen von Fables (4), gemessen:** (a) `messgroessen.py:59`
trägt nur `SLIPPAGE_PCT`; die Gebühr steht eine Zeile davor unter **anderem
Namen** (`GEBUEHR_PCT`) — für (3) heisst das: in `messgroessen.py` gibt es heute
**keine** Konstante `TRADING_FEE_PCT`. (b) **Nicht genannt, aber gemessen:**
Auch die neun `backtest_*.py` der Bots tragen je eine eigene Zuweisung
`TRADING_FEE_PCT = 0.1` / `SLIPPAGE_PCT = 0.05`
(`elliott_wave/backtest_elliott.py:73–74`,
`elliott_wave_stocks/backtest_elliott.py:77–78`, `rsi2_crypto/backtest_rsi2.py:58–59`,
`rsi2_mean_reversion/backtest_rsi2.py:85–86`, `t3_supertrend/backtest_trend.py:27–28`,
`turtle_soup_crypto/backtest_turtle_soup.py:96–97`,
`turtle_soup_stocks/backtest_turtle_soup.py:92–93`,
`volatility_breakout/backtest_breakout.py:105–106`,
`volatility_breakout_crypto/backtest_breakout.py:73–74`), dazu
`elliott_wave_stocks/signal_quality_test.py:37–38` als Verweis auf
`backtest_elliott`. **Ob der Laufpfad daraus liest, ist die Messung aus Plan
Punkt 5 — hier nicht gemessen.** Alle gemessenen Werte sind zeichengleich
`0.1` / `0.05` / `0.90`.

⚠️ **Vermerk nach (4):** Der Registertext von Punkt 7 und 9 nennt **keinen**
dieser Orte; der Zustand war bis zur Umsetzung von (1)–(3) **ungeschützt**.

**Fables Frage vor der Umsetzung, zeichengleich:**

> *Warum die Optimierer die Kosten heute vielleicht gar nicht aus `forward_test.py` lesen:* Das habe ich nicht gemessen und ihr nicht gefragt. **Nur das Ob, vor der Umsetzung:** Woher beziehen die neun `multi_symbol_optimise.py` und `equity_simulation.py` heute Kosten und Slippage — aus einer eigenen Konstante, aus `forward_test.py`, aus `messgroessen.py`, oder gar nicht? Wenn die Antwort „aus einer eigenen Konstante je Bot" lautet, gibt es neun weitere Kopien, und (2) ist grösser als eine Zeile.

⚠️⚠️ **Offen (Fable 22d), zeichengleich:**

> **Unsicher:** ob `messgroessen.py` und `registerdaten.py` als Abschnitt-0-eingefrorene Dateien für (3) noch geändert werden dürfen — wenn nicht, trägt ein neues kleines Modul die vier Werte, und die eingefrorenen Dateien bleiben stehen. Das seht ihr im Register (Abschnitt 0 und 15.8), ich nicht.

⭐ **Dazu gehört die Messung aus Plan Punkt 5:** woher beziehen die neun
`multi_symbol_optimise.py` und `equity_simulation.py` heute Kosten und
Slippage? ⛔ **Beides nicht Gegenstand dieses Eintrags.** Die Werte bleiben, wo
sie sind; Fables Kandidaten-Module (`messgroessen.py`, `registerdaten.py`)
sind Abschnitt-0-eingefroren (`herkunft.py` `EINGEFROREN`, 37.4) — ob sie für
(3) geändert werden dürfen, entscheidet nicht dieser Abschnitt.

**Marken am alten Ort:** bei **Sperrlistenpunkt 7** und bei **Punkt 9**.

### 37.6 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Sonde ändern** — sie meldet ihren Ausgang heute je Punkt; 37.1 verlangt ihn je Bestandteil, 37.2 die Prüfung der Gruppe „bestimmt" | Handwerk, eigene Freigabe |
| ⛔ | **Ein neues Abbild erzeugen** (Plan Punkt 2b) — der Befund `1` an Punkt 2 (37.3) bleibt bis dahin stehen; das Abbild `6a1b732e…` bleibt | eigene Aufgabe |
| ⛔ | **Werte verschieben** („ein Wert, ein Ort", 37.5 (1)–(3), Plan Punkt 6) — braucht erst die Messung aus Plan Punkt 5 | Betreiber, Freigabe |
| ⛔ | **`herkunft.py` öffnen** — Fables Entscheidung 37.4: nicht öffnen | — |
| ⛔ | **Irgendeine `.py` ändern** · ⚠️ `python3 faltenplan.py` — nicht aufgerufen | — |
| ⭐ | **Keine Zahl bewegt:** Faltenliste 33.2 vor und nach dem Eintrag zeichengleich (M5); die drei Sperrlisten-Hashes `0e54ac5c…`, `a163c498…`, `4549395f…` unverändert (M6); die Sperrlisten-Sonde lesend vor und nach dem Eintrag: Prüfung (ii) `0`, Listentext wie bei Erzeugung, unverändert `1` nur an Punkt 2 | — |
| ⚠️ | **Offen:** die Sonde muss je Bestandteil **zurückgeben** (37.1) · die Gruppe „bestimmt" **prüfen** (37.2) · das neue Abbild (Plan 2b, schliesst 37.3) · die Messung aus Plan 5 (woher lesen die Optimierer Kosten?) · Fables Unsicherheit zu den eingefrorenen Modulen (37.5) · die zwei Messabweichungen in 37.4 (Z. 51 statt 41; vier/vier statt „fünf") und in 37.5 (`GEBUEHR_PCT`; neun `backtest_*.py`) — Fable zur Kenntnis | Betreiber / Fable |

*Dieser Abschnitt ist rein additiv: Er trägt zwei Präzisierungen bzw.
Ergänzungen, eine Ergänzung zur Bedeutung eines Sondenbefunds, eine
Tatsachennotiz und einen Ersteintrag des Verfahrensprüfers zeichengleich ein;
setzt sieben Marken am alten Ort; hält die nachgemessenen Tatsachen samt vier
Abweichungen fest — und entfernt nichts. Gebaut wird nichts.*


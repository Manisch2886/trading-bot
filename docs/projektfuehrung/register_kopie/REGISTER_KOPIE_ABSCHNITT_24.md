# REGISTER-KOPIE Abschnitt 24 (von 0–52) — Register-Z. 4225–4569 — Commit ad351d5f0351d8a25479547edb96a32dd6cf3bd5 — 2026-10-02 — Original sha256 a749678043f32e5c6bf7034205bc7176550ec4ea35d08171b43d40401aec7ece — KOPIE, nicht das Register

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

> ⭐ **24.2 PRÄZISIERT durch R36 (48.4)** (Fable 29b R36, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

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


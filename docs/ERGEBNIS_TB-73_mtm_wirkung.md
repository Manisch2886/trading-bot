# ERGEBNIS TB-73 — Die Wirkung des Mark-to-Market-Drawdowns ist gemessen und berichtet (Mac-Sitzung, 20.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-73_mtm_wirkung.md`. **Ausgeführt am
MacBook**, Zweig `main`, Ausgang `537ca51` (= `origin/main` beim Start),
Interpreter **`trading-env/bin/python3`, Python 3.9.6**. Ein Anlauf, sechs
Schritte, jeder gesichert und gepusht.

⭐ **Kurz:** Der tägliche Mark-to-Market-Drawdown (M) ist in **59 von 64**
Falten mit Grundlage tiefer als der ereignisindizierte (E); der Median der
Differenzen je Bot liegt zwischen **−1,39 pp** und **−3,09 pp**, der Faktor M/E
je Falte bei 1,04 / 1,30 / 1,88 (10./50./90. Perzentil). **2020 ist bei
keinem Krypto-Bot messbar** — die TB-24-Listen der fünf Krypto-Bots beginnen
2021-09 bis 2022-03. **In fünf Falten ist M flacher als E**, darunter
`elliott_wave_stocks` 2020 (+3,90 pp) und 2022 (+1,20 pp); jeder Fall ist
zerlegt und hat denselben Grund — unrealisierte *Gewinne* in offenen
Positionen am Tiefpunkt der Ereigniskurve, von Hand nachgerechnet. Register
**24.6** trägt die Notiz (append-only 124/0). **Nichts in
`research/vorregistrierung/`, `shared/`, `strategies/`; keine Empfehlung,
keine Abwägung — Register 24.3 hat entschieden, bevor die Zahl existierte.**

*In einfacher Sprache, zu Beginn:* Die Verlustgrenze eines Bots wird heute nur
an Kauf- und Verkaufstagen gemessen; das Regelwerk verlangt seit TB-71 die
tägliche Messung zum Marktpreis. Diese Sitzung hat ausgerechnet, wie gross der
Unterschied ist — je Bot, je Jahr. Er beträgt meist ein bis drei Prozentpunkte,
in einzelnen Jahren bis acht; in fünf Jahren zeigt die tägliche Messung
weniger Verlust, weil der Bot damals grosse Buchgewinne in offenen Positionen
hatte. Für die Krypto-Bots fehlen die Handelsdaten vor Herbst 2021, deshalb ist
ihr Jahr 2020 nicht messbar. Entschieden wird daraus nichts.

---

## Nachweis 1 — `git status --short` vor dem ersten Schreiben

`docs/belege/TB-73/nachweis1_git_status_vor_dem_ersten_schreiben.txt`, wörtlich:

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/ARBEITSWEISE.md
?? docs/auftraege/MAC_TB-73_mtm_wirkung.md
?? docs/belege/TB-73/
```

Drei Betreiber-Dateien (Auftragszeiger, Auftrag, `ARBEITSWEISE.md` mit dem
neuen Block *„Das Ende einer Sitzung wird genauso vorgegeben wie ihr
Anfang"*), keine Zeile davon aus dieser Sitzung — Schritt 0, Commit `1b6cde7`.
`docs/belege/TB-73/` war zu diesem Zeitpunkt nur der Ordner mit dieser Datei.

---

## Nachweis 2 — Schritt 1: je Bot, welche Grundlage vorliegt — und welche fehlt

`research/mtm_drawdown/grundlage.py`, 27 s, Beleg
`docs/belege/TB-73/nachweis2_grundlage.txt`, Rohdaten
`research/mtm_drawdown/ergebnisse/grundlage.json`. Commit `5e9ef2b`.

| Bot | Liste | Positionen | Zeitraum | Kapitalkette | `entry_price` = Schluss der Einstiegskerze | 1d-Abdeckung | **Falten ohne Grundlage** | teilweise (Liste ab) |
|---|---|---:|---|---|---|---|---|---|
| `elliott_wave` | ja | 130 | 2021-09-22 … 2026-08-20 | schliesst | max 0 | ja, 0 fortgeschrieben / 660 | **2018-2019** | 2020-2021 (2021-09-22) |
| `t3_supertrend` | ja | 656 | 2021-09-01 … 2026-08-29 | schliesst | max 0 | ja, 0 / 2 614 | **2019, 2020** | 2021 (2021-09-01) |
| `rsi2_crypto` | ja | 392 | 2022-02-11 … 2026-08-20 | schliesst | max 0 | ja, 0 / 1 584 | **2019, 2020, 2021** | 2022 (2022-02-11) |
| `turtle_soup_crypto` | ja | 1 414 | 2021-10-12 … 2026-08-28 | schliesst | max 0 | ja, 0 / 7 037 | **2018, 2019, 2020** | 2021 (2021-10-12) |
| `volatility_breakout_crypto` | ja | 207 | 2022-03-17 … 2026-08-30 | schliesst | max 0 | ja, 0 / 1 557 | **2018, 2019, 2020, 2021** | 2022 (2022-03-17) |
| `elliott_wave_stocks` | ja | 395 | 2016-10-28 … 2026-09-01 | schliesst | max 2,2e-16 | ja, 0 / 9 884 | — | — |
| `rsi2_mean_reversion` | ja | 4 232 | 2016-09-01 … 2026-09-01 | schliesst | max 2,2e-16 | ja, 0 / 16 645 | — | — |
| `turtle_soup_stocks` | ja | 8 915 | 2016-09-01 … 2026-09-01 | schliesst | max 2,2e-16 | ja, 0 / 89 150 | — | — |
| `volatility_breakout` | ja | 1 454 | 2016-09-01 … 2026-09-01 | schliesst | max 2,2e-16 | ja, 0 / 19 850 | — | — |

**Was vorliegt:** neun Listen mit Ein- und Ausstiegszeitpunkt, Einstand,
Ausstiegskurs, `pnl_pct`, `allocation`, `capital_after` je ausgeführter
Position; die Kapitalkette schliesst bei allen neun (die Kurvenreihenfolge
ist daraus rekonstruierbar, auch bei gleichem Zeitstempel); `entry_price` ist
der Schlusskurs der Einstiegskerze in den heutigen Dateien (17 795 Positionen,
max. 2,2e-16); die 1d-Dateien haben an jedem Tagesschluss mit offener Position
einen eigenen Kurs (0 fortgeschriebene bei 148 981 Positionstagen).

⚠️ **Was fehlt — und nicht ersetzt wurde (Auftrag: *„miss nicht drumherum"*):**
Die fünf Krypto-Listen entstanden am 13.09.2026 auf dem Datenstand *vor* dem
TB-34-Neuaufbau (1 826 Tageszeilen, `research/kursdaten_neuaufbau/BERICHT.md`
Abschnitt 2) und beginnen deshalb 2021-09-01 bis 2022-03-17. Die Faltenpläne
beginnen 2018/2019. **Die Falten 2018–2020 aller Krypto-Bots haben keine
Grundlage; 2020 — eine der beiden Falten aus Fables Warnung — ist bei keinem
Krypto-Bot messbar.** Neue Listen wären ein neuer Backtest auf heutigen Daten,
nicht die TB-24-Grundlage, und kein Teil dieses Auftrags.

---

## Nachweis 3 — Die beiden Proben aus Schritt 2, je mit Ergebnis

`research/mtm_drawdown/test_mtm_kern.py`, **24 von 24 bestanden**, 0,3 s;
Beleg `docs/belege/TB-73/nachweis3_proben.txt`. Commit `732440c`.

| Probe | Aufbau | Ergebnis |
|---|---|---|
| **1** — ein Bot, dessen Positionen alle innerhalb eines Tages schliessen | echte `t3_supertrend`-Liste, jeder Ausstieg = Einstieg + 1 h, `pnl_pct` unverändert, Kette neu geschlossen | **1a** (höchstens ein Ausstieg je Tag, 337 Positionen): **E = E_tag = M in allen acht Falten**, Gesamt-Drawdown über das importierte `calculate_max_drawdown` −23,47 = M −23,47. **1b** (alle 656, mehrere Ausstiege je Tag): E_tag = M überall, E nie flacher als E_tag; Falte 2023 E −11,55 gegen E_tag −11,12 — der Raster-Effekt allein (siehe *„Was der Auftrag anders sah"*) |
| **2** — eine Position von Hand | Einstand 100, Schlüsse 100 / 90 / 80 / 95, Ausstieg 105; Allokation 2 000 auf 10 000; 0,15 % je Seite | Tagespfad **9 997 / 9 797 / 9 597 / 9 897 / 10 094** zeichengleich mit der Handrechnung; **E = 0,00, E_tag = 0,00, M = −4,03** — M zeigt den Zwischenverlust, E nicht |
| **3** *(Zusatz dieser Sitzung)* | A mit +20 % unrealisiert im Buch, B schliesst mit −10 % | E = −1,00, **M = −0,98 — flacher**, wie von Hand gerechnet; der Kern meldet den Fall. *„M nie flacher als E"* ist kein Satz der Rechnung |
| K1/K2 | Kette rekonstruiert (Q vor P); Kette, die nicht schliesst → `ValueError`; fehlender Kurs → `ValueError` | ✅ |

**Mutationsprobe** (Wegwerf-Kopie im Scratchpad, Original unberührt, `diff`
danach leer): unrealisierten Wert ignorieren → **5 rot**; Einstiegskosten aus
der Bewertung nehmen → **3 rot**; Tagesgrenze um einen Tag verschieben →
**10 rot**. Die Proben beissen.

---

## Nachweis 4 — Die Messung je Bot und Falte, 2020 und 2022 hervorgehoben

`research/mtm_drawdown/alle_bots.py` → `messung.py` je Bot → `auswertung.py`;
alle Tabellen in `research/mtm_drawdown/ergebnisse/messung.md`, Rohdaten
`ergebnisse/<bot>.json` und `<bot>_tagespfad.csv`; Beleg
`docs/belege/TB-73/nachweis4_messung_stdout.txt`. Commits `5e4dd95`,
`f27b6c0` (Bericht). Falten aus `faltenplan_tb72.json`.

E → M je Falte, Prozent. **Fett: 2020 und 2022.** ᵗ = Liste beginnt in der
Falte; ⚠️ = M flacher als E; „keine" = keine Grundlage; „″" = zweites Jahr der
Zweijahresfalte; 2026 = Bestätigungsperiode, nicht im Median.

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

**2020 und 2022 einzeln** (Differenz in pp, Faktor M/E):

| Bot | 2020 | 2022 |
|---|---|---|
| `elliott_wave` | 2020-2021 ᵗ: −2,81 → −4,48 (−1,67 pp, 1,59) | 2022-2023: −10,17 → −15,40 (−5,23 pp, 1,51) |
| `t3_supertrend` | keine Grundlage | −12,28 → −14,11 (−1,83 pp, 1,15) |
| `rsi2_crypto` | keine Grundlage | ᵗ −8,65 → −10,15 (−1,50 pp, 1,17) |
| `turtle_soup_crypto` | keine Grundlage | −27,86 → −30,38 (−2,52 pp, 1,09) |
| `volatility_breakout_crypto` | keine Grundlage | ᵗ −6,07 → −10,39 (−4,32 pp, 1,71) |
| `elliott_wave_stocks` | −13,35 → −9,45 ⚠️ (+3,90 pp, 0,71) | −19,31 → −18,11 ⚠️ (+1,20 pp, 0,94) |
| `rsi2_mean_reversion` | −9,01 → −11,28 (−2,27 pp, 1,25) | −10,52 → −11,93 (−1,41 pp, 1,13) |
| `turtle_soup_stocks` | −29,91 → −34,45 (−4,54 pp, 1,15) | −18,73 → −20,69 (−1,96 pp, 1,11) |
| `volatility_breakout` | −9,41 → −12,60 (−3,19 pp, 1,34) | −23,97 → −25,80 (−1,83 pp, 1,08) |

**Median der Differenzen je Bot** über die Selektionsfalten mit Grundlage
(nur neben den Faltenwerten oben gültig): `elliott_wave` −2,92 ·
`t3_supertrend` −3,09 · `rsi2_crypto` −1,39 · `turtle_soup_crypto` −1,42 ·
`volatility_breakout_crypto` −1,83 · `elliott_wave_stocks` −2,88 ·
`rsi2_mean_reversion` −1,71 · `turtle_soup_stocks` −2,53 ·
`volatility_breakout` −1,60 pp. Die grössten Differenzen liegen nicht in 2020
oder 2022: `turtle_soup_crypto` 2025 −7,87 pp, `turtle_soup_stocks` 2025
−6,72 pp, `turtle_soup_crypto` 2026 −6,22 pp, `elliott_wave_stocks` 2026
−5,97 pp.

Die mittlere Exposure je Falte (Definition aus
`research/exposure_messung/exposure_kern.py`) steht in `messung.md` neben jeder
Falte — sie ist das Argument, das der Benchmark tragen würde; **nachgeschlagen
wird nichts** (Register 24.3).

---

## Nachweis 5 — Die Richtungsprobe

Beleg `docs/belege/TB-73/nachweis5_richtungsprobe.md` (=
`research/mtm_drawdown/ergebnisse/richtungsfaelle.md`, erzeugt von
`richtungsfall.py`).

**Fünf Falten, in denen M flacher ist als E — einzeln benannt, keiner
geglättet:**

| Bot | Falte | E | M | M − E | am E-Tief unrealisiert in offenen Positionen |
|---|---|---:|---:|---:|---|
| `t3_supertrend` | 2023 (Sel.) | −11,55 | −11,25 | +0,30 pp | +63,52 in 1 Position (SOLUSDT, später +39,18 %) |
| `volatility_breakout_crypto` | 2023 (Sel.) | −12,90 | −12,84 | +0,06 pp | +1 029,65 in 5 Positionen (SOL, LINK, AAVE, PROM, DOGE; später +3 bis +58 %) |
| `elliott_wave_stocks` | **2020** (Sel.) | −13,35 | −9,45 | **+3,90 pp** | **+2 055,08 in 6 Positionen** (CRWD +98 %, WDC, GD, TJX, LMT, ACN — März-Einstiege, später +26 bis +168 %) |
| `elliott_wave_stocks` | **2022** (Sel.) | −19,31 | −18,11 | +1,20 pp | +773,93 in 2 Positionen (HOOD +45 %, BA) |
| `volatility_breakout` | 2026 (Best.) | −4,90 | −4,37 | +0,53 pp | +608,03 in 5 Positionen (DELL, VLO, PSX, MRVL, XOM) |

**Warum das kein falscher Pfad ist:** E bewertet offene Positionen zum
Einstand. Das lässt E unrealisierte Verluste nicht sehen (der Fall, den 24.1
beschreibt — 59 von 64 Falten) **und** unrealisierte Gewinne nicht (diese
fünf). Bei `elliott_wave_stocks` 2020 sind die Stop-Loss-Verluste vom
Februar/März am 13.05. realisiert, die sechs Einstiege vom 18.03.–06.04.
stehen zum Einstand im Buch, obwohl sie +2 055 tragen; M hat sein Tief am
18.03. bei −9,45 %. Probe 3 rechnet den Mechanismus von Hand nach. Ein Pfad,
der „M ≤ E" erzwänge, müsste unrealisierte Gewinne ignorieren — und wäre kein
Mark-to-Market. **Konsistenz-Gegenprobe: in 0 von 64 Falten ist E flacher als
E_tag** (erwartet: jeder Tagesendwert ist ein E-Punkt). Die Aussage im Kopf von
Register 24 (*„nie flacher"*) ist damit als Näherung belegt — Register 24.6
hält das als Tatsache fest.

---

## Nachweis 6 — SHA-256 der Sperrlisten-Dateien, alle unverändert

`docs/belege/TB-73/nachweis6_sha256_sperrlisten_dateien.txt`
(`research/vorregistrierung/ergebnisse/`):

| Datei | SHA-256 | Vergleich |
|---|---|---|
| `benchmark_drawdowns.json` | `a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee` | = TB-72 Nachweis 3 |
| `benchmark_drawdowns_vt.json` | `4549395fb3ac30f852362ba586b3ac73cdb6b32e5e944a921f0adb239818745d` | = TB-72 Nachweis 3 |
| `benchmark_drawdowns_tb72.json` | `e4ba341d3177d455b1c3151f4bb2e0cf7f16fbd516d9b30edd45d0c7dc005e56` | = Stand des Commits `27c58a2` (TB-72 Schritt 4) |
| `faltenplan.json` | `0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339` | = TB-72 Nachweis 3 |
| `faltenplan_tb72.json` | `19e8cbca874d6e7455f2f3bc0723def9ea058d0b314fa1772e04cd64ff1c9d24` | = `HEAD` |

`git status --short research/vorregistrierung/ shared/ strategies/`: leer.

---

## Nachweis 7 — Register: `numstat` Spalte zwei = 0

Commit `01da585`, `docs/belege/TB-73/nachweis7_register_numstat.txt`:

```
124	0	docs/VORREGISTRIERUNG_neuselektion.md
```

Abschnitt **24.6** (Tatsachennotiz zu 24.3 und 24.4, vor `## 25.` eingefügt)
plus eine Marke *„NACHGETRAGEN in Abschnitt 24.6"* als eigene Zeile unter der
24.4-Tabelle; die Zeile *„Wirkung, gemessen — noch nicht"* bleibt, wie sie war.
Kein Satz in 24.6 wirft 24.3 auf; keine Bot-Zahl steht neben `erlaubt(f)`,
`DD_Benchmark` oder `DD_Toleranz`.

---

## Nachweis 8 — Laufzeit je Messung *(Regel aus TB-72, Journal-Nachtrag 20k)*

Mac, `trading-env/bin/python3` 3.9.6, 20.09.2026; Beleg
`docs/belege/TB-73/nachweis8_laufprotokoll.json`.

| Messung | Laufzeit |
|---|---:|
| `grundlage.py` (Schritt 1, neun Bots, liest 17 795 Positionen und 1d-/Zeitrahmen-Dateien) | 27 s |
| `test_mtm_kern.py` (Schritt 2) | 0,3 s |
| `alle_bots.py` (Schritt 3, neun Kindprozesse + Auswertung) | **19,3 s** |
| davon `messung.py` je Bot, inkl. Import der Bot-Module: `elliott_wave` 0,8 · `t3_supertrend` 0,8 · `rsi2_crypto` 0,8 · `turtle_soup_crypto` 0,8 · `volatility_breakout_crypto` 0,7 · `elliott_wave_stocks` 3,3 · `rsi2_mean_reversion` 4,0 · `turtle_soup_stocks` 4,3 · `volatility_breakout` 3,8 s | |
| `richtungsfall.py` (fünf Fälle) | ~10 s |
| Mutationsprobe (drei Läufe in der Kopie) | 3 × 0,3 s |

Wer die Messung wiederholt, zahlt unter einer Minute. Sie hängt an keinem
Kindprozess des Laufcodes; die Bot-Module werden nur für Konstanten importiert.

---

## Nachweis 9 — `git diff --numstat 537ca51..HEAD` je Datei

`docs/belege/TB-73/nachweis9_numstat_537ca51_bis_schritt4.txt` (43 Dateien,
Stand nach Schritt 4; Schritt 5 fügt diese Datei, den Journal-Nachtrag, eine
Backlog-Zeile und zwei Belege hinzu). **Nichts in `research/vorregistrierung/`,
`shared/`, `strategies/`** (gemessen: 0 Zeilen mit diesen Pfaden). Geändert
sind ausschliesslich:

| Bereich | Dateien | Zeilen (+/−) |
|---|---|---|
| `research/mtm_drawdown/` (neu) | 7 Skripte, `BERICHT.md`, 22 Ergebnisdateien | nur `+` |
| `docs/VORREGISTRIERUNG_neuselektion.md` | Abschnitt 24.6, Marke | 124 / **0** |
| `docs/belege/TB-73/` | Nachweise 1–9 | nur `+` |
| Betreiber-Dateien aus Schritt 0 | `AKTUELLER_AUFTRAG.md` 3/4, `MAC_TB-73_mtm_wirkung.md` 214/0, `ARBEITSWEISE.md` 47/0 | nicht von dieser Sitzung geschrieben |
| Schritt 5 | `docs/projektfuehrung/BACKLOG.md` 1/0 (`K4m`), `nachtraege/JOURNAL_NACHTRAG_2026-09-20l.md`, dieses Dokument | |

---

## Was der Auftrag anders sah — und wo die Messung galt

| Auftrag | gemessen / getan |
|---|---|
| Schritt 3: *„bei 25 / 50 / 100 % Exposure: E gegen M"* | **Nicht so gerechnet.** Die Stufen sind das Argument des Benchmarks (`DD_Benchmark(f, e)`, Register 4.2); ein Bot hat je Falte **eine** Exposure, die aus seinen Positionen folgt (steht neben jeder Falte in `messung.md`: `turtle_soup_stocks` 0,66–0,86, `elliott_wave` 0,04–0,06). Sie auf drei Stufen zu setzen hiesse andere Positionen (*„zwei verschiedene Bots"*, vom Auftrag selbst verboten) oder Hebel — eine erfundene Zahl |
| Schritt 3: *„der Median … ist die Grösse, die zur `DD_Toleranz` führt"* | Median von E und M je Bot berichtet, neben den Faltenwerten. `DD_Toleranz` ist der Median der **Benchmark**-Drawdowns (Festlegung 5), nicht der Bot-Drawdowns — der Bot-Median führt zu keiner Grösse des Registers |
| Schritt 3: *„M darf nie flacher sein als E … sonst ist der Pfad falsch"* | Fünf Fälle gefunden, jeder zerlegt, Grund benannt, Probe 3 von Hand. Der Pfad ist richtig; der Satz ist eine Näherung (59 von 64) |
| Schritt 2, Probe 1: *„E und M müssen gleich sein"* | Exakt nur mit höchstens einem Ausstieg je Tag (1a). Mit mehreren (1b) ist E_tag = M, aber E tiefer — E hat Zwischenstände innerhalb eines Zeitstempels, deren Reihenfolge `zuteilung.py` per gesätem Zufall festlegt. In den echten Messungen höchstens 0,96 pp (`volatility_breakout` 2020) |
| Abschnitt 1: *„Die Grundlage liegt vor"* | Für Aktien ja; für Krypto nicht vor 2021-09 / 2022-03. 2020 Krypto nicht messbar; nicht ersetzt |
| Abschnitt 4: *„sechs Commits"* | sieben plus Abgabe: Schritt 0, 1, 2, 3 (Messung), 3 (Bericht), 4, 5 — der Bericht des Forschungsordners war ein eigener Teil |

---

## Offen

| | wer |
|---|---|
| ⚠️ **Krypto-Falten 2018–2020 ohne Grundlage.** Wer sie messen will, braucht Trade-Listen aus einem Backtest auf den heutigen Kursdateien (ab 2017/2018) — ein neuer Backtest, kein TB-24-Stand. Ob das gewünscht ist, ist eine Betreiberfrage; **diese Sitzung legt sie nicht vor**, weil nach 24.3 keine Zahl hier etwas entscheidet | Betreiber |
| Die Tatsachennotiz zur Richtung (24.6): der Satz *„nie flacher"* im Kopf von Abschnitt 24 und in 24.4 bleibt stehen; wer ihn zitiert, liest 24.6 mit | Register |
| Dieser Journal-Nachtrag `(20l)` ins Journal (Block nach dem höchsten vorhandenen) | nächste Einarbeitung / TB-64-Wächter |
| Projektablage nachziehen (`K4e`): `AKTUELLER_AUFTRAG.md` (TB-73-Zeile auf „erledigt") | steuernder Chat / Betreiber |
| `K4j` unverändert — der Laufcode, der die Tagesreihe je Zelle erzeugt, existiert weiterhin nicht; `mtm_kern.py` ist ein Forschungsskript, kein Vorbild für den Laufcode, und die Zahl aus dieser Messung ist für `K4j` kein Argument (24.3) | TB-30b |

---

## Commit-Liste dieser Sitzung

| Commit | Schritt |
|---|---|
| `1b6cde7` | 0 — drei Betreiber-Dateien gesichert |
| `5e9ef2b` | 1 — `grundlage.py`, `mtm_kern.py`, Nachweis 1 und 2 |
| `732440c` | 2 — `test_mtm_kern.py`, Nachweis 3 mit Mutationsprobe |
| `5e4dd95` | 3 — `messung.py`, `alle_bots.py`, `auswertung.py`, `richtungsfall.py`, Ergebnisse, Nachweise 4, 5, 6, 8 |
| `f27b6c0` | 3 — `research/mtm_drawdown/BERICHT.md` |
| `01da585` | 4 — Register 24.6, Nachweis 7 |
| `bb6ab88` | 5 — `K4m`, Journal-Nachtrag `(20l)`, dieses Dokument, Nachweis 9 |

---

## In einfacher Sprache

**Was gemessen wurde:** Wie tief jeder Bot in jedem Jahr gefallen ist — nach
der heutigen Rechnung (nur an Kauf- und Verkaufstagen) und nach der Rechnung,
die das Regelwerk seit TB-71 verlangt (jeden Tag zum Marktpreis).

**Was herauskam:** Die tägliche Rechnung zeigt in 59 von 64 messbaren Jahren
einen tieferen Fall, meist um ein bis drei Prozentpunkte, in einzelnen Jahren
bis acht. In fünf Jahren zeigt sie einen flacheren, weil der Bot damals grosse
Buchgewinne hatte, die die heutige Rechnung erst beim Verkauf sieht — das ist
nachgerechnet, kein Fehler.

**Was fehlt:** Für die fünf Krypto-Bots gibt es keine Handelsliste vor Herbst
2021. Ihr Jahr 2020 ist nicht messbar; das steht so da.

**Was daraus folgt:** Nichts, das hier entschieden würde. Die Entscheidung
steht seit TB-71 im Regelwerk und wurde absichtlich vor dieser Zahl getroffen.
Die Zahl ist berichtet und abgelegt.

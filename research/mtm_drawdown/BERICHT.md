# Die Wirkung des Mark-to-Market-Drawdowns, gemessen (TB-73)

**Status: reine Messung. KEINE Empfehlung, KEINE Abwägung, KEINE Änderung an
Bot-, Backtest-, Register- oder Laufcode.** Alle Dateien liegen unter
`research/mtm_drawdown/`; nichts in `research/vorregistrierung/`, `shared/`
oder `strategies/` ist berührt (Nachweis 9 im Ergebnisdokument).

> **Register 24.3, seit TB-71 und vor dieser Messung:** *„Der Drawdown der
> Nebenbedingung wird auf der täglichen Mark-to-Market-Reihe gerechnet (1a);
> die Grösse der Abweichung zur ereignisindizierten Kurve wird gemessen und
> berichtet und ist für die Entscheidung ohne Belang."*
>
> Dieser Bericht beziffert. Er entscheidet nichts, und er legt nichts zur
> Entscheidung vor. Wer aus den Zahlen unten *„zu klein für die Mühe"* oder
> *„zu gross vor dem Tag"* liest, trifft die nachträgliche Wahl, gegen die F17
> und 24.3 stehen.

*Gemessen am 20.09.2026 auf dem Mac, `trading-env/bin/python3` 3.9.6, an den
TB-24-Trade-Listen (`research/tb24_haltedauern/daten/`) und den Kursdateien in
`data/`; Falten aus `research/vorregistrierung/ergebnisse/faltenplan_tb72.json`.
Alle Zahlen dieses Berichts stehen zuerst in `ergebnisse/messung.md`
(erzeugt von `auswertung.py`) und `ergebnisse/<bot>.json`.*

---

## 0. Die Zahlen zuerst — je Bot, je Falte

E = ereignisindizierter Drawdown (der heutige Weg: `capital_after` je Ausstieg,
`shared/messkette.py::calculate_max_drawdown`). M = täglicher
Mark-to-Market-Drawdown (offene Positionen zum Tagesschluss, Registertext 1a).
Beide auf **denselben ausgeführten Positionen**, in Prozent, negativ.
**Fett: 2020 und 2022.** ᵗ = Liste beginnt innerhalb der Falte (teilweise).
⚠️ = M flacher als E (Abschnitt 4). „keine" = keine Grundlage (Abschnitt 1).
„″" = zweites Jahr einer Zweijahresfalte (`elliott_wave`).

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

*2026 ist die Bestätigungsperiode (bis 2026-09-01 ausschliesslich), kein
Selektionsjahr; der Median läuft nur über die Selektionsfalten mit Grundlage.
Die Spalte „Median Sel." steht hier absichtlich nur neben den Faltenwerten.*

**Die beiden hervorgehobenen Falten, einzeln:**

| Bot | 2020: E → M | Differenz | Faktor | 2022: E → M | Differenz | Faktor |
|---|---|---:|---:|---|---:|---:|
| `elliott_wave` | 2020-2021 (ab 2021-09-22): -2,81 → -4,48 | -1,67 pp | 1,59 | 2022-2023: -10,17 → -15,40 | -5,23 pp | 1,51 |
| `t3_supertrend` | keine Grundlage | | | -12,28 → -14,11 | -1,83 pp | 1,15 |
| `rsi2_crypto` | keine Grundlage | | | (ab 2022-02-11) -8,65 → -10,15 | -1,50 pp | 1,17 |
| `turtle_soup_crypto` | keine Grundlage | | | -27,86 → -30,38 | -2,52 pp | 1,09 |
| `volatility_breakout_crypto` | keine Grundlage | | | (ab 2022-03-17) -6,07 → -10,39 | -4,32 pp | 1,71 |
| `elliott_wave_stocks` | -13,35 → **-9,45** ⚠️ | +3,90 pp | 0,71 | -19,31 → **-18,11** ⚠️ | +1,20 pp | 0,94 |
| `rsi2_mean_reversion` | -9,01 → -11,28 | -2,27 pp | 1,25 | -10,52 → -11,93 | -1,41 pp | 1,13 |
| `turtle_soup_stocks` | **-29,91 → -34,45** | -4,54 pp | 1,15 | -18,73 → -20,69 | -1,96 pp | 1,11 |
| `volatility_breakout` | -9,41 → -12,60 | -3,19 pp | 1,34 | **-23,97 → -25,80** | -1,83 pp | 1,08 |

**Was die Tabelle zeigt, ohne es zu bewerten:**

- In **59 von 64** Falten mit Grundlage ist M tiefer als E. Der Median der
  Differenzen je Bot liegt zwischen **−1,39 pp** (`rsi2_crypto`) und
  **−3,09 pp** (`t3_supertrend`); der Faktor M/E je Falte zwischen 1,04 (10.-Perzentil) und 1,88 (90.-Perzentil), Median 1,30 — in ruhigen Falten mit kleinem E auch weit darüber
  (`elliott_wave_stocks` 2017: −0,99 → −5,26, Faktor 5,3).
- Die grösste Differenz in Prozentpunkten steht nicht in 2020 oder 2022:
  `turtle_soup_crypto` 2025 **−7,87 pp** (−27,42 → −35,29), `turtle_soup_stocks`
  2025 −6,72 pp, `turtle_soup_crypto` 2026 −6,22 pp, `elliott_wave_stocks` 2026
  −5,97 pp, `elliott_wave` 2022-2023 −5,23 pp.
- **2020 bei Krypto ist nicht messbar** — keine der fünf Listen reicht dorthin
  (Abschnitt 1). Bei den vier Aktien-Bots ist 2020 in drei Fällen die Falte mit
  der grössten oder zweitgrössten Differenz des Bots (`turtle_soup_stocks`
  −4,54 pp, `volatility_breakout` −3,19 pp, `rsi2_mean_reversion` −2,27 pp) —
  und bei `elliott_wave_stocks` die Falte, in der M am deutlichsten **flacher**
  ist als E (+3,90 pp; Abschnitt 4 erklärt, warum).
- **In fünf Falten ist M flacher als E** (⚠️). Das ist kein Fehler des Pfades,
  sondern ein Mechanismus der Ereigniskurve, der in Probe 3 von Hand
  nachgerechnet und in jedem der fünf Fälle zerlegt ist (Abschnitt 4,
  `ergebnisse/richtungsfaelle.md`).

---

## 1. Die Grundlage — was vorlag und was fehlt (Schritt 1)

`grundlage.py`, Nachweis 2. Für jeden der neun Bots:

| Bot | Liste | Positionen | Zeitraum der Liste | Kapitalkette | Einstand = Schluss der Einstiegskerze | 1d-Kurse decken alle Haltedauern |
|---|---|---:|---|---|---|---|
| `elliott_wave` | ja | 130 | 2021-09-22 … 2026-08-20 | schliesst | max 0 | ja, 0 fortgeschrieben / 660 Positionstage |
| `t3_supertrend` | ja | 656 | 2021-09-01 … 2026-08-29 | schliesst | max 0 | ja, 0 / 2 614 |
| `rsi2_crypto` | ja | 392 | 2022-02-11 … 2026-08-20 | schliesst | max 0 | ja, 0 / 1 584 |
| `turtle_soup_crypto` | ja | 1 414 | 2021-10-12 … 2026-08-28 | schliesst | max 0 | ja, 0 / 7 037 |
| `volatility_breakout_crypto` | ja | 207 | 2022-03-17 … 2026-08-30 | schliesst | max 0 | ja, 0 / 1 557 |
| `elliott_wave_stocks` | ja | 395 | 2016-10-28 … 2026-09-01 | schliesst | max 2,2e-16 | ja, 0 / 9 884 |
| `rsi2_mean_reversion` | ja | 4 232 | 2016-09-01 … 2026-09-01 | schliesst | max 2,2e-16 | ja, 0 / 16 645 |
| `turtle_soup_stocks` | ja | 8 915 | 2016-09-01 … 2026-09-01 | schliesst | max 2,2e-16 | ja, 0 / 89 150 |
| `volatility_breakout` | ja | 1 454 | 2016-09-01 … 2026-09-01 | schliesst | max 2,2e-16 | ja, 0 / 19 850 |

**Was vorliegt:** Alle neun TB-24-Listen haben je ausgeführter Position
`entry_time`, `exit_time`, `entry_price`, `exit_price`, `pnl_pct`,
`allocation`, `capital_after`. Die Kapitalkette
`capital_after[k] = capital_after[k−1] + allocation·pnl/100` schliesst bei
allen neun — die Listen sind die einer Kapitalsimulation, und die
Kurvenreihenfolge (auch bei gleichem Ausstiegszeitstempel) ist daraus
rekonstruierbar. `entry_price` ist bei allen 17 795 Positionen der
Schlusskurs der Einstiegskerze in den heutigen Kursdateien (grösste relative
Abweichung 2,2e-16) — die Bewertung `close_d / entry_price` ist damit gegen
Bereinigungsverschiebungen der Aktienkurse (yfinance) unempfindlich, weil
Zähler und Nenner aus derselben Datei stammen. Die 1d-Dateien haben an jedem
Tagesschluss, an dem eine Position offen ist, einen eigenen Kurs — kein
einziger fortgeschriebener Kurstag bei 149 000 Positionstagen.

⚠️ **Was fehlt:** **Die fünf Krypto-Listen beginnen zwischen 2021-09-01 und
2022-03-17.** Sie entstanden am 13.09.2026 auf dem Datenstand *vor* dem
TB-34-Neuaufbau — die Krypto-Kursdateien hatten damals 1 826 Tageszeilen
(rund fünf Jahre, `research/kursdaten_neuaufbau/BERICHT.md`, Abschnitt 2);
heute reichen sie bis 2017/2018. Die Faltenpläne der Krypto-Bots beginnen
2018 bzw. 2019. Damit haben **keine Grundlage**:

| Bot | Falten ohne Grundlage | Falte nur teilweise (Liste ab) |
|---|---|---|
| `elliott_wave` | 2018-2019 | 2020-2021 (2021-09-22) |
| `t3_supertrend` | 2019, 2020 | 2021 (2021-09-01) |
| `rsi2_crypto` | 2019, 2020, 2021 | 2022 (2022-02-11) |
| `turtle_soup_crypto` | 2018, 2019, 2020 | 2021 (2021-10-12) |
| `volatility_breakout_crypto` | 2018, 2019, 2020, 2021 | 2022 (2022-03-17) |

**Insbesondere 2020 — eine der beiden Falten aus Fables Warnung — ist bei
keinem Krypto-Bot messbar.** Diese Falten stehen in den Tabellen als „keine"
und tragen keine Zahl. Der Auftrag sagt: *„wenn die Listen nicht reichen, sag
es und miss nicht drumherum"* — die Listen für 2018–2020 Krypto neu zu
erzeugen wäre ein neuer Backtest auf anderen Daten, nicht die TB-24-Grundlage,
und ist nicht Teil dieser Aufgabe (Abschnitt 7).

Die Aktien-Listen (ab 2016-09-01, `RECENT_YEARS_ONLY = 10`) decken alle Falten
2017/2018–2026 vollständig.

---

## 2. Wie gerechnet wurde

**E, der heutige Weg.** `capital_after` je Ausstieg aus der TB-24-Liste — das
ist die `equity_curve` aus `shared/zuteilung.py::simuliere_portfolio`
(Register 24.1, Fundstelle 1). Der Drawdown darauf ist
`shared/messkette.py::max_drawdown_ungerundet`, importiert; die Gesamtzahl je
Bot über `calculate_max_drawdown` als Gegenprobe. Je Falte: Basis ist der
Kapitalstand nach dem letzten Ausstieg vor Faltenbeginn, gezählt werden die
Ausstiege mit `von ≤ exit_time < bis`.

**M, was Registertext 1a verlangt.** An jedem Tag des Rasters:

```
M(d) = Buch(d) + Σ über die am Tagesschluss d offenen Positionen von
       allocation · (close_d / entry_price − 1 − Kosten_Seite/100)
```

`Buch(d)` ist `capital_after` des letzten Ausstiegs vor Tagesende (offene
Positionen zum Einstand — das ist die Ereigniskurve am Tagesende, im Bericht
**E_tag**). Der Summand bewertet jede offene Position zum Tagesschlusskurs aus
`data/<symbol>_1d.csv`. Tage ohne Position tragen 0. Am Ausstiegstag geht
die Position mit ihrem realisierten Ergebnis ein (`pnl_pct` der Liste) — der
Stop-Kurs eines Stop-Loss ist nicht der Tagesschluss, und der Ereignispfad
soll an den Ausstiegen nicht verfälscht werden.

**Die Tagesgrenze.** Zeitstempel sind `open_time` der Kerze. Offen am
Tagesschluss `d` heisst `entry_time < d+1 Tag ≤ exit_time`. Eine Position,
die am selben Tag ein- und aussteigt, ist an keinem Tagesschluss offen
(Probe 1). Bei den Tagesbots ist die Einstiegskerze der Tag selbst, ihr
Schluss der Einstand — die Position steht am Einstiegstag zu
`allocation · (1 − Kosten_Seite/100)` im Buch.

**Die Kosten.** Importiert aus dem Backtest-Modul des Bots
(`TRADING_FEE_PCT`, `SLIPPAGE_PCT`; je Bot 0,1 + 0,05 = 0,15 % je Seite) und an
jeder Liste gegengeprüft: `pnl_pct = (exit/entry − 1)·100 − 2·0,15`, grösste
Abweichung 0,005 pp = die Rundung des Backtests. Die Bewertung zieht die
Einstiegsseite ab dem Einstiegstag ab, die Ausstiegsseite erst beim Ausstieg
— so, wie ein Konto eine offene Position zeigt. Diese Wahl bewegt M um höchstens
0,15 % der gebundenen Allokation; die Mutationsprobe (Nachweis 3) zeigt, dass
Probe 2 sie sieht.

**Das Raster.** Vereinigung der Kurstage der gehandelten Symbole aus den
1d-Dateien — bei Krypto jeder Kalendertag, bei Aktien die Börsentage. Das sind
dieselben Dateien, aus denen `benchmark.py` den Benchmark bewertet
(Registertext 3b (c)). Basis je Falte: der Wert am letzten Rastertag vor
`von`.

**Die Exposure.** Je Falte über `research/exposure_messung/exposure_kern.py`
(Brutto, Kalendertage, Nenner Kapital zu Tagesbeginn) gemittelt — die
Definition, die das Projekt für das Exposure-Argument des Benchmarks führt.
Sie steht in `ergebnisse/messung.md` neben jeder Falte. Der Benchmark selbst
wird **nicht** nachgeschlagen (Abschnitt 5).

**Was nicht neu geschrieben ist:** Zuteilung (die Positionen sind die der
Kaskade aus TB-24, `kennzeichnung_neutral`, Abgleich mit der Exposure-Messung
dort identisch), Drawdown-Rechnung (`messkette`), Kostenzahlen, Startkapital
und Allokation (`equity_simulation` des Bots, gegen das TB-24-Meta
abgeglichen), Bot-Umgebung (`research/drawdown_reihenfolge/botenv.py`).
`shared/zuteilung.py` und `shared/messkette.py` sind gelesen, nicht geändert.

---

## 3. Die Proben (Schritt 2, Nachweis 3)

`test_mtm_kern.py`, 24 von 24 bestanden, 0,3 s.

| Probe | Aufbau | Erwartung | Ergebnis |
|---|---|---|---|
| **1a** | echte `t3_supertrend`-Liste, jeder Ausstieg = Einstieg + 1 h, höchstens ein Ausstieg je Tag (337 Positionen) | E = E_tag = M in jeder Falte | ✅ in allen acht Falten auf die zweite Stelle gleich; Gesamt-Drawdown über das importierte `calculate_max_drawdown` −23,47 = M −23,47 |
| **1b** | dieselbe Liste, alle 656 Positionen (mehrere Ausstiege je Tag) | E_tag = M überall; E nie flacher als E_tag | ✅ E_tag = M in allen Falten; 2023: E −11,55 gegen E_tag −11,12 — **der reine Raster-Effekt** (Abschnitt 4) |
| **2** | eine Position von Hand: 100 → 90 → 80 → 95, Ausstieg 105; Allokation 2 000 auf 10 000; 0,15 % je Seite | Tagespfad 9 997 / 9 797 / 9 597 / 9 897 / 10 094; E = 0,00; M = −4,03 | ✅ zeichengleich |
| **3** *(Zusatz)* | A liegt mit +20 % unrealisiert im Buch, B schliesst mit −10 % | E = −1,00; M = −0,98 — **flacher** | ✅ zeichengleich, der Kern meldet den Fall |
| **K1/K2** | Kette rekonstruiert, Kette bricht ab, fehlender Kurs bricht ab | | ✅ |

**Mutationsprobe** (Wegwerf-Kopie, Original unberührt): unrealisierten Wert
ignorieren → 5 rot; Einstiegskosten aus der Bewertung nehmen → 3 rot;
Tagesgrenze um einen Tag verschieben → 10 rot. Die Proben beissen.

⚠️ **Wo Probe 1 anders ausfällt, als der Auftrag sie formuliert:** *„E und M
müssen gleich sein"* gilt exakt nur, wenn je Tag höchstens ein Ausstieg
liegt (1a). Mit mehreren Ausstiegen je Tag (1b) ist E_tag = M, aber E ist an
den feineren Stützstellen tiefer: E sieht den Zwischenstand nach jedem
einzelnen Ausstieg innerhalb eines Zeitstempels — und die Reihenfolge dieser
Ausstiege legt `zuteilung.py` per gesätem Zufall fest (`ausstiegsreihenfolge`,
Modulkopf: *„entscheidet … über die Zwischenstände der Kapitalkurve und damit
über den gemessenen Drawdown"*). Das ist kein Fehler des Pfades; es ist eine
Eigenschaft von E, die M nicht hat. In den echten Messungen ist der Effekt
klein (E gegen E_tag höchstens 0,96 pp: `volatility_breakout` 2020, −9,41
gegen −8,45), aber vorhanden — deshalb steht E_tag in allen Tabellen daneben.

---

## 4. Die Richtungsprobe — fünf Falten, in denen M flacher ist als E (Nachweis 5)

Der Auftrag: *„M darf nie flacher sein als E. Findest du einen Fall, in dem
doch, ist der Pfad falsch."* Register 24, Kopf: *„der tägliche Drawdown ist
nie flacher als der ereignisweise."*

**Gemessen: in 5 von 64 Falten mit Grundlage ist M flacher als E** — und in
keinem der fünf ist der Pfad falsch. Probe 3 zeigt den Mechanismus von Hand;
`richtungsfall.py` zerlegt jeden Fall (`ergebnisse/richtungsfaelle.md`):

| Bot | Falte | E | M | M − E | Am E-Tief: unrealisiert in offenen Positionen |
|---|---|---:|---:|---:|---|
| `t3_supertrend` | 2023 (Sel.) | −11,55 | −11,25 | +0,30 pp | +63,52 in 1 Position (SOLUSDT, später +39,18 %) |
| `volatility_breakout_crypto` | 2023 (Sel.) | −12,90 | −12,84 | +0,06 pp | +1 029,65 in 5 Positionen (SOL/LINK/AAVE Oktober 2023, später +27 bis +58 %) |
| `elliott_wave_stocks` | **2020** (Sel.) | −13,35 | −9,45 | **+3,90 pp** | **+2 055,08 in 6 Positionen** — die März-Einstiege (CRWD +98 % unrealisiert am 13.05., später +167,89 %; WDC, GD, TJX, LMT, ACN) |
| `elliott_wave_stocks` | **2022** (Sel.) | −19,31 | −18,11 | +1,20 pp | +773,93 in 2 Positionen (HOOD +45 %, BA) |
| `volatility_breakout` | 2026 (Best.) | −4,90 | −4,37 | +0,53 pp | +608,03 in 5 Positionen (DELL, VLO, PSX, XOM) |

**Der Mechanismus, an `elliott_wave_stocks` 2020:** Die Ereigniskurve fällt bis
zum 13.05.2020 auf 10 764,73 — die Stop-Loss-Ausstiege aus dem Februar/März
sind realisiert, die Erholung noch nicht: sechs Positionen, eingestiegen vom
18.03. bis 06.04., stehen zum Einstand im Buch, obwohl sie am 13.05. zusammen
+2 055 unrealisierten Gewinn tragen. M sieht diesen Gewinn; sein Tief liegt
am **18.03.2020** bei −9,45 %. E bucht Verluste sofort und Gewinne erst beim
Ausstieg — in einer V-Erholung ist die Ereigniskurve deshalb **tiefer** als
das Konto. Fables Satz *„Erlebbar ist, was das Konto an jedem Tag zeigt"*
(24.4) gilt in beide Richtungen: das Konto zeigt auch die unrealisierten
Gewinne.

**Was aus der Richtungsprobe folgt — als Tatsache, nicht als Bewertung:** Der
Satz *„M ist nie flacher als E"* ist eine Näherung, die in 59 von 64 Falten
zutrifft und in fünf nicht. Beide Abweichungsrichtungen haben denselben Grund
— E bewertet offene Positionen zum Einstand —, und die Richtung hängt davon
ab, ob am Tiefpunkt der Ereigniskurve unrealisierte Verluste oder Gewinne im
Buch liegen. Ein Pfad, der in den fünf Fällen „M ≤ E" erzwänge, müsste
unrealisierte Gewinne ignorieren — und wäre dann nicht mehr Mark-to-Market.

**Gegenprobe der Konsistenz:** In **0 von 64** Falten ist E flacher als E_tag
— erwartet, weil jeder Tagesendwert ein E-Punkt ist. Wäre diese Zahl > 0,
wäre der Pfad falsch.

---

## 5. Wo der Auftrag anders lag — und was stattdessen gemessen wurde

| Auftrag | gemessen / getan | warum |
|---|---|---|
| Schritt 3: *„je Bot, je Falte, **bei 25 / 50 / 100 % Exposure**: E gegen M"* | **E und M je Bot und Falte bei der Exposure, die die ausgeführten Positionen tatsächlich haben** — sie steht als Spalte „Exposure Ø" neben jeder Falte in `ergebnisse/messung.md` (z. B. `turtle_soup_stocks` 0,66–0,86, `elliott_wave` 0,04–0,06) | Die drei Stufen sind das Argument des **Benchmarks** (`DD_Benchmark(f, e)`, Register 4.2): *„im Lauf gilt die mittlere Exposure des jeweiligen Parametersatzes in der jeweiligen Falte"*. Ein Bot hat je Falte **eine** Exposure — sie ist Ergebnis seiner Positionen, kein Regler. Sie auf 25/50/100 % zu setzen hiesse entweder andere Positionen (eine andere Kaskade, ein anderer Bot — der Auftrag verbietet das ausdrücklich: *„sonst misst du zwei verschiedene Bots"*) oder Hebel (ein Bot mit 5 % Exposure auf 100 % skaliert hätte 20-fache Positionen). Beides wäre eine erfundene Zahl |
| Schritt 3: *„Der Median über die Selektionsfalten je Bot, **das ist die Grösse, die zur `DD_Toleranz` führt**"* | Median von E und M über die Selektionsfalten mit Grundlage je Bot berichtet — neben den Faltenwerten, nie allein | `DD_Toleranz` ist nach Festlegung 5 der Median der **Benchmark**-Drawdowns über die Selektionsfalten, nicht der Bot-Drawdowns (Register 4.2, `benchmark.py`). Der Bot-Median führt zu keiner Grösse des Registers; er ist eine Beschreibung |
| Schritt 3: *„M darf nie flacher sein als E. Findest du einen Fall …, ist der Pfad falsch"* | Fünf Fälle gefunden, jeden zerlegt, keinen geglättet (Abschnitt 4) | Der Satz ist kein Satz der Rechnung — Probe 3 widerlegt ihn von Hand. Ein Pfad, der ihn erzwingt, ignoriert unrealisierte Gewinne |
| Schritt 2, Probe 1: *„E und M müssen gleich sein"* | 1a (ein Ausstieg je Tag): gleich. 1b (alle Positionen): E_tag = M, E tiefer | Mehrere Ausstieg je Zeitstempel geben E Zwischenstände, die kein Tagesraster hat — die Reihenfolge ist gesäter Zufall (`zuteilung.py`) |
| Abschnitt 1: *„Die Grundlage liegt vor"* | Für die Aktien-Bots ja. **Für die Krypto-Bots nicht vor 2021-09/2022-03** — 2020 Krypto ist nicht messbar | Datenstand der TB-24-Listen (Abschnitt 1) |
| Schritt 4: Nachtrag als **24.6** | so gemacht | — |

---

## 6. Was diese Untersuchung ausdrücklich NICHT tut

- ⛔ **Keine Empfehlung, keine Abwägung, kein Vorschlag.** Nicht in diesem
  Bericht, nicht im Register, nicht im Ergebnisdokument. Register 24.3.
- ⛔ **Kein Vergleich mit `erlaubt(f)`, `DD_Benchmark` oder `DD_Toleranz`.**
  `benchmark.py` wird nicht aufgerufen; keine Grenze steht neben einer
  Bot-Zahl. Eine Tabelle „besteht / besteht nicht" wäre genau die Zahl, die
  nach 24.3 nicht auf dem Tisch liegen soll.
- ⛔ Kein Laufcode (`K4j`), kein Sperrlisten-Vollzug, keine Änderung an
  `research/vorregistrierung/`, `shared/`, `strategies/`; TB-74 unberührt.
- ⛔ Keine neuen Trade-Listen für Krypto 2018–2020. Das wäre ein Backtest auf
  heutigen Daten, nicht die TB-24-Grundlage.
- Kein Zufalls-, Bootstrap- oder Signifikanztest auf die Differenzen. Die
  Frage der Aufgabe war *„wie gross"*, nicht *„ob zufällig"*.

---

## 7. Dateien, Aufruf, Laufzeiten (Nachweis 8)

| Datei | was sie tut |
|---|---|
| `mtm_kern.py` | reine Funktionen: Kurvenreihenfolge aus der Kapitalkette, Tagesraster, MtM-Pfad, Messung je Falte (mit importiertem `max_drawdown_ungerundet`) |
| `grundlage.py` | Schritt 1 — Bestandsaufnahme je Bot, `ergebnisse/grundlage.json` |
| `test_mtm_kern.py` | Schritt 2 — Proben 1a/1b/2/3, Gegenproben K1/K2 |
| `messung.py <bot>` | Schritt 3 — ein Bot je Prozess; `ergebnisse/<bot>.json`, `<bot>_tagespfad.csv` |
| `alle_bots.py` | neun Kindprozesse, `laufprotokoll.json`, ruft `auswertung.py` |
| `auswertung.py` | `ergebnisse/messung.md` (alle Tabellen), `zusammenfassung.json` |
| `richtungsfall.py` | jeden Fall „M flacher als E" zerlegt, `ergebnisse/richtungsfaelle.md` |

```bash
trading-env/bin/python3 research/mtm_drawdown/grundlage.py       # 27 s
trading-env/bin/python3 research/mtm_drawdown/test_mtm_kern.py   # 0,3 s, rc 0
trading-env/bin/python3 research/mtm_drawdown/alle_bots.py       # 19,3 s für neun Bots
trading-env/bin/python3 research/mtm_drawdown/richtungsfall.py   # ~10 s
```

Je Bot (`messung.py`, inkl. Import der Bot-Module): `elliott_wave` 0,8 s ·
`t3_supertrend` 0,8 · `rsi2_crypto` 0,8 · `turtle_soup_crypto` 0,8 ·
`volatility_breakout_crypto` 0,7 · `elliott_wave_stocks` 3,3 ·
`rsi2_mean_reversion` 4,0 · `turtle_soup_stocks` 4,3 · `volatility_breakout`
3,8 — Mac, `trading-env/bin/python3` 3.9.6, 20.09.2026. Braucht `pandas`,
`numpy`; die Bot-Module importieren `binance` (auf dem Mac in `trading-env`
vorhanden; `botenv.py` stellt Stubs, die nie aufgerufen werden).

---

## In einfacher Sprache

**Was gemessen wurde:** Wie tief jeder Bot in jedem Jahr gefallen ist — einmal
so, wie es heute gerechnet wird (nur an Kauf- und Verkaufstagen, offene
Positionen zählen zum Kaufpreis), und einmal so, wie es das Regelwerk seit
TB-71 verlangt (jeden Tag, offene Positionen zum Tageskurs).

**Was herauskam:** Die tägliche Messung zeigt fast immer einen tieferen Fall —
in 59 von 64 messbaren Jahren, meist um ein bis drei Prozentpunkte, in
einzelnen Jahren um bis zu acht. In fünf Jahren zeigt sie einen *flacheren*
Fall, weil der Bot zu diesem Zeitpunkt offene Positionen mit grossen
Buchgewinnen hatte, die die heutige Rechnung erst beim Verkauf sieht. Das ist
kein Rechenfehler, sondern die Eigenschaft der heutigen Rechnung.

**Was fehlt:** Für die fünf Krypto-Bots reichen die vorhandenen Handelslisten
nur bis Herbst 2021 zurück. Das Krisenjahr 2020 ist bei ihnen nicht messbar.
Das steht so in den Tabellen, statt dass eine Zahl geraten wurde.

**Was daraus folgt:** Nichts, das hier entschieden würde. Die Entscheidung,
täglich zu messen, ist gefallen, bevor diese Zahlen existierten — genau
damit sie sie nicht beeinflussen können. Die Zahlen werden berichtet und
abgelegt.

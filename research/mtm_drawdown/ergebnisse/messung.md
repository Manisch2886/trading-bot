# TB-73 — E gegen M, je Bot und je Falte (erzeugt von `auswertung.py`)

E = ereignisindizierter Drawdown (`capital_after` je Ausstieg, `shared/messkette.py`), E_tag = dieselbe Kurve am Tagesende (Erklärungshilfe), M = täglicher Mark-to-Market-Drawdown (offene Positionen zum Tagesschluss). Alle Werte in Prozent, negativ; M − E in Prozentpunkten (negativ = M tiefer). Falten aus `research/vorregistrierung/ergebnisse/faltenplan_tb72.json`. **Fett: die Falten mit 2020 und 2022.** Kein Wert steht ohne die Faltenwerte daneben; keine Grenze, kein Vergleich mit dem Benchmark (Register 24.3).

## Übersicht

| Bot | Selektionsfalten mit Grundlage | Median E | Median M | Median der Differenzen M−E | 2020: E → M | 2022: E → M | M flacher als E (Falten) |
|---|---|---:|---:|---:|---|---|---|
| `elliott_wave` | 3 von 4 | -4,51 | **-7,43** | -2,92 pp | 2020-2021 (ab 2021-09-22): -2,81 → **-4,48** (-1,67 pp, ×1,594) | 2022-2023: -10,17 → **-15,40** (-5,23 pp, ×1,514) | keine |
| `t3_supertrend` | 5 von 7 | -11,55 | **-11,25** | -3,09 pp | 2020: keine Grundlage | 2022: -12,28 → **-14,11** (-1,83 pp, ×1,149) | 2023 |
| `rsi2_crypto` | 4 von 7 | -10,04 | **-11,43** | -1,39 pp | 2020: keine Grundlage | 2022 (ab 2022-02-11): -8,65 → **-10,15** (-1,50 pp, ×1,173) | keine |
| `turtle_soup_crypto` | 5 von 8 | -20,68 | **-21,53** | -1,42 pp | 2020: keine Grundlage | 2022: -27,86 → **-30,38** (-2,52 pp, ×1,090) | keine |
| `volatility_breakout_crypto` | 4 von 8 | -9,48 | **-11,62** | -1,83 pp | 2020: keine Grundlage | 2022 (ab 2022-03-17): -6,07 → **-10,39** (-4,32 pp, ×1,712) | 2023 |
| `elliott_wave_stocks` | 9 von 9 | -4,85 | **-8,61** | -2,88 pp | 2020: -13,35 → **-9,45** (3,90 pp, ×0,708) | 2022: -19,31 → **-18,11** (1,20 pp, ×0,938) | 2020, 2022 |
| `rsi2_mean_reversion` | 8 von 8 | -7,57 | **-8,44** | -1,71 pp | 2020: -9,01 → **-11,28** (-2,27 pp, ×1,252) | 2022: -10,52 → **-11,93** (-1,41 pp, ×1,134) | keine |
| `turtle_soup_stocks` | 9 von 9 | -5,19 | **-7,42** | -2,53 pp | 2020: -29,91 → **-34,45** (-4,54 pp, ×1,152) | 2022: -18,73 → **-20,69** (-1,96 pp, ×1,105) | keine |
| `volatility_breakout` | 8 von 8 | -10,05 | **-12,34** | -1,60 pp | 2020: -9,41 → **-12,60** (-3,19 pp, ×1,339) | 2022: -23,97 → **-25,80** (-1,83 pp, ×1,076) | 2026 |

## Je Bot

### `elliott_wave` — 1h, krypto, 130 Positionen (2021-09-22 … 2026-08-20)

Kosten je Seite 0,15 % aus `backtest_elliott` (Abgleich mit der Liste: max 0.0050 pp, innerhalb der Rundung). Raster 3165 Tage (2018-01-01 … 2026-08-31), 0 fortgeschriebene Kurstage. Gesamter Zeitraum: E -10,17 % (`calculate_max_drawdown`), E_tag -10,17 %, M -15,40 %. Laufzeit 0.2 s.

| Falte | Rolle | Grundlage | Exposure Ø | E | E_tag | **M** | M − E | Faktor M/E | offen am Faltenbeginn | Ausstiege | Richtung |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2018-2019 | selektion | **keine** | — | — | — | — | — | — | — | 0 | — |
| **2020-2021** | selektion | teilweise, Liste ab 2021-09-22 | 0,062 | **-2,81** | -2,81 | **-4,48** | **-1,67 pp** | 1,594 | 0 | 8 | M ≤ E |
| **2022-2023** | selektion | vollständig | 0,036 | **-10,17** | -10,17 | **-15,40** | **-5,23 pp** | 1,514 | 0 | 43 | M ≤ E |
| 2024-2025 | selektion | vollständig | 0,049 | -4,51 | -4,51 | **-7,43** | -2,92 pp | 1,647 | 0 | 61 | M ≤ E |
| 2026-2027 | bestaetigung | vollständig | 0,046 | -3,11 | -3,11 | **-3,34** | -0,23 pp | 1,074 | 0 | 18 | M ≤ E |
| *Median über die Selektionsfalten mit Grundlage (3); letzte Spalte: Median der Differenzen* | | | | *-4,51* | *-4,51* | ***-7,43*** | *-2,92 pp* | | | | |

### `t3_supertrend` — 4h, krypto, 656 Positionen (2021-09-01 … 2026-08-29)

Kosten je Seite 0,15 % aus `backtest_trend` (Abgleich mit der Liste: max 0.0050 pp, innerhalb der Rundung). Raster 2800 Tage (2019-01-01 … 2026-08-31), 0 fortgeschriebene Kurstage. Gesamter Zeitraum: E -22,20 % (`calculate_max_drawdown`), E_tag -22,20 %, M -24,22 %. Laufzeit 0.3 s.

| Falte | Rolle | Grundlage | Exposure Ø | E | E_tag | **M** | M − E | Faktor M/E | offen am Faltenbeginn | Ausstiege | Richtung |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2019 | selektion | **keine** | — | — | — | — | — | — | — | 0 | — |
| **2020** | selektion | **keine** | — | — | — | — | — | — | — | 0 | — |
| 2021 | selektion | teilweise, Liste ab 2021-09-01 | 0,157 | -5,58 | -4,76 | **-8,67** | -3,09 pp | 1,554 | 0 | 43 | M ≤ E |
| **2022** | selektion | vollständig | 0,132 | **-12,28** | -12,28 | **-14,11** | **-1,83 pp** | 1,149 | 0 | 102 | M ≤ E |
| 2023 | selektion | vollständig | 0,185 | -11,55 | -11,55 | **-11,25** | 0,30 pp | 0,974 | 0 | 122 | ⚠️ M flacher als E |
| 2024 | selektion | vollständig | 0,231 | -6,20 | -6,09 | **-10,79** | -4,59 pp | 1,740 | 1 | 156 | M ≤ E |
| 2025 | selektion | vollständig | 0,161 | -16,41 | -16,41 | **-19,61** | -3,20 pp | 1,195 | 0 | 133 | M ≤ E |
| 2026 | bestaetigung | vollständig | 0,203 | -9,92 | -9,80 | **-11,79** | -1,87 pp | 1,189 | 3 | 100 | M ≤ E |
| *Median über die Selektionsfalten mit Grundlage (5); letzte Spalte: Median der Differenzen* | | | | *-11,55* | *-11,55* | ***-11,25*** | *-3,09 pp* | | | | |

### `rsi2_crypto` — 1d, krypto, 392 Positionen (2022-02-11 … 2026-08-20)

Kosten je Seite 0,15 % aus `backtest_rsi2` (Abgleich mit der Liste: max 0.0050 pp, innerhalb der Rundung). Raster 2800 Tage (2019-01-01 … 2026-08-31), 0 fortgeschriebene Kurstage. Gesamter Zeitraum: E -13,30 % (`calculate_max_drawdown`), E_tag -13,30 %, M -16,53 %. Laufzeit 0.2 s.

| Falte | Rolle | Grundlage | Exposure Ø | E | E_tag | **M** | M − E | Faktor M/E | offen am Faltenbeginn | Ausstiege | Richtung |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2019 | selektion | **keine** | — | — | — | — | — | — | — | 0 | — |
| **2020** | selektion | **keine** | — | — | — | — | — | — | — | 0 | — |
| 2021 | selektion | **keine** | — | — | — | — | — | — | — | 0 | — |
| **2022** | selektion | teilweise, Liste ab 2022-02-11 | 0,025 | **-8,65** | -8,65 | **-10,15** | **-1,50 pp** | 1,173 | 0 | 13 | M ≤ E |
| 2023 | selektion | vollständig | 0,110 | -2,75 | -2,74 | **-4,01** | -1,26 pp | 1,458 | 0 | 87 | M ≤ E |
| 2024 | selektion | vollständig | 0,206 | -13,30 | -13,30 | **-16,53** | -3,23 pp | 1,243 | 0 | 148 | M ≤ E |
| 2025 | selektion | vollständig | 0,169 | -11,43 | -11,38 | **-12,71** | -1,28 pp | 1,112 | 2 | 120 | M ≤ E |
| 2026 | bestaetigung | vollständig | 0,053 | -3,14 | -3,14 | **-4,28** | -1,14 pp | 1,363 | 0 | 24 | M ≤ E |
| *Median über die Selektionsfalten mit Grundlage (4); letzte Spalte: Median der Differenzen* | | | | *-10,04* | *-10,02* | ***-11,43*** | *-1,39 pp* | | | | |

### `turtle_soup_crypto` — 1d, krypto, 1414 Positionen (2021-10-12 … 2026-08-28)

Kosten je Seite 0,15 % aus `backtest_turtle_soup` (Abgleich mit der Liste: max 0.0050 pp, innerhalb der Rundung). Raster 3165 Tage (2018-01-01 … 2026-08-31), 0 fortgeschriebene Kurstage. Gesamter Zeitraum: E -32,40 % (`calculate_max_drawdown`), E_tag -32,40 %, M -38,94 %. Laufzeit 0.3 s.

| Falte | Rolle | Grundlage | Exposure Ø | E | E_tag | **M** | M − E | Faktor M/E | offen am Faltenbeginn | Ausstiege | Richtung |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2018 | selektion | **keine** | — | — | — | — | — | — | — | 0 | — |
| 2019 | selektion | **keine** | — | — | — | — | — | — | — | 0 | — |
| **2020** | selektion | **keine** | — | — | — | — | — | — | — | 0 | — |
| 2021 | selektion | teilweise, Liste ab 2021-10-12 | 0,403 | -15,29 | -15,29 | **-16,43** | -1,14 pp | 1,075 | 0 | 44 | M ≤ E |
| **2022** | selektion | vollständig | 0,415 | **-27,86** | -27,86 | **-30,38** | **-2,52 pp** | 1,090 | 4 | 260 | M ≤ E |
| 2023 | selektion | vollständig | 0,423 | -20,68 | -20,68 | **-21,53** | -0,85 pp | 1,041 | 7 | 239 | M ≤ E |
| 2024 | selektion | vollständig | 0,484 | -18,00 | -17,84 | **-19,42** | -1,42 pp | 1,079 | 1 | 285 | M ≤ E |
| 2025 | selektion | vollständig | 0,534 | -27,42 | -27,42 | **-35,29** | -7,87 pp | 1,287 | 0 | 340 | M ≤ E |
| 2026 | bestaetigung | vollständig | 0,551 | -16,03 | -15,90 | **-22,25** | -6,22 pp | 1,388 | 4 | 246 | M ≤ E |
| *Median über die Selektionsfalten mit Grundlage (5); letzte Spalte: Median der Differenzen* | | | | *-20,68* | *-20,68* | ***-21,53*** | *-1,42 pp* | | | | |

### `volatility_breakout_crypto` — 1d, krypto, 207 Positionen (2022-03-17 … 2026-08-30)

Kosten je Seite 0,15 % aus `backtest_breakout` (Abgleich mit der Liste: max 0.0049 pp, innerhalb der Rundung). Raster 3165 Tage (2018-01-01 … 2026-08-31), 0 fortgeschriebene Kurstage. Gesamter Zeitraum: E -16,29 % (`calculate_max_drawdown`), E_tag -16,29 %, M -19,30 %. Laufzeit 0.2 s.

| Falte | Rolle | Grundlage | Exposure Ø | E | E_tag | **M** | M − E | Faktor M/E | offen am Faltenbeginn | Ausstiege | Richtung |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2018 | selektion | **keine** | — | — | — | — | — | — | — | 0 | — |
| 2019 | selektion | **keine** | — | — | — | — | — | — | — | 0 | — |
| **2020** | selektion | **keine** | — | — | — | — | — | — | — | 0 | — |
| 2021 | selektion | **keine** | — | — | — | — | — | — | — | 0 | — |
| **2022** | selektion | teilweise, Liste ab 2022-03-17 | 0,054 | **-6,07** | -6,07 | **-10,39** | **-4,32 pp** | 1,712 | 0 | 19 | M ≤ E |
| 2023 | selektion | vollständig | 0,100 | -12,90 | -12,90 | **-12,84** | 0,06 pp | 0,995 | 0 | 48 | ⚠️ M flacher als E |
| 2024 | selektion | vollständig | 0,144 | -14,40 | -14,40 | **-15,42** | -1,02 pp | 1,071 | 0 | 67 | M ≤ E |
| 2025 | selektion | vollständig | 0,104 | -5,22 | -5,22 | **-7,86** | -2,64 pp | 1,506 | 0 | 34 | M ≤ E |
| 2026 | bestaetigung | vollständig | 0,141 | -7,27 | -7,27 | **-9,63** | -2,36 pp | 1,325 | 0 | 39 | M ≤ E |
| *Median über die Selektionsfalten mit Grundlage (4); letzte Spalte: Median der Differenzen* | | | | *-9,48* | *-9,48* | ***-11,62*** | *-1,83 pp* | | | | |

### `elliott_wave_stocks` — 1d, aktien, 395 Positionen (2016-10-28 … 2026-09-01)

Kosten je Seite 0,15 % aus `backtest_elliott` (Abgleich mit der Liste: max 0.0050 pp, innerhalb der Rundung). Raster 2473 Tage (2016-10-28 … 2026-09-01), 0 fortgeschriebene Kurstage. Gesamter Zeitraum: E -22,44 % (`calculate_max_drawdown`), E_tag -22,44 %, M -20,63 %. Laufzeit 2.8 s.

| Falte | Rolle | Grundlage | Exposure Ø | E | E_tag | **M** | M − E | Faktor M/E | offen am Faltenbeginn | Ausstiege | Richtung |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2017 | selektion | vollständig | 0,150 | -0,99 | -0,99 | **-5,26** | -4,27 pp | 5,313 | 1 | 10 | M ≤ E |
| 2018 | selektion | vollständig | 0,402 | -4,85 | -4,54 | **-9,22** | -4,37 pp | 1,901 | 0 | 43 | M ≤ E |
| 2019 | selektion | vollständig | 0,506 | -4,86 | -4,86 | **-8,61** | -3,75 pp | 1,772 | 6 | 32 | M ≤ E |
| **2020** | selektion | vollständig | 0,435 | **-13,35** | -13,35 | **-9,45** | **3,90 pp** | 0,708 | 1 | 60 | ⚠️ M flacher als E |
| 2021 | selektion | vollständig | 0,285 | -3,88 | -3,88 | **-5,34** | -1,46 pp | 1,376 | 4 | 26 | M ≤ E |
| **2022** | selektion | vollständig | 0,490 | **-19,31** | -19,31 | **-18,11** | **1,20 pp** | 0,938 | 4 | 82 | ⚠️ M flacher als E |
| 2023 | selektion | vollständig | 0,555 | -1,96 | -1,96 | **-4,53** | -2,57 pp | 2,311 | 7 | 31 | M ≤ E |
| 2024 | selektion | vollständig | 0,243 | -3,26 | -3,26 | **-6,14** | -2,88 pp | 1,883 | 8 | 21 | M ≤ E |
| 2025 | selektion | vollständig | 0,520 | -8,92 | -8,92 | **-11,91** | -2,99 pp | 1,335 | 1 | 44 | M ≤ E |
| 2026 | bestaetigung | vollständig | 0,594 | -5,74 | -5,74 | **-11,71** | -5,97 pp | 2,040 | 7 | 38 | M ≤ E |
| *Median über die Selektionsfalten mit Grundlage (9); letzte Spalte: Median der Differenzen* | | | | *-4,85* | *-4,54* | ***-8,61*** | *-2,88 pp* | | | | |

### `rsi2_mean_reversion` — 1d, aktien, 4232 Positionen (2016-09-01 … 2026-09-01)

Kosten je Seite 0,15 % aus `backtest_rsi2` (Abgleich mit der Liste: max 0.0050 pp, innerhalb der Rundung). Raster 2513 Tage (2016-09-01 … 2026-09-01), 0 fortgeschriebene Kurstage. Gesamter Zeitraum: E -21,05 % (`calculate_max_drawdown`), E_tag -21,05 %, M -23,39 %. Laufzeit 3.5 s.

| Falte | Rolle | Grundlage | Exposure Ø | E | E_tag | **M** | M − E | Faktor M/E | offen am Faltenbeginn | Ausstiege | Richtung |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2018 | selektion | vollständig | 0,370 | -11,49 | -11,49 | **-14,92** | -3,43 pp | 1,299 | 8 | 385 | M ≤ E |
| 2019 | selektion | vollständig | 0,318 | -6,46 | -6,39 | **-7,66** | -1,20 pp | 1,186 | 0 | 357 | M ≤ E |
| **2020** | selektion | vollständig | 0,300 | **-9,01** | -9,01 | **-11,28** | **-2,27 pp** | 1,252 | 8 | 326 | M ≤ E |
| 2021 | selektion | vollständig | 0,440 | -3,53 | -3,53 | **-5,53** | -2,00 pp | 1,567 | 3 | 493 | M ≤ E |
| **2022** | selektion | vollständig | 0,295 | **-10,52** | -10,49 | **-11,93** | **-1,41 pp** | 1,134 | 1 | 288 | M ≤ E |
| 2023 | selektion | vollständig | 0,413 | -8,69 | -8,60 | **-9,21** | -0,52 pp | 1,060 | 1 | 425 | M ≤ E |
| 2024 | selektion | vollständig | 0,463 | -4,45 | -4,19 | **-5,48** | -1,03 pp | 1,231 | 1 | 522 | M ≤ E |
| 2025 | selektion | vollständig | 0,397 | -5,33 | -4,88 | **-7,49** | -2,16 pp | 1,405 | 5 | 429 | M ≤ E |
| 2026 | bestaetigung | vollständig | 0,440 | -3,84 | -3,79 | **-5,51** | -1,67 pp | 1,435 | 19 | 341 | M ≤ E |
| *Median über die Selektionsfalten mit Grundlage (8); letzte Spalte: Median der Differenzen* | | | | *-7,57* | *-7,49* | ***-8,44*** | *-1,71 pp* | | | | |

### `turtle_soup_stocks` — 1d, aktien, 8915 Positionen (2016-09-01 … 2026-09-01)

Kosten je Seite 0,15 % aus `backtest_turtle_soup` (Abgleich mit der Liste: max 0.0050 pp, innerhalb der Rundung). Raster 2513 Tage (2016-09-01 … 2026-09-01), 0 fortgeschriebene Kurstage. Gesamter Zeitraum: E -29,91 % (`calculate_max_drawdown`), E_tag -29,83 %, M -34,45 %. Laufzeit 3.7 s.

| Falte | Rolle | Grundlage | Exposure Ø | E | E_tag | **M** | M − E | Faktor M/E | offen am Faltenbeginn | Ausstiege | Richtung |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2017 | selektion | vollständig | 0,783 | -1,26 | -1,13 | **-2,42** | -1,16 pp | 1,921 | 45 | 922 | M ≤ E |
| 2018 | selektion | vollständig | 0,748 | -12,15 | -12,03 | **-14,93** | -2,78 pp | 1,229 | 37 | 872 | M ≤ E |
| 2019 | selektion | vollständig | 0,667 | -4,74 | -4,74 | **-6,86** | -2,12 pp | 1,447 | 47 | 810 | M ≤ E |
| **2020** | selektion | vollständig | 0,663 | **-29,91** | -29,83 | **-34,45** | **-4,54 pp** | 1,152 | 24 | 775 | M ≤ E |
| 2021 | selektion | vollständig | 0,782 | -3,30 | -3,18 | **-6,39** | -3,09 pp | 1,936 | 30 | 918 | M ≤ E |
| **2022** | selektion | vollständig | 0,736 | **-18,73** | -18,71 | **-20,69** | **-1,96 pp** | 1,105 | 27 | 858 | M ≤ E |
| 2023 | selektion | vollständig | 0,777 | -4,54 | -4,49 | **-7,07** | -2,53 pp | 1,557 | 34 | 923 | M ≤ E |
| 2024 | selektion | vollständig | 0,792 | -5,19 | -5,11 | **-7,42** | -2,23 pp | 1,430 | 18 | 929 | M ≤ E |
| 2025 | selektion | vollständig | 0,811 | -12,02 | -11,99 | **-18,74** | -6,72 pp | 1,559 | 32 | 952 | M ≤ E |
| 2026 | bestaetigung | vollständig | 0,860 | -3,81 | -3,77 | **-6,24** | -2,43 pp | 1,638 | 23 | 679 | M ≤ E |
| *Median über die Selektionsfalten mit Grundlage (9); letzte Spalte: Median der Differenzen* | | | | *-5,19* | *-5,11* | ***-7,42*** | *-2,53 pp* | | | | |

### `volatility_breakout` — 1d, aktien, 1454 Positionen (2016-09-01 … 2026-09-01)

Kosten je Seite 0,15 % aus `backtest_breakout` (Abgleich mit der Liste: max 0.0050 pp, innerhalb der Rundung). Raster 2513 Tage (2016-09-01 … 2026-09-01), 0 fortgeschriebene Kurstage. Gesamter Zeitraum: E -23,97 % (`calculate_max_drawdown`), E_tag -23,97 %, M -25,80 %. Laufzeit 3.3 s.

| Falte | Rolle | Grundlage | Exposure Ø | E | E_tag | **M** | M − E | Faktor M/E | offen am Faltenbeginn | Ausstiege | Richtung |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2018 | selektion | vollständig | 0,700 | -14,78 | -14,78 | **-15,36** | -0,58 pp | 1,039 | 10 | 131 | M ≤ E |
| 2019 | selektion | vollständig | 0,857 | -7,85 | -7,60 | **-9,05** | -1,20 pp | 1,153 | 1 | 144 | M ≤ E |
| **2020** | selektion | vollständig | 0,677 | **-9,41** | -8,45 | **-12,60** | **-3,19 pp** | 1,339 | 9 | 119 | M ≤ E |
| 2021 | selektion | vollständig | 0,907 | -3,38 | -3,38 | **-5,55** | -2,17 pp | 1,642 | 10 | 155 | M ≤ E |
| **2022** | selektion | vollständig | 0,705 | **-23,97** | -23,97 | **-25,80** | **-1,83 pp** | 1,076 | 7 | 140 | M ≤ E |
| 2023 | selektion | vollständig | 0,901 | -10,70 | -10,70 | **-12,08** | -1,38 pp | 1,129 | 6 | 157 | M ≤ E |
| 2024 | selektion | vollständig | 0,912 | -5,39 | -5,39 | **-6,15** | -0,76 pp | 1,141 | 5 | 160 | M ≤ E |
| 2025 | selektion | vollständig | 0,814 | -12,31 | -12,31 | **-15,36** | -3,05 pp | 1,248 | 6 | 145 | M ≤ E |
| 2026 | bestaetigung | vollständig | 0,812 | -4,90 | -4,90 | **-4,37** | 0,53 pp | 0,892 | 5 | 101 | ⚠️ M flacher als E |
| *Median über die Selektionsfalten mit Grundlage (8); letzte Spalte: Median der Differenzen* | | | | *-10,05* | *-9,57* | ***-12,34*** | *-1,60 pp* | | | | |

## Richtungsprobe — Falten, in denen M flacher ist als E

| Bot | Falte | Rolle | E | E_tag | M | M − E | Mechanismus (gemessen) |
|---|---|---|---:|---:|---:|---:|---|
| `t3_supertrend` | 2023 | selektion | -11,55 | -11,55 | -11,25 | 0,30 pp | Bewertung: M flacher als E_tag (Probe 3 — unrealisierter Gewinn hebt Hoch- und Tiefpunkt) |
| `volatility_breakout_crypto` | 2023 | selektion | -12,90 | -12,90 | -12,84 | 0,06 pp | Bewertung: M flacher als E_tag (Probe 3 — unrealisierter Gewinn hebt Hoch- und Tiefpunkt) |
| `elliott_wave_stocks` | 2020 | selektion | -13,35 | -13,35 | -9,45 | 3,90 pp | Bewertung: M flacher als E_tag (Probe 3 — unrealisierter Gewinn hebt Hoch- und Tiefpunkt) |
| `elliott_wave_stocks` | 2022 | selektion | -19,31 | -19,31 | -18,11 | 1,20 pp | Bewertung: M flacher als E_tag (Probe 3 — unrealisierter Gewinn hebt Hoch- und Tiefpunkt) |
| `volatility_breakout` | 2026 | bestaetigung | -4,90 | -4,90 | -4,37 | 0,53 pp | Bewertung: M flacher als E_tag (Probe 3 — unrealisierter Gewinn hebt Hoch- und Tiefpunkt) |

## Laufzeiten

| Bot | Positionen | Rastertage | Laufzeit `messung.py` |
|---|---:|---:|---:|
| `elliott_wave` | 130 | 3165 | 0.2 s |
| `t3_supertrend` | 656 | 2800 | 0.3 s |
| `rsi2_crypto` | 392 | 2800 | 0.2 s |
| `turtle_soup_crypto` | 1414 | 3165 | 0.3 s |
| `volatility_breakout_crypto` | 207 | 3165 | 0.2 s |
| `elliott_wave_stocks` | 395 | 2473 | 2.8 s |
| `rsi2_mean_reversion` | 4232 | 2513 | 3.5 s |
| `turtle_soup_stocks` | 8915 | 2513 | 3.7 s |
| `volatility_breakout` | 1454 | 2513 | 3.3 s |

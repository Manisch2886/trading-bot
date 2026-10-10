# TB-148 Leseprotokoll

Jede gelesene Datei mit gelesenem Zeilenbereich und Messpunkt. Gelesen mit dem Lesewerkzeug von Claude Code. Das Suchwerkzeug (Grep) stand in dieser Sitzung nicht zur Verfügung (Antwort des Werkzeugs: „No such tool available: Grep. Grep is not available in this session“); gesucht wurde deshalb nicht, sondern gelesen. Zeilen (`wc -l`) und md5 je Datei aus den zwei Blöcken von D0 (`lese_zeilen.txt`, `lese_md5.txt`, je Schlusszeile `rc 0`); „ganz“ heisst: bis zur letzten Zeile gelesen.

## Gelesene Dateien

| Datei | Zeilenbereich | Messpunkt | Zeilen | md5 |
|---|---|---|---:|---|
| `shared/zuteilung.py` | 1–798 (ganz) | M1 (auch M2, M3) | 798 | `ecb2af91a29577914b052feb5574e279` |
| `strategies/elliott_wave/equity_simulation.py` | 1–195 (ganz) | M1 (auch M3, M4) | 195 | `d420d096e9e14832816ca055cfcb39cd` |
| `strategies/t3_supertrend/equity_simulation.py` | 25–139 | M1 (auch M3, M4) | 187 | `e65e06cef898272187138cd84467b7c5` |
| `strategies/rsi2_crypto/equity_simulation.py` | 25–134 | M1 (auch M3, M4) | 177 | `62a78c697cb30ccd18d44605083ec137` |
| `strategies/turtle_soup_crypto/equity_simulation.py` | 25–119 | M1 (auch M3, M4) | 160 | `a2ac6fa97c8d9eadf072b36054dd2ad7` |
| `strategies/volatility_breakout_crypto/equity_simulation.py` | 1–170 | M1 (auch M3, M4) | 227 | `91d6568fc034dec82b32dbb29af07096` |
| `strategies/elliott_wave_stocks/equity_simulation.py` | 1–165 | M1 (auch M3, M4) | 235 | `9f0fe8aa04224cfcffadbcdd08d1fa0c` |
| `strategies/rsi2_mean_reversion/equity_simulation.py` | 1–165 | M1 (auch M3, M4) | 212 | `774e7fecad93bdad38bcba5e568b7243` |
| `strategies/turtle_soup_stocks/equity_simulation.py` | 1–150 | M1 (auch M3, M4) | 199 | `f45e55aadcb9d03b4342ec32e8644914` |
| `strategies/volatility_breakout/equity_simulation.py` | 1–150 | M1 (auch M3, M4) | 200 | `dd5fa96bb927aecb26051fbaefb4a0cd` |
| `research/vorregistrierung/registerdaten.py` | 80–144 | M2 | 633 | `b1df43ac7b4408dcf8780bb44c97110f` |
| `research/faltenplan_neun/faltenplan_neun.py` | 80–484; 555–629 | M2 (auch M4) | 634 | `329f671da5b7cd6d6179b22a16c59537` |
| `research/vorregistrierung/faltenplan.py` | 1–490 | M2 | 491 | `27c2d93577227a0199e266dbee7097cd` |
| `research/faltenplan_neun/erste_falte_trockenlauf.py` | 1–331 (ganz) | M2 | 331 | `fb320cfc5c1380d322d91349f97102a1` |
| `research/faltenplan_neun/faltenschranke_messung.py` | 1–533 (ganz) | M2 (auch M4, M5) | 533 | `6a72fd8833290860b9dad8929782cd38` |
| `research/vorregistrierung/registerbericht.py` | 115–154 | M2 | 218 | `dcc23096e84558c357cac6ca52667737` |
| `research/universum_trockenlauf/universum_trockenlauf.py` (weitere Datei, Aufruf aus `erste_falte_trockenlauf.py` Z. 85, 94) | 1–400 | M2 | 810 | `923ef7758c349cd8903f464758d8b09d` |
| `research/universum_trockenlauf/loaderlauf.py` (weitere Datei, Aufruf aus `universum_trockenlauf.py` Z. 318) | 1–645 (ganz) | M2 | 645 | `5032ace22ceb41efda2460a0b22026ea` |
| `strategies/elliott_wave/multi_symbol_optimise.py` | 1–120 | M2 (auch M4) | 242 | `dc458cde8374d1a7d05c74ca81444484` |
| `strategies/t3_supertrend/multi_symbol_optimise.py` | 1–105 | M2 (auch M4) | 239 | `bd9259fcbb4357663d1759d11aa5e9d6` |
| `strategies/rsi2_crypto/multi_symbol_optimise.py` | 1–105 | M2 (auch M4) | 193 | `d4fdbd57a35f95babbd5127ff24d896a` |
| `strategies/turtle_soup_crypto/multi_symbol_optimise.py` | 1–85 | M2 (auch M4) | 167 | `442032ab0eb268e2b9b7f21b9be9815d` |
| `strategies/volatility_breakout_crypto/multi_symbol_optimise.py` | 1–96 | M2 (auch M4) | 179 | `4f32fc9e0396c6adbffd6067dea16202` |
| `strategies/elliott_wave_stocks/multi_symbol_optimise.py` | 1–130 | M2 (auch M4) | 267 | `32aabbda9d3a4fbc297ea7bb423a5152` |
| `strategies/rsi2_mean_reversion/multi_symbol_optimise.py` | 1–115 | M2 (auch M4) | 218 | `57ab12ab0a357bfb1a5c0241071ccc1e` |
| `strategies/turtle_soup_stocks/multi_symbol_optimise.py` | 1–95 | M2 (auch M4) | 179 | `77cfcfe57c391b5ff626a5ad56fb317a` |
| `strategies/volatility_breakout/multi_symbol_optimise.py` | 1–112 | M2 (auch M4) | 214 | `66ce8cc780e7277e155f4a2f003e3896` |
| `shared/fetch_binance_data.py` | 85–129; 300–349 | M2 | 384 | `528f59408a99ead52ffb4e9524693b79` |
| `shared/binance_historie.py` | 90–109; 260–339; 475–599 | M2 | 830 | `8cbad1fe58ca908e90578c930b93ae1b` |
| `strategies/elliott_wave_stocks/fetch_stock_data.py` | 1–147 (ganz) | M2 | 147 | `46f4fe6fedf830aebea6a55a9bf08fe0` |
| `shared/abrufschutz.py` | 1–230 | M2 | 574 | `f8f7c5c470b81eabd103f3819c31ac67` |
| `shared/kursdaten.py` | 1–170 | M2 (auch M4) | 189 | `764318a64279c9a28e09beae0ed0da10` |
| `strategies/elliott_wave/backtest_elliott.py` | 1–215 | M2 (auch M3, M4) | 230 | `df5c314e9268bf5c51a5210113e27082` |
| `strategies/t3_supertrend/backtest_trend.py` | 1–140 | M2 (auch M3, M4) | 159 | `689d648d2599d2e54eb77dca26ced888` |
| `strategies/rsi2_crypto/backtest_rsi2.py` | 55–154 | M2 (auch M3, M4) | 156 | `35929d647c8b62ca7d59ec6e79120b37` |
| `strategies/turtle_soup_crypto/backtest_turtle_soup.py` | 95–194 | M2 (auch M3, M4) | 201 | `9ed99ea5d2fe16f9aed85b51752613a4` |
| `strategies/volatility_breakout_crypto/backtest_breakout.py` | 60–199 | M2 (auch M3, M4) | 203 | `4dcc955886faecf61c138e74506f7237` |
| `strategies/elliott_wave_stocks/backtest_elliott.py` | 60–179 | M2 (auch M3, M4) | 242 | `f1979557a945822dfbe623e0d80ca531` |
| `strategies/rsi2_mean_reversion/backtest_rsi2.py` | 90–184 | M2 (auch M3, M4) | 199 | `1fb6254c25aa2b169c3444b891842af5` |
| `strategies/turtle_soup_stocks/backtest_turtle_soup.py` | 95–179 | M2 (auch M3, M4) | 197 | `14f1c0f899975d196907b6579ad09dab` |
| `strategies/volatility_breakout/backtest_breakout.py` | 110–239 | M2 (auch M3, M4) | 244 | `8453b945e83ffe400d80ada6bff0ff2d` |
| `strategies/elliott_wave/multi_symbol_walk_forward.py` | 38–57 | M2 | 107 | `cd62a4af8a07f097f9952661dd07fea8` |
| `strategies/t3_supertrend/multi_symbol_walk_forward.py` | 34–51 | M2 | 90 | `8cb107ed60f5772dc6ec51d052be52d5` |
| `strategies/rsi2_crypto/multi_symbol_walk_forward.py` | 1–60 | M2 | 157 | `25f79142a9e28848df2e1a116ab9436c` |
| `strategies/turtle_soup_crypto/multi_symbol_walk_forward.py` | 14–31 | M2 | 138 | `22efed0c3b0d15f37f737b639b63884e` |
| `strategies/volatility_breakout_crypto/multi_symbol_walk_forward.py` | 1–50 | M2 | 142 | `13222d1647e90347bcb4da942abaece1` |
| `strategies/elliott_wave_stocks/multi_symbol_walk_forward.py` | 38–57 | M2 | 109 | `4f22493439d1d1b884e68ec2e4b81ac8` |
| `strategies/rsi2_mean_reversion/multi_symbol_walk_forward.py` | 1–70 | M2 | 168 | `19355e0d57c3b24e581c67f863ad7c40` |
| `strategies/turtle_soup_stocks/multi_symbol_walk_forward.py` | 14–31 | M2 | 138 | `edb6f88ed1a9e185414829b814816423` |
| `strategies/volatility_breakout/multi_symbol_walk_forward.py` | 1–60 | M2 | 153 | `0ab5fc0cd110e6181651fd34fd2baa1a` |
| `strategies/t3_supertrend/regime_filter.py` | 1–47 (ganz) | M2 (auch M3, M4) | 47 | `b02087926d7d6b376a47b19115f1ca58` |
| `strategies/volatility_breakout_crypto/regime_filter.py` | 1–43 (ganz) | M2 (auch M3, M4) | 43 | `9de449f6a4a63d73efafc9126a2c5145` |
| `strategies/rsi2_crypto/indicators.py` | 80–101 | M2 | 101 | `a34eb5905969d19827b0f93b6b154132` |
| `strategies/volatility_breakout_crypto/indicators.py` | 68–88 | M2 | 88 | `f44634e6226adaea67646de28903a012` |
| `strategies/elliott_wave/zigzag_indicator.py` | 25–214 | M2 (auch M4) | 216 | `6e9a91ccc131937079b602be875fa0dd` |
| `strategies/elliott_wave_stocks/zigzag_indicator.py` | 36–43; 132–137; 204–208 | M2 (auch M4) | 216 | `407cd69fb5c2181c5316e008ea7b7d81` |
| `research/vorregistrierung/benchmark.py` | 1–460 | M2 (auch M4, M5) | 463 | `6ca4ede617165d881623465244649c1d` |
| `research/mtm_drawdown/mtm_kern.py` | 1–135 | M3 | 339 | `fcf7a1ef7585d1ec78247031851fa85e` |
| `research/mtm_drawdown/grundlage.py` | 1–214 | M3 | 272 | `81cf1c93243a8248b96cf072e07fc289` |
| `research/mtm_drawdown/messung.py` | 60–159 | M3 | 240 | `00eb23079f1b92532f48f099f74dbe2f` |
| `research/mtm_drawdown/richtungsfall.py` | 50–79 | M3 | 150 | `77a7c08dc6094818d01d0667a9ccf4ab` |
| `research/mtm_drawdown/test_mtm_kern.py` | 30–109; 220–244 | M3 | 264 | `80f1511a18d26a61537748c2739d0d79` |
| `strategies/elliott_wave/elliott_wave_counter.py` (weitere Datei, importiert von `elliott_wave/multi_symbol_optimise.py` Z. 36) | 1–381 (ganz) | M4 | 381 | `e483aad3e62483cb6f730f255b0ae12e` |
| `strategies/elliott_wave_stocks/elliott_wave_counter.py` (weitere Datei, importiert von `elliott_wave_stocks/multi_symbol_optimise.py` Z. 36) | 160–189; 305–374 | M4 | 381 | `b5dcf72fa38abc7c4ddeeb8f3a84b42f` |
| `research/exposure_messung/exposure_kern.py` | 195–226 | M5 | 228 | `5d182d05464fea15cef5c40211eba45b` |
| `research/exposure_messung/auswertung.py` | 420–479 | M5 | 561 | `bf011dee838beb9c8b770ed85fa6c0dd` |
| `research/exposure_messung/test_exposure_kern.py` | 135–154 | M5 | 161 | `68bec9c679926e97136e2a87ec643f39` |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-10-09a_beitrag_aus_r45_listen_geschnitten_handelbar_tag.md` (weitere Datei: Quelle der Fragen M3–M5 und von R87 (a), (b)) | 195–233 | M3, M4, M5 | 233 | `a6e5d3d277c5d4069b443a8f8f9df17f` |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` (Steuerdatei, vor Schritt 0) | 1–98 (ganz) | — | 98 | `8f0a1160a0db9c0faab59f8e486a4c1d` |
| `docs/auftraege/MAC_TB-148_verfahrensmessung_schluessel_zeitzone_handelbar.md` (Auftrag, vor Schritt 0) | 1–373 (ganz) | — | 373 | `9c14bb54a59170893d316ac22af29e3e` |

Von den 63 Startdateien wurden alle 63 geöffnet; dazu 7 weitere Dateien (in der Tabelle als „weitere Datei“, „Steuerdatei“ oder „Auftrag“ gekennzeichnet), zusammen 70, wie in beiden Blöcken von D0.

## Vermerke

- `shared/zuteilung.py:18`–`19` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `shared/zuteilung.py:112` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `shared/zuteilung.py:151` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `shared/zuteilung.py:490` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `shared/zuteilung.py:589`–`591` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `shared/zuteilung.py:597` — Ergebniszahl im Quelltext, nicht wiedergegeben (Rechenzeit eines Laufs)
- `strategies/elliott_wave/equity_simulation.py:103`–`104` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `strategies/t3_supertrend/equity_simulation.py:50` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `strategies/rsi2_crypto/equity_simulation.py:91` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `strategies/turtle_soup_crypto/equity_simulation.py:78` — Ergebniszahl im Quelltext, nicht wiedergegeben (Kursspanne)
- `strategies/elliott_wave_stocks/equity_simulation.py:125`–`127` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `strategies/rsi2_mean_reversion/equity_simulation.py:119`–`127` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `strategies/turtle_soup_stocks/equity_simulation.py:57` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `research/faltenplan_neun/faltenplan_neun.py:92`–`93` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `research/vorregistrierung/faltenplan.py:38`–`41`, `55`–`59` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `research/universum_trockenlauf/universum_trockenlauf.py:20`, `25`–`26` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `shared/abrufschutz.py:20` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `shared/kursdaten.py:15`–`16`, `21`–`22` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `strategies/elliott_wave/backtest_elliott.py:26` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `research/vorregistrierung/benchmark.py:38`, `43`–`46`, `58` — Ergebniszahl im Quelltext, nicht wiedergegeben
- `strategies/elliott_wave/elliott_wave_counter.py:34`–`35`, `41`–`43`, `61`, `223` — Ergebniszahl im Quelltext, nicht wiedergegeben
- Parameterwerte in Kommentaren der Backtest-Module, nicht wiedergegeben: `strategies/elliott_wave/backtest_elliott.py:51`; `strategies/t3_supertrend/backtest_trend.py:37`–`39`; `strategies/turtle_soup_crypto/backtest_turtle_soup.py:97`–`98`; `strategies/volatility_breakout_crypto/backtest_breakout.py:103`; `strategies/volatility_breakout/backtest_breakout.py:140`
- Parameterwerte in Kommentaren (Werte aus oder gegen `live_params.py`), nicht wiedergegeben: `strategies/elliott_wave/equity_simulation.py:58`; `strategies/volatility_breakout_crypto/equity_simulation.py:5`; `strategies/elliott_wave_stocks/equity_simulation.py:65`; `strategies/rsi2_mean_reversion/equity_simulation.py:46`–`47`, `53`, `63`; `strategies/turtle_soup_stocks/equity_simulation.py:6`–`8`, `46`–`47`, `61`, `69`; `strategies/volatility_breakout/equity_simulation.py:41`, `51`, `62`; `strategies/rsi2_crypto/equity_simulation.py:52`; `strategies/turtle_soup_crypto/equity_simulation.py:46`; `strategies/volatility_breakout_crypto/equity_simulation.py:62`; `strategies/t3_supertrend/equity_simulation.py:49`

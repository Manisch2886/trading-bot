# TB-148 Leseprotokoll

Jede gelesene Datei mit gelesenem Zeilenbereich und Messpunkt. Gelesen mit dem Lesewerkzeug von Claude Code. Das Suchwerkzeug (Grep) stand in dieser Sitzung nicht zur Verfügung (Antwort des Werkzeugs: „No such tool available: Grep. Grep is not available in this session“); gesucht wurde deshalb nicht, sondern gelesen. Zeilen und md5 je Datei: siehe Schluss (D0).

Gelesen wurden ausserdem, vor M1, die Steuerdateien `docs/auftraege/AKTUELLER_AUFTRAG.md` (ganz) und der Auftrag `docs/auftraege/MAC_TB-148_verfahrensmessung_schluessel_zeitzone_handelbar.md` (ganz).

## Gelesene Dateien

| Datei | Zeilenbereich | Messpunkt |
|---|---|---|
| `shared/zuteilung.py` | 1–799 (ganz) | M1 (auch M2, M3) |
| `strategies/elliott_wave/equity_simulation.py` | 1–196 (ganz) | M1 (auch M3) |
| `strategies/t3_supertrend/equity_simulation.py` | 25–139 | M1 (auch M3) |
| `strategies/rsi2_crypto/equity_simulation.py` | 25–134 | M1 (auch M3) |
| `strategies/turtle_soup_crypto/equity_simulation.py` | 25–119 | M1 (auch M3) |
| `strategies/volatility_breakout_crypto/equity_simulation.py` | 1–170 | M1 (auch M3) |
| `strategies/elliott_wave_stocks/equity_simulation.py` | 1–165 | M1 (auch M3) |
| `strategies/rsi2_mean_reversion/equity_simulation.py` | 1–165 | M1 (auch M3) |
| `strategies/turtle_soup_stocks/equity_simulation.py` | 1–150 | M1 (auch M3) |
| `strategies/volatility_breakout/equity_simulation.py` | 1–150 | M1 (auch M3) |
| `research/vorregistrierung/registerdaten.py` | 80–144 | M2 |
| `research/faltenplan_neun/faltenplan_neun.py` | 80–484; 555–629 | M2 (auch M4) |
| `research/vorregistrierung/faltenplan.py` | 1–490 | M2 |
| `research/faltenplan_neun/erste_falte_trockenlauf.py` | 1–332 (ganz) | M2 |
| `research/faltenplan_neun/faltenschranke_messung.py` | 1–534 (ganz) | M2 (auch M4, M5) |
| `research/vorregistrierung/registerbericht.py` | 115–154 | M2 |
| `research/universum_trockenlauf/universum_trockenlauf.py` (weitere Datei, Aufruf aus `erste_falte_trockenlauf.py` Z. 85, 94) | 1–400 | M2 |
| `research/universum_trockenlauf/loaderlauf.py` (weitere Datei, Aufruf aus `universum_trockenlauf.py` Z. 318) | 1–646 (ganz) | M2 |
| `strategies/elliott_wave/multi_symbol_optimise.py` | 1–120 | M2 (auch M3, M4) |
| `strategies/t3_supertrend/multi_symbol_optimise.py` | 1–105 | M2 (auch M3, M4) |
| `strategies/rsi2_crypto/multi_symbol_optimise.py` | 1–105 | M2 (auch M3, M4) |
| `strategies/turtle_soup_crypto/multi_symbol_optimise.py` | 1–85 | M2 (auch M3, M4) |
| `strategies/volatility_breakout_crypto/multi_symbol_optimise.py` | 1–96 | M2 (auch M3, M4) |
| `strategies/elliott_wave_stocks/multi_symbol_optimise.py` | 1–130 | M2 (auch M3, M4) |
| `strategies/rsi2_mean_reversion/multi_symbol_optimise.py` | 1–115 | M2 (auch M3, M4) |
| `strategies/turtle_soup_stocks/multi_symbol_optimise.py` | 1–95 | M2 (auch M3, M4) |
| `strategies/volatility_breakout/multi_symbol_optimise.py` | 1–112 (ganz) | M2 (auch M3, M4) |
| `shared/fetch_binance_data.py` | 85–129; 300–349 | M2 |
| `shared/binance_historie.py` | 90–109; 260–339; 475–599 | M2 |
| `strategies/elliott_wave_stocks/fetch_stock_data.py` | 1–148 (ganz) | M2 |
| `shared/abrufschutz.py` | 1–230 | M2 |
| `shared/kursdaten.py` | 1–170 | M2 (auch M4) |
| `strategies/elliott_wave/backtest_elliott.py` | 1–215 | M2 (auch M3, M4) |
| `strategies/t3_supertrend/backtest_trend.py` | 1–140 | M2 (auch M3, M4) |
| `strategies/rsi2_crypto/backtest_rsi2.py` | 55–154 | M2 (auch M3, M4) |
| `strategies/turtle_soup_crypto/backtest_turtle_soup.py` | 95–194 | M2 (auch M3, M4) |
| `strategies/volatility_breakout_crypto/backtest_breakout.py` | 60–199 | M2 (auch M3, M4) |
| `strategies/elliott_wave_stocks/backtest_elliott.py` | 60–179 | M2 (auch M3, M4) |
| `strategies/rsi2_mean_reversion/backtest_rsi2.py` | 90–184 | M2 (auch M3, M4) |
| `strategies/turtle_soup_stocks/backtest_turtle_soup.py` | 95–179 | M2 (auch M3, M4) |
| `strategies/volatility_breakout/backtest_breakout.py` | 110–239 | M2 (auch M3, M4) |
| `strategies/elliott_wave/multi_symbol_walk_forward.py` | 38–57 | M2 |
| `strategies/t3_supertrend/multi_symbol_walk_forward.py` | 34–51 | M2 |
| `strategies/rsi2_crypto/multi_symbol_walk_forward.py` | 1–60 | M2 (auch M4) |
| `strategies/turtle_soup_crypto/multi_symbol_walk_forward.py` | 14–31 | M2 |
| `strategies/volatility_breakout_crypto/multi_symbol_walk_forward.py` | 1–50 | M2 (auch M4) |
| `strategies/elliott_wave_stocks/multi_symbol_walk_forward.py` | 38–57 | M2 |
| `strategies/rsi2_mean_reversion/multi_symbol_walk_forward.py` | 1–70 | M2 (auch M4) |
| `strategies/turtle_soup_stocks/multi_symbol_walk_forward.py` | 14–31 | M2 |
| `strategies/volatility_breakout/multi_symbol_walk_forward.py` | 1–60 | M2 (auch M4) |
| `strategies/t3_supertrend/regime_filter.py` | 1–48 (ganz) | M2 (auch M3) |
| `strategies/volatility_breakout_crypto/regime_filter.py` | 1–44 (ganz) | M2 (auch M3) |
| `strategies/rsi2_crypto/indicators.py` | 80–102 | M2 |
| `strategies/volatility_breakout_crypto/indicators.py` | 68–89 | M2 |
| `strategies/elliott_wave/zigzag_indicator.py` | 25–214 | M2 |
| `strategies/elliott_wave_stocks/zigzag_indicator.py` | 36–43; 132–137; 204–208 | M2 |
| `research/vorregistrierung/benchmark.py` | 1–460 | M2 (auch M4, M5) |
| `research/mtm_drawdown/mtm_kern.py` | 1–135 | M3 |
| `research/mtm_drawdown/grundlage.py` | 1–214 | M3 |
| `research/mtm_drawdown/messung.py` | 60–159 | M3 |
| `research/mtm_drawdown/richtungsfall.py` | 50–79 | M3 |
| `research/mtm_drawdown/test_mtm_kern.py` | 30–109; 220–244 | M3 |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-10-09a_beitrag_aus_r45_listen_geschnitten_handelbar_tag.md` (Quelle der Fragen und von R87 (a), (b)) | 195–234 | M3, M4, M5 |

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
- Parameterwerte in Kommentaren der Backtest-Module, nicht wiedergegeben: `strategies/elliott_wave/backtest_elliott.py:51`; `strategies/t3_supertrend/backtest_trend.py:37`–`39`; `strategies/turtle_soup_crypto/backtest_turtle_soup.py:97`–`98`; `strategies/volatility_breakout_crypto/backtest_breakout.py:103`; `strategies/volatility_breakout/backtest_breakout.py:140`
- Parameterwerte in Kommentaren (Werte aus oder gegen `live_params.py`), nicht wiedergegeben: `strategies/elliott_wave/equity_simulation.py:58`; `strategies/volatility_breakout_crypto/equity_simulation.py:5`; `strategies/elliott_wave_stocks/equity_simulation.py:65`; `strategies/rsi2_mean_reversion/equity_simulation.py:46`–`47`, `53`, `63`; `strategies/turtle_soup_stocks/equity_simulation.py:6`–`8`, `46`–`47`, `61`, `69`; `strategies/volatility_breakout/equity_simulation.py:41`, `51`, `62`; `strategies/rsi2_crypto/equity_simulation.py:52`; `strategies/turtle_soup_crypto/equity_simulation.py:46`; `strategies/volatility_breakout_crypto/equity_simulation.py:62`; `strategies/t3_supertrend/equity_simulation.py:49`

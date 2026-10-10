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
- Parameterwerte in Kommentaren (Werte aus oder gegen `live_params.py`), nicht wiedergegeben: `strategies/elliott_wave/equity_simulation.py:58`; `strategies/volatility_breakout_crypto/equity_simulation.py:5`; `strategies/elliott_wave_stocks/equity_simulation.py:65`; `strategies/rsi2_mean_reversion/equity_simulation.py:46`–`47`, `53`, `63`; `strategies/turtle_soup_stocks/equity_simulation.py:6`–`8`, `46`–`47`, `61`, `69`; `strategies/volatility_breakout/equity_simulation.py:41`, `51`, `62`; `strategies/rsi2_crypto/equity_simulation.py:52`; `strategies/turtle_soup_crypto/equity_simulation.py:46`; `strategies/volatility_breakout_crypto/equity_simulation.py:62`; `strategies/t3_supertrend/equity_simulation.py:49`

#!/bin/bash
# TB-140 V2 - Suchlaeufe zu R78 (d), ueber suche.py (nur verfolgte Dateien, nur lesen).
# Zuerst die breiten Muster nur gezaehlt ueber die fuenf Ordner; den Text druckt danach ein zweiter
# Aufruf nur fuer die Dateien des Codes des Laufs nach N5 (Sichtschutz, Register 27.1).
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-140/v2_suche.sh
set -u
PY="${PY:-trading-env/bin/python3}"; S=docs/belege/TB-140/suche.py
F5="--pfad research/vorregistrierung --pfad research/mtm_drawdown --pfad research/exposure_messung --pfad shared --pfad strategies"
LAUF=""
for b in elliott_wave t3_supertrend rsi2_crypto turtle_soup_crypto volatility_breakout_crypto elliott_wave_stocks rsi2_mean_reversion turtle_soup_stocks volatility_breakout; do
  for d in multi_symbol_optimise equity_simulation backtest_elliott backtest_trend backtest_rsi2 backtest_turtle_soup backtest_breakout indicators regime_filter zigzag_indicator elliott_wave_counter; do
    [ -f "strategies/$b/$d.py" ] && LAUF="$LAUF --pfad strategies/$b/$d.py"
  done
done
for f in shared/zuteilung.py shared/kursdaten.py shared/regimewache.py shared/data_quality.py shared/ladeprotokoll.py research/vorregistrierung/benchmark.py research/mtm_drawdown/mtm_kern.py research/mtm_drawdown/grundlage.py; do LAUF="$LAUF --pfad $f"; done
RC=0
lauf() { "$PY" -B "$S" "$@"; local r=$?; echo "rc $r"; [ $r -ne 0 ] && RC=2; }
echo "## V2 (b) - breite Muster, nur gezaehlt, Bereich die fuenf Ordner"
lauf --name V2-b1 $F5 --nur-zaehlen --regex --ohne-gross-klein --muster 'go.live' --muster '2026-09' --muster 'RECENT_YEARS_ONLY' --muster 'bfill|backfill' --muster 'shift\(\s*-' --muster 'center\s*=\s*True' --muster 'iloc\[-1\]' --muster 'tail\(' --muster 'open_time.\]?\.(max|min)\(\)' --muster 'entry_cutoff|cutoff'
echo "## V2 (b) - dieselben Muster mit Text, Bereich der Code des Laufs (N5)"
lauf --name V2-b2 $LAUF --regex --ohne-gross-klein --muster 'go.live' --muster '2026-09' --muster 'RECENT_YEARS_ONLY' --muster 'bfill|backfill' --muster 'shift\(\s*-' --muster 'center\s*=\s*True' --muster 'iloc\[-1\]' --muster 'tail\(' --muster 'open_time.\]?\.(max|min)\(\)' --muster 'entry_cutoff|cutoff' --muster 'MIN_HISTORY'
echo "## V2 (a) - Filter fuer Zeilen ohne Kurse und weitere Lesestellen, Bereich der Code des Laufs"
lauf --name V2-a1 $LAUF --muster 'entferne_unvollstaendige' --muster 'unvollstaendige_maske' --muster 'read_csv' --muster 'dropna' --muster 'KURSSPALTEN ='
echo "## Ende"
exit $RC

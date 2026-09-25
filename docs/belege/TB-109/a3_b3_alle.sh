#!/bin/bash
# TB-109 A3/B3 - a3_b3_trades.py fuer alle neun Bots, ohne Modus. Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-109/a3_b3_alle.sh > docs/belege/TB-109/<datei>.txt
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT
echo "# TB-109 a3_b3_alle.sh, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
for b in elliott_wave elliott_wave_stocks rsi2_crypto rsi2_mean_reversion t3_supertrend turtle_soup_crypto turtle_soup_stocks volatility_breakout volatility_breakout_crypto; do
    trading-env/bin/python3 -W ignore docs/belege/TB-109/a3_b3_trades.py "$b" 2>&1
    echo "  rc $?"
done
echo "# Ende $(date '+%H:%M:%S')"

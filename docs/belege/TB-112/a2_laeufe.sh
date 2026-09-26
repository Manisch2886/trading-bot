#!/bin/bash
# TB-112 A2 - die drei Lauf-Typen aus TB-107 F1 im Modus mit dem Haken (TB-104), am Eingangs-Commit im Repo.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-112/a2_laeufe.sh <scratch>
set -u
SP="$1"; G="docs/belege/TB-112/g_lauf.sh"
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT
echo "# TB-112 A2 Laeufe, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
bash "$G" "$SP/a2" benchmark bm_repo
for b in elliott_wave t3_supertrend rsi2_crypto turtle_soup_crypto volatility_breakout_crypto elliott_wave_stocks rsi2_mean_reversion turtle_soup_stocks volatility_breakout; do
  bash "$G" "$SP/a2" bot "bot_$b" "$b"
done
bash "$G" "$SP/a2" auswertung auswertung

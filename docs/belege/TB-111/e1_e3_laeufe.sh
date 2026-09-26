#!/bin/bash
# E1 + E3 nacheinander aus dem Worktree (g_lauf.sh aus TB-106)
S=/private/tmp/claude-501/-Users-jaquelineloffler-trading-bot/ecc21dc4-0f59-48b0-8b6c-97b6c632932b/scratchpad
cd ~/trading-bot-tb111
bash docs/belege/TB-106/g_lauf.sh $S/laeufe benchmark bm_modus
for b in elliott_wave t3_supertrend rsi2_crypto turtle_soup_crypto volatility_breakout_crypto elliott_wave_stocks rsi2_mean_reversion turtle_soup_stocks volatility_breakout; do
  bash docs/belege/TB-106/g_lauf.sh $S/laeufe bot tl_$b $b
done
echo E_FERTIG

#!/bin/bash
# TB-109 F: Benchmark im Modus (Repo und frischer Klon) und Trockenlauf 9 Bots im Modus, mit dem Haken aus TB-104.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-109/g1_g3.sh <scratch>
set -u
SP="$1"; R=$(pwd); G="$R/docs/belege/TB-109/g_lauf.sh"
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT
z() { for pr in tb40_lauf_ tb40_faltenplan_ tb40_proben_; do printf "%s %s  " $pr "$(ls -d "$TMPDIR"/${pr}* 2>/dev/null | wc -l | tr -d ' ')"; done; }
echo "# TB-109 F Modus-Laeufe, Repo, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "tb40_* vorher: $(z)"
bash "$G" "$SP/g" benchmark bm_repo
for b in elliott_wave t3_supertrend rsi2_crypto turtle_soup_crypto volatility_breakout_crypto elliott_wave_stocks rsi2_mean_reversion turtle_soup_stocks volatility_breakout; do
  bash "$G" "$SP/g" bot "bot_$b" "$b"
done
echo "tb40_* nachher: $(z)"
echo
K="$SP/klon"
if [ -e "$K" ]; then echo "ABBRUCH: $K existiert"; exit 1; fi
git clone -q "$R" "$K"
cd "$K" || exit 1
echo "# TB-109 F Modus-Lauf im frischen Klon <scratch>/klon, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "status --ignored vorher: [$(git status --porcelain --ignored | tr '\n' ' ')]"
echo "tb40_* vorher: $(z)"
bash "$G" "$SP/g" benchmark bm_klon
echo "tb40_* nachher: $(z)"
echo "status --ignored nachher: [$(git status --porcelain --ignored | tr '\n' ' ')]"

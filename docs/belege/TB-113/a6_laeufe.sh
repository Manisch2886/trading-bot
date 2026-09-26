#!/bin/bash
# (Kopie von TB-112 a6_laeufe.sh, Kennung ersetzt; gemessen am Merge-Commit statt am Endstand von A-C.)
# TB-113 A6 (Bauart TB-109 g1_g3.sh): Benchmark im Modus (Repo und frischer Klon) und Trockenlauf der neun Bots im Modus,
# mit dem Haken aus TB-104, am Endstand nach den Commits von A-C. Aufruf aus der Repo-Wurzel: bash docs/belege/TB-113/a6_laeufe.sh <scratch>
set -u
SP="$1"; R=$(pwd); G="$R/docs/belege/TB-113/g_lauf.sh"
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT
echo "# TB-113 A6 Modus-Laeufe, Repo, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "# git status ueber paths.ARBEITSBAUM_PFADE (leer = sauber): [$(git status --porcelain -- shared strategies requirements.lock notifications/manual_close.py research/exposure_messung/bot_lauf.py research/faltenplan_neun/erste_falte_trockenlauf.py research/faltenplan_neun/faltenplan_neun.py research/faltenplan_neun/faltenschranke_messung.py research/universum_trockenlauf/loaderlauf.py research/universum_trockenlauf/universum_trockenlauf.py research/vorregistrierung/auswertung.py research/vorregistrierung/benchmark.py research/vorregistrierung/faltenplan.py research/vorregistrierung/kennzahlen.py research/vorregistrierung/registerdaten.py | tr '\n' ' ')]"
bash "$G" "$SP/a6" benchmark bm_repo
for b in elliott_wave t3_supertrend rsi2_crypto turtle_soup_crypto volatility_breakout_crypto elliott_wave_stocks rsi2_mean_reversion turtle_soup_stocks volatility_breakout; do
  bash "$G" "$SP/a6" bot "bot_$b" "$b"
done
bash "$G" "$SP/a6" auswertung auswertung
echo
K="$SP/a6_klon"
if [ -e "$K" ]; then echo "ABBRUCH: $K existiert"; exit 1; fi
git clone -q "$R" "$K"
cd "$K" || exit 1
echo "# TB-113 A6 Modus-Lauf im frischen Klon <scratch>/a6_klon, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "status --ignored vorher: [$(git status --porcelain --ignored | tr '\n' ' ')]"
bash "$G" "$SP/a6k" benchmark bm_klon
echo "status --ignored nachher: [$(git status --porcelain --ignored | tr '\n' ' ')]"
echo "## Ende $(date '+%H:%M:%S')"

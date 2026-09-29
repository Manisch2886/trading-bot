#!/bin/bash
# TB-122 C4 - der TB-103-Trockenlauf (docs/belege/TB-103/d_trockenlauf.py, Bauart TB-117 E ueber g_lauf.sh "bot"),
# hier OHNE Modus und ohne Lesehaken: keine TB_SELEKTIONS*-Variablen, kein Snapshot - Kursdaten aus dem Repo (data/).
# Je Bot ein leerer Zielordner; verglichen wird sha256 jeder Datei darin (zusammenfassung.json, rechnung_stdout.txt).
# Inhalte werden nicht gelesen (Sichtschutz 27.1). Aufruf aus der Repo-Wurzel: bash docs/belege/TB-122/c4_trockenlauf.sh <ordner>
set -u
SP="$1"; PY=trading-env/bin/python3
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR PYTHONPATH
echo "# TB-122 C4 Trockenlauf ohne Modus, HEAD $(git rev-parse --short HEAD), Arbeitsbaum ausserhalb docs/ [$(git status --porcelain -- . ':!docs' | tr '\n' ' ')], $(date '+%Y-%m-%d %H:%M:%S %z')"
for b in elliott_wave t3_supertrend rsi2_crypto turtle_soup_crypto volatility_breakout_crypto elliott_wave_stocks rsi2_mean_reversion turtle_soup_stocks volatility_breakout; do
  Z="$SP/$b"; if [ -e "$Z" ]; then echo "ABBRUCH: $Z existiert"; exit 1; fi; mkdir -p "$Z"
  T0=$(date +%s)
  TB103_ZIEL="$Z" $PY -W ignore docs/belege/TB-103/d_trockenlauf.py "$b" > "$SP/$b.aussen.txt" 2>&1; rc=$?
  echo "$b rc=$rc $(( $(date +%s)-T0 ))s"
  (cd "$SP" && shasum -a 256 $b/* | sed 's/^/   /')
done
echo "# git status nach den Laeufen ausserhalb docs/: [$(git status --porcelain -- . ':!docs' | tr '\n' ' ')]"

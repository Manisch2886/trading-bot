#!/bin/bash
# TB-117 B - Sonde mit zweiter Seite (R9) gegen das gueltige Abbild 5e5ad109 (TB-114) und das alte e655c1c8 (TB-111).
# Rein lesend. Aufruf aus der Repo-Wurzel: bash docs/belege/TB-117/b_sonde.sh
set -u
PY=trading-env/bin/python3; E=research/vorregistrierung/ergebnisse
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
echo "# TB-117 B Sonde zweiseitig, HEAD $(git rev-parse --short HEAD), sperrlistensonde.py $(shasum -a 256 shared/sperrlistensonde.py | cut -c1-12), $(date '+%Y-%m-%d %H:%M:%S %z')"
for AB in $E/sperrliste_abbild_2026-09-26_tb114.json $E/sperrliste_abbild_2026-09-26.json; do
  echo; echo "## gegen $AB ($(shasum -a 256 $AB | cut -c1-12))"
  $PY -W ignore shared/sperrlistensonde.py --abbild $AB; echo "rc $?"
done

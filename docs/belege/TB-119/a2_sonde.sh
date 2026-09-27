#!/bin/bash
# TB-119 A2 - Sonde gegen das gueltige Abbild tb117. Rein lesend (Kopf der Sonde: "Sie schreibt nichts"; einziger subprocess: git rev-parse HEAD).
set -u
PY=trading-env/bin/python3; AB=research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
echo "# TB-119 A2 Sonde, HEAD $(git rev-parse --short HEAD), sperrlistensonde.py $(shasum -a 256 shared/sperrlistensonde.py | cut -c1-12), Abbild $(shasum -a 256 $AB | cut -c1-12), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "# git status --porcelain vorher: $(git status --porcelain | wc -l | tr -d ' ') Zeilen"
$PY -W ignore shared/sperrlistensonde.py --abbild $AB; echo "rc $?"
echo "# git status --porcelain nachher: $(git status --porcelain | wc -l | tr -d ' ') Zeilen"

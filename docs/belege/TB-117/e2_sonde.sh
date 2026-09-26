#!/bin/bash
# TB-117 E2 - Sonde (zweiseitig) gegen das neue Abbild tb117 und gegen das bisher gueltige 5e5ad109 (tb114). Rein lesend.
set -u
PY=trading-env/bin/python3; E=research/vorregistrierung/ergebnisse
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
echo "# TB-117 E2 Sonde, HEAD $(git rev-parse --short HEAD), sperrlistensonde.py $(shasum -a 256 shared/sperrlistensonde.py | cut -c1-12), $(date '+%Y-%m-%d %H:%M:%S %z')"
for AB in $E/sperrliste_abbild_2026-09-26_tb117.json $E/sperrliste_abbild_2026-09-26_tb114.json; do
  echo; echo "## gegen $AB ($(shasum -a 256 $AB | cut -c1-12))"
  $PY -W ignore shared/sperrlistensonde.py --abbild $AB; echo "rc $?"
done

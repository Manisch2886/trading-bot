#!/bin/bash
# TB-129 A5 - test_vorregistrierung ohne Zeitgrenze; Beleg nur rc, Dauer, Schlusszeile (Sichtschutz 27.1).
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-129/test_vorregistrierung.sh <scratch-ausgabe> > <beleg>
set -u
OUT="$1"
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
echo "# TB-129 test_vorregistrierung, HEAD $(git rev-parse --short HEAD), Register sha256 $(shasum -a 256 docs/VORREGISTRIERUNG_neuselektion.md | cut -c1-16), Start $(date '+%Y-%m-%d %H:%M:%S %z')"
T0=$(date +%s)
trading-env/bin/python3 -W ignore research/vorregistrierung/test_vorregistrierung.py > "$OUT" 2>&1; RC=$?
T1=$(date +%s)
echo "rc $RC"
echo "Dauer $((T1 - T0)) s"
echo "Schlusszeile: $(grep -v '^[[:space:]]*$' "$OUT" | tail -1)"

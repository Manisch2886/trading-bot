#!/bin/bash
# TB-106 B2 - registerbericht.py --pruefen vorher (Kopie des Ordners am Stand 327bc79 in <alt>) und nachher.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-106/b2_registerbericht.sh <alt-wurzel>
PY=/Users/jaquelineloffler/trading-bot/trading-env/bin/python3
echo "# TB-106 B2 registerbericht --pruefen, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "== vorher (327bc79, Kopie unter $1)"
TB30A_BASE_DIR="$PWD" $PY -W ignore "$1/research/vorregistrierung/registerbericht.py" --pruefen 2>&1 | tail -4
echo "rc ${PIPESTATUS[0]}"
echo "== nachher (Arbeitsbaum)"
$PY -W ignore research/vorregistrierung/registerbericht.py --pruefen 2>&1 | tail -4
echo "rc ${PIPESTATUS[0]}"
echo "== Unterschied erzeugter Block vorher/nachher"
diff <(TB30A_BASE_DIR="$PWD" $PY -W ignore "$1/research/vorregistrierung/registerbericht.py" 2>/dev/null) \
     <($PY -W ignore research/vorregistrierung/registerbericht.py 2>/dev/null)
echo "diff rc $?"

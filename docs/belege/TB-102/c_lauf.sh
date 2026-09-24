#!/bin/bash
# TB-102 Block C: Stoerprobe im Speicher mit Lesehaken. Schreibt nur in <scratch>.
# Aufruf aus der Repo-Wurzel:  bash docs/belege/TB-102/c_lauf.sh <scratch-ordner>
set -u
SP="$1"
if [ -e "$SP" ]; then echo "ABBRUCH: $SP existiert"; exit 1; fi
mkdir -p "$SP/prot"
FP=research/vorregistrierung/ergebnisse/faltenplan.json
echo "# TB-102 C Stoerprobe, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "# faltenplan.json vorher: $(shasum -a 256 $FP | cut -c1-64)"
env PYTHONPATH=docs/belege/TB-98/haken TB98_PROTOKOLL="$SP/prot" \
    trading-env/bin/python3 -W ignore docs/belege/TB-102/c_stoerprobe.py > "$SP/ausgabe.txt" 2>&1
echo "rc=$?"
echo "# faltenplan.json nachher: $(shasum -a 256 $FP | cut -c1-64)"
echo "# git status (muss leer sein ausser docs/belege/TB-102):"
git status --porcelain

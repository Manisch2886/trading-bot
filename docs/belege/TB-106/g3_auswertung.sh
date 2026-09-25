#!/bin/bash
# TB-106 G3 - auswertung.py gegen die Beispieldaten (beispieldaten.py, wie test_vorregistrierung), alle Bots
# mit endgueltigem Plan. Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-106/g3_auswertung.sh <rohordner> <ausgabe.json>
# Existiert <rohordner> noch nicht, werden die Beispieldaten dort EINMAL erzeugt; vorher und nachher lesen
# dieselben Rohergebnisse. Schreibt nur nach <rohordner> und <ausgabe.json> (Scratchpad).
set -u
R="$1"; J="$2"; PY=/Users/jaquelineloffler/trading-bot/trading-env/bin/python3
echo "# TB-106 G3, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
if [ -e "$J" ]; then echo "ABBRUCH: $J existiert"; exit 1; fi
if [ ! -d "$R" ]; then
  T0=$(date +%s); $PY -W ignore research/vorregistrierung/beispieldaten.py --ziel "$R" > "$R.erzeugung.txt" 2>&1
  echo "beispieldaten rc=$? $(( $(date +%s) - T0 ))s"
fi
T0=$(date +%s); $PY -W ignore research/vorregistrierung/auswertung.py --rohergebnisse "$R" --json "$J" > "$J.txt" 2>&1
echo "auswertung rc=$? $(( $(date +%s) - T0 ))s"
shasum -a 256 "$J" | sed "s#$(dirname "$J")/##"

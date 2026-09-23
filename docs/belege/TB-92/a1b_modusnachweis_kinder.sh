#!/bin/bash
# TB-92 A1b, Nachtrag: dieselbe Rechnung mit prozessuebergreifendem Lesehaken
# (haken/sitecustomize.py ueber PYTHONPATH). Lauf 3 = Umlenkung wie Lauf 1
# (nur TB30A_BASE_DIR); Lauf 4 = zusaetzlich TB36_BASE_DIR und TB40_BASE_DIR,
# die faltenplan_neun bzw. universum_trockenlauf in den Kindprozessen lesen.
set -u
SP="$1"; REPO="$(pwd)"; H="$SP/modus_hilfsordner"; B="$REPO/docs/belege/TB-92"
Z=research/vorregistrierung/ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json
for n in 3 4; do
  mkdir -p "$SP/protokoll_lauf$n"
  if [ $n = 3 ]; then EXTRA=""; else EXTRA="TB36_BASE_DIR=$H TB40_BASE_DIR=$H"; fi
  T0=$(date +%s)
  env PYTHONPATH="$B/haken" TB92_PROTOKOLL="$SP/protokoll_lauf$n" TB30A_BASE_DIR="$H" $EXTRA \
      trading-env/bin/python3 research/vorregistrierung/benchmark.py \
      --ziel "$SP/benchmark_modusnachweis_lauf$n.json" > "$SP/a1b_lauf${n}_ausgabe.txt" 2>&1
  echo "Lauf $n rc=$? Dauer $(( $(date +%s) - T0 )) s, Prozesse $(ls "$SP/protokoll_lauf$n" | wc -l | tr -d ' ')"
  cmp "$Z" "$SP/benchmark_modusnachweis_lauf$n.json" && echo "Lauf $n BYTEGLEICH mit $Z"
done

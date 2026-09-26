#!/bin/bash
# TB-111 C1 - dieselben Faelle wie c_proben.sh auf DENSELBEN Eingaben (<ziel> aus dem Vorher-Lauf) mit dem
# heutigen auswertung.py; stderr nach <fall>.nach.err und cmp gegen <fall>.err (Meldung wortgleich?).
#   bash docs/belege/TB-111/c_nochmal.sh <ziel>
set -u
Z="$1"; PY=/Users/jaquelineloffler/trading-bot/trading-env/bin/python3; BOT=turtle_soup_stocks
V=research/vorregistrierung
echo "# TB-111 C-Proben nochmal, HEAD $(git --no-optional-locks rev-parse --short HEAD), auswertung.py $(shasum -a 256 $V/auswertung.py | cut -c1-16), $(date '+%Y-%m-%d %H:%M:%S %z')"
for f in leer spalte zelle tage basis; do
  a=(--rohergebnisse "$Z/$f"); [ "$f" != leer ] && a+=(--bot $BOT)
  $PY -W ignore $V/auswertung.py "${a[@]}" > "$Z/$f.nach.out" 2> "$Z/$f.nach.err"; rc=$?
  cmp -s "$Z/$f.err" "$Z/$f.nach.err" && g="stderr wortgleich" || g="stderr VERSCHIEDEN"
  cmp -s "$Z/$f.out" "$Z/$f.nach.out" && o="stdout gleich" || o="stdout VERSCHIEDEN"
  echo "$f: rc $rc | $g ($(wc -c < "$Z/$f.nach.err" | tr -d ' ') B) | $o | $(tail -1 "$Z/$f.nach.err" | cut -c1-120)"
done

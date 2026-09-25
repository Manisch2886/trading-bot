#!/bin/bash
# TB-109 G2: die 8 Ausgaben ohne Modus (g2_ausgaben.sh) nachher, Vergleich gegen den Vorher-Lauf, dazu der
# Benchmark ohne Modus. Aufruf aus der Repo-Wurzel: bash docs/belege/TB-109/g2_gesamt.sh <scratch>
set -u
SP="$1"
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT
bash docs/belege/TB-109/g2_ausgaben.sh "$SP/g2_nachher"
echo "## Vergleich gegen g2_vorher (Code-Stand f4d6d6d, 0b)"
for f in fn embargo fsm lesart plan ut sf eft; do
  cmp -s "$SP/g2_nachher/$f.json" "$SP/g2_vorher/$f.json" && echo "$f BYTEGLEICH" || echo "$f VERSCHIEDEN"; done
echo "## Benchmark ohne Modus"
trading-env/bin/python3 -W ignore research/vorregistrierung/benchmark.py --ziel "$SP/g2_nachher/benchmark_ohne_modus.json" > "$SP/g2_nachher/bm.txt" 2>&1
echo "rc=$?"
shasum -a 256 "$SP/g2_nachher/benchmark_ohne_modus.json" | sed "s#$SP/##"

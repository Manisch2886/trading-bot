#!/bin/bash
# TB-107 Abnahme E: ut.json und sf.json (Ausgaben 5 und 6 aus g2_ausgaben.sh) ohne Modus, dazu die Zahl der
# tb40_lauf_* in $TMPDIR vor und nach jedem Lauf; danach test_universum_trockenlauf und test_zwischenablage.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-107/e_abnahme.sh <ziel>
set -u
Z="$1"; PY=/Users/jaquelineloffler/trading-bot/trading-env/bin/python3
if [ -e "$Z" ]; then echo "ABBRUCH: $Z existiert"; exit 1; fi
mkdir -p "$Z"
zahl() { ls -d "$TMPDIR"/tb40_lauf_* 2>/dev/null | wc -l | tr -d ' '; }
echo "# TB-107 E Abnahme ohne Modus, HEAD $(git rev-parse --short HEAD), Arbeitsbaum [$(git status --porcelain -- research shared | tr '\n' ' ')], $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "tb40_lauf_* vor ut: $(zahl)"
$PY -W ignore research/universum_trockenlauf/universum_trockenlauf.py --json "$Z/ut.json" > "$Z/ut.txt" 2>&1; echo "ut rc=$?"
echo "tb40_lauf_* nach ut: $(zahl)"
$PY -W ignore research/universum_trockenlauf/universum_trockenlauf.py --stille-filter --json "$Z/sf.json" > "$Z/sf.txt" 2>&1; echo "sf rc=$?"
echo "tb40_lauf_* nach sf: $(zahl)"
for f in ut sf; do shasum -a 256 "$Z/$f.json" | sed "s#$Z/##"; done
for t in test_universum_trockenlauf test_zwischenablage; do T0=$(date +%s)
  $PY -W ignore research/universum_trockenlauf/$t.py > "$Z/$t.log" 2>&1
  echo "$t rc=$? $(( $(date +%s)-T0 ))s: $(grep -E 'Pruefungen|bestanden' "$Z/$t.log" | tail -1)"; done
echo "tb40_lauf_* nach den Tests: $(zahl)"

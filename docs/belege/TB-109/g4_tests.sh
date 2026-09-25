#!/bin/bash
# (Kopie von TB-107 g4_tests.sh, dazu shared/test_nulltrades_modus.py; die Zaehlung am Ende je Praefix)
# TB-109 F - alle Tests am Endstand, trading-env (3.9.6), je Datei rc, Dauer, Schlusszeile.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-109/g4_tests.sh <scratch-logordner>
set -u
LOG="$1"; mkdir -p "$LOG"; PY=trading-env/bin/python3
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT
echo "# TB-109 F Tests, HEAD $(git rev-parse --short HEAD), Arbeitsbaum ausserhalb docs/ [$(git status --porcelain -- . ':!docs' | tr '\n' ' ')], $(date '+%Y-%m-%d %H:%M:%S %z')"
for t in research/faltenplan_neun/test_faltenplan_neun.py research/faltenplan_neun/test_erste_falte_trockenlauf.py \
         research/faltenplan_neun/test_horizontbeginn.py research/faltenplan_neun/test_min_history.py \
         research/faltenplan_neun/test_volle_jahre.py research/universum_trockenlauf/test_universum_trockenlauf.py \
         research/universum_trockenlauf/test_zwischenablage.py shared/test_paths.py shared/test_nulltrades_modus.py shared/test_strategy_paths.py \
         shared/test_rueckfaelle_modus.py shared/test_ergebniskurven.py shared/test_startpruefungen.py \
         shared/test_main_gegenprobe.py research/vorregistrierung/test_ersatzwerte.py \
         research/vorregistrierung/test_vorregistrierung.py; do
  T0=$(date +%s); n=$(basename "$t" .py)
  $PY -W ignore "$t" > "$LOG/$n.log" 2>&1; rc=$?
  echo "$n rc=$rc $(( $(date +%s)-T0 ))s: $(grep -iE 'bestanden|pruefungen|fehlgeschlagen' "$LOG/$n.log" | tail -1)"
done
echo "tb40_* in \$TMPDIR nach den Tests: $(for pr in tb40_lauf_ tb40_faltenplan_ tb40_proben_; do printf "%s %s  " $pr "$(ls -d "$TMPDIR"/${pr}* 2>/dev/null | wc -l | tr -d " ")"; done)"

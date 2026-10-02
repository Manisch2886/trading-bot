#!/bin/bash
# TB-129 A5 - Nachweis am echten Register (nach dem Echtlauf, vor dem Commit). Schreibt die Belege a5_*.txt.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-129/a5_nachweis.sh <scratch> <S0> <datum> <probekopie>
set -u
SP="$1"; S0="$2"; D="$3"; K="$4"; PY=trading-env/bin/python3; BL=docs/belege/TB-129; R=docs/VORREGISTRIERUNG_neuselektion.md
$PY $BL/a5_r_diff.py $S0 > $BL/a5_r_diff.txt; echo "a5_r_diff rc $?"; tail -1 $BL/a5_r_diff.txt
$PY $BL/a5_mutation.py $S0 $R "$SP/a5_mutation_kopie.md" > $BL/a5_r_diff_mutation.txt; echo "a5_mutation rc $? (0 = Mutation erkannt)"; tail -1 $BL/a5_r_diff_mutation.txt
$PY $BL/a5_zitate.py $S0 $D > $BL/a5_zitate.txt; echo "a5_zitate rc $?"; tail -1 $BL/a5_zitate.txt
$PY $BL/a5_marken.py $S0 $D > $BL/a5_marken.txt; echo "a5_marken rc $?"; tail -1 $BL/a5_marken.txt
{ echo "# git diff --numstat $R (Soll zweite Spalte 0)"; git diff --numstat -- $R; echo "# cmp Register Probekopie"; cmp $R "$K"; echo "cmp rc $?"; } > $BL/a5_numstat.txt
cat $BL/a5_numstat.txt

#!/bin/bash
# TB-126 A6 - Nachweis am echten Register (nach dem Echtlauf, vor dem Commit). Schreibt die Belege a6_*.txt.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-126/a6_nachweis.sh <scratch> <S0> <datum> <probekopie>
set -u
SP="$1"; S0="$2"; D="$3"; K="$4"; PY=trading-env/bin/python3; BL=docs/belege/TB-126; R=docs/VORREGISTRIERUNG_neuselektion.md
$PY $BL/a6_r_diff.py $S0 > $BL/a6_r_diff.txt; echo "a6_r_diff rc $?"; tail -1 $BL/a6_r_diff.txt
$PY $BL/a6_mutation.py $S0 $R "$SP/a6_mutation_kopie.md" > $BL/a6_r_diff_mutation.txt; echo "a6_mutation rc $? (0 = Mutation erkannt)"; tail -1 $BL/a6_r_diff_mutation.txt
$PY $BL/a6_zitate.py $S0 > $BL/a6_zitate.txt; echo "a6_zitate rc $?"; tail -1 $BL/a6_zitate.txt
$PY $BL/a6_marken.py $S0 $D > $BL/a6_marken.txt; echo "a6_marken rc $?"; tail -1 $BL/a6_marken.txt
{ echo "# git diff --numstat $R (Soll zweite Spalte 0)"; git diff --numstat -- $R; echo "# cmp Register Probekopie"; cmp $R "$K"; echo "cmp rc $?"; } > $BL/a6_numstat.txt
cat $BL/a6_numstat.txt

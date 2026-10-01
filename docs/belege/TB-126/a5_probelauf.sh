#!/bin/bash
# TB-126 A5 - Probelauf gegen eine Kopie des Registers, Textpruefungen aus A6 an der Kopie.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-126/a5_probelauf.sh <scratch> <S0> <datum>
set -u
SP="$1"; S0="$2"; D="$3"; PY=trading-env/bin/python3; BL=docs/belege/TB-126; R=docs/VORREGISTRIERUNG_neuselektion.md
K="$SP/a5_probe_$(date +%H%M%S).md"
echo "# TB-126 A5 Probelauf, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "Register $(shasum -a 256 $R | cut -c1-16), Kopie $K"
cp $R "$K"
echo "## Einsetzen gegen die Kopie"; TB126_PROBE="$K" $PY $BL/a5_eintrag.py; echo "rc $?"
echo "## Register selbst unberuehrt: $(shasum -a 256 $R | cut -c1-16)"
echo "## a6_r_diff.py";    $PY $BL/a6_r_diff.py $S0 "$K" | tail -1; echo "rc ${PIPESTATUS[0]}"
echo "## a6_mutation.py";  $PY $BL/a6_mutation.py $S0 "$K" "$K.mutation"; echo "rc $?"
echo "## a6_zitate.py";    $PY $BL/a6_zitate.py $S0 "$K" | tail -1; echo "rc ${PIPESTATUS[0]}"
echo "## a6_marken.py";    $PY $BL/a6_marken.py $S0 $D "$K" | grep -v " gesetzt Zeile"; echo "rc ${PIPESTATUS[0]}"
echo "## numstat Original -> Kopie"; git diff --no-index --numstat $R "$K" | cut -f1,2
echo "KOPIE=$K"

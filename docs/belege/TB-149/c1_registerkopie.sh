#!/bin/bash
# TB-149 C1 - Registerkopie (wie TB-136 C1, dort nach TB-132, TB-130 und TB-129): fuenf Aufrufe von docs/werkzeuge/registerkopie.py,
# je Ausgabe und rc nach docs/belege/TB-149/c1_*.txt. Nach dem Commit aus A, am sauberen Register.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-149/c1_registerkopie.sh
set -u
PY=trading-env/bin/python3; W=docs/werkzeuge/registerkopie.py; BL=docs/belege/TB-149
K="(HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z'))"
lauf() {  # <datei> <titel> <schalter...>
    local d="$1" t="$2"; shift 2
    { echo "# TB-149 C1: registerkopie.py $t  $K"; $PY $W "$@" 2>&1; echo "rc $?"; } > "$BL/$d"
    echo "$d: $(tail -1 "$BL/$d")"
}
lauf c1_registerkopie.txt ""
lauf c1_pruefen.txt "--pruefen" --pruefen
lauf c1_marken.txt "--marken" --marken
lauf c1_abschnitte.txt "--abschnitte" --abschnitte
lauf c1_abschnitte_pruefen.txt "--abschnitte --pruefen" --abschnitte --pruefen

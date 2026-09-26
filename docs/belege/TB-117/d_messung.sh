#!/bin/bash
# TB-117 D - auswertung.py: Hash-Uebergang, register(), Berichtigung R8 (a), Ausgang ohne Modus auf Beispieldaten.
# Rein lesend bis auf <scratch>. Aufruf aus der Repo-Wurzel: bash docs/belege/TB-117/d_messung.sh <scratch>
set -u
SP="$1"; PY=trading-env/bin/python3; V=research/vorregistrierung
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
echo "# TB-117 D, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## auswertung.py vorher (ff2f254) und jetzt"
git show ff2f254:$V/auswertung.py | shasum -a 256 | sed 's/-$/auswertung.py @ ff2f254/'
shasum -a 256 $V/auswertung.py
echo "## register() jetzt (auswertung.py steht in EINGEFROREN)"
$PY -W ignore -c "
import sys; sys.path.insert(0,'$V'); import herkunft
r = herkunft.register(); print('register()', r['register'], 'fehlend', r['fehlend'], 'teile', len(r['teile']))"
echo "## R8 (a): der Satz im Docstring von _abbruch_2 vorher / jetzt"
git show ff2f254:$V/auswertung.py | grep -n "endet mit 1"
grep -n "endet mit 1\|endet seit TB-111" $V/auswertung.py
echo "## git diff --numstat (ff2f254 -> Arbeitsbaum)"
git diff --numstat ff2f254 -- $V/auswertung.py
echo "## ohne Modus: auswertung.py auf Beispieldaten (turtle_soup_stocks), Kopf des Berichts"
R="$SP/d_roh"; [ -e "$R" ] && { echo "ABBRUCH: $R existiert"; exit 1; }
$PY -W ignore $V/beispieldaten.py --ziel "$R" --bot turtle_soup_stocks > /dev/null 2>&1
$PY -W ignore $V/auswertung.py --rohergebnisse "$R" --bot turtle_soup_stocks --json "$R.json" > "$R.txt" 2>&1; echo "rc $?"
sed -n 1,8p "$R.txt"
$PY -c "import json; print('JSON herkunft:', json.dumps(json.load(open('$R.json'))['herkunft'], sort_keys=True)[:300])"

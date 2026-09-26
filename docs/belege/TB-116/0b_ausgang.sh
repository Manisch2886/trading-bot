#!/bin/bash
# TB-116 0b - Ausgangswerte (Bauart TB-115 0b_ausgang.sh):
# HEAD, register(), Sonde gegen das TB-114-Abbild 5e5ad109. Rein lesend.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-116/0b_ausgang.sh <scratch> <marke>
set -u
SP="$1"; M="$2"; PY=trading-env/bin/python3; V=research/vorregistrierung
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
AB=$V/ergebnisse/sperrliste_abbild_2026-09-26_tb114.json
echo "# TB-116 0b ($M), HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## Letzter Nicht-docs-Commit (Soll: 0b7ab4b/e07fefd-Stand, seit 90307cb nur docs/)"
git log -1 --format='%h %s' -- . ':!docs' | cut -c1-100
echo "## Hashes (Soll Abbild 5e5ad109...)"
shasum -a 256 $V/herkunft.py $AB shared/sperrlistensonde.py
echo "## herkunft.register() (Soll 5acb4c19...)"
$PY -W ignore -c "
import sys; sys.path.insert(0,'$V'); import herkunft
r = herkunft.register(); print('register', r['register']); print('fehlend', r['fehlend']); print('teile', len(r['teile']))" 2>&1
echo "## Sonde gegen $AB (Soll: Pfad-Bestandteile 34/0/0)"
$PY -W ignore shared/sperrlistensonde.py --abbild $AB > "$SP/sonde_0b_$M.txt" 2>&1; echo "rc $?"
grep -E "^Pfad-Bestandteile|^\(ii\)|^RUECKGABEWERT|Registertext: |BEFUND" "$SP/sonde_0b_$M.txt"
echo "## git status (ausserhalb docs/ und research/leiter_pruefung/ muss leer sein)"; git status --porcelain -- . ':!docs' ':!research/leiter_pruefung'; echo "[Ende status]"
echo "## Ende"

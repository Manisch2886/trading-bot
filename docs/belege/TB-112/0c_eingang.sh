#!/bin/bash
# TB-112 0c - Eingangsmessung. Aufruf aus der Repo-Wurzel: bash docs/belege/TB-112/0c_eingang.sh <bezeichnung> <scratch>
set -u
B="$1"; SP="$2"; PY=trading-env/bin/python3; V=research/vorregistrierung
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT
AB=$V/ergebnisse/sperrliste_abbild_2026-09-25b.json
echo "# TB-112 0c $B, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## ARBEITSBAUM_PFADE / REGISTRIERTE_PROTOKOLLE (grep in shared/paths.py)"
grep -n "^ARBEITSBAUM_PFADE\|^REGISTRIERTE_PROTOKOLLE" shared/paths.py
echo "## herkunft.register()"
$PY -W ignore -c "
import sys; sys.path.insert(0,'$V'); import herkunft
r = herkunft.register(); print('register', r['register']); print('fehlend', r['fehlend'])" 2>&1
echo "## Sonde gegen $AB"
shasum -a 256 $AB
$PY -W ignore shared/sperrlistensonde.py --abbild $AB > "$SP/sonde_$B.txt" 2>&1; echo "rc $?"
grep -E "^Pfad-Bestandteile|^\(ii\)|^RUECKGABEWERT|Registertext: " "$SP/sonde_$B.txt"
echo "## test_startpruefungen"
T0=$(date +%s); $PY -W ignore shared/test_startpruefungen.py > "$SP/tsp_$B.txt" 2>&1; echo "rc $? $(( $(date +%s)-T0 ))s: $(grep -iE 'bestanden|pruefungen|fehlgeschlagen' "$SP/tsp_$B.txt" | tail -1)"
grep -E "N1 ohne|N4 ohne" "$SP/tsp_$B.txt"
echo "## tb40_* in \$TMPDIR je Praefix"
for pr in tb40_lauf_ tb40_faltenplan_ tb40_proben_ tb40_test_ tb44_l_; do echo "   $pr $(ls -d "$TMPDIR"/${pr}* 2>/dev/null | wc -l | tr -d ' ')"; done
echo "## herkunft_protokoll.jsonl"; ls -l $V/ergebnisse/herkunft_protokoll.jsonl 2>&1
echo "## git status ausserhalb docs/"; git status --porcelain -- . ':!docs'
echo "## Ende"

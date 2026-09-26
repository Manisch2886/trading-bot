#!/bin/bash
# TB-114 A/D - Messung vor und nach einem Registereintrag: Hash Register, register(), Sonde gegen ein Abbild.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-114/a_messung.sh <bezeichnung> <scratch> [<abbild>]
set -u
B="$1"; SP="$2"; PY=trading-env/bin/python3; V=research/vorregistrierung
AB="${3:-$V/ergebnisse/sperrliste_abbild_2026-09-26.json}"
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
echo "# TB-114 Messung $B, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
shasum -a 256 docs/VORREGISTRIERUNG_neuselektion.md $V/herkunft.py "$AB"
echo "Registerzeilen $(wc -l < docs/VORREGISTRIERUNG_neuselektion.md | tr -d ' ')"
$PY -W ignore -c "
import sys; sys.path.insert(0,'$V'); import herkunft
r = herkunft.register(); print('register', r['register']); print('fehlend', r['fehlend']); print('teile', len(r['teile']))" 2>&1
echo "## Sonde gegen $AB"
$PY -W ignore shared/sperrlistensonde.py --abbild "$AB" > "$SP/sonde_$B.txt" 2>&1; echo "rc $?"
grep -E "^Pfad-Bestandteile|^\(ii\)|^RUECKGABEWERT|Registertext: |BEFUND|ABWEICHUNG" "$SP/sonde_$B.txt"
$PY -W ignore shared/sperrlistensonde.py --abbild "$AB" --json > "$SP/sonde_$B.json" 2>/dev/null
echo "Sonde-JSON ohne Zeitangaben/Zeilen sha256: $($PY -c "
import json,hashlib; b=json.load(open('$SP/sonde_$B.json'))
b['ii'].pop('zeilen',None)
print(hashlib.sha256(json.dumps(b,sort_keys=True,ensure_ascii=False).encode()).hexdigest())")"

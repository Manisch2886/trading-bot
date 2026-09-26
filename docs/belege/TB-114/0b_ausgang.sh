#!/bin/bash
# TB-114 0b - Ausgangswerte (Bauart TB-113 a_messung.sh): register(), Hash herkunft.py, Sonde gegen e655c1c8,
# die neun TB-24-Listen (versioniert, sha256, Zeilenzahl). Aufruf aus der Repo-Wurzel: bash docs/belege/TB-114/0b_ausgang.sh <scratch>
set -u
SP="$1"; PY=trading-env/bin/python3; V=research/vorregistrierung
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
AB=$V/ergebnisse/sperrliste_abbild_2026-09-26.json
echo "# TB-114 0b, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## Hashes (Soll herkunft.py 5bbfc9e0..., Abbild e655c1c8...)"
shasum -a 256 $V/herkunft.py $AB
echo "## herkunft.register() (Soll a0e477fd...)"
$PY -W ignore -c "
import sys; sys.path.insert(0,'$V'); import herkunft
r = herkunft.register(); print('register', r['register']); print('fehlend', r['fehlend']); print('teile', len(r['teile']))" 2>&1
echo "## Sonde gegen $AB (Soll: Pfad-Bestandteile 25/0/0, (ii) 0)"
$PY -W ignore shared/sperrlistensonde.py --abbild $AB > "$SP/sonde_0b.txt" 2>&1; echo "rc $?"
grep -E "^Pfad-Bestandteile|^\(ii\)|^RUECKGABEWERT|Registertext: |BEFUND" "$SP/sonde_0b.txt"
echo "## die neun TB-24-Listen (Reihenfolge wie ls strategies/)"
for b in $(ls strategies/); do
  f=research/tb24_haltedauern/daten/${b}_alle_trades.csv
  v=$(git ls-files --error-unmatch "$f" >/dev/null 2>&1 && echo versioniert || echo NICHT-VERSIONIERT)
  d=$(git status --porcelain -- "$f")
  echo "$(shasum -a 256 "$f" | cut -d' ' -f1)  $(wc -l < "$f" | tr -d ' ') Zeilen  $v  status[$d]  $f"
done
echo "## git status ausserhalb docs/"; git status --porcelain -- . ':!docs'
echo "## Ende"

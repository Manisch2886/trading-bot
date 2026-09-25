#!/bin/bash
# TB-104 B0 - Ausgaben der umzustellenden Module OHNE Modus, als Vergleichsstand vor/nach Block B/C
# (Abbruchkriterium 3: "Ohne Modus aendert sich ein Ergebnis irgendeines der umgestellten Module").
# Schreibt NUR nach <ziel> (Scratchpad) und in mkdtemp-Ordner der Werkzeuge. Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-104/b0_ausgaben.sh <ziel>
set -u
Z="$1"; PY=trading-env/bin/python3
if [ -e "$Z" ]; then echo "ABBRUCH: $Z existiert"; exit 1; fi
mkdir -p "$Z"
echo "# TB-104 B0 Ausgaben ohne Modus, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
t() { local T0=$(date +%s); "$@"; echo "   rc=$? $(( $(date +%s) - T0 ))s"; }
echo "1 faltenplan_neun.py --json";   t $PY -W ignore research/faltenplan_neun/faltenplan_neun.py --json "$Z/fn.json" > "$Z/fn.txt" 2>&1
echo "2 embargo_neun.py --json";      t $PY -W ignore research/faltenplan_neun/embargo_neun.py --json "$Z/embargo.json" > "$Z/embargo.txt" 2>&1
echo "3 faltenschranke_messung.py --json"; t $PY -W ignore research/faltenplan_neun/faltenschranke_messung.py --json "$Z/fsm.json" > "$Z/fsm.txt" 2>&1
echo "4 loader_lesart (9 Bots) + faltenplan.faltenplan() im Speicher"
t $PY -W ignore - "$Z" > "$Z/speicher.txt" 2>&1 <<'PYEOF'
import json, sys
z = sys.argv[1]
sys.path.insert(0, "research/vorregistrierung")
import faltenplan as fp, registerdaten as rd
sys.path.insert(0, "research/faltenplan_neun")
import faltenschranke_messung as fsm
json.dump({b: fsm.loader_lesart(b) for b in rd.BOTS}, open(z + "/lesart.json", "w"), indent=1, sort_keys=True, default=str)
json.dump(fp.faltenplan(rd._mess()), open(z + "/plan.json", "w"), indent=1, sort_keys=True, default=str)
print("ok")
PYEOF
echo "5 universum_trockenlauf.py --json"; t $PY -W ignore research/universum_trockenlauf/universum_trockenlauf.py --json "$Z/ut.json" > "$Z/ut.txt" 2>&1
echo "6 universum_trockenlauf.py --stille-filter --json"; t $PY -W ignore research/universum_trockenlauf/universum_trockenlauf.py --stille-filter --json "$Z/sf.json" > "$Z/sf.txt" 2>&1
echo "7 erste_falte_trockenlauf.py --json"; t $PY -W ignore research/faltenplan_neun/erste_falte_trockenlauf.py --json "$Z/eft.json" > "$Z/eft.txt" 2>&1
echo "## sha256 der JSON-Ausgaben"
for f in fn embargo fsm lesart plan ut sf eft; do shasum -a 256 "$Z/$f.json" | sed "s#$Z/##"; done
echo FERTIG

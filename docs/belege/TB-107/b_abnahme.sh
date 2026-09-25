#!/bin/bash
# TB-107 Abnahme B/C: nur einzelne Ausgaben aus g2_ausgaben.sh, ohne Modus. Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-107/b_abnahme.sh <ziel> <auswahl...>   auswahl: fn fsm lesart eft
set -u
Z="$1"; shift; PY=/Users/jaquelineloffler/trading-bot/trading-env/bin/python3
if [ -e "$Z" ]; then echo "ABBRUCH: $Z existiert"; exit 1; fi
mkdir -p "$Z"
echo "# TB-107 Teilabnahme ohne Modus, HEAD $(git rev-parse --short HEAD), Arbeitsbaum: [$(git status --porcelain -- research shared | tr '\n' ' ')], $(date '+%Y-%m-%d %H:%M:%S %z')"
for a in "$@"; do case "$a" in
  fn)  $PY -W ignore research/faltenplan_neun/faltenplan_neun.py --json "$Z/fn.json" > "$Z/fn.txt" 2>&1; echo "fn rc=$?" ;;
  fsm) $PY -W ignore research/faltenplan_neun/faltenschranke_messung.py --json "$Z/fsm.json" > "$Z/fsm.txt" 2>&1; echo "fsm rc=$?" ;;
  eft) $PY -W ignore research/faltenplan_neun/erste_falte_trockenlauf.py --json "$Z/eft.json" > "$Z/eft.txt" 2>&1; echo "eft rc=$?" ;;
  lesart) $PY -W ignore - "$Z" > "$Z/lesart.txt" 2>&1 <<'PYEOF'
import json, sys
z = sys.argv[1]
sys.path.insert(0, "research/vorregistrierung")
import registerdaten as rd
sys.path.insert(0, "research/faltenplan_neun")
import faltenschranke_messung as fsm
json.dump({b: fsm.loader_lesart(b) for b in rd.BOTS}, open(z + "/lesart.json", "w"), indent=1, sort_keys=True, default=str)
PYEOF
     echo "lesart rc=$?" ;;
esac; done
for a in "$@"; do shasum -a 256 "$Z/$a.json" | sed "s#$Z/##"; done

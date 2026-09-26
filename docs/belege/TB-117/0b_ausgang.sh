#!/bin/bash
# TB-117 0b - Ausgangswerte (Bauart TB-116 0b_ausgang.sh, erweitert um auswertung.py und den Benchmark im Modus):
# HEAD, Hashes, register(), Sonde gegen das TB-114-Abbild 5e5ad109, Benchmark im Modus (Soll 64fb2912). Rein lesend,
# schreibt nur ins Scratchpad. Aufruf aus der Repo-Wurzel: bash docs/belege/TB-117/0b_ausgang.sh <scratch> <marke>
set -u
SP="$1"; M="$2"; PY=trading-env/bin/python3; V=research/vorregistrierung
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
AB=$V/ergebnisse/sperrliste_abbild_2026-09-26_tb114.json
echo "# TB-117 0b ($M), HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## Letzter Nicht-docs-Commit"
git log -1 --format='%h %s' -- . ':!docs' | cut -c1-100
echo "## Hashes (Soll herkunft ed521ac1, Abbild 5e5ad109, Sonde f88e54ee, auswertung wie TB-116 0b)"
shasum -a 256 $V/herkunft.py $AB shared/sperrlistensonde.py $V/auswertung.py
echo "## herkunft.register() (Soll 5acb4c19..., fehlend leer)"
$PY -W ignore -c "
import sys; sys.path.insert(0,'$V'); import herkunft
r = herkunft.register(); print('register', r['register']); print('fehlend', r['fehlend']); print('teile', len(r['teile']))" 2>&1
echo "## Sonde gegen $AB (Soll: Pfad-Bestandteile 34/0/0)"
$PY -W ignore shared/sperrlistensonde.py --abbild $AB > "$SP/sonde_0b_$M.txt" 2>&1; echo "rc $?"
grep -E "^Pfad-Bestandteile|^\(ii\)|^RUECKGABEWERT|Registertext: |BEFUND" "$SP/sonde_0b_$M.txt"
echo "## Benchmark im Modus, Repo (Soll 64fb2912...)"
bash docs/belege/TB-117/g_lauf.sh "$SP/0b_$M" benchmark bm_repo | grep -E "rc=|benchmark.json"
echo "## git status (ausserhalb docs/ muss leer sein)"; git status --porcelain -- . ':!docs'; echo "[Ende status]"
echo "## Ende"

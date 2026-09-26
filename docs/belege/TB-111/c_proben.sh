#!/bin/bash
# TB-111 C1/C3 - auswertung.py an vier Vertragsbruechen als eigener Prozess: rc und stderr.
# Vorher (Block B) und nachher (Block C) mit demselben Skript; stderr je Fall in <ziel>/<fall>.err,
# damit "Meldung wortgleich" per cmp/diff pruefbar ist. Aufruf aus der Worktree-Wurzel:
#   bash docs/belege/TB-111/c_proben.sh <ziel>      (<ziel> darf nicht existieren; Scratchpad)
set -u
Z="$1"; PY=/Users/jaquelineloffler/trading-bot/trading-env/bin/python3; BOT=turtle_soup_stocks
V=research/vorregistrierung
if [ -e "$Z" ]; then echo "ABBRUCH: $Z existiert"; exit 1; fi
mkdir -p "$Z/leer"
echo "# TB-111 C-Proben, HEAD $(git --no-optional-locks rev-parse --short HEAD), auswertung.py $(shasum -a 256 $V/auswertung.py | cut -c1-16), $(date '+%Y-%m-%d %H:%M:%S %z')"
$PY -W ignore $V/beispieldaten.py --ziel "$Z/basis" --bot $BOT > "$Z/basis.erzeugung.txt" 2>&1 || { echo "beispieldaten gescheitert"; exit 1; }
for f in spalte zelle tage; do cp -R "$Z/basis" "$Z/$f"; done
$PY -W ignore - "$Z" $BOT <<'PYEOF'
import sys, os, pandas as pd
z, bot = sys.argv[1], sys.argv[2]
p = os.path.join(z, "spalte", bot, "zellen.csv")
pd.read_csv(p, dtype=str).drop(columns=["mittlere_exposure"]).to_csv(p, index=False)
p = os.path.join(z, "zelle", bot, "zellen.csv")
df = pd.read_csv(p, dtype=str); df.loc[df.index[0], "zelle_id"] = "ausserhalb=1"; df.to_csv(p, index=False)
p = os.path.join(z, "tage", "benchmark_tagesreihen", "aktien.csv")
pd.read_csv(p, dtype=str).head(2).to_csv(p, index=False)
PYEOF
for f in leer spalte zelle tage basis; do
  a=(--rohergebnisse "$Z/$f"); [ "$f" != leer ] && a+=(--bot $BOT)
  $PY -W ignore $V/auswertung.py "${a[@]}" > "$Z/$f.out" 2> "$Z/$f.err"; rc=$?
  echo "$f: rc $rc | stderr ($(wc -c < "$Z/$f.err" | tr -d ' ') B, sha $(shasum -a 256 "$Z/$f.err" | cut -c1-16)): $(tail -1 "$Z/$f.err" | cut -c1-190)"
done

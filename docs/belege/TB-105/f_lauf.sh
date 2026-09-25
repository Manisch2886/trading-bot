#!/bin/bash
# TB-105 F1/F2 - Laeufe im Selektionsmodus auf den Snapshot der jeweiligen Wurzel, mit dem Haken
# docs/belege/TB-104/haken/sitecustomize.py (open/mkdir mit Aufrufstapel, Modulliste). Bauart TB-104 c5_lauf.sh.
# Aufruf AUS DER WURZEL (echtes Repo oder frischer Klon):
#   bash <wurzel>/docs/belege/TB-105/f_lauf.sh <laufordner> benchmark <name>   benchmark.py --ziel <laufordner>/<name>/benchmark.json
#   bash <wurzel>/docs/belege/TB-105/f_lauf.sh <laufordner> bot <name> <bot>   TB-103-Trockenlauf eines Bots
# Python immer aus dem echten Repo (trading-env liegt nicht im Klon).
set -u
SP="$1"; ART="$2"; NAME="$3"; BOT="${4:-}"
PY=/Users/jaquelineloffler/trading-bot/trading-env/bin/python3
SNAP=63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
Z="$SP/$NAME"
if [ -e "$Z" ]; then echo "ABBRUCH: $Z existiert"; exit 1; fi
mkdir -p "$Z/prot" "$Z/ziel"
echo "# TB-105 $ART $NAME $BOT, Wurzel $PWD, HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "# Arbeitsbaum shared/ strategies/ requirements.lock (leer = sauber): [$(git status --porcelain -- shared strategies requirements.lock)]"
case "$ART" in
  benchmark)  ZIEL=(research/vorregistrierung/benchmark.py --ziel "$Z/benchmark.json") ;;
  bot)        ZIEL=(docs/belege/TB-103/d_trockenlauf.py "$BOT") ;;
  *) echo "ABBRUCH: Art $ART unbekannt"; exit 1 ;;
esac
T0=$(date +%s)
env PYTHONPATH=docs/belege/TB-104/haken TB104_PROTOKOLL="$Z/prot" TB103_ZIEL="$Z/ziel" \
    TB_SELEKTIONSWURZEL="$PWD/snapshots/$SNAP" TB_SELEKTIONSHASH="$SNAP" \
    TB_SELEKTIONSCOMMIT="$(git rev-parse HEAD)" \
    "$PY" -W ignore "${ZIEL[@]}" > "$Z/ausgabe.txt" 2>&1
RC=$?
echo "$RC" > "$Z/rc"
echo "$ART $NAME $BOT rc=$RC $(( $(date +%s) - T0 ))s"
[ -f "$Z/benchmark.json" ] && shasum -a 256 "$Z/benchmark.json" | sed "s#$SP/##"
exit 0

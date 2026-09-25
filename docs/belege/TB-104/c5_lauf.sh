#!/bin/bash
# TB-104 C5/D1 - Laeufe im Selektionsmodus auf den ECHTEN Snapshot (TB_SELEKTIONS*, kein Hilfsordner),
# mit dem Haken docs/belege/TB-104/haken/sitecustomize.py (open/mkdir mit Aufrufstapel, Modulliste).
# Ausgaben NUR in <scratch>. Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-104/c5_lauf.sh <scratch> benchmark <name>     benchmark.py --ziel <scratch>/<name>/benchmark.json
#   bash docs/belege/TB-104/c5_lauf.sh <scratch> auswertung <name>    nur `import auswertung` (d1_auswertung_import.py)
#   bash docs/belege/TB-104/c5_lauf.sh <scratch> bot <name> <bot>     TB-103-Trockenlauf eines Bots (d_trockenlauf.py)
set -u
SP="$1"; ART="$2"; NAME="$3"; BOT="${4:-}"
SNAP=63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
Z="$SP/$NAME"
if [ -e "$Z" ]; then echo "ABBRUCH: $Z existiert"; exit 1; fi
mkdir -p "$Z/prot" "$Z/ziel"
echo "# TB-104 $ART $NAME $BOT, HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "# Arbeitsbaum shared/ strategies/ requirements.lock (leer = sauber): [$(git status --porcelain -- shared strategies requirements.lock)]"
case "$ART" in
  benchmark)  ZIEL=(research/vorregistrierung/benchmark.py --ziel "$Z/benchmark.json") ;;
  auswertung) ZIEL=(docs/belege/TB-104/d1_auswertung_import.py) ;;
  bot)        ZIEL=(docs/belege/TB-103/d_trockenlauf.py "$BOT") ;;
  *) echo "ABBRUCH: Art $ART unbekannt"; exit 1 ;;
esac
T0=$(date +%s)
env PYTHONPATH=docs/belege/TB-104/haken TB104_PROTOKOLL="$Z/prot" TB103_ZIEL="$Z/ziel" \
    TB_SELEKTIONSWURZEL="$PWD/snapshots/$SNAP" TB_SELEKTIONSHASH="$SNAP" \
    TB_SELEKTIONSCOMMIT="$(git rev-parse HEAD)" \
    trading-env/bin/python3 -W ignore "${ZIEL[@]}" > "$Z/ausgabe.txt" 2>&1
RC=$?
echo "$RC" > "$Z/rc"
echo "$ART $NAME $BOT rc=$RC $(( $(date +%s) - T0 ))s"
[ -f "$Z/benchmark.json" ] && shasum -a 256 "$Z/benchmark.json" | sed "s#$SP/##"
exit 0

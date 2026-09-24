#!/bin/bash
# TB-98 A1, dynamisch: EIN Probelauf (ein Bot) im Selektionsmodus mit Lesehaken.
# Aufruf aus der Repo-Wurzel:  bash docs/belege/TB-98/a1_lauf.sh <scratch> <bot>
# Schreibt nur in <scratch>/a1_ziel (Listen) und <scratch>/a1_prot (Protokoll).
set -u
SP="$1"; BOT="$2"
SNAP=63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
echo "# TB-98 A1 Probelauf $BOT, HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "# Arbeitsbaum ueber shared/ strategies/ requirements.lock:"
git status --porcelain -- shared strategies requirements.lock
mkdir -p "$SP/a1_ziel" "$SP/a1_prot"
T0=$(date +%s)
env PYTHONPATH=docs/belege/TB-98/haken \
    TB98_PROTOKOLL="$SP/a1_prot" TB98_ZIEL="$SP/a1_ziel" \
    TB_SELEKTIONSWURZEL="$PWD/snapshots/$SNAP" TB_SELEKTIONSHASH="$SNAP" \
    TB_SELEKTIONSCOMMIT="$(git rev-parse HEAD)" \
    trading-env/bin/python3 -W ignore docs/belege/TB-98/a1_probe.py "$BOT" \
    > "$SP/a1_ausgabe.txt" 2>&1
echo "rc=$? Dauer $(( $(date +%s) - T0 )) s"

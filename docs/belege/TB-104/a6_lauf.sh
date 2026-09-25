#!/bin/bash
# TB-104 A6 - legt ein Modus-Lauf eines Bots Ordner unter results/<bot>/ oder logs/<bot>/ an? (Fable 25a (2))
# Wegwerfbaum = frischer `git clone` des Repos (ohne logs/, ohne results/elliott_wave/), Modus auf den ECHTEN
# Snapshot, Lauf = TB-103-Trockenlauf (docs/belege/TB-103/d_trockenlauf.py, unveraendert) fuer EINEN Bot,
# Haken auf das Audit-Ereignis os.mkdir (os.makedirs ruft os.mkdir) mit Aufrufstapel.
# Aufruf:  bash docs/belege/TB-104/a6_lauf.sh <klon> <haken-ordner> <arbeitsordner> <bot>
set -u
K="$1"; H="$2"; A="$3"; BOT="$4"
REPO=/Users/jaquelineloffler/trading-bot
SNAP=63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
mkdir -p "$A/prot" "$A/ziel"
cd "$K" || exit 1
echo "# TB-104 A6, Klon HEAD $(git rev-parse --short HEAD), Bot $BOT, $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "vorher:  $(ls -d results/$BOT logs logs/$BOT 2>&1 | tr '\n' ' ')"
echo "Arbeitsbaum shared/ strategies/ lock (leer = sauber): [$(git status --porcelain -- shared strategies requirements.lock)]"
env PYTHONPATH="$H" TB104_A6_PROTOKOLL="$A/prot" TB103_ZIEL="$A/ziel" \
    TB_SELEKTIONSWURZEL="$REPO/snapshots/$SNAP" TB_SELEKTIONSHASH="$SNAP" \
    TB_SELEKTIONSCOMMIT="$(git rev-parse HEAD)" \
    "$REPO/trading-env/bin/python3" -W ignore docs/belege/TB-103/d_trockenlauf.py "$BOT" > "$A/ausgabe.txt" 2>&1
echo "rc=$?"
echo "nachher: $(ls -d results/$BOT logs logs/$BOT 2>&1 | tr '\n' ' ')"
echo "git status --porcelain --ignored (Klon):"
git status --porcelain --ignored
echo "## os.mkdir-Ereignisse (Pfad <- Aufrufstapel innen zuerst), Klonpfad als <klon>:"
cat "$A"/prot/*.tsv | grep -v '^#' | awk -F'\t' '{print $2"  <-  "$3}' | sed "s#$K#<klon>#g; s#$A#<arbeit>#g" | sort | uniq -c
echo "## Modus-Zeilen aus der Ausgabe:"
grep '\[paths\]' "$A/ausgabe.txt" | head -3

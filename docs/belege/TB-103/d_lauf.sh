#!/bin/bash
# TB-103 Block D - Trockenlauf aller neun Bots, je Bot ein Prozess, mit Lesehaken
# und Aufrufstapel (docs/belege/TB-98/haken/sitecustomize.py, unveraendert).
# Lauf-Typ wie TB-98 a1_neun.sh: TB_SELEKTIONSWURZEL auf den ECHTEN Snapshot,
# kein Hilfsordner. Ausgaben NUR in den Scratchpad.
# Aufruf aus der Repo-Wurzel:  bash docs/belege/TB-103/d_lauf.sh <scratch> <modus|ohne>
set -u
SP="$1"; ART="$2"
SNAP=63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
BOTS="elliott_wave t3_supertrend rsi2_crypto turtle_soup_crypto volatility_breakout_crypto elliott_wave_stocks rsi2_mean_reversion turtle_soup_stocks volatility_breakout"
echo "# TB-103 D neun Bots '$ART', HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "# Arbeitsbaum ueber shared/ strategies/ requirements.lock (leer = sauber):"
git status --porcelain -- shared strategies requirements.lock
for BOT in $BOTS; do
  Z="$SP/$ART/$BOT"
  if [ -e "$Z" ]; then echo "ABBRUCH: $Z existiert"; exit 1; fi
  mkdir -p "$Z/ziel" "$Z/prot"
  T0=$(date +%s)
  if [ "$ART" = modus ]; then
    env PYTHONPATH=docs/belege/TB-98/haken TB98_PROTOKOLL="$Z/prot" TB103_ZIEL="$Z/ziel" \
        TB_SELEKTIONSWURZEL="$PWD/snapshots/$SNAP" TB_SELEKTIONSHASH="$SNAP" \
        TB_SELEKTIONSCOMMIT="$(git rev-parse HEAD)" \
        trading-env/bin/python3 -W ignore docs/belege/TB-103/d_trockenlauf.py "$BOT" > "$Z/ausgabe.txt" 2>&1
  else
    env PYTHONPATH=docs/belege/TB-98/haken TB98_PROTOKOLL="$Z/prot" TB103_ZIEL="$Z/ziel" \
        trading-env/bin/python3 -W ignore docs/belege/TB-103/d_trockenlauf.py "$BOT" > "$Z/ausgabe.txt" 2>&1
  fi
  RC=$?
  echo "$RC" > "$Z/rc"
  echo "$BOT $ART rc=$RC $(( $(date +%s) - T0 ))s"
done
echo FERTIG

#!/bin/bash
# TB-98 A1, dynamisch, alle neun Bots: der UNVERAENDERTE Erzeuger ueber den
# Umschlag a1_probe.py (Ausgabe nur in den Scratchpad), je Bot ein Prozess,
# einmal MIT Selektionsmodus (Lesehaken aktiv) und einmal OHNE.
# Aufruf aus der Repo-Wurzel:  bash docs/belege/TB-98/a1_neun.sh <scratch>
set -u
SP="$1"
SNAP=63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
BOTS="elliott_wave t3_supertrend rsi2_crypto turtle_soup_crypto volatility_breakout_crypto elliott_wave_stocks rsi2_mean_reversion turtle_soup_stocks volatility_breakout"
echo "# TB-98 A1 neun Bots, HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "# Arbeitsbaum ueber shared/ strategies/ requirements.lock (leer = sauber):"
git status --porcelain -- shared strategies requirements.lock
for BOT in $BOTS; do
  for ART in modus ohne; do
    Z="$SP/a1n/$ART/$BOT"; mkdir -p "$Z/ziel" "$Z/prot"
    T0=$(date +%s)
    if [ $ART = modus ]; then
      env PYTHONPATH=docs/belege/TB-98/haken TB98_PROTOKOLL="$Z/prot" TB98_ZIEL="$Z/ziel" \
          TB_SELEKTIONSWURZEL="$PWD/snapshots/$SNAP" TB_SELEKTIONSHASH="$SNAP" \
          TB_SELEKTIONSCOMMIT="$(git rev-parse HEAD)" \
          trading-env/bin/python3 -W ignore docs/belege/TB-98/a1_probe.py "$BOT" > "$Z/ausgabe.txt" 2>&1
    else
      env TB98_ZIEL="$Z/ziel" \
          trading-env/bin/python3 -W ignore docs/belege/TB-98/a1_probe.py "$BOT" > "$Z/ausgabe.txt" 2>&1
    fi
    RC=$?
    echo "$BOT $ART rc=$RC $(( $(date +%s) - T0 ))s geschrieben=$(ls "$Z/ziel" | wc -l | tr -d ' ') | $(grep -h 'Warnung:\|^Geladen:\|Abbruch\|Error' "$Z/ausgabe.txt" | tr '\n' ' ' | sed "s#$PWD/##g")"
  done
done
echo FERTIG

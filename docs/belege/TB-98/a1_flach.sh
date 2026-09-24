#!/bin/bash
# TB-98 A1, Zusatzmessung: Liest der Erzeuger AUSSCHLIESSLICH aus dem Snapshot,
# wenn die Symbollisten gefunden werden?
#
# Im Scratchpad entsteht ein Ordner aus VERKNUEPFUNGEN auf den echten Snapshot
# (alle Dateien, MANIFEST.json, config/) und ZUSAETZLICH die zwei Symbollisten
# flach in der Wurzel (Verknuepfung auf <snapshot>/config/<liste>) - so, wie
# shared/paths.py sie unter dem Modus erwartet (CONFIG_DIR = Snapshot-Wurzel).
# Der Modus prueft nur das Feld `snapshot_hash` im MANIFEST, nicht die Dateien
# (shared/paths.py::_lies_snapshot_hash); deshalb laesst er diesen Ordner zu.
# Am Snapshot selbst wird nichts geaendert. Der Erzeuger bricht wie in
# a1_neun.sh an der Kennzeichnung ab und schreibt nichts; gemessen werden nur
# die geoeffneten Dateien und die Ladezeile.
#
# Aufruf aus der Repo-Wurzel:  bash docs/belege/TB-98/a1_flach.sh <scratch>
set -u
SP="$1"
SNAP=63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
ECHT="$PWD/snapshots/$SNAP"
F="$SP/snapflach/$SNAP"
mkdir -p "$F"
for d in "$ECHT"/*; do ln -s "$d" "$F/$(basename "$d")"; done
ln -s "$ECHT/config/top25_symbols.txt" "$F/top25_symbols.txt"
ln -s "$ECHT/config/sp500_top150.txt" "$F/sp500_top150.txt"
echo "# TB-98 A1 flach, HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "# Verknuepfungen im Hilfsordner: $(ls "$F" | wc -l | tr -d ' ') (Snapshot: $(ls "$ECHT" | wc -l | tr -d ' ') + 2 flache Listen)"
BOTS="elliott_wave t3_supertrend rsi2_crypto turtle_soup_crypto volatility_breakout_crypto elliott_wave_stocks rsi2_mean_reversion turtle_soup_stocks volatility_breakout"
for BOT in $BOTS; do
  Z="$SP/a1f/modus/$BOT"; mkdir -p "$Z/ziel" "$Z/prot"
  T0=$(date +%s)
  env PYTHONPATH=docs/belege/TB-98/haken TB98_PROTOKOLL="$Z/prot" TB98_ZIEL="$Z/ziel" \
      TB_SELEKTIONSWURZEL="$F" TB_SELEKTIONSHASH="$SNAP" \
      TB_SELEKTIONSCOMMIT="$(git rev-parse HEAD)" \
      trading-env/bin/python3 -W ignore docs/belege/TB-98/a1_probe.py "$BOT" > "$Z/ausgabe.txt" 2>&1
  RC=$?
  echo "$BOT rc=$RC $(( $(date +%s) - T0 ))s geschrieben=$(ls "$Z/ziel" | wc -l | tr -d ' ') | $(grep -h 'Warnung:\|^Geladen:\|Abbruch\|Error' "$Z/ausgabe.txt" | tr '\n' ' ' | sed "s#$SP/##g")"
done
echo FERTIG

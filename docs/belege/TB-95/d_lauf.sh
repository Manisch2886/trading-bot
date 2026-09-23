#!/bin/bash
# TB-95 Block D - Modus-Lauf mit Lesehaken und Aufrufstapel (D1) und Stoerprobe (D2).
# Aufbau des Hilfsordners wie TB-92 (docs/belege/TB-92/a1b_modusnachweis.sh): data/ -> je eine
# Verknuepfung auf die CSV der Snapshot-Wurzel, config/ -> <Snapshot>/config/, alles andere -> Repo.
# ⛔ Alle Ziele im Scratchpad (Argument 1), nie in ergebnisse/. Die Originale der neun Listen
# werden nur gelesen; die Stoerprobe arbeitet auf einer KOPIE (cp, keine Verknuepfung).
# Aufruf aus der Repo-Wurzel:  bash docs/belege/TB-95/d_lauf.sh <scratchpad>
set -u
SP="$1"; REPO="$(pwd)"
SNAP="$REPO/snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2"
B="$REPO/docs/belege/TB-95"
Z=research/vorregistrierung/ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json
L=research/tb24_haltedauern/daten

baue() {  # $1 = Hilfsordner; $2 = "kopie" -> research/tb24_haltedauern als echte Kopie
  local H="$1"
  mkdir -p "$H/data" "$H/research"
  for f in "$SNAP"/*.csv; do ln -s "$f" "$H/data/$(basename "$f")"; done
  ln -s "$SNAP/config" "$H/config"
  for d in "$REPO"/*; do n=$(basename "$d"); case "$n" in data|config|research|trading-env|snapshots) ;; *) ln -s "$d" "$H/$n";; esac; done
  for d in "$REPO"/research/*; do
    n=$(basename "$d")
    if [ "$n" = tb24_haltedauern ] && [ "${2:-}" = kopie ]; then cp -R "$d" "$H/research/$n"; else ln -s "$d" "$H/research/$n"; fi
  done
  echo "  $H: data/ $(ls "$H/data" | wc -l | tr -d ' ') Verknuepfungen, tb24 = $( [ -L "$H/research/tb24_haltedauern" ] && echo Verknuepfung || echo KOPIE )"
}

lauf() {  # $1 = Name, $2 = Hilfsordner, $3 = Protokollordner oder leer
  local T0=$(date +%s)
  if [ -n "$3" ]; then
    mkdir -p "$3"
    env PYTHONPATH="$B/haken" TB92_PROTOKOLL="$3" TB30A_BASE_DIR="$2" \
      trading-env/bin/python3 research/vorregistrierung/benchmark.py --ziel "$SP/$1.json" > "$SP/$1_ausgabe.txt" 2>&1
  else
    env TB30A_BASE_DIR="$2" \
      trading-env/bin/python3 research/vorregistrierung/benchmark.py --ziel "$SP/$1.json" > "$SP/$1_ausgabe.txt" 2>&1
  fi
  local rc=$?
  echo "  Lauf $1: rc=$rc, Dauer $(( $(date +%s) - T0 )) s$( [ -n "$3" ] && echo ", Prozesse $(ls "$3" | wc -l | tr -d ' ')")"
  echo "    sha256 $(shasum -a 256 "$SP/$1.json" | cut -c1-64)"
  cmp -s "$Z" "$SP/$1.json" && echo "    BYTEGLEICH mit $Z" || echo "    VERSCHIEDEN von $Z"
}

echo "# Originale der neun Listen VORHER"; shasum -a 256 $L/*_alle_trades.csv
echo "# D1 - Modus-Lauf mit Lesehaken und Stapel"
baue "$SP/d1_hilf"
lauf d1_modus "$SP/d1_hilf" "$SP/d1_protokoll"

echo "# D2 (b1) - Kopie, EINE Zeile entfernt (volatility_breakout_crypto, erste Zeile mit Einstieg 2024)"
baue "$SP/d2b1_hilf" kopie
trading-env/bin/python3 "$B/d_stoerung.py" eine_zeile "$SP/d2b1_hilf/$L/volatility_breakout_crypto_alle_trades.csv"
lauf d2b1_eine_zeile "$SP/d2b1_hilf" ""

echo "# D2 (b2) - Kopie, zwei von drei Datenzeilen entfernt (volatility_breakout_crypto) - ueber die Schwelle der Faltenlaenge"
baue "$SP/d2b2_hilf" kopie
trading-env/bin/python3 "$B/d_stoerung.py" jede_dritte "$SP/d2b2_hilf/$L/volatility_breakout_crypto_alle_trades.csv"
lauf d2b2_schwelle "$SP/d2b2_hilf" ""

echo "# Originale der neun Listen NACHHER"; shasum -a 256 $L/*_alle_trades.csv

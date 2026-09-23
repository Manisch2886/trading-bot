#!/bin/bash
# TB-92 A1b (Fable 23e): Reproduzierbarkeitsnachweis der vollzogenen Tabelle
# auf dem registrierten Snapshot, NICHT auf data/. benchmark.py liest nicht
# ueber shared/paths.py (TB_SELEKTIONSWURZEL wirkt nicht), deshalb Hilfsordner
# nach dem Weg aus TB-93 (b4_gegenprobe.sh): data/ -> je eine Verknuepfung auf
# die 223 CSV der Snapshot-Wurzel, config/ -> <Snapshot>/config/; die
# Code-Ordner, die ueber BASE_DIR in sys.path kommen, zeigen aufs Repo.
# Ziele im Beleg-Ordner, nie in ergebnisse/. Zwei Laeufe: (1) nackt = der
# Nachweis, (2) mit Lesehaken = welche Dateien gelesen wurden.
set -u
SP="$1"; REPO="$(pwd)"
SNAP="$REPO/snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2"
H="$SP/modus_hilfsordner"; B="$REPO/docs/belege/TB-92"
mkdir -p "$H/data" "$H/research"
for f in "$SNAP"/*.csv; do ln -s "$f" "$H/data/$(basename "$f")"; done
ln -s "$SNAP/config" "$H/config"
# Alles andere, was ueber BASE_DIR erreicht wird (Code-Ordner, research/*),
# zeigt aufs Repo - nur data/ und config/ kommen aus dem Snapshot.
# (Erster Anlauf mit drei Einzelordnern scheiterte am Import von
# research/universum_trockenlauf; verworfen, nichts geschrieben.)
for d in "$REPO"/*; do n=$(basename "$d"); case "$n" in data|config|research|trading-env|snapshots) ;; *) ln -s "$d" "$H/$n";; esac; done
for d in "$REPO"/research/*; do ln -s "$d" "$H/research/$(basename "$d")"; done
echo "Verknuepfungen data/: $(ls "$H/data" | wc -l | tr -d ' ')"
T0=$(date +%s)
TB30A_BASE_DIR="$H" trading-env/bin/python3 research/vorregistrierung/benchmark.py \
    --ziel "$B/benchmark_modusnachweis.json" > "$B/a1b_lauf1_ausgabe.txt" 2>&1
echo "Lauf 1 rc=$? Dauer $(( $(date +%s) - T0 )) s"
T0=$(date +%s)
TB30A_BASE_DIR="$H" trading-env/bin/python3 "$B/a1b_lesehaken.py" "$SP/a1b_geoeffnet.tsv" \
    research/vorregistrierung/benchmark.py --ziel "$SP/benchmark_modusnachweis_lauf2.json" \
    > "$SP/a1b_lauf2_ausgabe.txt" 2>&1
echo "Lauf 2 rc=$? Dauer $(( $(date +%s) - T0 )) s"
Z=research/vorregistrierung/ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json
cmp "$Z" "$B/benchmark_modusnachweis.json" && echo "Lauf 1 BYTEGLEICH mit $Z"
cmp "$Z" "$SP/benchmark_modusnachweis_lauf2.json" && echo "Lauf 2 BYTEGLEICH mit $Z"
shasum -a 256 "$Z" "$B/benchmark_modusnachweis.json" "$SP/benchmark_modusnachweis_lauf2.json"

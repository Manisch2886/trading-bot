#!/bin/bash
# TB-138 0b / D0 - Ausgangswerte (Bauart TB-115 0b_ausgang.sh). Rein lesend.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-138/0b_ausgang.sh <marke>
# <marke> = ausgang (0b) oder nachher (D0). Die Zeitzeile steht allein, damit
# der Vergleich D0 gegen 0b sie mit HEAD ausnehmen kann.
set -u
M="$1"; PY=trading-env/bin/python3
S=snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
R=docs/VORREGISTRIERUNG_neuselektion.md
AB=research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json
echo "# TB-138 0b ($M)"
echo "ZEIT $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "HEAD $(git rev-parse HEAD)"
echo "## Interpreter (Soll: startet; 3.9.6)"
$PY -B -c "import sys; print(sys.version)" 2>&1; echo "rc $?"
echo "## Register (Soll: 11581 Zeilen, 8d505a38...)"
wc -l < "$R" | tr -d ' '
shasum -a 256 "$R"
echo "## Abbild (Soll: beginnt 46f0ad5d1d83a253)"
shasum -a 256 "$AB"
echo "## requirements.lock (nur messen)"
shasum -a 256 requirements.lock
echo "## Universumsdateien im Snapshot (Soll: 6acba892..., 3afc95a4...)"
shasum -a 256 "$S/config/sp500_top150.txt" "$S/config/top25_symbols.txt"
echo "## Umgebungsvariablen des Selektionslaufs (shared/paths.py Z. 205-208), gesetzt?"
for v in TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT; do
  if [ -n "${!v+x}" ]; then echo "$v gesetzt"; else echo "$v nicht gesetzt"; fi
done
echo "## snapshot.py --pruefen (ohne --json; Soll rc 0)"
$PY -B shared/snapshot.py --pruefen "$S" 2>&1; echo "rc $?"
echo "## Dateiliste des Snapshots (nur messen; 226 Dateien)"
L=$(find "$S" -type f | LC_ALL=C sort)
echo "Dateien $(printf '%s\n' "$L" | wc -l | tr -d ' ')"
printf '%s\n' "$L" | while IFS= read -r f; do shasum -a 256 "$f"; done | shasum -a 256 | sed 's/  -$/  (sha256 ueber "sha256  Pfad", sortiert)/'
echo "## git status ausserhalb docs/ (muss leer sein)"; git status --porcelain -- . ':!docs'; echo "[Ende status]"
echo "## Ende"

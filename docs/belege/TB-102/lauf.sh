#!/bin/bash
# TB-102 - EIN Lauf von messgroessen.py (unveraendert) mit Lesehaken.
# Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-102/lauf.sh <scratch-ordner> <art> [<basis>]
#   art = ohne   : kein Modus (BASE_DIR = Repo-Wurzel)
#   art = modus  : TB30A_BASE_DIR=<snapshot> und die drei TB_SELEKTIONS*-Variablen
#   art = basis  : nur TB30A_BASE_DIR=<basis> (Zusatzprobe, Hilfsbaum)
#   art = selektion : NUR die drei TB_SELEKTIONS*-Variablen der Bots, ohne TB30A_BASE_DIR (Zusatzprobe Z3)
# Schreibt NUR nach <scratch-ordner>/{messgroessen.json,prot/,ausgabe.txt}.
# Lesehaken: docs/belege/TB-98/haken/sitecustomize.py (per PYTHONPATH, unveraendert).
set -u
SP="$1"; ART="$2"; BASIS="${3:-}"
SNAP=63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
if [ -e "$SP" ]; then echo "ABBRUCH: $SP existiert"; exit 1; fi
mkdir -p "$SP/prot"
echo "# TB-102 Lauf '$ART', HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
case "$ART" in
  ohne)  UMG=(TB102_ART=ohne) ;;
  modus) UMG=(TB30A_BASE_DIR="$PWD/snapshots/$SNAP"
              TB_SELEKTIONSWURZEL="$PWD/snapshots/$SNAP" TB_SELEKTIONSHASH="$SNAP"
              TB_SELEKTIONSCOMMIT="$(git rev-parse HEAD)") ;;
  basis) UMG=(TB30A_BASE_DIR="$BASIS") ;;
  selektion) UMG=(TB_SELEKTIONSWURZEL="$PWD/snapshots/$SNAP" TB_SELEKTIONSHASH="$SNAP"
              TB_SELEKTIONSCOMMIT="$(git rev-parse HEAD)") ;;
  *) echo "unbekannte Art"; exit 1 ;;
esac
echo "# Umgebung: ${UMG[*]:-(keine)}"
T0=$(date +%s)
env PYTHONPATH=docs/belege/TB-98/haken TB98_PROTOKOLL="$SP/prot" "${UMG[@]}" \
    trading-env/bin/python3 -W ignore research/vorregistrierung/messgroessen.py \
    --ziel "$SP/messgroessen.json" > "$SP/ausgabe.txt" 2>&1
RC=$?
echo "rc=$RC Dauer $(( $(date +%s) - T0 )) s"
echo "## Ausgabe (letzte 15 Zeilen)"
tail -15 "$SP/ausgabe.txt"
if [ -f "$SP/messgroessen.json" ]; then
  echo "## Ergebnis"
  shasum -a 256 "$SP/messgroessen.json"
else
  echo "## Ergebnis: keine Datei geschrieben"
fi

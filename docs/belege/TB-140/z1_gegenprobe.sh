#!/bin/bash
# TB-140 Z1 - Gegenprobe an zwei kleinen Ordnern in einem frischen Ordner unter $TMPDIR (dorthin
# schreibt das Skript). Die Kursspalten tragen den Text x. Der zweite Ordner traegt eine leere Tagesreihe.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-140/z1_gegenprobe.sh
# Rueckgabe: 0 die Probe beisst (alle Sollzeilen da), 1 eine Sollzeile fehlt, 2 nicht messbar.
set -u
PY="${PY:-trading-env/bin/python3}"
Z="${Z:-docs/belege/TB-140/z1_close_je_datei.py}"
T="$(mktemp -d "${TMPDIR:-/tmp}/tb140_z1_gegenprobe.XXXXXX")" || { echo "NICHT MESSBAR: kein Ordner unter TMPDIR"; exit 2; }
G="$T/eins"; L="$T/leer"
mkdir -p "$G/config" "$L/config"
printf 'AAA\n' > "$G/config/sp500_top150.txt"
printf 'BBBUSDT\nCCCUSDT\n' > "$G/config/top25_symbols.txt"
cat > "$G/AAA_1d.csv" <<'CSV'
open_time,open,high,low,close,volume
2026-08-28,x,x,x,x,x
2026-08-31,x,x,x,x,x
2026-09-01,,,,,x
CSV
cat > "$G/BBBUSDT_1d.csv" <<'CSV'
open_time,open,high,low,close,volume
2026-09-11,x,x,x,x,x
2026-09-12,x,x,x,,x
2026-09-13,x,x,x,NaN,x
2026-09-14,x,x,x,x,x
CSV
cp "$G/config/sp500_top150.txt" "$G/config/top25_symbols.txt" "$L/config/"; : > "$L/AAA_1d.csv"
echo "# TB-140 Z1 GEGENPROBE"; echo "Ordner $T"
echo "## erster Ordner (Soll rc 1)"
$PY -B "$Z" --snapshot "$G" > "$T/a.txt" 2>&1; RC1=$?; cat "$T/a.txt"; echo "rc $RC1"
echo "## zweiter Ordner, leere Tagesreihe (Soll rc 2)"
$PY -B "$Z" --snapshot "$L" > "$T/b.txt" 2>&1; RC2=$?; cat "$T/b.txt"; echo "rc $RC2"
zahl() { awk -F'\t' "$1" "$2" | wc -l | tr -d ' '; }
S1=$(zahl '$1=="DATEI" && $2=="aktien" && $3=="AAA_1d.csv" && $4==3 && $5==1 && $9=="2026-09-01" && $10=="2026-08-31"' "$T/a.txt")
S2=$(zahl '$1=="DATEI" && $2=="krypto" && $3=="BBBUSDT_1d.csv" && $4==4 && $5==2 && $6==1 && $7==1' "$T/a.txt")
S3=$(zahl '$1=="FALL" && $2=="z1"' "$T/a.txt")
S4=$(grep -c "TRIFFT NICHT ZU" "$T/a.txt")
S5=$(grep -c "Symbole ohne _1d-Reihe: 1 \['CCCUSDT'\]" "$T/a.txt")
S6=$(grep -c "NICHT LESBAR: leer" "$T/b.txt")
echo "## Soll"
echo "erster Ordner: rc $RC1 (Soll 1) · DATEI aktien AAA $S1 (Soll 1) · DATEI krypto BBBUSDT $S2 (Soll 1) · FALL $S3 (Soll 3) · TRIFFT NICHT ZU $S4 (Soll 2) · Symbole ohne _1d-Reihe CCCUSDT $S5 (Soll 1)"
echo "zweiter Ordner: rc $RC2 (Soll 2) · NICHT LESBAR: leer $S6 (Soll 1)"
if [ "$RC1" = 1 ] && [ "$RC2" = 2 ] && [ "$S1$S2$S3$S4$S5$S6" = "113211" ]; then echo "GEGENPROBE: beisst"; echo "## Ende"; exit 0; fi
if [ "$RC1" = 2 ]; then echo "GEGENPROBE: NICHT MESSBAR"; echo "## Ende"; exit 2; fi
echo "GEGENPROBE: beisst NICHT"; echo "## Ende"; exit 1

#!/bin/bash
# TB-140 V6 - Gegenprobe zu v6_zeile.py an sieben kleinen Texten; die Kursspalten tragen den Text x.
# Schreibt nichts. Aufruf aus der Repo-Wurzel: bash docs/belege/TB-140/v6_gegenprobe.sh
# Rueckgabe: 0 alle sieben Rueckgaben wie das Soll (die Probe beisst), 1 eine weicht ab, 2 nicht messbar.
set -u
PY="${PY:-trading-env/bin/python3}"
ZP="${ZP:-docs/belege/TB-140/v6_zeile.py}"
IST=""
probe() {  # $1 Name, $2 Soll; der Text kommt von stdin
  echo "## $1 (Soll rc $2)"
  $PY -B "$ZP" 2026-09-01; local rc=$?
  echo "rc $rc"; IST="$IST$rc"
}
echo "# TB-140 V6 GEGENPROBE"
[ -s "$ZP" ] && command -v "$PY" >/dev/null 2>&1 || { echo "GEGENPROBE: NICHT MESSBAR: $ZP oder $PY fehlt"; exit 2; }
probe "G1 Zeile mit close" 1 <<'CSV'
open_time,open,high,low,close,volume
2026-08-31,x,x,x,x,x
2026-09-01,x,x,x,x,x
CSV
probe "G2 close leer" 0 <<'CSV'
open_time,open,high,low,close,volume
2026-08-31,x,x,x,x,x
2026-09-01,,,,,x
CSV
probe "G3 close mit Fehlwert-Text NaN" 0 <<'CSV'
open_time,open,high,low,close,volume
2026-09-01,x,x,x,NaN,x
CSV
probe "G4 Datum fehlt" 1 <<'CSV'
open_time,open,high,low,close,volume
2026-08-31,x,x,x,x,x
CSV
probe "G5 Zeile doppelt" 1 <<'CSV'
open_time,open,high,low,close,volume
2026-09-01,,,,,x
2026-09-01,,,,,x
CSV
probe "G6 leere Eingabe" 2 < /dev/null
probe "G7 Kopfzeile ohne close" 2 <<'CSV'
open_time,open,high,low,volume
2026-09-01,x,x,x,x
CSV
echo "## Soll"
echo "Rueckgaben $IST (Soll 1001122)"
if [ "$IST" = "1001122" ]; then echo "GEGENPROBE: beisst"; exit 0; fi
echo "GEGENPROBE: beisst NICHT"; exit 1

#!/bin/bash
# TB-140 Z2 - was docs/ERGEBNIS_TB-47_snapshotgrenze.md zur Herkunft von 5.4.0 sagt. Rein lesend.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-140/z2_tb47.sh
# Rueckgabe: 0 gelesen (das Urteil liest die Sitzung aus der Ausgabe), 2 nicht messbar (die Datei fehlt oder ist leer).
set -u
PY="${PY:-trading-env/bin/python3}"
E=docs/ERGEBNIS_TB-47_snapshotgrenze.md
J=research/snapshotgrenze/ergebnisse/eingaben.json
echo "# TB-140 Z2"; echo "ZEIT $(date '+%Y-%m-%d %H:%M:%S %z')"; echo "HEAD $(git --no-optional-locks rev-parse HEAD)"
if [ ! -s "$E" ]; then echo "NICHT MESSBAR: $E fehlt oder ist leer"; echo "## Ende"; exit 2; fi
echo "## Datei"; echo "Zeilen $(wc -l < "$E" | tr -d ' '), Bytes $(wc -c < "$E" | tr -d ' ')"; shasum -a 256 "$E"
echo "## Feld kalender in $J (nur dieses Feld; die Datei wird nicht geaendert)"
$PY -B -c "import json,sys
try:
    print(json.dumps(json.load(open(sys.argv[1], encoding='utf-8')).get('kalender'), ensure_ascii=False, sort_keys=True))
except Exception as e:
    print('Feld kalender NICHT LESBAR: %s (ohne Einfluss auf die Rueckgabe)' % type(e).__name__)" "$J"
for m in '5\.4\.0' 'cloud' 'eingaben\.json' 'kalender' 'paket_vorhanden' 'nachinstall' 'python'; do
  echo "## Muster $m (ohne Gross/Klein): $(grep -c -i -- "$m" "$E") Zeilen"
  grep -n -i -- "$m" "$E"
done
echo "## Jede Zeile mit 5.4.0 mit drei Zeilen davor und danach"
grep -n -B3 -A3 -- '5\.4\.0' "$E"
echo "## Ende"
exit 0

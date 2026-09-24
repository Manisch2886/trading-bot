#!/bin/bash
# TB-98 - sha256 aller Pfade aus pfade.txt (28 Pfade aus TB-96/TB-97, die 18
# uebrigen Dateien unter tb24_haltedauern/daten/, Erzeuger, alle_bots.py, alles
# unter vorregistrierung/ergebnisse/). Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-98/hashes.sh <Bezeichnung>
echo "# TB-98 sha256 $1, HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
while read -r p; do shasum -a 256 "$p"; done < docs/belege/TB-98/pfade.txt

#!/bin/bash
# TB-97 - sha256 der 28 Pfade aus TB-96 (pfade_28.txt), Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-97/hashes.sh <Bezeichnung>
echo "# TB-97 sha256 $1, HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
while read -r p; do shasum -a 256 "$p"; done < docs/belege/TB-97/pfade_28.txt

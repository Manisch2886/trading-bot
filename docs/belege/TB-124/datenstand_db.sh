#!/bin/bash
# TB-124 0f / E1 - Datenstand data/ (herkunft.datenstand, Soll d9449faf... bei 223 Dateien) und sha256 der *.db
# (Repo-Wurzel und strategies/), Bauart docs/belege/TB-109/hashes.sh (7)/(8). Nur lesend.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-124/datenstand_db.sh <marke>
set -u
V=research/vorregistrierung
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
echo "# TB-124 Datenstand/db ($1), HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## Datenstand data/ (herkunft.datenstand)"
trading-env/bin/python3 -W ignore -c "import sys; sys.path.insert(0,'$V'); import herkunft; print(herkunft.datenstand('data'))" 2>&1 | tail -2
echo "## sha256 *.db (Repo-Wurzel und strategies/)"
for f in $(ls *.db strategies/*/*.db 2>/dev/null | sort); do shasum -a 256 "$f"; done
echo "## Ende"

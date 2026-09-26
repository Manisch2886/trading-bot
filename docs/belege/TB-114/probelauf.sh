#!/bin/bash
# TB-114 (Kopie von TB-113 probelauf.sh): Probelauf des Einsetzskripts gegen eine Kopie des Registers, dann Zitatpruefung gegen die Kopie.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-114/probelauf.sh <kopie>
export TB114_PROBE="$1"
trading-env/bin/python3 docs/belege/TB-114/eintrag_register_45.py; echo "eintrag rc $?"
trading-env/bin/python3 docs/belege/TB-114/c2_zitate.py | tail -3; echo "c2 rc ${PIPESTATUS[0]}"

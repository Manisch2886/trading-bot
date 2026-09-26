#!/bin/bash
# TB-113 (Kopie von TB-110 probelauf.sh): Probelauf des Einsetzskripts gegen eine Kopie des Registers, dann Zitatpruefung gegen die Kopie.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-113/probelauf.sh <kopie>
export TB113_PROBE="$1"
trading-env/bin/python3 docs/belege/TB-113/eintrag_register_44.py; echo "eintrag rc $?"
trading-env/bin/python3 docs/belege/TB-113/c2_zitate.py | tail -3; echo "c2 rc ${PIPESTATUS[0]}"

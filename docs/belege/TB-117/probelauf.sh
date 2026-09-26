#!/bin/bash
# TB-117 (Kopie von TB-114 probelauf.sh): Probelauf des Einsetzskripts gegen eine Kopie des Registers, dann
# Zitat- und R-Bausteinpruefung gegen die Kopie. Aufruf aus der Repo-Wurzel: bash docs/belege/TB-117/probelauf.sh <kopie>
export TB117_PROBE="$1"
trading-env/bin/python3 docs/belege/TB-117/eintrag_register_46.py; echo "eintrag rc $?"
trading-env/bin/python3 docs/belege/TB-117/a3_zitate.py | tail -3; echo "a3 rc ${PIPESTATUS[0]}"
trading-env/bin/python3 docs/belege/TB-117/a2_r_diff.py | tail -2; echo "a2 rc ${PIPESTATUS[0]}"

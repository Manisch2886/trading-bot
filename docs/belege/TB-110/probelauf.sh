#!/bin/bash
# TB-110: Probelauf des Einsetzskripts gegen eine Kopie des Registers, dann Zitatpruefung gegen die Kopie.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-110/probelauf.sh <kopie>
export TB110_PROBE="$1"
trading-env/bin/python3 docs/belege/TB-110/eintrag_register_43.py; echo "eintrag rc $?"
trading-env/bin/python3 docs/belege/TB-110/d2_zitate.py | tail -3; echo "d2 rc ${PIPESTATUS[0]}"

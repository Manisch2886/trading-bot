#!/bin/bash
# TB-114 B1 - register() vollstaendig (Hash, Teile, fehlend) als JSON, dazu der Hash von herkunft.py.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-114/b1_register.sh <ausgabe.json>
set -u
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
trading-env/bin/python3 -W ignore -c "
import sys, json; sys.path.insert(0, 'research/vorregistrierung'); import herkunft
print(json.dumps(herkunft.register(), indent=1, sort_keys=True))" > "$1"
echo "herkunft.py $(shasum -a 256 research/vorregistrierung/herkunft.py | cut -c1-64)"
echo "register()-JSON $(shasum -a 256 "$1" | cut -c1-64)  register $(grep '"register"' "$1")"

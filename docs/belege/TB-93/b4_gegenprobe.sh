#!/bin/bash
# TB-93 B4-Gegenprobe (ZUSATZ der Mac-Sitzung, nicht im Auftrag verlangt):
# derselbe Code (HEAD, messgroessen.py 623f8d77) auf den EINGABEN des Commits,
# der ergebnisse/messgroessen.json erzeugt hat (a2fcf01, 14.09.2026).
# Ziel liegt im Scratchpad -> nichts im Repo geschrieben. TB30A_BASE_DIR lenkt
# data/, config/ und research/tb24_haltedauern/ um; ERGEBNISSE bleibt am Modul.
set -u
S="$1"   # Scratchpad
mkdir -p "$S/stand_a2fcf01"
git archive a2fcf01 data config research/tb24_haltedauern/ergebnisse | tar -x -C "$S/stand_a2fcf01"
TB30A_BASE_DIR="$S/stand_a2fcf01" trading-env/bin/python3 research/vorregistrierung/messgroessen.py \
    --ziel "$S/gegenprobe_a2fcf01.json"
cmp research/vorregistrierung/ergebnisse/messgroessen.json "$S/gegenprobe_a2fcf01.json" && echo BYTEGLEICH

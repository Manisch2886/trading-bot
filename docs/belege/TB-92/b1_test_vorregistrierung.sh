#!/bin/bash
# TB-92 B1: test_vorregistrierung.py vollstaendig, trading-env (3.9.6), ohne Eingriff.
cd "$(dirname "$0")/../../.."
B=docs/belege/TB-92
echo "HEAD $(git rev-parse --short HEAD)  Python $(trading-env/bin/python3 -V 2>&1)  Start $(date -u +%FT%TZ)" > $B/b1_kopf.txt
T0=$(date +%s)
trading-env/bin/python3 research/vorregistrierung/test_vorregistrierung.py > $B/b1_ausgabe.txt 2>&1
RC=$?
echo "rc=$RC Dauer $(( $(date +%s) - T0 )) s Ende $(date -u +%FT%TZ)" >> $B/b1_kopf.txt

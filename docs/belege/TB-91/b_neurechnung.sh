#!/bin/bash
# TB-91 Block B: einmalige Neurechnung nach Fable 23b. Start per nohup.
cd /Users/jaquelineloffler/trading-bot || exit 9
echo "START $(date -u +%FT%TZ)  HEAD $(git rev-parse HEAD)"
echo '$ trading-env/bin/python3 -W ignore research/vorregistrierung/benchmark.py --ziel research/vorregistrierung/ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json'
T0=$(date +%s)
trading-env/bin/python3 -W ignore research/vorregistrierung/benchmark.py --ziel research/vorregistrierung/ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json
RC=$?
echo "rc=$RC"
echo "ENDE $(date -u +%FT%TZ)  Laufzeit $(( $(date +%s)-T0 )) s"
echo "FERTIG"

#!/bin/bash
# TB-109 B3 - Abnahme Live-Code ohne Modus. Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-109/b3_abnahme.sh > docs/belege/TB-109/b3_abnahme.txt
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT
PY=trading-env/bin/python3
echo "# TB-109 B3, HEAD $(git rev-parse --short HEAD), Arbeitsbaum strategies/ shared/: [$(git status --porcelain -- strategies shared | tr '\n' ' ')], $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## (1) Trade-Listen der neun Bots nachher (a3_b3_alle.sh) und Vergleich gegen a3_b3_vorher.txt"
bash docs/belege/TB-109/a3_b3_alle.sh > docs/belege/TB-109/b3_trades_nachher.txt 2>&1
diff <(grep -v "^# TB-109\|^# Ende" docs/belege/TB-109/a3_b3_vorher.txt) <(grep -v "^# TB-109\|^# Ende" docs/belege/TB-109/b3_trades_nachher.txt) && echo "   vorher = nachher (9 Bots, 10 Stellen, Hashes gleich, alle erreichen simulate_portfolio)"
echo "## (2) research/tb27_kapitalsimulation/vergleich.py --pruefen"
$PY -W ignore research/tb27_kapitalsimulation/vergleich.py --pruefen > docs/belege/TB-109/b3_vergleich.txt 2>&1; echo "   rc=$?"; tail -3 docs/belege/TB-109/b3_vergleich.txt | sed 's/^/   /'
for t in shared/test_ergebniskurven.py shared/test_rueckfaelle_modus.py shared/test_nulltrades_modus.py; do
  O=docs/belege/TB-109/b3_$(basename $t .py).txt
  echo "## $t -> $O"; T0=$(date +%s); $PY -W ignore $t > $O 2>&1; RC=$?
  echo "   rc=$RC $(( $(date +%s) - T0 ))s  $(grep -E 'bestanden|GESCHEITERT' $O | tail -2 | tr '\n' ' ')"
done
echo "## Ende $(date '+%H:%M:%S')"

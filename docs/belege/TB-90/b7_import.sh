#!/bin/bash
# TB-90 B7 - je backtest_*.py: python3 -c "import <modul>" im Strategieordner,
# ohne vorbereiteten sys.path (nur der Strategieordner selbst, durch cwd/-c).
REPO=$(cd "$(dirname "$0")/../../.." && pwd)
PY="$REPO/trading-env/bin/python3"
for f in "$REPO"/strategies/*/backtest_*.py; do
    d=$(dirname "$f"); m=$(basename "$f" .py)
    out=$(cd "$d" && "$PY" -W ignore -c "import $m, sys; print($m.TRADING_FEE_PCT, $m.SLIPPAGE_PCT, 'handelskosten' in sys.modules)" 2>&1)
    rc=$?
    echo "$(basename "$d")/$m: rc=$rc  $(echo "$out" | tail -1)"
done

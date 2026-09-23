#!/bin/bash
# TB-90 A5 - test_vorregistrierung.py mit aktiviertem trading-env. $1 = Ausgabedatei
REPO=$(cd "$(dirname "$0")/../../.." && pwd)
cd "$REPO" || exit 9
{
  echo "# A5: $(date -u +%FT%TZ)  HEAD $(git rev-parse --short HEAD)  faltenplan.py $(shasum -a 256 research/vorregistrierung/faltenplan.py | cut -c1-16)"
  source trading-env/bin/activate
  echo "# python3 = $(command -v python3), $(python3 --version 2>&1)"
  cd research/vorregistrierung && python3 -W ignore test_vorregistrierung.py 2>&1
  echo "rc=$?"
} > "$1"

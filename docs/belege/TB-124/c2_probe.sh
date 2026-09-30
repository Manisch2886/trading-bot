#!/bin/bash
# TB-124 C2 - die Wertprobe test_posten3_durchreichung.py der zwei Breakout-Bots an einem ausgepackten Stand
# (git archive), ausserhalb des Repos. Angepasst aus docs/belege/TB-122/c2_probe.sh: packt docs/ mit aus (die Stufen
# kommen ueber registerdaten.raster() aus dem Registertext) und faehrt nur volatility_breakout und
# volatility_breakout_crypto. Fuer die Gegenprobe (Register 40.7) ist <commit> der Stand VOR TB-124 B; die
# Testdateien kommen aus <testquelle> (Ordner mit <bot>/test_posten3_durchreichung.py).
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-124/c2_probe.sh <ziel> <commit> <testquelle>
set -u
Z="$1"; C="$2"; T="$3"; PY=$PWD/trading-env/bin/python3
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR PYTHONPATH
if [ -e "$Z" ]; then echo "ABBRUCH: $Z existiert"; exit 1; fi
mkdir -p "$Z"
git archive "$C" shared config notifications research/vorregistrierung strategies docs/VORREGISTRIERUNG_neuselektion.md | tar -x -C "$Z"
echo "# TB-124 C2 Probe, Stand $(git rev-parse --short "$C"), Testquelle $T, $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "# sha256 backtest_breakout.py am ausgepackten Stand:"; (cd "$Z" && shasum -a 256 strategies/volatility_breakout*/backtest_breakout.py | sed 's/^/#   /')
for b in volatility_breakout volatility_breakout_crypto; do
  cp "$T/$b/test_posten3_durchreichung.py" "$Z/strategies/$b/"
  echo "## $b  (sha256 Testdatei $(shasum -a 256 "$T/$b/test_posten3_durchreichung.py" | cut -c1-16))"
  (cd "$Z" && $PY -W ignore "strategies/$b/test_posten3_durchreichung.py" > "$Z/$b.log" 2>&1); rc=$?
  tail -40 "$Z/$b.log"; echo "rc $rc"
done

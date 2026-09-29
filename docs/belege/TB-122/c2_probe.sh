#!/bin/bash
# TB-122 C2 - die Wertprobe test_posten3_durchreichung.py der drei Bots an einem ausgepackten Stand (git archive),
# ausserhalb des Repos. Fuer die Gegenprobe (Register 40.7) ist <commit> der Stand VOR TB-122 B; die Testdateien kommen
# aus <testquelle> (Ordner mit <bot>/test_posten3_durchreichung.py). Optional <umbauquelle>: Ordner mit <bot>/<datei>.py,
# die ueber den ausgepackten Stand gelegt werden (nur zum Vorab-Probelauf des Umbaus vor dem Einbau).
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-122/c2_probe.sh <ziel> <commit> <testquelle> [<umbauquelle>]
set -u
Z="$1"; C="$2"; T="$3"; U="${4:-}"; PY=$PWD/trading-env/bin/python3
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR PYTHONPATH
if [ -e "$Z" ]; then echo "ABBRUCH: $Z existiert"; exit 1; fi
mkdir -p "$Z"
git archive "$C" shared config notifications research/vorregistrierung strategies | tar -x -C "$Z"
echo "# TB-122 C2 Probe, Stand $(git rev-parse --short "$C"), Testquelle $T, Umbauquelle ${U:-keine}, $(date '+%Y-%m-%d %H:%M:%S %z')"
for b in rsi2_mean_reversion volatility_breakout volatility_breakout_crypto; do
  if [ -n "$U" ]; then for f in "$U/$b"/*.py; do case "$f" in */test_*) ;; *) cp "$f" "$Z/strategies/$b/";; esac; done; fi
  cp "$T/$b/test_posten3_durchreichung.py" "$Z/strategies/$b/"
  echo "## $b  (sha256 Testdatei $(shasum -a 256 "$T/$b/test_posten3_durchreichung.py" | cut -c1-16))"
  (cd "$Z" && $PY -W ignore "strategies/$b/test_posten3_durchreichung.py" > "$Z/$b.log" 2>&1); rc=$?
  tail -25 "$Z/$b.log"; echo "rc $rc"
done

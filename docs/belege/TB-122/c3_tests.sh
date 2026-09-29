#!/bin/bash
# TB-122 C3 - Testmenge wie TB-117 E (docs/belege/TB-117/e_tests.sh, Zeitgrenze je Datei 900 s ueber perl alarm),
# test_vorregistrierung mit 2400 s (in TB-117 E bei 900 s abgebrochen, in F 196/196), dazu die research-Tests,
# die einen der drei Bots nennen. trading-env (3.9.6), je Datei rc, Dauer, Schlusszeile. Ohne Modus.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-122/c3_tests.sh <logordner>
set -u
LOG="$1"; mkdir -p "$LOG"; PY=trading-env/bin/python3
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
echo "# TB-122 C3 Tests, HEAD $(git rev-parse --short HEAD), Arbeitsbaum ausserhalb docs/ [$(git status --porcelain -- . ':!docs' | tr '\n' ' ')], $(date '+%Y-%m-%d %H:%M:%S %z')"
for t in research/faltenplan_neun/test_faltenplan_neun.py research/faltenplan_neun/test_erste_falte_trockenlauf.py \
         research/faltenplan_neun/test_horizontbeginn.py research/faltenplan_neun/test_min_history.py \
         research/faltenplan_neun/test_volle_jahre.py research/universum_trockenlauf/test_universum_trockenlauf.py \
         research/universum_trockenlauf/test_zwischenablage.py \
         $(ls shared/test_*.py) research/vorregistrierung/test_ersatzwerte.py \
         research/pnl_2025_fixed_size/test_pnl.py research/tb27_kapitalsimulation/test_vergleich.py \
         research/volatility_scaled_sizing/test_vol_sizing_core.py research/drawdown_reihenfolge/test_drawdown.py \
         research/sync_check/test_sync_check.py research/vbc_deepdive/test_vbc_core.py \
         research/backtest_defaults/test_backtest_defaults.py research/datenluecke_wurzelkorrektur/test_wurzelkorrektur.py \
         research/vorregistrierung/test_vorregistrierung.py; do
  T0=$(date +%s); n=$(basename "$t" .py); GRENZE=900
  [ "$n" = test_vorregistrierung ] && GRENZE=2400
  perl -e "alarm shift; exec @ARGV" $GRENZE $PY -W ignore "$t" > "$LOG/$n.log" 2>&1; rc=$?
  echo "$n rc=$rc $(( $(date +%s)-T0 ))s: $(grep -iE 'bestanden|pruefungen|fehlgeschlagen|passed|failed|OK' "$LOG/$n.log" | tail -1 | cut -c1-120)"
done
echo "## Ende $(date '+%H:%M:%S')"

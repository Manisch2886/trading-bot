#!/bin/bash
# TB-111 - Hashes vorher/nachher (Vorlage TB-106 hashes.sh), im Worktree ~/trading-bot-tb111. Aufruf aus der Worktree-Wurzel:
#   bash docs/belege/TB-111/hashes.sh <Bezeichnung>
# (1) freigegebene Dateien, (2) gesperrte / nicht freigegebene Dateien einzeln,
# (3) Einzelhashes unter ergebnisse/ und Ergebnisdateien der Kette, (4) Listing ergebnisse/,
# (5) je versionierte Datei ausserhalb docs/ ein Hash in docs/belege/TB-111/5_alle_<Bezeichnung>.txt,
# (6) Snapshot-Summenhash und snapshot.py --pruefen, (7) Datenstand data/, (8) Quersummen der *.db,
# (9) herkunft.register(), (10) herkunft_protokoll.jsonl, (11) git status ausserhalb docs/.
SNAP=snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
V=research/vorregistrierung
PY=/Users/jaquelineloffler/trading-bot/trading-env/bin/python3
FREI="$V/herkunft.py $V/auswertung.py $V/test_vorregistrierung.py $V/test_ersatzwerte.py"
echo "# TB-111 sha256 $1, Wurzel $PWD, HEAD $(git --no-optional-locks rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## (1) freigegeben"
for p in $FREI; do shasum -a 256 "$p"; done
echo "## (2) nicht freigegeben / gesperrt"
for p in $V/registerdaten.py $V/faltenplan.py $V/benchmark.py $V/kennzahlen.py $V/messgroessen.py $V/pruefe_grenzsaetze.py \
         $V/registerbericht.py $V/sperrliste_abbild.py $V/beispieldaten.py shared/sperrlistensonde.py shared/paths.py \
         shared/strategy_paths.py shared/regimewache.py shared/zuteilung.py shared/messkette.py shared/snapshot.py \
         research/faltenplan_neun/*.py research/universum_trockenlauf/*.py research/etf_trendfolge/datenstand.py \
         strategies/*/equity_simulation.py strategies/*/multi_symbol_optimise.py \
         strategies/*/multi_symbol_walk_forward.py strategies/*/forward_test.py strategies/*/live_params.py \
         docs/VORREGISTRIERUNG_neuselektion.md config/top25_symbols.txt config/sp500_top150.txt; do
    shasum -a 256 "$p"
done
echo "## (3) Einzelhashes ergebnisse/ und Kette"
for p in $V/ergebnisse/*; do shasum -a 256 "$p"; done
for p in research/tb24_haltedauern/ergebnisse/haltedauern_je_bot.csv $SNAP/MANIFEST.json; do shasum -a 256 "$p"; done
echo "## (4) ergebnisse/ (Name Groesse)"
ls -l $V/ergebnisse | awk 'NR>1 {print $9, $5}'
echo "## (5) je versionierte Datei ausserhalb docs/ -> docs/belege/TB-111/5_alle_$1.txt"
git --no-optional-locks ls-files -- . ':!docs' | while read -r f; do shasum -a 256 "$f"; done > "docs/belege/TB-111/5_alle_$1.txt"
echo "   Anzahl: $(wc -l < docs/belege/TB-111/5_alle_$1.txt | tr -d ' ')"
echo "## (6) Snapshot (alle Dateien, Summenhash) und --pruefen"
find $SNAP -type f | sort | while read -r f; do shasum -a 256 "$f"; done | shasum -a 256
$PY -W ignore shared/snapshot.py --pruefen $SNAP 2>&1 | grep -E 'hash|UNVER|VERAEND|Soll|Ist'
echo "## (7) Datenstand data/ (herkunft.datenstand)"
$PY -W ignore -c "import sys; sys.path.insert(0,'$V'); import herkunft; print(herkunft.datenstand('data'))" 2>&1 | tail -2
echo "## (8) Quersummen *.db (Worktree-Wurzel und strategies/)"
ls *.db strategies/*/*.db 2>/dev/null | sort | while read -r f; do shasum -a 256 "$f"; done
echo "   Anzahl: $(ls *.db strategies/*/*.db 2>/dev/null | wc -l | tr -d ' ')"
echo "## (9) herkunft.register()"
$PY -W ignore -c "
import sys, json; sys.path.insert(0,'$V'); import herkunft
r = herkunft.register(); print('register', r['register']); print('fehlend', r['fehlend'])
for t in r['teile']: print('  ', t['sha256'], t['datei'])" 2>&1
echo "## (10) herkunft_protokoll.jsonl"
ls -l $V/ergebnisse/herkunft_protokoll.jsonl 2>&1; shasum -a 256 $V/ergebnisse/herkunft_protokoll.jsonl 2>&1
echo "## (11) git status ausserhalb docs/ (muss leer sein)"
git --no-optional-locks status --porcelain -- . ':!docs'
echo "## Ende"

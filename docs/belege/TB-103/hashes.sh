#!/bin/bash
# TB-103 - Hashes vorher/nachher (Vorlage TB-102 hashes.sh). Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-103/hashes.sh <Bezeichnung>
# (1) freigegebene Dateien, (2) gesperrte / nicht freigegebene Dateien einzeln,
# (3) Ergebnisdateien der Kette, (4) Listing ergebnisse/, (5) Summenhash ueber
# alle versionierten Dateien ausserhalb docs/ OHNE die freigegebenen,
# (6) Snapshot-Summenhash und snapshot.py --pruefen, (7) Datenstand data/,
# (8) Quersummen der *.db, (9) git status ausserhalb docs/.
SNAP=snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
FREI="shared/paths.py shared/test_paths.py shared/test_startpruefungen.py research/vorregistrierung/messgroessen.py research/vorregistrierung/test_vorregistrierung.py"
echo "# TB-103 sha256 $1, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## (1) freigegeben"
for p in $FREI; do shasum -a 256 "$p"; done
echo "## (2) nicht freigegeben / gesperrt"
for p in shared/symbols_config.py strategies/*/stocks_symbols_config.py shared/ladeprotokoll.py \
         shared/strategy_paths.py research/vorregistrierung/registerdaten.py \
         research/vorregistrierung/faltenplan.py shared/zuteilung.py research/vorregistrierung/herkunft.py \
         docs/VORREGISTRIERUNG_neuselektion.md config/top25_symbols.txt config/sp500_top150.txt; do
    shasum -a 256 "$p"
done
echo "## (3) Ergebnisdateien der Kette"
for p in research/vorregistrierung/ergebnisse/messgroessen.json \
         research/vorregistrierung/ergebnisse/messgroessen_2026-09-23_nachweis.json \
         research/tb24_haltedauern/ergebnisse/haltedauern_je_bot.csv \
         research/vorregistrierung/ergebnisse/faltenplan.json \
         research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-23.json \
         $SNAP/MANIFEST.json; do
    shasum -a 256 "$p"
done
echo "## (4) ergebnisse/ (Name Groesse)"
ls -l research/vorregistrierung/ergebnisse | awk 'NR>1 {print $9, $5}'
echo "## (5) Summenhash ueber versionierte Dateien ausserhalb docs/ ohne die freigegebenen"
AUS=""; for p in $FREI; do AUS="$AUS :!$p"; done
git ls-files -- . ':!docs' $AUS | while read -r f; do shasum -a 256 "$f"; done | shasum -a 256
echo "   Anzahl: $(git ls-files -- . ':!docs' $AUS | wc -l | tr -d ' ')"
echo "## (6) Snapshot (alle Dateien, Summenhash) und --pruefen"
find $SNAP -type f | sort | while read -r f; do shasum -a 256 "$f"; done | shasum -a 256
trading-env/bin/python3 -W ignore shared/snapshot.py --pruefen $SNAP 2>&1 | grep -E 'hash|UNVER|VERAEND|Soll|Ist'
echo "## (7) Datenstand data/ (herkunft.datenstand)"
trading-env/bin/python3 -W ignore -c "import sys; sys.path.insert(0,'research/vorregistrierung'); import herkunft; print(herkunft.datenstand('data'))" 2>&1 | tail -2
echo "## (8) Quersummen *.db (Repo-Wurzel und strategies/)"
for f in $(ls *.db strategies/*/*.db 2>/dev/null | sort); do shasum -a 256 "$f"; done
echo "## (9) git status ausserhalb docs/ (muss leer sein)"
git status --porcelain -- . ':!docs'
echo "## Ende"

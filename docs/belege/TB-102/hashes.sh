#!/bin/bash
# TB-102 - Hashes vorher/nachher. Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-102/hashes.sh <Bezeichnung>
# (1) die Dateien der Kette einzeln, (2) Listing von ergebnisse/ (Name, Groesse),
# (3) ein Summenhash ueber ALLE versionierten Dateien ausserhalb von docs/,
# (4) git status ausserhalb von docs/ (muss leer sein).
echo "# TB-102 sha256 $1, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
for p in research/vorregistrierung/ergebnisse/messgroessen.json \
         research/vorregistrierung/ergebnisse/messgroessen_2026-09-23_nachweis.json \
         research/tb24_haltedauern/ergebnisse/haltedauern_je_bot.csv \
         research/vorregistrierung/messgroessen.py \
         research/vorregistrierung/registerdaten.py \
         research/vorregistrierung/faltenplan.py \
         research/vorregistrierung/ergebnisse/faltenplan.json \
         research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-23.json \
         snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/MANIFEST.json; do
    shasum -a 256 "$p"
done
echo "## ergebnisse/ (Name Groesse)"
ls -l research/vorregistrierung/ergebnisse | awk 'NR>1 {print $9, $5}'
echo "## tb24_haltedauern/ergebnisse/ (Name Groesse)"
ls -l research/tb24_haltedauern/ergebnisse | awk 'NR>1 {print $9, $5}'
echo "## Summenhash ueber alle versionierten Dateien ausserhalb von docs/"
git ls-files -- . ':!docs' | while read -r f; do shasum -a 256 "$f"; done | shasum -a 256
echo "   Anzahl: $(git ls-files -- . ':!docs' | wc -l | tr -d ' ')"
echo "## Snapshot (alle Dateien, Summenhash)"
find snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2 -type f | sort | while read -r f; do shasum -a 256 "$f"; done | shasum -a 256
echo "## git status ausserhalb docs/ (muss leer sein)"
git status --porcelain -- . ':!docs'
echo "## Ende"

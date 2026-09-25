#!/bin/bash
# TB-105 - Hashes vorher/nachher (Vorlage TB-104 hashes.sh). Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-105/hashes.sh <Bezeichnung>
# (1) freigegebene Dateien, (2) gesperrte / nicht freigegebene Dateien einzeln,
# (3) Ergebnisdateien der Kette, (4) Listing ergebnisse/, (5) je versionierte Datei
# ausserhalb docs/ ein Hash in docs/belege/TB-105/5_alle_<Bezeichnung>.txt (Vergleich per diff),
# (6) Snapshot-Summenhash und snapshot.py --pruefen, (7) Datenstand data/,
# (8) Quersummen der *.db, (9) git status ausserhalb docs/.
SNAP=snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
FREI="strategies/t3_supertrend/equity_simulation.py strategies/t3_supertrend/multi_symbol_optimise.py strategies/volatility_breakout_crypto/equity_simulation.py strategies/elliott_wave/equity_simulation.py strategies/rsi2_crypto/equity_simulation.py strategies/turtle_soup_crypto/equity_simulation.py strategies/elliott_wave_stocks/equity_simulation.py strategies/rsi2_mean_reversion/equity_simulation.py strategies/turtle_soup_stocks/equity_simulation.py strategies/volatility_breakout/equity_simulation.py strategies/elliott_wave/multi_symbol_optimise.py strategies/elliott_wave_stocks/multi_symbol_optimise.py strategies/rsi2_mean_reversion/multi_symbol_optimise.py strategies/volatility_breakout/multi_symbol_optimise.py shared/symbols_config.py notifications/manual_close.py shared/strategy_paths.py research/exposure_messung/bot_lauf.py"
echo "# TB-105 sha256 $1, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## (1) freigegeben"
for p in $FREI; do shasum -a 256 "$p"; done
echo "## (2) nicht freigegeben / gesperrt"
for p in shared/regimewache.py shared/paths.py shared/ladeprotokoll.py \
         research/vorregistrierung/*.py research/universum_trockenlauf/*.py \
         strategies/*/forward_test.py strategies/*/live_params.py \
         strategies/*/stocks_symbols_config.py shared/zuteilung.py shared/sperrlistensonde.py \
         docs/VORREGISTRIERUNG_neuselektion.md config/top25_symbols.txt config/sp500_top150.txt; do
    shasum -a 256 "$p"
done
echo "## (3) Ergebnisdateien der Kette"
for p in research/vorregistrierung/ergebnisse/messgroessen.json \
         research/tb24_haltedauern/ergebnisse/haltedauern_je_bot.csv \
         research/vorregistrierung/ergebnisse/faltenplan.json \
         research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-25.json \
         research/vorregistrierung/ergebnisse/benchmark_drawdowns.json \
         $SNAP/MANIFEST.json; do
    shasum -a 256 "$p"
done
echo "## (4) ergebnisse/ (Name Groesse)"
ls -l research/vorregistrierung/ergebnisse | awk 'NR>1 {print $9, $5}'
echo "## (5) je versionierte Datei ausserhalb docs/ -> docs/belege/TB-105/5_alle_$1.txt"
git ls-files -- . ':!docs' | while read -r f; do shasum -a 256 "$f"; done > "docs/belege/TB-105/5_alle_$1.txt"
echo "   Anzahl: $(wc -l < docs/belege/TB-105/5_alle_$1.txt | tr -d ' ')"
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

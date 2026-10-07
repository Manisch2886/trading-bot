#!/bin/bash
# TB-140 V1 - Suchlaeufe zu R78 (a), ueber suche.py (nur verfolgte Dateien, nur lesen).
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-140/v1_suche.sh
set -u
PY="${PY:-trading-env/bin/python3}"; S=docs/belege/TB-140/suche.py
F5="--pfad research/vorregistrierung --pfad research/mtm_drawdown --pfad research/exposure_messung --pfad shared --pfad strategies"
RC=0
lauf() { "$PY" -B "$S" "$@"; local r=$?; echo "rc $r"; [ $r -ne 0 ] && RC=2; }
echo "## V1 Nr. 0 - gibt es einen Zellen-Erzeuger? Namen der Ausgaben aus R39 (Register Z. 10857)"
lauf --name V1-0a --ohne docs --muster zellen.csv --muster zellenbericht --muster tagesreihen/ --muster benchmark_tagesreihen --muster symbole_je_falte --muster herkunft.json
lauf --name V1-0b --ohne docs --regex --ohne-gross-klein --muster 'zellen.?erzeuger' --muster 'lese.?audit'
echo "## V1 Nr. 1 - Lesestellen in benchmark.py"
lauf --name V1-1a --pfad research/vorregistrierung/benchmark.py --muster read_csv --muster 'open(' --muster _1d --muster _1h --muster _4h --muster DATA_DIR --muster CONFIG_DIR --muster '"close"'
echo "## V1 Nr. 1 und Nr. 2 - Aufrufer von tagesschluss und lade_schlusskurse"
lauf --name V1-1b --ohne docs --muster 'tagesschluss(' --muster 'tagesschluss =' --muster 'lade_schlusskurse('
echo "## V1 Nr. 2 - Kern und Ladestelle"
lauf --name V1-2a --pfad research/mtm_drawdown/mtm_kern.py --pfad research/mtm_drawdown/grundlage.py --pfad research/mtm_drawdown/messung.py --muster read_csv --muster 'open(' --muster DATA_DIR --muster REPO_ROOT --muster '"close"' --muster 'zeitrahmen' --muster 'tagesraster(' --muster 'kurse_auf_raster('
lauf --name V1-2b --pfad research/exposure_messung/auswertung.py --muster DATA_DIR --muster read_csv --muster '"close"' --muster 'def mtm_reihen' --muster 'bfill'
echo "## V1 Nr. 4 - der Weg zum Snapshot: Resolver und wer ihn kennt"
lauf --name V1-4a --pfad shared/paths.py --muster '_LIVE_DATA_DIR =' --muster 'DATA_DIR = ' --muster '_MODUS = ' --muster 'UMGEBUNG_WURZEL =' --muster 'CONFIG_UNTERORDNER ='
lauf --name V1-4b $F5 --muster 'import paths' --muster 'paths.DATA_DIR' --muster 'os.path.join(REPO_ROOT, "data")' --muster 'os.path.join(_REPO_ROOT, "data")' --muster 'TB_SELEKTIONSWURZEL'
lauf --name V1-4c --pfad docs/VORREGISTRIERUNG_neuselektion.md --endung .md --muster 'Ein Modus-Lauf ist ein Lauf unter dem Selektionsmodus des Resolvers'
echo "## Ende"
exit $RC

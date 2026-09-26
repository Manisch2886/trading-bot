#!/bin/bash
# TB-114 B2 - nur messen: Wer liest register()["fehlend"]? Fuehrt eine fehlende eingefrorene Datei zu rc != 0,
# im Modus und ohne? (1) Suchmuster ueber alle versionierten .py; (2) Probe in einem frischen Klon mit dem
# Arbeitsstand von herkunft.py (B1/B3/B4, im Klon committet), eine der neun TB-24-Listen umbenannt.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-114/b2_fehlend.sh <scratch>
set -u
SP="$1"; R=$(pwd); PY=$R/trading-env/bin/python3
SNAP=63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
echo "# TB-114 B2, HEAD $(git rev-parse --short HEAD), herkunft.py $(shasum -a 256 research/vorregistrierung/herkunft.py | cut -c1-16)..., $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## (1) Suchmuster: git grep -n -E \"\\[.fehlend.\\]|register_fehlend|\\.get\\(.fehlend\" -- '*.py'"
git grep -n -E "\[.fehlend.\]|register_fehlend|\.get\(.fehlend" -- '*.py'
echo "## (1b) Aufrufer von register()/block()/anhaengen() ausserhalb docs/belege: git grep -n -E \"herkunft\\.(register|block|anhaengen)\\(\" -- '*.py' ':!docs'"
git grep -n -E "herkunft\.(register|block|anhaengen)\(" -- '*.py' ':!docs'
echo "## (1c) Laufbereich (TB-112 a2_laufbereich.txt): Zeilen mit herkunft.py: $(grep -c 'herkunft.py' docs/belege/TB-112/a2_laufbereich.txt)"
K="$SP/b2_klon"
if [ -e "$K" ]; then echo "ABBRUCH: $K existiert"; exit 1; fi
git clone -q "$R" "$K"
cp research/vorregistrierung/herkunft.py "$K/research/vorregistrierung/herkunft.py"
cd "$K" || exit 1
git -c user.name=tb114 -c user.email=tb114@test commit -q -am "TB-114 B2 Probe: herkunft.py Arbeitsstand"
L=research/tb24_haltedauern/daten/rsi2_crypto_alle_trades.csv
mv "$L" "$SP/b2_weggelegt.csv"
echo "## (2) Klon <scratch>/b2_klon, HEAD $(git rev-parse --short HEAD) (lokaler Probecommit), weggelegt: $L"
echo "   git status: [$(git status --porcelain | tr '\n' ' ')]"
echo "### (2a) ohne Modus, register()"
$PY -W ignore -c "
import sys; sys.path.insert(0,'research/vorregistrierung'); import herkunft
r = herkunft.register(); print('register', r['register'][:16], '... fehlend', r['fehlend'], 'Teile', len(r['teile']))"; echo "rc $?"
echo "### (2b) ohne Modus, Pruefansicht herkunft.py"
$PY -W ignore research/vorregistrierung/herkunft.py > "$SP/b2_2b.txt" 2>&1; echo "rc $?"; grep -E "Register|fehlend|Protokoll" "$SP/b2_2b.txt"
echo "### (2c) Modus, Pruefansicht herkunft.py"
env TB_SELEKTIONSWURZEL="$K/snapshots/$SNAP" TB_SELEKTIONSHASH="$SNAP" TB_SELEKTIONSCOMMIT="$(git rev-parse HEAD)" \
    $PY -W ignore research/vorregistrierung/herkunft.py > "$SP/b2_2c.txt" 2>&1; echo "rc $?"; grep -E "Register|fehlend|Protokoll|ABBRUCH" "$SP/b2_2c.txt"
echo "### (2d) Modus, block() mit paths.DATA_DIR: register_fehlend im Herkunftsblock"
env TB_SELEKTIONSWURZEL="$K/snapshots/$SNAP" TB_SELEKTIONSHASH="$SNAP" TB_SELEKTIONSCOMMIT="$(git rev-parse HEAD)" \
    $PY -W ignore research/vorregistrierung/herkunft.py --json > "$SP/b2_2d.json" 2>"$SP/b2_2d.err"; echo "rc $?"
$PY -c "import json; b=json.load(open('$SP/b2_2d.json'))['herkunft']; print('register_fehlend', b['register_fehlend'], 'register', b['register'][:16])"
echo "### (2e) Gegenprobe: Liste zurueck, Modus, Pruefansicht"
mv "$SP/b2_weggelegt.csv" "$L"
echo "   git status: [$(git status --porcelain | tr '\n' ' ')]"
env TB_SELEKTIONSWURZEL="$K/snapshots/$SNAP" TB_SELEKTIONSHASH="$SNAP" TB_SELEKTIONSCOMMIT="$(git rev-parse HEAD)" \
    $PY -W ignore research/vorregistrierung/herkunft.py > "$SP/b2_2e.txt" 2>&1; echo "rc $?"; grep -E "Register|fehlend" "$SP/b2_2e.txt"
echo "## Ende $(date '+%H:%M:%S')"

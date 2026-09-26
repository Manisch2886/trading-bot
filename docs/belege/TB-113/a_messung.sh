#!/bin/bash
# TB-113 A - Messung nach dem Merge (Bauart TB-112 0c_eingang.sh): Hashes herkunft.py/auswertung.py, register(), Sonde gegen
# das gueltige Abbild e655c1c8, Wechselwirkung TB-111 x TB-112 (Laufbereich / ARBEITSBAUM_PFADE).
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-113/a_messung.sh <bezeichnung> <scratch>
set -u
B="$1"; SP="$2"; PY=trading-env/bin/python3; V=research/vorregistrierung
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
AB=$V/ergebnisse/sperrliste_abbild_2026-09-26.json
echo "# TB-113 A $B, HEAD $(git rev-parse --short HEAD), Baum $(git rev-parse --short HEAD^{tree}), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## Hashes (Soll herkunft.py 5bbfc9e0..., auswertung.py a864b216..., Abbild e655c1c8...)"
shasum -a 256 $V/herkunft.py $V/auswertung.py $AB
echo "## herkunft.register() (weder e7d82547... tb-111 noch c92900a8... main erwartet)"
$PY -W ignore -c "
import sys; sys.path.insert(0,'$V'); import herkunft
r = herkunft.register(); print('register', r['register']); print('fehlend', r['fehlend'])" 2>&1
echo "## Sonde gegen $AB"
$PY -W ignore shared/sperrlistensonde.py --abbild $AB > "$SP/sonde_$B.txt" 2>&1; echo "rc $?"
grep -E "^Pfad-Bestandteile|^\(ii\)|^RUECKGABEWERT|Registertext: |BEFUND" "$SP/sonde_$B.txt"
echo "## Wechselwirkung TB-111 x TB-112: Eintraege in paths.ARBEITSBAUM_PFADE und Laufbereichsmessung (TB-112 A2)"
$PY -W ignore -c "
import sys; sys.path.insert(0,'shared'); import paths
print('ARBEITSBAUM_PFADE', len(paths.ARBEITSBAUM_PFADE))
for p in paths.ARBEITSBAUM_PFADE: print('  ', p)
print('REGISTRIERTE_PROTOKOLLE', paths.REGISTRIERTE_PROTOKOLLE)
print('auswertung.py in ARBEITSBAUM_PFADE:', any(str(p).endswith('research/vorregistrierung/auswertung.py') for p in paths.ARBEITSBAUM_PFADE))
print('herkunft.py in ARBEITSBAUM_PFADE:', any(str(p).endswith('herkunft.py') for p in paths.ARBEITSBAUM_PFADE))" 2>&1
echo "   Laufbereichsmessung docs/belege/TB-112/a2_laufbereich.txt: auswertung.py $(grep -c 'vorregistrierung/auswertung.py' docs/belege/TB-112/a2_laufbereich.txt) Zeile(n), herkunft.py $(grep -c 'herkunft.py' docs/belege/TB-112/a2_laufbereich.txt) Zeile(n)"
echo "## herkunft_protokoll.jsonl"; ls -l $V/ergebnisse/herkunft_protokoll.jsonl 2>&1
echo "## git status ausserhalb docs/"; git status --porcelain -- . ':!docs'
echo "## Ende"

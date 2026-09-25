#!/bin/bash
# TB-106 A10 - Rueckgabewert von auswertung.Abbruch (erbt von SystemExit, mit Text geworfen). Nur messen.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-106/a10_abbruch_rc.sh <leerer Ordner>
PY=/Users/jaquelineloffler/trading-bot/trading-env/bin/python3
echo "# TB-106 A10, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "== (1) direkt: raise auswertung.Abbruch('Probe')"
$PY -W ignore -c "import sys; sys.path.insert(0,'research/vorregistrierung'); import auswertung as aw; raise aw.Abbruch('Probe')"
echo "   rc=$?"
echo "== (2) Ablauf: auswertung.py --rohergebnisse <leer> --bot turtle_soup_stocks (lies_zellen: zellen.csv fehlt)"
$PY -W ignore research/vorregistrierung/auswertung.py --rohergebnisse "$1" --bot turtle_soup_stocks 2>&1 | tail -2
echo "   rc=${PIPESTATUS[0]}"
echo "== (3) Klasse: $($PY -c "import sys; sys.path.insert(0,'research/vorregistrierung'); import auswertung as aw; print(aw.Abbruch.__mro__)" 2>/dev/null)"
echo "== (4) Stellen 'raise Abbruch' in auswertung.py: $(grep -c 'raise Abbruch' research/vorregistrierung/auswertung.py)"

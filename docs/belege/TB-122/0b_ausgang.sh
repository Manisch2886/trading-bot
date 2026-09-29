#!/bin/bash
# TB-122 0b - Ausgangswerte (Bauart TB-117 0b_ausgang.sh / TB-119 a2_sonde.sh): HEAD, sha256 der sieben Dateien,
# herkunft.register(), Sonde gegen das gueltige Abbild tb117 (nur lesend, git status vorher/nachher gezaehlt),
# Stellung der sieben Dateien in Abbild, Sperrliste Punkt 11 und herkunft.EINGEFROREN.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-122/0b_ausgang.sh <scratch> <marke>
set -u
SP="$1"; M="$2"; PY=trading-env/bin/python3; V=research/vorregistrierung
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
AB=$V/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json
S=strategies
SIEBEN="$S/rsi2_mean_reversion/backtest_rsi2.py $S/rsi2_mean_reversion/multi_symbol_optimise.py $S/rsi2_mean_reversion/equity_simulation.py $S/volatility_breakout/multi_symbol_optimise.py $S/volatility_breakout/equity_simulation.py $S/volatility_breakout_crypto/multi_symbol_optimise.py $S/volatility_breakout_crypto/equity_simulation.py"
echo "# TB-122 0b ($M), HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## sha256 der sieben Dateien"
shasum -a 256 $SIEBEN
echo "## Hashes Werkzeuge"
shasum -a 256 $V/herkunft.py $AB shared/sperrlistensonde.py $V/auswertung.py docs/VORREGISTRIERUNG_neuselektion.md
echo "## herkunft.register() (Soll laut ERGEBNIS_TB-117 Zeile F: 01f5997a...)"
$PY -W ignore -c "
import sys; sys.path.insert(0,'$V'); import herkunft
r = herkunft.register(); print('register', r['register']); print('fehlend', r['fehlend']); print('teile', len(r['teile']))" 2>&1
echo "## Sonde gegen $AB"
echo "# git status --porcelain vorher: $(git status --porcelain | wc -l | tr -d ' ') Zeilen"
$PY -W ignore shared/sperrlistensonde.py --abbild $AB > "$SP/sonde_0b_$M.txt" 2>&1; echo "rc $?"
echo "# git status --porcelain nachher: $(git status --porcelain | wc -l | tr -d ' ') Zeilen"
echo "# Ausgabe sha256: $(shasum -a 256 "$SP/sonde_0b_$M.txt" | cut -c1-64), $(wc -l < "$SP/sonde_0b_$M.txt" | tr -d ' ') Zeilen"
grep -E "^Pfad-Bestandteile|^\(ii\)|^RUECKGABEWERT|Registertext: |BEFUND" "$SP/sonde_0b_$M.txt"
echo "## Die sieben Dateien im Abbild (Pfad -> Gruppe/Punkt, gemessen aus JSON)"
$PY -W ignore - "$AB" $SIEBEN <<'PYEOF'
import json, sys
ab = json.load(open(sys.argv[1])); sieben = sys.argv[2:]
def wandern(o, weg):
    if isinstance(o, dict):
        for k, v in o.items(): yield from wandern(v, weg + [str(k)])
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from wandern(v, weg + [str(i)])
    else:
        yield weg, o
treffer = {p: [] for p in sieben}
for weg, wert in wandern(ab, []):
    for p in sieben:
        if isinstance(wert, str) and p in wert: treffer[p].append("/".join(weg) + " = " + wert[:90])
        if p in weg: treffer[p].append("/".join(weg) + " -> " + str(wert)[:90])
for p in sieben:
    print(p, "|", len(treffer[p]), "Treffer")
    for t in treffer[p][:6]: print("   ", t)
PYEOF
echo "## Die sieben Dateien in herkunft.EINGEFROREN"
$PY -W ignore -c "
import sys; sys.path.insert(0,'$V'); import herkunft
E = herkunft.EINGEFROREN; print('EINGEFROREN Typ', type(E).__name__, 'Laenge', len(E))
for p in '''$SIEBEN'''.split():
    print(p, '|', 'in EINGEFROREN' if any(p in str(e) for e in E) else 'nicht in EINGEFROREN')" 2>&1
echo "## Sperrliste Punkt 11 im Register (Abschnitt 10), Zeilen mit Punkt 11"
awk '/^## 10\. Die Sperrliste/{a=1} /^## 11\. /{a=0} a' docs/VORREGISTRIERUNG_neuselektion.md | grep -n "^| *11 \|^11\.\|^| \*\*11\|Punkt 11" | cut -c1-300
echo "## git status (ausserhalb docs/ muss leer sein)"; git status --porcelain -- . ':!docs'; echo "[Ende status]"
echo "## Ende"

#!/bin/bash
# TB-124 0d / C5 - Ausgangswerte (Bauart docs/belege/TB-122/0b_ausgang.sh): HEAD, sha256 der Dateien, die TB-124
# aendert oder anlegt, herkunft.register(), Sonde gegen das gueltige Abbild tb117 (nur lesend, git status vorher/nachher
# gezaehlt), Stellung jeder dieser Dateien in Abbild und herkunft.EINGEFROREN.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-124/0d_ausgang.sh <scratch> <marke>
set -u
SP="$1"; M="$2"; PY=trading-env/bin/python3; V=research/vorregistrierung
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
AB=$V/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json
S=strategies
DATEIEN="$S/volatility_breakout/backtest_breakout.py $S/volatility_breakout_crypto/backtest_breakout.py $S/volatility_breakout/test_posten3_durchreichung.py $S/volatility_breakout_crypto/test_posten3_durchreichung.py research/sync_check/sync_table.py research/sync_check/test_sync_check.py shared/test_verankerter_datenstand.py shared/snapshot.py"
echo "# TB-124 0d ($M), HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## sha256 der Dateien (geaendert/angelegt von TB-124; test_sync_check.py und snapshot.py nur zum Vergleich)"
for f in $DATEIEN; do if [ -e "$f" ]; then shasum -a 256 "$f"; else echo "(fehlt)  $f"; fi; done
echo "## Hashes Werkzeuge"
shasum -a 256 $V/herkunft.py $AB shared/sperrlistensonde.py $V/auswertung.py docs/VORREGISTRIERUNG_neuselektion.md
echo "## herkunft.register() (Soll laut Auftrag: 01f5997a...)"
$PY -W ignore -c "
import sys; sys.path.insert(0,'$V'); import herkunft
r = herkunft.register(); print('register', r['register']); print('fehlend', r['fehlend']); print('teile', len(r['teile']))" 2>&1
echo "## Sonde gegen $AB"
echo "# git status --porcelain vorher: $(git status --porcelain | wc -l | tr -d ' ') Zeilen"
$PY -W ignore shared/sperrlistensonde.py --abbild $AB > "$SP/sonde_0d_$M.txt" 2>&1; echo "rc $?"
echo "# git status --porcelain nachher: $(git status --porcelain | wc -l | tr -d ' ') Zeilen"
echo "# Ausgabe sha256: $(shasum -a 256 "$SP/sonde_0d_$M.txt" | cut -c1-64), $(wc -l < "$SP/sonde_0d_$M.txt" | tr -d ' ') Zeilen"
grep -E "^Pfad-Bestandteile|^\(ii\)|^RUECKGABEWERT|Registertext: |BEFUND" "$SP/sonde_0d_$M.txt"
echo "## Die Dateien im Abbild (Pfad -> Eintrag, gemessen aus JSON)"
$PY -W ignore - "$AB" $DATEIEN <<'PYEOF'
import json, sys
ab = json.load(open(sys.argv[1])); dateien = sys.argv[2:]
def wandern(o, weg):
    if isinstance(o, dict):
        for k, v in o.items(): yield from wandern(v, weg + [str(k)])
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from wandern(v, weg + [str(i)])
    else:
        yield weg, o
treffer = {p: [] for p in dateien}
for weg, wert in wandern(ab, []):
    for p in dateien:
        if isinstance(wert, str) and p in wert: treffer[p].append("/".join(weg) + " = " + wert[:90])
        if p in weg: treffer[p].append("/".join(weg) + " -> " + str(wert)[:90])
for p in dateien:
    print(p, "|", len(treffer[p]), "Treffer")
    for t in treffer[p][:6]: print("   ", t)
PYEOF
echo "## Die Dateien in herkunft.EINGEFROREN"
$PY -W ignore -c "
import sys; sys.path.insert(0,'$V'); import herkunft
E = herkunft.EINGEFROREN; print('EINGEFROREN Typ', type(E).__name__, 'Laenge', len(E))
for p in '''$DATEIEN'''.split():
    print(p, '|', 'in EINGEFROREN' if any(p in str(e) for e in E) else 'nicht in EINGEFROREN')" 2>&1
echo "## Gegenprobe Messweg: Dateinamen allein (ohne Ordner) in Abbild und EINGEFROREN"
$PY -W ignore - "$AB" <<'PYEOF'
import json, sys
sys.path.insert(0, "research/vorregistrierung"); import herkunft
roh = open(sys.argv[1], encoding="utf-8").read()
E = " ".join(str(e) for e in herkunft.EINGEFROREN)
for n in ("backtest_breakout", "test_posten3_durchreichung", "sync_table", "test_sync_check", "test_verankerter_datenstand", "snapshot.py"):
    print(n, "| Abbild-Rohtext:", roh.count(n), "| EINGEFROREN:", E.count(n))
PYEOF
echo "## git status (ausserhalb docs/ muss leer sein)"; git status --porcelain -- . ':!docs'; echo "[Ende status]"
echo "## Ende"

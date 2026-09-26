#!/bin/bash
# TB-117 C2 - die drei Snapshot-Eintraege (R15 (a)): versioniert? Pfade? Aufloesung in herkunft.py und in der Sonde?
# Dazu register() und Hashes am Stand vor/nach Block C. Rein lesend. Aufruf aus der Repo-Wurzel.
set -u
PY=trading-env/bin/python3; H=63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
echo "# TB-117 C2, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## Registrierter Snapshot (Register 18, Z. $(grep -n "^| Name (\`snapshot_hash\`)" docs/VORREGISTRIERUNG_neuselektion.md | cut -d: -f1))"
grep -F "| Name (\`snapshot_hash\`)" docs/VORREGISTRIERUNG_neuselektion.md
echo "## versioniert (git ls-files) und sha256"
git ls-files snapshots/$H/MANIFEST.json snapshots/$H/config/
shasum -a 256 snapshots/$H/MANIFEST.json snapshots/$H/config/top25_symbols.txt snapshots/$H/config/sp500_top150.txt config/top25_symbols.txt config/sp500_top150.txt
echo "## MANIFEST: Kursdateien im Datenstand vs. Dateien im Snapshot-Hash (Fables drittes 'Unsicher')"
$PY -c "
import json; m=json.load(open('snapshots/$H/MANIFEST.json'))
print('kursdateien', m['kursdateien'], 'dateien_gesamt', m['dateien_gesamt'], 'datenstand_hash', m['datenstand_hash'][:12])
print('config im MANIFEST (dateien):', sorted(k for k in m['dateien'] if k.startswith('config/')))"
echo "## Aufloesung: herkunft._eingefroren_pfad und sperrlistensonde._aufloesen (absolut, je Eintrag)"
$PY -W ignore -c "
import os, sys; sys.path.insert(0,'research/vorregistrierung'); sys.path.insert(0,'shared')
import herkunft, sperrlistensonde as s
for rel in herkunft.EINGEFROREN[-3:]:
    a = herkunft._eingefroren_pfad(rel); b = os.path.normpath(os.path.join(herkunft._WURZEL, s._aufloesen(rel)))
    print('gleich' if a == b else 'ABWEICHEND', os.path.exists(a), os.path.relpath(a, herkunft._WURZEL))
print('EINGEFROREN', len(herkunft.EINGEFROREN), 'abweichend', sum(herkunft._eingefroren_pfad(r) != os.path.normpath(os.path.join(herkunft._WURZEL, s._aufloesen(r))) for r in herkunft.EINGEFROREN))"
echo "## herkunft.py und register() - vor Block C (git show 42ef509) und jetzt"
git show 42ef509:research/vorregistrierung/herkunft.py | shasum -a 256 | sed 's/-$/herkunft.py @ 42ef509/'
shasum -a 256 research/vorregistrierung/herkunft.py
$PY -W ignore -c "
import sys; sys.path.insert(0,'research/vorregistrierung'); import herkunft
r = herkunft.register(); print('register()', r['register'], 'fehlend', r['fehlend'], 'teile', len(r['teile']))"

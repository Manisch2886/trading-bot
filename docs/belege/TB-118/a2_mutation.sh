#!/bin/bash
# TB-118 A2 Mutationsprobe: ein Byte im Body von Teil 3 aendern (Byte 100 000 der Datei, im Body), cmp muss rc 1 geben,
# registerkopie.py --pruefen ebenfalls rc 1; danach das Originalbyte zurueck und sha256 vorher = nachher.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-118/a2_mutation.sh <scratch>
set -u
SP="$1"; T=docs/projektfuehrung/REGISTER_KOPIE_teil3.md; PY=trading-env/bin/python3
echo "# TB-118 A2 Mutationsprobe, $(date '+%Y-%m-%d %H:%M:%S %z')"
VOR=$(shasum -a 256 $T | cut -d' ' -f1); echo "sha256 Teil 3 vorher  $VOR"
$PY - "$T" <<'PY'
import sys
p = sys.argv[1]; b = bytearray(open(p, 'rb').read()); alt = b[100000]
b[100000] = alt ^ 0x01; open(p, 'wb').write(bytes(b))
print("Byte 100000: %d -> %d" % (alt, b[100000]))
PY
for n in 1 2 3 4; do tail -n +3 docs/projektfuehrung/REGISTER_KOPIE_teil$n.md; done > "$SP/bodies_mut.md"
git show HEAD:docs/VORREGISTRIERUNG_neuselektion.md > "$SP/original.md"
echo '$ cmp <scratch>/bodies_mut.md <scratch>/original.md'; cmp "$SP/bodies_mut.md" "$SP/original.md" 2>&1 | sed "s#$SP#<scratch>#g"; echo "rc ${PIPESTATUS[0]}"
echo '$ registerkopie.py --pruefen'; $PY docs/werkzeuge/registerkopie.py --pruefen | grep -E 'Bodies|Teil 3'; echo "rc ${PIPESTATUS[0]}"
$PY - "$T" <<'PY'
import sys
p = sys.argv[1]; b = bytearray(open(p, 'rb').read()); b[100000] ^= 0x01; open(p, 'wb').write(bytes(b))
print("zurueckgesetzt")
PY
NACH=$(shasum -a 256 $T | cut -d' ' -f1); echo "sha256 Teil 3 nachher $NACH"; [ "$VOR" = "$NACH" ] && echo "vorher = nachher" || echo "ABWEICHUNG"
echo '$ registerkopie.py --pruefen (nach dem Zuruecksetzen)'; $PY docs/werkzeuge/registerkopie.py --pruefen | grep Bodies; echo "rc ${PIPESTATUS[0]}"

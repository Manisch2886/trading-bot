#!/bin/bash
# TB-140 Teil 2 - Gegenprobe zu fundstellen_pruefen.py an einer Kopie der Liste in einem frischen Ordner
# unter $TMPDIR: in Zeile V1-21 die Zeilennummer um eins verschoben (die Nachbarzeile lautet anders),
# in Zeile V3-36 ein Zeichen des Wortlauts geaendert. Soll: zwei UNGLEICH, rc 1.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-140/fundstellen_gegenprobe.sh
set -u
PY="${PY:-trading-env/bin/python3}"; L=docs/belege/TB-140/fundstellen.tsv
T="$(mktemp -d "${TMPDIR:-/tmp}/tb140_fundstellen.XXXXXX")" || { echo "NICHT MESSBAR: kein Ordner"; exit 2; }
echo "# TB-140 Fundstellen GEGENPROBE"; echo "Ordner $T"
"$PY" -B - "$L" "$T/kopie.tsv" <<'PYEOF'
import sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
a = [i for i, s in enumerate(z) if s.startswith("V1-21\t")]
b = [i for i, s in enumerate(z) if s.startswith("V3-36\t")]
assert len(a) == 1 and len(b) == 1
k, d, n, art, w = z[a[0]].split("\t", 4)
z[a[0]] = "\t".join([k, d, str(int(n) + 1), art, w])
k, d, n, art, w = z[b[0]].split("\t", 4)
z[b[0]] = "\t".join([k, d, n, art, w.replace("isna", "isnA", 1)])
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(z))
print("Eingriffe: V1-21 Zeile +1, V3-36 ein Zeichen (isna -> isnA)")
PYEOF
"$PY" -B docs/belege/TB-140/fundstellen_pruefen.py --liste "$T/kopie.tsv" > "$T/aus.txt" 2>&1; RC=$?; cat "$T/aus.txt"; echo "rc $RC"
N=$(grep -c '^UNGLEICH' "$T/aus.txt")
echo "## Soll: zwei UNGLEICH (V1-21, V3-36), rc 1 - Ist: $N UNGLEICH, rc $RC"
if [ "$RC" = 1 ] && [ "$N" = 2 ] && grep -q $'^UNGLEICH\tV1-21' "$T/aus.txt" && grep -q $'^UNGLEICH\tV3-36' "$T/aus.txt"; then echo "GEGENPROBE: beisst"; exit 0; fi
echo "GEGENPROBE: beisst NICHT"; exit 1

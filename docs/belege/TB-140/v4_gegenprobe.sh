#!/bin/bash
# TB-140 V4 - Gegenprobe: v4_umgebung.py an zwei Kopien des Locks in einem frischen Ordner unter $TMPDIR.
# Die erste Kopie bleibt unveraendert; die zweite traegt G1 (pandas==0.0.1), G2 (ein Paket, das es
# nicht gibt) und G3 (eine andere Plattform im Kopf). Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-140/v4_gegenprobe.sh
# Rueckgabe: 0 die Probe beisst (alle Sollzeilen da), 1 eine Sollzeile fehlt, 2 nicht messbar.
set -u
PY="${PY:-trading-env/bin/python3}"
V="${V:-docs/belege/TB-140/v4_umgebung.py}"
LOCK="${LOCK:-requirements.lock}"
echo "# TB-140 V4 GEGENPROBE"
if [ ! -s "$LOCK" ]; then echo "NICHT MESSBAR: $LOCK fehlt oder ist leer"; exit 2; fi
T="$(mktemp -d "${TMPDIR:-/tmp}/tb140_v4_gegenprobe.XXXXXX")" || { echo "NICHT MESSBAR: kein Ordner unter TMPDIR"; exit 2; }
echo "Ordner $T"
cp "$LOCK" "$T/k1.lock"
$PY -B - "$LOCK" "$T/k2.lock" <<'PYEOF' || { echo "NICHT MESSBAR: die zweite Kopie liess sich nicht bauen"; exit 2; }
import sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
g1 = [i for i, s in enumerate(z) if s.strip() == "pandas==2.3.3"]
g3 = [i for i, s in enumerate(z) if s.startswith("# plattform ")]
assert len(g1) == 1 and len(g3) == 1, (g1, g3)
z[g1[0]] = "pandas==0.0.1"                           # G1, die Probe aus Register Z. 3261
z[g3[0]] = "# plattform         andere-plattform"   # G3
while z and z[-1] == "":
    z.pop()
z.append("kein-solches-paket-tb140==1.0")            # G2
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(z) + "\n")
print("zweite Kopie: G1 in Z. %d, G3 in Z. %d, G2 als letzte Zeile" % (g1[0] + 1, g3[0] + 1))
PYEOF
echo "## erste Kopie (unveraendert)"
$PY -B "$V" --lock "$T/k1.lock" > "$T/a.txt" 2>&1; RC1=$?; cat "$T/a.txt"; echo "rc $RC1"
echo "## zweite Kopie (G1, G2, G3)"
$PY -B "$V" --lock "$T/k2.lock" > "$T/b.txt" 2>&1; RC2=$?; cat "$T/b.txt"; echo "rc $RC2"
echo "## Unterschied der Zeilen KOPF und PAKET (< erste Kopie, > zweite Kopie)"
diff <(grep -E '^(KOPF|PAKET)' "$T/a.txt") <(grep -E '^(KOPF|PAKET)' "$T/b.txt")
zahl() { awk -F'\t' "$1" "$2" | wc -l | tr -d ' '; }
S1=$(zahl '$1=="KOPF" && $2=="plattform" && $3 ~ /andere-plattform/ && $5=="ABWEICHUNG"' "$T/b.txt")
S2=$(zahl '$1=="PAKET" && $2=="W1" && $4=="pandas" && $5=="0.0.1"' "$T/b.txt")
S3=$(zahl '$1=="PAKET" && $2=="W1" && $4=="kein-solches-paket-tb140" && $6=="FEHLT"' "$T/b.txt")
N1=$(zahl '$1=="PAKET" && ($5=="0.0.1" || $4=="kein-solches-paket-tb140")' "$T/a.txt")
if grep -q '^W2 NICHT MESSBAR' "$T/b.txt"; then S4=-; S5=-
else
  S4=$(zahl '$1=="PAKET" && $2=="W2" && $4=="pandas" && $5=="0.0.1"' "$T/b.txt")
  S5=$(zahl '$1=="PAKET" && $2=="W2" && $4=="kein-solches-paket-tb140" && $6=="FEHLT"' "$T/b.txt")
fi
echo "## Soll"
echo "zweite Kopie: rc $RC2 (Soll 1) · KOPF plattform ABWEICHUNG $S1 (Soll 1) · PAKET W1 pandas 0.0.1: $S2 (Soll 1) · PAKET W1 kein-solches-paket-tb140 FEHLT: $S3 (Soll 1)"
echo "zweite Kopie, W2: PAKET W2 pandas 0.0.1: $S4 · PAKET W2 kein-solches-paket-tb140 FEHLT: $S5 (Soll je 1; ein Strich heisst: W2 war nicht messbar, die zwei Zeilen entfallen)"
echo "erste Kopie: keine dieser PAKET-Zeilen: $N1 (Soll 0)"
if [ "$RC1" = 2 ] || [ "$RC2" = 2 ]; then echo "GEGENPROBE: NICHT MESSBAR"; exit 2; fi
if [ "$RC2" = 1 ] && [ "$S1$S2$S3$N1" = "1110" ] && { [ "$S4$S5" = "11" ] || [ "$S4$S5" = "--" ]; }; then echo "GEGENPROBE: beisst"; exit 0; fi
echo "GEGENPROBE: beisst NICHT"; exit 1

#!/bin/bash
# TB-112 C Abnahme - test_universum_trockenlauf.py vorher (Fassung HEAD, voruebergehend aus git geholt) und nachher (neue
# Fassung aus der Scratch-Kopie), je mit einem EIGENEN, leeren TMPDIR, damit nichts anderes (parallele Sitzung) mitzaehlt.
# Dazu je Lauf die Zaehlung im System-TMPDIR. Aufruf aus der Repo-Wurzel: bash docs/belege/TB-112/c_abnahme.sh <scratch> <kopie_neu>
set -u
SP="$1"; NEU="$2"; T=research/universum_trockenlauf/test_universum_trockenlauf.py; PY=trading-env/bin/python3
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT
SYS="$TMPDIR"
z() { for pr in tb40_test_fp_ tb40_test_ll_ tb40_test_ tb44_l_; do printf "%s %s  " $pr "$(ls -d "$1"/${pr}* 2>/dev/null | wc -l | tr -d ' ')"; done; printf "alle Eintraege %s" "$(ls -A "$1" | wc -l | tr -d ' ')"; }
cmp -s "$T" "$NEU" || { echo "ABBRUCH: $T ist nicht die Scratch-Kopie"; exit 1; }
echo "# TB-112 C Abnahme, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
for fall in vorher nachher; do
  if [ $fall = vorher ]; then git show HEAD:$T > "$T"; else cp "$NEU" "$T"; fi
  echo "## $fall: $T sha256 $(shasum -a 256 "$T" | cut -c1-16), git diff --numstat [$(git diff --numstat -- "$T" | tr '\t' ' ')]"
  E="$SP/c_tmp_$fall"; if [ -e "$E" ]; then echo "ABBRUCH: $E existiert"; exit 1; fi; mkdir -p "$E"
  echo "   eigenes TMPDIR vorher:  $(z "$E")"
  echo "   System-TMPDIR vorher:   $(z "$SYS")"
  T0=$(date +%s); TMPDIR="$E/" $PY -W ignore "$T" > "$SP/c_test_$fall.txt" 2>&1; rc=$?
  echo "   test rc=$rc $(( $(date +%s)-T0 ))s: $(grep -iE 'bestanden|GESCHEITERT' "$SP/c_test_$fall.txt" | tail -1)"
  echo "   eigenes TMPDIR nachher: $(z "$E")"
  echo "   System-TMPDIR nachher:  $(z "$SYS")"
done
cmp -s "$T" "$NEU" && echo "# neue Fassung liegt wieder im Arbeitsbaum" || echo "# FEHLER: neue Fassung nicht zurueckgelegt"
echo "## Ende $(date '+%H:%M:%S')"

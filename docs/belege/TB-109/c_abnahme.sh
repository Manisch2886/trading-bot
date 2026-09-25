#!/bin/bash
# TB-109 C - Abnahme universum_trockenlauf.py ohne Modus: ut.json und sf.json gegen g2_vorher (Stand f4d6d6d),
# tb40_* im TMPDIR vor und nach dem Lauf. Eigenes TMPDIR (<scratch>/c_tmp), damit nur die Ordner dieser Laeufe
# gezaehlt werden (eine parallele Sitzung im Worktree schreibt ins System-TMPDIR). Dazu ein Lauf mit dem System-TMPDIR.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-109/c_abnahme.sh <scratch>
set -u
SP="$1"; PY=trading-env/bin/python3; U=research/universum_trockenlauf/universum_trockenlauf.py
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT
Z="$SP/c_nachher"; T="$SP/c_tmp"
if [ -e "$Z" ] || [ -e "$T" ]; then echo "ABBRUCH: $Z oder $T existiert"; exit 1; fi
mkdir -p "$Z" "$T"
zaehle() { for pr in tb40_lauf_ tb40_faltenplan_ tb40_proben_; do printf "%s %s  " $pr "$(ls -d "$1"/${pr}* 2>/dev/null | wc -l | tr -d ' ')"; done; echo; }
echo "# TB-109 C Abnahme, HEAD $(git rev-parse --short HEAD), Arbeitsbaum research/universum_trockenlauf: [$(git status --porcelain -- research/universum_trockenlauf | tr '\n' ' ')], $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## eigenes TMPDIR $T"
echo "   vorher:            $(zaehle "$T")"
TMPDIR="$T" $PY -W ignore $U --json "$Z/ut.json" > "$Z/ut.txt" 2>&1; echo "   ut --json rc=$?"
echo "   nach ut --json:    $(zaehle "$T")   (hole_faltenplan() ohne --faltenplan-json + 9 x messe_bot)"
TMPDIR="$T" $PY -W ignore $U --stille-filter --json "$Z/sf.json" > "$Z/sf.txt" 2>&1; echo "   sf --json rc=$?"
echo "   nach --stille-filter: $(zaehle "$T")"
echo "   alles unter $T: [$(ls -A "$T" | tr '\n' ' ')]"
echo "## Vergleich gegen g2_vorher"
for f in ut sf; do shasum -a 256 "$Z/$f.json" | sed "s#$SP/##"; cmp -s "$Z/$f.json" "$SP/g2_vorher/$f.json" && echo "   $f BYTEGLEICH" || echo "   $f VERSCHIEDEN"; done
echo "## System-TMPDIR ($TMPDIR), ein Lauf ut --json (Zaehlung kann durch die parallele Sitzung gestoert sein)"
echo "   vorher:  $(zaehle "$TMPDIR")"
$PY -W ignore $U --json "$Z/ut2.json" > "$Z/ut2.txt" 2>&1; echo "   ut --json rc=$?"
echo "   nachher: $(zaehle "$TMPDIR")"
cmp -s "$Z/ut2.json" "$SP/g2_vorher/ut.json" && echo "   ut2 BYTEGLEICH" || echo "   ut2 VERSCHIEDEN"
echo "## test_universum_trockenlauf.py, test_zwischenablage.py"
for t in test_universum_trockenlauf test_zwischenablage; do
  O=docs/belege/TB-109/c_$t.txt; T0=$(date +%s); $PY -W ignore research/universum_trockenlauf/$t.py > $O 2>&1; RC=$?
  echo "   $t rc=$RC $(( $(date +%s) - T0 ))s  $(grep -E 'bestanden|GESCHEITERT' $O | tail -1)"
done
echo "## Ende $(date '+%H:%M:%S')"

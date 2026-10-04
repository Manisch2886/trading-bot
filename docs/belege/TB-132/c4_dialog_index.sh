#!/bin/bash
# TB-132 C4 - Dialog-Index (Bauart TB-130 C4): Handfelder gegen den Auftrag am S0 (cmp), dialog_index.py --handfelder,
# dann --pruefen; Zeilen 02a, 02b, 02c, Schlusszeile, numstat und geaenderte Zeilen. Ausgabe nach stdout.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-132/c4_dialog_index.sh <S0> <scratch>
set -u
S0="$1"; SP="$2"; PY=trading-env/bin/python3; BL=docs/belege/TB-132; D=docs/projektfuehrung/FABLE_DIALOG_INDEX.md
echo "# TB-132 C4 (HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z'))"
git show $S0:docs/auftraege/MAC_TB-132_register_fable_02c.md | awk '/^\*\*C4\. Dialog-Index\.\*\*/{f=1} f&&/^```$/{n++; next} f&&n==1{print} n==2{exit}' > "$SP/c4_handfelder_soll.json"
echo "## Handfelder gleich dem Auftrag (cmp): $(cmp -s "$SP/c4_handfelder_soll.json" $BL/c4_handfelder.json && echo ja || echo NEIN)"
echo "## dialog_index.py --handfelder $BL/c4_handfelder.json"
$PY docs/werkzeuge/dialog_index.py --handfelder $BL/c4_handfelder.json; echo "rc $?"
echo "## dialog_index.py --pruefen"
$PY docs/werkzeuge/dialog_index.py --pruefen; echo "rc $?"
for b in 02a 02b 02c; do echo "## Zeile $b"; grep "^| $b |" $D; done
echo "## Schlusszeile"; grep -v '^[[:space:]]*$' $D | tail -1
echo "## git diff --numstat"; git diff --numstat -- $D
echo "## geänderte Zeilen (diff -U0)"; git diff -U0 -- $D | grep '^[-+]' | grep -v '^\(---\|+++\)'

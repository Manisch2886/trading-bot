#!/bin/bash
# TB-139 A4 - Probelauf gegen eine Kopie des Registers, Textpruefungen aus A5 an der Kopie.
# Vorlage docs/belege/TB-136/a4_probelauf.sh; das Einfuegeskript nimmt die Kopie hier ueber --register (nicht ueber eine Umgebungsvariable).
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-139/a4_probelauf.sh <scratch> <S0> <datum>
set -u
SP="$1"; S0="$2"; D="$3"; PY=trading-env/bin/python3; BL=docs/belege/TB-139; R=docs/VORREGISTRIERUNG_neuselektion.md
K="$SP/a4_probe_$(date +%H%M%S).md"
echo "# TB-139 A4 Probelauf, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "Register $(shasum -a 256 $R | cut -c1-16), Kopie $K"
cp $R "$K"
echo "## git diff --quiet $S0 -- Auftrag Quelle Anfrage Eroeffnungstext"; git diff --quiet $S0 -- docs/auftraege/MAC_TB-139_register_fable_07a.md docs/projektfuehrung/FABLE_ANTWORT_2026-10-07a_schnitt_im_erzeuger_wache_ein_eintrag.md docs/projektfuehrung/FABLE_ANFRAGE_2026-10-07a_go_live_schnitt_voraussetzungen.md docs/projektfuehrung/FABLE_UEBERGABE_2026-10-07_eroeffnung.md; echo "rc $?"
echo "## Einsetzen gegen die Kopie"; $PY $BL/a4_eintrag.py --s0 $S0 --datum $D --register "$K"; echo "rc $?"
echo "## Register selbst unberuehrt: $(shasum -a 256 $R | cut -c1-16)"
echo "## a5_r_diff.py";    $PY $BL/a5_r_diff.py $S0 "$K" | tail -1; echo "rc ${PIPESTATUS[0]}"
echo "## a5_mutation.py";  $PY $BL/a5_mutation.py $S0 "$K" "$K.mutation" | tail -1; echo "rc ${PIPESTATUS[0]}"
echo "## a5_zitate.py";    $PY $BL/a5_zitate.py $S0 $D "$K" | tail -1; echo "rc ${PIPESTATUS[0]}"
echo "## a5_marken.py";    $PY $BL/a5_marken.py $S0 $D "$K" | grep -v " Zeile [0-9]"; echo "rc ${PIPESTATUS[0]}"
echo "## numstat Original -> Kopie"; git diff --no-index --numstat $R "$K" | cut -f1,2
echo "## Zeilen der Kopie: $(wc -l < "$K" | tr -d ' ')"
echo "KOPIE=$K"

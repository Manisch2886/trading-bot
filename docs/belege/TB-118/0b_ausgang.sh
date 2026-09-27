#!/bin/bash
# TB-118 0b - Ausgangswerte nach Auftrag Schritt 0b. Rein lesend. Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-118/0b_ausgang.sh > docs/belege/TB-118/0b_ausgang.txt
set -u
R=docs/VORREGISTRIERUNG_neuselektion.md
echo "# TB-118 0b, $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "HEAD $(git rev-parse HEAD)"
echo "## wc -l Register"; wc -l $R
echo "## hoechste Abschnittsnummer"; grep -E '^## [0-9]+\.' $R | tail -1
echo "## sha256 Register"; shasum -a 256 $R
echo "## wc -l BACKLOG.md"; wc -l docs/projektfuehrung/BACKLOG.md
echo "## FABLE_*.md unter docs/projektfuehrung/ (Bytes Pfad)"
wc -c docs/projektfuehrung/FABLE_*.md | sed '$d'; ls docs/projektfuehrung/FABLE_*.md | wc -l | sed 's/^ */Anzahl /'
echo "## docs/auftraege/MAC_TB-*.md (Bytes Pfad)"
wc -c docs/auftraege/MAC_TB-*.md | sed '$d'; ls docs/auftraege/MAC_TB-*.md | wc -l | sed 's/^ */Anzahl /'
echo "## docs/ERGEBNIS_TB-*.md (Bytes Pfad)"
wc -c docs/ERGEBNIS_TB-*.md | sed '$d'; ls docs/ERGEBNIS_TB-*.md | wc -l | sed 's/^ */Anzahl /'
echo "## Ende"

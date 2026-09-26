#!/bin/bash
# TB-112 A5 - die 8 Ausgaben ohne Modus (g2_ausgaben.sh) mit dem neuen paths.py (nachher) und mit dem paths.py des
# Eingangs-Commits e731207 (vorher; die Datei wird dafuer voruebergehend aus git geholt und danach aus der
# Scratch-Kopie zurueckgelegt). Sonst ist der Arbeitsbaum in beiden Laeufen gleich (die neue Testdatei liegt daneben,
# kein Lauf importiert sie). Aufruf aus der Repo-Wurzel: bash docs/belege/TB-112/a5_ausgaben.sh <scratch> <kopie_neu>
set -u
SP="$1"; NEU="$2"
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT
cmp -s shared/paths.py "$NEU" || { echo "ABBRUCH: shared/paths.py ist nicht die Scratch-Kopie"; exit 1; }
echo "# nachher: shared/paths.py sha256 $(shasum -a 256 shared/paths.py | cut -c1-16)"
bash docs/belege/TB-112/g2_ausgaben.sh "$SP/a5_nachher"
git show e731207:shared/paths.py > shared/paths.py
echo "# vorher: shared/paths.py = e731207 (git diff --stat: [$(git diff --stat -- shared/paths.py | tr '\n' ' ')]) sha256 $(shasum -a 256 shared/paths.py | cut -c1-16)"
bash docs/belege/TB-112/g2_ausgaben.sh "$SP/a5_vorher"
cp "$NEU" shared/paths.py
cmp -s shared/paths.py "$NEU" && echo "# neues paths.py zurueckgelegt" || echo "# FEHLER: paths.py nicht zurueckgelegt"
echo "## Vergleich nachher gegen vorher"
for f in fn embargo fsm lesart plan ut sf eft; do
  cmp -s "$SP/a5_nachher/$f.json" "$SP/a5_vorher/$f.json" && echo "$f BYTEGLEICH" || echo "$f VERSCHIEDEN"; done
echo ENDE

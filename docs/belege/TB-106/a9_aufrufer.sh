#!/bin/bash
# TB-106 A9 - Aufrufer der vier Dateien ausserhalb des Modus. Statisch (crontab -l ist in dieser Sitzung
# abgelehnt, wie in TB-105). Aufruf aus der Repo-Wurzel.
echo "# TB-106 A9, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "== (1) crontab -l: in dieser Sitzung abgelehnt (Werkzeugfreigabe) - nicht gemessen"
echo "== (2) Importe/Starts der vier Module im Repo ausserhalb docs/, belege, trading-env (Python-Dateien)"
git grep -n -E "^[[:space:]]*import (faltenplan|benchmark|auswertung|herkunft)( |$)|spec_from_file_location\(.*herkunft|lade_fremdes_modul\(\s*$|\"herkunft\", os.path.join|vorregistrierung/(faltenplan|benchmark|auswertung|herkunft)\.py\"" -- '*.py' ':!docs' | cut -c1-170
echo "== (3) davon im Regelbetrieb (system/ dashboard/ notifications/ broker/ strategies/ shared/ ohne test_*)"
git grep -l -E "vorregistrierung" -- system dashboard notifications broker strategies 'shared/*.py' ':!shared/test_*' | while read f; do
  echo "   $f:"; grep -n -E "import (faltenplan|benchmark|auswertung|herkunft)|herkunft\.py|faltenplan\.py|benchmark\.py|auswertung\.py" "$f" | cut -c1-150 | sed "s/^/      /"; done
echo "== (4) Nutzer von herkunft.block / herkunft.anhaengen (ausser herkunft.py selbst)"
git grep -n -E "\.(block|anhaengen)\(" -- '*.py' ':!docs' | grep -i "herkunft\|\bh\.\|hk\." | grep -v "^research/vorregistrierung/herkunft.py" | grep -v "^research/turn_of_month" || echo "   keine"
echo "== (5) shared/snapshot.py ruft herkunft.datenstand MIT Pfad (unberuehrt von E1):"
grep -n "datenstand(" shared/snapshot.py | cut -c1-140

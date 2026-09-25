#!/bin/bash
# TB-107 A8 - Aufrufer der vier freigegebenen Dateien im Regelbetrieb. Statisch wie TB-106 A9
# (crontab -l bleibt gesperrt). Aufruf aus der Repo-Wurzel.
echo "# TB-107 A8, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "== (1) crontab -l: gesperrt - nicht gemessen"
for m in faltenschranke_messung faltenplan_neun universum_trockenlauf strategy_paths; do
  echo "== (2) $m: Importe/Nennungen in versionierten .py/.sh ausserhalb docs/ (ohne die Datei selbst)"
  git grep -n -w "$m" -- '*.py' '*.sh' ':!docs' | grep -v -E "^[^:]*/$m\.py:" | cut -c1-160
  echo "   -- davon im Regelbetrieb (system/ dashboard/ notifications/ broker/ strategies/ shared/ ohne test_*):"
  git grep -l -w "$m" -- system dashboard notifications broker strategies 'shared/*.py' ':!shared/test_*' | grep -v "/$m\.py$" | sed 's/^/      /' | sort | uniq
done
echo "== (3) strategy_paths: Nutzer in strategies/ (forward_test.py je Bot und Werkzeuge)"
git grep -l "get_strategy_paths" -- strategies | awk -F/ '{print $3}' | sort | uniq -c
echo "== (4) Ersatzmodule fuer strategy_paths (TB-105 Befund 1)"
git grep -n -E "ModuleType\(.strategy_paths|sys.modules\[.strategy_paths.\]" -- '*.py' ':!docs' | cut -c1-160

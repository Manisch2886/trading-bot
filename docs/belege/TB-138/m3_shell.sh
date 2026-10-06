#!/bin/bash
# TB-138 M3 Nr. 2-4 - Paketfassung des Kalenders (Register 54.6 Nr. 8). Rein lesend.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-138/m3_shell.sh
set -u
PY=trading-env/bin/python3
echo "# TB-138 M3 Nr. 2-4, HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo
echo "## Nr. 2  $PY -B research/snapshotgrenze/erhebung_eingaben.py (ohne --json), nur 'Paketfassung hier'"
AUS=$($PY -B research/snapshotgrenze/erhebung_eingaben.py 2>&1); RC=$?
echo "rc $RC"
printf '%s\n' "$AUS" | grep "Paketfassung hier" || { echo "Zeile nicht gefunden; letzte Zeilen der Ausgabe:"; printf '%s\n' "$AUS" | tail -5; }
echo
echo "## Nr. 3  Interpreter aus: which -a python3 python3.9 python3.10 python3.11 python3.12 python3.13"
LISTE=$(which -a python3 python3.9 python3.10 python3.11 python3.12 python3.13 2>/dev/null)
echo "Liste:"; printf '%s\n' "$LISTE" | sed 's/^/  /'
printf '%s\n' "$LISTE" | while IFS= read -r p; do
  [ -z "$p" ] && continue
  R=$("$p" -B -c "import sys, importlib.metadata as m; print(sys.version.split()[0], m.version('pandas_market_calendars'))" 2>/dev/null)
  if [ $? -eq 0 ]; then echo "$p -> $R"
  else V=$("$p" -B -c "import sys; print(sys.version.split()[0])" 2>/dev/null); echo "$p -> ${V:-?} nicht installiert"; fi
done
echo
echo "## Nr. 4  Nennen docs/ERGEBNIS_TB-47_snapshotgrenze.md oder die Commit-Nachricht von fc38d25 den Interpreter des Laufs?"
echo "### ERGEBNIS_TB-47 (Fundstellen: Sitzungsart, Python, Paketfassung)"
grep -nE "Cloud-Sitzung vom|^\| Python \||pandas_market_calendars 5\.4\.0|Fassung \*\*5\.4\.0" docs/ERGEBNIS_TB-47_snapshotgrenze.md
echo "### Commit fc38d25: Autor und Zeit"
git show -s --format='%h %an %ad' --date=iso fc38d25
echo "### Commit fc38d25: Zeilen der Nachricht mit python/interpreter/3.9/3.11/5.4/venv/trading-env (leer = nicht gefunden)"
git show -s --format='%B' fc38d25 | grep -niE "python|interpreter|3\.9|3\.11|5\.4|venv|trading-env" || echo "nicht gefunden"
echo "### Letzter Commit an eingaben.json"
git log -1 --format='%h %an %ad' --date=iso -- research/snapshotgrenze/ergebnisse/eingaben.json
echo "## Ende"

#!/bin/bash
# Die Bruecken-VM einsatzfaehig machen - gemessen am 23.09.2026 (TB-90)
# ============================================================================
# Die Geraeteanbindung laeuft in einer eigenen, isolierten Linux-VM mit einem
# FUSE-Mount des Repos. Sie hat ihr eigenes Python OHNE die Bot-Abhaengigkeiten;
# `faltenplan.faltenplan()` scheiterte dort an `ModuleNotFoundError: binance`,
# und damit war jede Messung, die den gerechneten Plan braucht, nur auf dem
# MacBook moeglich (TB-88, `A2`).
#
# ⭐ Gemessen am 23.09.2026: Beide fehlenden Pakete lassen sich in der VM
# nachinstallieren. Danach rechnet der Faltenplan dort, und
# `test_vorregistrierung.py` laeuft bis an DIESELBE Stelle wie auf dem Mac
# (`KeyError` in `auswertung.py::zulaessigkeit`).
#
# ⚠️ WAS DAS NICHT IST: die VM ist NICHT der Mac. Sie hat eine andere
# Python-Fassung und andere Paketversionen. Eine Messung hier ist eine
# VORMESSUNG - sie wird von der Mac-Sitzung nachgemessen, nie ersetzt
# (Betreiberentscheidung 23.09.2026; Pruefprinzip `A8`).
#
# ⚠️ Die VM ist sitzungsgebunden: Nach einem Neustart der Anbindung sind die
# Pakete wieder weg. Deshalb dieses Skript - ein Aufruf, und sie ist wieder da.
#
# Aufruf aus der Repo-Wurzel:   bash docs/werkzeuge/bruecke_ausstatten.sh
# ⛔ NICHT auf dem MacBook aufrufen - dort gilt `trading-env`.

set -u

echo "== Wo laufe ich? =="
uname -s -r
python3 --version
echo

if [ "$(uname -s)" != "Linux" ]; then
    echo "⛔ ABBRUCH: Das ist nicht die Linux-Bruecken-VM."
    echo "   Auf dem MacBook gilt das venv: source trading-env/bin/activate"
    exit 1
fi

echo "== Fehlende Pakete =="
for p in binance yfinance; do
    if python3 -c "import $p" 2>/dev/null; then
        echo "  $p: schon da"
    else
        echo "  $p: fehlt"
    fi
done
echo

echo "== Nachinstallieren (nur ins Benutzerverzeichnis der VM) =="
pip3 install --quiet python-binance yfinance 2>&1 | grep -v "^  WARNING: The script" \
    | grep -v "^  Consider adding this directory to PATH" || true
echo

echo "== Probe: rechnet der Faltenplan? =="
cd research/vorregistrierung || { echo "⛔ Nicht in der Repo-Wurzel aufgerufen."; exit 1; }
python3 - <<'PY'
import sys
try:
    import faltenplan as fp, registerdaten as rd
    plan = fp.faltenplan(rd._mess())
except Exception as e:
    print("  ⛔ Der Plan rechnet NICHT: %s: %s" % (type(e).__name__, e))
    print("     Fehlt ein weiteres Paket, nenne es in diesem Skript.")
    sys.exit(1)
print("  ✔ Der Plan rechnet. Bots: %d" % len(plan))
b = sorted(plan)[0]
print("  Stichprobe %s: Bestaetigungsperiode %s"
      % (b, plan[b]["bestaetigungsperiode"]))
print("FERTIG - die Bruecke kann messen (als VORMESSUNG).")
PY

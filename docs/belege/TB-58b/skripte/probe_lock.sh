#!/bin/bash
# Probe: Selektionsmodus mit absichtlich abweichendem Lock -> muss rc 2 sein.
# Laeuft in einem WEGWERF-KLON (kein Objekt, keine Datei im Arbeitsbaum von ~/trading-bot).
set -u
HAUPT=/Users/jaquelineloffler/trading-bot
PY=$HAUPT/trading-env/bin/python3
KLON=$1
SNAP=63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
rm -rf "$KLON"
git clone -q "$HAUPT" "$KLON" || exit 99
cd "$KLON"
git config user.email probe@lokal; git config user.name probe
echo "Klon HEAD: $(git rev-parse HEAD)  (Haupt HEAD: $(git -C $HAUPT rev-parse HEAD))"
cat > probe.py <<'PY'
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "shared"))
import paths
print("DATA_DIR =", paths.DATA_DIR)
print("lock_sha256 =", paths.startpruefung()["lock_sha256"])
PY
git add probe.py && git commit -q -m "probe: Einstiegsdatei" && echo "probe.py committet, HEAD=$(git rev-parse --short HEAD)"
export TB_SELEKTIONSWURZEL="$KLON/snapshots/$SNAP" TB_SELEKTIONSHASH="$SNAP"
echo; echo "=== Kontrolle: unveraenderter Lock, TB_SELEKTIONSCOMMIT=HEAD ==="
TB_SELEKTIONSCOMMIT=$(git rev-parse HEAD) $PY probe.py; echo "rc=$?"
echo; echo "=== Probe: eine Lock-Zeile verfaelscht (pandas==2.3.3 -> pandas==0.0.1), committet ==="
sed -i '' 's/^pandas==2.3.3$/pandas==0.0.1/' requirements.lock
grep -n "^pandas==" requirements.lock
git commit -q -am "probe: Lock absichtlich abweichend" && echo "HEAD=$(git rev-parse --short HEAD), Arbeitsbaum: $(git status --porcelain | wc -l | tr -d ' ') Eintraege"
echo "sha256 des abweichenden Locks: $(shasum -a 256 requirements.lock | cut -c1-64)"
TB_SELEKTIONSCOMMIT=$(git rev-parse HEAD) $PY probe.py; echo "rc=$?"
echo; echo "=== Probe 2: Lock verfaelscht, aber NICHT committet (Arbeitsbaum schmutzig) ==="
git revert --no-edit HEAD >/dev/null && sed -i '' 's/^pandas==2.3.3$/pandas==0.0.1/' requirements.lock
TB_SELEKTIONSCOMMIT=$(git rev-parse HEAD) $PY probe.py; echo "rc=$?"
echo; echo "=== Probe 3: Lock fehlt (geloescht und committet) ==="
git checkout -q -- requirements.lock && git rm -q requirements.lock && git commit -q -m "probe: ohne Lock"
TB_SELEKTIONSCOMMIT=$(git rev-parse HEAD) $PY probe.py; echo "rc=$?"
echo; echo "=== Probe 4: richtiger Lock, /usr/bin/python3 (andere Pakete) ==="
git revert --no-edit HEAD >/dev/null; git status --porcelain | wc -l
TB_SELEKTIONSCOMMIT=$(git rev-parse HEAD) /usr/bin/python3 probe.py; echo "rc=$?"
cd /; rm -rf "$KLON"; echo; echo "Klon entfernt: $(test -e "$KLON" && echo NEIN || echo ja)"

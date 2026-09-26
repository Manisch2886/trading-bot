#!/bin/bash
# TB-117 E - auswertung.py im echten Selektionsmodus (Snapshot 63e4b6c8, TB_SELEKTIONSCOMMIT = HEAD) auf Beispieldaten
# eines Bots, mit herkunft.json fuer alle neun: (1) gut -> rc 0, Kopf "geprueft"; (2) Datenstand eines Bots falsch -> rc 2.
# Schreibt nur nach <scratch>. Aufruf aus der Repo-Wurzel: bash docs/belege/TB-117/e_auswertung_modus.sh <scratch>
set -u
SP="$1"; PY=$PWD/trading-env/bin/python3; V=research/vorregistrierung
SNAP=63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2; BOT=turtle_soup_stocks
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
R="$SP/roh_modus"; [ -e "$R" ] && { echo "ABBRUCH: $R existiert"; exit 1; }
echo "# TB-117 E auswertung.py im Modus, HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "# Arbeitsbaum ausserhalb docs/ (leer = sauber): [$(git status --porcelain -- . ':!docs' | tr '\n' ' ')]"
$PY -W ignore $V/beispieldaten.py --ziel "$R" --bot $BOT > /dev/null 2>&1; echo "beispieldaten rc $?"
$PY -W ignore - "$R" "$(git rev-parse HEAD)" <<'PYEOF'
import json, os, sys
sys.path.insert(0, "research/vorregistrierung")
import herkunft, registerdaten as rd
r, head = sys.argv[1], sys.argv[2]
h = {"commit": head, "datenstand": "d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84",
     "register": herkunft.register()["register"]}
for b in rd.BOTS:
    os.makedirs(os.path.join(r, b), exist_ok=True)
    json.dump(h, open(os.path.join(r, b, "herkunft.json"), "w"))
print("herkunft.json x%d geschrieben: %s" % (len(rd.BOTS), h))
PYEOF
lauf() {
  env TB_SELEKTIONSWURZEL="$PWD/snapshots/$SNAP" TB_SELEKTIONSHASH="$SNAP" TB_SELEKTIONSCOMMIT="$(git rev-parse HEAD)" \
      $PY -W ignore $V/auswertung.py --rohergebnisse "$R" --bot $BOT --json "$SP/$1.json" > "$SP/$1.txt" 2>&1
  echo "## $1: rc $?"; grep -A3 "^HERKUNFT" "$SP/$1.txt"; grep "ABBRUCH" "$SP/$1.txt"
}
lauf modus_gut
$PY -c "
import json; p='$R/rsi2_crypto/herkunft.json'; h=json.load(open(p)); h['datenstand']='0'*64; json.dump(h, open(p,'w'))"
lauf modus_datenstand_falsch

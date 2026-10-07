#!/bin/bash
# TB-140 V6 - der Bestand vom 02.10.2026 an APH. Rein lesend. Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-140/v6_bestand.sh
# Rueckgabe: die von v6_zeile.py am Stand der Messung, das ist Teil (i): 0 genau eine Zeile
# 2026-09-01 ohne close, 1 nicht so, 2 nicht messbar. Die Teile (ii) und (iii) stehen in der Zeile TEIL.
set -u
PY="${PY:-trading-env/bin/python3}"
ZP="${ZP:-docs/belege/TB-140/v6_zeile.py}"
G="git --no-optional-locks"
S=snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
D=data/APH_1d.csv
B=0779453                          # Stand der Messung vom 02.10.2026 (Register Z. 11482; v3_daten.md Z. 3)
GRENZE=2026-10-01T22:00:00+00:00   # der 02.10.2026, 00:00 Uhr nach der Uhr des Repos (+02:00)
echo "# TB-140 V6"; echo "ZEIT $(date '+%Y-%m-%d %H:%M:%S %z')"; echo "HEAD $($G rev-parse HEAD)"
echo "## Stand der Messung vom 02.10.2026"
if ! $G rev-parse --verify --quiet "$B^{commit}" > /dev/null; then
  echo "NICHT MESSBAR: Stand $B unbekannt"; echo "TEIL (i) nicht messbar · (ii) nicht messbar · (iii) nicht messbar"; echo "## Ende"; exit 2
fi
$G log -1 --format='%H %cI %s' "$B"
echo "## Commits an $D (alle)"; $G log --format='%h %cI %s' -- "$D"
echo "## Commits an $D nach dem Stand $B"; NACH=$($G log --format='%h %cI %s' "$B..HEAD" -- "$D"); printf '%s\n' "${NACH:-keiner}"
echo "## Blobs in git"
BB=$($G rev-parse --verify --quiet "$B:$D") || BB=fehlt
echo "$B:$D $BB"
echo "HEAD:$D $($G rev-parse --verify --quiet "HEAD:$D" || echo fehlt)"
echo "$B:$S/APH_1d.csv $($G rev-parse --verify --quiet "$B:$S/APH_1d.csv" || echo fehlt)"
echo "HEAD:$S/APH_1d.csv $($G rev-parse --verify --quiet "HEAD:$S/APH_1d.csv" || echo fehlt)"
echo "## Arbeitsdateien: Blob (gerechnet wie git: sha1 ueber 'blob <Bytes>', ein Nullbyte und den Inhalt; git wird dafuer nicht aufgerufen), sha256, Bytes, Aenderungszeit (UTC)"
AD=$($PY -B -c "import datetime as d, hashlib, os, sys
grenze = d.datetime.fromisoformat(sys.argv[1])
for nr, p in enumerate(sys.argv[2:]):
    try:
        with open(p, 'rb') as f:
            b = f.read()
        zeit = d.datetime.fromtimestamp(os.stat(p).st_mtime, d.timezone.utc)
        blob = hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
        print('ARBEITSDATEI\t%s\tblob %s\tsha256 %s\tbytes %d\tmtime %s' % (
            p, blob, hashlib.sha256(b).hexdigest(), len(b), zeit.isoformat(timespec='seconds')))
        if nr == 0:
            print('WERT\tblob\t%s' % blob)
            print('WERT\tvor_grenze\t%s' % ('ja' if zeit < grenze else 'nein'))
    except Exception as e:
        print('ARBEITSDATEI\t%s\tNICHT LESBAR: %s' % (p, type(e).__name__))" "$GRENZE" "$D" "$S/APH_1d.csv")
printf '%s\n' "$AD"
WB=$(printf '%s\n' "$AD" | awk -F'\t' '$1=="WERT" && $2=="blob" {print $3}')
VOR=$(printf '%s\n' "$AD" | awk -F'\t' '$1=="WERT" && $2=="vor_grenze" {print $3}')
echo "## MANIFEST"
$PY -B -c "import json,sys
try:
    m=json.load(open(sys.argv[1], encoding='utf-8')); e=m['dateien']['APH_1d.csv']
    print('MANIFEST', e['sha256'], e['bytes'], m['zeitpunkt_utc'], m['quelle'])
except Exception as f:
    print('MANIFEST NICHT LESBAR: %s' % type(f).__name__)" "$S/MANIFEST.json"
echo "## Zeile 2026-09-01 am Stand $B (nur Spaltennamen)"
$G show "$B:$D" | $PY -B "$ZP" 2026-09-01; RI=${PIPESTATUS[1]}; echo "rc $RI"
echo "## Zeile 2026-09-01 in der Arbeitsdatei"
if [ -s "$D" ]; then $PY -B "$ZP" 2026-09-01 < "$D"; echo "rc $?"; else echo "NICHT MESSBAR: $D fehlt oder ist leer"; fi
echo "## Teile"
case "$RI" in 0) I=ja;; 1) I=nein;; *) I="nicht messbar";; esac
if [ "$BB" = fehlt ] || [ -z "$WB" ]; then II="nicht messbar"
elif [ "$WB" = "$BB" ] && [ -z "$NACH" ]; then II=ja
else II=nein; fi
case "$VOR" in ja|nein) III=$VOR;; *) III="nicht messbar";; esac
echo "TEIL (i) $I · (ii) $II · (iii) $III"
echo "## Ende"
case "$RI" in 0|1) exit "$RI";; *) exit 2;; esac

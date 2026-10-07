#!/bin/bash
# TB-139 0b/A5 - Ausgangs- bzw. Nachher-Werte (Vorlage docs/belege/TB-136/0b_ausgang.sh, dort nach TB-132 und Bauart TB-117):
# Register (Zeilen, sha256, md5), herkunft.register(), Sonde gegen das gueltige Abbild 46f0ad5d (Text + JSON ohne
# 'zeilen'), registerbericht.py --pruefen, md5 und Bytes der Quelle 07a am Commit S0, Abschnitt 10 und ERZEUGT-Block als Datei.
# Rein lesend bis auf die Belegdateien. Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-139/0b_ausgang.sh <marke: vorher|nachher> <scratch> <S0>
set -u
M="$1"; SP="$2"; S0="$3"; PY=trading-env/bin/python3; V=research/vorregistrierung; BL=docs/belege/TB-139
R=docs/VORREGISTRIERUNG_neuselektion.md; FD=docs/projektfuehrung
AB=$V/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
echo "# TB-139 0b ($M), HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## Register (Soll vorher: 11581 Zeilen, sha256 8d505a38..., md5 757cda8c...)"
echo "Zeilen $(wc -l < $R | tr -d ' ')"
shasum -a 256 $R
md5 -r $R
echo "## Abbild (Soll 46f0ad5d...)"
shasum -a 256 $AB
echo "## herkunft.register() (Soll vorher cfff54ca..., fehlend [], 23 Teile)"
$PY -W ignore -c "
import sys; sys.path.insert(0,'$V'); import herkunft
r = herkunft.register(); print('register', r['register']); print('fehlend', r['fehlend']); print('teile', len(r['teile']))" 2>&1
echo "## Sonde gegen $AB (Soll rc 2, 37/0/0, (ii) 0, Listentext wie bei Erzeugung: ja)"
echo "git status --porcelain vorher: $(git status --porcelain | wc -l | tr -d ' ') Zeilen"
$PY -W ignore shared/sperrlistensonde.py --abbild $AB > "$SP/sonde_$M.txt" 2>&1; echo "rc $?"
echo "git status --porcelain nachher: $(git status --porcelain | wc -l | tr -d ' ') Zeilen"
grep -E "^Pfad-Bestandteile|^\(ii\)|^RUECKGABEWERT|Registertext: |BEFUND|ABWEICHUNG" "$SP/sonde_$M.txt"
$PY -W ignore shared/sperrlistensonde.py --abbild $AB --json > "$SP/sonde_$M.json" 2>/dev/null; echo "Sonde --json rc $?"
echo "Sonde-JSON ohne 'zeilen' sha256: $($PY -c "
import json,hashlib; b=json.load(open('$SP/sonde_$M.json'))
b['ii'].pop('zeilen',None)
print(hashlib.sha256(json.dumps(b,sort_keys=True,ensure_ascii=False).encode()).hexdigest())")"
echo "## registerbericht.py --pruefen (kein Soll; nachher = vorher)"
$PY -W ignore $V/registerbericht.py --pruefen > "$SP/registerbericht_$M.txt" 2>&1; echo "rc $?"
echo "Schlusszeile: $(tail -1 "$SP/registerbericht_$M.txt")"
echo "## md5 und Bytes der Quelle 07a am Commit $S0 und im Arbeitsbaum (Soll 388187e2..., 57165 B)"
Q=FABLE_ANTWORT_2026-10-07a_schnitt_im_erzeuger_wache_ein_eintrag.md
echo "$(git show $S0:$FD/$Q | md5) $(git show $S0:$FD/$Q | wc -c | tr -d ' ') B  $S0:$Q"
echo "$(md5 -q $FD/$Q) $(wc -c < $FD/$Q | tr -d ' ') B  Arbeitsbaum:$Q"
echo "## Abschnitt 10 und ERZEUGT-Block -> $BL/0b_abschnitt10_$M.txt, $BL/0b_erzeugt_$M.txt"
$PY - "$R" "$BL/0b_abschnitt10_$M.txt" "$BL/0b_erzeugt_$M.txt" <<'PYEOF'
import sys
L = open(sys.argv[1], encoding="utf-8").read().split("\n")
a10 = next(i for i, s in enumerate(L) if s.startswith("## 10."))
a11 = next(i for i, s in enumerate(L) if s.startswith("## 11."))
ea = next(i for i, s in enumerate(L) if s.startswith("<!-- ERZEUGT:"))
ee = next(i for i, s in enumerate(L) if s.startswith("<!-- ENDE ERZEUGT -->"))
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(L[a10:a11]) + "\n")
open(sys.argv[3], "w", encoding="utf-8").write("\n".join(L[ea:ee + 1]) + "\n")
print("Abschnitt 10: Z. %d-%d (%d Zeilen); ERZEUGT: Z. %d-%d (%d Zeilen)" % (a10 + 1, a11, a11 - a10, ea + 1, ee + 1, ee - ea + 1))
PYEOF
shasum -a 256 "$BL/0b_abschnitt10_$M.txt" "$BL/0b_erzeugt_$M.txt"
echo "## Ende"

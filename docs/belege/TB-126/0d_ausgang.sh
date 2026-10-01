#!/bin/bash
# TB-126 0d/A6 - Ausgangs- bzw. Nachher-Werte (Bauart TB-117 0b_ausgang.sh, a_messung.sh, b_sonde.sh):
# Register (Zeilen, sha256, md5), herkunft.register(), Sonde gegen das gueltige Abbild 46f0ad5d (Text + JSON ohne
# 'zeilen'), registerbericht.py --pruefen, md5 der drei Quellen am Commit S0, Abschnitt 10 und ERZEUGT-Block als Datei.
# Rein lesend bis auf die Belegdateien. Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-126/0d_ausgang.sh <marke: vorher|nachher> <scratch> <S0>
set -u
M="$1"; SP="$2"; S0="$3"; PY=trading-env/bin/python3; V=research/vorregistrierung; BL=docs/belege/TB-126
R=docs/VORREGISTRIERUNG_neuselektion.md; FD=docs/projektfuehrung
AB=$V/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR
echo "# TB-126 0d ($M), HEAD $(git rev-parse HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## Register (Soll vorher: 10347 Zeilen, sha256 18e39ee2..., md5 c8a32c0f...)"
echo "Zeilen $(wc -l < $R | tr -d ' ')"
shasum -a 256 $R
md5 -r $R
echo "## Abbild (Soll 46f0ad5d...)"
shasum -a 256 $AB
echo "## herkunft.register() (Soll vorher 01f5997a..., fehlend [], 23 Teile)"
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
echo "## md5 der Quellen am Commit $S0 (Soll 27c ff96392e..., 29b 898d5bd5..., 30a f9cdbbef...)"
for Q in FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md FABLE_ANTWORT_2026-09-29b_sammlung_erzeuger_kalter_leser.md FABLE_ANTWORT_2026-09-30a_vorgepruefte_fragen_e2.md; do
  echo "$(git show $S0:$FD/$Q | md5) $(git show $S0:$FD/$Q | wc -c | tr -d ' ') B  $Q"
done
echo "## Abschnitt 10 und ERZEUGT-Block -> $BL/0d_abschnitt10_$M.txt, $BL/0d_erzeugt_$M.txt"
$PY - "$R" "$BL/0d_abschnitt10_$M.txt" "$BL/0d_erzeugt_$M.txt" <<'PYEOF'
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
shasum -a 256 "$BL/0d_abschnitt10_$M.txt" "$BL/0d_erzeugt_$M.txt"
echo "## Ende"

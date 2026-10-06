#!/bin/bash
# TB-138 Gegenprobe vor den Messungen (Pruefprinzipien B1, "Eine Mutationsprobe
# muss beissen"). Legt in $TMPDIR zwei Kopien eines kleinen Snapshots an
# (drei Aktien, zwei Krypto-Symbole, die zwei Universumsdateien auf diese
# Symbole gekuerzt). Kopie 1 bleibt unveraendert, Kopie 2 traegt acht Eingriffe
# G1-G8. Danach m1 und m2 an beiden Kopien; verglichen werden nur die
# FALL-Zeilen (Messung, Art, Symbol, Datum). Kein Kurs wird ausgegeben; eine
# eingefuegte Zeile traegt in den Kursspalten den Text x.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-138/gegenprobe.sh
set -u
PY="trading-env/bin/python3 -B"
SK=docs/belege/TB-138/verfahrensmessung_snapshot.py
S=snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
AKT="AAPL MSFT JNJ"; KRY="BTCUSDT ETHUSDT"
W=$(mktemp -d "${TMPDIR:-/tmp}/tb138_gegenprobe.XXXXXX")
echo "# TB-138 Gegenprobe, HEAD $(git rev-parse HEAD)"
echo "Arbeitsordner $W (nicht committet)"
for k in kopie1 kopie2; do
  mkdir -p "$W/$k/config"
  for s in $AKT; do cp "$S/${s}_1d.csv" "$W/$k/"; done
  for s in $KRY; do for tf in 1d 1h 4h; do cp "$S/${s}_${tf}.csv" "$W/$k/"; done; done
  printf '%s\n' $AKT > "$W/$k/config/sp500_top150.txt"
  printf '%s\n' $KRY > "$W/$k/config/top25_symbols.txt"
done
echo "Symbole: Aktien $AKT; Krypto $KRY"
echo
echo "## Eingriffe in kopie2 (nur Symbol, Datum, Art)"
$PY - "$W/kopie2" <<'PYEOF'
import csv, datetime as dt, os, sys
k = sys.argv[1]

def lies(s):
    with open(os.path.join(k, s + "_1d.csv"), newline="") as f:
        z = list(csv.reader(f))
    return z[0], z[1:]

def schreib(s, kopf, zeilen):
    with open(os.path.join(k, s + "_1d.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(kopf); w.writerows(zeilen)

def index(zeilen, tag):
    t = [i for i, z in enumerate(zeilen) if z[0][:10] == tag]
    assert len(t) == 1, (tag, len(t))
    return t[0]

def entferne(s, tag, g):
    kopf, z = lies(s); del z[index(z, tag)]; schreib(s, kopf, z)
    print("%s  %-8s %s  Zeile entfernt" % (g, s, tag))

entferne("AAPL", "2021-03-10", "G1")
for s in ("AAPL", "MSFT", "JNJ"):
    entferne(s, "2022-06-08", "G2")
# G3: Samstag einfuegen
kopf, z = lies("AAPL"); tag = "2023-04-15"
assert dt.date.fromisoformat(tag).weekday() == 5
pos = max(i for i, r in enumerate(z) if r[0][:10] < tag) + 1
z.insert(pos, [tag] + ["x"] * (len(kopf) - 1)); schreib("AAPL", kopf, z)
print("G3  AAPL     %s  Zeile an einem Samstag eingefuegt (Kursspalten x)" % tag)
# G4: letzte fuenf Zeilen
kopf, z = lies("JNJ"); weg = [r[0][:10] for r in z[-5:]]; z = z[:-5]
schreib("JNJ", kopf, z)
print("G4  JNJ      %s..%s  letzte fuenf Zeilen entfernt, neues Ende %s"
      % (weg[0], weg[-1], z[-1][0][:10]))
# G5: Zeile verdoppeln
kopf, z = lies("JNJ"); i = index(z, "2024-02-14"); z.insert(i + 1, list(z[i]))
schreib("JNJ", kopf, z)
print("G5  JNJ      2024-02-14  Zeile verdoppelt")
# G6: close leeren
kopf, z = lies("MSFT"); i = index(z, "2020-11-18"); z[i][kopf.index("close")] = ""
schreib("MSFT", kopf, z)
print("G6  MSFT     2020-11-18  close geleert")
# G7: Zeitanteil
kopf, z = lies("BTCUSDT"); i = index(z, "2023-03-15")
assert len(z[i][0]) == 10, z[i][0]
z[i][0] = z[i][0] + " 05:00:00"; schreib("BTCUSDT", kopf, z)
print("G7  BTCUSDT  2023-03-15  open_time + ' 05:00:00'")
entferne("ETHUSDT", "2025-01-22", "G8")
PYEOF
echo "rc Eingriffe $?"
NEUENDE=$(tail -1 "$W/kopie2/JNJ_1d.csv" | cut -d, -f1)

for k in kopie1 kopie2; do for m in m1 m2; do
  echo; echo "=================================================================="
  echo "## $m an $k"
  $PY $SK $m --snapshot "$W/$k" > "$W/${m}_$k.txt" 2>&1; rc=$?
  cat "$W/${m}_$k.txt"; echo "rc $rc"; echo "$rc" > "$W/${m}_$k.rc"
done; done

echo; echo "=================================================================="
echo "## Vergleich der FALL-Zeilen (Felder 1-5: FALL, Messung, Art, Symbol, Datum)"
for k in kopie1 kopie2; do
  cat "$W/m1_$k.txt" "$W/m2_$k.txt" | grep '^FALL' | cut -f1-5 | LC_ALL=C sort > "$W/fall_$k.txt"
done
echo "nur an kopie1:"; LC_ALL=C comm -23 "$W/fall_kopie1.txt" "$W/fall_kopie2.txt"; echo "[Ende]"
echo "nur an kopie2:"; LC_ALL=C comm -13 "$W/fall_kopie1.txt" "$W/fall_kopie2.txt" | tee "$W/diff.txt"; echo "[Ende]"
T=$(printf '\t')
{
  echo "FALL${T}m1${T}nur_in_H${T}-${T}2022-06-08"
  echo "FALL${T}m1${T}nur_in_K${T}AAPL${T}2023-04-15"
  echo "FALL${T}m1${T}close_fehlt_leer${T}MSFT${T}2020-11-18"
  echo "FALL${T}m2${T}luecke${T}AAPL${T}2021-03-10"
  echo "FALL${T}m2${T}luecke${T}AAPL${T}2022-06-08"
  echo "FALL${T}m2${T}luecke${T}MSFT${T}2022-06-08"
  echo "FALL${T}m2${T}luecke${T}JNJ${T}2022-06-08"
  echo "FALL${T}m2${T}frueher_endend_1d${T}JNJ${T}$NEUENDE"
  echo "FALL${T}m2${T}doppelt_open_time${T}JNJ${T}2024-02-14"
  echo "FALL${T}m2${T}luecke${T}MSFT${T}2020-11-18"
  echo "FALL${T}m2${T}zeitanteil${T}BTCUSDT${T}2023-03-15"
  echo "FALL${T}m2${T}luecke${T}ETHUSDT${T}2025-01-22"
} | LC_ALL=C sort > "$W/soll.txt"
echo "Soll (G1-G8):"; cat "$W/soll.txt"; echo "[Ende]"
if cmp -s "$W/soll.txt" "$W/diff.txt" && [ ! -s <(LC_ALL=C comm -23 "$W/fall_kopie1.txt" "$W/fall_kopie2.txt") ]; then
  echo "Unterschied gleich Soll: ja"
else
  echo "Unterschied gleich Soll: NEIN"
fi
echo "rc an kopie2 (Soll m1 1, m2 1): m1 $(cat "$W/m1_kopie2.rc"), m2 $(cat "$W/m2_kopie2.rc")"
echo "rc an kopie1 (kein Soll): m1 $(cat "$W/m1_kopie1.rc"), m2 $(cat "$W/m2_kopie1.rc")"
echo "## Ende"

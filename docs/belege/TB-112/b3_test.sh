#!/bin/bash
# TB-112 B3 - db_sicherung.sh zweimal hintereinander gegen ein Testziel, Originale sha256 und mtime vorher/nachher.
# ⚠️ Abweichung vom Auftrag: das Testziel liegt im Scratchpad der Sitzung (Argument), nicht unter $TMPDIR,
# weil `rm` in dieser Sitzung abgelehnt wird - das Scratchpad ist ein sitzungseigener Temp-Ordner.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-112/b3_test.sh <scratch>
set -u
SP="$1"; S=docs/werkzeuge/db_sicherung/db_sicherung.sh
q() { for f in $(ls *.db strategies/*/*.db 2>/dev/null | sort); do echo "$(shasum -a 256 "$f" | cut -c1-64)  $(stat -f '%Sm' -t '%Y-%m-%d %H:%M:%S' "$f")  $f"; done; }
TZIEL="$SP/b3_testziel"
if [ -e "$TZIEL" ]; then echo "ABBRUCH: $TZIEL existiert"; exit 1; fi
echo "# TB-112 B3, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z'), Testziel <scratch>/b3_testziel"
echo "## Zwischenordner db_sicherung.* in \$TMPDIR vorher: $(ls -d "$TMPDIR"/db_sicherung.* 2>/dev/null | wc -l | tr -d ' ')"
q > "$SP/b3_vorher.txt"; echo "## Originale vorher (sha256, mtime)"; cat "$SP/b3_vorher.txt"
for lauf in 1 2; do
  echo "## Lauf $lauf"; T0=$(date +%s)
  bash "$S" "$TZIEL" | sed "s#$TZIEL#<testziel>#g"
  echo "   rc=${PIPESTATUS[0]} Laufzeit $(( $(date +%s)-T0 ))s"
done
echo "## Testziel: Dateien"
(cd "$TZIEL" && find . -type f | sort | while read -r f; do echo "   $f $(wc -c < "$f" | tr -d ' ') B"; done)
echo "## je Satz: SHA256SUMS vollstaendig und stimmig (shasum -c), integrity_check je Datei erneut"
for d in "$TZIEL"/*/; do
  n=$(basename "$d"); z=$(grep -c . "$d/SHA256SUMS"); dbs=$(cd "$d" && find . -name '*.db' | wc -l | tr -d ' ')
  c=$(cd "$d" && shasum -a 256 -c SHA256SUMS 2>&1 | grep -c ': OK$')
  ic=$(cd "$d" && find . -name '*.db' | sort | while read -r f; do sqlite3 -readonly "$f" "PRAGMA integrity_check;"; done | sort | uniq -c | tr -s ' ' | tr '\n' ' ')
  echo "   $n: SHA256SUMS $z Zeilen, $dbs Datenbanken, shasum -c OK $c, integrity_check [$ic]"
done
echo "## Groesse eines Satzes (du -sk)"; for d in "$TZIEL"/*/; do echo "   $(du -sk "$d" | cut -f1) KiB  $(basename "$d")"; done
q > "$SP/b3_nachher.txt"; echo "## Originale nachher gegen vorher"
diff "$SP/b3_vorher.txt" "$SP/b3_nachher.txt" && echo "   gleich (sha256 und mtime aller $(wc -l < "$SP/b3_vorher.txt" | tr -d ' '))"
echo "## Zwischenordner db_sicherung.* in \$TMPDIR nachher: $(ls -d "$TMPDIR"/db_sicherung.* 2>/dev/null | wc -l | tr -d ' ')"
echo "## Ende $(date '+%H:%M:%S')"

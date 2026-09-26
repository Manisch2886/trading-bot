#!/bin/bash
# TB-112 B2 - Schema der gesicherten KOPIEN (nicht der Originale): Tabellen- und Spaltennamen, nie Werte.
# Dazu die Gegenprobe: ein Wegwerf-Repo mit einer Datenbank, die eine Spalte `api_key` hat -> das Skript sichert sie nicht, rc 1.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-112/b2_schema.sh <satzordner> <scratch>
set -u
SATZ="$1"; SP="$2"
echo "# TB-112 B2 Schema je Kopie (Satz $(basename "$SATZ")), Muster key|secret|token|api|passw auf Spaltennamen"
(cd "$SATZ" && find . -name '*.db' | sort | sed 's#^\./##') | while read -r f; do
  s=$(sqlite3 -readonly "$SATZ/$f" "SELECT m.name || '.' || c.name FROM sqlite_master m JOIN pragma_table_info(m.name) c WHERE m.type='table' ORDER BY 1;")
  t=$(sqlite3 -readonly "$SATZ/$f" "SELECT count(*) FROM sqlite_master WHERE type='table';")
  n=$(printf '%s\n' "$s" | grep -c .); h=$(printf '%s\n' "$s" | awk -F. 'tolower($2) ~ /key|secret|token|api|passw/' | grep -c .)
  echo "## $f: $t Tabellen, $n Spalten, Treffer $h"
  printf '%s\n' "$s" | grep . | awk -F. '{a[$1]=a[$1] " " $2} END {for (k in a) print "   " k ":" a[k]}' | sort
done
echo
echo "# Gegenprobe: Wegwerf-Repo <scratch>/b2_gegenprobe mit einer Datenbank mit Spalte api_key (Wert wird nie ausgegeben)"
W="$SP/b2_gegenprobe"; if [ -e "$W" ]; then echo "ABBRUCH: $W existiert"; exit 1; fi
mkdir -p "$W/repo/docs/werkzeuge/db_sicherung" "$W/repo/strategies/x"
cp docs/werkzeuge/db_sicherung/db_sicherung.sh "$W/repo/docs/werkzeuge/db_sicherung/"
sqlite3 "$W/repo/verdacht.db" "CREATE TABLE zugang(id INTEGER, api_key TEXT); INSERT INTO zugang VALUES (1, 'NICHT-AUSGEBEN');"
sqlite3 "$W/repo/strategies/x/harmlos.db" "CREATE TABLE trades(id INTEGER, preis REAL);"
bash "$W/repo/docs/werkzeuge/db_sicherung/db_sicherung.sh" "$W/ziel" | sed "s#$W#<gegenprobe>#g; s#$TMPDIR#\$TMPDIR/#g"
echo "   rc=${PIPESTATUS[0]}"
echo "   im Ziel: $(cd "$W/ziel" && find . -type f | sort | tr '\n' ' ')"
echo "   Wert 'NICHT-AUSGEBEN' im Ziel gefunden: $(grep -rl 'NICHT-AUSGEBEN' "$W/ziel" | wc -l | tr -d ' ') Dateien"

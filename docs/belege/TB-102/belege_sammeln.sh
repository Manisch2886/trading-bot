#!/bin/bash
# TB-102: traegt die Scratchpad-Ausgaben in die Belegdateien zusammen.
# Aufruf aus der Repo-Wurzel:  bash docs/belege/TB-102/belege_sammeln.sh <scratch-tb102>
SC="$1"; B=docs/belege/TB-102
S=snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
K() { sed "s#$SC#<scratch>#g; s#$PWD/#<repo>/#g; s#$PWD#<repo>#g"; }

{ echo "# TB-102 B1 - messgroessen.py im Selektionsmodus gegen Snapshot 63e4b6c8 (lauf.sh modus)"
  cat "$SC/b1_kopf.txt"; echo; echo "## Volle Ausgabe"; cat "$SC/b1_modus/ausgabe.txt"
  echo; echo "## Lesequellen (Lesehaken TB-98, lesequellen.py)"; cat "$SC/b1_quellen.txt"
  echo; echo "=================================================================="
  echo "# ZUSATZPROBEN (Hilfsbaeume aus Verknuepfungen im Scratchpad, nur TB30A_BASE_DIR)"
  echo "# Z1: Snapshot unveraendert (alle Eintraege verknuepft) + NUR haltedauern_je_bot.csv aus dem Repo"
  cat "$SC/z1_kopf.txt"; sed -n '/Herkunft/,$p' "$SC/z1_quellen.txt"
  echo; echo "# Z2: Snapshot-Inhalt in Repo-Anordnung (data -> Snapshot-Wurzel, config -> Snapshot/config) + haltedauern_je_bot.csv aus dem Repo"
  cat "$SC/z2_kopf.txt"; sed -n '/Herkunft/,$p' "$SC/z2_quellen.txt"
  echo; echo "# Z2 wiederholt (z2b):"; grep -E '^rc=|^[0-9a-f]{64}' "$SC/z2b_kopf.txt"
  echo; echo "# Z3: NUR die TB_SELEKTIONS*-Variablen der Bots (Selektionsmodus von shared/paths.py), OHNE TB30A_BASE_DIR"
  grep -E '^#|^rc=|^[0-9a-f]{64}' "$SC/z3_kopf.txt"
  cmp "$SC/z3/messgroessen.json" research/vorregistrierung/ergebnisse/messgroessen_2026-09-23_nachweis.json \
    && echo "Z3 bytegleich zu messgroessen_2026-09-23_nachweis.json (7f46d5f5)"
  sed -n '/Herkunft/,$p' "$SC/z3_quellen.txt" | grep -v "^  \[REPO data/\]" | grep -v 'messgroessen.py:100 (2 x)'
  echo "(die 222 Zeilen [REPO data/] ... messgroessen.py:100 sind oben ausgelassen; Zahl siehe Herkunftstabelle)"
} | K > $B/b1_modus.txt

{ echo "# TB-102 B2 - Gegenprobe ohne Modus (lauf.sh ohne)"; cat "$SC/b2_kopf.txt"
  echo; echo "## Vergleiche"
  cmp "$SC/b2_ohne/messgroessen.json" research/vorregistrierung/ergebnisse/messgroessen_2026-09-23_nachweis.json \
    && echo "B2 bytegleich zu ergebnisse/messgroessen_2026-09-23_nachweis.json (7f46d5f5)"
  echo "B2 gegen ergebnisse/messgroessen.json (2a9b9166):"
  cmp "$SC/b2_ohne/messgroessen.json" research/vorregistrierung/ergebnisse/messgroessen.json
  echo "B2 gegen B1: B1 hat keine Datei geschrieben (rc 1) - kein Vergleich moeglich"
  cmp "$SC/b2_ohne/messgroessen.json" "$SC/z2/messgroessen.json" && echo "B2 bytegleich zu Z2 (Snapshot-Inhalt in Repo-Anordnung)"
  echo; echo "## Byte-Vergleich der von B2 gelesenen Eingaben: Repo gegen Snapshot"
  n=0; d=0
  for f in $(cut -f2 "$SC"/b2_ohne/prot/*.tsv | grep "^$PWD/data/" | sort -u); do
    n=$((n+1)); cmp -s "$f" "$S/$(basename "$f")" || { d=$((d+1)); echo "abweichend: $f"; }
  done
  echo "data/*.csv: $n verglichen, $d abweichend"
  cmp config/top25_symbols.txt $S/config/top25_symbols.txt && cmp config/sp500_top150.txt $S/config/sp500_top150.txt \
    && echo "config/*.txt: 2 verglichen, 0 abweichend"
  echo "haltedauern_je_bot.csv im Snapshot: $(find $S -name 'haltedauern*' | wc -l | tr -d ' ') Treffer"
  echo; echo "## Lesequellen B2"; cat "$SC/b2_quellen.txt" | awk '/Nicht-Code/{exit} {print}'
} | K > $B/b2_ohne_modus.txt

{ echo "# TB-102 B3 - zweimal im selben Modus (Laeufe 2 und 3; Lauf 1 = B1)"
  for i in 2 3; do echo "## Lauf $i"; grep -E '^#|^rc=|FileNotFoundError|Ergebnis' "$SC/b3_kopf_$i.txt" | sort -u; done
  echo
  echo "Ergebnis: dreimal derselbe Abbruch an derselben Stelle (messgroessen.py:209 <- :329),"
  echo "keine Ausgabedatei. 'Zweimal bytegleich' ist im Modus nicht pruefbar."
  echo "Zum Vergleich Z2 (Hilfsbaum) zweimal: $(grep -E '^[0-9a-f]{64}' "$SC/z2_kopf.txt" | cut -c1-64) / $(grep -E '^[0-9a-f]{64}' "$SC/z2b_kopf.txt" | cut -c1-64)"
} | K > $B/b3_zweimal.txt

{ echo "# TB-102 b_hashes - vorher/nachher (hashes.sh), diff ohne Kopfzeile:"
  diff <(tail -n +2 $B/b_hashes_vorher.txt) <(tail -n +2 $B/b_hashes_nachher.txt) && echo "KEIN UNTERSCHIED"
  echo "Einzeldateien: b_hashes_vorher.txt, b_hashes_nachher.txt"
  echo; echo "# Sonde vorher/nachher (d1_sonde_*.txt), diff ohne Kopfzeile:"
  diff <(tail -n +2 $B/d1_sonde_vorher.txt) <(tail -n +2 $B/d1_sonde_nachher.txt) && echo "KEIN UNTERSCHIED"
} > $B/b_hashes.txt

{ echo "# TB-102 A7 - Lesequellen von messgroessen.py, EIN Lauf ohne Modus (= B2), Lesehaken TB-98"
  echo "# Spalten: Modus <TAB> Pfad <TAB> Aufrufstapel (innen zuerst). Rohprotokoll nur im Scratchpad."
  echo "# Alle Oeffnungen ausser Python/Pakete und ausser data/*.csv im Wortlaut:"
  grep -hv '^#' "$SC"/b2_ohne/prot/*.tsv | grep -v '/lib/python\|/trading-env/\|com.apple.python' | grep -v "^[^	]*	$PWD/data/"
  echo "# ... dazu $(cut -f2 "$SC"/b2_ohne/prot/*.tsv | grep -c "^$PWD/data/") Oeffnungen von $(cut -f2 "$SC"/b2_ohne/prot/*.tsv | grep "^$PWD/data/" | sort -u | wc -l | tr -d ' ') verschiedenen data/*.csv, alle von messgroessen.py:100"
  echo; cat "$SC/b2_quellen.txt" | awk '/Nicht-Code/{exit} {print}'
  echo "# 'anderswo' = SystemVersion.plist, /dev/urandom, zoneinfo/UTC (alle beim Import von pandas, Z. 48) und die Ausgabedatei im Scratchpad."
  echo "# Grenze des Hakens: os.path.exists (Z. 98) ist kein 'open'-Ereignis. Welche Symbole FEHLEN, sieht der Haken nicht - nur, welche gelesen wurden."
} | K > $B/a7_lesequellen.txt

{ echo "# TB-102 C - Stoerprobe im Speicher (c_lauf.sh / c_stoerprobe.py)"; cat "$SC/c2/ausgabe.txt"
  echo; echo "## Lesequellen der Stoerprobe (faltenplan() + rd.raster), ohne Python/Pakete"
  sed -n '/Herkunft/,/Nicht-Code/p' "$SC/c2_quellen.txt"
  grep -hv '^#' "$SC"/c2/prot/*.tsv | grep -v '/lib/python\|/trading-env/\|com.apple.python' \
     | grep -E 'tb24_haltedauern|ergebnisse/|manuelle_eingriffe' | cut -f1,2 | sort | uniq -c
} | K > $B/c_stoerprobe_lauf.txt
echo fertig; ls $B

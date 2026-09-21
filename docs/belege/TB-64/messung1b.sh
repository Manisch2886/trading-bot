#!/bin/bash
# TB-64, Schritt 1 - zweite, unabhaengige Zaehlung mit grep (kein sort -u,
# Muster ohne schliessenden Balken). Rein lesend.
cd "$(dirname "$0")/../../.." || exit 2
PF=docs/projektfuehrung
Z="$PF/BACKLOG.md $PF/BACKLOG_ARCHIV.md"
echo "Stand: $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M %z')"
echo "K-Zeilen im Ziel: $(cat $Z | grep -cE '^\| \*\*K[0-9][a-z]\*\*')  verschieden: $(cat $Z | grep -oE '^\| \*\*K[0-9][a-z]\*\*' | sort | uniq | wc -l | tr -d ' ')  doppelt: $(cat $Z | grep -oE '^\| \*\*K[0-9][a-z]\*\*' | sort | uniq -d | tr '\n' ' ')"
echo "Bloecke im Ziel:  $(cat $Z | grep -cE '^## 2[a-z]+\b')  doppelt: $(cat $Z | grep -oE '^## 2[a-z]+\b' | sort | uniq -d | tr '\n' ' ')"
echo "Quellenzeilen im Journal: $(grep -c '^\*Quelle:' $PF/JOURNAL.md)"
echo
printf "%-48s %6s %6s %6s %6s\n" Nachtrag K-Nr K-Ziel Bloecke Bl-Ziel
for f in $PF/nachtraege/BACKLOG_NACHTRAG_*.md; do
  n=$(basename "$f")
  ks=$(grep -oE '^\| \*\*K[0-9][a-z]\*\*' "$f" | sed 's/[|* ]//g')
  kz=0; for k in $ks; do c=$(cat $Z | grep -cE "^\| \*\*$k\*\*"); [ "$c" -gt 0 ] && kz=$((kz+1)); done
  bs=$(grep -oE '^#{2,3} 2[a-z]+\b' "$f" | sed -E 's/^#+ //')
  bz=0; for b in $bs; do c=$(cat $Z | grep -cE "^## $b\b"); [ "$c" -gt 0 ] && bz=$((bz+1)); done
  printf "%-48s %6s %6s %6s %6s\n" "$n" "$(echo $ks | wc -w | tr -d ' ')" "$kz" "$(echo $bs | wc -w | tr -d ' ')" "$bz"
done
echo
echo "Journal-Nachtraege (Dateiname in einer *Quelle:-Zeile):"
for f in $PF/nachtraege/JOURNAL_NACHTRAG_*.md $PF/nachtraege/_eingearbeitet/JOURNAL_NACHTRAG_*.md; do
  n=$(basename "$f"); printf "  %-36s %s\n" "$n" "$(grep -c "^\*Quelle:.*$n" $PF/JOURNAL.md)"
done
echo
echo "Handpruefung der vier Nachtraege ohne Nummer der drei Formen:"
echo "  (u)  T46.1a-d als Zeilen im Ziel: $(for t in T46.1a T46.1b T46.1c T46.1d; do cat $Z | grep -cE "^\| \*\*$t\*\*"; done | tr '\n' ' ')"
echo "  (q)  KG0-KG9 als Ueberschrift im Ziel: $(for i in 0 1 2 3 4 5 6 7 8 9; do cat $Z | grep -cE "^### KG$i — "; done | tr '\n' ' ') ; KG-F0..F12 als Zeilen: $(for i in 0 1 2 3 4 5 6 7 8 9 10 11 12; do cat $Z | grep -cE "^\| \*\*KG-F$i\*\*"; done | tr '\n' ' ')"
echo "  (r)  RT0-RT9 als Ueberschrift im Ziel: $(for i in 0 1 2 3 4 5 6 7 8 9; do cat $Z | grep -cE "^### RT$i — "; done | tr '\n' ' ') ; RT-F0..F11 als Zeilen: $(for i in 0 1 2 3 4 5 6 7 8 9 10 11; do cat $Z | grep -cE "^\| \*\*RT-F$i\*\*"; done | tr '\n' ' ')"
echo "  (q_r_berichtigung)  Zeilen im Ziel, die die Datei nennen: $(cat $Z | grep -c 'BACKLOG_NACHTRAG_2026-09-19q_r_berichtigung.md') ; davon 'Punkt 1..5': $(for i in 1 2 3 4 5; do cat $Z | grep -c "q_r_berichtigung.md\`, Punkt $i)"; done | tr '\n' ' ') ; Punkt 5 als K3e: $(cat $Z | grep -cE '^\| \*\*K3e\*\* \*\(aus der Berichtigung zu \(q\) und \(r\)')"
echo "  (q)  Vermerk zum Praefix KG-F (TB-59): $(grep -c 'Vermerk TB-59: die erste Spalte trägt das Präfix `KG-`' $PF/BACKLOG.md) ; (r) Praefix RT-F: $(grep -c 'Vermerk TB-59: die erste Spalte trägt das Präfix `RT-`' $PF/BACKLOG.md)"

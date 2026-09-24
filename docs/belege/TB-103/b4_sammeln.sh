#!/bin/bash
# TB-103 B4 - traegt die Testlaeufe (Scratchpad) in b4_tests.txt zusammen.
# Aufruf aus der Repo-Wurzel:  bash docs/belege/TB-103/b4_sammeln.sh <scratch>
SC="$1"
K() { sed "s#$SC#<scratch>#g; s#$PWD#<repo>#g; s#/var/folders/[^ ]*/T/#<tmp>/#g"; }
{
echo "# TB-103 B4 - die Testlandschaft nach dem Fix (Arbeitsbaum mit paths.py + Tests, vor Commit 2)"
echo "# und dieselben Tests im lokalen Klon 1d2b836 (vor dem Fix) als Vergleich."
echo
printf '%-26s %-22s %-22s\n' "Test" "vor dem Fix (1d2b836)" "nach dem Fix"
for t in test_paths test_startpruefungen test_strategy_paths test_stille_ausfaelle; do
  printf '%-26s %-22s %-22s\n' "$t" "$(grep -E 'bestanden' $SC/basis_$t.txt | tail -1 | grep -oE '[0-9]+ von [0-9]+')" "$(grep -E 'bestanden' $SC/b4_$t.txt | tail -1 | grep -oE '[0-9]+ von [0-9]+')"
done
printf '%-26s %-22s %-22s\n' "test_vorregistrierung" "188/188 (TB-97, Register)" "$(grep -E 'Pruefungen bestanden|GESCHEITERT' $SC/b4_test_vorregistrierung.txt | tail -1)"
echo
echo "## Namen - was neu ist, was umgeschrieben ist (Fable 24b B2: Namen, nicht die Zahl)"
echo "test_paths.py            NEU: G1, G2, G3, G3b, G4, G5, G6 (Proben), G7, G8, G9, G10 (Mutationsproben M1-M4)"
echo "                         UMGESCHRIEBEN: B2 ('CONFIG_DIR zeigt in den Snapshot' -> '... in den Snapshot-Unterordner config/')"
echo "                         ANGEPASST (Aufrufumgebung, nicht Prueflogik): baue_attrappe (config/ + MANIFEST-Eintraege),"
echo "                         baue_baum (Kopie der echten symbols_config.py + abfrage_symbole.py), frage(abfrage=...)"
echo "test_startpruefungen.py  NEU: keine. UMGESCHRIEBEN: keine. ANGEPASST: baue_attrappe (config/ + MANIFEST-Eintraege)"
echo "test_strategy_paths.py   UMGESCHRIEBEN: B2 (-> '... in den Snapshot-Unterordner config/'). ANGEPASST: baue_attrappe"
echo "                         (Freigabe des Betreibers 24.09.2026 23:49, in dieser Sitzung eingeholt)"
echo "test_stille_ausfaelle.py unveraendert"
echo "Keine Probe entfernt, keine abgeschwaecht; 0 x 'NICHT PRUEFBAR' in allen Laeufen: $(cat $SC/b4_test_*.txt | grep -c 'NICHT PRUEFBAR')"
echo
echo "## Kreuzprobe 1: NEUE paths.py gegen die ALTEN Tests (Klon 1d2b836) - warum die Attrappen angepasst werden mussten"
for t in test_paths test_startpruefungen test_strategy_paths test_stille_ausfaelle; do
  echo "--- $t: $(grep -E 'bestanden' $SC/kreuz_neupaths_alttests_$t.txt | tail -1)"
  grep "\[FEHLER\]" $SC/kreuz_neupaths_alttests_$t.txt | cut -c1-140
done
echo
echo "## Kreuzprobe 2: ALTE paths.py gegen die NEUEN Tests - die neuen Proben sehen den Fehler"
for t in test_paths test_startpruefungen test_strategy_paths; do
  echo "--- $t: $(grep -E 'bestanden' $SC/kreuz_altpaths_neutests_$t.txt | tail -1)"
  grep "\[FEHLER\]" $SC/kreuz_altpaths_neutests_$t.txt | cut -c1-140
done
echo
echo "## Volle Ausgaben"
for t in test_paths test_startpruefungen test_strategy_paths test_stille_ausfaelle test_vorregistrierung; do
  echo "=================== $t"; cat $SC/b4_$t.txt
done
} | K > docs/belege/TB-103/b4_tests.txt

#!/bin/bash
# TB-116 Block A: Suchmuster ueber das ganze Register, Treffer mit Zeilennummer.
# Muster 1-8 aus dem Auftrag, 9-18 von der Sitzung ergaenzt. Rein lesend.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-116/a_fundstellen.sh
R=docs/VORREGISTRIERUNG_neuselektion.md
echo "# TB-116 a_fundstellen, HEAD $(git rev-parse --short HEAD), Register $(wc -l < $R | tr -d ' ') Zeilen, sha256 $(shasum -a 256 $R | cut -c1-16)"
echo "# grep -n -F (feste Zeichenkette); Zeilen auf 240 Zeichen gekuerzt. Abschnitt 16.4 = Z. 1925-2046."
for p in '16.4' 'Registertext 6' 'Zellenbudget' 'Stufenfaktor' 'm_b' 'Klassenschlüssel' '80/20' 'Leiter' \
         'Benchmark-Position' 'mittleren Exposure' 'Budgetanteil' 'Budgetstufe' 'Grundbudget' 'Zellenanteil' \
         'Stufentabelle' '3⁹' 'Netting' 'Crash-Knopf'; do
  n=$(grep -c -F -- "$p" $R)
  echo; echo "== Muster '$p': $n Zeilen"
  grep -n -F -- "$p" $R | cut -c1-240
done

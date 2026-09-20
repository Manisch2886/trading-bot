#!/bin/bash
# TB-72 Nachweis 8: test_vorregistrierung.py (1) im Repo, (2) in einer Wegwerf-Kopie
# zwei Ebenen unter der Repo-Wurzel mit benchmark_drawdowns_tb72.json an der Stelle
# der gesperrten Tabelle (Muster TB-61/TB-66). Kopie wird danach entfernt.
cd "$(dirname "$0")/../../.."
B=docs/belege/TB-72
echo "== (1) im Repo"; date
trading-env/bin/python3 research/vorregistrierung/test_vorregistrierung.py > $B/nachweis8_test_im_repo.txt 2>&1; echo "rc=$?" >> $B/nachweis8_test_im_repo.txt
tail -3 $B/nachweis8_test_im_repo.txt
echo "== (2) in der Wegwerf-Kopie research/_tb72_kopie/"; date
rm -rf research/_tb72_kopie
cp -R research/vorregistrierung research/_tb72_kopie
rm -rf research/_tb72_kopie/__pycache__
cp research/vorregistrierung/ergebnisse/benchmark_drawdowns_tb72.json research/_tb72_kopie/ergebnisse/benchmark_drawdowns.json
shasum -a 256 research/_tb72_kopie/ergebnisse/benchmark_drawdowns.json research/vorregistrierung/ergebnisse/benchmark_drawdowns.json
trading-env/bin/python3 research/_tb72_kopie/test_vorregistrierung.py > $B/nachweis8_test_in_kopie_mit_tb72_tabelle.txt 2>&1; echo "rc=$?" >> $B/nachweis8_test_in_kopie_mit_tb72_tabelle.txt
tail -6 $B/nachweis8_test_in_kopie_mit_tb72_tabelle.txt
rm -rf research/_tb72_kopie
echo "== Kopie entfernt:"; ls research/_tb72_kopie 2>&1; date

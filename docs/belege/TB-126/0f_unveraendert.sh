#!/bin/bash
# TB-126 0f - die zwoelf Code-Dateien aus "Belegt" seit 0034960 unveraendert; auswertung.py seit 852f253.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-126/0f_unveraendert.sh
V=research/vorregistrierung
echo "# TB-126 0f, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## git diff --name-only 0034960 HEAD -- <12 Dateien> (Soll leer)"
git diff --name-only 0034960 HEAD -- $V/auswertung.py $V/kennzahlen.py $V/registerdaten.py $V/messgroessen.py \
  $V/registerbericht.py $V/pruefe_grenzsaetze.py research/mtm_drawdown/mtm_kern.py research/faltenplan_neun/embargo_neun.py \
  research/registernachtrag_tb48/pruefe_abschnitt17.py shared/snapshot.py research/exposure_messung/auswertung.py \
  research/exposure_messung/exposure_kern.py
echo "[Ende diff]"
echo "## git diff --name-only HEAD -- <12 Dateien> (Arbeitsbaum, Soll leer)"
git diff --name-only HEAD -- $V/*.py research/mtm_drawdown research/faltenplan_neun research/registernachtrag_tb48 shared/snapshot.py research/exposure_messung
echo "[Ende diff]"
echo "## git log --oneline 852f253..HEAD -- $V/auswertung.py (Soll leer)"
git log --oneline 852f253..HEAD -- $V/auswertung.py
echo "[Ende log]"
echo "## md5 auswertung.py (Soll 4f4b455e2d33aa46b309bbd2ff3bba33)"
md5 -r $V/auswertung.py

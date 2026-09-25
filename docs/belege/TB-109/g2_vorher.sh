#!/bin/bash
# TB-109 0b: die 8 Ausgaben ohne Modus VOR jeder Code-Aenderung. Aufruf aus der Repo-Wurzel:
#   bash docs/belege/TB-109/g2_vorher.sh <scratch>
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT
bash docs/belege/TB-109/g2_ausgaben.sh "$1/g2_vorher"

#!/bin/bash
# TB-140 V3 - Suchlaeufe zu R78 (e), ueber suche.py (nur verfolgte Dateien, nur lesen).
# Nr. 1: die eine Datei docs/VORREGISTRIERUNG_neuselektion.md; Nr. 2: die eine Datei auswertung.py.
# Dazu eine Werkzeugprobe (kein Code des Repos): was pandas.isna in der Umgebung als fehlend meldet.
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-140/v3_suche.sh
set -u
PY="${PY:-trading-env/bin/python3}"; S=docs/belege/TB-140/suche.py
R="--pfad docs/VORREGISTRIERUNG_neuselektion.md --endung .md"
A="--pfad research/vorregistrierung/auswertung.py"
RC=0
lauf() { "$PY" -B "$S" "$@"; local r=$?; echo "rc $r"; [ $r -ne 0 ] && RC=2; }
echo "## V3 Nr. 1 - Register: Dateien und Felder (Zaehlung)"
lauf --name V3-1a $R --nur-zaehlen --muster zellen.csv --muster zellenbericht --muster zelle_id --muster n_trades --muster netto_sharpe --muster netto_rendite_pct --muster kapital_drawdown_pct --muster kapital_drawdown_mtm_pct --muster kapital_drawdown_ereignis_pct --muster mittlere_exposure --muster haltedauer_median_handelstage --muster bestaetigung_ab_effektiv --muster Ertragsanteil --muster "nicht definiert" --muster endlich
echo "## V3 Nr. 1 - Register: Felder und Faelle ohne Zahl (Text, je Treffer hoechstens 300 Zeichen)"
lauf --name V3-1b $R --muster n_trades --muster netto_sharpe --muster netto_rendite_pct --muster kapital_drawdown_pct --muster kapital_drawdown_mtm_pct --muster kapital_drawdown_ereignis_pct --muster mittlere_exposure --muster haltedauer_median_handelstage --muster bestaetigung_ab_effektiv --muster Ertragsanteil --muster "nicht definiert" --muster endlich --muster "Standardabweichung 0" --muster "Formel für den Falten-Sharpe" --muster "Blocklänge L = max"
echo "## V3 Nr. 2 - auswertung.py: Pruefungen auf nicht endliche Werte"
lauf --name V3-2a $A --muster isfinite --muster isinf --muster finite --muster isna --muster notna --muster fillna --muster dropna --muster 'np.inf' --muster zellenbericht
echo "## V3 Nr. 2 - auswertung.py: Pflichtspalten, Leser der Spalten, Abbruch und Rueckgabewert"
lauf --name V3-2b $A --muster PFLICHTSPALTEN --muster 'def lies_zellen' --muster '"n_trades"' --muster '"netto_sharpe"' --muster '"netto_rendite_pct"' --muster '"kapital_drawdown_pct"' --muster '"mittlere_exposure"' --muster 'class Abbruch' --muster 'raise Abbruch' --muster RUECKGABEWERT_STARTPRUEFUNG --muster 'except'
lauf --name V3-2c --pfad shared/paths.py --muster 'RUECKGABEWERT_STARTPRUEFUNG ='
echo "## Werkzeugprobe: pandas.isna an NaN, +inf, -inf, 1.0 (Umgebung $PY; kein Code des Repos)"
"$PY" -B -c "import numpy as np, pandas as pd; print('pandas', pd.__version__, 'isna', pd.Series([np.nan, np.inf, -np.inf, 1.0]).isna().tolist())"; echo "rc $?"
echo "## Ende"
exit $RC

#!/bin/bash
# TB-108 A3: die Stand-Angaben der Stoffsammlung am Repo nachgemessen (nur lesend).
# Aufruf aus der Repo-Wurzel: bash docs/belege/TB-108/a3_stand.sh
V=research/vorregistrierung; E=$V/ergebnisse
echo "# TB-108 A3, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "## (1) Commits der Stoffsammlung"
for c in 836865f 516badc f334a7b d96b352 2e21471 f22f91e e1e6652 5791b4c f61bd97 f5fdb53 5cfe472 a79e715 9827a3e 069370d 0292e92; do
  git log -1 --format="%h %ad %s" --date=format:'%d.%m.%Y %H:%M' $c | cut -c1-120; done
echo "## (2) Abbilder, Benchmark-Tabelle, gesperrte Ergebnisdateien"
shasum -a 256 $E/sperrliste_abbild_*.json $E/benchmark_drawdowns_2026-09-23_nach_wegA.json $E/faltenplan.json $E/messgroessen.json $E/benchmark_drawdowns.json
echo "   herkunft_protokoll.jsonl: $(ls $E/herkunft_protokoll.jsonl 2>&1)"
echo "## (3) Laufbereich TB-107"
f=docs/belege/TB-107/f1_laufbereich_vereinigung.txt; echo "   $f: $(grep -vc '^#' $f) Nicht-Kommentarzeilen; regimewache: $(grep -c 'shared/regimewache.py' $f)"
grep -v '^#' $f | grep -c '^docs/' | sed 's/^/   davon unter docs\/: /'
echo "## (4) herkunft.py: daten_dir, makedirs, TB30A_BASE_DIR"
shasum -a 256 $V/herkunft.py; git log -1 --format='   letzter Commit %h %s' -- $V/herkunft.py | cut -c1-120
grep -n "def block\|def anhaengen\|def datenstand\|makedirs\|TB30A_BASE_DIR" $V/herkunft.py
echo "## (5) shared/paths.py: ARBEITSBAUM_PFADE, CONFIG_UNTERORDNER, selektionsmodus"
grep -n "^ARBEITSBAUM_PFADE\|ARBEITSBAUM_PFADE =\|^CONFIG_UNTERORDNER\|def selektionsmodus" shared/paths.py
echo "## (6) shared/strategy_paths.py: getattr auf paths"
grep -n "getattr(paths\|selektionsmodus()" shared/strategy_paths.py
echo "## (7) Ladeprotokoll: nennt es Zeilenzahl der Universumsdatei und Quelle (25a (B) (4))?"
ls shared/ladeprotokoll.py 2>&1; grep -n "zeilen\|Quelle\|quelle\|Keines ausgelassen" shared/ladeprotokoll.py | head -20
git log -1 --format='   letzter Commit %h %ad %s' --date=short -- shared/ladeprotokoll.py | cut -c1-120
echo "## (8) regimewache.pruefe_einbau()"
trading-env/bin/python3 -W ignore -c "import sys; sys.path.insert(0,'shared'); import regimewache as r; print('  ', r.pruefe_einbau())" 2>&1 | tail -3
echo "## (9) MIN_HISTORY_* je Bot (G9)"
for d in strategies/*/; do printf '   %-28s' $(basename $d); grep -l "MIN_HISTORY_\(HOURS\|DAYS\)\s*=" $d*.py 2>/dev/null | while read x; do printf '%s ' "$(basename $x):$(grep -c 'MIN_HISTORY_\(HOURS\|DAYS\)\s*=' $x):$(grep -o 'MIN_HISTORY_\(HOURS\|DAYS\)' $x | sort -u | tr '\n' ,)"; done; echo; done
echo "## (10) registerdaten.py: MINDESTTRAINING_JAHRE und Bedingungsdeutung (Z. 605)"
grep -n "MINDESTTRAINING_JAHRE" $V/*.py research/faltenplan_neun/*.py research/universum_trockenlauf/*.py | grep -v "/test_" 
sed -n 600,610p $V/registerdaten.py
echo "## (11) test_vorregistrierung: FELDLISTE_PLAN / FELDLISTE_FALTE"
grep -n "^FELDLISTE_PLAN\|^FELDLISTE_FALTE" $V/test_vorregistrierung.py
echo "## (12) Ersatzmodule fuer strategy_paths (G3)"
grep -n "sys.modules\[.strategy_paths.\]" shared/kurven_lauf.py shared/determinismus_lauf.py research/zuteilungskaskade/messung_primaerschluessel.py
echo "## (13) manual_close.py: Schreiben erst bei erster Zeile (D11)"
grep -n "manuelle_eingriffe\|makedirs\|open(" notifications/manual_close.py | head
echo "## (14) auswertung.Abbruch: Rueckgabewert (G5)"
grep -n "class Abbruch\|except Abbruch\|SystemExit(1)\|sys.exit(1)\|raise SystemExit" $V/auswertung.py | head
echo "## (15) TB-92 Lesehaken-Belege (C9/D10)"
ls -l docs/belege/TB-92/a1b_lesehaken.py docs/belege/TB-92/a1b_lesequellen_kinder.txt 2>&1 | awk '{print "  ",$5,$9}'
git log --diff-filter=A --format='   hinzugefuegt %h %ad' --date=format:'%d.%m.%Y %H:%M' -- docs/belege/TB-92/a1b_lesehaken.py docs/belege/TB-92/a1b_lesequellen_kinder.txt
head -5 docs/belege/TB-92/a1b_lesequellen_kinder.txt
echo "## (16) bot_lauf.py Kopf zu symbol (A8)"
f=$(git ls-files | grep 'bot_lauf.py$' | head -3); echo "   $f"; for x in $f; do grep -n -i "etikett\|symbol.*kein\|reines" $x | head -5; done
echo "## (17) 5.4 Wortlaut 'gefundene' (B1)"
awk '/^### 5.4 /,/^## 6\./' docs/VORREGISTRIERUNG_neuselektion.md | grep -n "gefunden" 
echo "## (18) Registerabschnitt 19: ARBEITSBAUM_PFADE-Zeile (E2)"
grep -n "ARBEITSBAUM_PFADE" docs/VORREGISTRIERUNG_neuselektion.md | cut -c1-160
echo "## (19) test_vorregistrierung: Zahl der Pruefungen am letzten Lauf (TB-107 G4)"
grep -n "test_vorregistrierung" docs/belege/TB-107/g4_tests.txt | head -3
echo "## (20) pfadvergleich.py rc (TB-107, nicht erneut ausgefuehrt)"
grep -n "rc" docs/belege/TB-107/d_pfadvergleich.txt | head -3
echo "## (21) faltenplan.py: Verfahren-A-Felder im gerechneten Plan"
grep -c "purge_tage\|embargo_tage\|training_bis_ausschliesslich\|embargo_nach_falten\|mindesttraining_jahre" $V/faltenplan.py
grep -n "purge_tage\|embargo_tage\|training_bis_ausschliesslich\|embargo_nach_falten\|mindesttraining_jahre" $V/faltenplan.py | head
echo "## Ende"

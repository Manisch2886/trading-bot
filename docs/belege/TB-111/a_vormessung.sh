#!/bin/bash
# TB-111 Block A - Vormessung (nur lesen). Aufruf aus der Worktree-Wurzel:
#   bash docs/belege/TB-111/a_vormessung.sh
PY=/Users/jaquelineloffler/trading-bot/trading-env/bin/python3
SNAP=63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
V=research/vorregistrierung
MODUS=(TB_SELEKTIONSWURZEL="$PWD/snapshots/$SNAP" TB_SELEKTIONSHASH="$SNAP" TB_SELEKTIONSCOMMIT="$(git --no-optional-locks rev-parse HEAD)")
echo "# TB-111 A, Wurzel $PWD, HEAD $(git --no-optional-locks rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "== A1 main(): Aufrufe von block( in herkunft.py"
grep -n "block(" $V/herkunft.py
echo "== A1 Laeufe der Pruefansicht (Protokoll existiert nicht; kein Schreiben ohne --anhaengen)"
for a in "" "--json" "--pruefen"; do
  env -u TB30A_BASE_DIR $PY -W ignore $V/herkunft.py $a > /dev/null 2>&1; r0=$?
  env -u TB30A_BASE_DIR "${MODUS[@]}" $PY -W ignore $V/herkunft.py $a > /dev/null 2>"$TMPDIR/tb111_a1.err"; r1=$?
  echo "   herkunft.py ${a:-(ohne Argument)}: ohne Modus rc $r0 | Modus rc $r1 | ABBRUCH-Zeile: $(grep ABBRUCH "$TMPDIR/tb111_a1.err" | cut -c1-170)"
done
rm -f "$TMPDIR/tb111_a1.err"
echo "== A2 Setzer von TB30A_BASE_DIR ausserhalb docs/ (git grep)"
git --no-optional-locks grep -n "TB30A_BASE_DIR\"\] = \|TB30A_BASE_DIR=\|pop(\"TB30A_BASE_DIR\|\"TB30A_BASE_DIR\", \"TB36" -- ':!docs' | cut -c1-170
echo "== A2 je Setzer: TB_SELEKTIONS in derselben Umgebung? (+-25 Zeilen)"
for s in research/vorregistrierung/test_vorregistrierung.py:810 research/vorregistrierung/test_ersatzwerte.py:73 \
         research/faltenplan_neun/test_erste_falte_trockenlauf.py:173; do
  f=${s%%:*}; z=${s##*:}
  n=$(sed -n "$((z-25)),$((z+25))p" "$f" | grep -c "TB_SELEKTIONS")
  echo "   $s  TB_SELEKTIONS im Fenster: $n"
done
echo "   test_vorregistrierung.py:810 _umgebung(): u = dict(os.environ) + TB30A -> Modus nur, wenn der Testprozess selbst ihn traegt"
echo "   test_ersatzwerte.py:73 _umgebung(): entfernt TB_SELEKTIONS*, setzt TB30A"
echo "   test_ersatzwerte.py:393, test_vorregistrierung.py:1113/1221, test_faltenplan_neun.py:775, test_universum_trockenlauf.py:1405: entfernen TB30A, bevor sie den Modus setzen"
echo "== A2 Wer ruft in einem Prozess mit TB30A herkunft auf? (import/Laden von herkunft)"
git --no-optional-locks grep -n "import herkunft\|lade_fremdes_modul(\s*$\|\"herkunft\", os.path\|lade_herkunft()" -- ':!docs' '*.py' | cut -c1-150
echo "== A3 raise Abbruch( in auswertung.py"
grep -c "raise Abbruch(" $V/auswertung.py
echo "== A3 Tests: Rueckgabewert 1 oder Abbruch mit Code"
grep -n "returncode == 1\|rc\"\] == 1\|Abbruch\b\|except SystemExit" $V/test_vorregistrierung.py $V/test_ersatzwerte.py $V/beispieldaten.py | grep -v Abbruchkrit
echo "   test_vorregistrierung.py:962 (H5) gilt pruefe_grenzsaetze.py, nicht auswertung.py"
echo "== A4 Import von herkunft.py unter dem Modus, ohne TB30A_BASE_DIR"
env -u TB30A_BASE_DIR "${MODUS[@]}" $PY -W ignore -c "
import sys; sys.path.insert(0, '$V'); import herkunft as h
print('   import ok; paths geladen:', 'paths' in sys.modules, '| BASE_DIR', h.BASE_DIR)
print('   datenstand(Snapshot):', h.datenstand('snapshots/$SNAP'))
print('   paths nach datenstand geladen:', 'paths' in sys.modules)"
echo "   rc=$?"
echo "== A4 dasselbe ueber die beiden Nutzer (datenstand.py per lade_fremdes_modul, snapshot.lade_herkunft)"
env -u TB30A_BASE_DIR "${MODUS[@]}" $PY -W ignore -c "
import sys; sys.path.insert(0, 'shared'); import snapshot as s
h = s.lade_herkunft(); print('   snapshot.lade_herkunft ok:', h.datenstand('snapshots/$SNAP')['datenstand'][:16])"
echo "   rc=$?"
env -u TB30A_BASE_DIR "${MODUS[@]}" $PY -W ignore -c "
import sys; sys.path.insert(0, 'research/etf_trendfolge'); import datenstand as d
print('   etf datenstand.py import ok')"
echo "   rc=$?"
echo "## Ende"
echo "== A2b heute: Modus + TB30A_BASE_DIR=/gibt/es/nicht, Pruefansicht (liest nur; --anhaengen wird hier NIE gerufen)"
env "${MODUS[@]}" TB30A_BASE_DIR=/gibt/es/nicht $PY -W ignore $V/herkunft.py > /dev/null 2>"$TMPDIR/tb111_a2b.err"; echo "   rc $?"
grep -v "^\[paths\]" "$TMPDIR/tb111_a2b.err" | tail -3 | cut -c1-200; rm -f "$TMPDIR/tb111_a2b.err"
echo "== A2b heute: dasselbe mit TB30A_BASE_DIR = Worktree-Wurzel"
env "${MODUS[@]}" TB30A_BASE_DIR="$PWD" $PY -W ignore $V/herkunft.py > /dev/null 2>"$TMPDIR/tb111_a2b.err"; echo "   rc $?"
grep -v "^\[paths\]" "$TMPDIR/tb111_a2b.err" | tail -3 | cut -c1-200; rm -f "$TMPDIR/tb111_a2b.err"
echo "== A2b _paths() laedt paths aus BASE_DIR/shared (herkunft.py), also unter einer Ersatzwurzel von dort"
grep -n "ordner = os.path.join(BASE_DIR, \"shared\")" $V/herkunft.py
echo "## Ende A2b"

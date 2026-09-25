"""TB-107 D Abnahme (Live-Code): shared/strategy_paths.py vorher (git show f5fdb53) gegen den
Arbeitsbaum, OHNE Modus. Je Fassung ein Wegwerfbaum in Projektform (echte paths.py), je Bot und je
Aufrufer (forward_test.py und jede andere Datei unter strategies/<bot>/, die get_strategy_paths
aufruft) ein eigener Prozess. Verglichen: das zurueckgegebene dict (Baumpfad neutralisiert) und die
Menge der danach im Baum vorhandenen Verzeichnisse. Schreibt nur in mkdtemp-Ordner, raeumt auf.
Aufruf aus der Repo-Wurzel: trading-env/bin/python3 docs/belege/TB-107/d_vergleich.py [<vorher-commit>]"""
import json, os, shutil, subprocess, sys, tempfile
REPO = os.getcwd()
VORHER = sys.argv[1] if len(sys.argv) > 1 else "f5fdb53"
alt = subprocess.run(["git", "show", VORHER + ":shared/strategy_paths.py"], capture_output=True, text=True, check=True).stdout
neu = open("shared/strategy_paths.py", encoding="utf-8").read()
aufrufer = sorted(subprocess.run(["git", "grep", "-l", "get_strategy_paths", "--", "strategies"],
                                 capture_output=True, text=True).stdout.split())
PROBE = r'''
import json, os, sys
caller = sys.argv[1]
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(caller)))), "shared"))
from strategy_paths import get_strategy_paths
print(json.dumps(get_strategy_paths(caller), sort_keys=True))
'''
def lauf(quelle):
    ergebnis = {}
    for datei in aufrufer:
        baum = tempfile.mkdtemp(prefix="tb107_d_")
        try:
            os.makedirs(os.path.join(baum, "shared"))
            shutil.copy2("shared/paths.py", os.path.join(baum, "shared", "paths.py"))
            open(os.path.join(baum, "shared", "strategy_paths.py"), "w").write(quelle)
            os.makedirs(os.path.join(baum, os.path.dirname(datei)))
            u = {k: v for k, v in os.environ.items() if not k.startswith("TB_SELEKTIONS")}
            r = subprocess.run([sys.executable, "-c", PROBE, os.path.join(baum, datei)], capture_output=True, text=True, env=u)
            ordner = sorted(os.path.relpath(os.path.join(w, d), baum) for w, ds, _ in os.walk(baum) for d in ds if "__pycache__" not in d)
            ergebnis[datei] = {"rc": r.returncode, "pfade": r.stdout.replace(baum, "<WURZEL>").strip(), "ordner": ordner,
                               "fehler": r.stderr[-200:] if r.returncode else ""}
        finally:
            shutil.rmtree(baum)
    return ergebnis
a, n = lauf(alt), lauf(neu)
unterschiede = [d for d in aufrufer if a[d] != n[d]]
print("# TB-107 D Vergleich strategy_paths.py %s (vorher) gegen Arbeitsbaum, ohne Modus" % VORHER)
print("Aufrufer (Dateien unter strategies/ mit get_strategy_paths): %d, Bots: %d" % (len(aufrufer), len({d.split('/')[1] for d in aufrufer})))
print("rc != 0 vorher: %d, nachher: %d" % (sum(a[d]['rc'] != 0 for d in aufrufer), sum(n[d]['rc'] != 0 for d in aufrufer)))
print("Schluessel je Aufruf: %s" % sorted(json.loads(n[aufrufer[0]]['pfade'])))
print("Beispiel %s: Pfade %s; Ordner %s" % (aufrufer[0], n[aufrufer[0]]['pfade'], n[aufrufer[0]]['ordner']))
print("UNTERSCHIEDE (Pfade oder angelegte Ordner): %d %s" % (len(unterschiede), unterschiede))
sys.exit(1 if unterschiede else 0)

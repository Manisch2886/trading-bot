"""TB-92 A1b: fuehrt benchmark.py unveraendert aus und protokolliert jede
geoeffnete Datei (sys.addaudithook, Ereignis 'open'). Schreibt nur das
Protokoll (Pfad als erstes Argument) - benchmark.py selbst schreibt sein --ziel."""
import os, runpy, sys
protokoll, skript = sys.argv[1], sys.argv[2]
gesehen = []
def haken(ereignis, args):
    if ereignis == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
        gesehen.append((os.fsdecode(args[0]), str(args[1]) if len(args) > 1 else ""))
sys.addaudithook(haken)
sys.argv = [skript] + sys.argv[3:]
sys.path.insert(0, os.path.dirname(os.path.abspath(skript)))
try:
    runpy.run_path(skript, run_name="__main__")
except SystemExit as e:
    rc = e.code
else:
    rc = 0
with open(protokoll, "w", encoding="utf-8") as f:
    for p, m in gesehen:
        f.write(f"{m}\t{p}\n")
sys.exit(rc)

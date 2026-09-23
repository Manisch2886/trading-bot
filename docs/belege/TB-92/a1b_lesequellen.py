"""TB-92 A1b: ordnet das Protokoll des Lesehakens nach Herkunft (Verknuepfungen aufgeloest)."""
import collections, os, sys
repo = os.path.realpath(sys.argv[2]); snap = os.path.join(repo, "snapshots")
gruppen = collections.defaultdict(set)
for zeile in open(sys.argv[1], encoding="utf-8"):
    modus, pfad = zeile.rstrip("\n").split("\t", 1)
    echt = os.path.realpath(pfad)
    if echt.startswith(snap + os.sep):
        g = "snapshot/" + ("config" if "/config/" in echt else "csv")
    elif echt.startswith(os.path.join(repo, "data") + os.sep):
        g = "REPO data/  <- darf nicht vorkommen"
    elif echt.startswith(os.path.join(repo, "config") + os.sep):
        g = "REPO config/ <- darf nicht vorkommen"
    elif echt.startswith(os.path.join(repo, "trading-env") + os.sep) or "/lib/python" in echt:
        g = "Python/Pakete"
    elif echt.startswith(repo + os.sep):
        rel = os.path.relpath(echt, repo)
        g = "repo " + ("*.py" if rel.endswith((".py", ".pyc")) else rel)
    else:
        g = "sonst"
    gruppen[g].add(echt)
for g in sorted(gruppen):
    print(f"{len(gruppen[g]):5d}  {g}")

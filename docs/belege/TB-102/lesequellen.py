"""TB-102: ordnet das Protokoll des Lesehakens (TB-98 haken/sitecustomize.py)
nach Herkunft (Verknuepfungen aufgeloest) und nennt fuer jede Nicht-Code-Datei
den innersten Rahmen, der sie oeffnet.

Aufruf:  python3 lesequellen.py <scratch-lauf>/prot <repo> [<hilfsbaum>]
Herkunftsklassen: SNAPSHOT (snapshots/<hash>/), REPO data/, REPO config/,
REPO research/, REPO sonst, Python/Pakete, anderswo.
Angezeigt wird der angefragte Pfad UND - falls anders - der aufgeloeste.
"""
import collections
import os
import sys

prot, repo = sys.argv[1], os.path.realpath(sys.argv[2])
hilf = os.path.realpath(sys.argv[3]) if len(sys.argv) > 3 else None
snap = os.path.join(repo, "snapshots")


def klasse(echt):
    if echt.startswith(snap + os.sep):
        return "SNAPSHOT"
    if echt.startswith(os.path.join(repo, "trading-env") + os.sep) or "/lib/python" in echt \
            or "/Library/Caches/com.apple.python" in echt:
        return "Python/Pakete"
    for unter in ("data", "config", "research"):
        if echt.startswith(os.path.join(repo, unter) + os.sep):
            if unter == "research" and echt.endswith((".py", ".pyc")):
                return "REPO Code"
            return "REPO %s/" % unter
    if echt.startswith(repo + os.sep):
        return "REPO Code" if echt.endswith((".py", ".pyc")) else "REPO sonst"
    return "anderswo"


gruppen = collections.defaultdict(set)
wer_je = collections.defaultdict(collections.Counter)
argvs = []
for datei in sorted(os.listdir(prot)):
    for zeile in open(os.path.join(prot, datei), encoding="utf-8"):
        if zeile.startswith("#argv"):
            argvs.append(zeile.rstrip("\n"))
            continue
        teile = zeile.rstrip("\n").split("\t")
        pfad = teile[1]
        wer = teile[2].split(" < ")[0] if len(teile) > 2 and teile[2] else "(kein Python-Rahmen)"
        echt = os.path.realpath(pfad)
        k = klasse(echt)
        gruppen[k].add(echt)
        if k not in ("Python/Pakete", "REPO Code"):
            anzeige = os.path.relpath(pfad, repo) if os.path.isabs(pfad) else pfad
            if echt != os.path.abspath(pfad):
                anzeige += "  ->  " + (os.path.relpath(echt, repo) if echt.startswith(repo) else echt)
            wer_je[(k, anzeige)][os.path.relpath(wer, repo) if wer.startswith(repo) else wer] += 1

print("Prozesse: %d" % len(argvs))
for a in argvs:
    print("  " + a.replace(repo, "<repo>"))
print("\nDateien je Herkunft (verschieden, nach Aufloesung):")
for g in sorted(gruppen):
    print("  %5d  %s" % (len(gruppen[g]), g))
print("\nNicht-Code-Dateien mit oeffnendem Rahmen (Snapshot-CSV zusammengefasst):")
zusammen = collections.Counter()
for (k, anzeige), wer in sorted(wer_je.items()):
    ziel = anzeige.split("  ->  ")[-1]
    flach = k == "SNAPSHOT" and ziel.count("/") == 2
    if flach and ziel.endswith(".csv") and os.path.exists(os.path.join(repo, ziel)):
        for w, n in wer.items():
            zusammen[(k, w)] += n
        continue
    fehlt = "" if os.path.exists(os.path.join(repo, anzeige.split("  ->  ")[0])) else "   <- EXISTIERT NICHT (Oeffnungsversuch)"
    print("  [%s] %s%s" % (k, anzeige, fehlt))
    for w, n in sorted(wer.items()):
        print("        geoeffnet von %s (%d x)" % (w, n))
for (k, w), n in sorted(zusammen.items()):
    print("  [%s] Kurs-CSV (%d Oeffnungen) geoeffnet von %s" % (k, n, w))

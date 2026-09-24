"""TB-98 A1: ordnet die Protokolle des Lesehakens (haken/sitecustomize.py) je
Bot nach Herkunft (Verknuepfungen aufgeloest; Bauart TB-92 a1b_lesequellen.py)
und nennt fuer Kursdaten/Symbollisten den innersten Rahmen, der sie oeffnet.

Aufruf:  python3 a1_lesequellen.py <scratch>/a1n/modus <repo>
"""
import collections
import os
import sys

basis, repo = sys.argv[1], os.path.realpath(sys.argv[2])
snap = os.path.join(repo, "snapshots")
for bot in sorted(os.listdir(basis)):
    gruppen = collections.defaultdict(set)
    stapel = collections.Counter()
    prot = os.path.join(basis, bot, "prot")
    for datei in sorted(os.listdir(prot)):
        for zeile in open(os.path.join(prot, datei), encoding="utf-8"):
            if zeile.startswith("#"):
                continue
            teile = zeile.rstrip("\n").split("\t")
            modus, pfad = teile[0], teile[1]
            wer = teile[2].split(" < ")[0] if len(teile) > 2 else ""
            echt = os.path.realpath(pfad)
            daten = False
            if echt.startswith(snap + os.sep):
                g = "snapshot/" + ("config" if "/config/" in echt else
                                   ("MANIFEST" if echt.endswith("MANIFEST.json") else "csv"))
                daten = True
            elif echt.startswith(os.path.join(repo, "data") + os.sep):
                g = "REPO data/   <- darf unter dem Modus nicht vorkommen"
                daten = True
            elif echt.startswith(os.path.join(repo, "config") + os.sep):
                g = "REPO config/ <- darf unter dem Modus nicht vorkommen"
                daten = True
            elif echt.startswith(os.path.join(repo, "trading-env") + os.sep) or "/lib/python" in echt:
                g = "Python/Pakete"
            elif echt.startswith(repo + os.sep):
                rel = os.path.relpath(echt, repo)
                g = "repo " + ("*.py/*.pyc" if rel.endswith((".py", ".pyc")) else rel)
            else:
                g = "sonst"
            gruppen[g].add(echt)
            if daten:
                stapel[(g, os.path.relpath(wer, repo) if wer.startswith(repo) else wer)] += 1
    print("== %s" % bot)
    for g in sorted(gruppen):
        print("  %5d  %s" % (len(gruppen[g]), g))
    for (g, wer), n in sorted(stapel.items()):
        print("         %-22s geoeffnet von %s (%d x)" % (g.split()[0] + (" " + g.split()[1] if g.startswith("REPO") else ""), wer, n))

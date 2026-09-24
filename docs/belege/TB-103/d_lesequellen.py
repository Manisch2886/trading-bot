"""TB-103 D: ordnet das Protokoll des Lesehakens (TB-98 haken/sitecustomize.py)
je Bot nach Herkunft (Verknuepfungen aufgeloest). Bauart TB-102 lesequellen.py,
erweitert um: Code (.py/.pyc) GETRENNT von Daten gezaehlt, Schreib- und
Lesezugriffe getrennt, eigene Ausgaben im Scratchpad getrennt.

Aufruf:  python3 d_lesequellen.py <scratch>/<art> <repo> <scratch>
Ausgabe: je Bot eine Herkunftstabelle und JEDER Nicht-Code-Zugriff ausserhalb
des Snapshots mit Modus und Aufrufstapel.
"""
import collections
import os
import sys

wurzel_art, repo, scratch = sys.argv[1], os.path.realpath(sys.argv[2]), os.path.realpath(sys.argv[3])
SNAP = os.path.join(repo, "snapshots", "63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2")


def klasse(echt):
    if echt.endswith((".py", ".pyc")) or "/__pycache__/" in echt:
        return "Code"
    if echt.startswith(os.path.join(repo, "trading-env") + os.sep) or "/lib/python" in echt \
            or "site-packages" in echt or "/Library/Caches/com.apple.python" in echt:
        return "Python/Pakete"
    if echt.startswith(SNAP + os.sep):
        return "SNAPSHOT"
    if echt.startswith(scratch + os.sep):
        return "Scratchpad (eigene Ausgabe/Protokoll)"
    for unter in ("data", "config", "research", "results", "logs"):
        if echt.startswith(os.path.join(repo, unter) + os.sep):
            return "REPO %s/" % unter
    if echt.startswith(repo + os.sep):
        return "REPO sonst"
    return "anderswo"


def schreibend(modus):
    return any(z in modus for z in ("w", "a", "x", "+"))


gesamt = {}
for bot in sorted(os.listdir(wurzel_art)):
    prot = os.path.join(wurzel_art, bot, "prot")
    if not os.path.isdir(prot):
        continue
    dateien = collections.defaultdict(set)
    ausserhalb = collections.defaultdict(collections.Counter)
    prozesse = 0
    for name in sorted(os.listdir(prot)):
        for zeile in open(os.path.join(prot, name), encoding="utf-8"):
            if zeile.startswith("#argv"):
                prozesse += 1
                continue
            teile = zeile.rstrip("\n").split("\t")
            modus, pfad = teile[0], teile[1]
            stapel = teile[2] if len(teile) > 2 else ""
            echt = os.path.realpath(pfad)
            k = klasse(echt)
            art = "schreibend" if schreibend(modus) else "lesend"
            dateien[(k, art)].add(echt)
            if k not in ("Code", "Python/Pakete", "SNAPSHOT", "Scratchpad (eigene Ausgabe/Protokoll)"):
                anzeige = echt.replace(repo, "<repo>")
                ausserhalb[(k, art, anzeige)][stapel.replace(repo, "<repo>") or "(kein Python-Rahmen)"] += 1
    rc_datei = os.path.join(wurzel_art, bot, "rc")
    rc = open(rc_datei).read().strip() if os.path.exists(rc_datei) else "?"
    print("=" * 100)
    print("%s  rc=%s  Prozesse=%d" % (bot, rc, prozesse))
    for (k, art), menge in sorted(dateien.items()):
        print("  %5d  %-40s %s" % (len(menge), k, art))
    snap_csv = [p for p in dateien.get(("SNAPSHOT", "lesend"), ()) if p.endswith(".csv")]
    snap_cfg = [os.path.relpath(p, SNAP) for p in dateien.get(("SNAPSHOT", "lesend"), ())
                if os.sep + "config" + os.sep in p]
    print("  Snapshot: %d Kurs-CSV, Universumsdateien %s" % (len(snap_csv), snap_cfg or "keine"))
    daten_aussen = [(k, a, p) for (k, a, p) in ausserhalb]
    print("  Nicht-Code-Zugriffe ausserhalb des Snapshots: %d" % len(daten_aussen))
    for (k, a, p), wer in sorted(ausserhalb.items()):
        print("    [%s, %s] %s" % (k, a, p))
        for w, n in sorted(wer.items()):
            print("        %dx  %s" % (n, w))
    gesamt[bot] = (rc, len(snap_csv), snap_cfg, sorted(ausserhalb))

print("=" * 100)
print("UEBERSICHT  bot | rc | Snapshot-CSV | Universum aus Snapshot | Nicht-Code ausserhalb (Klasse, Art, Pfad)")
for bot, (rc, n_csv, cfg, aus) in sorted(gesamt.items()):
    print("  %-28s rc=%s  csv=%3d  cfg=%s  aussen=%d %s" % (
        bot, rc, n_csv, ",".join(sorted(cfg)) or "-", len(aus),
        "; ".join("%s/%s:%s" % (k, a, p) for k, a, p in aus)))

"""TB-104 A8 - Sperrlistenpruefung der freigegebenen Dateien (Bauart TB-103 a8). Rein lesend.
Aufruf aus der Repo-Wurzel: trading-env/bin/python3 docs/belege/TB-104/a8_sperrliste.py"""
import json, os, re, sys
from datetime import datetime
REG = "docs/VORREGISTRIERUNG_neuselektion.md"
ABBILD = "research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-23.json"
FREI = ["research/vorregistrierung/benchmark.py", "research/vorregistrierung/faltenplan.py",
        "research/faltenplan_neun/faltenplan_neun.py", "research/faltenplan_neun/erste_falte_trockenlauf.py",
        "research/universum_trockenlauf/universum_trockenlauf.py", "research/universum_trockenlauf/loaderlauf.py",
        "research/faltenplan_neun/test_erste_falte_trockenlauf.py", "research/faltenplan_neun/test_faltenplan_neun.py",
        "research/faltenplan_neun/test_horizontbeginn.py",
        "research/universum_trockenlauf/test_universum_trockenlauf.py",
        "research/vorregistrierung/test_vorregistrierung.py", "research/vorregistrierung/registerbericht.py"]
zeilen = open(REG, encoding="utf-8").read().splitlines()
start = next(i for i, z in enumerate(zeilen) if z.startswith("## 10"))
ende = next(i for i in range(start + 1, len(zeilen)) if zeilen[i].startswith("## "))
abschnitt = zeilen[start:ende]
sys.path.insert(0, "research/vorregistrierung")
import herkunft as h
abbild_text = open(ABBILD, encoding="utf-8").read()
abbild = json.loads(abbild_text)
print("# TB-104 A8 - Sperrlistenpruefung, %s, HEAD %s" % (
    datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z"),
    os.popen("git rev-parse --short HEAD").read().strip()))
print("Register Abschnitt 10: Z. %d-%d" % (start + 1, ende))
for d in FREI:
    name = os.path.basename(d)
    treffer = [(start + 1 + i, z.strip()[:110]) for i, z in enumerate(abschnitt) if name in z]
    print("== %s" % d)
    print("   Abschnitt 10, Treffer '%s': %d" % (name, len(treffer)))
    for nr, z in treffer:
        print("      Z. %d: %s" % (nr, z))
    for attr in ("SPERRLISTE_DATEIEN", "EINGEFROREN"):
        wert = getattr(h, attr, None)
        drin = None if wert is None else any(name in str(x) for x in wert)
        print("   herkunft.py::%s: %s" % (attr, drin))
    punkte = sorted({p.get("nummer", p.get("punkt")) for p in abbild.get("punkte", [])
                     if name in json.dumps(p, ensure_ascii=False)}, key=str)
    print("   Abbild %s, Treffer: %d%s" % (os.path.basename(ABBILD), abbild_text.count(name),
                                           (" (Punkte %s)" % punkte) if punkte else ""))

"""TB-102 Block C: Wohin fliesst `haltedauer` aus messgroessen.json?

NUR im Speicher. `faltenplan.py` wird importiert, `main()` wird NIE gerufen
(TB-83: main() ueberschriebe den gesperrten faltenplan.json). Es wird nichts
geschrieben; die Ausgabe geht auf stdout.

Proben (je auf einer tiefen Kopie der eingefrorenen messgroessen.json):
  P0  unveraendert                      -> Referenz
  P1  max_tage aller Bots + 400 Tage     -> welche Felder des Faltenplans bewegen sich?
  P2  median_balken aller Bots x 3      -> Faltenplan? Raster (Zellenzahl und Achsenwerte)?
  P3  n_positionen / median_tage x 3    -> bewegt sich irgendetwas?
  P4  Gruppe `haltedauer` entfernt      -> wer bricht ab?
Gemeldet werden NUR Feldnamen, Anzahl geaenderter Felder und Zellenzahlen
(Verfahrensseite, 27.2) - keine Haltedauer- oder Trade-Zahl (27.1).

Aufruf aus der Repo-Wurzel:
  trading-env/bin/python3 -W ignore docs/belege/TB-102/c_stoerprobe.py
"""
import copy
import os
import sys
import time

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(_REPO, "research", "vorregistrierung"))
import registerdaten as rd  # noqa: E402
import faltenplan as fp     # noqa: E402


def blaetter(x, pfad=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from blaetter(v, f"{pfad}/{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from blaetter(v, f"{pfad}[{i}]")
    else:
        yield pfad, x


def unterschied(a, b):
    da, db = dict(blaetter(a)), dict(blaetter(b))
    geaendert = sorted(k for k in set(da) | set(db) if da.get(k) != db.get(k))
    # Feldname ohne Bot und ohne Faltenindex
    arten = {}
    for k in geaendert:
        teile = k.split("/")
        name = "/".join(t.split("[")[0] if i > 1 else t for i, t in enumerate(teile) if i != 1)
        name = name.replace("falten/", "falten[*]/")
        arten[name] = arten.get(name, 0) + 1
    bots = sorted({k.split("/")[1] for k in geaendert})
    return len(geaendert), arten, bots


def zellen(mess):
    return {b: rd.zellen(b, mess) for b in rd.BOTS}


t0 = time.time()
mess0 = rd._mess()
plan0 = fp.faltenplan(copy.deepcopy(mess0))
z0 = zellen(mess0)
r0 = rd.raster(mess0)
print(f"P0 Referenz: {len(plan0)} Bots, Faltenplan im Speicher ({time.time()-t0:.0f} s)")
print("   Zellen je Bot (Referenz, Verfahrensseite):", z0)

proben = []
m = copy.deepcopy(mess0)
for b in m["haltedauer"]:
    m["haltedauer"][b]["max_tage"] += 400.0
proben.append(("P1 max_tage +400", m))
m = copy.deepcopy(mess0)
for b in m["haltedauer"]:
    m["haltedauer"][b]["median_balken"] *= 3
proben.append(("P2 median_balken x3", m))
m = copy.deepcopy(mess0)
for b in m["haltedauer"]:
    m["haltedauer"][b]["n_positionen"] *= 3
    m["haltedauer"][b]["median_tage"] *= 3
proben.append(("P3 n_positionen, median_tage x3", m))

for name, m in proben:
    t = time.time()
    plan = fp.faltenplan(copy.deepcopy(m))
    n, arten, bots = unterschied(plan0, plan)
    z = zellen(m)
    zdiff = {b: ("gleich" if z[b] == z0[b] else "GEAENDERT") for b in z}
    print(f"\n{name}  ({time.time()-t:.0f} s)")
    print(f"   Faltenplan: {n} Blaetter geaendert, Bots: {bots}")
    for k, v in sorted(arten.items()):
        print(f"      {v:3d} x  {k}")
    print("   Zellen je Bot:", zdiff)
    rn, rarten, rbots = unterschied(r0, rd.raster(m))
    print(f"   Raster (Achsenwerte): {rn} Blaetter geaendert, Bots: {rbots}")
    for k, v in sorted(rarten.items()):
        print(f"      {v:3d} x  {k}")

m = copy.deepcopy(mess0)
del m["haltedauer"]
print("\nP4 Gruppe haltedauer entfernt")
for wer, f in (("faltenplan", lambda: fp.faltenplan(copy.deepcopy(m))),
               ("rd.raster", lambda: rd.raster(m))):
    try:
        f()
        print(f"   {wer}: laeuft ohne haltedauer durch")
    except Exception as e:  # noqa: BLE001
        tb = e.__traceback__
        while tb.tb_next:
            tb = tb.tb_next
        print(f"   {wer}: {type(e).__name__} {e} in "
              f"{os.path.relpath(tb.tb_frame.f_code.co_filename, _REPO)}:{tb.tb_lineno}")
print(f"\nGesamt {time.time()-t0:.0f} s")

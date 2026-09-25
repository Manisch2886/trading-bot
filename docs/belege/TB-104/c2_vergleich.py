"""TB-104 C2 - Ausgabevergleich des Faltenplans vor und nach C1, NUR im Speicher.

⛔ `python3 faltenplan.py` wird nie aufgerufen (TB-83: main() schreibt). Gerechnet
wird `faltenplan.faltenplan(registerdaten._mess())` im Prozess, JSON-Rundreise mit
`sort_keys=True, default=str` - dieselbe Form wie docs/belege/TB-104/b0_ausgaben.sh
Schritt 4 (plan.json, Stand VOR C1).

Soll (Auftrag C2): genau die drei Felder weniger (`purge_tage`, `embargo_tage` je
Plan, `training_bis_ausschliesslich` je Falte), jeder andere Schluessel und Wert
zeichengleich, alle Faltengrenzen gleich.

Aufruf aus der Repo-Wurzel:
    trading-env/bin/python3 -W ignore docs/belege/TB-104/c2_vergleich.py <plan.json vorher>
"""
import json
import sys

sys.path.insert(0, "research/vorregistrierung")
import faltenplan as fp  # noqa: E402
import registerdaten as rd  # noqa: E402

PLAN_FELDER = ("purge_tage", "embargo_tage")
FALTEN_FELDER = ("training_bis_ausschliesslich",)

with open(sys.argv[1], encoding="utf-8") as f:
    vorher = json.load(f)
nachher = json.loads(json.dumps(fp.faltenplan(rd._mess()), sort_keys=True, default=str))

entfernt = {"plan": {}, "falte": {}}
vorher_ohne = {}
for bot, p in vorher.items():
    q = dict(p)
    for k in PLAN_FELDER:
        entfernt["plan"].setdefault(k, 0)
        if k in q:
            del q[k]
            entfernt["plan"][k] += 1
    falten = []
    for f in q["falten"]:
        g = dict(f)
        for k in FALTEN_FELDER:
            entfernt["falte"].setdefault(k, 0)
            if k in g:
                del g[k]
                entfernt["falte"][k] += 1
        falten.append(g)
    q["falten"] = falten
    vorher_ohne[bot] = q

print("Bots vorher/nachher:", len(vorher), len(nachher), sorted(vorher) == sorted(nachher))
print("aus 'vorher' entfernt (Anzahl Vorkommen):", json.dumps(entfernt, sort_keys=True))
fremd_nachher = sorted({k for p in nachher.values() for k in p} & set(PLAN_FELDER)
                       | {k for p in nachher.values() for f in p["falten"] for k in f}
                       & set(FALTEN_FELDER))
print("die drei Felder im Plan NACH C1:", fremd_nachher or "keins")
gleich = json.dumps(vorher_ohne, sort_keys=True) == json.dumps(nachher, sort_keys=True)
print("vorher minus die drei Felder == nachher (zeichengleich, JSON sort_keys):", gleich)
grenzen = all([(f["name"], f["von"], f["bis_ausschliesslich"], f["rolle"]) for f in vorher[b]["falten"]]
              == [(f["name"], f["von"], f["bis_ausschliesslich"], f["rolle"]) for f in nachher[b]["falten"]]
              for b in vorher)
print("Faltengrenzen (name, von, bis, rolle) je Bot gleich:", grenzen)
if not gleich:
    for bot in vorher:
        for k in sorted(set(vorher_ohne[bot]) | set(nachher.get(bot, {}))):
            if vorher_ohne[bot].get(k) != nachher.get(bot, {}).get(k):
                print("  ABWEICHUNG", bot, k)
sys.exit(0 if gleich and grenzen and not fremd_nachher else 1)

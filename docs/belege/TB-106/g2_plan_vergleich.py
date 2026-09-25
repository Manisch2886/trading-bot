"""TB-106 G2 - plan.json vorher/nachher: Unterschied nur die zwei entfernten Schluessel?
Aufruf: python3 docs/belege/TB-106/g2_plan_vergleich.py <vorher/plan.json> <nachher/plan.json>"""
import json, sys
v, n = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
entfernt = {"plan": 0, "falte": 0}
for p in v.values():
    entfernt["plan"] += p.pop("mindesttraining_jahre", None) is not None
    for f in p["falten"]:
        entfernt["falte"] += f.pop("embargo_nach_falten", None) is not None
print("entfernt aus der Vorher-Fassung: mindesttraining_jahre %d x (Plaene), embargo_nach_falten %d x (Falten)" % (
    entfernt["plan"], entfernt["falte"]))
print("Falten insgesamt nachher: %d" % sum(len(p["falten"]) for p in n.values()))
a = json.dumps(v, indent=1, sort_keys=True, default=str)
b = json.dumps(n, indent=1, sort_keys=True, default=str)
print("vorher (ohne die zwei Schluessel) == nachher, zeichengleich: %s" % (a == b))

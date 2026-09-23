"""TB-93 B4: welche Blattwerte weichen ab? Alt = eingefroren, Neu = Nachweislauf."""
import json, sys
alt = json.load(open(sys.argv[1], encoding="utf-8"))
neu = json.load(open(sys.argv[2], encoding="utf-8"))
def blaetter(d, p=()):
    if isinstance(d, dict):
        for k, v in d.items():
            yield from blaetter(v, p + (k,))
    else:
        yield p, d
a = dict(blaetter(alt)); n = dict(blaetter(neu))
print("Blaetter alt/neu:", len(a), len(n), "| nur alt:", sorted(set(a)-set(n)), "| nur neu:", sorted(set(n)-set(a)))
anders = [k for k in a if k in n and a[k] != n[k]]
print("abweichend:", len(anders), "von", len(a))
gruppen = {}
for k in a:
    g = ".".join(k[:2]); gruppen.setdefault(g, [0, 0]); gruppen[g][0] += 1
    if k in anders: gruppen[g][1] += 1
for g, (t, x) in sorted(gruppen.items()):
    print("  %-28s %3d Blaetter, %3d abweichend" % (g, t, x))
print("Erste Abweichung in Dateireihenfolge (sort_keys):", ".".join(anders[0]) if anders else "-",
      "|", a[anders[0]] if anders else "", "->", n[anders[0]] if anders else "")

# TB-123 A3 - C3 vorher/nachher je Testdatei: rc und Schlusszeile (Dauer und Log-Ordner nicht verglichen).
# Aufruf: trading-env/bin/python3 docs/belege/TB-123/a3_vergleich.py <vorher.txt> <nachher.txt>
import re
import sys

ZEILE = re.compile(r"^(test_\w+) rc=(-?\d+) (\d+)s: ?(.*)$")
LOGORDNER = re.compile(r"/\S*/tb12\d_c3_(vorher|nachher)/")


def lesen(pfad):
    kopf, tests = None, {}
    for z in open(pfad, encoding="utf-8"):
        z = z.rstrip("\n")
        if z.startswith("# TB-122 C3"):
            kopf = z
        m = ZEILE.match(z)
        if m:
            tests[m.group(1)] = (int(m.group(2)), int(m.group(3)),
                                 LOGORDNER.sub("<LOG>/", m.group(4)))
    return kopf, tests


kv, v = lesen(sys.argv[1])
kn, n = lesen(sys.argv[2])
print("# vorher : " + (kv or "?"))
print("# nachher: " + (kn or "?"))
print("# Testdateien vorher %d, nachher %d, gemeinsam %d" % (len(v), len(n), len(set(v) & set(n))))
gleich, abw = 0, []
for t in list(v) + [t for t in n if t not in v]:
    a, b = v.get(t), n.get(t)
    if a is None or b is None:
        abw.append(t)
        print("FEHLT     %-30s vorher=%s nachher=%s" % (t, a, b))
        continue
    ok = a[0] == b[0] and a[2] == b[2]
    gleich += ok
    if not ok:
        abw.append(t)
    print("%-9s %-30s rc %s/%s  %4ss/%4ss  | %s%s" % (
        "GLEICH" if ok else "ABWEICHT", t, a[0], b[0], a[1], b[1], a[2],
        "" if a[2] == b[2] else "  ||  " + b[2]))
print("# gleich %d, abweichend %d: %s" % (gleich, len(abw), " ".join(abw) or "-"))

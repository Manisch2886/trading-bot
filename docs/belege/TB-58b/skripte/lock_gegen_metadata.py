"""Jede name==version-Zeile der requirements.lock gegen importlib.metadata (kein pip)."""
import sys, hashlib
from importlib import metadata
pfad = sys.argv[1]
def norm(n): return n.strip().lower().replace("_", "-")
pakete, kopf = [], {}
for z in open(pfad, encoding="utf-8"):
    z = z.strip()
    if not z: continue
    if z.startswith("#"):
        t = z[1:].split()
        if len(t) >= 2: kopf.setdefault(t[0], " ".join(t[1:]))
        continue
    n, v = z.split("==", 1); pakete.append((n.strip(), v.strip()))
abw = []
for n, v in pakete:
    try: ist = metadata.version(n)
    except metadata.PackageNotFoundError: ist = "NICHT"
    if ist != v: abw.append((n, v, ist))
print("interpreter:", sys.executable)
print("sys.version:", " ".join(sys.version.split()))
print("kopf interpreter_voll:", kopf.get("interpreter_voll"))
import platform; print("platform:", platform.platform(), "| kopf plattform:", kopf.get("plattform"))
print("pakete:", len(pakete), "abweichungen:", len(abw), abw[:3])
print("sha256:", hashlib.sha256(open(pfad, "rb").read()).hexdigest())

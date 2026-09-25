"""TB-108 C (42.5): Hash-Uebergaenge seit 4faef05 (Ende TB-94, Stand von 39.5) und register() je Commit.

(1) jede Datei der Sperrliste (Punkte) und der Gruppe eingefroren aus dem Abbild 40ffe18d; alle Commits
    seit 4faef05 mit altem und neuem vollem Hash (`git show <c>~1:<pfad>` / `<c>:<pfad>`).
(2) herkunft.register() (herkunft.py Z. 109-123) an jedem Commit, der einen seiner Teile aendert, nachgebaut
    aus `git show` (gleiche Reihenfolge, gleiche Namen); Probe: HEAD muss den gemessenen Wert geben.
Nur lesend. Aufruf aus der Repo-Wurzel:
  trading-env/bin/python3 docs/belege/TB-108/c_hashuebergaenge.py
"""
import hashlib
import json
import subprocess

V = "research/vorregistrierung/"
BASIS = "4faef05"


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout


def sha(rev, f):
    r = subprocess.run(["git", "show", "%s:%s" % (rev, f)], capture_output=True)
    return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else "(fehlt)"


a = json.load(open(V + "ergebnisse/sperrliste_abbild_2026-09-25b.json"))
pfade = {}
for p in a["punkte"]:
    for f in p["pfade"]:
        pfade.setdefault(f, []).append("Punkt %d" % p["punkt"])
for e in a["eingefroren"]:
    pfade.setdefault(e["pfad"], []).append("eingefroren")
print("# Basis %s (TB-94 Ende, 39.5), HEAD %s" % (BASIS, git("rev-parse", "--short", "HEAD").strip()))
for f in sorted(pfade):
    log = git("log", "--reverse", "--format=%h|%ad|%s", "--date=format:%d.%m.%Y %H:%M",
              BASIS + "..HEAD", "--", f).strip().splitlines()
    print("\n%s  [%s]  %d Commits seit %s" % (f, ", ".join(pfade[f]), len(log), BASIS))
    for z in log:
        h, d, s = z.split("|", 2)
        print("   %s %s  %s -> %s   %s" % (h, d, sha(h + "~1", f), sha(h, f), s[:90]))

TEILE = ["../../docs/VORREGISTRIERUNG_neuselektion.md", "registerdaten.py", "faltenplan.py", "benchmark.py",
         "kennzahlen.py", "auswertung.py", "messgroessen.py", "pruefe_grenzsaetze.py",
         "ergebnisse/messgroessen.json", "ergebnisse/faltenplan.json", "ergebnisse/benchmark_drawdowns.json"]


def repo(rel):
    return "docs/VORREGISTRIERUNG_neuselektion.md" if rel.startswith("../../") else V + rel


def reg(rev):
    h = hashlib.sha256()
    for rel in TEILE:
        b = subprocess.run(["git", "show", "%s:%s" % (rev, repo(rel))], capture_output=True, check=True).stdout
        h.update(rel.encode()); h.update(hashlib.sha256(b).hexdigest().encode())
    return h.hexdigest()


revs = git("log", "--reverse", "--format=%h", BASIS + "..HEAD", "--", *[repo(r) for r in TEILE]).split()
print("\n# register() nachgebaut (Teile: Registerdatei + EINGEFROREN), je Commit, der einen Teil aendert")
print("   %s (Basis, TB-94 Ende)  %s" % (BASIS, reg(BASIS)))
for r in revs:
    s = git("log", "-1", "--format=%ad %s", "--date=format:%d.%m.%Y %H:%M", r).strip()
    print("   %s  %s   %s" % (r, reg(r), s[:80]))
print("   HEAD %s" % reg("HEAD"))

"""TB-98 A3: der Parameterstand. Aus den Protokollen des Lesehakens (Modus-Lauf
a1_neun.sh) je Bot die Repo-Module, die der Erzeuger geladen hat (Python liest
sie ueber den Bytecode-Zwischenspeicher ~/Library/Caches/com.apple.python/<pfad>;
der Pfad dahinter ist die Quelle), dazu je Bot `live_params.py`. SHA-256 der
Quelldateien im Arbeitsbaum; ob sie gegen HEAD sauber sind, sagt `git status`.

Aufruf (Repo-Wurzel):  python3 a3_parameterstand.py <scratch>/a1n/modus
"""
import hashlib
import os
import subprocess
import sys

basis = sys.argv[1]
repo = os.path.realpath(".")
CACHE = os.path.expanduser("~/Library/Caches/com.apple.python")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
print("# TB-98 A3 Parameterstand, HEAD %s" % head)
alle = set()
for bot in sorted(os.listdir(basis)):
    module = set()
    prot = os.path.join(basis, bot, "prot")
    for datei in os.listdir(prot):
        for zeile in open(os.path.join(prot, datei), encoding="utf-8"):
            if zeile.startswith("#"):
                continue
            pfad = zeile.split("\t")[1]
            if pfad.startswith(CACHE) and pfad.endswith(".pyc"):
                quelle = pfad[len(CACHE):]
                quelle = quelle[: -len(".cpython-39.pyc")] + ".py"
            elif pfad.endswith(".py"):
                quelle = pfad
            else:
                continue
            quelle = os.path.realpath(quelle)
            if quelle.startswith(repo + os.sep) and "/trading-env/" not in quelle:
                module.add(os.path.relpath(quelle, repo))
    module.add("strategies/%s/live_params.py" % bot)
    alle |= module
    print("\n== %s: %d Repo-Module geladen (live_params.py dabei: %s)"
          % (bot, len(module), "strategies/%s/live_params.py" % bot in module))
    for m in sorted(module):
        print("   %s  %s" % (sha(m), m))

print("\n== Vereinigung: %d Dateien" % len(alle))
status = subprocess.run(["git", "status", "--porcelain", "--"] + sorted(alle),
                        capture_output=True, text=True).stdout
print("git status --porcelain ueber diese Dateien (leer = alle gleich HEAD): %r" % status)

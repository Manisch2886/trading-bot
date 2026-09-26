"""TB-113 C2 (Kopie von TB-110 d2_zitate.py; Quelle "git:<commit>:<pfad>" per git show): jedes eingesetzte Zitat im Register gegen seine Quelle (diff).

Bauart TB-108 (`docs/belege/TB-108/d2_zitate.py`), auf einen Abschnitt
und einen Abschnitt. Liest zitate.json (vom Einsetzskript), die Quelldateien und
das Register UNABHAENGIG voneinander:
- Zeilenzitat: im Abschnitt des Zitats wird die Registerzeile gesucht, die nach
  Abzug von "> " gleich der Quellzeile (ebenfalls ohne "> ") ist; Quellzeile und
  Registerzeile werden mit `diff` verglichen.
- Teilzitat: der Text muss in der Quellzeile UND in einer Registerzeile des
  Abschnitts stehen; verglichen wird der Ausschnitt der Quellzeile mit dem
  Ausschnitt der Registerzeile an der Fundstelle.
Aufruf aus der Repo-Wurzel; TB113_PROBE=<pfad> prueft eine Kopie.
"""
import json
import os
import subprocess
import tempfile

REG = os.environ.get("TB113_PROBE") or "docs/VORREGISTRIERUNG_neuselektion.md"
reg = open(REG, encoding="utf-8").read().split("\n")
zitate = json.load(open("docs/belege/TB-113/zitate.json", encoding="utf-8"))
BEREICH = {"Abschnitt 44": (next(i for i, r in enumerate(reg) if r.startswith("## 44. ")), len(reg))}


def lies(quelle):
    if quelle.startswith("git:"):
        _, commit, pfad = quelle.split(":", 2)
        return subprocess.run(["git", "show", "%s:%s" % (commit, pfad)], capture_output=True,
                              text=True, check=True).stdout
    return open(quelle, encoding="utf-8").read()


def ohne_praefix(s):
    return s[2:] if s.startswith("> ") else s


def diff(a, b):
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as fa, \
         tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as fb:
        fa.write(a + "\n"); fb.write(b + "\n")
    r = subprocess.run(["diff", fa.name, fb.name], capture_output=True, text=True)
    os.unlink(fa.name); os.unlink(fb.name)
    return r.returncode, r.stdout


fehler = 0
for z in zitate:
    von, bis = BEREICH[z["wo"]]
    quelle = ohne_praefix(lies(z["quelle"]).split("\n")[z["zeile"] - 1])
    if z["art"] == "zeile":
        soll = quelle
        treffer = [i for i in range(von, bis) if reg[i].startswith("> ") and reg[i][2:] == soll]
        wo = treffer[0] + 1 if treffer else 0
        ist = reg[treffer[0]][2:] if treffer else ""
    else:
        k = quelle.find(z["text"])
        soll = quelle[k:k + len(z["text"])] if k >= 0 else ""
        treffer = [i for i in range(von, bis) if z["text"] in reg[i]]
        treffer = sorted(treffer, key=lambda i: reg[i].startswith("> ") and reg[i][2:] == quelle)
        wo = treffer[0] + 1 if treffer else 0
        ist = ""
        if treffer:
            j = reg[treffer[0]].find(z["text"])
            ist = reg[treffer[0]][j:j + len(z["text"])]
    rc, out = diff(soll, ist)
    fehler += rc != 0
    print("%-5s %-8s Z. %3d  -> Register Z. %4d  %4d Zeichen  diff rc %d  (%s)"
          % (z["art"], os.path.basename(z["quelle"])[:14], z["zeile"], wo, len(soll), rc, z["wo"]))
    if rc:
        print(out)
print("Zitate: %d (Zeilen %d, Teile %d), diff rc 0: %d, Abweichungen: %d"
      % (len(zitate), sum(z["art"] == "zeile" for z in zitate),
         sum(z["art"] == "teil" for z in zitate), len(zitate) - fehler, fehler))
raise SystemExit(1 if fehler else 0)

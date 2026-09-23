"""TB-94 E2: jedes eingesetzte Fable-Zitat im Register gegen seine Quelle (diff).

Liest zitate.json (vom Einsetzskript). Fuer ein Zeilenzitat wird im Register die
Zeile gesucht, die nach Abzug des Blockzitat-Praefixes der Quellzeile
entspricht, und beide werden unabhaengig mit `diff` verglichen. Fuer ein
Teilzitat wird im Register der Wortlaut zwischen „ und " gesucht und gegen den
Ausschnitt der Quellzeile ge-diff-t. Aufruf aus der Repo-Wurzel.
"""
import json
import os
import re
import subprocess
import tempfile

REG = "docs/VORREGISTRIERUNG_neuselektion.md"
reg = open(REG, encoding="utf-8").read().split("\n")
zitate = json.load(open("docs/belege/TB-94/zitate.json", encoding="utf-8"))
START39 = next(i for i, r in enumerate(reg) if r.startswith("## 39. "))


def im_ort(i, wo):
    """Zitat in Abschnitt 39 oder in einer Marke davor - je nach Einsetzort."""
    return (i >= START39) == (wo == "Abschnitt 39")


def diff(a, b):
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as fa, \
         tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as fb:
        fa.write(a + "\n"); fb.write(b + "\n")
    r = subprocess.run(["diff", fa.name, fb.name], capture_output=True, text=True)
    os.unlink(fa.name); os.unlink(fb.name)
    return r.returncode, r.stdout


fehler = 0
for z in zitate:
    q = open(z["quelle"], encoding="utf-8").read().split("\n")[z["zeile"] - 1]
    if z["art"] == "zeile":
        treffer = [i for i, r in enumerate(reg)
                   if (r if q.startswith("> ") else r[2:]) == q and r.startswith("> ")
                   and im_ort(i, z["wo"])]
        im_register = (reg[treffer[-1]] if q.startswith("> ") else reg[treffer[-1]][2:]) if treffer else ""
        rc, out = diff(q, im_register)
        wo = treffer[-1] + 1 if treffer else 0
        soll = q
    else:
        soll = z["text"]
        assert soll in q
        kandidaten = [(i, m.group(1)) for i, r in enumerate(reg)
                      for m in re.finditer(r"„([^\"]+)\"", r)]
        passend = [(i, t) for i, t in kandidaten if t.rstrip() == soll and im_ort(i, z["wo"])]
        wo, im_register = (passend[-1][0] + 1, passend[-1][1]) if passend else (0, "")
        rc, out = diff(soll, im_register)
    fehler += rc != 0
    print("%-5s %-58s Z. %3d  -> Register Z. %4d  %4d Zeichen  diff rc %d  (%s)"
          % (z["art"], os.path.basename(z["quelle"])[:58], z["zeile"], wo, len(soll), rc, z["wo"]))
    if rc:
        print(out)
print("Zitate: %d, diff rc 0: %d, Abweichungen: %d" % (len(zitate), len(zitate) - fehler, fehler))
raise SystemExit(1 if fehler else 0)

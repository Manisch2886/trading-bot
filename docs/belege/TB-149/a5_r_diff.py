#!/usr/bin/env python3
"""TB-149 A5: jeder der 6 R-Bloecke (R84-R89) im Register gegen die Quelle 09a, mit `diff`.

Unabhaengig vom Einsetzskript: liest die Quelle am Commit S0 per `git show` und schneidet selbst
(Schnittregel des Auftrags: Beginn bei 'R<n> — ', Ende einschliesslich der ersten Zeile
'Quelle des Grundes:', nur in Z. 216-232).
Im Register: Ueberschrift '### 56.<n> R<nn> — ', danach eine Leerzeile, danach das Blockzitat bis zur
naechsten Leerzeile; je Zeile wird '> ' abgenommen.
Aufruf:  trading-env/bin/python3 docs/belege/TB-149/a5_r_diff.py <S0> [<register>]
rc 0 = 6/6 diff rc 0; rc 1 = Abweichung.
"""
import os
import re
import subprocess
import sys
import tempfile

S0 = sys.argv[1]
REG = sys.argv[2] if len(sys.argv) > 2 else "docs/VORREGISTRIERUNG_neuselektion.md"
Q = ("docs/projektfuehrung/FABLE_ANTWORT_2026-10-09a_beitrag_aus_r45_listen_geschnitten_handelbar_tag.md", 216, 232)

quelle = {}
z = subprocess.run(["git", "show", "%s:%s" % (S0, Q[0])], capture_output=True, text=True,
                   check=True).stdout.split("\n")
r = None
for s in z[Q[1] - 1:Q[2]]:
    m = re.match(r"^R(\d+) — ", s)
    if m:
        r = int(m.group(1))
        quelle[r] = [s]
    elif r is not None:
        quelle[r].append(s)
        if s.startswith("Quelle des Grundes:"):
            r = None

reg = open(REG, encoding="utf-8").read().split("\n")
im_reg = {}
for i, s in enumerate(reg):
    m = re.match(r"^### 56\.(\d+) R(\d+) — ", s)
    if m:
        r = int(m.group(2))
        assert r not in im_reg, ("Ueberschrift doppelt", r)
        assert reg[i + 1] == "", (r, "keine Leerzeile nach der Ueberschrift")
        k, zz = i + 2, []
        while reg[k] != "":
            assert reg[k].startswith("> "), (r, k + 1)
            zz.append(reg[k][2:])
            k += 1
        im_reg[r] = zz

print("# TB-149 A5 R-Diff: Register %s gegen Quelle am Commit %s" % (REG, S0))
print("Bloecke in der Quelle: %d, im Register: %d" % (len(quelle), len(im_reg)))
gut = 0
with tempfile.TemporaryDirectory() as t:
    for r in range(84, 90):
        qa, ra = os.path.join(t, "q%d" % r), os.path.join(t, "r%d" % r)
        open(qa, "w", encoding="utf-8").write("\n".join(quelle.get(r, ["(fehlt)"])) + "\n")
        open(ra, "w", encoding="utf-8").write("\n".join(im_reg.get(r, ["(fehlt)"])) + "\n")
        p = subprocess.run(["diff", qa, ra], capture_output=True, text=True)
        print("R%d: %d Zeilen, diff rc %d" % (r, len(quelle.get(r, [])), p.returncode))
        if p.returncode == 0:
            gut += 1
        else:
            print(p.stdout[:2000])
print("Ergebnis: %d/6 rc 0" % gut)
sys.exit(0 if gut == 6 and sorted(quelle) == list(range(84, 90)) else 1)

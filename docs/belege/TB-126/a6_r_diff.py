#!/usr/bin/env python3
"""TB-126 A6: jeder der 38 R-Bloecke (R18-R55) im Register gegen seine Quelle, mit `diff`.

Unabhaengig vom Einsetzskript: liest die Quellen am Commit S0 per `git show` und schneidet selbst
(Schnittregel des Auftrags: Beginn bei 'R<n> — ' bzw. '**R<n> — ', Ende einschliesslich der ersten Zeile
'Quelle des Grundes:' bzw. '*Quelle des Grundes:*', nur innerhalb der genannten Zeilenbereiche).
Im Register: Ueberschrift '### <x.n> R<nn> — ', danach eine Leerzeile, danach das Blockzitat bis zur
naechsten Leerzeile; je Zeile wird '> ' abgenommen.
Aufruf:  trading-env/bin/python3 docs/belege/TB-126/a6_r_diff.py <S0> [<register>]
rc 0 = 38/38 diff rc 0; rc 1 = Abweichung.
"""
import os
import re
import subprocess
import sys
import tempfile

S0 = sys.argv[1]
REG = sys.argv[2] if len(sys.argv) > 2 else "docs/VORREGISTRIERUNG_neuselektion.md"
FD = "docs/projektfuehrung/"
QUELLEN = [(FD + "FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md", 161, 209),
           (FD + "FABLE_ANTWORT_2026-09-29b_sammlung_erzeuger_kalter_leser.md", 190, 267),
           (FD + "FABLE_ANTWORT_2026-09-30a_vorgepruefte_fragen_e2.md", 25, 32)]

quelle = {}
for pfad, a, b in QUELLEN:
    z = subprocess.run(["git", "show", "%s:%s" % (S0, pfad)], capture_output=True, text=True,
                       check=True).stdout.split("\n")
    r = None
    for s in z[a - 1:b]:
        m = re.match(r"^(?:\*\*)?R(\d+) — ", s)
        if m:
            r = int(m.group(1))
            quelle[r] = [s]
        elif r is not None:
            quelle[r].append(s)
            if re.match(r"^\*?Quelle des Grundes:", s):
                r = None

reg = open(REG, encoding="utf-8").read().split("\n")
im_reg = {}
for i, s in enumerate(reg):
    m = re.match(r"^### (4[789])\.(\d+) R(\d+) — ", s)
    if m:
        r = int(m.group(3))
        assert r not in im_reg, ("Ueberschrift doppelt", r)
        assert reg[i + 1] == "", (r, "keine Leerzeile nach der Ueberschrift")
        k, zz = i + 2, []
        while reg[k] != "":
            assert reg[k].startswith("> "), (r, k + 1)
            zz.append(reg[k][2:])
            k += 1
        im_reg[r] = zz

print("# TB-126 A6 R-Diff: Register %s gegen Quellen am Commit %s" % (REG, S0))
print("Bloecke in den Quellen: %d, im Register: %d" % (len(quelle), len(im_reg)))
gut = 0
with tempfile.TemporaryDirectory() as t:
    for r in range(18, 56):
        qa, ra = os.path.join(t, "q%d" % r), os.path.join(t, "r%d" % r)
        open(qa, "w", encoding="utf-8").write("\n".join(quelle.get(r, ["(fehlt)"])) + "\n")
        open(ra, "w", encoding="utf-8").write("\n".join(im_reg.get(r, ["(fehlt)"])) + "\n")
        p = subprocess.run(["diff", qa, ra], capture_output=True, text=True)
        print("R%d: %d Zeilen, diff rc %d" % (r, len(quelle.get(r, [])), p.returncode))
        if p.returncode == 0:
            gut += 1
        else:
            print(p.stdout[:2000])
print("Ergebnis: %d/38 rc 0" % gut)
sys.exit(0 if gut == 38 and sorted(quelle) == list(range(18, 56)) else 1)

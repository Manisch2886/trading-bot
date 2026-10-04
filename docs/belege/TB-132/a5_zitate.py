#!/usr/bin/env python3
"""TB-132 A5: Kopf 53.0 und Schluss 53.9-53.10 aus dem Auftrag gegen das Register (2 diffs).

Unabhaengig vom Einsetzskript. Auftrag am Commit S0 per `git show`; alle ````-Zaeune des Auftrags,
der mit '## 53. ' beginnende ist der Kopf, der mit '### 53.9 ' beginnende der Schluss.
Ersetzt: ⟨S0⟩ -> `<S0>`, ⟨DATUM⟩ -> Datum.
Im Register: Kopf = von '## 53. ' bis vor '### 53.1 ' ohne Leerzeilen am Ende; Schluss = von '### 53.9 '
bis Dateiende ohne Leerzeilen am Ende.
Aufruf:  trading-env/bin/python3 docs/belege/TB-132/a5_zitate.py <S0> <datum> [<register>]
rc 0 = 2/2 diff rc 0.
"""
import os
import subprocess
import sys
import tempfile

S0, DATUM = sys.argv[1], sys.argv[2]
REG = sys.argv[3] if len(sys.argv) > 3 else "docs/VORREGISTRIERUNG_neuselektion.md"
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-132_register_fable_02c.md" % S0],
                     capture_output=True, text=True, check=True).stdout.split("\n")
zaeune, cur = [], None
for s in auf:
    if s == "````":
        if cur is None:
            cur = []
        else:
            zaeune.append(cur)
            cur = None
    elif cur is not None:
        cur.append(s)
kopf = [z for z in zaeune if z[0].startswith("## 53. ")]
schluss = [z for z in zaeune if z[0].startswith("### 53.9 ")]
assert len(kopf) == 1 and len(schluss) == 1, (len(kopf), len(schluss))


def ersetze(zz):
    return [s.replace("⟨S0⟩", "`%s`" % S0).replace("⟨DATUM⟩", DATUM) for s in zz]


reg = open(REG, encoding="utf-8").read().split("\n")


def einzig(prefix):
    t = [i for i, s in enumerate(reg) if s.startswith(prefix)]
    assert len(t) == 1, (prefix, t)
    return t[0]


i52, i521, i524 = einzig("## 53. "), einzig("### 53.1 "), einzig("### 53.9 ")
rk = reg[i52:i521]
rs = reg[i524:]
for zz in (rk, rs):
    while zz and zz[-1] == "":
        zz.pop()
paare = [("Kopf 53.0", ersetze(kopf[0]), rk), ("Schluss 53.9-53.10", ersetze(schluss[0]), rs)]
print("# TB-132 A5 Zitate: Register %s gegen Auftrag am Commit %s" % (REG, S0))
gut = []
with tempfile.TemporaryDirectory() as t:
    for n, (name, soll, ist) in enumerate(paare):
        a, b = os.path.join(t, "s%d" % n), os.path.join(t, "i%d" % n)
        open(a, "w", encoding="utf-8").write("\n".join(soll) + "\n")
        open(b, "w", encoding="utf-8").write("\n".join(ist) + "\n")
        p = subprocess.run(["diff", a, b], capture_output=True, text=True)
        print("%s: %d Zeilen (Register Z. %d-%d), diff rc %d" % (
            name, len(soll), (i52 if n == 0 else i524) + 1, (i52 if n == 0 else i524) + len(ist), p.returncode))
        if p.returncode:
            print(p.stdout[:2000])
        gut.append(p.returncode == 0)
print("Ergebnis: %d/2 rc 0" % sum(gut))
sys.exit(0 if all(gut) else 1)

#!/usr/bin/env python3
"""TB-126 A6: Koepfe 47.0, 48.0, 49.0 und der Text von 50 aus dem Auftrag gegen das Register (4 diffs),
dazu das Docstring-Zitat und die zwei Entwuerfe je gegen ihre Quelle (3 diffs).

Unabhaengig vom Einsetzskript. Auftrag und Quellen am Commit S0 per `git show`. Im Auftragstext werden
ersetzt: ⟨S0⟩ -> `<S0>`, ⟨Z_A⟩/⟨Z_B⟩ -> die Zeilen des Docstring-Bereichs, die drei Zitat-Platzhalter ->
die Zeilen ihrer Quelle.
Aufruf:  trading-env/bin/python3 docs/belege/TB-126/a6_zitate.py <S0> [<register>]
rc 0 = 4/4 und 3/3 diff rc 0.
"""
import os
import subprocess
import sys
import tempfile

S0 = sys.argv[1]
REG = sys.argv[2] if len(sys.argv) > 2 else "docs/VORREGISTRIERUNG_neuselektion.md"


def show(p):
    return subprocess.run(["git", "show", "%s:%s" % (S0, p)], capture_output=True, text=True, check=True).stdout


auf = show("docs/auftraege/MAC_TB-126_register_e2.md").split("\n")
# alle ````-Zaeune des Auftrags in Reihenfolge
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
k47 = next(z for z in zaeune if z[0].startswith("## 47. "))
k48 = next(z for z in zaeune if z[0].startswith("## 48. "))
k49 = next(z for z in zaeune if z[0].startswith("## 49. "))
t50 = next(z for z in zaeune if z[0].startswith("## 50. "))

A = show("research/vorregistrierung/auswertung.py").split("\n")
za = next(i for i, s in enumerate(A) if s.strip() == "DIE ROHERGEBNISSE - DER VERTRAG")
zb = next(i for i, s in enumerate(A) if s.strip() == "ZWEI DEFINITIONEN, DIE SONST SCHWEIGEND AUSEINANDERLAUFEN") - 1
while not A[zb].strip():
    zb -= 1
doc = A[za:zb + 1]
e122 = show("docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md").split("\n")[234:275]
e124 = show("docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md").split("\n")[288:323]


def ersetze(zz):
    aus = []
    for s in zz:
        if s == "⟨ZITAT_DOCSTRING⟩":
            aus += doc
        elif s == "⟨ENTWURF_TB122⟩":
            aus += e122
        elif s == "⟨ENTWURF_TB124⟩":
            aus += e124
        else:
            aus.append(s.replace("⟨S0⟩", "`%s`" % S0).replace("⟨Z_A⟩", str(za + 1)).replace("⟨Z_B⟩", str(zb + 1)))
    return aus


reg = open(REG, encoding="utf-8").read().split("\n")


def kopfzeile(prefix):
    t = [i for i, s in enumerate(reg) if s.startswith(prefix)]
    assert len(t) == 1, (prefix, t)
    return t[0]


def bis_vor(i, prefix):
    """Zeilen ab i bis vor die naechste Zeile mit prefix, ohne Leerzeilen am Ende."""
    j = next(k for k in range(i + 1, len(reg)) if reg[k].startswith(prefix))
    zz = reg[i:j]
    while zz and zz[-1] == "":
        zz.pop()
    return zz


r47 = bis_vor(kopfzeile("## 47. "), "### 47.1 ")
r48 = bis_vor(kopfzeile("## 48. "), "### 48.1 ")
r49 = bis_vor(kopfzeile("## 49. "), "### 49.1 ")
i50 = kopfzeile("## 50. ")
r50 = reg[i50:]
while r50 and r50[-1] == "":
    r50.pop()
# Einzelzitate im Register
i502 = kopfzeile("### 50.2 ")
f1 = next(k for k in range(i502, len(reg)) if reg[k] == "```")
f2 = next(k for k in range(f1 + 1, len(reg)) if reg[k] == "```")
rdoc = reg[f1 + 1:f2]
i503, i504, i505 = kopfzeile("### 50.3 "), kopfzeile("### 50.4 "), kopfzeile("### 50.5 ")
r122 = [s for s in reg[i503 + 1:i504]]
r124 = [s for s in reg[i504 + 1:i505]]
# Entwurf = alles nach der kursiven Einleitungszeile und ihrer Leerzeile, ohne Leerzeilen am Rand
def entwurf(zz):
    zz = zz[:]
    while zz and zz[0] == "":
        zz.pop(0)
    assert zz[0].startswith("*Übernommen zeichengleich"), zz[0][:40]
    zz = zz[1:]
    while zz and zz[0] == "":
        zz.pop(0)
    while zz and zz[-1] == "":
        zz.pop()
    return zz


r122, r124 = entwurf(r122), entwurf(r124)

paare = [("Kopf 47.0", ersetze(k47), r47), ("Kopf 48.0", ersetze(k48), r48), ("Kopf 49.0", ersetze(k49), r49),
         ("Text 50", ersetze(t50), r50),
         ("Docstring auswertung.py Z. %d-%d" % (za + 1, zb + 1), doc, rdoc),
         ("Entwurf TB-122 Z. 235-275", e122, r122), ("Entwurf TB-124 Z. 289-323", e124, r124)]
print("# TB-126 A6 Zitate: Register %s gegen Auftrag/Quellen am Commit %s" % (REG, S0))
gut = []
with tempfile.TemporaryDirectory() as t:
    for n, (name, soll, ist) in enumerate(paare):
        a, b = os.path.join(t, "s%d" % n), os.path.join(t, "i%d" % n)
        open(a, "w", encoding="utf-8").write("\n".join(soll) + "\n")
        open(b, "w", encoding="utf-8").write("\n".join(ist) + "\n")
        p = subprocess.run(["diff", a, b], capture_output=True, text=True)
        print("%s: %d Zeilen, diff rc %d" % (name, len(soll), p.returncode))
        if p.returncode:
            print(p.stdout[:2000])
        gut.append(p.returncode == 0)
print("Ergebnis: Koepfe/Text %d/4 rc 0; Einzelzitate %d/3 rc 0" % (sum(gut[:4]), sum(gut[4:])))
sys.exit(0 if all(gut) else 1)

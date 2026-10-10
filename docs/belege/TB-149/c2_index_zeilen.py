#!/usr/bin/env python3
"""TB-149 C2 (mechanischer Teil): in REGISTER_INDEX.md jede Registerzeile 'Z. <n>' vom alten Stand (S0) auf
den neuen Stand (Register-Commit des Schritts A) umschreiben, auch Listen 'Z. a, b' und Bereiche 'Z. a–b'
an jeder Zahl; Abbildung aus dem Vergleich der Registerzeilen (alte Zeilen stehen in derselben Reihenfolge im
neuen Register, Nachweis A5). Vorlage docs/belege/TB-139/c2_index_zeilen.py (dort Vorlage docs/belege/TB-136/c2_index_zeilen.py), dort nach TB-132, TB-130 und Bauart TB-129 (jede Zahl; TB-126 bildete nur die erste Zahl einer Liste
oder eines Bereichs ab).
Ausgenommen ist die Zeile '*Frühere Vierteilung*' (Teilgrenzen; sie wird aus c1 neu geschrieben).
Aufruf: trading-env/bin/python3 docs/belege/TB-149/c2_index_zeilen.py <S0> <commit_A>
"""
import re
import subprocess
import sys

S0, CA = sys.argv[1:3]
R = "docs/VORREGISTRIERUNG_neuselektion.md"
I = "docs/projektfuehrung/REGISTER_INDEX.md"
def show(c): return subprocess.run(["git", "show", "%s:%s" % (c, R)], capture_output=True, text=True, check=True).stdout.split("\n")
alt, neu = show(S0), show(CA)
abb, j = {}, 0
for i, s in enumerate(alt):
    while neu[j] != s:
        j += 1
    abb[i + 1] = j + 1
    j += 1
zeilen = open(I, encoding="utf-8").read().split("\n")
n = [0, 0]
def ersetze(m):
    teile = re.split(r"(, |–)", m.group(1))
    aus = []
    for t in teile:
        if t in (", ", "–"):
            aus.append(t)
            continue
        a = int(t); b = abb[a]
        assert neu[b - 1] == alt[a - 1]
        n[0] += 1
        n[1] += a != b
        print("Z. %d -> Z. %d  (%s)" % (a, b, alt[a - 1][:70]))
        aus.append(str(b))
    return "Z. " + "".join(aus)
for k, s in enumerate(zeilen):
    if s.startswith("*Frühere Vierteilung*"):
        print("ausgenommen: Index-Z. %d (Teilgrenzen)" % (k + 1))
        continue
    zeilen[k] = re.sub(r"Z\. (\d+(?:(?:, |–)\d+)*)", ersetze, s)
open(I, "w", encoding="utf-8").write("\n".join(zeilen))
print("Zahlen in Zeilenangaben umgeschrieben: %d, davon geaendert: %d" % (n[0], n[1]))

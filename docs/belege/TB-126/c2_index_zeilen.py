#!/usr/bin/env python3
"""TB-126 C2 (mechanischer Teil): in REGISTER_INDEX.md jede Registerzeile 'Z. <n>' vom alten Stand (S0) auf
den neuen Stand (Register-Commit des Schritts A) umschreiben; Abbildung aus dem Vergleich der Registerzeilen
(alte Zeilen stehen in derselben Reihenfolge im neuen Register, Nachweis A6). Spalte T nach dem neuen Zuschnitt
fuer die drei verschobenen Abschnitte 23 (T1->T2), 37 (T2->T3), 43 (T3->T4) und fuer '**23.3** (T1)'.
Aufruf: trading-env/bin/python3 docs/belege/TB-126/c2_index_zeilen.py <S0> <commit_A>
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
text = open(I, encoding="utf-8").read()
n = [0]
def ersetze(m):
    a = int(m.group(1)); b = abb[a]
    assert neu[b - 1] == alt[a - 1]
    n[0] += 1
    print("Z. %d -> Z. %d  (%s)" % (a, b, alt[a - 1][:70]))
    return "Z. %d" % b
text = re.sub(r"Z\. (\d+)", ersetze, text)
T = [("ERSETZT durch 23.3 | **23.3** (T1) |", "ERSETZT durch 23.3 | **23.3** (T2) |"),
     ("| 23 Benchmark tagesgenau | 1 |", "| 23 Benchmark tagesgenau | 2 |"),
     ("| 37 Sonde je Bestandteil | 2 |", "| 37 Sonde je Bestandteil | 3 |"),
     ("| 43 aus 25d/25e | 3 |", "| 43 aus 25d/25e | 4 |")]
for a, b in T:
    assert text.count(a) == 1, a
    text = text.replace(a, b)
open(I, "w", encoding="utf-8").write(text)
print("Zeilenangaben umgeschrieben: %d; Spalte T: %d Stellen" % (n[0], len(T)))

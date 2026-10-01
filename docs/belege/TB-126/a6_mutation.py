#!/usr/bin/env python3
"""TB-126 A6 Mutationsprobe: an einer KOPIE des Registers ein Wort in einem R-Block aendern
(Block R40 unter 48.8, erstes Vorkommen von ' die ' in der ersten Zitatzeile -> ' der '), dann
a6_r_diff.py gegen die Kopie laufen lassen. Soll: rc 1.
Aufruf:  trading-env/bin/python3 docs/belege/TB-126/a6_mutation.py <S0> <register> <kopie>
"""
import subprocess
import sys

S0, REG, KOPIE = sys.argv[1:4]
L = open(REG, encoding="utf-8").read().split("\n")
i = next(k for k, s in enumerate(L) if s.startswith("### 48.8 R40 — ")) + 2
assert L[i].startswith("> ") and " die " in L[i], L[i][:60]
L[i] = L[i].replace(" die ", " der ", 1)
open(KOPIE, "w", encoding="utf-8").write("\n".join(L))
print("geaendert: Register-Zeile %d (R40), ' die ' -> ' der ' (erstes Vorkommen)" % (i + 1))
p = subprocess.run([sys.executable, "docs/belege/TB-126/a6_r_diff.py", S0, KOPIE], capture_output=True, text=True)
print("\n".join(s for s in p.stdout.split("\n") if s.startswith("R40") or s.startswith("Ergebnis")))
print("a6_r_diff.py gegen die Kopie: rc %d (Soll 1)" % p.returncode)
sys.exit(0 if p.returncode == 1 else 1)

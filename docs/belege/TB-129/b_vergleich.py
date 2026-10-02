#!/usr/bin/env python3
"""TB-129 B: Zeichengleichheit des BACKLOG-Blocks E1.

Zweiter, unabhaengiger Leser (Bauart TB-128 c3_vergleich.py, eigener Parser): nimmt aus dem Auftrag am
Commit S0 den Abschnitt von `#### E1 — ` bis zur naechsten Zeile, die mit `## ` beginnt (ganze Zeile,
nicht `### ` im Codeblock), daraus den ersten ```-Codeblock ohne Zaeune, und prueft als Bytevergleich,
dass er in BACKLOG.md genau einmal an Zeilengrenzen steht, mit je einer Leerzeile davor und danach,
und dass danach der Anker folgt.
Aufruf aus der Repo-Wurzel:  trading-env/bin/python3 docs/belege/TB-129/b_vergleich.py <S0>
"""
import re
import subprocess
import sys

S0 = sys.argv[1]
roh = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-129_register_fable_01a.md" % S0],
                     capture_output=True, check=True).stdout
a = roh.index(b"\n#### E1 ")
b = roh.index(b"\n## ", a + 1)
abschnitt = roh[a:b]
text = re.search(rb"\n```\n(.*?)\n```\n", abschnitt, re.S).group(1)
ziel = open("docs/projektfuehrung/BACKLOG.md", "rb").read()
gesamt = ziel.count(text)
an_grenzen = ziel.count(b"\n" + text + b"\n")
form = ziel.count(b"\n\n" + text + b"\n\n## 6 \xe2\x80\x94 Geparkt, null Arbeit")
nz = text.count(bytes([10])) + 1
gut = gesamt == 1 and an_grenzen == 1 and form == 1
print("# TB-129 B — Zeichengleichheit (b_vergleich.py, Auftrag am Commit %s)" % S0)
print(f"E1 · docs/projektfuehrung/BACKLOG.md · {len(text)} Bytes · {nz} Zeilen · "
      f"Vorkommen {gesamt} · an Zeilengrenzen {an_grenzen} · Leerzeile davor/danach und Anker danach {form} · "
      f"{'GLEICH' if gut else 'ABWEICHUNG'}")
sys.exit(0 if gut else 1)

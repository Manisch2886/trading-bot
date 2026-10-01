#!/usr/bin/env python3
"""TB-126 C2 Gegenprobe: jede Angabe 'Z. <n>' (auch Listen 'Z. a, b' und Bereiche 'Z. a–b' an ihren Enden) in
REGISTER_INDEX.md zeigt im Register am HEAD auf eine Zeile mit einem Markenwort (ERSETZT, PRÄZISIERT, BERICHTIGT,
ERGÄNZT, KORRIGIERT) oder wird mit ihrem Text gezeigt. Dazu: die Indexzeilen aus Anhang A Liste A (6) stehen im Index.
Aufruf: trading-env/bin/python3 docs/belege/TB-126/c2_index_pruefen.py
"""
import re
I = open("docs/projektfuehrung/REGISTER_INDEX.md", encoding="utf-8").read()
L = open("docs/VORREGISTRIERUNG_neuselektion.md", encoding="utf-8").read().split("\n")
W = re.compile(r"ERSETZT|PRÄZISIERT|BERICHTIGT|ERGÄNZT|KORRIGIERT")
nummern = []
for m in re.finditer(r"Z\. (\d+(?:(?:, |–)\d+)*)", I):
    nummern += [int(x) for x in re.split(r", |–", m.group(1))]
ohne = [n for n in nummern if not W.search(L[n - 1])]
print("Zeilenangaben im Index: %d; mit Markenwort: %d" % (len(nummern), len(nummern) - len(ohne)))
for n in ohne:
    print("  ohne Markenwort: Z. %d: %s" % (n, L[n - 1][:100]))
print("Indexzeilen E-2: %d (Soll 6)" % I.count("**Indexzeile E-2**"))

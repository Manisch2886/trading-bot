#!/usr/bin/env python3
"""TB-129 D2: Journalblock EA vor '## Wiederkehrende Lehren' einfuegen (Anker vorher genau 1, Kennung 'EA' vorher 0,
letzter Buchstabenblock DZ). Text aus d2_journal_block.md. Aufruf: trading-env/bin/python3 docs/belege/TB-129/d2_journal.py
"""
import re
J = "docs/projektfuehrung/JOURNAL.md"
t = open(J, encoding="utf-8").read()
blk = open("docs/belege/TB-129/d2_journal_block.md", encoding="utf-8").read().rstrip("\n")
A = "\n## Wiederkehrende Lehren\n"
kennungen = re.findall(r"^## ([A-Z]{2}) — ", t, re.M)
print("Anker vorher:", t.count(A), "| letzte Kennung:", kennungen[-1], "| '## EA ' vorher:", t.count("\n## EA "))
assert t.count(A) == 1 and kennungen[-1] == "DZ" and t.count("\n## EA ") == 0
t = t.replace(A, "\n" + blk + "\n\n---\n" + A)
open(J, "w", encoding="utf-8").write(t)
print("erste Blockzeile nachher:", t.count(blk.split("\n")[0]), "| Block nachher:", t.count(blk))

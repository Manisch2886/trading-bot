#!/usr/bin/env python3
"""TB-154 D2: Journalblock ER vor '## Wiederkehrende Lehren' einfuegen (Anker vorher genau 1, Kennung 'ER' vorher 0,
letzter Buchstabenblock EQ). Text aus d2_journal_block.md. Aufruf: trading-env/bin/python3 docs/belege/TB-154/d2_journal.py
"""
import re
J = "docs/projektfuehrung/JOURNAL.md"
t = open(J, encoding="utf-8").read()
blk = open("docs/belege/TB-154/d2_journal_block.md", encoding="utf-8").read().rstrip("\n")
A = "\n## Wiederkehrende Lehren\n"
kennungen = re.findall(r"^## ([A-Z]{2}) — ", t, re.M)
print("Anker vorher:", t.count(A), "| letzte Kennung:", kennungen[-1], "| '## ER ' vorher:", t.count("\n## ER "))
assert t.count(A) == 1 and kennungen[-1] == "EQ" and t.count("\n## ER ") == 0
t = t.replace(A, "\n" + blk + "\n\n---\n" + A)
open(J, "w", encoding="utf-8").write(t)
print("erste Blockzeile nachher:", t.count(blk.split("\n")[0]), "| Block nachher:", t.count(blk))

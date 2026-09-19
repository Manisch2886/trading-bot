"""Fables Wortlaut (A) und (B) im Entwurf gegen den Auftrag pruefen.

(A) muss zeichengleich sein; bei (B) muessen alle festen Segmente zwischen
den Platzhaltern ⟨…⟩ in Reihenfolge vorkommen. Aufruf:
    python3 wortlaut_vergleich.py <auftrag.md> <entwurf.md>
"""
import re
import sys

auftrag = open(sys.argv[1], encoding="utf-8").read()
entwurf = open(sys.argv[2], encoding="utf-8").read()


def quotes(text):
    blocks, cur = [], []
    for z in text.splitlines():
        if z.startswith(">"):
            cur.append(z[1:].strip())
        elif cur:
            blocks.append("\n".join(cur))
            cur = []
    if cur:
        blocks.append("\n".join(cur))
    return blocks


qa, qe = quotes(auftrag), quotes(entwurf)
print("Blockzitate Auftrag:", len(qa), "Entwurf:", len(qe))
print("A woertlich gleich:", qa[0] == qe[0])
segs = re.split(r"⟨[^⟩]*⟩", qa[1])
pos, ok = 0, True
for s in segs:
    i = qe[1].find(s, pos)
    if i < 0:
        ok = False
        print("FEHLT:", repr(s[:60]))
        break
    pos = i + len(s)
print("B: alle festen Segmente in Reihenfolge vorhanden:", ok,
      "| Segmente:", len(segs), "| Platzhalter:", len(segs) - 1)

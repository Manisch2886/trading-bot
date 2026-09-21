#!/usr/bin/env python3
"""Verschiebenachweis TB-63: jede aus BACKLOG.md entfernte Zeile steht zeichengleich in BACKLOG_EPICS.md.

Vergleich der Zeilenmengen (Multimengen) - nicht ueber 'git diff', damit
Markdown-Trennlinien '---' nicht mit Diff-Kopfzeilen verwechselt werden
(TB-60: 546 statt 561). Gegenprobe: Zielzeilen, die nicht aus dem Backlog stammen.
Aufruf: python3 verschiebenachweis.py <basis-commit> [<neu-commit|WORKTREE>]
"""
import subprocess, sys
from collections import Counter

BASIS = sys.argv[1]
NEU = sys.argv[2] if len(sys.argv) > 2 else "WORKTREE"
BL = "docs/projektfuehrung/BACKLOG.md"
EP = "docs/projektfuehrung/BACKLOG_EPICS.md"

def lese(rev, pfad):
    if rev == "WORKTREE":
        with open(pfad, encoding="utf-8") as fh:
            return fh.read().splitlines()
    out = subprocess.run(["git", "show", f"{rev}:{pfad}"], capture_output=True, text=True)
    if out.returncode != 0:
        return []
    return out.stdout.splitlines()

alt = Counter(lese(BASIS, BL))
neu = Counter(lese(NEU, BL))
ziel = Counter(lese(NEU, EP))
ziel_alt = Counter(lese(BASIS, EP))

entfernt = alt - neu            # Zeilen, die im Backlog fehlen (Multimenge)
hinzu = neu - alt               # Zeilen, die im Backlog neu sind
fehlt_im_ziel = entfernt - ziel # entfernte Zeilen ohne zeichengleiches Gegenstueck im Ziel
nur_im_ziel = (ziel - ziel_alt) - entfernt  # Zielzeilen, die nicht aus dem Backlog stammen

def n(c): return sum(c.values())
print(f"Basis {BASIS} -> {NEU}")
print(f"BACKLOG.md entfernte Zeilen (Multimenge): {n(entfernt)}   hinzugefuegte: {n(hinzu)}")
print(f"davon NICHT zeichengleich in BACKLOG_EPICS.md: {n(fehlt_im_ziel)}")
for z, k in fehlt_im_ziel.items():
    print("   FEHLT:", k, "x", repr(z[:100]))
print(f"Gegenprobe - Zeilen nur im Ziel (Kopf und Verweise): {n(nur_im_ziel)}")
for z, k in sorted(nur_im_ziel.items()):
    print(f"   NUR IM ZIEL ({k}x): {z[:110]!r}")
print(f"Zeilen im Ziel gesamt: {n(ziel)}  (= {n(entfernt)} verschoben + {n(nur_im_ziel)} eigene"
      f"{'  -> stimmt' if n(ziel) == n(entfernt) + n(nur_im_ziel) else '  -> STIMMT NICHT'})")
print("--- hinzugefuegte Backlog-Zeilen (die Verweistabelle):")
for z, k in hinzu.items():
    print(f"   +{k}x {z[:110]!r}")
sys.exit(0 if n(fehlt_im_ziel) == 0 else 1)

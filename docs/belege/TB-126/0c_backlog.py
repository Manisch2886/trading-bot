#!/usr/bin/env python3
"""TB-126 0c: Block 'Aus der Abnahme TB-124' vor der Ankerzeile von BACKLOG Abschnitt 6 einfuegen.
Text zeichengleich aus dem Auftrag am Commit S0 (Codezaun nach '**0c. BACKLOG.**')."""
import subprocess, sys
S0 = sys.argv[1]
PFAD = "docs/projektfuehrung/BACKLOG.md"
ANKER = "## 6 — Geparkt, null Arbeit *(ins Archiv verschoben 20.09.2026, TB-60)*"
auftrag = subprocess.run(["git", "show", f"{S0}:docs/auftraege/MAC_TB-126_register_e2.md"],
                         capture_output=True, text=True, check=True).stdout
rest = auftrag.split("**0c. BACKLOG.**", 1)[1]
block = rest.split("```\n", 1)[1].split("```\n", 1)[0]   # Inhalt des Zauns, endet mit Leerzeile
assert block.startswith("### Aus der Abnahme TB-124 (30.09.2026)\n") and block.endswith("\n\n"), repr(block[-20:])
text = open(PFAD, encoding="utf-8").read()
zeilen = text.split("\n")
n = sum(1 for z in zeilen if z == ANKER)
print("Ankerzahl vorher:", n)
if n != 1:
    sys.exit("Anker nicht genau 1")
i = zeilen.index(ANKER)
assert zeilen[i - 1] == "", "vor dem Anker keine Leerzeile"
neu = "\n".join(zeilen[:i]) + "\n" + block + "\n".join(zeilen[i:])
open(PFAD, "w", encoding="utf-8").write(neu)
erste = block.split("\n", 1)[0]
print("erste Textzeile nachher:", sum(1 for z in neu.split("\n") if z == erste))

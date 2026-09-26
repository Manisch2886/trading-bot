#!/usr/bin/env python3
"""TB-111 B4 - die Proben aus test_ersatzwerte.py Teil F einzeln, mit Zahlen
(damit sichtbar ist, dass der Lesehaken unter der Mutation etwas SIEHT).
Aufruf aus der Worktree-Wurzel mit trading-env/bin/python3."""
import os, sys
sys.path.insert(0, "research/vorregistrierung")
import test_ersatzwerte as te

def zeige(name, r):
    print(f"{name}: rc {r['rc']}, Zugriffe unter der Ersatzwurzel {len(r['zugriffe'])}")
    for z in r["zugriffe"][:4]:
        print("     ", z)
    abb = [z for z in r["err"].splitlines() if "ABBRUCH" in z or "Error" in z]
    print("   stderr:", abb[-1][:200] if abb else "-")

r = te._fa_lauf(False); print("F-a  ohne Mutation: rc", r["rc"], "datenstand", r["json"].get("herkunft", {}).get("datenstand"), r["json"].get("herkunft", {}).get("datendateien"))
r = te._fa_lauf(True);  print("F-aM mit Mutation:  rc", r["rc"], [z for z in r["err"].splitlines() if "ABBRUCH" in z][:1])
for argv in (("pruefansicht",), ("commit",), ("register",), ("block", te._F_SNAP)):
    zeige(f"F-b  {argv[0]:12s} ohne Mutation", te._fb_lauf(False, argv=argv))
zeige("F-bM  'Pruefung weg'        mit Mutation", te._fb_lauf(True, (te.FB_NEU, te.FB_ALT)))
zeige("F-bM2 'paths aus BASE_DIR'  mit Mutation", te._fb_lauf(True, (te.FB2_NEU, te.FB2_ALT)))

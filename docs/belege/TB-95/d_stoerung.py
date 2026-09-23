#!/usr/bin/env python3
"""TB-95 D2: verfaelscht eine KOPIE einer Handelsliste im Scratchpad.

  d_stoerung.py eine_zeile  <kopie.csv>   erste Datenzeile mit Einstiegsjahr 2024 entfernen
  d_stoerung.py jede_dritte <kopie.csv>   nur jede dritte Datenzeile behalten

Weigert sich, eine Datei unter dem Repo-Pfad research/tb24_haltedauern/ zu aendern.
"""
import os
import sys

art, pfad = sys.argv[1], os.path.realpath(sys.argv[2])
REPO = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if pfad.startswith(os.path.join(REPO, "research")):
    sys.exit(f"VERWEIGERT: {pfad} liegt im Repo, nicht in der Kopie")
z = open(pfad, encoding="utf-8").read().splitlines(True)
if art == "eine_zeile":
    i = next(k for k, s in enumerate(z) if k > 0 and s.split(",")[2].startswith("2024"))
    neu = z[:i] + z[i + 1:]
    print(f"    entfernt: Zeile {i + 1} der Datei (Einstiegsjahr 2024); {len(z)} -> {len(neu)} Zeilen")
elif art == "jede_dritte":
    neu = [z[0]] + [s for k, s in enumerate(z[1:]) if k % 3 == 0]
    print(f"    behalten: jede dritte Datenzeile; {len(z)} -> {len(neu)} Zeilen")
else:
    sys.exit(f"unbekannte Art {art}")
open(pfad, "w", encoding="utf-8").writelines(neu)
print(f"    geaendert: {pfad}")

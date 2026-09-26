"""TB-114 C - Laufbereich nach Block B (Bauart TB-112 a2_vereinigen.py): Vereinigung der drei Listen aus
docs/belege/TB-104/d1_listen.py (Trockenlauf der neun Bots, benchmark.py im Modus, auswertung.py nur Import) aus den
Laeufen von c_laeufe.sh, Unterschied zur Messung TB-112 (docs/belege/TB-112/a2_laufbereich.txt, 81 Module), und ob
research/vorregistrierung/herkunft.py darin steht (R5 (a): erst mit dem Erzeuger).
Aufruf: python3 c_laufbereich.py <liste_trockenlauf> <liste_benchmark> <liste_auswertung>
"""
import sys
typen = {}
for datei in sys.argv[1:]:
    drin = False
    for z in open(datei, encoding="utf-8"):
        z = z.rstrip("\n")
        if z == "LISTE":
            drin = True
            continue
        if drin and z:
            typ, pfad = z.split("\t")
            typen.setdefault(pfad, set()).add(typ)
neu = {p for p in typen if not p.startswith("docs/")}
alt = {z.split("\t")[0] for z in open("docs/belege/TB-112/a2_laufbereich.txt", encoding="utf-8")
       if not z.startswith("#") and z.strip() and not z.startswith("docs/")}
print("TB-112: %d Module, TB-114: %d Module, gemeinsam %d" % (len(alt), len(neu), len(alt & neu)))
print("neu in TB-114 (%d): %s" % (len(neu - alt), sorted(neu - alt)))
print("nicht mehr in TB-114 (%d): %s" % (len(alt - neu), sorted(alt - neu)))
print("research/vorregistrierung/herkunft.py im Laufbereich:", "research/vorregistrierung/herkunft.py" in neu)
print("Messumschlaege (docs/, zaehlen nicht):", sorted(p for p in typen if p.startswith("docs/")))

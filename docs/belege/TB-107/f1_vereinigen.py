"""TB-107 F1 - Vereinigung der drei Laufbereichslisten (Ausgaben von docs/belege/TB-104/d1_listen.py) im
Format von docs/belege/TB-104/d1_laufbereich_vereinigung.txt, und der Unterschied zu den 80 Modulen von TB-104.
Aufruf: python3 f1_vereinigen.py <ziel_vereinigung> <ziel_unterschied> <liste_trockenlauf> <liste_benchmark> <liste_auswertung>
"""
import datetime, sys
ziel, ziel_u = sys.argv[1], sys.argv[2]
typen = {}
for datei in sys.argv[3:]:
    drin = False
    for z in open(datei, encoding="utf-8"):
        z = z.rstrip("\n")
        if z == "LISTE":
            drin = True
            continue
        if drin and z:
            typ, pfad = z.split("\t")
            typen.setdefault(pfad, [])
            if typ not in typen[pfad]:
                typen[pfad].append(typ)
REIHE = ["trockenlauf", "benchmark", "auswertung_import"]
with open(ziel, "w", encoding="utf-8") as f:
    f.write("# TB-107 F1 - Vereinigung der drei Lauf-Typen (Trockenlauf aller neun Bots, benchmark.py im Modus, "
            "auswertung.py nur Import), gemessen am Endstand von TB-107 am %s mit dem Werkzeug aus TB-104 D1\n"
            % datetime.date.today().isoformat())
    f.write("# Messumschlaege (docs/belege/...) sind ausgewiesen, zaehlen aber NICHT zum Laufbereich.\n")
    f.write("# Spalten: Pfad <TAB> Lauf-Typen\n")
    for p in sorted(typen):
        f.write("%s\t%s\n" % (p, ",".join(sorted(typen[p], key=REIHE.index))))
neu = {p for p in typen if not p.startswith("docs/")}
alt = set()
for z in open("docs/belege/TB-104/d1_laufbereich_vereinigung.txt", encoding="utf-8"):
    if z.startswith("#") or not z.strip():
        continue
    p = z.split("\t")[0]
    if not p.startswith("docs/"):
        alt.add(p)
with open(ziel_u, "w", encoding="utf-8") as f:
    f.write("# TB-107 F1 Unterschied zur Laufbereichsmessung TB-104 (d1_laufbereich_vereinigung.txt)\n")
    f.write("TB-104: %d Module, TB-107: %d Module, gemeinsam %d\n" % (len(alt), len(neu), len(alt & neu)))
    f.write("neu in TB-107 (%d):\n" % len(neu - alt))
    for p in sorted(neu - alt):
        f.write("  + %s\t%s\n" % (p, ",".join(typen[p])))
    f.write("nicht mehr in TB-107 (%d):\n" % len(alt - neu))
    for p in sorted(alt - neu):
        f.write("  - %s\n" % p)
print(open(ziel_u).read())

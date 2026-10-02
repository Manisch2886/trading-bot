#!/usr/bin/env python3
"""TB-130 C2: die Tabelle der 12 Marken aus Fable 02a fuer REGISTER_INDEX.md erzeugen (Abschnitt 7 des Index),
aus den Belegen, nicht aus dem Gedaechtnis (Bauart TB-129 c2_index_01a.py): Zeile, Art und Teil aus
registerkopie.py --marken (c1_marken.txt), Ort aus Anhang A (JSON 'stelle'), Wort und Ziel aus der Markenzeile.
Schreibt die Tabelle nach stdout. Aufruf: trading-env/bin/python3 docs/belege/TB-130/c2_index_02a.py <S0>
"""
import json, re, subprocess, sys
S0 = sys.argv[1]
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-130_register_fable_02a.md" % S0], capture_output=True,
                     text=True, check=True).stdout
d = json.loads(auf.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
km = {}
for s in open("docs/belege/TB-130/c1_marken.txt", encoding="utf-8"):
    sp = [x.strip() for x in s.split("|")]
    if len(sp) >= 6 and sp[0].isdigit() and "TB-130, 02.10.2026" in s:
        km[int(sp[0])] = (sp[1], sp[2], sp[3])
L = open("docs/VORREGISTRIERUNG_neuselektion.md", encoding="utf-8").read().split("\n")
RX = re.compile(r"^> ⭐ \*\*(.+?) (PRÄZISIERT|ERGÄNZT|BERICHTIGT) durch (.+?)\*\*")
zeilen = []
for m in d["marken"]:
    m1 = m["m1"].replace("⟨DATUM⟩", "02.10.2026")
    z = [i + 1 for i, s in enumerate(L) if s == m1]
    assert len(z) == 1, m1
    ab, teil, art = km[z[0]]
    mm = RX.match(m1)
    zeilen.append((z[0], "| %s | Z. %d | %s | %s | %s | %s |" % (m["stelle"], z[0], mm.group(2), mm.group(3), art, teil)))
assert len(zeilen) == 12 and len(km) == 12, (len(zeilen), len(km))
print("| alter Ort (Anhang A) | Marke | Wort | durch | Art | T |")
print("|---|---|---|---|---|---|")
print("\n".join(z for _, z in sorted(zeilen)))
print("Zeilen: %d" % len(zeilen), file=sys.stderr)

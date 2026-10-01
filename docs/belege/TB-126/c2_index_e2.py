#!/usr/bin/env python3
"""TB-126 C2: die Tabelle der 88 E-2-Marken fuer REGISTER_INDEX.md erzeugen (Abschnitt 5 des Index), aus
den Belegen, nicht aus dem Gedaechtnis: Zeile aus registerkopie.py --marken (c1_marken.txt), Ort aus Anhang A
(Spalte Registerstelle = JSON 'stelle'), Wort und Ziel aus der Markenzeile. Schreibt die Tabelle nach
stdout; die Sitzung fuegt sie ein. Aufruf: trading-env/bin/python3 docs/belege/TB-126/c2_index_e2.py <S0>
"""
import json, re, subprocess, sys
S0 = sys.argv[1]
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-126_register_e2.md" % S0], capture_output=True,
                     text=True, check=True).stdout
d = json.loads(auf.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
km = {}
for s in open("docs/belege/TB-126/c1_marken.txt", encoding="utf-8"):
    sp = [x.strip() for x in s.split("|")]
    if len(sp) >= 6 and sp[0].isdigit() and "TB-126, 01.10.2026" in s:
        km[int(sp[0])] = (sp[1], sp[2], sp[3])
L = open("docs/VORREGISTRIERUNG_neuselektion.md", encoding="utf-8").read().split("\n")
RX = re.compile(r"^> ⭐ \*\*(.+?) (PRÄZISIERT|ERGÄNZT|BERICHTIGT)( \(Verweis\))? durch (.+?)\*\*")
zeilen = []
eintraege = [(m["stelle"], m["m1"].replace("⟨DATUM⟩", "01.10.2026")) for m in d["marken"]]
eintraege.append(("48.16 (R48), neu in TB-126", d["r54_unter_48_16"]["m1"].replace("⟨DATUM⟩", "01.10.2026")))
for stelle, m1 in eintraege:
    z = [i + 1 for i, s in enumerate(L) if s == m1]
    assert len(z) == 1, m1
    ab, teil, art = km[z[0]]
    mm = RX.match(m1)
    wort = mm.group(2) + (mm.group(3) or "")
    zeilen.append("| %s | Z. %d | %s | %s | %s | %s |" % (stelle, z[0], wort, mm.group(4), art, teil))
print("| alter Ort (Anhang A) | Marke | Wort | durch | Art | T |")
print("|---|---|---|---|---|---|")
print("\n".join(zeilen))
print("Zeilen: %d" % len(zeilen), file=sys.stderr)

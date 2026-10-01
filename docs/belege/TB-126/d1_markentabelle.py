#!/usr/bin/env python3
"""TB-126 D1: Markentabelle fuer das Ergebnis aus a6_marken.txt (gesetzt, Zeile) und Anhang A (Ort, Wort) am S0 (Spaltenkopf danach von Hand: "R (Unterpunkt)", "Wort und Ziel");
ersetzt den Platzhalter ⟪MARKENTABELLE⟫ im Ergebnisdokument. Aufruf: ... d1_markentabelle.py <S0>"""
import json, re, subprocess, sys
S0 = sys.argv[1]
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-126_register_e2.md" % S0], capture_output=True,
                     text=True, check=True).stdout
d = json.loads(auf.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
st = {}
for s in open("docs/belege/TB-126/a6_marken.txt", encoding="utf-8"):
    m = re.match(r"^Nr\s+(\d+) R\S*\s+(?:\(unter 48\.16\) )?(gesetzt|NICHT GESETZT/FALSCH) Zeile (\S+)", s)
    if m:
        st[int(m.group(1))] = (m.group(2), m.group(3))
z = ["| Nr | R (x.n) | alter Ort | Wort | Zeile | Stand |", "|---|---|---|---|---|---|"]
for m in d["marken"] + [dict(nr=88, R=54, stelle="48.16 (R48), neu in TB-126", m1=d["r54_unter_48_16"]["m1"], unterpunkt="")]:
    w = re.search(r" (PRÄZISIERT|ERGÄNZT|BERICHTIGT)( \(Verweis\))? durch (.+?)\*\*", m["m1"])
    r = ("R%d %s" % (m["R"], m.get("unterpunkt") or "")).strip() if m["R"] else "B3"
    g, zl = st[m["nr"]]
    z.append("| %d | %s | %s | %s | %s | %s |" % (m["nr"], r, m["stelle"], w.group(1) + (w.group(2) or "") + " durch " + w.group(3), zl, g))
P = "docs/ERGEBNIS_TB-126_register_e2.md"
t = open(P, encoding="utf-8").read()
assert t.count("⟪MARKENTABELLE⟫") == 1
open(P, "w", encoding="utf-8").write(t.replace("⟪MARKENTABELLE⟫", "\n".join(z)))
print("Zeilen:", len(z) - 2, "gesetzt:", sum(1 for v in st.values() if v[0] == "gesetzt"))

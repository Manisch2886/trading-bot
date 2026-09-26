"""TB-116 C, Zusatz 2: Kombinationen, die alle 19 683 Tabellen beantworten (und mit Buchsumme 1);
die Tabellen, in denen die 24 vollstaendigen Kombinationen nur EINEN Vektor ergeben; ob L1b-L2b
und L1c-L2b je auseinanderfallen. Liest c_pruefung.json und c_paare.json, rechnet mit dem Werkzeug.
Aufruf aus der Repo-Wurzel."""
import json
import sys
sys.path.insert(0, "research/leiter_pruefung")
import leiter_lesarten as L  # noqa: E402

B = "docs/belege/TB-116/"
je = json.load(open(B + "c_pruefung.json", encoding="utf-8"))["je_lesart"]
alle = [n for n, v in je.items() if v["tabellen_mit_eindeutigem_vektor"] == 19683]
s1 = [n for n in alle if je[n]["buchsumme_ungleich_1"] == 0]
print("Kombinationen %d, alle Tabellen beantwortet %d, davon Buchsumme 1 in jeder Tabelle %d" % (len(je), len(alle), len(s1)))
voll = json.load(open(B + "c_paare.json", encoding="utf-8"))["vollstaendige_kombinationen"]
print("vollstaendig (c_paare) == Summe-1-Liste:", sorted(voll) == sorted(s1))
les = {L.lesart_name(l): l for l in L.alle_lesarten()}
eins, d = [], 0
for t in L.alle_tabellen():
    if len({L.rechne(t, les[n])["schluessel"] for n in voll}) == 1:
        eins.append(L.tabelle_text(t))
    for r in ("L3a", "L3b"):
        for q in ("L4a", "L4b"):
            for f in ("L5a", "L5b"):
                a = L.rechne(t, {"L1": "L1b", "L2": "L2b", "L3": r, "L4": q, "L5": f})
                b = L.rechne(t, {"L1": "L1c", "L2": "L2b", "L3": r, "L4": q, "L5": f})
                d += (a["schluessel"], a["benchmark"]) != (b["schluessel"], b["benchmark"])
print("Tabellen mit genau einem Vektor unter den %d vollstaendigen Kombinationen: %d" % (len(voll), len(eins)))
for e in eins:
    print("  " + e)
print("L1b-L2b gegen L1c-L2b (je L3, L4a/L4b, L5): Abweichungen in m oder Benchmark: %d" % d)

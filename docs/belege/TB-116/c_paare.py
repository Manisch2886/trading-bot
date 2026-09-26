"""TB-116 C, Zusatz: je Stelle und Optionspaar die Zahl der Tabellen mit verschiedenem m
(uebrige Stellen fest, mindestens eine Belegung), und fuer die Kombinationen, die ALLE
19 683 Tabellen mit Buchsumme 1 beantworten ("vollstaendig"), die Zahl verschiedener
Vektoren je Tabelle. Benutzt leiter_lesarten.py als Bibliothek, aendert es nicht.
Aufruf aus der Repo-Wurzel: trading-env/bin/python3 docs/belege/TB-116/c_paare.py
"""
import itertools
import json
import sys
from collections import Counter, defaultdict

sys.path.insert(0, "research/leiter_pruefung")
import leiter_lesarten as L  # noqa: E402

tabellen = L.alle_tabellen()
lesarten = L.alle_lesarten()
namen = [L.lesart_name(l) for l in lesarten]
paar = defaultdict(set)
paar_bench = defaultdict(set)
vollst = {n: True for n in namen}
ergebnisse = {}
for t in tabellen:
    erg = {n: L.rechne(t, l) for l, n in zip(lesarten, namen)}
    for n, e in erg.items():
        if not e["antwort"] or e["buchsumme"] != 1:
            vollst[n] = False
    alle = {n: (e["schluessel"], L._schluessel(e["benchmark"])) for n, e in erg.items() if e["antwort"]}
    ergebnisse[t] = {n: x for n, x in alle.items() if vollst[n]}   # nur, was noch vollstaendig sein kann
    for st in L.STELLEN:
        andere = [x for x in L.STELLEN if x != st]
        gruppen = defaultdict(list)
        for l, n in zip(lesarten, namen):
            if erg[n]["antwort"]:
                gruppen[tuple(l[x] for x in andere)].append((l[st], alle[n]))
        for glieder in gruppen.values():
            for (o1, (m1, b1)), (o2, (m2, b2)) in itertools.combinations(glieder, 2):
                if m1 != m2:
                    paar[st, o1, o2].add(t)
                elif b1 != b2:
                    paar_bench[st, o1, o2].add(t)

v = [n for n in namen if vollst[n]]
verteilung = Counter(len({ergebnisse[t][n][0] for n in v}) for t in tabellen)
verteilung_b = Counter(len({ergebnisse[t][n] for n in v}) for t in tabellen)
aus = {
    "paare_m_verschieden": {"%s %s≠%s" % k: len(s) for k, s in sorted(paar.items())},
    "paare_nur_benchmark_verschieden": {"%s %s≠%s" % k: len(s - paar[k]) for k, s in sorted(paar_bench.items())},
    "vollstaendige_kombinationen": v,
    "vollstaendig_verschiedene_m_je_tabelle": dict(sorted(verteilung.items())),
    "vollstaendig_verschiedene_m_und_benchmark_je_tabelle": dict(sorted(verteilung_b.items())),
}
print(json.dumps(aus, ensure_ascii=False, indent=1))

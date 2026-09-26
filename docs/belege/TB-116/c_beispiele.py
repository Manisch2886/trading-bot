"""TB-116 C, Zusatz 3: Anschauungsbeispiele fuer das Ergebnis (je Stelle eine Tabelle, Lesart
gegen Lesart; Bezug L1b-L2b-L3a-L4a-L5a, abweichend nur die genannte Stelle). Aufruf aus der Repo-Wurzel."""
import sys
sys.path.insert(0, "research/leiter_pruefung")
import leiter_lesarten as L  # noqa: E402

print("Bots:", " ".join(L.BOTS))
for t, k in [("FA:G UA:GGG FK:GG UK:GGG", {"L1": "L1a"}), ("FA:G UA:GGG FK:GG UK:GGG", {}),
             ("FA:G UA:SSS FK:GG UK:GGG", {"L2": "L2a"}), ("FA:G UA:SSS FK:GG UK:GGG", {}),
             ("FA:G UA:SSS FK:GG UK:GGG", {"L2": "L2a", "L1": "L1c"}), ("FA:G UA:SSS FK:GG UK:GGG", {"L2": "L2c"}),
             ("FA:G UA:GGS FK:GG UK:GGG", {}), ("FA:G UA:GGS FK:GG UK:GGG", {"L4": "L4b"}),
             ("FA:G UA:GGS FK:GG UK:GGG", {"L4": "L4c"}), ("FA:G UA:GGS FK:GG UK:GGG", {"L4": "L4d"}),
             ("FA:S UA:SSS FK:GG UK:GGG", {}), ("FA:S UA:SSS FK:GG UK:GGG", {"L3": "L3b"}),
             ("FA:G UA:GGB FK:GG UK:GGG", {}), ("FA:G UA:GGB FK:GG UK:GGG", {"L5": "L5b"})]:
    l = {"L1": "L1b", "L2": "L2b", "L3": "L3a", "L4": "L4a", "L5": "L5a"}
    l.update(k)
    e = L.rechne(L.tabelle_aus_text(t), l)
    if e["antwort"]:
        print("%s  %s  m=(%s)  Benchmark A/K=%s  Buchsumme=%s" % (
            t, L.lesart_name(l), " ".join(L.bruch(x) for x in e["m"]),
            "/".join(L.bruch(x) for x in e["benchmark"]), L.bruch(e["buchsumme"])))
    else:
        print("%s  %s  keine Antwort: %s" % (t, L.lesart_name(l), e["fehlt"]))

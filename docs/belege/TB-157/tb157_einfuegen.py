#!/usr/bin/env python3
# TB-157 Werkzeug (Python 3.9): fuegt die Stuecke aus Anhang A des Auftrags ein, nur in die Zieldateien dort.
# Liest nur den Auftrag und die Zieldateien; holt keine Zeile aus UEBERGABE.md. Prueft alles, bevor es schreibt.
# Aufruf im Repo: PY WZ probe | einfuegen | vergleich | numstat <a> <b> [j_block] | journal <j_block> [--probe]
# rc 0 gut · 1 numstat/vergleich abweichend · 2 abgewiesen, nichts geschrieben · 3 ABBRUCH, nichts geschrieben · 64 falscher Aufruf
import hashlib, json, re, subprocess, sys
AUF = "docs/auftraege/MAC_TB-157_regelwerk_nachtrag_1013.md"
JOU = "docs/projektfuehrung/JOURNAL.md"
ERG = "docs/ERGEBNIS_TB-157_regelwerk_nachtrag_1013.md"
BEL = "docs/belege/TB-157/"

def lies(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def md5(p):
    return hashlib.md5(lies(p).encode("utf-8")).hexdigest()

def auftrag():
    z = lies(AUF).split("\n")
    a = z.index("## Anhang A — Stücke (wörtlich)")
    b = z.index("## Anhang B — Werkzeug und Sollwerte")
    st, i = [], a
    while i < b:
        if z[i].startswith("#### "):
            d, j = {"id": z[i][5:].split(" — ")[0]}, i + 1
            while j < b and z[j] != "~~~" and not z[j].startswith("#### "):
                m = re.match(r"^(Zieldatei|Art|Form|Anker|Alt|Neu): (.*)$", z[j])
                if m:
                    d[m.group(1)] = m.group(2)
                j += 1
            d["text"] = []
            if j < b and z[j] == "~~~":
                k = z.index("~~~", j + 1)
                d["text"], j = z[j + 1:k], k + 1
            i = j
            d["datei"] = d["Zieldatei"].strip("`")
            for f in ("Anker", "Alt", "Neu"):
                v = d.get(f, "")
                d[f] = v[1:-1] if v.startswith("⟦") and v.endswith("⟧") else ""
            st.append(d)
        else:
            i += 1
    c = z.index("```json", z.index("### Sollwerte (maschinenlesbar)"))
    return st, json.loads("\n".join(z[c + 1:z.index("```", c + 1)]))

def plan(st, soll):
    fehler, schon, dat, ein, bil, aus = [], [], {}, {}, {}, []
    for d in st:
        if d["datei"] not in dat:
            dat[d["datei"]] = lies(d["datei"]).split("\n")
            ein[d["datei"]], bil[d["datei"]] = {}, [0, 0]
    neutext = "\n".join("\n".join(d["text"]) + "\n" + d["Neu"] for d in st)
    ers = {p: list(z) for p, z in dat.items()}
    for d in st:
        p, z, art = d["datei"], dat[d["datei"]], d["Art"]
        t = [i for i, s in enumerate(z) if d["Anker"] and d["Anker"] in s]
        if art == "ende":
            pos, nz, sch = len(z) - 1 if z[-1] == "" else len(z), "-", d["text"][0] in z
        else:
            if len(t) != 1:
                fehler.append("%s: Anker trifft %d Zeilen" % (d["id"], len(t)))
                aus.append("%s · %s · Anker %d Treffer · FEHL" % (d["id"], p, len(t)))
                continue
            nz = t[0] + 1
            if d["Anker"] in neutext:
                fehler.append("%s: Anker steht in einem neuen Text" % d["id"])
        if art == "ersetzen":
            s = z[t[0]]
            na, nn = "\n".join(z).count(d["Alt"]), "\n".join(z).count(d["Neu"])
            if na == 0 and nn == 1:
                schon.append(d["id"])
            elif s.count(d["Alt"]) != 1 or na != 1 or nn != 0:
                fehler.append("%s: Alt in Ankerzeile %d, in Datei %d, Neu in Datei %d" % (d["id"], s.count(d["Alt"]), na, nn))
            else:
                ers[p][t[0]] = s.replace(d["Alt"], d["Neu"])
                bil[p][0] += 1; bil[p][1] += 1
            aus.append("%s · %s · Anker Z. %d · ersetzen · Alt %d · Neu %d · ok" % (d["id"], p, nz, na, nn))
            continue
        if art in ("nach", "vor"):
            pos = t[0] + 1 if art == "nach" else t[0]
            sch = d["text"][0] in z
            if d["Form"] == "Zeilen" and d["text"][0].startswith("|") and not z[t[0]].startswith("|"):
                fehler.append("%s: Tabellenzeile an einer Zeile ohne Tabelle" % d["id"])
        if sch:
            schon.append(d["id"])
        ein[p].setdefault(pos, []).append(d)
        aus.append("%s · %s · Anker Z. %s · %s · Zeilen %d · erste Zeile schon %d · Anker in neuen Texten %d · ok" % (d["id"], p, nz, art, len(d["text"]), int(sch), int(bool(d["Anker"]) and d["Anker"] in neutext)))
    neu = {}
    for p, z in ers.items():
        z = list(z)
        for pos in sorted(ein[p], reverse=True):
            L = []
            for d in ein[p][pos]:
                if d["Form"] == "Block":
                    if L and L[-1] != "":
                        L.append("")
                    L += [""] + d["text"] + [""] if not L else d["text"] + [""]
                else:
                    L += d["text"]
            if L and L[0] == "" and (pos == 0 or z[pos - 1] == ""):
                L = L[1:]
            if L and L[-1] == "" and pos < len(z) and z[pos] == "":
                L = L[:-1]
            z[pos:pos] = L
            bil[p][0] += len(L)
        neu[p] = "\n".join(z)
    return fehler, schon, neu, bil, aus

def bilanz(bil, soll):
    ok = True
    for p in sorted(bil):
        s = soll["zeilen"].get(p)
        g = s == bil[p]
        ok = ok and g
        print("Datei %s · Soll +%s/-%s · Ist +%d/-%d · %s" % (p, s and s[0], s and s[1], bil[p][0], bil[p][1], "gleich" if g else "UNGLEICH"))
    return ok

def vorkommen(z, t):
    return sum(1 for i in range(len(z) - len(t) + 1) if z[i:i + len(t)] == t)

def main(a):
    if not a or a[0] not in ("probe", "einfuegen", "vergleich", "numstat", "journal"):
        print("Aufruf: probe | einfuegen | vergleich | numstat <a> <b> [j_block] | journal <j_block> [--probe]"); return 64
    st, soll = auftrag()
    if a[0] in ("probe", "einfuegen"):
        if len(a) != 1:
            return main([])
        fehler, schon, neu, bil, aus = plan(st, soll)
        print("\n".join(aus))
        if len(st) != soll["stuecke"]:
            fehler.append("Stuecke %d statt %d" % (len(st), soll["stuecke"]))
        if schon and len(schon) == len(st) and not fehler:
            print("ABGEWIESEN, nichts geschrieben: schon eingefuegt: " + ", ".join(schon)); return 2
        if schon:
            fehler.append("erste Zeile schon da: " + ", ".join(schon))
        gl = bilanz(bil, soll)
        print("Stuecke %d · eingefuegte Zeilen %d" % (len(st), sum(b[0] - b[1] for b in bil.values())))
        if fehler or not gl:
            for f in fehler + ([] if gl else ["Zeilenbilanz nicht wie Soll"]):
                print("ABBRUCH: " + f)
            print("ABGEWIESEN, nichts geschrieben"); return 3
        if a[0] == "probe":
            print("Gesamt: wie Soll, nichts geschrieben (Probe)"); return 0
        for p, t in neu.items():
            with open(p, "w", encoding="utf-8") as f:
                f.write(t)
        for p, t in neu.items():
            print("geschrieben und zurueckgelesen: %s · md5 %s · %s" % (p, md5(p), "gleich" if lies(p) == t else "UNGLEICH"))
        print("Gesamt: wie Soll, alle eingefuegt, je genau einmal"); return 0
    if a[0] == "vergleich":
        ok = True
        for d in st:
            z = lies(d["datei"]).split("\n")
            n = "\n".join(z).count(d["Neu"]) if d["Art"] == "ersetzen" and "\n".join(z).count(d["Alt"]) == 0 else (vorkommen(z, d["text"]) if d["text"] else 0)
            ok = ok and n == 1
            print("%s · %s · Vorkommen %d · %s" % (d["id"], d["datei"], n, "GLEICH" if n == 1 else "ABWEICHUNG"))
        print("Gesamt: alle zeichengleich, je genau einmal" if ok else "Gesamt: ABWEICHUNG"); return 0 if ok else 1
    if a[0] == "numstat":
        if len(a) not in (3, 4):
            return main([])
        r = subprocess.run(["git", "diff", "--numstat", a[1], a[2]], capture_output=True, text=True)
        print(r.stdout.rstrip("\n"))
        ist = {}
        for s in r.stdout.splitlines():
            x = s.split("\t")
            ist[x[2]] = [int(x[0]), int(x[1])]
        sl = dict(soll["zeilen"])
        if len(a) == 4:
            sl[JOU] = [len(lies(a[3]).split("\n")) - 1 + 3, 0]
        ok = True
        for p in sorted(sl):
            g = ist.get(p) == sl[p]
            ok = ok and g
            print("Soll %s %d\t%d · Ist %s · %s" % (p, sl[p][0], sl[p][1], ist.get(p), "gleich" if g else "UNGLEICH"))
        w = [p for p in ist if p not in sl and not p.startswith(BEL) and p not in (ERG, AUF)]
        print("weitere Dateien ausser Belegen, Auftrag und Ergebnis: " + (", ".join(w) or "keine"))
        return 0 if ok and not w else 1
    if len(a) not in (2, 3) or (len(a) == 3 and a[2] != "--probe"):
        return main([])
    b, z = lies(a[1]), lies(JOU).split("\n")
    bz = b.split("\n")
    L = [i for i, s in enumerate(z) if s == "## Wiederkehrende Lehren"]
    k = [re.match(r"^## ([A-Z]{2}) — TB-", s).group(1) for s in z[:L[0] if L else 0] if re.match(r"^## ([A-Z]{2}) — TB-", s)]
    letzte = k[-1] if k else "??"
    n2 = chr(ord(letzte[1]) + 1) if letzte[1] != "Z" else "A"
    nk = (letzte[0] if letzte[1] != "Z" else chr(ord(letzte[0]) + 1)) + n2
    be = [("endet mit Zeilenende", b.endswith("\n") and not b.endswith("\n\n")),
          ("Kopfzeile ## %s — TB-157: …" % nk, bz[0].startswith("## %s — TB-157: " % nk)),
          ("### Was gemessen ist genau einmal, Leerzeile davor", bz.count("### Was gemessen ist") == 1 and bz[bz.index("### Was gemessen ist") - 1] == ""),
          ("### Was offen bleibt genau einmal", bz.count("### Was offen bleibt") == 1),
          ("keine Zeile ---", "---" not in bz),
          ("Schlusszeile *Geschrieben …", bz[-2].startswith("*Geschrieben ") if len(bz) > 1 else False),
          ("## Wiederkehrende Lehren genau einmal", len(L) == 1),
          ("davor --- und Leerzeile", len(L) == 1 and z[L[0] - 1] == "" and z[L[0] - 2] == "---"),
          ("Kennung noch frei", not any(s.startswith("## %s — " % nk) for s in z))]
    for t, v in be:
        print("%s: %s" % (t, "ja" if v else "NEIN"))
    print("Kennung %s (erwartet %s) · letzte %s" % (nk, soll["journal_kennung"], letzte))
    if not all(v for _, v in be):
        return 2
    neu = bz[:-1] + ["", "---", ""]
    print("Zeilen +%d" % len(neu))
    if len(a) == 3:
        print("Probe: nichts geschrieben"); return 0
    z[L[0]:L[0]] = neu
    t = "\n".join(z)
    with open(JOU, "w", encoding="utf-8") as f:
        f.write(t)
    print("geschrieben und zurueckgelesen: %s · md5 %s · %s" % (JOU, md5(JOU), "gleich" if lies(JOU) == t else "UNGLEICH"))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

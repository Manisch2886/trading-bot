#!/usr/bin/env python3
# TB-160 Werkzeug (Python 3.9): setzt die Stuecke aus Anhang A des Auftrags ein, nur in die vier Zieldateien dort (ampel.py, ARBEITSWEISE, BACKLOG, UMZUG).
# Liest nur den Auftrag und die Zieldateien. Prueft alles, bevor es schreibt.
# Aufruf im Repo: PY WZ ausgang | probe | einfuegen | vergleich | journal <j_block> [--probe]
# rc 0 gut · 1 vergleich/ausgang abweichend · 2 abgewiesen, nichts geschrieben · 64 falscher Aufruf
import hashlib, json, os, re, sys
AUF = "docs/auftraege/MAC_TB-160_ampel_farbe_schlank.md"
BEL = "docs/belege/TB-160/"
AMP, AW, BL, JOU = ("docs/werkzeuge/ampel.py", "docs/projektfuehrung/ARBEITSWEISE.md",
                    "docs/projektfuehrung/BACKLOG.md", "docs/projektfuehrung/JOURNAL.md")
UM = "docs/projektfuehrung/UMZUG.md"
ZIEL = [AMP, AW, BL, UM]
KURZ = {"ARBEITSWEISE": AW, "UMZUG": UM}

def lies(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def md5t(t):
    return hashlib.md5(t.encode("utf-8")).hexdigest()

def zaun(z, kopf):
    i = z.index(kopf)
    a = z.index("~~~", i)
    e = z.index("~~~", a + 1)
    return z[a + 1:e], e

def stuecke():
    z = lies(AUF).split("\n")
    s = {"A1": zaun(z, "#### A1 — docs/werkzeuge/ampel.py, ganze Datei")[0],
         "A2": zaun(z, "#### A2 — ARBEITSWEISE Abschnitt 0, Absatz vor ⟦**Immer**⟧")[0],
         "B1": zaun(z, "#### B1 — BACKLOG Abschnitt 5, Ende, vor ⟦## 6 — Geparkt⟧")[0], "M": []}
    for k in [x for x in z if x.startswith("#### M")]:
        alt, e = zaun(z, k)
        j = z.index("Neu:", z.index(k))
        a2 = z.index("~~~", j); e2 = z.index("~~~", a2 + 1)
        neu = z[a2 + 1:e2]
        assert len(alt) == 1 and len(neu) == 1, k
        s["M"].append((k.split(" ")[1], KURZ[k.split(" ")[3]], alt[0], neu[0]))
    soll = json.loads("\n".join(zaun(z, "### Sollwerte (maschinenlesbar)")[0]))
    return s, soll

def bauen(s):
    neu, fehler = {}, []
    neu[AMP] = "\n".join(s["A1"]) + "\n"
    z = lies(AW).split("\n")
    u = lies(UM).split("\n")
    k0 = z.index("## 0. Vor jeder Antwort — die Ausgabe-Checkliste")
    i = z.index("**Immer**", k0)
    if z[i - 1] != "":
        fehler.append("A2: vor **Immer** keine Leerzeile")
    for mid, p, alt, nz in s["M"]:
        d = z if p == AW else u
        n = d.count(alt)
        print("%s · %s · Alt Vorkommen %d · %s" % (mid, p, n, "ok" if n == 1 else "FEHLER"))
        if n != 1:
            fehler.append(mid)
        else:
            d[d.index(alt)] = nz
    z[i:i] = s["A2"] + [""]
    print("A2 · ARBEITSWEISE · vor Z. %d · %d Zeilen" % (i + 1, len(s["A2"]) + 1))
    neu[AW] = "\n".join(z)
    neu[UM] = "\n".join(u)
    b = lies(BL).split("\n")
    a = [k for k, x in enumerate(b) if x.startswith("## 6 — Geparkt, null Arbeit")]
    if len(a) != 1 or b[a[0] - 1] != "":
        fehler.append("B1: Anker")
    else:
        b[a[0]:a[0]] = s["B1"] + [""]
        print("B1 · BACKLOG · vor Z. %d · %d Zeilen" % (a[0] + 1, len(s["B1"]) + 1))
    neu[BL] = "\n".join(b)
    return neu, fehler

def main(a):
    if not a or a[0] not in ("ausgang", "probe", "einfuegen", "vergleich", "journal"):
        print(__doc__ or "Aufruf: ausgang | probe | einfuegen | vergleich | journal <j_block> [--probe]")
        return 64
    s, soll = stuecke()
    if a[0] == "ausgang":
        os.makedirs(BEL, exist_ok=True)
        zeilen, ok = [], True
        for p in ZIEL + [JOU]:
            t = lies(p); g = md5t(t) == soll["vor"][p]
            ok = ok and g
            zeilen.append("%s · %d Z. · md5 %s · Soll %s · %s" % (p, len(t.split("\n")) - 1, md5t(t), soll["vor"][p], "gleich" if g else "UNGLEICH"))
        with open(BEL + "0b_ausgang.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(zeilen) + "\n")
        print("\n".join(zeilen))
        return 0 if ok else 1
    if a[0] == "vergleich":
        ok = True
        for p in ZIEL:
            g = md5t(lies(p)) == soll["nach"][p]
            ok = ok and g
            print("%s · md5 %s · %s" % (p, md5t(lies(p)), "GLEICH" if g else "UNGLEICH"))
        print("Gesamt: " + ("alle wie Soll" if ok else "ABWEICHUNG"))
        return 0 if ok else 1
    if a[0] in ("probe", "einfuegen"):
        if len(a) != 1:
            return main([])
        schon = [p for p in ZIEL if md5t(lies(p)) == soll["nach"][p]]
        if schon:
            print("ABGEWIESEN, nichts geschrieben: schon eingefuegt: " + ", ".join(schon)); return 2
        vor = [p for p in ZIEL if md5t(lies(p)) != soll["vor"][p]]
        if vor:
            print("ABGEWIESEN, nichts geschrieben: Ausgang weicht ab: " + ", ".join(vor)); return 2
        neu, fehler = bauen(s)
        for p in ZIEL:
            g = md5t(neu[p]) == soll["nach"][p]
            if not g:
                fehler.append(p)
            print("%s · Soll %s · Ist %s · %s" % (p, soll["nach"][p], md5t(neu[p]), "gleich" if g else "UNGLEICH"))
        if fehler:
            print("ABGEWIESEN, nichts geschrieben: " + ", ".join(fehler)); return 2
        if a[0] == "probe":
            print("Gesamt: wie Soll, nichts geschrieben (Probe)"); return 0
        for p in ZIEL:
            with open(p, "w", encoding="utf-8") as f:
                f.write(neu[p])
            print("geschrieben und zurueckgelesen: %s · %s" % (p, "gleich" if lies(p) == neu[p] else "UNGLEICH"))
        print("Gesamt: wie Soll, alle eingefuegt"); return 0
    if len(a) not in (2, 3) or (len(a) == 3 and a[2] != "--probe"):
        return main([])
    b, z = lies(a[1]), lies(JOU).split("\n")
    bz = b.split("\n")
    L = [i for i, x in enumerate(z) if x == "## Wiederkehrende Lehren"]
    k = [re.match(r"^## ([A-Z]{2}) — TB-", x).group(1) for x in z[:L[0] if L else 0] if re.match(r"^## ([A-Z]{2}) — TB-", x)]
    letzte = k[-1] if k else "??"
    nk = (letzte[0] if letzte[1] != "Z" else chr(ord(letzte[0]) + 1)) + (chr(ord(letzte[1]) + 1) if letzte[1] != "Z" else "A")
    be = [("endet mit Zeilenende", b.endswith("\n") and not b.endswith("\n\n")),
          ("Kopfzeile ## %s — TB-160: …" % nk, bz[0].startswith("## %s — TB-160: " % nk)),
          ("keine Zeile ---", "---" not in bz),
          ("Schlusszeile *Geschrieben …", len(bz) > 1 and bz[-2].startswith("*Geschrieben ")),
          ("## Wiederkehrende Lehren genau einmal", len(L) == 1),
          ("davor --- und Leerzeile", len(L) == 1 and z[L[0] - 1] == "" and z[L[0] - 2] == "---"),
          ("Kennung noch frei", not any(x.startswith("## %s — " % nk) for x in z))]
    for t, v in be:
        print("%s: %s" % (t, "ja" if v else "NEIN"))
    print("Kennung %s (gemessen; am Bau-HEAD erwartet %s) · letzte %s" % (nk, soll["journal_kennung"], letzte))
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
    print("geschrieben und zurueckgelesen: %s · md5 %s · %s" % (JOU, md5t(lies(JOU)), "gleich" if lies(JOU) == t else "UNGLEICH"))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

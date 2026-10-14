#!/usr/bin/env python3
# TB-158 Werkzeug (Python 3.9): fuegt eine Zeile in BACKLOG.md und den Block der Sitzung in JOURNAL.md ein; sonst nichts.
# Prueft alles, bevor es schreibt. Aufruf im Repo: PY WZ backlog <zeile.md> [--probe] | PY WZ journal <block.md> [--probe]
# rc 0 gut · 2 eine Bedingung NEIN, nichts geschrieben · 64 falscher Aufruf. Der Journal-Teil ist der von TB-157 (Kennung EV).
import hashlib, re, sys
JOU = "docs/projektfuehrung/JOURNAL.md"
BAC = "docs/projektfuehrung/BACKLOG.md"
ANKER = "- **`pgrep` ohne `-a`** (UEBERGABE, Nachtrag 13.10.2026, 15:57):"
VOR = "  - **Nachtrag TB-158 ("
ERG = "docs/ERGEBNIS_TB-158_waechter_probe.md"

def lies(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def md5(p):
    return hashlib.md5(lies(p).encode("utf-8")).hexdigest()

def backlog(a):
    if len(a) not in (2, 3) or (len(a) == 3 and a[2] != "--probe"):
        return main([])
    b, z = lies(a[1]), lies(BAC).split("\n")
    k = [i for i, s in enumerate(z) if s.startswith(ANKER)]
    be = [("genau eine Zeile mit Zeilenende", b.endswith("\n") and b.count("\n") == 1),
          ("beginnt mit '%s'" % VOR, b.startswith(VOR)),
          ("nennt %s" % ERG, ERG in b),
          ("keine offene Stelle (kein '<', kein '>')", "<" not in b and ">" not in b),
          ("Anker genau einmal", len(k) == 1),
          ("Nachtrag noch nicht da", not any(s.startswith(VOR) for s in z))]
    for t, v in be:
        print("%s: %s" % (t, "ja" if v else "NEIN"))
    print("Ausgang %s · %d Zeilen · md5 %s" % (BAC, len(z) - 1, md5(BAC)))
    if not all(v for _, v in be):
        return 2
    print("Anker Z. %d · Zeilen +1" % (k[0] + 1))
    if len(a) == 3:
        print("Probe: nichts geschrieben"); return 0
    z[k[0] + 1:k[0] + 1] = [b[:-1]]
    t = "\n".join(z)
    with open(BAC, "w", encoding="utf-8") as f:
        f.write(t)
    print("geschrieben und zurueckgelesen: %s · md5 %s · %s" % (BAC, md5(BAC), "gleich" if lies(BAC) == t else "UNGLEICH"))
    return 0

def journal(a):
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
          ("Kopfzeile ## %s — TB-158: …" % nk, bz[0].startswith("## %s — TB-158: " % nk)),
          ("### Was gemessen ist genau einmal, Leerzeile davor", bz.count("### Was gemessen ist") == 1 and bz[bz.index("### Was gemessen ist") - 1] == ""),
          ("### Was offen bleibt genau einmal", bz.count("### Was offen bleibt") == 1),
          ("keine Zeile ---", "---" not in bz),
          ("Schlusszeile *Geschrieben …", bz[-2].startswith("*Geschrieben ") if len(bz) > 1 else False),
          ("## Wiederkehrende Lehren genau einmal", len(L) == 1),
          ("davor --- und Leerzeile", len(L) == 1 and z[L[0] - 1] == "" and z[L[0] - 2] == "---"),
          ("Kennung noch frei", not any(s.startswith("## %s — " % nk) for s in z))]
    for t, v in be:
        print("%s: %s" % (t, "ja" if v else "NEIN"))
    print("Kennung %s (erwartet %s) · letzte %s" % (nk, "EV", letzte))
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

def main(a):
    f = {"backlog": backlog, "journal": journal}.get(a[0] if a else "")
    if not f:
        print("Aufruf: PY WZ backlog <zeile.md> [--probe] | PY WZ journal <block.md> [--probe]")
        return 64
    return f(a)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
